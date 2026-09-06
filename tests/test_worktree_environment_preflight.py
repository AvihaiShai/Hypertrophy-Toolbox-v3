"""Plan v2 V2.1/AR1: exercise preflight, never persistent environment setters."""
from __future__ import annotations

import json

import pytest

from tests.worktree_cleanup.support import HOSTS, ROOT, VARIABLES, WINDOWS_ONLY, entry, environment, ps, quote

SCRIPT = ROOT / "scripts" / "preflight-worktree-environment.ps1"


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("name", VARIABLES)
@pytest.mark.parametrize("scope", ("Process", "User", "Machine"))
@pytest.mark.parametrize("value", ("0", "*", "", "READ_ERROR"))
def test_each_scope_presence_or_unreadable_state_refuses(host, name, scope, value, tmp_path):
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    behavior = "throw 'scope unavailable'" if value == "READ_ERROR" else (
        "return @{Present=$true;Value=" + quote(value) + "}")
    code = f". {quote(SCRIPT)}; $reader = {{ param($n,$s) "
    code += f"if ($n -eq {quote(name)} -and $s -eq {quote(scope)}) {{ {behavior} }}; "
    code += "return @{Present=$false;Value=$null} }; "
    code += f"Test-WorktreeEnvironment -ApprovedRoot {quote(tmp_path)} -RuntimeRoot {quote(runtime)} "
    code += f"-DatabasePath {quote(runtime / 'data' / 'database.db')} -ScopeReader $reader | ConvertTo-Json -Depth 20"
    before = sorted(str(p.relative_to(tmp_path)) for p in tmp_path.rglob("*"))
    result = ps(host, code, env=environment(tmp_path))
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["ok"] is False
    assert report["errors"]
    # Scope refusal is portable even when path validation independently refuses
    # a POSIX root. Require the injected scope's error, not just any refusal.
    expected = f"{name} {scope} scope unreadable" if value == "READ_ERROR" else f"{name} is present at {scope} scope"
    assert any(expected in error for error in report["errors"])
    assert sorted(str(p.relative_to(tmp_path)) for p in tmp_path.rglob("*")) == before


@pytest.mark.parametrize("host", HOSTS)
@WINDOWS_ONLY
def test_absent_scopes_valid_identity_passes_without_creating_runtime(host, tmp_path):
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    code = f". {quote(SCRIPT)}; Test-WorktreeEnvironment -ApprovedRoot {quote(tmp_path)} "
    code += f"-RuntimeRoot {quote(runtime)} -DatabasePath {quote(runtime / 'data' / 'database.db')} "
    code += "-ScopeReader { param($n,$s) @{Present=$false;Value=$null} } | ConvertTo-Json -Depth 20"
    result = ps(host, code, env=environment(tmp_path))
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["ok"] is True
    assert not (runtime / "data").exists()


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("name", VARIABLES)
def test_real_process_inheritance_is_refused_by_entrypoint(host, name, tmp_path):
    env = environment(tmp_path)
    env[name] = "0"
    result = entry(host, SCRIPT, ["-ApprovedRoot", str(tmp_path), "-RuntimeRoot", str(tmp_path),
        "-DatabasePath", str(tmp_path / "database.db")], env=env)
    assert result.returncode != 0
    assert f"{name} is present at Process scope" in result.stdout
    assert not (tmp_path / "database.db").exists()


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("bad", ("relative/database.db", "/c/converted/database.db", "outside", "alias"))
@WINDOWS_ONLY
def test_unverified_runtime_or_database_root_refuses(host, bad, tmp_path):
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    db = tmp_path.parent / "outside.db" if bad == "outside" else bad
    if bad == "alias":
        db = str(tmp_path / "runtime" / ".." / "database.db")
    result = entry(host, SCRIPT, ["-ApprovedRoot", str(tmp_path), "-RuntimeRoot", str(runtime),
        "-DatabasePath", str(db)], env=environment(tmp_path))
    assert result.returncode != 0
    assert not (tmp_path.parent / "outside.db").exists()


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("missing_child", (False, True))
@WINDOWS_ONLY
def test_dangling_reparse_ancestor_is_not_treated_as_verified_absence(host, missing_child, tmp_path):
    target = tmp_path / "junction-target"
    target.mkdir()
    link = tmp_path / "dangling-link"
    creation = ps(host, f"New-Item -ItemType Junction -Path {quote(link)} -Target {quote(target)} | Out-Null")
    if creation.returncode != 0:
        pytest.skip("Disposable junction unavailable: " + creation.stderr)
    retained = tmp_path / "retained-original-target"
    # Make a dangling fixture by retaining the empty target at another verified
    # scratch child. No deletion and no live reparse/root manipulation.
    assert target.resolve().is_relative_to(tmp_path.resolve())
    assert retained.parent.resolve() == tmp_path.resolve() and not retained.exists()
    assert not list(target.iterdir())
    target.rename(retained)
    candidate = link / "missing-child" if missing_child else link
    code = f". {quote(SCRIPT)}; try {{ Get-VerifiedWorktreePath -Path {quote(candidate)}; exit 0 }} "
    code += "catch { [Console]::Error.WriteLine($_); exit 1 }"
    result = ps(host, code, env=environment(tmp_path))
    assert result.returncode != 0, "Present dangling reparse ancestry was mistaken for a safe missing path"
    assert retained.is_dir() and not list(retained.iterdir())


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("path", ("relative/database.db", "/c/converted/database.db", "C:relative.db"))
def test_non_drive_qualified_path_is_rejected_on_every_platform(host, path):
    code = f". {quote(SCRIPT)}; try {{ Get-VerifiedWorktreePath -Path {quote(path)}; exit 0 }} "
    code += "catch { [Console]::Error.WriteLine($_); exit 1 }"
    result = ps(host, code)
    assert result.returncode != 0
    assert "Drive-qualified, unambiguous path required" in result.stderr
