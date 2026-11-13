# tests/ — Orientation

## Purpose
Pytest suite covering routes, utils, and integration paths. Each test gets a unique tmp SQLite DB via the `app` / `client` fixtures — never hits the live `data/database.db`.

## Running

```bash
# Recommended local fast lane. --dist loadfile is REQUIRED, not a tuning knob:
# module-scoped fixtures mean a file's tests must stay on one worker.
.venv/Scripts/python.exe -m pytest tests/ -q -n 8 --dist loadfile

# Serial — diagnostic mode, and the form to use when investigating a failure.
.venv/Scripts/python.exe -m pytest tests/ -q
```

Measured locally: **serial median ≈195s, `-n 8 --dist loadfile` median ≈76s.**

Parallel is opt-in; without `-n` the plugin does nothing. CI runs no xdist: the
guard-hook file is split across four runners, serial within each, and
`pytest-core` is serial (`docs/ci_cd_expansion/PLANNING.md` §14 — xdist workers
crashed concurrent pwsh there). These medians are this machine's, and a CI worker
count must be derived from CI. Keep using serial to
diagnose a failure — worker output is interleaved, and a test that only fails in
parallel is itself the finding.

**More workers stop helping early.** `loadfile` makes a file indivisible, so
under this scheduler the slowest single file is the floor. Here that is
`test_guard_destructive_command.py`, which is parametrized over the installed
PowerShell hosts and dominates the suite on Windows, where both hosts exist.
Past a handful of workers the run is bounded by that one file, and `-n 16`
measured no better than `-n 8`. That floor is platform-dependent: the ubuntu
runner has one host and collects far fewer of those nodes, so a CI worker count
must be derived from CI, never from these numbers.

That floor belongs to the scheduler, not to the suite. A `loadgroup` design
could group only the modules that genuinely share state and let the independent
tests inside this file spread across workers. Establishing which modules those
are needs a suite-wide isolation audit, so it is separate work — not a
prerequisite for the command above.

## Key files
| File | Role |
|---|---|
| `conftest.py` | Fixture hierarchy (see `.claude/rules/testing.md`); the `app` fixture is the production `create_app()` factory |
| `test_<route>.py` | Per-route HTTP tests (e.g. `test_workout_plan_routes.py`) |
| `test_<util>.py` | Per-module unit tests (e.g. `test_effective_sets.py`, `test_fatigue.py`) |
| `test_priority0_*.py` | Cross-cutting contract / FK / filter tests |
| `test_harness_isolation.py` | Verifies the test fixtures themselves isolate DB state |

## Conventions
- Use the shared `app` / `client` / `db_handler` fixtures unless you need a specialized setup.
- New table? Register its creator in `run_all_initializers()` (`utils/schema_registry.py`); `schema_template` picks it up. A user-state table also joins `clean_db`'s `DELETE` list (see `.claude/rules/database.md`).

## See also
- `.claude/rules/testing.md` — full E2E map, baselines, fixture detail
- `/run-tests` skill (full or scoped) and `/verify-suite` skill (full gate)
