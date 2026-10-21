"""The one guarded runtime initialization: migrate, seed, schema, upgrade, snapshot.

``import app`` does no database work; every entry point that serves the real
runtime calls ``init_runtime()`` instead. The guard is per process: the same
request is a no-op, a different database or runtime root raises, and a failed
attempt leaves it unset so a retry runs.

This module touches no Flask object and imports no ``app`` or ``routes`` module.
"""
from __future__ import annotations

import os
import threading
from dataclasses import dataclass, replace
from pathlib import Path

from werkzeug.serving import is_running_from_reloader

import utils.config
from utils.auto_backup import create_startup_backup
from utils.catalog_seed import bootstrap_runtime_database
from utils.catalog_upgrade import upgrade_catalog_from_seed
from utils.logger import get_logger
from utils.runtime_migration import prepare_runtime_database
from utils.runtime_paths import runtime_root
from utils.schema_registry import run_all_initializers

logger = get_logger()

GuardKey = tuple[str | None, str]


@dataclass(frozen=True)
class RuntimeInitOutcome:
    """What ``init_runtime()`` decided and did."""

    database_path: Path
    migration_action: str
    seeded: bool
    snapshot_path: Path | None
    already_initialized: bool


_lock = threading.Lock()
_completed: tuple[GuardKey, RuntimeInitOutcome] | None = None
# Resolved database paths this process published from the seed, kept across a
# failed attempt so its retry still skips the upgrade and the snapshot.
_seeded_databases: set[str] = set()


def _guard_key(explicit: str | None) -> GuardKey:
    requested = explicit if explicit is not None else (os.environ.get("DB_FILE") or None)
    requested_key = str(Path(requested).expanduser().resolve()) if requested else None
    return (requested_key, str(runtime_root()))


def init_runtime(db_file: str | os.PathLike[str] | None = None) -> RuntimeInitOutcome:
    """Run the five startup steps once per process, in their load-bearing order.

    The migration runs before the seed so an upgrading install never boots onto
    a fresh catalog while its real data sits at the old path. A fresh seed skips
    the upgrade and the snapshot. ``utils.config.DB_FILE`` is assigned once, from
    the migration's decision, and is never read as input.

    Any exception propagates with the guard unset.
    """
    global _completed
    if db_file is not None and not os.fspath(db_file):
        raise ValueError("db_file must be a non-empty path or None")
    explicit = os.fspath(db_file) if db_file is not None else None
    with _lock:
        key = _guard_key(explicit)
        if os.environ.get("TESTING") == "1" and key[0] is None:
            raise RuntimeError(
                "init_runtime() refuses to run under TESTING=1 without an explicit "
                "db_file or a DB_FILE environment variable. If this is not a test run, "
                "unset TESTING; in a test, pass db_file=<scratch path>."
            )
        if _completed is not None:
            done_key, done = _completed
            if key == done_key:
                logger.debug("Runtime already initialized for %s; skipping", done.database_path)
                return replace(done, already_initialized=True)
            raise RuntimeError(
                f"init_runtime() already initialized {done_key}; "
                f"refusing a different database or runtime root {key}"
            )

        migration = prepare_runtime_database(explicit_override=explicit)
        utils.config.DB_FILE = str(migration.database_path)
        seeded_now = bootstrap_runtime_database()
        database_key = str(Path(utils.config.DB_FILE).expanduser().resolve())
        if seeded_now:
            _seeded_databases.add(database_key)
        seeded = database_key in _seeded_databases
        run_all_initializers(force_base=False)
        snapshot = None
        if not seeded:
            upgrade_catalog_from_seed()
            snapshot = create_startup_backup()

        outcome = RuntimeInitOutcome(
            Path(migration.database_path), migration.action, seeded, snapshot, False
        )
        _completed = (key, outcome)
        logger.info(
            "Runtime initialized: database=%s migration=%s seeded=%s snapshot=%s",
            outcome.database_path, outcome.migration_action, seeded, snapshot,
        )
        return outcome


def should_initialize_runtime(use_reloader: bool) -> bool:
    """Reloader rule: initialize (and register DB cleanup) only in the serving process."""
    return (not use_reloader) or is_running_from_reloader()


def _reset_for_tests() -> None:
    """Test-only. Never called by production code; tests enforce this."""
    global _completed
    with _lock:
        _completed = None
        _seeded_databases.clear()
