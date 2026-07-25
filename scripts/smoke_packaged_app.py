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
import shutil
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


def _launch(work_dir: Path, mode: str, payload_python: Path | None):
    child_environment = {
        **os.environ,
        "HT_NO_BROWSER": "1",
        "FLASK_USE_RELOADER": "0",
    }

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
) -> None:
    """Boot the distribution and assert it serves real catalog-backed pages."""
    base_url = f"http://127.0.0.1:{port}"
    runtime_db = work_dir / "_internal" / "data" / "database.db"
    seed = work_dir / "_internal" / "data" / "catalog.seed.db"
    seed_digest = file_digest(seed)

    _check(not runtime_db.exists(), "no runtime database before first launch")

    process = _launch(work_dir, mode, payload_python)
    try:
        _wait_for_server(base_url, process)
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

    _check(runtime_db.is_file(), "first launch created the runtime database")
    _check(
        file_digest(seed) == seed_digest,
        "the packaged catalog seed is byte-identical after first run",
    )
    _check(
        not (work_dir / "_internal" / "data" / "auto_backup").exists(),
        "no redundant first-run backup",
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
                work_dir, args.mode, args.payload_python, args.port
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
