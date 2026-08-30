"""Gate-0 characterization for blank/null plan-to-log rep bounds.

``POST /export_to_workout_log`` has no rep-bound request payload.  It validates
the complete persisted ``user_selection`` source set, then copies accepted rows
to ``workout_log``.  These tests deliberately pin the current blank-string
defect and the already-correct neighbouring behavior without changing
production code.  The future implementation packet must invert the tests whose
names contain ``known_defect`` and keep the compatibility controls green.

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
    "minimum,maximum,minimum_type,maximum_type",
    [
        ("", 12, "text", "integer"),
        (8, "", "integer", "text"),
        ("", "", "text", "text"),
    ],
    ids=["min_blank", "max_blank", "both_blank"],
)
def test_known_defect_exact_blank_rep_bounds_export_as_text(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    minimum,
    maximum,
    minimum_type,
    maximum_type,
):
    """Exact blanks currently pass and are copied as TEXT, never normalized to NULL."""
    exercise = "Gate Zero Blank Press"
    _seed_plan(
        clean_db,
        exercise_factory,
        workout_plan_factory,
        exercise=exercise,
        minimum=minimum,
        maximum=maximum,
    )

    response = client.post("/export_to_workout_log")

    assert response.status_code == 200
    assert response.get_json() == {
        "ok": True,
        "status": "success",
        "message": "Workout plan exported successfully (1 exercises)",
    }
    assert scan_export_bounds() == []

    with DatabaseHandler() as db:
        stored = db.fetch_one(
            """
            SELECT planned_min_reps, typeof(planned_min_reps) AS minimum_type,
                   planned_max_reps, typeof(planned_max_reps) AS maximum_type
            FROM workout_log
            WHERE exercise = ?
            """,
            (exercise,),
        )
    assert stored == {
        "planned_min_reps": minimum,
        "minimum_type": minimum_type,
        "planned_max_reps": maximum,
        "maximum_type": maximum_type,
    }


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


def test_known_defect_mixed_valid_and_blank_rows_export_together(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """A later blank row currently defeats the intended all-row preflight guarantee."""
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

    response = client.post("/export_to_workout_log")

    assert response.status_code == 200
    with DatabaseHandler() as db:
        rows = db.fetch_all(
            "SELECT exercise, planned_min_reps, planned_max_reps, "
            "typeof(planned_max_reps) AS max_type FROM workout_log ORDER BY exercise"
        )
    assert rows == [
        {
            "exercise": "Gate Zero Blank Last",
            "planned_min_reps": 20,
            "planned_max_reps": "",
            "max_type": "text",
        },
        {
            "exercise": "Gate Zero Valid First",
            "planned_min_reps": 8,
            "planned_max_reps": 12,
            "max_type": "integer",
        },
    ]


def test_known_defect_export_disagrees_with_restore_and_scanner_on_blank(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """The same stored blank passes export/scanner but restore rejects it per row."""
    exercise = "Gate Zero Boundary Disagreement"
    _seed_plan(
        clean_db,
        exercise_factory,
        workout_plan_factory,
        exercise=exercise,
        minimum=20,
        maximum="",
    )
    backup_id = create_backup("Gate Zero Blank Backup")["id"]

    assert scan_export_bounds() == []
    export_response = client.post("/export_to_workout_log")
    assert export_response.status_code == 200
    with DatabaseHandler() as db:
        exported = db.fetch_one(
            "SELECT planned_max_reps, typeof(planned_max_reps) AS value_type "
            "FROM workout_log WHERE exercise = ?",
            (exercise,),
        )
    assert exported == {"planned_max_reps": "", "value_type": "text"}

    restore_response = client.post(f"/api/backups/{backup_id}/restore")

    assert restore_response.status_code == 200
    restore_data = restore_response.get_json()["data"]
    assert restore_data["restored_count"] == 0
    assert restore_data["invalid"] == [
        {
            "routine": ROUTINE,
            "exercise": exercise,
            "reason": "Maximum reps must be a finite number.",
        }
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
