"""WP4.4-i cascade contracts for the `static/css/components.css` `:is()` family.

Packet-owned per N1. Complements — and does not duplicate —
`tests/test_css_wp4_4_components_contracts.py`, which owns the re-expressed
`:where()`/`:hover` premise, and `tests/test_css_cascade_contracts.py`, which
WP4.4-i runs and never edits (N6's amendment grant went unused).

**What the packet did.** The shared family borrows ID-level weight: `:is()` takes
the specificity of its most specific argument, so `#workout[data-page="workout-plan"]`
at (1,1,0) exported `a = 1` to the three branches carrying no ID at all.
`.progression-plan-container` is split out of **all thirteen rules** — fourteen
selector lines, R1 carrying two — so that branch no longer receives ID-level
specificity for any of the family's 39 declarations.

**Why only that branch.** De-weighting a branch hands every page-local rule that
currently loses to it a chance to win. Measured per branch:

* `.workout-log-page` — 16 of the 45 declarations in `pages-workout-log.css`
  regions A/B/C lose *only* to this family, and region B's dark header has zero
  always-wins (Inventory B §3.1).
* `.summary-frame.frame-calm-glass` — both summary bundles carry ID-scoped
  `!important` rules (`#weekly-summary-container` / `#session-summary-container`)
  that win on `a` alone once the arm drops to `a = 0`. De-weighting it was
  measured, not argued: 8,784 computed values change across the two summary
  routes, reverting to the unmigrated `#404040` / `#e0e0e0` / `#2d2d2d` /
  `#1a1a1a` legacy palette.
* `#workout[data-page="workout-plan"]` — carries the ID itself, so splitting it
  out changes its own specificity by nothing while stripping the donor from the
  other three. It is the donor and must stay.

Both unsafe branches keep the donor, which preserves their specificity *exactly*.
`test_the_unsafe_branches_never_lose_the_id_donor` is the pin that stops a later
edit reversing that quietly.

**The zero-line invariant.** `tests/test_css_wp4_4_a_baseline_contracts.py`
re-derives `measure.layer_spans("components.css")` from the working tree and pins
`openLine 3539`. The whole family sits above that line, so adding even one line
moves the span and reds a contract this packet may not touch — the same trap that
cost WP4.4-h 158 of 247 cuts. A first attempt that split each rule across two
lines moved it to 3552 and red six tests in two files. Every split is therefore
written on one physical line. That invariant is invisible in the CSS and a routine
reformatting pass would break it with a confusing error in an unrelated file, so
it is enforced here rather than left as folklore.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ROOT / "static" / "css" / "components.css"

ID_DONOR = '#workout[data-page="workout-plan"]'
LOG_BRANCH = ".workout-log-page"
SUMMARY_BRANCH = ".summary-frame.frame-calm-glass"
PROG_BRANCH = ".progression-plan-container"

DONOR_GROUP = f":is({ID_DONOR}, {LOG_BRANCH}, {SUMMARY_BRANCH})"
DONOR_GROUP_REDUCED_MOTION = f":is({ID_DONOR}, {LOG_BRANCH})"

# Thirteen rules; R1 carries two selector lines, so fourteen lines in total.
I_OWNED_SELECTOR_LINES = 14


def _css() -> str:
    return COMPONENTS.read_text(encoding="utf-8")


def _family_lines(css: str) -> list[str]:
    return [
        line
        for line in css.splitlines()
        if DONOR_GROUP in line or DONOR_GROUP_REDUCED_MOTION in line
    ]


def _is_groups(css: str) -> list[str]:
    """Return the argument list of every `:is(...)` in the file.

    A naive `\\(([^)]*)\\)` is wrong here: the family's arguments contain
    `[data-page="workout-plan"]` and the reduced-motion rule sits beside
    `:not(caption)`, so the scan counts parentheses instead of stopping at the
    first one.
    """
    groups = []
    for match in re.finditer(r":is\(", css):
        depth = 1
        i = match.end()
        while i < len(css) and depth:
            if css[i] == "(":
                depth += 1
            elif css[i] == ")":
                depth -= 1
            i += 1
        assert depth == 0, f"unbalanced :is( at offset {match.start()}"
        groups.append(css[match.end() : i - 1])
    return groups


def test_the_repair_added_no_lines() -> None:
    """The `@layer workout` span pin at `openLine 3539` sits below the family.

    WP4.4-h measured this file at 5,207 newlines and WP4.4-i is a selector
    rewrite, not a deletion, so the count must be identical. A failure here means
    a split was reflowed onto extra lines, which moves the frozen layer span and
    reds `tests/test_css_wp4_4_a_baseline_contracts.py` — a file neither packet
    may edit.
    """
    assert _css().count("\n") == 5207


def test_all_thirteen_rules_carry_the_progression_split() -> None:
    """Every rule in the family is repaired — the packet is not partial.

    The branch must stop receiving ID-level specificity for **all 39**
    declarations. A count below fourteen means a rule was left borrowing the
    donor's weight, which is the halfway state this packet exists not to ship.
    """
    lines = _family_lines(_css())
    assert len(lines) == I_OWNED_SELECTOR_LINES, (
        f"expected {I_OWNED_SELECTOR_LINES} repaired selector lines, got {len(lines)}"
    )
    for line in lines:
        assert line.count(PROG_BRANCH) == 1, line


def test_every_repaired_rule_keeps_both_arms_on_one_physical_line() -> None:
    """Each repaired rule is `<progression arm>, <donor arm>` on one line.

    Lowest specificity first, because `no-descending-specificity` reads a
    selector list in order and the split arm is one `a` below its sibling. Order
    inside a selector list has no cascade effect — every arm shares one
    declaration block at one source position — so this is presentation only.
    """
    for line in _family_lines(_css()):
        stripped = line.strip()
        assert stripped.startswith(PROG_BRANCH) or stripped.startswith(
            f"[data-theme='dark'] {PROG_BRANCH}"
        ), f"progression arm is not first: {stripped}"
        assert stripped.endswith(",") or stripped.endswith("{"), (
            f"split arm is not on one physical line: {stripped}"
        )
        assert DONOR_GROUP in line or DONOR_GROUP_REDUCED_MOTION in line


def test_the_unsafe_branches_never_lose_the_id_donor() -> None:
    """The safety premise of the whole packet, expressed as an invariant.

    `.workout-log-page` and `.summary-frame.frame-calm-glass` were measured
    unsafe to de-weight. They stay grouped with the ID donor, which keeps their
    specificity bit-identical. Any future edit that splits either of them out —
    or that removes the donor from a group containing them — resurrects
    suppressed page-local rules on Workout Log and both summary routes.
    """
    for group in _is_groups(_css()):
        if LOG_BRANCH in group or SUMMARY_BRANCH in group:
            assert ID_DONOR in group, (
                "an unsafe branch appears in an :is() group without the ID donor, "
                f"which de-weights it: :is({group})"
            )


def test_the_reduced_motion_rule_keeps_its_three_branch_asymmetry() -> None:
    """The reduced-motion rule omits `.summary-frame.frame-calm-glass` on purpose.

    Summary table cells are deliberately not transition-suppressed under
    `prefers-reduced-motion: reduce`. Adding the branch would be a visible
    behavioural change on two routes, and nothing in this repository can observe
    it: no spec sets `reducedMotion`, and `e2e/visual-helpers.ts` forces
    `transition-duration: 0s` globally. Splitting the rule for Progression must
    not normalise the branch set in passing.
    """
    css = _css()
    # Anchor on the rule, not on the at-rule: the file carries three
    # `prefers-reduced-motion` blocks and only one of them holds this selector.
    marker = f"{DONOR_GROUP_REDUCED_MOTION} .table.table-calm tbody td"
    assert css.count(marker) == 1, "reduced-motion anchor is not unique"
    anchor = css.index(marker)

    # The rule's selector list runs from the end of the previous block to the
    # `{` that opens this one. Sixteen arms; only the last carries `:is()`.
    selector_list = css[css.rindex("}", 0, anchor) + 1 : css.index("{", anchor)]

    assert SUMMARY_BRANCH not in selector_list, (
        "the summary branch was added to the reduced-motion rule; that is a "
        "behavioural change on Weekly and Session Summary under "
        "prefers-reduced-motion, and nothing in this repository can observe it"
    )
    assert f"{PROG_BRANCH} .table.table-calm tbody td" in selector_list


def test_the_family_token_counts_match_the_approved_delta() -> None:
    """Restated here so this packet fails on its own violation (F16).

    `tests/test_css_wp4_4_components_contracts.py` owns the authoritative
    partition — frozen outside the family, exact shapes inside it. These are the
    whole-file totals that partition implies, asserted on the raw text so the two
    files would disagree if either drifted.
    """
    css = _css()
    assert css.count(":is(") == 19
    assert css.count(":where(") == 59
    assert css.count(":hover") == 118
    # Unchanged: a selector rewrite adds no declarations. WP4.4-h shipped 919.
    assert len(re.findall(r"!important", css)) == 919
