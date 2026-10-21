"""Shared probes and assertions for the application-factory contracts."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections.abc import Callable
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


def run_probe(tmp_path: Path, probe: str, *args: str, env: dict[str, str]) -> dict:
    stdout = run_python(tmp_path, ["-c", probe, str(ROOT), *args], env)
    return json.loads(stdout.strip().splitlines()[-1])


OUTCOME_PROBE = """
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
    "snapshot_path": None if outcome.snapshot_path is None else str(outcome.snapshot_path),
    "already_initialized": outcome.already_initialized,
}))
"""
