"""Shared validation for persisted workout-plan and workout-log values."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
import math
from typing import Any, Optional

from utils.constants import (
    MAX_RIR,
    MAX_WORKOUT_WEIGHT_KG,
    MIN_RIR,
    MIN_WORKOUT_WEIGHT_KG,
)


UNSET = object()
SQLITE_INTEGER_MAX = 2**63 - 1


def _number(value: Any, field_label: str) -> tuple[Optional[float], Optional[str]]:
    """Coerce a JSON numeric value while rejecting booleans and non-finite values."""
    if isinstance(value, bool):
        return None, f"{field_label} must be a finite number."
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None, f"{field_label} must be a finite number."
    if not math.isfinite(number):
        return None, f"{field_label} must be a finite number."
    return number, None


def parse_workout_count(
    value: Any, minimum: int, label: str = "Reps"
) -> tuple[Optional[int], Optional[str]]:
    """Parse whole-number counts without rounding integers or numeric strings."""
    number_error = f"{label} must be a finite number."
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        return None, number_error
    if isinstance(value, str) and (not value.isascii() or "_" in value):
        return None, number_error
    try:
        number = Decimal.from_float(value) if isinstance(value, float) else Decimal(value)
    except InvalidOperation:
        return None, number_error
    if not number.is_finite():
        return None, number_error
    if number != number.to_integral_value():
        return None, f"{label} must be a whole number."
    if number < minimum:
        return None, f"{label} must be at least {minimum}."
    if number > SQLITE_INTEGER_MAX:
        return None, f"{label} is too large to store."
    return int(number), None


def rep_bound_for_update(
    updates: dict[str, Any], current: Optional[dict[str, Any]], column: str, *, minimum: int
) -> Any:
    """Compare with a stored sibling only if that sibling is usable on its own."""
    if column in updates:
        return updates[column]
    if current is None:
        return UNSET
    count, _ = parse_workout_count(current.get(column), minimum)
    return UNSET if count is None else count


def validate_workout_bounds(
    *,
    weight: Any = UNSET,
    rir: Any = UNSET,
    min_reps: Any = UNSET,
    max_reps: Any = UNSET,
    sets: Any = UNSET,
    rep_minimum: Optional[int] = None,
    allow_null: bool = False,
    allow_blank: Optional[bool] = None,
) -> Optional[str]:
    """Return a validation message, or ``None`` when canonical bounds hold.

    ``UNSET`` distinguishes an omitted partial-update field from an explicit
    JSON null. With ``rep_minimum``, rep bounds are whole-number counts.
    Analysis diagnostics omit it so they retain their numeric-only checks.
    Sets are required when supplied. Other fields follow ``allow_null`` and
    ``allow_blank``. If omitted, ``allow_blank`` follows ``allow_null``.
    """
    numeric_values: dict[str, int | float | None] = {}
    blank_allowed = allow_null if allow_blank is None else allow_blank
    for key, value, label in (
        ("weight", weight, "Weight"),
        ("rir", rir, "RIR"),
        ("min_reps", min_reps, "Minimum reps"),
        ("max_reps", max_reps, "Maximum reps"),
        ("sets", sets, "Sets"),
    ):
        if value is UNSET:
            continue
        if value is None and allow_null and key != "sets":
            numeric_values[key] = None
            continue
        if value == "" and blank_allowed and key != "sets":
            numeric_values[key] = None
            continue
        if value is None:
            return f"{label} cannot be null."
        if key == "sets":
            number, error = parse_workout_count(value, 1, label)
        elif rep_minimum is not None and key in ("min_reps", "max_reps"):
            number, error = parse_workout_count(value, rep_minimum, label)
        else:
            number, error = _number(value, label)
        if error:
            return error
        numeric_values[key] = number

    parsed_weight = numeric_values.get("weight")
    if parsed_weight is not None and not (
        MIN_WORKOUT_WEIGHT_KG <= parsed_weight <= MAX_WORKOUT_WEIGHT_KG
    ):
        return (
            f"Weight must be between {MIN_WORKOUT_WEIGHT_KG:g} and "
            f"{MAX_WORKOUT_WEIGHT_KG:g} kg."
        )

    parsed_rir = numeric_values.get("rir")
    if parsed_rir is not None and not (MIN_RIR <= parsed_rir <= MAX_RIR):
        return f"RIR must be between {MIN_RIR:g} and {MAX_RIR:g}."

    parsed_min = numeric_values.get("min_reps")
    parsed_max = numeric_values.get("max_reps")
    if parsed_min is not None and parsed_max is not None and parsed_min > parsed_max:
        return "Minimum reps cannot exceed maximum reps."

    return None


def validate_plan_log_bounds(row: dict[str, Any]) -> Optional[str]:
    """Apply the same plan-to-log policy before copying rows and diagnosing failures."""
    return validate_workout_bounds(
        weight=row.get("weight"),
        rir=row.get("rir"),
        min_reps=row.get("min_rep_range"),
        max_reps=row.get("max_rep_range"),
        sets=row.get("sets"),
        rep_minimum=1,
        allow_null=True,
        allow_blank=False,
    )
