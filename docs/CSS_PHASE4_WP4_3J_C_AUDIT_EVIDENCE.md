# WP4.3j-c — Workout Log header / table-cell glass ownership audit

**Branch:** `wt/wp4-3j-c-audit` · **Base:** merged `origin/main` @ `9a3f205`
**Production diff:** none · **Outcome:** evidence-only packet

---

## What this packet is

An audit of the overlapping header and table-cell glass systems in
`static/css/pages-workout-log.css`. It classifies every relevant declaration
across all 17 columns, in light and dark, at desktop, tablet and mobile widths.
**No production CSS was modified**, and the packet does not authorize any
deletion. The branch was cut fresh from merged `main` at `9a3f205`, not
continued from the pre-squash `wt/wp4-3j-b-dead` history.

Regions audited, all in `pages-workout-log.css` unless noted:

| ID | Region | Lines |
|---|---|---|
| A | Base light header block | 207–240 |
| B | Dark-mode header counterpart | 241–261 |
| C | Base light cell block (+ even / hover) | 262–304 |
| D | Dark-mode cell counterpart (+ even / hover) | 361–392 |
| E | Column colour pairing / metric-lane glass | 393–645 |
| F | Comprehensive dark-mode visibility block | 1366–1440 |
| G | Final override block | 1441–1548 |
| H | Explicit metric-lane pairing / table-calm compat | 1549–1830 |
| I | Late frame / table glass block | 1946–2002 |
| — | Shared `components.css` `.table.table-calm` owner (**read only, never modified**) | 3335–3411, 4433 |

---

## Headline

**The Workout Log table is painted by the shared `components.css`
`.table.table-calm` system, not by the page's own glass systems.** Of the 322
distinct source declarations audited across regions A–I, **227 never win
anywhere** — and the losses are not marginal. Nearly every page-local table rule
is `!important` yet still loses, because the shared selector carries an ID:

```css
:is(#workout[data-page="workout-plan"],      /* ← (1,1,0): most specific arm */
    .workout-log-page,                       /* ← the arm that actually matches */
    .summary-frame.frame-calm-glass,
    .progression-plan-container) .table.table-calm > :not(caption) > * > * { … !important }
```

`:is()` takes the specificity of its **most specific argument**, even when a
less specific argument is the one that matches. The shared cell rule is
therefore `(1,3,1)` and the header/body rules `(1,3,2)`, all `!important`. Every
page-local rule in regions A–G is ID-free — `(0,1,1)` to `(0,4,3)` — so no
amount of added `!important` or extra class chaining can reach it.

**The single exception is the one family that does carry an ID.** The region-H
`table-calm` compatibility rules are written
`.workout-log-page #workout-log-table.table.table-calm …` = **`(1,5,2)`**, which
out-specifies the shared owner. Those are the rules that put the metric-lane
tints on screen. The comment above them at line 1728 says exactly this, and it
is the only place in the file where the problem was diagnosed and solved rather
than answered with more `!important`.

This reframes the page: **`pages-workout-log.css` is not the owner of its own
table.** Regions A–G are a historical stack of four successive attempts to
restyle cells that had already lost the cascade.

---

## Method

### Oracle 1 — nesting-aware CSSOM ownership

For each target element and each of 36 properties, every rule in every
same-origin stylesheet was enumerated (recursing into `@media`/`@supports`/
`@layer`, skipping media conditions that do not currently match), the
best-matching selector arm was found, and candidates were ranked by importance,
specificity and source order. The WP4.3j-b-dead rule was honoured: **no naive
comma splitting and no regex specificity model.** The splitter respects `()`,
`[]` and quoting; the specificity model gives `:is()`/`:not()`/`:has()` the
specificity of their most specific argument, `:where()` zero, and handles
`:nth-child(An+B of S)` and pseudo-elements.

The model was unit-checked against hand-computed specificities before use,
including the shared `:is()` selector `(1,3,1)`, the `(1,5,2)` lane rule, and
`:where(.x) .y` = `(0,1,0)`.

### Oracle 2 — frame-scoped pixel contribution

To separate "wins the cascade" from "reaches the screen", each property was
overwritten on the live elements with a garish sentinel and the frame was
re-photographed. A zero diff means the winning value contributes no pixels.

The full-page oracle remains unusable on this route (j-b-dead: a same-CSS
control drifts inside the animated navbar strip), so every capture is scoped to
`.workout-log-frame`.

### Self-checks that gate every claim

| Check | Result |
|---|---|
| Same-CSS pixel control, two independent page loads per context | **0 differing pixels, 6/6 contexts** |
| Resolution self-check — reapplying the reported winner reproduces the computed value | **9,358 checks, 0 mismatches** |
| Sentinel took effect (computed value actually moved) | **222 / 222** |
| Sentinel zero-diffs not explained by the target being outside the capture | **0 unexplained** |
| Sentinels fully reverted afterwards | **6/6 clean** |

Ownership records: **15,336** (2,556 per context), against 2,196 / 2,052 / 1,950
matching rules at desktop / tablet / mobile.

### Four oracle defects found and fixed — all of which would have invented dead CSS

These cost most of the packet's time and are the most reusable part of it. Each
one produced a *confident, wrong* answer before it was caught.

1. **A `var()`-bearing shorthand is invisible to longhand queries.** CSSOM
   cannot expand `padding: var(--wp-table-cell-padding, 0.75rem 1rem)` into
   longhands — it is stored as a pending-substitution value, and
   `getPropertyValue('padding-top')` returns `''`. Querying longhands alone
   therefore hid **exactly the shared `components.css` owners that win**, and
   the audit reported page-local declarations as winners while the measured
   computed value disagreed. 338 resolution mismatches. Fixed by falling back
   from each longhand to its shorthands; mismatches went to **0**.
2. **A stylesheet sentinel has to win the cascade, and often did not.** An
   injected `#workout-log-table tbody td.metric-lane { … !important }` is
   `(1,1,2)` and loses to the page's own `(1,5,2)` lane rules. It changed
   nothing, produced a zero pixel diff, and that reads as "this value never
   renders". Fixed by applying sentinels as **inline** `!important`, which
   outranks every author rule, and by asserting the computed value moved.
3. **A running CSS transition outranks even important author declarations.**
   `components.css` puts an important 150ms transition on these cells, which the
   injected `*` stabilizer `(0,0,0)` cannot outrank, so reading the computed
   value immediately after applying a sentinel returned the *pre*-transition
   value — again indistinguishable from a failed sentinel. Fixed with a 400ms
   settle before every read and capture.
4. **`page.screenshot` does not paint clip regions beyond the viewport.** At
   mobile the frame starts at y≈649 and is ~8,000px tall; a naive frame-top clip
   returned a near-blank 3.5KB image, and **every sentinel on it read as a zero
   diff**. Fixed by scrolling the frame top to the viewport top and bounding the
   capture by the viewport, plus recording whether the sentinel's elements were
   actually inside the captured region and inside their scrollable ancestors.

Two smaller harness traps, recorded because they cost real time: `img.decode()`
on a `loading="lazy"` image that has never been fetched **never settles** (at
mobile the stacked table pushes most thumbnails below the fold, which hung the
run — the barrier now covers `complete` images only and is bounded); and Node
block-buffers a piped stdout, which makes a long run look hung.

> **General rule this packet adds:** *a probe that changes nothing proves
> nothing.* Every negative pixel result must carry positive evidence that the
> probe itself worked — the value moved, and the thing it moved was in frame.

---

## Results

### Declaration inventory by region

Counted as distinct source declarations (file, line, property). "Mixed" means
live in some context/role and dead in others — most commonly a light-mode
declaration that loses to its own dark-mode counterpart.

| Region | Total | Cascade-dead | Live winner | Mixed | Unverified | Overpainted |
|---|---:|---:|---:|---:|---:|---:|
| A base light header (208) | 28 | **17** | 6 | 4 | 1 | 0 |
| B dark header (242) | 12 | **10** | 2 | 0 | 0 | 0 |
| C base light cell (263/287/295) | 28 | **24** | 2 | 2 | 0 | 0 |
| D dark cell (362/375/383) | 16 | **16** | 0 | 0 | 0 | 0 |
| E metric-lane glass (401–643) | 70 | **70** | 0 | 0 | 0 | 0 |
| F dark visibility block (1371–1438) | 8 | **8** | 0 | 0 | 0 | 0 |
| G final override (1447–1547) | 58 | **56** | 1 | 1 | 0 | 0 |
| H lane pairing / table-calm (1553–1829) | 81 | 21 | 18 | 34 | 8 | 0 |
| I late frame / table glass (1947–2001) | 21 | 5 | 2 | 14 | 0 | 0 |
| **Total A–I** | **322** | **227** | **31** | **55** | **9** | **0** |

**Regions D, E and F are dead in their entirety** — every declaration, every
column, every role, both themes, all three widths.

### No declaration is "winning but visually overpainted"

The category is **empty** in this scope, and that is a measured result rather
than an unexamined one: all 37 sentinel probes moved real pixels in every
context where their targets were in frame (e.g. `tbody td background-color`
464,416 px; `thead th box-shadow` 18,454 px; `td.metric-lane background-color`
263,544 px).

This does **not** contradict WP4.3j-a. That packet's overpaint arose from a
page-local `background-color` sitting under a page-local opaque `background`
gradient *on the same element*; those five declarations are already deleted, and
`components.css` now owns the background outright, so the configuration no
longer exists here.

### Complementary declarations

Twelve declarations win only because nobody else sets that exact longhand, while
a sibling longhand of the same shorthand is owned elsewhere. They are live but
inert in isolation:

- **`border-top-width` / `border-top-style` at L208 (light) and L242 (dark)** —
  both win, but `border-top-color` is owned by `components.css`
  `border-color: transparent !important` `(1,3,1)`. The header therefore reserves
  a 1px top border that is **always transparent**: it occupies layout space and
  paints nothing. Deleting the colour alone would change nothing; deleting the
  width would shift layout by 1px.
- **`background-clip` at L1731 / L1740 / L1749 / L1756 (light) and L1781 / L1790 /
  L1799 / L1806 (dark)** — live, but the `background-image` beside it is owned by
  `components.css`, so the clip applies to a background the page does not own.

### Per-column result — the split is 2-way, not 17-way

Across all 17 columns the ownership pattern collapses into exactly two groups,
identical in light and dark:

| Property | Columns 1–4, 15–17 | Columns 5–14 (metric lanes) |
|---|---|---|
| `background-color` / `background-image` | `components.css` `(1,3,2)` | `pages-workout-log.css` `(1,5,2)` |
| `border-bottom-color` | `components.css` `(1,3,2)` | `(1,5,2)` on `th`, `components.css` on `td` |
| `color` | `components.css` | `(1,5,2)` on `th`, `components.css` on `td` |
| `box-shadow`, `padding`, `font-size`, `letter-spacing`, `border-top-color`, `text-shadow`, `font-weight` | `components.css` `(1,3,1)` / `(1,3,2)` | identical |

**No individual column deviates from its group.** The per-column `nth-child`
rules in region E, which exist precisely to differentiate columns 5–14, are
entirely dead; the live per-column differentiation comes from the class-based
region-H system instead. The `metric-lane` classes on the cells are what
actually drive column colour, so this result does not depend on column order —
a useful qualifier on the WP4.3j-a finding that "196 `nth-child` rules make
every column rule positional."

### Measured invariants (identical at all three widths, both themes)

| Property | Computed | Winning owner |
|---|---|---|
| `th`/`td` padding | `12px 16px` | `components.css` `(1,3,1)` important |
| `th`/`td` `font-size` | `14.08px` | same |
| `th`/`td` `letter-spacing` | `normal` | same |
| `th`/`td` `border-top-color` | `rgba(0, 0, 0, 0)` | same (`border-color: transparent`) |
| `th`/`td` `box-shadow` | `none` | same (`box-shadow: none`) |
| dark `td` `color` | `rgb(238, 241, 246)` | `components.css` `(1,4,2)` important |

This independently reproduces the j-b / j-b-dead padding and type findings from
a fresh harness.

---

## Correction to previously shipped evidence

`CSS_PHASE4_WP4_3J_A_EVIDENCE.md` records, about the dark-mode visibility block
(region F):

> "**The `color` declarations are live winners, not dead.** They set `#e0e0e0`
> at specificity (0,3,1), beating the earlier dark-glass rule's
> `rgba(255, 255, 255, 0.9)` at (0,2,1)."

**That is not what renders.** The comparison was made only against the
page-local dark-glass rule and never against the shared bundle. All eight
`color: #e0e0e0 !important` declarations in region F are **cascade-dead**: the
computed dark cell colour is `rgb(238, 241, 246)`, owned by `components.css`
`color: var(--ink-1, #eef1f6) !important` at `(1,4,2)`. Verified on all 17
columns, both `th` and `td`, at all three widths, with the reported owner
reproducing the computed value exactly.

The j-a *packet* is unaffected — it deleted `background-color` declarations, not
these — but the recorded reason for retaining region F does not hold. This is a
worked example of the same mistake the `:is()` trap caused in j-b: **ranking a
page-local declaration against its page-local neighbours instead of against
every loaded stylesheet.**

---

## Deletion candidate — documented, NOT implemented

A coherent candidate exists. **It is not authorized by this audit and must not
be started without new owner approval.**

### Exact scope

| Region | Rules | Lines | `!important` | Selector family |
|---|---:|---:|---:|---|
| D | 3 | 31 (361–391) | 8 | `[data-theme='dark'] .workout-log-table td` base / even / hover |
| E | 20 | 251 (393–643) | 30 | `.workout-log-table thead th:nth-child(N)` + `td:nth-child(N)` lane colours, light and dark |
| F | 8 | 74 (1366–1439) | 11 | `[data-theme='dark'] .workout-log-table` `td`/`th` `color: #e0e0e0` |
| G (6 of 8 rules) | 6 | 80 (1446–1525) | 22 | `.tbl…`/`.tbl--responsive…` header, cell, dark and even-row overrides |
| **Total** | **37** | **436** | **71** | |

**Properties:** every declaration in those rules. All are proven dead in all six
contexts, all 17 columns and all four cell roles.

**Explicitly retained inside region G:** the two hover rules at **L1527** and
**L1538**. Their background and box-shadow declarations are dead, but their
`filter: saturate(…) brightness(…)` is the **winning owner** of `filter` on
hovered cells — L1527 in light, L1538 in dark. Three other rules propose a hover
`filter` (L295, L383, L680) and all three lose. A deletion packet must keep the
`filter` declarations or prove them inert separately.

### Oracle a deletion packet would need

1. **Before/after computed-value + declaration-owner differential** over all
   15,336 records, expecting **0 differing records**.
2. **Frame-scoped pixel differential** at all six contexts, expecting
   **6/6 zero-diff**, preceded by a same-CSS control that reaches zero.
3. **Same-CSS control** on both sides — the j-dead rule; a sweep alone
   over-reports.
4. **Positive-control evidence** for every negative result, per the rule this
   packet adds.

### Proposed gates

- New cascade contract asserting the 37 rules are absent, that the
  `components.css` owners that beat them are unchanged, that `filter` survives at
  L1527/L1538, and that the region-H `(1,5,2)` lane family is untouched.
- Red path proven against the pre-deletion bundle.
- Workout Log visuals **6/6 update-free** with `PW_VISUAL_SEED=1`.
- Focused functional Chromium (`workout-log`, `smoke-navigation`).
- Full pytest.
- Stylelint before/after with no category increased. Expected movement is real
  here, unlike j-b-dead: **71 `!important` (285 → 214)** plus the colour literals
  in region E.

### Risk to state in that packet

The deadness of regions A–G is **conditional on `#workout-log-table` keeping its
`table` and `table-calm` classes**, which is what lets the shared
`components.css` rule match. Those classes are hardcoded in
`templates/workout_log.html:66` and no JavaScript mutates them — the only
runtime class changes are `tbl--view-simple` / `tbl--view-advanced` in
`static/js/table-responsiveness.js:335-339`, which hide Workout Plan columns
(`Movement Pattern`, `Stabilizers`, `Synergists`, `Tertiary Muscle`, `Utility`,
`Movement Subpattern`) and no Workout Log column. If `table-calm` were ever
removed from the log table, the deleted rules would have been the fallback.

---

## Findings recorded, not acted on

1. **The WP4.4 shared-selector finding is now quantified.** The ID-bearing
   `:is()` arm is not merely awkward — it is why four successive generations of
   page-local table styling in this file are dead. Any WP4.4 repair of that
   selector would **resurrect** regions A–G unless they are deleted first, which
   is an argument for sequencing the deletion packet *before* WP4.4, not after.
2. **Region H is the only correct pattern in the file** and should be the model
   for any future page-local table styling: match the shared owner's ID-level
   specificity deliberately, with a comment explaining why.
3. **The transparent 1px header top border** (`border-top-width`/`-style` live,
   `border-top-color` forced transparent by the shared bundle) is a latent
   layout-only artifact. Left alone.
4. **Region I is mostly `MIXED`**, driven by `theme-dark.css:88`
   `:where([data-theme="dark"] .workout-log-frame)` — specificity `(0,0,0)` but
   `!important` and loaded after the page bundle, so it takes the frame's
   background, border and box-shadow in dark mode while region I keeps them in
   light. Not a defect; recorded because it is easy to misread as duplication.
5. **Nine declarations remain `unverified`**, all in region H, all because their
   target cells are outside the captured region at mobile width where the table
   becomes an `overflow-x` scroll container. They are **not** classified as dead.

---

## Explicitly out of scope, and untouched

CSS deletion and tokenization; `components.css` and WP4.4; the five retained
empty media shells; the `992px` overflow rule and the other retained responsive
families; `nth-child` restructuring; modal and editable-input styling and
redesign; templates, JavaScript, SCSS, generated Bootstrap, databases, and
visual baselines.

`git status -- e2e/__screenshots__` is empty. The diff for this packet is
documentation only.
