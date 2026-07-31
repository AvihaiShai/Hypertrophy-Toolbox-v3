"""WP4.4-j contracts for ``static/css/theme-dark.css``.

Packet-owned per N1. j is **preservation-only** under continuation ruling C11:
the file stays linked and nonempty, custom properties and ``.value-changed`` are
retained, reduced-motion behaviour is preserved, and the deferred superset tint
is not added as a back door. These tests pin each of those, plus the specific
removals the packet certified, so a later packet cannot quietly undo them or
extend the deletion past what was proven.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "static" / "css" / "theme-dark.css"
BASE_HTML = ROOT / "templates" / "base.html"


def _css() -> str:
    return CSS_PATH.read_text(encoding="utf-8")


def _strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def test_theme_dark_is_still_linked_and_nonempty() -> None:
    """R4 forbids unlinking the file, and an empty linked bundle is worse than a
    small justified one. Both halves of that are asserted here because deleting
    the last rule and deleting the ``<link>`` are the two ways to violate it."""
    assert "css/theme-dark.css" in BASE_HTML.read_text(encoding="utf-8")
    body = _strip_comments(_css()).strip()
    assert body, "theme-dark.css is empty; R4 requires a linked, nonempty bundle"
    assert body.count("{") >= 50


def test_every_custom_property_declaration_survives() -> None:
    """M9: no packet may delete a custom-property declaration under the
    non-winner rule. A ``var()`` consumer in any of the other twenty
    hand-maintained sources keeps them live, and proving otherwise needs a
    dependency graph rather than an ownership sweep. The count is pinned rather
    than a floor so an accidental *addition* is caught too."""
    declarations = re.findall(r"^\s*(--[A-Za-z0-9-]+)\s*:", _css(), flags=re.MULTILINE)
    assert len(declarations) == 34, f"expected 34 custom-property declarations, found {len(declarations)}"


def test_the_reduced_motion_block_is_preserved() -> None:
    """C11 retains reduced-motion behaviour. The block is the only at-rule in the
    file, so losing it would be invisible in a rule count."""
    css = _strip_comments(_css())
    assert css.count("@media") == 1
    assert "prefers-reduced-motion: reduce" in css
    block = css.split("@media", 1)[1]
    assert "value-changed" in block, "the reduced-motion block no longer covers .value-changed"


def test_value_changed_rules_are_retained() -> None:
    """C11 names ``.value-changed`` explicitly: it is JS-applied state (M10), so a
    rest-state sweep sees it as unmatched and would nominate it as dead."""
    css = _strip_comments(_css())
    assert css.count(".value-changed") >= 7


def test_the_deferred_superset_tint_was_not_added() -> None:
    """G4 defers the superset dark-tint gap. C11 forbids adding a dark override
    for ``--superset-bg-1..4`` here as a back door to closing it."""
    assert "superset" not in _css().lower()


def test_the_certified_removals_stay_removed() -> None:
    """The 25 declarations j deleted were dead by intra-file shadowing under
    identical selector text. Re-adding any of them would restore a declaration
    proven unable to win, so the shadowing pairs are pinned by their surviving
    winner: each selector below must declare the longhand exactly once."""
    css = _strip_comments(_css())
    for selector, prop in [
        (':where([data-theme="dark"] #results-body)', "background-color"),
        (':where([data-theme="dark"] #results-body tr)', "background-color"),
        (':where([data-theme="dark"] #results-body td)', "color"),
        (':where([data-theme="dark"] .table-responsive .table)', "color"),
    ]:
        blocks = [
            body for head, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css)
            if selector in head
        ]
        occurrences = sum(len(re.findall(rf"^\s*{re.escape(prop)}\s*:", b, flags=re.MULTILINE)) for b in blocks)
        assert occurrences <= 1, (
            f"{selector} declares {prop} {occurrences} times; the duplicate generation "
            "WP4.4-j certified as shadowed has come back"
        )


def test_the_file_declares_no_layer() -> None:
    """The shadow certification reduces the in-file cascade to importance then
    document order. That argument only holds while the file is unlayered, so the
    assumption is pinned rather than left as a comment in the tool."""
    assert "@layer" not in _strip_comments(_css())
