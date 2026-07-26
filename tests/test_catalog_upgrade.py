"""Contracts for versioned, additive catalog upgrades (Packet B3).

The property under test throughout: an upgrade may add and it may refresh
catalog-owned columns, but it may never remove an exercise, rename one, discard
a user's edit, or touch a row outside the two catalog tables.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

import utils.config
from utils.catalog_upgrade import (
    CATALOG_OWNED_COLUMNS,
    CATALOG_VERSION,
    CATALOG_VERSION_TABLE,
    add_catalog_version_table,
    upgrade_catalog_from_seed,
)
from utils.schema_registry import OWNED_TABLES_DROP_ORDER, run_all_initializers

CATALOG_COLUMNS = (
    "exercise_name",
    "primary_muscle_group",
    "secondary_muscle_group",
    "tertiary_muscle_group",
    "advanced_isolated_muscles",
    "utility",
    "grips",
    "stabilizers",
    "synergists",
    "force",
    "equipment",
    "mechanic",
    "difficulty",
    "movement_pattern",
    "movement_subpattern",
    "youtube_video_id",
    "media_path",
)


def _exercise(name: str, **overrides) -> dict[str, str | None]:
    row: dict[str, str | None] = {column: None for column in CATALOG_COLUMNS}
    row["exercise_name"] = name
    row["primary_muscle_group"] = "Chest"
    row["equipment"] = "Barbell"
    row["movement_pattern"] = "horizontal_push"
    row.update(overrides)
    return row


def _write_seed(path: Path, exercises: list[dict], muscles: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path))
    try:
        connection.execute(
            "CREATE TABLE exercises ("
            + ", ".join(f"{column} TEXT" for column in CATALOG_COLUMNS)
            + ", PRIMARY KEY (exercise_name))"
        )
        connection.execute(
            "CREATE TABLE exercise_isolated_muscles ("
            "exercise_name TEXT, muscle TEXT, "
            "PRIMARY KEY (exercise_name, muscle))"
        )
        for row in exercises:
            connection.execute(
                "INSERT INTO exercises VALUES ("
                + ", ".join(f":{column}" for column in CATALOG_COLUMNS)
                + ")",
                row,
            )
        for name, entries in muscles.items():
            for muscle in entries:
                connection.execute(
                    "INSERT INTO exercise_isolated_muscles VALUES (?, ?)",
                    (name, muscle),
                )
        connection.commit()
    finally:
        connection.close()
    return path


@pytest.fixture
def runtime(app, db_handler):
    """A runtime database carrying one catalog exercise and one user plan."""
    db_handler.execute_query(
        "INSERT INTO exercises (exercise_name, primary_muscle_group, "
        "equipment, movement_pattern) VALUES (?, ?, ?, ?)",
        ("Bench Press", "Chest", "Barbell", "horizontal_push"),
    )
    db_handler.execute_query(
        "INSERT INTO user_selection (routine, exercise, sets, min_rep_range, "
        "max_rep_range, weight) VALUES (?, ?, 3, 8, 12, 60.0)",
        ("Push Day", "Bench Press"),
    )
    return db_handler


@pytest.fixture
def seed(tmp_path) -> Path:
    """A shipped catalog: the existing exercise plus a new one."""
    return _write_seed(
        tmp_path / "catalog.seed.db",
        [
            _exercise("Bench Press", media_path="media/bench.jpg"),
            _exercise("Cable Fly", primary_muscle_group="Chest"),
        ],
        {"Cable Fly": ["pectoralis-major-sternal"]},
    )


def _names(db) -> set[str]:
    return {row["exercise_name"] for row in db.fetch_all(
        "SELECT exercise_name FROM exercises"
    )}


class TestAdditiveUpgrade:
    def test_new_exercises_are_inserted_with_their_muscles(self, runtime, seed):
        result = upgrade_catalog_from_seed(seed_path=seed)

        assert result.applied
        assert result.inserted == 1
        assert _names(runtime) == {"Bench Press", "Cable Fly"}
        muscles = runtime.fetch_all(
            "SELECT muscle FROM exercise_isolated_muscles "
            "WHERE exercise_name = ?",
            ("Cable Fly",),
        )
        assert [row["muscle"] for row in muscles] == [
            "pectoralis-major-sternal"
        ]

    def test_catalog_owned_columns_are_refreshed(self, runtime, seed):
        upgrade_catalog_from_seed(seed_path=seed)

        row = runtime.fetch_one(
            "SELECT media_path FROM exercises WHERE exercise_name = ?",
            ("Bench Press",),
        )
        assert row["media_path"] == "media/bench.jpg"

    def test_running_twice_changes_nothing(self, runtime, seed):
        upgrade_catalog_from_seed(seed_path=seed)

        second = upgrade_catalog_from_seed(seed_path=seed)

        assert not second.applied
        assert second.reason == "already-current"
        assert _names(runtime) == {"Bench Press", "Cable Fly"}

    def test_a_changed_catalog_is_reapplied(self, runtime, seed, tmp_path):
        upgrade_catalog_from_seed(seed_path=seed)
        newer = _write_seed(
            tmp_path / "newer.seed.db",
            [
                _exercise("Bench Press", media_path="media/bench.jpg"),
                _exercise("Cable Fly"),
                _exercise("Pec Deck"),
            ],
            {},
        )

        result = upgrade_catalog_from_seed(seed_path=newer)

        assert result.applied
        assert result.inserted == 1
        assert "Pec Deck" in _names(runtime)

    def test_the_applied_version_is_recorded(self, runtime, seed):
        upgrade_catalog_from_seed(seed_path=seed)

        row = runtime.fetch_one(
            f"SELECT version, content_hash, applied_at "
            f"FROM {CATALOG_VERSION_TABLE} WHERE id = 1"
        )
        assert row["version"] == CATALOG_VERSION
        assert len(row["content_hash"]) == 64
        assert row["applied_at"]


class TestNeverDestructive:
    def test_an_exercise_missing_from_a_newer_catalog_is_kept(
        self, runtime, seed, tmp_path
    ):
        """Removing it would invalidate every plan and log row naming it."""
        upgrade_catalog_from_seed(seed_path=seed)
        shrunk = _write_seed(
            tmp_path / "shrunk.seed.db", [_exercise("Cable Fly")], {}
        )

        result = upgrade_catalog_from_seed(seed_path=shrunk)

        assert result.applied
        assert "Bench Press" in _names(runtime)

    def test_user_edits_to_catalog_exercises_survive(
        self, runtime, seed, tmp_path
    ):
        """save_exercise() lets a user rewrite these columns; we must not."""
        runtime.execute_query(
            "UPDATE exercises SET equipment = ?, difficulty = ?, "
            "primary_muscle_group = ? WHERE exercise_name = ?",
            ("Dumbbell", "Advanced", "Shoulders", "Bench Press"),
        )

        upgrade_catalog_from_seed(seed_path=seed)

        row = runtime.fetch_one(
            "SELECT equipment, difficulty, primary_muscle_group "
            "FROM exercises WHERE exercise_name = ?",
            ("Bench Press",),
        )
        assert row["equipment"] == "Dumbbell"
        assert row["difficulty"] == "Advanced"
        assert row["primary_muscle_group"] == "Shoulders"

    def test_a_missing_shipped_value_never_erases_a_populated_one(
        self, runtime, tmp_path
    ):
        """The seed ships media_path empty for every row today.

        Refreshing blindly would blank populated columns the moment a catalog
        was regenerated without them, which is data loss dressed as an update.
        """
        runtime.execute_query(
            "UPDATE exercises SET media_path = ?, youtube_video_id = ? "
            "WHERE exercise_name = ?",
            ("media/bench.jpg", "abc123", "Bench Press"),
        )
        sparse = _write_seed(
            tmp_path / "sparse.seed.db",
            [_exercise("Bench Press", media_path=None, youtube_video_id=None)],
            {},
        )

        upgrade_catalog_from_seed(seed_path=sparse)

        row = runtime.fetch_one(
            "SELECT media_path, youtube_video_id FROM exercises "
            "WHERE exercise_name = ?",
            ("Bench Press",),
        )
        assert row["media_path"] == "media/bench.jpg"
        assert row["youtube_video_id"] == "abc123"

    def test_a_shipped_correction_still_lands(self, runtime, tmp_path):
        """Not-erasing must not become not-updating."""
        corrected = _write_seed(
            tmp_path / "corrected.seed.db",
            [_exercise("Bench Press", movement_pattern="vertical_push")],
            {},
        )

        result = upgrade_catalog_from_seed(seed_path=corrected)

        assert result.refreshed == 1
        row = runtime.fetch_one(
            "SELECT movement_pattern FROM exercises WHERE exercise_name = ?",
            ("Bench Press",),
        )
        assert row["movement_pattern"] == "vertical_push"

    def test_user_created_exercises_are_untouched(self, runtime, seed):
        runtime.execute_query(
            "INSERT INTO exercises (exercise_name, primary_muscle_group, "
            "equipment) VALUES (?, ?, ?)",
            ("My Custom Lift", "Back", "Machine"),
        )

        upgrade_catalog_from_seed(seed_path=seed)

        row = runtime.fetch_one(
            "SELECT primary_muscle_group FROM exercises WHERE exercise_name = ?",
            ("My Custom Lift",),
        )
        assert row["primary_muscle_group"] == "Back"

    def test_user_isolated_muscle_edits_survive(self, runtime, seed):
        """Derived from the user-editable advanced_isolated_muscles column."""
        runtime.execute_query(
            "INSERT INTO exercise_isolated_muscles (exercise_name, muscle) "
            "VALUES (?, ?)",
            ("Bench Press", "a-muscle-the-user-chose"),
        )

        upgrade_catalog_from_seed(seed_path=seed)

        rows = runtime.fetch_all(
            "SELECT muscle FROM exercise_isolated_muscles "
            "WHERE exercise_name = ?",
            ("Bench Press",),
        )
        assert [row["muscle"] for row in rows] == ["a-muscle-the-user-chose"]

    def test_no_user_owned_table_is_touched(self, runtime, seed, tmp_path):
        before = {
            table: runtime.fetch_one(f'SELECT COUNT(*) AS n FROM "{table}"')[
                "n"
            ]
            for table in OWNED_TABLES_DROP_ORDER
        }
        shrunk = _write_seed(
            tmp_path / "shrunk.seed.db", [_exercise("Cable Fly")], {}
        )

        upgrade_catalog_from_seed(seed_path=shrunk)

        after = {
            table: runtime.fetch_one(f'SELECT COUNT(*) AS n FROM "{table}"')[
                "n"
            ]
            for table in OWNED_TABLES_DROP_ORDER
        }
        assert before == after
        assert before["user_selection"] == 1

    def test_a_plan_row_still_resolves_after_upgrade(self, runtime, seed):
        upgrade_catalog_from_seed(seed_path=seed)

        joined = runtime.fetch_one(
            "SELECT s.routine FROM user_selection s "
            "JOIN exercises e ON e.exercise_name = s.exercise"
        )
        assert joined["routine"] == "Push Day"


class TestFailureIsHarmless:
    def test_a_missing_catalog_is_not_an_error(self, runtime, tmp_path):
        result = upgrade_catalog_from_seed(seed_path=tmp_path / "absent.db")

        assert not result.applied
        assert result.reason == "no-seed"
        assert _names(runtime) == {"Bench Press"}

    def test_an_unreadable_catalog_leaves_the_database_alone(
        self, runtime, tmp_path
    ):
        broken = tmp_path / "broken.seed.db"
        broken.write_bytes(b"not a database" * 50)

        result = upgrade_catalog_from_seed(seed_path=broken)

        assert not result.applied
        assert result.reason == "unreadable-seed"
        assert _names(runtime) == {"Bench Press"}


class TestColumnSplitIsHonest:
    def test_catalog_owned_columns_are_not_user_editable(self):
        """The split is derived from what the application lets a user write.

        If save_exercise() gains one of these columns, refreshing it would
        start discarding user edits, and this fails rather than letting that
        happen quietly.
        """
        source = (
            Path(__file__).resolve().parents[1] / "utils" / "exercise_manager.py"
        ).read_text(encoding="utf-8")
        body = source.split("def save_exercise", 1)[1]
        editable_block = body.split("columns = [", 1)[1].split("]", 1)[0]

        for column in CATALOG_OWNED_COLUMNS:
            assert f'"{column}"' not in editable_block


class TestSchemaRegistration:
    def test_the_version_table_is_created_by_the_initializers(
        self, test_db_path, monkeypatch
    ):
        monkeypatch.setattr(utils.config, "DB_FILE", test_db_path)
        run_all_initializers(force_base=True)

        connection = sqlite3.connect(test_db_path)
        try:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
        finally:
            connection.close()
        assert CATALOG_VERSION_TABLE in tables

    def test_the_version_table_is_catalog_metadata_not_user_data(self):
        """Erasing user data must not force a needless full catalog re-scan."""
        assert CATALOG_VERSION_TABLE not in OWNED_TABLES_DROP_ORDER

    def test_creating_the_table_is_idempotent(self, db_handler):
        add_catalog_version_table()
        add_catalog_version_table()

        assert db_handler.fetch_one(
            f"SELECT COUNT(*) AS n FROM {CATALOG_VERSION_TABLE}"
        )["n"] == 0
