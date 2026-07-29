"""Canonical minimum-Python contract for source, launcher, and build paths.

Deliberate exception to the utils/ "never print()" convention: this module is
the pre-flight check that runs before anything else, including from START.bat
and build_exe.bat via `python -m utils.python_version`. Importing get_logger()
here would build the runtime path tree and open a log file as a side effect of
asking which interpreter is running, and the batch callers need a message on
stderr rather than in app.log. See docs/DECISIONS.md ADR-003.
"""

from __future__ import annotations

import sys
from collections.abc import Sequence


MIN_PYTHON = (3, 14, 6)
MIN_PYTHON_TEXT = ".".join(str(part) for part in MIN_PYTHON)


def require_supported_python(
    version_info: Sequence[int] | None = None,
) -> None:
    """Raise a clear error when the interpreter is below the project floor."""
    current = tuple((version_info or sys.version_info)[:3])
    if current < MIN_PYTHON:
        current_text = ".".join(str(part) for part in current)
        raise RuntimeError(
            "Hypertrophy Toolbox requires Python "
            f"{MIN_PYTHON_TEXT} or newer; found Python {current_text}."
        )


def main() -> int:
    """CLI contract used by the Windows launcher and build scripts."""
    try:
        require_supported_python()
    except RuntimeError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"Python {MIN_PYTHON_TEXT}+ requirement satisfied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
