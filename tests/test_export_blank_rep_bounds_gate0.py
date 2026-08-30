"""Blank/null plan-to-log rep-bound compatibility and mutation contracts.

``POST /export_to_workout_log`` has no rep-bound request payload.  It validates
the complete persisted ``user_selection`` source set, then copies accepted rows
to ``workout_log``. Exact blanks are rejected without repairing the source;
actual null and numeric strings remain accepted at the service seam.

The canonical source schema declares both rep bounds ``NOT NULL`` and SQLite
coerces numeric-looking text under INTEGER affinity.  Actual ``None`` and raw
numeric-string compatibility are therefore exercised at the service seam with a
capturing database handler; weakening or recreating the schema would be a false
oracle and is explicitly outside this packet.
"""
from __future__ import annotations

from typing import Any

import pytest

import utils.export_service as export_service
from utils.database import DatabaseHandler
from utils.program_backup import create_backup
from utils.rep_range_integrity import scan_export_bounds


ROUTINE = "GYM - Full Body - Workout A"


def _seed_plan(
    clean_db,
    exercise_factory,
    workout_plan_factory,
    *,
    exercise: str,
    minimum: Any,
    maximum: Any,
) -> int:
    exercise_factory(exercise, primary_muscle_group="Chest")
    plan_id = workout_plan_factory(exercise_name=exercise, routine=ROUTINE)
    clean_db.execute_query(
        "UPDATE user_selection SET min_rep_range = ?, max_rep_range = ? WHERE id = ?",
        (minimum, maximum, plan_id),
    )
    return plan_id


def _error_envelope(message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "status": "error",
        "message": message,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": message,
            "requestId": None,
        },
    }


@pytest.mark.parametrize(
    "minimum,maximum,minimum_type,maximum_type,field_message",
    [
        ("", 12, "text", "integer", "Minimum reps must be a finite number."),
        (8, "", "integer", "text", "Maximum reps must be a finite number."),
        ("", "", "text", "text", "Minimum reps must be a finite number."),
    ],
    ids=["min_blank", "max_blank", "both_blank"],
)
def test_exact_blank_rep_bounds_are_rejected_without_source_repair(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    workout_log_factory,
    minimum,
    maximum,
    minimum_type,
    maximum_type,
    field_message,
):
    """Exact blanks stay TEXT in the source but never reach the workout log."""
    exercise = "Gate Zero Blank Press"
    plan_id = _seed_plan(
        clean_db,
        exercise_factory,
        workout_plan_factory,
        exercise=exercise,
        minimum=minimum,
        maximum=maximum,
    )
    workout_log_factory(plan_id=plan_id, exercise=exercise)
    before_source = clean_db.fetch_all(
        "SELECT *, typeof(min_rep_range) AS min_type, "
        "typeof(max_rep_range) AS max_type FROM user_selection ORDER BY id"
    )
    before_log = clean_db.fetch_all("SELECT * FROM workout_log ORDER BY id")
    before_backups = clean_db.fetch_all("SELECT * FROM program_backups ORDER BY id")

    response = client.post("/export_to_workout_log")

    message = (
        f"{field_message} Invalid plan value on: {ROUTINE} / {exercise}. "
        "Fix these in the Workout Plan editor."
    )
    assert response.status_code == 400
    assert response.content_type == "application/json"
    assert response.get_json() == _error_envelope(message)
    assert scan_export_bounds() == [
        {"routine": ROUTINE, "exercise": exercise, "reason": field_message}
    ]

    with DatabaseHandler() as db:
        assert db.fetch_all(
            "SELECT *, typeof(min_rep_range) AS min_type, "
            "typeof(max_rep_range) AS max_type FROM user_selection ORDER BY id"
        ) == before_source
        assert before_source[0]["min_type"] == minimum_type
        assert before_source[0]["max_type"] == maximum_type
        assert db.fetch_all("SELECT * FROM workout_log ORDER BY id") == before_log
        assert db.fetch_all("SELECT * FROM program_backups ORDER BY id") == before_backups
        assert db.fetch_all("SELECT * FROM program_backup_items ORDER BY id") == []


@pytest.mark.parametrize(
    "minimum,maximum,field_message",
    [
        ("   ", 12, "Minimum reps must be a finite number."),
        (8, "\t ", "Maximum reps must be a finite number."),
        (" ", "\t", "Minimum reps must be a finite number."),
    ],
    ids=["min_whitespace", "max_whitespace", "both_whitespace"],
)
def test_whitespace_only_rep_bounds_keep_exact_rejection_and_no_data_write(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    minimum,
    maximum,
    field_message,
):
    """Whitespace is already invalid; Gate 1 must not broaden the accepted set."""
    exercise = "Gate Zero Whitespace Press"
    _seed_plan(
        clean_db,
        exercise_factory,
        workout_plan_factory,
        exercise=exercise,
        minimum=minimum,
        maximum=maximum,
    )
    before_source = clean_db.fetch_all(
        "SELECT *, typeof(min_rep_range) AS min_type, "
        "typeof(max_rep_range) AS max_type FROM user_selection ORDER BY id"
    )
    before_log = clean_db.fetch_all("SELECT * FROM workout_log ORDER BY id")
    before_backups = clean_db.fetch_all("SELECT * FROM program_backups ORDER BY id")

    response = client.post("/export_to_workout_log")

    message = (
        f"{field_message} Invalid plan value on: {ROUTINE} / {exercise}. "
        "Fix these in the Workout Plan editor."
    )
    assert response.status_code == 400
    assert response.content_type == "application/json"
    assert response.get_json() == _error_envelope(message)

    with DatabaseHandler() as db:
        assert db.fetch_all(
            "SELECT *, typeof(min_rep_range) AS min_type, "
            "typeof(max_rep_range) AS max_type FROM user_selection ORDER BY id"
        ) == before_source
        assert db.fetch_all("SELECT * FROM workout_log ORDER BY id") == before_log
        assert db.fetch_all("SELECT * FROM program_backups ORDER BY id") == before_backups
        assert db.fetch_all("SELECT * FROM program_backup_items ORDER BY id") == []

    assert scan_export_bounds() == [
        {"routine": ROUTINE, "exercise": exercise, "reason": field_message}
    ]


def test_mixed_valid_and_blank_rows_reject_before_any_log_insert(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """A later blank row rejects the complete source set before any insert."""
    _seed_plan(
        clean_db,
        exercise_factory,
        workout_plan_factory,
        exercise="Gate Zero Valid First",
        minimum=8,
        maximum=12,
    )
    _seed_plan(
        clean_db,
        exercise_factory,
        workout_plan_factory,
        exercise="Gate Zero Blank Last",
        minimum=20,
        maximum="",
    )
    before_source = clean_db.fetch_all("SELECT * FROM user_selection ORDER BY id")
    before_log = clean_db.fetch_all("SELECT * FROM workout_log ORDER BY id")

    response = client.post("/export_to_workout_log")

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"
    with DatabaseHandler() as db:
        assert db.fetch_all("SELECT * FROM user_selection ORDER BY id") == before_source
        assert db.fetch_all("SELECT * FROM workout_log ORDER BY id") == before_log


def test_export_scanner_and_per_item_restore_agree_on_blank(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """All boundaries reject the blank while restore still keeps a valid peer."""
    exercise = "Gate Zero Boundary Agreement"
    _seed_plan(
        clean_db,
        exercise_factory,
        workout_plan_factory,
        exercise=exercise,
        minimum=20,
        maximum="",
    )
    valid_exercise = "Gate Zero Restore Valid Peer"
    _seed_plan(
        clean_db,
        exercise_factory,
        workout_plan_factory,
        exercise=valid_exercise,
        minimum=8,
        maximum=12,
    )
    backup_id = create_backup("Gate Zero Blank Backup")["id"]

    reason = "Maximum reps must be a finite number."
    assert scan_export_bounds() == [
        {"routine": ROUTINE, "exercise": exercise, "reason": reason}
    ]
    export_response = client.post("/export_to_workout_log")
    assert export_response.status_code == 400
    with DatabaseHandler() as db:
        assert db.fetch_all("SELECT * FROM workout_log") == []

    restore_response = client.post(f"/api/backups/{backup_id}/restore")

    assert restore_response.status_code == 200
    restore_data = restore_response.get_json()["data"]
    assert restore_data["restored_count"] == 1
    assert restore_data["invalid"] == [
        {
            "routine": ROUTINE,
            "exercise": exercise,
            "reason": reason,
        }
    ]
    with DatabaseHandler() as db:
        restored = db.fetch_all(
            "SELECT exercise, min_rep_range, max_rep_range FROM user_selection ORDER BY exercise"
        )
    assert restored == [
        {"exercise": valid_exercise, "min_rep_range": 8, "max_rep_range": 12}
    ]


class _CapturingDatabase:
    def __init__(self, row: dict[str, Any]):
        self.row = row
        self.insert_params: list[tuple[Any, ...]] = []

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def fetch_all(self, _query, _params=None):
        return [self.row]

    def fetch_one(self, _query, _params=None):
        return None

    def execute_query(self, _query, params=None):
        self.insert_params.append(tuple(params or ()))
        return 1


@pytest.mark.parametrize(
    "minimum,maximum",
    [(None, 12), (8, None), (None, None)],
    ids=["min_none", "max_none", "both_none"],
)
def test_actual_none_remains_nullable_at_export_service_boundary(
    monkeypatch, minimum, maximum
):
    """A fake source is required: canonical rep-bound source columns are NOT NULL."""
    row = {
        "id": 1,
        "routine": ROUTINE,
        "exercise": "Gate Zero Nullable Seam",
        "sets": 3,
        "min_rep_range": minimum,
        "max_rep_range": maximum,
        "rir": None,
        "rpe": None,
        "weight": 50,
    }
    capturing_db = _CapturingDatabase(row)
    monkeypatch.setattr(export_service, "DatabaseHandler", lambda: capturing_db)

    result = export_service.export_plan_to_workout_log()

    assert result.ok is True
    assert len(capturing_db.insert_params) == 1
    inserted = capturing_db.insert_params[0]
    assert inserted[4] is minimum
    assert inserted[5] is maximum


def test_numeric_strings_remain_accepted_at_export_service_boundary(monkeypatch):
    """The validator accepts numeric strings and the export does not rewrite them."""
    row = {
        "id": 1,
        "routine": ROUTINE,
        "exercise": "Gate Zero Numeric String Seam",
        "sets": 3,
        "min_rep_range": "8",
        "max_rep_range": "12",
        "rir": "3",
        "rpe": None,
        "weight": "50",
    }
    capturing_db = _CapturingDatabase(row)
    monkeypatch.setattr(export_service, "DatabaseHandler", lambda: capturing_db)

    result = export_service.export_plan_to_workout_log()

    assert result.ok is True
    assert capturing_db.insert_params == [
        (1, ROUTINE, "Gate Zero Numeric String Seam", 3, "8", "12", "3", None, "50")
    ]
