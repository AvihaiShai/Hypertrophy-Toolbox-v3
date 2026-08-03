"""Static contracts for the accessible field-separator rule in components.css.

The row-card outline and the field separator are two different borders drawn by
two different rules. Raising `--tbl-border-color` fixed the outline but left the
field separator on `#d0d0d0` or `transparent`, because three earlier
`!important` rules owned it. That gap was invisible to the visual baselines --
the Progression and Body Composition tables render with zero rows unless the
visual seed supplies them -- so it needs its own contract.

The rendered half of this contract lives in
`e2e/visual-field-separator.spec.ts`, which reads computed styles in a real
browser. This file locks the source-level premises that spec depends on.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ROOT / "static" / "css" / "components.css"
SEPARATORS = ROOT / "static" / "css" / "layout.css"
BASE_TEMPLATE = ROOT / "templates" / "base.html"

# One arm per cascade competitor, in the theme that states it.
#
# The arms are `tbody td`, never `> :not(caption) > * > *`: the Calm Glass
# family states its cell colour through a `tbody td` rule, so the star form
# measures one class lower and loses. The first version of this fix used the
# star form and silently changed nothing on five of the seven families.
REQUIRED_LIGHT_ARMS = (
    ".table.table tbody td",
    ".progression-plan-container .table.table-calm.table-calm tbody td",
    ':is(#workout[data-page="workout-plan"], .workout-log-page, '
    '.summary-frame.frame-calm-glass) .table.table-calm.table-calm tbody td',
)

REQUIRED_DARK_ARMS = (
    "[data-theme='dark'][data-theme='dark'] .table.table tbody td",
    "[data-theme='dark'][data-theme='dark'] .results-section tbody td",
    "[data-theme='dark'][data-theme='dark'] .progression-plan-container "
    ".table.table-calm.table-calm tbody td",
)


def _css(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", lambda m: " " * len(m.group(0)), css, flags=re.S)


def _separator_rules() -> list[str]:
    """The appended rule blocks, located by declaration rather than by line.

    Two blocks: a light-theme set and a dark-theme set. Dark needs its own
    because dark states the same cell colour again through page-scoped
    `!important` rules that outrank the light arms.
    """
    css = _strip_comments(_css(SEPARATORS))
    matches = [
        m.group(0)
        for m in re.finditer(
            r"([^{}]*)\{[^{}]*border-bottom-color:\s*var\(--tbl-border-color\)\s*!important;[^{}]*\}",
            css,
            flags=re.S,
        )
    ]
    assert len(matches) == 2, (
        f"expected exactly two field-separator rules (light + dark), found "
        f"{len(matches)}. Fewer means a theme lost its accessible value; more "
        "makes the winning value ambiguous."
    )
    return matches


def test_separator_rules_carry_every_required_selector_arm() -> None:
    """One arm per competitor, each mirroring that competitor's specificity.

    Dropping an arm silently returns those tables to `#d0d0d0` (1.54:1),
    `#495057`, `#404040` or a near-transparent white, depending on which rule
    then wins.

    Red path: deleting the `:is(...)` arm fails this test.
    """
    joined = " ".join(" ".join(r.split()) for r in _separator_rules())
    for label, arms in (("light", REQUIRED_LIGHT_ARMS), ("dark", REQUIRED_DARK_ARMS)):
        missing = [arm for arm in arms if " ".join(arm.split()) not in joined]
        assert missing == [], f"{label} field-separator arms missing: {missing}"


def test_separator_rules_delegate_to_the_contrast_bound_token() -> None:
    """The value must be the token, never a literal.

    `--tbl-border-color` is contrast-bound by
    test_css_wp4_4_layout_contracts.py. A literal here would satisfy this file
    while silently escaping that floor.

    Red path: replacing either value with `#d0d0d0` fails.
    """
    for rule in _separator_rules():
        assert "var(--tbl-border-color)" in rule
        literal = re.search(r"border-bottom-color:\s*(#[0-9a-fA-F]{3,8})", rule)
        assert literal is None, (
            f"field separator hardcodes {literal.group(1)} instead of the "
            "contrast-bound token"
        )


def test_separator_rules_own_one_longhand_only() -> None:
    """Scope discipline: these rules may not become a general table restyle.

    They exist to win a colour argument they did not start. Anything beyond
    `border-bottom-color` belongs to the families that already own table
    chrome.

    Red path: adding `background: red !important;` fails.
    """
    for rule in _separator_rules():
        body = rule.split("{", 1)[1].rsplit("}", 1)[0]
        props = {
            d.split(":", 1)[0].strip()
            for d in body.split(";")
            if d.strip() and ":" in d
        }
        assert props == {"border-bottom-color"}, (
            f"field-separator rule declares {sorted(props)}; it must own "
            "border-bottom-color and nothing else"
        )


def test_dark_arms_buy_specificity_without_ids_or_new_important_surfaces() -> None:
    """The repeated attribute is the whole mechanism, so it is asserted.

    `[data-theme='dark'][data-theme='dark']` selects exactly what the single
    form selects; the duplication lifts each arm one step above its dark
    competitor without introducing an id.

    Red path: collapsing the duplication drops the arms below
    `[data-theme='dark'] .table tbody td` and dark silently reverts.
    """
    dark = [r for r in _separator_rules() if "[data-theme='dark']" in r]
    assert len(dark) == 1, "expected exactly one dark-theme field-separator rule"
    selector = dark[0].split("{", 1)[0]
    assert "[data-theme='dark'][data-theme='dark']" in selector, (
        "dark arms no longer repeat the theme attribute, so they sit below the "
        "dark rules they must outrank"
    )
    assert "#" not in selector.replace('#workout[data-page="workout-plan"]', ""), (
        "dark arms introduced an id selector; specificity must come from the "
        "repeated attribute, not from escalating to id weight"
    )


def test_card_mode_suppresses_the_trailing_separator() -> None:
    """The last field in a card needs no divider under it.

    In card mode cells stack, so a bottom border on the final cell draws a line
    immediately inside the card outline. Both card-mode queries must suppress
    it, and by width rather than colour so the geometry matches the
    non-important rule it reinforces.

    Red path: deleting either block leaves a doubled line at every card foot.
    """
    css = _strip_comments(_css(SEPARATORS))
    hits = re.findall(
        r":last-child\s*\{\s*border-bottom-width:\s*0\s*!important;\s*\}", css
    )
    assert len(hits) >= 2, (
        "expected the trailing-separator suppression in both the @container and "
        f"@media card-mode blocks, found {len(hits)}"
    )


@pytest.mark.parametrize("competitor", [
    ".table th,\n.table td",
    "border-color: transparent !important",
])
def test_the_outranked_rules_still_exist(competitor: str) -> None:
    """The separator rule wins on source order, so its competitors must remain.

    If one is deleted later, this rule stops being the last word and its
    placement stops being load-bearing -- at which point the arms above are
    carrying weight for a cascade that no longer exists and should be
    simplified deliberately, not discovered by a red visual diff.

    Red path: deleting either competitor fails, prompting that review.
    """
    css = _strip_comments(_css(COMPONENTS))
    assert competitor in css, (
        f"{competitor!r} is gone from components.css. The field-separator rule "
        "was written to outrank it on source order; re-derive whether its "
        "selector arms are still needed."
    )


def test_separator_sheet_loads_after_the_rules_it_outranks() -> None:
    """Placement is part of the mechanism, so it is asserted.

    a11y.css must come after components.css, which is where the `#d0d0d0` cell
    pin and the Calm Glass family live. It deliberately does NOT need to be
    last: the route bundles load after it, and the arms outrank those on
    specificity rather than order.

    Red path: moving the a11y.css link above components.css fails.
    """
    html = _css(BASE_TEMPLATE)
    order = re.findall(r"filename='css/([A-Za-z0-9_.-]+\.css)'", html)
    assert "a11y.css" in order and "components.css" in order
    assert order.index("a11y.css") > order.index("components.css"), (
        "a11y.css now loads before components.css, so the separator rules sit "
        "below the #d0d0d0 cell pin they exist to outrank"
    )


def test_no_extra_global_bundle_was_introduced() -> None:
    """The fix rides an existing bundle rather than adding a ninth.

    tests/test_css_cascade_contracts.py caps base.html at eight app-global
    stylesheets. An earlier draft of this fix shipped its own sheet and broke
    that cap; this records why it does not.

    Red path: adding another <link> to base.html fails there, and here.
    """
    html = _css(BASE_TEMPLATE)
    # Only first-party links; the CDN fallbacks are not app bundles. The count
    # itself is owned by test_css_cascade_contracts.py -- this asserts the
    # narrower fact that the separator fix did not add a sheet of its own.
    static = re.findall(r"filename='css/([A-Za-z0-9_.-]+\.css)'", html)
    assert "table-separators.css" not in static, (
        "the separator fix reintroduced its own stylesheet; it must ride "
        "a11y.css so the eight-bundle runtime cap still holds"
    )
    assert "a11y.css" in static


def test_no_global_bootstrap_border_variable_was_repointed() -> None:
    """The fix is component-owned; it must not move Bootstrap's own variables.

    Red path: adding `--bs-border-color: ...` to the separator rule fails.
    """
    rules = "".join(_separator_rules())
    for token in ("--bs-border-color", "--bs-table-border-color"):
        assert token not in rules, (
            f"field-separator rule repoints {token}; that would change every "
            "Bootstrap-bordered surface, not the seven table families"
        )
