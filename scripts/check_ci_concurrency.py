"""Prove the ci.yml concurrency group cannot cancel a push-triggered run.

On 2026-08-01 the non-PR key was `github.ref`, which gave every push to main one
shared concurrency group. Paired with `cancel-in-progress: false` -- believed at
the time to mean "never cancelled" -- it silently discarded post-merge
validation: WPB.4 (`9fe5dbd`) was cancelled while still QUEUED and ran zero jobs.

cancel-in-progress only governs runs that are already in progress. A run still
queued in an occupied group is cancelled when a newer run joins that group.
So the guarantee has to come from the KEY being unique per push, not from the
flag.

This script evaluates the committed expression against synthetic GitHub event
contexts and asserts the three properties that matter. It is deliberately a
property check rather than a string comparison, so it keeps working if the
expression is rewritten in some other equivalent form.

Usage:
    python scripts/check_ci_concurrency.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CI = REPO_ROOT / ".github" / "workflows" / "ci.yml"


def extract_concurrency() -> tuple[str, str]:
    """Pull the raw `group:` and `cancel-in-progress:` expressions out of ci.yml."""
    text = CI.read_text(encoding="utf-8")
    block = re.search(
        r"^concurrency:\n((?:[ \t]+.*\n)+)", text, re.M
    )
    if block is None:
        raise SystemExit("No top-level `concurrency:` block found in ci.yml.")
    body = block.group(1)

    group = re.search(r"^\s*group:\s*(.+?)\s*$", body, re.M)
    cancel = re.search(r"^\s*cancel-in-progress:\s*(.+?)\s*$", body, re.M)
    if group is None or cancel is None:
        raise SystemExit("concurrency block is missing `group:` or `cancel-in-progress:`.")
    return group.group(1), cancel.group(1)


def evaluate(expression: str, ctx: dict[str, str | None]) -> str:
    """Evaluate a GitHub `${{ ... }}` template against a synthetic context.

    Supports exactly what this expression needs: context lookups, the `||`
    fallback (falsy = None or empty), and `==` comparison.
    """

    def resolve(token: str) -> str | None:
        token = token.strip()
        if token.startswith("'") and token.endswith("'"):
            return token[1:-1]
        return ctx.get(token)

    def eval_inner(src: str) -> str:
        if "==" in src:
            left, right = src.split("==", 1)
            return "true" if resolve(left) == resolve(right) else "false"
        for part in src.split("||"):
            value = resolve(part)
            if value:
                return value
        return ""

    return re.sub(
        r"\$\{\{(.+?)\}\}", lambda m: eval_inner(m.group(1)), expression
    )


def context(event: str, *, pr: str | None = None, ref: str, run_id: str) -> dict[str, str | None]:
    return {
        "github.workflow": "CI/CD Pipeline",
        "github.event_name": event,
        "github.event.pull_request.number": pr,
        "github.ref": ref,
        "github.run_id": run_id,
    }


def main() -> int:
    group_expr, cancel_expr = extract_concurrency()
    print(f"group:               {group_expr}")
    print(f"cancel-in-progress:  {cancel_expr}\n")

    failures: list[str] = []

    def require(condition: bool, message: str) -> None:
        print(("  OK   " if condition else "  FAIL ") + message)
        if not condition:
            failures.append(message)

    # --- Property 1: two runs of the SAME pull request share a key, and cancel.
    pr_a = evaluate(group_expr, context("pull_request", pr="241", ref="refs/pull/241/merge", run_id="1001"))
    pr_b = evaluate(group_expr, context("pull_request", pr="241", ref="refs/pull/241/merge", run_id="1002"))
    pr_cancel = evaluate(cancel_expr, context("pull_request", pr="241", ref="refs/pull/241/merge", run_id="1002"))
    print("Property 1 - same PR, two pushes:")
    require(pr_a == pr_b, f"share one key ({pr_a})")
    require(pr_cancel == "true", "cancel-in-progress is true, so the older run is superseded")

    # --- Property 2: different pull requests never share a key.
    pr_other = evaluate(group_expr, context("pull_request", pr="239", ref="refs/pull/239/merge", run_id="1003"))
    print("\nProperty 2 - two different PRs:")
    require(pr_a != pr_other, f"distinct keys ({pr_a} vs {pr_other})")

    # --- Property 3: separate pushes to main get DIFFERENT keys.
    push_1 = evaluate(group_expr, context("push", ref="refs/heads/main", run_id="2001"))
    push_2 = evaluate(group_expr, context("push", ref="refs/heads/main", run_id="2002"))
    push_3 = evaluate(group_expr, context("push", ref="refs/heads/main", run_id="2003"))
    push_cancel = evaluate(cancel_expr, context("push", ref="refs/heads/main", run_id="2002"))
    print("\nProperty 3 - three separate pushes to main:")
    require(
        len({push_1, push_2, push_3}) == 3,
        f"three distinct keys ({push_1}, {push_2}, {push_3})",
    )
    require(push_cancel == "false", "cancel-in-progress is false for push events")

    # --- Property 4: the regression itself. A queued push run can only be
    # cancelled if it shares a group with a newer push run. Distinct keys make
    # that impossible, which is the guarantee cancel-in-progress does NOT give.
    print("\nProperty 4 - a push run cannot cancel another push run:")
    require(
        push_1 != push_2,
        "no two main pushes ever occupy the same group, so none can be queued behind another",
    )
    require(
        evaluate(group_expr, context("push", ref="refs/heads/develop", run_id="2004")) != push_1,
        "develop pushes are also independent",
    )

    # --- Property 5: workflow scoping survives (7.3 entry criterion 4).
    print("\nProperty 5 - workflow scoping:")
    require(push_1.startswith("CI/CD Pipeline"), "key is prefixed with the workflow name")
    deep_gate = context("workflow_dispatch", ref="refs/heads/main", run_id="2001")
    deep_gate["github.workflow"] = "Deep Gate (manual)"
    require(
        evaluate(group_expr, deep_gate) != push_1,
        "a Deep Gate run never shares a key with a CI/CD Pipeline run",
    )

    print()
    if failures:
        print(f"{len(failures)} property FAILED:")
        for f in failures:
            print("  - " + f)
        return 1
    print("All concurrency properties hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
