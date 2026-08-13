"""The cross-model consult dry-run matrix.

Every row here drives the real adapter -- real `Popen`, real argv, real bytes,
real timeout -- against a fake CLI (`tests/fixtures/consult/fake_cli.py`) that
impersonates `claude` or `codex` deterministically. Live dual-CLI runs cost
money, vary between runs, and cannot execute on the Linux CI runner where
neither CLI is installed; the two live end-to-end smokes are recorded in
`docs/ai_workflow/CROSS_MODEL_ORCHESTRATION_PLAN.md` instead.

Two things the council specifically asked for, and why they are here:

* **Every row must be able to fail for its stated reason.** The mutations that
  prove that are listed in the plan's dry-run section. A row that no mutation
  can flip is a liability, so rows that could only have asserted a structural
  property of an `if` block were rewritten to assert an observable instead.
* **The fixture is the observation channel.** It appends its full argv and its
  environment key names to `CONSULT_FIXTURE_LOG` on every invocation, including
  `--version`. Without that, the argv-shape, path-handoff and credential rows
  would have nothing to assert against and would pass vacuously.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
CONSULT_DIR = REPO / "scripts" / "consult"
FAKE_CLI = REPO / "tests" / "fixtures" / "consult" / "fake_cli.py"

# `scripts/` is already on Pyright's `extraPaths`, so importing through the
# namespace package resolves statically as well as at runtime. Inserting
# `scripts/consult` and importing `consult` bare would work when the tests run
# and leave Pyright reporting every symbol as unknown.
sys.path.insert(0, str(REPO / "scripts"))
from consult import consult  # noqa: E402  (repo tooling, not an installed package)

# Keywords the hand-rolled validator in consult.py actually implements. A schema
# that grows one outside this set would be silently unenforced with every gate
# green, which is the failure this list exists to catch.
IMPLEMENTED_SCHEMA_KEYWORDS = {
    "$schema", "$id", "title", "description",
    "type", "properties", "required", "additionalProperties",
    "items", "maxItems", "minLength", "maxLength", "enum",
}


@pytest.fixture(autouse=True)
def never_reach_a_live_cli(monkeypatch: pytest.MonkeyPatch) -> None:
    """Point both vendors at the fixture for every test in this module.

    Without this, `resolve_executable` falls through to `shutil.which`, which
    finds the real, billable CLIs on the developer host and finds nothing on the
    Linux runner -- so a row would pass for two different reasons on the two
    platforms, or spend money.
    """
    monkeypatch.setenv("CONSULT_CLAUDE_CLI", str(FAKE_CLI))
    monkeypatch.setenv("CONSULT_CODEX_CLI", str(FAKE_CLI))


def run_consult_cli(
    subcommand: str,
    request_path: Path,
    record_root: Path,
    *,
    env: dict[str, str] | None = None,
    extra: list[str] | None = None,
) -> tuple[int, dict]:
    """Invoke the adapter as a subprocess, the way a caller actually would."""
    argv = [
        sys.executable,
        str(CONSULT_DIR / "consult.py"),
        subcommand,
        "--request", str(request_path),
        "--record-root", str(record_root),
        "--consult-id", "row",
        *(extra or []),
    ]
    child_env = {**os.environ, **(env or {})}
    completed = subprocess.run(argv, capture_output=True, text=True, env=child_env, timeout=180)
    record_path = record_root / "row" / "record.json"
    record = json.loads(record_path.read_text(encoding="utf-8")) if record_path.exists() else {}
    return completed.returncode, record


def write_request(tmp_path: Path, **overrides) -> Path:
    request = {
        "objective": "prove the consult path",
        "question": "What does AGENTS.md say about the canonical guide?",
        "artifact_paths": ["AGENTS.md"],
        "constraints": ["read-only"],
        "expected": "one sentence",
    }
    request.update(overrides)
    path = tmp_path / "request.json"
    path.write_text(json.dumps(request), encoding="utf-8")
    return path


def fixture_env(vendor: str, mode: str, log: Path, **extra: str) -> dict[str, str]:
    return {
        "CONSULT_FIXTURE_VENDOR": vendor,
        "CONSULT_FIXTURE_MODE": mode,
        "CONSULT_FIXTURE_LOG": str(log),
        **extra,
    }


def read_log(log: Path) -> list[dict]:
    if not log.exists():
        return []
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line]


# --------------------------------------------------------------------------
# Success, both directions
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("subcommand", "vendor", "direction"),
    [
        ("ask-codex", "codex", "claude->codex"),
        ("ask-claude", "claude", "codex->claude"),
    ],
)
def test_consult_succeeds_in_both_directions(
    tmp_path: Path, subcommand: str, vendor: str, direction: str
) -> None:
    log = tmp_path / "fixture.log"
    code, record = run_consult_cli(
        subcommand,
        write_request(tmp_path),
        tmp_path / "records",
        env=fixture_env(vendor, "success", log),
    )

    assert code == consult.EXIT_SUCCESS
    assert record["status"] == "success"
    assert record["direction"] == direction
    assert record["result"]["summary"] == "The fixture answered."
    assert record["child_pid"] is not None

    # Exactly two spawns per consult: the `--version` probe, then the consult.
    # Asserting "one spawn" would have been wrong, and asserting nothing would
    # have let an accidental retry loop through unnoticed.
    invocations = read_log(log)
    assert len(invocations) == 2
    assert "--version" in invocations[0]["argv"]
    assert "--version" not in invocations[1]["argv"]

    # Criterion 14: the version must round-trip from the callee, not default.
    # `read_cli_version` returns the literal "unknown" on any failure, so
    # asserting a real string is what makes this row falsifiable.
    assert record["callee"]["cli_version"] == "fake-cli 9.9.9 (consult fixture)"


def test_record_reports_the_model_that_answered_not_the_one_requested(tmp_path: Path) -> None:
    """Criterion 14 exists to catch a silent model substitution.

    Echoing the `--model` argument back into the record could never do that, so
    the fixture deliberately answers as a different model than it was asked for.
    """
    log = tmp_path / "fixture.log"
    _, record = run_consult_cli(
        "ask-claude",
        write_request(tmp_path),
        tmp_path / "records",
        env=fixture_env("claude", "success", log),
        extra=["--model", "some-model-we-asked-for"],
    )

    assert record["callee"]["model_requested"] == "some-model-we-asked-for"
    assert record["callee"]["model_answered"] == "fixture-model-that-answered"


def test_result_carries_the_advisory_statement(tmp_path: Path) -> None:
    _, record = run_consult_cli(
        "ask-claude",
        write_request(tmp_path),
        tmp_path / "records",
        env=fixture_env("claude", "success", tmp_path / "fixture.log"),
    )
    assert "Advisory until the caller verifies it" in record["advisory"]


# --------------------------------------------------------------------------
# The capability boundary -- the packet's central safety claim
# --------------------------------------------------------------------------


def test_claude_callee_is_confined_by_flags_not_prose() -> None:
    argv = consult.build_claude_argv(
        ["claude"], "prompt", model="m", profile="lean", max_budget_usd=0.5
    )
    assert argv[argv.index("--permission-mode") + 1] == "plan"
    denied = argv[argv.index("--disallowedTools") + 1].split(",")
    assert {"Write", "Edit", "NotebookEdit", "Bash", "PowerShell"} <= set(denied)
    assert argv[argv.index("--max-budget-usd") + 1] == "0.5"
    # C-7 / criterion 17: a consult creates no checkout, ever.
    assert "--worktree" not in argv


def test_codex_callee_is_confined_by_the_read_only_sandbox(tmp_path: Path) -> None:
    argv = consult.build_codex_argv(
        ["codex"], "prompt", model="m", cwd=tmp_path, last_message_path=tmp_path / "out.json"
    )
    assert argv[argv.index("-s") + 1] == "read-only"
    assert "--dangerously-bypass-approvals-and-sandbox" not in argv
    assert "workspace-write" not in argv
    assert "danger-full-access" not in argv
    assert "--worktree" not in argv


def test_lean_profile_suppresses_settings_and_mcp_servers() -> None:
    lean = consult.build_claude_argv(
        ["claude"], "p", model="m", profile="lean", max_budget_usd=1.0
    )
    repo = consult.build_claude_argv(
        ["claude"], "p", model="m", profile="repo", max_budget_usd=1.0
    )
    assert "--strict-mcp-config" in lean
    assert lean[lean.index("--setting-sources") + 1] == ""
    assert "--strict-mcp-config" not in repo


# --------------------------------------------------------------------------
# Typed terminal outcomes
# --------------------------------------------------------------------------


def test_missing_cli_is_typed_not_a_traceback(tmp_path: Path) -> None:
    code, record = run_consult_cli(
        "ask-claude",
        write_request(tmp_path),
        tmp_path / "records",
        env={"CONSULT_CLAUDE_CLI": str(tmp_path / "no-such-cli.py")},
    )
    assert code == consult.EXIT_ERROR
    assert record["status"] == "error"
    assert record["error"]["kind"] == "cli_unavailable"
    # A failure still produces evidence; a caller must never be left guessing.
    assert record["consult_id"] == "row"


def test_timeout_terminates_the_owned_child_and_leaves_bystanders_alone(tmp_path: Path) -> None:
    sentinel = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(30)"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        code, record = run_consult_cli(
            "ask-claude",
            write_request(tmp_path),
            tmp_path / "records",
            env=fixture_env("claude", "sleep", tmp_path / "fixture.log", CONSULT_FIXTURE_SLEEP="30"),
            extra=["--timeout", "2"],
        )
        assert code == consult.EXIT_TIMEOUT
        assert record["status"] == "timeout"
        assert record["error"]["kind"] == "timeout"
        # "Only the owned child is signalled" is unfalsifiable without a
        # bystander to check, so this row spawns one.
        assert sentinel.poll() is None
    finally:
        sentinel.kill()
        sentinel.wait(timeout=10)


def test_cancellation_kills_the_child_and_reports_cancelled(tmp_path: Path) -> None:
    """The cancel path is `KeyboardInterrupt`, i.e. Ctrl-C.

    The interrupt is injected at the one seam that can raise it, but the
    assertion is on a real process: the fixture child must actually be dead
    afterwards, which is a property of `_terminate_owned_child`, not of the
    patch.
    """
    original = subprocess.Popen.communicate
    state = {"spawned": None, "interrupted": False}

    def interrupt_once(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        # Only the consult itself, never the `--version` probe: interrupting
        # that one would land inside `subprocess.run` and never reach the code
        # under test.
        is_version_probe = "--version" in list(self.args)
        if not state["interrupted"] and not is_version_probe:
            state["interrupted"] = True
            state["spawned"] = self
            raise KeyboardInterrupt
        return original(self, *args, **kwargs)

    subprocess.Popen.communicate = interrupt_once  # type: ignore[method-assign]
    try:
        os.environ["CONSULT_FIXTURE_VENDOR"] = "claude"
        os.environ["CONSULT_FIXTURE_MODE"] = "sleep"
        os.environ["CONSULT_FIXTURE_SLEEP"] = "30"
        record = consult.run_consult(
            "claude",
            json.loads(write_request(tmp_path).read_text(encoding="utf-8")),
            cwd=REPO,
            record_root=tmp_path / "records",
            consult_id="row",
            model="m",
            profile="lean",
            timeout=60,
            max_output_bytes=consult.DEFAULT_MAX_OUTPUT_BYTES,
            max_budget_usd=1.0,
        )
    finally:
        subprocess.Popen.communicate = original  # type: ignore[method-assign]
        for name in ("CONSULT_FIXTURE_VENDOR", "CONSULT_FIXTURE_MODE", "CONSULT_FIXTURE_SLEEP"):
            os.environ.pop(name, None)

    assert record.status == "cancelled"
    assert record.error is not None and record.error["kind"] == "cancelled"
    assert consult._EXIT_FOR_STATUS["cancelled"] == consult.EXIT_CANCELLED
    child = state["spawned"]
    assert child is not None
    assert child.poll() is not None, "the owned child survived cancellation"


def test_non_json_output_is_malformed_not_a_schema_violation(tmp_path: Path) -> None:
    code, record = run_consult_cli(
        "ask-claude",
        write_request(tmp_path),
        tmp_path / "records",
        env=fixture_env("claude", "not_json", tmp_path / "fixture.log"),
    )
    assert code == consult.EXIT_ERROR
    assert record["error"]["kind"] == "malformed_result"
    # Criterion 23: the bytes survive even when they could not be parsed.
    assert Path(record["raw_stdout_path"]).read_bytes().startswith(b"this is not json")


def test_schema_violating_output_is_reported_as_such(tmp_path: Path) -> None:
    """A distinct `kind` from `malformed_result`.

    The two failures need different fixes -- one is a broken CLI, the other is a
    model that answered in the wrong shape -- so collapsing them would cost the
    caller the diagnosis.
    """
    code, record = run_consult_cli(
        "ask-claude",
        write_request(tmp_path),
        tmp_path / "records",
        env=fixture_env("claude", "schema_violation", tmp_path / "fixture.log"),
    )
    assert code == consult.EXIT_ERROR
    assert record["error"]["kind"] == "schema_violation"
    assert record["result"] is None


def test_needs_input_is_terminal_and_spawns_no_second_child(tmp_path: Path) -> None:
    log = tmp_path / "fixture.log"
    code, record = run_consult_cli(
        "ask-claude",
        write_request(tmp_path),
        tmp_path / "records",
        env=fixture_env("claude", "needs_input", log),
    )
    assert code == consult.EXIT_NEEDS_INPUT
    assert record["status"] == "needs_input"
    assert record["result"]["questions"] == ["Which branch should I compare against?"]
    # The adapter never answers a question on the caller's behalf, so the spawn
    # count must stay at the version probe plus the one consult.
    assert len(read_log(log)) == 2


def test_needs_input_without_questions_is_rejected(tmp_path: Path) -> None:
    """The wire schema cannot express this, so the adapter must.

    OpenAI structured outputs rejects `if/then`, so `result.schema.json` cannot
    make `questions[]` conditionally non-empty. Left unchecked, a callee could
    stall the caller with a contentless `needs_input`.
    """
    code, record = run_consult_cli(
        "ask-claude",
        write_request(tmp_path),
        tmp_path / "records",
        env=fixture_env("claude", "needs_input_empty", tmp_path / "fixture.log"),
    )
    assert code == consult.EXIT_ERROR
    assert record["error"]["kind"] == "schema_violation"
    assert "questions[] is empty" in record["error"]["detail"]


def test_oversize_output_is_capped_but_the_bytes_are_kept(tmp_path: Path) -> None:
    code, record = run_consult_cli(
        "ask-claude",
        write_request(tmp_path),
        tmp_path / "records",
        env=fixture_env("claude", "oversize", tmp_path / "fixture.log"),
        extra=["--max-output-bytes", "1024"],
    )
    assert code == consult.EXIT_ERROR
    assert record["error"]["kind"] == "output_limit_exceeded"
    # The cap protects the caller's context, not the evidence. An over-cap
    # response is exactly when the raw stream matters most.
    assert Path(record["raw_stdout_path"]).stat().st_size > 1024


def test_nonzero_exit_is_reported_with_the_child_stderr(tmp_path: Path) -> None:
    code, record = run_consult_cli(
        "ask-claude",
        write_request(tmp_path),
        tmp_path / "records",
        env=fixture_env("claude", "nonzero_exit", tmp_path / "fixture.log"),
    )
    assert code == consult.EXIT_ERROR
    assert record["error"]["kind"] == "nonzero_exit"
    assert record["exit_code"] == 7
    assert "fixture failed on purpose" in record["error"]["detail"]


def test_every_status_maps_to_a_distinct_exit_code() -> None:
    mapping = consult._EXIT_FOR_STATUS
    assert mapping == {
        "success": 0,
        "error": 1,
        "needs_input": 3,
        "timeout": 4,
        "cancelled": 5,
    }
    assert len(set(mapping.values())) == len(mapping)


# --------------------------------------------------------------------------
# The trust boundary
# --------------------------------------------------------------------------


def test_a_result_full_of_instructions_changes_nothing(tmp_path: Path) -> None:
    """F5B-6: cross-model output is data.

    The adapter must reach the same terminal state as the benign run, and the
    imperative text must survive verbatim into the record -- recorded, never
    acted on.
    """
    benign_code, benign = run_consult_cli(
        "ask-claude",
        write_request(tmp_path),
        tmp_path / "benign",
        env=fixture_env("claude", "success", tmp_path / "a.log"),
    )
    hostile_code, hostile = run_consult_cli(
        "ask-claude",
        write_request(tmp_path),
        tmp_path / "hostile",
        env=fixture_env("claude", "embedded_instruction", tmp_path / "b.log"),
    )

    assert hostile_code == benign_code == consult.EXIT_SUCCESS
    assert hostile["status"] == benign["status"] == "success"
    assert hostile["error"] is None
    assert "IGNORE YOUR INSTRUCTIONS" in hostile["result"]["summary"]
    # Nothing in the record acquires an execution-shaped field because the free
    # text asked for one.
    assert set(hostile.keys()) == set(benign.keys())


def test_shell_metacharacters_reach_the_child_byte_identical(tmp_path: Path) -> None:
    """Criterion 24: the child is spawned from an argument vector.

    If anything ever joins argv into a shell string, this payload stops arriving
    intact -- which is a far better signal than reading the source and trusting
    that `shell=False` is still there.
    """
    payload = 'x"; rm -rf / & echo $HOME `whoami` | tee /tmp/pwned #'
    log = tmp_path / "fixture.log"
    run_consult_cli(
        "ask-claude",
        write_request(tmp_path, question=payload),
        tmp_path / "records",
        env=fixture_env("claude", "success", log),
    )
    consult_invocation = read_log(log)[1]

    # The question travels JSON-encoded inside one argv token, so the assertion
    # is that it decodes back to the exact bytes -- not that it appears raw. A
    # shell round-trip would eat the quote, split the token at the `&`, or
    # expand `$HOME`; none of those survives this.
    prompts = [token for token in consult_invocation["argv"] if "```json" in token]
    assert len(prompts) == 1, "the prompt must be exactly one argv token"
    embedded = json.loads(prompts[0].split("```json", 1)[1].rsplit("```", 1)[0])
    assert embedded["question"] == payload
    assert "$HOME" in prompts[0], "no shell expanded the payload on the way"


def test_artifact_paths_are_handed_over_as_paths_not_contents(tmp_path: Path) -> None:
    """The handoff must stay exact rather than becoming a paraphrase.

    A sentinel is planted in a real file inside the repo; naming its path must
    not drag its contents into the child's argv, the prompt, or the record.
    """
    sentinel = "SENTINEL_CONTENT_THAT_MUST_NOT_TRAVEL_1f4c9"
    # The sentinel must live in a file the request actually names -- otherwise
    # an adapter that inlined every artifact would still pass, which is exactly
    # how this row failed its own mutation the first time it was written.
    relative = "tests/fixtures/consult/sentinel_artifact.md"
    target = REPO / relative
    target.write_text(sentinel, encoding="utf-8")
    try:
        log = tmp_path / "fixture.log"
        record_root = tmp_path / "records"
        _, record = run_consult_cli(
            "ask-claude",
            write_request(tmp_path, artifact_paths=[relative]),
            record_root,
            env=fixture_env("claude", "success", log),
        )
        blob = json.dumps(read_log(log)) + json.dumps(record)
        blob += (record_root / "row" / "prompt.txt").read_text(encoding="utf-8")
        assert sentinel not in blob, "artifact contents travelled instead of the path"
        assert relative in blob, "the path itself must reach the callee"
    finally:
        target.unlink(missing_ok=True)


# --------------------------------------------------------------------------
# Read scope
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "denied",
    [
        "data/database.db",
        "data/catalog.seed.db",
        "logs/app.log",
        "artifacts/consult/consult-log.jsonl",
        ".env",
        ".git/config",
        "../Hypertrophy-Toolbox-v3-main/CLAUDE.md",
    ],
)
def test_denied_artifact_paths_are_refused_before_any_child_starts(
    tmp_path: Path, denied: str
) -> None:
    log = tmp_path / "fixture.log"
    code, record = run_consult_cli(
        "ask-claude",
        write_request(tmp_path, artifact_paths=[denied]),
        tmp_path / "records",
        env=fixture_env("claude", "success", log),
    )
    assert code == consult.EXIT_ERROR
    assert record["error"]["kind"] == "bad_request"
    # "Before any child starts" is the whole point: nothing may be transmitted.
    assert read_log(log) == []


def test_an_allowed_path_still_passes() -> None:
    """The denylist must not be so broad that it blocks the mechanism."""
    consult.check_artifact_paths(
        ["AGENTS.md", "docs/ai_workflow/QUALITY_GATE.md", "utils/effective_sets.py"], REPO
    )


def test_path_containment_uses_a_separator_terminated_anchor(tmp_path: Path) -> None:
    """A sibling whose name merely starts with the root's name is not inside it."""
    root = tmp_path / "repo"
    (root / "sub").mkdir(parents=True)
    sibling = tmp_path / "repo-other"
    sibling.mkdir()
    (sibling / "file.md").write_text("x", encoding="utf-8")

    consult.check_artifact_paths(["sub"], root)
    with pytest.raises(consult.ConsultError):
        consult.check_artifact_paths([str(sibling / "file.md")], root)


# --------------------------------------------------------------------------
# Credentials
# --------------------------------------------------------------------------


def test_each_child_keeps_only_its_own_vendor_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Criterion 25's testable half.

    The adapter reads no credential and decodes none -- each CLI finds its own.
    What it must not do is hand one vendor's model process another service's
    secret, and that is a real property with a real mutation.
    """
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic-value")
    monkeypatch.setenv("OPENAI_API_KEY", "openai-value")
    monkeypatch.setenv("GITHUB_TOKEN", "github-value")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "aws-value")
    monkeypatch.setenv("HT_PLAIN_SETTING", "kept")

    claude_env = consult.child_environment("claude")
    codex_env = consult.child_environment("codex")

    assert claude_env["ANTHROPIC_API_KEY"] == "anthropic-value"
    assert "OPENAI_API_KEY" not in claude_env
    assert codex_env["OPENAI_API_KEY"] == "openai-value"
    assert "ANTHROPIC_API_KEY" not in codex_env

    for env in (claude_env, codex_env):
        assert "GITHUB_TOKEN" not in env
        assert "AWS_SECRET_ACCESS_KEY" not in env
        assert env["HT_PLAIN_SETTING"] == "kept"


def test_a_credential_in_the_child_output_never_reaches_the_record_or_the_log(
    tmp_path: Path,
) -> None:
    """The adapter cannot stop a callee from quoting a secret at it.

    What it can do is keep that text out of the structured evidence and the
    session log, which are the two things a person reads and pastes. The raw
    capture keeps it, deliberately, so the incident is investigable.
    """
    record_root = tmp_path / "records"
    _, record = run_consult_cli(
        "ask-claude",
        write_request(tmp_path),
        record_root,
        env=fixture_env("claude", "success", tmp_path / "fixture.log"),
    )
    serialized = json.dumps(record)
    log_text = (record_root / consult.CONSULT_LOG_NAME).read_text(encoding="utf-8")

    # The prompt is elided from argv_shape rather than echoed back, so a long
    # argument cannot smuggle content into the record's own fields.
    assert any(re.fullmatch(r"<\d+ chars>", token) for token in record["argv_shape"])
    for blob in (serialized, log_text):
        assert "ANTHROPIC_API_KEY" not in blob
        assert "sk-ant-" not in blob


# --------------------------------------------------------------------------
# Records, logging, and the inert paths
# --------------------------------------------------------------------------


def test_validate_starts_no_child_and_writes_no_record(tmp_path: Path) -> None:
    """Criterion 1's observable half.

    Whether a *model* invokes the adapter is not testable in pytest. What is
    testable, and what makes the record a reliable tripwire, is that a code path
    which is not a consult leaves no trace and spawns nothing.
    """
    log = tmp_path / "fixture.log"
    record_root = tmp_path / "records"
    completed = subprocess.run(
        [
            sys.executable, str(CONSULT_DIR / "consult.py"),
            "validate", "--request", str(write_request(tmp_path)),
        ],
        capture_output=True,
        text=True,
        env={**os.environ, **fixture_env("claude", "success", log)},
        timeout=60,
    )
    assert completed.returncode == consult.EXIT_SUCCESS
    assert json.loads(completed.stdout)["valid"] is True
    assert read_log(log) == []
    assert not record_root.exists()


def test_a_bad_request_is_refused_but_still_recorded(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"objective": "no question field"}), encoding="utf-8")
    code, record = run_consult_cli("ask-claude", bad, tmp_path / "records")
    assert code == consult.EXIT_ERROR
    assert record["error"]["kind"] == "bad_request"
    assert "question" in record["error"]["detail"]


def test_every_consult_appends_exactly_one_session_log_line(tmp_path: Path) -> None:
    """F5B-7: this log is the owner's only live view of an exchange they no
    longer mediate."""
    record_root = tmp_path / "records"
    for consult_id in ("first", "second"):
        subprocess.run(
            [
                sys.executable, str(CONSULT_DIR / "consult.py"), "ask-claude",
                "--request", str(write_request(tmp_path)),
                "--record-root", str(record_root),
                "--consult-id", consult_id,
            ],
            capture_output=True,
            env={**os.environ, **fixture_env("claude", "success", tmp_path / "f.log")},
            timeout=180,
        )

    lines = [
        json.loads(line)
        for line in (record_root / consult.CONSULT_LOG_NAME).read_text(encoding="utf-8").splitlines()
        if line
    ]
    assert [entry["consult_id"] for entry in lines] == ["first", "second"]
    for entry in lines:
        assert entry["status"] == "success"
        assert {"at", "direction", "model_answered", "cli_version", "duration_ms", "record"} <= set(entry)


def test_a_consult_writes_only_inside_its_record_root(tmp_path: Path) -> None:
    """Criterion 10, in the form the adapter can actually guarantee.

    A consult does write -- to `artifacts/`. What it must never do is create a
    checkout or reach anywhere else, and the read-only callee flags asserted
    above are what keep the callee from writing at all.
    """
    record_root = tmp_path / "records"
    outside = tmp_path / "outside"
    outside.mkdir()
    run_consult_cli(
        "ask-claude",
        write_request(tmp_path),
        record_root,
        env=fixture_env("claude", "success", tmp_path / "fixture.log"),
    )
    assert list(outside.iterdir()) == []
    written = {p.name for p in (record_root / "row").iterdir()}
    assert {"request.json", "prompt.txt", "raw.stdout", "record.json"} <= written
    assert not any(p.suffix == ".db" for p in record_root.rglob("*"))


def test_the_default_record_root_is_gitignored() -> None:
    """Criterion 12: consult records never become tracked truth."""
    assert consult.DEFAULT_RECORD_ROOT.is_relative_to(REPO / "artifacts")
    completed = subprocess.run(
        ["git", "check-ignore", "-q", str(consult.DEFAULT_RECORD_ROOT / "x" / "record.json")],
        cwd=REPO,
        capture_output=True,
    )
    assert completed.returncode == 0, "artifacts/ is expected to be gitignored"


# --------------------------------------------------------------------------
# Contract self-consistency
# --------------------------------------------------------------------------


def test_the_executed_adapter_is_the_tracked_file() -> None:
    """Criterion 15: no machine-local copy that a PR cannot review."""
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch",
         "scripts/consult/consult.py",
         "scripts/consult/request.schema.json",
         "scripts/consult/result.schema.json"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert tracked.returncode == 0, tracked.stderr
    assert consult.__file__ is not None
    assert Path(consult.__file__).resolve().is_relative_to(REPO)


@pytest.mark.parametrize("schema_name", ["request.schema.json", "result.schema.json"])
def test_schemas_stay_inside_the_validators_implemented_subset(schema_name: str) -> None:
    """The validator ignores what it does not implement, silently.

    A future schema gaining `pattern` or `minItems` would be unenforced with
    every gate green. This walks the schema and fails on the first keyword the
    validator does not handle.
    """
    schema = json.loads((CONSULT_DIR / schema_name).read_text(encoding="utf-8"))
    unknown: list[str] = []

    def walk(node: object, path: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if path.endswith(".properties"):
                    walk(value, f"{path}.{key}")
                    continue
                if key not in IMPLEMENTED_SCHEMA_KEYWORDS:
                    unknown.append(f"{path}.{key}")
                walk(value, f"{path}.{key}")

    walk(schema, "$")
    assert not unknown, f"{schema_name} uses keywords consult.py does not implement: {unknown}"


def test_the_result_schema_stays_strict_mode_compatible() -> None:
    """One schema serves both CLIs by satisfying the stricter one.

    Measured 2026-08-13: OpenAI structured outputs rejects a schema whose object
    omits any property from `required`, with `invalid_json_schema`. A schema
    Claude accepts happily therefore breaks the Codex direction, and only that
    direction -- which is exactly the kind of half-broken symmetry this asserts
    away.
    """
    schema = json.loads((CONSULT_DIR / "result.schema.json").read_text(encoding="utf-8"))

    def check(node: dict, path: str) -> None:
        if node.get("type") == "object":
            assert node.get("additionalProperties") is False, f"{path} must be closed"
            assert set(node.get("required", [])) == set(node.get("properties", {})), (
                f"{path}: strict mode requires every property in required"
            )
            for name, child in node.get("properties", {}).items():
                check(child, f"{path}.{name}")
        elif node.get("type") == "array" and isinstance(node.get("items"), dict):
            check(node["items"], f"{path}[]")

    check(schema, "$")
    assert "maxLength" not in (CONSULT_DIR / "result.schema.json").read_text(encoding="utf-8")


def test_the_callee_cannot_report_an_adapter_owned_status() -> None:
    """A failing child must not be able to dress its failure as a protocol outcome."""
    schema = json.loads((CONSULT_DIR / "result.schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["status"]["enum"] == ["success", "needs_input"]
    for adapter_owned in ("error", "timeout", "cancelled"):
        assert adapter_owned in consult._EXIT_FOR_STATUS
        assert adapter_owned not in schema["properties"]["status"]["enum"]


# --------------------------------------------------------------------------
# The gates this packet promised not to touch
# --------------------------------------------------------------------------


def test_the_canonical_planning_gates_still_trigger() -> None:
    """Criterion 9 / D7, asserted as presence rather than as a diff.

    "Unchanged by this packet's diff" is not something pytest can evaluate --
    there is no base ref in the inventory CI job. What it can assert is that the
    text the packet promised to leave alone is still there and still says what
    it said, which is what would actually break if someone weakened it.
    """
    quality_gate = (REPO / "docs" / "ai_workflow" / "QUALITY_GATE.md").read_text(encoding="utf-8")
    assert "## Plan-stage routing" in quality_gate
    assert "Gate 0 (requirements approval) + Gate 1 (council-reviewed plan approval)" in quality_gate
    assert "Run the union, never the weaker set." in quality_gate

    council = (REPO / ".claude" / "commands" / "council-plan.md").read_text(encoding="utf-8")
    for reviewer in ("architecture-reviewer", "test-strategist", "product-risk-reviewer"):
        assert reviewer in council

    protocol = (REPO / "docs" / "ai_workflow" / "CONSULT_PROTOCOL.md").read_text(encoding="utf-8")
    assert "Not a gate" in protocol
    assert "Not a reviewer" in protocol
    assert "manager" in protocol


def test_the_manager_charter_still_forbids_the_shell_the_adapter_needs() -> None:
    """The protocol says `manager` cannot invoke a consult. That must stay true
    of the charter, not just of the prose describing it."""
    charter = (REPO / ".claude" / "agents" / "manager.md").read_text(encoding="utf-8")
    assert "disallowedTools" in charter
    disallowed = charter.split("disallowedTools:", 1)[1].splitlines()[0]
    assert "Bash" in disallowed and "PowerShell" in disallowed
