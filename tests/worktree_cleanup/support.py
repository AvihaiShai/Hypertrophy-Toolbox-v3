"""Public entrypoint drivers; never import application modules or use live data."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
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


def ps(host: str, code: str, *, env=None, timeout=30):
    if not shutil.which(host):
        pytest.skip(f"{host} unavailable")
    return subprocess.run([host, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                           "-Command", code], capture_output=True, text=True,
                          env=env, timeout=timeout)


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
