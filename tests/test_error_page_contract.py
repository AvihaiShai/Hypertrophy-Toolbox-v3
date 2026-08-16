"""Contract tests for route-level renders of the shared error page."""

import pytest

import routes.body_composition as body_composition_route
import routes.fatigue as fatigue_route
import routes.program_backup as program_backup_route
import routes.progression_plan as progression_plan_route
import routes.session_summary as session_summary_route
import routes.user_profile as user_profile_route
import routes.weekly_summary as weekly_summary_route


def _raise(*_args, **_kwargs):
    raise RuntimeError("forced route failure")


@pytest.mark.parametrize(
    ("route_module", "failure_target", "url", "expected_message"),
    [
        (
            weekly_summary_route,
            "calculate_weekly_summary",
            "/weekly_summary",
            "Unable to load weekly summary.",
        ),
        (
            session_summary_route,
            "calculate_session_summary",
            "/session_summary",
            "Unable to load session summary.",
        ),
        (
            progression_plan_route,
            "DatabaseHandler",
            "/progression",
            "Unable to load progression plan.",
        ),
        (
            program_backup_route,
            "list_backups",
            "/backup",
            "Unable to load backup center.",
        ),
        (
            body_composition_route,
            "DatabaseHandler",
            "/body_composition",
            "Unable to load Body Composition.",
        ),
        (
            user_profile_route,
            "DatabaseHandler",
            "/user_profile",
            "Unable to load user profile.",
        ),
        (
            fatigue_route,
            "build_fatigue_page_context",
            "/fatigue",
            "Unable to load fatigue page",
        ),
    ],
)
def test_route_error_page_uses_shared_template_contract(
    client,
    monkeypatch,
    route_module,
    failure_target,
    url,
    expected_message,
):
    """Every route supplies the title, status code, and message expected by error.html."""
    monkeypatch.setattr(route_module, failure_target, _raise)

    response = client.get(url)

    assert response.status_code == 500
    assert b"<title>Server Error - Hypertrophy Toolbox</title>" in response.data
    assert b'<h1 class="error-status-code">500</h1>' in response.data
    assert b'<h2 class="error-title">Server Error</h2>' in response.data
    assert expected_message.encode() in response.data


ROUTINE = "GYM - Full Body - Workout A"
POISONED_EXERCISE = "Diagnostic Incline Press"


@pytest.fixture
def poisoned_plan(clean_db, exercise_factory, workout_plan_factory):
    """A plan row whose stored min_rep_range is not a number.

    The direct UPDATE is a device for building a persisted state, not a modelled
    user action: it is what a pre-#384 restore of a pre-validation backup left
    behind. Nothing is mocked here — the real calculation raises on its own.
    """
    exercise_factory(POISONED_EXERCISE, primary_muscle_group="Chest")
    plan_id = workout_plan_factory(exercise_name=POISONED_EXERCISE, routine=ROUTINE)
    clean_db.execute_query(
        "UPDATE user_selection SET min_rep_range = ? WHERE id = ?", ("abc", plan_id)
    )
    return plan_id


@pytest.fixture
def clean_plan(clean_db, exercise_factory, workout_plan_factory):
    exercise_factory(POISONED_EXERCISE, primary_muscle_group="Chest")
    return workout_plan_factory(exercise_name=POISONED_EXERCISE, routine=ROUTINE)


@pytest.mark.parametrize("url", ["/weekly_summary", "/session_summary"])
def test_error_page_names_the_row_to_repair(client, poisoned_plan, url):
    """The 500 page must identify the routine and exercise, not just fail."""
    response = client.get(url)

    assert response.status_code == 500
    body = response.data.decode()
    assert ROUTINE in body
    assert POISONED_EXERCISE in body
    assert "Minimum reps must be a finite number." in body


@pytest.mark.parametrize("url", ["/weekly_summary", "/session_summary"])
def test_clean_plan_never_mentions_a_routine(client, clean_plan, monkeypatch, url):
    """Paired negative for the test above.

    Without it, a page whose boilerplate happened to contain the routine name
    would satisfy the positive assertion for the wrong reason. The failure is
    forced here so the comparison is between two 500 pages, not between a 500
    and a 200.
    """
    module = weekly_summary_route if url == "/weekly_summary" else session_summary_route
    target = (
        "calculate_weekly_summary"
        if url == "/weekly_summary"
        else "calculate_session_summary"
    )
    monkeypatch.setattr(module, target, _raise)

    response = client.get(url)

    assert response.status_code == 500
    body = response.data.decode()
    assert ROUTINE not in body
    assert POISONED_EXERCISE not in body
    assert "Fix these in the Workout Plan editor." not in body
