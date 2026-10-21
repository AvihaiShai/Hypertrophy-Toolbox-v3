"""G7: attempt-preserving Playwright retry report and its CI wiring.

Behaviour runs against tests/fixtures/ci_retry_report/: sanitized copies of real Playwright
1.61.0 JSON reporter captures of browser-free synthetic specs, with machine paths replaced by
placeholders. Their provenance is recorded in docs/ci_cd_expansion/PLANNING.md's G7 section.
Every malformed, partial or inconsistent report is derived from them in tmp_path.
"""
from __future__ import annotations

import ast
import configparser
import copy
import json
import os
import re
import shlex
import subprocess
import sys
import tomllib
from collections.abc import Callable
from pathlib import Path
from typing import Any, NamedTuple

import pytest

from scripts import ci_retry_report as retry_report
from tests.test_release_workflow_contracts import (
    CI,
    job_name,
    jobs,
    run_script,
    step_condition,
    step_env,
    steps,
    strip_comments,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "ci_retry_report"
SCRIPT = ROOT / "scripts" / "ci_retry_report.py"
PLAYWRIGHT_CONFIG = ROOT / "playwright.config.ts"

CAPTURES = (
    "clean.json",
    "mixed.json",
    "small-shard-1-of-2.json",
    "small-shard-2-of-2.json",
    "small-projects.json",
    "max-failures.json",
    "global-timeout.json",
    "load-error.json",
)
CLASSIFICATIONS = (
    "first-attempt",
    "recovered",
    "rerun",
    "exhausted",
    "failed",
    "skipped",
    "did-not-run",
    "interrupted",
)
RESULT_KEYS = {"status", "reason", "detail", "reporter_version", "shard", "retry_policy", "tests", "counts"}
SEP = " › "
NOT_ZERO = "Retry totals are unavailable; this is not a report of zero retries."
LABEL = "Retry Report Label"
PRIOR = "### Earlier step\n\nkept as written\n"

Row = tuple[str, int, str, str, list[tuple[int, str]], str]
Edit = Callable[[Any], object]
Source = Callable[[Path], Path]


# ------------------------------------------------------------------ fixture helpers


def load(name: str) -> Any:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def write(tmp_path: Path, data: Any, name: str = "results.json") -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / name
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def entries(data):
    """(spec, title path, test) in report order: a suite's specs, then its nested suites."""

    def walk(suite, titles):
        for spec in suite.get("specs", []):
            for test in spec["tests"]:
                yield spec, SEP.join([*titles, spec["title"]]), test
        for child in suite.get("suites", []) or []:
            yield from walk(child, [*titles, child["title"]])

    for file_suite in data["suites"]:
        yield from walk(file_suite, [])


def find(data, title, project=None):
    found = [test for _, path, test in entries(data) if path == title and project in (None, test["projectId"])]
    assert len(found) == 1, title
    return found[0]


def outcome(test) -> str:
    """Playwright's computeTestCaseOutcome over a test's results."""
    expected = unexpected = skipped = 0
    for result in test["results"]:
        status = result["status"]
        if status == "interrupted":
            continue
        if status == "skipped":
            skipped += test["expectedStatus"] == "skipped"
        elif status == test["expectedStatus"]:
            expected += 1
        else:
            unexpected += 1
    if not expected and not unexpected:
        return "skipped"
    if not unexpected:
        return "expected"
    if not expected and not skipped:
        return "unexpected"
    return "flaky"


def restat(data):
    """Recompute each test status and the top-level stats, so a variant isolates one defect."""
    stats = {"expected": 0, "skipped": 0, "unexpected": 0, "flaky": 0}
    for _, _, test in entries(data):
        test["status"] = outcome(test)
        stats[test["status"]] += 1
    data["stats"].update(stats)


def observed(data):
    return [
        {
            "file": spec["file"],
            "line": spec["line"],
            "title": title,
            "project": test["projectId"],
            "expected_status": test["expectedStatus"],
            "attempts": [
                {"retry": result["retry"], "status": result["status"], "duration_ms": result["duration"]}
                for result in test["results"]
            ],
        }
        for spec, title, test in entries(data)
    ]


def parsed(result):
    """result['tests'] reduced to the contract fields; extra keys are not this test's business."""
    return [
        {key: test[key] for key in ("file", "line", "title", "project", "expected_status")}
        | {"attempts": [{key: attempt[key] for key in ("retry", "status", "duration_ms")} for attempt in test["attempts"]]}
        for test in result["tests"]
    ]


def attempts(test):
    return [(attempt["retry"], attempt["status"]) for attempt in test["attempts"]]


def sequence(result) -> list[Row]:
    return [
        (test["file"], test["line"], test["title"], test["project"], attempts(test), test["classification"])
        for test in result["tests"]
    ]


def by_title(result, project="chromium"):
    found = {}
    for test in result["tests"]:
        if test["project"] == project:
            assert test["title"] not in found, test["title"]
            found[test["title"]] = test
    return found


def analyze(path: Path, step: str = "success", shard: str | None = None):
    return retry_report.analyze(path, step_outcome=step, expect_shard=shard)


def counts(**found: int) -> dict[str, int]:
    return {name: found.get(name.replace("-", "_"), 0) for name in CLASSIFICATIONS}


def rows(file: str, project: str, *specs: tuple[int, str, tuple[str, ...], str]) -> list[Row]:
    return [
        (file, line, title, project, list(enumerate(statuses)), classification)
        for line, title, statuses, classification in specs
    ]


def captured(name: str, edit: Edit | None = None) -> Source:
    def build(tmp_path: Path) -> Path:
        if edit is None:
            return FIXTURES / name
        data = load(name)
        edit(data)
        return write(tmp_path, data)

    return build


def absent(tmp_path: Path) -> Path:
    return tmp_path / "never-written" / "results.json"


def clean_bytes() -> bytes:
    return (FIXTURES / "clean.json").read_bytes()


def truncated_bytes() -> bytes:
    raw = clean_bytes()
    return raw[: len(raw) // 2]


def truncated(tmp_path: Path) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "results.json"
    path.write_bytes(truncated_bytes())
    return path


def on_test(title: str, change: Edit, project: str | None = None) -> Edit:
    return lambda data: change(find(data, title, project))


def set_version(version: str) -> Edit:
    return lambda data: data["config"].update(version=version)


def then_restat(*edits: Edit) -> Edit:
    def edit(data):
        for change in edits:
            change(data)
        restat(data)

    return edit


# ------------------------------------------------------------------ expected readings

D, S = "default-mode.spec.ts", "serial-mode.spec.ts"

CLEAN = rows(
    "clean.spec.ts", "chromium",
    (3, "clean one", ("passed",), "first-attempt"),
    (7, "clean two", ("passed",), "first-attempt"),
    (12, "clean group › clean three", ("passed",), "first-attempt"),
)
MIXED = rows(
    D, "chromium",
    (3, "passes first attempt", ("passed",), "first-attempt"),
    (7, "fails then recovers", ("failed", "passed"), "recovered"),
    (11, "times out then recovers", ("timedOut", "passed"), "recovered"),
    (18, "fails every attempt", ("failed", "failed", "failed"), "exhausted"),
    (22, "expected failure", ("failed",), "first-attempt"),
    (27, "unexpected pass of an expected failure", ("passed", "passed", "passed"), "exhausted"),
    (32, "skipped", ("skipped",), "skipped"),
    (37, "group › same title", ("passed",), "first-attempt"),
    (43, "other group › same title", ("failed", "passed"), "recovered"),
) + rows(
    S, "chromium",
    (4, "serial recovers › serial first passes", ("passed", "passed"), "rerun"),
    (7, "serial recovers › serial second fails once", ("failed", "passed"), "recovered"),
    (10, "serial recovers › serial third after second", ("skipped", "passed"), "rerun"),
    (16, "serial exhausts › serial head passes", ("passed", "passed", "passed"), "rerun"),
    (19, "serial exhausts › serial middle always fails", ("failed", "failed", "failed"), "exhausted"),
    (22, "serial exhausts › serial tail never runs", ("skipped", "skipped", "skipped"), "did-not-run"),
)
MIXED_COUNTS = counts(first_attempt=3, recovered=4, rerun=3, exhausted=3, skipped=1, did_not_run=1)
SHARD_1 = rows(
    "small-a.spec.ts", "chromium",
    (3, "small pass", ("passed",), "first-attempt"),
    (7, "small recovers", ("failed", "passed"), "recovered"),
)
SHARD_2 = rows("small-b.spec.ts", "chromium", (3, "small recovers", ("failed", "failed", "passed"), "recovered"))
PROJECTS = [
    *rows("small-a.spec.ts", "alpha", (3, "small pass", ("passed",), "first-attempt")),
    *rows("small-a.spec.ts", "alpha", (7, "small recovers", ("failed", "passed"), "recovered")),
    *rows("small-a.spec.ts", "beta", (3, "small pass", ("passed",), "first-attempt")),
    *rows("small-a.spec.ts", "beta", (7, "small recovers", ("failed", "passed"), "recovered")),
]
# Interrupted runs leave never-started tests with no results and expectedStatus "passed".
NEVER_STARTED = (
    (22, "expected failure", (), "did-not-run"),
    (27, "unexpected pass of an expected failure", (), "did-not-run"),
    (32, "skipped", (), "did-not-run"),
    (37, "group › same title", (), "did-not-run"),
    (43, "other group › same title", (), "did-not-run"),
)
MAX_FAILURES = rows(
    D, "chromium",
    (3, "passes first attempt", ("passed",), "first-attempt"),
    (7, "fails then recovers", ("failed", "passed"), "recovered"),
    (11, "times out then recovers", ("timedOut", "passed"), "recovered"),
    (18, "fails every attempt", ("failed", "failed", "failed"), "exhausted"),
    *NEVER_STARTED,
)
GLOBAL_TIMEOUT = rows(
    D, "chromium",
    (3, "passes first attempt", ("passed",), "first-attempt"),
    (7, "fails then recovers", ("failed", "passed"), "recovered"),
    (11, "times out then recovers", ("timedOut", "passed"), "recovered"),
    (18, "fails every attempt", ("failed",), "failed"),
    *NEVER_STARTED,
)


class Expected(NamedTuple):
    step: str
    status: str
    shard: str | None
    policy: dict[str, int]
    counts: dict[str, int]
    rows: list[Row]


AVAILABLE = {
    "clean.json": Expected("success", "no-retries", None, {"chromium": 2}, counts(first_attempt=3), CLEAN),
    "mixed.json": Expected("failure", "retries", None, {"chromium": 2}, MIXED_COUNTS, MIXED),
    "small-shard-1-of-2.json": Expected(
        "success", "retries", "1/2", {"chromium": 2}, counts(first_attempt=1, recovered=1), SHARD_1
    ),
    "small-shard-2-of-2.json": Expected("success", "retries", "2/2", {"chromium": 2}, counts(recovered=1), SHARD_2),
    "small-projects.json": Expected(
        "success", "retries", None, {"alpha": 2, "beta": 2}, counts(first_attempt=2, recovered=2), PROJECTS
    ),
}
PARTIAL_CAPTURES = {"max-failures.json": MAX_FAILURES, "global-timeout.json": GLOBAL_TIMEOUT, "load-error.json": []}


def assert_unavailable(result, reason):
    assert set(result) == RESULT_KEYS
    assert (result["status"], result["reason"], result["counts"]) == ("unavailable", reason, None)
    assert isinstance(result["detail"], str) and result["detail"].strip()


# ------------------------------------------------------------------ pins


@pytest.mark.parametrize("name", CAPTURES)
def test_every_capture_is_a_supported_playwright_json_report(name):
    assert load(name)["config"]["version"] in retry_report.SUPPORTED_PLAYWRIGHT_VERSIONS


def test_supported_versions_include_the_pinned_playwright():
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    pinned = package["devDependencies"]["@playwright/test"]
    # A Playwright bump must re-verify the JSON reporter shape before G7 trusts it.
    assert pinned in retry_report.SUPPORTED_PLAYWRIGHT_VERSIONS


def test_the_script_imports_only_the_standard_library():
    modules = set()
    for node in ast.walk(ast.parse(SCRIPT.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0, "relative import"
            modules.add((node.module or "").split(".")[0])
    assert "json" in modules
    assert sorted(module for module in modules if module not in sys.stdlib_module_names) == []


@pytest.mark.parametrize("name", CAPTURES)
def test_the_outcome_rule_reproduces_every_capture(name):
    # Guards the variant builders below: restat() must agree with what Playwright wrote.
    data = load(name)
    rebuilt = copy.deepcopy(data)
    restat(rebuilt)
    assert rebuilt == data


# ------------------------------------------------------------------ available reports


@pytest.mark.parametrize("name", AVAILABLE)
def test_an_available_report_classifies_every_test_in_report_order(name):
    expected = AVAILABLE[name]
    result = analyze(FIXTURES / name, expected.step)
    assert set(result) == RESULT_KEYS
    assert json.loads(json.dumps(result)) == result
    assert (result["status"], result["reason"], result["detail"]) == (expected.status, None, "")
    assert (result["reporter_version"], result["shard"]) == ("1.61.0", expected.shard)
    assert result["retry_policy"] == expected.policy
    assert result["counts"] == expected.counts
    assert sum(expected.counts.values()) == len(result["tests"])
    assert sequence(result) == expected.rows


@pytest.mark.parametrize("name", CAPTURES)
def test_every_attempt_is_preserved(name):
    data = load(name)
    step = AVAILABLE[name].step if name in AVAILABLE else "failure"
    assert parsed(analyze(FIXTURES / name, step)) == observed(data)


def test_failures_and_timeouts_that_pass_on_retry_are_recovered():
    tests = by_title(analyze(FIXTURES / "mixed.json", "failure"))
    found = {title: (attempts(tests[title]), tests[title]["classification"]) for title in (
        "fails then recovers",
        "times out then recovers",
        "other group › same title",
        "serial recovers › serial second fails once",
    )}
    assert found == {
        "fails then recovers": ([(0, "failed"), (1, "passed")], "recovered"),
        "times out then recovers": ([(0, "timedOut"), (1, "passed")], "recovered"),
        "other group › same title": ([(0, "failed"), (1, "passed")], "recovered"),
        "serial recovers › serial second fails once": ([(0, "failed"), (1, "passed")], "recovered"),
    }


def test_exhausted_retries_include_an_unexpected_pass_and_a_serial_middle():
    tests = by_title(analyze(FIXTURES / "mixed.json", "failure"))
    found = {title: (attempts(tests[title]), tests[title]["classification"]) for title in (
        "fails every attempt",
        "unexpected pass of an expected failure",
        "serial exhausts › serial middle always fails",
    )}
    assert found == {
        "fails every attempt": ([(0, "failed"), (1, "failed"), (2, "failed")], "exhausted"),
        "unexpected pass of an expected failure": ([(0, "passed"), (1, "passed"), (2, "passed")], "exhausted"),
        "serial exhausts › serial middle always fails": ([(0, "failed"), (1, "failed"), (2, "failed")], "exhausted"),
    }


def test_expected_failure_and_skip_on_the_first_attempt_are_not_retries():
    tests = by_title(analyze(FIXTURES / "mixed.json", "failure"))
    assert (tests["expected failure"]["expected_status"], attempts(tests["expected failure"])) == (
        "failed", [(0, "failed")]
    )
    assert tests["expected failure"]["classification"] == "first-attempt"
    assert (attempts(tests["skipped"]), tests["skipped"]["classification"]) == ([(0, "skipped")], "skipped")


def test_serial_reruns_without_a_failure_are_rerun_and_a_never_run_tail_did_not_run():
    tests = by_title(analyze(FIXTURES / "mixed.json", "failure"))
    found = {title: (attempts(tests[title]), tests[title]["classification"]) for title in (
        "serial recovers › serial first passes",
        "serial recovers › serial third after second",
        "serial exhausts › serial head passes",
        "serial exhausts › serial tail never runs",
    )}
    assert found == {
        "serial recovers › serial first passes": ([(0, "passed"), (1, "passed")], "rerun"),
        "serial recovers › serial third after second": ([(0, "skipped"), (1, "passed")], "rerun"),
        "serial exhausts › serial head passes": ([(0, "passed"), (1, "passed"), (2, "passed")], "rerun"),
        "serial exhausts › serial tail never runs": ([(0, "skipped"), (1, "skipped"), (2, "skipped")], "did-not-run"),
    }


def test_equal_titles_in_different_describe_blocks_stay_distinct():
    tests = by_title(analyze(FIXTURES / "mixed.json", "failure"))
    first, second = tests["group › same title"], tests["other group › same title"]
    assert (first["line"], attempts(first), first["classification"]) == (37, [(0, "passed")], "first-attempt")
    assert (second["line"], attempts(second), second["classification"]) == (
        43, [(0, "failed"), (1, "passed")], "recovered"
    )


def test_shards_keep_their_identity_files_and_attempt_numbers():
    one = analyze(FIXTURES / "small-shard-1-of-2.json", "success", "1/2")
    two = analyze(FIXTURES / "small-shard-2-of-2.json", "success", "2/2")
    assert (one["status"], one["shard"], two["status"], two["shard"]) == ("retries", "1/2", "retries", "2/2")
    first, second = by_title(one)["small recovers"], by_title(two)["small recovers"]
    assert (first["file"], first["line"], attempts(first)) == ("small-a.spec.ts", 7, [(0, "failed"), (1, "passed")])
    assert (second["file"], second["line"], attempts(second)) == (
        "small-b.spec.ts", 3, [(0, "failed"), (1, "failed"), (2, "passed")]
    )
    assert first["classification"] == second["classification"] == "recovered"


def test_projects_keep_distinct_identities():
    result = analyze(FIXTURES / "small-projects.json", "success")
    recovered = [
        (test["project"], test["file"], test["line"], test["title"], attempts(test))
        for test in result["tests"]
        if test["classification"] == "recovered"
    ]
    assert recovered == [
        ("alpha", "small-a.spec.ts", 7, "small recovers", [(0, "failed"), (1, "passed")]),
        ("beta", "small-a.spec.ts", 7, "small recovers", [(0, "failed"), (1, "passed")]),
    ]


def merge_projects(data):
    """The JSON reporter's merged form: one spec holding one test per project."""
    suite = data["suites"][0]
    merged = []
    for spec in suite["specs"]:
        where = (spec["title"], spec["line"], spec["column"])
        twin = next((m for m in merged if (m["title"], m["line"], m["column"]) == where), None)
        if twin is None:
            merged.append(spec)
        else:
            twin["tests"].extend(spec["tests"])
    suite["specs"] = merged


def test_merged_project_specs_report_the_same_tests(tmp_path):
    data = load("small-projects.json")
    merge_projects(data)
    assert [len(spec["tests"]) for spec in data["suites"][0]["specs"]] == [2, 2]
    result = analyze(write(tmp_path, data), "success")
    assert (result["status"], result["counts"]) == ("retries", counts(first_attempt=2, recovered=2))
    assert sorted(sequence(result)) == sorted(PROJECTS)


def stop_after_first_attempt(data):
    del find(data, "fails every attempt")["results"][1:]
    restat(data)


def test_a_test_stopped_before_its_retries_ran_out_is_failed(tmp_path):
    path = captured("mixed.json", stop_after_first_attempt)(tmp_path)
    assert json.loads(path.read_text(encoding="utf-8"))["stats"] == load("mixed.json")["stats"]
    result = analyze(path, "failure")
    test = by_title(result)["fails every attempt"]
    assert (attempts(test), test["classification"]) == ([(0, "failed")], "failed")
    assert result["status"] == "retries"
    assert result["counts"] == counts(first_attempt=3, recovered=4, rerun=3, exhausted=2, failed=1, skipped=1, did_not_run=1)


def test_classification_follows_the_reported_retry_policy(tmp_path):
    path = captured("mixed.json", lambda data: data["config"]["projects"][0].update(retries=3))(tmp_path)
    result = analyze(path, "failure")
    assert result["retry_policy"] == {"chromium": 3}
    tests = by_title(result)
    assert {title: tests[title]["classification"] for title in (
        "fails every attempt",
        "unexpected pass of an expected failure",
        "serial exhausts › serial middle always fails",
    )} == dict.fromkeys(("fails every attempt", "unexpected pass of an expected failure",
                         "serial exhausts › serial middle always fails"), "failed")
    assert result["counts"] == counts(first_attempt=3, recovered=4, rerun=3, failed=3, skipped=1, did_not_run=1)


def test_a_skip_expected_test_without_results_is_not_partial(tmp_path):
    edit = then_restat(on_test("clean two", lambda test: test.update(expectedStatus="skipped", results=[])))
    result = analyze(captured("clean.json", edit)(tmp_path), "success")
    assert (result["status"], result["reason"]) == ("no-retries", None)
    assert result["counts"] == counts(first_attempt=2, skipped=1)


@pytest.mark.parametrize("retries,classification", ((0, "exhausted"), (2, "failed")))
def test_one_failed_attempt_is_exhausted_only_when_no_retry_was_allowed(tmp_path, retries, classification):
    def fail_once(data):
        data["config"]["projects"][0]["retries"] = retries
        find(data, "clean two")["results"][0]["status"] = "failed"
        restat(data)

    result = analyze(captured("clean.json", fail_once)(tmp_path), "failure")
    test = by_title(result)["clean two"]
    assert (attempts(test), test["classification"]) == ([(0, "failed")], classification)
    assert (result["status"], result["retry_policy"]) == ("no-retries", {"chromium": retries})


# ------------------------------------------------------------------ unavailable, never zero


def test_a_missing_report_is_unavailable_not_zero(tmp_path):
    result = analyze(absent(tmp_path), "success")
    assert_unavailable(result, "missing")
    assert (result["tests"], result["retry_policy"], result["reporter_version"], result["shard"]) == ([], {}, None, None)


UNREADABLE = {
    "truncated": truncated_bytes,
    "empty-file": lambda: b"",
    "not-utf-8": lambda: clean_bytes().replace(b"clean one", b"clean \xff"),
    "empty-object": lambda: b"{}",
    "array": lambda: b"[]",
    "null": lambda: b"null",
    "number": lambda: b"42",
    "string": lambda: b'"results"',
}


@pytest.mark.parametrize("damage", UNREADABLE)
def test_an_unreadable_report_is_malformed(tmp_path, damage):
    path = tmp_path / "results.json"
    path.write_bytes(UNREADABLE[damage]())
    result = analyze(path, "success")
    assert_unavailable(result, "malformed")
    assert result["tests"] == []


def append_first_spec_again(data):
    specs = data["suites"][0]["specs"]
    specs.append(copy.deepcopy(specs[0]))


MALFORMED: dict[str, tuple[str, Edit]] = {
    "no-config": ("clean.json", lambda data: data.pop("config")),
    "config-not-object": ("clean.json", lambda data: data.update(config=[])),
    "no-version": ("clean.json", lambda data: data["config"].pop("version")),
    "version-not-text": ("clean.json", lambda data: data["config"].update(version=1.61)),
    "no-projects": ("clean.json", lambda data: data["config"].pop("projects")),
    "projects-not-list": ("clean.json", lambda data: data["config"].update(projects={"chromium": 2})),
    "project-not-object": ("clean.json", lambda data: data["config"].update(projects=["chromium"])),
    "project-without-id": ("clean.json", lambda data: data["config"]["projects"][0].pop("id")),
    "project-retries-not-int": ("clean.json", lambda data: data["config"]["projects"][0].update(retries="2")),
    "no-suites": ("clean.json", lambda data: data.pop("suites")),
    "suites-not-list": ("clean.json", lambda data: data.update(suites={})),
    "no-errors": ("clean.json", lambda data: data.pop("errors")),
    "errors-not-list": ("clean.json", lambda data: data.update(errors="none")),
    "no-stats": ("clean.json", lambda data: data.pop("stats")),
    "stats-not-object": ("clean.json", lambda data: data.update(stats=[])),
    "stats-count-missing": ("clean.json", lambda data: data["stats"].pop("flaky")),
    "stats-count-not-int": ("clean.json", lambda data: data["stats"].update(expected="3")),
    "unknown-result-status": ("clean.json", on_test("clean one", lambda test: test["results"][0].update(status="flaky"))),
    "result-status-wrong-case": ("clean.json", on_test("clean one", lambda test: test["results"][0].update(status="Passed"))),
    "result-without-status": ("clean.json", on_test("clean one", lambda test: test["results"][0].pop("status"))),
    "unknown-expected-status": ("clean.json", on_test("clean one", lambda test: test.update(expectedStatus="bogus"))),
    "retry-not-int": ("clean.json", on_test("clean one", lambda test: test["results"][0].update(retry="0"))),
    "retry-not-from-zero": ("clean.json", on_test("clean one", lambda test: test["results"][0].update(retry=1))),
    "duplicate-retry": ("mixed.json", on_test("fails then recovers", lambda test: test["results"][1].update(retry=0))),
    "retry-gap": ("mixed.json", on_test("fails then recovers", lambda test: test["results"][1].update(retry=2))),
    "retries-out-of-order": ("mixed.json", on_test("fails then recovers", lambda test: test["results"].reverse())),
    "unknown-project": ("clean.json", on_test("clean one", lambda test: test.update(projectId="firefox"))),
    "duplicate-identity": ("clean.json", append_first_spec_again),
    "duplicate-identity-across-specs": (
        "small-projects.json",
        on_test("small recovers", lambda test: test.update(projectId="alpha"), project="beta"),
    ),
    # Structural damage the brief does not enumerate still has to fail closed.
    "spec-without-tests": ("clean.json", lambda data: data["suites"][0]["specs"][0].pop("tests")),
    "test-without-results": ("clean.json", on_test("clean one", lambda test: test.pop("results"))),
    "specs-not-list": ("clean.json", lambda data: data["suites"][0].update(specs={})),
    "suite-not-object": ("clean.json", lambda data: data.update(suites=["clean.spec.ts"])),
    "nested-suites-not-list": ("clean.json", lambda data: data["suites"][0].update(suites="clean group")),
    "line-not-int": ("clean.json", lambda data: data["suites"][0]["specs"][0].update(line="3")),
}


@pytest.mark.parametrize("damage", MALFORMED)
def test_a_structurally_invalid_report_is_malformed(tmp_path, damage):
    name, edit = MALFORMED[damage]
    result = analyze(captured(name, edit)(tmp_path), AVAILABLE[name].step)
    assert_unavailable(result, "malformed")
    assert result["tests"] == []


@pytest.mark.parametrize("version", ("1.62.1", "1.60.0", "1.61.1"))
def test_an_unpinned_playwright_version_is_unsupported(tmp_path, version):
    result = analyze(captured("clean.json", set_version(version))(tmp_path), "success")
    assert_unavailable(result, "unsupported-reporter")
    assert (result["tests"], result["reporter_version"]) == ([], version)


@pytest.mark.parametrize("name", PARTIAL_CAPTURES)
def test_an_interrupted_capture_is_partial_with_its_attempts_retained(name):
    result = analyze(FIXTURES / name, "failure")
    assert_unavailable(result, "partial")
    assert (result["reporter_version"], result["retry_policy"]) == ("1.61.0", {"chromium": 2})
    assert sequence(result) == PARTIAL_CAPTURES[name]
    assert parsed(result) == observed(load(name))


PARTIAL: dict[str, tuple[Edit, list[tuple[str, str]]]] = {
    "top-level-error": (
        lambda data: data["errors"].append({"message": "Error: worker process exited unexpectedly"}),
        [("clean one", "first-attempt"), ("clean two", "first-attempt"), ("clean group › clean three", "first-attempt")],
    ),
    "zero-tests": (then_restat(lambda data: data.update(suites=[])), []),
    "interrupted-attempt": (
        then_restat(on_test("clean two", lambda test: test["results"][0].update(status="interrupted"))),
        [("clean one", "first-attempt"), ("clean two", "interrupted"), ("clean group › clean three", "first-attempt")],
    ),
    "never-started": (
        then_restat(on_test("clean two", lambda test: test.update(results=[]))),
        [("clean one", "first-attempt"), ("clean two", "did-not-run"), ("clean group › clean three", "first-attempt")],
    ),
}


@pytest.mark.parametrize("case", PARTIAL)
def test_an_incomplete_report_is_partial_with_observed_tests_retained(tmp_path, case):
    edit, classified = PARTIAL[case]
    path = captured("clean.json", edit)(tmp_path)
    result = analyze(path, "success")
    assert_unavailable(result, "partial")
    assert [(test["title"], test["classification"]) for test in result["tests"]] == classified
    assert parsed(result) == observed(json.loads(path.read_text(encoding="utf-8")))


INCONSISTENT: dict[str, tuple[str, str, str | None, Edit | None]] = {
    "stats-undercount": ("clean.json", "success", None, lambda data: data["stats"].update(expected=2)),
    "stats-extra-flaky": ("clean.json", "success", None, lambda data: data["stats"].update(flaky=1)),
    "test-status": (
        "mixed.json", "failure", None, on_test("fails then recovers", lambda test: test.update(status="expected"))
    ),
    "other-shard": ("small-shard-1-of-2.json", "success", "2/2", None),
    "other-shard-total": ("small-shard-1-of-2.json", "success", "1/4", None),
    "unsharded-report": ("clean.json", "success", "1/4", None),
    "clean-but-step-failed": ("clean.json", "failure", None, None),
    "flaky-only-but-step-failed": ("small-shard-1-of-2.json", "failure", None, None),
    "unexpected-but-step-succeeded": ("mixed.json", "success", None, None),
    "step-cancelled": ("clean.json", "cancelled", None, None),
    "step-skipped": ("clean.json", "skipped", None, None),
    "step-empty": ("clean.json", "", None, None),
    "step-wrong-case": ("clean.json", "SUCCESS", None, None),
    "failing-step-cancelled": ("mixed.json", "cancelled", None, None),
}


@pytest.mark.parametrize("case", INCONSISTENT)
def test_an_inconsistent_report_is_unavailable_with_attempts_retained(tmp_path, case):
    name, step, shard, edit = INCONSISTENT[case]
    path = captured(name, edit)(tmp_path)
    result = analyze(path, step, shard)
    assert_unavailable(result, "inconsistent")
    assert parsed(result) == observed(json.loads(path.read_text(encoding="utf-8")))


def broken_version_and_retries(data):
    set_version("1.62.1")(data)
    find(data, "fails then recovers")["results"][1]["retry"] = 0


def error_and_bad_stats(data):
    data["errors"].append({"message": "Error: worker process exited unexpectedly"})
    data["stats"]["expected"] = 0


PRECEDENCE: dict[str, tuple[Source, str, str | None, str]] = {
    "missing-over-everything": (absent, "", "9/9", "missing"),
    "malformed-over-unsupported": (captured("mixed.json", broken_version_and_retries), "failure", None, "malformed"),
    "malformed-over-partial": (
        captured("max-failures.json", on_test("passes first attempt", lambda test: test["results"][0].update(status="flaky"))),
        "failure", None, "malformed",
    ),
    "unsupported-over-partial": (
        captured("global-timeout.json", set_version("1.62.1")), "failure", None, "unsupported-reporter"
    ),
    "unsupported-over-inconsistent": (captured("clean.json", set_version("1.62.1")), "failure", "1/4", "unsupported-reporter"),
    "partial-over-step-outcome": (captured("max-failures.json"), "success", None, "partial"),
    "partial-over-cancelled-step": (captured("load-error.json"), "cancelled", None, "partial"),
    "partial-over-shard": (captured("global-timeout.json"), "failure", "1/4", "partial"),
    "partial-over-stats": (captured("clean.json", error_and_bad_stats), "success", None, "partial"),
}


@pytest.mark.parametrize("case", PRECEDENCE)
def test_unavailable_reasons_follow_the_documented_precedence(tmp_path, case):
    source, step, shard, reason = PRECEDENCE[case]
    assert_unavailable(analyze(source(tmp_path), step, shard), reason)


# ------------------------------------------------------------------ CLI


def cli(directory: Path, capsys, report: Path, step: str, *, label=LABEL, shard=None, attempt=None):
    directory.mkdir(parents=True, exist_ok=True)
    summary = directory / "summary.md"
    if not summary.exists():
        summary.write_text(PRIOR, encoding="utf-8")
    argv = ["--report", str(report), "--label", label, "--step-outcome", step, "--summary-file", str(summary)]
    if shard is not None:
        argv += ["--expect-shard", shard]
    if attempt is not None:
        argv += ["--run-attempt", str(attempt)]
    code = retry_report.main(argv)
    out = capsys.readouterr().out
    text = summary.read_text(encoding="utf-8")
    assert text.startswith(PRIOR)
    return code, text[len(PRIOR):], out


def cells(line: str) -> list[str]:
    return [cell.strip().strip("`*").strip() for cell in line.strip().strip("|").split("|")]


def counts_table(markdown: str) -> dict[str, int]:
    """Rows of the per-classification counts table; test rows always carry ' › '."""
    found = {}
    for line in markdown.splitlines():
        if not line.lstrip().startswith("|") or SEP in line:
            continue
        values = cells(line)
        names = [value for value in values if value in CLASSIFICATIONS]
        numbers = [value for value in values if re.fullmatch(r"\d+", value)]
        if len(names) == 1 and len(numbers) == 1:
            assert names[0] not in found, line
            found[names[0]] = int(numbers[0])
    return found


def assert_row(markdown: str, row: Row):
    file, line, title, project, tries, classification = row
    identity = f"{file}:{line}{SEP}{title} [{project}]"
    found = [text for text in markdown.splitlines() if identity in text]
    assert len(found) == 1, (identity, found)
    assert classification in cells(found[0]), found[0]
    if tries:
        pattern = " → ".join(rf"#{retry} {re.escape(status)}(?: \([^)]*\))?" for retry, status in tries)
        assert re.search(pattern, found[0]), found[0]


UNESCAPED = {"25": "%", "0D": "\r", "0A": "\n", "3A": ":", "2C": ","}


def unescape(value: str) -> str:
    return re.sub(r"%(25|0D|0A|3A|2C)", lambda match: UNESCAPED[match.group(1)], value)


def commands(out: str) -> list[str]:
    return [line for line in out.splitlines() if line.startswith("::")]


def warning(out: str) -> str:
    """The single workflow command on stdout, checked for escaping; returns title + message, unescaped."""
    found = commands(out)
    assert len(found) == 1, found
    assert found[0].startswith("::warning "), found[0]
    head, separator, data = found[0][len("::warning "):].partition("::")
    assert separator, found[0]
    properties = {}
    for item in head.split(","):
        key, equals, value = item.partition("=")
        assert equals and ":" not in value and not re.search(r"%(?!25|0D|0A|3A|2C)", value), found[0]
        properties[key] = value
    assert "title" in properties, found[0]
    assert not re.search(r"%(?!25|0D|0A)", data), found[0]
    return f"{unescape(properties['title'])} {unescape(data)}"


CLI_STATUS: dict[str, tuple[Source, str, str, dict[str, int] | None]] = {
    "no-retries": (captured("clean.json"), "success", "no retries", counts(first_attempt=3)),
    "retries": (captured("mixed.json"), "failure", "retries observed", MIXED_COUNTS),
    "missing": (absent, "success", "unavailable (missing)", None),
    "malformed": (truncated, "success", "unavailable (malformed)", None),
    "unsupported-reporter": (
        captured("clean.json", set_version("1.62.1")), "success", "unavailable (unsupported-reporter)", None
    ),
    "partial": (captured("max-failures.json"), "failure", "unavailable (partial)", None),
    "inconsistent": (captured("clean.json"), "failure", "unavailable (inconsistent)", None),
    "cancelled-step": (captured("mixed.json"), "cancelled", "unavailable (inconsistent)", None),
}


@pytest.mark.parametrize("case", CLI_STATUS)
def test_cli_never_changes_the_verdict_and_states_the_status(tmp_path, capsys, case):
    source, step, status, expected_counts = CLI_STATUS[case]
    code, markdown, _ = cli(tmp_path, capsys, source(tmp_path), step)
    assert code == 0
    assert markdown.lstrip("\r\n").splitlines()[0] == f"### Retry report — {LABEL}"
    assert f"**Status:** {status}" in markdown
    assert f"Original test step outcome: `{step}`" in markdown
    if expected_counts is None:
        assert NOT_ZERO in markdown
        assert counts_table(markdown) == {}
    else:
        assert NOT_ZERO not in markdown
        assert counts_table(markdown) == expected_counts
        assert "chromium retries=2" in markdown


def test_cli_appends_to_the_step_summary_without_replacing_it(tmp_path, capsys):
    summary = tmp_path / "summary.md"
    summary.write_text(PRIOR, encoding="utf-8")
    for name, step in (("clean.json", "success"), ("mixed.json", "failure")):
        argv = ["--report", str(FIXTURES / name), "--label", LABEL, "--step-outcome", step, "--summary-file", str(summary)]
        assert retry_report.main(argv) == 0
    text = summary.read_text(encoding="utf-8")
    assert text.startswith(PRIOR)
    assert text.count(f"### Retry report — {LABEL}") == 2
    assert text.index("**Status:** no retries") < text.index("**Status:** retries observed")
    assert "### Retry report" not in capsys.readouterr().out


def test_cli_identifies_reporter_policy_run_attempt_and_shard(tmp_path, capsys):
    _, markdown, _ = cli(tmp_path / "shard", capsys, FIXTURES / "small-shard-1-of-2.json", "success", shard="1/2", attempt=3)
    for text in ("Playwright JSON 1.61.0", "chromium retries=2", "Workflow run attempt 3", "shard 1/2"):
        assert text in markdown
    _, markdown, _ = cli(tmp_path / "clean", capsys, FIXTURES / "clean.json", "success")
    assert "unsharded" in markdown
    _, markdown, _ = cli(tmp_path / "projects", capsys, FIXTURES / "small-projects.json", "success")
    assert "alpha retries=2" in markdown and "beta retries=2" in markdown
    _, markdown, _ = cli(tmp_path / "missing", capsys, absent(tmp_path), "success")
    assert "Playwright JSON (version unknown)" in markdown
    unsupported = captured("clean.json", set_version("1.62.1"))(tmp_path / "unsupported")
    _, markdown, _ = cli(tmp_path / "unsupported", capsys, unsupported, "success")
    assert "Playwright JSON 1.62.1" in markdown


def listed(table: list[Row]) -> list[Row]:
    return [row for row in table if len(row[4]) > 1 or row[5] not in ("first-attempt", "skipped")]


def test_cli_lists_every_retried_or_non_first_attempt_test_with_its_attempts(tmp_path, capsys):
    _, markdown, _ = cli(tmp_path, capsys, FIXTURES / "mixed.json", "failure")
    assert len(listed(MIXED)) == 11
    for row in listed(MIXED):
        assert_row(markdown, row)
    _, markdown, _ = cli(tmp_path / "projects", capsys, FIXTURES / "small-projects.json", "success")
    for row in listed(PROJECTS):
        assert_row(markdown, row)


UNAVAILABLE_ROWS: dict[str, tuple[Source, str, list[Row]]] = {
    "inconsistent": (captured("mixed.json"), "success", listed(MIXED)),
    "partial": (captured("max-failures.json"), "failure", listed(MAX_FAILURES)),
    "partial-stopped-early": (captured("global-timeout.json"), "failure", listed(GLOBAL_TIMEOUT)),
}


@pytest.mark.parametrize("case", UNAVAILABLE_ROWS)
def test_cli_keeps_test_rows_when_the_report_is_unavailable(tmp_path, capsys, case):
    source, step, expected = UNAVAILABLE_ROWS[case]
    _, markdown, _ = cli(tmp_path, capsys, source(tmp_path), step)
    assert NOT_ZERO in markdown
    assert expected
    for row in expected:
        assert_row(markdown, row)


@pytest.mark.parametrize("name,retried", (("small-shard-2-of-2.json", 1), ("small-projects.json", 2)))
def test_cli_warns_once_with_the_retried_test_count(tmp_path, capsys, name, retried):
    code, _, out = cli(tmp_path, capsys, FIXTURES / name, "success")
    assert code == 0
    text = warning(out)
    assert LABEL in text
    assert re.search(rf"(?<!\d){retried}(?!\d)", text), text


UNAVAILABLE_WARNINGS: dict[str, tuple[Source, str, str]] = {
    "missing": (absent, "success", "missing"),
    "malformed": (truncated, "success", "malformed"),
    "unsupported-reporter": (captured("clean.json", set_version("1.62.1")), "success", "unsupported-reporter"),
    "partial": (captured("max-failures.json"), "failure", "partial"),
    "inconsistent": (captured("clean.json"), "failure", "inconsistent"),
}


@pytest.mark.parametrize("case", UNAVAILABLE_WARNINGS)
def test_cli_warns_once_with_the_unavailable_reason(tmp_path, capsys, case):
    source, step, reason = UNAVAILABLE_WARNINGS[case]
    code, _, out = cli(tmp_path, capsys, source(tmp_path), step)
    assert code == 0
    text = warning(out)
    assert LABEL in text and reason in text


def test_cli_emits_no_annotation_when_nothing_retried(tmp_path, capsys):
    code, markdown, out = cli(tmp_path, capsys, FIXTURES / "clean.json", "success")
    assert code == 0 and "**Status:** no retries" in markdown
    assert commands(out) == []


@pytest.mark.parametrize("source", (absent, captured("small-shard-1-of-2.json")), ids=("unavailable", "retries"))
def test_cli_escapes_annotation_text(tmp_path, capsys, source):
    label = "Shard 1/4: 100%, ok\nsecond line"
    code, _, out = cli(tmp_path, capsys, source(tmp_path), "success", label=label)
    assert code == 0
    assert label in warning(out)


def test_cli_records_each_workflow_run_attempt(tmp_path, capsys):
    for attempt in (1, 2):
        code, _, _ = cli(tmp_path, capsys, FIXTURES / "small-shard-1-of-2.json", "success", shard="1/2", attempt=attempt)
        assert code == 0
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert text.count(f"### Retry report — {LABEL}") == 2
    assert text.index("Workflow run attempt 1") < text.index("Workflow run attempt 2")


def test_cli_without_a_summary_file_prints_markdown(capsys):
    argv = ["--report", str(FIXTURES / "clean.json"), "--label", LABEL, "--step-outcome", "success"]
    assert retry_report.main(argv) == 0
    out = capsys.readouterr().out
    assert f"### Retry report — {LABEL}" in out and "**Status:** no retries" in out
    assert commands(out) == []


def test_cli_reports_an_internal_error_as_unavailable(tmp_path, capsys, monkeypatch):
    def broken(*args, **kwargs):
        raise RuntimeError("simulated reporter defect")

    monkeypatch.setattr(retry_report, "analyze", broken)
    code, markdown, out = cli(tmp_path, capsys, FIXTURES / "clean.json", "success")
    assert code == 0
    assert "**Status:** unavailable (reporter-error)" in markdown and NOT_ZERO in markdown
    assert "Original test step outcome: `success`" in markdown
    assert "reporter-error" in warning(out)


def test_cli_step_outcome_is_free_text(tmp_path, capsys):
    code, markdown, _ = cli(tmp_path, capsys, FIXTURES / "clean.json", "neutral")
    assert code == 0 and "**Status:** unavailable (inconsistent)" in markdown


@pytest.mark.parametrize(
    "statuses,classification", ((("failed",), "failed"), (("passed", "passed", "passed"), "exhausted"))
)
def test_a_skip_expected_test_that_ran_is_never_hidden_as_skipped(tmp_path, capsys, statuses, classification):
    def ran(test):
        first = test["results"][0]
        test["results"] = [dict(first, status=status, retry=retry) for retry, status in enumerate(statuses)]

    path = captured("mixed.json", then_restat(on_test("skipped", ran)))(tmp_path)
    result = analyze(path, "failure")
    test = by_title(result)["skipped"]
    tries = list(enumerate(statuses))
    assert (test["expected_status"], attempts(test), test["classification"]) == ("skipped", tries, classification)
    assert result["status"] == "retries"
    code, markdown, _ = cli(tmp_path / "cli", capsys, path, "failure")
    assert code == 0
    assert_row(markdown, (D, 32, "skipped", "chromium", tries, classification))


def test_cli_prints_the_markdown_when_the_summary_file_cannot_be_written(tmp_path, capsys):
    directory = tmp_path / "summary-is-a-directory"
    directory.mkdir()
    argv = ["--report", str(FIXTURES / "clean.json"), "--label", LABEL, "--step-outcome", "success"]
    assert retry_report.main([*argv, "--summary-file", str(directory)]) == 0
    out = capsys.readouterr().out
    assert f"### Retry report — {LABEL}" in out and "**Status:** no retries" in out
    assert directory.is_dir() and not any(directory.iterdir())


def test_cli_keeps_a_backtick_title_inside_one_code_span(tmp_path, capsys):
    def rename(data):
        spec = next(spec for spec, title, _ in entries(data) if title == "fails then recovers")
        spec["title"] = "fails `then` recovers"

    path = captured("mixed.json", rename)(tmp_path)
    code, markdown, _ = cli(tmp_path / "cli", capsys, path, "failure")
    assert code == 0
    identity = f"`{D}:7{SEP}fails 'then' recovers [chromium]`"
    assert len([line for line in markdown.splitlines() if identity in line]) == 1, markdown
    assert "fails `then` recovers" not in markdown


REPORTS_TO_KEEP: dict[str, Source] = {
    "available": captured("mixed.json"),
    "partial": captured("max-failures.json"),
    "malformed": truncated,
}


@pytest.mark.parametrize("case", REPORTS_TO_KEEP)
def test_the_report_file_is_never_modified(tmp_path, capsys, case):
    path = tmp_path / "results.json"
    path.write_bytes(REPORTS_TO_KEEP[case](tmp_path / "source").read_bytes())
    before = (path.read_bytes(), path.stat().st_mtime_ns)
    analyze(path, "failure")
    assert (path.read_bytes(), path.stat().st_mtime_ns) == before
    code, _, _ = cli(tmp_path / "cli", capsys, path, "failure")
    assert code == 0
    assert (path.read_bytes(), path.stat().st_mtime_ns) == before


@pytest.mark.parametrize("missing", ("--report", "--label", "--step-outcome"))
def test_cli_usage_errors_still_exit_nonzero(capsys, missing):
    options = {"--report": str(FIXTURES / "clean.json"), "--label": LABEL, "--step-outcome": "success"}
    del options[missing]
    with pytest.raises(SystemExit) as raised:
        retry_report.main([token for pair in options.items() for token in pair])
    assert raised.value.code not in (0, None)
    capsys.readouterr()


@pytest.mark.parametrize(
    "source,step,status",
    ((captured("mixed.json"), "failure", "retries observed"), (absent, "failure", "unavailable (missing)")),
    ids=("failed-step-with-retries", "missing-report"),
)
def test_the_script_runs_standalone_and_exits_zero(tmp_path, source, step, status):
    summary = tmp_path / "summary.md"
    argv = ["--report", str(source(tmp_path)), "--label", LABEL, "--step-outcome", step, "--run-attempt", "2"]
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *argv, "--summary-file", str(summary)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Traceback" not in proc.stderr
    text = summary.read_text(encoding="utf-8")
    assert f"**Status:** {status}" in text and "Workflow run attempt 2" in text
    assert len([line for line in proc.stdout.splitlines() if line.startswith("::warning ")]) == 1


def test_the_script_survives_a_cp1252_console_without_a_summary_file():
    env = {key: value for key, value in os.environ.items() if key != "PYTHONUTF8"} | {"PYTHONIOENCODING": "cp1252"}
    argv = ["--report", str(FIXTURES / "mixed.json"), "--label", LABEL, "--step-outcome", "failure"]
    proc = subprocess.run([sys.executable, str(SCRIPT), *argv], cwd=ROOT, env=env, capture_output=True, check=False)
    out, err = (stream.decode("utf-8", errors="replace") for stream in (proc.stdout, proc.stderr))
    assert proc.returncode == 0, out + err
    assert "Traceback" not in err
    # ASCII fragments only: the separator and arrows may be re-encoded for the console.
    rows = [line for line in out.splitlines() if f"{D}:7" in line and "fails then recovers [chromium]" in line]
    assert len(rows) == 1, out
    assert all(token in rows[0] for token in ("recovered", "#0 failed", "#1 passed")), rows[0]


# ------------------------------------------------------------------ pytest rerun tripwire
#
# No pytest reporter is selected for G7 because nothing reruns pytest tests: no plugin is
# installed or configured. Introducing one must fail here and send G7 back for review.

RERUN_DISTRIBUTIONS = frozenset(
    {"pytest-rerunfailures", "pytest-rerun", "pytest-retry", "pytest-retries", "flaky", "pytest-flaky"}
)
# pytest-rerunfailures and flaky options, and pytest-rerunfailures' ini keys.
RERUN_OPTION = re.compile(
    r"--reruns\b|--reruns-delay\b|--only-rerun\b|--rerun-except\b|--force-flaky\b|--max-runs\b"
    r"|(?:^|\s)-p\s*(?:pytest_)?rerunfailures\b"
)
RERUN_INI_KEYS = frozenset({"reruns", "reruns_delay", "only_rerun", "rerun_except"})
# pytest-retry's option; only meaningful on a pytest command, since pip has its own --retries.
PYTEST_RETRY_OPTION = re.compile(r"--retries\b")
PYTEST_COMMAND = re.compile(r"(?:^|[\s;&|(])(?:python3?\s+-m\s+)?pytest(?=\s|$)")
PIP_INSTALL = re.compile(r"\bpip3?\s+install\b")
RUN_KEY = re.compile(r"^( *)(?:- )?run:[ \t]*(.*)$")
INI_SECTIONS = {"pytest.ini": "pytest", "setup.cfg": "tool:pytest", "tox.ini": "pytest"}
WORKFLOWS = ROOT / ".github" / "workflows"


def distribution(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def requirement_names(path: Path) -> set[str]:
    names = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or line.startswith("-"):
            continue
        match = re.match(r"[A-Za-z0-9][A-Za-z0-9._-]*", line)
        assert match, raw
        names.add(distribution(match.group(0)))
    return names


def test_no_pytest_rerun_plugin_is_required():
    files = sorted(ROOT.glob("requirements*.txt"))
    assert "pytest" in requirement_names(ROOT / "requirements.txt")
    assert {path.name: sorted(requirement_names(path) & RERUN_DISTRIBUTIONS) for path in files} == {
        path.name: [] for path in files
    }


def flat(value, key=""):
    if isinstance(value, dict):
        for inner_key, inner in value.items():
            yield from flat(inner, inner_key)
    else:
        yield key, str(value)


def pytest_settings() -> list[tuple[str, str, str]]:
    """(file, key, value) for every setting in the sections pytest reads its configuration from."""
    found = []
    for name, section in INI_SECTIONS.items():
        parser = configparser.ConfigParser(interpolation=None)
        if parser.read(ROOT / name, encoding="utf-8") and parser.has_section(section):
            found += [(name, key, value) for key, value in parser.items(section)]
    pyproject = ROOT / "pyproject.toml"
    if pyproject.is_file():
        tool = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("tool", {})
        found += [
            ("pyproject.toml", key, value)
            for name, section in tool.items()
            if name.startswith("pytest")
            for key, value in flat(section)
        ]
    return found


def workflow_run_lines():
    """(workflow, logical shell line) for every `run:` value in every workflow."""
    for path in sorted(WORKFLOWS.glob("*.y*ml")):
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            key = RUN_KEY.match(line)
            if key is None:
                continue
            script = key.group(2).strip()
            if re.fullmatch(r"[|>][-+0-9]*", script):
                indent, body = len(key.group(1)), []
                for following in lines[index + 1:]:
                    if following.strip() and len(following) - len(following.lstrip()) <= indent:
                        break
                    body.append(following)
                script = "\n".join(body)
            for logical in script.replace("\\\n", " ").replace("`\n", " ").splitlines():
                if logical.strip() and not logical.lstrip().startswith("#"):
                    yield path.name, logical.strip()


def installed(line: str) -> set[str]:
    words = PIP_INSTALL.split(line, maxsplit=1)[1].split()
    return {
        distribution(re.split(r"[<>=!~\[;]", word.strip("'\""), maxsplit=1)[0])
        for word in words
        if not word.startswith("-")
    }


def test_no_pytest_rerun_is_configured():
    settings = pytest_settings()
    assert any(name == "pytest.ini" for name, _, _ in settings)
    assert [setting for setting in settings if setting[1] in RERUN_INI_KEYS or RERUN_OPTION.search(setting[2])] == []


def test_no_workflow_reruns_pytest_or_installs_a_rerun_plugin():
    lines = list(workflow_run_lines())
    commands = [(name, line) for name, line in lines if PYTEST_COMMAND.search(line) and not PIP_INSTALL.search(line)]
    installs = [(name, line) for name, line in lines if PIP_INSTALL.search(line)]
    # Vacuity floors: the parser still sees ci.yml's pytest runs and its installs.
    assert any(name == "ci.yml" for name, _ in commands) and any(name == "ci.yml" for name, _ in installs)
    offenders = [(name, line) for name, line in commands if RERUN_OPTION.search(line) or PYTEST_RETRY_OPTION.search(line)]
    offenders += [(name, line) for name, line in installs if installed(line) & RERUN_DISTRIBUTIONS]
    offenders += [
        (path.name, line)
        for path in sorted(WORKFLOWS.glob("*.y*ml"))
        for line in strip_comments(path.read_text(encoding="utf-8")).splitlines()
        if "PYTEST_ADDOPTS" in line and (RERUN_OPTION.search(line) or PYTEST_RETRY_OPTION.search(line))
    ]
    assert offenders == []


def test_no_rerun_plugin_is_loaded_into_this_session(request):
    loaded = {distribution(dist.project_name) for _, dist in request.config.pluginmanager.list_plugin_distinfo()}
    assert loaded
    assert loaded & RERUN_DISTRIBUTIONS == set()
    assert request.config.getoption("reruns", default=None) is None


# ------------------------------------------------------------------ playwright.config.ts wiring

JUNIT_REPORTER = "['junit',{outputFile:path.join(playwrightArtifactsDir,'junit.xml')}]"
JSON_REPORTER = "['json',{outputFile:path.join(playwrightArtifactsDir,'results.json')}]"


def config_code() -> str:
    source = PLAYWRIGHT_CONFIG.read_text(encoding="utf-8")
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    source = re.sub(r"^[ \t]*//.*$", "", source, flags=re.MULTILINE)
    compact = re.sub(r"\s+", "", source).replace('"', "'")
    return compact.replace(",]", "]").replace(",}", "}")


def literal_array(code: str, prefix: str) -> str:
    """The inside of the bracketed array that `prefix` (ending in '[') opens."""
    start = code.find(prefix)
    assert start != -1, prefix
    opening, depth = start + len(prefix) - 1, 0
    for end in range(opening, len(code)):
        depth += {"[": 1, "]": -1}.get(code[end], 0)
        if depth == 0:
            return code[opening + 1:end]
    raise AssertionError(f"unbalanced {prefix}")


def test_the_playwright_retry_policy_is_unchanged():
    assert re.findall(r"retries:([^,}]*)", config_code()) == ["process.env.CI?2:0"]


def test_ci_reporters_write_json_beside_junit_and_only_in_ci():
    code = config_code()
    ci = re.search(r"constciReporters(?::[^=]*)?=process\.env\.CI\?\[(.*?)\]:\[\];", code)
    assert ci, "ciReporters must stay a CI-gated list with an empty local branch"
    reporters = re.findall(r"\[[^\[\]]*\]", ci.group(1))
    assert ",".join(reporters) == ci.group(1)
    assert sorted(reporters) == sorted([JUNIT_REPORTER, JSON_REPORTER])
    local = re.findall(r"\[[^\[\]]*\]|\.\.\.\w+", literal_array(code, "reporter:["))
    assert "['list']" in local and "...ciReporters" in local
    assert "'json'" not in code.replace(ci.group(0), "")


def test_the_json_report_lands_where_the_summary_reads_it():
    code = config_code()
    assert "constartifactsRoot=process.env.TEST_ARTIFACTS_DIR??'artifacts';" in code
    assert "constplaywrightArtifactsDir=path.join(artifactsRoot,'playwright');" in code
    for job_id in PLAYWRIGHT_JOBS:
        assert "TEST_ARTIFACTS_DIR" not in ci_block(job_id), job_id


# ------------------------------------------------------------------ ci.yml wiring

PLAYWRIGHT_JOBS = {
    "e2e-smoke": "E2E Smoke (Chromium)",
    "e2e-functional-shard": "E2E Functional Shard ${{ matrix.shard }}/4",
    "e2e-backup": "E2E Backup (Chromium, isolated)",
    "e2e-fatigue-context": "E2E Fatigue Context (Chromium, non-required)",
    "e2e-erase-flow": "E2E Erase Flow (Chromium, isolated, non-required)",
    "visual-windows": "Visual Regression (Windows baselines)",
}
# A `run:` block cannot expand the matrix expression, so the shard label comes from $SHARD.
LABELS = PLAYWRIGHT_JOBS | {"e2e-functional-shard": "E2E Functional Shard $SHARD"}
PLAYWRIGHT_STEPS = {
    "e2e-smoke": "Run smoke spec",
    "e2e-functional-shard": "Run functional specs (shard ${{ matrix.shard }}/4)",
    "e2e-backup": "Run backup spec",
    "e2e-fatigue-context": "Run fatigue-context spec",
    "e2e-erase-flow": "Run erase-flow spec",
    "visual-windows": "Run Windows visual suite (compare only)",
}
LINE_REPORTER_JOBS = frozenset({"e2e-smoke", "e2e-fatigue-context", "e2e-erase-flow"})
# These keep the config reporters, where ciReporters adds the JSON file under CI=true.
CONFIG_REPORTER_JOBS = frozenset({"e2e-functional-shard", "e2e-backup", "visual-windows"})
PWSH_JOBS = {"visual-windows"}
SHARDED_JOBS = {"e2e-functional-shard"}
SUMMARY_STEP = "Summarize Playwright retries"
REPORT_PATH = "artifacts/playwright/results.json"


def ci_block(job_id: str, *, comments: bool = False) -> str:
    block = jobs(CI).get(job_id)
    assert block is not None, f"ci.yml has no {job_id} job"
    return block if comments else strip_comments(block)


def playwright_step(job_id: str) -> tuple[str, str]:
    found = [(name, raw) for name, raw in steps(ci_block(job_id)) if "npx playwright test" in (run_script(raw) or "")]
    assert len(found) == 1, (job_id, [name for name, _ in found])
    return found[0]


def summary_step(job_id: str, *, comments: bool = False) -> str:
    found = [raw for name, raw in steps(ci_block(job_id, comments=comments)) if name == SUMMARY_STEP]
    assert len(found) == 1, f"{job_id} has {len(found)} '{SUMMARY_STEP}' steps"
    return found[0]


def step_values(raw: str, key: str) -> list[str]:
    """Values of a step-level `key:` line."""
    return [value.strip() for value in re.findall(rf"^      {key}:(.*)$", raw, re.MULTILINE)]


def words(script: str) -> list[str]:
    joined = script.replace("\\\n", " ").replace("`\n", " ")
    lines = [line for line in joined.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    assert len(lines) == 1, lines
    return shlex.split(lines[0])


def unquote(value: str) -> str:
    value = value.strip()
    return value[1:-1] if len(value) > 1 and value[0] == value[-1] and value[0] in "'\"" else value


def report_options(job_id: str) -> tuple[str, dict[str, str]]:
    script = run_script(summary_step(job_id))
    assert script is not None, f"{job_id}: summary step has no run:"
    argv = words(script)
    assert argv[:2] == ["python", "scripts/ci_retry_report.py"], argv
    options: dict[str, str] = {}
    rest, index = argv[2:], 0
    while index < len(rest):
        token = rest[index]
        assert token.startswith("--"), argv
        if "=" in token:
            key, value = token.split("=", 1)
            index += 1
        else:
            assert index + 1 < len(rest), argv
            key, value = token, rest[index + 1]
            index += 2
        assert key not in options, f"{key} given twice"
        options[key] = value
    return script, options


def test_the_six_playwright_jobs_keep_their_names():
    assert {job_id: job_name(ci_block(job_id)) for job_id in PLAYWRIGHT_JOBS} == PLAYWRIGHT_JOBS
    assert LINE_REPORTER_JOBS | CONFIG_REPORTER_JOBS == set(PLAYWRIGHT_JOBS)
    assert not LINE_REPORTER_JOBS & CONFIG_REPORTER_JOBS


@pytest.mark.parametrize("job_id", PLAYWRIGHT_JOBS)
def test_the_playwright_step_is_identified_and_never_softened(job_id):
    block = ci_block(job_id)
    name, raw = playwright_step(job_id)
    assert [step for step, text in steps(block) if step_values(text, "id") == ["playwright"]] == [name]
    assert step_values(raw, "continue-on-error") == []
    assert not re.search(r"^    continue-on-error:", block, re.MULTILINE), job_id


@pytest.mark.parametrize("job_id", PLAYWRIGHT_JOBS)
def test_the_playwright_step_writes_the_json_report(job_id):
    _, raw = playwright_step(job_id)
    script = run_script(raw)
    assert script is not None
    flags = [word for word in shlex.split(script.replace("\\\n", " ")) if word.startswith("--reporter")]
    if job_id in LINE_REPORTER_JOBS:
        assert flags == ["--reporter=line,json"]
        assert unquote(step_env(raw).get("PLAYWRIGHT_JSON_OUTPUT_FILE", "")) == REPORT_PATH
    else:
        assert flags == [], job_id


@pytest.mark.parametrize("job_id", PLAYWRIGHT_JOBS)
def test_the_summary_runs_after_success_or_failure_and_cannot_fail_the_job(job_id):
    step = summary_step(job_id)
    assert step_condition(step) == "always()"
    assert step_values(step, "continue-on-error") == ["true"]
    if job_id in PWSH_JOBS:
        assert step_values(step, "shell") == ["pwsh"]


@pytest.mark.parametrize("job_id", PLAYWRIGHT_JOBS)
def test_the_summary_reports_the_original_outcome_and_run_attempt(job_id):
    required = {"STEP_OUTCOME": "${{ steps.playwright.outcome }}", "RUN_ATTEMPT": "${{ github.run_attempt }}"}
    if job_id in SHARDED_JOBS:
        required["SHARD"] = "${{ matrix.shard }}/4"
    env = {key: unquote(value) for key, value in step_env(summary_step(job_id)).items()}
    assert {key: env.get(key) for key in required} == required

    script, options = report_options(job_id)
    variable = (lambda name: f"$env:{name}") if job_id in PWSH_JOBS else (lambda name: f"${name}")
    expected = {
        "--report": REPORT_PATH,
        "--label": LABELS[job_id],
        "--step-outcome": variable("STEP_OUTCOME"),
        "--run-attempt": variable("RUN_ATTEMPT"),
        "--summary-file": variable("GITHUB_STEP_SUMMARY"),
    }
    if job_id in SHARDED_JOBS:
        expected["--expect-shard"] = variable("SHARD")
    assert options == expected
    # Quoted, so an empty or spaced value still reaches the script as one argument.
    for value in (LABELS[job_id], *(value for value in expected.values() if value.startswith("$"))):
        assert f'"{value}"' in script, value


@pytest.mark.parametrize("job_id", PLAYWRIGHT_JOBS)
def test_the_summary_keeps_expressions_out_of_its_shell(job_id):
    script = run_script(summary_step(job_id, comments=True))
    assert script is not None and "scripts/ci_retry_report.py" in script
    assert "${{" not in script


@pytest.mark.parametrize("job_id", PLAYWRIGHT_JOBS)
def test_one_summary_follows_the_pinned_playwright_step(job_id):
    names = [name for name, _ in steps(ci_block(job_id))]
    playwright = playwright_step(job_id)[0]
    assert playwright == PLAYWRIGHT_STEPS[job_id]
    assert names.count(SUMMARY_STEP) == 1
    assert names.index(playwright) < names.index(SUMMARY_STEP)


def test_no_playwright_command_overrides_the_retry_policy():
    scripts = [
        script
        for block in jobs(CI).values()
        for _, raw in steps(strip_comments(block))
        if (script := run_script(raw)) and "playwright test" in script
    ]
    assert len(scripts) >= len(PLAYWRIGHT_JOBS)
    assert [script for script in scripts if "--retries" in script] == []
