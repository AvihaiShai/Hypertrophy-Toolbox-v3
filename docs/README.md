# Hypertrophy Toolbox v3 Documentation

This directory holds current references, open work, and retained completion history. Use the categories below to distinguish their roles.

## Active Docs

### Product Reference

The [`product/`](product/) suite describes the shipped application — behavior, schema, and design.
It is descriptive and carries no task status; current public tracking is in GitHub, with runtime handover context in `MASTER_HANDOVER.md`.

- **[product/README.md](product/README.md)** - Suite index, canonical-source map, conflict rules, terminology, and how work gets planned
- **[product/APP_FLOW.md](product/APP_FLOW.md)** - Every screen: purpose, controls, action types, and success / no-result / failure outcomes
- **[product/BACKEND_SCHEMA.md](product/BACKEND_SCHEMA.md)** - Every table, column, constraint, index, and relationship, with an ER diagram
- **[product/DESIGN_BRIEF.md](product/DESIGN_BRIEF.md)** - The shipped design system: tokens with measured consumers, theming, typography, motion, accessibility

### Project State
- **[docs_cutover/README.md](docs_cutover/README.md)** - Documentation cutover rules, completion criteria and the owner-reviewed pilot boundary
- **[GitHub Project board](https://github.com/users/AvihaiShai/projects/5/views/2)** - Current public work, organized by canonical workstream parents; issues own status, decisions and completion evidence
- **[MASTER_HANDOVER.md](MASTER_HANDOVER.md)** - Runtime handover and operating context; the file new agents read first
- **[ACTIVE_DEVELOPMENT.md](ACTIVE_DEVELOPMENT.md)** - Fatigue calibration guardrails and agent authority rules; earlier objectives and status blocks archived
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and recent work
- **[DECISIONS.md](DECISIONS.md)** - Durable project decisions and lightweight ADRs
- **[CLAUDE_MD_AUDIT.md](CLAUDE_MD_AUDIT.md)** - Architecture-debt audit snapshot; check its "Last validated" date and re-verify a finding before relying on it
- **[LEFTOVERS_BY_PRIORITY.md](LEFTOVERS_BY_PRIORITY.md)** - Historical prioritization and retained evidence; current public tracking is in GitHub
- **[OPEN_WORK_EXECUTION_PLAN.md](OPEN_WORK_EXECUTION_PLAN.md)** - Retained sequencing, decision gates and closed/parked boundaries, with links to current GitHub tracking
- **[ai_workflow/INDEX.md](ai_workflow/INDEX.md)** - AI workflow navigation spine
- **[ai_workflow/DOC_RETENTION.md](ai_workflow/DOC_RETENTION.md)** - Rules for keeping, archiving, retiring, or deleting docs

Documentation cutover is tracked in [#595](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/595),
with index/status corrections in [#577](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/577)
and operating-guidance reconciliation in [#580](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/580).
Source contracts, approval boundaries and evidence remain in the retained documents; issue publication does not replace or retire a document by itself.

### Runtime, UI, And Testing
- **[CSS_OWNERSHIP_MAP.md](CSS_OWNERSHIP_MAP.md)** - Current CSS loading and ownership map
- **[E2E_TESTING.md](E2E_TESTING.md)** - How to run Playwright, and what each spec covers. For counts see **[test_inventory/TEST_INVENTORY.md](test_inventory/TEST_INVENTORY.md)**, the generated single producer
- **[UI_SCENARIOS_GAP_ANALYSIS.md](UI_SCENARIOS_GAP_ANALYSIS.md)** - UI risk status, deferred quality items, and Known Issues table (KI-001..)

### Feature Docs
- **[muscle_selector.md](muscle_selector.md)** - Muscle selector component notes
- **[muscle_selector_vendor.md](muscle_selector_vendor.md)** - Vendor SVG attribution

## Feature folders

Active includes current references, deferred work, and records awaiting reconciliation.
Closed describes execution status; current contracts and evidence in those folders stay in place.
Proposed entries do not authorize implementation. The archive container is indexed separately below.

### Active

- [agent_roles/](agent_roles/) — role rollout; Phase 6 default-manager activation remains conditional
- [ai_workflow/](ai_workflow/) — current workflow rules and navigation
- [app_factory/](app_factory/) — WS3 application factory, shipped in #545; its Gate 2 record and follow-ups are tracked in #593
- [backup_confirmation_continuity/](backup_confirmation_continuity/) — shipped U2; residual-risk and status records require reconciliation
- [backup_export_execution_fields/](backup_export_execution_fields/) — #567/#568 requirements brief, council-reviewed plan and implementation evidence; current status in #567 and #568
- [ci_cd_expansion/](ci_cd_expansion/) — CI/CD expansion plan, settings-activation records and the machine-read B1 action inventory
- [ci_cd_phase3/](ci_cd_phase3/) — pinned Pyright baseline used by CI
- [deep_gate_linux_visual_failure_20260831/](deep_gate_linux_visual_failure_20260831/) — completed Gate-1 diagnostic; further action awaits an owner decision
- [finding1_residual/](finding1_residual/) — shipped D7; residual poisoned-row behavior still needs a current reference
- [issue565_socket_allocation/](issue565_socket_allocation/) — #565 diagnosis, Gate 1 requirements and evidence for the ADR-014 static replay
- [ki005_controls_persistence/](ki005_controls_persistence/) — shipped KI-005; retains the held Stage 4 restoration baseline
- [product/](product/) — always-active reference for shipped behavior, schema, and design
- [project_direction/](project_direction/) — agreed project direction, owner decisions and workstream sequencing
- [r23_js_unit_promotion/](r23_js_unit_promotion/) — JS-unit Q4/D2 decision record
- [release_pipeline/](release_pipeline/) — shipped pipeline and remaining release/deep-gate entry conditions
- [service_extraction/](service_extraction/) — WS4 service extraction; slice 1 shipped in #556
- [test_inventory/](test_inventory/) — generated test inventory checked by CI
- [testing_d4_invariants/](testing_d4_invariants/) — ADR-009 property-invariant scope and deferred Packet C
- [testing_phase2/](testing_phase2/) — completed Phase 2 plan plus current, test-pinned accessibility exceptions
- [testing_phase3/](testing_phase3/) — testing plans and the live JS-unit observation ledger
- [toast_action_continuity/](toast_action_continuity/) — shipped U3b; its amended U1 follow-up condition was discharged when #553 closed U1-FOLLOWUP-1
- [visual_determinism/](visual_determinism/) — terminal visual contract and accepted residual under ADR-011
- [volume_failure_feedback/](volume_failure_feedback/) — shipped U1; U1-FOLLOWUP-1 closed by #553; retained evidence supports the separate JS-unit qualification work (#582/#592)

### Closed (history)

- [worktree_cleanup/](worktree_cleanup/) — campaign closed by owner decision on 2026-11-10 (#669); the closeout, owner acceptance and evidence stay here; the three plans are archived (see *Archive*), and the navigation stub is retired below

- [css_phase4_wp4_4/](css_phase4_wp4_4/) — completed WP4.4 arc and handoff history
- [css_scale_btn_cleanup/](css_scale_btn_cleanup/) — completed scale-button cleanup, council findings, and evidence
- [css_table_helpers_cleanup/](css_table_helpers_cleanup/) — completed table-helper cleanup and evidence
- [css_theme_dark_p3/](css_theme_dark_p3/) — arc terminated after shipped a0; no later packet authorized
- [deep_gate_robustness_gate0/](deep_gate_robustness_gate0/) — shipped: Gate 1 implementation #474 (`55953069`, deep-gate e2e selection fail-closed)
- [dnone_display_utilities/](dnone_display_utilities/) — shipped display-utility cleanup evidence
- [fatigue_meter/](fatigue_meter/) — shipped meter and heatmap; Stage 4 closed, with calibration contracts and evidence retained
- [msys_destination_validation/](msys_destination_validation/) — guard destination validation and drive-root monitor, merged in #654; delegated acceptance and coverage limits in its closeout
- [pyright_filter_predicates/](pyright_filter_predicates/) — closed Pyright burn-down record
- [pyright_volume_progress/](pyright_volume_progress/) — closed Pyright burn-down record
- [quality_gate_routing/](quality_gate_routing/) — shipped quality-gate routing work
- [toast_type_word_collision/](toast_type_word_collision/) — shipped KI-010; retains code and test references
- [u1_followup_1_vitest/](u1_followup_1_vitest/) — U1-FOLLOWUP-1 Vitest coverage: implementation #551, closeout #553
- [user_profile/](user_profile/) — shipped profile; design and estimator/calibration references remain current
- [visual_baseline_win32/](visual_baseline_win32/) — superseded Windows-baseline recovery evidence
- [workout_cool_integration/](workout_cool_integration/) — shipped integration; media rules, provenance, and video reference remain current

### Proposed

- [refactor_optional/](refactor_optional/) — optional-refactor assessments; no implementation approval is implied

## Archive

These files are historical reference only. They should not be treated as active backlog:

- **[archive/PLAN_GENERATOR_IMPLEMENTATION.md](archive/PLAN_GENERATOR_IMPLEMENTATION.md)** - Completed starter-plan implementation tracker
- **[archive/DOCS_AUDIT_PLAN.md](archive/DOCS_AUDIT_PLAN.md)** - Archived docs/code audit rollout record
- **[archive/ci_cd/](archive/ci_cd/)** - Completed CI/CD Improvement Plan and retained council plans (shipped via PRs #40–#51); the Phase 1 plan is retired below. Note: the live `docs/ci_cd_phase3/pyright-baseline.json` CI artifact stays in the active tree (referenced by `.github/workflows/ci.yml`), not archived.
- **[archive/VOLUME_TAXONOMY_AUDIT.md](archive/VOLUME_TAXONOMY_AUDIT.md)** - Phase 0 live database audit (2026-04-25). Completed audit, now archived.
- **[archive/workout_cool_integration/checkpoint3_coverage.md](archive/workout_cool_integration/checkpoint3_coverage.md)** - Completed free-exercise-db mapper coverage baseline (pre-curation snapshot).
- **[archive/2026/local-first-assets/PLANNING.md](archive/2026/local-first-assets/PLANNING.md)** - Local-first navigation assets plan, council response matrix and as-built record (shipped #341); current contract: `tests/test_local_first_assets.py` and `static/vendor/*/NOTICE.md`.
- **[archive/2026/worktree-plans/](archive/2026/worktree-plans/)** - Closed worktree cleanup plans, archived 2026-11-15 (#688) with their text unchanged apart from link repairs: [P1.2 ledger](archive/2026/worktree-plans/p1_2/PLANNING.md) (August 2026), [Operation A council record](archive/2026/worktree-plans/operation-a/PLANNING.md) and [drive-root amendment council record](archive/2026/worktree-plans/drive-root-amendment/PLANNING.md) (published in #659). The campaign was closed by #669; current rules: `ai_workflow/PARALLEL_WORKFLOW.md`, closeout: `worktree_cleanup/CLOSEOUT.md`.
- **[archive/2026/grounding-scan/](archive/2026/grounding-scan/)** - Codebase grounding scan of 2026-07-03 (merged in #89). The findings ledger, progress log and recommendations were archived on 2026-10-19. The [README](archive/2026/grounding-scan/README.md) and the 21 per-phase evidence files under [`phases/`](archive/2026/grounding-scan/phases/) followed on 2026-11-16: the phase files are byte-identical, and the README gains an archive note and re-pointed links. Evidence, not backlog: re-measure any nomination against current code. Current sources: `DUPLICATION_REGISTRY.md` and the owning GitHub issues.

## Removed From Active Docs

Two superseded guides were retired to Git history on 2026-11-11 by #670:
[`FILTER_VIEW_MODE.md`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/04816d8d8d6ee576ae3f2738468e29d8078fa293/docs/FILTER_VIEW_MODE.md)
and [`program_backups.md`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/04816d8d8d6ee576ae3f2738468e29d8078fa293/docs/program_backups.md),
linked at `04816d8d`, the last commit containing both. Their accurate content lives in
[`product/APP_FLOW.md`](product/APP_FLOW.md) (*Muscle naming mode*, *Backup Center*, *Startup snapshot*).

The old Backup Center hardening plan, Calm Glass redesign plan/audit/mockup, seed-fix plan, and spring-cleanup Phase 4/5 execution plans were completed and superseded by the current source, changelog, CSS map, and Backup Center docs.

Six shipped feature plans were retired to Git history on 2026-11-14 under
[Documentation Retention](ai_workflow/DOC_RETENTION.md#retirement-criteria). Each link opens the
plan at `189756f4`, the main snapshot immediately before this batch:

- [agent_workflow_integrity](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/189756f473601850c82912f43f25f16396bdc8fa/docs/agent_workflow_integrity/PLANNING.md) — shipped as #292
- [blank_null_rep_bounds](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/189756f473601850c82912f43f25f16396bdc8fa/docs/blank_null_rep_bounds/PLANNING.md) — Gate 0 #465, fix #467
- [page_readiness](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/189756f473601850c82912f43f25f16396bdc8fa/docs/page_readiness/PLANNING.md) — shipped as #347, #350 and #355
- [pyright_volume_splitter](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/189756f473601850c82912f43f25f16396bdc8fa/docs/pyright_volume_splitter/PLANNING.md) — shipped as #328
- [superset_routine_selection](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/189756f473601850c82912f43f25f16396bdc8fa/docs/superset_routine_selection/PLANNING.md) — shipped as #346
- [wpb4_unassigned_bucket](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/189756f473601850c82912f43f25f16396bdc8fa/docs/wpb4_unassigned_bucket/PLANNING.md) — shipped as #256

Twelve completed records and navigation stubs were retired to Git history on 2026-11-16
under the same criteria. Each historical link opens the file at `a0c32d63`, the last
commit containing all twelve on this batch branch. Current references are listed alongside it.

| Retired file | Maintained home |
|---|---|
| [archive/2026/fetch-wrapper/WP3_5_FETCH_INVENTORY.md](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/a0c32d637ee1e5e450d3e858a8ff75538956263f/docs/archive/2026/fetch-wrapper/WP3_5_FETCH_INVENTORY.md) | [Transport closeout](REFACTOR_PLAN.md#wp35-json-api-transport-consolidation) and [fetch wrapper](../static/js/modules/fetch-wrapper.js) |
| [archive/MISSING_TESTS_CHECKLIST.md](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/a0c32d637ee1e5e450d3e858a8ff75538956263f/docs/archive/MISSING_TESTS_CHECKLIST.md) | [Current test inventory](test_inventory/TEST_INVENTORY.md) and maintained tests |
| [archive/MISSING_TESTS_PART2.md](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/a0c32d637ee1e5e450d3e858a8ff75538956263f/docs/archive/MISSING_TESTS_PART2.md) | [Current test inventory](test_inventory/TEST_INVENTORY.md) and maintained tests |
| [archive/SUPERSET_FEATURE.md](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/a0c32d637ee1e5e450d3e858a8ff75538956263f/docs/archive/SUPERSET_FEATURE.md) | [Product flow](product/APP_FLOW.md), [schema](product/BACKEND_SCHEMA.md) and [superset tests](../tests/test_superset.py) |
| [archive/ci_cd/phase1/PLANNING.md](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/a0c32d637ee1e5e450d3e858a8ff75538956263f/docs/archive/ci_cd/phase1/PLANNING.md) | [E2E inclusion and privacy rules](../e2e/CLAUDE.md), current CI and retained [A11 evidence](archive/2026/master-handover/CURRENT_STATE_HISTORY.md) |
| [archive/plan-volume-integration/PLAN_VOLUME_INTEGRATION.md](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/a0c32d637ee1e5e450d3e858a8ff75538956263f/docs/archive/plan-volume-integration/PLAN_VOLUME_INTEGRATION.md) | [Planning](archive/plan-volume-integration/PLAN_VOLUME_INTEGRATION_PLANNING.md) and [execution](archive/plan-volume-integration/PLAN_VOLUME_INTEGRATION_EXECUTION.md) siblings |
| [backup_schema_version/PLANNING.md](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/a0c32d637ee1e5e450d3e858a8ff75538956263f/docs/backup_schema_version/PLANNING.md) | [ADR-008](DECISIONS.md#adr-008-backup_schema_version-is-a-reserved-informational-label-not-an-enforced-contract), [#373](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/373) and [restore fuzz tests](../tests/test_program_backup_restore_fuzz.py) |
| [deep_gate_robustness_gate0/GATE1_PLAN.md](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/a0c32d637ee1e5e450d3e858a8ff75538956263f/docs/deep_gate_robustness_gate0/GATE1_PLAN.md) | [Runner contract tests](../tests/test_playwright_runner_contracts.py); [original evidence](deep_gate_robustness_gate0/EVIDENCE.md) stays |
| [doc_truth/PLANNING.md](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/a0c32d637ee1e5e450d3e858a8ff75538956263f/docs/doc_truth/PLANNING.md) | [Duplication registry](DUPLICATION_REGISTRY.md), [quality gate](ai_workflow/QUALITY_GATE.md) and [retention rules](ai_workflow/DOC_RETENTION.md) |
| [p1_4_debug_scaffolding/PLANNING.md](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/a0c32d637ee1e5e450d3e858a8ff75538956263f/docs/p1_4_debug_scaffolding/PLANNING.md) | [#291](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/291) preserves decisions, visual measurements and residual observations |
| [user_profile/PLANNING.md](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/a0c32d637ee1e5e450d3e858a8ff75538956263f/docs/user_profile/PLANNING.md) | [Design](user_profile/DESIGN.md), [estimator](../utils/profile_estimator.py) and [tests](../tests/test_profile_estimator.py); [execution log](user_profile/EXECUTION_LOG.md) stays |
| [worktree_cleanup/AMENDMENT_2026-09-28.md](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/a0c32d637ee1e5e450d3e858a8ff75538956263f/docs/worktree_cleanup/AMENDMENT_2026-09-28.md) | [Retained council record](archive/2026/worktree-plans/drive-root-amendment/PLANNING.md#historical-source-reference-landing) reproduces this navigation stub; the September original remains private |

This index is maintained by hand. It carries no dated freshness stamp on purpose — one
was previously written here and went stale without anyone noticing. Check `git log` for
this file if you need to know when it last changed.
