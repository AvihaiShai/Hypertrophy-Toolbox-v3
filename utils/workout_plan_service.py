"""Plan-row removal behind ``POST /remove_exercise`` (WS4 slice 1).

Moved from ``routes/workout_plan.py`` without a behaviour change. Removal is not
atomic: each statement commits on its own (``execute_query``'s default
``commit=True``), so a failure in a later statement leaves the earlier ones
committed.
"""
from typing import Any, NamedTuple, Optional

from utils import supersets as superset_service
from utils.database import DatabaseHandler


class RemovedPlanExercise(NamedTuple):
    """The removed row's ``routine`` and ``exercise``, verbatim from the database."""

    routine: Any
    exercise: Any


def remove_plan_exercise(exercise_id: Any) -> Optional[RemovedPlanExercise]:
    """Delete one ``user_selection`` row and its ``workout_log`` rows.

    ``exercise_id`` is the caller-validated id exactly as sent. It is passed on
    unchanged to ``unlink_partner_for_removal``, which logs it. Returns ``None``,
    having written nothing, when no row has that id. Exceptions propagate unchanged.
    """
    with DatabaseHandler() as db_handler:
        exercise_info = db_handler.fetch_one(
            "SELECT routine, exercise, superset_group FROM user_selection WHERE id = ?",
            (int(exercise_id),)
        )
        if not exercise_info:
            return None
        if exercise_info.get('superset_group'):
            superset_service.unlink_partner_for_removal(
                db_handler, exercise_id, exercise_info['superset_group']
            )
        db_handler.execute_query(
            "DELETE FROM workout_log WHERE workout_plan_id = ?", (int(exercise_id),)
        )
        db_handler.execute_query(
            "DELETE FROM user_selection WHERE id = ?", (int(exercise_id),)
        )
    return RemovedPlanExercise(exercise_info.get('routine'), exercise_info.get('exercise'))
