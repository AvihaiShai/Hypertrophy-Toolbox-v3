"""Restore-acceptance contract for the four execution fields of a program backup.

Decides which stored ``execution_style``, ``time_cap_seconds``,
``emom_interval_seconds`` and ``emom_rounds`` values ``restore_backup()``
(``utils/program_backup.py``) accepts. ADR-015 (``docs/DECISIONS.md``) records
the decision.

The literals below are the contract. They are deliberately **not** read from the
plan page (``routes/workout_plan.py``): the two agree today, but a later
narrowing of a plan-page limit must not turn a backup that used to restore into
one that is refused. ``tests/test_backup_execution_contract.py`` pins these
literals and probes the live plan page against them, in both directions. When
either test fails, record a backup-compatibility decision under ADR-015 before
changing this module or the plan page.

There are no defaults here. Restore never fills in a missing timing value.

This module is pure: no database access, no logging, no imports from ``routes``.
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
# and restored, as this style.
_MISSING_STYLE = "standard"

_STYLE_FIELD = "execution_style"

_TIMING_LABELS: Dict[str, str] = {
    "time_cap_seconds": "time cap",
    "emom_interval_seconds": "EMOM interval",
    "emom_rounds": "EMOM rounds",
}

# Longest text shown as stored; anything longer is cut to this many characters
# and an ellipsis (owner decision (iii), Gate 1 of #567).
_MAX_RENDERED_CHARS = 40
_ELLIPSIS = "\N{HORIZONTAL ELLIPSIS}"
_EN_DASH = "\N{EN DASH}"


def render_value(value: object) -> str:
    """Render a stored value as text for the refusal message and response.

    Text of up to 40 characters is returned as stored -- nothing is trimmed or
    case-folded. Longer text is its first 40 characters and an ellipsis. A blob
    is reported by its size. Anything else, a number in practice, is ``str()``.
    """
    if isinstance(value, (bytes, bytearray, memoryview)):
        return f"<binary, {len(value)} bytes>"
    if isinstance(value, str):
        if len(value) > _MAX_RENDERED_CHARS:
            return value[:_MAX_RENDERED_CHARS] + _ELLIPSIS
        return value
    return str(value)


def _problem(field: str, rendered: str, problem: str) -> Dict[str, str]:
    return {"field": field, "value": rendered, "problem": problem}


def check_execution_fields(row: Mapping[str, Any]) -> List[Dict[str, str]]:
    """Return every reason ``row``'s execution fields cannot be restored.

    ``row`` is a backup item. A field is *missing* when its key is absent or its
    value is ``None``; a missing value is never a problem. The result is empty
    when the row can be restored as stored, and otherwise holds one
    ``{"field", "value", "problem"}`` entry per offending field, all text.
    ``row`` is not modified.

    A present style that is not exactly one of ``ACCEPTED_STYLES`` is the only
    problem reported for its row: with no recognized style there is nothing to
    judge the timing values against.
    """
    style = row.get(_STYLE_FIELD)
    if style is None:
        style = _MISSING_STYLE
    elif not isinstance(style, str) or style not in ACCEPTED_STYLES:
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
