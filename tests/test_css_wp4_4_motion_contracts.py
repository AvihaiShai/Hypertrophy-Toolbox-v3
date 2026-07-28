"""WP4.4-c contracts — `static/css/motion.css` after the dead-paint deletion.

Per-packet contract file (owner ruling N1). Owned by packet **c** alone.

WP4.4-c deleted exactly three declarations, all from `.is-success`, all proven
non-winners on the only element that ever carries that class. Everything else in
`motion.css` was measured and retained, so this file pins both halves: what went,
and what may not go with it.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOTION = (ROOT / "static" / "css" / "motion.css").read_text(encoding="utf-8")


def _rule_body(selector: str, css: str = MOTION) -> str:
    """Return the declaration block for a top-level rule, by exact selector."""
    match = re.search(
        rf"(?m)^{re.escape(selector)}\s*\{{(.*?)\n\}}", css, re.DOTALL
    )
    assert match, f"rule {selector!r} not found in motion.css"
    return match.group(1)


def test_is_success_keeps_only_the_declaration_that_wins() -> None:
    """The three deleted declarations never rendered; the animation always did.

    `.is-success` is added by `workout-plan-add-exercise.js:275-278` to
    `#add_exercise_btn` and to nothing else. On that element, in both themes,
    adding the class moved `animation-name` and `animation-duration` but left
    `background-color`, `color` and all four `border-*-color` byte-identical —
    they were beaten by `!important` rules at higher specificity. Deleting a
    non-winner cannot change a computed value (M8).
    """
    body = _rule_body(".is-success")

    assert "animation: success-pulse 1s var(--ease-out, ease) !important;" in body

    for deleted in ("background-color", "border-color", "color:"):
        assert deleted not in body, f"{deleted} was proven dead and must stay deleted"

    # Exactly one declaration remains.
    declarations = [line for line in body.split(";") if line.strip()]
    assert len(declarations) == 1, declarations


def test_success_pulse_keyframes_are_retained() -> None:
    """The animation is the half of `.is-success` that renders.

    It draws the green pulse ring through `box-shadow`. Deleting the fill
    colours must not be read as a licence to delete the effect itself.
    """
    assert "@keyframes success-pulse {" in MOTION
    assert MOTION.count("success-pulse") == 2  # the keyframes plus its one use


def test_reduced_motion_suppression_is_intact() -> None:
    """The accessibility guarantee, and the highest-impact rule in the file.

    Measured winner on **17,194** element-matches for the animation longhands
    and **16,651** for the transition longhands across the 11 rendered routes in
    both themes. It is also what makes `body > .container-fluid.mt-4` stop
    animating under `prefers-reduced-motion: reduce` — the M11 capture proved
    that rule loses to this one, which is the intended behaviour.
    """
    assert "@media (prefers-reduced-motion: reduce) {" in MOTION

    block = re.search(
        r"@media \(prefers-reduced-motion: reduce\) \{(.*?)\n\}", MOTION, re.DOTALL
    )
    assert block, "reduced-motion block missing"
    assert "animation: none !important;" in block.group(1)
    assert "transition: none !important;" in block.group(1)
    assert "*," in block.group(1)
    assert "*::before," in block.group(1)
    assert "*::after" in block.group(1)


def test_page_enter_and_skeleton_families_are_retained() -> None:
    """Everything else in the file was measured live and stays.

    `page-enter` wins on the main wrapper on all 11 routes under
    `no-preference`. The `.skeleton` families are JS-inserted loading
    placeholders (M10) and win under that state, including the dark override.
    """
    assert "@keyframes page-enter {" in MOTION
    assert "body > .container-fluid.mt-4 {" in MOTION
    assert "animation: page-enter var(--dur-slow, 360ms)" in MOTION

    assert "@keyframes skeleton-shimmer {" in MOTION
    assert re.search(r"(?m)^\.skeleton \{", MOTION)
    assert '[data-theme="dark"] .skeleton {' in MOTION

    # The dark override re-declares `background`, which resets `background-size`
    # to its initial value — so the repeat is required, not redundant.
    dark = _rule_body('[data-theme="dark"] .skeleton')
    assert "background:" in dark
    assert "background-size: 200% 100%;" in dark


def test_motion_css_declares_no_layer() -> None:
    """N2 freezes `@layer` membership arc-wide.

    `motion.css` is entirely unlayered, which is what lets the packet's
    ownership reasoning use plain specificity ordering.
    """
    assert "@layer" not in MOTION
