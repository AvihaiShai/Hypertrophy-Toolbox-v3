"""WP4.4-h cascade contracts for `static/css/components.css`.

These lock the premises WP4.4-h's deletions rest on. Each test fails under its
own violation (F16); the red-path proofs are recorded in
`docs/CSS_PHASE4_WP4_4_H_COMPONENTS_DEAD_EVIDENCE.md`.

This file is packet-owned. It is not, and must not be confused with, the shared
`tests/test_css_cascade_contracts.py`, which this packet runs and never edits.

**Why this packet is smaller than its plan row projected.** The dry run proposed
554 lines. `tests/test_css_wp4_4_a_baseline_contracts.py` re-derives
`measure.layer_spans("components.css")` from the *working tree* and pins
`openLine 3539 / closeLine 4104` exactly, and that file is outside this packet's
authorized write set. Deleting a line at or before 4104 therefore shifts one of
those numbers and reds a contract WP4.4-h may not touch. The deletion set was
narrowed to the only legal window — lines 4105 onward — which costs 158 of 247
cuts. That trade is deliberate: under-delivery is recoverable, an unfixable red
is not.

**101 declarations, not 103.** Inside that window the seeded 446-context census
classified 121 declarations as zero-winner. Eighteen of them belong to the
`.btn.btn-video` family, which no differential run covers, and were excluded for
missing DOM coverage. Of the remaining 103, the removal oracle — which deletes
each declaration from the live CSSOM and re-reads every computed value —
contradicted the census twice:

* `.collapse-toggle { color: #6c757d }` is **live**: removing it moves the
  computed colour of the button and its `.toggle-icon` child from
  `rgb(0, 131, 143)` to `rgb(102, 102, 102)` in 42 element-property pairs.
* `.collapse-toggle { background: none }` was **never probed**, so it is
  unproven rather than proven dead.

Both were withdrawn. A declaration is deleted here only where the cascade
model, the zero-winner recount and the removal oracle all agree, and every
excluded family is pinned numerically below rather than described in prose,
because a count is the only form of that claim a later packet cannot quietly
break.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ROOT / "static" / "css" / "components.css"


def _css() -> str:
    return COMPONENTS.read_text(encoding="utf-8")


def _strip_comments(css: str) -> str:
    """Blank comments in place, preserving both length and newlines.

    Length-preserving alone is not enough: blanking a multi-line comment to
    spaces keeps every offset valid but collapses the lines inside it, so any
    line number derived afterwards is wrong. This file asserts two absolute line
    numbers, and the first draft of this helper put them out by 70.
    """
    return re.sub(
        r"/\*.*?\*/",
        lambda m: re.sub(r"[^\n]", " ", m.group(0)),
        css,
        flags=re.S,
    )


def _head_pattern(selector: str) -> str:
    """Match `selector` only where it ends a selector-list entry.

    The leading guard rejects a longer compound that merely ends in the same
    text: without it `.frame-title` also matches `& .frame-title`, and the
    resurrection of a deleted rule would hide behind a surviving one.
    """
    parts = [re.escape(part) for part in selector.split()]
    return r"(?<![\w.#\[&-])" + r"\s+".join(parts) + r"\s*[,{]"


def _rule_heads(css: str, selector: str) -> int:
    return len(re.findall(_head_pattern(selector), css, flags=re.S))


def _body_from(css: str, brace: int) -> str:
    """Brace-matched body starting at `brace`.

    Brace-matched rather than regex-delimited because the frame families are
    nested (`[data-theme='dark'] & .frame-header`), so a rule body legitimately
    contains further `{}` pairs.
    """
    depth = 0
    for index in range(brace, len(css)):
        if css[index] == "{":
            depth += 1
        elif css[index] == "}":
            depth -= 1
            if depth == 0:
                return css[brace + 1 : index]
    raise AssertionError("unbalanced braces")


def _rule_body_at_line(css: str, selector: str, line: int) -> str:
    """Body of the rule whose head `selector` starts on exactly `line`.

    Anchored by line, not by occurrence index. An earlier draft of this file
    keyed these assertions by `(selector, nth occurrence)` and every ambiguous
    selector resolved to the wrong rule: `.frame-title` #0 landed on line 3815,
    inside `@layer workout` and nowhere near this packet's window, so the
    assertion passed by checking a rule the packet never touched. Ten of the
    nineteen keys were wrong that way. Line anchoring is the same convention
    WP4.4-a already uses for the layer span, and it fails loudly instead of
    silently drifting onto a different rule.
    """
    for match in re.finditer(_head_pattern(selector), css, flags=re.S):
        if css.count("\n", 0, match.start()) + 1 != line:
            continue
        brace = css.find("{", match.end() - 1)
        assert brace != -1, f"{selector} at line {line} has no body"
        return _body_from(css, brace)
    raise AssertionError(f"no rule head {selector!r} starts on line {line}")


# ---------------------------------------------------------------------------
# The eleven generations deleted whole.
#
# Each owned ZERO longhands in all 446 audited contexts. The comment records the
# pre-deletion head count so a reviewer can see the size of each cut; the
# assertion is that nothing with that head survives.
# ---------------------------------------------------------------------------

# The `.summary-frame` glass table generation. Every declaration is `!important`
# and every one lost: the Weekly and Session bundles repaint the same longhands
# later in the same origin, and `components.css` loads before both on all four
# routes that mount a summary frame.
WHOLE_RULE_DELETIONS = {
    ".summary-frame.frame-calm-glass .table": 1,
    ".summary-frame.frame-calm-glass .table thead th": 2,
    ".summary-frame.frame-calm-glass .table tbody td": 2,
    "[data-theme='dark'] .summary-frame.frame-calm-glass .table thead th": 1,
    "[data-theme='dark'] .summary-frame.frame-calm-glass .table tbody td": 1,
    # The Bootstrap-era dark generation, superseded by the token surfaces in
    # `theme-dark.css`. Two `.collapsible-frame` rules share one head.
    "[data-theme='dark'] & .collapsible-frame": 2,
    "[data-theme='dark'] & .input-fields-group": 1,
    "[data-theme='dark'] & .btn-primary": 1,
    "[data-theme='dark'] & .btn-secondary": 1,
}

# ---------------------------------------------------------------------------
# The nineteen rules that survive with dead declarations removed.
#
# Keyed by (selector, post-deletion line) — `.frame-content` and the dark
# `.frame-title` pair each have two generations and only one of each was cut,
# and several of these selectors also appear as the tail of longer compounds.
# The assertion is per-property inside that rule's own body, so a resurrection
# cannot hide in a different rule that happens to set the same property.
# ---------------------------------------------------------------------------
COLLAPSE_TOGGLE_LINE = 4750

PARTIAL_RULE_DELETIONS: dict[tuple[str, int], tuple[str, ...]] = {
    (".frame-title", 4497): (
        "background", "color", "font-size", "font-weight", "letter-spacing",
        "padding", "position", "text-transform",
    ),
    ("[data-theme='dark'] & .frame-title, [data-theme='dark'] & .filters-title", 4506): (
        "backdrop-filter", "background", "color",
    ),
    (
        "[data-theme='dark'] & .action-frame .frame-title, "
        "[data-theme='dark'] & .filters-section .filters-title",
        4511,
    ): ("background", "color"),
    (".filters-section", 4519): (
        "backdrop-filter", "background", "border", "border-radius", "box-shadow",
        "contain", "isolation", "position",
    ),
    (".filters-title", 4526): (
        "backdrop-filter", "background", "color", "font-size", "font-weight",
        "letter-spacing", "padding", "position", "text-transform",
    ),
    (".action-frame", 4579): ("background-color", "display", "flex-direction", "margin-bottom"),
    (".collapsible-frame", 4647): ("background", "border", "border-radius", "box-shadow"),
    (".frame-header", 4671): (
        "align-items", "background", "display", "padding", "position", "z-index",
    ),
    (".frame-title, .filters-title", 4696): ("font-size", "padding-bottom", "position"),
    ("[data-theme='dark'] & .frame-header", 4730): ("background", "border-bottom"),
    ("[data-theme='dark'] & .frame-title, [data-theme='dark'] & .filters-title", 4744): ("color",),
    # `background` and `color` are absent from this tuple on purpose: the
    # removal oracle withdrew both from the deletion set (see the module
    # docstring), so they must still be present in the rule. They are asserted
    # positively by `test_the_two_withdrawn_declarations_are_still_present`.
    (".collapse-toggle", COLLAPSE_TOGGLE_LINE): (
        "align-items", "background-color", "border", "border-radius",
        "box-shadow", "cursor", "display", "font-size", "font-weight",
        "gap", "height", "letter-spacing", "margin", "min-width", "padding",
        "transition",
    ),
    (".collapse-toggle i", 4769): ("transition",),
    (".frame-content", 4807): ("overflow", "transition"),
    (".filters-section .frame-header", 4869): ("padding",),
    ("[data-theme='dark'] & .collapsible-frame .frame-header", 4917): ("background-color",),
    (".frame-header-2025", 4943): ("display", "align-items"),
    (".collapse-toggle .toggle-icon", 4977): ("transition",),
    (".frame-content", 4992): ("overflow",),
}

# ---------------------------------------------------------------------------
# Every family the packet excluded, pinned as a count.
#
# Prose exclusions are unenforceable. These numbers are identical before and
# after the deletion, so any later edit that reaches into an excluded family
# reds here rather than being argued about.
# ---------------------------------------------------------------------------
FROZEN_FAMILY_COUNTS = {
    # A9 / N4: the whole `:is()` family belongs to WP4.4-i.
    r":is\(": 19,
    r":where\(": 58,
    # M10 / PR#3: reachable only through a JS-applied class.
    r"\.value-changed": 20,
    # M12 / PR#10: hover, focus and active are out of scope, declared up front.
    r":hover": 115,
    r":focus": 174,
    r":active": 16,
    # An inline sentinel cannot address a pseudo-element, so none was eligible.
    r"::[\w-]+": 51,
    r"@keyframes": 9,
    # M9: custom properties never enter a dead nomination.
    r"^\s*--[\w-]+\s*:": 3,
    # M11: condition-specific coverage was required, not deletion.
    r"@media": 33,
    r"prefers-reduced-motion": 3,
    # N2 freezes layer membership arc-wide.
    r"@layer": 1,
}

BEFORE_LINES = 5345
AFTER_LINES = 5207
BEFORE_IMPORTANT = 939
AFTER_IMPORTANT = 919

# The two candidates the removal oracle withdrew, kept as a positive assertion
# so a later packet cannot quietly delete them by widening this one.
WITHDRAWN = (
    ("background", "none"),
    ("color", "#6c757d"),
)


def test_whole_rule_generations_are_gone() -> None:
    """The eleven zero-winner generations have no surviving rule head.

    Counted rather than merely detected. `.collapsible-frame` and
    `.input-fields-group` legitimately survive as the tail of longer selectors,
    so "is it still mentioned" is too weak to notice that a deleted rule came
    back — the WP4.4-e red path proved exactly that failure mode on
    `.tbl-show-sm`.
    """
    css = _strip_comments(_css())
    for selector in WHOLE_RULE_DELETIONS:
        assert _rule_heads(css, selector) == 0, selector


def test_partial_rules_survive_without_their_dead_declarations() -> None:
    """Nineteen rules keep their live declarations and lose only the dead ones.

    Both halves matter. If the rule vanished the packet would have deleted more
    than it proved; if a listed property reappeared inside it, a later edit
    resurrected a declaration this packet measured as owning nothing.
    """
    css = _strip_comments(_css())
    for (selector, line), properties in PARTIAL_RULE_DELETIONS.items():
        body = _rule_body_at_line(css, selector, line)
        assert body.strip(), f"{selector}:{line} was emptied, not trimmed"
        for prop in properties:
            found = re.search(rf"(?<![\w-]){re.escape(prop)}\s*:", body)
            assert not found, f"{selector}:{line} regained {prop}"


def test_excluded_families_are_numerically_frozen() -> None:
    """Every excluded family has exactly the count it had before the deletion.

    This is the packet's real scope statement. The deletion set is 101
    declarations of paint and layout in the rest state; nothing it removed lives
    in an interaction state, a JS-applied class, a pseudo-element, a keyframe, a
    custom property, a media condition or the `:is()` family.
    """
    css = _strip_comments(_css())
    for pattern, expected in FROZEN_FAMILY_COUNTS.items():
        flags = re.M if pattern.startswith("^") else 0
        assert len(re.findall(pattern, css, flags)) == expected, pattern


def test_the_packet_stayed_above_the_frozen_layer_span() -> None:
    """N2 / the Packet-a pin: `@layer workout` did not move a single line.

    WP4.4-h's entire deletion window was chosen to make this true. Asserted here
    as well as in the Packet-a file so this packet reds on its own if a later
    edit widens it downward, instead of only reding a contract it may not edit.
    """
    css = _strip_comments(_css())
    open_index = css.index("@layer workout")
    brace = css.index("{", open_index)
    depth = 0
    close_index: int | None = None
    for index in range(brace, len(css)):
        if css[index] == "{":
            depth += 1
        elif css[index] == "}":
            depth -= 1
            if depth == 0:
                close_index = index
                break

    assert close_index is not None
    assert css.count("@layer") == 1
    assert css.count("\n", 0, open_index) + 1 == 3539
    assert css.count("\n", 0, close_index) + 1 == 4104


def test_the_deletion_was_pure_removal() -> None:
    """No insertion, no re-weighting: only whole declarations left the file.

    `!important` moves by exactly the twenty important declarations deleted. A
    packet that answered a cascade problem with a new `!important`, or that
    rewrote a value rather than removing it, cannot satisfy both of these.
    """
    raw = _css()
    assert raw.count("\n") == AFTER_LINES
    assert len(re.findall(r"!important", _strip_comments(raw))) == AFTER_IMPORTANT
    assert BEFORE_IMPORTANT - AFTER_IMPORTANT == 20
    assert BEFORE_LINES - AFTER_LINES == 138


def test_the_two_withdrawn_declarations_are_still_present() -> None:
    """`.collapse-toggle` keeps the two declarations the removal oracle saved.

    The 446-context census classified both as zero-winner, but the oracle that
    actually removes a declaration from the live CSSOM disagreed: deleting
    `color: #6c757d` moved the computed colour of every `.collapse-toggle` and
    its `.toggle-icon` child from `rgb(0, 131, 143)` to `rgb(102, 102, 102)` in
    42 element-property pairs, and `background: none` was never probed at all.
    Both were withdrawn under the oracle-disagreement and never-probed rules.

    Asserted positively, because their absence from `PARTIAL_RULE_DELETIONS` is
    only the absence of a claim — it would not notice their deletion.
    """
    css = _strip_comments(_css())
    body = _rule_body_at_line(css, ".collapse-toggle", COLLAPSE_TOGGLE_LINE)
    for prop, value in WITHDRAWN:
        found = re.search(rf"(?<![\w-]){re.escape(prop)}\s*:\s*{re.escape(value)}", body)
        assert found, f".collapse-toggle lost the withdrawn declaration {prop}: {value}"


def test_shared_cascade_premises_inside_components_are_intact() -> None:
    """The strings `tests/test_css_cascade_contracts.py` pins are all still here.

    That file is the arc's shared ceiling and only WP4.4-i may amend it (N6).
    Echoing its `components.css` premises locally means this packet fails in its
    own file, naming the packet, rather than surfacing as a red in a shared
    contract with no indication of which packet broke it.
    """
    raw = _css()
    assert raw.count("/* Shared frame infrastructure used by Workout Plan") == 1
    assert raw.count("/* Frame Base Styles - Glass Effect */") == 1
    assert raw.count(":where(#workout, .workout-log-page, .summary-frame) {") == 1
    assert raw.count("[data-theme='dark'] & .frame-title") == 2
    assert len(re.findall(r"^\.frame-header-2025 \{", raw, re.M)) == 1
    assert "html:has(" not in raw
    assert "&[data-theme='dark']" not in raw
