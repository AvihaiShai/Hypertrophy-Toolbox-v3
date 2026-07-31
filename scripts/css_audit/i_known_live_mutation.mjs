/**
 * WP4.4-i — the known-live control's mutation.
 *
 * A differential that reports zero is indistinguishable from a broken
 * differential until the same instrument is shown to report non-zero when the
 * cascade really moves. That is what this mutation is for: it de-weights a
 * branch the packet proved UNSAFE, so the five-route differential must light up.
 *
 * Until this script existed the mutation was a hand edit made in a scratch tree
 * and never committed. The number it produced (8,856) was real, but no committed
 * artifact could regenerate it, so the control could not be re-executed and the
 * evidence cited a run nobody could repeat. Worse, two different hand mutations
 * were made on different days and their results were quoted side by side as if
 * they were one run — 8,784 in the property/theme table and 8,856 in the summary.
 *
 * The transformation, applied to each rule of the shared `:is()` family:
 *
 *   :is(#workout[data-page="workout-plan"], .workout-log-page,
 *       .summary-frame.frame-calm-glass, .progression-plan-container) REST
 *
 * becomes two comma-separated arms on the same physical line, so pinned line
 * numbers stay valid:
 *
 *   :is(#workout[data-page="workout-plan"], .workout-log-page,
 *       .progression-plan-container) REST, .summary-frame.frame-calm-glass REST
 *
 * `:is()` takes the specificity of its most specific argument, so every arm of
 * the original list inherits a = 1 from the `#workout` ID donor. Splitting the
 * summary branch out drops it to a = 0, and the page-local `!important` rules in
 * `pages-session-summary.css` and `pages-weekly-summary.css` win instead —
 * resurrecting the unmigrated legacy palette on exactly the two summary routes.
 * That is the N3 disproof for this branch and the packet's known-live control.
 *
 * The mutation is destructive to a working tree on purpose: it is meant to be
 * applied to a throwaway checkout, measured, and reverted with
 * `git checkout -- static/css/components.css`. It refuses to run unless the file
 * it is about to overwrite hashes to the expected pristine input, so it can never
 * be layered onto an already-mutated or unrelated tree.
 *
 * usage:
 *   node scripts/css_audit/i_known_live_mutation.mjs --root <checkout> \
 *     [--expect-sha <sha256 of the pristine input>]
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { createHash } from 'node:crypto';

const argv = process.argv.slice(2);
const arg = (name, fallback = null) => {
  const i = argv.indexOf(name);
  return i < 0 ? fallback : argv[i + 1];
};

/** The post-h, pre-i `components.css` this mutation is defined against. */
const PRISTINE_SHA = '883e6aa85564c42b36ca801529081b279f119e5c99a539dc235bc84d72107964';

const root = resolve(arg('--root'));
const expectSha = arg('--expect-sha', PRISTINE_SHA);
const cssPath = join(root, 'static/css/components.css');

const IS_LIST = '#workout[data-page="workout-plan"], .workout-log-page, .summary-frame.frame-calm-glass, .progression-plan-container';
const IS_TOKEN = `:is(${IS_LIST})`;
const IS_WITHOUT_SUMMARY = ':is(#workout[data-page="workout-plan"], .workout-log-page, .progression-plan-container)';
const SUMMARY_ARM = '.summary-frame.frame-calm-glass';

const sha = (buffer) => createHash('sha256').update(buffer).digest('hex');

const original = readFileSync(cssPath);
const actualSha = sha(original);
if (actualSha !== expectSha) {
  throw new Error(
    `${cssPath} hashes to ${actualSha} but this mutation is defined against ${expectSha}. ` +
    'Point --root at a pristine checkout of the pre-repair commit, or pass --expect-sha deliberately.'
  );
}

const text = original.toString('utf8');
// Byte fidelity matters: this repository checks `components.css` out with CRLF,
// and a run that silently rewrote the file with LF would change the digest for a
// reason that has nothing to do with the cascade.
const eol = text.includes('\r\n') ? '\r\n' : '\n';
const lines = text.split(eol);

const touched = [];
const mutated = lines.map((line, index) => {
  if (!line.includes(IS_TOKEN)) return line;

  // Each family selector occupies one physical line and ends either in `,`
  // (another selector follows) or in ` {` (the block opens).
  const match = /^(.*?)(,|\s*\{)$/.exec(line);
  if (!match) throw new Error(`line ${index + 1} contains the family token but does not end in "," or "{": ${line}`);
  const [, selector, terminator] = match;

  const keptArms = selector.replace(IS_TOKEN, IS_WITHOUT_SUMMARY);
  const summaryArm = selector.replace(IS_TOKEN, SUMMARY_ARM);
  touched.push({ line: index + 1, selector });
  return `${keptArms}, ${summaryArm}${terminator}`;
});

if (touched.length === 0) throw new Error('no family selectors matched; the mutation would be a no-op');

const output = Buffer.from(mutated.join(eol), 'utf8');
writeFileSync(cssPath, output);

console.log(`mutated ${touched.length} family selector lines in ${cssPath}`);
console.log(`lines: ${touched.map((entry) => entry.line).join(', ')}`);
console.log(`before sha256: ${actualSha}`);
console.log(`after  sha256: ${sha(output)}`);
console.log(`revert with: git -C ${root} checkout -- static/css/components.css`);
