# Routine-day transient superset selection — Packet B

*Owner-approved 2026-08-13 (Session 10 residual program, Packet B). Gate 0 is
granted by the authorization text; Gate 1 is pre-approved for the smallest
council-reviewed plan that stays inside the locked behavior below.*

Closes MASTER_HANDOVER's 2026-08-09 *Open and owner-gated* **item 2**:

> **Should the superset selection clear on a routine-day change?** It does not
> today; the dropdown targets the Add form, not the plan table. The test was
> renamed to match reality.

---

## Section 0 — Requirements

### Locked owner decisions (not re-openable here)

1. Changing the Add-form routine/day **clears transient checked
   superset-selection checkboxes and action/info state immediately**.
2. It must **not** unlink or alter already-persisted superset relationships in
   the plan table, and must **not** change which routine's rows are displayed.
   This is UI-state cleanup only.

### What "transient selection state" actually is

Six things, spread across two modules. Naming them all is the point of the
packet — the current code already resets *some* of them in *some* paths, which
is why the inconsistency exists.

| # | State | Owner |
|---|---|---|
| 1 | `workoutPlanState.selectedExerciseIds` (a `Set`) | `workout-plan-state.js` |
| 2 | `.superset-checkbox` `checked` flags | DOM |
| 3 | `tr.superset-selected` row highlight | DOM |
| 4 | `#superset-actions` container visibility | `updateSupersetActionButtons()` |
| 5 | `#superset-selection-info` `textContent` | `updateSupersetActionButtons()` |
| 6 | `#superset-selection-info` inline `style.color` | set, never cleared |

**None of this is persisted.** No API call, no `localStorage`, no dataset write.
Everything the server knows about a superset lives in `user_selection.superset_group`
and is only changed by `POST /api/superset/link` and `/api/superset/unlink`.

### Non-goals

- No route, schema, API-response, or calculation change.
- No change to `currentRoutineTabFilter` or to routine-tab filtering — which
  rows the plan table shows is a different control and is explicitly out of
  scope per decision 2.
- No new `addEventListener` on `#routine`. See the duplicate-listener note below.
- No CSS change.

### Calculation surface

**None.** Nothing under `utils/` is touched.

---

## Section 1 — Plan v1

> **Superseded throughout by §3, "Plan v2 (as built)".** Council review found
> the trace below incomplete (it names three entry paths; there are four), the
> six-item state table short by the button flags, and two of B5's risk rows
> guarding states that cannot occur. Where §1 and §3 disagree, §3 is what
> shipped. Kept as the record of the reasoning that went in.

### B1. Where the reset belongs — the listener trace

All three cascade dropdowns funnel into one place:

```
#routine-env    change -> handleEnvironmentChange ─┐
#routine-program change -> handleProgramChange    ─┼-> updateCompositeRoutineValue()
#routine-day     change -> handleRoutineChange    ─┘      (routine-cascade.js:254)
                                                              │
                                    writes #routine.value and dispatches ONE
                                    `change` event on it
                                                              │
                                                              v
                        handleRoutineSelection()'s listener (workout-plan.js:258)
```

`handleRoutineChange` additionally fires a `routineSelected` CustomEvent, and
`applyStatelessCascadeReset()` (on load and on `pageshow`) reaches
`updateCompositeRoutineValue()` too.

**Exactly one listener is registered on `#routine`.** There used to be two —
`app.js` called `handleRoutineSelection()` alongside
`initializeWorkoutPlanHandlers()`, which already calls it — and that duplicate
is the #316 defect that fired `/get_all_exercises` twice per navigation. It is
pinned by `e2e/exercise-catalog-fetch.spec.ts`.

**Therefore the reset hooks into the existing listener and adds no new one.**
Registering a second `change` handler for the reset would re-create #316 in
spirit: two listeners on the same field, one fetch-bearing, both fanning out
from the cascade's single dispatch.

Hooking there also means environment and program changes clear the selection
too, which is correct: all three invalidate the composite routine the Add form
targets.

### B2. Centralize the reset

Add `clearSupersetSelection()` to `workout-plan-supersets.js`, owning all six
pieces of state, and call it from three places:

1. **New:** synchronously at the top of the `#routine` `change` listener, before
   any `await`, so "immediately" is literal rather than after a fetch settles.
2. **Replacing existing partial clears:** `handleLinkSuperset` and
   `handleUnlinkSuperset` each already do `selectedExerciseIds.clear()` plus a
   checkbox sweep — items 1 and 2 only. Neither clears the row highlight (3) or
   the info colour (6). Routing both through the new function removes the
   duplication *and* fixes that latent inconsistency.

`updateWorkoutPlanTable()` (`workout-plan-table.js:310`) is deliberately left
alone: it clears the `Set` and then rebuilds `tbody.innerHTML`, so the DOM state
is recreated fresh rather than reset. Calling the new function there would be
redundant, and the existing call is not wrong.

### B3. Criteria-derived tests, written first

**Strengthen `e2e/superset-edge-cases.spec.ts:474`** — currently
`'changing the routine day leaves the superset action unavailable'`, which pins
today's behavior with `toHaveCount(1)` for checked boxes. The owner decision
inverts it. Renaming it back is the point: the name was changed *to match
reality* when the reality was the open question.

The strengthened test does four things in order:

1. Add an exercise, make a transient selection (checkbox checked).
2. Change the routine day.
3. Assert **checked count is zero** and the action is **unavailable**.
4. Assert an **already-linked pair is still linked in the plan table** — the
   half that proves this is UI-state cleanup and not a covert unlink.

Step 4 needs a linked pair that exists *before* the routine change, so the test
links two exercises first, then selects a third row transiently.

**Do not weaken the current persistence tests.** `'superset persists after page
refresh'`, `'unlink clears both exercises from superset'` and
`'deleting one exercise from superset breaks the link'` are untouched.

---

## Section 2 — Council response matrix

Three reviewers ran against Plan v1. Every finding is dispositioned; conservative
findings were accepted automatically per the packet's authorization.

| # | Finding | Reviewer(s) | Disposition | What changed |
|---|---|---|---|---|
| 1 | **`filters.js clearFilters()` is a fourth entry path** — it writes `#routine.value = ''` and dispatches `change` (twice, since it also re-enters via `#routine-env`). Hooking the listener silently turns **Clear Filters** into a superset-selection wipe. | all three (blocking) | **accept** | The repo had already ruled on exactly this shape: **KI-005 / OWNER-4**, recorded on the `#exercise` listener — *"Clearing the dropdown is not a deliberate exercise choice — it happens on Clear Filters"*. The reset is guarded on a **non-empty** composite value, so Clear Filters is inert by the same rule. Pinned by a dedicated negative test. |
| 2 | **`pageshow`/BFCache also dispatches**, against a restored DOM *and* a live `selectedExerciseIds` — so B5's "no selection yet by construction" is false. | architecture, product-risk | **accept** | Same guard: the stateless reset writes `''`, so it no longer clears. The false justification is removed. |
| 3 | **Step 4 cannot fail.** A routine change does not re-render the table, so `data-superset-group` attributes are stale DOM. A covert unlink leaves them intact and the assertion green — the one check carrying the owner lock is blind to the thing it names. | test-strategist, product-risk (blocking) | **accept** | Three independent channels now: a request counter asserting **0** POSTs to either superset endpoint, a `GET /get_workout_plan` re-read asserting both rows still share one group, and the DOM assertion retained for the in-place-strip case. |
| 4 | **`toBeDisabled()` on the link button is vacuous** — the template ships it `disabled`, and it is disabled at every count except a linkable pair. It can also go falsely **red** when the last selection was a superset row. | test-strategist, architecture (blocking) | **accept** | Asserts `#superset-actions` (the container) instead, and pins the **pre**-state (`toHaveCount(1)` + `toBeVisible()`) before the change, since "hidden" and "0 checked" are both already true on arrival. |
| 5 | **The state table omits the button flags #317 was about.** `updateSupersetActionButtons()` early-returns at count 0, so `unlinkBtn.hidden = false` survives inside a `display:none` container. | product-risk, architecture | **accept** | The zero branch now restores the template rest state (link visible+disabled, unlink hidden, info empty). Asserted via the `hidden` **attribute**, because `toBeHidden()` passes on the ancestor's `display:none` and cannot bite. |
| 6 | **A `className` clobber would strip `superset-group-N`** from persisted rows — the DB untouched but the superset visually dissolving — and every assertion in the spec is attribute-based, so nothing would notice. | product-risk, test-strategist | **accept** | The sweep is `classList.remove('superset-selected')` only, stated in the docstring. The test makes its transient selection **on a row of the linked pair** and asserts it still carries `superset-group`. Mutation M5b was **vacuous until that change** — the original test selected an unlinked row, so the clobber could not reach it. |
| 7 | **Four of the six state items had no assertion**, and item 1 (the id `Set`) has no DOM projection at all. | test-strategist | **accept** | Added: `tr.superset-selected` count, info `toHaveText('')`, inline `style.color` (not `toHaveCSS`, which reads the computed value), and a **re-click probe** — if the `Set` survived, the next click reads as the second selection, not the first. That probe is the only thing that kills mutation M2. |
| 8 | **"Immediately" is an undetectable claim** — every assertion auto-retries, so a reset moved below the `await` passes identically. | test-strategist | **accept** | A test stalls `/get_routine_exercises/*` and asserts the cleared state **while the request is in flight**. Proven by mutation: moving the call past that fetch fails it. |
| 9 | **The info colour bleeds** — the `selectedCount === 1` branches write `textContent` but never `color`, so a `--wp-warn` from a prior 2-selection survives onto a neutral message. Plan v1 over-claimed this as fixed. | product-risk, architecture | **accept** | The colour is reset once on entry to the non-zero path, so every branch starts neutral. |
| 10 | **`updateWorkoutPlanTable()` leaves items 5 and 6 stale on every tab switch, add, and drag-reorder**, so B2's "the existing call is not wrong" is inaccurate. | architecture | **accept — fixed at the source** | Fixing the zero branch of `updateSupersetActionButtons()` repairs that call site too, with no new call and no extra coupling. |
| 11 | **Re-routing link/unlink is a second, undeclared behavior change** — today the action bar holds a stale message until the async refresh lands; centralizing makes it vanish at once. | architecture | **accept** | Declared below as an explicit second criterion. |
| 12 | The "hook, don't add" reason is the **listener-count contract test**, not "#316 in spirit" — a non-fetching duplicate listener still reds `exercise-catalog-fetch`. And "before any `await`" must mean **above the `try`**, or a throw surfaces as the misleading *"Failed to load exercises for routine"* toast. | architecture | **accept** | Both corrected; the call sits above the `try` and the comment says why. |
| 13 | **`Test Inventory Drift` pins hard-wait counts, not just node counts** — this spec is pinned at 9 `waitForTimeout` lines, and the change moves that number. | test-strategist, architecture | **accept** | Regenerated canonically. The removed `waitForTimeout(500)` is replaced by web-first assertions, so the count moves **down**. |
| 14 | Add **`browser-navigation-state.spec.ts`** to the gate — it is the only required spec driving the `pageshow` path. `listener-cleanup` is a page smoke here, not the duplicate-listener proof; that proof is `exercise-catalog-fetch`, which is deep-gate tier and must be run locally. | test-strategist | **accept** | Both corrected in the gate list. |
| 15 | Three documents assert the opposite behavior and would contradict the shipped code. | all three | **accept, minus one** | `E2E_PERFORMANCE_PROFILE.md` and the in-spec rationale block are updated here. **`docs/MASTER_HANDOVER.md` is deliberately NOT edited** — this program's authorization forbids touching it from a feature packet; item 2 is recorded for Session 10 in the worktree-local handover. |
| 16 | `selectExerciseCheckboxes()` asserts against **all** rows, so "add A, add B, add C, then link A+B" is impossible — the link must happen before the third row exists. | test-strategist | **accept** | Ordering fixed and called out in a comment. |
| 17 | "0 checked" is vacuous on an empty table. | test-strategist | **accept** | Paired with a total-checkbox count and an unchanged row count. |
| 18 | B5 row 4 (orphan highlight outside the tab filter) guards an impossible state — filtered-out rows are not in the DOM. `routineSelected` has zero listeners anywhere. The composite dispatch also reaches a delegated handler in `filters.js` that no-ops. | architecture, product-risk | **accept** | Removed from the risk table; the trace now says "one direct listener plus one delegated observer that no-ops". |
| 19 | The clear is silent — no toast, no `aria-live` on the info span. | product-risk | **accept — recorded, not changed** | Stated as an explicit decision below. Adding an announcement is a UX change the owner did not ask for; the loss is one or two checkboxes and no data. |
| 20 | Pin `clearSupersetSelection()` as UI-state-only so it cannot later acquire a fetch. | product-risk | **accept** | Stated in the docstring and enforced by the zero-superset-requests assertion. |

---

## Section 3 — Plan v2 (as built)

### The guard is the design

`updateCompositeRoutineValue()` is the single funnel, but it has **four**
callers, not three, and two of them are not the user changing routine:

| Source | Composite written | Clears? |
|---|---|---|
| `handleRoutineChange` (day) | non-empty | **yes** |
| `handleEnvironmentChange` / `handleProgramChange` | `''` | no — until the cascade completes |
| `filters.js clearFilters()` | `''` | **no** — KI-005 / OWNER-4 |
| `applyStatelessCascadeReset()` on `pageshow` | `''` | **no** |

Guarding on a non-empty value separates them without sniffing the event source,
without a new listener, and without coupling `routine-cascade.js` to a plan
feature. The rule reads as: *the Add form now targets a different real routine,
so a selection made against the previous one is stale.*

### Two criteria, both asserted

1. **Routine change clears transient selection.** Four state items via one
   function; the action bar and info span via
   `updateSupersetActionButtons()`'s repaired zero branch.
2. **Link and unlink use the same reset** (finding 11). They previously cleared
   the id set and the checkboxes but not the row highlight or the info colour,
   and left the bar visible with a stale message until `refreshPlan()` landed.

   Asserting this needs the refresh **stalled**: once it lands,
   `updateWorkoutPlanTable()` clears the id set and calls
   `updateSupersetActionButtons()` anyway, so deleting the reset from
   `handleLinkSuperset` is invisible. Code review caught that the first draft
   claimed this criterion was asserted when all sixteen tests stayed green with
   it reverted.

### What it must not do, and how that is proven

| Lock | Proof |
|---|---|
| No persisted superset altered | 0 requests to either superset endpoint across the change; `GET /get_workout_plan` re-read shows both rows still sharing one group |
| Displayed rows unchanged | row count and `.exercise-name` list identical before/after |
| Not a covert unlink via the DOM | `data-superset-group` retained **and** `superset-group` class retained on a linked row that was itself transiently selected |
| Cleanup is immediate | asserted while `/get_routine_exercises` is stalled |

### Verification

| Gate | Result |
|---|---|
| `superset-edge-cases` | 16 passed (12 pre-existing + 4 new) |
| `workout-plan`, `exercise-interactions` | recorded in the PR |
| `exercise-catalog-fetch` (deep-gate tier — local only) | the listener-count contract |
| `browser-navigation-state` | the `pageshow` path |
| `listener-cleanup` | page-level smoke |
| Full `pytest` | no Python change expected |
| Red-path battery | **8/8** mutations rejected |
| Test inventory | regenerated; hard-wait count moves down |
