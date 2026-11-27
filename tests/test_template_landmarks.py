"""Structural contracts for the shared main-content landmark."""

from pathlib import Path


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
