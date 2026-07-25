"""Move an existing database out of the installation directory, once, safely.

Packet B1 built the resolver but deliberately left the database where it was.
This module is the other half: it decides which database a frozen install
actually opens, and migrates a legacy one when the new location is empty.

The legacy database is **never** deleted, moved, or written to. It is copied
through SQLite's backup API, the copy is verified before it is published, and
the original stays exactly where it was as the recovery path. If anything about
the migration cannot be proven, this run keeps using the legacy database and
says so — it never seeds a clean database after finding real user data, which
would present as data loss whether or not the data was recoverable.
"""
from __future__ import annotations

import os
import shutil
import sqlite3
import tempfile
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

from utils.logger import get_logger
from utils.runtime_paths import (
    ensure_directory,
    legacy_data_dir,
    legacy_database_path,
    publish_without_overwrite,
    runtime_data_dir,
    runtime_database_path,
)

logger = get_logger()

DB_FILE_ENV = "DB_FILE"
AUTO_BACKUP_DIRNAME = "auto_backup"

# A journal or WAL sidecar means the legacy database has state that only a
# writer can resolve, and writing to it is forbidden. Copying anyway would
# silently drop committed transactions still living in the WAL.
_UNRESOLVED_SIDECARS = ("-wal", "-journal")

RECOVERY_MESSAGE = (
    "The existing database was left untouched at %s and is still in use. "
    "Close any other running copy of the application and restart to retry "
    "the move to %s."
)


@dataclass(frozen=True)
class MigrationOutcome:
    """What startup decided, and which database it should open."""

    action: str
    database_path: Path
    legacy_path: Path | None = None
    backups_copied: int = 0
    reason: str | None = None

    @property
    def migrated(self) -> bool:
        return self.action == "migrated"


class MigrationError(RuntimeError):
    """Raised internally when a migration cannot be proven correct."""


def _table_names(connection: sqlite3.Connection) -> set[str]:
    rows = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%'"
    ).fetchall()
    return {row[0] for row in rows}


def _row_counts(connection: sqlite3.Connection) -> dict[str, int]:
    return {
        table: connection.execute(
            f'SELECT COUNT(*) FROM "{table}"'
        ).fetchone()[0]
        for table in _table_names(connection)
    }


def _read_only_connection(path: Path) -> sqlite3.Connection:
    """Open *path* in a mode that cannot modify it."""
    return sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)


def _assert_no_unresolved_sidecars(legacy: Path) -> None:
    outstanding = [
        legacy.with_name(legacy.name + suffix)
        for suffix in _UNRESOLVED_SIDECARS
        if legacy.with_name(legacy.name + suffix).exists()
    ]
    if outstanding:
        raise MigrationError(
            "the database has unresolved journal state "
            f"({', '.join(path.name for path in outstanding)}); it must be "
            "closed cleanly before it can be copied without writing to it"
        )


def _verify_copy(legacy: Path, copy: Path) -> None:
    """Fail unless *copy* is a sound database holding the same rows.

    ``closing`` rather than ``with connection``: the latter commits but leaves
    the handle open, and Windows refuses to rename a file that is still open —
    so the copy would verify and then fail to publish.
    """
    with closing(_read_only_connection(legacy)) as source, closing(
        _read_only_connection(copy)
    ) as destination:
        integrity = destination.execute("PRAGMA integrity_check").fetchone()
        if not integrity or integrity[0] != "ok":
            raise MigrationError(
                f"the copy failed its integrity check: {integrity}"
            )
        violations = destination.execute("PRAGMA foreign_key_check").fetchall()
        if violations:
            raise MigrationError(
                f"the copy has {len(violations)} foreign-key violations"
            )

        expected = _row_counts(source)
        actual = _row_counts(destination)
        if expected != actual:
            differing = sorted(
                table
                for table in set(expected) | set(actual)
                if expected.get(table) != actual.get(table)
            )
            raise MigrationError(
                "the copy does not hold the same rows; differing tables: "
                + ", ".join(differing)
            )


def _copy_and_publish(legacy: Path, target: Path) -> None:
    """Copy *legacy* to *target* via a verified temporary sibling.

    Verification happens before publication, never after: checking a database
    that is already the live one leaves a window in which a half-copied file is
    what the application opens.
    """
    ensure_directory(target.parent)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.migrating.", suffix=".tmp", dir=target.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with closing(_read_only_connection(legacy)) as source, closing(
            sqlite3.connect(str(temporary))
        ) as destination:
            source.backup(destination)

        _verify_copy(legacy, temporary)

        try:
            publish_without_overwrite(temporary, target)
        except FileExistsError:
            logger.info(
                "Runtime database appeared at %s while migrating; "
                "preserving it and leaving the original untouched",
                target,
            )
    finally:
        temporary.unlink(missing_ok=True)


def copy_legacy_backups(
    source_directory: Path | None = None,
    target_directory: Path | None = None,
) -> int:
    """Copy legacy auto-backup snapshots to the new runtime root, best-effort.

    Failure is logged and swallowed on purpose. The originals are untouched, so
    a failed copy costs nothing; blocking startup over it would cost the user
    their session.
    """
    source = (
        source_directory
        if source_directory is not None
        else legacy_data_dir() / AUTO_BACKUP_DIRNAME
    )
    target = (
        target_directory
        if target_directory is not None
        else runtime_data_dir() / AUTO_BACKUP_DIRNAME
    )
    if not source.is_dir() or source.resolve() == target.resolve():
        return 0

    copied = 0
    try:
        ensure_directory(target)
        for snapshot in sorted(source.glob("database_*.db")):
            destination = target / snapshot.name
            if destination.exists():
                continue
            shutil.copy2(snapshot, destination)
            copied += 1
    except OSError:
        logger.warning(
            "Could not copy every legacy backup from %s; the originals are "
            "unchanged and still readable there",
            source,
            exc_info=True,
        )
    if copied:
        logger.info("Copied %s legacy backup snapshot(s) to %s", copied, target)
    return copied


def prepare_runtime_database(
    *,
    target: Path | None = None,
    legacy: Path | None = None,
    explicit_override: str | None = None,
) -> MigrationOutcome:
    """Decide which database to open, migrating a legacy one exactly once.

    Precedence, and every branch is a no-op on the legacy file:

    1. An explicit ``DB_FILE`` wins outright and is never migrated into.
    2. A runtime database that already exists is used unchanged.
    3. A legacy database is copied once, verified, and published.
    4. Neither present — the caller's seed bootstrap handles a fresh install.

    Never raises. A migration that cannot be proven correct leaves the legacy
    database authoritative for this run and reports how to retry.
    """
    override = (
        explicit_override
        if explicit_override is not None
        else os.environ.get(DB_FILE_ENV)
    )
    if override:
        return MigrationOutcome("explicit-override", Path(override))

    destination = target if target is not None else runtime_database_path()
    origin = legacy if legacy is not None else legacy_database_path()

    if destination == origin:
        # A source checkout resolves both to the repository; nothing to move.
        return MigrationOutcome("same-path", destination, origin)
    if destination.exists():
        return MigrationOutcome("already-present", destination, origin)
    if not origin.is_file():
        return MigrationOutcome("no-legacy", destination, origin)

    try:
        _assert_no_unresolved_sidecars(origin)
        _copy_and_publish(origin, destination)
    except (MigrationError, sqlite3.Error, OSError) as exc:
        logger.error(
            "Could not move the existing database to %s: %s", destination, exc
        )
        logger.error(RECOVERY_MESSAGE, origin, destination)
        return MigrationOutcome(
            "failed", origin, origin, reason=str(exc)
        )

    backups_copied = copy_legacy_backups()
    logger.info(
        "Moved the existing database from %s to %s; the original was left in "
        "place",
        origin,
        destination,
    )
    return MigrationOutcome(
        "migrated", destination, origin, backups_copied=backups_copied
    )
