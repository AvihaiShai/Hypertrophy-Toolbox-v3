"""G6: require the nine approved cases to execute in their enforced destinations.

The expectations are fixed, never inferred from collection. Windows collects both
complete host families before selecting PowerShell; core checks both complete
installed-braces families while allowing unrelated cases and their legitimate skips.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

if __package__:
    from .ci_executed_report import executed_cases, junit_identity, read_collection
else:
    from ci_executed_report import executed_cases, junit_identity, read_collection

ROOT = Path(__file__).resolve().parents[1]
WINDOWS_NODES = (
    "tests/test_agent_workflow_contracts.py::test_skill_guard_decides_as_the_senior_developer_allowlist_says[handover-0-powershell]",
    "tests/test_agent_workflow_contracts.py::test_skill_guard_decides_as_the_senior_developer_allowlist_says[verify-and-polish-0-powershell]",
    "tests/test_agent_workflow_contracts.py::test_skill_guard_decides_as_the_senior_developer_allowlist_says[council-plan-2-powershell]",
    "tests/test_agent_workflow_contracts.py::test_skill_guard_decides_as_the_senior_developer_allowlist_says[-2-powershell]",
    "tests/test_agent_workflow_contracts.py::test_all_effective_destructive_registrations_execute_deny_allow[default-powershell]",
    "tests/test_agent_workflow_contracts.py::test_all_effective_destructive_registrations_execute_deny_allow[bypassPermissions-powershell]",
)
DEPENDENCY_NODES = (
    "tests/test_braces_override_contracts.py::test_installed_braces_preserves_ordinary_glob_behavior",
    "tests/test_braces_override_contracts.py::test_installed_braces_bounds_malicious_nesting[compile]",
    "tests/test_braces_override_contracts.py::test_installed_braces_bounds_malicious_nesting[expand]",
)


def require_exact(expected_nodes: tuple[str, ...], cases: list[tuple[str, str]]) -> int:
    expected = Counter(junit_identity(node) for node in expected_nodes)
    seen = Counter(identity for identity, _ in cases)
    problems = {
        "missing": sorted(set(expected) - set(seen)),
        "unexpected": sorted(set(seen) - set(expected)),
        "duplicated": sorted(identity for identity, count in seen.items() if count != 1),
        "not passed": [f"{identity} ({outcome})" for identity, outcome in cases if outcome != "passed"],
    }
    found = {kind: values for kind, values in problems.items() if values}
    if found:
        raise ValueError(f"selected identities did not execute exactly once and pass: {found}")
    return len(cases)


def select_windows(collected: str) -> list[str]:
    nodes = read_collection(collected)
    families = {node.partition("[")[0] for node in WINDOWS_NODES}
    if any(node.partition("[")[0] not in families for node in nodes):
        raise ValueError("Windows collection contains an unapproved function family")
    selected = [node for node in nodes if node.endswith("-powershell]")]
    require_exact(WINDOWS_NODES, [(junit_identity(node), "passed") for node in selected])
    return selected


def validated_cases(report: Path) -> list[tuple[str, str]]:
    try:
        root = ET.parse(report).getroot()
    except (OSError, ET.ParseError) as exc:
        raise ValueError(f"{report}: unreadable JUnit report ({exc})") from None
    if root.tag not in {"testsuites", "testsuite"}:
        raise ValueError(f"{report}: invalid JUnit root {root.tag!r}")
    suites = list(root) if root.tag == "testsuites" else [root]
    if any(suite.tag != "testsuite" or suite.find(".//testsuite") is not None for suite in suites):
        raise ValueError(f"{report}: malformed testsuite nesting")
    all_cases = list(root.iter("testcase"))
    direct_cases = [case for suite in suites for case in suite.findall("testcase")]
    if not suites or not all_cases or direct_cases != all_cases:
        raise ValueError(f"{report}: empty or malformed testsuite/testcase structure")
    totals = {"tests": 0, "skipped": 0, "failures": 0, "errors": 0}
    for suite in suites:
        cases = suite.findall("testcase")
        observed = {
            "tests": len(cases),
            "skipped": sum(case.find("skipped") is not None for case in cases),
            "failures": sum(case.find("failure") is not None for case in cases),
            "errors": sum(case.find("error") is not None for case in cases),
        }
        for case in cases:
            if any(child.tag not in {"properties", "system-out", "system-err", "skipped", "failure", "error"} for child in case):
                raise ValueError(f"{report}: testcase has an unknown outcome or child")
            if sum(len(case.findall(tag)) for tag in ("skipped", "failure", "error")) > 1:
                raise ValueError(f"{report}: testcase has multiple outcomes")
        for key, count in observed.items():
            declared = suite.get(key, "")
            if not declared.isdecimal() or int(declared) != count:
                raise ValueError(f"{report}: testsuite {key} count disagrees with testcases")
            totals[key] += count
    if root.tag == "testsuites":
        for key, count in totals.items():
            declared = root.get(key)
            if declared is not None and (not declared.isdecimal() or int(declared) != count):
                raise ValueError(f"{report}: testsuites {key} count disagrees with testcases")
    return executed_cases(report)


def verify(group: str, report: Path) -> int:
    cases = validated_cases(report)
    if group == "windows":
        return require_exact(WINDOWS_NODES, cases)
    if group != "dependencies":
        raise ValueError(f"unknown selected group: {group}")
    families = {junit_identity(node).partition("[")[0] for node in DEPENDENCY_NODES}
    # Match whole function families, not just the three expected parameter IDs.
    # A newly added parameter must fail until its expectation is deliberately reviewed.
    selected = [(identity, outcome) for identity, outcome in cases if identity.partition("[")[0] in families]
    return require_exact(DEPENDENCY_NODES, selected)


def preflight(group: str) -> None:
    if group == "windows":
        host = shutil.which("powershell")
        if sys.platform != "win32" or host is None:
            raise ValueError("native Windows and Windows PowerShell are required")
        command = [host, "-NoProfile", "-NonInteractive", "-Command",
                   "if ($PSVersionTable.PSEdition -ne 'Desktop') { exit 1 }; $PSVersionTable.PSVersion.ToString()"]
    elif group == "dependencies":
        node = shutil.which("node")
        if not (ROOT / "node_modules").is_dir() or node is None:
            raise ValueError("installed npm dependencies and Node are required")
        command = [node, "-e", "const {createRequire}=require('node:module');"
                   "const r=createRequire(require.resolve('micromatch/package.json'));r('braces');"]
    else:
        raise ValueError(f"unknown selected group: {group}")
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError(f"{group} prerequisite could not run: {exc}") from None
    if result.returncode:
        raise ValueError(f"{group} prerequisite failed ({result.returncode}): {result.stdout}{result.stderr}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("preflight")
    check.add_argument("group", choices=("windows", "dependencies"))
    select = commands.add_parser("select-windows")
    select.add_argument("collected", type=Path)
    report = commands.add_parser("verify")
    report.add_argument("group", choices=("windows", "dependencies"))
    report.add_argument("report", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "preflight":
            preflight(args.group)
            print(f"{args.group}: prerequisites available")
        elif args.command == "select-windows":
            for node in select_windows(args.collected.read_text(encoding="utf-8-sig")):
                print(node)
        else:
            count = verify(args.group, args.report)
            print(f"{args.group}: all {count} fixed identities executed once and passed")
    except (OSError, ValueError) as exc:
        print(f"::error title=G6 selected execution::{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
