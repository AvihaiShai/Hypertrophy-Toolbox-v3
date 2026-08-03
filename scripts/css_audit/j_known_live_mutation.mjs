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
 * ## What the digests are digests *of*
 *
 * `EXPECTED_INPUT`, `--expect-sha` and `--expect-output-sha` are all sha256 over
 * the **canonical representation**: the file decoded as UTF-8 with every `CRLF`
 * rewritten to a single `LF`. They are deliberately **not** digests of the bytes
 * on disk, and `sha256sum static/css/theme-dark.css` on a Windows checkout will
 * not print them. What does print `EXPECTED_INPUT`, on either platform, is the
 * committed blob — `git show HEAD:static/css/theme-dark.css | sha256sum` — for
 * the reason below.
 *
 * The repository is `core.autocrlf=true` with no `.gitattributes`, so a single
 * commit of `theme-dark.css` materializes as LF on Linux and CRLF on Windows —
 * 22,018 bytes against 22,592, one `CR` per each of its 574 lines. Hashing the
 * raw buffer therefore pinned the *Windows* form: the control ran here and
 * refused to run in CI, where the only way past it was the `--expect-sha`
 * override this docstring forbids using to silence it. Canonicalizing first
 * makes both checkouts agree on `3ab06083…`, which is also the digest of the
 * committed blob.
 *
 * Only content is pinned; line endings are not. The mutated file is written back
 * with whatever ending it arrived with, so the bytes this produces in a Windows
 * worktree are unchanged from before the normalization.
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

/**
 * The post-removal `theme-dark.css` this control is defined against, as the
 * sha256 of its **LF-normalized** text — see "What the digests are digests of".
 * Re-pinned from the CRLF digest `e54818bf…` (LEFTOVERS P2.6); the file itself
 * is untouched.
 */
const EXPECTED_INPUT = '3ab06083c89eae0b5dd46d820dde4d2da1d59de1ffa6d825585aaca0ad17e14a';
const TOKEN = '--bg-primary';
/**
 * `--bg-primary` proves the instrument is live, but it only surfaces where no
 * later rule overrides it — in practice the volume-splitter tables. The
 * declarations this packet deleted live in the results-section /
 * table-responsive cluster, which `background: none !important` dominates, and a
 * control that never lights up that cluster cannot show the instrument would
 * have seen a regression there. The `shadow-winner` mode re-points that very
 * declaration — the one whose presence made the deleted declarations dead — so
 * the control fires in exactly the region the packet touched.
 */
const MODE = arg('--mode', 'token');
/** A colour that appears nowhere else in the bundle, so every hit is the token. */
const SENTINEL = '#ff00ff';

const root = resolve(arg('--root'));
const expectSha = arg('--expect-sha', EXPECTED_INPUT);
const expectOutputSha = arg('--expect-output-sha');
const cssPath = join(root, 'static/css/theme-dark.css');

/** UTF-8 text with every CRLF collapsed to LF: the form every digest is taken over. */
const canonical = (text) => text.replace(/\r\n/g, '\n');
const sha = (text) => createHash('sha256').update(text, 'utf8').digest('hex');

const original = readFileSync(cssPath, 'utf8');
const source = canonical(original);
const actual = sha(source);
if (actual !== expectSha) {
  throw new Error(
    `${cssPath} normalizes to ${actual} but this control is defined against ${expectSha} `
    + '(sha256 of the LF-normalized text, not of the bytes on disk — line endings cannot '
    + 'be the cause). Point --root at the post-removal tree, or pass --expect-sha deliberately.'
  );
}

/** Preserved for the write-back only; the line-offset math runs on the canonical form. */
const eol = original.includes('\r\n') ? '\r\n' : '\n';
const lines = source.split('\n');

const touched = [];
const mutated = lines.map((line, index) => {
  if (MODE === 'shadow-winner') {
    const m = /^(\s*)background\s*:\s*none\s*!important;(.*)$/.exec(line);
    if (!m) return line;
    touched.push({ line: index + 1, from: 'background: none !important' });
    return `${m[1]}background: ${SENTINEL} !important;${m[2]}`;
  }
  const match = new RegExp(`^(\\s*)${TOKEN}\\s*:\\s*([^;]+);(.*)$`).exec(line);
  if (!match) return line;
  touched.push({ line: index + 1, from: match[2].trim() });
  return `${match[1]}${TOKEN}: ${SENTINEL};${match[3]}`;
});

if (touched.length === 0) throw new Error(`mode ${MODE} matched nothing; the control would be a no-op`);

const outputSha = sha(mutated.join('\n'));
if (expectOutputSha && outputSha !== expectOutputSha) {
  throw new Error(`the mutation produced ${outputSha} but the recorded control CSS is ${expectOutputSha}`);
}
writeFileSync(cssPath, mutated.join(eol), 'utf8');

console.log(`re-pointed ${TOKEN} to ${SENTINEL} on ${touched.length} line(s): ${touched.map((t) => `${t.line} (was ${t.from})`).join(', ')}`);
console.log(`before sha256 (LF-normalized): ${actual}`);
console.log(`after  sha256 (LF-normalized): ${outputSha}`);
console.log(`revert with: git -C ${root} checkout -- static/css/theme-dark.css`);
