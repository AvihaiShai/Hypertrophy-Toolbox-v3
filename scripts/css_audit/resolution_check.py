"""M4 resolution self-check — does the specificity model agree with the browser?

Method rule M4: a model that mishandles ``:is()``/``:where()``/``:not()``/``:has()``
or naively comma-splits a selector list will report an owner that contradicts the
computed value. Unit tests over hand-computed selectors (``specificity.self_check``)
catch the arithmetic; this catches the rest, by replaying the browser's own
cascade data.

Chrome returns ``CSS.getMatchedStylesForNode`` results in increasing precedence
order. Within one cascade bucket — same origin, same importance, same layer —
that order must be non-decreasing in specificity. Every inversion is a place
where this model and Blink disagree about who owns a declaration, which is
exactly the failure that would let a packet delete a live rule.

usage:
    python -m scripts.css_audit.resolution_check [--runtime artifacts/wp4_4/runtime]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import measure, specificity


def _bucket(rule: dict, important: bool) -> tuple:
    """Cascade bucket: declarations only compete on specificity inside one."""
    layers = tuple(rule.get("layers") or ())
    media = tuple(rule.get("media") or ())
    return (important, layers, media)


def _matched_specificity(rule: dict) -> specificity.Specificity:
    """Specificity of the branches that actually matched this element.

    Using the whole selector list would answer a different question. A rule
    written `:is(#id, .cls) td` matches a `.cls` element through its class
    branch, and CSS still charges it the ID branch's weight — but a rule written
    `#id td, .cls td` matched through its second branch is charged only (0,1,1).
    `matchingSelectors` is what distinguishes the two, and it is the distinction
    WP4.4-i exists to act on.
    """
    selectors = rule.get("selectors") or []
    indices = rule.get("matchingSelectors") or []

    if selectors and indices:
        matched = [selectors[i] for i in indices if i < len(selectors)]
        if matched:
            return max(
                (specificity.compound_specificity(s) for s in matched), key=tuple
            )

    return specificity.selector_list_specificity(rule.get("selector", ""))


def check_file(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    inversions: list[dict] = []
    compared = 0
    elements = 0

    for record in payload.get("matchedRules", []):
        elements += 1
        buckets: dict[tuple, list[dict]] = {}

        for rule in record.get("rules", []):
            has_important = any(
                declaration.get("important") for declaration in rule.get("declarations", [])
            )
            for important in ({True, False} if has_important else {False}):
                buckets.setdefault(_bucket(rule, important), []).append(rule)

        for bucket, rules in buckets.items():
            previous: tuple[str, specificity.Specificity] | None = None
            for rule in rules:
                current = _matched_specificity(rule)
                if previous is not None:
                    previous_selector, previous_specificity = previous
                    compared += 1
                    if tuple(current) < tuple(previous_specificity):
                        inversions.append(
                            {
                                "path": record["path"],
                                "bucket": {
                                    "important": bucket[0],
                                    "layers": list(bucket[1]),
                                    "media": list(bucket[2]),
                                },
                                "earlierSelector": previous_selector,
                                "earlierSpecificity": str(previous_specificity),
                                "laterSelector": rule.get("selector", ""),
                                "laterSpecificity": str(current),
                            }
                        )
                previous = (rule.get("selector", ""), current)

    return {
        "file": path.name,
        "elements": elements,
        "orderedPairsCompared": compared,
        "inversions": len(inversions),
        "detail": inversions[:50],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--runtime",
        type=Path,
        default=measure.ROOT / "artifacts" / "wp4_4" / "runtime",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=measure.ROOT / "artifacts" / "wp4_4" / "resolution_check.json",
    )
    args = parser.parse_args()

    files = sorted(
        path
        for path in args.runtime.glob("*.json")
        if path.name not in {"summary.json", "resolution_check.json"}
    )
    if not files:
        raise SystemExit(f"no runtime capture files under {args.runtime}")

    unit_failures = specificity.self_check()
    results = [check_file(path) for path in files]
    total_inversions = sum(result["inversions"] for result in results)
    total_pairs = sum(result["orderedPairsCompared"] for result in results)

    report = {
        "schemaVersion": 1,
        "sourceCommit": measure.source_commit(),
        "unitSelfCheckFailures": unit_failures,
        "contextsChecked": len(results),
        "orderedPairsCompared": total_pairs,
        "inversions": total_inversions,
        "pass": total_inversions == 0 and not unit_failures,
        "byContext": results,
    }
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"contexts            {len(results)}")
    print(f"ordered pairs       {total_pairs}")
    print(f"unit self-check     {'PASS' if not unit_failures else unit_failures}")
    print(f"cascade inversions  {total_inversions}")
    print(f"M4 resolution check {'PASS' if report['pass'] else 'FAIL'}")
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
