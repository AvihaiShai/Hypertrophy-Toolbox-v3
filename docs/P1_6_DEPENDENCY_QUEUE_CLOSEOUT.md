# P1.6 — dependency-queue closeout

*Status: **DECIDED AND EXECUTED**. Owner authorized A1 (defer Playwright) and B1
(freeze stylelint) on 2026-08-03. Verified against `origin/main` @ `4e9b7d0`.*

Source row: [`LEFTOVERS_BY_PRIORITY.md`](LEFTOVERS_BY_PRIORITY.md) P1.6.

---

## 1. Outcome

`gh pr list --state open` contains **zero** red dependency pull requests. Both
remaining reds were disposed of deliberately, and no contract test was weakened
to get there.

| | Decision | Action |
|---|---|---|
| **Lane A** — #288, `@playwright/test` 1.62.1 | **A1 — defer** | Closed. Both halves of the lockstep ignored in [`.github/dependabot.yml`](../.github/dependabot.yml); upgrade re-enabled by the condition in §3.4 |
| **Lane B** — #287, `stylelint` 16.26.1 | **B1 — freeze at 16.11.0** | Closed. Ignore widened from majors to every version-update type, and extended to `postcss-scss` |

What was **not** done, on purpose: no Playwright bump, no visual-baseline
regeneration, no change to `tests/test_playwright_version_contract.py`, no
rewrite of `CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json`, and no relaxation of
`tests/test_css_cascade_contracts.py`.

### The four v23 lanes are discharged

| Lane | v23 state | Now |
|---|---|---|
| (a) merge #245 | green, independent | **Superseded** — #245 CLOSED; #283 merged 2026-08-02 as a two-ecosystem 1.61.0 bump *plus* the lockstep contract |
| (b) land #275, then #250 | both open | **#275 merged** 2026-08-02T14:17Z; **#250 merged** 2026-08-02T14:40Z |
| (c) #274 blocked twice over | draft, double-blocked | **#274 merged** 2026-08-02T13:44Z |
| (d) Actions v7 / TypeScript 7 | discharged | unchanged; `Type Check (tsc blocking …)` green on `main` |

P1.6 as scoped — *triage the dependency queue* — is closed. The deferred
Playwright upgrade in §3.4 is newly-tracked debt with a named unblock condition,
not P1.6 residue.

---

## 2. Evidence

Both PRs opened 2026-08-03T00:26Z, red on the **required** `Run Tests` context
and green on all 16 others. Failing assertions read from the CI logs (runs
`30774473693` and `30774468573`), not inferred:

| PR | Bump | Failing assertion |
|---|---|---|
| **#288** | `@playwright/test` 1.61.0 → **1.62.1** | `test_python_and_npm_playwright_pins_are_exact_and_identical` — *"Playwright is skewed across ecosystems: requirements.txt pins 1.61.0, package.json pins 1.62.1."* |
| **#287** | `stylelint` 16.11.0 → **16.26.1** | `test_stylelint_is_pinned_measure_only_with_committed_baseline` — `assert '16.26.1' == '16.11.0'` ([`test_css_cascade_contracts.py:166`](../tests/test_css_cascade_contracts.py#L166)) |

Neither red was a defect. In both cases the contract test did exactly the job it
was written for, which is why the disposition is a config rule rather than a fix.

---

## 3. Lane A — Playwright, deferred (A1)

### 3.1 Why the bump is red

[`test_playwright_version_contract.py`](../tests/test_playwright_version_contract.py)
(added by #283, blindspot B9) requires `requirements.txt` and `package.json` to
pin the *same literal* Playwright version, because each release ships its own
browser build. Dependabot raises pip and npm as separate pull requests and
**cannot group across ecosystems**, so every future Playwright bump arrives
one-sided and red. That is a permanent property of the setup, not a one-off.

### 3.2 Why deferring is the right call, not just the cheap one

| | Playwright 1.61.0 (current) | Playwright 1.62.1 (#288) |
|---|---|---|
| Chromium revision | 1223 | 1234 |
| Chromium version | **148.0.7778.96** | **151.0.7922.34** |

*(1.61.0 read from `node_modules/playwright-core/browsers.json`; 1.62.1 read from
the `v1.62.1` tag of `microsoft/playwright`.)*

Every committed visual baseline was rendered by Chromium 148. Three Chromium
majors will move text metrics and antialiasing.

The decisive part is that **no required check would report it**. The visual specs
run only in [`deep-gate.yml`](../.github/workflows/deep-gate.yml)'s `visual-linux`
job, which is `if: ${{ inputs.run_visual }}` — manual, opt-in, and explicitly
never a required PR check — and `ci.yml` excludes both specs. Merging #288 would
turn every baseline stale silently, and the next deep-gate run would inherit an
unexplained wall of red.

There is also a live collision: **#281** (`recovery/linux-visual-baselines`) is
open with all checks green, carrying Linux baselines regenerated at `4de6b62` and
waiting on owner review of 84 PNGs. **#286** (visual determinism, draft) failed
its Gate 2 at 78/86. A Playwright bump merged now invalidates the exact artifact
#281 is asking the owner to review.

### 3.3 What was configured

Both halves of the lockstep are ignored, because ignoring only npm would produce
the identical one-sided red from the pip side:

- **npm** — `@playwright/test`, all three `version-update:semver-*` types.
- **pip** — `playwright`, all three `version-update:semver-*` types.

Only `version-update:` types are listed; what is suppressed is the routine bump.
A security advisory against Playwright still surfaces — as a **Dependabot alert**
and as a red `js-supply-chain` run — but **not** as a Dependabot *security
update*. This paragraph claimed it did until 2026-08-21, and that was wrong on
both counts at the time of writing: Dependabot alerts were disabled outright
(measured in [`NPM_AUDIT_SEVERITY_POLICY_DECISION.md`](NPM_AUDIT_SEVERITY_POLICY_DECISION.md)
§2.4), and security updates are opened by "automated security fixes", which
decision **D-6** deliberately leaves off so a lockfile change stays a reviewed
pull request. Alerts are now on per that ruling; acting on one means a human
opens the bump.

### 3.4 Unblock condition

> Remove the `@playwright/test` entry from the npm `ignore` block **and** the
> `playwright` entry from the pip `ignore` block once **both** hold:
>
> 1. **#281 is merged** — the Linux baselines are owner-reviewed and current.
> 2. **#286's determinism work is resolved** — its Gate 2 passes or the arc is
>    explicitly terminated.
>
> Then bump both ecosystems in a **single branch**, and regenerate **both**
> platforms' baselines within the same arc. Do not split the bump and the
> regeneration across PRs — between them, the visual gate certifies nothing.

This condition is duplicated as a comment on the ignore rule itself, so the next
reader of `dependabot.yml` does not have to find this file first.

---

## 4. Lane B — stylelint, frozen at 16.11.0 (B1)

### 4.1 Why the pin is a contract

[`test_css_cascade_contracts.py:155-173`](../tests/test_css_cascade_contracts.py#L155-L173)
pins the entire measure-only design: `stylelint == "16.11.0"`,
`postcss-scss == "4.0.9"`, the job name, `continue-on-error: true`, and three
counters in [`CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json`](CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json)
(`sourceCommit 9ee7638`, `warningCount 7202`, `parseErrorCount 0`). The pin is
part of the baseline, not a preference — a changed rule implementation moves the
count on byte-identical CSS, at which point the number stops measuring CSS debt
and starts measuring tool churn.

### 4.2 The old rule never matched the contract it protected

[`.github/dependabot.yml`](../.github/dependabot.yml) ignored stylelint
`version-update:semver-major` only — the #268/#252 precedent, written for the
16 → 17 case. But the test asserts an **exact** version, so a *minor* (#287) reds
it just as hard, and a patch would too. The ignore was narrower than the contract
from the day it was written; #287 is simply the first bump to expose the gap.

### 4.3 The postcss-scss check, and what was deliberately left alone

`postcss-scss` **does** need the same treatment. The same test pins it exactly at
4.0.9, and the baseline JSON records it under `tools.postcssScss` — it is the
parser that produces the warning counts, so it is part of the same instrument.
It had no ignore rule at all. Added.

Two other exactly-pinned packages were checked and **deliberately not ignored**:

- **`bootstrap` (5.3.8)** — has a version contract
  ([`test_bootstrap_version_contract.py`](../tests/test_bootstrap_version_contract.py)),
  but a *relative* one: it reads whatever `package.json` declares and asserts
  `base.html`'s two CDN URLs match. A bump reds it, and the fix is a two-line
  template edit — not a re-baselining packet. The repository's contract does not
  support freezing it, and #274 landed 5.3.8 on 2026-08-02 precisely so this
  package could move.
- **`sass` (1.102.0)** — no contract test pins it; #261 bumped and merged it
  normally.

This is the line the baseline contract draws: freeze what is a *measurement
instrument*, not everything that happens to be pinned.

---

## 5. Verification run

Both lanes are config-and-docs only. No test file, workflow, or lockfile changed,
so the gate is the contract tests plus YAML validity:

```bash
.venv/Scripts/python.exe -m pytest \
  tests/test_playwright_version_contract.py \
  tests/test_css_cascade_contracts.py \
  tests/test_bootstrap_version_contract.py \
  tests/test_node_version_contract.py -q
# 35 passed in 0.23s
```

`dependabot.yml` was parsed and schema-checked: `version: 2`, every `ignore`
entry uses only `dependency-name` / `update-types`, and every `update-types`
value is one of the three `version-update:semver-*` literals.

`Test Inventory Drift` is unaffected — no test was added or removed.

---

## 6. Remaining P1.6 work

**None.** The queue is drained and both new reds are disposed of.

Carried forward as separately-tracked debt, not P1.6 residue:

| Item | Where it lives |
|---|---|
| The Playwright 1.62.1 upgrade | §3.4 above, mirrored in the `dependabot.yml` comment. Blocked on #281 + #286. |
| The `npm audit` severity / exception policy | Still an open, separate decision — the P1.6 row always held it apart. |

---

*Created 2026-08-03 against `main` @ `4e9b7d0`; updated the same day to record the
owner's A1/B1 authorization and the executed configuration.*
