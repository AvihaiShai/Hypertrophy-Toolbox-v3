"""Importing ``app`` does no data work; ``init_runtime()`` alone decides the database.

The contract has two parts (``docs/app_factory/PLANNING.md`` AC1, AC5):

* **Import** constructs one Flask app and nothing else: no ``DatabaseHandler``,
  no ``sqlite3.connect``, no database or ``auto_backup/``, and
  ``utils.config.DB_FILE`` left exactly as it was. Only ``logs/`` may appear,
  from the first ``get_logger()``.
* **Initialization** honours an explicit argument, then the environment's
  ``DB_FILE``, then the resolver. A patched ``utils.config.DB_FILE`` is never an
  input: it is overwritten by the resolved path, which is why
  ``real_app_client`` passes its scratch path explicitly.

Each probe is a fresh interpreter, because both the import and the
initialization guard are once per process. Every interpreter uses a disposable
installation for the installation-relative legacy paths and a separate scratch
directory for ``HT_RUNTIME_DIR``.
"""
import os
import shutil
from pathlib import Path

import pytest

from tests.app_factory_support import (
    OUTCOME_PROBE,
    probe_env as _probe_env,
    run_probe as _run,
    stage_probe_installation,
)
from utils.database import DatabaseHandler

# Imports app (or only its constant) in a fresh interpreter with the database
# primitives counted, and reports what the import touched. Kept as source rather
# than a helper module so what runs under the subprocess is visible at the point
# of assertion.
IMPORT_PROBE = """
import json, os, sqlite3, sys
subject, patched = sys.argv[2], sys.argv[3]
import flask
import utils.config
import utils.database
from utils.runtime_paths import runtime_database_path
counts = {"flask": 0, "database_handler": 0, "sqlite_connect": 0}
def counted(key, original):
    def wrapper(*args, **kwargs):
        counts[key] += 1
        return original(*args, **kwargs)
    return wrapper
flask.Flask.__init__ = counted("flask", flask.Flask.__init__)
utils.database.DatabaseHandler.__init__ = counted(
    "database_handler", utils.database.DatabaseHandler.__init__)
sqlite3.connect = counted("sqlite_connect", sqlite3.connect)
if patched:
    utils.config.DB_FILE = patched
before = utils.config.DB_FILE
if subject == "constant":
    from app import STATIC_LONG_MAX_AGE_SECONDS  # noqa: F401
else:
    import app  # noqa: F401
print(json.dumps({
    "counts": counts,
    "is_flask": isinstance(sys.modules["app"].app, flask.Flask),
    "db_file_before": before,
    "db_file_after": utils.config.DB_FILE,
    "env_resolved_db": os.environ.get("DB_FILE") or str(runtime_database_path()),
}))
"""


def _tree(root):
    if not root.exists():
        return set()
    return {path.relative_to(root).as_posix() for path in root.rglob("*")}


def _import_report(tmp_path, *, subject="app", patched="", env_db=None):
    sandbox = tmp_path / "rt"
    overrides = {"HT_RUNTIME_DIR": str(sandbox)}
    if env_db is not None:
        overrides["DB_FILE"] = str(env_db)
    report = _run(tmp_path, IMPORT_PROBE, subject, patched, env=_probe_env(**overrides))
    return report, sandbox


def _assert_import_did_no_data_work(report, sandbox, *, db_parent=None):
    assert report["counts"] == {"flask": 1, "database_handler": 0, "sqlite_connect": 0}
    assert report["is_flask"]
    assert report["db_file_after"] == report["db_file_before"]
    assert not Path(report["env_resolved_db"]).exists(), report["env_resolved_db"]
    assert _tree(sandbox) <= {"logs", "logs/app.log"}, sorted(_tree(sandbox))
    if db_parent is not None:
        assert not (db_parent / "auto_backup").exists()


def test_import_creates_no_data_without_db_file(tmp_path):
    report, sandbox = _import_report(tmp_path)

    _assert_import_did_no_data_work(report, sandbox)


def test_import_creates_no_data_with_missing_db_file(tmp_path):
    scratch = tmp_path / "scratch.db"
    report, sandbox = _import_report(tmp_path, env_db=scratch)

    _assert_import_did_no_data_work(report, sandbox, db_parent=tmp_path)
    assert Path(report["env_resolved_db"]) == scratch


def test_import_creates_no_data_with_patched_attribute_only(tmp_path):
    """Import preserves a patched attribute without acting on its path."""
    scratch = tmp_path / "scratch.db"
    report, sandbox = _import_report(tmp_path, patched=str(scratch))

    _assert_import_did_no_data_work(report, sandbox, db_parent=tmp_path)
    assert report["db_file_after"] == str(scratch)
    assert not scratch.exists()


def test_constant_import_creates_no_data(tmp_path):
    """``scripts/smoke_packaged_app.py`` imports only this constant, in its own
    process, with no ``DB_FILE`` (A5)."""
    report, sandbox = _import_report(tmp_path, subject="constant")

    _assert_import_did_no_data_work(report, sandbox)


def test_init_runtime_explicit_argument_lands_on_scratch(tmp_path):
    """``real_app_client``'s path: ``TESTING=1``, no environment ``DB_FILE``, an
    explicit argument. The argument is the whole decision."""
    sandbox, scratch = tmp_path / "rt", tmp_path / "scratch.db"

    report = _run(
        tmp_path, OUTCOME_PROBE, "", str(scratch),
        env=_probe_env(HT_RUNTIME_DIR=str(sandbox), TESTING="1"),
    )

    assert report["migration_action"] == "explicit-override"
    assert Path(report["active_db"]).resolve() == scratch.resolve()
    assert Path(report["database_path"]) == scratch
    assert report["seeded"] is True and scratch.exists()
    assert not (sandbox / "data" / "database.db").exists()


@pytest.mark.parametrize(
    "legacy_present", [False, True], ids=["fresh-install", "legacy-install"],
)
def test_init_runtime_ignores_patched_attribute(tmp_path, legacy_present):
    """With no environment ``DB_FILE``, initialization uses the runtime path
    and overwrites a patched config attribute (A4). The scratch path is never
    created.
    """
    sandbox, scratch = tmp_path / "rt", tmp_path / "scratch.db"
    runtime_db = sandbox / "data" / "database.db"
    installation = stage_probe_installation(tmp_path)
    legacy = installation / "data" / "database.db"
    exercise = ("Runtime migration probe exercise", "Chest")
    if legacy_present:
        shutil.copyfile(legacy.with_name("catalog.seed.db"), legacy)
        with DatabaseHandler(str(legacy)) as db:
            db.execute_query(
                "INSERT INTO exercises (exercise_name, primary_muscle_group) VALUES (?, ?)",
                exercise,
            )

    report = _run(
        tmp_path, OUTCOME_PROBE, str(scratch), "",
        env=_probe_env(HT_RUNTIME_DIR=str(sandbox)),
        installation=installation,
    )

    assert Path(report["active_db"]).resolve() == runtime_db.resolve()
    assert Path(report["database_path"]) == runtime_db
    assert runtime_db.is_file()
    assert not scratch.exists()
    assert report["migration_action"] == ("migrated" if legacy_present else "no-legacy")
    assert report["seeded"] is (not legacy_present)
    assert legacy.is_file() is legacy_present
    with DatabaseHandler(str(runtime_db)) as db:
        rows = db.fetch_all(
            "SELECT exercise_name, primary_muscle_group FROM exercises WHERE exercise_name = ?",
            (exercise[0],),
        )
    expected = {"exercise_name": exercise[0], "primary_muscle_group": exercise[1]}
    assert rows == ([expected] if legacy_present else [])


def test_init_runtime_with_env_db_file(tmp_path):
    sandbox, scratch = tmp_path / "rt", tmp_path / "scratch.db"

    report = _run(
        tmp_path, OUTCOME_PROBE, "", "",
        env=_probe_env(HT_RUNTIME_DIR=str(sandbox), DB_FILE=str(scratch)),
    )

    assert report["migration_action"] == "explicit-override"
    assert Path(report["active_db"]).resolve() == scratch.resolve()
    assert scratch.exists()
    assert not (sandbox / "data" / "database.db").exists()


@pytest.mark.parametrize('mode', ['patch-config-too', 'env-only'])
def test_env_override_wins_regardless_of_config_patch(tmp_path, mode):
    """``DB_FILE`` in the environment is what decides the path; a patched module
    attribute pointing elsewhere is not even consulted."""
    sandbox, scratch, decoy = tmp_path / "rt", tmp_path / "scratch.db", tmp_path / "decoy.db"

    report = _run(
        tmp_path, OUTCOME_PROBE, str(decoy) if mode == 'patch-config-too' else "", "",
        env=_probe_env(HT_RUNTIME_DIR=str(sandbox), DB_FILE=str(scratch), TESTING="1"),
    )

    assert Path(report["active_db"]).resolve() == scratch.resolve()
    assert not (sandbox / "data" / "database.db").exists()
    assert not decoy.exists()


def test_real_app_client_lands_on_its_scratch_database(real_app_client, tmp_path_factory):
    """In-process counterpart: whatever import order produced this client, the
    active database is the fixture's scratch file and not a runtime one."""
    import utils.config

    active = Path(utils.config.DB_FILE).resolve()
    runtime_root = Path(os.environ["HT_RUNTIME_DIR"]).resolve()
    assert active == Path(os.environ["DB_FILE"]).resolve()
    assert active.name == "database.db"
    assert active.is_file()
    assert active.parent.parent == tmp_path_factory.getbasetemp().resolve()
    assert runtime_root / "data" / "database.db" != active
