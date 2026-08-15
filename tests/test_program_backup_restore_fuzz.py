"""Restore-path row robustness: program_backup_items -> user_selection.

``restore_backup()`` validates every backup item against the canonical
``validate_workout_bounds`` contract before inserting it, so a persisted backup item carrying a
value ``POST /add_exercise`` rejects is skipped per row and reported, rather than written into
``user_selection``. FINDING-1 -- a non-numeric rep range reaching the analysis surfaces -- is
closed at that boundary.

Harness non-claim
-----------------
The direct UPDATE below is a harness device for constructing a persisted state, not a modelled
user action. This packet makes no claim that editing the database by hand is supported, expected,
or protected. What is modelled is the STATE: a ``program_backup_items`` row holding a value the
current plan routes reject -- reachable in production either by a backup taken before
``validate_workout_bounds`` gated that field, or by a backup taken from a ``user_selection`` row
written through a route that does not validate that field today.

Where the fix is, and is not
----------------------------
The fix is at the restore boundary only. **No calculation site was changed** --
``utils/effective_sets.py``, ``utils/weekly_summary.py``, ``utils/session_summary.py``,
``utils/progression_plan.py`` and ``utils/_fatigue/**`` are untouched, because mapping a
non-numeric rep range onto a number is a semantic choice that would silently alter displayed
volume. Rows already poisoned by a restore that predates this packet still reach those sites and
still raise; that is a separately scoped follow-up recorded in
``docs/LEFTOVERS_BY_PRIORITY.md`` §4a, not a gap here.

Nullability
-----------
``program_backup_items`` declares ``weight``, ``min_rep_range`` and ``max_rep_range`` NOT NULL and
only ``rir``/``rpe`` nullable. ``validate_workout_bounds`` has a single ``allow_null`` flag
covering all four bounded fields, which cannot express that split, and it additionally maps ``""``
onto null. The restore path therefore never sets the flag: it omits ``rir`` -- leaving it UNSET --
when and only when it is exactly ``None``, so NULL rir restores while a blank is rejected on every
column.

Incidental contract pin
-----------------------
The exact ``utils/workout_validation.py`` messages asserted below are pinned in this file and
nowhere else in the repository. They are asserted verbatim on purpose -- the exact string is what
distinguishes the bounds-rejection branch from the duplicate-row ``VALIDATION_ERROR`` branch, and
it is now also the user-facing ``reason`` the restore response returns -- so editing that copy
reds several nodes here. That is intended, but it means this file is also the sole guard on those
strings.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Mapping

import pytest

from utils.database import DatabaseHandler
from utils.program_backup import create_backup


_ROUTINE = "GYM - Full Body - Workout A"
_BACKUP_NAME = "Restore Fuzz Backup"


def _valid_add_exercise_payload(exercise_name: str) -> Dict[str, Any]:
    """A fully in-bounds ``POST /add_exercise`` body, before one field is made malformed."""
    return {
        "routine": _ROUTINE,
        "exercise": exercise_name,
        "sets": 3,
        "min_rep_range": 6,
        "max_rep_range": 8,
        "rir": 3,
        "weight": 50.0,
    }


def _seed_tampered_backup(
    workout_plan_factory: Any,
    exercise_name: str,
    updates: Mapping[str, Any],
    expected_typeof: Mapping[str, str],
) -> int:
    """Seed one valid plan row, back it up, then rewrite one backup item in place.

    The backup header is always built through production ``create_backup()`` -- never a
    hand-written ``INSERT INTO program_backups`` -- so this file stays independent of the
    backup header schema (``schema_version`` included).

    The ``typeof()`` check is what catches a numeric seeded as a string and silently coerced by
    column affinity.
    """
    workout_plan_factory(exercise_name=exercise_name, routine=_ROUTINE)

    backup = create_backup(name=_BACKUP_NAME)
    backup_id = backup["id"]

    columns = list(updates)
    assignments = ", ".join(f"{column} = ?" for column in columns)
    params = tuple(updates[column] for column in columns) + (backup_id,)

    with DatabaseHandler() as db:
        rowcount = db.execute_query(
            f"UPDATE program_backup_items SET {assignments} WHERE backup_id = ?",
            params,
        )
        assert rowcount == 1, f"Expected the tamper UPDATE to hit exactly one row, got {rowcount}"

        # restore_backup() never reads the header's item_count -- it re-selects the item rows --
        # so the item rows are what must be pinned here.
        count_row = db.fetch_one(
            "SELECT COUNT(*) AS cnt FROM program_backup_items WHERE backup_id = ?",
            (backup_id,),
        )
        assert count_row is not None
        assert count_row["cnt"] == 1

        for column in columns:
            stored = db.fetch_one(
                f"SELECT {column} AS value, typeof({column}) AS value_type "
                "FROM program_backup_items WHERE backup_id = ?",
                (backup_id,),
            )
            assert stored is not None
            assert stored["value"] == updates[column]
            assert stored["value_type"] == expected_typeof[column], (
                f"program_backup_items.{column} stored as {stored['value_type']!r}, "
                f"expected {expected_typeof[column]!r}"
            )

    return backup_id


# case id, backup-item updates, expected typeof per column, exact boundary message.
#
# `updates` is the SINGLE source of truth: it is both what the fixture writes into
# program_backup_items and what is layered onto the /add_exercise payload. Carrying a separate
# copy of the values for the payload would let the two drift apart, and the node would keep
# passing while no longer asserting the same value on both paths -- which is the whole premise.
# The backup-item column names and the payload field names coincide, so no mapping is needed.
_OUT_OF_BOUNDS_CASES = [
    (
        "weight_above_max",
        {"weight": 99999.0},
        {"weight": "real"},
        "Weight must be between 0 and 1000 kg.",
    ),
    (
        "weight_negative",
        {"weight": -50.0},
        {"weight": "real"},
        "Weight must be between 0 and 1000 kg.",
    ),
    (
        "rir_above_max",
        {"rir": 99},
        {"rir": "integer"},
        "RIR must be between 0 and 10.",
    ),
    (
        "rep_range_inverted",
        {"min_rep_range": 20, "max_rep_range": 5},
        {"min_rep_range": "integer", "max_rep_range": "integer"},
        "Minimum reps cannot exceed maximum reps.",
    ),
    (
        "min_rep_non_numeric",
        {"min_rep_range": "abc"},
        {"min_rep_range": "text"},
        "Minimum reps must be a finite number.",
    ),
]


@pytest.mark.parametrize(
    "updates,expected_typeof,expected_message",
    [case[1:] for case in _OUT_OF_BOUNDS_CASES],
    ids=[case[0] for case in _OUT_OF_BOUNDS_CASES],
)
def test_restore_rejects_rows_the_plan_route_rejects(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    updates,
    expected_typeof,
    expected_message,
):
    """A backup item the plan route rejects is also rejected, per row, by the restore path.

    The same value is asserted twice: once as the 400 the write path returns for it, and once as
    the row the restore path refuses to persist. The two now agree; the gap this file was written
    to characterize is closed.
    """
    exercise_name = exercise_factory("Fuzz Bench Press", primary_muscle_group="Chest")
    backup_id = _seed_tampered_backup(
        workout_plan_factory,
        exercise_name,
        updates,
        expected_typeof,
    )

    # (b) BOUNDARY -- the plan route rejects this exact value. The message, not just the code,
    # is asserted: routes/workout_plan.py returns VALIDATION_ERROR from four separate places
    # (no data, bounds, missing fields, and the duplicate-row branch). The duplicate branch is the
    # one that matters here -- this payload duplicates the row already seeded above, so if bounds
    # validation were removed the route would still answer 400 VALIDATION_ERROR with
    # "already exists". Only the exact-message assertion distinguishes them.
    payload = _valid_add_exercise_payload(exercise_name)
    payload.update(updates)
    response = client.post("/add_exercise", json=payload, content_type="application/json")

    assert response.status_code == 400
    error_payload = response.get_json()
    assert error_payload["ok"] is False
    assert error_payload["error"]["code"] == "VALIDATION_ERROR"
    assert error_payload["error"]["message"] == expected_message

    # (c) RESTORE -- the restore path now applies the same contract, per row. The request still
    # succeeds (replace mode is not abandoned over one bad row); the row is reported, not written.
    restore_response = client.post(
        f"/api/backups/{backup_id}/restore",
        content_type="application/json",
    )
    assert restore_response.status_code == 200
    restore_payload = restore_response.get_json()
    assert restore_payload["ok"] is True
    assert restore_payload["data"]["restored_count"] == 0

    invalid = restore_payload["data"]["invalid"]
    assert len(invalid) == 1
    assert invalid[0]["exercise"] == exercise_name
    assert invalid[0]["reason"] == expected_message
    assert invalid[0]["routine"]

    # The catalog channel stays empty -- the row was rejected for its bounds, not its exercise.
    assert restore_payload["data"]["skipped"] == []

    # (d) NOT PERSISTED -- the whole point of the packet. No row, in any storage class.
    with DatabaseHandler() as db:
        stored = db.fetch_one(
            "SELECT COUNT(*) AS row_count FROM user_selection WHERE exercise = ?",
            (exercise_name,),
        )
        assert stored is not None
        assert stored["row_count"] == 0


def test_weekly_summary_200_after_restore_skips_non_numeric_rep_range(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    caplog,
):
    """FINDING-1 closed: the poisoned row never reaches the analysis surfaces.

    This node is the inversion of the former ``known_defect`` node, which asserted the 500. The
    fix is at the restore boundary, so the assertion that matters is that nothing was written --
    not that the calculators tolerate the value. No calculation site was changed.
    """
    exercise_name = exercise_factory("Fuzz Incline Press", primary_muscle_group="Chest")
    backup_id = _seed_tampered_backup(
        workout_plan_factory,
        exercise_name,
        {"min_rep_range": "abc"},
        {"min_rep_range": "text"},
    )

    restore_response = client.post(
        f"/api/backups/{backup_id}/restore",
        content_type="application/json",
    )
    assert restore_response.status_code == 200
    restore_payload = restore_response.get_json()
    assert restore_payload["ok"] is True
    assert restore_payload["data"]["restored_count"] == 0
    assert restore_payload["data"]["invalid"] == [
        {
            "routine": _ROUTINE,
            "exercise": exercise_name,
            "reason": "Minimum reps must be a finite number.",
        }
    ]

    with caplog.at_level(logging.ERROR):
        response = client.get("/weekly_summary")

    assert response.status_code == 200

    # The former defect surfaced as a logged TypeError from utils/weekly_summary.py. Its absence
    # is what proves the row never entered the arithmetic, rather than the calculator absorbing it.
    type_error_records = [
        record
        for record in caplog.records
        if record.exc_info is not None and record.exc_info[0] is TypeError
    ]
    assert type_error_records == []


def test_restore_skips_out_of_range_numerics_instead_of_persisting_them(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """Out-of-range numerics are now skipped per row rather than restored unvalidated.

    This node previously asserted that these values restored, rendered, and entered the
    arithmetic with no user-visible signal. Under the full canonical contract they are rejected
    at the boundary, so the surviving assertion is that nothing was written and the reason names
    the first failing field.
    """
    exercise_name = exercise_factory(
        "Fuzz Chest Press",
        primary_muscle_group="Chest",
        secondary_muscle_group=None,
        tertiary_muscle_group=None,
    )

    updates: Dict[str, Any] = {
        "sets": 3,
        "min_rep_range": 20,
        "max_rep_range": 5,
        "rir": 99,
        "rpe": None,
        "weight": 99999.0,
    }
    backup_id = _seed_tampered_backup(
        workout_plan_factory,
        exercise_name,
        updates,
        {
            "sets": "integer",
            "min_rep_range": "integer",
            "max_rep_range": "integer",
            "rir": "integer",
            "rpe": "null",
            "weight": "real",
        },
    )

    restore_response = client.post(
        f"/api/backups/{backup_id}/restore",
        content_type="application/json",
    )
    assert restore_response.status_code == 200
    restore_payload = restore_response.get_json()
    assert restore_payload["data"]["restored_count"] == 0
    assert len(restore_payload["data"]["invalid"]) == 1
    # Weight is checked before RIR and the rep relation, so it is the reported reason.
    assert restore_payload["data"]["invalid"][0]["reason"] == (
        "Weight must be between 0 and 1000 kg."
    )

    with DatabaseHandler() as db:
        stored = db.fetch_one(
            "SELECT COUNT(*) AS row_count FROM user_selection WHERE exercise = ?",
            (exercise_name,),
        )
        assert stored is not None
        assert stored["row_count"] == 0

    assert client.get("/weekly_summary").status_code == 200


def test_restore_preserves_a_null_rir(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """``rir`` is the only nullable bounded column, so NULL must restore, not be rejected.

    The validator has a single ``allow_null`` flag covering all four fields, which cannot express
    "rir nullable, the rest not". The restore path therefore omits ``rir`` -- leaving it UNSET --
    when and only when it is exactly ``None``.
    """
    exercise_name = exercise_factory("Fuzz Null Rir Row", primary_muscle_group="Chest")
    backup_id = _seed_tampered_backup(
        workout_plan_factory,
        exercise_name,
        {"rir": None},
        {"rir": "null"},
    )

    restore_response = client.post(
        f"/api/backups/{backup_id}/restore",
        content_type="application/json",
    )
    assert restore_response.status_code == 200
    restore_payload = restore_response.get_json()
    assert restore_payload["data"]["restored_count"] == 1
    assert restore_payload["data"]["invalid"] == []

    with DatabaseHandler() as db:
        stored = db.fetch_one(
            "SELECT rir, typeof(rir) AS rir_type FROM user_selection WHERE exercise = ?",
            (exercise_name,),
        )
        assert stored is not None
        assert stored["rir"] is None
        assert stored["rir_type"] == "null"


@pytest.mark.parametrize(
    "column,blank_typeof,expected_reason",
    [
        ("rir", "text", "RIR must be a finite number."),
        ("weight", "text", "Weight must be a finite number."),
        ("min_rep_range", "text", "Minimum reps must be a finite number."),
        ("max_rep_range", "text", "Maximum reps must be a finite number."),
    ],
    ids=["rir_blank", "weight_blank", "min_rep_blank", "max_rep_blank"],
)
def test_restore_rejects_blank_bounded_values(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    column,
    blank_typeof,
    expected_reason,
):
    """An empty string must not reach the insert on any bounded column, nullable or not.

    ``validate_workout_bounds(allow_null=True)`` maps ``""`` onto null, which would clear the
    bounds check and then land a blank in a NOT NULL column under SQLite's type affinity. The
    restore path never sets that flag, so a blank stays present and is rejected -- including for
    ``rir``, where NULL itself is legitimate.
    """
    exercise_name = exercise_factory(f"Fuzz Blank {column}", primary_muscle_group="Chest")
    backup_id = _seed_tampered_backup(
        workout_plan_factory,
        exercise_name,
        {column: ""},
        {column: blank_typeof},
    )

    restore_response = client.post(
        f"/api/backups/{backup_id}/restore",
        content_type="application/json",
    )
    assert restore_response.status_code == 200
    restore_payload = restore_response.get_json()
    assert restore_payload["data"]["restored_count"] == 0
    assert len(restore_payload["data"]["invalid"]) == 1
    assert restore_payload["data"]["invalid"][0]["reason"] == expected_reason

    with DatabaseHandler() as db:
        stored = db.fetch_one(
            "SELECT COUNT(*) AS row_count FROM user_selection WHERE exercise = ?",
            (exercise_name,),
        )
        assert stored is not None
        assert stored["row_count"] == 0


def _seed_backup_with_rows(
    workout_plan_factory: Any,
    exercise_names: list[str],
    tamper: Mapping[str, Mapping[str, Any]],
) -> int:
    """Back up several valid plan rows, then rewrite named items in place.

    ``tamper`` maps an exercise name to the column updates applied to its backup item, so a batch
    can carry good and bad rows at once.
    """
    for name in exercise_names:
        workout_plan_factory(exercise_name=name, routine=_ROUTINE)

    backup_id = create_backup(name=_BACKUP_NAME)["id"]

    with DatabaseHandler() as db:
        for name, updates in tamper.items():
            assignments = ", ".join(f"{column} = ?" for column in updates)
            params = tuple(updates.values()) + (backup_id, name)
            rowcount = db.execute_query(
                f"UPDATE program_backup_items SET {assignments} "
                "WHERE backup_id = ? AND exercise = ?",
                params,
            )
            assert rowcount == 1, f"Expected one row for {name!r}, got {rowcount}"

        count_row = db.fetch_one(
            "SELECT COUNT(*) AS cnt FROM program_backup_items WHERE backup_id = ?",
            (backup_id,),
        )
        assert count_row is not None
        assert count_row["cnt"] == len(exercise_names)

    return backup_id


def test_restore_mixed_batch_keeps_valid_rows_and_skips_the_invalid_one(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """One bad row must not cost the user the rest of the backup.

    There is no backup-item editor in this app, so refusing the whole restore would make a legacy
    backup permanently unrestorable. The valid rows are asserted present and byte-correct, not
    merely counted.
    """
    good_one = exercise_factory("Fuzz Batch Good One", primary_muscle_group="Chest")
    good_two = exercise_factory("Fuzz Batch Good Two", primary_muscle_group="Back")
    bad = exercise_factory("Fuzz Batch Bad", primary_muscle_group="Quads")

    backup_id = _seed_backup_with_rows(
        workout_plan_factory,
        [good_one, good_two, bad],
        {bad: {"min_rep_range": "abc"}},
    )

    restore_response = client.post(
        f"/api/backups/{backup_id}/restore",
        content_type="application/json",
    )
    assert restore_response.status_code == 200
    data = restore_response.get_json()["data"]

    assert data["restored_count"] == 2
    assert data["skipped"] == []
    assert len(data["invalid"]) == 1
    assert data["invalid"][0]["exercise"] == bad

    with DatabaseHandler() as db:
        present = {
            row["exercise"]
            for row in db.fetch_all("SELECT exercise FROM user_selection")
        }
        assert present == {good_one, good_two}

        # Byte-correct, not just present: the surviving rows keep their seeded values.
        stored = db.fetch_one(
            "SELECT min_rep_range, max_rep_range, weight FROM user_selection WHERE exercise = ?",
            (good_one,),
        )
        assert stored is not None
        assert stored["min_rep_range"] == 6
        assert stored["max_rep_range"] == 8
        assert stored["weight"] == 50.0

    assert client.get("/weekly_summary").status_code == 200


def test_restore_reports_catalog_and_invalid_rows_on_separate_channels(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """The two skip reasons must not contaminate each other.

    ``skipped`` carries catalog misses only -- the UI copy for it says the exercise is no longer
    in the catalog, which would be a false statement about a bounds failure.
    """
    good = exercise_factory("Fuzz Channels Good", primary_muscle_group="Chest")
    bad_bounds = exercise_factory("Fuzz Channels Bad Bounds", primary_muscle_group="Back")
    dropped = exercise_factory("Fuzz Channels Dropped", primary_muscle_group="Quads")

    backup_id = _seed_backup_with_rows(
        workout_plan_factory,
        [good, bad_bounds, dropped],
        {bad_bounds: {"weight": 99999.0}},
    )

    # Remove one exercise from the catalog after the backup, so its item restores as a catalog miss.
    with DatabaseHandler() as db:
        db.execute_query("DELETE FROM user_selection WHERE exercise = ?", (dropped,))
        db.execute_query("DELETE FROM exercises WHERE exercise_name = ?", (dropped,))

    restore_response = client.post(
        f"/api/backups/{backup_id}/restore",
        content_type="application/json",
    )
    assert restore_response.status_code == 200
    data = restore_response.get_json()["data"]

    assert data["restored_count"] == 1
    assert data["skipped"] == [dropped]
    assert [entry["exercise"] for entry in data["invalid"]] == [bad_bounds]
    assert data["invalid"][0]["reason"] == "Weight must be between 0 and 1000 kg."


def test_restore_stays_replace_mode_while_skipping_an_invalid_row(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """Skipping a row must not turn the restore into a rollback of the whole request.

    Replace mode is unchanged: the previous active program and its logs are still cleared before
    the valid rows are committed. "No partial write" means the invalid backup row is never
    inserted -- not that the previous program survives.
    """
    previous = exercise_factory("Fuzz Replace Previous", primary_muscle_group="Chest")
    good = exercise_factory("Fuzz Replace Good", primary_muscle_group="Back")
    bad = exercise_factory("Fuzz Replace Bad", primary_muscle_group="Quads")

    backup_id = _seed_backup_with_rows(
        workout_plan_factory,
        [good, bad],
        {bad: {"min_rep_range": "abc"}},
    )

    # A pre-existing active program that replace mode must clear.
    workout_plan_factory(exercise_name=previous, routine=_ROUTINE)
    with DatabaseHandler() as db:
        before = db.fetch_one(
            "SELECT COUNT(*) AS cnt FROM user_selection WHERE exercise = ?",
            (previous,),
        )
        assert before is not None
        assert before["cnt"] == 1

    restore_response = client.post(
        f"/api/backups/{backup_id}/restore",
        content_type="application/json",
    )
    assert restore_response.status_code == 200
    assert restore_response.get_json()["data"]["restored_count"] == 1

    with DatabaseHandler() as db:
        present = {
            row["exercise"]
            for row in db.fetch_all("SELECT exercise FROM user_selection")
        }
        assert present == {good}, "replace mode must clear the previous program"

        logs = db.fetch_one("SELECT COUNT(*) AS cnt FROM workout_log")
        assert logs is not None
        assert logs["cnt"] == 0
