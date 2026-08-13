# Rolling page readiness onto other pages — measured, and closed without a conversion

*Packet C of the Session-10 product-residual program, 2026-08-13, measured on
`main` at `538919a` (i.e. after the local-first assets packet removed nine
external requests per navigation, which moved every `networkidle` window).*

**Outcome: no page meets the replacement criterion. No production observable was
added and no wait was converted.** The owner's authorization anticipated this
outcome explicitly — *"stop the packet sequence when no candidate meets the
measured replacement criterion; that is a successful evidence-based close"* —
and this document is that close.

It answers MASTER_HANDOVER's 2026-08-09 *Open and owner-gated* **item 3**:

> Rolling the readiness signal onto **other pages**. … every remaining
> `networkidle` call lives on a page with no observable of its own. That needs a
> per-page readiness design.

The per-page design was attempted. The measurement says most pages have nothing
to observe.

---

## 1. Inventory of runtime `networkidle` sites

| Site | Classification | Eligible? |
|---|---|---|
| `e2e/fixtures.ts` `waitForPageReady()` | The one general readiness wait; ~24 specs, every page | the subject of this packet |
| `e2e/visual-helpers.ts` (×1 executable) | Capture wait | **No** — out of bounds by the owner's lock |
| `e2e/exercise-catalog-fetch.spec.ts` (×2) | Deliberate | **No** — the guarantee that nothing is in flight is what makes its request count final. Documented in `e2e/CLAUDE.md`. |
| `e2e/workout-plan.spec.ts` (×1) | Deliberate | **No** — its own comment records that tests in that block read the plan table without waiting for the fetch that fills it |
| `e2e/ui-hardening.spec.ts` (×1) | Deliberate | **No** — same, for the `/workout_log` modal |
| `e2e/progression.spec.ts` (×1) | Accidental | assessed below |

`waitForWorkoutPlanReady()` is already converted and is the model this packet
tried to copy: `data-workout-controls-busy`, set synchronously before the first
`await` and cleared in a `finally`.

## 2. What `networkidle` costs, and what it is waiting for

Cold context, 1440×900, median of 3 per route, seeded exactly as the E2E suite
seeds (catalog present, user state wiped — the condition these waits actually
run in).

| Route | load | last request | idle resolves | dead time | **async init after load** |
|---|---:|---:|---:|---:|---:|
| `/` | 143ms | 138ms | 651ms | 513ms | **0ms** |
| `/workout_log` | 122ms | 117ms | 632ms | 515ms | **0ms** |
| `/progression` | 124ms | 118ms | 626ms | 508ms | **0ms** |
| `/fatigue` | 126ms | 122ms | 632ms | 510ms | **0ms** |
| `/backup` | 113ms | 119ms | 632ms | 512ms | 6ms |
| `/body_composition` | 112ms | 113ms | 631ms | 514ms | 1ms |
| `/volume_splitter` | 124ms | 128ms | 640ms | 502ms | 4ms |
| `/session_summary` | 146ms | 153ms | 663ms | 510ms | 7ms |
| `/weekly_summary` | 144ms | 152ms | 656ms | 504ms | 8ms |
| `/workout_plan` | 233ms | 246ms | 754ms | 508ms | 13ms *(already converted)* |
| `/user_profile` | 196ms | 244ms | 746ms | 502ms | 34ms |

**Median dead time: 509ms per navigation.** That reproduces the 490–538ms the
performance profile measured before the CDN removal, so the local-first packet
did not change the shape — it removed four requests that were finishing inside
the same window.

The right-hand column is the one that decides eligibility. It is what a
busy/ready observable would represent.

## 3. Why each candidate fails

### `/progression` (17 calls) and `/workout_log` (11 calls) — nothing to represent

**Zero requests after `load`.** Both pages render their content server-side and
their JS initializes from the DOM; every `api.*` call in
`progression-plan.js` and `workout-log.js` is a user-action handler, not an
initializer. These are the two highest-value single pages by call count, and a
busy/ready marker on either would mark nothing.

This is the criterion failing at its root: the owner authorized replacing a wait
where *"a page's real async initialization can be represented"*. There is no
async initialization.

### `/user_profile` + `learned-calibration` (24 calls) — the marker would be weaker than the wait

The highest-value candidate overall, and the most interesting failure.

It does have an init fetch — `/api/user_profile/calibration/dashboard` at
`load + 10ms`. But it is **not the last request**. Thirty more follow it: the
reference-lift thumbnails and both bodymap SVGs, the last finishing at
`load + 53ms`.

```
load                                        196ms
/api/user_profile/calibration/dashboard     206ms   <- what a marker could see
/static/bodymaps/…/body_posterior.svg       206ms
… 30 asset requests …
/static/vendor/…/One-Legged_Cable_Kickback  249ms   <- what networkidle waits for
```

A production observable cannot know when the browser decides to fetch a lazily
referenced image. So a marker here would release ~43ms **before** `networkidle`
does, making it a strictly weaker wait — and any spec relying on those
thumbnails being present would newly race. Converting this page would trade a
correct wait for a faster wrong one.

### `/backup` (9), `/body_composition` (8), `/volume_splitter` (4) — representable, but the marker would have no red-path proof

These three are the only pages where a marker is technically faithful: one XHR,
fired at init, landing 1–6ms after `load`, nothing after it.

So the question becomes whether the wait is protecting anything. Measured
directly, by replacing `networkidle` with `load` inside `waitForPageReady()` and
running the three owning specs:

| Run | `waitForPageReady` body | Result | Wall |
|---|---|---|---|
| control | `domcontentloaded` + `networkidle` | **61 passed** | 66.0s |
| variant 1 | `domcontentloaded` + `load` | **61 passed** | 44.8s |
| variant 2 | `domcontentloaded` + `load` | **61 passed** | 45.2s |
| variant 3 | `domcontentloaded` + `load` | **61 passed** | 45.4s |
| variant 4 | `domcontentloaded` + `load` | **61 passed** | 45.4s |

**Nothing fails. Four consecutive runs, ~21s faster.**

Contrast the `/workout_plan` conversion, which is why that one was correct: the
identical experiment there **reliably red** `rejects empty sets field`, because
`networkidle` was accidentally standing in for the profile-estimate fetch that
rewrites `#sets` — it passed by 17ms in the control. The marker earned its place
by *restoring a guarantee that removal destroyed*.

Here removal destroys no guarantee. A marker would therefore be production code
whose red-path proof is impossible to construct: you cannot demonstrate it
catching a race that does not occur. That is precisely the "gate that cannot
fail" class this repository has flagged repeatedly, and adding one is worse than
adding nothing — it carries the documented boolean-not-a-counter limitation for
no coverage in return.

## 4. What was deliberately not done

**The three inert pages were not converted to `load`.** The measurement above
shows it is safe on this evidence and worth ~21s across those three specs. But
this packet's authorization is to *replace a wait with an observable*, not to
remove waits — and removal is the change the performance profile warns against
doing mechanically. It needs its own owner decision and its own ADR-005 timing
evidence per change.

The numbers above are recorded so that decision can be made without re-deriving
them. **Do not extrapolate the 21s to the whole suite** — ADR-005's scope rule
forbids exactly that, and per-page call counts differ.

## 5. Reproducing

```bash
# with the app running on 5000 against a throwaway DB
node artifacts/readiness/probe.mjs  http://127.0.0.1:5000 3   # the §2 table
node artifacts/readiness/probe2.mjs http://127.0.0.1:5000     # the §3 per-request trace
```

Both probes live under the gitignored `artifacts/`; they are measurement
instruments, not tests, and nothing in the suite depends on them.

## 6. Reopen condition

Re-run §2 if a page gains a genuine post-`load` initialization — a dashboard
fetch, a deferred render, a background sync. The criterion is the right-hand
column of that table being non-trivial **and** the last request of the
navigation being that fetch rather than an asset.
