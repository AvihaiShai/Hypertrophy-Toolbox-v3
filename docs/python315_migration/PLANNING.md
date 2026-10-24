# Plan Review — Python 3.15 migration (#564)

## Section 0 — Requirements Brief

**Status:** Gate 0 approved on 2026-10-23; **Gate 1 approved with conditions on 2026-10-24**. Approved implementation, focused QA, preparation/type/inventory and corrected full pytest are complete. **Local full Chromium remains failed**, with failed/partial controls preserved; the owner approved proceeding to required independent reviews under added pre-merge conditions. Latest evidence/remaining boundaries are recorded below. Reviewed plans and earlier snapshots remain historical. Gate 2, first push, Sandbox and merge remain pending.

**Raw request** (verbatim)
> [https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/564](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/564)
> I want you to handle this issue end to end using multiple agents until it get done.

**Requirements source:** [Issue #564](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/564), fetched through the connected GitHub tool on 2026-10-23; open, with no comments at inspection. Its checklist defines delivery obligations, not completed work.

**Problem**
The project currently specifies Python 3.14.6. The requested coordinated migration must establish that one verified, exact Python 3.15 patch supports development, tests, analysis, existing CI platforms, and the Windows executable while preserving saved data and application behavior. A changed version pin alone does not establish that outcome.

**Verified repository facts**
- In this checkout, `.python-version` is `3.14.6`, `utils/python_version.py` declares `MIN_PYTHON = (3, 14, 6)`, and `pyrightconfig.json` targets `3.14` on Windows.
- `requirements.txt` currently pins Python Playwright `1.61.0`; `requirements-build.txt` pins PyInstaller `6.22.3` (the issue's `6.22.2` snapshot is stale). These declarations do not prove project compatibility.
- The inspected CI, release, deep-gate, and reusable Windows-packaging workflows select Python through `.python-version`. Their current runners include Ubuntu and Windows; exact runner and dependency coverage must be inventoried for the plan.
- `docs/DECISIONS.md` ADR-003 records the 3.14.6 choice. Historical records must remain intact when a dated decision supersedes that choice.
- The owning manager reports the isolated checkout was initially created with the older script at `85e23725`, safely switched to fetched `origin/main` `498e3b34`, then fast-forwarded without conflicts to latest measured **`ae5ec18c3293df302393b28195d8e12ceb92d176`** (#563), branch `wt/python315-564-current-20261023`. Original references and main-checkout changes were retained. Path: `D:\development\Hypertrophy-Toolbox-v3-main-python315-564-20261023`. Current guides/configuration were reread after the first switch; applicable guidance and dependency drift must be checked against the final measured baseline before Gate 1. The issue's starting snapshot is not the implementation baseline.
- Current `PARALLEL_WORKFLOW.md` requires lifecycle/baseline review and target-bound launch setup. The initial older-creator setup has now received **target-local isolation/lifecycle repair**, evidenced in `artifacts/worktree/isolation-repair.RESULT.json`: configuration probe PASS, target row ANNOTATED/ACTIVE and `blocked: false`, database absent, unrelated records/prose and baseline hash unchanged. Its next review is 2026-11-22, with retention until separate owner approval. This is not a successful precreation/global audit: shared audit remains red with **165 unrelated errors**, reduced only by repairing this target's missing row (166 before).
- Before Gate 1, the owning manager must refresh current `main`, dependency declarations, and applicable operating guides again, and reconcile any drift from the measured `ae5ec18c` baseline. Target-local repair does not grant global reconciliation, baseline changes, or PREVENTION_COMPLETE.
- The manager's read-only host probe found `WindowsSandbox.exe` absent and the current session not elevated. Sandbox availability is not established; D2 would require separately scheduled owner enablement/admin/reboot work before that executable proof can run.
- The owning manager's parallel upstream investigation reports official [Python 3.15.1](https://www.python.org/downloads/release/python-3151/) availability (2026-10-21) and preliminary [PyInstaller 6.22.3](https://pypi.org/project/pyinstaller/6.22.3/) support. These upstream signals do not prove fresh project installation, the full dependency graph, platform support, or an actual executable build.
- `QUALITY_GATE.md` classifies this cross-cutting migration as requiring Gate 0 and Gate 1. Gate 0 is now recorded below; Gate 1 is pending.

**Acceptance criteria**
1. Given the candidate Python **3.15.1**, when official release artifacts, porting notes, and compatibility are investigated, then the plan records one verified stable CPython patch, standard Windows x64 architecture, exact supported CI platforms, and evidence for that selection. An unavailable candidate or incompatible required tool is recorded as a blocker; no prerelease, floating `3.15` pin, or older-runtime fallback is silently substituted.
2. Given the approved patch, when the version contract is inspected and exercised, then the canonical pin, minimum-version helper, source and frozen startup, batch launch/build paths, tests, analyzer language target, and CI/release/deep-gate packaging agree. The exact floor and newer supported versions pass; older patches/minors fail with actionable stale-environment guidance. No machine-specific interpreter path is committed.
3. Given fresh independent `.venv` and launcher/build `venv` environments in the isolated checkout, when committed dependencies and all CI-only/developer tools are installed under 3.15, then installation and `python -m pip check` pass on supported platforms, resolved versions and relevant Windows/Linux binary artifacts are recorded, and interpreter identity, base prefix, launcher selection, and editor selection are verified. Direct/transitive runtime, test, build, lint, audit, and type tools are included; successful installation of only the runtime requirements is insufficient.
4. Given dependency or analyzer incompatibilities, when they are resolved, then each changed pin has evidence and a minimal compatibility reason; Python/npm Playwright remain aligned. PyInstaller and its resolved hooks must support the interpreter and pass the actual project build. An unresolved blocker leaves this migration incomplete and the working 3.14 setup available.
5. Given a retained 3.14 virtual environment and a fresh approved 3.15 environment, when launch/build preflight and source startup run, then 3.14 is rejected with recovery instructions and 3.15 starts successfully. The owner's existing main-checkout environments, unrelated changes, and rollback interpreter remain preserved before post-merge coordination.
6. Given an isolated fresh runtime and a representative copied older database, when initialization and core plan/log/analyze/progress/distribute/profile workflows run under 3.15, then both runtimes remain usable and saved user data and expected results are preserved without an intentional schema, API-contract, or calculation change. Experiments never use the owner's live database.
7. Given non-ASCII names and Windows paths, when applicable CSV import/export, JSON, backup/restore, and Excel export flows run, then text and data round-trip correctly under Python 3.15's UTF-8 behavior. Backup creation, restore, persistence, startup backup, and old-data compatibility have recorded evidence; demonstrated regressions receive focused coverage.
8. Given the implementation revision, when the repository's full pytest and full Chromium E2E gates and relevant workflow, security/audit, lint, backup/restore, and old-DB checks run, then required checks pass with reproducible evidence. Failures, skips, and inherited issues are reported accurately; uncertain origins are compared against an isolated base revision. Assertions, snapshots, allowlists, and gates are not weakened to obtain green.
9. Given the same revision, when type analysis and inventory checks run, then `tsc --noEmit` and the blocking pyright baseline diff pass without unexplained new diagnostics, and test inventory has no drift. Inventory is regenerated only for real covered identity/count/configuration changes; baseline changes follow owner-approval rules rather than hiding regressions.
10. Given a fresh 3.15 build environment and the committed `Hypertrophy-Toolbox.spec`, when the Windows distribution is built and tested, then the actual executable bootloader passes packaged-smoke tooling with isolated runtime data and a dedicated port. Bundled templates/static/seed assets, runtime paths, persistence, backup/restore, and representative exports work. Payload-only startup is insufficient, and executable startup on clean Windows without installed system Python is separately evidenced.
11. Given CI/release/deep-gate integration, when PR checks and approved non-publishing smoke runs execute for the implementation revision, then required CI and the Windows packaged build pass and applicable paths are exercised while existing job/check names, branch-protection contexts, triggers, and reusable-workflow callers remain intact. No release publication is part of this task.
12. Given the completed diff, when independent review and `/verify-and-polish` are applied, then the union of current path-based checks/reviewers passes, including independent `code-reviewer` and any additional required reviewers. Missing or failed reviews remain incomplete. Linked PR(s) contain exact patch/platforms, dependency rationale, migration instructions, evidence, limitations, and rollback; the final migration PR closes #564 only after acceptance requirements are satisfied.
13. Given approved checks/reviews, owner Gate 2 review of the finished diff, and explicit owner merge confirmation for the named PR and exact head, when the migration is delivered, then the merge revision, issue evidence, handover/changelog, current setup documentation, README/quick start, and dated superseding runtime decision are recorded. Main-checkout environments are recreated only after merge in coordination with active workstreams; interpreter selection, source startup, and packaged startup are verified again before final acceptance. Under approved D4, the owner rebuilds main `.venv`; main launcher/build `venv` coordination and verification remain explicit acceptance handoff items.
14. Given a failed acceptance or need to revert, when documented rollback is followed, then the known-good prior application revision and a separate retained/recreated 3.14 environment can be used without downgrading a 3.15 environment in place. Data copies and backup/restore compatibility evidence support recovery; rollback capability remains until final acceptance is recorded.

**Calculation surface**
- `none` — runtime/toolchain migration only. No calculation functions, effective-set semantics, progression rules, DB schema, or API response shapes are authorized to change. Existing behavior must be regression-verified under the new interpreter. Any discovered change requiring new semantics returns to owner scope approval and the applicable calculation-surface requirements rather than being folded into this migration.

**In scope**
- Coordinated exact-patch runtime/minimum-version contract, launcher/build environments, analysis target, dependency compatibility work, and existing CI/packaging paths.
- Version-contract and demonstrated compatibility regression coverage; full required verification, independent review, evidence, and linked implementation delivery through coordinated post-merge acceptance.
- Fresh isolated runtime data/environments, stale-environment recovery, dated documentation/decision updates, and verified rollback while preserving the working owner setup.

**Out of scope / non-goals**
- Calculation, schema, API, or intentional product behavior changes; unrelated dependency cleanup or test-policy changes.
- Free-threaded CPython, opt-in JIT/lazy imports, alternate architectures, new supported platforms, or a Python 3.10 fallback.
- Release publication, system-wide Python removal, overwriting another workstream's environment, or experimentation against the owner's live database.
- Rewriting historical outcomes, weakening checks, or claiming installation, upstream compatibility, executable independence, approvals, or acceptance without evidence.

**Assumptions made**
- ⚠️ Python 3.15.1 is the owner-approved exact target, supported by preliminary official availability evidence reported above. Project suitability and complete dependency/platform support remain unproved. Risks and concrete validation routes must be established before Gate 1; full execution evidence belongs to approved implementation/acceptance. A different target needs an explicit recorded owner decision.
- ⚠️ Target-local launch/config/lifecycle repair is evidenced as above without owner-runtime mutation; the broader audit remains red. Private environment feasibility is limited to the verified existing target and cannot authorize global repairs, new checkout creation, or a waiver of remaining lifecycle rules.
- ⚠️ Existing Ubuntu/Windows CI coverage is retained. Exact runner images, binary-wheel coverage, CI-only tooling, and clean-Windows evidence facilities are investigation obligations, not proven support or available infrastructure.
- ⚠️ Minimum necessary dependency/tool updates and focused regression tests are included, while dependency changes requiring broader behavior or policy decisions return to the owner.
- ⚠️ A representative older-data copy and a clean Windows environment without installed Python can be obtained through isolated fixtures or approved infrastructure. Their adequacy and execution route must be established in the council plan; absence cannot be replaced by payload-only or PATH-only smoke claims.
- ⚠️ The user's end-to-end instruction authorizes useful preparation and orchestration; issue-required Gate 0/Gate 1 approvals, protected shared-path coordination, merge prerequisites, and post-merge main-environment coordination remain explicit checkpoints. No approval is inferred from this document's existence.

**Owner decisions — approved at Gate 0**

The earlier forwarded Opus advisory did not approve these choices. The owner subsequently answered the manager's direct asynchronous Gate 0 question: **"Approve all four decisions"** (verbatim), on 2026-10-23. The question explicitly covered Python 3.15.1, Windows Sandbox executable proof without Python, smallest required dependency upgrades with stop/report if insufficient, owner rebuild of main `.venv` after merge, and separately scheduled Sandbox enablement/reboot. This records direct owner approval of those scoped requirements and assumptions; it does not approve Plan v1/v2, waive unresolved setup/evidence obligations, or authorize merge.

| ID | Proposed decision for direct owner confirmation | Status |
|---|---|---|
| D1 | Use exact stable CPython **3.15.1**, standard Windows x64, as the new runtime pin and minimum. Do not substitute another patch or fallback without a new owner decision. | Approved |
| D2 | Prove executable startup without installed Python in **Windows Sandbox**. Hiding Python from `PATH` does not satisfy this proof. Owner enablement/admin/reboot is scheduled separately; inability to obtain proof remains a blocker requiring an owner decision. | Approved |
| D3 | Allow only the smallest dependency/tool upgrades required for 3.15 compatibility. If those are insufficient, stop the affected migration work and report the blocker rather than broaden scope or weaken gates. | Approved |
| D4 | After merge and coordination with active workstreams, the **owner rebuilds the main checkout's `.venv`**. Keep its existing working 3.14 environment available until that coordinated replacement; responsibility/timing for main launcher/build `venv` and acceptance verification must be recorded before final acceptance. | Approved |

**Open questions for the user**
- No blocking Gate 0 question remains within D1–D4's approved scope. Broader dependency changes, a different target, Sandbox substitution, and merge remain owner decisions if needed.
- Before Gate 1, identify dependency/platform compatibility risks, reconcile current-main drift and target isolation prerequisites, and establish concrete validation routes. Full installation/build/regression evidence remains mandatory during approved implementation/acceptance. Sandbox enablement scheduling and coordinated post-merge environment handoff remain outstanding acceptance dependencies.

### Section 0 sign-off — GATE 0
- [x] User confirms the acceptance criteria match intent within the directly approved Gate 0 question's scope.
- [x] User accepted the question's four decisions and associated scoped assumptions; unproved feasibility/setup items remain obligations, not facts.
- [x] Blocking Gate 0 questions answered by "Approve all four decisions"; later plan and merge approvals remain separate.

**Approval evidence:** direct owner asynchronous response **"Approve all four decisions"**, 2026-10-23, to the Gate 0 question described above, delivered to this agent by the owning manager. No Gate 1 approval recorded. Section 0 author: `/root/product_manager` (agent ID supplied by owning manager).

---

## Plan v1

**Goal:** Move the existing application and Windows distribution to standard CPython Windows x64 **3.15.1**, preserving workflows and data, with matching Linux/Windows CI evidence and a recoverable 3.14 setup.

**Baseline:** `ae5ec18c3293df302393b28195d8e12ceb92d176`, verified by `git rev-parse HEAD` while drafting. Refresh remote `main`, changed paths, dependencies, claims, and governing guides before Gate 1; report meaningful drift for council/owner review rather than applying an obsolete plan.

**Scope**
- **In:** exact runtime floor and analysis target; batch guidance; fresh private development/build environments; smallest demonstrated dependency compatibility adjustments; runtime-contract/regression coverage; current setup/rollback documentation; required local/native-CI/Sandbox validation; staged-diff review, PR delivery, and owner-led post-merge handoff.
- **Out:** schema/API/calculation changes; unrelated upgrades; free-threaded/JIT/lazy-import adoption; new platforms; release publication/tags; repository or OS settings changes; owner live-data experiments; global lifecycle cleanup; retirement/deletion of retained environments, worktrees, recovery roots, refs or snapshots.

**Artifacts**

| Path | Planned change | Boundary |
|---|---|---|
| `.python-version`, `utils/python_version.py` | Exact `3.15.1` pin/floor | Preserve minimum-version interface and early-startup behavior. |
| `pyrightconfig.json` | `pythonVersion: 3.15` | Keep Windows analysis platform and existing exclusions. |
| `START.bat`, `build_exe.bat` | Current download/minimum/stale-environment guidance | Preserve interpreter selection from canonical pin and both preflight checks. |
| `requirements.txt`, `requirements-build.txt` | Version comments; pins only for demonstrated blockers | Current PyInstaller **6.22.3** stays unless proven incompatible; no speculative bump. |
| `.github/workflows/ci.yml` | Correct current py3.14 diagnostic prose; analyzer pin only if necessary | Keep every job/check name, triggers, permissions, gate behavior, shard policy, and workflow callers. |
| `.github/workflows/{ci,deep-gate,release,_packaged-windows,deep-gate-visual,deep-gate-watch}.yml` | Verify all six consume `.python-version` | Already covered by runtime-contract tests; no broad workflow rewrite. Non-CI files need no edit unless active stale assumptions are found. |
| `scripts/pyright_baseline_diff.py`, `docs/ci_cd_phase3/pyright-baseline.json` | Update runtime metadata text only | Preserve empty diagnostic set and zero-headroom policy. No diagnostic allowance or gate weakening. |
| `tests/test_python_version_contract.py` | Assert 3.15.1 floor/older rejection/newer acceptance and coordinated surfaces | Add retained-environment coverage only where observable behavior requires it. |
| Existing `tests/test_{runtime_init,runtime_migration,db_migration,program_backup,auto_backup,exports,export_weekly_summary_sheet}.py` and appropriate existing E2E specs | Focused fixes/coverage only for demonstrated compatibility gaps | QA derives cases from AC6/7; no unrelated rewrites or changed product semantics. |
| `package.json`, `package-lock.json` | Conditional Python/npm Playwright alignment only if its upgrade is required | Python Playwright/npm currently both 1.61.0; no unmotivated npm changes. |
| `README.md`, `QUICK_START.md`, `docs/ACTIVE_DEVELOPMENT.md`, `docs/DECISIONS.md`, applicable current runtime/setup documents | 3.15.1 setup, stale-env recovery, superseding dated decision, rollback | Preserve historical ADR-003 and dated historical outcomes. Search tracked active references before deciding additional paths. |
| `docs/test_inventory/**` | Generated changes only for actual covered test/config identity/count changes | Use generator; never hand-edit inventory or include scratch markdown in globbed surfaces. |
| `docs/python315_migration/PLANNING.md`, migration evidence under `docs/python315_migration/`; ignored `artifacts/python315_migration/` | Planning and durable evidence/index; full logs/manifests under artifacts | Evidence references exact SHA/platform/environment and distinguishes pending, failed, skipped, inherited, passed. |
| `docs/MASTER_HANDOVER.md`, existing changelog destination if required | Coordinated final milestone/handoff | Shared-path coordination; not a change in calculation or schema. |

**Effort:** L. **Owner:** owning manager coordinates; `senior-developer` implements, `automation-qa` owns test writes, independent reviewers review, owner handles Sandbox enablement and post-merge main `.venv`. **Depends on:** verified task-local isolation; current-main refresh; Gate 1 approval; separately scheduled Sandbox availability; explicit finished-diff/merge approvals.

**Sequence**
1. **Finish preparation and separate local safety from global audit.** Target-local launch/config/lifecycle repair is now verified in `artifacts/worktree/isolation-repair.RESULT.json`: PASS probe using existing standard system Python 3.14.6 in isolated stdlib-only mode, module/DB/log/interpreter identity checks, DB absent, own ACTIVE row ANNOTATED/`blocked: false`, next review 2026-11-22. Other 96 records and outside-JSON prose were preserved and approved-baseline SHA unchanged. Global audit **166 → 165 errors** reflects only this target's repaired row; exact unrelated errors remain and `globalAuditOk: false`. No app/DB/tests/install/environment creation or production changes were needed for that repair. Retain the report and recovery artifacts; no unrelated registry/baseline repair, waiver, new checkout creation, cleanup, PREVENTION_COMPLETE, or claim of global health is authorized. Recheck preflight before later runtime work and assign private DB/backups/logs and dedicated free ports. If current rules make remaining errors block task-local work, stop for an owner ruling; local repair cannot override them. Refresh `main` and resolve path claims before Gate 1.
2. **Bounded feasibility after verified isolation.** Review official 3.15.1 Windows/porting notes and complete a dependency/tool inventory including transitive packages, MarkupSafe, greenlet, pytest/Playwright, PyInstaller/hooks, pip/setuptools, flake8/pylint, pip-audit, safety, and pinned npm-invoked pyright 1.1.410. Record Windows/Linux wheel/installer availability, analyzer 3.15 recognition, and CI runner image implications. Once task-local isolation is verified, a private fresh 3.15 feasibility environment may establish installability, `pip check`, resolved versions, and imports without committed production changes. Do not reuse another workstream's 3.14 environments or install into the owner environment. Report blockers and the smallest necessary pin changes for the final council plan. Full proof remains post-approval acceptance work.
3. **Council and owner Gate 1.** Three independent reviewers read this artifact; manager synthesizes dispositions, and the same PM writes their verbatim findings, response matrix, and Plan v2. Owner approval is required before committed runtime/config/application/test implementation. Material compatibility scope expansion returns to owner decision; no prerelease/older runtime fallback.
4. **QA then coordinated implementation.** QA adds/updates runtime-contract cases for exact minimum 3.15.1, accepted 3.15.2/newer supported versions, rejected 3.15.0/3.14.6/older minors, analyzer target, six workflow consumers and batch checks. Senior developer applies the minimal listed changes and creates fresh **independent** `.venv` and `venv` from standard CPython 3.15.1 x64. Verify `sys.version`, `sys.executable`, `sys.base_prefix`, launcher registration, editor selection, resolved dependencies and `pip check` in each. No machine paths committed. Retain old interpreters/environments; do not downgrade an environment in place.
5. **Source/data regression evidence.** Exercise explicit `python app.py`/supported initialized entry points against task-private fresh runtime and historical-schema/copy fixtures, not import-only proof. Verify stale 3.14 environment rejection using an isolated retained/test 3.14 interpreter, successful 3.15 source and launcher startup, representative plan/log/analyze/progress/distribute/profile flows, startup backup, persistence, backup/restore, non-ASCII CSV/JSON/Excel exports and Windows paths. Compare stable data/contract results with the known-good base; do not alter calculation semantics or schema. A demonstrated encoding/runtime defect receives the smallest focused fix and coverage; broader changes return to scope review.
6. **Full local gates and typing.** Run repository full pytest, then the full Chromium suite with the runner's separate functional/visual seeds. Use task-specific `HT_RUNTIME_DIR`, `PW_DB_PATH`, `PW_PORT`, `TEST_ARTIFACTS_DIR`, one local worker and no shared/reused server; confirm the chosen ports are free. Capture no-retry primary outcomes and every retry if a configured CI run retries; retries are not silently treated as first-pass success. Build CSS as the established E2E prerequisite without accepting generated drift. Execute `tsc`, pinned pyright JSON and blocking baseline diff, inventory drift, and affected lint/audit/workflow contracts. Keep pyright's zero diagnostics; metadata-only regeneration may not import diagnostics. For unclear failures use an already-approved isolated base or owner-approved creation, never the live main DB.
7. **Native Windows packaging plus Sandbox.** Build from fresh task `venv` and committed requirements via canonical spec; run `scripts/stage_package_assets.py`, PyInstaller `--clean --noconfirm Hypertrophy-Toolbox.spec`, then `scripts/smoke_packaged_app.py --mode bootloader --port <free dedicated port>` with no skip flags. Record PyInstaller/hooks, interpreter, asset inventory, executable hash, runtime migration/backup/persistence/export evidence. Separately, owner schedules/enables Windows Sandbox with needed admin/reboot; agent does not alter OS settings. In a clean Sandbox with no installed Python, copy the complete hashed distribution from a read-only host share into guest-local storage, set guest-private `HT_RUNTIME_DIR`/`HT_PORT`, and launch the **exe directly**. Use guest PowerShell HTTP/UI probes and process/log checks, not a Python harness installed into the guest. Verify startup, assets, create/restart/persist, backup/restore and representative export; save transcript/screenshots/hash/absence-of-Python evidence to a dedicated evidence share. PATH hiding is insufficient. Missing Sandbox proof keeps acceptance incomplete.
8. **PR/native CI and non-publishing workflow paths.** Prepare a linked PR after required diff reviews and authorized remote publication. Inspect real check runs on its exact head: existing Ubuntu source/dependency/test/type/inventory paths, Windows 2022 tests/visual compare, Windows latest packaged bootloader, and required contexts. Dispatch approved `deep-gate.yml` on the branch and `deep-gate-visual.yml` in **compare** mode for Ubuntu 24.04 evidence; dispatch `release.yml` with `dry_run=true` only when exact-head CI provenance can satisfy it. No tags/releases, baseline generation, settings changes, or automatic issue-writing watchdog dispatch; validate `deep-gate-watch.yml` via contracts/std-lib checks or separately approved `dry_run=true` only. Link actual SHA/run/artifacts; absent platform support remains a blocker, not a local-green inference.
9. **Finish review and delivery with explicit handoff.** Run `/verify-and-polish` under the current quality-guide requirements: full gate, independent `code-reviewer`, and the exact union of required path-specific reviewers from the final diff (including architecture for any added/removed/converted workflow job, and additional DB/product reviewers if scope changes). No optional style reviewer is added without explicit user request. Resolve findings and rerun affected checks after changes. Obtain owner Gate 2 review of finished diff and separate merge confirmation for named PR/exact head; checks or Gate 1 alone cannot authorize merge. Record merge SHA and issue/handover evidence accurately. **Owner rebuilds main `.venv` after merge**, coordinated with other workstreams; main launcher/build `venv` replacement and source/packaged checks are explicitly handed off and evidenced. Final acceptance remains pending until that handoff and Sandbox proof pass. Preserve the known-good 3.14 revision/environment and backup copies through acceptance, with no cleanup authority inferred.

**Acceptance-to-check map / expected gates**

Proposed for the `test-strategist` to confirm; names below are planned evidence, not completed checks.

| Acceptance | Concrete check / route | Required evidence |
|---|---|---|
| AC1–4 | Official artifact/porting inventory; private Windows `.venv` + build `venv` install and `pip check`; native Ubuntu/Windows CI installs; resolved dependency/wheel/analyzer inventory | Exact CPython 3.15.1 x64, runner/platform identity, resolved tools and any minimal pin rationale. |
| AC2/5 | `tests/test_python_version_contract.py`; real isolated 3.14 rejection and 3.15 source/batch/frozen launch | Guard result/error guidance plus pin/analyzer/six-workflow/batch agreement; no owner-env mutation. |
| AC6/7 | `tests/test_runtime_init.py`, `test_runtime_migration.py`, `test_db_migration.py`, `test_program_backup.py`, `test_program_backup_restore_fuzz.py`, `test_auto_backup.py`, `test_exports.py`, `test_export_weekly_summary_sheet.py`; source/manual core-flow probes | Fresh and older-data startup, preserved fixture records, non-ASCII import/export/backup round-trip, persistence and SQLite version/runtime notes. |
| AC8 | `.venv/Scripts/python.exe -m pytest tests/ -q`; `npm run test:e2e` with no spec arguments so `scripts/run-playwright.ps1` partitions full functional and visual-seed suites | Full counts, failures/skips/retries and logs; Windows byte compare without baseline writes; core specs include workout-plan/log, summaries, progression, volume-splitter, user-profile, program-backup. |
| AC9 | `npx tsc --noEmit`; `npx pyright@1.1.410 --outputjson` (upgrade only if proven needed); `.venv/Scripts/python.exe scripts/pyright_baseline_diff.py --current <artifact JSON> --baseline docs/ci_cd_phase3/pyright-baseline.json`; inventory generator `--check` | Zero new diagnostics, retained empty diagnostic allowance, no inventory drift; regenerate only on genuine test/config changes. |
| AC8/9/11 | Affected lint/audit/workflow tests including `test_python_version_contract`, `test_release_workflow_contracts`, `test_playwright_runner_contracts`, `test_playwright_shard_launcher_contracts`, `test_pyright_baseline_diff`; existing PR security/dependency/supply-chain jobs | Unchanged status contexts/callers/triggers/gates; native CI on exact implementation head; failure comparison if origin unclear. |
| AC10 | Canonical-spec fresh-build + actual bootloader smoke; separate clean Windows Sandbox direct-exe run | Hash-linked distribution, no smoke skip flags, isolated port/runtime, data/assets/export proof; guest has no installed Python. |
| AC11/12 | PR checks; deep-gate and Linux visual **compare** dispatch; release **dry_run** exact-head provenance; independent review/`verify-and-polish` | Run URLs/head SHA/check conclusions, reviewer passes and resolved findings; no publication or acceptance inferred from partial checks. |
| AC13/14 | Current setup/dated ADR; owner approved named PR/head and recorded merge; owner main-environment handoff; isolated prior-revision + separate 3.14 recovery rehearsal | Owner handoff completion/source/frozen startup results and preserved rollback revision/environment/data compatibility. |

**Failure / rollback rule:** Keep migration open on any unresolved dependency, native-CI, bootloader, Sandbox, review or post-merge acceptance blocker. D3 permits only smallest required compatibility upgrades; if insufficient, stop affected work and report. Restore the known-good revision into the separately retained/recreated 3.14 environment with isolated copied data/backups; never downgrade the new environment or mutate live data as a test. No silent baseline/allowlist expansion or fallback. No worktree/ref/snapshot retirement under this plan.

---

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `/root/product_manager` | Supplied by manager; same agent authored Section 0 and Plan v1. |
| `product-manager` — response matrix + Plan v2 | `/root/product_manager` | Same PM resumed for this write; ID supplied again by manager. |
| `architecture-reviewer` | `/root/council_architecture` | Verbatim review below. |
| `test-strategist` | `/root/council_tests` | Verbatim review below. |
| `product-risk-reviewer` | `/root/council_product_risk` | Verbatim review below. |

**Same product-manager resumed for the matrix + Plan v2?** `yes` — manager resumed `/root/product_manager` using collaboration follow-up/send messages. Original Plan v1 preserved as reviewed.

**Evidence gap:** none. All IDs supplied by the manager; no completed council work rerun to manufacture continuity.

## Reviewer findings

### architecture-reviewer (agent `/root/council_architecture`)

**Plan is sound.**

### test-strategist (agent `/root/council_tests`)

## Required gates

- **Full `/verify-suite` required.** Root runtime/analyzer configuration and `scripts/pyright_baseline_diff.py` are cross-cutting; `.github/workflows/**` independently requires full pytest. See `docs/ai_workflow/QUALITY_GATE.md`, “Change-type → gates” and “Targeted-test derivation.”
- **pytest:** `.venv/Scripts/python.exe -m pytest tests/ -q`, including runtime-version, runtime initialization/migration, backup/restore/export, packaging, Playwright-version, workflow-contract and pyright-gate tests.
- **E2E:** `npm run test:e2e` **without additional arguments**, after CSS build and browser installation. This correctly uses `scripts/run-playwright.ps1:157–174` to partition functional and visual seeds. Raw `/verify-suite`’s single `npx playwright test` command is insufficient for the required seed partition; retain the plan’s explicit runner choice.
- **Types/inventory:** `npx tsc --noEmit`; pinned pyright JSON plus blocking baseline diff; `scripts/generate_test_inventory.py --check`. Regenerate inventory for changed parametrized/test counts, using the generator.
- **Packaging/data:** canonical-spec build, actual bootloader smoke without skip flags, isolated fresh/older-data startup and backup/restore smoke, plus separately recorded Windows Sandbox proof.
- **CI:** exact-head required PR checks and the approved deep-gate/Linux-visual/release-dry-run evidence specified in Plan v1.
- **Independent post-code review:** `code-reviewer` **and `unslop-reviewer`**. Add path-required reviewers if the eventual diff expands. Architecture review is additionally mandatory if a workflow job is added, removed or converted to `uses:`.

## Existing coverage

- `.python-version`, `utils/python_version.py`, `pyrightconfig.json`, `START.bat`, `build_exe.bat`, all six listed workflow consumers — `tests/test_python_version_contract.py:19–105`. Covers interpreter minimum, simulated rejection/acceptance, pin/analyzer agreement and textual batch/workflow contracts.
- `build_exe.bat` and canonical packaging path — `tests/test_packaging_contract.py:50–110`, `tests/test_package_asset_staging.py`; real executable evidence comes from `scripts/smoke_packaged_app.py` and `_packaged-windows.yml`, not those source-contract tests.
- `requirements.txt`, conditional `package.json`/lock changes — `tests/test_playwright_version_contract.py:51` asserts exact Python/npm Playwright alignment. Fresh installation, binary compatibility and transitive dependency validity still require execution evidence.
- `.github/workflows/ci.yml` — full pytest covers the seven parsing contract modules enumerated by `QUALITY_GATE.md`; reusable packaging/release callers are covered by `tests/test_release_workflow_contracts.py`.
- `scripts/pyright_baseline_diff.py` and its baseline — `tests/test_pyright_baseline_diff.py:36–192` covers multiset regression detection, normalization, serialization and CLI pass/fail. Actual 3.15 analyzer recognition and diagnostics require the real analyzer run.
- Runtime/data probes — `tests/test_runtime_init.py:425` actually upgrades an older-schema database; `tests/test_runtime_migration.py:74` checks preserved rows/original bytes, and `:260` covers spaces/non-ASCII paths. `tests/test_program_backup.py:947` supplies row-preserving backup/restore coverage. `tests/test_auto_backup.py:80` covers startup snapshot copying/rotation.
- Excel exports — `tests/test_exports.py:284` checks workbook structure; `tests/test_export_weekly_summary_sheet.py:62–109` checks exported calculation figures and route agreement. These are useful regression coverage, but do not establish all AC7 encoding claims.
- `README.md`, `QUICK_START.md`, current setup/development/decision documents, migration planning/evidence and handover — documentation self-review; executable examples must match the validated commands. No separate product-doc tests are required.
- `docs/test_inventory/**` — generator drift check, not manual editing.

## Coverage gaps

**T1 — Required reviewer omitted; fix before Gate 1.**
`docs/python315_migration/PLANNING.md:130` names `code-reviewer` and path-specific reviewers, omits `unslop-reviewer`, and then excludes optional style review. `unslop-reviewer` is mandatory under `.claude/commands/verify-and-polish.md:15–16` and `QUALITY_GATE.md`, “Two gates, two purposes.” Name it explicitly in Plan v2 so it cannot be treated as optional. No additional reviewer authorization is needed for this already-required gate.

**T2 — Native-platform `pip check` acceptance lacks an execution route.**
AC3 at `PLANNING.md:31` requires dependency installation **and `python -m pip check` on supported platforms**. Plan v1’s map at `:138` promises private Windows checks but only existing native-CI installations. The inspected install steps in `ci.yml`, `_packaged-windows.yml` and `deep-gate.yml` do not run `pip check`. Existing green checks therefore cannot prove this acceptance criterion. Plan v2 must identify actual Windows/Linux commands/jobs that run it and retain their output. A small addition to appropriate existing install steps is a concrete route; preserve their names and behavior otherwise.

**T3 — AC7’s file list does not itself prove non-ASCII round trips.**
`PLANNING.md:140` groups runtime/export/backup tests under “non-ASCII import/export/backup round-trip,” but the verified Unicode case in `test_runtime_migration.py:260` exercises directory names. The inspected export tests cover structure, ordering, figures and errors; `test_program_backup_restore_fuzz.py` covers malformed bounds, not Unicode transport.

Specify an acceptance probe matrix in Plan v2: supported interface, non-ASCII fixture values, bytes/text/workbook values asserted, restart/restore boundary, and evidence destination. Use existing supported JSON/Excel/backup interfaces. The source inspected in `routes/exports.py` provides Excel export; no generic user CSV import/export route was verified. Mark unavailable interfaces as such rather than creating functionality to satisfy a loosely worded checklist. Manual reproducible probes can discharge this requirement; if automated, extend `tests/test_exports.py` and `tests/test_program_backup.py` with the actual round-trip assertions. Do not add speculative behavior tests.

**Known-red handling:** retain the historical `e2e/program-backup.spec.ts:79` pollution flake designation and record isolation results if it appears. Current visual authority is `docs/MASTER_HANDOVER.md:159–181`: Windows residuals are existing `BYTE_GATE_EXEMPT` policy cases, and Linux baselines were refreshed by #548. Do not import older red counts or regenerate snapshots to pass this migration.

## Conftest / fixture work

None currently required. No blueprint/table/schema change is authorized. Existing test application fixtures use `create_app()`; retain separate actual entry-point initialization probes for startup acceptance.

## Verdict

**Full `/verify-suite` required. Revise Plan v1 for T1–T3 before owner Gate 1.** No tests, applications, installations, database operations or file writes were performed during this review. This reviewer verdict does not approve Gate 1.

### product-risk-reviewer (agent `/root/council_product_risk`)

**PR1 — Plan v1, Sequence 8–9: move required Gate 2 before committing or publishing the implementation.**

Invariant at risk: `docs/ai_workflow/QUALITY_GATE.md:24–30` defines Gate 2, when required, as direct owner review of the finished diff and evidence **before commit or activation**. Plan v1 explicitly requires Gate 2, but Sequence 8 prepares/publishes a PR (`docs/python315_migration/PLANNING.md:129`) before Sequence 9 obtains that approval (`:130`).

Risk: The implementation can be committed and published before its required owner checkpoint. Gate 1 and reviewer passes cannot supply that approval.

Fix: Complete local verification and independent diff review, obtain direct owner Gate 2 approval before committing/publishing, then collect exact-head PR/CI evidence and obtain separate named-PR/head merge confirmation; material subsequent changes require refreshed applicable review and approval.

No additional product-invariant findings. The plan preserves calculation/schema/API boundaries (`:44–55`), isolated data and backup verification (`:126–128`), retained 3.14 rollback (`:148`), and owner responsibility for main `.venv` and Sandbox enablement (`:68–75`, `:130`). It introduces no product terminology changes, remote-data services, or resumption of parked product work.

Review was read-only; no files, environments, application state, databases, or tests were changed or executed.

**Verdict: Needs revision.**

---

## Response matrix

All dispositions are the manager's synthesis, incorporated for owner consideration at Gate 1. No finding is deferred.

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| Architecture: Plan is sound; no finding | `/root/council_architecture` | accept | Preserve module/data/contract boundaries and isolation constraints. |
| T1: required `unslop-reviewer` omitted | `/root/council_tests` | accept | Restore explicit mandatory `code-reviewer` + `unslop-reviewer` and path-required union before Gate 2. The manager's earlier interpretation came from differing uncommitted main-checkout policy; tracked task guides govern and no waiver exists. |
| T2: native `pip check` route absent | `/root/council_tests` | accept | Add bounded commands to existing Linux/Windows install bodies, including tooling/build environments; record outputs and resolved versions in actual native jobs. |
| T3: Unicode round-trip proof not specified | `/root/council_tests` | accept | Add supported-interface probe matrix with exact fixtures/assertions/restart/restore/evidence; unsupported generic user CSV is N/A with source evidence. |
| PR1: Gate 2 after publication | `/root/council_product_risk` | accept | Local full gates + independent reviews → direct owner Gate 2 finished-diff approval → commit/push/PR → exact-head native CI/dry runs → separate owner named-PR/head merge approval. Refresh checks/reviews/owner approval for material changes before another commit. |

---

## Plan v2

**Goal:** Deliver standard CPython **3.15.1 Windows x64** consistently across development, runtime enforcement, analysis, six workflow consumers and the Windows distribution, with unchanged product/data contracts and recorded rollback.

**Final manager live recheck:** `git ls-remote origin refs/heads/main` still returned `ae5ec18c3293df302393b28195d8e12ceb92d176`; connected GitHub returned no open PRs at that instant. No baseline drift requires new council work. Existing stale claim rows remain other owners' records; coordinate affected paths before implementation rather than retiring their rows. This is a dated observation, not continuing merge authority.

**Scope**
- **In:** Plan v1's minimal runtime/environment/configuration/docs/test migration, plus the bounded native dependency checks and concrete Unicode probes below. Preserve Python/npm Playwright alignment, zero pyright baseline diagnostics, and current PyInstaller **6.22.3** unless demonstrated compatibility failure requires the smallest upgrade.
- **Out:** Schema/API/calculation changes; speculative upgrades or new CSV features; JIT/free-threaded/lazy imports; new platforms; release publication/tags or settings changes; global lifecycle repair/waivers; live owner-data experiments; worktree/environment/ref/snapshot retirement.

**Artifacts**

| Paths | Final planned change |
|---|---|
| `.python-version`, `utils/python_version.py`, `pyrightconfig.json`, `START.bat`, `build_exe.bat` | Exact 3.15.1 floor/pin, 3.15 analysis target, current launch/build/download/stale-environment guidance; retain interfaces and explicit pin-derived interpreter selection. |
| `requirements.txt`, `requirements-build.txt`; conditionally `package.json`/lock | Update runtime comments; only smallest proven compatibility pin changes. Retain PyInstaller 6.22.3 and Playwright 1.61.0 alignment unless evidence justifies change. |
| `.github/workflows/ci.yml`, `_packaged-windows.yml`, `deep-gate.yml`, `deep-gate-visual.yml` | Existing diagnostic prose/analyzer pin where necessary; add bounded `pip check`/resolved-version output to named existing install steps below. No new/removed/renamed/converted jobs, changed triggers/permissions/contexts/callers or gate weakening. All six consumers, including `release.yml` and `deep-gate-watch.yml`, remain canonical-pin checked. |
| `scripts/pyright_baseline_diff.py`, `docs/ci_cd_phase3/pyright-baseline.json` | Runtime metadata only; diagnostic allowance remains empty/zero. |
| `tests/test_python_version_contract.py`; demonstrated-gap cases in existing runtime/export/backup modules | QA-first floor/config/retained-env regressions; Unicode assertions only for actual supported behavior. No conftest/schema/blueprint change planned. |
| README, quick start, current runtime/development docs, dated `docs/DECISIONS.md` entry | Installation, stale-env replacement, owner post-merge handoff, rollback; retain ADR-003/history. |
| `docs/test_inventory/**`, migration evidence/docs, coordinated handover/changelog | Generator-only inventory changes for real test/config drift; exact-revision evidence and pending acceptance handoff. Full logs under ignored `artifacts/python315_migration/`. |

**Sequence**
1. **Refresh and feasibility.** Re-read remote `main` immediately before final Gate 1, compare with `ae5ec18c3293df302393b28195d8e12ceb92d176`, and reconcile guide/dependency/claim drift. Existing target setup is verified in `artifacts/worktree/isolation-repair.RESULT.json`: stdlib-only identity/config probe PASS, private DB absent, ACTIVE unblocked row, next review 2026-11-22; all other records/prose/baseline preserved. Global audit still has **165 unchanged unrelated errors**: no global health, PREVENTION_COMPLETE, new-checkout or cleanup authority follows. Recheck preflight/target identity before later private work. Bounded fresh private 3.15 feasibility can establish dependency/analyzer risks and smallest changes; no production/config/test implementation before direct owner Gate 1. Any rule that blocks further existing-target work is escalated rather than waived.
2. **Owner Gate 1, then QA/implementation.** Owner reviews this Plan v2 and all accepted dispositions. After approval, QA updates exact-floor/newer acceptance and 3.15.0/3.14/older rejection tests and real batch/runtime contracts. Developer applies the coordinated artifact changes, creates independent task `.venv` and build `venv`, and records interpreter/base prefix/launcher/editor identity, resolved requirements and `pip check`. Preserve main 3.14 environments and known-good revision. Any upgrade beyond the smallest required compatibility changes, different interpreter target or changed product semantics stops affected work for owner decision.
3. **Local source/data/full gates.** Use target-private runtime/DB/backups/logs and dedicated free ports; no shared/reused server or owner live DB. Run actual initialized source/launcher entry points against fresh and older-schema/copy fixtures, stale-3.14 rejection, full core flows and the Unicode matrix. Record SQLite/runtime versions and data preservation. Run **full pytest first**, then `npm run test:e2e` **without arguments**, following CSS build and Chromium install; this partitions functional and visual seeds correctly. Run type/baseline diff, inventory and affected audit/lint/workflow gates. Do not weaken assertions, snapshots, diagnostic allowances or retries; report inherited failures, isolate the backup pollution flake if seen, use current visual authority without snapshot regeneration, and seek an approved isolated base if origin is unclear.
4. **Local Windows executable and clean guest.** Fresh build environment + committed requirements + canonical spec: stage assets, build with `--clean --noconfirm`, execute existing host `scripts/smoke_packaged_app.py --mode bootloader --port <free port>` without skip flags. Verify bundled assets, source-to-runtime migration, startup backup, persistence, backup/restore and exports. Separately owner schedules Sandbox enablement/admin/reboot; agent makes no OS setting change. Copy complete hash-identified distribution from read-only mapped dist into guest-local storage; map only a separate results directory writable, never host live data. Set guest-private runtime and dedicated port. With Python absent, use **PowerShell-only** `Start-Process` of the executable plus `Invoke-WebRequest`/`Invoke-RestMethod`, process/log/HTTP probes and results to prove startup and representative create/restart/persist/backup/restore/export behavior. No Python harness is installed into the guest; no PATH-hiding substitution. If availability is still pending, record that explicitly and keep acceptance incomplete.
5. **Required review and direct owner Gate 2 before committing/publishing.** Complete local full verification and the actual required `code-reviewer` **and `unslop-reviewer`**, plus the final-diff union of path-required reviewers. Current tracked `QUALITY_GATE.md` “Two gates, two purposes” and `verify-and-polish.md` require both; Plan v1's exclusion is superseded. Fix findings and refresh affected checks/reviews. Bind precommit test/build/Sandbox evidence to the **staged source tree/file hashes and executable hash**; the existing base HEAD is not the implementation revision. Present the finished diff and all local evidence, with any outstanding external/Sandbox evidence clearly marked, for **direct owner Gate 2 approval before any implementation commit, push, PR publication or activation**. Gate 1 and reviewer passes cannot supply this decision.
6. **Commit/publication and exact-head native evidence.** Only after Gate 2 and authorized remote publication, commit/push and open linked PR(s). Verify the committed source tree matches the approved/tested staged tree, then run real native dependency checks below and all exact-head required contexts, packaged Windows CI, approved branch `deep-gate.yml`, Linux visual **compare**, and `release.yml` **dry_run=true** when exact-head provenance permits. No tags/releases/settings or watchdog issue writes; watcher contracts suffice unless owner separately approves a dry run. Native/platform or compatibility failures remain blockers. Every material source/config fix refreshes applicable checks, independent reviews and **direct owner approval before the new commit/push**; final native evidence must match the final head.
7. **Separate merge approval and acceptance handoff.** Present final PR/head, checks and outstanding acceptance status for direct owner merge confirmation. No missing required gate is waived by this plan. Record merge SHA, issue links, limitations and coordinated handover. Owner rebuilds main `.venv` after merge and workstream coordination; main build `venv` responsibility/timing must be coordinated separately. Verify interpreter selection, source and packaged startup again. Keep final issue acceptance open until required Sandbox/data/runtime evidence and main-environment handoff are complete. Retain 3.14 rollback revision/environments and copied backups through acceptance; no deletion/cleanup is authorized.

### Native dependency checks (T2)

These are actual command additions to existing appropriate install bodies, not assertions that current install-green proves dependency consistency. Append **`python -m pip check`** after all installations in the named environment and **`python -m pip list --format=json`** (or `freeze --all`) for resolved evidence. Preserve the native command's nonzero status, including explicit `$LASTEXITCODE` handling in PowerShell where necessary. Retain run URLs/SHA/job logs and downloaded resolved manifests under `artifacts/python315_migration/dependencies/<platform>/<job>/` with a durable evidence index.

| Existing workflow / job ID | Exact environment/placement |
|---|---|
| `ci.yml` / `pytest-core` | Ubuntu-latest runtime/test installation: after `requirements.txt`, run `python -m pip check` and resolved-version output before pytest. |
| `ci.yml` / `security-audit` | Ubuntu audit environment: after requirements, setuptools and pinned pip-audit are installed, run checks/output before audit. |
| `ci.yml` / `lint` | Ubuntu lint environment: after requirements plus flake8/pylint, run checks/output before lint. |
| `ci.yml` / `worktree-windows` | Native Windows-2022 runtime/test installation: after `python -m pip install -r requirements.txt`, run checks/output before existing tests. |
| `_packaged-windows.yml` / `build-and-smoke` | Native Windows-latest build environment: after **both** requirements manifests and their resolved hooks, run checks/output before staging/spec build/bootloader smoke. All three existing callers retain identical behavior. |
| `deep-gate.yml` / `dependency-health` | Ubuntu supplementary-tool environment: after requirements and `safety` are installed, run checks/output to cover this CI-only tool environment. No tool-policy redesign. |
| `deep-gate-visual.yml` / `visual-linux` | Ubuntu-24.04 existing requirements installation: run checks/output before the current compare-only browser path to evidence the distinct existing Linux runner image. |

Task-local fresh `.venv` and build `venv` also run their own explicit `python -m pip check`. Full direct/transitive inventory includes pip/setuptools, binary wheels/greenlet/MarkupSafe, runtime/test/build/hooks, CI-only lint/audit tools and pyright; resolve any incompatibility with smallest evidenced changes or stop/report under D3. Upstream classifiers and wheel listings supplement execution; they cannot replace it.

### Unicode and file-boundary acceptance probes (T3)

Use fixture text **`אימון כוח – Café`**, Unicode notes and a task/guest-private Windows directory containing **`בדיקה Café`**. Keep numeric inputs/expected results identical to the base; the migration must not change calculations. Manual reproducible probes can discharge these checks; add focused cases to `tests/test_exports.py`, `tests/test_program_backup.py` or actual parser/runtime modules only when coverage is needed. Store commands/input fixtures, raw responses/downloads, parsed assertions, hashes and transcripts under `artifacts/python315_migration/unicode/<source|frozen|sandbox>/`, indexed in durable migration evidence.

| Actual supported boundary | Assertions and restart/restore boundary |
|---|---|
| JSON backup API in `routes/program_backup.py`: `POST /api/backups`, `GET /api/backups/<id>` and restore endpoint | Submit Unicode backup name/note and a safely seeded plan with a Unicode routine through existing supported fixture/UI contracts; decode captured HTTP bytes as strict UTF-8 JSON, compare decoded strings/code points exactly (JSON escapes are valid), and assert saved plan fields/row values. Restart the real source/frozen process, fetch again, restore the snapshot through its supported endpoint and verify the same strings/rows after another restart. Save input/raw response/decoded assertions; no claim that backups expose a nonexistent JSON-file import interface. |
| Existing Excel `GET /export_to_excel` in `routes/exports.py` and applicable summary/large-data export interfaces | Save actual XLSX bytes under Unicode paths; verify nonempty valid ZIP/workbook, read using installed host openpyxl and assert Unicode routine/text cell values plus unchanged numeric figures/row ordering. Repeat after persistence restart and backup restore. For Sandbox, save guest-produced workbook and verify those exact hashed bytes on host, without installing Python into guest. Check Unicode only in fields each existing export actually includes. |
| Private runtime/backup paths and old-data copies | Start source and frozen app with Unicode `HT_RUNTIME_DIR`, verify runtime DB/log/backup destinations, preserved copied rows, restart persistence and readable startup snapshot. Preserve original copy/hash and compare logical user data after existing initialization; no new schema semantics or live-data writes. |
| Actual CSV catalog-maintenance parsers: `scripts/apply_free_exercise_db_mapping.py::parse_csv` and `scripts/apply_youtube_curated.py::parse_csv` | Prepare valid existing-format CSV fixture bytes using explicit UTF-8 with Unicode text in allowed name fields and a Unicode filename. Verify bytes decode strictly and actual parser returns exact strings with expected validation; use parser-only or existing dry-run/safe isolated fixture path, never catalog writes/live data. Retain original fixture bytes/hash and parser result; no invented user CSV workflow. |
| Generic user CSV import/export | **N/A unless an actual supported interface is identified.** Inspected `routes/exports.py` exposes Excel and plan-to-log exports, not a generic CSV route; the named scripts are catalog maintenance. Record the source search/revision as evidence of N/A. Do not add a CSV feature or claim a nonexistent UI flow passed. |

### Acceptance-to-check map / final required gates

| Criteria | Concrete acceptance evidence |
|---|---|
| AC1–4 | Official 3.15.1 artifact/porting review and dependency/wheel/tool inventory; task `.venv`/build `venv` install + explicit `pip check`; native job matrix above; exact runner/interpreter/resolved versions. |
| AC2/5 | Runtime-contract pytest including canonical pin/minimum/analyzer/six consumers/batch checks; actual isolated retained-3.14 rejection and successful 3.15 source/batch/frozen startup. |
| AC6/7 | Fresh/older-data initialization, `test_runtime_init`, `test_runtime_migration`, `test_db_migration`, program/auto backup and export coverage; **separate concrete Unicode matrix evidence**, persistence, backup/restore and stable data/results. Existing filenames alone do not discharge Unicode transport. |
| AC8 | Full `.venv/Scripts/python.exe -m pytest tests/ -q`, then CSS/browser prerequisites and `npm run test:e2e` without arguments; all current identities with correct functional/visual seeds. Record counts/skips/failures/retries and isolated historical backup flake; no retry-as-pass or snapshot regeneration. |
| AC9 | `npx tsc --noEmit`; `npx pyright@1.1.410 --outputjson` unless smallest proven analyzer upgrade; blocking `scripts/pyright_baseline_diff.py --current <JSON> --baseline docs/ci_cd_phase3/pyright-baseline.json`; inventory generator `--check`. Zero diagnostic headroom retained; regenerate only real covered inventory changes. |
| AC8/10/11 | Full workflow/packaging/staging/version/runner/pyright contract tests and appropriate lint/security/audit checks; canonical Windows spec + **host real bootloader**; **separate no-Python Sandbox direct-exe** evidence; exact-head PR/native CI, approved deep-gate/Linux-compare/release dry runs. |
| AC12/13 | Required independent **code-reviewer + unslop-reviewer + final-diff path union**; direct owner Gate 2 **before commit/publish**, exact-head final checks, then separate owner named-PR/head merge approval. Gate approvals/reviewer passes remain distinct. |
| AC13/14 | Setup/dated ADR and rollback instructions; merge/evidence index; coordinated **owner main `.venv` rebuild** and separately coordinated build `venv`; repeated source/frozen checks; retained known-good revision plus separate 3.14 recovery rehearsal on copied data. |

**Failure and rollback:** No unresolved compatibility, native-CI, bootloader, Sandbox, required review or handoff is silently accepted. Stop/report if the smallest dependency upgrades are insufficient. Reuse a known-good revision with a separately retained/recreated 3.14 environment and copied data/backups; never downgrade 3.15 in place, expand baselines to hide failures, or test recovery against live data. Scope/target changes need owner decision. All final execution evidence remains pending; this plan is not a claim of passed tests or Gate 1 approval.

---

## Owner execution amendment — 2026-10-24

**Direct owner Gate 1 approval (verbatim)**

> Gate 1 approved with conditions: (1) Before writing any implementation code, run a private 3.15.1 install + pip check for requirements.txt and requirements-build.txt and record the result; if any pin must change, report it to me first. (2) Add pip check only to pytest-core, worktree-windows, and _packaged-windows build-and-smoke; don't touch lint, security-audit, dependency-health, or visual-linux. (3) Gate 2 once before the first push; later in-scope CI fixes don't need re-approval, and I review the final diff at merge. (4) The Sandbox no-Python test is a requirement for merging; I'll enable Sandbox separately.

**Effect:** This direct instruction approves Gate 1 conditionally and supersedes conflicting execution details in Plan v2, its native dependency-check table, acceptance map, response-matrix actions and earlier sign-off prose. The reviewed plans remain unchanged above; these conditions govern execution. No installation, dependency consistency, test, Sandbox or merge success is inferred from approval.

| Condition | Governing execution rule | Evidence / status |
|---|---|---|
| 1 — private feasibility before implementation | Before writing **any implementation code**, install standard CPython **3.15.1** into a private task environment and install the committed `requirements.txt` and `requirements-build.txt`; run explicit `python -m pip check` against that resolved environment and record interpreter identity, installation outcome, resolved versions and check result. If **any dependency/tool pin** needs changing, report the proposed change and blocker to the owner **first**; the earlier smallest-upgrade scope is not permission to silently alter a pin. | **PASS**, actual evidence recorded below: both unchanged manifests installed and runtime/test plus combined `pip check` exited 0; `pinChangesRequired: false`. This clears the preimplementation prerequisite, not later acceptance gates. |
| 2 — exact three CI additions | Add native `python -m pip check` only to `ci.yml` job **`pytest-core`**, `ci.yml` job **`worktree-windows`**, and `_packaged-windows.yml` job **`build-and-smoke`** after their relevant existing requirements installation (both manifests for build-and-smoke). Preserve command failure propagation and retain actual job output. **Do not touch `lint`, `security-audit`, `dependency-health`, or `visual-linux`.** No additional `pip check` job/body additions are authorized. | **Pending implementation; condition 1 passed.** Supersedes Plan v2's broader job table; other dependency inventory comes from read-only inspection/existing execution evidence without editing the forbidden jobs. Preserve names/triggers/permissions/contexts/callers. |
| 3 — Gate 2 once before first push | Complete required local gates and independent reviews and obtain **one direct owner Gate 2 approval before the first push**. The owner no longer requires approval before every commit or repeated approval for **later in-scope CI fixes**. Those fixes still need applicable validation/review, accurate evidence and final-head CI. Scope or target expansion and pin changes retain their separate decision/reporting boundaries. | **Gate 2 pending.** No first push authorized by this document. Owner reviews the **final diff at merge**, with the named PR and exact head; no merge approval is recorded here. |
| 4 — Sandbox before merge | The clean Windows Sandbox **no-installed-Python direct-executable test must pass before merge**. Owner enables Sandbox separately; no agent OS feature/admin/reboot action is authorized. Keep the PowerShell-only guest harness, private guest runtime, read-only distribution mapping, separate results mapping, hash-linked evidence and no PATH-hiding substitution. | **Pending owner enablement and execution.** This is a **merge prerequisite**, not a post-merge follow-up. Missing Sandbox evidence blocks merge. |

**Unchanged requirements:** exact 3.15.1 target; no intentional schema/API/calculation changes; retained working 3.14 rollback; full pytest then correctly seeded full Chromium, zero-headroom type/inventory gates, host real-bootloader build/smoke, required independent code/unslop/path reviewers, and native exact-head CI. Main `.venv` remains the **owner's coordinated post-merge rebuild**, with main build `venv` responsibility/timing recorded separately. No live main runtime/data mutation or global audit repair/waiver is granted.

**Evidence binding and delivery:** Record precommit local build/test/Sandbox results against tested source-tree/file hashes and executable hash, then prove committed source matches that tested tree and attach native exact-head CI evidence. Gate 2's revised placement does not let base HEAD stand in for an implementation revision. Later in-scope CI repairs do not require another Gate 2 approval; final owner diff review and named-PR/head merge confirmation remain separate and occur only after all merge prerequisites, including Sandbox, pass.

### Preimplementation prerequisite result — PASS

Recorded on the user's local date **2026-10-24**; the raw run completed **2026-10-23T21:18:28.5868517+00:00** (00:18 on 2026-10-24 in Asia/Jerusalem). Evidence was read directly from [RESULT.json](../../artifacts/python315-prerequisite/RESULT.json), interpreter/check output, [artifact-verification.json](../../artifacts/python315-prerequisite/downloads/artifact-verification.json), and [selected-wheels.json](../../artifacts/python315-prerequisite/selected-wheels.json).

- Standard **CPython 3.15.1 final**, Windows x64, `pointer_bits: 64`, `Py_GIL_DISABLED: 0`, UTF-8 mode 1. Official PythonCore archive extracted privately under this checkout's artifacts; feasibility environment is `.venv315-feasibility`, with its own prefix and the private interpreter as base prefix.
- All **11 recorded commands exited 0**. Unchanged `requirements.txt` installation passed, then explicit runtime/test `pip check` passed; unchanged `requirements-build.txt` installation passed, then explicit combined `pip check` passed. Both check outputs state **"No broken requirements found."** Resolved installs selected **36 wheels, zero non-wheel artifacts**; resolved freeze/inspect and install-report files are retained beside RESULT.json. `pinChangesRequired` is **false**.
- Interpreter provenance: official archive `https://www.python.org/ftp/python/3.15.1/python-3.15.1-amd64.zip`; archive SHA-256 **`cc1448e5dc0e1c5782396ededcaea11dd3966175751ae67857629d1dca20aff5`**; official manifest SHA-256 **`b819787561df37cea04b116666dab47977b1c270a9dc19cdf59554b4e1b34b69`**. Executable Authenticode status **Valid**, signer **Python Software Foundation**, certificate thumbprint **`CE40D4BBE67DC0F452A1C41F47920973B9BE1408`**.
- Input manifest SHA-256: `requirements.txt` **`553DD4A5317EE14E878C0D395D56D5916A4A5089797A3B46F62DD7EAF4858A91`**; `requirements-build.txt` **`9AA22671CDF53751373EB123BB95E3F2C9DB35E3F0513BC35082B60E60BAE691`**. These bind the installation result to the actual unchanged requirements, not a proposed dependency update.
- Task DB remains absent. Manager reports no registration/PATH/launcher changes or main-environment mutation. This evidence proves the requested Windows private-install prerequisite; it does **not** prove native Linux CI, full regression tests, the final canonical build, real bootloader, Sandbox or final acceptance.

**Execution handoff:** QA may now write the approved criteria-derived tests and supply the red-test handoff. Developer may prepare independent development/build environments, then apply production changes after that QA handoff. Any newly required pin change must still be reported to the owner first. Gate 2 once before first push, Sandbox before merge, final owner diff/merge review, and owner post-merge main `.venv` rebuild remain unchanged.

## Sign-off

- [x] Gate 0 complete within the recorded direct owner approval.
- [x] Three independent council reviews completed and verbatim findings recorded.
- [x] Every finding has a disposition and Plan v2 reflects accepted findings.
- [x] Agent provenance completed for the full council; same PM resumed and evidence gap none.
- [x] Owner approved Gate 1 **with conditions**, direct instruction dated 2026-10-24 recorded verbatim above; the execution amendment supersedes conflicting Plan v2 details.
- [x] Private standard CPython 3.15.1 installation of both unchanged requirements manifests and explicit runtime/test plus combined `pip check` passed; actual result recorded before implementation.
- [x] Ready for implementation within conditional Gate 1 and verified task isolation; no pin changes required by feasibility. QA-first test handoff and first-report of any later pin change remain binding.
- [ ] Owner Gate 2 approval obtained once before the first push.
- [ ] No-Python Sandbox test passed before merge; final owner diff review and named-PR/head merge approval obtained.

**Current boundary:** Conditional Gate 1's private install/`pip check` prerequisite is evidenced **PASS**; approved QA-first implementation may proceed. This write changes only the planning record. It records no completed implementation, full verification, first-push Gate 2 approval, Sandbox pass or merge approval.

### Execution snapshot — 2026-10-24, corrected full pytest complete

This dated snapshot supersedes earlier pending-implementation/full-pytest status prose only; owner conditions, plans, council findings and remaining gates are unchanged. Developer maintains the detailed [execution index](EXECUTION.md). The PM read the raw RESULT/step/stdout/source-manifest evidence below before recording these outcomes.

- Approved initial runtime/configuration/docs changes and **only the three owner-named CI `pip check` additions** are applied. QA first recorded the expected red, then focused verification passed **23/23**, exit 0 (`artifacts/python315_migration/qa/focused.RESULT.json`). Independent fresh development/build environments passed both-manifest installation/checks; no dependency/tool pin changed.
- Preparation completed with lockfile installation, CSS content identity preserved after line-ending normalization, private Chromium installation, `tsc`, pinned Pyright **0 errors / 0 warnings / 0 information diagnostics**, blocking baseline diff and inventory regeneration/check passing. Raw initial preparation `FAIL: Compiled CSS drifted` is retained; `validation/preparation-remainder/RESULT.json` records the content/line-ending proof and actual successful analysis/checks. This is measured analyzer output, not an inference from zero baseline allowance.
- **First full pytest attempt failed:** **6143 passed, 14 failed, 2 skipped**, raw exit 1 (`artifacts/python315_migration/validation/full-pytest-1/RESULT.json`). Manager/developer diagnosis identified 12 Bash-probe failures from the WSL stub selection, one CSS index/stat issue and one runner/runtime DB-path collision. Process-only runner corrections and index-stat refresh changed no production source or test assertions; all 14 focused cases then passed, exit 0, in 13.45s (`validation/runner-correction/focused.{stdout,exit}.txt`). The failed attempt remains part of the evidence.
- **Corrected full pytest attempt passed:** **6157 passed, 2 skipped in 978.62s**, raw exit **0**. [Full result](../../artifacts/python315_migration/validation/full-pytest-2/RESULT.json), raw stdout, command step and JUnit are retained under `artifacts/python315_migration/validation/full-pytest-2/`. Actual invocation used task `.venv` Python, `pytest tests/ -q -n 4 --dist loadfile`, and a private JUnit/runtime path. Fresh collection and JUnit accounting both contain **6159 identities**, exact match, no missing/unexpected cases. The result's source comparison is **unchanged**. Completion time was **2026-10-23T22:04:51.949782+00:00** (2026-10-24 01:04 in Asia/Jerusalem).
- Both full attempts bind to recorded source-manifest SHA-256 **`7efe90cb382f79d6ec356bfc4ba7c83c52c4a7529de028696352ca7c6eac6485`**. That manifest includes this planning document, whose prior captured hash was **`5880532e1f9ca7f8677d3bf12b22e35236dfee5c4c645e20d1a0ee7ac4937fd6`**. This subsequent PM evidence-only update does not retroactively change the tested manifest. Later campaign manifests must capture or explicitly account for this documentation change; base HEAD is not the implementation revision.
- **Pending:** canonical no-argument full seeded Chromium campaign; canonical Windows build/host bootloader; saved-data/Unicode acceptance beyond focused tests; native exact-head CI/dry-run evidence; required independent diff reviews; Gate 2 before first push; owner-enabled no-Python Sandbox **before merge**; final owner diff/named-PR/head merge approval; coordinated post-merge owner main `.venv` handoff. Passing pytest is not full acceptance, and two recorded skips are not asserted to have executed.

**Current boundary after snapshot:** Local full pytest has passed with retained failed-attempt history and source accounting. No first-push Gate 2, Sandbox pass, PR publication or merge approval is recorded. This PM write changes only `PLANNING.md`.

### Direct owner sequencing and merge amendment — 2026-10-24

**Owner instruction (verbatim)**

> Approved. Before merge, also require the exact-head native Windows CI E2E/visual jobs to pass, not just Linux. After I reboot to enable Sandbox, re-run the full local E2E once and record the result. Open a separate issue for the TIME_WAIT/10055 socket exhaustion; don't fix it in #564.

**Approval scope:** This direct response approves the pending sequencing exception: required independent diff review may proceed despite the failed local Windows full-E2E gate. It does **not** declare that local gate passed, supply a reviewer pass, approve Gate 2/first push, or authorize merge. The required independent `code-reviewer` and `unslop-reviewer` still must run. The earlier **Gate 2 once before first push** and separate owner final-diff/named-PR/head merge review remain pending.

**Binding execution conditions**

- Before merge, require the full native Linux Chromium evidence **and exact-head native Windows CI E2E and visual jobs to pass**. Linux green alone, host diagnostics, bootloader smoke, or a partial local campaign cannot discharge the Windows CI requirement. Record actual job/run identities, final head SHA, exercised test identities and results; do not infer unexecuted coverage or Windows success.
- The owner will reboot to enable Windows Sandbox separately. **After that reboot, run the full canonical local E2E once and record its result**, with normal functional/visual seed partition, actual accounting and source binding. A later result must preserve prior failed/partial attempts; no local full-E2E or Sandbox success is asserted by this amendment.
- The clean **no-installed-Python Sandbox direct-executable test must still pass before merge**. Owner enablement/reboot and post-reboot E2E execution are distinct from the Sandbox executable acceptance proof. Main `.venv` remains the owner's coordinated post-merge rebuild.
- The manager is directly authorized to open a **separate GitHub issue for TIME_WAIT/10055 socket exhaustion**. Keep the failure evidence and issue link in the execution record when created. **Do not fix socket exhaustion in #564** or silently broaden migration code, tests or runtime policy to address it.

**Documentation-only campaign delta:** This amendment was appended while the developer's separately reported visual diagnostic campaign was running. Immediately before this write, `PLANNING.md` SHA-256 was **`B6E943A0C21F0D766B0CCCA9C2021B2A475EE9E6E62DB193D6F9C4D46C8DC339`**. Preserve existing campaign source manifests; record this intentional planning-only change separately instead of retroactively rebinding test evidence. No production/test/config file changed in this PM write. The manager/developer receive the resulting document hash for their campaign accounting.

**Current boundary:** Sequencing exception approved with the above conditions. Required reviews, Gate 2/first push, exact-head native CI, post-reboot full local E2E result, Sandbox-before-merge proof and final merge approval remain outstanding. No Windows/local/Sandbox pass is recorded here.

### Pre-review execution snapshot — 2026-10-24

This concise snapshot supersedes older pending-campaign prose while preserving every owner instruction and failed attempt. Detailed execution evidence remains in [EXECUTION.md](EXECUTION.md). PM inspected the named raw results and provenance reconciliation before this append; no test, source, baseline, timeout or dependency-pin change is made here.

| Evidence | Recorded outcome and limit |
|---|---|
| Full pytest | **6157 passed, 2 skipped**, exit 0; exact **6159** collected/JUnit identities and unchanged tested source. Prior 14-failure attempt and process-only correction evidence remain recorded above. |
| Normal 3.15 canonical functional campaigns | `validation/full-e2e-1/RESULT.json`: **582 passed / 4 failed**; `full-e2e-2/RESULT.json`: **584 / 2**. Each completed the same **586** functional identities once, exit 1; canonical runner stopped before the **100** visual identities. Neither is a full-E2E pass. |
| Exact unmodified 3.14 base functional control | `validation/full-e2e-base-314-1/RESULT.json`: **584 passed / 2 failed** over the same 586 identities, once each, exit 1. Control evidence does not turn the migration campaign green. |
| CPU/job-affinity experiment | `validation/full-e2e-3-job-affinity-1/RESULT.json`: **ABORTED_FAILED_MITIGATION_PARTIAL**, **339 passed / 4 failed** among **343** completed reports; **243** expected functional identities unreported. `full_gate_credit: false`; allocation errors persisted and separate timing/input-validation failures were observed. No completed/full-gate claim or socket fix is credited. |
| Normal 3.15 visual diagnostic | Correctly seeded **100** identities, **98 passed / 2 failed**, exit 1: workout-plan mobile dark **1503** differing pixels and tablet dark **2805**. This diagnostic is separate from the failed canonical functional campaigns and cannot be combined into a full pass. |
| Exact 3.14 base visual control | Same 100 identities, **98 passed / 2 failed**, exit 1: workout-log desktop light **3892** differing pixels and backup tablet dark **764861**. **No shared failed keys** with 3.15; the hypothesis that the same two visual failures are inherited is **not established**. No pixel root cause or migration-independence label is asserted. See `validation/visual-attribution-comparison.json`. |
| Canonical Windows build / real bootloader | `validation/build-and-bootloader-1/RESULT.json`: **PASS**, all recorded build/staging/check/smoke commands exit 0, actual bootloader port 5123 with no skip flags. Executable SHA-256 **`0abc23fb4b43c2f9e022034f9adb6a93f6780fb0923963ef07ec0ef016e7d35e`**. This is host evidence, **not** clean no-Python Sandbox acceptance. |
| Source/frozen saved-data and Unicode | `unicode/source/RESULT.json` and `unicode/frozen/RESULT.json`: **PASS** for actual initialized old-data startup, strict UTF-8 JSON, Unicode plan/backup metadata, Excel text/numbers, real process restarts, backup/restore, private paths/logs/startup snapshots and original-byte preservation. |
| 3.14 rollback rehearsal | `validation/rollback-314-1/ROLLBACK.RESULT.json`: **PASS** against a private copy of 3.15-written fixture data; retained exact-base source/3.14 reads and restores Unicode backup/plan values, exports workbook, restarts and preserves original 3.15 DB bytes. No owner data or shared environment used. |
| Types/inventory/audits and tooling | Actual pyright/tsc/baseline/inventory passes remain recorded above. `validation/local-tools-1` records passing pip-audit and blocking flake8, but its raw overall result **FAIL** at Vulture exit 3 is preserved; first comparison also failed. `local-tools-remainder-2/RESULT.json` records passing npm high-severity policy and isolated supplementary-tool compatibility, with **19 identical qualified-diagnostic/enclosing-AST Vulture findings on current and exact base**, both exit 3. No new allowlist, pin change or blanket clean-tool claim. |

**Source accounting:** Migration browser/build campaigns bind to source manifest **`80dfecadd9986881697cb5a9be8d6205ae4dd3c187e9dd555fc9f19b9f236c30`**. The 3.15 visual raw result accurately says `source_unchanged: false` because of the previously authorized owner-amendment append to this document. Its `provenance-reconciliation.json` records only that exact planning hash delta, **1871 stable production/test/config/non-evidence files**, stable manifest **`6e868c016ed1b19fc1377688d455da346f550f5f45930142a0bdfe758a0bbb90`**, and unchanged visual **FAIL**. Preserve these original manifests; this later PM evidence append and developer execution-ledger updates require new review/staging manifests and do not retroactively relabel prior runs.

**Socket follow-up:** Manager created and read-verified the separately authorized open [issue #565 — TIME_WAIT/10055 socket exhaustion](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/565). Creating that tracking issue is neither Gate 2 approval nor implementation publication. Socket exhaustion remains outside #564's fix scope; no snapshots, assertions, timeouts or pins were changed to force green.

**Outstanding owner-condition clarification:** The owner's native-Windows E2E/visual-before-merge condition remains binding. Existing native Windows `visual-windows` covers 66 visual tests; current functional CI is on Linux. The manager asked whether the intended proof is existing Windows visual/build/test jobs or a new native Windows functional job; **no answer is recorded** and no new job edit is authorized by inference. Exact final-head native Linux Chromium and the clarified native Windows requirements must be satisfied before merge.

**Review and delivery boundary:** Under the direct sequencing exception, proceed to required independent **code review, then unslop review**; neither has run or passed at this snapshot. Gate 2 is still required **once before first push**. After the owner reboots/enables Sandbox, run the **full canonical local E2E once and record the result**; clean no-Python Sandbox executable proof must pass **before merge**. Native CI/dry-run evidence, final owner diff review/named-PR/head merge approval and coordinated post-merge owner main `.venv` rebuild remain outstanding. No complete local full-E2E, Windows CI or Sandbox pass, Gate 2, push/PR publication or merge is asserted. PM freezes this document after the append for staging/review.

### Independent review completion snapshot — 2026-10-24

The required independent **code review, then unslop review both completed PASS, with no actionable findings**, under the owner's recorded sequencing exception. Both reviewed the same staged tree **`da351225324d6237ae45f2e6bc324c8ebcf304c8`** against base **`ae5ec18c3293df302393b28195d8e12ceb92d176`**. PM read the verbatim verdicts: [code review](../../artifacts/python315_migration/reviews/code-review.md), SHA-256 **`c76db05050fedfe4d505c33a93e1752b4d6df9298505f3f1d360005f1d6f67da`**, and [unslop review](../../artifacts/python315_migration/reviews/unslop-review.md), SHA-256 **`51cfba29a8bc678b443f11b230b302ef3bd899c7879c8f5df3a165a2fa00ff35`**. Each reviewer explicitly withheld owner approval and merge clearance; prior failed/partial browser attempts remain failures.

This evidence-only append follows the reviewed tree. Preserve its original source proof and artifact manifest; the final Gate 2 proof must account separately for this planning append and the developer's execution-record update. No production/test/config change, dependency/tool pin change or socket fix is authorized or recorded here; socket work remains in separate issue #565.

**Delivery boundary:** Gate 2 remains unapproved; no commit or push has occurred. The native Windows functional-job clarification remains unanswered. Before merge, require exact-final-head native Linux Chromium and the clarified native Windows E2E/visual evidence, **one full canonical local E2E run after the owner's Sandbox-enabling reboot with its actual result recorded**, actual clean no-Python Sandbox **PASS**, and the owner's final-diff/named-PR/head merge approval. None of those pending conditions is discharged by the reviewer passes. The owner retains the coordinated post-merge main `.venv` rebuild.

### Direct owner publication approval and Windows clarification — 2026-10-24

**Gate 2 reply (verbatim)**

> :Gate 2 approved. In the first follow-up commit on the PR (in scope, no re-approval needed): (1) change the stale-venv message in START.bat/build_exe.bat to tell users to rename the old venv folder and rerun; (2) remove the "private extracted PythonCore runtime" wording from README, QUICK_START and ADR-013; (3) make the pyright-baseline.json note identical to the text pyright_baseline_diff.py generates.

The approval names finished staged tree **`9a10e87937fe39ca6ac661b023e5738b584b4537`**. That exact tree was committed as **`7e86c0546d80784ae3e8262067bd398f7187752a`**, pushed, and published in draft [PR #566](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/566), against base **`ae5ec18c3293df302393b28195d8e12ceb92d176`**. This supersedes older pending-Gate-2/publication status above. The three requested changes belong in the **first follow-up commit on that PR**, with applicable verification and accurate evidence; they require no repeated Gate 2 approval. No dependency-pin change or socket-exhaustion fix is authorized.

**Native Windows scope clarification (verbatim)**

> Require existing Windows jobs (Recommended)

The owner selected the existing native Windows visual/build/test jobs, alongside the required post-reboot full local E2E run. Do not add a native Windows functional E2E CI job for #564. Before merge, require **exact-final-head native Linux Chromium and all existing Windows visual/build/test jobs to pass**, record **one full canonical local E2E run after the owner's Sandbox-enabling reboot with its actual result**, obtain actual clean no-Python Sandbox **PASS**, and obtain the owner's final-diff review and **named-PR/head merge approval**. Publication approval supplies none of those results and does not authorize merge. The owner retains the coordinated post-merge main `.venv` rebuild; socket work remains in separate issue #565.
