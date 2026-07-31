/**
 * WP4.4-j — diff two `j_theme_differential.mjs` captures.
 *
 * j's rollback criteria are absolute in both directions: any dark-mode
 * difference, and any light-mode difference at all. So differences are reported
 * partitioned by theme, and a light-theme difference is called out separately —
 * a dark-only file that moves light rendering means the classification was
 * wrong, which is a different and worse failure than a dark regression.
 *
 * Refusals mirror the WP4.4-i differs: the two halves must come from different
 * checkouts and must have served different `theme-dark.css` bytes, both halves'
 * own controls must have passed, and an empty comparison is not a pass.
 *
 * usage:
 *   node scripts/css_audit/j_diff_theme.mjs <before/> <after/> [--out <dir>]
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve, join } from 'node:path';

const argv = process.argv.slice(2);
const arg = (name, fallback = null) => {
  const i = argv.indexOf(name);
  return i < 0 ? fallback : argv[i + 1];
};
const positional = [];
for (let i = 0; i < argv.length; i += 1) {
  if (argv[i].startsWith('--')) { i += 1; continue; }
  positional.push(argv[i]);
}
const [beforeDir, afterDir] = positional;
if (!beforeDir || !afterDir) throw new Error('usage: j_diff_theme.mjs <before/> <after/> [--out <dir>]');
const outDir = arg('--out') ? resolve(arg('--out')) : null;

const load = (dir) => ({
  meta: JSON.parse(readFileSync(join(dir, 'meta.json'), 'utf8')),
  computed: JSON.parse(readFileSync(join(dir, 'computed.json'), 'utf8')),
});
const before = load(beforeDir);
const after = load(afterDir);

const fatal = [];
const must = (cond, msg) => { if (!cond) fatal.push(msg); };

const bm = before.meta.meta;
const am = after.meta.meta;
must(Boolean(bm.root) && Boolean(am.root) && bm.root !== am.root,
  `both halves were captured from the same root ${bm.root}`);
must(Boolean(bm.themeDarkCssSha256) && Boolean(am.themeDarkCssSha256)
  && bm.themeDarkCssSha256 !== am.themeDarkCssSha256,
  `both halves served the same theme-dark.css ${bm.themeDarkCssSha256} — nothing under test changed`);
for (const [label, m] of [['before', bm], ['after', am]]) {
  must(m.servedThemeDarkCssSha256 === m.themeDarkCssSha256,
    `${label} half served ${m.servedThemeDarkCssSha256} but its checkout has ${m.themeDarkCssSha256}`);
  must(m.controlsPassed === true, `${label} half's own controls did not pass`);
}
must(Boolean(bm.frozenDbSha256) && bm.frozenDbSha256 === am.frozenDbSha256,
  `frozen DB differs or was not recorded: ${bm.frozenDbSha256} vs ${am.frozenDbSha256}`);
must(JSON.stringify(bm.properties) === JSON.stringify(am.properties),
  'the two halves measured different property sets');

const beforeCtx = Object.keys(before.computed.contexts).sort();
const afterCtx = Object.keys(after.computed.contexts).sort();
must(beforeCtx.length > 0, 'before half captured zero contexts; an empty comparison is not a pass');
const onlyBefore = beforeCtx.filter((k) => !afterCtx.includes(k));
const onlyAfter = afterCtx.filter((k) => !beforeCtx.includes(k));
must(onlyBefore.length === 0 && onlyAfter.length === 0,
  `context drift: onlyBefore=${onlyBefore} onlyAfter=${onlyAfter}`);

const differences = [];
const elementDrift = [];
let elements = 0;
let values = 0;
for (const ctx of beforeCtx) {
  const b = before.computed.contexts[ctx];
  const a = after.computed.contexts[ctx] ?? {};
  const bKeys = Object.keys(b);
  const aKeys = Object.keys(a);
  if (bKeys.length !== aKeys.length) {
    elementDrift.push({ context: ctx, before: bKeys.length, after: aKeys.length });
  }
  for (const el of bKeys) {
    if (!a[el]) { elementDrift.push({ context: ctx, element: el, missing: 'after' }); continue; }
    elements += 1;
    for (const prop of Object.keys(b[el])) {
      values += 1;
      if (b[el][prop] !== a[el][prop]) {
        differences.push({ context: ctx, theme: ctx.split('|')[1], route: ctx.split('|')[0], element: el, prop, before: b[el][prop], after: a[el][prop] });
      }
    }
  }
}

const light = differences.filter((d) => d.theme === 'light');
const dark = differences.filter((d) => d.theme === 'dark');

const report = {
  generatedFrom: 'scripts/css_audit/j_diff_theme.mjs',
  before: { root: bm.root, css: bm.themeDarkCssSha256 },
  after: { root: am.root, css: am.themeDarkCssSha256 },
  db: bm.frozenDbSha256,
  compared: { contexts: beforeCtx.length, elements, values },
  elementDrift,
  differences: { total: differences.length, light: light.length, dark: dark.length },
  sample: differences.slice(0, 50),
  fatal,
  passed: fatal.length === 0 && differences.length === 0 && elementDrift.length === 0,
};
if (outDir) {
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'diff.json'), `${JSON.stringify(report, null, 2)}\n`);
}

console.log(`before ${bm.root}\n       theme-dark.css ${bm.themeDarkCssSha256}`);
console.log(`after  ${am.root}\n       theme-dark.css ${am.themeDarkCssSha256}`);
console.log(`compared ${beforeCtx.length} contexts, ${elements} elements, ${values} computed values`);
console.log(`element drift:      ${elementDrift.length}`);
console.log(`LIGHT differences:  ${light.length}`);
console.log(`DARK differences:   ${dark.length}`);
for (const d of report.sample.slice(0, 12)) {
  console.log(`  ${d.context} ${d.prop}: "${d.before}" -> "${d.after}"  ${d.element.slice(-60)}`);
}
for (const m of fatal) console.log(`FATAL: ${m}`);
console.log(report.passed ? '\nPASS — zero computed-value differences in either theme' : '\nFAIL — see diff.json');
process.exit(report.passed ? 0 : 1);
