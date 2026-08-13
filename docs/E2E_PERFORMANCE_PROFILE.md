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

**The signal.** `data-workout-controls-busy` on `<html>`, present while a profile
estimate is in flight and may still write the six Workout Controls. Set
**synchronously before the first `await`** (so a caller that has just dispatched
the change event already observes it) and cleared in **`finally`** (so a rejected
estimate cannot strand it). It is display-only and never read by application
code — it makes existing internal state observable and changes no behavior.

**It is a boolean, not a counter — and the distinction is a real limitation, not
a quibble.** Set and clear are a plain `setAttribute` / `removeAttribute` pair,
with no refcount and no request-generation token. If two estimates ever overlap,
the first response to settle runs the `finally` and clears the marker while the
second is still in flight, and a waiter would be released early. The signal is
therefore **exact only for serialized estimates**, which is what the converted
paths do: each drives at most one selection at a time and awaits it. Treat it as
a sound observable for those paths, not as a general concurrency primitive.
Overlapping estimates are a **latent limitation, recorded and deliberately not
fixed here** — `applyUserProfileEstimateForSelectedExercise()` is dispatched
un-awaited from the `#exercise` change handler (`workout-plan.js`), so a fast
enough double selection could in principle overlap. Making the marker exact under
concurrency means refcounting or request-generation plus cancellation, which is a
production behavior change and a separate owner decision. Any future spec that
deliberately fires concurrent estimates must not assume this marker covers it.

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
exercise *selection*.

**The safety basis is the position of the converted sites, not the behavior of
the selection helpers.** All 26 converted sites sit immediately after a
`page.goto()` or a `page.reload()`, where no selection has happened and so no
estimate is in flight. The packet is a strict 1:1 substitution at those sites —
26 `waitForPageReady` lines removed, 26 `waitForWorkoutPlanReady` lines added,
and no other `await` deleted — so **no post-selection wait was converted or
removed anywhere in this spec.** Sites that do need the post-selection guarantee
already had their own and still have it: `selectExerciseWithEstimate()` brackets
the selection with `page.waitForResponse(ESTIMATE_API)`.

**Out of scope: a pre-existing post-selection race.** `selectFirstExercise()`
waits on a `waitForFunction` *before* selecting — for the `#exercise` dropdown to
be populated — and returns as soon as `selectOption()` resolves. It does **not**
wait for the estimate the selection fires. So the two TS-3/TS-4 tests that call
`selectFirstExercise(page)` and then assert on or write the six controls are
racing that response. That race predates this packet, is unchanged by it, and is
not introduced or repaired here; closing it means adding a post-selection wait at
those two call sites, which is a behavior change to the assertions and a separate
packet.

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

*(Superseded by packet 7 below, which repaired the helper instead of working
around it. The diagnosis above stayed correct — the fix was simply out of that
packet's scope.)*

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

### The `exercise-interactions` helper repair — **DONE 2026-08-09 (packet 7)**

Packet 6 retained seven sites here because of a **test-design defect, not a
property of the page**: `ensureRoutineHasExercises()` opened with an unguarded
`rowLocator.count()`, and that read decided whether the helper seeded. This
packet repaired the helper instead of working around it. Test-only — no
production JS, template, route or API touched, and `waitForPageReady` itself is
unchanged for the specs that still use it.

**What makes it deterministic now.** The helper has two halves, both awaited:

1. `seedRoutineToMinimum()` decides from `/get_workout_plan` — an awaited HTTP
   response says the same thing however fast the browser is. It counts the rows
   already in the routine there, excludes their names from the add candidates,
   and returns how many rows it actually added. So an empty routine is seeded
   from zero, a partially seeded one is topped up rather than duplicated, and a
   full one is left alone.
2. The helper reloads **only** when it added rows — otherwise the loaded page's
   own `fetchWorkoutPlan()` is already fetching what is there — and then polls
   until the table has rendered at least `minimumCount` rows *of the test
   routine*: `tr[data-exercise-id][data-routine="…"]`, both stamped by
   `updateWorkoutPlanTable()` on every row it builds, so neither a placeholder
   nor another routine's row can satisfy it.

The seeding decision no longer reads asynchronous state at all, and the render
`networkidle` had been covering by accident is now waited for explicitly and by
name. Nothing else in the file depended on it, so **all seven retained sites /
21 calls converted; `networkidle` executions in this spec go 21 → 0.**

**Realized inventory, instrumented rather than counted — and it is DB-state
dependent.** Packet 6 recorded 21 retained calls. Instrumenting
`waitForPageReady` directly measured **21 executions (11.6s, mean 551ms) against
the DB state the timing runs used, and 23 (13.0s, mean 564ms) against a freshly
seeded one**. The difference is real, not noise: 19 calls come from the six
`beforeEach` blocks and the rest from the helper's post-seed reload, which fires
once per seeding event — and the delete tests remove rows, so how many seeding
events a run needs depends on what the previous run left behind. The converted
side measures **0** `waitForPageReady` executions and 23
`waitForWorkoutPlanReady` executions costing **0.65s in total** (mean 28ms) —
those 23 being the 21 converted here plus the 2 the `Exercise Filter
Application` block already had.

**Measured, same isolated server / DB / session (port 5336), same reporter and
`workers=1`, control first. Wall clock, as in every table above:**

| | runs | median | range | result |
|---|---|---|---|---|
| control (`fc54330`) | 3 | **32.8s** | 32.8–33.0s | 21/21 |
| converted | 5 | **22.8s** | 22.6–23.0s | **21/21 × 5** |

**10.0s saved (30.5%), zero retries, flakes or skips across all 8 runs.** The
largest proportional win of the rollout, and the arithmetic closes: 11.6s of
`networkidle` removed, 0.65s of marker waits and one extra `/get_workout_plan`
round trip per invocation added back.

*Basis, since the two numbers a reader can find will differ: these are
launcher-process elapsed times, which run ~0.6–0.7s above the reporter's own
`N passed (Xs)` line in the saved run logs (32.1–32.3s control, 21.9–22.4s
converted) because the reporter starts counting after process and browser
startup. Control and converted are measured the same way, so the comparison is
on one consistent basis and the conclusion is unchanged: 10.0s on the launcher
basis, 10.1s on the reporter's.*

**Realized yield: 0.48s per converted call** — near the top of the 0.19–0.55s
band, for the same reason packet 6's converted half was: the tail was dead time
that no following work overlapped.

**Assertions went up, not down.** 25 → 29 assertion sites (+4), all of them in
setup: `/get_workout_plan` and `/get_all_exercises` must succeed, seeding must
reach the minimum, and the table must render it. Nothing was removed or
weakened; 21 tests before and after; hard waits unchanged at **7 sites /
5100ms**. A helper that used to silently skip seeding now fails loudly if its
precondition cannot be met.

**The one semantic delta, stated rather than buried.** The old early-return read
`#workout_plan_table_body tr` — *every* row, whatever routine it belonged to —
so in a full-suite run, where earlier specs leave rows behind, it could return
having seeded nothing into the test routine and hand the tests another routine's
rows. Both the new decision and the new wait are scoped to `TEST_ROUTINE`, so
the helper now delivers what its name says. That is strictly stronger, and it
can mean *more* seeding than before in a shared-DB run — which is why it was
verified there and not only in isolation: the full functional gate (every spec
bar the two snapshot specs and `workout-plan-desktop-contract`) passed
**508/508**, with pytest at 2614 passed / 2 skipped and the test inventory
unchanged.

### Cumulative

| Spec | calls | saved | per call |
|---|---:|---:|---:|
| `validation-boundary` | 23 | 9.1s | 0.40s |
| `workout-plan` | 17 | 3.3s | 0.19s |
| `ui-hardening` | 71 | 18.6s | 0.26s |
| `superset-edge-cases` + `exercise-interactions` | 15 | 8.2s | 0.55s |
| `exercise-interactions` (helper repair) | 21 | 10.0s | 0.48s |
| **total** | **147** | **49.2s** | **0.33s** |

The independently measured per-spec savings sum to **49.2s**, equivalent to
**6.9%** of the 711.3s pre-work local group. The full group has not been re-timed
after the rollout. Test counts, hard-wait counts, and production behavior stayed
unchanged throughout, and assertion counts were unchanged or higher.

### The workout-plan rollout is closed

Every spec the marker was authorized for has now been converted and measured.
What is still on `networkidle` is retained deliberately and recorded above:

| Site | Why it stays |
|---|---|
| `workout-plan.spec.ts` › `Workout Plan Page` (15 tests) | Its tests read the plan table without waiting for the `fetchWorkoutPlan()` that fills it. The helper repair above is not transferable — there is no shared helper to fix, so this is 15 individual per-test waits, a different change. |
| `workout-plan.spec.ts` › `§4 thumbnails` (4 tests) | They inject rows with `updateWorkoutPlanTable()`; the real fetch must have landed or it repaints over the mock. |
| `ui-hardening.spec.ts` › `Workout Log Modal Keyboard & Focus` (4 calls) | Runs on `/workout_log`, where the workout-plan marker never appears. |

The remaining `networkidle` traffic is on other pages. **Going further needs a
per-page readiness design, which is a production change and a separate owner
decision — this packet does not propose one**, and no page-specific observable
should be invented ad hoc in a test to avoid asking.

### Rollout to Volume Splitter — **Packet C, measured 2026-08-13**

The separate owner decision was granted for a measurement-first, one-page
packet. A post-local-first census found two eligible non-Workout-Plan pages with
one un-awaited initialization fetch. Volume Splitter was the clear first slice:
**32 runtime waits / 16.27–16.33s of instrumented `networkidle` tail per spec
run**, versus Body Composition's 9 relevant waits / about 4.63s.

`initializeVolumeSplitter()` now wraps only its initial
`GET /api/volume_history` hydration with `data-volume-history-busy` on `<html>`:
set synchronously before the request is awaited and removed in `finally` after
the existing renderer (or handled error state) completes.
`waitForVolumeSplitterReady()` waits for `load` plus absence of that attribute.
The shared `waitForPageReady()` is unchanged.

**Initialization-only is load-bearing scope, not naming polish.** The shared
`loadVolumeHistory()` also runs after save, delete, and active-plan actions.
Putting the boolean marker there would make page readiness describe user
actions and become inexact if refreshes overlap. Those later calls remain
unmarked and keep their existing response/DOM observables.

Measured on the same fresh post-Packet-A worktree, same Chromium project and
isolated E2E seed; control first, then converted. The comparison excludes the
new blocked-request oracle from the converted timing so both sides run the same
original 32 tests:

| | runs | launcher median | range | result |
|---|---:|---:|---:|---:|
| control (`networkidle`) | 3 | **41.06s** | 40.89–41.26s | 32/32 |
| converted (exact same 32 tests) | 5 | **30.35s** | 29.82–31.18s | **32/32 × 5** |

**10.70s saved (26.1%), 0.33s per converted call.** The precise helper itself
spent only **0.37–0.40s total** across all 32 calls (mean 11.6–12.4ms), compared
with the control's 16.27–16.33s inside `networkidle`; the rest of that removed
tail had overlapped useful test work, which is why launcher savings are smaller
than the raw wait total.

The complete 33-test spec, including a live oracle that stalls
`/api/volume_history`, observes the marker while the request is in flight,
releases it, and requires history rows to be rendered when the helper returns,
passed **33/33 × 5** (launcher
30.51–32.27s), with zero retries, flakes, or skips. Nine source contracts pin
attribute identity, set-before-await, `finally`, the initialization call edge,
action-refresh exclusion, helper predicate/diagnostic/no-`networkidle`, generic
helper preservation, and exact three-site conversion. An **8/8 mutation
battery** rejected each silent-failure variant.

Only `volume-splitter.spec.ts`'s three static sites / 32 measured calls are
converted. Generic multi-route loops, the deliberate direct waits, visual
capture readiness, and Body Composition remain untouched. Full requirements,
council dispositions, and raw-evidence routing:
[`page_readiness/PLANNING.md`](page_readiness/PLANNING.md).

### Rollout to Body Composition — **the census's second and last candidate**

The other eligible page from the same census, taken as its own slice because
the owner requires one page/flow at a time. `data-body-composition-history-busy`
wraps only the initial `GET /api/body_composition/snapshots`; the save and
delete refreshes call the same loader and stay unmarked.

Six of seven sites converted. The seventh is the navbar test's `page.goto('/')`
— the home page has no readiness signal, so it keeps `waitForPageReady()`, and
a source contract pins *which* site that is, because the counts alone cannot
tell a correct split from a swapped one.

| | runs | launcher median | range | result |
|---|---|---:|---:|---:|
| control (`networkidle`) | 3 | **11.83s** | 11.71–11.84s | 9/9 |
| converted, identical 9 tests | 5 | **8.16s** | 8.14–8.18s | **9/9 × 5** |

**3.67s saved (31.0%)**, zero retries, flakes or skips. The full converted spec
including its new readiness oracle runs at 8.28s median.

**Two corrections this slice made to the pattern, both worth carrying:**

1. **`expect.poll(() => readySettled).toBe(false)` proves nothing on its own.**
   `expect.poll` succeeds on its *first satisfying observation*, so it passes
   the moment it sees `false` — which is also what it sees when the helper is
   one microtask from resolving. It cannot tell "blocked" from "not settled
   yet". This slice instead yields across two full CDP round trips and then
   reads the flag once, synchronously.

   **Whether that makes the whole oracle vacuous depends on what comes after
   it**, and the two slices differ — measured, not assumed:

   | Oracle | no-op helper (`await Promise.resolve()`) |
   |---|---|
   | Slice 1, Volume Splitter (as merged) | **rejected** |
   | Slice 2 first draft, Body Composition | **survived** |

   Slice 1 is saved by a *non-retrying* `#history-body tr` count after
   `await ready`: with a no-op helper the render has not happened, the count is
   0, and the test fails. Slice 2's first draft put an auto-retrying
   `toBeHidden()` first, which absorbed exactly that signal.

   So the transferable rule is not "`expect.poll` makes a test vacuous" — it is
   **put the non-retrying reads immediately after the wait, and never rely on
   `expect.poll` as the thing that proves a wait blocked**.
2. **Non-retrying reads must come first.** An auto-retrying matcher placed
   before them absorbs "the render completed shortly after the helper
   returned", which is the exact failure being tested.

**Mutation attribution matters.** The lost-wakeup mutation is owned by the
*source-order contract*, not the oracle: the oracle synchronises on the request
starting and `toHaveAttribute` auto-retries, so a marker appearing a tick late
still satisfies it. **12/12** mutations rejected once each was pointed at the
gate that actually owns it.

**Packet C is now exhausted.** `/progression` and `/workout_log` issue zero
requests after `load` — there is nothing for a marker to represent.
`/user_profile`'s init fetch is not the last request: thirty asset requests
follow it, the last at `load + 53ms`, so a marker there would release early and
be strictly weaker than `networkidle`. Everything else is a deliberate wait, a
capture wait, or the generic helper.

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
defects, fixed here; one was a product defect, reported here and fixed later.

1. **PRODUCT DEFECT — the Unlink button is visible when it should not be. FIXED.**
   `updateSupersetActionButtons()` correctly sets `display: none` inline for a
   single non-superset selection, but three `!important` rules in
   `components.css` (`button.btn…`, and two `.btn-calm-danger` rules) outrank the
   inline style, so the computed display stays `inline-flex`. A user selecting one
   ordinary exercise sees an Unlink button. It is cosmetic, not corrupting:
   `handleUnlinkSuperset()` guards the action and refuses with a toast. The test
   therefore asserts the app's own decision (the inline style) *and* that
   invoking the button mutates nothing — `toBeHidden()` would fail today.

   Fixed since: both buttons toggle the `hidden` attribute, and
   `#superset-actions .btn[hidden] { display: none !important; }` in
   `pages-workout-plan.css` outweighs all three component rules. The test now
   asserts the rendered state (`toBeHidden()`) rather than the inline style —
   asserting intent is exactly what let this through — and exercises the guard
   with `dispatchEvent('click')`, since the button is no longer clickable. The
   guard itself is unchanged.
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

   > **RESOLVED 2026-08-13 — the owner ruled that it clears, and it now does.**
   > The test is renamed back to
   > `changing the routine day clears a transient superset selection`. Read the
   > paragraph above as the record of what was true when written.


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

## Finding 4 — two observations that were out of bounds to act on

> **Both are now closed, and the first one undercounted.** `/get_all_exercises`
> was fixed by **#316** (`9794676`). The external-CDN dependency was closed by
> the local-first assets packet, which vendored every remaining runtime asset —
> **but the census below found four resources across three hosts, and the real
> figure was nine elements across five.** It measured `/workout_plan` and read
> `base.html`; it never covered `/progression` (flatpickr, jsdelivr, on an
> *unpinned* URL) or `/volume_splitter` (Popper and tippy.js, both on
> `unpkg.com` — a host this finding does not name at all).
>
> Two consequences worth keeping: readiness timing no longer depends on
> external latency at all, so `networkidle` settles earlier on every page; and
> `scripts/css_audit/runtime_probe.mjs`'s network-pinning layer (its
> `jsdelivrRequested` / `googleFontsOk` summary fields) is now a permanent
> no-op — a future audit must not read `googleFontsOk: false` as a regression.
> *Original text follows, as the record of what was measured on 2026-08-09.*

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
