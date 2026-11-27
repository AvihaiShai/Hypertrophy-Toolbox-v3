"""Shared probes and assertions for the application-factory contracts."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import sysconfig
from collections.abc import Callable
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST_ID = re.compile(r"^req_[0-9a-f]{16}$")

# (step name, positional args, keyword args, utils.config.DB_FILE at the call)
Call = tuple[str, tuple[object, ...], dict[str, object], str]


def install_runtime_steps(
    monkeypatch,
    database: Path,
    *,
    action: str = "explicit-override",
    overrides: dict[str, Callable[[], object]] | None = None,
) -> list[Call]:
    """Record each startup step and the database path visible when it runs."""
    import utils.config
    import utils.runtime_init as runtime_init
    from utils.runtime_migration import MigrationOutcome

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


def probe_env(**overrides: str) -> dict[str, str]:
    """Keep host necessities and private caches; reset application settings."""
    env = {
        name: value for name, value in os.environ.items()
        if name not in ("TESTING", "DB_FILE") and not name.startswith("HT_")
    }
    env.update(overrides)
    return env


def run_python(tmp_path: Path, args: list[str], env: dict[str, str]) -> str:
    result = subprocess.run(
        [sys.executable, *args],
        capture_output=True, text=True, env=env, cwd=str(tmp_path), timeout=300,
    )
    assert result.returncode == 0, f"probe failed:\n{result.stdout}\n{result.stderr}"
    return result.stdout


def stage_probe_installation(tmp_path: Path) -> Path:
    """Copy just the application Python source and shipped catalog seed."""
    installation = tmp_path.resolve() / "installation"
    installation.mkdir()
    sources = [ROOT / "app.py", ROOT / "data" / "catalog.seed.db"]
    for package in ("routes", "utils"):
        sources.extend(sorted((ROOT / package).rglob("*.py")))
    for source in sources:
        assert not source.is_symlink() and source.resolve() == source
        destination = installation / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    return installation


def _installation_state(installation: Path) -> dict[str, tuple[int, str | None]]:
    state = {}
    for path in installation.rglob("*"):
        assert not path.is_symlink() and path.resolve() == path
        state[path.relative_to(installation).as_posix()] = (
            path.stat().st_mtime_ns,
            sha256(path.read_bytes()).hexdigest() if path.is_file() else None,
        )
    return state


_PROBE_BOOTSTRAP = """
import json
import sys
from importlib.util import find_spec
from pathlib import Path

installation = Path(sys.argv[1])
sys.path.insert(0, str(installation))
sys.path.extend(json.loads(sys.argv.pop(2)))
application_packages = {"app", "routes", "utils"}


def assert_local_spec(name, spec):
    assert spec is not None, name
    if spec.origin is not None:
        assert Path(spec.origin).resolve().is_relative_to(installation), spec.origin
    for location in spec.submodule_search_locations or ():
        assert Path(location).resolve().is_relative_to(installation), location


for package in application_packages:
    assert package not in sys.modules, package
    assert_local_spec(package, find_spec(package))
"""


_PROBE_VERIFY = """
for name, module in sys.modules.items():
    if name.split(".", 1)[0] in application_packages:
        assert_local_spec(name, module.__spec__)
assert sys.modules["utils.runtime_paths"].installation_root() == installation
"""


def run_probe(
    tmp_path: Path, probe: str, *args: str, env: dict[str, str],
    installation: Path | None = None,
) -> dict:
    if installation is None:
        installation = stage_probe_installation(tmp_path)
    assert installation == tmp_path.resolve() / "installation"
    before = _installation_state(installation)
    # Skip Python's site startup (.pth files and sitecustomize). Add only the
    # interpreter's installed-dependency directories, without executing hooks.
    dependency_paths = list(dict.fromkeys(
        sysconfig.get_path(name) for name in ("purelib", "platlib")
    ))
    stdout = run_python(
        tmp_path,
        [
            "-I", "-S", "-B", "-c", "\n".join((_PROBE_BOOTSTRAP, probe, _PROBE_VERIFY)),
            str(installation), json.dumps(dependency_paths), *args,
        ],
        env,
    )
    assert _installation_state(installation) == before, "probe changed its installation"
    return json.loads(stdout.strip().splitlines()[-1])


OUTCOME_PROBE = """
import json, os, sys
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
    "snapshot_path": None if outcome.snapshot_path is None else str(outcome.snapshot_path),
    "already_initialized": outcome.already_initialized,
}))
"""
