"""P3-a0 contracts — over this packet's own outputs, not over the CSS.

Per-packet file (P-4). P3-a0 is read-only: it writes no production CSS, repairs
no existing apparatus and edits no existing contract. So these contracts pin the
*emitter* and the *audit findings*, and every one of them obeys two rules the
plan makes binding for this arc:

**O14 — an assertion satisfiable by absence is not a gate.** Every contract
below is paired with an executed red path that removes exactly the thing the
contract protects and shows the check fails. The pairs are named
``test_x`` / ``test_x_red_path``.

**O15 — red paths are committed, executed fixtures, not prose.** Every red path
here is a synthetic tree written by the test and fed to the same function under
test. Nothing is described in markdown and asserted nowhere.

One design rule runs through the whole file, and it is the reason several
obvious-looking assertions are absent: **no contract here may red on a change a
later packet is authorized to make.** P3-c deletes from ``theme-dark.css`` under
owner checkpoint; a contract in this permanently-collected file that pinned the
file's current shape would force a later packet to weaken it, which the arc
forbids. So the live figures are *reported* in
``docs/CSS_THEME_DARK_P3_A0_AUDIT_EVIDENCE.md`` and what is *pinned* here is
that the emitter derives them correctly from whatever it is given.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

import pytest

from scripts.css_audit import measure, p3_ceiling
from tests.test_css_wp4_4_a_baseline_contracts import EXPECTED_SNAPSHOT_COUNTS


ROOT = Path(__file__).resolve().parents[1]
THEME_DARK = ROOT / "static" / "css" / "theme-dark.css"
EVIDENCE_RELATIVE = "docs/CSS_THEME_DARK_P3_A0_AUDIT_EVIDENCE.md"

# The reader modules the walk must reach. Named rather than globbed so a module
# that stops reading the file is a red, not a silently smaller table.
READER_MODULES = (
    "test_css_wp4_4_theme_dark_contracts.py",
    "test_css_wp4_4_a_baseline_contracts.py",
    "test_css_cascade_contracts.py",
)

# Every content-class ceiling row, by (file alias, test name). Line numbers are
# deliberately NOT pinned: a contract keyed on a line number in someone else's
# file reds on an unrelated edit above it, which is drift, not protection.
EXPECTED_CONTENT_ROWS = {
    ("theme_dark_contracts.py", "test_theme_dark_is_still_linked_and_nonempty"),
    ("theme_dark_contracts.py", "test_every_custom_property_declaration_survives"),
    ("theme_dark_contracts.py", "test_the_reduced_motion_block_is_preserved"),
    ("theme_dark_contracts.py", "test_value_changed_rules_are_retained"),
    ("theme_dark_contracts.py", "test_the_deferred_superset_tint_was_not_added"),
    ("theme_dark_contracts.py", "test_the_certified_removals_stay_removed"),
    ("theme_dark_contracts.py", "test_the_file_declares_no_layer"),
    ("a_baseline_contracts.py", "test_important_is_counted_in_reconcilable_units"),
    (
        "cascade_contracts.py",
        "test_workout_plan_page_header_and_collapsible_frame_ownership_cleanup",
    ),
}


# ---------------------------------------------------------------------------
# Line endings — normalize the INPUT, never the expectation
# ---------------------------------------------------------------------------
#
# This repository is `core.autocrlf=true` with no `.gitattributes`, so the
# committed blob for `theme-dark.css` is LF while a Windows worktree checks it
# out as CRLF. Reading it with `newline=""` (no translation) therefore yields
# CRLF on Windows and LF on Linux, and any CSS literal in this module that
# embeds a specific line ending matches on exactly one platform.
#
# The fix is to normalize what is *read* and to write every embedded literal
# with `\n`. Rewriting the literals to CRLF instead would only flip which
# platform fails; normalizing the input makes both agree. This is the concrete
# form of the same CRLF hazard the evidence records against
# `measure.surface_counts()` (§3.1) — there it is a byte-count unit mismatch,
# here it was a substring-match mismatch.
#
# `read_bytes()` inside `p3_ceiling` is deliberately left alone: it must keep
# reporting the true on-disk bytes and line ending, which is what makes the
# O10 offset hazard visible at all.


def _read_css(path: Path) -> str:
    """Read CSS with line endings normalized to ``\\n`` on every platform.

    `newline=""` first, so nothing is translated on the way in and the
    normalization is explicit and single-sourced rather than implicit in
    Python's universal-newline mode.
    """
    return path.read_text(encoding="utf-8", newline="").replace("\r\n", "\n")


# ---------------------------------------------------------------------------
# Fixture builders — the committed, executed red paths (O15)
# ---------------------------------------------------------------------------


def _synthetic_tests_dir(tmp_path: Path, edits: dict[str, tuple[str, str]]) -> Path:
    """Copy the reader modules into ``tmp_path/tests``, applying text edits.

    ``edits`` maps a module filename to a single ``(old, new)`` replacement,
    asserted to have applied so a stale fixture cannot pass by doing nothing.
    """
    target = tmp_path / "tests"
    target.mkdir(parents=True, exist_ok=True)
    for name in READER_MODULES:
        text = (ROOT / "tests" / name).read_text(encoding="utf-8")
        if name in edits:
            old, new = edits[name]
            assert old in text, f"fixture anchor missing from {name}: {old!r}"
            text = text.replace(old, new, 1)
        (target / name).write_text(text, encoding="utf-8")
    return target


def _synthetic_css(tmp_path: Path, edits: list[tuple[str, str, int]]) -> Path:
    """Copy ``theme-dark.css`` into ``tmp_path``, applying text edits.

    The copy is normalized to ``\\n`` and written back with ``newline=""`` so no
    translation happens on the way out either: the fixture is byte-for-byte LF
    on Windows and on Linux, and so is every anchor matched against it.
    """
    text = _read_css(THEME_DARK)
    for old, new, count in edits:
        assert old in text, f"fixture anchor missing from theme-dark.css: {old!r}"
        text = text.replace(old, new, count)
    target = tmp_path / "theme-dark.css"
    target.write_text(text, encoding="utf-8", newline="")
    return target


def _row(records: list[dict[str, object]], suffix: str) -> dict[str, object]:
    matches = [
        record
        for record in records
        if str(record["file"]).endswith(suffix.split(":")[0])
        and str(record["line"]) == suffix.split(":")[1]
    ]
    assert len(matches) == 1, f"expected exactly one row for {suffix}, got {matches}"
    return matches[0]


def _content_row_identities(records: list[dict[str, object]]) -> set[tuple[str, str]]:
    return {
        (str(record["file"]).split("/")[-1], str(record["test"]))
        for record in records
        if record["readerClass"] == "content"
    }


def _alias(identities: set[tuple[str, str]]) -> set[tuple[str, str]]:
    mapping = {
        "test_css_wp4_4_theme_dark_contracts.py": "theme_dark_contracts.py",
        "test_css_wp4_4_a_baseline_contracts.py": "a_baseline_contracts.py",
        "test_css_cascade_contracts.py": "cascade_contracts.py",
    }
    return {(mapping.get(name, name), test) for name, test in identities}


# ---------------------------------------------------------------------------
# 1. The walk reaches every committed content reader
# ---------------------------------------------------------------------------


def _check_reader_coverage(records: list[dict[str, object]]) -> None:
    found = _alias(_content_row_identities(records))
    missing = EXPECTED_CONTENT_ROWS - found
    assert not missing, f"the emitter no longer reaches these ceiling rows: {missing}"


def test_the_emitter_reaches_every_committed_content_reader() -> None:
    """AC7 / P-8 — the ceiling is enumerated mechanically, not recalled.

    The walk is independent of ``measure.CONTRACT_FILES`` on purpose: that tuple
    is the two shared files, and twelve of the fourteen rows live in a
    per-packet contract file it does not list.
    """
    _check_reader_coverage(p3_ceiling.theme_dark_readers())


def test_the_emitter_reaches_every_committed_content_reader_red_path(
    tmp_path: Path,
) -> None:
    """Remove one reader's file read and the coverage check must fail."""
    tests_dir = _synthetic_tests_dir(
        tmp_path,
        {
            "test_css_wp4_4_a_baseline_contracts.py": (
                'theme_dark = (ROOT / "static" / "css" / "theme-dark.css")'
                '.read_text(encoding="utf-8")',
                'theme_dark = ""',
            )
        },
    )
    records = p3_ceiling.theme_dark_readers(tests_dir=tests_dir, css_path=THEME_DARK)
    with pytest.raises(AssertionError):
        _check_reader_coverage(records)


def test_the_walk_does_not_mistake_a_bundle_name_list_for_a_file_read() -> None:
    """The precision half, which the coverage check alone cannot show.

    ``tests/test_css_cascade_contracts.py`` has a module-level ``GLOBAL_BUNDLES``
    tuple containing the string ``"theme-dark.css"``. A name-mention walk turns
    every test that touches that tuple into a ceiling row and reports roughly
    130 of them. Only assertions that reach the file's *text* are ceilings.
    """
    records = p3_ceiling.theme_dark_readers()
    cascade = [
        record
        for record in records
        if str(record["file"]).endswith("test_css_cascade_contracts.py")
    ]
    assert {int(str(record["line"])) for record in cascade} == {1007, 1008}


def _check_self_exclusion_is_counted(bucket: dict[str, object]) -> None:
    assert int(bucket["excludedAssertionCount"]) > 0, (  # type: ignore[arg-type]
        "this packet's own contract file reads theme-dark.css, so the "
        "self-exclusion bucket cannot be empty; an empty bucket means the "
        "exclusion is silently dropping rows instead of counting them"
    )
    assert bucket["excludedFiles"] == [
        "tests/test_css_theme_dark_p3_audit_contracts.py"
    ]


def test_the_arcs_own_contract_files_are_excluded_as_a_counted_bucket() -> None:
    """An exclusion without a count is an omission.

    This file reads ``theme-dark.css`` to build its fixtures, so the walk finds
    it. Folding it into the ceiling table would make the arc's own output an
    input to its own ceiling; dropping it silently would hide that it was ever
    there. It is excluded and counted.
    """
    _check_self_exclusion_is_counted(p3_ceiling.self_owned_readers())


def test_the_arcs_own_contract_files_are_excluded_as_a_counted_bucket_red_path(
    tmp_path: Path,
) -> None:
    """A P3 contract file that reads the CSS must land in the bucket, not vanish."""
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir(parents=True)
    (tests_dir / "test_css_theme_dark_p3_future_packet_contracts.py").write_text(
        "from pathlib import Path\n"
        "\n"
        "ROOT = Path(__file__).resolve().parents[1]\n"
        "\n"
        "\n"
        "def test_future() -> None:\n"
        '    css = (ROOT / "static" / "css" / "theme-dark.css").read_text()\n'
        '    assert css.count("{") >= 1\n',
        encoding="utf-8",
    )
    assert (
        p3_ceiling.theme_dark_readers(tests_dir=tests_dir, css_path=THEME_DARK) == []
    )
    bucket = p3_ceiling.self_owned_readers(tests_dir=tests_dir, css_path=THEME_DARK)
    assert bucket["excludedAssertionCount"] == 1
    with pytest.raises(AssertionError):
        _check_self_exclusion_is_counted(bucket)


def test_the_walk_does_not_mistake_a_bundle_name_list_for_a_file_read_red_path(
    tmp_path: Path,
) -> None:
    """A module that only *names* the file must produce no ceiling rows at all."""
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir(parents=True)
    (tests_dir / "test_names_only.py").write_text(
        'BUNDLES = ("navbar.css", "theme-dark.css", "a11y.css")\n'
        "\n"
        "\n"
        "def test_bundle_set_is_unchanged() -> None:\n"
        '    assert "theme-dark.css" in BUNDLES\n'
        "    assert len(BUNDLES) == 3\n",
        encoding="utf-8",
    )
    assert (
        p3_ceiling.theme_dark_readers(tests_dir=tests_dir, css_path=THEME_DARK) == []
    )

    # And the same module gains a row the moment it actually reads the file.
    (tests_dir / "test_names_only.py").write_text(
        "from pathlib import Path\n"
        "\n"
        "ROOT = Path(__file__).resolve().parents[1]\n"
        "\n"
        "\n"
        "def test_bundle_set_is_unchanged() -> None:\n"
        '    css = (ROOT / "static" / "css" / "theme-dark.css").read_text()\n'
        '    assert css.count("{") >= 50\n',
        encoding="utf-8",
    )
    rows = p3_ceiling.theme_dark_readers(tests_dir=tests_dir, css_path=THEME_DARK)
    assert len(rows) == 1
    assert rows[0]["shape"] == "count-floor"


# ---------------------------------------------------------------------------
# 2. The whole-block deletion budget
# ---------------------------------------------------------------------------


def _check_budget(figures: dict[str, object], readers: list[dict[str, object]]) -> None:
    row = _row(readers, "test_css_wp4_4_theme_dark_contracts.py:35")
    assert row["shape"] == "count-floor"
    assert row["currentValue"] == figures["braceOpeningBlocks"]
    assert row["headroom"] == int(figures["braceOpeningBlocks"]) - int(row["bound"])  # type: ignore[arg-type]


def test_the_block_budget_is_derived_from_the_file_and_the_bound() -> None:
    """The 24-block arc-wide budget is arithmetic over two measured inputs.

    Neither the 74 nor the 50 is written down here — the first is counted off
    the file and the second is read out of the assertion — so the budget cannot
    drift away from either.
    """
    figures = p3_ceiling.measure_theme_dark()
    _check_budget(figures, p3_ceiling.theme_dark_readers())


def test_the_block_budget_is_derived_from_the_file_and_the_bound_red_path(
    tmp_path: Path,
) -> None:
    """Delete a whole rule and the budget must move with it."""
    css = _synthetic_css(
        tmp_path,
        [
            (
                ':where([data-theme="dark"] .frame-content) {\n'
                "    background: transparent !important;\n"
                "}\n",
                "",
                1,
            )
        ],
    )
    figures = p3_ceiling.measure_theme_dark(css)
    stale = p3_ceiling.theme_dark_readers()  # counted against the REAL file
    assert figures["braceOpeningBlocks"] == 73
    with pytest.raises(AssertionError):
        _check_budget(figures, stale)


# ---------------------------------------------------------------------------
# 3. The custom-property split and the F1 shadow nomination
# ---------------------------------------------------------------------------


def _check_token_blocks(figures: dict[str, object]) -> None:
    blocks = figures["customPropertyBlocks"]
    assert isinstance(blocks, list) and len(blocks) == 2, blocks
    assert sum(int(block["declarations"]) for block in blocks) == figures[
        "customPropertyDeclarations"
    ]
    nomination = figures["tokenBlockShadowNomination"]
    assert isinstance(nomination, dict)
    assert nomination["everyEarlierNameRedeclaredLater"] is True, (
        "the later unwrapped block no longer redeclares every name in the "
        "earlier :where() block, so the F1 shadow NOMINATION is void"
    )


def test_the_two_token_blocks_and_the_f1_shadow_nomination_are_measured() -> None:
    """P-2 keeps custom properties out of the non-winner rule; this is only the
    structural nomination, and it is emitted as such."""
    _check_token_blocks(p3_ceiling.measure_theme_dark())


def test_the_two_token_blocks_and_the_f1_shadow_nomination_are_measured_red_path(
    tmp_path: Path,
) -> None:
    """Drop one redeclaration from the later block and the nomination must void."""
    css = _synthetic_css(
        tmp_path, [("  --table-stripe: var(--surface-1);\n", "", 1)]
    )
    figures = p3_ceiling.measure_theme_dark(css)
    with pytest.raises(AssertionError):
        _check_token_blocks(figures)


# ---------------------------------------------------------------------------
# 4. Zero-headroom rows
# ---------------------------------------------------------------------------


def _check_zero_headroom(readers: list[dict[str, object]]) -> None:
    """Every ``>=`` row whose current value equals its bound has headroom 0."""
    value_changed = _row(readers, "test_css_wp4_4_theme_dark_contracts.py:62")
    assert value_changed["headroom"] == 0, (
        "the .value-changed floor no longer has zero headroom; the emitted "
        "ceiling would understate what a deletion costs"
    )


def test_the_value_changed_floor_is_emitted_with_zero_headroom() -> None:
    """``css.count(".value-changed") >= 7`` against a file containing exactly 7:
    deleting any one of them reds a WP4.4-j contract."""
    _check_zero_headroom(p3_ceiling.theme_dark_readers())


def test_the_value_changed_floor_is_emitted_with_zero_headroom_red_path(
    tmp_path: Path,
) -> None:
    """Add an eighth occurrence and the emitted headroom must stop being zero."""
    css = _synthetic_css(
        tmp_path,
        [
            (
                "/* Dark mode reduced motion */",
                ":where([data-theme='dark'] .value-changed) { outline: none; }\n"
                "/* Dark mode reduced motion */",
                1,
            )
        ],
    )
    readers = p3_ceiling.theme_dark_readers(tests_dir=ROOT / "tests", css_path=css)
    with pytest.raises(AssertionError):
        _check_zero_headroom(readers)


# ---------------------------------------------------------------------------
# 5. O14 — the substring pin that survives what it protects
# ---------------------------------------------------------------------------


def _check_backdrop_pin_is_satisfiable_by_absence(
    readers: list[dict[str, object]],
) -> None:
    row = _row(readers, "test_css_cascade_contracts.py:1008")
    assert row["satisfiableByAbsence"] is True, (
        "the cascade contract's backdrop-filter pin is no longer detected as "
        "satisfiable by absence; if it was repaired, this contract is obsolete "
        "and its packet must say so rather than deleting it"
    )
    assert int(row["pinnedLiteralOccurrencesInCss"]) > 1  # type: ignore[arg-type]


def test_the_backdrop_filter_pin_is_detected_as_satisfiable_by_absence() -> None:
    """O14, on the sharpest live instance in this arc's scope.

    ``tests/test_css_cascade_contracts.py:1008`` is a bare substring check for
    ``backdrop-filter: blur(8px) !important;``. The detector reports how many
    lines in the file satisfy it, which is the number that decides whether the
    pin can notice the loss of the line it exists to protect.
    """
    _check_backdrop_pin_is_satisfiable_by_absence(p3_ceiling.theme_dark_readers())


def test_the_backdrop_filter_pin_is_detected_as_satisfiable_by_absence_red_path(
    tmp_path: Path,
) -> None:
    """Reduce the literal to a single occurrence and the flag must clear."""
    css = _synthetic_css(
        tmp_path,
        [
            ("    -webkit-backdrop-filter: blur(8px) !important;\n", "", 2),
            (
                "    backdrop-filter: blur(8px) !important;\n"
                "    border: 1px solid rgba(255, 255, 255, 0.1) !important;",
                "    border: 1px solid rgba(255, 255, 255, 0.1) !important;",
                1,
            ),
        ],
    )
    readers = p3_ceiling.theme_dark_readers(tests_dir=ROOT / "tests", css_path=css)
    row = _row(readers, "test_css_cascade_contracts.py:1008")
    assert row["pinnedLiteralOccurrencesInCss"] == 1
    with pytest.raises(AssertionError):
        _check_backdrop_pin_is_satisfiable_by_absence(readers)


def _check_haystack_discrimination(readers: list[dict[str, object]]) -> None:
    """A sliced haystack must not be flagged just because the file repeats."""
    sliced = _row(readers, "test_css_wp4_4_theme_dark_contracts.py:55")
    assert sliced["satisfiableByAbsence"] is False
    assert sliced["haystackIsWholeFile"] is False


def test_the_o14_detector_distinguishes_a_sliced_haystack() -> None:
    """``assert "value-changed" in block`` where ``block`` is the text after
    ``@media`` is a slice check. Counting the literal across the whole file
    would flag it, and the flag would be wrong."""
    _check_haystack_discrimination(p3_ceiling.theme_dark_readers())


def test_the_o14_detector_distinguishes_a_sliced_haystack_red_path(
    tmp_path: Path,
) -> None:
    """Turn the slice into a whole-file haystack and the detector must flag it."""
    tests_dir = _synthetic_tests_dir(
        tmp_path,
        {
            "test_css_wp4_4_theme_dark_contracts.py": (
                'block = css.split("@media", 1)[1]',
                "block = css",
            )
        },
    )
    readers = p3_ceiling.theme_dark_readers(tests_dir=tests_dir, css_path=THEME_DARK)
    row = _row(readers, "test_css_wp4_4_theme_dark_contracts.py:55")
    assert row["haystackIsWholeFile"] is True
    assert row["satisfiableByAbsence"] is True


# ---------------------------------------------------------------------------
# 6. Q1 — the `occurrences <= 1` defect, probed rather than argued
# ---------------------------------------------------------------------------

_RESULTS_BODY_RULE = (
    ':where([data-theme="dark"] .table.table-hover tbody),\n'
    ':where([data-theme="dark"] #results-body) {\n'
    "    background-color: var(--bg-primary) !important;\n"
    "    color: var(--text-primary) !important;\n"
    "}\n"
)


def _check_q1_defect_is_live(css_text: str) -> None:
    """The granted `<= 1` -> `== 1` strengthening is still needed, measured."""
    intact = p3_ceiling.q1_occurrences(css_text)
    assert all(row["occurrences"] == 1 for row in intact), (
        "a pinned pair no longer declares its longhand exactly once; the Q1 "
        f"probe reads {[row['occurrences'] for row in intact]}"
    )

    assert _RESULTS_BODY_RULE in css_text, "the Q1 probe anchor rule is gone"
    without = p3_ceiling.q1_occurrences(css_text.replace(_RESULTS_BODY_RULE, "", 1))
    deleted = [
        row
        for row in without
        if row["selector"] == ':where([data-theme="dark"] #results-body)'
    ]
    assert len(deleted) == 1
    assert deleted[0]["occurrences"] == 0
    assert deleted[0]["passesUnderLessThanOrEqualOne"] is True, (
        "deleting the surviving winner no longer satisfies `<= 1`; the defect "
        "is repaired and this contract is obsolete"
    )
    assert deleted[0]["passesUnderEqualsOne"] is False


def test_the_certified_removals_pin_still_passes_at_zero() -> None:
    """Executed proof of the defect the owner granted permission to repair.

    P3-a0 does **not** perform that repair — it edits no existing contract file.
    This records that the repair is still available and still needed, by running
    the assertion's own predicate over a CSS text with the protected rule
    deleted and showing it stays green.
    """
    _check_q1_defect_is_live(_read_css(THEME_DARK))


def test_the_certified_removals_pin_still_passes_at_zero_red_path(
    tmp_path: Path,
) -> None:
    """Duplicate a pinned longhand and the "exactly once today" half must fail."""
    css = _synthetic_css(
        tmp_path,
        [
            (
                _RESULTS_BODY_RULE,
                _RESULTS_BODY_RULE + _RESULTS_BODY_RULE,
                1,
            )
        ],
    )
    with pytest.raises(AssertionError):
        _check_q1_defect_is_live(_read_css(css))


# ---------------------------------------------------------------------------
# 7. Production CSS is byte-identical — asserted, not assumed
# ---------------------------------------------------------------------------


def _check_production_css_clean(status: dict[str, object]) -> None:
    assert status["clean"] is True, (
        "P3-a0 writes no production CSS, but git reports changes under "
        f"static/css: {status['statusPorcelain']}"
    )


def test_this_packet_wrote_no_production_css() -> None:
    """The P3-a0 gate row: production CSS diff empty, asserted.

    Scoped to the working tree rather than to a base SHA. A base-SHA pin in a
    permanently-collected per-packet file would red the moment P3-c makes its
    authorized cut, and no packet may be made to weaken another's assertion.
    """
    _check_production_css_clean(p3_ceiling.production_css_status())


def test_this_packet_wrote_no_production_css_red_path(tmp_path: Path) -> None:
    """A dirty static/css tree must fail the same check."""
    repo = tmp_path / "repo"
    (repo / "static" / "css").mkdir(parents=True)
    (repo / "static" / "css" / "theme-dark.css").write_text("a{}\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=p3@example.invalid",
            "-c",
            "user.name=p3",
            "commit",
            "-q",
            "-m",
            "fixture",
        ],
        cwd=repo,
        check=True,
    )
    assert p3_ceiling.production_css_status(repo)["clean"] is True

    (repo / "static" / "css" / "theme-dark.css").write_text("b{}\n", encoding="utf-8")
    dirty = p3_ceiling.production_css_status(repo)
    assert dirty["clean"] is False
    with pytest.raises(AssertionError):
        _check_production_css_clean(dirty)


def test_the_arc_base_is_measured_from_the_repository_not_hardcoded(
    tmp_path: Path,
) -> None:
    """"Record the SHA you actually measured" has to be a read, not a constant.

    Red path and green path in one: the same function run against a synthetic
    repository must report that repository's HEAD.
    """
    live = p3_ceiling.arc_base()
    assert re.fullmatch(r"[0-9a-f]{40}", str(live["measuredCommit"]))

    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "seed.txt").write_text("seed\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=p3@example.invalid",
            "-c",
            "user.name=p3",
            "commit",
            "-q",
            "-m",
            "fixture",
        ],
        cwd=repo,
        check=True,
    )
    synthetic = p3_ceiling.arc_base(repo)
    assert synthetic["measuredCommit"] != live["measuredCommit"]
    assert synthetic["planPinnedBaseIsAncestorOfHead"] is None


# ---------------------------------------------------------------------------
# 8. The nineteen-tool assessment
# ---------------------------------------------------------------------------


def _check_tool_coverage(assessment: dict[str, object]) -> None:
    assert assessment["coverageComplete"] is True, (
        "the committed tool set and the assessed tool set disagree; "
        f"unassessed={assessment['unassessed']} "
        f"absent={assessment['assessedButAbsent']}"
    )


def test_every_committed_css_audit_tool_is_assessed() -> None:
    """The packet boundary that makes "re-scope before building" enforceable.

    P3-a1 is priced off this list, so a tool added to ``scripts/css_audit/``
    without a verdict has to red rather than quietly widen the scope.
    ``p3_*`` files are excluded: they are this arc's own output, not inputs to
    the assessment.
    """
    _check_tool_coverage(p3_ceiling.tool_assessment())


def test_every_committed_css_audit_tool_is_assessed_red_path(tmp_path: Path) -> None:
    """An unassessed tool in the directory must fail the coverage check."""
    directory = tmp_path / "css_audit"
    directory.mkdir()
    for path in (ROOT / "scripts" / "css_audit").iterdir():
        if path.is_file():
            shutil.copy2(path, directory / path.name)
    (directory / "z_unassessed_tool.mjs").write_text("// new\n", encoding="utf-8")

    assessment = p3_ceiling.tool_assessment(directory)
    assert assessment["unassessed"] == ["z_unassessed_tool.mjs"]
    with pytest.raises(AssertionError):
        _check_tool_coverage(assessment)


def test_no_committed_tool_is_claimed_to_be_a_removal_oracle() -> None:
    """AB-1's premise: M-h3 deletion authority does not exist in this repository.

    Asserted against the directory rather than against prose, so a recovered or
    newly added ``h_*`` harness reds this and forces the claim to be re-made.
    """
    _check_no_removal_oracle(p3_ceiling.tool_assessment())
    verdicts = {
        str(entry["tool"]): str(entry["verdict"])
        for entry in p3_ceiling.TOOL_ASSESSMENT
    }
    assert "NOT a removal oracle" in verdicts["runtime_probe.mjs"]


def _check_no_removal_oracle(assessment: dict[str, object]) -> None:
    recovered = [
        name
        for name in assessment["committedTools"]  # type: ignore[union-attr]
        if str(name).startswith("h_")
    ]
    assert not recovered, (
        "a WP4.4-h harness is present again: "
        f"{recovered}. AB-1's premise — that no removal oracle exists — has to "
        "be re-made, and P3-a1's scope re-priced, before anything is built."
    )


def test_no_committed_tool_is_claimed_to_be_a_removal_oracle_red_path(
    tmp_path: Path,
) -> None:
    """Restore an ``h_*`` harness and the premise check must fail."""
    directory = tmp_path / "css_audit"
    directory.mkdir()
    for path in (ROOT / "scripts" / "css_audit").iterdir():
        if path.is_file():
            shutil.copy2(path, directory / path.name)
    (directory / "h_certify.mjs").write_text("// recovered\n", encoding="utf-8")

    with pytest.raises(AssertionError):
        _check_no_removal_oracle(p3_ceiling.tool_assessment(directory))


# ---------------------------------------------------------------------------
# 9. C7 — the uncertifiable set, recovered by reading
# ---------------------------------------------------------------------------


def _check_uncertifiable(record: dict[str, object]) -> None:
    assert record["countAgrees"] is True
    assert record["recoveredCount"] == 8
    assert record["everyElementHasDomPath"] is True
    assert record["everyElementHasSelector"] is True
    assert "developer-credit-banner" in str(record["adjacentNote"])


def test_the_c7_uncertifiable_set_is_recoverable_from_the_committed_ledger() -> None:
    """architecture-reviewer #11, retracted at re-review, confirmed here.

    The eight elements were said to be lost with the gitignored ``artifacts/``
    tree. They are not: the committed schema-v2 ledger carries all eight with
    ``domPath`` and ``selector``, plus the ``::before`` adjacency note.
    """
    _check_uncertifiable(p3_ceiling.uncertifiable_elements())


def test_the_c7_uncertifiable_set_is_recoverable_from_the_committed_ledger_red_path(
    tmp_path: Path,
) -> None:
    """Strip one ``domPath`` and the recovery check must fail."""
    ledger = json.loads(
        (ROOT / p3_ceiling.LEDGER_RELATIVE).read_text(encoding="utf-8")
    )
    del ledger["uncertifiableElements"]["elements"][0]["domPath"]
    path = tmp_path / "ledger.json"
    path.write_text(json.dumps(ledger), encoding="utf-8")

    record = p3_ceiling.uncertifiable_elements(path)
    assert record["everyElementHasDomPath"] is False
    with pytest.raises(AssertionError):
        _check_uncertifiable(record)


# ---------------------------------------------------------------------------
# 10. The N8 denominator
# ---------------------------------------------------------------------------


def _synthetic_root(tmp_path: Path, ledger: dict) -> Path:
    root = tmp_path / "root"
    (root / "docs").mkdir(parents=True)
    (root / "e2e").mkdir(parents=True)
    (root / ".github" / "workflows").mkdir(parents=True)
    (root / p3_ceiling.LEDGER_RELATIVE).write_text(
        json.dumps(ledger), encoding="utf-8"
    )
    for name in ("visual.spec.ts", "visual-baseline-thumbnails.spec.ts", "visual-helpers.ts"):
        shutil.copy2(ROOT / "e2e" / name, root / "e2e" / name)
    shutil.copy2(
        ROOT / ".github" / "workflows" / "deep-gate.yml",
        root / ".github" / "workflows" / "deep-gate.yml",
    )
    return root


def _check_n8(record: dict[str, object]) -> None:
    assert record["dispatched"] is False, "P3-a0 may not dispatch the deep gate"
    assert record["workflowRunsBothSpecsTogether"] is True
    assert record["expectedTotal"] == 84
    assert int(str(record["recordedRunCount"])) >= 1, (
        "the ledger records no run result to reconcile against, so this "
        "reconciliation asserts nothing"
    )
    assert record["derivationMatchesEveryRecordedRun"] is True, (
        "the serial-mode derivation no longer reproduces the run results the "
        f"ledger itself records: {record['recordedRuns']}"
    )
    reconciliation = record["reconciliation"]
    assert reconciliation["closes"] is True  # type: ignore[index]


def test_the_n8_denominator_reconciles_against_the_recorded_runs() -> None:
    """66 + 18 = 84 expected against 68 reported; the 16 are serial-mode collateral.

    The falsifiable half is not the sum — that closes for any inputs — it is
    that the derivation reproduces ``11 failed / 57 passed`` from the spec
    matrices and the ledgered red's position, for every run the ledger records.
    """
    _check_n8(p3_ceiling.n8_denominator())


def test_the_n8_denominator_reconciles_against_the_recorded_runs_red_path(
    tmp_path: Path,
) -> None:
    """Move the ledgered thumbnail red to the last test in the file.

    Nothing then gets skipped, the derivation predicts ``11 failed / 73 passed``,
    and the recorded ``57 passed`` stops matching.
    """
    ledger = json.loads(
        (ROOT / p3_ceiling.LEDGER_RELATIVE).read_text(encoding="utf-8")
    )
    ledger["linuxInheritedReds"]["specs"][1]["files"] = ["log-mobile-dark.png"]
    record = p3_ceiling.n8_denominator(_synthetic_root(tmp_path, ledger))

    assert record["reconciliation"]["didNotRun"] == 0  # type: ignore[index]
    assert record["derivationMatchesEveryRecordedRun"] is False
    with pytest.raises(AssertionError):
        _check_n8(record)


# ---------------------------------------------------------------------------
# 10a. Citation hygiene against the shared WP4.4-a contract
# ---------------------------------------------------------------------------
#
# Added after the arc closed, because the emitter and the evidence document had
# both drifted: they cited `tests/test_css_wp4_4_a_baseline_contracts.py` by
# line number in nine places, and one of those citations carried a transcribed
# `18` where the pin it named reads 15. Nothing could red on either, so both
# rules below are enforced on *shape* rather than on a number.

WIN32_THUMBNAILS = "win32/visual-baseline-thumbnails.spec.ts-snapshots"

# The alias form, which is what `_row_key()` produces and what the prose uses.
# Matching only the full path would miss every alias-form citation, and the
# alias form is the one the module already writes by hand.
_LINE_CITATION = re.compile(r"a_baseline_contracts\.py:\d+")

# Introduced by the repair, in the emitted record and in the document alike.
# Its presence is the positive half: a text that cites nothing at all must not
# satisfy a contract phrased as "no line citations".
_SYMBOL_CITATION = "test_contract_anchor_register_covers_every_shared_surface"


def _check_baseline_pins(pins: dict[str, object], matrices: dict[str, object]) -> None:
    """The pin agrees with the shared contract, and the shortfall is explained."""
    assert pins["snapshotRootExists"] is True, (
        "the snapshot tree is absent, so every count below is a silent zero "
        "rather than a measurement"
    )
    assert pins["counts"] == EXPECTED_SNAPSHOT_COUNTS

    # The thumbnail spec's tests, less its exempt captures, is its baseline
    # count. Both sides derive from the spec matrix, so neither is a literal.
    exempt = {name for name in pins["byteGateExempt"] if name.startswith("plan-")}  # type: ignore[union-attr]
    thumbnails = matrices["visual-baseline-thumbnails.spec.ts"]  # type: ignore[index]
    assert pins["counts"][WIN32_THUMBNAILS] == thumbnails["tests"] - len(exempt)  # type: ignore[index]


def _check_no_line_citation(text: str, allowed: set[str]) -> None:
    """No hand-written `<file>:<line>` citation, and the symbol form is present."""
    assert _SYMBOL_CITATION in text, (
        "the text cites the shared contract nowhere, so 'it carries no line "
        "citation' is satisfied by absence rather than by repair"
    )
    found = set(_LINE_CITATION.findall(text))
    assert not found - allowed, (
        f"line citations into the shared WP4.4-a contract: {sorted(found - allowed)}. "
        "Cite the test, not the line — an unrelated edit above an assertion "
        "moves the number and nothing reds."
    )


@lru_cache(maxsize=1)
def _report() -> dict[str, object]:
    """The whole emitted record, built once for the two shape contracts.

    `report()` walks every module under `tests/` several times, so a per-test
    call would cost ~3s twice. Neither caller mutates it.
    """
    return p3_ceiling.report()


def _emitted_allowances(record: dict[str, object]) -> set[str]:
    """The two `<file>:<line>` forms that legitimately reach the record.

    `_row_key()` ceiling-table keys are measurements at the running commit and
    are *meant* to move; the `PLAN_CLAIMS` transcription quotes the plan
    verbatim so `plan_discrepancies()` can report its drift.
    """
    allowed = {p3_ceiling._row_key(row) for row in record["ceilingTable"]}  # type: ignore[union-attr]
    return allowed | set(p3_ceiling.PLAN_CLAIMS["ceilingRows"])  # type: ignore[arg-type]


def test_the_emitted_baseline_pins_are_measured_not_transcribed() -> None:
    """The pin is counted on disk, not transcribed, and must match its source."""
    _check_baseline_pins(
        p3_ceiling.committed_baseline_pins(),
        p3_ceiling.n8_denominator()["specMatrices"],  # type: ignore[arg-type]
    )


def test_the_emitted_baseline_pins_are_measured_not_transcribed_red_path(
    tmp_path: Path,
) -> None:
    """A tree the emitter cannot read must not report a confident zero.

    This is the shape the old transcription hid behind: a static `18` beside a
    count nothing measured. `glob()` on a missing directory returns no error,
    so absence has to be reported rather than counted.
    """
    (tmp_path / "e2e").mkdir()
    shutil.copy2(
        ROOT / "e2e" / "visual-helpers.ts", tmp_path / "e2e" / "visual-helpers.ts"
    )

    pins = p3_ceiling.committed_baseline_pins(tmp_path)

    assert pins["snapshotRootExists"] is False
    assert pins["counts"][WIN32_THUMBNAILS] == 0  # type: ignore[index]
    with pytest.raises(AssertionError):
        _check_baseline_pins(pins, p3_ceiling.n8_denominator()["specMatrices"])  # type: ignore[arg-type]


def test_the_emitted_record_cites_the_shared_contract_by_symbol_not_by_line() -> None:
    """A line citation into someone else's test file goes stale silently."""
    record = _report()

    _check_no_line_citation(
        json.dumps(record, ensure_ascii=False), _emitted_allowances(record)
    )


def test_the_evidence_document_cites_the_shared_contract_by_symbol_not_by_line() -> None:
    """The same rule on the document half of the same packet."""
    evidence = (ROOT / EVIDENCE_RELATIVE).read_text(encoding="utf-8")

    _check_no_line_citation(evidence, set(p3_ceiling.PLAN_CLAIMS["ceilingRows"]))  # type: ignore[arg-type]


def _regress(text: str, old: str, new: str) -> str:
    """One citation put back in its stale form, refusing to be a no-op."""
    regressed = text.replace(old, new, 1)
    assert regressed != text, f"mutation is a no-op: {old!r} is not in the text"
    return regressed


def test_the_emitted_record_cites_the_shared_contract_by_symbol_not_by_line_red_path() -> None:
    """Put one emitted citation back in its stale form and the check fails.

    The allowance set is the live one, so the red is attributable to the
    reintroduced citation and not to the measured row keys the record carries
    legitimately.
    """
    record = _report()
    regressed = _regress(
        json.dumps(record, ensure_ascii=False),
        f"tests/test_css_wp4_4_a_baseline_contracts.py::{_SYMBOL_CITATION}",
        "tests/test_css_wp4_4_a_baseline_contracts.py:297-298",
    )

    with pytest.raises(AssertionError, match="297"):
        _check_no_line_citation(regressed, _emitted_allowances(record))


def test_the_evidence_document_cites_the_shared_contract_by_symbol_not_by_line_red_path() -> None:
    """The same, on the document: restore the pre-repair snapshot-digest citation."""
    regressed = _regress(
        (ROOT / EVIDENCE_RELATIVE).read_text(encoding="utf-8"),
        "`a_baseline_contracts.py::test_snapshot_manifest_makes_an_accidental_"
        "rebaseline_a_pytest_red`",
        "`a_baseline_contracts.py:234-255`",
    )

    with pytest.raises(AssertionError, match="234"):
        _check_no_line_citation(regressed, set(p3_ceiling.PLAN_CLAIMS["ceilingRows"]))  # type: ignore[arg-type]


def test_a_text_that_cites_nothing_does_not_satisfy_the_shape_contract() -> None:
    """O14 — the ban is satisfiable by deletion unless presence is asserted too."""
    with pytest.raises(AssertionError, match="satisfied by absence"):
        _check_no_line_citation("this text mentions no contract at all", set())


# ---------------------------------------------------------------------------
# 11. Q10 — the blind-spot sizing instrument
# ---------------------------------------------------------------------------


def _check_sizing_partition(sizing: dict[str, object]) -> None:
    """Every rule block in the helper lands in exactly one bucket."""
    total = (
        int(sizing["fullyMappedBlocks"])  # type: ignore[arg-type]
        + int(sizing["unmappedBlockCount"])  # type: ignore[arg-type]
        + int(sizing["partiallyMappedBlockCount"])  # type: ignore[arg-type]
        + len(sizing["tokenDefinitionBlocks"])  # type: ignore[arg-type]
    )
    assert total == sizing["helperRuleBlocks"], (
        f"the sizing partition drops {int(sizing['helperRuleBlocks']) - total} "  # type: ignore[arg-type]
        "rule block(s); an unclassified neutralizer is exactly the gap Q10 is "
        "about"
    )


def test_the_blind_spot_sizing_partitions_every_helper_rule_block() -> None:
    """Q10 sizing, and only sizing. Nothing here repairs the shared register.

    The measured gap is reported in the evidence document rather than pinned:
    a contract asserting "the gap is N blocks" would red when the owner grants
    the repair, which is a gate that fires on the good change.
    """
    _check_sizing_partition(p3_ceiling.blind_spot_repair_sizing())


def test_the_blind_spot_sizing_partitions_every_helper_rule_block_red_path(
    tmp_path: Path,
) -> None:
    """A neutralizer added to the helper must surface as unmapped, and a helper
    whose blocks are all registered must report no gap."""
    helper = (ROOT / p3_ceiling.VISUAL_HELPERS_RELATIVE).read_text(encoding="utf-8")
    baseline = p3_ceiling.blind_spot_repair_sizing()

    added = helper.replace(
        "      [data-visual-icon] {",
        "      .p3-red-path-neutralizer { filter: none !important; }\n"
        "      [data-visual-icon] {",
        1,
    )
    assert added != helper
    path = tmp_path / "visual-helpers.ts"
    path.write_text(added, encoding="utf-8")

    mutated = p3_ceiling.blind_spot_repair_sizing(path)
    _check_sizing_partition(mutated)
    assert int(mutated["helperRuleBlocks"]) == int(baseline["helperRuleBlocks"]) + 1  # type: ignore[arg-type]
    assert int(mutated["unmappedBlockCount"]) == int(baseline["unmappedBlockCount"]) + 1  # type: ignore[arg-type]
    assert ".p3-red-path-neutralizer" in {
        str(block["selector"]) for block in mutated["unmappedBlocks"]  # type: ignore[union-attr]
    }

    # The partition check itself must fail when a block goes missing, or it is
    # not a gate.
    dropped = dict(mutated)
    dropped["unmappedBlockCount"] = int(mutated["unmappedBlockCount"]) - 1  # type: ignore[arg-type]
    with pytest.raises(AssertionError):
        _check_sizing_partition(dropped)


def test_the_shared_blind_spot_verifier_is_bidirectional() -> None:
    """Q10's premise, repaired: the verifier now sees an addition too.

    P3-a0 measured ``measure.verify_blind_spots()`` as one-way — it searched the
    helper for each register entry's ``helperEvidence`` and asked nothing about
    what the helper contained that the register did not. A neutralizer *added*
    to ``prepareForScreenshot()`` was therefore invisible, which is how the dark
    ``.summary-header`` flattening and the sticky-table ``position: static``
    demotion both shipped with the whole suite green.

    Both directions are asserted here, and the previous shape of this test — one
    that required the addition to go **unnoticed** — is what the repair
    retired. The guarantee is unchanged; only its sign is.
    """
    helper = (ROOT / p3_ceiling.VISUAL_HELPERS_RELATIVE).read_text(encoding="utf-8")
    assert measure.verify_blind_spots() == []

    added = helper.replace(
        "      [data-visual-icon] {",
        "      .p3-unregistered { filter: none !important; }\n"
        "      [data-visual-icon] {",
        1,
    )
    assert added != helper
    addition = measure.verify_blind_spots(added)
    assert any(".p3-unregistered" in line for line in addition), (
        "a neutralizer added to the helper is still invisible to the shared "
        f"verifier; Q10's repair has regressed. Got: {addition}"
    )

    removed = helper.replace("animation-duration: 0s !important;", "", 1)
    assert removed != helper
    removal = measure.verify_blind_spots(removed)
    assert any("animation-duration" in line for line in removal), (
        f"the direction the verifier always had has stopped working: {removal}"
    )


def test_the_two_backdrop_filter_neutralizers_are_registered_independently() -> None:
    """The O14 instance inside the shared apparatus itself, repaired.

    P3-a0 recorded that the register's backdrop-filter entry cited
    ``backdrop-filter: none !important;`` while the helper's own
    ``-webkit-backdrop-filter: none !important;`` line *contains* that string —
    so deleting the neutralizer the entry described left its evidence satisfied,
    the identical defect as ``tests/test_css_cascade_contracts.py:1008``.

    Identity is now ``(stage, selector, property)``, and one property cannot
    stand in for another. This asserts the repair on the case that named it.
    """
    helper = (ROOT / p3_ceiling.VISUAL_HELPERS_RELATIVE).read_text(encoding="utf-8")

    without_unprefixed = helper.replace(
        "        backdrop-filter: none !important;\n", "", 1
    )
    assert without_unprefixed != helper
    assert "-webkit-backdrop-filter: none !important;" in without_unprefixed, (
        "the prefixed line is gone too, so this no longer exercises shadowing"
    )

    failures = measure.verify_blind_spots(without_unprefixed)
    assert any("{ backdrop-filter:" in line for line in failures), (
        "the surviving -webkit- line still satisfies the unprefixed property's "
        f"registration. Got: {failures}"
    )


# ---------------------------------------------------------------------------
# 12. The shared registers cannot reach this ceiling
# ---------------------------------------------------------------------------


def _check_register_reach(reach: dict[str, object]) -> None:
    assert reach["contractFilesCoverTheThemeDarkPacketContract"] is False
    assert set(reach["ceilingRowsReachable"]) == {  # type: ignore[arg-type]
        "cascade_contracts.py:1007",
        "cascade_contracts.py:1008",
    }
    assert int(reach["ceilingRowsUnreachableCount"]) > 0  # type: ignore[arg-type]


def test_the_shared_registers_reach_only_the_two_cascade_rows() -> None:
    """re-review N1, measured rather than argued.

    ``measure.contract_anchors()`` / ``pinned_declarations()`` iterate
    ``measure.CONTRACT_FILES``, so a "mechanical emitter" built on them reaches
    the two ``.frame-header`` rows and nothing else. That is the whole reason
    ``scripts/css_audit/p3_ceiling.py`` exists.
    """
    _check_register_reach(p3_ceiling.shared_register_reach())


def test_the_shared_registers_reach_only_the_two_cascade_rows_red_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Extend CONTRACT_FILES in memory and the reach claim must stop holding.

    ``monkeypatch`` is used precisely so the demonstration cannot become the
    change: the shared tuple is restored at teardown, the committed baseline is
    never regenerated, and ``tests/test_css_wp4_4_a_baseline_contracts.py``
    never sees a moved register.
    """
    monkeypatch.setattr(
        measure,
        "CONTRACT_FILES",
        measure.CONTRACT_FILES + ("tests/test_css_wp4_4_theme_dark_contracts.py",),
    )
    reach = p3_ceiling.shared_register_reach()
    assert len(reach["ceilingRowsReachable"]) > 2  # type: ignore[arg-type]
    with pytest.raises(AssertionError):
        _check_register_reach(reach)


# ---------------------------------------------------------------------------
# 13. The plan's copy is compared, never inherited
# ---------------------------------------------------------------------------


def _check_discrepancies_are_reported(rows: list[dict[str, object]]) -> None:
    disagreements = [row for row in rows if not row["agrees"]]
    assert disagreements, (
        "plan_discrepancies() reported no disagreement at all, which would mean "
        "the comparison is not running"
    )


def test_the_plan_table_is_compared_and_its_disagreements_are_reported() -> None:
    """The plan's 14-row table is Gate-0 material and is not a source.

    This asserts the comparison *runs and can disagree* rather than pinning the
    disagreements themselves — those are findings, recorded in the evidence
    document, and several of them are things a later packet may legitimately
    change.
    """
    _check_discrepancies_are_reported(p3_ceiling.plan_discrepancies())


def test_the_plan_table_is_compared_and_its_disagreements_are_reported_red_path() -> None:
    """Feed the comparison the plan's own numbers and it must report agreement.

    The red path for a *difference detector* is the input that makes it find no
    difference; if it still reported one, the detector would be noise.
    """
    figures = dict(p3_ceiling.measure_theme_dark())
    figures["lines"] = p3_ceiling.PLAN_CLAIMS["lines"]
    figures["topLevelStyleRules"] = p3_ceiling.PLAN_CLAIMS["topLevelRules"]
    rows = p3_ceiling.plan_discrepancies(figures, p3_ceiling.theme_dark_readers())
    by_item = {str(row["item"]): row for row in rows}
    assert by_item["lines"]["agrees"] is True
    assert by_item["top-level rules"]["agrees"] is True

    # And the check that consumes the list must fail on a fully-agreeing one,
    # or "the comparison ran" is not something it can tell you.
    with pytest.raises(AssertionError):
        _check_discrepancies_are_reported(
            [dict(row, agrees=True) for row in rows]
        )
