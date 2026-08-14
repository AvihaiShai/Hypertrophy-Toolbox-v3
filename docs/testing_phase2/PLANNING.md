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
| **A** | **Merged as `1438a14` (PR #342, 18/18 green).** Repaired nine assertions in `e2e/accessibility.spec.ts` — eight found by re-audit, a ninth by code review; no test node added or removed. Seven red-path rounds proved every repair fails under a seeded violation *and* that the pre-repair spec passed under the identical violation. The only inventory movement is the hard-wait row, from the one removed sleep. No production file changed. |
| **C** | `e2e/console-guard.ts` added; `smoke-navigation`, `workout-plan` and `accessibility` migrated onto it. `strict-fixtures.ts` now re-exports the same guard with the allowlist option removed from its type. One allowlist exists, scoped to a single describe. Four red-path rounds, including the decisive one: an injected null-dereference makes a migrated spec fail while a spec still on `fixtures.ts` passes green. No production file changed; no test node added or removed. |
| **C** | `e2e/console-guard.ts` + migrate `smoke-navigation`, `workout-plan`, `accessibility` | queued |
| **D** | `@axe-core/playwright` on 11 routes × 2 themes + 3 deterministic states | queued |

Packet C's allowlist is a Playwright **option fixture** consumed per file via `test.use({...})` —
never module state. With `workers: 1` and `fullyParallel: false`, a module-level allowlist would
leak across spec files in the same worker and silently weaken the visual/redesign gates.
`strict-fixtures.ts` will re-export a **narrowed** `test` whose type omits the option, so its four
existing importers cannot weaken their gate.

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
| **A** | Repaired 8 assertions in `e2e/accessibility.spec.ts`. Test node count unchanged (24). Six red-path rounds proved every repair fails under a seeded violation *and* that the pre-repair spec passed under the identical violation. Inventory moved only in the hard-wait row (84 → 83). No production file changed. |
