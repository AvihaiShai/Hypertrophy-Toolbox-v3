"""Smoke a built distribution: inspect the tree, then serve from it.

Two modes, and the difference matters:

``bootloader``
    Launches ``Hypertrophy-Toolbox.exe`` — the PyInstaller bootloader an end
    user actually double-clicks. This is the real packaged-application test.

``payload``
    Runs the packaged application modules with an external interpreter over the
    distribution's own ``_internal/`` tree. It exercises the packaged
    templates, static assets, catalog seed, and compiled modules, and **not**
    the bootloader. It exists because Windows Smart App Control refuses to
    launch a freshly built, unsigned bootloader on the development machine
    (``WinError 4551``). Never read a passing payload run as evidence that the
    executable starts.

Static checks always run against the untouched build output; the server runs
from a throwaway copy, so first-run writes never dirty ``dist/``.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.stage_package_assets import (  # noqa: E402
    DIGEST_FILENAME,
    STAGING_RELATIVE,
    file_digest,
    verify_against_digest_manifest,
)

APPROVED_DATA_FILES = {"catalog.seed.db", "free_exercise_db_mapping.csv"}
FORBIDDEN_NAME_PREFIXES = (".personal",)
SIDECAR_SUFFIXES = ("-wal", "-shm", "-journal")

EXPECTED_EXERCISES = 1897
EXPECTED_BARBELL_MATCHES = 225

PAGES = (
    "/",
    "/workout_plan",
    "/workout_log",
    "/weekly_summary",
    "/session_summary",
    "/progression",
)
ASSETS = {
    "/static/css/base.css": "text/css",
    "/static/css/bootstrap.custom.min.css": "text/css",
    "/static/js/app.js": "javascript",
    "/static/js/modules/fetch-wrapper.js": "javascript",
    "/static/images/favicon.ico": None,
    "/static/bodymaps/hypertrophy-advanced/body_anterior.svg": "svg",
    "/static/vendor/free-exercise-db/exercises.json": "json",
    "/static/vendor/free-exercise-db/LICENSE": None,
    "/static/vendor/musclemap/VERSION": None,
    "/static/vendor/free-exercise-db/exercises/Barbell_Squat/0.jpg": "image",
}


class SmokeError(RuntimeError):
    """Raised when the distribution or the running packaged app is wrong."""


def _check(condition: bool, message: str) -> None:
    if not condition:
        raise SmokeError(message)
    print(f"  ok  {message}")


def inspect_distribution(dist: Path, digest_manifest: Path | None) -> None:
    """Assert the built tree carries only approved, tracked, intact content."""
    internal = dist / "_internal"
    _check(internal.is_dir(), f"distribution has _internal/: {internal}")

    data_files = sorted(path.name for path in (internal / "data").iterdir())
    _check(
        set(data_files) == APPROVED_DATA_FILES,
        f"data/ holds exactly the allowlist: {data_files}",
    )

    everything = list(dist.rglob("*"))
    _check(
        not [p for p in everything if p.is_dir() and p.name == ".git"],
        "no repository metadata anywhere in the distribution",
    )
    _check(
        not [p for p in everything if p.is_dir() and p.name == "auto_backup"],
        "no auto_backup directory",
    )
    _check(
        not [
            p
            for p in everything
            if p.name.startswith(FORBIDDEN_NAME_PREFIXES)
        ],
        "no personal export or utility files",
    )
    databases = sorted(
        p.relative_to(dist).as_posix()
        for p in everything
        if p.suffix == ".db"
    )
    _check(
        databases == ["_internal/data/catalog.seed.db"],
        f"the catalog seed is the only database: {databases}",
    )
    _check(
        not [
            p
            for p in everything
            if p.is_file() and p.name.endswith(SIDECAR_SUFFIXES)
        ],
        "no SQLite sidecars",
    )

    if digest_manifest is not None:
        verified = verify_against_digest_manifest(internal, digest_manifest)
        _check(
            len(verified) > 0,
            f"{len(verified)} packaged assets match {digest_manifest.name}",
        )


def _get(url: str, timeout: float = 30.0):
    request = urllib.request.Request(url, headers={"Accept": "*/*"})
    return urllib.request.urlopen(request, timeout=timeout)


def _post_json(url: str, payload: dict, timeout: float = 30.0):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    return urllib.request.urlopen(request, timeout=timeout)


def _require_free_port(port: int) -> None:
    """Refuse to smoke against a port something else already owns.

    Without this the smoke can pass while never having launched anything: it
    polls ``127.0.0.1:<port>``, some unrelated process answers, and every
    assertion runs against that instead of the packaged build.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(1.0)
        if probe.connect_ex(("127.0.0.1", port)) == 0:
            raise SmokeError(
                f"port {port} is already in use; the smoke would test whatever "
                f"owns it rather than the packaged build. Pass --port with a "
                f"free port."
            )


def _check_asset_version_policy(base_url: str) -> None:
    """F4, and the only place it can actually be verified.

    The one-year ``STATIC_LONG_MAX_AGE`` applies **only** in a frozen build, so
    the whole point of the cache-busting work is unobservable outside a packaged
    run. Three things have to hold together, and each fails differently:

    1. rendered pages carry ``?v=<APP_VERSION>`` on their first-party links;
    2. a request at the current version is long-cached;
    3. a request without one -- transitive ES-module imports and runtime-built
       asset URLs can never carry it -- must revalidate instead, or it inherits
       the year and goes stale after an upgrade, which is the bug itself.
    """
    from utils.version import APP_VERSION

    with _get(f"{base_url}/") as response:
        html = response.read().decode("utf-8", "replace")

    links = re.findall(r'(?:href|src)="(/static/(?:css|js)/[^"]+)"', html)
    _check(bool(links), "the rendered page links first-party CSS/JS")
    unversioned = [link for link in links if f"?v={APP_VERSION}" not in link]
    _check(
        not unversioned,
        f"all {len(links)} rendered first-party links carry ?v={APP_VERSION}"
        + (f" (missing on {unversioned})" if unversioned else ""),
    )

    probe = links[0].split("?")[0]

    with _get(f"{base_url}{probe}?v={APP_VERSION}") as response:
        cache_control = response.headers.get("Cache-Control", "")
    _check(
        "max-age=31536000" in cache_control and "immutable" in cache_control,
        f"versioned asset is long-cached: {probe}?v={APP_VERSION} -> "
        f"{cache_control!r}",
    )

    for label, url in (
        ("unversioned", f"{base_url}{probe}"),
        ("stale version", f"{base_url}{probe}?v=0.0.0-stale"),
        # A transitive ES-module import: fetched bare, since ?v= on the parent
        # never propagates to what it imports.
        ("transitive import", f"{base_url}/static/js/modules/fetch-wrapper.js"),
        # A runtime-built URL: JS constructs this, so no template can version it.
        (
            "runtime-built asset",
            f"{base_url}/static/bodymaps/hypertrophy-advanced/body_anterior.svg",
        ),
    ):
        with _get(url) as response:
            cache_control = response.headers.get("Cache-Control", "")
        _check(
            "no-cache" in cache_control and "31536000" not in cache_control,
            f"{label} must revalidate: {cache_control!r}",
        )


def _launch(
    work_dir: Path,
    mode: str,
    payload_python: Path | None,
    runtime_root: Path,
    port: int,
):
    child_environment = {
        **os.environ,
        "HT_NO_BROWSER": "1",
        "FLASK_USE_RELOADER": "0",
        # Never let a smoke write into the real per-user data directory.
        "HT_RUNTIME_DIR": str(runtime_root),
        # Both launch paths read this -- app_launcher.py for the bootloader and
        # app.py's __main__ for the payload. Without it they hardcode 5000 while
        # this script polls --port, so a non-default port could never work.
        "HT_PORT": str(port),
    }
    child_environment.pop("DB_FILE", None)

    if mode == "bootloader":
        executable = work_dir / "Hypertrophy-Toolbox.exe"
        if not executable.is_file():
            executable = work_dir / "Hypertrophy-Toolbox"
        if not executable.is_file():
            raise SmokeError(f"No bootloader executable in {work_dir}")
        print(f"[SMOKE] launching the real bootloader: {executable}")
        return subprocess.Popen(
            [str(executable)],
            cwd=str(work_dir),
            env=child_environment,
        )

    interpreter = payload_python or Path(sys.executable)
    entry = work_dir / "_internal" / "app.pyc"
    if not entry.is_file():
        raise SmokeError(f"No packaged application payload at {entry}")
    print("[SMOKE] *** payload mode: the bootloader is NOT exercised ***")
    print(f"[SMOKE] running {entry} with {interpreter}")
    return subprocess.Popen(
        [str(interpreter), "app.pyc"],
        cwd=str(entry.parent),
        env=child_environment,
    )


def _wait_for_server(base_url: str, process, attempts: int = 60) -> None:
    for _ in range(attempts):
        if process.poll() is not None:
            raise SmokeError(
                f"packaged app exited early with code {process.returncode}"
            )
        try:
            with _get(f"{base_url}/", timeout=5) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, OSError, TimeoutError):
            pass
        time.sleep(2)
    raise SmokeError(f"packaged app never served {base_url}/")


def serve_and_check(
    work_dir: Path,
    mode: str,
    payload_python: Path | None,
    port: int,
    runtime_root: Path,
) -> None:
    """Boot the distribution and assert it serves real catalog-backed pages."""
    _require_free_port(port)
    base_url = f"http://127.0.0.1:{port}"
    bundled_data = work_dir / "_internal" / "data"
    runtime_db = runtime_root / "data" / "database.db"
    seed = bundled_data / "catalog.seed.db"
    seed_digest = file_digest(seed)

    _check(not runtime_db.exists(), "no runtime database before first launch")

    process = _launch(work_dir, mode, payload_python, runtime_root, port)
    try:
        _wait_for_server(base_url, process)

        # Identity: prove the server answering is the child just launched, not
        # something that already owned the port. _require_free_port() showed the
        # port was free beforehand and this child is still the live owner.
        _check(
            process.poll() is None,
            f"the launched child (pid {process.pid}) is still serving",
        )

        for route in PAGES:
            with _get(f"{base_url}{route}") as response:
                _check(response.status == 200, f"GET {route} -> 200")

        for route, expected_type in ASSETS.items():
            with _get(f"{base_url}{route}") as response:
                content_type = response.headers.get("Content-Type", "")
                _check(
                    response.status == 200
                    and (
                        expected_type is None or expected_type in content_type
                    ),
                    f"GET {route} -> 200 ({content_type})",
                )

        _check_asset_version_policy(base_url)

        with _get(f"{base_url}/get_all_exercises") as response:
            exercises = json.loads(response.read())["data"]
        _check(
            len(exercises) == EXPECTED_EXERCISES,
            f"/get_all_exercises -> {len(exercises)} exercises",
        )

        with _post_json(
            f"{base_url}/filter_exercises", {"equipment": "Barbell"}
        ) as response:
            matches = json.loads(response.read())["data"]
        _check(
            len(matches) == EXPECTED_BARBELL_MATCHES,
            f"/filter_exercises Barbell -> {len(matches)} exercises",
        )
    finally:
        process.terminate()
        try:
            process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            process.kill()

    _check(
        runtime_db.is_file(),
        f"first launch created the runtime database at {runtime_db}",
    )
    _check(
        file_digest(seed) == seed_digest,
        "the packaged catalog seed is byte-identical after first run",
    )
    # The Packet B property, asserted against the real installation directory:
    # a running application must add nothing to the bundle it was installed
    # from, or an update would overwrite user data.
    _check(
        sorted(path.name for path in bundled_data.iterdir())
        == sorted(APPROVED_DATA_FILES),
        "the installation directory gained no runtime files",
    )
    _check(
        (runtime_root / "logs" / "app.log").is_file(),
        "logs were written under the runtime root, not the installation",
    )
    _check(
        not (bundled_data / "auto_backup").exists()
        and not (runtime_root / "data" / "auto_backup").exists(),
        "no redundant first-run backup",
    )


LEGACY_ROUTINE = "SMOKE - Legacy Routine"


def _plant_legacy_database(work_dir: Path) -> Path:
    """Write a pre-Packet-B database into the installation directory.

    This is what an existing user's install looks like: a real database sitting
    beside the packaged assets, because that is where every earlier release put
    it.
    """
    bundled_data = work_dir / "_internal" / "data"
    legacy = bundled_data / "database.db"
    shutil.copyfile(bundled_data / "catalog.seed.db", legacy)
    connection = sqlite3.connect(str(legacy))
    try:
        exercise = connection.execute(
            "SELECT exercise_name FROM exercises ORDER BY exercise_name LIMIT 1"
        ).fetchone()[0]
        connection.execute(
            "INSERT INTO user_selection "
            "(routine, exercise, sets, min_rep_range, max_rep_range, weight) "
            "VALUES (?, ?, 3, 8, 12, 60.0)",
            (LEGACY_ROUTINE, exercise),
        )
        connection.commit()
    finally:
        connection.close()
    return legacy


def check_upgrade_migration(
    work_dir: Path,
    mode: str,
    payload_python: Path | None,
    port: int,
    runtime_root: Path,
) -> None:
    """Assert an existing install's data moves once and survives intact."""
    legacy = _plant_legacy_database(work_dir)
    legacy_digest = file_digest(legacy)
    runtime_db = runtime_root / "data" / "database.db"
    _require_free_port(port)
    base_url = f"http://127.0.0.1:{port}"

    process = _launch(work_dir, mode, payload_python, runtime_root, port)
    try:
        _wait_for_server(base_url, process)
        with _get(f"{base_url}/get_all_exercises") as response:
            exercises = json.loads(response.read())["data"]
        _check(
            len(exercises) == EXPECTED_EXERCISES,
            f"upgraded install serves {len(exercises)} exercises",
        )
    finally:
        process.terminate()
        try:
            process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            process.kill()

    _check(runtime_db.is_file(), "the database moved to the runtime root")

    connection = sqlite3.connect(str(runtime_db))
    try:
        migrated = connection.execute(
            "SELECT COUNT(*) FROM user_selection WHERE routine = ?",
            (LEGACY_ROUTINE,),
        ).fetchone()[0]
    finally:
        connection.close()
    _check(migrated == 1, "the pre-existing plan row survived the move")

    _check(
        legacy.is_file() and file_digest(legacy) == legacy_digest,
        "the original database is still there, byte-identical",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dist",
        type=Path,
        default=REPO_ROOT / "dist" / "Hypertrophy-Toolbox",
    )
    parser.add_argument(
        "--mode",
        choices=("bootloader", "payload"),
        default="bootloader",
        help="payload mode does NOT exercise the bootloader.",
    )
    parser.add_argument(
        "--payload-python",
        type=Path,
        default=None,
        help="Interpreter for payload mode; must match the build's version.",
    )
    parser.add_argument(
        "--digest-manifest",
        type=Path,
        default=REPO_ROOT / STAGING_RELATIVE.parent / DIGEST_FILENAME,
    )
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument(
        "--skip-runtime",
        action="store_true",
        help="Inspect the built tree only.",
    )
    parser.add_argument(
        "--skip-upgrade",
        action="store_true",
        help="Skip the legacy-database migration run.",
    )
    args = parser.parse_args()

    dist = args.dist.resolve()
    digest_manifest = (
        args.digest_manifest.resolve()
        if args.digest_manifest and args.digest_manifest.is_file()
        else None
    )

    try:
        print(f"[SMOKE] inspecting {dist}")
        inspect_distribution(dist, digest_manifest)
        if args.skip_runtime:
            print("[SMOKE] PASS (static checks only)")
            return

        with tempfile.TemporaryDirectory(prefix="ht-smoke-") as temporary:
            work_dir = Path(temporary) / dist.name
            print(f"[SMOKE] copying distribution to {work_dir}")
            shutil.copytree(dist, work_dir)
            serve_and_check(
                work_dir,
                args.mode,
                args.payload_python,
                args.port,
                Path(temporary) / "runtime",
            )

            if not args.skip_upgrade:
                upgrade_dir = Path(temporary) / f"{dist.name}-upgrade"
                print(f"[SMOKE] upgrade run from {upgrade_dir}")
                shutil.copytree(dist, upgrade_dir)
                check_upgrade_migration(
                    upgrade_dir,
                    args.mode,
                    args.payload_python,
                    args.port,
                    Path(temporary) / "runtime-upgrade",
                )
    except (SmokeError, OSError, ValueError) as exc:
        raise SystemExit(f"[SMOKE] FAIL: {exc}") from exc

    label = (
        "real bootloader"
        if args.mode == "bootloader"
        else "packaged payload (bootloader NOT exercised)"
    )
    print(f"[SMOKE] PASS via {label}")


if __name__ == "__main__":
    main()
