# Hypertrophy Toolbox v3 Documentation

This directory holds current references, open work, and retained completion history. Use the categories below to distinguish their roles.

## Active Docs

### Product Reference

The [`product/`](product/) suite describes the shipped application — behavior, schema, and design.
It is descriptive and carries no status; anything time-sensitive stays in `MASTER_HANDOVER.md`.

- **[product/README.md](product/README.md)** - Suite index, canonical-source map, conflict rules, terminology, and how work gets planned
- **[product/APP_FLOW.md](product/APP_FLOW.md)** - Every screen: purpose, controls, action types, and success / no-result / failure outcomes
- **[product/BACKEND_SCHEMA.md](product/BACKEND_SCHEMA.md)** - Every table, column, constraint, index, and relationship, with an ER diagram
- **[product/DESIGN_BRIEF.md](product/DESIGN_BRIEF.md)** - The shipped design system: tokens with measured consumers, theming, typography, motion, accessibility

### Project State
- **[MASTER_HANDOVER.md](MASTER_HANDOVER.md)** - Canonical current state; the file new agents read first
- **[ACTIVE_DEVELOPMENT.md](ACTIVE_DEVELOPMENT.md)** - Fatigue calibration guardrails and agent authority rules; earlier objectives and status blocks archived
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and recent work
- **[DECISIONS.md](DECISIONS.md)** - Durable project decisions and lightweight ADRs
- **[CLAUDE_MD_AUDIT.md](CLAUDE_MD_AUDIT.md)** - Current architecture debt snapshot
- **[LEFTOVERS_BY_PRIORITY.md](LEFTOVERS_BY_PRIORITY.md)** - Prioritized punch list of unfinished / parked / deferred items
- **[OPEN_WORK_EXECUTION_PLAN.md](OPEN_WORK_EXECUTION_PLAN.md)** - Reconciled order of work, estimates, decision gates, and explicit closed/parked boundaries
- **[ai_workflow/INDEX.md](ai_workflow/INDEX.md)** - AI workflow navigation spine
- **[ai_workflow/DOC_RETENTION.md](ai_workflow/DOC_RETENTION.md)** - Rules for keeping, archiving, or deleting docs

### Runtime, UI, And Testing
- **[CSS_OWNERSHIP_MAP.md](CSS_OWNERSHIP_MAP.md)** - Current CSS loading and ownership map
- **[E2E_TESTING.md](E2E_TESTING.md)** - How to run Playwright, and what each spec covers. For counts see **[test_inventory/TEST_INVENTORY.md](test_inventory/TEST_INVENTORY.md)**, the generated single producer
- **[UI_SCENARIOS_GAP_ANALYSIS.md](UI_SCENARIOS_GAP_ANALYSIS.md)** - UI risk status, deferred quality items, and Known Issues table (KI-001..)

### Feature Docs
- **[FILTER_VIEW_MODE.md](FILTER_VIEW_MODE.md)** - Simple vs scientific muscle naming mode
- **[program_backups.md](program_backups.md)** - Backup Center and program snapshot behavior
- **[muscle_selector.md](muscle_selector.md)** - Muscle selector component notes
- **[muscle_selector_vendor.md](muscle_selector_vendor.md)** - Vendor SVG attribution

## Feature folders

Active includes current references, deferred work, and records awaiting reconciliation.
Closed describes execution status; current contracts and evidence in those folders stay in place.
Proposed entries do not authorize implementation. The archive container is indexed separately below.

### Active

- [agent_roles/](agent_roles/) — role rollout; Phase 6 default-manager activation remains conditional
- [ai_workflow/](ai_workflow/) — current workflow rules and navigation
- [backup_confirmation_continuity/](backup_confirmation_continuity/) — shipped U2; residual-risk and status records require reconciliation
- [ci_cd_phase3/](ci_cd_phase3/) — pinned Pyright baseline used by CI
- [deep_gate_linux_visual_failure_20260831/](deep_gate_linux_visual_failure_20260831/) — completed Gate-1 diagnostic; further action awaits an owner decision
- [finding1_residual/](finding1_residual/) — shipped D7; residual poisoned-row behavior still needs a current reference
- [ki005_controls_persistence/](ki005_controls_persistence/) — shipped KI-005; retains the held Stage 4 restoration baseline
- [product/](product/) — always-active reference for shipped behavior, schema, and design
- [release_pipeline/](release_pipeline/) — shipped pipeline and remaining release/deep-gate entry conditions
- [test_inventory/](test_inventory/) — generated test inventory checked by CI
- [testing_d4_invariants/](testing_d4_invariants/) — ADR-009 property-invariant scope and deferred Packet C
- [testing_phase2/](testing_phase2/) — completed Phase 2 plan plus current, test-pinned accessibility exceptions
- [testing_phase3/](testing_phase3/) — testing plans and the live JS-unit observation ledger
- [toast_action_continuity/](toast_action_continuity/) — shipped U3b; retains the amended U1 follow-up condition
- [visual_determinism/](visual_determinism/) — terminal visual contract and accepted residual under ADR-011
- [volume_failure_feedback/](volume_failure_feedback/) — shipped U1; U1-FOLLOWUP-1 remains open under its recorded conditions
- [worktree_cleanup/](worktree_cleanup/) — committed workflow and preservation records; separate owner approvals govern further operations

### Closed (history)

- [agent_workflow_integrity/](agent_workflow_integrity/) — shipped workflow-integrity contracts
- [backup_schema_version/](backup_schema_version/) — closed D6 investigation; ADR-008 records the outcome
- [css_phase4_wp4_4/](css_phase4_wp4_4/) — completed WP4.4 arc and handoff history
- [css_scale_btn_cleanup/](css_scale_btn_cleanup/) — completed scale-button cleanup, council findings, and evidence
- [css_table_helpers_cleanup/](css_table_helpers_cleanup/) — completed table-helper cleanup and evidence
- [css_theme_dark_p3/](css_theme_dark_p3/) — arc terminated after shipped a0; no later packet authorized
- [dnone_display_utilities/](dnone_display_utilities/) — shipped display-utility cleanup evidence
- [doc_truth/](doc_truth/) — shipped documentation-truth repairs
- [fatigue_meter/](fatigue_meter/) — shipped meter and heatmap; Stage 4 closed, with calibration contracts and evidence retained
- [local_first_assets/](local_first_assets/) — shipped local asset work
- [p1_4_debug_scaffolding/](p1_4_debug_scaffolding/) — completed debug-scaffolding work
- [page_readiness/](page_readiness/) — shipped page-readiness work
- [pyright_filter_predicates/](pyright_filter_predicates/) — closed Pyright burn-down record
- [pyright_volume_progress/](pyright_volume_progress/) — closed Pyright burn-down record
- [pyright_volume_splitter/](pyright_volume_splitter/) — closed Pyright burn-down record
- [quality_gate_routing/](quality_gate_routing/) — shipped quality-gate routing work
- [scan/](scan/) — completed grounding-scan evidence
- [superset_routine_selection/](superset_routine_selection/) — shipped routine-selection work
- [toast_type_word_collision/](toast_type_word_collision/) — shipped KI-010; retains code and test references
- [user_profile/](user_profile/) — shipped profile; design and estimator/calibration references remain current
- [visual_baseline_win32/](visual_baseline_win32/) — superseded Windows-baseline recovery evidence
- [workout_cool_integration/](workout_cool_integration/) — shipped integration; media rules, provenance, and video reference remain current
- [wpb4_unassigned_bucket/](wpb4_unassigned_bucket/) — shipped unassigned-bucket behavior

### Proposed

- [blank_null_rep_bounds/](blank_null_rep_bounds/) — Gate 0 characterization shipped as #465; production implementation is unauthorized
- [deep_gate_robustness_gate0/](deep_gate_robustness_gate0/) — Gate 0 evidence and bounded Gate-1 proposal; implementation requires separate authorization
- [refactor_optional/](refactor_optional/) — optional-refactor assessments; no implementation approval is implied

## Archive

These files are historical reference only. They should not be treated as active backlog:

- **[archive/MISSING_TESTS_CHECKLIST.md](archive/MISSING_TESTS_CHECKLIST.md)** - Historical missing-tests tracker
- **[archive/MISSING_TESTS_PART2.md](archive/MISSING_TESTS_PART2.md)** - Follow-up historical test tracker
- **[archive/SUPERSET_FEATURE.md](archive/SUPERSET_FEATURE.md)** - Completed superset feature implementation notes
- **[archive/PLAN_GENERATOR_IMPLEMENTATION.md](archive/PLAN_GENERATOR_IMPLEMENTATION.md)** - Completed starter-plan implementation tracker
- **[archive/DOCS_AUDIT_PLAN.md](archive/DOCS_AUDIT_PLAN.md)** - Archived docs/code audit rollout record
- **[archive/ci_cd/](archive/ci_cd/)** - Completed CI/CD Improvement Plan + per-phase council plans (Phases 0–5, shipped via PRs #40–#51). Note: the live `docs/ci_cd_phase3/pyright-baseline.json` CI artifact stays in the active tree (referenced by `.github/workflows/ci.yml`), not archived.
- **[archive/VOLUME_TAXONOMY_AUDIT.md](archive/VOLUME_TAXONOMY_AUDIT.md)** - Phase 0 live database audit (2026-04-25). Completed audit, now archived.
- **[archive/workout_cool_integration/checkpoint3_coverage.md](archive/workout_cool_integration/checkpoint3_coverage.md)** - Completed free-exercise-db mapper coverage baseline (pre-curation snapshot).

## Removed From Active Docs

The old Backup Center hardening plan, Calm Glass redesign plan/audit/mockup, seed-fix plan, and spring-cleanup Phase 4/5 execution plans were completed and superseded by the current source, changelog, CSS map, and Backup Center docs.

This index is maintained by hand. It carries no dated freshness stamp on purpose — one
was previously written here and went stale without anyone noticing. Check `git log` for
this file if you need to know when it last changed.
