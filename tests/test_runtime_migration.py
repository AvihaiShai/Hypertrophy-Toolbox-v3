"""Contracts for the legacy-database migration (Packet B2).

The property under test throughout is that the legacy database survives every
path — success, refusal, corruption, concurrency — byte for byte.
"""
from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path

import pytest

from utils.runtime_migration import (
    MigrationError,
    _verify_copy,
    copy_legacy_backups,
    prepare_runtime_database,
)


def _write_database(path: Path, exercises: int = 3, plans: int = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path))
    try:
        connection.execute(
            "CREATE TABLE exercises (exercise_name TEXT PRIMARY KEY)"
        )
        connection.execute(
            "CREATE TABLE user_selection ("
            "id INTEGER PRIMARY KEY, exercise TEXT, "
            "FOREIGN KEY (exercise) REFERENCES exercises(exercise_name))"
        )
        for index in range(exercises):
            connection.execute(
                "INSERT INTO exercises VALUES (?)", (f"Exercise {index}",)
            )
        for index in range(plans):
            connection.execute(
                "INSERT INTO user_selection (exercise) VALUES (?)",
                (f"Exercise {index}",),
            )
        connection.commit()
    finally:
        connection.close()


def _row_count(path: Path, table: str) -> int:
    connection = sqlite3.connect(str(path))
    try:
        return connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    finally:
        connection.close()


@pytest.fixture
def legacy(tmp_path: Path) -> Path:
    path = tmp_path / "install" / "data" / "database.db"
    _write_database(path)
    return path


@pytest.fixture
def target(tmp_path: Path) -> Path:
    return tmp_path / "userdata" / "data" / "database.db"


@pytest.fixture(autouse=True)
def no_ambient_override(monkeypatch):
    monkeypatch.delenv("DB_FILE", raising=False)


class TestSuccessfulMigration:
    def test_copies_rows_and_leaves_the_original_untouched(self, legacy, target):
        original = legacy.read_bytes()

        outcome = prepare_runtime_database(target=target, legacy=legacy)

        assert outcome.action == "migrated"
        assert outcome.database_path == target
        assert target.is_file()
        assert _row_count(target, "exercises") == 3
        assert _row_count(target, "user_selection") == 2
        assert legacy.is_file()
        assert legacy.read_bytes() == original

    def test_runs_exactly_once(self, legacy, target):
        prepare_runtime_database(target=target, legacy=legacy)
        _write_database(legacy.with_name("other.db"), exercises=99)
        # Simulate the user continuing to work in the migrated database.
        connection = sqlite3.connect(str(target))
        connection.execute("INSERT INTO exercises VALUES ('Added Later')")
        connection.commit()
        connection.close()

        outcome = prepare_runtime_database(target=target, legacy=legacy)

        assert outcome.action == "already-present"
        assert _row_count(target, "exercises") == 4

    def test_leaves_no_temporary_files_behind(self, legacy, target):
        prepare_runtime_database(target=target, legacy=legacy)

        assert sorted(p.name for p in target.parent.iterdir()) == [
            "database.db"
        ]


class TestNeverDestructive:
    def test_an_existing_runtime_database_is_never_replaced(
        self, legacy, target
    ):
        _write_database(target, exercises=7)
        existing = target.read_bytes()

        outcome = prepare_runtime_database(target=target, legacy=legacy)

        assert outcome.action == "already-present"
        assert target.read_bytes() == existing

    def test_an_empty_existing_runtime_database_is_still_not_replaced(
        self, legacy, target
    ):
        """"Looks empty" is not a licence to overwrite; it may be mid-repair."""
        target.parent.mkdir(parents=True)
        target.touch()

        outcome = prepare_runtime_database(target=target, legacy=legacy)

        assert outcome.action == "already-present"
        assert target.stat().st_size == 0

    def test_a_concurrent_winner_is_preserved(
        self, legacy, target, monkeypatch
    ):
        """Two simultaneous first launches must not clobber each other."""
        import utils.runtime_migration as migration_module

        real_verify = migration_module._verify_copy

        def verify_then_race(source: Path, copy: Path) -> None:
            real_verify(source, copy)
            if not target.exists():
                _write_database(target, exercises=42)

        monkeypatch.setattr(
            migration_module, "_verify_copy", verify_then_race
        )

        outcome = prepare_runtime_database(target=target, legacy=legacy)

        assert outcome.action == "migrated"
        assert _row_count(target, "exercises") == 42
        assert legacy.is_file()


class TestRefusesRatherThanGuesses:
    @pytest.mark.parametrize("suffix", ["-wal", "-journal"])
    def test_unresolved_journal_state_refuses_migration(
        self, legacy, target, suffix
    ):
        """Copying past a live WAL would silently drop committed rows."""
        legacy.with_name(legacy.name + suffix).write_bytes(b"pending")
        original = legacy.read_bytes()

        outcome = prepare_runtime_database(target=target, legacy=legacy)

        assert outcome.action == "failed"
        assert "unresolved journal state" in (outcome.reason or "")
        assert not target.exists()
        assert legacy.read_bytes() == original

    def test_a_failed_migration_keeps_using_the_legacy_database(
        self, legacy, target
    ):
        legacy.with_name(legacy.name + "-wal").write_bytes(b"pending")

        outcome = prepare_runtime_database(target=target, legacy=legacy)

        assert outcome.database_path == legacy

    def test_a_corrupt_legacy_database_never_becomes_a_clean_seed(
        self, legacy, target
    ):
        """The failure mode that would read to a user as data loss."""
        legacy.write_bytes(b"this is not a database" * 100)

        outcome = prepare_runtime_database(target=target, legacy=legacy)

        assert outcome.action == "failed"
        assert outcome.database_path == legacy
        assert not target.exists()

    def test_an_unverifiable_copy_is_discarded(
        self, legacy, target, monkeypatch
    ):
        import utils.runtime_migration as migration_module

        def reject(source: Path, copy: Path) -> None:
            raise MigrationError("row counts differ")

        monkeypatch.setattr(migration_module, "_verify_copy", reject)

        outcome = prepare_runtime_database(target=target, legacy=legacy)

        assert outcome.action == "failed"
        assert not target.exists()
        assert not list(target.parent.glob("*.tmp"))
        assert legacy.is_file()

    def test_verification_rejects_a_copy_missing_rows(self, legacy, tmp_path):
        truncated = tmp_path / "truncated.db"
        shutil.copyfile(legacy, truncated)
        connection = sqlite3.connect(str(truncated))
        connection.execute("DELETE FROM user_selection")
        connection.commit()
        connection.close()

        with pytest.raises(MigrationError, match="user_selection"):
            _verify_copy(legacy, truncated)

    def test_verification_accepts_a_faithful_copy(self, legacy, tmp_path):
        faithful = tmp_path / "faithful.db"
        shutil.copyfile(legacy, faithful)

        _verify_copy(legacy, faithful)


class TestPrecedence:
    def test_an_explicit_db_file_is_never_migrated_into(
        self, legacy, target, monkeypatch, tmp_path
    ):
        chosen = tmp_path / "chosen.db"
        monkeypatch.setenv("DB_FILE", str(chosen))

        outcome = prepare_runtime_database(target=target, legacy=legacy)

        assert outcome.action == "explicit-override"
        assert outcome.database_path == chosen
        assert not target.exists()

    def test_identical_paths_are_a_no_op(self, legacy):
        outcome = prepare_runtime_database(target=legacy, legacy=legacy)

        assert outcome.action == "same-path"
        assert outcome.database_path == legacy

    def test_a_fresh_install_defers_to_seed_bootstrap(self, tmp_path, target):
        absent = tmp_path / "install" / "data" / "database.db"

        outcome = prepare_runtime_database(target=target, legacy=absent)

        assert outcome.action == "no-legacy"
        assert outcome.database_path == target
        assert not target.exists()


class TestAwkwardEnvironments:
    @pytest.mark.parametrize(
        "name", ["with spaces", "ünïcodé", "spaces and ünïcodé"]
    )
    def test_paths_with_spaces_and_non_ascii_migrate(self, tmp_path, name):
        legacy = tmp_path / f"install {name}" / "data" / "database.db"
        _write_database(legacy)
        target = tmp_path / f"userdata {name}" / "data" / "database.db"

        outcome = prepare_runtime_database(target=target, legacy=legacy)

        assert outcome.action == "migrated"
        assert _row_count(target, "exercises") == 3

    def test_a_read_only_installation_directory_still_migrates(
        self, legacy, target
    ):
        """The whole point: the source is only ever read.

        Genuinely restrictive on POSIX (where CI runs pytest); on Windows
        chmod does not restrict directories, so there it asserts only that the
        happy path is unaffected.
        """
        install_directory = legacy.parent
        original_mode = install_directory.stat().st_mode
        install_directory.chmod(0o500)
        try:
            outcome = prepare_runtime_database(target=target, legacy=legacy)
        finally:
            install_directory.chmod(original_mode)

        assert outcome.action == "migrated"
        assert _row_count(target, "exercises") == 3


class TestBackupCopying:
    def test_copies_snapshots_once(self, tmp_path):
        source = tmp_path / "install" / "data" / "auto_backup"
        source.mkdir(parents=True)
        for stamp in ("20260101_010101", "20260102_010101"):
            _write_database(source / f"database_{stamp}.db")
        target = tmp_path / "userdata" / "data" / "auto_backup"

        assert copy_legacy_backups(source, target) == 2
        assert copy_legacy_backups(source, target) == 0
        assert sorted(p.name for p in target.iterdir()) == [
            "database_20260101_010101.db",
            "database_20260102_010101.db",
        ]
        assert len(list(source.iterdir())) == 2

    def test_missing_legacy_backups_are_not_an_error(self, tmp_path):
        assert copy_legacy_backups(
            tmp_path / "absent", tmp_path / "target"
        ) == 0

    def test_a_copy_failure_never_blocks_startup(self, tmp_path, monkeypatch):
        source = tmp_path / "auto_backup"
        source.mkdir()
        _write_database(source / "database_20260101_010101.db")

        def explode(*args, **kwargs):
            raise OSError("disk full")

        monkeypatch.setattr("utils.runtime_migration.shutil.copy2", explode)

        assert copy_legacy_backups(source, tmp_path / "target") == 0

    def test_migration_carries_backups_across(self, tmp_path, monkeypatch):
        legacy = tmp_path / "install" / "data" / "database.db"
        _write_database(legacy)
        backups = legacy.parent / "auto_backup"
        backups.mkdir()
        _write_database(backups / "database_20260101_010101.db")
        target = tmp_path / "userdata" / "data" / "database.db"
        monkeypatch.setattr(
            "utils.runtime_migration.legacy_data_dir", lambda: legacy.parent
        )
        monkeypatch.setattr(
            "utils.runtime_migration.runtime_data_dir", lambda: target.parent
        )

        outcome = prepare_runtime_database(target=target, legacy=legacy)

        assert outcome.backups_copied == 1
        assert (target.parent / "auto_backup").is_dir()
