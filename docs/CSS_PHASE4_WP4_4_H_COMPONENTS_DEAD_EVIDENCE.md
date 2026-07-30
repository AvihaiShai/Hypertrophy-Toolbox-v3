# WP4.4-h — `components.css` dead-declaration deletion evidence

**Status:** complete, stopped at the N4 checkpoint. WP4.4-i is **not** started.
**Branch:** `wt/wp4-4-h-components-dead`, cut from merged `main` at
`4b7ca585cf03cc5f2de4fd88c257f29460173640`.

WP4.4-h deletes declarations that own nothing. It is a pure deletion: `git diff` on
`static/css/components.css` shows removals only — no insertion, no re-weighting, no new
`!important`.

> **Every original shipment measurement in this document comes from the `h4` cycle.** The
> post-review classification and single-process aggregate reruns are identified explicitly as
> `h5`. All earlier `h`, `h2` and `h3` artifacts are inadmissible and are retained under
> `artifacts/wp4_4/` with `CONTAMINATED-`, `SUPERSEDED-`, `INADMISSIBLE-` or `QUARANTINED-`
> prefixes, never cited as proof. §5 records why.

Three files changed: `static/css/components.css`,
`tests/test_css_wp4_4_components_contracts.py`, and this document. No shared contract, baseline
JSON, snapshot, template, JavaScript, Python or database file was touched.

| Identity | Value |
|---|---|
| Branch base | `4b7ca585cf03cc5f2de4fd88c257f29460173640` (PR #207, WP4.4-g evidence) |
| Predecessors merged | a, c, b, e, d1, d2, f1, f2, g — the full `b…f → h` and `g → h` prerequisite set |
| `components.css` SHA-256 **before** | `53799e819816b15a46a6e30ba7751c3e46781cb193095398947d139bdf171099` |
| `components.css` SHA-256 **after** | `883e6aa85564c42b36ca801529081b279f119e5c99a539dc235bc84d72107964` |
| Lines before / after | 5,345 / 5,207 (**−138**) |
| `!important` before / after | 939 / 919 (**−20**) |
| Declarations deleted | **101** across 30 rules (11 removed whole, 19 trimmed) |
| Frozen probe DB | `7cef8e0acb9106534ba9ff8a935d825d94f913211191f43e46dba830b4da1d47` |

---

## 1. The headline result

**101 of a possible 121 declarations were deleted.** The gap is the whole point of this packet, so
it is stated before anything else:

| Stage | Declarations | Why the rest fell out |
|---|---:|---|
| Zero-winner in the seeded 446-context census, above line 4104 | **121** | — |
| …with differential blast coverage | 103 | 18 `.btn.btn-video` declarations have no ownership records in any differential run (§7.1) |
| …surviving the removal oracle | **101** | 1 proved **live** on removal, 1 was **never probed** (§7.3) |

The two withdrawals matter more than their count. `.collapse-toggle { color: #6c757d }` was
classified dead by a 446-context cascade model — matched 178 longhand instances across 86 contexts
and won **zero** — and is nevertheless live: removing it from the live CSSOM moves the computed
colour of every `.collapse-toggle` and its `.toggle-icon` child from `rgb(0, 131, 143)` to
`rgb(102, 102, 102)`, in 42 element-property pairs. A cascade model that disagrees with the rendered
result is not evidence. That is why nothing here is deleted on the strength of the census alone.

---

## 2. Why this packet is much smaller than its plan row projected

The dry run proposed **554 lines**; **138** were deleted.

`tests/test_css_wp4_4_a_baseline_contracts.py::test_layer_membership_is_recorded_exactly_and_frozen`
re-derives `measure.layer_spans("components.css")` **from the working tree** and asserts:

```python
assert layers["spans"]["components.css"] == [
    {"layer": "workout", "openLine": 3539, "closeLine": 4104}
]
```

Those are absolute line numbers. Deleting any line at or before 4104 shifts `openLine` or
`closeLine` and reds that assertion — and that file is outside this packet's authorized write set,
so the red could not be repaired in scope. Re-pinning it would also defeat its purpose: N2 freezes
layer membership arc-wide and this pin is the mechanism.

The only legal deletion window is therefore **`components.css` lines 4105–5345**.

| | Dry-run projection | Shipped | Withheld |
|---|---:|---:|---:|
| Cuts | 247 | **87** | 160 |
| Declarations | 336 | **101** | 235 |
| Lines | 554 | **138** | 416 |
| `!important` removed | 105 | **20** | 85 |
| Rules deleted whole | 62 | **11** | 51 |

The withheld declarations remain dead by measurement and remain deletable in principle. Recovering
them requires an owner decision to re-pin the Packet-a layer span. That is a separate authorization
and is **not** requested here.

Because the whole legal window sits *after* the layer close line, this packet deletes **nothing from
inside `@layer workout`**. Layer membership is untouched in the strongest possible sense, and
`test_the_packet_stayed_above_the_frozen_layer_span` re-asserts `openLine 3539 / closeLine 4104`
locally so a later widening reds in this packet's own file.

---

## 3. Scope, and what was withheld

**Interaction states are out of scope, stated up front as PR#10 / M12 requires:** hover, focus,
focus-visible, focus-within and active. Nothing here depends on an interaction state. WP4.3i-dead's
same-CSS control on exactly this class produced 52 differing records and shrank that packet from 24
declarations to 14; this packet does not re-open that ground.

**Region H** is locked byte-for-byte by `REGION_H_SHA256`
(`tests/test_css_cascade_contracts.py:43`) and lives in `pages-workout-log.css`. This packet writes
one production file, `components.css`, so Region H is untouchable by construction as well as by
rule.

| Bucket | Declarations | Disposition |
|---|---:|---|
| Deleted | **101** | agreed dead by all three oracles (§7) |
| `.btn.btn-video` family | 18 | **withheld** — no differential blast coverage (§7.1) |
| Withdrawn by the removal oracle | 2 | **withheld** — 1 live, 1 never probed (§7.3) |
| Withheld by the Packet-a layer pin | 235 | dead, but not legally reachable (§2) |
| `.value-changed` | 6 | **withheld** — reachable only through a JS-applied class (M10 / PR#3) |
| `:is()` family | 0 | none eligible; the whole family belongs to WP4.4-i, owner-gated (N4) |
| Custom properties | 0 | never eligible under the non-winner rule (M9) |
| Pseudo-state | 0 | out of scope, declared up front (M12) |
| Pseudo-element | 0 | an inline sentinel cannot address one |
| Keyframe steps | 0 | not eligible |

Each exclusion is pinned as a **count** in `tests/test_css_wp4_4_components_contracts.py`, identical
before and after the deletion, because a prose exclusion is unenforceable. Measured on the pristine
and the shipped file:

| Family | Before | After |
|---|---:|---:|
| `:is(` tokens | 19 | 19 |
| `:where(` tokens | 58 | 58 |
| `.value-changed` | 20 | 20 |
| `:hover` | 115 | 115 |
| `:focus` | 174 | 174 |
| `:active` | 16 | 16 |
| `::` pseudo-elements | 51 | 51 |
| `@keyframes` | 9 | 9 |
| custom properties | 3 | 3 |
| `@media` | 33 | 33 |
| `prefers-reduced-motion` | 3 | 3 |
| `@layer` | 1 | 1 |
| **`!important`** | **939** | **919** |

`!important` is the only count that moves, by exactly the 20 important declarations deleted. The
twelve four-branch `:is()` rules and the three-branch reduced-motion rule at `:4433` are untouched,
as is the entire `@media (prefers-reduced-motion: reduce)` family.

---

## 4. Method

Classification and the deletion proof are different measurements, and M1 requires both. This packet
runs **three independent oracles** and deletes only their intersection.

1. **Cascade census (does it ever win?)** — `h_census.mjs`, 446 contexts, resolving ownership from
   CDP cascade data with the WP4.4-a/g model: browser specificity from matching-selector indices,
   `@layer` ordering, and the `!important` inversion (M4). A declaration is *dead* only if it
   matched at least one real rendered element, won zero longhands in every context, and its
   inline-important sentinel both changed and restored the computed value (M6/M6a).
2. **Zero-winner recount (does it own anything in the differential?)** — `h_zero_winner_check.mjs`,
   an independent recount over the *differential's* 11,295 ownership records rather than the
   census's own bookkeeping.
3. **Removal certification (does removing it change the page?)** — `h_certify.mjs` removes each
   declaration from the live CSSOM with `style.removeProperty`, re-reads every computed value on the
   page, then restores and verifies the restoration. This is the only oracle that cannot be argued
   with, and it is the one that withdrew two candidates.

The deletion itself is then proved by a **before/after differential** (`h_differential.mjs`), run
first twice on identical CSS as its own same-CSS control. Per context it records the computed value
of every element over a 113-longhand property universe, the *structural* winning-owner identity for
every element a deleted selector matched, the `components.css` candidate set behind each of those
longhands, and an M3-scoped element raster.

Owner identities are line-free by construction —
`sheet | selector | property | value | important | specificity | layers` — because the edit being
measured renumbers every line. A line-keyed identity would report the entire file as changed.

`@media` declarations were classified only under captures taken with their own condition (M11): all
seven `screen and (min/max-width …)` intervals plus `(max-width: 768px)`, and separately
reduced-motion, print and forced-contrast.

### Determinism controls shared by every browser oracle

All three browser oracles use the **same** frozen seeded database, `DB_FILE`, sidecar handling,
selector normalization, property universe, animation handling and cached-network pin:

| Control | Mechanism |
|---|---|
| Database | one frozen copy, `7cef8e0a…`, restored before every run; WAL/SHM sidecars deleted first, because a leftover sidecar can replay a *later* transaction over a restored main file and hashing the main file cannot see it |
| `TESTING` | deliberately **unset** — `utils/db_initializer.py:160,231` drop `user_selection` and `workout_log` outright when `TESTING=1` (§5) |
| Exclusivity | a PID lock (`artifacts/wp4_4/.h-probe.lock`) plus a `netstat` listener check recorded at 24 checkpoints per run; every run recorded exactly one listener PID |
| Identity | `--expect-css-sha` and `--expect-db-sha` asserted before the server starts, and the CSS/DB hashes re-checked every 15 contexts |
| Network | every non-`127.0.0.1` request served from `artifacts/wp4_4/net-cache` (11 assets: Inter + FontAwesome), identical cache key across all three oracles; an unavailable asset is recorded, never silently skipped. All runs: 11 cached, **0 unavailable** |
| Animations | paused, then seeked to the canonical instant, then verified to be *at* that instant (§5) |

### Harness inventory

| Tool | Provenance |
|---|---|
| `scripts/css_audit/measure.py`, `specificity.py` | committed WP4.4-a harness, used unmodified |
| `scripts/css_audit/stylelint_surfaces.mjs` | committed WP4.4-a seven-surface lint measurement (F20) |
| `artifacts/wp4_4/h_census.mjs` | 446-context cascade census |
| `artifacts/wp4_4/h_ranges.mjs` | postcss source-range emitter |
| `artifacts/wp4_4/h_zero_winner_check.mjs` | independent zero-winner recount (no browser) |
| `artifacts/wp4_4/h_certify.mjs` | live-CSSOM removal oracle |
| `artifacts/wp4_4/h_differential.mjs` | before/after owner + computed-value + candidate + raster oracle |
| `artifacts/wp4_4/h_compare_strict.mjs` | comparator, **no suppression list** |
| `artifacts/wp4_4/h_build_manifest.mjs` | deletion-manifest builder, self-validated (§7.4) |
| `artifacts/wp4_4/h_apply.mjs` | byte-range applier / restorer |

Generated output stays under gitignored `artifacts/wp4_4/` (A11).

**Two offset hazards, both hit and both corrected.**

1. **CRLF.** `h_ranges.mjs` reads the file with `readFileSync(path, 'utf8')` and does not normalize
   line endings, so every offset in the deletion manifest indexes the **CRLF** text. An applier that
   works on LF-normalized text lands every cut in the wrong place while still producing a
   plausible-looking diff.
2. **Characters, not bytes.** An earlier draft of this document asserted the cuts are raw *byte*
   offsets. They are not — postcss reports **character** offsets, and `components.css` holds
   **177,136 bytes against 177,119 characters**: ten non-ASCII characters, seven of them before the
   first cut, for thirteen bytes of drift. Splicing on byte offsets lands the first cut
   mid-declaration and, again, still produces a plausible diff.

`h_apply.mjs` therefore splices the utf-8 **string**, and proves its own model before it cuts:
re-encoding the untouched string must reproduce the pristine hash exactly, and the file's current
SHA-256 must equal the manifest's `beforeSha256`, or no edit is attempted.

---

## 5. Controls, and every cycle that was thrown away

Four measurement cycles were run. **Only `h4` is used.**

**`h` / `h2` — inadmissible: `TESTING=1`.** Every census before `h4` ran with `TESTING=1`.
`utils/db_initializer.py:160` and `:231` **drop `user_selection` and `workout_log` outright** under
that flag, so the seeded session was destroyed on every server start: Workout Log rendered an empty
table and the summary routes rendered no rows. Declarations were being classified against a DOM that
does not exist in use. These runs are retained as
`INADMISSIBLE-h-census-TESTING1-unseeded/` and are cited for nothing.

The replacement is a frozen seeded database (`h_seed_probe_db.py`) carrying a real logged session —
6 `user_selection` rows and 6 `workout_log` rows for `GYM - Full Body - Workout A` — with `TESTING`
unset. The difference is not cosmetic:

| | unseeded (`TESTING=1`) | seeded (`h4`) |
|---|---:|---:|
| Candidate DOM nodes inspected | 21,693 | **37,915** |
| Matched CDP rule entries | 295,798 | **717,386** |
| dead / live / mixed / unverified | 342 / 289 / 345 / 1,172 | **388 / 287 / 362 / 1,111** |

**`h3` — the same-CSS control failed, and the failure was real.** Two runs of *identical* CSS were
compared with no suppression list. Ownership, raster, membership and structure were all exactly
zero, but **6 computed values differed**, all on the `welcome` route's three animated decorative
nodes:

```
welcome--dark--1200--media-rest  transform   matrix(1, 8.47237e-12, -8.47237e-12, 1, 0, -3.64073e-09)  vs  matrix(1, 0, 0, 1, 0, 0)
welcome--light--1560--media-rest transform   matrix(1.00019, 0, 0, 1.00019, 0, 0)                      vs  matrix(1, 0, 0, 1, 0, 0)
welcome--light--1560--media-rest box-shadow  … 0px 0px 40.0047px 0px …                                 vs  … 0px 0px 40px 0px …
welcome--light--1560--media-rest transform   matrix(1.00002, 0, 0, 1.00002, -40, -40)                  vs  matrix(1, 0, 0, 1, -40, -40)
welcome--light--1560--media-rest transform   matrix(1, 2.02461e-06, -2.02461e-06, 1, 0, -0.00087001)   vs  matrix(1, 0, 0, 1, 0, 0)
welcome--light--768--rest        transform   matrix(1.00019, 0, 0, 1.00019, 0, 0)                      vs  matrix(1, 0, 0, 1, 0, 0)
```

This was **not** absorbed as noise and **not** waived. It was diagnosed to a defect in the harness's
own animation quiescer, which did:

```js
animation.currentTime = 0;   // seek…
animation.pause();           // …then pause
```

Setting `currentTime` on a **running** animation re-anchors its start time to *now*, so the
animation immediately resumes advancing from 0 and `pause()` pins it a few microseconds later. The
residues are exactly that: picoseconds of rotation (`8.47e-12`), microseconds (`2.02e-06`), and a
partially-advanced pulse (`1.00019`). Two prior attempts to fix the same symptom had treated it as a
registration-timing problem and added polling loops, which is why the direction of the disagreement
kept flipping between runs.

The repair is the ordering, applied identically in all three browser oracles:

```js
animation.pause();           // pause FIRST — now it cannot advance…
animation.currentTime = 0;   // …so the seek is exact
```

plus a verifier that treats "paused" as insufficient and requires each animation to sit *at* its
canonical instant (0 for infinite, `endTime` for finite), forcing another pinning pass otherwise —
because an animation that registers mid-pass can be paused at an arbitrary phase, which reads
*stably within a run* and differently between runs.

Three independent measurements confirm the repair rather than merely asserting it:

| Signal | before repair (`h3`) | after repair (`h4`) |
|---|---:|---:|
| Same-CSS control computed differences | 6 | **0** |
| Contexts needing a second computed pass | 20 | **0** |
| Census contexts recorded raster-uncertifiable | 2 | **0** |

The `h3` artifacts are retained as `QUARANTINED-h3-*-animation-seek-race`.

### The `h4` same-CSS control — the admissible one

`h4-before` and `h4-control` are two runs of the pristine file, compared by `h_compare_strict.mjs`
in `--mode control`, where **no term is allowed to be non-zero** and there is no suppression list:

```
run                 : h4 same-CSS control (pristine vs pristine)
mode                : control (allowed non-zero: none)
identical CSS       : true
contexts compared   : 330
  computedDifferences      0
  ownerDifferences         0
  candidatesLost           0
  candidatesGained         0
  pagePromotions           0
  pixelDifferingContexts   0
  elementsOnlyBefore       0
  elementsOnlyAfter        0
  blastNodesOnlyBefore     0
  blastNodesOnlyAfter      0
  stackDifferences         0
verdict             : PASS
```

Both runs recorded identical `cssSha256`, `frozenDbSha256`, `manifestSha256`, property universe
(113), blast selectors (43), blast cap (0 = uncapped), 11 cached network assets with 0 unavailable,
**0 retries**, and a single listener PID across all 24 guard checkpoints.

---

## 6. The census result

| Census identity | Value |
|---|---|
| Source SHA-256 | `53799e8…` (pristine) |
| Contexts | **446/446** |
| Same-CSS control | **446 passed / 0 failed** |
| Owner control | **446 passed / 0 failed** |
| Raster uncertifiable | **0** |
| Candidate DOM nodes inspected | 37,915 |
| Matched CDP rule entries | 717,386 |
| Exact CDP source-range mapping failures | **0** |
| Sentinel attempted / took effect / restored | 1,286 / 1,252 / 1,286 |
| Restoration failures | **0** |
| Classification control failures | **0** |
| Sentinel no-effect quarantined to *unverified* | 34 — never classified dead |

Classification totals: **live 287 · dead 388 · mixed 362 · unverified 1,111.**

Matrix: all 11 rendered routes × both themes × the 375/768/1440 core widths, reduced-motion and
forced-pseudo at each core width, every distinct `components.css` breakpoint representative (576,
992, 1200, 1280, 1300, 1440, 1560, 1700, 2200, 2600 px), high-contrast and print emulation, and the
real `.value-changed` class driven on Workout Plan at both themes and all core widths — 446
contexts. Twelve animation families were observed: `enablePulse`, `fadeIn`, `float`, `heartbeat`,
`inputFocus`, `inputValuePulse`, `nav-fa-icon-pop`, `page-enter`, `pulse-glow`, `shimmer`,
`slideIn`, `slideInRight`.

---

## 7. Candidate lineage — from 388 dead to 101 deleted

### 7.1 Source window and coverage

Of the 388 dead declarations, **121** lie above the frozen layer close line (pristine line > 4104).
Nested declarations under the `:where()` wrapper at line 4515 are eligible; the wrapper itself is
frozen and untouched.

Of those 121, **18 are excluded for missing DOM coverage**: the `.btn.btn-video` family appears only
in the *seeded* DOM (the exercise-media buttons the seeded workout rows render), and no differential
run carries ownership records for it, so its removal cannot be structurally certified.

| Excluded selector | Declarations |
|---|---:|
| `.btn.btn-video` | 13 |
| `.btn.btn-video > i` | 2 |
| `[data-theme='dark'] .btn.btn-video` | 3 |

These 18 remain dead by measurement and are a legitimate future candidate set once a differential
covers them. They are **not** deleted here.

### 7.2 Zero-winner recount — 103/103

Run against the `h4-before` differential, independently of the census's own bookkeeping:

```
contexts scanned          : 330
ownership records          : 11295
nominated declarations     : 103
distinct selector+property : 103
proven zero-winner         : 103
WINNERS (must be 0)        : 0
unreached by this oracle   : 0
verdict                    : PASS
```

### 7.3 Removal certification — the two withdrawals

66 contexts (11 routes × 2 themes × 375/768/1440), every candidate removed from the live CSSOM and
restored:

```
candidates            : 103
LIVE (must not delete): 1
dead, certified       : 101
never probed (harness): 1
probed, reached nothing: 0
unresolved cand. rules : 0
controls              : idempotence=0 restore=0 alignment=0 knownLive=true
```

| Withdrawn | Census verdict | Removal verdict | Rule applied |
|---|---|---|---|
| `.collapse-toggle { color: #6c757d }` (line 4843) | dead — matched 178 longhands over 86 contexts, won 0 | **LIVE** — 42 element-property pairs move, `rgb(0,131,143)` → `rgb(102,102,102)` on the button and its `.toggle-icon` child, including `outline-color` and `border-top-color` tracking `currentColor` | oracle disagreement |
| `.collapse-toggle { background: none }` (line 4836) | dead — matched 1,602 longhands over 86 contexts, won 0 | **never probed** — every context reported `probed=102` of 103 | neverProbed |

Both are asserted *positively* by
`test_the_two_withdrawn_declarations_are_still_present`, because their absence from the deletion
list is only the absence of a claim and would not notice a later packet deleting them.

#### Post-review clean-SHA certification with fatal independent controls

Review of the first certification exposed a genuine oracle-design gap: a run containing only
deletion candidates can return zero differences both when every candidate is dead and when the
oracle is blind. The certification was therefore re-run from the exact pristine stylesheet SHA
`53799e819816b15a46a6e30ba7751c3e46781cb193095398947d139bdf171099` with the 101 candidates and
five independently proven live declarations kept in separate result sets.

The live spikes are not annotations. Missing any one is a fatal run failure, as are any
idempotence, restoration or CSSOM/source-alignment failure; a candidate classified live,
`neverProbed`, `reachedNothing` or unresolved also fails the run.

| Result | Value |
|---|---:|
| Candidate declarations | **101** |
| Candidate `deadCertified` | **101** |
| Candidate live / `neverProbed` / `reachedNothing` / unresolved | **0 / 0 / 0 / 0** |
| Idempotence / restoration / CSSOM-source alignment failures | **0 / 0 / 0** |
| External assets unavailable | **0** |
| Fatal failures | **0** |
| Verdict | **PASS** |

| Independent live spike | Family | Computed differences | Probed / matched contexts | Result |
|---|---|---:|---:|---|
| D196 | `.form-label { color }` | 972 | 66 / 48 | **LIVE** |
| D477 | `.table th { border-bottom }` | 242 | 66 / 48 | **LIVE** |
| D1094 | `.alert { border-radius }` | 432 | 66 / 66 | **LIVE** |
| D1178 | `.btn-calm-primary { color }` | 1,404 | 66 / 66 | **LIVE** |
| D1187 | `.btn-calm-ghost { border }` | 2,250 | 66 / 66 | **LIVE** |

All declaration IDs above are the 1-based postcss `walkDecls` ordinal over that single pristine
SHA. This identity discipline also makes the independent-review intersection valid: of the 101 PR
candidates, 7 had been independently classified dead and 94 had been reported as “no demonstrated
match.” The corrected clean-SHA run resolved **all 94** rather than treating that bucket as a
deletion warrant. None remained unproven.

The binding disposition is now explicit:

- `deadCertified` → eligible for deletion;
- `live` → retain;
- `neverProbed`, unresolved, or no demonstrated match → retain unless separately certified.

The result is `artifacts/wp4_4/h5-certify-live-spikes.json`, SHA-256
`b3982329832fb87decc4b015ff162b34a378f4f12fa6bf175be478e80c6c3714`. Generated evidence remains
gitignored under A11; the command and identities needed to reproduce it are recorded in §11.

### 7.4 The intersection, and the manifest that encodes it

The deletion set is the intersection: **101 declarations**, each of which
(a) matched a real rendered element, (b) won zero longhands in all 446 census contexts, (c) was
independently recounted as a zero-winner over the differential's ownership records, (d) was
certified dead by live-CSSOM removal, (e) has a sentinel that both took effect and restored, and
(f) belongs to no excluded family.

| Evidence for the 101 specifically | Value |
|---|---:|
| Longhand instances matched | **73,590** |
| Longhand instances **won** | **0** |
| Distinct contexts in which a candidate matched | 166 |
| Sentinel took effect | **101 / 101** |
| Sentinel restored | **101 / 101** |
| Certified dead by removal | **101 / 101** |

`h_build_manifest.mjs` turns declaration ids into cuts. It was trusted only after reproducing the
previously-shipped 103-declaration manifest **exactly** — 89 cuts, identical offsets, identical
`afterSha256` — from the 103 ids alone (`--verify-against`). It was then re-run on the 101 ids.

Two cut-geometry rules were derived from that self-check and matter for correctness: a rule deleted
whole absorbs the contiguous comment block directly above it, and a declaration absorbs a trailing
same-line comment. Without them the packet would orphan prose describing code that no longer exists.

An independent cross-check confirms the two candidate sets agree where they should: the seeded
census's 103 covered candidates and the previously-shipped manifest's 103 declarations have **zero
symmetric difference**.

---

## 8. The before/after differential

`h4-before` (pristine, `53799e8…`) against `h4-after` (deleted, `883e6aa8…`), same 330 contexts,
same seeded database, same 43 blast selectors, same 113-longhand property universe, same 11 cached
network assets, compared with the **no-suppression-list** comparator:

```
run                 : h4 before vs after (101 declarations deleted)
mode                : after (allowed non-zero: candidatesLost)
identical CSS       : false
contexts compared   : 330
  computedDifferences      0
  ownerDifferences         0
  candidatesLost           52425  (allowed)
  candidatesGained         0
  pagePromotions           0
  pixelDifferingContexts   0
  elementsOnlyBefore       0
  elementsOnlyAfter        0
  blastNodesOnlyBefore     0
  blastNodesOnlyAfter      0
  stackDifferences         0
verdict             : PASS
```

Read term by term, because each one falsifies a different failure mode:

| Term | Result | What a non-zero would have meant |
|---|---:|---|
| `computedDifferences` | **0** | the deletion changed something a user can see |
| `ownerDifferences` | **0** | a different declaration now owns a longhand |
| `candidatesGained` | **0** | a deletion **resurrected** a rule — the G3/G6/G7 hazard |
| `pagePromotions` | **0** | a page-bundle declaration was promoted to owner |
| `pixelDifferingContexts` | **0** | the M3-scoped element raster moved |
| `elementsOnly*`, `blastNodesOnly*` | **0** | the DOM itself differed, so the comparison was invalid |
| `stackDifferences` | **0** | stylesheet order or layer structure moved |
| `candidatesLost` | 52,425 | **this is the deletion** — the only term permitted to move |

`candidatesLost` is the positive control: 101 declarations vanished from the candidate set of every
longhand they used to sit behind, across 330 contexts, and **not one longhand changed owner or
value as a result**. That is the definition of a declaration that owns nothing.

The same-CSS control (§5) and this run differ in exactly one input — the stylesheet — so the zero on
every other term is attributable to the deletion and not to harness stability, which the control
independently established at zero.

### 8.1 Post-review single-process paired proof

The `h4` aggregate was valid, but it captured the two stylesheet states in separate processes.
Review correctly identified a stronger design: serve the pristine stylesheet as a route override
against the on-disk deleted stylesheet, capture both sides of each context consecutively, and keep
the browser, server, seeded database, network cache and process fixed. This removes cross-run state
as a possible silent confounder.

`h5-paired-full` implements that design. One Node process (PID 19348) and one Flask listener (PID
27884) captured **330 pristine + 330 deleted** sides. The on-disk file remained
`883e6aa85564c42b36ca801529081b279f119e5c99a539dc235bc84d72107964` throughout; only the response
body for `/static/css/components.css` changed between paired sides. The pristine override was
reconstructed from the branch base and refused to run unless its bytes hashed to
`53799e819816b15a46a6e30ba7751c3e46781cb193095398947d139bdf171099`.

| Paired-run identity/control | Result |
|---|---|
| Contexts | **330 before + 330 after**, 330 unique labels on each side, identical ordered label set |
| Paired process | **same PID 19348** on both indices |
| CSS identities | pristine `53799e8…` / deleted `883e6aa…`; on-disk identity stayed deleted |
| Frozen database | `7cef8e0a…` on both sides; startup/end runtime DB hashes identical |
| Manifest | `d4e2dfee3bae1b77827960a4acb1e5d011a24372c0a76c2dd5384045f3a77ac5` on both sides |
| Property universe / blast set | 113 / 43, identical, blast cap 0 (uncapped) |
| Network | 11 cached assets, **0 unavailable**, identical on both sides |
| Unstable computed passes / retries | **0 / 0** |
| Exclusivity guards | 354 checks, one CSS hash, one runtime DB hash, one listener PID |
| Process stderr | **0 bytes** |

The hardened comparator also refuses an `after` run unless the CSS identities differ and
`candidatesLost > 0`; that makes “compared the same input twice” and “captured no candidate
effect” fatal rather than clean-looking zeroes.

```
run                 : h5 single-process paired (101 declarations deleted)
mode                : after (allowed non-zero: candidatesLost)
identical CSS       : false
contexts compared   : 330
  computedDifferences      0
  ownerDifferences         0
  candidatesLost           52425  (required positive control)
  candidatesGained         0
  pagePromotions           0
  pixelDifferingContexts   0
  elementsOnlyBefore       0
  elementsOnlyAfter        0
  blastNodesOnlyBefore     0
  blastNodesOnlyAfter      0
  stackDifferences         0
positive controls   : PASS
verdict             : PASS
```

| `h5` artifact | SHA-256 |
|---|---|
| `h5-paired-full/before/index.json` | `2fa635a8bfd019cbff8b3fce1f47c1d065ff3bd36f12ee1373436a4686b42dd6` |
| `h5-paired-full/after/index.json` | `133c1c664ceec30ee3e8dc54710b2ceaf230470359de94acae476b4b58374dfa` |
| `h5-paired-full-strict.json` | `0a93e67145e30c6c3d9b741b6b817756bf4b153b1c3a0b31994216a9cfd3f113` |
| stdout / empty stderr | `4c2572a954b7eb4678b9b9c98465bb98d499a93c07011756dedda07c6b31dce7` / `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

---

## 9. What was deleted

All 101 declarations lie between lines 4,151 and 5,130.

### 9.1 The `.summary-frame` glass table generation — 10 declarations, 5 rules deleted whole

Every declaration carries `!important` and every one lost: the Weekly and Session bundles repaint
the same longhands later in the same origin, and `components.css` loads before both on the routes
that mount a summary frame.

| Line | Selector | Declarations |
|---:|---|---:|
| 4150 | `.summary-frame.frame-calm-glass .table` | 2 |
| 4155 | `.summary-frame.frame-calm-glass .table thead th` | 4 |
| 4162 | `.summary-frame.frame-calm-glass .table tbody td` | 1 |
| 4199 | `[data-theme='dark'] .summary-frame.frame-calm-glass .table thead th` | 2 |
| 4204 | `[data-theme='dark'] .summary-frame.frame-calm-glass .table tbody td` | 1 |

### 9.2 The frame / filters / collapsible generation — 91 declarations, 6 rules deleted whole

The unlayered originals of the shared frame furniture. They lose to the `@layer workout` owners —
layer order inverts for `!important`, so a layered important declaration outranks an unlayered one
at any specificity (G10 / A6) — and to the page bundles.

Lines are **pristine rule-head lines**, as recorded by postcss in
`artifacts/wp4_4/h4-manifest-101.json`.

| Line | Selector | Deleted | Rule |
|---:|---|---:|---|
| 4517 | `.frame-title` | 8 | partial |
| 4534 | `[data-theme='dark'] & .frame-title, … .filters-title` | 3 | partial |
| 4542 | `[data-theme='dark'] & .action-frame .frame-title, …` | 2 | partial |
| 4552 | `.filters-section` | 8 | partial |
| 4567 | `.filters-title` | 9 | partial |
| 4629 | `.action-frame` | 4 | partial |
| 4701 | `.collapsible-frame` | 4 | partial |
| 4731 | `.frame-header` | 6 | partial |
| 4762 | `.frame-title, .filters-title` | 3 | partial |
| 4791 | `[data-theme='dark'] & .collapsible-frame` | 3 | **whole** |
| 4810 | `[data-theme='dark'] & .frame-header` | 2 | partial |
| 4828 | `[data-theme='dark'] & .frame-title, … .filters-title` | 1 | partial |
| 4835 | `.collapse-toggle` | **17** | partial |
| 4871 | `.collapse-toggle i` | 1 | partial |
| 4910 | `.frame-content` | 2 | partial |
| 4974 | `.filters-section .frame-header` | 1 | partial |
| 5010 | `[data-theme='dark'] & .input-fields-group` | 1 | **whole** |
| 5019 | `[data-theme='dark'] & .input-fields-group .form-control, … .form-select` | 3 | **whole** |
| 5034 | `[data-theme='dark'] & .collapsible-frame` | 2 | **whole** |
| 5039 | `[data-theme='dark'] & .collapsible-frame .frame-header` | 1 | partial |
| 5050 | `[data-theme='dark'] & .btn-primary` | 3 | **whole** |
| 5061 | `[data-theme='dark'] & .btn-secondary` | 3 | **whole** |
| 5077 | `.frame-header-2025` | 2 | partial |
| 5113 | `.collapse-toggle .toggle-icon` | 1 | partial |
| 5129 | `.frame-content` | 1 | partial |

10 + 91 = **101**. The nineteen partial rules are pinned in
`tests/test_css_wp4_4_components_contracts.py` by `(selector, post-deletion line)`, not by
occurrence index — an earlier draft keyed them by index and ten of the nineteen silently resolved to
the wrong rule, several of them inside `@layer workout` where this packet never reached.

The largest single cut, `.collapse-toggle`, is the one the removal oracle trimmed: 19 declarations
were nominated and **17** deleted. Its `cursor: pointer` matched **178** longhand instances across
Workout Log and Workout Plan, at every width, in both themes, and under reduced-motion, contrast,
print and forced-pseudo — and won **none** of them. Its `color` and `background`, nominated by the
same census, survive.

Nineteen rules survive with only their dead declarations removed; none was emptied.

---

## 10. Gates

All gates were run on the shipped file, `883e6aa8…`, serialized — no probe, server, database or test
run overlapped another.

| Gate | Result |
|---|---|
| `tests/test_css_wp4_4_components_contracts.py` (this packet) | **7 passed** |
| Pyright, packet contract | **0 errors**; `close_index` initialized and narrowed without changing the assertion |
| `tests/test_css_cascade_contracts.py` (shared, unmodified) | **passed** |
| `tests/test_css_wp4_4_a_baseline_contracts.py` (Packet a, unmodified) | **passed** |
| Full `pytest tests/` | **2,278 passed, 1 skipped, 0 failed** (370 s) |
| Chromium E2E, full suite | **475 passed, 0 failed**, 17 not run (§10.2) |
| Chromium visual gate (`PW_VISUAL_SEED=1`) | 66 passed, **2 pre-existing failures** (§10.2) |
| Stylelint, seven WP4.4 surfaces | **2,844 → 2,775 (−69)**, **0 category increases** |
| Post-review Stylelint re-measure | **2,775**, byte-identical to the `h4` after report; SHA-256 `e7952a1d…` |
| PostCSS structure | parse **PASS**; 0 empty rules; 0 empty at-rules; stack differential 0 |
| Region H SHA-256 | `18658442…` — **unchanged**, 282 lines, source file untouched |
| Tracked paths changed | exactly the three authorized |
| `components.css` diff shape | **0 insertions, 138 deletions** |

The local structure helper also carries a conservative “orphan comment” heuristic. It reports one
standalone `/* Modal Base Styles */` comment at line 2374 on both the pristine and deleted files
(**1 → 1**), so that pre-existing signal is not treated as deletion debris. The actual structural
requirements are clean: both files parse, neither has an empty rule or at-rule, and the paired
stylesheet-stack comparison is zero.

### 10.1 Stylelint, per rule

Measured by re-running the committed `scripts/css_audit/stylelint_surfaces.mjs` over both the
pristine and the shipped file, not by trusting an older baseline:

| Rule | Before | After | Δ |
|---|---:|---:|---:|
| `declaration-no-important` | 1,259 | 1,239 | **−20** |
| `declaration-property-value-disallowed-list` | 1,099 | 1,060 | **−39** |
| `no-descending-specificity` | 243 | 235 | **−8** |
| `declaration-block-no-duplicate-properties` | 2 | 1 | −1 |
| `no-duplicate-selectors` | 23 | 22 | −1 |
| `property-no-unknown` | 2 | 2 | 0 |
| `selector-max-id` | 115 | 115 | 0 |
| `selector-max-specificity` | 101 | 101 | 0 |
| **total** | **2,844** | **2,775** | **−69** |

No category increased, so the "any Stylelint category increase" rollback criterion did not fire.
`selector-max-id` and `selector-max-specificity` are unmoved, as expected: this packet deletes
declarations, never selectors, and the `:is()` family it would have to touch belongs to WP4.4-i.

### 10.2 The E2E result, stated honestly

**The functional suite is clean: 475 passed, 0 failed.**

Two things in the visual layer need naming rather than burying.

**The 17 "did not run" are the `§4` thumbnail baselines.** They require `PW_VISUAL_SEED=1`; under the
default functional seed (`e2e/scripts/prepare_e2e_db.py`, which wipes user state) their fixture does
not exist. This is the config's documented behaviour, not a regression.

**Running the visual specs without that flag fails 36 of 66 — on pristine CSS too.** The failure is
`Expected an image 375px by 9330px, received 375px by 3889px`: a page-*height* difference from
missing plan rows, i.e. a data difference, not a paint difference. Run correctly, with
`PW_VISUAL_SEED=1`, the picture is:

| | pristine `53799e8…` | shipped `883e6aa8…` |
|---|---|---|
| passed | 66 | 66 |
| failed | 2 | 2 |
| did not run | 16 | 16 |
| `plan-desktop-light-advanced.png` | 6,084 px differ | **6,084 px differ** |
| `workout-plan-desktop-dark.png` | 875 px differ | **875 px differ** |

**The two failures are byte-for-byte identical before and after the deletion** — same snapshots, same
pixel counts — so they are pre-existing baseline drift on the branch base and are attributable to
this packet in no part. They belong to the WP4.0 known-red ledger and the M7 band. This packet
neither introduced nor repaired them.

That A/B is the honest form of the claim. "The visual suite passed" would have been false; "the
visual suite is unchanged by this deletion" is true and is what the differential in §8 independently
predicted at 330 contexts with **0 differing rasters**.

### 10.3 Red-path proofs (F16)

A contract that cannot fail is not a gate. Both new assertions were driven red on the shipped file
and the file restored afterwards:

| Injected violation | Reds |
|---|---|
| `cursor: pointer` put back into `.collapse-toggle` | `test_partial_rules_survive_without_their_dead_declarations`, `test_the_deletion_was_pure_removal` |
| the withdrawn `background: none` deleted from `.collapse-toggle` | the two above **plus** `test_the_two_withdrawn_declarations_are_still_present` |

After each, `components.css` was restored and re-verified at `883e6aa8…` with all 7 contracts green.

A third red path was found without being sought: keying the partial-rule assertions by occurrence
index silently resolved ten of nineteen rules to the wrong rule — `.frame-title` #0 landed on line
3815, inside `@layer workout`. The line-anchored form reds instead of drifting.

---

## 11. Reproducing this

Every command below runs from the worktree root, serialized, one at a time.

```bash
# 0. restore the pristine file if needed
node artifacts/wp4_4/h_apply.mjs --mode restore

# 1. same-CSS control: two runs of identical CSS, then compare with no waiver
node artifacts/wp4_4/h_differential.mjs --out artifacts/wp4_4/h4-before \
  --manifest artifacts/wp4_4/h-narrowed-deletion-manifest.json \
  --expect-css-sha 53799e819816b15a46a6e30ba7751c3e46781cb193095398947d139bdf171099 \
  --expect-db-sha  7cef8e0acb9106534ba9ff8a935d825d94f913211191f43e46dba830b4da1d47
node artifacts/wp4_4/h_differential.mjs --out artifacts/wp4_4/h4-control  # same flags
node artifacts/wp4_4/h_compare_strict.mjs --mode control \
  --before artifacts/wp4_4/h4-before --after artifacts/wp4_4/h4-control \
  --out artifacts/wp4_4/h4-control-strict.json

# 2. the 446-context seeded census
node artifacts/wp4_4/h_census.mjs \
  --expect-css-sha 53799e819816b15a46a6e30ba7751c3e46781cb193095398947d139bdf171099 \
  --expect-db-sha  7cef8e0acb9106534ba9ff8a935d825d94f913211191f43e46dba830b4da1d47

# 3. the two remaining oracles
node artifacts/wp4_4/h_zero_winner_check.mjs --dir artifacts/wp4_4/h4-before \
  --manifest artifacts/wp4_4/h-narrowed-deletion-manifest.json \
  --out artifacts/wp4_4/h4-zero-winner.json
node artifacts/wp4_4/h_certify.mjs --manifest artifacts/wp4_4/h-narrowed-deletion-manifest.json \
  --out artifacts/wp4_4/h4-certify.json --widths 375,768,1440 \
  --expect-css-sha 53799e819816b15a46a6e30ba7751c3e46781cb193095398947d139bdf171099 \
  --expect-db-sha  7cef8e0acb9106534ba9ff8a935d825d94f913211191f43e46dba830b4da1d47

# 4. build the intersection manifest (self-validating) and apply it
node artifacts/wp4_4/h_build_manifest.mjs --ids artifacts/wp4_4/h4-ids-103.json \
  --out artifacts/wp4_4/h4-manifest-103.json \
  --verify-against artifacts/wp4_4/h-narrowed-deletion-manifest.json
node artifacts/wp4_4/h_build_manifest.mjs --ids artifacts/wp4_4/h4-ids-101.json \
  --out artifacts/wp4_4/h4-manifest-101.json
node artifacts/wp4_4/h_apply.mjs --manifest artifacts/wp4_4/h4-manifest-101.json --mode apply

# 5. the after differential, compared against the admissible before
node artifacts/wp4_4/h_differential.mjs --out artifacts/wp4_4/h4-after \
  --manifest artifacts/wp4_4/h4-manifest-101.json \
  --expect-css-sha 883e6aa85564c42b36ca801529081b279f119e5c99a539dc235bc84d72107964 \
  --expect-db-sha  7cef8e0acb9106534ba9ff8a935d825d94f913211191f43e46dba830b4da1d47
node artifacts/wp4_4/h_compare_strict.mjs --mode after \
  --before artifacts/wp4_4/h4-before --after artifacts/wp4_4/h4-after \
  --out artifacts/wp4_4/h4-after-strict.json

# 6. post-review classification with five fatal, independently proven live controls
node artifacts/wp4_4/h_apply.mjs --manifest artifacts/wp4_4/h4-manifest-101.json --mode restore
node artifacts/wp4_4/h_certify.mjs --manifest artifacts/wp4_4/h4-manifest-101.json \
  --out artifacts/wp4_4/h5-certify-live-spikes.json --widths 375,768,1440 \
  --live-control-ids 1187,196,1178,477,1094 \
  --expect-css-sha 53799e819816b15a46a6e30ba7751c3e46781cb193095398947d139bdf171099 \
  --expect-db-sha  7cef8e0acb9106534ba9ff8a935d825d94f913211191f43e46dba830b4da1d47
node artifacts/wp4_4/h_apply.mjs --manifest artifacts/wp4_4/h4-manifest-101.json --mode apply

# 7. post-review aggregate: both stylesheet states captured per context in one process
node artifacts/wp4_4/h_differential.mjs --out artifacts/wp4_4/h5-paired-full \
  --manifest artifacts/wp4_4/h4-manifest-101.json \
  --expect-css-sha 883e6aa85564c42b36ca801529081b279f119e5c99a539dc235bc84d72107964 \
  --expect-db-sha  7cef8e0acb9106534ba9ff8a935d825d94f913211191f43e46dba830b4da1d47 \
  --paired-before-ref 4b7ca585cf03cc5f2de4fd88c257f29460173640 \
  --paired-before-sha 53799e819816b15a46a6e30ba7751c3e46781cb193095398947d139bdf171099
node artifacts/wp4_4/h_compare_strict.mjs --mode after \
  --before artifacts/wp4_4/h5-paired-full/before \
  --after artifacts/wp4_4/h5-paired-full/after \
  --out artifacts/wp4_4/h5-paired-full-strict.json \
  --label h5-single-process-paired
```
