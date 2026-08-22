# npm audit — severity and exception policy: owner decision packet

*Status: **DECIDED 2026-08-15 (§6.1) and now EXECUTED.** The owner accepted every
recommendation in §6, including **D-7: remediate first, then enforce**. Everything
those seven rulings authorize has since landed — the remediation (M1) and the
enforcement flip (M2 + M3) — and `js-supply-chain` blocks on a `high` advisory today.
**M4 is deliberately not taken**: promoting the job into branch protection is lever L3,
which no ruling on this page authorizes. §5.4 is the ledger. This file records the
decisions and the evidence behind them.*

> **Every measurement below is dated 2026-08-15 and several are now superseded.**
> They are kept as written, because a decision has to be readable against the evidence
> that was actually in front of the owner. Where a later measurement contradicts one,
> the contradiction is annotated in place and marked **SUPERSEDED** — the original
> number is never edited to match today. The three that moved:
>
> | Measured 2026-08-15 | True as of 2026-08-21 | Where |
> |---|---|---|
> | Five high-severity advisories, nine advisory IDs, five packages | **Zero advisories of any severity** — cleared by M1 (#390) | §2.1, §3 |
> | Dependabot alerts **disabled** (403 / 404) | **Enabled**, zero open (200 / 204) — D-6's setting half | §2.4 |
> | `js-supply-chain` is **measure-only** | **Enforcing** — M2 + M3 | §5.2 |
>
> The one thing D-6 did *not* make true is the sentence that prompted it. See §2.4a.

*Original measurement: 2026-08-15 against `origin/main` @ `c404a06` in an isolated
docs-only worktree. No dependency was updated, no pin moved, no allowlist created, and
`.github/workflows/ci.yml` was unchanged **by the PR that created this file**.*

Source row: the *"npm audit severity / exception policy"* row in
[`LEFTOVERS_BY_PRIORITY.md`](LEFTOVERS_BY_PRIORITY.md), which read *"**OWNER**, held
apart from P1.6 throughout and still undecided"* and is **now closed** by the
enforcement PR. (This citation said "line 808" until 2026-08-21; the row had already
moved to line 877 by then, which is why it is now named rather than numbered.) Owning
document:
[`P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md`](P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md) §6.
Design prompt: [`TESTING_STRATEGY_PLANNING.md`](TESTING_STRATEGY_PLANNING.md) §9.2
**F5-7** — *"the npm-audit flip mechanism is undesigned, and Dependabot changes the
picture weekly."*

---

## 0. The short version

Five high-severity advisories stand in the npm graph. **All five are transitive, none
is reachable by anything a user runs, and every one has an in-range, lockfile-only
fix that requires no direct-dependency bump and no semver-major move.**

That last clause is the finding that reframes the decision. F5-7 assumed the job's only
futures were "measure-only forever" or "block with four standing reds", so an allowlist
was the way out. It is no longer the only way out: **the standing reds can be driven to
zero by a lockfile-only remediation, after which the gate can be flipped with an empty
allowlist.** Building the allowlist first means designing an exception mechanism for
exceptions that need not exist.

Two measurements make the decision more urgent than the "measure-only, no user impact"
framing suggests:

1. **Dependabot alerts are disabled on this repository** (§2.4). The standing claim in
   [`.github/dependabot.yml`](../.github/dependabot.yml) — *"A security advisory against
   any of these still reaches us as a security update"* — does not hold today. The
   `js-supply-chain` job is the **only** JS vulnerability signal that exists, and it is
   measure-only, so today the repository has no enforced JS supply-chain signal at all.
   — **Both halves SUPERSEDED (§2.4a).** Alerts are on, and the job enforces. The
   `dependabot.yml` sentence is *still* wrong, for a different reason, and has been
   rewritten rather than re-dated.
2. **The documented baseline is stale.** §8.6 of `TESTING_STRATEGY_PLANNING.md` records
   *"4 high — `immutable`, `picomatch`, `postcss`, `fast-uri`"*. `immutable` is gone and
   `js-yaml` and `nanoid` are new. The set moved 4 → 3 → 5 in two weeks with no change
   to what this repository ships (§2.3). Any policy that names packages rather than
   advisory IDs is stale before it merges.

**Recommendation: R2 (§7) — remediate first, then flip with an empty allowlist.**
**Accepted by the owner on 2026-08-15, together with every other recommendation in §6.**

### 0.1 Findings of record

The four statements this packet exists to put on the record, each with the section
that carries its evidence:

1. **All nine advisory IDs are currently remediable inside the parent ranges already
   declared in the committed `package-lock.json`.** No direct-dependency bump, no
   `package.json` edit, and no semver-major move is required for any of them. Every
   fixed version was confirmed to exist on the registry *and* to satisfy every
   declaring parent's range. — **§3**, table.
   **Confirmed by execution:** M1 (#390) took all nine as in-range lockfile-only
   bumps, exactly as the table predicted.
2. **The accepted-debt allowlist is therefore empty.** There is no advisory in the
   graph today that lacks an in-range fix, and none of the five affected packages is
   frozen by a repository contract pin. An exception file written now would contain
   zero entries, and that is the correct content, not an omission. — **§3**, bucket
   table.
   **Confirmed by execution:** [`npm_audit_allowlist.json`](npm_audit_allowlist.json)
   shipped with `"allow": []`, and `tests/test_npm_audit_gate_contracts.py` pins that
   emptiness so an entry cannot appear without an owner decision.
3. **Dependabot alerts are disabled on this repository**, which invalidates the stated
   premise in [`.github/dependabot.yml`](../.github/dependabot.yml) — *"a security
   advisory against any of these still reaches us as a security update"* — and the
   identical premise in [`P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md`](P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md)
   §3.3. Both sentences describe a mechanism that is not running. Until D-6 is
   executed, `js-supply-chain` is the repository's only JS vulnerability signal, and
   it is measure-only. — **§2.4**, four read-only API probes.
   **SUPERSEDED as to the alerts, upheld as to the sentences.** Alerts were enabled
   under D-6 and `js-supply-chain` now enforces, so neither premise of the first
   clause still holds. But **both sentences remain wrong**, and enabling alerts did
   not fix them: a Dependabot *security update* is a pull request opened by
   **automated security fixes**, which ruling (a) leaves off on purpose. Advisories
   arrive as **alerts**, which a human acts on. Both sentences have been rewritten,
   not re-dated. — **§2.4a**.
4. **Advisory IDs are the policy key — not package names, and not counts.** The
   advisory set turned over inside a fortnight (`immutable` gone, `js-yaml` and
   `nanoid` new) while the count moved *non-monotonically*, 4 → 3 → 5, with no change
   to what this repository ships. A package-keyed or count-keyed policy is stale
   before it merges; a `GHSA-*` ID is immutable and is what the advisory database is
   keyed on. — **§2.3**, six sampled CI annotations.

---

## 1. What was measured, and how

| | |
|---|---|
| Base | `origin/main` @ `c404a06` |
| Worktree | `HT-v3-npm-audit-policy`, created `git worktree add … origin/main`, docs-only |
| Command | `npm audit --json` and `npm audit`, run against the committed `package-lock.json` |
| Local exit status | **1** (npm exits non-zero whenever the graph carries any advisory) |
| CI cross-check | run **31856035853**, `main`, 2026-08-15T01:15:59Z |
| Registry queries | `npm view <pkg> versions --json`, read-only, for the fix-availability table in §3 |

No `node_modules` was installed. `npm audit` resolves the committed lockfile against the
advisory database directly, which is the same thing CI does and the reason the CI job
carries no `npm ci` step.

**Local and CI agree exactly.** The CI annotation on the latest `main` run reads
`critical=0 high=5 moderate=0 low=0 info=0 total=5`, which is the local result. The
`::warning` annotation fires; the job conclusion is `success` on all eight most recent
runs, because the step ends in `exit 0` and the job carries `continue-on-error: true`.

---

## 2. Current exposure

### 2.1 Advisories by ID

npm's summary counts **5 vulnerabilities**; those roll up **9 distinct advisory IDs**.
The two numbers are not interchangeable, and §4.1 explains why the allowlist must be
keyed on the nine rather than the five.

| Advisory ID | Package (installed) | npm severity | CVSS | Direct? | Vulnerable range | Fixed in |
|---|---|---|---|---|---|---|
| `GHSA-v2hh-gcrm-f6hx` | `fast-uri` 3.1.3 | high | 7.5 | transitive | `>=3.0.0 <=3.1.3` | 3.1.4 |
| `GHSA-7p8r-x3mc-p8w7` | `fast-uri` 3.1.3 | high | 7.5 | transitive | `>=3.0.0 <3.1.5` | **3.1.5** |
| `GHSA-5p4m-2wfm-xmqj` | `js-yaml` 4.3.0 | high | 7.5 | transitive | `>=4.0.0 <4.3.1` | **4.3.1** |
| `GHSA-28wg-ghj8-5hjv` | `nanoid` 3.3.15 | high | 5.9 | transitive | `<3.3.16` | 3.3.16 |
| `GHSA-2v37-7h3g-55p8` | `nanoid` 3.3.15 | high | 5.9 | transitive | `<3.3.18` | **3.3.18** |
| `GHSA-3v7f-55p6-f55p` | `picomatch` 2.3.1 | moderate | 5.3 | transitive | `<2.3.2` | 2.3.2 |
| `GHSA-c2c7-rcm5-vvqj` | `picomatch` 2.3.1 | high | 7.5 | transitive | `<2.3.2` | **2.3.2** |
| `GHSA-fxqj-rqcc-2cmp` | `postcss` 8.5.16 | moderate | — | transitive | `<=8.5.22` | **8.5.23** |
| `GHSA-r28c-9q8g-f849` | `postcss` 8.5.16 | high | 7.5 | transitive | `<=8.5.17` | 8.5.18 |

Bold = the binding constraint for that package. **`isDirect` is `false` for all five
packages; there are zero direct-dependency advisories.**

Note the severity mismatch in the last four rows: npm reports `picomatch` and `postcss`
as **high** at the package level because the *worst* of their advisories is high, while
`GHSA-3v7f-55p6-f55p` and `GHSA-fxqj-rqcc-2cmp` are individually **moderate**. A policy
written as "fail on high" against the summary counter and an allowlist written against
per-advisory severity will disagree about these two IDs. §4.4 resolves it.

### 2.2 Reachability — production vs dev, and what "dev" means here

[`package.json`](../package.json) declares **no `dependencies` block at all**; every one
of the 12 declared packages is a `devDependency`. `npm audit --json` reports
`dependencies: {prod: 1, dev: 283, optional: 70, peer: 1, total: 283}` — the `prod: 1`
is the root project itself. This is the quantified basis for the `NEVER add --omit=dev`
comment at [`ci.yml:1206`](../.github/workflows/ci.yml#L1206).

The app is a Flask server that ships Python plus committed static assets. **Nothing
npm-installed is served to a browser or executed at runtime.** The only npm-derived
artifact that reaches a user is `static/css/bootstrap.custom.min.css`, built by `sass`
from `bootstrap` — and it is *committed*, so even that is produced at author time, not
install time or run time.

The reachability question that actually matters is therefore narrower than prod/dev:
*does the package sit on the CSS build path, or is it lint/test-only?*

| Package | Reached from | Build path? |
|---|---|---|
| `fast-uri` 3.1.3 | `stylelint → table → ajv` | No — lint only |
| `js-yaml` 4.3.0 | `stylelint → cosmiconfig` | No — lint config loading only |
| `nanoid` 3.3.15 | `stylelint → postcss`, `postcss-scss → postcss`, `vitest → vite → postcss` | No — lint and JS unit tests only |
| `picomatch` 2.3.1 | `stylelint → micromatch`, `stylelint → fast-glob → micromatch`, `sass → @parcel/watcher → micromatch` | **No** — see below |
| `postcss` 8.5.16 | `stylelint`, `postcss-scss`, `vitest → vite` | No — lint and JS unit tests only |

The `picomatch` row is the only one that touches `sass`, and it does so through
`@parcel/watcher`, which `sass` declares as an **`optionalDependencies`** entry. That
watcher backs `npm run watch:css`; `npm run build:css` — the script CI and the
`/build-css` skill invoke — does not use it. So `picomatch` is not on the build path
that produces the committed bundle either.

**Conclusion: all nine advisories are toolchain-only.** None is reachable by a user of
the application, and none can influence the bytes of the committed CSS bundle. That
justifies the *current* non-blocking posture — it does not justify leaving them
unremediated, given §3.

### 2.3 Churn — why a package-keyed policy cannot work

`::notice` annotations from `js-supply-chain` on `main`, sampled backwards:

| Date | Total | Severity line |
|---|---|---|
| 2026-08-01T18:23Z | 4 | `high=4` |
| 2026-08-02T15:22Z | **3** | `high=3` |
| 2026-08-08T13:03Z | 5 | `high=5` |
| 2026-08-12T21:59Z | 5 | `high=5` |
| 2026-08-14T00:28Z | 5 | `high=5` |
| 2026-08-15T01:15Z | 5 | `high=5` |

Against the §8.6 named set (`immutable`, `picomatch`, `postcss`, `fast-uri`): `immutable`
has **disappeared** from the graph, and `js-yaml` and `nanoid` have **appeared**. The
count went down before it went up, so a policy written as "tolerate 4" would have been
simultaneously too loose (it would have hidden the two new highs) and, on 2026-08-02, a
false description of the state.

Neither direction was caused by a change to this repository's product code. Advisories
appear when the database is updated against versions that were already installed, and
disappear when a routine Dependabot bump re-resolves an intermediate package. **A count
threshold and a package-name allowlist are both unusable. Advisory ID is the only stable
key.** This is F5-7's claim, now with the measurement behind it.

### 2.4 Dependabot alerts are disabled — the ignore-block premise does not hold

> **SUPERSEDED 2026-08-21 by §2.4a.** Alerts are now enabled under D-6. Everything
> below is the 2026-08-15 measurement, kept unedited because it is the evidence the
> ruling was made on.

Measured against the repository API:

| Probe | Result |
|---|---|
| `GET /repos/{owner}/{repo}/vulnerability-alerts` | **404** — not enabled |
| `GET /repos/{owner}/{repo}/automated-security-fixes` | `{"enabled": false, "paused": false}` |
| `GET /repos/{owner}/{repo}/dependabot/alerts?state=open` | **403** — *"Dependabot alerts are disabled for this repository"* |
| `gh pr list --state open` filtered to `dependabot/*` | **none open** |

[`.github/dependabot.yml`](../.github/dependabot.yml) states, as the justification for
listing only `version-update:` types in every `ignore` block:

> *Only `version-update:` types are listed, deliberately. A security advisory against
> any of these still reaches us as a security update; what is suppressed is the routine
> version bump.*

Dependabot **security** updates are gated on Dependabot alerts. With alerts disabled,
that sentence describes a mechanism that is not running. The same premise is written
into [`P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md`](P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md) §3.3.

Two consequences, both material to this decision:

- **`js-supply-chain` is the repository's sole JS vulnerability signal**, and it is
  measure-only. There is no second channel that would catch a critical advisory.
- **Dependabot churn is entirely `version-update` churn.** §4.5's design does not need
  to reason about security-update PRs unless the owner enables alerts (decision **D-6**).

This is reported as measured. Enabling alerts is a repository-settings change rather
than a code change, so it is carried as decision **D-6** — ruled *enable alerts, leave
automated fixes off* on 2026-08-15 (§6.1), and **not performed by this pull request or
by either of the two that follow it**.

### 2.4a D-6 executed — and the sentence it was meant to repair is still wrong

Re-probed 2026-08-21, against the same four endpoints, read-only:

| Probe | 2026-08-15 | 2026-08-21 |
|---|---|---|
| `GET /repos/{owner}/{repo}/vulnerability-alerts` | **404** — not enabled | **204** — enabled |
| `GET /repos/{owner}/{repo}/automated-security-fixes` | `{"enabled": false, "paused": false}` | `{"enabled": false, "paused": false}` — unchanged, per ruling (a) |
| `GET /repos/{owner}/{repo}/dependabot/alerts?state=open` | **403** — *"Dependabot alerts are disabled"* | **200** — `[]`, zero open |
| `GET /repos/{owner}/{repo}` → `security_and_analysis.dependabot_security_updates` | *(not probed)* | `disabled` — per ruling (a) |

That is **exactly ruling (a)**: alerts on, automated security fixes off.

**But D-6's own note is wrong for (a).** It reads: *"under (a)/(b) they become true
only from the date of the change."* Under **(b)** that holds. Under **(a)** those two
sentences never become true, at any date, because they do not describe alerts:

> *"A security advisory against any of these still reaches us as a **security
> update**."*

A Dependabot **security update** is a pull request opened by *automated security
fixes* — the setting ruling (a) deliberately leaves off, so that a lockfile change
stays a reviewed PR. What alerts restore is a **notification**, which a human then
acts on by opening the bump. Alert ≠ update, and enabling one does not produce the
other.

So the repair is a **rewording**, not a re-dating, and it is made in the enforcement
PR alongside the flip:

- [`.github/dependabot.yml`](../.github/dependabot.yml), the npm `ignore` preamble.
- [`P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md`](P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md) §3.3.

Both now say what is true under (a): the advisory surfaces as an **alert** and as a
red `js-supply-chain` run; what the `ignore` block suppresses is the routine version
bump, and nothing else.

The second consequence in §2.4 is also superseded, and in the direction the packet
argued for: `js-supply-chain` is no longer the *only* JS vulnerability signal, and it
is no longer measure-only. There are now two, one of which blocks.

---

## 3. Actionable vulnerabilities vs accepted toolchain debt

> **Snapshot, 2026-08-15. All nine advisories below are GONE** — M1 (#390) took every
> row of the fix table. Re-measured 2026-08-21 on `origin/main` and inside the
> enforcement worktree: `{"critical":0,"high":0,"moderate":0,"low":0,"info":0,"total":0}`
> over 283 dependencies (prod 1). The table stands as the prediction the remediation
> was authorized on, and it held: every fix was in range, none needed a
> direct-dependency bump, and `warningCount` did not move.

The separation F5-7 asks for turns out to be **degenerate in the useful direction**: on
today's graph, the "accepted debt" bucket is empty because everything in it is fixable
without an exception.

For each package, the fixed version was checked against the registry (it exists) and
against every parent's declared range in `package-lock.json` (it satisfies them):

| Package | Installed | Minimum fix | Parent's declared range | In range? | Direct dep changes? |
|---|---|---|---|---|---|
| `fast-uri` | 3.1.3 | 3.1.5 | `ajv` requires `^3.0.1` | ✅ | No |
| `js-yaml` | 4.3.0 | 4.3.1 | `cosmiconfig` requires `^4.1.0` | ✅ | No |
| `nanoid` | 3.3.15 | 3.3.18 | `postcss` requires `^3.3.12` | ✅ | No |
| `picomatch` | 2.3.1 | 2.3.2 | `micromatch` requires `^2.3.1` | ✅ | No |
| `postcss` | 8.5.16 | 8.5.23 | `stylelint` `^8.4.49`, `postcss-scss` peer `^8.4.29`, `vite` `^8.5.16` | ✅ | No |

`npm audit` reports `fixAvailable: true` (the boolean, not the breaking-change object)
for all five, and its own footer says `To address all issues, run: npm audit fix` —
without `--force`. Both are consistent with the table.

**So the buckets are:**

| Bucket | Members today |
|---|---|
| **Actionable — in-range lockfile-only fix** | All 9 advisories / all 5 packages |
| **Accepted toolchain debt — no fix, or fix blocked by a contract pin** | **Empty** |

None of the five packages is pinned by a repository contract. The frozen pins are
`stylelint` 16.11.0, `postcss-scss` 4.0.9 and `@playwright/test` 1.61.0 — all *direct*
devDependencies, none of them a vulnerable package. A transitive re-resolution leaves
their declared versions untouched.

### 3.1 The one real risk in remediating, and how to bound it

`stylelint`'s warning count is a committed measurement instrument:
[`tests/test_css_cascade_contracts.py`](../tests/test_css_cascade_contracts.py) pins
`warningCount 7202` at `sourceCommit 9ee7638` in
[`CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json`](CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json).
`postcss` and `js-yaml` are inside stylelint's own dependency tree — `postcss` is the
parser that produces those warnings. The whole reason `postcss-scss` was frozen is that
*"a changed rule or parser implementation moves that count on byte-identical CSS"*.

A transitive `postcss` 8.5.16 → 8.5.23 patch bump is far less likely to move the count
than a `postcss-scss` minor, but "far less likely" is not "cannot". **The remediation
lane must therefore run full `pytest` and treat any movement in `warningCount` as a stop
condition, not as a number to re-baseline.** That is the same rule
`P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md` §4.1 applies to the direct pin, and it is why §7
recommends the remediation as its own reviewable PR rather than folding it into the
policy change.

---

## 4. Proposed allowlist design

Presented as a design for owner approval. **This packet does not create the file.**

### 4.1 Key on advisory ID, not package, and not count

§2.1 shows 5 packages carrying 9 advisory IDs, and §2.3 shows the package set turning
over inside a fortnight while the count moved non-monotonically. A `GHSA-*` ID is
immutable, is what the advisory database is keyed on, and is what `via[].url` in
`npm audit --json` reports directly. It is the only stable key available.

Corollary: an entry that names a package without an ID is not expressible in this
format, deliberately. "We accept `postcss` problems" is not a decision anyone can
review; "we accept `GHSA-fxqj-rqcc-2cmp` until 2026-11-15 because X" is.

### 4.2 File

`docs/npm_audit_allowlist.json`, committed, alongside
`docs/ci_cd_phase3/pyright-baseline.json` and
`docs/CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json` as the third instance of the
"committed baseline the gate reads" pattern this repository already uses twice.

JSON over YAML for one reason: `PyYAML` is not in `requirements.txt`, which is why
`tests/test_release_workflow_contracts.py` parses workflows by indentation. A JSON file
can be validated by a pytest contract test with no new dependency.

```jsonc
{
  "schemaVersion": 1,
  "note": "Exceptions to the js-supply-chain gate. See docs/NPM_AUDIT_SEVERITY_POLICY_DECISION.md.",
  "allow": [
    {
      "id": "GHSA-xxxx-xxxx-xxxx",       // required, ^GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}$
      "package": "example",              // required; cross-checked against the audit, informational
      "severity": "high",                // required; the severity accepted at approval time
      "rationale": "…",                  // required, non-empty, >= 40 chars
      "owner": "avihay1989",             // required, non-empty
      "approvedOn": "2026-08-15",        // required, ISO-8601 date
      "expiresOn": "2026-11-15"          // required, ISO-8601 date, strictly after approvedOn
    }
  ]
}
```

Every field is required. There is no optional field and no default, because every
omission this format could tolerate is an omission that makes an entry unreviewable.

### 4.3 Fail-closed handling

The failure mode this design exists to prevent is the one this repository keeps
rediscovering — `--omit=dev` scoring "found 0 vulnerabilities", and the compiled-SCSS
drift gate that parsed cleanly while detecting nothing: a gate that scores green when
its own input is broken. Every abnormal condition below
therefore **fails the job**, and none of them is silently skipped:

| Condition | Behaviour |
|---|---|
| File absent | **Fail.** An empty allowlist is written as `"allow": []`, never as a missing file — "no exceptions" and "the file was deleted" must not look alike. |
| Malformed JSON | **Fail**, quoting the parse error. |
| `schemaVersion` unknown | **Fail.** A future entry shape must not be silently reinterpreted by an older reader. |
| Any required field missing, empty, or the wrong type | **Fail**, naming the offending entry index and field. |
| `id` not matching the `GHSA-` pattern | **Fail.** A CVE ID or a bare package name is a malformed entry, not a lenient one. |
| Duplicate `id` | **Fail.** Two entries for one advisory means two rationales, one of which is unread. |
| `expiresOn` on or before the run date | **Fail**, naming the ID and its expiry. An expired exception is *stricter* than no exception, which is what makes expiry a real deadline. |
| `expiresOn` more than `MAX_TTL` days after `approvedOn` | **Fail.** Without a ceiling, "expiry" is satisfied by the year 2099. `MAX_TTL` is decision **D-3**. |
| Entry whose `id` is **not** in the current audit | **Fail** as stale (see §4.6). |

Note the direction of every rule: a broken allowlist file makes the gate *harder* to
pass, never easier. A validator that skipped malformed entries would let a typo in an
`id` silently widen the gate — which is the same class of defect as
`--omit=dev` scoring a false green, and is the reason this table has no "warn" row.

### 4.4 Severity comparison is per-advisory, not per-package

§2.1 records the mismatch: `picomatch` and `postcss` are *package*-level `high` while
carrying individually-`moderate` advisories. The gate must read severity from
`vulnerabilities[pkg].via[].severity` — the per-advisory value — and never from
`vulnerabilities[pkg].severity`, or `GHSA-3v7f-55p6-f55p` (moderate) inherits `high`
from its sibling and a "fail on high only" policy blocks on a moderate advisory it never
meant to cover. The summary counters in `metadata.vulnerabilities` are for the job
summary only and must not drive the exit status.

### 4.5 CI behaviour, by event

Assumes a new `scripts/npm_audit_gate.mjs` reading both the audit JSON and the
allowlist. The current inline `node -e` block is already at the limit of what belongs in
YAML, and a script file is testable from pytest the way `scripts/release_gate.py` is.

| Event | Behaviour | Why |
|---|---|---|
| **New advisory at or above the severity floor, not allowlisted** | **Fail.** Message names the ID, package, path to a direct dependency, and whether a fix is in range. | The gate's entire purpose. |
| **New advisory below the floor** | Pass; report in the job summary. | D-1 sets the floor. |
| **Advisory present and allowlisted, unexpired** | Pass; list it in the summary with owner and days remaining. | Visible, dated, attributable. |
| **Advisory disappears from the audit** but is still allowlisted | **Fail** as a stale entry, with the remedy in the message: delete the entry. | §2.3: `immutable` vanished. A stale entry is a live exception nobody is watching, and if the advisory returns it is pre-approved by an expired decision. Failing on removal is the only thing that keeps the file honest. |
| **Severity of an allowlisted advisory rises above its recorded `severity`** | **Fail.** | The approval was given for the severity written in the entry. A `moderate` accepted in August must not silently cover a re-scored `critical` in November. |
| **Severity falls** | Pass. | Strictly less exposure than approved. |
| **Registry or advisory API unavailable** (`npm audit` exits non-zero **without** parseable JSON, or writes to stderr and produces no report) | **Fail the job, with a message distinguishing "audit could not run" from "advisories found".** | Decision **D-4**. Treating an unreachable registry as clean is a false green on the one signal §2.4 shows is the only one. |
| **`npm audit` exit code 1 with a valid report** | Not itself a failure. Exit status is computed from the report against the allowlist. | npm exits 1 for *any* advisory including allowlisted ones; using its exit code directly makes the allowlist inert. |
| **Dependabot `version-update` PR churn** | Same rules; no special case. | The gate reads the branch's own lockfile. A bump that re-resolves `postcss` clears its advisories on that branch and the gate goes green there before it goes green on `main`. |
| **A Dependabot PR that introduces a new advisory** | **Fail on that PR.** | This is the case the gate is most valuable for and needs no exception. |
| **Dependabot security-update PR** | Same rules. | Still not reachable: alerts are on since D-6, but *automated security fixes* — the setting that opens a security-update PR — stay off by ruling (a). See §2.4a. |

### 4.6 The stale-entry rule is the one to argue about

Failing when an allowlisted advisory *disappears* is unusual and will be the friction
point in daily use: a Dependabot bump that fixes `postcss` turns the gate red until
someone deletes the entry, which reads as "the gate broke when the problem was fixed".

It is proposed anyway, for the reason §2.3 measures: entries that outlive their
advisories are exactly how an allowlist rots into a permanent blanket. The pyright
baseline has the same property and the repository already accepts it there. If the
owner finds the friction unacceptable, the alternative is to warn rather than fail on
stale entries — but that is a deliberate loosening and belongs in **D-5**, not in an
implementer's judgement call.

---

## 5. Migration, rollback, and local reproduction

### 5.1 Local reproduction

Run from the repository root; no `node_modules` needed and none is written:

```bash
mkdir -p artifacts/npm-audit
npm audit --json > artifacts/npm-audit/npm-audit.json 2>artifacts/npm-audit/npm-audit.err
npm audit            # human-readable; exits 1 whenever any advisory exists
```

Advisory IDs, which the human-readable output gives only as URLs:

```bash
node -e "const r=JSON.parse(require('fs').readFileSync('artifacts/npm-audit/npm-audit.json','utf8'));
for(const [p,v] of Object.entries(r.vulnerabilities))
  for(const a of v.via) if(typeof a==='object')
    console.log(a.url.split('/').pop(), p, a.severity, a.range);"
```

Reachability for one package, root-ward through the committed lockfile — the query
behind §2.2, and the one to re-run before writing any rationale:

```bash
npm ls postcss --all
```

CI's own verdict for a commit, without re-running anything:

```bash
gh run list --workflow=ci.yml --branch main --limit 1 --json databaseId --jq '.[].databaseId'
gh api repos/{owner}/{repo}/actions/runs/<RUN_ID>/jobs \
  --jq '.jobs[] | select(.name|test("JS Supply Chain")) | .id'
gh api repos/{owner}/{repo}/check-runs/<JOB_ID>/annotations \
  --jq '.[] | "\(.annotation_level): \(.message)"'
```

`artifacts/` is gitignored, per ADR-002.

### 5.2 Migration — three levers, deliberately separable

Flipping this gate is not one change. Conflating the three is how a required context
gets orphaned.

| Lever | Edit | Effect | Renames a context? | State |
|---|---|---|---|---|
| **L1** | Drop the step's trailing `exit 0`; the step now ends in the gate's own status — [`ci.yml:1271-1275`](../.github/workflows/ci.yml#L1271-L1275) | The **step** fails | No | **Taken** |
| **L2** | Remove `continue-on-error: true` from the job — the key is simply absent at [`ci.yml:1238-1241`](../.github/workflows/ci.yml#L1238-L1241) | The **job** reports red instead of neutral-success | No | **Taken** |
| **L3** | Add `JS Supply Chain (npm audit, non-required)` to branch protection | A red job **blocks merge** | No — but see below | **Not taken** (step M4) |

*Two notes on those citations. The pre-flip line numbers this table used to carry —
`ci.yml:1274` for L1 and `ci.yml:1225` for L2 — were **both off by two**; the lines
were 1276 and 1227. And L1's edit is not the `exit 0` → `exit $STATUS` the row
originally described: the inline `node -e` block that computed `STATUS` was replaced
wholesale by [`scripts/npm_audit_gate.mjs`](../scripts/npm_audit_gate.mjs), so the
step's status is now the script's exit code with no shell arithmetic in between. The
effect is the one L1 specified.*

L1 and L2 are safe in either order and neither touches a check name. L3 is the one with
teeth, and it drags two source files with it:

- [`scripts/release_gate.py:39-58`](../scripts/release_gate.py#L39-L58) — `REQUIRED_CONTEXTS`
  and the derived `EXPECTED_CONTEXTS`. The release gate's *"main is green"* means these
  twelve contexts; a thirteenth required context that the gate does not wait for is a
  gate that certifies less than branch protection enforces.
- [`tests/test_release_workflow_contracts.py:40-46, 157-159`](../tests/test_release_workflow_contracts.py#L40-L46) —
  `UNEXPECTED_CI_JOB_NAMES` asserts both `name in names` (the job exists in `ci.yml`
  under exactly that string) **and** `name not in EXPECTED_CONTEXTS`. Promoting the job
  without editing this tuple reds the test; editing the tuple without editing
  `release_gate.py` reds it the other way. They move together or not at all.

**The job name does not change under any of the three levers.** The `(non-required)`
suffix stays even if L3 is taken, under the rule in
[`QUALITY_GATE.md`](ai_workflow/QUALITY_GATE.md) §"CI job naming — the `(non-required)`
suffix is not a status claim": two currently-required contexts already carry a false
`(non-required)` suffix on purpose, because renaming a protected context orphans it and
every PR then waits forever on a check that will never report. The `pyright` job is the
documented precedent — *"Correct the understanding here; do not correct the label."*

Suggested sequencing:

| Step | Change | Gate |
|---|---|---|
| **M0** | *(this packet)* — decisions recorded | Docs-only; no gates |
| **M1** | Remediation: `package-lock.json` only, `npm audit fix` reviewed hunk by hunk, no `package.json` edit | Full `pytest` + `/build-css` + byte-compare the bundle + `npm run test:js`. **Stop if `warningCount` moves** (§3.1) |
| **M2** | Add `docs/npm_audit_allowlist.json` with `"allow": []`, `scripts/npm_audit_gate.mjs`, and its pytest contract test | Full `pytest`; regenerate `docs/test_inventory/` (a new test file moves node counts) |
| **M3** | L1 + L2 in `ci.yml` | Full `pytest` — seven test files parse `ci.yml`; `code-reviewer` + `architecture-reviewer` per the CI-workflows row |
| **M4** | L3, with `release_gate.py` and `test_release_workflow_contracts.py` in the same PR | Full `pytest`; verify the context appears on a real PR **before** adding it to protection |

> **Packaging note.** This table read *"one reviewable PR each"* until 2026-08-21,
> which contradicted §6.1's "Lands in" row and §8, both of which say **"the enforcement
> PR — §5.2 M2 + M3"**, singular. Nothing outside this file broke the tie. The owner
> ruled for the combined reading on 2026-08-21: **M2 and M3 ship as one PR**, and the
> per-row phrasing above is superseded. M1 and M4 remain separate — M1 because §7 wants
> the `warningCount` risk isolated, M4 because it is the only lever that touches branch
> protection. The gates in the M2 and M3 rows are cumulative, not alternatives.

M2's validator must be mutation-tested in **both** directions before it is trusted:
corrupt the JSON, drop a required field, forge an expired entry, forge a stale entry, and
confirm each reds — then confirm a clean file greens. A validator that only ever sees
valid input is indistinguishable from one that parses nothing, which is precisely the
`test_compiled_scss_drift_gate` failure mode.

**Done, and recorded.** [`tests/test_npm_audit_gate_contracts.py`](../tests/test_npm_audit_gate_contracts.py)
runs the real script over both directions — every rule in §4.3 and §4.5 red-cased, and
the nine cases that must **not** fail green-cased, including the four that are one
flipped comparison away from a red one: an advisory below the floor, a severity that
*fell* rather than rose, an entry expiring tomorrow, and npm's own exit code 1 over a
report that parses. The red set is generated over `REQUIRED_FIELDS` read out of the
script rather than hand-listed, so a field added to the format cannot outrun its test.
The suite was itself checked by mutating the script ten ways — including reinstating the
`catch { console.log('::warning'); process.exit(0); }` on unparseable audit JSON that
the old inline block carried, which is the third false-green path §5.2 did not name —
and all ten red it.

### 5.3 Rollback

| From | Revert | Blast radius |
|---|---|---|
| **M4** | Remove the context from branch protection **first**, then revert the commit | Leaving protection pointing at a removed context blocks every PR. Protection first, always. |
| **M3** | Restore `continue-on-error: true` on the job **and** a trailing `exit 0` on the step | Job returns to measure-only; no context changes. Both, or the gate stays half-open — and `tests/test_npm_audit_gate_contracts.py` asserts both are absent, so a partial rollback reds pytest rather than passing quietly |
| **M2** | Revert the commit; regenerate `docs/test_inventory/` | Removing a test file moves node counts and reds `Test Inventory Drift` if not regenerated. M2 and M3 shipped as one PR, so this row and the one above are one revert |
| **M1** | `git revert` the lockfile commit | Restores byte-identical `package-lock.json`; re-run `npm ci` locally. Note the worktree hazard: a lockfile change on `main` means every worktree junctioned to `main`'s `node_modules` is on the wrong install state — `npm ci` in the main checkout is the repair |

M1 through M4 are independent reverts in any order, which is the point of splitting
them. M1 alone leaves a strictly better graph with no policy attached; M3 alone leaves a
gate enforcing an empty allowlist.

### 5.4 Execution ledger

| Step | Landed as | State |
|---|---|---|
| **M0** | #386 (`81df507`) | Merged — this document |
| **M1** | #390 (`8baddd2`) | Merged — nine advisories cleared with in-range lockfile-only bumps; `warningCount` did not move |
| **D-6** | *(a repository setting, no PR)* | Setting done — alerts on, automated fixes off (§2.4a). Its **prose** half landed with M2 + M3 |
| **M2 + M3** | the enforcement PR | Allowlist, gate script, contract test, L1 + L2 — one PR, per the 2026-08-21 packaging ruling |
| **M4** | — | **Not done, and not authorized by any ruling on this page.** D-1 – D-5 authorize M2 + M3; lever L3 needs its own decision, and §5.2's precondition first: see the context report on a real PR *before* adding it to protection |

---

## 6. Owner decisions required

Nothing in §4 or §5 may be built until these are answered. **All seven were answered on
2026-08-15 — the ruling is in §6.1.** The table below is retained as written, with its
recommendation column intact, so the ruling can be read against what was actually put
to the owner rather than against a summary of it.

| # | Decision | Options | Recommendation |
|---|---|---|---|
| **D-1** | **Severity floor** — at what per-advisory severity does an un-allowlisted advisory fail the job? | (a) `critical` only; (b) **`high` and above**; (c) `moderate` and above; (d) any | **(b)**. `critical` alone would not fail on any of today's nine. `moderate` would pull in the two `picomatch`/`postcss` moderates, which are real but low-value at this reachability. |
| **D-2** | **Does dev-only reachability get a standing carve-out**, or does the gate apply to the whole graph with per-advisory exceptions? | (a) **whole graph, exceptions per ID**; (b) standing "dev-only is exempt" rule | **(a)**. (b) is `--omit=dev` re-expressed as policy: with zero runtime dependencies it exempts 283 of 283 packages and the gate can never fire. |
| **D-3** | **`MAX_TTL`** — the ceiling on `expiresOn − approvedOn`. | 90 / 180 / 365 days | **90 days.** Long enough to schedule a real remediation, short enough that a forgotten entry surfaces within a quarter. |
| **D-4** | **Registry/API unavailable** — fail the job, or pass with a warning? | (a) **fail**; (b) warn and pass | **(a)**, fail-closed. §2.4: this is the only JS vulnerability signal. A flake costs a re-run; a false green costs the signal. |
| **D-5** | **Stale-entry handling** — allowlisted advisory no longer present in the audit. | (a) **fail**, entry must be deleted; (b) warn and pass | **(a)**, with §4.6's friction acknowledged. Reverse it deliberately if the friction proves real, not by default. |
| **D-6** | **Enable Dependabot alerts and automated security fixes?** (repository settings; outside this packet) | (a) **enable alerts, leave automated fixes off**; (b) enable both; (c) leave both off | **(a)**. It restores the premise the `dependabot.yml` ignore blocks are written on and gives a second signal. Automated fixes off, so a lockfile change stays a reviewed PR. Note: whichever is chosen, the `dependabot.yml` comment and `P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md` §3.3 need correcting — under (c) they are simply wrong, and under (a)/(b) they become true only from the date of the change. |
| **D-7** | **Sequencing** — remediate first (R2), or allowlist first (R1)? | See §7 | **R2.** |

### 6.1 Owner ruling, 2026-08-15

**Every recommendation above was accepted as written.** Restated so no later reader has
to reconstruct it from a column heading:

| # | Ruling |
|---|---|
| **D-1** | Severity floor is **`high` and above**, read per-advisory. |
| **D-2** | The gate applies to the **whole graph**; exceptions are per advisory ID. There is no standing dev-only carve-out. |
| **D-3** | `MAX_TTL` is **90 days**. |
| **D-4** | An unavailable registry or unparseable audit **fails the job**. Fail-closed. |
| **D-5** | A stale allowlist entry — one whose advisory is no longer in the audit — **fails the job**; the entry must be deleted. §4.6's friction is accepted knowingly. |
| **D-6** | **Enable Dependabot alerts; leave automated security fixes off.** |
| **D-7** | **R2 — remediate first, then enforce.** |

**None of these was executed by the pull request that recorded them** (#386), which
stayed documentation-only. What each ruling authorizes, where it lands, and where it
has since landed:

| Ruling | Lands in | Landed |
|---|---|---|
| D-7 | The remediation PR — lockfile-only, §5.2 **M1** | #390 |
| D-1 – D-5 | The enforcement PR — §5.2 **M2 + M3**, allowlist committed with `"allow": []` | the enforcement PR (§5.4) |
| D-6 | A **repository-settings** change, not a code change. It is not performed by any of these pull requests, and it does not gate them. The two stale sentences named in §0.1 finding 3 stay wrong until it is done, and correcting them is part of the same follow-up. | Setting done; sentences reworded with M2 + M3 — but **not** because the setting made them true. See §2.4a. |

Note that "the enforcement PR" is written **singular** here and in §8, while §5.2's
sequencing table said *"one reviewable PR each"*. That contradiction was ruled on
2026-08-21 in favour of the singular reading; §5.2 carries the note.

---

## 7. Recommendation

**R2 — remediate first, then flip the gate with an empty allowlist.** *(Accepted, D-7.)*

| | R1: allowlist the five, then flip | **R2: remediate, then flip empty** | R3: stay measure-only |
|---|---|---|---|
| Standing exceptions on day one | 9 entries | **0** | n/a |
| Direct-dependency change | none | none | none |
| Frozen pins touched | none | none | none |
| Risk carried | 9 live advisories, dated | `warningCount` movement (§3.1), caught by full pytest | 9 live advisories, undated |
| First unrelated advisory | fails correctly | fails correctly | never fails |

R2's argument in one line: **§3 shows the accepted-debt bucket is empty**, so R1 would
be building an exception mechanism to hold exceptions that need not exist — nine entries
whose rationale would have to read *"a fix is available and in range, but we chose not
to take it"*, which is not a rationale anyone would approve at review.

R2's cost is real and bounded: the `postcss` re-resolution could move the stylelint
warning count (§3.1). That risk is detected by the full pytest run M1 already requires,
and its handling is prescribed — **stop, do not re-baseline**. If the count does move,
M1 is abandoned and the decision falls back to R1 for `postcss`/`js-yaml` only, with the
other three still remediated.

The allowlist should still be **designed and built** (M2), because R2's steady state is
"gate on, file empty" and the first genuinely unfixable advisory will arrive with no
warning. Building it while the file can honestly be empty is easier than building it
under pressure with a red gate.

R3 is not recommended, and §2.4 is why: with Dependabot alerts disabled, measure-only is
not "we watch but do not block" — it is **no enforced JS supply-chain signal at all**,
which is the state B10 was opened to close.

*(Both premises of that paragraph have since changed — alerts are on and the job
enforces, §2.4a — which is R2 having been carried out rather than R3's case improving.
It is left as written because it is the argument the ruling was made on.)*

---

## 8. What this packet did not do

Recorded explicitly so a later reader does not mistake absence for oversight. **"This
packet" means the docs-only PR that created this file (#386)** — every bullet below is
a statement about that commit, not about the repository today. §5.4 is where to look
for what has since been done.

- No `npm audit fix`, not even `--dry-run`. `package-lock.json` and `package.json` are
  byte-unchanged; the §3 fix table was derived from registry version lists and the
  committed lockfile's declared ranges, not from npm's resolver.
- No dependency added, removed, or re-pinned.
- No `.github/workflows/ci.yml` edit. `exit 0` and `continue-on-error: true` stand.
- No allowlist file created. §4 is a design, approved under D-1 – D-5 and built in the
  enforcement PR, not here.
- No check context added, removed, renamed, or weakened. The `js-supply-chain` job name
  is byte-identical to the string pinned at
  `tests/test_release_workflow_contracts.py:44`.
- No repository setting changed, **D-6 included**; the §2.4 probes are read-only `GET`s.
  The ruling authorizes enabling Dependabot alerts. This PR does not perform it.
- No `dependabot.yml` edit, including the §2.4 comment that measurement shows to be
  currently false — correcting it is part of **D-6**, not of this packet.
- `docs/LEFTOVERS_BY_PRIORITY.md`'s npm-audit-policy row is **not** updated. The §6 decisions are now
  made, but the row tracks the *policy*, and the policy is not in force until the
  enforcement PR lands. Closing that row belongs to the PR that flips the gate, so that
  the row and the gate become true on the same commit. — **Done there.**

---

*Created 2026-08-15 against `origin/main` @ `c404a06`. Advisory data is a snapshot —
§2.3 shows it moving within days. Re-run §5.1 before acting on any specific ID.*
