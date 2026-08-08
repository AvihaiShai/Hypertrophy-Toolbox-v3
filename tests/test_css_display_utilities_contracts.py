"""Contracts for the Bootstrap display utilities (`d-*`).

The build imported `bootstrap/scss/utilities` (which only DEFINES the
`$utilities` map) and never `bootstrap/scss/utilities/api` (which emits the
classes), so every `d-*` class was inert for the app's whole history.

A class token is not a style: `toHaveClass(/d-none/)` stayed green throughout.
These assert that the stylesheet really declares the utility, and that no
template or module uses a `d-*` the build does not emit.

Full record: docs/dnone_display_utilities/EVIDENCE.md.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCSS = ROOT / "scss" / "custom-bootstrap.scss"
BUNDLE = ROOT / "static" / "css" / "bootstrap.custom.min.css"
CSS_DIR = ROOT / "static" / "css"
TEMPLATES = ROOT / "templates"
JS = ROOT / "static" / "js"

# `d-*` utilities the app uses that the build deliberately does NOT emit.
# Activating them is a rendering change, not a bug fix -- see the LEFTOVERS entry.
#
# This is an exact set, not an allowlist: a name that stops being used must come
# out, and a name that starts being used must be emitted or added here on
# purpose. Both directions are asserted below.
KNOWN_INERT = {
    "d-flex": "15 call sites; activating it re-flows session-summary and weekly-summary",
    "d-inline-block": "1 call site (fatigue.html:22 period select)",
}


def _strip_comments(css: str) -> str:
    """Blank out comments so a commented-out rule cannot satisfy a contract."""
    return re.sub(r"/\*.*?\*/", lambda m: " " * len(m.group(0)), css, flags=re.S)


def _emitted_display_classes(css: str) -> dict[str, list[tuple[str, str]]]:
    """Map `d-*` class -> [(declared display value, priority)] from a stylesheet.

    Parsed from the built artifact rather than predicted from the SCSS, because
    the artifact is what the browser loads and what the defect lived in.
    """
    found: dict[str, list[tuple[str, str]]] = {}
    for head, body in re.findall(r"([^{}]*)\{([^{}]*)\}", _strip_comments(css)):
        # A UTILITY is a bare `.d-*` selector. Token containment is not enough:
        # `a11y.css` carries `#error-message-container.d-none{display:none!important}`,
        # whose head contains `.d-none` and whose body sets `display` -- so a
        # containment test credits `d-none` as emitted even on the pre-fix tree,
        # where no utility existed. That blinds this module on the very class it
        # exists to guard. An ID-scoped rule styles one element; it is not a utility.
        classes = {
            match.group(1)
            for selector in head.split(",")
            if (match := re.fullmatch(r"\s*\.(d-[a-z0-9-]+)\s*", selector))
        }
        for cls in classes:
            match = re.search(r"(?<![\w-])display\s*:\s*([^;!}]+)(\s*!important)?", body)
            if match:
                found.setdefault(cls, []).append(
                    (match.group(1).strip(), "important" if match.group(2) else "")
                )
    return found


def _classes_used_by_the_app() -> dict[str, set[str]]:
    """Every `d-*` class token the templates or JS modules apply, by file."""
    class_attr = re.compile(r"""class\s*=\s*["']([^"']*)["']""")
    class_name = re.compile(r"""className\s*=\s*["'`]([^"'`]*)["'`]""")
    list_call = re.compile(r"""classList\.(?:add|toggle|remove|replace)\(\s*["']([\w-]+)["']""")

    used: dict[str, set[str]] = {}
    for base, pattern in ((TEMPLATES, "**/*.html"), (JS, "**/*.js")):
        for path in base.glob(pattern):
            if "__tests__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            tokens: set[str] = set()
            for match in class_attr.finditer(text):
                tokens.update(match.group(1).split())
            for match in class_name.finditer(text):
                tokens.update(match.group(1).split())
            tokens.update(list_call.findall(text))
            for token in tokens:
                if re.fullmatch(r"d-[a-z0-9-]+", token):
                    used.setdefault(token, set()).add(str(path.relative_to(ROOT)))
    return used


def test_the_build_emits_the_display_utility_api() -> None:
    """The SCSS imports the API that actually emits `d-*`, not just the map.

    Red path: delete the `utilities/api` import and this fails.
    """
    scss = SCSS.read_text(encoding="utf-8")
    assert re.search(r'@import\s+["\']bootstrap/scss/utilities/api["\']', scss), (
        "scss/custom-bootstrap.scss no longer imports bootstrap/scss/utilities/api. "
        "Without it the $utilities map is defined but no utility class is emitted, "
        "and every d-* class in the templates silently does nothing."
    )


def test_d_none_resolves_to_display_none_important() -> None:
    """`.d-none` is a real declaration in the built bundle, not just a token.

    Red path: rebuild without the API import and this fails.
    """
    emitted = _emitted_display_classes(BUNDLE.read_text(encoding="utf-8"))
    assert "d-none" in emitted, (
        "the built bundle does not define .d-none at all; anything relying on it "
        "renders visible"
    )
    assert ("none", "important") in emitted["d-none"], (
        f".d-none does not declare `display: none !important`; got {emitted['d-none']}. "
        "Bootstrap's display utilities are !important by design, and the app's own "
        "bundles set display on some of these elements."
    )


def test_the_responsive_partner_of_d_none_is_emitted() -> None:
    """`d-lg-inline` ships too, because it is half of an indivisible pair.

    `templates/base.html:213,219` use `class="d-none d-lg-inline"` -- hidden by
    default, inline from `lg` up. Emitting `d-none` without `d-lg-inline` would
    hide those two labels permanently, turning one defect into another.

    Red path: restrict the utility's values to `none` alone and this fails.
    """
    css = _strip_comments(BUNDLE.read_text(encoding="utf-8"))
    emitted = _emitted_display_classes(css)
    assert "d-lg-inline" in emitted, (
        ".d-lg-inline is not emitted, but base.html pairs it with .d-none; without "
        "it the Simple and Dark Mode labels are hidden at every width"
    )
    assert ("inline", "important") in emitted["d-lg-inline"]

    # And it must be inside the lg breakpoint, not unconditional. Assert the exact
    # emitted shape rather than trying to slice out the media block: `(.*?)\}\s*(?=@|\Z)`
    # is not a balanced-brace parser, so it runs past the block's real end to the next
    # at-rule and can satisfy this by textual proximity -- the very thing being checked.
    # `[^@{}]*` cannot cross into or out of a nested block, so this cannot over-reach.
    assert re.search(
        r"@media\s*\(min-width:\s*992px\)\s*\{[^@]*?\.d-lg-inline\s*\{[^{}]*?"
        r"display\s*:\s*inline\s*!important",
        css,
    ), (
        ".d-lg-inline is emitted but not inside a (min-width: 992px) query, so the "
        "label would show below the lg breakpoint too"
    )


def test_no_template_uses_a_display_utility_the_build_does_not_emit() -> None:
    """The contract that would have caught the original defect.

    Red path: add `class="d-md-flex"` to any template and this fails.
    """
    emitted: set[str] = set()
    for path in sorted(CSS_DIR.glob("*.css")):
        emitted |= set(_emitted_display_classes(path.read_text(encoding="utf-8", errors="replace")))

    used = _classes_used_by_the_app()
    unsupported = {
        cls: sorted(files) for cls, files in used.items()
        if cls not in emitted and cls not in KNOWN_INERT
    }
    assert unsupported == {}, (
        "these d-* utilities are used by the app but no loaded stylesheet defines "
        f"them, so they do nothing: {unsupported}. Either emit them from "
        "scss/custom-bootstrap.scss (and re-measure the visual impact -- turning a "
        "display utility on is a rendering change) or record them in KNOWN_INERT "
        "with the reason."
    )


def test_the_known_inert_list_has_no_stale_entries() -> None:
    """KNOWN_INERT is an exact set, so it cannot rot into a blanket exemption.

    Red path: add a name nothing uses to KNOWN_INERT and this fails.
    """
    used = _classes_used_by_the_app()
    emitted: set[str] = set()
    for path in sorted(CSS_DIR.glob("*.css")):
        emitted |= set(_emitted_display_classes(path.read_text(encoding="utf-8", errors="replace")))

    unused = sorted(cls for cls in KNOWN_INERT if cls not in used)
    assert unused == [], (
        f"KNOWN_INERT names utilities the app no longer uses: {unused}. Remove them."
    )
    now_emitted = sorted(cls for cls in KNOWN_INERT if cls in emitted)
    assert now_emitted == [], (
        f"KNOWN_INERT names utilities the build now emits: {now_emitted}. They are "
        "no longer inert -- remove them from the list so the coverage above applies."
    )


@pytest.mark.parametrize("selector", [".d-flex", ".d-inline-block"])
def test_the_deliberately_withheld_utilities_stay_withheld(selector: str) -> None:
    """The narrowing is deliberate and pinned, so it cannot widen by accident.

    Emitting the display utility's full value list activates these two and
    re-flows session-summary and weekly-summary -- 18 of 66 visual captures moved
    when measured. That is an owner-reviewed visual change with its own baseline
    regeneration, not something this bug fix carries.

    Red path: drop the `values: none inline` narrowing and this fails.
    """
    emitted = _emitted_display_classes(BUNDLE.read_text(encoding="utf-8"))
    assert selector.lstrip(".") not in emitted, (
        f"{selector} is now emitted. That is a rendering change on session-summary "
        "and weekly-summary; it needs its own visual baseline review, and this "
        "contract plus KNOWN_INERT must be updated in the same change."
    )
