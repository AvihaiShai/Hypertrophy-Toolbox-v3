/**
 * Stylelint, filtered to the seven WP4.4 shared surfaces.
 *
 * F20: `npm run lint:css` globs `scss/**\/*.scss` as well, so an unfiltered
 * delta moves with SCSS noise and confounds V3/V4. This runs the same config
 * over the seven surfaces only and emits per-file, per-rule counts.
 *
 * usage: node scripts/css_audit/stylelint_surfaces.mjs <out.json>
 */
import { writeFileSync } from 'node:fs';
import { relative } from 'node:path';
import stylelint from 'stylelint';

const SURFACES = [
  'motion.css',
  'base.css',
  'layout.css',
  'components.css',
  'navbar.css',
  'theme-dark.css',
  'a11y.css',
];

const outputPath = process.argv[2];
if (!outputPath) {
  console.error('usage: node scripts/css_audit/stylelint_surfaces.mjs <out.json>');
  process.exit(2);
}

const files = SURFACES.map((name) => `static/css/${name}`);
const { results } = await stylelint.lint({ files, formatter: 'json' });

const bySurface = {};
const byRule = {};
let total = 0;

for (const result of results) {
  const file = relative(process.cwd(), result.source).replaceAll('\\', '/');
  const warnings = result.warnings ?? [];
  const rules = {};
  for (const warning of warnings) {
    const rule = warning.rule ?? '<unknown>';
    rules[rule] = (rules[rule] ?? 0) + 1;
    byRule[rule] = (byRule[rule] ?? 0) + 1;
  }
  bySurface[file] = {
    warningCount: warnings.length,
    byRule: Object.fromEntries(
      Object.entries(rules).sort(([a], [b]) => a.localeCompare(b)),
    ),
    parseErrorCount: (result.parseErrors ?? []).length,
  };
  total += warnings.length;
}

writeFileSync(
  outputPath,
  `${JSON.stringify(
    {
      scope: 'seven WP4.4 shared surfaces only (F20 — excludes scss/** and page bundles)',
      surfaces: SURFACES,
      warningCount: total,
      byRule: Object.fromEntries(
        Object.entries(byRule).sort(([a], [b]) => a.localeCompare(b)),
      ),
      bySurface,
    },
    null,
    2,
  )}\n`,
  'utf8',
);

console.log(`seven-surface stylelint warnings: ${total}`);
