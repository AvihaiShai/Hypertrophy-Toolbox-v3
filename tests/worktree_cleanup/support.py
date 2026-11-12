"""Public entrypoint drivers; never import application modules or use live data."""
from __future__ import annotations

import itertools
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HOSTS = ("powershell", "pwsh")
WINDOWS_ONLY = pytest.mark.skipif(
    sys.platform != "win32", reason="Requires Windows path identities and filesystem semantics"
)
VARIABLES = ("MSYS_NO_PATHCONV", "MSYS2_ARG_CONV_EXCL")


def quote(value: object) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def environment(root: Path) -> dict[str, str]:
    env = os.environ.copy()
    for key in list(env):
        if key in VARIABLES or key.startswith("GIT_"):
            del env[key]
    env.update(HT_RUNTIME_DIR=str(root), DB_FILE=str(root / "data" / "database.db"),
               TEMP=str(root), TMP=str(root), TMPDIR=str(root),
               PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1",
               GIT_CONFIG_COUNT="2", GIT_CONFIG_KEY_0="gc.auto", GIT_CONFIG_VALUE_0="0",
               GIT_CONFIG_KEY_1="maintenance.auto", GIT_CONFIG_VALUE_1="false")
    return env


# --- Issue #614 pilot instrumentation (experiment branch only; never merged) ---
_HT614_DIR = ROOT / "artifacts" / "ht614" / "timing"
_HT614_ORDINAL = itertools.count(1)


def _ht614_qpc() -> tuple[int | None, int | None]:
    """Raw QueryPerformanceCounter value and frequency (the child's Stopwatch clock)."""
    if sys.platform != "win32":
        return None, None
    import ctypes
    count, frequency = ctypes.c_int64(), ctypes.c_int64()
    ctypes.windll.kernel32.QueryPerformanceCounter(ctypes.byref(count))
    ctypes.windll.kernel32.QueryPerformanceFrequency(ctypes.byref(frequency))
    return count.value, frequency.value


def _ht614_write(record: dict) -> None:
    _HT614_DIR.mkdir(parents=True, exist_ok=True)
    name = f"{os.environ.get('PYTEST_XDIST_WORKER', 'main')}-{os.getpid()}.jsonl"
    with open(_HT614_DIR / name, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


_HT614_PREFLIGHT = ROOT / "scripts" / "preflight-worktree-environment.ps1"


def _ht614_mark(name: str, extra: str = "") -> str:
    return f"[Console]::Error.WriteLine('HT614 {name} '+[Diagnostics.Stopwatch]::GetTimestamp(){extra})"


def _ht614_wrap(code: str) -> str | None:
    """Arm C: add child phase markers to the target family's command text only."""
    prefix = f". {quote(_HT614_PREFLIGHT)}; "
    test = os.environ.get("PYTEST_CURRENT_TEST", "")
    if ("test_worktree_environment_preflight.py" not in test or not code.startswith(prefix)
            or "Test-WorktreeEnvironment " not in code):
        return None
    return "; ".join((_ht614_mark("cmd-start", "+' freq '+[Diagnostics.Stopwatch]::Frequency"),
                      prefix[:-2], _ht614_mark("dotsource-end"), code[len(prefix):],
                      _ht614_mark("pipeline-end")))


def _ht614_markers(stderr) -> list[str]:
    if isinstance(stderr, bytes):
        stderr = stderr.decode("utf-8", "replace")
    return [line[6:].strip() for line in (stderr or "").splitlines() if line.startswith("HT614 ")]


def ps(host: str, code: str, *, env=None, timeout=30):
    wrapped = _ht614_wrap(code)
    if wrapped is not None:
        code = wrapped
        env = dict(os.environ if env is None else env, HT614_MARKERS="1")
    record: dict = {"ordinal": next(_HT614_ORDINAL), "pid": os.getpid(), "wrapped": wrapped is not None,
                    "worker": os.environ.get("PYTEST_XDIST_WORKER", "main"),
                    "test": os.environ.get("PYTEST_CURRENT_TEST"), "host": host,
                    "timeout": timeout, "wall_start": datetime.now(timezone.utc).isoformat(),
                    "t_entry_ns": time.perf_counter_ns()}
    resolved = shutil.which(host)
    record["resolved"] = resolved
    record["t_after_which_ns"] = time.perf_counter_ns()
    if not resolved:
        record["outcome"] = "skip"
        _ht614_write(record)
        pytest.skip(f"{host} unavailable")
    record["qpc_before_run"], record["qpc_frequency"] = _ht614_qpc()
    record["t_before_run_ns"] = time.perf_counter_ns()
    try:
        result = subprocess.run([host, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                                 "-Command", code], capture_output=True, text=True,
                                env=env, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        record["t_end_ns"] = time.perf_counter_ns()
        record["qpc_end"] = _ht614_qpc()[0]
        record["outcome"] = "TimeoutExpired"
        record["markers"] = _ht614_markers(error.stderr)
        _ht614_write(record)
        raise
    record["t_end_ns"] = time.perf_counter_ns()
    record["qpc_end"] = _ht614_qpc()[0]
    record["outcome"] = "returned"
    record["returncode"] = result.returncode
    record["markers"] = _ht614_markers(result.stderr)
    _ht614_write(record)
    return result


def entry(host: str, script: Path, args: list[str], *, env=None, timeout=40):
    if not shutil.which(host):
        pytest.skip(f"{host} unavailable")
    return subprocess.run([host, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                           "-File", str(script), *args], capture_output=True, text=True,
                          env=env, timeout=timeout)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                          text=True, check=True, env=environment(repo)).stdout


def json_result(result):
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout.lstrip("\ufeff"))


def identity(host: str, path: Path) -> str:
    result = ps(host, f". {quote(ROOT / 'scripts' / 'audit-worktrees.ps1')}; "
                f"Get-WorktreePathIdentity -Path {quote(path)}")
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def annotation(host: str, repo: Path, **changes):
    now = datetime.now(timezone.utc)
    record = dict(identity=identity(host, repo), path=str(repo), owner="acceptance-owner",
                  task="synthetic fixture", branch=git(repo, "branch", "--show-current").strip(),
                  createdAt=now.isoformat(), expectedPr=None, teardownCondition="Retain until separately approved",
                  nextReviewDate=(now + timedelta(days=30)).isoformat(), disposition="KEEP",
                  rationale="Synthetic fixture retained", activity="UNKNOWN", activityObservedAt=now.isoformat())
    record.update(changes)
    return record


def write_annotations(path: Path, records) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Synthetic annotations\n\n```json\n" + json.dumps(
        {"schemaVersion": 1, "records": records}, indent=2) + "\n```\n", encoding="utf-8")


def fixture_repo(tmp_path: Path, host: str, *, tracked_db=False):
    parent = tmp_path / "development"
    repo = parent / "fixture"
    repo.mkdir(parents=True)
    (repo / "scripts").mkdir()
    for name in ("new-worktree.ps1", "audit-worktrees.ps1", "preflight-worktree-environment.ps1",
                 "seed_worktree_snapshot.py"):
        source = ROOT / "scripts" / name
        assert source.is_file(), f"Required Operation A entrypoint missing: {source}"
        shutil.copyfile(source, repo / "scripts" / name)
    # The real target config resolver must be present: omitting it would let the
    # creator's application-import verification silently escape test coverage.
    (repo / "utils").mkdir()
    for name in ("__init__.py", "config.py", "runtime_paths.py"):
        shutil.copyfile(ROOT / "utils" / name, repo / "utils" / name)
    (repo / ".gitignore").write_text("*.local.md\n*.db\nartifacts/\n", encoding="utf-8")
    (repo / "README.md").write_text("Disposable synthetic repository\n", encoding="utf-8")
    (repo / "data").mkdir()
    git(repo, "init")
    git(repo, "config", "user.name", "Synthetic Acceptance")
    git(repo, "config", "user.email", "acceptance@example.invalid")
    git(repo, "add", "scripts", "utils", ".gitignore", "README.md")
    if tracked_db:
        (repo / "data" / "database.db").write_bytes(b"TRACKED COLLISION SENTINEL")
        git(repo, "add", "-f", "data/database.db")
    git(repo, "commit", "-m", "synthetic fixture")
    annotations = repo / "docs" / "ai_workflow" / "WORKSTREAM_OWNERSHIP.local.md"
    write_annotations(annotations, [annotation(host, repo)])
    baseline = tmp_path / "baseline.json"
    baseline.write_text(json.dumps({"schemaVersion": 1, "approvedBy": "synthetic owner",
        "approvedAt": datetime.now(timezone.utc).isoformat(), "developmentParent": str(parent),
        "roots": [{"path": str(parent), "children": [{"path": str(repo), "identity": identity(host, repo)}]}]}),
        encoding="utf-8")
    return repo, annotations, baseline


def creator_args(repo: Path, annotations: Path, baseline: Path, task="new", seed="empty"):
    return ["-RepoRoot", str(repo), "-DevelopmentParent", str(repo.parent),
            "-AnnotationPath", str(annotations), "-BaselinePath", str(baseline),
            "-Task", task, "-Seed", seed, "-Owner", "acceptance-owner",
            "-NextReviewDate", (datetime.now(timezone.utc) + timedelta(days=10)).isoformat(),
            "-TeardownCondition", "Retain for separate owner approval", "-PythonExecutable", sys.executable]


def audit(host, repo, annotations, baseline):
    result = entry(host, repo / "scripts" / "audit-worktrees.ps1", [
        "-RepoRoot", str(repo), "-DevelopmentParent", str(repo.parent),
        "-AnnotationPath", str(annotations), "-BaselinePath", str(baseline)], env=environment(repo))
    # An unresolved projection may use a nonzero command exit; JSON remains evidence.
    assert result.stdout.strip(), result.stderr
    return json.loads(result.stdout.lstrip("\ufeff"))


def state(repo):
    return (git(repo, "worktree", "list", "--porcelain", "-z"),
            git(repo, "show-ref"), sorted(p.name for p in repo.parent.iterdir()))
