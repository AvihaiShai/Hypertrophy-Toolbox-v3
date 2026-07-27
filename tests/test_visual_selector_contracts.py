from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_visual_helper_uses_stable_hooks_not_presentation_classes():
    helper = read("e2e/visual-helpers.ts")
    presentation_selectors = (
        ".card",
        ".collapsible-frame",
        ".frame-calm-glass",
        ".glass-neumorph-card",
        ".page-header",
        ".summary-frame",
        ".table-header",
        ".table-calm",
        ".wpdd-button",
        ".form-control",
        ".form-select",
        ".filter-dropdown",
        ".uniform-input",
        ".nav-icon",
        ".toggle-icon",
        ".wpdd-caret",
    )

    assert not any(selector in helper for selector in presentation_selectors)
    assert "[data-visual-surface]" in helper
    assert "[data-visual-icon]" in helper
    assert "[data-visual-control]" in helper


def test_visual_matrix_covers_profile_and_backup():
    visual_spec = read("e2e/visual.spec.ts")

    assert "{ name: 'user-profile', route: ROUTES.USER_PROFILE }" in visual_spec
    assert "{ name: 'backup', route: ROUTES.BACKUP }" in visual_spec
    assert 'data-testid="user-profile-page"' in read("templates/user_profile.html")
    assert 'data-testid="backup-center-page"' in read("templates/backup.html")


def test_visual_matrix_covers_fatigue_the_purely_shared_css_route():
    """`/fatigue` is painted 100% by the shared global bundles.

    `templates/fatigue.html` declares no `page_css` block and links no
    stylesheet of its own, so every pixel on it comes from the seven surfaces
    the WP4.4 arc rewrites. It was the one rendered route with no pixel oracle
    at all, which made "no unexplained visual differences" unfalsifiable exactly
    where shared-CSS exposure is highest. Baselines created by WP4.4-a under
    owner ruling N7.
    """
    visual_spec = read("e2e/visual.spec.ts")
    fixtures = read("e2e/fixtures.ts")
    template = read("templates/fatigue.html")

    assert "FATIGUE: '/fatigue'," in fixtures
    assert "{ name: 'fatigue', route: ROUTES.FATIGUE }," in visual_spec

    # The premise of the test above: if fatigue.html ever gains its own bundle,
    # this route stops being the pure shared-CSS canary and the reasoning that
    # justified the baselines no longer holds.
    assert "page_css" not in template
    assert ".css" not in template

    snapshots = ROOT / "e2e" / "__screenshots__" / "win32" / "visual.spec.ts-snapshots"
    for viewport in ("mobile", "tablet", "desktop"):
        for theme in ("light", "dark"):
            assert (snapshots / f"fatigue-{viewport}-{theme}.png").is_file()


def test_style_assertions_resolve_semantic_tokens_without_literal_rgb():
    nav_spec = read("e2e/nav-dropdown.spec.ts")
    summary_spec = read("e2e/summary-pages.spec.ts")

    assert "--nav-icon-accent" in nav_spec
    assert "data-nav-icon" in nav_spec
    assert "rgb(109, 93, 252)" not in nav_spec
    assert "rgb(15, 159, 143)" not in nav_spec
    assert "rgb(217, 119, 6)" not in nav_spec

    for token in ("--bs-danger", "--bs-orange", "--bs-success", "--bs-purple"):
        assert token in summary_spec
    assert "data-volume-level" in summary_spec
    assert "rgb(220, 53, 69)" not in summary_spec
    assert "rgb(253, 126, 20)" not in summary_spec
    assert "rgb(25, 135, 84)" not in summary_spec
    assert "rgb(111, 66, 193)" not in summary_spec
