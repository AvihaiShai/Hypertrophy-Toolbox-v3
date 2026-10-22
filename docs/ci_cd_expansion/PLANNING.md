# CI/CD Expansion — Planning

| Field | Value |
|---|---|
| Status | **Core Plan v2 owner Gate 1 remains approved. G6 #552, standalone Q4 #554 and G7 #557 are merged; their exact-main push runs succeeded. JS Unit is now named `JS Unit (Vitest)` and remains unprotected.** Current completion receipts are in §7 and §22.7. C4 is preparation only: explicit JS-only code/contracts authority and later settings/blocking proof remain separate. S3/WS5 retains the next shared workflow slot under its own authorization; dated implementation evidence below remains historical. |
| Authors | Historical draft: Claude and Astra, 2026-10-18. Formal council document owner: `product-manager` `/root/product_manager`, 2026-10-19; read-only manager `/root`. |
| Source of truth | This file. The chat threads that produced it are not. |
| Baseline measured | `origin/main` `7ac1af2d`, CI run `39125460089`, 2026-10-18 |
| Planning size | Large (new workflows, new jobs, repo-settings changes) — per `docs/ai_workflow/QUALITY_GATE.md` plan-stage routing: Gate 0 → council (`/council-plan`) → Gate 1 → implementation |
| Branch / PR | G6 [#552](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/552), final head `2e480330930f01fc4dffd3f68689c2d4227c74ec`, merged `155181d67a89fe72e86c75a1ff438caec250a9bd`; Q4 [#554](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/554), final head `316d7f69930b11d80b089b8c7956d296949f08ac`, merged `73de866ecb22bc8472dafb85f1405a27caf6513b`; G7 [#557](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/557), final head `4473c913cbb060602981e73696e682f31d81a9f3`, merged `b77cb742f3af5222d9d80b608d497390c4b3e4f2`. Retain branches and dated receipts. Lane07's bounded record PR changes no workflow or setting. |

### Review log

| Date | Reviewer | Kind | Disposition |
|---|---|---|---|
| 2026-10-18 | Astra | Preliminary peer review of v1 (not council) | 8 points: all accepted or adjusted, see §10. Five factual corrections folded into §0–§2. |
| 2026-10-19 | Owner | Gate 0 decision | Approved the complete CI-D1–CI-D11 package in §§11.4–11.8 with §11.9 boundaries; request quoted in §1. No implementation or settings authority. |
| 2026-10-19 | `/root/product_manager` | Formal core council Step 1 | Reconciled §§0–9 and drafted §12 Plan v1. Formal reviewers, response matrix and Plan v2 pending. Historical consultations receive no formal-council credit. |
| 2026-10-19 | `/root/architecture_reviewer`, `/root/test_strategist`, `/root/product_risk_reviewer` | Formal independent council Step 2 | All completed; AR-1/AR-2 and TS-1/TS-2/TS-3 recorded verbatim in §12.2; product-risk review returned no findings. |
| 2026-10-19 | `/root` → resumed `/root/product_manager` | Formal Steps 3–4 | Manager proposed acceptance of all five findings; same PM wrote §12.3 matrix and §12.4 Plan v2, completed provenance, and reconciled operative §§0–9. No reject/defer or repeated review pass. |
| 2026-10-19 | Owner | Core Gate 1 and B1 execution | Approved §12.4 including the five accepted findings; authorized B1 implementation, gates, independent code-reviewer, push and ready PR. Stop before merge; §13 records execution. |
| 2026-10-20 local (+03:00); 2026-10-19 UTC | Owner | B2 and E1+D3 execution; ledger follow-up | Authorized B2, E1+D3 as one coherent observability change, four documentation follow-ups, and implementation/tests/independent reviews/bounded rehearsals/commits/pushes/ready PRs. Stop before merge. Settings, C4, credentials, spending, release publication and B3+ excluded. §15 quotes the boundaries. |
| 2026-10-20 | Owner; Codex consulting team | Named PR decisions and execution | Owner asked the AI consulting team to decide and proceed with #531, #532 and #533. Three independent read-only advisers recommended proceeding; Codex adopted the decisions and merge sequence in §16.8. Earlier stop-before-merge instructions are superseded for these three PRs only. |
| 2026-10-20 local (+03:00) | Owner | B3 execution; delegation of in-scope decisions | Authorized B3 under the approved core plan: implementation, required tests and independent reviews, commits, push and one ready PR. Stop before merge. No settings change, check promotion, C4 or A2. Delegated unresolved in-scope technical and plan-disposition decisions to an AI consulting team. §17.1 quotes it. |
| 2026-10-20 | Architecture (`a67569b0e01c8f77e`), testing (`ac33d32e838b19c24`) and security/product-risk (`a58655a4066be0189`) advisers; adopted by manager session `hypertrophy-toolbox-v3-main-68` | Delegated B3 decision panel | Three independent read-only advisers on one brief; one security blocking item, resolved by adoption; dissent recorded. The manager adopted seven decisions under the owner's delegation (§17.3). Not an owner signature and not a formal council; implementation reviews remain separate. |
| 2026-10-20 | Owner | B2 residuals; delegation to an AI consulting team | Asked session `hypertrophy-toolbox-v3-main-4e` to work the workflow-lint leftovers with the AI consulting team until done. Applied as §17.1-style delegation with stop before merge; §18.1 quotes it. |
| 2026-10-20 | Architecture (`a25abea4397d97c42`), testing (`a32c0e2f4bd93f237`) and security/product-risk (`a2fd2bc67f77c955c`) advisers; adopted by session `hypertrophy-toolbox-v3-main-4e` | Delegated B2-residuals decision panel | Three independent read-only advisers on one brief; no blocking item; dissent recorded. Eight decisions adopted (§18.3). Not an owner signature and not a formal council; implementation reviews remain separate. |
| 2026-10-21 local | Owner | #546 against post-A2 main | Asked for #546 to be resolved against current `main`, preserving merged A2 behavior, with the affected gates and required reviews completed, and presented ready for a separately authorized merge. §18.7 records the merge of `43f5df33`. |
| 2026-10-21 local | Owner | A2 named-head merge and A3 execution | Approved merging #540 at `30c88a2e`, then continuing A3 from merged main. Merge `43f5df33` independently read back; §20 records A3 execution and the separate #546 workflow-slot constraint. |
| 2026-10-21 local | Owner | CI implementation lane continuation | Directed the sole workflow-editing lane to resume retained A3 from `398b0564`, refresh it on current main and prepare a ready PR; G6 follows an explicitly authorized A3 merge and G7 follows G6. Independent isolation, required gates/reviews and named-PR merge authority remain binding (§20.6). |
| 2026-10-21 local | Owner | Named A3 merge and G6 continuation | Explicitly approved merging #549 at `f069bed1`, then continuing G6; prohibited every other merge without separate explicit approval naming its PR (§§20.7, 21.1). |

---

## 0. Operating protocol — reconciled 2026-10-19

Other sessions share this repository; preserve their changes. The council originally owned only this planning document. The owner subsequently approved core Gate 1 and authorized B1 alone; §13 records that authority. The following controls apply to implementation; they do not authorize any other packet.

1. **Nothing in §4 starts before its applicable Gate 1 and execution authority.** Gate 0 was approved 2026-10-19 for requirements and formal core planning only. Formal core council and owner Plan v2/Gate 1 approval are complete; packet execution authority is recorded in §§13–20; the current owner request authorizes A2 → A3 → G6 → G7 in the serial workflow slots (§§19–20). F1/F3 require their own scoped delivery council/Gate 1. §10 and §11 consultations are advisory evidence, not formal reviews. Q4/D2, credentials, spending, settings, PR merge and publication remain separate owner actions.
   *Dated supersession, 2026-10-20 (2026-10-19 UTC):* the text above is retained as written. A1 (§14) and E3 later received their own authority and merged. The 2026-10-20 owner authorization adds execution authority for **B2 and E1+D3 only** (§§15–16); B3 and every later packet still lack it.
   *Dated supersession, 2026-10-20 (B3):* the text and note above are retained as written. A later 2026-10-20 owner authorization adds execution authority for **B3 only** (§17), stopping before merge. A2 and every later packet still lack it.
2. **Claim before you start.** Write your name and the date in the §7 ledger row. One packet is one PR. Two agents never hold the same packet.
3. **Isolated implementation copies.** Follow `docs/ai_workflow/PARALLEL_WORKFLOW.md` and `scripts/new-worktree.ps1` before parallel work touching tests, DB or dev servers, preserving the Operation A hold. Read-only council reviewers and one planning-document writer need no DB/worktree activity. Never stash, reset or incorporate another session's changes.
4. **One `ci.yml` PR in flight at a time.** Proposed order: B1 → A1 → B2 → B3 → A2 → A3 → G6 → G7; B4 may follow any merged slot after A1, but **must never delay B1**. E1/D3 and promotion-contract packets also serialize whenever they touch the same workflow. Each starts from current `origin/main` after the prior merge; merges require owner authority. B2/B3/G6/G7 priorities may move between free slots without weakening their dependencies or gates.
   *Dated note, 2026-10-20:* the text above is retained as written. E1+D3 departs from "each starts from current `origin/main`": its PR carries B2's commits and merges after B2 (§15.2 and §16.2).
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
| G4 | Distinct enforcement sets preserve intent | Conditional promotions follow §11.5. Code/contracts declare `PR_REQUIRED_CONTEXTS` (target 18) separately from `RELEASE_EXPECTED_CONTEXTS` (target 17); owner applies only qualified PR checks with app binding. Existing enforcement never weakens; Q4 is approved and D2's ledger condition is met. The standalone rename and C4 activation remain separate (§21.3). |
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
| CI-D3 | Four independent conditional promotions; B2/B3 required after qualification | §11.5 proof matrix; Q4 approved and standalone rename merged through #554; D2 historical ledger condition met (§21.3). JS-only C4 code/contracts and live enforcement proofs precede separate owner settings activation. Separate PR/release sets; no A2 or Linux coupling. | C4 |
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
| C4 | After candidate qualification/signatures and code/contracts merge: `strict: true`, `checks: [{context: <exact observed name>, app_id: 15368}, ...]`. Preserve existing checks/bindings; include only the currently qualified approved subset, not all 18 target members. Q4 approved; D2 ledger condition met; rename and C4 activation remain separate (§21.3). No context-only POST. |
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

B1 was claimed by Codex `/root`, 2026-10-19, and merged through #521 (§13.2). A1 was claimed by Claude Code, 2026-10-19, under separate owner authority (§14), and merged through #530. E3 was held by another session under its own authority and merged through #529. B2, D3 and E1 are claimed by the CI coordinating lead under the 2026-10-20 owner authorization (§15). B3 is claimed by Claude Code session `hypertrophy-toolbox-v3-main-68` (Opus) under a separate 2026-10-20 owner authorization (§17). A2 merged under §19. A3 merged through #549 (§20.7). G6 #552 is integrating current main after U1 #551, with fresh-head gates and explicit merge approval pending (§21.4). G7 remains unclaimed and requires its own separate approval after G6 merges. Other packets remain unclaimed under their existing authority boundaries. Merge receipts for A1 and E3 were verified by the lead with `gh pr view` / `gh run list` at 2026-10-19T22:1xZ and recorded by the product-manager; §§13–14's historical receipts are not rewritten. Core Gate 1 is approved; `blocked` now names remaining packet-specific prerequisites or execution authority, not missing core Gate 1 or Gate 0. `deferred` and `separate milestone` distinguish excluded work. No PR/head/run is invented; §11.5 evidence qualifies only its named criterion, never implementation or owner approval.

| Packet | Owner (proposed) | Status | Branch / PR | Head SHA | Evidence (run id, job, value) | Notes |
|---|---|---|---|---|---|---|
| A1 | Claude Code (A1 session), 2026-10-19 | **merged** 2026-10-19T19:06:48Z by AvihaiShai as squash `f3adacf1c1b48cc6e2c7ca9ac900e3294b3bae2d` | `ci/a1-guard-split-b`; [#530](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/530) | published head `18fc388a38cd4efcd9140aaf9cdfa3f49b0ad6db` (code tree `0e4f342` + review nits, §14.6); final PR head `699c56820603237fc490ced3114d359b00f37cf9` | PR run `39289691671` 25/25 success, last required context 10.4 min (baseline 28.2–32.3); bench `39270742974` attempts 1–2; rehearsals `39285097596`, `39285103455`, `39285105591`, `39285108590`, `39285112726`, `39288227037`; local full pytest 5,330 passed / 2 skipped at `0e4f342`; §14. Final head: PR run `39291809942` (`pull_request`, attempt 1) success, rollup 25/25 success. Post-merge `main` push run `39308234107` on `f3adacf1`, attempt 1, success | Closed. Final head advanced after §14.6; §14's receipts are historical. `download-artifact` joins the C3 candidate set. §14.7's post-merge timing confirmation is not recorded here; no scheduled Deep Gate has run since A1 |
| A2 | Codex `/root` | merged | `ci/a2-operation-a-parallel`; [#540](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/540) | approved head `30c88a2e`; merge `43f5df33` | Final run `39493591638`: 27/27 jobs successful; exact 251-case Counter preserved; Windows jobs 439 s / 432 s vs serial 677 s; independent reviews no findings | Owner named-head merge approval, 2026-10-21 local; §19 |
| A3 | Codex `/root`, resumed 2026-10-21 | **merged** 2026-10-21T17:38:23Z as `dee3c379` | `ci/a3-functional-four-shards`; [#549](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/549) | approved/tested head `f069bed180e425bd1dbdf3967a19b246b3d5271e` | Exact-head CI `39613142357`: 29/29 jobs success; fresh four-report Counter equals 540 passing identities/25 specs; source reviews pass. Actual PR wall 485 s, functional aggregate 423 s; historical 499→367 pair remains dated (§20.7) | Only this named PR was authorized to merge. Source/evidence/checkouts retained; G6 now follows merged main |
| A4 | Astra | deferred | | | | Optional cache experiment outside core |
| A5 | either | deferred | | | | CI-D5; no docs filtering in core |
| B1 | Codex `/root`, 2026-10-19 | **merged** 2026-10-18T23:46:43Z by the owner as squash `77f400bb331e1de631a32114a7cc9996f5b5dd1e` | `ci/b1-action-pins`; [#521](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/521) | implementation `1dfe011b1533f1339660b72a60249b390b296104`; final PR head `c91986bf376a1a09f055c4ee4dc4cb4d27bb601e` | Local: §13.1 unchanged. PR run `39171777513` (final head) 19/19 success; post-merge `main` push run `39177927596` on `77f400bb` success; post-merge scheduled Deep Gate `39226020933` 6/7 success, only pre-existing `visual-linux` red; §13.2 | Closed. C3/settings remain unauthorized |
| B2 | Claude Code (Opus) CI coordinating lead, 2026-10-20 | implemented; local gates, acceptance rehearsals and both delta reviews complete (code-reviewer approve, architecture-reviewer approve with nits); **merged** 2026-10-20T13:12:10Z as squash `1a5e0e6f` | `ci/b2-workflow-lint`; [#532](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/532) | base `origin/main` `f3adacf1c1b48cc6e2c7ca9ac900e3294b3bae2d`; implementation `704016f5e01f26c2b5efbf0b3678593d060f0794`, review fixes `9823beb9c7ba1f3f800dcfdabca349c472035595`; published head `d5dfa0615fb5770dca2fab50a8d052211c99308b` | PR run `39344273368` (`pull_request`, attempt 1, head `d5dfa061`) 26/26 success, `Workflow Lint (actionlint + zizmor)` 10 s, name observed exactly; local full pytest 5,356 passed / 2 skipped / 0 failed at `9823beb9`; targeted contracts and mutation 74/74 killed, 6/6 controls green at `d5dfa061`; rehearsals `39342689323` green control success, `39342691486` seeded PR-title red (both linters); baseline §15.3; §§15.5–15.6 | First main-push run `39428398134`: lint job `118646704773` and both linters succeeded (§15.6); missing post-merge lint evidence complete; overall pipeline 26/26 success (§16.9). Not in `REQUIRED_CONTEXTS`; promotion is C4. §15.5 residuals: `ci/b2-residuals`; [#546](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/546), merged as `28484dda` at 2026-10-21T12:40:52Z (§18; readback §20.6) |
| B3 | Claude Code session `hypertrophy-toolbox-v3-main-68` (Opus), 2026-10-20 | implemented; gates, rehearsals, reviews and delta reviews complete; **merged** 2026-10-20T20:07:19Z by AvihaiShai as squash `1f5ae0f0` from head `b7a6fecf` (PR run `39484164996` 27/27); main push `39489279999` success, `Dependency Review` skipped (§17.7) | `ci/b3-dependency-review`; [#539](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/539) | implementation `90cde802e4ed4215db6e11e4d4ecd737380bdb15` (parent `71c4cc6d`); receipts commit follows | Full pytest 5,580 passed / 2 skipped / 0 failed at `90cde802`; rehearsal push runs `39474857728` (a, success), `39474859322` (b, failure), `39474857709` (c, failure), `39474857803` (d, success); mutation 73/73 arms (63 red killed, 10 green held); B3 contracts 11/11; inventory 3,550; PR CI pending when written, superseded by §17.7 (final head `b7a6fecf`, PR run `39484164996` 27/27); §17.5–17.7 | After B2 (merged). Owner authority and delegated decisions §17; stop before merge. Not in `REQUIRED_CONTEXTS`/`EXPECTED_CONTEXTS`; promotion and blocking proof are C4 |
| B4 | Claude | blocked | | | | After A1 free slot; non-blocking measurement; never delays B1 |
| B5 | Claude | deferred | | | | Unique scanner value unproven; no removal |
| C1 | S2 (bounded owner authority) | **partial activation**; CodeQL/rule/proofs prepare-only | `docs/s2-settings-activation-20261022`; [#555](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/555) | content `bddfd74` on base `155181d6`; final head in PR metadata | Secret scanning enabled 2026-10-21T21:43:46Z; clean paginated observed baseline 0 all/open/resolved; push protection enabled 21:50:09Z after claims notice; full private before/after + pre-tested rollback | [SETTINGS_ACTIVATION.md](SETTINGS_ACTIVATION.md): DELEGATED three-adviser gate classification; historical scan completion unverified; D-6 preserved; no seeded public proof or bypass executed. 2026-10-22: C1b/C1c completion package prepared read-only (private `artifacts/c1bc-codeql-prep-20261022/`); owner decisions D1–D8 pending; nothing activated |
| C2 | Owner; S2 prepares | **prepared; not activated** | `docs/s2-settings-activation-20261022`; [#555](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/555) | content `bddfd74` on base `155181d6`; final head in PR metadata | Exact strict-only PATCH, expected full-object comparison and rollback prepared; live strict false and existing 12 check/app bindings preserved. Re-read 2026-10-22T15:27Z at `b77cb742`/`295f2acd`: no drift | [SETTINGS_ACTIVATION.md](SETTINGS_ACTIVATION.md); recommend owner activation after the WS5 workflow PR merges |
| C3 | Owner; S2 prepares | **prepared; not activated** | `docs/s2-settings-activation-20261022`; [#555](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/555) | content `bddfd74` on base `155181d6`; final head in PR metadata | 6 workflows / 39 jobs / 99 remote uses + 3 local reusable calls; 6 exact SHA patterns cover every current caller; both broad flags false and SHA policy prepared. Re-inventoried 2026-10-22 at `b77cb742`: unchanged; WS5 staged workflows add no action; 38 other refs: 30 compatible, 8 blocked by SHA pinning | [SETTINGS_ACTIVATION.md](SETTINGS_ACTIVATION.md); static compatibility only; three-write transition with one hidden-list capture, and the effective-policy rollback limit, recorded; owner chooses exact-SHA or repository patterns and the 8-ref disposition; actual activation/caller proof pending |
| C4 | Owner; lane 07 prepares | preparation only; implementation/settings authority absent | JS-only proposal; no implementation PR | base `295f2acdb3596c72a7d8d5db54fb6a2baf12554f` | Reuse §11.5 historical qualification, Q4 renamed-main success and native seeded-failure proof ([C4 supplement](SETTINGS_ACTIVATION.md#qualification-and-native-proof)) | D2 historical condition met; Q4 rename merged. First proposed stage only JS: PR 13 / release 14, preserving existing floors/app bindings/strict. Lane03 final handoff received; its separately owned ledger proposal is #559, not declared merged here. Candidate-specific code/contracts approval and later owner settings/readback/blocking proof remain separate. |
| Q4 rename | Codex S1, 2026-10-22 | **merged** 2026-10-22T10:13:05Z | `ci/s1-q4-rename-20261022`; [#554](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/554) | final head `316d7f69930b11d80b089b8c7956d296949f08ac`; merge `73de866ecb22bc8472dafb85f1405a27caf6513b` | PR run `39685134972` 30/30; main run `39761432262` success, 29 success + expected Dependency Review skip; exact `JS Unit (Vitest)` job `119766292139` success, 14 files / 269 tests | Workflow slot 1 released. Historical qualification corpus is distinct; rename alone grants no C4 activation or live merge-enforcement credit (§22.7). This current row supersedes the pre-merge ledger narrative above. |
| C5 | S2 (bounded owner authority) | **activated**; history retained | `docs/s2-settings-activation-20261022`; [#555](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/555) | content `bddfd74` on base `155181d6`; final head in PR metadata | 2026-10-21T21:43:49Z PUT204; full before active / after disabled_manually; historical run 33274031928 retained; enable rollback transport-tested beforehand | [SETTINGS_ACTIVATION.md](SETTINGS_ACTIVATION.md); no workflow file or run deleted |
| D1 | Claude | blocked | | | | Core Gate 1 + OAuth/app; trusted orchestration/isolated config and adversarial/fresh-head proof; subscription only |
| D2 | Astra | deferred | | | | Paired-trial proposal requires evidence, spend cap, credential |
| D3 | Claude Code (Opus) CI coordinating lead, 2026-10-20 | implemented; gates and delta reviews complete (code-reviewer approve, architecture-reviewer approve with nits); **merged** 2026-10-20T13:27:21Z as squash `48d6a450` | `ci/e1-d3-deep-gate-observability`; [#533](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/533) (rebased onto merged #532) | published head `cacc3f79e0eddc07fcb046654dd2cff0d4d1049c` (code `44cd5416`: implementation `b99b0ce4`, creation guard `29f8dfa1`, review fixes `d3b6e527`, `MANAGED_LINE` `44cd5416`; stacked on B2 `ddda9492`) | PR run `39421286969` (`pull_request`, attempt 1, head `cacc3f79`) 26/26 success, carrying B2's commits; full pytest 5,569 passed / 2 skipped / 0 failed at `cacc3f79` and at `d3b6e527`; lint, pyright, flake8 and inventory clean at `d3b6e527`; watch dry-runs `39343196678` (v1) and `39414109552` (v2, final code: creation guard live) success; §16 | Authorized with E1 as one change, 2026-10-20 (§15.1). Rebased onto B2 squash `1a5e0e6f`; final head `f9a675c7` passed 26/26 in run `39428761400` before merge (§16.9). E1 monitoring; newer executed-compare recovery distinct from schedule freshness; one registered `dangerous-triggers` suppression expected (§15.4). Literal suite trigger repaired by #538; corrected automatic delivery and issue recovery verified (§16.10) |
| E1 | Claude Code (Opus) CI coordinating lead, 2026-10-20 | implemented; gates and delta reviews complete (code-reviewer approve, architecture-reviewer approve with nits); **merged** 2026-10-20T13:27:21Z as squash `48d6a450` | `ci/e1-d3-deep-gate-observability`; [#533](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/533) (rebased onto merged #532) | published head `cacc3f79e0eddc07fcb046654dd2cff0d4d1049c` (code `44cd5416`: implementation `b99b0ce4`, creation guard `29f8dfa1`, review fixes `d3b6e527`, `MANAGED_LINE` `44cd5416`; stacked on B2 `ddda9492`) | PR run `39421286969` (`pull_request`, attempt 1, head `cacc3f79`) 26/26 success, carrying B2's commits; full pytest 5,569 passed / 2 skipped / 0 failed at `cacc3f79` and at `d3b6e527`; visual compare rehearsal `39343153293`: compare executed, 65 failed / 18 passed (the pre-existing reds), no baseline written; `deep-gate-visual.yml` byte-identical at `d3b6e527`; 30/30 E1 contract mutations killed; v2 dry-run `39414109552`; §16 | Authorized with D3 as one change, 2026-10-20 (§15.1). Rebased onto B2 squash `1a5e0e6f`; final head `f9a675c7` passed 26/26 in run `39428761400` before merge (§16.9). Visual completion delivery worked at split; the suite filter was corrected by #538 (§16.10). `run_visual` dropped: interface delta accepted under delegation (§16.8). First scheduled visual run 2026-10-26 pending |
| E3 | Claude Code session `hypertrophy-toolbox-v3-main-3f`, 2026-10-19 | executed; **merged** 2026-10-19T19:06:05Z by AvihaiShai as squash `c7fec0523f35f39d15b0e204edd2cfdf02650656` | `docs/e3-gate2-linux-bisect`; [#529](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/529) | harness `abf65918e01af75c0de9352a45fd0a9741d2ba70` (never-merged `diag/e3-h-linux-unsync-01-bisect`); final PR head `390ae1bf17d4a8bddc349a2c045e79e976666f63` | Run [`39276388378`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39276388378): `BOUNDARY_FOUND` then `CONFIRMED`; one capture, first-parent boundary `e6e57eac` (#463) → `e9eff89a` (#464); 10 probes / 30 invocations; [GATE2.md](../deep_gate_linux_visual_failure_20260831/GATE2.md). Final head: PR run `39278678473` (`pull_request`) success, rollup 19/19 success. Post-merge `main` push run `39308135423` on `c7fec052` success | No fix or visual-policy change; GATE1 options B/C/D remain owner decisions |
| F1 | Astra | separate milestone | | | | Delivery council/Gate 1; candidate before publication |
| F2 | tbd | deferred | | | | No signing purchase/credential/identity authority |
| F3 | Claude | separate milestone | | | | Delivery council/Gate 1; exact candidate ZIP, before publication |
| G1–G5/G8 | per §4 | deferred | | | | Expansion outside core; coverage stays non-blocking |
| G6 | Codex implementation team | **merged** 2026-10-21T20:19:20Z | `ci/g6-enforced-selected-tests`; [#552](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/552) | final head `2e480330930f01fc4dffd3f68689c2d4227c74ec`; merge `155181d67a89fe72e86c75a1ff438caec250a9bd` | Final PR run `39665357619` 30/30; main `39669286271` success; Windows `119462546731` six fixed passes; core `119462546987` three fixed dependency passes; required aggregate `119466508178` success | Preserve §21's original negative proofs and dated integration receipts. Subsequent separately approved G7 merge recorded in §22.7; no Operation A promotion. This current row supersedes the pre-merge ledger narrative above. |
| G7 | Claude Code O1 (Opus), 2026-10-22 | **merged** 2026-10-22T12:59:55Z | `ci/g7-retry-report`; [#557](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/557) | final head `4473c913cbb060602981e73696e682f31d81a9f3`; merge `b77cb742f3af5222d9d80b608d497390c4b3e4f2` | Final PR run `39774255096` 30/30; local full pytest 6,095 passed / 2 skipped; exact-main `39783010460` success (29 success + expected Dependency Review skip), nine retry-summary steps successful | §22 history retained; §22.7 records named-head owner E2E exception and accepted CI-only reporter. Local E2E remains failed historical evidence. Slot 2 released; no WS5 or C4 waiver. This current row supersedes the pre-merge ledger narrative above. |

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

Core Gate 1 is approved for Plan v2; execution receipts and authority are recorded per packet in §§13–19, including the newly authorized A2 → A3 → G6 → G7 sequence (§19). Q4 is approved and D2's ledger condition is met (§21.3). Q4's standalone rename and successful renamed merged-main check are complete through #554 (§7). JS-only C4 code/contracts, activation proofs, settings execution, D1 credentials, E3 named diagnostic extension and separate delivery council/Gate 1 remain individual gates. GitHub access is capability, not authorization.

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

**JS status supersession, 2026-10-22:** Q4's separately approved rename merged
through #554; the exact `JS Unit (Vitest)` merged-main job succeeded (§7).
D2's specified historical §13.0 condition is met, with no repeat signature needed.
The first proposed C4 stage is JS only: R0+JS for PR (13), R0+JS+Windows visual
for release (14); the other full-adoption members below stay future candidates.
The dated 2026-10-18 accounting below, including carrier-level cancellation
arithmetic and unsigned wording, remains historical and is superseded by the
owner's exact-JS-job ruling in DECISION.md. Lane03 retains all ledger/window
decisions; #559 is its separately owned proposal. No row, T0 or new completed
window is declared here. Candidate-specific JS-only implementation and later
owner settings/proof approval remain separate; preserve fresh strict (C2 is
independent). The append-only C4 supplement in SETTINGS_ACTIVATION.md supplies
the concrete implementation/tests, 13-check snapshot and owner action sheet.

These are **target sets after each named promotion qualifies**, not a report of changed protection. Keep every existing requirement throughout transition. Let `R0` be the exact twelve strings in §2.3 and define:

| Set | Target membership | Count at full adoption |
|---|---|---|
| `PR_REQUIRED_CONTEXTS` | `R0` + `JS Unit (Vitest)` + `Operation A Windows Tests` + `Packaged Smoke (Windows bootloader, non-required) / Build and smoke` + `Visual Regression (Windows baselines)` + `Workflow Lint (actionlint + zizmor)` + proposed `Dependency Review` | 18 |
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

Local gates are complete using the exact evidence above. Pushed
`ci/b1-action-pins` and opened ready PR
[#521](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/521),
verified `OPEN` / `isDraft: false`. Initial published head:
`c63b403152897dd06edfb8df5642544b2298fa3e`, whose workflow/test tree is identical
to reviewed/tested implementation `1dfe011b1533f1339660b72a60249b390b296104`.

GitHub assigned initial PR CI run
[`39171727770`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39171727770),
event `pull_request`, on `c63b403152897dd06edfb8df5642544b2298fa3e`; its jobs
started `2026-10-18T22:19:39Z` onward. This is an **in-progress snapshot, not a
passing runtime result**. This publication-receipt-only commit supersedes that
carrier through the existing PR concurrency policy. The PR description links the
current-head CI run after GitHub assigns it; no incomplete/cancelled run is
credited as validation. GitHub CI remains separate runtime evidence.
The branch stops before merge. No other packet, promotion, setting, credential,
spend, delivery or release action was executed.

**Post-merge closeout (recorded by the A1 session, 2026-10-19; verified from Git and
the GitHub API, nothing above is rewritten).** The paragraphs above are the
pre-merge publication receipt. Final PR head
`c91986bf376a1a09f055c4ee4dc4cb4d27bb601e` added only this file on top of the
receipt commit. Its PR run
[`39171777513`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39171777513)
(`pull_request`, attempt 1) concluded **success** with all 19 check runs
successful. The owner merged #521 on 2026-10-18T23:46:43Z as squash
`77f400bb331e1de631a32114a7cc9996f5b5dd1e`, parent `7ac1af2d`. The squash tree
`cfc864bd` is identical to the final head's tree. `.github/`, `tests/` and
`scripts/` are identical to implementation `1dfe011b`, so §13.1's local evidence
still describes the merged workflow/test tree.

Post-merge `main` push run
[`39177927596`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39177927596)
on `77f400bb` concluded **success**. The first scheduled Deep Gate containing B1,
[`39226020933`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39226020933)
on `e486e3b5` (2026-10-19), passed six of seven jobs with pinned actions. The
exception is the pre-existing `Visual regression (Linux baselines)` failure (CI-D1/E3
scope), unchanged by B1. `release.yml` has not run since B1, so its pins have
parse/contract evidence only. B1 is closed; C3 remains an owner action.

## 14. A1 execution — 2026-10-19

The owner authorized **A1 only**: implementation, its bounded benchmarks and failure
rehearsals on existing GitHub Actions infrastructure, the required tests and
independent reviews, push and a ready PR. The PR stops before merge. The same
instruction authorized the bounded B1 closeout correction (§7, §13.2). It authorizes
no other packet, settings change, check promotion, paid service or release. This
section supersedes the earlier "B1 only" statements for A1 alone; historical text is
retained. B2 was not started.

### 14.1 Claim, isolation and coordination

- **Claim.** Claude Code A1 session, 2026-10-19. The live path claim is in the shared
  checkout's gitignored `WORKSTREAM_OWNERSHIP.local.md`. The §7 row was committed and
  pushed first (`ci/a1-guard-split` @ `a8688b1`, before any implementation commit; after the rebase onto `f85ec050` the work is published as `ci/a1-guard-split-b`, because the guard forbids force pushes). At claim time
  no open PR touched `ci.yml`; the only open PRs were #526–#528, all docs.
- **Isolation.** A standalone HTTPS clone at
  `D:/development/Hypertrophy-Toolbox-v3-ci-a1-20261019` with its own `.git` (no
  alternates), venv, `node_modules` and runtime paths. A full-history clone stalled on
  transport, so the clone was taken shallow and later unshallowed from `origin`.
  Rehearsal branches were built in a second independent clone inside the session
  scratchpad, so the full pytest run was never disturbed. The shared checkout, its
  stale local plan and its locally modified guard test were never edited, reset or
  stashed. The only write to the shared checkout was the claim row in the gitignored
  local claims file.
- **E3 coordination.** The E3 session (`hypertrophy-toolbox-v3-main-3f`) owns E3, its
  `GATE2.md` and its §7 row; this packet edits neither. Runner windows were
  serialized by message:

  | Window (UTC) | Owner | Run |
  |---|---|---|
  | 14:38:13–15:06:57 | A1 benchmark rep 1 | `39270742974` attempt 1 |
  | 15:15:31–15:23:06 | E3 bisect + confirmation (one runner) | `39276388378` |
  | 15:23:51–15:52:09 | A1 benchmark rep 2 | `39270742974` attempt 2 |

  Nothing overlapped. **Interference that did occur:**
  - GitHub declared an Actions incident ("degraded availability for GitHub Actions,
    Pages and Webhooks") at 15:49:25Z. It was still open at the time of writing.
    During it, the jobs API returned HTTP 502 and stale `in_progress` states.
  - Rep 2's last job and all rehearsals ran inside the incident window.
  - Run-level `queued` statuses were shown while jobs had in fact already started.
    Job-level `created_at` / `started_at` is authoritative and showed at most 5 s of
    queueing.
  - Durations below are runner start-to-finish.

### 14.2 Benchmark matrix (bounded, before choosing the shape)

Workflow `.github/workflows/a1-bench.yml`. It lives only on throwaway branch
`bench/a1-guard-shape-20261019`, head `27fad2927a7604fb0c1604b2ef871131d9644c5f`
(A1 verifier commit plus the bench file), and is never merged. Every arm runs
`tests/test_guard_destructive_command.py` on `ubuntu-latest`: 4 vCPUs, pwsh 7.6.6,
Python 3.14.6, pip cache. Each arm collects the file, selects its slice, runs it, and
then `scripts/ci_executed_report.py verify` checks its executed JUnit against the
collection. A `core` arm runs pytest minus the guard file, with coverage. Rep 1 is
attempt 1, created 14:38:13Z; rep 2 is attempt 2, created 15:23:51Z, on the same
commit.

| Arm | Jobs | Slowest job, rep 1 / rep 2 (min) | Arm end-to-end from run creation (min) | Runner-min (billed) | Max queue (s) | Executed identities |
|---|---|---|---|---|---|---|
| serial | 1 | 28.7 / 28.2 | 28.7 / 28.3 | 28.7 / 28.2 (29 / 29) | 4 | 1,018 / 1,018, all passed |
| `-n 4` | 1 | 17.1 / 21.4 | 17.2 / 21.6 | 17.1 / 21.4 (18 / 22) | 4 | same set, all passed |
| `-n 8` | 1 | 15.5 / 15.7 | 15.5 / 15.8 | 15.5 / 15.7 (16 / 16) | 4 | same set, all passed |
| 2 shards | 2 | 14.1 / 16.5 | 14.2 / 16.6 | 23.3 / 27.6 (25 / 29) | 4 | same set, all passed |
| 2 shards × `-n 4` | 2 | 8.8 / 8.2 | 8.9 / 8.3 | 15.0 / 15.3 (16 / 17) | 4 | same set, all passed |
| **4 shards (chosen)** | 4 | **7.3 / 12.5** (legs 7.2–7.6 plus one 12.5 straggler) | 7.4 / 12.6 | 27.5 / 34.7 (30 / 37) | 4 | same set, all passed |
| 4 shards × `-n 4` | 4 | 4.9 / 5.3 | 5.0 / 5.4 | 17.7 / 18.6 (19 / 20) | 5 | same set, all passed |
| core (minus guard) | 1 | 2.9 / 2.3 | 2.9 / 2.4 | 2.9 / 2.3 (3 / 3) | 4 | 3,213; see below |

**Identity checks.**
- For every guard arm, in both reps:
  - collection equalled the serial arm's collection;
  - executed identities equalled the serial set: 1,018 cases, pwsh host only on Linux;
  - there were zero duplicates;
  - every shard executed exactly its own slice;
  - there were zero skips, failures or errors.
- Core ∪ serial-guard equals main push run `39249316854` (on `c6a982cf`, same corpus)
  identity-for-identity: 4,231 identities, none missing or extra, and the same 211
  skips.
- The one core failure in both reps was `test_the_workflow_directory_holds_exactly_the_files_this_file_reads`.
  It fired because the bench workflow file itself is an undeclared workflow — the
  census contract working as designed — and it does not occur on the A1 branch.
- Coverage from the core arm equals the baseline exactly: 6,930 / 7,938 lines
  (87.3%), all 72 files identical. The guard file contributes nothing to
  `utils`/`routes` coverage, so the guard legs measure none.
- The §2 figure of 1,018 guard cases still held at this corpus.

**Shape decision: four runner shards, serial within each.**
- `4 × -n 4` was fastest and cheapest, but it was **rejected after failure evidence**
  (§14.3).
- No single-runner arm reaches the required-gate path's current floor. `E2E Functional
  (Chromium)` is about 10.4 min on baseline run `39249316854`.
- `2 shards` alone is slower than that floor.
- Four serial shards keep each pwsh process as isolated as before. They cost about
  1–9 runner-minutes more than the old single serial job (27.5–34.7 against 28.2–28.7),
  plus four setups.
- **Deviation from §4's "guard timeout 15":** `timeout-minutes: 20`, because the rep 2
  straggler took 12.5 min. A timeout fails closed. Raise it to 25 if a timeout-cancelled
  leg ever appears.

### 14.3 Failure rehearsals (separate from green equivalence)

Workflow `.github/workflows/a1-rehearsal.yml`, generated per case on throwaway
`rehearsal/a1-*` branches (never merged). It contains `ci.yml`'s `pytest-core`,
`guard-hook-shard`, `guard-hook-tests` and `run-tests` blocks **copied verbatim**. The
generator asserts that byte equality, so each case differs from `ci.yml` only by its one
named mutation. A census line for the rehearsal file is added only on these branches.

**Round 1** (on `7642645`, the `4 × -n 4` shape):
- The **green control failed.** Run `39280323729`, shard 3/4: two guard cases,
  `test_agent_git_rm_is_hard_deny_in_every_mode[sh -c "git rm retained"-default-pwsh]`
  and `test_suppression_forms_are_profile_and_permission_invariant[MSYS_NO_PATHCONV-default-agent-pwsh]`.
  pwsh exited -6 with `System.IO.FileLoadException: The given assembly name was invalid`
  on a truncated `PublicKeyToken=b03f5f7f11d50a3`.
- This crash occurred while four pwsh processes ran concurrently on one runner. A
  shared per-user pwsh startup cache is the **suspected, not proven** mechanism.
- Before the decision, 28 xdist legs ran: 16 benchmark legs and 12 round-1 rehearsal
  legs. This was the only crashing leg. None of the 14 serial benchmark legs crashed.
- A required check must not flake, so the shape moved to serial legs (`0e4f342`).
  `ci.yml` and the contracts now forbid `-n` in the guard leg.
- Round-1 guard-fail `39280328021` and core-fail `39280332221` also turned
  `Run Tests` red as designed.

**Round 2** (on `0e4f342`, the final shape; branches `rehearsal/a1-*-v2` and
`cancel-v3`, pushed 16:23:47Z and 16:46:02Z):

| Case | Mutation | Run | Shards | `Guard Hook Tests` | Python Tests (core) | **Run Tests** |
|---|---|---|---|---|---|---|
| green control | none | `39285097596` | 4 × success (7.2–7.9 min) | success | success (2.6 min) | **success** |
| injected guard failure | guard case `powershell -File scripts/run-pytest.ps1` expected `deny` | `39285103455` | shard 2 failure (that one identity), 3 × success | failure (shard gate) | success | **failure** |
| injected core failure | `GUARD_SHARDS = 5` in the A1 contract suite | `39285105591` | 4 × success | success | failure | **failure** |
| lost shard (every leg green) | matrix `[1, 2, 3]`, total still 4 | `39285108590` | 3 × success | failure (union step only) | success | **failure** |
| skipped shards | `if: ${{ false }}` on the shard job | `39285112726` | skipped | failure (shard gate) | success | **failure** |
| cancellation | run cancelled at 16:46:56Z with all four shards in progress | `39288227037` | 4 × cancelled | failure | cancelled | **failure** |

**Coverage of failure modes.**
- Every non-success, cancelled, skipped and partial-union case turned `Run Tests` red,
  and the green control turned it green.
- A "missing" dependency result cannot be produced by a valid workflow. It is covered
  by `scripts/ci_fan_in.py` behaviour tests, as are malformed and unexpected `needs`
  input.
- An earlier cancellation attempt, `rehearsal/a1-cancel-v2` (`39285117239`), completed
  green before the watcher fired. It was not cancelled and is not credited.

### 14.4 Implementation

**Final shape.**
- `pytest-core` / `Python Tests (core)` is the former job, with
  `--ignore=tests/test_guard_destructive_command.py` and timeout 20. Coverage flags,
  artifacts (`pytest-junit`, `pytest-coverage`), Node, `fetch-depth: 0` and the D1
  summary are unchanged.
- `guard-hook-shard` (4 legs, `fail-fast: false`, timeout 20) collects the guard file,
  writes its round-robin slice and runs `pytest @artifacts/guard/shard.txt`. It then
  verifies that it executed exactly that slice with no skips, failures or errors, and
  uploads `guard-hook-junit-<n>` with `if-no-files-found: error`.
- `guard-hook-tests` / `Guard Hook Tests (Linux pwsh)` runs `if: always()`. Its fan-in
  over the shards comes first, then `actions/download-artifact`, then
  `ci_executed_report.py union --shards 4`: identical collections on every leg, and the
  union executes every identity exactly once.
- `run-tests` / **`Run Tests`** runs `if: always()` and `needs: [pytest-core,
  guard-hook-shard, guard-hook-tests]`. It passes only when every dependency is
  exactly `success`.
- The direct shard edge is deliberate defence in depth.
- No required context, release-gate list, settings or app binding changed. The three
  child names join `UNEXPECTED_CI_JOB_NAMES`, so they can never become expected
  contexts by accident.

**Named helpers** (§12.4's helper rule):
- `scripts/ci_fan_in.py` makes the fan-in decision. It fails on failure, cancelled,
  skipped, absent or extra dependency, or malformed `toJSON(needs)`.
- `scripts/ci_executed_report.py` provides `shard`, `verify` and `union`. Missing,
  unexpected, duplicate-expected, duplicate-executed, skipped (including xfail),
  failed/errored, empty, nameless and unparsable reports all fail. A collection whose
  node count disagrees with pytest's own summary fails. An empty slice is refused
  before pytest could fall back to collecting the whole tree.
- `tests/worktree_cleanup/verify_ci_report.py` is **not** reused or broadened. It is
  Operation A's module/host verifier. A1 reuses its executed-outcome rule (a testcase
  with a `skipped`, `failure` or `error` child does not count) without changing its
  scope.

**Divergence from the `e2e-functional` fan-in** (deliberate): the two new aggregates
check out the repository and call a script instead of an inline shell test. This makes
the decision behaviourally testable. A checkout failure still fails closed.

**Contracts.**
- `tests/test_ci_expansion_contracts.py` (87 cases) covers the fan-in result matrix,
  the identity/collection/shard/union decisions and the CLIs. It includes a real
  `--collect-only` parse of the guard file, plus `ci.yml` wiring.
- `tests/test_worktree_ci_contracts.py` now reads `pytest-core`. It keeps every
  Windows host/report assertion and adds the single-`--ignore` check.
- Seventeen `ci.yml` weakenings were each applied and turned the suites red. They
  include dropping a dependency, a missing `always()`, `continue-on-error`, a three-leg
  matrix, a shard-count drift, deselection, a second `--ignore`, reintroduced `-n`,
  `merge-multiple`, `if-no-files-found: warn` and a second `Run Tests`.

**Action inventory.** One newly adopted action, `actions/download-artifact` v8.0.2 at
full SHA, is recorded in [B1_ACTION_INVENTORY.md](B1_ACTION_INVENTORY.md). The C3
candidate set becomes five repositories.

**Notes for later packets.**
- A3 must update the `/2` shard literal and these wiring pins.
- G6 adds its Windows leg to `run-tests` `needs`, to the `ci_fan_in.py` arguments and to
  `FAN_IN_DEPENDENCIES`. The exact-set check forces all three.
- B4 is compatible with `pytest-core`'s flags.

### 14.5 Gates and reviews

**Required union.** The diff touches a workflow (jobs added and converted), scripts,
tests, generated inventory and docs. That requires:
- full pytest;
- `code-reviewer` and `architecture-reviewer`;
- a pyright baseline diff;
- inventory regeneration plus `--check`;
- the blocking flake8 selection on changed Python.

No product, route, template, JS or CSS change is involved, so no Chromium gate applies.

| Gate | Commit | Result |
|---|---|---|
| Full pytest, local Windows (Python 3.14.6, Git Bash first on process PATH, as §13.1) | `7642645` | 5,324 passed, 2 skipped, 1 failed. The failure was `test_wp4_4_baseline_is_pinned_and_matches_its_source_commit`: the shallow clone lacked `46e340e5`. After unshallowing, that file passed 33/33. The skips are the same two as §13.1. |
| Full pytest, local Windows, non-shallow clone | `0e4f342` (final code tree) | **5,330 passed, 2 skipped, exit 0**, 1521.69 s, 16:24:35–16:49:58Z. The skips are the same two as §13.1. |
| Targeted contracts, plus 17-mutation matrix | `0e4f342` | all pass; 17 / 17 killed |
| pyright 1.1.410 baseline diff | `bcff949` tree | PASS, 0 net-new. One net-new diagnostic in the first draft was fixed in code, not baselined. |
| `generate_test_inventory.py --check` | `0e4f342` | up to date |
| flake8 blocking selection on changed Python | `bcff949` tree | 0 |

**Reviews.** Both reviewers were independent subagents. They read files, not chat, and
ran nothing.
- **`code-reviewer`, on `a440844`: approve.**
  - Should-fix: an empty slice would make `pytest @file` collect the whole tree. Fixed
    in `bcff949`.
  - Nit: the CLI paths were untested. Subprocess tests were added.
  - Nit: the secondary verify error after a failed collection is left as is.
  - Delta review of `0e4f342`: all resolved, no new gap, timeout 20 acceptable. The
    collection-test message nit is fixed in the commit that adds this section.
- **`architecture-reviewer`, on `a440844`: needs revision.**
  - This §14 was missing; it is resolved by this section.
  - Stale CI-shape prose in `tests/CLAUDE.md`, `scripts/generate_test_inventory.py` and
    `tests/test_vitest_inventory_contracts.py` is fixed.
  - The fan-in divergence and the YAML-pin notes are recorded above.
  - Delta review of `0e4f342`: the serial change and the timeout deviation are sound.
    The only further nit, a stale "both" in the `pytest-core` comment, is fixed in
    the same commit. That commit changes one comment and one assertion message; the
    targeted contracts, lint and inventory check were re-run on it.
  - No reviewer was re-run on this documentation section.

### 14.6 PR and measured speed

**Publication.**
- Pushed `ci/a1-guard-split-b` and opened ready PR
  [#530](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/530), verified
  `OPEN` and `isDraft: false` at 2026-10-19T16:55:29Z.
- The published head is `18fc388a38cd4efcd9140aaf9cdfa3f49b0ad6db`. Its workflow,
  script and test tree is `0e4f342` plus the two review nits; §14.5 re-ran the
  targeted gates on it.
- This receipt-only commit changes nothing but this file, and it starts a new PR run.
  That run supersedes the one below as the current-head carrier. A run that is
  incomplete or cancelled is not credited.

**PR CI run [`39289691671`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39289691671)**
(`pull_request`, attempt 1, head `18fc388`, created 16:55:33Z): **all 25 jobs
success.**
- **Identities.** Core ∪ guard executed 4,318 identities: 3,300 core and 1,018 guard
  (the union was re-verified locally from the downloaded reports). That is the
  baseline's 4,231 plus exactly the 87 new `test_ci_expansion_contracts` cases. None is
  missing, no outcome changed, and there are 211 skips as before.
- **Coverage** is identical: 6,930 / 7,938 lines across 72 files.

| Measure | Baseline `main` push `39249316854` | Baseline PRs `39171777513` / `39245465367` | **A1 PR `39289691671`** |
|---|---|---|---|
| Creation → `Run Tests` | 32.3 min | 31.8 / 28.2 min | **8.1 min** |
| Creation → last required context | 32.3 min (`Run Tests`) | 31.8 / 28.2 min (`Run Tests`) | **10.4 min** (`E2E Functional (Chromium)`) |
| Creation → last job | 32.3 min | 31.8 / 28.2 min | 11.9 min (`Operation A Windows Tests`, not required) |
| Runner-minutes (billed) | 80.3 (91) | 73.7 (85) / 73.7 (81) | 79.9 (93) |
| Max job queue | 4 s | 3 s / 54 s | 5 s |

**Result on G1.**
- The 12–15-minute initial objective is **met on this one PR run**: 10.4 min from
  creation to the last required context. It is a single sample, taken during the open
  GitHub Actions incident, so it is not a median.
- `Run Tests` is no longer the critical path; E2E Functional is.
- The 8-minute second stage and the 6-minute stretch are **not** met. They depend on
  A3, and on the 1.7× leg variance noted in §14.7.
- The cost is about +6 runner-minutes against same-event PR runs (+8–12 billed): four
  guard-leg setups plus two short aggregates.

**Baseline for comparison:** `main` push run `39249316854` on `c6a982cf`,
2026-10-19 12:05:08Z.
- The run took 32.3 min from creation to its last job.
- `Run Tests`, a single job, completed at 32.2 min and was the slowest required
  context.
- The other required contexts finished by 10.5 min (`E2E Functional (Chromium)`
  12:15:40Z).
- Creation to the last required context was therefore 32.3 min.

### 14.7 Remaining limitations

- **The pwsh crash mechanism is suspected, not proven.** Restoring xdist (about
  5 min and 18 runner-min instead of 7.3–12.5 and 28–35) needs per-process pwsh cache
  isolation, plus fresh failure-free evidence across many legs.
- **Leg times vary by up to 1.7× between runners** (7.2 against 12.5 min on the same
  slice). The required gate's guard path therefore runs 8–14 min. That is near or
  below E2E Functional today, but it would become the critical path after A3.
- **Timing.** §1.2's 12–15-minute initial objective is met on **one** PR run (10.4 min,
  §14.6), not on a median. Confirm it on post-merge `main` runs before treating it as
  established. The 8-minute second stage and the 6-minute stretch were not reached.
- **Rep 2 and every rehearsal ran inside an open GitHub Actions incident.**
- `release.yml` is untouched. The release gate still reads the exact `Run Tests` name;
  no tag rehearsal was run.

## 15. B2 execution — 2026-10-20

Recorded by `product-manager` from the coordinating lead's relay. This agent did not read
the owner's message directly; the quotations below are the lead-supplied verbatim excerpts.
Evidence in §§15.5–15.6 is as the lead reported it, tied to the branch's commits:
implementation `704016f5e01f26c2b5efbf0b3678593d060f0794`, review fixes
`9823beb9c7ba1f3f800dcfdabca349c472035595`, and published head
`d5dfa0615fb5770dca2fab50a8d052211c99308b`. Short forms `704016f5`, `9823beb9` and
`d5dfa061` refer to these. Only the post-merge `main` run is still pending; nothing
pending is filled in advance.

### 15.1 Authority

Owner authorization, 2026-10-20 local (+03:00), 2026-10-19 UTC. Verbatim excerpts:

> I authorize:
> - B2: workflow lint with actionlint and zizmor.
> - E1 + D3: separate Linux visual workflow and deterministic Deep Gate monitoring, delivered together as the coherent observability change permitted by the plan.
> - The four documentation follow-ups below.
> - Necessary implementation, tests, independent reviews, bounded CI rehearsals on existing infrastructure, commits, pushes, and ready PRs.
>
> Stop before merging. Repository settings, required-check promotion/C4, credentials, spending, release publication, and later CI packets remain outside this authorization. Publishing AGREED_PLAN.md into a documentation PR is explicitly authorized.
>
> Preserve the sequence: B1 → A1 → B2 → B3 → A2 → A3 → G6 → G7. B2 has priority. Do not begin B3 or later packets.
>
> Documentation follow-ups: Correct A1 and E3 ledger statuses from verified merge receipts, preserving historical execution evidence.
>
> Agent organization: product-manager owns writes to the CI PLANNING.md, including execution authority, claims, ledger reconciliation, and evidence. senior-developer owns implementation. automation-qa owns acceptance tests. A documentation writer owns the handover, queue reconciliation, and AGREED_PLAN publication. Independent code-reviewer and architecture-reviewer review the implementation.

The lead summarized, not quoted, the other three documentation follow-ups: handover
refresh, `OPEN_WORK` queue reconciliation and Q9 `AGREED_PLAN.md` publication. They ship
in a separate documentation PR on branch `docs/ci-ledger-handover-queue-q9` and do not
edit this file. The first follow-up (A1/E3 ledger statuses) is this file's §7 and header
update, from the receipts the lead verified at 2026-10-19T22:1xZ.

**Boundaries as applied here.**
- Authorized: B2; E1+D3 as one change; implementation, tests, independent reviews, bounded
  rehearsals on existing GitHub Actions infrastructure, commits, pushes and ready PRs.
- Not authorized: any merge; repository settings or branch protection; C4 or any
  required-check promotion; credentials; spending; release publication.
- B3 and every later packet (A2, A3, G6, G7 and all others) are **not started**.
  `Workflow Lint (actionlint + zizmor)` is not added to `REQUIRED_CONTEXTS` or
  `scripts/release_gate.py`; that change belongs to C4.
- This section supersedes the earlier "B1 only" and "A1 alone" statements (§0.1, §5
  batch 0, §9, §12.4, §§13–14) for B2 and E1+D3 alone. Historical text is retained.

### 15.2 Claim, isolation and coordination

- **Claim.** Claude Code (Opus) CI coordinating lead, 2026-10-20, for B2, D3 and E1 (§7).
  Live path claims are in the shared checkout's gitignored
  `docs/ai_workflow/WORKSTREAM_OWNERSHIP.local.md`. The lead reports that the A1 and E3
  rows there were released on their merge evidence. No open PR existed at
  2026-10-19T22:1xZ.
- **Isolation.** Standalone clone `D:/development/Hypertrophy-Toolbox-v3-ci-b2-20261020`
  on `ci/b2-workflow-lint`, from `origin/main`
  `f3adacf1c1b48cc6e2c7ca9ac900e3294b3bae2d`, with its own `.git`, `.venv` and
  `node_modules`. It was made as a local clone and its remote then set to GitHub. No
  linked worktree, shared DB, stash, reset or other-session edit. The shared checkout's
  untracked copy of this plan is a divergent stale lineage and is not used.
- **Serialization.** B2 is the only `ci.yml` PR in flight (§0.4). E1+D3 is built on top
  of B2 on `ci/e1-d3-deep-gate-observability`, because B2 edits every `deep-gate.yml`
  checkout and adds the lint that gates the new workflows. This departs from §0.4's "each
  starts from current `origin/main` after the prior merge".
  - **The E1+D3 PR targets `main`, not the B2 branch.** `ci.yml`'s `pull_request` filter
    is `[main, develop]`, so a PR based on the B2 branch would get no CI. Until B2 merges,
    the E1+D3 PR therefore carries B2's commits.
  - **Binding merge order, stated in the PR body.** B2 merges first. After B2's squash
    merge, the E1+D3 branch is rebased with `git rebase --onto origin/main <B2 head>`, and
    CI is re-run on that final head.
  - **B2 changes.** Any further B2 code change requires re-stacking E1+D3 and re-review.
  - **Review.** The `architecture-reviewer` endorsed this choice (§15.5).
- **Other lanes.** The lead noted an advisory claim on `OPEN_WORK` held by a
  docs-cleanup lane; the separate documentation PR coordinates with it.
- **Observed concurrent activity (E1 coordination note).** Manual Deep Gate run
  `39331294762` (`workflow_dispatch`, branch `visual/linux-baseline-resync-20261020` at
  `f3adacf1`) was in progress at 2026-10-19T22:1xZ. It was triggered from the owner
  account by an unidentified session, with no claim or PR. It is **not interpreted** and
  is not evidence for any packet. No scheduled Deep Gate has run since A1 merged.

| Role | Agent | Owns |
|---|---|---|
| `product-manager` | this agent | This file only: authority, claims, ledger, evidence |
| `senior-developer` | — | B2 implementation |
| `automation-qa` | — | The headed B2 section of `tests/test_ci_expansion_contracts.py` and its mutation proof |
| `code-reviewer` | Claude Code subagent launched by the lead, 2026-10-20 (UTC 2026-10-19) | Independent review of the B2 implementation (§15.5) |
| `architecture-reviewer` | Claude Code subagent launched by the lead, 2026-10-20 (UTC 2026-10-19) | Independent review of the B2 implementation (§15.5) |
| Documentation writer | — | Separate docs PR (`docs/ci-ledger-handover-queue-q9`) |

Internal agent IDs were not recorded, so none is stamped and none is invented.

### 15.3 Baseline lint measurement on `f3adacf1`

Measured by the lead, 2026-10-20 local, over `.github/workflows` at `origin/main`
`f3adacf1`. Local Windows builds of the pinned versions were used for verification only;
CI runs the Linux release assets of the same versions (§15.4).

| Tool / mode | Result |
|---|---|
| actionlint 1.7.12, no shellcheck | clean |
| actionlint 1.7.12 + shellcheck 0.11.0 | 4 × `SC2016` (info), all in `ci.yml` run blocks: line 214 (two hits), 954, 1334. Intentional single-quoted `$` literals |
| zizmor 1.30.1 `--min-severity medium`, offline | **34 findings.** 31 × `artipacked` (every `actions/checkout` without `persist-credentials: false`: 19 `ci.yml`, 6 `deep-gate.yml`, 5 `release.yml`, 1 `_packaged-windows.yml`); 2 × `cache-poisoning` (`release.yml` setup-python `cache: 'pip'` in the tag-triggered workflow); 1 × `template-injection` (`release.yml` `${{ github.ref }}` in a `run:` block) |
| zizmor 1.30.1, online | `artipacked` reported as Low; the other three findings identical |
| zizmor, repository-root scan | adds 3 × `dependabot-cooldown` on `.github/dependabot.yml` |

The `dependabot-cooldown` findings are **out of B2 scope**: B2 lints
`.github/workflows` only, and changing Dependabot cadence is a D-6-adjacent owner
decision. Recorded as an observation and possible follow-up; `dependabot.yml` is not
changed.

*Dated disposition, 2026-10-20:* §18.3 decisions 3–4 adopt the cooldown under owner
delegation, reading the owner routing above as overstated, with dissent recorded. This
is not an owner signature; merging still needs the owner's explicit PR message.

### 15.4 Design

Source: the lead's B2 implementation brief ("Required job shape" and its rationale),
read by this agent.

**Job.** `workflow-lint` / `Workflow Lint (actionlint + zizmor)` in `ci.yml`:
`ubuntu-latest`, `timeout-minutes: 10`, job `permissions: {contents: read}`. No `needs`,
no job `if:`, no `continue-on-error`, no `|| true`, no path filter. It runs on every PR
and every `main` push.
- Checkout uses the B1-pinned `actions/checkout` with `persist-credentials: false`.
- One install step downloads the three release assets into `$RUNNER_TEMP` with
  `curl --fail --proto '=https' --proto-redir '=https'`, `--retry 3 --retry-all-errors`,
  `--connect-timeout 15` and `--max-time 120`. It verifies all three with
  `sha256sum --check --strict` before any extraction or execution, and prints each
  version. Retries, timeouts and `--proto-redir` were added in `9823beb9` (§15.5).
- `actionlint` runs with `-shellcheck=` pointing at the pinned binary and `-pyflakes=`
  (optional pyflakes integration disabled).
- `zizmor --min-severity medium --format plain .github/workflows` runs under
  `if: ${{ !cancelled() }}`, so it reports even when actionlint fails. It runs online
  with `GH_TOKEN: ${{ github.token }}` (read-only).

**Pins.** All three digests match the GitHub-published release-asset digests, verified by
the lead through the releases API.

| Tool | Version | Asset | SHA-256 |
|---|---|---|---|
| actionlint | 1.7.12 | `rhysd/actionlint` `actionlint_1.7.12_linux_amd64.tar.gz` | `8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8` |
| zizmor | 1.30.1 | `zizmorcore/zizmor` `zizmor-x86_64-unknown-linux-gnu.tar.gz` | `e65324f4430c2717591937edcec90ccbefaf14c174f8ec9415e03ca875b46e1a` |
| shellcheck | v0.11.0 | `koalaman/shellcheck` `shellcheck-v0.11.0.linux.x86_64.tar.gz` | `b7af85e41cc99489dcc21d66c6d5f3685138f06d34651e6d34b42ec6d54fe6f6` |

**Rationale.**
- zizmor 1.30.1 was chosen over 1.31.x as the newest release at least five weeks old (the
  lead's selection).
- shellcheck is pinned because actionlint otherwise uses whatever the runner image ships.
- No new action is adopted, so the C3 candidate set is unchanged. The three binaries are
  recorded as non-Action tools in
  [B1_ACTION_INVENTORY.md](B1_ACTION_INVENTORY.md#non-action-tool-binaries-b2), written by
  the senior-developer. The lint job's pinned checkout takes `ci.yml` from 62 to 63
  remote `uses:` and the repository from 91 to 92, per the senior-developer's count.
- **Online-mode consequence.** zizmor's pin audits (impostor commit, ref/version mismatch,
  known-vulnerable actions) run, so a newly published advisory for a pinned action can red
  this job. The repair is a reviewed pin bump, never a suppression. Because online mode
  rates `artipacked` Low, the CI job alone would not catch a reintroduced persisted
  credential at `medium`; the repository-wide `persist-credentials: false` contract in
  the B2 test section covers that. Online mode also couples the job to GitHub API
  availability (§15.5).
- Not added to `REQUIRED_CONTEXTS`; promotion waits for C4 (§6, §11.5).

**Remediation plan (no weakening).** Applied in `704016f5`; §15.5 records the outcome.
1. `persist-credentials: false` on every `actions/checkout` in all four workflows, after
   showing that no job needs persisted git credentials.
2. Remove `cache: 'pip'` from the two flagged `release.yml` setup-python steps.
3. Replace `${{ github.ref }}` in the `release.yml` `run:` block with `"$GITHUB_REF"`, and
   check every other `run:` for attacker-controllable expansion.
4. The four `SC2016` infos: an inline `# shellcheck disable=SC2016` with a one-line reason
   at each site, or a byte-for-byte behaviour-preserving rewrite. No blanket disable.
5. B2 adds no zizmor configuration file and no `zizmor: ignore[...]` comment.

Target: actionlint (with pinned shellcheck) clean and zizmor `--min-severity medium` clean
in both offline and online mode.

**Contracts.** A headed B2 section of the existing `tests/test_ci_expansion_contracts.py`
(automation-qa), per the §12.4 file table; no new test file. It covers job identity,
triggers without path filters, permissions, exact pins and download/verify order, step
flags, linter-softening environment, repo-wide checkout/injection/cache guards, a
suppression register (explicit allowlist with exact counts, starting with B2's `SC2016`
entries and no zizmor entries), and absence from `REQUIRED_CONTEXTS`. Each assertion
family has a recorded mutation that turns it red (§15.5).

**E1/D3 implication.** zizmor flags every `workflow_run` trigger as `dangerous-triggers`
(High). D3's `deep-gate-watch.yml` uses `workflow_run` by design (§4 D3), so the E1/D3 PR
will carry one explained inline suppression, registered in the suppression allowlist and
reviewed in that PR. B2 itself adds none.

### 15.5 Gates and reviews

**Required union.** The diff edits workflows (one job added), Python tests (the B2 section
of an existing test file) and the generated inventory. That requires:
- full pytest;
- `code-reviewer` and `architecture-reviewer`;
- a pyright baseline diff;
- the blocking flake8 selection on changed Python;
- inventory regeneration plus `--check`;
- local actionlint and zizmor clean.

No product, route, template, JS or CSS change is involved, so no Chromium gate applies.
All figures below are as the lead reported them.

**Tests first.** automation-qa wrote the B2 contracts before the implementation existed:
25 tests, of which 18 failed and 7 passed before implementation. After the review fixes
the B2 section holds 26 tests, and `tests/test_ci_expansion_contracts.py` holds 113 (A1's
87 plus B2's 26).

**Mutation proof.** The mutation driver was a scratch script and was never committed.
- At `704016f5`, it killed 57 / 57 arms.
- At `9823beb9`, it killed 72 / 72 arms, and all 6 / 6 unmutated controls stayed green.
- The arms include:
  - an unpinned digest; verification after `tar`; `sha256sum --ignore-missing` or
    `--quiet`; a dropped `--fail` or `--proto`; `wget`;
  - `|| true`, `continue-on-error`, a job `if:`, a paths filter;
  - zizmor `--min-severity high`, `--offline` or `--no-exit-codes`;
  - linter-softening environment variables (`SHELLCHECK_OPTS`, `ZIZMOR_OFFLINE`,
    `ZIZMOR_CONFIG`) and a `GITHUB_ENV` export;
  - a checkout without `persist-credentials: false`;
  - PR title, `github.ref_name`, `github.base_ref` or `github.ref` in a `run:`;
  - release `cache: 'pip'`;
  - an unregistered `zizmor: ignore` or `shellcheck disable`, and zizmor config files;
  - promotion into `REQUIRED_CONTEXTS`.

| Gate | Commit | Result |
|---|---|---|
| Full pytest, local | `704016f5` | 5,355 passed, 2 skipped, 0 failed, 1654.5 s |
| Full pytest, local | `9823beb9` | **5,356 passed, 2 skipped, 0 failed, 1615.6 s**: A1's 5,330 plus the 26 B2 tests |

The skip count (2) in both full runs matches §14's A1 baseline. The skipped identities
were not re-captured in these runs, so this record does not claim they are the same two
as §13.1.

| Gate | Commit | Result |
|---|---|---|
| B2 section plus the 8 workflow-contract files | `9823beb9` | 323 passed |
| pyright 1.1.410 baseline diff | `704016f5` and `9823beb9` | PASS, 0 net-new on both |
| flake8 blocking selection on changed Python | `704016f5` and `9823beb9` | 0 on both |
| `generate_test_inventory.py` regeneration | `704016f5` and `9823beb9` | regenerated in both; 3,300 before B2 → 3,325 at `704016f5` → 3,326 at `9823beb9` |
| `generate_test_inventory.py --check` | `9823beb9` | up to date (3,326 collected) |
| actionlint 1.7.12 + pinned shellcheck 0.11.0 + `-pyflakes=`, local | `9823beb9` | exit 0, no output |
| zizmor 1.30.1 `--min-severity medium .github/workflows`, local | `9823beb9` | "No findings" offline and online |

**At the published head `d5dfa061`.** Relative to `9823beb9`, it tightens test assertions
inside existing tests, adding no new identities, and changes documentation. Full pytest
last ran at `9823beb9` (5,356 / 2 / 0) and was not re-run at `d5dfa061`.

| Gate | Commit | Result |
|---|---|---|
| `test_ci_expansion_contracts.py` + `test_release_workflow_contracts.py` | `d5dfa061` | 176 passed |
| The 9 workflow-contract files | `d5dfa061` | 323 passed |
| flake8 blocking selection on changed Python | `d5dfa061` | 0 |
| `generate_test_inventory.py --check` | `d5dfa061` | up to date (3,326) |
| Mutation driver (scratch, not committed) | `d5dfa061` | 74 / 74 arms killed, 6 / 6 controls green |

**Fixes applied** (against the §15.3 baseline).
- **Checkouts.** All 32 `actions/checkout` steps set `persist-credentials: false`: the
  31 existing ones plus the lint job's own. By file: 20 `ci.yml`, 6 `deep-gate.yml`,
  5 `release.yml`, 1 `_packaged-windows.yml`.
  No job needs persisted git credentials. After checkout, jobs run only local
  `git diff`, `git status`, `git show`, `git rev-parse`, `git merge-base` and
  `git ls-files`. `scripts/release_gate.py` calls the API via `urllib` with an explicit
  token.
- **Release caches.** The `release.yml` jobs `first-install` and `old-db-migration` no
  longer set `cache: 'pip'`. In `9823beb9` the workflow comment was narrowed so it no
  longer claims the whole tag path is cache-free (see residuals below).
- **Template injection.** `release.yml` now passes `--ref "$GITHUB_REF"`.
- **SC2016.** Four inline `# shellcheck disable=SC2016` directives, each with a reason.
  The pwsh probe became a `run: |` block to carry its directive.

**Local seeded evidence.** These are local checks, not the §4 acceptance rehearsals in
§15.6.
- Seeding a PR-title interpolation into a scratch copy made zizmor exit 14
  (`template-injection`, High) and actionlint exit 1.
- Flipping one character of a digest made `sha256sum --check --strict` fail before any
  extraction.
- A real download stall hit `--max-time 120` and recovered on retry. The install step
  exited 0 after 2 min 07 s.

**Online availability coupling: an owner decision before C4.** The lead probed online
zizmor. With an invalid token, or with the API unreachable, zizmor exits 1. That fails
closed: the job turns red and never falsely green. The cost is that a GitHub API outage
can red this job. Before C4 promotes it, the owner chooses between two options:
- keep it online as a single check; or
- split it into an offline required check plus an online non-required or scheduled
  audit.

This record does not decide.

**Reviews.** Each reviewer was a Claude Code subagent launched by the lead, 2026-10-20
(UTC 2026-10-19), independent of the implementation. They read files and ran nothing.
Internal agent IDs were not recorded.

| Reviewer | Commit | Verdict | Findings and dispositions |
|---|---|---|---|
| `code-reviewer` | `704016f5` | **approve with nits** | S1, no curl retry/timeouts: fixed in `9823beb9`. S2, linter-softening env vars not contracted: fixed (exact env key sets, no `GITHUB_ENV`, no workflow-level env). N1, `_packaged-windows.yml` pip cache: recorded residual. N2, stale test-file name in §15: fixed in this documentation update. N3, mutation driver not committed: confirmed. N4, widened untrusted-context pattern: fixed. N5, full `sha256sum` flags pinned: fixed. N6, `--proto-redir`: fixed. N7, the Linux tar member layout can only be proved on a Linux runner: proved by green-control rehearsal run `39342689323` (§15.6). Online mode is acceptable while non-required; owner decision before C4. |
| `architecture-reviewer` | `704016f5` | **approve with nits** | Should-fix, stale §15 file name: fixed in this documentation update. Should-fix, the `release.yml` cache comment overclaimed tag-path cache-freedom: narrowed in `9823beb9`, residual recorded. "Inventory not regenerated": withdrawn by the reviewer in its delta review (it had misread the post-`704016f5` count); the inventory is regenerated in both commits. Nits: B1 inventory pointer (added, §15.4); untrusted-pattern gap (fixed). Endorsed building E1+D3 on B2 with the merge order in §15.2. |
| `code-reviewer`, delta | `9823beb9` / `5e80a091` | **approve** | All prior S and N items resolved; no new defect. Nit N-a: the download contract should also pin `--proto-redir '=https'` and `--max-time`; applied in `d5dfa061`. Nits N-b and N-c: the checkout count (32), the inventory-row wording and the Dependabot line number (109); applied in `d5dfa061`. |
| `architecture-reviewer`, delta | `9823beb9` / `5e80a091` | **approve with nits** | Withdrew the "inventory not regenerated" point. Nits: the §0.4 dated note, the §15.2 stacking text, the §7 D3/E1 row wording and the inventory base count (3,300 before B2); applied in `d5dfa061`. |

A review that did not run, or whose reviewer failed, is recorded as incomplete, never as
"no findings".

**Residuals and observations.** These have no owner yet and are recorded for routing.
- **`_packaged-windows.yml` pip cache.** It keeps `cache: 'pip'` and is reachable from
  the tag path through `workflow_call`. zizmor does not flag it. It is the shared PR,
  weekly and release build. Route to A2/A3 or the owner.
- **Dependabot cooldown.** `.github/dependabot.yml` has 3 × `dependabot-cooldown` (§15.3).
  This is D-6-adjacent. Route to the owner.
- **Stale Dependabot comment.** `.github/dependabot.yml:109` describes deep-gate's opt-in
  `visual-linux` job. That comment becomes more stale after E1. Fix later.

*Dated disposition, 2026-10-20:* all three residuals, and the zizmor online/offline
question above, are dispositioned in §18. The text above is kept as written.

### 15.6 PR, rehearsals and post-merge evidence

**Acceptance rehearsals (§4 B2).** Both ran on `ubuntu-latest` from throwaway branches
built on `9823beb9`. Neither branch is merged. Both are retained, because branch deletion
is not authorized under the Operation A teardown restrictions. These runs are rehearsals,
**not** the representative PR run.

| Case | Branch / head | Mutation | Run | Window (UTC, 2026-10-19) | Result |
|---|---|---|---|---|---|
| Green control | `rehearsal/b2-green-v1` @ `807d203e` | adds a throwaway push-triggered `b2-rehearsal.yml` whose job is a byte-for-byte copy of `ci.yml`'s `workflow-lint` job (substring identity checked when generated) | [`39342689323`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39342689323), push, attempt 1 | 23:37:13Z → 23:37:29Z | **success** |
| Seeded red | `rehearsal/b2-seeded-red-v1` @ `184070f4` | the green branch, plus a `ci.yml` job whose `run:` is `echo "${{ github.event.pull_request.title }}"` | [`39342691486`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39342691486), push, attempt 1 | 23:37:14Z → 23:37:28Z | **failure** |

- **Green control.** Every step succeeded:
  - install, printing zizmor 1.30.1 and ShellCheck 0.11.0;
  - actionlint;
  - zizmor, "No findings to report".

  This proves the Linux tarball member layout on a real runner (code-reviewer N7).
- **Seeded red.**
  - Step `actionlint` failed with exit 1: `"github.event.pull_request.title" is
    potentially untrusted … [expression]` at `ci.yml:173:22`.
  - Step `zizmor (min severity medium)` still ran under `!cancelled()`. It failed with
    exit 14: `error[template-injection]`, 1 high.
  - Both linters independently turned the job red.

**Publication.**
- Pushed `ci/b2-workflow-lint` and opened ready PR
  [#532](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/532), verified `OPEN`
  and `isDraft: false` at 2026-10-19T23:52:50Z.
- The published head is `d5dfa0615fb5770dca2fab50a8d052211c99308b`.
- This receipt-only commit changes nothing but this file, and it starts a new PR run. That
  run supersedes the one below as the current-head carrier. A run that is incomplete or
  cancelled is not credited.

**PR CI run [`39344273368`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39344273368)**
(`pull_request`, attempt 1, head `d5dfa061`, created 2026-10-19T23:52:53Z, last job done
2026-10-20T00:05:01Z, 12.1 min): **all 26 jobs success**, A1's 25 plus the new one. This
is B2's clean representative PR run (§4 B2 acceptance).

| Context | Completed (UTC) | From creation |
|---|---|---|
| `Workflow Lint (actionlint + zizmor)` | 23:52:57Z → 23:53:07Z (10 s) | 0.2 min |
| `Run Tests` | 2026-10-20T00:00:34Z | 7.7 min |
| `E2E Functional (Chromium)` | 2026-10-20T00:03:24Z | 10.5 min |

The check name was observed on the PR exactly as `Workflow Lint (actionlint + zizmor)`.
That observation is one input to C4's "actual check-name observation". C4 itself is not
activated, and the job is not a required check.

**Pending: the post-merge `main` push run.** It cannot exist before merge, and B2
qualification is not complete until it is recorded. After the owner merges #532, record
in this ledger the first `main` push run on the squash commit: the
`Workflow Lint (actionlint + zizmor)` job's conclusion and its executed steps. It is not
inferred from PR runs.

**Promotion.** A red seeded job is pre-activation evidence only. Promotion still needs C4
activation and its blocking proof, which this authorization excludes.

**2026-10-20 post-merge receipt — the pending paragraph above is discharged.**
Under the later delegation (§16.8), #532 was squash-merged at `2026-10-20T13:12:10Z`
as `1a5e0e6fa1fbcfbb3544c16270edf6367956a435`, from verified head `ddda9492`.
The first `main` push run is
[`39428398134`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39428398134),
attempt 1, on that exact squash SHA. Job `118646704773`, named exactly
`Workflow Lint (actionlint + zizmor)`, succeeded at `13:12:27Z` (started `13:12:17Z`).
Its checkout, pinned-tool install, `actionlint` and `zizmor (min severity medium)`
steps all executed and succeeded. This completes B2's missing main-push lint evidence;
the overall pipeline was still running when this job-level receipt was read.
No required-check promotion or C4 activation is implied.

## 16. E1 + D3 execution — 2026-10-20

Recorded by `product-manager` from the coordinating lead's relay and the lead's E1/D3
implementation brief, which quotes the owner's requirements verbatim (§16.1). Evidence is
as the lead reported it, tied to these commits:
- E1+D3 implementation `b99b0ce4064b2809313c69d76c85fd7665b657d3`;
- creation guard `29f8dfa1c9267f8088864ebcf055847d63ad8a11`;
- review fixes `d3b6e527c52d7f1e3f5577bed1d1f5ec7bf59775`;
- final `MANAGED_LINE` wording `44cd54165c523c6cf2ef1507d5138862343fc80c`.

Short forms refer to these. The published PR head is `cacc3f79e0eddc07fcb046654dd2cff0d4d1049c`
(§16.7). All post-merge evidence is pending; nothing pending is filled in advance.

### 16.1 Authority

The same 2026-10-20 owner instruction as §15.1 authorizes "E1 + D3: separate Linux visual
workflow and deterministic Deep Gate monitoring, delivered together as the coherent
observability change permitted by the plan". The same stop-before-merge boundary applies,
and the same exclusions: settings, C4, credentials, spending, release publication and
later packets.

Owner requirements, verbatim as quoted at the top of the brief:

> Move visual-linux into Deep Gate Visual (Linux), preserving its weekly schedule, dispatch inputs,
> compare behavior, and visual policy. Retain the six other Deep Gate jobs.
> - Track each workflow independently.
> - Upsert a workflow-specific issue for non-success completion, targeting the approved one-hour bound.
> - Detect missing scheduled runs within the approved 36-hour bound using the current expected Monday 03:17 UTC slot.
> - Manual runs, prior-week runs, and successes from another workflow cannot satisfy scheduled freshness.
> - Resolve a visual-failure issue only with newer, successfully executed compare-mode evidence for the matching workflow/run/attempt/head.
> - Skipped comparison, generation-mode success, and a green six-job Deep Gate cannot establish visual recovery.
> - Handle duplicate/stale events, pagination, API failures, and incomplete or late runs explicitly.
> Use minimal permissions and no execution of untrusted upstream artifacts. Preserve ADR-011,
> baselines, tolerances, exemptions, and E3's diagnostic boundary.
> Update the named workflow census, visual-source, seed, and recovery contracts. Provide the
> approved behavioral fixtures and bounded live evidence. Distinguish measured timing from timing
> that remains unproven.

**Boundaries as applied here.** This packet does separation and monitoring only.
- No rendering fix.
- No baseline regeneration.
- No ADR-011, tolerance or exemption change.
- E3's diagnostic boundary is preserved: [GATE2.md](../deep_gate_linux_visual_failure_20260831/GATE2.md)
  is untouched.

### 16.2 Claim, isolation and serialization

- **Claim.** Claude Code (Opus) CI coordinating lead, 2026-10-20, for D3 and E1 (§7).
- **Isolation.** Standalone clone `D:/development/Hypertrophy-Toolbox-v3-ci-e1d3-20261020`
  on `ci/e1-d3-deep-gate-observability`, with its own `.git`, `.venv` and `node_modules`.
- **History.**
  - The branch was started from `origin/main` `f3adacf1` and rebased onto `9823beb9`.
  - It was then re-stacked onto B2's final head `ddda9492`.
  - Rebase conflicts:
    - `deep-gate.yml`: E1's removal of the visual job was taken onto B2's checkout lines.
    - `tests/test_ci_expansion_contracts.py`: both the B2 and the D3 sections were kept.
  - The test inventory was regenerated.
- **Serialization.** As §15.2 records, the PR targets `main`, carries B2's commits and
  merges after #532. This is the departure from §0.4 noted at §0 item 4.
- **Coordination.** Another session dispatched manual Deep Gate run `39331294762` on
  `visual/linux-baseline-resync-20261020`, with no PR and no claim (§15.2). The watch
  ignores non-`main` runs, and no files overlap.

| Role | Agent | Owns |
|---|---|---|
| `product-manager` | this agent | This file only |
| `automation-qa` | — | Contracts and behavioral fixtures, written before implementation |
| `senior-developer` | — | Implementation through `d3b6e527`. The owner stopped this agent during the pause; it is not relaunched without an explicit owner request |
| `code-reviewer` | Claude Code subagent launched by the lead, 2026-10-20 (UTC 2026-10-19), read-only | Independent review (§16.4) |
| `architecture-reviewer` | Claude Code subagent launched by the lead, 2026-10-20 (UTC 2026-10-19), read-only | Independent review (§16.4) |
| Coordinating lead | Claude Code (Opus) | Bounded live rehearsals (§16.5); the wording-only `MANAGED_LINE` commit `44cd5416` |

Internal agent IDs were not recorded.

### 16.3 Design

**E1: `.github/workflows/deep-gate-visual.yml`, "Deep Gate Visual (Linux)".**
- Triggers: schedule `17 3 * * 1`, plus `workflow_dispatch` with `visual_mode`
  (`compare` | `generate`, default `compare`).
- One job, `visual-linux` / `Visual regression (Linux baselines)`: `ubuntu-24.04`,
  timeout 25 min, no job `if:`.
- The mode is resolved in its own step. The compare and generate steps are split, so the
  API shows whether compare actually executed.
- **Deliberate interface delta, for owner acknowledgement: `run_visual` is dropped.**
  - The `architecture-reviewer` judged dropping it the safer choice. Keeping it would need
    a job-level `if:`, and a default-false dispatch would then report green without
    comparing.
  - A stale `-f run_visual=true` dispatch now fails loudly, with HTTP 422.
  - This still departs from the literal owner wording "preserving … dispatch inputs". The
    owner has not yet acknowledged it.

**E1: `deep-gate.yml`.** It keeps its six jobs, names unchanged, and now has no
dispatch inputs.

**D3: `.github/workflows/deep-gate-watch.yml`.**
- **Triggers:**
  - `workflow_run` on both workflow names, type `completed`, branch `main` only. It carries
    one registered `zizmor: ignore[dangerous-triggers]` with its reason (§15.4).
  - An hourly Monday–Tuesday cron `23 * * * 1,2`.
  - A 6-hourly backup sweep `53 */6 * * *` (review fix, `d3b6e527`). It is a backup for
    lost deliveries, not a means of meeting the one-hour target (§16.6).
  - `workflow_dispatch` with `dry_run`.
- **Permissions:** `{}` at the top level. The job gets `actions: read`, `contents: read`
  and `issues: write`.
- **Concurrency:** group `deep-gate-watch`, no cancellation.
- **Untrusted input:** default-branch checkout only, no artifact download, no install. The
  triggering event is read only as data.

**D3: `scripts/deep_gate_watch.py`** (standard library only).
- **Reconciliation.** Every trigger reconciles the full history over a 21-day window.
- **Issues.** Each workflow has two independent issue kinds: failure and missing-schedule.
  Each issue carries an HTML marker with `evidence=<run>.<attempt>` and `created=`.
- **Recovery.**
  - The suite issue resolves on a newer run in which every job succeeded.
  - The visual issue resolves only on a newer run in which three things succeeded: the
    `Visual regression (Linux baselines)` job, its `Run visual specs (compare)` step and its
    `Assert compare mode wrote no baseline` step.
  - Generation success, a skipped compare and a green suite never resolve the visual issue.
- **Freshness.**
  - Only `schedule` runs on `main` count, created in [slot, slot + 7 d) for the current
    Monday 03:17Z slot.
  - The alarm threshold is 20 h; the approved bound is 36 h.
  - The first hourly check after the threshold is Monday 23:23Z, 20 h 06 min after the
    slot. That leaves 15 h 54 min of margin before the bound.
- **Creation guard** (`29f8dfa1`). A slot that began before the workflow's `created_at` is
  `not_applicable`.
- **Fail-closed.**
  - Any of these makes that workflow unavailable: an API error, a pagination problem (cap
    50, same-origin `Link` only), malformed data, or a jobs/attempt/head mismatch.
  - "Unavailable" means exit 2 and no writes. It is never reported as healthy.
  - Degraded path (review fix, `d3b6e527`): a failure run whose jobs cannot be read still
    opens the failure issue, marked "job details unavailable". It can never count as
    recovery or suppress a newer failure. Mismatched job rows are never shown, and the
    path is idempotent.
- **Managed issues** (`44cd5416`). Each issue body carries this `MANAGED_LINE` (§16.6):
  `_Managed by Deep Gate Watch — do not edit the HTML comment marker; closing this issue by hand does not acknowledge it: the next sweep recreates it while the state persists._`
- **Ordering.** A stale or duplicate delivery never regresses or duplicates an issue.

**Reference and documentation updates.**
- `scripts/css_audit/p3_ceiling.py` now reads the visual spec pair from
  `deep-gate-visual.yml`. This is a required reference update; no audit baseline was
  regenerated.
- Narrow documentation updates: `docs/ai_workflow/QUALITY_GATE.md` and `e2e/CLAUDE.md`.
- Review fixes in `d3b6e527`: `docs/MASTER_HANDOVER.md:486`,
  `.github/dependabot.yml:109`, and an E1/D3 subsection in
  [B1_ACTION_INVENTORY.md](B1_ACTION_INVENTORY.md).
- **Known-stale, deliberately left alone:**
  - `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json:221` (the baseline ledger's
    `scopeNote`);
  - historical evidence documents.

### 16.4 Gates and reviews

**Commits.**
- Implementation `b99b0ce4064b2809313c69d76c85fd7665b657d3`, rebased from `655e008f` /
  `b78bd296`.
- Creation guard `29f8dfa1c9267f8088864ebcf055847d63ad8a11`, rebased from `ade69ae8`.
- Review fixes `d3b6e527c52d7f1e3f5577bed1d1f5ec7bf59775`, by the senior-developer.
- `MANAGED_LINE` wording `44cd54165c523c6cf2ef1507d5138862343fc80c`. The CI lead applied
  this change, not the senior-developer, because the owner had stopped the developer agent
  during the pause.
- PR head `cacc3f79e0eddc07fcb046654dd2cff0d4d1049c`: `44cd5416` plus the commit carrying
  the §16 PLANNING.md update.

**Tests first.** automation-qa wrote:
- 136 D3 tests, all erroring with `ModuleNotFoundError` before the implementation existed;
- 21 creation-guard tests;
- 19 review-fix tests, in `d3b6e527`.

On the E1 contracts, 30 / 30 workflow mutations were killed.

| Gate | Commit | Result |
|---|---|---|
| Full pytest, local | `ade69ae8` (pre-rebase) | 5,550 passed, 2 skipped, 1606 s |
| Full pytest, local | `29f8dfa1` | **not credited**: 5,549 passed / 1 failed. The working tree was edited mid-run, so the watch cron contract read a file the developer had just changed |
| Full pytest, local (code-reviewer N6) | `d3b6e527` | **5,569 passed, 2 skipped, 0 failed, 1543.2 s**, 2026-10-20T11:19:04Z → 11:44:48Z, with no concurrent working-tree edits |
| 7 contract files | `29f8dfa1` | 477 passed |
| actionlint + pinned shellcheck + `-pyflakes=`, all workflows | `d3b6e527` | exit 0 |
| zizmor `--min-severity medium`, offline and online | `d3b6e527` | "No findings" (4 ignored, 13 suppressed); the one registered `dangerous-triggers` ignore |
| pyright baseline diff | `d3b6e527` | PASS, 0 net-new |
| flake8 blocking selection | `d3b6e527` | 0 |
| Test inventory `--check` | `d3b6e527` | up to date (3,520 collected at `ade69ae8`) |
| D3 section + `test_release_workflow_contracts.py` | `44cd5416` | 385 passed |
| flake8 blocking selection; advisory (complexity 10, line 127) | `44cd5416` | 0; 0 |
| pyright on `scripts/deep_gate_watch.py` | `44cd5416` | 0 errors |
| Full pytest on the committed PR head | `cacc3f79` | **5,569 passed, 2 skipped, 0 failed, 1534.7 s**, 2026-10-20T11:48:24Z → 12:13:59Z, with no concurrent edits |
| Test inventory `--check` | `cacc3f79` | up to date |

`deep-gate-visual.yml` is byte-identical between the rehearsed `b78bd296` and `d3b6e527`
(`git diff --quiet`), so compare rehearsal `39343153293` still applies to the final file.
`44cd5416` is a one-line wording change made after the `d3b6e527` gates. Its own targeted
gates are the `44cd5416` rows above.

**Reviews.** The first reviews were on `29f8dfa1` and the delta reviews on `d3b6e527`. All
reviewers were Claude Code subagents launched by the lead, and they were read-only.

| Reviewer | Verdict | Findings and dispositions |
|---|---|---|
| `code-reviewer` | **approve with nits** | **S1**, the day-one suite issue: kept deliberately and documented (§16.5). **N1**, a jobs error blocks the failure issue: fixed in `d3b6e527`. **N2**, the sweep ran Monday–Tuesday only and nothing watches the watchdog: a 6-hourly sweep was added; watching the watchdog is recorded as a known limit (§16.6). **N3**, `created_at` registration semantics: at most one false "missing", never a false green. **N4**, a repeated comment on a partial close: accepted. **N5**, style: the unused `id: visual` is kept because a contract pins the step ids, and the static concurrency group is accepted. **N6**, a final-head full pytest is required: run at `d3b6e527`, 5,569 / 2 / 0. |
| `architecture-reviewer` | **approve with should-fixes** | **Day-one false alarm:** kept deliberately, with a healing follow-up (§16.5). **Jobs-error suppression:** fixed in `d3b6e527`. **Name the `run_visual` delta:** done (§16.3). **Stale `MASTER_HANDOVER.md:486`:** fixed in `d3b6e527`. **B1 inventory line:** fixed in `d3b6e527`. **`MASTER_HANDOVER.md:41` / `:104` and the DECISIONS R1-D3 gate-clock reading:** not edited here, because docs PR #531 rewrites that block (§16.6 follow-up). **Nits:** marker durability, fixed with a "do not edit" line; cron-margin wording, fixed. |
| `code-reviewer`, delta on `d3b6e527` | **approve** | The degraded path is fail-closed: it can never become recovery or suppress a newer failure, mismatched rows are never shown, and it is idempotent. The QA test changes weaken nothing. All three nits are accepted and recorded: **(a)** a "job details unavailable" issue is not backfilled at the same evidence key; **(b)** there is no success-run timeout arm (it takes the same path as a 502); **(c)** the 6-hourly sweep is a backup, not the one-hour target (§16.6). |
| `architecture-reviewer`, delta on `d3b6e527` plus the §16 draft | **approve with nits** | **Withdrew** its classify special-case, and accepts keeping the day-one suite issue on condition that the healing dispatch is recorded as an owner action (done, §16.5). **Should-fix:** a manually closed issue does not stay closed, because the sweep recreates it. Fixed by the `MANAGED_LINE` commit `44cd5416` (§16.3, §16.6). It also reported the §0.4 note as missing; the note exists at §0 item 4 (from §15.2), and §16.2 now points to it. |

**Disposition of S1 / the day-one finding.** The day-one suite issue is kept. The
architecture-reviewer accepted this, on condition that the healing dispatch is recorded as
an owner action. The code-reviewer accepted it.

**The DECISIONS R1-D3 gate-clock point.**
- After E1, the weekly-gate evidence spans two workflows.
- The R2.4 / R1-D3 three-green clock should therefore be read per workflow.
- The owner decisions themselves are unchanged.
- Handle this at the next handover refresh.

### 16.5 Live evidence

These are bounded rehearsals on push-triggered throwaway branches. None of the branches is
merged, and all are retained (no branch deletion under the Operation A teardown
restrictions). The visual compare and v1 dry-run ran on the pre-rebase tree `b78bd296`;
`deep-gate-visual.yml` is byte-identical at `d3b6e527` (§16.4). The v2 dry-run ran on the
final code.

| Case | Branch @ head | Run | Window (UTC) | Result |
|---|---|---|---|---|
| Visual compare | `rehearsal/e1d3-visual-compare-v1` @ `9edc9d6d` (`b78bd296` plus a push trigger) | [`39343153293`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39343153293), push, attempt 1 | job 2026-10-19T23:41:54Z → 23:58:11Z (16.3 min) | failure, as expected (the known reds) |
| Watch dry-run v1 | `rehearsal/e1d3-watch-dryrun-v1` @ `a4e1d308` (`b78bd296` plus a push trigger, `DRY_RUN` forced true, `issues: read` only so writes were impossible) | [`39343196678`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39343196678), push, attempt 1 | 2026-10-19T23:42:15Z → 23:42:36Z | success |
| Watch dry-run v2 | `rehearsal/e1d3-watch-dryrun-v2` @ `2d0f13f6` (`d3b6e527` plus a push trigger, `issues: read`, `DRY_RUN` forced) | [`39414109552`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39414109552), push, attempt 1 | 2026-10-20T11:19:18Z → 11:19:44Z | success |

**Visual compare.**
- Steps:
  - `Resolve visual mode`: success.
  - `Run visual specs (compare)`: **failure, 65 failed / 18 passed**. This matches the 65
    pre-existing H-LINUX-UNSYNC-01 captures.
  - `Run visual specs (generate)`: skipped.
  - `Assert compare mode wrote no baseline`: success.
  - Generated-baseline upload: skipped.
  - Report upload: success.
- ADR-011 is unchanged and no baseline was written.
- For comparison, the last scheduled in-workflow visual job, in run `39226020933`, took
  12.7 min.

**Watch dry-run v1 summary.**
- **Suite:** "failing (run 39226020933 attempt 1)"; freshness "fresh" for slot
  2026-10-19T03:17Z; planned action "create failure issue".
- **Visual:** "unknown", "missing"; planned action "create missing-schedule issue".
- That visual result exposed the gap for slots before the workflow existed, which led to
  the creation guard in `29f8dfa1`.

**Watch dry-run v2 summary (final code).**
- **Suite:** "failing (run 39226020933 attempt 1)"; fresh for slot 2026-10-19T03:17Z;
  planned action "create failure issue". This is the expected day-one issue.
- **Visual:** failure "unknown"; freshness "**not_applicable** (workflow created after this
  slot began)"; no planned action. The creation guard is confirmed on live data.

**Not exercised live.** Neither dry-run exercised the degraded path, the 6-hourly sweep or
the managed line on live data; those are proven by fixtures only. The creation guard was
exercised live, in v2.

**Expected day-one behaviour after merge.**
- The first reconcile opens "Deep Gate (manual + weekly) — failing" from pre-split run
  `39226020933`. That run failed only on the visual job that has now moved. This is kept
  deliberately, so the Linux failure stays visible across the split (§4 D3).
- **Healing follow-up: owner actions.** No post-merge authority is held, so these
  dispatches are the owner's. After merge, dispatch each workflow once on `main`:
  - `deep-gate.yml`: a green six-job run heals the suite issue.
  - `deep-gate-visual.yml` in compare mode: it will fail on the known reds and open the
    visual failure issue. Linux tracking then lives with its own workflow.
- The visual missing-schedule check is `not_applicable` for the 2026-10-19 slot. It is
  live from the 2026-10-26 slot.

### 16.6 Measured versus unproven

**Measured:**
- classification against real history (dry-runs v1 and v2, including the creation guard);
- compare execution and its duration;
- B2's `Workflow Lint (actionlint + zizmor)` linting `deep-gate-visual.yml` and
  `deep-gate-watch.yml` in CI, green with the one registered suppression (PR run
  `39421286969`, §16.7).

**Unproven until after merge:**
- **Dispatch latency of `workflow_run`.** It bounds the one-hour target. The step summary
  records a "Dispatch latency" line for each event. That line measures from the watched
  run's `updated_at` to the watchdog's start. It excludes the watchdog's own runtime and
  its issue-write time, while the one-hour bound is end to end.
- **Cron delay for the watch schedule.** It bounds the 36-hour target. The 6.5–7.5 h figure
  is the Deep Gate's observed cron delay (§2.1), used here only as an estimate.
- **The first real scheduled visual run,** due 2026-10-26.
- **Issue writes with `issues: write`,** label creation (`POST /labels`), and closing an
  issue with `state_reason`.
- **Real `Link`-header pagination** beyond one page, and the `created>=` filter. Both are
  proven by fixtures only.
- **The degraded path and the 6-hourly sweep** on live data.

**Known limits.**
- **Nothing watches the watchdog** (code-reviewer N2).
- **Lost `workflow_run` deliveries** are bounded by the 6-hourly sweep, which means up to
  about 6 h plus cron delay, not 1 h (code-reviewer delta nit c).
- **A manual close does not acknowledge an issue.** The sweep recreates a manually closed
  issue while the condition persists. The `MANAGED_LINE` (`44cd5416`) makes this
  explicit in the issue body (architecture-reviewer delta should-fix).

**Post-merge follow-ups to record in this ledger:**
- **Healing dispatches (owner action).** Dispatch `deep-gate.yml` once on `main`, and
  `deep-gate-visual.yml` once in compare mode (§16.5).
- **Rebase after #532 merges.** On this branch, run
  `git rebase --onto origin/main ddda9492` (B2's head), then re-run CI on the final head.
- **Owner acknowledgement of the `run_visual` delta** (§16.3).
- **`MASTER_HANDOVER.md` gate-clock reading (`:41` / `:104`).** Record the per-workflow
  reading (§16.4).
  - Owner: the next session holding the handover-writer role.
  - Trigger: the later of the #531 merge and this PR's merge.
  - This PR edits `MASTER_HANDOVER.md:486`, a region #531 does not rewrite. Re-check for
    conflicts at merge either way.
- **The 2026-10-26 slot.** Record the first `fresh` result for both workflows and the
  first scheduled `Deep Gate Visual (Linux)` run.
- **The first `workflow_run`-triggered watch run,** with its dispatch-latency line.
- **The first scheduled watch runs** on Monday and Tuesday.
- **Whether a manually closed issue is recreated.**

### 16.7 PR and publication

**Publication.**
- **Push.** Pushed `ci/e1-d3-deep-gate-observability`. The first push attempt failed with a
  connection reset and was retried.
- **PR.** Opened ready PR [#533](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/533),
  titled with the suffix "[stacked on #532]". It was created at about
  2026-10-20T12:18Z, after one GitHub API 499 on the first attempt, and verified `OPEN`
  with `isDraft: false`.
- **Published head:** `cacc3f79e0eddc07fcb046654dd2cff0d4d1049c`.
- **PR body** states:
  - the binding merge order: #532 first, then `git rebase --onto origin/main ddda9492`
    and a CI re-run on the final head;
  - the `run_visual` delta, for owner acknowledgement;
  - the day-one issue and the owner's healing dispatches;
  - that `git merge-tree` of `cacc3f79` against #531's head `20264e1b` is clean.
- **This commit.** This receipt-only commit changes nothing but this file, and it starts a
  new PR run. That run supersedes the one below as the current-head carrier. A run that is
  incomplete or cancelled is not credited.

**PR CI run [`39421286969`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39421286969)**
(`pull_request`, attempt 1, head `cacc3f79`, 2026-10-20T12:18:41Z → 12:30:26Z): **all 26
jobs success.**
- `Workflow Lint (actionlint + zizmor)` succeeded at 12:18:55Z. This is B2's lint checking
  the new `deep-gate-visual.yml` and `deep-gate-watch.yml` in CI, with the one registered
  suppression.
- `Run Tests` succeeded at 12:26:48Z.
- The run carries B2's commits, as the stack requires (§16.2). It is **not** post-merge
  evidence. After #532 merges, the rebased final head needs its own CI run (§16.6).

### 16.8 Delegated decisions and merge execution — 2026-10-20

The owner supplied the three-PR handoff and asked: "span the ai consulting team to
decide and proceed with those PRs". Codex adopted that delegation for #531, #532 and
#533, including their binding rebase/CI sequence and bounded post-merge qualification.
It supersedes the earlier stop-before-merge boundary for these named PRs. It does not
authorize settings, C4, later packets, release publication or baseline regeneration.

Three independent read-only Codex advisers completed, with no blocking findings:
`/root/ci_architecture_consult`, `/root/ci_test_consult` and
`/root/ci_operations_consult`. They inspected source and recorded evidence, ran no
tests and made no changes. These are advisory reviews of merge readiness, not a new
formal council or replacements for the implementation reviews in §§15.5 and 16.4.

The primary session adopted their unanimous recommendations:
- **Accept the removal of `run_visual`.** Dispatching the separate visual workflow
  supplies opt-in; an unconditional job avoids skipped-green comparisons. The pending
  acknowledgement in §16.3 is discharged under this delegation.
- **Keep zizmor online while non-required.** API failure remains red. The choice of a
  required-check arrangement remains with C4; this does not authorize promotion.
- **Merge #532 first; then rebase #533; require new CI; merge #531 last.** #532 merged
  as `1a5e0e6f` (§15.6). `git rebase --onto origin/main ddda9492` completed without
  conflicts, producing `7b6fd959`; its complete tree is identical to the former
  `8ab0a5c8` head. This receipt adds documentation only. The resulting pushed head
  still needs its own successful CI before #533 can merge.
- **Qualify the split on merged `main`.** Run the six-job Deep Gate and the visual
  workflow explicitly in compare mode; inspect the real watchdog issue writes and
  completion-to-issue latency. Its dispatch-latency line excludes runtime and issue
  writes and cannot alone prove the one-hour target.

The 2026-10-26 scheduled runs and each workflow's freshness remain pending until
observed. Manual dispatches cannot satisfy scheduled freshness or ADR-007's visual
threshold. Existing release-cache and Dependabot-cooldown findings remain outside
this packet. Branches and worktrees are retained under the teardown restrictions.

### 16.9 Merge receipts and live qualification — 2026-10-20

**B2 final main-push result.** Run
[`39428398134`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39428398134)
on squash `1a5e0e6f` finished at `13:24:24Z`: **all 26 jobs succeeded**. This completes
the overall-pipeline reading that was still in progress in §15.6; the lint job's
executed-step evidence remains the receipt there. C4 is not activated.

**E1+D3 final-head CI and merge.** After the required rebase, documentation-only
commit `f9a675c79c841745d64b84708ea3dcdf2c2ccd2b` records §16.8 and the B2 lint
receipt. The source tree outside this plan is identical to reviewed head `8ab0a5c8`.
Fresh PR run
[`39428761400`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39428761400),
attempt 1, on `f9a675c7`, ran `13:14:50Z` → `13:26:40Z`: **all 26 jobs succeeded**.
The primary session then squash-merged #533 at `13:27:21Z` as
`48d6a4500aa24f2497f45995c94ebcebd352a407`. #531 rebased onto that merged main
without conflicts; it carries this documentation closeout.

**Bounded main dispatches.** All three use `48d6a450`; no baseline generation was
dispatched. These are manual qualification, not scheduled freshness evidence:
- Initial watch, `dry_run=false`:
  [`39430550927`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39430550927).
  It succeeded and created
  [suite issue #534](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/534)
  at `13:28:10Z`, from the deliberately retained pre-split failing run `39226020933`.
- Six-job suite:
  [`39430555131`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39430555131),
  dispatched at `13:27:33Z`; running at this reading.
- Visual, explicit `visual_mode=compare`:
  [`39430559081`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39430559081),
  dispatched at `13:27:35Z`; running at this reading.

**Visual result and first real event.** The visual run finished at `13:43:38Z` with
the expected **65 failed / 18 passed** (compare-step summary: 14.3 min). Its compare
step executed and failed; generation and generated-baseline upload were skipped;
`Assert compare mode wrote no baseline` succeeded. No baseline was regenerated.

The completion triggered successful watchdog run
[`39432907482`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39432907482),
event `workflow_run`, `13:43:40Z` → `13:44:05Z`. It created
[visual issue #537](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/537)
at `13:44:02Z`, pinned to `39430559081.1`, head `48d6a450`. The measured interval
from the watched run's completion `updated_at` (`13:43:38Z`) to the issue write is
**24 s**, including watchdog execution and the write. This one observed response
meets the one-hour target; it is not a guarantee about future deliveries or cron.
The log's separate dispatch metric is 21 s, to script start at `13:43:59Z`.

**E1+D3 main CI.** First main-push run
[`39430536736`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39430536736)
on `48d6a450`, `13:27:25Z` → `13:38:49Z`: **all 26 jobs succeeded**.

**Suite result.** Run `39430555131`, attempt 1, finished at `13:47:35Z`: **all six
jobs succeeded**, including full E2E and the real Windows bootloader smoke. A suite
completion-triggered watch run did not appear during qualification. The asymmetry
with the working visual trigger exposed the workflow-name filter defect in §16.10.
Suite issue #534 remained open during initial qualification; its automatic closure
after the correction is recorded in §16.10. It was never manually closed.

**Still pending after §16.10:** first 2026-10-26 scheduled runs/freshness for both
workflows; this cron's actual delay, lost-delivery recovery, live pagination beyond
one page, the degraded path and manual-close recreation. Issue creation, suite
recovery and both completion responses are now observed (§16.10); scheduled timing
is not yet credited.

### 16.10 D3 literal workflow-name repair discovered during qualification

The primary session found that suite success did not trigger the observer, while
visual failure did (§16.9). A follow-up by independent adviser
`/root/ci_test_consult` identified a concrete configuration defect: GitHub interprets
`on.workflow_run.workflows` entries as glob patterns, so the literal `+` in
`Deep Gate (manual + weekly)` must be escaped. The previous raw-name equality
contract incorrectly pinned the unescaped spelling. GitHub's
[workflow-name filter reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onworkflow_runworkflows)
documents that rule and gives an escaped `Build C++` example. This is a source
trigger defect, not evidence of a lost delivery or an excuse to claim recovery.

**Scope and authority.** Under the owner's delegation to decide and proceed with
the named PRs, the primary session authorized the necessary bounded correction of
D3 in follow-up [#538](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/538).
This applies the already approved requirement to watch both workflows; it starts
no later CI/CD packet and grants no settings, promotion or baseline authority.
The repair has two files only:
- `deep-gate-watch.yml`: use the single-quoted literal pattern
  `'Deep Gate (manual \+ weekly)'`, with a maintenance comment. Keep the actual
  workflow name, all triggers, permissions, jobs and script behavior unchanged.
- `test_release_workflow_contracts.py`: strengthen the existing subscription node
  to derive escaped literal patterns from the actual source workflow names. Keep
  the script-name, subscription-set, uniqueness, completed-event, main-branch and
  trigger-set assertions. No node is added or renamed; inventory is unchanged.

**Tests first and review.** The test adviser then acted only as the test implementer
in a new isolated checkout, `Hypertrophy-Toolbox-v3-main-pr533-watch-glob-20261020`.
The strengthened node failed against the unchanged broken filter: 1 failed in
0.21 s. The primary session applied the workflow correction; the node then passed:
1 passed in 0.14 s. Inventory `--check` is up to date. The committed repair head is
`7ac31956824c3cb81f64166dc4d2fb9391842516`.

Independent `code-reviewer` `/root/ci_architecture_consult` approved that exact
two-file diff, with no blocking findings; it wrote no code and ran no tests. Fresh
PR CI `39434706240` passed **26/26**. The clean full pytest result below completed
the remaining pre-merge gate. The earlier reviews remain historical evidence, not proof
that they caught this defect.

**Local setup correction; failed runs are not credited.** The primary session used
the older worktree helper from the stale main checkout, then initially ran with a
shared-venv junction and a PATH that selected the Windows WSL bash stub. That full
run ended **5,535 passed / 34 failed / 2 skipped, 1,545.63 s**: six bash-dependent
cases failed on the WSL stub; 28 lifecycle/snapshot cases rejected the reparse
interpreter path. Source was frozen; these were setup failures, not a passing gate.
The junction entry was retained under ignored artifacts, and a private ordinary
venv was installed from the pinned requirements. Git Bash is now selected through
a process-only PATH change. Seven representative checks passed in 3.99 s.

A second attempt exposed the default-config tests' dependence on an absent
`DB_FILE` override and was stopped without gate credit. The pytest process now
removes that override while retaining a target-bound `HT_RUNTIME_DIR`, private
temp/cache/bytecode paths and verified default DB resolution inside this checkout.
The configuration module passes **20/20**. The fresh full run used `--maxfail=1` on
the unchanged `7ac31956` tree and passed **5,569 / 2 skipped / 0 failed in
1,570.38 s**. Every collected case ran; fail-fast never activated. No test or
application code was weakened or changed
to work around the setup. Both created checkouts are retained with explicit local
ownership notes; current creation preflight and Operation A completion are not
claimed by those notes.

**Merge.** #538 merged at `2026-10-20T14:59:48Z` as
`b86e9ad783d6ba4e7b5835db5aec64a180e915da`, from reviewed head `7ac31956`.
Its tree matches that reviewed head. No baseline PNG changed from `f3adacf1`.

**Live delivery and recovery proof.** The primary session requested a rerun only
of the already-successful `Empty-schema initializer smoke` job (`118654192437`) in
suite run `39430555131`. Attempt 2 retained source head `48d6a450` and completed
successfully at `15:01:34Z`. This is a targeted delivery probe; it does not claim
that all six jobs reran. Attempt 1's six-job success in §16.9 remains the full-suite
evidence, and neither attempt is scheduled freshness evidence.

That completion automatically triggered successful watch run
[`39444622699`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39444622699),
event `workflow_run`, on the fixed default-branch head `b86e9ad7`:
`15:01:40Z` → `15:02:09Z`. Its log reports the suite healthy from
`39430555131` attempt 2 and closes
[suite issue #534](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/534)
at `15:02:01Z`: **27 s** from source completion `updated_at` to the issue change.
The separate dispatch metric is 23 s, to script start at `15:01:57Z`.
[Visual issue #537](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/537)
remains open and unchanged, pinned to the failed executed compare. No issue was
manually opened, closed or acknowledged during these checks.

Both completion paths now have one live response observation, including real
issue writes and suite recovery. This discharges the bounded manual healing
follow-up. The 2026-10-26 scheduled runs, per-workflow freshness, cron timing,
lost-delivery backup, real multi-page pagination, degraded path and manual-close
recreation remain unqualified. No settings, C4, later packet or visual-policy
change is authorized by this result.

## 17. B3 execution — 2026-10-20

Recorded by `product-manager` `a8501dd3530da91e2` from the manager session's written
records. This agent did not read the owner's message directly. The quotation in §17.1 is
the verbatim text that manager session `hypertrophy-toolbox-v3-main-68` reports
receiving. Facts and evidence in §§17.2–17.6 are as that session measured or the named
agent reported them. As of authorization (2026-10-20) nothing was implemented. The
evidence below is as of implementation commit
`90cde802e4ed4215db6e11e4d4ecd737380bdb15` (parent `71c4cc6d`), which also carries the
first §17 evidence update; short form `90cde802`. This receipts update is committed
after it and cannot cite its own commit. PR #539's CI is pending and is recorded at
closeout; nothing pending is filled in advance.

### 17.1 Authority

Owner authorization, 2026-10-20 local (+03:00), received by Claude Code session
`hypertrophy-toolbox-v3-main-68`. Verbatim excerpts:

> Take ownership of CI/CD packet B3: Dependency Review.
>
> I authorize implementation under the already-approved CI/CD core plan, required tests and independent reviews, commits, push and a ready PR. Stop before merge.
>
> Act as a read-only manager. Use product-manager for canonical planning edits, automation-qa for tests before implementation, senior-developer for implementation, and independent code-reviewer and architecture-reviewer.
>
> I delegate unresolved in-scope technical and plan-disposition decisions to an AI consulting team. When needed, spawn three independent read-only advisers covering architecture, testing and security/product risk. Adopt a reasoned decision, record dissent and actual agent IDs, and continue. Preserve required reviews and record delegated approval honestly; never invent my signature.
>
> Parallel boundaries:
> - This session alone owns the next shared CI workflow-edit slot.
> - Coordinate handoff of the stale B2/E1+D3 claims; do not silently release them.
> - I authorize creating one fresh standalone clone from the remote with independent Git storage, no alternates/hardlinks, and private dependencies/runtime/temp/cache paths.
> - Never pull, reset, stash or clean shared main. Retain the new clone and branch.
> - Other sessions own WS3, recovery, settings preparation and future-packet planning.
>
> Implement B3 exactly within the approved scope:
> - Reviewed full-SHA actions/dependency-review-action.
> - Proposed check name Dependency Review.
> - Every eligible PR; severity high; scopes runtime, development, unknown; warn-only false.
> - Minimal permissions and job-summary output; no PR-comment writes.
> - Preserve full pip/npm audits on main.
> - Keep Dependency Review out of RELEASE_EXPECTED_CONTEXTS.
> - Inventory the adopted action and nested dependencies for C3.
>
> Run the applicable gate union, including full pytest, workflow lint, inventory checks and both required independent reviewers. Prepare bounded clean/vulnerable dependency rehearsals; execute only those covered by this prompt and existing CI authority. No settings changes or check promotion.
>
> Coordinate generated inventory and overlapping contract changes before landing. Require current-base CI; do not weaken tests or widen baselines.
>
> Finish with the PR, exact tested head, verification evidence, qualification still outstanding and merge prerequisites. Do not merge or start A2.

The full message also names the documents to read first and asks that uncommitted local
drafts be preserved; those lines are omitted here.

**Boundaries as applied here.**
- Authorized: B3 within §4 B3 and §11.5; implementation, required tests, independent
  reviews, rehearsals covered by existing CI authority, commits, push and **one** ready PR.
- Delegated: unresolved in-scope technical and plan-disposition decisions, to an AI
  consulting team (§17.3). This is not an owner signature.
- Not authorized: any merge; repository settings or branch protection; C4 or any
  required-check promotion; A2 or any later packet.
- `Dependency Review` is not added to `REQUIRED_CONTEXTS` or `EXPECTED_CONTEXTS` in
  `scripts/release_gate.py`, and never to C4's future `RELEASE_EXPECTED_CONTEXTS`.
  Membership of `PR_REQUIRED_CONTEXTS` remains C4's decision (§11.5).
- This section supersedes, for B3 alone, the statements that B3 lacks execution authority
  or is not started (§0.1 note, §15.1). Historical text is retained.

### 17.2 Claim, isolation and coordination

- **Claim.** Claude Code session `hypertrophy-toolbox-v3-main-68` (Opus), 2026-10-20,
  for B3 (§7). This session alone holds the next shared CI workflow-edit slot (§0.4).
- **Base.** `origin/main` `71c4cc6d2eea1147fcd3b1defe89fabaff0fb3ac` (#531), fetched
  2026-10-20. `gh pr list --state open` returned `[]` at fetch time.
- **Isolation.** Fresh standalone clone `D:\development\Hypertrophy-Toolbox-v3-ci-b3-20261020`,
  made with `git clone --no-hardlinks` from
  `https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3.git`;
  `.git/objects/info/alternates` is absent. Branch `ci/b3-dependency-review`. Private
  `.venv` and `node_modules`; TEMP, cache, bytecode and pytest-cache paths sit under the
  clone's gitignored `artifacts/`, set by the process-only `artifacts/b3/env.ps1`. The
  shared main checkout is untouched except for its gitignored claim file. No pull, reset,
  stash or clean of shared main. The clone and branch are retained.
- **Claim handoff.** The shared checkout's gitignored
  `docs/ai_workflow/WORKSTREAM_OWNERSHIP.local.md` now holds a B3 row. The stale B2 row
  (#532 merged `1a5e0e6f`) and E1+D3 row (#533 merged `48d6a450`; repair #538 merged
  `b86e9ad7`) were moved to the released log as **handed off, not silently released**,
  with `gh pr view` merge evidence. Handoff notices went to the three live peer sessions:
  `hypertrophy-toolbox-v3-main-5a` (recovery readiness), `-53` (WS3) and `-2d` (issue
  #537 Linux baseline sync). None was the original CI coordinating lead, and none has
  pending `.github/**` edits. The stale #531 docs row remains; it is outside this
  packet's mandate.
- **WS3 inventory landing agreement.** WS3 (`-53`) also regenerates
  `docs/test_inventory/`. Agreed: whichever PR merges second rebases and regenerates the
  inventory from scratch. Generated inventory is never hand-merged.
  Later confirmation: WS3 (`hypertrophy-toolbox-v3-main-53`) agreed this rule and
  touches no `.github/**` and not `tests/test_ci_expansion_contracts.py`. Sessions `-5a`
  and `-2d` have no `.github/**` edits and need no sequencing. `-2d`'s planned PR touches
  `e2e/__screenshots__/linux/**`, `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` and possibly
  `docs/MASTER_HANDOVER.md`, with no overlap with B3.
- **Pre-existing, unchanged.** §16.10's 2026-10-26 scheduled qualification has no
  claimant. Noted for the owner; not taken up by B3.

| Role | Agent ID | Owns |
|---|---|---|
| Manager | Claude Code session `hypertrophy-toolbox-v3-main-68` (Opus), read-only | Coordination, adviser panel, delegated decisions and dispositions, local gates marked "manager" |
| `product-manager` | `a8501dd3530da91e2` | This file only |
| `automation-qa` | `a68b15d4e59c0fa6d` | The headed B3 test section, the mutation driver and the review-fix round |
| `senior-developer` | `adcbf78c370f89741` | The `ci.yml` job, the B1 inventory B3 addition and the AR3 fix |
| `code-reviewer` | `a27312dfe469a87b9` | Independent review; read-only; ran no tests (§17.5) |
| `architecture-reviewer` | `afaa3581390cd3568` | Independent review, a fresh instance and not the design adviser; read-only; ran no tests (§17.5) |

### 17.3 Delegated decisions

Three independent read-only advisers each received the same brief and ran no tests and
made no edits. The security adviser was limited to read-only `gh api` GETs.

| Lens | Agent type | Actual agent ID | Blocking | Dissent | Disposition |
|---|---|---|---|---|---|
| Architecture | `architecture-reviewer` | `a67569b0e01c8f77e` | none | The three explicit `with:` values should be mandatory, not open | Adopted (decision 2) |
| Testing | `test-strategist` | `ac33d32e838b19c24` | none, on condition that the rehearsal job is byte-identical apart from triggers and base/head refs, with the diff recorded | Arm (d), low/moderate-only, should be required, not optional; pin scorecard and license check false | Adopted (decisions 2 and 6) |
| Security / product risk | `Plan` (read-only by instruction) | `a58655a4066be0189` | `show-openssf-scorecard` must be explicitly false and contract-pinned, because a third-party outage could red a future required check | Push-based arms prove the action's policy decisions, not the PR acceptance criterion. A seeded red on a real PR, merge blocking, branch protection/bypass, license policy, GHSA exceptions, D-6 and extra PRs stay owner-only/C4 | Blocking item resolved by adoption (decision 2); the dissent is carried as outstanding qualification (decision 7, §17.6) |

**Adopted by manager session `hypertrophy-toolbox-v3-main-68` under the owner's
delegation.** The panel was unanimous on structure.

1. **Job.** `ci.yml` job id `dependency-review`, name exactly `Dependency Review`;
   `ubuntu-latest`; `timeout-minutes: 10`; job `permissions: {contents: read}`; job-level
   `if: github.event_name == 'pull_request'` (exact string). That `if:` is the single
   sanctioned skip, so a `main` push shows the job as skipped. No `needs`, `strategy`,
   `continue-on-error`, checkout or `run:`. Not in the `Run Tests` fan-in. Fork and
   Dependabot PRs run it with a read-only token; PRs to `develop` are covered by the
   existing trigger.
2. **Step.** One named step, `Review dependency changes` (the contract step parser needs
   `- name:`), using the pin and the exact `with:` map in §17.4. Banned keys:
   `config-file`, `external-repo-token`, `allow-ghsas`, `allow-licenses`,
   `deny-licenses`, `allow-dependencies-licenses`, `deny-packages`, `deny-groups`,
   `base-ref`, `head-ref`, `repo-token`, and any key not in the map.
3. **Release separation.** Not added to `REQUIRED_CONTEXTS` or `EXPECTED_CONTEXTS` in
   `scripts/release_gate.py`. A contract asserts absence from every `*CONTEXTS` constant
   there, which also covers C4's future `RELEASE_EXPECTED_CONTEXTS`.
   `scripts/release_gate.py` is not edited.
   *Refined during test authoring (manager, delegated):* `PR_*` constants are exempt,
   because §11.5 puts `Dependency Review` into C4's `PR_REQUIRED_CONTEXTS`. Absence is
   still required from `REQUIRED_CONTEXTS`, `EXPECTED_CONTEXTS` and every other
   `*CONTEXTS` constant, including a future `RELEASE_EXPECTED_CONTEXTS`.
4. **Contracts first.** A new headed B3 section of `tests/test_ci_expansion_contracts.py`,
   written by automation-qa before implementation, with a recorded mutation proof run in
   both directions.
5. **Inventory.** A B3 addition to
   [B1_ACTION_INVENTORY.md](B1_ACTION_INVENTORY.md): pin, signature, metadata blob,
   `node24` with no nested dependencies, permissions, and updated remote-`uses:` counts.
   The C3 candidate set gains `actions/dependency-review-action` as a proposal only.
6. **Rehearsals.** Four required arms on throwaway push-triggered branches (§17.6), under
   existing CI authority and the B2 precedent (§15.6).
7. **Outstanding qualification.** The items listed in §17.6 are not executed; they belong
   to the owner or C4.

Delegated approval is recorded as the AI consulting team's decision under the owner's
delegation. It is **not an owner signature** and not a formal council. The formal
implementation reviews (`code-reviewer` and `architecture-reviewer`, fresh instances)
remain required and separate (§17.5).

### 17.4 Design

**Pin, as measured by the manager session.** `actions/dependency-review-action`
**v5.0.0** = commit `a1d282b36b6f3519aa1f3fc636f609c47dddb294`.
- Newest tag and release, published 2026-05-08T20:23:50Z. Lightweight tag; no moving
  `v5` tag exists.
- GitHub signature `verified` (`valid`); `package.json` version `5.0.0`; 19 commits ahead
  of and 0 behind `v4.9.0`.
- `action.yml` blob `5f6cf73d694f70892899c2768fa9814a9218dd0d`: `runs.using: node24`,
  `main: dist/index.js`. No post step, no `runs.steps`, no nested `uses:` and no
  container, so the nested-dependency traversal terminates at this action.
- The only API used is `GET /repos/{o}/{r}/dependency-graph/compare/{base}...{head}`,
  with `repo-token` defaulting to `github.token`. `contents: read` suffices, and no
  checkout is needed without a `config-file`.
- Schema defaults at that commit (`src/schemas.ts`, as read by the security adviser):
  `license_check` true; `show_openssf_scorecard` true, which calls `api.deps.dev` and
  `api.securityscorecards.dev`, and a deps.dev failure reaches `setFailed`;
  `comment_summary_in_pr` `never`; `retry_on_snapshot_warnings` false (120 s timeout).

**Re-verification.** The senior-developer independently re-verified the pin with
read-only `gh api`: lightweight tag, the only `v5*` tag, signature verified/valid,
`action.yml` blob, `node24` `dist/index.js` only, `package.json` 5.0.0, 19 ahead / 0
behind `v4.9.0`, and all eight `with:` keys are declared inputs.

**Shipped job shape.** This is the `ci.yml` job as implemented by the senior-developer,
placed after `workflow-lint`, with a comment block (+33 lines in `ci.yml`).

```yaml
dependency-review:
  name: Dependency Review
  runs-on: ubuntu-latest
  timeout-minutes: 10
  if: github.event_name == 'pull_request'
  permissions:
    contents: read
  steps:
    - name: Review dependency changes
      uses: actions/dependency-review-action@a1d282b36b6f3519aa1f3fc636f609c47dddb294 # v5.0.0
      with:
        fail-on-severity: high
        fail-on-scopes: runtime, development, unknown
        warn-only: false
        vulnerability-check: true
        license-check: false
        show-openssf-scorecard: false
        comment-summary-in-pr: never
        retry-on-snapshot-warnings: false
```

**Rationale.**
- **Vulnerability-only at `high`.** The owner's scope is vulnerability review at
  severity `high`. Explicit values make any drift a contract failure rather than a
  silent change of upstream defaults.
- **Scorecard off.** It is an unapproved third-party egress, and its failure can red the
  check.
- **License check off.** Without allow/deny lists it gates nothing but adds traffic, and
  it would silently start blocking if lists appeared. License policy is an owner item
  (§17.6).
- **Comment summary `never`.** Job-summary output only; no comment-write permission.
- **No snapshot retry.** Snapshot warnings never fail the job, so a retry adds only
  latency. Known false-green surface: snapshot warnings go to the job summary only.
- **PR-only by job `if:`.** Existing full pip/npm audits stay on `main`. For C4: a
  skipped required check counts as success, so `pull_request_target` or `merge_group`
  triggers must never be added without revisiting this design.
- **Release separation.** PR-only `Dependency Review` is never release evidence (§11.5).

**Inventory.** [B1_ACTION_INVENTORY.md](B1_ACTION_INVENTORY.md) gains
`## B3 addition — 2026-10-20` (pin row with metadata blob, facts and counts) plus the
AR3 header pointer. Remote `uses:`, counted with
`^\s*(- )?uses: [A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@`: `ci.yml` 63 → 64; repository
94 → 95. Six repositories, one SHA each: checkout 33, setup-python 26, upload-artifact
19, setup-node 15, download-artifact 1, dependency-review-action 1.

### 17.5 Gates and reviews

**Required union.** The diff adds a `ci.yml` job, a headed test section and an inventory
addition. That requires:
- full pytest;
- `code-reviewer` and `architecture-reviewer`;
- a pyright baseline diff;
- the blocking flake8 selection on changed Python;
- inventory regeneration plus `--check`, coordinated with WS3 (§17.2);
- workflow lint: local actionlint (with pinned shellcheck) and zizmor at
  `--min-severity medium`, plus the CI `Workflow Lint (actionlint + zizmor)` job.

No product, route, template, JS or CSS change is involved, so no Chromium gate applies.
Results marked "before / after review fixes" were taken on the working tree before
implementation commit `90cde802`; results marked `90cde802` were re-measured on that
commit with a clean tree (`git status --porcelain` empty before and after the full run).
`ci.yml` is unchanged by the review fixes, so the workflow-lint rows hold for the final
head. `origin/main` was re-fetched at about 2026-10-20T18:47Z: still `71c4cc6d`, with no
other open PR.

**Tests first.** automation-qa added 11 tests in a headed B3 section of
`tests/test_ci_expansion_contracts.py`; every name contains `dependency_review`. Before
implementation: `8 failed, 3 passed, 292 deselected in 0.31s`. The three that passed on
base were (g) no job waits on it, (h) release-gate absence and (k) the trigger guard.
(a)–(f), (i) and (j) failed: no job, no pin, no reference.

**Mutation proof.** The driver was a scratch file, `tests/_b3_mutation_driver.py.tmp`.
It is gitignored by `*.tmp` and was never committed; it sat under `tests/` because the
automation-qa hook allows writes only under `tests/` and `e2e/`. It runs real pytest in a
child process against redirected temp copies of `ci.yml`, `deep-gate.yml`,
`release_gate.py` and the inventory doc. It verifies that each copy was actually read
and hashes the live files before and after.
- Run 1, on the implementation: 68/68 arms passed (64 red arms killed, 4 green controls
  held); live files unchanged (`artifacts/b3/mutation-run-1.log`).
- Run 2, after the review fixes: **73/73 arms passed (63 red arms killed, 10 green
  controls held)**; baseline 11/11 before and after; live files hash-unchanged.

| Gate | Tree | Result |
|---|---|---|
| Full pytest, local (private venv, `artifacts/b3/env.ps1`, `pytest tests/ -q --junitxml=...`) | `90cde802` | **5,580 passed, 2 skipped, 0 failed in 1,637.12 s**, exit 0. Expected: §16.10's 5,569 plus the 11 B3 tests |
| Full pytest, local | before review fixes | **Superseded; not credited.** 5,580 passed, 2 skipped, 0 failed, 1,630.31 s. The review fixes then edited only existing B3 tests |
| B3 contracts, `-k dependency_review` | after review fixes | `11 passed, 292 deselected in 0.33s` |
| 10 workflow/release contract files (senior-developer) | before review fixes | `575 passed in 64.29s` |
| `test_ci_expansion_contracts.py` + `test_release_workflow_contracts.py` (automation-qa) | after review fixes | `396 passed in 64.45s` |
| actionlint 1.7.12 + shellcheck 0.11.0, `-pyflakes=` | `90cde802` | exit 0. The senior-developer's earlier run also exited 0 with no output, using Windows release assets SHA-256-verified against the GitHub release digests |
| zizmor 1.30.1 `--min-severity medium --format plain .github/workflows` | `90cde802` | "No findings to report", offline and online, "(4 ignored, 13 suppressed)". The counts are identical on base `71c4cc6d`'s workflows, so B3 adds no ignore or suppression |
| pyright 1.1.410 + `scripts/pyright_baseline_diff.py` | `90cde802` | PASS, 0 net-new (baseline 0, current 0). The earlier run used the PyPI wrapper in the private venv after `npx pyright@1.1.410` failed on an npm registry `ECONNRESET` |
| flake8 blocking selection (`E9,F63,F7,F82,F811,E711,E712,F401`) | `90cde802` | 0 on the whole repository |
| `generate_test_inventory.py` regeneration and `--check` | before / after review fixes; `90cde802` | 3,539 → 3,550 (+11) across 133 files; `--check` up to date at `90cde802` |

The skip count (2) matches §16.10. The skipped identities were not re-captured, so this
record does not claim they are the same two as §13.1.

**Dependency-graph precondition (AR2).** Measured by the manager with read-only
`GET /repos/AvihaiShai/Hypertrophy-Toolbox-v3/dependency-graph/compare/b86e9ad7...a305e5a4`.
It returned sass 1.105.1 → 1.105.2 (`package-lock.json`, npm, scope development) and
hypothesis 6.170.0 → 6.170.1 (`requirements.txt`, pip, scope runtime). The dependency
graph is enabled and compare is reachable. The `pull_request` default-ref path is still
proved only by the PR's own run.

**Reviews.** Both reviewers were independent and read-only and ran no tests. The first
pass reviewed the pre-fix tree, diff sha256 `7e05b05c…7d1c`; the delta pass, by the same
two agents, reviewed the committed diff at `90cde802`. The manager made the dispositions
under delegation.

| Reviewer | Agent ID | Verdict | Findings and dispositions |
|---|---|---|---|
| `code-reviewer` | `a27312dfe469a87b9` | **approve with nits**, no blocking | Should-fix CR1, stale §17 "nothing implemented / pending" text: accepted, fixed in the first §17 evidence update (in `90cde802`). CR2, the `if:` inline-comment strip: applied, plus a green arm. CR3, the inventory contract should bind the metadata blob: applied, plus a red arm. CR4, composite actions under `.github/actions` not scanned: **declined**, because no `.github/actions` directory exists; recorded as a future-adoption note. CR5, a C4 comment on the REQUIRED/EXPECTED name requirement: applied by automation-qa |
| `architecture-reviewer` | `afaa3581390cd3568` | **approve with nits**, no blocking | Should-fix AR1, stale §17 text: accepted, fixed in the first §17 evidence update (in `90cde802`). Should-fix AR2, dependency-graph precondition missing from the outstanding list: accepted, measured above and listed in §17.6. AR3, B1 inventory "exactly four" standing sentence: applied by the senior-developer. AR4, release-gate test type assertion brittle for C4: applied by automation-qa. AR5, trigger-ban message should point C4 to §17.4: applied. AR6, A2 and later `ci.yml` packets: accepted, sentence in §17.6 |
| `code-reviewer`, delta | `a27312dfe469a87b9` | **approve** | Reviewed the committed diff `71c4cc6d..90cde802` (`artifacts/b3/review-diff-2.patch`, sha256 `1e60334e…6b30`). All accepted findings resolved; the CR4 decline is reasonable. D-CR1, "uncommitted tree" wording and the "not stated relative to the fixes" gate cells: accepted, fixed in this receipts update. D-CR2, rehearsal change lists also include `+ actions/dependency-review-action@a1d282b3…`, and the B3 PR's own run will too: accepted, recorded in §17.6. D-CR3, the string-typed check precedes the `PR_` skip: left as is (harmless, fails closed) |
| `architecture-reviewer`, delta | `afaa3581390cd3568` | **approve with nits** | Same committed diff. The `ci.yml` hunk is byte-identical to the first diff; every AR disposition holds; CR2/CR3/CR5 hold; the CR4 decline is accepted. It found the separation of delegated decisions, reviewer passes and owner approvals in §17 clean, the outstanding list complete, and nothing that unduly constrains C4 or A2. D-AR1, reword stale "uncommitted tree" text as of implementation commit `90cde802`: accepted, fixed in this receipts update. D-AR2, replace "not stated relative to the fixes" with the `90cde802` measurements: accepted, fixed above. D-AR3, merge prerequisites should list full pytest and delta review recorded on the final head: accepted, §17.6. D-AR4, move the function-local `from collections.abc import Mapping` to module imports: **declined**. It is style-only; automation-qa kept the import local to confine the B3 section, and changing reviewed code after both delta approvals would need another review and test cycle for no behavioural gain |

A review that did not run, or whose reviewer failed, is recorded as incomplete, never as
"no findings".

### 17.6 Rehearsals, PR and outstanding qualification

**Acceptance rehearsals.** These ran under existing CI authority and the B2 precedent, on
throwaway push-triggered branches. The branches were never merged and are retained,
because there is no deletion authority. No extra PR was opened.
- **Construction.** Each branch was built from base `71c4cc6d` with git plumbing
  (temporary index + `commit-tree`), leaving the clone's working tree untouched. The
  builder was the session scratch script `b3_rehearsals.py`. Outputs (`job-delta.diff`,
  `arms.json` and run logs) are under `artifacts/b3/rehearsal/`.
- **Workflow.** `.github/workflows/b3-rehearsal.yml` ("B3 rehearsal (throwaway)"), on
  push to `rehearsal/b3-*`, with `permissions: contents: read`.
- **Recorded job delta against the `ci.yml` job.** It removes only
  `if: github.event_name == 'pull_request'` and adds only
  `base-ref: 71c4cc6d2eea1147fcd3b1defe89fabaff0fb3ac` and `head-ref: ${{ github.sha }}`.
- **Nothing seeded runs.** There is no checkout and no install, so no seeded package was
  ever installed or executed.

| Arm | Branch @ head | Seed | Run (push, attempt 1) | Window (UTC, 2026-10-20) | Result |
|---|---|---|---|---|---|
| (a) clean | `rehearsal/b3-a-clean-v1` @ `93cdd7c5` | `requirements.txt` `requests==2.33.0` (no advisories) | [`39474857728`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39474857728), job `118808063686` | 18:27:14Z → 18:27:26Z | **success**. Change `+ requests@2.33.0`; "did not detect any vulnerable packages with severity level "high" or higher" |
| (b) runtime red | `rehearsal/b3-b-runtime-red-v1` @ `6d55ea8f` | `requirements.txt` `PyYAML==5.3.1` | [`39474859322`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39474859322), job `118808069523` | 18:27:15Z → 18:27:25Z | **failure**. `requirements.txt » PyYAML@5.3.1`, critical GHSA-8q59-q68h-6hv4; "##[error]Dependency review detected vulnerable packages." |
| (c) development red | `rehearsal/b3-c-dev-red-v1` @ `76987feb` | npm devDependency lodash 4.17.20 (`package.json` + `package-lock.json` `dev: true`) | [`39474857709`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39474857709), job `118808063783` | 18:27:14Z → 18:27:24Z | **failure**. `package-lock.json » lodash@4.17.20`, high GHSA-35jh-r3h4-6jhm and high GHSA-r5fr-rjxr-66jc |
| (d) moderate-only green | `rehearsal/b3-d-moderate-green-v1` @ `ad1ac991` | `requirements.txt` `requests==2.31.0` (GHSA-9wx4-h78v-vm56, GHSA-9hjg-9r4m-mvj7, GHSA-gc5v-m9x4-r6x2, all medium) | [`39474857803`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39474857803), job `118808064093` | 18:27:14Z → 18:27:22Z | **success**. Change `+ requests@2.31.0`; below the `high` threshold |

Every run printed the effective configuration: fail-on-severity `high`; fail-on-scopes
`runtime, development, unknown`; vulnerability-check true; license-check false;
show-openssf-scorecard false.

Each arm's detected change list also contains
`+ actions/dependency-review-action@a1d282b3…`, because every rehearsal commit adds the
workflow file that uses it (D-CR2). PR #539's own run will likewise list the action as a
detected change.

**Security adviser's dissent stands.** These push arms prove the action's policy
decisions on the shipped inputs. They do not prove the `pull_request` event path,
blocking of a PR check, or branch protection, so they do not by themselves satisfy §4
B3's PR acceptance criterion.

**PR.** Pushed `ci/b3-dependency-review` and opened ready PR
[#539](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/539), verified `OPEN`
with `isDraft: false` at about 2026-10-20T19:16Z. Its head at opening was `90cde802`.
- **PR CI.** The run on `90cde802` was in progress when this was recorded. It is
  **pending and is recorded in the PR closeout**. This receipts commit starts a new run,
  which supersedes it as the current-head carrier. A run that is incomplete or cancelled
  is not credited.
- **Name and clean-change observation.** The B3 PR's own run supplies the in-PR
  observation of the name `Dependency Review`. It counts as a clean dependency-change PR
  only if its job summary shows a detected dependency change. As D-CR2 notes, the
  detected changes will include the action itself.

**Outstanding qualification (not executed; owner or C4).**
- A seeded red that visibly blocks a real PR check.
- Merge-blocking readback.
- Branch protection and bypass.
- An observed skipped state on a real `main` push after merge.
- Fork and Dependabot PR observations.
- The `pull_request` default-ref path beyond the B3 PR's own run.
- License policy.
- Any GHSA exception.
- D-6 unchanged.
- The repository's dependency-graph setting staying enabled (AR2).

**Merge prerequisites.**
- Full pytest recorded on the final head: **satisfied** at `90cde802` (5,580 / 2 / 0,
  §17.5).
- Delta review recorded: **satisfied** at `90cde802` (§17.5).
- Current-base CI green on the final head, with `Dependency Review` observed by exact
  name: **pending**.
- The WS3/B3 inventory rule (§17.2): whichever merges second rebases onto `main` and
  regenerates the inventory from scratch, never hand-merging.
- An explicit owner merge message naming #539 (§0.10).

A2 and later `ci.yml` packets start from post-B3 `origin/main`, regenerate the inventory
and re-count remote `uses:` (95) (AR6). Promotion still needs C4 activation and its
blocking proof, which this authorization excludes.

**Coordination follow-ups (routing only; B3 does not act on them).**
- **WS3 and `QUALITY_GATE.md`.** WS3 (`-53`) will edit only the Route/API gate cell of
  `docs/ai_workflow/QUALITY_GATE.md`. B3 does not edit that file, so there is no overlap.
- **Stale `ci.yml` comment after WS3.** WS3 deletes the `app_client` fixture in
  `tests/test_pattern_coverage.py`. `.github/workflows/ci.yml` (around lines 919–924)
  cites that fixture to justify omitting `--cov=app`, so the comment goes stale once WS3
  merges. This is outside B3's scope. Route it to the next `ci.yml` slot after WS3 merges
  (A2 or later), or to WS3 if it edits `ci.yml` after B3.
- **Unclaimed qualification.** §16.10's 2026-10-26 scheduled qualification still has no
  claimant. This is an owner follow-up and is unchanged.

### 17.7 Merge receipt and post-merge observation

Recorded by Claude Code session `hypertrophy-toolbox-v3-main-4e` under §18's authority.
Session `-68` confirmed that its authority stopped at the ready PR and that it had no
pending edits.

- **Merge.** #539 merged 2026-10-20T20:07:19Z by AvihaiShai as squash
  `1f5ae0f059f6cb4a994f92b6e03c57d689fd060c` from head `b7a6fecf`. That head's PR run
  [`39484164996`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39484164996)
  (`pull_request`, attempt 1) concluded success with 27/27 jobs successful.
- **First `main` push.** Run
  [`39489279999`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39489279999)
  (`push`, head `1f5ae0f0`, 20:07:22Z → 20:19:23Z) concluded success. Its job list shows
  `Dependency Review` as **completed / skipped** and every other job as success. This
  discharges §17.6's "observed skipped state on a real `main` push after merge". The
  other §17.6 qualification items are unchanged.

## 18. B2 residuals — execution, 2026-10-20

### 18.1 Authority

Owner instruction to Claude Code session `hypertrophy-toolbox-v3-main-4e`, 2026-10-20,
verbatim:

> keep working onWorkflow-lint leftovers with the ai consulting team until it get done

**Boundaries as applied here.**
- **Scope.** The §15.5 residuals: the reusable-build pip cache, the three Dependabot
  cooldown findings and the stale Dependabot comment. It also covers the zizmor
  online/offline question that §15.5 left to the owner before C4.
- **Delegated.** In-scope technical and plan-disposition decisions, to an AI consulting
  team (§18.3), following the §17.1 pattern. This is not an owner signature.
- **Authorized.** Implementation, required tests, independent reviews, commits, push and
  one ready PR.
- **Not authorized.** Any merge, which needs an explicit owner message naming the PR
  (§0.10). Also excluded: settings, C4 or any promotion, A2/A3, release publication, and
  any change to D-6.
- **Departure from §12.4.** Both §12.4 file tables limit `release.yml` and
  `_packaged-windows.yml` to "pins/permissions/contract preservation only in core".
  Removing the reusable build's `cache:` is neither of those, and it changes all three
  callers' install step. That limit is deliberately widened for this PR only, under the
  delegation above. Caller and child names, the smoke, install and migration steps,
  and the no-`inputs:` design are unchanged.
- **Not in scope.** `docs/OPEN_WORK_EXECUTION_PLAN.md` §0.4's "Workflow-lint residuals"
  row. The docs-slices session (`-c5`) owns that file and was told about this PR.

### 18.2 Claim, isolation and coordination

- **Claim.** The gitignored `docs/ai_workflow/WORKSTREAM_OWNERSHIP.local.md` holds the
  claim for the shared `ci.yml` slot, `_packaged-windows.yml`, `release.yml` (comment
  only), `dependabot.yml`, the B2 test section, inventory drift and this section.
- **B3 row handed off.** The B3 row was moved to the released log as handed off, not
  silently released. Its evidence is #539 merged as `1f5ae0f0`, and session `-68`
  confirmed it had no pending edits.
- **Notices.** Live peers `-23`, `-70`, `-c5`, `-cb` and `-68` were told about this
  work. None edits `.github/**` or these tests.
- **Inventory rule with `-70` (U1-FOLLOWUP-1).** Whichever PR merges second rebases and
  regenerates the inventory from scratch.
- **Base.** `origin/main` `1f5ae0f059f6cb4a994f92b6e03c57d689fd060c`. `gh pr list
  --state open` returned none.
- **Isolation.** No worktree or clone was created. The candidate tree is a `git archive`
  export in the shared checkout's gitignored `artifacts/b2-leftovers/tree`, indexed with
  `read-tree` so `git ls-files` tests are real. The commit was built with a temporary
  index and `commit-tree`. The shared working tree, index and HEAD are untouched.
- **Linters.** These are the B3 clone's verified local copies, used read-only: actionlint
  1.7.12, zizmor 1.30.1 and shellcheck.

### 18.3 Delegated decisions

Three independent read-only advisers received one brief with the same two residuals.
They ran no tests and made no edits. Both the architecture and the testing adviser read
the shared checkout's stale working tree instead of `origin/main`. Their B2-contract
statements were marked as inferred and were re-checked against `origin/main` by the
manager before adoption.

| Lens | Agent type | Actual agent ID | Blocking | Dissent |
|---|---|---|---|---|
| Architecture | `architecture-reviewer` | `a25abea4397d97c42` | none | Widen the zizmor scan, as a separate commit |
| Testing | `test-strategist` | `a32c0e2f4bd93f237` | none | Defer widening to a separate PR; cooldown is owner-reserved |
| Security / product risk | `Plan` (read-only by instruction) | `a2fd2bc67f77c955c` | none | 14-day majors for pip/npm; a conservative reading reserves any `dependabot.yml` edit to the owner |

**Adopted by session `hypertrophy-toolbox-v3-main-4e` under the owner's delegation.**

1. **R1, reusable-build cache: remove it (unanimous).** `_packaged-windows.yml` loses
   `cache: 'pip'` for all three callers.
   - **Why not a context-derived `cache:` keyed on `github.ref_type`.** It is the
     per-caller knob that file rules out. A dispatch rehearsal would also stop matching
     a real tag run.
   - **Exposure.** A tag run restores caches any `main`-ref job could have written.
     `requirements*.txt` pin with `==` but not `--require-hashes`, and the cached wheels
     feed the PyInstaller build.
   - **Impact today.** Nothing is exported or published, so the worst case is a falsely
     green release gate. The impact grows with F1.
   - **Cost.** Uncached pip installs on the PR, weekly and release builds; the advisers
     estimate tens of seconds. This is measured after merge, not here.
2. **R1 contract.** `test_release_setup_steps_restore_no_cache` now follows release.yml's
   local `uses: ./` call graph transitively. It also asserts that `_packaged-windows.yml`
   is reached, so the rule does not depend on a hand-kept file list. `release.yml`'s
   narrowed comment is restored to "the whole tag path is cache-free".
3. **R2, cooldown: adopt it (unanimous on adoption).** All three ecosystems get
   `cooldown: default-days: 7`, uniformly.
   - **The value.** 7 is zizmor 1.30.1's threshold, verified locally: the finding reads
     "insufficient implicit default-days (less than 7)".
   - **Security's 14-day majors were not adopted.** Two of three advisers preferred the
     smaller surface, and majors already arrive as separate PRs. The dissent is recorded.
   - **Authority, majority view (architecture dissenting).** B2's "D-6-adjacent, route to
     owner" overstated the overlap. Cooldown delays version-update PRs only. Security
     updates stay OFF, alerts are unaffected, and every lockfile change remains a reviewed
     PR. The owner can veto, and the visible effect is that routine Dependabot PRs arrive
     about a week later.
4. **R2 enforcement: widen the zizmor input (2 of 3; testing dissents).** The argv
   becomes `... .github/workflows .github/dependabot.yml`.
   - **Why the file is named explicitly.** Naming it, rather than scanning `.`, keeps the
     input set fixed.
   - **Why widen at all.** Without it, the finding regresses silently.
   - **The dissent.** Testing wanted widening deferred because it re-pins an exact-argv
     contract. It is answered by landing it with the cooldown and re-proving the argv
     contract by mutation in this PR.
   - **No separate rehearsal.** zizmor accepting the file path is proven locally, both
     offline and online. The PR's own `Workflow Lint` run is the first GitHub
     observation.
5. **Cooldown contract.** A new `test_every_dependabot_ecosystem_waits_out_the_cooldown`
   requires every `package-ecosystem` entry to carry exactly `cooldown: {default-days: 7}`.
6. **Stale `dependabot.yml:109` comment: already resolved.** On `1f5ae0f0` it names
   `deep-gate-visual.yml`'s weekly `visual-linux` job, which #533 (E1) corrected. No edit
   is needed.
7. **zizmor online/offline: unchanged.** §16.8's consulting-team decision stands: keep it
   online while the check is non-required, and leave the required arrangement to C4. No
   new decision is taken.
8. **Deferred to F1 (security adviser).** Make `--require-hashes` a precondition of any
   CI-built distributable. It is outside this scope and changes no file here.

Delegated approval is recorded as the AI consulting team's decision under the owner's
delegation. It is **not an owner signature** and not a formal council. The
implementation reviews (§18.5) remain required and separate.

### 18.4 Change set

| File | Change |
|---|---|
| `.github/workflows/_packaged-windows.yml` | Removes `cache: 'pip'`, with a comment giving the reason |
| `.github/workflows/release.yml` | Comment only: the tag path is cache-free |
| `.github/dependabot.yml` | `cooldown: default-days: 7` on pip, npm and github-actions, plus a header paragraph |
| `.github/workflows/ci.yml` | `workflow-lint` zizmor argv gains `.github/dependabot.yml`, plus one comment line |
| `tests/test_ci_expansion_contracts.py` | Call-graph cache rule, the new cooldown test, and the re-pinned zizmor argv |
| `docs/test_inventory/**` | Regenerated for the one added test |

No action is adopted, no pin moves and no permission changes. The B1 inventory and the
C3 candidate set are unchanged. Nothing enters `REQUIRED_CONTEXTS` or
`EXPECTED_CONTEXTS`.

### 18.5 Gates and reviews

**Union.** This change touches several kinds of file:
- a workflow, and a lint-job argv;
- a Dependabot config;
- a Python contract test;
- the generated inventory;
- documentation.

Its gates are therefore full pytest, local workflow lint, a mutation proof of the
changed contracts, the inventory check, flake8's blocking selection, a pyright check on
the changed file, and both independent reviewers. Every local run used the candidate
export in `artifacts/b2-leftovers/tree`, with the shared `.venv` and linters taken
read-only from the B3 clone.

| Gate | Tree | Result |
|---|---|---|
| Full pytest, local Windows | `41be88db` | **5,578 passed, 5 skipped, 0 failed**, 1618.6 s. Skips: 3 × `test_braces_override_contracts.py` (export has no `node_modules`), the executable-bit check (Windows) and one pre-existing app-fixture skip |
| Full pytest, local Windows | pre-review draft | 5,573 passed, 5 skipped, 5 failed. All 5 failures said "Not a valid object name HEAD": the export had an index but no commit. With HEAD set to the draft commit, the two files (`test_css_theme_dark_p3_audit_contracts.py`, `test_css_wp4_4_a_baseline_contracts.py`) passed 77/77. Recorded as a harness artifact, not a product failure |
| `test_ci_expansion_contracts.py` + `test_release_workflow_contracts.py` | final | 397 passed |
| Mutation driver (scratch, not committed) | final | 10/10 mutants red, 2/2 controls green, files restored byte-identical (arms below) |
| actionlint 1.7.12 + shellcheck, `-pyflakes=` | final | clean |
| zizmor 1.30.1 `--min-severity medium .github/workflows .github/dependabot.yml` | final | "No findings" offline and online (4 ignored, 13 suppressed; same as `1f5ae0f0` over `.github/workflows`). One earlier online attempt hit a transient connection reset and was rerun |
| zizmor, seeded: `1f5ae0f0`'s `dependabot.yml` | base | 3 × `dependabot-cooldown`, exit 13 |
| pyright 1.1.410 on `tests/test_ci_expansion_contracts.py` | final | 0 errors |
| flake8 blocking selection on the changed test file | final | 0 |
| `generate_test_inventory.py --check` | final | up to date: 3,551 collected (B3's 3,550 + 1) |

**Mutation arms.**
- **Red, cache rule:**
  - M1: `cache: 'pip'` restored in `_packaged-windows.yml`.
  - M2: an `actions/cache` step added there.
  - M3: `cache: 'pip'` restored in a `release.yml` smoke.
- **Red, cooldown rule:**
  - M4: npm cooldown removed.
  - M5: npm cooldown set to 3 days.
  - M6: npm `semver-major-days` added.
  - M7: a fourth ecosystem with no cooldown.
  - M7b: the github-actions ecosystem deleted.
- **Red, argv rule:**
  - M8: zizmor drops `dependabot.yml`.
  - M9: zizmor scans `.` instead.
- **Green controls:**
  - The unmutated tree. `ci.yml` keeps 13 `cache: 'pip'` steps, so this also shows the rule does not leak past the tag path.
  - `cache: 'pip'` added to `deep-gate.yml`, which is outside the tag path.

**Reviews.** Each reviewer was a fresh Claude Code subagent, independent of the
implementation and of the §18.3 advisers. Both read the tree and diff and ran nothing.

| Reviewer | Verdict | Findings and disposition |
|---|---|---|
| `code-reviewer` | **approve with nits** | N1, the call-graph regex missed `- uses: ./`: widened. N2, a per-file `assert setups` would red a future setup-free child: now required only for `release.yml` and `_packaged-windows.yml`. N3, the ecosystem count was unpinned: the set is now pinned to pip/npm/github-actions, with mutation M7b. S4, the B3 §7 cells contradicted §17.7: superseded in place. N5, "ready PR" wording before the PR exists: the PR is opened from this head and §18.6 records it. N6, comment wording on enforcement: tightened |
| `architecture-reviewer` | **approve with nits** | M1, §12.4's "pins/permissions only" rows were not reconciled: §18.1 now records the deliberate, PR-scoped departure. M2, §15.3 still routed cooldown to the owner: dated disposition added. L3–L5 and both nits: accepted as recorded; the ecosystem count is now pinned (as N3) |

A review that did not run, or whose reviewer failed, is recorded as incomplete, never
as "no findings". Both reviews completed.

**Delta reviews.** Both reviewers were resumed on the review-fix delta, from the
reviewed draft `a3a2e330` (never pushed) to `41be88db`. Both read the delta and ran
nothing.
- `code-reviewer`: **approve**. All six findings are resolved and the delta adds no
  defect. One nit: the quoted ecosystem pin would false-red, with an opaque message,
  if an ecosystem were unquoted.
- `architecture-reviewer`: **approve**. Its findings are resolved and the delta adds no
  defect. Its nit was that §18.6 did not exist yet; this section adds it.

### 18.6 PR, publication and outstanding qualification

**Publication.**
- Implementation commit `41be88dbb678d1a9ab735726ea4acfc87fffbd17`, parent `1f5ae0f0`,
  was built with a temporary index and `commit-tree`.
- `ci/b2-residuals` was pushed to `origin`. `git ls-remote` showed no existing branch of
  that name, and `origin/main` was still `1f5ae0f0` at push time.
- Draft PR [#546](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/546) was
  opened from that head. This receipts commit adds this section and the PR number, and
  the PR is then marked ready.
- The receipts commit supersedes the implementation head as the CI carrier. A run that
  is incomplete or cancelled is not credited.

**PR CI.** Pending when this was written; it is recorded in the PR closeout. This PR's
`Workflow Lint (actionlint + zizmor)` run is the first GitHub observation of the
widened zizmor input. A green run there is the acceptance evidence for decision 4. No
throwaway rehearsal was run, because zizmor accepting the file path is already proven
locally, offline and online (§18.5).

**Outstanding (not executed).**
- The first `main` push run after merge, including its lint job.
- A timing comparison for the uncached packaged build. Compare `Packaged Smoke (Windows
  bootloader, non-required) / Build and smoke` on that run against the cached runs
  before it. Measure it after merge, not here.
- C4 promotion of `Workflow Lint` and the online/offline arrangement (§16.8), both
  unchanged.
- `--require-hashes` as an F1 precondition, routed by §18.3 decision 8.
- `docs/OPEN_WORK_EXECUTION_PLAN.md` §0.4's "Workflow-lint residuals" row can point
  here after merge. That edit belongs to the docs-slices lane or the owner.

**Merge prerequisites.**
- Full pytest on the final head: **satisfied** at `41be88db`. The receipts commit changes
  only this file.
- Both reviews and both delta reviews: **satisfied** (§18.5).
- Current-base CI green on the final head: **pending**.
- Inventory rule with `-70`: whichever merges second rebases and regenerates.
- An explicit owner merge message naming #546 (§0.10).

### 18.7 Brought up to post-A2 `main` — 2026-10-21

A2 (#540) merged as `43f5df33` while #546 was open, and #546 became `CONFLICTING`, so
GitHub ran no CI on it. On the owner's 2026-10-21 request (review log), `43f5df33` was
merged into `ci/b2-residuals` as an ordinary merge commit. The guard blocks force push,
and a merge keeps #546 and its review history in place.

**Conflict.** Only this file conflicted: the header status row, and the slot after §17.6,
where `main` had added §19 and #546 had added §17.7 and §18. The status row now
carries both lanes, and the sections run in number order: §17.7, §18, §19. The header
Branch / PR row and the §7 A2 row now name #540's merge. §19's text is unchanged; its
"draft #540" receipts are dated and are superseded by the A2 row.

**A2 behavior.** `ci.yml` merged without conflict. Against `43f5df33`, the merged tree
changes only #546's two `workflow-lint` hunks (a two-line comment edit and the zizmor
argv).
A2's `worktree-windows` invocation, with `-n 4 --dist load` and its three modules, is
byte-identical to `main`, and `tests/test_worktree_ci_contracts.py` is `main`'s file.
A2 changed no test identity, so the inventory stays at 3,551.

| Gate | Tree | Result |
|---|---|---|
| Full pytest, local Windows, candidate export with HEAD set | merge tree `ebd3216f` | **5,578 passed, 5 skipped, 0 failed**, 1799.8 s. Same five skips as §18.5 |
| actionlint 1.7.12 + shellcheck, `-pyflakes=` | `ebd3216f` | clean |
| zizmor 1.30.1 `--min-severity medium .github/workflows .github/dependabot.yml` | `ebd3216f` | "No findings" offline and online (4 ignored, 13 suppressed) |
| `generate_test_inventory.py --check` | `ebd3216f` | up to date: 3,551 |

The commit differs from `ebd3216f` only in this file: the review nits below and this
table. No test reads this file.

**Review.** QUALITY_GATE's CI-workflow row requires `code-reviewer`; no job is added or
removed, so `architecture-reviewer` is not required. A fresh read-only `code-reviewer`
subagent reviewed the merge delta from #546's head, the candidate against `main`, and
this file, and ran nothing. Verdict: **approve with nits**, with no blocking finding. It
confirmed A2's invocation and test file equal `main`'s and that #546's change set is
intact. Applied: the review-log row moved to the end, this section's comment wording,
and the §7 A3 row now queues A3 after #546. Not applied: restoring B3's and A2's figures
to the status row, since §7, §17 and §19 still carry them.

**Merge prerequisites now.**
- Full pytest on the merged tree: see the table.
- Current-base CI green on the final head: recorded on the PR, since this commit cannot
  name its own run.
- An explicit owner merge message naming #546 (§0.10).

A3 starts from the `main` that #546 produces, under the same one-workflow-PR rule.

## 19. CI core after B3 — A2 execution, 2026-10-20

### 19.1 Authority and serial scope

Owner request, verbatim:

> keep working on **CI/CD core after B3:** A2 → A3 → G6 → G7, with B4 as an optional measurement slot. **with the ai consulting team until it get done**

This authorizes the named approved core implementation sequence and consulting work.
The existing one-workflow-PR-at-a-time rule and explicit named-PR merge boundary
in §0.10 continue to apply. B4 is optional and does not delay the named sequence.
No repository setting, check promotion, credential, release or delivery action is
part of this packet. The earlier core council remains sufficient; it is not rerun.

B3 #539 was independently read back as MERGED at `2026-10-20T20:07:19Z`, merge
`1f5ae0f059f6cb4a994f92b6e03c57d689fd060c`, with all 27 PR checks successful on
head `b7a6fecf516add32a96f7dd9980695289a7400b2` (run `39484164996`). This
updates the historical pending receipt in §17; it does not promote Dependency Review.

### 19.2 A2 implementation and decisions

The candidate `worktree-windows` invocation adds `-n 4 --dist load`, retaining
all three module arguments, both PowerShell hosts, xunit2 JUnit, explicit pytest
exit handling, unconditional no-skip verification, artifact name and protected
context names. No Operation A held test module or helper is edited.

The initial `loadfile` approach passed every identity/outcome check but did not
show a repeatable performance gain: native rehearsal job **651 s**, actual PR
job **701 s**, versus serial **677 s**. Its two-sample mean is 676 s. Neither
sample is represented as proof of a causal speed improvement. Lifecycle alone
accounts for 508.4 of baseline testcase seconds; file scheduling leaves that
dominant module together and increased its runtime in both samples.

The AI test adviser `/root/ci_test_adviser` and independent code reviewer
`/root/a2_code_reviewer` directly audited all three modules and their helper:
no selected test requests a module/session fixture; synthetic repositories,
runtime roots and annotations are per-test `tmp_path`, child environments are
copied, and monkeypatches are local to each worker process. The primary adopts
one bounded exception to `requirements.txt`'s general `loadfile` comment:
**only these three audited modules use test-level scheduling**. The full-suite
module-fixture rule stays unchanged. The existing workflow contract now rejects
extra `.py` arguments as well as pinning the exact distribution option. Adding
another module requires a new safety assessment, not automatic extension of
this exception. No dependency or retry policy changes.

The adviser's baseline-equivalence concern is also adopted: the existing
verifier checks both-host symmetry but deduplicates cases and cannot establish
equivalence to a previous run. Acceptance compares complete `(classname, name)`
identity Counters and executed outcomes from downloaded baseline/candidate
reports, rejecting omissions, additions, duplicates and nonpassed outcomes.
All three module blobs were verified identical between baseline PR head and
candidate base. Host symmetry alone is insufficient.

Implementation uses a standalone clone of current `origin/main`, with private
Python/npm dependencies and isolated runtime/temp roots. The original dirty
checkout and retained development/rehearsal branches are preserved.

### 19.3 Baseline, gates and evidence

| Evidence | State |
|---|---|
| Baseline | B3 PR run `39484164996` (attempt 1), Operation A Windows job `118840137591`, head `b7a6fecf`; same three Operation A modules are byte-identical to A2 base `1f5ae0f0` |
| Baseline executed report | `operation-a-windows-junit`: 251 cases, 0 skipped/failures/errors, suite 589.869 s; job `19:31:22Z`–`19:42:39Z` = 677 s; native test step `19:32:41Z`–`19:42:33Z` = 592 s |
| Targeted workflow contracts | 12 passed |
| Pyright baseline diff | pyright 1.1.410, 0 current diagnostics / 0 net-new |
| Independent code review | `/root/a2_code_reviewer`, initial and scheduling delta reviews completed independently with no findings; delta review supersedes initial approval; final execution gates still required; native test-scheduling rehearsal subsequently passed all 251 identities |
| Full pytest | Initial Windows run: 5,571 passed / 2 skipped / 9 failed in 1,049.79 s. Failures were setup-specific: six selected WSL `bash.exe` instead of Git Bash; one lacked historical Git objects in the shallow clone; two conflicted with explicit runtime/default-path setup. After correcting only the private test environment and fetching history, all 159 cases in the four affected modules passed. Initial candidate CI `39490332424` on `0cc6ec49` passed all 27 jobs, including core + all four guard shards; final-scheduler CI is still required. |
| Initial file-scheduled native evidence | Rehearsal `39490106461`, SHA `877ac8d2`, job `118860700944`: 251 passed, exact baseline Counter, suite 561.791 s / step 564 s / job 651 s. PR run `39490332424`, head `0cc6ec49`, job `118861501297`: same 251 passed, suite 613.081 s / step 616 s / job 701 s. Both have 0 omissions/additions/duplicates/skips/failures/errors; no repeatable speed gain. |
| Test-scheduled native candidate | Retained branch `rehearsal/a2-test-load-20261020`, SHA `6367191ae1cfbd19c419d88f73d333e97c78a569`, run `39492310219`; the test invocation matches the final candidate, with push trigger/job census narrowed for this unmerged rehearsal; 251 passed, 0 skipped/failures/errors and exact baseline identity Counter; suite 349.758 s / test step 352 s / job 439 s, job `118868376133`. Job saving 238 s (35.2%), test-step saving 240 s (40.5%); runner time 7.32 min vs 11.28 min. One sample; the revised-head PR run supplies the repeat before adoption. |
| Ready PR / owner merge | Draft [#540](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/540); requires final scheduler evidence and explicit named-PR merge authority |

Generated reports and local consult records stay under ignored `artifacts/`.
Editing assertions/comments in an existing test changes no collected node
identity/count, so inventory regeneration is unnecessary unless a later change
trips a canonical drift surface. A2 is independent of Operation A promotion.


### 19.4 Receipt boundary and remaining serial work

The table above is the receipt written with the revised scheduler. The final
implementation commit cannot name its own SHA or its future CI run. The
[#540 checks](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/540/checks)
and PR description carry that later exact-head result and repeat measurement;
no pending check is represented here as passed. A ready state requires that
fresh-head evidence. A2 merges only after explicit owner authority naming #540;
A3 then starts from the newly merged `origin/main`, followed by G6 and G7 under
the same serial rule. A later packet may reconcile this dated receipt without
rerunning completed reviews or inventing a self-referential commit identity.


## 20. A3 execution — 2026-10-21 local

### 20.1 Authority, base and coordination

Owner request, verbatim:

> Merge PR #540 (head 30c88a2e), then continue A3 from merged main.

The earlier owner request authorizes A2 → A3 → G6 → G7 with the AI consulting
team; B4 remains optional. #540 was verified open, clean and still at the named
head, with all 27 final CI jobs successful. It merged as
`43f5df3357e0c8d9a1e7e3c050eb57ad1af5b538` at `2026-10-20T21:56:44Z`
(2026-10-21 local). A3 starts from that fetched merged main; the dirty original
checkout, all retained branches/worktrees and private runtime remain intact.

B2 residual PR [#546](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/546)
is already open against separate `ci.yml`/plan hunks. A3 prepares and rehearses
without opening a competing workflow PR. Rebase and refresh the affected gates
after that slot closes; preserve its cache/lint changes. This grants no authority
to merge, close or alter #546. A3 and later merges still take §0.10's owner gate.

### 20.2 Implementation and adopted technical decisions

- The fixed matrix changes from two to four members; every invocation, matrix
  check label and artifact denominator agrees at four. The protected
  `E2E Functional (Chromium)` aggregate keeps its exact name, body, `always()`
  condition and empty permissions.
- The 25 functional specs, one worker per runner, CI retries=2, isolated
  server/database setup and ADR-006's local N=1 launcher stay unchanged.
- Every shard uploads only its small JUnit report on success or failure, using
  the already adopted SHA-pinned upload action, unique per-shard names and
  failure on missing output. Full HTML/trace artifacts retain failure-only
  upload. There are no new permissions, dependencies or action adoptions.
- Required workflow contracts pin four distinct members, no include/exclude or
  softened job/test/report step, the exact spec command, report presence and
  the existing protected fan-in. Removing any one member fails its contract.
  The actual Bash fan-in body is executed for success, failure, cancellation,
  skip, empty/missing and unknown uppercase results; only success returns zero.

The fan-in sees one matrix aggregate, not four independently enumerated API
records. Membership is therefore a required source contract, while downloaded
report unions prove the actual executed partitions. This preserves the existing
API-free gate rather than adding an untested per-leg reducer. GitHub documents
[job conditions before matrix expansion](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idif)
and the [dependency result context](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#needs-context).
The live seeded failure below proves the real platform's matrix-to-gate path.

### 20.3 Reviews and local gates

| Gate | Receipt |
|---|---|
| Independent code review | `/root/a2_code_reviewer` resumed for the staged A3 diff, completed: no findings; no execution evidence inferred |
| Independent architecture review | `/root/ci_test_adviser` applied `.claude/agents/architecture-reviewer.md` in a distinct completed diff review: no findings; earlier advisory work receives no gate credit |
| Targeted union | 472 passed across CI expansion, shard launcher, Playwright runner and release workflow contracts |
| New coverage | 23 cases: fixed membership/removal/softening mutations plus the actual aggregate shell's result handling; all 23 rerun passed after removal of a redundant shadowed helper import |
| Inventory | Generator-owned regeneration; 3,573 deterministic pytest nodes / 133 files, 540 required functional Playwright cases / 25 specs; other surfaces unchanged |
| Full pytest | 5,603 passed / 2 skipped in 1,191.85 s; `-n 4 --dist loadfile`, Git Bash selected, full historical objects and a private runtime. The two skips are the existing fixtureless legacy happy-path test and the Unix executable-bit check on Windows; no failed/error cases |
| Python baseline | pyright 1.1.410: 0 current diagnostics / 0 net-new against the unchanged baseline |
| Final inventory check | `scripts/generate_test_inventory.py --check`: up to date |

### 20.4 Native evidence — no future result is claimed

All rehearsals are retained unmerged branches. Green baseline/candidate runs
copy the canonical frontend, functional shard and aggregate job bodies, with a
narrow push trigger and lightweight reports. Their app/test/dependency corpus
is the same merged-main base. The deliberately red control-flow harness copies
the production fan-in and real four-child matrix, using an explicit fourth-child
failure; it is not represented as successful browser execution.

| Rehearsal | SHA / run | Observed receipt |
|---|---|---|
| Same-corpus two-shard baseline | `b950d582f8a3d73bf80175d44a283f8a67b801e7`; [39505028713](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39505028713) | All 4 jobs successful; reports contain 279 + 261 = 540 passing identities across 25 specs |
| Four-shard candidate | `a72ef314ae574c23502f00050b314bba54001b81`; [39505374537](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39505374537) | All 6 jobs successful; reports contain 143 + 136 + 126 + 135 = 540 passing identities, exactly the baseline Counter |
| Seeded fourth-child failure | `a95885946e6e691eb3e1c188ff0546f235de2135`; `39505374066` | Shards 1/2/3 success, shard 4 failure, exact protected aggregate failure; expected red, separate from equivalence |

The report comparison requires exactly two baseline and four candidate artifact
paths. It checks readable nonempty XML, declared counts, project/file/full-title
identity Counters, every required spec, no duplicate/missing/unexpected identity,
and zero skipped/failure/error outcomes. Timings include job/queue-to-gate and
runner-minutes; estimates are not substituted for observations.

Both positive rehearsal commits have parent `43f5df33`; their only differing
file is `ci.yml`. The project/file/full-title identity digest is
`d7076599e7cde16dba9d17831ff819f67eb944fe0b78032288f9e6cec9ee66ed`.
Every identity executes once, with no skips, failures, errors, omissions,
additions or duplicates. Downloaded artifact inventories, reports, raw run/job
API receipts and strict comparison/timing scripts are retained under ignored
`artifacts/ci-a3/`. `/root/ci_test_adviser` independently cross-checked these
receipts, the comparator's rejection paths and the seeded native failure; no
evidence gap remains in that bounded comparison.
Seven executed probes against private report copies also rejected missing or
extra shard directories, malformed XML, a skipped case, a duplicate identity,
a changed identity and an omitted case with corrected declared counts.

| Observed measure | Two shards | Four shards |
|---|---:|---:|
| Workflow creation → required aggregate completion | 499 s | 367 s |
| Frontend queue | 3 s | 3 s |
| Longest shard job including setup | 470 s | 335 s |
| Shard test-step walls | 424 / 349 s | 230 / 281 / 226 / 247 s |
| Shard wait after frontend completion | 3 / 3 s | 4 / 3 / 3 / 3 s |
| Sum of frontend, shard and aggregate execution | 879 s | 1,225 s |
| Runner-job minutes, unrounded | 14.650 | 20.417 |

This pair saves 132 s (26.5%) to the protected aggregate while adding 346 s
(5.767 runner-job minutes). It measures one isolated A3 path, including setup,
queue and fan-in, not full-pipeline latency, repeatability or rounded billing.
It authorizes no spending. The final PR's exact-head full CI is still required.

**Evidence limit:** Playwright 1.61.0 JUnit reports final testcase outcomes and
combined attempt duration with the current reporter settings. This packet can
prove final executed identity/outcome equivalence while preserving retries=2;
it does not claim zero retries or reconstruct recovered attempts. G7 remains
the attempt-preserving reporter packet.

### 20.5 Serial handoff and receipt boundary

The A3 source is qualified locally and through the retained native rehearsals.
The current PR slot is still #546; its lane's local coordination record shows
an active post-A2 rebase. This packet preserves that lane and waits to open its
own PR. After #546 closes, fetch current main, preserve its changes on rebase,
refresh affected gates/reviews and run final-head PR CI before claiming ready.
No future PR, commit identity or check result is invented in this receipt.

G6 and G7 have read-only technical preparation from the consulting team,
retained in ignored `artifacts/ci-a3/next-packet-preparation.json`; neither
implementation nor reviewer credit is inferred. G6 starts after A3 merges;
G7 follows G6. B4 remains optional and unstarted. All new merges retain §0.10's
separate named-PR owner authority; settings, promotions, releases and cleanup
remain outside this execution.

### 20.6 Retained A3 resumed on current main — 2026-10-21

The owner's CI implementation-lane request resumes existing branch
`ci/a3-functional-four-shards` at
`398b0564da076442e2e467cfe646538d39423cc8`; it does not rebuild A3. This is
the sole workflow-editing lane among the five parallel sessions. The manager
coordinates the existing owner's handoff separately and preserves every retained
checkout, recovery artifact and rehearsal branch. G6 starts only after A3 merges
with explicit named-PR authority; G7 starts only after G6 merges. WS5 workflow
integration waits until after G7.

**Current-main integration.** PR
[#546](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/546) was
independently read back as merged at `2026-10-21T12:40:52Z`, merge
`28484ddaf7c85da1fa485eaa31c784f17f851d8f`. The resumed branch merges fetched
`origin/main` `d98f45d34de8356f7ac2becb7a7c4b3bef48f8e3` (#545), retaining
the recorded A3 source commit and remote branch history. This supersedes the
queued-behind-#546 state in §§20.1 and 20.5. The merge preserves B2's widened
lint input, cooldown and packaged-cache removal, as well as WS3's application
factory/runtime separation and #548's owner-approved Linux visual work. No
application or visual-baseline change is introduced by A3.

`ci.yml` and contract tests merge without conflict. The planning conflicts are
bounded to live status, review-log and ledger rows; both lanes' historical
receipts remain. The conflicting generated inventory is taken from current main
as an intermediate tree and must be regenerated by its canonical generator from
the actual merged candidate, with private dependencies installed. It is not
hand-merged or represented as final before that run.

**Isolation.** Implementation uses the manager-owned standalone clone
`D:/development/Hypertrophy-Toolbox-v3-ci-core-20261021`, with independent Git
object storage and private Python/npm dependencies, database, runtime, caches
and temporary paths. It writes no tracked source in the dirty shared checkout
or retained `D:/development/Hypertrophy-Toolbox-v3-ci-a2-20261020` clone. New
coordination and evidence live under ignored
`artifacts/parallel-next-five/ci-core/`; original A3 evidence remains retained
in its original location.

**Qualification boundary.** §§20.3–20.4 describe the original tested source and
same-corpus rehearsals. Their 132 s aggregate saving and additional 346 s runner
execution are historical observations, not a current-main benchmark or proof
of repeatability. WS3 changes the app/test corpus, so current-candidate full
pytest, regenerated inventory, pyright baseline diff, required independent code
and architecture reviews, and final-head PR CI are pending. Fresh functional
reports must establish actual candidate execution without claiming the old
same-corpus comparison covers the new runtime. Protected check names, selected
functional specs, failure propagation and retries=2 stay unchanged.

**Bounded follow-ups.** Q4's standalone JS Unit rename is coordinated with the
qualification lane and remains its own change before any protection change.
WS3 GA-14's stale coverage comment is queued for a separate bounded comment
change in this sole workflow lane; it is not folded into A3. No settings,
promotion, merge, release, spending or artifact removal is authorized here.

### 20.7 Exact-head A3 completion and named merge — 2026-10-21

The owner explicitly approved only PR #549 at
`f069bed180e425bd1dbdf3967a19b246b3d5271e`. Fresh pre-merge readback found that
exact head, OPEN/ready/MERGEABLE and all 30 check runs successful: the 29 CI
workflow jobs plus the independent Dependabot configuration check. Squash merge
completed at `2026-10-21T17:38:23Z` as
`dee3c379b8435e1ba0941884b9f264675f8012b7`, independently read back and fetched.
No branch or artifact was removed. The connector returned 403; authenticated
GitHub CLI performed the authorized merge with `--match-head-commit`.

Final PR run [39613142357](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39613142357),
attempt 1, passed 29/29 jobs. Independent four-report parsing proves exactly 540
passing project/file/full-title identities across 25 specs, equal to the retained
baseline Counter. Native approved full-pytest route: 4,458 passed / 211 existing
skips / zero failures or errors; native Operation A Windows: 251/251 passed.
Local full Windows: 5,678 passed / two existing skips / three setup failures in
1,069.75 s. After creating the private runtime/data directory and shortening
private TEMP (Git object writes exceeded MAX_PATH), complete affected config and
lifecycle modules passed 166/166 in 389.73 s, including all three original
failures. Source stayed unchanged. These counts overlap; this is not a clean
all-green local full rerun. Independent evidence assessment accepted the native
full gate plus the transparent local correction.

Fresh independent `/root/code_reviewer` and `/root/architecture_reviewer` reviews
passed with no findings at the exact tested head/tree. Inventory regeneration and
`--check` passed; pyright 1.1.410 reported zero current/net-new diagnostics.
Actual full-PR wall was 485 s, functional aggregate 423 s, longest shard 385 s and
summed frontend/shards/aggregate runner-job time 20.317 min. This is a fresh
scheduling observation, not a controlled performance pair; the longest shard
exceeds the old six-minute estimate. The historical 499→367 s pair and its
additional runner time remain dated. JUnit final outcomes do not prove recovered
retries. Raw reports, reviews and local setup diagnoses are retained under
`artifacts/parallel-next-five/ci-core/`, mirrored to the shared checkout.

The first merged-main push run is
[39645582155](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39645582155),
on `dee3c379`; pending at the initial G6 claim. It is not reported green in advance.

## 21. G6 — required destinations for nine existing cases

### 21.1 Authority, isolation and boundaries

Owner instruction, verbatim:

> Approved: merge PR #549 at f069bed1, then continue to G6. Do not merge anything else without a separate explicit approval naming the PR.

This follows the approved core Plan v2/TS-2 acceptance, not a new council or a
promotion authorization. Implementation starts from merged main `dee3c379` in
the retained independent clone `D:/development/Hypertrophy-Toolbox-v3-ci-core-20261021`,
branch `ci/g6-enforced-selected-tests`, with private .venv/node_modules, runtime,
database, caches and short temporary paths. The dirty shared checkout and all
retained A3/recovery refs and artifacts remain untouched. Only this lane edits
workflows. G6 ends at a ready PR; its merge requires a separately named approval.
G7 begins only after that authorized G6 merge and its own separate approval. WS5 workflow integration waits for
G7 and its own execution assignment.

Parent manager owns this planning record; `/root/implementer` owns bounded source
and acceptance tests; `/root/evidence_analyst` owns evidence analysis. Fresh code
and architecture reviewers remain independent of implementation and each other.
Use no more than four concurrent agents. A reviewer that has not completed is
pending, never credited as a pass.

### 21.2 Approved implementation and evidence

Add only `workflow-contracts-windows`, a narrow Windows job for the six fixed
`powershell` identities, to existing `Run Tests` needs and its all-success fan-in
arguments. Keep the guard legs and their cross-shard proof; never include the
entire unqualified Operation A job. Install from existing `requirements.txt`.
In existing `pytest-core`, add `npm ci` before pytest so the three installed-braces
identities execute. A stdlib-only selected-report helper reuses existing pytest
identity conventions, compares fixed exact identities and rejects missing,
unexpected, duplicated, skipped, failed/error and absent/malformed reports.
Collection may select complete approved function families but may not redefine
the fixed allowlist from whatever remains. Verify reports after failed test
steps too; preserve the original test verdict and all existing retry policies.
Preflight both required host/dependency prerequisites. Reports and exact node IDs
must come from the actual candidate corpus, not from documentation alone.

`tests/test_ci_expansion_contracts.py` covers actual report decisions, removal,
skip, prerequisite and failure controls, plus failure/cancellation/skip/missing
of every required dependency. Existing workflow/caller/job census contracts must
adopt the narrow job without weakening protected-name or exclusion assertions.
Fresh full pytest, pyright baseline diff, generator-owned inventory and its drift
check, independent code/architecture reviews, final-head PR CI and representative
native prerequisite/selected-failure rehearsals are required. Native bounded
route harnesses may shorten only unrelated work, and must disclose that scope;
they prove required-route propagation, not activated branch-protection behavior.
No prerequisites, cases, production code, dependency pins or retry policies are
changed to make the nine identities pass.

G6 also resolves WS3 **GA-14** with an explicitly bounded comment-only correction
above the same core coverage command: pytest now imports the production factory;
the deleted pattern-coverage fixture reference is removed. Keep
`--cov=utils --cov=routes`, report outputs and D1's non-blocking policy unchanged.
No app.py coverage expansion is implied.

At this pre-implementation record, implementation, generated inventory, required
checks, current-candidate native outcomes and independent reviews are pending.
Final receipt numbers are recorded only after the tests/reviews actually run.

### 21.3 Reviewed handoffs and serial ownership

Qualification lane supplied a reviewed Q4 specification/candidate plus its
independent reconciliation review. Q4 was approved by the owner in #547; D2's
recorded ledger prerequisite is met on main through #544 (cycle rows 26–75,
50 / 0 / 0 / 0 / 0 exact JS jobs), independently rechecked by that lane. This
reconciles live "unsigned" cells only; dated council/decision blocks remain
verbatim. #550 records the follow-up documentation receipt and is a different
ready PR, not authorized for merge here. Q4's rename remains a standalone change
before any protection update; C4 remains unapproved. The prospective §11.5
target-set name will be reconciled with the standalone rename, not by this G6
workflow change. The latest owner instruction continues G6 now; qualification
imposes no timing constraint, so Q4 stays queued for a coordinated separate slot.
Do not copy the qualification lane's JS ledger rows into this PR.

Reviewed WS5 readiness handoff is received with conditions, not execution
authority. Keep G6's new helper stdlib-only and install the existing manifest;
do not pre-split requirements, add test-tool pins, touch security-audit or change
the fan-in CLI on WS5's behalf. WS5 re-censuses after G7; its open readiness
decisions and execution assignment remain with that lane/owner. No WS5 work is
implemented by G6. Both handoffs and their review records are retained beside
CI evidence; no handoff grants merge, settings, release or cleanup authority.

### 21.4 Current-main refresh after U1 #551 — 2026-10-21

Owner instruction, verbatim:

> Not approved yet. #551 merged to main at 18:45Z, after #552's CI. Per your own PR body, integrate current main (`a12b680f`) into #552, regenerate the inventory from the actual tree, rerun CI on the new head, then re-ask with the new exact SHA. G7 needs its own approval after the merge.

PR #551 merged at `2026-10-21T18:45:23Z` as
`a12b680fba9503b8578d777ed51dff571f7c44f2`. The integration preserves the
previous G6 head `df91daec8330f4ea80a8878535a24f88cc05d34b` in
`retain/g6-df91-before-u1` and merges that fetched current main through an
ordinary two-parent merge. No squash, rebase, held test edits, dependency
reinstallation or workflow-policy change is part of this refresh. Both U1 and
G6 source are preserved. The generated inventory is regenerated by the actual
combined-tree collector even where Git's text merge reported no conflict.

At this dated integration receipt, bounded G6/Vitest inventory contracts, JS
coverage, final inventory check, full current-candidate pytest, fresh independent
reviews and new-head CI are pending. The PR closeout and ignored evidence carry
the exact resulting commit and tree after they exist. Earlier positive/native
negative receipts remain retained and dated; they are not relabeled as new-head
CI. If held G6 enforcement bytes remain identical, the representative native
negative rehearsals need no repeat. Any changed enforcement byte must be
reported and its affected evidence refreshed.

New integration evidence belongs under
`artifacts/parallel-next-five/ci-core/g6/refresh-20261021/`; previous evidence,
rehearsal refs, the dirty shared checkout and recovery artifacts remain retained.
No PR merge, settings activation or G7 execution is authorized by this integration.
After fresh new-head CI is complete, re-ask for #552 with that exact SHA.
G7 requires its own separate approval after G6 merges and is not started here.

## 22. G7 — attempt-preserving retry report, 2026-10-22

### 22.1 Authority, isolation and boundaries

Owner instruction (lane O1 of the 2026-10-22 owner commission), verbatim:

> **Authority.** I approve G7 execution under the approved core Plan v2. This is the separate
> approval that CI PLANNING §21.4 requires after G6 (#552, merged as `155181d6`). It runs to a
> ready PR; the merge is mine.

G6 #552 merged 2026-10-21T20:19:20Z as `155181d67a89fe72e86c75a1ff438caec250a9bd` (head
`2e480330`). This lane writes `scripts/ci_retry_report.py`, `tests/test_ci_retry_report.py` with
its fixtures in `tests/fixtures/ci_retry_report/`, the CI-only JSON reporter line in
`playwright.config.ts`, the `ci.yml` summary wiring, the §7 G7 row and this section.
`requirements*.txt`, the `security-audit` job and `scripts/ci_fan_in.py` stay with WS5 (§21.3);
no pytest reruns are introduced. Workflow slot order is S1 Q4 rename → O1 G7 → S3 WS5: G7 is
pushed only after Q4 merges or S1 releases the slot, then rebased and re-gated.

Implementation ran in the standalone clone `D:\development\Hypertrophy-Toolbox-v3-ci-g7-20261022`
(branch `ci/g7-retry-report` from `origin/main` `155181d6`) with private dependencies, Chromium,
runtime/DB, caches and a 64-character TEMP; no app launch used port 5000. Evidence is under its
ignored `artifacts/ci-g7/`. `automation-qa` wrote the acceptance tests first (`2a55ffe`, before
any implementation existed), `senior-developer` implemented against them, and `code-reviewer`,
`test-strategist` (diff stage) and `unslop-reviewer` reviewed cold and independently.

### 22.2 Selected reporter formats (pinned)

- **Playwright: built-in JSON reporter, `@playwright/test` 1.61.0** (`package.json`; the pip
  `playwright==1.61.0` pin is in lockstep). The JUnit reporter cannot serve G7. With the repo's
  settings it emits one `<testcase>` per test with the final outcome and summed duration, so
  recovered attempts disappear (§20.4's evidence limit). Its `includeRetries` option
  (`PLAYWRIGHT_JUNIT_INCLUDE_RETRIES`) adds `flakyFailure`/`flakyError` (recovered test) or
  `rerunFailure`/`rerunError` (failed test) children only for attempts that neither passed nor
  were skipped: earlier passed or skipped attempts (serial-group re-runs) are dropped and no entry
  carries its retry number, so it was not adopted. The JSON reporter keeps every attempt's retry
  number, status and duration, plus the shard and each project's retry policy.
  `SUPPORTED_PLAYWRIGHT_VERSIONS = ("1.61.0",)`; a test asserts it contains the `package.json`
  version, so a Playwright bump fails pytest until the format is re-verified, and any other
  `config.version` is reported `unavailable (unsupported-reporter)`.
- **pytest: no reporter selected.** pytest 9.1.1 `xunit2` carries no attempt metadata, and no
  rerun plugin is installed or configured, so "already-configured pytest rerun output" is none.
  A tripwire test fails if a rerun plugin enters `requirements*.txt` or a workflow
  `pip install`, if pytest config sets rerun keys, or if a workflow pytest command line or
  `PYTEST_ADDOPTS` passes `--reruns`, `--only-rerun`, `-o reruns=…`, `-p rerunfailures` or
  similar; introducing reruns therefore forces G7 to be revisited.

Format facts come from `node_modules/playwright/lib/runner/index.js` (`JSONReporter`) and
`lib/common/index.js` (`computeTestCaseOutcome`), confirmed on real captures: each result carries
a 0-based `retry` and its own `status`; there is no overall run status; `stats` counts per-test
outcomes, **not** retries — serial groups re-run tests that already passed (`[passed, passed]`
→ `expected`), never-started tests in an interrupted run have `results: []` and count as
`skipped`, and interruptions appear only in top-level `errors[]`.

**Fixture provenance.** The eight files in `tests/fixtures/ci_retry_report/` are real Playwright
1.61.0 JSON reports from browser-free synthetic specs, run with `retries: 2`, `workers: 1`; only
machine paths were rewritten (`/capture`, `/repo`). `mixed.json` holds the single-run classes
(pass, fail→pass, timeout→pass, always fail, expected failure, unexpected pass, skip, nested
equal titles, a recovering and an exhausting serial group); `clean.json` is first-attempt only;
`small-shard-1-of-2.json`/`small-shard-2-of-2.json` are a 2-way shard pair; `small-projects.json`
has two projects; `max-failures.json`, `global-timeout.json` and `load-error.json` are
interrupted or failed runs. The specs, config, runner and sanitizer are retained under the
clone's ignored `artifacts/ci-g7/capture/`; a Playwright bump re-captures with them before the
pin is widened.

### 22.3 Implementation

`scripts/ci_retry_report.py` (stdlib only) classifies every test in one job's JSON report from
its own attempts: `first-attempt`; `recovered` (final attempt met its expected status after an
earlier attempt that was neither that status nor skipped); `rerun` (re-run without such an
attempt, e.g. a serial group); `exhausted` (final attempt missed its expected status after all
`retries + 1` attempts were used); `failed` (stopped before exhaustion); `skipped`; `did-not-run`; `interrupted`. Every
attempt's retry number, status and duration is kept. A missing, malformed, unpinned (§22.2),
partial (top-level errors, interruption, never-started tests, no tests) or inconsistent (stats or
per-test status disagreeing with the attempts, a shard other than the job's, or a step outcome
that contradicts the report) report is `unavailable` with its reason. The summary then says
"Retry totals are unavailable; this is not a report of zero retries.", shows no counts table,
and still lists observed attempts when the report was readable (partial or inconsistent). The
markdown names the original test-step outcome (reported, never changed), the reporter version,
each project's retry policy, the workflow run attempt and shard, a counts table, and one row per
test with more than one attempt or a classification other than `first-attempt` or `skipped`.
Retries and unavailability each raise one `::warning` annotation. Every report outcome exits 0;
an internal error renders `unavailable (reporter-error)`; a summary-file write failure falls back
to stdout.

`playwright.config.ts` adds `['json', { outputFile: <artifacts>/playwright/results.json }]` to
the existing CI-only `ciReporters` beside junit (decision in §22.5); local reporters and
`retries: process.env.CI ? 2 : 0` are unchanged.

`ci.yml`, in six job definitions (nine runs with the four functional shards) — `e2e-smoke`,
`e2e-functional-shard`, `e2e-backup`, `e2e-fatigue-context`, `e2e-erase-flow`, `visual-windows`:
the Playwright step gets `id: playwright` (never `continue-on-error`); the three
`--reporter=line` jobs request `--reporter=line,json` with
`PLAYWRIGHT_JSON_OUTPUT_FILE: artifacts/playwright/results.json`, the others get JSON from the
config reporters; a following `Summarize Playwright retries` step (`if: always()`,
`continue-on-error: true`) passes `steps.playwright.outcome`, the workflow run attempt and, for
shards, the expected shard through `env:`. Job names, `needs`, fan-ins, permissions, required
contexts and retry policy are unchanged. `deep-gate*.yml`, which load the config under
`CI=true`, only gain an extra `results.json` in their existing `artifacts/playwright` output.

### 22.4 Gates, reviews and bite proof

SHAs below are pre-rebase; post-rebase receipts go in §22.5.

| Gate | Result |
|---|---|
| Acceptance tests (`tests/test_ci_retry_report.py`) | 228 passed at `ce111f2` |
| Two-direction bite proof | 35/35 at `ce111f2`, every TS-3 class: each deliberate break turned the suite red and restoring it turned it green. Breaks were applied to a separate `--no-local` copy and restored with `git checkout --` (`artifacts/ci-g7/bite/results-ce111f2.json`) |
| ci.yml-parsing and related contract suites (12 files) | 701 passed, no existing pin changed (`b529008`; the later commits touch no workflow logic) |
| Full pytest (serial, `/verify-suite` step 1) | **6,039 passed / 2 skipped, exit 0 at `ce111f2`** in 1,601 s (`artifacts/ci-g7/verify/full-pytest-ce111f2.log`); the skips are `test_package_asset_staging.py:267` (no executable bit on Windows) and `test_priority7_error_handling.py:339` (deliberate) |
| pyright 1.1.410 + baseline diff | 0 errors, 0 net-new (measured at `ee44eed`, whose code is `ce111f2`'s) |
| flake8, both ci.yml invocations | 0 blocking repo-wide; 0 informational findings in the two changed Python files (measured at `09a1f3b`, code identical to `ce111f2`; `artifacts/ci-g7/verify/flake8-inventory-09a1f3b.log`) |
| `tsc --noEmit`; actionlint 1.7.12 + shellcheck v0.11.0; zizmor 1.30.1 offline | exit 0; clean and identical to the pre-change baselines (`b529008`/`222e29e`; the later commits change no workflow syntax) |
| Inventory | regenerated by the generator for the new file (228 cases); `--check` reports no drift at `09a1f3b` (same log) |
| `/verify-suite` E2E (command verbatim, `PW_PORT=5082`) | **not green:** 593 passed / 76 failed / 17 did not run at `b529008`, under concurrent CPU load. Re-running the eight affected spec files alone at `ce111f2`: head config 115 passed / 69 failed, base (`155181d6`) config 116 passed / 68 failed, 17 did not run each. Every functional failure from the loaded run passed on both sides; the rest are visual, thumbnail and desktop-contract specs this command runs without `PW_VISUAL_SEED` (QUALITY_GATE's documented condition) and `visual-field-separator` volume-splitter desktop/tablet dark, red on both sides on this host. The three tests whose outcome differed between head and base passed twice on head. The config differs only inside its CI-gated branch, which local runs never take |

**Root-config substitute.** The `/verify-suite` E2E command passes `--reporter=line`, which
replaces the config reporters, and `ciReporters` exists only under `CI`, so the local suite never
exercises the config change. Substitute runs on port 5081 with `CI=1`: (1) smoke with the config
reporters wrote both `junit.xml` and `results.json`, summary `no retries`; (2) the exact
`--reporter=line,json` + `PLAYWRIGHT_JSON_OUTPUT_FILE` invocation wrote `results.json` there, and
its summary showed a real local retry that the console reported only as `1 flaky`, with no
attempt statuses — the smoke spec's "navigate back to home via brand link", `recovered`
(`#0 failed → #1 passed`); (3) a temporary fail-once spec
(never committed) through the real config and web server gave `recovered` under `retries=2`. The
six summary-step bodies were also executed under bash and pwsh with GitHub-style env.

**Reviews** (verdicts as reported to the lane; the reports are retained under
`artifacts/ci-g7/review/`). Cold `code-reviewer` on `b529008`: no BLOCKING. The changes that
matter later: a skip-expected test whose attempts ran is no longer counted as `skipped`; its
optional `!cancelled()` suggestion was declined by the lane (a job hitting `timeout-minutes` is
cancelled, and `!cancelled()` would skip the summary exactly then). `test-strategist` (diff stage): one BLOCKING gate-evidence
finding (the root-config limit above); per-case malformed-detail pinning was declined (it would
pin wording; the precedence tests and the bite proof cover the branches). `unslop-reviewer`: no
BLOCKING; the rerun tripwire is kept because TS-3 requires it. Delta `code-reviewer` on
`222e29e`: no BLOCKING; its three items are fixed in `ce111f2`.

A fresh cold `test-strategist` re-reviewed the BLOCKING finding at `ce111f2`: **cleared with
conditions.** Substitute items (1) and (3) are resolved. Item (2), the script against real
reports, was resolved with a condition, since met: `ce111f2` renders the three real reports
identically to the `b529008` outputs (`artifacts/ci-g7/substitute/ce111f2/`). Item (4), PR CI, is pending. The local E2E
evidence was judged adequate, with no pre-merge action on the 76 local failures. Conditions for
the PR: its body states that local `/verify-suite` never exercises the CI reporters and that the
`CI=1` runs stand in; the `ce111f2` full pytest is recorded (done, above); and PR CI is recorded for all six
job definitions — run URL, head SHA, each `Summarize Playwright retries` conclusion, each
rendered `### Retry report` block (including the first live shard legs and the Windows pwsh
step) and the unchanged Playwright step conclusion. A missing summary or a changed Playwright
conclusion reopens the finding.

### 22.5 Decisions and pending receipts

Lane decisions (no consulting-team delegation was needed):
1. The JSON reporter line in `playwright.config.ts`. The alternative, CLI `--reporter` plus
   output-path env in `ci.yml`, duplicates the config and contradicts the functional-shard
   step's documented "no --reporter" contract. The line sits outside the named deliverable
   files: **owner confirmation requested.**
2. All six Playwright job definitions are covered, not only the functional shards, because every
   one runs with `retries: 2`.
3. `if: always()` on the summary steps, as above.

### 22.6 Rebase, PR and CI receipts — 2026-10-22

S1's #554 merged at 2026-10-22T10:13:05Z as `73de866e` (after #550 as `61da31cb`), releasing
workflow slot 1; no other open PR touched `.github/workflows/**`. G7 rebased onto `73de866e`
without conflicts. Its own bytes — script, tests, fixtures, config and `ci.yml` hunks — are
identical to `ce111f2`, so the bite proof applies unchanged; the pre-rebase head is retained
locally as `retain/g7-c0e971a-pre-rebase`. The regenerated inventory matched git's merge. On the
rebased head `9a13efe`: 929 G7 and contract tests passed; full pytest 6,039 passed / 2 skipped,
exit 0; pyright 0 net-new; flake8, `tsc`, inventory `--check`, actionlint + shellcheck and
zizmor clean (`artifacts/ci-g7/verify/rebase-73de866/`, `verify/full-pytest-9a13efe-rebased.log`).

PR [#557](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/557), CI run
[39762263460](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39762263460)
(`pull_request`, attempt 1, head `9a13efe`): success, 30/30 jobs. In all nine Playwright runs the
Playwright step and the `Summarize Playwright retries` step succeeded, and each job summary
rendered a `Retry report` block with status `no retries`, original outcome `success`,
`Playwright JSON 1.61.0`, `chromium retries=2` and run attempt 1. First-attempt counts: Visual
Regression (Windows, pwsh) 66; Smoke 11; functional shards 1/4–4/4 143 / 136 / 126 / 135, each
with its own shard and summing to the 540-test required set; Backup 33; Fatigue Context 6; Erase
Flow 2 (`artifacts/ci-g7/prci/`). This discharges the re-review's PR-CI condition; no Playwright
step conclusion changed. The commit recording these receipts is verified by the PR's final-head
CI, reported in the PR.

Remaining owner actions: decision 1 above and the merge of #557.


### 22.7 G7 final-head, owner exception and merge receipt — 2026-10-22

This completion receipt supersedes §22.5's reporter-confirmation request and
§22.6's remaining merge action, preserving their dated pre-merge evidence.
The owner approved #557 at exact final head
`4473c913cbb060602981e73696e682f31d81a9f3` and accepted its recorded local
/verify-suite E2E failures on full pytest **6,095 passed / 2 skipped**, exact-head
[PR CI 39774255096](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39774255096)
**30/30**, and CI=1 reporter substitutes. The CI-only JSON reporter was accepted.
The exception is for that one PR/head only: local E2E remains failed evidence,
and no WS5/C4 waiver is inherited. The verbatim owner exception and raw merge
receipts are retained in the G7 merge lane's `artifacts/merge-557/OWNER_EXCEPTION.md`
and `CLOSEOUT.md`; this record creates no new approval.

GitHub confirms merge `b77cb742f3af5222d9d80b608d497390c4b3e4f2` at
`2026-10-22T12:59:55Z`. Exact merged-main
[run 39783010460](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39783010460),
attempt 1, succeeded: **29 successful jobs plus the expected PR-only Dependency
Review skip**, 30 jobs total; completed `2026-10-22T13:14:33Z`.
All nine retry-summary steps succeeded on final PR head and merged main.
Main jobs: visual `119838831138`; smoke `119839053624`; backup `119839053549`;
fatigue `119839053522`; erase `119839053941`; functional `119839053469`,
`119839053701`, `119839053811`, `119839053872`. These step conclusions are not
a fresh claim that every rendered summary contains zero retries.

G7 followed Q4's approved #554 merge and successful renamed-main JS check
(`39761432262` / `119766292139`, §7). Slots 1 and 2 are released; S3/WS5
retains slot 3 under its existing authority. No settings, qualification row/T0,
later PR merge, broader exception or competing workflow publication is authorized
by this receipt. G6's selected-identity and exact-main completion receipts are
recorded in its §7 row; its dated §21 implementation history remains untouched.
