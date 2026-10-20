"""Importing ``app`` does no data work; ``init_runtime()`` alone decides the database.

Before WS3, ``app.py``'s module body ran the whole runtime startup, so these
tests pinned where a *first import* landed -- including the defect that a
patched ``utils.config.DB_FILE`` was discarded. WS3 (``docs/app_factory/
PLANNING.md`` AC1, AC5) moved that startup into ``utils.runtime_init.
init_runtime()``, and the contract split in two:

* **Import** constructs one Flask app and nothing else: no ``DatabaseHandler``,
  no ``sqlite3.connect``, no database or ``auto_backup/``, and
  ``utils.config.DB_FILE`` left exactly as it was. Only ``logs/`` may appear,
  from the first ``get_logger()``.
* **Initialization** honours an explicit argument, then the environment's
  ``DB_FILE``, then the resolver. A patched ``utils.config.DB_FILE`` is never an
  input: it is overwritten by the resolved path, which is why
  ``real_app_client`` passes its scratch path explicitly.

Each probe is a fresh interpreter, because both the import and the
initialization guard are once per process. ``HT_RUNTIME_DIR`` points every
probe at a throwaway sandbox.

``HT_RUNTIME_DIR`` does **not** relocate the *legacy* source path, though:
``legacy_data_dir()`` is installation-relative, so a run without ``DB_FILE``
still reads the repository's own ``data/database.db`` when deciding whether to
migrate. It opens that file read-only and never deletes it, but if unresolved
``-wal``/``-journal`` sidecars make the migration refuse, it returns the legacy
path -- and initialization would then write to the developer's real database.
``_skip_if_legacy_database_is_busy`` refuses to run in that state rather than
write to it. The import probes keep the skip too: on a tree where import still
initializes, they would take the same path.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

# Imports app (or only its constant) in a fresh interpreter with the database
# primitives counted, and reports what the import touched. Kept as source rather
# than a helper module so what runs under the subprocess is visible at the point
# of assertion.
IMPORT_PROBE = """
import json, os, sqlite3, sys
sys.path.insert(0, sys.argv[1])
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

# Calls init_runtime() in a fresh interpreter and reports where it landed.
INIT_PROBE = """
import json, os, sys
sys.path.insert(0, sys.argv[1])
patched, explicit = sys.argv[2], sys.argv[3]
import utils.config
if patched:
    utils.config.DB_FILE = patched
from utils.runtime_init import init_runtime
outcome = init_runtime(db_file=explicit) if explicit else init_runtime()
print(json.dumps({
    "active_db": os.path.abspath(utils.config.DB_FILE),
    "database_path": str(outcome.database_path),
    "migration_action": outcome.migration_action,
    "seeded": outcome.seeded,
}))
"""


def _skip_if_legacy_database_is_busy():
    """Refuse a no-``DB_FILE`` probe when it could reach the real database.

    With no ``DB_FILE`` override, ``prepare_runtime_database()`` inspects the
    repository's own database, and an outstanding SQLite sidecar makes it
    decline the migration and hand back the legacy path. Skipping is the honest
    outcome -- the alternative is a test that writes to a developer's live data
    to prove a point about isolation.
    """
    legacy = ROOT / 'data' / 'database.db'
    busy = [
        suffix for suffix in ('-wal', '-shm', '-journal')
        if Path(f"{legacy}{suffix}").exists()
    ]
    if busy:
        pytest.skip(
            f"{legacy.name} has outstanding {', '.join(busy)} sidecars; the "
            "no-DB_FILE case would fall back to the real database"
        )


def _probe_env(**overrides):
    env = {
        name: value for name, value in os.environ.items()
        if name not in ("TESTING", "DB_FILE") and not name.startswith("HT_")
    }
    env.update(overrides)
    return env


def _run(tmp_path, probe, *args, env):
    result = subprocess.run(
        [sys.executable, "-c", probe, str(ROOT), *args],
        capture_output=True, text=True, env=env, cwd=str(tmp_path), timeout=300,
    )
    assert result.returncode == 0, f"probe failed:\n{result.stdout}\n{result.stderr}"
    return json.loads(result.stdout.strip().splitlines()[-1])


def _checkout_data_state():
    """What a probe could create under the checkout's ``data/``.

    Only those paths: the checkout may already hold a ``database.db`` from
    earlier tests, so the comparison is before/after, never "absent".
    """
    data = ROOT / "data"
    state = {}
    for path in sorted(data.glob("database.db*")):
        stat = path.stat()
        state[path.name] = (stat.st_size, stat.st_mtime_ns)
    backups = data / "auto_backup"
    if backups.exists():
        state["auto_backup/"] = (
            backups.stat().st_mtime_ns, tuple(sorted(p.name for p in backups.iterdir()))
        )
    return state


def _tree(root):
    if not root.exists():
        return set()
    return {path.relative_to(root).as_posix() for path in root.rglob("*")}


def _import_report(tmp_path, *, subject="app", patched="", env_db=None):
    sandbox = tmp_path / "rt"
    overrides = {"HT_RUNTIME_DIR": str(sandbox)}
    if env_db is not None:
        overrides["DB_FILE"] = str(env_db)
    before = _checkout_data_state()

    report = _run(tmp_path, IMPORT_PROBE, subject, patched, env=_probe_env(**overrides))

    assert _checkout_data_state() == before, "the import touched the checkout's data/"
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
    _skip_if_legacy_database_is_busy()
    report, sandbox = _import_report(tmp_path)

    _assert_import_did_no_data_work(report, sandbox)


def test_import_creates_no_data_with_missing_db_file(tmp_path):
    scratch = tmp_path / "scratch.db"
    report, sandbox = _import_report(tmp_path, env_db=scratch)

    _assert_import_did_no_data_work(report, sandbox, db_parent=tmp_path)
    assert Path(report["env_resolved_db"]) == scratch


def test_import_creates_no_data_with_patched_attribute_only(tmp_path):
    """The case the old negative test pinned: a patched attribute with no
    environment override. Import must neither discard it nor act on it."""
    _skip_if_legacy_database_is_busy()
    scratch = tmp_path / "scratch.db"
    report, sandbox = _import_report(tmp_path, patched=str(scratch))

    _assert_import_did_no_data_work(report, sandbox, db_parent=tmp_path)
    assert report["db_file_after"] == str(scratch)
    assert not scratch.exists()


def test_constant_import_creates_no_data(tmp_path):
    """``scripts/smoke_packaged_app.py`` imports only this constant, in its own
    process, with no ``DB_FILE`` (A5)."""
    _skip_if_legacy_database_is_busy()
    report, sandbox = _import_report(tmp_path, subject="constant")

    _assert_import_did_no_data_work(report, sandbox)


def test_init_runtime_explicit_argument_lands_on_scratch(tmp_path):
    """``real_app_client``'s path: ``TESTING=1``, no environment ``DB_FILE``, an
    explicit argument. The argument is the whole decision."""
    sandbox, scratch = tmp_path / "rt", tmp_path / "scratch.db"
    before = _checkout_data_state()

    report = _run(
        tmp_path, INIT_PROBE, "", str(scratch),
        env=_probe_env(HT_RUNTIME_DIR=str(sandbox), TESTING="1"),
    )

    assert report["migration_action"] == "explicit-override"
    assert Path(report["active_db"]).resolve() == scratch.resolve()
    assert Path(report["database_path"]) == scratch
    assert report["seeded"] is True and scratch.exists()
    assert not (sandbox / "data" / "database.db").exists()
    assert _checkout_data_state() == before


def test_init_runtime_ignores_patched_attribute(tmp_path):
    """Replaces ``test_patching_config_alone_is_not_isolation`` (A4).

    That test pinned import-time startup discarding a patched attribute. The
    attribute is still not an input, but now by contract: with no environment
    ``DB_FILE``, production-mode initialization resolves the runtime database
    and overwrites the patch. The scratch path is never created.
    """
    _skip_if_legacy_database_is_busy()
    sandbox, scratch = tmp_path / "rt", tmp_path / "scratch.db"
    runtime_db = sandbox / "data" / "database.db"
    before = _checkout_data_state()

    report = _run(
        tmp_path, INIT_PROBE, str(scratch), "",
        env=_probe_env(HT_RUNTIME_DIR=str(sandbox)),
    )

    assert Path(report["active_db"]).resolve() == runtime_db.resolve()
    assert runtime_db.exists()
    assert not scratch.exists()
    assert report["migration_action"] in {"no-legacy", "migrated"}
    assert _checkout_data_state() == before


def test_init_runtime_with_env_db_file(tmp_path):
    sandbox, scratch = tmp_path / "rt", tmp_path / "scratch.db"

    report = _run(
        tmp_path, INIT_PROBE, "", "",
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
        tmp_path, INIT_PROBE, str(decoy) if mode == 'patch-config-too' else "", "",
        env=_probe_env(HT_RUNTIME_DIR=str(sandbox), DB_FILE=str(scratch), TESTING="1"),
    )

    assert Path(report["active_db"]).resolve() == scratch.resolve()
    assert not (sandbox / "data" / "database.db").exists()
    assert not decoy.exists()


def test_real_app_client_lands_on_its_scratch_database(real_app_client):
    """In-process counterpart: whatever import order produced this client, the
    active database is the fixture's scratch file and not a runtime one."""
    import utils.config

    active = Path(utils.config.DB_FILE).resolve()
    assert active.name == 'database.db'
    assert active.exists()
    # pytest's tmp_path_factory roots everything under a "pytest-of-<user>" dir;
    # a runtime or checkout database would never be under it.
    assert any(part.startswith('pytest-') for part in active.parts), (
        f"active database is not under a pytest temp root: {active}"
    )
    assert ROOT / 'data' / 'database.db' != active
