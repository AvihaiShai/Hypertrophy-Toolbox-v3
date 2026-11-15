"""The execution-field values a program-backup restore accepts (ADR-015).

The literals below are deliberately **not** read from the plan page
(``routes/workout_plan.py``): the two agree today, but a later narrowing of a
plan-page limit must not turn a backup that used to restore into one that is
refused. ``tests/test_backup_execution_contract.py`` pins these literals and
probes the live plan page against them, in both directions. When either test
fails, record a backup-compatibility decision under ADR-015
(``docs/DECISIONS.md``) before changing this module or the plan page.
"""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Tuple

# The execution styles restore accepts, compared exactly: no case folding and no
# trimming. An empty string is a present value and is not one of these.
ACCEPTED_STYLES: Tuple[str, ...] = ("standard", "amrap", "emom")

# Inclusive (minimum, maximum) for each timing field.
TIMING_RANGES: Dict[str, Tuple[int, int]] = {
    "time_cap_seconds": (10, 600),
    "emom_interval_seconds": (15, 180),
    "emom_rounds": (1, 20),
}

# The timing fields each style uses. A present value in any other timing field
# is a value stored against a style that does not use it.
STYLE_TIMING_FIELDS: Dict[str, Tuple[str, ...]] = {
    "standard": (),
    "amrap": ("time_cap_seconds",),
    "emom": ("emom_interval_seconds", "emom_rounds"),
}

# A missing style (SQL NULL, or a backup that predates the column) is judged,
# and restored, as this style. No timing value has a default.
MISSING_STYLE = "standard"

_STYLE_FIELD = "execution_style"

_TIMING_LABELS: Dict[str, str] = {
    "time_cap_seconds": "time cap",
    "emom_interval_seconds": "EMOM interval",
    "emom_rounds": "EMOM rounds",
}

# Longest text shown as stored; anything longer is cut to this many characters
# and an ellipsis.
_MAX_RENDERED_CHARS = 40
_ELLIPSIS = "\N{HORIZONTAL ELLIPSIS}"
_EN_DASH = "\N{EN DASH}"


def render_value(value: object) -> str:
    """Render a stored value as text: long text is shortened, a blob is reported by its size."""
    if isinstance(value, bytes):
        return f"<binary, {len(value)} bytes>"
    if isinstance(value, str):
        if len(value) > _MAX_RENDERED_CHARS:
            return value[:_MAX_RENDERED_CHARS] + _ELLIPSIS
        return value
    return str(value)


def _problem(field: str, rendered: str, problem: str) -> Dict[str, str]:
    return {"field": field, "value": rendered, "problem": problem}


def check_execution_fields(row: Mapping[str, Any]) -> List[Dict[str, str]]:
    """Return one ``{"field", "value", "problem"}`` entry per execution field restore refuses.

    A missing value (absent key or ``None``) is never a problem, and an
    unrecognized style is the only problem reported for its row.
    """
    style = row.get(_STYLE_FIELD)
    if style is None:
        style = MISSING_STYLE
    elif style not in ACCEPTED_STYLES:
        rendered = render_value(style)
        return [
            _problem(
                _STYLE_FIELD,
                rendered,
                f'execution style "{rendered}" is not recognized',
            )
        ]

    used_fields = STYLE_TIMING_FIELDS[style]
    problems: List[Dict[str, str]] = []
    for field, (minimum, maximum) in TIMING_RANGES.items():
        value = row.get(field)
        if value is None:
            continue

        label = _TIMING_LABELS[field]
        rendered = render_value(value)
        if field not in used_fields:
            problems.append(
                _problem(field, rendered, f"{label} {rendered} is not used by the {style} style")
            )
        elif isinstance(value, bool) or not isinstance(value, int):
            problems.append(
                _problem(field, rendered, f'{label} "{rendered}" is not a whole number')
            )
        elif not minimum <= value <= maximum:
            problems.append(
                _problem(
                    field,
                    rendered,
                    f"{label} {rendered} is outside {minimum}{_EN_DASH}{maximum}",
                )
            )
    return problems
