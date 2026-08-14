"""Contracts for the `.theme-animating` transition suppression.

Register row X6 (`docs/testing_phase2/A11Y_EXCEPTIONS.md`). `darkMode.js` adds
`.theme-animating` to `<html>` for the two frames around a theme toggle so the
swap is instant. The CSS half of that mechanism was deleted from the retired
`static/css/styles.css` by `ee82643` ("chore(redesign): P10 remove legacy CSS
sources") while the JS was left untouched, so for four months the class was
applied to nothing and the toggle cross-faded against `theme-dark.css`'s
unconditional `transition: all 0.3s`.

The failure mode was a **pair drifting apart**, so both halves are pinned here.
A contract that pinned only the stylesheet would have been satisfied by deleting
the JS, and one that pinned only the JS is what already failed.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOTION = (ROOT / "static" / "css" / "motion.css").read_text(encoding="utf-8")
DARK_MODE_JS = (ROOT / "static" / "js" / "darkMode.js").read_text(encoding="utf-8")


def _theme_animating_rule() -> str:
    """Return the declaration block of the suppression rule."""
    match = re.search(
        r"(?ms)^html\.theme-animating,\s*\n"
        r"html\.theme-animating \*,\s*\n"
        r"html\.theme-animating \*::before,\s*\n"
        r"html\.theme-animating \*::after \{(.*?)\n\}",
        MOTION,
    )
    assert match, (
        "motion.css no longer carries the four-branch `html.theme-animating` "
        "rule. Deleting it re-creates the ee82643 regression: darkMode.js keeps "
        "applying a class that matches nothing."
    )
    return match.group(1)


def test_the_suppression_rule_covers_elements_and_both_pseudo_elements() -> None:
    """A bare `html.theme-animating` would suppress nothing that transitions.

    The transitions this exists to defeat are declared on descendants — body,
    .navbar, .card, .table, .form-control, .btn in theme-dark.css — not on the
    root, so the descendant and pseudo-element branches are the load-bearing
    ones, not decoration.
    """
    _theme_animating_rule()


def test_the_rule_suppresses_both_transition_and_animation() -> None:
    """`!important` is required, not stylistic.

    `theme-dark.css` declares `transition: all 0.2s ease !important` on dark
    form controls, so an unweighted suppression loses to it on exactly the
    elements a theme switch repaints.
    """
    body = _theme_animating_rule()

    assert "transition: none !important;" in body
    assert "animation: none !important;" in body


def test_darkmode_js_still_applies_the_class() -> None:
    """The JS half. Without it the stylesheet rule is the dead one instead."""
    assert "classList.add('theme-animating')" in DARK_MODE_JS
    assert "classList.remove('theme-animating')" in DARK_MODE_JS


def test_no_other_runtime_bundle_claims_the_class() -> None:
    """One owner. A second definition would reintroduce the ordering question
    that made the original deletion invisible."""
    others = sorted(
        path.name
        for path in (ROOT / "static" / "css").glob("*.css")
        if path.name != "motion.css"
        and "theme-animating" in path.read_text(encoding="utf-8")
    )
    assert others == [], f"theme-animating is also styled in: {others}"
