"""Contracts for ``utils/runtime_init.py``: the one guarded runtime initialization.

WS3 moved the five startup steps out of ``app.py``'s module body
(``docs/app_factory/PLANNING.md`` Plan v2 §V6). These pin what the move must
preserve -- the step order and fresh-seed skip -- and what the guard adds:
same key is a no-op, a different key raises, a failure leaves the guard unset,
``TESTING=1`` without a path refuses, and only tests may reset it.

In-process tests mock the steps by patching the names ``utils.runtime_init``
imports. Anything that needs real files runs in a fresh interpreter on a
scratch tree, because the guard is process-global.
"""
from __future__ import annotations

import ast
import dataclasses
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

import utils.config
import utils.runtime_init as runtime_init
import utils.runtime_migration as runtime_migration
from utils.catalog_seed import bootstrap_runtime_database, resolve_catalog_seed_path
from utils.runtime_migration import MigrationOutcome
from utils.schema_registry import OWNED_TABLES_DROP_ORDER

ROOT = Path(__file__).resolve().parents[1]

MIGRATION_ACTIONS = (
    "explicit-override",
    "same-path",
    "already-present",
    "no-legacy",
    "migrated",
    "failed",
)
OUTCOME_FIELDS = {
    "database_path",
    "migration_action",
    "seeded",
    "snapshot_path",
    "already_initialized",
}
_ISOLATED_ENV = ("DB_FILE", "HT_RUNTIME_DIR", "TESTING")

# (step name, positional args, keyword args, utils.config.DB_FILE at the call)
Call = tuple[str, tuple[object, ...], dict[str, object], str]


@pytest.fixture(autouse=True)
def isolated_runtime_init(monkeypatch, tmp_path):
    """Every test starts with an unset guard and a scratch runtime root.

    The guard and ``utils.config.DB_FILE`` are process-global, so a leak from
    here would change what every later module in this worker initializes.
    Teardown therefore proves the restore instead of trusting it.
    """
    saved_attribute = utils.config.DB_FILE
    saved_env = {name: os.environ.get(name) for name in _ISOLATED_ENV}

    monkeypatch.setattr(utils.config, "DB_FILE", str(tmp_path / "sentinel.db"))
    monkeypatch.delenv("DB_FILE", raising=False)
    monkeypatch.setenv("HT_RUNTIME_DIR", str(tmp_path / "rt"))
    monkeypatch.setenv("TESTING", "1")
    runtime_init._reset_for_tests()
    yield
    runtime_init._reset_for_tests()
    monkeypatch.undo()

    assert utils.config.DB_FILE == saved_attribute
    assert {name: os.environ.get(name) for name in _ISOLATED_ENV} == saved_env


def _install_steps(
    monkeypatch,
    database: Path,
    *,
    action: str = "explicit-override",
    overrides: dict[str, Callable[[], object]] | None = None,
) -> list[Call]:
    """Replace the five steps with recorders; ``overrides`` supplies results."""
    results: dict[str, Callable[[], object]] = {
        "prepare_runtime_database": lambda: MigrationOutcome(action, database),
        "bootstrap_runtime_database": lambda: False,
        "run_all_initializers": lambda: None,
        "upgrade_catalog_from_seed": lambda: None,
        "create_startup_backup": lambda: None,
    }
    results.update(overrides or {})
    calls: list[Call] = []

    def recorder(name: str, result: Callable[[], object]) -> Callable[..., object]:
        def step(*args: object, **kwargs: object) -> object:
            calls.append((name, args, kwargs, utils.config.DB_FILE))
            return result()
        return step

    for name, result in results.items():
        monkeypatch.setattr(runtime_init, name, recorder(name, result))
    return calls


def _names(calls: list[Call]) -> list[str]:
    return [call[0] for call in calls]


def _sequence(*values: object) -> Callable[[], object]:
    """A step result that yields ``values`` in turn; exceptions are raised."""
    remaining = list(values)

    def result() -> object:
        value = remaining.pop(0)
        if isinstance(value, BaseException):
            raise value
        return value
    return result


def _probe_env(**overrides: str) -> dict[str, str]:
    env = {
        name: value for name, value in os.environ.items()
        if name not in ("TESTING", "DB_FILE") and not name.startswith("HT_")
    }
    env.update(overrides)
    return env


def _run_python(tmp_path: Path, args: list[str], env: dict[str, str]) -> str:
    result = subprocess.run(
        [sys.executable, *args],
        capture_output=True, text=True, env=env, cwd=str(tmp_path), timeout=300,
    )
    assert result.returncode == 0, f"probe failed:\n{result.stdout}\n{result.stderr}"
    return result.stdout


def _snapshots(directory: Path) -> list[Path]:
    return sorted((directory / "auto_backup").glob("database_*.db"))


# --- AC2: outcome and boundary -------------------------------------------------


@pytest.mark.parametrize("action", MIGRATION_ACTIONS)
def test_outcome_fields(monkeypatch, tmp_path, action):
    """Every migration action reaches the outcome unchanged.

    The database already exists for each case, so the real seed bootstrap
    declines -- the ``failed`` case's legacy file in particular, which is why a
    failed migration never seeds over real data.
    """
    database = tmp_path / ("legacy.db" if action == "failed" else "database.db")
    database.write_bytes(b"")
    snapshot = tmp_path / "auto_backup" / "database_20260101_000000.db"
    _install_steps(
        monkeypatch, database, action=action,
        overrides={"create_startup_backup": lambda: snapshot},
    )
    monkeypatch.setattr(
        runtime_init, "bootstrap_runtime_database", bootstrap_runtime_database
    )
    monkeypatch.delenv("TESTING")

    if action == "explicit-override":
        outcome = runtime_init.init_runtime(db_file=str(database))
    else:
        outcome = runtime_init.init_runtime()

    assert {field.name for field in dataclasses.fields(outcome)} == OUTCOME_FIELDS
    assert outcome.database_path == database
    assert outcome.migration_action == action
    assert outcome.seeded is False
    assert outcome.snapshot_path == snapshot
    assert outcome.already_initialized is False
    assert utils.config.DB_FILE == str(database)


def test_module_imports_no_routes_or_app():
    tree = ast.parse((ROOT / "utils" / "runtime_init.py").read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)

    forbidden = {name for name in imported if name.split(".")[0] in ("app", "app_launcher", "routes")}
    assert not forbidden, f"utils/runtime_init.py imports {sorted(forbidden)}"


def test_importing_runtime_init_loads_no_app_or_routes(tmp_path):
    """The AST test misses transitive imports; a fresh interpreter does not.

    ``flask`` may load transitively (``utils/logger.py`` imports it), so only
    the application layers are checked.
    """
    probe = (
        "import json, sys; sys.path.insert(0, sys.argv[1]); "
        "import utils.runtime_init; "
        "print(json.dumps(sorted(m for m in sys.modules "
        "if m in ('app', 'app_launcher', 'routes') or m.startswith('routes.'))))"
    )
    stdout = _run_python(
        tmp_path, ["-c", probe, str(ROOT)],
        _probe_env(HT_RUNTIME_DIR=str(tmp_path / "rt")),
    )

    assert json.loads(stdout.strip().splitlines()[-1]) == []


# --- AC3: the guard ------------------------------------------------------------


@pytest.mark.parametrize("second_call", ["same-argument", "path-object", "env-db-file"])
def test_same_key_is_a_noop(monkeypatch, tmp_path, second_call):
    database = tmp_path / "database.db"
    snapshot = tmp_path / "auto_backup" / "database_20260101_000000.db"
    calls = _install_steps(
        monkeypatch, database, overrides={"create_startup_backup": lambda: snapshot}
    )
    first = runtime_init.init_runtime(db_file=str(database))
    steps_after_first = len(calls)

    if second_call == "same-argument":
        again = runtime_init.init_runtime(db_file=str(database))
    elif second_call == "path-object":
        again = runtime_init.init_runtime(db_file=database)
    else:
        monkeypatch.setenv("DB_FILE", str(database))
        again = runtime_init.init_runtime()

    assert again.already_initialized is True
    assert dataclasses.replace(again, already_initialized=False) == first
    assert len(calls) == steps_after_first, "a no-op re-ran a step"


def test_different_database_raises_and_changes_nothing(monkeypatch, tmp_path):
    first, other = tmp_path / "first.db", tmp_path / "other.db"
    calls = _install_steps(monkeypatch, first)
    runtime_init.init_runtime(db_file=str(first))
    steps_after_first = len(calls)

    with pytest.raises(RuntimeError):
        runtime_init.init_runtime(db_file=str(other))

    assert len(calls) == steps_after_first
    assert utils.config.DB_FILE == str(first)
    assert not other.exists()


def test_different_runtime_root_raises(monkeypatch, tmp_path):
    database = tmp_path / "database.db"
    calls = _install_steps(monkeypatch, database)
    runtime_init.init_runtime(db_file=str(database))
    steps_after_first = len(calls)

    monkeypatch.setenv("HT_RUNTIME_DIR", str(tmp_path / "rt2"))
    with pytest.raises(RuntimeError):
        runtime_init.init_runtime(db_file=str(database))

    assert len(calls) == steps_after_first
    assert utils.config.DB_FILE == str(database)


def test_failed_call_leaves_guard_unset(monkeypatch, tmp_path):
    database = tmp_path / "database.db"
    calls = _install_steps(
        monkeypatch, database,
        overrides={"run_all_initializers": _sequence(RuntimeError("schema"), None)},
    )

    with pytest.raises(RuntimeError, match="schema"):
        runtime_init.init_runtime(db_file=str(database))
    retried = runtime_init.init_runtime(db_file=str(database))

    assert retried.already_initialized is False
    assert _names(calls).count("prepare_runtime_database") == 2
    assert _names(calls).count("run_all_initializers") == 2


def test_migration_exception_propagates_and_leaves_guard_unset(monkeypatch, tmp_path):
    """A failure inside the real migration reaches the caller [AR-4].

    ``copy_legacy_backups()`` runs after the verified copy is published, so
    its exception escapes ``prepare_runtime_database()`` even though that
    function's docstring says it never raises (GA-8). The retry then finds the
    published database and proceeds.
    """
    target = tmp_path / "rt" / "data" / "database.db"
    legacy = tmp_path / "legacy.db"
    with sqlite3.connect(legacy) as connection:
        connection.execute("CREATE TABLE marker (id INTEGER PRIMARY KEY)")
        connection.execute("INSERT INTO marker DEFAULT VALUES")
    connection.close()

    monkeypatch.delenv("TESTING")
    monkeypatch.setattr(runtime_migration, "runtime_database_path", lambda: target)
    monkeypatch.setattr(runtime_migration, "legacy_database_path", lambda: legacy)

    def copy_fails() -> int:
        raise OSError("backup copy failed")

    monkeypatch.setattr(runtime_migration, "copy_legacy_backups", copy_fails)
    calls = _install_steps(monkeypatch, target)
    monkeypatch.setattr(
        runtime_init, "prepare_runtime_database", runtime_migration.prepare_runtime_database
    )
    sentinel = utils.config.DB_FILE

    with pytest.raises(OSError, match="backup copy failed"):
        runtime_init.init_runtime()
    assert calls == []
    assert utils.config.DB_FILE == sentinel
    assert target.is_file(), "the migration did not publish before the exception"

    monkeypatch.setattr(runtime_migration, "copy_legacy_backups", lambda: 0)
    retried = runtime_init.init_runtime()

    assert retried.already_initialized is False
    assert retried.migration_action == "already-present"
    assert retried.database_path == target
    assert _names(calls)[0] == "bootstrap_runtime_database"


def test_retry_after_seed_skips_upgrade_and_backup(monkeypatch, tmp_path):
    """The first attempt seeded and then failed; the retry sees an existing file
    but must still treat it as a fresh seed (4c)."""
    database = tmp_path / "database.db"
    calls = _install_steps(
        monkeypatch, database,
        overrides={
            "bootstrap_runtime_database": _sequence(True, False),
            "run_all_initializers": _sequence(RuntimeError("schema"), None),
        },
    )

    with pytest.raises(RuntimeError, match="schema"):
        runtime_init.init_runtime(db_file=str(database))
    retried = runtime_init.init_runtime(db_file=str(database))

    assert retried.seeded is True
    assert retried.snapshot_path is None
    assert "upgrade_catalog_from_seed" not in _names(calls)
    assert "create_startup_backup" not in _names(calls)


def test_testing_without_path_refuses_before_any_step(monkeypatch, tmp_path):
    database = tmp_path / "database.db"
    calls = _install_steps(monkeypatch, database)
    sentinel = utils.config.DB_FILE

    with pytest.raises(RuntimeError, match="unset TESTING"):
        runtime_init.init_runtime()

    assert calls == []
    assert utils.config.DB_FILE == sentinel
    assert not (tmp_path / "rt").exists()

    # An environment DB_FILE is an explicit path, so the same call now runs.
    monkeypatch.setenv("DB_FILE", str(database))
    assert runtime_init.init_runtime().already_initialized is False
    assert _names(calls)[0] == "prepare_runtime_database"


def test_reset_allows_a_different_key(monkeypatch, tmp_path):
    first, other = tmp_path / "first.db", tmp_path / "other.db"
    _install_steps(monkeypatch, first)
    runtime_init.init_runtime(db_file=str(first))

    runtime_init._reset_for_tests()
    _install_steps(monkeypatch, other)
    outcome = runtime_init.init_runtime(db_file=str(other))

    assert outcome.already_initialized is False
    assert utils.config.DB_FILE == str(other)


def test_reset_is_never_referenced_by_production_code():
    candidates = [ROOT / "app.py", ROOT / "app_launcher.py"]
    for package in ("utils", "routes", "scripts"):
        candidates.extend(sorted((ROOT / package).rglob("*.py")))
    scanned = [path for path in candidates if path != ROOT / "utils" / "runtime_init.py"]
    assert ROOT / "app.py" in scanned and len(scanned) > 50, "the scan found nothing to check"

    offenders = [
        path.relative_to(ROOT).as_posix() for path in scanned
        if "_reset_for_tests" in path.read_text(encoding="utf-8", errors="replace")
    ]
    assert offenders == []


SNAPSHOT_PROBE = """
import json, sys
sys.path.insert(0, sys.argv[1])
from utils.runtime_init import init_runtime
first = init_runtime(db_file=sys.argv[2])
second = init_runtime(db_file=sys.argv[2])
print(json.dumps({
    "first": None if first.snapshot_path is None else str(first.snapshot_path),
    "second": None if second.snapshot_path is None else str(second.snapshot_path),
    "second_already_initialized": second.already_initialized,
}))
"""


def test_second_call_takes_no_second_snapshot_subprocess(tmp_path):
    """Outside TESTING a real snapshot is taken, so a repeat would be visible."""
    database = tmp_path / "database.db"
    shutil.copyfile(resolve_catalog_seed_path(), database)

    stdout = _run_python(
        tmp_path, ["-c", SNAPSHOT_PROBE, str(ROOT), str(database)],
        _probe_env(HT_RUNTIME_DIR=str(tmp_path / "rt")),
    )
    report = json.loads(stdout.strip().splitlines()[-1])

    snapshots = _snapshots(tmp_path)
    assert len(snapshots) == 1, snapshots
    assert report["first"] is not None and Path(report["first"]).resolve() == snapshots[0].resolve()
    assert report["second_already_initialized"] is True
    assert report["second"] == report["first"]


# --- AC5b / AC5d ---------------------------------------------------------------


def test_explicit_argument_wins(monkeypatch, tmp_path):
    """The argument beats an environment ``DB_FILE`` through the real migration
    decision; the later steps all see the argument."""
    explicit, from_env = tmp_path / "explicit.db", tmp_path / "from_env.db"
    monkeypatch.setenv("DB_FILE", str(from_env))
    calls = _install_steps(monkeypatch, explicit)
    monkeypatch.setattr(
        runtime_init, "prepare_runtime_database", runtime_migration.prepare_runtime_database
    )

    outcome = runtime_init.init_runtime(db_file=str(explicit))

    assert outcome.migration_action == "explicit-override"
    assert outcome.database_path == explicit
    assert utils.config.DB_FILE == str(explicit)
    assert calls and all(call[3] == str(explicit) for call in calls)
    assert not from_env.exists()


OUTCOME_PROBE = """
import json, sys
sys.path.insert(0, sys.argv[1])
from utils.runtime_init import init_runtime
outcome = init_runtime(db_file=sys.argv[2])
print(json.dumps({
    "database_path": str(outcome.database_path),
    "migration_action": outcome.migration_action,
    "seeded": outcome.seeded,
    "snapshot_path": None if outcome.snapshot_path is None else str(outcome.snapshot_path),
    "already_initialized": outcome.already_initialized,
}))
"""


def test_init_runtime_upgrades_old_schema_database(tmp_path):
    """An existing pre-migration database is upgraded in place, not reseeded.

    The snapshot expectation depends on the catalog upgrade lifting the
    exercise count to at least 100 (``utils/auto_backup.py``); if only that
    assertion is red, read the auto-backup log lines before changing anything.
    """
    database = tmp_path / "old.db"
    env = _probe_env(HT_RUNTIME_DIR=str(tmp_path / "rt"))
    _run_python(
        tmp_path,
        [str(ROOT / "tests" / "fixtures" / "make_old_schema_db.py"), "--output", str(database)],
        env,
    )

    stdout = _run_python(tmp_path, ["-c", OUTCOME_PROBE, str(ROOT), str(database)], env)
    report = json.loads(stdout.strip().splitlines()[-1])

    assert report["migration_action"] == "explicit-override"
    assert Path(report["database_path"]).resolve() == database.resolve()
    assert report["seeded"] is False
    assert report["already_initialized"] is False

    with sqlite3.connect(database) as connection:
        tables = {
            row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        columns = {row[1] for row in connection.execute("PRAGMA table_info(user_selection)")}
        catalog_versions = connection.execute("SELECT COUNT(*) FROM catalog_version").fetchone()[0]
        exercises = connection.execute("SELECT COUNT(*) FROM exercises").fetchone()[0]
        legacy_rows = connection.execute(
            "SELECT routine, exercise FROM user_selection WHERE routine = 'Legacy Routine'"
        ).fetchall()
    connection.close()

    assert set(OWNED_TABLES_DROP_ORDER) | {"exercises", "catalog_version"} <= tables
    assert "exercise_order" in columns
    assert catalog_versions >= 1
    assert legacy_rows == [("Legacy Routine", "Legacy Bench Press")]
    assert exercises >= 100

    snapshots = _snapshots(tmp_path)
    assert len(snapshots) == 1, snapshots
    assert report["snapshot_path"] is not None
    assert Path(report["snapshot_path"]).resolve() == snapshots[0].resolve()


# --- AC7: reloader rule --------------------------------------------------------


@pytest.mark.parametrize(
    ("use_reloader", "serving_child", "expected"),
    [
        (False, False, True),
        (False, True, True),
        (True, False, False),
        (True, True, True),
    ],
)
def test_should_initialize_runtime_matrix(monkeypatch, use_reloader, serving_child, expected):
    """Only the reloader's monitoring parent skips; Werkzeug marks the serving
    child with ``WERKZEUG_RUN_MAIN=true``."""
    if serving_child:
        monkeypatch.setenv("WERKZEUG_RUN_MAIN", "true")
    else:
        monkeypatch.delenv("WERKZEUG_RUN_MAIN", raising=False)

    assert runtime_init.should_initialize_runtime(use_reloader) is expected
