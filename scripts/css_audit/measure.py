"""Static measurement of the seven WP4.4 shared surfaces.

Everything here is derived from files on disk at a known commit. Nothing is
projected, and nothing is inherited from an earlier arc's baseline — F14 is the
reason V3/V4 compare against *this* measurement rather than the WP4.1 JSON,
which is kept only as the immutable historical anchor.
"""

from __future__ import annotations

import ast
import re
import subprocess
from pathlib import Path

from . import specificity

ROOT = Path(__file__).resolve().parents[2]
CSS_DIR = ROOT / "static" / "css"

# The seven surfaces this arc rewrites, in cascade (link) order.
SHARED_SURFACES = (
    "motion.css",
    "base.css",
    "layout.css",
    "components.css",
    "navbar.css",
    "theme-dark.css",
    "a11y.css",
)
# Read but never written by this arc: R1 freezes tokens.css.
READ_ONLY_SURFACES = ("tokens.css",)

CONTRACT_FILES = (
    "tests/test_css_cascade_contracts.py",
    "tests/test_visual_selector_contracts.py",
)

IMPORTANT_RE = re.compile(r"!\s*important", re.IGNORECASE)
LAYER_BLOCK_RE = re.compile(r"@layer\s+([\w-]+)\s*\{")
LAYER_STATEMENT_RE = re.compile(r"@layer\s+([^;{}]+);")
COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)


def _blank_comments(css: str) -> str:
    """Replace comment bodies with spaces, preserving offsets and line numbers."""
    return COMMENT_RE.sub(lambda match: re.sub(r"[^\n]", " ", match.group(0)), css)


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def source_commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


# --------------------------------------------------------------------------
# Per-surface counts
# --------------------------------------------------------------------------


def surface_counts(filename: str) -> dict[str, int]:
    """Line count plus `!important` in BOTH units.

    F15: the plan's headline figures are `rg --count` *line* counts while
    Stylelint's `declaration-no-important` counts *declarations*. Three units
    are recorded because on these surfaces they genuinely disagree:

    * `importantLines` — a line matching `!important` (the plan's 1,264).
    * `importantOccurrences` — every match, comments included.
    * `importantDeclarations` — matches outside comments. This is the only unit
      comparable to Stylelint, and it is authoritative for V3.

    `theme-dark.css:595` carries the literal text "Zero !important." inside a
    comment, which is why the raw units over-count by exactly one arc-wide.
    """
    text = (CSS_DIR / filename).read_text(encoding="utf-8")
    code = _blank_comments(text)
    lines = text.splitlines()

    return {
        "lines": len(lines),
        "bytes": len(text.encode("utf-8")),
        "importantLines": sum(1 for line in lines if IMPORTANT_RE.search(line)),
        "importantOccurrences": len(IMPORTANT_RE.findall(text)),
        "importantDeclarations": len(IMPORTANT_RE.findall(code)),
    }


# --------------------------------------------------------------------------
# @layer spans (G10 / N2)
# --------------------------------------------------------------------------


def layer_spans(filename: str) -> list[dict[str, object]]:
    """Exact open/close line of every `@layer name { … }` block in a file.

    N2 freezes layer membership arc-wide, which is only checkable if the spans
    are recorded exactly: a rule "inside layer workout" is a claim about line
    ranges, and layered normal declarations lose to every unlayered one while
    layered `!important` wins over every unlayered one.
    """
    raw = (CSS_DIR / filename).read_text(encoding="utf-8")
    text = _blank_comments(raw)
    spans: list[dict[str, object]] = []

    for match in LAYER_BLOCK_RE.finditer(text):
        open_index = text.index("{", match.start())
        depth = 0
        close_index = None
        for index in range(open_index, len(text)):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    close_index = index
                    break
        if close_index is None:
            raise ValueError(f"unclosed @layer block in {filename} at {match.start()}")

        spans.append(
            {
                "layer": match.group(1),
                "openLine": _line_of(text, match.start()),
                "closeLine": _line_of(text, close_index),
            }
        )

    return spans


def layer_order() -> list[str]:
    text = (CSS_DIR / "tokens.css").read_text(encoding="utf-8")
    match = LAYER_STATEMENT_RE.search(text)
    if not match:
        raise ValueError("no @layer order statement in tokens.css")
    return [name.strip() for name in match.group(1).split(",")]


# --------------------------------------------------------------------------
# The `:is()` family (A10 / G1)
# --------------------------------------------------------------------------


def _selector_before(text: str, brace_index: int) -> tuple[str, int]:
    """Return the selector text preceding a `{`, and its start offset."""
    start = brace_index
    while start > 0 and text[start - 1] not in "{};":
        start -= 1
    return text[start:brace_index].strip(), start


def _enclosing_at_rules(text: str, index: int) -> list[str]:
    """Names of the at-rule blocks enclosing ``index``, outermost first."""
    stack: list[tuple[str, int]] = []
    for position, char in enumerate(text):
        if position >= index:
            break
        if char == "{":
            prelude, _ = _selector_before(text, position)
            stack.append((prelude, position))
        elif char == "}":
            if stack:
                stack.pop()
    return [prelude for prelude, _ in stack if prelude.startswith("@")]


def is_family(filename: str = "components.css") -> list[dict[str, object]]:
    """Enumerate and classify **every** `:is(` occurrence in a surface.

    A10: the plan's "complete `:is()` family" is twelve four-branch rules plus a
    three-branch reduced-motion rule at `:4433`; `components.css` contains 19
    `:is(` occurrences in total. The remainder must be classified rather than
    waved past, so R3 condition 1 ("the complete affected family") has a
    defensible closure argument.
    """
    raw = (CSS_DIR / filename).read_text(encoding="utf-8")
    text = _blank_comments(raw)
    records: list[dict[str, object]] = []

    for match in re.finditer(r":is\(", text):
        brace_index = text.find("{", match.start())
        if brace_index == -1:
            continue
        selector, selector_start = _selector_before(text, brace_index)
        # An occurrence inside a declaration value (rare) has no selector.
        if ":is(" not in selector:
            continue

        branches = specificity.branch_specificities(selector)
        # The `:is()` argument list is what exports weight across branches.
        argument_start = match.end() - 1
        argument, _ = specificity._read_balanced(text, argument_start)
        argument_branches = specificity.branch_specificities(argument)

        records.append(
            {
                "selectorLine": _line_of(text, selector_start),
                "isTokenLine": _line_of(text, match.start()),
                "ruleLine": _line_of(text, brace_index),
                "selector": " ".join(selector.split()),
                "selectorSpecificity": str(
                    specificity.selector_list_specificity(selector)
                ),
                "topLevelBranchCount": len(branches),
                "isArgumentBranchCount": len(argument_branches),
                "isArgumentBranches": [
                    {"branch": " ".join(branch.split()), "specificity": str(value)}
                    for branch, value in argument_branches
                ],
                "exportsIdWeight": any(
                    value.ids > 0 for _, value in argument_branches
                )
                and not all(value.ids > 0 for _, value in argument_branches),
                "enclosingAtRules": [
                    " ".join(rule.split())
                    for rule in _enclosing_at_rules(text, match.start())
                ],
            }
        )

    return records


# --------------------------------------------------------------------------
# Contract-anchor + pinned-declaration register (A8 + F6)
# --------------------------------------------------------------------------


def contract_anchors() -> list[dict[str, object]]:
    """Every contract assertion that reads one of the seven shared surfaces.

    A8: without this, each packet discovers its ceiling at gate time. F6: AC4's
    "proven disjoint at the file level" is already false for b–f, because the
    shared contract file pins strings *inside* `navbar.css` and `a11y.css`.

    Derived by walking the test files' ASTs rather than grepping, so a renamed
    test cannot silently drop out of the register.
    """
    anchors: list[dict[str, object]] = []
    surfaces = set(SHARED_SURFACES) | set(READ_ONLY_SURFACES)

    for relative in CONTRACT_FILES:
        path = ROOT / relative
        source = path.read_text(encoding="utf-8")
        lines = source.splitlines()
        tree = ast.parse(source)

        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            if not node.name.startswith("test_"):
                continue

            body_source = ast.get_source_segment(source, node) or ""
            touched = sorted(
                name for name in surfaces if name in body_source
            )
            # Functions that reach a surface through a dict of bundles rather
            # than a literal filename still bind it; record the indirection.
            indirect = sorted(
                name
                for name in ("FRAME_ROUTE_BUNDLES", "GLOBAL_BUNDLES", "ROUTE_BUNDLES")
                if name in body_source
            )
            if not touched and not indirect:
                continue

            assertion_lines = [
                sub.lineno
                for sub in ast.walk(node)
                if isinstance(sub, ast.Assert)
            ]

            anchors.append(
                {
                    "file": relative,
                    "test": node.name,
                    "startLine": node.lineno,
                    "endLine": (node.end_lineno or node.lineno),
                    "surfaces": touched,
                    "indirectBundleMaps": indirect,
                    "assertionCount": len(assertion_lines),
                    "assertionLines": assertion_lines,
                    "firstLine": lines[node.lineno - 1].strip(),
                }
            )

    return anchors


def pinned_declarations() -> list[dict[str, str]]:
    """Literal strings a contract pins *inside* a surface a packet owns.

    These are the packets' hard ceilings: deleting or reformatting any of these
    strings reds the shared contract file, which no packet except **i** may
    amend (N6).
    """
    pins: list[dict[str, str]] = []
    surfaces = set(SHARED_SURFACES)

    for relative in CONTRACT_FILES:
        source = (ROOT / relative).read_text(encoding="utf-8")
        tree = ast.parse(source)

        for node in tree.body:
            if not isinstance(node, ast.FunctionDef) or not node.name.startswith("test_"):
                continue
            body_source = ast.get_source_segment(source, node) or ""
            touched = sorted(name for name in surfaces if name in body_source)
            if not touched:
                continue

            for sub in ast.walk(node):
                if not isinstance(sub, ast.Compare):
                    continue
                if not any(isinstance(op, ast.In) for op in sub.ops):
                    continue
                if not isinstance(sub.left, ast.Constant) or not isinstance(
                    sub.left.value, str
                ):
                    continue
                pins.append(
                    {
                        "file": relative,
                        "test": node.name,
                        "line": str(sub.lineno),
                        "pinnedString": sub.left.value,
                        "candidateSurfaces": ", ".join(touched),
                    }
                )

    return pins


# --------------------------------------------------------------------------
# Oracle blind-spot register (F2)
# --------------------------------------------------------------------------

# The (selector, property) pairs `prepareForScreenshot()` neutralizes before any
# pixel is captured. Curated deliberately rather than parsed: the point is a
# reviewable statement of what the pixel oracle CANNOT see, and a TS parser that
# silently missed a rule would produce exactly the false confidence F2 names.
# `verify_blind_spots()` re-derives each entry from the helper text, so the
# register cannot drift away from the file it describes.
BLIND_SPOT_REGISTER: tuple[dict[str, object], ...] = (
    {
        "selector": "*, *::before, *::after",
        "properties": [
            "animation-delay",
            "animation-duration",
            "animation-iteration-count",
            "transition-duration",
            "transition-delay",
        ],
        "neutralizedTo": "0s / 1",
        "helperEvidence": "animation-duration: 0s !important;",
        "blindsPackets": ["c"],
        "why": "F1 — motion.css's entire output is zeroed before capture, so a "
               "packet deleting the whole file yields a byte-identical matrix.",
    },
    {
        "selector": "*, *::before, *::after",
        "properties": ["backdrop-filter", "-webkit-backdrop-filter"],
        "neutralizedTo": "none",
        "helperEvidence": "backdrop-filter: none !important;",
        "blindsPackets": ["h", "i", "j"],
        "why": "F2 — the glass families in components.css and the theme-dark.css "
               "rule pinned by the cascade contract are the core surface of h/i/j.",
    },
    {
        "selector": "[data-visual-scale-control]",
        "properties": ["background", "border-color", "color"],
        "neutralizedTo": "transparent",
        "helperEvidence": "[data-visual-scale-control]",
        "blindsPackets": ["d"],
        "why": "F2 — WP4.4-d owns the data-scale UI scale system.",
    },
    {
        "selector": "[data-visual-icon]",
        "properties": ["visibility"],
        "neutralizedTo": "hidden",
        "helperEvidence": "[data-visual-icon]",
        "blindsPackets": ["b", "f"],
        "why": "F2 — icon affordances are invisible to the oracle entirely.",
    },
    {
        "selector": "[data-visual-surface][data-visual-surface] (dark theme only)",
        "properties": [
            "background",
            "background-image",
            "border-color",
            "border-radius",
            "box-shadow",
            "text-shadow",
        ],
        "neutralizedTo": "forced flat values",
        "helperEvidence": "[data-visual-surface][data-visual-surface]",
        "blindsPackets": ["j"],
        "why": "F2 — the dark baseline is blind to surface paint on exactly the "
               "elements theme-dark.css exists to paint.",
    },
    {
        "selector": "form controls (input/select/textarea/button families)",
        "properties": ["border-radius", "box-shadow", "text-shadow"],
        "neutralizedTo": "0 / none",
        "helperEvidence": "box-shadow: none !important;",
        "blindsPackets": ["d", "h", "j"],
        "why": "F2 — re-applied inline after load, so even late overrides are hidden.",
    },
)


def verify_blind_spots() -> list[str]:
    """Confirm every register entry still corresponds to the live helper."""
    helper = (ROOT / "e2e" / "visual-helpers.ts").read_text(encoding="utf-8")
    failures = [
        f"blind-spot register entry {entry['selector']!r} cites "
        f"{entry['helperEvidence']!r}, absent from e2e/visual-helpers.ts"
        for entry in BLIND_SPOT_REGISTER
        if str(entry["helperEvidence"]) not in helper
    ]
    return failures


SNAPSHOT_DIRS = (
    "win32/visual.spec.ts-snapshots",
    "win32/visual-baseline-thumbnails.spec.ts-snapshots",
    "linux/visual.spec.ts-snapshots",
    "linux/visual-baseline-thumbnails.spec.ts-snapshots",
)


def snapshot_manifest() -> dict[str, dict[str, object]]:
    """Name + size manifest over the committed screenshot trees (F12).

    Deliberately not a content hash of the PNGs: the point is to make an
    accidental `--update-snapshots` loud, and a regenerated baseline changes its
    byte size essentially always while costing nothing to check. Content hashing
    162 files on every pytest run buys precision this guard does not need.
    """
    import hashlib

    root = ROOT / "e2e" / "__screenshots__"
    manifest: dict[str, dict[str, object]] = {}

    for relative in SNAPSHOT_DIRS:
        directory = root / relative
        files = sorted(path.name for path in directory.glob("*.png"))
        digest = hashlib.sha256()
        for name in files:
            digest.update(name.encode("utf-8"))
            digest.update(str((directory / name).stat().st_size).encode("utf-8"))
        manifest[relative] = {
            "count": len(files),
            "files": files,
            "nameAndSizeSha256": digest.hexdigest(),
        }

    return manifest


def fatigue_baseline_status() -> dict[str, str]:
    """N7 — `/fatigue` baselines are CREATED, on both platforms.

    Windows is generated locally. Linux can only come from the `visual-linux`
    deep-gate job, so the status is reported honestly rather than assumed; the
    contract asserts the set is all-or-nothing on each platform.
    """
    root = ROOT / "e2e" / "__screenshots__"
    expected = [
        f"fatigue-{viewport}-{theme}.png"
        for viewport in ("mobile", "tablet", "desktop")
        for theme in ("light", "dark")
    ]

    status = {}
    for platform in ("win32", "linux"):
        directory = root / platform / "visual.spec.ts-snapshots"
        present = sum(1 for name in expected if (directory / name).is_file())
        status[platform] = "created" if present == len(expected) else "pending"
    return status


def screenshot_tolerances() -> dict[str, object]:
    """The tolerance constants F3 says V1 cannot be enforced through.

    Recorded so a packet cannot quietly widen the oracle: `maxDiffPixels: 800`
    means up to 800 px per route × viewport × theme pass unnoticed, and the
    animated-logo band (1,039 / 1,046 px) sits *above* that tolerance — it is a
    real snapshot failure, not a diff the option absorbs.
    """
    helper = (ROOT / "e2e" / "visual-helpers.ts").read_text(encoding="utf-8")
    values: dict[str, object] = {}
    for key in ("maxDiffPixels", "threshold", "fullPage"):
        # Match the returned object literals (`key: 800,`), not the TypeScript
        # interface declarations above them (`key: number;`).
        found = re.findall(rf"{key}:\s*([^,;\n}}]+),", helper)
        values[key] = sorted({value.strip() for value in found})
    values["animatedLogoBandPx"] = [1039, 1046]
    values["bandExceedsTolerance"] = True
    return values
