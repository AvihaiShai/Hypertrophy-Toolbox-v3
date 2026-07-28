"""Emit `docs/CSS_PHASE4_WP4_4_A_BASELINE.json`.

F13 converts "no later packet may inherit a projection as fact" from prose into
a gate: every number packets b–k cite must appear in this file, and
`test_wp4_4_baseline_is_pinned_and_matches_its_source_commit` re-derives the
per-surface line counts from the surfaces **as committed at `sourceCommit`** —
not from the working tree — so a stale baseline reds pytest rather than passing
quietly, while a later packet's authorized deletion does not.

usage:
    python -m scripts.css_audit.emit_baseline [--stylelint artifacts/wp4_4/stylelint_surfaces.json]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import measure, specificity

BASELINE_PATH = measure.ROOT / "docs" / "CSS_PHASE4_WP4_4_A_BASELINE.json"


def build(stylelint_path: Path | None) -> dict[str, object]:
    self_check_failures = specificity.self_check()
    if self_check_failures:
        raise SystemExit(
            "M4 specificity self-check failed; refusing to emit a baseline:\n  "
            + "\n  ".join(self_check_failures)
        )

    blind_spot_failures = measure.verify_blind_spots()
    if blind_spot_failures:
        raise SystemExit(
            "F2 blind-spot register no longer matches e2e/visual-helpers.ts:\n  "
            + "\n  ".join(blind_spot_failures)
        )

    surfaces: dict[str, dict[str, object]] = {
        name: dict(measure.surface_counts(name)) for name in measure.SHARED_SURFACES
    }
    for name in measure.READ_ONLY_SURFACES:
        entry: dict[str, object] = dict(measure.surface_counts(name))
        entry["readOnly"] = True
        surfaces[name] = entry

    totals = measure_totals()

    stylelint: dict[str, object] | None = None
    if stylelint_path and stylelint_path.exists():
        stylelint = json.loads(stylelint_path.read_text(encoding="utf-8"))

    is_records = measure.is_family()
    four_branch = [r for r in is_records if r["isArgumentBranchCount"] == 4]
    three_branch = [r for r in is_records if r["isArgumentBranchCount"] == 3]
    six_branch = [r for r in is_records if r["isArgumentBranchCount"] == 6]

    is_family_summary = {
        "totalIsTokens": len(is_records),
        "distinctRules": len({r["ruleLine"] for r in is_records}),
        "fourBranchTokens": len(four_branch),
        "fourBranchRules": len({r["ruleLine"] for r in four_branch}),
        "threeBranchRules": len({r["ruleLine"] for r in three_branch}),
        "sixBranchTokens": len(six_branch),
        "sixBranchRules": len({r["ruleLine"] for r in six_branch}),
    }

    return {
        "schemaVersion": 1,
        "packet": "WP4.4-a",
        "sourceCommit": measure.source_commit(),
        "purpose": (
            "Measured baseline for the WP4.4 shared-bundle arc. Packets b-k cite "
            "this file; a number absent from it may not be quoted as fact (F13)."
        ),
        "authoritativeUnits": {
            "important": "importantDeclarations (comments excluded) — the only unit comparable to Stylelint",
            "stylelint": "seven shared surfaces only, excluding scss/** and page bundles (F20)",
            "lineCounts": "splitlines() over the file as committed at sourceCommit",
        },
        "supersedes": {
            "docs/CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json": (
                "retained as the immutable historical anchor for the arc-level "
                "report at k; its thresholds are two arcs old and are NOT V3/V4 "
                "pass conditions (F14)"
            ),
        },
        "surfaces": surfaces,
        "totals": totals,
        "stylelintSevenSurfaces": stylelint,
        "layers": {
            "order": measure.layer_order(),
            "orderDeclaredIn": "static/css/tokens.css",
            "frozenForArc": True,
            "freezeRuling": "N2 — no packet may move a rule across a layer boundary",
            "spans": {
                name: measure.layer_spans(name)
                for name in sorted(
                    set(measure.SHARED_SURFACES)
                    | set(measure.READ_ONLY_SURFACES)
                    | {
                        "pages-workout-plan.css",
                        "pages-welcome.css",
                    }
                )
                if measure.layer_spans(name)
            },
        },
        "isFamily": is_family_summary | {"records": is_records},
        "snapshotManifest": measure.snapshot_manifest(),
        "fatigueBaselines": measure.fatigue_baseline_status()
        | {
            "ruling": "N7 — creation on Windows and Linux, authorized at Gate 1; "
            "NOT authorization to rebaseline any pre-existing screenshot",
            "matrixSize": "11 pages x 3 viewports x 2 themes = 66 (was 60)",
        },
        "contractAnchors": measure.contract_anchors(),
        "pinnedDeclarations": measure.pinned_declarations(),
        "oracleBlindSpots": [dict(entry) for entry in measure.BLIND_SPOT_REGISTER],
        "screenshotTolerances": measure.screenshot_tolerances(),
        "specificityModel": {
            "module": "scripts/css_audit/specificity.py",
            "selfCheckCases": len(specificity.SELF_CHECK_CASES),
            "splitSelfCheckCases": len(specificity.SPLIT_SELF_CHECK_CASES),
            "selfCheckFailures": 0,
        },
    }


def measure_totals() -> dict[str, int]:
    """Line and `!important` totals over the seven shared surfaces."""
    counts = [measure.surface_counts(name) for name in measure.SHARED_SURFACES]
    return {
        "sharedSurfaceLines": sum(entry["lines"] for entry in counts),
        "importantDeclarations": sum(entry["importantDeclarations"] for entry in counts),
        "importantLines": sum(entry["importantLines"] for entry in counts),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stylelint",
        type=Path,
        default=measure.ROOT / "artifacts" / "wp4_4" / "stylelint_surfaces.json",
        help="seven-surface stylelint JSON from stylelint_surfaces.mjs",
    )
    parser.add_argument("--out", type=Path, default=BASELINE_PATH)
    args = parser.parse_args()

    baseline = build(args.stylelint)
    args.out.write_text(
        json.dumps(baseline, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    # Reported from typed sources rather than by indexing back into the
    # object-valued payload, which is JSON-shaped and not statically indexable.
    totals = measure_totals()
    family = measure.is_family()
    print(f"wrote {args.out.relative_to(measure.ROOT)}")
    print(f"  sourceCommit           {measure.source_commit()}")
    print(f"  shared surface lines   {totals['sharedSurfaceLines']}")
    print(f"  !important decls       {totals['importantDeclarations']}")
    print(
        f"  :is() tokens / rules   {len(family)} / "
        f"{len({record['ruleLine'] for record in family})}"
    )
    print(f"  contract anchors       {len(measure.contract_anchors())}")
    print(f"  pinned declarations    {len(measure.pinned_declarations())}")


if __name__ == "__main__":
    main()
