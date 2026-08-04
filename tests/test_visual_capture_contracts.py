"""Determinism contracts for the visual-regression capture pipeline.

Three defects made the 84-baseline visual suite nondeterministic across runs of
the identical CI job at the identical SHA. Two of them are checkable from Python
and are locked here; the third (media readiness) is a capture-time property and
lives in ``e2e/visual-helpers.ts``.

**The startup race.** ``e2e/fixtures/database.visual.seed.db`` has no
``youtube_video_id`` column. ``prepare_visual_db.py`` snapshots it and runs
``run_all_initializers()``, which ``ALTER TABLE``s the column in as all NULL.
``app.py`` startup *then* runs ``upgrade_catalog_from_seed()``, which takes about
1.6 s and populates 56 curated ids. Playwright's ``webServer`` readiness only
waits for the TCP port, so any page served inside that window renders the
uncurated branch of ``buildPlayButton`` (a magnifier icon) while a page served
after it renders the curated branch (a play icon). Four of the six seeded plan
exercises are curated, so every plan-bearing baseline had two legal renderings.
The fix is to finish the catalog upgrade *before* the server starts.

**The Chromium surface limit.** A capture taller than 16,384 px does not fail —
it silently truncates to a flat, unpainted tail. Two committed baselines
(``user-profile-mobile-dark``/``-light``, 19,785 px and 19,742 px) truncate at
row 16,392, so the bottom 3,393 px (17.1%) of the mobile Profile page has never
been exercised in either theme.
"""
from __future__ import annotations

import re
import shutil
import sqlite3
import struct
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_ROOT = REPO_ROOT / "e2e" / "__screenshots__"
VISUAL_SEED = REPO_ROOT / "e2e" / "fixtures" / "database.visual.seed.db"
CATALOG_SEED = REPO_ROOT / "data" / "catalog.seed.db"
PREPARE_VISUAL_DB = REPO_ROOT / "e2e" / "scripts" / "prepare_visual_db.py"
PREPARE_E2E_DB = REPO_ROOT / "e2e" / "scripts" / "prepare_e2e_db.py"
PLAYWRIGHT_CONFIG = REPO_ROOT / "playwright.config.ts"
VISUAL_HELPER = REPO_ROOT / "e2e" / "visual-helpers.ts"
FONT_AWESOME_ROOT = REPO_ROOT / "static" / "vendor" / "fontawesome"

# Chromium cannot allocate a capture surface taller than this. Keep in step with
# MAX_CAPTURE_HEIGHT_PX in e2e/visual-helpers.ts.
MAX_CAPTURE_HEIGHT_PX = 16_384

CURATED_ID_SQL = (
    "SELECT COUNT(*) FROM exercises "
    "WHERE youtube_video_id IS NOT NULL AND TRIM(youtube_video_id) <> ''"
)
POPULATED_MEDIA_SQL = (
    "SELECT COUNT(*) FROM exercises "
    "WHERE media_path IS NOT NULL AND TRIM(media_path) <> ''"
)

# Baselines that the segmented user-profile capture retires but whose platform
# has not yet been regenerated. Linux is regenerated and reviewed in #281;
# Windows remains an independent owner-local baseline workflow.
#
# The assertion below is a strict *equality*, not an allowlist, and that is the
# point. A new oversized baseline fails it, and so does a stale entry: once the
# regeneration step replaces a platform's two names with ``-segment-N`` files,
# its relative paths disappear from this set. Once both platforms are current,
# the set becomes empty. Do not add anything here to silence a real capture.
AWAITING_SEGMENTED_REGENERATION = {
    "win32/visual.spec.ts-snapshots/user-profile-mobile-dark.png",
    "win32/visual.spec.ts-snapshots/user-profile-mobile-light.png",
}


def _png_size(path: Path) -> tuple[int, int]:
    """Return ``(width, height)`` from a PNG IHDR chunk."""
    header = path.read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"Not a PNG: {path}")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def _committed_baselines() -> list[Path]:
    return sorted(SCREENSHOT_ROOT.rglob("*.png"))


def _run_seeder(script: Path, output: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(script), "--output", str(output)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, (
        f"{script.name} failed ({result.returncode}):\n"
        f"{result.stdout}\n{result.stderr}"
    )


def _scalar(database: Path, sql: str) -> int:
    with sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True) as db:
        return int(db.execute(sql).fetchone()[0])


def _columns(database: Path, table: str) -> set[str]:
    with sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True) as db:
        return {row[1] for row in db.execute(f"PRAGMA table_info({table})")}


@pytest.fixture(scope="module")
def prepared_visual_db(tmp_path_factory) -> Path:
    output = tmp_path_factory.mktemp("visual-seed") / "database.visual.db"
    _run_seeder(PREPARE_VISUAL_DB, output)
    return output


@pytest.fixture(scope="module")
def prepared_e2e_db(tmp_path_factory) -> Path:
    output = tmp_path_factory.mktemp("e2e-seed") / "database.e2e.db"
    _run_seeder(PREPARE_E2E_DB, output)
    return output


# --------------------------------------------------------------------------
# Chromium surface limit
# --------------------------------------------------------------------------


def test_no_committed_visual_baseline_exceeds_the_chromium_surface_limit():
    """A capture over 16,384 px truncates to a blank tail instead of failing.

    Nothing in Playwright or Chromium reports this, so the only place it can be
    caught is the committed corpus.
    """
    baselines = _committed_baselines()
    assert baselines, f"No committed baselines found under {SCREENSHOT_ROOT}"

    oversized = {}
    for path in baselines:
        width, height = _png_size(path)
        if max(width, height) > MAX_CAPTURE_HEIGHT_PX:
            relative = path.relative_to(SCREENSHOT_ROOT).as_posix()
            oversized[relative] = (width, height)

    assert set(oversized) == AWAITING_SEGMENTED_REGENERATION, (
        "Baselines over Chromium's "
        f"{MAX_CAPTURE_HEIGHT_PX}px capture surface: {oversized}. "
        "Expected exactly the platform-relative files still awaiting segmented "
        "regeneration."
    )


def test_the_retired_oversized_baselines_are_real_platform_relative_files():
    """Pin what the carve-out above is allowed to cover.

    Every carve-out entry must still exist, so the constant cannot quietly stop
    describing a real file after that platform is regenerated.
    """
    for relative in sorted(AWAITING_SEGMENTED_REGENERATION):
        assert (SCREENSHOT_ROOT / relative).is_file(), (
            f"{relative} is listed as awaiting regeneration but is not present; "
            "drop it from AWAITING_SEGMENTED_REGENERATION."
        )


def test_the_capture_helper_declares_the_same_surface_limit():
    """The TypeScript capture path and this contract must agree on the number."""
    helper = VISUAL_HELPER.read_text(encoding="utf-8")
    assert "MAX_CAPTURE_HEIGHT_PX = 16_384" in helper, (
        "e2e/visual-helpers.ts must export MAX_CAPTURE_HEIGHT_PX = 16_384 so a "
        "capture taller than Chromium's surface limit is segmented rather than "
        "silently truncated."
    )


# The five captures deliberately not byte-compared, and the spec that carries
# their coverage instead. Kept here as a strict equality so the exemption cannot
# grow without this test failing and someone justifying the addition.
BYTE_GATE_EXEMPT = {
    "workout-plan-desktop-light",
    "workout-plan-desktop-dark",
    "plan-desktop-light-advanced",
    "plan-desktop-dark-advanced",
    "plan-desktop-dark-simple",
}
REPLACEMENT_SPEC = REPO_ROOT / "e2e" / "workout-plan-desktop-contract.spec.ts"


def test_the_byte_gate_exemption_is_exactly_the_five_measured_captures():
    """The exemption list may not grow without this test being changed.

    Each of these five was measured flipping between two rasters at
    byte-identical layout across 8 independent experiment sets, and each
    exceeds the 800px tolerance when it flips. Two other captures were seen to
    flip once each — ``log-desktop-light`` by 178px and
    ``workout-plan-mobile-light`` by 13px — and stay on the gate because they
    cannot fail it.
    """
    helper = VISUAL_HELPER.read_text(encoding="utf-8")
    declared, _, rest = helper.partition("export const BYTE_GATE_EXEMPT = new Set([")
    assert rest, "e2e/visual-helpers.ts must declare BYTE_GATE_EXEMPT"
    body = rest.partition("]);")[0]
    names = set(re.findall(r"'([^']+)'", body))
    assert names == BYTE_GATE_EXEMPT, (
        f"BYTE_GATE_EXEMPT drifted from the measured set: {names ^ BYTE_GATE_EXEMPT}"
    )


def test_the_exempt_captures_have_no_baseline_on_either_platform():
    """An exempt capture that still has a PNG is a baseline nothing compares.

    It would also survive `--update-snapshots` as a permanently stale file, so
    the absence is the contract, not an accident of deletion.
    """
    stray = [
        path.relative_to(SCREENSHOT_ROOT).as_posix()
        for path in _committed_baselines()
        if path.stem in BYTE_GATE_EXEMPT
    ]
    assert stray == [], f"Exempt captures still have committed baselines: {stray}"


def test_the_exempt_captures_route_through_the_non_pixel_assertion():
    """Both capture paths must honour the exemption, not just the full-page one.

    Two of the five are full-page captures and three are locator captures, so a
    guard in only one path would leave the other three byte-compared.
    """
    helper = VISUAL_HELPER.read_text(encoding="utf-8")
    thumbnails = (REPO_ROOT / "e2e" / "visual-baseline-thumbnails.spec.ts").read_text(
        encoding="utf-8"
    )
    assert "if (isByteGateExempt(name)) {" in helper, (
        "expectFullPageScreenshot must divert exempt captures before toHaveScreenshot"
    )
    assert "if (isByteGateExempt(label)) {" in thumbnails, (
        "the thumbnails spec must divert exempt captures before toHaveScreenshot"
    )


def test_the_replacement_spec_covers_every_exempt_surface():
    """The exemption is only defensible if the coverage actually moved."""
    assert REPLACEMENT_SPEC.is_file(), (
        "e2e/workout-plan-desktop-contract.spec.ts must exist: it is what the "
        "five exempt captures were traded for."
    )
    spec = REPLACEMENT_SPEC.read_text(encoding="utf-8")
    required = (
        "page composition and section order",   # replaces the two full-page captures
        "progressive column disclosure",        # replaces the advanced/simple element captures
        "row media and controls",               # thumbnails, swap, curated media split
        "theme surfaces and separator contrast",
        "width: 1440",                          # the viewport must not be narrowed to dodge the defect
    )
    missing = [literal for literal in required if literal not in spec]
    assert not missing, f"Replacement coverage missing: {missing}"

    # No pixel comparison may sneak back into the replacement.
    assert "toHaveScreenshot" not in spec, (
        "the replacement spec must not screenshot; that is the whole point"
    )


def test_visual_chromium_serializes_the_compositor_pipeline():
    """Fresh browser processes must raster the same completed frame."""
    config = PLAYWRIGHT_CONFIG.read_text(encoding="utf-8")
    required = (
        "'--font-render-hinting=none'",
        "'--disable-skia-runtime-opts'",
        "'--run-all-compositor-stages-before-draw'",
        "'--disable-threaded-animation'",
        "'--disable-threaded-scrolling'",
        "'--disable-checker-imaging'",
        "'--disable-image-animation-resync'",
    )
    missing = [literal for literal in required if literal not in config]
    assert not missing, f"Deterministic compositor controls missing: {missing}"


def test_oversized_element_captures_exclude_fixed_and_sticky_page_layers():
    """Table baselines must contain the table, not recomposited page chrome."""
    helper = VISUAL_HELPER.read_text(encoding="utf-8")
    common_prepare, element_prepare = helper.split(
        "export async function prepareForElementScreenshot", maxsplit=1
    )
    required = (
        '.vp-drawer[aria-hidden="true"]',
        "html[data-theme='dark'] .summary-header",
        "#navbar { visibility: hidden !important; }",
    )
    missing = [literal for literal in required if literal not in helper]
    assert not missing, f"Element-capture determinism controls missing: {missing}"
    for selector in (
        '[data-testid="exercise-table"] thead th',
        '[data-testid="workout-log-table"] thead th',
    ):
        assert selector in common_prepare, (
            f"{selector} must be flattened by prepareForScreenshot so full-page "
            "and locator table captures share one compositor path."
        )
    assert "requestAnimationFrame(() => requestAnimationFrame" in element_prepare, (
        "prepareForElementScreenshot must settle the paint invalidated by its "
        "element-only style before Playwright auto-scrolls the locator."
    )


def test_font_awesome_is_local_and_complete_for_offline_visual_runs():
    """Icon pixels must not depend on cdnjs availability or CORS headers."""
    base = (REPO_ROOT / "templates" / "base.html").read_text(encoding="utf-8")
    assert "vendor/fontawesome/css/all.min.css" in base
    assert "cdnjs.cloudflare.com/ajax/libs/font-awesome" not in base

    required = (
        FONT_AWESOME_ROOT / "css" / "all.min.css",
        FONT_AWESOME_ROOT / "webfonts" / "fa-solid-900.woff2",
        FONT_AWESOME_ROOT / "webfonts" / "fa-regular-400.woff2",
        FONT_AWESOME_ROOT / "webfonts" / "fa-brands-400.woff2",
        FONT_AWESOME_ROOT / "LICENSE.txt",
    )
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.is_file()]
    assert not missing, f"Vendored Font Awesome files missing: {missing}"
    empty = [str(path.relative_to(REPO_ROOT)) for path in required if path.stat().st_size == 0]
    assert not empty, f"Vendored Font Awesome files are empty: {empty}"


# --------------------------------------------------------------------------
# Visual-fixture catalog determinism
# --------------------------------------------------------------------------


def test_the_committed_visual_seed_still_lacks_the_curated_video_column():
    """Why the seeder has to run the catalog upgrade at all.

    If a regenerated fixture ever ships the column populated this test fails,
    which is the signal to re-derive the numbers below rather than trust them.
    """
    assert "youtube_video_id" not in _columns(VISUAL_SEED, "exercises")


def test_prepared_visual_db_ships_a_fully_upgraded_catalog(prepared_visual_db):
    """The prepared DB must already hold every curated id the shipped catalog has.

    Without this the ids arrive ~1.6 s into ``app.py`` startup, after Playwright
    has already accepted the port as ready, and ``buildPlayButton`` renders a
    magnifier before that point and a play icon after it.
    """
    assert "youtube_video_id" in _columns(prepared_visual_db, "exercises")

    shipped = _scalar(CATALOG_SEED, CURATED_ID_SQL)
    assert shipped > 0, "The shipped catalog carries no curated ids to compare against"

    prepared = _scalar(prepared_visual_db, CURATED_ID_SQL)
    assert prepared == shipped, (
        f"Prepared visual DB has {prepared} curated youtube_video_id rows but the "
        f"shipped catalog has {shipped}. app.py startup would mutate the "
        "difference in under a running capture."
    )


def test_prepared_visual_db_leaves_no_catalog_work_for_app_startup(
    prepared_visual_db, tmp_path, monkeypatch
):
    """The race-closing property, asserted directly.

    A second upgrade against the same catalog must be a recorded no-op. That is
    what guarantees ``app.py`` cannot change a rendered value after Playwright
    has decided the server is ready.

    Runs against a copy: the upgrade writes, and the module-scoped fixture is
    shared with the assertions below.
    """
    import utils.config
    from utils.catalog_upgrade import upgrade_catalog_from_seed

    replica = tmp_path / "database.visual.replica.db"
    shutil.copy2(prepared_visual_db, replica)

    monkeypatch.setattr(utils.config, "DB_FILE", str(replica))
    result = upgrade_catalog_from_seed()

    assert result.reason == "already-current", (
        f"app.py startup would still apply a catalog upgrade: {result}"
    )
    assert result.applied is False


def test_prepared_visual_db_keeps_the_fixture_thumbnails(prepared_visual_db):
    """``media_path`` is catalog-owned but ships empty, and must not be blanked.

    The visual fixture's whole purpose is rendering real thumbnails; a refresh
    that overwrote populated values with the shipped NULLs would empty every
    plan and log baseline.
    """
    fixture_media = _scalar(VISUAL_SEED, POPULATED_MEDIA_SQL)
    assert fixture_media > 0, "The visual fixture carries no media_path values"
    assert _scalar(prepared_visual_db, POPULATED_MEDIA_SQL) == fixture_media


def test_the_functional_seed_is_not_dragged_into_the_catalog_upgrade(prepared_e2e_db):
    """``prepare_e2e_db.py`` reuses ``apply_migrations`` and must stay unchanged.

    The functional suite asserts the *uncurated* branch of the video button
    (``workout-plan.spec.ts``: "Seed rows are uncurated -> search-variant icon").
    Upgrading its catalog is a separate, deliberate decision with its own
    re-baselining cost, so the visual seeder opts in explicitly rather than
    changing the shared helper's default.
    """
    assert _scalar(prepared_e2e_db, CURATED_ID_SQL) == 0
