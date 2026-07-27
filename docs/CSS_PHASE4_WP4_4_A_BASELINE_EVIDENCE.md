# WP4.4-a — Shared-surface measurement baseline and cascade harness

*Phase 4 CSS. Read-only audit packet: **no production path was modified**. Plan:
[`docs/css_phase4_wp4_4/PLANNING.md`](css_phase4_wp4_4/PLANNING.md) (Gate 1 approved, rulings N1–N10).*

**Base:** `wt/wp4-4-a-baseline` from `main` @ `918e7f5`, worktree seeded `-Seed visual`.
**Machine-readable baseline:** [`docs/CSS_PHASE4_WP4_4_A_BASELINE.json`](CSS_PHASE4_WP4_4_A_BASELINE.json) — packets b–k cite this file; a number absent from it may not be quoted as fact (F13).

---

## 1. What this packet delivers

| Deliverable | Path | Ruling / finding |
|---|---|---|
| Static measurement + baseline emitter | `scripts/css_audit/measure.py`, `emit_baseline.py` | A11 (committed, not under `artifacts/`) |
| Specificity model + hand-computed self-check | `scripts/css_audit/specificity.py` | M4 |
| Seven-surface Stylelint | `scripts/css_audit/stylelint_surfaces.mjs` | F20 |
| Runtime cascade harness | `scripts/css_audit/runtime_probe.mjs` | M1/M3/M5/M6, F1, F2, PR#11 |
| M4 resolution self-check | `scripts/css_audit/resolution_check.py` | M4 |
| Pinned baseline JSON | `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` | F13 |
| Contracts (9 tests) | `tests/test_css_wp4_4_a_baseline_contracts.py` | N1, F12, F13, F15, A8/F6, A10 |
| `/fatigue` visual baselines | `e2e/__screenshots__/win32/…` (6 new) | **N7** |
| Matrix-membership contract | `tests/test_visual_selector_contracts.py` | N7 |
| Stale-count correction | `.claude/rules/testing.md:87` | F18 |

Generated captures and reports stay under the gitignored `artifacts/wp4_4/`.

---

## 2. Measured baseline — projections corrected

⚠️ **Plan v1's projections were wrong, and by more than rounding.** This is exactly what F13 predicted.

| Surface | Lines | `!important` decls | Stylelint | Plan v1 projected |
|---|---:|---:|---:|---:|
| `motion.css` | 71 | 8 | 16 | 16 |
| `base.css` | 123 | 0 | 15 | 15 |
| `layout.css` | 1,841 | 24 | 102 | 102 |
| `components.css` | 5,345 | 939 | **1,989** | 1,787 |
| `navbar.css` | 1,542 | 93 | 362 | 362 |
| `theme-dark.css` | 621 | 148 | 264 | 264 |
| `a11y.css` | 813 | 51 | 135 | 135 |
| **Total** | **10,356** | **1,263** | **2,883** | 2,681 |

`components.css` is **+202** warnings over projection; every other surface matched. **V3/V4 gate against this table, not against `docs/CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json`** (F14) — that file is pinned at commit `9ee7638`, predates the whole WP4.3 arc, and is retained only as the historical anchor for the arc-level report at k.

**Per-rule, seven surfaces:**

| Rule | Count | Note |
|---|---:|---|
| `declaration-no-important` | 1,263 | V3 threshold |
| `declaration-property-value-disallowed-list` | 1,127 | |
| `no-descending-specificity` | 245 | |
| `selector-max-id` | 116 | V3 — must not rise |
| `selector-max-specificity` | 102 | V3 — must not rise |
| `no-duplicate-selectors` | **26** | V4 — plan said 86 (global, stale) |
| `declaration-block-no-duplicate-properties` | **2** | V4 — plan said 8 (global, stale) |
| `property-no-unknown` | 2 | |

**V4's stated thresholds were unreachable.** 86 and 8 are *global* WP4.1 figures; on the seven surfaces the true values are 26 and 2. A packet gating against 86 could have tripled duplicate selectors and still "passed".

### F15 — `!important` reconciles across three units

`importantLines` 1,264 · `importantOccurrences` 1,264 · `importantDeclarations` **1,263**.

The one-unit gap is `theme-dark.css:595`, which contains the literal text `Zero !important. */` **inside a comment**. `importantDeclarations` (comments excluded) is the only unit comparable to Stylelint, matches `declaration-no-important` exactly, and is authoritative for V3. The contract asserts all three stay reconciled.

---

## 3. `@layer` spans — exact, and frozen by N2

Order declared at `static/css/tokens.css:2`: `workout, navbar, workout-dropdowns, welcome`.

| File | Layer | Open | Close |
|---|---|---:|---:|
| `components.css` | `workout` | 3539 | 4104 |
| `navbar.css` | `navbar` | 6 | 883 |
| `pages-workout-plan.css` | `workout-dropdowns` | 468 | 571 |
| `pages-workout-plan.css` | `workout` | 718 | 1697 |
| `pages-welcome.css` | `welcome` | 6 | 1071 |

The two page-bundle rows are recorded for completeness and are **out of this arc's scope** — no WP4.4 packet writes a page bundle. Note that the layered regions are far smaller than their files: `pages-workout-plan.css` is 5,799 lines but only lines 468–571 and 718–1697 are layered, so most of that file outranks everything inside `@layer workout` for normal declarations.

**N2 freezes membership for the whole arc.** Layered *normal* declarations lose to every unlayered one; layered `!important` wins over every unlayered one. Moving a rule across a boundary flips precedence in opposite directions depending on importance, which is why this is a hard gate rather than a style note.

---

## 4. The `:is()` family — complete, closed, classified (A10, R3 condition 1)

**19 `:is(` tokens → 17 distinct rules.** Two rules spread their selector list across two lines (`:3335`+`:3336`, `:3749`+`:3750`), which is why the token count exceeds the rule count.

| Group | Tokens | Rules | Specificity | Exports ID weight? | Location |
|---|---:|---:|---|---|---|
| Four-branch shared family | 13 | **12** | (1,3,0) … (1,5,3) | **yes** | `:3335`–`:3413`, unlayered |
| Reduced-motion rule | 1 | **1** | (1,3,2) | **yes** | `:4433`, inside `@media (prefers-reduced-motion: reduce)`, unlayered |
| `input.input-calm-inset:is(#weight, #sets, …)` | 5 | **4** | (2,4,1) … (2,6,1) | **no** | `:3635`–`:3750`, inside `@layer workout` |

**Two refinements to G1, both material for packet i:**

1. **G1 understates the specificity range.** It records `(1,3,1)`/`(1,3,2)`; the twelve rules actually span **(1,3,0) to (1,5,3)**. A repair that assumes a single uniform specificity across the family will mis-predict the winner on the higher rules.
2. **The six-branch construct is doubly non-leaking.** All six branches are IDs, so there is no asymmetric export — *and* it sits inside `@layer workout`, so its normal declarations lose to every unlayered declaration in the app. It is correctly excluded from i's scope, and now for a stated reason rather than by assertion.

The `:4433` three-branch asymmetry (no `.summary-frame.frame-calm-glass`, so reduced-motion transition suppression does not reach Weekly/Session Summary) is **preserved and recorded, not fixed** — normalizing it is a behavioural change on two routes and needs its own approval.

---

## 5. Harness self-checks — all green, after six real defects were found

Full matrix: **11 routes × 2 themes = 22 contexts**, 1440×900, captured **without** `prepareForScreenshot()`.

```
22/22 same-CSS control PASS · 22/22 sentinel PASS · 22/22 pixel control PASS
M4 resolution check: 9,842 ordered cascade pairs, 0 inversions
```

The self-checks were not decorative. **Every one of them failed first**, and each failure was a genuine defect that would have produced false deadness verdicts downstream:

| # | Defect | Symptom | Fix |
|---|---|---|---|
| 1 | Sentinel injected via stylesheet at `body *` = (0,0,1) | 183/200 elements "unaffected" | inline `!important` — the strongest author-origin position |
| 2 | **Sentinel read back through a transition** | `header` and `select` carry `transition: all 0.3s`, so `getComputedStyle` returned the **pre-sentinel** value and reported "no effect" on elements the sentinel reached perfectly | suppress transitions *before* writing the sentinel, and release them *after* reading the revert |
| 3 | Screenshot taken after the sentinel in pass 1 only | every pixel control failed | strict symmetry: both passes run identical work in identical order |
| 4 | Infinite animations treated as measurable | Welcome's `pulse-glow` drifts 57.76px → 58.37px between captures | 8 elements **registered uncertifiable**, excluded from pass/fail, never silently dropped |
| 5 | Fixed navbar paints over `main` | element-scoped capture still contained the animated band; 33–515 px diffs at `y ∈ [2,44]` | clip below every *top-bar* overlay — with horizontal-overlap and top-third tests, because Workout Plan parks a full-height `aside.vp-drawer` off-screen |
| 6 | First raster of a page ≠ its second | up to 36,925 px at channel delta 2 in the Welcome hero | one discarded raster per page, in both passes |

**Defect 2 is a new entry in the M6 family.** M6 lists four oracle defects that each produced a confident false deadness verdict; this is a fifth, and it is not covered by the existing rule. Proposed wording for the arc:

> **M6a.** A sentinel written to a *transitioned* property reads back its pre-sentinel value for the duration of the transition. Suppress transitions before reading, or the sweep will report a live declaration as dead — inline `!important` does not help, because the lag is in the computed value, not the cascade.

**Defect 5 is M3, made specific.** M3 said the full-page oracle is unusable on animated-navbar routes. The mechanism is now pinned down: `header.navbar` is `position: fixed; z-index: 1000`, occupies page `y 0–64`, and `main` begins at `y 8` — so *any* capture including main's top 56px contains the animated band, element-scoped or not.

---

## 6. Uncertifiable set (M1 — registered, not hidden)

| Context | Uncertifiable elements | Cause |
|---|---:|---|
| `welcome--light` / `welcome--dark` | **8** | infinite animations: `pulse-glow` (`.hero-center-icon`), `float` (`.hero-card-1..6`), `heartbeat` (`.credit-heart`), plus a `::before` animation on `.developer-credit-banner` |
| all other 20 contexts | 0 | — |

**No packet may claim a declaration on these 8 elements is dead on this harness's authority.** Their paths are listed in `artifacts/wp4_4/runtime/summary.json` under `selfChecks.sameCssControl[].uncertifiablePaths`.

---

## 7. Motion oracle for WP4.4-c (F1)

`visual.spec.ts` cannot falsify WP4.4-c: `prepareForScreenshot()` sets `animation-duration: 0s !important` and `transition-duration: 0s !important` globally, so deleting `motion.css` entirely would produce a byte-identical visual matrix. The replacement oracle captures the transition/animation longhands at rest, with no determinism tag, under **both** `prefers-reduced-motion` states.

| Route (per theme) | Elements | With motion | Changed under reduced-motion |
|---|---:|---:|---:|
| welcome | 361 | 83 | 83 |
| workout-plan | 4,884 | 2,313 | 2,307 |
| workout-log | 193 | 57 | 57 |
| weekly-summary | 235 | 50 | **48** |
| session-summary | 232 | 49 | **47** |
| progression | 243 | 50 | 50 |
| body-composition | 210 | 43 | 42 |
| volume-splitter | 316 | 54 | 54 |
| user-profile | 1,487 | 305 | 300 |
| backup | 229 | 54 | 53 |
| fatigue | 134 | 31 | 31 / 30 |

Weekly and Session Summary are the two routes where motion-carrying elements are **left unsuppressed** under reduced motion — consistent with the `:4433` three-branch omission documented in §4. This is the pre-existing asymmetry, now measured rather than inferred.

---

## 8. Oracle blind-spot register (F2)

The `(selector, property)` pairs `prepareForScreenshot()` neutralizes before any screenshot. **A packet whose declarations fall inside this register may not cite the pixel matrix as evidence; it must supply a computed-style differential.**

| Selector | Properties neutralized | Blinds |
|---|---|---|
| `*, *::before, *::after` | `animation-*`, `transition-duration`, `transition-delay` → `0s` | **c** |
| `*, *::before, *::after` | `backdrop-filter`, `-webkit-backdrop-filter` → `none` | **h, i, j** |
| `[data-visual-scale-control]` | `background`, `border-color`, `color` → `transparent` | **d** |
| `[data-visual-icon]` | `visibility` → `hidden` | **b, f** |
| `[data-visual-surface][data-visual-surface]` (dark only) | `background`, `background-image`, `border-color`, `border-radius`, `box-shadow`, `text-shadow` | **j** |
| form controls | `border-radius`, `box-shadow`, `text-shadow` | **d, h, j** |

Each entry is re-derived from `e2e/visual-helpers.ts` on every emit, so the register cannot drift from the file it describes.

**Tolerances recorded (F3):** `maxDiffPixels: 800`, `threshold: 0`, `fullPage: true`. The animated-logo band (1,039 / 1,046 px) sits **above** 800 — it is a real snapshot failure of `workout-plan-desktop-dark`, not a diff the option absorbs. Nobody may "fix" it by raising `maxDiffPixels`.

---

## 9. Contract-anchor + pinned-declaration register (A8 + F6)

**21 contract tests** across the two shared contract files read one or more of the seven surfaces; **83 literal strings** are pinned inside them. F6's named examples are both confirmed live: `--nav-gap: var(--s-3);` (binds **f**) and `*:focus-visible,` (binds **d**).

Both registers are re-derived from the test files' ASTs on every emit — a renamed test cannot silently drop out.

**Standing rule (N6):** every packet *runs* `tests/test_css_cascade_contracts.py` and *never edits* it. Only **i** may amend it, as a serialized single-writer claim restricted to re-expressing the same premise; the regression assertion may not be removed or weakened.

---

## 10. Network state, pinned and recorded (PR#11)

`templates/base.html` pulls **11 distinct external assets** (Google Fonts CSS + Inter woff2, FontAwesome CSS + two webfonts, Bootstrap JS, Sortable, flatpickr ×2, Popper, Tippy). Left live, they resolve at different moments on every run — measured directly: two captures of byte-identical CSS disagreed by 33 to 474 pixels, with the diff region moving between runs.

The harness now **caches every external response to `artifacts/wp4_4/net-cache/` on first use and replays it thereafter**, so the page renders exactly as a user sees it while every subsequent run — including a run with no network at all — is byte-reproducible. The manifest (URL → status, sha256, source) is written into `summary.json`. Current state: **11/11 assets cached, 0 unavailable**.

**Correction to the plan's load-order note.** Section 0 describes "the jsdelivr Bootstrap `onerror` fallback at `:15`". The direction is the reverse of what that implies: `base.html:15` loads the **local** `bootstrap.custom.min.css` and falls back **to** jsdelivr only if the local file fails. FontAwesome (`:16`) is CDN-only with **no fallback of any kind** — it is the single external asset whose loss visibly degrades the UI, and nothing guards it.

---

## 11. Route coverage — 11 rendered routes, and the error page (F5, PR#2)

All 11 rendered routes are in the harness matrix, `/fatigue` included.

**`templates/error.html` is NOT reachable by navigation, and the plan's premise about it needs correcting.** `app.py:194` handles 404 by returning a **hard-coded inline HTML document with no stylesheet link at all** — not `error.html`. `error.html` renders only when a route handler catches an exception (`routes/fatigue.py:29`, `routes/weekly_summary.py:130`, and five others). So it is not "painted 100% by the shared bundles" in the way a visited route is; it cannot be reached by requesting a bad URL, and it has no pixel coverage. **Recorded as a gap; no packet should assume a 404 exercises it.**

### N7 — `/fatigue` visual baselines

`templates/fatigue.html` links no stylesheet and declares no `page_css` block, so every pixel on it comes from the seven surfaces this arc rewrites — the highest shared-CSS exposure in the app, and previously the only rendered route with no pixel oracle.

- **Windows: created.** 6 new PNGs (3 viewports × 2 themes), verified reproducible on a second run.
- **Linux: pending.** Only the `visual-linux` deep-gate job can produce them; dispatched separately, see §13.
- **V2 held exactly:** `git status` shows 6 *new* files under `e2e/__screenshots__/` and **zero modified** existing snapshots. N7 authorizes creation, not rebaselining.
- Matrix size **60 → 66**.

### F18 — stale count corrected

`.claude/rules/testing.md:87` recorded `visual.spec.ts | 48 | Eight-page …`. Re-measured with `npx playwright test --list`: **60 before this packet, 66 after**, across eleven pages. Suite total: **535 tests in 30 files**.

---

## 12. Gates

| Gate | Result |
|---|---|
| `pytest tests/` (full suite) | **1,869 passed, 1 skipped, 0 failed** |
| `pytest tests/test_css_cascade_contracts.py tests/test_visual_selector_contracts.py` | pass |
| New contracts `tests/test_css_wp4_4_a_baseline_contracts.py` | 9 passed |
| Harness same-CSS control | 22/22 pass, 0 differing records |
| Harness sentinel-took-effect (M6) | 22/22 pass, all probed elements took and reverted |
| Harness pixel control (0 tolerance) | 22/22 pass |
| M4 resolution self-check | 9,842 pairs, **0 inversions** |
| M4 unit self-check | 17 specificity cases + 3 split cases, 0 failures |
| Seven-surface Stylelint | 2,883 — baseline established |
| `visual.spec.ts -g fatigue` | 6 passed against the new baselines |
| Production CSS diff | **none** — read-only packet |

### F16 red-path proofs

Each new contract was **proven to fail**, then reverted:

| Contract | Injected fault | Observed |
|---|---|---|
| `test_wp4_4_baseline_is_pinned_and_matches_disk` | appended 2 lines to `base.css` | `assert 123 == 125` |
| `test_snapshot_manifest_…_pytest_red` | appended one byte to a baseline PNG | manifest sha mismatch |
| `test_specificity_model_agrees_…` | removed `where` from the zero-specificity set | self-check failure on the `:where()` case |

---

## 13. Open items handed to downstream packets

1. **Linux `/fatigue` baselines — pending.** Requires the `visual-linux` deep-gate job (`workflow_dispatch`, `run_visual=true`, `visual_mode=generate`), which uploads `visual-baselines-linux`. The contract asserts the Linux fatigue set is all-or-nothing, so it stays honest until those six files land. N8 requires the Linux deep gate at h, i, j and k regardless.
2. **G1 specificity range** is wider than recorded — (1,3,0)…(1,5,3), not (1,3,1)/(1,3,2). Packet **i** must not assume a uniform family specificity.
3. **M6a** (transitioned-sentinel lag) is proposed for adoption as an arc method rule.
4. **`error.html` unreachable by 404** — the plan's route-coverage premise needs amending; no packet should treat a bad URL as exercising it.
5. **8 uncertifiable elements on Welcome** — outside what any rest-state differential in this arc can certify.
6. **`components.css` Stylelint is 1,989, not 1,787** — V5 line-contribution projections that lean on the old figure are optimistic.

---

## 14. Rollback

Not applicable — no production file was modified. Per the packet's own criterion, a failing harness self-check would have blocked every downstream packet from citing it; all self-checks pass, twice, on consecutive full-matrix runs.
