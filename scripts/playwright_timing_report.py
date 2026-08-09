"""Summarize where Playwright wall-clock actually goes.

Reads a report Playwright already produces -- the CI JUnit file or a local JSON
run -- and prints per-spec duration, the slowest individual tests, the
slowest-file floor, and shard balance. Nothing here runs a browser, so it is
free to run after any suite.

The floor is the number worth internalizing before changing shard count. A
spec file is the indivisible unit of `--shard`, so no shard count can finish
sooner than the single slowest file. Adding shards below that point buys
wall-clock; adding them past it buys nothing but runner cost.

Two scope rules, because both are easy to get wrong and neither is visible in
the output:

* **Match the group to the decision.** The local default suite is every
  non-visual spec; CI's required functional gate runs a smaller curated set
  (the list in `ci.yml`, see e2e/CLAUDE.md's inclusion contract). A local
  whole-group measurement must not be used to argue for a CI shard count —
  only the required set can do that.
* **Pass `--shards 1` when the input is already one shard's report.** Packing
  a half-suite into N models a hypothetical re-split of that half, and reads
  as a global balance it cannot describe. Real balance is the shards' totals
  compared.

Usage:
    python scripts/playwright_timing_report.py --junit artifacts/playwright/junit.xml
    python scripts/playwright_timing_report.py --json  artifacts/playwright/timing/functional.json
    python scripts/playwright_timing_report.py --junit ... --shards 2 --markdown
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys
import xml.etree.ElementTree as ET


def _spec_name(raw: str) -> str:
    return pathlib.PurePath(raw.replace("\\", "/")).name


def load_json(path: pathlib.Path) -> tuple[dict[str, float], dict[str, int], list]:
    report = json.loads(path.read_text(encoding="utf-8"))
    per_spec: dict[str, float] = collections.defaultdict(float)
    counts: dict[str, int] = collections.defaultdict(int)
    tests: list[tuple[float, str, str]] = []

    def walk(suite: dict, spec: str) -> None:
        spec = _spec_name(suite.get("file", spec))
        for case in suite.get("specs", []):
            for test in case.get("tests", []):
                ms = sum(r.get("duration", 0) for r in test.get("results", []))
                per_spec[spec] += ms
                counts[spec] += 1
                tests.append((ms, spec, case.get("title", "")))
        for child in suite.get("suites", []):
            walk(child, spec)

    for suite in report.get("suites", []):
        walk(suite, suite.get("file", "?"))
    return dict(per_spec), dict(counts), tests


def load_junit(path: pathlib.Path) -> tuple[dict[str, float], dict[str, int], list]:
    root = ET.parse(path).getroot()
    suites = root.iter("testsuite") if root.tag == "testsuites" else [root]
    per_spec: dict[str, float] = collections.defaultdict(float)
    counts: dict[str, int] = collections.defaultdict(int)
    tests: list[tuple[float, str, str]] = []

    for suite in suites:
        spec = _spec_name(suite.get("name", "?"))
        for case in suite.iter("testcase"):
            ms = float(case.get("time", "0")) * 1000
            # Prefer the file attribute when Playwright supplies it; a suite can
            # otherwise be named after a describe block rather than the file.
            owner = _spec_name(case.get("file") or spec)
            per_spec[owner] += ms
            counts[owner] += 1
            tests.append((ms, owner, case.get("name", "")))
    return dict(per_spec), dict(counts), tests


def balance(per_spec: dict[str, float], shards: int) -> list[tuple[int, float, int]]:
    """Greedy longest-first packing -- the best a file-granular split can do.

    Playwright's own `--shard` does not pack optimally, so this is a bound, not
    a prediction: it says how much room a smarter split would have.
    """
    slots: list[tuple[float, int, int]] = [(0.0, 0, index) for index in range(shards)]
    for _, ms in sorted(per_spec.items(), key=lambda kv: -kv[1]):
        total, count, index = min(slots)
        slots[slots.index((total, count, index))] = (total + ms, count + 1, index)
    return [(index + 1, total, count) for total, count, index in sorted(slots, key=lambda s: s[2])]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--junit", type=pathlib.Path)
    source.add_argument("--json", type=pathlib.Path)
    parser.add_argument(
        "--shards",
        type=int,
        default=2,
        help=(
            "Model a split of THIS report across N shards. Use 1 when the report "
            "is already one shard's output -- packing a half-suite into 2 models a "
            "hypothetical re-split, not the real global balance."
        ),
    )
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--markdown", action="store_true", help="GitHub step-summary form")
    parser.add_argument(
        "--label",
        default="",
        help="Scope label for the heading, e.g. 'shard 1/2'. Names what the report covers.",
    )
    args = parser.parse_args()

    path = args.junit or args.json
    if not path.is_file():
        print(f"No report at {path}; nothing to summarize.", file=sys.stderr)
        return 0

    per_spec, counts, tests = load_junit(path) if args.junit else load_json(path)
    if not per_spec:
        print(f"{path} contained no test cases.", file=sys.stderr)
        return 0

    total = sum(per_spec.values())
    floor_spec = max(per_spec, key=lambda k: per_spec[k])
    floor = per_spec[floor_spec]
    out = print

    if args.markdown:
        scope = f" — {args.label}" if args.label else ""
        out(f"### Playwright timing{scope}")
        out("")
        out(f"**{sum(counts.values())} tests / {len(per_spec)} specs / {total/1000:.1f}s**")
        out("")
        if args.shards <= 1:
            # This report is one shard's own output. Its slowest file is the
            # floor *within this shard*, and its total is half the story: the
            # global balance is the two jobs' totals side by side, which no
            # single job can see. Saying otherwise would invent a number.
            out(f"Slowest file in this scope: `{floor_spec}` at {floor/1000:.1f}s")
            out("")
            out("_Scope is this job alone. Global shard balance is the two jobs' totals compared; it is not derivable here._")
        else:
            out(f"Slowest file (shard floor): `{floor_spec}` at {floor/1000:.1f}s")
        out("")
        out("| spec | tests | sec | % |")
        out("|---|---:|---:|---:|")
        for spec, ms in sorted(per_spec.items(), key=lambda kv: -kv[1])[: args.top]:
            out(f"| `{spec}` | {counts[spec]} | {ms/1000:.1f} | {100*ms/total:.1f}% |")
        if args.shards > 1:
            out("")
            out("| shard | sec | specs |")
            out("|---:|---:|---:|")
            for index, seconds, count in balance(per_spec, args.shards):
                out(f"| {index} | {seconds/1000:.1f} | {count} |")
        return 0

    out(f"tests {sum(counts.values())} / specs {len(per_spec)} / total {total/1000:.1f}s")
    out(f"\n{'spec':46s} {'tests':>5s} {'sec':>8s} {'%':>6s}")
    for spec, ms in sorted(per_spec.items(), key=lambda kv: -kv[1]):
        out(f"{spec:46s} {counts[spec]:5d} {ms/1000:8.1f} {100*ms/total:5.1f}%")

    out(f"\nslowest {args.top} tests:")
    for ms, spec, title in sorted(tests, reverse=True)[: args.top]:
        out(f"  {ms/1000:6.1f}s  {spec:40s} {title[:60]}")

    out(f"\nslowest-file floor: {floor/1000:.1f}s ({floor_spec})")
    out(f"best-case balanced split at N shards is max(floor, total/N):")
    for n in (2, 3, 4, 6, 8):
        best = max(floor, total / n)
        note = "  <- floor-bound, more shards buy nothing" if best == floor else ""
        out(f"  N={n}: {best/1000:7.1f}s{note}")

    out(f"\ngreedy {args.shards}-shard packing (bound, not Playwright's own split):")
    for index, seconds, count in balance(per_spec, args.shards):
        out(f"  shard {index}: {seconds/1000:7.1f}s over {count} specs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
