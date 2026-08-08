# tests/ — Orientation

## Purpose
Pytest suite covering routes, utils, and integration paths. Each test gets a unique tmp SQLite DB via the `app` / `client` fixtures — never hits the live `data/database.db`.

## Key files
| File | Role |
|---|---|
| `conftest.py` | Fixture hierarchy (see below) and blueprint registration for the test app |
| `test_<route>.py` | Per-route HTTP tests (e.g. `test_workout_plan_routes.py`) |
| `test_<util>.py` | Per-module unit tests (e.g. `test_effective_sets.py`, `test_fatigue.py`) |
| `test_priority0_*.py` | Cross-cutting contract / FK / filter tests |
| `test_harness_isolation.py` | Verifies the test fixtures themselves isolate DB state |

## Fixture hierarchy (`conftest.py`)
```
schema_template (session)       — empty schema built ONCE per worker
test_db_path (function)         — unique tmp_path SQLite per test
  app (function)                — Flask app + copy of schema_template, all blueprints
    client (function)           — test client bound to the same DB
    db_handler (function)       — DatabaseHandler at the same DB
      clean_db (function)       — DELETEs rows, preserves tables
        exercise_factory        — INSERTs into exercises
        workout_plan_factory    — needs exercise
        workout_log_factory     — needs plan
```

The `app` fixture **copies** `schema_template` rather than re-running
`run_all_initializers()`. Rebuilding cost ~290ms × 787 setups; the copy is
~0.4ms. Adding a table still only means registering its initializer in
`utils/schema_registry.py` — the template picks it up automatically.

## Conventions
- Patch DB path by **assignment**, not import: `import utils.config; utils.config.DB_FILE = test_db_path`. `DatabaseHandler.__init__` reads `utils.config.DB_FILE` at call time (`database.py:209`).
- Use the shared `app` / `client` / `db_handler` fixtures unless you need a specialized setup.
- New blueprint? Register in **both** `app.py` and `conftest.py`'s `app` fixture.
- New table? Call its creator in `conftest.py`'s `app` fixture and `erase_data()` inner function (see `.claude/rules/database.md`).

## Gotchas
- `pytest` not found → use `.venv/Scripts/python.exe -m pytest` (system Python lacks deps).
- `no such table` → bypassed conftest init; use the shared fixtures.
- `FK constraint failed` → call `exercise_factory` before `workout_plan_factory` before `workout_log_factory`.

## See also
- `.claude/rules/testing.md` — full E2E map, baselines, fixture detail
- `/run-tests` skill (full or scoped) and `/verify-suite` skill (full gate)
