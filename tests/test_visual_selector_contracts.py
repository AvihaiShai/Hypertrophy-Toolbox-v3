import re
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


def test_border_preserve_hook_is_inert_and_used_only_by_the_visual_helper():
    """`data-visual-preserve-border` is a test-only hook and must stay one.

    The visual determinism layer flattens border geometry on every
    `[data-visual-surface]`. The Progression goals table's borders are owned by
    the shared Calm Glass table family instead — but only because that family's
    `:is()` list borrows ID-level weight from its `#workout` branch. A
    specificity repair of that list drops the arm below the flattener, which
    would then silently take the borders and move two committed dark baselines
    for a product change that alters no rendered value.

    The hook exists so the flattener can withhold exactly those two properties
    from exactly that element. It is keyed on an attribute rather than a class
    because `test_visual_helper_uses_stable_hooks_not_presentation_classes`
    forbids presentation classes here — those are precisely what a CSS refactor
    churns — and rather than on the `aria-label`, which is user-facing copy that
    could be reworded, silently disabling the exclusion.

    Inert means inert: if any production stylesheet or script ever reads it, it
    stops being a test hook and starts being an undeclared styling contract.
    """
    # Jinja comments are stripped first: the comment above the hook names it, and
    # counting mentions rather than uses makes the "hook was deleted" red path
    # undetectable — removing the attribute would leave the comment behind and
    # the count unchanged.
    jinja_comment = re.compile(r"\{#.*?#\}", re.DOTALL)
    occurrences = {
        path.name: jinja_comment.sub("", path.read_text(encoding="utf-8")).count(
            "data-visual-preserve-border"
        )
        for path in sorted((ROOT / "templates").glob("*.html"))
    }
    total = sum(occurrences.values())
    assert total == 1, f"expected exactly one hook, found {total}: {occurrences}"
    assert occurrences["progression_plan.html"] == 1

    # Inert: no production CSS or JS may reference it.
    for directory, pattern in (("static/css", "*.css"), ("static/js", "*.js")):
        for path in (ROOT / directory).rglob(pattern):
            assert "data-visual-preserve-border" not in path.read_text(
                encoding="utf-8", errors="ignore"
            ), f"{path} references a test-only hook"

    helper = read("e2e/visual-helpers.ts")
    # The helper keys on the hook, and on nothing more fragile.
    assert ":where(:not([data-visual-preserve-border]))" in helper
    assert "Current progression goals" not in helper, "keyed on user-facing copy"

    # The exclusion is scoped to border geometry only. The flattening set must
    # keep matching every surface, or the whole determinism layer weakens.
    flatten, _, border = helper.partition(
        "html[data-theme='dark'] [data-visual-surface][data-visual-surface]:where(:not([data-visual-preserve-border]))"
    )
    assert border, "border-geometry rule missing"
    border_block = border[: border.index("}")]
    assert "border-color" in border_block and "border-radius" in border_block
    for owned_by_the_flattener in ("background", "box-shadow", "text-shadow"):
        assert owned_by_the_flattener not in border_block, (
            f"{owned_by_the_flattener} must stay on the unexcluded flattening rule"
        )
    assert (
        "html[data-theme='dark'] [data-visual-surface][data-visual-surface] {" in flatten
    ), "the unexcluded flattening rule was narrowed"


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
