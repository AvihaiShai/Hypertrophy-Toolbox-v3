/**
 * WP4.4-j — intra-file shadow certification for `theme-dark.css`.
 *
 * j must classify every rule as a legacy value or a justified token remap, and
 * may delete only what is *certified* removable. Most deadness claims need the
 * full M1 apparatus — a sentinel sweep, a rest-state differential and a same-CSS
 * control — because "nothing else declares this" is a statement about the whole
 * cascade across ten routes.
 *
 * One class of deadness is stronger than that and decidable statically: a
 * declaration shadowed **inside its own file, under identical selector text**.
 * Two declarations written with the same selector string necessarily match the
 * same elements on every route, in every state, at every viewport — there is no
 * DOM in which one applies and the other does not. `theme-dark.css` contains no
 * `@layer` (asserted below), so within it the cascade reduces to importance then
 * document order. If a later-or-stronger declaration of the same longhand exists
 * under that same selector, the earlier one cannot win anywhere, and deleting it
 * cannot change a computed value.
 *
 * The certification is deliberately conservative:
 *
 *   - **Custom properties are never candidates** (M9). A `var()` consumer in any
 *     of the other twenty hand-maintained sources keeps them live, and proving
 *     otherwise needs a dependency graph, not an ownership sweep.
 *   - A declaration in a rule with N selectors must be shadowed under **every**
 *     one of them. Shadowed under two of three means deleting it changes
 *     rendering under the third.
 *   - Shorthands are expanded to longhands in both directions, so
 *     `background: none` correctly shadows an earlier `background-color`, and a
 *     shorthand is only certified when every longhand it sets is shadowed.
 *   - A rule is only removed when **all** of its declarations are certified.
 *
 * The result is still confirmed by a full dark-theme differential, because a
 * static proof that is wrong about the file is still wrong. This narrows what
 * must be trusted; it does not replace the measurement.
 *
 * usage:
 *   node scripts/css_audit/j_shadow_certification.mjs [--out <file.json>] [--apply]
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
const apply = argv.includes('--apply');
const outPath = arg('--out') ? resolve(arg('--out')) : null;

/** Shorthand -> the longhands it sets. Only those this file actually uses. */
const LONGHANDS = {
  border: ['border-top-width', 'border-right-width', 'border-bottom-width', 'border-left-width',
    'border-top-style', 'border-right-style', 'border-bottom-style', 'border-left-style',
    'border-top-color', 'border-right-color', 'border-bottom-color', 'border-left-color'],
  'border-color': ['border-top-color', 'border-right-color', 'border-bottom-color', 'border-left-color'],
  'border-width': ['border-top-width', 'border-right-width', 'border-bottom-width', 'border-left-width'],
  'border-style': ['border-top-style', 'border-right-style', 'border-bottom-style', 'border-left-style'],
  background: ['background-color', 'background-image', 'background-position', 'background-size',
    'background-repeat', 'background-origin', 'background-clip', 'background-attachment'],
  padding: ['padding-top', 'padding-right', 'padding-bottom', 'padding-left'],
  margin: ['margin-top', 'margin-right', 'margin-bottom', 'margin-left'],
};
const expand = (prop) => LONGHANDS[prop] ?? [prop];

const source = readFileSync(CSS_PATH);
const root = postcss.parse(source.toString('utf8'), { from: CSS_PATH });

// The whole argument below assumes plain document order inside this file.
root.walkAtRules((at) => {
  if (at.name === 'layer') {
    throw new Error('theme-dark.css declares @layer; the document-order argument no longer holds');
  }
});

const decls = [];
root.walkRules((rule) => {
  // A declaration inside `@media` applies only in that context; comparing it
  // with an unconditional one would be comparing different cascades.
  if (rule.parent && rule.parent.type === 'atrule') return;
  const selectors = rule.selectors.map((s) => s.replace(/\s+/g, ' ').trim());
  rule.walkDecls((d) => {
    decls.push({
      node: d,
      rule,
      line: d.source.start.line,
      prop: d.prop,
      value: d.value,
      important: d.important,
      selectors,
      order: decls.length,
    });
  });
});

/** Winner per (selector, longhand): importance first, then document order. */
const winner = new Map();
for (const d of decls) {
  if (d.prop.startsWith('--')) continue;
  for (const sel of d.selectors) {
    for (const lh of expand(d.prop)) {
      const key = `${sel}||${lh}`;
      const cur = winner.get(key);
      if (!cur) { winner.set(key, d); continue; }
      if (d.important && !cur.important) { winner.set(key, d); continue; }
      if (d.important === cur.important && d.order > cur.order) winner.set(key, d);
    }
  }
}

const certified = [];
for (const d of decls) {
  if (d.prop.startsWith('--')) continue; // M9
  let shadowedEverywhere = true;
  for (const sel of d.selectors) {
    for (const lh of expand(d.prop)) {
      if (winner.get(`${sel}||${lh}`) === d) { shadowedEverywhere = false; break; }
    }
    if (!shadowedEverywhere) break;
  }
  if (!shadowedEverywhere) continue;
  const w = winner.get(`${d.selectors[0]}||${expand(d.prop)[0]}`);
  certified.push({
    line: d.line,
    prop: d.prop,
    value: d.value,
    important: d.important,
    selectorCount: d.selectors.length,
    shadowedBy: { line: w.line, prop: w.prop, value: w.value, important: w.important },
    node: d.node,
    rule: d.rule,
  });
}

// A rule whose every declaration is certified is removed whole.
const certifiedNodes = new Set(certified.map((c) => c.node));
const emptiedRules = [];
const seenRules = new Set();
for (const c of certified) {
  if (seenRules.has(c.rule)) continue;
  seenRules.add(c.rule);
  let all = true;
  c.rule.walkDecls((d) => { if (!certifiedNodes.has(d)) all = false; });
  if (all) {
    emptiedRules.push({
      startLine: c.rule.source.start.line,
      endLine: c.rule.source.end.line,
      selector: c.rule.selector.replace(/\s+/g, ' '),
    });
  }
}

const report = {
  generatedFrom: 'scripts/css_audit/j_shadow_certification.mjs',
  cssFile: 'static/css/theme-dark.css',
  cssSha256Before: createHash('sha256').update(source).digest('hex'),
  basis: 'intra-file shadowing under identical selector text; no @layer in file; importance then document order',
  totals: {
    declarationsExaminedExcludingCustomProperties: decls.filter((d) => !d.prop.startsWith('--')).length,
    certifiedDeclarations: certified.length,
    rulesRemovedWhole: emptiedRules.length,
  },
  certified: certified.map(({ node, rule, ...rest }) => rest),
  emptiedRules,
};

if (apply) {
  for (const c of certified) c.node.remove();
  for (const rule of seenRules) {
    let empty = true;
    rule.walkDecls(() => { empty = false; });
    if (empty) rule.remove();
  }
  const out = root.toResult().css;
  writeFileSync(CSS_PATH, out, 'utf8');
  report.cssSha256After = createHash('sha256').update(readFileSync(CSS_PATH)).digest('hex');
}

if (outPath) {
  mkdirSync(dirname(outPath), { recursive: true });
  writeFileSync(outPath, `${JSON.stringify(report, null, 2)}\n`);
}

console.log(JSON.stringify(report.totals, null, 2));
for (const c of report.certified) {
  console.log(`  :${c.line} ${c.prop}${c.important ? ' !important' : ''} = ${c.value.slice(0, 40)}  <- shadowed by :${c.shadowedBy.line} ${c.shadowedBy.prop}`);
}
console.log(`rules removed whole: ${emptiedRules.map((r) => `${r.startLine}-${r.endLine}`).join(', ') || 'none'}`);
if (apply) console.log(`\napplied. ${report.cssSha256Before} -> ${report.cssSha256After}`);
