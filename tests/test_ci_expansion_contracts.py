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
from scripts import ci_selected_report as selected_report
from scripts.release_gate import EXPECTED_CONTEXTS, REQUIRED_CONTEXTS
from tests.test_release_workflow_contracts import (
    ALL_WORKFLOWS,
    CI,
    PACKAGED,
    RELEASE,
    bash_executable,
    command,
    executable,
    jobs,
    job_name,
    permissions,
    step_condition,
    steps,
    strip_comments,
    triggers,
)
from tests.test_release_workflow_contracts import text as workflow_text
from tests.worktree_cleanup.support import ROOT
from tests.test_playwright_shard_launcher_contracts import launcher_array

GUARD_FILE = "tests/test_guard_destructive_command.py"
FAN_IN_DEPENDENCIES = ("pytest-core", "guard-hook-shard", "guard-hook-tests", "workflow-contracts-windows")
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


@pytest.mark.parametrize("job_id", ("pytest-core", "guard-hook-shard", "workflow-contracts-windows"))
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
    ZIZMOR_STEP: [
        f"{LINT_BIN}/zizmor", "--min-severity", "medium", "--format", "plain", ".github/workflows", ".github/dependabot.yml",
    ],
}
DEPENDABOT = ROOT / ".github" / "dependabot.yml"
ZIZMOR_CONDITIONS = {"${{ !cancelled() }}", "!cancelled()", "${{ always() }}", "always()"}

# (workflow file, rule) -> (exact occurrences, reason). One inline directive per SC2016
# finding at f3adacf1; B2 adds no zizmor entry, and any later one is a deliberate edit here.
LINT_SUPPRESSIONS = {
    ("ci.yml", "SC2016"): (4, "single-quoted `$`/backtick text is printed literally on purpose"),
    # D3: zizmor flags every `workflow_run` trigger.
    ("deep-gate-watch.yml", "dangerous-triggers"): (
        1,
        "D3 requires workflow_run; the watched workflows are schedule/dispatch-only here, the "
        "trigger is filtered to main, and the job checks out only the default-branch revision, "
        "downloads no artifact, executes nothing from the triggering run and reads the event "
        "only as data via $GITHUB_EVENT_PATH",
    ),
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
        for flag in ("--proto", "--proto-redir"):
            assert any(argv[i : i + 2] == [flag, "=https"] for i in range(len(argv))), (flag, argv)
        assert "--max-time" in argv, argv
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
    # Policy: a future workflow-level env must change this line deliberately, since it could reconfigure the linters.
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


def tag_path_workflows():
    """release.yml plus every local workflow it reaches through `uses: ./`, transitively."""
    found, pending = [], [RELEASE]
    while pending:
        path = pending.pop()
        if path not in found:
            found.append(path)
            pending += [
                ROOT / local for local in re.findall(r"^ *(?:- )?uses: \./(\S+)", executable(path), re.MULTILINE)
            ]
    return found


def test_release_setup_steps_restore_no_cache():
    # zizmor checks release.yml's own steps only; a cache in a workflow_call child is
    # restored by the same tag run, so the child is held to the same rule (section 18).
    reached = tag_path_workflows()
    assert PACKAGED in reached
    for path in reached:
        setups = steps_using(path, "actions/setup-python") + steps_using(path, "actions/setup-node")
        assert setups or path not in (RELEASE, PACKAGED), path.name
        for where, step in setups:
            assert not re.search(r"^        cache", key_body(step, "with", 6), re.MULTILINE), (path.name, where)
        assert "actions/cache" not in executable(path), path.name


def test_every_dependabot_ecosystem_waits_out_the_cooldown():
    # zizmor's dependabot-cooldown threshold is 7 days. One uniform window, no semver
    # split, so any change to it is a deliberate edit here (section 18).
    entries = re.split(r"^  - package-ecosystem:", DEPENDABOT.read_text(encoding="utf-8"), flags=re.MULTILINE)[1:]
    assert sorted(entry.splitlines()[0].strip() for entry in entries) == ['"github-actions"', '"npm"', '"pip"']
    for entry in entries:
        cooldown = key_body(entry, "cooldown", 4)
        assert mapping_keys(cooldown, 6) == {"default-days"}, entry.splitlines()[0]
        assert re.search(r"^      default-days: 7[ \t]*$", cooldown, re.MULTILINE), entry.splitlines()[0]


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


# =================================================== B3: Dependency Review
#
# The PR-only dependency gate: one pinned action step whose policy inputs are all explicit,
# a read-only token, and no path into the release gate or the `Run Tests` fan-in.

DEPENDENCY_REVIEW_JOB_ID = "dependency-review"
DEPENDENCY_REVIEW_NAME = "Dependency Review"
DEPENDENCY_REVIEW_STEP = "Review dependency changes"
DEPENDENCY_REVIEW_ACTION = "actions/dependency-review-action"
DEPENDENCY_REVIEW_SHA = "a1d282b36b6f3519aa1f3fc636f609c47dddb294"
DEPENDENCY_REVIEW_VERSION = "v5.0.0"
DEPENDENCY_REVIEW_METADATA_BLOB = "5f6cf73d694f70892899c2768fa9814a9218dd0d"  # action.yml at the pin
DEPENDENCY_REVIEW_CONDITION = "github.event_name == 'pull_request'"
DEPENDENCY_REVIEW_CONDITIONS = {DEPENDENCY_REVIEW_CONDITION, f"${{{{ {DEPENDENCY_REVIEW_CONDITION} }}}}"}
# Exact job keys: an extra `env:` could inject INPUT_* variables the `with:` map never shows.
DEPENDENCY_REVIEW_JOB_KEYS = {"name", "runs-on", "timeout-minutes", "permissions", "if", "steps"}
# Every input explicit, so a changed upstream default cannot change the policy. Scorecard
# calls third-party APIs whose outage would red the check; a license check without lists
# gates nothing today and starts blocking silently once a list appears.
DEPENDENCY_REVIEW_SCOPES = ["runtime", "development", "unknown"]  # order pinned, spacing not
DEPENDENCY_REVIEW_INPUTS = {
    "fail-on-severity": "high",
    "fail-on-scopes": ", ".join(DEPENDENCY_REVIEW_SCOPES),
    "warn-only": "false",
    "vulnerability-check": "true",
    "license-check": "false",
    "show-openssf-scorecard": "false",
    "comment-summary-in-pr": "never",
    "retry-on-snapshot-warnings": "false",
}
# A skipped required check counts as success, so either trigger would let this gate pass
# without running (merge_group) or run it against an untrusted base (pull_request_target).
DEPENDENCY_REVIEW_BANNED_TRIGGERS = ("pull_request_target", "merge_group")
ACTION_INVENTORY = ROOT / "docs" / "ci_cd_expansion" / "B1_ACTION_INVENTORY.md"
ACTION_REFERENCE = re.compile(r"([\w.-]+)/dependency-review-action(@\S*)?", re.IGNORECASE)


def dependency_review_job():
    return strip_comments(ci_job(DEPENDENCY_REVIEW_JOB_ID))


def job_needs(block):
    """Every job id in a job's `needs:`, in flow-list, bare or block-sequence form; [] if none."""
    found = re.findall(r"^    needs:[ \t]*(.*?)[ \t]*$", block, re.MULTILINE)
    assert len(found) <= 1, found
    if not found:
        return []
    inline = found[0].split(" #", 1)[0].strip()
    if inline:
        return [item.strip().strip("'\"") for item in inline.strip("[]").split(",") if item.strip()]
    return re.findall(r"^ +- ['\"]?([A-Za-z0-9_-]+)", key_body(block, "needs", 4), re.MULTILINE)


def action_inputs(step):
    """A step's `with:` map as {input: unquoted value}; every line must be one plain input."""
    inputs = {}
    for line in key_body(step, "with", 6).splitlines():
        if not line.strip():
            continue
        # A deeper line is a folded continuation or block scalar: `high` + `  low` reads "high low".
        match = re.fullmatch(r" {8}([A-Za-z0-9_-]+):[ \t]*(.*?)[ \t]*", line)
        assert match, f"`with:` line is not a one-line input: {line!r}"
        key, value = match.group(1), match.group(2).split(" #", 1)[0].strip()
        assert key not in inputs, f"input {key} is declared twice"
        if len(value) > 1 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        inputs[key] = value
    return inputs


def test_exactly_one_ci_job_reports_the_dependency_review_name():
    named = [job_id for job_id, block in jobs(CI).items() if job_name(block) == DEPENDENCY_REVIEW_NAME]
    assert named == [DEPENDENCY_REVIEW_JOB_ID]
    # jobs() is a dict: a second block under the same id would silently replace the first.
    source = executable(CI)
    assert len(re.findall(rf"^  {DEPENDENCY_REVIEW_JOB_ID}:[ \t]*$", source, re.MULTILINE)) == 1
    assert len(re.findall(rf"^    name: {DEPENDENCY_REVIEW_NAME}[ \t]*$", source, re.MULTILINE)) == 1


def test_dependency_review_runs_for_pull_request_events_only():
    found = re.findall(r"^    if:[ \t]*(.*?)[ \t]*$", dependency_review_job(), re.MULTILINE)
    conditions = [condition.split(" #", 1)[0].strip() for condition in found]
    assert len(conditions) == 1 and conditions[0] in DEPENDENCY_REVIEW_CONDITIONS, found


def test_the_dependency_review_job_cannot_wait_soften_or_widen_itself():
    block = dependency_review_job()
    # `strategy:` mints a `(matrix value)` suffix, renaming the check C4 will require.
    for key in ("needs", "strategy", "continue-on-error", "services", "container", "env"):
        assert not re.search(rf"^    {key}:", block, re.MULTILINE), key
    assert mapping_keys(block, 4) == DEPENDENCY_REVIEW_JOB_KEYS
    assert re.search(r"^    runs-on: ubuntu-latest[ \t]*$", block, re.MULTILINE)
    timeout = re.findall(r"^    timeout-minutes: (\d+)[ \t]*$", block, re.MULTILINE)
    assert len(timeout) == 1 and 1 <= int(timeout[0]) <= 10, timeout


def test_the_dependency_review_token_is_read_only():
    block = dependency_review_job()
    assert permissions(block) == {"contents": "read"}
    # permissions() stops at a blank line; key_body() does not, so a hidden scope still reds.
    assert len(re.findall(r"^    permissions:", block, re.MULTILINE)) == 1
    assert mapping_keys(key_body(block, "permissions", 4), 6) == {"contents"}


def test_dependency_review_is_one_pinned_action_step_and_nothing_else():
    block = dependency_review_job()
    parsed = steps(block)
    assert [name for name, _ in parsed] == [DEPENDENCY_REVIEW_STEP]
    # An unnamed `- uses:` step merges into a neighbour in steps(); counting `uses:` catches it.
    assert len(re.findall(r"^ *(?:- )?uses:", block, re.MULTILINE)) == 1
    assert not re.search(r"^ *(?:- )?run:", block, re.MULTILINE)
    assert "actions/checkout" not in block.lower()
    step = parsed[0][1]
    assert mapping_keys(step, 6) == {"uses", "with"}
    pin = rf"^      uses: {DEPENDENCY_REVIEW_ACTION}@{DEPENDENCY_REVIEW_SHA}[ \t]+#[ \t]*{re.escape(DEPENDENCY_REVIEW_VERSION)}[ \t]*$"
    assert re.search(pin, step, re.MULTILINE), step


def test_dependency_review_inputs_are_exactly_the_adopted_policy():
    step = dict(steps(dependency_review_job())).get(DEPENDENCY_REVIEW_STEP)
    assert step is not None, f"no {DEPENDENCY_REVIEW_STEP} step"
    assert len(re.findall(r"^      with:", step, re.MULTILINE)) == 1
    inputs = action_inputs(step)
    # Exact key set: config-file, allow-ghsas, base-ref, repo-token or any other key reds.
    assert set(inputs) == set(DEPENDENCY_REVIEW_INPUTS)
    assert [scope.strip() for scope in inputs.pop("fail-on-scopes").split(",")] == DEPENDENCY_REVIEW_SCOPES
    expected = dict(DEPENDENCY_REVIEW_INPUTS)
    del expected["fail-on-scopes"]
    assert inputs == expected


def test_no_job_waits_on_dependency_review():
    declared = {job_id: job_needs(strip_comments(block)) for job_id, block in jobs(CI).items()}
    # Vacuity floor: the parser must still read the fan-in it is guarding.
    assert set(FAN_IN_DEPENDENCIES) <= set(declared["run-tests"])
    assert [job_id for job_id, needed in declared.items() if DEPENDENCY_REVIEW_JOB_ID in needed] == []


def test_dependency_review_is_absent_from_every_release_gate_context_set():
    # PR-only: a push to main never reports it, so the release gate would wait out its deadline.
    from collections.abc import Mapping

    module = importlib.import_module("scripts.release_gate")
    sets = {name: value for name, value in vars(module).items() if name.endswith("CONTEXTS")}
    # `in` on a str is a substring test, so a string-typed *CONTEXTS would answer the wrong question.
    assert [name for name, value in sets.items() if isinstance(value, str)] == []
    checked = set()
    for name, value in sets.items():
        # PR_* sets are the PR-only merge sets B3 belongs in (docs/ci_cd_expansion/PLANNING.md §11.5).
        if name.startswith("PR_"):
            continue
        if isinstance(value, Mapping):
            value = list(value.keys())
        elif not isinstance(value, (tuple, list, set, frozenset)):
            continue  # Deliberately skipped: not a collection of context names.
        assert [context for context in value if DEPENDENCY_REVIEW_NAME in str(context)] == [], name
        checked.add(name)
    # C4: if these constants are renamed or split, update this requirement deliberately.
    assert {"REQUIRED_CONTEXTS", "EXPECTED_CONTEXTS"} <= checked


def test_the_action_inventory_records_the_dependency_review_pin():
    rows = [
        line
        for line in ACTION_INVENTORY.read_text(encoding="utf-8").splitlines()
        if line.lstrip().startswith("|")
        and all(
            fact in line
            for fact in (
                DEPENDENCY_REVIEW_ACTION,
                DEPENDENCY_REVIEW_VERSION,
                DEPENDENCY_REVIEW_SHA,
                DEPENDENCY_REVIEW_METADATA_BLOB,
            )
        )
    ]
    assert rows, f"{ACTION_INVENTORY.name} has no table row with the {DEPENDENCY_REVIEW_ACTION} pin and metadata blob"


def test_every_dependency_review_action_reference_is_the_one_pinned_step():
    references = [
        (path.name, match.group(0))
        for path in ALL_WORKFLOWS
        for match in ACTION_REFERENCE.finditer(executable(path))
    ]
    # Owner/repo match case-insensitively on GitHub, so a fork or recased copy counts too.
    assert references == [("ci.yml", f"{DEPENDENCY_REVIEW_ACTION}@{DEPENDENCY_REVIEW_SHA}")], references
    assert len(ACTION_REFERENCE.findall(dependency_review_job())) == 1


def test_ci_triggers_cannot_skip_or_bypass_dependency_review():
    on = triggers(CI)
    assert "pull_request" in on, on
    for event in DEPENDENCY_REVIEW_BANNED_TRIGGERS:
        assert event not in on, f"{event}: revisit Dependency Review's PR-only skip (PLANNING.md §17.4) before adding it"


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
# freshness_state(watched, runs, now, *, workflow_created_at) takes the aware UTC datetime from
# GET /actions/workflows/{file} (fetched once per watched file by reconcile) and returns
# `not_applicable` when the workflow was created after the slot start (created_at == slot is
# applicable); that endpoint failing makes the workflow unavailable, never fresh or healthy.
# A non-success run whose jobs cannot be listed (HTTP/timeout/JSON error or a run_id/attempt/head
# mismatch) is still failure evidence: its issue body says "job details unavailable", the CLI
# summary says so too, and the workflow is not unavailable; a success run's unreadable jobs stay
# EvidenceUnavailable. Every issue body has a visible line, outside the marker comment, naming
# Deep Gate Watch and saying "do not edit".
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
CREATED = datetime(2026, 1, 5, 9, 0, tzinfo=UTC)  # both watched workflows long predate SLOT
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
        self.created = {SUITE: CREATED, VISUAL: CREATED}  # served by GET /actions/workflows/{file}
        # path substring (or exact path suffix when it ends in "$") ->
        # "404" | "502" | "403" | "malformed" | "slow" | "endless"; "kind@N" only on page N
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

        fault = next(
            (
                kind
                for needle, kind in gh.faults.items()
                if (parts.path.endswith(needle[:-1]) if needle.endswith("$") else needle in parts.path)
            ),
            "",
        )
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
        workflow = re.fullmatch(r"/actions/workflows/([^/]+)", path)
        if method == "GET" and workflow and workflow[1] in gh.created:
            file = workflow[1]
            return self._reply(
                200,
                {
                    "id": len(file),
                    "name": NAMES[file],
                    "path": f".github/workflows/{file}",
                    "state": "active",
                    "created_at": iso(gh.created[file]),
                    "updated_at": iso(gh.created[file]),
                },
            )
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


def fresh(dgw, file, runs, now, created=CREATED):
    return dgw.freshness_state(watched(dgw, file), runs, now, workflow_created_at=created)


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


APPLICABILITY = {
    # A workflow merged after Monday 03:17 never had this slot to miss.
    "created-after-slot": (SLOT + 10 * HOUR, [], AFTER, "not_applicable"),
    "created-a-second-after": (SLOT + SECOND, [], AFTER, "not_applicable"),
    "created-after-slot-before-threshold": (SLOT + HOUR, [], BEFORE, "not_applicable"),
    "created-after-slot-manual-run": (
        SLOT + 10 * HOUR,
        [gh_run(VISUAL, 1, SLOT + 11 * HOUR, event="workflow_dispatch")],
        AFTER,
        "not_applicable",
    ),
    "created-a-second-before": (SLOT - SECOND, [], AFTER, "missing"),
    "created-exactly-at-slot": (SLOT, [], AFTER, "missing"),
    "created-at-slot-and-ran": (SLOT, [gh_run(VISUAL, 1, SLOT)], AFTER, "fresh"),
    "next-slot-applies": (SLOT + 10 * HOUR, [], SLOT + 7 * DAY + 21 * HOUR, "missing"),
}


@pytest.mark.parametrize("case", list(APPLICABILITY))
def test_a_slot_that_began_before_the_workflow_existed_is_not_applicable(dgw, case):
    created, runs, now, status = APPLICABILITY[case]
    state = fresh(dgw, VISUAL, runs, now, created=created)
    assert (state.status, state.slot) == (status, dgw.expected_slot(now))


def test_freshness_state_requires_the_workflow_creation_time(dgw):
    with pytest.raises(TypeError):
        dgw.freshness_state(watched(dgw, VISUAL), [], AFTER)
    with pytest.raises(TypeError):
        dgw.freshness_state(watched(dgw, VISUAL), [], AFTER, CREATED)  # keyword-only


# -------------------------------------------------------------------- plan_actions


def test_plan_actions_has_nothing_to_do_without_evidence_or_issues(dgw):
    for file in (SUITE, VISUAL):
        x = watched(dgw, file)
        assert dgw.plan_actions(x, dgw.failure_state(x, []), fresh(dgw, file, [], BEFORE), []) == []


def test_plan_actions_is_a_no_op_when_the_open_issue_already_cites_the_evidence(dgw, gh):
    s = seed_failure(gh, SUITE, 150)
    seed_success(gh, VISUAL, 900)
    run_watch(dgw, gh, AFTER)
    sw = watched(dgw, SUITE)
    state = dgw.failure_state(sw, [dgw.classify_run(sw, s, gh.jobs[(150, 1)])])
    assert dgw.plan_actions(sw, state, fresh(dgw, SUITE, [s], AFTER), gh.open_issues()) == []


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


# ------------------------------------------- reconcile: workflow created after the slot


def test_a_workflow_merged_after_the_slot_opens_no_missing_schedule_issue(dgw, gh):
    seed_success(gh, SUITE, 100)
    gh.created[VISUAL] = SLOT + 10 * HOUR  # merged Monday afternoon; no run exists yet
    report = run_watch(dgw, gh, AFTER)
    assert set(report.unavailable) == set()
    assert gh.writes == []
    assert gh.find(VISUAL, "missing-schedule") == []


@pytest.mark.parametrize("created", [SLOT - SECOND, SLOT], ids=["before-slot", "exactly-at-slot"])
def test_a_workflow_that_existed_at_the_slot_still_reports_a_missing_run(dgw, gh, created):
    seed_success(gh, SUITE, 100)
    gh.created[VISUAL] = created
    run_watch(dgw, gh, AFTER)
    assert "2026-10-19" in gh.only(VISUAL, "missing-schedule")["body"]


def test_a_not_applicable_slot_leaves_an_open_missing_issue_for_it_untouched(dgw, gh):
    seed_success(gh, SUITE, 100)
    run_watch(dgw, gh, AFTER)
    issue = gh.only(VISUAL, "missing-schedule")
    gh.created[VISUAL] = SLOT + 10 * HOUR
    gh.writes.clear()
    run_watch(dgw, gh, AFTER + HOUR)
    assert gh.writes == []
    assert gh.issue(issue["number"])["state"] == "open"


def test_reconcile_reads_each_watched_workflow_object_once(dgw, gh):
    seed_success(gh, SUITE, 100)
    seed_success(gh, VISUAL, 900)
    run_watch(dgw, gh, AFTER)
    fetched = Counter(p for m, p, _, _ in gh.requests if m == "GET" and re.fullmatch(rf"{PREFIX}/actions/workflows/[^/]+", p))
    assert fetched == {f"{PREFIX}/actions/workflows/{SUITE}": 1, f"{PREFIX}/actions/workflows/{VISUAL}": 1}


@pytest.mark.parametrize("fault", ["404", "502", "malformed"])
def test_an_unreadable_workflow_object_is_unavailable_never_healthy(dgw, gh, fault):
    seed_failure(gh, SUITE, 150)
    seed_failure(gh, VISUAL, 250)
    run_watch(dgw, gh, AFTER)
    failing = gh.only(VISUAL, "failure")
    good = seed_success(gh, VISUAL, 260, SLOT + 4 * HOUR, event="workflow_dispatch")
    newer = seed_failure(gh, SUITE, 160, SLOT + 5 * HOUR, event="workflow_dispatch")
    gh.faults[f"/actions/workflows/{VISUAL}$"] = fault
    gh.writes.clear()
    report = run_watch(dgw, gh, AFTER + HOUR, event=delivered(good))
    assert set(report.unavailable) == {VISUAL}
    assert gh.issue(failing["number"])["state"] == "open"  # the compare recovery is not applied
    assert not [x for x in gh.writes if VISUAL in json.dumps(x) or NAMES[VISUAL] in json.dumps(x)]
    assert not [x for x in gh.writes if x[1] == f"/issues/{failing['number']}" or x[1].startswith(f"/issues/{failing['number']}/")]
    assert f"evidence={newer['id']}.1" in gh.only(SUITE, "failure")["body"]  # the suite is still tracked


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


JOBS_DEGRADED = {
    "502": ("fault", "502"),
    "malformed": ("fault", "malformed"),
    "timeout": ("fault", "slow"),
    "other-attempt": ("field", ("run_attempt", 9)),
    "other-head": ("field", ("head_sha", "f" * 40)),
    "other-run": ("field", ("run_id", 999)),
}


def degrade_jobs(gh, r, case):
    """Make the jobs of `r` unreadable the way JOBS_DEGRADED[case] says."""
    how, what = JOBS_DEGRADED[case]
    if how == "fault":
        gh.faults[f"/actions/runs/{r['id']}/attempts/{r['run_attempt']}/jobs"] = what
        return
    field, value = what
    listed = gh.jobs[(r["id"], r["run_attempt"])]
    listed[-1] = {**listed[-1], field: value}


@pytest.mark.parametrize("file", [SUITE, VISUAL])
@pytest.mark.parametrize("case", list(JOBS_DEGRADED))
def test_a_failure_whose_jobs_cannot_be_read_still_opens_its_issue(dgw, gh, file, case):
    other = VISUAL if file == SUITE else SUITE
    seed_success(gh, other, 900)
    bad = seed_failure(gh, file, 150)
    degrade_jobs(gh, bad, case)
    report = run_watch(dgw, gh, AFTER, event=delivered(bad), timeout=1.0 if case == "timeout" else 5.0)
    assert set(report.unavailable) == set()
    body = gh.only(file, "failure")["body"]
    assert "job details unavailable" in body.lower()
    for fragment in (str(bad["id"]), bad["head_sha"], "failure", "Status: UNRESOLVED"):
        assert fragment in body, fragment
    if file == SUITE:  # nothing is reported from jobs that could not be trusted
        assert FAILED_JOB not in body and FAILED_STEP not in body


@pytest.mark.parametrize("case", ["502", "other-head"])
def test_a_newer_failure_with_unreadable_jobs_still_updates_the_issue(dgw, gh, case):
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150)
    run_watch(dgw, gh, AFTER)
    number = gh.only(SUITE, "failure")["number"]
    newer = seed_failure(gh, SUITE, 160, SLOT + 3 * HOUR, event="workflow_dispatch")
    degrade_jobs(gh, newer, case)
    report = run_watch(dgw, gh, AFTER + HOUR, event=delivered(newer))
    assert set(report.unavailable) == set()
    issue = gh.only(SUITE, "failure")
    assert issue["number"] == number
    assert "evidence=160.1" in issue["body"]
    assert "job details unavailable" in issue["body"].lower()


def test_unreadable_jobs_of_a_newer_success_do_not_close_a_failure_whose_jobs_also_failed(dgw, gh):
    seed_success(gh, VISUAL, 900)
    bad = seed_failure(gh, SUITE, 150)
    degrade_jobs(gh, bad, "502")
    run_watch(dgw, gh, AFTER)
    number = gh.only(SUITE, "failure")["number"]
    good = seed_success(gh, SUITE, 160, SLOT + 3 * HOUR, event="workflow_dispatch")
    degrade_jobs(gh, good, "502")
    gh.writes.clear()
    report = run_watch(dgw, gh, AFTER + HOUR, event=delivered(good))
    assert set(report.unavailable) == {SUITE}
    assert gh.writes == []
    assert gh.issue(number)["state"] == "open"


def test_every_issue_body_tells_humans_not_to_edit_the_marker(dgw, gh):
    seed_failure(gh, SUITE, 150, PREV + 5 * MINUTE)  # prior-week failure; visual never ran
    run_watch(dgw, gh, AFTER)  # creates: suite failure, suite missing, visual missing
    seed_failure(gh, SUITE, 160, SLOT + 3 * HOUR, event="workflow_dispatch")
    run_watch(dgw, gh, AFTER + HOUR)  # updates the suite failure issue
    run_watch(dgw, gh, SLOT + 7 * DAY + 21 * HOUR)  # moves both missing issues to the next slot
    bodies = [body["body"] for method, path, body in gh.writes if body and "body" in body and (
        (method == "POST" and path == "/issues") or (method == "PATCH" and re.fullmatch(r"/issues/\d+", path))
    )]
    assert len(bodies) >= 6, bodies
    for text in bodies:
        assert "<!-- deep-gate-watch v1 " in text
        visible = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        assert re.search(r"Deep Gate Watch[^\n]*do not edit|do not edit[^\n]*Deep Gate Watch", visible, re.IGNORECASE), text


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


@pytest.mark.parametrize("fault", ["502", "malformed"])
def test_cli_exits_two_when_a_success_runs_jobs_are_unreadable(dgw, gh, tmp_path, fault):
    """Relocated from the `jobs-502` / `jobs-malformed` arms above: unreadable jobs still
    mean unavailable for a SUCCESS, which could otherwise close an issue unproven."""
    seed_failure(gh, SUITE, 150)
    seed_failure(gh, VISUAL, 250)
    run_watch(dgw, gh, AFTER)
    seed_success(gh, SUITE, 160, SLOT + 3 * HOUR, event="workflow_dispatch")
    seed_success(gh, VISUAL, 260, SLOT + 3 * HOUR, event="workflow_dispatch")
    gh.faults["/jobs"] = fault
    gh.writes.clear()
    proc, summary = watch_cli(gh, tmp_path, event=SCHEDULE_EVENT)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert gh.writes == []
    assert "unavailable" in summary.lower()
    assert len(gh.find(SUITE, "failure")) == len(gh.find(VISUAL, "failure")) == 1


@pytest.mark.parametrize("fault", ["502", "malformed"])
def test_cli_exits_zero_and_still_reports_a_failure_whose_jobs_are_unreadable(dgw, gh, tmp_path, fault):
    seed_failure(gh, SUITE, 150)
    seed_failure(gh, VISUAL, 250)
    gh.faults["/jobs"] = fault
    proc, summary = watch_cli(gh, tmp_path, event=SCHEDULE_EVENT)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    for file in (SUITE, VISUAL):
        assert "job details unavailable" in gh.only(file, "failure")["body"].lower()
    assert "job details unavailable" in summary.lower()


@pytest.mark.parametrize("fault", ["404", "502", "malformed"])
def test_cli_exits_two_when_a_workflow_object_is_unreadable(dgw, gh, tmp_path, fault):
    seed_failure(gh, SUITE, 150)
    seed_failure(gh, VISUAL, 250)
    for file in (SUITE, VISUAL):
        gh.faults[f"/actions/workflows/{file}$"] = fault
    proc, summary = watch_cli(gh, tmp_path, event=SCHEDULE_EVENT)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert gh.writes == []
    assert "unavailable" in summary.lower()


def test_cli_exits_zero_for_a_workflow_merged_after_the_slot(dgw, gh, tmp_path):
    seed_success(gh, SUITE, 100)
    gh.created[VISUAL] = SLOT + 10 * HOUR
    proc, _ = watch_cli(gh, tmp_path, event=SCHEDULE_EVENT)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert gh.writes == []


def test_cli_exits_one_on_an_unreadable_event_payload(dgw, gh, tmp_path):
    seed_success(gh, VISUAL, 900)
    seed_failure(gh, SUITE, 150)
    proc, _ = watch_cli(gh, tmp_path, event="{not json")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert gh.writes == []


# ---------------------------------------------------------- A3: four functional shards


def assert_a3_shard_contract(raw):
    """Membership is enforced here; GitHub exposes one aggregate matrix result."""
    block = strip_comments(raw)
    assert job_name(block) == "E2E Functional Shard ${{ matrix.shard }}/4"
    assert needs_list(block) == ["frontend-build"]
    matrix = re.findall(r"^        shard: \[([^\]]*)\]$", block, re.MULTILINE)
    assert len(matrix) == 1
    assert [int(value.strip()) for value in matrix[0].split(",")] == [1, 2, 3, 4]
    assert re.search(r"^      fail-fast: false$", block, re.MULTILINE)
    assert not re.search(r"^        (include|exclude):", block, re.MULTILINE)
    assert not re.search(r"^    (if|continue-on-error):", block, re.MULTILINE)
    by_name = dict(steps(block))
    run = by_name["Run functional specs (shard ${{ matrix.shard }}/4)"]
    assert step_condition(run) is None
    assert "continue-on-error" not in run
    expected = (
        "npx playwright test --project=chromium --shard=${{ matrix.shard }}/4 "
        + " ".join(sorted(launcher_array("RequiredSpecs")))
    )
    assert command(run) == expected
    report = by_name["Upload functional JUnit"]
    assert step_condition(report) == "always()"
    assert "continue-on-error" not in report
    assert re.search(r"uses: actions/upload-artifact@[0-9a-f]{40}\b", report)
    for line in (
        "name: playwright-functional-report-shard-${{ matrix.shard }}-of-4",
        "path: artifacts/playwright/junit.xml",
        "if-no-files-found: error",
        "retention-days: 7",
    ):
        assert re.search(rf"^        {re.escape(line)}$", report, re.MULTILINE), line


def test_a3_four_shards_preserve_the_required_selection_and_executed_reports():
    assert_a3_shard_contract(ci_job("e2e-functional-shard"))


@pytest.mark.parametrize("missing", (1, 2, 3, 4))
def test_a3_removing_any_shard_fails_the_required_workflow_contract(missing):
    block = ci_job("e2e-functional-shard")
    reduced = ", ".join(str(value) for value in (1, 2, 3, 4) if value != missing)
    mutated = block.replace("shard: [1, 2, 3, 4]", f"shard: [{reduced}]")
    assert mutated != block
    with pytest.raises(AssertionError):
        assert_a3_shard_contract(mutated)


@pytest.mark.parametrize(
    "before,after",
    (
        ("shard: [1, 2, 3, 4]", "shard: [1, 2, 3, 3]"),
        ("fail-fast: false", "fail-fast: true"),
        ("        shard: [1, 2, 3, 4]", "        shard: [1, 2, 3, 4]\n        exclude: []"),
        ("        shard: [1, 2, 3, 4]", "        shard: [1, 2, 3, 4]\n        include: []"),
        ("    needs: frontend-build", "    needs: frontend-build\n    continue-on-error: true"),
        ("    needs: frontend-build", "    needs: frontend-build\n    if: false"),
        ("--shard=${{ matrix.shard }}/4", "--shard=${{ matrix.shard }}/2"),
        ("      run: |\n        npx playwright", "      if: false\n      run: |\n        npx playwright"),
        ("e2e/workout-plan.spec.ts\n", "e2e/workout-plan.spec.ts || true\n"),
        ("      if: always()\n      uses: actions/upload-artifact", "      if: failure()\n      uses: actions/upload-artifact"),
        ("if-no-files-found: error", "if-no-files-found: warn"),
    ),
)
def test_a3_cannot_soften_or_skip_a_shard_or_its_execution_report(before, after):
    block = ci_job("e2e-functional-shard")
    mutated = block.replace(before, after)
    assert mutated != block
    with pytest.raises(AssertionError):
        assert_a3_shard_contract(mutated)


def test_a3_preserves_the_single_always_running_required_aggregate():
    named = [job_id for job_id, raw in jobs(CI).items() if job_name(raw) == "E2E Functional (Chromium)"]
    assert named == ["e2e-functional"]
    assert "E2E Functional (Chromium)" in REQUIRED_CONTEXTS
    block = strip_comments(ci_job("e2e-functional"))
    assert needs_list(block) == ["e2e-functional-shard"]
    assert re.search(r"^    if: always\(\)$", block, re.MULTILINE)
    assert not re.search(r"^    continue-on-error:", block, re.MULTILINE)
    decision_steps = steps(block)
    assert len(decision_steps) == 1
    name, raw = decision_steps[0]
    assert name == "Require all functional shards to pass"
    assert step_condition(raw) is None
    assert "continue-on-error" not in raw


@pytest.mark.parametrize("result", ("success", "failure", "cancelled", "skipped", "", "SUCCESS"))
def test_a3_actual_aggregate_shell_fails_closed_for_every_non_success_result(result):
    raw = dict(steps(strip_comments(ci_job("e2e-functional"))))["Require all functional shards to pass"]
    script = run_script(raw)
    expression = "${{ needs.e2e-functional-shard.result }}"
    assert script is not None and script.count(expression) == 1
    script = script.replace(expression, result)
    assert "${{" not in script
    proc = subprocess.run(
        [bash_executable(), "--noprofile", "--norc", "-eo", "pipefail", "-c", script],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == (0 if result == "success" else 1), proc.stdout + proc.stderr
    if result != "success":
        assert "::error title=E2E Functional gate::" in proc.stdout


# ------------------------------------------------ G6: fixed, executed selected identities

G6_WINDOWS_FILE = "tests/test_agent_workflow_contracts.py"
G6_SKILL_FAMILY = "test_skill_guard_decides_as_the_senior_developer_allowlist_says"
G6_DESTRUCTIVE_FAMILY = "test_all_effective_destructive_registrations_execute_deny_allow"
G6_WINDOWS = tuple(
    f"{G6_WINDOWS_FILE}::{family}[{parameter}-powershell]"
    for family, parameters in (
        (G6_SKILL_FAMILY, ("handover-0", "verify-and-polish-0", "council-plan-2", "-2")),
        (G6_DESTRUCTIVE_FAMILY, ("default", "bypassPermissions")),
    )
    for parameter in parameters
)
G6_DEPENDENCIES = (
    "tests/test_braces_override_contracts.py::test_installed_braces_preserves_ordinary_glob_behavior",
    "tests/test_braces_override_contracts.py::test_installed_braces_bounds_malicious_nesting[compile]",
    "tests/test_braces_override_contracts.py::test_installed_braces_bounds_malicious_nesting[expand]",
)
G6_GROUPS = {"windows": G6_WINDOWS, "dependencies": G6_DEPENDENCIES}
G6_ALL = [(group, node) for group, nodes in G6_GROUPS.items() for node in nodes]


def g6_junit(tmp_path, cases, name="g6.xml"):
    path = junit(tmp_path, cases, name)
    tree = ET.parse(path)
    for suite in tree.getroot().iter("testsuite"):
        found = suite.findall("testcase")
        suite.set("tests", str(len(found)))
        for attribute, tag in (("skipped", "skipped"), ("failures", "failure"), ("errors", "error")):
            suite.set(attribute, str(sum(case.find(tag) is not None for case in found)))
    tree.write(path, encoding="utf-8")
    return path


def test_g6_expectations_are_the_approved_nine_fixed_node_ids():
    assert selected_report.WINDOWS_NODES == G6_WINDOWS
    assert selected_report.DEPENDENCY_NODES == G6_DEPENDENCIES
    assert len(set((*G6_WINDOWS, *G6_DEPENDENCIES))) == 9


def test_g6_selects_windows_from_both_complete_host_families():
    nodes = [*G6_WINDOWS, *(node.replace("-powershell]", "-pwsh]") for node in G6_WINDOWS)]
    assert selected_report.select_windows(collection(nodes)) == list(G6_WINDOWS)


@pytest.mark.parametrize("missing", G6_WINDOWS)
def test_g6_collection_cannot_hide_removal_of_any_windows_identity(missing):
    with pytest.raises(ValueError, match="missing"):
        selected_report.select_windows(collection([node for node in G6_WINDOWS if node != missing]))


@pytest.mark.parametrize("mutation", ("extra-parameter", "duplicate", "wrong-host", "unapproved-family"))
def test_g6_windows_collection_rejects_unreviewed_membership(mutation):
    nodes = list(G6_WINDOWS)
    if mutation == "extra-parameter":
        nodes.append(G6_WINDOWS[0].replace("handover-0", "new-parameter-0"))
    elif mutation == "duplicate":
        nodes.append(nodes[0])
    elif mutation == "wrong-host":
        nodes[0] = nodes[0].replace("-powershell]", "-pwsh]")
    else:
        nodes.append("tests/test_other.py::test_other[powershell]")
    with pytest.raises(ValueError):
        selected_report.select_windows(collection(nodes))


@pytest.mark.parametrize("group", G6_GROUPS)
@pytest.mark.parametrize("root_tag", ("testsuites", "testsuite"))
def test_g6_verifier_accepts_every_fixed_case_exactly_once(tmp_path, group, root_tag):
    report = g6_junit(tmp_path, [(node, None) for node in G6_GROUPS[group]])
    if root_tag == "testsuite":
        suite = ET.parse(report).getroot().find("testsuite")
        assert suite is not None
        ET.ElementTree(suite).write(report, encoding="utf-8")
    assert selected_report.verify(group, report) == len(G6_GROUPS[group])


def test_g6_core_ignores_unrelated_legitimate_host_skips(tmp_path):
    cases: list[tuple[str, str | None]] = [(node, None) for node in G6_DEPENDENCIES]
    cases.extend((node, "skipped") for node in G6_WINDOWS)
    assert selected_report.verify("dependencies", g6_junit(tmp_path, cases)) == 3


@pytest.mark.parametrize("group,node", G6_ALL)
@pytest.mark.parametrize("mutation", ("remove", "duplicate", "skipped", "failure", "error"))
def test_g6_each_selected_identity_requires_one_executed_pass(tmp_path, group, node, mutation):
    cases = [(identity, None) for identity in G6_GROUPS[group] if identity != node]
    if mutation == "duplicate":
        cases.extend(((node, None), (node, None)))
    elif mutation != "remove":
        cases.append((node, mutation))
    with pytest.raises(ValueError):
        selected_report.verify(group, g6_junit(tmp_path, cases))


@pytest.mark.parametrize("group", G6_GROUPS)
def test_g6_both_complete_function_families_reject_new_parameters(tmp_path, group):
    for family_node in (G6_GROUPS[group][0], G6_GROUPS[group][-1]):
        extra = family_node.partition("[")[0] + "[unreviewed-parameter-powershell]"
        cases = [(node, None) for node in (*G6_GROUPS[group], extra)]
        with pytest.raises(ValueError, match="unexpected"):
            selected_report.verify(group, g6_junit(tmp_path, cases))


@pytest.mark.parametrize("extra", ("pwsh", "unrelated"))
def test_g6_windows_report_rejects_extra_cases_even_outside_approved_families(tmp_path, extra):
    node = G6_WINDOWS[0].replace("-powershell]", "-pwsh]") if extra == "pwsh" else "tests/test_other.py::test_other"
    cases = [(identity, None) for identity in (*G6_WINDOWS, node)]
    with pytest.raises(ValueError, match="unexpected"):
        selected_report.verify("windows", g6_junit(tmp_path, cases))


@pytest.mark.parametrize("group", G6_GROUPS)
@pytest.mark.parametrize("problem", ("absent", "empty", "malformed", "no-cases", "wrong-root", "misplaced-case",
                                    "no-classname", "no-name", "tests", "skipped", "failures", "errors", "root-count", "multiple-outcomes",
                                    "nested-suite", "unknown-case-child", "unknown-root-child"))
def test_g6_unverifiable_junit_fails_closed(tmp_path, group, problem):
    path = tmp_path / "bad.xml"
    if problem in {"empty", "malformed", "no-cases"}:
        path.write_text({"empty": "", "malformed": "<testsuites>", "no-cases": "<testsuites/>"}[problem], encoding="utf-8")
    elif problem != "absent":
        path = g6_junit(tmp_path, [(node, None) for node in G6_GROUPS[group]])
        tree = ET.parse(path)
        root = tree.getroot()
        suite = root.find("testsuite")
        first = root.find(".//testcase")
        assert suite is not None and first is not None
        if problem == "wrong-root":
            root.tag = "arbitrary"
        elif problem == "misplaced-case":
            suite.remove(first)
            root.append(first)
        elif problem.startswith("no-"):
            del first.attrib[problem.removeprefix("no-")]
        elif problem == "root-count":
            root.set("tests", "9999")
        elif problem == "multiple-outcomes":
            ET.SubElement(first, "failure")
            ET.SubElement(first, "error")
        elif problem == "nested-suite":
            root.remove(suite)
            ET.SubElement(root, "testsuite").append(suite)
        elif problem == "unknown-case-child":
            ET.SubElement(first, "not-run")
        elif problem == "unknown-root-child":
            ET.SubElement(root, "not-a-suite")
        else:
            suite.set(problem, "9999")
        tree.write(path, encoding="utf-8")
    with pytest.raises(ValueError):
        selected_report.verify(group, path)


@pytest.mark.parametrize("group", G6_GROUPS)
def test_g6_verifier_cli_preserves_the_executed_outcome_verdict(tmp_path, group):
    for outcome, expected in ((None, 0), ("skipped", 1), ("failure", 1)):
        path = g6_junit(tmp_path, [(node, outcome) for node in G6_GROUPS[group]])
        result = subprocess.run([sys.executable, str(ROOT / "scripts/ci_selected_report.py"), "verify", group, str(path)],
                                capture_output=True, text=True, check=False)
        assert result.returncode == expected, result.stdout + result.stderr
        assert ("::error" in result.stderr) == bool(expected)


@pytest.mark.parametrize("group", G6_GROUPS)
def test_g6_preflight_rejects_a_missing_required_executable(monkeypatch, tmp_path, group):
    (tmp_path / "node_modules").mkdir()
    monkeypatch.setattr(selected_report, "ROOT", tmp_path)
    monkeypatch.setattr(selected_report.sys, "platform", "win32")
    monkeypatch.setattr(selected_report.shutil, "which", lambda _: None)
    with pytest.raises(ValueError, match="required"):
        selected_report.preflight(group)


def test_g6_preflight_rejects_linux_even_when_a_powershell_named_program_exists(monkeypatch):
    monkeypatch.setattr(selected_report.sys, "platform", "linux")
    monkeypatch.setattr(selected_report.shutil, "which", lambda _: "fake-powershell")
    with pytest.raises(ValueError, match="native Windows"):
        selected_report.preflight("windows")


def test_g6_preflight_rejects_absent_npm_tree_even_when_node_exists(monkeypatch, tmp_path):
    monkeypatch.setattr(selected_report, "ROOT", tmp_path)
    monkeypatch.setattr(selected_report.shutil, "which", lambda _: "fake-node")
    with pytest.raises(ValueError, match="npm dependencies"):
        selected_report.preflight("dependencies")


@pytest.mark.parametrize("group", G6_GROUPS)
@pytest.mark.parametrize("outcome", ("success", "failure", "unlaunchable", "timeout"))
def test_g6_preflight_requires_the_actual_host_or_installed_resolution_to_run(monkeypatch, tmp_path, group, outcome):
    (tmp_path / "node_modules").mkdir()
    monkeypatch.setattr(selected_report, "ROOT", tmp_path)
    monkeypatch.setattr(selected_report.sys, "platform", "win32")
    monkeypatch.setattr(selected_report.shutil, "which", lambda name: f"fake-{name}")
    calls = []

    def run(command, **kwargs):
        calls.append((command, kwargs))
        if outcome == "unlaunchable":
            raise OSError("prerequisite unavailable")
        if outcome == "timeout":
            raise subprocess.TimeoutExpired(command, 30)
        return subprocess.CompletedProcess(command, 0 if outcome == "success" else 1, "", "")

    monkeypatch.setattr(selected_report.subprocess, "run", run)
    if outcome == "success":
        selected_report.preflight(group)
    else:
        with pytest.raises(ValueError, match="prerequisite"):
            selected_report.preflight(group)
    command_line, options = calls[0]
    assert options["cwd"] == tmp_path and options["check"] is False
    if group == "windows":
        assert "PSEdition" in command_line[-1] and "Desktop" in command_line[-1]
    else:
        assert "micromatch/package.json" in command_line[-1] and "r('braces')" in command_line[-1]


def test_g6_preflight_and_missing_report_cli_fail_instead_of_succeeding(monkeypatch, tmp_path):
    monkeypatch.setattr(selected_report.shutil, "which", lambda _: None)
    assert selected_report.main(["preflight", "dependencies"]) == 1
    assert selected_report.main(["verify", "windows", str(tmp_path / "missing.xml")]) == 1


def test_g6_windows_route_collects_whole_families_and_preserves_pytest_exit():
    block = strip_comments(ci_job("workflow-contracts-windows"))
    assert job_name(block) == "Workflow Contracts (Windows PowerShell)"
    assert re.search(r"^    runs-on: windows-latest$", block, re.MULTILINE)
    assert not re.search(r"^    (if|continue-on-error|needs|strategy):", block, re.MULTILINE)
    by_name = dict(steps(block))
    assert command(by_name["Require native Windows PowerShell"]) == "python scripts/ci_selected_report.py preflight windows"
    select = by_name["Collect and select the six Windows identities"]
    script = run_script(select)
    assert script is not None
    collects = f"python -m pytest --collect-only -q {G6_WINDOWS_FILE}::{G6_SKILL_FAMILY} {G6_WINDOWS_FILE}::{G6_DESTRUCTIVE_FAMILY}"
    assert collects + " > artifacts/workflow-contracts-windows/collected.txt" in script
    assert "python scripts/ci_selected_report.py select-windows artifacts/workflow-contracts-windows/collected.txt > artifacts/workflow-contracts-windows/selected.txt" in script
    assert script.count("if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }") == 2
    run = by_name["Run the selected Windows cases"]
    assert command(run) == "python -m pytest '@artifacts/workflow-contracts-windows/selected.txt' -v --tb=short -o junit_family=xunit2 --junitxml=artifacts/workflow-contracts-windows/junit.xml"
    for name in ("Require native Windows PowerShell", "Collect and select the six Windows identities", "Run the selected Windows cases"):
        assert step_condition(by_name[name]) is None
        assert "continue-on-error" not in by_name[name]
    names = list(by_name)
    assert names.index("Require native Windows PowerShell") < names.index("Collect and select the six Windows identities") < names.index("Run the selected Windows cases")


@pytest.mark.parametrize("job,step,expected", (
    ("pytest-core", "Require installed dependency cases to execute and pass", "dependencies artifacts/pytest/junit.xml"),
    ("workflow-contracts-windows", "Require all six Windows cases to execute and pass", "windows artifacts/workflow-contracts-windows/junit.xml"),
))
def test_g6_both_verifiers_run_even_after_prerequisite_or_pytest_failure(job, step, expected):
    by_name = dict(steps(strip_comments(ci_job(job))))
    verify_step = by_name[step]
    assert step_condition(verify_step) == "always()"
    assert "continue-on-error" not in verify_step
    assert command(verify_step) == f"python scripts/ci_selected_report.py verify {expected}"
    run = "Run pytest with coverage" if job == "pytest-core" else "Run the selected Windows cases"
    assert list(by_name).index(run) < list(by_name).index(step)


def test_g6_core_installs_npm_and_checks_prerequisites_before_existing_full_suite():
    by_name = dict(steps(strip_comments(ci_job("pytest-core"))))
    install = "Install npm dependencies for enforced dependency cases"
    preflight = "Require installed dependency prerequisites"
    assert command(by_name[install]) == "npm ci"
    assert command(by_name[preflight]) == "python scripts/ci_selected_report.py preflight dependencies"
    for name in (install, preflight):
        assert step_condition(by_name[name]) is None and "continue-on-error" not in by_name[name]
    names = list(by_name)
    assert names.index(install) < names.index(preflight) < names.index("Run pytest with coverage")


@pytest.mark.parametrize("job,step,artifact", (
    ("pytest-core", "Upload pytest JUnit XML", "pytest-junit"),
    ("workflow-contracts-windows", "Upload Windows workflow-contract reports", "workflow-contracts-windows-junit"),
))
def test_g6_execution_reports_are_always_retained_and_required(job, step, artifact):
    upload = dict(steps(strip_comments(ci_job(job))))[step]
    assert step_condition(upload) == "always()" and "continue-on-error" not in upload
    assert f"name: {artifact}" in upload and "if-no-files-found: error" in upload
    assert "actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9" in upload


def test_g6_fan_in_requires_the_narrow_leg_without_promoting_operation_a():
    assert "workflow-contracts-windows" in fan_in_gate("run-tests")
    assert "worktree-windows" not in fan_in_gate("run-tests")
    assert needs_of(strip_comments(ci_job("run-tests"))) == list(FAN_IN_DEPENDENCIES)
