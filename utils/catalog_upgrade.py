"""Bring an existing runtime catalog up to the shipped one, additively.

The seed only initializes a *new* install. Without this, a user who installed
once would never receive a corrected movement pattern or a newly mapped
exercise image, and fresh installs would silently diverge from upgraded ones.

The policy is additive and update-only:

- Exercises in the shipped catalog but not in the runtime database are inserted.
- Exercises already present have only their **catalog-owned** columns refreshed.
- Nothing is ever deleted or renamed, and nothing outside the two catalog tables
  is touched.

Deletion is not a symmetric risk to insertion. A wrong extra exercise is
cosmetic and ignorable; removing one silently invalidates every plan and log row
that references it, because `exercises.exercise_name` is the key those rows
carry. Renaming is deletion plus insertion against that same key, so it is not
automatic either. An exercise that disappears from a future catalog is left
alone.

**The column split is derived, not invented.** `ExerciseManager.save_exercise`
lets a user edit an exercise's muscle groups, equipment, mechanic, difficulty,
and the rest of its descriptive columns — including catalog exercises. Those
columns are therefore user-owned once a row exists, and refreshing them would
silently discard the user's edit. Only the columns no application path lets a
user write are refreshed. For the same reason `exercise_isolated_muscles` is
populated only for exercises this upgrade inserts: for existing rows it is
derived from the user-editable `advanced_isolated_muscles` column, so
reconciling it would overwrite user intent.
"""
from __future__ import annotations

import hashlib
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from utils.catalog_seed import resolve_catalog_seed_path
from utils.database import DatabaseHandler
from utils.logger import get_logger

logger = get_logger()

CATALOG_VERSION = 1
CATALOG_VERSION_TABLE = "catalog_version"

EXERCISES_TABLE = "exercises"
ISOLATED_MUSCLES_TABLE = "exercise_isolated_muscles"

# Columns no application path lets a user write, so refreshing them cannot
# discard an edit. Keep this in step with ExerciseManager.save_exercise: a
# column that becomes user-editable must move out of here.
CATALOG_OWNED_COLUMNS = (
    "movement_pattern",
    "movement_subpattern",
    "youtube_video_id",
    "media_path",
)


@dataclass(frozen=True)
class CatalogUpgradeResult:
    """What the upgrade did, for logging and for tests."""

    applied: bool
    inserted: int = 0
    refreshed: int = 0
    reason: str | None = None


def add_catalog_version_table() -> None:
    """Create the applied-catalog-version record.

    Catalog metadata, not user data: it is deliberately absent from
    ``OWNED_TABLES_DROP_ORDER`` so erasing user data does not force a needless
    full catalog re-scan on the next start.
    """
    with DatabaseHandler() as db:
        db.execute_query(
            f"""CREATE TABLE IF NOT EXISTS {CATALOG_VERSION_TABLE} (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                version INTEGER NOT NULL,
                content_hash TEXT NOT NULL,
                applied_at TEXT NOT NULL
            )"""
        )


def _catalog_content_hash(connection: sqlite3.Connection) -> str:
    """A content-addressed catalog version.

    Derived from the rows themselves rather than a hand-maintained number,
    which cannot be forgotten during a catalog change and cannot go stale.
    """
    digest = hashlib.sha256()
    for statement in (
        f"SELECT * FROM {EXERCISES_TABLE} ORDER BY exercise_name",
        f"SELECT * FROM {ISOLATED_MUSCLES_TABLE} ORDER BY exercise_name, muscle",
    ):
        for row in connection.execute(statement):
            digest.update(repr(row).encode("utf-8"))
            digest.update(b"\x1e")
        digest.update(b"\x1d")
    return digest.hexdigest()


def _read_seed_catalog(seed: Path) -> tuple[dict, dict, str]:
    """Return the shipped exercises, their isolated muscles, and the hash."""
    with closing(
        sqlite3.connect(f"file:{seed.as_posix()}?mode=ro", uri=True)
    ) as connection:
        content_hash = _catalog_content_hash(connection)
        connection.row_factory = sqlite3.Row
        exercises = {
            row["exercise_name"]: dict(row)
            for row in connection.execute(f"SELECT * FROM {EXERCISES_TABLE}")
        }
        muscles: dict[str, list[str]] = {}
        for row in connection.execute(
            f"SELECT exercise_name, muscle FROM {ISOLATED_MUSCLES_TABLE}"
        ):
            muscles.setdefault(row["exercise_name"], []).append(row["muscle"])
    return exercises, muscles, content_hash


def _recorded_content_hash(db: DatabaseHandler) -> str | None:
    row = db.fetch_one(
        f"SELECT content_hash FROM {CATALOG_VERSION_TABLE} WHERE id = 1"
    )
    return row["content_hash"] if row else None


def _record_applied(db: DatabaseHandler, content_hash: str) -> None:
    db.execute_query(
        f"""INSERT INTO {CATALOG_VERSION_TABLE}
                (id, version, content_hash, applied_at)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                version = excluded.version,
                content_hash = excluded.content_hash,
                applied_at = excluded.applied_at""",
        (CATALOG_VERSION, content_hash, datetime.now().isoformat(" ")),
    )


def _insert_exercise(db: DatabaseHandler, row: dict, muscles: list[str]) -> None:
    columns = list(row)
    db.execute_query(
        f"INSERT INTO {EXERCISES_TABLE} ({', '.join(columns)}) "
        f"VALUES ({', '.join(':' + column for column in columns)})",
        row,
    )
    for muscle in muscles:
        db.execute_query(
            f"INSERT OR IGNORE INTO {ISOLATED_MUSCLES_TABLE} "
            "(exercise_name, muscle) VALUES (?, ?)",
            (row["exercise_name"], muscle),
        )


def upgrade_catalog_from_seed(
    *,
    seed_path: Path | str | None = None,
    force: bool = False,
) -> CatalogUpgradeResult:
    """Apply the shipped catalog to the runtime database, additively.

    Idempotent: a second run against an unchanged catalog does nothing. Never
    raises — a catalog that cannot be read leaves the runtime database exactly
    as it was, which is a working application with a slightly older catalog.
    """
    seed = Path(
        seed_path if seed_path is not None else resolve_catalog_seed_path()
    )
    if not seed.is_file():
        return CatalogUpgradeResult(False, reason="no-seed")

    try:
        shipped, shipped_muscles, content_hash = _read_seed_catalog(seed)
    except sqlite3.Error as exc:
        logger.warning("Could not read the shipped catalog at %s: %s", seed, exc)
        return CatalogUpgradeResult(False, reason="unreadable-seed")

    try:
        with DatabaseHandler() as db:
            if not force and _recorded_content_hash(db) == content_hash:
                return CatalogUpgradeResult(False, reason="already-current")

            existing = {
                row["exercise_name"]: row
                for row in db.fetch_all(
                    f"SELECT exercise_name, "
                    f"{', '.join(CATALOG_OWNED_COLUMNS)} FROM {EXERCISES_TABLE}"
                )
            }

            inserted = 0
            for name, row in shipped.items():
                if name in existing:
                    continue
                _insert_exercise(db, row, shipped_muscles.get(name, []))
                inserted += 1

            refreshed = 0
            for name, current in existing.items():
                shipped_row = shipped.get(name)
                if shipped_row is None:
                    # Absent from a newer catalog: a user's own exercise, or one
                    # that was retired. Either way it is not ours to remove.
                    continue
                # A value the shipped catalog does not carry never erases one
                # the runtime database has. The seed currently ships
                # media_path empty for all 1,897 rows and youtube_video_id for
                # all but 56, so refreshing blindly would blank populated
                # columns the moment a catalog was regenerated without them.
                changes = {
                    column: shipped_row[column]
                    for column in CATALOG_OWNED_COLUMNS
                    if shipped_row[column] is not None
                    and current[column] != shipped_row[column]
                }
                if not changes:
                    continue
                assignments = ", ".join(f"{c} = :{c}" for c in changes)
                db.execute_query(
                    f"UPDATE {EXERCISES_TABLE} SET {assignments} "
                    "WHERE exercise_name = :exercise_name",
                    {**changes, "exercise_name": name},
                )
                refreshed += 1

            _record_applied(db, content_hash)
    except sqlite3.Error as exc:
        logger.warning("Catalog upgrade did not complete: %s", exc)
        return CatalogUpgradeResult(False, reason="failed")

    if inserted or refreshed:
        logger.info(
            "Catalog upgrade: %s exercise(s) added, %s refreshed (version %s)",
            inserted,
            refreshed,
            CATALOG_VERSION,
        )
    return CatalogUpgradeResult(True, inserted=inserted, refreshed=refreshed)
