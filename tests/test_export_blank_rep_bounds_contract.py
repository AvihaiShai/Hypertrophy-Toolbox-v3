"""Executable contract tests for the blank-string export boundary."""
from __future__ import annotations

from typing import Any

import pytest

import utils.export_service as export_service
from utils.database import DatabaseHandler
from utils.rep_range_integrity import scan_export_bounds


ROUTINE = "GYM - Full Body - Workout A"


def _seed(clean_db, exercise_factory, workout_plan_factory, exercise, minimum, maximum):
    exercise_factory(exercise, primary_muscle_group="Chest")
    plan_id = workout_plan_factory(exercise_name=exercise, routine=ROUTINE)
    clean_db.execute_query(
        "UPDATE user_selection SET min_rep_range = ?, max_rep_range = ? WHERE id = ?",
        (minimum, maximum, plan_id),
    )


@pytest.mark.parametrize(
    "minimum,maximum,reason",
    [
        ("", 12, "Minimum reps must be a finite number."),
        (8, "", "Maximum reps must be a finite number."),
        ("", "", "Minimum reps must be a finite number."),
    ],
    ids=["min_blank", "max_blank", "both_blank"],
)
def test_export_rejects_exact_blank_rep_bounds_without_mutation(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    minimum: Any,
    maximum: Any,
    reason: str,
):
    exercise = "Gate Zero Intended Blank"
    _seed(clean_db, exercise_factory, workout_plan_factory, exercise, minimum, maximum)
    source_before = clean_db.fetch_all(
        "SELECT *, typeof(min_rep_range) AS min_type, "
        "typeof(max_rep_range) AS max_type FROM user_selection ORDER BY id"
    )
    log_before = clean_db.fetch_all("SELECT * FROM workout_log ORDER BY id")

    response = client.post("/export_to_workout_log")

    message = (
        f"{reason} Invalid plan value on: {ROUTINE} / {exercise}. "
        "Fix these in the Workout Plan editor."
    )
    assert response.status_code == 400
    assert response.get_json() == {
        "ok": False,
        "status": "error",
        "message": message,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": message,
            "requestId": None,
        },
    }
    assert scan_export_bounds() == [
        {"routine": ROUTINE, "exercise": exercise, "reason": reason}
    ]
    with DatabaseHandler() as db:
        assert db.fetch_all(
            "SELECT *, typeof(min_rep_range) AS min_type, "
            "typeof(max_rep_range) AS max_type FROM user_selection ORDER BY id"
        ) == source_before
        assert db.fetch_all("SELECT * FROM workout_log ORDER BY id") == log_before


def test_mixed_valid_and_blank_source_set_rejects_atomically(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    _seed(clean_db, exercise_factory, workout_plan_factory, "Gate Zero Intended Valid", 8, 12)
    _seed(clean_db, exercise_factory, workout_plan_factory, "Gate Zero Intended Blank", 20, "")
    source_before = clean_db.fetch_all("SELECT * FROM user_selection ORDER BY id")
    log_before = clean_db.fetch_all("SELECT * FROM workout_log ORDER BY id")

    response = client.post("/export_to_workout_log")

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"
    with DatabaseHandler() as db:
        assert db.fetch_all("SELECT * FROM user_selection ORDER BY id") == source_before
        assert db.fetch_all("SELECT * FROM workout_log ORDER BY id") == log_before


class _TracingDatabase:
    def __init__(self, rows: list[dict[str, Any]]):
        self.rows = rows
        self.calls: list[str] = []

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def fetch_all(self, _query, _params=None):
        self.calls.append("fetch_all")
        return self.rows

    def fetch_one(self, _query, _params=None):
        self.calls.append("fetch_one")
        return None

    def execute_query(self, _query, _params=None):
        self.calls.append("execute_query")
        return 1


def test_full_source_set_is_validated_before_duplicate_checks_or_inserts(monkeypatch):
    valid = {
        "id": 1,
        "routine": ROUTINE,
        "exercise": "Gate Zero Intended Valid",
        "sets": 3,
        "min_rep_range": 8,
        "max_rep_range": 12,
        "rir": 3,
        "rpe": 7,
        "weight": 50,
    }
    blank = {
        **valid,
        "id": 2,
        "exercise": "Gate Zero Intended Blank",
        "min_rep_range": 20,
        "max_rep_range": "",
    }
    tracing_db = _TracingDatabase([valid, blank])
    monkeypatch.setattr(export_service, "DatabaseHandler", lambda: tracing_db)

    result = export_service.export_plan_to_workout_log()

    assert result.ok is False
    assert result.code == "VALIDATION_ERROR"
    assert result.message == "Maximum reps must be a finite number."
    assert tracing_db.calls == ["fetch_all"]
