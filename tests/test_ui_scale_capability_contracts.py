"""Pin the capability-based application-scale controls from #607."""

from __future__ import annotations

import re
from pathlib import Path

from tests.test_css_wp4_4_a11y_contracts import _strip_comments

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "static" / "css"
HOOK = r"data-scale-control-item(?![\w-])"
FALLBACK = r"@supports\s+not\s*\(\s*zoom\s*:\s*1\s*\)"


def test_runtime_styles_have_no_firefox_document_override():
    offenders = [
        path.name
        for path in sorted(CSS.glob("*.css"))
        if re.search(r"@-moz-document\b", _strip_comments(path.read_text(encoding="utf-8")))
    ]
    assert not offenders, f"Firefox document overrides reappeared in {offenders}"


def test_application_scale_writes_zoom_without_browser_or_capability_branch():
    source = (ROOT / "static" / "js" / "accessibility.js").read_text(encoding="utf-8")
    source = re.sub(r"//[^\n]*", lambda comment: " " * len(comment[0]), _strip_comments(source))
    assert not re.search(r"firefox|useragent", source, re.I)

    function = re.search(r"\.applyScale\s*=\s*function\(level\)\s*\{(.*?)^ {4}\};", source, re.S | re.M)
    assert function, "Could not locate the application-scale function"
    body = function[1]
    assert not re.search(r"\bnavigator\b|\bCSS\.supports\b|\bremoveProperty\b", body)
    assert not re.search(r"\bif\b|\?|&&|\|\|", body)
    writes = re.findall(r"document\.documentElement\.style\.zoom\s*=\s*zoomValue\s*;", body)
    assert len(writes) == 1


def test_unsupported_zoom_hides_only_the_scale_item_and_trailing_divider():
    source = _strip_comments((CSS / "a11y.css").read_text(encoding="utf-8"))
    assert len(re.findall(FALLBACK, source)) == 1
    selector = rf"#navbar\s+\.nav-item\[{HOOK}\]"
    rule = re.compile(
        rf"{FALLBACK}\s*\{{\s*{selector}\s*,\s*{selector}\s*\+\s*\.nav-divider\s*"
        r"\{\s*display\s*:\s*none\s*!\s*important\s*;\s*\}\s*\}"
    )
    assert rule.search(source), "The fallback must hide the hooked item and its next divider"
    assert not re.search(HOOK, rule.sub("", source))
    for path in CSS.glob("*.css"):
        if path.name != "a11y.css":
            assert not re.search(HOOK, _strip_comments(path.read_text(encoding="utf-8"))), path.name


def test_scale_hook_is_on_the_item_immediately_before_its_divider():
    template = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
    template = re.sub(r"<!--.*?-->", "", template, flags=re.S)
    assert len(re.findall(HOOK, template)) == 1
    item = re.search(
        rf"<li\b(?P<attrs>[^>]*\s{HOOK}(?=\s|>)[^>]*)>(?P<body>(?:(?!</?li\b).)*)</li>",
        template,
        re.S,
    )
    assert item, "The scale hook belongs on the scale list item"
    item_class = re.search(r'\sclass="([^"]*)"', item["attrs"])
    assert item_class and "nav-item" in item_class[1].split()
    body_classes = re.findall(r'\sclass="([^"]*)"', item["body"])
    assert any("scale-control-compact" in classes.split() for classes in body_classes)
    divider = re.match(r'\s*<li\b[^>]*\sclass="([^"]*)"', template[item.end():])
    assert divider and "nav-divider" in divider[1].split()


def test_navbar_and_modal_keep_capability_gated_counter_zoom():
    for name, selector in (("a11y.css", "#navbar"), ("components.css", ".modal")):
        source = _strip_comments((CSS / name).read_text(encoding="utf-8"))
        assert re.search(
            rf"@supports\s*\(\s*zoom\s*:\s*1\s*\)\s*\{{\s*{re.escape(selector)}\s*"
            r"\{\s*zoom\s*:\s*var\(\s*--ui-scale-inverse\s*,\s*1\s*\)\s*;\s*\}\s*\}",
            source,
        ), f"{name} lost capability-gated counter zoom for {selector}"
