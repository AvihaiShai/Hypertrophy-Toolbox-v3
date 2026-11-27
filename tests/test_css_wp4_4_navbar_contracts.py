"""Navigation cascade contracts and the preserved WP4.4-f1 deletion premise.

The #736 Navigation redesign replaced the f2 layout and paint rules. Selector
and at-rule checks bind their live successors. The nav-dropdown browser suite
checks actual fixed-header clearance, scrollability, focus and utility behavior.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

import pytest

ROOT = Path(__file__).resolve().parents[1]
NAVBAR = ROOT / "static" / "css" / "navbar.css"
TEMPLATES = ROOT / "templates"


def _css() -> str:
    return NAVBAR.read_text(encoding="utf-8").replace("\r\n", "\n")


def _strip_comments(css: str) -> str:
    """Preserve offsets and line numbers."""
    return re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), css, flags=re.S)


def _rules(css: str) -> list[dict]:
    """Every style rule as (selector, line, declarations), @keyframes excluded.

    Rule identity is selector + source line. Never re-serialized text: that is
    not byte-preserving and would make the source-shape assertions meaningless.
    """
    text = _strip_comments(css)
    out: list[dict] = []
    at_stack: list[str] = []
    i, n, start = 0, len(text), 0
    while i < n:
        ch = text[i]
        if ch == "{":
            prelude = " ".join(text[start:i].split())
            if prelude.startswith("@"):
                at_stack.append(prelude)
                i += 1
                start = i
                continue
            depth, j = 1, i + 1
            while j < n and depth:
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                j += 1
            if not any(a.startswith("@keyframes") for a in at_stack):
                out.append(
                    {
                        "selector": prelude,
                        "line": css[:i].count("\n") + 1 - prelude.count("\n"),
                        "decls": [
                            d.strip()
                            for d in text[i + 1 : j - 1].split(";")
                            if d.strip() and ":" in d
                        ],
                        "at_rules": tuple(at_stack),
                        "layer": next((a for a in at_stack if a.startswith("@layer")), None),
                    }
                )
            i, start = j, j
            continue
        if ch == "}":
            if at_stack:
                at_stack.pop()
            i += 1
            start = i
            continue
        i += 1
    return out


# --------------------------------------------------------------------------
# The deletion
# --------------------------------------------------------------------------

# The one rule WP4.4-f1 deleted. It was unreachable by construction, not merely
# by census: navbar.css is linked only from templates/base.html, and that
# template renders <header id="navbar"> unconditionally, so a document that
# loads this stylesheet always contains #navbar and `body:not(:has(#navbar))`
# can never be satisfied. The runtime census agreed at 0/522 contexts.
DELETED_SELECTOR = "body:not(:has(#navbar)) .navbar"
DELETED_DECLS = ("background-color: #212529", "height: 40px")


def test_the_unreachable_legacy_rule_stays_deleted() -> None:
    """Occurrence count, not substring: `.navbar` survives in a retained rule."""
    selectors = [r["selector"] for r in _rules(_css())]
    assert selectors.count(DELETED_SELECTOR) == 0


def test_the_deleted_guard_compound_appears_nowhere() -> None:
    """`:not(:has(#navbar))` was unique to the deleted rule."""
    assert _strip_comments(_css()).count(":not(:has(#navbar))") == 0


def test_no_rule_reintroduces_the_deleted_declarations_under_a_navbar_guard() -> None:
    """A restore under a renamed selector is still a restore."""
    for rule in _rules(_css()):
        if ":has(#navbar)" not in rule["selector"]:
            continue
        joined = " ".join(rule["decls"])
        for decl in DELETED_DECLS:
            assert decl not in joined, f"{rule['selector']} at line {rule['line']}"


# --------------------------------------------------------------------------
# Live Navigation layout and paint
# --------------------------------------------------------------------------


def test_fixed_header_geometry_has_one_owner() -> None:
    matches = [rule for rule in _rules(_css()) if rule["selector"] == "#navbar"]
    assert len(matches) == 1
    assert {"position: fixed", "inset: 0 0 auto", "z-index: 1000"} <= set(matches[0]["decls"])


def test_fixed_header_geometry_stays_unlayered() -> None:
    """Bootstrap's navbar rules are unlayered."""
    matches = [rule for rule in _rules(_css()) if rule["selector"] == "#navbar"]
    assert len(matches) == 1
    assert matches[0]["at_rules"] == ()


@pytest.mark.parametrize(
    "selector,declaration",
    [
        (":root", "--nav-height: 64px"),
        ("#navbar", "background: var(--surface-2)"),
        ("#navbar > .container-fluid", "padding: 0 var(--ui-gutter)"),
    ],
)
def test_header_uses_shared_frame_values(selector: str, declaration: str) -> None:
    rules = [rule for rule in _rules(_css()) if rule["selector"] == selector]
    assert sum(declaration in rule["decls"] for rule in rules) == 1


def test_the_single_sourced_navbar_layer_block_survives() -> None:
    """G11 binds the name and global order of the navbar layer."""
    assert re.search(r"@layer\s+navbar\s*\{", _strip_comments(_css()))


def test_mobile_panel_owns_scrolling_from_header_edge_to_viewport_bottom() -> None:
    """The same placement applies as the header compacts."""
    rules = _rules(_css())
    mobile = ("@media (max-width: 1359.98px)",)
    [panel] = [
        rule for rule in rules
        if rule["selector"] == ".navbar .navbar-collapse" and rule["at_rules"] == mobile
    ]
    assert {
        "position: absolute",
        "inset: calc(100% + 1px) 0 auto",
        "max-height: calc(100dvh - 100% - 1px)",
        "overscroll-behavior: contain",
    } <= set(panel["decls"])
    [opened] = [
        rule for rule in rules
        if rule["selector"] == ".navbar .navbar-collapse.show" and rule["at_rules"] == mobile
    ]
    assert {"height: calc(100dvh - 100% - 1px)", "overflow-y: auto"} <= set(opened["decls"])
    for rule in rules:
        if rule["selector"] == "#navbar":
            assert all(
                not decl.startswith(("-ms-overflow-style:", "scrollbar-width:", "overflow"))
                for decl in rule["decls"]
            )


def test_theme_toggle_uses_inherited_ink_and_keeps_its_utility_glyph() -> None:
    """Current-page decoration stays on active destinations."""
    rules = _rules(_css())
    assert not any(
        "#darkModeToggle" in rule["selector"] and "::before" in rule["selector"]
        for rule in rules
    )
    icon_rules = [
        rule for rule in rules
        if ".navbar .nav-utilities i" in rule["selector"].split(", ")
    ]
    assert len(icon_rules) == 1
    assert {"color: inherit", "font-size: 1em"} <= set(icon_rules[0]["decls"])

    base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
    toggle = re.search(r'<button[^>]+id="darkModeToggle"[^>]*>(.*?)</button>', base, re.S)
    assert toggle is not None
    assert 'class="fas fa-moon"' in toggle[1]
    assert "Dark Mode" in toggle[1]
    script = (ROOT / "static" / "js" / "darkMode.js").read_text(encoding="utf-8")
    assert "classList.add('fa-sun')" in script
    assert "classList.add('fa-moon')" in script
    assert "this.darkModeToggle.classList." not in script


def test_shared_container_owns_regular_and_compact_frame_geometry() -> None:
    rules = _rules(_css())
    assert not any(rule["selector"] == ":where(#navbar) > .container-fluid" for rule in rules)
    [regular] = [
        rule for rule in rules if rule["selector"] == "#navbar > .container-fluid"
        and not rule["at_rules"]
    ]
    assert {
        "position: static",
        "flex-wrap: nowrap",
        "min-height: calc(var(--nav-height) - 1px)",
        "padding: 0 var(--ui-gutter)",
    } <= set(regular["decls"])
    [compact] = [
        rule for rule in rules if rule["selector"] == "#navbar.nb-compact > .container-fluid"
        and not rule["at_rules"]
    ]
    assert "min-height: 51px" in compact["decls"]


# --------------------------------------------------------------------------
# Whole-surface invariants
# --------------------------------------------------------------------------


def test_navbar_adds_no_important_declarations() -> None:
    assert not re.search(r"!\s*important", _strip_comments(_css()), re.I)


def test_navbar_custom_property_count_matches_contract() -> None:
    decls = [d for r in _rules(_css()) for d in r["decls"] if d.lstrip().startswith("--")]
    assert len(decls) == 5
    assert not any(re.match(r"--nav-(?:gap|padding-[xy])\s*:", decl) for decl in decls)


def test_the_navbar_layer_contains_only_frame_and_theme_tokens() -> None:
    css = _strip_comments(_css())
    assert len(re.findall(r"@layer\s+[\w-]+\s*\{", css)) == 1
    layered = [rule for rule in _rules(css) if rule["layer"]]
    assert [rule["selector"] for rule in layered] == [
        ":root", ".navbar", '[data-theme="dark"] .navbar',
    ]
    assert all(rule["at_rules"] == ("@layer navbar",) for rule in layered)
    assert all(decl.startswith("--") for rule in layered for decl in rule["decls"])


def test_navbar_rule_count_matches_contract() -> None:
    rules = _rules(_css())
    assert len(rules) == 37
    assert sum(rule["layer"] is None for rule in rules) == 34


def test_compact_motion_uses_a_transition_and_respects_reduced_motion() -> None:
    css = _strip_comments(_css())
    assert not re.search(r"@keyframes\s+", css)
    selector = "#navbar > .container-fluid"
    transitions = [
        (rule["at_rules"], decl)
        for rule in _rules(css) if rule["selector"] == selector
        for decl in rule["decls"] if decl.startswith("transition:")
    ]
    assert transitions == [
        ((), "transition: min-height 150ms ease"),
        (("@media (prefers-reduced-motion: reduce)",), "transition: none"),
    ]


# --------------------------------------------------------------------------
# The premise that made the deletion safe
# --------------------------------------------------------------------------


def test_navbar_css_is_linked_only_from_base_html() -> None:
    linking = [
        p.name
        for p in TEMPLATES.rglob("*.html")
        if "css/navbar.css" in p.read_text(encoding="utf-8")
    ]
    assert linking == ["base.html"]


class NavbarDocument(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.headers = 0
        self.stylesheets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "header" and attributes.get("id") == "navbar":
            self.headers += 1
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.stylesheets.append(urlsplit(attributes.get("href") or "").path)


def test_base_html_renders_the_navbar_unconditionally(client) -> None:
    """Every destination that loads navbar.css renders exactly one header."""
    routes = (
        "/", "/workout_plan", "/workout_log", "/weekly_summary", "/session_summary",
        "/fatigue", "/progression", "/user_profile", "/body_composition",
        "/volume_splitter", "/backup",
    )
    for route in routes:
        response = client.get(route)
        assert response.status_code == 200, route
        document = NavbarDocument()
        document.feed(response.get_data(as_text=True))
        assert sum(path.endswith("/css/navbar.css") for path in document.stylesheets) == 1, route
        assert document.headers == 1, route
