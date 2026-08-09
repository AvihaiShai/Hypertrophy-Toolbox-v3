"""Contracts that keep the committed agent configuration consistent with itself.

Two defects motivated this file. Neither was reachable by any existing gate,
because every file involved is Markdown and no gate reads prose:

1. `senior-developer` was permitted to invoke `/verify-and-polish` but not the
   `/handover` that command names as its own step 4. The agent could start a
   command it was allowed to run and be blocked partway through -- after step 1
   had already spent a full pytest + Chromium run.
2. Eleven sites across eight files told a reader to act "per
   `.claude/SHARED_PLAN.md` Tier 2.1 / Appendix A1.1 / ...". That file is
   gitignored and absent, so the instruction resolved to nothing, and the
   numbering it asked readers to honor no longer mapped to anything.

Both are configuration truth rather than code, which is why they are asserted
here instead of being left to review.

Scope notes, all deliberate:

* **The surface is non-recursive.** Nested agent worktrees under
  `.claude/worktrees/` carry their own copies of these files; they are other
  checkouts' configuration, not this one's.
* **`docs/ai_workflow/*_PLAN.md` is excluded from the numbering check.** A
  proposal document owns whatever internal numbering it defines in its own text
  (`CROSS_MODEL_ORCHESTRATION_PLAN.md` builds in Tier 1/2/3). What an *authority*
  document may not do is import numbering from a file that does not exist.
* **Only a command's `## Steps` section is scanned for invocations.** A skill
  named in a "See also" or "Difference vs" section is a cross-reference, not
  something the agent will be stopped on mid-run.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from collections.abc import Iterable
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
COMMANDS = REPO / ".claude" / "commands"
AGENTS = REPO / ".claude" / "agents"
SKILLS = REPO / ".claude" / "skills"
GUARD = REPO / ".claude" / "hooks" / "guard-skill.ps1"

# Every authority document here has an optional gitignored local twin: the
# `.local.md` layer that PARALLEL_WORKFLOW.md tells a developer to put live
# workstream claims in, so claim churn stays out of git. `.gitignore` names
# today's two individually (MASTER_HANDOVER.local.md,
# WORKSTREAM_OWNERSHIP.local.md); the suffix is the convention behind both.
#
# Those files must not reach these contracts, for two separate reasons:
#
# * **Assertion scope.** This file asserts what the *committed* configuration
#   says. One machine's uncommitted scratch is not configuration truth, and
#   nothing it contains can be true of a fresh clone.
# * **Collection determinism**, which is the sharper hazard. SURFACE is
#   parametrized, so a filesystem glob makes this file's node count depend on
#   whatever happens to sit in those directories. That count feeds the committed
#   `docs/test_inventory/` artifact, so a purely local file reds
#   `--check` against an artifact that is in fact correct -- and the tempting
#   repair, regenerating, *corrupts* the artifact by baking the local file in.
#
# This is the same principle the HOSTS note below states: node count must not
# depend on the machine. `ENVIRONMENT_DEPENDENT_PYTEST_FILES` in
# scripts/generate_test_inventory.py exists to absorb variance that is genuinely
# by design; this variance was an accident, so it is removed rather than
# allowlisted.
LOCAL_ONLY_SUFFIX = ".local.md"


def committed_markdown(paths: Iterable[Path]) -> list[Path]:
    """Sorted committed-configuration Markdown, minus local-only layers."""
    return sorted(p for p in paths if not p.name.endswith(LOCAL_ONLY_SUFFIX))


SURFACE = [
    *committed_markdown(COMMANDS.glob("*.md")),
    *committed_markdown(AGENTS.glob("*.md")),
    *committed_markdown((REPO / ".claude" / "rules").glob("*.md")),
    *committed_markdown((REPO / "docs" / "ai_workflow").glob("*.md")),
    REPO / "CLAUDE.md",
]

# The one file permitted to name the retired plan file, and only to say it is
# retired. Removing that note would let a future session recreate the ghost.
ANTI_RECREATION_NOTE = REPO / "docs" / "ai_workflow" / "INDEX.md"

RETIRED_NUMBERING = re.compile(r"\bTier \d|\bAppendix A\d")
ALLOWED_CSV = re.compile(r"-AllowedCsv\s+([A-Za-z0-9,\-]+)")
STEPS_SECTION = re.compile(r"^## Steps$(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
# A slash command reference, never a path segment: `/handover` matches,
# `.claude/commands/handover.md` and `docs/ai_workflow/X.md` do not.
SLASH_COMMAND = re.compile(r"(?<![\w./-])/([a-z0-9][a-z0-9-]*)")

# Parametrized over both hosts unconditionally and skipped at *run* time, not
# collection time. Deciding this at collection would make the file's node count
# depend on the machine, which is what ENVIRONMENT_DEPENDENT_PYTEST_FILES in
# scripts/generate_test_inventory.py exists to absorb -- better not to need it.
HOSTS = ("powershell", "pwsh")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def invocable_names() -> set[str]:
    skills = {d.name for d in SKILLS.iterdir() if (d / "SKILL.md").is_file()}
    return skills | {p.stem for p in committed_markdown(COMMANDS.glob("*.md"))}


def allowlist(charter: Path) -> list[str]:
    found = ALLOWED_CSV.search(read(charter))
    if found is None:
        return []
    return [name.strip().lstrip("/") for name in found.group(1).split(",")]


def guarded_charters() -> list[Path]:
    return [p for p in committed_markdown(AGENTS.glob("*.md")) if allowlist(p)]


def step_invocations(command: Path) -> set[str]:
    section = STEPS_SECTION.search(read(command))
    if section is None:
        return set()
    known = invocable_names()
    return {name for name in SLASH_COMMAND.findall(section.group(1)) if name in known}


def surface_ids() -> list[str]:
    return [p.relative_to(REPO).as_posix() for p in SURFACE]


@pytest.mark.parametrize("path", SURFACE, ids=surface_ids())
def test_surface_does_not_direct_readers_to_the_retired_plan_file(path: Path) -> None:
    hits = [
        f"{path.relative_to(REPO).as_posix()}:{n}: {line.strip()}"
        for n, line in enumerate(read(path).splitlines(), start=1)
        if "SHARED_PLAN" in line
    ]
    if path == ANTI_RECREATION_NOTE:
        assert len(hits) == 1, (
            "INDEX.md may name the retired plan file exactly once, in the note "
            f"that says it is retired. Found {len(hits)}:\n" + "\n".join(hits)
        )
        return
    assert not hits, (
        ".claude/SHARED_PLAN.md does not exist and is gitignored. Point at the "
        "document that actually owns the rule -- see docs/ai_workflow/INDEX.md.\n"
        + "\n".join(hits)
    )


@pytest.mark.parametrize(
    "path",
    [p for p in SURFACE if not p.name.endswith("_PLAN.md")],
    ids=[p.relative_to(REPO).as_posix() for p in SURFACE if not p.name.endswith("_PLAN.md")],
)
def test_surface_does_not_use_the_retired_tier_numbering(path: Path) -> None:
    hits = [
        f"{path.relative_to(REPO).as_posix()}:{n}: {line.strip()}"
        for n, line in enumerate(read(path).splitlines(), start=1)
        if RETIRED_NUMBERING.search(line)
    ]
    assert not hits, (
        "The Tier / Appendix numbering was retired with .claude/SHARED_PLAN.md "
        "and resolves to nothing. Name the authority document instead.\n"
        + "\n".join(hits)
    )


def test_gitignore_still_blocks_a_tracked_shared_plan() -> None:
    """The backstop, not a leftover.

    The ignore rule is what keeps a local scratch copy from being committed and
    re-establishing the ghost authority as tracked truth.
    """
    lines = [line.strip() for line in read(REPO / ".gitignore").splitlines()]
    assert ".claude/SHARED_PLAN.md" in lines


def test_local_only_authority_layers_cannot_reach_these_contracts() -> None:
    """A gitignored ``*.local.md`` twin must not enter the parametrized surface.

    Asserted on the derivation rather than only on the result: checking SURFACE
    alone would pass vacuously on any machine that happens to have no local
    layer, which is every CI runner and so exactly the machine that cannot
    catch the regression.
    """
    leaked = [p.name for p in SURFACE if p.name.endswith(LOCAL_ONLY_SUFFIX)]
    assert not leaked, f"local-only layers reached SURFACE: {leaked}"

    committed = Path("docs/ai_workflow/WORKSTREAM_OWNERSHIP.md")
    local = Path("docs/ai_workflow/WORKSTREAM_OWNERSHIP.local.md")
    assert committed_markdown([committed, local]) == [committed]

    # The suffix rule reaches the other two derivations too, so a local twin can
    # neither invent a slash command nor add an agent charter.
    assert "WORKSTREAM_OWNERSHIP.local" not in invocable_names()


def test_every_surface_file_is_tracked_by_git() -> None:
    """Collection must not depend on any untracked file, local twin or not.

    The suffix rule above covers the documented convention. This is the general
    form: anything untracked in these directories changes this file's node
    count, which drifts the committed ``docs/test_inventory/`` artifact on one
    machine only. Failing here names the file; the fix is to commit it or to
    give it the ``.local.md`` suffix, never to regenerate the inventory around
    it.
    """
    if shutil.which("git") is None:
        pytest.skip("git not on PATH")

    listed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    )
    tracked = {entry for entry in listed.stdout.split("\0") if entry}

    untracked = [
        path.relative_to(REPO).as_posix()
        for path in SURFACE
        if path.relative_to(REPO).as_posix() not in tracked
    ]
    assert not untracked, (
        "untracked files are being collected as configuration surface, so this "
        "file's node count differs from a clean checkout: "
        + ", ".join(untracked)
        + ". Commit them, or name them *.local.md if they are local-only."
    )


@pytest.mark.parametrize(
    "charter", guarded_charters(), ids=[p.stem for p in guarded_charters()]
)
def test_allowed_commands_do_not_have_forbidden_steps(charter: Path) -> None:
    """An agent must not be able to start a command it cannot finish.

    This is the P1.3 regression: `/verify-and-polish` was allowed while the
    `/handover` it names as step 4 was not.
    """
    allowed = set(allowlist(charter))
    for name in sorted(allowed):
        command = COMMANDS / f"{name}.md"
        if not command.is_file():
            continue
        missing = step_invocations(command) - allowed
        assert not missing, (
            f"{charter.stem} may invoke /{name}, whose documented steps also "
            f"invoke {sorted('/' + m for m in missing)} -- not in its allowlist. "
            "The agent would be blocked partway through a command it was "
            "permitted to start."
        )


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize(
    ("skill", "expected"),
    [("handover", 0), ("verify-and-polish", 0), ("council-plan", 2), ("", 2)],
)
def test_skill_guard_decides_as_the_senior_developer_allowlist_says(
    host: str, skill: str, expected: int
) -> None:
    """Run the real hook with the real allowlist, on every host present.

    `test_guard_destructive_command.py` established why this is per-host: a
    guard green under pwsh 7 was a parser error under Windows PowerShell 5.1,
    which exits 1 -- a non-blocking code, so the hook failed open.
    """
    if shutil.which(host) is None:
        pytest.skip(f"{host} is not installed on this platform")
    csv = ",".join(allowlist(AGENTS / "senior-developer.md"))
    result = subprocess.run(
        [host, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(GUARD),
         "-AllowedCsv", csv],
        input=json.dumps({"tool_input": {"skill": skill}}),
        capture_output=True,
        text=True,
    )
    assert result.returncode == expected, (
        f"{host} skill={skill!r} exit={result.returncode} "
        f"(expected {expected})\n{result.stderr}"
    )
