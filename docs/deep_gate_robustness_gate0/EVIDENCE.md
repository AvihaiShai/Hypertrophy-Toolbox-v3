# Deep-gate robustness — Gate 0 evidence

**Date:** 2026-08-30

**Base:** `origin/main` at `b36ea9e1a3d7e0e37918e9db4198cb4bf7e0ecf8`

**Branch:** `wt/deepgate-robustness-gate0`

**Decision:** evidence and green test contracts only; the workflow is unchanged.

## Scope and boundaries

This packet covers two latent deep-gate robustness gaps:

1. the visual compare job's no-baseline-write assertion was carried only by the
   workflow and prose, not by a durable repository test;
2. `full-e2e` builds its spec arguments with an unanchored `grep -vE` pipeline
   whose trailing `tr` masks a zero-match result.

No workflow, Playwright behavior, visual baseline, seed, branch-protection rule,
or retry/artifact policy changes in Gate 0. The following expressly remain
untouched:

- `docs/OPEN_WORK_EXECUTION_PLAN.md`;
- `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json`;
- `e2e/visual-helpers.ts`;
- `docs/visual_determinism/PLANNING.md`;
- `.github/workflows/**` and `e2e/__screenshots__/**`.

## A. No-baseline-write contract

### Exact current contract

The load-bearing step is
[`deep-gate.yml`](../../.github/workflows/deep-gate.yml), `visual-linux`, lines
458–466 at the Gate-0 base:

```yaml
- name: Assert compare mode wrote no baseline
  if: ${{ always() && steps.visual.outputs.mode != 'generate' }}
  run: |
    CHANGED="$(git status --porcelain -- e2e/__screenshots__)"
    if [ -n "$CHANGED" ]; then
      echo "$CHANGED"
      echo "a compare run wrote to e2e/__screenshots__; baselines change only through a reviewed generate run"
      exit 1
    fi
```

The preceding `Run visual specs` step has `id: visual` and writes
`mode=$MODE` to `$GITHUB_OUTPUT` before invoking Playwright. Therefore a
terminal Playwright failure still leaves the guard reachable, and a missing
output is also fail-safe because empty is not the literal `generate` value.

The precise guarantee is:

> Every non-generate visual run must finish with no Git-visible index/worktree
> delta under `e2e/__screenshots__`; otherwise the guard emits the porcelain
> paths and fails.

It is not proof that no write syscall occurred. An identical overwrite or a
write later reverted before the guard leaves no final delta. The current
command also inherits Git's untracked-file configuration; a future
`status.showUntrackedFiles=no` setting would blind it to new baselines unless
the command is hardened separately. Today the setting is unset, the subtree is
not ignored, and all 162 committed screenshot PNGs are tracked.

### Why the repository did not pin it

Before this packet:

- `test_the_deep_gate_keeps_baseline_generation_behind_its_generate_mode`
  pinned the single `--update-snapshots` occurrence and the schedule/generate
  assignments only;
- `test_no_step_carries_a_condition_that_could_skip_it_silently` iterated
  `NEW_WORKFLOWS = (RELEASE, PACKAGED)`, excluding `DEEP_GATE`;
- the Playwright runner contracts parsed `Run visual specs` only, stopping at
  the next step;
- no test named `Assert compare mode wrote no baseline`, its porcelain command,
  its condition, its path scope, or its failing exit.

Deleting the step, moving it before Playwright, changing its condition to
false, checking the wrong path, replacing its body with `echo ok`, or removing
`exit 1` therefore escaped the existing tests.

### Green Gate-0 characterization

[`tests/test_release_workflow_contracts.py`](../../tests/test_release_workflow_contracts.py)
now extends the existing baseline-mode contract without adding a new pytest
node. It requires:

- exactly one `Run visual specs` step and one named guard;
- the guard immediately after the visual step;
- `id: visual` and the exact `always()` non-generate condition;
- one scoped porcelain assignment, dirty branch, path emission, diagnostic,
  and `exit 1`, in fail-closed order;
- no `continue-on-error` or `|| true` escape.

This is a structural workflow contract. The emitted-path/runtime distinction
remains grounded in real job logs below.

## B. `full-e2e` spec selection

### Exact current contract

The current step contains:

```bash
SPECS=$(ls e2e/*.spec.ts | grep -vE 'visual\.spec\.ts|visual-baseline-thumbnails\.spec\.ts|workout-plan-desktop-contract\.spec\.ts' | tr '\n' ' ')
echo "Running: $SPECS"
npx playwright test --project=chromium $SPECS
```

At this base the inventory is 33 specs. The command selects 30 and excludes the
three intended visual-seed consumers. That current arithmetic is correct; the
construction is not robust.

### Reproduction 1 — trailing `tr` masks zero matches

Run under Git-for-Windows Bash with the workflow's effective `set -e` behavior:

```bash
set -e
SPECS=$(printf '%s\n' e2e/visual.spec.ts \
  | grep -vE 'visual\.spec\.ts' \
  | tr '\n' ' ')
printf 'masked_exit_reached specs_len=%s\n' "${#SPECS}"
```

Observed:

```text
masked_exit_reached specs_len=0
shell exit 0
```

Control with the same zero-match `grep` as the last command:

```text
shell exit 1
```

The trailing command supplies the pipeline's exit status because the workflow
uses the default Linux shell without `pipefail`. It also masks upstream
`ls`/`grep` errors, not only the legitimate zero-match case.

### Reproduction 2 — the regex is unanchored

Against representative paths, the current expression silently removes:

```text
e2e/dark-visual.spec.ts
e2e/nonvisual.spec.ts
e2e/not-visual-baseline-thumbnails.spec.ts
e2e/pre-workout-plan-desktop-contract.spec.ts
```

An exact-path comparison keeps those names while excluding only:

```text
e2e/visual.spec.ts
e2e/visual-baseline-thumbnails.spec.ts
e2e/workout-plan-desktop-contract.spec.ts
```

The real current inventory has no such collision, which is why the latent
defect has not yet changed a run's 30-file selection.

### Reproduction 3 — empty arguments select everything

Collection-only Playwright probes were used; no server, browser test, snapshot
write, or baseline update occurred.

```text
explicit current 30 paths:
  exit 0
  Total: 586 tests in 30 files

empty positional array:
  exit 0
  Total: 686 tests in 33 files
```

With empty `SPECS`, the unquoted expansion contributes no positional filters,
so the workflow executes `npx playwright test --project=chromium`.
[`playwright.config.ts`](../../playwright.config.ts) sets `testDir: './e2e'`
and no `testMatch` or `testIgnore`; Playwright therefore discovers all 33
files. The 100 re-admitted tests are:

- `visual.spec.ts`: 66;
- `visual-baseline-thumbnails.spec.ts`: 18;
- `workout-plan-desktop-contract.spec.ts`: 16.

Those three require the visual seed, while `full-e2e` uses the functional,
user-state-wiped seed.

### Green Gate-0 characterization and intended-red evidence

[`tests/test_playwright_runner_contracts.py`](../../tests/test_playwright_runner_contracts.py)
now extends its existing local/CI visual-seed equivalence test. It applies the
actual workflow ERE to every real spec and requires the selected set to equal
the inventory minus the already-pinned exact visual-seed group. It also keeps
`visual-field-separator.spec.ts` on the functional side. This is deliberately
labeled a current-inventory characterization: it does not bless the unanchored
ERE or claim empty selection is safe.

The intended Gate-1 enforcement is retained at the ignored path:

```text
artifacts/deepgate-robustness-gate0/intended-red/
  test_full_e2e_selection_intended.py
```

Gate-0 execution result:

```text
4 failed, 1 passed
- representative unrelated names are falsely excluded
- no explicit fail-closed empty-selection guard exists
- the selector still ends in the status-masking `| tr`
- Playwright receives an unquoted scalar rather than a quoted argument array
```

The passing case is the vacuity floor: exactly one selector and one Playwright
invocation exist, so the red properties are not assertions over a missing step.

The file is intentionally not staged, so the committed suite remains green.

## Echoed shell source versus emitted dirt

GitHub Actions echoes a `run:` script before executing it. Consequently even a
clean log contains the literal source lines:

```text
CHANGED="$(git status --porcelain -- e2e/__screenshots__)"
echo "$CHANGED"
echo "a compare run wrote to e2e/__screenshots__; ..."
```

The diagnostic phrase's mere presence is not evidence that the branch ran.
A dirty run emits a separate runtime porcelain record after the source block,
for example:

```text
?? e2e/__screenshots__/linux/.../new.png
 M e2e/__screenshots__/linux/.../existing.png
```

Valid clean evidence is the guard step's `success` conclusion plus no emitted
porcelain screenshot path after the echoed source. In flaky-success run
`32688747703`, the diagnostic source appears once, the guard succeeds, and no
porcelain path is emitted.

## Artifact expectations

These are the existing semantics to preserve in Gate 1:

| Outcome | Guard | Upload steps | Retrievable result |
|---|---|---|---|
| Clean compare success | runs and succeeds | generated-baseline and failure-report uploads skip | no visual artifact; observed run `31993105305`, artifact count 0 |
| Flaky compare success | runs and succeeds if the tree is clean | `failure()` is false, so both uploads skip | no retry actual/diff/trace/video survives; observed run `32688747703`, artifact count 0 despite an 11,392-pixel first-attempt failure |
| Terminal compare failure | still runs because of `always()`; may succeed on a clean tree or fail with emitted paths on dirt | generated-baseline upload skips; failure-report upload runs | `visual-linux-report` from `artifacts/playwright` when files exist; observed run `31745901088`, one 69,887,362-byte artifact (now expired) |

A dirty baseline under `e2e/__screenshots__` is outside the
`artifacts/playwright` upload path. Its porcelain path and diagnostic survive in
the log, but the newly written PNG is not promised by the current artifact
contract. Retaining flaky-success diagnostics would be a separate behavior and
policy change, not part of this robustness repair.

## Independent review record

Four read-only reviewers worked independently and edited no files:

1. **Shell/workflow semantics:** reproduced the masked status, upstream-error
   masking, unanchored false exclusions, and current 33/30 arithmetic.
2. **Playwright selection:** independently collected 586/30 with explicit paths
   and 686/33 with no paths, and confirmed the three re-admitted files total 100
   tests.
3. **Baseline-write contract:** traced the fail-safe output/control flow,
   current Git/ignore caveats, source/runtime distinction, and the three
   artifact outcomes.
4. **Test strength:** identified the step-order/duplicate-name mutation hole;
   the committed green contract was tightened to require unique ordered steps
   and unique ordered guard primitives.

No reviewer ran or dispatched a workflow, generated a baseline, or changed the
worktree.

## Verification

Executed in the isolated worktree at the Gate-0 base plus this diff:

```text
pytest tests/test_playwright_runner_contracts.py
       tests/test_release_workflow_contracts.py -q
  PASS

python scripts/generate_test_inventory.py --check
  Test inventory is up to date.

pytest tests/ -q
  PASS (standard platform skips only)

npx tsc --noEmit
  exit 0

npx pyright@1.1.410 --outputjson
python scripts/pyright_baseline_diff.py ...
  0 current diagnostics; 0 net-new; baseline gate PASS
```

The green assertions were folded into existing pytest nodes, so the committed
inventory legitimately remains unchanged. The separate ignored intended-red
run remains `4 failed, 1 passed` and is not part of CI collection.
