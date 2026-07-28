"""WP4.4-b contracts — `static/css/base.css` after the dead-rule deletion.

Per-packet contract file (owner ruling N1). Owned by packet **b** alone.

WP4.4-b deleted four blocks for two different reasons, and the distinction is
what these contracts exist to preserve:

* `.skeleton` and `@keyframes skeleton-loading` were **cascade non-winners**.
  `motion.css` declares `.skeleton` at equal specificity and loads after
  `base.css`, so every declaration base.css wrote was already overridden.

* `.loading-spinner`, `.fade-enter` and `.fade-enter-active` were **unreachable**.
  The rules worked — a synthetic element carrying the class was painted by them —
  but no element anywhere in the app ever carries the class. Same precedent as
  WP4.3i-filter-btn, which deleted five rules gated on a `#filter-btn` that does
  not exist.

The second reason is the fragile one. An unreachable rule becomes reachable the
moment somebody adds the class name to a template, so the deletion is only sound
while the class stays absent. `test_deleted_classes_are_still_unreachable` is
what makes that a gate rather than an assumption.

The retention half matters just as much: three claims inherited from
`docs/scan/PHASE_20.md` were re-measured for this packet and found **false**.
`@keyframes fadeIn` and the three `.text-*` utilities were all documented as
dead and are all live. They are pinned below so the next packet does not act on
the stale claim.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSS_DIR = ROOT / "static" / "css"
BASE = (CSS_DIR / "base.css").read_text(encoding="utf-8")
LAYOUT = (CSS_DIR / "layout.css").read_text(encoding="utf-8")
MOTION = (CSS_DIR / "motion.css").read_text(encoding="utf-8")

# Every file that can put a class into the DOM. CSS is excluded on purpose:
# a class named only in a stylesheet is exactly what "unreachable" means.
REACHABILITY_GLOBS = ("templates/**/*.html", "static/js/**/*.js")

DELETED_CLASSES = ("loading-spinner", "fade-enter", "fade-enter-active")


def _rule_exists(selector: str, css: str) -> bool:
    """True if a top-level rule opens with exactly this selector."""
    return re.search(rf"(?m)^{re.escape(selector)}\s*\{{", css) is not None


def _reachability_hits(name: str) -> list[str]:
    hits = []
    for glob in REACHABILITY_GLOBS:
        for path in ROOT.glob(glob):
            if name in path.read_text(encoding="utf-8", errors="replace"):
                hits.append(str(path.relative_to(ROOT)))
    return hits


def test_cascade_dead_skeleton_block_stays_deleted() -> None:
    """`base.css`'s `.skeleton` lost all three of its declarations to `motion.css`.

    `motion.css` loads at `templates/base.html:27`, `base.css` at `:19`, and both
    declare `.skeleton` at specificity (0,1,0) — so the later file wins every
    property the earlier one sets. base.css set `background`, `background-size`
    and `animation`; motion.css sets all three plus `border-radius`, `color` and
    `border-color`.

    Measured, not inferred: a synthetic `.skeleton` element on all 11 routes in
    both themes read `animation-name: skeleton-shimmer` (motion.css) and never
    `skeleton-loading` (base.css), and its `background-image` resolved to
    motion.css's `var(--surface-1)`/`var(--surface-2)` gradient rather than
    base.css's `#f0f0f0`/`#e0e0e0` literals. Deleting a non-winner cannot change
    a computed value (M8).
    """
    assert not _rule_exists(".skeleton", BASE)
    assert "@keyframes skeleton-loading" not in BASE
    assert "skeleton-loading" not in BASE


def test_motion_css_still_owns_the_skeleton_family() -> None:
    """The premise of the deletion above, pinned in the file that supplies it.

    If a later packet deletes `motion.css`'s `.skeleton`, the skeleton loader
    silently loses all its paint — base.css no longer carries a fallback. That
    would be a regression introduced by a packet that never opens `base.css`,
    which is precisely the failure mode a cross-file contract catches.
    """
    assert _rule_exists(".skeleton", MOTION)
    assert "@keyframes skeleton-shimmer {" in MOTION
    assert "animation: skeleton-shimmer" in MOTION


def test_unreachable_classes_stay_deleted() -> None:
    """The three rules that worked but matched nothing."""
    for name in DELETED_CLASSES:
        assert not _rule_exists(f".{name}", BASE), f".{name} must stay deleted"


def test_deleted_classes_are_still_unreachable() -> None:
    """The live half of the unreachability claim — this one can rot.

    A census across all 11 routes in both themes found **0** elements carrying
    any of these classes. That census is a point-in-time measurement; this
    assertion is what keeps it true. If someone adds `class="loading-spinner"`
    to a template, this test fails and tells them the CSS backing it was
    deliberately removed, instead of leaving them with a silently unstyled
    element.
    """
    for name in DELETED_CLASSES:
        hits = _reachability_hits(name)
        assert not hits, (
            f"{name!r} is now referenced in {hits}, but WP4.4-b deleted the rule "
            f"that styled it as unreachable. Restore the rule or drop the reference."
        )


def test_fadein_keyframes_are_retained_and_still_consumed() -> None:
    """A correction to `docs/scan/PHASE_20.md`, pinned so it is not re-made.

    That scan listed `@keyframes fadeIn` as dead, on the reasoning that it backed
    the `.fade-enter*` classes it had just found unreferenced. It does not:
    `.fade-enter-active` animates via `transition`, and the real consumer of the
    keyframe is `layout.css`, which is a different file and very much live.
    Deleting it with the `.fade-enter*` block would have broken that animation.
    """
    assert "@keyframes fadeIn {" in BASE
    assert "animation: fadeIn" in LAYOUT


def test_bootstrap_text_utilities_are_retained() -> None:
    """The other correction: these are not redundant with Bootstrap.

    `docs/scan/PHASE_20.md` called them duplicates of Bootstrap's own utilities
    and therefore safe to drop. The compiled `bootstrap.custom.min.css` in this
    repo contains **no** `.text-center`, `.text-muted` or `.text-danger` rule —
    the custom build excludes that part of the utilities API — so base.css is
    their only source. The census found 40 live `.text-muted` elements across the
    route matrix.
    """
    bootstrap = (CSS_DIR / "bootstrap.custom.min.css").read_text(
        encoding="utf-8", errors="replace"
    )
    for name in (".text-center", ".text-muted", ".text-danger"):
        assert _rule_exists(name, BASE), f"{name} is base.css's only definition"
        assert not re.search(rf"{re.escape(name)}\s*[,{{]", bootstrap), (
            f"{name} now also ships in the Bootstrap build; re-measure ownership "
            f"before treating base.css's copy as authoritative"
        )


def test_element_defaults_and_tokens_are_retained() -> None:
    """The rest of the file was measured live and stays.

    The `:root` block is additionally protected by M9: no packet in this arc may
    delete a custom-property declaration under the non-winner rule, because
    resolving a `var()` dependency graph across all 21 hand-maintained sources is
    out of scope for a single-file packet.
    """
    for selector in ("body", "h1, h2, h3", "h2", "h3", "p, label"):
        assert _rule_exists(selector, BASE), f"{selector} must be retained"

    for token in (
        "--bs-border-color",
        "--bs-table-border-color",
        "--glass-blur",
        "--glass-bg",
        "--glass-bg-hover",
        "--glass-border",
        "--glass-shadow",
        "--glass-shadow-hover",
        "--glass-inset",
        "--type-body",
        "--type-h2",
        "--type-h3",
    ):
        assert f"{token}:" in BASE, f"{token} is a custom property; M9 forbids deleting it"


def test_base_css_remains_important_free_and_unlayered() -> None:
    """V3 and N2, measured against the WP4.4-a baseline.

    base.css carried 0 `!important` occurrences at baseline and must still carry
    0 — this packet deletes only, so any appearance would be a rewrite in
    disguise. `@layer` membership is frozen arc-wide by N2, and base.css declares
    no layer at all, which is what lets this packet reason in plain source order.
    """
    assert "!important" not in BASE
    assert "@layer" not in BASE
