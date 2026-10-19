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
import shlex
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter

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
