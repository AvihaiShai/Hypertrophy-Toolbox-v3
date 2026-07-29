"""WP4.4-d1 cascade contracts for `static/css/a11y.css`.

d1 deleted a superseded generation of the scale / accessibility-menu UI. These
contracts lock the premises that deletion rested on, and -- just as importantly
-- lock the d1/d2 boundary and the accessibility guarantees d1 was required to
preserve.

Packet-owned. This file never edits, and must not be confused with, the shared
`tests/test_css_cascade_contracts.py`, which d1 runs but does not touch
(Plan v2 section 4d -- only packet i may amend that file).

Every assertion here has a demonstrated red path; see
docs/CSS_PHASE4_WP4_4_D1_A11Y_EVIDENCE.md.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
A11Y = ROOT / "static" / "css" / "a11y.css"
TEMPLATES = ROOT / "templates"
JS = ROOT / "static" / "js"


def _css() -> str:
    return A11Y.read_text(encoding="utf-8")


def _strip_comments(css: str) -> str:
    """Blank comments while preserving BOTH length and line structure.

    Replacing a comment with `" " * len(...)` is length-preserving in characters
    but destroys the newlines inside multi-line comments, so any line number
    computed from the result is wrong -- it under-counts by one per commented
    newline. Measured on this file: the retained print rule sits at source line
    328, and the naive blanker placed it at 304.

    Nothing here does line arithmetic today, but a stripper that silently
    corrupts it is the exact hazard `.claude/rules/verification.md` calls out.
    """
    return re.sub(
        r"/\*.*?\*/",
        lambda m: "".join(c if c == "\n" else " " for c in m.group(0)),
        css,
        flags=re.S,
    )


# The legacy generation d1 deleted. Runtime census was 0 for every one of these
# across 11 routes x 2 themes x 10 widths x 8 data-scale levels, plus print and
# reduced-motion, and every deleted rule was visible to the synthetic oracle
# before deletion.
LEGACY_CLASSES = (
    "scale-control-label",
    "scale-btn-group",
    "accessibility-menu",
    "accessibility-section",
    "accessibility-section-title",
    "scale-labels",
    "scale-label",
)

# The generation that IS live -- present in templates/base.html:190-202 and
# census > 0 in 160/160 measured contexts. d1 must not have touched these, and
# they are what makes the deletion safe rather than merely quiet.
LIVE_GENERATION = {
    "scale-control-compact": 5,
    "scale-btn-compact": 6,
    "scale-indicator": 2,
}


def test_legacy_scale_and_menu_generation_stays_deleted() -> None:
    """No rule targets the superseded generation.

    Red path: restoring any deleted block reintroduces its selector.
    """
    css = _strip_comments(_css())
    offenders = [c for c in LEGACY_CLASSES if re.search(rf"\.{re.escape(c)}(?![\w-])", css)]
    assert offenders == [], (
        f"a11y.css again styles the superseded generation: {offenders}. If one "
        "became reachable, re-run the census -- do not simply re-add the rule."
    )


def test_legacy_classes_are_still_unreachable() -> None:
    """Nothing in the app applies the deleted classes.

    This is the premise the deletion rests on, turned into a gate. It is the
    reason a JavaScript *query* was never accepted as proof of reachability:
    `accessibility.js` queries `.accessibility-dropdown` and
    `.scale-btn[data-scale]`, and both resolve to empty sets at runtime.

    Red path: adding `class="accessibility-menu"` to a template, or
    `classList.add('scale-labels')` to a JS module, fails this test.
    """
    class_attr = re.compile(r"""class\s*=\s*["']([^"']*)["']""")
    add_call = re.compile(r"""classList\.(?:add|toggle|replace)\(\s*["']([\w-]+)["']""")

    offenders: list[str] = []
    for base, pattern in ((TEMPLATES, "**/*.html"), (JS, "**/*.js")):
        for path in base.glob(pattern):
            text = path.read_text(encoding="utf-8", errors="replace")
            applied: set[str] = set()
            for m in class_attr.finditer(text):
                applied.update(m.group(1).split())
            applied.update(add_call.findall(text))
            for cls in LEGACY_CLASSES:
                if cls in applied:
                    offenders.append(f"{path.relative_to(ROOT)} applies .{cls}")

    assert offenders == [], "a deleted a11y.css class is applied again: " + "; ".join(offenders)


def test_live_compact_generation_is_untouched() -> None:
    """The generation the app actually renders survives d1 intact.

    This is the known-live control that validated the whole oracle: if these
    were not visible, no deletion claim from the run would have counted.

    Red path: deleting any `.scale-btn-compact` rule fails on the count.
    """
    css = _strip_comments(_css())
    wrong = {}
    for cls, expected in LIVE_GENERATION.items():
        found = len(re.findall(rf"\.{re.escape(cls)}(?![\w-])", css))
        if found != expected:
            wrong[cls] = f"{found} (expected {expected})"
    assert wrong == {}, f"the live compact scale generation changed: {wrong}"


def test_live_compact_generation_is_still_rendered() -> None:
    """base.html still emits the live generation d1 preserved.

    Red path: removing `scale-control-compact` from base.html fails this test,
    which is what makes the previous test meaningful rather than circular.
    """
    base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
    for cls in LIVE_GENERATION:
        assert cls in base, (
            f"templates/base.html no longer renders .{cls}; the a11y.css rules "
            "d1 preserved for it would now be unreachable and must be re-audited"
        )
    assert "data-visual-scale-control" in base, (
        "base.html lost data-visual-scale-control, the registered visual "
        "blind-spot hook the d1 oracle used as a known-live control"
    )


def test_deleted_scale_control_rules_stay_deleted_by_source_shape() -> None:
    """`.scale-control` needs a SOURCE-SHAPE assertion, not a presence check.

    Two `.scale-control` rules were deleted (former lines 126 and 387), but the
    selector text legitimately survives inside the retained `@media print` rule
    `.scale-control, .accessibility-dropdown`. So "is `.scale-control` absent?"
    is the wrong question -- it would fail on the retained rule -- and "is it
    present?" is satisfied by the retained rule even if a deleted block came
    back. Neither separates the two claims.

    What distinguishes them is the RULE SHAPE: `.scale-control` may appear
    exactly once, and only as part of a multi-selector list that also names
    `.accessibility-dropdown`. A restored standalone `.scale-control { ... }`
    block violates that immediately.

    Red path: appending `.scale-control { display: flex; }` fails here.
    """
    css = _strip_comments(_css())

    occurrences = re.findall(r"\.scale-control(?![\w-])", css)
    assert len(occurrences) == 1, (
        f".scale-control appears {len(occurrences)} times in a11y.css, expected "
        "exactly 1 (the retained @media print mixed rule). A deleted standalone "
        "block may have been restored."
    )

    # The single occurrence must be a member of the retained mixed selector list,
    # never the sole subject of its own rule.
    # NB: the hyphen must be LAST inside the class -- `[\w-,]` is parsed as a
    # range from \w to ',' and raises re.PatternError.
    standalone = re.search(r"(?<![\w,-])\.scale-control(?![\w-])\s*\{", css)
    assert standalone is None, (
        "a standalone `.scale-control { ... }` rule exists again; the only "
        "permitted occurrence is inside the retained "
        "`.scale-control, .accessibility-dropdown` print rule"
    )


def test_mixed_selector_lists_kept_their_dead_branch() -> None:
    """A rule mixing a dead branch with a non-candidate branch survives whole.

    `.scale-control, .accessibility-dropdown { display: none !important }` --
    `.accessibility-dropdown` was never audited as a d1 candidate, so trimming
    `.scale-control` out would be re-weighting a rule this packet did not prove.
    That is d2's work, not d1's.

    Red path: trimming `.scale-control,` from that rule fails this test.
    """
    css = _strip_comments(_css())
    assert re.search(r"\.scale-control\s*,\s*\.accessibility-dropdown\s*\{", css), (
        "the mixed `.scale-control, .accessibility-dropdown` rule lost a branch; "
        "d1 is pure deletion and may not trim live-or-unaudited selector lists"
    )


def test_d1_removed_no_important_declaration() -> None:
    """The d1/d2 boundary, expressed as a count.

    Every one of the 14 deleted rules contained zero `!important`, so d1
    removed none. All 51 remain in retained rules. Re-weighting is d2's.

    Red path: deleting any `!important` declaration from a retained rule, or
    deleting a retained rule that carries one, fails this test.
    """
    assert _strip_comments(_css()).count("!important") == 51, (
        "a11y.css !important count moved. d1 is pure deletion and must not "
        "re-weight: dropping !important from a retained declaration belongs to d2."
    )


def test_focus_visible_contract_premise_is_preserved() -> None:
    """The contract-pinned `*:focus-visible,` premise survives d1.

    `tests/test_css_cascade_contracts.py` pins this string against a11y.css.
    d1 runs that shared contract but never edits it; this asserts the source
    side of the same premise so a d1-shaped edit cannot silently break it.

    Red path: deleting the `*:focus-visible,` selector fails this test.
    """
    css = _css()
    # Anchored to line start on purpose. A plain `"*:focus-visible," in css`
    # substring check is satisfied by the per-scale rules -- every
    # `html[data-scale="1"] *:focus-visible,` line CONTAINS that substring -- so
    # deleting the bare global selector would leave the test green. The red-path
    # proof caught exactly that.
    assert re.search(r"^\*:focus-visible,", css, flags=re.M), (
        "a11y.css lost the contract-pinned bare `*:focus-visible,` selector "
        "(the per-scale rules do not substitute for it)"
    )
    # The per-scale focus ladder covers data-scale 1..5 ONLY, and did so before
    # d1 as well -- scales 6..8 declare --ui-scale tokens and inherit the global
    # `*:focus-visible` rule instead. Asserting 1..8 here would be asserting a
    # premise that was never true; the pre-deletion comparison caught exactly
    # that. d1 deleted none of this ladder.
    missing = [
        n for n in range(1, 6)
        if f'html[data-scale="{n}"] *:focus-visible' not in css
    ]
    assert missing == [], (
        f"the per-scale focus-visible ladder is gone for data-scale {missing}"
    )


def test_every_targeted_data_scale_level_still_has_rules() -> None:
    """a11y.css targets data-scale 1..8; d1 deleted none of that ladder.

    Red path: deleting the `[data-scale="6"]` block fails this test.
    """
    css = _strip_comments(_css())
    missing = [n for n in range(1, 9) if f'[data-scale="{n}"]' not in css]
    assert missing == [], f"a11y.css no longer targets data-scale levels {missing}"


def test_a11y_css_declares_no_cascade_layer() -> None:
    """N2 freezes @layer membership arc-wide; a11y.css had zero and keeps zero.

    Red path: wrapping any rule in `@layer navbar { ... }` fails.
    """
    assert "@layer" not in _strip_comments(_css()), (
        "a11y.css now declares an @layer; N2 freezes layer membership for the arc"
    )


def test_no_custom_property_was_deleted() -> None:
    """d1 deleted no custom property (M9).

    The 14 deleted rules declared none. Custom properties are never deleted
    under the ordinary non-winner rule, because a `var()` in another bundle may
    be their only consumer.

    Red path: deleting a `--` declaration from a retained rule fails this test.
    """
    decls = re.findall(r"(?<![\w-])--[\w-]+\s*:", _strip_comments(_css()))
    assert len(decls) == 17, (
        f"a11y.css custom-property declaration count is {len(decls)}, expected 17; "
        "d1 deleted none and must not."
    )


@pytest.mark.parametrize(
    "surface", ["layout.css", "components.css", "navbar.css", "theme-dark.css", "base.css"]
)
def test_legacy_generation_is_not_resurrected_by_a_sibling_surface(surface: str) -> None:
    """No sibling bundle may start styling the generation a11y.css dropped.

    Red path: adding `.accessibility-menu {}` to components.css fails.
    """
    path = ROOT / "static" / "css" / surface
    if not path.exists():
        pytest.skip(f"{surface} not present")
    css = _strip_comments(path.read_text(encoding="utf-8"))
    offenders = [c for c in LEGACY_CLASSES if re.search(rf"\.{re.escape(c)}(?![\w-])", css)]
    assert offenders == [], (
        f"{surface} now styles the generation WP4.4-d1 deleted: {offenders}"
    )
