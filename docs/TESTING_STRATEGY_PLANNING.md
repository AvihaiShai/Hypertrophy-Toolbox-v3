# Testing Strategy Review & Plan

> **Date**: 2026-08-01
> **Provenance**: Claims below were checked against the live repository (configs read directly; `npx playwright test --list --project=chromium` and pytest collection executed; all 90 pytest files, both workflows, the backup subsystem, and the E2E suite audited). This document adjudicates two external AI reviews (Opus 5's testing-gap analysis and Codex's critique of it), records the verified current state, lists blindspots **both** models missed, and proposes a risk-ranked plan. A second-pass implementation review by **sol5.6** is incorporated into the phases and recorded in §7.
> **Status**: **Phase 0 + Phase 1 authorized 2026-08-01** (owner sign-off on D1 and the `e2e-erase-flow` half of D2 — recorded in [§8.1](#81-owner-sign-off-recorded-2026-08-01), execution log in [§8.6](#86-execution-log)). **Phases 2–5 remain PLANNING** — proposals awaiting owner selection, with D3–D7 unsigned. Read [§8 Parallel-execution constraints](#8-parallel-execution-constraints) before executing anything from this document.

---

## 1. Verdict on the two AI responses

### 1.1 Summary

| | Opus 5 | Codex |
|---|---|---|
| Conceptual framing (scope / purpose / technique axes) | ✅ Sound | ✅ Endorsed it, correctly |
| Repo-specific factual accuracy | ❌ ~half the "missing" list already exists | ✅ Nearly all claims verified correct |
| "Pyramid speed" claim | ❌ Stated backwards ("wider tier = faster/cheaper") | ✅ Caught the inversion |
| Backup fuzzing proposal | ❌ Targets an interface that does not exist | ✅ Correctly identified the real mechanism |
| Coverage advice | ⚠️ "Gate first" — risky as stated | ✅ Measure → ratchet is the right sequence |
| Awareness of existing prior art (quality gate map, KI registry) | ❌ None | ⚠️ Partial (proposed building a traceability matrix; half of one already exists) |

**Bottom line**: Codex's critique is accurate on essentially every disputed fact. Opus's response is a good *generic* checklist applied without reading the repo. Neither model found the most important problems (§4).

### 1.2 Opus 5 — claim-by-claim

| Opus claim | Verdict | Evidence |
|---|---|---|
| "Coverage gates — do this first" | ⚠️ Half right | Coverage is genuinely absent everywhere ([pytest.ini](../pytest.ini), [vitest.config.js](../vitest.config.js), no `pytest-cov`/`@vitest/coverage-*` in any manifest, no `--cov` in CI). **But** its absence was an explicit prior decision (`docs/archive/ci_cd/phase3/PLANNING.md:125` — "Out: `pytest --cov`"), and a blocking `--cov-fail-under` on day one invites low-value tests. Measure first (§5, Phase 1). |
| "Hypothesis on the calculation core" | ✅ Valid gap | Zero property-based testing. `hypothesis` appears nowhere except as the English word in prose docs. Highest-ROI genuinely-new idea in the Opus response. |
| "Round-trip + fuzz on program backups… truncated/reordered/type-corrupted backup **files**" | ❌ Wrong interface | There is **no backup file**. Backups live in two internal SQLite tables (`program_backups`, `program_backup_items` — [utils/program_backup.py:38-68](../utils/program_backup.py#L38-L68)); `restore_backup(backup_id: int)` takes a row id ([utils/program_backup.py:389](../utils/program_backup.py#L389)); the route takes `<int:backup_id>` only ([routes/program_backup.py:144](../routes/program_backup.py#L144)); zero `request.files` anywhere in the app. Round-trip fidelity is **already tested** row-for-row ([tests/test_program_backup.py:852](../tests/test_program_backup.py#L852)), as are mid-restore fault-injection rollback ([:226](../tests/test_program_backup.py#L226)), create-rollback ([:94](../tests/test_program_backup.py#L94)), single-commit ([:316](../tests/test_program_backup.py#L316)), missing-exercise skip ([:277](../tests/test_program_backup.py#L277)), and pre-`exercise_order` schema drift ([:912](../tests/test_program_backup.py#L912)). |
| "Fresh-install / seed-integrity test" | ❌ Already exists | [tests/test_catalog_seed_bootstrap.py](../tests/test_catalog_seed_bootstrap.py) (10 tests incl. frozen `_MEIPASS` seed resolution), [tests/test_catalog_upgrade.py](../tests/test_catalog_upgrade.py) (19 tests incl. corrupt/missing/shrunk seed), [tests/test_runtime_migration.py](../tests/test_runtime_migration.py) (21 tests incl. corrupted + truncated legacy DB), plus three deep-gate jobs (`first-install`, `empty-schema`, `old-db-migration`). |
| "Visual regression via `toHaveScreenshot()`" | ❌ Already exists | 66-case full-page matrix ([e2e/visual.spec.ts](../e2e/visual.spec.ts): 11 pages × 3 viewports × 2 themes — arithmetic verified against code, `--list`, and disk) + 18 element-scoped thumbnail cases ([e2e/visual-baseline-thumbnails.spec.ts](../e2e/visual-baseline-thumbnails.spec.ts)) = 84 per platform, **168 committed baseline PNGs** (win32 + linux). |
| "Accessibility: axe-core, one assertion per page" | ⚠️ Half right | 24 hand-written a11y tests exist ([e2e/accessibility.spec.ts](../e2e/accessibility.spec.ts)); axe is genuinely absent (no `@axe-core/playwright` in [package.json](../package.json), zero code references). But "one assertion per page" is the wrong prescription, and the existing suite has a deeper problem Opus couldn't see (§4, B1). |
| "Build smoke test — catches PyInstaller didn't bundle templates" | ❌ Already exists | [deep-gate.yml:287-336](../.github/workflows/deep-gate.yml#L287-L336): `windows-latest`, real `pyinstaller --clean --noconfirm`, then `scripts/smoke_packaged_app.py --mode bootloader` (real bootloader, explicitly not weakened to payload mode). Plus 27 source-level packaging contract tests in pytest. The *real* gap is that it never runs on a PR (§4, B8). |
| "Supply chain: pip-audit + npm audit + Dependabot + bandit" | ⚠️ Half right | `pip-audit` is already a **blocking required check** on every PR ([ci.yml:31-38](../.github/workflows/ci.yml#L31-L38)). `npm audit`, Dependabot, bandit, semgrep, CodeQL: all genuinely absent — the JS dependency surface has zero automated vulnerability scanning. |
| "Mutation testing, quarterly" | ✅ Valid gap | `mutmut` absent; no mutation testing anywhere. And §4 B1 shows exactly why this repo needs it. |
| "Skip load testing" | ✅ Correct call | Nothing to add for concurrent users. (Two inline latency assertions already exist — see §4 B17.) |
| "The wider the tier, the faster and cheaper each test is" | ❌ Backwards | Unit tests are the fast/cheap tier; browser E2E is the slow/expensive one. Codex caught this; the rest of Opus's own paragraph (run the fast suite on every save) only makes sense with the correct ordering. |
| "'Never test manually again' is not reachable; keep a 10-minute release checklist" | ✅ Correct | Both models agree; this document keeps that conclusion (§5, residual). |

### 1.3 Codex — claim-by-claim

| Codex claim | Verdict | Evidence |
|---|---|---|
| "~500 documented Playwright tests across 30 specs" | ✅ (trusted stale docs) | Docs say 501 ([.claude/rules/testing.md:13](../.claude/rules/testing.md#L13)); the **live count is 541** (`--list`, 2026-08-01). Codex quoted the documentation faithfully; the documentation is wrong — see §4 B3. |
| "66-case visual matrix across 11 pages, 3 viewports, 2 themes" | ✅ Verified | Matches spec code, runtime listing, and 66 PNGs per platform directory. |
| "Accessibility tests covering keyboard, focus, ARIA, contrast, responsive" | ⚠️ Overstated | The tests exist, but several are tautological or vacuous — including every "contrast" test (§4 B1). Codex correctly said axe is missing but did not detect that some existing assertions cannot fail. |
| "Row-for-row backup/restore round-trip and rollback tests" | ✅ Verified | See Opus row above. |
| "Fresh-install, existing-DB preservation, migration, corrupted-DB tests" | ✅ Verified | See Opus row above. Nuance: corruption tests cover the *legacy DB migration* and *catalog seed* paths; no test feeds corrupted **backup rows** to `restore_backup()` — which matches Codex's own refined fuzzing proposal. |
| "Windows PyInstaller build + real bootloader smoke" | ✅ Verified | [deep-gate.yml:287-336](../.github/workflows/deep-gate.yml#L287-L336). |
| "Required pip-audit security scanning" | ✅ Verified | Blocking, `continue-on-error: false`, required branch-protection check. |
| "The application does not restore an uploaded backup file; backups are internal SQLite tables" | ✅ Verified | Zero `request.files` / upload / import surface repo-wide. A *separate* file-level mechanism exists (`utils/auto_backup.py` writes whole-DB snapshots to `data/auto_backup/`), but it has **no restore path by documented design** ([docs/program_backups.md:66](program_backups.md#L66)). |
| "Coverage should be non-blocking info first, then ratchet" | ✅ Adopted | §5, Phase 1. |
| "Proposed properties may not be valid product rules" | ✅ Important | E.g. "volume after splitting always exactly equals input" must be checked against rounding/caps before becoming a test, and this repo's council workflow (Gate 0 + `product-risk-reviewer`) is the right vehicle — calculation-surface changes are explicitly owner-gated ([docs/ai_workflow/QUALITY_GATE.md](ai_workflow/QUALITY_GATE.md)). |
| "E2E suite is Chromium-only; Firefox/WebKit commented out" | ✅ Verified | [playwright.config.ts:97-105](../playwright.config.ts#L97-L105); every CI invocation passes `--project=chromium`; Firefox/WebKit binaries are never even downloaded. |
| "Deep-gate checks should become release gates" | ✅ Confirmed gap | Deep gate is `workflow_dispatch` **only** — explicitly "no cron / schedule" ([deep-gate.yml:3](../.github/workflows/deep-gate.yml#L3)). No release/tag workflow exists at all. |
| "Expand Vitest coverage and promote the non-required job" | ✅ Confirmed gap | Vitest job is non-required ([ci.yml:586-590](../.github/workflows/ci.yml#L586-L590)); only **8 of 49 modules (16%)** have unit tests; `jsdom` is installed but zero test files opt into it, so every DOM-touching module is untested at unit level. |
| Codex misses | — | The vacuous a11y assertions (B1), the `/erase-data` substitute-route gap (B2), the documentation drift itself (B3), the weakened console-error fixture (B4), CI hygiene issues (B9), and the prior art in `QUALITY_GATE.md` / `UI_SCENARIOS_GAP_ANALYSIS.md` (§2.3). |

---

## 2. Verified current state (ground truth, 2026-08-01)

### 2.1 What exists, by layer

| Layer | Reality | Runs on PR? |
|---|---|---|
| **Python unit + integration (pytest)** | 90 files, 1,716 test-function definitions, **2,288 currently collected nodes** (verified 2026-08-01 with `.venv/Scripts/python.exe -m pytest tests --collect-only -q`; 70 parametrize decorators). Last recorded full run: **2,271 passed / 1 skipped** (2026-07-30, WP4.4-f2 gate). Per-test tmp SQLite isolation via conftest fixture chain. | ✅ Required (`Run Tests`) |
| **JS unit (Vitest)** | 9 files, 93 tests, pure helpers only (`environment: 'node'`). 8/49 modules covered (16%); 41 modules + 6 top-level scripts untested. | ⚠️ Runs, **non-required** |
| **API contract (E2E)** | `api-integration.spec.ts` — 57 tests hitting real endpoints. | ✅ Required (functional shards) |
| **Browser E2E (Playwright)** | 30 specs, **541 live tests**, Chromium only, serial, 1 worker, 2 retries on CI. 24 specs in the required functional shard set (recomputed: **426 tests**, not the documented 404). | ✅ Mostly required; `erase-flow`, `listener-cleanup`, visual specs are not |
| **Visual regression** | 84 cases/platform, 168 committed PNGs, deterministic helpers (frozen Date, animation flattener), `maxDiffPixels: 800, threshold: 0`. | ❌ Manual deep-gate only (`run_visual` input) |
| **Accessibility** | 24 hand-written tests in one spec + modal/toast contracts in `ui-hardening.spec.ts` (31 tests). No axe. 3 of 11 pages covered. | ✅ Required (in shards) — but see B1 |
| **Packaged build** | Real PyInstaller build + bootloader smoke on `windows-latest`; 27 source-level packaging contract tests in pytest. | ❌ Build/smoke: manual deep-gate only |
| **Install / migration** | 50 pytest tests (seed bootstrap, catalog upgrade, legacy migration incl. corrupt/truncated DBs) + 3 deep-gate boot smokes. | ✅ pytest side; ❌ boot smokes manual |
| **Static analysis** | flake8 (blocking subset), tsc (blocking; e2e/ + config only — app JS not typechecked), pyright (blocking baseline-diff vs allowlist), stylelint (measure-only), vulture (dead code, `min_confidence=100`). | ✅ Mostly |
| **Security / supply chain** | `pip-audit` blocking on every PR; `safety` informational in deep gate. **No npm audit, no Dependabot, no bandit, no semgrep, no CodeQL.** | ⚠️ Python yes, JS no |
| **Golden / snapshot** | `tests/goldens/` — weekly-summary + fatigue golden JSON pins. | ✅ Required |

### 2.2 What is genuinely absent (all verified by exhaustive sweep)

- **Coverage measurement** — none, Python or JS (explicit prior decision, now worth revisiting).
- **Property-based testing** (`hypothesis`) — none.
- **Mutation testing** (`mutmut`) — none.
- **Fuzzing** — none (all "fuzz" hits are the exercise-media fuzzy-matching feature).
- **Load testing** — none (correctly out of scope).
- **Automated a11y engine** (axe/pa11y) — none.
- **Firefox / WebKit / mobile-device projects** — none active.
- **Scheduled/nightly/release/tag workflows** — none. `build_exe.bat` is never referenced by any workflow.
- **Time-freezing library** (freegun/time-machine) — none on the Python side (visual specs freeze the browser clock).
- **Test retry tooling for pytest** — none (Playwright gets 2 CI retries; a flaky pytest hard-fails the required check).

### 2.3 Prior art both models missed

- [docs/ai_workflow/QUALITY_GATE.md](ai_workflow/QUALITY_GATE.md) — already a change-type → required-tests/reviewers traceability map with a frontend feature → E2E-spec table. Codex's "build a traceability matrix" should **extend this**, not start fresh.
- [docs/UI_SCENARIOS_GAP_ANALYSIS.md](UI_SCENARIOS_GAP_ANALYSIS.md) — Known-Issues registry (KI-001…KI-009), each row linked to the regression test that locks it.
- `docs/archive/MISSING_TESTS_CHECKLIST.md` / `_PART2.md` — historical gap checklists (archived).
- The repo's agent workflow already includes a **manual-qa-reviewer** charter (exploratory QA via Playwright MCP against the running app) — directly relevant to the "never test manually" goal: part of the residual manual layer is already delegated to an agent.

---

## 3. The taxonomy, answered against this repo

The part of the original question Opus never answered, in one table, using this codebase's own layers:

| Type | Definition | Where it lives here | Speed |
|---|---|---|---|
| **Unit** | One function/module in isolation, no I/O | pytest over `utils/*.py` pure functions (`test_effective_sets.py`, `test_double_progression.py`, `test_body_fat.py`…); Vitest over JS helpers | ms |
| **Integration** | Several real components together (route + logic + real SQLite) | Most of the pytest suite: Flask test client + per-test tmp DB via conftest fixtures | ms–10s of ms |
| **Contract** | Response *shapes* stay stable for consumers | `test_priority0_api_contract.py`, `test_workout_log_calibration_route.py`, golden-JSON pins; `api-integration.spec.ts` at the HTTP level | ms / s |
| **System / E2E** | Whole app through the real UI | 541 Playwright tests against a real Flask server + seeded throwaway DB | s–min |
| **Acceptance (packaged)** | The artifact users actually run | deep-gate `frozen-windows`: real .exe, real bootloader, HTTP 200 poll | min |
| **Non-functional lenses** | Visual, a11y, security, perf — applied at whatever level fits | visual specs (E2E), a11y spec (E2E), pip-audit (dependency), 2 inline latency assertions | varies |
| **Techniques** (cut across levels) | example-based (everything here today), golden/snapshot (2 JSON pins + 168 PNGs), fault-injection (backup rollback tests), property-based (absent), mutation (absent), fuzz (absent) | | |

The correct cost gradient: unit is the cheap/fast tier you run constantly; E2E is the expensive/slow tier you keep small and stable. This repo is actually **inverted relative to the ideal** in one specific sense: its E2E suite (541) is large and load-bearing while its JS unit layer (93) is thin — which is why E2E wall-clock and flake management (93 hard sleeps, shard jobs, isolation jobs) absorb so much CI machinery.

---

## 4. Blindspots — found by this review, missed by both models

Ranked by how much they change the picture.

**B1 — Several accessibility tests are tautological or vacuous (test-suite *quality*, not quantity).**
Verified line-by-line in [e2e/accessibility.spec.ts](../e2e/accessibility.spec.ts):
- All four "Color and Contrast" tests assert only that computed colors are truthy strings — **no contrast ratio is ever computed anywhere in the suite** (`:354-366`, `:368-387`; same pattern in `fatigue-stage4-smokes.spec.ts:144-154`).
- Modal focus-trap final assertion is `expect(a || b !== null).toBeTruthy()` with `b` always non-null (`:303`) — cannot fail.
- "Links distinguishable" has a dead right-operand (`:389-399`) — cannot fail.
- "Error states not color-only" iterates an empty selector set on a fresh page (`:401-423`) — vacuous; no error state is ever induced.
- "Enter activates links" clicks instead of pressing Enter (`:81-87`); Escape-close falls back to clicking the close button, masking Escape regressions (`:108-113`).
- Sampling caps (`Math.min(count, 3|5|10)`) make defects past the 10th element structurally invisible; tap-target test passes if **1 of 5** sampled buttons meets a 32px (not 44px) threshold.
- A11y coverage reaches only `/`, `/workout_plan`, `/volume_splitter` — 3 of 11 pages; zero a11y assertions after data mutation, in error states, or in most dialogs.
This is precisely the failure mode mutation testing exposes: tests that execute code without being able to fail. It also means the repo's "24 accessibility tests" line overstates real protection.

**B2 — pytest never exercises the real `/erase-data` route.**
[tests/conftest.py:105-119](../tests/conftest.py#L105-L119) registers a **substitute** route with no `ERASE_ALL_DATA` confirm guard and no pre-erase snapshot. Consequences: `test_program_backup.py:718` posts with no body and gets 200 where production returns 400; the production confirm-guard, 400 path, and `auto_backup` response payload are covered **only** by `e2e/erase-flow.spec.ts` (2 tests) — which runs in the **non-required** `e2e-erase-flow` CI job. Net: the most destructive endpoint in the app has no required-path negative test.

**B3 — Test-count documentation has rotted, in five different directions.**
Live suite: **541 tests / 30 specs**. Documented totals: 501 ([.claude/rules/testing.md:13](../.claude/rules/testing.md#L13)), 504/505 (MASTER_HANDOVER, REFACTOR_PLAN), 523 (testing.md's own table sum — self-contradicting its 501 headline), 535 (WP4.4-a evidence), 28 spec files (docs/E2E_TESTING.md — actual 30). Three per-spec rows are individually wrong (`ui-hardening` 12 → 31, `body-composition` 5 → 9, `api-integration` 58 → 57), and the "404 required tests, 202+202" figure is actually **426**. The meta-lesson: hand-maintained counts always drift — replace them with a generated inventory (Phase 0).

**B4 — The default E2E fixture suppresses real crashes.**
[e2e/fixtures.ts:29-58](../e2e/fixtures.ts#L29-L58) ignores console/page errors containing `'Cannot read properties of null'`, `'Cannot read properties of undefined'`, `'classList'`, `'is not defined'`, `'404'`, `'Failed to fetch'`… — i.e., genuine null-dereference crashes pass silently. [e2e/strict-fixtures.ts](../e2e/strict-fixtures.ts) exists to fix exactly this but is imported **only** by `visual.spec.ts` and `nav-dropdown.spec.ts`-era specs. Error-collection is also opt-in per spec.

**B5 — 93 hard `waitForTimeout` sleeps across 15 specs** (volume-splitter 23, superset-edge-cases 17, error-handling 11…). This is the suite's dominant flake-and-latency debt; the geometry-flake history (A10 watch) traces to the same class of timing assumptions.

**B6 — The visual oracle is looser than its reputation.**
`maxDiffPixels: 800` with `threshold: 0` means any change touching ≤800 pixels per route × viewport × theme passes silently — already documented as a known weakness in the WP4.4 planning file, plus a standing "animated-logo" red whose diff (875/882 px) *exceeds* the tolerance and is ledgered rather than fixed. Visual specs also apply theme via `addInitScript`, so they never exercise the actual dark-mode toggle path (functional specs cover that separately).

**B7 — JS is the least-protected layer of the stack.**
16% module unit coverage; `jsdom` installed but unused; `tsc` typechecks only `e2e/**` and the Playwright config — **application JS under `static/js/` is neither typechecked nor mostly unit-tested**; the Vitest CI job is non-required. Combined with B4, a runtime TypeError in a module like `exercises.js` can only be caught by an E2E test that happens to traverse it *and* doesn't match a suppression substring.

**B8 — The shipping artifact is never tested on the PR path.**
The frozen .exe build + bootloader smoke, first-install boot, old-DB migration boot, and visual comparison all live exclusively in a manually-dispatched workflow with no schedule and no release trigger. Nothing forces them to run before a release because **there is no release process at all** (no tag workflow, no release checklist in force).

**B9 — CI hygiene findings (none affect correctness today, all are latent cost/risk):**
no `timeout-minutes` on any of the 20 jobs (hangs burn up to 6h of runner); no `concurrency` group (rapid pushes run redundant 12-job pipelines); setup (`npm ci` + CSS build + pip install + browser install) duplicated verbatim across 6+ jobs with no artifact reuse; `pylint` installed but never invoked; `pip-audit`/`safety` installed unpinned at runtime; Python↔Node Playwright version skew (1.59.0 vs 1.60.0); two required job names are factually misleading and can't be renamed without orphaning branch-protection contexts (known gotcha).

**B10 — JS supply chain fully unscanned.** No npm audit, no Dependabot, no lockfile scanning; `bootstrap` pinned at 5.1.3 (2021-era) and consumed by the SCSS build.

**B11 — Backup subsystem residue:** `BACKUP_SCHEMA_VERSION` is written but never consumed (TODO at [utils/program_backup.py:18-21](../utils/program_backup.py#L18-L21)) — the versioning escape hatch doesn't actually exist yet; `prune_auto_backups()` has zero tests; no test feeds corrupted/type-confused **rows** to `restore_backup()` (Codex's refined fuzz target, still open); the file-level auto-backup snapshots have no restore tooling (documented as intentional — but that means disaster recovery is "user copies a file by hand" and is itself untested).

**B12 — Suite hermeticity is per-run, not per-test.** All 541 E2E tests share one mutable SQLite DB serially; isolation is DIY per-spec cleanup calls. This is a deliberate, workable trade-off, but it is why `program-backup.spec.ts` has a documented pollution flake and its own isolated CI job — worth knowing before ever enabling `PW_WORKERS > 1`.

**B13 — Perf assertions that exist are the wrong kind.** `api-integration.spec.ts:881` allows 5,000ms (a hang detector, not a budget); `test_volume_progress.py:590` asserts <100ms wall-clock on a shared CI runner (noise-prone). Codex's "perf budgets for startup/large-history/export/restore" idea is sound but should use generous, variance-aware budgets or it will flake.

**B14 — Positives neither model credited:** `vulture` dead-code gate at `min_confidence=100`; pyright baseline-diff ratchet (the exact "ratchet" pattern Codex recommended for coverage, already proven in this repo for types); golden-fixture pins for the two most drift-sensitive calculations; fault-injection tests in the backup layer; a committed 5×-repeat stability-probe practice before promoting specs to required.

---

## 5. Risk-ranked plan

Ordering principle: **make the existing suite honest before making it bigger.** Each phase is independently shippable; calculation-surface items go through Gate 0/council per [QUALITY_GATE.md](ai_workflow/QUALITY_GATE.md).

### Phase 0 — Hygiene & truth (small, mechanical, high leverage)
1. **Generated and enforced test inventory.** Replace hand-counted totals in `.claude/rules/testing.md` with output from a deterministic script (`playwright --list` + pytest `--collect-only -q` → one committed JSON/markdown table). Add a CI drift check that regenerates the inventory and fails on an unexplained diff; a committed artifact without this check will rot exactly like the current prose. `/status` should consume the same artifact rather than maintain another count.
2. **CI hardening:** add `timeout-minutes` to all jobs; add a workflow-prefixed concurrency group (for example `${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}`) so CI cannot cancel a deep-gate/release run on the same ref; pin `pip-audit`; align Playwright versions (1.59 ↔ 1.60).
3. **JS supply chain:** add `.github/dependabot.yml` (pip + npm + actions, weekly) and run a **full** `npm audit` as measure-only first. Do not use `--omit=dev`: every current package, including Bootstrap/Sass and the test/build toolchain, is in `devDependencies`, so omitting dev dependencies would scan effectively nothing and falsely leave B10 looking closed. Define a documented severity/exception policy before making it blocking.
4. **Promote `e2e-erase-flow` to required** (2 tests, isolated job, cheap) — the only current guard on the destructive path. This requires both the repository change and an explicit GitHub branch-protection update; renaming the job or editing YAML alone does not promote a status context. Preserve the exact required-context name and verify it on a test PR.

### Phase 1 — Measurement, non-blocking (Codex's sequence, adopted)
5. **Python coverage:** add `pytest-cov`, emit report + artifact in the `test` job, no threshold. After 2–3 weeks of data, commit the observed baseline and compare each run against it. A threshold at “observed − 2%” is a tolerance, not a ratchet: it permits an immediate regression and never rises after improvement. Use an explicit baseline-update workflow (the pyright baseline-diff pattern) and include regression checks for `utils/effective_sets.py`, `utils/double_progression*`, `utils/volume_*`, and `utils/program_backup.py` so unrelated coverage cannot mask a core-module drop.
6. **JS coverage:** add the Vitest-4-compatible pinned `@vitest/coverage-v8`, using the same report-first and committed-baseline pattern. Expect a very low number (16% of modules have any tests) — that number is the argument for Phase 3, step 12. Do not make coverage blocking until the collector has produced stable, reproducible results in CI.

### Phase 2 — Make existing tests honest (fixes B1, B2, B4)
7. **Repair or replace the vacuous a11y assertions** (the ≥5 identified in B1, with real contrast-ratio math or axe), then **add `@axe-core/playwright`** on all 11 pages × both themes **plus key states** (open modal, induced validation error, populated tables) — Codex's nuance, adopted. Keep the strong hand-written tests (skip-link, focus-restoration, ui-hardening modal contracts); they cover behavior axe cannot.
8. **Test the real `/erase-data`:** there is no `create_app()` factory, and importing `app.py` performs database migration/bootstrap/initialization. Extract the production erase handler into a reusable route module/blueprint (or a registration helper) and register that exact implementation in both `app.py` and `tests/conftest.py`; delete the substitute test-only handler. Assert 400 without `confirm`, no destructive calls on that path, and 200 + `auto_backup` payload with confirmation. Add failure-path assertions proving a snapshot/drop/initializer error returns the standard 500 contract without reporting success.
9. **Adopt strict console-error fixtures beyond visual specs.** Migrate specs off the suppressing fixture incrementally (start with smoke-navigation + workout-plan); keep a per-spec allowlist for genuinely expected errors instead of the global substring list.

### Phase 3 — New test types where they pay (the valid half of Opus)
10. **Hypothesis on the calculation core** — `effective_sets`, `double_progression`, volume splitter, plan generator. **Every invariant must be owner-confirmed first** (Gate 0 + `product-risk-reviewer`): candidate invariants like "suggested weight never decreases when reps hit ceiling" or "split volume sums to input" must survive rounding/caps/config review before they become tests. Remember the module's own product rule: effective sets are informational-only.
11. **Backup-row fuzzing (Codex's corrected version):** feed `restore_backup()` type-confused/NULL/out-of-range `program_backup_items` rows; assert a clean error + intact live program (the rollback machinery is already tested for injected faults — this extends it to malformed persisted data). Treat `schema_version` as a compatibility-policy decision first: it is persisted, tested, and returned by the API, so deleting it is a DB/API contract change requiring migration notes and consumer review. If retained, define supported/unsupported-version behavior and test it; do not fuzz a value that restore still ignores. `prune_auto_backups()` currently has no production caller—decide whether to remove that dead surface before adding tests that would entrench it.
12. **JS unit expansion with jsdom** for the highest-risk DOM modules (`exercises.js`, `workout-controls-persistence.js` — the KI-005 contract, `toast.js` — the KI-004 contract, `backup-center.js`), then **promote the Vitest job to required** once green for 2 weeks.

### Phase 4 — Release gate (fixes B8; the largest structural gap)
13. **Precondition: make the visual job capable of being a green gate.** The current suite has a ledgered animated-logo failure above `maxDiffPixels: 800`; resolve it or encode a narrow, reviewable expected-difference oracle before requiring the job. Do not raise the global tolerance. Then define a tag/`workflow_dispatch` "release" pipeline that runs frozen-windows, first-install, old-db-migration, and visual compare as **blocking** steps, plus the 10-minute manual checklist below. Until then, add a weekly scheduled deep-gate run—but change `visual-linux` from `if: inputs.run_visual` to a condition that also runs on `schedule` (and release/tag events), because scheduled events supply no workflow-dispatch input and would otherwise silently skip visual comparison. Verify the scheduled run's required job set rather than treating an overall green workflow with skipped jobs as coverage.
14. Decide the browser-matrix question **explicitly** (recommendation: stay Chromium-only for this single-user local tool, but record it as an ADR in `docs/DECISIONS.md` so it's a decision, not drift).

### Phase 5 — Periodic audits (not CI)
15. **Mutation testing** (`mutmut`) over `utils/` calculation modules, quarterly, as a suite audit. B1 is direct evidence this class of problem exists here; expect it to also flag weak pytest assertions.
16. **Flake-debt burn-down:** replace `waitForTimeout` sleeps with event/condition waits, worst files first (volume-splitter 23, superset-edge-cases 17). Track count in the generated inventory.
17. **Further visual-oracle tightening:** after Phase 4's known-red precondition is satisfied, revisit `maxDiffPixels: 800` per-page (the WP4.4 harness work already provides better per-element oracles) and prefer per-element zero-diff checks for high-risk controls. Keep any permanent animated-logo exception narrow and explicit rather than weakening the global oracle.

### Residual manual layer (permanent, by design)
- The 10-minute written release checklist (5–6 core flows: plan → log → summary → progression → backup/restore → erase), run before any release/tag.
- Exploratory QA via the existing `manual-qa-reviewer` agent charter for novel-problem hunting (layout that's technically correct but unusable, suggestions that are mathematically right but wrong in the gym) — the category no automation catches.

---

## 6. Decisions needed from the owner

| # | Decision | Recommendation |
|---|---|---|
| D1 | Reverse the phase-3 "no coverage" decision? | Yes — as non-blocking measurement first (Phase 1); the pyright baseline-diff proves the ratchet pattern works here |
| D2 | Promote `e2e-erase-flow` (and later `js-unit`) to required checks? | Yes / yes-after-stability; mind the exact-name branch-protection gotcha |
| D3 | Release process: full pipeline or weekly scheduled deep-gate as stopgap? | Stopgap now, pipeline when the next packaged release is planned |
| D4 | Hypothesis invariants for calculation modules | Owner review required per invariant (Gate 0) before any property test lands |
| D5 | Browser matrix | Stay Chromium-only; record as ADR |
| D6 | `BACKUP_SCHEMA_VERSION` | Prefer defining and enforcing a compatibility policy. Removal is only acceptable as an explicit DB/API contract migration, not a testing cleanup |
| D7 | Auto-backup file snapshots: keep "no in-app restore" stance? | Keep, but document the manual recovery procedure in the README |

**Sign-off state (2026-08-01):** D1 is signed as non-blocking measurement, and D2 is signed for
`e2e-erase-flow` only. **D3–D7 are unsigned** and no work may act on them. See [§8.1](#81-owner-sign-off-recorded-2026-08-01).

---

## 7. sol5.6 implementation review and action record

**Reviewer identity:** `sol5.6`  
**Review type:** independent implementation-readiness review, 2026-08-01  
**Disposition:** the diagnosis is strong, but execution should not start until the two release/security false-green paths and the inventory enforcement gap are corrected.

### 7.1 Findings incorporated above

| Priority | Finding | Incorporated action |
|---|---|---|
| **P1** | `npm audit --omit=dev` excludes the repository's entire current npm dependency graph. | Phase 0 now requires a full audit plus an explicit severity/exception policy. |
| **P1** | A scheduled deep gate would skip `visual-linux`, while a blocking visual release gate would inherit a known failure. | Phase 4 now requires known-red resolution/containment first and an event-aware visual-job condition. |
| **P2** | The claimed live pytest and hard-wait counts were not reproducible. | §2.1/B5 are corrected to 2,288 collected pytest nodes and 93 hard waits; Phase 0 makes the generated inventory CI-enforced. |
| **P2** | “Observed − 2%” is not a coverage ratchet. | Phase 1 now uses a committed baseline-diff with an explicit update workflow and core-module regression checks. |
| **P2** | The erase-route action referenced a nonexistent application factory. | Phase 2 now requires one shared production route implementation registered in both production and tests. |
| **P2** | Backup actions risked testing dead code and deleting a persisted/API-visible field as cleanup. | Phase 3 now requires dead-code disposition and a compatibility policy before tests or schema/API changes. |

### 7.2 Evidence commands used by sol5.6

```powershell
.venv\Scripts\python.exe -m pytest tests --collect-only -q
# 2288 tests collected

npx playwright test --list --project=chromium
# Total: 541 tests in 30 files

rg -n 'waitForTimeout' e2e -g '*.ts'
# 93 occurrences across 15 specs
```

These were collection/listing/read-only checks; no functional test suite or application mutation was performed for this review.

### 7.3 Execution entry criteria

Before Phase 0 is marked complete:

1. The inventory generator must be deterministic on Windows and Linux and CI must fail on unexplained drift.
2. The npm audit must demonstrably inspect the current lockfile dependency graph, including `devDependencies`.
3. Required-check promotion must be verified in GitHub branch protection on a real PR.
4. The concurrency key must be workflow-scoped so PR CI cannot cancel deep-gate or release runs.

Before Phase 4 is marked complete:

1. Visual compare must have no unconditional known red; any accepted exception must be narrow, documented, and machine-enforced.
2. A scheduled dry run must show visual, packaging, first-install, and old-DB migration jobs as executed—not skipped.
3. A release dry run must fail when any one of those jobs is deliberately made red, proving the fan-in/gating contract.

---

## 8. Parallel-execution constraints

> **Status of this section**: binding on the Phase 0–1 execution slice authorized on
> 2026-08-01. It records the rules that keep this document's execution from breaking
> two other plans running concurrently against the same repository.

### 8.1 Owner sign-off recorded (2026-08-01)

| Decision | Ruling | Scope authorized |
|---|---|---|
| **D1** — reverse the phase-3 "no coverage" decision | **Signed: yes, as NON-BLOCKING measurement.** No threshold, no `--cov-fail-under`, no gate. The observed number is recorded as the baseline for a future baseline-diff ratchet (the `pyright_baseline_diff.py` pattern), not as a pass/fail line | Phase 1, steps 5 and 6 |
| **D2** — promote `e2e-erase-flow` to a required check | **Signed for the `e2e-erase-flow` half only.** The `js-unit` half is explicitly *not* signed and stays non-required until its own stability window is argued separately | Phase 0, step 4 |
| **D3–D7** | **Not signed.** No work in this slice may act on them | — |

Nothing beyond Phase 0 and Phase 1 is authorized by this sign-off. Phases 2–5 remain proposals.

### 8.2 The port-5000 single-runner rule

`playwright.config.ts` pins `baseURL http://127.0.0.1:5000` and its `webServer` auto-starts Flask
on that port. Two concurrent E2E runs on one machine collide — and the `/worktree` skill isolates
the **SQLite database, not the port**.

This is the same constraint recorded as
[`APP_PY_REVIEW_PLAN.md` §5 D4](APP_PY_REVIEW_PLAN.md), extended here from two contenders to
**three**: the app.py review packets (P1–P5), the WPB.4 weekly-summary `Unassigned` bucket work,
and this document's execution. Consequences:

- Only one session may hold port 5000 at a time. A session that does not need E2E must not take it.
- **The Phase 0–1 slice takes no E2E turn at all.** Nothing in Phase 0 or Phase 1 requires a local
  Playwright run or a local Flask server; every CI change in this slice is validated on its own
  pull request's CI run, where each job gets its own runner and its own server.
- Full local `pytest` is unaffected — it uses the Flask test client and a per-test temporary SQLite
  file, binds no port, and contends with nothing.

### 8.3 CI edits are strictly additive

`.github/workflows/ci.yml` job `name:` fields are branch-protection contexts matched **exactly**.
Renaming one orphans its required check and leaves every in-flight pull request unmergeable.

- **Never rename an existing job `name:`.** Add jobs and steps; do not re-label.
- This includes names that are now factually wrong. `e2e-fatigue-context` is named
  `E2E Fatigue Context (Chromium, non-required)` and *has been required since 2026-07-05*. The
  parenthetical is a lie, and it is load-bearing configuration — keep it. The same applies to
  `Type Check (tsc blocking + pyright measure-only)`, where pyright is also baseline-gated.
- Promotion to required is a **branch-protection API change**, never a YAML rename. Read the
  current context list, append to it, and never replace it blindly — other sessions' open pull
  requests depend on the existing set.
- Serialize `ci.yml` edits to one open pull request at a time, so this slice does not conflict with
  itself.

### 8.4 The inventory drift check ships measure-only

Phase 0 step 1 calls for a CI drift check that **fails** on an unexplained inventory diff. It ships
with `continue-on-error: true` instead, because Sessions A and B are actively adding tests: a
blocking drift gate would red every pull request that legitimately changes the test count, including
theirs.

**Flip condition** — the check becomes blocking only after *both* of these have merged:

1. `docs/APP_PY_REVIEW_PLAN.md` packets **P1–P5**, and
2. **WPB.4** (the weekly-summary `Unassigned` bucket).

At that point, regenerate the committed inventory, confirm it matches, and remove
`continue-on-error`. Until then §7.3 entry criterion 1 is only half-satisfied: determinism is
proven, enforcement is deferred by design and this paragraph is the record of why.

### 8.5 Ownership hand-offs

| This document's item | Owner | Note |
|---|---|---|
| **Phase 2, step 8** — test the real `/erase-data` | **Delivered by `APP_PY_REVIEW_PLAN.md` P1 + P5**, not by this plan | P1 extracts the shared handler registration consumed by both `app.py` and `tests/conftest.py`; P5 adds the confirm-guard pytest (missing/wrong `confirm` → 400) against the real handler. Blindspot **B2** closes there. Do not implement it here |
| Phase 0, step 4 — promote `e2e-erase-flow` | This plan | Independent of the above: it makes the *existing* E2E guard required while P1+P5 add the pytest-level guard |

### 8.6 Execution log

Filled in as each pull request merges. Numbers here are **observed**, never carried over from the
prose above — §4 B3 is the standing reminder that hand-maintained counts drift.

| PR | Item | State |
|---|---|---|
| — | PR-0 — this section | in flight |
| — | PR-1 — generated test inventory (Phase 0.1) | pending |
| — | PR-2 — CI hardening (Phase 0.2) | pending |
| — | PR-3 — JS supply chain (Phase 0.3) | pending |
| — | PR-4 — promote `e2e-erase-flow` (Phase 0.4) | pending |
| — | PR-5 — Python coverage, non-blocking (Phase 1.5) | pending |
| — | PR-6 — JS coverage, non-blocking (Phase 1.6) | pending |
