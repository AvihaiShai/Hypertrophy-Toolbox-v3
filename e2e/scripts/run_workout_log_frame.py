"""Measure the Workout Log against its signed frame requirements on a scratch database.

Kept so the Log's documented command still works. The launcher for every route is
run_frame_check.py; this is `run_frame_check.py --route workout_log`.
"""
from __future__ import annotations

from collections.abc import Sequence

if __package__:
    from . import run_frame_check
else:
    import run_frame_check


def main(argv: Sequence[str] | None = None) -> None:
    run_frame_check.main(argv, fixed_route="workout_log")


if __name__ == "__main__":
    main()
