# WP4.3i-filter-btn — Workout Plan dead `#filter-btn` family removal

Packet: WP4.3i-filter-btn (Phase 4 CSS, page #9 Workout Plan)
Base: `main` @ `db23801`, branch `wt/css-wp4-3i-filter-btn`, isolated worktree
Date: 2026-07-25

## Scope

Deletion only, in `static/css/pages-workout-plan.css`. Removed the five rules gated exclusively on
`#filter-btn` — an element that exists nowhere in the application. **0 insertions, 48 deletions.**

No tokenization of the remaining white values. No i-n work, no Page Header change, no edit to the
WP4.3i-c contract, no unrelated declarations, no layer movement, no formatting churn.

## Why the family is dead

### Selector searches — zero consumers

Searched `templates/`, `static/js/`, `routes/`, `utils/`, `e2e/`, `tests/`, `scripts/` and `app.py`
across `*.html`, `*.js`, `*.ts`, `*.py`, `*.json`, `*.jinja`:

| Search | Hits |
|---|---|
| `id="filter-btn"` | **0** |
| `getElementById('filter-btn')` / `("filter-btn")` | **0** |
| `#filter-btn` selector in JS/TS | **0** |
| any `filter-btn` string outside this stylesheet | only `backup-filter-btn` — a different, live control on the Backup page |

### Runtime DOM count — zero, before and after using the filters

Loaded `/workout_plan` against the running app and counted, then changed a filter dropdown, fired
its `change` handler, waited 1.5 s and recounted, in case anything injects an apply button lazily:

| Probe | Before | After filtering |
|---|---|---|
| `document.getElementById('filter-btn')` | 0 | 0 |
| `querySelectorAll('#filter-btn')` | 0 | 0 |
| `#workout[data-page="workout-plan"] #filter-btn.btn` | 0 | 0 |

The filter change did take effect (`primary_muscle_group_button` moved to `Abs` and gained
`filter-active`), so the UI was genuinely exercised.

### The live filter hooks — what actually exists

Every element on the page whose id contains `filter`: `filters-content`, `filters-form`,
`clear-filters-btn`. The real filter controls are:

- **12 dropdown triggers** `button.wpdd-button.wpdd-filter` (`primary_muscle_group_button`,
  `equipment_button`, `difficulty_button`, …);
- **`#clear-filters-btn`** — "Clear Filters" (`templates/workout_plan.html:261`, wired at
  `static/js/modules/filters.js:123`).

**There is no Apply Filters button.** Filtering is change-driven: `filters.js` exports
`filterExercises()` and calls it from the debounced change handler (`filters.js:93`, `:137`, `:347`).
The deleted rules are a leftover from a UI generation that had an apply button; the page moved to
auto-apply and the CSS was never removed.

### Rule-level check — no live grouped arms

All five rules were parsed and every comma-separated arm inspected:

| Lines | Layer | Arms | All arms dead? |
|---|---|---|---|
| 1891–1899 | unlayered | 2 | yes |
| 1901–1909 | unlayered | 2 | yes |
| 1911–1918 | unlayered | 2 | yes |
| 2130–2138 | unlayered | 2 | yes |
| 2140–2146 | unlayered | 2 | yes |

10 arms total, every one gated on `#filter-btn`, **zero live grouped arms**. Each rule pairs a
`#filter-btn.btn` arm with a `#filter-btn.btn.btn-primary` arm, in light and dark, for base / hover
/ active states.

Also removed: the comment `/* Apply Filters Button - Blue - High Contrast */`, which described only
this family, and the blank separator lines that belonged to the deleted blocks.

## Deltas

| Metric | Before | After | Delta |
|---|---|---|---|
| File lines | 5,847 | 5,799 | **−48** |
| CSS rules | 760 | 755 | **−5** |
| Declarations | 2,523 | 2,496 | **−27** |
| `!important` | 513 | 488 | **−25** |
| Colour literals | — | — | **−37** |
| `#filter-btn` references | 5 rules | **0** | — |
| `clear-filters-btn` references | 5 | 5 | **0 (untouched)** |

Diff is deletion-only: `0` insertions, `48` deletions. `git diff --check` clean. No rule emptied,
braces balanced 808/808, file still pure CRLF.

### Stylelint — focused (`static/css/pages-workout-plan.css`)

| Rule | Before | After | Delta |
|---|---|---|---|
| `declaration-no-important` | 513 | 488 | **−25** |
| `declaration-property-value-disallowed-list` | 471 | 452 | **−19** |
| `selector-max-id` | 75 | 65 | **−10** |
| `selector-max-specificity` | 77 | 67 | **−10** |
| `no-descending-specificity` | 61 | 59 | **−2** |
| `no-duplicate-selectors` | 7 | 7 | 0 |
| **TOTAL** | **1,204** | **1,138** | **−66** |

### Stylelint — total (`static/css/*.css` + `scss/**/*.scss`)

5,860 → 5,794 (**−66**), with the same per-rule deltas. **No category increased**, focused or total.

This is the largest single lint reduction of the WP4.3i arc, and the only one to move
`selector-max-id` and `selector-max-specificity` — those rules carried three ids each.

## Cascade-layer integrity

| | Before | After |
|---|---|---|
| `@layer workout-dropdowns` | 468–571 | 468–571 |
| `@layer workout` | 718–1697 | 718–1697 |

**Byte-identical** — every deleted line sits above the layered region (first deletion at L1891, the
`workout` layer ends at L1697), so nothing layered was touched and no rule crossed a boundary.

## Contract lock

`tests/test_css_cascade_contracts.py::test_workout_plan_drops_dead_filter_button_family` pins both
halves of the argument:

1. `#filter-btn` is absent from the page bundle;
2. no template, `static/js` script, e2e spec, or `app.py` supplies a `#filter-btn` consumer — so
   reintroducing the element forces a deliberate restyle rather than silently reviving dead CSS
   (`backup-filter-btn` and `clear-filters-btn` are masked out, being different live controls);
3. the live hooks survive — `#clear-filters-btn` in the template, `filterExercises()` and the
   `clear-filters-btn` wiring in `filters.js`, and both `#clear-filters-btn.btn` rules (light and
   dark) in this bundle;
4. no empty rule, layer split unchanged.

Red path proven **twice**: re-adding a `#filter-btn` CSS rule fails the test, and independently,
renaming the template's `clear-filters-btn` to `filter-btn` also fails it.

## Gates

| Gate | Result |
|---|---|
| CSS parse (postcss) | PASS — 755 rules / 53 at-rules / 2,496 decls; braces 808/808; pure CRLF |
| `git diff --check` | CLEAN |
| Cascade/selector contracts | **27/27 pass** (26 + 1 new) |
| Workout Plan Chromium (`workout-plan` + `exercise-interactions`) | **56 passed** |
| Full pytest (canonical catalog) | **1,753 passed / 0 failed** (1,752 baseline + 1 new contract) |
| Focused Workout Plan visual, no `--update-snapshots` | **5 passed, 1 failed** — the established known red; see drift note |

The pytest gate used the canonical tracked catalog (`HEAD:data/database.db`, blob `b8c7bd0b`,
sha256 `e7665b3e…`) swapped in for the run only; the visual seed was restored afterwards
(sha256 `6477b2ac…`, verified pristine) and `data/database.db` stayed `skip-worktree` throughout.

## Known baseline drift

`workout-plan desktop dark` failed at **1,039 pixels** on the first attempt and **1,046 pixels** on
the retry within the same run. This is the established WP4.0 animated-navbar-logo red, and the
±7 px is drift *within* the animation: the logo is captured at a marginally different frame per
attempt. Earlier packets (i-h, i-dead) happened to land on 1,039 both times.

Diff-image inspection confirms the character is unchanged: red pixels appear **only** on the
animated navbar logo (two instances, top-right and lower-right of the tall capture). The filter
panel, controls, exercise-selection block and plan table are all ghosted-unchanged, and there is no
red anywhere near the filter or button regions this packet touched. Animated-media drift, not
layout or cascade drift.

The other five — `desktop light`, `tablet light`, `tablet dark`, `mobile light`, `mobile dark` —
are byte-identical. **No baseline was updated**; `git status -- e2e/__screenshots__` is empty.

## Findings recorded, not acted on

1. The remaining white literals (`#fff` / `#ffffff`) are **not** tokenized here. After this deletion
   only a handful of raw consumers remain and, per the i-o investigation, just two are both live and
   semantically equivalent — far too few to justify a token.
2. The superset dark-tint gap and the dead `body.dark-mode` in `static/css/layout.css:1120` remain
   deferred, unchanged.
3. The 10 interaction-state declarations deferred by WP4.3i-dead remain deferred; per owner
   instruction they must not be removed without a same-CSS control reaching zero differing records
   after animations are stabilized.
