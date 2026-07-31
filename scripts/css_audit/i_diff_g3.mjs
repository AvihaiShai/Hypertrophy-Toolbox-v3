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
 * usage:
 *   node scripts/css_audit/i_diff_g3.mjs <before/summary.json> <after/summary.json>
 */
import { readFileSync } from 'node:fs';

const [beforePath, afterPath] = process.argv.slice(2);
const before = JSON.parse(readFileSync(beforePath, 'utf8'));
const after = JSON.parse(readFileSync(afterPath, 'utf8'));

const resurrections = [];
const drift = [];
const missing = [];

for (const [key, b] of Object.entries(before.perDeclaration)) {
  const a = after.perDeclaration[key];
  if (!a) { missing.push(key); continue; }
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
console.log(`before totals: ${JSON.stringify(t(before))}`);
console.log(`after  totals: ${JSON.stringify(t(after))}`);
console.log(`declarations compared: ${Object.keys(before.perDeclaration).length}`);
console.log(`RESURRECTIONS (wins 0 -> n): ${resurrections.length}`);
for (const r of resurrections) console.log(`  ${r.region} ${r.prop} :${r.line} ${r.wins}`);
console.log(`other wins/loses drift:     ${drift.length}`);
for (const d of drift) console.log(`  ${d.region} ${d.prop} :${d.line} wins ${d.wins} loses ${d.loses}`);
console.log(`declaration-set drift:      ${missing.length}`);
for (const m of missing) console.log(`  ${m}`);

const totalsEqual = JSON.stringify(t(before)) === JSON.stringify(t(after));
const clean = !resurrections.length && !drift.length && !missing.length && totalsEqual;
console.log(clean ? '\nPASS — G3: no resurrection, no ownership drift in regions A/B/C' : '\nFAIL — G3 differences found');
process.exit(clean ? 0 : 1);
