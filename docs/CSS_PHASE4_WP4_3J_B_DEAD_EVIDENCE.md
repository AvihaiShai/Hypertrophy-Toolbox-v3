# WP4.3j-b-dead — Workout Log inert responsive-family deletion

**Branch:** `wt/wp4-3j-b-dead` · **Base:** `origin/main` @ `ff9fe4b`
**File:** `static/css/pages-workout-log.css` (+ one cascade contract)
**Diff:** 11 insertions / 166 deletions in the bundle

---

## What this packet is, and how it differs from WP4.3j-b

WP4.3j-b was an **audit-only, zero-CSS-change** packet. It examined the apparent
duplicate responsive `@media` ladders, rejected the consolidation premise, and
classified three property families as inert. It explicitly did **not** authorize
their deletion:

> "Such a packet needs its own before/after pixel oracle, same-CSS control,
> cascade contracts, functional checks, and owner approval. This audit does not
> authorize the deletion."
> — [`CSS_PHASE4_WP4_3J_B_EVIDENCE.md`](CSS_PHASE4_WP4_3J_B_EVIDENCE.md)

**WP4.3j-b-dead is that separate deletion packet.** The j-b findings were treated
as a *nomination*, not as proof. Every liveness claim was re-established from
scratch in a fresh browser walk on this branch before a line was removed. No
responsive behavior was redesigned, and no j-b conclusion was taken on trust.

Branching note: this packet was cut fresh from merged `main` at `ff9fe4b`, not
continued from the pre-squash `wt/wp4-3j-b-media-ladders` history.

---

## Authorized scope, and what was deliberately left alone

**Deleted — three families, all independently re-proven inert:**

1. the complete eight-query `RESPONSIVE FRAME ADJUSTMENTS` block;
2. the `thead th` (padding / font-size / letter-spacing) and `td`
   (padding / font-size) rule blocks in the first responsive ladder;
3. the base `.workout-log-frame` `padding: var(--frame-padding, 1.25rem)`
   declaration.

**Retained — explicitly out of scope, and asserted present by the contract:**
the `max-width: 992px` table display/overflow rule; page-padding rules;
delete-button and icon sizing; routine-cell widths and routine typography; the
late `.legend-item` query; j-c header/cell-glass work; `components.css` and its
shared `:is()` selector; WP4.4; modal styling, `nth-child` restructuring,
tokenization, templates, JavaScript, SCSS, and generated Bootstrap.

The five first-ladder media **shells** that became empty were **kept**, each with
a one-line comment recording why. Removing them would have gone beyond deleting
proven-dead declarations into restructuring the ladder, and Stylelint carries no
`block-no-empty` rule, so the retained shells cost nothing. This is the only
reason the diff is not pure deletion.

---

## Oracles

Two oracles were used, because neither alone answers the question. The WP4.3i-dead
rule (a sentinel sweep over-reports; pair it with a differential **and** a
same-CSS control) and the WP4.3j-a rule (take the differential in the space the
claim lives) both applied.

### 1. Computed value + declaration ownership, 14 widths

A browser walk at **1200, 1201, 1280, 1281, 1366, 1367, 1536, 1537, 1600, 1601,
1920, 1921, 2560, 2561** captured, for a representative `thead th`, `tbody td`,
and the `.workout-log-frame`: the computed value of every padding longhand,
`font-size` and `letter-spacing`, **plus the full list of candidate declarations**
from every same-origin stylesheet whose rule matched the element under
currently-matching media conditions, ranked by importance, specificity and source
order. That is **504 computed/winner records per run**.

> **Method correction worth recording.** The first implementation ranked owners
> with a regex specificity model and a naive `,` split. Both are wrong on this
> page: the split shreds the `components.css` `:is(...)` selector into invalid
> fragments, and the regex model does not give `:is()` the specificity of its most
> specific argument. The result was a reported "winner" that **contradicted the
> measured computed value**. The model was rewritten with a nesting-aware splitter
> and correct `:is()`/`:not()`/`:has()`/`:where()` handling; only then did the
> reported owner reproduce the computed value exactly. **A reported owner that
> disagrees with the computed value is a broken oracle, not a finding.**

### 2. Pixel differential, frame-scoped

The **full-page** pixel oracle is unusable here, and this was proven rather than
assumed. A same-CSS control produced non-zero diffs at **10 of 14** widths,
localized to `y ∈ [18, 40]` — the animated navbar strip, the known WP4.0
animated-logo drift:

| width | control diff (full page) | bounding box |
|---|---:|---|
| 1200 / 1201 / 1280 / 1281 | 0 | — |
| 1366 | 76 | `[35,18,44,32]` |
| 1920 | 456 | `[35,18,1146,40]` |
| 2561 | 348 | `[35,20,1146,40]` |

The oracle was therefore scoped to the `.workout-log-frame` element, which is
where every authorized deletion's claim lives and which excludes animated navbar
chrome entirely.

---

## Same-CSS control

| Comparison | Computed/winner records | Frame pixels |
|---|---|---|
| `before-A` vs `before-B` | **0 differing / 504** | **14/14 zero-diff** |
| `after-A` vs `after-C` | 0 differing / 504 | 14/14 zero-diff |
| `after-C` vs `after-D` | 0 differing / 504 | 14/14 zero-diff |
| `final-1` vs `final-2` | **0 differing / 504** | **14/14 zero-diff** |

**One characterized flake, disclosed.** Of six after-state runs, `after-B` alone
differed, at two widths (`w1920` 25,350 px over the whole frame; `w2560` 231 px).
Its **computed values were identical** to every other run, and side-by-side
inspection shows a ~1px text-baseline shift, i.e. layout rounding jitter, not a
cascade change. Five runs — `before-A`, `before-B`, `after-A`, `after-C`,
`after-D` — plus both `final` runs are mutually byte-identical in the frame. An
earlier round also showed a one-off thumbnail-decode drift, which was eliminated
by adding an explicit image-decode and font-ready barrier to the harness.

---

## Result: before vs after

| Comparison | Computed/winner records | Frame pixels |
|---|---|---|
| `before-A` vs `after-A` | **0 differing / 504** | **14/14 zero-diff** |
| `before-A` vs `after-C` | 0 differing / 504 | 14/14 zero-diff |
| `before-A` vs `final-1` | **0 differing / 504** | **14/14 zero-diff** |
| `before-B` vs `final-2` | 0 differing / 504 | 14/14 zero-diff |

**Not one computed value, and not one declaration owner, changed at any of the
14 widths.**

### Deadness proof

Across the 14 widths, the before-state walk examined **385 declaration-instances**
belonging to the deletion scope (every media-gated candidate plus the base frame
padding). **Zero of them were ever the winning owner.**

| Family | Instances | Times winner |
|---|---:|---:|
| Frame-adjustment block — 8 responsive `.workout-log-frame` paddings | 56 | **0** |
| Frame-adjustment block — 7 `.workout-log-frame … thead th` pairs | 65 | **0** |
| First ladder — `.workout-log-table thead th` | 82 | **0** |
| First ladder — `.workout-log-table td` | 70 | **0** |
| Base `.workout-log-frame` padding | 112 | **0** |
| **Total** | **385** | **0** |

(Counts differ per family because each is sampled only at the widths its media
condition matches, and because `thead th` carries `letter-spacing` while `td`
does not.)

### Measured invariants

Measured, not assumed — identical before and after at **all 14 widths**:

| Property | Computed value | Winning owner |
|---|---|---|
| `th`/`td` padding | `12px 16px` | `components.css` `:is()` cell rule, spec `(1,3,1)`, important |
| `th`/`td` `font-size` | `14.08px` | same |
| `th`/`td` `letter-spacing` | `normal` (from `0px`) | same |
| `.workout-log-frame` padding | `0px` | `html body .workout-log-frame`, spec `(0,1,2)`, important |

This independently reproduces the WP4.3j-b conclusion, including the ID-bearing
`:is()` specificity trap: the shared selector's most specific argument
(`#workout[data-page="workout-plan"]`) exports ID-level specificity to the
`.workout-log-page` branch that actually matches.

---

## Deltas

| Metric | Before | After | Δ |
|---|---:|---:|---:|
| Lines (`pages-workout-log.css`) | 2,180 | 2,025 | **−155** |
| `@media` queries | 17 | 9 | **−8** |
| `!important` declarations | 285 | 285 | **0** |
| Stylelint — focused | 717 | 717 | **0** |
| Stylelint — total (`static/css/*.css` + `scss/**/*.scss`) | 5,784 | 5,784 | **0** |
| Stylelint categories increased | — | — | **NONE** |

**The Stylelint delta is honestly zero.** None of the deleted declarations was an
`!important`, a colour literal, an ID selector, or a duplicate, so none of them
triggered a rule in this configuration. The win here is 155 lines of CSS that
could never render, not a lint score.

> Counting note: `grep -c '!important'` reports *lines*, not occurrences, and the
> file contains prose mentions of the keyword. The 285 figure is occurrences in
> the comment-stripped body, and is what the contract asserts.

---

## Gates

| Gate | Result |
|---|---|
| Focused Workout Log visuals (6 win32 variants, `PW_VISUAL_SEED=1`) | **6 passed**, update-free |
| CSS cascade + visual selector contracts | **31 passed** (30 + 1 new) |
| Focused functional Chromium (`workout-log`, `smoke-navigation`) | **33 passed** |
| Full pytest | **1,857 passed / 1 skipped** |
| Stylelint before/after | no category increased |

Baseline at branch point `ff9fe4b` was **1,856 passed / 1 skipped**; the +1 is the
new contract test. `git status -- e2e/__screenshots__` is empty — **no visual
baseline was updated**. No generated file, database, snapshot, SCSS, template, or
JavaScript appears in the diff.

### Contract

`test_workout_log_drops_inert_responsive_table_and_frame_families` in
`tests/test_css_cascade_contracts.py` pins both halves, which is the point:

1. the three deleted families are absent;
2. the shared `components.css` owner that beat them is unchanged;
3. **every explicitly out-of-scope family is still present** — the 992px overflow
   rule, page padding, delete-button and icon sizing, routine-cell width and
   typography, and the late legend query;
4. the five retained shells are still there;
5. the `!important` count did not move.

Its red path was proven: run against the pre-deletion bundle, it fails.

Two assertions needed anchoring rather than substring matching, because the
deleted selectors also appear as **live comma arms** of base grouped rules
(`.workout-log-frame .workout-log-table thead th,` and
`table.workout-log-table thead th {`). The contract matches on the `{` terminator
and the media-query indent so it can never pass by deleting a live grouped arm.

---

## Findings recorded, not acted on

1. **The WP4.4 shared-selector finding stands and was not touched.** The
   `components.css` `:is()` arm exports ID-level specificity to four route
   branches, which is why page-local table-cell overrides on this page are
   effectively impossible. Repairing it is cross-page work.
2. **The five retained empty media shells** are a deliberate scope choice, not an
   oversight. Collapsing them belongs to a structural packet.
3. **The families the j-b audit never measured remain unclassified** — they were
   retained on that basis, not because they were proven live.
4. **The full-page pixel oracle remains unusable on this route** until the
   animated navbar logo is stabilized. Any future Workout Log pixel claim should
   scope to the element under test.
