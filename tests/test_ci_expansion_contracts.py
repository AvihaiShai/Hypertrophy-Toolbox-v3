"""CI/CD expansion packet A1: the guard-test split may not weaken `Run Tests`.

`Run Tests` used to be one job running all of pytest. A1 runs the guard-hook file
in its own job(s) and makes `Run Tests` a fan-in over them. Two decisions carry
the whole guarantee, and both are exercised here as behaviour rather than read
back as constants:

* ``scripts/ci_fan_in.py`` -- the fan-in is green only when EVERY expected
  dependency reports ``success``; failure, cancellation, skip, an absent or extra
  dependency and unreadable input all fail it.
* ``scripts/ci_executed_report.py`` -- a guard run counts only when its JUnit
  report executed exactly the collected identities, once each, all passed.

The wiring tests then pin that ``ci.yml`` actually routes through both, so
neither can be bypassed by editing the workflow alone.

The D3 section at the end drives ``scripts/deep_gate_watch.py`` against a fake
GitHub REST server: clock, freshness, recovery, pagination and unavailable API.
"""
from __future__ import annotations

import copy
import hashlib
import importlib
import json
import os
import re
import shlex
import subprocess
import sys
import threading
import time
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, cast
from urllib.parse import parse_qsl, urlencode, urlsplit

import pytest

from scripts.ci_executed_report import (
    junit_identity,
    read_collection,
    select_shard,
    verify,
    verify_union,
)
from scripts.ci_fan_in import problems
from scripts.release_gate import EXPECTED_CONTEXTS, REQUIRED_CONTEXTS
from tests.test_release_workflow_contracts import (
    ALL_WORKFLOWS,
    CI,
    RELEASE,
    executable,
    jobs,
    job_name,
    permissions,
    steps,
    strip_comments,
)
from tests.test_release_workflow_contracts import text as workflow_text
from tests.worktree_cleanup.support import ROOT

GUARD_FILE = "tests/test_guard_destructive_command.py"
FAN_IN_DEPENDENCIES = ("pytest-core", "guard-hook-shard", "guard-hook-tests")
GUARD_SHARDS = 4
NODE_IDS = [
    "tests/test_a.py::test_plain",
    "tests/test_a.py::test_param[main:[Environment]::Set('X','1')-pwsh]",
    "tests/test_a.py::TestGroup::test_method[rm -rf tmp-pwsh]",
    "tests/sub/test_b.py::test_other[a|b --c]",
]


# ------------------------------------------------------------------ fan-in decision


def needs(**results):
    return json.dumps({job: {"result": result, "outputs": {}} for job, result in results.items()})


def test_fan_in_passes_only_when_every_dependency_succeeded():
    assert problems(needs(**{job: "success" for job in FAN_IN_DEPENDENCIES}), list(FAN_IN_DEPENDENCIES)) == []


@pytest.mark.parametrize("dependency", FAN_IN_DEPENDENCIES)
@pytest.mark.parametrize("result", ("failure", "cancelled", "skipped", "", None, "SUCCESS"))
def test_fan_in_rejects_any_non_success_dependency(dependency, result):
    results = {job: "success" for job in FAN_IN_DEPENDENCIES}
    results[dependency] = result
    found = problems(needs(**results), list(FAN_IN_DEPENDENCIES))
    assert found and all(dependency in problem for problem in found)


@pytest.mark.parametrize("dependency", FAN_IN_DEPENDENCIES)
def test_fan_in_rejects_a_missing_dependency(dependency):
    results = {job: "success" for job in FAN_IN_DEPENDENCIES if job != dependency}
    assert problems(needs(**results), list(FAN_IN_DEPENDENCIES)) == [f"{dependency}: result=missing"]


@pytest.mark.parametrize(
    "raw",
    ("", "not json", "[]", "null", json.dumps({"pytest-core": "success", "guard-hook-tests": "success"})),
    ids=("empty", "malformed", "list", "null", "flat-strings"),
)
def test_fan_in_rejects_unreadable_needs(raw):
    assert problems(raw, list(FAN_IN_DEPENDENCIES))


def test_fan_in_rejects_a_dependency_it_was_not_told_to_expect():
    results = {job: "success" for job in (*FAN_IN_DEPENDENCIES, "extra-leg")}
    assert problems(needs(**results), list(FAN_IN_DEPENDENCIES)) == ["unexpected dependency extra-leg"]


@pytest.mark.parametrize("expected", ([], ["pytest-core", "pytest-core"]))
def test_fan_in_rejects_an_empty_or_repeated_expectation(expected):
    assert problems(needs(**{"pytest-core": "success"}), expected)


@pytest.mark.parametrize("result,code", (("success", 0), ("failure", 1)))
def test_fan_in_exit_status_is_the_decision(result, code):
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/ci_fan_in.py"), *FAN_IN_DEPENDENCIES],
        env={**os.environ, "NEEDS": needs(**{job: "success" for job in FAN_IN_DEPENDENCIES[:-1]}, **{FAN_IN_DEPENDENCIES[-1]: result})},
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == code, proc.stdout + proc.stderr
    assert ("::error" in proc.stdout) == bool(code)


# ------------------------------------------------------- executed-identity decision


def collection(node_ids, reported=None):
    count = len(node_ids) if reported is None else reported
    return "\n".join(node_ids) + f"\n\n{count} tests collected in 0.01s\n"


def junit(tmp_path, cases, name="report.xml"):
    """cases: iterable of (node_id, outcome) where outcome None means passed."""
    root = ET.Element("testsuites")
    suite = ET.SubElement(root, "testsuite")
    for node_id, outcome in cases:
        classname, test = junit_identity(node_id).rsplit("::", 1)
        case = ET.SubElement(suite, "testcase", classname=classname, name=test)
        if outcome:
            ET.SubElement(case, outcome)
    path = tmp_path / name
    ET.ElementTree(root).write(path, encoding="utf-8")
    return path


def test_identity_mapping_splits_only_outside_parameter_ids():
    assert [junit_identity(node_id) for node_id in NODE_IDS] == [
        "tests.test_a::test_plain",
        "tests.test_a::test_param[main:[Environment]::Set('X','1')-pwsh]",
        "tests.test_a.TestGroup::test_method[rm -rf tmp-pwsh]",
        "tests.sub.test_b::test_other[a|b --c]",
    ]


@pytest.mark.parametrize("bad", ("tests/test_a.py", "test_a::test_x", "tests/test_a.py::", "::test_x"))
def test_identity_mapping_rejects_non_node_ids(bad):
    with pytest.raises(ValueError):
        junit_identity(bad)


def test_collection_reads_node_ids_and_their_own_count():
    assert read_collection(collection(NODE_IDS)) == NODE_IDS


@pytest.mark.parametrize(
    "text",
    (
        collection(NODE_IDS, reported=len(NODE_IDS) + 1),
        "\n".join(NODE_IDS) + "\n\n",
        "\n".join(NODE_IDS),
        collection([]),
        collection(["not a node id"], reported=1),
    ),
    ids=("count-mismatch", "no-summary", "no-terminator", "empty", "garbage"),
)
def test_collection_rejects_unverifiable_output(text):
    with pytest.raises(ValueError):
        read_collection(text)


@pytest.mark.parametrize("total", range(1, 6))
def test_shards_partition_the_collection_exactly(total):
    node_ids = [f"tests/test_x.py::test_{n}" for n in range(23)]
    shards = [select_shard(node_ids, index, total) for index in range(1, total + 1)]
    flat = [node_id for shard in shards for node_id in shard]
    assert sorted(flat) == sorted(node_ids) and len(flat) == len(node_ids)
    assert max(map(len, shards)) - min(map(len, shards)) <= 1


@pytest.mark.parametrize("index,total", ((0, 2), (3, 2), (1, 0)))
def test_shard_out_of_range_is_refused(index, total):
    with pytest.raises(ValueError):
        select_shard(NODE_IDS, index, total)


def test_an_empty_shard_is_refused_before_pytest_could_run_everything():
    with pytest.raises(ValueError, match="selected no identities"):
        select_shard(NODE_IDS[:2], 3, 3)


def test_the_real_guard_collection_parses_and_maps_to_distinct_identities():
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", GUARD_FILE],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    node_ids = read_collection(proc.stdout)
    assert len({junit_identity(n) for n in node_ids}) == len(node_ids) > 0


def test_verify_accepts_exactly_the_collected_identities(tmp_path):
    assert verify(NODE_IDS, [junit(tmp_path, [(n, None) for n in NODE_IDS])]) == len(NODE_IDS)


def test_verify_accepts_shard_reports_that_together_cover_the_collection(tmp_path):
    reports = [
        junit(tmp_path, [(n, None) for n in select_shard(NODE_IDS, index, 2)], f"s{index}.xml")
        for index in (1, 2)
    ]
    assert verify(NODE_IDS, reports) == len(NODE_IDS)


@pytest.mark.parametrize("outcome", ("skipped", "failure", "error"))
def test_verify_rejects_a_case_that_did_not_pass(tmp_path, outcome):
    cases = [(n, None) for n in NODE_IDS]
    cases[1] = (NODE_IDS[1], outcome)
    with pytest.raises(ValueError, match="not passed"):
        verify(NODE_IDS, [junit(tmp_path, cases)])


def test_verify_rejects_a_missing_identity(tmp_path):
    with pytest.raises(ValueError, match="missing"):
        verify(NODE_IDS, [junit(tmp_path, [(n, None) for n in NODE_IDS[:-1]])])


def test_verify_rejects_an_unexpected_identity(tmp_path):
    cases = [(n, None) for n in (*NODE_IDS, "tests/test_a.py::test_extra")]
    with pytest.raises(ValueError, match="unexpected"):
        verify(NODE_IDS, [junit(tmp_path, cases)])


def test_verify_rejects_duplicate_execution_within_one_report(tmp_path):
    cases = [(n, None) for n in (*NODE_IDS, NODE_IDS[0])]
    with pytest.raises(ValueError, match="more than once"):
        verify(NODE_IDS, [junit(tmp_path, cases)])


def test_verify_rejects_duplicate_execution_across_shard_reports(tmp_path):
    whole = [(n, None) for n in NODE_IDS]
    with pytest.raises(ValueError, match="more than once"):
        verify(NODE_IDS, [junit(tmp_path, whole, "a.xml"), junit(tmp_path, whole[:1], "b.xml")])


def test_verify_rejects_a_duplicated_expectation(tmp_path):
    with pytest.raises(ValueError, match="duplicated expected"):
        verify([*NODE_IDS, NODE_IDS[0]], [junit(tmp_path, [(n, None) for n in NODE_IDS])])


@pytest.mark.parametrize("damage", ("absent", "malformed", "empty", "nameless"))
def test_verify_rejects_an_absent_or_malformed_report(tmp_path, damage):
    path = tmp_path / "report.xml"
    if damage == "malformed":
        path.write_text("<testsuites><testsuite>", encoding="utf-8")
    elif damage == "empty":
        path.write_text("<testsuites><testsuite/></testsuites>", encoding="utf-8")
    elif damage == "nameless":
        path.write_text('<testsuites><testsuite><testcase name="x"/></testsuite></testsuites>', encoding="utf-8")
    with pytest.raises(ValueError):
        verify(NODE_IDS, [path])


def shard_reports(tmp_path, total, node_ids=NODE_IDS):
    return [
        junit(tmp_path, [(n, None) for n in select_shard(node_ids, index, total)], f"shard{index}.xml")
        for index in range(1, total + 1)
    ]


def test_union_accepts_identical_collections_whose_shards_cover_everything(tmp_path):
    assert verify_union([collection(NODE_IDS)] * 2, shard_reports(tmp_path, 2), shards=2) == len(NODE_IDS)


def test_union_rejects_shards_that_collected_different_identities(tmp_path):
    drifted = collection([*NODE_IDS[:-1], "tests/test_a.py::test_new"])
    with pytest.raises(ValueError, match="different identities"):
        verify_union([collection(NODE_IDS), drifted], shard_reports(tmp_path, 2), shards=2)


def test_union_rejects_a_lost_shard(tmp_path):
    with pytest.raises(ValueError, match="expected 2"):
        verify_union([collection(NODE_IDS)], shard_reports(tmp_path, 2)[:1], shards=2)


def test_union_rejects_shards_that_together_miss_an_identity(tmp_path):
    reports = shard_reports(tmp_path, 2)
    reports[1] = junit(tmp_path, [(n, None) for n in select_shard(NODE_IDS, 2, 2)[:-1]], "short.xml")
    with pytest.raises(ValueError, match="missing"):
        verify_union([collection(NODE_IDS)] * 2, reports, shards=2)


def cli(*args):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts/ci_executed_report.py"), *map(str, args)],
        capture_output=True, text=True, check=False,
    )


def test_shard_cli_writes_exactly_its_selection(tmp_path):
    collected = tmp_path / "collected.txt"
    collected.write_text(collection(NODE_IDS), encoding="utf-8")
    proc = cli("shard", collected, "--index", 2, "--total", 2)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.splitlines() == select_shard(NODE_IDS, 2, 2)
    assert cli("shard", collected, "--index", 3, "--total", 2).returncode == 1


def test_verify_cli_checks_only_its_own_shard(tmp_path):
    collected = tmp_path / "collected.txt"
    collected.write_text(collection(NODE_IDS), encoding="utf-8")
    report = junit(tmp_path, [(n, None) for n in select_shard(NODE_IDS, 1, 2)])
    assert cli("verify", collected, report, "--index", 1, "--total", 2).returncode == 0
    assert cli("verify", collected, report, "--index", 2, "--total", 2).returncode == 1
    assert cli("verify", collected, report).returncode == 1


def test_union_cli_requires_every_shard(tmp_path):
    collected = tmp_path / "collected.txt"
    collected.write_text(collection(NODE_IDS), encoding="utf-8")
    reports = shard_reports(tmp_path, 2)
    ok = cli("union", "--shards", 2, "--collected", collected, collected, "--reports", *reports)
    assert ok.returncode == 0, ok.stderr
    lost = cli("union", "--shards", 2, "--collected", collected, "--reports", reports[0])
    assert lost.returncode == 1 and "::error" in lost.stderr


@pytest.mark.parametrize("passing,code", ((True, 0), (False, 1)))
def test_verify_cli_exit_status_is_the_decision(tmp_path, passing, code):
    collected = tmp_path / "collected.txt"
    collected.write_text(collection(NODE_IDS), encoding="utf-8")
    cases = [(n, None if passing else "failure") for n in NODE_IDS]
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/ci_executed_report.py"), "verify", str(collected), str(junit(tmp_path, cases))],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == code, proc.stdout + proc.stderr


# ------------------------------------------------------------------- ci.yml wiring


def ci_job(job_id):
    block = jobs(CI).get(job_id)
    assert block is not None, f"ci.yml has no {job_id} job"
    return block


def needs_of(block):
    match = re.search(r"^    needs: \[([^\]]*)\]$", block, re.MULTILINE)
    assert match, "fan-in must declare its needs as one flow list"
    return [item.strip() for item in match.group(1).split(",")]


def test_run_tests_is_exactly_one_always_running_fan_in():
    named = [job_id for job_id, block in jobs(CI).items() if job_name(block) == "Run Tests"]
    assert named == ["run-tests"]
    assert "Run Tests" in REQUIRED_CONTEXTS
    assert needs_of(strip_comments(ci_job("run-tests"))) == list(FAN_IN_DEPENDENCIES)


def needs_list(block):
    """`needs:` as a flow list or a single bare job id."""
    match = re.search(r"^    needs: (.+)$", block, re.MULTILINE)
    assert match, "job declares no needs"
    return [item.strip() for item in match.group(1).strip("[]").split(",")]


def fan_in_gate(job_id):
    """The single unconditional step that decides through scripts/ci_fan_in.py."""
    block = strip_comments(ci_job(job_id))
    gates = [raw for _, raw in steps(block) if "scripts/ci_fan_in.py" in raw]
    assert len(gates) == 1, job_id
    gate = gates[0]
    assert "NEEDS: ${{ toJSON(needs) }}" in gate
    assert not re.search(r"^      (if|continue-on-error):", gate, re.MULTILINE)
    command = next(line.strip() for line in gate.splitlines() if "scripts/ci_fan_in.py" in line)
    return command.split("scripts/ci_fan_in.py", 1)[1].split()


@pytest.mark.parametrize("job_id", ("run-tests", "guard-hook-tests"))
def test_each_aggregate_decides_through_the_tested_fan_in_with_its_own_needs(job_id):
    block = strip_comments(ci_job(job_id))
    assert re.search(r"^    if: always\(\)$", block, re.MULTILINE), job_id
    assert not re.search(r"^    continue-on-error:", block, re.MULTILINE), job_id
    assert fan_in_gate(job_id) == needs_list(block)


def test_the_guard_aggregate_waits_for_every_shard():
    assert needs_list(strip_comments(ci_job("guard-hook-tests"))) == ["guard-hook-shard"]


@pytest.mark.parametrize("job_id", ("pytest-core", "guard-hook-shard"))
def test_test_running_jobs_cannot_skip_or_soften_themselves(job_id):
    block = strip_comments(ci_job(job_id))
    assert not re.search(r"^    (if|continue-on-error|needs):", block, re.MULTILINE), job_id
    for name, raw in steps(block):
        # Only the measure-only coverage summary (decision D1) may never fail.
        if name != "Summarize coverage (measure-only)":
            assert "continue-on-error" not in raw, f"{job_id} / {name}"


def shard_steps():
    return dict(steps(strip_comments(ci_job("guard-hook-shard"))))


def test_guard_shards_partition_one_collection_of_only_the_guard_file():
    block = strip_comments(ci_job("guard-hook-shard"))
    matrix = re.search(r"^        shard: \[([^\]]*)\]$", block, re.MULTILINE)
    assert matrix and [int(n) for n in matrix.group(1).split(",")] == list(range(1, GUARD_SHARDS + 1))
    assert job_name(block) == f"Guard Hook Tests (Linux pwsh) shard ${{{{ matrix.shard }}}}/{GUARD_SHARDS}"
    assert "fail-fast: false" in block
    # A measured 12.5-minute straggler (PLANNING.md §14) is why this is not 15.
    assert re.search(r"^    timeout-minutes: 20$", block, re.MULTILINE)
    select = shard_steps()["Collect and select this shard"]
    assert f"pytest --collect-only -q {GUARD_FILE} > artifacts/guard/collected.txt" in select
    selection = f"--index ${{{{ matrix.shard }}}} --total {GUARD_SHARDS}"
    assert f"shard artifacts/guard/collected.txt {selection} > artifacts/guard/shard.txt" in select
    verify_step = shard_steps()["Require executed shard identities without skips"]
    assert re.search(r"^      if: always\(\)$", verify_step, re.MULTILINE)
    assert f"verify artifacts/guard/collected.txt artifacts/guard/junit.xml {selection}" in verify_step


def test_guard_shards_run_exactly_their_selection_and_require_pwsh():
    run = shard_steps()["Run guard-hook tests"]
    command = run.split("run: ", 1)[1].strip()
    # Serial on purpose: concurrent pwsh processes on one runner crashed (PLANNING.md §14).
    assert command == "python -m pytest @artifacts/guard/shard.txt -v --tb=short --junitxml=artifacts/guard/junit.xml"
    assert "pwsh -NoProfile" in shard_steps()["Require PowerShell 7"]
    upload = shard_steps()["Upload guard-hook shard report"]
    assert "name: guard-hook-junit-${{ matrix.shard }}" in upload
    assert "if-no-files-found: error" in upload and re.search(r"^      if: always\(\)$", upload, re.MULTILINE)


def test_guard_aggregate_proves_the_union_of_every_shard():
    aggregate = dict(steps(strip_comments(ci_job("guard-hook-tests"))))
    download = aggregate["Download guard-hook shard reports"]
    assert "pattern: guard-hook-junit-*" in download and "merge-multiple" not in download
    union = " ".join(aggregate["Require the shards to have executed every collected identity once"].replace("\\\n", " ").split())
    assert f"union --shards {GUARD_SHARDS} " in union
    assert "--collected artifacts/guard/guard-hook-junit-*/collected.txt" in union
    assert "--reports artifacts/guard/guard-hook-junit-*/junit.xml" in union
    names = list(aggregate)
    assert names.index("Require every guard-hook shard to pass") < names.index("Download guard-hook shard reports")
    for name, raw in aggregate.items():
        assert not re.search(r"^      (if|continue-on-error):", raw, re.MULTILINE), name


def test_together_the_two_test_jobs_cover_every_test_file():
    """pytest-core ignores exactly the guard file; the guard legs collect exactly it."""
    core = strip_comments(ci_job("pytest-core"))
    assert re.findall(r"--ignore=(\S+)", core) == [GUARD_FILE]
    assert (ROOT / GUARD_FILE).is_file()
    collects = re.findall(r"pytest --collect-only -q (\S+)", strip_comments(ci_job("guard-hook-shard")))
    assert collects == [GUARD_FILE]


def test_pytest_core_runs_the_whole_suite_except_the_guard_file():
    block = strip_comments(ci_job("pytest-core"))
    assert job_name(block) == "Python Tests (core)"
    assert re.search(r"^    timeout-minutes: 20$", block, re.MULTILINE)
    script = dict(steps(block))["Run pytest with coverage"].split("run: |", 1)[1].split("\n      env:", 1)[0]
    command = " ".join(script.replace("\\\n", " ").split())
    assert command.startswith("pytest tests/ -v --tb=short ")
    assert re.findall(r"--ignore=(\S+)", command) == [GUARD_FILE]
    assert not re.search(r"(?:^| )(-k|-m|--deselect|-x|--lf)(?:[ =]|$)", command)
    for flag in ("--cov=utils", "--cov=routes", "--junitxml=artifacts/pytest/junit.xml"):
        assert flag in command


# =================================================== B2: workflow lint (actionlint + zizmor)
#
# The always-on lint job, its pinned tools, and the findings it keeps fixed repo-wide.

LINT_JOB_ID = "workflow-lint"
LINT_JOB_NAME = "Workflow Lint (actionlint + zizmor)"
LINT_BIN = "$RUNNER_TEMP/workflow-lint-bin"
INSTALL_STEP = "Install pinned workflow linters"
ACTIONLINT_STEP = "actionlint"
ZIZMOR_STEP = "zizmor (min severity medium)"
LINT_STEP_NAMES = ("Checkout code", INSTALL_STEP, ACTIONLINT_STEP, ZIZMOR_STEP)

LINT_PINS = {
    "ACTIONLINT_VERSION": "1.7.12",
    "ACTIONLINT_SHA256": "8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8",
    "ZIZMOR_VERSION": "1.30.1",
    "ZIZMOR_SHA256": "e65324f4430c2717591937edcec90ccbefaf14c174f8ec9415e03ca875b46e1a",
    "SHELLCHECK_VERSION": "v0.11.0",
    "SHELLCHECK_SHA256": "b7af85e41cc99489dcc21d66c6d5f3685138f06d34651e6d34b42ec6d54fe6f6",
}
LINT_DIGEST_KEYS = tuple(key for key in LINT_PINS if key.endswith("_SHA256"))
LINT_TOOL_REPOS = {"rhysd/actionlint", "zizmorcore/zizmor", "koalaman/shellcheck"}

# Exact argv: any extra token (`|| true`, `--no-exit-codes`, `--offline`, a narrower
# target, a second severity flag) is a softening and must red.
LINTER_ARGV = {
    ACTIONLINT_STEP: [f"{LINT_BIN}/actionlint", "-color", f"-shellcheck={LINT_BIN}/shellcheck", "-pyflakes="],
    ZIZMOR_STEP: [f"{LINT_BIN}/zizmor", "--min-severity", "medium", "--format", "plain", ".github/workflows"],
}
ZIZMOR_CONDITIONS = {"${{ !cancelled() }}", "!cancelled()", "${{ always() }}", "always()"}

# (workflow file, rule) -> (exact occurrences, reason). One inline directive per SC2016
# finding at f3adacf1; B2 adds no zizmor entry, and any later one is a deliberate edit here.
LINT_SUPPRESSIONS = {
    ("ci.yml", "SC2016"): (4, "single-quoted `$`/backtick text is printed literally on purpose"),
}
SUPPRESSION = re.compile(r"zizmor:\s*ignore\[([^\]]*)\]|shellcheck\s+disable=([\w,-]+)")
# Each of these would suppress findings repository-wide without a comment at the site.
LINT_CONFIG_FILES = (
    "zizmor.yml",
    "zizmor.yaml",
    ".zizmor.yml",
    ".zizmor.yaml",
    ".github/zizmor.yml",
    ".github/zizmor.yaml",
    ".github/actionlint.yml",
    ".github/actionlint.yaml",
    ".shellcheckrc",
)

RUN_KEY = re.compile(r"^( *)(?:- )?run:[ \t]*(.*)$")
BLOCK_SCALAR = re.compile(r"^[|>][-+0-9]*$")
EXPRESSION = re.compile(r"\$\{\{(.*?)\}\}", re.DOTALL)
# Event payloads and every branch/tag name (chosen by whoever pushes) never reach a shell
# through `${{ }}`; scripts read the runner's own env vars ($GITHUB_REF) instead.
UNTRUSTED = re.compile(r"\bgithub\.(?:event[.\[]|head_ref\b|base_ref\b|ref_name\b|ref\b)")


def lint_job():
    return strip_comments(ci_job(LINT_JOB_ID))


def lint_steps():
    return dict(steps(lint_job()))


def run_script(step):
    """A step's `run:` shell text, unwrapped from YAML quoting."""
    match = re.search(r"^      run:[ \t]*(.*)$", step, re.MULTILINE)
    assert match, "step has no run:"
    value = match.group(1).strip()
    if not BLOCK_SCALAR.match(value):
        if len(value) > 1 and value[0] == value[-1] == "'":
            return value[1:-1].replace("''", "'")
        return value
    body = []
    for line in step[match.end() :].split("\n")[1:]:
        if line.strip() and not line.startswith(" " * 8):
            break
        body.append(line[8:])
    return "\n".join(body)


def single_command(step):
    script = run_script(step).replace("\\\n", " ").replace("${RUNNER_TEMP}", "$RUNNER_TEMP")
    commands = [line for line in script.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    assert len(commands) == 1, commands
    return shlex.split(commands[0])


def run_blocks(path):
    """Every `run:` value in a workflow, at any indent, comments inside it included.

    Raw text on purpose: Actions expands `${{ }}` inside a shell comment too.
    """
    lines = workflow_text(path).splitlines()
    found = []
    for index, line in enumerate(lines):
        key = RUN_KEY.match(line)
        if key is None:
            continue
        indent, value = len(key.group(1)), key.group(2).strip()
        if not BLOCK_SCALAR.match(value):
            found.append(value)
            continue
        body = []
        for following in lines[index + 1 :]:
            if following.strip() and len(following) - len(following.lstrip()) <= indent:
                break
            body.append(following)
        found.append("\n".join(body))
    return found


def run_expressions(path):
    return [expr.strip() for script in run_blocks(path) for expr in EXPRESSION.findall(script)]


def key_body(block, key, indent):
    """The lines under a block-style `key:` at `indent`, blank lines included.

    Blank-line tolerant on purpose: YAML lets a blank line sit inside a mapping, and a
    key hidden after one must still be seen. A flow-style `key: {...}` returns "".
    """
    match = re.search(rf"^{' ' * indent}{key}:[ \t]*\n", block, re.MULTILINE)
    if match is None:
        return ""
    body = []
    for line in block[match.end() :].split("\n"):
        if line.strip() and len(line) - len(line.lstrip()) <= indent:
            break
        body.append(line)
    return "\n".join(body)


def mapping_keys(body, indent):
    return set(re.findall(rf"^{' ' * indent}([A-Za-z0-9_-]+):", body, re.MULTILINE))


def steps_using(path, action):
    return [
        (f"{job_id} / {name}", strip_comments(raw))
        for job_id, block in jobs(path).items()
        for name, raw in steps(block)
        if re.search(rf"^      uses: {action}@", strip_comments(raw), re.MULTILINE)
    ]


def test_exactly_one_ci_job_reports_the_workflow_lint_name():
    named = [job_id for job_id, block in jobs(CI).items() if job_name(block) == LINT_JOB_NAME]
    assert named == [LINT_JOB_ID]


@pytest.mark.parametrize("event", ("push", "pull_request"))
def test_ci_triggers_reach_main_with_no_path_or_branch_exclusion(event):
    on = re.search(r"^on:[ \t]*\n(.*?)(?=^\S)", strip_comments(workflow_text(CI)), re.MULTILINE | re.DOTALL)
    assert on, "ci.yml has no on: block"
    trigger = re.search(rf"^  {event}:[ \t]*\n((?:    .*\n)*)", on.group(1), re.MULTILINE)
    assert trigger, f"ci.yml does not trigger on {event}"
    body = trigger.group(1)
    assert not re.search(r"^    (paths|paths-ignore|branches-ignore):", body, re.MULTILINE), body
    flow = re.search(r"^    branches:[ \t]*\[([^\]]*)\]", body, re.MULTILINE)
    listed = (
        [b.strip().strip("'\"") for b in flow.group(1).split(",")]
        if flow
        else re.findall(r"^      - ['\"]?([^'\"\s]+)", body, re.MULTILINE)
    )
    assert "main" in listed, listed


def test_the_lint_job_cannot_skip_wait_soften_or_rename_itself():
    block = lint_job()
    # `strategy:` mints a `(matrix value)` suffix, renaming the check C4 will require.
    for key in ("if", "needs", "continue-on-error", "strategy"):
        assert not re.search(rf"^    {key}:", block, re.MULTILINE), key
    timeout = re.search(r"^    timeout-minutes: (\d+)[ \t]*$", block, re.MULTILINE)
    assert timeout and int(timeout.group(1)) <= 15


def test_the_lint_job_token_is_read_only():
    assert permissions(lint_job()) == {"contents": "read"}


def test_the_lint_job_runs_exactly_its_four_steps_in_order():
    assert tuple(lint_steps()) == LINT_STEP_NAMES


def test_the_tool_versions_and_digests_are_pinned_exactly():
    assert all(re.fullmatch(r"[0-9a-f]{64}", LINT_PINS[key]) for key in LINT_DIGEST_KEYS)
    env = key_body(lint_job(), "env", 4)
    declared = dict(re.findall(r"^      ([A-Za-z0-9_-]+):[ \t]*'?([^'\n]*?)'?[ \t]*$", env, re.MULTILINE))
    # Exact keys: a job-level SHELLCHECK_OPTS or ZIZMOR_* would reconfigure every step.
    assert declared == LINT_PINS


def test_every_download_is_a_release_asset_verified_before_unpacking():
    script = run_script(lint_steps()[INSTALL_STEP])
    commands = [
        line.strip()
        for line in script.replace("\\\n", " ").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    downloads = [shlex.split(command) for command in commands if "://" in command]
    repos = set()
    for argv in downloads:
        assert argv[0] == "curl" and "--fail" in argv, argv
        assert any(argv[i : i + 2] == ["--proto", "=https"] for i in range(len(argv))), argv
        for url in (token for token in argv if "://" in token):
            asset = re.fullmatch(r"https://github\.com/([\w.-]+/[\w.-]+)/releases/download/\S+", url)
            assert asset, url
            repos.add(asset.group(1))
    assert repos == LINT_TOOL_REPOS

    joined = "\n".join(commands)
    # One verify, no extra flags: `--ignore-missing` passes a checksum list that names no
    # downloaded file, and `--quiet` is the first step toward ignoring its output.
    assert [flags.split() for flags in re.findall(r"\bsha256sum\b([^|;&\n]*)", joined)] == [["--check", "--strict"]]
    unpack = re.search(r"(?:^|[;&|])[ \t]*tar\s", joined, re.MULTILINE)
    assert unpack, "the install step never unpacks anything"
    before = joined[: unpack.start()]
    assert re.search(r"\bsha256sum\b", before)
    for key in LINT_DIGEST_KEYS:
        assert re.search(rf"\$\{{?{key}\b", before), f"{key} is not checked before the first tar"
    # Under the runner's default `bash -e`, any `||` or `set +e` can swallow a failed check.
    assert "||" not in script and "set +e" not in script


def test_the_job_installs_nothing_but_the_verified_binaries():
    block = lint_job()
    assert "pip install" not in block and "go install" not in block
    uses = re.findall(r"^ *(?:- )?uses:[ \t]*(\S+)", block, re.MULTILINE)
    assert len(uses) == 1 and re.fullmatch(r"actions/checkout@[0-9a-f]{40}", uses[0]), uses


@pytest.mark.parametrize("step", sorted(LINTER_ARGV))
def test_each_linter_runs_exactly_its_pinned_command(step):
    assert single_command(lint_steps()[step]) == LINTER_ARGV[step]


def test_zizmor_runs_online_and_even_after_actionlint_fails():
    step = lint_steps()[ZIZMOR_STEP]
    env = key_body(step, "env", 6)
    # Exact keys: ZIZMOR_OFFLINE / ZIZMOR_CONFIG / ZIZMOR_* flags all soften the run.
    assert mapping_keys(env, 8) == {"GH_TOKEN"}
    assert re.search(r"^        GH_TOKEN: \$\{\{ github\.token \}\}[ \t]*$", env, re.MULTILINE)
    condition = re.search(r"^      if:[ \t]*(.+?)[ \t]*$", step, re.MULTILINE)
    assert condition and condition.group(1) in ZIZMOR_CONDITIONS


def test_no_other_environment_can_reconfigure_the_linters():
    for name in (INSTALL_STEP, ACTIONLINT_STEP):
        assert not re.search(r"^      env:", lint_steps()[name], re.MULTILINE), name
    # $GITHUB_ENV carries variables into every later step; a workflow-level env reaches
    # every job. Neither is used today, so neither may appear unreviewed.
    assert "GITHUB_ENV" not in lint_job()
    assert not re.search(r"^env:", strip_comments(workflow_text(CI)), re.MULTILINE)


def test_no_lint_step_is_tolerated_or_conditional():
    for name, step in lint_steps().items():
        assert not re.search(r"^      continue-on-error:", step, re.MULTILINE), name
        if name != ZIZMOR_STEP:
            assert not re.search(r"^      if:", step, re.MULTILINE), name


@pytest.mark.parametrize("path", ALL_WORKFLOWS, ids=lambda p: p.name)
def test_every_checkout_drops_its_credentials(path):
    checkouts = steps_using(path, "actions/checkout")
    # An unnamed `- uses:` step merges into its neighbour; the count makes that red.
    assert len(checkouts) == executable(path).count("actions/checkout@") > 0
    for where, step in checkouts:
        assert re.search(r"^        persist-credentials: false[ \t]*$", key_body(step, "with", 6), re.MULTILINE), where


@pytest.mark.parametrize("path", ALL_WORKFLOWS, ids=lambda p: p.name)
def test_no_run_block_interpolates_attacker_controlled_context(path):
    assert run_blocks(path)
    assert [expr for expr in run_expressions(path) if UNTRUSTED.search(expr)] == []


def test_release_runs_take_the_ref_from_the_runner_environment():
    # The `${{ github.ref }}` ban itself is UNTRUSTED, above; this pins the replacement.
    assert '--ref "$GITHUB_REF"' in run_script(dict(steps(jobs(RELEASE)["version-guard"]))["Assert the tag matches the code"])


def test_release_setup_steps_restore_no_cache():
    setups = steps_using(RELEASE, "actions/setup-python") + steps_using(RELEASE, "actions/setup-node")
    assert setups
    for where, step in setups:
        assert not re.search(r"^        cache", key_body(step, "with", 6), re.MULTILINE), where
    assert "actions/cache" not in executable(RELEASE)


def test_every_lint_suppression_is_registered():
    assert [name for name in LINT_CONFIG_FILES if (ROOT / name).exists()] == []
    found = Counter()
    for path in ALL_WORKFLOWS:
        for match in SUPPRESSION.finditer(workflow_text(path)):
            found.update((path.name, rule.strip()) for rule in (match.group(1) or match.group(2)).split(","))
    assert dict(found) == {key: count for key, (count, _) in LINT_SUPPRESSIONS.items()}


def test_workflow_lint_is_not_a_required_or_expected_context_yet():
    # Promotion is C4's deliberate change, after seeded blocking proof.
    assert LINT_JOB_NAME not in REQUIRED_CONTEXTS
    assert LINT_JOB_NAME not in EXPECTED_CONTEXTS
# =========================================================================================
# D3 — deep_gate_watch
#
# Seam (implement to this): reconcile(client, now, event=None, dry_run=False) receives a real
# GitHubClient(repo, token, api_url=..., timeout=...) that these tests point at FakeGitHub, an
# in-process server for the REST routes the brief names; the label is checked with
# GET /labels/deep-gate, and issues close by PATCH state=closed plus POST /comments. `event` is
# the parsed $GITHUB_EVENT_PATH payload, and the returned Report's `unavailable` iterates the
# watched file names whose evidence was unavailable. The CLI reads GH_TOKEN, GITHUB_API_URL and
# GITHUB_STEP_SUMMARY; `--now` is also the watchdog start time, and a workflow_run summary
# carries a line containing "latency" and the latency in whole seconds.
# =========================================================================================

SCRIPT = ROOT / "scripts" / "deep_gate_watch.py"
REPO = "octo/toolbox"
PREFIX = f"/repos/{REPO}"
TOKEN = "test-token"
LABEL = "deep-gate"
UTC = timezone.utc
SECOND, MINUTE, HOUR, DAY = (
    timedelta(seconds=1),
    timedelta(minutes=1),
    timedelta(hours=1),
    timedelta(days=1),
)

SUITE, VISUAL = "deep-gate.yml", "deep-gate-visual.yml"
NAMES = {SUITE: "Deep Gate (manual + weekly)", VISUAL: "Deep Gate Visual (Linux)"}
SUITE_JOBS = (
    "Full E2E incl. accessibility (Chromium)",
    "First install (catalog seed) smoke",
    "Empty-schema initializer smoke",
    "Old-DB migration compatibility",
    "Frozen executable (real bootloader, Windows) / Build and smoke",
    "Dependency Health Check",
)
FAILED_JOB = SUITE_JOBS[3]
FAILED_STEP = "Generate historical-schema DB, boot, assert upgrade"
VISUAL_JOB = "Visual regression (Linux baselines)"
COMPARE = "Run visual specs (compare)"
GENERATE = "Run visual specs (generate)"
NO_WRITE = "Assert compare mode wrote no baseline"
NON_SUCCESS = (
    "failure",
    "cancelled",
    "timed_out",
    "startup_failure",
    "action_required",
    "stale",
    "neutral",
    "skipped",
    None,
)

SLOT = datetime(2026, 10, 19, 3, 17, tzinfo=UTC)  # a Monday
PREV = SLOT - 7 * DAY
BEFORE = SLOT + 2 * HOUR
AFTER = SLOT + 21 * HOUR
SCHEDULE_EVENT = {"schedule": "23 * * * 1,2"}
ENDLESS_LIMIT = 500
SLOW_SECONDS = 3


# ------------------------------------------------------------------ fixture builders


def iso(moment: datetime) -> str:
    return moment.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def gh_run(
    file,
    run_id,
    created,
    *,
    event="schedule",
    conclusion="success",
    status="completed",
    attempt=1,
    branch="main",
    updated=None,
):
    return {
        "id": run_id,
        "run_attempt": attempt,
        "head_sha": hashlib.sha1(str(run_id).encode()).hexdigest(),
        "head_branch": branch,
        "event": event,
        "status": status,
        "conclusion": conclusion if status == "completed" else None,
        "created_at": iso(created),
        "updated_at": iso(updated or created + 30 * MINUTE),
        "path": f".github/workflows/{file}",
        "name": NAMES[file],
        "html_url": f"https://github.com/{REPO}/actions/runs/{run_id}",
    }


def gh_step(name, conclusion="success"):
    return {"name": name, "status": "completed", "conclusion": conclusion}


def gh_job(r, name, conclusion="success", step_list=(gh_step("Checkout code"),)):
    return {
        "id": r["id"] * 100 + len(name),
        "run_id": r["id"],
        "run_attempt": r["run_attempt"],
        "head_sha": r["head_sha"],
        "name": name,
        "status": "completed",
        "conclusion": conclusion,
        "steps": [{**s, "number": n} for n, s in enumerate(step_list, 1)],
        "html_url": f"{r['html_url']}/job/{r['id'] * 100 + len(name)}",
    }


def suite_jobs(r, failed=None, skipped=None):
    out = []
    for name in SUITE_JOBS:
        if name == failed:
            out.append(
                gh_job(
                    r,
                    name,
                    "failure",
                    (
                        gh_step("Checkout code"),
                        gh_step(FAILED_STEP, "failure"),
                        gh_step("Upload diagnostics", "failure"),
                    ),
                )
            )
        elif name == skipped:
            out.append(gh_job(r, name, "skipped", ()))
        else:
            out.append(gh_job(r, name))
    return out


def visual_job(
    r,
    *,
    compare="success",
    generate="skipped",
    no_write="success",
    conclusion="success",
    name=VISUAL_JOB,
):
    planned = (
        ("Checkout code", "success"),
        ("Resolve visual mode", "success"),
        (COMPARE, compare),
        (GENERATE, generate),
        (NO_WRITE, no_write),
    )
    return gh_job(r, name, conclusion, tuple(gh_step(n, c) for n, c in planned if c is not None))


def delivered(r):
    return {
        "action": "completed",
        "workflow_run": r,
        "workflow": {"path": r["path"], "name": r["name"]},
    }


def new_issue(number, title, body, labels):
    return {
        "number": number,
        "title": title,
        "body": body,
        "state": "open",
        "state_reason": None,
        "labels": [{"name": n if isinstance(n, str) else n["name"]} for n in labels],
        "comments": 0,
        "html_url": f"https://github.com/{REPO}/issues/{number}",
    }


# --------------------------------------------------------------------- fake GitHub


class FakeGitHub(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _Handler)
        self.runs: list[dict[str, Any]] = []
        self.jobs: dict[tuple[int, int], list[dict[str, Any]]] = {}
        self.issues: list[dict[str, Any]] = []
        self.comments: dict[int, list[str]] = {}
        self.label = True
        self.page_size = 100
        # path substring -> "502" | "403" | "malformed" | "slow" | "endless"; "kind@N" only on page N
        self.faults: dict[str, str] = {}
        self.requests: list[tuple[str, str, dict[str, str], dict[str, str]]] = []
        self.writes: list[tuple[str, str, Any]] = []

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.server_port}"

    def handle_error(self, request, client_address) -> None:
        pass  # a client that timed out hangs up mid-reply

    def add(self, r, jobs=None):
        self.runs = [x for x in self.runs if x["id"] != r["id"]] + [r]
        if jobs is not None:
            self.jobs[(r["id"], r["run_attempt"])] = jobs
        return r

    def issue(self, number):
        return next(i for i in self.issues if i["number"] == number)

    def find(self, file, kind, state="open"):
        marker = f"<!-- deep-gate-watch v1 workflow={file} kind={kind} "
        return [i for i in self.issues if i["state"] == state and marker in (i["body"] or "")]

    def only(self, file, kind):
        found = self.find(file, kind)
        assert len(found) == 1, found
        return found[0]

    def open_issues(self):
        return [i for i in self.issues if i["state"] == "open"]

    def note(self, title):
        number = max((i["number"] for i in self.issues), default=0) + 1
        self.issues.append(new_issue(number, title, "filed by hand", [LABEL]))


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        pass

    def do_GET(self) -> None:
        self._route("GET")

    def do_POST(self) -> None:
        self._route("POST")

    def do_PATCH(self) -> None:
        self._route("PATCH")

    def do_PUT(self) -> None:
        self._route("PUT")

    def do_DELETE(self) -> None:
        self._route("DELETE")

    def _route(self, method: str) -> None:
        gh = cast(FakeGitHub, self.server)
        parts = urlsplit(self.path)
        query = dict(parse_qsl(parts.query))
        length = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(length)) if length else None
        headers = {key.lower(): value for key, value in self.headers.items()}
        gh.requests.append((method, parts.path, query, headers))
        if method != "GET":
            gh.writes.append((method, parts.path.removeprefix(PREFIX), body))

        fault = next((kind for needle, kind in gh.faults.items() if needle in parts.path), "")
        kind, _, on_page = fault.partition("@")
        if kind and on_page in ("", query.get("page", "1")):
            if kind == "slow":
                time.sleep(SLOW_SECONDS)
            elif kind == "malformed":
                return self._reply(200, raw=b'{"workflow_runs": [')
            elif kind != "endless":
                return self._reply(int(kind), {"message": "injected"})
        if not parts.path.startswith(PREFIX + "/"):
            return self._reply(404, {"message": "Not Found"})
        self._serve(gh, method, parts.path.removeprefix(PREFIX), query, body, kind == "endless")

    def _serve(self, gh, method, path, query, body, endless) -> None:
        runs = re.fullmatch(r"/actions/workflows/([^/]+)/runs", path)
        jobs = re.fullmatch(r"/actions/runs/(\d+)/attempts/(\d+)/jobs", path)
        issue = re.fullmatch(r"/issues/(\d+)", path)
        comment = re.fullmatch(r"/issues/(\d+)/comments", path)
        if method == "GET" and runs:
            listed = [
                r
                for r in gh.runs
                if r["path"] == f".github/workflows/{runs[1]}"
                and query.get("branch", r["head_branch"]) == r["head_branch"]
            ]
            listed.sort(key=lambda r: (r["created_at"], r["id"]), reverse=True)
            return self._page(gh, listed, query, endless, "workflow_runs")
        if method == "GET" and jobs:
            listed = gh.jobs.get((int(jobs[1]), int(jobs[2])), [])
            return self._page(gh, listed, query, endless, "jobs")
        if method == "GET" and path == "/issues":
            wanted = query.get("labels")
            listed = [
                i
                for i in gh.issues
                if i["state"] == query.get("state", "open")
                and (wanted is None or wanted in {label["name"] for label in i["labels"]})
            ]
            listed.sort(key=lambda i: i["number"], reverse=True)
            return self._page(gh, listed, query, endless, None)
        if method == "POST" and path == "/issues":
            number = max((i["number"] for i in gh.issues), default=0) + 1
            created = new_issue(number, body["title"], body.get("body", ""), body.get("labels", []))
            gh.issues.append(created)
            return self._reply(201, created)
        if method == "PATCH" and issue:
            target = gh.issue(int(issue[1]))
            target.update({k: v for k, v in body.items() if k in ("title", "body", "state", "state_reason")})
            if "labels" in body:
                target["labels"] = new_issue(0, "", "", body["labels"])["labels"]
            return self._reply(200, target)
        if method == "POST" and comment:
            target = gh.issue(int(comment[1]))
            target["comments"] += 1
            gh.comments.setdefault(target["number"], []).append(body["body"])
            return self._reply(201, {"id": target["comments"], "body": body["body"]})
        if method == "GET" and path == f"/labels/{LABEL}":
            if gh.label:
                return self._reply(200, {"name": LABEL})
            return self._reply(404, {"message": "Not Found"})
        if method == "POST" and path == "/labels":
            gh.label = True
            return self._reply(201, {"name": body["name"]})
        self._reply(404, {"message": "Not Found"})

    def _page(self, gh, items, query, endless, envelope) -> None:
        size = max(1, min(int(query.get("per_page", 30)), gh.page_size))
        number = int(query.get("page", 1))
        if number > ENDLESS_LIMIT:
            return self._reply(500, {"message": "the fake stops serving here"})
        chunk = items[:size] if endless else items[(number - 1) * size : number * size]
        last = number + 1 if endless else max(1, -(-len(items) // size))
        base = f"{gh.url}{urlsplit(self.path).path}"

        def link(page, rel):
            return f'<{base}?{urlencode({**query, "page": page})}>; rel="{rel}"'

        # `next` is never the first relation listed, so a parser that takes the first URL skips pages.
        links = [link(1, "first"), link(number - 1, "prev")] if number > 1 else []
        if number < last:
            links += [link(last, "last"), link(number + 1, "next")]
        total = 10**6 if endless else len(items)
        payload = {"total_count": total, envelope: chunk} if envelope else chunk
        self._reply(200, payload, headers={"Link": ", ".join(links)} if links else None)

    def _reply(self, status, payload=None, raw=None, headers=None) -> None:
        data = raw if raw is not None else json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(data)


# -------------------------------------------------------------------------- fixtures


@pytest.fixture(scope="module")
def dgw():
    return importlib.import_module("scripts.deep_gate_watch")


@pytest.fixture
def gh(monkeypatch):
    monkeypatch.setenv("NO_PROXY", "*")
    server = FakeGitHub()
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield server
    server.shutdown()
    server.server_close()


def watched(dgw, file):
    return next(x for x in dgw.WATCHED if x.file == file)


def classify(dgw, file, r, jobs):
    return dgw.classify_run(watched(dgw, file), r, jobs)


def fresh(dgw, file, runs, now):
    return dgw.freshness_state(watched(dgw, file), runs, now)


def run_watch(dgw, gh, now, event=None, dry_run=False, timeout=5.0):
    client = dgw.GitHubClient(REPO, TOKEN, api_url=gh.url, timeout=timeout)
    return dgw.reconcile(client, now, event=event, dry_run=dry_run)


def seed_success(gh, file, run_id, created=SLOT + 5 * MINUTE, event="schedule"):
    r = gh_run(file, run_id, created, event=event)
    return gh.add(r, suite_jobs(r) if file == SUITE else [visual_job(r)])


def seed_failure(gh, file, run_id, created=SLOT + 5 * MINUTE, event="schedule", conclusion="failure"):
    r = gh_run(file, run_id, created, event=event, conclusion=conclusion)
    if file == SUITE:
        return gh.add(r, suite_jobs(r, failed=FAILED_JOB))
    return gh.add(r, [visual_job(r, compare="failure", conclusion="failure")])


def issue_comments(gh, issue):
    return "\n".join(gh.comments.get(issue["number"], []))


# ------------------------------------------------------------ constants and the slot


def test_constants_pin_the_slot_bounds_and_identities(dgw):
    assert dgw.DEFAULT_BRANCH == "main"
    assert (dgw.SLOT_WEEKDAY, dgw.SLOT_TIME) == (0, (3, 17))
    assert dgw.MISSING_THRESHOLD == timedelta(hours=20)
    assert dgw.FRESHNESS_DEADLINE == timedelta(hours=36)
    assert dgw.MISSING_THRESHOLD < dgw.FRESHNESS_DEADLINE
    assert [(x.file, x.name, x.kind) for x in dgw.WATCHED] == [
        (SUITE, NAMES[SUITE], "suite"),
        (VISUAL, NAMES[VISUAL], "visual"),
    ]
    assert (dgw.VISUAL_JOB_NAME, dgw.COMPARE_STEP_NAME, dgw.NO_WRITE_STEP_NAME) == (
        VISUAL_JOB,
        COMPARE,
        NO_WRITE,
    )
    assert (dgw.ISSUE_LABEL, dgw.MARKER_PREFIX) == (LABEL, "<!-- deep-gate-watch v1 ")


SLOT_CASES = {
    "at-the-slot": (SLOT, SLOT),
    "monday-0316-59": (SLOT - SECOND, PREV),
    "monday-0316": (SLOT - MINUTE, PREV),
    "sunday-before-next": (SLOT + 7 * DAY - SECOND, SLOT),
    "next-slot": (SLOT + 7 * DAY, SLOT + 7 * DAY),
    "europe-dst-ends-sunday": (datetime(2026, 10, 25, 23, 59, tzinfo=UTC), SLOT),
    "two-weeks-later": (SLOT + 14 * DAY + HOUR, SLOT + 14 * DAY),
    "plus-three-offset-before": (
        datetime(2026, 10, 19, 6, 16, 59, tzinfo=timezone(timedelta(hours=3))),
        PREV,
    ),
    "plus-one-offset-at": (datetime(2026, 10, 19, 4, 17, tzinfo=timezone(timedelta(hours=1))), SLOT),
    "year-boundary-sunday": (
        datetime(2027, 1, 3, 12, tzinfo=UTC),
        datetime(2026, 12, 28, 3, 17, tzinfo=UTC),
    ),
    "year-boundary-monday": (
        datetime(2027, 1, 4, 3, 17, tzinfo=UTC),
        datetime(2027, 1, 4, 3, 17, tzinfo=UTC),
    ),
}


@pytest.mark.parametrize("case", list(SLOT_CASES))
def test_expected_slot_is_the_latest_monday_0317_utc_at_or_before_now(dgw, case):
    now, slot = SLOT_CASES[case]
    found = dgw.expected_slot(now)
    assert found == slot
    assert found.utcoffset() == timedelta(0)


def test_evidence_key_orders_by_creation_then_id_then_attempt(dgw):
    a = gh_run(SUITE, 5, SLOT)
    b = gh_run(SUITE, 4, SLOT + SECOND)
    c = gh_run(SUITE, 6, SLOT + SECOND)
    d = {**c, "run_attempt": 2}
    assert sorted([d, c, b, a], key=dgw.evidence_key) == [a, b, c, d]
    assert dgw.evidence_key(d) != dgw.evidence_key(c)


# -------------------------------------------------------------------- classify_run


def test_runs_of_other_workflows_or_branches_are_ignored(dgw):
    foreign = {**gh_run(SUITE, 1, SLOT), "path": ".github/workflows/ci.yml", "name": "CI"}
    suite_green = gh_run(SUITE, 2, SLOT)
    branch = gh_run(SUITE, 3, SLOT, branch="feature")
    assert classify(dgw, SUITE, foreign, suite_jobs(foreign)).kind == "ignored"
    assert classify(dgw, VISUAL, suite_green, suite_jobs(suite_green)).kind == "ignored"
    assert classify(dgw, SUITE, branch, suite_jobs(branch)).kind == "ignored"
    assert classify(dgw, SUITE, {**branch, "conclusion": "failure"}, []).kind == "ignored"


@pytest.mark.parametrize("status", ["queued", "in_progress", "waiting", "requested", "pending"])
def test_incomplete_runs_are_not_evaluative(dgw, status):
    for file in (SUITE, VISUAL):
        assert classify(dgw, file, gh_run(file, 1, SLOT, status=status), None).kind == "non_evaluative"


@pytest.mark.parametrize("file", [SUITE, VISUAL])
@pytest.mark.parametrize("conclusion", NON_SUCCESS)
def test_every_non_success_conclusion_is_failure_evidence(dgw, file, conclusion):
    evidence = classify(dgw, file, gh_run(file, 1, SLOT, conclusion=conclusion), [])
    assert evidence.kind == "failure"
    assert evidence.run["id"] == 1


@pytest.mark.parametrize("file", [SUITE, VISUAL])
def test_a_success_without_its_jobs_is_unavailable_never_healthy(dgw, file):
    with pytest.raises(dgw.EvidenceUnavailable):
        classify(dgw, file, gh_run(file, 1, SLOT), None)


def test_suite_recovery_needs_every_job_green(dgw):
    r = gh_run(SUITE, 1, SLOT)
    assert classify(dgw, SUITE, r, suite_jobs(r)).kind == "recovery"
    assert classify(dgw, SUITE, r, suite_jobs(r, skipped=SUITE_JOBS[-1])).kind == "non_evaluative"
    assert classify(dgw, SUITE, r, []).kind == "non_evaluative"


VISUAL_CARRIERS = {
    "compare-executed": ({}, "recovery"),
    "generation": ({"compare": "skipped", "generate": "success", "no_write": "skipped"}, "non_evaluative"),
    "compare-skipped": ({"compare": "skipped"}, "non_evaluative"),
    "compare-absent": ({"compare": None}, "non_evaluative"),
    "no-write-skipped": ({"no_write": "skipped"}, "non_evaluative"),
    "no-write-absent": ({"no_write": None}, "non_evaluative"),
    "job-skipped": ({"conclusion": "skipped"}, "non_evaluative"),
    "renamed-job": ({"name": "Visual regression"}, "non_evaluative"),
}


@pytest.mark.parametrize("carrier", list(VISUAL_CARRIERS))
def test_only_an_executed_compare_is_visual_recovery(dgw, carrier):
    options, kind = VISUAL_CARRIERS[carrier]
    r = gh_run(VISUAL, 1, SLOT, event="workflow_dispatch")
    assert classify(dgw, VISUAL, r, [visual_job(r, **options)]).kind == kind


def test_a_successful_visual_run_without_its_visual_job_is_not_recovery(dgw):
    r = gh_run(VISUAL, 1, SLOT)
    assert classify(dgw, VISUAL, r, []).kind == "non_evaluative"
    assert classify(dgw, VISUAL, r, suite_jobs(r)).kind == "non_evaluative"


# ------------------------------------------------------------------- failure_state


def test_failure_state_follows_the_newest_evaluative_evidence(dgw):
    sw = watched(dgw, SUITE)
    failed = gh_run(SUITE, 10, PREV, conclusion="failure")
    recovered = gh_run(SUITE, 11, SLOT)
    partial = gh_run(SUITE, 12, SLOT + HOUR, event="workflow_dispatch")
    running = gh_run(SUITE, 13, SLOT + 2 * HOUR, status="in_progress")
    foreign = gh_run(VISUAL, 14, SLOT + 3 * HOUR, conclusion="failure")
    evidence = [
        dgw.classify_run(sw, partial, suite_jobs(partial, skipped=SUITE_JOBS[0])),
        dgw.classify_run(sw, recovered, suite_jobs(recovered)),
        dgw.classify_run(sw, running, None),
        dgw.classify_run(sw, foreign, []),
        dgw.classify_run(sw, failed, suite_jobs(failed, failed=FAILED_JOB)),
    ]
    state = dgw.failure_state(sw, evidence)
    assert (state.status, state.evidence.run["id"]) == ("healthy", 11)

    later = gh_run(SUITE, 15, SLOT + 4 * HOUR, conclusion="timed_out")
    state = dgw.failure_state(sw, [dgw.classify_run(sw, later, []), *evidence])
    assert (state.status, state.evidence.run["id"]) == ("failing", 15)


def test_failure_state_is_unknown_without_evaluative_evidence(dgw):
    sw = watched(dgw, SUITE)
    assert dgw.failure_state(sw, []).status == "unknown"
    noise = [
        dgw.classify_run(sw, gh_run(SUITE, 1, SLOT, status="queued"), None),
        dgw.classify_run(sw, gh_run(VISUAL, 2, SLOT, conclusion="failure"), []),
        dgw.classify_run(sw, gh_run(SUITE, 3, SLOT, branch="feature", conclusion="failure"), []),
    ]
    assert dgw.failure_state(sw, noise).status == "unknown"


@pytest.mark.parametrize("order", [1, -1], ids=["listed-in-order", "listed-reversed"])
def test_a_re_run_attempt_outranks_its_own_first_attempt(dgw, order):
    sw = watched(dgw, SUITE)
    first = gh_run(SUITE, 20, SLOT, conclusion="failure")
    second = gh_run(SUITE, 20, SLOT, attempt=2)
    evidence = [dgw.classify_run(sw, first, []), dgw.classify_run(sw, second, suite_jobs(second))][::order]
    state = dgw.failure_state(sw, evidence)
    assert (state.status, state.evidence.run["run_attempt"]) == ("healthy", 2)


def test_generation_skipped_compare_and_suite_success_leave_the_visual_state_failing(dgw):
    vw = watched(dgw, VISUAL)
    failed = gh_run(VISUAL, 30, SLOT, conclusion="failure")
    generated = gh_run(VISUAL, 31, SLOT + HOUR, event="workflow_dispatch")
    skipped = gh_run(VISUAL, 32, SLOT + 2 * HOUR, event="workflow_dispatch")
    suite_green = gh_run(SUITE, 33, SLOT + 3 * HOUR)
    evidence = [
        dgw.classify_run(vw, failed, [visual_job(failed, compare="failure", conclusion="failure")]),
        dgw.classify_run(
            vw,
            generated,
            [visual_job(generated, compare="skipped", generate="success", no_write="skipped")],
        ),
        dgw.classify_run(vw, skipped, [visual_job(skipped, compare="skipped")]),
        dgw.classify_run(vw, suite_green, suite_jobs(suite_green)),
    ]
    state = dgw.failure_state(vw, evidence)
    assert (state.status, state.evidence.run["id"]) == ("failing", 30)


# ----------------------------------------------------------------- freshness_state


@pytest.mark.parametrize("conclusion", ["success", "failure", "cancelled", "timed_out"])
def test_a_completed_scheduled_run_in_the_slot_is_fresh_whatever_its_conclusion(dgw, conclusion):
    state = fresh(dgw, SUITE, [gh_run(SUITE, 1, SLOT + 6 * HOUR, conclusion=conclusion)], AFTER)
    assert (state.status, state.slot, state.run["id"]) == ("fresh", SLOT, 1)


def test_the_slot_boundary_is_inclusive_and_the_second_before_it_is_last_week(dgw):
    assert fresh(dgw, SUITE, [gh_run(SUITE, 1, SLOT)], AFTER).status == "fresh"
    assert fresh(dgw, SUITE, [gh_run(SUITE, 1, SLOT - SECOND)], AFTER).status == "missing"


@pytest.mark.parametrize(
    "offset, with_run, status",
    [
        (20 * HOUR - SECOND, True, "pending"),
        (20 * HOUR, True, "late"),
        (35 * HOUR, True, "late"),
        (20 * HOUR - SECOND, False, "pending"),
        (20 * HOUR, False, "missing"),
    ],
    ids=["running-before", "running-at", "running-near-deadline", "absent-before", "absent-at"],
)
def test_incomplete_and_absent_slots_turn_late_or_missing_at_the_threshold(dgw, offset, with_run, status):
    runs = [gh_run(SUITE, 1, SLOT + HOUR, status="in_progress")] if with_run else []
    assert fresh(dgw, SUITE, runs, SLOT + offset).status == status


def test_one_completed_run_makes_the_slot_fresh_despite_another_still_running(dgw):
    runs = [
        gh_run(SUITE, 1, SLOT + HOUR, status="in_progress"),
        gh_run(SUITE, 2, SLOT + 2 * HOUR, conclusion="failure"),
    ]
    state = fresh(dgw, SUITE, runs, AFTER)
    assert (state.status, state.run["id"]) == ("fresh", 2)


NOT_THIS_SLOT = {
    "manual-only": [gh_run(SUITE, 1, SLOT + HOUR, event="workflow_dispatch")],
    "manual-in-progress": [gh_run(SUITE, 1, SLOT + HOUR, event="workflow_dispatch", status="in_progress")],
    "prior-week": [gh_run(SUITE, 1, PREV), gh_run(SUITE, 2, PREV + 6 * HOUR)],
    "other-workflow": [gh_run(VISUAL, 1, SLOT + HOUR)],
    "other-branch": [gh_run(SUITE, 1, SLOT + HOUR, branch="release")],
    "other-events": [
        gh_run(SUITE, 1, SLOT + HOUR, event="push"),
        gh_run(SUITE, 2, SLOT + HOUR, event="workflow_run"),
    ],
}


@pytest.mark.parametrize("history", list(NOT_THIS_SLOT))
def test_runs_that_are_not_this_weeks_scheduled_run_never_satisfy_freshness(dgw, history):
    state = fresh(dgw, SUITE, NOT_THIS_SLOT[history], AFTER)
    assert (state.status, state.slot) == ("missing", SLOT)


# -------------------------------------------------------------------- plan_actions


def test_plan_actions_has_nothing_to_do_without_evidence_or_issues(dgw):
    for file in (SUITE, VISUAL):
        x = watched(dgw, file)
        assert dgw.plan_actions(x, dgw.failure_state(x, []), dgw.freshness_state(x, [], BEFORE), []) == []


def test_plan_actions_is_a_no_op_when_the_open_issue_already_cites_the_evidence(dgw, gh):
    s = seed_failure(gh, SUITE, 150)
    seed_success(gh, VISUAL, 900)
    run_watch(dgw, gh, AFTER)
    sw = watched(dgw, SUITE)
    state = dgw.failure_state(sw, [dgw.classify_run(sw, s, gh.jobs[(150, 1)])])
    assert dgw.plan_actions(sw, state, dgw.freshness_state(sw, [s], AFTER), gh.open_issues()) == []


# ------------------------------------------------------- reconcile: failure issues


def test_suite_and_visual_failures_each_open_their_own_issue(dgw, gh):
    s = seed_failure(gh, SUITE, 150)
    v = seed_failure(gh, VISUAL, 250, SLOT + 6 * MINUTE)
    report = run_watch(dgw, gh, AFTER)

    assert set(report.unavailable) == set()
    suite_issue, visual_issue = gh.only(SUITE, "failure"), gh.only(VISUAL, "failure")
    assert suite_issue["number"] != visual_issue["number"]
    for file, issue, r, failed_job, failed_step in (
        (SUITE, suite_issue, s, FAILED_JOB, FAILED_STEP),
        (VISUAL, visual_issue, v, VISUAL_JOB, COMPARE),
    ):
        assert issue["title"] == f"Deep Gate watch: {NAMES[file]} — failing"
        assert LABEL in {label["name"] for label in issue["labels"]}
        for fragment in (
            NAMES[file],
            str(r["id"]),
            r["html_url"],
            r["head_sha"],
            r["event"],
            r["conclusion"],
            failed_job,
            failed_step,
            "Status: UNRESOLVED",
        ):
            assert fragment in issue["body"], fragment
    assert gh.find(SUITE, "missing-schedule") == gh.find(VISUAL, "missing-schedule") == []
    assert ("POST", "/labels", {"name": LABEL}) not in [(m, p, b) for m, p, b in gh.writes]


@pytest.mark.parametrize("file", [SUITE, VISUAL])
@pytest.mark.parametrize("conclusion", ["cancelled", "timed_out", "skipped", "startup_failure"])
def test_every_non_success_completion_opens_that_workflows_issue(dgw, gh, file, conclusion):
    other = VISUAL if file == SUITE else SUITE
    seed_success(gh, other, 900)
    r = gh.add(gh_run(file, 150, SLOT + 5 * MINUTE, conclusion=conclusion))
    run_watch(dgw, gh, AFTER, event=delivered(r))
    issue = gh.only(file, "failure")
    assert conclusion in issue["body"] and str(r["id"]) in issue["body"]
    assert gh.find(other, "failure") == []


def test_a_newer_failure_updates_the_open_issue_instead_of_opening_another(dgw, gh):
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150)
    run_watch(dgw, gh, AFTER)
    number = gh.only(SUITE, "failure")["number"]
    newer = seed_failure(gh, SUITE, 200, SLOT + 3 * HOUR, event="workflow_dispatch")
    gh.writes.clear()
    run_watch(dgw, gh, AFTER + HOUR, event=delivered(newer))
    issue = gh.only(SUITE, "failure")
    assert issue["number"] == number
    assert "evidence=200.1" in issue["body"]
    assert ("POST", "/issues") not in [(m, p) for m, p, _ in gh.writes]


def test_a_duplicate_delivery_writes_nothing_the_second_time(dgw, gh):
    seed_success(gh, VISUAL, 900)
    s = seed_failure(gh, SUITE, 150)
    run_watch(dgw, gh, AFTER, event=delivered(s))
    assert len(gh.find(SUITE, "failure")) == 1
    gh.writes.clear()
    run_watch(dgw, gh, AFTER + 5 * MINUTE, event=delivered(s))
    assert gh.writes == []


def test_an_older_event_after_a_newer_one_never_regresses_the_issue(dgw, gh):
    seed_success(gh, VISUAL, 900)
    older = seed_failure(gh, SUITE, 150)
    newer = seed_failure(gh, SUITE, 200, SLOT + 3 * HOUR, event="workflow_dispatch")
    run_watch(dgw, gh, AFTER, event=delivered(newer))
    assert "evidence=200.1" in gh.only(SUITE, "failure")["body"]

    gh.runs = [r for r in gh.runs if r["id"] != 200]  # a stale listing
    gh.writes.clear()
    run_watch(dgw, gh, AFTER + 10 * MINUTE, event=delivered(older))
    assert gh.writes == []
    assert "evidence=200.1" in gh.only(SUITE, "failure")["body"]


def test_a_recovery_older_than_the_issue_evidence_does_not_close_it(dgw, gh):
    seed_success(gh, SUITE, 100)
    good = seed_success(gh, VISUAL, 150)
    bad = seed_failure(gh, VISUAL, 200, SLOT + 3 * HOUR, event="workflow_dispatch")
    run_watch(dgw, gh, AFTER, event=delivered(bad))
    gh.runs = [r for r in gh.runs if r["id"] != 200]
    gh.writes.clear()
    run_watch(dgw, gh, AFTER + 10 * MINUTE, event=delivered(good))
    assert gh.writes == []
    assert gh.only(VISUAL, "failure")["state"] == "open"


def test_duplicate_open_watch_issues_collapse_onto_the_lowest_number(dgw, gh):
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150)
    run_watch(dgw, gh, AFTER)
    original = gh.only(SUITE, "failure")
    for number in (original["number"] + 1, original["number"] + 2):
        gh.issues.append({**copy.deepcopy(original), "number": number})
    run_watch(dgw, gh, AFTER + 5 * MINUTE)
    assert gh.issue(original["number"])["state"] == "open"
    for number in (original["number"] + 1, original["number"] + 2):
        duplicate = gh.issue(number)
        assert duplicate["state"] == "closed"
        assert f"Duplicate of #{original['number']}" in issue_comments(gh, duplicate)


def test_the_label_is_created_before_the_first_issue_when_absent(dgw, gh):
    gh.label = False
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150)
    run_watch(dgw, gh, AFTER)
    order = [(m, p) for m, p, _ in gh.writes]
    assert order.index(("POST", "/labels")) < order.index(("POST", "/issues"))
    assert LABEL in {label["name"] for label in gh.only(SUITE, "failure")["labels"]}


# ------------------------------------------------------ reconcile: visual recovery


@pytest.mark.parametrize("event", ["schedule", "workflow_dispatch"])
def test_an_executed_compare_success_closes_the_visual_failure_issue(dgw, gh, event):
    seed_success(gh, SUITE, 100)
    seed_failure(gh, VISUAL, 150)
    run_watch(dgw, gh, AFTER)
    issue = gh.only(VISUAL, "failure")
    good = seed_success(gh, VISUAL, 160, SLOT + 4 * HOUR, event=event)
    run_watch(dgw, gh, AFTER + HOUR, event=delivered(good))
    assert gh.issue(issue["number"])["state"] == "closed"
    note = issue_comments(gh, issue)
    for fragment in (NAMES[VISUAL], str(good["id"]), good["head_sha"], COMPARE):
        assert fragment in note, fragment


@pytest.mark.parametrize("carrier", ["skipped-compare", "generation", "green-six-job-suite"])
def test_carriers_that_executed_no_comparison_never_close_the_visual_issue(dgw, gh, carrier):
    seed_success(gh, SUITE, 100)
    seed_failure(gh, VISUAL, 150)
    run_watch(dgw, gh, AFTER)
    number = gh.only(VISUAL, "failure")["number"]
    if carrier == "green-six-job-suite":
        carried = seed_success(gh, SUITE, 160, SLOT + 4 * HOUR, event="workflow_dispatch")
    else:
        carried = gh_run(VISUAL, 160, SLOT + 4 * HOUR, event="workflow_dispatch")
        options = {"compare": "skipped"}
        if carrier == "generation":
            options = {"compare": "skipped", "generate": "success", "no_write": "skipped"}
        gh.add(carried, [visual_job(carried, **options)])
    gh.writes.clear()
    run_watch(dgw, gh, AFTER + HOUR, event=delivered(carried))
    assert gh.writes == []
    assert gh.issue(number)["state"] == "open"


def test_a_manual_compare_recovery_closes_the_failure_issue_but_never_the_missing_one(dgw, gh):
    seed_success(gh, SUITE, 100)
    seed_failure(gh, VISUAL, 150, PREV + 5 * MINUTE)
    run_watch(dgw, gh, AFTER)
    failure, missing = gh.only(VISUAL, "failure"), gh.only(VISUAL, "missing-schedule")
    good = seed_success(gh, VISUAL, 160, AFTER + 10 * MINUTE, event="workflow_dispatch")
    run_watch(dgw, gh, AFTER + HOUR, event=delivered(good))
    assert gh.issue(failure["number"])["state"] == "closed"
    assert gh.issue(missing["number"])["state"] == "open"


# -------------------------------------------------------- reconcile: freshness issues


@pytest.mark.parametrize("file", [SUITE, VISUAL])
@pytest.mark.parametrize("history", ["none", "manual-only", "prior-week"])
def test_no_scheduled_run_in_the_current_slot_opens_a_missing_schedule_issue(dgw, gh, file, history):
    other = VISUAL if file == SUITE else SUITE
    seed_success(gh, other, 900)
    if history == "manual-only":
        seed_success(gh, file, 101, SLOT + HOUR, event="workflow_dispatch")
    if history == "prior-week":
        seed_success(gh, file, 101, PREV + 5 * MINUTE)
    run_watch(dgw, gh, AFTER)
    issue = gh.only(file, "missing-schedule")
    assert issue["title"] == f"Deep Gate watch: {NAMES[file]} — missing scheduled run"
    assert "Status: UNRESOLVED" in issue["body"]
    assert "2026-10-19" in issue["body"]
    assert gh.find(other, "missing-schedule") == []
    assert gh.find(file, "failure") == []


@pytest.mark.parametrize(
    "now, running, opened",
    [(BEFORE, True, 0), (AFTER, True, 1), (BEFORE, False, 0)],
    ids=["running-before-threshold", "running-after-threshold", "absent-before-threshold"],
)
def test_the_current_slot_is_pending_before_the_threshold_and_late_after(dgw, gh, now, running, opened):
    seed_success(gh, VISUAL, 900)
    if running:
        gh.add(gh_run(SUITE, 101, SLOT + HOUR, status="in_progress"))
    run_watch(dgw, gh, now)
    assert len(gh.find(SUITE, "missing-schedule")) == opened
    assert gh.find(SUITE, "failure") == []
    if not opened:
        assert gh.writes == []


def test_the_missing_issue_follows_the_slot_and_only_a_scheduled_run_closes_it(dgw, gh):
    seed_success(gh, VISUAL, 801, PREV + 5 * MINUTE)
    run_watch(dgw, gh, PREV + 21 * HOUR)
    issue = gh.only(SUITE, "missing-schedule")
    assert "2026-10-12" in issue["body"]

    seed_success(gh, VISUAL, 802)
    gh.writes.clear()
    run_watch(dgw, gh, AFTER)
    assert gh.only(SUITE, "missing-schedule")["number"] == issue["number"]
    assert "2026-10-19" in gh.issue(issue["number"])["body"]
    assert ("POST", "/issues") not in [(m, p) for m, p, _ in gh.writes]

    manual = seed_success(gh, SUITE, 300, SLOT + 21 * HOUR + 10 * MINUTE, event="workflow_dispatch")
    gh.writes.clear()
    run_watch(dgw, gh, SLOT + 21 * HOUR + 30 * MINUTE, event=delivered(manual))
    assert gh.writes == []
    assert gh.issue(issue["number"])["state"] == "open"

    scheduled = seed_success(gh, SUITE, 301, SLOT + 22 * HOUR)
    run_watch(dgw, gh, SLOT + 23 * HOUR, event=delivered(scheduled))
    assert gh.issue(issue["number"])["state"] == "closed"
    assert str(scheduled["id"]) in issue_comments(gh, issue)


def test_freshness_and_failure_issues_recover_independently(dgw, gh):
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150, PREV + 5 * MINUTE)
    run_watch(dgw, gh, AFTER)
    failure, missing = gh.only(SUITE, "failure"), gh.only(SUITE, "missing-schedule")

    late = seed_failure(gh, SUITE, 160, SLOT + 22 * HOUR)
    run_watch(dgw, gh, SLOT + 24 * HOUR, event=delivered(late))
    assert gh.issue(missing["number"])["state"] == "closed"
    assert str(late["id"]) in issue_comments(gh, missing)
    assert gh.issue(failure["number"])["state"] == "open"
    assert "evidence=160.1" in gh.issue(failure["number"])["body"]

    good = seed_success(gh, SUITE, 170, SLOT + 25 * HOUR, event="workflow_dispatch")
    run_watch(dgw, gh, SLOT + 26 * HOUR, event=delivered(good))
    assert gh.issue(failure["number"])["state"] == "closed"
    assert gh.find(SUITE, "missing-schedule") == []


# ------------------------------------------------------- reconcile: event payloads


@pytest.mark.parametrize("listed", ["in-progress", "lower-attempt"])
def test_the_delivered_event_supersedes_a_stale_listing_of_the_same_run(dgw, gh, listed):
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150)
    run_watch(dgw, gh, AFTER)
    number = gh.only(SUITE, "failure")["number"]

    done = gh_run(SUITE, 160, SLOT + 2 * HOUR, event="workflow_dispatch", attempt=2)
    if listed == "in-progress":
        gh.add({**done, "status": "in_progress", "conclusion": None})
    else:
        stale = {**done, "run_attempt": 1, "conclusion": "failure"}
        gh.add(stale, suite_jobs(stale, failed=FAILED_JOB))
    gh.jobs[(160, 2)] = suite_jobs(done)
    run_watch(dgw, gh, AFTER + HOUR, event=delivered(done))
    assert gh.issue(number)["state"] == "closed"


def test_a_stale_event_for_an_older_attempt_does_not_override_the_listing(dgw, gh):
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150)
    run_watch(dgw, gh, AFTER)
    number = gh.only(SUITE, "failure")["number"]
    done = gh_run(SUITE, 160, SLOT + 2 * HOUR, event="workflow_dispatch", attempt=2)
    gh.add(done, suite_jobs(done))
    run_watch(dgw, gh, AFTER + HOUR, event=delivered({**done, "run_attempt": 1, "conclusion": "failure"}))
    assert gh.issue(number)["state"] == "closed"
    assert gh.find(SUITE, "failure") == []


def test_an_event_from_an_unwatched_workflow_changes_nothing(dgw, gh):
    seed_success(gh, SUITE, 100)
    seed_success(gh, VISUAL, 900)
    foreign = {**gh_run(SUITE, 999, SLOT + HOUR, conclusion="failure"), "path": ".github/workflows/ci.yml", "name": "CI"}
    report = run_watch(dgw, gh, AFTER, event=delivered(foreign))
    assert set(report.unavailable) == set()
    assert gh.writes == []


# ------------------------------------------------------ reconcile: pagination, API


def test_runs_are_read_across_every_page(dgw, gh):
    seed_success(gh, VISUAL, 900)
    seed_success(gh, SUITE, 500)  # the only scheduled run is the oldest, so it is listed last
    for n in range(3):
        seed_success(gh, SUITE, 501 + n, SLOT + (n + 1) * HOUR, event="workflow_dispatch")
    gh.page_size = 1
    run_watch(dgw, gh, AFTER)
    assert gh.writes == []
    pages = {q.get("page", "1") for _, p, q, _ in gh.requests if p.endswith(f"/workflows/{SUITE}/runs")}
    assert len(pages) == 4


def test_jobs_are_read_across_every_page(dgw, gh):
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150)
    run_watch(dgw, gh, AFTER)
    number = gh.only(SUITE, "failure")["number"]
    partial = gh_run(SUITE, 160, SLOT + 2 * HOUR, event="workflow_dispatch")
    gh.add(partial, suite_jobs(partial, skipped=SUITE_JOBS[-1]))  # the skip sits on the last page
    gh.page_size = 1
    gh.writes.clear()
    run_watch(dgw, gh, AFTER + HOUR)
    assert gh.writes == []
    assert gh.issue(number)["state"] == "open"
    pages = {q.get("page", "1") for _, p, q, _ in gh.requests if p.endswith("/actions/runs/160/attempts/1/jobs")}
    assert len(pages) == len(SUITE_JOBS)


def test_open_issues_are_read_across_every_page(dgw, gh):
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150)
    run_watch(dgw, gh, AFTER)
    for n in range(3):
        gh.note(f"hand-filed {n}")  # newer, so the watch's own issue is listed last
    gh.page_size = 1
    gh.writes.clear()
    run_watch(dgw, gh, AFTER + 5 * MINUTE)
    assert gh.writes == []
    assert all(i["state"] == "open" for i in gh.issues)
    pages = {q.get("page", "1") for m, p, q, _ in gh.requests if m == "GET" and p == f"{PREFIX}/issues"}
    assert len(pages) == 4


@pytest.mark.parametrize("fault", ["502", "403", "malformed", "endless", "502@2", "slow"])
def test_an_unreadable_runs_listing_isolates_that_workflow_without_writes(dgw, gh, fault):
    seed_failure(gh, SUITE, 150)
    for n in range(3):
        seed_failure(gh, VISUAL, 200 + n, SLOT + n * HOUR, event="workflow_dispatch")
    gh.page_size = 1 if fault == "502@2" else 100
    gh.faults[f"/actions/workflows/{VISUAL}/runs"] = fault
    report = run_watch(dgw, gh, AFTER, timeout=1.0 if fault == "slow" else 5.0)
    assert set(report.unavailable) == {VISUAL}
    assert not [x for x in gh.writes if VISUAL in json.dumps(x) or NAMES[VISUAL] in json.dumps(x)]
    assert gh.find(VISUAL, "failure") == gh.find(VISUAL, "missing-schedule") == []
    assert gh.only(SUITE, "failure")
    listed = Counter(p for _, p, _, _ in gh.requests if p.endswith(f"/workflows/{VISUAL}/runs"))
    assert max(listed.values()) <= 100


@pytest.mark.parametrize("field, value", [("run_attempt", 1), ("head_sha", "f" * 40), ("run_id", 999)])
def test_jobs_of_another_attempt_head_or_run_are_unavailable_evidence(dgw, gh, field, value):
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150)
    run_watch(dgw, gh, AFTER)
    number = gh.only(SUITE, "failure")["number"]
    good = gh_run(SUITE, 160, SLOT + 2 * HOUR, event="workflow_dispatch", attempt=2)
    listed = suite_jobs(good)
    listed[-1] = {**listed[-1], field: value}
    gh.add(good, listed)
    gh.writes.clear()
    report = run_watch(dgw, gh, AFTER + HOUR, event=delivered(good))
    assert set(report.unavailable) == {SUITE}
    assert gh.writes == []
    assert gh.issue(number)["state"] == "open"


def test_dry_run_reads_but_never_writes(dgw, gh):
    gh.label = False
    seed_failure(gh, SUITE, 150)  # and the visual workflow has no run at all
    run_watch(dgw, gh, AFTER, dry_run=True)
    assert gh.writes == [] and gh.issues == []
    assert {method for method, *_ in gh.requests} == {"GET"}


def test_requests_are_authenticated_and_scoped_to_the_named_endpoints(dgw, gh):
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150)
    run_watch(dgw, gh, AFTER)
    assert gh.requests
    for _, path, _, headers in gh.requests:
        assert headers["authorization"] == f"Bearer {TOKEN}"
        assert headers["x-github-api-version"] == "2022-11-28"
        assert path.startswith(PREFIX + "/")
        assert "/artifacts" not in path and "/logs" not in path

    listings = {p.split("/")[-2]: q for m, p, q, _ in gh.requests if m == "GET" and p.endswith("/runs")}
    assert set(listings) == {SUITE, VISUAL}
    for query in listings.values():
        assert (query["branch"], query["per_page"]) == ("main", "100")
        assert query["created"].startswith(">=")
        since = datetime.strptime(query["created"][2:12], "%Y-%m-%d").date()
        assert (AFTER - 22 * DAY).date() <= since <= (AFTER - 21 * DAY).date()
    issue_queries = [q for m, p, q, _ in gh.requests if m == "GET" and p == f"{PREFIX}/issues"]
    assert issue_queries and all(q["state"] == "open" and q["labels"] == LABEL for q in issue_queries)


# ----------------------------------------------------------------------------- CLI


def watch_cli(gh, tmp_path, *args, event=None):
    summary = tmp_path / "summary.md"
    env = {k: v for k, v in os.environ.items() if not k.startswith("GITHUB_")}
    env.update(GH_TOKEN=TOKEN, GITHUB_API_URL=gh.url, GITHUB_STEP_SUMMARY=str(summary), NO_PROXY="*")
    argv = [sys.executable, str(SCRIPT), "reconcile", "--repo", REPO, "--now", iso(AFTER), *args]
    if event is not None:
        payload = tmp_path / "event.json"
        payload.write_text(event if isinstance(event, str) else json.dumps(event), encoding="utf-8")
        argv += ["--event-path", str(payload)]
    proc = subprocess.run(argv, env=env, cwd=ROOT, capture_output=True, text=True, timeout=120, check=False)
    return proc, summary.read_text(encoding="utf-8") if summary.is_file() else ""


def test_cli_reconciles_exits_zero_and_summarises_both_workflows(dgw, gh, tmp_path):
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150)
    proc, summary = watch_cli(gh, tmp_path, event=SCHEDULE_EVENT)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert gh.only(SUITE, "failure")
    assert NAMES[SUITE] in summary and NAMES[VISUAL] in summary
    # A schedule event has no watched run to time; the summary must not claim a measured latency.
    assert not re.search(r"latency[^\n]*\d", summary, re.IGNORECASE), summary


def test_cli_summary_measures_dispatch_latency_for_a_workflow_run_event(dgw, gh, tmp_path):
    seed_success(gh, VISUAL, 900)
    s = gh_run(SUITE, 150, SLOT + 5 * MINUTE, conclusion="failure", updated=AFTER - 450 * SECOND)
    gh.add(s, suite_jobs(s, failed=FAILED_JOB))
    proc, summary = watch_cli(gh, tmp_path, event=delivered(s))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert re.search(r"latency[^\n]*\b450\b", summary, re.IGNORECASE), summary


def test_cli_dry_run_reports_the_plan_and_writes_nothing(dgw, gh, tmp_path):
    gh.label = False
    seed_failure(gh, SUITE, 150)
    proc, summary = watch_cli(gh, tmp_path, "--dry-run", event=SCHEDULE_EVENT)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert gh.writes == [] and gh.issues == []
    assert "create" in summary.lower()


CLI_FAULTS = [
    ("/issues", "502"),
    ("/issues", "403"),
    ("/issues", "malformed"),
    ("/issues", "endless"),
    ("/issues", "502@2"),
    ("/actions/workflows/", "502"),
    ("/actions/workflows/", "endless"),
    ("/jobs", "502"),
    ("/jobs", "malformed"),
]


@pytest.mark.parametrize(
    "needle, fault", CLI_FAULTS, ids=[f"{n.strip('/').split('/')[-1]}-{f}" for n, f in CLI_FAULTS]
)
def test_cli_exits_two_and_writes_nothing_when_evidence_is_unavailable(dgw, gh, tmp_path, needle, fault):
    seed_failure(gh, SUITE, 150)
    seed_failure(gh, VISUAL, 250)
    for n in range(3):
        gh.note(f"hand-filed {n}")
    gh.page_size = 1 if fault == "502@2" else 100
    gh.faults[needle] = fault
    proc, summary = watch_cli(gh, tmp_path, event=SCHEDULE_EVENT)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert gh.writes == []
    assert "unavailable" in summary.lower()
    assert max(Counter(p for _, p, _, _ in gh.requests if needle in p).values(), default=0) <= 100


def test_cli_exits_one_on_an_unreadable_event_payload(dgw, gh, tmp_path):
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150)
    proc, _ = watch_cli(gh, tmp_path, event="{not json")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert gh.writes == []
