"""Contracts for the Vitest surface of the generated test inventory.

`Test Inventory Drift` is a required branch-protection context, and after this
packet it also pins the JS-unit suite: 13 files, 245 cases, and every case's
identity. (231 until the KI-010 toast fix of 2026-08-27, which inverted two
characterization cases and added fourteen -- see
docs/toast_type_word_collision/PLANNING.md.) Two things can quietly unpin it, and `--check` sees neither, because
`--check` only compares a committed artifact with what the generator produces
right now:

  * a renderer that stops emitting a section, against a committed file that
    never contained it -- green forever;
  * a parser that stops validating, against a tree that happens to be clean.

So the numbers are pinned here as literals, the parser is exercised as a pure
function, and the committed Markdown is asserted to actually contain the section
the generator claims to write.

Two authoring rules this file must keep obeying:

1. **No subprocess, no `node_modules`, no `_npx()`.** `Run Tests` has node on its
   PATH, so `shutil.which("npx")` succeeds there and would not fail fast -- a
   shelling test would attempt a registry fetch inside a required job. The
   subprocess seam is `_run_vitest_list()`, and it is deliberately not covered
   here; everything reachable without a runner lives in `parse_vitest_listing()`.
2. **The collected node count must be identical on Windows and Linux.** No
   `shutil.which` parametrization, no environment-derived parametrize list --
   this file's own count is committed to the artifact it tests.
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

import scripts.generate_test_inventory as generator
from scripts.generate_test_inventory import (
    COLLECTION_FAILURE,
    SCHEMA_VERSION,
    VITEST_COLLECTOR,
    _console_safe,
    _run_vitest_list,
    _vitest_list_argv,
    parse_vitest_listing,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = REPO_ROOT / "docs" / "test_inventory" / "TEST_INVENTORY.json"
MARKDOWN_PATH = REPO_ROOT / "docs" / "test_inventory" / "TEST_INVENTORY.md"

# The suite as measured on the commit that introduced this file. These literals
# are the point of the file: if the artifact and these disagree, one of them is
# wrong and a human decides which -- regenerating is only the right repair when
# the JS suite really did change.
EXPECTED_TOTAL_CASES = 245
EXPECTED_TOTAL_FILES = 13
EXPECTED_PER_FILE = {
    "static/js/modules/__tests__/exercise-helpers.test.js": 15,
    "static/js/modules/__tests__/exercises.test.js": 29,
    "static/js/modules/__tests__/exports.test.js": 2,
    "static/js/modules/__tests__/fatigue-heatmap.test.js": 15,
    "static/js/modules/__tests__/fetch-wrapper.test.js": 3,
    "static/js/modules/__tests__/session-summary-helpers.test.js": 7,
    "static/js/modules/__tests__/summary-helpers.test.js": 22,
    "static/js/modules/__tests__/toast.test.js": 61,
    "static/js/modules/__tests__/user-profile-data.test.js": 12,
    "static/js/modules/__tests__/workout-controls-persistence.test.js": 35,
    "static/js/modules/__tests__/workout-plan-helpers.test.js": 13,
    "static/js/modules/__tests__/workout-plan-seams.test.js": 29,
    "static/js/modules/__tests__/workout-plan-state.test.js": 2,
}

# A root that exists on neither platform, built the same way the payload's file
# strings are, so path handling is pinned identically on Windows and Linux.
FAKE_ROOT = Path("/repo").resolve()


@pytest.fixture(scope="module")
def inventory() -> dict:
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def markdown() -> str:
    return MARKDOWN_PATH.read_text(encoding="utf-8")


def _abs(relative: str) -> str:
    return str(FAKE_ROOT / relative)


def _payload(*rows: tuple[str, str]) -> str:
    return json.dumps([{"file": _abs(path), "name": name} for path, name in rows])


# --- the whole-artifact contract --------------------------------------------
#
# Not Vitest-specific, and kept here on purpose: these two assertions are what
# make the new surface's presence -- rather than only its contents -- load
# bearing. A test shaped "if the key exists, its total is 245" is satisfied by
# deleting the key.


def test_schema_version_is_pinned(inventory):
    assert inventory["schema_version"] == SCHEMA_VERSION == 2


def test_top_level_key_set_is_exact(inventory):
    assert set(inventory) == {
        "schema_version",
        "generator",
        "playwright",
        "pytest",
        "vitest",
        "hard_waits",
    }


# --- the vitest block --------------------------------------------------------


def test_vitest_block_key_set_is_exact(inventory):
    assert set(inventory["vitest"]) == {
        "collector",
        "total_cases",
        "total_files",
        "files",
        "cases",
    }


def test_vitest_totals_are_pinned(inventory):
    block = inventory["vitest"]
    assert block["total_cases"] == EXPECTED_TOTAL_CASES
    assert block["total_files"] == EXPECTED_TOTAL_FILES


def test_vitest_per_file_counts_are_pinned(inventory):
    rows = {row["file"]: row["cases"] for row in inventory["vitest"]["files"]}
    assert rows == EXPECTED_PER_FILE


def test_vitest_file_rows_have_exactly_file_and_cases(inventory):
    assert all(set(row) == {"file", "cases"} for row in inventory["vitest"]["files"])


def test_vitest_case_rows_have_exactly_file_and_name(inventory):
    assert all(set(row) == {"file", "name"} for row in inventory["vitest"]["cases"])


def test_vitest_case_rows_reconcile_with_both_totals(inventory):
    """The three ways the artifact states its own size must agree.

    Nothing in the generator derives these from each other at render time, so a
    renderer that emitted the wrong list would show up here.
    """
    block = inventory["vitest"]
    assert len(block["cases"]) == block["total_cases"]
    assert sum(row["cases"] for row in block["files"]) == block["total_cases"]
    assert len(block["files"]) == block["total_files"]


def test_vitest_case_rows_are_sorted(inventory):
    identities = [(row["file"], row["name"]) for row in inventory["vitest"]["cases"]]
    assert identities == sorted(identities)


def test_vitest_case_identities_are_unique(inventory):
    identities = [(row["file"], row["name"]) for row in inventory["vitest"]["cases"]]
    assert len(identities) == len(set(identities))


def test_vitest_case_files_match_the_file_table(inventory):
    block = inventory["vitest"]
    assert {row["file"] for row in block["cases"]} == {row["file"] for row in block["files"]}


def test_vitest_paths_are_repo_relative_posix(inventory):
    block = inventory["vitest"]
    for path in [row["file"] for row in block["files"]] + [
        row["file"] for row in block["cases"]
    ]:
        assert "\\" not in path, path
        assert ":" not in path, path
        assert not path.startswith("/"), path
        assert ".." not in path.split("/"), path
        assert path.startswith("static/js/"), path
        assert path.endswith(".test.js"), path


def test_vitest_block_records_no_status_and_no_duration(inventory):
    """`vitest list` cannot see a skipped or todo case at all.

    Recording a status field would be a claim the collector cannot support, and
    `duration` would only be available from `vitest run`, which is rejected.
    """
    serialized = json.dumps(inventory["vitest"])
    assert '"status"' not in serialized
    assert '"duration"' not in serialized


def test_collector_string_matches_the_argv_actually_run(inventory):
    assert inventory["vitest"]["collector"] == VITEST_COLLECTOR
    argv = _vitest_list_argv(Path("/tmp/vitest-list.json"))
    assert VITEST_COLLECTOR == "vitest list --json=<path>"
    assert argv[1:3] == ["vitest", "list"]
    assert argv[3].startswith("--json=")


# --- the argv ----------------------------------------------------------------


def test_argv_lists_and_never_runs():
    """The collector may not become `vitest run`.

    Running the suite would put machine-speed durations into a file whose whole
    contract is determinism, and would make a required context fail on JS test
    outcomes -- which is decision D2's call, and D2 is not signed. Without this
    assertion that commitment is prose a later change can undo silently.
    """
    argv = _vitest_list_argv(Path("/tmp/vitest-list.json"))
    assert "list" in argv
    assert "run" not in argv
    assert not any(arg.startswith("--reporter") for arg in argv)
    assert not any(arg.startswith("--outputFile") for arg in argv)


def test_argv_writes_to_the_given_file_and_not_stdout():
    argv = _vitest_list_argv(Path("/tmp/somewhere/vitest-list.json"))
    assert argv[-1] == "--json=/tmp/somewhere/vitest-list.json"


def test_argv_uses_the_npx_it_is_given():
    """The executable is a parameter so this file never resolves one."""
    assert _vitest_list_argv(Path("/tmp/x.json"), "/usr/bin/npx")[0] == "/usr/bin/npx"


def test_the_call_site_uses_the_pinned_argv_and_pins_CI(monkeypatch, tmp_path):
    """The argv commitment has to bind the CALL SITE, not only the helper.

    Every assertion above pins `_vitest_list_argv`. Nothing stops a later change
    from inlining a different command into `_run_vitest_list` -- `vitest run`
    included -- and leaving all of them green.

    `_npx` is REPLACED here, never invoked: node is on the `Run Tests` job's
    PATH, so the real one resolves successfully and a shelling test would attempt
    a registry fetch inside a required job. `subprocess.run` is replaced for the
    same reason -- no runner starts.
    """
    captured: list[tuple[list[str], dict[str, str], Path]] = []

    def fake_run(argv, **kwargs):
        captured.append((argv, kwargs["env"], kwargs["cwd"]))
        Path(argv[-1].split("=", 1)[1]).write_text("[]", encoding="utf-8")
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr(generator, "_npx", lambda: "FAKE-NPX")
    monkeypatch.setattr(generator.subprocess, "run", fake_run)

    output = tmp_path / "vitest-list.json"
    assert _run_vitest_list(output) == "[]"
    argv, env, cwd = captured[0]
    assert argv == _vitest_list_argv(output, "FAKE-NPX")
    assert env["CI"] == "true"
    assert cwd == generator.REPO_ROOT


# --- the parser: happy path --------------------------------------------------


def test_parser_returns_counts_and_sorted_identities():
    payload = _payload(
        ("static/js/modules/__tests__/b.test.js", "suite > second"),
        ("static/js/modules/__tests__/a.test.js", "suite > zulu"),
        ("static/js/modules/__tests__/a.test.js", "suite > alpha"),
    )
    counts, identities = parse_vitest_listing(payload, FAKE_ROOT)
    assert counts == {
        "static/js/modules/__tests__/a.test.js": 2,
        "static/js/modules/__tests__/b.test.js": 1,
    }
    assert identities == [
        ("static/js/modules/__tests__/a.test.js", "suite > alpha"),
        ("static/js/modules/__tests__/a.test.js", "suite > zulu"),
        ("static/js/modules/__tests__/b.test.js", "suite > second"),
    ]


def test_parser_sorts_a_shuffled_payload_into_the_same_order():
    """Listing order is not stable between runs; the committed order must be."""
    rows = [
        ("static/js/modules/__tests__/a.test.js", "b"),
        ("static/js/modules/__tests__/a.test.js", "a"),
        ("static/js/modules/__tests__/c.test.js", "a"),
        ("static/js/modules/__tests__/b.test.js", "a"),
    ]
    first = parse_vitest_listing(_payload(*rows), FAKE_ROOT)[1]
    second = parse_vitest_listing(_payload(*reversed(rows)), FAKE_ROOT)[1]
    assert first == second == sorted(first)


def test_parser_emits_posix_separators_from_native_paths():
    """`_abs` produces backslashes on Windows; the artifact must never carry them."""
    payload = _payload(("static/js/modules/__tests__/a.test.js", "case"))
    assert "\\" not in parse_vitest_listing(payload, FAKE_ROOT)[1][0][0]


def test_parser_accepts_forward_slash_absolute_paths():
    """What the lister actually emits on Windows: an absolute path, POSIX-separated."""
    payload = json.dumps(
        [
            {
                "file": _abs("static/js/modules/__tests__/a.test.js").replace("\\", "/"),
                "name": "case",
            }
        ]
    )
    counts, _ = parse_vitest_listing(payload, FAKE_ROOT)
    assert counts == {"static/js/modules/__tests__/a.test.js": 1}


def test_parser_keeps_a_case_name_containing_the_delimiter_whole():
    """The `>` join is not invertible, so the joined string is never re-split."""
    name = "name with > angle > has > inside name"
    payload = _payload(("static/js/modules/__tests__/a.test.js", name))
    assert parse_vitest_listing(payload, FAKE_ROOT)[1][0][1] == name


# --- the parser: fails closed ------------------------------------------------


def test_parser_rejects_invalid_json():
    with pytest.raises(SystemExit) as excinfo:
        parse_vitest_listing("RAW STDOUT WRITE\n[]", FAKE_ROOT)
    assert COLLECTION_FAILURE in str(excinfo.value)
    assert "not valid JSON" in str(excinfo.value)


def test_parser_rejects_a_truncated_payload():
    payload = _payload(("static/js/modules/__tests__/a.test.js", "case"))
    with pytest.raises(SystemExit) as excinfo:
        parse_vitest_listing(payload[: len(payload) // 2], FAKE_ROOT)
    assert COLLECTION_FAILURE in str(excinfo.value)


def test_parser_rejects_a_non_list_payload():
    with pytest.raises(SystemExit) as excinfo:
        parse_vitest_listing('{"tests": []}', FAKE_ROOT)
    assert "expected a list" in str(excinfo.value)


def test_parser_refuses_an_empty_listing():
    with pytest.raises(SystemExit) as excinfo:
        parse_vitest_listing("[]", FAKE_ROOT)
    assert "refusing to write an empty inventory" in str(excinfo.value)


def test_parser_rejects_an_element_missing_a_key():
    payload = json.dumps([{"file": _abs("static/js/modules/__tests__/a.test.js")}])
    with pytest.raises(SystemExit) as excinfo:
        parse_vitest_listing(payload, FAKE_ROOT)
    assert "expected exactly ['file', 'name']" in str(excinfo.value)


def test_parser_rejects_an_element_with_an_extra_key():
    """A superset is a format change, not a bonus.

    An "at least these keys" check would pass a changed output format and commit
    a number derived from a shape nobody has read.
    """
    payload = json.dumps(
        [
            {
                "file": _abs("static/js/modules/__tests__/a.test.js"),
                "name": "case",
                "status": "skipped",
            }
        ]
    )
    with pytest.raises(SystemExit) as excinfo:
        parse_vitest_listing(payload, FAKE_ROOT)
    assert "expected exactly ['file', 'name']" in str(excinfo.value)


@pytest.mark.parametrize(
    "entry",
    [
        {"file": _abs("static/js/a.test.js"), "name": None},
        {"file": _abs("static/js/a.test.js"), "name": 7},
        {"file": 7, "name": "case"},
        {"file": None, "name": "case"},
    ],
    ids=["null-name", "int-name", "int-file", "null-file"],
)
def test_parser_rejects_non_string_values(entry):
    """Right key names, wrong value types.

    Without this, a null `name` survives until `identities.sort()` raises
    TypeError and a non-string `file` raises out of `Path()` -- both bare
    tracebacks on a job whose CI annotation says "regenerate the inventory".
    """
    with pytest.raises(SystemExit) as excinfo:
        parse_vitest_listing(json.dumps([entry]), FAKE_ROOT)
    assert COLLECTION_FAILURE in str(excinfo.value)
    assert "string values" in str(excinfo.value)


def test_parser_rejects_a_non_dict_element():
    with pytest.raises(SystemExit) as excinfo:
        parse_vitest_listing('["static/js/a.test.js > case"]', FAKE_ROOT)
    assert "expected exactly ['file', 'name']" in str(excinfo.value)


def test_parser_rejects_a_file_outside_the_repository():
    payload = json.dumps(
        [{"file": str(Path("/elsewhere").resolve() / "a.test.js"), "name": "case"}]
    )
    with pytest.raises(SystemExit) as excinfo:
        parse_vitest_listing(payload, FAKE_ROOT)
    assert "outside the repository" in str(excinfo.value)


def test_parser_rejects_a_relative_file_path():
    payload = json.dumps(
        [{"file": "static/js/modules/__tests__/a.test.js", "name": "case"}]
    )
    with pytest.raises(SystemExit) as excinfo:
        parse_vitest_listing(payload, FAKE_ROOT)
    assert "outside the repository" in str(excinfo.value)


def test_parser_treats_duplicate_identities_as_a_hard_failure():
    """De-duplicating would under-count and stay green."""
    payload = _payload(
        ("static/js/modules/__tests__/a.test.js", "same > name"),
        ("static/js/modules/__tests__/a.test.js", "same > name"),
    )
    with pytest.raises(SystemExit) as excinfo:
        parse_vitest_listing(payload, FAKE_ROOT)
    assert "duplicate (file, name) identities" in str(excinfo.value)
    assert "same > name" in str(excinfo.value)


def test_every_failure_message_disowns_the_regenerate_advice():
    """The CI annotation says "regenerate"; on this path that is the wrong repair."""
    payloads = ["not json", '{"a": 1}', "[]", '[{"file": "x"}]']
    for payload in payloads:
        with pytest.raises(SystemExit) as excinfo:
            parse_vitest_listing(payload, FAKE_ROOT)
        assert str(excinfo.value).startswith(COLLECTION_FAILURE), payload


def test_quoted_child_output_survives_a_non_utf8_console():
    """A failure message must not fail while being printed.

    `vitest` writes U+276F into its stack frames. On a cp1252 console the
    `SystemExit` message raises UnicodeEncodeError as Python prints it, and the
    diagnostic is replaced by a traceback about the diagnostic -- measured, on
    exactly the fail-closed path this file exists to protect. cp1252 is named
    explicitly so the substitution is exercised on Linux too.
    """
    safe = _console_safe("frame ❯ at line 1", "cp1252")
    assert "❯" not in safe
    safe.encode("cp1252")  # would raise if the substitution had not happened


def test_console_safe_leaves_encodable_text_alone():
    assert _console_safe("plain ASCII diagnostic", "cp1252") == "plain ASCII diagnostic"


def test_console_safe_defaults_to_the_real_stderr_encoding(monkeypatch):
    """Every production call site omits the encoding, so the DEFAULT must work.

    Pinning only the explicit-encoding form would leave `codec = encoding or
    "utf-8"` -- which restores the original bug in full -- passing both other
    tests here.
    """
    monkeypatch.setattr(sys, "stderr", io.TextIOWrapper(io.BytesIO(), encoding="cp1252"))
    safe = _console_safe("frame ❯ at line 1")
    assert "❯" not in safe
    safe.encode("cp1252")


# --- the committed Markdown --------------------------------------------------
#
# `--check` compares committed against regenerated, so it cannot see a renderer
# that never emits a section against a committed file that never contains one.
# Nothing else in the repository parses this file; these assertions are the only
# oracle it has.


def test_markdown_has_the_vitest_section(markdown):
    assert "\n## Vitest test files\n" in markdown


def test_markdown_totals_row_is_pinned(markdown):
    assert (
        f"| JS unit cases (Vitest) | **{EXPECTED_TOTAL_CASES}** "
        f"across {EXPECTED_TOTAL_FILES} files |"
    ) in markdown


def test_markdown_lists_every_vitest_file_with_its_count(markdown):
    section = markdown.split("\n## Vitest test files\n", 1)[1].split("\n## ", 1)[0]
    for path, cases in EXPECTED_PER_FILE.items():
        assert f"| `{path}` | {cases} |" in section


def test_markdown_discloses_that_skipped_cases_are_invisible(markdown):
    section = markdown.split("\n## Vitest test files\n", 1)[1].split("\n## ", 1)[0]
    assert "`.skip`" in section
    assert "no status" in section.lower()


def test_markdown_points_at_the_json_for_case_identities(markdown):
    section = markdown.split("\n## Vitest test files\n", 1)[1].split("\n## ", 1)[0]
    assert "vitest.cases" in section
