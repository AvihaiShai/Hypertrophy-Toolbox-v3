# Hypertrophy Toolbox v3 Documentation

This directory keeps the current project docs. Completed execution plans and migration handoff files have been removed from the active docs surface so the folder stays focused on what still helps maintain the app.

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
- **[ACTIVE_DEVELOPMENT.md](ACTIVE_DEVELOPMENT.md)** - Execution source of truth for autonomous sessions
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
