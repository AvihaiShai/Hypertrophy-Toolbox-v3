# WP4.4-i — `components.css` `:is()` shared-selector repair

**Status:** implemented across **all thirteen rules** of the family. One branch of four was
repaired; the other three are retained deliberately, two because de-weighting them is
*measured* to resurrect suppressed page-local rules and one because it is the specificity
donor.

**Branch:** `wt/wp4-4-i-is-repair`. **Base:** `89523ed` (`main` after PR #210).
**`static/css/components.css`:** `883e6aa8…` → `0702558b…`, **5,207 newlines before and
after**, 14 selector lines rewritten in place, no declaration added or removed.

> **Verification is complete with one explicit, owner-approved exception.** Gate 8's "no
> category up" is **not** satisfied: `no-descending-specificity` rises by 10. §7 enumerates
> every one of those warnings and attributes 100% of them to the approved split lines. The
> packet also **does not deliver** the `selector-max-id` / `selector-max-specificity`
> movement its plan row projected; §7 records that as measured under-delivery rather than
> restating the projection.

---

## 1. What was approved

Ruling **N4** stopped the arc after `h`. The fresh owner decision approved WP4.4-i as
**proof-first and narrow-or-abandon**: repair only branches *proven* safe under **N3**,
retain unsafe or inconclusive branches unchanged, and abandon the packet on documented
evidence if no branch survives. The admissible shape is **N9's CSS-local split of the
selector list**; `:where()`, page bundles, templates, JavaScript, layer membership and
deletion of page-local offenders are all excluded.

A follow-up owner clarification authorised a **narrow extension of i's test write set** —
re-expressing WP4.4-h's global `:where()`/`:hover` occurrence locks so they cannot forbid
i from repairing the exact family i owns (§4) — and a **bounded Stylelint exception** for
`no-descending-specificity` only (§7).

---

## 2. The family, and why the ID branch cannot be the one that moves

Twelve four-branch rules at `:3335`–`:3411` (R1 carrying two selector lines) and the
three-branch reduced-motion rule at `:4398`–`:4415` shared one argument list:

```
:is(#workout[data-page="workout-plan"], .workout-log-page, .summary-frame.frame-calm-glass, .progression-plan-container)
```

`:is()` takes the specificity of its most specific argument — `#workout[data-page="workout-plan"]`
at **(1,1,0)** — so all four branches carried `a = 1`, including the three with no ID.

| Branch | Split out | Consequence |
|---|---|---|
| `#workout[data-page="workout-plan"]` | specificity **unchanged** — it owns the ID itself | pure loss: gains nothing, strips the donor from the other three at once |
| `.workout-log-page` | (1,x,y) → (0,x,y) | **unsafe** — §3 |
| `.summary-frame.frame-calm-glass` | (1,x,y) → (0,x,y) | **unsafe, measured** — §3 |
| `.progression-plan-container` | (1,x,y) → (0,x,y) | **safe, measured — repaired on all 13 rules** |

**The ID branch must stay inside the `:is()` as the donor.** Removing it de-weights every
remaining branch at once. So the repair splits *out* the branch proven safe to de-weight
and leaves the donor grouped with both unsafe branches. The retained group
`:is(#workout[data-page="workout-plan"], .workout-log-page, .summary-frame.frame-calm-glass)`
is **bit-identical in specificity** to the four-branch original on all fourteen selector
lines, because the donor is unchanged and `:is()` takes the maximum.

Each rewritten line reads `<progression arm>, <donor-group arm>` on **one physical line**
(§4, zero-line invariant), lowest specificity first.

**Result:** `.progression-plan-container` no longer receives ID-level specificity from this
family for **any of its 39 declarations**.

---

## 3. Per-branch safety, measured

### `.summary-frame.frame-calm-glass` — UNSAFE, and the packet's known-live control

Both summary bundles carry ID-scoped `!important` table rules that lose today **only**
because the family borrows `a = 1`:

| Page-local rule | Specificity | Contends with |
|---|---|---|
| `pages-weekly-summary.css:120-123` `#weekly-summary-container .table th, … td { border: 1px solid var(--wk-table-border) !important }` | (1,1,1) | R2 `border-color: transparent` |
| `pages-weekly-summary.css:172-177` `[data-theme='dark'] #weekly-summary-container .table thead th` | (1,2,2) | R9 |
| `pages-weekly-summary.css:183-188` `[data-theme='dark'] #weekly-summary-container .table td` | (1,2,1) | R10 |

`pages-session-summary.css:116-127, 178-204` mirrors all of them.

This was not left as arithmetic. The branch was de-weighted in a scratch mutation and the
five-route differential re-run against the same frozen database:

| Control result | Value |
|---|---|
| Computed-value changes | **8,784** |
| Routes affected | session-summary 4,542 · weekly-summary 4,242 |
| Routes unaffected | workout-plan **0** · workout-log **0** · progression **0** |
| By theme | dark 5,616 · light 3,168 |
| Properties | `border-*-color` 7,056 · `color` 972 · `background-color` 756 |

The resurrected values are the **unmigrated legacy palette**: `border-*-color:
rgba(0,0,0,0) → rgb(64,64,64)` (`#404040`), `color: rgb(238,241,246) → rgb(224,224,224)`
(`#e0e0e0`), `background-color: rgb(22,26,45) → rgb(26,26,26)` (`#1a1a1a`) and
`→ rgb(45,45,45)` (`#2d2d2d`) — `--wk-dark-*` / `--ss-dark-*`, which `theme-dark.css` does
not remap.

**This run does double duty.** It is the N3 disproof for this branch *and* the known-live
control for the instrument: a differential reporting zero is indistinguishable from a broken
differential until it is shown to report non-zero when the cascade really moves. The
instrument is unchanged between that run and §5, so the control carries.

### `.workout-log-page` — UNSAFE, retained on Inventory B

[Inventory B](CSS_PHASE4_WP4_4_N4_INVENTORY_B_REGIONS_ABC.md) §3.1 measured 45 declarations
across regions A/B/C: **16 lose only to this family**, 13 more are partially blocked by it,
and region B — the dark-mode Workout Log header — has **zero** always-wins. Retained inside
the donor group, so its specificity is unchanged. §6 measures that nothing resurrected.

### `#workout[data-page="workout-plan"]` — retained as the donor

Splitting it changes its own specificity by nothing while de-weighting the other three.
Retained. The ten frozen WP4.3i interaction-state declarations (G6) at
`pages-workout-plan.css:2522` (1,3,3) and `:2537` (1,4,3), and `tr.superset-group-1..4`
(PR#6), are consequently untouched: they lose to R6 (1,4,3) and R12 (1,5,3) by the same
margin as before, and the superset rules target `tr` where the family declares only on
`td`/`th`.

### `.progression-plan-container` — SAFE, repaired

`static/css/pages-progression.css` contains **no** table-matching rules at all (341 lines
read in full). Every other rule that can match the goals table lives in
`components.css:1205-1546` — *before* the family in the same file, so it loses on source
order even at a tie — and sits at least `b + 1` below the post-split Progression arm.
`theme-dark.css`'s entire table block is `:where()`-wrapped to **(0,0,0)** and can never
win. All 39 family declarations are `!important`, so every non-`!important` rule in
`layout.css`'s `.tbl` system and in Bootstrap loses unconditionally. No JavaScript writes
inline styles or classes to that table.

Two independent analyses reached this verdict; §5 measures zero computed-value change on
`/progression` across twelve contexts.

---

## 4. Re-expressing WP4.4-h's `:where()` / `:hover` premise

`tests/test_css_wp4_4_components_contracts.py` froze **global text-occurrence counts**
(`:where(` == 58, `:hover` == 115). Splitting a selector line duplicates every token on it,
so those locks forbade repairing R1 (`:where(.table)`) and R6/R12 (`tbody tr:hover td`) —
15 of the 39 declarations, including the family's largest block.

Those locks were over-broad for their purpose. h's premise is that **h touched no
`:where()`/`:hover` construct**, not that such constructs may never change. Under owner
authorisation the premise is **re-expressed, not relaxed**, and the protection is now
narrower in scope and stronger in kind.

The file is partitioned on the retained donor group — structurally, not by line number,
because the zero-line invariant is what keeps the layer span pinned:

| Token | total | on the 14 i-owned lines | outside (frozen at h's counts) |
|---|---:|---:|---:|
| `:is(` | 19 | 14 | **5** |
| `:where(` | 59 | 2 | **57** |
| `:hover` | 117 | 4 | **113** |

The outside counts are **identical before and after** the split — the split only ever
duplicates a token onto the line it already occupied. The inside counts are the exact
attributable delta: **+1 `:where(`** (R1's first arm) and **+2 `:hover`** (R6, R12). The
four exact post-split selector shapes are asserted verbatim. Every other h contract and
deletion invariant is untouched; `!important` stays 919 and the 5,207-newline count is
re-asserted.

### Red paths, all proven

| Mutation | Fires |
|---|---|
| Unrelated `:where(` **added** outside the family | ✔ 2 failed |
| Unrelated `:hover` **removed** outside the family | ✔ 2 failed |
| h-family erosion — a `.value-changed` occurrence removed | ✔ 1 failed |
| `.progression-plan-container` re-admitted into an `:is()` list | ✔ 3 failed |
| A family split arm dropped (13 lines instead of 14) | ✔ 3 failed |
| A family line reflowed onto two lines | ✔ 9 failed, incl. Packet-a |

One finding worth recording rather than fixing: h's `r"\.value-changed"` pattern also
matches `.value-changed-x`, so a *rename* does not red it — only a genuine removal does.
That is a pre-existing looseness in a contract this packet may not alter, and it is
reported here rather than silently patched.

### The N6 amendment

`tests/test_css_cascade_contracts.py:1616` pinned the four-branch string. **N6** authorises
i to amend `:1614-1627` solely to re-express the same premise, and the premise — *the
shared rule still out-specifies the page-local Workout Log families* — is unchanged,
because the donor and `.workout-log-page` both remain in the retained group and its
specificity is bit-identical.

The edit is **one line, line-count-neutral** (1,789 lines before and after). That matters:
`tests/test_css_wp4_4_a_baseline_contracts.py` pins `assertionLines` for that test as
absolute line numbers, so an amendment that added or removed a line would red a register
this packet may not touch. The two other pinned substrings at `:1335` and `:1487`
(`'#workout[data-page="workout-plan"], .workout-log-page'`) survive verbatim in the
retained group and needed no change.

### The zero-line invariant

`tests/test_css_wp4_4_a_baseline_contracts.py:145-151` re-derives
`measure.layer_spans("components.css")` from the **working tree** and pins
`openLine 3539 / closeLine 4104`. The whole family sits above 3539, so adding even one line
moves the span — the same trap that cost WP4.4-h 158 of 247 cuts. A first attempt that split
each rule across two lines produced exactly that:

```
components.css @layer workout: openLine 3539 → 3552   (6 contract failures, 2 files)
```

Every split is therefore written on one physical line. The invariant is invisible in the CSS
and a routine reformatting pass would break it with a confusing error in an unrelated file,
so it is pinned by `test_the_repair_added_no_lines` and
`test_every_repaired_rule_keeps_both_arms_on_one_physical_line`.

---

## 5. The five-route computed-value differential

The committed pixel matrix cannot falsify this repair: `visual.spec.ts` is deep-gate-only,
carries `maxDiffPixels: 800` against V1's "zero visual differences", and
`docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` already reds **every desktop capture of
every affected route in at least one theme** — so a real regression there is
indistinguishable from the inherited red by any assertion M7 permits. The primary oracle is
therefore a computed-value differential; the pixel matrix corroborates.

Harness: [`i_five_route_computed.mjs`](../scripts/css_audit/i_five_route_computed.mjs),
diff: [`i_diff_computed.mjs`](../scripts/css_audit/i_diff_computed.mjs). Both committed —
a gitignored one-off cannot satisfy a before/after gate (A11), which is exactly how
Inventory B's evidence was lost (§8).

**Matrix:** 5 routes × 2 themes × 3 widths (375/768/1440) × rest/hover = **60 contexts**,
50 computed longhands per element.

| Result | Value |
|---|---|
| Contexts compared | 60 |
| Elements compared | 15,168 |
| Computed values compared | **758,400** |
| Context drift | **0** |
| Element drift (DOM structure) | **0** |
| **Computed-value differences** | **0** |

Measured `883e6aa8…` → `0702558b…` against the same frozen database. The known-live control
in §3, run through this identical instrument, reports **8,784** differences, so this zero is
a measurement rather than a blind spot.

Controls, each fatal: same-CSS control (every context captured twice, zero differing); DOM
presence (every route renders a `.table-calm` with body cells); theme applied (`data-theme`
asserted, per Inventory B defect 2); transition settling via the Web Animations API before
any computed read (M6a). All clean on both halves.

---

## 5b. The visual red, its root cause, and the separate harness correction

The differential says the repair changes nothing. The committed visual matrix initially
disagreed: `progression desktop dark` and `progression tablet dark` failed
**deterministically** — 3,613 and 2,235 pixels, identical to the pixel over three repeats,
while pristine `main` passed the same captures 18/18. A contradiction between two oracles
has to be resolved, not averaged.

**The production cascade really is unchanged.** A full-page capture — every element, every
computed property, plus bounding rects, rendered against the same database the visual
matrix uses — reports **0 differences across 276 elements at both widths**.

**The red came from the test harness's own injected CSS.** `e2e/visual-helpers.ts` flattened
dark surfaces with a rule computing to **(0,3,1)**, and the Progression goals table carries
`data-visual-surface`. R1's Progression arm moves from **(1,3,0)** to **(0,3,0)** — across
that rule — so the flattener took `border-color` and `border-radius`. `background` and
`box-shadow` were unaffected because the family's dark rule R8 re-declares them at (0,4,0).

**That was fixed as a separate, independently proven change** — PR #211, merged as
`1019d34`, evidence in
[`CSS_PHASE4_WP4_4_VISUAL_HELPER_BAND_EVIDENCE.md`](CSS_PHASE4_WP4_4_VISUAL_HELPER_BAND_EVIDENCE.md).
It splits the flattener by property and withholds only border geometry, from only that
element, keyed on an inert `data-visual-preserve-border` hook. On unmodified `main` it is a
measured no-op: match-set delta of exactly one element per Progression dark viewport, zero
computed differences, zero element-scoped pixels, and a visual failure set identical to
main's. No snapshot was rebaselined.

**The transferable finding.** De-weighting a shared selector does not only expose
*page-local* rules. It exposes anything occupying the vacated specificity band — including
CSS that exists only inside the test harness. An N3 pre-change inventory that sweeps
`static/css/**` will not find it. Any future packet lowering a shared selector's specificity
must sweep `e2e/**` injected CSS as well.

---

## 6. G3 — Workout Log regions A, B and C, before and after

G3 is the packet's hard gate, and it binds even though the `.workout-log-page` arm's
specificity is provably unchanged — the shared selector *text* moved, so the measurement is
owed regardless of the arithmetic. Inventory B fixes the pass condition: *"any declaration
whose `wins` rises from 0 is a resurrection and must be accounted for explicitly."*

Both halves run the committed [`n4_regions_abc.mjs`](../scripts/css_audit/n4_regions_abc.mjs)
against the same probe database; the diff is
[`i_diff_g3.mjs`](../scripts/css_audit/i_diff_g3.mjs).

| | before (`883e6aa8…`) | after (`0702558b…`) |
|---|---:|---:|
| Ownership records | 56,304 | 56,304 |
| Declarations | 45 | 45 |
| always-wins | 9 | 9 |
| mixed | 6 | 6 |
| never-wins | 30 | 30 |
| no record | 0 | 0 |

| Diff class | Count |
|---|---:|
| **Resurrections** (`wins` 0 → n) | **0** |
| Other `wins`/`loses` drift | **0** |
| Declaration-set drift | **0** |

All controls clean on both halves: specificity model 10/10, the G3 ID-free assertion (every
region arm `a = 0`), DOM presence, dark-theme presence, same-CSS control (56,304 records, 0
differing), known-live control (live winners found in A, B and C), and resolution self-check
(4,800 checked, 0 mismatches).

**The before half reproduces Inventory B's published totals exactly** — 56,304 / 45 / 9 / 6
/ 30 / 0 — despite running against a regenerated probe database rather than the lost
`probe-frozen.db`. The A–C measurement is invariant to the fixture rebuild, so Inventory B's
numbers stand and these halves are comparable to it as well as to each other.

The 16 declarations Inventory B identified as losing *only* to the `:is()` family, and the
13 partially blocked by it, remain suppressed. Region B's dark-mode Workout Log header still
has zero always-wins. Nothing resurrected.

---

## 7. Stylelint — the bounded exception, enumerated

Measured with the pinned configuration over `static/css/**`; `components.css` is the only
file changed.

| Rule | Before | After | Δ |
|---|---:|---:|---:|
| `declaration-no-important` | 919 | 919 | 0 |
| `declaration-property-value-disallowed-list` | 742 | 742 | 0 |
| **`no-descending-specificity`** | 194 | 204 | **+10** |
| `selector-max-specificity` | 27 | 27 | 0 |
| `no-duplicate-selectors` | 20 | 20 | 0 |
| `selector-max-id` | 17 | 17 | 0 |
| `declaration-block-no-duplicate-properties` | 1 | 1 | 0 |

### Every new warning, attributed

The exception is bounded to `no-descending-specificity` and requires that the increase be
mechanically caused **solely** by the approved split lines. Attributed per source line:

| Line | Before → After | Line is an approved split |
|---:|---|---|
| 3351 | 0 → 1 | ✔ |
| 3368 | 0 → 1 | ✔ |
| 3377 | 0 → 1 | ✔ |
| 3381 | 0 → 1 | ✔ |
| 3386 | 0 → 1 | ✔ |
| 3390 | 0 → 1 | ✔ |
| 3395 | 0 → 1 | ✔ |
| 3400 | 1 → 2 | ✔ |
| 3405 | 0 → 1 | ✔ |
| 3409 | 0 → 1 | ✔ |
| **net** | **+10** | **lines outside the approved set with any change: NONE** |

Four of the fourteen split lines (`3335`, `3336`, `3360`, `4413`) gained no warning.

A text-keyed diff initially showed 14 "new" warnings and 4 "removed", three of them at lines
`4153`, `4188` and `4337` — outside the approved set. Those are **not** new: their warning
text embeds the family selector as the counterpart, and that string lost a branch, so the
same warning re-serialised. Keyed on source line, their counts are unchanged. The
line-keyed attribution is the honest one and is what the table above reports.

No warning was suppressed, disabled or configured around; `.stylelintrc.json` is unmodified.
Stylelint is measure-only and non-blocking in CI (`.github/workflows/ci.yml:644`), and
against the pinned WP4.1 baseline every category remains far below it
(`no-descending-specificity` 783 → ~481 arc-wide).

### Measured under-delivery

i's plan row projected `selector-max-id` **191** and `selector-max-specificity` **188**
would "fall measurably — this is the only planned packet that can move them at the shared
level". **They did not move at all**, and cannot under any admissible shape: the retained
`:is()` still carries the ID on every one of the fourteen selector lines, and the split adds
ID-free arms rather than removing ID-bearing ones. Removing the ID is precisely what
de-weights the two branches measured unsafe in §3.

This is recorded as measured under-delivery. The projected gate movement **did not occur**.

---

## 8. Two defects in the inherited evidence trail

**Inventory B was not reproducible as written.** It reproduces against
`artifacts/wp4_4/probe-frozen.db` with `--expect-db-sha 7cef8e0a…`. `artifacts/**` is
gitignored (A11), and by the time this packet needed the *after* half of that same
before/after gate the file no longer existed. The surviving `artifacts/wp4_4/probe.db` has
**0 rows** in `user_selection` and `workout_log`, so every route renders an empty table.

Fixed: [`i_seed_probe_db.py`](../scripts/css_audit/i_seed_probe_db.py) derives the probe
database **deterministically from the committed `e2e/fixtures/database.visual.seed.db`**
and is byte-reproducible (`5bc6d340…` on repeated builds). **The generated database is not
committed** — only the script that regenerates it. Using the visual seed is also better
provenance: it is the database the visual matrix renders against, so this differential sees
what the pixel oracle would.

**The visual seed alone cannot exercise Progression.** `progression_goals` holds one row
with `completed = 1` and `routes/progression_plan.py:118-122` selects `WHERE completed = 0`,
so the Current Goals table renders a header and **zero body cells**. Progression is the only
route this packet changes; measuring it with an empty table would satisfy every control
while proving nothing (M6). The script seeds six open goals — enough to exercise
`tbody td`, `tr:nth-child(even) td`, `tr:last-child td` and `tr:hover td`, every
row-position rule in the family. Progression went from 11 elements per context to **95**.

---

## 9. Contracts and gates

`tests/test_css_wp4_4_i_is_repair_contracts.py` is packet-owned per **N1**. Its six tests
pin the thirteen-rule completeness, the zero-line invariant, the single-physical-line shape,
the donor-group invariant for both unsafe branches, the reduced-motion asymmetry, and the
whole-file token totals.

The reduced-motion asymmetry deserves its pin. That rule's `:is()` omits
`.summary-frame.frame-calm-glass` deliberately: summary table cells are **not**
transition-suppressed under `prefers-reduced-motion: reduce`. Normalising it would be a
visible behavioural change on two routes, and **nothing in this repository could observe
it** — no spec sets `reducedMotion`, and `e2e/visual-helpers.ts:44-48` forces
`transition-duration: 0s !important` globally. The rule now carries
`.progression-plan-container` plus a two-branch `:is()`, and no summary branch.

All figures below are from **post-rebase** runs onto `1019d34`; every pre-rebase result was
discarded rather than carried forward.

| Gate | Result |
|---|---|
| Full `pytest` | **2287 passed, 1 skipped** |
| CSS + visual contracts | **59 passed** |
| Computed-value differential | **0 differences / 758,400 values**, served sha asserted on both halves |
| Known-live control | **8,856** differences, summary routes only — the instrument is live |
| G3 regions A–C | **0 resurrections, 0 ownership drift** |
| Stylelint | **+10 `no-descending-specificity`, 100% attributed to the approved split lines**; every other category flat; no line outside the approved set changed |
| Visual matrix (visual specs only) | **37 failures, identities exactly `main`'s 37**; both Progression reds gone; **no snapshot changed** |
| Full Chromium suite | **49 failed / 475 passed / 17 not run — identical counts _and_ identities to `main`'s full-suite run** |

The full suite reports 12 more failures than the visual-only run
(`body-composition`, `user-profile`). Those are pre-existing full-suite state pollution:
earlier functional specs mutate the database before the visual captures run, and `main`
reproduces the same 49 with the same identities. `user-profile` was independently measured
**nondeterministic** — five captures of an identical variant produced five distinct hashes.

### A measurement defect found and closed during this packet

Several intermediate results in this arc were produced by harnesses that spawn a Flask
server and then poll port 5000. When a server from an earlier run was still listening, the
freshly spawned process failed to bind and exited, and the run measured the **stale** server
while reporting the sha of the file at `--root`. The recorded digest never proved which
checkout was rendered, so a zero could mean "no change" or "compared a checkout against
itself".

`scripts/css_audit/i_five_route_computed.mjs` now refuses to start when the port is held and
asserts that the **served** `components.css` bytes match the checkout under test — the served
bytes being what the browser actually cascades. Every number in this document comes from a
guarded run, and each capture records `servedCssSha256` alongside the on-disk digest.

---

## 10. Reproduction

```bash
# probe database (byte-reproducible; not committed)
python scripts/css_audit/i_seed_probe_db.py --out artifacts/wp4_4/i/probe-i.db
# → sha256 5bc6d3405464ca983123e95309b13cb1b505f28053bc043565adb2b0389a1b61

# five-route computed capture, once per checkout
node scripts/css_audit/i_five_route_computed.mjs \
  --root <checkout> --frozen-db artifacts/wp4_4/i/probe-i.db \
  --out artifacts/wp4_4/i/<label>

# differential (non-zero exit on any difference)
node scripts/css_audit/i_diff_computed.mjs \
  artifacts/wp4_4/i/before/computed.json artifacts/wp4_4/i/after13/computed.json

# G3 regions A-C, once per checkout, then diff
node scripts/css_audit/n4_regions_abc.mjs \
  --frozen-db artifacts/wp4_4/i/probe-i.db \
  --expect-db-sha 5bc6d3405464ca983123e95309b13cb1b505f28053bc043565adb2b0389a1b61 \
  --expect-css-sha d07e2c07ebe9585df2779ad078a3d5335247a4427cf41420af2497630173c8c6 \
  --out artifacts/wp4_4/i/g3-<label>
node scripts/css_audit/i_diff_g3.mjs \
  artifacts/wp4_4/i/g3-before/summary.json artifacts/wp4_4/i/g3-after13/summary.json
```

`pages-workout-log.css` is byte-identical to Inventory B's recorded digest (`d07e2c07…`) on
both sides.
