"""WP4.4-a contracts — the measured baseline and the guards that keep it honest.

Per-packet contract file (owner ruling N1: per-packet files permanently, no
consolidation at WP4.4-k). This file is owned by packet **a** alone.

Three things are locked here:

* **F13** — packets b-k cite `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` instead of
  quoting projections. The pin re-derives the per-surface line counts from the
  surfaces **as they were at the baseline's own `sourceCommit`**, so a baseline
  whose recorded numbers never matched the code it claims to describe reds
  pytest rather than being quietly inherited as fact. It deliberately does not
  compare against the working tree: that would couple an immutable measurement
  to every later packet and red on the arc's first authorized deletion.
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
import subprocess
from pathlib import Path

import pytest

from scripts.css_audit import measure, specificity


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "docs" / "CSS_PHASE4_WP4_4_A_BASELINE.json"
SCREENSHOT_ROOT = ROOT / "e2e" / "__screenshots__"

# Baselines committed at WP4.4-a, after N7 added the six `/fatigue` captures.
# A packet that regenerates snapshots moves these numbers and fails here.
# Both platforms drop the same five captures, which are exempt from byte
# comparison and therefore have no baseline file at all: two from visual.spec.ts
# (workout-plan-desktop-{light,dark}) and three from the thumbnails spec
# (plan-desktop-{light,dark}-advanced, plan-desktop-dark-simple). See
# BYTE_GATE_EXEMPT in e2e/visual-helpers.ts and PLANNING.md §8.10.
EXPECTED_SNAPSHOT_COUNTS = {
    "win32/visual.spec.ts-snapshots": 66,
    "win32/visual-baseline-thumbnails.spec.ts-snapshots": 15,
    "linux/visual.spec.ts-snapshots": 66,
    "linux/visual-baseline-thumbnails.spec.ts-snapshots": 15,
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

    # The pin is only meaningful if the commit is in this history. `main` is not
    # checked by name: a worktree or a detached CI checkout has no local `main`.
    # This also fails readably, before `git show` raises CalledProcessError on a
    # missing object or a shallow clone.
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert ancestry.returncode == 0, (
        f"baseline sourceCommit {commit} is not an ancestor of HEAD. A baseline "
        f"pinned to a pre-squash branch commit passes locally and dies on a "
        f"fresh clone; re-pin it to the merged commit. {ancestry.stderr.strip()}"
    )

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


def _helper() -> str:
    return (ROOT / "e2e" / "visual-helpers.ts").read_text(encoding="utf-8")


def _mutated_helper(old: str, new: str) -> str:
    """The live helper with one edit applied, refusing to be a no-op.

    A mutation test whose mutation silently missed is a green test that proves
    nothing, which is the exact failure mode Q10 exists to remove.
    """
    helper = _helper()
    mutated = helper.replace(old, new, 1)
    assert mutated != helper, f"mutation is a no-op: {old!r} is not in the helper"
    return mutated


def _serialized_register() -> list:
    """The live Python register as JSON — the form the baseline must equal."""
    return json.loads(
        json.dumps([dict(entry) for entry in measure.BLIND_SPOT_REGISTER], ensure_ascii=False)
    )


def test_oracle_blind_spot_register_matches_the_live_helper() -> None:
    """F2 — the pixel oracle is blind to the families d/h/i/j are cleaning.

    `prepareForScreenshot()` zeroes transitions and animations, forces
    `backdrop-filter: none`, hides icons and flattens dark surfaces before any
    screenshot is taken. A packet whose declarations fall in this register must
    supply a computed-style differential instead of citing the pixel matrix.

    The committed array must equal the serialized live register **exactly**.
    Comparing lengths was the weaker pin it replaces: it accepted any edit that
    kept the entry count, and it accepted a register whose contents had drifted
    from the helper as long as the count still matched.
    """
    baseline = _baseline()
    register = baseline["oracleBlindSpots"]

    assert measure.verify_blind_spots() == []
    assert register == _serialized_register()

    covered = {packet for entry in register for packet in entry["blindsPackets"]}
    assert {"c", "d", "h", "i", "j"}.issubset(covered)

    properties = {prop for entry in register for prop in entry["properties"]}
    assert "backdrop-filter" in properties
    assert "transition-duration" in properties


def test_the_register_enumerates_every_rule_the_capture_helper_applies() -> None:
    """The whole injected stylesheet is classified, plus the inline stage.

    Two neutralizers reached `prepareForScreenshot()` without ever reaching the
    register — the dark `.summary-header` paint flattening and the sticky-table
    `position: static` demotion — and full pytest stayed green through both,
    because the old check only searched the helper for one substring per entry
    and never asked what the helper contained that the register did not.
    """
    stylesheet = measure.helper_rule_blocks()
    inline = measure.helper_inline_blocks()

    classifications = [block["classification"] for block in stylesheet]
    assert classifications.count(measure.NEUTRALIZER) == 18
    assert classifications.count(measure.SUPPORT_TOKEN) == 2
    assert len(stylesheet) == 20

    # The post-load `setProperty()` stage is a second channel, not a restatement
    # of the stylesheet: inline `!important` outranks every author rule.
    assert len(inline) == 1
    assert all(block["classification"] == measure.NEUTRALIZER for block in inline)

    applied = measure.helper_rules()
    assert {rule["stage"] for rule in applied} == {
        measure.STYLESHEET_STAGE,
        measure.INLINE_STAGE,
    }
    # Order-insensitive on purpose: the register is maintained in helper source
    # order for readability, but a curated regrouping that preserved every
    # record would be a legitimate edit and must not have to red this file.
    assert sorted(map(repr, measure.register_rules())) == sorted(map(repr, applied))

    # Both escaped neutralizers, named, so a future deletion of either has to be
    # a deliberate edit here rather than a silent one there.
    signatures = {
        (rule["stage"], rule["selector"], rule["property"]) for rule in applied
    }
    assert (
        "stylesheet",
        "html[data-theme='dark'] .summary-header",
        "background",
    ) in signatures
    assert any(
        stage == "stylesheet" and prop == "position"
        for stage, _, prop in signatures
    )


# Each case edits `e2e/visual-helpers.ts` in memory and must make
# `verify_blind_spots()` red while *naming* what moved. The helper file itself is
# never written: this packet is test infrastructure and moves no pixel.
BLIND_SPOT_MUTATIONS = [
    pytest.param(
        "      [data-visual-icon] {",
        "      .q10-unregistered { filter: none !important; }\n      [data-visual-icon] {",
        ".q10-unregistered",
        id="a-wholly-new-neutralizer-block",
    ),
    pytest.param(
        "        visibility: hidden !important;",
        "        visibility: hidden !important;\n        opacity: 0 !important;",
        "opacity",
        id="an-extra-property-inside-a-registered-block",
    ),
    pytest.param(
        "      [data-visual-icon] {",
        "      [data-visual-icon], .q10-extra {",
        ".q10-extra",
        id="an-extended-selector",
    ),
    pytest.param(
        "        animation-duration: 0s !important;\n",
        "",
        "animation-duration",
        id="a-registered-declaration-deleted",
    ),
    pytest.param(
        "        backdrop-filter: none !important;\n",
        "",
        "{ backdrop-filter:",
        id="the-unprefixed-backdrop-filter-deleted",
    ),
    pytest.param(
        "      html[data-theme='dark'] {\n"
        "        --visual-surface-0: #090c16;\n"
        "        --visual-surface-1: #0d101d;\n"
        "      }\n",
        "",
        "#090c16",
        id="one-of-the-two-support-token-blocks-deleted",
    ),
    pytest.param(
        "      [data-visual-icon] {",
        "      html[data-theme='sepia'] { --visual-surface-2: #fff; }\n"
        "      [data-visual-icon] {",
        "--visual-surface-2",
        id="an-unregistered-custom-property-only-block",
    ),
    pytest.param(
        "        element.style.setProperty('text-shadow', 'none', 'important');",
        "        element.style.setProperty('text-shadow', 'none', 'important');\n"
        "        element.style.setProperty('outline', 'none', 'important');",
        "outline",
        id="a-new-inline-setProperty-neutralizer",
    ),
    pytest.param(
        "  await page.evaluate(async () => {",
        "  await page.addStyleTag({ content: `.q10-second { opacity: 0 !important; }` });\n"
        "  await page.evaluate(async () => {",
        "addStyleTag",
        id="a-second-injected-stylesheet-fails-closed",
    ),
    pytest.param(
        "        element.style.setProperty('border-radius', '0', 'important');",
        "        element.style.cssText += ';opacity:0';",
        "channel",
        id="an-unenumerated-style-channel-fails-closed",
    ),
    pytest.param(
        "border-color: #273145 !important;",
        "border-color: #111111 !important;",
        "#111111",
        id="a-changed-value",
    ),
    pytest.param(
        "::-webkit-scrollbar { display: none; }",
        "::-webkit-scrollbar { display: none !important; }",
        "important=True",
        id="a-changed-importance",
    ),
]


@pytest.mark.parametrize("old, new, named", BLIND_SPOT_MUTATIONS)
def test_a_helper_mutation_reds_the_blind_spot_contract(
    old: str, new: str, named: str
) -> None:
    """Every way the helper and the register can diverge, in both directions."""
    failures = measure.verify_blind_spots(_mutated_helper(old, new))

    assert failures, "the mutated helper still verifies clean against the register"
    assert any(named in line for line in failures), (
        f"no failure names {named!r}; a red that cannot say what moved is not a "
        f"usable gate. Got: {failures}"
    )


# The element-capture stage, pinned exactly. These declarations are outside
# `BLIND_SPOT_REGISTER` on purpose — the register describes the full-page stage
# every capture shares, and these apply to locator captures only — but they are
# neutralizers in the same file, so an unpinned one would be the same blind spot
# one function further down.
ELEMENT_CAPTURE_RULES = [
    {
        "stage": "stylesheet",
        "selector": "#navbar",
        "property": "visibility",
        "value": "hidden",
        "important": True,
        "classification": "neutralizer",
    },
    {
        "stage": "stylesheet",
        "selector": '.vp-drawer[aria-hidden="true"], .vp-backdrop[hidden]',
        "property": "display",
        "value": "none",
        "important": True,
        "classification": "neutralizer",
    },
]


def test_the_element_capture_stage_adds_no_unpinned_neutralizer() -> None:
    """`prepareForElementScreenshot()` layers a second stylesheet of its own.

    It runs `prepareForScreenshot()` and then hides fixed page chrome so an
    oversized locator capture is not contaminated by it. Nothing in the register
    reaches that stylesheet, so it is enumerated on the same terms and pinned
    here: a neutralizer added to it has to be a deliberate edit to this list.
    """
    assert measure.element_capture_rules() == ELEMENT_CAPTURE_RULES

    registered = {
        (rule["stage"], rule["selector"], rule["property"])
        for rule in measure.register_rules()
    }
    overlap = {
        (rule["stage"], rule["selector"], rule["property"])
        for rule in ELEMENT_CAPTURE_RULES
    } & registered
    assert not overlap, (
        f"the element-capture stage restates a registered rule: {overlap}. One "
        "machine identity cannot describe two stages."
    )


@pytest.mark.parametrize(
    "old, new",
    [
        pytest.param(
            "      #navbar { visibility: hidden !important; }",
            "      #navbar { visibility: hidden !important; }\n"
            "      .q10-element-extra { opacity: 0 !important; }",
            id="a-new-block",
        ),
        pytest.param(
            "      #navbar { visibility: hidden !important; }",
            "      #navbar { visibility: hidden !important; transform: none !important; }",
            id="an-extra-property",
        ),
    ],
)
def test_an_element_capture_addition_moves_its_pin(old: str, new: str) -> None:
    """A neutralizer added to the element stage must not survive the pin."""
    derived = measure.element_capture_rules(_mutated_helper(old, new))

    assert derived != ELEMENT_CAPTURE_RULES, (
        "the element-capture stage gained a declaration without moving its pin"
    )


# The one line unique to `prepareForElementScreenshot()`; anchoring on
# `addStyleTag(` instead would land the mutation in `prepareForScreenshot()`,
# which is a different function and a different contract.
_ELEMENT_ANCHOR = "  await prepareForScreenshot(page);"


@pytest.mark.parametrize(
    "old, new, named",
    [
        pytest.param(
            _ELEMENT_ANCHOR,
            f"{_ELEMENT_ANCHOR}\n  await page.evaluate(() =>\n"
            "    document.body.style.setProperty('zoom', '1', 'important'));",
            "setProperty",
            id="an-inline-stage",
        ),
        pytest.param(
            _ELEMENT_ANCHOR,
            f"{_ELEMENT_ANCHOR}\n  await page.addStyleTag({{ content: "
            "`.q10-first { opacity: 0 !important; }` });",
            "addStyleTag",
            id="a-second-injected-stylesheet",
        ),
        pytest.param(
            _ELEMENT_ANCHOR,
            f"{_ELEMENT_ANCHOR}\n"
            "  await page.evaluate(() => (document.body.style.zoom = '1'));",
            "channel",
            id="an-unenumerated-style-channel",
        ),
    ],
)
def test_an_element_capture_channel_fails_closed(old: str, new: str, named: str) -> None:
    """A style channel the extractor cannot enumerate must raise, not be skipped."""
    with pytest.raises(measure.HelperParseError, match=re.escape(named)):
        measure.element_capture_rules(_mutated_helper(old, new))


def test_an_unrelated_block_is_not_bound_to_the_form_control_entry() -> None:
    """The substring defect, stated as the property it violated.

    The old check matched a register entry to a helper rule by searching the
    rule's text for the entry's evidence string, so the form-control entry's
    `box-shadow: none !important;` claimed the dark `.summary-header` and
    `[data-visual-accent]` blocks — three unrelated rules, one identity. Machine
    identity is now `(stage, selector, property)`, which cannot collide.
    """
    mutated = _mutated_helper(
        "      [data-visual-icon] {",
        "      .q10-unrelated-shadow { box-shadow: none !important; }\n"
        "      [data-visual-icon] {",
    )
    failures = measure.verify_blind_spots(mutated)

    assert any(".q10-unrelated-shadow" in line for line in failures)
    assert not any("form control" in line for line in failures), (
        f"a box-shadow block was associated with the form-control entry: {failures}"
    )


def test_formatting_churn_alone_leaves_the_blind_spot_contract_green() -> None:
    """Comments, blank lines, indentation and CRLF must not be findings.

    A contract that reds on reformatting gets weakened the first time someone
    reformats, so formatting independence is what makes the exact comparison
    above affordable to keep.
    """
    churn = [
        (
            "/* Sticky table cells are promoted into compositor-managed layers.",
            "/* REWORDED. Sticky cells are compositor-promoted.",
        ),
        ("      [data-visual-icon] {", "\n\n          [data-visual-icon]      {"),
        (
            "        visibility: hidden !important;",
            "\tvisibility:   hidden   !important;",
        ),
    ]
    reformatted = _helper()
    for old, new in churn:
        reformatted, applied = reformatted.replace(old, new, 1), reformatted
        assert reformatted != applied, f"formatting churn is a no-op: {old!r}"
    reformatted = reformatted.replace("\n", "\r\n")

    assert measure.verify_blind_spots(reformatted) == []


def test_a_tampered_baseline_entry_reds_even_at_an_unchanged_length() -> None:
    """Why the pin is equality and not `len(...) == len(...)`.

    Both tampered arrays below keep the committed entry count, so the length
    pin this replaces accepted both: one rewrites curated prose, the other
    rewrites a machine-verified value.
    """
    register = _serialized_register()

    reworded = [dict(entry) for entry in register]
    reworded[0] = dict(reworded[0], why="something else entirely")

    revalued = [dict(entry) for entry in register]
    declarations = [dict(item) for item in revalued[0]["declarations"]]
    declarations[0] = dict(declarations[0], value="9s")
    revalued[0] = dict(revalued[0], declarations=declarations)

    for tampered in (reworded, revalued):
        assert len(tampered) == len(measure.BLIND_SPOT_REGISTER)
        assert tampered != register


def test_two_register_entries_cannot_claim_one_machine_signature(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A duplicated identity would make one of the two rules unverifiable."""
    duplicate = dict(measure.BLIND_SPOT_REGISTER[-1])
    monkeypatch.setattr(
        measure, "BLIND_SPOT_REGISTER", measure.BLIND_SPOT_REGISTER + (duplicate,)
    )

    failures = measure.verify_blind_spots()
    assert any("duplicate register signature" in line for line in failures), failures


def test_the_register_mirror_fields_cannot_drift_from_the_declarations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`properties` is a readable mirror, so it must be checked, not trusted."""
    entries = [dict(entry) for entry in measure.BLIND_SPOT_REGISTER]
    entries[0]["properties"] = ["invented-property"]
    monkeypatch.setattr(measure, "BLIND_SPOT_REGISTER", tuple(entries))

    failures = measure.verify_blind_spots()
    assert any("does not mirror" in line for line in failures), failures


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
