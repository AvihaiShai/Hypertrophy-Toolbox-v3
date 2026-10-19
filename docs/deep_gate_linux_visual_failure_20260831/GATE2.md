# Gate 2: H-LINUX-UNSYNC-01 bounded bisect (CI/CD packet E3), 2026-10-19

## Status

**Pre-registration.** Everything above [Results](#results) was written and pushed before the
first probe ran. The results section is appended afterwards and does not edit the contract.

This packet is diagnosis only. It authorizes no fix, no baseline regeneration, no CSS, theme,
template, tolerance, mask, retry, viewport or exemption change, and no `visual-linux` promotion.
[ADR-007](../DECISIONS.md#adr-007-release-tags-are-exact-vapp_version-tags-and-the-release-gate-reuses-ci-rather-than-re-running-it)
and
[ADR-011](../DECISIONS.md#adr-011-the-terminal-visual-contract-is-81-byte-gated-captures-plus-five-semantic-exemptions)
are unchanged.

## Authority

- [GATE1.md](GATE1.md) "The next owner decision", **option A**: bisect `31659a59..b36ea9e`,
  same compare-only shape, diagnostic only.
- Owner authorization of 2026-10-19 for the named H-LINUX-UNSYNC-01 Gate-1 diagnostic
  extension, restricted to the existing `backup desktop light` capture, under CI/CD FORMAL CORE
  Plan v2 (core Gate 1 signed in [`docs/ci_cd_expansion/PLANNING.md`](../ci_cd_expansion/PLANNING.md)
  §12.5; packet E3 in §4 Phase E).

## Pre-registered contract

### Endpoints and candidate set

| Field | Value |
|---|---|
| Control endpoint | `31659a59ccc82391287d98f2e9d899a048d20b2c` (last scheduled flaky-green Linux run, [GATE0.md](GATE0.md)) |
| Treatment endpoint | `b36ea9e1a3d7e0e37918e9db4198cb4bf7e0ecf8` (first observed broad red, GATE0) |
| Candidate set | `git rev-list --first-parent --reverse 31659a59..b36ea9e1`: **50 commits**, first `5111a7fc9793fe5323134c157054e6b740641717` (first parent = control), last = treatment |
| Candidate-list digest | SHA-256 of the 50 full SHAs, one per line, LF-terminated: `d11d59a010a447bb0866d6f9d0b15145a3cf9c89b44f2ce192b51849011bc6d2` |
| Positions | 0 = control, 1..50 = candidates in order, 50 = treatment |
| Only merge in the interval | `07781a83` (#433). Its two second-parent commits (`99cb8af`, `d35e369`) change only `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md`; probing the merge covers them. |

Measured in the clone before execution, and re-asserted by the harness on the runner for every
probe: the committed Linux baseline tree `e2e/__screenshots__/linux` is
`206f30d8b7e90777bcf157217d04839045528000` at every position, the baseline
`backup-desktop-light.png` is SHA-256 `4e116bdb35cc6697d92d3f77249f9b9e032f8ceef3b0e6e0d5c2159ba4ff87ca`
(the same value GATE1 measured), and `.python-version` (`3.14.6`) does not change in the
interval. `package-lock.json` pins Playwright `1.61.0` at both endpoints. Sass changes from
`1.102.0` to `1.103.1` inside the interval (`b733c14`) and `requirements.txt` gains `hypothesis`
(`e9f942f`); each probe installs its own commit's dependencies, so those are part of the tree
under test, as in GATE1.

### Selector and command

One capture only: `e2e/visual.spec.ts`, Playwright project `chromium`, grep
`backup desktop light$`, which must list exactly `Total: 1 test in 1 file`. Per invocation, in
the probed commit's own checkout:

```
CI=true PW_VISUAL_SEED=1 PW_WORKERS=1 PW_PORT=<unique> PW_DB_PATH=<run>/database.db \
TEST_ARTIFACTS_DIR=<run> npx playwright test e2e/visual.spec.ts --project=chromium \
  --grep 'backup desktop light$' --retries=0 --workers=1 --reporter=line
```

This is GATE1's command unchanged. `--update-snapshots` appears nowhere in the harness.
`playwright.config.ts`, `e2e/visual.spec.ts`, `e2e/visual-helpers.ts`, `e2e/strict-fixtures.ts`
and `e2e/scripts/` have **no** first-parent change anywhere in the interval, so the test, its
seeding and its artifact routing (`outputDir` under `TEST_ARTIFACTS_DIR`) are identical at every
position.

Two deliberate differences from the deep gate, which make a probe stricter, not equivalent:
retries are `0` where the CI configuration allows `2`, so a capture that recovers on retry is
never `GOOD` here; and the one test runs alone, where the deep gate runs three visual specs in
one invocation. The endpoint controls below run under the same conditions, so neither
difference can manufacture a boundary that the endpoints do not also show.

### Fixed environment

- GitHub-hosted `ubuntu-24.04`, the image the deep gate's `visual-linux` job pins. Runner-image
  release, kernel, Node, npm and Python are recorded per job, not assumed equal to GATE1's. The
  confirmation job records whether its image release matches the bisect job's.
- Python from the treatment's `.python-version`; Node `24` via `actions/setup-node`.
- Per probe: a fresh runner-local checkout of that commit, its own venv
  (`pip install -r requirements.txt`), `npm ci`, `npm run build:css` — the deep gate's own
  install sequence.
- One Chromium installed once per job with `npx playwright install --with-deps chromium`.
  Every probe must report the same Playwright version, browser executable path and browser
  version as the job's first probe, or it is `ENV_MISMATCH`.

### Harness

| Field | Value |
|---|---|
| Workflow | `TEMP E3 H-LINUX-UNSYNC-01 bounded bisect`, `.github/workflows/e3-linux-bisect.yml` |
| Script | `.github/e3-bisect/e3_bisect.sh` |
| Branch | `diag/e3-h-linux-unsync-01-bisect`, **never merged**; the only trigger is a push to that branch |
| Harness commit | `abf65918e01af75c0de9352a45fd0a9741d2ba70` (reviewed; see [Harness gates](#harness-gates)) |
| Permissions | `contents: read`; `persist-credentials: false`; actions pinned to the same full SHAs as `ci.yml` |

The harness does not run on `main`, on pull requests or on a schedule, and it does not touch
`ci.yml` or `deep-gate.yml`. It checks out each interval commit separately, so current product
source is never under test. Its one test-file edit, an `ALL_WORKFLOWS` census entry so the
workflow contracts cover it on that branch, never reaches `main`.

### Classification

Each invocation is one of:

| Class | Rule |
|---|---|
| `PASS` | exit 0, `1 passed`, no failed/flaky/skipped/did-not-run count, no `*-actual.png` |
| `RENDER_FAIL` | exit 1, exactly one `*-actual.png`, a `toHaveScreenshot` failure reporting differing pixels or a different image size, and no stable-screenshot timeout |
| `STARTUP_FAIL` | a Playwright `config.webServer` failure or a refused connection |
| `OTHER_FAIL` | anything else, including an unstable-screenshot timeout |

Each probe (one commit, three fresh invocations) is one of:

| Class | Rule |
|---|---|
| `GOOD` | 3 × `PASS` |
| `BAD` | 3 × `RENDER_FAIL` with one actual-PNG SHA-256, one diff-PNG SHA-256, and actual ≠ committed baseline |
| `NONDETERMINISTIC` | `PASS` mixed with `RENDER_FAIL`, or 3 × `RENDER_FAIL` with differing hashes |
| `STARTUP_FAIL` / `OTHER_FAIL` | any invocation in that class |
| `INSTALL_FAIL` | venv, pip, `npm ci` or `build:css` failed |
| `INPUT_MISMATCH` | baseline tree, baseline SHA-256 or `.python-version` differs from the pre-registered value |
| `ENV_MISMATCH` | Playwright or browser identity differs within the job |
| `SELECTOR_FAIL` | the selector does not list exactly one test |

Only `GOOD` and `BAD` move the bisect. A baseline write — the `e2e/__screenshots__` manifest
changing, or `git status` reporting a change there — aborts the whole run as a harness fault.

### Endpoint controls

The bisect job probes the control and then the treatment before anything else, on the same
runner and browser installation as every bisect probe. **The bisect runs only if the control is
`GOOD` and the treatment is `BAD`.** Otherwise the verdict is `ENDPOINTS_NOT_DISTINGUISHED`
and the result is reported as inconclusive; the older commit is not assumed to be a valid
control because GATE1 found it to be one on an earlier runner image.

### Budget

- 50 candidates need at most ⌈log₂ 50⌉ = **6** bisect probes (interval 50 → 25 → 13 → 7 → 4 → 2 → 1).
- Plus 2 endpoint probes and, only after `BOUNDARY_FOUND`, 2 confirmation probes.
- **Planned cap: 10 probes = 30 invocations in one workflow run of two jobs.** The harness
  refuses a seventh bisect probe (`BUDGET_EXHAUSTED`).
- **Infrastructure allowance: at most one re-run of the whole workflow run**, and only if a job
  ended without a verdict for an infrastructure reason (runner loss, timeout, network or
  registry failure), or the verdict is `INCONCLUSIVE_INSTALL_FAIL` or
  `INCONCLUSIVE_STARTUP_FAIL` with logs showing an infrastructure cause. No re-run for any other
  verdict, and never to change a rendering observation. Absolute ceiling: **2 run attempts,
  20 probes, 60 invocations.**

### Stopping criteria and what each verdict supports

| Verdict | Meaning | Reported as |
|---|---|---|
| `ENDPOINTS_NOT_DISTINGUISHED` | The endpoints do not separate pass from fail in this environment | Inconclusive; the whole interval stays unresolved |
| `INCONCLUSIVE_<class>` | A probe was neither `GOOD` nor `BAD` | Inconclusive; the narrowed interval at that point is reported |
| `BUDGET_EXHAUSTED` | Six bisect probes did not converge (not reachable for 50 candidates unless the harness is wrong) | Inconclusive |
| `BOUNDARY_FOUND` then `NOT_CONFIRMED` | The adjacent pair did not reproduce on a fresh runner | Inconclusive; the pair is reported as unconfirmed |
| `BOUNDARY_FOUND` then `CONFIRMED` | The adjacent pair reproduces `GOOD` → `BAD` on a fresh runner | Attribution, subject to the check below |

**Pre-registered sanity check before naming a commit:** the first-bad commit's own first-parent
diff must touch at least one path that can reach this capture's rendering — any path outside
`docs/**`, `tests/**`, `.claude/**`, `.github/**` and `*.md`. A confirmed boundary at a commit
that touches none of these contradicts the hypothesis that source drift caused the change, and
is reported as inconclusive.

### Limits on the claim, stated in advance

- Binary search assumes a single pass→fail transition. Untested positions are inferred, not
  observed, so the result is a **first-parent boundary**, not proof that no other transition
  exists; confirmation re-tests only the adjacent pair. A first-bad actual-PNG hash that differs from the treatment's means at least one
  later commit changed this capture again; the attribution then names only the first change.
- An attribution says that commit's tree is the first on the first-parent line whose rendering
  of this one capture differs from the committed Linux baseline in this environment. It does not
  identify which file or mechanism inside the commit is responsible, says nothing about the
  other 64 failing captures, and does not say whether the baseline or the new rendering is
  correct.

## Harness gates

The harness is a CI-workflow change that adds jobs, so its gate is full `pytest` plus
independent `code-reviewer` and `architecture-reviewer` (`docs/ai_workflow/QUALITY_GATE.md`).

- **architecture-reviewer** (first pass on `c94b012b`): no blocking findings. Isolation from
  `ci.yml`, `deep-gate.yml`, `release.yml`, required contexts and E1/D3 confirmed. Accepted and
  fixed: per-probe disk exhaustion; runner-image comparison between jobs; "boundary" wording;
  disclosing retries `0`. One remark — that ADR-007 does not cover `visual-linux` — is refuted:
  ADR-007's decision R1-D3 is exactly "`visual-linux` stays out of the release gate".
- **code-reviewer** (first pass on `c94b012b`): no path to a false `GOOD` or `BAD`. Fixed: an
  absolute `python-version-file` that `setup-python` may resolve against the workspace; `set -e`
  being ignored inside the `if ! ( … )` install block, which would have mislabelled a pip failure;
  the baseline manifest now precedes installs; single-transition wording. Artifact routing at
  earlier commits was measured unchanged (above), so no change was needed.
- **Fix delta `abf65918`**, same code-reviewer resumed: no blocking findings; every fix above
  verified. Two minor residuals accepted without change: the runner-image comparison is written
  to the confirmation job's `environment.txt` rather than its summary (this document reads the
  artifact, so it is reported either way); and a checkout missing `e2e/__screenshots__` would
  surface as a harness fault rather than `INPUT_MISMATCH`, which is still a stop, never a
  `GOOD` or `BAD`.
- **Full pytest** on exactly `abf65918`, in the standalone clone (Windows, Python 3.14.6, Git
  Bash first on `PATH`): `python -m pytest tests/ -q --junitxml=artifacts/e3/pytest-full.xml`
  → **5,243 passed, 2 skipped, 0 failed, 0 errors**, 1,607.74 s, exit 0,
  `2026-10-19T14:43:52Z`–`15:10:41Z`. JUnit SHA-256
  `031686b76d3d2335f69645bbcc1b3938b638a2aab445e83864d4fe088cb43cbf` (retained in the clone's
  ignored `artifacts/e3/`). An earlier run on `c94b012b` was stopped by hand because the review
  fixes were edited into its working tree mid-run; it is not credited.

## Isolation and coordination

- Standalone HTTPS clone `D:/development/Hypertrophy-Toolbox-v3-e3-bisect-20261019`
  (blobless: full commit history, independent object storage, no alternates), its own venv and
  `node_modules`, clone-local runtime paths. The shared checkout, recovery sources and other
  sessions' changes were not touched.
- The A1 owner session (packet A1, `ci.yml`) agreed that E3 runs first and that it will not
  dispatch a benchmark wave while an E3 job is in progress. E3's UTC run window is recorded
  below so A1 can exclude it from its speed measurements.

## Results

*Appended after execution. Nothing above this heading was changed after the pre-registration
commit `b1207f17ab3549be9c54ea3f911cfd595ee89fab`, whose branch GitHub records as created at
`2026-10-19T15:15:21Z`, twelve seconds before the harness branch (`15:15:33Z`).*

### Verdict

**Supported attribution for the one selected capture: the first-parent boundary is
`e6e57eac` (#463) → `e9eff89a` (#464).** The bisect returned `BOUNDARY_FOUND` and the separate
confirmation job returned `CONFIRMED`. Under the single-transition assumption bisection rests on,
#464 is the initiating commit: the first on the first-parent line whose tree renders
`backup desktop light` differently from the committed Linux baseline in this environment. It
produces the same failing image that the treatment endpoint and GATE1's `e093081` produced.

This assigns no mechanism inside #464. It also says nothing about the other 64 captures and does
not decide whether the baseline or the new rendering is correct.

### The run

| Field | Exact value |
|---|---|
| Run | [`39276388378`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39276388378), event `push`, attempt **1**, head `abf65918e01af75c0de9352a45fd0a9741d2ba70`, created `2026-10-19T15:15:35Z`, conclusion `success` |
| Bisect job | [`118141659831`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39276388378/job/118141659831), `15:15:38Z`–`15:20:59Z`, `success`, verdict `BOUNDARY_FOUND` |
| Confirmation job | [`118144248491`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39276388378/job/118144248491), `15:21:03Z`–`15:23:06Z`, `success`, verdict `CONFIRMED` |
| Artifact `e3-bisect` | id `12198335832`, 20,561,064 B, `sha256:8a2bf74eef0e4aaa93fb5468aeb7d41e57ba11ed7e79a1f804d4ba4223a967ed`, expires `2027-01-17T15:15:35Z` |
| Artifact `e3-confirm` | id `12197364011`, 8,307,922 B, `sha256:9cf2ef59482d2ce3c8ffb80007341a2b19aba82136aaf5d19725300f966a4650`, expires `2027-01-17T15:15:35Z` |

As in GATE1, the job conclusion is **not** the result. The verdicts come from each job's
`verdict.env` and `results.tsv`, and every figure below is transcribed from those files so the
record outlives the artifacts.

### Environment, measured

| Input | Bisect job | Confirmation job |
|---|---|---|
| Runner image | `ImageOS=ubuntu24`, `ImageVersion=20261012.334.1`, Ubuntu 24.04.5 LTS, kernel `6.17.0-1022-azure` | `20261012.334.1` (recorded `same_image_version=yes`) |
| Runner identity | `RUNNER_NAME=GitHub Actions 1000022835`, hostname `runnervm8k3b6` | `GitHub Actions 1000022836`, the **same** hostname `runnervm8k3b6` |
| Node / npm / Python | `v24.21.0` / `11.19.0` / `3.14.6` | identical |
| Playwright | `Version 1.61.0` at all 8 probes | `1.61.0` at both probes |
| Browser installed | Chrome for Testing **and** Chrome Headless Shell `149.0.7827.55`, both Playwright revision `1228`, downloaded into an empty cache | identical, downloaded again into an empty cache |
| Browser reported | `chromium.executablePath()` = `…/chromium-1228/chrome-linux64/chrome`, `Google Chrome for Testing 149.0.7827.55` at every probe | identical |
| Committed baseline | `4e116bdb…87ca` at every probe | identical |
| Selector | `Total: 1 test in 1 file` at every probe | identical |
| Baseline guard | the 162-file `e2e/__screenshots__` manifest was unchanged before and after at every probe, and `git status` was clean | identical |

The harness records the path `chromium.executablePath()` reports, not the binary each headless
run launched. Both revision-`1228` builds were present, and the deep gate's own failing run used
the headless shell of that revision (GATE0), so the measured identity is the revision and
version, not which of the two executables rendered.

Compared with GATE1, the runner image (`20260823.283.1` → `20261012.334.1`), Node
(`24.19.0` → `24.21.0`) and npm (`11.17.0` → `11.19.0`) moved, while Playwright, the browser
build and the baseline did not. The endpoint controls were therefore re-established here rather
than inherited from GATE1.

### Endpoint controls

| Probe | Commit | Sass | Invocations | Result |
|---|---|---|---|---|
| 1 | control `31659a59` (position 0) | 1.102.0 | `1 passed` ×3 (4.6 s, 4.8 s, 4.6 s), exit 0 ×3, no actual PNG | **GOOD** |
| 2 | treatment `b36ea9e1` (position 50) | 1.103.1 | exit 1 ×3, `20112 pixels (ratio 0.01 of all image pixels) are different` ×3 | **BAD** |

**The endpoints distinguish pass from fail in this environment.** The treatment's actual PNG is
`f2a689840749eb3ddfed993e8cf020ea124e853c687d73f185ed105af50de608` and its diff PNG is
`2b376bef9bf91c904d56aa33eded07c8e0c5013a9bf0edf4b09f836a8134bb8b`, three times each. Both
hashes, and the 20,112-pixel count, are byte-for-byte the values GATE1 recorded for `e093081`
on the older image.

### Bisect

| Probe | Position | Commit | PR | Interval before → after | Result |
|---|---|---|---|---|---|
| 3 | 25 | `3e60cdd446d4d33c447762a59909814ea366776e` | #442 | 0..50 → 25..50 | GOOD (3 × `PASS`) |
| 4 | 37 | `8c844dfda6ca6363f779721529e808445c24b828` | #454 | 25..50 → 37..50 | GOOD |
| 5 | 43 | `7d9a836c3204b81f357bc6ebf90b90ea421db9eb` | #461 | 37..50 → 43..50 | GOOD |
| 6 | 46 | `8a1ad9dbc2fe9983545f6e9ec5952755afe6a5af` | #457 | 43..50 → 46..50 | GOOD |
| 7 | 48 | `e9eff89a1344f87668b733bef272879d9e95c040` | #464 | 46..50 → 46..48 | **BAD**: actual `f2a68984…`, diff `2b376bef…`, 20,112 px, ×3 |
| 8 | 47 | `e6e57eac224a09957d9c8ce3128ee6013cee6208` | #463 | 46..48 → 47..48 | GOOD |

Six bisect probes, as predicted for 50 candidates. Every bisect probe ran Sass `1.103.1`.

### Boundary confirmation on a fresh runner

| Probe | Commit | Result |
|---|---|---|
| 1 | `e6e57eac` (position 47) | GOOD, exit 0 ×3 |
| 2 | `e9eff89a` (position 48) | BAD, exit 1 ×3, 20,112 px; actual `f2a68984…` ×3, diff `2b376bef…` ×3 |

The confirmation job re-tested the pair with fresh checkouts, fresh dependency installs and a
browser downloaded again into an empty cache, and reproduced both classes and both hashes. It
reported a different `RUNNER_NAME` but the same hostname, so a different VM is not established;
what it does establish is that the result does not depend on state the bisect job left behind. It
ran on the same image release, so it is not a cross-image control.

### Pre-registered sanity check

Passed. `e9eff89a` (#464, squash-merged; its only parent is `e6e57eac`) changes eleven rendering
inputs: eight files under `static/css/` (`tokens.css`, `theme-dark.css`, `components.css`,
`layout.css`, `navbar.css` and three page bundles), `templates/base.html`,
`static/js/theme-init.js` and `static/js/darkMode.js`. It also changes 77 Win32 screenshots and **zero** Linux screenshots.
`e6e57eac` (#463) changes four files, all under `docs/`.

### Budget used

1 workflow run, 1 attempt, 10 probes and 30 invocations, the planned path. No harness fault, no
infrastructure failure, no re-run; the infrastructure allowance was not used.

### Contract wording corrected against the code

The pre-registration says `.python-version` is checked against the pre-registered value. The
harness actually compares each probe with the first probe's copy and does not compare with the
literal `3.14.6`. The job's Python comes from the treatment's file, which is `3.14.6`, and no
probe reported `INPUT_MISMATCH`, so the result is unaffected. A probe mixing `STARTUP_FAIL` with
another failure class resolves to `STARTUP_FAIL`; no probe in this run mixed failure classes.

### What this establishes, and what it does not

**Established for the selected capture, in this environment:**

1. **The boundary itself is observed, not inferred** (see [Verdict](#verdict)): each side three
   times in each of two jobs.
2. **Later commits in the interval did not change this capture again at the tested points.**
   #464, the treatment `b36ea9e1` and GATE1's `e093081` all produce one byte-identical actual
   PNG. That is consistent with a single change, but position 49 (`52ca8a82`) was not probed.
3. **None of the other named candidate changes produces this failure by itself.** Each is
   present in a probed GOOD tree: the Sass bump `b733c14` (position 11) in all five GOOD bisect
   probes, positions 25–47, which ran Sass `1.103.1`; #427's `backup-center.js` change (16) in
   the same trees; the summary-template change `e9f942f` (41) in the trees at 43–47; and
   `7d9a836` (43) was probed directly. That one of them caused a failure that later recovered
   before position 25 or 43 is excluded only by the single-transition assumption.
4. **The newer runner image `20261012.334.1` does not by itself red this capture.** The control
   passes on it, as it passed on `20260823.283.1` in GATE1.

**Not established:**

- **No mechanism.** This experiment does not say which of #464's eleven rendering inputs, or
  which interaction between them, produces the 20,112 differing pixels.
  Isolating that would be a new experiment inside one commit and is not authorized.
- **Monotonicity is assumed, not proven.** 43 of the 49 intermediate positions were not probed.
  A pass→fail→pass→fail pattern elsewhere in the interval would not be visible here, although
  the single repeated failing image makes that unlikely for this capture.
- **Nothing is generalized to the other 64 failing captures.** They may share #464 as their
  initiator or not; that is GATE1 option B and was not run.
- **Nothing about correctness.** GATE0 records that #464's merged description states no Linux
  baseline was touched and Linux work remained outstanding. This result is consistent with
  H-LINUX-UNSYNC-01 for this capture. It does not decide whether the Linux baseline should be
  regenerated (GATE1 option C), which remains a separate owner decision.
- **Not a deep-gate outcome.** Retries were 0, the test ran alone, and the launched browser
  executable was not recorded (see [Environment, measured](#environment-measured)). The verdicts
  are stricter than, not equivalent to, a deep-gate result.

### What remains unfixed

- The weekly deep gate's `Visual regression (Linux baselines)` job stays red. Nothing here
  changes CSS, templates, baselines, tolerances, masks, viewports, retries or exemptions.
- The committed Linux baseline tree is still `206f30d8…`, unsynchronized with #464's source.
- The other 64 captures are uninvestigated. `visual-linux` stays outside the release gate under
  ADR-007 (R1-D3). ADR-011's 81 byte-gated captures and five semantic exemptions are unchanged.

### Disposition of the harness

The harness exists only on `diag/e3-h-linux-unsync-01-bisect` (head `abf65918`). It was never
merged, so no workflow on `main` needs retiring and `main`'s `ALL_WORKFLOWS` census is untouched.
It runs only on a push to that branch. The branch is retained under the standing Operation A
retention hold, and no further push to it is authorized by this packet.

### The next owner decision

GATE1 option A is complete. Options **B** (widen the capture matrix — for example the pair
`e6e57eac`/`e9eff89a` over the other 64 captures), **C** (owner-authorized Linux baseline
synchronization) and **D** (stop) stand as GATE1 defines them; none is taken here. Isolating a
mechanism inside #464 would be a further diagnostic outside GATE1's options and needs its own
authorization.
