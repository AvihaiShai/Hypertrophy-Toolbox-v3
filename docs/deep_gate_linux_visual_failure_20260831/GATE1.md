# Gate 1: H-LINUX-UNSYNC-01 diagnostic result, 2026-09-01

## Verdict

**The Gate-1 experiment specified in [`GATE0.md`](GATE0.md) executed once, completely, and
landed on acceptance criterion 2.** For the one selected capture, the result **supports**
H-LINUX-UNSYNC-01 and **excludes runner-image, browser and within-arm nondeterminism** as
explanations. It **assigns causality to no commit**, and it says nothing about the other 64
failing captures.

This packet records that result and retires the temporary diagnostic workflow. It authorizes
no fix, no baseline regeneration, no CSS, theme, template, tolerance, mask, retry, viewport or
exemption change, no `visual-linux` promotion, and no R2.4 decision. [ADR-007](../DECISIONS.md#adr-007-release-tags-are-exact-vapp_version-tags-and-the-release-gate-reuses-ci-rather-than-re-running-it)
and [ADR-011](../DECISIONS.md#adr-011-the-terminal-visual-contract-is-81-byte-gated-captures-plus-five-semantic-exemptions)
are unchanged.

## The run

| Field | Exact value |
|---|---|
| Workflow | `TEMP H-LINUX-UNSYNC-01 Gate-1 diagnostic` (`.github/workflows/linux-visual-gate1.yml`, added by [#477](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/477), `fabdb2f`) |
| Run | [`33565764116`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33565764116), event `workflow_dispatch`, attempt **1**, conclusion **`success`** |
| Head | `5d3bc95a5251f74d74ff9350a1de11a4131d7999` (the run's own checkout ref; both experiment arms are pinned by SHA and do **not** use this tree) |
| Job | [`100048464157`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33565764116/job/100048464157), started `2026-09-01T22:20:12Z`, completed `2026-09-01T22:22:14Z` |
| Steps | **12 of 12 succeeded**, including both guard steps and the artifact upload |
| Evidence artifact | `h-linux-unsync-01-gate1`, id `9823089086`, 8,292,115 bytes, **expires `2026-09-15T22:22:09Z`** |

The job's `success` conclusion is **not** the experimental result. The workflow deliberately
captures each Playwright invocation's exit code with `set +e` and records it as evidence, so a
failing treatment arm is an expected observation rather than a red job. Read the per-invocation
exit codes below, never the job conclusion.

## Held-equal inputs

Both arms ran in the same job, on one runner, against one browser installation.

| Input | Control `31659a5` | Treatment `e093081` |
|---|---|---|
| Runner image | `ImageOS=ubuntu24`, `ImageVersion=20260823.283.1`, Ubuntu 24.04.4 LTS, kernel `6.17.0-1022-azure` | one runner, so identical by construction |
| Node / npm / Python | `v24.19.0` / `11.17.0` / `3.14.6` | identical |
| Playwright | `Version 1.61.0` | `Version 1.61.0` |
| Browser executable | `/home/runner/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome` | identical path |
| Browser version | `Google Chrome for Testing 149.0.7827.55` | identical |
| Committed Linux baseline `backup-desktop-light.png` | `4e116bdb35cc6697d92d3f77249f9b9e032f8ceef3b0e6e0d5c2159ba4ff87ca` | identical |
| Selector resolution | `Total: 1 test in 1 file` | `Total: 1 test in 1 file` |

The workflow asserted the browser path, the browser version, the Playwright version and the
committed-baseline SHA-256 to be equal across arms **before** running anything, and the step
succeeded. The equality is measured, not assumed.

### The one input that differs, recorded without a causal claim

`npx sass --version` reports **`1.102.0` (dart2js 3.12.2)** in the control checkout and
**`1.103.1` (dart2js 3.13.1)** in the treatment checkout. That is expected: each arm installed
from its own `package-lock.json` and compiled its own CSS, so the Sass toolchain is part of the
treatment, not a confounder introduced by the harness. GATE0 already named `b733c14` as one of
several candidate rendering-input changes in the interval. **This run does not separate the Sass
bump from #464's token/theme changes or from the two template changes**, and nothing here ranks
them.

## Results

Three fresh compare-only invocations per arm, `--retries=0 --workers=1`, each in its own
`TEST_ARTIFACTS_DIR` and its own `PW_DB_PATH`, on distinct ports.

| Arm | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| **Control `31659a5`** | `1 passed (5.1s)`, exit **0** | `1 passed (5.0s)`, exit **0** | `1 passed (4.9s)`, exit **0** |
| **Treatment `e093081`** | `1 failed`, exit **1** | `1 failed`, exit **1** | `1 failed`, exit **1** |

Every treatment failure is the same comparison failing the same way:

```
Error: expect(page).toHaveScreenshot(expected) failed
  20112 pixels (ratio 0.01 of all image pixels) are different.
```

**20112** is the pixel count in all three treatment runs.

### Byte-level determinism within the treatment arm

| Produced file | SHA-256 | Occurrences |
|---|---|---|
| `backup-desktop-light-actual.png` | `f2a689840749eb3ddfed993e8cf020ea124e853c687d73f185ed105af50de608` | 3 of 3 treatment runs |
| `backup-desktop-light-diff.png` | `2b376bef9bf91c904d56aa33eded07c8e0c5013a9bf0edf4b09f836a8134bb8b` | 3 of 3 treatment runs |

The treatment actual differs from the committed baseline `4e116bd…`. The control arm produced
**no** `*-actual.png` and **no** `*-diff.png` at all — its hash manifest is empty, which is what
three clean passes look like.

### The baseline-write guard held

For each arm the workflow hashed the entire `e2e/__screenshots__` tree before and after,
`cmp`-ed the two manifests, and additionally required `git status --porcelain -- e2e/__screenshots__`
to be empty. Both checks passed for both arms. **No baseline was written or modified.** The
`--update-snapshots` flag appears nowhere in this workflow.

## What this establishes, and what it does not

### Established for the selected capture

1. **Acceptance criterion 2 of GATE0 is met exactly as written**: control 3/3 pass, treatment
   3/3 fail, one actual SHA-256, one diff SHA-256, both differing from the committed baseline.
2. **Runner-image drift is excluded for this capture.** GATE0 listed it as "present and not
   excluded" because the last green scheduled run used `ubuntu24/20260816.277` while both
   observed reds used `ubuntu24/20260823.283`. Here the control tree — the tree that was green
   on the older image — passes **3/3 on `20260823.283.1`**, the newer image. The image change
   is therefore not what turned this capture red.
3. **Browser drift is excluded for this capture** by construction: one installation, one
   executable path, asserted equal.
4. **Within-arm nondeterminism is excluded for this capture.** Three independent invocations of
   the treatment tree produced a byte-identical actual PNG. This is a stable difference, not a
   flake.
5. **The difference is carried by the checked-out tree.** With runner, browser and committed
   baseline held equal and measured, the only variable left between the two arms is the source
   at `31659a5` versus `e093081` — which is what H-LINUX-UNSYNC-01 asserts.

### Not established

- **No commit is identified as causal.** This is a two-point comparison across a multi-commit
  interval. GATE0's first execution-supported divergence remains the bounded interval
  `31659a59..b36ea9e`, and no run exists at any intermediate commit. #464, the Sass bump and the
  template changes remain unranked candidates.
- **No mechanism is identified.** The experiment shows *that* the tree changed the rendering of
  this capture, not *which* rendering input did it, and not what the 20,112 differing pixels are.
- **Nothing is generalized to the other 64 captures.** One non-exempt capture was selected on
  purpose. The scheduled failure was **65 failed, 17 did not run, 18 passed**; this run speaks to
  one of the 65.
- **Nondeterminism is not globally excluded.** It is excluded for this capture over three
  invocations on one runner. ADR-011's bar is unchanged.
- **Nothing about the baseline's correctness is established.** That the committed Linux baseline
  no longer matches the current tree does not say which of the two is right. Deciding that is a
  separate, owner-authorized act, and regeneration remains forbidden here.

## Disposition of the temporary workflow

`.github/workflows/linux-visual-gate1.yml` was introduced by #477 as a single-use,
`workflow_dispatch`-only diagnostic. It has now been dispatched once and has produced its
result, so this packet **deletes it** and reverts the one contract line #477 added to
`tests/test_release_workflow_contracts.py`.

That revert is required, not cosmetic. `test_the_workflow_directory_holds_exactly_the_files_this_file_reads`
compares `.github/workflows/` on disk against the `ALL_WORKFLOWS` literal in **both** directions,
so deleting the file without removing `LINUX_VISUAL_GATE1` reds that contract. `ALL_WORKFLOWS`
is iterated only inside test bodies and is not a `parametrize` source, so the file's pytest node
count is unchanged and `docs/test_inventory/` does not move.

Re-running this experiment means restoring the workflow under a fresh authorization, with the
evidence above as the prior. The retained artifact expires `2026-09-15T22:22:09Z`; every figure
this document depends on is transcribed here so the record outlives it.

## The next owner decision

**One decision is now due: what, if anything, follows this result.** GATE0 states that any
follow-on commit bisection or broader capture matrix "requires a separately authorized Gate-1
extension; it is not implicit in this experiment." None of the options below is taken here.

| Option | What it would authorize | Cost and risk |
|---|---|---|
| **A — Bisect the interval** | One further diagnostic run per probed commit inside `31659a59..b36ea9e`, same compare-only shape, to name the initiating commit | ~2 minutes of runner time per probe; the interval is small; still diagnostic, still no fix |
| **B — Widen the capture matrix** | Re-run the same two-arm comparison over more of the 65 failing captures, to test whether they share one cause | Larger runs; risks being read as a fix mandate when it is still only evidence |
| **C — Authorize Linux baseline synchronization** | Regenerate the Linux baseline tree against the current source and accept it by eye | The heaviest option; forbidden without explicit owner sign-off, and never to be taken merely because a comparison is red |
| **D — Stop here** | Nothing further; the Linux failure stays a recorded, bounded, unfixed residual | Zero cost; `visual-linux` stays out of the release gate and the weekly deep gate stays red |

**Recommendation, not a decision: A.** It is the cheapest option, it directly closes the one gap
GATE0 named ("there is no Linux deep-gate execution at an intermediate commit"), and it is the
prerequisite for arguing about B or C on evidence rather than on inference. **A is a diagnostic
authorization only and would not license a fix.**

**R2.4 is not decided here and is not on this list.** `visual-linux` remains outside the release
gate, ADR-007 is untouched, and nothing in this result is a promotion argument.

## Hard stops carried forward from GATE0

- **ADR-007 unchanged.** `visual-linux` stays outside the release gate. Promotion needs a fresh
  owner decision regardless of any evidence here.
- **ADR-011 unchanged.** 81 byte-gated captures plus five named semantic exemptions. No
  tolerance, retry, mask, crop, viewport or exemption-set change is authorized.
- **Baseline regeneration remains explicitly forbidden** without separate authorization, Linux
  and Win32 alike.
- **Production, CSS, theme, template, screenshot and baseline changes remain explicitly
  forbidden** without separate authorization.
