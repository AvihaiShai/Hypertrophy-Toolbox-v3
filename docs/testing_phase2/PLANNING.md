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
| **D** | `@axe-core/playwright` on 11 routes × 2 themes + 3 deterministic states | shipped — see §5 |

E and F are register closures, not part of the repairs → console → axe spine. Both were owner-gated
on 2026-08-14: E under a **named Decision-4 carve-out** (defect established by inspection, because
no honest test can demand an attribute that does not yet exist), F on the finding that its recorded
R1 blocker was false. Rows X1, X2 and X6 in
[`A11Y_EXCEPTIONS.md`](A11Y_EXCEPTIONS.md) carry the decisions.

### 3a. Why Packet D ships as an exception register

A pre-flight axe run, taken before D was written, established that the app produces real WCAG
violations on every route — most consequentially `color-contrast`, which is a colour/token surface
and therefore bound by **R1**: no required check measures visual output, so a token fix would stale
66 win32 + 66 linux captures with CI green. That made the packet's shape an owner question rather
than an implementer's.

The owner decided on **2026-08-14** to take the **explicit-exception path**. Packet D ships as a scan
that still executes every WCAG rule, with each existing violation pinned by surface, rule id and
exact node count. It is deliberately **not** `disableRules()`, impact filtering, broad suppression,
or a global `color-contrast` exemption — each was ruled out by name. The colour/token rewrite and the
two-platform visual re-baseline are out of scope for this arc, and the production corrections for
X7–X13 and X15 are **owner-deferred**: recorded, measured and pinned, but neither blocking Phase 2
nor permanently declined.

The measurements themselves live in [`A11Y_EXCEPTIONS.md`](A11Y_EXCEPTIONS.md) and are not restated
here, so the two files cannot drift apart.

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
| **D** | See §6 for the runtime measurement and the deep-gate threshold. `@axe-core/playwright` pinned exactly at **4.13.0**; 14 test nodes added to `e2e/accessibility.spec.ts` (11 routes × 2 themes in one page load each, plus three light-only states) — no new spec file, so no CI spec-count contract moved. The deliverable is `AXE_REGISTER`: **exact equality** against every WCAG violation the app produces today, so a new violation, a grown one *and* a silently-fixed one are all red. `tests/test_axe_contracts.py` binds the pin, the single-`playwright-core` resolution, matrix completeness, and the rule ↔ `A11Y_EXCEPTIONS.md` write-up. **No production file changed.** Findings: 7 distinct WCAG rules across every route — recorded as rows X7–X15, all **owner-deferred** on 2026-08-14 under the explicit-exception decision in §3a, none fixed here. **Rebased onto `a64ea76` and fully re-verified.** Two things changed in that rebase and both are recorded rather than absorbed: (1) X10 had attributed all fourteen `aria-hidden-focus` nodes to `.wpdd-native`, which a direct probe disproved — there are exactly 13 such selects and the fourteenth is `#vpDrawer`, now split out as **X15**; (2) `volume_splitter:dark` (2 → **3**) and `fatigue:dark` (4 → **6**) drifted, and the register caught it. The cause was proven, not assumed: those counts were first measured before #365 restored the theme-switch transition suppression, so axe was scoring partly-transitioned colour — reverting #365 puts both back to the old numbers, and with it in place three consecutive repeats show zero drift. Four red-path rounds this pass, covering each way the register must fail: a new `image-alt` reds a surface registered as an explicit empty list; labelling `#exerciseSelect` reds with "no longer reported"; a typo'd key reds the missing-entry guard at runtime *and* independently reds `test_axe_contracts.py`. The count-drift mode needed no seeding — it fired for real on the two surfaces above. Stability: `--repeat-each=3 --retries=0`, **114/114**, zero count drift. Gates: full pytest **2858 passed, 2 skipped** · `accessibility.spec.ts` **38 passed** · `tsc --noEmit` clean · inventory regenerated (**647** Playwright / **514** required / **2538** pytest) and `--check` clean · no production or visual-baseline file touched. |
| **C2** | Second console wave, **zero allowlist entries**. Migrated `dark-mode` (7), `browser-navigation-state` (3), `fatigue-stage4-smokes` (5) and `erase-flow` (2) onto `console-guard.ts` — 17 tests, four files, import swap plus hook deletion only. No production file, no allowlist, no Playwright test node added/removed/renamed, no hard wait changed, and the inventory did not move (`--check` clean **without regenerating**, before and after). Closes the two specs §2 named as having **no** console oracle at all (`browser-navigation-state`, `fatigue-stage4-smokes`), both of them in the required functional shard. `erase-flow` is a third case §2 did not name: it called `startCollecting()` and never `assertNoErrors()`, so it carried a **dead** oracle inside a required isolated job. `api-integration` is deliberately **excluded** — all 57 of its tests destructure only `{ request }` and never open a page, so the guard would resolve no `page` fixture and bank coverage that does not exist; that exclusion is a finding, not an omission. All four specs load `base.html` → `darkMode.js`, so one mutation site covers the wave. Red path, both channels, re-run on the shipped base after rebasing onto `a64ea76`: injected `console.error` → **17 failed**; injected null dereference → **17 failed**, reported as `Page error: TypeError: Cannot read properties of null (reading 'classList')`. Control arm is `exercise-catalog-fetch.spec.ts`, still on `fixtures.ts` with a live oracle — under the *identical* mutation it passed **2/2 green**, because the legacy collector suppresses both `Cannot read properties of null` and `classList`. That is a stronger control than Packet C's, which reverted a migrated spec to obtain its green arm; this one is untouched. Both mutations were appended **after** `new DarkMode()` so the feature still initialises and the only new failure is the oracle itself. Mutations reverted, none committed. Packet F's X6 test landed in `dark-mode.spec.ts` during this packet and is now covered by the guard rather than by the suppressing fixture. Gates: full pytest **2851 passed, 2 skipped** (identical to F, confirming zero movement) · 17/17 migrated green post-revert · `tsc` clean · inventory `--check` clean. |

**Post-reconciliation correction to Packet D's stability claim.** The recorded 114/114 run is
factual, but it was not sufficient proof that #365 closed the settlement race. While merging #368,
later runs reproduced the original `volume_splitter:dark` 2 and `fatigue:dark` 4. The 3/6 readings
had the direction backwards: they included transition paint, not additional final-state defects. A
first `document.getAnimations()` repair also failed 7/114 stress cases because the transition list
could be empty before descendant transitions started. `setThemeAndSettle` now holds a document-wide
computed-paint signature stable, `tests/test_axe_contracts.py` pins that scope, and the register is
corrected to **2/4**. This corrects the oracle, not production CSS or the accepted violation set.
Settled-tree gates after the correction: accessibility `--repeat-each=3 --retries=0` **114/114**;
Packet D plus #368's four migrated specs **55/55**; full pytest **2859 passed, 2 skipped**; TypeScript
and generated-inventory checks clean.

## 6. Packet D runtime, and when axe should leave the required gate

### Measured

`e2e/accessibility.spec.ts` runs in the **required** `e2e-functional` gate, so all of this cost lands
on the PR path. Measured locally, win32 Chromium, `--retries=0`, same machine, back to back:

| | Tests | Wall clock |
|---|---|---|
| `accessibility.spec.ts` before | 24 | 28.4 s |
| `accessibility.spec.ts` after | 38 | 59.6 s |
| **Added** | **+14** | **+31.2 s** |

That is 25 axe scans (22 route-theme + 3 states) at a **marginal ~1.25 s per scan**; the rest is 14
page loads and 22 theme settles. The required functional set moves **499 → 513** tests.

> **Baseline note.** Every figure in this section was measured before #365 (Packet F) merged. That
> packet added one `dark-mode` node, so on the shipped base the same +14 reads **500 → 514**, which
> is what `docs/test_inventory/` records. The runtimes and the port-exhaustion findings below are
> unaffected and are left as measured rather than rescaled.

### Why the cost lands where it does

`playwright.config.ts` runs `fullyParallel: false` with `workers: 1`, so a spec is never split across
the two CI legs — the whole +31.2 s lands on whichever `e2e-functional-shard` leg owns
`accessibility.spec.ts`. The required check is the `e2e-functional` **fan-in** gate, green only when
both shards pass, so its wall clock has a floor equal to the longest single spec on the slower leg.
Against the ADR-006 reference of 719 s serial for the required set, each CI leg carries roughly 360 s,
and axe is therefore about **8 % of one leg** today — real, but well inside the existing variance
between the two legs.

### Recommendation

> **Keep axe in the required gate while it adds less than ~60 s to `accessibility.spec.ts`. Above
> that, move it to the deep gate.**

Three things pin that number:

1. **Headroom, quantified.** 60 s ÷ 1.25 s ≈ **48 scans**, against 25 today. That is enough to widen
   the three states to both themes (row X14, +3 scans) and add several routes without reopening this
   decision — but not enough to absorb a third theme or a viewport axis, which are the changes that
   *should* be re-argued.
2. **Shard balance is the real constraint.** At +60 s the spec runs ~90 s, roughly a quarter of a
   leg's ~360 s budget, making it the largest single item in the required set and the gate's floor.
   Past that the cheaper fix is n=3 sharding, not a faster scan.
3. **Crossing it is already an owner decision.** Re-sharding is a four-file contract change
   (`ci.yml`, the `RequiredSpecs` array and shard plan in `scripts/run-playwright-shards.ps1`, the
   pinned spec count in `tests/test_playwright_shard_launcher_contracts.py`, and the ADR-006
   reference counts). The threshold exists so that cost is weighed deliberately rather than absorbed.

**If it moves to the deep gate**, the deep gate needs no edit — its "full suite (minus visual)" step
globs `e2e/*.spec.ts`. What would be needed is a split of the axe describes into their own spec so
they can be excluded from the required list, which *is* a spec-count contract change. That is the
argument for keeping the scan inside `accessibility.spec.ts` until the threshold is actually crossed.

### The other cost: ephemeral ports on the local lane

Wall clock is not the only budget axe spends. Measured over the full required set:

| Run | Tests | Wall clock | Result |
|---|---|---|---|
| Required set, axe excluded (`--grep-invert axe`) | 499 | 9.7 min | 499 passed |
| Required set, first attempt with axe | 513 | 10.8 min | **7 failed** — `EADDRINUSE` / `ERR_ADDRESS_IN_USE` |
| Required set with axe, from a drained port pool | 513 | 10.5 min | **513 passed**, zero `EADDRINUSE` |

The seven failures were all in `user-profile.spec.ts`, all client-side connect failures, and none of
them an assertion about the app. This is the ADR-006 hazard: Werkzeug closes the connection per
request, so every one of the suite's ~44,500 requests holds an ephemeral port for the 120 s recycle
window. The clean re-run started at **TIME_WAIT = 13** and peaked at **7,998** of this host's
**16,384** ports — the serial local lane already consumes about half the pool on its own.

Attribution, because the first result invites the wrong conclusion: axe is **not** what exhausted the
pool. Request volume was effectively unchanged (44,520 with axe and seven tests aborted early, versus
44,793 without), putting axe's marginal cost at roughly **1,300 requests, ~2.9 %**. What differed was
the starting state — the first attempt followed a burst of ad-hoc spec batches whose ports had not
recycled. Re-running the identical set from a drained pool passes.

Two consequences worth keeping:

- **A local full-set run needs a quiet port pool.** Below roughly 8,400 already-held ports it fits;
  above that it does not, whatever the diff. Drain (or wait 120 s) before treating a local
  `EADDRINUSE` as a regression.
- **None of this applies to CI.** `e2e-functional-shard` gives each leg its own runner, port pool and
  server, and each leg carries about 250 tests rather than 513.

### Cross-platform: measured, not assumed

Every registered count was measured on **win32** Chromium, and CI runs ubuntu — the one way this
register could have been born broken. It is not: PR #366 went green on both `E2E Functional Shard
1/2` and `2/2`, so all 25 surfaces reproduce their exact node counts on Linux Chromium. That matches
the mechanism — `color-contrast` is computed from CSS values rather than rasterised glyphs, and the
structural ARIA rules read the DOM — but it is now a measurement rather than an argument.

The register is therefore **not** platform-keyed, and should not be split pre-emptively. If a future
Linux count ever does diverge, the fix is a platform split like the visual baselines already use, and
never a loosened assertion.
