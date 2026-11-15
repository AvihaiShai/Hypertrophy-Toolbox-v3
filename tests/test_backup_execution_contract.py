"""Restore-acceptance contract for the four execution fields (#567, ADR-015).

``utils/backup_execution_contract.py`` decides which stored ``execution_style``,
``time_cap_seconds``, ``emom_interval_seconds`` and ``emom_rounds`` values a program-backup
restore accepts. It holds its own literals and never reads the plan page, so narrowing a
plan-page limit cannot silently strand a backup that used to restore.

Three groups of tests live here:

* **Unit tests of the pure check** -- which rows it accepts, the exact wording of each
  problem it reports, and how a stored value is rendered in that wording.
* **The literal pin** -- the contract's constants equal the values written in this file. It
  fails when the contract itself is edited.
* **The behavioral tripwire** -- every probe in ``_PROBES`` is sent to the live plan page
  (``POST /api/execution_style``) and to the contract, and both must reach the verdict written
  beside it. It fails when the plan page and the contract stop agreeing, in either direction.

The tripwire's two halves are separate tests joined by the one probe table, so the plan-page
half runs against unmodified plan-page code without the contract module existing.

A probe's plan-page verdict is "stored as sent": the request succeeds **and** the row
afterwards holds exactly the probed values. It is read from the stored row, never from the
response, because the endpoint replaces an omitted or zero timing value with a default -- a
request for 0 rounds answers 200 and stores 5.

When a pin or tripwire test fails, do not edit the expected value to make it pass. Record a
backup-compatibility decision under ADR-015 (``docs/DECISIONS.md``) first; the failure messages
say the same.
"""
from __future__ import annotations

import ast
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, Mapping, Optional

import pytest

from utils.database import DatabaseHandler


_ROUTINE = "GYM - Full Body - Workout A"

_DECISION_REQUIRED = (
    "The plan page and the restore-acceptance contract (utils/backup_execution_contract.py) "
    "must accept the same execution styles and timing limits. Record a backup-compatibility "
    "decision under ADR-015 (docs/DECISIONS.md) before changing either side: narrowing the "
    "contract makes existing backups unrestorable, and widening the plan page alone produces "
    "backups that restore refuses."
)

# The values in force when #567 shipped. Restore keeps accepting them whatever the plan page
# does later. These literals are the pin: the contract must equal them, and the plan page is
# probed against them.
_PINNED_STYLES = ("standard", "amrap", "emom")
_PINNED_RANGES = {
    "time_cap_seconds": (10, 600),
    "emom_interval_seconds": (15, 180),
    "emom_rounds": (1, 20),
}
_PINNED_STYLE_FIELDS = {
    "standard": (),
    "amrap": ("time_cap_seconds",),
    "emom": ("emom_interval_seconds", "emom_rounds"),
}
_TIMING_FIELDS = ("time_cap_seconds", "emom_interval_seconds", "emom_rounds")
_LABELS = {
    "time_cap_seconds": "time cap",
    "emom_interval_seconds": "EMOM interval",
    "emom_rounds": "EMOM rounds",
}
_EN_DASH = "–"
_ELLIPSIS = "…"


@pytest.fixture
def contract() -> ModuleType:
    """The contract module, imported per test.

    Imported here rather than at module top so the plan-page half of the tripwire still runs
    when the contract module is missing or fails to import.
    """
    import utils.backup_execution_contract as module

    return module


def _row(
    style: Any = None,
    time_cap: Any = None,
    interval: Any = None,
    rounds: Any = None,
) -> Dict[str, Any]:
    """A backup item's four execution fields, as ``restore_backup()`` reads them."""
    return {
        "execution_style": style,
        "time_cap_seconds": time_cap,
        "emom_interval_seconds": interval,
        "emom_rounds": rounds,
    }


def _problems_by_field(problems: Any) -> Dict[str, Dict[str, str]]:
    """Index the check's result by field, asserting its shape on the way.

    Every problem is ``{"field", "value", "problem"}`` with text values only: the route puts
    them in a JSON response and in a user-facing message without further rendering.
    """
    assert isinstance(problems, list)
    indexed: Dict[str, Dict[str, str]] = {}
    for problem in problems:
        assert set(problem) == {"field", "value", "problem"}
        assert all(isinstance(text, str) for text in problem.values())
        assert problem["field"] not in indexed, "one problem per field"
        indexed[problem["field"]] = problem
    return indexed


# ---------------------------------------------------------------------------
# The literal pin
# ---------------------------------------------------------------------------


def test_contract_literals_are_pinned(contract):
    """An edit to the contract's own values fails here, with the decision-required message."""
    assert len(contract.ACCEPTED_STYLES) == len(_PINNED_STYLES), _DECISION_REQUIRED
    assert set(contract.ACCEPTED_STYLES) == set(_PINNED_STYLES), _DECISION_REQUIRED

    ranges = {field: tuple(bounds) for field, bounds in contract.TIMING_RANGES.items()}
    assert ranges == _PINNED_RANGES, _DECISION_REQUIRED

    style_fields = {
        style: set(fields) for style, fields in contract.STYLE_TIMING_FIELDS.items()
    }
    expected_style_fields = {
        style: set(fields) for style, fields in _PINNED_STYLE_FIELDS.items()
    }
    assert style_fields == expected_style_fields, _DECISION_REQUIRED


def test_contract_reads_neither_the_plan_page_nor_the_database(contract):
    """The contract holds its own literals.

    Importing the route layer would let a plan-page edit change what restore accepts, which is
    exactly what ADR-015 forbids; it would also break the ``utils`` -> ``routes`` boundary.
    The check is pure, so it needs no database access either.
    """
    source = Path(contract.__file__).read_text(encoding="utf-8")
    imported: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)

    forbidden = sorted(
        name
        for name in imported
        if name == "routes" or name.startswith("routes.") or name == "utils.database"
    )
    assert forbidden == []


# ---------------------------------------------------------------------------
# The pure check: accepted rows
# ---------------------------------------------------------------------------

_ACCEPTED_ROWS = [
    ("all_missing", _row()),
    ("standard", _row("standard")),
    ("amrap_typical", _row("amrap", time_cap=120)),
    ("amrap_time_cap_min", _row("amrap", time_cap=10)),
    ("amrap_time_cap_max", _row("amrap", time_cap=600)),
    ("emom_typical", _row("emom", interval=60, rounds=10)),
    ("emom_both_min", _row("emom", interval=15, rounds=1)),
    ("emom_both_max", _row("emom", interval=180, rounds=20)),
    # A missing timing value is never an error and is never defaulted.
    ("amrap_time_cap_missing", _row("amrap")),
    ("emom_both_missing", _row("emom")),
    ("emom_rounds_missing", _row("emom", interval=60)),
    ("emom_interval_missing", _row("emom", rounds=10)),
]


@pytest.mark.parametrize(
    "row", [case[1] for case in _ACCEPTED_ROWS], ids=[case[0] for case in _ACCEPTED_ROWS]
)
def test_check_accepts_row(contract, row):
    assert contract.check_execution_fields(row) == []


def test_check_treats_an_absent_key_as_missing(contract):
    """A legacy backup item has no value for any of the four fields."""
    assert contract.check_execution_fields({}) == []
    assert contract.check_execution_fields({"execution_style": "amrap"}) == []


def test_check_does_not_modify_the_row(contract):
    """Restore writes the stored values afterwards, so the check must leave them alone."""
    row = _row("emom", time_cap=600, interval=60, rounds=10)
    before = dict(row)
    contract.check_execution_fields(row)
    assert row == before


# ---------------------------------------------------------------------------
# The pure check: refused rows and the wording of each problem
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "style",
    ["tabata", "EMOM", " emom", ""],
    ids=["tabata", "upper_case", "leading_space", "empty_string"],
)
def test_check_refuses_an_unrecognized_style(contract, style):
    """No case folding and no trimming: an empty string is present, and unrecognized."""
    problems = _problems_by_field(contract.check_execution_fields(_row(style)))

    assert problems == {
        "execution_style": {
            "field": "execution_style",
            "value": style,
            "problem": f'execution style "{style}" is not recognized',
        }
    }


# style, field, the other fields that style needs to be otherwise valid
_USED_FIELD_CASES = [
    ("amrap", "time_cap_seconds", {}),
    ("emom", "emom_interval_seconds", {"emom_rounds": 5}),
    ("emom", "emom_rounds", {"emom_interval_seconds": 60}),
]


def _row_with(style: Optional[str], field: str, value: Any, others: Mapping[str, Any]) -> Dict[str, Any]:
    row = _row(style)
    row.update(others)
    row[field] = value
    return row


@pytest.mark.parametrize(
    "style,field,others", _USED_FIELD_CASES, ids=[case[1] for case in _USED_FIELD_CASES]
)
@pytest.mark.parametrize(
    "value,rendered",
    [("abc", "abc"), ("", ""), (12.5, "12.5")],
    ids=["text", "empty_string", "fractional"],
)
def test_check_refuses_a_timing_value_that_is_not_a_whole_number(
    contract, style, field, others, value, rendered
):
    """A value the style uses must be a whole number. A present non-int is non-numeric text,
    a fractional real or a blob."""
    problems = _problems_by_field(
        contract.check_execution_fields(_row_with(style, field, value, others))
    )

    assert problems == {
        field: {
            "field": field,
            "value": rendered,
            "problem": f'{_LABELS[field]} "{rendered}" is not a whole number',
        }
    }


_OUT_OF_RANGE_CASES = [
    ("amrap", "time_cap_seconds", {}, 0),
    ("amrap", "time_cap_seconds", {}, -5),
    ("amrap", "time_cap_seconds", {}, 9),
    ("amrap", "time_cap_seconds", {}, 601),
    ("emom", "emom_interval_seconds", {"emom_rounds": 5}, 14),
    ("emom", "emom_interval_seconds", {"emom_rounds": 5}, 181),
    ("emom", "emom_rounds", {"emom_interval_seconds": 60}, 0),
    ("emom", "emom_rounds", {"emom_interval_seconds": 60}, 21),
]


@pytest.mark.parametrize(
    "style,field,others,value",
    _OUT_OF_RANGE_CASES,
    ids=[f"{case[1]}_{case[3]}" for case in _OUT_OF_RANGE_CASES],
)
def test_check_refuses_a_timing_value_outside_the_range(contract, style, field, others, value):
    """A value the style uses must be inside its range. The range in the message is the
    contract's own, joined by an en dash."""
    low, high = _PINNED_RANGES[field]
    problems = _problems_by_field(
        contract.check_execution_fields(_row_with(style, field, value, others))
    )

    assert problems == {
        field: {
            "field": field,
            "value": str(value),
            "problem": f"{_LABELS[field]} {value} is outside {low}{_EN_DASH}{high}",
        }
    }


# stored style, the style named in the message, the unused field, its value, the rest of the row
_UNUSED_FIELD_CASES = [
    ("standard_time_cap", "standard", "standard", "time_cap_seconds", 60, {}),
    ("standard_interval", "standard", "standard", "emom_interval_seconds", 60, {}),
    ("standard_rounds", "standard", "standard", "emom_rounds", 5, {}),
    ("amrap_interval", "amrap", "amrap", "emom_interval_seconds", 60, {"time_cap_seconds": 60}),
    ("amrap_rounds", "amrap", "amrap", "emom_rounds", 5, {"time_cap_seconds": 60}),
    # A row the application cannot write: for emom the plan page clears the time cap.
    (
        "emom_time_cap_reproduction_b",
        "emom",
        "emom",
        "time_cap_seconds",
        600,
        {"emom_interval_seconds": 60, "emom_rounds": 10},
    ),
    # A missing style counts as standard.
    ("missing_style_time_cap", None, "standard", "time_cap_seconds", 60, {}),
]


@pytest.mark.parametrize(
    "stored_style,named_style,field,value,others",
    [case[1:] for case in _UNUSED_FIELD_CASES],
    ids=[case[0] for case in _UNUSED_FIELD_CASES],
)
def test_check_refuses_a_timing_value_the_style_does_not_use(
    contract, stored_style, named_style, field, value, others
):
    """A value stored against a style that does not use it is refused. Nothing is cleared or
    repaired; the row is refused as stored."""
    problems = _problems_by_field(
        contract.check_execution_fields(_row_with(stored_style, field, value, others))
    )

    assert problems == {
        field: {
            "field": field,
            "value": str(value),
            "problem": f"{_LABELS[field]} {value} is not used by the {named_style} style",
        }
    }


def test_check_collects_every_problem_of_a_row(contract):
    """The refusal names every problem, not just the first one found."""
    problems = _problems_by_field(
        contract.check_execution_fields(_row("standard", time_cap=60, rounds=5))
    )

    assert problems == {
        "time_cap_seconds": {
            "field": "time_cap_seconds",
            "value": "60",
            "problem": "time cap 60 is not used by the standard style",
        },
        "emom_rounds": {
            "field": "emom_rounds",
            "value": "5",
            "problem": "EMOM rounds 5 is not used by the standard style",
        },
    }


_STYLE_ONLY_ROWS = [
    ("timing_outside_every_range", _row("tabata", time_cap=601, interval=14, rounds=21)),
    ("timing_not_whole_numbers", _row("EMOM", time_cap="abc", interval=12.5, rounds=b"\x00")),
    ("timing_valid_for_a_real_style", _row("", time_cap=60, interval=60, rounds=5)),
]


@pytest.mark.parametrize(
    "row", [case[1] for case in _STYLE_ONLY_ROWS], ids=[case[0] for case in _STYLE_ONLY_ROWS]
)
def test_check_reports_only_the_style_when_it_is_unrecognized(contract, row):
    """An unrecognized style is the only problem reported for its row.

    With no recognized style there is nothing to judge the timing values against, so they are
    not examined -- whatever they hold.
    """
    style = row["execution_style"]

    assert contract.check_execution_fields(row) == [
        {
            "field": "execution_style",
            "value": style,
            "problem": f'execution style "{style}" is not recognized',
        }
    ]


# stored style, the style named in the message, the unused field, its value, its rendering,
# the rest of the row
_NON_INTEGER_UNUSED_FIELD_CASES = [
    ("standard_time_cap_text", "standard", "standard", "time_cap_seconds", "abc", "abc", {}),
    (
        "standard_interval_fractional",
        "standard",
        "standard",
        "emom_interval_seconds",
        12.5,
        "12.5",
        {},
    ),
    (
        "amrap_rounds_empty_string",
        "amrap",
        "amrap",
        "emom_rounds",
        "",
        "",
        {"time_cap_seconds": 60},
    ),
    (
        "emom_time_cap_blob",
        "emom",
        "emom",
        "time_cap_seconds",
        b"\x00\x01\x02",
        "<binary, 3 bytes>",
        {"emom_interval_seconds": 60, "emom_rounds": 10},
    ),
    ("missing_style_time_cap_text", None, "standard", "time_cap_seconds", "abc", "abc", {}),
]


@pytest.mark.parametrize(
    "stored_style,named_style,field,value,rendered,others",
    [case[1:] for case in _NON_INTEGER_UNUSED_FIELD_CASES],
    ids=[case[0] for case in _NON_INTEGER_UNUSED_FIELD_CASES],
)
def test_check_judges_an_unused_field_before_the_kind_of_value_it_holds(
    contract, stored_style, named_style, field, value, rendered, others
):
    """Being unused by the style wins over not being a whole number: a value in a field the
    style does not use is refused as unused, whatever kind of value it is.

    Telling the user that an unused time cap "is not a whole number" would send them to fix
    the number, when the value should not be there at all. The value is shown unquoted, as in
    every "is not used by" message.
    """
    problems = _problems_by_field(
        contract.check_execution_fields(_row_with(stored_style, field, value, others))
    )

    assert problems == {
        field: {
            "field": field,
            "value": rendered,
            "problem": f"{_LABELS[field]} {rendered} is not used by the {named_style} style",
        }
    }


# ---------------------------------------------------------------------------
# Value rendering: long text is shortened and a blob is shown by its size
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value,rendered",
    [
        ("tabata", "tabata"),
        ("", ""),
        (" emom", " emom"),
        ("x" * 40, "x" * 40),
        ("x" * 41, "x" * 40 + _ELLIPSIS),
        ("abcdefghij" * 10, "abcdefghij" * 4 + _ELLIPSIS),
        (601, "601"),
        (-5, "-5"),
        (12.5, "12.5"),
        (b"\x00\x01\x02", "<binary, 3 bytes>"),
        (b"x" * 500, "<binary, 500 bytes>"),
    ],
    ids=[
        "short_text",
        "empty_string",
        "leading_space_kept",
        "exactly_40_chars",
        "41_chars_shortened",
        "100_chars_shortened",
        "integer",
        "negative_integer",
        "fractional",
        "blob",
        "long_blob",
    ],
)
def test_render_value(contract, value, rendered):
    """Up to 40 characters as stored; longer text is its first 40 characters and an ellipsis;
    a blob is its size. Nothing is trimmed or case-folded."""
    assert contract.render_value(value) == rendered


def test_a_long_unrecognized_style_is_shortened_in_the_problem(contract):
    style = "s" * 50
    shortened = "s" * 40 + _ELLIPSIS

    problems = _problems_by_field(contract.check_execution_fields(_row(style)))

    assert problems == {
        "execution_style": {
            "field": "execution_style",
            "value": shortened,
            "problem": f'execution style "{shortened}" is not recognized',
        }
    }


def test_a_blob_timing_value_is_reported_by_its_size(contract):
    problems = _problems_by_field(
        contract.check_execution_fields(_row("amrap", time_cap=b"\x00\x01\x02\x03"))
    )

    assert problems == {
        "time_cap_seconds": {
            "field": "time_cap_seconds",
            "value": "<binary, 4 bytes>",
            "problem": 'time cap "<binary, 4 bytes>" is not a whole number',
        }
    }


# ---------------------------------------------------------------------------
# The behavioral tripwire
# ---------------------------------------------------------------------------

# probe id, style, timing values sent, and the one verdict both sides must reach:
# the plan page stores the probe exactly as sent, and the contract accepts the same row.
_PROBES = [
    # Each style the contract accepts is stored as sent -- catches the plan page dropping or
    # renaming a style.
    ("style_standard", "standard", {}, True),
    ("style_amrap", "amrap", {"time_cap_seconds": 120}, True),
    ("style_emom", "emom", {"emom_interval_seconds": 60, "emom_rounds": 10}, True),
    # One unlisted style -- catches a probe that accepts everything.
    ("style_unlisted_tabata", "tabata", {}, False),
    # Each limit value is stored as sent -- catches a narrowed limit.
    ("time_cap_min_10", "amrap", {"time_cap_seconds": 10}, True),
    ("time_cap_max_600", "amrap", {"time_cap_seconds": 600}, True),
    ("interval_min_15", "emom", {"emom_interval_seconds": 15, "emom_rounds": 5}, True),
    ("interval_max_180", "emom", {"emom_interval_seconds": 180, "emom_rounds": 5}, True),
    ("rounds_min_1", "emom", {"emom_interval_seconds": 60, "emom_rounds": 1}, True),
    ("rounds_max_20", "emom", {"emom_interval_seconds": 60, "emom_rounds": 20}, True),
    # One step beyond each limit is not stored as sent -- catches a widened limit.
    ("time_cap_below_9", "amrap", {"time_cap_seconds": 9}, False),
    ("time_cap_above_601", "amrap", {"time_cap_seconds": 601}, False),
    ("interval_below_14", "emom", {"emom_interval_seconds": 14, "emom_rounds": 5}, False),
    ("interval_above_181", "emom", {"emom_interval_seconds": 181, "emom_rounds": 5}, False),
    # 0 rounds answers 200 and stores the default 5, so only the stored row shows the refusal.
    ("rounds_below_0", "emom", {"emom_interval_seconds": 60, "emom_rounds": 0}, False),
    ("rounds_above_21", "emom", {"emom_interval_seconds": 60, "emom_rounds": 21}, False),
]
_PROBE_IDS = [probe[0] for probe in _PROBES]
_PROBE_PARAMS = [probe[1:] for probe in _PROBES]

# A starting state no probe asks for, so a row that still holds it was not written.
_SENTINEL = {
    "execution_style": "amrap",
    "time_cap_seconds": 333,
    "emom_interval_seconds": None,
    "emom_rounds": None,
}


def _probe_as_row(style: str, timing: Mapping[str, Any]) -> Dict[str, Any]:
    """The row a probe asks for: its style, the timing values it sends, the rest empty."""
    row: Dict[str, Any] = {"execution_style": style}
    for field in _TIMING_FIELDS:
        row[field] = timing.get(field)
    return row


def _stored_execution_fields(plan_id: int) -> Dict[str, Any]:
    with DatabaseHandler() as db:
        stored = db.fetch_one(
            "SELECT execution_style, time_cap_seconds, emom_interval_seconds, emom_rounds "
            "FROM user_selection WHERE id = ?",
            (plan_id,),
        )
    assert stored is not None
    return dict(stored)


@pytest.mark.parametrize("style,timing,expected", _PROBE_PARAMS, ids=_PROBE_IDS)
def test_tripwire_plan_page_stores_probe_as_sent(
    client, clean_db, exercise_factory, workout_plan_factory, style, timing, expected
):
    """The live plan page reaches the verdict written beside each probe."""
    exercise_name = exercise_factory("Tripwire Probe Press")
    plan_id = workout_plan_factory(exercise_name=exercise_name, routine=_ROUTINE)
    with DatabaseHandler() as db:
        db.execute_query(
            "UPDATE user_selection SET execution_style = ?, time_cap_seconds = ?, "
            "emom_interval_seconds = ?, emom_rounds = ? WHERE id = ?",
            (
                _SENTINEL["execution_style"],
                _SENTINEL["time_cap_seconds"],
                _SENTINEL["emom_interval_seconds"],
                _SENTINEL["emom_rounds"],
                plan_id,
            ),
        )
    assert _stored_execution_fields(plan_id) == _SENTINEL

    payload: Dict[str, Any] = {"exercise_id": plan_id, "execution_style": style}
    payload.update(timing)
    response = client.post("/api/execution_style", json=payload)

    stored = _stored_execution_fields(plan_id)
    stored_as_sent = response.status_code == 200 and stored == _probe_as_row(style, timing)

    assert stored_as_sent is expected, (
        f"Plan page verdict for probe {payload!r} changed: HTTP {response.status_code}, "
        f"row now holds {stored!r}. {_DECISION_REQUIRED}"
    )
    if response.status_code != 200:
        # A rejected request must not have written anything either.
        assert stored == _SENTINEL


@pytest.mark.parametrize("style,timing,expected", _PROBE_PARAMS, ids=_PROBE_IDS)
def test_tripwire_contract_reaches_the_same_verdict(contract, style, timing, expected):
    """The contract accepts exactly the probes the plan page stores as sent."""
    row = _probe_as_row(style, timing)

    accepted = contract.check_execution_fields(row) == []

    assert accepted is expected, (
        f"Contract verdict for row {row!r} changed. {_DECISION_REQUIRED}"
    )


def test_tripwire_options_payload_advertises_the_pinned_styles(client, clean_db):
    """A style added to or removed from the plan page's advertised list, in either direction."""
    response = client.get("/api/execution_style_options")
    assert response.status_code == 200

    advertised = set(response.get_json()["data"]["styles"])

    assert advertised == set(_PINNED_STYLES), _DECISION_REQUIRED


def test_tripwire_options_payload_advertises_the_pinned_limits(client, clean_db):
    """The advertised numbers, in either direction."""
    response = client.get("/api/execution_style_options")
    assert response.status_code == 200

    advertised = response.get_json()["data"]["limits"]
    expected = {
        field: {"min": low, "max": high} for field, (low, high) in _PINNED_RANGES.items()
    }

    assert advertised == expected, _DECISION_REQUIRED
