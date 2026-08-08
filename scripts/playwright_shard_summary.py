"""Consolidate one isolated shard run into a single comparable result.

`run-playwright-shards.ps1` writes a `shards.json` manifest holding what only
the launcher can know -- each shard's process wall time and exit code -- next to
the per-shard Playwright JSON reports, which hold what only Playwright knows:
which tests ran and how long each took.

The distinction those two sources make is the whole point of this script.

* **Wall time** is the launcher's stopwatch on the shard process. It includes
  seeding the database, starting Flask, waiting for the port, launching
  Chromium, and tearing all of it down.
* **Testcase duration** is the sum of what Playwright timed. It includes none of
  that.

Reporting either one alone misleads in a specific direction. Summed duration
makes sharding look better than it is, because it hides the per-shard startup
that N shards pay N times. Wall time alone hides that a shard finished its tests
early and spent the difference on setup. The gap between them is the overhead
budget, and it is the number that decides whether adding a shard can still pay.

Balance is reported as the shards' own totals compared, never as a repacking of
one shard's report -- see the scope rules in playwright_timing_report.py.
"""

from __future__ import annotations

import argparse
import itertools
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from playwright_timing_report import load_json  # noqa: E402


def _outcome_counts(report: pathlib.Path) -> dict[str, int]:
    """Pass/fail/skip straight from the reporter's own stats block."""
    stats = json.loads(report.read_text(encoding="utf-8")).get("stats", {})
    return {
        "passed": stats.get("expected", 0),
        "failed": stats.get("unexpected", 0),
        "flaky": stats.get("flaky", 0),
        "skipped": stats.get("skipped", 0),
    }


def _spec_ids(report: pathlib.Path) -> list[tuple[str, str]]:
    """Every test case's stable id, paired with a human-readable label.

    Returned as a list rather than a set on purpose: duplicates are one of the
    things being checked, and a set would silently swallow them.
    """
    data = json.loads(report.read_text(encoding="utf-8"))
    found: list[tuple[str, str]] = []

    def walk(suite: dict) -> None:
        for spec in suite.get("specs", []):
            name = pathlib.PurePath(str(spec.get("file", "?")).replace("\\", "/")).name
            found.append((spec["id"], f"{name} :: {spec.get('title', '')}"))
        for child in suite.get("suites", []):
            walk(child)

    for suite in data.get("suites", []):
        walk(suite)
    return found


def check_identity(
    reports: list[tuple[int, pathlib.Path]],
    baseline: pathlib.Path | None,
    expected_total: int,
) -> bool:
    """Prove the shards partition the suite: unique, disjoint, complete.

    Sharding is only trustworthy if the union of what ran equals what a serial
    run would have run. A shard that silently drops a spec still exits 0 and
    still looks fast, and the timing table cannot show it -- so it is checked
    against the ids themselves.
    """
    print("\n--- test identity ---")
    ok = True
    per_shard: dict[int, list[tuple[str, str]]] = {}

    for index, path in reports:
        if not path.is_file():
            print(f"  shard {index}: NO REPORT at {path}")
            ok = False
            continue
        entries = _spec_ids(path)
        per_shard[index] = entries
        ids = [entry[0] for entry in entries]
        duplicates = {i for i in ids if ids.count(i) > 1}
        if duplicates:
            ok = False
            print(f"  shard {index}: {len(duplicates)} DUPLICATE id(s) within the shard")
            for dupe in sorted(duplicates):
                label = next(label for i, label in entries if i == dupe)
                print(f"      {dupe}  {label}")
        else:
            print(f"  shard {index}: {len(ids)} tests, all ids unique")

    indices = sorted(per_shard)
    for left, right in itertools.combinations(indices, 2):
        overlap = {i for i, _ in per_shard[left]} & {i for i, _ in per_shard[right]}
        if overlap:
            ok = False
            print(f"  shards {left} and {right}: {len(overlap)} OVERLAPPING id(s)")
            for shared in sorted(overlap):
                label = next(label for i, label in per_shard[left] if i == shared)
                print(f"      {shared}  {label}")
    if len(indices) > 1 and ok:
        print(f"  shards are pairwise disjoint ({len(indices)} shards compared)")

    union = {i for entries in per_shard.values() for i, _ in entries}
    print(f"  union: {len(union)} unique test ids (expected {expected_total})")
    if len(union) != expected_total:
        ok = False
        print(f"  !! union size {len(union)} != expected {expected_total}")

    if baseline is not None and baseline.is_file():
        expected = {i: label for i, label in _spec_ids(baseline)}
        missing = set(expected) - union
        unexpected = union - set(expected)
        if missing:
            ok = False
            print(f"  !! {len(missing)} id(s) MISSING versus the N=1 baseline:")
            for i in sorted(missing):
                print(f"      {i}  {expected[i]}")
        if unexpected:
            ok = False
            labels = {i: label for entries in per_shard.values() for i, label in entries}
            print(f"  !! {len(unexpected)} UNEXPECTED id(s) absent from the baseline:")
            for i in sorted(unexpected):
                print(f"      {i}  {labels.get(i, '?')}")
        if not missing and not unexpected:
            print(f"  union matches the N=1 baseline exactly ({len(expected)} ids)")
    elif baseline is not None:
        print(f"  (no baseline report at {baseline})")

    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=pathlib.Path, required=True)
    parser.add_argument("--top", type=int, default=8, help="slowest specs to list")
    parser.add_argument(
        "--baseline",
        type=pathlib.Path,
        help="an N=1 report.json defining the expected test-id set",
    )
    parser.add_argument("--expect-tests", type=int, default=477)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
    shards = manifest["shards"]
    results = manifest["results"]

    rows = []
    combined: dict[str, float] = {}
    for result in results:
        report = pathlib.Path(result["jsonReport"])
        wall = float(result["wallSeconds"])
        if report.is_file():
            per_spec, counts, _ = load_json(report)
            outcome = _outcome_counts(report)
            tested = sum(per_spec.values()) / 1000
            for spec, ms in per_spec.items():
                combined[spec] = combined.get(spec, 0.0) + ms
            specs = len(per_spec)
            total_tests = sum(counts.values())
        else:
            outcome = {"passed": 0, "failed": 0, "flaky": 0, "skipped": 0}
            tested = 0.0
            specs = 0
            total_tests = 0

        rows.append(
            {
                "index": result["index"],
                "port": result["port"],
                # A null exit code means the launcher could not read one, which
                # is a launcher defect and not a passing shard. Shown as '?' so
                # it can never be mistaken for 0.
                "exit": "?" if result["exitCode"] is None else result["exitCode"],
                "wall": wall,
                "tested": tested,
                "overhead": wall - tested,
                "specs": specs,
                "tests": total_tests,
                **outcome,
            }
        )

    walls = [row["wall"] for row in rows]
    slowest = max(rows, key=lambda row: row["wall"])

    print(f"\n=== {shards} isolated shard(s) — required functional set ===\n")
    print(
        f"{'shard':>5} {'port':>6} {'exit':>5} {'wall s':>8} {'tested s':>9} "
        f"{'overhead':>9} {'specs':>6} {'tests':>6} {'pass':>5} {'fail':>5} "
        f"{'flaky':>5} {'skip':>5}"
    )
    for row in rows:
        print(
            f"{row['index']:>5} {row['port']:>6} {row['exit']:>5} {row['wall']:>8.1f} "
            f"{row['tested']:>9.1f} {row['overhead']:>9.1f} {row['specs']:>6} "
            f"{row['tests']:>6} {row['passed']:>5} {row['failed']:>5} "
            f"{row['flaky']:>5} {row['skipped']:>5}"
        )

    print()
    print(f"run wall clock (launcher)      : {manifest['wallSeconds']:.1f}s")
    print(f"slowest shard                  : {slowest['index']} at {slowest['wall']:.1f}s")
    print(f"summed testcase duration       : {sum(r['tested'] for r in rows):.1f}s")
    print(f"summed setup/teardown overhead : {sum(r['overhead'] for r in rows):.1f}s")

    if len(rows) > 1:
        spread = max(walls) - min(walls)
        ratio = max(walls) / min(walls) if min(walls) else float("inf")
        print(f"shard balance (wall)           : {min(walls):.1f}s–{max(walls):.1f}s "
              f"(spread {spread:.1f}s, {ratio:.2f}x)")
        # The run cannot finish before its slowest shard, so idle time is what
        # every other shard wasted waiting. It is the honest cost of imbalance.
        idle = sum(max(walls) - wall for wall in walls)
        print(f"idle worker time               : {idle:.1f}s")

    total_failed = sum(row["failed"] for row in rows)
    total_flaky = sum(row["flaky"] for row in rows)
    if total_failed or total_flaky:
        print(f"\n!! {total_failed} failed, {total_flaky} flaky — timings are not comparable")

    bad_exit = [row["index"] for row in rows if row["exit"] != 0]
    if bad_exit:
        print(f"\n!! shard(s) {bad_exit} did not report exit code 0")

    identity_ok = check_identity(
        [(result["index"], pathlib.Path(result["jsonReport"])) for result in results],
        args.baseline,
        args.expect_tests,
    )

    if combined:
        print(f"\nslowest {args.top} specs (summed testcase time across shards):")
        for spec, ms in sorted(combined.items(), key=lambda kv: -kv[1])[: args.top]:
            print(f"  {ms / 1000:>7.1f}s  {spec}")
        floor_spec, floor_ms = max(combined.items(), key=lambda kv: kv[1])
        print(
            f"\nfile-granular floor: {floor_ms / 1000:.1f}s ({floor_spec}) — no "
            "shard count finishes sooner, because --shard splits by file."
        )

    return 0 if (not total_failed and not bad_exit and identity_ok) else 1


if __name__ == "__main__":
    raise SystemExit(main())
