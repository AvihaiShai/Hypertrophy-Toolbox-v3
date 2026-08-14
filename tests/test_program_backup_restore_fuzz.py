"""Characterization of restore-path row robustness: program_backup_items -> user_selection.

``restore_backup()`` (``utils/program_backup.py``) applies no bounds validation, so a persisted
backup item can carry values that ``POST /add_exercise`` rejects at the boundary, and restoring
places them in ``user_selection`` with HTTP 200. For one shape -- non-numeric text in a rep-range
column -- the restored row then makes ``GET /weekly_summary`` return 500.

Harness non-claim
-----------------
The direct UPDATE below is a harness device for constructing a persisted state, not a modelled
user action. This packet makes no claim that editing the database by hand is supported, expected,
or protected. What is modelled is the STATE: a ``program_backup_items`` row holding a value the
current plan routes reject -- reachable in production either by a backup taken before
``validate_workout_bounds`` gated that field, or by a backup taken from a ``user_selection`` row
written through a route that does not validate that field today.

Known defect (FINDING-1)
------------------------
The node whose name contains ``known_defect`` asserts a DEFECT: restoring a backup item whose
``min_rep_range`` holds non-numeric text makes ``GET /weekly_summary`` return 500. If that node
reds, the defect was FIXED -- invert or delete it in the same packet that fixes it, and update
``docs/testing_phase3/PLANNING.md``. Do not "repair" it.

Expected churn
--------------
When restore-path validation eventually lands, the five parametrized nodes of
``test_restore_accepts_rows_the_plan_route_rejects`` must be REWRITTEN TO ASSERT REJECTION, not
preserved. They pin today's permissive behavior, not a guarantee. Which rewrite depends on an
owner decision this packet does not make (``docs/testing_phase3/PLANNING.md`` §3.4 / PR7): a
*refusing* restore fails the request, while a *skipping* restore returns 200 with
``restored_count == 0`` -- under the skip shape the node's name is wrong too, not just its
assertions.

Incidental contract pin
-----------------------
The four exact ``utils/workout_validation.py`` messages asserted below are pinned in this file and
nowhere else in the repository. They are asserted verbatim on purpose -- the exact string is what
distinguishes the bounds-rejection branch from the duplicate-row ``VALIDATION_ERROR`` branch -- so
editing that user-facing copy reds five nodes here. That is intended, but it means this
characterization file is also the sole guard on those strings.
"""
from __future__ import annotations

import logging
import os
import traceback
from typing import Any, Dict, Mapping

import pytest

from utils.constants import MAX_RIR
from utils.database import DatabaseHandler
from utils.effective_sets import get_effort_factor, get_rep_range_factor
from utils.program_backup import create_backup
from utils.weekly_summary import calculate_weekly_summary


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
def test_restore_accepts_rows_the_plan_route_rejects(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    updates,
    expected_typeof,
    expected_message,
):
    """A backup item the plan route would reject at the boundary restores with HTTP 200.

    The same value is asserted twice: once as the 400 the write path returns for it, and once as
    the row the restore path persists verbatim into ``user_selection``. The gap between those two
    assertions is the characterized behavior.
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

    # (c) RESTORE -- the same value goes through the restore path unchallenged.
    restore_response = client.post(
        f"/api/backups/{backup_id}/restore",
        content_type="application/json",
    )
    assert restore_response.status_code == 200
    restore_payload = restore_response.get_json()
    assert restore_payload["ok"] is True
    assert restore_payload["data"]["restored_count"] == 1

    # (d) PERSISTED -- verbatim, storage class included. For min_rep_non_numeric this is the
    # load-bearing assertion: text survives a `min_rep_range INTEGER NOT NULL` column.
    with DatabaseHandler() as db:
        for column, value in updates.items():
            stored = db.fetch_one(
                f"SELECT {column} AS value, typeof({column}) AS value_type "
                "FROM user_selection WHERE exercise = ?",
                (exercise_name,),
            )
            assert stored is not None
            assert stored["value"] == value
            assert stored["value_type"] == expected_typeof[column]


def test_known_defect_weekly_summary_500_after_restoring_non_numeric_rep_range(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
    caplog,
):
    """FINDING-1: a restored non-numeric ``min_rep_range`` makes ``GET /weekly_summary`` 500.

    This node asserts a DEFECT. Restore returns 200 and persists the row; the analysis page then
    raises ``TypeError`` while averaging the rep range. If this node reds, the defect was fixed --
    see the module docstring before changing anything here.
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
    assert restore_payload["data"]["restored_count"] == 1

    # No headers at all: utils/errors.py treats either X-Requested-With: XMLHttpRequest or an
    # Accept containing application/json as XHR and would answer with JSON instead of the page.
    with caplog.at_level(logging.ERROR):
        response = client.get("/weekly_summary")

    assert response.status_code == 500

    # Byte markers proven by tests/test_error_page_contract.py -- a 500 from an unrelated cause
    # must not satisfy this node.
    assert b"<title>Server Error - Hypertrophy Toolbox</title>" in response.data
    assert b'<h1 class="error-status-code">500</h1>' in response.data
    assert b'<h2 class="error-title">Server Error</h2>' in response.data
    assert b"Unable to load weekly summary." in response.data

    # FRAME ORACLE. Status alone cannot distinguish the failure sites: guarding only the
    # rep-range average in utils/weekly_summary.py still produces a 500 from a second site
    # (the rep-range factor in utils/effective_sets.py). Pin the innermost frame instead.
    type_error_records = [
        record
        for record in caplog.records
        if record.exc_info is not None and record.exc_info[0] is TypeError
    ]
    assert len(type_error_records) == 1, (
        "Expected exactly one logged TypeError from the weekly summary request, got "
        f"{len(type_error_records)}"
    )

    exc_info = type_error_records[0].exc_info
    assert exc_info is not None
    tb = exc_info[2]
    assert tb is not None

    innermost = traceback.extract_tb(tb)[-1]
    # Two files are named weekly_summary.py (utils/ and routes/), so the basename alone does not
    # discriminate -- pin the parent directory too rather than leaning on the function name.
    innermost_path = os.path.normpath(innermost.filename)
    assert os.path.basename(innermost_path) == "weekly_summary.py"
    assert os.path.basename(os.path.dirname(innermost_path)) == "utils"
    assert innermost.name == "_aggregate_weekly_volumes"


def test_weekly_summary_returns_200_without_validating_restored_out_of_range_numerics(
    client,
    clean_db,
    exercise_factory,
    workout_plan_factory,
):
    """Out-of-range numerics restore, render, and enter the arithmetic with no user-visible signal.

    "Returns 200" means only that nothing raised. The values are NOT validated, corrected, or
    flagged: they propagate into the displayed Effective sets, Raw sets and total volume exactly
    as stored.
    """
    exercise_name = exercise_factory(
        "Fuzz Chest Press",
        primary_muscle_group="Chest",
        secondary_muscle_group=None,
        tertiary_muscle_group=None,
    )

    # One item only. user_selection carries a composite UNIQUE that program_backup_items does not,
    # so cloning items from one plan row would collide, roll the restore back, and make the
    # assertions below pass vacuously.
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

    # 1. RESTORE GUARD -- a rolled-back restore would leave an empty program and pass vacuously.
    restore_response = client.post(
        f"/api/backups/{backup_id}/restore",
        content_type="application/json",
    )
    assert restore_response.status_code == 200
    restore_payload = restore_response.get_json()
    assert restore_payload["ok"] is True
    assert restore_payload["data"]["restored_count"] == 1

    # 2. The out-of-range values are what landed in the active program.
    with DatabaseHandler() as db:
        row = db.fetch_one(
            "SELECT sets, min_rep_range, max_rep_range, rir, weight "
            "FROM user_selection WHERE exercise = ?",
            (exercise_name,),
        )
        assert row is not None
        assert row["sets"] == 3
        assert row["min_rep_range"] == 20
        assert row["max_rep_range"] == 5
        assert row["rir"] == 99
        assert row["weight"] == 99999.0

    # 3. Accept: application/json on purpose -- the JSON branch is the one with proven pytest
    # coverage on this route. N2 deliberately sends the opposite (no headers at all) because it
    # asserts the HTML error page; see utils/errors.py:52-63 for the XHR triggers.
    response = client.get("/weekly_summary", headers={"Accept": "application/json"})
    assert response.status_code == 200

    # 4. ARITHMETIC -- the values are consumed, not dropped or clamped.
    summary = calculate_weekly_summary()
    chest = summary["Chest"]

    # 3 raw sets * avg_reps 12.5. Rules out min-only (60.0), max-only (15.0), and a dropped row
    # (0.0) -- the inverted range is averaged exactly as a valid one would be.
    assert chest["raw_total_reps"] == 37.5
    # 37.5 reps * 99999.0 kg: the out-of-range load survived and entered the arithmetic.
    assert chest["raw_total_volume"] == 3749962.5

    # Relational on purpose: the effort factor is a product-tunable in EFFORT_FACTOR_BUCKETS,
    # so hard-coding its value here would pin a tuning decision this packet does not own.
    expected_effective = round(
        3 * get_effort_factor(rir=int(MAX_RIR)) * get_rep_range_factor(20, 5), 2
    )
    assert chest["effective_weekly_sets"] == expected_effective

    # The clamp itself, also relational: RIR 99 is silently treated as the maximum valid RIR.
    assert get_effort_factor(rir=99) == get_effort_factor(rir=int(MAX_RIR))

    # The rep-range factor has its OWN averaging, separate from the one behind raw_total_reps
    # above, and the relational assertion cannot pin it: get_rep_range_factor appears on both
    # sides of `expected_effective`, so a change to its averaging moves both sides together and
    # cancels out. Pin it by symmetry instead -- an inverted range is treated as its midpoint,
    # so reversing the arguments must not change the factor. Replacing the average with either
    # endpoint breaks this equality while leaving `expected_effective` untouched.
    #
    # Accidental behavior, not a designed contract: 12.5 falls in a gap between the (6, 12) and
    # (13, 20) buckets, so this factor is the DEFAULT_MULTIPLIER fall-through -- a path whose own
    # comment reads "shouldn't happen with current buckets". A bounds-fix packet may legitimately
    # change this, and must then update this assertion.
    assert get_rep_range_factor(20, 5) == get_rep_range_factor(5, 20)

    # Deliberately NOT asserted: total_reps. The effective rep total is 1.65 * 12.5, which lands
    # on a float boundary (20.625000000000004) where round()'s half-to-even rule makes any pinned
    # literal a footgun rather than a characterization.
