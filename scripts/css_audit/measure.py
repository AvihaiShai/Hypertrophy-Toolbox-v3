"""Static measurement of the seven WP4.4 shared surfaces.

Everything here is derived from files on disk at a known commit. Nothing is
projected, and nothing is inherited from an earlier arc's baseline — F14 is the
reason V3/V4 compare against *this* measurement rather than the WP4.1 JSON,
which is kept only as the immutable historical anchor.
"""

from __future__ import annotations

import ast
import re
import subprocess
from pathlib import Path

from . import specificity

ROOT = Path(__file__).resolve().parents[2]
CSS_DIR = ROOT / "static" / "css"

# The seven surfaces this arc rewrites, in cascade (link) order.
SHARED_SURFACES = (
    "motion.css",
    "base.css",
    "layout.css",
    "components.css",
    "navbar.css",
    "theme-dark.css",
    "a11y.css",
)
# Read but never written by this arc: R1 freezes tokens.css.
READ_ONLY_SURFACES = ("tokens.css",)

CONTRACT_FILES = (
    "tests/test_css_cascade_contracts.py",
    "tests/test_visual_selector_contracts.py",
)

IMPORTANT_RE = re.compile(r"!\s*important", re.IGNORECASE)
LAYER_BLOCK_RE = re.compile(r"@layer\s+([\w-]+)\s*\{")
LAYER_STATEMENT_RE = re.compile(r"@layer\s+([^;{}]+);")
COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)


def _blank_comments(css: str) -> str:
    """Replace comment bodies with spaces, preserving offsets and line numbers."""
    return COMMENT_RE.sub(lambda match: re.sub(r"[^\n]", " ", match.group(0)), css)


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def source_commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


# --------------------------------------------------------------------------
# Per-surface counts
# --------------------------------------------------------------------------


def surface_counts(filename: str) -> dict[str, int]:
    """Line count plus `!important` in BOTH units.

    F15: the plan's headline figures are `rg --count` *line* counts while
    Stylelint's `declaration-no-important` counts *declarations*. Three units
    are recorded because on these surfaces they genuinely disagree:

    * `importantLines` — a line matching `!important` (the plan's 1,264).
    * `importantOccurrences` — every match, comments included.
    * `importantDeclarations` — matches outside comments. This is the only unit
      comparable to Stylelint, and it is authoritative for V3.

    `theme-dark.css:595` carries the literal text "Zero !important." inside a
    comment, which is why the raw units over-count by exactly one arc-wide.
    """
    return counts_from_text((CSS_DIR / filename).read_text(encoding="utf-8"))


def counts_from_text(text: str) -> dict[str, int]:
    """The same measurement, over arbitrary text rather than a file on disk.

    Split out so a baseline can be checked against the surfaces **as they were
    at the commit it was measured at**, which is the only claim a baseline
    actually makes. Comparing it to HEAD instead couples it to every later
    packet, and the first legitimate deletion in the arc reds it.
    """
    code = _blank_comments(text)
    lines = text.splitlines()

    return {
        "lines": len(lines),
        "bytes": len(text.encode("utf-8")),
        "importantLines": sum(1 for line in lines if IMPORTANT_RE.search(line)),
        "importantOccurrences": len(IMPORTANT_RE.findall(text)),
        "importantDeclarations": len(IMPORTANT_RE.findall(code)),
    }


def surface_text_at(commit: str, filename: str) -> str:
    """`static/css/<filename>` as committed at ``commit``."""
    return subprocess.run(
        ["git", "show", f"{commit}:static/css/{filename}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    ).stdout


# --------------------------------------------------------------------------
# @layer spans (G10 / N2)
# --------------------------------------------------------------------------


def layer_spans(filename: str) -> list[dict[str, object]]:
    """Exact open/close line of every `@layer name { … }` block in a file.

    N2 freezes layer membership arc-wide, which is only checkable if the spans
    are recorded exactly: a rule "inside layer workout" is a claim about line
    ranges, and layered normal declarations lose to every unlayered one while
    layered `!important` wins over every unlayered one.
    """
    raw = (CSS_DIR / filename).read_text(encoding="utf-8")
    text = _blank_comments(raw)
    spans: list[dict[str, object]] = []

    for match in LAYER_BLOCK_RE.finditer(text):
        open_index = text.index("{", match.start())
        depth = 0
        close_index = None
        for index in range(open_index, len(text)):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    close_index = index
                    break
        if close_index is None:
            raise ValueError(f"unclosed @layer block in {filename} at {match.start()}")

        spans.append(
            {
                "layer": match.group(1),
                "openLine": _line_of(text, match.start()),
                "closeLine": _line_of(text, close_index),
            }
        )

    return spans


def layer_order() -> list[str]:
    text = (CSS_DIR / "tokens.css").read_text(encoding="utf-8")
    match = LAYER_STATEMENT_RE.search(text)
    if not match:
        raise ValueError("no @layer order statement in tokens.css")
    return [name.strip() for name in match.group(1).split(",")]


# --------------------------------------------------------------------------
# The `:is()` family (A10 / G1)
# --------------------------------------------------------------------------


def _selector_before(text: str, brace_index: int) -> tuple[str, int]:
    """Return the selector text preceding a `{`, and its start offset."""
    start = brace_index
    while start > 0 and text[start - 1] not in "{};":
        start -= 1
    return text[start:brace_index].strip(), start


def _enclosing_at_rules(text: str, index: int) -> list[str]:
    """Names of the at-rule blocks enclosing ``index``, outermost first."""
    stack: list[tuple[str, int]] = []
    for position, char in enumerate(text):
        if position >= index:
            break
        if char == "{":
            prelude, _ = _selector_before(text, position)
            stack.append((prelude, position))
        elif char == "}":
            if stack:
                stack.pop()
    return [prelude for prelude, _ in stack if prelude.startswith("@")]


def is_family(filename: str = "components.css") -> list[dict[str, object]]:
    """Enumerate and classify **every** `:is(` occurrence in a surface.

    A10: the plan's "complete `:is()` family" is twelve four-branch rules plus a
    three-branch reduced-motion rule at `:4433`; `components.css` contains 19
    `:is(` occurrences in total. The remainder must be classified rather than
    waved past, so R3 condition 1 ("the complete affected family") has a
    defensible closure argument.
    """
    raw = (CSS_DIR / filename).read_text(encoding="utf-8")
    text = _blank_comments(raw)
    records: list[dict[str, object]] = []

    for match in re.finditer(r":is\(", text):
        brace_index = text.find("{", match.start())
        if brace_index == -1:
            continue
        selector, selector_start = _selector_before(text, brace_index)
        # An occurrence inside a declaration value (rare) has no selector.
        if ":is(" not in selector:
            continue

        branches = specificity.branch_specificities(selector)
        # The `:is()` argument list is what exports weight across branches.
        argument_start = match.end() - 1
        argument, _ = specificity._read_balanced(text, argument_start)
        argument_branches = specificity.branch_specificities(argument)

        records.append(
            {
                "selectorLine": _line_of(text, selector_start),
                "isTokenLine": _line_of(text, match.start()),
                "ruleLine": _line_of(text, brace_index),
                "selector": " ".join(selector.split()),
                "selectorSpecificity": str(
                    specificity.selector_list_specificity(selector)
                ),
                "topLevelBranchCount": len(branches),
                "isArgumentBranchCount": len(argument_branches),
                "isArgumentBranches": [
                    {"branch": " ".join(branch.split()), "specificity": str(value)}
                    for branch, value in argument_branches
                ],
                "exportsIdWeight": any(
                    value.ids > 0 for _, value in argument_branches
                )
                and not all(value.ids > 0 for _, value in argument_branches),
                "enclosingAtRules": [
                    " ".join(rule.split())
                    for rule in _enclosing_at_rules(text, match.start())
                ],
            }
        )

    return records


# --------------------------------------------------------------------------
# Contract-anchor + pinned-declaration register (A8 + F6)
# --------------------------------------------------------------------------


def contract_anchors() -> list[dict[str, object]]:
    """Every contract assertion that reads one of the seven shared surfaces.

    A8: without this, each packet discovers its ceiling at gate time. F6: AC4's
    "proven disjoint at the file level" is already false for b–f, because the
    shared contract file pins strings *inside* `navbar.css` and `a11y.css`.

    Derived by walking the test files' ASTs rather than grepping, so a renamed
    test cannot silently drop out of the register.
    """
    anchors: list[dict[str, object]] = []
    surfaces = set(SHARED_SURFACES) | set(READ_ONLY_SURFACES)

    for relative in CONTRACT_FILES:
        path = ROOT / relative
        source = path.read_text(encoding="utf-8")
        lines = source.splitlines()
        tree = ast.parse(source)

        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            if not node.name.startswith("test_"):
                continue

            body_source = ast.get_source_segment(source, node) or ""
            touched = sorted(
                name for name in surfaces if name in body_source
            )
            # Functions that reach a surface through a dict of bundles rather
            # than a literal filename still bind it; record the indirection.
            indirect = sorted(
                name
                for name in ("FRAME_ROUTE_BUNDLES", "GLOBAL_BUNDLES", "ROUTE_BUNDLES")
                if name in body_source
            )
            if not touched and not indirect:
                continue

            assertion_lines = [
                sub.lineno
                for sub in ast.walk(node)
                if isinstance(sub, ast.Assert)
            ]

            anchors.append(
                {
                    "file": relative,
                    "test": node.name,
                    "startLine": node.lineno,
                    "endLine": (node.end_lineno or node.lineno),
                    "surfaces": touched,
                    "indirectBundleMaps": indirect,
                    "assertionCount": len(assertion_lines),
                    "assertionLines": assertion_lines,
                    "firstLine": lines[node.lineno - 1].strip(),
                }
            )

    return anchors


def pinned_declarations() -> list[dict[str, str]]:
    """Literal strings a contract pins *inside* a surface a packet owns.

    These are the packets' hard ceilings: deleting or reformatting any of these
    strings reds the shared contract file, which no packet except **i** may
    amend (N6).
    """
    pins: list[dict[str, str]] = []
    surfaces = set(SHARED_SURFACES)

    for relative in CONTRACT_FILES:
        source = (ROOT / relative).read_text(encoding="utf-8")
        tree = ast.parse(source)

        for node in tree.body:
            if not isinstance(node, ast.FunctionDef) or not node.name.startswith("test_"):
                continue
            body_source = ast.get_source_segment(source, node) or ""
            touched = sorted(name for name in surfaces if name in body_source)
            if not touched:
                continue

            for sub in ast.walk(node):
                if not isinstance(sub, ast.Compare):
                    continue
                if not any(isinstance(op, ast.In) for op in sub.ops):
                    continue
                if not isinstance(sub.left, ast.Constant) or not isinstance(
                    sub.left.value, str
                ):
                    continue
                pins.append(
                    {
                        "file": relative,
                        "test": node.name,
                        "line": str(sub.lineno),
                        "pinnedString": sub.left.value,
                        "candidateSurfaces": ", ".join(touched),
                    }
                )

    return pins


# --------------------------------------------------------------------------
# Oracle blind-spot register (F2)
# --------------------------------------------------------------------------

HELPER_RELATIVE = "e2e/visual-helpers.ts"
HELPER_FUNCTION = "prepareForScreenshot"
# The element-capture path calls `prepareForScreenshot()` and then layers a
# second stylesheet of its own. That stylesheet is NOT part of the register — it
# applies to locator captures only — but it is a neutralizing channel in the same
# file, so it is enumerated and pinned rather than left undescribed.
ELEMENT_HELPER_FUNCTION = "prepareForElementScreenshot"

STYLESHEET_STAGE = "stylesheet"
INLINE_STAGE = "inline"
STAGES = (STYLESHEET_STAGE, INLINE_STAGE)

NEUTRALIZER = "neutralizer"
SUPPORT_TOKEN = "support-token"
CLASSIFICATIONS = (NEUTRALIZER, SUPPORT_TOKEN)

_DECLARATION_RE = re.compile(r"^(-{0,2}[A-Za-z][-A-Za-z0-9_]*)\s*:\s*(.+)$", re.DOTALL)
_IMPORTANT_SUFFIX_RE = re.compile(r"!\s*important\s*$", re.IGNORECASE)
_STRING_LITERAL_RE = re.compile(r"^(['\"])(.*)\1$", re.DOTALL)

# Every way `prepareForScreenshot()` could apply a style that this extractor does
# NOT enumerate. Finding one is a parse failure, not a silent omission: a
# register that quietly skips a channel reproduces the exact false confidence
# Q10 exists to remove.
_UNSUPPORTED_CHANNELS = (
    (re.compile(r"\.style\.(?!setProperty\b)"), "direct element.style.<property> assignment"),
    (re.compile(r"cssText"), "style.cssText"),
    (re.compile(r"setAttribute\s*\("), "setAttribute()"),
    (re.compile(r"insertRule\s*\("), "CSSOM insertRule()"),
)


class HelperParseError(RuntimeError):
    """`prepareForScreenshot()` is not in a shape the extractor can enumerate.

    Raised — never swallowed — so that an unrecognised construct fails the
    contract closed. The alternative, skipping what the parser does not
    understand, is how the two escaped neutralizers (`.summary-header` paint
    flattening and sticky-table `position: static`) were added without moving a
    single test.
    """


def helper_source() -> str:
    return (ROOT / HELPER_RELATIVE).read_text(encoding="utf-8")


def _reject_unsupported_channels(body: str, function: str) -> None:
    for pattern, description in _UNSUPPORTED_CHANNELS:
        if pattern.search(body):
            raise HelperParseError(
                f"`{function}` uses {description}, a style channel this "
                "extractor does not enumerate"
            )


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _collapse(text: str) -> str:
    return " ".join(text.split())


def _normalize_selector(text: str) -> str:
    """Formatting-independent selector identity.

    Indentation, line breaks inside a selector list and comments all collapse
    away; quote style and case do not, because changing either is a real edit to
    the selector and Q10's whole point is that a real edit must be visible.
    """
    return re.sub(r"\s*,\s*", ", ", _collapse(text))


def _skip_string(text: str, index: int) -> int:
    """Index just past the string literal opening at ``index`` (any quote form)."""
    quote = text[index]
    index += 1
    while index < len(text):
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char == quote:
            return index + 1
        index += 1
    raise HelperParseError(f"unterminated {quote} string literal in {HELPER_RELATIVE}")


def _matching_brace(text: str, open_index: int) -> int:
    """Index of the `}` closing the `{` at ``open_index``, skipping JS noise.

    String literals — backticks included — and both comment forms are skipped
    whole, so the braces of the injected CSS never enter the count and a brace
    inside a comment cannot unbalance it.
    """
    depth = 0
    index = open_index
    while index < len(text):
        char = text[index]
        if char in "\"'`":
            index = _skip_string(text, index)
            continue
        if char == "/" and index + 1 < len(text):
            following = text[index + 1]
            if following == "/":
                newline = text.find("\n", index)
                index = len(text) if newline == -1 else newline
                continue
            if following == "*":
                close = text.find("*/", index + 2)
                if close == -1:
                    raise HelperParseError("unterminated block comment")
                index = close + 2
                continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    raise HelperParseError(f"unbalanced braces in {HELPER_FUNCTION}()")


def _split_top_level(text: str, separator: str) -> list[str]:
    """Split on ``separator`` outside parentheses and string literals."""
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    index = 0
    while index < len(text):
        char = text[index]
        if char in "\"'":
            end = _skip_string(text, index)
            current.append(text[index:end])
            index = end
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        if char == separator and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
        index += 1
    parts.append("".join(current))
    return [part for part in (item.strip() for item in parts) if part]


def _string_literal_arguments(arguments: str) -> list[str] | None:
    """The argument list as plain strings, or ``None`` if any is not a literal."""
    values: list[str] = []
    for part in _split_top_level(arguments, ","):
        match = _STRING_LITERAL_RE.match(part)
        if not match:
            return None
        values.append(match.group(2))
    return values


def _prepare_function_body(helper: str, function: str = HELPER_FUNCTION) -> str:
    matches = list(re.finditer(rf"function\s+{function}\s*\(", helper))
    if len(matches) != 1:
        raise HelperParseError(
            f"expected exactly one `{function}` definition in "
            f"{HELPER_RELATIVE}, found {len(matches)}"
        )
    _, after_parameters = specificity._read_balanced(helper, matches[0].end() - 1)
    brace = helper.find("{", after_parameters)
    if brace == -1:
        raise HelperParseError(f"`{function}` has no body")
    return helper[brace + 1 : _matching_brace(helper, brace)]


def _injected_stylesheet(body: str, function: str = HELPER_FUNCTION) -> str:
    calls = list(re.finditer(r"addStyleTag\s*\(", body))
    if len(calls) != 1:
        raise HelperParseError(
            f"`{function}` makes {len(calls)} addStyleTag() call(s); the "
            "extractor enumerates exactly one, so a second injected stylesheet "
            "is an unenumerated neutralizer channel"
        )
    content = re.compile(r"content\s*:\s*`").search(body, calls[0].end())
    if content is None:
        raise HelperParseError(
            "addStyleTag() is not called with a `content:` template literal"
        )
    open_backtick = content.end() - 1
    css = body[open_backtick + 1 : _skip_string(body, open_backtick) - 1]
    if "${" in css:
        raise HelperParseError(
            "the injected stylesheet interpolates a template expression, so its "
            "text is not statically knowable"
        )
    return css


def helper_rule_blocks(helper: str | None = None) -> list[dict[str, object]]:
    """Every rule block of the stylesheet `prepareForScreenshot()` injects.

    One record per block: its normalized selector, its declarations in source
    order, and the classification the block's own contents imply — a block whose
    declarations are all custom properties is a support token, everything else
    neutralizes something the pixel oracle would otherwise have seen.
    """
    return _rule_blocks(
        _injected_stylesheet(_prepare_function_body(
            _normalize_newlines(helper if helper is not None else helper_source())
        ))
    )


def _rule_blocks(css: str) -> list[dict[str, object]]:
    blanked = _blank_comments(_normalize_newlines(css))

    blocks: list[dict[str, object]] = []
    depth = 0
    selector_start = 0
    open_index = 0
    last_close = -1
    for index, char in enumerate(blanked):
        if char == "{":
            if depth == 0:
                start = index
                while start > 0 and blanked[start - 1] not in "{};":
                    start -= 1
                selector_start = start
                open_index = index
            depth += 1
        elif char == "}":
            if depth == 0:
                raise HelperParseError("unbalanced `}` in the injected stylesheet")
            depth -= 1
            if depth == 0:
                selector = _normalize_selector(blanked[selector_start:open_index])
                if not selector:
                    raise HelperParseError(f"rule block at offset {open_index} has no selector")
                if selector.startswith("@"):
                    raise HelperParseError(
                        f"at-rule {selector!r} in the injected stylesheet: its "
                        "declarations apply only under a condition this register "
                        "does not model"
                    )
                declarations = _parse_declarations(
                    blanked[open_index + 1 : index], selector
                )
                blocks.append(
                    {
                        "selector": selector,
                        "declarations": declarations,
                        "classification": (
                            SUPPORT_TOKEN
                            if all(
                                str(item["property"]).startswith("--")
                                for item in declarations
                            )
                            else NEUTRALIZER
                        ),
                    }
                )
                last_close = index
    if depth:
        raise HelperParseError("unbalanced `{` in the injected stylesheet")
    if blanked[last_close + 1 :].strip():
        raise HelperParseError(
            "text outside every rule block in the injected stylesheet: "
            f"{_collapse(blanked[last_close + 1 :])!r}"
        )
    return blocks


def _parse_declarations(body: str, where: str) -> list[dict[str, object]]:
    if "{" in body:
        raise HelperParseError(
            f"nested rule inside {where!r}; CSS nesting is not modelled"
        )
    declarations: list[dict[str, object]] = []
    for segment in _split_top_level(body, ";"):
        match = _DECLARATION_RE.match(segment)
        if not match:
            raise HelperParseError(f"cannot parse {segment!r} in {where!r} as a declaration")
        value = match.group(2).strip()
        important = bool(_IMPORTANT_SUFFIX_RE.search(value))
        if important:
            value = _IMPORTANT_SUFFIX_RE.sub("", value).strip()
        value = _collapse(value)
        if not value:
            raise HelperParseError(f"declaration {segment!r} in {where!r} has no value")
        declarations.append(
            {"property": match.group(1), "value": value, "important": important}
        )
    if not declarations:
        raise HelperParseError(f"rule block {where!r} declares nothing")
    return declarations


def helper_inline_blocks(helper: str | None = None) -> list[dict[str, object]]:
    """The post-load `element.style.setProperty()` re-application stage.

    A second neutralizing channel, and the one a stylesheet-only parser misses
    entirely: these land as inline `!important`, above every author rule, after
    the page has finished running its own scripts.
    """
    body = _prepare_function_body(
        _normalize_newlines(helper if helper is not None else helper_source())
    )
    _reject_unsupported_channels(body, HELPER_FUNCTION)

    expected = len(re.findall(r"setProperty\s*\(", body))
    blocks: list[dict[str, object]] = []
    seen = 0

    for match in re.finditer(r"querySelectorAll\s*(?:<[^>]*>)?\s*\(", body):
        arguments, after = specificity._read_balanced(body, match.end() - 1)
        literals = _string_literal_arguments(arguments)
        if literals is None or len(literals) != 1:
            raise HelperParseError(
                f"querySelectorAll({_collapse(arguments)!r}) is not called with a "
                "single string-literal selector"
            )
        chain = re.match(r"\s*\.\s*forEach\s*\(", body[after:])
        if chain is None:
            raise HelperParseError(
                f"the querySelectorAll({literals[0]!r}) result is consumed by "
                "something other than .forEach()"
            )
        brace = body.find("{", after + chain.end())
        if brace == -1:
            raise HelperParseError("the .forEach() callback has no body")
        callback = body[brace + 1 : _matching_brace(body, brace)]

        declarations: list[dict[str, object]] = []
        for call in re.finditer(r"setProperty\s*\(", callback):
            arguments, _ = specificity._read_balanced(callback, call.end() - 1)
            values = _string_literal_arguments(arguments)
            if values is None or len(values) not in (2, 3):
                raise HelperParseError(
                    f"setProperty({_collapse(arguments)!r}) does not take two or "
                    "three string literals"
                )
            priority = values[2] if len(values) == 3 else ""
            if priority.lower() not in ("", "important"):
                raise HelperParseError(f"unknown setProperty priority {priority!r}")
            seen += 1
            declarations.append(
                {
                    "property": values[0],
                    "value": _collapse(values[1]),
                    "important": priority.lower() == "important",
                }
            )
        if not declarations:
            continue
        blocks.append(
            {
                "selector": _normalize_selector(literals[0]),
                "declarations": declarations,
                "classification": (
                    SUPPORT_TOKEN
                    if all(
                        str(item["property"]).startswith("--") for item in declarations
                    )
                    else NEUTRALIZER
                ),
            }
        )

    if seen != expected:
        raise HelperParseError(
            f"{expected} setProperty() call(s) in `{HELPER_FUNCTION}` but only "
            f"{seen} reachable through an enumerated querySelectorAll().forEach()"
        )
    return blocks


def _flatten(blocks: list[dict[str, object]], stage: str) -> list[dict[str, object]]:
    return [
        {
            "stage": stage,
            "selector": block["selector"],
            "property": declaration["property"],
            "value": declaration["value"],
            "important": declaration["important"],
            "classification": block["classification"],
        }
        for block in blocks
        for declaration in block["declarations"]  # type: ignore[attr-defined]
    ]


def helper_rules(helper: str | None = None) -> list[dict[str, object]]:
    """Every declaration `prepareForScreenshot()` applies, across both stages."""
    return _flatten(helper_rule_blocks(helper), STYLESHEET_STAGE) + _flatten(
        helper_inline_blocks(helper), INLINE_STAGE
    )


def element_capture_rules(helper: str | None = None) -> list[dict[str, object]]:
    """The extra declarations `prepareForElementScreenshot()` layers on top.

    Locator captures run `prepareForScreenshot()` first and then inject a second
    stylesheet that hides fixed page chrome. Those declarations are outside
    `BLIND_SPOT_REGISTER` by construction — the register describes the full-page
    stage that every visual capture shares — but they are a neutralizing channel
    in the same file, so leaving them underived would rebuild the blind spot Q10
    exists to remove, one function further down.

    Enumerated on the same terms: exactly one `addStyleTag()`, no inline stage
    and no other style channel. Anything else raises rather than returning a
    shorter list.
    """
    body = _prepare_function_body(
        _normalize_newlines(helper if helper is not None else helper_source()),
        ELEMENT_HELPER_FUNCTION,
    )
    _reject_unsupported_channels(body, ELEMENT_HELPER_FUNCTION)
    if "setProperty" in body:
        raise HelperParseError(
            f"`{ELEMENT_HELPER_FUNCTION}` applies an inline setProperty() stage; "
            "only its injected stylesheet is enumerated"
        )
    return _flatten(
        _rule_blocks(_injected_stylesheet(body, ELEMENT_HELPER_FUNCTION)),
        STYLESHEET_STAGE,
    )


# The declarations `prepareForScreenshot()` applies before any pixel is
# captured, curated into reviewable groups. The curated half — `why`,
# `blindsPackets`, `context` — is the point of the register: a machine cannot
# say which packet family a neutralizer blinds. The machine half — `stage`,
# `selector`, `declarations`, `classification` — is compared against the helper
# in BOTH directions by `verify_blind_spots()`, exactly, so neither an added
# neutralizer nor a changed value nor a dropped property can pass unnoticed.
#
# One entry is one (stage, selector) group; a block whose declarations blind
# different packet families is split into several entries over the same
# selector, and `verify_blind_spots()` rejects any two entries that claim the
# same (stage, selector, property).
BLIND_SPOT_REGISTER: tuple[dict[str, object], ...] = (
    {
        "selector": "*, *::before, *::after",
        "stage": STYLESHEET_STAGE,
        "helperSelector": "*, *::before, *::after",
        "classification": NEUTRALIZER,
        "properties": [
            "animation-delay",
            "animation-duration",
            "animation-iteration-count",
            "transition-duration",
            "transition-delay",
        ],
        "declarations": [
            {"property": "animation-delay", "value": "0s", "important": True},
            {"property": "animation-duration", "value": "0s", "important": True},
            {"property": "animation-iteration-count", "value": "1", "important": True},
            {"property": "transition-duration", "value": "0s", "important": True},
            {"property": "transition-delay", "value": "0s", "important": True},
        ],
        "neutralizedTo": "0s / 1",
        "helperEvidence": "animation-duration: 0s !important;",
        "blindsSurfaces": ["motion.css"],
        "blindsPackets": ["c"],
        "why": "F1 — motion.css's entire output is zeroed before capture, so a "
               "packet deleting the whole file yields a byte-identical matrix.",
    },
    {
        "selector": "*, *::before, *::after",
        "stage": STYLESHEET_STAGE,
        "helperSelector": "*, *::before, *::after",
        "classification": NEUTRALIZER,
        "properties": ["backdrop-filter", "-webkit-backdrop-filter"],
        "declarations": [
            {"property": "backdrop-filter", "value": "none", "important": True},
            {"property": "-webkit-backdrop-filter", "value": "none", "important": True},
        ],
        "neutralizedTo": "none",
        "helperEvidence": "-webkit-backdrop-filter: none !important;",
        "blindsSurfaces": ["components.css", "theme-dark.css"],
        "blindsPackets": ["h", "i", "j"],
        "why": "F2 — the glass families in components.css and the theme-dark.css "
               "rule pinned by the cascade contract are the core surface of h/i/j. "
               "The prefixed and unprefixed properties are registered separately: "
               "citing only `backdrop-filter: none !important;` was satisfiable by "
               "the `-webkit-` line, so deleting the property this entry describes "
               "left the old one-way check green.",
    },
    {
        "selector": "html (scroll behaviour)",
        "stage": STYLESHEET_STAGE,
        "helperSelector": "html",
        "classification": NEUTRALIZER,
        "properties": ["scroll-behavior"],
        "declarations": [
            {"property": "scroll-behavior", "value": "auto", "important": True},
        ],
        "neutralizedTo": "auto",
        "helperEvidence": "html { scroll-behavior: auto !important; }",
        "blindsSurfaces": ["layout.css"],
        "blindsPackets": ["e"],
        "why": "layout.css sets `scroll-behavior: smooth` on the scroll root. A "
               "capture is taken at the origin, so the oracle cannot distinguish "
               "smooth from auto and a packet changing it moves no pixel.",
    },
    {
        "selector": "html (light `--visual-surface-*` definitions)",
        "stage": STYLESHEET_STAGE,
        "helperSelector": "html",
        "classification": SUPPORT_TOKEN,
        "properties": ["--visual-surface-0", "--visual-surface-1"],
        "declarations": [
            {"property": "--visual-surface-0", "value": "#eef1f6", "important": False},
            {"property": "--visual-surface-1", "value": "#f7f9fc", "important": False},
        ],
        "neutralizedTo": "n/a — defines the tokens the flatteners consume",
        "helperEvidence": "--visual-surface-0: #eef1f6;",
        "blindsSurfaces": [],
        "blindsPackets": [],
        "why": "Support token, registered explicitly rather than skipped as "
               "'just a custom property'. It neutralizes nothing on its own; it "
               "supplies the flat values the registered dark flatteners paint.",
    },
    {
        "selector": "html[data-theme='dark'] (dark `--visual-surface-*` definitions)",
        "stage": STYLESHEET_STAGE,
        "helperSelector": "html[data-theme='dark']",
        "classification": SUPPORT_TOKEN,
        "properties": ["--visual-surface-0", "--visual-surface-1"],
        "declarations": [
            {"property": "--visual-surface-0", "value": "#090c16", "important": False},
            {"property": "--visual-surface-1", "value": "#0d101d", "important": False},
        ],
        "neutralizedTo": "n/a — defines the tokens the flatteners consume",
        "helperEvidence": "--visual-surface-0: #090c16;",
        "blindsSurfaces": [],
        "blindsPackets": [],
        "why": "The dark half of the support pair. Separate from the light block "
               "because they are separate rules with different selectors; a "
               "register that treated the pair as one could not see either go.",
    },
    {
        "selector": "body (both themes)",
        "stage": STYLESHEET_STAGE,
        "helperSelector": "html[data-theme] body, body",
        "classification": NEUTRALIZER,
        "properties": ["background", "background-attachment"],
        "declarations": [
            {
                "property": "background",
                "value": "var(--visual-surface-0)",
                "important": True,
            },
            {"property": "background-attachment", "value": "scroll", "important": True},
        ],
        "neutralizedTo": "a flat token colour, unattached",
        "helperEvidence": "background-attachment: scroll !important;",
        "blindsSurfaces": ["theme-dark.css", "base.css"],
        "blindsPackets": ["b", "j"],
        "why": "The headline case. The whole page background is repainted flat in "
               "BOTH themes, so the multi-gradient dark `body` rule in "
               "theme-dark.css and the fixed attachment in base.css are invisible "
               "to every capture in the matrix.",
    },
    {
        "selector": "[data-visual-surface][data-visual-surface] (dark theme only)",
        "stage": STYLESHEET_STAGE,
        "helperSelector": (
            "html[data-theme='dark'] [data-visual-surface][data-visual-surface]"
        ),
        "classification": NEUTRALIZER,
        "properties": ["background", "background-image", "box-shadow", "text-shadow"],
        "declarations": [
            {
                "property": "background",
                "value": "var(--visual-surface-1)",
                "important": True,
            },
            {"property": "background-image", "value": "none", "important": True},
            {"property": "box-shadow", "value": "none", "important": True},
            {"property": "text-shadow", "value": "none", "important": True},
        ],
        "neutralizedTo": "forced flat values",
        "helperEvidence": (
            "html[data-theme='dark'] [data-visual-surface][data-visual-surface] {"
        ),
        "blindsSurfaces": ["theme-dark.css"],
        "blindsPackets": ["j"],
        "why": "F2 — the dark baseline is blind to surface paint on exactly the "
               "elements theme-dark.css exists to paint.",
    },
    {
        "selector": ".summary-header (dark theme only)",
        "stage": STYLESHEET_STAGE,
        "helperSelector": "html[data-theme='dark'] .summary-header",
        "classification": NEUTRALIZER,
        "properties": ["background", "border-radius", "box-shadow"],
        "declarations": [
            {
                "property": "background",
                "value": "var(--visual-surface-1)",
                "important": True,
            },
            {"property": "border-radius", "value": "0", "important": True},
            {"property": "box-shadow", "value": "none", "important": True},
        ],
        "neutralizedTo": "forced flat values",
        "helperEvidence": "html[data-theme='dark'] .summary-header {",
        "blindsSurfaces": ["theme-dark.css", "components.css"],
        "blindsPackets": ["j"],
        "why": "Added to defeat a fractional-edge rounding flake on the summary "
               "filter bar. It reached the register only through Q10: the old "
               "one-way check could not see a block the helper gained, so the "
               "dark summary surface silently left the pixel oracle's reach.",
    },
    {
        "selector": "[data-visual-surface] border geometry (dark theme only)",
        "stage": STYLESHEET_STAGE,
        "helperSelector": (
            "html[data-theme='dark'] [data-visual-surface][data-visual-surface]"
            ":where(:not([data-visual-preserve-border]))"
        ),
        "classification": NEUTRALIZER,
        "properties": ["border-color", "border-radius"],
        "declarations": [
            {"property": "border-color", "value": "#273145", "important": True},
            {"property": "border-radius", "value": "0", "important": True},
        ],
        "neutralizedTo": "one flat border colour, square corners",
        "helperEvidence": ":where(:not([data-visual-preserve-border])) {",
        "blindsSurfaces": ["theme-dark.css"],
        "blindsPackets": ["j"],
        "why": "Split out of the paint flattener above so a specificity change in "
               "the product could not silently hand these two properties to the "
               "capture layer. Registered as its own rule for the same reason it "
               "exists as its own rule.",
    },
    {
        "selector": "[data-visual-header]::before (dark Workout Plan only)",
        "stage": STYLESHEET_STAGE,
        "helperSelector": (
            "html[data-theme='dark'] [data-page=\"workout-plan\"] "
            "[data-visual-header]::before"
        ),
        "classification": NEUTRALIZER,
        "properties": ["background"],
        "declarations": [
            {"property": "background", "value": "transparent", "important": True},
        ],
        "neutralizedTo": "transparent",
        "helperEvidence": "[data-visual-header]::before {",
        "blindsSurfaces": ["theme-dark.css", "pages-workout-plan.css"],
        "blindsPackets": ["j"],
        "why": "The decorative header wash on the dark plan page is erased before "
               "capture, so nothing painted by that pseudo-element is compared.",
    },
    {
        "selector": "[data-visual-accent] (dark Workout Plan only)",
        "stage": STYLESHEET_STAGE,
        "helperSelector": (
            "html[data-theme='dark'] [data-page=\"workout-plan\"] "
            "[data-visual-accent]"
        ),
        "classification": NEUTRALIZER,
        "properties": [
            "background",
            "border-radius",
            "box-shadow",
            "transform",
            "transition",
        ],
        "declarations": [
            {"property": "background", "value": "#4f8cff", "important": True},
            {"property": "border-radius", "value": "0", "important": True},
            {"property": "box-shadow", "value": "none", "important": True},
            {"property": "transform", "value": "none", "important": True},
            {"property": "transition", "value": "none", "important": True},
        ],
        "neutralizedTo": "one flat accent colour, no geometry, no motion",
        "helperEvidence": "[data-visual-accent] {",
        "blindsSurfaces": ["theme-dark.css", "components.css", "motion.css"],
        "blindsPackets": ["c", "j"],
        "why": "Five properties, not one: the old register reached this block only "
               "because the form-control entry cited `box-shadow: none !important;` "
               "and that string happens to occur here too. background, transform "
               "and transition were never registered at all.",
    },
    {
        "selector": "input, textarea (caret)",
        "stage": STYLESHEET_STAGE,
        "helperSelector": "input, textarea",
        "classification": NEUTRALIZER,
        "properties": ["caret-color"],
        "declarations": [
            {"property": "caret-color", "value": "transparent", "important": True},
        ],
        "neutralizedTo": "transparent",
        "helperEvidence": "input, textarea { caret-color: transparent !important; }",
        "blindsSurfaces": [],
        "blindsPackets": [],
        "why": "A capture-determinism control rather than a product blind spot — "
               "no shared surface declares caret-color. Registered anyway: the "
               "register's claim is that the injected stylesheet is enumerated "
               "completely, and an unlisted rule would break that claim whatever "
               "its motive.",
    },
    {
        "selector": "select (native affordance)",
        "stage": STYLESHEET_STAGE,
        "helperSelector": "select",
        "classification": NEUTRALIZER,
        "properties": ["appearance", "-webkit-appearance", "background-image"],
        "declarations": [
            {"property": "appearance", "value": "none", "important": True},
            {"property": "-webkit-appearance", "value": "none", "important": True},
            {"property": "background-image", "value": "none", "important": True},
        ],
        "neutralizedTo": "none",
        "helperEvidence": "select {",
        "blindsSurfaces": ["components.css"],
        "blindsPackets": ["h", "i"],
        "why": "components.css styles the select affordance through appearance and "
               "a background-image chevron; both are erased before capture, so the "
               "control's whole custom affordance is outside the oracle.",
    },
    {
        "selector": "form controls (injected stylesheet stage)",
        "stage": STYLESHEET_STAGE,
        "helperSelector": (
            "[data-visual-control], input, textarea, select, input[type=\"number\"]"
        ),
        "classification": NEUTRALIZER,
        "properties": ["border-radius", "box-shadow", "text-shadow"],
        "declarations": [
            {"property": "border-radius", "value": "0", "important": True},
            {"property": "box-shadow", "value": "none", "important": True},
            {"property": "text-shadow", "value": "none", "important": True},
        ],
        "neutralizedTo": "0 / none",
        "helperEvidence": "input[type=\"number\"] {",
        "blindsSurfaces": ["components.css", "theme-dark.css", "a11y.css"],
        "blindsPackets": ["d", "h", "j"],
        "why": "F2 — the stylesheet half of the form-control neutralization. Its "
               "inline twin below re-applies the same three properties after load, "
               "and the two are registered separately because they are two "
               "distinct channels with two distinct selectors.",
    },
    {
        "selector": "navbar link/button ::before wash",
        "stage": STYLESHEET_STAGE,
        "helperSelector": (
            "[data-testid=\"navbar\"] a::before, [data-testid=\"navbar\"] "
            "button::before"
        ),
        "classification": NEUTRALIZER,
        "properties": ["background-color", "border-radius", "transform", "transition"],
        "declarations": [
            {"property": "background-color", "value": "transparent", "important": True},
            {"property": "border-radius", "value": "0", "important": True},
            {"property": "transform", "value": "none", "important": True},
            {"property": "transition", "value": "none", "important": True},
        ],
        "neutralizedTo": "transparent, no geometry, no motion",
        "helperEvidence": "[data-testid=\"navbar\"] a::before,",
        "blindsSurfaces": ["navbar.css", "motion.css"],
        "blindsPackets": ["c", "f"],
        "why": "The navbar hover/active wash is a pseudo-element that the capture "
               "erases outright, so navbar.css's whole ::before treatment — colour, "
               "corner geometry and its transition — is unmeasurable by pixels.",
    },
    {
        "selector": "[data-visual-dropdown-toggle]::after (caret)",
        "stage": STYLESHEET_STAGE,
        "helperSelector": "[data-visual-dropdown-toggle]::after",
        "classification": NEUTRALIZER,
        "properties": ["border-color"],
        "declarations": [
            {"property": "border-color", "value": "transparent", "important": True},
        ],
        "neutralizedTo": "transparent",
        "helperEvidence": "[data-visual-dropdown-toggle]::after {",
        "blindsSurfaces": ["navbar.css"],
        "blindsPackets": ["f"],
        "why": "The dropdown caret is drawn with borders; making them transparent "
               "removes the glyph from every capture.",
    },
    {
        "selector": "[data-visual-icon]",
        "stage": STYLESHEET_STAGE,
        "helperSelector": "[data-visual-icon]",
        "classification": NEUTRALIZER,
        "properties": ["visibility"],
        "declarations": [
            {"property": "visibility", "value": "hidden", "important": True},
        ],
        "neutralizedTo": "hidden",
        "helperEvidence": "[data-visual-icon] {",
        "blindsSurfaces": ["components.css", "navbar.css", "base.css"],
        "blindsPackets": ["b", "f"],
        "why": "F2 — icon affordances are invisible to the oracle entirely.",
    },
    {
        "selector": "[data-visual-scale-control]",
        "stage": STYLESHEET_STAGE,
        "helperSelector": "[data-visual-scale-control]",
        "classification": NEUTRALIZER,
        "properties": ["background", "border-color", "color"],
        "declarations": [
            {"property": "background", "value": "transparent", "important": True},
            {"property": "border-color", "value": "transparent", "important": True},
            {"property": "color", "value": "transparent", "important": True},
        ],
        "neutralizedTo": "transparent",
        "helperEvidence": "[data-visual-scale-control] {",
        "blindsSurfaces": ["components.css"],
        "blindsPackets": ["d"],
        "why": "F2 — WP4.4-d owns the data-scale UI scale system.",
    },
    {
        "selector": "sticky table headers and first columns",
        "stage": STYLESHEET_STAGE,
        "helperSelector": (
            "[data-testid=\"exercise-table\"] thead th, "
            "[data-testid=\"exercise-table\"] tr > :first-child, "
            "[data-testid=\"workout-log-table\"] thead th, "
            "[data-testid=\"workout-log-table\"] tr > :first-child"
        ),
        "classification": NEUTRALIZER,
        "properties": ["position"],
        "declarations": [
            {"property": "position", "value": "static", "important": True},
        ],
        "neutralizedTo": "static",
        "helperEvidence": "position: static !important;",
        "blindsSurfaces": ["layout.css", "pages-workout-log.css", "pages-workout-plan.css"],
        "blindsPackets": ["e"],
        "why": "Demotes the compositor-promoted sticky cells back onto the static "
               "paint path. The second neutralizer that escaped registration "
               "entirely: it changes `position`, which no register entry mentioned "
               "and which the old substring check had no way to notice.",
    },
    {
        "selector": "number-input spin buttons",
        "stage": STYLESHEET_STAGE,
        "helperSelector": (
            "input[type=\"number\"]::-webkit-outer-spin-button, "
            "input[type=\"number\"]::-webkit-inner-spin-button"
        ),
        "classification": NEUTRALIZER,
        "properties": ["-webkit-appearance", "margin"],
        "declarations": [
            {"property": "-webkit-appearance", "value": "none", "important": True},
            {"property": "margin", "value": "0", "important": True},
        ],
        "neutralizedTo": "none / 0",
        "helperEvidence": "input[type=\"number\"]::-webkit-outer-spin-button,",
        "blindsSurfaces": ["components.css"],
        "blindsPackets": ["h", "i"],
        "why": "components.css has its own spin-button treatment, including hover "
               "and active states. The capture removes the control, so none of it "
               "is comparable by pixels.",
    },
    {
        "selector": "::-webkit-scrollbar",
        "stage": STYLESHEET_STAGE,
        "helperSelector": "::-webkit-scrollbar",
        "classification": NEUTRALIZER,
        "properties": ["display"],
        "declarations": [
            {"property": "display", "value": "none", "important": False},
        ],
        "neutralizedTo": "none",
        "helperEvidence": "::-webkit-scrollbar { display: none; }",
        "blindsSurfaces": ["components.css", "navbar.css"],
        "blindsPackets": ["f", "h", "i"],
        "why": "The one declaration in the injected stylesheet that is NOT "
               "`!important`, recorded as such: importance is part of the machine "
               "identity, so quietly adding it later would be a visible change. "
               "components.css and navbar.css both style scrollbars; nothing they "
               "declare survives to a capture.",
    },
    {
        "selector": "form controls (post-load inline re-application)",
        "stage": INLINE_STAGE,
        "helperSelector": "[data-visual-control], input, textarea, select",
        "classification": NEUTRALIZER,
        "properties": ["border-radius", "box-shadow", "text-shadow"],
        "declarations": [
            {"property": "border-radius", "value": "0", "important": True},
            {"property": "box-shadow", "value": "none", "important": True},
            {"property": "text-shadow", "value": "none", "important": True},
        ],
        "neutralizedTo": "0 / none",
        "helperEvidence": "element.style.setProperty('border-radius', '0', 'important');",
        "blindsSurfaces": ["components.css", "theme-dark.css", "a11y.css"],
        "blindsPackets": ["d", "h", "j"],
        "why": "F2 — re-applied inline after load, so even late overrides are "
               "hidden. A second channel, not a restatement of the stylesheet "
               "entry: inline `!important` outranks every author rule, and a "
               "stylesheet-only extractor would not see it at all.",
    },
)

_REQUIRED_ENTRY_KEYS = (
    "selector",
    "stage",
    "helperSelector",
    "classification",
    "properties",
    "declarations",
    "neutralizedTo",
    "helperEvidence",
    "blindsSurfaces",
    "blindsPackets",
    "why",
)


def register_rules() -> list[dict[str, object]]:
    """The curated register, flattened to the same shape as `helper_rules()`."""
    return [
        {
            "stage": entry["stage"],
            "selector": entry["helperSelector"],
            "property": declaration["property"],
            "value": declaration["value"],
            "important": declaration["important"],
            "classification": entry["classification"],
        }
        for entry in BLIND_SPOT_REGISTER
        for declaration in entry["declarations"]  # type: ignore[attr-defined]
    ]


def _register_shape_failures() -> list[str]:
    """Internal consistency of the curated register, checked before comparison."""
    failures: list[str] = []
    for index, entry in enumerate(BLIND_SPOT_REGISTER):
        label = f"register entry {index} ({entry.get('selector')!r})"
        missing = [key for key in _REQUIRED_ENTRY_KEYS if key not in entry]
        if missing:
            failures.append(f"{label} is missing {missing}")
            continue
        if entry["stage"] not in STAGES:
            failures.append(f"{label} has unknown stage {entry['stage']!r}")
        if entry["classification"] not in CLASSIFICATIONS:
            failures.append(
                f"{label} has unknown classification {entry['classification']!r}"
            )
        declarations = list(entry["declarations"])  # type: ignore[call-overload]
        if not declarations:
            failures.append(f"{label} registers no declaration")
        # `properties` is a human-readable mirror of `declarations`; keeping the
        # two in lockstep is what stops the mirror from rotting into a claim of
        # its own.
        mirrored = [item["property"] for item in declarations]
        if list(entry["properties"]) != mirrored:  # type: ignore[call-overload]
            failures.append(
                f"{label}: `properties` {list(entry['properties'])} does not "  # type: ignore[call-overload]
                f"mirror `declarations` {mirrored}"
            )
        for item in declarations:
            if set(item) != {"property", "value", "important"}:
                failures.append(f"{label}: malformed declaration {item!r}")
            elif not isinstance(item["important"], bool):
                failures.append(
                    f"{label}: declaration {item['property']!r} records "
                    f"importance as {item['important']!r}, not a bool"
                )
    return failures


def _by_signature(
    rules: list[dict[str, object]], side: str
) -> tuple[dict[tuple[str, str, str], dict[str, object]], list[str]]:
    """Index rules by `(stage, selector, property)`, rejecting duplicates."""
    indexed: dict[tuple[str, str, str], dict[str, object]] = {}
    failures: list[str] = []
    for rule in rules:
        key = (str(rule["stage"]), str(rule["selector"]), str(rule["property"]))
        if key in indexed:
            failures.append(
                f"duplicate {side} signature {key}: one machine identity cannot "
                "describe two rules, so one of them would be unverifiable"
            )
            continue
        indexed[key] = rule
    return indexed, failures


def _describe(rule: dict[str, object]) -> str:
    bang = " !important" if rule["important"] else ""
    return (
        f"[{rule['stage']}] {rule['selector']} {{ {rule['property']}: "
        f"{rule['value']}{bang}; }} ({rule['classification']})"
    )


def verify_blind_spots(helper: str | None = None) -> list[str]:
    """Compare the curated register against the live helper, both directions.

    The register is the reviewable statement of what the pixel oracle CANNOT
    see, so it has to be curated — a machine cannot say which packet family a
    neutralizer blinds. What it must not be is *unchecked*: the previous version
    searched the helper text for one substring per entry and checked nothing in
    the other direction, so two neutralizers (dark `.summary-header` paint
    flattening, sticky-table `position: static`) were added to
    `prepareForScreenshot()` with the whole suite green.

    Every declaration the helper applies — in the injected stylesheet and in the
    later inline `setProperty()` stage — is derived mechanically and matched
    against the register on `(stage, selector, property)`, with value and
    importance and classification compared on the matches. Anything the
    extractor cannot parse is a failure, never a silent omission.
    """
    failures = _register_shape_failures()

    try:
        derived = helper_rules(helper)
    except HelperParseError as error:
        return failures + [
            f"{HELPER_RELATIVE} could not be enumerated exactly, so the register "
            f"cannot be verified against it: {error}"
        ]

    helper_text = _collapse(
        _blank_comments(
            _normalize_newlines(helper if helper is not None else helper_source())
        )
    )
    failures += [
        f"register entry {entry['selector']!r} cites {entry['helperEvidence']!r}, "
        f"absent from {HELPER_RELATIVE}"
        for entry in BLIND_SPOT_REGISTER
        if _collapse(str(entry["helperEvidence"])) not in helper_text
    ]

    registered, register_duplicates = _by_signature(register_rules(), "register")
    applied, helper_duplicates = _by_signature(derived, "helper")
    failures += register_duplicates + helper_duplicates

    for key in sorted(set(applied) - set(registered)):
        failures.append(
            f"{HELPER_RELATIVE} applies {_describe(applied[key])}, which no "
            "register entry declares"
        )
    for key in sorted(set(registered) - set(applied)):
        failures.append(
            f"register declares {_describe(registered[key])}, which "
            f"{HELPER_RELATIVE} does not apply"
        )
    for key in sorted(set(registered) & set(applied)):
        expected, actual = registered[key], applied[key]
        for field in ("value", "important", "classification"):
            if expected[field] != actual[field]:
                failures.append(
                    f"{key[0]} rule `{key[1]}` property {key[2]!r}: register says "
                    f"{field}={expected[field]!r}, {HELPER_RELATIVE} says "
                    f"{field}={actual[field]!r}"
                )

    return failures


SNAPSHOT_DIRS = (
    "win32/visual.spec.ts-snapshots",
    "win32/visual-baseline-thumbnails.spec.ts-snapshots",
    "linux/visual.spec.ts-snapshots",
    "linux/visual-baseline-thumbnails.spec.ts-snapshots",
)


def snapshot_manifest() -> dict[str, dict[str, object]]:
    """Name + size manifest over the committed screenshot trees (F12).

    Deliberately not a content hash of the PNGs: the point is to make an
    accidental `--update-snapshots` loud, and a regenerated baseline changes its
    byte size essentially always while costing nothing to check. Content hashing
    162 files on every pytest run buys precision this guard does not need.
    """
    import hashlib

    root = ROOT / "e2e" / "__screenshots__"
    manifest: dict[str, dict[str, object]] = {}

    for relative in SNAPSHOT_DIRS:
        directory = root / relative
        files = sorted(path.name for path in directory.glob("*.png"))
        digest = hashlib.sha256()
        for name in files:
            digest.update(name.encode("utf-8"))
            digest.update(str((directory / name).stat().st_size).encode("utf-8"))
        manifest[relative] = {
            "count": len(files),
            "files": files,
            "nameAndSizeSha256": digest.hexdigest(),
        }

    return manifest


def fatigue_baseline_status() -> dict[str, str]:
    """N7 — `/fatigue` baselines are CREATED, on both platforms.

    Windows is generated locally. Linux can only come from the `visual-linux`
    deep-gate job, so the status is reported honestly rather than assumed; the
    contract asserts the set is all-or-nothing on each platform.
    """
    root = ROOT / "e2e" / "__screenshots__"
    expected = [
        f"fatigue-{viewport}-{theme}.png"
        for viewport in ("mobile", "tablet", "desktop")
        for theme in ("light", "dark")
    ]

    status = {}
    for platform in ("win32", "linux"):
        directory = root / platform / "visual.spec.ts-snapshots"
        present = sum(1 for name in expected if (directory / name).is_file())
        status[platform] = "created" if present == len(expected) else "pending"
    return status


def screenshot_tolerances() -> dict[str, object]:
    """The tolerance constants F3 says V1 cannot be enforced through.

    Recorded so a packet cannot quietly widen the oracle: `maxDiffPixels: 800`
    means up to 800 px per route × viewport × theme pass unnoticed, and the
    animated-logo band (1,039 / 1,046 px) sits *above* that tolerance — it is a
    real snapshot failure, not a diff the option absorbs.
    """
    helper = (ROOT / "e2e" / "visual-helpers.ts").read_text(encoding="utf-8")
    values: dict[str, object] = {}
    for key in ("maxDiffPixels", "threshold", "fullPage"):
        # Match the returned object literals (`key: 800,`), not the TypeScript
        # interface declarations above them (`key: number;`).
        found = re.findall(rf"{key}:\s*([^,;\n}}]+),", helper)
        values[key] = sorted({value.strip() for value in found})
    values["animatedLogoBandPx"] = [1039, 1046]
    values["bandExceedsTolerance"] = True
    return values
