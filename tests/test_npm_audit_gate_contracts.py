"""Contracts for `scripts/npm_audit_gate.mjs` -- the js-supply-chain verdict.

`docs/NPM_AUDIT_SEVERITY_POLICY_DECISION.md` section 5.2 states the standard this
file has to meet, and states it as a warning rather than a nicety:

    M2's validator must be mutation-tested in BOTH directions before it is
    trusted: corrupt the JSON, drop a required field, forge an expired entry,
    forge a stale entry, and confirm each reds -- then confirm a clean file
    greens. A validator that only ever sees valid input is indistinguishable
    from one that parses nothing, which is precisely the
    `test_compiled_scss_drift_gate` failure mode.

So every rule below is asserted twice. `test_the_gate_reds_on` drives a mutation
of a known-green pair through the real script and requires exit 1 plus a message
that names the rule; `test_the_gate_greens_on` drives the cases that must NOT
fail, including the four that are one flipped comparison away from the red ones
-- an advisory below the floor, a severity that fell rather than rose, an
allowlist entry that is merely close to expiry, and npm's own exit code 1 on a
report that is perfectly readable.

The green half is the half that matters. A gate that fails on everything is
useless in the opposite direction and would still pass a red-only suite.

`node` is invoked as a subprocess rather than the logic being reimplemented in
Python, following `tests/test_css_audit_digest_normalization_contracts.py`. The
`test` job in `ci.yml` pins `node-version: '24'` for exactly this reason.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "npm_audit_gate.mjs"
ALLOWLIST = ROOT / "docs" / "npm_audit_allowlist.json"
CI = ROOT / ".github" / "workflows" / "ci.yml"
NODE = shutil.which("node")

needs_node = pytest.mark.skipif(NODE is None, reason="node is not on PATH")

# A date every fixture below is written relative to, so no test depends on when
# it runs. The script takes `--today` for this; CI never passes it.
TODAY = "2026-09-01"

# The rulings, pinned here so loosening one in the script reds this file rather
# than silently widening the gate. Read out of the source instead of retyped, so
# these cannot drift into a second copy of the policy.
_SOURCE = SCRIPT.read_text(encoding="utf-8")


def _constant(name: str) -> str:
    match = re.search(rf"^const {name} = (.+);$", _SOURCE, re.MULTILINE)
    assert match, f"{name} is no longer a single top-level const in {SCRIPT.name}"
    return match.group(1).strip()


def _required_fields() -> list[str]:
    """The entry format's required fields, read out of the script.

    Hard-coding them here would make "every required field is asserted" a claim
    about this file's copy rather than about the format, and a field added to the
    script would quietly arrive untested.
    """
    match = re.search(r"^const REQUIRED_FIELDS = \[(.*?)\];$", _SOURCE, re.MULTILINE | re.DOTALL)
    assert match, f"REQUIRED_FIELDS is no longer a single top-level const in {SCRIPT.name}"
    fields = re.findall(r"'([A-Za-z]+)'", match.group(1))
    assert fields, "REQUIRED_FIELDS parsed to an empty list"
    return fields


REQUIRED_FIELDS = _required_fields()


def test_every_field_section_4_2_calls_required_is_required_in_the_script():
    """Section 4.2: "Every field is required. There is no optional field and no
    default, because every omission this format could tolerate is an omission
    that makes an entry unreviewable." Pinned here so a field cannot be softened
    to optional without this test saying so."""
    assert REQUIRED_FIELDS == [
        "id",
        "package",
        "severity",
        "rationale",
        "owner",
        "approvedOn",
        "expiresOn",
    ]


def test_the_signed_rulings_are_still_what_the_script_enforces():
    """D-1, D-3 and the schema version, asserted against the source.

    This is the vacuity floor for the constants: every fixture below is built
    around a `high` floor and a 90-day ceiling, so a script that quietly moved
    either would make half of the red cases pass for the wrong reason.
    """
    assert _constant("SEVERITY_FLOOR") == "'high'", "D-1: the floor is `high` and above"
    assert _constant("MAX_TTL_DAYS") == "90", "D-3: MAX_TTL is 90 days"
    assert _constant("SCHEMA_VERSION") == "1"


# --------------------------------------------------------------------- fixtures


def _audit(vulnerabilities: dict, counts: dict | None = None) -> dict:
    """An `npm audit --json` report, shaped as npm actually writes one.

    `metadata.vulnerabilities` is deliberately allowed to disagree with the
    `via` entries: section 4.4 requires the exit status to come from the
    per-advisory severities and the counters to drive the job summary only. A
    fixture where the two disagree is the only way to prove the script reads the
    one it is supposed to.
    """
    return {
        "auditReportVersion": 2,
        "vulnerabilities": vulnerabilities,
        "metadata": {
            "vulnerabilities": counts
            or {"info": 0, "low": 0, "moderate": 0, "high": 0, "critical": 0, "total": 0},
            "dependencies": {
                "prod": 1,
                "dev": 283,
                "optional": 70,
                "peer": 1,
                "peerOptional": 0,
                "total": 283,
            },
        },
    }


def _via(ghsa: str, package: str, severity: str) -> dict:
    return {
        "source": 1108500,
        "name": package,
        "dependency": package,
        "title": f"{package} is affected by {ghsa}",
        "url": f"https://github.com/advisories/{ghsa}",
        "severity": severity,
        "cwe": ["CWE-1333"],
        "range": "<1.2.3",
    }


def _package(ghsa: str, package: str, severity: str, package_severity: str | None = None) -> dict:
    return {
        package: {
            "name": package,
            # The package-level severity is the maximum across the package's
            # advisories. Section 4.4: reading it instead of `via[].severity`
            # is the specific defect this shape exists to catch.
            "severity": package_severity or severity,
            "isDirect": False,
            "via": [_via(ghsa, package, severity)],
            "effects": [],
            "range": "<1.2.3",
            "nodes": [f"node_modules/{package}"],
            "fixAvailable": True,
        }
    }


HIGH_GHSA = "GHSA-abcd-1234-wxyz"
CLEAN_AUDIT = _audit({})
HIGH_AUDIT = _audit(
    _package(HIGH_GHSA, "picomatch", "high"),
    {"info": 0, "low": 0, "moderate": 0, "high": 1, "critical": 0, "total": 1},
)


def _entry(**overrides) -> dict:
    entry = {
        "id": HIGH_GHSA,
        "package": "picomatch",
        "severity": "high",
        "rationale": (
            "Transitive devDependency of stylelint only; no fix in range and no runtime "
            "reachability. Tracked for removal with the stylelint 17 bump."
        ),
        "owner": "avihay1989",
        "approvedOn": "2026-08-20",
        "expiresOn": "2026-10-20",
    }
    entry.update(overrides)
    return entry


def _allow(*entries: dict) -> dict:
    return {"schemaVersion": 1, "note": "test fixture", "allow": list(entries)}


def _run(tmp_path: Path, audit, allowlist, *extra: str) -> subprocess.CompletedProcess:
    """Write both inputs and run the real script over them.

    `audit` and `allowlist` are dicts to be serialized, or raw `str` to be
    written verbatim -- which is how the unparseable-input cases are expressed
    without a JSON encoder refusing to produce them.
    """
    assert NODE is not None
    audit_path = tmp_path / "npm-audit.json"
    allow_path = tmp_path / "allowlist.json"
    for path, value in ((audit_path, audit), (allow_path, allowlist)):
        if value is None:
            continue  # deliberately absent
        path.write_text(
            value if isinstance(value, str) else json.dumps(value, indent=2),
            encoding="utf-8",
        )

    return subprocess.run(
        [
            NODE,
            str(SCRIPT),
            "--audit",
            str(audit_path),
            "--allowlist",
            str(allow_path),
            "--today",
            TODAY,
            "--summary",
            str(tmp_path / "summary.md"),
            *extra,
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


# ------------------------------------------------------- direction 1: must red

RED_CASES = {
    # D-4 -- the audit side. The owner's instruction names this one explicitly:
    # the gate must fail closed on invalid or unparseable JSON.
    "audit json is truncated mid-object": (
        '{"auditReportVersion": 2, "vulnerabilities": {',
        _allow(),
        "not valid JSON",
    ),
    "audit json is empty": ("", _allow(), "not valid JSON"),
    "audit json is a bare array": ("[]", _allow(), "not a JSON object"),
    "audit json is html from a proxy": (
        "<html><body>502 Bad Gateway</body></html>",
        _allow(),
        "not valid JSON",
    ),
    "audit file is absent": (None, _allow(), "could not be read"),
    "audit reports a registry error instead of a report": (
        {"error": {"code": "ENOTFOUND", "summary": "request to registry failed"}},
        _allow(),
        "reported an error instead of a report",
    ),
    "audit report version is one this gate has not read": (
        {"auditReportVersion": 3, "vulnerabilities": {}, "metadata": {}},
        _allow(),
        "auditReportVersion",
    ),
    "audit report has no vulnerabilities mapping": (
        {"auditReportVersion": 2, "metadata": {}},
        _allow(),
        "no `vulnerabilities` mapping",
    ),
    "audit report has no metadata block": (
        {"auditReportVersion": 2, "vulnerabilities": {}},
        _allow(),
        "metadata",
    ),
    "an advisory carries no GHSA id": (
        _audit(
            {
                "picomatch": {
                    "name": "picomatch",
                    "severity": "high",
                    "via": [{"title": "unkeyable", "severity": "high", "url": "https://x/"}],
                    "fixAvailable": True,
                }
            }
        ),
        _allow(),
        "carries no GHSA id",
    ),
    "an advisory carries a severity outside the scale": (
        _audit(_package(HIGH_GHSA, "picomatch", "catastrophic")),
        _allow(),
        "which is not one of",
    ),
    # The gate's whole purpose.
    "a high advisory is not allowlisted": (HIGH_AUDIT, _allow(), HIGH_GHSA),
    "a critical advisory is not allowlisted": (
        _audit(_package("GHSA-crit-crit-crit", "postcss", "critical")),
        _allow(),
        "GHSA-crit-crit-crit",
    ),
    # The allowlist side. Every one of these must make the gate HARDER to pass.
    "allowlist is absent": (HIGH_AUDIT, None, "missing"),
    "allowlist json is truncated": (HIGH_AUDIT, '{"schemaVersion": 1, "allow": [', "not valid JSON"),
    "allowlist json is a bare array": (HIGH_AUDIT, "[]", "must be a JSON object"),
    "allowlist declares a future schema version": (
        HIGH_AUDIT,
        {"schemaVersion": 2, "allow": [_entry()]},
        "schemaVersion",
    ),
    "allowlist has no allow array": (HIGH_AUDIT, {"schemaVersion": 1}, "no `allow` array"),
    "allow holds something that is not an object": (
        HIGH_AUDIT,
        {"schemaVersion": 1, "allow": [HIGH_GHSA]},
        "is not an object",
    ),
    "the id is a CVE rather than a GHSA": (
        HIGH_AUDIT,
        _allow(_entry(id="CVE-2026-0001")),
        "is not a GHSA id",
    ),
    "the id is a bare package name": (
        HIGH_AUDIT,
        _allow(_entry(id="picomatch")),
        "is not a GHSA id",
    ),
    "two entries claim one advisory": (
        HIGH_AUDIT,
        _allow(_entry(), _entry(owner="someone-else")),
        "duplicates",
    ),
    "the entry carries a field this schema does not define": (
        HIGH_AUDIT,
        _allow(_entry(expiresOnn="2026-10-20")),
        "is not a field of schemaVersion",
    ),
    "a required field is present but blank": (
        HIGH_AUDIT,
        _allow(_entry(owner="   ")),
        "allow[0].owner is missing, empty, or not a string",
    ),
    "a required field holds a number rather than a string": (
        HIGH_AUDIT,
        _allow(_entry(approvedOn=20260820)),
        "allow[0].approvedOn is missing, empty, or not a string",
    ),
    "the rationale is a shrug": (
        HIGH_AUDIT,
        _allow(_entry(rationale="dev only")),
        "at least 40",
    ),
    "the severity recorded is off the scale": (
        HIGH_AUDIT,
        _allow(_entry(severity="scary")),
        "is not one of",
    ),
    "approvedOn is not a date": (
        HIGH_AUDIT,
        _allow(_entry(approvedOn="last tuesday")),
        "approvedOn",
    ),
    "expiresOn is a day that does not exist": (
        HIGH_AUDIT,
        _allow(_entry(approvedOn="2026-08-20", expiresOn="2026-09-31")),
        "expiresOn",
    ),
    "the entry expires before it was approved": (
        HIGH_AUDIT,
        _allow(_entry(approvedOn="2026-08-20", expiresOn="2026-08-01")),
        "on or before its approval",
    ),
    "the entry already expired": (
        HIGH_AUDIT,
        _allow(_entry(approvedOn="2026-06-01", expiresOn="2026-08-30")),
        "expired on 2026-08-30",
    ),
    "the entry expires the day the gate runs": (
        HIGH_AUDIT,
        _allow(_entry(approvedOn="2026-07-01", expiresOn=TODAY)),
        f"expired on {TODAY}",
    ),
    "the TTL outruns the 90-day ceiling by one day": (
        HIGH_AUDIT,
        _allow(_entry(approvedOn="2026-08-20", expiresOn="2026-11-19")),
        "91-day TTL",
    ),
    "the TTL is the year 2099": (
        HIGH_AUDIT,
        _allow(_entry(approvedOn="2026-08-20", expiresOn="2099-01-01")),
        "D-3 caps it",
    ),
    # D-5.
    "the allowlisted advisory has left the audit": (
        CLEAN_AUDIT,
        _allow(_entry()),
        "STALE",
    ),
    # Section 4.5, severity rise.
    "the allowlisted advisory was re-scored upward": (
        _audit(_package(HIGH_GHSA, "picomatch", "critical")),
        _allow(_entry(severity="high")),
        "above the high recorded",
    ),
    # Section 4.5, npm itself failing rather than reporting.
    "npm audit exited 2 with a report": (HIGH_AUDIT, _allow(), "which is npm failing"),
}

# Section 5.2 names "drop a required field" as one of the five mutations this
# validator has to survive, and it is the one a hand-picked case list is most
# likely to under-cover: writing two of the seven by hand looks like coverage and
# leaves five fields whose absence is unasserted. Generated over the whole set so
# adding a field to the format cannot outrun its test.
for _field in REQUIRED_FIELDS:
    RED_CASES[f"the entry has no {_field}"] = (
        HIGH_AUDIT,
        _allow({k: v for k, v in _entry().items() if k != _field}),
        f"allow[0].{_field} is missing, empty, or not a string",
    )


@needs_node
@pytest.mark.parametrize("case", sorted(RED_CASES), ids=lambda name: name.replace(" ", "_"))
def test_the_gate_reds_on(tmp_path, case):
    audit, allowlist, expected = RED_CASES[case]
    extra = ["--audit-exit-status", "2"] if "exited 2" in case else []
    result = _run(tmp_path, audit, allowlist, *extra)

    assert result.returncode == 1, (
        f"{case!r} must fail the job.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert expected in result.stderr, (
        f"{case!r} failed, but for a reason that does not mention {expected!r}. "
        f"A gate that reds by accident is not a gate.\nstderr:\n{result.stderr}"
    )
    # A failure has to be legible in the Actions UI, not only in the raw log.
    assert "::error title=npm audit::" in result.stdout


# ----------------------------------------------------- direction 2: must green

GREEN_CASES = {
    # The steady state R2 was chosen to reach: gate on, file empty.
    "a clean graph against an empty allowlist": (CLEAN_AUDIT, _allow(), []),
    # D-1: the floor is `high`, so these are reported and not blocking. Without
    # this pair the floor could be `info` and every red case above would still
    # pass.
    "a moderate advisory nobody allowlisted": (
        _audit(_package("GHSA-modr-modr-modr", "postcss", "moderate")),
        _allow(),
        [],
    ),
    "a low advisory nobody allowlisted": (
        _audit(_package("GHSA-lowl-lowl-lowl", "nanoid", "low")),
        _allow(),
        [],
    ),
    # Section 4.4, stated as a ruling and asserted here because it is invisible
    # from every other case: the package rolls up to `high`, the advisory itself
    # is `moderate`, and reading the wrong one blocks on an advisory D-1 never
    # meant to cover.
    "a moderate advisory inside a package that rolls up to high": (
        _audit(_package("GHSA-modr-insi-high", "postcss", "moderate", package_severity="high")),
        _allow(),
        [],
    ),
    # The allowlist actually working.
    "a high advisory with a valid unexpired entry": (HIGH_AUDIT, _allow(_entry()), []),
    "an entry expiring tomorrow is still an entry": (
        HIGH_AUDIT,
        _allow(_entry(approvedOn="2026-08-20", expiresOn="2026-09-02")),
        [],
    ),
    "the TTL sits exactly on the 90-day ceiling": (
        HIGH_AUDIT,
        _allow(_entry(approvedOn="2026-08-20", expiresOn="2026-11-18")),
        [],
    ),
    # Section 4.5: a fall is strictly less exposure than what was approved.
    "the allowlisted advisory was re-scored downward": (
        _audit(_package(HIGH_GHSA, "picomatch", "moderate")),
        _allow(_entry(severity="high")),
        [],
    ),
    # Section 4.5: npm exits 1 for ANY advisory, allowlisted ones included.
    # Using that exit code directly is what would make the allowlist inert.
    "npm exited 1 over an advisory the allowlist covers": (
        HIGH_AUDIT,
        _allow(_entry()),
        ["--audit-exit-status", "1"],
    ),
}


@needs_node
@pytest.mark.parametrize("case", sorted(GREEN_CASES), ids=lambda name: name.replace(" ", "_"))
def test_the_gate_greens_on(tmp_path, case):
    audit, allowlist, extra = GREEN_CASES[case]
    result = _run(tmp_path, audit, allowlist, *extra)

    assert result.returncode == 0, (
        f"{case!r} must NOT fail the job. A gate that reds on everything is as useless as one "
        f"that greens on everything.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
    assert "npm_audit_gate: PASSED." in result.stdout


# --------------------------------------------------- the committed artifacts


def test_the_committed_allowlist_is_an_empty_list_and_not_a_missing_file():
    """R2's outcome, section 6.1: the enforcement PR lands the allowlist empty.

    `"allow": []` and a deleted file must never look alike, so the emptiness is
    asserted through a parsed document rather than through the file's absence.
    """
    doc = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    assert doc["schemaVersion"] == 1
    assert doc["allow"] == [], (
        "The accepted-debt bucket was measured empty (section 3). An entry appearing here "
        "needs an owner decision, not an implementer's judgement call."
    )
    assert "NPM_AUDIT_SEVERITY_POLICY_DECISION.md" in doc["note"]


@needs_node
def test_the_committed_allowlist_passes_the_real_gate_against_the_real_audit(tmp_path):
    """End to end over the two files CI actually reads, with no fixture in between.

    Every case above builds its allowlist in `tmp_path`; if the committed file
    were malformed, not one of them would notice.
    """
    assert NODE is not None
    audit = tmp_path / "npm-audit.json"
    audit.write_text(json.dumps(CLEAN_AUDIT), encoding="utf-8")
    result = subprocess.run(
        [NODE, str(SCRIPT), "--audit", str(audit), "--allowlist", str(ALLOWLIST)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0, result.stderr


@needs_node
def test_a_waived_advisory_is_reported_with_dates_a_reviewer_can_read(tmp_path):
    """Section 4.5: an allowlisted advisory passes, and is "listed in the summary
    with owner and days remaining" — visible, dated, attributable.

    Pinned because the dates are the half that fails silently. The validator has
    to parse `expiresOn` into a timestamp to compare it, and carrying that
    timestamp back under the same key renders every date in the summary as a
    13-digit epoch. The gate still exits 0, so nothing else in this file notices.
    """
    result = _run(tmp_path, HIGH_AUDIT, _allow(_entry()))
    assert result.returncode == 0, result.stderr

    summary = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "#### Allowlisted, unexpired" in summary
    assert f"`{HIGH_GHSA}`" in summary
    assert "2026-10-20" in summary, f"expiresOn is not rendered as a date:\n{summary}"
    assert "avihay1989" in summary
    # 2026-09-01 -> 2026-10-20.
    assert "| 49 |" in summary, f"days-remaining is not rendered:\n{summary}"
    # The same date has to survive into the annotation a reviewer sees in the log.
    assert "until 2026-10-20 (49 days left)" in result.stdout


@needs_node
def test_a_misinvocation_is_not_a_pass(tmp_path):
    """Exit 2, never 0. A typo in the workflow's argv must not read as "clean"."""
    assert NODE is not None
    for argv in (
        [],
        ["--audit", str(tmp_path / "a.json")],
        ["--audit", "a.json", "--allowlist", "b.json", "--not-a-flag", "x"],
        ["--audit", "a.json", "--allowlist", "b.json", "--today", "not-a-date"],
    ):
        result = subprocess.run(
            [NODE, str(SCRIPT), *argv], capture_output=True, text=True, cwd=ROOT
        )
        assert result.returncode == 2, f"{argv} should be a usage error, got {result.returncode}"


# --------------------------------------------------------------- M3: the wiring


def _js_supply_chain_block() -> str:
    source = CI.read_text(encoding="utf-8")
    start = source.index("\n  js-supply-chain:\n")
    rest = source[start + 1 :]
    end = re.search(r"^  [A-Za-z0-9_-]+:[ \t]*$", rest[len("  js-supply-chain:\n") :], re.MULTILINE)
    return rest[: len("  js-supply-chain:\n") + end.start()] if end else rest


def _executable(block: str) -> str:
    """`block` with whole-line comments removed.

    Every "this string must not appear" assertion below has to read code rather
    than prose: the job's own comments explain what `continue-on-error` and
    `exit 0` used to do there, and those sentences are the record, not a
    violation of it.
    """
    return "\n".join(
        line for line in block.splitlines() if not line.lstrip().startswith("#")
    )


def test_the_supply_chain_job_still_exists_under_its_pinned_name():
    """Vacuity floor for the three assertions below.

    They all read one job block. A parser that stops finding it turns "the job
    does not swallow failures" into a statement about the empty string.
    """
    block = _js_supply_chain_block()
    assert len(block.splitlines()) > 20, "the js-supply-chain block did not parse"
    assert "    name: JS Supply Chain (npm audit, non-required)" in block, (
        "The name is pinned at tests/test_release_workflow_contracts.py and must stay "
        "byte-identical; the `(non-required)` suffix stays accurate because M3 does not "
        "touch branch protection."
    )


def test_the_flip_is_both_edits_and_not_just_one():
    """The `test-inventory` precedent, stated in ci.yml's own comments: an
    `exit 0` step can never fail, and `continue-on-error` swallows a real
    failure. Either one alone leaves the gate open, so both are asserted.
    """
    block = _executable(_js_supply_chain_block())
    assert "continue-on-error" not in block, (
        "L2: `continue-on-error` on this job turns a red gate neutral-green again"
    )
    assert not re.search(r"^\s*exit 0\s*$", block, re.MULTILINE), (
        "L1: a trailing `exit 0` makes the step incapable of failing whatever the gate decides"
    )


def test_the_job_runs_the_gate_script_rather_than_an_inline_reimplementation():
    """Section 4.5 moved the verdict into a script file so it is testable from
    pytest the way `scripts/release_gate.py` is. An inline `node -e` block that
    grew back would be untested by every case in this file and still look like a
    working gate in the workflow."""
    block = _executable(_js_supply_chain_block())
    assert "scripts/npm_audit_gate.mjs" in block
    assert "docs/npm_audit_allowlist.json" in block
    assert "--omit=dev" not in block, "D-2: the gate reads the whole graph"
