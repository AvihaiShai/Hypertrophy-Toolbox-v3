# Gate 0: scheduled deep-gate Linux visual failure, 2026-08-31

## Verdict

**Bounded Gate 0: sufficient evidence exists for one diagnostic Gate-1 experiment.**
This packet does not authorize a fix. It records the failure boundary, names one
testable hypothesis, and preserves the release and visual-contract decisions in
[ADR-007](../DECISIONS.md#adr-007-release-tags-are-exact-vapp_version-tags-and-the-release-gate-reuses-ci-rather-than-re-running-it)
and
[ADR-011](../DECISIONS.md#adr-011-the-terminal-visual-contract-is-81-byte-gated-captures-plus-five-semantic-exemptions).

Evidence was re-read live from GitHub Actions on 2026-08-31. The deep gate was
not rerun for this packet.

## Primary observations

| Observation | Exact result |
|---|---|
| Scheduled run | [`33379302035`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33379302035), event `schedule`, attempt 1, head `e093081626abba66df883f61831bf0d3a3d0e1fb`, overall `failure` |
| Job boundary | Six jobs succeeded. Only `Visual regression (Linux baselines)`, job [`99447749767`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33379302035/job/99447749767), failed. |
| Visual test count | `Running 100 tests using 1 worker`; **65 failed, 17 did not run, 18 passed**. |
| Retry behavior | Each of the **65 unique final failing snapshots** produced failure records on the initial attempt, retry `#1`, and retry `#2`: **195 screenshot-failure records = 65 x 3**. None of those 65 recovered on retry. |
| Compare-only guard | `Assert compare mode wrote no baseline` succeeded after the test failure. No baseline was written. |
| Prior scheduled comparison | [`32688747703`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32688747703), event `schedule`, attempt 1, head `31659a59ccc82391287d98f2e9d899a048d20b2c`, concluded `success`, but was **not clean**: the visual job ran 100 tests and ended **99 passed, 1 flaky**. `plan-desktop-light-simple.png` failed its first comparison by 11,392 pixels (ratio 0.02), passed on retry `#1`, and made the job green. |
| Earlier confirming failure | Manual deep-gate run [`33336856336`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33336856336) at `b36ea9e1a3d7e0e37918e9db4198cb4bf7e0ecf8` already had the same terminal summary: **65 failed, 17 did not run, 18 passed**. |

The 65 final failures span broad page families rather than one isolated capture:
backup, body composition, fatigue, progression, session summary, user profile,
volume splitter, weekly summary, welcome, workout log, and workout plan.
That breadth and survival through both configured retries distinguish this event
from the single flaky comparison in the 2026-08-24 scheduled run.

## What the evidence does and does not distinguish

### Intended CSS/source drift

This is **present and proven**, but no individual commit is proved causal. Between
`31659a5` and `e093081`, rendering inputs changed. In particular, #464
(`e9eff89`) intentionally changed shared CSS tokens and consumers, theme
initialization, `base.html`, and dark-mode behavior, and updated approved Win32
baselines. Earlier in the interval, `b733c14` changed Sass from 1.102.0 to
1.103.1, and other commits changed two summary templates. These are candidates,
not a causal ranking.

### Missing Linux baseline synchronization

This is **present and proven**. The Git tree for
`e2e/__screenshots__/linux` is exactly
`206f30d8b7e90777bcf157217d04839045528000` at `31659a5`, `b36ea9`, and
`e093081`, while the `static/css` tree changes from
`7de5ca925d698c4937ffe2e4a8eae2af419f2c36` at `31659a5` to
`ff3309f2671d9627a02aade1afef87803090fa2f` at both later heads. #464's own
merged description explicitly states that no Linux baseline was touched and
that Linux work remained outstanding. This establishes an unsynchronized
source/baseline state; it does not by itself prove which source commit produced
each pixel difference.

### Runner and browser drift

Browser drift is **not observed** in the two scheduled runs: both used Node
24.19.0, npm 11.17.0, Playwright 1.61.0, and Chrome Headless Shell
149.0.7827.55 (`chromium-headless-shell` v1228). Runner-image drift is
**present and not excluded**: the successful scheduled run used
`ubuntu24/20260816.277`, while the manual and scheduled failures used
`ubuntu24/20260823.283`. The identical manual and scheduled failure summaries
on the newer image are repeat evidence, not a cross-image control.

### Nondeterminism

Nondeterminism is **known to exist**: the prior scheduled run's one flaky test
failed once and recovered. It is not a sufficient explanation for the observed
broad failure by itself: all 65 final failures survived the initial comparison
and both retries. Nondeterminism is nevertheless not globally excluded, and
ADR-011 forbids treating a single clean committed-baseline comparison as proof
of determinism.

## First supported divergence

The first **execution-supported** divergence is the bounded interval
`31659a59..b36ea9e`: the former head has the last observed scheduled flaky-green
Linux job; the latter has the first observed broad red and already matches the
later scheduled result exactly. Commits `c38b565`, `38606f4`, and `e093081`
landed after `b36ea9`, so they are excluded as initiators of this failure.

There is no Linux deep-gate execution at an intermediate commit in
`31659a59..b36ea9e`. Therefore this packet does **not** identify #464, the Sass
bump, or any other single commit as causal. #464 is evidence of intentional
rendering-source drift plus omitted Linux synchronization, not proof of the
point at which the run first became red.

## Named hypothesis

**H-LINUX-UNSYNC-01 — unsynchronized rendering-input drift.** The broad,
retry-stable failures at `b36ea9` and `e093081` occur because rendering inputs
changed after `31659a5` while the committed Linux baseline tree stayed
byte-identical. The hypothesis is interval-scoped: it does not assume #464 alone
is causal. The runner-image change is the principal unresolved confounder.

## Smallest Gate-1 experiment

On one fresh `ubuntu-24.04` runner, use two separate checkouts, one at
`31659a5` (control) and one at `e093081` (treatment). Record the runner-image
release, Node, npm, Sass, Playwright, and browser revisions. In each checkout,
run only the non-exempt `backup desktop light` visual comparison against the
already committed Linux baseline, with Playwright retries disabled, three fresh
times per arm. Do not invoke the deep-gate workflow and do not write snapshots.

Acceptance criteria:

1. Both arms execute on the same runner and browser installation, and the
   compare-only guard shows zero baseline writes.
2. The control passes 3/3 and the treatment fails 3/3 with the same substantive
   result: all three treatment actual PNGs have one SHA-256, all three diff PNGs
   have one SHA-256, and both differ from the committed-baseline SHA-256. That
   result supports H-LINUX-UNSYNC-01 and excludes runner drift for this capture;
   it still does not assign causality to #464 alone.
3. If the control also fails consistently, runner/toolchain drift remains viable
   and the hypothesis is inconclusive. If results vary within either arm,
   nondeterminism is implicated and the hypothesis is inconclusive. If both arms
   pass consistently, H-LINUX-UNSYNC-01 is falsified for the selected capture.

Any follow-on commit bisection or a broader capture matrix requires a separately
authorized Gate-1 extension; it is not implicit in this experiment.

## Decision preservation and hard stops

- **ADR-007 is unchanged.** `visual-linux` remains outside the release gate.
  The failed third scheduled run does not satisfy the three-consecutive-green
  revisit condition, and even satisfying that condition would require a fresh
  owner decision before promotion.
- **ADR-011 is unchanged.** The terminal contract remains 81 byte-gated
  captures plus the five named semantic exemptions. No tolerance, retry, mask,
  crop, viewport, or exemption-set change is authorized.
- **Baseline regeneration is explicitly forbidden** without separate
  authorization, including Linux or Win32 screenshot/baseline updates.
- **Promotion of `visual-linux` into any release gate is explicitly forbidden**
  without separate authorization.
- **Production, CSS, theme, template, workflow, screenshot, and baseline changes
  are explicitly forbidden** without separate authorization. Gate 1, if
  authorized, is diagnostic and compare-only.
