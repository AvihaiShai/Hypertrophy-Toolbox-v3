# CSS Phase 4 — WP4.3j-d Hover Paint Evidence

Date: 2026-07-27
Branch: `wt/wp4-3j-d-hover-paint`
Base: merged `main` at `c29b05f`
Pull request: #186

## Outcome

WP4.3j-d removes exactly four cascade-dead declarations from the two retained
Region G Workout Log hover rules in `static/css/pages-workout-log.css`:

- light: `background` and `box-shadow`;
- dark: `background` and `box-shadow`.

Both selector lists are byte-identical to the base revision. The live filters
are also byte-identical:

- light: `saturate(1.02) brightness(0.99)`;
- dark: `saturate(1.05) brightness(1.03)`.

The two rules are now filter-only. No rule, selector, media query, template,
JavaScript, SCSS, shared CSS, visual baseline, or database was changed.
`!important` declarations in the comment-stripped bundle fall **217 → 213**.
The file remains **1,621 lines** and contains **9 `@media` rules**.

## Why the four declarations are dead

The audit used real mouse hover, not a selector model. In each of six contexts
(light/dark × desktop/tablet/mobile), row 0 was the only `:hover` row and its
first metric-lane cell was the target.

Before deletion, both Region G hover selectors resolved to exactly one CSSOM
rule and declared `background`, `box-shadow`, and `filter`. The matching-theme
rule owned only `filter`; its expanded `background-color`, `background-image`,
`background-clip`, and `box-shadow` declarations entered the candidate set but
lost everywhere.

The winning paint owners were:

| Target | Light owner | Dark owner |
|---|---|---|
| metric-lane background colour/image | Region H `(1,6,3)` / `(1,5,2)` | Region H `(1,7,3)` / `(1,6,2)` |
| metric-lane box shadow | `components.css` `(1,4,3)` | `components.css` `(1,5,3)` |
| non-metric hover paint | `components.css` `(1,4,3)` | `components.css` `(1,5,3)` |
| filter | Region G light `(0,3,3)` | Region G dark `(0,4,3)` |

`--lane-hover-bg` and `--lane-hover-shadow` are not orphaned. The separate
Region C hover rule still consumes both variables and retains the third
`filter: saturate(…)` declaration.

## Before/after differential

The browser harness audited 51 targets × 36 properties = **1,836 records per
context**, **11,016 total**.

| Oracle | Result |
|---|---|
| computed values | **0 differences / 11,016** |
| declaration owners | **0 differences / 11,016** |
| frame pixels | **0 differences, 6/6 byte-identical PNGs** |
| same-CSS pixel controls | **0 differing pixels, before and after, 6/6** |
| resolution self-check | **2,924 checks / 0 mismatches per side** |
| sentinels | **24/24 effective per side; restoration clean 6/6** |
| matching-rule count | unchanged: 2,159 / 2,015 / 1,913 by viewport |
| candidate-count positive control | **408 records fell; 0 rose** |

Candidate totals fell by 68 in each light context and 136 in each dark context.
The larger dark movement is expected: both Region G rules match under the dark
theme, although only the dark rule owns the live filter. Rule-count delta is
zero because declarations, not rules, were removed.

The known-live control passed before and after in all six contexts: computed
filter was the expected theme value and the matching Region G rule remained its
owner. A missing filter owner was a stop condition.

Artifacts are gitignored under `artifacts/wp43jd/`, including
`before-report.json`, `after-report.json`, `differential.json`, and the twelve
frame captures.

## Contract corrections and red path

The WP4.3j-c-dead Region H sha256 contract had used the first occurrence of
`EXPLICIT METRIC LANE PAIRING`. That phrase also appeared in an earlier deletion
note, so the purported Region H span actually began near line 367 and included
the authorized Region G edit. It was over-broad and produced a false failure;
it never produced a false pass.

WP4.3j-d fixes the contract by anchoring on the unique two-line banner at line
1146, asserts that the span contains **282 newline-delimited lines**, and locks
the corrected span at sha256:

`18658442af0598e5612be704b7e655d14b1dab689efd404138d90a7a93988818`

A new contract pins both complete Region G selector lists, requires each rule
body to contain exactly its expected filter, rejects `background` and
`box-shadow`, and proves the Region C hover family and third filter remain.
The contract passed current CSS and went red against:

1. the complete pre-deletion CSS read as bytes from `git show HEAD`;
2. a targeted removal of the Region G light filter;
3. a targeted restoration of a Region G light background.

The comparator also needed one evidence-only correction. Its owner identity
included `propKey`, the inventory of every property declared by the rule.
Deleting losing properties from the unchanged filter-owning rule therefore
reported 102 false owner changes. Owner identity now uses `viaProp` (the
property actually supplying the record) and excludes mutable rule-wide
`propKey`; the corrected differential is **0 owner changes**.

## Stylelint

The WP4.3j-c-dead after report is the before baseline. JSON was captured from
Stylelint's stderr.

| Scope | Before | After | Delta |
|---|---:|---:|---:|
| all CSS/SCSS warnings | 5,498 | 5,490 | −8 |
| `pages-workout-log.css` warnings | 431 | 423 | −8 |
| `declaration-no-important` (focused) | 217 | 213 | −4 |
| `declaration-property-value-disallowed-list` (focused) | 166 | 162 | −4 |

No warning category increased.

## Gates

- Real-hover after audit: **6/6 contexts green**.
- Browser differential: **0 computed / 0 owner / 0 pixel differences**.
- Workout Log visuals: **6/6 passed**, update-free; screenshot status empty.
- CSS + visual-selector contracts: **33/33 passed**.
- Workout Log + smoke navigation Chromium: **33/33 passed**.
- Full pytest: **1,859 passed / 1 skipped**.
- `git diff --check`: clean.

## Scope boundary

Regions A/B/C/H/I remain untouched, as do `components.css`,
`theme-dark.css`, templates, JavaScript, SCSS, snapshots, and databases.
WP4.4 remains unstarted and requires separate owner direction.
