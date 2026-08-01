"""WPB.4 / OD4 — falsy routines bucket into one synthetic ``Unassigned`` session.

Weekly summary used to guard its frequency accumulation with ``if routine:``, so rows
with no routine name contributed volume but dropped out of the frequency signal. They now
coalesce into a single ``Unassigned`` session bucket, matching ``session_summary.py``.

**Seeding note.** These rows cannot be created through the product. ``add_exercise``
rejects a falsy routine at ``utils/exercise_manager.py:36`` and no route can update
``routine``, so an empty-routine row reaches a live database only via a restored backup,
legacy data, or a direct edit. Every scenario here therefore seeds ``user_selection``
directly, mirroring ``tests/test_weekly_summary_golden.py::_add_sel``. Do **not** "fix"
this by relaxing the ``exercise_manager`` guard — that guard is separately shipped
behavior (OD1) and is outside this packet's scope.

``routine`` is ``TEXT NOT NULL``, so a ``None`` routine is unreachable through the
database at all. Criterion 2 is therefore expressed against the private
``_aggregate_weekly_volumes`` helper, which is the only seam where ``None`` can appear
(mocked or legacy rows).

Owner decision **D1** is asserted here too: ``global_sessions``
(``weekly_summary.py:244``) still excludes the synthetic bucket, so it remains the
fallback denominator only for muscles that clear ``>= 1.0`` in no session at all.
"""
from __future__ import annotations

import pytest

from utils.effective_sets import CountingMode, ContributionMode
from utils.weekly_summary import (
    UNASSIGNED_ROUTINE,
    _aggregate_weekly_volumes,
    calculate_pattern_coverage,
    calculate_weekly_summary,
)

# One set at reps 8-10 / RIR 2 is worth 0.85 effective sets for a primary muscle.
# Two clear the >= 1.0 frequency threshold; one does not.
EFF_PER_SET = 0.85

MODE_MATRIX = [
    pytest.param(CountingMode.EFFECTIVE, ContributionMode.TOTAL, id="effective_total"),
    pytest.param(CountingMode.RAW, ContributionMode.TOTAL, id="raw_total"),
    pytest.param(CountingMode.EFFECTIVE, ContributionMode.DIRECT_ONLY, id="effective_direct"),
    pytest.param(CountingMode.RAW, ContributionMode.DIRECT_ONLY, id="raw_direct"),
]


def _add_ex(db, name, primary, pattern="lower_isolation"):
    db.execute_query(
        """
        INSERT INTO exercises (exercise_name, primary_muscle_group, mechanic, movement_pattern)
        VALUES (?, ?, 'Isolated', ?)
        """,
        (name, primary, pattern),
    )


def _add_sel(db, routine, exercise, sets, min_rep=8, max_rep=10, rir=2, weight=50.0):
    """Insert a plan row directly, bypassing ``add_exercise``'s non-empty routine guard."""
    db.execute_query(
        """
        INSERT INTO user_selection (
            routine, exercise, sets, min_rep_range, max_rep_range, rir, rpe, weight
        ) VALUES (?, ?, ?, ?, ?, ?, NULL, ?)
        """,
        (routine, exercise, sets, min_rep, max_rep, rir, weight),
    )


def _summary(counting=CountingMode.EFFECTIVE, contribution=ContributionMode.TOTAL):
    return calculate_weekly_summary(counting_mode=counting, contribution_mode=contribution)


# ---------------------------------------------------------------------------
# Criterion 1 — an empty-string routine is bucketed, not discarded
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(("counting", "contribution"), [(p.values[0], p.values[1]) for p in MODE_MATRIX],
                         ids=[p.id for p in MODE_MATRIX])
@pytest.mark.usefixtures("clean_db")
def test_empty_routine_counts_toward_frequency(db_handler, counting, contribution):
    _add_ex(db_handler, "Anon Raise", "Calves")
    _add_sel(db_handler, "", "Anon Raise", 2)

    calves = _summary(counting, contribution)["Calves"]

    assert calves["frequency"] == 1, "the empty-routine bucket must count as one session"
    assert calves["effective_weekly_sets"] == pytest.approx(2 * EFF_PER_SET)
    assert calves["raw_weekly_sets"] == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# Criterion 2 — a None routine lands in the same bucket (helper-level only)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("falsy", [None, "", 0], ids=["none", "empty_string", "zero"])
def test_every_falsy_routine_uses_the_same_bucket(falsy):
    """``routine`` is TEXT NOT NULL, so None is reachable only through this helper."""
    row = {
        "routine": falsy,
        "sets": 2,
        "min_rep_range": 8,
        "max_rep_range": 10,
        "rir": 2,
        "rpe": None,
        "weight": 50.0,
        "primary_muscle_group": "Calves",
        "secondary_muscle_group": None,
        "tertiary_muscle_group": None,
    }

    _, _, sessions_by_muscle = _aggregate_weekly_volumes([row], ContributionMode.TOTAL)

    assert list(sessions_by_muscle["Calves"]) == [UNASSIGNED_ROUTINE]


# ---------------------------------------------------------------------------
# Criterion 3 — many anonymous rows accumulate into exactly ONE bucket
# ---------------------------------------------------------------------------
@pytest.mark.usefixtures("clean_db")
def test_multiple_anonymous_rows_collapse_into_one_session(db_handler):
    _add_ex(db_handler, "Anon A", "Calves")
    _add_ex(db_handler, "Anon B", "Calves")
    _add_ex(db_handler, "Anon C", "Calves")
    for exercise in ("Anon A", "Anon B", "Anon C"):
        _add_sel(db_handler, "", exercise, 1)

    calves = _summary()["Calves"]

    assert calves["frequency"] == 1, "three anonymous rows are one session, not three"
    assert calves["effective_weekly_sets"] == pytest.approx(3 * EFF_PER_SET)
    # Accumulated before the threshold test: 3 x 0.85 = 2.55 clears 1.0 as a sum.
    assert calves["max_sets_per_session"] == pytest.approx(3 * EFF_PER_SET)


# ---------------------------------------------------------------------------
# Criteria 4 + 5 — the >= 1.0 threshold applies to the bucket on the same terms
# ---------------------------------------------------------------------------
@pytest.mark.usefixtures("clean_db")
def test_bucket_at_or_above_threshold_raises_frequency(db_handler):
    _add_ex(db_handler, "Anon Raise", "Calves")
    _add_sel(db_handler, "", "Anon Raise", 2)  # 1.7 effective >= 1.0

    calves = _summary()["Calves"]

    assert calves["frequency"] == 1
    assert calves["avg_sets_per_session"] == pytest.approx(2 * EFF_PER_SET)
    assert calves["max_sets_per_session"] == pytest.approx(2 * EFF_PER_SET)
    # frequency > 0, so the global_sessions fallback is not used.
    assert calves["sets_per_session"] == pytest.approx(2 * EFF_PER_SET)


@pytest.mark.usefixtures("clean_db")
def test_bucket_below_threshold_does_not_raise_frequency(db_handler):
    """A sub-1.0 bucket leaves ``frequency`` at 0 — but still moves ``max_sets_per_session``.

    ``max_sets_per_session`` (``weekly_summary.py:193``) reads ``muscle_sessions``
    directly and applies no threshold, so it changes from 0.0 to the bucket value while
    ``frequency`` and ``avg_sets_per_session`` stay at zero. That asymmetry is intended.
    """
    _add_ex(db_handler, "Anon Raise", "Calves")
    _add_ex(db_handler, "Named Curl", "Biceps", pattern="upper_isolation")
    _add_sel(db_handler, "", "Anon Raise", 1)          # 0.85 effective < 1.0
    _add_sel(db_handler, "Pull A", "Named Curl", 4)

    calves = _summary()["Calves"]

    assert calves["frequency"] == 0
    assert calves["avg_sets_per_session"] == 0.0
    assert calves["max_sets_per_session"] == pytest.approx(EFF_PER_SET)


# ---------------------------------------------------------------------------
# Criterion 6 — named and anonymous sessions count additively
# ---------------------------------------------------------------------------
@pytest.mark.usefixtures("clean_db")
def test_named_and_anonymous_sessions_are_additive(db_handler):
    _add_ex(db_handler, "Shared Raise", "Calves")
    _add_sel(db_handler, "Legs A", "Shared Raise", 2)
    _add_sel(db_handler, "Legs B", "Shared Raise", 2)
    _add_sel(db_handler, "", "Shared Raise", 2)

    calves = _summary()["Calves"]

    assert calves["frequency"] == 3, "two named routines plus the one anonymous bucket"
    assert calves["max_sets_per_session"] == pytest.approx(2 * EFF_PER_SET)


# ---------------------------------------------------------------------------
# Owner decision D1 — global_sessions still EXCLUDES the synthetic bucket
# ---------------------------------------------------------------------------
@pytest.mark.usefixtures("clean_db")
def test_d1_global_sessions_excludes_the_synthetic_bucket(db_handler):
    """A zero-frequency muscle's fallback denominator must not count the bucket.

    ``Forearms`` here never clears 1.0 in any session, so its ``sets_per_session`` falls
    back to ``len(global_sessions)``. Under D1 that set holds only the two *named*
    routines, so the divisor is 2. Had the bucket been included it would be 3, and this
    assertion is what catches that regression.
    """
    _add_ex(db_handler, "Anon Raise", "Calves")
    _add_ex(db_handler, "Grip A", "Forearms", pattern="upper_isolation")
    _add_ex(db_handler, "Grip B", "Forearms", pattern="upper_isolation")
    _add_sel(db_handler, "", "Anon Raise", 2)
    _add_sel(db_handler, "Grip Day", "Grip A", 1, min_rep=30, max_rep=40, rir=8)
    _add_sel(db_handler, "Grip Day 2", "Grip B", 1, min_rep=30, max_rep=40, rir=8)

    forearms = _summary()["Forearms"]

    assert forearms["frequency"] == 0, "neither grip session clears 1.0 effective sets"
    expected = forearms["effective_weekly_sets"] / 2  # 2 named routines, bucket excluded
    assert forearms["sets_per_session"] == pytest.approx(expected, abs=0.01)


# ---------------------------------------------------------------------------
# Criterion 7 — totals are invariant to whether the routine is named
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(("counting", "contribution"), [(p.values[0], p.values[1]) for p in MODE_MATRIX],
                         ids=[p.id for p in MODE_MATRIX])
@pytest.mark.usefixtures("clean_db")
def test_totals_are_identical_whether_the_routine_is_named(db_handler, counting, contribution):
    """The same rows must produce the same volume figures under either routine value."""
    invariant = (
        "weekly_sets", "raw_weekly_sets", "effective_weekly_sets",
        "total_reps", "total_volume", "raw_total_reps", "raw_total_volume",
        "status", "volume_class",
    )

    _add_ex(db_handler, "Swing Raise", "Calves")
    _add_sel(db_handler, "", "Swing Raise", 2)
    anonymous = _summary(counting, contribution)["Calves"]

    db_handler.execute_query("DELETE FROM user_selection")
    _add_sel(db_handler, "Legs A", "Swing Raise", 2)
    named = _summary(counting, contribution)["Calves"]

    for field in invariant:
        assert anonymous[field] == named[field], f"{field} must not depend on the routine name"


# ---------------------------------------------------------------------------
# Criterion 8 — no muscle key is added or removed
# ---------------------------------------------------------------------------
@pytest.mark.usefixtures("clean_db")
def test_the_bucket_is_a_session_key_not_a_muscle_row(db_handler):
    """``Unassigned`` lives inside ``sessions_by_muscle``, never in the output keys."""
    _add_ex(db_handler, "Anon Raise", "Calves")
    _add_sel(db_handler, "", "Anon Raise", 2)

    summary = _summary()

    assert set(summary) == {"Calves"}
    assert UNASSIGNED_ROUTINE not in summary


# ---------------------------------------------------------------------------
# Criterion 11 — pattern coverage keeps keying falsy routines as ''
# ---------------------------------------------------------------------------
@pytest.mark.usefixtures("clean_db")
def test_pattern_coverage_still_keys_falsy_routines_as_empty_string(db_handler):
    _add_ex(db_handler, "Anon Raise", "Calves")
    _add_sel(db_handler, "", "Anon Raise", 2)

    coverage = calculate_pattern_coverage()

    assert "" in coverage["sets_per_routine"]
    assert UNASSIGNED_ROUTINE not in coverage["sets_per_routine"]
    assert UNASSIGNED_ROUTINE not in coverage["per_routine"]


# ---------------------------------------------------------------------------
# Accepted collision — a real routine named 'Unassigned' merges with the bucket
# ---------------------------------------------------------------------------
@pytest.mark.usefixtures("clean_db")
def test_a_real_routine_named_unassigned_merges_with_the_bucket(db_handler):
    """Accepted behavior, inherited from ``session_summary.py``. Documented, not fixed."""
    _add_ex(db_handler, "Anon Raise", "Calves")
    _add_sel(db_handler, "", "Anon Raise", 2)
    _add_sel(db_handler, UNASSIGNED_ROUTINE, "Anon Raise", 2)

    calves = _summary()["Calves"]

    assert calves["frequency"] == 1, "the homonym merges rather than counting separately"
    assert calves["max_sets_per_session"] == pytest.approx(4 * EFF_PER_SET)


# ---------------------------------------------------------------------------
# D3 — the route JSON carries the corrected values (DB-backed, unmocked)
# ---------------------------------------------------------------------------
@pytest.mark.usefixtures("clean_db")
def test_route_json_reports_the_corrected_frequency_and_per_session_values(client, db_handler):
    """Owner decision D3, and the amended criterion 10.

    D5 replaced criterion 10's browser assertion with this one. The rendered "Routines"
    column is ``row.frequency`` (``static/js/modules/weekly-summary.js:211``), so the
    payload asserted here is exactly what the page displays;
    ``avg_sets_per_session`` / ``max_sets_per_session`` are not rendered anywhere and are
    observable only here and in the Excel export.

    This test deliberately does NOT patch ``calculate_weekly_summary`` — a mocked
    assertion would pass against unmodified production code.
    """
    _add_ex(db_handler, "Anon Raise", "Calves")
    _add_sel(db_handler, "", "Anon Raise", 2)

    response = client.get("/weekly_summary", headers={"Accept": "application/json"})
    assert response.status_code == 200

    rows = response.get_json()["data"]["weekly_summary"]
    calves = next(row for row in rows if row["muscle_group"] == "Calves")

    assert calves["frequency"] == 1
    assert calves["avg_sets_per_session"] == pytest.approx(2 * EFF_PER_SET)
    assert calves["max_sets_per_session"] == pytest.approx(2 * EFF_PER_SET)
    assert calves["sets_per_session"] == pytest.approx(2 * EFF_PER_SET)
