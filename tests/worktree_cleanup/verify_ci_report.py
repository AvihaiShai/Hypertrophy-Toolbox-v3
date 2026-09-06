"""Require executed, successful Operation A coverage on both Windows hosts."""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET

MODULES = (
    "tests.test_worktree_environment_preflight",
    "tests.test_worktree_lifecycle",
    "tests.test_worktree_snapshot",
)
HOSTS = ("powershell", "pwsh")


def verify(root: ET.Element) -> dict[str, int]:
    cases = list(root.iter("testcase"))
    if not cases or any(
        case.find(tag) is not None for case in cases
        for tag in ("skipped", "failure", "error")
    ):
        raise ValueError("Operation A requires a nonempty report with no skips, failures or errors")
    counts = {}
    for module in MODULES:
        by_host = {host: set() for host in HOSTS}
        for case in cases:
            if case.get("classname") != module:
                continue
            name = case.get("name", "")
            for host in HOSTS:
                if re.search(rf"[\[-]{host}(?=[\]-])", name):
                    by_host[host].add(re.sub(rf"(?<=[\[-]){host}(?=[\]-])", "HOST", name))
        if not by_host["powershell"] or by_host["powershell"] != by_host["pwsh"]:
            raise ValueError(f"{module}: missing or unequal PowerShell host coverage")
        counts[module] = len(by_host["pwsh"])
    return counts


if __name__ == "__main__":
    print(verify(ET.parse(sys.argv[1]).getroot()))
