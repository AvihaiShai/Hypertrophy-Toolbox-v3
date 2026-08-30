"""Name the ``user_selection`` rows behind a bounds failure, for error messages.

A restore taken before ``validate_workout_bounds`` gated the plan columns can
leave a row whose ``min_rep_range`` / ``max_rep_range`` is not a number. #384
closed that ingress, but rows poisoned by an earlier restore still reach the
analysis surfaces and still raise, and the resulting error names no routine and
no exercise -- so the user cannot find the row to repair.

This module is read-only and purely descriptive. It repairs nothing, coerces
nothing, and is never consulted before a calculation: each entry point is called
from a handler whose failure has *already* happened, so a database with no
poisoned rows never reaches this module at all.

Per-call-site predicates
------------------------
There is deliberately no single canonical scan. Each scanner reproduces the
``validate_workout_bounds`` call its own caller makes, and the two callers do not
make the same one:

* the analysis surfaces fail on rep-range arithmetic alone, so
  :func:`scan_rep_ranges` and :func:`scan_exercise_plan_default` validate
  ``min_rep_range`` and ``max_rep_range`` **one field at a time**, with
  ``allow_null=False``;
* ``export_plan_to_workout_log`` makes a **single combined call** over all four
  bounded columns with ``allow_null=True`` and ``allow_blank=False``
  (``utils/export_service.py:493-500``), so :func:`scan_export_bounds` makes
  that same one call -- accepting actual null while rejecting an exact blank.

That split is what makes each result honest rather than merely convenient, and
"Minimum reps cannot exceed maximum reps." is the case that shows why. Per-field
isolation structurally excludes it, which is correct for the analysis surfaces:
arithmetic on an inverted-but-numeric rep pair succeeds, so that verdict is not
what makes them raise, and a row tripping only it returns no finding and leaves
their message byte-for-byte unchanged. It is wrong for the export, where that
verdict is precisely what blocks the write -- so :func:`scan_export_bounds`
reports it, as it reports the weight and RIR range verdicts for the same reason.

Reproducing the caller's call rather than approximating it also keeps the
reported reason identical to the caller's when a row has more than one fault: the
combined call parses all four columns before range-checking any, so a per-field
replay interleaves parse and range checks and can name a different column than
the one the export actually stopped on.

Failure policy
--------------
Every entry point swallows its own exceptions and returns ``[]``. A diagnostic
must never mask, replace, or escalate the failure it is describing.

That swallow does not make the module side-effect free, and the exception is
worth knowing: these functions open a fresh ``DatabaseHandler``, and
``get_db_connection`` responds to a malformed/not-a-database/encrypted
``sqlite3.DatabaseError`` by *renaming the live database* to
``<name>.corrupted_<timestamp>`` (``utils/database.py:226-231``). Describing a
corrupt database must not be the call that quarantines it, so callers pass the
exception they caught to :func:`suppressed_for` and skip the scan when it says
so. The swallow cannot cover this: the rename happens inside the connect, before
any exception reaches this module.
"""
from __future__ import annotations

import sqlite3
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from utils.database import DatabaseHandler
from utils.logger import get_logger
from utils.workout_validation import validate_workout_bounds

logger = get_logger()

# The message is rendered into a single <p> (templates/error.html) and verbatim
# into a Bootstrap toast (fetch-wrapper.js, exports.js), so the clause has to
# stay one sentence and the row list has to stay short.
MAX_NAMED_ROWS = 5

# utils/session_summary.py uses this literal for the same empty-routine case.
# Importing the constant instead would widen this module's import closure into a
# calculation file for no benefit.
UNASSIGNED_ROUTINE = "Unassigned"

REP_RANGE_LABEL = "Invalid rep range on"
PLAN_VALUE_LABEL = "Invalid plan value on"

# (column in user_selection, keyword accepted by validate_workout_bounds)
_REP_FIELDS: Tuple[Tuple[str, str], ...] = (
    ("min_rep_range", "min_reps"),
    ("max_rep_range", "max_reps"),
)


def suppressed_for(cause: Optional[BaseException]) -> bool:
    """Whether describing this failure would risk making it worse.

    A ``sqlite3.DatabaseError`` may mean the database is corrupt, and opening a
    fresh connection to describe it can be the call that trips
    ``_attempt_database_recovery`` into renaming the live file away
    (``utils/database.py:226-231``). Staying silent is the lesser outcome.
    """
    return isinstance(cause, sqlite3.DatabaseError)


def accepts_in_isolation(keyword: str, value: Any) -> bool:
    """Whether ``validate_workout_bounds`` accepts *value* for *keyword* alone.

    *keyword* is a ``validate_workout_bounds`` parameter name (``min_reps``,
    ``max_reps``, ``weight``, ``rir``); every other field is left ``UNSET``.

    This is the canonical "is the stored value usable" test, and deliberately
    not a bare ``float()``: the validator also rejects booleans and non-finite
    values, so ``'nan'`` and ``'inf'`` parse but are still not usable.
    """
    return validate_workout_bounds(**{keyword: value}) is None


def _rep_rejection(row: Dict[str, Any]) -> Optional[str]:
    """The first rep-column message this row is rejected on, or ``None``.

    Each field is validated alone, so cross-field and range verdicts cannot
    appear here -- only the per-value contract the analysis surfaces depend on.
    """
    for column, keyword in _REP_FIELDS:
        # Explicit: allow_null=False is the analysis contract, and naming it stops
        # pyright reading the ** unpack as a candidate binding for that parameter.
        message = validate_workout_bounds(**{keyword: row.get(column)}, allow_null=False)
        if message:
            return message
    return None


def _export_rejection(row: Dict[str, Any]) -> Optional[str]:
    """The message ``export_plan_to_workout_log`` returns for this row, or ``None``.

    One combined call over all four bounded columns, including the caller's
    independently selected null and blank policies
    (``utils/export_service.py:493-500``).
    """
    return validate_workout_bounds(
        weight=row.get("weight"),
        rir=row.get("rir"),
        min_reps=row.get("min_rep_range"),
        max_reps=row.get("max_rep_range"),
        allow_null=True,
        allow_blank=False,
    )


def _findings(
    rows: Sequence[Dict[str, Any]],
    reject: Callable[[Dict[str, Any]], Optional[str]],
) -> List[Dict[str, str]]:
    """Shape rejected rows as ``{routine, exercise, reason}``.

    Same shape ``restore_backup()`` already returns
    (``utils/program_backup.py:500-506``).
    """
    findings: List[Dict[str, str]] = []
    for row in rows:
        reason = reject(row)
        if reason:
            findings.append({
                "routine": row.get("routine") or UNASSIGNED_ROUTINE,
                "exercise": row.get("exercise") or "",
                "reason": reason,
            })
    return findings


def scan_rep_ranges(routine: Optional[str] = None) -> List[Dict[str, str]]:
    """Rows whose stored rep range is not a usable number.

    Pass *routine* only where the failing calculation was itself filtered by
    routine -- ``/session_summary`` with a ``routine`` argument. The weekly and
    Excel paths aggregate every row, so they pass nothing.
    """
    query = """
        SELECT id, routine, exercise, min_rep_range, max_rep_range
        FROM user_selection
    """
    params: Tuple[Any, ...] = ()
    if routine:
        query += " WHERE routine = ?"
        params = (routine,)
    query += " ORDER BY id"

    try:
        with DatabaseHandler() as db:
            rows = db.fetch_all(query, params or None)
        return _findings(rows, _rep_rejection)
    except Exception:
        logger.exception("Rep-range diagnostic failed; reporting no rows")
        return []


def scan_exercise_plan_default(exercise: str) -> List[Dict[str, str]]:
    """The single plan row ``get_exercise_plan_defaults`` reads for *exercise*.

    Mirrors that query's ``ORDER BY id DESC LIMIT 1``
    (``utils/progression_plan.py:22-33``) so the row named is the row the failing
    request actually read, not merely some poisoned row. That query selects no
    ``routine`` column, so this one adds it.
    """
    try:
        with DatabaseHandler() as db:
            rows = db.fetch_all(
                """
                SELECT routine, exercise, min_rep_range, max_rep_range
                FROM user_selection
                WHERE exercise = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (exercise,),
            )
        return _findings(rows, _rep_rejection)
    except Exception:
        logger.exception("Rep-range diagnostic failed; reporting no rows")
        return []


def scan_export_bounds() -> List[Dict[str, str]]:
    """Rows ``export_plan_to_workout_log`` rejects, in the order it reads them.

    Reproduces that caller's own validation by making the same single combined
    call (:func:`_export_rejection`), so a numeric ``min > max`` row is named
    here. Neither query orders explicitly, so both see the same table order and
    the row that blocked the export is normally the first one reported here;
    adding an ORDER BY to this one alone would make them diverge.
    """
    try:
        with DatabaseHandler() as db:
            rows = db.fetch_all(
                """
                SELECT routine, exercise, weight, rir, min_rep_range, max_rep_range
                FROM user_selection
                """
            )
        return _findings(rows, _export_rejection)
    except Exception:
        logger.exception("Plan-bounds diagnostic failed; reporting no rows")
        return []


def annotate(
    message: str,
    findings: Sequence[Dict[str, str]],
    label: str = REP_RANGE_LABEL,
) -> str:
    """Append the offending rows to *message*, or return it untouched.

    An empty *findings* returns *message* byte for byte. A diagnostic that
    reported "nothing found" would be worse than the bare message it replaced:
    it would tell the user the app checked and the data is fine, on a request
    that just failed.
    """
    if not findings:
        return message

    named = findings[:MAX_NAMED_ROWS]
    # The plan-to-log message is itself the validator string, so a row rejected
    # for that same reason would otherwise state it twice in one sentence.
    listed = "; ".join(
        f"{item['routine']} / {item['exercise']}"
        + ("" if item["reason"] == message else f" ({item['reason']})")
        for item in named
    )
    remaining = len(findings) - len(named)
    more = f" (+{remaining} more)" if remaining > 0 else ""
    return f"{message} {label}: {listed}{more}. Fix these in the Workout Plan editor."
