# WP4.3i-dead — Workout Plan overridden rest-state declaration removal

Packet: WP4.3i-dead (Phase 4 CSS, page #9 Workout Plan)
Base: `main` @ `bfadf9d`, branch `wt/css-wp4-3i-dead`, isolated worktree
Date: 2026-07-25

## Scope

Deletion only, in `static/css/pages-workout-plan.css`. Removed 14 declarations that a browser
sweep proved never reach the rendered page. **0 insertions, 33 deletions.**

No tokenization. The Page Header section was not touched and the shipped WP4.3i-c contract was not
modified. No `!important` was edited in place, no selector rewritten, no declaration reordered, no
layer boundary moved, no duplicate-selector cleanup, no formatting churn.

## How liveness was established

### Stage 1 — sentinel sweep

Every ramp literal (`rgba(255,255,255,α)` / `rgba(0,0,0,α)` / `rgba(79,140,255,α)`) in the five
candidate sections was replaced with a **unique opaque `rgb()` sentinel** — 97 in total — and the
page was loaded with both themes and with `hover` / `focus` / `focus-visible` / `active` /
`disabled` forced via CDP on each candidate component. A sentinel that appears in any computed
style is live; one that never appears is overridden.

| Section | Live | Total |
|---|---|---|
| 829 Page Header | 15 | 15 |
| 934 Collapse Toggles | 0 | 2 |
| 1078 Filters | 0 | 1 |
| 1157 Inline Controls | 0 | 21 |
| 2275 Workout Plan Table | 42 | 58 |
| **Total** | **57** | **97** |

Coherence check: **zero declarations showed mixed liveness** across all 63 declarations — liveness
is a per-declaration property, exactly as the cascade requires.

### Stage 2 — computed-style differential, and why the scope shrank to 14

The sweep nominated 24 declarations. Before deleting them, a full computed-style differential was
run old-vs-new across every element (plus `::before` / `::after`) over the 37 longhands the deleted
shorthands can set — `background-*`, `border-*` including `border-image-*`, `box-shadow`, `color`,
`text-shadow`, `outline-*`, `opacity`, `visibility`, `backdrop-filter`, `filter`.

**A control run with identical CSS produced 52 differing records.** The interaction states on this
page animate, so forced-state snapshots are not a stable oracle and cannot certify anything. The
rest state, by contrast, is perfectly stable.

The 24 were therefore split by whether their rule carries an interaction pseudo-class:

- **14 rest-state declarations — shipped here**, certified by the rest-state differential.
- **10 interaction-state declarations — deferred**, because the only evidence available for them is
  the sweep, and the differential cannot corroborate it. They are left in place rather than deleted
  on weaker evidence.

### Stage 3 — certification of the 14

| Comparison | Records | Differ |
|---|---|---|
| Control (same CSS, two runs) | 31,074 | **0** |
| Old vs new (14 declarations deleted) | 31,074 | **0** |

Both themes, transitions and animations disabled, every element plus `::before`/`::after`. The
control proves the harness is stable; the old-vs-new run proves the deletion is inert.

## Declarations removed (14)

| Rule | Property | Literals | `!important` |
|---|---|---|---|
| `#workout[data-page="workout-plan"] .selection-actions` | `background` | 3 | no |
| `#workout[data-page="workout-plan"] .selection-actions` | `border` | 1 | no |
| `#workout[data-page="workout-plan"] .selection-actions` | `box-shadow` | 4 | no |
| `[data-theme='dark'] … .selection-actions` | `border` | 1 | no |
| `[data-theme='dark'] … .selection-actions` | `box-shadow` | 4 | no |
| `#workout[data-page="workout-plan"] .workout-plan-table thead th` | `background` | 3 | yes |
| `#workout[data-page="workout-plan"] .workout-plan-table thead th` | `border-bottom` | 1 | yes |
| `#workout[data-page="workout-plan"] .workout-plan-table thead th` | `border-top` | 1 | yes |
| `#workout[data-page="workout-plan"] .workout-plan-table thead th` | `box-shadow` | 3 | yes |
| `#workout[data-page="workout-plan"] .workout-plan-table thead th` | `text-shadow` | 1 | no |
| `[data-theme='dark'] … .workout-plan-table thead th` | `color` | 1 | yes |
| `[data-theme='dark'] … .workout-plan-table thead th` | `text-shadow` | 1 | no |
| `#workout[data-page="workout-plan"] .workout-plan-table tbody td` | `background` | 2 | yes |
| `#workout[data-page="workout-plan"] .workout-plan-table tbody td` | `box-shadow` | 1 | yes |

## The actual owners

These declarations lose to rules in `static/css/components.css`, which are unlayered, later, more
specific, and `!important`:

- **Plan table** → the Calm-Glass table system,
  `:is(#workout[data-page="workout-plan"], .workout-log-page, …) .table.table-calm thead th`
  and `… .table.table-calm tbody td` (plus their `[data-theme='dark']` twins).
- **Selection actions** →
  `#workout[data-page="workout-plan"] #exercise-selection-frame #action-buttons-row.selection-actions`,
  which carries three ids and `!important` on every declaration.

The page bundle's own `2026 Glass/Neumorphic` versions have been dead ever since the Calm-Glass
system landed.

## Declarations deferred (10) — NOT removed

| Rule | Property | Literals |
|---|---|---|
| `… .collapse-toggle:focus-visible` | `box-shadow` | 2 |
| `… .collapse-toggle:disabled` | `box-shadow` | 1 |
| `… .filter-dropdown:focus, … .form-select:focus` | `box-shadow` | 1 |
| `… .selection-actions:hover` | `background` | 3 |
| `… .selection-actions:hover` | `border-color` | 1 |
| `… .selection-actions:hover` | `box-shadow` | 4 |
| `[data-theme='dark'] … .selection-actions:hover` | `box-shadow` | 4 |
| `… .workout-plan-table tbody tr:hover td` | `background` | 2 |
| `… .workout-plan-table tbody tr:hover td` | `box-shadow` | 1 |
| `[data-theme='dark'] … .workout-plan-table tbody tr:hover td` | `background` | 2 |

Note: `… .workout-plan-table tbody tr:hover td` has **both** of its declarations in the deferred
set, so if they are ever certified, the whole rule goes rather than just its declarations.

## Deltas

| Metric | Before | After | Delta |
|---|---|---|---|
| File lines | 5,880 | 5,847 | **−33** |
| CSS rules | 760 | 760 | 0 |
| Declarations | 2,537 | 2,523 | −14 |
| Colour literals removed | — | — | **27** (22 ramp + 5 co-located) |
| `!important` | 520 | 513 | **−7** |

Diff is deletion-only: `0` insertions, `33` deletions. `git diff --check` clean.

### Stylelint — focused (`static/css/pages-workout-plan.css`)

| Rule | Before | After | Delta |
|---|---|---|---|
| `declaration-property-value-disallowed-list` | 481 | 471 | **−10** |
| `declaration-no-important` | 520 | 513 | **−7** |
| `no-descending-specificity` | 61 | 61 | 0 |
| `selector-max-id` | 75 | 75 | 0 |
| `selector-max-specificity` | 77 | 77 | 0 |
| `no-duplicate-selectors` | 7 | 7 | 0 |
| **TOTAL** | **1,221** | **1,204** | **−17** |

### Stylelint — total (`static/css/*.css` + `scss/**/*.scss`)

5,877 → 5,860 (**−17**), same −10 / −7 split, every other category flat.
**No category increased**, focused or total.

## Cascade-layer integrity

| | Before | After |
|---|---|---|
| `@layer workout-dropdowns` | 468–571 | 468–571 (unchanged) |
| `@layer workout` | 718–1713 | 718–1697 |

The `workout` layer shrank by exactly the 16 lines deleted inside it (the Selection Actions
declarations); the other 17 deleted lines are in the unlayered Table section. Layer names, order,
and nesting are unchanged, and no rule crossed the boundary. No rule was emptied — brace count
holds at 813/813 and the file is still pure CRLF.

## Contract lock

`tests/test_css_cascade_contracts.py::test_workout_plan_drops_overridden_rest_state_declarations`
asserts, per rule body rather than by fragile file-wide string match:

1. the 14 dropped properties are absent from the exact rules that carried them;
2. the surviving declarations in those same rules are still present;
3. the real owners in `components.css` still own the painted surface;
4. the 10 interaction-state twins are still present — deliberately deferred, so a future packet
   cannot quietly delete them on the same weaker evidence;
5. no rule is empty and the layer split is unchanged.

## Gates

| Gate | Result |
|---|---|
| CSS parse (postcss) | PASS — 760 rules / 53 at-rules / 2,523 decls; braces 813/813; pure CRLF |
| `git diff --check` | CLEAN |
| Cascade/selector contracts | **26/26 pass** (25 + 1 new) |
| Rest-state computed-style differential | **0 diffs / 31,074 records**, control **0** |
| Full pytest (canonical catalog) | **1,752 passed / 0 failed** (1,751 baseline + 1 new contract) |
| Focused Workout Plan visual, no `--update-snapshots` | **5 passed, 1 failed** — `workout-plan desktop dark` at **exactly 1,039 pixels**, the established WP4.0 animated-logo signature |

The pytest gate used the canonical tracked catalog (`HEAD:data/database.db`, blob `b8c7bd0b`,
sha256 `e7665b3e…`) swapped into the worktree for the run only; the visual seed was restored
afterwards (sha256 `6477b2ac…`) and `data/database.db` stayed `skip-worktree` throughout.

**No visual baseline was updated.** `git status -- e2e/__screenshots__` is empty. No Bootstrap
output, SCSS, or database file is in the diff.

## Findings recorded, not acted on

1. **The sentinel sweep over-reports deadness in animated states.** Its 24-declaration verdict
   reduced to 14 once a stable oracle was demanded. Any future dead-CSS packet on this page must
   pair the sweep with a rest-state differential, and must treat interaction states as unproven.
2. **Page Header (section 829) is fully live** — 15/15 literals render — and remains locked against
   tokenization by the WP4.3i-c contract. Untouched here.
3. The superset dark-tint gap and the dead `body.dark-mode` in `static/css/layout.css:1120` remain
   deferred, unchanged.
