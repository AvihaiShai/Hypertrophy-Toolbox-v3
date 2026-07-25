---
paths:
  - "utils/database.py"
  - "utils/db_initializer.py"
  - "utils/config.py"
  - "utils/program_backup.py"
  - "utils/auto_backup.py"
---

# Database guide

## Schema (from `utils/db_initializer.py`)
| Table | PK | Key FK | Created in |
|---|---|---|---|
| `exercises` | `exercise_name TEXT` | — | `db_initializer.py:34` |
| `exercise_isolated_muscles` | `(exercise_name, muscle)` | → `exercises` CASCADE | `db_initializer.py:90` |
| `user_selection` | `id INTEGER` | `exercise` → `exercises` CASCADE | `db_initializer.py:166` |
| `workout_log` | `id INTEGER` | `workout_plan_id` → `user_selection` CASCADE | `db_initializer.py:237` |
| `progression_goals` | `id INTEGER` | — | `database.py:460` |
| `volume_plans` | `id INTEGER` | — | `database.py:484` |
| `muscle_volumes` | `id INTEGER` | `plan_id` → `volume_plans` CASCADE | `database.py:491` |
| `program_backups` | `id INTEGER` | — | `utils/program_backup.py:23` |
| `program_backup_items` | `id INTEGER` | `backup_id` → `program_backups` CASCADE | `utils/program_backup.py:23` |

## DatabaseHandler pattern (required for all DB access)
```python
from utils.database import DatabaseHandler
with DatabaseHandler() as db:
    rows = db.fetch_all("SELECT ... WHERE col = ?", (value,))    # list[dict]
    row = db.fetch_one("SELECT ... WHERE id = ?", (id,))         # dict | None
    db.execute_query("INSERT INTO t (c) VALUES (?)", (val,))     # write (locks)
```
Slow queries (>100ms) auto-logged as WARNING (`database.py:250`).

## Adding a DB table — five places
1. Write creation function in `utils/database.py`:
```python
def add_myfeature_table() -> None:
    with DatabaseHandler() as db:
        db.execute_query("""CREATE TABLE IF NOT EXISTS myfeature (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ...
        )""")
```
2. Call in `app.py` startup block (after line 52, alongside other `add_*` calls)
3. Call in `tests/conftest.py` → `app` fixture `with app.app_context():` block (line 107-112)
4. Call in `tests/conftest.py` → `erase_data()` inner function (line 92-97)
5. If FK to an existing table: add child name to drop-order list in `erase_data` and `clean_db` fixture

## Connection config (`utils/database.py:80-104`)
`_configure_connection()` sets PRAGMAs per connection:
- `foreign_keys = ON` (line 84)
- `busy_timeout = 30000` (line 86)
- Journal mode: `FLASK_DEBUG` env defaults to `'1'` → `DELETE` mode; set `FLASK_DEBUG=0` for `WAL` (line 90)
- Synchronous: debug → `FULL`; non-debug → `NORMAL` (lines 99-102)

**Note:** `database.py:90` defaults `FLASK_DEBUG` to `'1'`, but `app.py:259` defaults it to `'0'`. Result: `python app.py` runs Flask non-debug, but DB uses DELETE journal + FULL sync (safe defaults).

## Thread safety
DatabaseHandler writes are locked via `_DB_LOCK` (`threading.RLock`, `database.py:24`) — see `execute_query` (line 236) and `executemany` (line 311).

## Seed database
`data/catalog.seed.db` is an immutable, physically sanitized catalog asset.
`bootstrap_runtime_database()` in `utils/catalog_seed.py` copies it atomically
to a missing configured `DB_FILE` during real `app.py` startup. Existing
databases are never replaced. The bootstrap is deliberately not called by
`DatabaseHandler`, config imports, or `run_all_initializers()`, so isolated
tests and explicit empty-schema initialization remain empty.

On corruption, `_attempt_database_recovery()` quarantines the bad file as
`*.corrupted_<timestamp>` and a fresh empty DB is created on next init.

## Runtime paths (`utils/runtime_paths.py`)
One resolver owns every mutable path. Precedence, highest first: `DB_FILE`
(database only) → `HT_RUNTIME_DIR` (whole runtime tree) → frozen per-user OS
data directory → the repository. Never derive a runtime path from `__file__`,
and never create runtime directories at import time — `get_db_connection()`
creates a missing database parent, and logging creates its own directory.

Database, backups, and logs all follow the resolver. A frozen install writes to
`%LOCALAPPDATA%\HypertrophyToolbox\` and adds nothing to its own installation
directory; a source checkout still uses `<repo>/data` and `<repo>/logs`.

`utils/runtime_migration.py::prepare_runtime_database()` runs in `app.py`
**before** `bootstrap_runtime_database()` — seeding first would create an empty
database that migration would then correctly decline to replace. It opens the
legacy database `mode=ro`, refuses when `-wal`/`-journal` sidecars are
outstanding, verifies the copy (`integrity_check`, `foreign_key_check`, row
counts) before publishing it atomically, and never deletes or writes to the
original. Any failure returns the legacy path and logs recovery steps; it never
seeds a clean database after finding real data.

## Env vars that affect DB (`utils/config.py`)
| Variable | Default | Effect |
|---|---|---|
| `DB_FILE` | `data/database.db` | SQLite path; wins over every resolved path. Tests patch `utils.config.DB_FILE` directly. |
| `HT_RUNTIME_DIR` | unset | Relocates the whole runtime tree (data + logs). Portable installs. |
| `FLASK_DEBUG` | `'0'` in `app.py:259`; `'1'` in `database.py:90` | Controls Flask debug AND journal mode |
| `TESTING` | unset | Set to `'1'` by `tests/conftest.py` for the shared pytest harness |

## Startup sequence (`app.py`)
```
app.py startup:
  prepare_runtime_database()      ← moves a legacy database to the runtime root, once
  utils.config.DB_FILE = ...      ← whatever that decided (legacy path on failure)
  bootstrap_runtime_database()    ← copies catalog seed only when DB_FILE is missing
  run_all_initializers()          ← canonical schema registry sequence
  create_startup_backup()         ← skipped for the pristine first-run seed copy
```

## Typical failures
| Symptom | Cause | Evidence |
|---|---|---|
| `database is locked` | Concurrent writes (e.g. reloader spawned 2 processes) | Check `_DB_LOCK` in `database.py:24`; disable reloader |
| Empty exercise list on fresh start | No DB backup restored | `db_initializer.py:348` |
| `FK constraint failed` | Inserting log without valid `workout_plan_id` | `db_initializer.py:257` |
