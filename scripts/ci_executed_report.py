"""Prove that pytest EXECUTED exactly the identities it collected.

Collection is not execution. An identity counts only when a JUnit report records
it exactly once with no ``skipped``/``failure``/``error`` child. Missing,
unexpected and duplicated identities, an empty or malformed report and an
unreadable collection all fail. CI uses this for the guard-hook tests, which run
outside ``pytest-core``; ``tests/test_ci_expansion_contracts.py`` pins it.

    pytest --collect-only -q <paths> > collected.txt
    python scripts/ci_executed_report.py shard collected.txt --index 1 --total 2 > shard.txt
    python scripts/ci_executed_report.py verify collected.txt report.xml [--index 1 --total 2]
    python scripts/ci_executed_report.py union --shards 2 --collected c1.txt c2.txt --reports r1.xml r2.xml
"""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

OUTCOMES = ("skipped", "failure", "error")
_SUMMARY = re.compile(r"^(\d+) tests? collected\b")


def junit_identity(node_id: str) -> str:
    """``tests/a.py::Cls::test_x[p]`` -> ``tests.a.Cls::test_x[p]``.

    Parameter ids may themselves contain ``::`` (``[Environment]::Set...``), so
    only the part before the first ``[`` is split.
    """
    head, bracket, params = node_id.partition("[")
    parts = head.split("::")
    if len(parts) < 2 or not parts[0].endswith(".py") or not all(parts):
        raise ValueError(f"not a pytest node id: {node_id!r}")
    classname = ".".join([parts[0][:-3].replace("/", "."), *parts[1:-1]])
    return f"{classname}::{parts[-1]}{bracket}{params}"


def read_collection(text: str) -> list[str]:
    """Node ids from ``pytest --collect-only -q``, checked against its own count."""
    lines = text.splitlines()
    try:
        end = lines.index("")
    except ValueError:
        raise ValueError("collection output has no node-id block") from None
    node_ids = lines[:end]
    summary = next((m for line in lines[end:] if (m := _SUMMARY.match(line))), None)
    if summary is None:
        raise ValueError("collection output has no 'N tests collected' summary")
    if not node_ids or len(node_ids) != int(summary.group(1)):
        raise ValueError(f"collected {len(node_ids)} node ids but pytest reported {summary.group(1)}")
    for node_id in node_ids:
        junit_identity(node_id)
    return node_ids


def select_shard(node_ids: list[str], index: int, total: int) -> list[str]:
    """Round-robin slice ``index`` (1-based) of ``total`` over collection order."""
    if total < 1 or not 1 <= index <= total:
        raise ValueError(f"shard {index}/{total} is out of range")
    selected = node_ids[index - 1::total]
    if not selected:
        # An empty argument file would make `pytest @shard.txt` collect the whole tree.
        raise ValueError(f"shard {index}/{total} selected no identities")
    return selected


def executed_cases(report: Path) -> list[tuple[str, str]]:
    """(identity, outcome) for every testcase in one JUnit report."""
    try:
        root = ET.parse(report).getroot()
    except (OSError, ET.ParseError) as exc:
        raise ValueError(f"{report}: unreadable JUnit report ({exc})") from None
    cases = []
    for case in root.iter("testcase"):
        classname, name = case.get("classname"), case.get("name")
        if not classname or not name:
            raise ValueError(f"{report}: testcase without classname/name")
        outcome = next((tag for tag in OUTCOMES if case.find(tag) is not None), "passed")
        cases.append((f"{classname}::{name}", outcome))
    if not cases:
        raise ValueError(f"{report}: report contains no testcases")
    return cases


def verify(expected_node_ids: list[str], reports: list[Path]) -> int:
    """Return the executed count, or raise naming every violated identity."""
    expected = Counter(junit_identity(node_id) for node_id in expected_node_ids)
    if not expected:
        raise ValueError("no expected identities")
    cases = [case for report in reports for case in executed_cases(report)]
    seen = Counter(identity for identity, _ in cases)
    problems = {
        "duplicated expected": sorted(i for i, n in expected.items() if n > 1),
        "missing": sorted(set(expected) - set(seen)),
        "unexpected": sorted(set(seen) - set(expected)),
        "executed more than once": sorted(i for i, n in seen.items() if n > 1),
        "not passed": sorted(f"{i} ({o})" for i, o in cases if o != "passed"),
    }
    found = {kind: ids for kind, ids in problems.items() if ids}
    if found:
        detail = "; ".join(f"{len(ids)} {kind}: {ids[:5]}" for kind, ids in found.items())
        raise ValueError(f"executed report does not match collection -- {detail}")
    return len(cases)


def verify_union(collections: list[str], reports: list[Path], shards: int) -> int:
    """Every shard collected the same identities, and together they executed all of them."""
    if len(collections) != shards or len(reports) != shards:
        raise ValueError(f"expected {shards} shard collections and reports, got {len(collections)} and {len(reports)}")
    node_ids = [read_collection(text) for text in collections]
    if any(other != node_ids[0] for other in node_ids[1:]):
        raise ValueError("shards collected different identities; their union proves nothing")
    return verify(node_ids[0], reports)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prove pytest executed exactly what it collected.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("shard", "verify"):
        command = sub.add_parser(name)
        command.add_argument("collected", type=Path)
        command.add_argument("--index", type=int, default=1)
        command.add_argument("--total", type=int, default=1)
        if name == "verify":
            command.add_argument("reports", type=Path, nargs="+")
    union = sub.add_parser("union")
    union.add_argument("--shards", type=int, required=True)
    union.add_argument("--collected", type=Path, nargs="+", required=True)
    union.add_argument("--reports", type=Path, nargs="+", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "union":
            texts = [path.read_text(encoding="utf-8") for path in args.collected]
            count = verify_union(texts, args.reports, args.shards)
            print(f"{args.shards} shards executed all {count} collected identities exactly once; all passed")
            return 0
        node_ids = read_collection(args.collected.read_text(encoding="utf-8"))
        selected = select_shard(node_ids, args.index, args.total)
        if args.command == "shard":
            sys.stdout.write("".join(f"{node_id}\n" for node_id in selected))
        else:
            count = verify(selected, args.reports)
            print(f"executed {count} of {len(node_ids)} collected (shard {args.index}/{args.total}); all passed")
    except (OSError, ValueError) as exc:
        print(f"::error title=Executed test identities::{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
