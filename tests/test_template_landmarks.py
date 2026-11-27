"""Structural contracts for the shared main-content landmark."""

from pathlib import Path
import re


TEMPLATES = Path(__file__).resolve().parents[1] / "templates"


def test_base_owns_skip_target_and_single_main_landmark(client, clean_db):
    base = (TEMPLATES / "base.html").read_text(encoding="utf-8")

    assert 'class="nb-skip-link" href="#main-content"' in base
    assert base.count("<main") == 1
    assert base.count("</main>") == 1
    for route, frame in (("/", "container-fluid mt-4"), ("/workout_log", "ui-page-frame")):
        response = client.get(route)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert html.count("<main") == 1
        assert f'<main id="main-content" class="{frame}" tabindex="-1">' in html


def test_child_templates_do_not_define_additional_main_landmarks():
    offenders = []
    for template in TEMPLATES.glob("*.html"):
        if template.name == "base.html":
            continue
        source = template.read_text(encoding="utf-8")
        if "<main" in source or 'role="main"' in source:
            offenders.append(template.name)

    assert offenders == []


def test_workout_plan_template_orders_header_exercise_list_then_add_exercise():
    source = (TEMPLATES / "workout_plan.html").read_text(encoding="utf-8")
    header = re.search(r"<header\b[^>]*>\s*<h1\b", source)
    exercise_list = re.search(r'<section\b[^>]*aria-labelledby="workout-plan-table-heading"', source)
    add_exercise = re.search(r"<h2\b[^>]*>\s*Add exercise\s*</h2>", source, re.IGNORECASE)

    assert header is not None, "Workout Plan has a page header"
    assert exercise_list is not None, "Workout Plan has a named exercise list panel"
    assert add_exercise is not None, "Workout Plan has a named Add exercise panel"
    assert header.start() < exercise_list.start() < add_exercise.start()
