# CLAUDE.md

Operational guidance for Claude Code. Keep this file under 200 lines and limited to what most tasks need. Subsystem-specific detail lives in `.claude/rules/*.md` and loads only when the matching files enter context. **For long-running work, read [`docs/MASTER_HANDOVER.md`](docs/MASTER_HANDOVER.md) first** (canonical current state); folder orientation lives in `<dir>/CLAUDE.md` files.

---

## 1. Product Intent

A local-first Flask web app for designing, logging, and analyzing hypertrophy (muscle-building) resistance-training programs. Single user, no auth, runs on `localhost:5000`. Core workflows: Plan (`/workout_plan`), Log (`/workout_log`), Analyze (`/weekly_summary`, `/session_summary`), Progress (`/progression`), Distribute (`/volume_splitter`), Profile (`/user_profile`) and Backup (`/api/backups`). Per-page controls and outcomes: [`docs/product/APP_FLOW.md`](docs/product/APP_FLOW.md).

### Key terminology
| Term | Meaning |
|---|---|
| RIR | Reps In Reserve — how many reps short of failure |
| RPE | Rate of Perceived Exertion — 1–10 effort scale |
| Effective sets | Raw sets × effort factor × rep-range factor × muscle contribution weight (`calculate_effective_sets()` in `utils/effective_sets.py`) |
| CountingMode | `RAW` or `EFFECTIVE` — which set number to display (`utils/effective_sets.py`) |
| ContributionMode | `DIRECT_ONLY` (primary only) or `TOTAL` (weighted secondary/tertiary) (`utils/effective_sets.py`) |
| Routine | Named exercise group, e.g. `"GYM - Full Body - Workout A"` |
| Movement pattern | Biomechanical classification: squat, hinge, horizontal_push, etc. (`utils/movement_patterns.py`) |
| Superset | Two exercises linked for back-to-back performance — stored in `user_selection.superset_group` |

### Refactor invariant
Any change to core workflow behavior (plan/log/analyze/progress/distribute/backup) requires migration notes in the PR description and updated test coverage. Do not silently alter calculation logic, DB schema, or API response shapes.

### Non-goals
- No user accounts or authentication — single-user local only.
- No cloud sync or remote database.
- Effective sets are **informational only** — never auto-adjust or block user actions (module docstring, `utils/effective_sets.py`).

---

## 2. Architecture

### Startup
Importing `app` performs no database, data-directory, migration, seed, catalog-upgrade or backup work. The first `get_logger()` call in a process — triggered transitively by importing `app`, any route module or most `utils` modules — still creates `<runtime root>/logs/` and attaches the `app.log` file handler and the console handler.

`create_app()` registers 13 blueprints plus one direct route, `POST /erase-data` (`erase_data()` in `app.py`), which is **not** a blueprint. Only the entry points call `init_runtime()` (`utils/runtime_init.py`), once per process; it runs migration, seeding, the schema registry, the catalog upgrade and the startup backup in a load-bearing order. The tests' `app` fixture is `create_app()` without it. Sequence, entry points and reasoning: `.claude/rules/database.md`.

### Module boundaries
```
app.py                 ← create_app() + middleware + entry points only; no business logic
  routes/*.py          ← HTTP: validate input → call utils → return response
    utils/*.py         ← all business logic + DB queries
      utils/database.py → DatabaseHandler → SQLite (path resolved by utils/runtime_paths.py)
```

- Routes import from utils; utils never import from routes.
- Prefer concrete module imports such as `utils.db_initializer`; `utils/__init__.py` is no longer the authoritative facade for new code.
- All DB access via `DatabaseHandler` context manager (class + `__enter__` / `__exit__` in `utils/database.py`).
- All JSON responses via `success_response()` / `error_response()` (`utils/errors.py`).
- All logging via `get_logger()` (`utils/logger.py`).
- Named infrastructure exception: `scripts/seed_worktree_snapshot.py` (validated worktree seeding only); see `.claude/rules/database.md`.

### Deeper references
- Routes / API endpoints / filters / security / new-feature checklist → `.claude/rules/routes.md` (loads when editing `routes/**`).
- DB schema / DatabaseHandler / adding tables / startup / env vars → `.claude/rules/database.md` (loads when editing `utils/database*.py` or `utils/db_initializer.py`).
- Templates / JS modules / SCSS → `.claude/rules/frontend.md` (loads when editing `templates/**`, `static/**`, `scss/**`).
- Pytest + Playwright + E2E map → `.claude/rules/testing.md` (loads when editing `tests/**` or `e2e/**`).
- Logging / request tracing / typical failures → `.claude/rules/debugging.md` (loads when editing `utils/logger.py` or `utils/request_id.py`).

---

## 3. Conventions

### Windows workflow safety
Never set/export `MSYS_NO_PATHCONV` or `MSYS2_ARG_CONV_EXCL`; run the worktree
environment preflight in fresh sessions. Use PowerShell end to end, argument arrays
and drive-qualified native output paths. Resolve Git blobs via one validated full
OID before `cat-file blob`. The command-text guard is bounded prevention, not a sandbox.
Worktree creation requires lifecycle/baseline review and target-bound launch setup;
see `docs/ai_workflow/PARALLEL_WORKFLOW.md`. During the approved cleanup sequence,
retain worktrees, branches, reflogs, recovery roots and discovered snapshots until
their separate owner-approved operation; no ordinary teardown bypasses that hold.

### Logging and paths
`get_logger()` returns the `'hypertrophy_toolbox'` logger (`utils/logger.py`), writing to `<runtime root>/logs/app.log` and the console. The runtime root is the repository in a source checkout and `%LOCALAPPDATA%\HypertrophyToolbox` in a frozen build — never assume repository-local paths (`utils/runtime_paths.py`). `DB_FILE` overrides the SQLite path (tests patch `utils.config.DB_FILE`) and `HT_RUNTIME_DIR` relocates the whole runtime tree; the full env-var table is in `.claude/rules/database.md`.

### Repository root policy
The root holds five categories only — entry points, user-facing start/readme files, build manifests, root-discovered tool config, and repository operating instructions. Generated output (baselines, reports, screenshots, scratch DBs) goes under the gitignored `artifacts/`, never the root. Full table and rationale: `docs/DECISIONS.md` ADR-002.

### Constants and normalization
`utils/constants.py` has canonical enums. Always normalize before persisting: `normalize_muscle()`, `normalize_equipment()`, etc. from `utils/normalization.py`.

### Reasoning effort is not agent authorization

Applies to every kind of task — implementation, audits, migrations, research and reviews alike.
Reasoning-effort words such as "high", "max" and "ultra" do not authorize additional agents. Use
the minimum agents required by the explicit request and applicable repository workflow, such as
the gates in
[`docs/ai_workflow/QUALITY_GATE.md`](docs/ai_workflow/QUALITY_GATE.md#plan-stage-routing).
Additional optional agents, review layers, or per-finding verifier pairs require explicit user
authorization — propose them and let the owner decide. Preserve mandatory delegation, approval
gates, and reviewer independence.

A review that did not run, or whose reviewer failed, is **incomplete** — never record it as
"no findings" or "refuted", and never let it move an approval status.

### Run commands
```bash
# Dev server
.venv/Scripts/python.exe app.py

# Tests — use the /run-tests skill, or:
.venv/Scripts/python.exe -m pytest tests/ -q

# E2E — use the /run-e2e skill, or:
npx playwright test --project=chromium --reporter=line

# Full gate — use the /verify-suite skill
# CSS — use the /build-css skill, or: npm run build:css
```

---

## 4. Cross-cutting Playbooks

### A. Add a new feature
Follow the checklist in `.claude/rules/routes.md` (*Adding a feature end to end*).

### B. Refactor safely
1. **Scope**: search the function/class name across `routes/`, `utils/`, `templates/`, `tests/`.
2. **Change**: keep the old interface as a thin wrapper while callers span multiple files.
3. **Gate**: finish with `/verify-and-polish`; tests and reviewers follow `docs/ai_workflow/QUALITY_GATE.md`. No blanket pre-change baseline; if a failure's origin is unclear, reproduce it in an isolated base checkout, not by stashing.
4. Generated output goes under the gitignored `artifacts/`.

---

## 5. Current State & Risks

Point-in-time status lives in [`docs/MASTER_HANDOVER.md`](docs/MASTER_HANDOVER.md); this section holds durable gotchas only. The response-contract rule and its HTTP-200 "no result" cases are in `.claude/rules/routes.md`.

### exercise_order column
Added at startup by `initialize_exercise_order()` (defined in `utils/schema_registry.py`, re-exported from `routes/workout_plan.py`) via `ALTER TABLE`. `get_workout_plan()` in `routes/workout_plan.py` defensively checks `column_exists()` for pre-migration DBs.

### session_summary vs weekly_summary — not duplicates
`calculate_session_summary()` (`utils/session_summary.py`) groups by routine with an optional date filter; `calculate_weekly_summary()` (`utils/weekly_summary.py`) aggregates all routines weekly with no date filter and tracks frequency. The first imports only `EFFECTIVE_STATUS_MAP` from the second.

### Historical audit trail
Full audit history and resolved violations: `docs/CLAUDE_MD_AUDIT.md`.
