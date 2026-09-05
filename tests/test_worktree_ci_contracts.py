"""Keep native Windows coverage executed and portable Linux coverage selected."""
import importlib
import re
import sys
import xml.etree.ElementTree as ET

import pytest

from tests.worktree_cleanup.support import ROOT
from tests.worktree_cleanup.verify_ci_report import HOSTS, MODULES, verify


def report():
    root = ET.Element("testsuites")
    suite = ET.SubElement(root, "testsuite")
    for module in MODULES:
        for host in HOSTS:
            ET.SubElement(suite, "testcase", classname=module, name=f"test_example[case-{host}]")
    ET.SubElement(suite, "testcase", classname=MODULES[-1], name="test_portable_snapshot")
    return root


def test_ci_report_accepts_both_hosts_and_portable_tests():
    assert verify(report()) == dict.fromkeys(MODULES, 1)


@pytest.mark.parametrize("damage", ("empty", "skipped", "failure", "error", "module", "host", "unequal"))
def test_ci_report_rejects_absent_or_unexecuted_coverage(damage):
    root = report()
    suite = root.find("testsuite")
    assert suite is not None
    if damage == "empty":
        suite.clear()
    elif damage in ("skipped", "failure", "error"):
        ET.SubElement(suite[0], damage)
    elif damage == "module":
        for case in list(suite)[:2]:
            suite.remove(case)
    elif damage == "host":
        suite.remove(suite[0])
    else:
        suite[0].set("name", "test_different[powershell]")
    with pytest.raises(ValueError):
        verify(root)


def test_windows_job_runs_all_operation_a_modules_and_checks_execution():
    source = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    job = source.split("\n  worktree-windows:\n", 1)[1].split("\n  test:\n", 1)[0]
    assert "runs-on: windows-2022" in job
    assert "continue-on-error" not in job
    assert "@('powershell', 'pwsh')" in job
    assert "Get-Command $hostName -ErrorAction Stop" in job
    for variable in ("TEMP", "TMP", "TMPDIR"):
        assert f"{variable}: ${{{{ runner.temp }}}}" in job
    command = next(line.strip() for line in job.splitlines() if "python -m pytest " in line)
    assert command.split()[3:6] == [module.replace(".", "/") + ".py" for module in MODULES]
    assert not re.search(r"(?:^| )(-k|-m|--ignore|--deselect)(?:[ =]|$)", command.split("pytest ", 1)[1])
    assert "--junitxml=artifacts/pytest/worktree-windows.xml" in command
    assert "if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }" in job
    assert "if: always()\n      run: python -m tests.worktree_cleanup.verify_ci_report artifacts/pytest/worktree-windows.xml" in job
    assert "name: operation-a-windows-junit" in job and "if-no-files-found: error" in job
    linux = re.split(r"\n  [\w-]+:\n", source.split("\n  test:\n", 1)[1], maxsplit=1)[0]
    assert "runs-on: ubuntu-latest" in linux
    assert "pytest tests/ -v --tb=short" in linux


@pytest.mark.parametrize("module_name", MODULES)
def test_platform_marks_preserve_portable_tests(module_name):
    module = importlib.import_module(module_name)
    module_marks = getattr(module, "pytestmark", [])
    if not isinstance(module_marks, list):
        module_marks = [module_marks]
    native_preflight = {
        "test_absent_scopes_valid_identity_passes_without_creating_runtime",
        "test_unverified_runtime_or_database_root_refuses",
        "test_dangling_reparse_ancestor_is_not_treated_as_verified_absence",
    }
    for name, function in vars(module).items():
        if not name.startswith("test_") or not callable(function):
            continue
        marks = module_marks + list(getattr(function, "pytestmark", []))
        skips = [mark for mark in marks if mark.name == "skipif"]
        native = module_name.endswith("lifecycle") or name in native_preflight or (
            module_name.endswith("snapshot") and "host" in function.__code__.co_varnames[:function.__code__.co_argcount]
        )
        assert bool(skips) == native, name
        if native:
            assert len(skips) == 1 and skips[0].args == (sys.platform != "win32",), name
