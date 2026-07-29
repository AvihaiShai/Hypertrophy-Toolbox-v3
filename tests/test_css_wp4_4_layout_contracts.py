"""WP4.4-e cascade contracts for `static/css/layout.css`.

These lock the premises the packet's deletions rest on. Each test is written so
that it fails under its own violation (F16) -- the red-path proofs are recorded
in docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md.

This file is packet-owned. It never edits, and must not be confused with, the
shared `tests/test_css_cascade_contracts.py`, which WP4.4-e runs but does not
touch (Plan v2 section 4d -- only packet i may amend that file).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "static" / "css" / "layout.css"
TEMPLATES = ROOT / "templates"
JS = ROOT / "static" / "js"


def _css() -> str:
    return LAYOUT.read_text(encoding="utf-8")


def _strip_comments(css: str) -> str:
    """Length-preserving, so byte offsets stay valid after stripping."""
    return re.sub(r"/\*.*?\*/", lambda m: " " * len(m.group(0)), css, flags=re.S)


# Classes whose entire rule set WP4.4-e deleted from layout.css. Every one was
# measured at census 0 across 11 routes x 2 themes x 16 viewport widths, and
# each deleted rule was demonstrably visible to the synthetic oracle before
# deletion (so its disappearance is a measurement, not an assumption).
DELETED_CLASSES = (
    "form-container",
    "input-frame",
    "el-clip",
    "col--ellipsis",
    "col--wrap",
    "col--nowrap",
    "tbl-col-chooser",
    "tbl-col-chooser-trigger",
    "tbl-col-chooser-menu",
    "tbl-toolbar",
    "sr-only",
    "tbl--loading",
)

# Classes whose every layout.css rule is gone. `tbl-toolbar` and `input-frame`
# are excluded: both still appear inside selector lists that also name a LIVE
# class, and those rules were retained whole. Removing just the dead branch
# would be re-weighting a live rule, which is out of scope for a pure-deletion
# packet -- see test_partially_reachable_rules_kept_their_dead_branch.
FULLY_REMOVED_CLASSES = tuple(
    c for c in DELETED_CLASSES if c not in {"tbl-toolbar", "input-frame"}
)

# Rules WP4.4-e deliberately did NOT touch, each for a stated reason. Pinning
# them here is what stops a later packet from treating this packet's silence as
# permission.
RETAINED_SNIPPETS = (
    # The live dark-theme token block. body.dark-mode was deleted as
    # unreachable; this attribute-selector block is the live definition and
    # must survive.
    '[data-theme="dark"]',
    # The print rule pairs .tbl-toolbar with .tbl-controls, which IS live
    # (table-responsiveness.js:112 creates it). Partially reachable -> retained
    # in full, including its .tbl-toolbar branch.
    ".tbl-controls,",
)

# The deferred breakpoint-helper family, pinned by exact occurrence count.
#
# Substring presence is too weak a gate here: `.tbl-show-sm` appears twice (a
# top-level rule and an @media override), so asserting "it is still mentioned"
# stays green when one of the two is deleted. The red-path proof caught exactly
# that. Counts pin the family member by member.
#
# Deferred because three members (the @media overrides) declare `display: block`
# -- a bare div's initial value -- so no control element can distinguish them
# and the oracle is inherently blind. Deleting only the six observable members
# would leave @media overrides targeting classes with no base rule.
DEFERRED_HELPER_COUNTS = {
    "tbl-show-sm": 2,
    "tbl-show-md": 2,
    "tbl-show-lg": 2,
    "tbl-hide-sm": 1,
    "tbl-hide-md": 1,
    "tbl-hide-lg": 1,
}


def test_deleted_rule_blocks_stay_deleted() -> None:
    """No rule in layout.css targets a class this packet proved unreachable.

    Red path: restoring any deleted block reintroduces its selector and fails.
    """
    css = _strip_comments(_css())
    offenders = []
    for cls in FULLY_REMOVED_CLASSES:
        # A selector use, not a mention inside a var() name or another word.
        if re.search(rf"\.{re.escape(cls)}(?![\w-])", css):
            offenders.append(cls)
    assert offenders == [], (
        "layout.css again styles classes WP4.4-e deleted as unreachable: "
        f"{offenders}. If a class became reachable, the deletion must be "
        "revisited with a fresh census -- do not simply re-add the rule."
    )


def test_partially_reachable_rules_kept_their_dead_branch() -> None:
    """Rules whose selector list mixes a dead branch with a LIVE one survive whole.

    `.tbl-controls, .tbl-toolbar` -- `.tbl-controls` is created at runtime by
    static/js/table-responsiveness.js, so the rule paints and stays.
    `.input-frame, .action-frame` -- `.action-frame` is applied throughout
    templates/user_profile.html.

    Trimming the dead branch out of either would re-weight a live rule. That is
    not a deletion and is out of scope for WP4.4-e.

    Red path: deleting the `.tbl-toolbar` branch from the print rule, or the
    `.input-frame` branch from the frame rules, fails this test.
    """
    css = _strip_comments(_css())
    assert re.search(r"\.tbl-controls\s*,\s*\.tbl-toolbar\s*\{", css), (
        "the print rule `.tbl-controls, .tbl-toolbar` lost its .tbl-toolbar "
        "branch; .tbl-controls is live so the rule must be retained whole"
    )
    assert re.search(r"\.input-frame\s*,\s*\.action-frame\s*\{", css), (
        "the `.input-frame, .action-frame` rules lost their .input-frame "
        "branch; .action-frame is live so the rule must be retained whole"
    )
    # And no OTHER layout.css rule may target these two classes alone.
    for cls, allowed in (("tbl-toolbar", 1), ("input-frame", 9)):
        found = len(re.findall(rf"\.{re.escape(cls)}(?![\w-])", css))
        assert found == allowed, (
            f".{cls} appears {found} times in layout.css, expected {allowed} "
            "(only inside the retained mixed selector lists)"
        )


def test_deleted_classes_are_still_unreachable() -> None:
    """Nothing in the app applies the deleted classes.

    This is the premise the deletion rests on, converted into a gate: adding
    `class="tbl-toolbar"` to a template now fails pytest rather than silently
    resurrecting a style whose rules are gone.

    Red path: adding `class="sr-only"` to any template fails this test.
    """
    corpus = []
    for base, pattern in ((TEMPLATES, "**/*.html"), (JS, "**/*.js")):
        for path in base.glob(pattern):
            corpus.append((path, path.read_text(encoding="utf-8", errors="replace")))

    class_attr = re.compile(r"""class\s*=\s*["']([^"']*)["']""")
    add_call = re.compile(
        r"""classList\.(?:add|toggle|replace)\(\s*["']([\w-]+)["']"""
    )

    offenders: list[str] = []
    for path, text in corpus:
        applied: set[str] = set()
        for match in class_attr.finditer(text):
            applied.update(match.group(1).split())
        applied.update(add_call.findall(text))
        for cls in DELETED_CLASSES:
            if cls in applied:
                offenders.append(f"{path.relative_to(ROOT)} applies .{cls}")

    assert offenders == [], (
        "a deleted layout.css class is now applied by the app: "
        + "; ".join(offenders)
    )


def test_retained_rules_are_still_present() -> None:
    """The rules WP4.4-e deliberately kept are still there.

    Red path: deleting the `[data-theme="dark"]` token block, or the print
    `.tbl-controls, .tbl-toolbar` rule, or the deferred breakpoint helpers,
    fails this test.
    """
    css = _css()
    missing = [snippet for snippet in RETAINED_SNIPPETS if snippet not in css]
    assert missing == [], (
        f"layout.css lost rules WP4.4-e explicitly retained: {missing}"
    )

    stripped = _strip_comments(css)
    wrong = {}
    for cls, expected in DEFERRED_HELPER_COUNTS.items():
        found = len(re.findall(rf"\.{re.escape(cls)}(?![\w-])", stripped))
        if found != expected:
            wrong[cls] = f"{found} (expected {expected})"
    assert wrong == {}, (
        "the deferred .tbl-show-*/.tbl-hide-* breakpoint-helper family changed: "
        f"{wrong}. WP4.4-e deferred this family whole because three of its "
        "members are invisible to any control element; it must be deleted as a "
        "unit under fresh evidence, not eroded rule by rule."
    )


def test_dark_theme_table_tokens_have_a_live_definition() -> None:
    """The seven --tbl-* tokens survive the body.dark-mode deletion.

    body.dark-mode declared exactly these seven custom properties and nothing
    else. It was deleted because `<body>` never carries the class -- not under
    the ordinary non-winner rule, which does not apply to custom properties.
    The live `[data-theme="dark"]` block above it declares the same seven, and
    that is what must remain.

    Red path: removing any one token from the `[data-theme="dark"]` block fails.
    """
    tokens = (
        "--tbl-border-color",
        "--tbl-header-bg",
        "--tbl-header-color",
        "--tbl-row-hover-bg",
        "--tbl-stripe-bg",
        "--tbl-sticky-shadow",
        "--tbl-sticky-shadow-header",
    )
    css = _strip_comments(_css())
    match = re.search(r'\[data-theme="dark"\]\s*\{(.*?)\}', css, flags=re.S)
    assert match, 'the [data-theme="dark"] token block is gone from layout.css'
    block = match.group(1)
    missing = [t for t in tokens if f"{t}:" not in block]
    assert missing == [], (
        f'[data-theme="dark"] no longer defines: {missing}. These are the only '
        "live definitions since body.dark-mode was deleted."
    )


def test_body_dark_mode_block_stays_deleted() -> None:
    """`.dark-mode` is not styled by layout.css and is not applied anywhere.

    Red path: restoring the `body.dark-mode` block fails the first assertion;
    adding `classList.add('dark-mode')` to a JS module fails the second.
    """
    assert "dark-mode" not in _strip_comments(_css()), (
        "layout.css styles .dark-mode again; the live mechanism is the "
        "data-theme attribute set by static/js/darkMode.js"
    )

    applies = re.compile(
        r"""classList\.(?:add|toggle|replace)\(\s*["']dark-mode(?![\w-])"""
    )
    hardcoded = re.compile(r"""class\s*=\s*["'][^"']*\bdark-mode(?![\w-])""")
    for base, pattern in ((TEMPLATES, "**/*.html"), (JS, "**/*.js")):
        for path in base.glob(pattern):
            text = path.read_text(encoding="utf-8", errors="replace")
            assert not applies.search(text), f"{path} applies .dark-mode as a class"
            assert not hardcoded.search(text), f"{path} hardcodes .dark-mode"


def test_layout_css_declares_no_cascade_layer() -> None:
    """N2 freezes @layer membership arc-wide.

    layout.css had zero `@layer` tokens at the WP4.4-a baseline and must still
    have zero: this packet may not move a rule across a layer boundary, and the
    cheapest expression of that for this surface is that no layer exists in it.

    Red path: wrapping any rule in `@layer navbar { ... }` fails.
    """
    assert "@layer" not in _strip_comments(_css()), (
        "layout.css now declares an @layer; N2 freezes layer membership for "
        "the whole WP4.4 arc"
    )


def test_orphaned_keyframes_went_with_their_only_consumer() -> None:
    """`@keyframes tbl-spin` had exactly one consumer, `.tbl--loading::after`.

    Deleting the consumer without the keyframes would leave dead animation
    data; keeping the keyframes reachable would be a false claim.

    Red path: restoring `@keyframes tbl-spin` fails.
    """
    css = _strip_comments(_css())
    assert "tbl-spin" not in css, (
        "@keyframes tbl-spin (or a reference to it) is back in layout.css, but "
        "its only consumer .tbl--loading::after was deleted"
    )


@pytest.mark.parametrize(
    "surface",
    ["tokens.css", "components.css", "navbar.css", "theme-dark.css", "a11y.css"],
)
def test_deleted_classes_are_not_resurrected_by_a_sibling_surface(surface: str) -> None:
    """A sibling bundle must not start styling a class layout.css stopped
    styling, which would silently re-create the family this packet removed.

    `.form-container` and `.input-frame` are deliberately excluded:
    components.css already defines them, and WP4.4-e's deletion was scoped to
    layout.css's own copies. Their reachability -- census 0 -- is what makes
    both copies dead, and that premise is gated by
    test_deleted_classes_are_still_unreachable above.

    Red path: adding `.tbl-toolbar {}` to components.css fails this test.
    """
    path = ROOT / "static" / "css" / surface
    if not path.exists():
        pytest.skip(f"{surface} not present")
    css = _strip_comments(path.read_text(encoding="utf-8"))
    scoped = [c for c in DELETED_CLASSES if c not in {"form-container", "input-frame"}]
    offenders = [c for c in scoped if re.search(rf"\.{re.escape(c)}(?![\w-])", css)]
    assert offenders == [], (
        f"{surface} now styles classes WP4.4-e deleted from layout.css: {offenders}"
    )
