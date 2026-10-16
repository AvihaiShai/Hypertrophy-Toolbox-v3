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
STATUS_COMMAND = COMMANDS / "status.md"

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
    REPO / "AGENTS.md",
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


def test_status_uses_object_ids_instead_of_disabling_msys_conversion() -> None:
    """Historical blob reads must not disable Git for Windows path conversion."""
    status = read(STATUS_COMMAND)
    assert "MSYS_NO_PATHCONV=" not in status
    assert "MSYS2_ARG_CONV_EXCL=" not in status
    assert "git ls-tree" in status
    assert "git cat-file blob" in status


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


FRONTMATTER = re.compile(r"\A---\r?\n(.*?)^---[ \t]*\r?$", re.DOTALL | re.MULTILINE)
SHELL_TOOLS = ("Bash", "PowerShell")
# Flow style, a comment, a flow mapping or an anchor. This parser does not read
# them, and "not read" has to mean "assume every tool".
UNREADABLE_TOOLS_VALUE = re.compile(r"[\[\]{}#&]")
SEQUENCE_ITEM = re.compile(r"^[ \t]*-[ \t]")
MATCHER_VALUE = re.compile(r"^[ \t]*-?[ \t]*matcher:[ \t]*(.*)$", re.MULTILINE)
# Either quote style. The single-quoted form legitimately contains the double
# quotes around ${CLAUDE_PROJECT_DIR}, so the delimiter cannot be excluded from
# the body.
QUOTED_COMMAND = re.compile(r"""command:[ \t]*(?:'([^'\n]*)'|"([^"\n]*)")""")
# PowerShell binds parameter names case-insensitively, by unambiguous prefix,
# and with a colon as well as whitespace before the value: -G main, -Gu MAIN and
# -GuardProfile:main all reach $GuardProfile.
# The value group is optional so that a parameter given with NO value is still
# seen: it does not bind, and PowerShell's exit 1 on the binding error is
# non-blocking, so such a registration fails open rather than defaulting.
PROFILE_ARGUMENT = re.compile(r"""-([A-Za-z]+)(?:[ \t]*[:\s][ \t]*['"]?([A-Za-z]*))?""")


def frontmatter(content: str, name: str) -> str:
    found = FRONTMATTER.search(content)
    assert found is not None, name + " has no YAML frontmatter"
    return found.group(1)


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip())


def split_outside_parens(value: str) -> list[str]:
    """Split a tools-style list on commas that are not inside parentheses.

    `Agent(product-manager, senior-developer)` is one tool carrying an argument
    list, not three tools.
    """
    items: list[str] = []
    depth = 0
    current = ""
    for char in value:
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        if char == "," and depth == 0:
            items.append(current)
            current = ""
        else:
            current += char
    items.append(current)
    return [item.strip().strip("\"'") for item in items if item.strip()]


def declared_tools(block: str, key: str) -> set[str] | None:
    """Tool names under a top-level `key:`, or None for "assume every tool".

    None is returned for an absent key -- a charter with no `tools:` inherits
    everything -- and for any value this parser cannot fully read: a duplicate
    key (YAML takes the last), flow style `[Read, Bash]`, a trailing `# comment`,
    an anchor or alias, a wildcard, or a key with nothing readable under it.
    Both answers mean the same thing to the caller, and that is the fail-closed
    direction: an unread `tools:` must never be mistaken for "no shell". Written
    by hand because PyYAML is not a dependency of this repository.
    """
    lines = block.splitlines()
    head = re.compile(r"^" + re.escape(key) + r":[ \t]*(.*)$")
    found = [
        (index, match)
        for index, match in ((i, head.match(line)) for i, line in enumerate(lines))
        if match is not None
    ]
    if len(found) != 1:
        return None
    index, match = found[0]
    inline = match.group(1).strip()
    if UNREADABLE_TOOLS_VALUE.search(inline):
        return None
    items = split_outside_parens(inline)
    for candidate in lines[index + 1:]:
        if not candidate.strip():
            continue
        # Only an indented `- ` item continues this key. The next top-level key,
        # a nested mapping such as `mcpServers:`, or a sequence written at column
        # zero all end it -- and the last of those leaves `items` empty, which is
        # why an empty result has to be None rather than "no tools".
        if not SEQUENCE_ITEM.match(candidate) or indent_of(candidate) == 0:
            break
        items.extend(split_outside_parens(candidate.split("-", 1)[1]))
    if not items or any(item.startswith("*") for item in items):
        return None
    return {item.split("(", 1)[0].strip() for item in items}


def granted_shell_tools(content: str, name: str) -> set[str]:
    """Which of Bash and PowerShell this charter can reach.

    `disallowedTools` deliberately does not subtract. No charter in this
    repository names a tool in both keys, so its precedence over an explicit
    `tools:` grant is unobservable here, and treating it as a denial would
    exempt `tools: Bash` + `disallowedTools: Bash` from carrying the hook on an
    unverified premise. Failing closed costs one hook line on a charter that
    never shells.
    """
    granted = declared_tools(frontmatter(content, name), "tools")
    if granted is None:
        return set(SHELL_TOOLS)
    return {tool for tool in SHELL_TOOLS if tool in granted}


def pre_tool_use_block(block: str) -> str:
    """The `PreToolUse:` section of a charter's `hooks:` mapping.

    Only PreToolUse can block a call. A guard registered under PostToolUse runs
    after the tool has already executed, so its exit 2 prevents nothing -- and
    reads as a present, correctly matched hook.
    """
    lines = block.splitlines()
    for index, line in enumerate(lines):
        if not re.match(r"^[ \t]*PreToolUse:[ \t]*$", line):
            continue
        depth = indent_of(line)
        end = len(lines)
        for offset in range(index + 1, len(lines)):
            if lines[offset].strip() and indent_of(lines[offset]) <= depth:
                end = offset
                break
        return "\n".join(lines[index + 1:end])
    return ""


def hook_entries(section: str) -> list[str]:
    """Top-level sequence items of a hook section, each as one text block."""
    lines = section.splitlines()
    starts = [index for index, line in enumerate(lines) if SEQUENCE_ITEM.match(line)]
    if not starts:
        return []
    base = min(indent_of(lines[index]) for index in starts)
    starts = [index for index in starts if indent_of(lines[index]) == base]
    bounds = starts + [len(lines)]
    return ["\n".join(lines[bounds[i]:bounds[i + 1]]) for i in range(len(starts))]


def matcher_covers(value: str | None, required: set[str]) -> bool:
    """Whether a matcher routes every shell tool the charter grants.

    An entry with no `matcher` matches every tool, so it covers. A matcher is an
    alternation, so `"Edit|Write|Bash|PowerShell"` covers as fully as
    `"Bash|PowerShell"` -- membership, not string equality.
    """
    if value is None:
        return True
    alternatives = {part.strip().strip("\"'") for part in value.split("|")}
    return required <= alternatives


def guard_commands(text: str) -> list[str]:
    return [
        single or double
        for single, double in QUOTED_COMMAND.findall(text)
        if "guard-destructive-command.ps1" in (single or double)
    ]


def shell_hook_commands(block: str, name: str, required: set[str]) -> list[str]:
    """Guard commands that actually sit in front of this charter's shell calls.

    Scoped to one PreToolUse entry whose matcher covers the granted shell tools.
    Two independent whole-file searches -- one for the matcher, one for the
    command -- accept a charter whose shell matcher carries an unrelated hook
    while the destructive guard sits under `matcher: "Skill"` or under
    PostToolUse, and then enrol it as a live registration.
    """
    section = pre_tool_use_block(block)
    covering: list[str] = []
    stray: list[str] = []
    for entry in hook_entries(section):
        matcher = MATCHER_VALUE.search(entry)
        target = covering if matcher_covers(matcher.group(1).strip() if matcher else None, required) else stray
        target.extend(guard_commands(entry))
    accounted = sum(len(guard_commands(entry)) for entry in hook_entries(section))
    elsewhere = len(guard_commands(block)) - accounted
    assert not stray and elsewhere == 0, (
        name + " registers the destructive guard where it cannot gate a shell "
        "call -- outside PreToolUse, or under a matcher that does not cover "
        + ", ".join(sorted(required))
    )
    return covering


def resolved_profile(command: str) -> str:
    """The profile this registration actually selects at run time.

    `"-GuardProfile main" not in command` is not that question. PowerShell
    resolves `-G main`, `-Gu MAIN` and `-GuardProfile:main` to the same
    permissive profile, so a charter can register the owner profile and still
    read as if it had not. A parameter given with no value does not bind at all:
    PowerShell exits 1 on the binding error, which is non-blocking, so that
    registration fails OPEN and is reported as such rather than as `agent`.
    """
    for name, value in PROFILE_ARGUMENT.findall(command):
        if "guardprofile".startswith(name.lower()):
            return value.lower() or "<missing value>"
    return "agent"  # the guard's param() default


def destructive_registrations(settings=None, charters=None):
    """Resolve actual registrations and reject missing/misrouted hook wiring."""
    settings = settings if settings is not None else json.loads(read(REPO / ".claude/settings.json"))
    if charters is None:
        # committed_markdown, not a bare glob: `.claude/agents/*.local.md` is not
        # gitignored, so an uncommitted charter could otherwise green or red this
        # contract from one machine.
        charters = {p.name: read(p) for p in committed_markdown(AGENTS.glob("*.md"))}
    registrations = []
    for registration in settings.get("hooks", {}).get("PreToolUse", []):
        if "Bash" in registration.get("matcher", "") and "PowerShell" in registration.get("matcher", ""):
            for hook in registration.get("hooks", []):
                if "guard-destructive-command.ps1" in hook.get("command", ""):
                    registrations.append(("project", hook["command"], "main"))
    assert len(registrations) == 1, "Project shell destructive hook missing or ambiguous"
    for name, content in charters.items():
        required = granted_shell_tools(content, name)
        if not required:
            continue
        commands = shell_hook_commands(frontmatter(content, name), name, required)
        assert len(commands) == 1, name + " missing or ambiguous destructive hook"
        registrations.append((name, commands[0], "agent"))
    for name, command, profile in registrations:
        assert "${CLAUDE_PROJECT_DIR}/.claude/hooks/guard-destructive-command.ps1" in command, name
        actual = resolved_profile(command)
        assert actual == profile, (
            f"{name} resolves to the {actual} profile where {profile} is required"
        )
    return registrations


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("permission", ("default", "bypassPermissions"))
def test_all_effective_destructive_registrations_execute_deny_allow(host, permission):
    if shutil.which(host) is None:
        pytest.skip(f"{host} unavailable")
    for name, command, profile in destructive_registrations():
        # Execute each resolved installed command, retaining its declared arguments.
        resolved = command.replace("${CLAUDE_PROJECT_DIR}", str(REPO))
        host_prefix = "& '" + str(shutil.which(host)).replace("'", "''") + "'"
        resolved = re.sub(r"^powershell\b", lambda _: host_prefix, resolved)
        probes = (
            ("MSYS2_ARG_CONV_EXCL=0 echo inert", 2),
            ("git status --short", 0),
            # The other two rows behave identically under both profiles, so they
            # cannot tell an agent registration from an owner one. This one can.
            ("git push origin HEAD", 2 if profile == "agent" else 0),
        )
        for inert, expected in probes:
            # The outer harness shell must preserve the registered child's exact
            # exit code; PowerShell -Command otherwise maps any nonzero to 1.
            result = subprocess.run([host, "-NoProfile", "-Command", resolved + "; exit $LASTEXITCODE"], input=json.dumps({
                "permission_mode": permission, "tool_input": {"command": inert}}),
                capture_output=True, text=True, timeout=20)
            assert result.returncode == expected, (name, profile, result.stdout, result.stderr)


# The four original arms, and the assertion each must raise. Without `match=`,
# an arm is satisfied by any AssertionError -- including one from an unrelated
# charter or a different rule.
MUTATION_REASONS = {
    "remove_project": "Project shell destructive hook missing or ambiguous",
    "misroute_project": "Project shell destructive hook missing or ambiguous",
    "remove_agent": "missing or ambiguous destructive hook",
    "main_agent": "resolves to the main profile",
}

NO_HOOK = "rogue.md missing or ambiguous destructive hook"
MISROUTED = "cannot gate a shell call"


def _rogue(frontmatter_body: str) -> str:
    return "---\nname: rogue\ndescription: d\n" + frontmatter_body + "---\n\nbody\n"


def _rogue_hook(matcher: str, argument: str = "", event: str = "PreToolUse") -> str:
    return _rogue(
        "tools: Read, Bash\nhooks:\n"
        f"  {event}:\n"
        f"    - matcher: {matcher}\n"
        "      hooks:\n"
        "        - type: command\n"
        "          command: 'powershell -File \"${CLAUDE_PROJECT_DIR}/.claude/hooks/"
        "guard-destructive-command.ps1\"" + argument + "'\n"
    )


# Charter shapes that reach a shell in the harness. The first group ships no
# effective guard at all; the second ships a hook that cannot gate a shell call;
# the third ships one that hands the charter the permissive owner profile. Every
# one of them read green before the predicate was rewritten.
UNGUARDED_CHARTERS = {
    # No `tools:` key, so the charter inherits every tool, Bash included.
    "no_tools_key": (_rogue("model: inherit\n"), NO_HOOK),
    "wildcard_tools": (_rogue('tools: "*"\n'), NO_HOOK),
    "block_sequence_tools": (_rogue("tools:\n  - Read\n  - Bash\n"), NO_HOOK),
    "flow_sequence_tools": (_rogue("tools: [Read, Bash]\n"), NO_HOOK),
    "commented_tools": (_rogue("tools: Read, Bash  # shell for the test runner\n"), NO_HOOK),
    "zero_indent_sequence_tools": (_rogue("tools:\n- Read\n- Bash\n"), NO_HOOK),
    # YAML takes the last key; a reader that takes the first sees no shell.
    "duplicate_tools_key": (_rogue("tools: Read\ntools: Read, Bash\n"), NO_HOOK),
    "empty_tools_value": (_rogue("tools:\n"), NO_HOOK),
    # The shell matcher carries an unrelated hook while the destructive guard
    # sits where no shell call reaches it.
    "hook_under_wrong_matcher": (
        _rogue(
            "tools: Read, Bash\nhooks:\n  PreToolUse:\n"
            '    - matcher: "Bash|PowerShell"\n'
            "      hooks:\n"
            "        - type: command\n"
            "          command: 'powershell -File \"${CLAUDE_PROJECT_DIR}/.claude/hooks/guard-skill.ps1\"'\n"
            '    - matcher: "Skill"\n'
            "      hooks:\n"
            "        - type: command\n"
            "          command: 'powershell -File \"${CLAUDE_PROJECT_DIR}/.claude/hooks/"
            "guard-destructive-command.ps1\"'\n"
        ),
        MISROUTED,
    ),
    # PostToolUse runs after the call, so exit 2 prevents nothing.
    "hook_under_wrong_event": (_rogue_hook('"Bash|PowerShell"', event="PostToolUse"), MISROUTED),
    # A charter may not hand itself the owner profile. PowerShell matches
    # parameter names case-insensitively, by unambiguous prefix, and with a
    # colon as well as whitespace before the value.
    "cased_main_profile": (_rogue_hook('"Bash|PowerShell"', " -GuardProfile MAIN"), MUTATION_REASONS["main_agent"]),
    "abbreviated_main_profile": (_rogue_hook('"Bash|PowerShell"', " -G main"), MUTATION_REASONS["main_agent"]),
    "colon_main_profile": (_rogue_hook('"Bash|PowerShell"', " -GuardProfile:main"), MUTATION_REASONS["main_agent"]),
    "colon_abbreviated_main_profile": (_rogue_hook('"Bash|PowerShell"', " -G:main"), MUTATION_REASONS["main_agent"]),
    # No value binds nothing: PowerShell exits 1 on the binding error, which is
    # non-blocking, so this registration fails OPEN.
    "profile_argument_without_a_value": (
        _rogue_hook('"Bash|PowerShell"', " -GuardProfile"),
        "resolves to the <missing value> profile",
    ),
}

# This file's collected node count is identical before and after the predicate
# hardening -- the arms exist in both states -- so no count-based check can tell
# them apart. Resolving one registration at import time can: an unhardened copy
# of this file has no `resolved_profile`, so it fails at COLLECTION rather than
# silently shipping with the arms red.
assert resolved_profile(_rogue_hook('"Bash|PowerShell"', " -G:main")) == "main"


@pytest.mark.parametrize("mutation", (*MUTATION_REASONS, *UNGUARDED_CHARTERS))
def test_missing_or_misrouted_registration_is_detected(mutation):
    settings = json.loads(read(REPO / ".claude/settings.json"))
    charters = {p.name: read(p) for p in committed_markdown(AGENTS.glob("*.md"))}
    if mutation == "remove_project":
        settings["hooks"]["PreToolUse"] = []
    elif mutation == "misroute_project":
        settings = json.loads(json.dumps(settings).replace("guard-destructive-command.ps1", "guard-skill.ps1"))
    elif mutation == "remove_agent":
        charters["automation-qa.md"] = charters["automation-qa.md"].replace("guard-destructive-command.ps1", "guard-skill.ps1")
    elif mutation == "main_agent":
        charters["automation-qa.md"] = charters["automation-qa.md"].replace('guard-destructive-command.ps1"', 'guard-destructive-command.ps1" -GuardProfile main')
    else:
        charters["rogue.md"] = UNGUARDED_CHARTERS[mutation][0]
    reason = MUTATION_REASONS.get(mutation) or UNGUARDED_CHARTERS[mutation][1]
    with pytest.raises(AssertionError, match=re.escape(reason)):
        destructive_registrations(settings, charters)


def test_snapshot_exception_is_named_and_keeps_application_rules():
    root = read(REPO / "CLAUDE.md")
    db_rule = read(REPO / ".claude/rules/database.md")
    for text in (root, db_rule):
        assert "seed_worktree_snapshot.py" in text
        assert "DatabaseHandler" in text
    assert len(root.splitlines()) < 200
    assert "get_logger()" in root
