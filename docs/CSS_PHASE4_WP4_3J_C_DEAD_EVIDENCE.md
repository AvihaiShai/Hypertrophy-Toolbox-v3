# WP4.3j-c-dead — deleting the 37 cascade-dead header / table-cell glass rules

**Branch:** `wt/wp4-3j-c-dead` · **Base:** merged `origin/main` @ `69dcf5e`
**Production diff:** `static/css/pages-workout-log.css` (+18 / −422) and one new
contract in `tests/test_css_cascade_contracts.py` · **Outcome:** deletion shipped

---

## What this packet is

The deletion packet that [`CSS_PHASE4_WP4_3J_C_AUDIT_EVIDENCE.md`](CSS_PHASE4_WP4_3J_C_AUDIT_EVIDENCE.md)
documented but explicitly did not authorize. It removes the 37 rules that audit
nominated — regions **D** (dark cell glass), **E** (positional metric-lane
glass), **F** (comprehensive dark-mode visibility) and six of the eight rules in
region **G** (final override) — from `static/css/pages-workout-log.css`.

**The audit was treated as a nomination, not as inherited proof.** The branch
was cut fresh from merged `main` at `69dcf5e`, not continued from the pre-squash
`wt/wp4-3j-c-audit` history, and every ownership and pixel claim was
re-established from scratch before a byte was deleted. That re-verification
found two new oracle defects, both of which produced confident wrong answers
(§ Oracle defects).

| | Before | After | Δ |
|---|---:|---:|---:|
| Lines | 2,025 | 1,621 | **−404** |
| Rules in the four regions | 37 | 0 | **−37** |
| Declarations | 69 | 0 | **−69** |
| `!important` (comment-stripped) | 285 | 217 | **−68** |
| `@media` blocks | 9 | 9 | 0 |

---

## Why these rules could not render

Unchanged from the audit, and independently reproduced here: the Workout Log
table is painted by the shared `components.css` `.table.table-calm` system, not
by the page's own glass systems. The shared selector carries an ID arm:

```css
:is(#workout[data-page="workout-plan"],      /* ← (1,1,0): most specific arm */
    .workout-log-page,                       /* ← the arm that actually matches */
    .summary-frame.frame-calm-glass,
    .progression-plan-container) .table.table-calm > :not(caption) > * > * { … !important }
```

`:is()` takes the specificity of its most specific argument even when a less
specific argument matches, so the shared rule is `(1,3,1)`/`(1,3,2)` and
important. Every deleted rule is ID-free — `(0,1,1)` to `(0,4,3)` — so no amount
of `!important` reaches it. The one page-local family that *does* render is
region H at `(1,5,2)`, which is retained byte-for-byte.

---

## Structural resolution of the scope

Line numbers were not trusted. Each region was resolved from the file by
selector shape and declared properties, then cross-checked against its expected
rule count (`artifacts/wp43jcdead/extract-targets.mjs`):

| Region | Rules | Declarations | `!important` | Resolved by |
|---|---:|---:|---:|---|
| D dark cell glass | 3 | 9 | 8 | every arm dark-theme, ends at `td`, no positional filter |
| E positional lane glass | 20 | 30 | 30 | `:nth-child(5…14)` filter, declares only `background`/`box-shadow` |
| F dark-mode visibility | 8 | 8 | 8 | single `color: #e0e0e0` declaration on `td`/`th` |
| G final override (non-hover) | 6 | 22 | 22 | **every** arm targets `.tbl`/`.tbl--responsive`, not `.workout-log-table` |
| **Total** | **37** | **69** | **68** | |

The region-G shape test is what separates it from the region-A/C base blocks
(whose first arms are `.workout-log-table …`) and from region H
(`table.workout-log-table …`). A first attempt keyed on a line range swept up 26
rules including region H; the shape test returns exactly 6.

The resolved spans, the two retained hover rules, and an overlap guard are
asserted before deletion; the deleter refuses to write on any failed assertion.

### Correction to the audit's `!important` projection

The audit projected **71** removed `!important` and `285 → 214`. The measured
figure is **68** and `285 → 217`. The audit's region-F count of 11 was taken over
the line span 1366–1439, which also covers the retained `.editable-input` (2) and
`.badge` (1) rules; the eight region-F rules themselves carry 8. D (8), E (30)
and G (22) match the audit exactly.

### Correction to the audit's "unverified" location

The audit records nine unverified declarations as "all in region H". Eight are
(the dark planned/scored lane-header properties at old L1781/L1790); the ninth is
the base header `text-transform` at old L208, in region A. Both regions are
retained in full, so nothing about the scope changes.

---

## Re-establishing the evidence, before deletion

`artifacts/wp43jcdead/nominate-check.mjs`, run against the **pre-deletion**
bundle across all six contexts:

| Check | Result |
|---|---|
| Each nominated rule resolves to exactly one CSSOM rule | **37/37, in all 6 contexts** |
| Rules that match no element (dead by selector, a different claim) | **0** |
| Rules that ever win any of the audited records | **0** |
| Retained region-G hover rules own `filter` | **L1527 51 records, L1538 51 records** |

Every one of the 37 genuinely matches live elements and genuinely loses. The
losers' opponents were recorded: regions D/F/G lose to `components.css` at
`(1,3,1)`–`(1,5,3)`, and the dark region-E header rules lose to the region-H
lane family at `(1,6,2)`.

---

## Before / after differential

`artifacts/wp43jcdead/diff-audit.mjs` was run on both sides — same harness, same
36 properties, same 71 targets (17 columns × {`th`, `td-odd`, `td-odd-hover`,
`td-even`} + frame + frame-hover + table) — and compared by
`artifacts/wp43jcdead/compare.mjs`.

| Claim | Result |
|---|---|
| Records compared | **15,336** (2,556 × 6 contexts) |
| Computed-value differences | **0** |
| Declaration-owner differences | **0** |
| Frame pixel differential, `.workout-log-frame` | **6/6 zero-diff — byte-identical PNGs** |
| Same-CSS control, two independent loads per context | **0 differing pixels, 6/6, on both sides** |
| Resolution self-check (reapplying the winner reproduces the computed value) | **9,358 checks, 0 mismatches, on both sides** |
| Sentinel probes verified effective | **38/38 per context, both sides (456 total)** |
| Zero-diffs not explained by the target being out of frame | **0** |
| Sentinels fully reverted | **6/6 clean, both sides** |
| `#workout-log-table` classes at runtime | `table table-calm table-striped tbl tbl--responsive workout-log-table`, both sides |

The owner identity compared is the declaration — `href`, `selectorText`,
`propKey`, matched arm, specificity, importance, media, layer, value and
`viaProp`. The rule's `order` index is deliberately excluded and compared
separately, because deleting 37 rules shifts the index of every rule after them;
comparing it would report 15,336 spurious differences.

### Two positive controls that the deletion actually happened

A differential of zero is only meaningful if the change reached the browser.

1. **Matching-rule count fell by exactly 37 in every context** — 2,196 → 2,159
   (desktop), 2,052 → 2,015 (tablet), 1,950 → 1,913 (mobile).
2. **5,496 records lost candidates and 0 gained any.** Those are the records
   where a deleted rule had been in the candidate set and lost. The deleted
   rules were demonstrably participating in the cascade and demonstrably never
   winning it.

---

## Oracle defects found in this packet

The j-c audit's rule — *a probe that changes nothing proves nothing* — held.
This packet adds a second one, because both defects below were caught by the
same control.

1. **`Array.from(rule.style)` enumerates expanded longhands, not authored
   property names.** An authored `background: …` appears in `propKey` as
   `background-image|background-position|…`. Identifying a source rule by
   comparing its authored property list against `propKey` therefore matched
   nothing for every rule that declares a shorthand — **29 of the 37** reported
   "this rule matches no element", which reads as *even deader* than the claim
   being tested and would have been quietly welcome.
2. **Chrome re-serializes `:nth-child(even)` as `:nth-child(2n)`** (and `odd` as
   `2n+1`). A matcher comparing authored selector text to CSSOM selector text
   without normalizing this reported "matches no element" for exactly the **13**
   even-row rules among the 37.

Both defects are invisible to the question the packet is actually asking. "Does
this rule ever win?" answered **0** under both the broken and the fixed matcher,
so a run that only checked for wins would have shipped with a matcher that
matched nothing at all.

> **General rule this packet adds:** *every deadness sweep must carry a
> known-live control.* The two retained region-G hover rules are known to own
> `filter`. Under the broken matcher they reported **0 wins** — the same answer
> as the 37 rules under test. That contradiction, not the deadness result, is
> what exposed both defects. If the oracle cannot see a declaration you already
> know wins, its silence about the ones you think are dead means nothing.

Carried forward unchanged from j-b-dead and j-c: the full-page pixel oracle is
unusable on this route (a same-CSS control drifts inside the animated navbar
strip), sentinels must be applied **inline** `!important` and asserted to have
moved the computed value, a 400 ms settle is required because a running
transition outranks important author declarations, and the capture must be
scrolled into the viewport with the tested elements proven inside it and inside
their scroll ancestors.

---

## What was deliberately retained

- **The two region-G hover rules** (old L1527 light, L1538 dark). Their
  `background` and `box-shadow` are dead, but their
  `filter: saturate(…) brightness(…)` is the winning owner of `filter` on
  hovered cells — 51 records each. They are **not** partially cleaned in this
  packet; that is a separate decision.
- **Regions A, B, C, H and I** in full, including the region-H `(1,5,2)`
  metric-lane system, which is locked byte-for-byte by a checksum in the
  contract. A third `filter: saturate(…)` remains in the file: the region-C
  light hover rule, a documented loser that is out of scope.
- The transparent 1 px header top border, the nine unverified declarations, the
  five empty media shells and every other retained responsive family, the 992 px
  overflow rule, and the late legend query.
- Modal / editable-input / badge styling, and `nth-child` structural
  replacement.
- `components.css`, `theme-dark.css`, SCSS, generated Bootstrap, templates,
  JavaScript, snapshots, databases, and every WP4.4 concern.

---

## The premise this deletion rests on

The deadness of regions A–G is **conditional on `#workout-log-table` keeping its
`table` and `table-calm` classes** — that is what lets the shared rule match. The
contract now protects that premise directly: it asserts the classes on
`templates/workout_log.html`, and that no JavaScript removes or toggles them.
Neither file was modified; the tests only read them. The live sweep also
confirmed both classes present at runtime in all six contexts, before and after.

---

## Cascade contract

`test_workout_log_drops_cascade_dead_header_and_cell_glass` asserts, in eight
clauses: all 37 rules absent (by a selector arm unique to each, plus the lane
colour literals and the block banner); the shared `components.css` owners
unchanged, including the `(1,4,2)` dark-cell rule the region-F declarations lost
to; both hover rules and their exact winning filters present; region H
byte-for-byte by sha256; the nine unverified declarations present;
`#workout-log-table` retaining `table table-calm` with no JS mutation; the five
empty media shells, the 992 px overflow rule, the legend query and the retained
editable-input/badge neighbours present; and `!important` at 217.

The `!important` clause in the shipped j-b-dead contract asserted 285. That
packet's deletions carried no `!important`, so the number was correct then; it
is updated to 217 here with the reason recorded in place, and ownership of the
figure moved to the new test.

**Red path**, proven against the pre-deletion bundle and by targeted mutation:

| Mutation | Result |
|---|---|
| Whole pre-deletion `pages-workout-log.css` restored | **RED** |
| Remove the light hover `filter` (a live winner) | **RED** |
| Mutate one byte inside region H | **RED** |
| Resurrect one deleted region-E rule | **RED** |
| Drop `table-calm` from the log table template | **RED** |

---

## Gates

| Gate | Result |
|---|---|
| Workout Log visuals, `PW_VISUAL_SEED=1` | **6/6 update-free**, no baseline written |
| Cascade + visual-selector contracts | **32/32** (29 + 3), red path proven |
| Focused functional Chromium (`workout-log`, `smoke-navigation`) | **33/33** |
| Full pytest | **1,858 passed / 1 skipped** (baseline 1,857 + this contract) |
| Stylelint, no category increased | **confirmed** |

### Stylelint

| Scope | Before | After | Δ |
|---|---:|---:|---:|
| Total warnings | 5,784 | 5,498 | **−286** |
| Focused (`pages-workout-log.css`) | 717 | 431 | **−286** |
| `declaration-no-important` (focused) | 285 | 217 | −68 |
| `declaration-property-value-disallowed-list` (focused) | 222 | 166 | −56 |
| `no-descending-specificity` (focused) | 200 | 38 | **−162** |

The entire total-warning reduction comes from the target file. Unlike
j-b-dead — where the deleted declarations triggered no rule and Stylelint moved
by zero — this is the largest single-file movement of the Phase 4 arc, and
`no-descending-specificity` falling 200 → 38 is the biggest category move so
far: the deleted rules were the ones being out-ordered by the shared bundle.

`git status -- e2e/__screenshots__` is empty. No `components.css`,
`theme-dark.css`, SCSS, generated Bootstrap, template, JavaScript, snapshot or
database file appears in the production diff.

---

## Sequencing note

This deletion had to precede WP4.4. A WP4.4 repair of the shared `:is()`
selector — removing the ID arm so it stops exporting `(1,3,x)` to the
`.workout-log-page` branch — would **resurrect** these 37 rules, and with them
four generations of conflicting table paint. They are now gone, so that repair
can be evaluated on its own merits.

## Out of scope, and untouched

WP4.4 and the shared bundles; the remaining Workout Log raw-literal → token
extraction; the two region-G hover rules' dead `background`/`box-shadow`;
`nth-child` structural replacement; modal and editable-input redesign; the ten
WP4.3i deferred interaction-state declarations; visual baselines.
