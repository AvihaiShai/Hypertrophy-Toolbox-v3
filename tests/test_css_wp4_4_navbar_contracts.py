"""WP4.4-f1 cascade contracts for `static/css/navbar.css`.

These lock the premises the packet's single deletion rests on. Each test fails
under its own violation (F16); the red-path proofs are recorded in
docs/CSS_PHASE4_WP4_4_F1_NAVBAR_EVIDENCE.md.

The assertions are deliberately **structural and occurrence-aware** rather than
substring-based. `.navbar` is the selector text of BOTH the rule f1 deleted
(`body:not(:has(#navbar)) .navbar`) and the rule f1 retained (`.navbar` at
navbar.css:892), so `assert ".navbar" in css` cannot tell a successful deletion
from a restored one. That defect class was found in packet `e` and again in
packet `d1`; this file avoids it by parsing rules and counting occurrences.

This file is packet-owned. It never edits, and must not be confused with, the
shared `tests/test_css_cascade_contracts.py`, which WP4.4-f1 runs but does not
touch (Plan v2 section 4d -- only packet i may amend that file).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
NAVBAR = ROOT / "static" / "css" / "navbar.css"
TEMPLATES = ROOT / "templates"


def _css() -> str:
    return NAVBAR.read_text(encoding="utf-8").replace("\r\n", "\n")


def _strip_comments(css: str) -> str:
    """Length-preserving, so byte offsets stay valid after stripping."""
    return re.sub(r"/\*.*?\*/", lambda m: " " * len(m.group(0)), css, flags=re.S)


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
# by census: navbar.css is linked only from templates/base.html:22, and that
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
# What must NOT have been deleted
# --------------------------------------------------------------------------

# The sibling of the deleted rule. `.navbar` is NOT dead legacy: #navbar carries
# the Bootstrap `navbar` class, and because this rule is UNLAYERED while
# `#navbar { position: sticky }` sits inside @layer navbar, the unlayered normal
# declaration wins regardless of specificity. `position: fixed` here is the
# value the browser actually computes -- which is why WP4.4-a's harness had to
# clip below a fixed top bar. Deleting it would move the navbar.
RETAINED_LEGACY_DECLS = (
    "position: fixed",
    "top: 0",
    "left: 0",
    "right: 0",
    "z-index: 1000",
)


def test_the_live_legacy_navbar_rule_is_retained_whole() -> None:
    matches = [r for r in _rules(_css()) if r["selector"] == ".navbar"]
    assert len(matches) == 1
    joined = " ".join(matches[0]["decls"])
    for decl in RETAINED_LEGACY_DECLS:
        assert decl in joined


def test_the_retained_legacy_rule_is_unlayered() -> None:
    """Its layer membership is what makes it the winner; N2 freezes that."""
    matches = [r for r in _rules(_css()) if r["selector"] == ".navbar"]
    assert matches and matches[0]["layer"] is None


@pytest.mark.parametrize(
    "declaration",
    ["--nav-gap: var(--s-3)", "--nav-padding-y: var(--s-3)", "--nav-padding-x: 1rem"],
)
def test_contract_pinned_navbar_tokens_survive(declaration: str) -> None:
    """Pinned by the shared tests/test_css_cascade_contracts.py:150-152 (F6)."""
    assert declaration in _strip_comments(_css())


def test_the_single_sourced_navbar_layer_block_survives() -> None:
    """G11: `navbar` is the only file declaring @layer navbar."""
    assert re.search(r"@layer\s+navbar\s*\{", _strip_comments(_css()))


# --------------------------------------------------------------------------
# Whole-surface invariants -- these are what make the packet pure deletion
# --------------------------------------------------------------------------

# Measured on the post-deletion file; every one was identical before it.
IMPORTANT_DECLARATIONS = 93
CUSTOM_PROPERTY_DECLARATIONS = 72
LAYER_BLOCKS = 1
STYLE_RULES = 193
KEYFRAME_STEPS = 5


def test_no_important_was_added_or_removed() -> None:
    """V3: a pure deletion that changes !important has re-weighted something."""
    assert len(re.findall(r"!\s*important", _strip_comments(_css()))) == IMPORTANT_DECLARATIONS


def test_no_custom_property_declaration_was_deleted() -> None:
    """Custom properties paint nothing and are non-winners for every property,
    so the ordinary non-winner rule must never be applied to them."""
    decls = [d for r in _rules(_css()) for d in r["decls"] if d.lstrip().startswith("--")]
    assert len(decls) == CUSTOM_PROPERTY_DECLARATIONS


def test_layer_membership_is_frozen() -> None:
    """N2: no rule moved across the boundary, and no layer block was added."""
    css = _strip_comments(_css())
    assert len(re.findall(r"@layer\s+[\w-]+\s*\{", css)) == LAYER_BLOCKS
    rules = _rules(_css())
    assert sum(1 for r in rules if r["layer"]) == 103
    assert sum(1 for r in rules if r["layer"] is None) == 90


def test_exactly_one_rule_was_removed_from_the_surface() -> None:
    """The packet's whole production change, stated as a count."""
    assert len(_rules(_css())) == STYLE_RULES


def test_keyframe_steps_are_untouched() -> None:
    """@keyframes steps are not style rules and have no DOM census; the first
    version of the f1 audit wrongly nominated five of them as dead."""
    css = _strip_comments(_css())
    blocks = re.findall(r"@keyframes\s+[\w-]+\s*\{", css)
    assert len(blocks) == 2
    steps = re.findall(r"^\s*(?:from|to|\d+%)\s*\{", css, flags=re.M)
    assert len(steps) == KEYFRAME_STEPS


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


def test_base_html_renders_the_navbar_unconditionally() -> None:
    """The deleted rule's guard `body:not(:has(#navbar))` is unsatisfiable only
    while this holds: if #navbar ever became conditional, the rule would have
    been reachable and its deletion would be a behaviour change."""
    html = (TEMPLATES / "base.html").read_text(encoding="utf-8")
    body = html[html.index("<body>") : html.index("</body>")]
    header = re.search(r'<header[^>]*id="navbar"', body)
    assert header is not None
    preceding = body[: header.start()]
    assert "{%" not in preceding.replace("{% block", "")
