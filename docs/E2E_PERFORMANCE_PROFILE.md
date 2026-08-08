# E2E performance profile

*Where Playwright wall-clock actually goes, measured. This document ranks
opportunities; it does not authorize any of them. [`DECISIONS.md`](DECISIONS.md)
**ADR-005** remains binding: an E2E performance change requires timing evidence
for that specific change, produced from the group the decision applies to.*

## Scope and source

Everything below is measured on the **local functional benchmark group** — the
25 CI-required functional specs, 477 tests — from the supported N=1 reference
run, `artifacts/shards/20260808-203801-n1/shard-1/report.json`:

```bash
.venv/Scripts/python.exe scripts/playwright_timing_report.py \
  --json artifacts/shards/20260808-203801-n1/shard-1/report.json --shards 1 --top 12
```

**719.0s launcher wall clock; 711.3s of testcase time; 477/477 passed.**

This is the *local* group. It is not the CI functional gate's wall-clock and
must not be used to argue for a CI shard count — ADR-005's scope rule.

Local parallelism is not an option here: same-machine N>1 is rejected by
evidence (**ADR-006**). Local wall-clock can only improve by making the work
smaller.

## There is no overhead to reclaim — the time is inside the tests

| | |
|---|---|
| first test start → last test end | 714.7s |
| sum of test durations | 711.3s |
| unattributed gap between tests | **3.4s (0.5%)** |
| largest single inter-test gap | 0.07s |

Fixture setup, worker startup and teardown are already negligible. Every
opportunity below is inside a test body.

## The five slowest specs

| Spec | tests | sec | %suite | s/test |
|---|---:|---:|---:|---:|
| `ui-hardening.spec.ts` | 37 | 78.6 | 11.1% | 2.12 |
| `superset-edge-cases.spec.ts` | 12 | 66.4 | 9.3% | **5.53** |
| `validation-boundary.spec.ts` | 23 | 55.3 | 7.8% | 2.40 |
| `workout-log.spec.ts` | 23 | 54.2 | 7.6% | 2.36 |
| `workout-plan.spec.ts` | 35 | 47.7 | 6.7% | 1.36 |

Suite mean is 1.49s/test. Two different shapes hide in that table:
`superset-edge-cases` is expensive **per test** (5.53s, and 8 of the suite's 12
slowest individual tests), while `validation-boundary` is a flat ~2.4s for all
23 tests — a range of 2.24s to 2.69s. That flatness is the signature of a fixed
per-test cost, not of expensive test bodies, and it is what finding 1 is about.

## Finding 1 — `networkidle` is ~30% of the suite, and most of it is dead time

**Measured cost.** `waitForPageReady()` in `e2e/fixtures.ts` is
`domcontentloaded` + `networkidle`. It executes an estimated **435 times** per
suite run. Two independent measurements of its tail:

| Measurement | Result |
|---|---|
| Standalone probe, cold context, 4 routes | 471–496ms (p50 **488ms**, p90 497ms) |
| Instrumented in-suite run, `validation-boundary`, 23 samples | mean **538ms**, min 524, max 547, total 12.4s |
| The `domcontentloaded` half of the same call | mean **0.4ms** — already satisfied |

At the conservative 490ms that is **213.1s of 711.3s — 30.0%**. At the in-suite
538ms it is 234.0s (32.9%). The 435 count is itself conservative: see *Oracle
controls* below.

For scale, ADR-005 measured every hard wait in the suite at 61.3s / 8.5%. This
is roughly **3.5× larger**, and it was invisible to that review because the
hard-wait inventory counts `waitForTimeout`, not `networkidle`.

**Causal mechanism.** `page.goto()` already waits for `load`, so
`waitForPageReady` contributes almost nothing except the `networkidle` wait, and
`networkidle` is defined as *500ms with no network activity*. On an absolute
timeline for one cold-context navigation to `/workout_plan` (72 requests: 68
same-origin, 4 external):

```
  load fired at             994ms
  last request finished    1006ms   <- the app's own post-load fetches
  networkidle resolved at  1547ms
  idle window actually paid  540ms after the last request
```

The last requests are the page's own post-load XHRs — `/get_all_exercises`
(twice), `/get_workout_plan`, `/api/volume_progress`, a bodymap SVG — finishing
about 12ms after `load`. So `networkidle` is doing **two** jobs: it waits for the
app's post-load fetches to settle (load-bearing, ~12ms) and then it waits out a
500ms quiet window (pure dead time).

**Expected saving.** Keeping the guarantee and dropping the window: roughly
500ms × 435 ≈ **218s**, taking the N=1 reference from 719.0s to about 500s.

**Coverage / determinism risk — real, and already demonstrated.** This must not
be done by deleting `networkidle`. A before/after experiment on
`validation-boundary.spec.ts` (server and DB isolated on port 5321, no live data
touched):

| Run | `waitForPageReady` body | Result | Wall (as reported) | Measured tail |
|---|---|---|---|---|
| control | `domcontentloaded` + `networkidle` | **23 passed** | 1.1m | 12.4s |
| variant | `domcontentloaded` + `load` | **22 passed, 1 failed** | 50.3s | 0.0s |

The variant is roughly 15s faster — consistent with the 12.4s of tail it removed
— and breaks `Empty Value Validation › rejects empty
sets field`, which asserts that clicking Add with an empty `#sets` sends no
`/add_exercise` request. Without the tail, the click lands before the page's
post-load initialization has settled and the request goes out. `networkidle` is
accidentally serving as the app-ready signal, and the app exposes no explicit
one. That is the whole risk in one test: the saving is real, and the naive form
of the change is wrong.

**Smallest targeted next experiment.** Give one page an explicit readiness
signal, convert `validation-boundary.spec.ts` alone to wait on it, and re-run
that spec 5× (the repeat-probe precedent used for the A10 promotions) against
the control numbers above. Only if that is green for all 23 tests on all 5
repeats does converting a second spec become worth pricing. `waitForPageReady`
is shared by 22 specs and the correct observable differs per page, so a
suite-wide rewrite is not the unit of work.

## Finding 2 — `superset-edge-cases.spec.ts` hard waits — **SHIPPED 2026-08-08**

Owner-approved and implemented. Seven `linkBtn.click()` + `waitForTimeout(1000)`
sites now call a `linkSelectedExercises()` helper that waits for
`API_ENDPOINTS.SUPERSET_LINK` **and** for the resulting row re-render.

**Why the POST alone is not the observable.** `handleLinkSuperset()` in
`static/js/modules/workout-plan-supersets.js` awaits `/api/superset/link` and
*then* calls `refreshPlan()`, so the table re-renders on a second round trip.
Waiting only for the POST would have raced that re-render — the 1000ms sleep was
covering both hops, so the helper waits for both.

**Measured, same isolated server and DB (port 5331), wall clock:**

| | runs | median | range |
|---|---|---|---|
| before | 3 | **66.8s** | 65.2–67.0s |
| after | 5 | **60.7s** | 59.2–62.8s |

**6.1s saved (9.2%), 12/12 passing in all eight runs, zero retries, zero flakes,
zero skips.** The suite hard-wait total drops 92 → 85, and this file 17 → 10.

**The one semantic delta, stated rather than buried.** A blind sleep never
fails; an observable wait does. Where the link silently failed before, the test
used to continue and could still pass on a weak later assertion — it now fails at
the wait. That is strictly stronger, not weaker, but it is a change and is
recorded here as one.

### Guard inventory — reported, deliberately NOT changed

The `if (await linkBtn.isEnabled())` guards were left exactly as they were, per
the packet's scope. Inventorying them found the concern is much wider than those
seven, so it is recorded here as its own finding rather than folded into a
performance packet:

- **27 runtime conditionals** in the file, 7 of them the `linkBtn.isEnabled()`
  guards.
- **10 of the 12 tests place every one of their assertions inside at least one
  runtime conditional**, so each can report a pass having executed no assertion
  at all. Only `successfully links exactly 2 exercises` and `deleting a linked
  exercise clears the partner superset group` assert unconditionally.
- **4 `.catch(() => …)` fallbacks resolve a failed query to the value the
  assertion wants** — `linkBtn.isDisabled().catch(() => true)` twice, and the
  `unlinkBtn` visible/enabled pair. A locator that breaks outright reads as a
  pass.

This is a coverage question, not a performance one, and it needs its own owner
decision: these tests can go green while verifying nothing.

### What was predicted vs what happened

Kept because the gap is the useful part, not to preserve the original prose.

| | predicted | actual |
|---|---|---|
| link-click sleeps | 5 | **7** (the analysis miscounted from a `-B1/-A1` grep) |
| recoverable | 8–10s | **6.1s** |
| observable needed | the POST | the POST **and** the `refreshPlan()` re-render |

The saving came in under the estimate because the estimate priced the sleeps
against a bare API round trip and ignored the second hop the helper must now
wait for. The spec's other 5.3s of hard waits (300ms/500ms/1500ms, guarding
checkbox, delete, unlink and replace flows) were out of this packet's scope and
remain.

## Finding 3 — the rest of the hard-wait debt is already correctly ruled on

Runtime-executed hard-wait delay across the group is **60.3s = 8.5%**,
independently reproducing ADR-005's published 61.3s / 8.5%. Distribution after
`superset-edge-cases`:

| Spec | sec | runtime wait | % of spec |
|---|---:|---:|---:|
| `error-handling.spec.ts` | 38.4 | 13.2 | 34.4% |
| `volume-splitter.spec.ts` | 39.4 | 10.0 | 25.4% |
| `progression.spec.ts` | 33.4 | 7.5 | 22.4% |
| `exercise-interactions.spec.ts` | 35.0 | 5.4 | 15.4% |
| `empty-states.spec.ts` | 24.9 | 4.8 | 19.3% |

ADR-005's ruling stands: no blanket rewrite. Each of these is eligible only
individually, on the same two conditions finding 2 satisfies.

## Finding 4 — two observations that are out of bounds to act on

Recorded because they were measured, not as proposals. Both are production
behavior and would need an explicit owner decision.

- **Every navigation depends on the public internet.** Four resources are
  fetched from external CDNs on each page load: Bootstrap (jsdelivr), Sortable
  (cdnjs), and the Inter stylesheet plus its woff2 (Google Fonts / gstatic).
  Local E2E readiness is therefore gated on external latency and availability.
  The repository already vendors FontAwesome under `static/vendor/`, so the
  inconsistency is visible, but changing it changes what the application ships.
- **`/get_all_exercises` is requested twice per navigation** to `/workout_plan`.

## What the profile says *not* to do

- **Do not split `api-integration.spec.ts`.** Re-confirmed at **2.4s, 0.3%** of
  the group across 57 tests — the cheapest spec per test in the suite by an order
  of magnitude (0.04s/test). ADR-005 settled this.
- **Do not remove hard waits mechanically.** Finding 3.
- **Do not shard locally.** ADR-006.
- **Do not chase fixture or worker overhead.** It is 3.4s total.

## Oracle controls

Per [`.claude/rules/verification.md`](../.claude/rules/verification.md), the
counting model is not evidence until it passes a control. It passed two:

1. **Ground truth.** The model predicted 21 `waitForPageReady` executions for
   `validation-boundary.spec.ts`; an instrumented run of that spec logged **23**.
   The model **under-reports by ~9%**, so every figure derived from it in
   finding 1 is a floor, not a ceiling.
2. **Independent cross-check.** Applied to `waitForTimeout` instead, the same
   model returns 60.3s / 8.5%, reproducing ADR-005's separately measured
   61.3s / 8.5%.

Both directions matter: the first says the headline number is conservative, the
second says the attribution logic reproduces a figure it did not derive.

## Raw evidence

Under `artifacts/` (gitignored), not in this document:

| Path | What |
|---|---|
| `artifacts/shards/20260808-203801-n1/` | The supported N=1 reference run |
| `artifacts/probe/control_run.txt` | Instrumented `validation-boundary` control, 23 passed |
| `artifacts/probe/variant_run.txt` | Same spec without `networkidle`, 22 passed / 1 failed |
| `artifacts/probe/readiness_probe.mjs` | Per-strategy navigation timing probe |
| `artifacts/probe/request_census.mjs` | Absolute-timeline request census |
| `artifacts/controlled/`, `artifacts/shards/20260808-213418-n2/` | ADR-006 sharding evidence |
