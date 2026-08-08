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
— and breaks `Empty Value Validation › rejects empty sets field`, which asserts
that clicking Add with an empty `#sets` sends no `/add_exercise` request.
`networkidle` was standing in for an app-ready signal that did not exist, so
removing it removed a guarantee as well as the dead time. That is the whole risk
in one test: the saving is real, and the naive form of the change is wrong. The
section below identifies exactly which guarantee, and replaces it.

### The experiment was run — **PASSED 2026-08-08, scoped to one spec**

**What `networkidle` was actually protecting was not page load.** Instrumenting
`#sets`'s value setter through the failing test's exact step sequence found the
writer: selecting an exercise fires `/api/user_profile/estimate`, and its
response writes `#sets` via `setWorkoutControlValue()` in
`workout-plan-estimates.js`. In the probe the response landed at 738ms and the
test's fills at 755ms — it passed by 17ms. When the estimate lands after the
fills instead, the field is repopulated, the form is valid, and
`rejects empty sets field` fails. It is a race, not a fixed ordering, which is
why one variant run showed it and the control never did.

**The signal.** `data-workout-controls-busy` on `<html>`, present exactly while
an estimate is in flight and may still write the six Workout Controls. Set
**synchronously before the first `await`** (so a caller that has just dispatched
the change event already observes it) and cleared in **`finally`** (so a rejected
estimate cannot strand it). It is display-only and never read by application
code — it makes existing internal state observable and changes no behavior.

`waitForWorkoutPlanReady()` in `e2e/fixtures.ts` waits for `load` plus the
absence of that attribute. `validation-boundary.spec.ts` uses it in all seven
`beforeEach` hooks **and inside `selectExercise()`** — the load-time wait alone is
not enough, because the race starts at exercise selection.

**Measured, same server / DB / session (port 5332), wall clock:**

| | runs | median | range | result |
|---|---|---|---|---|
| control (`networkidle`) | 3 | **55.8s** | 55.5–56.2s | 23/23 |
| converted | 5 | **46.7s** | 44.9–53.0s | **23/23 × 5** |

**9.1s saved (16.3%), 23/23 in all five repeats, zero retries, zero flakes, zero
skips.** That is ~0.40s realized per call against the ~0.49–0.54s raw tail — the
difference is the estimate wait, which is real work `networkidle` was also doing.

The earlier 66s control in the table above was measured on a different, busier
server; the 55.8s same-conditions control supersedes it for this calculation.

**Regression surface checked**, because this changed production JS:
`ui-hardening` 37/37 (the KI-005 controls/estimate suite), `workout-plan` 35/35,
`fatigue-context` 6/6 (mocks this very endpoint), `learned-calibration` 8/8,
vitest 105/105, pytest 2614 passed / 2 skipped.

`tests/test_workout_controls_busy_signal_contracts.py` pins the three properties
that fail silently — set-before-await, cleared-in-`finally`, and no `networkidle`
fallback — plus the fact that `waitForPageReady` is left intact for the other 21
specs. It was itself controlled: moving the `setAttribute` after the first
`await` makes `test_marker_is_set_before_the_first_await` fail.

**Not rolled out further, by instruction.** `waitForPageReady` still backs 21
specs and the correct observable differs per page.

### Rollout to `workout-plan.spec.ts` — **DONE 2026-08-08 (packet 4)**

Same marker, same helper, no new production mechanism. The rollout is **partial
by design**, and the reason is the most useful thing this packet produced.

**The marker subsumes exactly one thing: the estimate write.** On a fresh `goto`
no estimate is in flight, so `waitForWorkoutPlanReady()` is a no-op there and
converting a `beforeEach` is really just *deleting* `networkidle`. That is only
safe where the spec already waits on its own observables for the page's other
post-load fetches. So each of the 7 sites was classified, not swept:

| Site | Verdict |
|---|---|
| 3 × estimate waits (`waitForResponse('/api/user_profile/estimate')`) | **Converted** — the marker subsumes these directly, and two of the three registered `waitForResponse` *after* `selectOption`, so they could miss a fast response. The marker is set synchronously in the change handler and clears only once the value is written. |
| `page.reload()` in the Issue-#17 test | **Converted** — followed by cascade `waitForFunction`s |
| `Plan Generator v1.5.0 Features` | **Converted** — server-rendered modal, auto-retrying assertions |
| `Starter plan toast severity contract` | **Converted** — same |
| `Muscle selector body map` | **Converted** — its `beforeEach` already waits for the SVG with `expect(...).toBeVisible()` |
| `Exercise reference video modal` | **Converted** — cascade `waitForFunction`s |
| `Workout Plan Page` (15 tests) | **KEPT on `networkidle`** — several tests read the plan table without waiting for the `fetchWorkoutPlan()` that fills it |
| `§4 free-exercise-db thumbnails` (4 tests) | **KEPT on `networkidle`** — these inject rows via `updateWorkoutPlanTable()`, so the real fetch must have landed or it repaints over the mock |

17 of 36 runtime calls converted; `networkidle` sites 7 → 2.

**Measured, same server / DB / session (port 5333), wall clock:**

| | runs | median | range | result |
|---|---|---|---|---|
| control | 3 | **50.7s** | 49.8–51.7s | 35/35 |
| converted | 5 | **47.4s** | 46.8–48.3s | **35/35 × 5** |

**3.3s (6.5%), zero retries, flakes or skips. Assertion count unchanged at 158
`expect(` calls in both versions** — nothing was weakened to buy the time.

### Revise the suite-wide projection downward

Finding 1 projected ~218s from 435 calls at ~500ms each. Two real conversions now
bound that properly:

Per-spec measurements live in one place — the **Cumulative** table at the end of
this document. Do not restate them here; two tables of the same numbers is how
this file would start contradicting itself.

The 500ms tail is only fully recoverable when nothing else needed that time.
Where a test then waits on a real async condition — the body-map SVG, a modal, a
cascade — part of the tail was overlapping work the new wait now performs
instead. **A realistic suite-wide figure is therefore ~85–175s, not ~218s**, and
it is spec-dependent enough that each rollout must be measured rather than
extrapolated.

Note also that the 435-call estimate the ~218s came from is itself a floor: the
counting model misses helper-internal calls, and `ui-hardening` alone measured
75 against a predicted 64. The true call total is higher, the per-call yield is
lower, and the two errors partly cancel.

### Rollout to `ui-hardening.spec.ts` — **DONE 2026-08-09 (packet 5)**

**The static model was wrong about the size of this one.** It projected 64 calls
/ ~31.4s. Instrumenting `waitForPageReady` and running the spec measured **75
executions totalling 40.7s** (mean 542ms, p50 541, range 504–581) — **51.8% of
the 78.6s spec**, not 39.9%. The model misses calls made from *helpers* rather
than from a test body or `beforeEach`; `expectDisplayedValuesPersistAcrossReload()`
alone accounts for 5. Treat the model's per-spec numbers as a floor.

**Classification — all 27 static sites / 75 runtime calls:**

| Describe | sites | runtime calls | verdict |
|---|---:|---:|---|
| Toast Stacking | 1 | 4 | Converted — touches only the server-rendered `#liveToast` |
| Form State Persistence | 3 | 5 | Converted — reload-then-`expectControls`; restore is synchronous |
| Modal Keyboard & Focus | 1 | 7 | Converted — its helper waits on Bootstrap's `shown.bs.modal` |
| **Workout Log Modal Keyboard & Focus** | **1** | **4** | **RETAINED** |
| Workout Controls Persistence (KI-005) | 13 | 33 | Converted |
| Estimate actions persist (OWNER-9) | 3 | 15 | Converted |
| Estimate state neutral (OWNER-10) | 2 | 4 | Converted |
| AR-3 restored-weight | 3 | 3 | Converted |
| **Total** | **27** | **75** | **26 sites / 71 calls converted, 1 site / 4 calls retained** |

**Why the retained one is retained** (recorded inline at the site too): that block
runs on `/workout_log`. `data-workout-controls-busy` is set by the workout-plan
estimate module, so on the log page the marker never appears and
`waitForWorkoutPlanReady()` would degrade to a bare `load`. The page fetches its
log rows after load and no assertion there waits for them, so `networkidle` is
carrying a real guarantee. Converting it would have meant inventing a second
marker, which this packet deliberately does not do.

**Why the rest are safe.** The KI-005 family is the timing-sensitive part, and
the thing it depends on is synchronous: `initializeWorkoutPlanHandlers()` runs
`beginHydration → initializeDefaultValues → restoreWorkoutControls → endHydration`
inside the `DOMContentLoaded` handler, so it has completed by `load`. The only
async writer of those six controls is the profile estimate, which fires on
exercise *selection* — no selection happens on a bare `goto`/`reload`, and where
a test does select, its own helper waits. `selectFullBodyRoutine`,
`selectFirstExercise` and `clickAddExercise` each wait on a `waitForFunction`.

**Measured, same server / DB / session (port 5334), wall clock. Control ran
FIRST so the session's rising `TIME_WAIT` biases against the converted side:**

| | runs | median | range | result |
|---|---|---|---|---|
| control | 3 | **77.7s** | 76.7–79.3s | 37/37 |
| converted | 5 | **59.1s** | 55.1–63.3s | **37/37 × 5** |

**18.6s saved (23.9%), zero retries, flakes or skips in all 8 runs. Assertion
count unchanged at 89 `expect(` calls; hard waits unchanged at 1.** The converted
runs drift upward across the five repeats (55.1 → 63.3s) purely from accumulating
`TIME_WAIT`, which is the ADR-006 mechanism showing up as slope rather than
failure.

**Realized yield: 0.26s per converted call** — squarely inside the 0.19–0.40s
band the previous two packets established, and the largest single-spec win so far.

### Rollout to `superset-edge-cases` + `exercise-interactions` — **DONE 2026-08-09 (packet 6)**

Both specs live on `/workout_plan`, so the existing marker applies with no new
mechanism. Measured first: **13 calls / 7.1s** in `superset-edge-cases` (the model
was right here) and **23 calls / 12.6s** in `exercise-interactions` (model said 20
— three more helper-internal ones). 36 calls, 19.7s.

The classification split them almost completely:

| Spec | sites | calls | converted | retained |
|---|---:|---:|---:|---:|
| `superset-edge-cases` | 7 | 13 | **7 sites / 13 calls** | 0 |
| `exercise-interactions` | 8 | 23 | **1 site / 2 calls** | **7 sites / 21 calls** |
| total | 15 | 36 | **8 sites / 15 calls** | **7 sites / 21 calls** |

**Why `exercise-interactions` is almost entirely retained.** Six of its seven
`beforeEach` blocks call `ensureRoutineHasExercises()`, which opens with an
**unguarded** `rowLocator.count()` — and that read *decides whether the helper
seeds the routine at all*. `fetchWorkoutPlan()` fills that table
asynchronously, so `networkidle` in the preceding `beforeEach` is precisely what
makes the read deterministic. The marker only tracks the profile-estimate write
and cannot substitute. Converting those would turn seeding into a coin flip:
sometimes early-return, sometimes add rows, with the row count differing per run.
The seventh retained site is the helper's own post-reload wait, kept for the same
reason. The reasoning is recorded at the helper and at the converted block.

The one converted block, `Exercise Filter Application`, never touches the plan
table: it reads the server-rendered filter dropdowns, and the test that uses the
exercise dropdown waits for it with its own `waitForFunction`.

`superset-edge-cases` converts cleanly because packet 3 already replaced its
guards with waits — `selectExerciseCheckboxes()` asserts row counts,
`linkSelectedExercises()` waits for the POST and the re-render, `addExercise()`
waits on `waitForResponse` + `toHaveCount`, and every `beforeEach` is followed by
`selectRoutine()`, which blocks on two dropdown round trips.

**Measured, same server / DB / session (port 5335), control first:**

| | runs | median | range | result |
|---|---|---|---|---|
| control | 3 | **90.1s** | 90.1–95.3s | 33/33 |
| converted | 5 | **81.9s** | 79.0–88.9s | **33/33 × 5** |

**8.2s (9.1%), zero retries, flakes or skips across all 8 runs. Assertion counts
unchanged (44 and 24); hard waits unchanged (10 and 7).**

**Realized yield: 0.55s per converted call — full recovery of the 544–550ms
tail**, the top of the observed band and the first time a rollout recovered
essentially all of it. That is the signature of calls whose following work never
overlapped the tail: in `superset-edge-cases` the `beforeEach` tail was pure dead
time before `selectRoutine()` started its own round trips.

### Cumulative

| Spec | calls | saved | per call |
|---|---:|---:|---:|
| `validation-boundary` | 23 | 9.1s | 0.40s |
| `workout-plan` | 17 | 3.3s | 0.19s |
| `ui-hardening` | 71 | 18.6s | 0.26s |
| `superset-edge-cases` + `exercise-interactions` | 15 | 8.2s | 0.55s |
| **total** | **126** | **39.2s** | **0.31s** |

39.2s off a 711.3s local group — **5.5%** — with assertion counts, hard-wait
counts and production behavior unchanged throughout.

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

### Guard inventory — **FIXED 2026-08-08 (packet 3)**

The original finding: **27 runtime conditionals**, of which **10 of 12 tests
placed every assertion inside one** (so each could report a pass having asserted
nothing), plus **4 `.catch(() => …)` fallbacks** that resolved a failed query to
the value the assertion wanted.

All are gone. Preconditions are now asserted rather than tested for
(`selectExerciseCheckboxes()` asserts the row count; `linkSelectedExercises()`
asserts the button is enabled), and the only remaining `if`s are inside
`addExercise()`'s option picker, which already ends in an assertion. 12 tests,
12 preserved. Hard waits unchanged at 10 — this packet removed no waits.

**Proof it mattered — two mutations, run against both versions of the spec:**

| Mutation | Pre-packet-3 spec | Strengthened spec |
|---|---|---|
| **M1** `superset-checkbox` class renamed (no row is selectable at all) | **11 passed / 1 failed** | **12 failed** |
| **M2** `unlink_partner_for_removal()` disabled (deleting a member leaves the partner linked) | test 4 **passed**, test 5 failed | **both fail** |

M1 is the headline: with superset selection completely broken, the old suite
reported eleven green tests. M2 isolates the weak assertion — test 4 checked
`rows <= 1`, which a still-linked partner satisfies; it now asserts the link is
gone. Both mutations were reverted and the spec re-verified.

**Verified after:** 12/12 across 5 consecutive runs, median 56.3s (55.9–57.3s),
zero retries, flakes or skips.

### What strengthening surfaced

Removing the guards exposed three things they had been hiding. Two were test
defects, fixed here; one is a product defect, reported not fixed.

1. **PRODUCT DEFECT — the Unlink button is visible when it should not be.**
   `updateSupersetActionButtons()` correctly sets `display: none` inline for a
   single non-superset selection, but three `!important` rules in
   `components.css` (`button.btn…`, and two `.btn-calm-danger` rules) outrank the
   inline style, so the computed display stays `inline-flex`. A user selecting one
   ordinary exercise sees an Unlink button. It is cosmetic, not corrupting:
   `handleUnlinkSuperset()` guards the action and refuses with a toast. The test
   therefore asserts the app's own decision (the inline style) *and* that
   invoking the button mutates nothing — `toBeHidden()` would fail today.
   **Needs an owner decision.**
2. **Test defect — the replace test used an unreplaceable exercise.** The
   catalog's first unused options are stretch variations with no muscle-group or
   equipment metadata, and `/replace_exercise` rejects those with `400
   missing_metadata`. The old test hid this behind a "did the page crash" check.
   It now adds named exercises (`bench`/`row`), gets a real `200 ok:true` swap,
   and asserts the actual invariant: the pair is never left half-linked.
   (Measured: the group survives a swap — 2 rows still linked.)
3. **Test defect — the routine-change test never changed the routine.** Its
   `differentDay` lookup matched the **`"Select Workout"` placeholder**, so it
   re-selected a non-day. With a real day the selection still does not clear: the
   routine dropdown chooses what the *Add Exercise* form targets and does not
   filter the plan table. The old name described behavior the app has never had,
   so the test was renamed to
   `changing the routine day leaves the superset action unavailable` and asserts
   that. **Whether the selection should clear on routine change is an open
   product question for the owner.**

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
| `artifacts/packet1/before-*.txt`, `after-*.txt` | Finding 2: 3 control + 5 converted runs |
| `artifacts/packet2/control-*.txt`, `run-*.txt` | Finding 1: 3 control + 5 converted runs |
| `artifacts/packet2/diagnose_sets.mjs` | The `#sets` value-setter trace that found the estimate race |
| `artifacts/packet2/affected-*.txt` | Regression runs for the production-JS change |
| `artifacts/controlled/`, `artifacts/shards/20260808-213418-n2/` | ADR-006 sharding evidence |
