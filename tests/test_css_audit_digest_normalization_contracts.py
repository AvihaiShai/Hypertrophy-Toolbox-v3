"""Contracts for the line-ending representation `j_known_live_mutation.mjs` pins.

LEFTOVERS P2.6. The control refuses to run against anything but a pinned digest
of `static/css/theme-dark.css`, and that digest used to be taken over the raw
bytes on disk. This repository is `core.autocrlf=true` with no `.gitattributes`,
so one commit materializes as LF in a Linux checkout and CRLF in a Windows one —
the same file, 574 bytes apart. The pin was therefore the Windows-only digest:
the control ran here and refused to run in CI, where the only way past it was the
`--expect-sha` override the tool's own docstring forbids using to silence it.

The repair is to hash a canonical representation — UTF-8 text with every CRLF
collapsed to LF — so both checkouts agree. These tests pin that property from
both directions: the constant must be the canonical digest of the tracked file,
the tool must accept both checkout forms and report identical digests for them,
and normalizing must not have cost the control its ability to refuse a
stylesheet that genuinely differs.
"""
from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "css_audit" / "j_known_live_mutation.mjs"
CSS_RELATIVE = Path("static/css/theme-dark.css")
NODE = shutil.which("node")

needs_node = pytest.mark.skipif(NODE is None, reason="node is not on PATH")


def _tracked_css_as_lf() -> str:
    """The stylesheet with line endings normalized, whatever this checkout has.

    ``newline=""`` disables Python's universal-newline translation so the CRLF a
    Windows checkout materializes is visible and can be collapsed deliberately,
    rather than being hidden on one platform and not the other.
    """
    raw = (ROOT / CSS_RELATIVE).read_text(encoding="utf-8", newline="")
    return raw.replace("\r\n", "\n")


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _pinned_digest() -> str:
    match = re.search(
        r"const EXPECTED_INPUT = '([0-9a-f]{64})';", SCRIPT.read_text(encoding="utf-8")
    )
    assert match, "EXPECTED_INPUT is no longer a single pinned sha256 literal"
    return match.group(1)


def _tree(directory: Path, css: str) -> Path:
    """Write a checkout-shaped root holding exactly the one file the tool reads."""
    target = directory / CSS_RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(css.encode("utf-8"))
    return directory


def _run_control(root: Path) -> subprocess.CompletedProcess[str]:
    assert NODE is not None
    return subprocess.run(
        [NODE, str(SCRIPT), "--root", str(root)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def _reported_digests(stdout: str) -> dict[str, str]:
    return dict(re.findall(r"^(before|after) +sha256 \(LF-normalized\): ([0-9a-f]{64})$",
                           stdout, flags=re.MULTILINE))


def test_the_pin_is_the_canonical_digest_of_the_tracked_stylesheet() -> None:
    """The constant must be the LF-normalized digest of the file in this checkout.

    This is the platform claim itself: a Windows worktree reaches it by
    collapsing CRLF, a Linux one is already there, and both must land on the
    committed blob's own digest. It also forces a *deliberate* re-pin — editing
    `theme-dark.css` reds this test, which is the intended cost, because the
    alternative is silencing the control with `--expect-sha`.
    """
    assert _pinned_digest() == _digest(_tracked_css_as_lf())


def test_the_superseded_pin_was_the_windows_only_digest() -> None:
    """Keeps the test above from being vacuous.

    If the two forms happened to hash alike, nothing here would be measuring
    anything. They do not: the CRLF form is one `CR` per line larger, and its
    digest is the constant this packet replaced.
    """
    lf = _tracked_css_as_lf()
    crlf = lf.replace("\n", "\r\n")
    assert len(crlf.encode("utf-8")) - len(lf.encode("utf-8")) == lf.count("\n")
    assert _digest(crlf) == "bd220b44ac4c9d036824b9c58346e049a00effe20e0effc6c2157d874c2d2352"
    assert _digest(crlf) != _pinned_digest()


@needs_node
def test_lf_and_crlf_checkouts_are_accepted_and_report_the_same_digests(tmp_path: Path) -> None:
    """The contract: the same commit in either checkout form runs the control.

    Both roots hold the same content and differ only in line endings. Each must
    pass the digest gate on the pinned constant alone — no `--expect-sha` — and
    both must report the same before and after digests, since those are the
    digests of the representation, not of the bytes.
    """
    lf = _tracked_css_as_lf()
    runs = {
        form: _run_control(_tree(tmp_path / form, text))
        for form, text in (("lf", lf), ("crlf", lf.replace("\n", "\r\n")))
    }

    for form, run in runs.items():
        assert run.returncode == 0, f"the {form} checkout was refused:\n{run.stderr}"

    digests = {form: _reported_digests(run.stdout) for form, run in runs.items()}
    assert digests["lf"] == digests["crlf"], "the two checkout forms disagree on the digests"
    assert digests["lf"]["before"] == _pinned_digest()
    assert digests["lf"]["after"] != digests["lf"]["before"], "the mutation was a no-op"


@needs_node
def test_each_checkout_keeps_its_own_line_endings_through_the_mutation(tmp_path: Path) -> None:
    """Only content is pinned; the write-back must not reformat the file.

    Normalizing for the digest would be a bad trade if it also rewrote a Windows
    worktree to LF — `git checkout --` would still revert it, but the mutated
    file measured between apply and revert would no longer be the bytes the
    browser is served in that checkout.
    """
    lf = _tracked_css_as_lf()
    roots = {form: _tree(tmp_path / form, text)
             for form, text in (("lf", lf), ("crlf", lf.replace("\n", "\r\n")))}
    for root in roots.values():
        assert _run_control(root).returncode == 0

    written = {form: (root / CSS_RELATIVE).read_bytes() for form, root in roots.items()}
    assert b"\r\n" not in written["lf"]
    assert b"\n" not in written["crlf"].replace(b"\r\n", b"")
    assert written["crlf"].replace(b"\r\n", b"\n") == written["lf"]


@needs_node
def test_the_control_still_refuses_a_stylesheet_that_genuinely_differs(tmp_path: Path) -> None:
    """Normalization must not have widened the gate to anything but line endings.

    A control that cannot be layered onto an already-mutated tree is the whole
    reason the digest check exists, so the refusal is asserted against a change
    that survives normalization — a colour edit, not a `CR`.
    """
    source = _tracked_css_as_lf()
    altered = source.replace("#0f0f14", "#0f0f15", 1)
    assert altered != source, "the colour this test edits is gone; pick another"
    run = _run_control(_tree(tmp_path / "altered", altered))

    assert run.returncode != 0, "an edited stylesheet was accepted"
    assert "LF-normalized text, not of the bytes on disk" in run.stderr
