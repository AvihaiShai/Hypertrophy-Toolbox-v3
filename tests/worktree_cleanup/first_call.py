"""Make each Windows host's first preflight call once, before the tests run.

On a fresh hosted runner the first call on each host can stall machine-wide for
10-30+ seconds (issue #614). With four workers starting together, every worker's
first call then crossed the tests' 30-second subprocess limit. CI runs this
module first, so that one-time cost is paid serially and outside that limit.
The call is the one test_absent_scopes_valid_identity_passes_without_creating_runtime makes.
"""
from __future__ import annotations

import tempfile
import time
from pathlib import Path

from tests.worktree_cleanup.support import HOSTS, ROOT, environment, json_result, ps, quote

SCRIPT = ROOT / "scripts" / "preflight-worktree-environment.ps1"
# Bounds a genuine hang. The tests keep their own 30-second limit.
HANG_LIMIT_SECONDS = 300


def first_call(host: str, root: Path) -> float:
    runtime = root / "runtime"
    runtime.mkdir(parents=True)
    code = (f". {quote(SCRIPT)}; Test-WorktreeEnvironment -ApprovedRoot {quote(root)} "
            f"-RuntimeRoot {quote(runtime)} -DatabasePath {quote(runtime / 'data' / 'database.db')} "
            "-ScopeReader { param($n,$s) @{Present=$false;Value=$null} } | ConvertTo-Json -Depth 20")
    started = time.perf_counter()
    result = ps(host, code, env=environment(root), timeout=HANG_LIMIT_SECONDS)
    elapsed = time.perf_counter() - started
    if json_result(result)["ok"] is not True:
        raise SystemExit(f"{host} first preflight call was refused:\n{result.stdout}")
    return elapsed


if __name__ == "__main__":
    # The children write compiler scratch files here; a lingering handle must not fail the step.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp:
        for name in HOSTS:
            print(f"{name} first preflight call: {first_call(name, Path(temp) / name):.1f} s", flush=True)
