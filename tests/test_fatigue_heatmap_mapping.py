"""Contract tests for the /fatigue body heatmap (mapping, palette, plumbing).

The heatmap is a pure visualization of bands `utils/_fatigue/per_muscle.py`
already computes. These tests pin the three things that can rot silently:

  1. the region -> fatigue-muscle mapping, against the regions the SVGs actually
     draw and against `MUSCLE_VOLUME_LANDMARKS`, in both directions;
  2. the band vocabulary shared by Python, the JS module and the SCSS palette;
  3. the server -> client plumbing, including that the embedded JSON cannot
     break out of its <script> block.

No fatigue math is *asserted* here - `tests/test_fatigue.py` owns that.
"""
import json
import re
from pathlib import Path

import pytest

from utils._fatigue.per_muscle import MUSCLE_VOLUME_LANDMARKS, classify_muscle_fatigue
from utils.fatigue_data import build_fatigue_page_context

ROOT = Path(__file__).resolve().parents[1]
HEATMAP_JS = ROOT / "static" / "js" / "modules" / "fatigue-heatmap.js"
FATIGUE_SCSS = ROOT / "scss" / "_fatigue.scss"
COMPILED_BUNDLE = ROOT / "static" / "css" / "bootstrap.custom.min.css"
BODYMAPS = ROOT / "static" / "bodymaps" / "hypertrophy-advanced"
ANTERIOR_SVG = BODYMAPS / "body_anterior.svg"
POSTERIOR_SVG = BODYMAPS / "body_posterior.svg"

BANDS = ("light", "moderate", "heavy", "very_heavy")

DATA_BLOCK_RE = re.compile(
    r'<script type="application/json" id="fatigue-heatmap-data">(.*?)</script>',
    re.DOTALL,
)


def _js_literal(name: str):
    """Parse one exported const from the module.

    The three mapping consts are authored as a strict JSON subset precisely so
    this can be `json.loads` rather than a hand-rolled JS reader. If someone
    reformats them into real JS, this raises instead of silently degrading every
    mapping assertion below into a pass.
    """
    source = HEATMAP_JS.read_text(encoding="utf-8")
    match = re.search(
        rf"export const {name} = (\{{.*?\}}|\[.*?\]);", source, re.DOTALL
    )
    assert match, f"{name} not exported from {HEATMAP_JS.name} in the expected form"
    return json.loads(match.group(1))


@pytest.fixture(scope="module")
def region_to_muscle() -> dict:
    return _js_literal("REGION_TO_MUSCLE")


@pytest.fixture(scope="module")
def unmapped_regions() -> list:
    return _js_literal("UNMAPPED_REGIONS")


@pytest.fixture(scope="module")
def band_class() -> dict:
    return _js_literal("BAND_CLASS")


def _svg_region_keys() -> set:
    keys = set()
    for svg in (ANTERIOR_SVG, POSTERIOR_SVG):
        text = svg.read_text(encoding="utf-8")
        for raw in re.findall(r'data-canonical-muscles="([^"]+)"', text):
            keys.update(part.strip() for part in raw.split(",") if part.strip())
    return keys


def _reachable_bands(muscle: str, mrv: float) -> set:
    step = max(mrv, 1.0) / 200.0
    reachable = set()
    score = 0.0
    while score <= mrv + step:
        reachable.add(classify_muscle_fatigue(muscle, score))
        score += step
    return reachable


# ---------------------------------------------------------------------------
# The mapping
# ---------------------------------------------------------------------------

def test_mapped_muscles_are_exactly_the_landmark_muscles(region_to_muscle):
    """A mapped region must resolve to a muscle the classifier can band.

    Otherwise a region could map to an unranked label (Front-Shoulder,
    Middle-Traps, ...) whose band is always None and render neutral forever
    while looking mapped.
    """
    assert set(region_to_muscle.values()) == set(MUSCLE_VOLUME_LANDMARKS)


def test_mapping_decides_on_exactly_the_regions_the_svgs_draw(
    region_to_muscle, unmapped_regions
):
    """Both directions.

    The pre-council draft claimed an `upper-back` region the SVGs never draw and
    omitted `obliques` entirely. Set equality is what makes that class of error
    impossible to reintroduce.
    """
    declared = set(region_to_muscle) | set(unmapped_regions)
    drawn = _svg_region_keys()

    assert declared - drawn == set(), "mapping names regions the SVGs do not draw"
    assert drawn - declared == set(), "SVGs draw regions the mapping never decides on"


def test_mapped_and_unmapped_are_disjoint(region_to_muscle, unmapped_regions):
    assert set(region_to_muscle) & set(unmapped_regions) == set()


def test_middle_shoulder_colors_both_deltoid_regions(region_to_muscle):
    """Owner-locked: Middle-Shoulder covers front and rear delts."""
    assert region_to_muscle["front-deltoid"] == "Middle-Shoulder"
    assert region_to_muscle["rear-deltoid"] == "Middle-Shoulder"


def test_unranked_shoulder_and_trap_labels_drive_no_region(region_to_muscle):
    """The consequence of that lock, pinned so it stays a decision."""
    painted = set(region_to_muscle.values())
    for label in ("Front-Shoulder", "Rear-Shoulder", "Middle-Traps"):
        assert label not in painted


def test_obliques_and_abs_share_the_abdominals_bucket(region_to_muscle):
    """`External Obliques` canonicalizes to `Abdominals`, so both regions carry
    the same band - otherwise the figure contradicts the bar list."""
    assert region_to_muscle["abs"] == "Abdominals"
    assert region_to_muscle["obliques"] == "Abdominals"


def test_regions_without_a_fatigue_muscle_are_declared_unmapped(unmapped_regions):
    assert set(unmapped_regions) == {"neck", "adductors", "lower-back"}


# ---------------------------------------------------------------------------
# Band vocabulary: Python <-> JS <-> SCSS
# ---------------------------------------------------------------------------

def test_classifier_emits_exactly_the_four_bands():
    emitted = set()
    for muscle, (_mev, _mav_low, _mav_high, mrv) in MUSCLE_VOLUME_LANDMARKS.items():
        emitted |= _reachable_bands(muscle, mrv)
    assert emitted == set(BANDS)


def test_js_band_class_table_covers_the_classifier_output(band_class):
    """`very_heavy` -> `.fatigue-very-heavy`. Getting the underscore/hyphen
    conversion wrong is silent - the region just renders neutral - so the
    mapping is a table and the table is asserted."""
    assert set(band_class) == set(BANDS)
    for band, css_class in band_class.items():
        assert css_class == f"fatigue-{band.replace('_', '-')}"


def test_scss_declares_a_class_for_every_band_and_the_neutral_state(band_class):
    scss = FATIGUE_SCSS.read_text(encoding="utf-8")
    for css_class in band_class.values():
        assert f".{css_class} {{" in scss, f"{css_class} has no SCSS declaration"
    assert ".fatigue-unranked {" in scss


def test_reachable_bands_per_mapped_muscle_are_recorded():
    """Not every muscle can show every color, so color alone is not comparable
    across regions.

    Four muscles have MEV == 0, so `light` is unreachable for them; Abdominals
    additionally has MAV_high == MRV, so `heavy` is unreachable too. This
    records current shipped behavior of `MUSCLE_VOLUME_LANDMARKS` rather than
    constraining it - and it is the reason each region carries its percentage in
    the hover title instead of relying on color. A landmark change should update
    this list deliberately, with the heatmap copy re-reviewed.
    """
    cannot_show_light = set()
    cannot_show_heavy = set()
    for muscle, (_mev, _mav_low, _mav_high, mrv) in MUSCLE_VOLUME_LANDMARKS.items():
        reachable = _reachable_bands(muscle, mrv)
        if "light" not in reachable:
            cannot_show_light.add(muscle)
        if "heavy" not in reachable:
            cannot_show_heavy.add(muscle)

    assert cannot_show_light == {"Glutes", "Abdominals", "Traps", "Forearms"}
    assert cannot_show_heavy == {"Abdominals"}


# ---------------------------------------------------------------------------
# CSS containment - the compiled bundle loads on every page
# ---------------------------------------------------------------------------

def test_muscle_region_rules_in_the_shared_bundle_are_heatmap_scoped():
    """`bootstrap.custom.min.css` is linked from base.html on every page.

    An unscoped `.muscle-region` rule would reach the workout-plan selector and
    the profile coverage map, leaking exactly the properties those consumers do
    not themselves declare. This makes the scoping mechanical, not a convention.
    """
    bundle = COMPILED_BUNDLE.read_text(encoding="utf-8", errors="replace")
    occurrences = list(re.finditer(r"\.muscle-region", bundle))
    assert occurrences, "heatmap region rules are missing from the compiled bundle"
    for match in occurrences:
        prefix = bundle[max(0, match.start() - 17):match.start()]
        assert prefix.endswith(".fatigue-heatmap "), (
            "unscoped .muscle-region rule in the globally-loaded bundle: "
            f"...{prefix}.muscle-region..."
        )


def test_heatmap_region_paint_declares_no_animated_property():
    """The visual harness neutralises animation with a global stylesheet, but its
    inline pass only reaches form controls. A region that transitioned would be
    the one thing still moving under a screenshot, so the paint is static by
    construction. The plan-page copy of these rules does animate - deliberately
    not shared."""
    scss = FATIGUE_SCSS.read_text(encoding="utf-8")
    block = scss.split(".fatigue-heatmap .muscle-region {", 1)
    assert len(block) == 2, "heatmap region rule not found"
    body = block[1].split("}", 1)[0]
    for forbidden in ("transition", "filter", "box-shadow", "animation"):
        assert forbidden not in body


def test_heatmap_scss_never_names_base_owned_text_utilities():
    """`.text-muted` / `.text-center` / `.text-danger` must not ship in the
    Bootstrap build - `tests/test_css_wp4_4_base_contracts.py` asserts base.css
    is their only source, and a descendant rule here would break that."""
    scss = FATIGUE_SCSS.read_text(encoding="utf-8")
    for name in (".text-center", ".text-muted", ".text-danger"):
        assert name not in scss


def test_body_outline_keeps_the_flat_gray_fill():
    """Owner-locked: the current flat-gray head, no cosmetic demo hair."""
    for svg in (ANTERIOR_SVG, POSTERIOR_SVG):
        text = svg.read_text(encoding="utf-8")
        assert 'class="body-outline"' in text
        assert "#d9dee4" in text


# ---------------------------------------------------------------------------
# Module hygiene
# ---------------------------------------------------------------------------

def test_module_does_not_borrow_the_profile_annotator():
    """`annotateBodymapPolygons` writes Profile-specific `data-bodymap-*` from a
    different mapping; the heatmap owns its own annotation."""
    source = HEATMAP_JS.read_text(encoding="utf-8")
    assert "annotateBodymapPolygons" not in source
    assert "loadBodymapSvg" in source


def test_module_places_muscle_labels_without_innerhtml():
    """`canonicalize_muscle_for_fatigue` passes unknown catalog labels through
    verbatim, so a muscle name is an arbitrary database string. The only
    sanctioned innerHTML is the first-party SVG asset."""
    source = HEATMAP_JS.read_text(encoding="utf-8")
    assignments = re.findall(r"\.innerHTML\s*=\s*([^;]+);", source)
    assert assignments == ["svgText"], (
        f"unexpected innerHTML assignment(s): {assignments}"
    )


# ---------------------------------------------------------------------------
# Server -> client plumbing
# ---------------------------------------------------------------------------

class TestHeatmapDataBlock:
    def test_absent_on_the_empty_state(self, client):
        response = client.get("/fatigue")
        assert response.status_code == 200
        assert b'id="fatigue-heatmap-data"' not in response.data
        assert b'data-testid="fatigue-empty-state"' in response.data
        # The visual harness waits on this attribute; rendering it only when
        # data exists would turn a seed change into an opaque marker timeout on
        # all six /fatigue baselines.
        assert b'data-heatmap-state="empty"' in response.data

    def test_panel_renders_even_when_nothing_aggregates_to_a_bar(
        self, client, exercise_factory, workout_plan_factory
    ):
        """The panel gates on raw row counts, the JS on aggregated bars.

        A plan row whose sets resolve to 0 satisfies the first and not the
        second, so the panel renders around an empty `muscle_rows`. The client
        has to reach a terminal state from there rather than sitting at
        `pending` forever, which would strand the visual harness.

        Covered here rather than in E2E because the app's own endpoints
        cannot produce it: `/add_exercise` rejects `sets: 0` and
        `/clear_workout_plan` deletes the dependent log rows first. It is
        still reachable at the database level - a restored backup, or a
        direct edit - so the client guard is not dead code.
        """
        exercise_factory("Zero Sets Row", primary_muscle_group="Chest")
        workout_plan_factory(exercise_name="Zero Sets Row", sets=0)

        response = client.get("/fatigue")
        html = response.data.decode("utf-8")
        assert 'data-heatmap-state="pending"' in html
        assert 'data-testid="fatigue-heatmap-nodata"' in html
        match = DATA_BLOCK_RE.search(html)
        assert match, "panel rendered without its data block"
        assert json.loads(match.group(1)) == []

    def test_data_page_starts_pending_so_the_marker_is_not_premature(
        self, client, exercise_factory, workout_plan_factory
    ):
        exercise_factory("Bench Press", primary_muscle_group="Chest")
        workout_plan_factory(exercise_name="Bench Press", sets=4)
        response = client.get("/fatigue")
        assert b'data-heatmap-state="pending"' in response.data
        assert b'data-testid="fatigue-heatmap"' in response.data

    def test_region_caveat_renders_once_and_includes_middle_traps(
        self, client, exercise_factory, workout_plan_factory
    ):
        exercise_factory("Bench Press", primary_muscle_group="Chest")
        workout_plan_factory(exercise_name="Bench Press", sets=4)

        response = client.get("/fatigue")
        html = response.data.decode("utf-8")

        assert html.count("Shoulder regions show Middle-Shoulder") == 1
        assert "the upper-back region shows Traps" in html
        assert "Front-Shoulder, Rear-Shoulder and Middle-Traps" in html

    def test_embedded_json_matches_the_context_muscle_rows(
        self, client, exercise_factory, workout_plan_factory
    ):
        exercise_factory(
            "Bench Press",
            primary_muscle_group="Chest",
            secondary_muscle_group="Triceps",
            tertiary_muscle_group="Front-Shoulder",
        )
        workout_plan_factory(exercise_name="Bench Press", sets=4)

        response = client.get("/fatigue")
        assert response.status_code == 200
        match = DATA_BLOCK_RE.search(response.data.decode("utf-8"))
        assert match, "heatmap data block missing when planned data exists"
        assert json.loads(match.group(1)) == build_fatigue_page_context(None)["muscle_rows"]

    def test_muscle_label_cannot_break_out_of_the_script_block(
        self, client, exercise_factory, workout_plan_factory
    ):
        hostile = "</script><script>window.__x=1</script>"
        exercise_factory("Hostile Row", primary_muscle_group=hostile)
        workout_plan_factory(exercise_name="Hostile Row", sets=3)

        response = client.get("/fatigue")
        match = DATA_BLOCK_RE.search(response.data.decode("utf-8"))
        assert match, "heatmap data block missing"
        payload = match.group(1)
        assert "</script>" not in payload
        assert "\\u003c" in payload
        # ...and the label still round-trips intact once parsed.
        assert any(row["muscle"] == hostile for row in json.loads(payload))
