# Testing Strategy Review & Plan

> **Status update 2026-08-14 (superseding the earlier same-day entry):
> Phase 2 is COMPLETE.** Every packet is on `origin/main`. **A** shipped as #342
> (`1438a14`), **C** as #362 (`52331bf`) with #368 (`9be1a3f`) extending it,
> **E** as #364 (`ebfa716`), **F** as #365 (`a49da8d`), and **D** as #366
> (`f627161`). Step 8's real `/erase-data` coverage was already shipped and
> remains retired. The earlier wording of this banner — *"Packet C … and Packet D
> … remain queued; do not report them as delivered"* — is now false and is
> corrected here rather than deleted.
>
> Packet D shipped on the owner's **explicit-exception path**: axe executes every
> WCAG rule, and each existing violation is pinned by surface, rule id and exact
> node count in `AXE_REGISTER`. The remaining accessibility debt is **X7–X13 and
> X15, owner-deferred** — see
> [`testing_phase2/A11Y_EXCEPTIONS.md`](testing_phase2/A11Y_EXCEPTIONS.md).
> Phases 3 and 5 remain proposals. **The release/tag half of Phase 4 shipped
> 2026-08-14 as Packet R1**
> ([`release_pipeline/PLANNING.md`](release_pipeline/PLANNING.md)) — this corrects
> the "remain proposals" wording that covered it — **but Phase 4 is still open**:
> §7.3 entry criteria 2 and 3 are unmet, and R1's tag trigger has never fired. The
> D3 weekly compare-only stopgap is shipped, but **no scheduled execution has ever
> occurred** (measured 2026-08-16T22:41Z: zero `schedule`-event runs repo-wide; re-measure
> before relying on it, the cron is due 03:17 UTC each Monday). The 2026-08-17 run is
> contaminated by the #388 merge (it runs R2-b's file); the first uncontaminated
> schedule-event checkpoint is **2026-08-24** — see
> [`release_pipeline/PLANNING.md`](release_pipeline/PLANNING.md) § Packet R2-b.

> **Date**: 2026-08-01
> **Provenance**: Claims below were checked against the live repository (configs read directly; `npx playwright test --list --project=chromium` and pytest collection executed; all 90 pytest files, both workflows, the backup subsystem, and the E2E suite audited). This document adjudicates two external AI reviews (Opus 5's testing-gap analysis and Codex's critique of it), records the verified current state, lists blindspots **both** models missed, and proposes a risk-ranked plan. A second-pass implementation review by **sol5.6** is incorporated into the phases and recorded in §7. A third-pass, post-execution review by **Fable 5** (2026-08-02) is recorded in §9; its inline amendments are marked *(Fable 5, 2026-08-02: …)*.
> **Status**: **Phase 0 + Phase 1 COMPLETE, shipped 2026-08-01** (owner sign-off on D1 and the `e2e-erase-flow` half of D2 — recorded in [§8.1](#81-owner-sign-off-recorded-2026-08-01), execution log in [§8.6](#86-execution-log)). **Phases 2, 3 and 5 remain PLANNING** — proposals awaiting owner selection. **D3 and D5 were signed 2026-08-02** ([§8.1a](#81a-second-sign-off-2026-08-02--d3-and-d5)); **D6 was signed 2026-08-14** as retain-informational ([§8.1c](#81c-fourth-sign-off-2026-08-14--d6), ADR-008); **D4 and D7 remain unsigned**, as does the js-unit half of D2. Phase 4 is not complete — D3 was signed as the **stopgap half only**, and **that stopgap SHIPPED 2026-08-11 as PR #323 (`3b1160b`)**: the deep gate now runs weekly, compare-only, with `visual-linux` executed rather than skipped on the schedule. *No scheduled run has ever executed (measured 2026-08-16T22:41Z: zero `schedule`-event runs repo-wide). 2026-08-17 03:17 UTC was to be the first authoritative one, but the #388 merge of 2026-08-16 means that run executes R2-b's file and is **contaminated**; the first uncontaminated schedule-event checkpoint is **2026-08-24**.* The **release/tag pipeline half of Phase 4 shipped 2026-08-14 as Packet R1** ([§8.1b](#81b-third-sign-off-2026-08-14--the-releasetag-pipeline), design record in [`release_pipeline/PLANNING.md`](release_pipeline/PLANNING.md)), **but Phase 4 is still open**: §7.3 entry criteria 2 and 3 are not satisfied by R1, and R1's tag trigger has never executed. ([§8.7](#87-phase-4-stopgap-the-precondition-is-not-met-2026-08-02) is now history — its blocked-on-stale-baselines diagnosis was resolved 2026-08-04.) Read [§8 Parallel-execution constraints](#8-parallel-execution-constraints) before executing anything from this document, and [§9](#9-fable-5-review-2026-08-02) for what had already drifted by 2026-08-02 plus the preconditions Phases 2–5 still need.

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
| "Accessibility: axe-core, one assertion per page" | ⚠️ Half right | 24 hand-written a11y tests exist ([e2e/accessibility.spec.ts](../e2e/accessibility.spec.ts)); axe was genuinely absent when this was audited (no `@axe-core/playwright` in [package.json](../package.json), zero code references); **Packet D closed that gap on 2026-08-14 via #366**. But "one assertion per page" is the wrong prescription, and the existing suite has a deeper problem Opus couldn't see (§4, B1). |
| "Build smoke test — catches PyInstaller didn't bundle templates" | ❌ Already exists | `deep-gate.yml`'s `frozen-windows` job: `windows-latest`, real `pyinstaller --clean --noconfirm`, then `scripts/smoke_packaged_app.py --mode bootloader` (real bootloader, explicitly not weakened to payload mode). Plus 27 source-level packaging contract tests in pytest. The *real* gap is that it never runs on a PR (§4, B8). *Audited against an inline copy in `deep-gate.yml`; **Packet R2-b** lifted that body into [`_packaged-windows.yml`](../.github/workflows/_packaged-windows.yml), which is now the only place those three commands appear. The job and its guarantee are unchanged — only the file holding them moved. The original `deep-gate.yml:287-336` anchor was already stale before the lift; do not re-add a line citation.* |
| "Supply chain: pip-audit + npm audit + Dependabot + bandit" | ⚠️ Half right | `pip-audit` is already a **blocking required check** on every PR ([ci.yml:31-38](../.github/workflows/ci.yml#L31-L38)). `npm audit`, Dependabot, bandit, semgrep, CodeQL: all genuinely absent — the JS dependency surface has zero automated vulnerability scanning. |
| "Mutation testing, quarterly" | ✅ Valid gap | `mutmut` absent; no mutation testing anywhere. And §4 B1 shows exactly why this repo needs it. |
| "Skip load testing" | ✅ Correct call | Nothing to add for concurrent users. (Two inline latency assertions already exist — see §4 B13.) |
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
| "Windows PyInstaller build + real bootloader smoke" | ✅ Verified | `deep-gate.yml`'s `frozen-windows` job, whose body **Packet R2-b** lifted into [`_packaged-windows.yml`](../.github/workflows/_packaged-windows.yml) — see the "Build smoke test" row above. |
| "Required pip-audit security scanning" | ✅ Verified | Blocking, `continue-on-error: false`, required branch-protection check. |
| "The application does not restore an uploaded backup file; backups are internal SQLite tables" | ✅ Verified | Zero `request.files` / upload / import surface repo-wide. A *separate* file-level mechanism exists (`utils/auto_backup.py` writes whole-DB snapshots to `data/auto_backup/`), but it has **no restore path by documented design** ([docs/program_backups.md:66](program_backups.md#L66)). |
| "Coverage should be non-blocking info first, then ratchet" | ✅ Adopted | §5, Phase 1. |
| "Proposed properties may not be valid product rules" | ✅ Important | E.g. "volume after splitting always exactly equals input" must be checked against rounding/caps before becoming a test, and this repo's council workflow (Gate 0 + `product-risk-reviewer`) is the right vehicle — calculation-surface changes are explicitly owner-gated ([docs/ai_workflow/QUALITY_GATE.md](ai_workflow/QUALITY_GATE.md)). |
| "E2E suite is Chromium-only; Firefox/WebKit commented out" | ✅ Verified | [playwright.config.ts:97-105](../playwright.config.ts#L97-L105); every CI invocation passes `--project=chromium`; Firefox/WebKit binaries are never even downloaded. |
| "Deep-gate checks should become release gates" | ✅ Confirmed gap | Deep gate was `workflow_dispatch` **only** — explicitly "no cron / schedule". No release/tag workflow exists at all. **Partly closed 2026-08-11 (D3 stopgap, PR #323 → `3b1160b`):** a weekly `schedule:` now runs the deep gate, compare-only. The release/tag half of the gap stands. *The original line cited `deep-gate.yml:3` for the "no cron" comment; that line anchor no longer says it — do not re-add the citation, the file now documents the schedule.* |
| "Expand Vitest coverage and promote the non-required job" | ✅ Confirmed gap | Vitest job is non-required ([ci.yml:586-590](../.github/workflows/ci.yml#L586-L590)); only **8 of 49 modules (16%)** have unit tests; `jsdom` is installed but zero test files opt into it, so every DOM-touching module is untested at unit level. |
| Codex misses | — | The vacuous a11y assertions (B1), the `/erase-data` substitute-route gap (B2), the documentation drift itself (B3), the weakened console-error fixture (B4), CI hygiene issues (B9), and the prior art in `QUALITY_GATE.md` / `UI_SCENARIOS_GAP_ANALYSIS.md` (§2.3). |

---

## 2. Verified current state (ground truth, 2026-08-01)

### 2.1 What exists, by layer

| Layer | Reality | Runs on PR? |
|---|---|---|
| **Python unit + integration (pytest)** | Dated evidence: 90 files, 1,716 test-function definitions, **2,288 collected nodes as of 2026-08-01**; last recorded full run **2,271 passed / 1 skipped** (2026-07-30, WP4.4-f2 gate). **Superseded — the current count is generated into [`TEST_INVENTORY.md`](test_inventory/TEST_INVENTORY.md); do not quote the 2,288 as current.** Per-test tmp SQLite isolation via conftest fixture chain. | ✅ Required (`Run Tests`) |
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
- **Time-freezing library** (freezegun/time-machine) — none on the Python side (visual specs freeze the browser clock).
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
*Update 2026-08-02: partially closed — #262 added `packaged-smoke-windows` (real PyInstaller build + real bootloader smoke, non-required) to every PR. The release-process half of B8 still stands. See §9.1.*

**B9 — CI hygiene findings (none affect correctness today, all are latent cost/risk):**
no `timeout-minutes` on any of the 20 jobs (hangs burn up to 6h of runner); no `concurrency` group (rapid pushes run redundant 12-job pipelines); setup (`npm ci` + CSS build + pip install + browser install) duplicated verbatim across 6+ jobs with no artifact reuse; `pylint` installed but never invoked; `pip-audit`/`safety` installed unpinned at runtime; Python↔Node Playwright version skew (1.59.0 vs 1.60.0); two required job names are factually misleading and can't be renamed without orphaning branch-protection contexts (known gotcha).

**B10 — JS supply chain fully unscanned.** No npm audit, no Dependabot, no lockfile scanning; `bootstrap` pinned at 5.1.3 (2021-era) and consumed by the SCSS build.

**B11 — Backup subsystem residue:** `BACKUP_SCHEMA_VERSION` is written but never consumed — *resolved 2026-08-14 as a decision rather than a defect: the value is a **reserved informational label** and restore is deliberately version-blind (D6, [§8.1c](#81c-fourth-sign-off-2026-08-14--d6), ADR-008). The TODO is gone and the contract, including the bump-and-branch rule for the next payload change, is stated at the definition site.* `prune_auto_backups()` has zero tests; no test feeds corrupted/type-confused **rows** to `restore_backup()` (Codex's refined fuzz target, still open); the file-level auto-backup snapshots have no restore tooling (documented as intentional — but that means disaster recovery is "user copies a file by hand" and is itself untested).

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
5. **Python coverage:** add `pytest-cov`, emit report + artifact in the `test` job, no threshold. After 2–3 weeks of data, commit the observed baseline and compare each run against it. A threshold at “observed − 2%” is a tolerance, not a ratchet: it permits an immediate regression and never rises after improvement. Use an explicit baseline-update workflow (the pyright baseline-diff pattern) and include regression checks for `utils/effective_sets.py`, `utils/double_progression*`, `utils/volume_*`, and `utils/program_backup.py` so unrelated coverage cannot mask a core-module drop. *(Fable 5, 2026-08-02: when the ratchet is designed, prefer a per-PR **diff-coverage** gate over a baseline-total comparison, keeping the per-core-module floors as the safety net — §9.2 F5-5.)*
6. **JS coverage:** add the Vitest-4-compatible pinned `@vitest/coverage-v8`, using the same report-first and committed-baseline pattern. Expect a very low number (16% of modules have any tests) — that number is the argument for Phase 3, step 12. Do not make coverage blocking until the collector has produced stable, reproducible results in CI.

### Phase 2 — Make existing tests honest (fixes B1, B2, B4)
7. **Repair or replace the vacuous a11y assertions** (the ≥5 identified in B1, with real contrast-ratio math or axe), then **add `@axe-core/playwright`** on all 11 pages × both themes **plus key states** (open modal, induced validation error, populated tables) — Codex's nuance, adopted. Keep the strong hand-written tests (skip-link, focus-restoration, ui-hardening modal contracts); they cover behavior axe cannot.
8. **Test the real `/erase-data`:** there is no `create_app()` factory, and importing `app.py` performs database migration/bootstrap/initialization. Extract the production erase handler into a reusable route module/blueprint (or a registration helper) and register that exact implementation in both `app.py` and `tests/conftest.py`; delete the substitute test-only handler. Assert 400 without `confirm`, no destructive calls on that path, and 200 + `auto_backup` payload with confirmation. Add failure-path assertions proving a snapshot/drop/initializer error returns the standard 500 contract without reporting success.
9. **Adopt strict console-error fixtures beyond visual specs.** Migrate specs off the suppressing fixture incrementally (start with smoke-navigation + workout-plan); keep a per-spec allowlist for genuinely expected errors instead of the global substring list.

### Phase 3 — New test types where they pay (the valid half of Opus)
10. **Hypothesis on the calculation core** — `effective_sets`, `double_progression`, volume splitter, plan generator. **Every invariant must be owner-confirmed first** (Gate 0 + `product-risk-reviewer`): candidate invariants like "suggested weight never decreases when reps hit ceiling" or "split volume sums to input" must survive rounding/caps/config review before they become tests. Remember the module's own product rule: effective sets are informational-only. *(Fable 5, 2026-08-02: two operational preconditions before any property test lands — point Hypothesis's `.hypothesis/` example database under `artifacts/` (ADR-002) and register a CI profile with `derandomize=True`/`deadline=None`, because `Run Tests` is a required check with no retry — §9.2 F5-3.)*
11. **Backup-row fuzzing (Codex's corrected version):** feed `restore_backup()` type-confused/NULL/out-of-range `program_backup_items` rows; assert a clean error + intact live program (the rollback machinery is already tested for injected faults — this extends it to malformed persisted data). **The `schema_version` precondition is discharged (2026-08-14, D6 → ADR-008): it is retained as a reserved informational label and restore stays version-blind, so the fuzz target is the `program_backup_items` rows and never the version itself** — fuzzing a value restore ignores would prove nothing. Version-blindness is already pinned by `test_restore_ignores_foreign_schema_version`, so step 11 need not re-cover it. *(Original wording, superseded: "Treat `schema_version` as a compatibility-policy decision first … If retained, define supported/unsupported-version behavior and test it; do not fuzz a value that restore still ignores.")* `prune_auto_backups()` currently has no production caller—decide whether to remove that dead surface before adding tests that would entrench it.
12. **JS unit expansion with jsdom** for the highest-risk DOM modules (`exercises.js`, `workout-controls-persistence.js` — the KI-005 contract, `toast.js` — the KI-004 contract, `backup-center.js`), then **promote the Vitest job to required** once green for 2 weeks. *(Fable 5, 2026-08-02: adopt jsdom via per-file `// @vitest-environment jsdom` pragmas, leaving the global `environment: 'node'` and the 9 existing files untouched — §9.2 F5-6.)*

### Phase 4 — Release gate (fixes B8; the largest structural gap)
13. **Precondition: make the visual job capable of being a green gate.** *(**Status 2026-08-11: the
    weekly-deep-gate half of this step is DONE** — precondition satisfied 2026-08-04, schedule
    shipped as PR #323 → `3b1160b`, with `visual-linux` executed rather than skipped on the
    schedule and compare-only enforced four ways. No scheduled run has executed yet;
    the 2026-08-17 target was forfeited by the #388 merge and the first clean
    schedule-event checkpoint is Monday 2026-08-24.)*

    > **Status 2026-08-14 — the release/tag pipeline half SHIPPED as Packet R1**
    > ([`release_pipeline/PLANNING.md`](release_pipeline/PLANNING.md), owner Gate 0 at
    > [§8.1b](#81b-third-sign-off-2026-08-14--the-releasetag-pipeline),
    > [`DECISIONS.md`](DECISIONS.md) ADR-007). `release.yml` runs `version-guard`,
    > `ci-provenance`, the frozen Windows build via a `workflow_call` reusable workflow
    > shared with `ci.yml`, the first-install and old-DB-migration smokes, and a fan-in
    > gate — all blocking. The build+smoke was extracted rather than copied, as F5-8
    > required; `deep-gate.yml` kept its own copy through R1, deliberately, because
    > editing it before 2026-08-17 would invalidate the first scheduled run.
    >
    > **Packet R2-b converts that copy** to the same `workflow_call` workflow, so F5-8 is
    > satisfied in full: one definition, three triggers (PR, release, schedule). It is
    > **merged 2026-08-16 as #388 (`949b15e`)**. It had been held from merge until a
    > scheduled run after 2026-08-17 03:17 UTC could be inspected under the pre-R2-b
    > workflow — a scheduled workflow executes the default branch's HEAD copy of its own
    > file — but that hold was **waived by explicit owner override on 2026-08-16, not
    > satisfied**: checklist rows 1–3 were never met. Consequently the 2026-08-17 run
    > executes R2-b's file and is **forfeited as clean evidence**; the first uncontaminated
    > schedule-event checkpoint is **2026-08-24**. **No scheduled run has executed at any
    > point — the `schedule` trigger has still never fired.** Design record,
    > preserved/changed behavior, residuals R-10 (discharged 2026-08-16 by dispatch
    > 31972476567)/R-11/R-12/R-13, and the full cost of the waiver:
    > [`release_pipeline/PLANNING.md`](release_pipeline/PLANNING.md), Packet R2-b section.
    >
    > **Its tag trigger is unproven.** The only validation route is `workflow_dispatch`
    > with `dry_run: true` (owner option (c)), and because `workflow_dispatch` requires
    > the file to be on the default branch, that dispatch runs *after* the packet merges.
    > The first genuine release tag is also the first execution of the trigger path —
    > [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) step 1 is the only compensation, and
    > it is a human one.
    >
    > **Phase 4 remains open.** §7.3 entry criteria 2 and 3 are **not** satisfied by
    > Packet R1: no visual job executes in the release gate (R1-D2 reuses the comparison
    > by provenance, R1-D3 keeps `visual-linux` out), and the fan-in behavior is proven by
    > static contract test rather than by a release dry run deliberately reddened. Both
    > remain to be discharged before Phase 4 can be marked complete. *(Measured 2026-08-02: this
    step's premise understates the problem. It is not one animated-logo failure — the **Linux**
    baseline set reds on **at least eleven** tests because 57 CSS/template commits landed after the
    baselines were frozen. Read [§8.7](#87-phase-4-stopgap-the-precondition-is-not-met-2026-08-02)
    before acting on this step.)* The current suite has a ledgered animated-logo failure above `maxDiffPixels: 800`; resolve it or encode a narrow, reviewable expected-difference oracle before requiring the job. Do not raise the global tolerance. Then define a tag/`workflow_dispatch` "release" pipeline that runs frozen-windows, first-install, old-db-migration, and visual compare as **blocking** steps, plus the 10-minute manual checklist below. Until then, add a weekly scheduled deep-gate run—but change `visual-linux` from `if: inputs.run_visual` to a condition that also runs on `schedule` (and release/tag events), because scheduled events supply no workflow-dispatch input and would otherwise silently skip visual comparison. Verify the scheduled run's required job set rather than treating an overall green workflow with skipped jobs as coverage. *(Fable 5, 2026-08-02: #262 has since put the frozen build + bootloader smoke on the PR path as the non-required `packaged-smoke-windows` job, so step 13's remaining scope is the release/tag pipeline, the visual precondition established in the bracket above, and that job's promotion; build the release gate by extracting the build+smoke into a `workflow_call` reusable workflow consumed by PR, schedule, and release triggers rather than authoring a third copy — §9.2 F5-8.)*

    > **Regeneration route — owner decision, 2026-08-02.** The stale Linux baselines are **not**
    > regenerated on `main`. PR #274 (Bootstrap 5.1.3 → 5.3.8) adds **86 `!important`
    > declarations** and **638 `--bs-*` custom properties** to `bootstrap.custom.min.css`, so any
    > baseline generated against 5.1.3 is invalidated the moment #274 lands — costing a second
    > review of the same 84 PNGs. The regeneration therefore runs **on the Bootstrap branch**, and
    > **#274 lands carrying its own baselines**, which discharges this precondition and the D3
    > stopgap together. Dispatch requires **both** inputs — `visual-linux` is gated
    > `if: ${{ inputs.run_visual }}` and `run_visual` defaults to `false`, so a bare
    > `gh workflow run deep-gate.yml --ref <branch>` runs the deep gate with **no visual job and
    > no baselines**:
    >
    > ```
    > gh workflow run deep-gate.yml --ref wt/bootstrap-538-compat \
    >   -f run_visual=true -f visual_mode=generate
    > ```
    >
    > Generate mode sets `--update-snapshots` and uploads the artifact
    > **`visual-baselines-linux`** (`e2e/__screenshots__/linux/**`, 14-day retention). CI never
    > pushes; the owner downloads, reviews and commits.
14. Decide the browser-matrix question **explicitly** (recommendation: stay Chromium-only for this single-user local tool, but record it as an ADR in `docs/DECISIONS.md` so it's a decision, not drift).

### Phase 5 — Periodic audits (not CI)
15. **Mutation testing** (`mutmut`) over `utils/` calculation modules, quarterly, as a suite audit. B1 is direct evidence this class of problem exists here; expect it to also flag weak pytest assertions. *(Fable 5, 2026-08-02: `mutmut` ≥3 is fork-based and does not run on Windows — this checkout's primary platform. Run it as a manually-dispatched Linux CI job on the deep-gate pattern, or pin the WSL route explicitly — §9.2 F5-2.)*
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
| D6 | `BACKUP_SCHEMA_VERSION` | *Recommendation (unchanged, for the record):* prefer defining and enforcing a compatibility policy; removal is only acceptable as an explicit DB/API contract migration, not a testing cleanup. **Owner decision 2026-08-14: retain-informational instead** — a reserved label, version-blind restore, bump-and-branch rule for the next payload change. Reason for the departure and the evidence behind it: [§8.1c](#81c-fourth-sign-off-2026-08-14--d6); recorded as ADR-008 |
| D7 | Auto-backup file snapshots: keep "no in-app restore" stance? | Keep, but document the manual recovery procedure in the README |

**Sign-off state (updated 2026-08-14):** D1 is signed as non-blocking measurement; D2 is signed for
`e2e-erase-flow` only; D3 is signed as the stopgap half and D5 as Chromium-only ([§8.1a](#81a-second-sign-off-2026-08-02--d3-and-d5));
D6 is signed as retain-informational ([§8.1c](#81c-fourth-sign-off-2026-08-14--d6)). **D4 and D7
remain unsigned** and no work may act on them. See [§8.1](#81-owner-sign-off-recorded-2026-08-01).

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

#### 8.1a Second sign-off (2026-08-02) — D3 and D5

The 8.1 table above is the **first** sign-off and is left unedited as the historical record of what
was authorized on 2026-08-01. This is the second.

| Decision | Ruling | Scope authorized |
|---|---|---|
| **D3** — release process: full pipeline or weekly scheduled deep-gate as stopgap | **Signed as the stopgap only.** Add a weekly scheduled deep-gate now; **defer the full release/tag pipeline** until the next packaged release is planned | Phase 4, step 13 — *stopgap half only* |
| **D5** — browser matrix | **Signed: stay Chromium-only, recorded as an ADR.** Shipped as [`DECISIONS.md`](DECISIONS.md) **ADR-004** | Phase 4, step 14 |
| **D2** (`js-unit` half) | **Still not signed.** Reconsider only after the documented two-week stability window, with evidence | — |
| **D4, D6, D7** | **Still not signed.** | — |

**Phases 2, 3 and 5 are not authorized by this sign-off**, and Phase 4 is authorized only as the
narrow stopgap above. **Phase 4 is not complete** — see [§8.7](#87-phase-4-stopgap-the-precondition-is-not-met-2026-08-02),
which records why the scheduled deep-gate could not ship with this slice.

#### 8.1b Third sign-off (2026-08-14) — the release/tag pipeline

This section's D3 row above defers "the full release/tag pipeline until the next packaged
release is planned". **That deferral is superseded by an owner Gate 0 sign-off on 2026-08-14**,
recorded in [`release_pipeline/PLANNING.md`](release_pipeline/PLANNING.md) Section 0. §8.1a's
own text is left unedited per its rule; this section is the supersession record.

Six decisions were signed, namespaced **R1-D1 … R1-D6** to avoid collision with this
document's D1–D7, and written up as [`DECISIONS.md`](DECISIONS.md) **ADR-007**. The blocking
question — how to prove the tag trigger without weakening the exact-tag invariant — was
answered **option (c)**: create no rehearsal tag, validate through `workflow_dispatch` with
`dry_run: true`, and leave the real tag path explicitly unproven until the first genuine
release.

**What this does NOT establish.** *No release tag has been pushed and none will be by this
packet.* The `push: tags` trigger in `release.yml` has never fired; what was validated is the
dispatch path and the guard logic beneath it. Nothing here bears on the weekly scheduled deep
gate, whose first scheduled execution is still due 2026-08-17 03:17 UTC.

#### 8.1c Fourth sign-off (2026-08-14) — D6

The three sign-offs above are left unedited as the historical record. This is the fourth. It
is independent of §8.1b — that section covers the release/tag pipeline, and its **R1-D6** is a
namespaced local label, not this document's D6.

| Decision | Ruling | Scope authorized |
|---|---|---|
| **D6** — `BACKUP_SCHEMA_VERSION` | **Signed as retain-informational.** The value is a reserved label; `restore_backup()` stays deliberately version-blind; structural compatibility remains owned by destination-column probing. Recorded as [`DECISIONS.md`](DECISIONS.md) **ADR-008** | Phase 3, step 11 — precondition only |
| **D4, D7** | **Still not signed.** | — |
| **D2** (`js-unit` half) | **Still not signed.** | — |

**This departs from §6's stated recommendation of A** (define and enforce a compatibility policy).
The reason is evidence that postdates the recommendation: the label had already failed to track a
real payload change — `superset_group` was added to `program_backup_items` in `6b99535`
(2026-02-05) with an `ALTER` migration but **without** bumping the constant introduced two days
earlier in `720cb0e`, and `create_backup()` writes absent columns as `NULL`, so rows labelled
version `1` already differ in shape. Enforcing a range over a label that was never maintained
enforces nothing, and the guard would sit on the disaster-recovery path where a false refusal is
worse than the silent mis-restore it prevents. Full analysis and the requirements brief:
[`backup_schema_version/PLANNING.md`](backup_schema_version/PLANNING.md).

**This authorizes the D6 precondition only.** Step 11's fuzzing work is not authorized by this
sign-off; it remains a separate packet.

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

### 8.5.1 Required-check promotion — the exact procedure used

Promoting a job is a **branch-protection API change**. Editing YAML does nothing, and renaming
the job actively breaks things. The procedure, for the next person who needs it:

```bash
# 1. READ the current list first. Never write one from memory.
gh api repos/{owner}/{repo}/branches/main/protection/required_status_checks --jq '.contexts'

# 2. APPEND the exact existing job name. Never replace the list —
#    other sessions' open pull requests depend on every entry already in it.
gh api -X PATCH repos/{owner}/{repo}/branches/main/protection/required_status_checks \
  -f 'contexts[]=<each existing context>' \
  -f 'contexts[]=E2E Erase Flow (Chromium, isolated, non-required)'

# 3. VERIFY on a real pull request that the context is both required and satisfied.
```

The context string is copied byte-for-byte from the job's `name:` field, parenthetical included —
even though that parenthetical is now false. See §8.3.

**Applied 2026-08-01**: nine contexts before, ten after. The tenth is
`E2E Erase Flow (Chromium, isolated, non-required)`. §7.3 entry criterion 3 is satisfied.

### 8.6 Execution log

**Phase 0 and Phase 1 are COMPLETE.** All seven pull requests merged on 2026-08-01. Numbers here
are **observed**, never carried over from the prose above — §4 B3 is the standing reminder that
hand-maintained counts drift.

| PR | Item | Squash | State |
|---|---|---|---|
| [#229](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/pull/229) | PR-0 — §8, D1 + D2(erase-flow) recorded as signed | `fe5917b` | ✅ merged |
| [#231](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/pull/231) | PR-1 — generated test inventory (Phase 0.1) | `037d98c` | ✅ merged |
| [#233](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/pull/233) | PR-2 — CI hardening (Phase 0.2) | `99c5a36` | ✅ merged |
| [#237](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/pull/237) | PR-3 — JS supply chain (Phase 0.3) | `11cb732` | ✅ merged |
| [#248](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/pull/248) | PR-4 — promote `e2e-erase-flow` (Phase 0.4) | `83958e5` | ✅ merged |
| [#253](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/pull/253) | PR-5 — Python coverage, non-blocking (Phase 1.5) | `bb4858e` | ✅ merged |
| [#254](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/pull/254) | PR-6 — JS coverage, report-only (Phase 1.6) | `70b8931` | ✅ merged |

#### Observed baselines

Every figure below was produced by CI on Linux unless noted. Regenerate rather than quote.

> **Historical snapshot — do not quote as current.** Every value in this table was
> copied by hand and has since drifted. The live figures are generated into
> [`test_inventory/TEST_INVENTORY.md`](test_inventory/TEST_INVENTORY.md). Read them
> there; do not transcribe a replacement here.

| Metric | Value (snapshot, superseded) | Source |
|---|---|---|
| Playwright tests | **541** across 30 specs | `TEST_INVENTORY.json` |
| Required functional gate | **426** across 24 specs | derived from `ci.yml` |
| pytest, deterministic subset | **1,994** across 92 files | `TEST_INVENTORY.json` |
| Hard waits (`waitForTimeout` lines) | **93** across 15 files | `TEST_INVENTORY.json` |
| **Python coverage** (`utils` + `routes`) | **87%** — 7,801 statements, 1,040 missed | `Run Tests`, PR #253 |
| **JS coverage** (statements) | **5.14%** — 375 / 7,293 | `js-unit`, PR #254 |
| JS modules at exactly 0% | **47 of 55** | `js-unit`, PR #254 |
| npm audit, full graph | **4 high** — `immutable`, `picomatch`, `postcss`, `fast-uri` | `js-supply-chain` |

**Python per-module**, for the future baseline-diff ratchet:
`utils/progression_plan.py` 98% · `utils/effective_sets.py` 96% · `utils/volume_ai.py` 100% ·
`utils/volume_export.py` 100% · `utils/volume_classifier.py` 97% · `utils/volume_taxonomy.py` 96% ·
`utils/volume_progress.py` 87% · `utils/program_backup.py` 83% ·
`utils/volume_splitter_service.py` 66% · `routes/program_backup.py` 68% ·
`routes/volume_splitter.py` 67%.
Weakest overall: `routes/filters.py` **49%**, `utils/python_version.py` 60%, `utils/logger.py` 64%.

#### Corrections to this document, found by executing it

1. **`utils/double_progression*` does not exist.** Phase 1 step 5 names it as a core module for
   coverage regression checks. There is no such file — only `tests/test_double_progression.py`. The
   double-progression logic lives in **`utils/progression_plan.py`** (98%), which the coverage
   summary reports instead. A regression check on a phantom module would have protected nothing
   while appearing to protect something.

2. **`app.py` has zero pytest coverage and cannot be measured today.** Coverage answers `--cov=app`
   with `Module app was never imported`. Its only import site is the `app_client` fixture at
   `tests/test_pattern_coverage.py:329`, which **no test in its class requests** — a dead fixture.
   So the startup sequence, middleware, error handlers and the erase route are invisible to
   coverage. This is blindspot **B2** surfacing independently in the coverage data. The scope is
   `utils` + `routes` for that reason.
   *Update 2026-08-02: stale — since #230/#258, `real_app_client` is a live, order-independent
   fixture consumed by `test_erase_data_guard.py`, `test_real_app_db_isolation.py`, and
   `test_static_cache_policy.py`, so `app.py` is imported on every full run and `--cov=app` is now
   feasible. See §9.1.*

3. **The pytest node count is not platform-invariant, and one file is why.**
   `tests/test_guard_destructive_command.py:58` parametrizes over the PowerShell hosts actually
   installed (`HOSTS = [n for n in ("powershell", "pwsh") if shutil.which(n)]`): 322 nodes on a
   Windows box with both, 163 on the ubuntu runner with `pwsh` only. That variance is the file's
   design — it exists because the guard passed under pwsh 7 while being a parser error under Windows
   PowerShell 5.1 — so the inventory models it via `ENVIRONMENT_DEPENDENT_PYTEST_FILES` and reports
   a deterministic subset instead of flattening the test. §7.3 entry criterion 1 is satisfied on
   that basis, not by pretending the raw total reproduces.

4. **`--omit=dev` is a false green here, quantifiably.** `npm audit --json` reports
   `dependencies: {prod: 1, dev: 246}`. Omitting dev scans **one package out of 246** and prints
   "found 0 vulnerabilities" for a graph carrying four high-severity advisories. sol5.6's P1 finding
   is confirmed with a number, and the reason is written into `ci.yml` beside the command.

#### Deviations from the plan as written

| Deviation | Why |
|---|---|
| The drift check reports via `::warning` and exits 0, rather than relying on `continue-on-error` alone | `continue-on-error` keeps a job from *blocking* but still paints a red ✗, which reads as failure to the other sessions — precisely the noise §8.4 promised not to create. "Measure-only" now means genuinely green. Flipping to blocking is `exit 0` → `exit $STATUS` |
| `cancel-in-progress` restricted to `pull_request` events | Tighter than asked. Superseded PR runs are cancelled (the B9 complaint), but a push to `main`/`develop` is never cancelled, so a merge always gets a complete pipeline |
| The npm audit job is also measure-only | Phase 0 step 3 requires a documented severity/exception policy before blocking, and that policy is not in this slice. All four current findings are transitive devDependencies of the build/test toolchain, so blocking today would halt every merge over code that never reaches a user |
| PR-4 verified on its own pull request rather than a throwaway | Protection was applied *after* #248 was green, then #248 was re-queried: `MERGEABLE` / `CLEAN` with the new context passing. That satisfies §7.3 criterion 3 on a real PR without extra noise |

#### Cross-session incident, 2026-08-01

`main` was red from `d453010` (app.py **P2**, #232) until `bd121c9` (#234). `Run Tests` is a required
context, so **every** pull request in the repository was unmergeable for the duration.

Root cause: a module-scoped `real_app_client` fixture that depended on `app.py` import order — **not**
trailing-slash behaviour, which the failing assertions superficially pointed at. P2 and P5 each
passed on their own pull request; the defect existed only with both on `main`. Session A fixed it in
[#234](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/pull/234).

The durable lesson is the one this document already argues elsewhere: **a green pull request is not
evidence of a green `main`** when several packets land in the same window. Nothing in the current CI
shape detects a cross-PR interaction before it reaches `main`.

#### Still open

- ~~**The inventory drift check is measure-only.**~~ **Discharged 2026-08-01.** WPB.4 merged
  (`9fe5dbd`, #256), completing §8.4's flip condition, and [#267](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/pull/267)
  `5b7a4f1` flipped the check to blocking and dropped its stale `(non-required)` suffix. The job
  summary prose that still described measure-only behaviour is corrected by
  [#271](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/pull/271).
  *(See [§9.1](#91-ground-truth-deltas--the-doc-rotted-within-hours) for what this closure —
  landing hours after the log was written — teaches about §8.6 as a hand-maintained ledger.)*
- **The npm audit job is measure-only**, pending the severity/exception policy (Phase 0 step 3).
- **No coverage ratchet exists.** Both numbers above are baselines, nothing more. Designing the
  baseline-diff (per `scripts/pyright_baseline_diff.py`) is future work; do not add a bare threshold.
- **`js-unit` stays non-required.** D2's js-unit half is unsigned, and the 2026-08-02 sign-off
  (§8.1a) explicitly kept it that way: reconsider only after the documented two-week stability
  window, with evidence.
- **D4 and D7 remain unsigned** (D6 signed 2026-08-14, §8.1c). Phases 2, 3 and 5 remain proposals. Phase 2 step 8 was
  delivered by APP_PY P1+P5 (§8.5). D3 and D5 were signed on 2026-08-02 (§8.1a); D5 shipped as
  ADR-004, and **D3's stopgap shipped 2026-08-11 as PR #323 (`3b1160b`)**.
- ~~**The Linux visual baseline set is stale, and it blocks the Phase 4 stopgap.**~~
  **Resolved 2026-08-04** — regenerated, owner-reviewed, eight consecutive clean compares; the
  stopgap then shipped 2026-08-11. §8.7 is retained as the diagnosis of the original condition.

### 8.7 Phase 4 stopgap: the precondition is not met (2026-08-02)

> **CLOSED 2026-08-11 — this section is history, not current state.** The precondition was
> satisfied 2026-08-04 (the Linux baselines were regenerated and reviewed; eight consecutive
> clean compares). The owner approved the schedule on 2026-08-11 and **PR #323 shipped it,
> squash-merged as `3b1160b`** — every clause of the *Ordering* paragraph at the end of this
> section was discharged in that one change. **Do not re-run the unblock sequence, and do not
> read the measurements below as today's state.** What is *not* yet established: no scheduled
> execution has happened. *(Written when the first authoritative run was **2026-08-17
> 03:17 UTC**. Superseded by the #388 merge of 2026-08-16: that run now executes R2-b's
> file and is contaminated, so the first uncontaminated checkpoint is **2026-08-24**.)* It
> must show **all seven jobs with `visual-linux` executed rather than skipped** — the job
> set, not the overall green, is the thing to verify.

D3's stopgap was signed, then **not shipped**, because Phase 4 step 13's own precondition —
*"make the visual job capable of being a green gate"* — is currently false. This section records the
diagnosis so the next session does not re-derive it.

**What was measured.** Deep-gate run
[30722690389](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/actions/runs/30722690389) on
`44fe838`, and the prior run `30721970863` on `d49cc80`, both `workflow_dispatch` with
`run_visual=true`, `visual_mode=compare`.

| Deep-gate job | Result |
|---|---|
| Full E2E incl. accessibility (Chromium) | pass |
| First install (catalog seed) smoke | pass |
| Empty-schema initializer smoke | pass |
| Old-DB migration compatibility | pass |
| Frozen executable (real bootloader, Windows) | pass |
| Dependency Health Check | pass |
| **Visual regression (Linux baselines)** | **fail** |

`visual-linux` is the **only** failing job, in both runs. Tally: **11 failed, 57 passed, 16 did not
run** (the suite is serial; the 16 unrun tests mean 11 is a **floor**, not the true red count).

**The failures are not the ledgered pair.** `MASTER_HANDOVER.md`'s *"Known Windows visual reds"*
ledger describes **two** Windows reds. This is the **Linux** baseline set, and it reds on at least
eleven tests spanning nearly every page:

| Snapshot | Observed diff (px) |
|---|---:|
| `welcome-desktop-light` | 807 |
| `workout-plan-desktop-light` | 989 → 93,671 across attempts |
| `workout-plan-desktop-dark` | 821 → 55,531 |
| `plan-desktop-light-advanced` | 6,539 → 25,673 |
| plus `workout-log` light/dark, `weekly-summary`, `session-summary`, `progression`, `body-composition`, `volume-splitter` | above the 800 px oracle |

**Root cause — corrected 2026-08-02 after a full review of all 74 differing images.** The first
version of this paragraph said the baselines "were last written by `46e340e`" and attributed the
reds to the CSS arc plus the later Bootstrap 5.3 upgrade. Both claims were wrong, and the
measurement that corrects them is recorded here so the error is not re-derived.

**Baseline provenance is mixed, not single-vintage.** Of the 84 committed PNGs, **66 date from
`04b9819` (2026-06-06)**, 12 from `ab9dc7b` (2026-07-17) and 6 from `46e340e` (2026-07-27). The
"last written by `46e340e`" claim holds for 6 files.

**The Bootstrap upgrade is excluded as the cause.** Deep-gate visual was **green** on `894d882`
(2026-07-27 17:10, run 30288077299) and **first red** on `7685e2b` (2026-07-31, run 30663355864),
which failed on `visual-linux` alone with every other deep-gate job passing. Bootstrap 5.3 (#274,
`4435b04`) landed 2026-08-02 — *after* the breakage. The first failure therefore originates inside
the **`894d882..7685e2b`** bracket, which is WP4.4 cascade-cleanup work. Bootstrap and sass do
change rendering broadly and stale the set further, but they did not start it.

**Three distinct causes are mixed in the diffs**, and they carry different verdicts:

| # | Cause | Images | Verdict |
|---|---|---:|---|
| a | Bootstrap 5.3 / sass restyling — navbar glyph metrics, `form-range` tracks, button fills, border-radius | 58 | expected |
| b | `b5e837d` (#88) gives uncurated exercise rows a search icon instead of a play glyph; the 2026-06-06 baselines predate it | — | expected feature drift |
| c | card-mode table separators moved from `currentColor` ink to the declared `--tbl-border-color` | 16 | **cascade correction, inadequate token** |

**(c) is the one that mattered.** Sampling the separator on both themes shows the committed
baselines painted it at `currentColor` — `#0f1220` on light, near-white on dark, i.e. the *text*
colour — while the candidate paints the declared token exactly (`#d0d0d0` / `#374151`). No token,
document or test ever sanctioned an ink-coloured separator; the WP4.4 cleanup removed the
higher-weight rule that had been supplying that paint, so the rendering became **correct** by
design intent. The contrast, however, fell from 18.6:1 / 11.0:1 to **1.54:1 / 1.21:1**, and in card
mode that token is the only divider between label/value pairs inside a row card. So the cascade
correction and a latent token-contrast defect surfaced in the same change, and nothing in the suite
caught either. Corrected separately by raising `--tbl-border-color` to `#7d839d` (light) and
`#7a8099` (dark) — both from the `--ink-3`/`--ink-2` neutral family — with
`tests/test_css_wp4_4_layout_contracts.py::test_table_separator_clears_non_text_contrast` enforcing
a 3:1 floor against every surface the separator meets. **No baselines may be approved from a run
that predates that correction.**

**Why this slice did not ship the schedule.** Adding the weekly cron now would create a job that
reds every week from its first run, which trains the owner to ignore it — the precise failure mode
the plan's *"verify the scheduled run's required job set"* instruction exists to prevent. The
alternative, scheduling the deep-gate with `visual-linux` still skipped, is the false-green that
step 13 explicitly forbids.

**The unblock is an owner action, by design.** It is a baseline regeneration
(`workflow_dispatch` → `run_visual=true`, `visual_mode=generate`), followed by downloading the
`visual-baselines-linux` artifact, **reviewing 84 PNGs by eye**, and committing them. The workflow
is built so CI never pushes pixels: *"every pixel change is committed by a human after downloading
and inspecting this artifact."* That review is also the only thing that can separate expected
CSS-arc drift from a genuine regression hiding inside these eleven — a distinction this diagnosis
**cannot** make from pixel counts alone, and deliberately does not claim to.

Three things were considered and rejected as out of authorization: updating snapshots, rebaselining
the known reds, and raising the global `maxDiffPixels: 800`.

**Ordering, once baselines are refreshed.** *(Discharged 2026-08-11 by PR #323 → `3b1160b`: the
compare was confirmed green first, and the `schedule:` trigger, the `visual-linux` `if:` fix, the
`compare` default and both prose corrections landed together in that change. Retained as the
specification it was written to be.)* Re-run compare and confirm green *first*; only then add
the `schedule:` trigger, and in the same change fix `visual-linux`'s `if: ${{ inputs.run_visual }}`
— a `schedule` event supplies no `inputs`, so the job would silently skip — and default
`visual_mode` to `compare` so a scheduled run can never enter `generate` mode. Note also that
`deep-gate.yml`'s header comment and `docs/archive/ci_cd/CI_CD_IMPROVEMENT_PLAN.md` §0 both state
*"do not schedule cron jobs for this repo"*; D3 reverses that older decision, so the comment must be
updated in the same PR or the workflow will contradict itself.
- **Dependabot is now live** and opened ~14 pull requests on first run. The per-ecosystem limit is 5
  and npm/actions minor+patch are grouped, but the first sweep is unavoidably large because nothing
  had ever been updated. Expect the steady-state weekly volume to be far smaller.

---

## 9. Fable 5 review (2026-08-02)

**Reviewer identity:** `claude-fable-5`
**Review type:** independent post-execution review, one day after the Phase 0–1 slice shipped.
Every claim below was re-verified against the live repository on 2026-08-02 (`ci.yml`, branch
protection via `gh api`, `.gitignore`, `utils/auto_backup.py`, `package.json`, `tests/`,
`e2e/fixtures.ts`); read-only except for this document.
**Disposition:** the ordering principle (§5 — make the suite honest before making it bigger) is
correct, and nothing below argues for reordering. What this pass adds: (a) the document had
drifted from ground truth **within hours** of its last update, including one blindspot that
partially closed itself; (b) implementation-level blindspots in Phases 1–5 that Opus 5, Codex,
sol5.6, and the executing session all missed. Small in-place amendments are marked
*(Fable 5, 2026-08-02: …)*; everything heavier awaits owner selection.

*Corrected at owner review, 2026-08-02: this disposition originally carried a third claim — that
**F5-1** was "one non-test finding that is the highest harm-per-effort item currently in this
file." **F5-1 was factually wrong and has been retracted**; `.gitignore:29` already ignores
every snapshot, and the real defect is two WAL sidecars, tracked at `LEFTOVERS_BY_PRIORITY.md`
P1.7. The claim is struck rather than re-ranked. Note also that **D3 and D5 were signed on
2026-08-02** (§8.1a) — the original wording "awaits owner selection alongside D3–D7" predated
that and has been narrowed.*

### 9.1 Ground-truth deltas — the doc rotted within hours

| Claim (written 2026-08-01, PR #255) | Reality, verified 2026-08-02 |
|---|---|
| §8.6 "The inventory drift check is measure-only… flip only when WPB.4 has [merged]" | WPB.4 merged the same evening (#256, `9fe5dbd`); #267 (`5b7a4f1`, 22:30) flipped the check to blocking and added **`Test Inventory Drift` as the 11th required context** — applied via the §8.5.1 read-first procedure. Closed. |
| B8 "The shipping artifact is never tested on the PR path" | #262 added `packaged-smoke-windows` to `ci.yml`: real `pyinstaller --clean` build + real bootloader smoke (port 5123, deliberately ≠ 5000) **on every PR**, non-required by design pending green accumulation (the `e2e-fatigue-context` promotion precedent, per the job's own comment). B8's remaining substance: the promotion decision, the absent release/tag pipeline, and visual compare still manual-only. |
| §8.6 correction 2: "`app.py` has zero pytest coverage **and cannot be measured today**" | Stale. Since #230/#258, `real_app_client` is a live, order-independent fixture consumed by three test files; `app.py` is imported on every full pytest run. Adding `--cov=app` to the coverage job is now feasible and closes the measurement blind spot that correction described. |
| `.claude/rules/testing.md:22` names the job "`Test Inventory Drift (non-required)`" | The suffix was dropped in #267 and the job is required. One more B3-class prose drift; fix in the next docs PR. |

**Meta-finding.** §8.6's "Still open" list is a hand-maintained **status** ledger inside a
planning document. B3's lesson was applied to *counts* (generated inventory) but not to *status
claims* — and two of the list's five bullets were wrong before the calendar day ended. Treat §8.6
as the dated point-in-time record it is; answer "what is open now" only with ground-truth queries
(`gh api …/required_status_checks --jq '.contexts'`, the drift step's `exit` line in `ci.yml`,
`/status`), never by reading this file.

### 9.2 New findings

**F5-1 — two WAL sidecars in `data/auto_backup/` are unignored. *(Corrected at owner review,
2026-08-02 — the original finding was wrong and is retracted.)***

**What this finding first claimed, and why it was wrong.** It asserted that `data/auto_backup/`
is not gitignored at all and that the full database snapshots are *"one `git add` away"* — a
directory-wide privacy exposure — and proposed ignoring the whole directory. That is false.
`.gitignore:29`'s bare `*.db` pattern is **not** path-anchored, so it already matches every
snapshot at any depth. Verified by `git check-ignore` over all nine files in the directory:

| File | Verdict |
|---|---|
| `database_20260704_004339.db` · `…20260711_172725.db` · `…20260711_213123.db` · `…20260711_215217.db` · `…20260712_000549.db` · `…20260722_044704.db` · `…20260724_034925.db` | **IGNORED** (7 of 7) |
| `database_20260712_000549.db-shm` | **UNIGNORED** |
| `database_20260712_000549.db-wal` | **UNIGNORED** |

**No snapshot of the live database is exposed.** The directory shows as `?? data/auto_backup/`
in `git status` only because git collapses a directory containing *any* untracked file — here,
the two sidecars. Reading that line as "the snapshots are untracked" is the error that produced
this finding, and it is the same class of mistake as trusting a hand-maintained status ledger:
a summary display was read as a per-file fact.

**The real finding, correctly scoped.** Exactly two files are unignored: the `.db-shm` and
`.db-wal` sidecars of `database_20260712_000549`. They are WAL journal sidecars, not snapshots.
The fix is **sidecar-scoped**, not directory-wide.

**`docs/LEFTOVERS_BY_PRIORITY.md` P1.7 has this right and supersedes this entry** — it scopes
the fix to `*.db-shm` / `*.db-wal`, and its §3 hold-table deliberately **protects**
`data/auto_backup/*.db` as *"Real recovery snapshots; retention/rotation owns them."* Ignoring
the whole directory as originally proposed would have fought that protection for no gain.
**Track the fix at P1.7; this entry stands only as the retraction.**

**F5-2 — Phase 5's mutation-testing tool does not run on the owner's machine.**
`mutmut` ≥3 is fork-based and unsupported on Windows; this checkout is Windows-first. "Quarterly
mutmut audit" as written would silently become *never*. Run it as a manually-dispatched **Linux CI
job** (deep-gate is already the template for exactly this shape) or pin the WSL route explicitly.
Intent unchanged; only the venue moves. *(Amendment applied at Phase 5 step 15.)*

**F5-3 — Phase 3's Hypothesis step is missing its operational preconditions.**
(a) Hypothesis writes its example database to `.hypothesis/` in the CWD by default — a
repository-root artifact, which ADR-002 forbids; point it under `artifacts/` or set
`database=None` in CI. (b) `Run Tests` is a required check with **no retry** (§2.2), and
Hypothesis generation is randomized by design; register a CI settings profile with
`derandomize=True` and `deadline=None` (shared-runner timing variance), keeping randomized
exploration for local or scheduled runs — otherwise step 10 introduces the suite's first
nondeterministic required-path failures, the exact class §2.2 flags as un-retryable. (c) Hypothesis
tests collect as single pytest nodes, so the now-blocking inventory gate is insensitive to example
counts — but every Phase 2–5 test add/remove must regenerate
`docs/test_inventory/TEST_INVENTORY.json` in the same PR, which no phase currently says.
*(Amendment applied at Phase 3 step 10.)*

**F5-4 — Phase 2 will turn required jobs red, and the plan doesn't sequence for it.**
Repairing assertions that "cannot fail" (B1) and unsuppressing console errors (B4) surfaces
whatever the vacuity and suppression have been masking — real contrast violations, real
null-dereferences — and `accessibility.spec.ts` runs inside the **required** functional shards.
Landing repairs directly can block every PR the day they merge. The repo already owns the correct
pattern and Phase 1 uses it: **measure → baseline → ratchet.** Run axe and the strict fixture in
report-only mode first, size the debt, triage into fix-now vs. per-spec allowlist entries with
issue links, then flip to asserting. Budget for *app-side* fixes (theme contrast tokens, null
guards), not only test edits — those are user-visible changes that take the normal review path.
*(No amendment applied — this materially reshapes Phase 2's steps and belongs to the owner's
Phase 2 selection.)*

**F5-5 — Design the coverage ratchet as a per-PR diff gate, not a baseline-total comparison.**
The planned committed-baseline + per-core-module floors (Phase 1, per the pyright pattern) still
admits the classic global-ratchet failure: new untested code in one module hides behind deletions
or unrelated test adds elsewhere, and per-module floors punish refactors that legitimately move
code across module boundaries. A diff-coverage gate (`diff-cover` consumes the `coverage.xml` the
job already emits plus the PR diff; the same tool reads LCOV for the JS side) asserts the thing
actually wanted — *new and changed lines are tested* — needs no stored baseline, and hands the PR
author a local, actionable number. Recommendation: diff coverage as the blocking primitive, with
the per-core-module floors kept as the safety net for `utils/effective_sets.py`-class modules.
None of the four prior reviews considered it. *(Amendment applied at Phase 1 step 5.)*

**F5-6 — Phase 3 step 12 has a cheaper migration path than it implies.**
Vitest honors a per-file `// @vitest-environment jsdom` pragma, so DOM-module tests adopt jsdom
file-by-file with the global `environment: 'node'` (and the 9 existing green files) untouched.
`jsdom` 29 is already in `devDependencies`. *(Amendment applied at Phase 3 step 12.)*

**F5-7 — The npm-audit flip mechanism is undesigned, and Dependabot changes the picture weekly.**
Phase 0 step 3 requires a "documented severity/exception policy" before blocking, but nothing
defines how a *new* advisory is distinguished from the four standing highs — all transitive
devDependencies that Dependabot's grouped updates may clear or churn at any time. Without a
committed allowlist, the job's only futures are "measure-only forever" or "block with four
standing reds". Concrete form of the missing policy: commit an advisory allowlist keyed by
advisory ID with expiry dates (the pyright-baseline pattern yet again); the job fails only on
advisories not in the file.

**F5-8 — Phase 4 should reuse the PR-path build, not author a third copy.**
`ci.yml`'s packaged-smoke job comment already mandates keeping *two* build definitions in step
(`ci.yml` ↔ `deep-gate.yml`). A release pipeline written as a third copy triples that sync burden.
Extract the build+smoke into a reusable workflow (`workflow_call`) consumed by all three triggers —
PR, schedule, release/tag — so Phase 4's blocking release gate is the same tested definition that
runs daily, and §7.3's fan-in dry-run proves one artifact instead of three. *(Amendment applied at
Phase 4 step 13.)*

### 9.3 In-place amendments applied by this pass

Beyond the *(Fable 5, 2026-08-02: …)* notes at Phase 1 step 5, Phase 3 steps 10 and 12, Phase 4
step 13, and Phase 5 step 15, plus the dated updates inside B8 and §8.6:

1. §1.2's "Skip load testing" row referenced **§4 B17**, which does not exist — the blindspot list
   ends at B14 and the latency-assertion content is **B13**. Corrected.
2. §2.2 "freegun" → "freezegun".

Nothing else was altered: the §1–§4 adjudications, the §6 decision table, and the §7 sol5.6 record
stand as written.

**Sign-off status — corrected at owner review, 2026-08-02.** This section originally closed
*"D3–D7 remain unsigned; Phases 2–5 remain proposals."* The first half is **superseded**:
**D3 and D5 were signed on 2026-08-02** and are recorded in **§8.1a**, which governs. D5 shipped
as `DECISIONS.md` **ADR-004** (Chromium-only); **D3 was signed as the stopgap half only**, and
that stopgap was blocked on the stale Linux baseline set (**§8.7**) — *updated 2026-08-11: the
baselines were regenerated and reviewed on 2026-08-04, and the stopgap **shipped** as PR #323
(`3b1160b`); §8.7 is now history.* *(updated 2026-08-14: D6 signed as retain-informational, §8.1c.)* **D4 and D7
remain unsigned**, as does the js-unit half of D2. **Phases 2, 3 and 5 remain proposals, and
Phase 4 is not complete** — *updated 2026-08-14: its release/tag pipeline half **shipped** as
Packet R1 (§8.1b), but Phase 4 stays open because §7.3 entry criteria 2 and 3 are unmet and
R1's tag trigger has never fired.*
