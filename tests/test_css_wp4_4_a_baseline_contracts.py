"""WP4.4-a contracts — the measured baseline and the guards that keep it honest.

Per-packet contract file (owner ruling N1: per-packet files permanently, no
consolidation at WP4.4-k). This file is owned by packet **a** alone.

Three things are locked here:

* **F13** — packets b-k cite `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` instead of
  quoting projections. The pin re-derives the per-surface line counts from disk,
  so a baseline that has drifted from the code reds pytest rather than being
  quietly inherited as fact.
* **F12** — V2 ("no rebaseline") and R3 condition 6 were honour-system. A
  manifest over the committed screenshot trees turns an accidental
  `--update-snapshots` into a pytest red, instead of a Playwright green.
* **M4** — the specificity model the whole arc's ownership reasoning rests on
  must agree with its hand-computed cases before any packet uses it.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from scripts.css_audit import measure, specificity


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "docs" / "CSS_PHASE4_WP4_4_A_BASELINE.json"
SCREENSHOT_ROOT = ROOT / "e2e" / "__screenshots__"

# Baselines committed at WP4.4-a, after N7 added the six `/fatigue` captures.
# A packet that regenerates snapshots moves these numbers and fails here.
EXPECTED_SNAPSHOT_COUNTS = {
    "win32/visual.spec.ts-snapshots": 66,
    "win32/visual-baseline-thumbnails.spec.ts-snapshots": 18,
    "linux/visual.spec.ts-snapshots": 66,
    "linux/visual-baseline-thumbnails.spec.ts-snapshots": 18,
}

SEVEN_SURFACES = (
    "motion.css",
    "base.css",
    "layout.css",
    "components.css",
    "navbar.css",
    "theme-dark.css",
    "a11y.css",
)


def _baseline() -> dict:
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def test_wp4_4_baseline_is_pinned_and_matches_its_source_commit() -> None:
    """The baseline's per-surface counts equal the surfaces AT ITS OWN COMMIT.

    This is the gate that makes "no later packet may inherit a projection as
    fact" mechanical. Plan v1 projected 2,681 Stylelint warnings across the
    seven surfaces and 1,787 for components.css; the measured values are 2,883
    and 1,989. Prose could not have caught that.

    Checked against `sourceCommit` rather than the working tree. A baseline
    claims "these were the counts when I measured them", and that is what makes
    it citable; comparing it to HEAD instead couples it to every later packet,
    so the arc's first legitimate deletion reds it — WP4.4-c hit exactly that
    and fixed the semantics here. The `git show` form is also the stronger
    check: it cannot be satisfied by editing the CSS and the JSON together.
    """
    baseline = _baseline()

    assert baseline["packet"] == "WP4.4-a"
    commit = baseline["sourceCommit"]
    assert re.fullmatch(r"[0-9a-f]{40}", commit)

    total = 0
    for name in SEVEN_SURFACES:
        recorded = baseline["surfaces"][name]
        at_commit = measure.counts_from_text(measure.surface_text_at(commit, name))
        assert recorded["lines"] == at_commit["lines"], name
        assert (
            recorded["importantDeclarations"] == at_commit["importantDeclarations"]
        ), name
        total += at_commit["lines"]

    assert baseline["totals"]["sharedSurfaceLines"] == total


def test_important_is_counted_in_reconcilable_units() -> None:
    """F15 — the plan counted `!important` in two units without saying so.

    `theme-dark.css` carries the literal text "Zero !important." inside a
    comment, so the raw line/occurrence counts over-count by exactly one against
    Stylelint's `declaration-no-important`. V3 gates on the declaration count;
    this test keeps the three units reconciled so a packet cannot satisfy one
    while moving another.
    """
    baseline = _baseline()
    stylelint = baseline["stylelintSevenSurfaces"]

    declarations = baseline["totals"]["importantDeclarations"]
    assert declarations == stylelint["byRule"]["declaration-no-important"]
    assert baseline["totals"]["importantLines"] == declarations + 1

    theme_dark = (ROOT / "static" / "css" / "theme-dark.css").read_text(encoding="utf-8")
    assert "Zero !important. */" in theme_dark


def test_layer_membership_is_recorded_exactly_and_frozen() -> None:
    """N2 freezes `@layer` membership arc-wide, which needs exact spans.

    Layered normal declarations lose to every unlayered one and layered
    `!important` wins over every unlayered one, so moving a rule across a layer
    boundary flips precedence in opposite directions depending on importance.
    """
    baseline = _baseline()
    layers = baseline["layers"]

    assert layers["frozenForArc"] is True
    assert layers["order"] == ["workout", "navbar", "workout-dropdowns", "welcome"]
    assert layers["orderDeclaredIn"] == "static/css/tokens.css"

    for filename, spans in layers["spans"].items():
        assert spans == measure.layer_spans(filename), filename

    # The two layered blocks inside surfaces this arc owns.
    assert layers["spans"]["components.css"] == [
        {"layer": "workout", "openLine": 3539, "closeLine": 4104}
    ]
    assert layers["spans"]["navbar.css"] == [
        {"layer": "navbar", "openLine": 6, "closeLine": 883}
    ]


def test_is_family_enumeration_is_complete_and_classified() -> None:
    """A10 / R3 condition 1 — the family must be closed, not sampled.

    19 `:is(` tokens resolve to 17 rules, because two rules each spread their
    selector list over two lines (`:3335`+`:3336`, `:3749`+`:3750`). The split
    matters: only the twelve four-branch rules plus the three-branch
    reduced-motion rule leak ID weight across branches that do not carry it.
    """
    baseline = _baseline()
    family = baseline["isFamily"]

    assert family["totalIsTokens"] == 19
    assert family["distinctRules"] == 17
    assert family["fourBranchTokens"] == 13
    assert family["fourBranchRules"] == 12
    assert family["threeBranchRules"] == 1
    assert family["sixBranchRules"] == 4

    leaking = [record for record in family["records"] if record["exportsIdWeight"]]
    # Twelve four-branch rules (13 tokens) + the reduced-motion rule.
    assert len(leaking) == 14
    assert len({record["ruleLine"] for record in leaking}) == 13

    reduced_motion = [
        record
        for record in family["records"]
        if record["ruleLine"] == 4433
    ]
    assert len(reduced_motion) == 1
    assert reduced_motion[0]["isArgumentBranchCount"] == 3
    assert reduced_motion[0]["enclosingAtRules"] == [
        "@media (prefers-reduced-motion: reduce)"
    ]

    # The six-branch `input.input-calm-inset:is(#weight, #sets, …)` construct is
    # all-ID, so it exports nothing across branches, and it sits inside
    # `@layer workout` where it loses to every unlayered normal declaration.
    six_branch = [
        record for record in family["records"] if record["isArgumentBranchCount"] == 6
    ]
    assert all(record["exportsIdWeight"] is False for record in six_branch)
    assert all(record["enclosingAtRules"] == ["@layer workout"] for record in six_branch)


def test_specificity_model_agrees_with_its_hand_computed_cases() -> None:
    """M4 — the model is unit-checked before any packet reasons with it."""
    assert specificity.self_check() == []
    assert len(specificity.SELF_CHECK_CASES) >= 17
    assert len(specificity.SPLIT_SELF_CHECK_CASES) >= 3

    # The two cases the whole `:is()` repair turns on.
    assert str(specificity.selector_list_specificity(":is(#workout, .log)")) == "(1,0,0)"
    assert str(specificity.selector_list_specificity(":where(#workout, .log)")) == "(0,0,0)"


def test_oracle_blind_spot_register_matches_the_live_helper() -> None:
    """F2 — the pixel oracle is blind to the families d/h/i/j are cleaning.

    `prepareForScreenshot()` zeroes transitions and animations, forces
    `backdrop-filter: none`, hides icons and flattens dark surfaces before any
    screenshot is taken. A packet whose declarations fall in this register must
    supply a computed-style differential instead of citing the pixel matrix.
    """
    baseline = _baseline()
    register = baseline["oracleBlindSpots"]

    assert measure.verify_blind_spots() == []
    assert len(register) == len(measure.BLIND_SPOT_REGISTER)

    covered = {packet for entry in register for packet in entry["blindsPackets"]}
    assert {"c", "d", "h", "i", "j"}.issubset(covered)

    properties = {prop for entry in register for prop in entry["properties"]}
    assert "backdrop-filter" in properties
    assert "transition-duration" in properties


def test_snapshot_manifest_makes_an_accidental_rebaseline_a_pytest_red() -> None:
    """F12 — V2 was honour-system; `--update-snapshots` is one command.

    A rebaseline turns a Playwright failure green. This manifest makes it turn
    pytest red instead, so the packet has to stop and escalate rather than
    quietly absorbing a visual difference it was supposed to explain.
    """
    baseline = _baseline()
    manifest = baseline["snapshotManifest"]

    for relative, expected in EXPECTED_SNAPSHOT_COUNTS.items():
        directory = SCREENSHOT_ROOT / relative
        actual = sorted(path.name for path in directory.glob("*.png"))
        assert len(actual) == expected, f"{relative}: {len(actual)} != {expected}"
        assert manifest[relative]["count"] == expected
        assert manifest[relative]["files"] == actual

        digest = hashlib.sha256()
        for name in actual:
            digest.update(name.encode("utf-8"))
            digest.update(str((directory / name).stat().st_size).encode("utf-8"))
        assert manifest[relative]["nameAndSizeSha256"] == digest.hexdigest(), relative


def test_fatigue_baselines_exist_on_both_platforms() -> None:
    """N7 — creation on both platforms, all-or-nothing per platform.

    Windows generated locally; Linux generated by the `visual-linux` deep-gate
    job (`run_visual=true`, `visual_mode=generate`) and copied in file-by-file.
    The all-or-nothing assertion is what keeps a half-created set from looking
    finished.
    """
    baseline = _baseline()
    fatigue = baseline["fatigueBaselines"]

    win32 = SCREENSHOT_ROOT / "win32" / "visual.spec.ts-snapshots"
    linux = SCREENSHOT_ROOT / "linux" / "visual.spec.ts-snapshots"
    expected = [
        f"fatigue-{viewport}-{theme}.png"
        for viewport in ("mobile", "tablet", "desktop")
        for theme in ("light", "dark")
    ]

    assert all((win32 / name).is_file() for name in expected)
    assert fatigue["win32"] == "created"

    linux_present = [name for name in expected if (linux / name).is_file()]
    assert fatigue["linux"] == ("created" if len(linux_present) == 6 else "pending")
    assert len(linux_present) in (0, 6)


def test_contract_anchor_register_covers_every_shared_surface() -> None:
    """A8 + F6 — each packet must know its ceiling before it starts.

    The shared cascade contract pins literal strings *inside* the surfaces b-f
    own, so "proven disjoint at the file level" was already false for them. Only
    packet **i** may amend that file, and only to re-express the same premise
    (N6); every other packet runs it and never edits it.
    """
    baseline = _baseline()
    anchors = baseline["contractAnchors"]
    pins = baseline["pinnedDeclarations"]

    assert anchors == measure.contract_anchors()
    assert pins == measure.pinned_declarations()

    bound = {surface for anchor in anchors for surface in anchor["surfaces"]}
    for surface in ("navbar.css", "a11y.css", "theme-dark.css", "components.css"):
        assert surface in bound, surface

    # F6's named examples, still present.
    pinned_strings = {pin["pinnedString"] for pin in pins}
    assert "--nav-gap: var(--s-3);" in pinned_strings
    assert "*:focus-visible," in pinned_strings

    # G9 — the Region H block stays locked byte-for-byte.
    cascade = (ROOT / "tests" / "test_css_cascade_contracts.py").read_text(
        encoding="utf-8"
    )
    assert "REGION_H_SHA256" in cascade
