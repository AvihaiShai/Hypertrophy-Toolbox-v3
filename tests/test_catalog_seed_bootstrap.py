"""First-install catalog bootstrap and isolation contracts."""
from __future__ import annotations

import hashlib
import importlib
import os
import sqlite3
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import utils.config
from utils.catalog_seed import (
    bootstrap_runtime_database,
    resolve_catalog_seed_path,
)
from utils.database import DatabaseHandler
from utils.schema_registry import OWNED_TABLES_DROP_ORDER, run_all_initializers


def test_bootstrap_copies_seed_to_explicit_missing_database(tmp_path):
    seed = tmp_path / "seed.db"
    seed.write_bytes(b"immutable catalog")
    target = tmp_path / "nested" / "runtime.db"

    assert bootstrap_runtime_database(
        seed_path=seed,
        database_path=target,
    )
    assert target.read_bytes() == seed.read_bytes()


def test_bootstrap_never_overwrites_existing_database(tmp_path):
    seed = tmp_path / "seed.db"
    target = tmp_path / "runtime.db"
    seed.write_bytes(b"catalog")
    target.write_bytes(b"existing user data")

    assert not bootstrap_runtime_database(
        seed_path=seed,
        database_path=target,
    )
    assert target.read_bytes() == b"existing user data"


def test_bootstrap_handles_simultaneous_first_launches(tmp_path):
    seed = tmp_path / "seed.db"
    target = tmp_path / "runtime.db"
    seed.write_bytes(os.urandom(1024 * 64))

    def launch() -> bool:
        return bootstrap_runtime_database(
            seed_path=seed,
            database_path=target,
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: launch(), range(2)))

    assert sorted(results) == [False, True]
    assert hashlib.sha256(target.read_bytes()).digest() == hashlib.sha256(
        seed.read_bytes()
    ).digest()
    assert list(tmp_path.glob(".runtime.db.*.tmp")) == []


def test_missing_seed_preserves_empty_schema_path(tmp_path):
    target = tmp_path / "runtime.db"

    assert not bootstrap_runtime_database(
        seed_path=tmp_path / "missing.seed.db",
        database_path=target,
    )
    assert not target.exists()


def test_configured_missing_db_file_receives_seed(monkeypatch, tmp_path):
    target = tmp_path / "configured" / "runtime.db"
    monkeypatch.setattr(utils.config, "DB_FILE", str(target))

    assert bootstrap_runtime_database()
    assert target.read_bytes() == resolve_catalog_seed_path().read_bytes()


def test_source_and_frozen_seed_resolution(monkeypatch, tmp_path):
    source_seed = resolve_catalog_seed_path()
    assert source_seed == (
        Path(__file__).resolve().parents[1] / "data" / "catalog.seed.db"
    )

    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path), raising=False)
    assert resolve_catalog_seed_path() == tmp_path / "data" / "catalog.seed.db"


def test_initializers_do_not_bootstrap_catalog(monkeypatch, tmp_path):
    target = tmp_path / "initializer-only.db"
    monkeypatch.setattr(utils.config, "DB_FILE", str(target))

    run_all_initializers(force_base=True)

    with sqlite3.connect(target) as connection:
        row = connection.execute("SELECT COUNT(*) FROM exercises").fetchone()
        count = row[0]
        assert count == 0


def test_database_handler_does_not_bootstrap_catalog(monkeypatch, tmp_path):
    target = tmp_path / "handler-only.db"
    monkeypatch.setattr(utils.config, "DB_FILE", str(target))

    with DatabaseHandler() as database:
        tables = database.fetch_all(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )

    assert tables == []


def test_config_import_does_not_create_database(monkeypatch, tmp_path):
    target = tmp_path / "config-only.db"
    monkeypatch.setenv("DB_FILE", str(target))

    importlib.reload(utils.config)
    try:
        assert not target.exists()
    finally:
        monkeypatch.delenv("DB_FILE")
        importlib.reload(utils.config)


def test_real_app_first_install_seeds_catalog_without_mutating_seed(tmp_path):
    target = tmp_path / "runtime.db"
    seed = resolve_catalog_seed_path()
    seed_hash = hashlib.sha256(seed.read_bytes()).digest()
    environment = os.environ.copy()
    environment.pop("TESTING", None)
    environment["DB_FILE"] = str(target)
    environment["FLASK_USE_RELOADER"] = "0"
    smoke = (
        "import app; "
        "assert app.app.test_client().get('/').status_code == 200"
    )

    subprocess.run(
        [
            sys.executable,
            "-c",
            smoke,
        ],
        cwd=Path(__file__).resolve().parents[1],
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )

    with sqlite3.connect(target) as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM exercises"
        ).fetchone()[0] == 1897
        for table in OWNED_TABLES_DROP_ORDER:
            count = connection.execute(
                f'SELECT COUNT(*) FROM "{table}"'
            ).fetchone()[0]
            assert count == 0

    assert hashlib.sha256(seed.read_bytes()).digest() == seed_hash
    assert not (tmp_path / "auto_backup").exists()
