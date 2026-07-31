/**
 * WP4.4-i — diff the G3 regions A/B/C before and after halves.
 *
 * G3 is a hard gate on this packet: *"Workout Log regions A, B and C remain
 * page-local and ID-free. Any packet that changes shared selector ownership MUST
 * re-measure A-C before and after."* The measurement is
 * `scripts/css_audit/n4_regions_abc.mjs`; this is the diff half.
 *
 * Inventory B states the pass condition precisely: *"any declaration whose `wins`
 * rises from 0 is a resurrection and must be accounted for explicitly."* So `wins`
 * and `loses` are compared per declaration, and a rising `wins` is reported
 * separately from any other drift because it is the specific failure G3 exists to
 * catch.
 *
 * A clean diff is only meaningful if the two inputs really are opposite halves of
 * the gate. This script used to compare `perDeclaration` and `totals` and nothing
 * else, so passing the same summary twice printed a full PASS — and because the
 * measurement recorded only `pages-workout-log.css`, which no admissible repair
 * touches, the two halves were indistinguishable by construction. Every check
 * below exists to close one of those paths:
 *
 *   - both summaries must declare opposite `--side` values;
 *   - they must come from different checkout roots;
 *   - their `components.css` digests must differ — that is the variable under test;
 *   - served digests must match their on-disk digests on both halves;
 *   - the frozen DB and `pages-workout-log.css` must be identical, or the two
 *     halves differ in more than the one thing the gate is measuring;
 *   - both halves' own fatal controls must have passed;
 *   - the comparison must be non-empty.
 *
 * The verdict is written to disk. A gate whose result exists only as console
 * output cannot be cited later.
 *
 * usage:
 *   node scripts/css_audit/i_diff_g3.mjs <before/summary.json> <after/summary.json> [--out <dir>]
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

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
const [beforePath, afterPath] = positional;
if (!beforePath || !afterPath) {
  throw new Error('usage: i_diff_g3.mjs <before/summary.json> <after/summary.json> [--out <dir>]');
}
const outDir = arg('--out') ? resolve(arg('--out')) : null;

const before = JSON.parse(readFileSync(beforePath, 'utf8'));
const after = JSON.parse(readFileSync(afterPath, 'utf8'));

// ---------------------------------------------------------------------------
// provenance — refuse to bless a comparison whose inputs are not what they claim
// ---------------------------------------------------------------------------
const provenance = [];
const idBefore = before.identity ?? {};
const idAfter = after.identity ?? {};

const must = (condition, message) => { if (!condition) provenance.push(message); };

must(idBefore.side === 'before', `before half declares side ${JSON.stringify(idBefore.side)}, expected "before"`);
must(idAfter.side === 'after', `after half declares side ${JSON.stringify(idAfter.side)}, expected "after"`);
must(
  Boolean(idBefore.root) && Boolean(idAfter.root) && idBefore.root !== idAfter.root,
  `both halves were measured from the same checkout root ${JSON.stringify(idBefore.root)}`,
);
must(
  Boolean(idBefore.componentsCssSha256) && Boolean(idAfter.componentsCssSha256)
    && idBefore.componentsCssSha256 !== idAfter.componentsCssSha256,
  `both halves served the same components.css ${idBefore.componentsCssSha256} — nothing under test changed`,
);
for (const [label, capture, id] of [['before', before, idBefore], ['after', after, idAfter]]) {
  must(
    id.servedComponentsCssSha256 === id.componentsCssSha256,
    `${label} half served components.css ${id.servedComponentsCssSha256} but its checkout has ${id.componentsCssSha256}`,
  );
  // Boolean() first: `undefined === undefined` would satisfy an equality-only
  // guard, so a summary missing both fields would pass the check that exists to
  // catch exactly that kind of missing provenance.
  must(
    Boolean(id.cssSha256) && Boolean(id.servedCssSha256) && id.servedCssSha256 === id.cssSha256,
    `${label} half served a different pages-workout-log.css than its checkout has, or recorded neither digest`,
  );
  must(capture.controls?.passed === true, `${label} half's own fatal controls did not pass`);
}
must(
  Boolean(idBefore.cssSha256) && idBefore.cssSha256 === idAfter.cssSha256,
  'the two halves used different pages-workout-log.css; the gate measures that file and it must be held constant',
);
must(
  idBefore.frozenDbSha256 === idAfter.frozenDbSha256,
  `frozen DB differs: ${idBefore.frozenDbSha256} vs ${idAfter.frozenDbSha256}`,
);
must(
  Object.keys(before.perDeclaration ?? {}).length > 0,
  'before half compared zero declarations; an empty set is not a pass',
);
must(Boolean(before.totals) && Boolean(after.totals), 'a half is missing its totals block');

// ---------------------------------------------------------------------------
const resurrections = [];
const drift = [];
const missing = [];
const identityDrift = [];

for (const [key, b] of Object.entries(before.perDeclaration)) {
  const a = after.perDeclaration[key];
  if (!a) { missing.push(key); continue; }
  // Keys are positional (`A1`, `A2`, ...). If a declaration were inserted or
  // removed inside a region, every later key would re-point at a different
  // declaration and a content-blind comparison would report clean while
  // comparing padding against color.
  if (b.region !== a.region || b.prop !== a.prop || b.line !== a.line) {
    identityDrift.push({ key, before: `${b.region} ${b.prop} :${b.line}`, after: `${a.region} ${a.prop} :${a.line}` });
    continue;
  }
  if (b.wins === 0 && a.wins > 0) {
    resurrections.push({ key, region: b.region, prop: b.prop, line: b.line, wins: `0 -> ${a.wins}` });
  } else if (b.wins !== a.wins || b.loses !== a.loses) {
    drift.push({
      key, region: b.region, prop: b.prop, line: b.line,
      wins: `${b.wins} -> ${a.wins}`, loses: `${b.loses} -> ${a.loses}`,
    });
  }
}
for (const key of Object.keys(after.perDeclaration)) {
  if (!(key in before.perDeclaration)) missing.push(`only-in-after: ${key}`);
}

const t = (capture) => capture.totals;
const totalsEqual = JSON.stringify(t(before)) === JSON.stringify(t(after));
const clean = !provenance.length && !resurrections.length && !drift.length
  && !missing.length && !identityDrift.length && totalsEqual;

console.log(`before: ${idBefore.root} @ ${idBefore.git?.head ?? '?'} components ${idBefore.componentsCssSha256}`);
console.log(`after:  ${idAfter.root} @ ${idAfter.git?.head ?? '?'} components ${idAfter.componentsCssSha256}`);
console.log(`before totals: ${JSON.stringify(t(before))}`);
console.log(`after  totals: ${JSON.stringify(t(after))}`);
console.log(`declarations compared: ${Object.keys(before.perDeclaration).length}`);
console.log(`provenance failures:        ${provenance.length}`);
for (const p of provenance) console.log(`  ${p}`);
console.log(`RESURRECTIONS (wins 0 -> n): ${resurrections.length}`);
for (const r of resurrections) console.log(`  ${r.region} ${r.prop} :${r.line} ${r.wins}`);
console.log(`other wins/loses drift:     ${drift.length}`);
for (const d of drift) console.log(`  ${d.region} ${d.prop} :${d.line} wins ${d.wins} loses ${d.loses}`);
console.log(`declaration-set drift:      ${missing.length}`);
for (const m of missing) console.log(`  ${m}`);
console.log(`declaration identity drift: ${identityDrift.length}`);
for (const d of identityDrift) console.log(`  ${d.key}: ${d.before} -> ${d.after}`);

if (outDir) {
  mkdirSync(outDir, { recursive: true });
  writeFileSync(
    resolve(outDir, 'diff.json'),
    `${JSON.stringify({
      before: { path: beforePath, identity: idBefore, totals: t(before) },
      after: { path: afterPath, identity: idAfter, totals: t(after) },
      declarationsCompared: Object.keys(before.perDeclaration).length,
      provenance, resurrections, drift, missing, identityDrift, totalsEqual, clean,
    }, null, 2)}\n`,
  );
}

console.log(clean ? '\nPASS — G3: no resurrection, no ownership drift in regions A/B/C' : '\nFAIL — G3 differences found');
process.exit(clean ? 0 : 1);
