/**
 * WP4.4-i — diff two `i_five_route_computed.mjs` captures.
 *
 * The packet's success criterion is that computed values are identical while
 * ownership becomes honest, and its rollback criterion is ANY unexplained
 * rendering difference. So this reports three independent classes of change, not
 * just value drift:
 *
 *   contexts   a context present on one side only — the capture matrix moved
 *   elements   a DOM path present on one side only — the page structure moved,
 *              which a value-only diff would silently score as clean
 *   values     a differing computed value — the thing the repair must not do
 *
 * Exit code is non-zero if any of the three is non-empty, so this is usable as a
 * gate and not only as a report.
 *
 * usage:
 *   node scripts/css_audit/i_diff_computed.mjs <before.json> <after.json> [--out <dir>]
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve, join } from 'node:path';

const [beforePath, afterPath] = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const outArg = process.argv.indexOf('--out');
const outDir = outArg < 0 ? null : resolve(process.argv[outArg + 1]);

const before = JSON.parse(readFileSync(beforePath, 'utf8'));
const after = JSON.parse(readFileSync(afterPath, 'utf8'));

const contextKeys = (capture) => Object.keys(capture.contexts).sort();
const onlyIn = (a, b) => a.filter((key) => !b.includes(key));

const beforeContexts = contextKeys(before);
const afterContexts = contextKeys(after);

const report = {
  before: { root: before.meta.root, css: before.meta.componentsCssSha256 },
  after: { root: after.meta.root, css: after.meta.componentsCssSha256 },
  db: { before: before.meta.frozenDbSha256, after: after.meta.frozenDbSha256 },
  contextsOnlyInBefore: onlyIn(beforeContexts, afterContexts),
  contextsOnlyInAfter: onlyIn(afterContexts, beforeContexts),
  elementDrift: [],
  valueDifferences: [],
  compared: { contexts: 0, elements: 0, values: 0 },
};

if (report.db.before !== report.db.after) {
  console.error('FATAL: the two captures used different databases; the diff is meaningless');
  process.exit(2);
}

for (const context of beforeContexts) {
  if (!afterContexts.includes(context)) continue;
  report.compared.contexts += 1;

  const a = before.contexts[context];
  const b = after.contexts[context];
  const aPaths = Object.keys(a).sort();
  const bPaths = Object.keys(b).sort();

  for (const path of onlyIn(aPaths, bPaths)) {
    report.elementDrift.push({ context, path, side: 'only-in-before' });
  }
  for (const path of onlyIn(bPaths, aPaths)) {
    report.elementDrift.push({ context, path, side: 'only-in-after' });
  }

  for (const path of aPaths) {
    if (!(path in b)) continue;
    report.compared.elements += 1;
    for (const [property, value] of Object.entries(a[path])) {
      report.compared.values += 1;
      if (b[path][property] !== value) {
        report.valueDifferences.push({
          context,
          path,
          property,
          before: value,
          after: b[path][property],
        });
      }
    }
  }
}

const routeOf = (context) => context.split('|')[0];
const byRoute = {};
for (const difference of report.valueDifferences) {
  byRoute[routeOf(difference.context)] = (byRoute[routeOf(difference.context)] || 0) + 1;
}

console.log(`before css ${report.before.css}`);
console.log(`after  css ${report.after.css}`);
console.log(
  `compared ${report.compared.contexts} contexts, ` +
    `${report.compared.elements} elements, ${report.compared.values} computed values`
);
console.log(`context drift:  ${report.contextsOnlyInBefore.length + report.contextsOnlyInAfter.length}`);
console.log(`element drift:  ${report.elementDrift.length}`);
console.log(`value changes:  ${report.valueDifferences.length}`);
for (const [route, count] of Object.entries(byRoute)) console.log(`    ${route}: ${count}`);

for (const difference of report.valueDifferences.slice(0, 25)) {
  console.log(
    `  ${difference.context} ${difference.path} ${difference.property}: ` +
      `${JSON.stringify(difference.before)} -> ${JSON.stringify(difference.after)}`
  );
}
if (report.valueDifferences.length > 25) {
  console.log(`  ... ${report.valueDifferences.length - 25} more (see the JSON report)`);
}

if (outDir) {
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'diff.json'), JSON.stringify(report, null, 1));
}

const clean =
  !report.contextsOnlyInBefore.length &&
  !report.contextsOnlyInAfter.length &&
  !report.elementDrift.length &&
  !report.valueDifferences.length;

console.log(clean ? '\nPASS — zero computed-value and zero structural differences' : '\nFAIL — differences found');
process.exit(clean ? 0 : 1);
