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
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

import pytest

from scripts.ci_executed_report import (
    junit_identity,
    read_collection,
    select_shard,
    verify,
    verify_union,
)
from scripts.ci_fan_in import problems
from scripts.release_gate import REQUIRED_CONTEXTS
from tests.test_release_workflow_contracts import (
    CI,
    jobs,
    job_name,
    steps,
    strip_comments,
)
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
    assert command == (
        "python -m pytest -n 4 --dist load @artifacts/guard/shard.txt -v --tb=short "
        "--junitxml=artifacts/guard/junit.xml"
    )
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
