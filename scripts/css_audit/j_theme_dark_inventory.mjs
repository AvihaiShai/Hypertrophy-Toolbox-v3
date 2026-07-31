/**
 * WP4.4-j — `theme-dark.css` rule inventory.
 *
 * j classifies every rule in the file as a **legacy value** (delete only if
 * removal is certified) or a **justified token remap** (retain, documented).
 * That triage has to start from a structural census that is reproducible, not
 * from a hand count: the plan's "81 top-level rules / 149 `!important` / 1
 * `@media`" figures are the acceptance surface, and a packet that cannot
 * regenerate them cannot show it classified all of them.
 *
 * The census also separates the two populations the rules M9 and C11 protect:
 *
 *   - **custom-property declarations** (`--x: …`). M9 forbids deleting any of
 *     these under the non-winner rule — a `var()` consumer in any of the other
 *     20 hand-maintained sources keeps them live, and proving otherwise needs a
 *     dependency graph rather than an ownership sweep.
 *   - **`@media (prefers-reduced-motion: reduce)`** and the `.value-changed`
 *     rules, which C11 retains outright.
 *
 * Emits JSON so the evidence document quotes a file rather than a transcript.
 *
 * usage:
 *   node scripts/css_audit/j_theme_dark_inventory.mjs [--out <file.json>]
 */
import postcss from 'postcss';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const CSS_PATH = join(ROOT, 'static/css/theme-dark.css');

const argv = process.argv.slice(2);
const arg = (name, fallback = null) => {
  const i = argv.indexOf(name);
  return i < 0 ? fallback : argv[i + 1];
};
const outPath = arg('--out') ? resolve(arg('--out')) : null;

const source = readFileSync(CSS_PATH);
const css = source.toString('utf8');
const root = postcss.parse(css, { from: CSS_PATH });

const rules = [];
let topLevelRules = 0;
let atRules = 0;

const describe = (node) => {
  let custom = 0;
  let normal = 0;
  let important = 0;
  const customProps = [];
  node.walkDecls((decl) => {
    if (decl.important) important += 1;
    if (decl.prop.startsWith('--')) { custom += 1; customProps.push(decl.prop); }
    else normal += 1;
  });
  return { custom, normal, important, customProps };
};

root.each((node) => {
  if (node.type === 'rule') {
    topLevelRules += 1;
    const d = describe(node);
    rules.push({
      kind: 'rule',
      startLine: node.source.start.line,
      endLine: node.source.end.line,
      selector: node.selector.replace(/\s+/g, ' '),
      // A rule declaring only custom properties is a token remap by construction:
      // it changes no property directly, it re-points variables the other bundles
      // consume. M9 protects every one of these declarations.
      population: d.custom && !d.normal ? 'token-remap'
        : (d.custom && d.normal ? 'mixed' : 'value-override'),
      ...d,
    });
  } else if (node.type === 'atrule') {
    atRules += 1;
    const d = describe(node);
    const inner = [];
    node.walkRules((r) => inner.push(r.selector.replace(/\s+/g, ' ')));
    rules.push({
      kind: 'atrule',
      startLine: node.source.start.line,
      endLine: node.source.end.line,
      selector: `@${node.name} ${node.params}`,
      population: 'at-rule',
      innerSelectors: inner,
      ...d,
    });
  }
});

const totals = {
  topLevelRules,
  atRules,
  total: topLevelRules + atRules,
  lines: css.split(/\r?\n/).length - (css.endsWith('\n') ? 1 : 0),
  importantDeclarations: rules.reduce((n, r) => n + r.important, 0),
  customPropertyDeclarations: rules.reduce((n, r) => n + r.custom, 0),
  normalDeclarations: rules.reduce((n, r) => n + r.normal, 0),
  byPopulation: rules.reduce((acc, r) => { acc[r.population] = (acc[r.population] ?? 0) + 1; return acc; }, {}),
};

const report = {
  generatedFrom: 'scripts/css_audit/j_theme_dark_inventory.mjs',
  cssFile: 'static/css/theme-dark.css',
  cssSha256: createHash('sha256').update(source).digest('hex'),
  totals,
  rules,
};

if (outPath) {
  mkdirSync(dirname(outPath), { recursive: true });
  writeFileSync(outPath, `${JSON.stringify(report, null, 2)}\n`);
}

console.log(`theme-dark.css ${report.cssSha256}`);
console.log(JSON.stringify(totals, null, 2));
for (const r of rules) {
  console.log(
    `${String(r.startLine).padStart(4)}-${String(r.endLine).padEnd(4)} ${r.population.padEnd(14)} `
    + `custom=${String(r.custom).padStart(2)} normal=${String(r.normal).padStart(2)} imp=${String(r.important).padStart(2)}  `
    + r.selector.slice(0, 100),
  );
}
