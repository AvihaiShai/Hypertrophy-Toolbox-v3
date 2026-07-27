"""Selector specificity model for the WP4.4 audit harness.

Method rule M4: a model that mishandles ``:is()``/``:where()``/``:not()``/``:has()``
or naively comma-splits a selector list reports an owner that contradicts the
computed value. Two failure modes this module exists to avoid:

* ``split(",")`` on ``:is(a, #b)`` yields two fragments that are not selectors.
* ``:where(...)`` contributes zero, so a rule can look ID-heavy and lose.

``self_check()`` runs the hand-computed cases; the harness refuses to emit a
baseline until it passes.
"""

from __future__ import annotations

import re
from typing import NamedTuple


class Specificity(NamedTuple):
    """CSS specificity as the usual (a, b, c) triple."""

    ids: int
    classes: int
    types: int

    def __str__(self) -> str:
        return f"({self.ids},{self.classes},{self.types})"


ZERO = Specificity(0, 0, 0)

# Pseudo-classes whose specificity is that of their most specific argument.
_MATCHES_ANY = ("is", "not", "has", "matches", "-webkit-any", "-moz-any")
# Pseudo-classes that contribute nothing themselves and nothing from arguments.
_ZERO_SPECIFICITY = ("where",)
# Pseudo-elements: one type-level unit, and their arguments never count.
_PSEUDO_ELEMENTS = (
    "before",
    "after",
    "first-line",
    "first-letter",
    "selection",
    "placeholder",
    "backdrop",
    "marker",
    "file-selector-button",
)

_FUNCTIONAL_RE = re.compile(r"(::?)([\w-]+)\(")
_SIMPLE_RE = re.compile(
    r"""
    (?P<id>\#[\w-]+)
  | (?P<class>\.[\w-]+)
  | (?P<attr>\[[^\]]*\])
  | (?P<pseudo_element>::[\w-]+)
  | (?P<pseudo_class>:[\w-]+)
  | (?P<type>(?:[\w-]+\|)?[\w-]+|\*)
    """,
    re.VERBOSE,
)


def _add(left: Specificity, right: Specificity) -> Specificity:
    return Specificity(
        left.ids + right.ids,
        left.classes + right.classes,
        left.types + right.types,
    )


def split_selector_list(selector_list: str) -> list[str]:
    """Split a selector list on top-level commas only.

    Commas inside ``()``, ``[]`` or a quoted string belong to a functional
    pseudo-class argument, not to the list.
    """
    parts: list[str] = []
    depth = 0
    quote: str | None = None
    current: list[str] = []

    for char in selector_list:
        if quote is not None:
            current.append(char)
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
            current.append(char)
            continue
        if char in "([":
            depth += 1
        elif char in ")]":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)

    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return [part for part in parts if part]


def _read_balanced(text: str, open_index: int) -> tuple[str, int]:
    """Return the argument inside the parens opened at ``open_index``."""
    depth = 0
    quote: str | None = None
    for index in range(open_index, len(text)):
        char = text[index]
        if quote is not None:
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[open_index + 1 : index], index + 1
    raise ValueError(f"unbalanced parenthesis in selector: {text!r}")


def compound_specificity(selector: str) -> Specificity:
    """Specificity of a single complex selector (no top-level commas)."""
    total = ZERO
    index = 0
    text = selector.strip()

    while index < len(text):
        char = text[index]

        if char in " >+~\t\n":
            index += 1
            continue

        functional = _FUNCTIONAL_RE.match(text, index)
        if functional:
            colons, name = functional.group(1), functional.group(2).lower()
            argument, next_index = _read_balanced(text, functional.end() - 1)

            if colons == "::" or name in _PSEUDO_ELEMENTS:
                total = _add(total, Specificity(0, 0, 1))
            elif name in _ZERO_SPECIFICITY:
                pass
            elif name in _MATCHES_ANY:
                total = _add(total, selector_list_specificity(argument))
            elif name == "nth-child" or name == "nth-last-child":
                # `of S` takes the most specific S; the An+B part is one class.
                total = _add(total, Specificity(0, 1, 0))
                _, _, of_clause = argument.partition(" of ")
                if of_clause.strip():
                    total = _add(total, selector_list_specificity(of_clause))
            else:
                total = _add(total, Specificity(0, 1, 0))

            index = next_index
            continue

        simple = _SIMPLE_RE.match(text, index)
        if not simple:
            index += 1
            continue

        if simple.group("id"):
            total = _add(total, Specificity(1, 0, 0))
        elif simple.group("class") or simple.group("attr"):
            total = _add(total, Specificity(0, 1, 0))
        elif simple.group("pseudo_element"):
            total = _add(total, Specificity(0, 0, 1))
        elif simple.group("pseudo_class"):
            name = simple.group("pseudo_class")[1:].lower()
            if name in _PSEUDO_ELEMENTS:
                total = _add(total, Specificity(0, 0, 1))
            else:
                total = _add(total, Specificity(0, 1, 0))
        elif simple.group("type"):
            if simple.group("type") != "*":
                total = _add(total, Specificity(0, 0, 1))

        index = simple.end()

    return total


def selector_list_specificity(selector_list: str) -> Specificity:
    """Specificity of a list: the maximum over its branches (the `:is()` rule)."""
    branches = split_selector_list(selector_list)
    if not branches:
        return ZERO
    return max((compound_specificity(branch) for branch in branches), key=tuple)


def branch_specificities(selector_list: str) -> list[tuple[str, Specificity]]:
    """Per-branch specificity — what a rule actually applies at, branch by branch.

    A rule's *effective* specificity is uniform across its branches only when the
    branches agree. Where they do not, this is the list that shows an ID branch
    exporting its weight through a shared `:is()`.
    """
    return [
        (branch, compound_specificity(branch))
        for branch in split_selector_list(selector_list)
    ]


# Hand-computed cases. Each entry is (selector, expected triple, why).
SELF_CHECK_CASES: tuple[tuple[str, tuple[int, int, int], str], ...] = (
    ("#workout", (1, 0, 0), "bare id"),
    (".workout-log-page", (0, 1, 0), "bare class"),
    ("div", (0, 0, 1), "bare type"),
    ("*", (0, 0, 0), "universal contributes nothing"),
    ("#workout[data-page='workout-plan']", (1, 1, 0), "id + attribute"),
    (
        ":is(#workout, .workout-log-page)",
        (1, 0, 0),
        "M4 core: :is() takes the MOST specific branch, so the id leaks out",
    ),
    (
        ":where(#workout, .workout-log-page)",
        (0, 0, 0),
        "M4 core: :where() is always zero, however id-heavy its argument",
    ),
    (
        "table:is(#workout[data-page='workout-plan'], .summary-frame.frame-calm-glass) td",
        (1, 1, 2),
        "the shared WP4.4 shape: id branch wins, plus table + td types",
    ),
    (
        "table:where(#workout[data-page='workout-plan'], .summary-frame.frame-calm-glass) td",
        (0, 0, 2),
        "the N9 :where() repair shape: the same rule drops to two types",
    ),
    (":not(.a, #b)", (1, 0, 0), ":not() also takes the most specific argument"),
    (":has(> .child)", (0, 1, 0), ":has() takes its argument's specificity"),
    ("a:hover", (0, 1, 1), "pseudo-class is class-level; the `a` is still a type"),
    ("a::before", (0, 0, 2), "pseudo-element is TYPE-level, so both units land in c"),
    ("li:nth-child(2n + 1)", (0, 1, 1), "nth-child is one class, li is one type"),
    (
        "input.input-calm-inset:is(#weight, #sets)",
        (1, 1, 1),
        "the second id-exporting construct in components.css",
    ),
    (
        "#a #b .c .d .e span",
        (2, 3, 1),
        "additive counting across a descendant chain",
    ),
    (
        "[data-theme='dark'] .frame-header",
        (0, 2, 0),
        "attribute selector counts as a class",
    ),
)

# Lists whose top-level comma split must not fall inside a functional argument.
SPLIT_SELF_CHECK_CASES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        ":is(#workout, .log), .other",
        (":is(#workout, .log)", ".other"),
    ),
    (
        "a[title='x,y'], b",
        ("a[title='x,y']", "b"),
    ),
    (
        ":is(a, :is(b, c)), d",
        (":is(a, :is(b, c))", "d"),
    ),
)


def self_check() -> list[str]:
    """Return a list of failure strings; empty means the model is trustworthy."""
    failures: list[str] = []

    for selector, expected, why in SELF_CHECK_CASES:
        actual = selector_list_specificity(selector)
        if tuple(actual) != expected:
            failures.append(
                f"specificity({selector!r}) = {tuple(actual)}, hand-computed {expected} — {why}"
            )

    for selector_list, expected_parts in SPLIT_SELF_CHECK_CASES:
        actual_parts = tuple(split_selector_list(selector_list))
        if actual_parts != expected_parts:
            failures.append(
                f"split({selector_list!r}) = {actual_parts}, hand-computed {expected_parts}"
            )

    return failures
