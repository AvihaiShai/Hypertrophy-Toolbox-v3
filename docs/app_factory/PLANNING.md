# Plan Review — WS3 Application factory (`create_app()` / `init_runtime()`)

| Field | Value |
|---|---|
| Status | **Gate 0 signed by the owner 2026-10-20. Council complete (rev 4, 2026-10-20): Plan v1, three independent reviews (all sound-with-changes, none blocking), response matrix and Plan v2 written. Gate 1 disposed 2026-10-20 (rev 5) by a delegated AI-team decision adopted under the owner's direct instruction — not an owner signature (Plan v2 §V19).** Implementation is authorized by the owner's 2026-10-20 instruction, conditional on that favorable decision and S0 readiness (§V19 GA-13). Gate 2 and any merge confirmation are owner-only and not given. |
| Authors | Rev 1: Fable (Claude Code), 2026-10-19. Rev 2: `product-manager` agent `af7285ca1164caf98`, 2026-10-20. Rev 3 (Gate 0 record + Plan v1): a fresh `product-manager` `a9259355287e3c511` in manager session `hypertrophy-toolbox-v3-main-c3`, 2026-10-20 (ID supplied by the manager; see Agent provenance). Rev 4 (Reviewer findings, response matrix, Plan v2): the same `a9259355287e3c511`, resumed via `SendMessage`. Rev 5 (§V19 delegated Gate 1 record): a fresh `product-manager` in manager session `hypertrophy-toolbox-v3-main-53`; ID recorded by the manager after return (see Agent provenance). |
| Source of truth | This file for WS3 requirements. Direction: `docs/project_direction/AGREED_PLAN.md` §4 WS3, §6 WS3 row and **§11** (the operative Q8(a)/Q9 dispositions; §5's Q8/Q9 owner cells are blank and §5's preamble defers to §11). AGREED_PLAN is untracked (working tree only). Tracked corroboration on `origin/main` `f3adacf1`: `docs/MASTER_HANDOVER.md` Current State → *Holds in force* → *Sequencing*. |
| Governing baseline | `origin/main` **`f3adacf1c1b48cc6e2c7ca9ac900e3294b3bae2d`** (`git ls-remote`, 2026-10-20, no fetch), read from a byte-exact `git archive` snapshot; nothing executed. F1–F10 below are the rev 1 record measured on `e486e3b5`; their status at `f3adacf1` is in the re-verification table. |
| Planning size | **Large** (cross-cutting: `app.py`, `app_launcher.py`, new `utils/` module, `tests/conftest.py`, several tests, agent-config docs) — `docs/ai_workflow/QUALITY_GATE.md` plan-stage routing: Gate 0 → `/council-plan` → Gate 1 → implementation. |
| Tracking | Untracked local file. Q9 (§11) concerns `AGREED_PLAN.md` only and does not decide this file's commit path; that is settled with the WS3 change. Not committed by this session. Rev 5: per §V19 GA-12 the file is to be committed in the WS3 PR as commit C0; the rev 5 author does not commit it. |

### Revision history

| Rev | Date | Author (agent ID) | Change | Inputs |
|---|---|---|---|---|
| 1 | 2026-10-19 | Fable (Claude Code) | Section 0 drafted at `e486e3b5`; stopped at Gate 0. | Owner request 2026-10-19 (quoted below). |
| 2 | 2026-10-20 | `product-manager` `af7285ca1164caf98` (spawned 2026-10-20 by the manager session) | Section 0 revised via `/requirements`: governing request added; Q-WS3-1 and Q9 recorded as existing decisions; Q-WS3-2…6 converted to a recommendation table; facts re-verified at `f3adacf1`; assumptions and acceptance criteria corrected; Gate 0 block consolidated. F1–F10 preserved verbatim. | Owner request 2026-10-20; read-only investigation by `senior-developer` `a003588583f306f4e` (spawned 2026-10-20 by the manager session), report at `C:\Users\aviha\AppData\Local\Temp\claude\d--development-Hypertrophy-Toolbox-v3-main\12105a05-de2f-4197-8a6d-907a42037005\scratchpad\ws3-senior-dev-findings-f3adacf1.md`. Rev 1 preimage: `C:\Users\aviha\AppData\Local\Temp\claude\d--development-Hypertrophy-Toolbox-v3-main\12105a05-de2f-4197-8a6d-907a42037005\scratchpad\PLANNING.preimage-20261020.md`, SHA-256 `bc7b61c06b51c9e3eefa206c4636eed76b08e35e32fdd95f92ee17060a327df4` (computed by the manager with `sha256sum` on the file before the rev 2 edit). Durable copies of the preimage, the senior-developer report and the owner request are kept under the gitignored `artifacts/ws3-app-factory-20261020/` with the same filenames. Rev 2 correction (same day): Q-WS3-4 sub-choice 4d added to resolve rule (iii) against the module-scoped `real_app_client`; AC3/AC6 adjusted. |
| 3 | 2026-10-20 | Fresh `product-manager` `a9259355287e3c511` in manager session `hypertrophy-toolbox-v3-main-c3` (ID returned to the manager when the Plan v1 call ended, and supplied back by it) | Gate 0 recorded (owner reply quoted verbatim in the Gate 0 block; three sign-off boxes ticked; A1–A13 marked as accepted planning assumptions). Plan v1 written below Section 0 via `/council-plan` step 1. Section 0 otherwise unchanged. | Owner Gate 0 reply, 2026-10-20, pasted into manager session `hypertrophy-toolbox-v3-main-c3`; durable copy `artifacts/ws3-app-factory-20261020/ws3-owner-gate0-council-request-20261020.md`. Preimage of this revision: `artifacts/ws3-app-factory-20261020/PLANNING.preimage-gate0-rev2-0a54ec8d.md` (SHA-256 `0a54ec8dd26d1115a1454d126226dfac1ca3cd04e82e188d68ae737e450bfec6`, supplied by the manager). The rev 3 author had no shell and could not recompute the hash; it confirmed the live file matched the preimage by line count (489), anchored-line positions and a character-class count before editing. **Planning-file handoff:** the previous owner of this file, session `12105a05` (now named `hypertrophy-toolbox-v3-main-81`), replied on 2026-10-20 (relayed by the manager): "Released … I have no pending edits … The last write I know of is SHA-256 0a54ec8d…bfec6 … I'll make no further edits." It also confirmed that `af7285ca1164caf98` (Section 0 `product-manager`) and `a003588583f306f4e` (`senior-developer`) were its in-process subagents. **Citation correction (same day):** the manager withdrew its brief's claim that the shared working tree was a valid read source; its `HEAD` `85e23725` is not on `origin/main`. Plan v1's citations were re-checked against the byte-exact snapshot `artifacts/ws3-app-factory-20261020/src-f3adacf1/`, and three citations from uncommitted shared-checkout edits were corrected (Plan v1 source note). The design is unchanged apart from what those corrections force: an S1 baseline run, and `unslop-reviewer` inside `/verify-and-polish`. |
| 4 | 2026-10-20 | `product-manager` `a9259355287e3c511`, resumed by the manager via `SendMessage` (same agent as rev 3) | Reviewer findings recorded verbatim (AR-1…4, TS-1…13, PR-1…5). Response matrix written: 22 rows; 20 accept, 1 accept in part with an owner choice (PR-1), 1 reviewer disagreement for owner decision (PR-2). Self-contained Plan v2 written, with AC refinements R-1…R-5 and the Gate 1 decision list (§V18). Plan v1 kept unchanged. Section 0 unchanged apart from this row and the header Status/Authors rows. | Reviewer reports under `artifacts/ws3-app-factory-20261020/` (`council-architecture-a484bd1ac77e7e978.md`, `council-test-strategist-af3d581707e375d82.md`, `council-product-risk-a12256eb7f65a549a.md`), all against the frozen `PLANNING.plan-v1-as-reviewed.md` (SHA-256 `950e64f5…696c`, hashed by the manager). The manager's proposed dispositions and its premise checks against `src-f3adacf1` were taken as input; the `product-manager` re-read every report directly. |
| 5 | 2026-10-20 | Fresh `product-manager` in manager session `hypertrophy-toolbox-v3-main-53` (ID recorded by the manager after return; see Agent provenance) | Delegated Gate 1 record added as Plan v2 §V19: owner delegation quoted verbatim; §V18 items 1–7 disposed (RP-4 and RP-6 owner-direct; RP-7 not adopted); binding amendments GA-1…GA-14; dissent. Agent provenance sub-block appended; Sign-off updated (Gate 1 by delegated decision, not owner signature; Gate 2 line added). Plan v1, matrix and §V1–§V18 unchanged; Section 0 unchanged apart from this row and the header Status/Authors/Tracking rows. | `artifacts/ws3-impl-20261020/gate1-team/DELEGATED_GATE1_DISPOSITION.md` and the three adviser reports beside it; `artifacts/ws3-impl-20261020/owner-request-impl-20261020.md`. Preimage: this file as copied into the clone, SHA-256 `cc8dcbe98249dd0348eea0d1e827cf988ac14b37c8c0f867dc968d3af85202e6` (recorded by the manager; the rev 5 author has no shell and confirmed only the line count, 1,811). |

The scratchpad paths are session-local. The facts this section relies on are restated here with `path:line`; the report is cited for detail only. Report cross-references "B.7(n)" mean B.6(n) (manager note in the report).

---

## Section 0 — Requirements Brief

### Raw requests

**Governing request** (verbatim, owner, 2026-10-20, pasted into the manager session; quoted in full)

> Take ownership of WS3 — application factory — using multiple agents.
>
> Advance the existing work through:
> Q-WS3-2…6 recommendations → owner Gate 0 → council → owner Gate 1.
>
> This authorizes investigation and planning. It does not sign either gate or authorize implementation. Complete the work needed for each approval before stopping there.
>
> 1. Read the existing context
>
> Read CLAUDE.md first, then:
> - docs/app_factory/PLANNING.md
> - docs/project_direction/AGREED_PLAN.md, especially §4 WS3 and §11
> - docs/MASTER_HANDOVER.md for applicable current state
> - docs/ai_workflow/QUALITY_GATE.md
> - docs/ai_workflow/AUTONOMY.md
> - docs/ai_workflow/PARALLEL_WORKFLOW.md
> - docs/ai_workflow/WORKSTREAM_OWNERSHIP.md and applicable live claims
> - docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md
> - .claude/commands/council-plan.md
> - The charters of the agents you use
>
> Continue the existing WS3 artifact. Preserve its evidence, history and explicit owner decisions. Do not create a competing plan or copy unrelated historical material into it.
>
> Reconcile stale status before asking questions:
> - AGREED_PLAN.md §11 already resolves Q8(a) for WS3: independently isolated implementation need not wait for PREVENTION_COMPLETE or recovery completion, but WS3’s own gates remain mandatory.
> - Record that disposition against Q-WS3-1 with its source and isolation conditions. Do not ask me to decide it again.
> - Q9 is also selected in §11; its separate publication work is not a prerequisite for WS3.
> - WS1b+, WS2, queue consolidation and broad archiving are not prerequisites.
>
> 2. Use these agent responsibilities
>
> Act as the read-only manager and orchestrator.
>
> Before Gate 0:
> - product-manager owns all edits to docs/app_factory/PLANNING.md and prepares the revised Section 0 through /requirements.
> - senior-developer performs a read-only technical investigation of the current source and supplies evidence-backed recommendations. No implementation, application imports, server starts, tests, collectors or runtime-database access in this phase.
>
> Let their independent reading proceed in parallel, then have the product-manager incorporate the technical findings. Only the product-manager edits the planning document.
>
> After Gate 0:
> - Resume the same product-manager to draft Plan v1.
> - Run architecture-reviewer, test-strategist and product-risk-reviewer in parallel, independently, against the actual artifact.
> - Resume the product-manager for the response matrix and Plan v2.
>
> Record real agent IDs, supply the PM its ID for provenance, and preserve continuity where available. Report missing IDs or unavailable reviewers honestly. A failed or missing review is incomplete, never a clean verdict.
>
> 3. Prepare concrete recommendations for Q-WS3-2…6
>
> Do not merely repeat the existing questions. For each, provide:
> - Recommended answer.
> - Evidence and affected callers.
> - Behavior and compatibility consequences.
> - Required acceptance-criterion changes.
> - Any remaining owner choice.
>
> Cover:
> - Q-WS3-2: explicit, idempotent logging versus a deliberately narrowed import-side-effect promise. Address transitive get_logger() calls, standalone scripts and the currently unattached request hooks. Treat enabling or deleting those hooks as a distinct decision.
> - Q-WS3-3: retain module-level app or require factory callers. Account for existing imports and Flask CLI discovery.
> - Q-WS3-4: repeated init_runtime() behavior, startup snapshots, failed initialization/retry, and what happens if the requested database/runtime changes within one process.
> - Q-WS3-5: every flask run caller and its explicit initialization path; justify any proposed retirement.
> - Q-WS3-6: init_runtime() module boundary while preserving utils → no routes imports.
>
> Check recommendations together for consistency. For example, retaining app = create_app() must not silently violate the selected import-side-effect promise.
>
> Verify the existing caller inventory against a clearly identified source revision. Separate measured facts from assumptions; do not present older line numbers or repository state as freshly verified.
>
> 4. Produce a reviewable Gate 0 package
>
> Have the product-manager update Section 0 with:
> - The decision table above.
> - Corrected assumptions, including any mismatched assumption references.
> - Observable acceptance criteria consistent with the recommended answers.
> - Explicit scope and non-goals.
> - Calculation surface: none.
> - Clear separation between existing decisions and recommendations awaiting my acceptance.
>
> Preserve:
> - Production initialization order and fresh-seed skip behavior.
> - DB_FILE / HT_RUNTIME_DIR precedence and explicit process-global configuration.
> - Unseeded test schemas.
> - All 13 blueprints, middleware, handlers, filters, context processors and static caching.
> - The real /erase-data confirmation, backup, response and failure contracts.
> - Source and packaged launch behavior.
>
> Stop at Gate 0 with the completed artifact and one consolidated approval request covering the recommendations, acceptance criteria and assumptions. Explain that this pause is required by QUALITY_GATE.md and /requirements. Do not draft Plan v1 before approval.
>
> 5. After explicit Gate 0 approval, run the council
>
> Follow /council-plan exactly:
> - Product-manager writes Plan v1.
> - The three independent reviewers read it directly.
> - Preserve their findings verbatim.
> - Propose a disposition for every finding.
> - Product-manager writes the response matrix and Plan v2.
> - Resolve blockers and rerun affected reviewers when substantive revisions require it.
> - Surface unresolved reviewer disagreements for my decision.
>
> Plan v2 must specify:
> - File manifest, boundaries, sequencing and agent ownership.
> - Configuration/logging/factory/runtime initialization order.
> - Repeated factory and runtime behavior.
> - Launcher, fixture and import-caller migration.
> - Compatibility changes and rollback approach.
> - Acceptance-criterion-to-test mapping.
> - Full pytest + Chromium, packaged-Windows smoke, fresh-process import checks, initialization-order checks, first-install/upgrade and backup/restore coverage.
> - Applicable pyright, test-inventory and workflow-contract checks.
> - Independent implementation reviewers derived from the required gate union.
>
> 6. Preserve isolation and scope
>
> The §11 WS3 ruling requires a standalone clone with independent Git storage and private dependencies, DB/runtime, backups, logs, temp, cache and bytecode paths for implementation. A linked worktree is not equivalent under this ruling.
>
> Check applicable live freezes and ownership constraints. Preserve recovery storage, pending drafts, branches, worktrees and environments. Coordinate shared-file edits and landing order.
>
> Do not include Waitress, service extraction, dependency regrouping, calculation changes, schema changes, CI redesign, broad documentation cleanup or recovery operations.
>
> 7. Stop at Gate 1
>
> Present:
> - The revised planning artifact.
> - Proposed final decisions and remaining owner choices.
> - Council findings and dispositions.
> - Agent provenance and any evidence gaps.
> - Implementation scope, validation requirements and readiness.
> - The exact Gate 1 approval needed.
>
> Do not implement, publish, push or merge under this planning request. Keep updates concise and continue independently until the next actual owner gate.

**Original request** (verbatim, owner, 2026-10-19 — step 3 of a three-step instruction; steps 1–2 concerned the WS1a merge and `AGREED_PLAN.md`; retained from rev 1)

> 3. Prepare WS3 — analysis and requirements only
>
> Follow A9: the next code candidate is the application factory. WS1b+, WS2, queue consolidation, and broad archiving are not prerequisites.
>
> Inspect the current remote-main source without importing the application, starting servers, or touching runtime databases. Prepare a concise WS3 requirements/design proposal covering:
>
> - Every import and launch caller, including the packaged launcher and affected tests.
> - DB_FILE / HT_RUNTIME_DIR precedence and process-global configuration.
> - Empty test schemas versus production runtime initialization.
> - Transitive logging side effects from module-level get_logger() calls.
> - Explicit initialization order, repeated create_app() behavior, and logger idempotence.
> - Preservation of all 13 blueprints, handlers, filters, static caching, and the real /erase-data confirmation/backup contract.
> - Proposed file boundaries, compatibility risks, and validation against §4's acceptance criteria.
>
> Identify the exact Q8(a) sequencing decision needed for WS3 implementation. Do not infer a hold release.
>
> Follow the existing Gate 0 → council-reviewed plan → Gate 1 sequence, stopping at the next owner gate. This authorizes preparatory analysis, not WS3 implementation or approval.

### Problem

`import app` is the application's only construction path. It runs the whole runtime initialization at module level, against whatever database path the process environment resolves at that moment: legacy-database migration, catalog-seed bootstrap, schema initializers, catalog upgrade and a startup backup. Every importer pays for those side effects and risks them. That includes the packaged launcher, three in-process test importers (`tests/conftest.py`, `test_static_cache_policy.py`, the dead `test_pattern_coverage.py` fixture), two subprocess importers (`test_real_app_db_isolation.py`, `test_catalog_seed_bootstrap.py`), the packaged smoke script's own process, a documented developer command (`docs/product/README.md:191`) and both `flask run` callers.

Importing the real app is unsafe in tests, so `tests/conftest.py` builds a second, hand-maintained Flask application that is not the production object. It has its own 13 blueprint registrations, one copied filter, a guard-less `/erase-data` and none of the middleware, handlers or cache policy. The "register in both `app.py` and `conftest.py`" rule exists only to keep that twin in step.

The goal fixed by `AGREED_PLAN.md` §4 WS3 is that importing `app` performs no filesystem or database work, and that production, launcher and tests build the application through one path. This revision recommends narrowing the "no filesystem work" half in writing (Q-WS3-2): importing `app` performs no database or data-directory work, but the logging directory and handlers are still created on first `get_logger()`.

### Existing decisions — recorded, NOT awaiting owner acceptance

| ID | Decision | Source and provenance | Effect on WS3 |
|---|---|---|---|
| **ED-1** (= **Q-WS3-1**, AGREED_PLAN Q8(a) for WS3) | §11 row "Q8(a), WS3", verbatim: *"Independently isolated implementation need not wait for `PREVENTION_COMPLETE` or recovery completion. Complete the factory design and its Gate 0, council and Gate 1 first; then use the conditions below."* | `docs/project_direction/AGREED_PLAN.md` §11 "Delegated direction decisions — 2026-10-19". A direction decision adopted 2026-10-19 by the primary session under the owner's delegation, with advisers `/root/hold_classification`, `/root/memory_binding` and `/root/direction_queue`. §11 states it is not an owner Gate 0/Gate 1 signature. Tracked corroboration: `MASTER_HANDOVER.md` @`f3adacf1` *Holds in force → Sequencing*. Owner restated it 2026-10-20: "Record that disposition… Do not ask me to decide it again." | Design, Gate 0, council and Gate 1 proceed now. Implementation is eligible only after Gate 1 **and** under IC-1…IC-8. Operation A status and the B–E sequence are unchanged. |
| **ED-2** (Q9) | §11: publish `AGREED_PLAN.md` at its current path through a separate bounded documentation change. | AGREED_PLAN §11; owner 2026-10-20: "its separate publication work is not a prerequisite for WS3." | Not a WS3 prerequisite. Does not decide this file's commit path. |
| **ED-3** | WS1b+, WS2, queue consolidation and broad archiving are not prerequisites. | AGREED_PLAN A9 / §4; owner 2026-10-19 and 2026-10-20. | None of them gates WS3. |
| **ED-4** | Preservation list (owner, 2026-10-20, verbatim in the governing request §4). | Owner. | Binding requirement; traced to ACs in the preservation table below. |
| **ED-5** | Exclusions: "Do not include Waitress, service extraction, dependency regrouping, calculation changes, schema changes, CI redesign, broad documentation cleanup or recovery operations." | Owner, 2026-10-20 §6. | Binding non-goals. |

**ED-1 isolation conditions.** Source: the §11 "Q8(a) boundaries" paragraph, verbatim:

> This is a prospective scheduling classification for these three workstreams, not a claim that the previous hold was absent. Use a standalone clone with independent Git storage, no alternates/hardlinks to recovery storage, and private dependencies, DB/runtime, backup, log, temp, cache and bytecode paths. A linked worktree does not provide that isolation. Coordinate shared-file edits and landing order, including `app.py` and `CLAUDE.md`. Check applicable live freezes and blocked-recovery states before work; no tests or collectors run during a live preservation/destructive freeze. Preserve recovery sources, pending drafts, branches, worktrees and environments. This decision leaves Operation A's status and B–E's sequence, approvals and safety contracts unchanged and authorizes no recovery action.

The same conditions as a checklist. They are implementation-readiness preconditions, not acceptance criteria and not Gate 0 questions:

- [ ] **IC-1** Standalone clone with independent Git storage; no alternates or hardlinks to recovery storage.
- [ ] **IC-2** Private dependencies, DB/runtime, backup, log, temp, cache and bytecode paths.
- [ ] **IC-3** No linked worktree is used in its place.
- [ ] **IC-4** Shared-file edits and landing order are coordinated. This covers `app.py`, root and folder `CLAUDE.md`, and everything under `.claude/**` (`WORKSTREAM_OWNERSHIP.md` rule 4 @`f3adacf1`).
- [ ] **IC-5** Live freezes and blocked-recovery states are checked before any work.
- [ ] **IC-6** No tests or collectors run during a live preservation or destructive freeze.
- [ ] **IC-7** Recovery sources, pending drafts, branches, worktrees and environments are preserved.
- [ ] **IC-8** No recovery action is taken; Operation A status and B–E are unchanged.

**Implementation-readiness preconditions** (follow from ED-1 and the live state; raised again at Gate 1, not asked now)

| ID | Precondition | Evidence |
|---|---|---|
| RP-1 | The implementation manager session is launched inside an **owner-created standalone clone**. Subagents work in their manager's checkout. `scripts/new-worktree.ps1` creates linked worktrees, which ED-1 rules out. | `PARALLEL_WORKFLOW.md` *Manager-session ownership* and *Python environment* ("owner-created standalone clone", cleanup plan §1.3); `AUTONOMY.md` *Workflow roles*. |
| RP-2 | Per-edit coordination with the session holding uncommitted edits in the shared checkout to `CLAUDE.md`, `.claude/agents/{architecture-reviewer,code-reviewer,test-strategist}.md` and other `.claude/**` files. These overlap the WS3 doc targets. | Shared-checkout `git status` at session start; IC-4. |
| RP-3 | `Packaged Smoke (Windows bootloader, non-required)` is not branch-protected. Its green result must be observed explicitly. | `_packaged-windows.yml:106`; QUALITY_GATE CI job naming. |
| RP-4 | The Gate 1 approval names the move of all 13 `register_blueprint` calls into `create_app()` explicitly. AUTONOMY lists "changes to `app.py` blueprint registration" as needing explicit confirmation. | `docs/ai_workflow/AUTONOMY.md:18,144` @`f3adacf1`. |
| RP-5 | `docs/test_inventory/` is regenerated only in a clone with no untracked or gitignored `.md` in a globbed surface directory. | QUALITY_GATE *Blocking CI gates* (`Test Inventory Drift`). |

### Measured facts

**Rev 1 record (baseline `e486e3b5`; preserved verbatim; corrections at `f3adacf1` follow in the re-verification table)**

**F1 — Import callers of `app`.**

| Caller | How | Depends on today's import-time startup? |
|---|---|---|
| `app_launcher.py:main()` (packaged bootloader entry, `Hypertrophy-Toolbox.spec:40`) | `from app import app`; then `app.run(host='127.0.0.1', port=runtime_port(), debug=False, threaded=True, use_reloader=False)`; sets `cwd` to the exe directory, inserts `BASE_DIR` into `sys.path`, honours `HT_NO_BROWSER` | **Yes** — nothing else initializes the runtime on this path. |
| `tests/conftest.py:182` `real_app_client` (module scope) | sets `os.environ['DB_FILE']`, `os.environ['HT_RUNTIME_DIR']` and `utils.config.DB_FILE` **before** `from app import app`; asserts the path startup resolved equals the scratch path; then calls `bootstrap_runtime_database()` + `run_all_initializers(force_base=True)` itself | Yes for the path-resolution assertion; it already performs its own schema work. Used by `test_erase_data_guard.py`, `test_trailing_slash_routing.py`, `test_static_cache_policy.py`, `test_real_app_db_isolation.py`, `test_local_first_assets.py` (3 tests). |
| `tests/test_static_cache_policy.py:54,108,162` | `from app import app` (mutates `app.config['STATIC_LONG_MAX_AGE']`), `from app import STATIC_LONG_MAX_AGE_SECONDS` | Needs a module-level `app` object and the module constant. |
| `tests/test_pattern_coverage.py:417` `app_client` fixture | patches `utils.config.DB_FILE` only, then `from app import app` | Dead fixture (no test requests it; `ci.yml:823-828` records this). On a first import it would resolve the real runtime database — the defect `test_real_app_db_isolation.py` pins. |
| `tests/test_real_app_db_isolation.py:53` (subprocess probe) | fresh interpreter `import app` with `HT_RUNTIME_DIR` + optional `DB_FILE` | **Yes — pins today's behavior as a contract**, including the negative case `test_patching_config_alone_is_not_isolation` (startup *discards* a patched `utils.config.DB_FILE`). Its docstring says to revisit it if the startup contract changes. |
| `tests/test_catalog_seed_bootstrap.py:142` (subprocess) | `import app; app.app.test_client().get('/')` with env `DB_FILE`, `TESTING` removed; asserts 1,897 seeded exercises, empty owned tables, seed unchanged, no `auto_backup/` | **Yes** — relies on import performing bootstrap. |
| `scripts/smoke_packaged_app.py:247` (bootloader mode, run by `_packaged-windows.yml:106`) | `from app import STATIC_LONG_MAX_AGE_SECONDS` **in the smoke's own process** (`sys.path[0] = REPO_ROOT`); the smoke's own environment carries no `DB_FILE`/`HT_RUNTIME_DIR` (only the child's does) | Not intentionally — today this import runs the full startup inside the smoke process against the checkout's default runtime path. Becomes side-effect-free after WS3 (a behavior change to record, not a regression). |
| `tests/test_runtime_paths.py:206` | `ast.parse(app.py)`; asserts `prepare_runtime_database` is called before `bootstrap_runtime_database` before `run_all_initializers` **by line number in `app.py`** | Breaks if the calls move to another module; must be re-pointed. |
| `tests/test_css_cascade_contracts.py:1385` | reads `app.py` text for a dead element id | Unaffected unless the text moves. |

**F2 — Launch callers (process entry, not import).**

| Launch path | Who uses it | Notes |
|---|---|---|
| `python app.py` (`__main__`: atexit/SIGINT/SIGTERM WAL-checkpoint cleanup, `FLASK_DEBUG`, `FLASK_USE_RELOADER`, `runtime_port()`) | `START.bat:136`; `playwright.config.ts:171` webServer (after the E2E seed); `deep-gate.yml` ×3 (first-install, empty-schema, old-DB) and `release.yml` ×2 with `DB_FILE=…`; seven `scripts/css_audit/*.mjs` spawn `python app.py`; `.vscode/launch.json` "Python: Run app.py"; `scripts/smoke_packaged_app.py` payload mode runs `<interpreter> app.pyc` from `_internal/` | Only path with the WAL-checkpoint cleanup. |
| Packaged bootloader → `app_launcher.main()` | `Hypertrophy-Toolbox.exe`; `scripts/smoke_packaged_app.py --mode bootloader` (CI) | The only automated proof of the launcher path and of the legacy-DB migration (`check_upgrade_migration`). |
| `flask run` with `FLASK_APP=app.py` / `app:app` | `.vscode/launch.json` config 1 (`--no-reload`); `e2e/run_puppeteer_summary_regression.ps1:29` (port 5001) | **Bypasses `__main__` entirely** — today it works only because import runs the startup. |

Mirrors that encode the startup table order without importing `app`: `e2e/scripts/prepare_e2e_db.py:82`, `e2e/scripts/prepare_visual_db.py:89-130`, `tests/fixtures/make_old_schema_db.py`.

**F3 — Current module-level order in `app.py`** (line order is the only contract today): `require_supported_python()` → imports (these trigger F5's logging side effect) → `Flask(__name__)`, `strict_slashes=False`, `ProxyFix` → frozen block (`jinja_env.auto_reload=False`, `TEMPLATES_AUTO_RELOAD=False`, `DEBUG=False`, `TESTING=False`, `STATIC_LONG_MAX_AGE=STATIC_LONG_MAX_AGE_SECONDS`) → `setup_logging(app)` → `add_request_id_middleware(app)` → `register_error_handlers(app)` → `register_fallback_handlers(app)` → `prepare_runtime_database()` → `utils.config.DB_FILE = migration.database_path` → `bootstrap_runtime_database()` → `run_all_initializers(force_base=False)` → `upgrade_catalog_from_seed()` if not seeded → `create_startup_backup()` if not seeded → 13 `register_blueprint` (main, workout_log, weekly_summary, session_summary, exports, filters, workout_plan, progression_plan, user_profile, body_composition, volume_splitter, program_backup, fatigue) → debug route listing → template filters `datetime`, `safe_media_path` → `before_request start_timer` → `after_request apply_static_cache_policy` → context processors `inject_app_version`, `inject_scale_level` → `POST /erase-data` → `__main__`.

**F4 — `DB_FILE` / `HT_RUNTIME_DIR` precedence and process-global state.** `utils/config.py` resolves `DB_FILE = os.getenv("DB_FILE", runtime_database_path())` **at import**; `runtime_database_path()` honours `HT_RUNTIME_DIR`, then the frozen per-user directory, then the repository (`utils/runtime_paths.py`, pinned by `tests/test_runtime_paths.py::TestEnvironmentOverride`). `prepare_runtime_database()` reads `os.environ["DB_FILE"]` **itself** (explicit-override branch) — not `utils.config.DB_FILE` — and `app.py` then reassigns `utils.config.DB_FILE` from its outcome. Every consumer reads `utils.config.DB_FILE` dynamically at call time (`DatabaseHandler.__init__`, `get_db_connection`, `bootstrap_runtime_database`, `create_startup_backup`). So there are two process-global mechanisms — the environment (read at `utils.config` import and again inside migration) and the mutable attribute `utils.config.DB_FILE` (patched by every test fixture) — and today the import-time reassignment silently discards a patched attribute unless the environment agrees. `HT_RUNTIME_DIR` does not relocate the legacy source path (`legacy_data_dir()` is installation-relative), so a run without `DB_FILE` still inspects the checkout's own `data/database.db` when deciding whether to migrate.

**F5 — Logging side effects are transitive and precede `app.py`'s own call.** 45 modules (12 `routes/`, 33 `utils/`) run `logger = get_logger()` at module level; `get_logger()` lazily calls `setup_logging()` (`utils/logger.py:123-127`), which creates `<runtime root>/logs/` (`ensure_directory(logs_dir())`) and attaches a `RotatingFileHandler` on `app.log` plus a console handler to the `hypertrophy_toolbox` logger on the **first** such import in the process. `utils/database.py:17` is one of them and is imported at `app.py:13`, so the handlers already exist when `app.py:72` calls `setup_logging(app)`. **Consequence (verified by reading `setup_logging`): the early return `if logger.handlers: return logger` precedes the `if app:` block, so `app.logger` handler sharing and the `log_request_info` / `log_response_info` hooks (per-request INFO lines and the slow-request WARNING) never attach in production today.** No test asserts those hooks (`tests/test_logger.py` only exercises them with a `MagicMock` app). The directory creation is repeated (idempotent `mkdir`) on every `setup_logging()` call; handler attachment is once per process (`tests/test_logger.py::test_prevents_duplicate_handlers`). The log directory is fixed by whichever runtime root is in force at the first import — a later `HT_RUNTIME_DIR` is ignored. Moving `app.py`'s `setup_logging(app)` alone cannot make `import app` logging-side-effect-free, exactly as Astra's round-10 note said.

**F6 — Empty test schema versus production runtime.** The conftest `app` fixture: `Flask(__name__, template_folder, static_folder)`, `TESTING=True`, `WTF_CSRF_ENABLED=False`, `strict_slashes=False`, the 13 blueprints, only the `safe_media_path` filter, a guard-less `/erase-data` that drops and re-runs `run_all_initializers(force_base=True)`, and a copied schema template built once per session by `run_all_initializers(force_base=True)`; **no** migration, seed bootstrap, catalog upgrade, backup, request-id middleware, error/fallback handlers, cache policy, context processors or `datetime` filter. `TESTING=1` (set by conftest) makes `create_startup_backup()` return `None` and disables the `_INITIALIZATION_COMPLETE` once-per-process guard in `utils/db_initializer.py:569-575`. Production `init_runtime()` is the five-step order in F3; `deep-gate.yml` "empty-schema" job separately proves the initializers alone yield a bootable empty schema.

**F7 — Repeated initialization today.** `prepare_runtime_database()` is a no-op when the runtime DB exists; `bootstrap_runtime_database()` returns `False` when the target exists; `run_all_initializers()` is idempotent DDL (and guarded once per process outside `TESTING`); `upgrade_catalog_from_seed()` is a SHA no-op; **`create_startup_backup()` is not idempotent** — each call writes another rotated snapshot (and `/erase-data` relies on calling it on demand). Blueprint objects are module-level singletons; Flask permits registering one blueprint on several `Flask` instances but not twice on the same instance.

**F8 — `/erase-data` contract (real route).** `POST` only; JSON body `{"confirm": "ERASE_ALL_DATA"}` compared exactly (case, whitespace, key) or `400 VALIDATION_ERROR` via `error_response` **before** any write; then `create_startup_backup()` (snapshot; `None` under `TESTING=1`) → `drop_all_owned_tables` → `run_all_initializers(force_base=True)` → `success_response(data={"auto_backup": describe_snapshot(path)}, message=…)`; any exception → `logger.exception` + `500 INTERNAL_ERROR`. Consumers: `static/js/welcome.js`, `e2e/fatigue.spec.ts`, `tests/test_erase_data_guard.py` (real route), `tests/test_volume_progress.py:343` (token, conftest twin). Five call sites in three files (`test_database_user_profile.py`, `test_db_migration.py`, `test_program_backup.py` ×3) POST `/erase-data` **without** the token against the twin and expect success.

**F9 — Documentation that states the "register in both" rule or the import-time startup** (all edited in place; adding/deleting files under `.claude/**` would trip `Test Inventory Drift`, editing does not): `CLAUDE.md` §2 startup sequence and §4A; `.claude/rules/routes.md:49-53`; `.claude/rules/testing.md:126`; `.claude/rules/database.md` "Adding a DB table" and "Startup sequence"; `.claude/rules/debugging.md:39`; `.claude/agents/architecture-reviewer.md:17,19`; `.claude/agents/code-reviewer.md:13`; `.claude/agents/test-strategist.md:32`; `routes/CLAUDE.md:21,25`; `tests/CLAUDE.md:43,71-72`; `utils/CLAUDE.md:26`.

**F10 — Gates the eventual diff will trip** (`QUALITY_GATE.md`): Route/API row for `app.py` (route pytest target + blueprint-registration coverage in `tests/conftest.py`; `code-reviewer`, plus `product-risk-reviewer` if any response shape changes); Business-logic row for a new `utils/` module; DB row (`code-reviewer` + `architecture-reviewer`, full pytest + manual backup/restore smoke) if `utils/auto_backup.py`/`database.py`/`db_initializer.py`/`program_backup.py` change; `tests/conftest.py` → `test-strategist` sizes it **Full** (`/verify-suite`); AI-workflow row for the F9 docs; pyright baseline diff on any `.py` (`main` has zero headroom — no net-new diagnostic); `Test Inventory Drift` when a test file is added or a test count moves (regenerate `docs/test_inventory/`); packaged smoke (`Packaged Smoke (Windows bootloader, non-required)`) proves the launcher path.

**Re-verification at `f3adacf1`** (by `senior-developer` `a003588583f306f4e`, read-only; M = measured `path:line` at `f3adacf1`, I = inference, which is listed under Assumptions instead)

`git diff --stat e486e3b5 f3adacf1` is empty for these files (M): `app.py`, `app_launcher.py`, `utils/`, `routes/`, `tests/conftest.py`, `test_real_app_db_isolation.py`, `test_catalog_seed_bootstrap.py`, `test_runtime_paths.py`, `test_static_cache_policy.py`, `test_pattern_coverage.py`, `test_logger.py`, `test_erase_data_guard.py`, `scripts/smoke_packaged_app.py`, `.vscode/`, the Puppeteer `.ps1`, the `.spec`, `CLAUDE.md`, `.claude/rules`, `.claude/agents`, `playwright.config.ts`, `START.bat`, `pyproject.toml` and `pyrightconfig.json`. Changed but immaterial to WS3: `tests/CLAUDE.md` (line shift of 2), `AUTONOMY.md` (lines 18 and 144 unchanged in content), `ci.yml` (comment moves from 823 to 822), `QUALITY_GATE.md`, `scripts/generate_test_inventory.py`, `docs/test_inventory/*`, and `requirements.txt` (hypothesis only).

| Fact | Status at `f3adacf1` | Correction / addition (M) |
|---|---|---|
| F1 | Confirmed, **extended** | Launcher: `from app import app` at `app_launcher.py:69`; frozen `chdir` (`:37`) and `sys.path.insert` (`:43`) run at **launcher import**, not in `main()`. `real_app_client` consumers: `test_erase_data_guard.py` 5, `test_trailing_slash_routing.py` 4, `test_static_cache_policy.py` 4 direct + 4 via `frozen_cache_client`, `test_real_app_db_isolation.py:148`, `test_local_first_assets.py` 3. `frozen_cache_client` (`test_static_cache_policy.py:45-61`) mutates the **module-level** `app` while yielding `real_app_client`, so both must wrap the same object. The isolation probe runs with `TESTING=1` (`test_real_app_db_isolation.py:93-94`); the negative case is at `:121-135`. The first-install subprocess (`test_catalog_seed_bootstrap.py:133-170`) sets `DB_FILE` with no `HT_RUNTIME_DIR`. `ci.yml` B2 comment now `:822-828`, and its text ("pytest never imports `app.py`") is stale. Order test at `test_runtime_paths.py:200-222`. **New callers:** `docs/product/README.md:191` (`HT_RUNTIME_DIR=<scratch> python -c "import app; … app.app.url_map…"`, prose `:194-195` says import runs startup); three archived scripts under `docs/archive/2026/one-off-scripts/fatigue/` (`from app import app`; not executed by anything; pyright excludes `docs/archive/**`). `tests/test_worktree_snapshot.py:362` asserts an Operation A script does **not** import `app` (not a caller). |
| F1a (new) | — | **Five self-built minimal test apps** (not the twin; do not import `app`): `test_priority7_error_handling.py:48-66`, `test_weekly_summary_routes.py:28-30`, `test_session_summary_routes.py:26-28`, `test_pattern_coverage.py:310-312`, `test_errors_utils.py:266-267`. |
| F2 | Confirmed, **extended** | `__main__` at `app.py:274-314`. Additional `python app.py` callers: `README.md:77`, `.claude/skills/run-hypertrophy-toolbox/SKILL.md:16`, `.claude/settings.json:5,11` (permission strings), `docs/E2E_TESTING.md:35`; the seven `css_audit` spawners are named in the report §A.2. Bootloader also via `RUN_APP.bat:4`. `flask run` callers: `.vscode/launch.json:18-37` (`FLASK_APP=app.py` `:23`, `FLASK_DEBUG=1` `:24`, `--no-reload` `:28`) and `e2e/run_puppeteer_summary_regression.ps1:24,29` (`FLASK_APP=app:app`, only `DB_FILE` set at `:11`). **New:** the `app.py:306` comment recommends `flask run --reload`. Tree-wide grep finds no other `FLASK_APP` / `flask run` / `-m flask` / `app:app` outside `docs/archive/**` and `docs/TESTING_STRATEGY_PLANNING.md:408`. |
| F3 | Confirmed | Line map: imports `:12-45`; `STATIC_LONG_MAX_AGE_SECONDS` `:50`; `Flask` `:52`; `strict_slashes` `:53`; `ProxyFix` `:54`; frozen block `:57-69`; `setup_logging(app)` `:72`; request-id `:75`; handlers `:82-83`; runtime steps `:92-108`; blueprints `:111-125`; debug listing `:128-131`; filters `:133-158`; `start_timer` `:160-163`; cache policy `:166-207`; context processors `:209-241`; `/erase-data` `:245-271`. |
| F4 | Confirmed, **two corrections** | (a) Auto-backups go **beside the database** (`auto_backup.py:19-20`), not under `HT_RUNTIME_DIR`. Only `copy_legacy_backups` uses `runtime_data_dir()` (`runtime_migration.py:189-193`). (b) In pytest, `conftest.py:9` imports `utils.database`, which fixes the logs root before `real_app_client` sets `HT_RUNTIME_DIR` (`:179`). That variable therefore relocates neither logs nor backups, so the docstring at `conftest.py:175-178` is inaccurate. Migration actions: `explicit-override` / `same-path` / `already-present` / `no-legacy` / `migrated` / `failed` (returns **the legacy path**) (`runtime_migration.py:236-265`). `prepare_runtime_database(explicit_override=…)` exists (`:218-242`) and `app.py` does not use it. |
| F5 | Confirmed, **corrected** | The first logging trigger is `app.py:14` (`from utils.database import …`), not `:13`. Module-level `get_logger()` counts: 12 `routes/` (all except `routes/main.py`), 33 `utils/` (incl. 3 in `utils/_fatigue/`), and 0 in `scripts/`, `e2e/scripts/` and `tests/fixtures/`. `ensure_directory(logs_dir())` runs on every `setup_logging()` call with `parents=True`, so it also creates the runtime root (`logger.py:36`, `runtime_paths.py:140`). The early return at `logger.py:43-44` precedes the `if app:` branch (`:75-114`). **New:** `.claude/rules/debugging.md:29-31` documents the dead slow-request WARNING as live. `start_timer` (`app.py:160-163`) only feeds the dead hook. The 500 handler logs via `app.logger.exception` (`errors.py:188-198`) to Flask's default handler, not `app.log` (I). |
| F6 | Confirmed, **extended** | Twin at `conftest.py:243-306`; `TESTING` set at `:30`. **New:** under `TESTING=1`, `initialize_database()` runs `DROP TABLE IF EXISTS user_selection` and `workout_log` on every call (`db_initializer.py:160-161,231-232`). The once-per-process guard (`:24`, set `:593`) covers only `initialize_database()`, not the other nine steps of `run_all_initializers()` (`schema_registry.py:115-137`). |
| F7 | **Corrected** | A second call after a fresh seed is **not** a no-op. `bootstrap_runtime_database()` returns `False` because the target now exists (`catalog_seed.py:46-47`), so that call runs `upgrade_catalog_from_seed()` (writes `catalog_version`, `catalog_upgrade.py:186-233`) and `create_startup_backup()` (1,897 ≥ 100, `auto_backup.py:59`). Snapshot names have one-second resolution (`:70-71`); rotation keeps 7 by mtime, so every extra snapshot evicts the oldest (`:15,23-34`). `create_startup_backup()` never raises (`:85-87`). |
| F8 | Confirmed | Real route `app.py:245-271`. Token sites: `welcome.js:24`, `e2e/fatigue.spec.ts:41-42,300-301`, `e2e/erase-flow.spec.ts:27-30` (via UI). Real-route tests `test_erase_data_guard.py:56,69,74-77,97`. Twin with token `test_volume_progress.py:341-343`. **Twin without token (5 sites / 3 files):** `test_database_user_profile.py:170`, `test_db_migration.py:171`, `test_program_backup.py:822,838,855`. |
| F8a (new) | — | Under the conftest `app` built by `create_app()`, two tests **will fail** as written because they pin `"requestId": None`: `tests/test_export_blank_rep_bounds_contract.py:58-67` and `tests/test_export_blank_rep_bounds_gate0.py:47-57` (request-id middleware fills it; `errors.py:83,96-104`). Router-level 404/405 bodies change for XHR/`/api/` (status codes unchanged). Uncaught exceptions return 500 via the catch-all instead of propagating (I). No context processor or hook touches the DB; they read a constant, a cookie, wall time, `request`/`config` and the request-id header (`app.py:160-241`, `request_id.py:26-45`). The debug route listing logs at DEBUG to `app.log` only (console INFO+, `logger.py:56,64`), ungated, on every construction. |
| F9 | **Extended** | At `f3adacf1`: `CLAUDE.md:45-54,58,136`; `.claude/rules/routes.md:50-51,76`; `.claude/rules/testing.md:63,121-123,126`; `.claude/rules/database.md:58-66,77-80,89,97,116,127,150,153-162`; `.claude/rules/debugging.md:27,29-31,39`; `.claude/agents/architecture-reviewer.md:17,19`; `.claude/agents/code-reviewer.md:13`; `.claude/agents/test-strategist.md:27,32`; `routes/CLAUDE.md:21,25`; `tests/CLAUDE.md:45,73,74`; `utils/CLAUDE.md:26`; `docs/ai_workflow/AUTONOMY.md:18,144`; `docs/ai_workflow/PARALLEL_WORKFLOW.md:7,132`; `docs/product/README.md:191-195`; `docs/DUPLICATION_REGISTRY.md:53` (row 14, the conftest/app duplication); `docs/E2E_TESTING.md:88-89`; `ci.yml:822-828` (stale comment); `app.py:306`. **Constraint:** `tests/test_agent_workflow_contracts.py:673-680` requires root `CLAUDE.md` to stay **< 200 lines** (175 now) and keep its `get_logger()` and `seed_worktree_snapshot.py` mentions. |
| F10 | Confirmed, **refined** | A new `utils/runtime_init.py` routes to the **Business-logic** row (`QUALITY_GATE.md:48`), not the DB row, unless a DB-row file also changes. `architecture-reviewer` is requested regardless by AGREED §4 WS3 *Gates*. E2E row for the `.ps1`; AI-workflow row for docs; CI row only if `ci.yml` is touched. `app.py`/`conftest.py` → `/verify-suite`. vulture (`pyproject.toml:1-10`, `min_confidence 100`). There is no routing row for `.vscode/**`. `Test Inventory Drift` trips on new or changed test files, not on a new `utils/*.py`. |

### Recommendations awaiting owner acceptance (Q-WS3-2…6)

Recommended answers are consistent with each other. Under (a), importing `app` constructs one Flask instance and performs no DB or data-directory work, and logging is set up only by the existing transitive `get_logger()` path. All entry points, including `flask run`, go through the same guarded `init_runtime()`.

| Q | Recommended answer | Evidence and affected callers | Behavior and compatibility consequences | Required AC changes | Remaining owner choice |
|---|---|---|---|---|---|
| **Q-WS3-2** Logging promise | **(a) Narrowed written promise:** *"Importing `app` performs no database, data-directory, migration, seed, catalog-upgrade or backup work. The first `get_logger()` call in a process — triggered transitively by importing `app`, any route module or most `utils` modules — still creates `<runtime root>/logs/` and attaches the `app.log` file handler and the console handler."* `create_app()` calls `get_logger()`, never `setup_logging(app)`, so hook absence no longer depends on import order. The explicit `configure_logging()` (option b) is deferred to a separate change. | F5 at `f3adacf1`: 45 module-level calls; first trigger `app.py:14`; early return `logger.py:43-44`. Nine callers log only through the implicit configuration: `scripts/apply_free_exercise_db_mapping.py`, `apply_youtube_curated.py`, `fatigue_calibration_report.py`, `fatigue_stage4_observer.py`, `fatigue_stage4_status.py`, `e2e/scripts/prepare_visual_db.py` (→ Playwright webServer seed), `seed_summary_regression_db.py`, `tests/fixtures/make_old_schema_db.py`, and `deep-gate.yml:230-236` inline. Frozen launcher imports only `utils.python_version` + `utils.config` before `app` (`app_launcher.py:12,56`). | **(a):** no change for scripts, the frozen log path (`%LOCALAPPDATA%\HypertrophyToolbox\logs`) or tests. `import app` still creates `logs/`, and the runtime root itself if absent. The log root stays fixed by the first importer. **(b), if chosen:** import becomes free of filesystem work, but the nine callers lose INFO output unless edited. `test_logger.py:172-197` breaks and others port. `test_fatigue.py` caplog level reliance is unknown. The hooks decision becomes forced (calling `setup_logging(app)` on an unconfigured logger would activate them). | AC1: `logs/` allowed, `data/` forbidden. AC4: `create_app()` does not call `setup_logging(app)`. AC10: the exact promise text. | Accept (a), or select (b) in WS3. (b) tightens AC1 to "no `logs/` and empty handler list after import", replaces AC10 with a `configure_logging()` contract, and brings the nine callers and `test_logger.py` into scope. |
| **Q-WS3-2H** Unattached request hooks (distinct decision) | **Delete** `log_request_info` / `log_response_info` (the `if app:` branch, `logger.py:74-114`) and `start_timer` (`app.py:160-163`). Correct `.claude/rules/debugging.md:29-31`. | Never attached in production (F5). No test asserts them: `test_logger.py::TestFlaskIntegration` (`:227-239`) asserts only `logger is not None`. `debugging.md:29-31` documents them as live. | **Delete:** no runtime behavior change. Touches `utils/logger.py`, and probably changes or removes tests in `tests/test_logger.py` → regenerate the inventory. **Enable, if chosen:** two INFO lines per request including ~20 static assets per page (`templates/base.html:11-292`), slow-request WARNINGs, 500-handler exceptions start reaching `app.log` (handler-list aliasing, `logger.py:76`), and pytest/E2E console noise. **Leave dead:** no diff, but documented non-features stay, reachable by any ordering change. | AC4: drop `start_timer`; no `before_request`/`after_request` other than request-id and cache policy. AC13: add `debugging.md:29-31`. | Delete (rec.) / enable / leave dead. |
| **Q-WS3-3** Module-level `app` | **Retain `app = create_app()`** (confirms A1), with signature `create_app(config_overrides: Mapping \| None = None)`. Overrides are applied **after** the frozen block, matching AGREED §4's `create_app(config)`. Module-level construction does no DB or data work. **Debug route listing (`app.py:127-131`): delete** (see consequences). | Object importers: `app_launcher.py:69`, `conftest.py:182`, `test_static_cache_policy.py:54,108`, `test_catalog_seed_bootstrap.py:142-143`, `docs/product/README.md:191`, dead `test_pattern_coverage.py:417`, 3 archived scripts. Constant importers: `smoke_packaged_app.py:247`, `test_static_cache_policy.py:162`. With `FLASK_APP=app.py`, Flask finds the attribute `app` first (I). Blueprints register no app-wide hooks (grep 0). The frozen block forces `TESTING=False` (`app.py:63`), hence overrides go after it. `strict_slashes` must be set before any `register_blueprint` (I). | Every caller keeps working. A pytest process holds ≥ 2 Flask instances, which is fine. Tests that mutate the singleton must mutate the instance their client wraps, so `real_app_client` keeps the module-level object (report C.3). Removing the attribute would change six live callers and both `flask run` callers, and silently break the archived scripts. **Debug listing:** it is DEBUG-only to `app.log`, ungated on every construction, has no consumer or test, and would repeat per test under the function-scoped conftest fixture (`conftest.py:243`). Gating it on `app.debug` may never fire at construction (⚠️ A8). Deleting removes those DEBUG lines from `app.log`. | AC1: "exactly one Flask instance constructed". AC4: overrides applied after the frozen block; no route listing. AC9 unchanged. In-scope cross-reference corrected to A1. | Retain (rec.) / remove. Debug listing: delete (rec.) / move into `create_app()` gated on `app.debug`. `config_overrides` parameter (rec.) vs plain `app.config.update()` after construction (stylistic). |
| **Q-WS3-4** Repeated `init_runtime()` | **Guarded initialization:** **(i)** a process-level guard keyed by the resolved requested database (explicit argument or env `DB_FILE`, resolved) plus `runtime_root()` at call time, stored only after all steps succeed. **(ii)** Same key → no-op returning the cached outcome with `already_initialized=True`: no migration, seed, schema pass, upgrade or snapshot. **(iii)** Different key → `RuntimeError`. **(iv)** On exception the guard stays unset and the error propagates, so a retry is allowed. A `seeded` flag carries over from a failed attempt so a retry after a successful seed still skips upgrade and backup. **(v)** Under `TESTING=1`, refuse unless the path is explicit (argument or env). **(vi)** A private, test-only guard reset `utils.runtime_init._reset_for_tests()`. `real_app_client` calls it immediately before its `init_runtime(db_file=<scratch>)`; production code never calls it. `/erase-data` keeps calling `create_startup_backup()` directly. **Reloader:** initialize only in the serving process (`not use_reloader or is_running_from_reloader()`). | F7 correction (a second call after a seed upgrades and snapshots; each snapshot evicts one of 7). A "failed" migration returns the legacy path, and a retry may flip `DB_FILE` mid-process (`runtime_migration.py:258-265`). The `db_initializer` guard is a bare bool covering one step, so a different DB would get a partial schema (`db_initializer.py:569-577`). `TESTING=1` drops two user tables on every call (F6). The isolation probe runs `TESTING=1` with no `DB_FILE` (`test_real_app_db_isolation.py:93-98`), which risks a legacy-path fallback (⚠️ A9). Today the reloader runs startup in the parent and every child (I). `real_app_client` is **module-scoped** (`conftest.py:136-137`) and builds a fresh scratch DB per test module. Under Q-WS3-6 it calls `init_runtime(db_file=<scratch>)`, so the second module in one pytest process presents a different key, and rule (iii) alone would raise `RuntimeError`. | No double snapshots and no mid-process database switch. `/erase-data` unchanged. **Behavior changes to record:** with the reloader on, the monitoring parent no longer initializes or snapshots, while each serving child still takes one startup snapshot as today. The subject of the negative isolation test moves from `import app` to `init_runtime()`; under (v) it asserts "raises". **(vi):** each `real_app_client` module re-initializes its own scratch DB as today. The reset is a private test seam; a contract test proves no production entry point references it. | AC2: return fields. AC3: rules (i)–(vi), each asserted, plus the production-never-calls-reset contract. AC5: the replacement for the negative test. AC6: `real_app_client` resets before init. AC7: the reloader rule. | **4a** different key: raise (rec.) / warn and no-op. **4b** accept (v) (rec.; changes the isolation-probe contract) / reject. **4c** seeded-flag carry-over (rec.) / accept one redundant snapshot after a failed first boot. **4d** multi-module `real_app_client`: test-only `_reset_for_tests()` (rec.) / make `real_app_client` session-scoped, so one scratch DB is shared across modules and per-module isolation is lost / keep `real_app_client` off `init_runtime()`, calling the steps directly as today, so the real init path is not exercised in-process. |
| **Q-WS3-5** `flask run` callers | Add **`create_initialized_app()`** in `app.py`: `init_runtime()` then `return create_app()`. Point `.vscode/launch.json:23` and `e2e/run_puppeteer_summary_regression.ps1:29` at `FLASK_APP=app:create_initialized_app` (one-line repairs). Fix the `app.py:306` comment. **Puppeteer runner:** repair only in WS3; retirement is a separate later change, not WS3 scope. | Only callers: `.vscode/launch.json:18-37` and the `.ps1` (`:24,29`), plus the `app.py:306` comment; tree-wide grep finds no other. Both work today only because import initializes. Puppeteer runner: no workflow, `package.json` or test reference; Puppeteer is not a dependency; it fetches `npx -y @modelcontextprotocol/server-puppeteer` at run time (network); it leaks `auto_backup/` in `%TEMP%`; `.claude/settings.json:61` lists a dangling `"puppeteer"` server. Overlap with `e2e/summary-pages.spec.ts` is unverified (⚠️ A10). | Both callers keep working and go through the same guard (C.2). `--no-reload` keeps the reloader rule moot. The `.ps1` edit trips the E2E row. A `flask init-runtime` CLI command suits the `.ps1` but not the single-step debugpy configuration. Dropping VS Code config 1 loses `FLASK_DEBUG=1` / `jinja: true`. Retiring the runner in WS3 would add file deletions and a `.claude/settings.json` edit: broader cleanup the owner excluded. | AC11: names the mechanism and a direct-call test. AC13: adds `app.py:306`. | Factory function (rec.) / `flask init-runtime` CLI / drop VS Code config 1. Puppeteer: repair now and propose retirement separately (rec.) / retire in WS3. |
| **Q-WS3-6** `init_runtime()` boundary | **New `utils/runtime_init.py`** (confirms A2) exposing `init_runtime(db_file=None)`, which forwards to `prepare_runtime_database(explicit_override=db_file)`. The env fallback is unchanged. **The `utils.config.DB_FILE` attribute is never an input**; `init_runtime()` writes it exactly once from the migration outcome. `create_app()` stays in `app.py`. `real_app_client` keeps the module-level `app` and calls `init_runtime(db_file=<scratch>)` explicitly, after the 4d test-only reset (report option B.6(7)(C)). | The five home modules import only `utils` (`runtime_migration.py:24-32`, `catalog_seed.py:10-12`, `schema_registry.py:4-16`, `catalog_upgrade.py:40-42`, `auto_backup.py:9-10`). `utils` → `routes`/`app` imports: 0, so there is no cycle. Attribute-only patchers (`conftest.py:119,247`, `test_priority7_error_handling.py:45`, `test_pattern_coverage.py:307,415`, `prepare_visual_db.py:85`, `seed_summary_regression_db.py:26`, `make_old_schema_db.py:41-44`) never call startup, so they are unaffected. `test_runtime_paths.py:200-222` (AST over `app.py`) fails once the calls move. | Business-logic row (`code-reviewer`). Initializer callers no longer import all 13 route modules. Honouring a patched attribute (option B) would be fragile, because the attribute is bound at import and `HT_RUNTIME_DIR` changes would look like patches. Keeping today's discard (option A) without an argument gives tests no explicit path. | AC2: names the module and a mock-based order test. AC5: split into path precedence, explicit argument, attribute-never-input and outcomes. | Confirm module (rec.) / keep `init_runtime()` inside `app.py`. Attribute handling: explicit argument + discard (rec., C) / discard only (A) / honour attribute (B). |

### Acceptance criteria

Each criterion assumes the recommended answers. The criterion numbering follows rev 1. Where an owner override would change a criterion, the decision table says how.

1. **Import is free of DB and data work** (Q-WS3-2a, Q-WS3-3). Given a fresh interpreter with `HT_RUNTIME_DIR` set to an empty scratch directory and no `DB_FILE`, when `import app` runs, then:
   - nothing exists under `<scratch>/data/`;
   - no `auto_backup/` directory is created anywhere;
   - the env-resolved runtime database file does not exist;
   - `utils.config.DB_FILE` equals its import-time value;
   - `app.app` is a `Flask` instance and exactly one was constructed;
   - only `<scratch>/` and `<scratch>/logs/` (with `app.log`) may have been created.
   
   The same holds when `DB_FILE` points at a non-existent scratch path, and when only `utils.config.DB_FILE` is patched before import. Asserted by subprocess tests that replace the import-subject cases of `tests/test_real_app_db_isolation.py`.
2. **Initialization order** (Q-WS3-6). Given `utils/runtime_init.py`, when `init_runtime()` is called once with its steps mocked, then the calls occur in this order:
   1. `prepare_runtime_database`;
   2. a single assignment of `utils.config.DB_FILE`;
   3. `bootstrap_runtime_database`;
   4. `run_all_initializers(force_base=False)`;
   5. `upgrade_catalog_from_seed` (skipped when the seed just ran);
   6. `create_startup_backup` (skipped when the seed just ran).
   
   The result exposes `database_path`, `migration_action`, `seeded`, `snapshot_path` and `already_initialized`. This mock-based test replaces the AST line-number test at `tests/test_runtime_paths.py:200-222`. `utils/runtime_init.py` imports no `routes` or `app` module.
3. **Repeated initialization** (Q-WS3-4). Given `init_runtime()` has completed once in a process:
   - (a) a second call with the same resolved key returns `already_initialized=True`, with no migration, seed copy, schema pass or upgrade, and no new file in `auto_backup/`;
   - (b) a call with a different resolved database or runtime root raises `RuntimeError` and changes nothing;
   - (c) a call that raises leaves the guard unset, so a later identical call runs;
   - (d) a retry after a failed call that had already seeded skips upgrade and backup;
   - (e) under `TESTING=1`, a call with neither an explicit `db_file` nor env `DB_FILE` raises before touching any file;
   - (f) after `utils.runtime_init._reset_for_tests()`, a call with a different key initializes normally instead of raising. A contract test proves that no production entry point (`app.py`, `app_launcher.py`, any `utils/`, `routes/` or `scripts/` module other than `utils/runtime_init.py` itself) references `_reset_for_tests`.
   
   `/erase-data` still writes a snapshot on every confirmed call.
4. **Factory construction** (Q-WS3-2, Q-WS3-2H, Q-WS3-3). Given `create_app()` is called twice in one process, when both applications are inspected, then:
   - each is a distinct `Flask` instance with the same 13 blueprint names and the same URL rule set as today's module-level app;
   - `strict_slashes=False` is in effect on all rules;
   - `ProxyFix` wraps the WSGI app;
   - responses carry `X-Request-ID`;
   - error handlers and then fallback handlers are registered in the order documented at `utils/errors.py:232-236`;
   - the `datetime` and `safe_media_path` filters, the after-request `apply_static_cache_policy`, the context processors `inject_app_version` and `inject_scale_level`, and `POST /erase-data` are present;
   - there are no other `before_request`/`after_request` functions besides the request-id pair and the cache policy;
   - `config_overrides` are applied after the frozen block;
   - no route listing is logged;
   - `create_app()` never calls `setup_logging(app)` and opens no database;
   - the `hypertrophy_toolbox` logger still has exactly one `RotatingFileHandler` and one console handler.
5. **Precedence and explicit configuration** (Q-WS3-6, Q-WS3-4).
   - (a) Import-time path resolution is unchanged: env `DB_FILE` > `HT_RUNTIME_DIR` > frozen per-user root > installation root. `tests/test_runtime_paths.py::TestEnvironmentOverride` passes unmodified.
   - (b) `init_runtime(db_file=X)` resolves to `X` with migration action `explicit-override` and sets `utils.config.DB_FILE = X` exactly once.
   - (c) `init_runtime()` without an argument resolves exactly as today's startup. A pre-patched `utils.config.DB_FILE` is never read as input, and is overwritten by the resolved path. This is asserted in a non-`TESTING` subprocess and replaces `test_patching_config_alone_is_not_isolation`, with its revision recorded.
   - (d) Initialization outcomes are unchanged: an existing DB is not migrated or seeded; a legacy DB is migrated; a missing DB is fresh-seeded with upgrade and backup skipped. `tests/test_catalog_seed_bootstrap.py::test_real_app_first_install_seeds_catalog_without_mutating_seed` still asserts 1,897 exercises, empty owned tables, an unchanged seed and no `auto_backup/`, now driven through the explicit init path.
6. **One construction path in tests** (Q-WS3-3, Q-WS3-6). Given `tests/conftest.py`'s `app` fixture builds its application with `create_app(config_overrides={TESTING, WTF_CSRF_ENABLED})`, when the suite runs, then:
   - the hand-maintained twin (`conftest.py:243-306`) is gone;
   - the schema still comes from the unseeded template (`run_all_initializers(force_base=True)`), never from the catalog seed, upgrade or backup;
   - `real_app_client` stays module-scoped and uses the module-level `app`. It calls `utils.runtime_init._reset_for_tests()` and then `init_runtime(db_file=<scratch>)`, so every consuming module (`test_erase_data_guard.py`, `test_trailing_slash_routing.py`, `test_static_cache_policy.py`, `test_real_app_db_isolation.py`, `test_local_first_assets.py`) passes in one full-suite process without `RuntimeError`. Its docstring no longer claims `HT_RUNTIME_DIR` relocates backups or logs;
   - the two certain failures, `test_export_blank_rep_bounds_contract.py:58-67` and `test_export_blank_rep_bounds_gate0.py:47-57` (`"requestId": None`), are updated;
   - the five token-less `/erase-data` sites (`test_database_user_profile.py:170`, `test_db_migration.py:171`, `test_program_backup.py:822,838,855`) send `{"confirm": "ERASE_ALL_DATA"}`;
   - **every changed assertion is listed in the PR with its reason, and none is weakened**;
   - the dead `test_pattern_coverage.py:417` fixture is deleted with a reason.
   
   The five self-built minimal test apps (F1a) are explicitly unchanged.
7. **Launch paths** (Q-WS3-4). Given `python app.py` and the packaged bootloader (`app_launcher.main()`), when each starts, then `init_runtime()` runs exactly once per serving process before `app.run(...)`; with the reloader on, the monitoring parent does not initialize. The following behave as today: `HT_PORT`, `FLASK_DEBUG`, `FLASK_USE_RELOADER`, `HT_NO_BROWSER`, the `__main__` WAL-checkpoint/signal cleanup (not added to the launcher), and the launcher's import-time `chdir`/`sys.path` and error-wait UX. `scripts/smoke_packaged_app.py` passes in bootloader mode (including `check_upgrade_migration`) and payload mode, and the `deep-gate.yml` / `release.yml` first-install, empty-schema and old-DB jobs pass with no workflow edit.
8. **`/erase-data` unchanged.** Given the real route on `create_app()`, when it is called with and without the exact token, then the F8 contract is unchanged:
   - 400 `VALIDATION_ERROR` before any write;
   - snapshot → `drop_all_owned_tables` → `run_all_initializers(force_base=True)`;
   - `data.auto_backup` as `{"filename": …}` or `None`;
   - the same message;
   - 500 `INTERNAL_ERROR` on any exception.
   
   `tests/test_erase_data_guard.py` passes.
9. **Frozen build and imports.** Given `sys.frozen` is true, the frozen block and `STATIC_LONG_MAX_AGE_SECONDS` apply exactly as today. `from app import app` and `from app import STATIC_LONG_MAX_AGE_SECONDS` keep working for `app_launcher.py`, `tests/test_static_cache_policy.py` and `scripts/smoke_packaged_app.py`. The smoke's in-process import no longer runs startup, and that behavior change is recorded in the PR.
10. **Written promise** (Q-WS3-2). When the PR lands, root `CLAUDE.md` states the Q-WS3-2(a) promise text verbatim and stays under 200 lines (`tests/test_agent_workflow_contracts.py:673-680` passes).
11. **`flask run` callers** (Q-WS3-5). Given `FLASK_APP=app:create_initialized_app`, then `create_initialized_app()` calls `init_runtime()` once and then `create_app()`, asserted by a direct-call test with mocks and no server. `.vscode/launch.json:23` and `e2e/run_puppeteer_summary_regression.ps1:29` use it, and the `app.py:306` comment no longer recommends a bare `flask run --reload`.
12. **Validation evidence.** Given the full gate, when the PR is verified, then all of these are green:
    - `/verify-suite` (full pytest + Chromium);
    - the packaged-Windows smoke, observed (non-required, RP-3);
    - the fresh-process subprocess checks of AC1/AC5;
    - the mock order and guard tests of AC2/AC3;
    - first install (AC5d), existing-DB upgrade via `tests/fixtures/make_old_schema_db.py`, and legacy migration via the smoke's `check_upgrade_migration`;
    - backup/restore: `tests/test_program_backup.py` plus a manual backup/restore smoke in the clone;
    - both launch paths;
    - pyright with no net-new diagnostics, vulture, a regenerated `Test Inventory Drift`, and `tests/test_agent_workflow_contracts.py`.
    
    No Waitress or server-behavior change. All runtime evidence comes from the standalone clone with private paths (IC-1…IC-2) and records those paths.
13. **Documentation.** When the PR lands, every statement in the F9 `f3adacf1` list that WS3 makes false is corrected in place:
    - "Register in both `app.py` and `tests/conftest.py`" becomes "register in `create_app()`".
    - `CLAUDE.md` §2's startup sequence names `init_runtime()` and its callers.
    - `docs/product/README.md:191-195`, `DUPLICATION_REGISTRY.md:53`, `AUTONOMY.md:18,144`, `PARALLEL_WORKFLOW.md:7,132` (where made false), `debugging.md:29-31` and `app.py:306` are updated.
    - No file under `.claude/**` is added or deleted.
    - `ci.yml:822-828` is left unchanged and its stale comment recorded as a follow-up.

**Preservation traceability (ED-4)**

| Preserved item | AC | Current location (M, `f3adacf1`) |
|---|---|---|
| Production init order and fresh-seed skip | 2, 5d, 7 | `app.py:92-108` |
| `DB_FILE` / `HT_RUNTIME_DIR` precedence; explicit process-global config | 5a–c, 1 | `config.py:22`; `runtime_paths.py:74-81,89-110`; `runtime_migration.py:236-253` |
| Unseeded test schemas | 6 | `conftest.py:76-78,93-133,296-300` |
| 13 blueprints, middleware, handlers, filters, context processors, static caching | 4 | `app.py:53-83,111-125,133-241`; `errors.py:148-282`; `request_id.py:18-45` |
| `/erase-data` confirmation, backup, response, failure | 8 | `app.py:245-271` |
| Source and packaged launch behavior | 7, 9, 11 | `app.py:274-314`; `app_launcher.py:37-110`; `smoke_packaged_app.py:290-326,443-470` |

### Calculation surface
- `none`. No change to effective sets, progression, weekly/session summary, fatigue, schema, catalog data or production API response shapes. Test-only response bodies change where the real middleware and handlers now apply (AC6); production responses do not.

### In scope
- `create_app(config_overrides=None)` in `app.py`, building everything in F3 except the five runtime steps, the debug listing and `__main__`; module-level `app = create_app()` retained (⚠️ A1 / Q-WS3-3).
- `utils/runtime_init.py` with the guarded `init_runtime(db_file=None)` and the private test-only `_reset_for_tests()` (⚠️ A2 / Q-WS3-6, Q-WS3-4 incl. 4d).
- `create_initialized_app()` in `app.py`; the `.vscode/launch.json:23` and Puppeteer `.ps1:29` one-line repairs; the `app.py:306` comment (Q-WS3-5).
- `app.py __main__` and `app_launcher.main()` calling `init_runtime()` under the reloader rule (AC7).
- Deleting the dead request hooks and `start_timer` in `utils/logger.py` / `app.py`, with the matching `tests/test_logger.py` changes (Q-WS3-2H).
- `tests/conftest.py` (`app` fixture via `create_app()`, `real_app_client` via explicit init, twin removed). Changes to `test_real_app_db_isolation.py`, `test_runtime_paths.py:200-222`, `test_catalog_seed_bootstrap.py:133-170`, the two `requestId` tests and the five token sites. Deletion of `test_pattern_coverage.py:417`. New tests for AC1–AC4 and AC11.
- The AC13 documentation corrections, edited in place; `docs/test_inventory/` regenerated.

### Out of scope / non-goals
- **Owner exclusions (ED-5):** Waitress or any server change; service extraction (WS4); dependency regrouping (WS5); calculation changes; schema changes; CI redesign; broad documentation cleanup; recovery operations.
- Editing `.github/workflows/**` (including the stale `ci.yml:822-828` comment), `playwright.config.ts`, the `e2e/scripts/*` mirrors, the `scripts/css_audit/*.mjs` spawners, `START.bat`, `RUN_APP.bat` or `Hypertrophy-Toolbox.spec`.
- Changing migration, seed, upgrade or backup semantics; changing `/erase-data`'s request or response; changing journal-mode or `FLASK_DEBUG` defaults (`utils/database.py:88`).
- Explicit `configure_logging()` (Q-WS3-2b) and enabling the request hooks, unless the owner selects them.
- Retiring the Puppeteer runner, or removing the dangling `"puppeteer"` entry at `.claude/settings.json:61`; recorded as a separate later proposal.
- The five self-built minimal test apps (F1a); the archived `docs/archive/**` scripts; the dead `_INITIALIZATION_COMPLETE` declaration at `utils/database.py:27`.
- Pre-existing stale line references in docs that WS3 does not otherwise make false (for example `.claude/rules/routes.md:76`, `database.md:89,150`, `utils/CLAUDE.md:26`). They are corrected only inside a sentence WS3 already edits.
- Adding the WAL-checkpoint cleanup to `app_launcher`; any new CI job.
- Any worktree or clone creation or removal, shared-checkout write, recovery change, release, publication, push or merge.

### Assumptions made

All thirteen rows were **accepted as planning assumptions (owner, 2026-10-20) — not experimentally proven.** The prior status text is kept after "Was:". Plan v1's *Assumption verification* table gives each one a concrete verification criterion.

| ID | Assumption | Status |
|---|---|---|
| ⚠️ **A1** | Keeping a module-level `app = create_app()` is acceptable even though `import app` still constructs a Flask object (and, under Q-WS3-2a, attaches log handlers transitively). | Accepted as planning assumption (owner, 2026-10-20) — not experimentally proven. Was: Recommended in Q-WS3-3; awaiting acceptance. |
| ⚠️ **A2** | `init_runtime()` belongs in a new `utils/runtime_init.py`; ADR-002 needs no new root module. | Accepted as planning assumption (owner, 2026-10-20) — not experimentally proven. Was: Recommended in Q-WS3-6; awaiting acceptance. |
| ⚠️ **A3** | The five twin tests that POST `/erase-data` without the token intend "erase then reinitialize", not "the route accepts an empty body", so adding the token preserves intent. | Accepted as planning assumption (owner, 2026-10-20) — not experimentally proven. Was: Unchanged from rev 1. |
| ⚠️ **A4** | `test_patching_config_alone_is_not_isolation` (which pins the current defect) is replaced, not preserved. Its replacement contract is AC1 (import touches no DB even with a patched attribute) + AC5c (non-`TESTING` `init_runtime()` ignores the attribute) + AC3e (`TESTING=1` without a path raises). | Accepted as planning assumption (owner, 2026-10-20) — not experimentally proven. Was: Revised from rev 1. |
| ⚠️ **A5** | Today the smoke's in-process import (`smoke_packaged_app.py:247`) runs full startup against the checkout's default path, and on a fresh CI checkout it seeds `<checkout>/data/database.db` (inference from `catalog_seed.py:43-90`). WS3 removes that without any smoke edit; the change is recorded, not treated as a regression. | Accepted as planning assumption (owner, 2026-10-20) — not experimentally proven. Was: Corrected from rev 1 ("incidental"); the rev 1 alternative of moving the constant is withdrawn. |
| ⚠️ **A6** | No one relies on the never-attached request hooks (no test, no consumer; `debugging.md:29-31` is documentation only). | Accepted as planning assumption (owner, 2026-10-20) — not experimentally proven. Was: Basis of Q-WS3-2H. |
| ⚠️ **A7** | The packaged smoke (both modes) plus the existing deep-gate and release jobs suffice as "both launch paths" validation; WS3 adds no CI job. | Accepted as planning assumption (owner, 2026-10-20) — not experimentally proven. Was: Unchanged. |
| ⚠️ **A8** | Framework behavior cited from Flask 3.1.3 / Werkzeug 3.1.9 documentation and not measured: CLI app-discovery order; whether `flask run`'s reloader parent loads the app; `Rule.strict_slashes` bound when a rule is added; exception propagation under `TESTING` when an `Exception` handler exists; the `app.logger` default stderr handler; `app.debug` being `False` at construction under `python app.py`. | Accepted as planning assumption (owner, 2026-10-20) — not experimentally proven. Was: DOC/INFERENCE (report gap 1). |
| ⚠️ **A9** | Under `TESTING=1`, a migration failure other than the busy-sidecar check could return the legacy path, and initialization would then drop two tables in the developer's real `data/database.db`. This is a static analysis only. | Accepted as planning assumption (owner, 2026-10-20) — not experimentally proven. Was: INFERENCE (report B.3, gap 8); basis of Q-WS3-4(v). |
| ⚠️ **A10** | Whether `e2e/summary-pages.spec.ts` covers the Puppeteer harness's two checks, and whether its npx package still resolves. Not relied on, because WS3 repairs the runner rather than retiring it. | Accepted as planning assumption (owner, 2026-10-20) — not experimentally proven. Was: Unverified (gap 6). |
| ⚠️ **A11** | Beyond the two `requestId` tests and the five token sites, no other test outcome changes under `create_app()`. This rests on grep; only a full run settles it. AC6 requires every changed assertion to be listed. | Accepted as planning assumption (owner, 2026-10-20) — not experimentally proven. Was: Grep-based (gaps 2–3). |
| ⚠️ **A12** | PyInstaller import analysis picks up `utils/runtime_init.py` with no `hiddenimports` change. | Accepted as planning assumption (owner, 2026-10-20) — not experimentally proven. Was: INFERENCE; confirmed by the packaged smoke (gap 5). |
| ⚠️ **A13** | `test_fatigue.py`'s caplog use does not depend on the DEBUG level `setup_logging` sets; this matters only if Q-WS3-2(b) is selected. | Accepted as planning assumption (owner, 2026-10-20) — not experimentally proven. Was: Unverified (gap 4). |

### Open questions for the owner
- None beyond the per-row choices in the recommendation table, which the consolidated Gate 0 block below collects. Q-WS3-1 is decided (ED-1) and is not asked again.

### Section 0 sign-off — GATE 0

This pause is required. Under `docs/ai_workflow/QUALITY_GATE.md` plan-stage routing, Large / cross-cutting work needs Gate 0 (owner approval of requirements) before the council, and `/requirements` stops at Gate 0. Gate 0 is an owner approval; an agent's relay or summary is not one (QUALITY_GATE *Owner approvals and reviewer passes*). Plan v1 is not drafted until it is given.

- [x] Owner accepted or overrode each recommendation row (Q-WS3-2, Q-WS3-2H, Q-WS3-3 + sub-choices, Q-WS3-4 + 4a/4b/4c/4d, Q-WS3-5 + Puppeteer, Q-WS3-6). **All recommendations accepted, no overrides.**
- [x] Owner confirms acceptance criteria 1–13 match intent.
- [x] Owner reviewed assumptions A1–A13 and accepted or corrected each. **All accepted as documented planning assumptions, not as experimentally proven facts.**

**Gate 0 record.** Owner reply, verbatim, 2026-10-20. Source: the owner's message pasted into manager session `hypertrophy-toolbox-v3-main-c3`; durable copy at `artifacts/ws3-app-factory-20261020/ws3-owner-gate0-council-request-20261020.md`.

> Gate 0: accept all revision-2 recommendations; acceptance criteria 1–13 match intent; assumptions A1–A13 are accepted as documented planning assumptions, not as experimentally proven facts.
>
> This includes:
> - the narrowed import-side-effect promise with logging retained;
> - deletion of dead request hooks/start_timer;
> - retaining module-level app = create_app();
> - guarded explicit runtime initialization and the stated test-path refusal/reset behavior;
> - repairing the flask/Puppeteer launch paths;
> - placing runtime initialization in utils/runtime_init.py.
>
> I authorize the formal planning council through a reviewable Plan v2 and the next owner Gate 1. Implementation is not authorized.
>
> Do not repeat completed requirements investigation. Resolve remaining design uncertainties in the plan, and give unmeasured assumptions concrete verification criteria. Preserve startup order, unseeded test schemas, all blueprints and handlers, erase confirmation/backup behavior, and production API/calculation semantics.

The manager reports that "all recommendations" means the recommended option in every row 1–8 of the consolidated table below. That covers sub-choices 3a (delete the debug listing), 3b (`config_overrides`), 4a (raise), 4b (refuse), 4c (keep the seeded carry-over), 4d (`_reset_for_tests()`), 5 (`create_initialized_app()`), 5a (repair the Puppeteer runner and propose retirement separately) and 6 (the attribute is never an input). This record signs Gate 0 only. Gate 1 and implementation are not approved.

**Consolidated Gate 0 request.** Reply once: either "**Gate 0: accept all recommendations; ACs 1–13 match intent; A1–A13 accepted**", or list only the items you change:

| # | Item | Recommended | Alternatives |
|---|---|---|---|
| 1 | Q-WS3-2 logging promise | (a) narrowed written promise; `create_app()` uses `get_logger()` | (b) explicit `configure_logging()` in WS3 |
| 2 | Q-WS3-2H request hooks + `start_timer` | delete | enable / leave dead |
| 3 | Q-WS3-3 module-level `app` | retain `app = create_app()` | remove |
| 3a | Debug route listing | delete | move into `create_app()`, gated on `app.debug` |
| 3b | Test configuration | `create_app(config_overrides=None)`, applied after the frozen block | `app.config.update()` after construction |
| 4 | Q-WS3-4 repeated `init_runtime()` | guard (i)–(vi) + reloader rule | — |
| 4a | Different database/runtime in one process | raise `RuntimeError` | warn and no-op |
| 4b | `TESTING=1` without an explicit path | refuse (raise) | allow |
| 4c | `seeded` carry-over after a failed attempt | keep | accept one redundant snapshot |
| 4d | Re-initialization across `real_app_client` modules in one pytest process | private test-only `_reset_for_tests()`, called only by `real_app_client`; contract test that production never calls it | make `real_app_client` session-scoped / keep `real_app_client` off `init_runtime()` |
| 5 | Q-WS3-5 `flask run` callers | `create_initialized_app()` + two one-line repairs + `app.py:306` comment | `flask init-runtime` CLI / drop VS Code config 1 |
| 5a | Puppeteer runner | repair in WS3; propose retirement separately | retire in WS3 |
| 6 | Q-WS3-6 boundary | `utils/runtime_init.py`, `init_runtime(db_file=None)`, attribute never an input | keep in `app.py` / discard-only / honour attribute |
| 7 | Acceptance criteria 1–13 | match intent | corrections |
| 8 | Assumptions A1–A13 | accepted | corrections |

---

*Gate 0 was signed 2026-10-20 (record above). Plan v1, Agent provenance, Reviewer findings, Response matrix, Plan v2 and Sign-off now follow the rev 1 audit trail below, at the end of this file, so Section 0 stays contiguous. They are written via `/council-plan` under the owner's 2026-10-20 Gate 0 authorization, which stops at Gate 1, using `docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md`. Section 0 agent IDs (not council provenance): `product-manager` `af7285ca1164caf98`, `senior-developer` `a003588583f306f4e`.*

### Superseded text (rev 1, verbatim — kept for the audit trail)

**Rev 1 Q-WS3-1** (superseded 2026-10-20 by ED-1):

> - **Q-WS3-1 — Q8(a) sequencing (blocking for implementation, not for planning).** The Operation A rollout order on fixed main (`docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md` §1.2 "Approved rollout order": Gate 1 → A. Prevention → `PREVENTION_COMPLETE` → "finish or explicitly disposition open development; retain its worktrees" → stabilization checkpoint → B, C, D) has `PREVENTION_COMPLETE` undeclared. The decision needed is an **individual classification of WS3** (AGREED_PLAN §9.1): (i) WS3 implementation waits for `PREVENTION_COMPLETE` or another named milestone; (ii) WS3 implementation may proceed now in an isolated standalone clone with its own runtime/backup/log/temp paths under §4's parallel conditions; or (iii) (ii) with named constraints (for example: no shared-checkout writes, no worktree creation, no `data/database.db` access, CI as the only verification of the launcher path). No hold release is inferred by this brief; design, council and Gate 1 can proceed under any of (i)–(iii) because they are read-only.

**Rev 1 Q9 note** (superseded 2026-10-20 by ED-2):

> **Decision not needed now:** Q9 (where `AGREED_PLAN.md` lives) does not gate WS3 planning; this file follows the same untracked status until Q9 is answered.

**Rev 1 Q-WS3-2…6** (superseded 2026-10-20 by the recommendation table):

> - **Q-WS3-2 — Logging promise.** Choose (a) narrow the "no side effects on import" promise to database/data-directory work and document the retained logging side effect and the F5 dead hooks as a separate decision (recommended for WS3: smallest diff, 45 modules untouched), or (b) make logging configuration explicit and idempotent in WS3 (handlers attached by `configure_logging()` from the init path; `get_logger()` returns the named logger without creating handlers or directories), accepting that scripts importing `utils` would stop logging to `app.log` until they call it. Separately: should the never-attached per-request hooks be activated (behavior change: two INFO lines per request plus slow-request WARNINGs) or deleted as dead code? Recommendation: delete in WS3 under (a), record in the PR.
> - **Q-WS3-3 — Module-level `app`.** Confirm A1 (keep `app = create_app()` at import) or choose "no module-level app" (launcher and tests call `create_app()`; `flask run` callers use `FLASK_APP=app:create_app`).
> - **Q-WS3-4 — Repeated `init_runtime()`.** Should a second call in one process be a guarded no-op (recommended; `/erase-data` keeps calling `create_startup_backup()` directly, so on-demand snapshots are unaffected), or is a second startup snapshot acceptable?
> - **Q-WS3-5 — `flask run` callers.** Keep and repair (`flask init-runtime` CLI command registered in `create_app()`, used by `.vscode/launch.json` config 1 and `e2e/run_puppeteer_summary_regression.ps1`), or retire the Puppeteer runner and leave only the VS Code config? If retired, that is a separate E2E-row change.
> - **Q-WS3-6 — File boundary for `init_runtime()`.** Confirm A2 (`utils/runtime_init.py`) or keep it inside `app.py`.

The full rev 1 text, including its acceptance criteria, scope and assumptions, is in the preimage cited in the Revision history. Rev 2 keeps the AC numbering, so rev 1 criteria map one-to-one.

---

## Plan v1

*Written 2026-10-20 (rev 3) by a fresh `product-manager` (`a9259355287e3c511`) after the owner signed Gate 0. It builds on Section 0 and does not repeat its investigation.*

*Source note. **Every `path:line` citation in Plan v1 is against `origin/main` `f3adacf1c1b48cc6e2c7ca9ac900e3294b3bae2d`**, read from the byte-exact `git archive` snapshot at `artifacts/ws3-app-factory-20261020/src-f3adacf1/` (gitignored, prepared by the manager).*

*Correction to the first draft. The draft relied on a manager brief saying the shared checkout's working tree was a valid read source; the manager has since withdrawn that. The shared checkout's `HEAD` is `85e23725`, which is **not** an ancestor of `origin/main`; `f3adacf1` is 81 commits ahead. In the WS3 source set (`app.py`, `app_launcher.py`, `utils/`, `routes/`, `tests/conftest.py`, `scripts/smoke_packaged_app.py`, `.vscode/`, the Puppeteer `.ps1`), the only differences are three files unrelated to WS3: `utils/export_service.py`, `utils/rep_range_integrity.py` and `utils/workout_validation.py`. 22 test files differ.*

*Every citation the draft took from the working tree outside that identical set was re-checked against the snapshot:*
- *`tests/test_catalog_seed_bootstrap.py:125-130,141-144,159-170`, `tests/test_logger.py:227-239`, `tests/test_pattern_coverage.py:346-423,417`, `tests/test_erase_data_guard.py:3-13,17-18,94-95`, `tests/test_runtime_paths.py:200-222`, `tests/test_static_cache_policy.py:54,108,162`, the five token sites, `tests/test_css_cascade_contracts.py:1385`, `tests/test_worktree_snapshot.py:362` and `pyproject.toml` (vulture `min_confidence 100`): all unchanged.*
- *The two files the draft flagged as missing exist in the snapshot: `tests/test_export_blank_rep_bounds_contract.py` (`"requestId": None` at `:65`, inside `:58-67`) and `tests/test_export_blank_rep_bounds_gate0.py` (`:55`, inside `:47-57`). The `tests/test_agent_workflow_contracts.py` root-`CLAUDE.md` guard is at `:677-680`. That gap is withdrawn.*
- *Three citations taken from **uncommitted** shared-checkout edits did not hold at `f3adacf1` and are corrected:*
  - *`CLAUDE.md` §4B at `f3adacf1` (`:143-153`) **requires** a pre-change full-pytest baseline under `artifacts/` (step 1). The draft's "no blanket baseline" wording exists only in an uncommitted edit (§P8 S1, §P12 item 2).*
  - *`CLAUDE.md` at `f3adacf1` has no "Reasoning effort is not agent authorization" section (§P13).*
  - *`QUALITY_GATE.md` at `f3adacf1` defines `/verify-and-polish` as `/verify-suite` + `code-reviewer` + `unslop-reviewer` (*Two gates, two purposes*, `:153-156`), and has an *Owner approvals and reviewer passes* section (`:22-40`) (§P13).*
- *The `QUALITY_GATE.md` rows used here are at `:46` (Route / API), `:47` (DB / schema), `:48` (Business logic), `:53` (E2E spec), `:56` (AI workflow), `:57` (Product docs) and `:132` (targeted-test fallback).*

**Goal**: `import app` does no database or data-directory work. Production, the packaged launcher, `flask run` and the test suite build the application through `create_app()`, and every runtime initialization goes through one guarded `init_runtime()`. Startup order, production API shapes, calculations and the `/erase-data` contract are unchanged.

**Scope**
- **In**: Section 0 *In scope*, made concrete by §P1 below.
- **Out**: Section 0 *Out of scope / non-goals*, unchanged. In addition, WS3 does not edit any DB-row file (`utils/db_initializer.py`, `utils/database.py`, `utils/auto_backup.py`, `utils/program_backup.py`) or any runtime-step module (`utils/runtime_migration.py`, `utils/catalog_seed.py`, `utils/catalog_upgrade.py`, `utils/schema_registry.py`). The guard lives only in the new module. Also untouched: `scripts/**`, `.github/**`, `Hypertrophy-Toolbox.spec`, `START.bat`, `RUN_APP.bat`, `playwright.config.ts`.

**Effort**: L · **Owner**: a manager-led implementation session in an owner-created standalone clone (RP-1). `automation-qa` writes tests; `senior-developer` writes production code, launch configurations, documentation and the regenerated inventory · **Depends on**: owner Gate 1; IC-1…IC-8; RP-1…RP-5; proposed RP-6 and RP-7 (§P16).

### P1. File manifest

| Path | Change | Purpose | Agent | Step |
|---|---|---|---|---|
| `utils/runtime_init.py` | **new** | `RuntimeInitOutcome`, `init_runtime(db_file=None)`, `should_initialize_runtime(use_reloader)`, private `_reset_for_tests()` (§P5). Imports only `utils` modules and Werkzeug. | `senior-developer` | S3 |
| `app.py` | modify | Adds `create_app(config_overrides=None)`, `create_initialized_app()` and `main()`. Module-level `logger = get_logger()` replaces `setup_logging(app)` (`:72`). The filter, hook, context-processor and view functions move to module level and are registered by `create_app()`. `app = create_app()` stays at module level. Removed: the five runtime steps (`:92-108`), the debug listing (`:127-131`), `start_timer` (`:160-163`) and the now-unused imports (`prepare_runtime_database`, `bootstrap_runtime_database`, `upgrade_catalog_from_seed`, `setup_logging`, `g`, `time`). The `:303-306` comment is rewritten (§P4). | `senior-developer` | S4 |
| `app_launcher.py` | modify | `main()` calls `init_runtime()` right after `from app import app` (`:69`), inside the existing `try`. Nothing else changes. | `senior-developer` | S4 |
| `utils/logger.py` | modify | Delete the `if app:` branch (`:74-114`) and the `app` parameter of `setup_logging()` (`:25`). Handlers, formats, levels and the early return are unchanged. | `senior-developer` | S4 |
| `.vscode/launch.json` | modify | `:23` becomes `"FLASK_APP": "app:create_initialized_app"`. The comment at `:5-10` is corrected: startup no longer runs at import, and `--no-reload` stays load-bearing because the factory initializes in every process that loads it. | `senior-developer` | S4 |
| `e2e/run_puppeteer_summary_regression.ps1` | modify | `:29` becomes `$env:FLASK_APP = "app:create_initialized_app"`. | `senior-developer` | S4 |
| `tests/test_runtime_init.py` | **new** | AC2 boundary, AC3(a)–(f), AC5b, the reset contract, the reloader helper and the outcome fields (§P11). | `automation-qa` | S2 |
| `tests/test_app_factory.py` | **new** | AC4, AC6 fixture identity, AC7 (mocked `main()` and launcher), AC8 success and failure paths, AC9, AC10 promise text, AC11, and the A8 probes (§P15). | `automation-qa` | S2 |
| `tests/test_real_app_db_isolation.py` | modify | AC1 import probes; init-subject probes replace the import-subject ones; the negative test is replaced (A4); the docstring is rewritten. `test_real_app_client_lands_on_its_scratch_database` is unchanged. | `automation-qa` | S2 |
| `tests/test_runtime_paths.py` | modify | The body of `TestPacketB2MovesTheDatabase::test_startup_migrates_before_it_seeds` (`:200-222`) becomes the mock-based AC2 order test over `utils.runtime_init.init_runtime`. Name and docstring intent are kept. | `automation-qa` | S2 |
| `tests/test_catalog_seed_bootstrap.py` | modify | The subprocess of `test_real_app_first_install_seeds_catalog_without_mutating_seed` (`:141-144`) runs `import app; assert app.create_initialized_app().test_client().get('/').status_code == 200`. All assertions at `:159-170` are unchanged. | `automation-qa` | S2 |
| `tests/test_logger.py` | modify | `TestFlaskIntegration::test_flask_app_provided_configures_app_logger` (`:227-239`) is replaced by `test_setup_logging_takes_no_app_argument`, which uses `inspect.signature`. | `automation-qa` | S2 |
| `tests/conftest.py` | modify | The `app` fixture builds `create_app(config_overrides={"TESTING": True, "WTF_CSRF_ENABLED": False})` via a lazy `from app import create_app` inside the fixture. The twin is deleted: the 13 blueprint imports (`:10-22`), the copied filter, the guard-less route, and `_initialize_test_database` if nothing else uses it. `real_app_client` moves to explicit init (§P3 row 5). Docstrings are corrected. | `automation-qa` | S5 |
| `tests/test_export_blank_rep_bounds_contract.py:58-67`, `tests/test_export_blank_rep_bounds_gate0.py:47-57` | modify | `"requestId": None` becomes equality with the response's `X-Request-ID` header, which must also match `^req_[0-9a-f]{16}$` (D-15). | `automation-qa` | S5 |
| `tests/test_database_user_profile.py:170`, `tests/test_db_migration.py:171`, `tests/test_program_backup.py:822,838,855` | modify | Each call sends `json={"confirm": "ERASE_ALL_DATA"}`. All following assertions are unchanged (A3). | `automation-qa` | S5 |
| `tests/test_pattern_coverage.py` | modify | Delete the dead `app_client` fixture (`:346-423`, method of a test class; its `from app import app` is at `:417`). The deletion reason goes in the PR. | `automation-qa` | S5 |
| `tests/test_erase_data_guard.py` | modify (docstring only) | `:3-13` and `:17-18` describe the conftest twin, which no longer exists. Assertions are unchanged. | `automation-qa` | S5 |
| `CLAUDE.md` and the F9 `f3adacf1` documentation list | modify in place | AC10 and AC13. `CLAUDE.md` §2 startup block (`:45-54`), `:58`, and §4A (`:136`) gain the Q-WS3-2(a) promise verbatim and stay under 200 lines. Also corrected: `.claude/rules/routes.md:50-51`; `.claude/rules/testing.md:63,121-123,126`; the `.claude/rules/database.md` startup and adding-a-table sentences that WS3 makes false (`:58-66,77-80,97,116,127,153-162`); `.claude/rules/debugging.md:27,29-31,39`; `.claude/agents/architecture-reviewer.md:17,19`; `.claude/agents/code-reviewer.md:13`; `.claude/agents/test-strategist.md:27,32`; `routes/CLAUDE.md:21,25`; `tests/CLAUDE.md:45,73,74`; `docs/ai_workflow/PARALLEL_WORKFLOW.md:7,132` where made false; `docs/product/README.md:191-195`; `docs/DUPLICATION_REGISTRY.md:53`; `docs/E2E_TESTING.md:88-89`. `docs/ai_workflow/AUTONOMY.md:18,144` gets a wording change only, to "blueprint registration in `create_app()` (`app.py`)". **The explicit-confirmation rule itself is not changed**, because an autonomy change belongs to WS2. No file under `.claude/**` is added or deleted. | `senior-developer` | S6 |
| `docs/test_inventory/*` | regenerate | `Test Inventory Drift` (RP-5). | `senior-developer` | S7 |

**Verified to need no edit**: `scripts/smoke_packaged_app.py` (A5); `tests/test_static_cache_policy.py`, whose `frozen_cache_client` still mutates the same module-level object that `real_app_client` wraps (§P3 row 5); `tests/test_css_cascade_contracts.py:1385`, which reads `app.py` text for a dead element id that WS3 does not add; `tests/test_trailing_slash_routing.py`; `tests/test_local_first_assets.py`; the five self-built minimal test apps (F1a); `e2e/scripts/*`; `tests/fixtures/make_old_schema_db.py`; `tests/test_worktree_snapshot.py:362`; and `docs/archive/**`.

### P2. Module boundaries

- `app.py` gains one import edge, `from utils.runtime_init import init_runtime, should_initialize_runtime`. Its other imports are today's set minus the removed ones. `create_app()` stays in `app.py` (Q-WS3-6).
- `utils/runtime_init.py` imports only `os`, `threading`, `dataclasses`, `pathlib` and `werkzeug.serving.is_running_from_reloader`. From `utils` it imports `utils.config` as a module object, plus `get_logger`, `runtime_root`, and the five step functions by name. Importing the module object keeps `importlib.reload(utils.config)` in `tests/test_runtime_paths.py` and `tests/test_catalog_seed_bootstrap.py:125-130` visible. Importing the step functions by name lets tests patch `utils.runtime_init.<step>`. The module does not import `flask`, `routes`, `app` or `app_launcher`; a test enforces this (AC2).
- `create_app()` calls no runtime step and never calls `setup_logging()`, `DatabaseHandler`, `sqlite3` or any filesystem function. `init_runtime()` never touches a Flask object. The two are independent and are joined only by entry points (§P3).
- The direction rule is unchanged: `routes` → `utils`, never the reverse.

### P3. Configuration → logging → factory → runtime-initialization order, per entry point

"Configuration" means the environment (`DB_FILE`, `HT_RUNTIME_DIR`, `HT_PORT`, `FLASK_DEBUG`, `FLASK_USE_RELOADER`, `TESTING`, `HT_NO_BROWSER`). `utils.config.DB_FILE` is resolved from the environment when `utils.config` is first imported (`config.py:22`). After WS3 it is reassigned **only** by `init_runtime()`. The logging root is fixed by `HT_RUNTIME_DIR` at the process's first `get_logger()` call, as today (F5). The port is read only at serve time (`runtime_port()`), as today.

| # | Entry point (callers) | 1. Configuration | 2. Logging | 3. Factory | 4. Runtime initialization | 5. Serve |
|---|---|---|---|---|---|---|
| 1 | `python app.py`: `START.bat:136`, Playwright webServer, `deep-gate.yml` ×3, `release.yml` ×2, the seven `css_audit` spawners, VS Code config 2, packaged payload `app.pyc` | `require_supported_python()` (`app.py:8-10`); `import utils.config` (`:13`) resolves `DB_FILE` | First `get_logger()` during `from utils.database import …` (`:14`); then module `logger = get_logger()` (cached) | Module-level `app = create_app()` in the `__main__` module | `main()` reads `FLASK_USE_RELOADER` and `FLASK_DEBUG`. If `should_initialize_runtime(use_reloader)`, it calls `init_runtime()`. It then registers the atexit and SIGINT/SIGTERM WAL cleanup, after initialization as today. | `app.run(port=utils.config.runtime_port(), debug=…, use_reloader=…)` |
| 2 | Packaged bootloader `app_launcher.main()`: `Hypertrophy-Toolbox.exe`, `RUN_APP.bat:4`, smoke `--mode bootloader` | At launcher import: frozen `chdir` and `sys.path` (`app_launcher.py:31-45`). In `main()`: `require_supported_python()`, then `runtime_port()` (imports `utils.config`; no logging yet) | `from app import app` (`:69`) configures logging transitively | Module-level `app = create_app()` in module `app` | `from utils.runtime_init import init_runtime; init_runtime()` immediately after the import, inside the same `try`. A failure reaches the existing error-wait UX (`:100-110`). The import is lazy so `require_supported_python()` still runs first (D-11). | Browser thread unless `HT_NO_BROWSER=1`; `app.run(host='127.0.0.1', port=port, debug=False, threaded=True, use_reloader=False)` |
| 3 | `flask run` with `FLASK_APP=app:create_initialized_app` and `--no-reload`: `.vscode/launch.json` config 1, the Puppeteer `.ps1` | Environment as launched | The Flask CLI imports module `app` (transitive) | Import builds module-level `app` #1, which is never served. The CLI then calls `create_initialized_app()`, which builds `app` #2. | `create_initialized_app()` calls `init_runtime()` before `create_app()`. It applies no reloader rule (D-10). | `flask run` serves #2 |
| 4 | pytest `app` fixture (function scope) | `conftest.py:30` sets `TESTING=1`. Per test, `utils.config.DB_FILE = test_db_path` | Already configured by `conftest.py:9` (`utils.database`) | Lazy `from app import create_app`; the first use constructs module-level `app` with no init. Then `create_app(config_overrides={"TESTING": True, "WTF_CSRF_ENABLED": False})` | **None.** The schema is a copy of `schema_template` (`conftest.py:296-300`), so it stays unseeded. | Test client |
| 5 | `real_app_client` (module scope) | Sets env `DB_FILE` and `HT_RUNTIME_DIR` to scratch, keeping today's lines `:174,179` (D-13), plus the attribute | Already configured | `from app import app as real_app` returns the module-level object, with no init | `_reset_for_tests()`, then `outcome = init_runtime(db_file=str(scratch_db))`. The steps: explicit override, then `DB_FILE` set to scratch, then the seed copy (`seeded=True`), then `run_all_initializers(force_base=False)`; upgrade and backup are skipped. The fixture asserts that `outcome.database_path` and `utils.config.DB_FILE` both resolve to the scratch file, otherwise `pytest.fail`. Teardown restores the environment and attribute and calls `_reset_for_tests()`. | `real_app.config['TESTING'] = True`; test client |
| 6 | Subprocess tests | Explicit `env` per probe | First `get_logger()` happens inside the probe | (a) AC1 probes: `import app` only. (b) First install: `import app; app.create_initialized_app()`. | (a) none. (b) once. (c) Init probes call `init_runtime(...)` directly without the factory. | (b) test client only |
| 7 | Packaged smoke's own process (`smoke_packaged_app.py:247`) | Smoke environment (no `DB_FILE` or `HT_RUNTIME_DIR`) | `from app import STATIC_LONG_MAX_AGE_SECONDS` configures logging transitively | Module-level `create_app()` | **None.** This is the A5 behavior change. Child processes follow row 1 (payload) or row 2 (bootloader). | — |

**Equivalence of `real_app_client` to today.** Today the fixture calls `bootstrap_runtime_database()` and then `run_all_initializers(force_base=True)` (`conftest.py:204-206`). Under `TESTING=1` the `initialize_database()` guard is bypassed whatever `force` is (`db_initializer.py:569,575`). So `force_base=False` builds the identical schema. On a just-seeded scratch database the upgrade and backup are skipped, and `create_startup_backup()` would return `None` under `TESTING=1` anyway (`auto_backup.py:45-46`). The scratch database therefore ends in the same state, including the seeded catalog that `test_rejected_erase_leaves_the_catalog_intact` requires (`test_erase_data_guard.py:94-95`). The old "fail before any write" check (`conftest.py:184-199`) has no counterpart between steps. It is no longer needed because the explicit-argument branch is the first branch of `prepare_runtime_database()` (`runtime_migration.py:236-242`). AC5b proves that branch, and the fixture still asserts the result before yielding.

### P4. `create_app()` and the shape of `app.py`

```python
# app.py, in module order
from utils.python_version import require_supported_python
require_supported_python()
# imports: today's set (:12-45), minus prepare_runtime_database, bootstrap_runtime_database,
#          upgrade_catalog_from_seed, setup_logging, g, time; plus:
from flask import current_app
from utils.logger import get_logger
from utils.runtime_init import init_runtime, should_initialize_runtime

STATIC_LONG_MAX_AGE_SECONDS = 31536000          # unchanged (:50)
logger = get_logger()                           # replaces setup_logging(app) (:72)

def format_datetime(value, date_format='%d-%m-%Y'): ...     # body verbatim (:134-145)
def safe_media_path(value): ...                             # body verbatim (:149-158)
def apply_static_cache_policy(response): ...                # body verbatim except
                                                            # app.config -> current_app.config (:196)
def inject_app_version(): ...                               # verbatim (:210-222)
def inject_scale_level(): ...                               # verbatim (:226-241)
def erase_data(): ...                                       # body verbatim (:246-271)

def create_app(config_overrides: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(__name__)                                   # F3: Flask
    app.url_map.strict_slashes = False                      # F3: before any rule exists (A8c)
    app.wsgi_app = ProxyFix(app.wsgi_app)                   # F3: ProxyFix
    if getattr(sys, 'frozen', False):                       # F3: frozen block, verbatim (:57-69)
        ...
    if config_overrides:                                    # 3b: after the frozen block
        app.config.update(config_overrides)
    add_request_id_middleware(app)                          # F3 order
    register_error_handlers(app)                            # F3 order; errors.py:232-236
    register_fallback_handlers(app)
    for blueprint in (main_bp, workout_log_bp, weekly_summary_bp, session_summary_bp,
                      exports_bp, filters_bp, workout_plan_bp, progression_plan_bp,
                      user_profile_bp, body_composition_bp, volume_splitter_bp,
                      program_backup_bp, fatigue_bp):       # today's 13, today's order (:111-125)
        app.register_blueprint(blueprint)
    app.add_template_filter(format_datetime, 'datetime')
    app.add_template_filter(safe_media_path, 'safe_media_path')
    app.after_request(apply_static_cache_policy)
    app.context_processor(inject_app_version)
    app.context_processor(inject_scale_level)
    app.add_url_rule('/erase-data', endpoint='erase_data', view_func=erase_data, methods=['POST'])
    return app

def create_initialized_app() -> Flask:
    init_runtime()
    return create_app()

app = create_app()

def main() -> None:                                         # today's __main__ body (:275-314)
    use_reloader = os.getenv('FLASK_USE_RELOADER', '0') == '1'
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    if should_initialize_runtime(use_reloader):
        init_runtime()
    # cleanup_on_exit / signal_handler definitions and registration: verbatim
    app.run(port=utils.config.runtime_port(), debug=debug_mode, use_reloader=use_reloader)

if __name__ == "__main__":
    main()
```

**Compared with F3.** The construction order is F3's order with four items removed. The three settings `Flask`, `strict_slashes` and `ProxyFix` come first, then the frozen block, request-id, error handlers, fallback handlers, the 13 blueprints, the `datetime` and `safe_media_path` filters, the cache policy, the two context processors and `/erase-data`. The removed items are `setup_logging(app)` (Q-WS3-2a), the five runtime steps (now `init_runtime()`), the debug listing (3a) and `start_timer` (Q-WS3-2H). The only new step is `config_overrides`, applied right after the frozen block. Before WS3 the runtime steps ran between the handlers and the blueprints. They touch no Flask object, so moving them out changes no app state (F8a: no hook or processor touches the DB).

**The `:303-306` comment** becomes: "`use_reloader` defaults to off. With `FLASK_USE_RELOADER=1`, only the serving child initializes the runtime (see `should_initialize_runtime`). For `flask run`, use `FLASK_APP=app:create_initialized_app` with `--no-reload`." It no longer recommends a bare `flask run --reload` (AC11).

### P5. `init_runtime()` specification

```python
# utils/runtime_init.py
@dataclass(frozen=True)
class RuntimeInitOutcome:
    database_path: Path          # migration.database_path, as assigned to utils.config.DB_FILE
    migration_action: str        # explicit-override | same-path | already-present | no-legacy | migrated | failed
    seeded: bool                 # this process published this database from the seed (incl. a failed earlier attempt)
    snapshot_path: Path | None   # create_startup_backup() result, or None when skipped
    already_initialized: bool    # True only on a guarded no-op return

_lock = threading.Lock()
_completed: tuple[tuple[str | None, str], RuntimeInitOutcome] | None = None
_seeded_databases: set[str] = set()            # resolved database paths seeded in this process

def _guard_key(explicit: str | None) -> tuple[str | None, str]:
    requested = explicit if explicit is not None else (os.environ.get("DB_FILE") or None)
    requested_key = str(Path(requested).expanduser().resolve()) if requested else None
    return (requested_key, str(runtime_root()))            # rule (i)

def init_runtime(db_file: str | os.PathLike[str] | None = None) -> RuntimeInitOutcome:
    global _completed
    if db_file is not None and not os.fspath(db_file):
        raise ValueError("db_file must be a non-empty path or None")          # D-6
    explicit = os.fspath(db_file) if db_file is not None else None
    with _lock:
        key = _guard_key(explicit)
        if os.environ.get("TESTING") == "1" and key[0] is None:              # rule (v), before any file access
            raise RuntimeError("init_runtime() refuses to run under TESTING=1 without "
                               "an explicit db_file or a DB_FILE environment variable")
        if _completed is not None:
            done_key, done = _completed
            if key == done_key:                                              # rule (ii)
                logger.debug("Runtime already initialized for %s; skipping", done.database_path)
                return dataclasses.replace(done, already_initialized=True)
            raise RuntimeError(f"init_runtime() already initialized {done_key}; "  # rule (iii) / 4a
                               f"refusing a different database or runtime root {key}")
        # Rule (iv): any exception below propagates with _completed still None.
        migration = prepare_runtime_database(explicit_override=explicit)     # step 1 (never raises)
        utils.config.DB_FILE = str(migration.database_path)                  # step 2, the only assignment
        seeded_now = bootstrap_runtime_database()                            # step 3
        database_key = str(Path(utils.config.DB_FILE).expanduser().resolve())
        if seeded_now:
            _seeded_databases.add(database_key)                              # 4c carry-over
        seeded = database_key in _seeded_databases
        run_all_initializers(force_base=False)                               # step 4
        snapshot = None
        if not seeded:
            upgrade_catalog_from_seed()                                      # step 5
            snapshot = create_startup_backup()                               # step 6 (never raises)
        outcome = RuntimeInitOutcome(Path(migration.database_path), migration.action,
                                     seeded, snapshot, False)
        _completed = (key, outcome)
        logger.info("Runtime initialized: database=%s migration=%s seeded=%s snapshot=%s",
                    outcome.database_path, outcome.migration_action, seeded, snapshot)
        return outcome

def should_initialize_runtime(use_reloader: bool) -> bool:
    """Reloader rule: initialize only in the serving process."""
    return (not use_reloader) or is_running_from_reloader()

def _reset_for_tests() -> None:
    """Test-only (rule vi). Never called by production code; tests enforce this."""
    global _completed
    with _lock:
        _completed = None
        _seeded_databases.clear()
```

**Rules mapped to the accepted recommendation:**
- (i) The key is (resolved requested database, or `None` when neither the argument nor env `DB_FILE` is set; `runtime_root()` at call time). It is stored only after every step succeeds.
- (ii) The same key is a no-op. It returns the cached outcome with `already_initialized=True`.
- (iii) A different key raises `RuntimeError` before any step, so `utils.config.DB_FILE` is untouched (4a).
- (iv) An exception leaves the guard unset, so the same call may be retried.
- 4c: the seeded carry-over is keyed by the resolved **database path**, not the guard key (D-4).
- (v) Under `TESTING=1`, a call with no explicit path refuses before any file access (4b).
- (vi) `_reset_for_tests()` (4d).
- The reloader rule lives in `should_initialize_runtime()`.

**What it does not touch:** `utils.db_initializer._INITIALIZATION_COMPLETE`, which keeps its own semantics (D-17). `/erase-data` keeps calling `create_startup_backup()`, `drop_all_owned_tables()` and `run_all_initializers(force_base=True)` directly, so on-demand snapshots are unaffected. A `failed` migration still proceeds on the legacy path, as today (`runtime_migration.py:258-265`); `init_runtime()` adds no new failure mode for it.

### P6. Repeated factory and repeated runtime behavior

**Repeated `create_app()`.** Each call returns a new `Flask` instance with its own `config`, `url_map` and handler maps. The 13 module-level blueprint objects are registered on each instance; Flask allows this across instances, and today's suite already does it for every twin. The hook, filter and view functions are the same module-level objects on every instance. No logging handler is added: `get_logger()` is cached and `create_app()` attaches none, so the logger keeps exactly one `RotatingFileHandler` and one console handler. No database, data-directory, migration, seed, upgrade or snapshot work happens. Building a new instance does not change the module-level `app` or any earlier instance. In a pytest process this means one module-level instance plus one per `app`-fixture test.

**Repeated `init_runtime()` in one process.**

| Situation | Result |
|---|---|
| Same key after success | No-op; cached outcome with `already_initialized=True`; no step runs; no snapshot |
| Different key (database or runtime root) after success | `RuntimeError`; nothing runs; `utils.config.DB_FILE` unchanged |
| Retry after an exception | Runs all steps again. A database seeded by the failed attempt counts as `seeded`, so upgrade and backup stay skipped. |
| `TESTING=1` with no explicit path and no env `DB_FILE` | `RuntimeError` before any file access, on every call |
| After `_reset_for_tests()` | Behaves as a first call; tests only |
| Reloader on (`python app.py`) | Parent: `should_initialize_runtime` is false, so no call. Serving child: one call. |
| `flask run --reload` (not a supported caller) | Unmeasured. A8b decides whether the reloader parent also calls `create_initialized_app()`; §P15 records what changes either way. |

### P7. Caller migration, caller by caller

| Caller | Today | After WS3 | Edit |
|---|---|---|---|
| `app_launcher.py:69` | `from app import app` runs startup | Import, then explicit `init_runtime()` | Yes (S4) |
| `python app.py` callers (§P3 row 1) | `__main__` after import-time startup | `main()`, with init under the reloader rule | None to callers |
| `.vscode/launch.json:23` | `FLASK_APP=app.py` | `app:create_initialized_app` | Yes (S4), plus the comment |
| `e2e/run_puppeteer_summary_regression.ps1:29` | `FLASK_APP=app:app` | `app:create_initialized_app` | Yes (S4) |
| `app.py:306` comment | Recommends `flask run --reload` | §P4 text | Yes (S4) |
| `tests/conftest.py` `app` | Hand-built twin | `create_app(config_overrides=…)`; no init | Yes (S5) |
| `tests/conftest.py` `real_app_client` | Import-time startup, path assertion, then bootstrap and initializers | Explicit `_reset_for_tests()` + `init_runtime(db_file=…)` | Yes (S5) |
| `tests/test_static_cache_policy.py:54,108,162` | Module-level `app`, constant | Unchanged | None |
| `tests/test_pattern_coverage.py:417` | Dead fixture | Deleted | Yes (S5) |
| `tests/test_real_app_db_isolation.py` | `import app` subject | `import app` for AC1; `init_runtime()` for AC5 | Yes (S2) |
| `tests/test_catalog_seed_bootstrap.py:142` | `import app` seeds | `app.create_initialized_app()` seeds | Yes (S2) |
| `tests/test_runtime_paths.py:200-222` | AST line order in `app.py` | Mock order over `init_runtime` | Yes (S2) |
| `scripts/smoke_packaged_app.py:247` | Import runs startup in the smoke process | Import only (A5) | None |
| `docs/product/README.md:191` | Command runs startup | Command lists routes with no data work | Prose `:194-195` (S6) |
| `docs/archive/2026/one-off-scripts/fatigue/*` | `from app import app` | Still imports; no longer initializes | None (archived, not executed) |
| `e2e/scripts/prepare_*`, `tests/fixtures/make_old_schema_db.py`, F1a minimal apps | Do not import `app` | Unchanged | None |

### P8. Sequencing (steps, commits, agents)

- **S0 — Readiness (manager; no code).** Record IC-1…IC-8, RP-1 and RP-2. Fetch `origin/main` in the standalone clone. If the base is not `f3adacf1`, run `git diff --stat f3adacf1 <base> -- <every §P1 path>`. If that diff is non-empty, the `product-manager` revises the affected parts of the plan before S2. Record the private paths: venv, `HT_RUNTIME_DIR`, `TEMP`/`TMP` (created, `len <= 103`), `PYTHONPYCACHEPREFIX` and the npm cache.
- **S1 — Pre-change evidence (`senior-developer`, scratch only, output under `artifacts/ws3-impl-<date>/`).** (a) Capture the URL map at the base revision, using the `docs/product/README.md:191` command with a scratch `HT_RUNTIME_DIR` and `DB_FILE`. Record each rule's text, endpoint and methods (D-16). (b) Run the A6 and A11 read-only greps (§P15). (c) Record the pre-change full-pytest baseline in the clone under `artifacts/`, as `CLAUDE.md` §4B step 1 requires at `f3adacf1` (`:144-148`).
- **S2 — Acceptance tests first (`automation-qa`, from the approved Plan v2).** Write the two new files and the S2 rows of §P1. They are expected to fail on unchanged code, with ImportErrors for `utils.runtime_init` and `create_app` and assertion failures in the rewritten probes. **Commit C1** `test(app-factory): WS3 acceptance tests (red until C3)`.
- **S3 — `utils/runtime_init.py` (`senior-developer`).** **Commit C2.** Expected green: `tests/test_runtime_init.py` and the AC2 order test.
- **S4 — Factory, launchers and logger (`senior-developer`).** `app.py`, `app_launcher.py`, `utils/logger.py`, `.vscode/launch.json` and the `.ps1` go in **one commit, C3**. The `flask run` repairs must land with the factory (D-19). Expected green: `tests/test_app_factory.py` except its AC6 fixture-identity test, the AC1 and AC5 probes, the first-install test and `tests/test_logger.py`.
- **S5 — Harness migration (`automation-qa`).** `tests/conftest.py`, the two `requestId` tests, the five token sites, the dead fixture and the guard-test docstring go in **commit C4**. Then run full pytest in the clone and triage under A11 (§P15). These changes are consequences of the conftest switch, so they land with it, and every commit from C4 on is green.
- **S6 — Documentation (`senior-developer`).** AC10 and AC13 edits in **commit C5**. Every edit starts from the fetched-main version of the file and is coordinated per RP-2 and IC-4.
- **S7 — Generated and static gates (`senior-developer`).** Regenerate `docs/test_inventory/` (RP-5) in **commit C6**. Run the pyright baseline diff, vulture and flake8 (§P12).
- **S8 — Diff-time gate (manager orchestrates).** `/verify-and-polish` in the clone: `/verify-suite`, the §P13 reviewers, the manual backup/restore smoke and the launch-path checks (§P12).
- **S9 — CI observation.** Pushing the branch and opening a PR are needed to observe RP-3. **This planning authorization does not cover them**; Gate 1 must name them (proposed RP-6). A merge needs separate explicit owner confirmation naming the PR.

**Landing unit.** One PR. C1 and C2 are red or unused only on the branch. If the PR is not squash-merged, C1 is folded into C3 before merge, so `main` never holds a red commit.

### P9. Compatibility changes (all intentional; carried into the PR's migration notes)

1. **C-1** `import app` no longer runs migration, seed, initializers, upgrade or backup. This affects ad-hoc `python -c "import app"` use, the smoke's own process (A5), `docs/product/README.md:191` (now free of data work) and the archived scripts.
2. **C-2** `utils.config.DB_FILE` is no longer reassigned at import. It holds the environment/resolver value until `init_runtime()` assigns it once. No production path reads it in between.
3. **C-3** `flask run` with `FLASK_APP=app.py` or `app:app` serves an **uninitialized** runtime. Both known callers are repaired. A personal habit must switch to `app:create_initialized_app`; `CLAUDE.md` and the routes rule say so (AC13).
4. **C-4** With the reloader on, `python app.py`'s monitoring parent no longer migrates, seeds or snapshots. The serving child does each once.
5. **C-5** New guard behavior: a repeat call with the same key is a no-op; a different key raises `RuntimeError`; `TESTING=1` without a path raises `RuntimeError`. No existing caller hits the raising branches.
6. **C-6** A new INFO line, "Runtime initialized: …", is logged once per initializing process (D-9). The existing schema-registry INFO lines are unchanged.
7. **C-7** The DEBUG route listing is no longer written to `app.log`.
8. **C-8** The never-attached request hooks and `start_timer` are deleted. `setup_logging()` no longer accepts `app`; its only caller passing one was `app.py:72`.
9. **C-9** `app` module attributes removed: `migration`, `database_seeded`, `start_timer`, and the imported names that are no longer used. New: `create_app`, `create_initialized_app`, `main`, and the imported `init_runtime` and `should_initialize_runtime`. The hook and filter functions are module-level. `apply_static_cache_policy` reads `current_app.config` (same values). No importer uses a removed name (grep, §P7).
10. **C-10** The `__main__` body moves into `main()`. `python app.py` behaves identically apart from C-4.
11. **C-11** The test harness's `app` is now the production factory app:
    - `requestId` is populated;
    - XHR and `/api/` 404/405 bodies are envelopes;
    - uncaught exceptions return 500 (A8d);
    - 404s log a WARNING to the run's `app.log`;
    - `/erase-data` requires the token;
    - `app.name` is `"app"`, not `"conftest"`.
12. **C-12** `test_patching_config_alone_is_not_isolation` is replaced (A4). `real_app_client` no longer depends on import order.
13. **C-13** The launcher initializes explicitly after the import, with the same console text and the same error-wait UX.

**Unchanged:** production API response shapes, calculations, schema, migration/seed/upgrade/backup semantics, the `/erase-data` contract, journal mode and `FLASK_DEBUG` defaults, port handling, frozen static caching and the WAL cleanup.

### P10. Rollback

- **Mechanism:** one `git revert` of the landed PR commit. That restores import-time startup, the twin and the old docs together. The revert also restores the committed `docs/test_inventory/` that matches the restored tests.
- **No data rollback:** WS3 has no schema or data migration. Databases, snapshots and logs written by a WS3 build use the same formats and paths, and a reverted build reads them unchanged. The only persistent difference is fewer snapshots in the reloader-parent case (C-4), which needs no reversal.
- **Partial states (branch only):** after C1, tests are red. After C2, an unused module is present and behavior is unchanged. After C3, production is migrated but the AC6 fixture-identity test stays red until C4. The old `real_app_client` still works at C3: import no longer reassigns `DB_FILE`, so its scratch-path assertion holds. **Must never reach `main`:** C3 without the `flask run` repairs (D-19), or C5's docs without C3's code, which would describe behavior that does not exist.
- **After merge:** if one launch path alone regresses, the default is to revert the whole PR. A forward fix instead is an owner decision at that time.

### P11. Acceptance criterion → test mapping

| AC | Test(s) | New / changed | Gate that runs it |
|---|---|---|---|
| 1 | `test_real_app_db_isolation.py`: `test_import_creates_no_data_without_db_file`, `test_import_creates_no_data_with_missing_db_file`, `test_import_creates_no_data_with_patched_attribute_only`, `test_constant_import_creates_no_data` (the smoke's `from app import STATIC_LONG_MAX_AGE_SECONDS`). Each runs in a fresh subprocess with `TESTING` removed. The probe counts `flask.Flask.__init__` calls (exactly 1), checks `isinstance(app.app, Flask)`, lists the scratch tree (only `logs/` and `logs/app.log` allowed), checks that the env-resolved database does not exist, that `utils.config.DB_FILE` equals its pre-import value, and that `auto_backup/` is absent under the scratch tree, under the `DB_FILE` parent and in the clone's `data/` listing (before and after). The no-`DB_FILE` cases keep `_skip_if_legacy_database_is_busy`. | Changed file; 4 new tests replace the import-subject tests | pytest (Route/API row via `/verify-suite`) |
| 2 | `test_runtime_paths.py::TestPacketB2MovesTheDatabase::test_startup_migrates_before_it_seeds`, rewritten. A shared recorder mocks the five steps. Each mock records `utils.config.DB_FILE` at its call: `prepare` sees the sentinel; `bootstrap`, the initializers, upgrade and backup all see the migration path (D-14). `force_base=False` is asserted. A second case has `bootstrap` return `True` and asserts that upgrade and backup are skipped. `test_runtime_init.py::test_outcome_fields` and `::test_module_imports_no_routes_or_app` (AST). | Changed + new | pytest |
| 3 | `test_runtime_init.py`, with an autouse fixture that calls `_reset_for_tests()` before and after each test: `test_same_key_is_a_noop` (a), `test_different_database_raises_and_changes_nothing` and `test_different_runtime_root_raises` (b), `test_failed_call_leaves_guard_unset` (c), `test_retry_after_seed_skips_upgrade_and_backup` (d), `test_testing_without_path_refuses_before_any_step` (e), `test_reset_allows_a_different_key` (f), `test_reset_is_never_referenced_by_production_code` (scans `app.py`, `app_launcher.py`, `utils/**/*.py` except `runtime_init.py`, `routes/**/*.py` and `scripts/**/*.py`), and `test_second_call_takes_no_second_snapshot_subprocess`. The last is a real-file check: in a non-`TESTING` subprocess it calls `init_runtime(db_file=<copy of the seed>)` twice and expects exactly 1 file in `auto_backup/`. `/erase-data` snapshots on every call are covered under AC8. | New | pytest |
| 4 | `test_app_factory.py`: `test_two_factory_calls_build_distinct_equivalent_apps` (13 blueprint names from a hard-coded list; equal rule sets to each other and to the module-level `app`), `test_every_rule_is_non_strict`, `test_proxyfix_wraps_wsgi_app`, `test_responses_carry_request_id` (static asset), `test_handler_layering_behaves_as_documented` (XHR 400 → `BAD_REQUEST`; 405 → `METHOD_NOT_ALLOWED` with `Allow`; 404 → `NOT_FOUND`; a temporary raising route → 500 `INTERNAL_ERROR`), `test_filters_hooks_processors_and_erase_route_present`, `test_only_request_id_and_cache_policy_hooks`, `test_config_overrides_apply_after_frozen_block` (monkeypatched `sys.frozen`), `test_no_route_listing_logged` (caplog at DEBUG), `test_factory_does_no_logging_setup_or_database_work` (`setup_logging` and `sqlite3.connect` patched to raise; the `DB_FILE` target is not created), `test_logger_keeps_one_file_and_one_console_handler`. **One-off evidence** (not a permanent test): the S1 URL-map capture diffed against the post-C3 capture (D-16). | New | pytest; S8 evidence |
| 5a | `test_runtime_paths.py::TestEnvironmentOverride`, **unmodified** | Unchanged | pytest |
| 5b | `test_runtime_init.py::test_explicit_argument_wins` (mocked), plus the subprocess `test_real_app_db_isolation.py::test_init_runtime_explicit_argument_lands_on_scratch` (`TESTING=1`, no env `DB_FILE`; expects action `explicit-override`, `DB_FILE` equal to scratch, and no runtime database) | New | pytest |
| 5c | `test_real_app_db_isolation.py::test_init_runtime_ignores_patched_attribute`: a non-`TESTING` subprocess patches the attribute, sets no env `DB_FILE` and sets `HT_RUNTIME_DIR` to a sandbox, then calls `init_runtime()`. It expects the active database to be `<sandbox>/data/database.db` and the scratch file not to exist. It keeps the busy-sidecar skip. It replaces `test_patching_config_alone_is_not_isolation`, and the revision is recorded in the docstring. Also `test_init_runtime_with_env_db_file` and the parametrized `test_env_override_wins_regardless_of_config_patch`, whose subject is now `init_runtime()`. | Changed | pytest |
| 5d | `test_catalog_seed_bootstrap.py::test_real_app_first_install_seeds_catalog_without_mutating_seed`, driven through `create_initialized_app()`; assertions unchanged | Changed | pytest |
| 6 | Full suite on the migrated `tests/conftest.py`; `test_app_factory.py::test_app_fixture_is_the_factory_app` (13 blueprints, `erase_data` endpoint, `ProxyFix`, `TESTING` true); the in-process `test_real_app_db_isolation.py::test_real_app_client_lands_on_its_scratch_database`; the five `real_app_client` consumer modules passing in one serial process and under `-n 8 --dist loadfile`; the two `requestId` tests; the five token sites | Changed | `/verify-suite` |
| 7 | `test_app_factory.py`: `test_main_initializes_before_run`, `test_main_reloader_parent_does_not_initialize`, `test_main_reloader_child_initializes`, `test_main_honours_port_and_debug`, `test_launcher_initializes_after_import_before_run` (`HT_NO_BROWSER=1`, `HT_PORT`; checks the `app.run` kwargs), `test_launcher_init_failure_uses_error_wait` (`input` patched; `SystemExit(1)`), `test_runtime_init.py::test_should_initialize_runtime_matrix`. Real launches: packaged smoke in bootloader mode (CI) and payload mode (local), `deep-gate.yml`/`release.yml` jobs (A7), and Playwright's webServer. | New; real launches unchanged | pytest; CI packaged smoke (RP-3); `/verify-suite` |
| 8 | `test_erase_data_guard.py`, unchanged (rejections, catalog intact). `test_app_factory.py`: `test_erase_success_snapshots_then_drops_then_reinitializes` (mocks record the order and `force_base=True`; expects `data.auto_backup == {"filename": …}` and the exact message), `test_erase_success_without_snapshot_reports_none` (real path under `TESTING`), `test_erase_failure_returns_internal_error`, `test_erase_rejection_writes_nothing` (mocks not called) | Unchanged + new | pytest; E2E `erase-flow.spec.ts`, `fatigue.spec.ts` |
| 9 | `test_app_factory.py::test_frozen_block_values` (monkeypatched frozen state: `STATIC_LONG_MAX_AGE == STATIC_LONG_MAX_AGE_SECONDS`, `TEMPLATES_AUTO_RELOAD` false, `jinja_env.auto_reload` false, `DEBUG` and `TESTING` false); `test_public_import_surface` (`from app import app, STATIC_LONG_MAX_AGE_SECONDS, create_app, create_initialized_app`); `test_static_cache_policy.py`, unchanged; AC1's `test_constant_import_creates_no_data` | New + unchanged | pytest; packaged smoke |
| 10 | `test_app_factory.py::test_claude_md_states_the_import_promise` (verbatim string); `tests/test_agent_workflow_contracts.py` (the under-200-line guard) | New + unchanged | pytest |
| 11 | `test_app_factory.py::test_create_initialized_app_initializes_then_builds` (mocks; order init then create; init called once with no arguments); `test_flask_run_callers_use_the_factory` (`.vscode/launch.json` with `//` comments stripped, the `.ps1` text, and no "flask run --reload" in `app.py`); real path via AC5d; manual A8a check | New | pytest; S8 manual |
| 12 | §P12 as a whole | — | S8, plus CI (RP-3) |
| 13 | §P12 item 16 (greps) plus diff review by `code-reviewer` (AI-workflow row) | — | S8 |

**Expected gates** *(the template has `test-strategist` fill this in; this is the product-manager's proposal for that review)*
- pytest: the full suite via `/verify-suite`, because `app.py` and `tests/conftest.py` fall back to it. Targeted per commit: `tests/test_runtime_init.py`, `tests/test_app_factory.py`, `tests/test_real_app_db_isolation.py`, `tests/test_runtime_paths.py`, `tests/test_catalog_seed_bootstrap.py`, `tests/test_logger.py`, `tests/test_erase_data_guard.py`, `tests/test_static_cache_policy.py`, `tests/test_agent_workflow_contracts.py`.
- e2e: the full Chromium suite via `/verify-suite`. Specifically watch `erase-flow.spec.ts`, `program-backup.spec.ts`, `fatigue.spec.ts`, `smoke-navigation.spec.ts` and `summary-pages.spec.ts`.
- other: packaged smoke (RP-3), pyright baseline diff, vulture, flake8, inventory regeneration plus `--check`, and the `.ps1` run (A10).

### P12. Validation plan (all in the standalone clone with private paths, IC-1/IC-2; every evidence record names those paths)

1. **Per-commit targeted pytest** (`/run-tests <file>`) at C2–C4.
2. **Full pytest**, serial and `-n 8 --dist loadfile`. Then **`/verify-suite`** (full pytest + Chromium). Compare against the pre-change baseline that `CLAUDE.md` §4B step 1 requires at `f3adacf1` (`:144-148`), which S1(c) records in the clone under `artifacts/`. If a failure's origin is still unclear, reproduce it in an isolated base checkout of the fetched base. Treat the known exceptions in `QUALITY_GATE.md` *Known exceptions* as pre-existing only after confirming they reproduce on the base.
3. **Packaged-Windows smoke.** Bootloader mode must be observed green in CI (RP-3; needs RP-6). Payload mode runs locally after a PyInstaller build in the private venv. Payload evidence never stands in for bootloader evidence (`smoke_packaged_app.py:9-15`).
4. **Fresh-process import checks.** The AC1 subprocess tests, plus a manual `python -c "import app"` and `python -c "from app import STATIC_LONG_MAX_AGE_SECONDS"` with `HT_RUNTIME_DIR=<empty scratch>`. Record a directory listing before and after.
5. **Initialization-order checks.** The AC2 mock test. At runtime, for each launch path, `<scratch>/logs/app.log` shows the migration and seed lines followed by exactly one "Runtime initialized" line per serving process.
6. **First install.** The AC5d test. Manually, `python app.py` with an empty `HT_RUNTIME_DIR` must report `seeded=True`, 1,897 exercises and no `auto_backup/`.
7. **Existing-DB upgrade.** Build a database with `tests/fixtures/make_old_schema_db.py`, run `python app.py` with `DB_FILE` pointing at it and a free `HT_PORT`, and check: `GET /` returns 200; `catalog_version` is populated; exactly one snapshot exists beside the database. Stop the app and repeat; a second snapshot appears, one per process, as today.
8. **Legacy migration.** The smoke's `check_upgrade_migration` in bootloader mode (CI) and payload mode (local). A source checkout resolves `same-path`, so it cannot exercise the migration.
9. **Backup/restore.** Automated: `tests/test_program_backup.py`, `tests/test_auto_backup.py`, and E2E `program-backup.spec.ts` and `erase-flow.spec.ts`. Manual smoke via the `run-hypertrophy-toolbox` skill on a scratch runtime: create a program backup, change the plan, restore it, and confirm the plan; then erase through the UI and confirm that the banner names a snapshot file that exists in `<db dir>/auto_backup/`.
10. **Repeated initialization at runtime.** Run `FLASK_USE_RELOADER=1 python app.py` on a scratch runtime with an existing database. Expect 0 "Runtime initialized" lines from the parent, 1 per serving child, and 1 snapshot for that start.
11. **pyright.** `scripts/pyright_baseline_diff.py` must report no net-new diagnostics.
12. **vulture** (`pyproject.toml`, `min_confidence 100`) and **flake8** (the blocking F401/F811/E711/E712 gate named at `app.py:2-7`) must be clean. Removed imports must not linger.
13. **Test Inventory Drift.** `python scripts/generate_test_inventory.py`, then `--check` clean, in a clone with no untracked or gitignored `.md` in a globbed surface directory (RP-5).
14. **Workflow contracts.** Run `tests/test_agent_workflow_contracts.py`, plus every test that names an edited doc path, found with `rg -l "CLAUDE.md|rules/(routes|testing|database|debugging)|AUTONOMY.md|PARALLEL_WORKFLOW|DUPLICATION_REGISTRY|E2E_TESTING|product/README" tests`. No file under `.claude/**` or `docs/ai_workflow/**` is added or deleted.
15. **Launch paths.** `python app.py` (Playwright webServer, items 6–7, 9–10). `flask run` via `python -m flask --app app:create_initialized_app run --no-reload --port <free>` with the VS Code config's environment (A8a). The `.ps1` (A10). The bootloader (item 3).
16. **AC13 documentation greps** return nothing in the F9 files: `rg -n "register(ed)? in (\*\*)?both" CLAUDE.md .claude routes/CLAUDE.md tests/CLAUDE.md utils/CLAUDE.md docs/ai_workflow`, `rg -n "flask run --reload" app.py`, and `rg -n "Slow request detected|log_request_info|start_timer" --glob "!docs/archive/**"`. A reviewer reads each F9 line against the new behavior.
17. **URL-map evidence.** The S1 capture equals the post-C3 capture of `create_app().url_map` (D-16).

### P13. Independent implementation reviewers (from the `QUALITY_GATE.md` required-gate union)

| Manifest path(s) | `QUALITY_GATE.md` row | Reviewer required |
|---|---|---|
| `app.py` | Route / API | `code-reviewer`. `product-risk-reviewer` only "if response shape changes"; production shapes do not change (test-only bodies are C-11) |
| `utils/runtime_init.py`, `utils/logger.py` | Business logic (non-DB) | `code-reviewer` (no `effective_sets`/`weekly_summary`/`session_summary`/`progression`/`fatigue` touched) |
| `tests/**` incl. `tests/conftest.py`, `app_launcher.py`, `.vscode/launch.json` | Targeted-test derivation fallback (`/verify-suite`); no reviewer row | none added |
| `e2e/run_puppeteer_summary_regression.ps1` | E2E spec | none |
| `CLAUDE.md`, `*/CLAUDE.md`, `.claude/**`, `docs/ai_workflow/**` | AI workflow / agent config | `code-reviewer` or careful self-review (here `code-reviewer`, already in the union) |
| `docs/product/README.md`, `docs/DUPLICATION_REGISTRY.md`, `docs/E2E_TESTING.md`, `docs/test_inventory/*` | Product docs only | none |
| DB-row files | DB / schema | **Not tripped**: no DB-row file is in the manifest. The manual backup/restore smoke is still run because AGREED §4 WS3 *Acceptance* requires it (§P12 item 9). |

**Union of the change-type rows (`QUALITY_GATE.md:46-57` at `f3adacf1`): `code-reviewer`.**

Three additions, each with its own source:
- **`unslop-reviewer`**: the S8 gate is `/verify-and-polish`, which `f3adacf1` defines as `/verify-suite` + `code-reviewer` + `unslop-reviewer` (*Two gates, two purposes*, `:156`). It runs as part of that gate. *(The draft omitted this. It had followed an uncommitted shared-checkout edit that makes `unslop-reviewer` opt-in.)*
- **`architecture-reviewer`**: required by `AGREED_PLAN.md` §4 WS3 *Gates* ("Route/API + DB rows → `code-reviewer` + `architecture-reviewer`"), which the owner adopted as WS3's governing direction (F10 refined).
- **`product-risk-reviewer`**: offered as an optional diff-time addition for Gate 1 (§P17). The table requires it only if a response shape changes, and production shapes do not. At `f3adacf1`, a reviewer the active plan calls for counts as a reviewer pass (*Owner approvals and reviewer passes*, `:31-34`), so the owner decides at Gate 1 whether Plan v2 calls for it. *(The draft cited a `CLAUDE.md` section that does not exist at `f3adacf1`.)*

`test-strategist` runs at plan stage only (`:59`). Diff-time reviewers are independent of the implementing `senior-developer` and `automation-qa`. A reviewer that does not run is incomplete, never "no findings", and does not satisfy a Required-reviewers cell (`:38-40`).

### P14. Design decisions resolved in Plan v1

| ID | Decision | Rationale |
|---|---|---|
| D-1 | Filter, hook, context-processor and view functions are module-level in `app.py` and registered by `create_app()` through `add_template_filter`, `after_request`, `context_processor` and `add_url_rule(endpoint='erase_data')`. `apply_static_cache_policy` reads `current_app.config`. | One function object per hook across instances, like blueprints. Tests can assert identity in `after_request_funcs` (AC4). Endpoint and filter names are unchanged. `current_app` is the active instance, so `frozen_cache_client`'s mutation of the module-level `app` still applies. |
| D-2 | The `__main__` body moves verbatim into `main()`. | AC7 becomes testable with mocks and no server. `python app.py` and payload `app.pyc` still run as `__main__`. |
| D-3 | The reloader rule is `utils.runtime_init.should_initialize_runtime(use_reloader)`, using Werkzeug's `is_running_from_reloader()`. | One tested predicate (AC7) and no ad-hoc environment parsing in `app.py`. |
| D-4 | The seeded carry-over (4c) is keyed by the resolved database path, not the guard key. | Seeding is a property of the file. A failed migration returns the legacy path and a retry may resolve another, so carrying "seeded" across different files would skip a needed upgrade or backup. |
| D-5 | Guard key = (resolved requested path or `None`, `str(runtime_root())`). `init_runtime(db_file=X)` and `init_runtime()` with env `DB_FILE=X` share a key. | Matches recommendation (i). Equivalent requests stay no-ops, not `RuntimeError`. |
| D-6 | `init_runtime(db_file="")` raises `ValueError`. | `prepare_runtime_database()` treats `""` as "no override" (`runtime_migration.py:241`), which would silently fall back to the resolver. |
| D-7 | A `threading.Lock` makes the check-run-set sequence atomic. | Cheap. Prevents a double run if two threads ever initialize; the steps never re-enter `init_runtime()`. |
| D-8 | `RuntimeInitOutcome` is a frozen dataclass with exactly AC2's five fields. A no-op returns the cached outcome via `dataclasses.replace(…, already_initialized=True)`, keeping the first run's `snapshot_path`. | Minimal surface. The migration failure reason is already logged by `runtime_migration.py:259-262`. |
| D-9 | One INFO line per real initialization and one DEBUG line per no-op. | Gives an observable oracle for "exactly once per serving process" in the launch-path and reloader checks (§P12 items 5, 10) without editing the smoke. |
| D-10 | `create_initialized_app()` takes no arguments and always initializes. | The Flask CLI calls it with no arguments. It cannot tell a reloader parent from a plain process, because `is_running_from_reloader()` is false in both. Both supported callers pass `--no-reload`; A8b measures the `--reload` case. |
| D-11 | The launcher imports `init_runtime` lazily inside `main()`, after `from app import app`. | Keeps `require_supported_python()` ahead of every heavy import (`app_launcher.py:12,53`). Lets tests patch `utils.runtime_init.init_runtime`. |
| D-12 | The conftest `app` fixture imports `create_app` lazily inside the fixture. The 13 route imports are deleted. | Collection-time imports stay as today, with no `app` import at collection. Nothing in conftest needs the blueprints any more. |
| D-13 | `real_app_client` keeps setting env `DB_FILE` and `HT_RUNTIME_DIR` alongside the explicit argument. It calls `_reset_for_tests()` before init **and in teardown**. It drops the `app_context()` wrapper, which is not needed by `DatabaseHandler`. | Belt-and-braces isolation for any code that reloads `utils.config`. The teardown reset stops a stale key from leaking into later modules or unit tests. 4d's "called only by `real_app_client`" is read as "the only fixture or production caller". The `test_runtime_init.py` unit tests also call it, because AC3(f) requires a test to. |
| D-14 | AC2's "single assignment" is checked by observation. `prepare` sees the old value; every later step sees the migration path; the final value equals it. | A Python module attribute cannot count its own assignments without a production test seam. A repeated identical assignment is unobservable and harmless. |
| D-15 | The `requestId` tests assert equality with the response's `X-Request-ID` header and the `req_[0-9a-f]{16}` shape. | Strictly tighter than `None`, so nothing is weakened (AC6). It pins the middleware wiring end to end. |
| D-16 | "Same URL rule set as today" is proven once, by diffing the S1 base capture against the post-C3 capture. Permanently, tests assert only structural invariants: 13 named blueprints, `/erase-data` POST, all rules non-strict, and equality between instances. | A committed URL-map fixture would recreate the "register in two places" burden that WS3 removes. |
| D-17 | `init_runtime()` does not reset or read `utils.db_initializer._INITIALIZATION_COMPLETE`. | Under `TESTING=1` that guard is bypassed. In production there is one key per process. Touching it would trip the DB row for no benefit. |
| D-18 | In `main()`, `init_runtime()` runs before the atexit and signal cleanup is registered. | Preserves today's order, where startup ran at import before `__main__`. A failed initialization still exits before any cleanup is registered. |
| D-19 | The `flask run` repairs are in the same commit as the factory (C3). The whole change is one PR. | Between the two, `FLASK_APP=app.py` would serve an uninitialized runtime (C-3). |
| D-20 | `setup_logging()` loses its `app` parameter. `TestFlaskIntegration`'s single test becomes a signature test. | With the branch deleted, the parameter would be dead, and vulture or reviewers would flag it. A signature test stops the hooks coming back unnoticed. |
| D-21 | AC1 probes run with `TESTING` removed. | It is a stronger proof: production mode is the case where import-time startup would write. The busy-sidecar skip keeps a regression from reaching the clone's own database. |
| D-22 | Test-first commits: `automation-qa` writes the S2 tests from Plan v2 before any production code. The harness migration (S5) follows the factory. | Repository workflow (`AUTONOMY.md` *Workflow roles*). Placing the conftest switch after C3 keeps every commit from C4 on green, and keeps the suite runnable at C3. |

### P15. Assumption verification (A1–A13; A8 split into six)

| ID | Verification: what is run, where, when | Pass condition | If refuted |
|---|---|---|---|
| A1 | AC1 subprocess probes (S2 tests, green from C3) and §P12 item 4, in the clone | One Flask instance; only `logs/` created; no data or DB file | Find the import-time side effect, from a route module or a new import, and remove it. If it cannot be removed, stop and return to the owner (Q-WS3-3 "remove" alternative). |
| A2 | `test_module_imports_no_routes_or_app` (AST); packaged smoke both modes (A12); `QUALITY_GATE.md` routing review at S8 | No `routes`/`app` import; smoke green | Stop; the owner chooses between keeping the logic in `app.py` and another boundary. |
| A3 | S5: before adding the token, `automation-qa` reads each of the five tests and their docstrings. After adding it, the tests' following assertions pass **unchanged**. | No test's intent is "an empty body is accepted"; all pass unmodified apart from the token | If any intends empty-body acceptance, it conflicts with AC8. Stop and raise it for owner decision; never weaken the guard. |
| A4 | AC1 patched-attribute case, AC5c and AC3e green. Mutation check in a scratch copy, never committed: make `init_runtime()` read `utils.config.DB_FILE` as input, and AC5c must fail; remove the `TESTING` refusal, and AC3e must fail. | Both mutations go red; both revert green | Strengthen the replacement tests until both mutations are caught, then re-review with `test-strategist`. |
| A5 | AC1's `test_constant_import_creates_no_data` (fresh process, same import as `smoke_packaged_app.py:247`); packaged smoke green | No `data/` or database created by the constant import | A remaining write path in import is a WS3 defect; fix before merge. |
| A6 | S1 grep (read-only): `rg -n "log_request_info|log_response_info|start_time|Slow request detected" --glob "!docs/archive/**"` | Hits only in the code being deleted, `.claude/rules/debugging.md:29-31` (being corrected) and this plan | A consumer exists. Stop; the owner revisits Q-WS3-2H (enable / leave dead). |
| A7 | Packaged smoke bootloader (CI, RP-3/RP-6) and payload (local). `deep-gate.yml`'s three jobs and `release.yml`'s two: either an owner-authorized `workflow_dispatch` of `deep-gate.yml` on the branch (proposed RP-7), or local equivalents: first install (§P12 item 6), empty schema (`run_all_initializers` alone, unchanged code), old DB (item 7) | All green | A job that fails on the WS3 branch but passes on base is a WS3 defect. If a CI-only gap shows up, it goes to the owner; WS3 adds no CI job. |
| A8a | CLI app discovery. In the clone, scratch runtime: `python -m flask --app app:create_initialized_app routes` | Exit 0; routes include `/erase-data`; scratch DB created; exactly one "Runtime initialized" line | Flask does not call a factory named this way. Switch both callers to the explicit call syntax `app:create_initialized_app()` and retest. If that also fails, return to the owner (alternative: `flask init-runtime` CLI). |
| A8b | Reloader parent. In the clone, scratch runtime: `python -m flask --app app:create_initialized_app run --reload --port <free>` for about 10 s, then count "Runtime initialized" lines in `<scratch>/logs/app.log` | Recorded as measured: 1 means the parent does not load the app; 2 means it does | No plan change either way, because no supported caller uses `--reload`. If 2, the `CLAUDE.md` and launch.json text say `--no-reload` is required with `flask run` (as §P4 already does), and the PR records it. |
| A8c | `Rule.strict_slashes` bound when a rule is added: `test_every_rule_is_non_strict`, plus `tests/test_trailing_slash_routing.py` | Every rule has `strict_slashes is False`; trailing-slash tests green | Keep `strict_slashes` set before registration (already planned) and set it per rule if needed; record the measured binding time. |
| A8d | Exception propagation under `TESTING` with an `Exception` handler: `test_handler_layering_behaves_as_documented` (raising route under `TESTING=True`) | 500 `INTERNAL_ERROR` response, no exception raised in the test | If the exception propagates, C-11's "uncaught exceptions → 500" is wrong. Correct C-11 and re-triage A11 for tests that expect a response. |
| A8e | `app.logger`'s default handler: `test_app_factory.py::test_app_logger_keeps_flask_default_handler` (`flask.logging.default_handler in app.logger.handlers`; no `hypertrophy_toolbox` handler aliased) | Default handler present, no aliasing; matches today's never-attached state | No behavior change from WS3, because handlers were never aliased in production (F5). Record the measured state; no plan change. |
| A8f | `app.debug` at construction: subprocess runs `python -c "import app; print(app.app.debug)"` with `FLASK_DEBUG` unset and with `=1` | Recorded as measured | Informational only. No WS3 decision depends on it, because 3a deleted the debug listing that it would have gated. |
| A9 | AC3e test plus the A4 mutation check. `real_app_client` always passes an explicit path (AC6 review). | Refusal enforced; mutation caught | A9 is mitigated by design and does not need proving true. If AC3e cannot be made to fail under mutation, strengthen it before merge. |
| A10 | Run `e2e/run_puppeteer_summary_regression.ps1` in the clone (needs network for `npx`) | Exit 0 | If `npx`/MCP is unavailable for external reasons, run steps 1–2 by hand: seed, then `flask run` with the new `FLASK_APP` and `GET /weekly_summary` 200. Record that step 3 could not run and why. Retirement stays a separate proposal (5a). |
| A11 | Before S5, `automation-qa` greps tests that use `client`/`app` for `pytest.raises` around requests, `requestId`, 404/405 body assertions, `caplog` absence-of-warning checks and `app.name`. After S5, full pytest serial and `-n 8 --dist loadfile`. | Only the AC6-listed outcomes change | Classify each new failure. If the test relied on twin-only behavior, update it with the reason listed in the PR (never weakened). If it is a production defect, stop and fix. If the classification is unclear, stop and escalate. |
| A12 | Packaged smoke bootloader (CI) and payload (local) | Green; `utils.runtime_init` importable in the frozen build | Adding `hiddenimports` changes `Hypertrophy-Toolbox.spec`, which is out of WS3 scope. Stop and return to the owner. |
| A13 | None needed: Q-WS3-2(a) was accepted, so the DEBUG level `setup_logging` sets is unchanged. Full pytest covers `test_fatigue.py`. | `test_fatigue.py` green | Moot unless the owner later selects (b). |

### P16. Implementation-readiness preconditions carried to Gate 1

- **IC-1 … IC-8** (Section 0, ED-1 isolation conditions): unchanged, all unchecked. They are verified and recorded at S0 by the implementation manager.
- **RP-1 … RP-5** (Section 0): unchanged. RP-4 (Gate 1 names the move of all 13 `register_blueprint` calls into `create_app()`) remains a required part of the Gate 1 wording.
- **Proposed RP-6:** Gate 1 explicitly authorizes pushing the implementation branch and opening a PR, without merging, so that the non-required packaged bootloader smoke can be observed (RP-3). Merge needs a separate confirmation naming the PR.
- **Proposed RP-7:** Gate 1 chooses between an owner-authorized `workflow_dispatch` of `deep-gate.yml` on the branch and the local equivalents in A7.

### P17. Items the product-manager did not resolve (owner decisions for Gate 1)

1. RP-4: the explicit blueprint-registration approval (AUTONOMY).
2. RP-6: push and PR authority for CI observation.
3. RP-7: `deep-gate.yml` dispatch versus local equivalents.
4. Whether to add `product-risk-reviewer` as an optional diff-time reviewer. The table does not require it; the owner may authorize it given the startup and erase risk class.

Measurement-only items (A8a, A8b, A8f, A10, and D-16's URL-map diff) are not owner decisions. The A-items have a criterion and fallback in §P15. D-16 is §P12 item 17: a non-empty diff is a WS3 defect, fixed before merge.

---

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Section 0 (rev 2; context, not a council row) | `af7285ca1164caf98` | In-process subagent of session `12105a05` (now `hypertrophy-toolbox-v3-main-81`); that session confirmed the ID on 2026-10-20. Could not be resumed from this session. |
| `product-manager` — Plan v1 | `a9259355287e3c511` | Fresh `product-manager` in manager session `hypertrophy-toolbox-v3-main-c3`. Wrote the rev 3 Gate 0 record and Plan v1, including the same-day citation correction. ID supplied by the manager. |
| `product-manager` — response matrix + Plan v2 | `a9259355287e3c511` | The same agent as Plan v1, resumed by the manager via `SendMessage` after the council. Wrote the Reviewer findings record, the response matrix and Plan v2 (rev 4). |
| `architecture-reviewer` | `a484bd1ac77e7e978` | Step 2 reviewer; verdict sound-with-changes (AR-1…AR-4). Report: `artifacts/ws3-app-factory-20261020/council-architecture-a484bd1ac77e7e978.md`. |
| `test-strategist` | `af3d581707e375d82` | Step 2 reviewer; verdict sound-with-changes (TS-1…TS-13). Report: `artifacts/ws3-app-factory-20261020/council-test-strategist-af3d581707e375d82.md`. |
| `product-risk-reviewer` | `a12256eb7f65a549a` | Step 2 reviewer; verdict sound-with-changes (PR-1…PR-5). Report: `artifacts/ws3-app-factory-20261020/council-product-risk-a12256eb7f65a549a.md`. |

All three reviewers read the frozen copy `artifacts/ws3-app-factory-20261020/PLANNING.plan-v1-as-reviewed.md` (SHA-256 `950e64f56410d798fe17e063f367974245c3585048246693ab2f6d6c6dc4696c`). The reviewers could not hash it themselves; the manager hashed it before dispatch.

**Same product-manager resumed?**
- **Section 0 → Plan v1:** `no`. Both IDs are recorded: `af7285ca1164caf98` wrote Section 0 and `a9259355287e3c511` wrote Plan v1. The gap is continuity only (below).
- **Plan v1 → matrix + Plan v2:** **`yes`**. `a9259355287e3c511` was resumed via `SendMessage`.

**Evidence gap (continuity only; both IDs recorded)**
> The Section 0 author, `product-manager` `af7285ca1164caf98` (an in-process subagent of session `12105a05`, now named `hypertrophy-toolbox-v3-main-81`, which confirmed the ID on 2026-10-20), could not be resumed: `SendMessage` returned "No transcript found for agent ID: af7285ca1164caf98" (cross-session). Plan v1 was therefore written by a fresh `product-manager` `a9259355287e3c511` in session `hypertrophy-toolbox-v3-main-c3`. It read this artifact directly, with no relay, and preserved Section 0's audit trail verbatim apart from the Gate 0 record.
>
> The previous owning session formally released the file on 2026-10-20. It reported no pending edits, gave its last known write as SHA-256 `0a54ec8d…bfec6` (the rev 3 preimage), and said it would make no further edits.
>
> Council-internal continuity (Plan v1 → response matrix and Plan v2) was preserved: `a9259355287e3c511` was resumed via `SendMessage`. No ID was invented and no completed work was rerun.

### Delegated Gate 1 — added 2026-10-20 (rev 5)

*Appended; the rows above are unchanged. The advisers below are a separate delegated Gate 1 team (§V19), not a re-run of council step 2.*

| Role | Agent ID | Notes |
|---|---|---|
| Manager (adopting session) | Session `hypertrophy-toolbox-v3-main-53`, session id `8baa0d6f-a419-4e4e-b812-5a1e73da9a8b` | Read-only manager. Spawned the three advisers and wrote the synthesis `artifacts/ws3-impl-20261020/gate1-team/DELEGATED_GATE1_DISPOSITION.md`. |
| `architecture-reviewer` (Gate 1 adviser) | `a1eeea22faba20495` | FAVORABLE WITH CONDITIONS. Report `artifacts/ws3-impl-20261020/gate1-team/architecture-a1eeea22faba20495.md`, saved by the manager with "prose lightly condensed". |
| `test-strategist` (Gate 1 adviser) | `a582e93753711c30d` | FAVORABLE WITH CONDITIONS. Report `artifacts/ws3-impl-20261020/gate1-team/test-strategist-a582e93753711c30d.md`, saved by the manager, "condensed only where the return repeated plan text". |
| `product-risk-reviewer` (Gate 1 adviser) | `a7be2f933a6121799` | FAVORABLE WITH CONDITIONS. Report `artifacts/ws3-impl-20261020/gate1-team/product-risk-a7be2f933a6121799.md`, saved by the manager verbatim. |
| `product-manager` — §V19 record (rev 5) | product-manager (Gate 1 record) — ID recorded by the manager in artifacts/ws3-impl-20261020/gate1-team/ after return | Fresh `product-manager` in session `hypertrophy-toolbox-v3-main-53`. Wrote §V19, this sub-block, the Sign-off update and the rev 5 header rows. |

**Same product-manager resumed (Plan v2 → §V19)?** **`no`**. The Plan v1/v2 `product-manager` `a9259355287e3c511` belongs to another session (`hypertrophy-toolbox-v3-main-c3`) and cannot be resumed from this one.

**Evidence gap (continuity only; every ID is recorded or will be recorded by the manager)**
> §V19 was written by a fresh `product-manager`, not by `a9259355287e3c511`. It read this artifact, the manager's synthesis, the three adviser reports and the owner request directly, and preserved the audit trail above verbatim. It cannot know its own agent ID; the manager records that ID under `artifacts/ws3-impl-20261020/gate1-team/` after the call returns. Two of the three adviser reports are condensed copies saved by the manager, not the raw returns (noted in the table). The prior council was reused, not re-run. No ID was invented.

---

## Reviewer findings

*`/council-plan` step 2, run 2026-10-20. The three reviewers ran in parallel and independently. Each read the frozen copy `artifacts/ws3-app-factory-20261020/PLANNING.plan-v1-as-reviewed.md` (SHA-256 `950e64f56410d798fe17e063f367974245c3585048246693ab2f6d6c6dc4696c`). The reviewers could not hash the file themselves; the manager hashed it before dispatch. Each report is reproduced below verbatim from its file under `artifacts/ws3-app-factory-20261020/`, in a quote block so its own headings do not join this document's outline. Finding IDs: report item *n* is AR-*n*, TS-*n* or PR-*n*, in the order the items appear. Every verdict is "sound-with-changes"; no finding was marked blocking.*

### architecture-reviewer (agent `a484bd1ac77e7e978`) — AR-1…AR-4

Source: `artifacts/ws3-app-factory-20261020/council-architecture-a484bd1ac77e7e978.md`. Item 1 = AR-1, 2 = AR-2, 3 = AR-3, 4 = AR-4.

> # architecture-reviewer a484bd1ac77e7e978 — WS3 Plan v1 (PLANNING.md sha256 950e64f5…696c), verbatim final report
>
> **WS3 Plan v1 architecture review.** I read the frozen `PLANNING.plan-v1-as-reviewed.md` (lines 514–953) cold and checked its claims against `src-f3adacf1`. Nothing was run.
>
> The module boundaries, the DB-access pattern, logger use and the response contracts hold up. Two findings should be fixed before Gate 1, plus two nits.
>
> 1. **Should-fix. §P4 `main()` and D-18: the reloader parent still registers DB cleanup on a database nobody initialized.**
>    - **Defect.** `main()` calls `init_runtime()` only when `should_initialize_runtime(use_reloader)` is true. The `cleanup_on_exit` and signal registration is unconditional ("verbatim"). With `FLASK_USE_RELOADER=1` the monitoring parent therefore registers an atexit hook that opens `DatabaseHandler()` without ever having initialized the runtime.
>    - **Evidence.**
>      - `app.py:280-301` is the cleanup that the plan keeps verbatim.
>      - `utils/database.py:247-254` shows `get_db_connection` calls `ensure_directory` and `sqlite3.connect` when the file is missing.
>      - `utils/database.py:288` reads `utils.config.DB_FILE`.
>      - The plan's own C-2 says that value is no longer reassigned at import.
>    - **Risk.** On a first install, a parent exit (for example Ctrl+C before the child has seeded) creates an empty `database.db` at the resolved path. The seed bootstrap only copies when the file is missing (CLAUDE.md startup notes), so the next start would run with an empty catalog. The plan's C-4 says the parent "no longer migrates, seeds or snapshots" and does not mention this write.
>    - **Change.** Gate the cleanup and signal registration behind the same `should_initialize_runtime(...)` condition as the init call. Alternatively, make the cleanup skip when `init_runtime` has not completed in this process. Add a test beside `test_main_reloader_parent_does_not_initialize` that asserts the parent registers no DB cleanup. Reword C-4 and D-18 accordingly.
>
> 2. **Should-fix. §P5 and §P3 rows 3/5: `init_runtime()` has no declared fate for the module-level `app` it is separated from.**
>    - **Defect.** `app = create_app()` runs at import (§P4). The plan's invariant is that "no production path reads `utils.config.DB_FILE` in between" (C-2). That is asserted, not verified. Nothing in the plan enumerates or tests which code paths run between import and init. The paths that exist are:
>      - the launcher's `from app import app` at `app_launcher.py:69`;
>      - the Flask CLI's first import of module `app`;
>      - the smoke's own-process import.
>    - **Evidence.** The only readers of `DB_FILE` are `utils/database.py:247,288`, `utils/catalog_seed.py:44` and `utils/auto_backup.py:48`. All of them are call-time reads, so import is safe today. A future `@app.before_first_request`-style addition would not be caught.
>    - **Change.** Add one cheap permanent guard in AC1 or AC4. After `import app`, assert `utils.config.DB_FILE` is unchanged and no `DatabaseHandler` was constructed. AC1 already asserts the `DB_FILE` part, so adding the `DatabaseHandler` check is enough. Keep the C-2 wording as a tested invariant rather than prose.
>
> 3. **Nit. §P15 A8a: `flask routes` and `flask shell` initialize the runtime.**
>    - **Defect.** A8a uses `flask --app app:create_initialized_app routes` as the pass test. That command now runs migration, seed and backup. The plan notes "scratch DB created", so it knows, but the §P9 compat notes (C-3) do not warn that every Flask CLI subcommand against `create_initialized_app` mutates the DB.
>    - **Change.** State this in C-3 and in the launch.json comment. No design change is needed.
>
> 4. **Nit. §P5 comment "step 1 (never raises)".**
>    - **Defect.** `prepare_runtime_database` is documented as never raising (`runtime_migration.py:233`). `copy_legacy_backups()` at `:267` sits outside the `try` that catches `MigrationError`, `sqlite3.Error` and `OSError`, so an exception there would propagate. Rule (iv) already handles propagation, so this is only a comment/test accuracy issue.
>    - **Change.** Drop "never raises" from the `init_runtime` inline comment, or cover the case with a test.
>
> **Checked and sound**
> - **Module boundaries.** `utils/runtime_init.py` imports no `routes`, `app` or `flask`, and an AST test enforces this. The `routes` → `utils` direction is kept.
> - **Registration triple.** The plan collapses it to a single location (`create_app()`) and deletes the conftest twin. It also rewrites the stale "register in both" prose and greps for it (§P12 item 16). This is a deliberate, owner-gated change (RP-4).
> - **Schema registration.** No new tables.
> - **DB access.** All access stays through `DatabaseHandler` and `run_all_initializers`, and no DB-row file is edited.
> - **Logger and response contract.** There is no `print`. `get_logger()` is cached, and the `setup_logging(app)` branch removed in §P1 is dead because `get_logger()` runs first and takes the early return (`utils/logger.py:43-44`). The only `app=` caller is `tests/test_logger.py:236`, which the plan replaces. `/erase-data` keeps its `error_response` and `success_response` shapes.
> - **Normalization.** Not applicable.
> - **Shared-state edits.** `app.py`, CLAUDE.md, `.claude/**` and the `AUTONOMY.md` wording are declared under IC-4/RP-2, and the explicit-confirmation rule is left to WS2.
> - **`utils/__init__.py`.** It is untouched.
> - **Hook ordering.** `request-id` precedes `apply_static_cache_policy`, so `after_request` ordering is preserved.
> - **`from app import …` outside tests.** No hits in `routes/`, `utils/`, `scripts/` or `e2e/`, so no importer breaks on the removed names.
>
> **Verdict: sound-with-changes.** Finding 1 should be fixed in Plan v2. Finding 2 is a tested-invariant addition. Findings 3 and 4 are wording.

### test-strategist (agent `af3d581707e375d82`) — TS-1…TS-13

Source: `artifacts/ws3-app-factory-20261020/council-test-strategist-af3d581707e375d82.md`. Under *Findings*, item *n* = TS-*n*. The remaining sections are reproduced verbatim as context.

> # test-strategist af3d581707e375d82 — WS3 Plan v1 (PLANNING.md sha256 950e64f5…696c), verbatim final report
>
> # Test-strategy review of WS3 Plan v1 (`test-strategist`)
>
> I read the frozen copy `PLANNING.plan-v1-as-reviewed.md`, not the live file. I could not recompute the SHA-256, because I had no hashing tool. Source citations are against the snapshot, `artifacts/ws3-app-factory-20261020/src-f3adacf1/`, and I abbreviate that prefix below. Nothing was run, imported or collected. Two findings (2 and 7) are predictions from the repo's own `.venv` copies of Flask 3.1.3 and Werkzeug 3.1.8. The pin is 3.1.9 (`requirements.txt:4`), so measure them at A8c and A8e before relying on them.
>
> ## Required gates (derived from `QUALITY_GATE.md` at `f3adacf1`)
>
> - **Full `/verify-suite`.**
>   - `app.py` and `tests/conftest.py` fall back to it (`QUALITY_GATE.md:132`).
>   - `app_launcher.py` has no path row, so it also falls back.
>   - Unit-style test gating cannot be targeted, because the conftest `app` fixture serves nearly every test file.
> - **Targeted pytest (inside the full run).**
>   - New: `tests/test_runtime_init.py`, `tests/test_app_factory.py`.
>   - Edited: `test_real_app_db_isolation.py`, `test_runtime_paths.py`, `test_catalog_seed_bootstrap.py`, `test_logger.py`, `test_pattern_coverage.py`, `test_erase_data_guard.py`.
>   - Consumers of the changed fixtures: `test_static_cache_policy.py`, `test_trailing_slash_routing.py`, `test_local_first_assets.py`, `test_program_backup.py`, `test_database_user_profile.py`, `test_db_migration.py`, `test_volume_progress.py`, `test_export_blank_rep_bounds_contract.py`, `test_export_blank_rep_bounds_gate0.py`, `test_free_exercise_db_mapping.py`.
>   - Contract tests that pin the edited docs: `test_agent_workflow_contracts.py`. It checks root `CLAUDE.md` is under 200 lines and that `CLAUDE.md` and `.claude/rules/database.md` both mention `seed_worktree_snapshot.py` and `DatabaseHandler` (`:673-680`).
> - **E2E.**
>   - Full Chromium via `/verify-suite`.
>   - Specs to watch: `erase-flow`, `program-backup`, `fatigue`, `smoke-navigation`, `summary-pages`.
>   - `e2e/run_puppeteer_summary_regression.ps1` falls under the `e2e/**` row.
> - **Other required gates.**
>   - `Test Inventory Drift`: regenerate `docs/test_inventory/` in the standalone clone (RP-5).
>   - pyright baseline diff, which covers `tests/` too (`pyrightconfig.json` excludes only `docs/archive`).
>   - flake8, plus vulture (`pyproject.toml`).
>   - Packaged Smoke (Windows bootloader, non-required): the only automated check of `app_launcher.py` end to end. It runs on every PR (`ci.yml:1485`).
> - **Reviewers.**
>   - `code-reviewer` for the Route/API, Business-logic and AI-workflow rows.
>   - `unslop-reviewer` via `/verify-and-polish` (`QUALITY_GATE.md:156`).
>   - `architecture-reviewer`, because AGREED §4 adds it.
>   - `product-risk-reviewer` is optional (P17 item 4). The table does not require it, because production response shapes are unchanged.
> - **Not tripped.** The DB/schema row, since no DB-row file is in the manifest.
> - **Known red.** `e2e/program-backup.spec.ts:79` (`QUALITY_GATE.md:244`). The plan watches that spec but never names the flake (finding 4).
>
> ## Existing coverage
>
> - `app.py`
>   - There is no direct import test today beyond `real_app_client`.
>   - `test_erase_data_guard.py` covers the real route's rejection paths and the fallback handlers.
>   - `test_trailing_slash_routing.py` and `test_static_cache_policy.py` cover the real object.
>   - `test_runtime_paths.py:200-222` is an AST line-order test.
> - `app_launcher.py`
>   - No pytest references it (grep of `tests/`).
>   - Everything the plan lists for the launcher is new (`test_launcher_*`), plus the CI bootloader smoke.
> - `utils/logger.py`: `tests/test_logger.py` only. Nothing asserts the dead hooks (`:227-239`).
> - `tests/conftest.py`: the whole suite.
> - `test_free_exercise_db_mapping.py:690-710` currently tests the twin's copy of `safe_media_path`. After WS3 it tests the production filter, which is a coverage gain.
>
> ## Findings
>
> 1. **Should-fix (high). P1 token-site row, A3, AC6, A11: a sixth test outcome change that the plan says does not exist.**
>    - `tests/test_program_backup.py:843` asserts `data.get('data') is None` after `POST /erase-data`.
>    - The twin returns `data=None`. The real route returns `success_response(data={"auto_backup": ...})` (`app.py:265-268`).
>    - `success_response` omits `data` only when it is `None` (`utils/errors.py:34-35`), so the real body has `"data": {"auto_backup": null}` and the assertion fails.
>    - The plan says "All following assertions are unchanged (A3)" and that only the `requestId` tests and token sites change.
>    - Change for Plan v2: add `test_program_backup.py:843` to AC6 and the P1 row, changing it to `data['data'] == {"auto_backup": None}`. That tightens the assertion and fits the "listed, not weakened" rule. Reword A3 and A11 so a literal token-only edit is not prescribed.
>
> 2. **Should-fix (high). AC4, A8c, P4 comment: `test_every_rule_is_non_strict` will fail on the `static` rule.**
>    - Flask registers the `static` rule inside `Flask.__init__` (`.venv/.../flask/app.py:267-275`).
>    - `Rule.bind` copies the map's `strict_slashes` at add time (`.venv/.../werkzeug/routing/rules.py:574-575`).
>    - So that rule keeps `strict_slashes=True` before `url_map.strict_slashes = False` runs. This is already true at `app.py:52-53`.
>    - The P4 comment "before any rule exists" is wrong. A8c's fallback of setting it per rule would be a production edit with no behavioral gain.
>    - Change: assert behavior (trailing-slash GET returns 200 with no redirect for blueprint rules), or exempt endpoint `static` with the reason recorded. Fix the comment and the AC4 wording.
>
> 3. **Should-fix (high). D-2, D-18, AC7 `test_main_*`: in-process `main()` tests install process-global shutdown hooks.**
>    - The `__main__` body moves verbatim into `main()`. It registers `atexit` cleanup and SIGINT/SIGTERM handlers (`app.py:280-301`).
>    - `cleanup_on_exit` opens `DatabaseHandler()` on whatever `utils.config.DB_FILE` is at interpreter exit (`:284`).
>    - After the fixtures restore it, that is the ambient default. The hook then touches, and via sqlite connect can create, the clone's `data/database.db`. That is the "test hits live DB" pitfall in `.claude/rules/testing.md`, and it can contaminate the AC1 `data/` listings.
>    - The SIGINT handler also ends `sys.exit(0)` and swallows Ctrl+C.
>    - Change: factor the registration into a small patchable function. Require the tests to patch `atexit.register` and `signal.signal`, and assert D-18 ordering through that seam.
>
> 4. **Should-fix. S1(c), P12 item 2, AC12: there is no Chromium baseline, and the known red is not named.**
>    - S1(c) records a pytest baseline only (`CLAUDE.md:144-148`).
>    - `/verify-suite` says "declare success only if both green" (`.claude/skills/verify-suite/SKILL.md:13`). But visual state is platform-specific and "do not read a red count out of this file" (`QUALITY_GATE.md:61`). The Known exceptions list is dated 2026-05-10 and names one flake (`:243-246`).
>    - Without a recorded base-revision E2E run, "Chromium green" is undefined or unmeetable.
>    - Change: S1 also records a Chromium baseline in the clone, using the same seed settings as the later run. Pass means no new red against it. Name `program-backup.spec.ts:79` and require an isolated rerun before calling it known. Never update snapshots.
>
> 5. **Should-fix. P11 AC3, AC2: the `test_runtime_init.py` fixture leaks global state.**
>    - The autouse fixture only calls `_reset_for_tests()`.
>    - But `init_runtime()` assigns `utils.config.DB_FILE` at step 2, even with every step mocked, and the AC2 test deliberately observes that assignment.
>    - Nothing restores the attribute or the env (`DB_FILE`, `HT_RUNTIME_DIR`, `TESTING`). Later tests and `real_app_client`'s captured `original_config_db` inherit the leak.
>    - Change: have the autouse fixture `monkeypatch` the attribute and env, and assert they are restored.
>
> 6. **Should-fix. P11 AC4, D-16: two logging tests are order-dependent.**
>    - `test_factory_does_no_logging_setup_or_database_work` patches `setup_logging` to raise.
>    - But `create_app()` reaches `register_fallback_handlers`, which calls `get_logger()` (`utils/errors.py:237-238`). That calls `setup_logging()` whenever `utils.logger._logger is None`.
>    - `tests/test_logger.py` leaves it `None` (`:83-90`, `:208-219`, `:230`). Under `-n 8 --dist loadfile`, file order differs, so the test can go red.
>    - Fix: call `get_logger()` before patching, or assert that no handler is constructed or added.
>    - `test_logger_keeps_one_file_and_one_console_handler` should compare before and after rather than assert an absolute count. It should use exact types, because `RotatingFileHandler` is a `StreamHandler` subclass.
>
> 7. **Should-fix. A8e, P6: the Flask default-handler check cannot run under pytest as written.**
>    - `create_logger` adds `default_handler` only if no handler in the logger chain covers the effective level (`.venv/.../flask/logging.py:31-47,76-77`).
>    - Pytest's capture handlers sit on the root logger, so `default_handler in app.logger.handlers` will likely be false in-process even though production has it.
>    - Run that measurement in a subprocess.
>    - Also record that `app.logger` is the process-global logger named `app.name`, which is `"app"` (`flask/logging.py:71`). Every `create_app()` instance shares it, which the P6 "repeated factory" prose does not say.
>
> 8. **Should-fix. A7, RP-7, P12 item 7: the real-step, existing-database upgrade path has no PR-time automated test.**
>    - No test references `make_old_schema_db`. It is exercised only by `deep-gate.yml` (schedule or manual dispatch only) and a manual step.
>    - The plan lets Gate 1 choose "local equivalents".
>    - Either make RP-7 dispatch mandatory evidence, or add a subprocess pytest. It would run `init_runtime(db_file=&lt;old-schema DB&gt;)`, check `catalog_version` is populated, and check there is exactly one snapshot.
>    - Also parametrize `test_outcome_fields` over all six `migration_action` values. `failed` should assert the legacy path is assigned to `DB_FILE` and the seed is skipped (`runtime_migration.py:255-265`).
>
> 9. **Should-fix (low). AC2, Q-WS3-6: the boundary proof is only direct-import.**
>    - The claim "initializer callers no longer import all 13 route modules" is stated but unproven.
>    - No global utils→routes test exists (grep).
>    - Add a fresh-interpreter test that imports `utils.runtime_init` and asserts that neither `app` nor any `routes*` module appears in `sys.modules`.
>
> 10. **Nit. D-16 against AC4/AC13.** The hard-coded 13-name list in `test_app_factory.py` is itself a second registration site, so the "register in both" burden returns in a milder form. Say so in the AC13 wording ("update the blueprint list in `test_app_factory.py`").
>
> 11. **Nit. Stale text the plan does not list.**
>     - `tests/test_trailing_slash_routing.py:20-22` is declared "needs no edit" but describes the conftest app lacking a hook.
>     - `tests/conftest.py:140-143` and `test_priority7_error_handling.py:21` have the same problem.
>     - `AUTONOMY.md:144` gives a rationale ("affects every test in conftest… 404s silently") that WS3 makes false, while the rule stays.
>
> 12. **Nit. Rule (v) evidence.** C-5 says no caller hits the raising branches. My grep confirms no launcher or config sets `TESTING` (`START.bat`, `playwright.config.ts`, `.vscode`, workflows). The seven `css_audit` spawners explicitly set `TESTING: '0'` (for example `scripts/css_audit/n4_regions_abc.mjs:590`). Cite that. Make the error text tell a developer to unset `TESTING`, since an exported `TESTING=1` now breaks `python app.py`.
>
> 13. **Nit. A8b and P6.**
>     - `flask run` loads the app unconditionally (`.venv/.../flask/cli.py:962-963`), so with `--reload` the parent also calls `create_initialized_app()`. A8b will probably measure 2, not "unmeasured".
>     - CI `pytest-core` is serial with `--cov` (`ci.yml:830-835`); `-n 8` is local-only evidence.
>
> ## Coverage gaps
>
> - **`app_launcher.py`:** needs the new `test_launcher_*` tests in `tests/test_app_factory.py`. The plan has them. They are the only unit-level coverage.
> - **Real `init_runtime()` on an old-schema database:** needs the subprocess test from finding 8, in `tests/test_runtime_init.py`.
> - **`utils.runtime_init` transitive imports:** needs the fresh-interpreter test from finding 9.
> - **`failed` and other migration actions through `init_runtime`:** need the parametrized case from finding 8.
>
> ## Conftest and fixture work
>
> - The conftest `app` fixture, `real_app_client` and `_initialize_test_database` are covered by the plan.
> - Add the `monkeypatch` isolation from finding 5 to the new test file's autouse fixture.
> - Add the `atexit`/`signal` patching seam from finding 3.
> - No other fixture or `erase_data()` change is needed. No new blueprint or table is added.
>
> ## Spot-checks that held (no finding)
>
> - **Citations and equivalence.** Spot-checked citations in the plan hold, including `conftest.py:204-206`, `db_initializer.py:569,575`, `auto_backup.py:45-46`, `logger.py:43-44,74-114`, `runtime_migration.py:236-242` and `test_runtime_paths.py:200-222`. The `real_app_client` equivalence argument (`force_base=False` is identical under `TESTING=1`) is correct.
> - **Order and equality tests.** The after-request order (cache policy, then request-id) is preserved in `create_app`. The only exact-dict equality tests that change are the two `requestId` ones, and no test wraps a client call in `pytest.raises`.
> - **Removed names.** No importer uses `app.migration`, `app.database_seeded` or `start_timer`.
>
> ## Verdict
>
> **Sound-with-changes.** The architecture, sequencing, rollback and gate selection are sound, and I found no blocking defect. Plan v2 must correct findings 1 to 3 (a wrong compatibility claim, a test that fails as specified, and a test-hygiene hazard that touches the live database) and define the E2E baseline (finding 4). Findings 5 to 9 are test-design fixes that belong in v2. Findings 10 to 13 can be dispositioned as nits.

### product-risk-reviewer (agent `a12256eb7f65a549a`) — PR-1…PR-5

Source: `artifacts/ws3-app-factory-20261020/council-product-risk-a12256eb7f65a549a.md`. Item 1 = PR-1 … item 5 = PR-5.

> # product-risk-reviewer a12256eb7f65a549a — WS3 Plan v1 (PLANNING.md sha256 950e64f5…696c), verbatim final report
>
> Findings from a cold read of Plan v1 (lines 514–953), checked against the `f3adacf1` snapshot where I could. I did not re-verify every cited `path:line`.
>
> 1. **Should-fix. §P9 C-3 and §P3 row 3: a stale `flask run` habit now silently serves an uninitialized runtime.**
>    - Defect: `flask run` with `FLASK_APP=app.py` or `app:app` imports a module-level `app` that has had no migration, seed or schema work. The plan relies on prose in `CLAUDE.md` and the routes rule, plus repairs to the two known callers (`.vscode/launch.json` and the Puppeteer `.ps1`).
>    - Risk: if no database exists at the resolved path, `DatabaseHandler` creates an empty file there. A user with a legacy database that was never migrated would see an empty app. That looks like data loss on the Plan, Log and Backup workflows, even though the old file is untouched. This is the only item in the plan that can affect user data.
>    - Evidence: the plan's own reasoning at P9 C-3 and D-19. The legacy migration lives only in `prepare_runtime_database()`.
>    - Recommendation:
>      - Add a fail-loud signal for the uninitialized case without breaking the "`create_app()` does no I/O" rule. One option is a `before_request` check on a module flag set by `init_runtime()`, which logs an ERROR or returns a clear envelope.
>      - Alternatively, record in the Gate 1 packet that the owner accepted documentation-only mitigation.
>      - Either way, state the empty-database symptom in the C-3 migration note.
>
> 2. **Should-fix. §P13 and §P17 item 4: `product-risk-reviewer` is left optional.**
>    - Defect: the plan reasons only about response shape. This change touches the startup sequence that `CLAUDE.md` §2 calls load-bearing, the `auto_backup` guarantee, and the `/erase-data` snapshot-then-drop path. Those are Backup and Refactor-invariant concerns.
>    - Evidence: `app.py:108` and `:256` (`create_startup_backup`), and the `:248` confirm guard. The plan itself notes "startup and erase risk class".
>    - Recommendation: make `product-risk-reviewer` a required diff-time reviewer at Gate 1, not an owner option.
>
> 3. **Should-fix. §P9 C-4 and §P12 item 10: the change to snapshot count in reloader mode should be a stated Backup-contract change.**
>    - Defect: today, with `FLASK_USE_RELOADER=1`, both the parent and the child run startup at import, so two snapshots are written. After WS3 there is one, and the plan treats that as needing no reversal.
>    - Risk: it is benign for the user, but it is a Backup-workflow behavior change. `create_startup_backup()` also rotates old snapshots, so the count affects how much history is kept (`utils/auto_backup.py:25-34,80`).
>    - Recommendation: write the PR migration note as "snapshots per start change from 2 to 1 under the reloader" and cite the rotation depth.
>
> 4. **Should-fix. §P5 rule (iii) and D-10: a `RuntimeError` guard is added to the production startup path.**
>    - Defect: `init_runtime()` now raises on a second call with a different database or runtime root. The plan says no caller hits this, but `create_initialized_app()` takes no arguments and `flask run --reload` is unmeasured (A8b).
>    - Risk: if the reloader parent also loads the factory, a user could see a hard startup error instead of a working app. The plan says no plan change either way, which understates this.
>    - Recommendation: make A8b a pre-Gate-2 measurement. If the result is 2 (parent also loads the app), confirm the second call is a same-key no-op and does not raise, and record that in the PR.
>
> 5. **Nit. §P9 and C-11: the test harness now logs WARNINGs to the run's `app.log`.**
>    - Defect: this is a test-side change only, so there is no invariant risk. The migration note should say it is test-only so a reader does not take it for a production logging change.
>    - Recommendation: add "test harness only" to the C-11 wording and to the PR note.
>
> Checks that came back clean:
> - **Calculation modules:** none are touched. No `effective_sets`, `weekly_summary`, `session_summary`, `progression_plan`, `volume_*` or `_fatigue` files appear in the manifest.
> - **Local-first:** no telemetry, remote data or auth is introduced.
> - **Production `/erase-data`:** the contract is unchanged. The five test calls that gain the token only align the harness with the existing production guard at `app.py:248`.
> - **Terminology:** no user-facing copy is changed.
> - **Parked workstreams:** the fatigue meter is not resumed. `test_fatigue.py` is run only as part of the full suite.
> - **Migration notes:** P9 carries migration notes and test coverage. P10 covers rollback, and the backup and restore smoke is in P12 item 9.
> - **Schema:** none changes, so existing backups stay restorable.
> - **Workflow ownership:** `AUTONOMY.md` is wording-only, and P17 item 1 sends the blueprint-registration move to Gate 1.
>
> **Verdict: sound-with-changes.** Findings 1 and 2 should be resolved at Gate 1. Findings 3 and 4 are PR-note and measurement changes. There is no calculation or non-goal violation.

---

## Response matrix

*`/council-plan` steps 3–4. The manager synthesized the proposed dispositions and checked the premises of TS-1, AR-1/TS-3 and TS-2 against `src-f3adacf1`. The `product-manager` re-checked TS-1 (`tests/test_program_backup.py:843`), TS-11 (`tests/test_trailing_slash_routing.py:20-22`, `tests/test_priority7_error_handling.py:20-21`, `AUTONOMY.md:144`) and TS-12 (`scripts/css_audit/n4_regions_abc.mjs:590`) against the snapshot.*

*TS-2, TS-7 and TS-13 rest on the reviewer's reading of the `.venv` Flask/Werkzeug sources and are treated as design inputs, measured at A8c, A8e and A8b. Every finding has a row. Merged findings carry the same action and point to each other. **The owner confirms every disposition at Gate 1.** No finding was blocking and none is rejected or deferred.*

| # | Finding (one line) | Reviewer | Disposition | Action in Plan v2 |
|---|---|---|---|---|
| AR-1 | Reloader parent registers DB cleanup on a runtime it never initialized | architecture-reviewer | **accept** (merged with TS-3) | §V5: cleanup/signal registration factored into `_register_shutdown_cleanup()` and called only when `should_initialize_runtime(...)` is true. New test `test_main_reloader_parent_registers_no_db_cleanup`. C-4 and D-18 reworded (§V10, §V15). |
| AR-2 | "Nothing reads `DB_FILE` between import and init" is asserted, not tested | architecture-reviewer | **accept** | AC1 probes also count `DatabaseHandler` construction and `sqlite3.connect` calls during `import app` and require 0 (refinement R-1). C-2 becomes a tested invariant. |
| AR-3 | Every Flask CLI subcommand against `create_initialized_app` initializes the runtime | architecture-reviewer | **accept** (nit) | C-3 and the `.vscode/launch.json` comment say so. A8a runs with scratch `DB_FILE` and `HT_RUNTIME_DIR`. |
| AR-4 | "step 1 (never raises)" is inaccurate: `copy_legacy_backups()` is outside the `try` | architecture-reviewer | **accept** (nit) | Comment dropped (§V6). New test `test_migration_exception_propagates_and_leaves_guard_unset` (rule iv). |
| TS-1 | `tests/test_program_backup.py:843` (`data.get('data') is None`) changes outcome; plan said only 7 sites change | test-strategist | **accept** | §V2 row and AC6 list (R-3): `:843` becomes `data['data'] == {"auto_backup": None}` (tightened). A3 reworded. A11 is recorded as **refuted in part by grep**: this sixth change is listed, and the full run still settles the rest. |
| TS-2 | `test_every_rule_is_non_strict` fails on Flask's built-in `static` rule | test-strategist | **accept** | AC4 test asserts behavior (trailing-slash GETs on blueprint rules return 200, no `Location`), and `strict_slashes is False` for every rule except endpoint `static`, with the reason recorded (R-2). §V5 comment fixed. A8c fallback has no per-rule production edit. |
| TS-3 | In-process `main()` tests would install process-global atexit/signal hooks | test-strategist | **accept** (merged with AR-1) | Same seam as AR-1. `main()` tests patch `app._register_shutdown_cleanup`; the test of that function patches `atexit.register` and `signal.signal`. D-18 ordering is asserted through the seam. |
| TS-4 | No Chromium baseline; known red not named | test-strategist | **accept** | S1 records a Chromium baseline in the clone with the same seed settings. Pass = no new red against it. `e2e/program-backup.spec.ts:79` is named and needs an isolated rerun before being classed as known. Snapshots are never updated (§V9, §V13). |
| TS-5 | `test_runtime_init.py` autouse fixture leaks `utils.config.DB_FILE` and env | test-strategist | **accept** | The autouse fixture monkeypatches `utils.config.DB_FILE` and env `DB_FILE`/`HT_RUNTIME_DIR`/`TESTING`, resets the guard before and after, and asserts restoration at teardown (§V12 AC3). |
| TS-6 | Two logging tests are order-dependent | test-strategist | **accept** | Tests prime `get_logger()` before patching and assert no handler is added. The handler test compares before/after with exact types (§V12 AC4). |
| TS-7 | A8e default-handler check cannot run in-process; `app.logger` is shared | test-strategist | **accept** | A8e measured in a subprocess. §V7 records that `app.logger` is the process-global logger named `"app"`, shared by every `create_app()` instance. |
| TS-8 | Existing-DB upgrade path has no PR-time automated test | test-strategist | **accept** | New subprocess pytest `test_init_runtime_upgrades_old_schema_database` (old-schema DB from `tests/fixtures/make_old_schema_db.py`). Outcome-field tests are parametrized over all six `migration_action` values, including `failed`. RP-7 stays an owner option, not the only evidence (§V12, §V16 A7). |
| TS-9 | Boundary proof is direct-import only | test-strategist | **accept** | New fresh-interpreter test `test_importing_runtime_init_loads_no_app_or_routes` (§V12 AC2). |
| TS-10 | The 13-name list in `test_app_factory.py` is a second registration site | test-strategist | **accept** (nit) | AC13 wording names it as the one deliberate second site, a test oracle (R-4). |
| TS-11 | Stale comments not listed | test-strategist | **accept** (nit) | Added to in-place corrections: `tests/test_trailing_slash_routing.py:20-22`, `tests/conftest.py:140-143`, `tests/test_priority7_error_handling.py:20-21` (comment only; its minimal app unchanged), and the `AUTONOMY.md:144` rationale (rule unchanged) (R-4, §V2). |
| TS-12 | Cite rule (v) evidence; error text should tell the developer what to do | test-strategist | **accept** (nit) | C-5 cites the css_audit spawners' `TESTING: '0'` (`n4_regions_abc.mjs:590`). The rule (v) message says to unset `TESTING` or pass an explicit `db_file` (§V6). |
| TS-13 | `flask run --reload` parent also loads the app; `-n 8` is local-only | test-strategist | **accept** (merged with PR-4) | Resolved by design (§V7, D-10): the parent also calls `create_initialized_app()`. Parent and child are separate processes, so the in-process guard cannot raise across them; each initializes and each writes a snapshot, as today. The repaired callers keep `--no-reload`. A8b becomes a pre-Gate-2 measurement. §V13 notes CI `pytest-core` is serial with `--cov`. |
| PR-1 | Stale `FLASK_APP=app.py`/`app:app` silently serves an uninitialized runtime | product-risk-reviewer | **accept in part; owner choice at Gate 1** | C-3 and the PR note state the symptom: an empty database file may be created at the resolved path, and a later normal start would **not** re-seed it, because the seed copies only into a missing file. Recommended: documentation-only mitigation in WS3. A `before_request` guard contradicts AC4 (only request-id + cache-policy hooks), would fire under the unseeded conftest `app`, and the stale paths are developer-only once both known callers are repaired. The guard is offered as the alternative at Gate 1 (§V18 item 5). |
| PR-2 | `product-risk-reviewer` should be a required diff-time reviewer | product-risk-reviewer | **reviewer disagreement; owner decision at Gate 1** | product-risk-reviewer: required. test-strategist and Plan v1: optional, because the table requires it only on a production response-shape change and there is none. Both positions are recorded. **Recommendation: include it**, because startup, backup and erase are refactor-invariant workflows. It is an additional reviewer, so the owner decides (§V14, §V18 item 6). |
| PR-3 | Reloader snapshot count change is a Backup-contract change | product-risk-reviewer | **accept** | C-4 and the PR migration note: under the reloader via `python app.py`, startup snapshots per start go from 2 to 1. Rotation keeps 7 (`utils/auto_backup.py:15,23-34`), so the oldest snapshot is evicted one start later (§V10). |
| PR-4 | `RuntimeError` guard on the production path; reloader parent unmeasured | product-risk-reviewer | **accept** (merged with TS-13) | Same as TS-13. A8b is a pre-Gate-2 measurement that must confirm no `RuntimeError` and record the snapshot count; the PR records the result. |
| PR-5 | C-11 should say "test harness only" | product-risk-reviewer | **accept** (nit) | C-11 is labelled "test harness only" in §V10 and the PR note. |

**Counts:** 22 rows: 20 accept, 1 accept in part with an owner choice (PR-1), and 1 reviewer disagreement for owner decision (PR-2). None rejected, none deferred. Merged pairs: AR-1 + TS-3, and TS-13 + PR-4.

---

## Plan v2

*Written 2026-10-20 (rev 4) by `product-manager` `a9259355287e3c511`, resumed by the manager via `SendMessage` after the council. This is a **complete, self-contained plan**; Plan v1 is kept above, unchanged since its review, for the audit trail. Every `path:line` is against `origin/main` `f3adacf1c1b48cc6e2c7ca9ac900e3294b3bae2d`, read from the byte-exact snapshot `artifacts/ws3-app-factory-20261020/src-f3adacf1/`. Changes from v1 are tagged with the finding that caused them, e.g. [AR-1] or [TS-2]. Section numbers are §V1…§V18 to keep them distinct from v1's §P-numbers.*

**Goal**: `import app` does no database or data-directory work. Production, the packaged launcher, `flask run` and the test suite build the application through `create_app()`, and every runtime initialization goes through one guarded `init_runtime()`. Startup order, unseeded test schemas, all 13 blueprints and every handler, filter, hook and context processor, the `/erase-data` confirmation/backup contract, and production API and calculation semantics are preserved.

**Scope**
- **In**: Section 0 *In scope*, made concrete by §V2.
- **Out**: Section 0 *Out of scope / non-goals*, unchanged: no Waitress or server change, service extraction, dependency regrouping, calculation change, schema change, CI redesign, broad documentation cleanup or recovery operation. WS3 also edits none of these:
  - DB-row files: `utils/db_initializer.py`, `utils/database.py`, `utils/auto_backup.py`, `utils/program_backup.py`;
  - runtime-step modules: `utils/runtime_migration.py`, `utils/catalog_seed.py`, `utils/catalog_upgrade.py`, `utils/schema_registry.py`;
  - `scripts/**`, `.github/**`, `Hypertrophy-Toolbox.spec`, `START.bat`, `RUN_APP.bat`, `playwright.config.ts`.

  Retiring the Puppeteer runner and an uninitialized-runtime `before_request` guard are also out, unless the owner selects the guard at Gate 1 (PR-1).

**Effort**: L · **Owner**: a manager-led implementation session in an owner-created standalone clone (RP-1); `automation-qa` writes tests; `senior-developer` writes production code, launch configurations, documentation and the regenerated inventory · **Depends on**: owner Gate 1 (§V18); IC-1…IC-8; RP-1…RP-5; RP-6/RP-7 if adopted.

### V1. Acceptance-criterion refinements (binding once the owner approves Plan v2)

Section 0's AC text stays as signed at Gate 0. These refinements follow from the council and apply to implementation once Gate 1 approves Plan v2:
- **R-1 (AC1)** [AR-2]: the import probes also count `DatabaseHandler` construction and `sqlite3.connect` calls during `import app`, and require 0.
- **R-2 (AC4)** [TS-2]: "`strict_slashes=False` is in effect on all rules" becomes "on every rule except Flask's built-in `static` rule". Flask adds that rule inside `Flask.__init__` before any setting can apply, which is also true today at `app.py:52-53`. In addition, trailing-slash GETs on blueprint rules are served 200 with no `Location` header.
- **R-3 (AC6)** [TS-1]: the listed assertion changes add `tests/test_program_backup.py:843`. `data.get('data') is None` becomes `data['data'] == {"auto_backup": None}`.
- **R-4 (AC13)** [TS-10, TS-11]:
  - The replacement for "register in both" reads: "register in `create_app()` (`app.py`) and add the name to `EXPECTED_BLUEPRINTS` in `tests/test_app_factory.py`, the one deliberate second site, a test oracle".
  - The in-place corrections add `tests/test_trailing_slash_routing.py:20-22`, `tests/conftest.py:140-143`, `tests/test_priority7_error_handling.py:20-21` (comment only) and the `AUTONOMY.md:144` rationale. The confirmation rule itself is unchanged.
- **R-5 (AC7)** [AR-1, TS-3]: the reloader parent neither initializes nor registers the WAL-checkpoint cleanup or signal handlers.

### V2. File manifest

| Path | Change | Purpose | Agent | Step |
|---|---|---|---|---|
| `utils/runtime_init.py` | **new** | `RuntimeInitOutcome`, `init_runtime(db_file=None)`, `should_initialize_runtime(use_reloader)`, private `_reset_for_tests()` (§V6). Imports only `utils` modules and Werkzeug. | `senior-developer` | S3 |
| `app.py` | modify | Adds `create_app(config_overrides=None)`, `create_initialized_app()`, `main()` and `_register_shutdown_cleanup()` [AR-1/TS-3]. Module-level `logger = get_logger()` replaces `setup_logging(app)` (`:72`). The filter, hook, context-processor and view functions move to module level and are registered by `create_app()`. `app = create_app()` stays at module level. Removed: the five runtime steps (`:92-108`), the debug listing (`:127-131`), `start_timer` (`:160-163`), and the unused imports `prepare_runtime_database`, `bootstrap_runtime_database`, `upgrade_catalog_from_seed`, `setup_logging`, `g` and `time`. The `:303-306` comment is rewritten (§V5). | `senior-developer` | S4 |
| `app_launcher.py` | modify | `main()` calls `init_runtime()` right after `from app import app` (`:69`), inside the existing `try`. | `senior-developer` | S4 |
| `utils/logger.py` | modify | Delete the `if app:` branch (`:74-114`) and the `app` parameter of `setup_logging()` (`:25`). | `senior-developer` | S4 |
| `.vscode/launch.json` | modify | `:23` becomes `"FLASK_APP": "app:create_initialized_app"`. The comment at `:5-10` is corrected: startup no longer runs at import. `--no-reload` stays load-bearing because the factory initializes in every process that loads it. **Every Flask CLI subcommand against this factory (`run`, `routes`, `shell`, …) initializes the runtime database** [AR-3]. | `senior-developer` | S4 |
| `e2e/run_puppeteer_summary_regression.ps1` | modify | `:29` becomes `$env:FLASK_APP = "app:create_initialized_app"`. | `senior-developer` | S4 |
| `tests/test_runtime_init.py` | **new** | AC2 boundary (AST + fresh interpreter [TS-9]); AC3 (a)–(f) with an isolating autouse fixture [TS-5]; AC5b; the reset contract; the reloader helper; outcome fields over all six migration actions [TS-8]; the old-schema upgrade subprocess test [TS-8]; migration-exception propagation [AR-4]. | `automation-qa` | S2 |
| `tests/test_app_factory.py` | **new** | AC4 (incl. R-2 behavior and order-independent logging checks [TS-2, TS-6]); AC6 fixture identity; AC7 (mocked `main()` and launcher, incl. no parent cleanup [AR-1/TS-3]); AC8; AC9; AC10; AC11; `EXPECTED_BLUEPRINTS` oracle [TS-10]. | `automation-qa` | S2 |
| `tests/test_real_app_db_isolation.py` | modify | AC1 import probes incl. R-1 [AR-2]; init-subject probes replace the import-subject ones; the negative test is replaced (A4); the docstring is rewritten; `test_real_app_client_lands_on_its_scratch_database` is unchanged. | `automation-qa` | S2 |
| `tests/test_runtime_paths.py` | modify | `TestPacketB2MovesTheDatabase::test_startup_migrates_before_it_seeds` (`:200-222`) becomes the mock-based AC2 order test. | `automation-qa` | S2 |
| `tests/test_catalog_seed_bootstrap.py` | modify | The subprocess at `:141-144` runs `import app; assert app.create_initialized_app().test_client().get('/').status_code == 200`. Assertions at `:159-170` are unchanged. | `automation-qa` | S2 |
| `tests/test_logger.py` | modify | `TestFlaskIntegration::test_flask_app_provided_configures_app_logger` (`:227-239`) is replaced by `test_setup_logging_takes_no_app_argument`. | `automation-qa` | S2 |
| `tests/conftest.py` | modify | The `app` fixture becomes `create_app(config_overrides={"TESTING": True, "WTF_CSRF_ENABLED": False})`, with a lazy import. The twin is deleted: the 13 imports (`:10-22`), the copied filter, the guard-less route, and `_initialize_test_database` if nothing else uses it. `real_app_client` moves to explicit init (§V4 row 5). Docstrings are corrected, incl. `:140-143` [TS-11]. | `automation-qa` | S5 |
| `tests/test_export_blank_rep_bounds_contract.py:58-67`, `tests/test_export_blank_rep_bounds_gate0.py:47-57` | modify | `"requestId": None` (`:65`, `:55`) becomes equality with the response's `X-Request-ID` header, which must also match `^req_[0-9a-f]{16}$`. | `automation-qa` | S5 |
| `tests/test_database_user_profile.py:170`, `tests/test_db_migration.py:171`, `tests/test_program_backup.py:822,838,855` | modify | Each sends `json={"confirm": "ERASE_ALL_DATA"}`. **Also** `tests/test_program_backup.py:843`: `data.get('data') is None` becomes `data['data'] == {"auto_backup": None}` [TS-1]. | `automation-qa` | S5 |
| `tests/test_pattern_coverage.py` | modify | Delete the dead `app_client` fixture (`:346-423`). | `automation-qa` | S5 |
| `tests/test_erase_data_guard.py` | modify (docstring/comment) | `:3-13`, `:17-18` describe the twin; assertions unchanged. | `automation-qa` | S5 |
| `tests/test_trailing_slash_routing.py` | modify (comment only) | `:20-22` says the conftest app lacks the production hooks; that becomes false [TS-11]. | `automation-qa` | S5 |
| `tests/test_priority7_error_handling.py` | modify (comment only) | `:20-21` "the shared app from conftest.py" wording updated; its self-built minimal app (F1a) is unchanged [TS-11]. | `automation-qa` | S5 |
| `CLAUDE.md` and the F9 `f3adacf1` documentation list | modify in place | AC10 and AC13. `CLAUDE.md` §2 (`:45-54`), `:54` sentence, and §4A (`:136`) gain the Q-WS3-2(a) promise verbatim and stay under 200 lines. Also corrected: `.claude/rules/routes.md:50-51`; `.claude/rules/testing.md:63,121-123,126`; the `.claude/rules/database.md` startup and adding-a-table sentences that WS3 makes false; `.claude/rules/debugging.md:27,29-31,39`; `.claude/agents/architecture-reviewer.md:17,19`; `.claude/agents/code-reviewer.md:13`; `.claude/agents/test-strategist.md:27,32`; `routes/CLAUDE.md:21,25`; `tests/CLAUDE.md:45,73,74`; `docs/ai_workflow/PARALLEL_WORKFLOW.md:7,132` where made false; `docs/product/README.md:191-195`; `docs/DUPLICATION_REGISTRY.md:53`; `docs/E2E_TESTING.md:88-89`. `docs/ai_workflow/AUTONOMY.md:18` gets a wording change only (blueprint registration in `create_app()` in `app.py`). `AUTONOMY.md:144` keeps the rule but its rationale is reworded: a missing `register_blueprint` now 404s in production and in every test, because the tests use the same factory [TS-11]. No file under `.claude/**` is added or deleted. | `senior-developer` | S6 |
| `docs/test_inventory/*` | regenerate | `Test Inventory Drift` (RP-5). | `senior-developer` | S7 |

**Verified to need no edit**:
- `scripts/smoke_packaged_app.py` (A5);
- `tests/test_static_cache_policy.py`, whose `frozen_cache_client` still mutates the module-level object that `real_app_client` wraps;
- `tests/test_css_cascade_contracts.py:1385`;
- `tests/test_local_first_assets.py`;
- `tests/test_free_exercise_db_mapping.py:690-710`, which now exercises the production `safe_media_path` filter, a coverage gain;
- the five F1a minimal apps' code;
- `e2e/scripts/*`;
- `tests/fixtures/make_old_schema_db.py`;
- `tests/test_worktree_snapshot.py:358-366`;
- `docs/archive/**`.

### V3. Module boundaries

- `app.py` gains one import edge, `from utils.runtime_init import init_runtime, should_initialize_runtime`, and keeps today's imports minus the removed ones. `create_app()` stays in `app.py` (Q-WS3-6).
- `utils/runtime_init.py` imports:
  - `os`, `threading`, `dataclasses`, `pathlib` and `werkzeug.serving.is_running_from_reloader`;
  - `utils.config` as a module object, so `importlib.reload(utils.config)` (`tests/test_catalog_seed_bootstrap.py:125-130`, `tests/test_runtime_paths.py`) stays visible;
  - `get_logger` and `runtime_root`;
  - the five step functions by name, so tests patch `utils.runtime_init.<step>`.
  
  It imports no `flask`, `routes`, `app` or `app_launcher`. This is enforced by an AST test and by a fresh-interpreter `sys.modules` test [TS-9].
- `create_app()` calls no runtime step and never calls `setup_logging()`, `DatabaseHandler`, `sqlite3` or any filesystem function. `init_runtime()` never touches a Flask object. Only the entry points join them (§V4).
- `routes` → `utils` only; never the reverse.

### V4. Configuration → logging → factory → runtime-initialization order, per entry point

Configuration is the environment: `DB_FILE`, `HT_RUNTIME_DIR`, `HT_PORT`, `FLASK_DEBUG`, `FLASK_USE_RELOADER`, `TESTING` and `HT_NO_BROWSER`.
- `utils.config.DB_FILE` is resolved from the environment at the first import of `utils.config` (`config.py:22`). It is reassigned **only** by `init_runtime()`, and import-time code reads nothing between the two. AC1 tests this (R-1) [AR-2].
- The logging root is fixed by `HT_RUNTIME_DIR` at the process's first `get_logger()` call (F5).
- The port is read only at serve time.

| # | Entry point (callers) | 1. Configuration | 2. Logging | 3. Factory | 4. Runtime initialization | 5. Serve |
|---|---|---|---|---|---|---|
| 1 | `python app.py`: `START.bat:136`, Playwright webServer, `deep-gate.yml` ×3, `release.yml` ×2, seven `css_audit` spawners, VS Code config 2, packaged payload `app.pyc` | `require_supported_python()` (`app.py:8-10`); `import utils.config` (`:13`) | First `get_logger()` during `from utils.database import …` (`:14`); then module `logger = get_logger()` | Module-level `app = create_app()` in `__main__` | `main()` reads `FLASK_USE_RELOADER`/`FLASK_DEBUG`. If `should_initialize_runtime(use_reloader)`: `init_runtime()`, then `_register_shutdown_cleanup()`. Otherwise (reloader parent) **neither** runs [AR-1]. | `app.run(port=utils.config.runtime_port(), debug=…, use_reloader=…)` |
| 2 | Packaged bootloader `app_launcher.main()`: `Hypertrophy-Toolbox.exe`, `RUN_APP.bat:4`, smoke `--mode bootloader` | Launcher import: frozen `chdir`/`sys.path` (`app_launcher.py:31-45`). `main()`: `require_supported_python()`, then `runtime_port()` | `from app import app` (`:69`) | Module-level `app = create_app()` | Lazy `from utils.runtime_init import init_runtime; init_runtime()` right after the import, inside the same `try`. Failure reaches the error-wait UX (`:100-110`). No WAL cleanup, as today. | Browser thread unless `HT_NO_BROWSER=1`; `app.run(host='127.0.0.1', port=port, debug=False, threaded=True, use_reloader=False)` |
| 3 | `flask <subcommand>` with `FLASK_APP=app:create_initialized_app`: `.vscode/launch.json` config 1 (`run --no-reload`), the Puppeteer `.ps1` (`run --no-reload`) | Environment | The CLI imports module `app` | Module-level `app` #1 (never served); the CLI then calls `create_initialized_app()` → `app` #2 | `init_runtime()` inside `create_initialized_app()`. **Every subcommand that loads the app initializes** (`run`, `routes`, `shell`) [AR-3]. Under `run --reload` the reloader parent loads the app too, so parent and child each initialize in their own process (§V7) [TS-13/PR-4]. | `flask run` serves #2 |
| 4 | pytest `app` fixture | `conftest.py:30` `TESTING=1`; per test `utils.config.DB_FILE = test_db_path` | Already configured by `conftest.py:9` | Lazy `from app import create_app` (first use builds module-level `app`, no init), then `create_app(config_overrides={"TESTING": True, "WTF_CSRF_ENABLED": False})` | **None**; the schema is a copy of `schema_template` (`conftest.py:296-300`), so it stays unseeded | Test client |
| 5 | `real_app_client` (module scope) | Env `DB_FILE`/`HT_RUNTIME_DIR` set to scratch (kept from `:174,179`), attribute set | Already configured | `from app import app as real_app` (module-level object, no init) | `_reset_for_tests()`, then `outcome = init_runtime(db_file=str(scratch_db))`: explicit override → `DB_FILE` = scratch → seed copy (`seeded=True`) → `run_all_initializers(force_base=False)`; upgrade and backup skipped. Asserts `outcome.database_path` and `utils.config.DB_FILE` resolve to scratch, else `pytest.fail`. Teardown restores env and attribute and calls `_reset_for_tests()`. | `real_app.config['TESTING'] = True`; test client |
| 6 | Subprocess tests | Explicit `env` | Inside the probe | (a) AC1 probes: `import app` only; (b) first install: `app.create_initialized_app()` | (a) none; (b) once; (c) init probes and the old-schema test call `init_runtime(...)` directly | (b) test client only |
| 7 | Packaged smoke's own process (`smoke_packaged_app.py:247`) | No `DB_FILE`/`HT_RUNTIME_DIR` | `from app import STATIC_LONG_MAX_AGE_SECONDS` | Module-level `create_app()` | **None** (A5 change). Children follow row 1 or row 2. | — |

**Equivalence of `real_app_client`.** Under `TESTING=1` the `initialize_database()` guard is bypassed whatever `force` is (`db_initializer.py:569,575`), so `force_base=False` builds the same schema as today's `force_base=True` (`conftest.py:204-206`). On a just-seeded scratch database the upgrade and backup are skipped, and `create_startup_backup()` returns `None` under `TESTING=1` anyway (`auto_backup.py:45-46`). The resulting state therefore matches today's, including the seeded catalog that `test_erase_data_guard.py:94-95` requires. The explicit-argument branch is the first branch of `prepare_runtime_database()` (`runtime_migration.py:236-242`), proven by AC5b and checked again before yield.

### V5. `create_app()` and the shape of `app.py`

```python
# app.py, in module order
from utils.python_version import require_supported_python
require_supported_python()
# imports: today's set (:12-45) minus prepare_runtime_database, bootstrap_runtime_database,
#          upgrade_catalog_from_seed, setup_logging, g, time; plus:
from flask import current_app
from utils.logger import get_logger
from utils.runtime_init import init_runtime, should_initialize_runtime

STATIC_LONG_MAX_AGE_SECONDS = 31536000          # unchanged (:50)
logger = get_logger()                           # replaces setup_logging(app) (:72)

def format_datetime(value, date_format='%d-%m-%Y'): ...     # body verbatim (:134-145)
def safe_media_path(value): ...                             # body verbatim (:149-158)
def apply_static_cache_policy(response): ...                # verbatim except app.config -> current_app.config (:196)
def inject_app_version(): ...                               # verbatim (:210-222)
def inject_scale_level(): ...                               # verbatim (:226-241)
def erase_data(): ...                                       # body verbatim (:246-271)

def create_app(config_overrides: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(__name__)                                   # F3; Flask adds its `static` rule here,
                                                            # bound with strict_slashes=True, as today [TS-2]
    app.url_map.strict_slashes = False                      # F3; before any blueprint rule is added
    app.wsgi_app = ProxyFix(app.wsgi_app)                   # F3
    if getattr(sys, 'frozen', False):                       # F3 frozen block, verbatim (:57-69)
        ...
    if config_overrides:                                    # 3b: after the frozen block
        app.config.update(config_overrides)
    add_request_id_middleware(app)
    register_error_handlers(app)                            # errors.py:232-236 order
    register_fallback_handlers(app)
    for blueprint in (main_bp, workout_log_bp, weekly_summary_bp, session_summary_bp,
                      exports_bp, filters_bp, workout_plan_bp, progression_plan_bp,
                      user_profile_bp, body_composition_bp, volume_splitter_bp,
                      program_backup_bp, fatigue_bp):       # today's 13, today's order (:111-125)
        app.register_blueprint(blueprint)
    app.add_template_filter(format_datetime, 'datetime')
    app.add_template_filter(safe_media_path, 'safe_media_path')
    app.after_request(apply_static_cache_policy)
    app.context_processor(inject_app_version)
    app.context_processor(inject_scale_level)
    app.add_url_rule('/erase-data', endpoint='erase_data', view_func=erase_data, methods=['POST'])
    return app

def create_initialized_app() -> Flask:
    init_runtime()
    return create_app()

app = create_app()

def _register_shutdown_cleanup() -> None:                   # [AR-1, TS-3] patchable seam
    import atexit, signal
    # cleanup_on_exit and signal_handler definitions: verbatim from :280-298
    atexit.register(cleanup_on_exit)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def main() -> None:                                         # today's __main__ body (:275-314)
    use_reloader = os.getenv('FLASK_USE_RELOADER', '0') == '1'
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    if should_initialize_runtime(use_reloader):             # reloader parent: neither step
        init_runtime()
        _register_shutdown_cleanup()
    app.run(port=utils.config.runtime_port(), debug=debug_mode, use_reloader=use_reloader)

if __name__ == "__main__":
    main()
```

**Compared with F3.** The order is F3's with four items removed:
- `setup_logging(app)` (Q-WS3-2a);
- the five runtime steps (now `init_runtime()`);
- the debug listing (3a);
- `start_timer` (Q-WS3-2H).

The only addition is `config_overrides`, applied after the frozen block. The runtime steps touch no Flask object, so moving them out changes no app state (F8a).

**The `:303-306` comment** becomes: "`use_reloader` defaults to off. With `FLASK_USE_RELOADER=1`, only the serving child initializes the runtime and registers the WAL cleanup (see `should_initialize_runtime`). For `flask run`, use `FLASK_APP=app:create_initialized_app` with `--no-reload`; every `flask` subcommand against that factory initializes the runtime database."

### V6. `init_runtime()` specification

```python
# utils/runtime_init.py
@dataclass(frozen=True)
class RuntimeInitOutcome:
    database_path: Path          # migration.database_path, as assigned to utils.config.DB_FILE
    migration_action: str        # explicit-override | same-path | already-present | no-legacy | migrated | failed
    seeded: bool                 # this process published this database from the seed (incl. a failed earlier attempt)
    snapshot_path: Path | None   # create_startup_backup() result, or None when skipped
    already_initialized: bool    # True only on a guarded no-op return

_lock = threading.Lock()
_completed: tuple[tuple[str | None, str], RuntimeInitOutcome] | None = None
_seeded_databases: set[str] = set()            # resolved database paths seeded in this process

def _guard_key(explicit: str | None) -> tuple[str | None, str]:
    requested = explicit if explicit is not None else (os.environ.get("DB_FILE") or None)
    requested_key = str(Path(requested).expanduser().resolve()) if requested else None
    return (requested_key, str(runtime_root()))            # rule (i)

def init_runtime(db_file: str | os.PathLike[str] | None = None) -> RuntimeInitOutcome:
    global _completed
    if db_file is not None and not os.fspath(db_file):
        raise ValueError("db_file must be a non-empty path or None")
    explicit = os.fspath(db_file) if db_file is not None else None
    with _lock:
        key = _guard_key(explicit)
        if os.environ.get("TESTING") == "1" and key[0] is None:              # rule (v), before any file access
            raise RuntimeError(                                              # [TS-12]
                "init_runtime() refuses to run under TESTING=1 without an explicit "
                "db_file or a DB_FILE environment variable. If this is not a test run, "
                "unset TESTING; in a test, pass db_file=<scratch path>.")
        if _completed is not None:
            done_key, done = _completed
            if key == done_key:                                              # rule (ii)
                logger.debug("Runtime already initialized for %s; skipping", done.database_path)
                return dataclasses.replace(done, already_initialized=True)
            raise RuntimeError(f"init_runtime() already initialized {done_key}; "  # rule (iii) / 4a
                               f"refusing a different database or runtime root {key}")
        # Rule (iv): any exception below propagates with _completed still None.
        migration = prepare_runtime_database(explicit_override=explicit)     # step 1; an exception from
                                                                             # copy_legacy_backups() propagates [AR-4]
        utils.config.DB_FILE = str(migration.database_path)                  # step 2, the only assignment
        seeded_now = bootstrap_runtime_database()                            # step 3
        database_key = str(Path(utils.config.DB_FILE).expanduser().resolve())
        if seeded_now:
            _seeded_databases.add(database_key)                              # 4c carry-over
        seeded = database_key in _seeded_databases
        run_all_initializers(force_base=False)                               # step 4
        snapshot = None
        if not seeded:
            upgrade_catalog_from_seed()                                      # step 5
            snapshot = create_startup_backup()                               # step 6
        outcome = RuntimeInitOutcome(Path(migration.database_path), migration.action,
                                     seeded, snapshot, False)
        _completed = (key, outcome)
        logger.info("Runtime initialized: database=%s migration=%s seeded=%s snapshot=%s",
                    outcome.database_path, outcome.migration_action, seeded, snapshot)
        return outcome

def should_initialize_runtime(use_reloader: bool) -> bool:
    """Reloader rule: initialize (and register DB cleanup) only in the serving process."""
    return (not use_reloader) or is_running_from_reloader()

def _reset_for_tests() -> None:
    """Test-only (rule vi). Never called by production code; tests enforce this."""
    global _completed
    with _lock:
        _completed = None
        _seeded_databases.clear()
```

**Rules mapped to the accepted recommendation:**
- (i) The key is (resolved requested path or `None`, `runtime_root()`), stored only after success.
- (ii) The same key is a no-op.
- (iii) A different key raises `RuntimeError` before any step, so `utils.config.DB_FILE` is untouched (4a).
- (iv) An exception leaves the guard unset, including one from `copy_legacy_backups()` [AR-4].
- 4c: the carry-over is keyed by the resolved **database path**.
- (v) Under `TESTING=1`, a call with no path refuses, with an actionable message [TS-12].
- (vi) `_reset_for_tests()`.
- The reloader rule lives in `should_initialize_runtime()`.

**It does not touch** `utils.db_initializer._INITIALIZATION_COMPLETE`. `/erase-data` keeps calling `create_startup_backup()`, `drop_all_owned_tables()` and `run_all_initializers(force_base=True)` directly. A `failed` migration still proceeds on the legacy path (`runtime_migration.py:258-265`).

### V7. Repeated factory and repeated runtime behavior

**Repeated `create_app()`.**
- Each call returns a new `Flask` instance with its own `config`, `url_map` and handler maps.
- The 13 blueprint singletons are registered on each instance.
- Hook, filter and view functions are the same module-level objects.
- No `hypertrophy_toolbox` handler is added, because `get_logger()` is cached.
- No database, data-directory, migration, seed, upgrade or snapshot work happens.
- Earlier instances and the module-level `app` are not affected.
- **`app.logger` is Flask's process-global logger named after `app.name` (`"app"`), so every `create_app()` instance in a process shares it** [TS-7]. WS3 adds no handler to it and aliases none (A8e measures the default-handler state in a subprocess).
- A pytest process holds one module-level instance plus one per `app`-fixture test.

**Repeated `init_runtime()`.**

| Situation | Result |
|---|---|
| Same key after success | No-op; cached outcome with `already_initialized=True`; no step; no snapshot |
| Different key after success | `RuntimeError`; nothing runs; `utils.config.DB_FILE` unchanged |
| Retry after an exception (incl. from `copy_legacy_backups()`) | Runs again. A database seeded by the failed attempt counts as `seeded`, so upgrade and backup stay skipped. |
| `TESTING=1`, no explicit path, no env `DB_FILE` | `RuntimeError` before any file access, with an actionable message |
| After `_reset_for_tests()` | First-call behavior; tests only |
| Reloader on via `python app.py` | Parent: no init, no cleanup registration. Serving child: one init, one cleanup registration, one snapshot (when not seeded). |
| `flask run --reload` (no supported caller uses it) | **Resolved by design** [TS-13/PR-4]. `flask run` loads the app in the reloader parent too (`.venv` Flask `cli.py:962-963`, per TS-13), so the parent calls `create_initialized_app()` as well. Parent and child are **separate processes, each with its own in-process guard**, so the guard cannot raise across them. Each initializes, and each writes a snapshot when the database was not just seeded. That matches today, where import-time startup runs in both. The repaired callers keep `--no-reload`, and the `app.py` comment does not recommend `--reload`. A8b confirms this before Gate 2 (no `RuntimeError`; snapshot count recorded). |

### V8. Caller migration, caller by caller

| Caller | Today | After WS3 | Edit |
|---|---|---|---|
| `app_launcher.py:69` | Import runs startup | Import, then explicit `init_runtime()` | Yes (S4) |
| `python app.py` callers (§V4 row 1) | `__main__` after import-time startup | `main()`, with init and cleanup under the reloader rule | None to callers |
| `.vscode/launch.json:23` | `FLASK_APP=app.py` | `app:create_initialized_app` | Yes (S4), plus comment [AR-3] |
| `e2e/run_puppeteer_summary_regression.ps1:29` | `FLASK_APP=app:app` | `app:create_initialized_app` | Yes (S4) |
| `app.py:306` comment | Recommends `flask run --reload` | §V5 text | Yes (S4) |
| `tests/conftest.py` `app` | Hand-built twin | `create_app(config_overrides=…)`; no init | Yes (S5) |
| `tests/conftest.py` `real_app_client` | Import-time startup + path assertion + bootstrap + initializers | Explicit `_reset_for_tests()` + `init_runtime(db_file=…)` | Yes (S5) |
| `tests/test_static_cache_policy.py:54,108,162` | Module-level `app`, constant | Unchanged | None |
| `tests/test_pattern_coverage.py:346-423` | Dead fixture | Deleted | Yes (S5) |
| `tests/test_real_app_db_isolation.py` | `import app` subject | `import app` for AC1; `init_runtime()` for AC5 | Yes (S2) |
| `tests/test_catalog_seed_bootstrap.py:142` | `import app` seeds | `app.create_initialized_app()` seeds | Yes (S2) |
| `tests/test_runtime_paths.py:200-222` | AST line order | Mock order over `init_runtime` | Yes (S2) |
| `tests/test_program_backup.py:822,838,843,855` | Twin; `data` absent | Token sent; `data == {"auto_backup": None}` at `:843` [TS-1] | Yes (S5) |
| `scripts/smoke_packaged_app.py:247` | Import runs startup in-process | Import only (A5) | None |
| `docs/product/README.md:191` | Command runs startup | Command lists routes with no data work | Prose `:194-195` (S6) |
| `docs/archive/2026/one-off-scripts/fatigue/*` | `from app import app` | Still imports; no initialization | None (archived) |
| `e2e/scripts/prepare_*`, `tests/fixtures/make_old_schema_db.py`, F1a minimal apps | Do not import `app` | Unchanged | None (F1a: comment at `test_priority7_error_handling.py:20-21` only) |

### V9. Sequencing (steps, commits, agents)

- **S0 — Readiness (manager; no code).**
  - Record IC-1…IC-8, RP-1 and RP-2.
  - Fetch `origin/main` in the standalone clone. If the base is not `f3adacf1`, run `git diff --stat f3adacf1 <base> -- <every §V2 path>`. A non-empty diff sends the plan back to the `product-manager` before S2.
  - Record the private paths: venv, `HT_RUNTIME_DIR`, `TEMP`/`TMP` (created, `len <= 103`), `PYTHONPYCACHEPREFIX`, npm cache.
- **S1 — Pre-change evidence at the base revision (`senior-developer`, clone scratch only, under `artifacts/ws3-impl-<date>/`).**
  - (a) Capture the URL map (rule, endpoint, methods) using the `docs/product/README.md:191` command with scratch `HT_RUNTIME_DIR` and `DB_FILE` (D-16).
  - (b) Run the A6 and A11 greps.
  - (c) Record a full-pytest baseline (`CLAUDE.md` §4B step 1, `:144-148`).
  - (d) **Record a Chromium baseline with the same seed settings the later run will use** (`PW_VISUAL_SEED` unset for the functional run; record the exact environment) [TS-4].
- **S2 — Acceptance tests first (`automation-qa`, from Gate-1-approved Plan v2).** The two new files and the S2 rows of §V2. Expected red on unchanged code. **Commit C1.**
- **S3 — `utils/runtime_init.py` (`senior-developer`).** **Commit C2.** `tests/test_runtime_init.py` and the AC2 order test go green.
- **S4 — Factory, launchers and logger (`senior-developer`).** `app.py`, `app_launcher.py`, `utils/logger.py`, `.vscode/launch.json` and the `.ps1` go in **one commit, C3** (D-19). Expected green: everything except the AC6 fixture-identity test.
- **S5 — Harness migration (`automation-qa`).** `tests/conftest.py`, the two `requestId` tests, the five token sites plus `:843`, the dead fixture and the comment/docstring corrections go in **commit C4**. Run full pytest; triage under A11. Every commit from C4 on is green.
- **S6 — Documentation (`senior-developer`).** AC10/AC13 with R-4, in **commit C5**. Each edit starts from the fetched-main version of the file and is coordinated per RP-2/IC-4.
- **S7 — Generated and static gates (`senior-developer`).** Inventory regeneration (RP-5) in **commit C6**; pyright baseline diff, vulture, flake8.
- **S8 — Diff-time gate.** `/verify-and-polish` in the clone, run by the manager: `/verify-suite` against the S1 baselines, the §V14 reviewers, the manual backup/restore smoke and the launch-path checks (§V13). **A8b's measurement (§V16) must be recorded before Gate 2** [PR-4].
- **S9 — CI observation.** Push the branch and open a PR without merging, only if Gate 1 adopts RP-6, to observe the packaged bootloader smoke (RP-3). A merge needs separate explicit owner confirmation naming the PR.

**Landing unit.** One PR. If it is not squash-merged, C1 is folded into C3 before merge, so `main` never holds a red commit.

### V10. Compatibility changes (all intentional; carried into the PR's migration notes)

1. **C-1** `import app` no longer runs migration, seed, initializers, upgrade or backup. This affects ad-hoc `python -c "import app"` use, the smoke's own process (A5), `docs/product/README.md:191` (now free of data work) and the archived scripts.
2. **C-2** `utils.config.DB_FILE` is no longer reassigned at import. It holds the environment/resolver value until `init_runtime()` assigns it once. **Tested invariant:** importing `app` constructs no `DatabaseHandler` and calls no `sqlite3.connect` (AC1/R-1) [AR-2].
3. **C-3** `FLASK_APP=app.py` or `app:app` now serves an **uninitialized** runtime [PR-1]:
   - **Symptom:** if no database exists at the resolved path, the first request makes `DatabaseHandler` create an **empty** file there. The user sees an empty app, while any un-migrated legacy database stays untouched at its old path.
   - **A later normal start does not re-seed that empty file**, because the seed copies only into a missing file (`catalog_seed.py:46-47`).
   - Both known callers are repaired. Developers must use `app:create_initialized_app`.
   - **Every `flask` subcommand against `create_initialized_app` (`run`, `routes`, `shell`, …) initializes the runtime database** [AR-3].
   - Mitigation is documentation-only unless the owner selects the guard at Gate 1 (§V18 item 5).
4. **C-4** Reloader on via `python app.py` [AR-1, PR-3]:
   - The monitoring parent no longer migrates, seeds or snapshots, and no longer registers the WAL-checkpoint cleanup or SIGINT/SIGTERM handlers. It therefore opens no database. The serving child still does all of these once.
   - **Backup contract note:** startup snapshots per start go from 2 to 1 under the reloader. Rotation keeps the newest 7 (`utils/auto_backup.py:15,23-34`), so each start now evicts at most one old snapshot instead of two, and a given snapshot is retained over more starts.
   - Without the reloader there is no change: one snapshot per non-seeded start.
5. **C-5** New guard behavior: same key is a no-op; a different key raises `RuntimeError`; `TESTING=1` without a path raises `RuntimeError` with an actionable message. No known launcher sets `TESTING`; the seven `css_audit` spawners set `TESTING: '0'` (`scripts/css_audit/n4_regions_abc.mjs:590`) [TS-12]. A developer with `TESTING=1` exported in their shell now gets that error from `python app.py`.
6. **C-6** A new INFO line, "Runtime initialized: …", is logged once per initializing process.
7. **C-7** The DEBUG route listing is no longer written to `app.log`.
8. **C-8** The never-attached request hooks and `start_timer` are deleted. `setup_logging()` no longer accepts `app`.
9. **C-9** `app` module attributes:
   - Removed: `migration`, `database_seeded`, `start_timer`, and the unused imports.
   - New: `create_app`, `create_initialized_app`, `main`, `_register_shutdown_cleanup`, and the imported `init_runtime`/`should_initialize_runtime`.
   - The hook, filter and view functions are now module-level. `apply_static_cache_policy` reads `current_app.config`.
   - No importer uses a removed name.
10. **C-10** The `__main__` body moves into `main()` and `_register_shutdown_cleanup()`. `python app.py` behaves identically apart from C-4.
11. **C-11 (test harness only; no production change)** [PR-5]. The test `app` fixture is now the production factory app:
    - `requestId` is populated;
    - XHR and `/api/` 404/405 bodies are envelopes;
    - uncaught exceptions return 500 (A8d);
    - 404s log a WARNING to the test run's `app.log`;
    - `/erase-data` requires the token and returns `data == {"auto_backup": null}` under `TESTING`;
    - `app.name` is `"app"`.
12. **C-12** `test_patching_config_alone_is_not_isolation` is replaced (A4). `real_app_client` no longer depends on import order.
13. **C-13** The launcher initializes explicitly after the import, with the same console text and error-wait UX.

**Unchanged:** production API response shapes, calculations, schema, migration/seed/upgrade/backup semantics, the `/erase-data` contract, journal mode and `FLASK_DEBUG` defaults, port handling, frozen static caching, and WAL cleanup in every serving process.

### V11. Rollback

- **Mechanism:** one `git revert` of the landed PR commit. It restores import-time startup, the twin, the old docs and the matching committed `docs/test_inventory/`.
- **No data rollback:** WS3 has no schema or data migration, and databases, snapshots and logs keep their formats and paths. The only persistent difference is fewer reloader-mode snapshots (C-4), which needs no reversal.
- **Partial states (branch only):**
  - After C1, tests are red.
  - After C2, the module is unused.
  - After C3, the AC6 fixture-identity test stays red until C4. The old `real_app_client` still works because import no longer reassigns `DB_FILE`.
  - **Must never reach `main`:** C3 without the `flask run` repairs (D-19), or C5's docs without C3's code.
- **After merge:** a regression in one launch path defaults to reverting the whole PR. A forward fix instead is an owner decision.

### V12. Acceptance criterion → test mapping

| AC | Test(s) | New / changed | Gate |
|---|---|---|---|
| 1 (+R-1) | `test_real_app_db_isolation.py`: `test_import_creates_no_data_without_db_file`, `test_import_creates_no_data_with_missing_db_file`, `test_import_creates_no_data_with_patched_attribute_only`, `test_constant_import_creates_no_data`. Each is a fresh subprocess with `TESTING` removed. Before `import app`, the probe wraps `flask.Flask.__init__`, `utils.database.DatabaseHandler.__init__` and `sqlite3.connect` with counters. It requires exactly 1 Flask construction and 0 `DatabaseHandler`/`connect` calls [AR-2], and `isinstance(app.app, Flask)`. The scratch tree may hold only `logs/` and `logs/app.log`. The env-resolved database must not exist, `utils.config.DB_FILE` must equal its pre-import value, and no `auto_backup/` may appear (scratch tree, `DB_FILE` parent, clone `data/` before/after). The no-`DB_FILE` cases keep `_skip_if_legacy_database_is_busy`. | Changed file; 4 tests replace the import-subject tests | pytest (`/verify-suite`) |
| 2 | `test_runtime_paths.py::TestPacketB2MovesTheDatabase::test_startup_migrates_before_it_seeds`, rewritten: a shared recorder mocks the five steps; each records `utils.config.DB_FILE` at its call (`prepare` sees the sentinel; later steps see the migration path; D-14); asserts `force_base=False`; a second case with `bootstrap` returning `True` asserts upgrade and backup are skipped. `test_runtime_init.py`: `test_outcome_fields` **parametrized over all six `migration_action` values** (for `failed`: `DB_FILE` is set to the legacy path, and the seed is skipped because that file exists) [TS-8]; `test_module_imports_no_routes_or_app` (AST); `test_importing_runtime_init_loads_no_app_or_routes` (a fresh interpreter imports `utils.runtime_init`, then asserts that no `app`, `app_launcher` or `routes`/`routes.*` key is in `sys.modules`) [TS-9]. | Changed + new | pytest |
| 3 | `test_runtime_init.py`, whose **autouse fixture** monkeypatches `utils.config.DB_FILE` and env `DB_FILE`/`HT_RUNTIME_DIR`/`TESTING`, calls `_reset_for_tests()` before and after, and asserts at teardown that the attribute and env are restored [TS-5]. Tests: `test_same_key_is_a_noop` (a); `test_different_database_raises_and_changes_nothing`, `test_different_runtime_root_raises` (b); `test_failed_call_leaves_guard_unset` (c); `test_migration_exception_propagates_and_leaves_guard_unset` (real `prepare_runtime_database` over tmp target/legacy paths, `copy_legacy_backups` patched to raise `OSError`, `TESTING` unset inside the fixture) [AR-4]; `test_retry_after_seed_skips_upgrade_and_backup` (d); `test_testing_without_path_refuses_before_any_step` (e; also asserts that the message names "unset TESTING"); `test_reset_allows_a_different_key` (f); `test_reset_is_never_referenced_by_production_code`, which scans `app.py`, `app_launcher.py`, `utils/**/*.py` except `runtime_init.py`, `routes/**/*.py` and `scripts/**/*.py`; and `test_second_call_takes_no_second_snapshot_subprocess`, a non-`TESTING` subprocess that calls `init_runtime(db_file=<copy of the seed>)` twice and expects exactly 1 file in `auto_backup/`. | New | pytest |
| 4 (+R-2) | `test_app_factory.py`. `test_two_factory_calls_build_distinct_equivalent_apps` checks `EXPECTED_BLUEPRINTS` (13 names, hard-coded) and that rule sets are equal across instances and to the module-level `app`. `test_blueprint_rules_are_non_strict_static_excepted`: every rule except endpoint `static` has `strict_slashes is False`; the reason for the exemption is in the docstring [TS-2]. `test_trailing_slash_get_on_blueprint_rules_is_served` (200, no `Location`, on `create_app(TESTING)`). Also: `test_proxyfix_wraps_wsgi_app`; `test_responses_carry_request_id` (static asset); `test_handler_layering_behaves_as_documented` (XHR 400 → `BAD_REQUEST`; 405 → `METHOD_NOT_ALLOWED` + `Allow`; 404 → `NOT_FOUND`; temporary raising route → 500 `INTERNAL_ERROR`); `test_filters_hooks_processors_and_erase_route_present`; `test_only_request_id_and_cache_policy_hooks`; `test_config_overrides_apply_after_frozen_block`; `test_no_route_listing_logged`. `test_factory_does_no_logging_setup_or_database_work` **primes `get_logger()` first**, then patches `setup_logging` and `sqlite3.connect` to raise; the `DB_FILE` target must not be created [TS-6]. `test_factory_adds_no_logger_handlers` compares the `hypertrophy_toolbox` handler list before and after two `create_app()` calls, with exact types (`type(h) is RotatingFileHandler` / `type(h) is logging.StreamHandler`) [TS-6]. One-off evidence: the S1 vs post-C3 URL-map diff (D-16). | New | pytest; S8 evidence |
| 5a | `test_runtime_paths.py::TestEnvironmentOverride`, unmodified | Unchanged | pytest |
| 5b | `test_runtime_init.py::test_explicit_argument_wins` (mocked); subprocess `test_real_app_db_isolation.py::test_init_runtime_explicit_argument_lands_on_scratch` (`TESTING=1`, no env `DB_FILE`; action `explicit-override`; `DB_FILE` = scratch; no runtime database) | New | pytest |
| 5c | `test_real_app_db_isolation.py::test_init_runtime_ignores_patched_attribute`: a non-`TESTING` subprocess patches the attribute, sets no env `DB_FILE`, sets `HT_RUNTIME_DIR` to a sandbox, and calls `init_runtime()`. Active database = `<sandbox>/data/database.db`; scratch does not exist. Keeps the busy-sidecar skip and replaces `test_patching_config_alone_is_not_isolation`. Also `test_init_runtime_with_env_db_file` and the parametrized `test_env_override_wins_regardless_of_config_patch`. | Changed | pytest |
| 5d | `test_catalog_seed_bootstrap.py::test_real_app_first_install_seeds_catalog_without_mutating_seed`, driven through `create_initialized_app()`; assertions unchanged. **Existing-DB upgrade** [TS-8]: `test_runtime_init.py::test_init_runtime_upgrades_old_schema_database`. Subprocess 1 runs `tests/fixtures/make_old_schema_db.py --output <tmp>/old.db`. Subprocess 2 is non-`TESTING`, with `HT_RUNTIME_DIR` = scratch, and calls `init_runtime(db_file=<tmp>/old.db)`. Expected: action `explicit-override`; `seeded` false; the old schema gains the later tables and the `exercise_order` column; `catalog_version` populated; the `Legacy Routine` row preserved; **exactly one** file in `<tmp>/auto_backup/` (the upgrade brings the catalog to ≥ 100 exercises, `auto_backup.py:59`). | Changed + new | pytest |
| 6 (+R-3) | The full suite on the migrated `tests/conftest.py`. `test_app_factory.py::test_app_fixture_is_the_factory_app`. In-process `test_real_app_db_isolation.py::test_real_app_client_lands_on_its_scratch_database`. The five `real_app_client` consumer modules passing in one serial process (the CI form) and locally under `-n 8 --dist loadfile`. The two `requestId` tests, the five token sites, and `tests/test_program_backup.py:843` [TS-1]. | Changed | `/verify-suite` |
| 7 (+R-5) | `test_app_factory.py`. These tests patch `app._register_shutdown_cleanup` [TS-3]: `test_main_initializes_then_registers_cleanup_before_run` (order init → cleanup → run); `test_main_reloader_parent_does_not_initialize`; `test_main_reloader_parent_registers_no_db_cleanup` [AR-1]; `test_main_reloader_child_initializes_and_registers_cleanup`; `test_main_honours_port_and_debug`. `test_register_shutdown_cleanup_registers_atexit_and_signals` patches `atexit.register` and `signal.signal` and asserts the registrations without installing them. Also: `test_launcher_initializes_after_import_before_run` (`HT_NO_BROWSER=1`, `HT_PORT`; `app.run` kwargs); `test_launcher_init_failure_uses_error_wait` (`input` patched; `SystemExit(1)`); `test_runtime_init.py::test_should_initialize_runtime_matrix`. Real launches: packaged smoke in bootloader (CI) and payload (local) mode; `deep-gate.yml`/`release.yml` jobs (A7); Playwright webServer. | New | pytest; CI packaged smoke (RP-3); `/verify-suite` |
| 8 | `test_erase_data_guard.py`, unchanged. `test_app_factory.py`: `test_erase_success_snapshots_then_drops_then_reinitializes` (mocks record the order and `force_base=True`; `data.auto_backup == {"filename": …}`; exact message); `test_erase_success_without_snapshot_reports_none`; `test_erase_failure_returns_internal_error`; `test_erase_rejection_writes_nothing`. | Unchanged + new | pytest; E2E `erase-flow.spec.ts`, `fatigue.spec.ts` |
| 9 | `test_app_factory.py`: `test_frozen_block_values`; `test_public_import_surface`. `test_static_cache_policy.py`, unchanged. AC1's `test_constant_import_creates_no_data`. | New + unchanged | pytest; packaged smoke |
| 10 | `test_app_factory.py::test_claude_md_states_the_import_promise`; `tests/test_agent_workflow_contracts.py` (`:673-680`) | New + unchanged | pytest |
| 11 | `test_app_factory.py::test_create_initialized_app_initializes_then_builds`; `test_flask_run_callers_use_the_factory` (launch.json with `//` comments stripped, the `.ps1` text, no "flask run --reload" in `app.py`). Real path via AC5d. Manual A8a. | New | pytest; S8 manual |
| 12 | §V13 as a whole | — | S8, plus CI (RP-3) |
| 13 (+R-4) | §V13 item 16 greps, plus diff review by `code-reviewer` (AI-workflow row) | — | S8 |

**Expected gates** (the `test-strategist` review is recorded in the Reviewer findings; this list incorporates it):
- **pytest:** full suite via `/verify-suite`, because `app.py`, `tests/conftest.py` and `app_launcher.py` fall back to it (`QUALITY_GATE.md:132`). Targeted per commit: the two new files, the six edited test files, and the fixture consumers named in TS's *Required gates*.
- **e2e:** full Chromium via `/verify-suite`, judged against the S1(d) baseline. Watch `erase-flow`, `program-backup`, `fatigue`, `smoke-navigation` and `summary-pages`.
- **other:** packaged smoke (RP-3); pyright baseline diff (covers `tests/`); vulture; flake8; inventory regeneration plus `--check`; the `.ps1` run (A10).

### V13. Validation plan

All of this runs in the standalone clone with private paths (IC-1/IC-2); every evidence record names the paths.

1. **Per-commit targeted pytest** (`/run-tests <file>`) at C2–C4.
2. **Full pytest:**
   - Serial (the CI form: `ci.yml` `pytest-core` runs serially with `--cov`, `:830-835`) and locally `-n 8 --dist loadfile`. The parallel run is local evidence only [TS-13].
   - Then `/verify-suite`.
   - Pass condition: **no new failure against the S1(c) pytest baseline and the S1(d) Chromium baseline**, with the same seed settings [TS-4].
   - `e2e/program-backup.spec.ts:79` is the known historical flake (`QUALITY_GATE.md` *Known exceptions*, `:243-246`). Any red there, or any other red that also appears in the baseline, must be **rerun in isolation** before being classed as known. **Never use `--update-snapshots`.**
   - If a failure's origin is still unclear, reproduce it in an isolated base checkout.
3. **Packaged-Windows smoke:** bootloader observed green in CI (RP-3; needs RP-6). Payload mode runs locally after a PyInstaller build in the private venv. Payload evidence never stands in for bootloader evidence (`smoke_packaged_app.py:9-15`).
4. **Fresh-process import checks:** the AC1 subprocess tests, plus a manual `python -c "import app"` and `python -c "from app import STATIC_LONG_MAX_AGE_SECONDS"` with an empty scratch `HT_RUNTIME_DIR`, recording the directory listing before and after.
5. **Initialization-order checks:** the AC2 mock test. At runtime, `<scratch>/logs/app.log` shows the migration and seed lines followed by exactly one "Runtime initialized" line per serving process.
6. **First install:** the AC5d test. Manually, `python app.py` on an empty `HT_RUNTIME_DIR` must show `seeded=True`, 1,897 exercises and no `auto_backup/`.
7. **Existing-DB upgrade:** automated by `test_init_runtime_upgrades_old_schema_database` [TS-8]. Manually, `python app.py` against a `make_old_schema_db.py` database with a free `HT_PORT` must give `GET /` 200, `catalog_version` populated and one snapshot. A restart gives a second snapshot.
8. **Legacy migration:** `check_upgrade_migration` in bootloader (CI) and payload (local) mode. A source checkout resolves `same-path`.
9. **Backup/restore:** automated by `tests/test_program_backup.py`, `tests/test_auto_backup.py` and E2E `program-backup.spec.ts`/`erase-flow.spec.ts`. Manual smoke via the `run-hypertrophy-toolbox` skill on a scratch runtime: create a program backup, change the plan, restore, confirm; then erase via the UI and confirm the banner names a snapshot file that exists in `<db dir>/auto_backup/`.
10. **Repeated initialization at runtime:** `FLASK_USE_RELOADER=1 python app.py` on a scratch runtime with an existing database. Expect 0 "Runtime initialized" lines from the parent, 1 from the serving child, and 1 snapshot for that start. Confirm the parent opened no database: no database file is created at the resolved path on a first-install run that is stopped before the child seeds [AR-1].
11. **pyright:** `scripts/pyright_baseline_diff.py` reports no net-new diagnostics.
12. **vulture** (`pyproject.toml`, `min_confidence 100`) and **flake8** (blocking F401/F811/E711/E712, `app.py:2-7`) are clean.
13. **Test Inventory Drift:** regenerate, then `--check` clean, in a clone with no untracked or gitignored `.md` in a globbed surface directory (RP-5).
14. **Workflow contracts:** `tests/test_agent_workflow_contracts.py`, plus every test naming an edited doc path, found with `rg -l "CLAUDE.md|rules/(routes|testing|database|debugging)|AUTONOMY.md|PARALLEL_WORKFLOW|DUPLICATION_REGISTRY|E2E_TESTING|product/README" tests`. No file under `.claude/**` or `docs/ai_workflow/**` is added or deleted.
15. **Launch paths:** `python app.py` (Playwright webServer, items 6–7, 9–10); `flask run` via `python -m flask --app app:create_initialized_app run --no-reload --port <free>` with scratch `DB_FILE`/`HT_RUNTIME_DIR` (A8a); the `.ps1` (A10); the bootloader (item 3).
16. **AC13 documentation greps** return nothing in the F9 files:
    - `rg -n "register(ed)? in (\*\*)?both" CLAUDE.md .claude routes/CLAUDE.md tests/CLAUDE.md utils/CLAUDE.md docs/ai_workflow`
    - `rg -n "flask run --reload" app.py`
    - `rg -n "Slow request detected|log_request_info|start_timer" --glob "!docs/archive/**"`
    
    A reviewer also reads each F9 and R-4 line against the new behavior.
17. **URL-map evidence:** the S1(a) capture equals the post-C3 capture (D-16). A non-empty diff is a WS3 defect.
18. **A8b measurement before Gate 2** (§V16).

### V14. Independent implementation reviewers

| Manifest path(s) | `QUALITY_GATE.md` row (`f3adacf1`) | Reviewer required |
|---|---|---|
| `app.py` | Route / API (`:46`) | `code-reviewer`; `product-risk-reviewer` only "if response shape changes", and production shapes do not change (C-11 is test-only) |
| `utils/runtime_init.py`, `utils/logger.py` | Business logic (`:48`) | `code-reviewer` |
| `tests/**`, `app_launcher.py`, `.vscode/launch.json` | Targeted-test fallback (`:132`); no reviewer row | none added |
| `e2e/run_puppeteer_summary_regression.ps1` | E2E spec (`:53`) | none |
| `CLAUDE.md`, `*/CLAUDE.md`, `.claude/**`, `docs/ai_workflow/**` | AI workflow (`:56`) | `code-reviewer` or careful self-review (here `code-reviewer`) |
| `docs/product/README.md`, `docs/DUPLICATION_REGISTRY.md`, `docs/E2E_TESTING.md`, `docs/test_inventory/*` | Product docs (`:57`) | none |
| DB-row files | DB / schema (`:47`) | **Not tripped.** The manual backup/restore smoke still runs because AGREED §4 WS3 *Acceptance* requires it. |

Reviewers that run:
- **Required:** `code-reviewer` (table union), and `unslop-reviewer`, because `/verify-and-polish` includes it at `f3adacf1` (`:156`).
- **Required by direction:** `architecture-reviewer` (AGREED §4 WS3 *Gates*).
- **Owner decision at Gate 1 (PR-2):** `product-risk-reviewer`. The product-risk reviewer says it should be required; the test-strategist and Plan v1 derive it as optional. **Recommendation: include it**, because startup, auto-backup and erase are refactor-invariant workflows.

Diff-time reviewers are independent of `senior-developer` and `automation-qa`. A reviewer that does not run is incomplete, never "no findings", and does not satisfy a Required-reviewers cell (`QUALITY_GATE.md:38-40`).

### V15. Design decisions

| ID | Decision | Rationale |
|---|---|---|
| D-1 | Filter, hook, context-processor and view functions are module-level and registered by `create_app()`; `apply_static_cache_policy` reads `current_app.config` | One function object per hook across instances; identity assertable; names unchanged; `frozen_cache_client` still works |
| D-2 | The `__main__` body becomes `main()` plus `_register_shutdown_cleanup()` [TS-3] | AC7 is testable without a server and without installing process-global hooks |
| D-3 | The reloader rule is `should_initialize_runtime(use_reloader)` | One tested predicate |
| D-4 | The seeded carry-over is keyed by the resolved database path | Seeding is a property of the file; a failed migration can switch files |
| D-5 | Guard key = (resolved requested path or `None`, `runtime_root()`) | Equivalent requests stay no-ops |
| D-6 | `init_runtime(db_file="")` raises `ValueError` | `""` would silently fall back to the resolver (`runtime_migration.py:241`) |
| D-7 | A lock makes check-run-set atomic | Cheap; prevents a double run |
| D-8 | `RuntimeInitOutcome` has exactly AC2's five fields; a no-op returns the cached outcome with `already_initialized=True` | Minimal surface; the failure reason is already logged |
| D-9 | One INFO line per real initialization | Observable "exactly once" oracle |
| D-10 | `create_initialized_app()` takes no arguments and always initializes. Under `flask run --reload` the parent also initializes, in its own process, as today [TS-13/PR-4] | The CLI calls factories with no arguments. The guard is per-process, so it cannot raise across parent and child. The supported callers use `--no-reload`. |
| D-11 | The launcher imports `init_runtime` lazily inside `main()` | Keeps `require_supported_python()` first (`app_launcher.py:12,53`) |
| D-12 | The conftest `app` fixture imports `create_app` lazily | No `app` import at collection |
| D-13 | `real_app_client` keeps the env settings, resets before init and in teardown, and drops `app_context()` | Belt-and-braces isolation; no leaked guard key |
| D-14 | AC2's "single assignment" is checked by observation | A module attribute cannot count its own assignments without a production seam |
| D-15 | `requestId` tests check against the `X-Request-ID` header and its shape | Tighter than `None` |
| D-16 | "Same URL rules as today" is a one-off S1/post-C3 diff; the permanent tests are structural, plus `EXPECTED_BLUEPRINTS` as the one deliberate test-oracle site [TS-10] | A committed URL-map fixture would recreate dual maintenance |
| D-17 | `_INITIALIZATION_COMPLETE` is untouched | Not needed; would trip the DB row |
| D-18 | In `main()`, cleanup and signal registration follow `init_runtime()` and share its reloader condition [AR-1] | Preserves today's order in the serving process. The reloader parent, which never initialized, opens no database on exit. |
| D-19 | The `flask run` repairs share commit C3; one PR | Avoids serving an uninitialized runtime in between |
| D-20 | `setup_logging()` loses `app`; the signature test replaces `TestFlaskIntegration` | The parameter would be dead |
| D-21 | AC1 probes run with `TESTING` removed and count DB access primitives [AR-2] | Production mode is where import-time startup would write |
| D-22 | Tests first (S2), harness migration after the factory (S5) | `AUTONOMY.md` *Workflow roles*; keeps C4+ green |
| D-23 | `static` is exempt from the non-strict assertion; no production per-rule edit [TS-2] | Flask binds that rule in `Flask.__init__`, as today; behavior is asserted instead |
| D-24 | Logging tests prime `get_logger()` and compare before/after [TS-6]; A8e runs in a subprocess [TS-7] | Order-independent under `-n 8 --dist loadfile`; pytest's root handlers mask Flask's default handler |
| D-25 | The uninitialized-runtime risk (PR-1) is mitigated by documentation, unless the owner chooses the guard | A `before_request` guard contradicts AC4, fires under the unseeded test `app`, and covers developer-only paths once both callers are repaired |

### V16. Assumption verification (A1–A13; A8 split into six)

| ID | Verification: what is run, where, when | Pass condition | If refuted |
|---|---|---|---|
| A1 | AC1 subprocess probes (green from C3); §V13 item 4 | One Flask construction; 0 `DatabaseHandler`/`connect`; only `logs/` created | Remove the import-time side effect; if impossible, stop and return to the owner |
| A2 | AST + fresh-interpreter boundary tests [TS-9]; packaged smoke (A12) | No `app`/`routes` loaded; smoke green | Stop; owner chooses another boundary |
| A3 (reworded) [TS-1] | S5: `automation-qa` reads each of the five token sites and their docstrings, adds the token, and changes **only** `tests/test_program_backup.py:843`, as R-3 lists. Every other following assertion stays unchanged. | Intent is "erase then reinitialize"; the sites pass with the token alone, except `:843`, which is tightened to `data['data'] == {"auto_backup": None}` | A site whose intent is "an empty body is accepted" conflicts with AC8: stop and escalate. Any further assertion change is listed in the PR with its reason, never weakened. |
| A4 | AC1 patched-attribute case, AC5c, AC3e. Mutations in a scratch copy, never committed: read `utils.config.DB_FILE` as input → AC5c red; remove the `TESTING` refusal → AC3e red. | Both mutations red; both reverts green | Strengthen the tests; re-review with `test-strategist` |
| A5 | AC1 `test_constant_import_creates_no_data`; packaged smoke | No `data/` or database from the constant import | WS3 defect; fix before merge |
| A6 | S1 grep `rg -n "log_request_info|log_response_info|start_time|Slow request detected" --glob "!docs/archive/**"` | Hits only in deleted code, `debugging.md:29-31` (corrected) and this plan | Stop; the owner revisits Q-WS3-2H |
| A7 | **Automated:** `test_init_runtime_upgrades_old_schema_database` (PR-time) [TS-8], AC5d first install, packaged smoke in both modes. **Optional additional:** owner-authorized `deep-gate.yml` dispatch (RP-7) or the local equivalents (§V13 items 6–7). | All green | A branch-only failure is a WS3 defect. WS3 adds no CI job. |
| A8a (revised) [AR-3] | In the clone, with **scratch `DB_FILE` and `HT_RUNTIME_DIR`**: `python -m flask --app app:create_initialized_app routes` | Exit 0; `/erase-data` listed; the scratch database is created (expected: every subcommand initializes); exactly one "Runtime initialized" line | Switch the callers to `app:create_initialized_app()` and retest. If that also fails, return to the owner (alternative: a `flask init-runtime` CLI). |
| A8b (revised) [TS-13, PR-4] | **Before Gate 2**, in the clone with scratch paths and an existing database: `python -m flask --app app:create_initialized_app run --reload --port <free>` for about 10 s. Count "Runtime initialized" lines and new snapshots; read the console for `RuntimeError`. | Expected per §V7: 2 lines (parent + child), no `RuntimeError`, 2 snapshots (same as today). Recorded in the PR. | If any `RuntimeError` appears, that is a WS3 defect, fixed before Gate 2. If 1 line, record it; no design change is needed. |
| A8c (revised) [TS-2] | `test_blueprint_rules_are_non_strict_static_excepted`, `test_trailing_slash_get_on_blueprint_rules_is_served`, `tests/test_trailing_slash_routing.py` | Blueprint rules non-strict; `static` strict, as today; trailing-slash GETs 200 with no redirect | Keep `strict_slashes` set before blueprint registration. **No per-rule production edit.** If a blueprint rule is strict, the defect is ordering inside `create_app()`; fix it there. |
| A8d | `test_handler_layering_behaves_as_documented` (raising route under `TESTING=True`) | 500 `INTERNAL_ERROR` response; no exception raised in the test | Correct C-11 and re-triage A11 |
| A8e (revised) [TS-7] | **Subprocess** probe: `python -c "import app, flask.logging; …"` prints whether `flask.logging.default_handler in app.app.logger.handlers` and whether any `hypertrophy_toolbox` handler is aliased | Recorded as measured; expected: default handler present, no aliasing | No WS3 behavior change either way (F5); record the state |
| A8f | Subprocess `python -c "import app; print(app.app.debug)"` with `FLASK_DEBUG` unset and `=1` | Recorded | Informational only (3a deleted the listing) |
| A9 | AC3e plus the A4 mutation; `real_app_client` always passes an explicit path | Refusal enforced; mutation caught | Strengthen AC3e before merge |
| A10 | Run `e2e/run_puppeteer_summary_regression.ps1` in the clone | Exit 0 | If `npx`/MCP is unavailable, run steps 1–2 by hand (seed, `flask run` with the new `FLASK_APP`, `GET /weekly_summary` 200) and record why step 3 could not run |
| A11 (revised) [TS-1] | **Refuted in part by grep:** a sixth outcome change exists (`tests/test_program_backup.py:843`) and is now listed (R-3). Before S5, `automation-qa` greps for `pytest.raises` around requests, `requestId`, 404/405 body checks, `data.get('data')`/`['data']` after `/erase-data`, `caplog` absence checks and `app.name`. After S5, run full pytest serially and with `-n 8 --dist loadfile`. | Only the R-3-amended AC6 list changes | For each new failure: twin-only reliance → update, listed with its reason, never weakened; production defect → stop and fix; unclear → escalate |
| A12 | Packaged smoke bootloader (CI) and payload (local) | Green | Adding `hiddenimports` is out of scope; return to the owner |
| A13 | None needed under Q-WS3-2(a); full pytest covers `test_fatigue.py` | Green | Moot unless the owner later selects (b) |

### V17. Implementation-readiness preconditions (carried to Gate 1)

- **IC-1 … IC-8** (Section 0, ED-1 isolation conditions): unchanged and all unchecked. The implementation manager verifies and records them at S0.
- **RP-1 … RP-5** (Section 0): unchanged.
- **RP-6 (proposed):** push the implementation branch and open a PR, without merging, so the non-required packaged bootloader smoke can be observed (RP-3).
- **RP-7 (proposed):** an owner-authorized `workflow_dispatch` of `deep-gate.yml` on the branch, as additional evidence. Since TS-8 the PR-time old-schema test is the primary automated upgrade evidence; RP-7 is no longer the only option.

### V18. Gate 1 — exactly what the owner must approve

1. **Plan v2** as written, including AC refinements R-1…R-5 (§V1) and the response-matrix dispositions.
2. **RP-4:** the explicit approval to move all 13 `register_blueprint` calls into `create_app()` (`AUTONOMY.md:18,144`).
3. **RP-6 (proposed):** authority to push the implementation branch and open a PR, **without merging**, to observe the packaged bootloader smoke. A merge needs a separate confirmation naming the PR.
4. **RP-7 (proposed):** whether to dispatch `deep-gate.yml` on the branch as additional evidence (yes / no).
5. **PR-1 mitigation choice:**
   - (a) **documentation-only** (recommended; C-3 symptom note plus the repaired callers); or
   - (b) an uninitialized-runtime `before_request` guard. This would require amending AC4's hook list, and it would need a carve-out for the unseeded test `app`.
6. **PR-2 reviewer choice:** add `product-risk-reviewer` as a diff-time reviewer (**recommended: include**) or keep it optional/omitted. This is a reviewer disagreement and is recorded in the matrix.
7. **Implementation-readiness preconditions** acknowledged: IC-1…IC-8 and RP-1…RP-5 must be verified at S0 before any implementation. Gate 1 does not satisfy them by itself.

**Re-review.** No reviewer finding was blocking, and every finding is accepted or sent to an owner decision. No reviewer was re-run (`.claude/commands/council-plan.md:76-77` at `f3adacf1`, *Failure handling*, re-runs a reviewer after a "blocking" result). **The owner may request a re-review of Plan v2** by any or all of the three reviewers before signing Gate 1. This plan does not sign Gate 1 and authorizes no implementation.

### V19. Gate 1 — delegated decision record (2026-10-20)

*Added in rev 5 by a fresh `product-manager`. Sources, each read directly: the manager's synthesis `artifacts/ws3-impl-20261020/gate1-team/DELEGATED_GATE1_DISPOSITION.md` (the source of truth for what is adopted), the three adviser reports in the same folder, and the owner request `artifacts/ws3-impl-20261020/owner-request-impl-20261020.md`. Everything under `artifacts/` is gitignored and not in the repository. §V1–§V18 above are kept verbatim. Where an amendment below names Plan v2 text, the amendment takes precedence for implementation.*

**What kind of decision this is.** This is a **delegated AI-team decision, adopted under the owner's direct instruction. It is not the owner's personal Gate 1 signature.** Gate 2 (owner review of the finished diff and evidence) and any merge confirmation remain owner-only.

**Authority** (owner, 2026-10-20, verbatim):

> "I delegate the remaining V18 choices and Gate 1 disposition to an AI consulting team within the existing WS3 requirements. Spawn independent architecture, test-strategy and product-risk advisers. They must read the actual Plan v2 and existing reports, reuse sufficient evidence, resolve outstanding choices and return reasoned recommendations. Record the adopted delegated decision, real IDs and dissent; never represent it as my personal signature."
>
> "After a favorable delegated Gate 1 decision and verified implementation-readiness conditions, I authorize implementation, required verification, commits, push and a ready PR. This includes moving the 13 blueprint registrations into create_app(). Stop before merge. Optional remote Deep Gate dispatch requires separately established authority; use the plan's primary automated evidence first."

**Adopting session:** Claude Code manager session `hypertrophy-toolbox-v3-main-53` (session id `8baa0d6f-a419-4e4e-b812-5a1e73da9a8b`), working in the clone `D:\development\Hypertrophy-Toolbox-v3-ws3-app-factory-20261020` at `origin/main` `71c4cc6d`.

**Advisers.** All three were independent and read-only, spawned in parallel, and none saw another's report.

| Role | Agent ID | Verdict | Report |
|---|---|---|---|
| `architecture-reviewer` | `a1eeea22faba20495` | FAVORABLE WITH CONDITIONS | `artifacts/ws3-impl-20261020/gate1-team/architecture-a1eeea22faba20495.md` |
| `test-strategist` | `a582e93753711c30d` | FAVORABLE WITH CONDITIONS | `artifacts/ws3-impl-20261020/gate1-team/test-strategist-a582e93753711c30d.md` |
| `product-risk-reviewer` | `a7be2f933a6121799` | FAVORABLE WITH CONDITIONS | `artifacts/ws3-impl-20261020/gate1-team/product-risk-a7be2f933a6121799.md` |

The prior council was **reused, not re-run**: architecture `a484bd1ac77e7e978`, test-strategist `af3d581707e375d82`, product-risk `a12256eb7f65a549a`; Plan v1/v2 `product-manager` `a9259355287e3c511`.

**Base note.** The implementation base is `origin/main` `71c4cc6d`. `git diff --stat f3adacf1 71c4cc6d` over every §V2 path and the DB-row/runtime-step files changes only `docs/test_inventory/TEST_INVENTORY.{json,md}` (manager measurement, owner-request file). The `path:line` citations that all three advisers spot-checked still hold.

#### §V18 dispositions

| # | Item | Disposition | Decided by |
|---|---|---|---|
| 1 | Plan v2, including R-1…R-5 and the 22 matrix dispositions | **Approved (delegated), with amendments GA-1…GA-14 below.** No adviser found a blocking design defect. | Delegated team (all three advisers) |
| 2 | RP-4 — move all 13 `register_blueprint` calls into `create_app()` | **Approved by the owner directly** ("This includes moving the 13 blueprint registrations into create_app()"). | **Owner-direct; not a team decision** |
| 3 | RP-6 — push and PR, no merge | **Authorized by the owner directly** ("commits, push and a ready PR … Stop before merge"). The PR is ready, not draft. A merge needs a separate owner confirmation naming the PR. | **Owner-direct; not a team decision** |
| 4 | RP-7 — `deep-gate.yml` dispatch | **Not adopted.** No separately established authority exists. The primary automated evidence is sufficient: the PR-time old-schema upgrade test, the first-install test, the PR-CI bootloader smoke and the Playwright `python app.py` webServer. The limitation is recorded in GA-10. | Owner text; test-strategist item 2 |
| 5 | PR-1 — stale `FLASK_APP=app.py` / `app:app` | **Option (c): documentation, caller repair, a repository-wide stale-caller tripwire test, a measured symptom and an `app.py` comment. No request hook.** Option (b) was rejected unanimously: it contradicts AC4's hook list, fires under the unseeded test `app`, and would couple `create_app()` to runtime state. Specified in GA-1…GA-4. | Delegated team (all three) |
| 6 | PR-2 — diff-time `product-risk-reviewer` | **Include:** one bounded, read-only pass on the final head after S7. This is an optional addition authorized by the owner's delegation. It substitutes for no Required-reviewers cell. A failed run is incomplete and is rerun once. | Delegated team (all three; the test-strategist reverses its predecessor's "optional") |
| 7 | Implementation-readiness preconditions | Acknowledged; status in GA-13. RP-1 is satisfied in substance, **not in letter** (GA-13). | Delegated team (architecture item 4) |

#### Amendments GA-1…GA-14 (binding for implementation; they take precedence over the Plan v2 text they name)

- **GA-1 — PR-1 tripwire (amends the AC11 row of §V12 and `tests/test_app_factory.py` in §V2).** `test_flask_run_callers_use_the_factory` scans every tracked file (`git ls-files`, run from the repo root; a failure to run git is a test failure, not a skip). It excludes `docs/archive/**`, `docs/app_factory/**` and the test module itself. It fails on any assigned `FLASK_APP` value, any `--app` value and any `flask … run` target other than `app:create_initialized_app`, and on `flask run --reload` anywhere in `app.py`. Save/restore lines that assign a variable rather than a literal target (`e2e/run_puppeteer_summary_regression.ps1:27,61`) are not violations. Manager measurement at `71c4cc6d` (`git grep -E "FLASK_APP|flask run|--app[ =]|flask --app"`, minus the two excluded trees) found only `.vscode/launch.json:6,23`, `app.py:306` and `e2e/run_puppeteer_summary_regression.ps1:27,29,61`, all repaired or benign. Dissent: see below.
- **GA-2 — PR-1 comment (amends §V5).** A short comment above the module-level `app = create_app()`: do not point `FLASK_APP` at this object; it is uninitialized; use `app:create_initialized_app`.
- **GA-3 — PR-1 measurement (new A8g; amends C-3).** At S8, on a scratch `HT_RUNTIME_DIR` with no database, run `python -m flask --app app:app run --no-reload --port <free>`, then `GET /` and two data pages. Record the status codes, whether the database file was created and its size, and whether a later `python app.py` on the same runtime re-seeds. The measured result replaces C-3's symptom wording ("empty app"). C-3 also states:
  - a stale caller on an existing database gets no schema initializers, catalog upgrade or startup snapshot;
  - the hazard is reachable only through a developer-run Flask CLI or WSGI server; START.bat, RUN_APP.bat and the packaged exe initialize explicitly;
  - recovery: stop the app, confirm the file has 0 exercises, delete it plus its `-wal`/`-shm` sidecars, restart.
- **GA-4 — PR-1 documentation (amends D-25).** The recovery sentence goes into `.claude/rules/debugging.md` and `docs/product/README.md` (both already in §V2). CLAUDE.md stays under 200 lines. The PR states the residual risk: an ad-hoc developer shell with a stale `FLASK_APP` is unprotected; the impact is limited to a missing or empty runtime database, and it is recoverable. D-25 now reads: "mitigated by documentation, caller repair, the GA-1 tripwire and the GA-2 comment; no request hook".
- **GA-5 — launcher console order (amends §V4 row 2 and §V8).** In `app_launcher.main()`, `init_runtime()` runs before the "Application loaded successfully!" print, so a failed initialization never prints success. Console text and the error-wait UX are otherwise unchanged (C-13).
- **GA-6 — migration notes (amends §V10).** The PR migration notes carry C-1…C-13, plus:
  - C-3 as rewritten by GA-3;
  - **C-4 addition** — first install under the reloader: today the parent seeds, then the child runs the upgrade and snapshots the fresh seed; after WS3 only the child seeds, and it takes no snapshot;
  - **C-5 widened** — the `TESTING=1` refusal applies to every initializing entry point (START.bat, the exe/RUN_APP.bat launcher, `flask` commands, `python app.py`). A stray `TESTING=1` that used to start the app now fails at startup with the "unset TESTING" message (shown in the launcher's error-wait window);
  - a note that `create_initialized_app` is a third `init_runtime` caller beside the two launch paths. Q-WS3-5 settled this; AGREED_PLAN §4 WS3 *Shape* said "only the two launch paths".
- **GA-7 — test refinements (amends §V12).**
  - `test_only_request_id_and_cache_policy_hooks` asserts the **order** of `after_request_funcs[None]`, not only membership.
  - `test_app_fixture_is_the_factory_app` also asserts that `app.root_path` is the repo root.
  - Subprocess probes build their env from `dict(os.environ)` minus `TESTING`/`DB_FILE`/`HT_*`, keep `SYSTEMROOT`/`TEMP`/`TMP`, and use `timeout=300` and `cwd=tmp_path` (the shape of `tests/test_real_app_db_isolation.py:92-102`).
  - No pytest test binds a port. Scratch trees stay flat.
  - AC1's clone-`data/` before/after comparison covers only paths the probe could create (`database.db*`, `auto_backup/`).
  - The A8b oracle is the "Runtime initialized" line count; the snapshot count is secondary (snapshot names have second resolution, `utils/auto_backup.py:70`).
  - The old-schema test's "exactly one snapshot" depends on the upgrade reaching at least 100 exercises (`utils/auto_backup.py:16,59`). If it is red, read the auto-backup log lines before changing anything.
  - The A4/A9 mutation runs are recorded: red, then green after revert.
  - The pyright baseline diff runs at C2, C3 and C4 as well as S7.
- **GA-8 — boundary wording (amends §V3 and §V6).** The AST and fresh-interpreter tests assert only that `app`, `app_launcher` and `routes`/`routes.*` are absent. `flask` may be present transitively (`utils/logger.py` imports Flask). §V6 notes that the docstring of `prepare_runtime_database` says "Never raises" (`utils/runtime_migration.py:233`), while AR-4 relies on `copy_legacy_backups()` exceptions propagating. WS3 does not edit that file.
- **GA-9 — baselines (amends §V9 S1 and §V13 item 2).**
  - S1(c): full pytest at unmodified `71c4cc6d`, both serial (the CI form) and `-n 8 --dist loadfile`.
  - S1(d): Chromium `npx playwright test --project=chromium --reporter=line` with a private `PW_PORT` and `PW_DB_PATH`, and `PW_VISUAL_SEED`/`PW_REUSE_SERVER`/`PW_BASE_URL`/`PW_WORKERS` unset; run separately from pytest.
  - "No new red" means the post-change failing node-ID set is a subset of the baseline set, and the collected count equals the baseline plus the WS3 additions. Each new red is rerun once in isolation. `e2e/program-backup.spec.ts:79` counts as "known" only after a recorded isolated pass.
  - Never `--update-snapshots`. Only the R-3 assertion changes are allowed, each listed.
- **GA-10 — packaged evidence and the RP-7 limitation (amends §V13 item 3 and §V16 A7).**
  - Before the PR is marked ready: the local payload smoke (`scripts/stage_package_assets.py`, `pyinstaller --clean --noconfirm Hypertrophy-Toolbox.spec`, `scripts/smoke_packaged_app.py --mode payload …`) is green in the private venv.
  - After push: "Packaged Smoke (Windows bootloader, non-required) / Build and smoke" must be green at the exact PR head. A red is a WS3 defect (A12).
  - Observe `visual-windows`, `e2e-erase-flow`, `e2e-backup` and `e2e-functional`.
  - Limitation: `deep-gate.yml` (three `python app.py` jobs) and `release.yml` are not run. This is mitigated by §V13 items 6, 7 and 10, and the evidence is valid only at the exact head.
- **GA-11 — inventory and landing (amends §V9 S7).** Regenerate `docs/test_inventory/*` last, after the final rebase onto fetched `origin/main`, and again if main moves before push. `--check` must exit 0. Never hand-merge; on conflict, take `origin/main` and regenerate. Agreed with the CI/CD B3 lane (session `hypertrophy-toolbox-v3-main-68`): whichever PR merges second regenerates.
- **GA-12 — the plan file (new S0 step).** `docs/app_factory/PLANNING.md` is committed in the PR as commit C0, carrying this Gate 1 record. `docs/ai_workflow/INDEX.md` (docs-cleanup claim) and `docs/MASTER_HANDOVER.md` (shared) are not edited; the pointer is reported to the owner instead. Owner handoff note: the shared checkout holds this file untracked, which will block a `git pull` there until it is moved aside. Evidence cited under `artifacts/` is gitignored and not in the repository.
- **GA-13 — readiness (amends §V17).**
  - IC-1, IC-2 and IC-3 are satisfied: the clone was made by `git clone --no-hardlinks <GitHub URL>`, has no `objects/info/alternates`, and its `.git` is a directory; the private venv and `node_modules` are real directories; TEMP is 74 characters and created.
  - IC-4/RP-2 are verified per hunk at S6: re-fetch, re-read the claims, take a read-only look at the shared checkout's overlapping hunks; the second lander rebases.
  - IC-5/IC-6 were satisfied at 17:43Z and are **re-checked before the first post-Gate-1 test run and before push**.
  - IC-7/IC-8 hold by construction. At the end, the shared checkout's `git status --porcelain` is shown unchanged from the session-start snapshot.
  - RP-1: the manager session was launched from the shared checkout directory, so RP-1 is met in substance (isolated storage, dependencies, runtime and caches) but not in letter. Controls:
    1. every shell command sources `artifacts/ws3-impl-20261020/env.sh` (which `cd`s into the clone) and uses absolute paths or `git -C <clone>`;
    2. subagent prompts carry absolute clone paths and forbid reading or writing under `D:\development\Hypertrophy-Toolbox-v3-main`, except a read-only RP-2 look;
    3. the clone's `CLAUDE.md`, `.claude/**` and charters are authoritative for edits and review, not the shared checkout's dirty copies (note: hooks still execute from the shared checkout's `.claude/hooks`);
    4. the end-of-session shared-checkout status proof;
    5. the manager does not edit `MEMORY.md`.
  - RP-3 is checked after push. RP-4 and RP-6 are owner-direct. RP-5 holds once PLANNING.md is committed. RP-7 is not granted.
- **GA-14 — follow-up outside WS3.** The comment at `.github/workflows/ci.yml:919-924` cites the dead `tests/test_pattern_coverage.py` fixture that WS3 deletes. This is recorded as a follow-up for the CI/CD B3 lane. WS3 makes no `.github/**` edit.

**Adviser conditions already carried by Plan v2.** The product-risk adviser's B3 (the manual backup/restore/erase smoke, with the banner naming an on-disk snapshot, and the A8b measurement, both recorded in the PR before Gate 2) is §V13 items 9 and 18 and §V9 S8. It needs no amendment.

#### Dissent and minority positions

- **Stale-caller scan scope:** the test-strategist preferred a fixed caller list and the product-risk adviser a listed surface set. The architecture adviser's whole-tree form was adopted because it is the superset of both.
- **PR-2:** the prior council's test-strategist `af3d581707e375d82` and Plan v1 treated the `product-risk-reviewer` as optional. All three current advisers say include.
- **C-4:** the architecture adviser anticipated that C-4 (2 → 1 reloader snapshots) might be called an owner choice. No adviser asked for that, so it stays a migration note.
- **PR-1 alternative:** the product-risk adviser noted the owner may still choose a module-level-only guard instead of (c). No adviser recommends it.

#### What this does NOT do

It is not an owner Gate 1 signature, not Gate 2, and not a merge confirmation. It does not widen any AC beyond R-1…R-5 and GA-1…GA-14. All of those strengthen or document; none weakens an assertion.

---

## Sign-off

- [x] Gate 0 complete when required by planning size (owner, 2026-10-20; record in Section 0).
- [x] Every finding has a disposition (22 rows). The owner confirms them at Gate 1; PR-1 and PR-2 need an owner choice (§V18 items 5–6).
- [x] Agent provenance complete: both `product-manager` IDs, same-PM-resumed yes/no, the three reviewer IDs, and an evidence-gap line.
- [x] Plan v2 approved (Gate 1) **by delegated AI-team decision (§V19), not by owner signature**, 2026-10-20. The §V18 decision list is disposed in §V19; RP-4 and RP-6 were decided by the owner directly.
- [x] Ready to implement. Implementation is authorized by the owner's 2026-10-20 instruction, conditional on the favorable delegated decision and S0 readiness (§V19 GA-13).
- [ ] Gate 2 (owner review of the finished diff and evidence) — owner only; not given.
