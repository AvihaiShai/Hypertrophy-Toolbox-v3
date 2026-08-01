"""``real_app_client``'s isolation must hold on a *first* import of ``app``.

The in-process tests cannot prove this. By the time any of them run, some other
module has usually imported ``app`` already, so its startup is a cached no-op and
the dangerous path never executes. Only a fresh interpreter re-runs
``app.py``'s module-level startup, which is where the database path is decided.

What the startup actually does (``app.py``):

    migration = prepare_runtime_database()
    utils.config.DB_FILE = str(migration.database_path)

``prepare_runtime_database()`` takes its ``explicit-override`` branch only when
``os.environ['DB_FILE']`` is set (``utils/runtime_migration.py``). Patching
``utils.config.DB_FILE`` alone is therefore discarded by that reassignment, and a
first import resolves the **real runtime database** — in a source checkout, the
repository's own ``data/database.db``.

These tests spawn a subprocess so the startup genuinely re-runs. Each one also
sets ``HT_RUNTIME_DIR`` to a throwaway sandbox, which relocates the runtime tree
(database, backups, logs) and gives the negative case a concrete runtime path to
assert was never created.

``HT_RUNTIME_DIR`` does **not** relocate the *legacy* source path, though:
``legacy_data_dir()`` is installation-relative, so ``prepare_runtime_database()``
still reads the repository's own ``data/database.db`` when deciding whether to
migrate. It opens that file read-only and never deletes it, but if unresolved
``-wal``/``-journal`` sidecars make the migration refuse, it returns the legacy
path — and the negative case, which deliberately withholds ``DB_FILE``, would then
run ``upgrade_catalog_from_seed()`` against the developer's real database.
``_skip_if_legacy_database_is_busy`` refuses to run in that state rather than
write to it.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

# Imports app in a fresh interpreter and reports where the database actually
# landed. Kept as source rather than a helper module so what runs under the
# subprocess is visible at the point of assertion.
PROBE = """
import json, os, sys
sys.path.insert(0, sys.argv[1])
import utils.config
if sys.argv[3] == "patch-config-too":
    utils.config.DB_FILE = sys.argv[2]
import app  # noqa: F401
runtime_db = os.path.join(os.environ["HT_RUNTIME_DIR"], "data", "database.db")
print(json.dumps({
    "active_db": str(os.path.abspath(utils.config.DB_FILE)),
    "scratch_exists": os.path.exists(sys.argv[2]),
    "runtime_db_exists": os.path.exists(runtime_db),
    "runtime_db": os.path.abspath(runtime_db),
}))
"""


def _skip_if_legacy_database_is_busy():
    """Refuse the negative case when it could reach the real database.

    Only the ``set_env_db=False`` path needs this: with no ``DB_FILE`` override,
    ``prepare_runtime_database()`` inspects the repository's own database, and an
    outstanding SQLite sidecar makes it decline the migration and hand back the
    legacy path. Skipping is the honest outcome — the alternative is a test that
    writes to a developer's live data to prove a point about isolation.
    """
    legacy = ROOT / 'data' / 'database.db'
    busy = [
        suffix for suffix in ('-wal', '-shm', '-journal')
        if Path(f"{legacy}{suffix}").exists()
    ]
    if busy:
        pytest.skip(
            f"{legacy.name} has outstanding {', '.join(busy)} sidecars; the "
            "negative case would fall back to the real database"
        )


def _first_import(tmp_path, *, set_env_db, mode="patch-config-too"):
    """Import ``app`` in a fresh interpreter and report the resolved database."""
    sandbox = tmp_path / "runtime_sandbox"
    sandbox.mkdir()
    scratch = tmp_path / "scratch" / "database.db"
    scratch.parent.mkdir()

    env = dict(os.environ)
    env["HT_RUNTIME_DIR"] = str(sandbox)
    env["TESTING"] = "1"
    if set_env_db:
        env["DB_FILE"] = str(scratch)
    else:
        env.pop("DB_FILE", None)

    result = subprocess.run(
        [sys.executable, "-c", PROBE, str(ROOT), str(scratch), mode],
        capture_output=True, text=True, env=env, cwd=str(tmp_path), timeout=300,
    )
    assert result.returncode == 0, f"probe failed:\n{result.stdout}\n{result.stderr}"
    return json.loads(result.stdout.strip().splitlines()[-1]), scratch


def test_first_import_honours_the_fixture_isolation(tmp_path):
    """With the fixture's isolation applied, a first import stays on the scratch
    database and never creates the runtime one."""
    report, scratch = _first_import(tmp_path, set_env_db=True)

    assert Path(report["active_db"]).resolve() == scratch.resolve()
    assert report["scratch_exists"], "startup did not create the scratch database"
    assert not report["runtime_db_exists"], (
        "startup created the runtime database despite the DB_FILE override: "
        f"{report['runtime_db']}"
    )


def test_patching_config_alone_is_not_isolation(tmp_path):
    """The negative case, pinned so the reason for the environment variable
    cannot be optimized away.

    Without ``os.environ['DB_FILE']``, ``app.py``'s startup discards the patched
    ``utils.config.DB_FILE`` and builds the runtime database instead. This is the
    exact defect the fixture guards against; if this test ever fails, the startup
    contract changed and ``real_app_client``'s comment needs revisiting.
    """
    _skip_if_legacy_database_is_busy()
    report, scratch = _first_import(tmp_path, set_env_db=False)

    assert Path(report["active_db"]).resolve() != scratch.resolve()
    assert not report["scratch_exists"]
    assert report["runtime_db_exists"]


@pytest.mark.parametrize('mode', ['patch-config-too', 'env-only'])
def test_env_override_wins_regardless_of_config_patch(tmp_path, mode):
    """``DB_FILE`` in the environment is what decides the path; patching the
    module attribute is a convenience, not the mechanism."""
    report, scratch = _first_import(tmp_path, set_env_db=True, mode=mode)

    assert Path(report["active_db"]).resolve() == scratch.resolve()
    assert not report["runtime_db_exists"]


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
