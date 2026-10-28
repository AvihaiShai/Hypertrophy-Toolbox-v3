"""Acceptance tests for the drive-root-child monitor.

The script under test is `.claude/hooks/drive-root-monitor.ps1`. The source of
truth is docs/msys_destination_validation/PLANNING.md: Section 0 AC4-AC7 and
Plan v2 (final, rev. round 3), decisions D9-D18 and the H/M monitor nodes. Every
node id carries the plan's own label (`H2`, `M4-missing-root`, ...), so an AC7
arm can select its must-fail set with `-k`.

Isolation (AC7, D10, D20):

* Every invocation goes through `run_monitor`. It always passes `-Root` and
  `-SnapshotDir`, and it refuses any root, snapshot directory or protected path
  outside the calling test's own `tmp_path`. M8-helper pins that nothing else
  starts the script. The one exception is H8/H8b: `ListRoots` is print-only
  and is run without `-Root` on purpose.
* A real drive root is never passed. The built-in protected trees
  (`D:\\dev-cleanup-20260824-digest`, `D:\\_digest-discard-bin`) are never
  touched: protection is exercised only through `-ProtectedPath` under
  `tmp_path`, and M6-list only reads the print-only `protected[]` field.

Hosts (D20, F8 ruling): the tests are NOT host-parametrized at collection, so
the node count is machine-independent. Each test runs its scenario under every
available PowerShell host, records every host's result, and only then asserts,
naming each host. No host at all fails inside the test body, never at import.

The CLI contract these tests fix where the plan is silent:

* `-Mode Snapshot|Compare|ListRoots|HookSessionStart|HookStop`;
* `-Root <path>`, repeated once per root; `-SnapshotDir <dir>`;
  `-ProtectedPath <path>`, repeated; the standalone modes take
  `-SessionId <id>`;
* every mode uses the D14 file `<SnapshotDir>/claude-drive-root-<id>.json`, so
  a standalone `Compare` can read a hook session's snapshot (H7);
* the standalone modes print the D12 JSON report on stdout; the hook modes read
  the hook payload on stdin.
"""

from __future__ import annotations

import ast
import contextlib
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
MONITOR = REPO / ".claude" / "hooks" / "drive-root-monitor.ps1"
HOST_NAMES = ("powershell", "pwsh")
IS_WINDOWS = sys.platform == "win32"
TIMEOUT_SECONDS = 120

# D12 standalone exit codes and report shape.
EXIT_CLEAN = 0
EXIT_NEW_CHILDREN = 10
EXIT_UNKNOWN = 11
REPORT_KEYS = ("status", "new", "unknown", "faultShapedPresent", "protected")
BUILTIN_PROTECTED = ("D:\\dev-cleanup-20260824-digest", "D:\\_digest-discard-bin")

SNAPSHOT_PREFIX = "claude-drive-root-"
EVERYONE_SID = "*S-1-1-0"

# D18 notice texts, exact.
INVALID_SNAPSHOT_TEXT = (
    "Drive-root monitoring: this session's snapshot is invalid or unreadable; UNKNOWN. "
    "No claim is made about drive roots."
)
INVALID_SESSION_ID_TEXT = (
    "Drive-root monitoring: the session id is not usable, so nothing was recorded; UNKNOWN. "
    "No claim is made about drive roots."
)
INTERNAL_FAILURE_TEXT = "Drive-root monitoring failed internally; UNKNOWN. No claim is made about drive roots."


def new_child_text(root: str, utc: str, paths: str) -> str:
    return (
        f"New direct child(ren) of {root} since monitoring began at {utc}: {paths}. "
        "Cause unknown; not necessarily created by this session."
    )


def fault_text(path: str) -> str:
    return f"Single-letter child exists: {path}. It matches the MSYS fault shape; its origin is not known."


def new_root_text(root: str, utc: str) -> str:
    return f"{root} was not present when monitoring began at {utc}; UNKNOWN."


def root_gone_text(root: str, utc: str) -> str:
    return f"{root} was present when monitoring began at {utc} but is missing or unreadable now; UNKNOWN."


def midsession_text(utc: str) -> str:
    return (
        f"Drive-root monitoring began mid-session at {utc}; children created earlier in this "
        "session are not covered."
    )


# --- hosts ---------------------------------------------------------------------

Scenario = Callable[[str, Path], None]


def available_hosts() -> list[str]:
    hosts = [name for name in HOST_NAMES if shutil.which(name)]
    if not hosts:
        pytest.fail(
            "no PowerShell host (powershell or pwsh) is available. The monitor cannot be "
            "exercised, and a missing host fails rather than skips (D20).",
            pytrace=False,
        )
    return hosts


def across_hosts(tmp_path: Path, scenario: Scenario) -> None:
    """Run the scenario under every host, then assert, naming each host's result."""
    results: list[str] = []
    failed = False
    for host in available_hosts():
        base = tmp_path / host
        (base / "snap").mkdir(parents=True)
        try:
            scenario(host, base)
        except Exception as exc:  # every host is evaluated before anything is asserted
            failed = True
            results.append(f"[{host}] FAIL {type(exc).__name__}: {exc}")
        else:
            results.append(f"[{host}] pass")
    if failed:
        pytest.fail("\n".join(results), pytrace=False)


# --- the single invocation helper ------------------------------------------------

def _inside(base: Path, path: Path | str) -> bool:
    anchor = os.path.normcase(os.path.abspath(base))
    target = os.path.normcase(os.path.abspath(path))
    return os.path.commonpath([anchor, target]) == anchor


def run_monitor(
    host: str,
    base: Path,
    mode: str,
    *,
    roots: Sequence[Path | str] = (),
    snapshot_dir: Path | None = None,
    session_id: str | None = None,
    stdin: str | None = None,
    protected: Sequence[Path] = (),
    extra: Sequence[str] = (),
    list_roots_only: bool = False,
    copies: int = 1,
) -> list[subprocess.CompletedProcess[str]]:
    """The ONLY place the monitor is started (M8-helper).

    It always passes `-Root` (except the print-only ListRoots of H8/H8b) and
    `-SnapshotDir`, and every path it passes lies under the test's `tmp_path`.
    `copies` starts that many identical processes at once (H1c).
    """
    if not MONITOR.is_file():
        raise AssertionError(f"the monitor script does not exist: {MONITOR}")
    snapshot = base / "snap" if snapshot_dir is None else snapshot_dir
    if list_roots_only:
        assert mode == "ListRoots" and not roots, "only the print-only ListRoots may omit -Root"
    else:
        assert roots, "run_monitor always passes at least one -Root"
    for path in [*roots, snapshot, *protected]:
        assert _inside(base, path), f"refusing to pass a path outside the test's tmp_path: {path}"
    argv = [host, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", str(MONITOR), "-Mode", mode]
    for root in roots:
        argv += ["-Root", str(root)]
    argv += ["-SnapshotDir", str(snapshot)]
    if session_id is not None:
        argv += ["-SessionId", session_id]
    for path in protected:
        argv += ["-ProtectedPath", str(path)]
    argv += list(extra)
    text = "" if stdin is None else stdin
    if copies == 1:
        return [
            subprocess.run(
                argv,
                input=text,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=TIMEOUT_SECONDS,
            )
        ]
    processes = [
        subprocess.Popen(
            argv,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        for _ in range(copies)
    ]
    # Release every copy's stdin before reading any output, so the copies run
    # concurrently instead of one after another.
    for process in processes:
        assert process.stdin is not None
        process.stdin.write(text)
        process.stdin.close()
    finished: list[subprocess.CompletedProcess[str]] = []
    for process in processes:
        out, err = process.communicate(timeout=TIMEOUT_SECONDS)
        finished.append(subprocess.CompletedProcess(argv, process.returncode, out, err))
    return finished


def _icacls(path: Path, *arguments: str) -> None:
    proc = subprocess.run(["icacls", str(path), *arguments], capture_output=True, text=True)
    if proc.returncode != 0:
        raise AssertionError(f"icacls {arguments} failed on {path}: {proc.stdout}{proc.stderr}")


# --- fixtures and readers ----------------------------------------------------------

def make_roots(base: Path, *names: str) -> list[Path]:
    roots = [base / name for name in names]
    for root in roots:
        root.mkdir()
    return roots


def snapshot_file(base: Path, session_id: str, snapshot_dir: Path | None = None) -> Path:
    return (base / "snap" if snapshot_dir is None else snapshot_dir) / f"{SNAPSHOT_PREFIX}{session_id}.json"


def read_snapshot(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    assert isinstance(data, dict), f"snapshot is not a JSON object: {path}"
    return data


def created_utc(path: Path) -> str:
    value = read_snapshot(path).get("createdUtc")
    assert isinstance(value, str) and value.endswith("Z"), f"createdUtc is not an ISO 8601 Z time: {value!r}"
    return value


def snapshot_children(path: Path) -> set[str]:
    roots = read_snapshot(path).get("roots")
    assert isinstance(roots, dict), f"snapshot roots is not an object: {roots!r}"
    children: set[str] = set()
    for names in roots.values():
        assert isinstance(names, list), f"snapshot root entry is not an array: {names!r}"
        children.update(str(name) for name in names)
    return children


def snap_listing(base: Path) -> list[str]:
    return sorted(entry.name for entry in (base / "snap").iterdir())


def tree_state(path: Path) -> dict[str, tuple[bool, int, int]]:
    """Every entry under `path`: (is directory, size, mtime). Detects any write."""
    state: dict[str, tuple[bool, int, int]] = {}
    for current, directories, files in os.walk(path):
        for name in [*directories, *files]:
            full = os.path.join(current, name)
            info = os.lstat(full)
            is_dir = os.path.isdir(full)
            state[os.path.relpath(full, path)] = (is_dir, 0 if is_dir else info.st_size, info.st_mtime_ns)
    return state


def entry_stamps(root: Path) -> dict[str, tuple[int, int]]:
    """CreationTime and LastWriteTime of a root and each of its entries (M5)."""

    def stamp(path: str) -> tuple[int, int]:
        info = os.stat(path)
        birth = getattr(info, "st_birthtime_ns", None)
        return (birth if isinstance(birth, int) else info.st_ctime_ns, info.st_mtime_ns)

    stamps = {".": stamp(str(root))}
    for entry in os.scandir(root):
        stamps[entry.name] = stamp(entry.path)
    return stamps


@contextlib.contextmanager
def held_exclusively(path: Path) -> Iterator[None]:
    """Hold the snapshot as another monitor instance would (TS-S4).

    On Windows a plain handle suffices: Python opens files sharing read and
    write, so the monitor's `FileShare.None` open fails with a sharing
    violation, while a `FileShare.ReadWrite` open (the M-lock mutation) would
    succeed. On POSIX, .NET implements `FileShare.None` with `flock`.
    """
    with open(path, "r+b") as handle:
        if not IS_WINDOWS:
            fcntl = importlib.import_module("fcntl")
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        yield


def write_red_audit_fixture(base: Path, root: Path) -> None:
    """A failing standing-audit report and baseline BESIDE the roots (AC4, AC5).

    The monitor must neither read these nor be influenced by them.
    """
    audit = base / "audit"
    audit.mkdir()
    (audit / "audit-worktrees-report.json").write_text(
        json.dumps(
            {
                "exitCode": 1,
                "issues": [f"Drive baseline UNEXPECTED : {root / 'stale-child'}"],
                "rows": [{"status": "ORPHANED_ANNOTATION", "reviewReasons": ["ORPHANED_ANNOTATION"]}],
            }
        ),
        encoding="utf-8",
    )
    (audit / "drive-baseline.json").write_text(
        json.dumps({"schemaVersion": 1, "roots": [{"path": str(root), "children": []}]}), encoding="utf-8"
    )


# --- hook and standalone wrappers (all start the script through run_monitor) ------

def start_payload(session_id: object, base: Path, source: str = "startup") -> str:
    return json.dumps(
        {
            "session_id": session_id,
            "cwd": str(base),
            "hook_event_name": "SessionStart",
            "source": source,
            "transcript_path": str(base / "transcript.jsonl"),
        }
    )


def stop_payload(session_id: object, base: Path) -> str:
    return json.dumps(
        {
            "session_id": session_id,
            "cwd": str(base),
            "hook_event_name": "Stop",
            "stop_hook_active": False,
            "transcript_path": str(base / "transcript.jsonl"),
        }
    )


def hook_start(
    host: str,
    base: Path,
    roots: Sequence[Path | str],
    session_id: str,
    source: str = "startup",
    snapshot_dir: Path | None = None,
) -> None:
    run = run_monitor(
        host, base, "HookSessionStart", roots=roots, snapshot_dir=snapshot_dir,
        stdin=start_payload(session_id, base, source),
    )[0]
    assert run.returncode == 0, f"HookSessionStart must exit 0 (D13), got {run.returncode}: {run.stderr}"
    assert run.stdout == "", f"HookSessionStart must write nothing to stdout (D13): {run.stdout!r}"


def stop_notice(stdout: str) -> str | None:
    """D13: HookStop stdout is empty, or exactly one object whose only key is systemMessage."""
    if stdout == "":
        return None
    try:
        message = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"HookStop stdout is neither empty nor one JSON object (D13): {stdout!r}") from exc
    assert isinstance(message, dict) and list(message) == ["systemMessage"], (
        f"HookStop stdout must be exactly one object whose only key is systemMessage (D13): {stdout!r}"
    )
    text = message["systemMessage"]
    assert isinstance(text, str) and text, f"systemMessage is not a non-empty string: {stdout!r}"
    return text


def hook_stop(
    host: str,
    base: Path,
    roots: Sequence[Path | str],
    session_id: object,
    *,
    stdin: str | None = None,
    snapshot_dir: Path | None = None,
) -> str | None:
    run = run_monitor(
        host, base, "HookStop", roots=roots, snapshot_dir=snapshot_dir,
        stdin=stop_payload(session_id, base) if stdin is None else stdin,
    )[0]
    assert run.returncode == 0, f"HookStop must always exit 0, never block (D13), got {run.returncode}: {run.stderr}"
    return stop_notice(run.stdout)


def parse_report(stdout: str) -> dict[str, object]:
    try:
        report = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"standalone stdout is not the D12 JSON report: {stdout!r}") from exc
    assert isinstance(report, dict), f"report is not a JSON object: {stdout!r}"
    missing = [key for key in REPORT_KEYS if key not in report]
    assert not missing, f"report lacks {missing}: {stdout!r}"
    return report


def report_list(report: dict[str, object], key: str) -> list[object]:
    value = report[key]
    assert isinstance(value, list), f"report {key} is not an array: {value!r}"
    return value


def unknown_reasons(report: dict[str, object]) -> list[tuple[object, object]]:
    reasons: list[tuple[object, object]] = []
    for entry in report_list(report, "unknown"):
        assert isinstance(entry, dict), f"unknown[] entry is not an object: {entry!r}"
        reasons.append((entry.get("root"), entry.get("reason")))
    return reasons


def take_snapshot(host: str, base: Path, roots: Sequence[Path | str], session_id: str) -> None:
    run = run_monitor(host, base, "Snapshot", roots=roots, session_id=session_id)[0]
    assert run.returncode == EXIT_CLEAN, f"Snapshot exited {run.returncode}: {run.stdout}{run.stderr}"


def standalone(
    host: str,
    base: Path,
    mode: str,
    roots: Sequence[Path | str],
    session_id: str,
    *,
    protected: Sequence[Path] = (),
    extra: Sequence[str] = (),
) -> tuple[int, dict[str, object]]:
    run = run_monitor(host, base, mode, roots=roots, session_id=session_id, protected=protected, extra=extra)[0]
    return run.returncode, parse_report(run.stdout)


def compare(host: str, base: Path, roots: Sequence[Path | str], session_id: str) -> tuple[int, dict[str, object]]:
    return standalone(host, base, "Compare", roots, session_id)


# --- SessionStart --------------------------------------------------------------------

H1_SOURCES = {"H1-startup": "startup", "H1-clear": "clear", "H1-resume": "resume", "H1-compact-keep": "compact"}


@pytest.mark.parametrize(
    "case_id",
    ["H1-startup", "H1-clear", "H1-resume", "H1-compact-keep", "H1-compact-invalid", "H1-held"],
)
def test_hook_session_start_creates_once(case_id: str, tmp_path: Path) -> None:
    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        (root / "existing").mkdir()
        session = "h1"
        path = snapshot_file(base, session)
        hook_start(host, base, [root], session, "startup")
        assert path.is_file(), f"SessionStart did not create {path}"
        if case_id == "H1-compact-invalid":
            path.write_text("{not json", encoding="ascii")
            hook_start(host, base, [root], session, "compact")
            assert read_snapshot(path).get("schemaVersion") == 1, "compact did not replace an invalid snapshot"
            assert snap_listing(base) == [path.name], f"extra files: {snap_listing(base)}"
            return
        before = path.read_bytes()
        file_id = os.stat(path).st_ino
        # Created first, so a SessionStart that rewrites the file visibly changes it.
        (root / "added").mkdir()
        if case_id == "H1-held":
            with held_exclusively(path):
                hook_start(host, base, [root], session, "startup")
            assert path.read_bytes() == before, "a SessionStart rewrote a snapshot another instance holds"
            hook_start(host, base, [root], session, "startup")
            assert "added" in snapshot_children(path), "once released, SessionStart must act again"
            assert snap_listing(base) == [path.name], f"extra files: {snap_listing(base)}"
            return
        source = H1_SOURCES[case_id]
        hook_start(host, base, [root], session, source)
        if case_id == "H1-compact-keep":
            assert path.read_bytes() == before, "compact replaced a valid snapshot"
            assert "added" not in snapshot_children(path)
        else:
            children = snapshot_children(path)
            assert {"existing", "added"} <= children, f"{source} did not re-snapshot: {sorted(children)}"
            assert read_snapshot(path).get("source") == source
            assert os.stat(path).st_ino == file_id, "the snapshot was replaced, not written in place (D14)"
        assert snap_listing(base) == [path.name], f"no other file may appear (D14): {snap_listing(base)}"

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize("case_id", ["H1c"])
def test_hook_session_start_concurrent_smoke(case_id: str, tmp_path: Path) -> None:
    # Smoke test only; in no must-fail set (TS2-B1). M-9 measured overlapping
    # hook instances losing unlocked writes.
    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        runs = run_monitor(host, base, "HookSessionStart", roots=[root], stdin=start_payload("h1c", base), copies=4)
        for index, run in enumerate(runs):
            assert run.returncode == 0, f"copy {index} exited {run.returncode}: {run.stderr}"
            assert run.stdout == "", f"copy {index} wrote to stdout: {run.stdout!r}"
        path = snapshot_file(base, "h1c")
        assert snap_listing(base) == [path.name], f"expected one snapshot: {snap_listing(base)}"
        assert read_snapshot(path).get("schemaVersion") == 1

    across_hosts(tmp_path, scenario)


# --- Stop ------------------------------------------------------------------------------

@pytest.mark.parametrize("case_id", ["H2"])
def test_hook_stop_reports_new_child_exit_zero(case_id: str, tmp_path: Path) -> None:
    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        (root / "existing").mkdir()
        hook_start(host, base, [root], "h2")
        (root / "newchild").mkdir()
        notice = hook_stop(host, base, [root], "h2")
        assert notice is not None, "a new child produced no notice"
        expected = new_child_text(str(root), created_utc(snapshot_file(base, "h2")), os.path.join(str(root), "newchild"))
        assert expected in notice, f"expected {expected!r} in {notice!r}"

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize("case_id", ["H3-once", "H3-second"])
def test_hook_stop_dedupes_per_session(case_id: str, tmp_path: Path) -> None:
    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        hook_start(host, base, [root], "h3")
        (root / "first").mkdir()
        first = os.path.join(str(root), "first")
        notice = hook_stop(host, base, [root], "h3")
        assert notice is not None and first in notice, f"the first child was not announced: {notice!r}"
        if case_id == "H3-once":
            repeat = hook_stop(host, base, [root], "h3")
            assert repeat is None, f"an announced child was announced again: {repeat!r}"
            return
        (root / "second").mkdir()
        second = os.path.join(str(root), "second")
        notice = hook_stop(host, base, [root], "h3")
        assert notice is not None, "a later second child produced no notice"
        expected = new_child_text(str(root), created_utc(snapshot_file(base, "h3")), second)
        assert expected in notice, f"expected {expected!r} in {notice!r}"
        assert first not in notice, f"the first child was repeated: {notice!r}"

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize(
    "case_id",
    ["H4-malformed", "H4-badid-chars", "H4-badid-129", "H4-traversal", "H4-invalid-snapshot", "H4-forced-error"],
)
def test_hook_stop_never_exits_two(case_id: str, tmp_path: Path) -> None:
    bad_ids = {"H4-badid-chars": "ab*cd", "H4-badid-129": "a" * 129, "H4-traversal": "x/../../y"}

    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        if case_id in bad_ids or case_id == "H4-malformed":
            before = tree_state(base)
            if case_id == "H4-malformed":
                notice = hook_stop(host, base, [root], None, stdin="{not json")
                # A payload that cannot be parsed has no usable session id; the
                # plan names no single text for it, so either UNKNOWN text is accepted.
                assert notice is not None and (
                    INVALID_SESSION_ID_TEXT in notice or INTERNAL_FAILURE_TEXT in notice
                ), f"no UNKNOWN notice for a malformed payload: {notice!r}"
            else:
                notice = hook_stop(host, base, [root], bad_ids[case_id])
                assert notice is not None and INVALID_SESSION_ID_TEXT in notice, (
                    f"expected the invalid-session-id text, got {notice!r}"
                )
            # A MAX_PATH failure would also be caught as UNKNOWN, so the absence
            # of any written file is what proves the id was refused (G2-5).
            assert snap_listing(base) == [], f"a file was written for an invalid id: {snap_listing(base)}"
            assert tree_state(base) == before, "something was written under tmp_path"
            return
        if case_id == "H4-invalid-snapshot":
            hook_start(host, base, [root], "h4")
            path = snapshot_file(base, "h4")
            path.write_text("{not json", encoding="ascii")
            for attempt in (1, 2):
                notice = hook_stop(host, base, [root], "h4")
                assert notice is not None and INVALID_SNAPSHOT_TEXT in notice, (
                    f"Stop {attempt}: expected the invalid-snapshot text on every Stop, got {notice!r}"
                )
            assert path.read_text(encoding="ascii") == "{not json", "an invalid snapshot was overwritten at Stop"
            return
        # H4-forced-error: the snapshot directory is a regular file.
        blocker = base / "snapfile"
        blocker.write_text("not a directory", encoding="ascii")
        notice = hook_stop(host, base, [root], "h4", snapshot_dir=blocker)
        assert notice is not None and INTERNAL_FAILURE_TEXT in notice, f"expected the internal text, got {notice!r}"

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize("case_id", ["H5"])
def test_sessions_are_isolated(case_id: str, tmp_path: Path) -> None:
    # Both ids are longer than 8 characters and share their first 8, so a file
    # name keyed on a prefix (the M-sessionfile mutation) would merge them.
    session_a, session_b = "h5shared-alpha", "h5shared-bravo"

    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        hook_start(host, base, [root], session_a)
        (root / "newchild").mkdir()
        hook_start(host, base, [root], session_b)
        file_a, file_b = snapshot_file(base, session_a), snapshot_file(base, session_b)
        assert snap_listing(base) == sorted([file_a.name, file_b.name]), f"files: {snap_listing(base)}"
        notice = hook_stop(host, base, [root], session_a)
        assert notice is not None, "session A lost its child to session B's snapshot"
        expected = new_child_text(str(root), created_utc(file_a), os.path.join(str(root), "newchild"))
        assert expected in notice, f"expected {expected!r} in {notice!r}"
        assert hook_stop(host, base, [root], session_b) is None, "session B saw a child that predates it"

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize("case_id", ["H6"])
def test_hook_stop_skips_when_locked(case_id: str, tmp_path: Path) -> None:
    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        hook_start(host, base, [root], "h6")
        path = snapshot_file(base, "h6")
        before = path.read_bytes()
        # Created first, so an unlocked Stop would print a notice and update
        # `announced` (TS3-S1).
        (root / "newchild").mkdir()
        with held_exclusively(path):
            notice = hook_stop(host, base, [root], "h6")
        assert notice is None, f"a Stop acted on a snapshot another instance holds: {notice!r}"
        assert path.read_bytes() == before, "a held snapshot was modified"
        released = hook_stop(host, base, [root], "h6")
        assert released is not None and os.path.join(str(root), "newchild") in released, (
            f"once released, Stop must announce the child: {released!r}"
        )

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize("case_id", ["H7"])
def test_standalone_compare_ignores_reported(case_id: str, tmp_path: Path) -> None:
    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        hook_start(host, base, [root], "h7")
        (root / "newchild").mkdir()
        path = os.path.join(str(root), "newchild")
        notice = hook_stop(host, base, [root], "h7")
        assert notice is not None and path in notice, f"precondition: the hook announces first: {notice!r}"
        code, report = compare(host, base, [root], "h7")
        assert code == EXIT_NEW_CHILDREN, f"standalone Compare exited {code}: {report}"
        assert path in report_list(report, "new"), f"new[] lacks {path}: {report}"

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize("case_id", ["H8", "H8b"])
def test_default_roots_are_fixed_volumes(case_id: str, tmp_path: Path) -> None:
    if case_id == "H8" and not IS_WINDOWS:
        pytest.skip("H8 enumerates Windows fixed volumes; it does not run in Linux CI (accepted gap)")
    if case_id == "H8b" and IS_WINDOWS:
        pytest.skip("H8b covers non-Windows hosts, where no fixed volume can be enumerated")

    def scenario(host: str, base: Path) -> None:
        run = run_monitor(host, base, "ListRoots", list_roots_only=True)[0]
        if case_id == "H8b":
            assert run.returncode == EXIT_UNKNOWN, f"no -Root on non-Windows must exit 11, got {run.returncode}"
            return
        assert run.returncode == 0, f"ListRoots exited {run.returncode}: {run.stderr}"
        roots = list_roots_output(run.stdout)
        assert roots, f"ListRoots printed no roots: {run.stdout!r}"
        bad = [root for root in roots if not re.fullmatch(r"[A-Za-z]:\\", root)]
        assert not bad, f"roots not in X:\\ form: {bad}"

    across_hosts(tmp_path, scenario)


def list_roots_output(stdout: str) -> list[str]:
    # The plan fixes the root shape, not the print format: accept a JSON array,
    # a JSON object with `roots`, or one root per line.
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return [line.strip() for line in stdout.splitlines() if line.strip()]
    if isinstance(data, dict):
        data = data.get("roots")
    assert isinstance(data, list), f"unrecognised ListRoots output: {stdout!r}"
    return [str(root) for root in data]


@pytest.mark.parametrize("case_id", ["H9-notice", "H9-once", "H9-standalone"])
def test_fault_shaped_child(case_id: str, tmp_path: Path) -> None:
    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        (root / "existing").mkdir()
        (root / "q").mkdir()
        fault = os.path.join(str(root), "q")
        if case_id == "H9-standalone":
            take_snapshot(host, base, [root], "h9")
            code, report = compare(host, base, [root], "h9")
            assert code == EXIT_CLEAN, f"a standing fault-shaped child must not change the exit code: {code}"
            assert fault in report_list(report, "faultShapedPresent"), f"faultShapedPresent lacks {fault}: {report}"
            return
        hook_start(host, base, [root], "h9")
        notice = hook_stop(host, base, [root], "h9")
        assert notice is not None and fault_text(fault) in notice, f"expected {fault_text(fault)!r} in {notice!r}"
        assert "New direct child" not in notice, f"a pre-existing child was reported as new: {notice!r}"
        if case_id == "H9-once":
            repeat = hook_stop(host, base, [root], "h9")
            assert repeat is None, f"the fault-shape warning was repeated: {repeat!r}"

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize("case_id", ["H10-baseline", "H10-once", "H10-later-child"])
def test_hook_stop_midsession_baseline(case_id: str, tmp_path: Path) -> None:
    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        (root / "existing").mkdir()
        path = snapshot_file(base, "h10")
        notice = hook_stop(host, base, [root], "h10")
        assert path.is_file(), "Stop with no snapshot must create the mid-session baseline"
        assert snap_listing(base) == [path.name], f"extra files: {snap_listing(base)}"
        if case_id == "H10-baseline":
            assert read_snapshot(path).get("source") == "stop-baseline"
            expected = midsession_text(created_utc(path))
            assert notice is not None and expected in notice, f"expected {expected!r} in {notice!r}"
            return
        assert notice is not None, "precondition: the mid-session notice is printed once"
        if case_id == "H10-once":
            repeat = hook_stop(host, base, [root], "h10")
            assert repeat is None, f"the mid-session notice was repeated: {repeat!r}"
            return
        (root / "newchild").mkdir()
        later = hook_stop(host, base, [root], "h10")
        expected = new_child_text(str(root), created_utc(path), os.path.join(str(root), "newchild"))
        assert later is not None and expected in later, f"expected {expected!r} in {later!r}"

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize("case_id", ["H11-newroot-once"])
def test_hook_stop_new_root_announced_once(case_id: str, tmp_path: Path) -> None:
    def scenario(host: str, base: Path) -> None:
        (first,) = make_roots(base, "r1")
        hook_start(host, base, [first], "h11")
        (second,) = make_roots(base, "r2")
        notice = hook_stop(host, base, [first, second], "h11")
        expected = new_root_text(str(second), created_utc(snapshot_file(base, "h11")))
        assert notice is not None and expected in notice, f"expected {expected!r} in {notice!r}"
        repeat = hook_stop(host, base, [first, second], "h11")
        assert repeat is None, f"the newly-discovered-root notice was repeated: {repeat!r}"

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize("case_id", ["H12-rootgone-once"])
def test_hook_stop_root_gone_announced_once(case_id: str, tmp_path: Path) -> None:
    def scenario(host: str, base: Path) -> None:
        first, second = make_roots(base, "r1", "r2")
        hook_start(host, base, [first, second], "h12")
        second.rmdir()
        notice = hook_stop(host, base, [first, second], "h12")
        expected = root_gone_text(str(second), created_utc(snapshot_file(base, "h12")))
        assert notice is not None and expected in notice, f"expected {expected!r} in {notice!r}"
        repeat = hook_stop(host, base, [first, second], "h12")
        assert repeat is None, f"the missing-root notice was repeated: {repeat!r}"

    across_hosts(tmp_path, scenario)


# --- standalone ----------------------------------------------------------------------

@pytest.mark.parametrize("case_id", ["M1"])
def test_new_child_reported_despite_red_audit_fixture(case_id: str, tmp_path: Path) -> None:
    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        (root / "existing").mkdir()
        write_red_audit_fixture(base, root)
        take_snapshot(host, base, [root], "m1")
        (root / "newchild").mkdir()
        code, report = compare(host, base, [root], "m1")
        assert code == EXIT_NEW_CHILDREN, f"expected exit 10, got {code}: {report}"
        assert report["status"] == "NEW_CHILDREN", f"status: {report['status']!r}"
        assert report_list(report, "new") == [os.path.join(str(root), "newchild")], f"new[]: {report['new']}"

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize("case_id", ["M2"])
def test_no_new_child_exits_zero(case_id: str, tmp_path: Path) -> None:
    # Exit code only (TS2-B2). The red audit and ORPHANED_ANNOTATION fixture
    # sits beside the root and must not move it.
    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        (root / "existing").mkdir()
        write_red_audit_fixture(base, root)
        take_snapshot(host, base, [root], "m2")
        run = run_monitor(host, base, "Compare", roots=[root], session_id="m2")[0]
        assert run.returncode == EXIT_CLEAN, f"expected exit 0, got {run.returncode}: {run.stdout}{run.stderr}"

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize("case_id", ["M3"])
def test_removed_child_not_reported_as_new(case_id: str, tmp_path: Path) -> None:
    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        (root / "keep").mkdir()
        (root / "gone").mkdir()
        take_snapshot(host, base, [root], "m3")
        (root / "gone").rmdir()
        code, report = compare(host, base, [root], "m3")
        assert report_list(report, "new") == [], f"new[] must be empty: {report['new']}"
        assert code == EXIT_CLEAN, f"expected exit 0, got {code}: {report}"

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize(
    "case_id",
    [
        "M4-missing-root",
        "M4-unreadable-root",
        "M4-missing-snapshot",
        "M4-invalid-snapshot",
        "M4-wrong-schema",
        "M4-newroot",
    ],
)
def test_unknown_cases(case_id: str, tmp_path: Path) -> None:
    geteuid = getattr(os, "geteuid", None)
    if case_id == "M4-unreadable-root" and not IS_WINDOWS and geteuid is not None and geteuid() == 0:
        pytest.skip("root ignores chmod 000, so no directory is unreadable to it")

    def expect(code: int, report: dict[str, object], reason: str, root: Path | None) -> None:
        assert code == EXIT_UNKNOWN, f"expected exit 11, got {code}: {report}"
        assert report["status"] == "UNKNOWN", f"status: {report['status']!r}"
        reasons = unknown_reasons(report)
        if root is None:
            assert any(found == reason for _, found in reasons), f"no {reason!r} in unknown[]: {reasons}"
        else:
            assert (str(root), reason) in reasons, f"no ({str(root)!r}, {reason!r}) in unknown[]: {reasons}"

    def scenario(host: str, base: Path) -> None:
        first, second = make_roots(base, "r1", "r2")
        (first / "existing").mkdir()
        session = "m4"
        if case_id == "M4-missing-snapshot":
            code, report = compare(host, base, [first], session)
            expect(code, report, "snapshot-missing", None)
            return
        if case_id == "M4-newroot":
            take_snapshot(host, base, [first], session)
            code, report = compare(host, base, [first, second], session)
            expect(code, report, "root-new", second)
            return
        take_snapshot(host, base, [first, second], session)
        path = snapshot_file(base, session)
        if case_id == "M4-missing-root":
            second.rmdir()
            code, report = compare(host, base, [first, second], session)
            expect(code, report, "root-missing", second)
        elif case_id == "M4-invalid-snapshot":
            path.write_text("{not json", encoding="ascii")
            code, report = compare(host, base, [first, second], session)
            expect(code, report, "snapshot-invalid", None)
        elif case_id == "M4-wrong-schema":
            data = read_snapshot(path)
            data["schemaVersion"] = 2
            path.write_text(json.dumps(data), encoding="utf-8")
            code, report = compare(host, base, [first, second], session)
            expect(code, report, "schema-mismatch", None)
        else:
            unreadable_root_case(host, base, first, second, session, expect)

    across_hosts(tmp_path, scenario)


def unreadable_root_case(
    host: str,
    base: Path,
    first: Path,
    second: Path,
    session: str,
    expect: Callable[[int, dict[str, object], str, Path | None], None],
) -> None:
    # The deny is always removed again, so pytest can clean tmp_path (TS2-S3).
    if IS_WINDOWS:
        _icacls(first, "/deny", f"{EVERYONE_SID}:(RD)")
    else:
        os.chmod(first, 0)
    try:
        try:
            os.listdir(first)
        except PermissionError:
            pass
        else:
            raise AssertionError(f"fixture defect: {first} is still listable, so the case proves nothing")
        code, report = compare(host, base, [first, second], session)
        expect(code, report, "root-unreadable", first)
    finally:
        if IS_WINDOWS:
            _icacls(first, "/remove:d", EVERYONE_SID)
        else:
            os.chmod(first, 0o755)


@pytest.mark.parametrize("case_id", ["M5"])
def test_monitor_is_read_only(case_id: str, tmp_path: Path) -> None:
    def scenario(host: str, base: Path) -> None:
        first, second = make_roots(base, "r1", "r2")
        (first / "a.txt").write_text("content", encoding="ascii")
        (first / "sub").mkdir()
        (second / "other").mkdir()

        def outside_snap() -> dict[str, tuple[bool, int, int]]:
            return {key: value for key, value in tree_state(base).items() if key.split(os.sep)[0] != "snap"}

        tree_before = outside_snap()
        stamps_before = {root.name: entry_stamps(root) for root in (first, second)}
        take_snapshot(host, base, [first, second], "m5")
        # Compare runs against a VALID snapshot, so a write placed after
        # enumeration (the M-write mutation) is reached (TS3-S5).
        code, report = compare(host, base, [first, second], "m5")
        assert code == EXIT_CLEAN, f"precondition: an unchanged tree compares clean, got {code}: {report}"
        assert {root.name: entry_stamps(root) for root in (first, second)} == stamps_before, (
            "a root entry's CreationTime or LastWriteTime changed"
        )
        assert outside_snap() == tree_before, "something outside the snapshot directory was written"
        assert snap_listing(base) == [snapshot_file(base, "m5").name], (
            f"only the snapshot file may be written, with no temp or lock file: {snap_listing(base)}"
        )

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize("case_id", ["M6-protected", "M6-root-parent", "M6-list"])
def test_protected_and_root_parent_paths(case_id: str, tmp_path: Path) -> None:
    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        if case_id == "M6-list":
            take_snapshot(host, base, [root], "m6")
            code, report = compare(host, base, [root], "m6")
            assert code == EXIT_CLEAN, f"exit {code}: {report}"
            listed = report_list(report, "protected")
            missing = [path for path in BUILTIN_PROTECTED if path not in listed]
            assert not missing, f"protected[] lacks {missing}: {listed}"
            return
        before = tree_state(base)
        if case_id == "M6-protected":
            # The snapshot path lies under an additive protected path.
            code, report = standalone(host, base, "Snapshot", [root], "m6", protected=[base / "snap"])
            reason = "protected-path"
        else:
            # The snapshot's parent directory is itself a monitored root.
            code, report = standalone(host, base, "Snapshot", [root, base / "snap"], "m6")
            reason = "root-parent-path"
        assert code == EXIT_UNKNOWN, f"expected exit 11, got {code}: {report}"
        reasons = [found for _, found in unknown_reasons(report)]
        assert reason in reasons, f"no {reason!r} in unknown[]: {reasons}"
        assert snap_listing(base) == [], f"a refused snapshot path was written: {snap_listing(base)}"
        assert tree_state(base) == before, "something was written under tmp_path"

    across_hosts(tmp_path, scenario)


@pytest.mark.parametrize("case_id", ["M7"])
def test_bad_arguments_exit_unknown(case_id: str, tmp_path: Path) -> None:
    variants: list[tuple[str, tuple[str, ...]]] = [
        ("Bogus", ()),
        ("Compare", ("-Frobnicate", "1")),
        ("Compare", ("-Root",)),
    ]

    def scenario(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        problems: list[str] = []
        for mode, extra in variants:
            code, report = standalone(host, base, mode, [root], "m7", extra=extra)
            reasons = [found for _, found in unknown_reasons(report)]
            if code != EXIT_UNKNOWN or "bad-arguments" not in reasons:
                problems.append(f"-Mode {mode} {' '.join(extra)}: exit {code}, reasons {reasons}")
        assert not problems, "; ".join(problems)

    across_hosts(tmp_path, scenario)


# --- static checks -----------------------------------------------------------------------

SUBPROCESS_STARTERS = {"run", "Popen", "call", "check_call", "check_output", "getoutput", "getstatusoutput"}
OS_STARTERS = {"system", "popen", "startfile", "execv", "execve", "execl", "execlp", "execvp", "spawnv", "spawnl"}


@pytest.mark.parametrize("case_id", ["M8-helper"])
def test_only_run_monitor_invokes_the_script(case_id: str) -> None:
    """No test starts the monitor except through run_monitor (TS-S8)."""
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    problems: list[str] = []

    def visit(node: ast.AST, function: str | None) -> None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function = node.name if function is None else function
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            owner, attribute = node.func.value.id, node.func.attr
            if owner == "subprocess" and attribute in SUBPROCESS_STARTERS:
                if function == "_icacls":
                    first = node.args[0] if node.args else None
                    is_icacls = (
                        isinstance(first, ast.List) and bool(first.elts)
                        and isinstance(first.elts[0], ast.Constant) and first.elts[0].value == "icacls"
                    )
                    if not is_icacls:
                        problems.append(f"line {node.lineno}: _icacls starts something other than icacls")
                elif function != "run_monitor":
                    problems.append(f"line {node.lineno}: subprocess.{attribute} outside run_monitor ({function})")
            if owner == "os" and attribute in OS_STARTERS:
                problems.append(f"line {node.lineno}: os.{attribute} starts a process")
        if isinstance(node, ast.Name) and node.id == "MONITOR" and isinstance(node.ctx, ast.Load):
            if function not in ("run_monitor", "monitor_code"):
                problems.append(f"line {node.lineno}: MONITOR referenced in {function}")
        for child in ast.iter_child_nodes(node):
            visit(child, function)

    visit(tree, None)
    runner = next(
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "run_monitor"
    )
    literals = {node.value for node in ast.walk(runner) if isinstance(node, ast.Constant)}
    for flag in ("-Root", "-SnapshotDir"):
        if flag not in literals:
            problems.append(f"run_monitor no longer passes {flag}")
    assert not problems, "\n".join(problems)


def strip_powershell_comments(source: str) -> str:
    """Drop `#` line comments and `<# #>` blocks, keeping quoted text (TS-N2)."""
    out: list[str] = []
    index, quote = 0, ""
    while index < len(source):
        character = source[index]
        if quote:
            out.append(character)
            if quote == '"' and character == "`" and index + 1 < len(source):
                out.append(source[index + 1])
                index += 2
                continue
            if character == quote:
                if source.startswith(quote * 2, index):
                    out.append(quote)
                    index += 2
                    continue
                quote = ""
            index += 1
            continue
        if source.startswith("<#", index):
            end = source.find("#>", index + 2)
            index = len(source) if end < 0 else end + 2
            out.append(" ")
            continue
        if character == "#":
            end = source.find("\n", index)
            index = len(source) if end < 0 else end
            continue
        if character in "'\"":
            quote = character
        out.append(character)
        index += 1
    return "".join(out)


def monitor_code() -> str:
    if not MONITOR.is_file():
        raise AssertionError(f"the monitor script does not exist: {MONITOR}")
    return strip_powershell_comments(MONITOR.read_text(encoding="utf-8-sig"))


# The standing audit, its owner baseline and the ownership ledger. The monitor's
# independence (AC4) means its code never names any of them; comments may.
AUDIT_REFERENCES = ("audit-worktrees", "Get-WorktreeAudit", "drive-baseline", "BaselinePath",
                    "driveRootUnexpected", "WORKSTREAM_OWNERSHIP")


@pytest.mark.parametrize("case_id", ["M8-static"])
def test_monitor_never_reads_the_audit_or_baseline(case_id: str) -> None:
    code = monitor_code().lower()
    found = [reference for reference in AUDIT_REFERENCES if reference.lower() in code]
    assert not found, f"the monitor's code references {found}"


# --- reported paths and texts -------------------------------------------------------------

@pytest.mark.parametrize("case_id", ["M9-path", "M9-case", "M9-texts"])
def test_reported_paths_and_texts(case_id: str, tmp_path: Path) -> None:
    def path_case(host: str, base: Path) -> None:
        make_roots(base, "r1")
        # The root as given keeps its `.` segment; the reported path is that
        # string plus the child name, not a canonicalised form (TS-N3).
        given = os.path.join(str(base), ".", "r1")
        take_snapshot(host, base, [given], "m9")
        (base / "r1" / "newchild").mkdir()
        code, report = compare(host, base, [given], "m9")
        assert code == EXIT_NEW_CHILDREN, f"expected exit 10, got {code}: {report}"
        assert report_list(report, "new") == [os.path.join(given, "newchild")], f"new[]: {report['new']}"

    def case_case(host: str, base: Path) -> None:
        (root,) = make_roots(base, "r1")
        (root / "Alpha").mkdir()
        take_snapshot(host, base, [root], "m9")
        os.rename(root / "Alpha", root / "ALPHA")
        code, report = compare(host, base, [root], "m9")
        if IS_WINDOWS:
            # Ordinal-ignore-case on Windows (D11): a case-only rename is not new.
            assert code == EXIT_CLEAN and report_list(report, "new") == [], f"exit {code}: {report}"
        else:
            assert code == EXIT_NEW_CHILDREN, f"ordinal elsewhere: expected exit 10, got {code}: {report}"
            assert os.path.join(str(root), "ALPHA") in report_list(report, "new"), f"new[]: {report['new']}"

    def texts_case(host: str, base: Path) -> None:
        missing: list[str] = []

        def area(name: str) -> Path:
            place = base / name
            (place / "snap").mkdir(parents=True)
            return place

        def check(label: str, expected: str, notice: str | None) -> None:
            if notice is None or expected not in notice:
                missing.append(f"{label}: expected {expected!r}, got {notice!r}")

        place = area("new")
        (root,) = make_roots(place, "r1")
        hook_start(host, place, [root], "t")
        (root / "newchild").mkdir()
        check("new child", new_child_text(str(root), created_utc(snapshot_file(place, "t")),
                                          os.path.join(str(root), "newchild")), hook_stop(host, place, [root], "t"))

        place = area("fault")
        (root,) = make_roots(place, "r1")
        (root / "q").mkdir()
        hook_start(host, place, [root], "t")
        check("fault shape", fault_text(os.path.join(str(root), "q")), hook_stop(host, place, [root], "t"))

        place = area("newroot")
        first, second = make_roots(place, "r1", "r2")
        hook_start(host, place, [first], "t")
        check("new root", new_root_text(str(second), created_utc(snapshot_file(place, "t"))),
              hook_stop(host, place, [first, second], "t"))

        place = area("gone")
        first, second = make_roots(place, "r1", "r2")
        hook_start(host, place, [first, second], "t")
        second.rmdir()
        check("missing root", root_gone_text(str(second), created_utc(snapshot_file(place, "t"))),
              hook_stop(host, place, [first, second], "t"))

        place = area("invalid")
        (root,) = make_roots(place, "r1")
        hook_start(host, place, [root], "t")
        snapshot_file(place, "t").write_text("{not json", encoding="ascii")
        check("invalid snapshot", INVALID_SNAPSHOT_TEXT, hook_stop(host, place, [root], "t"))

        place = area("badid")
        (root,) = make_roots(place, "r1")
        check("invalid session id", INVALID_SESSION_ID_TEXT, hook_stop(host, place, [root], "ab*cd"))

        place = area("internal")
        (root,) = make_roots(place, "r1")
        blocker = place / "snapfile"
        blocker.write_text("not a directory", encoding="ascii")
        check("internal failure", INTERNAL_FAILURE_TEXT, hook_stop(host, place, [root], "t", snapshot_dir=blocker))

        place = area("midsession")
        (root,) = make_roots(place, "r1")
        notice = hook_stop(host, place, [root], "t")
        check("mid-session", midsession_text(created_utc(snapshot_file(place, "t"))), notice)

        assert not missing, "\n".join(missing)

    scenarios: dict[str, Scenario] = {"M9-path": path_case, "M9-case": case_case, "M9-texts": texts_case}
    across_hosts(tmp_path, scenarios[case_id])
