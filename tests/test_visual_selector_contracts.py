import hashlib
import re
from html.parser import HTMLParser
from pathlib import Path


import pytest


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_template_icon_names_are_defined_in_bundled_fontawesome():
    font = read("static/vendor/fontawesome/css/all.min.css")
    glyphs = set(re.findall(r"\.(fa-[\w-]+):before\b", font))
    for page in ("workout_plan", "user_profile", "body_composition"):
        template = read(f"templates/{page}.html")
        for classes in re.findall(r'<i\b[^>]*\bclass="([^"]+)"', template):
            names = set(classes.split())
            if "fas" in names and "{" not in classes:
                assert names & glyphs, f"{page}: missing bundled glyph for {classes}"


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

    assert "--nav-icon-accent" not in nav_spec
    assert "data-visual-icon" in nav_spec
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

# The cmap indices were read directly from this bundled WOFF2's format-4 cmap.
# Its digest binds that offline verification to the exact font served in CI.
SOLID_FONT_SHA256 = "9834b82ad26e2a37583d22676a12dd2eb0fe7c80356a2114d0db1aa8b3899537"
# DOM id, destination, accessible text, Free Solid name, CSS codepoint, glyph index
NAVIGATION = (
    ("nav-brand", "/", "Hypertrophy Toolbox", "dumbbell", "f44b", 523),
    ("nav-workout-plan", "/workout_plan", "Plan", "tasks", "f0ae", 170),
    ("nav-workout-log", "/workout_log", "Log", "book-open", "f518", 610),
    ("nav-analyze-toggle", "#", "Analyze", "chart-line", "f201", 358),
    ("nav-weekly-summary", "/weekly_summary", "Weekly", "calendar-week", "f784", 916),
    ("nav-session-summary", "/session_summary", "Session", "calendar-day", "f783", 915),
    ("nav-fatigue", "/fatigue", "Fatigue", "battery-half", "f242", 393),
    ("nav-progression-plan", "/progression", "Progress", "level-up-alt", "f3bf", 495),
    ("nav-user-profile", "/user_profile", "Profile", "user-circle", "f2bd", 446),
    ("nav-body-composition", "/body_composition", "Body Composition", "ruler", "f545", 655),
    ("nav-volume-splitter", "/volume_splitter", "Distribute", "sliders-h", "f1de", 338),
    ("nav-backup", "/backup", "Backup", "folder-open", "f07c", 141),
)


class NavbarParser(HTMLParser):
    """Read anchor order, attributes and label from the original Flask response."""

    def __init__(self):
        super().__init__()
        self.in_header = False
        self.current = None
        self.links = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "header" and attrs.get("id") == "navbar":
            self.in_header = True
        if self.in_header and tag in ("a", "button") and attrs.get("id", "").startswith("nav-"):
            self.current = attrs["id"]
            assert self.current not in self.links
            self.links[self.current] = (attrs, [])

    def handle_endtag(self, tag):
        if tag in ("a", "button"):
            self.current = None
        if tag == "header":
            self.in_header = False

    def handle_data(self, data):
        if self.current:
            self.links[self.current][1].append(data)


@pytest.mark.parametrize("page_id,path", [(r[0], r[1]) for r in NAVIGATION if r[1] != "#"])
def test_navigation_server_marks_only_current_destination(client, page_id, path):
    for url in dict.fromkeys([path, path.rstrip("/") + "/", path + "?x=1", path.rstrip("/") + "/?x=1"]):
        response = client.get(url)
        assert response.status_code == 200, url
        nav = NavbarParser()
        nav.feed(response.get_data(as_text=True))
        assert list(nav.links) == [r[0] for r in NAVIGATION], url
        for ident, href, name, *_ in NAVIGATION:
            attrs, text = nav.links[ident]
            if ident != "nav-analyze-toggle":
                assert attrs["href"] == href
                assert attrs["data-testid"] == ident
            else:
                assert attrs["data-bs-toggle"] == "dropdown"
                assert attrs["aria-expanded"] == "false"
            assert " ".join(" ".join(text).split()) == name
            assert attrs.get("aria-current") == ("page" if ident == page_id else None), (url, ident)
            selected_group = ident == "nav-analyze-toggle" and path in ("/weekly_summary", "/session_summary", "/fatigue")
            assert ("active" in attrs["class"].split()) == (ident == page_id or selected_group), (url, ident)


def test_navigation_glyphs_exist_in_the_bundled_free_solid_face():
    font = ROOT / "static/vendor/fontawesome/webfonts/fa-solid-900.woff2"
    assert hashlib.sha256(font.read_bytes()).hexdigest() == SOLID_FONT_SHA256
    css = read("static/vendor/fontawesome/css/all.min.css")
    for _, _, _, glyph, codepoint, cmap_index in NAVIGATION:
        assert re.search(rf'\.fa-{glyph}:before[^{{}}]*\{{content:"\\{codepoint}"', css)
        assert cmap_index > 0


def test_navigation_image_references_retired_and_files_retained():
    images = ("7-days.gif", "dividers.gif", "icons8-bench-press.gif", "icons8-growth.gif",
              "icons8-to-do.gif", "notebook.gif", "icons8-session-50.png")
    templates = list((ROOT / "templates").rglob("*.html"))
    for image in images:
        assert (ROOT / "static/images" / image).is_file()
        assert not [p for p in templates if image in p.read_text(encoding="utf-8")], image
    assert "static/images/icons8-session-50.png" in read("tests/test_package_asset_staging.py")
