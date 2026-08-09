"""Cascade contracts for `static/css/layout.css`.

These lock the premises two packets' deletions rest on. Each test is written so
that it fails under its own violation (F16); the red-path proofs are recorded in
the evidence document that owns each group.

Two packets share this file:

* **WP4.4-e** deleted 34 unreachable rule blocks. Evidence:
  docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md.
* **The table-helper re-audit** deleted the nine `.tbl-show-*` / `.tbl-hide-*`
  breakpoint helpers WP4.4-e deferred, and replaced their occurrence-count pin
  with C1-C5. Evidence: docs/css_table_helpers_cleanup/EVIDENCE.md, which
  supersedes `_E_LAYOUT_` section 4a -- that section's stated reason for the
  deferral ("no control element can distinguish them ... an inherent limit, not
  a fixable probe defect") was measured and refuted. See
  BREAKPOINT_HELPER_CLASSES.

This file is packet-owned. It never edits, and must not be confused with, the
shared `tests/test_css_cascade_contracts.py`, which both packets run but do not
touch.
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

# The breakpoint-helper family WP4.4-e deferred and the table-helper re-audit
# deleted, as one indivisible unit.
#
# WP4.4-e deferred all nine on a stated measurement limit: three of them declare
# `display: block`, and that packet's probe host was a bare `<div>` whose UA
# initial `display` is already `block`, so those three could not be told apart
# from their control. It recorded that as "an inherent limit, not a fixable probe
# defect", and pinned the family by exact occurrence count so it could not be
# eroded rule by rule.
#
# THAT LIMIT WAS A PROPERTY OF THE PROBE HOST, NOT OF THE RULES, and the re-audit
# measured the refutation: hosts whose UA initial `display` is NOT `block` --
# `<span>` (`inline`), `<li>` (`list-item`), `<td>` (`table-cell`) -- distinguish
# all nine, with no injected author CSS.
#
# Full record, including every denominator: docs/css_table_helpers_cleanup/
# EVIDENCE.md, which supersedes docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md
# section 4a. The C1-C5 banner below states what replaced the pin and why.
BREAKPOINT_HELPER_CLASSES = (
    "tbl-show-sm",
    "tbl-show-md",
    "tbl-show-lg",
    "tbl-hide-sm",
    "tbl-hide-md",
    "tbl-hide-lg",
)


def _rule_heads(css: str) -> list[tuple[tuple[str, ...], str]]:
    """Every rule head in `css` as `(enclosing_preludes, head)`.

    A "head" is whatever precedes a `{` -- a selector list, or an at-rule
    prelude, or a selector list nested inside one. Scanning brace boundaries
    finds a class wherever it can actually select: at any depth, inside `@media`,
    and in any position within a compound or descendant chain.

    The enclosing preludes are carried, not just a depth integer, because
    "is it inside an `@media`" is a weaker question than "which `@media`". A
    restoration that merged the family into two rules inside ONE query collapses
    three breakpoint bands into one while still presenting three base rules and
    six overrides; only the prelude tells them apart.

    `_head_pattern` in tests/test_css_wp4_4_components_contracts.py matches a
    selector only where it ends a selector-list entry. That is the right tool
    there and the wrong one here -- it would not see `.foo.tbl-show-sm` or
    `.tbl-show-sm .bar`, and this family's whole risk is that a member comes
    back in some shape the pin did not anticipate.
    """
    heads: list[tuple[tuple[str, ...], str]] = []
    stack: list[str] = []
    buf: list[str] = []
    for char in css:
        if char == "{":
            head = " ".join("".join(buf).split())
            heads.append((tuple(stack), head))
            stack.append(head)
            buf = []
        elif char == "}":
            buf = []
            # Clamping instead of raising would silently rebase every later head
            # one level shallower, which flips the classification C2 is built
            # from. Fail loudly, as the sibling walker in
            # tests/test_css_wp4_4_components_contracts.py does.
            assert stack, "unbalanced braces: a stray '}' in the stylesheet"
            stack.pop()
        elif char == ";":
            # A top-level statement such as `@layer a, b, c;` is not a head and
            # must not leak into the next one.
            buf = []
        else:
            buf.append(char)
    assert not stack, f"unbalanced braces: {len(stack)} block(s) left open"
    return heads


def _heads_carrying(css: str, cls: str) -> list[tuple[tuple[str, ...], str]]:
    token = re.compile(rf"\.{re.escape(cls)}(?![\w-])")
    return [(ancestors, head) for ancestors, head in _rule_heads(css) if token.search(head)]


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
    `.tbl-controls, .tbl-toolbar` rule, fails this test.

    The breakpoint-helper half of this assertion is gone: that family was
    certified and deleted by the table-helper re-audit, and its guarantee is now
    carried by C1-C5 below at greater strength. See BREAKPOINT_HELPER_CLASSES.
    """
    css = _css()
    missing = [snippet for snippet in RETAINED_SNIPPETS if snippet not in css]
    assert missing == [], (
        f"layout.css lost rules WP4.4-e explicitly retained: {missing}"
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


# --- Breakpoint-helper family: C1-C5 ------------------------------------------
#
# These replace DEFERRED_HELPER_COUNTS. Its three structural weaknesses, and
# which contract closes each:
#   W1 it pinned a NUMBER, not a state -- `2` could not express "gone"     -> C1
#   W2 it pinned the STYLESHEET, not the app -- it said nothing about
#      whether anything applies the class, which is the premise the whole
#      deletion argument rests on                                          -> C3
#   W3 it pinned ONE FILE -- a sibling bundle could define the class
#      tomorrow and the assertion would stay green                         -> C4
# C2 pins indivisibility, which the count pin only encoded by accident, and C5
# forecloses a residue the count pin had no analogue for.


def test_breakpoint_helper_family_is_absent_from_layout_css() -> None:
    """C1 - no rule head in layout.css carries a breakpoint-helper class.

    One test over all six classes rather than a parametrize: the collected node
    count must not depend on how many classes the tuple happens to hold, because
    `Test Inventory Drift` is a required branch-protection context.

    Red path: re-adding `.tbl-show-md { display: none; }` fails, naming it.
    """
    css = _strip_comments(_css())
    offenders = {
        cls: heads
        for cls in sorted(BREAKPOINT_HELPER_CLASSES)
        if (heads := _heads_carrying(css, cls))
    }
    assert offenders == {}, (
        "layout.css styles breakpoint-helper classes the table-helper re-audit "
        f"certified unreachable and deleted: {offenders}. The family is "
        "indivisible -- if one member became reachable, the deletion must be "
        "revisited with a fresh census and the whole family reinstated, not one "
        "rule re-added."
    )


def test_breakpoint_helper_family_is_all_or_nothing() -> None:
    """C2 - the family is present in full or absent in full, never in part.

    This is the contract the family's indivisibility actually needs, and it is
    outcome-independent: it holds whether the family is deleted or retained. A
    partial state in EITHER direction fails -- `@media` overrides left targeting
    a class with no base rule, or base rules left with no overrides.

    The shape is asserted PER CLASS and PER BAND, not as two totals. Totals are
    too weak in two separate ways, and both were reachable:

    * `(3 base, 6 nested)` is satisfied by three merged rules as readily as by
      nine separate ones, so a restoration collapsing every member into two
      selector lists inside ONE `@media` still summed correctly.
    * Counting only "is it nested" cannot see WHICH query. The three bands are
      the whole point of the family; a restoration that put all six overrides in
      `(max-width: 820px)` would have passed while silently changing what every
      class does at every breakpoint.

    So: each `.tbl-show-*` must have exactly one base rule and one override;
    each `.tbl-hide-*` exactly one override and no base rule; and the sm / md /
    lg overrides must sit under three DISTINCT enclosing preludes.

    Red path (deleted side): adding back only the `@media (max-width: 820px)`
    override, with no base rule, fails here.
    Red paths (present side, proven by restoring all nine): removing any single
    one of the nine fails here, and so does a merged restoration that collapses
    the three bands into one.
    """
    css = _strip_comments(_css())
    shape = {}
    bands: dict[str, set[tuple[str, ...]]] = {}
    for cls in BREAKPOINT_HELPER_CLASSES:
        carried = _heads_carrying(css, cls)
        shape[cls] = (
            sum(1 for ancestors, _ in carried if not ancestors),
            sum(1 for ancestors, _ in carried if ancestors),
        )
        bands[cls] = {ancestors for ancestors, _ in carried if ancestors}

    absent = {cls: (0, 0) for cls in BREAKPOINT_HELPER_CLASSES}
    present = {
        cls: ((1, 1) if cls.startswith("tbl-show-") else (0, 1))
        for cls in BREAKPOINT_HELPER_CLASSES
    }
    assert shape in (absent, present), (
        f"the breakpoint-helper family is in a PARTIAL state: {shape} is neither "
        f"fully absent {absent} nor the complete family {present}. It must be all "
        "nine or none -- a base rule without its override silently changes what "
        "the class does at a breakpoint, and an override without its base rule "
        "targets a class nothing else styles."
    )

    if shape == present:
        per_suffix = {
            suffix: bands[f"tbl-show-{suffix}"] | bands[f"tbl-hide-{suffix}"]
            for suffix in ("sm", "md", "lg")
        }
        assert all(len(v) == 1 for v in per_suffix.values()), (
            f"a breakpoint suffix spans more than one enclosing query: {per_suffix}"
        )
        distinct = {next(iter(v)) for v in per_suffix.values()}
        assert len(distinct) == 3, (
            "the sm / md / lg overrides do not sit in three distinct queries: "
            f"{per_suffix}. Collapsing the bands changes what every member does "
            "at every breakpoint while keeping the counts intact."
        )


def test_breakpoint_helper_classes_are_unreachable() -> None:
    """C3 - nothing in the app applies a breakpoint-helper class.

    This is the premise the deletion rests on, and the one the occurrence-count
    pin never covered (W2). It converts a one-time census into a standing gate:
    adopting one of these classes now fails pytest instead of silently relying
    on a rule that no longer exists.

    The detector is a bare-stem substring scan, and that is deliberately
    *simpler* than `test_deleted_classes_are_still_unreachable`'s parser rather
    than a wider version of it. That test enumerates syntactic forms --
    `class="..."` attributes and `classList.add/toggle/replace` literals -- so it
    cannot see `className =`, `setAttribute('class', ...)`, or a name assembled
    at runtime. Enumerating more forms would only move the boundary. Matching
    `tbl-show` / `tbl-hide` anywhere subsumes all of them at once, including
    `'tbl-show-' + size` and `` `tbl-hide-${size}` ``, which produce a real class
    name while containing no full class literal.

    It can only over-fire, never under-fire, and over-firing is the safe
    direction. Two narrow exemptions keep the over-firing honest rather than
    obstructive, because both are legitimate mentions that apply nothing:
    comments -- the likeliest is a note beside `table-responsiveness.js:112`
    explaining why the family went -- and JS unit tests, which may assert the
    absence of a class by name.

    Red paths: three realistic application shapes were each executed and each
    goes red -- `class="tbl-hide-lg"` in a template, `classList.add('tbl-show-sm')`
    in a module, and `className = 'tbl-show-' + size`. They exercise three
    *shapes*, not three detector branches; one mechanism catches all three, which
    is the point.
    """
    stems = ("tbl-show", "tbl-hide")
    line_comment = re.compile(r"(?<!:)//[^\n]*")
    html_comment = re.compile(r"<!--.*?-->", re.S)

    offenders: list[str] = []
    for base, pattern in ((TEMPLATES, "**/*.html"), (JS, "**/*.js")):
        for path in base.glob(pattern):
            if "__tests__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            text = _strip_comments(text)          # /* ... */
            text = line_comment.sub("", text)     # // ...
            text = html_comment.sub("", text)     # <!-- ... -->
            for stem in stems:
                if stem in text:
                    offenders.append(f"{path.relative_to(ROOT)} mentions '{stem}'")
    assert offenders == [], (
        "the app now references a breakpoint-helper class name, but layout.css "
        f"no longer styles any of them: {offenders}. Nothing will apply. Either "
        "drop the reference or reinstate the whole family with fresh evidence -- "
        "do not re-add a single rule to make one call site work."
    )


def test_breakpoint_helper_classes_have_no_definition_site_in_a_sibling_bundle() -> None:
    """C4 - no other CSS bundle defines a breakpoint-helper class.

    Closes W3. `layout.css` is excluded by name and is owned by C1 instead, at
    the stronger rule-head granularity; that split is what lets this contract
    hold unchanged whether the family is deleted or retained.

    Globbing rather than a hard-coded surface list means a bundle added later is
    covered automatically -- unlike
    `test_deleted_classes_are_not_resurrected_by_a_sibling_surface`, whose five
    surfaces are fixed. One test, not a parametrize over the glob, so the
    collected node count cannot vary with the files present on the machine doing
    the collecting.

    The walk is RECURSIVE over `static/`, not just `static/css/`. The one-time
    census covered `static/vendor/fontawesome/css/all.min.css` -- FontAwesome is
    vendored locally and is a real loaded stylesheet -- so a gate confined to
    `static/css/*.css` would guarantee less than the evidence claimed. `layout.css`
    is excluded by resolved path rather than by bare filename, so a future
    `vendor/**/layout.css` cannot slip through on its name.

    Red path: adding `.tbl-show-sm {}` to components.css fails, naming it.
    """
    offenders: dict[str, list[str]] = {}
    for path in sorted((ROOT / "static").rglob("*.css")):
        if path.resolve() == LAYOUT.resolve():
            continue
        css = _strip_comments(path.read_text(encoding="utf-8"))
        found = [
            cls for cls in sorted(BREAKPOINT_HELPER_CLASSES) if _heads_carrying(css, cls)
        ]
        if found:
            offenders[path.name] = found
    assert offenders == {}, (
        f"a sibling bundle now defines breakpoint-helper classes: {offenders}. "
        "The re-audit certified them unreachable across every loaded stylesheet; "
        "re-creating the family in another bundle reintroduces it without the "
        "evidence."
    )


def test_layout_css_has_no_empty_media_block() -> None:
    """C5 - no `@media` block in layout.css has a whitespace-only body.

    Small, and it forecloses one specific sloppy deletion: removing the nine
    rules while leaving three empty `@media` shells behind. That state passes C1
    and leaves a residue a later reader takes for intentional.

    Scoped to layout.css. A glob-all form would be red on arrival --
    pages-workout-log.css already carries five whitespace-only `@media` blocks
    that WP4.3j-b-dead kept deliberately, with an explanatory comment.

    Red path: leaving `@media (min-width: 1201px) { }` behind fails.
    """
    css = _strip_comments(_css())
    empty = re.findall(r"@media[^{]*\{\s*\}", css)
    assert empty == [], (
        f"layout.css has {len(empty)} empty @media block(s): "
        f"{[' '.join(m.split()) for m in empty]}. An emptied media query is "
        "deletion residue, not a rule."
    )


# --- Separator contrast -------------------------------------------------------
#
# `--tbl-border-color` is the only colour behind the card-mode row separator:
# `.tbl--responsive tr` draws the row-card outline with it, and
# `.tbl--responsive td` draws the divider between label/value pairs inside a
# card with it. In that layout the intra-card divider has no gap, fill change
# or shadow to fall back on, so if the token washes out the fields stop being
# separable.
#
# This is not hypothetical. Until 2026-08-02 the separator rendered at
# `currentColor` -- near-black on light, near-white on dark -- because a
# higher-weight rule was supplying the paint. The WP4.4 cascade cleanup
# (bracketed to 894d882..7685e2b) removed that accidental override, and the
# declared token finally took effect at 1.54:1 / 1.21:1. The rendering became
# correct and the contrast became inadequate in the same change, and nothing in
# the suite noticed either. This contract is the missing half.

TOKEN_SURFACES = ROOT / "static" / "css" / "tokens.css"
MIN_CONTRAST = 3.0  # WCAG 2.2 SC 1.4.11, non-text contrast


def _srgb_to_linear(channel: int) -> float:
    c = channel / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _relative_luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (_srgb_to_linear(int(h[i : i + 2], 16)) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast(a: str, b: str) -> float:
    la, lb = _relative_luminance(a), _relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _declaration(blocks: list[str], name: str) -> str:
    """The winning literal value of a custom property.

    A selector can open more than once in a file, so every block is scanned and
    the last declaration wins -- which is what the cascade does for rules of
    equal specificity.
    """
    found = [
        value
        for block in blocks
        for value in re.findall(rf"{re.escape(name)}\s*:\s*(#[0-9a-fA-F]{{6}})\s*;", block)
    ]
    assert found, f"{name} has no literal hex value in any matching block"
    return found[-1]


def _blocks(css: str, selector_pattern: str) -> list[str]:
    found = re.findall(selector_pattern + r"\s*\{(.*?)\n\}", css, flags=re.S | re.M)
    assert found, f"no rule block matched {selector_pattern!r}"
    return found


@pytest.mark.parametrize(
    ("theme", "layout_selector", "tokens_selector"),
    [
        ("light", r"^:root", r"^:root"),
        ("dark", r'^\[data-theme="dark"\]', r'^\[data-theme="dark"\]'),
    ],
)
def test_table_separator_clears_non_text_contrast(
    theme: str, layout_selector: str, tokens_selector: str
) -> None:
    """The card-mode separator must clear 3:1 against every surface it meets.

    Both surfaces matter, not just the card fill. The row-card outline sits
    between the fill (`--surface-2` on light) and the page behind it
    (`--surface-0`), so the weaker of the two governs. On dark they are the same
    colour, which is precisely why the border is the only row boundary there.

    Red path: restoring `--tbl-border-color: #d0d0d0` (light) or `#374151`
    (dark) fails at 1.54:1 and 1.81:1 respectively.
    """
    layout_css = _strip_comments(_css())
    tokens_css = _strip_comments(TOKEN_SURFACES.read_text(encoding="utf-8"))

    separator = _declaration(_blocks(layout_css, layout_selector), "--tbl-border-color")
    surface_blocks = _blocks(tokens_css, tokens_selector)
    surfaces = {
        name: _declaration(surface_blocks, f"--{name}")
        for name in ("surface-0", "surface-1", "surface-2")
    }

    failures = {
        f"{name} ({value})": round(_contrast(separator, value), 2)
        for name, value in surfaces.items()
        if _contrast(separator, value) < MIN_CONTRAST
    }
    assert failures == {}, (
        f"{theme} --tbl-border-color {separator} falls below "
        f"{MIN_CONTRAST}:1 against {failures}. In card mode this token is the "
        "only divider between label/value pairs inside a row card; weakening it "
        "removes the sole cue that separates them."
    )
