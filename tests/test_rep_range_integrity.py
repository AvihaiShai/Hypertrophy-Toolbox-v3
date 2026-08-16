"""Unit coverage for the read-only rep-range diagnostic.

The module exists to name the ``user_selection`` rows behind a bounds failure so
the user can repair them. What is asserted here is therefore mostly about
*honesty*: that it reports the row the failing caller actually read, that it
reports nothing when it knows nothing, and that it never becomes the reason a
request fails.

Harness non-claim
-----------------
The direct ``UPDATE`` below writes a value the plan routes reject. That is a
device for constructing a persisted state, not a modelled user action. The state
is reachable in production through a backup taken before ``validate_workout_bounds``
gated those columns and restored before #384 closed that ingress.
"""
from __future__ import annotations

import sqlite3

import pytest

import routes.exports as exports_route
import routes.progression_plan as progression_route
import routes.session_summary as session_route
import routes.weekly_summary as weekly_route

from utils import rep_range_integrity
from utils.workout_validation import validate_workout_bounds
from utils.rep_range_integrity import (
    MAX_NAMED_ROWS,
    PLAN_VALUE_LABEL,
    UNASSIGNED_ROUTINE,
    accepts_in_isolation,
    annotate,
    scan_exercise_plan_default,
    scan_export_bounds,
    scan_rep_ranges,
    suppressed_for,
)

ROUTINE = "GYM - Full Body - Workout A"
OTHER_ROUTINE = "GYM - Full Body - Workout B"


@pytest.fixture
def plan_row(clean_db, exercise_factory, workout_plan_factory):
    """Create a plan row, optionally forcing one column past the validator."""

    created: set[str] = set()

    def _plan_row(name="Diagnostic Curl", routine=ROUTINE, column=None, value=None, **kwargs):
        # exercises.exercise_name is the PRIMARY KEY, so a second plan row for
        # the same exercise must not re-insert the catalog entry.
        if name not in created:
            exercise_factory(name, primary_muscle_group="Biceps")
            created.add(name)
        plan_id = workout_plan_factory(exercise_name=name, routine=routine, **kwargs)
        if column is not None:
            clean_db.execute_query(
                f"UPDATE user_selection SET {column} = ? WHERE id = ?", (value, plan_id)
            )
        return plan_id

    return _plan_row


class TestAcceptsInIsolation:
    """The shared predicate behind both the scan and the edit-order fix."""

    @pytest.mark.parametrize("value", [6, 12, 0, 8.5, "10"])
    def test_usable_numbers_are_accepted(self, value):
        assert accepts_in_isolation("min_reps", value) is True

    @pytest.mark.parametrize("value", ["abc", "", None, "nan", "inf", float("inf"), True])
    def test_unusable_values_are_rejected(self, value):
        # 'nan'/'inf' are the cases a bare float() would wrongly accept, and a
        # bool is the case float() would silently turn into 1.0.
        assert accepts_in_isolation("min_reps", value) is False

    def test_cross_field_verdicts_cannot_reach_it(self):
        """Isolation is what keeps min > max out of the diagnostic.

        An inverted-but-numeric pair is a real validation error, but it is not
        what makes the analysis pages raise, so it must not be reported as the
        cause of one.
        """
        assert accepts_in_isolation("min_reps", 20) is True
        assert accepts_in_isolation("max_reps", 5) is True
        # Control: without this, the two assertions above are equally
        # consistent with there being no cross-field rule at all.
        assert validate_workout_bounds(min_reps=20, max_reps=5) is not None


class TestScanRepRanges:
    def test_clean_plan_reports_nothing(self, plan_row):
        plan_row()
        assert scan_rep_ranges() == []

    def test_inverted_but_numeric_range_reports_nothing(self, plan_row):
        """Guards the A5/P3 boundary: over-reporting misdirects the repair."""
        plan_row(min_rep_range=20, max_rep_range=5)
        assert scan_rep_ranges() == []

    @pytest.mark.parametrize(
        "column,expected",
        [
            ("min_rep_range", "Minimum reps must be a finite number."),
            ("max_rep_range", "Maximum reps must be a finite number."),
        ],
    )
    def test_poisoned_column_is_named_with_its_own_reason(self, plan_row, column, expected):
        plan_row(column=column, value="abc")
        assert scan_rep_ranges() == [
            {"routine": ROUTINE, "exercise": "Diagnostic Curl", "reason": expected}
        ]

    def test_empty_string_is_reported(self, plan_row):
        """NOT NULL rejects NULL but not '', so the empty string is reachable."""
        plan_row(column="min_rep_range", value="")
        assert len(scan_rep_ranges()) == 1

    def test_falsy_routine_renders_as_unassigned(self, plan_row):
        plan_row(routine="", column="min_rep_range", value="abc")
        assert scan_rep_ranges()[0]["routine"] == UNASSIGNED_ROUTINE

    def test_routine_filter_excludes_other_routines(self, plan_row):
        plan_row(name="Mine", routine=ROUTINE, column="min_rep_range", value="abc")
        plan_row(name="Theirs", routine=OTHER_ROUTINE, column="min_rep_range", value="abc")

        scoped = scan_rep_ranges(ROUTINE)
        assert [row["exercise"] for row in scoped] == ["Mine"]
        assert len(scan_rep_ranges()) == 2

    def test_swallows_its_own_failure(self, plan_row, monkeypatch):
        """A broken diagnostic must report nothing, never raise."""
        plan_row(column="min_rep_range", value="abc")
        monkeypatch.setattr(
            rep_range_integrity,
            "DatabaseHandler",
            lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")),
        )
        assert scan_rep_ranges() == []


class TestScanExercisePlanDefault:
    def test_names_only_the_requested_exercise(self, plan_row):
        plan_row(name="Asked For", column="max_rep_range", value="abc")
        plan_row(name="Not Asked For", column="max_rep_range", value="abc")

        findings = scan_exercise_plan_default("Asked For")
        assert [row["exercise"] for row in findings] == ["Asked For"]

    def test_reads_the_same_row_the_route_reads(self, plan_row):
        """get_exercise_plan_defaults takes ORDER BY id DESC LIMIT 1.

        The older row is poisoned and the newer one is clean, so a scan that
        ignored the ordering would blame a row the route never read.
        """
        plan_row(name="Curl", routine=ROUTINE, column="max_rep_range", value="abc")
        plan_row(name="Curl", routine=OTHER_ROUTINE)

        assert scan_exercise_plan_default("Curl") == []

    def test_unknown_exercise_reports_nothing(self, plan_row):
        plan_row()
        assert scan_exercise_plan_default("No Such Exercise") == []


class TestScanExportBounds:
    def test_mirrors_allow_null_true(self, plan_row):
        """export_plan_to_workout_log passes allow_null=True, so '' is accepted.

        Scanning with the stricter default would report a row that the export
        itself lets through — naming a field the row did not fail on.
        """
        plan_row(column="min_rep_range", value="")
        assert scan_export_bounds() == []
        # The same row is a finding for the analysis surfaces, which validate
        # with allow_null=False. The two scans are deliberately not the same.
        assert len(scan_rep_ranges()) == 1

    def test_reports_non_rep_columns_too(self, plan_row):
        """The export validates all four bounded columns, so the scan must too."""
        plan_row(column="weight", value="abc")
        assert scan_export_bounds() == [
            {
                "routine": ROUTINE,
                "exercise": "Diagnostic Curl",
                "reason": "Weight must be a finite number.",
            }
        ]

    def test_nullable_rir_is_accepted(self, plan_row):
        plan_row(column="rir", value=None)
        assert scan_export_bounds() == []


class TestAnnotate:
    def test_empty_findings_returns_the_message_byte_for_byte(self):
        original = "Unable to load weekly summary."
        assert annotate(original, []) is original

    def test_names_routine_and_exercise(self):
        message = annotate(
            "Unable to load weekly summary.",
            [{"routine": "Push Day", "exercise": "Bench", "reason": "Minimum reps must be a finite number."}],
        )
        assert "Push Day / Bench" in message
        assert message.startswith("Unable to load weekly summary.")
        assert "\n" not in message

    def test_caps_the_list_and_counts_the_remainder(self):
        findings = [
            {"routine": f"R{index}", "exercise": f"E{index}", "reason": "Minimum reps must be a finite number."}
            for index in range(MAX_NAMED_ROWS + 3)
        ]
        message = annotate("Boom.", findings)

        assert "(+3 more)" in message
        assert "E0" in message, "the first row must survive the cap"
        assert f"E{MAX_NAMED_ROWS}" not in message

    def test_reason_is_not_repeated_when_it_is_already_the_message(self):
        reason = "Minimum reps must be a finite number."
        message = annotate(reason, [{"routine": "R", "exercise": "E", "reason": reason}], PLAN_VALUE_LABEL)
        assert message.count(reason) == 1
        assert "R / E." in message


# --- Cross-cutting oracles -------------------------------------------------
#
# These two classes are the reason the diagnostic can claim to be free on a
# healthy database and harmless on a broken one. Both are written to be
# falsifiable: the first counts calls rather than patching the scanner to raise
# (the module swallows its own exceptions, so a raise-patch would pass whether
# or not the scanner ever ran), and the second breaks the scanner for real and
# pins the resulting message to the byte.


@pytest.fixture
def clean_plan(clean_db, exercise_factory, workout_plan_factory):
    exercise_factory("Healthy Curl", primary_muscle_group="Biceps")
    workout_plan_factory(exercise_name="Healthy Curl", routine=ROUTINE)


class TestTheScannerNeverRunsOnAHealthyDatabase:
    """No extra work on any path that succeeds today."""

    @pytest.fixture
    def calls(self, monkeypatch):
        recorded = []

        def _counted(*args, **kwargs):
            recorded.append(args)
            return []

        # Patched per route module, because that is where the name is bound.
        monkeypatch.setattr(weekly_route, "scan_rep_ranges", _counted)
        monkeypatch.setattr(session_route, "scan_rep_ranges", _counted)
        monkeypatch.setattr(exports_route, "scan_rep_ranges", _counted)
        monkeypatch.setattr(exports_route, "scan_export_bounds", _counted)
        monkeypatch.setattr(progression_route, "scan_exercise_plan_default", _counted)
        return recorded

    def test_weekly_summary(self, client, clean_plan, calls):
        assert client.get("/weekly_summary").status_code == 200
        assert calls == []

    def test_session_summary(self, client, clean_plan, calls):
        assert client.get("/session_summary").status_code == 200
        assert calls == []

    def test_excel_export(self, client, clean_plan, calls):
        assert client.get("/export_to_excel").status_code == 200
        assert calls == []

    def test_plan_to_log_export(self, client, clean_plan, calls):
        assert client.post("/export_to_workout_log").status_code == 200
        assert calls == []

    def test_exercise_suggestions(self, client, clean_plan, calls):
        response = client.post(
            "/get_exercise_suggestions", json={"exercise": "Healthy Curl"}
        )
        assert response.status_code == 200
        assert calls == []

    def test_empty_plan_export_is_a_conformant_failure(self, client, clean_db, calls):
        """NO_DATA is an empty plan, not a broken one.

        It is the one non-exception failure branch the wiring touches, so it is
        the case most likely to acquire a scan by accident.
        """
        response = client.post("/export_to_workout_log")

        assert response.status_code == 400
        assert response.get_json()["error"]["code"] == "NO_DATA"
        assert calls == []


class TestABrokenScannerCannotMaskTheRealFailure:
    """The diagnostic degrades to silence, never to a different outcome.

    Precedent for the bug class: a helper newly called inside an ``except``
    raised there and replaced the real error with its own.
    """

    @pytest.fixture
    def broken_scanner(self, monkeypatch):
        def _explode(*args, **kwargs):
            raise RuntimeError("diagnostic database unavailable")

        # Break the scanner's own database access, which is its realistic
        # failure mode. The routes keep their own working handler, so the
        # poisoned row still produces the genuine failure being described.
        monkeypatch.setattr(rep_range_integrity, "DatabaseHandler", _explode)

    @pytest.fixture
    def poisoned(self, clean_db, exercise_factory, workout_plan_factory):
        exercise_factory("Broken Scanner Press", primary_muscle_group="Chest")
        plan_id = workout_plan_factory(
            exercise_name="Broken Scanner Press", routine=ROUTINE
        )
        clean_db.execute_query(
            "UPDATE user_selection SET min_rep_range = ? WHERE id = ?", ("abc", plan_id)
        )
        return plan_id

    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            ("/weekly_summary", "Unable to fetch weekly summary"),
            ("/session_summary", "Unable to fetch session summary"),
        ],
    )
    def test_summary_surfaces_keep_their_original_message(
        self, client, poisoned, broken_scanner, url, expected
    ):
        response = client.get(url, headers={"X-Requested-With": "XMLHttpRequest"})

        assert response.status_code == 500
        assert response.get_json()["message"] == expected

    def test_excel_export_keeps_its_original_message(
        self, client, poisoned, broken_scanner
    ):
        response = client.get("/export_to_excel")

        assert response.status_code == 500
        assert (
            response.get_json()["message"]
            == "Failed to export data to Excel. Please try again."
        )

    def test_plan_to_log_keeps_its_original_message_and_status(
        self, client, poisoned, broken_scanner
    ):
        response = client.post("/export_to_workout_log")

        assert response.status_code == 400
        assert response.get_json()["message"] == "Minimum reps must be a finite number."

    def test_suggestions_keep_their_original_message(
        self, client, clean_db, exercise_factory, workout_plan_factory, broken_scanner
    ):
        exercise_factory("Broken Suggestion Press", primary_muscle_group="Chest")
        plan_id = workout_plan_factory(
            exercise_name="Broken Suggestion Press", routine=ROUTINE
        )
        clean_db.execute_query(
            "UPDATE user_selection SET max_rep_range = ? WHERE id = ?", ("abc", plan_id)
        )

        response = client.post(
            "/get_exercise_suggestions", json={"exercise": "Broken Suggestion Press"}
        )

        assert response.status_code == 500
        assert response.get_json()["message"] == "Failed to get exercise suggestions"


class TestACorruptionErrorIsNeverDescribed:
    """Opening a connection to describe a corrupt database can destroy it.

    ``get_db_connection`` reacts to a malformed/not-a-database error by renaming
    the live file to ``<name>.corrupted_<timestamp>``. The scanner opens its own
    connection, so on that one class of failure it has to stay silent — its
    ``except`` swallow is too late, because the rename happens during connect.
    """

    def test_database_errors_are_suppressed(self):
        assert suppressed_for(sqlite3.DatabaseError("file is not a database")) is True
        assert suppressed_for(sqlite3.DatabaseError("database disk image is malformed")) is True

    def test_ordinary_failures_are_not_suppressed(self):
        """The failure this packet exists for is a TypeError, so it must pass."""
        assert suppressed_for(TypeError("can only concatenate str")) is False
        assert suppressed_for(ValueError("bad value")) is False
        assert suppressed_for(None) is False

    @pytest.mark.parametrize(
        ("url", "expected"),
        [
            ("/weekly_summary", "Unable to fetch weekly summary"),
            ("/session_summary", "Unable to fetch session summary"),
        ],
    )
    def test_summary_routes_do_not_scan_after_a_database_error(
        self, client, clean_db, exercise_factory, workout_plan_factory,
        monkeypatch, url, expected,
    ):
        exercise_factory("Corruption Press", primary_muscle_group="Chest")
        plan_id = workout_plan_factory(
            exercise_name="Corruption Press", routine=ROUTINE
        )
        clean_db.execute_query(
            "UPDATE user_selection SET min_rep_range = ? WHERE id = ?", ("abc", plan_id)
        )

        module = weekly_route if url == "/weekly_summary" else session_route
        target = (
            "calculate_weekly_summary"
            if url == "/weekly_summary"
            else "calculate_session_summary"
        )

        def _corrupt(*args, **kwargs):
            raise sqlite3.DatabaseError("database disk image is malformed")

        calls = []
        monkeypatch.setattr(module, target, _corrupt)
        monkeypatch.setattr(
            module, "scan_rep_ranges", lambda *a, **k: calls.append(a) or []
        )

        response = client.get(url, headers={"X-Requested-With": "XMLHttpRequest"})

        assert response.status_code == 500
        assert response.get_json()["message"] == expected
        # The poisoned row is present and would otherwise be named; the guard,
        # not an empty database, is what keeps the scan from running.
        assert calls == []
