"""WPB.4 owner decision D2 — the exported "Weekly Summary" sheet carries the new figures.

`utils/export_service.py` is a real consumer of `calculate_weekly_summary()`:
`build_summary_sheets` calls it and `_weekly_summary_to_rows` splats **every** stat field
into the workbook, so the four fields WPB.4 changes (`frequency`, `sets_per_session`,
`avg_sets_per_session`, `max_sets_per_session`) reach an exported spreadsheet.

This coverage is **net new**. Before WPB.4 nothing under `tests/` imported
`utils/export_service.py` at all, and `tests/test_exports.py` — which tests
`utils/export_utils.py` — never referenced weekly summary, so it was green whether or not
the export path worked. That is why D2 was re-put to the owner at Gate 1 and the packet
was re-estimated M -> L.

Figures are pinned exactly, not merely checked for presence: `_weekly_summary_to_rows`
splats `**stats`, so a presence assertion passes whatever the numbers are and cannot
catch a denominator regression. Each sheet value is also cross-checked against the
`/weekly_summary` route JSON for the same seed, so the two consumers cannot drift apart.
"""
from __future__ import annotations

import pytest

from utils.export_service import build_summary_sheets

# One set at reps 8-10 / RIR 2 is worth 0.85 effective sets for a primary muscle.
EFF_PER_SET = 0.85


def _add_ex(db, name, primary):
    db.execute_query(
        """
        INSERT INTO exercises (exercise_name, primary_muscle_group, mechanic, movement_pattern)
        VALUES (?, ?, 'Isolated', 'lower_isolation')
        """,
        (name, primary),
    )


def _add_sel(db, routine, exercise, sets):
    """Insert directly — ``add_exercise`` rejects a falsy routine (`exercise_manager.py:36`)."""
    db.execute_query(
        """
        INSERT INTO user_selection (
            routine, exercise, sets, min_rep_range, max_rep_range, rir, rpe, weight
        ) VALUES (?, ?, ?, 8, 10, 2, NULL, 50.0)
        """,
        (routine, exercise, sets),
    )


def _seed_anonymous_only(db):
    _add_ex(db, "Anon Raise", "Calves")
    _add_sel(db, "", "Anon Raise", 2)


def _calves_row(sheets):
    assert "Weekly Summary" in sheets, "the anonymous-only plan must still produce the sheet"
    return next(row for row in sheets["Weekly Summary"] if row["muscle_group"] == "Calves")


@pytest.mark.usefixtures("clean_db")
def test_weekly_summary_sheet_pins_the_unassigned_bucket_figures(db_handler):
    """Exact values for a muscle sourced only from an empty-routine row."""
    _seed_anonymous_only(db_handler)

    calves = _calves_row(build_summary_sheets("Total"))

    assert calves["frequency"] == 1
    assert calves["sets_per_session"] == pytest.approx(2 * EFF_PER_SET)
    assert calves["avg_sets_per_session"] == pytest.approx(2 * EFF_PER_SET)
    assert calves["max_sets_per_session"] == pytest.approx(2 * EFF_PER_SET)
    # Volume figures are untouched by WPB.4 (criterion 7).
    assert calves["effective_weekly_sets"] == pytest.approx(2 * EFF_PER_SET)
    assert calves["raw_weekly_sets"] == pytest.approx(2.0)


@pytest.mark.usefixtures("clean_db")
def test_export_sheet_agrees_with_the_route_json(client, db_handler):
    """The workbook and the page must report the same numbers for the same seed."""
    _seed_anonymous_only(db_handler)

    sheet_calves = _calves_row(build_summary_sheets("Total"))

    response = client.get("/weekly_summary", headers={"Accept": "application/json"})
    assert response.status_code == 200
    rows = response.get_json()["data"]["weekly_summary"]
    route_calves = next(row for row in rows if row["muscle_group"] == "Calves")

    for field in ("frequency", "sets_per_session", "avg_sets_per_session", "max_sets_per_session"):
        assert sheet_calves[field] == pytest.approx(route_calves[field]), (
            f"export and route disagree on {field}"
        )


@pytest.mark.usefixtures("clean_db")
def test_below_threshold_bucket_is_exported_without_raising_frequency(db_handler):
    """The sub-1.0 asymmetry survives into the workbook: max moves, frequency does not."""
    _add_ex(db_handler, "Anon Raise", "Calves")
    _add_sel(db_handler, "", "Anon Raise", 1)  # 0.85 effective < 1.0

    calves = _calves_row(build_summary_sheets("Total"))

    assert calves["frequency"] == 0
    assert calves["avg_sets_per_session"] == 0.0
    assert calves["max_sets_per_session"] == pytest.approx(EFF_PER_SET)


@pytest.mark.usefixtures("clean_db")
def test_named_routines_export_unchanged(db_handler):
    """A plan with no anonymous rows must export exactly what it did before WPB.4."""
    _add_ex(db_handler, "Named Raise", "Calves")
    _add_sel(db_handler, "Legs A", "Named Raise", 2)

    calves = _calves_row(build_summary_sheets("Total"))

    assert calves["frequency"] == 1
    assert calves["sets_per_session"] == pytest.approx(2 * EFF_PER_SET)
    assert calves["max_sets_per_session"] == pytest.approx(2 * EFF_PER_SET)
