# Volume Splitter initial-history readiness — Packet C

*Owner-approved 2026-08-13 (Session 10 residual program, Packet C). Gate 0 is
granted by the authorization text; Gate 1 is pre-approved for the smallest
council-reviewed plan that stays inside the locked behavior below.*

Closes the highest-value eligible slice of MASTER_HANDOVER's 2026-08-09
*Open and owner-gated* item 3: readiness observability on a non-Workout-Plan
page.

---

## Section 0 — Requirements

### Locked owner decisions

1. Replace accidental `networkidle` waits only when a page's real asynchronous
   initialization has one narrowly scoped production observable.
2. Work one page/flow at a time and measure before changing it.
3. Do not create a global ready switch, remove waits that protect real work,
   convert visual capture waits, change API/calculation semantics, or inflate a
   timeout.
4. Stop successfully on evidence when no remaining candidate satisfies those
   conditions.

### Candidate census

The direct `networkidle` sites are ineligible or deliberate:

| Site | Disposition |
|---|---|
| `visual-helpers.ts` | Capture readiness; explicitly locked out |
| `exercise-catalog-fetch.spec.ts` | Deliberate: request silence makes its request count final |
| `workout-plan.spec.ts`, `ui-hardening.spec.ts` | Retained comments identify real asynchronous work |
| `progression.spec.ts` | Inside a post-save polling assertion; action completion, not page initialization |

The shared `waitForPageReady()` remains the production-facing candidate
surface. A static initialization audit found two pages with one un-awaited
initial fetch: `/volume_splitter` (`GET /api/volume_history`) and
`/body_composition` (`GET /api/body_composition/snapshots`). Other per-page API
calls are action handlers and do not define page readiness.

### Post-Packet-A measurement

Measured from fresh worktree `wt/networkidle-packet-c` at `18c7916`, which
contains local-first Packet A (`ddbec6a`). Three repetitions per candidate,
same Chromium project and isolated E2E seed:

| Candidate | Runtime waits/run | Instrumented tail/run | Tail mean | Launcher median |
|---|---:|---:|---:|---:|
| Volume Splitter | **32** | **16.27–16.33s** | 508–510ms | **41.06s** |
| Body Composition | 9 relevant (+1 Home navigation) | 4.63s relevant | 513–515ms overall | 11.98s |

Volume Splitter is the highest-value eligible flow by more than 3×. Packet C
therefore scopes itself to that page only. Raw logs live under the gitignored
`artifacts/packet-c/` directory.

### Non-goals

- No change to `/api/volume_history`, history rendering, saved plans, active
  plan behavior, calculations, database state, or user-visible UI.
- No edit to `waitForPageReady()` or any visual/capture helper.
- No conversion of generic multi-route loops merely because they sometimes
  visit `/volume_splitter`.
- Body Composition is recorded as the next smaller candidate, not bundled into
  this one-page packet.

---

## Section 1 — Plan v1

1. Wrap the initialization-only `loadVolumeHistory()` call with a named async
   lifecycle that sets `data-volume-history-busy` on `<html>` synchronously,
   awaits the existing loader, and removes the attribute in `finally`.
2. Add `waitForVolumeSplitterReady(page)` to `e2e/fixtures.ts`: wait for
   document `load`, then for that attribute to be absent, with a diagnostic
   naming the signal and its production owner. It must never fall back to
   `networkidle`.
3. Replace the three static `waitForPageReady()` sites in
   `volume-splitter.spec.ts` (32 measured runtime calls) one-for-one.
4. Add criteria-derived source contracts and a live blocked-request E2E proof.
5. Run three control timings, five converted timings, repeated stability,
   focused pytest/E2E, inventory check, and proportional regression gates.

---

## Section 2 — Council response matrix

Architecture, test-strategy, and product-risk passes reviewed Plan v1 against
the live call graph. Conservative findings are accepted below.

| # | Finding | Disposition | Plan correction |
|---|---|---|---|
| 1 | `loadVolumeHistory()` is also called after save/delete/activate. Marking the loader itself makes a navigation signal describe user actions and becomes inexact under overlap. | Accept, blocking | Mark only a new initialization wrapper; later refreshes remain unmarked. |
| 2 | A boolean marker set after invoking the request has a lost-wakeup race: the test can observe absence and return while the fetch is live. | Accept, blocking | Set synchronously before the wrapper's first `await`; pin source order and prove it with a stalled request. |
| 3 | Rejection or a synchronous throw can strand the attribute. | Accept, blocking | Removal lives in `finally`; the contract rejects cleanup in `then`/`catch`. |
| 4 | Waiting directly for the response is attach-order fragile because page initialization can fire before the test installs its listener. | Accept | The durable production state is the oracle; helper waits on the attribute after `load`. |
| 5 | Converting `waitForPageReady()` globally would weaken unrelated pages, while conditionally switching inside it would be the forbidden global fake-ready design. | Accept, blocking | Original helper stays byte-for-byte in behavior; add a page-specific helper used only by the Volume Splitter spec. |
| 6 | Static source checks alone can pass while the initializer never invokes the wrapper. | Accept | Pin the call edge and add a live test that blocks `/api/volume_history`, observes the marker, releases it, then awaits the helper. |
| 7 | The tooltip block also uses the shared setup; conversion must not release before tippy/Popper initialization. | Accept | Helper waits for `load`; synchronous tooltip binding runs in the same DOMContentLoaded initializer before the async history wait can settle. Existing tooltip assertions remain in the converted spec. |
| 8 | A bespoke timeout would change tolerated readiness and could hide a stranded marker. | Accept | Use Playwright's existing default; diagnostic enriches only the error message. |
| 9 | The progression direct wait is not a candidate: it is inside `expect.poll()` after Save Goal. | Accept | Explicitly excluded from this packet. |
| 10 | New test nodes and helper/source contracts move generated inventory. | Accept | Regenerate canonically after the last test edit and re-check after integrating current `main`. |
| 11 | One green converted run is insufficient timing evidence. | Accept | Same-machine control first (3), converted second (5), plus five-repeat stability with zero retries/flakes. |
| 12 | `MASTER_HANDOVER.md` is a shared integration surface excluded from feature packets. | Accept | Record the result in this plan, `E2E_PERFORMANCE_PROFILE.md`, and worktree-local handover; Session 10 owns canonical reconciliation. |

---

## Section 3 — Plan v2 (binding)

The production observable describes exactly one lifecycle:

```text
DOMContentLoaded
  -> initializeVolumeSplitter()
     -> loadInitialVolumeHistory()
        -> set data-volume-history-busy synchronously
        -> await existing loadVolumeHistory()
        -> remove attribute in finally
```

No later history refresh touches the marker. `waitForVolumeSplitterReady()` is
only a test consumer and waits for `load` plus absence of the exact signal.
The existing generic helper, APIs, rendered states, retries, and timeout budgets
remain unchanged.

### Acceptance gates

| Gate | Required result |
|---|---|
| Source contracts | marker order, `finally`, call edge, helper predicate/diagnostic/no-networkidle, generic-helper preservation, exact spec conversion |
| Live blocked-request proof | marker observable while request is in flight; helper returns only after release/render |
| `volume-splitter.spec.ts` | all tests green ×5, zero retry/flaky/skip |
| Timing | 3 control + 5 converted, same launcher/project/seed; report medians and realized per-call yield |
| Regression | focused pytest, Vitest, required relevant E2E/inventory checks proportional to the final diff |
| Mutations | every silent-failure property rejected and source restored byte-identically |

---

## Section 4 — Execution record

| Gate | Result |
|---|---|
| Pre-implementation red | 6/9 source contracts failed; TypeScript rejected the missing helper |
| Source contracts | **9 passed** |
| First live run | **33 passed** |
| Matched timing | control 41.06s median (3) → converted **30.35s** median (5), **−10.70s / −26.1%** |
| Precise wait cost | 0.37–0.40s total per 32 calls, versus control `networkidle` 16.27–16.33s |
| Full stability | **33/33 × 5**, 30.51–32.27s launcher range, zero retries/flakes/skips |
| Mutation battery | **8/8 rejected**; intended source contracts restored at 9/9 |
| TypeScript / Vitest | `tsc --noEmit` green; **120/120** Vitest |
| Relevant E2E union | **49/49** (`volume-progress` then `volume-splitter`) |
| Full pytest | **2,820 passed / 2 skipped** in 219.22s (serial; local venv lacks xdist) |
| Generated inventory | **631** Playwright / **498** required; **2,500** deterministic pytest nodes; hard waits unchanged at 83 |

The first combined-order E2E run was **48/49** and exposed a defect in the new
test, not production: it assumed Volume Splitter history was empty, while the
preceding `volume-progress.spec.ts` intentionally left one active plan. The
oracle was corrected to assert the actual readiness invariant — at least one
history row has already rendered when the helper returns, without assuming DB
contents — and the exact combined order then passed **49/49**. The isolated
five-repeat result used a stricter empty-seed assertion, so the readiness
lifecycle itself was exercised on every repetition; the integrated order is
the control that proved the final assertion is state-independent.
