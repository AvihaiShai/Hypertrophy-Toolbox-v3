# Testing Strategy Phase 2 — execution plan (Plan v2)

> **Scope**: the *remaining* Phase-2 work from [`TESTING_STRATEGY_PLANNING.md`](../TESTING_STRATEGY_PLANNING.md) §5
> (steps 7, 8, 9), after a fresh truth audit against the live tree. Owner authorized this on
> 2026-08-13 as Gate 0 plus pre-approved Gate 1 for the smallest council-reviewed plan.
> **Base**: `main` @ `542df07`. Phases 3, 4 and 5 remain proposals and are untouched here.

## 1. Owner decisions (fixed)

1. Retire any Phase-2 step already shipped. Never reimplement the real erase-handler work or the
   test-honesty packet (#334).
2. Accessibility honesty = real standards-based **axe** coverage **plus** strong hand-written
   behavior tests. Axe does **not** replace focus/keyboard contracts.
3. Console-error strictness migrates **incrementally**, with **per-spec explicit allowlists**.
   No global substring suppression.
4. **No production behavior change** unless a new honest test exposes a concrete defect; then fix
   only that defect, with matching regression evidence *and* migration notes per CLAUDE.md §1.

Out of scope by instruction: promoting `js-unit`, editing branch protection, editing
`MASTER_HANDOVER.md`.

## 2. Reconciliation — what was already shipped

### Step 8 (real `/erase-data`) — **RETIRED, delivered**

`tests/test_erase_data_guard.py` drives the **real** `app.py` route through the `real_app_client`
fixture: no body → 400, wrong token (parametrized) → 400, non-JSON body → 400, and a rejected erase
leaves the catalog intact. Blindspot **B2** is closed. Two claims in the original plan are stale:
`e2e-erase-flow` has been a **required** branch-protection context since 2026-08-01 (its job name
still carries a false `(non-required)` suffix that must not be renamed), and the guard is no longer
E2E-only.

**Residual, recorded and deliberately not actioned**: `tests/conftest.py` still registers a
guard-less `/erase-data` twin, so the *success* payload (`data.auto_backup`) is covered only by
`e2e/erase-flow.spec.ts`. That is a test-infrastructure refactor with no defect behind it, so
owner decision 4 excludes it.

### Step 7 (accessibility) — **partly shipped**; four B1 claims are stale

| B1 claim | Status 2026-08-13 |
|---|---|
| Escape-close masked by a fallback click | **Already fixed** (KI-006). Escape is the only close path, and backdrop + `body.modal-open` are asserted. |
| "focus returns after modal closes" is weak | **Already fixed** — asserts `toBeFocused()`. |
| "no contrast ratio is ever computed anywhere in the suite" | **Stale.** `e2e/visual-field-separator.spec.ts` computes real WCAG ratios against a 3:1 floor in the **required** gate. |
| modal focus-trap has no real coverage | **Stale at suite level.** `e2e/ui-hardening.spec.ts` owns forward-wrap, backward-wrap and Escape-alone contracts for two modals. |

### Step 9 (strict console) — **barely started**

Most specs still use the suppressing `fixtures.ts`, which ignores page errors matching
`Cannot read properties of null`/`undefined`, `classList` and `is not defined` — genuine
null-dereference crashes. Collection is also **opt-in per describe block**, and four specs assert
nothing about the console at all (`browser-navigation-state`, `fatigue-stage4-smokes`,
`api-integration`, `visual-baseline-thumbnails`). Only `strict-fixtures.ts` fails on them, and it
is imported by a handful of visual/redesign specs. Current counts: see
[`TEST_INVENTORY.md`](../test_inventory/TEST_INVENTORY.md).

## 3. Packets

Ordered **repairs → console → axe**. The order is load-bearing: two council reviewers independently
found that adding axe checks to `accessibility.spec.ts` while it still imports the suppressing
fixture would certify pages whose JavaScript had crashed mid-render.

| Packet | Scope | State |
|---|---|---|
| **A** | Repair the a11y assertions that cannot fail | shipped — see §5 |
| **C** | `e2e/console-guard.ts` + migrate `smoke-navigation`, `workout-plan`, `accessibility` | shipped — see §5 |
| **C2** | Second console wave — migrate `dark-mode`, `browser-navigation-state`, `fatigue-stage4-smokes`, `erase-flow` | shipped — see §5 |
| **E** | Register row X1 — `aria-invalid` on invalid required controls | shipped — see §5 |
| **F** | Register row X6 — restore the `.theme-animating` transition suppression | shipped — see §5 |
| **D** | `@axe-core/playwright` on 11 routes × 2 themes + 3 deterministic states | queued — **blocked, see §3a** |

E and F are register closures, not part of the repairs → console → axe spine. Both were owner-gated
on 2026-08-14: E under a **named Decision-4 carve-out** (defect established by inspection, because
no honest test can demand an attribute that does not yet exist), F on the finding that its recorded
R1 blocker was false. Rows X1, X2 and X6 in
[`A11Y_EXCEPTIONS.md`](A11Y_EXCEPTIONS.md) carry the decisions.

### 3a. Packet D is blocked — measured, not predicted

A pre-flight run of **axe-core 4.13.0** against a live server (4 routes × 2 themes, scratchpad
install so neither the repo nor the junctioned `node_modules` was touched) found violations that
Packet D would inherit on day one:

| Rule | Impact | Nodes on `/workout_plan` | Cause |
|---|---|---|---|
| `aria-allowed-attr` | **critical** | 5 | `aria-activedescendant` on the `.wpdd-button`, a bare `<button>` with no `role`. Not permitted on `role=button`. |
| `aria-hidden-focus` | serious | 14 | 13 `.wpdd-native` selects are `aria-hidden="true"` yet still focusable (`opacity: 0`, no `tabindex="-1"`; an explicit focus test reports `FOCUSABLE`). The 14th is `#vpDrawer`, an unrelated offender. |
| `color-contrast` | serious | 6 here; **84 light / 80 dark on `/user_profile`**, 26 on `/` | Token-level. |

The first two have small corrections — `tabindex="-1"` beside the existing `aria-hidden` for the
selects, and `role="combobox"` for the buttons, though the latter changes the announced role and is
therefore an owner decision rather than a one-liner. **`color-contrast` is the one that reshapes the
packet**: it is a colour/token surface, so under R1 any fix leaves Packet D and becomes an
owner-gated packet carrying the two-platform re-baseline. Packet D cannot go green as scoped
without either that re-baseline or explicit per-rule allowlists, and choosing between those is an
owner decision that belongs before D starts, not during it.

Packet C's allowlist is a Playwright **option fixture** declared on the narrowest describe that
provokes the error — never module state. With `workers: 1` and `fullyParallel: false`, a
module-level allowlist would leak across spec files in the same worker and silently weaken the
visual/redesign gates. `strict-fixtures.ts` re-exports a **narrowed** `test` whose type omits the
option; because a type alone cannot stop a spec importing the wide guard directly,
`tests/test_console_guard_contracts.py` binds the four zero-allowance importers in the required
pytest gate.

## 4. Standing rules

- **R1 — colour/token discoveries split out.** No required check measures visual output, so a
  contrast fix in `tokens.css`/`theme-dark.css` would stale 66 win32 + 66 linux captures with CI
  green. Any such change leaves its packet and becomes an owner-gated packet carrying the
  two-platform re-baseline, `EXPECTED_SNAPSHOT_COUNTS`, and `snapshotManifest`.
- **R2 — flake trap.** `accessibility.spec.ts` "focus returns after modal closes" has a documented
  historical flake. Stability repeats run at `--retries=0`, before and after.
- **R3 — decision-4 contract.** A defect fix needs the failing honest test, a minimal fix, a
  regression test, real-browser verification, and migration notes per CLAUDE.md §1.
- **R4 — red-path ordering.** red-path runs → delete every scratch artifact under `e2e/` → full
  pytest → inventory regen + `--check`. A scratch spec in `e2e/` is visible to four contract tests
  and to the inventory generator.
- **R5 — no committed tracked-file mutation.** Mutate-then-revert; the reverted diff goes in the PR
  body.
- **R6 — serialization.** These packets regenerate `docs/test_inventory/`, which pins per-file
  pytest node counts *and* per-spec Playwright counts behind the required `Test Inventory Drift`
  context. Any open PR that moves either count is a conflict; re-fetch `origin/main` immediately
  before regenerating.

## 5. Execution log

| Packet | Result |
|---|---|
| **A** | **Merged as `1438a14`** (PR #342, 18/18 CI green). Repaired nine assertions in `e2e/accessibility.spec.ts` — eight found by re-audit, the ninth by code review. No test node added or removed; no production file changed. Seven red-path rounds each proved the repair fails under a seeded violation **and** that the pre-repair spec passed under the identical violation. Gates: full pytest 2811 · required set 478 passed · spec ×3 at `--retries=0`, zero flakes · `tsc` clean · inventory `--check` clean. The only inventory movement was the hard-wait row, from the one removed sleep. |
| **C** | `e2e/console-guard.ts` added; `smoke-navigation`, `workout-plan` and `accessibility` migrated onto it; `strict-fixtures.ts` narrowed to a re-export; `tests/test_console_guard_contracts.py` added to bind the narrowing. `smoke-navigation` and `accessibility` needed **zero** allowlist entries; `workout-plan` needed four, scoped to the one describe that mocks a 400. No production file changed, and no Playwright test node added or removed. Four red-path rounds — the decisive one injects a null dereference and shows a migrated spec red while a spec still on `fixtures.ts` passes green. The source contract was itself mutation-tested. Gates: full pytest 2820 · required set 498 passed, zero guard trips · migrated three + both non-visual strict importers 121 passed · `tsc` clean. |
| **E** | **Merged as `ebfa716`** (PR #364, 18/18 CI green). Register row X1. `aria-invalid` set and cleared at the six sites owning `.is-invalid-required`, across `workout-plan-add-exercise.js` and `routine-cascade.js`. On `#exercise` it lands on the `.wpdd-button`, because `workout-dropdowns.js` marks the native select `aria-hidden="true"`; the three cascade selects are unenhanced and carry it directly. Coverage extended the **existing** "error states are not color-only" node, so the inventory did not move (24 nodes before and after). Red path run **both directions**: production reverted fails the mark assertion (`null`), and clear-path-only removal fails the correction assertion with `aria-invalid="true"` stuck on a corrected select — a mark-only fix and a suite blind to the clear path are otherwise indistinguishable. Gates: full pytest 2847 · accessibility 24 passed · inventory `--check` clean · zero CSS touched, so zero baseline exposure (`aria-invalid` matches no selector in any file under `static/css/`, `bootstrap.custom.min.css` included). |
| **F** | **Merged as `a49da8d`** (PR #365, 18/18 CI green). Register row X6. Restored the four-branch `html.theme-animating` suppression into `motion.css` — not `theme-dark.css`, which is digest-pinned, nor `a11y.css`, whose `!important` count is pinned at 50. No JS change. The defect was measured, not inferred: `body` reports `transitionDuration` **`0.3s`** with the rule absent and **`0s`** with it restored. Contracts pin **both halves** of the CSS/JS pair, because the failure mode was the two drifting apart — `ee82643` deleted the CSS and left the JS. Red path: the two CSS-pinning contract nodes fail with the rule removed while the JS-half nodes correctly still pass, and the E2E node fails at `0.3s`, proving the `0s` assertion is not vacuous. Gates: full pytest 2851 · dark-mode 7 / accessibility 24 / nav-dropdown 7 passed · inventory regenerated and `--check` clean · baselines unchanged at 81 win32 / 81 linux, none regenerated. **Note for future CSS work:** `test_css_theme_dark_p3_audit_contracts.py::test_this_packet_wrote_no_production_css` reds on any *uncommitted* `static/css` change by design (working-tree-scoped) and clears once committed. |
| **C2** | Second console wave, **zero allowlist entries**. Migrated `dark-mode` (7), `browser-navigation-state` (3), `fatigue-stage4-smokes` (5) and `erase-flow` (2) onto `console-guard.ts` — 17 tests, four files, import swap plus hook deletion only. No production file, no allowlist, no Playwright test node added/removed/renamed, no hard wait changed, and the inventory did not move (`--check` clean **without regenerating**, before and after). Closes the two specs §2 named as having **no** console oracle at all (`browser-navigation-state`, `fatigue-stage4-smokes`), both of them in the required functional shard. `erase-flow` is a third case §2 did not name: it called `startCollecting()` and never `assertNoErrors()`, so it carried a **dead** oracle inside a required isolated job. `api-integration` is deliberately **excluded** — all 57 of its tests destructure only `{ request }` and never open a page, so the guard would resolve no `page` fixture and bank coverage that does not exist; that exclusion is a finding, not an omission. All four specs load `base.html` → `darkMode.js`, so one mutation site covers the wave. Red path, both channels, re-run on the shipped base after rebasing onto `a64ea76`: injected `console.error` → **17 failed**; injected null dereference → **17 failed**, reported as `Page error: TypeError: Cannot read properties of null (reading 'classList')`. Control arm is `exercise-catalog-fetch.spec.ts`, still on `fixtures.ts` with a live oracle — under the *identical* mutation it passed **2/2 green**, because the legacy collector suppresses both `Cannot read properties of null` and `classList`. That is a stronger control than Packet C's, which reverted a migrated spec to obtain its green arm; this one is untouched. Both mutations were appended **after** `new DarkMode()` so the feature still initialises and the only new failure is the oracle itself. Mutations reverted, none committed. Packet F's X6 test landed in `dark-mode.spec.ts` during this packet and is now covered by the guard rather than by the suppressing fixture. Gates: full pytest **2851 passed, 2 skipped** (identical to F, confirming zero movement) · 17/17 migrated green post-revert · `tsc` clean · inventory `--check` clean. |
