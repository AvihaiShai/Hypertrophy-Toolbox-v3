/**
 * WP4.4-j — the known-live control's mutation.
 *
 * The packet's claim is that deleting 25 shadowed declarations moves zero
 * computed values across 66 contexts. A differential reporting zero is
 * indistinguishable from a broken differential until the same instrument is
 * shown to report non-zero when the cascade really moves. WP4.4-i learned this
 * the expensive way: its control existed only as an unrepeatable hand edit, and
 * two different mutations were quoted as one run.
 *
 * The mutation re-points `--bg-primary` in the dark token block to a colour no
 * other rule uses. That property is consumed by `var()` throughout the dark
 * bundle, so it must move many dark values — and, because the token lives under
 * `[data-theme="dark"]`, it must move **exactly zero light values**. The control
 * therefore proves two things at once: the instrument is live, and its
 * light/dark partition is real rather than a labelling accident.
 *
 * Destructive to a working tree on purpose: apply to a throwaway checkout,
 * measure, then `git checkout -- static/css/theme-dark.css`. It refuses to run
 * against anything but the expected input digest, so it cannot be layered onto
 * an already-mutated tree, and it pins its own output so a later edit to the
 * transformation cannot silently decouple the script from the recorded figure.
 *
 * usage:
 *   node scripts/css_audit/j_known_live_mutation.mjs --root <checkout> \
 *     [--expect-sha <sha256>] [--expect-output-sha <sha256>]
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { createHash } from 'node:crypto';

const argv = process.argv.slice(2);
const arg = (name, fallback = null) => {
  const i = argv.indexOf(name);
  return i < 0 ? fallback : argv[i + 1];
};

/** The post-removal `theme-dark.css` this control is defined against. */
const EXPECTED_INPUT = 'e54818bf790eb2c11474f68ecddc25d66304d9edf650cf698853276e419f2fca';
const TOKEN = '--bg-primary';
/** A colour that appears nowhere else in the bundle, so every hit is the token. */
const SENTINEL = '#ff00ff';

const root = resolve(arg('--root'));
const expectSha = arg('--expect-sha', EXPECTED_INPUT);
const expectOutputSha = arg('--expect-output-sha');
const cssPath = join(root, 'static/css/theme-dark.css');

const sha = (buf) => createHash('sha256').update(buf).digest('hex');

const original = readFileSync(cssPath);
const actual = sha(original);
if (actual !== expectSha) {
  throw new Error(
    `${cssPath} hashes to ${actual} but this control is defined against ${expectSha}. `
    + 'Point --root at the post-removal tree, or pass --expect-sha deliberately.'
  );
}

const text = original.toString('utf8');
const eol = text.includes('\r\n') ? '\r\n' : '\n';
const lines = text.split(eol);

const touched = [];
const mutated = lines.map((line, index) => {
  const match = new RegExp(`^(\\s*)${TOKEN}\\s*:\\s*([^;]+);(.*)$`).exec(line);
  if (!match) return line;
  touched.push({ line: index + 1, from: match[2].trim() });
  return `${match[1]}${TOKEN}: ${SENTINEL};${match[3]}`;
});

if (touched.length === 0) throw new Error(`no ${TOKEN} declaration found; the control would be a no-op`);

const output = Buffer.from(mutated.join(eol), 'utf8');
const outputSha = sha(output);
if (expectOutputSha && outputSha !== expectOutputSha) {
  throw new Error(`the mutation produced ${outputSha} but the recorded control CSS is ${expectOutputSha}`);
}
writeFileSync(cssPath, output);

console.log(`re-pointed ${TOKEN} to ${SENTINEL} on ${touched.length} line(s): ${touched.map((t) => `${t.line} (was ${t.from})`).join(', ')}`);
console.log(`before sha256: ${actual}`);
console.log(`after  sha256: ${outputSha}`);
console.log(`revert with: git -C ${root} checkout -- static/css/theme-dark.css`);
