"""Generate the committed test inventory from live collection output.

Blindspot B3 in docs/TESTING_STRATEGY_PLANNING.md: every hand-maintained test
count in this repository had drifted, in five mutually contradictory directions
at once. The fix is to stop maintaining them by hand. This script is the single
producer of those numbers; docs point at its output instead of restating it.

Sources of truth, all read-only:
  * `npx playwright test --list --project=chromium --reporter=json`
  * `<this interpreter> -m pytest tests --collect-only -q`
  * a literal scan of `e2e/**/*.ts` for `waitForTimeout`

The required-functional-set figure is *derived* from `.github/workflows/ci.yml`
rather than typed in, so it cannot disagree with what CI actually runs.

Usage:
    python scripts/generate_test_inventory.py            # regenerate in place
    python scripts/generate_test_inventory.py --check    # diff against committed

Determinism contract (docs/TESTING_STRATEGY_PLANNING.md section 7.3, criterion 1):
no timestamps, no absolute paths, no host or tool versions, POSIX separators,
sorted keys and sorted rows, LF newlines, and `--check` compares with line
endings normalized so a CRLF checkout is not reported as drift.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "docs" / "test_inventory"
JSON_PATH = OUTPUT_DIR / "TEST_INVENTORY.json"
MARKDOWN_PATH = OUTPUT_DIR / "TEST_INVENTORY.md"

CI_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"
FUNCTIONAL_SHARD_JOB = "e2e-functional-shard"

SCHEMA_VERSION = 1

# Files whose COLLECTED NODE COUNT legitimately depends on the machine, not on
# the code. Their counts are reported but never committed, because a committed
# number would report drift on every host that differs from whoever regenerated
# last. Everything else must reproduce byte-for-byte on Windows and Linux.
#
# Add an entry only for genuine environment dependence, never to silence a real
# diff. A stale entry is caught: the generator fails if a listed file collects
# nothing.
ENVIRONMENT_DEPENDENT_PYTEST_FILES = {
    "tests/test_guard_destructive_command.py": (
        "Parametrized over the PowerShell hosts actually installed "
        "(HOSTS = [n for n in ('powershell', 'pwsh') if shutil.which(n)], line 58). "
        "A Windows box has both and collects 322; the ubuntu runner has pwsh only "
        "and collects 163. That is the point of the file -- the guard once passed "
        "under pwsh 7 and was a parser error under Windows PowerShell 5.1 -- so the "
        "variance is the design, not drift."
    ),
}


# --------------------------------------------------------------------------
# Playwright
# --------------------------------------------------------------------------

def _npx() -> str:
    npx = shutil.which("npx")
    if npx is None:
        raise SystemExit(
            "npx not found on PATH. Run `npm ci` first (the Playwright test list "
            "needs node_modules; it does not need browser binaries)."
        )
    return npx


def collect_playwright() -> dict[str, int]:
    """Return {spec filename: test count}. Lists only; starts no browser or server."""
    env = dict(os.environ)
    # The JSON reporter writes to a file instead of stdout when this is set.
    env.pop("PLAYWRIGHT_JSON_OUTPUT_NAME", None)
    env.pop("PLAYWRIGHT_JSON_OUTPUT_DIR", None)
    env.pop("PLAYWRIGHT_JSON_OUTPUT_FILE", None)

    result = subprocess.run(
        [_npx(), "playwright", "test", "--list", "--project=chromium", "--reporter=json"],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    stdout = result.stdout or ""
    brace = stdout.find("{")
    if result.returncode != 0 or brace < 0:
        raise SystemExit(
            f"playwright --list failed (exit {result.returncode}).\n"
            f"--- stdout ---\n{stdout[:2000]}\n--- stderr ---\n{(result.stderr or '')[:2000]}"
        )
    report = json.loads(stdout[brace:])

    counts: dict[str, int] = {}

    def walk(node: dict) -> None:
        for spec in node.get("specs", []):
            counts[spec["file"]] = counts.get(spec["file"], 0) + 1
        for child in node.get("suites", []):
            walk(child)

    for suite in report.get("suites", []):
        counts.setdefault(suite["file"], 0)
        walk(suite)

    if not counts:
        raise SystemExit("playwright --list produced no specs; refusing to write an empty inventory.")
    return counts


def required_functional_specs() -> list[str]:
    """The spec list the required E2E Functional gate actually runs, read from ci.yml.

    Derived, never typed: if a spec joins or leaves the shard matrix, the
    inventory follows on the next regeneration.
    """
    text = CI_WORKFLOW.read_text(encoding="utf-8")
    lines = text.splitlines()

    start = None
    for index, line in enumerate(lines):
        if line.rstrip() == f"  {FUNCTIONAL_SHARD_JOB}:":
            start = index
            break
    if start is None:
        raise SystemExit(
            f"Could not find the `{FUNCTIONAL_SHARD_JOB}:` job in {CI_WORKFLOW.name}. "
            "If the job was renamed, update FUNCTIONAL_SHARD_JOB here — and check whether "
            "the rename orphaned a branch-protection context (see TESTING_STRATEGY_PLANNING.md 8.3)."
        )

    end = len(lines)
    for index in range(start + 1, len(lines)):
        if re.match(r"^  [A-Za-z0-9_-]+:\s*$", lines[index]):
            end = index
            break

    block = "\n".join(lines[start:end])
    specs = sorted(set(re.findall(r"e2e/([A-Za-z0-9._-]+\.spec\.ts)", block)))
    if not specs:
        raise SystemExit(f"No spec files found inside the `{FUNCTIONAL_SHARD_JOB}` job block.")
    return specs


# --------------------------------------------------------------------------
# pytest
# --------------------------------------------------------------------------

def collect_pytest() -> dict[str, int]:
    """Return {test file path: collected node count}, POSIX-separated."""
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest", "tests",
            "--collect-only", "-q", "--no-header", "-p", "no:cacheprovider",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    stdout = result.stdout or ""
    if result.returncode != 0:
        raise SystemExit(
            f"pytest --collect-only failed (exit {result.returncode}).\n"
            f"--- stdout ---\n{stdout[-4000:]}\n--- stderr ---\n{(result.stderr or '')[-2000:]}"
        )

    counts: dict[str, int] = {}
    for raw in stdout.splitlines():
        line = raw.strip()
        match = re.match(r"^(tests[/\\][^:]+\.py)::", line)
        if match:
            path = match.group(1).replace("\\", "/")
            counts[path] = counts.get(path, 0) + 1

    reported = re.search(r"(\d+) tests? collected", stdout)
    if reported is None:
        raise SystemExit(f"Could not find pytest's collected-count line.\n{stdout[-2000:]}")
    total = sum(counts.values())
    if total != int(reported.group(1)):
        raise SystemExit(
            f"Parsed {total} pytest node IDs but pytest reported {reported.group(1)}. "
            "The output format changed; fix the parser rather than committing a wrong number."
        )
    return counts


# --------------------------------------------------------------------------
# Hard waits
# --------------------------------------------------------------------------

def collect_hard_waits() -> dict[str, int]:
    """Lines containing `waitForTimeout` per e2e TypeScript file.

    Lines, not occurrences: this reproduces `rg -n waitForTimeout e2e -g '*.ts'`,
    the command section 7.2 recorded, so the two numbers stay comparable.
    """
    counts: dict[str, int] = {}
    for path in sorted((REPO_ROOT / "e2e").rglob("*.ts")):
        relative = path.relative_to(REPO_ROOT).as_posix()
        hits = sum(1 for line in path.read_text(encoding="utf-8").splitlines() if "waitForTimeout" in line)
        if hits:
            counts[relative] = hits
    return counts


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def build_inventory() -> dict:
    playwright_counts = collect_playwright()
    required_specs = required_functional_specs()
    pytest_counts = collect_pytest()
    hard_waits = collect_hard_waits()

    unknown = [spec for spec in required_specs if spec not in playwright_counts]
    if unknown:
        raise SystemExit(
            "ci.yml runs spec files Playwright does not list: " + ", ".join(unknown)
        )

    # A listed file that no longer collects anything means the allowlist has gone
    # stale and is now hiding a file instead of describing one.
    stale = [path for path in ENVIRONMENT_DEPENDENT_PYTEST_FILES if path not in pytest_counts]
    if stale:
        raise SystemExit(
            "ENVIRONMENT_DEPENDENT_PYTEST_FILES lists files pytest did not collect: "
            + ", ".join(stale)
            + ". Remove the entry rather than leaving it to suppress a real count."
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "generator": "scripts/generate_test_inventory.py",
        "playwright": {
            "project": "chromium",
            "total_tests": sum(playwright_counts.values()),
            "total_spec_files": len(playwright_counts),
            "required_functional_set": {
                "gate": "E2E Functional (Chromium)",
                "spec_files": len(required_specs),
                "tests": sum(playwright_counts[spec] for spec in required_specs),
            },
            "specs": [
                {
                    "spec": spec,
                    "tests": playwright_counts[spec],
                    "in_required_functional_set": spec in set(required_specs),
                }
                for spec in sorted(playwright_counts)
            ],
        },
        "pytest": {
            "collected_deterministic": sum(
                count for path, count in pytest_counts.items()
                if path not in ENVIRONMENT_DEPENDENT_PYTEST_FILES
            ),
            "deterministic_files": len(
                [path for path in pytest_counts if path not in ENVIRONMENT_DEPENDENT_PYTEST_FILES]
            ),
            "total_files": len(pytest_counts),
            "environment_dependent_files": [
                {"file": path, "reason": reason}
                for path, reason in sorted(ENVIRONMENT_DEPENDENT_PYTEST_FILES.items())
            ],
            "files": [
                {
                    "file": path,
                    "tests": (
                        None if path in ENVIRONMENT_DEPENDENT_PYTEST_FILES else pytest_counts[path]
                    ),
                }
                for path in sorted(pytest_counts)
            ],
        },
        "hard_waits": {
            "metric": "lines containing waitForTimeout",
            "total_lines": sum(hard_waits.values()),
            "files_with_waits": len(hard_waits),
            "files": [{"file": path, "lines": hard_waits[path]} for path in sorted(hard_waits)],
        },
    }


def render_json(inventory: dict) -> str:
    return json.dumps(inventory, indent=2, sort_keys=True) + "\n"


def render_markdown(inventory: dict) -> str:
    pw = inventory["playwright"]
    py = inventory["pytest"]
    waits = inventory["hard_waits"]

    out: list[str] = []
    out.append("# Test inventory (generated — do not hand-edit)")
    out.append("")
    out.append("Produced by `scripts/generate_test_inventory.py`. Regenerate with:")
    out.append("")
    out.append("```bash")
    out.append(".venv/Scripts/python.exe scripts/generate_test_inventory.py")
    out.append("```")
    out.append("")
    out.append(
        "Every test count in this repository's prose should link here rather than restate a "
        "number. See `docs/TESTING_STRATEGY_PLANNING.md` blindspot B3 for what happened the "
        "last time counts were maintained by hand."
    )
    out.append("")
    out.append("## Totals")
    out.append("")
    out.append("| Metric | Value |")
    out.append("|---|---|")
    out.append(f"| Playwright tests (chromium) | **{pw['total_tests']}** |")
    out.append(f"| Playwright spec files | **{pw['total_spec_files']}** |")
    out.append(
        f"| Required functional gate — `{pw['required_functional_set']['gate']}` | "
        f"**{pw['required_functional_set']['tests']}** tests across "
        f"{pw['required_functional_set']['spec_files']} specs |"
    )
    out.append(
        f"| pytest collected nodes (deterministic subset) | **{py['collected_deterministic']}** "
        f"across {py['deterministic_files']} files |"
    )
    out.append(f"| pytest test files (all) | **{py['total_files']}** |")
    out.append(
        f"| Hard waits ({waits['metric']}) | **{waits['total_lines']}** across "
        f"{waits['files_with_waits']} files |"
    )
    out.append("")
    out.append(
        "The required-functional figure is derived from the `e2e-functional-shard` job in "
        "`.github/workflows/ci.yml`, not typed in, so it cannot disagree with what CI runs."
    )
    out.append("")
    out.append("## Playwright specs")
    out.append("")
    out.append("| Spec | Tests | In required functional set |")
    out.append("|---|---:|:---:|")
    for row in pw["specs"]:
        mark = "yes" if row["in_required_functional_set"] else "—"
        out.append(f"| `{row['spec']}` | {row['tests']} | {mark} |")
    out.append("")
    out.append("## pytest files")
    out.append("")
    out.append(
        "`env-dependent` marks a file whose collected count varies with the machine, not the "
        "code. Those counts are deliberately not committed — a committed number would report "
        "drift on every host that differs from whoever regenerated last — so the headline total "
        "above is the deterministic subset and reproduces byte-for-byte on Windows and Linux."
    )
    out.append("")
    for row in inventory["pytest"]["environment_dependent_files"]:
        out.append(f"- **`{row['file']}`** — {row['reason']}")
    out.append("")
    out.append("| File | Collected |")
    out.append("|---|---:|")
    for row in py["files"]:
        value = "env-dependent" if row["tests"] is None else row["tests"]
        out.append(f"| `{row['file']}` | {value} |")
    out.append("")
    out.append("## Hard waits by file")
    out.append("")
    out.append(
        "Flake-and-latency debt (blindspot B5). Phase 5 step 16 burns this down worst-file-first; "
        "this table is the tracker."
    )
    out.append("")
    out.append("| File | Lines with `waitForTimeout` |")
    out.append("|---|---:|")
    for row in waits["files"]:
        out.append(f"| `{row['file']}` | {row['lines']} |")
    out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def _normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _check(path: Path, expected: str) -> bool:
    if not path.exists():
        print(f"DRIFT: {path.relative_to(REPO_ROOT).as_posix()} does not exist.")
        return False
    actual = _normalize(path.read_text(encoding="utf-8"))
    if actual == _normalize(expected):
        return True
    relative = path.relative_to(REPO_ROOT).as_posix()
    print(f"DRIFT: {relative} differs from freshly generated output.")
    diff = difflib.unified_diff(
        actual.splitlines(),
        _normalize(expected).splitlines(),
        fromfile=f"{relative} (committed)",
        tofile=f"{relative} (regenerated)",
        lineterm="",
    )
    for line in list(diff)[:200]:
        print(line)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Regenerate in memory and diff against the committed files; exit 1 on drift.",
    )
    args = parser.parse_args()

    inventory = build_inventory()
    json_text = render_json(inventory)
    markdown_text = render_markdown(inventory)

    if args.check:
        ok = _check(JSON_PATH, json_text) & _check(MARKDOWN_PATH, markdown_text)
        if ok:
            print("Test inventory is up to date.")
            return 0
        print(
            "\nRegenerate with `python scripts/generate_test_inventory.py` and commit the result."
        )
        return 1

    _write(JSON_PATH, json_text)
    _write(MARKDOWN_PATH, markdown_text)
    print(f"Wrote {JSON_PATH.relative_to(REPO_ROOT).as_posix()}")
    print(f"Wrote {MARKDOWN_PATH.relative_to(REPO_ROOT).as_posix()}")
    pw = inventory["playwright"]
    py = inventory["pytest"]
    print(
        f"  playwright: {pw['total_tests']} tests / {pw['total_spec_files']} specs "
        f"({pw['required_functional_set']['tests']} required-functional)"
    )
    print(
        f"  pytest:     {py['collected_deterministic']} collected / "
        f"{py['deterministic_files']} files (deterministic subset; "
        f"{py['total_files'] - py['deterministic_files']} env-dependent file(s) excluded)"
    )
    print(f"  hard waits: {inventory['hard_waits']['total_lines']} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
