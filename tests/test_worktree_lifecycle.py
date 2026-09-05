"""Plan v2 lifecycle acceptance: real disposable Git repositories, retained roots."""
from __future__ import annotations

import json
import base64
import os
import subprocess
import sys
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from tests.worktree_cleanup.support import (HOSTS, ROOT, annotation, audit, creator_args,
    entry, environment, fixture_repo, git, identity, ps, quote, state, write_annotations)


@pytest.mark.parametrize("host", HOSTS)
def test_real_creator_adds_exactly_one_registration_and_final_annotation(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    before_refs = git(repo, "show-ref")
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline), env=environment(repo))
    assert result.returncode == 0, result.stdout + result.stderr
    target = repo.parent / "fixture-new"
    assert target.is_dir()
    assert git(repo, "worktree", "list", "--porcelain").count("worktree ") == 2
    assert before_refs.strip() in git(repo, "show-ref")
    report = audit(host, repo, annotations, baseline)
    row = next(row for row in report["rows"] if Path(row["path"]) == target)
    assert row["registered"] is True
    assert row["status"] not in ("OWNERLESS", "UNRESOLVED", "ORPHANED_ANNOTATION")
    assert row["annotation"]["owner"] == "acceptance-owner"
    assert row["annotation"]["nextReviewDate"]
    assert "Worktree ready" in result.stdout


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("problem", ("ownerless", "overdue", "orphan", "unknown_baseline", "missing", "unregistered"))
def test_creation_preflight_refuses_without_changing_registry_refs_or_children(host, problem, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    if problem == "ownerless":
        write_annotations(annotations, [])
    elif problem == "overdue":
        write_annotations(annotations, [annotation(host, repo, disposition="", rationale="",
            nextReviewDate=(datetime.now(timezone.utc) - timedelta(days=3)).isoformat())])
    elif problem == "orphan":
        write_annotations(annotations, [annotation(host, repo), annotation(host, repo,
            path=str(repo.parent / "absent"), identity="nonexistent-identity")])
    elif problem == "unknown_baseline":
        baseline = tmp_path / "absent-baseline.json"
    elif problem == "missing":
        other = repo.parent / "missing"
        git(repo, "worktree", "add", "--detach", str(other), "HEAD")
        other.rename(repo.parent / "retained-moved")
    elif problem == "unregistered":
        (repo.parent / "unregistered").mkdir()
    before = state(repo)
    annotations_before = annotations.read_bytes()
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline), env=environment(repo))
    assert result.returncode != 0
    assert state(repo) == before
    assert annotations.read_bytes() == annotations_before
    assert "Worktree ready" not in result.stdout


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("boundary", ("after_git", "before_seed", "after_seed", "before_runtime",
                                     "after_runtime", "before_annotation", "before_annotation_replace"))
def test_interrupted_creator_is_retained_ownerless_without_readiness(host, boundary, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    args = creator_args(repo, annotations, baseline)
    code = f". {quote(repo / 'scripts' / 'new-worktree.ps1')}; "
    # Parameters are bound by name, never Invoke-Expression or a production bypass.
    params = " ".join(args[i] + " " + quote(args[i+1]) for i in range(0, len(args), 2))
    code += "try { New-IsolatedWorktree " + params
    code += " -Boundary { param($name) if ($name -eq " + quote(boundary)
    code += ") { throw 'synthetic interruption' } }; exit 0 } catch { [Console]::Error.WriteLine($_); exit 1 }"
    result = ps(host, code, env=environment(repo), timeout=40)
    assert result.returncode != 0
    target = repo.parent / "fixture-new"
    assert target.is_dir()
    assert git(repo, "worktree", "list", "--porcelain").count("worktree ") == 2
    assert "Worktree ready" not in result.stdout
    row = next(row for row in audit(host, repo, annotations, baseline)["rows"] if Path(row["path"]) == target)
    assert row["status"] == "OWNERLESS" and row["activity"] == "UNKNOWN"


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("boundary", ("after_annotation_replace", "after_annotation"))
def test_interruption_after_durable_annotation_keeps_complete_projection(host, boundary, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    args = creator_args(repo, annotations, baseline)
    params = " ".join(args[i] + " " + quote(args[i+1]) for i in range(0, len(args), 2))
    result = ps(host, f". {quote(repo / 'scripts' / 'new-worktree.ps1')}; try {{ New-IsolatedWorktree "
        + params + " -Boundary { param($name) if ($name -eq " + quote(boundary) + ") { throw 'interrupted' } }; "
        + "exit 0 } catch { exit 1 }", env=environment(repo), timeout=40)
    assert result.returncode != 0
    row = next(row for row in audit(host, repo, annotations, baseline)["rows"]
               if Path(row["path"]).name == "fixture-new")
    assert row["annotation"]["owner"] == "acceptance-owner"
    assert row["status"] != "OWNERLESS"


@pytest.mark.parametrize("host", HOSTS)
def test_audit_keeps_ownerless_detached_and_orphan_rows_and_does_not_write(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    detached = repo.parent / "detached with spaces"
    git(repo, "worktree", "add", "--detach", str(detached), "HEAD")
    write_annotations(annotations, [annotation(host, repo), annotation(host, repo,
        path=str(repo.parent / "orphan"), identity="orphan-identity")])
    before = state(repo)
    tracked_before = git(repo, "status", "--porcelain=v1", "-z")
    bytes_before = annotations.read_bytes(), baseline.read_bytes()
    report = audit(host, repo, annotations, baseline)
    assert state(repo) == before
    assert git(repo, "status", "--porcelain=v1", "-z") == tracked_before
    assert (annotations.read_bytes(), baseline.read_bytes()) == bytes_before
    row = next(row for row in report["rows"] if Path(row["path"]) == detached)
    assert row["status"] == "OWNERLESS" and row["registered"] is True
    assert row["activity"] == "UNKNOWN"
    assert any(row["status"] == "ORPHANED_ANNOTATION" for row in report["rows"])


@pytest.mark.parametrize("host", HOSTS)
def test_missing_baseline_is_explicit_unknown_and_unexpected_children_are_only_reported(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    child = repo.parent / "unexpected"
    child.mkdir()
    (child / "sentinel").write_bytes(b"RETAIN")
    before = state(repo)
    report = audit(host, repo, annotations, baseline)
    assert report["ok"] is False
    assert "unexpected" in json.dumps(report).lower()
    unknown = audit(host, repo, annotations, tmp_path / "missing.json")
    assert unknown["ok"] is False
    assert "baseline" in json.dumps(unknown).lower()
    assert state(repo) == before and (child / "sentinel").read_bytes() == b"RETAIN"


@pytest.mark.parametrize("host", HOSTS)
def test_nofollow_reparse_entry_is_reported_without_reading_target(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    protected = tmp_path / "protected"
    protected.mkdir()
    sentinel = protected / "sentinel"
    sentinel.write_bytes(b"DO NOT FOLLOW")
    link = repo.parent / "redirected"
    result = ps(host, f"New-Item -ItemType Junction -Path {quote(link)} -Target {quote(protected)} | Out-Null")
    if result.returncode != 0:
        pytest.skip("Host cannot create a disposable junction: " + result.stderr)
    report = audit(host, repo, annotations, baseline)
    assert report["ok"] is False
    assert "reparse" in json.dumps(report).lower() or "unresolved" in json.dumps(report).lower()
    row = next(row for row in report["rows"] if Path(row["path"]) == link)
    assert row["status"] == "UNRESOLVED"
    assert sentinel.read_bytes() == b"DO NOT FOLLOW"
    assert not any(Path(row["path"]) == sentinel for row in report["rows"])
    # Retain the junction fixture; pytest owns its tmp_path lifecycle.


@pytest.mark.parametrize("host", HOSTS)
def test_supported_launch_overrides_inherited_source_database_and_logs(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    env = environment(repo)
    env["DB_FILE"] = str(repo / "data" / "source.db")
    env["HT_RUNTIME_DIR"] = str(repo)
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline), env=env)
    assert result.returncode == 0, result.stdout + result.stderr
    target = repo.parent / "fixture-new"
    assert str(target) in result.stdout
    assert "HT_RUNTIME_DIR" in result.stdout and "DB_FILE" in result.stdout
    # Execute only the emitted process-only launch setup artifact, never app startup.
    launches = list(target.rglob("*launch*.ps1"))
    assert len(launches) == 1, "Supported launch must expose one auditable process setup script"
    code = f". {quote(launches[0])}; @{{db=$env:DB_FILE;runtime=$env:HT_RUNTIME_DIR;temp=$env:TEMP;"
    code += "cache=$env:npm_config_cache;bytecode=$env:PYTHONDONTWRITEBYTECODE} | ConvertTo-Json"
    launch = ps(host, code, env=env)
    assert launch.returncode == 0, launch.stdout + launch.stderr
    effective = json.loads(launch.stdout)
    assert Path(effective["db"]) == target / "data" / "database.db"
    assert Path(effective["runtime"]) == target
    assert Path(effective["temp"]).is_relative_to(target)
    assert Path(effective["cache"]).is_relative_to(target)
    assert effective["bytecode"] == "1"
    resolver_code = ("import json,sys; import utils.config; from utils.runtime_paths import logs_dir; "
                     "print(json.dumps({'db':utils.config.DB_FILE,'logs':str(logs_dir()),"
                     "'module':utils.config.__file__,'interpreter':sys.executable}))")
    resolved = ps(host, f". {quote(launches[0])}; & {quote(sys.executable)} -c {quote(resolver_code)}", env=env)
    assert resolved.returncode == 0, resolved.stdout + resolved.stderr
    actual = json.loads(resolved.stdout)
    assert Path(actual["db"]) == target / "data" / "database.db"
    assert Path(actual["logs"]) == target / "logs"
    assert Path(actual["module"]) == target / "utils" / "config.py"
    assert Path(actual["interpreter"]).resolve() == Path(sys.executable).resolve()
    assert env["DB_FILE"] == str(repo / "data" / "source.db")


@pytest.mark.parametrize("host", HOSTS)
def test_concurrent_creators_never_lose_successful_annotation(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    # Two actual entrypoints race their legitimate preflights. A safe early refusal
    # is allowed; every successfully registered result must remain accounted for.
    import shutil
    executable = shutil.which(host)
    if executable is None:
        pytest.skip(f"{host} unavailable")
    children = [subprocess.Popen([executable, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
        "-File", str(repo / "scripts" / "new-worktree.ps1"),
        *creator_args(repo, annotations, baseline, task=task)], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, env=environment(repo)) for task in ("one", "two")]
    outputs = [child.communicate(timeout=50) for child in children]
    report = audit(host, repo, annotations, baseline)
    assert sum(child.returncode == 0 for child in children) >= 1, outputs
    for task, child, output in zip(("one", "two"), children, outputs):
        target = repo.parent / ("fixture-" + task)
        rows = [row for row in report["rows"] if Path(row["path"]) == target]
        if child.returncode == 0:
            assert len(rows) == 1 and rows[0]["annotation"]["owner"] == "acceptance-owner"
        elif target.exists():
            assert len(rows) == 1 and rows[0]["registered"] is True
            assert "Worktree ready" not in output[0]


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("locked", ("annotation", "coordination_lock"))
def test_annotation_locked_for_write_retains_postgit_ownerless_creation(host, locked, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    args = creator_args(repo, annotations, baseline)
    params = " ".join(args[i] + " " + quote(args[i+1]) for i in range(0, len(args), 2))
    original = annotations.read_bytes()
    # A real Windows handle permits readers but refuses replacement/writes. Acquire
    # only after runtime completion so the test exercises the final annotation gate.
    code = f". {quote(repo / 'scripts' / 'new-worktree.ps1')}; $script:hold=$null; try {{ "
    code += "New-IsolatedWorktree " + params + " -Boundary { param($name) if ($name -eq 'before_annotation') { "
    if locked == "annotation":
        code += "$script:hold=[IO.File]::Open(" + quote(annotations)
        code += ",[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::Read) "
    else:
        code += "$script:hold=[IO.File]::Open(" + quote(str(annotations) + ".lock")
        code += ",[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None) "
    code += "} }; exit 0 "
    code += "} catch { [Console]::Error.WriteLine($_); exit 1 } finally { if ($script:hold) {$script:hold.Dispose()} }"
    result = ps(host, code, env=environment(repo), timeout=40)
    assert result.returncode != 0
    assert annotations.read_bytes() == original
    target = repo.parent / "fixture-new"
    assert target.is_dir()
    row = next(row for row in audit(host, repo, annotations, baseline)["rows"] if Path(row["path"]) == target)
    assert row["status"] == "OWNERLESS" and row["registered"]
    assert "Worktree ready" not in result.stdout


@pytest.mark.parametrize("host", HOSTS)
def test_corrupt_annotation_read_refuses_before_git_creation(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    annotations.write_text("```json\n{broken\n```\n", encoding="utf-8")
    before = state(repo)
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline), env=environment(repo))
    assert result.returncode != 0
    assert state(repo) == before
    assert annotations.read_text(encoding="utf-8") == "```json\n{broken\n```\n"


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("metadata_kind", ("fresh_merged", "stale", "wrong_head", "unavailable"))
def test_pr_metadata_is_fresh_exact_head_triage_only(host, metadata_kind, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    write_annotations(annotations, [annotation(host, repo, expectedPr=42, disposition="", rationale="")])
    metadata = tmp_path / "pr-metadata.json"
    now = datetime.now(timezone.utc)
    observed = now - timedelta(days=10) if metadata_kind == "stale" else now
    head = "0" * 40 if metadata_kind == "wrong_head" else git(repo, "rev-parse", "HEAD").strip()
    if metadata_kind != "unavailable":
        metadata.write_text(json.dumps({"schemaVersion": 1, "observedAt": observed.isoformat(),
            "records": [{"number": 42, "state": "MERGED", "headRefOid": head}]}), encoding="utf-8")
    before = state(repo)
    result = entry(host, repo / "scripts" / "audit-worktrees.ps1", ["-RepoRoot", str(repo),
        "-DevelopmentParent", str(repo.parent), "-AnnotationPath", str(annotations),
        "-BaselinePath", str(baseline), "-PrMetadataPath", str(metadata)], env=environment(repo))
    report = json.loads(result.stdout)
    row = next(row for row in report["rows"] if Path(row["path"]) == repo)
    if metadata_kind == "fresh_merged":
        assert row["prState"] == "MERGED" and row["reviewReasons"]
    else:
        assert row["prState"] == "UNKNOWN"
    assert state(repo) == before and repo.is_dir()


@pytest.mark.parametrize("host", HOSTS)
def test_simultaneous_annotation_commits_preserve_both_creators(host, tmp_path):
    import shutil
    executable = shutil.which(host)
    if executable is None:
        pytest.skip(f"{host} unavailable")
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    children = []
    for task, peer in (("one", "two"), ("two", "one")):
        args = creator_args(repo, annotations, baseline, task=task)
        params = " ".join(args[i] + " " + quote(args[i+1]) for i in range(0, len(args), 2))
        code = f". {quote(repo / 'scripts' / 'new-worktree.ps1')}; try {{ New-IsolatedWorktree " + params
        code += " -Boundary { param($name) if ($name -in @('before_git','before_annotation')) { "
        code += "$mine=Join-Path " + quote(tmp_path) + " (" + quote(task + "-") + "+$name); "
        code += "$peer=Join-Path " + quote(tmp_path) + " (" + quote(peer + "-") + "+$name); "
        code += "[IO.File]::WriteAllText($mine,'ready'); $deadline=[DateTime]::UtcNow.AddSeconds(15); "
        code += "while (-not [IO.File]::Exists($peer)) { if ([DateTime]::UtcNow -gt $deadline) {throw 'barrier timeout'}; Start-Sleep -Milliseconds 20 } "
        code += "} }; exit 0 } catch { [Console]::Error.WriteLine($_); exit 1 }"
        children.append(subprocess.Popen([executable, "-NoProfile", "-NonInteractive", "-ExecutionPolicy",
            "Bypass", "-Command", code], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, env=environment(repo)))
    outputs = [child.communicate(timeout=50) for child in children]
    assert [child.returncode for child in children] == [0, 0], outputs
    report = audit(host, repo, annotations, baseline)
    for task in ("one", "two"):
        row = next(row for row in report["rows"] if Path(row["path"]).name == "fixture-" + task)
        assert row["registered"] and row["annotation"]["owner"] == "acceptance-owner"


@pytest.mark.parametrize("host", HOSTS)
def test_open_terminal_child_payload_sets_target_runtime_before_use(host, tmp_path):
    if os.name != "nt":
        pytest.skip("Windows Terminal transport requires Windows")
    repo, annotations, baseline = fixture_repo(tmp_path / "terminal owner's fixture", host)
    captured = tmp_path / "terminal-arguments.json"
    # Replace WT with a PS adapter forwarding unchanged operands into a trusted
    # Python process. This checks actual native argv after that extra adapter,
    # not WT's AppExecutionAlias activation or its visible tab. Those remain
    # owner acceptance; Application Control may block a compiled native stub.
    receiver = tmp_path / "terminal receiver.py"
    receiver.write_text(
        "import json, os, sys\nfrom pathlib import Path\n"
        "Path(os.environ['TERMINAL_TEST_CAPTURE']).write_text("
        "json.dumps(sys.argv[1:]), encoding='utf-8')\n", encoding="utf-8")
    terminal = tmp_path / "terminal adapter.ps1"
    terminal.write_text(
        f"& {quote(sys.executable)} -I -S -B {quote(receiver)} @args\nexit $LASTEXITCODE\n",
        encoding="utf-8")
    args = creator_args(repo, annotations, baseline)
    params = " ".join(args[i] + " " + quote(args[i+1]) for i in range(0, len(args), 2))
    code = f". {quote(repo / 'scripts' / 'new-worktree.ps1')}; "
    code += "function Get-Command { [CmdletBinding()] param([string]$Name,[string]$CommandType) if($Name -eq 'wt.exe') "
    code += "{[pscustomobject]@{Source=" + quote(terminal) + "}} "
    code += "else {Microsoft.PowerShell.Core\\Get-Command @PSBoundParameters} }; "
    source_observation = tmp_path / "source-environment.json"
    code += "$sourceBefore=@{db=$env:DB_FILE;runtime=$env:HT_RUNTIME_DIR;temp=$env:TEMP;policy=$env:PSExecutionPolicyPreference}; "
    code += "try { New-IsolatedWorktree " + params + " -OpenTerminal; "
    code += "@{before=$sourceBefore;after=@{db=$env:DB_FILE;runtime=$env:HT_RUNTIME_DIR;temp=$env:TEMP;policy=$env:PSExecutionPolicyPreference}} "
    code += f"| ConvertTo-Json -Depth 3 | Set-Content -LiteralPath {quote(source_observation)} -Encoding UTF8; "
    code += "exit 0 } catch { [Console]::Error.WriteLine($_); exit 1 }"
    env = environment(repo)
    env["DB_FILE"] = str(repo / "data" / "source.db")
    env["TERMINAL_TEST_CAPTURE"] = str(captured)
    result = ps(host, code, env=env, timeout=40)
    assert result.returncode == 0, result.stdout + result.stderr
    assert captured.is_file(), result.stdout + result.stderr
    terminal_args = json.loads(captured.read_text(encoding="utf-8"))
    target = repo.parent / "fixture-new"
    # Owner WT evidence: sending the spaced caller executable directly failed;
    # a whitespace-free system-host bootstrap reached the exact PS7 caller.
    assert "-d" not in terminal_args, "Target setup belongs inside the encoded child payload"
    assert all(not any(char.isspace() for char in arg) for arg in terminal_args), \
        "WT must not receive raw spaced paths across the observed failing boundary"
    assert terminal_args[:3] == ["-w", "0", "nt"]
    system_folder = ps(host, "[Environment]::GetFolderPath('System')", env=env)
    assert system_folder.returncode == 0, system_folder.stderr
    system_host = Path(system_folder.stdout.strip()) / "WindowsPowerShell/v1.0/powershell.exe"
    assert Path(terminal_args[3]).samefile(system_host)
    host_executable = shutil.which(host)
    assert host_executable is not None
    assert terminal_args[4:6] == ["-NoProfile", "-EncodedCommand"]
    assert len(terminal_args) == 7, "Native transport split or grouped command operands"
    bootstrap = base64.b64decode(terminal_args[-1]).decode("utf-16le")
    assert "-NoExit" in bootstrap, "The intended isolated caller shell must remain interactive"
    observation = tmp_path / "nested-host-observation.json"
    # Add only an observer/exit to the disposable emitted setup. Execute both
    # generated encoded layers unchanged; the exit prevents a visible/idle shell.
    launch = target / "artifacts/worktree/launch-worktree.ps1"
    launch_contents = launch.read_text(encoding="utf-8-sig")
    with launch.open("a", encoding="utf-8") as setup:
        setup.write("\n@{host=(Get-Process -Id $PID).Path; db=$env:DB_FILE; "
            "runtime=$env:HT_RUNTIME_DIR; current=$PWD.Path; temp=$env:TEMP; tmp=$env:TMP; "
            "npm=$env:npm_config_cache; bytecode=$env:PYTHONDONTWRITEBYTECODE} | "
            f"ConvertTo-Json | Set-Content -LiteralPath {quote(observation)} -Encoding UTF8\nexit 0\n")
    source_state = json.loads(source_observation.read_text(encoding="utf-8-sig"))
    assert source_state["before"] == source_state["after"]
    assert {key: source_state["after"][key] for key in ("db", "runtime", "temp")} == {
        "db": env["DB_FILE"], "runtime": env["HT_RUNTIME_DIR"], "temp": env["TEMP"]}
    # Replay the real driver process's inherited policy. ps() runs the test
    # driver with its existing process-only policy flag; Python's own env lacks
    # that child value. No persistent setting or production override is changed.
    launch_env = env.copy()
    if source_state["after"]["policy"] is None:
        launch_env.pop("PSExecutionPolicyPreference", None)
    else:
        launch_env["PSExecutionPolicyPreference"] = source_state["after"]["policy"]
    actual = subprocess.run(terminal_args[3:], capture_output=True, text=True,
        stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW,
        env=launch_env, timeout=30)
    assert actual.returncode == 0, actual.stdout + actual.stderr
    assert observation.is_file(), actual.stdout + actual.stderr
    paths = json.loads(observation.read_text(encoding="utf-8-sig"))
    assert Path(paths["host"]).samefile(host_executable)
    assert Path(paths["db"]) == target / "data" / "database.db"
    assert Path(paths["runtime"]) == target
    assert Path(paths["current"]) == target
    assert Path(paths["temp"]) == Path(paths["tmp"]) == target / "artifacts/worktree/tmp"
    assert Path(paths["npm"]) == target / "artifacts/worktree/cache/npm"
    assert paths["bytecode"] == "1"
    # The same generated outer process must also terminate on inner failure,
    # rather than leave an interactive source-bound bootstrap prompt behind.
    launch.write_text(launch_contents + "\nexit 19\n", encoding="utf-8-sig")
    failed = subprocess.run(terminal_args[3:], capture_output=True, text=True,
        stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW,
        env=launch_env, timeout=30)
    assert failed.returncode != 0, failed.stdout + failed.stderr
    assert "Caller PowerShell exited with code" in failed.stderr


@pytest.mark.parametrize("host", HOSTS)
def test_terminal_dispatch_failure_retains_created_worktree_and_annotation(host, tmp_path):
    if os.name != "nt":
        pytest.skip("Windows Terminal transport requires Windows")
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    terminal = tmp_path / "failed-terminal.ps1"
    terminal.write_text("exit 17\n", encoding="utf-8")
    args = creator_args(repo, annotations, baseline)
    params = " ".join(args[i] + " " + quote(args[i + 1]) for i in range(0, len(args), 2))
    code = f". {quote(repo / 'scripts/new-worktree.ps1')}; "
    code += "function Get-Command { [CmdletBinding()] param([string]$Name,[string]$CommandType) "
    code += "if($Name -eq 'wt.exe'){[pscustomobject]@{Source=" + quote(terminal) + "}} "
    code += "else {Microsoft.PowerShell.Core\\Get-Command @PSBoundParameters} }; "
    code += "try { New-IsolatedWorktree " + params + " -OpenTerminal; exit 0 } "
    code += "catch { [Console]::Error.WriteLine($_); exit 1 }"
    result = ps(host, code, env=environment(repo), timeout=40)
    assert result.returncode != 0
    assert "Windows Terminal dispatch failed (17)" in result.stderr
    target = repo.parent / "fixture-new"
    assert target.is_dir()
    row = next(row for row in audit(host, repo, annotations, baseline)["rows"] if Path(row["path"]) == target)
    assert row["registered"] and row["status"] == "ANNOTATED"
    assert row["annotation"]["owner"] == "acceptance-owner"


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("invalid", ("missing", "whitespace"))
def test_invalid_terminal_bootstrap_refuses_before_git_mutation(host, invalid, tmp_path):
    if os.name != "nt":
        pytest.skip("Windows Terminal transport requires Windows")
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    candidate = tmp_path / ("missing.exe" if invalid == "missing" else "invalid bootstrap.exe")
    if invalid == "whitespace":
        candidate.write_bytes(b"Synthetic non-executable sentinel; never launch")
    before = state(repo), annotations.read_bytes()
    terminal_called = tmp_path / "terminal-was-dispatched"
    terminal = tmp_path / "unexpected-terminal.ps1"
    terminal.write_text(f"[IO.File]::WriteAllText({quote(terminal_called)}, 'unexpected')\n", encoding="utf-8")
    args = creator_args(repo, annotations, baseline)
    params = " ".join(args[i] + " " + quote(args[i + 1]) for i in range(0, len(args), 2))
    code = f". {quote(repo / 'scripts/new-worktree.ps1')}; "
    # Substitute only path discovery, never the real Windows installation or
    # its environment. The creator must validate this candidate before Git add.
    code += "function Join-Path { [CmdletBinding()] param([string]$Path,[string]$ChildPath) "
    code += "if($ChildPath -eq 'WindowsPowerShell\\v1.0\\powershell.exe'){" + quote(candidate) + "} "
    code += "else {Microsoft.PowerShell.Management\\Join-Path @PSBoundParameters} }; "
    code += "function Get-Command { [CmdletBinding()] param([string]$Name,[string]$CommandType) "
    code += "if($Name -eq 'wt.exe'){[pscustomobject]@{Source=" + quote(terminal) + "}} "
    code += "else {Microsoft.PowerShell.Core\\Get-Command @PSBoundParameters} }; "
    code += "try { New-IsolatedWorktree " + params + " -OpenTerminal; exit 0 } "
    code += "catch { [Console]::Error.WriteLine($_); exit 1 }"
    result = ps(host, code, env=environment(repo), timeout=40)
    assert result.returncode != 0, "An unusable bootstrap host must refuse before worktree creation"
    assert (state(repo), annotations.read_bytes()) == before
    assert not terminal_called.exists()


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("variable", ("GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_CONFIG", "GIT_CONFIG_COUNT"))
def test_git_redirection_environment_refuses_before_any_registry_or_filesystem_mutation(host, variable, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    decoy = tmp_path / "unrelated-repository"
    decoy.mkdir()
    git(decoy, "init")
    git(decoy, "config", "user.name", "Synthetic Acceptance")
    git(decoy, "config", "user.email", "acceptance@example.invalid")
    (decoy / "sentinel.txt").write_text("retain decoy", encoding="utf-8")
    git(decoy, "add", "sentinel.txt")
    git(decoy, "commit", "-m", "unrelated synthetic root")
    env = environment(repo)
    destinations = {"GIT_DIR": decoy / ".git", "GIT_COMMON_DIR": decoy / ".git",
        "GIT_WORK_TREE": decoy, "GIT_INDEX_FILE": decoy / ".git" / "index",
        "GIT_CONFIG": decoy / ".git" / "config"}
    if variable == "GIT_CONFIG_COUNT":
        env[variable] = "1"
        env["GIT_CONFIG_KEY_0"] = "core.worktree"
        env["GIT_CONFIG_VALUE_0"] = str(decoy)
    else:
        env[variable] = str(destinations[variable])
    inherited_value = env[variable]
    before = state(repo), state(decoy)
    decoy_index = (decoy / ".git" / "index").read_bytes()
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline), env=env)
    assert result.returncode != 0, "Unverified Git routing must fail closed before Git creation"
    assert (state(repo), state(decoy)) == before
    assert (decoy / ".git" / "index").read_bytes() == decoy_index
    assert env[variable] == inherited_value


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("disposition", ("KEEP", "DEFERRED", "COMPLETED", "ABANDONED"))
@pytest.mark.parametrize("anomaly", ("branch", "created_date", "activity_date", "future_created", "future_activity"))
def test_disposition_never_waives_branch_or_annotation_date_anomaly(host, disposition, anomaly, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    future = (datetime.now(timezone.utc) + timedelta(days=10)).isoformat()
    changes = {"branch": {"branch": "different-retained-branch"},
        "created_date": {"createdAt": "not-an-iso-date"},
        "activity_date": {"activityObservedAt": "not-an-iso-date"},
        "future_created": {"createdAt": future}, "future_activity": {"activityObservedAt": future}}[anomaly]
    write_annotations(annotations, [annotation(host, repo, disposition=disposition, **changes)])
    before = state(repo)
    annotation_bytes = annotations.read_bytes()
    report = audit(host, repo, annotations, baseline)
    assert report["ok"] is False, "Owner disposition acknowledges review, never inconsistent evidence"
    row = next(row for row in report["rows"] if Path(row["path"]) == repo)
    assert row["reviewReasons"]
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline), env=environment(repo))
    assert result.returncode != 0
    assert state(repo) == before and annotations.read_bytes() == annotation_bytes


@pytest.mark.parametrize("host", HOSTS)
def test_swapped_worktree_admin_pointer_is_unresolved_even_with_keep(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    first, second = repo.parent / "fixture-a", repo.parent / "fixture-b"
    # Identical detached HEAD/branch fields prevent those cheaper comparisons from
    # masking a broken reciprocal admin-pointer identity check.
    git(repo, "worktree", "add", "--detach", str(first), "HEAD")
    git(repo, "worktree", "add", "--detach", str(second), "HEAD")
    write_annotations(annotations, [annotation(host, p) for p in (repo, first, second)])
    baseline_data = json.loads(baseline.read_text())
    baseline_data["roots"][0]["children"] += [
        {"path": str(p), "identity": identity(host, p)} for p in (first, second)]
    baseline.write_text(json.dumps(baseline_data), encoding="utf-8")
    original_first_pointer = (first / ".git").read_bytes()
    swapped_pointer = (second / ".git").read_bytes()
    assert original_first_pointer != swapped_pointer
    # Git marks the pointer hidden on Windows; open the existing file instead of
    # CREATE_ALWAYS, which refuses hidden paths. Preserve its attribute identity.
    with (first / ".git").open("r+b") as pointer:
        pointer.write(swapped_pointer)
        pointer.truncate()
    before = state(repo)
    report = audit(host, repo, annotations, baseline)
    row = next(row for row in report["rows"] if Path(row["path"]) == first)
    assert report["ok"] is False and row["status"] == "UNRESOLVED"
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline), env=environment(repo))
    assert result.returncode != 0 and state(repo) == before
    assert (first / ".git").read_bytes() == swapped_pointer, "Audit must not repair the fixture"


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("override", ("PYTHONPATH", "PYTHONHOME"))
def test_launch_normalizes_import_overrides_and_verifies_real_target_module(host, override, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    foreign = tmp_path / "foreign-python"
    foreign.mkdir()
    sentinel = tmp_path / "foreign-code-ran"
    (foreign / "sitecustomize.py").write_text(
        f"import sys\nfrom pathlib import Path\nPath({str(sentinel)!r}).write_text('foreign startup')\n"
        f"sys.path.insert(0,{str(foreign)!r})\n", encoding="utf-8")
    (foreign / "utils").mkdir()
    (foreign / "utils" / "__init__.py").write_text("", encoding="utf-8")
    (foreign / "utils" / "config.py").write_text(
        "import os\nDB_FILE=os.environ['DB_FILE']\nLOGS_DIR=os.path.join(os.environ['HT_RUNTIME_DIR'],'logs')\n",
        encoding="utf-8")
    env = environment(repo)
    env[override] = str(foreign)
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline), env=env)
    assert result.returncode == 0, result.stdout + result.stderr
    assert not sentinel.exists(), "Foreign startup/import code ran before target identity verification"
    target = repo.parent / "fixture-new"
    launch = next(target.rglob("*launch*.ps1"))
    check = ps(host, f". {quote(launch)}; @{{pythonpath=$env:PYTHONPATH;pythonhome=$env:PYTHONHOME}} | ConvertTo-Json", env=env)
    assert check.returncode == 0, check.stderr
    imported_environment = json.loads(check.stdout)
    assert not imported_environment["pythonpath"] and not imported_environment["pythonhome"]
    python_code = "import json,sys,utils.config as c;print(json.dumps({'module':c.__file__,'python':sys.executable}))"
    child = ps(host, f". {quote(launch)}; & {quote(sys.executable)} -c {quote(python_code)}", env=env)
    assert child.returncode == 0, child.stdout + child.stderr
    imported = json.loads(child.stdout)
    assert Path(imported["module"]) == target / "utils" / "config.py"
    assert Path(imported["python"]).resolve() == Path(sys.executable).resolve()
    assert not sentinel.exists() and env[override] == str(foreign)


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("variable", ("GIT_TRACE", "GIT_TRACE2_EVENT"))
@pytest.mark.parametrize("existing", (False, True))
def test_git_trace_output_environment_cannot_make_audit_or_creator_write_elsewhere(host, variable, existing, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    outside = tmp_path / "outside-approved-development-parent"
    outside.mkdir()
    trace = outside / "trace.txt"
    if existing:
        trace.write_bytes(b"RETAIN EXISTING TRACE SENTINEL")
    before_files = {p.name: p.read_bytes() for p in outside.iterdir()}
    before_git = state(repo)
    env = environment(repo)
    env[variable] = str(trace)
    audit_result = entry(host, repo / "scripts" / "audit-worktrees.ps1", [
        "-RepoRoot", str(repo), "-DevelopmentParent", str(repo.parent),
        "-AnnotationPath", str(annotations), "-BaselinePath", str(baseline)], env=env)
    after_audit = {p.name: p.read_bytes() for p in outside.iterdir()}
    assert after_audit == before_files, "Read-only audit wrote inherited Git trace output outside its approved parent"
    assert audit_result.returncode != 0
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline), env=env)
    assert {p.name: p.read_bytes() for p in outside.iterdir()} == before_files
    assert result.returncode != 0 and state(repo) == before_git
    assert env[variable] == str(trace)


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("scope", ("root", "registered"))
def test_git_pointer_reparse_is_rejected_before_any_child_receives_checkout(host, scope, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    bad = repo.parent / "redirected-checkout"
    if scope == "registered":
        git(repo, "worktree", "add", "--detach", str(bad), "HEAD")
        pointer = bad / ".git"
        retained_pointer = bad / "git-pointer.retained"
        assert pointer.parent.resolve().is_relative_to(tmp_path.resolve())
        assert retained_pointer.parent.resolve() == pointer.parent.resolve()
        pointer.rename(retained_pointer)
    else:
        bad.mkdir()
    created = ps(host, f"New-Item -ItemType Junction -Path {quote(bad / '.git')} -Target {quote(repo / '.git')} | Out-Null")
    assert created.returncode == 0, created.stderr
    baseline_data = json.loads(baseline.read_text())
    baseline_data["roots"][0]["children"].append({"path": str(bad), "identity": identity(host, bad)})
    baseline.write_text(json.dumps(baseline_data), encoding="utf-8")
    called = tmp_path / "git-received-unverified-checkout"
    root = bad if scope == "root" else repo
    code = f". {quote(repo / 'scripts' / 'audit-worktrees.ps1')}; "
    code += "$script:realGit=(Get-Command Invoke-WorktreeGit).ScriptBlock; "
    code += "function Invoke-WorktreeGit { param($Root,$Arguments) if($Root -eq " + quote(bad) + ") { "
    code += f"[IO.File]::WriteAllText({quote(called)},$Root); throw 'Unverified checkout reached Git adapter' }}; "
    code += "& $script:realGit -Root $Root -Arguments $Arguments }; "
    code += f"Get-WorktreeAudit -RepoRoot {quote(root)} -DevelopmentParent {quote(repo.parent)} "
    code += f"-AnnotationPath {quote(annotations)} -BaselinePath {quote(baseline)} | ConvertTo-Json -Depth 30"
    result = ps(host, code, env=environment(repo))
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert not called.exists(), "Git adapter received a checkout whose literal .git entry redirects elsewhere"
    assert report["ok"] is False and "reparse" in json.dumps(report).lower()


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("date", ("2050-10-01", "10/01/2050", "2050-10-01T12:00:00"))
def test_creator_rejects_timezone_free_or_ambiguous_review_date_before_git(host, date, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    args = creator_args(repo, annotations, baseline)
    args[args.index("-NextReviewDate") + 1] = date
    before = state(repo)
    result = entry(host, repo / "scripts" / "new-worktree.ps1", args, env=environment(repo))
    assert result.returncode != 0
    assert state(repo) == before
    assert "Worktree ready" not in result.stdout


@pytest.mark.parametrize("host", HOSTS)
def test_annotation_lock_reparse_refuses_without_opening_external_sentinel(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    external = tmp_path / "outside-lock-target"
    external.write_bytes(b"RETAIN LOCK TARGET")
    lock = Path(str(annotations) + ".lock")
    try:
        # Python requests Windows' existing unprivileged-symlink capability;
        # PS5's older New-Item refuses it even when this OS supports it. The
        # production creator is still invoked under each parametrized host.
        lock.symlink_to(external)
    except OSError as exc:
        pytest.skip("Native file symlink creation unavailable: " + str(exc))
    annotation_before = annotations.read_bytes()
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline), env=environment(repo))
    assert result.returncode != 0
    assert "reparse" in (result.stdout + result.stderr).lower(), "Refuse topology before trying the lock handle"
    assert external.read_bytes() == b"RETAIN LOCK TARGET" and annotations.read_bytes() == annotation_before
    target = repo.parent / "fixture-new"
    assert target.is_dir(), "Post-Git annotation refusal must retain the new checkout"
    row = next(row for row in audit(host, repo, annotations, baseline)["rows"] if Path(row["path"]) == target)
    assert row["status"] == "OWNERLESS" and row["registered"]


@pytest.mark.parametrize("host", HOSTS)
def test_missing_target_config_after_git_is_retained_incomplete_without_readiness(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    target = repo.parent / "fixture-new"
    config = target / "utils" / "config.py"
    retained = target / "utils" / "config.py.retained"
    assert config.resolve().is_relative_to(tmp_path.resolve())
    assert retained.parent.resolve() == config.parent.resolve()
    args = creator_args(repo, annotations, baseline)
    params = " ".join(args[i] + " " + quote(args[i + 1]) for i in range(0, len(args), 2))
    code = f". {quote(repo / 'scripts' / 'new-worktree.ps1')}; try {{ New-IsolatedWorktree " + params
    code += " -Boundary { param($name) if($name -eq 'after_git') { "
    code += f"[IO.File]::Move({quote(config)},{quote(retained)}) "
    code += "} }; exit 0 } catch { [Console]::Error.WriteLine($_); exit 1 }"
    result = ps(host, code, env=environment(repo), timeout=40)
    assert result.returncode != 0, "A missing real target configuration cannot pass readiness"
    assert target.is_dir() and retained.is_file() and not config.exists()
    assert "Worktree ready" not in result.stdout
    row = next(row for row in audit(host, repo, annotations, baseline)["rows"] if Path(row["path"]) == target)
    assert row["status"] == "OWNERLESS" and row["registered"]
