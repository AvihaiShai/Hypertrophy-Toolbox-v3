---
paths:
  - "utils/database.py"
  - "utils/db_initializer.py"
  - "utils/schema_registry.py"
  - "utils/catalog_upgrade.py"
  - "utils/config.py"
  - "utils/program_backup.py"
  - "utils/auto_backup.py"
---

# Database guide

## Schema (from `utils/db_initializer.py`)

> **This table is a quick reference, not the inventory.** The full runtime schema is **19 tables**.
> Four modules create them — `utils/db_initializer.py`, `utils/database.py`,
> `utils/program_backup.py`, `utils/catalog_upgrade.py` — and `utils/schema_registry.py` adds one
> column by `ALTER TABLE`. Field-level detail (every column, type, nullability, default, unique
> constraint, index, CHECK, and the enforced-versus-by-convention relationship split) is in
> [`docs/product/BACKEND_SCHEMA.md`](../../docs/product/BACKEND_SCHEMA.md), derived by PRAGMA from
> a freshly built database. Read that before concluding a table or column does not exist.

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

The sole Operation A infrastructure exception is `scripts/seed_worktree_snapshot.py`:
it uses Python stdlib `sqlite3` directly, a read-only source URI, online backup into
an owned temporary destination, disposable-copy validation, and no-overwrite
publication. Diagnostics are return codes and caller-captured output. It imports
no `DatabaseHandler`, application config, `get_logger()` or application startup;
those imports would change journal/log state. This exception covers worktree seeding
only, never application DB access or B–E preservation/cleanup. Automated verification
uses synthetic SQLite families in the approved standalone scratch lane. Root
`CLAUDE.md` keeps all application DatabaseHandler/logging requirements unchanged.

## Adding a DB table — three places

Every schema build goes through one registry, `run_all_initializers()` in
`utils/schema_registry.py`: `init_runtime()` (`utils/runtime_init.py`) on startup
(`force_base=False`), `erase_data()` in `app.py` (`force_base=True`), and the test suite's
`schema_template` in `tests/conftest.py` (`force_base=True`). Neither `app.py` nor
`tests/conftest.py` calls an `add_*_table()` function directly. Root `CLAUDE.md` §2 states the
current model.

1. Write creation function in `utils/database.py`:
```python
def add_myfeature_table() -> None:
    with DatabaseHandler() as db:
        db.execute_query("""CREATE TABLE IF NOT EXISTS myfeature (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ...
        )""")
```
2. Add it to `run_all_initializers()` in `utils/schema_registry.py`; startup, erase and the test
   `schema_template` all pick it up from there.
3. If it holds user state: add the table name to `OWNED_TABLES_DROP_ORDER` in FK-safe order
   (children before parents) — `erase_data()` drops through it — and to the `clean_db` fixture's
   `DELETE` list in `tests/conftest.py`.

## Connection config (`utils/database.py:80-104`)
`_configure_connection()` sets PRAGMAs per connection:
- `foreign_keys = ON` (line 84)
- `busy_timeout = 30000` (line 86)
- Journal mode: `FLASK_DEBUG` env defaults to `'1'` → `DELETE` mode; set `FLASK_DEBUG=0` for `WAL` (line 90)
- Synchronous: debug → `FULL`; non-debug → `NORMAL` (lines 99-102)

**Note:** `database.py:90` defaults `FLASK_DEBUG` to `'1'`, but `main()` in `app.py` defaults it to `'0'`. Result: `python app.py` runs Flask non-debug, but DB uses DELETE journal + FULL sync (safe defaults).

## Thread safety
DatabaseHandler writes are locked via `_DB_LOCK` (`threading.RLock`, `database.py:24`) — see `execute_query` (line 236) and `executemany` (line 311).

## Seed database
`data/catalog.seed.db` is an immutable, physically sanitized catalog asset.
`bootstrap_runtime_database()` in `utils/catalog_seed.py` copies it atomically
to a missing configured `DB_FILE` during `init_runtime()`. Existing
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

`utils/runtime_migration.py::prepare_runtime_database()` runs in `init_runtime()`
**before** `bootstrap_runtime_database()` — seeding first would create an empty
database that migration would then correctly decline to replace. It opens the
legacy database `mode=ro`, refuses when `-wal`/`-journal` sidecars are
outstanding, verifies the copy (`integrity_check`, `foreign_key_check`, row
counts) before publishing it atomically, and never deletes or writes to the
original. Any failure returns the legacy path and logs recovery steps; it never
seeds a clean database after finding real data.

## Catalog upgrades (`utils/catalog_upgrade.py`)
The seed only initializes a new install. `upgrade_catalog_from_seed()` brings an
existing runtime catalog up to the shipped one and runs from `init_runtime()`
only — never from `run_all_initializers()`, which the test suite uses to build
deliberately empty schemas.

Additive and update-only. It inserts exercises the runtime database lacks
(with their isolated muscles), refreshes only `movement_pattern`,
`movement_subpattern`, `youtube_video_id`, `media_path` on existing rows, and
**never deletes or renames**. Everything else is user-owned: `save_exercise()`
lets a user rewrite an exercise's muscle groups, equipment, mechanic, and
difficulty — including on catalog exercises — and derives
`exercise_isolated_muscles` from `advanced_isolated_muscles`. A `NULL` shipped
value never overwrites a populated one.

The trigger is a SHA-256 over the shipped catalog's rows, recorded in
`catalog_version` (catalog metadata, deliberately not in
`OWNED_TABLES_DROP_ORDER`). Adding a column to `save_exercise`'s editable list
fails `tests/test_catalog_upgrade.py`.

## Env vars (`utils/config.py`)
| Variable | Default | Effect |
|---|---|---|
| `DB_FILE` | `<runtime root>/data/database.db` | SQLite path; wins over every resolved path. Tests patch `utils.config.DB_FILE` directly. |
| `HT_RUNTIME_DIR` | unset | Relocates the whole runtime tree (database, backups, logs) in one move. The supported portable-install mechanism. |
| `FLASK_DEBUG` | `'0'` in `main()` in `app.py`; `'1'` in `database.py:90` | Controls Flask debug AND journal mode |
| `FLASK_USE_RELOADER` | `'0'` | Auto-reload (off by default — avoids WAL corruption) |
| `TESTING` | unset | Set to `'1'` by `tests/conftest.py` for the shared pytest harness |
| `MAX_EXPORT_ROWS` | `1000000` | Export cap |

## Startup sequence (`init_runtime()`, `utils/runtime_init.py`)
Importing `app` does none of this. Only the entry points call `init_runtime()` —
`main()` in `app.py`, `app_launcher.main()` and `create_initialized_app()` — once per
process; a repeat with the same database and runtime root is a no-op, and a different
one raises `RuntimeError`.
```
init_runtime():
  prepare_runtime_database()      ← moves a legacy database to the runtime root, once
  utils.config.DB_FILE = ...      ← whatever that decided (legacy path on failure)
  bootstrap_runtime_database()    ← copies catalog seed only when DB_FILE is missing
  run_all_initializers(force_base=False)  ← canonical schema registry sequence
  upgrade_catalog_from_seed()     ← additive catalog refresh; skipped when the seed just ran
  create_startup_backup()         ← skipped for the pristine first-run seed copy
```
Under the reloader only the serving child of `python app.py` calls it. The per-table
`initialize_*` / `add_*_table` functions are registered in `utils/schema_registry.py`, not
called individually from `app.py`. Seeding and the catalog upgrade run **only** from
`init_runtime()`, never from `run_all_initializers()`: the test suite creates empty schemas on
purpose, and its `app` fixture is `create_app()` without `init_runtime()`.

## Typical failures
| Symptom | Cause | Evidence |
|---|---|---|
| `database is locked` | Concurrent writes (e.g. reloader spawned 2 processes) | Check `_DB_LOCK` in `database.py:24`; disable reloader |
| Empty exercise list on fresh start | No DB backup restored | `db_initializer.py:348` |
| `FK constraint failed` | Inserting log without valid `workout_plan_id` | `db_initializer.py:257` |
