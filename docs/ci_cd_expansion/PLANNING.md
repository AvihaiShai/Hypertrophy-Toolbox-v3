# CI/CD Expansion — Planning

| Field | Value |
|---|---|
| Status | **FORMAL CORE Plan v2 approved at owner Gate 1, 2026-10-19, including all five accepted findings. B1 only authorized and claimed.** Other packets require later execution authority; delivery council/Gate 1 remain separate. |
| Authors | Historical draft: Claude and Astra, 2026-10-18. Formal council document owner: `product-manager` `/root/product_manager`, 2026-10-19; read-only manager `/root`. |
| Source of truth | This file. The chat threads that produced it are not. |
| Baseline measured | `origin/main` `7ac1af2d`, CI run `39125460089`, 2026-10-18 |
| Planning size | Large (new workflows, new jobs, repo-settings changes) — per `docs/ai_workflow/QUALITY_GATE.md` plan-stage routing: Gate 0 → council (`/council-plan`) → Gate 1 → implementation |
| Branch / PR | `ci/b1-action-pins`; PR pending |

### Review log

| Date | Reviewer | Kind | Disposition |
|---|---|---|---|
| 2026-10-18 | Astra | Preliminary peer review of v1 (not council) | 8 points: all accepted or adjusted, see §10. Five factual corrections folded into §0–§2. |
| 2026-10-19 | Owner | Gate 0 decision | Approved the complete CI-D1–CI-D11 package in §§11.4–11.8 with §11.9 boundaries; request quoted in §1. No implementation or settings authority. |
| 2026-10-19 | `/root/product_manager` | Formal core council Step 1 | Reconciled §§0–9 and drafted §12 Plan v1. Formal reviewers, response matrix and Plan v2 pending. Historical consultations receive no formal-council credit. |
| 2026-10-19 | `/root/architecture_reviewer`, `/root/test_strategist`, `/root/product_risk_reviewer` | Formal independent council Step 2 | All completed; AR-1/AR-2 and TS-1/TS-2/TS-3 recorded verbatim in §12.2; product-risk review returned no findings. |
| 2026-10-19 | `/root` → resumed `/root/product_manager` | Formal Steps 3–4 | Manager proposed acceptance of all five findings; same PM wrote §12.3 matrix and §12.4 Plan v2, completed provenance, and reconciled operative §§0–9. No reject/defer or repeated review pass. |
| 2026-10-19 | Owner | Core Gate 1 and B1 execution | Approved §12.4 including the five accepted findings; authorized B1 implementation, gates, independent code-reviewer, push and ready PR. Stop before merge; §13 records execution. |

---

## 0. Operating protocol — reconciled 2026-10-19

Other sessions share this repository; preserve their changes. The council originally owned only this planning document. The owner subsequently approved core Gate 1 and authorized B1 alone; §13 records that authority. The following controls apply to implementation; they do not authorize any other packet.

1. **Nothing in §4 starts before its applicable Gate 1 and execution authority.** Gate 0 was approved 2026-10-19 for requirements and formal core planning only. Formal core council and owner Plan v2/Gate 1 approval are complete; only B1 has execution authority in this session. F1/F3 require their own scoped delivery council/Gate 1. §10 and §11 consultations are advisory evidence, not formal reviews. Q4/D2, credentials, spending, settings, PR merge and publication remain separate owner actions.
2. **Claim before you start.** Write your name and the date in the §7 ledger row. One packet is one PR. Two agents never hold the same packet.
3. **Isolated implementation copies.** Follow `docs/ai_workflow/PARALLEL_WORKFLOW.md` and `scripts/new-worktree.ps1` before parallel work touching tests, DB or dev servers, preserving the Operation A hold. Read-only council reviewers and one planning-document writer need no DB/worktree activity. Never stash, reset or incorporate another session's changes.
4. **One `ci.yml` PR in flight at a time.** Proposed order: B1 → A1 → B2 → B3 → A2 → A3 → G6 → G7; B4 may follow any merged slot after A1, but **must never delay B1**. E1/D3 and promotion-contract packets also serialize whenever they touch the same workflow. Each starts from current `origin/main` after the prior merge; merges require owner authority. B2/B3/G6/G7 priorities may move between free slots without weakening their dependencies or gates.
5. **Evidence is tied to a commit.** Every ledger number names the PR head SHA and the run id it came from. A reviewer that did not run is `incomplete`, never `no findings`.
6. **Reuse sufficient evidence; refresh only what the packet changes.** §2 remains the dated audit at `7ac1af2d`; manager confirmed the existing `origin/main` ref still matches that SHA on 2026-10-19 without a new live audit. New implementation evidence records tested SHA, run/event/attempt, exact job/step, executed identities, and current settings snapshots where relevant.
7. **Never rename a protected check in isolation.** Preserve §2.3's exact twelve names and all adopted composite caller/child names. §11.5 defines distinct PR/release target sets; PR-only B3 is never demanded from a `main` release carrier. Preserve trusted-app binding `app_id: 15368`, exact-SHA and newest-run release checks.
8. **Agents never change repository settings or branch protection.** Agents prepare the §6 commands; the owner runs them.
9. **Each future PR runs the union of its change-type gates.** Workflow edits require full `pytest` + `code-reviewer`; adding/removing/converting jobs also requires `architecture-reviewer`. Script edits derive real coverage by stem/directory-token search, with `/verify-suite` for the required exceptions or uncovered changes; any Python edit also runs the pyright baseline diff. Inventory regeneration follows the canonical drift triggers, with installed dependencies and no stray globbed Markdown. The present product-doc-only council runs no tests.
10. **No PR work, push, merge or release is authorized by this council request.** Later PR handling follows separately authorized scope; merging requires a separate owner message naming the PR and saying "merge". Settings and release tags remain owner-run.
11. **Do not re-litigate** the decisions in §1.4.

---

## 1. Section 0 — Requirements brief

**Raw request (verbatim, owner, 2026-10-19):**

> Continue the GitHub Actions / CI-CD expansion plan.
>
> Read CLAUDE.md, docs/ci_cd_expansion/PLANNING.md, and the planning workflow in docs/ai_workflow/QUALITY_GATE.md and .claude/commands/council-plan.md.
>
> I approve the complete CI-D1–CI-D11 Gate 0 requirements package in §§11.4–11.8, with the approval boundaries in §11.9.
>
> Run the formal /council-plan workflow for the core milestone:
> 1. Have product-manager record this Gate 0 approval and reconcile the earlier requirements, packets, sequencing, settings commands, and ledger with the approved package.
> 2. Run the architecture-reviewer, test-strategist, and product-risk-reviewer independently. The earlier advisory consultations do not count as formal council reviews.
> 3. Have product-manager record every finding and disposition, actual agent provenance, and the revised plan.
> 4. Present the completed plan for my separate Gate 1 approval.
>
> Keep delivery under its separate scoped council/Gate 1. Preserve conditional promotion requirements, separate PR/release enforcement sets, and the rule that B4 measurement must not delay B1 hardening.
>
> This approves requirements and council planning only. It does not sign JS Unit Q4/D2, authorize implementation, change repository settings, supply credentials, approve spending, merge PRs, or publish releases.
>
> Preserve other sessions’ changes and reuse existing evidence where sufficient.

### 1.1 Problem

- **Slow for the wrong reason.** 31.4 min wall is one job, and 92% of that job is one test file. Every PR waits on it.
- **Merge integrity relies on luck.** Required checks need no up-to-date base. Two green sibling PRs have already broken `main` once.
- **The repo-settings security layer is off.** Secret scanning, push protection and CodeQL are free on this public repository and all disabled. Actions are tag-pinned; any action is allowed.
- **The dated audit found seven consecutive failed weekly Deep Gates.** The approved requirements now select bounded option A plus separation E, preserving the one-capture hypothesis and all other unresolved captures; execution remains gated. There is no deterministic tracking mechanism in the audited baseline.

Core also needs bounded advisory review, enforced destinations for skipped tests and retry visibility. Traceable artifact delivery is a separate milestone.

### 1.2 Goals

| ID | Goal | Success measure |
|---|---|---|
| G1 | Shorter PR feedback | Creation-to-required-gate completion: 12–15 min initial objective, eight-minute measured second-stage target, six-minute stretch; include queue time and runner-minutes. §2's 31.4-minute job-dominated wall is dated evidence, not a current latency median. |
| G2 | Merge integrity | `strict: true` on `main`. Merge queue evaluated as a separate decision (needs an org-owned repo). |
| G3 | Security layers | Secret scanning/push protection and CodeQL configured; baseline triaged; native CodeQL rule blocks newly introduced High/Critical alerts with seeded proof and explicit owner bypass. Every adopted action/dependency is SHA-pinned and explicitly allowlisted with both broad flags false. B2 always runs on PR/main; B3 enforces PR dependency changes. |
| G4 | Distinct enforcement sets preserve intent | Conditional promotions follow §11.5. Code/contracts declare `PR_REQUIRED_CONTEXTS` (target 18) separately from `RELEASE_EXPECTED_CONTEXTS` (target 17); owner applies only qualified PR checks with app binding. Existing enforcement never weakens; Q4/D2 remains unsigned. |
| G5 | Scheduled-gate observability | Any non-success completion of either Deep Gate workflow upserts a tracking issue within 1 h; a missing scheduled run is detected within 36 h. Visual-linux owner decision (GATE1 A–D) taken. |
| G6 | Bounded agentic review | After separate owner OAuth/app authorization, ten completed fresh-head reviews of eligible human same-repo code/workflow PRs, 15 min/20 turns, existing subscription quota only, no paid fallback. Failed/stale/skipped attempts are visible and do not count. |
| G7 | Separately gated delivery direction | F1 candidate artifact → F3 upgrade/recovery → publication; same final ZIP throughout, genuine exact version tag only, dispatch nonpublishing. Separate delivery council/Gate 1 and owner timing; no delivery work in core. |
| G8 | Test effectiveness | Guard identities preserved; six Windows-host and three dependency cases execute in enforced destinations; first-attempt E2E failures visible. Branch/patch coverage stays non-blocking; broader expansion deferred. |

### 1.3 Non-goals

No application/runtime, schema, API, calculation, catalog, backup-startup semantics or visual-baseline changes. No auth/cloud sync/telemetry. No canaries, blue/green, feature flags, production DAST/load tests, Lighthouse blocker or browser expansion beyond Chromium (ADR-004). Core excludes delivery/signing, organization transfer/merge queue, docs filtering, optional browser cache, B5 scanner expansion, mutation/coverage expansion and second AI reviewer.

**Acceptance criteria:**
1. Given this explicit approval, Section 0 records CI-D1–CI-D11 Gate 0 as approved and preserves every §11.9 boundary; the three independent formal reviewer outputs, actual IDs, findings/dispositions and Plan v2 are present before Gate 1 is requested.
2. Given later authorized core execution, speed evidence includes creation-to-required-gate completion, queue/job duration, runner-minutes and unchanged executed test identities; existing required gates fail closed through every split and promotion.
3. Given a qualification or security-control gap, its promotion/activation remains blocked individually; unrelated hardening proceeds under its own gates. B4 never blocks B1, A2 never blocks packaged smoke, and Linux diagnosis never blocks Windows visual.
4. Given a non-success or missing weekly run, deterministic monitoring reports each watched workflow within the approved one-hour/36-hour bounds; previous-week/manual runs cannot satisfy freshness.
5. Given the pilot has no authorized credentials, stale review behavior or exhausted subscription quota, it stays disabled/incomplete without paid fallback or any effect on merge authority.
6. Given a future delivery proposal, its scoped council/Gate 1 checks exact-ZIP recovery before publication and exact version tags; this core approval does not authorize it.

**Calculation surface:** `none`. No hypertrophy formulas or production semantics change. Any later packet introducing such changes returns to requirements and the appropriate migration/test gates.

**Assumptions:** The dated baseline and bounded qualification evidence are sufficient for council design; packet activation rechecks only relevant drift. Proposed agent owners are scheduling suggestions, not assignments. Requirements approval does not imply owner execution, credentials, spending or implementation.

**Open questions:** None blocking formal core planning. Owner-only future actions remain explicit: core Gate 1; JS Q4/D2; individual settings/promotion activation; OAuth/app authorization; named diagnostic execution; separate delivery council/Gate 1 and release timing. Deferred work needs its own decision, not an inferred answer here.

### Section 0 sign-off — GATE 0

- [x] Owner confirms acceptance intent by approving the complete §§11.4–11.8 package, 2026-10-19.
- [x] Package assumptions, conditional evidence and §11.9 exclusions accepted as requirements; no additional execution authority inferred.
- [x] No blocking requirements question remains for the formal core council. Deferred owner actions above remain unsigned.

### 1.4 Standing decisions this plan does not reopen

| Decision | Where | Meaning here |
|---|---|---|
| D-6 | `docs/NPM_AUDIT_SEVERITY_POLICY_DECISION.md` §6.1 | Dependabot **security updates** stay OFF. Dependabot **version-update** PRs still arrive automatically; acting on a security *alert* is a human-opened PR. |
| D1 | `ci.yml` test job comment, 2026-08-01 | Coverage is non-blocking measurement. This plan adds `--cov-branch` and, later, measure-only patch coverage; no absolute threshold. |
| ADR-006 | `docs/DECISIONS.md` | Same-machine *local* Playwright sharding rejected. Cross-runner CI matrix sharding is unaffected and in use. |
| ADR-007 | `docs/DECISIONS.md` | Release provenance reuses exact-SHA CI. Separate delivery will require an amendment and F1 candidate → F3 recovery → publication; exact `^v\d+\.\d+\.\d+$` tags only, dispatch nonpublishing. No publication authority here. |
| ADR-011 | `docs/DECISIONS.md` | 81 byte-gated visual captures + 5 semantic exemptions. No packet changes tolerances, masks or exemptions. |
| False `(non-required)` names | `ci.yml` comments; `scripts/release_gate.py` | **Three** required contexts carry the suffix: E2E Fatigue Context, E2E Erase Flow, JS Supply Chain. Load-bearing; never rename. |
| `braces` / #513 | `docs/BRACES_REMEDIATION.md` | Closed by #519. |

---

## 2. Verified baseline — 2026-10-18

### 2.1 Pipeline shape

| Item | Value |
|---|---|
| Workflows | `ci.yml` (19 jobs) · `deep-gate.yml` (7 jobs; cron `17 3 * * 1`, observed start 09:47–10:50 UTC, i.e. 6.5–7.5 h late; ~19 min) · `release.yml` (tag-triggered; 2 manual rehearsals; never a real tag; **gates only, publishes nothing by design**) · `_packaged-windows.yml` (reusable: build + smoke; **exports no artifact**) |
| Orphan | "V1 Probe (THROWAWAY - dropCompositingHints stability)" id `345538425`, `active`, file not on `main` |
| Run wall | 31.4 min (31 m 23 s) |
| Critical path | `Run Tests` 31.3 min; `tests/test_guard_destructive_command.py` = 28.2 min (1,018 cases, one `pwsh` process per case, ~1.7 s each). Remaining pytest ≈ 2.5 min. |
| Next longest | Operation A Windows Tests 11.9 (10.6 in one serial step, 3 files, both PowerShell hosts) · E2E Functional Shard 1/2 9.9 (8.9 of specs) · Shard 2/2 8.4 · Windows visual 3.9 · Packaged smoke 2.5 · others < 2 |
| pytest | 4,231 cases, 211 skipped, serial, 87.3% line coverage over `utils` + `routes`, no branch coverage, `app.py` excluded by design. `psutil` is not installed, so `pytest -n auto` would mean logical CPUs (4 on `ubuntu-latest`). |
| Vitest | 245 passed; 8.24% statements; 45 of 58 modules at 0% |
| tsc scope | `e2e/**/*.ts` + `playwright.config.ts`; the 51 modules in `static/js/modules/` have no type check and no ESLint |
| Playwright | `retries: 2` in CI (first-attempt failures invisible); browsers installed fresh per job |
| Deep Gate history | Scheduled runs failed 2026-08-31 → 2026-10-12 (7 consecutive); only `visual-linux` fails, the other six jobs pass. **Investigated:** `docs/deep_gate_linux_visual_failure_20260831/GATE0.md` + `GATE1.md` (2026-09-01) ran a controlled two-arm comparison on one capture, supports hypothesis H-LINUX-UNSYNC-01, excludes runner-image/browser/nondeterminism, assigns no commit, says nothing about the other 64 failing captures (65 total, matching Astra's reading of the 2026-10-12 run). GATE1 lists owner options **A** bisect · **B** widen matrix · **C** regenerate Linux baselines · **D** stop, recommends A, and records that **none has been taken**. |

### 2.2 Repository and release-gate settings

| Setting | Value |
|---|---|
| Default workflow token | `read` ✔ · `can_approve_pull_request_reviews: false` ✔ |
| `permissions:` block | present in `release.yml`, `_packaged-windows.yml`; **absent** in `ci.yml`, `deep-gate.yml` |
| Action pinning / policy | tags only (`@v7`); `sha_pinning_required: false`; `allowed_actions: all` |
| Secret scanning / push protection | **disabled** |
| CodeQL default setup | **not configured**; eligible: `actions`, `javascript-typescript`, `python` |
| Dependabot | alerts on, 0 open; version updates on (pip, npm, github-actions, weekly); security updates off (D-6) |
| Branch protection `main` | 12 contexts; `strict: false`; `enforce_admins: false`; 0 reviews; no rulesets |
| Merge queue | **not available**: GitHub offers it on Enterprise Cloud and on public repos owned by *organizations*; this repo is user-owned |
| Release provenance | `scripts/release_gate.py` `REQUIRED_CONTEXTS` = the 12 names below, byte-for-byte, plus `VISUAL_CONTEXT = "Visual Regression (Windows baselines)"` → 13 expected, each must conclude `success` on the tagged commit (newest run per name) |

### 2.3 Required contexts (exact strings; mirrored in `scripts/release_gate.py`)

```
Run Tests
E2E Functional (Chromium)
E2E Backup (Chromium, isolated)
E2E Smoke (Chromium)
Type Check (tsc blocking + pyright measure-only)
Code Linting
Frontend Build (npm ci + SCSS)
Security Audit
E2E Fatigue Context (Chromium, non-required)
E2E Erase Flow (Chromium, isolated, non-required)
Test Inventory Drift
JS Supply Chain (npm audit, non-required)
```

Not required: `JS Unit (Vitest, non-required)`, `Visual Regression (Windows baselines)` (release-expected but not protected), `Operation A Windows Tests`, `Packaged Smoke (Windows bootloader, non-required) / Build and smoke`, `CSS Stylelint Measurement (non-required)`, the two shard legs.

---

## 3. Owner decisions — approved Gate 0 package, 2026-10-19

This is the operative decision sheet. It supersedes the pre-approval §3 recommendations; §§10–11 retain their dated advisory audit trail. **All eleven requirements decisions are approved; none of the execution actions below has been taken by this council.**

| ID | Approved requirement | Remaining prerequisite / boundary | Packets |
|---|---|---|---|
| CI-D1 | Bounded compare-only bisect A of `31659a59..b36ea9e` and separately monitored visual workflow E | Core Gate 1 plus named diagnostic extension; retain one-capture hypothesis H-LINUX-UNSYNC-01, ADR-011, baselines/tolerances/exemptions; stop at attribution or bounded inconclusive result. No broader experiment/fix. | E1, D3, E3 |
| CI-D2 | Strict checks; defer organization transfer/merge queue | Owner settings execution after approved plan; retain every check/app binding. | C2 |
| CI-D3 | Four independent conditional promotions; B2/B3 required after qualification | §11.5 proof matrix; original JS Q4/D2 unsigned; code/contracts before owner activation. Separate PR/release sets; no A2 or Linux coupling. | C4 |
| CI-D4 | Claude-only advisory ten-review pilot, 15 minutes/20 turns, existing OAuth subscription quota only | Owner credential/app authorization and two-push fresh-head/security rehearsal before enablement; no paid fallback. Codex requires separate paired-trial evidence, credential and hard spend cap. | D1; D2 deferred |
| CI-D5 | Docs filtering deferred | Measured speed work, A5 protection proof and fail-closed classifier cases before a new proposal; `main` always validates fully. | A5 deferred |
| CI-D6 | Initial prereleases unsigned; no signing purchase | Owner distribution acceptance at separate delivery gate. Any signing identity/credential/purchase separate; smoke final signed bytes if later approved. | F2 deferred |
| CI-D7 | Secret scanning, push protection, CodeQL; after baseline triage block newly introduced High/Critical CodeQL security alerts | Native CodeQL rule with `security_alerts_threshold: high_or_higher`, `alerts_threshold: none`, seeded blocking proof, and CI-D10-compatible bypass. Preserve D-6 and non-blocking coverage. | C1 |
| CI-D8 | Full SHA policy; explicit adopted direct/nested action repositories only | B1 merged, callers/nested inventory reviewed; owner sets `github_owned_allowed: false`, `verified_allowed: false`; no pre-allowing Codex/signing. | B1, C3 |
| CI-D9 | Disable orphan `345538425`, preserve run history | Owner runs/verifies disable command. | C5 |
| CI-D10 | Sole-owner emergency bypass only for red-on-main hotfixes | Document reason, affected checks, compensating evidence and follow-up green; new CodeQL rule must explicitly support this, since `enforce_admins: false` alone does not. | C1/C2/C4 policy |
| CI-D11 | Separate prerelease delivery milestone; exact version tag and candidate recovery before publication | Separate delivery council/Gate 1, ADR-007 amendment, same-ZIP acceptance, owner tag timing; dispatch never publishes and stable promotion remains manual. | F1/F3 separate |

Core Gate 1 was approved after the formal reviewers, all dispositions, actual provenance and Plan v2 were complete (§13). It does not sign JS Q4/D2 or a delivery plan, authorize settings/credentials/spending, merge PRs or publish releases by implication.

---

## 4. Reconciled packet catalog — FORMAL CORE Plan v2

Code packets are one PR each. `Owner` is proposed except B1, claimed in §7. The active core scope is B1/A1/B2/B3/A2/A3/B4/C1–C5/D1/D3/E1/E3/G6/G7 (B4 non-blocking measurement; D1 and E3 retain extra activation gates). All other entries are retained as deferred or separate delivery directions. Time figures are **estimates until measured**.

### Phase A — Speed

**A1 — Isolate the guard tests without weakening `Run Tests`.** Owner: Claude.
- Rename the current pytest job id/name to `pytest-core` / `Python Tests (core)`; add `--ignore=tests/test_guard_destructive_command.py`; restore `timeout-minutes: 20`; rewrite the comment that justified 35 so it does not go stale.
- New job(s) `guard-hook-tests` / `Guard Hook Tests (Linux pwsh)` running only that file, `timeout-minutes: 15`.
- New fan-in job **named exactly `Run Tests`**, `needs: [pytest-core, guard-hook-tests]`, `if: always()`, failing unless **every** dependency result is `success` (so failed, cancelled, skipped and missing all fail), mirroring the existing `e2e-functional` fan-in. Branch protection and `scripts/release_gate.py` keep matching the same string; no settings change, no enforcement gap, atomic in one PR.
- **Benchmark before choosing the parallel shape** (all on a throwaway branch, each run twice): (i) `-n 4`, (ii) `-n 8` (process-spawn-bound work may benefit from oversubscription), (iii) 2 and 4 runner shards from collected node IDs, with and without xdist. Record end-to-end latency, queue/job time, runner-minutes and per-host full test identities/outcomes against a serial run of the **same corpus/environment**. Keep §2's 1,018 count as dated evidence, not an eternal denominator. Preserve per-process PowerShell isolation.
- Green equivalence evidence rejects missing/unexpected identities, unintended duplicate execution, skipped cases and absent/malformed reports; JUnit testcase presence alone is not execution. Separate intentional failure rehearsals from green equivalence. `tests/test_ci_expansion_contracts.py` covers these report/partition decisions; use the existing Operation A verifier's executed-outcome distinction without silently broadening its scope.
- Acceptance: exact `Run Tests` fan-in rejects every failed/cancelled/skipped/missing dependency; seeded guard failure propagates. Core ≤4 min remains an objective; compare coverage to the same-corpus serial baseline (87.3 ±0.1 was the dated starting observation), inventory drift clean, all existing twelve contexts retained. Update `tests/test_worktree_ci_contracts.py` parsers from old `test` job to `pytest-core` without weakening host/report contracts. G6 later adds only its narrow Windows-case leg to this aggregate.
- Gate: full `pytest`; `code-reviewer` + `architecture-reviewer`.
- Note: `tests/test_guard_destructive_command.py` is locally modified by another session in the shared checkout. Do not touch it; work from a clean clone of `origin/main`.

**A2 — Shorten Operation A Windows Tests.** Owner: Astra.
- Preferred: `-n 4` on the existing invocation (no test edits; `verify_ci_report` consumes xunit2 JUnit, which xdist emits). Alternative: 2-leg host matrix, which needs an env var in the test files under the Operation A hold → owner acknowledgement first.
- Acceptance: job time recorded; executed test-id set identical to the baseline `operation-a-windows-junit` artifact; still green.
- Gate: full `pytest`; `code-reviewer`.

**A3 — E2E functional shards 2 → 4.** Owner: Claude. After A1.
- `matrix.shard: [1,2,3,4]`, `--shard=i/4`, leg name `E2E Functional Shard ${{ matrix.shard }}/4` (legs are not contexts; the fan-in `E2E Functional (Chromium)` is and stays). Update the "2-way matrix" comment. `tests/test_playwright_shard_launcher_contracts.py` pins the spec list, not the shard count; run it. `scripts/run-playwright-shards.ps1` is local N=1 (ADR-006), untouched.
- Acceptance: unchanged 25-spec functional set executes across four runners; fan-in rejects every failed/cancelled/skipped/missing leg; leg and aggregate timing recorded (leg estimate ≤6 min). Update the literal shard exclusion in `tests/test_release_workflow_contracts.py`; preserve `tests/test_playwright_shard_launcher_contracts.py` equivalence/resource-isolation coverage.
- Gate: full `pytest`; `code-reviewer` + `architecture-reviewer`.

**A4 — Playwright browser cache (experiment, low priority).** Owner: Astra. After A1–A3.
- Playwright's own guidance: restoring a browser cache can take as long as downloading, and `--with-deps` still installs OS libraries on Linux. So: measure first. Key on OS + arch + `@playwright/test` version; compare "Install Playwright Chromium" step time over ≥ 3 runs each way. Keep only on a demonstrated net saving.
- Gate: full `pytest`; `code-reviewer`.

**A5 — Prove docs-only skipping safely (CI-D5).** Owner: either. Deferred.
- Throwaway PR: job-level `if:` on one non-required job, then on one required job; record `mergeStateStatus`. Then a classifier test matrix: docs-only, docs + code, rename of a code file, `.github/**` edit, and a forced `git diff` failure (must fail closed). Only on `pull_request`; never on `push`. Close unmerged. Design the real filter only after all five behave.

### Phase B — Workflow hardening

**B1 — SHA-pin every adopted `uses:` and add explicit `permissions:`.** Owner: Astra. First shared-workflow hardening slot; no dependency on A1 or B4.
- Inventory all current workflow/reusable callers and action metadata, including nested `uses:`; pin remote actions to reviewed full SHAs with version comments. Add explicit least-privilege defaults to `ci.yml`/`deep-gate.yml` and preserve any justified job permissions. Local/reusable calls retain exact contracts; later B2/B3/D1/D3/E1 additions must satisfy the same policy before adoption. Dependabot version updates remain enabled.
- Acceptance: all baseline jobs retain their effective enforcement; no mutable remote action reference remains; inventory and permission exceptions are reviewable. Do not claim completion from a tag-text grep alone. C3 activation follows this proof; B4 measurement cannot hold it.
- Gate: full `pytest`; `code-reviewer`.

**B2 — actionlint + zizmor.** Owner: Astra. After B1.
- Job `workflow-lint` / `Workflow Lint (actionlint + zizmor)` always runs on every PR and `main` push; no path skip of a required check. Pin tool releases; any adopted action and nested dependency must satisfy B1/C3. Start zizmor `--min-severity medium`; fix findings without unexplained suppression.
- Acceptance: clean representative PR and main run; seeded untrusted PR-title interpolation in `run:` makes lint red. Promotion waits for seeded blocking proof, actual check-name observation and C4 activation; release set includes B2.
- Gate: full `pytest`; `code-reviewer` + `architecture-reviewer`.

**B3 — Dependency review on PRs.** Owner: Astra. After B2.
- `actions/dependency-review-action` (explicitly allowlisted, SHA-pinned), proposed exact name `Dependency Review`; every eligible PR, `fail-on-severity: high`, scopes `runtime, development, unknown`, `warn-only: false`. Job-summary output only; no comment-write permission. Existing full pip/npm audits remain on `main`.
- Acceptance: clean dependency-change PR and seeded vulnerable dependency produce green/red respectively; actual name and merge blocking verified for C4. PR-only: never add B3 to `RELEASE_EXPECTED_CONTEXTS`.
- Gate: full `pytest`; `code-reviewer` + `architecture-reviewer`.

**B4 — Branch coverage.** Owner: Claude. After A1.
- `--cov-branch`; extend "Summarize coverage" with branch rate. No threshold (D1).
- Gate: full `pytest`; `code-reviewer`.

**B5 — Additional scanner isolation/actionability.** Owner: Claude. **Deferred outside core** until incremental findings justify maintenance/triage; a fresh proposal determines tooling, credentials and cost. No scanner is removed by this plan.
- Today (`deep-gate.yml` Dependency Health): `pip install safety` into the same environment as the app requirements, then `safety check --json || true`. It does run, but (a) the scanner's own dependencies land in the scanned environment, (b) `check` is the deprecated 3.x subcommand, (c) `|| true` plus JSON to the log means nobody reads it.
- Retained direction only: isolated scanner environment and frozen app inventory with summaries. Required audits stay intact. Do not implement, remove or newly enforce this scanner as part of core.
- Gate: full `pytest`; `code-reviewer`.

### Phase C — Settings (owner runs §6; agents verify)

| ID | Setting | Depends on | Verify |
|---|---|---|---|
| C1 | Secret scanning/push protection/CodeQL setup, baseline triage, native alert rule and emergency bypass | Core Gate 1, owner settings execution; seeded High/Critical proof and supported bypass required | Setup state plus alert-rule configuration and blocked seeded PR; no invented Actions context |
| C2 | `strict: true` with existing check/app bindings preserved | Core Gate 1 and owner execution | Read full before/after required-check object, strict true, no dropped checks |
| C3 | Selected actions, full SHA, explicit adopted direct/nested repositories, both broad flags false | B1 merged, inventory reviewed; owner execution; later additions separately inventoried first | Both policy endpoints read back; all callers still execute |
| C4 | Independently qualified promotions; PR/release set contract migration | §11.5 proofs, JS Q4/D2 for JS only, code/contracts merged; owner activates qualified PR subset | `tests/test_release_gate.py` and workflow contracts cover every supported staged set, both existing floors, B3 exclusion, visual once, composite names, exact app/SHA/newest-run checks; actual settings/blocking readback required |
| C5 | Disable orphan; history retained | Core Gate 1 and owner execution | `gh workflow list --all` shows `disabled_manually` for `345538425` |

### Phase D — Agentic review (CI-D4)

**D1 — Bounded Claude advisory pilot.** Owner: Claude. Core plan includes its design; enablement waits for owner OAuth/app authorization and qualification.
- Proposed `claude-review.yml`: trusted default-branch `workflow_run` completion orchestration for eligible same-repo human code/workflow PR CI runs targeting `main`. Verify the originating run's PR event, repository, author, base and exact head against current PR metadata before review/posting; stale or excluded carriers do not count. **No secret-bearing PR-defined workflow executes.** Record/pin the reviewed trusted default-branch revision supplying executable workflow, isolated reviewer configuration, prompt, hooks policy, MCP policy and plugin/action versions. Review the exact PR head only as inert source/diff data, never checkout/run its workflow, scripts, package hooks or configuration in the credential-bearing environment.
- Proposed trusted configuration lives under `.github/claude-review/`; it must not inherit this repository's development `.claude/settings.json`, hooks, project MCP servers or tool permissions. Use a clean reviewer environment with a reviewed minimal read/review tool set and only authorized comment output; no application startup, tests, package installation or PR-derived executable tool configuration. Pin/inventory action/plugin dependencies; if the chosen action cannot enforce this boundary, hold D1 pending a reviewed design change. Keep 15-minute timeout, 20 turns and per-PR cancellation.
- Prove two pushes on one PR review their respective head SHAs. If the pinned plugin skips an already-commented PR, hold enablement pending a reviewed invocation change. Untrusted PR code must not execute with privileged tokens; constrain output to authorized review comments. Bot, fork, docs-only, stale, failed, skipped and incomplete attempts are classified explicitly.
- Count ten **completed fresh-head** reviews, recording §11.6's ledger fields and human dispositions. Existing subscription OAuth quota only; exhausted quota fails visibly, with no paid API fallback or automatic retry escalation. No required check, bypass, automatic patch or merge.
- Acceptance: seeded representative defect has exact-head output; two-push freshness and least-privilege/exclusion rehearsal pass; adversarial PR workflow/settings/hooks/MCP/plugin/package-script edits cannot execute PR-controlled code with credentials. Include tests of untrusted executable files outside restored config, attempted tool escalation and stale-result posting. Attempts/completions remain distinct. Optional AI diagnosis in D3 is outside this pilot. This implements AR-1; pinned vendor behavior is validated before activation, not assumed from the historical command.
- Gate: full `pytest`; `code-reviewer` + `architecture-reviewer`.

**D2 — Codex comparison proposal, deferred outside core.** Owner: Astra, unclaimed.
- After ten completed D1 reviews, a human-established material missed defect class permits proposing a paired trial on the same ten archived heads; it does not launch one. Owner must first choose a hard spend cap and supply/authorize its API credential. No present credential, spend or allowlist authority.
- Standing second-reviewer recommendation requires ≥2 unique human-confirmed actionable defects on ≥2 heads, ≥50% actionable nonduplicate findings and cost within the cap. One reproduced High/Critical security/data-loss defect permits only an explicit owner exception. Any future plan separates read-only review from least-privilege posting, chooses model/effort, and obtains its own gates.

**D3 — Deterministic Deep Gate watchdog.** Owner: Claude. Ship with E1 as a single coherent observability change or before separation with both watched identities configured.
- `deep-gate-watch.yml`: `workflow_run` completions for both `Deep Gate (manual + weekly)` and `Deep Gate Visual (Linux)`; every non-success conclusion upserts one workflow-specific `deep-gate` issue within one hour, including run/attempt/head, failed jobs/first failing step and a visible unresolved state. Keep Linux failures visible after splitting. No AI or credential is necessary; optional AI diagnosis is deferred.
- Freshness is keyed to **this week's expected Monday 03:17 UTC slot**, with workflow identity and `event: schedule`; a manual run, previous week's run or recent success from the wrong workflow cannot qualify. Tuesday 12:00 UTC checks the current slot (~32 h 43 min later), below the 36-hour requirement. Account for incomplete, late and absent runs explicitly; do not reuse the superseded “within eight days” predicate. Record watchdog dispatch delay too; if GitHub scheduling cannot demonstrate the deadline, surface that limitation for an owner decision rather than claim the guarantee.
- **Visual recovery predicate:** only a newer successfully **executed compare-mode** job/step for the matching visual workflow/head/run/attempt can resolve its visual-failure issue. A successful workflow whose comparison skipped or ran generation cannot resolve it. Manual executed comparison may establish visual recovery but never scheduled freshness; keep missing-slot status separate. Order updates by run/attempt evidence so stale delivery cannot clear or overwrite newer unresolved results. A green six-job workflow never resolves the Linux issue.
- Acceptance: fixtures/rehearsals cover both failures, cancelled/timed-out/skipped results, manual-only/previous-week history, in-progress/late/missing current slots, duplicate and out-of-order deliveries, compare success, skipped compare, generation success, and independent issue recovery/freshness. API pagination or unavailable responses never become healthy evidence. Minimal `actions: read`/`issues: write`; no upstream artifact or untrusted-code execution. Local fixtures prove classification; real dispatch/completion timestamps prove timing targets.
- Gate: full `pytest`; `code-reviewer` + `architecture-reviewer`.

### Phase E — Deep Gate repair (CI-D1)

**E1 — `visual-linux` to `Deep Gate Visual (Linux)`.** Owner: either. Same weekly cron + `workflow_dispatch`, preserving compare behavior/inputs and all visual policy; `deep-gate.yml` retains six jobs. Couple activation to D3 monitoring/recovery predicates. Update `tests/test_release_workflow_contracts.py` workflow census/job counts, Linux conditions and baseline-generation guards, and `tests/test_playwright_runner_contracts.py` visual-source/seed reads. D1/D3/E1 enter the declared workflow census without admitting undeclared workflows/callers; preserve positive/negative contracts. Narrowly update `QUALITY_GATE.md` references. No PR trigger or baseline regeneration added. Gate: full `pytest`; real Linux compare execution with ADR-011 unchanged; `code-reviewer` + `architecture-reviewer`; manual agent-workflow reference review.

**E2** merged into D3 (freshness check).

**E3 — Bounded diagnostic A, separately activated within core.** Owner: owner-assigned. Requirements select bisect `31659a59..b36ea9e` under the already named H-LINUX-UNSYNC-01, one-capture scope. Proposed extension records interval, binary-bisect probe cap derived from its finite commit count, stop criteria and compare-only command before execution; requires core Gate 1 and that named diagnostic authorization. Record `docs/deep_gate_linux_visual_failure_20260831/GATE2.md`; stop at attribution or bounded inconclusive result. Do not widen to 64 other captures, modify baselines/tolerances/exemptions, rerun rejected hypotheses or implement a fix.

### Phase F — Release delivery (CI-D11)

**F1 — Candidate artifact preparation, then separately gated publication.** Proposed owner: Astra. **Outside this core council; separate delivery council/Gate 1 required.**
- Retain §11.7 acceptance: build/smoke candidate; explicitly create final ZIP, digest and immutable artifact identity; transfer the exact ZIP to F3 via direct reusable-build dependency/output forwarding. SBOMs distinguish build inputs/tools from bundled contents. No rebuild/substitution between evidence and publication.
- After F3 passes, verify digest again, attest that ZIP, retain existing provenance/install/version gates and amend ADR-007. Genuine owner-created `^v\d+\.\d+\.\d+$` tag on `main` must match both version files; only then may separately authorized prerelease publication occur. Dispatch rehearsals publish nothing; `v0.0.0-rc.test` is invalid. Stable promotion stays manual; partial publication failure remains failed/visible.
- Delivery council must define artifact-retention/recovery/attestation tests and full applicable gates. No artifacts, tags, releases or settings are created by core.

**F2 — Signing, deferred separately.** No purchase/identity/credential authority. Initial distribution is unsigned with the delivery-gate tradeoff. If later approved: sign before final smoke → ZIP/digest → F3 recovery → attestation/publication; never sign already-tested bytes afterwards.

**F3 — Unpublished-candidate upgrade/recovery validation.** Proposed owner: Claude. After F1 **candidate preparation**, before publication, under separate delivery council/Gate 1.
- Extract the exact final ZIP and cover fresh install, historical-schema bootstrap, later previous-release upgrade, default/portable runtime trees, startup/restart and interrupted upgrade. Preserve routines/order, logged history, profile/settings and stored program backups.
- Take/verify a consistent pre-upgrade DB snapshot before first candidate launch; startup backup follows schema/catalog mutation and can be absent, so cannot replace it. Later releases restore with a compatible prior binary; first release restores/verifies the legacy fixture and retries the candidate. No prior release is invented and no runtime backup/startup semantics are changed by this requirement.

### Phase G — Test effectiveness (G6/G7 core; remaining expansion deferred)

| ID | Packet | Owner | Note |
|---|---|---|---|
| G1 | Hash-locked Python requirements (`pip-compile --generate-hashes`, `--require-hashes`) | Astra | npm has lockfile integrity; pip does not |
| G2 | Nightly bounded mutation testing (`mutmut` on `utils/`, report-only) in Deep Gate | Claude | Replaces the manual mutation arms run by hand today |
| G3 | ESLint over `static/js/**`, measure-only first | Astra | Then `checkJs` incrementally |
| G4 | Vitest coverage ramp: 5 highest-risk modules at 0% | Claude | 45 of 58 at zero |
| G5 | Bring `app.py` into coverage via the real-app tests | Claude | Fix the `Module app was never imported` exclusion |
| G6 | Six Windows-host cases in `tests/test_agent_workflow_contracts.py`; three installed-dependency cases in `tests/test_braces_override_contracts.py` | Astra | **Core:** new narrow `workflow-contracts-windows` leg runs the six `powershell` identities and is added to existing required `Run Tests` fan-in; three dependency identities execute in `pytest-core` after `npm ci`. Independent of Operation A promotion; never aggregate the entire unqualified Operation A job. |
| G7 | Attempt-preserving `scripts/ci_retry_report.py` with `tests/test_ci_retry_report.py` | Claude | **Core:** first-attempt failures, recovered/exhausted retries and explicit unavailable report status; summaries after success/failure preserve original verdict and retry policy. |
| G8 | Patch coverage, measure-only | either | Compatible with D1 |

**G6 acceptance (TS-2):** record the exact nine selected node IDs (including host parameters), dependency/Windows preflight and executed outcomes from the candidate corpus. `tests/test_ci_expansion_contracts.py` rejects missing/unexpected/duplicated identities, skips, failed/error outcomes and absent/malformed reports. Prove removing a selected case, withholding its prerequisite, skipping it or injecting failure cannot leave its required route green. The existing required `Run Tests` dependency set includes `pytest-core`, guard legs and the narrow Windows leg after G6 lands, with all-success required; failure/cancellation/skip/missing of any leg fails it. This adds enforcement of the approved six cases only, not implicit promotion of all Operation A tests.

**G7 acceptance (TS-3):** pin/identify selected reporter formats; behavioral fixtures cover first-attempt success, fail→recover, exhausted retries, distinct tests/shards and attempt numbers, and any already-configured pytest rerun output (do not introduce reruns). Missing/malformed/partial reports are visibly `unavailable`, never zero retries. Summary runs after successful or failed test steps and cannot overwrite the original result. Script behavior tests and the actual changed-path gates apply; existing timing helper/wiring tests alone are insufficient.

---

## 5. Ordering and expected effect

| Batch | Packets | Pipeline wall after (estimate) | Needs |
|---|---|---|---|
| 0 | Formal v1 → independent reviewers → every disposition → v2 → owner Gate 1 | Complete, 2026-10-19 | Core Gate 1 approved; subsequent execution authority is B1 only (§13) |
| 1 | B1 first shared-workflow slot, then A1 benchmark/fail-closed fan-in; B2/B3; C1/C2/C5 prepared for owner execution | **12–15 min initial objective**; include queue time | Core Gate 1 and implementation authority; settings remain owner actions |
| 2 | A2/A3, G6 enforced destinations, G7 retry visibility; B4 optional measurement slot after A1 | **8 min second-stage target**, 6 min stretch; neither promised | Serialize shared workflows; B4 cannot delay B1; preserve test identities |
| 3 | C3 inventory/policy; C4 contract migration and independent qualified activations | No fixed speed claim | Pins/contracts first; proofs per candidate; JS Q4/D2 separate; owner readback |
| 4 | E1+D3 monitoring, E3 diagnostic; D1 pilot | Observability and advisory coverage | Monitoring coupled to split; E3 named extension; D1 credential/freshness gates; earlier independent slots allowed |
| Separate | F1 candidate → F3 recovery → publication | No core dependency | Separate delivery council/Gate 1 and owner release timing |
| Deferred | A4/A5/B5/D2/F2/G1–G5/G8, organization/merge queue | No promised saving/service | Separate decision; never a prerequisite to core hardening |

Measure workflow creation → required-gate completion, queue delay, job wall and runner-minutes against comparable events/commits. Reuse §2 as a dated baseline, not a current median. §11.2's 22.5-minute queue example establishes no distribution. Record available concurrency and budget constraints at the future benchmark; speed targets authorize no spending.

---

## 6. Owner command sheet (PowerShell) — proposals only

**Do not execute during council.** After the applicable approved plan and separate owner settings action, prepare exact JSON under `artifacts/ci_cd_expansion/settings/`; capture timestamped before/after API readbacks and preserve other sessions' settings. No root-level payload files, guessed actor IDs, or blind replacement with a stale full object.

| Packet | Reviewed payload / prerequisites |
|---|---|
| C1a | `security_and_analysis.secret_scanning.status` and `secret_scanning_push_protection.status` = `enabled`; preserve Dependabot security-updates OFF. |
| C1b | `state: configured`, `query_suite: default`, languages `python`, `javascript-typescript`, `actions`; baseline triage follows. |
| C1c | Native code-scanning ruleset on `main`, tool CodeQL, `security_alerts_threshold: high_or_higher`, `alerts_threshold: none`; seeded newly introduced High/Critical alert must block. Separate rule, no invented check context. Sole-owner **numeric User ID**, `bypass_mode: pull_request`; no blanket admin or unaudited `exempt`. Owner emergency PR records reason/checks/compensating evidence/follow-up green. |
| C2 | PATCH only `strict: true`; preserve exact current checks and app bindings. |
| C3 | After B1 pins and adopted direct/nested/caller inventory: selected-actions body `github_owned_allowed: false`, `verified_allowed: false`, explicit `patterns_allowed` repositories (including adopted GitHub-owned actions). Policy body `enabled: true`, `allowed_actions: selected`, `sha_pinning_required: true`. No broad `actions/*`, deferred Codex/signing or unreviewed nested dependency. |
| C4 | After candidate qualification/signatures and code/contracts merge: `strict: true`, `checks: [{context: <exact observed name>, app_id: 15368}, ...]`. Preserve existing checks/bindings; include only the currently qualified approved subset, not all 18 target members. JS Q4/D2 remains unsigned. No context-only POST. |
| C5 | Disable workflow `345538425`; retain historical runs. |

The manager verified the supported rule/bypass fields, check app bindings and repository SHA-policy field against [GitHub rules API](https://docs.github.com/en/rest/repos/rules), [branch protection API](https://docs.github.com/en/rest/branches/branch-protection), and [Actions permissions API](https://docs.github.com/en/rest/actions/permissions) during this council. An admin exemption in branch protection does not bypass a ruleset.

```powershell
$REPO = "AvihaiShai/Hypertrophy-Toolbox-v3"
$EvidenceDir = "artifacts/ci_cd_expansion/settings"
# Future owner-run readbacks; retain full JSON before/after each relevant change.
gh api "repos/$REPO/branches/main/protection/required_status_checks"
gh api "repos/$REPO/rulesets"
gh api "repos/$REPO/actions/permissions"
gh api "repos/$REPO/actions/permissions/selected-actions"
gh api "repos/$REPO" --jq .security_and_analysis
gh api "repos/$REPO/code-scanning/default-setup"

# Proposed mutations remain commented until payload review and separate owner execution.
# gh api -X PATCH "repos/$REPO" --input "$EvidenceDir/c1-security.json"
# gh api -X PATCH "repos/$REPO/code-scanning/default-setup" --input "$EvidenceDir/c1-codeql.json"
# gh api -X POST "repos/$REPO/rulesets" --input "$EvidenceDir/c1-alert-rule.json"
# gh api -X PATCH "repos/$REPO/branches/main/protection/required_status_checks" -F strict=true
# gh api -X PUT "repos/$REPO/actions/permissions/selected-actions" --input "$EvidenceDir/c3-adopted-actions.json"
# gh api -X PUT "repos/$REPO/actions/permissions" --input "$EvidenceDir/c3-policy.json"
# gh api -X PATCH "repos/$REPO/branches/main/protection/required_status_checks" --input "$EvidenceDir/c4-qualified-checks.json"
# gh workflow disable 345538425 -R $REPO
```

**Staging and verification:** C3 prepares the complete adopted allowlist while existing policy permits it, then activates selected/full-SHA policy and verifies every caller; future adopted integrations update inventory before use. C4 stages one independently qualified promotion at a time: evidence/signature → code/contracts → owner applies PR set → exact readback and blocking proof. Refresh settings immediately before apply; drift requires reconciliation, never overwriting another session. Seeded job failure is pre-activation proof; owner-controlled activation then proves that the failure actually blocks merge. Existing checks never disappear.

The contract PR distinguishes `PR_REQUIRED_CONTEXTS` from `RELEASE_EXPECTED_CONTEXTS`, maintaining each current floor; PR-only B3 never becomes release evidence and Windows visual occurs once. Settings compare to the **approved staged subset**, not future full adoption. No release is tagged during a partially applied transition. Do not activate or sign JS by interpreting this command sheet as approval.

---

## 7. Ledger

B1 is claimed by Codex `/root`, 2026-10-19; all other packets remain unclaimed and unauthorized for execution in this session. Core Gate 1 is approved; `blocked` now names remaining packet-specific prerequisites or execution authority, not missing core Gate 1 or Gate 0. `deferred` and `separate milestone` distinguish excluded work. No PR/head/run is invented; §11.5 evidence qualifies only its named criterion, never implementation or owner approval.

| Packet | Owner (proposed) | Status | Branch / PR | Head SHA | Evidence (run id, job, value) | Notes |
|---|---|---|---|---|---|---|
| A1 | Claude | blocked | | | | Core Gate 1; benchmark/fan-in proofs; after B1 shared-file slot |
| A2 | Astra | blocked | | | | Core Gate 1; identities preserved; not a promotion prerequisite |
| A3 | Claude | blocked | | | | Core Gate 1; after A1; four-leg fan-in proof |
| A4 | Astra | deferred | | | | Optional cache experiment outside core |
| A5 | either | deferred | | | | CI-D5; no docs filtering in core |
| B1 | Codex `/root`, 2026-10-19 | implemented; local gates complete; ready to push | `ci/b1-action-pins`; PR pending | implementation `1dfe011b1533f1339660b72a60249b390b296104` | Full run `b1-local-full-pytest-attempt-2` + resolved Bash contract rerun; independent review complete, no findings; §13 | B1 only; merge pending separate owner instruction; C3/settings remain unauthorized |
| B2 | Astra | blocked | | | | after B1 |
| B3 | Astra | blocked | | | | after B2 |
| B4 | Claude | blocked | | | | After A1 free slot; non-blocking measurement; never delays B1 |
| B5 | Claude | deferred | | | | Unique scanner value unproven; no removal |
| C1 | Owner | blocked | | | | Core Gate 1; setup/triage/native rule/bypass and seeded proof; owner execution |
| C2 | Owner | blocked | | | | Core Gate 1; strict-only change preserves checks/bindings |
| C3 | Owner | blocked | | | | Pins/inventory first; broad flags false; owner execution |
| C4 | Owner + implementer | blocked | | | §11.5 evidence reused | Candidate proofs/signatures; separate sets; contracts then settings; JS Q4/D2 unsigned |
| C5 | Owner | blocked | | | | Core Gate 1; owner disable; retain history |
| D1 | Claude | blocked | | | | Core Gate 1 + OAuth/app; trusted orchestration/isolated config and adversarial/fresh-head proof; subscription only |
| D2 | Astra | deferred | | | | Paired-trial proposal requires evidence, spend cap, credential |
| D3 | Claude | blocked | | | | Core Gate 1; E1 monitoring; newer executed-compare recovery distinct from schedule freshness |
| E1 | either | blocked | | | | Core Gate 1; both monitors active at split |
| E3 | owner-assigned | blocked | | | | Core Gate 1 + named bounded diagnostic extension; no fix |
| F1 | Astra | separate milestone | | | | Delivery council/Gate 1; candidate before publication |
| F2 | tbd | deferred | | | | No signing purchase/credential/identity authority |
| F3 | Claude | separate milestone | | | | Delivery council/Gate 1; exact candidate ZIP, before publication |
| G1–G5/G8 | per §4 | deferred | | | | Expansion outside core; coverage stays non-blocking |
| G6 | Astra | blocked | | | | Core Gate 1; narrow Windows leg + dependency cases feed Run Tests; independent of Operation A promotion |
| G7 | Claude | blocked | | | | Core Gate 1; ci_retry_report behavior suite; unavailable reports visible; verdict/policy preserved |

---

## 8. Known traps for these packets

- Required names/app bindings are exact contracts (§0.7/§11.5). Compare live checks to the staged PR set; release evidence excludes B3. Composite child renames affect every caller.
- Adding or removing any test trips `Test Inventory Drift`; regenerate with `node_modules` present and no gitignored `.md` in `.claude/rules`, `.claude/commands`, `.claude/agents`, `docs/ai_workflow`.
- `tests/test_playwright_shard_launcher_contracts.py` pins the required E2E spec list at 25; A3 changes shard count, not the list.
- `main` has zero pyright headroom.
- Any uncommitted change under `static/css/` reds full pytest until committed.
- `gh pr merge` can exit 1 while the merge succeeded; verify with `gh pr view <n> --json state,mergedAt`.
- A push to a PR cancels its in-flight CI run; a push to `main` never cancels another `main` run.
- Vitest exits 1 while printing "N passed"; judge by exit code.
- `jq` is not on PATH here; use `gh --jq` or `python -I`.
- The Deep Gate cron fires hours late; never key a watchdog on the cron minute.
- Current-slot schedule evidence is necessary; previous-week/manual runs cannot establish freshness. Watchdog dispatch latency needs proof.
- Successful CodeQL execution is not alert blocking; ruleset bypass differs from branch-protection admin exemption.
- A green sample is not Q4/D2 approval, activated protection or a fresh-head AI review.
- Delivery uses a verified pre-upgrade snapshot and final ZIP; startup backup is not assumed recovery evidence.

---

## 9. Remaining decisions and scope checks

No unanswered requirement blocks completed formal core planning. The three independent reviewers read formal v1 cold; §12.2 preserves their outputs and §12.3 accepts all five findings in final v2. B1 is claimed in §7; other owners remain proposed. A2 prefers xdist without test edits; a host-matrix variant touching held tests returns to its owner boundary. D2 model/effort/budget and F1/F3 details belong to separate proposals.

Core Gate 1 is approved for Plan v2; only B1 is authorized for execution (§13). JS Q4/D2, activation proofs, settings execution, D1 credentials, E3 named diagnostic extension and separate delivery council/Gate 1 remain individual gates. GitHub access is capability, not authorization.

---

## 10. Disposition of Astra's v1 review (2026-10-18)

> **Historical advisory record; superseded where inconsistent, 2026-10-19.** Text below is preserved verbatim. Live requirements/packets are §§0–9, reconciled to approved §§11.4–11.8; formal council starts at §12. References below to old fixed ordering, mirrored enforcement sets or publication-first F1 do not govern the current plan. No advisory pass counts as a formal review.

| # | Point | Disposition |
|---|---|---|
| 1 | A1 weakened `Run Tests` by moving 1,018 tests to an optional job | **Accepted.** A1 now keeps `Run Tests` as an aggregate fan-in requiring every dependency to be `success`; failed/skipped/cancelled/missing all fail it; atomic in one PR. |
| 2 | C3 "GitHub-owned only" would block the planned third-party actions | **Accepted.** §6 C3 carries `patterns_allowed` and a transitive-`uses:` verification step; flip only after B1 and the allowlist check. |
| 3 | Six-minute pipeline stated as outcome; `-n auto` ≠ runner sharding; 8-min guard job contradicts 6-min total | **Accepted.** A1 benchmarks explicit worker counts vs runner shards on elapsed, queue, runner-minutes and executed test-id sets. §5 now says ~12–15 after batch 1, 6 min stretch. `psutil` absence noted. |
| 4 | F1 attested artifacts the reusable build never exports; release publishes nothing; F3 has no previous release | **Accepted.** F1 adds artifact export + a tag-only `release-publish` job after `release-gate`; SBOM from the build's frozen set; CI-D11 added for publication; ADR-007 amendment; F3 bootstrap case. |
| 5 | E1 + D3 blind spot; E2 Tuesday 06:00 misses the 24 h target; AI should not be the only issue-creator | **Accepted.** D3 watches both workflows via `workflow_run`, upserts the issue deterministically with `github-script`, AI diagnosis second; freshness check Tuesday 12:00 UTC; G5 restated as failure ≤ 1 h, missing ≤ 36 h. E2 folded into D3. |
| 6 | Promotions must update `scripts/release_gate.py`; docs skipping on `main` would break release provenance | **Accepted.** CI-D3/C4 require the `release_gate.py` + contract-test PR first; CI-D5 deferred with `pull_request`-only and classifier test matrix preconditions. |
| 7 | A4 is an experiment, not a saving | **Accepted.** Reworded; measured over ≥ 3 runs each way; lowest priority in Phase A. |
| 8 | Protocol lacks isolation and approval sequencing | **Accepted.** §0.1 (nothing before Gate 1), §0.3 (own clone), §0.4 (one `ci.yml` PR at a time, fixed order), §0.5 (evidence tied to head SHA). |
| — | Three, not two, false `(non-required)` contexts | **Corrected** in §0.7, §1.4, §2.2 (also confirmed by `release_gate.py`'s own comment). |
| — | Deep Gate was investigated (GATE0/GATE1) | **Corrected** in §1.1 and §2.1; CI-D1 now maps to GATE1's options A–D. |
| — | `safety` did execute | **Corrected**; B5 reframed as isolation + actionable reporting. |
| — | D-6 does not make every dependency PR human-opened | **Corrected** in §1.4. |
| — | C4 body is `{"contexts":[...]}`; commands should be PowerShell-compatible | **Corrected** in §6. |
| rec. | Strict now, org transfer separately; one AI reviewer first; defer docs skipping | **Adopted** in CI-D2, CI-D4, CI-D5. |

---

## Agent provenance

- 2026-10-18 — Claude: live audit of `origin/main` `7ac1af2d` and run `39125460089` (Actions API job/step timings, JUnit and coverage artifacts), repo settings via `gh api`, `scripts/release_gate.py`, `docs/deep_gate_linux_visual_failure_20260831/GATE1.md`, external references (GitHub Actions 2026 security roadmap, Claude Code GitHub Actions docs, Codex GitHub Action docs, merge-queue GA changelog). Drafted v1; revised to v2 per §10.
- 2026-10-18 — Astra: independent audit of the same commit and run; v1 review (§10). Figures attributed to Astra in §2.1 were not independently re-verified by Claude except where noted.

---

## 11. Gate 0 advisory decision panel — 2026-10-18

> **Dated status supersession, 2026-10-19:** owner approved §§11.4–11.8 with §11.9 boundaries. Text below remains verbatim, including then-correct “unsigned”/“unmade” language; §1 supersedes those historical Gate 0 status claims only. Advice is now approved requirements, not formal council work. Core Gate 1, JS Q4/D2, activation/execution authority and separate delivery council/Gate 1 remain pending.

**Team recommendations; owner Gate 0 signature pending.** The owner requested this consultation. It is not the formal council, does not approve Gate 0 or Gate 1, and does not authorize implementation, settings changes, spending, or publication. Earlier sections remain the v2 proposal; reconcile the differences below before council review.

### 11.1 Recommended decisions

| ID | Team recommendation |
|---|---|
| CI-D1 | **A + E:** bounded, compare-only bisect and a separately monitored Linux-visual workflow. Preserve baselines, tolerances, exemptions, and unresolved residuals; evidence about one capture does not explain the other 64. |
| CI-D2 | Enable strict required checks now. Defer organization transfer and merge queue to a separate proposal. |
| CI-D3 | Promote JS Unit, Operation A Windows, packaged smoke, and Windows visual on their **own qualification evidence**. Reconcile JS Unit's original 14-day ledger before its owner decision; elapsed time is not approval. Remove the packaged-smoke/A2 and Windows-visual/Linux-investigation dependencies. Make B2 workflow lint and B3 dependency review required after seeded-failure validation. Retain GitHub Actions app binding `app_id: 15368`. |
| CI-D4 | Claude first: advisory pilot of ten eligible PRs, existing subscription OAuth quota, 15-minute timeout and 20 turns, no automatic paid fallback. Test review freshness for each head SHA; record skipped, failed, and incomplete attempts. Consider Codex only after paired comparison and human adjudication show additional actionable findings. |
| CI-D5 | Defer docs filtering until speed work is measured. Retain fail-closed classification and full `main` validation as prerequisites. |
| CI-D6 | Initially unsigned prereleases with checksums, SBOMs, and attestations. No signing purchase; identity and budget decisions remain deferred. Attestation is not Windows executable signing. |
| CI-D7 | Enable secret scanning, push protection, and CodeQL for Python, JavaScript/TypeScript, and Actions. After initial triage, newly introduced high/critical findings need explicit supported merge enforcement, verified by a failing example; a successful scan alone is insufficient. Preserve D-6's disabled Dependabot security updates and D1's non-blocking coverage. |
| CI-D8 | Selected actions and full-SHA enforcement after pins and nested `uses:` inventory verification. Allowlist adopted actions only. |
| CI-D9 | Disable the orphan probe workflow; preserve its historical runs. |
| CI-D10 | Keep owner emergency bypass, documenting reason, evidence, and follow-up CI results. No automated bypass or routine convenience exception. |
| CI-D11 | A genuine owner-created, version-matching tag runs gates and then publishes a prerelease. Stable promotion remains manual; `workflow_dispatch` remains nonpublishing. Delivery is a separate milestone. |

### 11.2 Conditions before implementation

1. **Separate merge checks from release evidence.** Define `PR_REQUIRED_CONTEXTS` as the old twelve plus the four qualified promotions and B2/B3. Define `RELEASE_EXPECTED_CONTEXTS` as the old thirteen plus JS Unit, Operation A Windows, packaged smoke, and B2; Windows visual appears once. B3 compares PR dependencies and is PR-only; full pip/npm audits continue on `main`. Its dependency scopes include runtime, development, and unknown. Cheap workflow lint always runs. Reconcile contracts and owner settings commands with these distinct sets, preserving exact context strings and app bindings.

2. **Repair the release artifact path.** Remove the invalid `v0.0.0-rc.test` production rehearsal. Keep the existing version/tag guard; exercise artifact preparation without publication. Explicitly create the distributable ZIP and digest, transfer that exact artifact, and connect publication directly to the reusable build's outputs through `needs` or explicit forwarding. If signing is later added, smoke-test the final signed executable before creating and attesting its ZIP.

3. **Test recovery before publication.** Move F3's candidate upgrade/recovery rehearsal before publishing the candidate. Bootstrap the first release from the legacy database fixture; subsequent rehearsals use the previous released binary and unpublished candidate. Verify preservation of routines, workout history, settings, and backups. Remove F3's circular dependency on first publishing F1.

4. **Stage scope without skipping gates.** Core speed, security, check integrity, and observability receive Gate 0, formal council, then Gate 1. Delivery gets its own scoped gates; signing and release timing do not hold A1. B4 measurement must not artificially delay B1 hardening. Bring skipped-test destinations and retry reporting forward. Keep one `ci.yml` PR in flight, with isolated working copies and evidence tied to the tested SHA.

5. **Measure end-to-end latency.** Record workflow creation to required-gate completion, queue time, job time, and total runner-minutes. Keep 12–15 minutes as the initial objective, eight minutes as a second-stage target, and six minutes as a stretch. One verified example, run `39069157572`, was created at 21:01:15Z; `Run Tests` started at 21:23:48Z and JS Unit at 21:23:54Z. This shows roughly 22.5 minutes of waiting in that run, not a typical queue or a pipeline median.

### 11.3 Evidence and provenance

The architecture adviser checked the latest ten main-push runs, all four promotion candidates successful in each:

`39125460089`, `39125437122`, `39076077548`, `39076056102`, `39073910652`, `39071497683`, `39069157572`, `39069138125`, `39069120674`, `39069106566`.

These observations span **October 17–18 only**. They satisfy the packaged-smoke ten-green numerical criterion; they do **not** establish JS Unit's original 14-day qualification or supply any owner signature.

Native, role-separated advisers: `/root/ci_architecture_adviser`, `/root/security_release_adviser`, and `/root/product_scope_adviser`. This was neither an external Claude consultation nor the required formal council. No reviewer identity or owner approval is inferred.

Primary references: [Claude action authentication and review behavior](https://code.claude.com/docs/en/github-actions), [Codex action authentication and privilege controls](https://learn.chatgpt.com/docs/github-action), [GitHub Actions policy API](https://docs.github.com/en/rest/actions/permissions), [direct dependency outputs](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#needs-context), and [dependency-review configuration](https://github.com/actions/dependency-review-action#configuration-options). Subscription authentication consumes quota; the Claude review plugin can skip already-commented PRs, so fresh-head behavior needs explicit validation.

Owner actions remain separate: Gate 0/Gate 1 sign-off, credential and app authorization, settings execution, any new expenditure, and genuine release timing. No packets are claimed by this record.

### 11.4 Consolidated Gate 0 package — independent consultation, 2026-10-18

**Recommendation only; Gate 0 and Gate 1 remain unsigned.** This addendum preserves §§0–11.3 as their authors' record. For the next owner decision, use §§11.4–11.9 where they refine the earlier proposal. It is a requirements consultation, not `/council-plan`; none of §4 has started. The three advisers below completed independent, read-only assessments before the coordinator consolidated them.

| ID | Selected recommendation | Tradeoff | Prerequisite / authority still needed |
|---|---|---|---|
| CI-D1 | **A + E:** bounded compare-only bisect of `31659a59..b36ea9e`; separate Linux visual workflow with deterministic monitoring of both workflows. | An extra workflow and diagnostic runner time buy attribution and visibility into new failures in the other six jobs; neither fixes the 65 captures. | Gate 0, council/Gate 1 and the named diagnostic extension; retain GATE1's one-capture scope, ADR-011, baselines and tolerances. Stop at attribution or an inconclusive bounded interval; broader experiments or fixes need a new decision. |
| CI-D2 | **Enable strict required checks; defer organization transfer/merge queue.** | More rebases/reruns, but no transfer maintenance or migration risk. | Owner executes and verifies settings after the approved plan; preserve existing checks and app bindings. |
| CI-D3 | **Promote JS Unit, Operation A Windows, packaged smoke and Windows visual independently; make B2/B3 required after qualification.** | More merge-blocking surfaces; qualification and failure proofs prevent weak or unreliable blockers. | §11.5 evidence, original JS Q4/D2 signature, approved contracts and owner-applied settings. A2 and Linux diagnosis are not dependencies of unrelated promotions. |
| CI-D4 | **Claude-only advisory pilot: ten completed fresh-head reviews, 15 minutes/20 turns each; no automatic paid fallback.** | Uses subscription quota and human triage; deliberately limits extra review cost. | Owner supplies OAuth/app authorization; fresh-head and least-privilege rehearsal. Codex requires the separate evidence/budget decision in §11.6. |
| CI-D5 | **Defer docs-only filtering.** | Retains runner cost while avoiding classifier and missing-check failure modes. | Reconsider only after measured speed work, A5's protection proof and fail-closed mixed-diff/rename/workflow/diff-error cases. Never filter `main` release evidence. |
| CI-D6 | **Unsigned initial prereleases; no signing purchase.** | Windows publisher-trust friction remains; checksum/attestation does not sign the executable. | Owner accepts this distribution tradeoff at the delivery gate. Any later signing identity, credential or purchase is separate; test final signed bytes. |
| CI-D7 | **Enable secret scanning, push protection and CodeQL; after baseline triage block newly introduced High/Critical CodeQL security alerts.** | Adds alert triage and possible blocked PRs. | Owner configures a native code-scanning rule for CodeQL, `security_alerts_threshold: high_or_higher`, `alerts_threshold: none`; seeded vulnerable PR must prove blocking. Coordinate emergency bypass with CI-D10. Preserve D-6 and non-blocking coverage. |
| CI-D8 | **Full-SHA policy and explicit allowlist of adopted action repositories, including reviewed nested dependencies.** | Narrower trust surface costs inventory and update work. | Merge pins first; verify direct/transitive `uses:` and every caller, then owner enables policy. Select `github_owned_allowed: false` and `verified_allowed: false`; explicitly list adopted GitHub-owned actions too. Do not pre-allow deferred Codex/signing integrations. |
| CI-D9 | **Disable orphan workflow `345538425`; retain history.** | Removes accidental execution/noise without deleting evidence. | Owner runs and verifies C5. |
| CI-D10 | **Keep a sole-owner emergency bypass for red-on-main hotfixes.** | Retains a human exception path to avoid recovery lockout. | PR records reason, affected checks, compensating evidence and follow-up green results. No automated/convenience bypass. A new CodeQL ruleset must explicitly support this policy; `enforce_admins: false` alone does not bypass it. |
| CI-D11 | **Prerelease delivery as a separate milestone; publish only a genuine owner-created exact version tag after candidate recovery passes.** | Adds artifact and recovery maintenance without delaying core CI. | Separate delivery council/Gate 1, ADR-007 amendment, §11.7 acceptance and owner release timing. Dispatch never publishes; stable promotion remains manual. Gate 0 approval grants no publication authority. |

### 11.5 Enforcement sets and promotion qualification

These are **target sets after each named promotion qualifies**, not a report of changed protection. Keep every existing requirement throughout transition. Let `R0` be the exact twelve strings in §2.3 and define:

| Set | Target membership | Count at full adoption |
|---|---|---|
| `PR_REQUIRED_CONTEXTS` | `R0` + `JS Unit (Vitest, non-required)` + `Operation A Windows Tests` + `Packaged Smoke (Windows bootloader, non-required) / Build and smoke` + `Visual Regression (Windows baselines)` + `Workflow Lint (actionlint + zizmor)` + proposed `Dependency Review` | 18 |
| `RELEASE_EXPECTED_CONTEXTS` | The same set **without** PR-only `Dependency Review`; Windows visual occurs once | 17 |

`Dependency Review` is a proposed new display name, to be verified from a real check-run before protection changes. It runs on every eligible PR with severity `high`, scopes `runtime, development, unknown`, and `warn-only: false`; use the job summary without comment-write permission. It is not expected on a `main` push. Existing full pip/npm audits still run on `main`. B2 runs on every PR and `main` push; do not path-skip a required lint context. CodeQL's alert-based merge rule is a separate control, not another invented Actions context or a claim that a successful scan means no vulnerabilities.

The promotion PR must reconcile the two sets, `scripts/release_gate.py`, contract tests and C4's owner command sheet together. Merge the code/contracts first, then the owner applies the exact qualified set with GitHub Actions binding `app_id: 15368`, and reads settings back. Release provenance retains exact-SHA, newest-run and trusted-app checks, with missing/skipped/cancelled/failing evidence rejected. Preserve the `Run Tests` fan-in and its fail-closed dependency set; test-id equality, not counts alone, validates guard parallelization. No release should be tagged during a partially applied settings transition.

| Candidate | Evidence reused / remaining qualification |
|---|---|
| JS Unit | Original Q2 requires 14 failure-free days after final expansion, plus Packet F and a separate Q4/D2 owner decision. The targeted ledger reconciliation below addresses the missing interval; October's ten-green sample alone never substitutes for it. No owner signature is inferred. |
| Packaged smoke | §11.3's ten consecutive main-push successes under the exact composite context satisfy ADR-007 R1-D4's numerical condition. Retain bootloader smoke and prove its failure propagates; no A2 dependency. |
| Operation A Windows | Adopt the existing ten-green sample as this proposal's stability criterion, plus proof that both PowerShell hosts actually execute the intended test identities and an injected failure makes the context red. Optimization is optional for promotion. |
| Windows visual | Adopt the existing ten-green sample plus real compare execution and a failing-comparison propagation proof. Preserve 81 byte-gated captures and five semantic exemptions; a skipped comparison or generated baseline is not qualification. Linux diagnosis is independent. |
| B2 / B3 | No green-history claim exists yet. Require a clean representative PR/main run for B2, clean dependency-change PR for B3, and seeded failures that visibly block the corresponding PR checks before owner activation. |

The new ten-green standard for Operation A/Windows visual and seeded-failure proofs are proposed requirements, not claims that those proofs already ran. Reuse existing evidence where it covers them; do not rerun completed audits to manufacture a new history.

**Targeted JS qualification reconciliation (architecture adviser, queried 2026-10-18):** canonical `STEP12_JS_UNIT_GATE0.md` §13.0 at audited `7ac1af2d2dc10be6bf6a5016c09bc5244cf37ed7` contains 39 qualifying successes (rows 26–64), through `2026-08-31T23:05:48Z`. Its declared T0 is `2026-08-27T23:18:21Z`; the strict mark is `2026-09-10T23:18:21Z`. Querying only the missing interval through `2026-09-11T00:00:00Z`, on `main`/`ci.yml`, returned the same eleven runs with and without a push-event filter. Every exact JS Unit job and its `Run Vitest with coverage` step succeeded:

| Run | Head SHA | JS Unit job | Completed UTC |
|---|---|---|---|
| 33523146853 | `fe05bdb4ac46dfb8128cbe692d52ef49f1789f8e` | 99907156047 | 2026-09-01T15:01:38Z |
| 33523178261 | `8767e120cc154b8582b20ead70a7beac9b7d0342` | 99907266034 | 2026-09-01T15:01:54Z |
| 33547291593 | `ec9779f39d35bf71f3a347e56770a9a5b3491df6` | 99987847053 | 2026-09-01T19:04:09Z |
| 33563897334 | `bd152a4e4a5bd3152d9ef6a4bf51858ba0bd5744` | 100042542841 | 2026-09-01T21:58:50Z |
| 33564812258 | `5d3bc95a5251f74d74ff9350a1de11a4131d7999` | 100045442226 | 2026-09-01T22:09:29Z |
| 33570429334 | `22ee9ade7b5b69dcb9aecf6eb19526cc5db31158` | 100062982601 | 2026-09-01T23:19:04Z |
| 33792990269 | `919f29fcb38c8c0547e8d7d2499871d058754c16` | 100773813322 | 2026-09-03T18:51:57Z |
| 33798714799 | `0f1ac2ed66c24151f6d8c00d9962ebd8a959ad6f` | 100792592669 | 2026-09-03T19:50:29Z |
| 34022722343 | `c0cc3f1d5fb3a53a83c80f1d54f8ad6e8f62a848` | 101458142252 | 2026-09-06T08:45:18Z |
| 34065119085 | `87e431c4328206732600b74d656c0080e8a98e75` | 101572407604 | 2026-09-06T22:49:36Z |
| 34170988104 | `343ac37b42b1f4cd5c5faa6a7e2927d1d6c7c241` | 101891095968 | 2026-09-07T23:43:57Z |

**Cancellation is not hidden:** run `34170988104` has a cancelled latest overall conclusion. Its attempt-1 JS job succeeded; attempt-2 job `102565307402` carries the same successful execution timestamps and is not another execution. Exclude this carrier from qualification credit under §6.5. The accounting is **39 + 10 = 49 wholly successful qualifying workflow carriers, plus one excluded cancelled carrier with successful JS execution**. No later CI run occurred before the strict mark; no failed/missing/skipped/cancelled JS job was observed in the bounded gap.

The test tree `static/js/modules/__tests__` is `5858c8497c571548e5116f4b660ff7702dd298b1` and `vitest.config.js` is `c16ca428f7478708d8dd96a20ebcb86f98a8b935` at T0, `343ac37b` and audited main. The bounded git history for `static/js/**/*.test.js` and `vitest.config.js` contains no changes from `288667d` through audited main. Packet F is already completed in the canonical record.

**Technical interpretation, not an owner ruling:** §0.1 requires “14 consecutive days with no `js-unit` failure”; §6.5 says a cancelled run “neither starts nor advances” the clock and a JS failure resets it. The unchanged corpus and failure-free calendar interval support completion without crediting the cancelled carrier; the rule specifies no minimum run count or closing-day execution. The earlier adviser wording “50 qualifying runs” was corrected during synthesis. This closes the bounded evidence gap in §11.3 without rewriting its historical reading, waiving a rule, or signing Q4/D2. Promotion still needs that separate signature and the enforcement prerequisites above.

### 11.6 Claude limits and the decision to add Codex

Count ten **completed, fresh-head** Claude reviews of eligible same-repo human code/workflow PRs. Log head SHA, attempted/completed/skipped/stale/failed status, duration, quota use where available, findings, duplicates and human disposition. Docs-only skips, bot/fork exclusions and incomplete reviews do not count as clean reviews. Keep the proposed 15-minute timeout, 20-turn limit and per-PR cancellation; do not silently retry through a paid API. Review remains advisory and never bypasses the owner merge gate.

Before enabling the pilot, prove two pushes on one PR receive reviews of their respective heads. The documented Claude review plugin can skip already-commented PRs; a comment on an older head is not current review. If freshness cannot be established with the pinned action/plugin, hold the pilot pending a reviewed invocation change. Keep untrusted PR code away from privileged execution and retain the least permissions needed for the authorized review output. Owner credential/app authorization is still outstanding. [Claude Actions documentation](https://code.claude.com/docs/en/github-actions)

After ten completed reviews, a material missed defect class established by human/existing review is the trigger to **propose**, not automatically launch, a separately funded Codex comparison on the same ten archived heads. The owner must first choose a hard spend cap and supply/authorize the API credential. Recommend a standing second reviewer only if the paired trial yields **at least two unique, human-confirmed actionable defects on at least two heads**, **at least 50% actionable nonduplicate findings**, and usage within that cap. A single independently reproduced high/critical security or data-loss defect may support an explicit owner exception; it never adds a service automatically. These are proposed thresholds, not measured results. This package requests no new expenditure.

### 11.7 Core milestone and publication prerequisites

**Core:** measured guard/E2E/Windows speed work, strict checks and qualified promotions, SHA/permissions/security hardening, deterministic monitoring of both Deep Gate workflows, skipped-test execution destinations, retry visibility, and the bounded Claude pilot. Keep branch/patch coverage measurement non-blocking. Preserve one `ci.yml` PR in flight and isolated implementation copies; B4 measurement must not delay B1 hardening. Compare creation-to-required-gate completion, queue time and total runner-minutes, not job duration alone; 12–15 minutes remains the initial objective, eight a measured second-stage target, six a stretch.

The watchdog must report non-success within one hour of completion and detect a missing scheduled run within 36 hours of its expected weekly slot; a manual run or the previous week's success cannot substitute. Keep Linux failures visible in their own issue. Give the six Windows-host cases in `tests/test_agent_workflow_contracts.py` an enforced Windows destination and the three installed-dependency cases in `tests/test_braces_override_contracts.py` an enforced destination with `node_modules`; assert execution rather than accepting skips. Report first-attempt E2E failures without silently changing the retry policy.

**Separate or deferred:** F1/F3 delivery receives its own scoped council/Gate 1; F2 signing, organization transfer, docs filtering, optional browser caching, mutation/coverage expansion and a second AI reviewer cannot become prerequisites for fixing core CI. Defer B5's additional scanner work until unique findings justify its maintenance and triage cost; retained required audits and the adopted security layers remain core. No scanner is removed in this consultation.

Delivery must build and smoke the candidate, create a distributable ZIP, record its digest and immutable artifact identity, then extract **that ZIP** for upgrade/recovery validation. Publication receives that same artifact through a direct dependency on the reusable build or explicit output forwarding; it cannot rebuild or silently substitute it. Keep existing install/migration/provenance/version gates. SBOMs describe the build inputs accurately, distinguishing build tools from bundled contents. Recheck the ZIP digest before attestation/publication. A later signing step precedes final smoke, ZIP, digest and recovery evidence. [GitHub dependency-output rules](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#needs-context)

| Unpublished-candidate scenario | Required evidence before publication |
|---|---|
| Fresh install | Distributed binary starts with expected catalog, writable runtime tree and a working basic plan/log/read flow. |
| First release | Extended historical-schema fixture carries routine/order, logged sets/history, profile/settings and stored program backups; candidate startup and restart preserve their values. No prior published release is needed. |
| Later upgrades | Previous released binary creates representative data; candidate extracted from the final ZIP preserves it in default and portable runtime locations. |
| Failed/interrupted upgrade | Take and verify a consistent **pre-upgrade** DB snapshot before first candidate launch; exercise documented restoration and restart with a compatible prior binary. First-release bootstrap restores and verifies the legacy fixture and retries the candidate instead of inventing a prior release. Prove history/settings/backups survive. |
| Publication | Exact `^v\d+\.\d+\.\d+$` tag on `main` matches both version files; release fan-in includes candidate recovery; expected checks and the adopted security-alert policy pass; final artifact digest, SBOMs and attestation match the tested ZIP. Owner controls the genuine tag/release timing. |

The pre-upgrade snapshot is substantive: at audited `7ac1af2d`, `app.py` initializes schemas and upgrades the catalog **before** `create_startup_backup()`, and `utils/auto_backup.py` can skip/return `None`. A candidate startup backup therefore cannot be assumed to restore the prior schema. Existing packaged smoke preserves one selection row and the legacy-file digest; it does not prove the history/profile/backups recovery matrix. This requirement concerns the delivery rehearsal and documented recovery procedure; it does not authorize changing startup order or backup semantics.

F1 artifact preparation → F3 candidate validation → publication replaces §4's F1-publication → F3 sequence. `workflow_dispatch` rehearsals publish nothing; `v0.0.0-rc.test` remains invalid under ADR-007. A GitHub prerelease flag does not create an RC tag class. Publication failures must leave a failed delivery visible, not a successful partially documented release.

### 11.8 Dispositions, disagreements and actual provenance

| Issue | Advice / disposition in this package |
|---|---|
| §3's immediate JS promotion and A2/Linux coupling | All three advisers favor independent evidence. Preserve original JS qualification and signature; remove the unrelated dependencies. The architecture adviser's targeted reconciliation supplements, rather than repeats, the earlier sample. |
| Mirrored PR/release sets and CodeQL scan success | Separate PR-only B3 from release evidence; use the explicit alert rule for CodeQL. Security adviser supplied the supported mechanism and bypass interaction. |
| §6's broad GitHub-owned allowance versus “adopted only” | Security adviser recommends explicit repositories with both broad flags false. Coordinator adopts the narrower policy; extra allowlist upkeep is accepted as the tradeoff. |
| F1 “goes first regardless” / F3 after publication | All three favor a separate delivery milestone and recovery before publication. Product adviser identified the pre-upgrade snapshot gap; security adviser binds evidence to the final ZIP. |
| Codex default versus a single severe miss | All support a bounded paired trial and objective default. Product adviser proposes a single high/critical defect exception; coordinator adopts it only as a separate owner exception, retaining the default threshold. |
| B5 extra scanner | Product adviser recommends deferral absent incremental value. Coordinator adopts deferral, rather than treating it as a core prerequisite. Existing required audits stay intact. |

No unresolved adviser disagreement remains over the recommended package; all owner choices remain unmade. The initial role assessments were independent. The coordinator subsequently asked for refinements to the AI threshold and JS cancellation treatment; those exchanges are synthesis, not additional independent reviews.

| Actual agent path returned in this consultation | Role / contribution | Status |
|---|---|---|
| `/root/gate0_ci_adviser` | CI architecture, performance, enforcement; targeted JS qualification gap | Completed advisory |
| `/root/gate0_security_adviser` | Security, supply chain, delivery; primary vendor-policy checks | Completed advisory |
| `/root/gate0_product_adviser` | Product risk, maintenance, cost; recovery acceptance | Completed advisory |
| `/root` | Coordinator; consolidated and appended §§11.4–11.9 | Document author |

These are native agents spawned for this request, not the earlier `/root/*_adviser` identities in §11.3 and not external Claude/Astra consultations. The older provenance is retained verbatim; no continuity or formal-council credit is claimed. All three requested assessments ran; no missing review is represented as “no findings.” No PM/council provenance is invented.

Evidence reused: §§2/10/11.3's audited commit/run and ten-run sample; ADR-007/ADR-011; canonical JS Gate 0 §§0.1/6.5/13.0. Narrow additional reads: the original Linux diagnostic GATE1 at `7ac1af2d`, the JS ledger gap, and the backup/startup assumptions above. No tests, DB mutations, dev servers or broad repeated audit ran. Security prerequisites use [GitHub code-scanning merge protection](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/manage-your-configuration/set-merge-protection), [rules API thresholds](https://docs.github.com/en/rest/repos/rules), [Actions policy flags](https://docs.github.com/en/rest/actions/permissions), and [dependency-review scopes](https://github.com/actions/dependency-review-action#configuration-options).

### 11.9 Approval boundary

**One requested owner decision: approve the complete CI-D1–CI-D11 Gate 0 requirements package in §§11.4–11.8 for formal council planning.** This includes core scope, conditional promotion criteria, review limits, deferrals, and the separately gated delivery direction. It does not sign Q4/D2, Gate 1 or a delivery plan, supply credentials, approve a purchase, change settings, claim packets, merge a PR or authorize publication. Those remain distinct owner actions at their stated gates.

Authority: [QUALITY_GATE.md, Plan-stage routing](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) requires **“Gate 0 (requirements approval) + Gate 1 (council-reviewed plan approval)”** for large/new-workflow work. This plan §0.1 additionally states **“Nothing in §4 starts before Gate 1.”** After Gate 0 approval, reconcile §§3–7 to this package through the formal council workflow; only its separately approved Gate 1 can permit implementation.

---

## 12. FORMAL CORE Plan v1 — 2026-10-19

> **Reviewed v1 audit trail:** the original Step-1 body below is retained; current operative dispatch detail is the reconciled §§0–9 and final Plan v2 in §12.4. Reviewers read the frozen full-document snapshot with SHA256 `B87313F1464F697FEA38267AAF6E89E697A0FDA21E68F7B963DF748919A63E84`. Their line references refer to that v1 snapshot, not the later expanded document. No historical v1 wording below overrides the five accepted v2 amendments.

This is council Step 1, distinct from historical **DRAFT v2**. Requirements brief and Gate 0 signature are in §1; §§0–9 are its reconciled packet detail. §§10–11 retain dated evidence and advisory findings only. The three formal reviewers must read this artifact independently before Step 3 synthesis and the same PM's Step 4 revision.

**Goal:** make core CI faster to reach a trustworthy required-gate result, enforce qualified security/check controls without weakening provenance, and expose scheduled failures, skipped tests and retry behavior.

**Scope:**
- **In:** B1/A1/B2/B3/A2/A3; B4 non-blocking measurement; C1–C5 settings proposals and verification design; D1 bounded credential-gated pilot; D3/E1 deterministic monitoring/split; E3 separately activated bounded diagnostic; G6/G7 execution destinations/retry reporting. Preserve local-first behavior and exact existing check names.
- **Out:** implementation during this request; owner settings, credentials, spending, merges and release actions; Q4/D2 signature; F1/F3 delivery (separate council/Gate 1); F2/A4/A5/B5/D2/G1–G5/G8 expansion; application/schema/API/calculation/visual-baseline changes.

**Artifacts proposed for later authorized core implementation:**

| Path | Change | Packet / contract |
|---|---|---|
| `.github/workflows/ci.yml` | Modify in serial packets | Pins/permissions; guard fan-in; cheap always-present B2; PR-only B3; Windows/E2E speed; executed G6 cases and G7 reporting; optional B4 measurement |
| `.github/workflows/deep-gate.yml` | Modify | B1 pins; E1 preserves six non-Linux jobs; compare logic moves intact |
| `.github/workflows/release.yml`, `.github/workflows/_packaged-windows.yml` | Pins/permissions or contract-preservation changes only in core | Preserve reusable caller/child names and install/migration gates; no artifact publication/signing additions |
| `.github/workflows/deep-gate-visual.yml` | Proposed new | E1 Linux schedule/dispatch compare; exact display name `Deep Gate Visual (Linux)` |
| `.github/workflows/deep-gate-watch.yml` | Proposed new | D3 deterministic per-workflow issues, current-slot freshness and timing evidence |
| `.github/workflows/claude-review.yml` | Proposed new, inactive until authorization/qualification | D1 advisory ten-review pilot; fresh-head/exclusion/privilege proof; no paid fallback |
| `scripts/release_gate.py` | Modify for staged promotion contracts | Distinct PR/release sets, exact SHA/newest run/trusted app preserved, B3 excluded from release |
| `tests/test_release_workflow_contracts.py` | Modify | Set floors/staging, exact names/apps, fan-in failure and reusable callers |
| Existing workflow contract tests; proposed `tests/test_ci_expansion_contracts.py` | Modify/add meaningful behavior tests | Aggregate result matrix, tool/policy configuration, monitoring current-slot logic, review freshness/exclusions; tests must check behavior, not mirror YAML |
| `tests/test_agent_workflow_contracts.py`, `tests/test_braces_override_contracts.py` | Execution destinations/assertions as necessary | Six Windows-host and three installed-dependency identities must execute; no skip-as-pass or deletion |
| `docs/test_inventory/` | Regenerate only on canonical triggers | Changed test identities/counts, functional spec list or parametrized surface additions/deletions |
| `docs/ai_workflow/QUALITY_GATE.md` | Narrow reference change | E1 Linux workflow location; preserve all existing quality requirements |
| `docs/deep_gate_linux_visual_failure_20260831/GATE2.md` | Diagnostic evidence only after named extension | Bounded one-capture comparison; no fix/baseline edits |
| `artifacts/ci_cd_expansion/` | Ignored evidence produced later | SHA/run/attempt/node identities, timings, seed proofs, settings snapshots/payloads, D1 attempt ledger |
| `docs/ci_cd_expansion/PLANNING.md` | Council record now; future packet ledger updates | Sole write artifact of this request |

**Effort:** L, multiple independently gated packets. **Owners:** proposed in §7, all unclaimed; council document owner `/root/product_manager`. **Depends on:** Gate 0 complete; formal council then owner core Gate 1; later implementation/activation authorities as §3. Reuse sufficient dated evidence rather than rerunning history.

**Sequence:**
1. Record Gate 0 and reconcile plan (this write); obtain independent architecture/test/product-risk reviews; preserve verbatim findings, actual IDs and every proposed disposition; same PM writes formal Plan v2.
2. Present Plan v2 for separate owner core Gate 1. Stop before implementation. Delivery remains separate and Q4/D2 remains unsigned.
3. On later authorized execution, use §5's serial workflow slots: B1 before optional B4; A1 benchmarking/fan-in; B2/B3; A2/A3/G6/G7; B4 only without delaying hardening. Keep isolated test/DB copies per the canonical workflow.
4. Qualify C1 security enforcement and independent C4 candidates, merge code/contracts first, then owner activates settings with current snapshot/readback and actual blocking proof. Preserve strict checks, app binding and the PR/release distinction throughout; no tag during transition.
5. Couple D3 to E1; execute E3 only under its named bounded extension. D1 starts only after owner OAuth/app and freshness/security proof; log ten completed eligible reviews, incomplete attempts separately. No optional/deferred packet holds core progress.

**Expected gates — proposed for test-strategist to assess:**
- **Current council:** product-doc-only editing, manual consistency review; no tests, DB, dev server or CI dispatch.
- **Future workflow packets:** full `pytest` plus `code-reviewer`; `architecture-reviewer` when jobs are added/removed/converted. Reuse the seven workflow-parser suites through the full run; do not infer coverage from filenames alone.
- **Scripts/Python/root configs:** derive targeted behavior coverage by stem and directory tokens, take the canonical union; `/verify-suite` for uncovered script/root-config changes or the named mandatory exceptions; pyright baseline diff on every Python change. No generic test reduction because the work is “CI.”
- **A1/A2/A3:** compare executed test identities (not counts) on representative runs, guard failure/cancel/skip/missing states all red the exact required fan-in; E2E four-leg fan-in stays required and spec list unchanged. Record queue-to-gate latency and runner-minutes.
- **Promotion/security:** reuse ten-green/JS bounded evidence where sufficient; remaining seeded job failures and actual merge-blocking proofs, CodeQL alert rule/bypass tests, exact check/app set readback; original JS signature separate.
- **G6/G7:** assert intended cases execute with host/dependencies and their failures reach required gates; verify recovered retries still appear without changing retry policy.
- **D3/E1/D1:** fixture/rehearsal matrices in §4; D3 issue/timing/current-slot correctness; no untrusted artifact execution; D1 two-head freshness and exclusion/privilege/quota behavior before activation.
- **Inventory/agent workflow:** regenerate inventory only for its canonical triggers with clean collection inputs; manual dry-run/self-review for the narrow QUALITY_GATE reference. No product runtime change, hence no new browser/manual product gate unless actual implementation expands that surface.

### 12.1 Agent provenance — formal core council

| Role / write | Actual agent path supplied by manager | Evidence |
|---|---|---|
| `product-manager` — Plan v1 | `/root/product_manager` | Manager supplied returned path; Section 0 reconciliation and formal v1 written by this agent |
| `product-manager` — response matrix + Plan v2 | `/root/product_manager` | Same recorded PM resumed by manager; wrote the matrix, v2 and operative catalog amendments |
| `architecture-reviewer` | `/root/architecture_reviewer` | Completed independent formal v1 review; AR-1/AR-2; verbatim §12.2 |
| `test-strategist` | `/root/test_strategist` | Completed independent formal v1 review; TS-1/TS-2/TS-3; verbatim §12.2 |
| `product-risk-reviewer` | `/root/product_risk_reviewer` | Completed independent formal v1 review; no findings; verbatim §12.2 |

**Same product-manager resumed for matrix + Plan v2?** **yes** — manager resumed `/root/product_manager` with `collaboration.followup_task`, supplying its recorded ID, all three returned reviewer IDs, verbatim outputs and proposed dispositions. This is the actual resume mechanism; no replacement PM or continuity claim is invented.

**Evidence gap:** **none**. Actual paths were supplied by the manager for all five provenance rows. Native role-directed agents used the repository charters; no external Claude or model-specific run is claimed. All three reviews completed independently against the frozen v1 snapshot. Historical adviser IDs remain distinct. No completed council work was repeated to manufacture evidence.

### 12.2 Reviewer findings

All outputs below are verbatim formal review results. Original line references identify the frozen v1 snapshot named above. Native role-directed agents read the plan independently under their respective charters; these are not external Claude consultations or claims of a particular vendor/model run.

#### architecture-reviewer — `/root/architecture_reviewer`

```markdown
Formal architecture review of **FORMAL CORE Plan v1**, independently read from `docs/ci_cd_expansion/PLANNING.md` §§0–12. Earlier advisory reviews receive no formal-review credit. Supporting source reads used audited `origin/main` `7ac1af2d`, preserving this older shared checkout and other sessions’ changes. No files were changed and no tests, workflows or settings were executed.

**AR-1 — `docs/ci_cd_expansion/PLANNING.md:267–270`, §12 artifact row at line 663 — D1 states the privilege boundary without defining the execution/configuration boundary.**

Risk: Eligible PRs include workflow changes, while the proposed reviewer receives OAuth credentials and comment capability. The plan does not identify which revision supplies its executable workflow, Claude settings, hooks, MCP configuration and plugin, or prevent inherited development permissions from executing PR-controlled code. At audited `7ac1af2d`, `.claude/settings.json:4–11` permits package installation, pytest and application startup, and lines 60–61 enable project MCP servers. Merely restoring trusted-base configuration does not establish a read-only reviewer: Anthropic documents that other executable project files can remain PR-controlled. This is a concrete configuration surface the security rehearsal must cover. [Claude action security documentation](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md#which-files-come-from-the-base-branch-on-pull-requests)

Fix: Specify trusted orchestration and an isolated, reviewed reviewer configuration/plugin that does not inherit development tools, hooks or project MCP permissions; treat the exact PR head as review data, restrict posting to the authorized output, and require adversarial workflow/configuration/package-script changes to prove that PR-controlled code cannot execute with credentials before D1 activation.

**AR-2 — `docs/ci_cd_expansion/PLANNING.md:277–285` — D3 recovery needs an executed-comparison predicate for the separated Linux visual workflow.**

Risk: E1 preserves existing inputs and behavior, but audited `deep-gate.yml` supports manual `run_visual: false` and `visual_mode: generate`. A successful workflow carrier therefore does not necessarily contain a successful comparison. D3 covers workflow conclusions, duplicate deliveries and recovery, but does not specify that recovery requires the visual comparison itself to execute successfully. The current-slot schedule rule governs freshness; it does not by itself define issue recovery.

Fix: Define visual-issue recovery from a successful, executed compare-mode job/step for the relevant workflow/head/run attempt; skipped or generation carriers cannot resolve it, manual runs cannot satisfy scheduled freshness, and stale deliveries cannot overwrite newer unresolved evidence. Add those cases to the existing D3 fixture/rehearsal matrix.

No application module, blueprint-registration, schema, database-access or response-contract change is proposed. The plan correctly preserves independent promotions, separate PR/release enforcement sets, protected names, the B1/B4 ordering boundary and delivery’s separate council/Gate 1.

**Needs revision**
```

#### test-strategist — `/root/test_strategist`

```markdown
Formal independent test-strategist review of FORMAL CORE Plan v1, read directly from `docs/ci_cd_expansion/PLANNING.md` §§0–12. Historical advisory reviews were not counted as formal review.

Coverage references below use audited `origin/main` commit `7ac1af2d2dc10be6bf6a5016c09bc5244cf37ed7`, because the shared checkout is older and contains other sessions’ changes. No files were edited, tests run, workflows dispatched, or settings changed.

## Required gates

- **This council:** manual consistency review only. Product-document planning requires no test run (`QUALITY_GATE.md:37`).
- **Every future workflow-edit packet:** full pytest plus `code-reviewer`; add `architecture-reviewer` when adding, removing, or converting jobs. This follows `QUALITY_GATE.md:35`, including new D1/D3/E1 workflows.
- **Scripts:** derive actual behavioral coverage by stem/directory-token search. Use `/verify-suite` when coverage is absent or a canonical mandatory exception applies. Every Python edit also requires the pyright baseline diff. Script filename mentions alone do not establish coverage.
- **Inventory:** regenerate with installed dependencies when canonical collection surfaces change; run its drift check. Do not regenerate merely because a workflow changed when none of the pinned surfaces changed.
- **E2E:** A3 needs representative executions of the unchanged 25-spec functional set across four runners, plus aggregate failure propagation. E1 needs Linux compare execution with existing visual policy preserved. Windows-visual promotion needs its separate real-comparison and failure-propagation evidence. These do not authorize baseline regeneration.
- **Settings and promotion:** local pytest cannot prove GitHub merge enforcement. Preserve the approved staged sequence of seeded job failure, code/contracts, separately authorized owner activation, exact context/app readback, and actual merge-blocking proof.
- **QUALITY_GATE reference edit:** manual dry-run/self-review in addition to the workflow packet’s gates.
- A blanket Chromium suite is not required merely because workflows change. `/verify-suite` remains required wherever the actual changed paths or milestone gate call for it.

## Existing coverage

| Planned surface | Verified coverage and limits |
|---|---|
| `ci.yml`, A1/A2 | `tests/test_guard_destructive_command.py` exercises the real hook in available PowerShell hosts. `tests/test_worktree_ci_contracts.py` verifies Operation A module/host selection and report rejection; `tests/worktree_cleanup/verify_ci_report.py` rejects empty, skipped, failed and errored reports and unequal host coverage. These do not yet establish the new A1 fan-in. |
| `ci.yml`, A3 | `tests/test_playwright_shard_launcher_contracts.py` pins equivalence with the required functional set, its 25-spec floor and resource isolation. It does not independently prove all four new matrix legs executed or propagated their failures. |
| Existing workflows and E1 | `tests/test_release_workflow_contracts.py` covers workflow/job/step census, protected names, reusable callers, weekly execution, skip/error suppression and generation guards. `tests/test_playwright_runner_contracts.py` binds visual consumers to the proper seed and checks functional exclusion. Both contain explicit references that must migrate with E1. |
| Workflow runtime/build conventions | `tests/test_python_version_contract.py`, `tests/test_node_version_contract.py`, `tests/test_css_cascade_contracts.py`, and `tests/test_compiled_css_drift_gate_contracts.py` cover runtime floors, measurement policy and compiled-CSS enforcement. Full pytest preserves these checks. |
| `scripts/release_gate.py`, C4 | `tests/test_release_gate.py` exercises newest-run selection, foreign-app exclusion, pending/missing/non-success evidence, pagination, version guards and fail-closed release fan-in. `tests/test_release_workflow_contracts.py` provides workflow wiring and name contracts. |
| G6 | At audited main, `tests/test_agent_workflow_contracts.py:275` has four skill cases per host and `:541` has two registration cases per host. The six `powershell` cases skip on Linux. `tests/test_braces_override_contracts.py:76` and `:91` provide three installed-dependency cases; `_run_node()` at `:29` skips them without `node_modules`. |
| G7 | `scripts/playwright_timing_report.py:46` reads attempts but sums duration at `:56`; it does not report first failures or recovered retries. `tests/test_playwright_runner_contracts.py:289` verifies report-path wiring, not retry-report behavior. |
| D3/D1/B2/B3 | No existing implementation establishes the new watchdog, fresh-head review classification or new security-job enforcement. The planned fixtures and live qualification proofs are necessary new coverage. |
| Planning/evidence documents | No application fixture or browser coverage is required for prose. Inventory outputs remain generator-owned. |

## Findings and coverage gaps

**TS-1 — Medium, nonblocking planning correction: explicitly name the existing-contract migrations.**

Plan v1’s artifact table (`PLANNING.md:664–667`) groups these under “existing workflow contract tests,” but several changes have concrete coupling:

- A1’s `test` → `pytest-core` rename breaks the parser in `tests/test_worktree_ci_contracts.py:49` and `:63`.
- A3 changes the literal excluded shard name in `tests/test_release_workflow_contracts.py:116`.
- C4 changes the 12/13-context assertions and imports in `tests/test_release_gate.py:14` and `:120`, alongside the workflow contracts.
- E1 changes the workflow census/job count at `tests/test_release_workflow_contracts.py:265` and `:289`, Linux conditions at `:627`, and baseline-generation guard at `:1127`. `tests/test_playwright_runner_contracts.py:39` and `:70` still read visual steps from `deep-gate.yml`.
- New D1/D3/E1 files must enter the workflow census without weakening its protection against undeclared workflows/callers.

**Proposed disposition: accept.** Add these explicit paths to Plan v2 and associate them with their packets. Preserve the positive/negative contract pairs when changing their wiring. In C4, test each supported staged set, both existing floors, B3’s exclusion from release evidence, visual membership exactly once, and composite-name resolution. Do not replace the existing assertions with permissive existence checks.

**TS-2 — Medium, nonblocking acceptance refinement: define execution evidence beyond identity presence.**

A1’s JUnit identity comparison (`PLANNING.md:206`) and G6’s enforced-destination requirement (`:313`, `:688`) are correct goals, but the verifier must distinguish a testcase element from an executed case. The existing Operation A verifier demonstrates this distinction by rejecting `<skipped>`, `<failure>` and `<error>` (`tests/worktree_cleanup/verify_ci_report.py:16`). Identity-set equality alone can conceal skips and duplicate shard execution.

**Proposed disposition: accept.** Plan the following in `tests/test_ci_expansion_contracts.py`, or a specifically named verifier suite if implementation extracts a helper:

- A1 partition evidence rejects missing identities, unexpected identities, unintended duplicate execution, skipped cases and absent/malformed reports. Separate deliberate failure rehearsals from green equivalence evidence.
- Benchmark against the same corpus/environment as the candidate; retain the dated 1,018-case evidence without making that historical count an eternal baseline.
- G6 records the exact six Windows-host and three dependency-case identities, required host/dependency preflight, and their executed outcomes.
- Prove removing a case, omitting its prerequisite, skipping it, or injecting failure cannot leave its enforced required destination green.
- Name the required aggregation path for G6 before implementation. Its enforcement must not depend on a still-unqualified Operation A promotion.

These are implementation acceptance cases, not requests to run them during council.

**TS-3 — Medium, nonblocking planning correction: give G7 a concrete report artifact and behavioral test target.**

G7 promises attempt-level reporting (`PLANNING.md:314`), but §12 names no report producer/helper path. The existing timing helper discards attempt statuses, and its current test verifies wiring only. Reusing it unchanged would not satisfy G7.

**Proposed disposition: accept.** Add a proposed attempt-preserving reporter path and a behavioral suite, for example `scripts/ci_retry_report.py` and `tests/test_ci_retry_report.py`, or explicitly name an extension of the existing helper. Use representative fixtures from the selected pinned reporters:

- First-attempt success; failure followed by recovery; exhausted retries.
- Multiple tests/shards with distinct identities and attempt numbers.
- Any configured pytest rerun output; no implicit introduction of reruns.
- Missing, malformed or partial report visibly classified as unavailable, never “zero retries.”
- Summary generation after successful and failed test steps, preserving the original test verdict and current retry policy.

The final packet’s gate follows the actual script implementation and verified coverage.

## Additional fixture requirements already supported by Plan v1

The proposed `tests/test_ci_expansion_contracts.py` should exercise the actual decision paths, including:

- A1/A3 aggregates: all dependencies successful versus failure, cancellation, skip or missing dependency.
- D3: synthetic clock/API histories for both workflow identities, current scheduled slot versus manual/previous-week evidence, in-progress/late/missing runs, duplicate deliveries, recovery and independent Linux issue state. Include pagination and unavailable API responses where used; unavailable evidence must not become a healthy result. Local fixtures prove classification, while dispatch/completion timestamps prove the one-hour/36-hour service targets.
- D1: eligible/excluded attempts, two-head freshness, stale-result handling, timeout/quota failure and non-counting of incomplete reviews.
- B2/B3/C1/C4: preserve the approved live seeded proofs; YAML inspection alone is insufficient.

## Conftest / fixture work

No new application blueprint, table, schema or response contract is proposed. No `tests/conftest.py` registration change is indicated.

Use temporary report fixtures, synthetic API histories and isolated rehearsal environments. Any future work touching tests, DBs or servers follows the worktree-isolation workflow and Operation A hold.

Known-red awareness remains unchanged: `e2e/program-backup.spec.ts:79` is the documented historical pollution flake; record isolation results if it reappears. Linux visual failures remain visible bounded residuals, not automatic permission to regenerate baselines. Preserve ADR-011’s 81 byte-gated captures and five semantic exemptions.

## Verdict

**Sound with TS-1–TS-3 incorporated as nonblocking planning refinements.** No blocking test-strategy objection requires a new council review. Workflow packets require full pytest; script-only packets may use genuinely mapped targeted coverage, with `/verify-suite` wherever canonical escalation applies.

This verdict approves no implementation or activation. Gate 1, JS Q4/D2, settings, credentials, spending, merges and publication remain unsigned or separately authorized. Delivery retains its own council/Gate 1, and B4 measurement must not delay B1.
```

#### product-risk-reviewer — `/root/product_risk_reviewer`

```markdown
Formal independent product-risk review completed against `docs/ci_cd_expansion/PLANNING.md` §§0–9, §§11.4–11.9 and FORMAL CORE Plan v1 §12, using the product-risk-reviewer charter, `CLAUDE.md`, `QUALITY_GATE.md` and `/council-plan`. Historical consultations were treated as evidence only.

**Findings: none within the product-risk charter.** No PR finding IDs are allocated.

The plan preserves the relevant invariants:

- **Calculation semantics and informational Effective sets:** §§1.3/12 expressly exclude application, schema, API, calculation and catalog changes (`PLANNING.md:86`, `:96`, `:652`). The proposed artifact list contains no calculation-engine or user-interface edits. No worked calculation example or migration note is missing for this scope; any later behavior change must return to the requirements and migration/test gates under `CLAUDE.md` §1.
- **Local-first behavior and terminology:** §1.3 excludes application authentication, cloud sync and telemetry (`PLANNING.md:86`). D1 concerns developer review of repository changes, introduces no user-data service, remains advisory and cannot patch or merge automatically (`:266–270`). No product terminology, navigation or ownership of the seven core workflows changes.
- **Backup and startup contracts:** Delivery remains outside this core council (`PLANNING.md:293`, `:300`, `:652`). Its retained requirements correctly distinguish a verified pre-upgrade snapshot from a startup backup taken after schema/catalog mutation (`:302`, `:605–608`), preserve routines/history/profile/settings/program backups, and bind recovery evidence to the final candidate ZIP. Those requirements explicitly authorize no startup-order or backup-semantics change. This respects `CLAUDE.md` §§1–2.
- **Parked work and visual-policy boundaries:** E3 preserves the named H-LINUX-UNSYNC-01 one-capture scope, requires a separately authorized bounded extension, and forbids broader investigation, baseline changes or a fix (`PLANNING.md:289`). I also read the referenced diagnostic GATE1 directly from `origin/main` because that file is absent from the shared checkout; its follow-on authorization and hard stops agree with the plan. No fatigue calibration or other parked product work is resumed.
- **Owner decisions and scope:** Gate 0 is recorded without signing Q4/D2 or authorizing execution (`PLANNING.md:104–106`, `:192`, `:727`). Conditional promotions retain independent evidence and distinct PR/release sets (`:539–558`). Delivery retains its separate council/Gate 1, and B4 cannot delay B1 (`:29`, `:230–232`, `:325–329`).

This verdict assesses the proposed core plan’s product boundaries; it supplies no Gate 1 signature, delivery approval or execution authority. The review was read-only: no edits, tests, DB/dev-server activity, settings changes or remote actions were performed. Existing dated evidence was reused.

**Plan respects product invariants**.
```

### 12.3 Response matrix

Manager proposed the following dispositions; the same PM incorporated every accepted change in the operative catalog and §12.4. They remain reviewable for the owner's Gate 1 decision.

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| AR-1 — D1 executable/configuration trust boundary unspecified | `/root/architecture_reviewer` | **accept** | §4 D1 and §12.4 use default-branch `workflow_run` orchestration tied to a recorded trusted revision, isolated `.github/claude-review/` configuration/plugin with no development settings/hooks/project MCP inheritance, exact head as inert data, minimal output tools, and adversarial workflow/config/package-script proof before activation. No secret-bearing PR-defined workflow executes. |
| AR-2 — visual recovery could accept successful skip/generation carrier | `/root/architecture_reviewer` | **accept** | §4 D3/E1 and §12.4 require a newer successful executed compare-mode job/step with matching workflow/head/run/attempt; skipped/generation success cannot resolve Linux issue, manual runs cannot satisfy freshness, stale events cannot overwrite newer unresolved evidence. Fixture matrix covers these distinctions. |
| TS-1 — existing contract migrations not explicitly named | `/root/test_strategist` | **accept** | §§4/12.4 name `tests/test_worktree_ci_contracts.py` for A1, `tests/test_release_workflow_contracts.py` for A3/census/E1, `tests/test_release_gate.py` for staged C4 sets, and `tests/test_playwright_runner_contracts.py` for E1 visual reads. Keep negative assertions, both floors, all staged sets, B3 exclusion, visual once and composite names. |
| TS-2 — identity presence is weaker than executed partition evidence | `/root/test_strategist` | **accept** | A1/G6 use same-corpus/environment baseline, full identities plus executed outcomes, no unintended duplicates/skips/missing/malformed reports. G6 six-case Windows leg feeds required `Run Tests`; dependency cases run after `npm ci` in `pytest-core`. No dependence on or implicit promotion of entire Operation A. Meaningful verifier/aggregate negative tests in `tests/test_ci_expansion_contracts.py`. |
| TS-3 — G7 needs a report producer and behavioral suite | `/root/test_strategist` | **accept** | Propose `scripts/ci_retry_report.py` + `tests/test_ci_retry_report.py`; preserve attempts/statuses, first success/recovery/exhaustion, shard identities, existing reruns, unavailable malformed/partial output, original verdict and retry policy; summary after successful/failed test steps. |

**Finding accounting:** five findings, five accepted, zero rejected, zero deferred. Product-risk reviewer completed its review with **no findings**; no synthetic finding is allocated. No deferral follow-up file is required. Architecture's “Needs revision” is addressed by the adopted AR-1/AR-2 plan amendments; this is a disposition, **not** a claim that the reviewer reread or approved v2. No reviewer returned the protocol's blocking verdict, and no repeat pass was requested or performed. The owner decides Plan v2 at Gate 1.

### 12.4 FORMAL CORE Plan v2

**Status:** formal core council complete; **owner approved Plan v2 at Gate 1 on 2026-10-19, including all five accepted findings; B1 alone authorized for implementation**. This is the approved plan, incorporating AR-1/AR-2/TS-1/TS-2/TS-3. Operative §§0–9 are reconciled to it; §12's v1 body and §§10–11 remain dated audit history. Approval covers the core plan only, not its separately gated activations or delivery. B1 execution is separately authorized in §13.

**Goal:** shorten the time from a code PR's workflow creation to a trustworthy required-gate result, preserve merge/release evidence integrity, add qualified security controls, and expose scheduled failures, previously skipped tests and recovered retries.

**Scope:**

- **In:** B1 action pins/least permissions; A1 guard split with fail-closed `Run Tests`; B2 always-present workflow lint and B3 PR-only dependency review; A2/A3 measured Windows/E2E optimization; optional non-blocking B4 measurement; C1–C5 reviewable settings/conditional-promotion design; D1 credential-gated ten-review advisory pilot; D3/E1 deterministic monitoring and Linux split; separately activated E3 bounded diagnostic; G6/G7 executed-case and retry visibility.
- **Out of the council request:** implementation (B1 subsequently authorized in §13); JS Q4/D2 signature; credentials/app authorization, spending, settings execution, PR merges and publication; delivery F1/F3 (separate scoped council/Gate 1), signing F2, cache/docs filtering/scanner expansion A4/A5/B5, Codex D2, G1–G5/G8 expansion, org/merge queue; application/schema/API/calculation/catalog/backup-startup or visual-baseline changes.
- **Unchanged product invariants:** local-first behavior; Effective Sets informational semantics; module/DB/response/logging conventions; no authentication/cloud sync/telemetry; no dormant product work reopened. Calculation surface `none`; no `tests/conftest.py` registration change indicated.

**Artifacts:** proposed paths for later authorized work, not files created by this council.

| Path | Change | Packet and acceptance contract |
|---|---|---|
| `.github/workflows/ci.yml` | Serial packet edits | B1/A1/B2/B3/A2/A3/B4/G6/G7; preserve exact required names and all-success fan-ins; no path-skipped B2; B3 PR-only |
| `.github/workflows/deep-gate.yml` | Pins, E1 move | Retain six jobs; preserve weekly/dispatch contracts |
| `.github/workflows/release.yml`, `.github/workflows/_packaged-windows.yml` | Pins/permissions/contract preservation only in core | Caller/child names, smoke/install/migration/provenance preserved; no delivery implementation |
| `.github/workflows/deep-gate-visual.yml` | New | E1 exact `Deep Gate Visual (Linux)` identity, existing schedule/dispatch/compare policy; no baseline regeneration |
| `.github/workflows/deep-gate-watch.yml` | New | D3 per-workflow issue state, current scheduled-slot freshness, executed-compare recovery and stale-event protection |
| `.github/workflows/claude-review.yml` | New, disabled until authorized/qualified | D1 trusted default-branch `workflow_run` orchestration; no executable PR workflow/configuration; exact-head eligibility/freshness |
| `.github/claude-review/` (reviewed prompt/settings/plugin policy) | New isolated trusted configuration | Pin/record trusted revision; no inherited development hooks/settings/MCP/tools; PR head inert, authorized output only |
| `scripts/release_gate.py` | Staged set migration | Separate PR/release sets; exact SHA, newest carrier, trusted app and fail-closed evidence retained |
| `tests/test_release_gate.py` | C4 update | Every supported staged set and existing 12/13 floors; missing/pending/non-success/foreign-app rejection, pagination/version/fan-in tests preserved; B3 absent from release, visual once |
| `tests/test_release_workflow_contracts.py` | A3/C4/E1/D1/D3/G6 wiring/census | Literal shard exclusion, declared workflows/job counts, caller/composite names, Linux conditions/generation guards and protected-name pairs; no permissive existence-only replacements |
| `tests/test_worktree_ci_contracts.py` | A1 parser migration | `test` → `pytest-core` while retaining Operation A module/host/report guarantees |
| `tests/test_playwright_runner_contracts.py` | E1 visual-source migration; G7 wiring | Move visual-source/seed reads; retain functional exclusion and report wiring |
| `tests/test_playwright_shard_launcher_contracts.py` | A3 existing contract preservation | Exact unchanged 25-spec set and resource isolation; real four-runner evidence supplements parser tests |
| `tests/test_python_version_contract.py`, `tests/test_node_version_contract.py`, `tests/test_css_cascade_contracts.py`, `tests/test_compiled_css_drift_gate_contracts.py` | Existing preservation gates | Full pytest retains runtime/measurement/CSS contracts; change assertions only when the approved wiring requires it |
| `tests/test_ci_expansion_contracts.py` | New behavioral suite | A1/G6 executed report/partition decisions, A1/A3/G6 aggregate result matrix, D1 trust/freshness/classification, D3 clock/API/recovery paths, B2/B3 policy wiring; test real decisions, not mirrored constants |
| `tests/test_agent_workflow_contracts.py`, `tests/test_braces_override_contracts.py` | Existing selected cases, destination enforcement as needed | Six Windows `powershell` identities plus three installed-dependency identities execute; no deletion/skip accepted as coverage |
| `scripts/ci_retry_report.py`, `tests/test_ci_retry_report.py` | New G7 reporter and behavioral tests | Attempts/statuses, distinct tests/shards, first failures/recovery/exhaustion, existing reruns, unavailable report handling; preserve original verdict/policy |
| `docs/test_inventory/` | Generator-owned output when triggered | Regenerate for actual identity/count/spec/parametrized-surface changes, then drift check; not on every arbitrary workflow edit |
| `docs/ai_workflow/QUALITY_GATE.md` | Narrow E1 location reference | Preserve requirements; manual dry-run/self-review |
| `docs/deep_gate_linux_visual_failure_20260831/GATE2.md` | Later diagnostic evidence only | Named, bounded H-LINUX-UNSYNC-01 one-capture extension; no fix or broadened hypothesis |
| `artifacts/ci_cd_expansion/` | Later ignored evidence | Same-corpus benchmarks/report identities, queue/gate/runner timings, seed proofs, settings snapshots/payloads, D1 attempts and D3 timing evidence |
| `docs/ci_cd_expansion/PLANNING.md` | Current council and later ledger | Sole file written by this planning request |

If implementation extracts a verifier/helper beyond this proposed suite, name it in that packet and derive its real script gates before writing it; no unlisted helper evades the canonical union. Existing tests may only be migrated for actual changed wiring, with their positive/negative guarantees retained.

**Effort:** L, multiple independently reviewable packets. **Owners:** §7 proposals, B1 now claimed by Codex `/root`; PM `/root/product_manager` authored the council artifact. **Dependencies:** Gate 0, council and owner core Gate 1 complete; only B1 execution authorized (§13). Every setting/promotion/credential/diagnostic/release boundary below remains separate.

**Sequence:**

1. **Gate 1 complete:** the owner approved Plan v2, all five accepted findings and provenance on 2026-10-19. Council completion itself authorized no execution; the subsequent owner instruction authorizes B1 only (§13).
2. **After later authorized implementation:** create the isolated checkout required for test/DB work and preserve other sessions' edits/Operation A hold. One `ci.yml` PR in flight. B1 takes the first hardening slot; B4 never delays it. B1 inventories/pins adopted direct/nested actions and least permissions; no broad future integrations are allowlisted.
3. **Required-gate speed and test integrity:** A1 benchmarks the current serial corpus/environment against each candidate partition shape and proves exact executed outcomes, no unintended duplicates/skips, and all-success `Run Tests`. B2/B3 follow B1, always-present lint on PR/main and PR-only dependency review. A2/A3 optimize independently of promotions, preserving host identities and the 25-spec/four-leg aggregate. Measure creation-to-required-gate completion, queue/job time and runner-minutes: 12–15 min initial objective, eight-minute second-stage target, six-minute stretch.
4. **Bring hidden coverage into existing enforcement:** G6 adds only the six-case `workflow-contracts-windows` leg to `Run Tests`; three dependency cases execute after `npm ci` in `pytest-core`. Their exact identity/outcome/preflight evidence must fail on removal, skip, missing prerequisite or report/failure. This neither waits for nor implicitly promotes all Operation A. G7 adds the named attempt-preserving reporter with unavailable-report classification, summaries on both successful/failed steps, unchanged test verdict and retry policy. B4 occupies a free slot after A1 as non-blocking measurement.
5. **Stage security/settings independently:** C1 proposes secret scanning/push protection/CodeQL, then baseline triage and native CodeQL High/Critical security-alert rule (`high_or_higher`, other alerts `none`) with explicit sole-owner PR bypass and seeded blocking proof. C2 strict preserves existing checks/bindings; C5 disables only the orphan and keeps history. After B1 inventory/pins, C3 proposes selected/full-SHA policy with both broad flags false. Owner separately executes reviewed current payloads and verifies readbacks; configuration alone is not proof of enforcement.
6. **Promote only qualified candidates:** §11.5 evidence reused plus each remaining proof/signature → code/contracts for that supported stage → owner PR-setting activation with `app_id: 15368` → exact readback and actual failing-check merge block. Target full sets are 18 PR / 17 release; existing floors stay enforced; B3 is PR-only, visual once. JS remains withheld until Q4/D2. Packaged smoke does not wait for A2; Windows visual does not wait for Linux diagnosis. Keep exact SHA/newest run/trusted app release provenance; no tag during partial transition.
7. **Observe both weekly workflows without false recovery:** ship E1 with D3 monitoring ready, or monitoring first. Classify this week's expected Monday slot using schedule-event evidence only; report non-success within one hour and missing slot within 36 hours, with real dispatch/completion evidence and visible platform-delay limits. Linux issue clears only on newer matching executed successful compare-mode evidence; skipped/generation/manual-as-scheduled/stale evidence cannot counterfeit recovery or freshness. Preserve independent six-job/Linux state. E3 requires its own named bounded extension, stops at attribution/inconclusive interval, and implements no fix.
8. **Pilot only after trust and credential qualification:** D1 uses default-branch `workflow_run` orchestration and recorded trusted executable/config/plugin revisions, validates eligible same-repo human PR/head/base metadata, reads head as inert data, and isolates review config from all development settings/hooks/project MCP permissions. Adversarial workflow/config/package-script and stale-result tests plus two-head freshness must pass before owner OAuth/app activation. Ten completed fresh-head reviews, 15 minutes/20 turns, existing subscription quota only; incomplete/stale/skipped/failed attempts recorded but not counted; no paid fallback, patch, merge or required check.
9. **Keep deferred/delivery work separate:** optional cache/docs filtering/scanner expansion/Codex/mutation/coverage/org transfer never hold core. F1 candidate artifact → F3 recovery → publication requires separate delivery council/Gate 1, final-ZIP identity and pre-upgrade recovery matrix. Exact owner-created version tags only, dispatch nonpublishing, signing/credential/spending and release timing separately authorized.

**Required gates and evidence:**

- **This council:** manual prose/consistency review only; no product-doc test run. Manager checked the proposed PowerShell example syntactically (one block, zero syntax errors, zero commands executed); PM checks review/provenance/matrix completeness. This is not settings or workflow validation.
- **Every workflow-edit packet:** full pytest and independent `code-reviewer`; add `architecture-reviewer` whenever jobs are added/removed/converted, including G6/D1/D3/E1. Preserve the named existing contract migrations above and their negative cases. A new workflow must be declared in census/caller tests.
- **Scripts/Python/root configs/milestones:** actual stem/directory-token behavioral coverage determines targeted tests; `/verify-suite` for missing coverage, mandatory exceptions, root-config cross-cutting changes or the applicable milestone gate. Python edits also run the pyright baseline diff. G7's named behavioral suite is necessary but does not weaken a stronger matching gate. No blanket Chromium run merely because a workflow changes.
- **A1/A2/A3/G6 runtime evidence:** same-corpus full identities and executed outcomes; reject missing/unexpected/duplicate/skipped or malformed/absent reports; separate deliberate failure rehearsals. All-success aggregate versus failed/cancelled/skipped/missing leg; A3 representative unchanged 25-spec execution across four runners; G6 prerequisite/removal/failure injections hit its existing required path.
- **C1/C4 promotions/security:** preserve dated ten-green and bounded JS evidence where sufficient; prove remaining seeded failures and actual GitHub merge enforcement after separately authorized owner activation. Local tests/YAML cannot prove merge blocking. C4 tests every staged set/floor, B3 exclusion, visual once, composite resolution, newest-run/SHA/trusted-app behavior; Q4/D2 separately signed.
- **D1:** meaningful eligible/excluded/fresh/stale/timeout/quota classification and trusted-source/config tests; adversarial PR workflow/hooks/MCP/plugin/package scripts cannot execute with secrets; exact-head two-push rehearsal and authorized-output boundary. Hold activation if the pinned action cannot meet these controls.
- **D3/E1:** synthetic clocks/API histories for both identities, pagination/unavailable API, current slot/manual/prior-week/in-progress/late/missing, duplicate/out-of-order events, compare/skipped/generation outcomes and recovery independent of freshness. Real Linux compare execution preserves ADR-011; real timestamps prove service targets. No snapshot regeneration or suppression of bounded residuals.
- **G7:** pinned-reporter fixtures for first success, recovery, exhausted retries, test/shard/attempt identities and any existing pytest reruns; missing/malformed/partial output visibly unavailable; summaries after success/failure cannot change verdict or retry policy.
- **Inventory/fixtures/known reds:** generator-owned regeneration plus drift check only on canonical triggers, with installed dependencies and clean glob surfaces; no `tests/conftest.py` change. Temporary reports and synthetic histories; isolated rehearsals under worktree rules. Preserve known-red policy and ADR-011's 81 byte-gated captures/five semantic exemptions; a historical flake or Linux residual is not permission to weaken enforcement.

**Completion criterion for the later core milestone:** accepted packets have their applicable gates/evidence recorded, settings and candidate promotions show only actually authorized state, D1/E3 are reported accurately as completed or explicitly held at their independent activation boundary, and delivery/deferred work stays separate. No unsigned conditional item is represented as done merely to close the milestone.

### 12.5 Sign-off — core Gate 1

- [x] Gate 0 complete for the full CI-D1–CI-D11 requirements package, 2026-10-19, with §11.9 boundaries.
- [x] Every formal finding has a disposition: AR-1/AR-2/TS-1/TS-2/TS-3 accepted and incorporated; product-risk review has no findings.
- [x] Agent provenance complete: both PM writes, same PM resumed yes, all three reviewer IDs and evidence gap none.
- [x] Owner approved FORMAL CORE Plan v2 including all five accepted findings, 2026-10-19.
- [x] B1 authorized for implementation, full applicable gates, independent code review, push and ready PR; stop before merge. Other packets and execution-specific owner gates remain separate.

**Delivery Gate 1:** not requested by this council and not approved. **JS Q4/D2:** unsigned. **Settings/credentials/spend/merges/publication:** not authorized by this planning request.


## 13. B1 execution — 2026-10-19

The owner approved §12.4 at Gate 1 including AR-1/AR-2/TS-1/TS-2/TS-3,
and authorized **B1 only**: inventory and SHA-pin adopted direct/nested actions,
explicit least permissions, full pytest and the actual-diff gates, independent
code-reviewer review, resolve findings, update this ledger, push and open a ready
PR. Stop before merging. This execution record supersedes earlier planning-only
pending/unclaimed statements for core Gate 1 and B1 only; historical council text
is retained. No Q4/D2 signature, promotion, settings, credentials, spending,
delivery approval, release publication or merge authority follows.

- Claim: Codex `/root`, 2026-10-19; branch `ci/b1-action-pins`.
- Isolation: standalone HTTPS clone (initially shallow) at
  `D:/development/Hypertrophy-Toolbox-v3-ci-b1-shallow-20261019`, from current
  `origin/main` `7ac1af2d2dc10be6bf6a5016c09bc5244cf37ed7`. No linked worktree,
  shared DB, cleanup/ref retirement, stash, reset, or other-session edit.
  The first full-history clone was slow and stopped; its incomplete directory
  `D:/development/Hypertrophy-Toolbox-v3-ci-b1-20261019` is retained.
- Approved local plan copied from the shared checkout without editing its source;
  source SHA256 `A994FC1B5AEBAD7036AD12ECE2CF12D79AA8040B2D6833F7CC59A94C403BDF33`.
  No other dirty source file is imported. Existing baseline/qualification evidence
  is reused; B4 is not started.
- Open-PR check at claim: only #520, documentation archival; no `ci.yml` PR.
- Planned diff: four workflow files plus this plan and B1 action/permission inventory.
  No job added, removed or converted; required gate is full pytest plus independent
  code-reviewer. No Python, test identity, shard/spec, root-config or product diff
  is planned, so no pyright, inventory regeneration or extra Chromium gate is derived.
- Implementation commit: `1dfe011b1533f1339660b72a60249b390b296104`.
  Four actions / 85 remote calls pinned; CI and Deep Gate default to `contents:
  read`; CI's API-free E2E fan-in uses `{}`; the existing release `checks: read`
  exception is preserved. [B1_ACTION_INVENTORY.md](B1_ACTION_INVENTORY.md) records
  exact pins, upstream metadata, all three reusable callers and permission needs.
- Metadata/structure run `b1-structural-and-metadata-verification`: **PASS** at the
  implementation commit against the base above. Parsed workflows are identical
  after normalizing only pins and the three permission additions; job names,
  conditions, triggers, matrices, steps, contracts and enforcement are unchanged.
- Independent code-reviewer **`/root/b1_code_reviewer` completed with no findings**
  on implementation `1dfe011b1533f1339660b72a60249b390b296104` versus base
  `7ac1af2d2dc10be6bf6a5016c09bc5244cf37ed7`. It independently compared Git blobs
  and freshly retrieved official tags/exact-SHA metadata. No tests, DB/server
  activity, source edits or additional agents were performed by the reviewer.
- Final diff is four existing workflow files and two CI-expansion documents.
  Full pytest and independent code-reviewer are the required union; no job is
  added/removed/converted, no Python/root config is changed, and no test identity
  or functional spec list changes. No architecture review, extra Chromium gate,
  pyright run or test-inventory regeneration is derived. Ledger closeout is
  documentation only, manually checked; the reviewed workflow/test tree stays
  byte-identical to the implementation commit.

### 13.1 Exact local test evidence

The standalone clone has its own venv, npm dependencies and runtime path. Python
3.14.6 / pytest 9.1.1. The initial setup attempt was interrupted after exposing
an unnecessary `DB_FILE` override and missing shallow-history ancestry. Removing
that process override restores the clone-local default DB path. A Git transport
fetch of exact base `7ac1af2d2dc10be6bf6a5016c09bc5244cf37ed7` from the shared
checkout supplied its committed ancestry without importing working files, shared
objects, alternates or worktree metadata. The clone is now non-shallow. Both
specific environment checks passed (`2 passed in 0.19s`). The interrupted attempt
is retained as `pytest-first-attempt*`, not credited as a complete run.

| Run | Exact implementation commit | Command / environment | Result |
|---|---|---|---|
| `b1-local-full-pytest-attempt-2` | `1dfe011b1533f1339660b72a60249b390b296104` | `python -m pytest tests/ -q --junitxml=artifacts/ci_cd_expansion/b1/pytest-full.xml` | **5,242 passed, 2 skipped, 1 failed**, 1514.51s; exit 1. Sole failure: Windows selected `C:/WINDOWS/system32/bash.EXE`, the unconfigured WSL launcher, for the existing Deep Gate selector contract. |
| `b1-local-bash-contract-repair` | same workflow/test tree | Process-local PATH prepends `C:/Program Files/Git/bin`; `python -m pytest tests/test_playwright_runner_contracts.py -q --junitxml=artifacts/ci_cd_expansion/b1/pytest-bash-repair.xml` | **12 passed in 0.47s**, exit 0, including the sole failed identity and all selector-negative cases. No repository/test change. |

Full-run UTC interval: `2026-10-18T21:52:40.5614657Z` to
`2026-10-18T22:17:56.0167874Z` (2026-10-19 locally). The full run and repaired
contract run cover **5,243 distinct passing identities plus two existing skips,
zero unresolved failures**. JUnit identity reconciliation verifies that every
rerun identity belongs to the full run and replaces its sole failure. This is
full-run evidence plus a targeted environment repair, **not a claim that the
original full invocation exited zero**. Reuse of the other 5,242 passes avoids
repeating the unaffected guard/lifecycle corpus.

The two skipped identities and unchanged reasons are:

- `tests.test_package_asset_staging::test_executable_bit_survives_staging` —
  Windows filesystems carry no executable bit.
- `tests.test_priority7_error_handling.TestWorkoutLogEndpoints::test_update_workout_log_success`
  — happy path covered by `test_workout_log_routes.py`; this app has no fixtures.

Raw evidence is retained under `artifacts/ci_cd_expansion/b1/`: full and repaired
JUnit/logs, `pytest-full-result.json`, `validation-summary.json`,
`verification.json`, upstream metadata/commit records, and `code-review.txt`.
`validation-summary.json` records the SHA256 receipts below.


| Evidence | SHA256 |
|---|---|
| `pytest-full.xml` | `2da8e36d01b696eea7ea6d8d9e86146d1d21be29ca92721fe703f0fd9902004b` |
| `pytest-bash-repair.xml` | `a2d5717a582c7b579504243a48336f1dcff5342c7927ac1dc55259f8082bdb2d` |
| `verification.json` | `c6f49f6a55347f8e587fa3f941920c38dbd7b28e136fb19744beca3e6f315da3` |
| `code-review.txt` | `1429706385888feb09ca1ae79aeef1b921d8bb386f7f93912fab45766a3f717b` |


### 13.2 Publication boundary

Local gates are complete using the exact evidence above. Push and ready PR are
owner-authorized; PR/run IDs will be recorded after GitHub assigns them. GitHub CI
is separate runtime evidence and is not represented as passed before completion.
The branch stops before merge. No other packet, promotion, setting, credential,
spend, delivery or release action was executed.
