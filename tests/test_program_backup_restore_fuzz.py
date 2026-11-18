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
only ``rir``/``rpe`` nullable. ``validate_workout_bounds`` can select blank handling independently,
but its null policy still covers all four bounded fields and cannot express that field-level split.
The restore path therefore omits ``rir`` -- leaving it UNSET -- when and only when it is exactly
``None``, so NULL rir restores while a blank is rejected on every column.

Incidental contract pin
-----------------------
The exact ``utils/workout_validation.py`` messages asserted below are pinned in this file and
nowhere else in the repository. They are asserted verbatim on purpose -- the exact string is what
distinguishes the bounds-rejection branch from the duplicate-row ``VALIDATION_ERROR`` branch, and
it is now also the user-facing ``reason`` the restore response returns -- so editing that copy
reds several nodes here. That is intended, but it means this file is also the sole guard on those
strings.

Execution fields (#567)
-----------------------
The second half of this file covers the four execution columns -- ``execution_style``,
``time_cap_seconds``, ``emom_interval_seconds`` and ``emom_rounds`` -- which follow a different
rule from the bounded columns above. A row skipped for its catalog entry or its bounds is still
skipped per row. But a row that *would be restored* and holds an execution value restore cannot
interpret refuses the **whole** restore, before anything is written: HTTP 400
``VALIDATION_ERROR`` with ``error.reason == "RESTORE_REFUSED"`` and one ``error.rows`` entry per
problem, leaving the plan, the workout log and the backup exactly as they were (ADR-015). A
row already skipped for its catalog entry or its bounds cannot cause a refusal: its execution
values are never examined, because it would not have been written.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import pytest

from utils.database import DatabaseHandler
from utils.program_backup import create_backup, get_active_program_count, restore_backup


_ROUTINE = "GYM - Full Body - Workout A"
_BACKUP_NAME = "Restore Fuzz Backup"

_EXECUTION_COLUMNS: Tuple[str, ...] = (
    "execution_style",
    "time_cap_seconds",
    "emom_interval_seconds",
    "emom_rounds",
)
# SQLite storage class a Python value is expected to keep in program_backup_items. A value the
# column's affinity converts -- the text '60' or the real 60.0 in an INTEGER column -- fails the
# typeof() pin in _seed_tampered_backup instead of silently testing a different stored value.
_STORAGE_CLASS = {
    type(None): "null",
    int: "integer",
    float: "real",
    str: "text",
    bytes: "blob",
}


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

    ``updates`` may name any ``program_backup_items`` column, the four execution columns
    included. Execution-field cases build ``updates`` and ``expected_typeof`` with
    ``_execution_updates()``, which always writes all four columns, so the tampered row is fully
    specified and does not depend on what ``create_backup()`` captured from the seeded plan row.
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
    (
        "sets_zero",
        {"sets": 0},
        {"sets": "integer"},
        "Sets must be at least 1.",
    ),
    (
        "max_rep_fraction",
        {"max_rep_range": 8.5},
        {"max_rep_range": "real"},
        "Maximum reps must be a whole number.",
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

    The validator's null policy covers all four fields, so it cannot express "rir nullable, the
    rest not". The restore path therefore omits ``rir`` -- leaving it UNSET -- when and only when
    it is exactly ``None``.
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

    The validator's legacy ``allow_null=True`` default maps ``""`` onto null, which would clear
    the bounds check and then land a blank in a NOT NULL column under SQLite's type affinity. The
    restore path never enables null or blank acceptance, so a blank stays present and is rejected
    -- including for ``rir``, where NULL itself is legitimate.
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


@pytest.mark.parametrize("include_valid_row", [True, False], ids=["mixed", "all-skipped"])
def test_restore_counts_skipped_rows_before_deduplicating_catalog_names(
    client, clean_db, exercise_factory, workout_plan_factory, workout_log_factory, include_valid_row,
):
    retired = exercise_factory("Repeated Retired Exercise")
    invalid = exercise_factory("Invalid Count Exercise")
    active = exercise_factory("Current Active Exercise")
    workout_plan_factory(exercise_name=retired, routine="Retired A")
    workout_plan_factory(exercise_name=retired, routine="Retired B")
    workout_plan_factory(exercise_name=invalid, routine="Invalid Routine")
    expected_exercises = []
    if include_valid_row:
        retained = exercise_factory("Restorable Exercise")
        workout_plan_factory(exercise_name=retained, routine="Retained Routine")
        expected_exercises.append({"exercise": retained, "routine": "Retained Routine"})
    backup_id = create_backup(name=_BACKUP_NAME)["id"]

    clean_db.execute_query(
        "UPDATE program_backup_items SET sets = ? WHERE backup_id = ? AND exercise = ?",
        (-2, backup_id, invalid),
    )
    clean_db.execute_query("DELETE FROM user_selection WHERE exercise = ?", (retired,))
    clean_db.execute_query("DELETE FROM exercises WHERE exercise_name = ?", (retired,))
    current_plan_id = workout_plan_factory(exercise_name=active, routine="Current Routine")
    workout_log_factory(plan_id=current_plan_id, exercise=active)

    response = client.post(f"/api/backups/{backup_id}/restore", content_type="application/json")

    assert response.status_code == 200, response.get_json()
    payload = response.get_json()
    assert payload["ok"] is True
    assert payload["data"] == {
        "backup_id": backup_id,
        "backup_name": _BACKUP_NAME,
        "restored_count": len(expected_exercises),
        "skipped": [retired],
        "invalid": [{"routine": "Invalid Routine", "exercise": invalid, "reason": "Sets must be at least 1."}],
    }
    assert "Skipped 3 rows (2 missing from the catalog, 1 with invalid values)." in payload["message"]
    cleared_notice = "Your current plan and workout log were cleared."
    if include_valid_row:
        assert payload["message"].startswith("Restored 1 exercise")
        assert cleared_notice not in payload["message"]
    else:
        assert payload["message"].startswith("Nothing was restored")
        assert payload["message"].endswith(cleared_notice)
    assert clean_db.fetch_all("SELECT exercise, routine FROM user_selection") == expected_exercises
    assert clean_db.fetch_all("SELECT id FROM workout_log") == []


def test_restore_stores_the_parsed_integer_count(
    client, clean_db, exercise_factory, workout_plan_factory,
):
    exercise = exercise_factory("Padded Count Exercise")
    workout_plan_factory(exercise_name=exercise, routine="Padded Routine")
    backup_id = create_backup(name=_BACKUP_NAME)["id"]
    # "\x1c" is whitespace to Python's number parser but not to SQLite, so the
    # raw backup value would land in user_selection as text.
    clean_db.execute_query(
        "UPDATE program_backup_items SET sets = ? WHERE backup_id = ?",
        ("\x1c4", backup_id),
    )

    response = client.post(f"/api/backups/{backup_id}/restore", content_type="application/json")

    assert response.status_code == 200, response.get_json()
    assert clean_db.fetch_all("SELECT sets, typeof(sets) AS kind FROM user_selection") == [
        {"sets": 4, "kind": "integer"},
    ]


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


# ---------------------------------------------------------------------------
# Execution fields (#567): missing values, whole-restore refusal, untouched plan
# ---------------------------------------------------------------------------

_EN_DASH = "–"
_REFUSAL_CLOSING = (
    "The backup itself was left unchanged and cannot be restored until these values are corrected."
)

ExecutionFields = Tuple[Any, Any, Any, Any]


def _refusal_opening(offending_rows: int) -> str:
    """The fixed opening of the refusal message, up to and including the colon before the rows."""
    return (
        f"Backup '{_BACKUP_NAME}' was not restored. Your current plan and workout log were "
        f"preserved; nothing was changed. {offending_rows} row(s) hold execution settings that "
        "cannot be restored: "
    )


def _execution_updates(fields: ExecutionFields) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """``updates`` and ``expected_typeof`` for ``_seed_tampered_backup``, for all four columns."""
    updates = dict(zip(_EXECUTION_COLUMNS, fields))
    expected_typeof = {column: _STORAGE_CLASS[type(value)] for column, value in updates.items()}
    return updates, expected_typeof


def _refused_row(exercise: str, field: str, value: str, problem: str) -> Dict[str, str]:
    """One expected ``error.rows`` entry."""
    return {
        "routine": _ROUTINE,
        "exercise": exercise,
        "field": field,
        "value": value,
        "problem": problem,
    }


def _stored_execution_fields(exercise: str) -> Dict[str, Any]:
    """A restored plan row's four fields and their storage classes."""
    selected = ", ".join(
        f"{column}, typeof({column}) AS {column}_type" for column in _EXECUTION_COLUMNS
    )
    with DatabaseHandler() as db:
        stored = db.fetch_one(
            f"SELECT {selected} FROM user_selection WHERE exercise = ?", (exercise,)
        )
    assert stored is not None
    return dict(stored)


def _expected_execution_fields(fields: ExecutionFields) -> Dict[str, Any]:
    expected: Dict[str, Any] = {}
    for column, value in zip(_EXECUTION_COLUMNS, fields):
        expected[column] = value
        expected[f"{column}_type"] = _STORAGE_CLASS[type(value)]
    return expected


def _snapshot_database() -> Dict[str, List[Dict[str, Any]]]:
    """Every row of the plan, the log and both backup tables, ids included, in id order."""
    tables = ("user_selection", "workout_log", "program_backups", "program_backup_items")
    with DatabaseHandler() as db:
        return {
            table: [dict(row) for row in db.fetch_all(f"SELECT * FROM {table} ORDER BY id")]
            for table in tables
        }


def _seed_current_plan_and_log(
    exercise_factory: Any,
    workout_plan_factory: Any,
    workout_log_factory: Any,
) -> None:
    """Give a restore something to destroy: a plan row the backup does not hold, and its log.

    Seeded after the backup is taken. A restore that went ahead would delete both; a restore
    that was rolled back would restore them, which is why the call-spy test exists as well.
    """
    name = exercise_factory("Fuzz Current Plan Row", primary_muscle_group="Back")
    plan_id = workout_plan_factory(exercise_name=name, routine=_ROUTINE)
    with DatabaseHandler() as db:
        db.execute_query(
            "UPDATE user_selection SET execution_style = 'amrap', time_cap_seconds = 90 "
            "WHERE id = ?",
            (plan_id,),
        )
    workout_log_factory(plan_id=plan_id, exercise=name)


def _assert_restore_refused(
    client: Any,
    backup_id: int,
    expected_rows: Sequence[Mapping[str, str]],
    offending_rows: Optional[int] = None,
) -> Dict[str, Any]:
    """Request the restore and assert the whole refusal contract.

    The response: 400, ``VALIDATION_ERROR``, ``reason`` ``RESTORE_REFUSED``, the fixed opening
    and closing sentences, every offending row named in the message, and the matching
    ``rows`` entries.

    The database: ``user_selection``, ``workout_log`` and both backup tables hold exactly the
    rows they held before the request, ids included, and the refused backup is still listed.

    ``expected_rows`` has one entry per *problem*. ``offending_rows`` is the number of backup
    rows the opening sentence must count; it defaults to ``len(expected_rows)``, which is right
    only when every offending row has exactly one problem. Returns the response's ``error``
    object for assertions a single case adds on top.
    """
    if offending_rows is None:
        offending_rows = len(expected_rows)
    before = _snapshot_database()
    assert before["user_selection"], "seed a current plan first, or the snapshot proves nothing"
    assert before["workout_log"], "seed a logged session first, or the snapshot proves nothing"
    active_before = get_active_program_count()

    response = client.post(
        f"/api/backups/{backup_id}/restore",
        content_type="application/json",
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body["ok"] is False
    error = body["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert error["reason"] == "RESTORE_REFUSED"

    message = error["message"]
    assert message.startswith(_refusal_opening(offending_rows)), message
    assert message.endswith(_REFUSAL_CLOSING), message
    for row in expected_rows:
        row_text = f"{row['routine']} / {row['exercise']}: {row['problem']}"
        assert row_text in message, f"{row_text!r} is not named in {message!r}"

    def by_row(entry: Mapping[str, str]) -> Tuple[str, str]:
        return (entry["exercise"], entry["field"])

    assert sorted(error["rows"], key=by_row) == sorted(
        (dict(row) for row in expected_rows), key=by_row
    )

    # A refused restore changes nothing: same ids, same values, every logged session intact, and
    # the stored value that caused the refusal neither normalized nor discarded.
    assert _snapshot_database() == before
    assert get_active_program_count() == active_before
    listed = client.get("/api/backups").get_json()["data"]
    assert backup_id in [entry["id"] for entry in listed]
    return error


# case id, stored (style, time cap, interval, rounds), restored (style, time cap, interval, rounds)
_MISSING_VALUE_CASES: List[Tuple[str, ExecutionFields, ExecutionFields]] = [
    # A missing style is restored as the stored text 'standard'.
    ("style_and_timing_missing", (None, None, None, None), ("standard", None, None, None)),
    # A missing timing value stays empty: never the 60 / 60 / 5 the plan page would fill in.
    ("amrap_time_cap_missing", ("amrap", None, None, None), ("amrap", None, None, None)),
    ("emom_rounds_missing", ("emom", None, 60, None), ("emom", None, 60, None)),
    ("emom_interval_missing", ("emom", None, None, 10), ("emom", None, None, 10)),
    ("emom_both_missing", ("emom", None, None, None), ("emom", None, None, None)),
]


@pytest.mark.parametrize(
    "stored,restored",
    [case[1:] for case in _MISSING_VALUE_CASES],
    ids=[case[0] for case in _MISSING_VALUE_CASES],
)
def test_restore_never_refuses_or_defaults_a_missing_execution_value(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    stored,
    restored,
):
    """SQL NULL is *missing* -- never an error, and never filled with a default."""
    exercise_name = exercise_factory("Fuzz Missing Execution Value", primary_muscle_group="Chest")
    updates, expected_typeof = _execution_updates(stored)
    backup_id = _seed_tampered_backup(workout_plan_factory, exercise_name, updates, expected_typeof)

    restore_response = client.post(
        f"/api/backups/{backup_id}/restore",
        content_type="application/json",
    )

    assert restore_response.status_code == 200
    data = restore_response.get_json()["data"]
    assert data["restored_count"] == 1
    assert data["skipped"] == []
    assert data["invalid"] == []
    assert _stored_execution_fields(exercise_name) == _expected_execution_fields(restored)


@pytest.mark.parametrize(
    "style",
    ["tabata", "EMOM", " emom", ""],
    ids=["tabata", "upper_case", "leading_space", "empty_string"],
)
def test_restore_refuses_an_unrecognized_execution_style(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    workout_log_factory,
    style,
):
    """One unrecognized style refuses the whole restore and changes nothing.

    No case folding and no trimming -- ``EMOM`` and `` emom`` are not ``emom`` -- and the empty
    string is a present value, not a missing one.
    """
    exercise_name = exercise_factory("Fuzz Unrecognized Style", primary_muscle_group="Chest")
    updates, expected_typeof = _execution_updates((style, None, None, None))
    backup_id = _seed_tampered_backup(workout_plan_factory, exercise_name, updates, expected_typeof)
    _seed_current_plan_and_log(exercise_factory, workout_plan_factory, workout_log_factory)

    _assert_restore_refused(
        client,
        backup_id,
        [
            _refused_row(
                exercise_name,
                "execution_style",
                style,
                f'execution style "{style}" is not recognized',
            )
        ],
    )

    # No row anywhere was converted to standard: the backup still holds the value as stored.
    with DatabaseHandler() as db:
        item = db.fetch_one(
            "SELECT execution_style, typeof(execution_style) AS style_type "
            "FROM program_backup_items WHERE backup_id = ?",
            (backup_id,),
        )
    assert item is not None
    assert item["execution_style"] == style
    assert item["style_type"] == "text"


def test_restore_refusal_names_every_offending_row(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    workout_log_factory,
):
    """With more than five offending rows, every one is named -- none is cut off."""
    # exercise -> (backup-item updates, refused field, rendered value, problem)
    offending: Dict[str, Tuple[Dict[str, Any], str, str, str]] = {
        "Fuzz Many Tabata": (
            {"execution_style": "tabata"},
            "execution_style",
            "tabata",
            'execution style "tabata" is not recognized',
        ),
        "Fuzz Many Upper Case": (
            {"execution_style": "EMOM"},
            "execution_style",
            "EMOM",
            'execution style "EMOM" is not recognized',
        ),
        "Fuzz Many Leading Space": (
            {"execution_style": " emom"},
            "execution_style",
            " emom",
            'execution style " emom" is not recognized',
        ),
        "Fuzz Many Empty Style": (
            {"execution_style": ""},
            "execution_style",
            "",
            'execution style "" is not recognized',
        ),
        "Fuzz Many Time Cap Too Long": (
            {"execution_style": "amrap", "time_cap_seconds": 601},
            "time_cap_seconds",
            "601",
            f"time cap 601 is outside 10{_EN_DASH}600",
        ),
        "Fuzz Many Stray Time Cap": (
            {"execution_style": "standard", "time_cap_seconds": 60},
            "time_cap_seconds",
            "60",
            "time cap 60 is not used by the standard style",
        ),
    }
    restorable = "Fuzz Many Valid Amrap"
    names = list(offending) + [restorable]
    for name in names:
        exercise_factory(name, primary_muscle_group="Chest")

    tamper: Dict[str, Dict[str, Any]] = {name: case[0] for name, case in offending.items()}
    tamper[restorable] = {"execution_style": "amrap", "time_cap_seconds": 120}
    backup_id = _seed_backup_with_rows(workout_plan_factory, names, tamper)
    _seed_current_plan_and_log(exercise_factory, workout_plan_factory, workout_log_factory)

    _assert_restore_refused(
        client,
        backup_id,
        [
            _refused_row(name, field, value, problem)
            for name, (_updates, field, value, problem) in offending.items()
        ],
    )


# case id, stored (style, time cap, interval, rounds), refused field, rendered value, problem
_INVALID_TIMING_CASES: List[Tuple[str, ExecutionFields, str, str, str]] = [
    # A value the plan page would reject for that style -- not a whole number ...
    (
        "time_cap_text",
        ("amrap", "abc", None, None),
        "time_cap_seconds",
        "abc",
        'time cap "abc" is not a whole number',
    ),
    (
        "time_cap_empty_string",
        ("amrap", "", None, None),
        "time_cap_seconds",
        "",
        'time cap "" is not a whole number',
    ),
    (
        "time_cap_fractional",
        ("amrap", 12.5, None, None),
        "time_cap_seconds",
        "12.5",
        'time cap "12.5" is not a whole number',
    ),
    # ... or outside the limits.
    (
        "time_cap_zero",
        ("amrap", 0, None, None),
        "time_cap_seconds",
        "0",
        f"time cap 0 is outside 10{_EN_DASH}600",
    ),
    (
        "time_cap_negative",
        ("amrap", -5, None, None),
        "time_cap_seconds",
        "-5",
        f"time cap -5 is outside 10{_EN_DASH}600",
    ),
    (
        "time_cap_below_min",
        ("amrap", 9, None, None),
        "time_cap_seconds",
        "9",
        f"time cap 9 is outside 10{_EN_DASH}600",
    ),
    (
        "time_cap_above_max",
        ("amrap", 601, None, None),
        "time_cap_seconds",
        "601",
        f"time cap 601 is outside 10{_EN_DASH}600",
    ),
    (
        "interval_below_min",
        ("emom", None, 14, 5),
        "emom_interval_seconds",
        "14",
        f"EMOM interval 14 is outside 15{_EN_DASH}180",
    ),
    (
        "interval_above_max",
        ("emom", None, 181, 5),
        "emom_interval_seconds",
        "181",
        f"EMOM interval 181 is outside 15{_EN_DASH}180",
    ),
    (
        "rounds_below_min",
        ("emom", None, 60, 0),
        "emom_rounds",
        "0",
        f"EMOM rounds 0 is outside 1{_EN_DASH}20",
    ),
    (
        "rounds_above_max",
        ("emom", None, 60, 21),
        "emom_rounds",
        "21",
        f"EMOM rounds 21 is outside 1{_EN_DASH}20",
    ),
    # A value stored against a style that does not use it.
    (
        "standard_with_time_cap",
        ("standard", 60, None, None),
        "time_cap_seconds",
        "60",
        "time cap 60 is not used by the standard style",
    ),
    (
        "amrap_with_interval",
        ("amrap", 60, 60, None),
        "emom_interval_seconds",
        "60",
        "EMOM interval 60 is not used by the amrap style",
    ),
    (
        "amrap_with_rounds",
        ("amrap", 60, None, 5),
        "emom_rounds",
        "5",
        "EMOM rounds 5 is not used by the amrap style",
    ),
    # The combination the application cannot write: for emom the plan page clears the time cap.
    (
        "emom_with_time_cap_reproduction_b",
        ("emom", 600, 60, 10),
        "time_cap_seconds",
        "600",
        "time cap 600 is not used by the emom style",
    ),
    # A missing style counts as standard.
    (
        "missing_style_with_time_cap",
        (None, 60, None, None),
        "time_cap_seconds",
        "60",
        "time cap 60 is not used by the standard style",
    ),
]


@pytest.mark.parametrize(
    "stored,field,value,problem",
    [case[1:] for case in _INVALID_TIMING_CASES],
    ids=[case[0] for case in _INVALID_TIMING_CASES],
)
def test_restore_refuses_a_present_invalid_timing_value(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    workout_log_factory,
    stored,
    field,
    value,
    problem,
):
    """The message names the row, the field and the stored value; nothing is silently
    repaired, cleared or discarded."""
    exercise_name = exercise_factory("Fuzz Invalid Timing", primary_muscle_group="Chest")
    updates, expected_typeof = _execution_updates(stored)
    backup_id = _seed_tampered_backup(workout_plan_factory, exercise_name, updates, expected_typeof)
    _seed_current_plan_and_log(exercise_factory, workout_plan_factory, workout_log_factory)

    _assert_restore_refused(
        client,
        backup_id,
        [_refused_row(exercise_name, field, value, problem)],
    )


def _restore_write_statements(recorded: Sequence[str]) -> List[str]:
    """The statements a restore that goes ahead issues: the transaction, the deletes, the inserts."""
    writes = []
    for query in recorded:
        normalized = " ".join(query.split()).upper()
        if normalized.startswith(("BEGIN IMMEDIATE", "DELETE", "INSERT")):
            writes.append(normalized)
    return writes


def _record_execute_query(monkeypatch: pytest.MonkeyPatch) -> List[str]:
    """Record every statement that goes through ``DatabaseHandler.execute_query`` from here on."""
    recorded: List[str] = []
    original_execute_query = DatabaseHandler.execute_query

    def recording_execute_query(self, query, params=None, *, commit=True):
        recorded.append(query)
        return original_execute_query(self, query, params, commit=commit)

    monkeypatch.setattr(DatabaseHandler, "execute_query", recording_execute_query)
    return recorded


def test_refused_restore_issues_no_write_statement(
    clean_db,
    exercise_factory,
    workout_plan_factory,
    workout_log_factory,
    monkeypatch,
):
    """Restore decides to refuse *before* it writes anything.

    The snapshot comparison alone cannot prove this. A refusal raised after the two DELETEs
    still leaves the tables intact, because ``DatabaseHandler.__exit__`` rolls the transaction
    back. Only the absence of ``BEGIN IMMEDIATE``, ``DELETE`` and ``INSERT`` shows the decision
    came first.
    """
    from utils.program_backup import BackupRestoreRefused

    exercise_name = exercise_factory("Fuzz Call Spy Refused", primary_muscle_group="Chest")
    updates, expected_typeof = _execution_updates(("tabata", None, None, None))
    backup_id = _seed_tampered_backup(workout_plan_factory, exercise_name, updates, expected_typeof)
    _seed_current_plan_and_log(exercise_factory, workout_plan_factory, workout_log_factory)

    recorded = _record_execute_query(monkeypatch)

    with pytest.raises(BackupRestoreRefused):
        restore_backup(backup_id)

    assert _restore_write_statements(recorded) == []


def test_call_spy_sees_the_writes_of_a_restore_that_goes_ahead(
    clean_db,
    exercise_factory,
    workout_plan_factory,
    monkeypatch,
):
    """Positive control for the call-spy test above.

    If restore stopped issuing these statements through ``execute_query``, the refusal test
    would pass without proving anything. This keeps its oracle honest.
    """
    names = [
        exercise_factory("Fuzz Call Spy Good One", primary_muscle_group="Chest"),
        exercise_factory("Fuzz Call Spy Good Two", primary_muscle_group="Back"),
    ]
    backup_id = _seed_backup_with_rows(workout_plan_factory, names, {})

    recorded = _record_execute_query(monkeypatch)

    result = restore_backup(backup_id)

    assert result["restored_count"] == 2
    writes = _restore_write_statements(recorded)
    assert writes[:3] == [
        "BEGIN IMMEDIATE",
        "DELETE FROM WORKOUT_LOG",
        "DELETE FROM USER_SELECTION",
    ]
    inserts = writes[3:]
    assert len(inserts) == 2, "one INSERT per restored row, not executemany"
    assert all(statement.startswith("INSERT INTO USER_SELECTION") for statement in inserts)


def test_refusal_is_its_own_exception_carrying_the_backup_name_and_rows(
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """``BackupRestoreRefused`` derives from ``Exception`` directly.

    A ``ValueError`` subclass would be answered as ``NOT_FOUND`` 404 by the route, and anything
    caught as ``sqlite3.Error`` would be treated as a failed write. The exception carries what
    the route needs to build the message: the backup's name and the rows, already rendered to
    text.
    """
    from utils.program_backup import BackupRestoreRefused

    assert BackupRestoreRefused.__bases__ == (Exception,)

    exercise_name = exercise_factory("Fuzz Refusal Exception", primary_muscle_group="Chest")
    updates, expected_typeof = _execution_updates(("emom", 600, 60, 10))
    backup_id = _seed_tampered_backup(workout_plan_factory, exercise_name, updates, expected_typeof)

    with pytest.raises(BackupRestoreRefused) as excinfo:
        restore_backup(backup_id)

    assert excinfo.value.backup_name == _BACKUP_NAME
    assert excinfo.value.rows == [
        _refused_row(
            exercise_name,
            "time_cap_seconds",
            "600",
            "time cap 600 is not used by the emom style",
        )
    ]


def test_uncatalogued_row_with_a_bad_style_is_skipped_not_refused(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """Only rows that would be restored can refuse a restore.

    A row already skipped because its exercise left the catalog is reported in ``skipped`` as
    before, whatever its execution values are, and the other rows are restored with theirs.
    """
    good = exercise_factory("Fuzz Skipped Style Good", primary_muscle_group="Chest")
    dropped = exercise_factory("Fuzz Skipped Style Dropped", primary_muscle_group="Quads")

    backup_id = _seed_backup_with_rows(
        workout_plan_factory,
        [good, dropped],
        {
            good: {"execution_style": "amrap", "time_cap_seconds": 120},
            dropped: {"execution_style": "tabata", "time_cap_seconds": 601},
        },
    )
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
    assert data["invalid"] == []
    assert _stored_execution_fields(good) == _expected_execution_fields(("amrap", 120, None, None))


def test_out_of_bounds_row_with_a_bad_style_is_skipped_not_refused(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """A row skipped for its bounds does not refuse the restore.

    It is reported in ``invalid`` with the bounds reason, exactly as before; its unrecognized
    style is never examined because the row would not have been written.
    """
    good = exercise_factory("Fuzz Invalid Style Good", primary_muscle_group="Chest")
    bad_bounds = exercise_factory("Fuzz Invalid Style Bad Bounds", primary_muscle_group="Back")

    backup_id = _seed_backup_with_rows(
        workout_plan_factory,
        [good, bad_bounds],
        {
            good: {
                "execution_style": "emom",
                "emom_interval_seconds": 60,
                "emom_rounds": 10,
            },
            bad_bounds: {"weight": 99999.0, "execution_style": "tabata"},
        },
    )

    restore_response = client.post(
        f"/api/backups/{backup_id}/restore",
        content_type="application/json",
    )

    assert restore_response.status_code == 200
    data = restore_response.get_json()["data"]
    assert data["restored_count"] == 1
    assert data["skipped"] == []
    assert data["invalid"] == [
        {
            "routine": _ROUTINE,
            "exercise": bad_bounds,
            "reason": "Weight must be between 0 and 1000 kg.",
        }
    ]
    assert _stored_execution_fields(good) == _expected_execution_fields(("emom", None, 60, 10))

    with DatabaseHandler() as db:
        present = {
            row["exercise"] for row in db.fetch_all("SELECT exercise FROM user_selection")
        }
    assert present == {good}


# ---------------------------------------------------------------------------
# Execution fields (#567): what the count counts, the separators, the style-only rule
# ---------------------------------------------------------------------------


def test_one_row_with_two_problems_is_counted_once_and_named_twice(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    workout_log_factory,
):
    """``<n> row(s)`` counts offending backup rows, not problems.

    One ``standard`` row holding both a time cap and an EMOM interval is one row to correct.
    The message says ``1 row(s)``, names the row once per problem, and ``error.rows`` carries
    both entries.
    """
    exercise_name = exercise_factory("Fuzz Two Problems", primary_muscle_group="Chest")
    updates, expected_typeof = _execution_updates(("standard", 60, 45, None))
    backup_id = _seed_tampered_backup(workout_plan_factory, exercise_name, updates, expected_typeof)
    _seed_current_plan_and_log(exercise_factory, workout_plan_factory, workout_log_factory)

    error = _assert_restore_refused(
        client,
        backup_id,
        [
            _refused_row(
                exercise_name,
                "time_cap_seconds",
                "60",
                "time cap 60 is not used by the standard style",
            ),
            _refused_row(
                exercise_name,
                "emom_interval_seconds",
                "45",
                "EMOM interval 45 is not used by the standard style",
            ),
        ],
        offending_rows=1,
    )

    assert len(error["rows"]) == 2
    assert error["message"].count(f"{_ROUTINE} / {exercise_name}: ") == 2


def test_refusal_exception_counts_backup_rows_not_problems(
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """``BackupRestoreRefused.row_count`` is the number of offending backup rows.

    It is a separate number from ``len(rows)``, which has one entry per problem. The route
    builds ``<n> row(s)`` from ``row_count``; if either side used ``len(rows)`` instead, a row
    with two problems would be announced as two rows.
    """
    from utils.program_backup import BackupRestoreRefused

    exercise_name = exercise_factory("Fuzz Row Count", primary_muscle_group="Chest")
    updates, expected_typeof = _execution_updates(("standard", 60, 45, None))
    backup_id = _seed_tampered_backup(workout_plan_factory, exercise_name, updates, expected_typeof)

    with pytest.raises(BackupRestoreRefused) as excinfo:
        restore_backup(backup_id)

    assert excinfo.value.row_count == 1
    assert len(excinfo.value.rows) == 2
    assert {row["exercise"] for row in excinfo.value.rows} == {exercise_name}
    assert {row["field"] for row in excinfo.value.rows} == {
        "time_cap_seconds",
        "emom_interval_seconds",
    }


def test_refusal_message_is_pinned_exactly_for_several_rows(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    workout_log_factory,
):
    """The whole message, character for character, for three offending rows and four problems.

    The Backup Center shows this text and nothing else, so its shape is part of the contract:
    the row segments are joined by ``; ``, the last one ends with ``. `` before the closing
    sentence, a row with two problems is named twice but counted once, rows appear in backup
    order, and the valid row is not mentioned. ``error.rows`` holds the same four entries in
    the same order.
    """
    unrecognized = "Fuzz Exact A Unrecognized"
    two_problems = "Fuzz Exact B Two Problems"
    out_of_range = "Fuzz Exact C Time Cap"
    valid = "Fuzz Exact D Valid"
    names = [unrecognized, two_problems, out_of_range, valid]
    for name in names:
        exercise_factory(name, primary_muscle_group="Chest")

    backup_id = _seed_backup_with_rows(
        workout_plan_factory,
        names,
        {
            unrecognized: {"execution_style": "tabata"},
            two_problems: {
                "execution_style": "standard",
                "time_cap_seconds": 60,
                "emom_rounds": 5,
            },
            out_of_range: {"execution_style": "amrap", "time_cap_seconds": 601},
            valid: {"execution_style": "amrap", "time_cap_seconds": 120},
        },
    )
    # The order the message is expected in is the backup's own item order.
    with DatabaseHandler() as db:
        backup_order = [
            row["exercise"]
            for row in db.fetch_all(
                "SELECT exercise FROM program_backup_items WHERE backup_id = ? ORDER BY id",
                (backup_id,),
            )
        ]
    assert backup_order == names
    _seed_current_plan_and_log(exercise_factory, workout_plan_factory, workout_log_factory)

    expected_rows = [
        _refused_row(
            unrecognized,
            "execution_style",
            "tabata",
            'execution style "tabata" is not recognized',
        ),
        _refused_row(
            two_problems,
            "time_cap_seconds",
            "60",
            "time cap 60 is not used by the standard style",
        ),
        _refused_row(
            two_problems,
            "emom_rounds",
            "5",
            "EMOM rounds 5 is not used by the standard style",
        ),
        _refused_row(
            out_of_range,
            "time_cap_seconds",
            "601",
            f"time cap 601 is outside 10{_EN_DASH}600",
        ),
    ]

    error = _assert_restore_refused(client, backup_id, expected_rows, offending_rows=3)

    # Written out in full rather than assembled from the helpers above, so a change to a
    # separator or to a sentence cannot move the expectation along with it.
    assert error["message"] == (
        "Backup 'Restore Fuzz Backup' was not restored. Your current plan and workout log were "
        "preserved; nothing was changed. 3 row(s) hold execution settings that cannot be "
        "restored: "
        'GYM - Full Body - Workout A / Fuzz Exact A Unrecognized: execution style "tabata" is '
        "not recognized; "
        "GYM - Full Body - Workout A / Fuzz Exact B Two Problems: time cap 60 is not used by "
        "the standard style; "
        "GYM - Full Body - Workout A / Fuzz Exact B Two Problems: EMOM rounds 5 is not used by "
        "the standard style; "
        "GYM - Full Body - Workout A / Fuzz Exact C Time Cap: time cap 601 is outside "
        "10–600. "
        "The backup itself was left unchanged and cannot be restored until these values are "
        "corrected."
    )
    assert error["rows"] == expected_rows


@pytest.mark.parametrize(
    ("stored_routine", "displayed_routine"),
    [
        (b"\x00\xff" * 512, "<binary, 1024 bytes>"),
        (b"", "<binary, 0 bytes>"),
        ("Long routine name — " * 8, "Long routine name — " * 8),
    ],
    ids=["binary", "empty_binary", "full_text"],
)
def test_refusal_summarizes_binary_routine_names_and_preserves_text(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    workout_log_factory,
    stored_routine,
    displayed_routine,
):
    exercise_name = exercise_factory("Fuzz Routine Display", primary_muscle_group="Chest")
    updates, expected_typeof = _execution_updates(("tabata", None, None, None))
    updates["routine"] = stored_routine
    expected_typeof["routine"] = _STORAGE_CLASS[type(stored_routine)]
    backup_id = _seed_tampered_backup(workout_plan_factory, exercise_name, updates, expected_typeof)
    _seed_current_plan_and_log(exercise_factory, workout_plan_factory, workout_log_factory)

    expected_row = _refused_row(
        exercise_name,
        "execution_style",
        "tabata",
        'execution style "tabata" is not recognized',
    )
    expected_row["routine"] = displayed_routine
    error = _assert_restore_refused(client, backup_id, [expected_row])

    assert error["rows"][0]["routine"] == displayed_routine
    assert error["message"].count(f"{displayed_routine} / {exercise_name}:") == 1


def test_unrecognized_style_is_the_only_problem_reported_for_its_row(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    workout_log_factory,
):
    """With no recognized style there is nothing to judge the timing values against.

    The row's time cap, interval and rounds are each outside every limit, yet the refusal
    names the style alone: one ``error.rows`` entry and one segment in the message.
    """
    exercise_name = exercise_factory("Fuzz Style Only", primary_muscle_group="Chest")
    updates, expected_typeof = _execution_updates(("tabata", 601, 14, 21))
    backup_id = _seed_tampered_backup(workout_plan_factory, exercise_name, updates, expected_typeof)
    _seed_current_plan_and_log(exercise_factory, workout_plan_factory, workout_log_factory)

    error = _assert_restore_refused(
        client,
        backup_id,
        [
            _refused_row(
                exercise_name,
                "execution_style",
                "tabata",
                'execution style "tabata" is not recognized',
            )
        ],
    )

    assert len(error["rows"]) == 1
    message = error["message"]
    assert message.count(f"{_ROUTINE} / {exercise_name}: ") == 1
    for label in ("time cap", "EMOM interval", "EMOM rounds"):
        assert label not in message
