"""V2.2/TS3 synthetic WAL snapshots and actual creator collision contracts."""
from __future__ import annotations

import importlib.util
import json
import sqlite3
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from tests.worktree_cleanup.support import (HOSTS, ROOT, WINDOWS_ONLY, audit, creator_args, entry, environment,
                                            fixture_repo, git, ps, quote, state)

SCRIPT = ROOT / "scripts" / "seed_worktree_snapshot.py"


def helper():
    spec = importlib.util.spec_from_file_location("operation_a_snapshot", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def database(path: Path, *, wal=False):
    conn = sqlite3.connect(path)
    if wal:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA wal_autocheckpoint=0")
    conn.executescript("CREATE TABLE parent(id INTEGER PRIMARY KEY, value INTEGER);"
                       "CREATE TABLE child(id INTEGER PRIMARY KEY REFERENCES parent(id), value INTEGER);"
                       "PRAGMA user_version=7;")
    conn.execute("INSERT INTO parent VALUES(1, 10)")
    conn.execute("INSERT INTO child VALUES(1, 10)")
    conn.commit()
    return conn


def run_snapshot(source, target, timeout: float = 5):
    return subprocess.run([sys.executable, str(SCRIPT), "--source", str(source), "--target", str(target),
                           "--timeout-seconds", str(timeout)], capture_output=True, text=True,
                          env=environment(target.parent), timeout=timeout + 8)


def assert_snapshot(path):
    assert path.is_file(), "No validated snapshot was published"
    with sqlite3.connect(path.as_uri() + "?mode=ro", uri=True) as conn:
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert conn.execute("PRAGMA user_version").fetchone()[0] == 7
        assert conn.execute("SELECT count(*) FROM parent p JOIN child c ON p.id=c.id WHERE p.value != c.value").fetchone()[0] == 0
        assert conn.execute("SELECT count(*) FROM parent").fetchone()[0] > 0
        assert conn.execute("SELECT count(*) FROM parent").fetchone() == conn.execute("SELECT count(*) FROM child").fetchone()


def test_cli_includes_committed_active_wal_and_reports_distinct_identities(tmp_path):
    source, target = tmp_path / "source.db", tmp_path / "target.db"
    conn = database(source, wal=True)
    try:
        assert Path(str(source) + "-wal").stat().st_size > 0
        # Prove this synthetic family really defeats base-file copying: the schema
        # and committed row exist only in WAL. Inspect a disposable base-only probe.
        base_probe = tmp_path / "base-only-probe.db"
        base_probe.write_bytes(source.read_bytes())
        with sqlite3.connect(base_probe.as_uri() + "?mode=ro", uri=True) as probe:
            with pytest.raises(sqlite3.OperationalError, match="no such table"):
                probe.execute("SELECT value FROM parent WHERE id=1")
        result = run_snapshot(source, target)
        assert result.returncode == 0, result.stdout + result.stderr
        assert_snapshot(target)
        with sqlite3.connect(target) as captured:
            assert captured.execute("SELECT value FROM parent WHERE id=1").fetchone() == (10,)
        assert conn.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
        report = json.loads(result.stdout)
        assert Path(report["source"]) == source and Path(report["target"]) == target
    finally:
        conn.close()


def test_concurrent_atomic_multitable_writes_remain_coherent(tmp_path):
    source, target = tmp_path / "source.db", tmp_path / "target.db"
    conn = database(source, wal=True)
    stop = threading.Event()
    started = threading.Event()
    errors = []
    def writer():
        try:
            with sqlite3.connect(source) as db:
                started.set()
                while not stop.is_set():
                    db.execute("BEGIN IMMEDIATE")
                    db.execute("UPDATE parent SET value=value+1")
                    db.execute("UPDATE child SET value=value+1")
                    db.commit()
                    stop.wait(0.005)
        except Exception as exc:
            errors.append(exc)
    thread = threading.Thread(target=writer)
    thread.start()
    assert started.wait(3)
    try:
        result = run_snapshot(source, target)
        assert result.returncode == 0, result.stdout + result.stderr
        assert_snapshot(target)
    finally:
        stop.set()
        thread.join(5)
        conn.close()
    assert not thread.is_alive() and not errors


def test_busy_source_stops_at_total_deadline_without_published_seed(tmp_path):
    source, target = tmp_path / "source.db", tmp_path / "target.db"
    conn = database(source)
    conn.execute("BEGIN EXCLUSIVE")
    start = time.monotonic()
    try:
        result = run_snapshot(source, target, timeout=0.4)
    finally:
        conn.rollback()
        conn.close()
    assert time.monotonic() - start < 5
    assert result.returncode != 0
    assert not target.exists()


@pytest.mark.parametrize("kind", ("missing", "corrupt", "same", "existing", "relative"))
def test_invalid_or_colliding_identity_never_replaces_source_target(kind, tmp_path):
    source, target = tmp_path / "source.db", tmp_path / "target.db"
    if kind != "missing":
        source.write_bytes(b"CORRUPT SENTINEL")
    if kind == "same":
        target = source
    elif kind == "existing":
        target.write_bytes(b"TARGET SENTINEL")
    elif kind == "relative":
        target = Path("unapproved-relative.db")
    before_source = source.read_bytes() if source.exists() else None
    before_target = target.read_bytes() if target.is_absolute() and target.exists() else None
    result = run_snapshot(source, target)
    assert result.returncode != 0
    assert (source.read_bytes() if source.exists() else None) == before_source
    if target.is_absolute():
        assert (target.read_bytes() if target.exists() else None) == before_target
    else:
        assert not (ROOT / target).exists()


@pytest.mark.parametrize("boundary", ("before_backup", "after_backup", "before_validation",
                                     "after_validation", "before_publish"))
def test_interruption_before_publication_never_creates_final_seed(boundary, tmp_path):
    source, target = tmp_path / "source.db", tmp_path / "target.db"
    database(source).close()
    before = source.read_bytes()
    reached = []
    def interrupt(name, *args, **kwargs):
        reached.append(name)
        if name == boundary:
            raise KeyboardInterrupt("synthetic interruption")
    with pytest.raises(BaseException):
        helper().snapshot_database(source, target, boundary=interrupt)
    assert boundary in reached
    assert not target.exists()
    assert source.read_bytes() == before
    assert all(p.parent == tmp_path for p in tmp_path.iterdir())


def test_destination_appearing_at_publication_retains_sentinel(tmp_path):
    source, target = tmp_path / "source.db", tmp_path / "target.db"
    database(source).close()
    def collide(name, *args, **kwargs):
        if name == "before_publish":
            target.write_bytes(b"APPEARED TARGET")
    with pytest.raises(Exception):
        helper().snapshot_database(source, target, boundary=collide)
    assert target.read_bytes() == b"APPEARED TARGET"


def test_validation_failure_and_publish_failure_do_not_publish(tmp_path, monkeypatch):
    source, target = tmp_path / "source.db", tmp_path / "target.db"
    database(source).close()
    module = helper()
    calls = []
    def fail(*args, **kwargs):
        calls.append(args)
        raise OSError("synthetic validator unavailable")
    monkeypatch.setattr(module, "validate_snapshot", fail)
    with pytest.raises(Exception):
        module.snapshot_database(source, target)
    assert calls and not target.exists()
    calls.clear()
    module = helper()
    monkeypatch.setattr(module, "publish_snapshot", fail)
    with pytest.raises(Exception):
        module.snapshot_database(source, target)
    assert calls and not target.exists()


@pytest.mark.parametrize("host", HOSTS)
@WINDOWS_ONLY
def test_creator_predictable_tracked_collision_preserves_bytes_index_refs(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host, tracked_db=True)
    before = state(repo)
    db = repo / "data" / "database.db"
    bytes_before = db.read_bytes()
    index_before = git(repo, "ls-files", "-v", "--stage")
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline, seed="copy-current"), env=environment(repo))
    assert result.returncode != 0
    assert state(repo) == before
    assert db.read_bytes() == bytes_before
    assert git(repo, "ls-files", "-v", "--stage") == index_before
    assert "Worktree ready" not in result.stdout


@pytest.mark.parametrize("host", HOSTS)
@WINDOWS_ONLY
def test_creator_copy_current_runs_real_snapshot_helper(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    source = repo / "data" / "database.db"
    conn = database(source, wal=True)
    try:
        result = entry(host, repo / "scripts" / "new-worktree.ps1",
                       creator_args(repo, annotations, baseline, seed="copy-current"), env=environment(repo))
        assert result.returncode == 0, result.stdout + result.stderr
        assert_snapshot(repo.parent / "fixture-new" / "data" / "database.db")
    finally:
        conn.close()


@pytest.mark.parametrize("host", HOSTS)
@WINDOWS_ONLY
def test_creator_seed_error_retains_registered_ownerless_worktree(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    (repo / "data" / "database.db").write_bytes(b"INVALID SQLITE")
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline, seed="copy-current"), env=environment(repo))
    assert result.returncode != 0
    target = repo.parent / "fixture-new"
    assert target.is_dir()
    assert str(target).replace("\\", "/") in git(repo, "worktree", "list", "--porcelain")
    assert not (target / "data" / "database.db").exists()
    assert "Worktree ready" not in result.stdout
    row = next(row for row in audit(host, repo, annotations, baseline)["rows"] if Path(row["path"]) == target)
    assert row["status"] == "OWNERLESS"


@pytest.mark.parametrize("host", HOSTS)
@WINDOWS_ONLY
def test_creator_missing_helper_refuses_without_claiming_ready(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    database(repo / "data" / "database.db").close()
    missing = repo / "scripts" / "seed_worktree_snapshot.py"
    missing.rename(missing.with_suffix(".retained"))
    source_before = (repo / "data" / "database.db").read_bytes()
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline, seed="copy-current"), env=environment(repo))
    assert result.returncode != 0
    assert "Worktree ready" not in result.stdout
    assert (repo / "data" / "database.db").read_bytes() == source_before
    target = repo.parent / "fixture-new"
    if target.exists():
        assert not (target / "data" / "database.db").exists()
        row = next(row for row in audit(host, repo, annotations, baseline)["rows"] if Path(row["path"]) == target)
        assert row["registered"] and row["status"] == "OWNERLESS"


def test_source_target_identity_refused_before_any_sqlite_open(tmp_path, monkeypatch):
    source = tmp_path / "source.db"
    source.write_bytes(b"SENTINEL")
    module = helper()
    opened = []
    def reject_open(*args, **kwargs):
        opened.append(args)
        raise AssertionError("SQLite opened before identity rejection")
    monkeypatch.setattr(module.sqlite3, "connect", reject_open)
    with pytest.raises(Exception):
        module.snapshot_database(source, source)
    assert opened == []
    assert source.read_bytes() == b"SENTINEL"


def test_interruption_after_publish_has_only_complete_validated_seed(tmp_path):
    source, target = tmp_path / "source.db", tmp_path / "target.db"
    database(source).close()
    def interrupt(name, *args, **kwargs):
        if name == "after_publish":
            raise KeyboardInterrupt("after publication")
    with pytest.raises(BaseException):
        helper().snapshot_database(source, target, boundary=interrupt)
    assert_snapshot(target)


def test_native_backup_failure_does_not_publish_or_modify_source(tmp_path, monkeypatch):
    source, target = tmp_path / "source.db", tmp_path / "target.db"
    database(source).close()
    original = source.read_bytes()
    module = helper()
    connect = module.sqlite3.connect
    calls = []
    class BrokenBackup:
        def __init__(self, connection):
            self.connection = connection
        def __getattr__(self, name):
            return getattr(self.connection, name)
        def backup(self, *args, **kwargs):
            calls.append(args)
            raise sqlite3.OperationalError("synthetic online backup unavailable")
    def fail_backup(*args, **kwargs):
        connection = connect(*args, **kwargs)
        if kwargs.get("uri"):
            assert "mode=ro" in str(args[0]) and "immutable" not in str(args[0])
            return BrokenBackup(connection)
        return connection
    monkeypatch.setattr(module.sqlite3, "connect", fail_backup)
    with pytest.raises(Exception):
        module.snapshot_database(source, target)
    assert calls and not target.exists() and source.read_bytes() == original


def test_completed_but_corrupt_copy_is_rejected_by_real_validation(tmp_path):
    source, target = tmp_path / "source.db", tmp_path / "target.db"
    database(source).close()
    corrupted = []
    def corrupt_copy(name, *args, **kwargs):
        if name == "before_validation":
            copies = [p for p in tmp_path.iterdir() if p != source and p.is_file()]
            assert len(copies) == 1
            copies[0].write_bytes(b"CORRUPTED DISPOSABLE COPY")
            corrupted.append(copies[0])
    with pytest.raises(Exception):
        helper().snapshot_database(source, target, boundary=corrupt_copy)
    assert corrupted and not target.exists()
    assert_snapshot(source)


def test_actual_process_death_before_publication_retains_only_owned_scratch(tmp_path):
    source, target = tmp_path / "source.db", tmp_path / "target.db"
    database(source).close()
    original = source.read_bytes()
    code = "import importlib.util,sys,os; "
    code += f"s=importlib.util.spec_from_file_location('snapshot_child',{str(SCRIPT)!r}); "
    code += "m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m); "
    code += f"m.snapshot_database({str(source)!r},{str(target)!r},boundary=lambda name,*a,**k: os._exit(79) if name=='before_publish' else None)"
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                            env=environment(tmp_path), timeout=10)
    assert result.returncode == 79, result.stdout + result.stderr
    assert not target.exists() and source.read_bytes() == original
    owned = [p for p in tmp_path.iterdir() if p != source]
    assert owned, "Abrupt process death must leave recoverable owned scratch visible"
    assert all(p.is_file() and p.parent == tmp_path for p in owned)


def test_standalone_helper_import_does_not_bind_application_runtime(tmp_path):
    code = "import importlib.util,sys,json; "
    code += f"s=importlib.util.spec_from_file_location('snapshot_import',{str(SCRIPT)!r}); "
    code += "m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m); "
    code += "print(json.dumps([n for n in sys.modules if n=='app' or n=='utils' or n.startswith('utils.')]))"
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                            env=environment(tmp_path), timeout=10)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == []
    assert not list(tmp_path.iterdir()), "Import must not create database, logs, caches or bytecode"


@pytest.mark.parametrize("host", HOSTS)
@WINDOWS_ONLY
def test_actual_target_appearing_after_git_preserves_bytes_and_index(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    database(repo / "data" / "database.db").close()
    target = repo.parent / "fixture-new"
    db = target / "data" / "database.db"
    captured_index = tmp_path / "index-before.txt"
    args = creator_args(repo, annotations, baseline, seed="copy-current")
    params = " ".join(args[i] + " " + quote(args[i+1]) for i in range(0, len(args), 2))
    code = f". {quote(repo / 'scripts' / 'new-worktree.ps1')}; try {{ New-IsolatedWorktree " + params
    code += " -Boundary { param($name) if ($name -eq 'after_git') { "
    code += f"[IO.Directory]::CreateDirectory({quote(db.parent)}) | Out-Null; "
    code += f"[IO.File]::WriteAllText({quote(db)},'APPEARED TARGET'); "
    code += f"$index = git -C {quote(target)} ls-files -v --stage; "
    code += f"[IO.File]::WriteAllText({quote(captured_index)},($index -join [Environment]::NewLine)) "
    code += "} }; exit 0 } catch { exit 1 }"
    result = ps(host, code, env=environment(repo), timeout=40)
    assert result.returncode != 0 and target.is_dir()
    assert db.read_bytes() == b"APPEARED TARGET"
    assert git(target, "ls-files", "-v", "--stage").strip() == captured_index.read_text().strip()
    assert "Worktree ready" not in result.stdout
    row = next(row for row in audit(host, repo, annotations, baseline)["rows"] if Path(row["path"]) == target)
    assert row["status"] == "OWNERLESS"


@pytest.mark.parametrize("host", HOSTS)
@WINDOWS_ONLY
def test_creator_helper_ignores_foreign_pythonpath_startup_code(host, tmp_path):
    repo, annotations, baseline = fixture_repo(tmp_path, host)
    database(repo / "data" / "database.db").close()
    foreign = tmp_path / "foreign-python-imports"
    foreign.mkdir()
    sentinel = tmp_path / "foreign-startup-executed"
    (foreign / "sitecustomize.py").write_text(
        f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('foreign startup')\n", encoding="utf-8")
    env = environment(repo)
    env["PYTHONPATH"] = str(foreign)
    result = entry(host, repo / "scripts" / "new-worktree.ps1",
                   creator_args(repo, annotations, baseline, seed="copy-current"), env=env)
    assert result.returncode == 0, result.stdout + result.stderr
    assert not sentinel.exists(), "Foreign PYTHONPATH startup executed before snapshot helper isolation"
    assert_snapshot(repo.parent / "fixture-new" / "data" / "database.db")
    assert env["PYTHONPATH"] == str(foreign)
