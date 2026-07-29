# WP4.4-f2 — `navbar.css` generation consolidation

Plan: [`docs/css_phase4_wp4_4/PLANNING.md`](css_phase4_wp4_4/PLANNING.md).
Base: `origin/main` at `1dcec85` after the independently verified d2 implementation
and status merges (`#201`, `#202`) plus the d2 evidence correction (`#204`).
Worktree: `wt/wp4-4-f2-navbar`, created with `scripts/new-worktree.ps1 -Seed
visual`.

**Outcome:** three exact duplicate source rules are folded into their existing
generation owners. No computed navbar state changes in 486/486 exhaustive
post-change scenarios. `@layer` membership, all 93 `!important` occurrences,
all 72 custom-property declarations, and the three pinned navigation variables
are unchanged.

This is a generation-consolidation/re-weighting packet, not a deletion-count
exercise. The production diff is 14 insertions and 17 deletions (net `-3`
lines); the eight-line boundary comment preserves the source-pinned layer span.

---

## 1. Complete pre-edit inventory and candidate set

The pre-edit inventory was produced before changing `navbar.css`:

| Measure | Base (`1dcec85`) | f2 |
|---|---:|---:|
| physical lines | 1,536 | 1,533 |
| style rules | 193 | 190 |
| style declarations | 685 | 683 |
| keyframe declarations | 7 | 7 |
| all declarations | 692 | 690 |
| layered / unlayered rules | 103 / 90 | 101 / 89 |
| layered / unlayered declarations | 429 / 256 | 427 / 256 |
| `!important` occurrences | 93 | 93 |
| custom-property declarations | 72 | 72 |
| `@layer` blocks | 1 | 1 |
| `@keyframes` / steps | 2 / 5 | 2 / 5 |

The sole `@layer navbar` block remains at the WP4.4-a source-pinned boundary,
open line 6 through close line 883. The last navbar layer block therefore
survives (G11), and no declaration crossed that boundary (N2).

`--nav-gap`, `--nav-padding-y`, and `--nav-padding-x` remain present and
unchanged. The 155 declarations nominated as matched-but-never-winning by f1
were treated only as nominations; none was used as proof and none was chased.

An exact-structure walk found only these three consolidation candidates:

| Candidate | Exact source relationship | Adjudication |
|---|---|---|
| layered `#navbar` | two identical selector/layer blocks with non-overlapping declarations | fold the scrollbar declarations into the base block |
| layered `#navbar #darkModeToggle::before` | two identical selector/layer blocks; the later block replaces the earlier transform/background | put the final light-theme values directly in the first block |
| unlayered navbar container | `:where(#navbar) > .container-fluid` and `#navbar > .container-fluid` match the same element set | fold `max-width` and `gap` into the existing ID rule after declaration-owner proof |

No selector was relaxed. In particular, the container move uses a provably
identical match set, not a census-derived approximation or a claimed superset.

---

## 2. Ownership oracle validity and exact adjudication

The packet oracle performs in-browser CSS replacement through CDP, captures
computed values and structure, restores the original CSS, and asserts the
restore. Its generated reports live under `artifacts/wp4_4/` and are ignored.

Before candidates were trusted, `f2_oracle_preflight_5.json` passed 86/86
scenarios and both required ownership polarities:

- known-live winner: mobile container `max-width` changed from `1200px` to the
  sentinel `777px`, then restored;
- known-live overridden declaration: the same base `max-width` did not change
  the desktop result because the later media owner remained in force.

Layered important declarations were not classified by normal layer intuition.
Both a layered-important `#navbar` height probe and the competing unlayered
important override were matched and measured; neither was assumed dead.
Important layer order is inverted, so all layered `!important` declarations
remain potentially live unless the browser proves otherwise.

Post-change exact-owner controls (`f2_oracle_post_controls_after_span.json`)
passed:

| Consolidated declaration | Browser result |
|---|---|
| layered `#navbar` `scrollbar-width` | live winner; sentinel changed `none → auto → none` |
| toggle `transform` | matched but overridden in the exercised rest state |
| toggle light-theme `background-color` | live winner; sentinel changed `rgb(59,130,246) → rgb(1,2,3) → original` |
| container mobile `max-width` | live winner |
| container desktop base `max-width` | overridden |
| later desktop-media `max-width` | live winner |
| container `gap` | base owns row gap; later media rule owns column gap |

The exhaustive post report initially expected the toggle background to be
overridden. The browser proved it was a live light-theme winner, so that
expectation was corrected rather than hiding the finding. The clean exhaustive
run itself has 486/486 `candidateSame`, 486/486 `restoredSame`, and 486/486
focus/restore checks green; its sole report-level failure is that now-corrected
expectation. The corrected compact owner/control report is fully green.

This is the exact-structure declaration-owner adjudication that follows the
broad census. A broad “never winning” verdict alone would not have authorized
any of these moves.

---

## 3. State, route, media, motion, and network coverage

The preflight and exhaustive matrices cover:

- 11 rendered routes in both themes;
- workout-plan breakpoint edges at 375, 575/576/577, 767/768/769,
  990/991/992/993, 1359/1360/1361, 1499/1500/1501, and
  1599/1600/1601 pixels;
- collapsed navigation, click-expanded navigation, open dropdowns, and
  keyboard focus at 375, 992, and 1440 pixels in both themes;
- CDP-forced hover/focus/focus-visible/active combinations;
- `prefers-reduced-motion: reduce`, `prefers-contrast: more`, and print.

The full post matrix is the cross-product of 11 routes, both themes, and all 20
edge widths, plus interaction and accessibility media cases: **486 scenarios,
zero computed/structure/focus differences**.

The committed shared runtime harness was also run after the change:

| Shared-harness control | Result |
|---|---:|
| same-CSS controls | 22/22 pass |
| sentinel took effect and reverted | 22/22 pass |
| same-CSS screenshot controls | 22/22 pass |
| unavailable pinned external assets | 0 |
| specificity unit self-check | pass |
| browser-ordered cascade pairs replayed | 9,808 |
| browser/model cascade inversions | 0 |

The runtime harness used one owned Flask listener and its throwaway audit DB.
The port was clear before launch and after shutdown.

### Genuine M6a transition control

M6a does not rely on a universal `transition: none !important` style:

1. a known-live `.collapse-toggle:not(:disabled)` transition is measured at
   `0.2s`;
2. the universal CSS suppressor is injected;
3. CDP forces hover and the browser reports **7 running `CSSTransition`
   objects**;
4. the oracle finishes those objects outside the cascade and reaches the exact
   `translateY(-1px)` endpoint;
5. removal is likewise settled and restores `none`.

The dedicated `--controls-only --no-settle` red path exits non-zero with exactly
the transition-control failure. It proves the CSS-only suppressor cannot make
the probe pass.

---

## 4. Structural contracts and falsification

`tests/test_css_wp4_4_navbar_contracts.py` adds exact, occurrence-aware
contracts for the three consolidated structures and updates the whole-surface
counts. Each new premise was individually falsified, then restored:

| Mutation | Required red |
|---|---|
| remove consolidated `scrollbar-width` | scrollbar-owner contract fails |
| change consolidated toggle `scaleX(1)` to `scaleX(0)` | toggle-owner contract fails |
| remove consolidated container `gap` | container-owner contract fails |
| restore the old `:where(#navbar)` duplicate block | layered/unlayered and total-rule count contracts fail |

The final packet contract file is **19 passed**. The final combined contract
run is **62 passed**:

```text
tests/test_css_cascade_contracts.py
tests/test_visual_selector_contracts.py
tests/test_css_wp4_4_a_baseline_contracts.py
tests/test_css_wp4_4_navbar_contracts.py
```

The first full pytest run correctly rejected an eight-line shift of the frozen
layer closing boundary. The production declarations were already in the right
layer; an in-layer explanatory comment restored the source-pinned close at line
883. The clean full rerun is **2,271 passed, 1 skipped, 0 failed**.

---

## 5. Functional, accessibility, navigation, and visual gates

All Playwright runs were serialized, `PW_REUSE_SERVER` was unset, workers were
fixed at one, and each run owned a throwaway DB and Flask process.

The grouped Chromium functional run is **127 passed** across:

- `nav-dropdown.spec.ts` (blocking);
- `smoke-navigation.spec.ts`;
- `accessibility.spec.ts`;
- `dark-mode.spec.ts`;
- `summary-pages.spec.ts`;
- `volume-progress.spec.ts`;
- `fatigue-stage4-smokes.spec.ts`;
- `ui-hardening.spec.ts`;
- the fatigue navigation/geometry guards reached by those specs.

The separately reconciled required `/fatigue` suite is **8 passed**, including
dark-mode parity, a 375px no-overflow assertion, and badge navigation. Together
these exercise collapsed/expanded navigation, dropdown and keyboard paths,
both themes, accessibility-blocking behavior, required routes, and mobile
geometry.

The Windows visual matrix used the visual seed and ran all 66 cases (11 routes
× 3 viewports × 2 themes):

- **65 passed**;
- only `workout-plan-desktop-dark` failed;
- the run/retry measurements were **875 / 882 / 875 pixels**, exactly within
  the established animated-logo band `875/882 ∪ 1,039/1,046`.

No snapshot was updated, no tolerance was raised, and
`e2e/visual-helpers.ts` was not changed.

---

## 6. Stylelint and integrity

All Stylelint commands exited successfully with warnings only:

| Scope | Base `1dcec85` | f2 | Delta |
|---|---:|---:|---:|
| `navbar.css` | 361 | 356 | -5 |
| seven shared surfaces | 2,849 | 2,844 | -5 |
| full CSS/SCSS tree | 5,456 | 5,451 | -5 |

For `navbar.css`, `declaration-no-important` stays 93 and the categories that
move all improve: descending specificity `17 → 16`, duplicate selectors
`2 → 0`, max ID `75 → 74`, and max specificity `75 → 74`. No category rises in
the seven-surface or full-tree census. The historical WP4.4-a navbar anchor is
362; f1 had already moved current main to 361.

Final integrity checks require and confirm:

- production scope is only `static/css/navbar.css`;
- test/evidence scope is only the packet contract and this evidence document;
- zero paths under `e2e/__screenshots__/`;
- zero changes to `e2e/visual-helpers.ts`, `playwright.config.ts`, `scss/**`,
  runtime DB content, or packets g–k;
- `git diff --check` passes;
- port 5000 has no listener.

Rollback criterion remains any new owner/computed difference, visual difference
outside the ledger band, contract red, Stylelint category increase, layer
membership change, pinned-variable loss, or snapshot drift. None is present.
