# Plan Review — Packet U3a: KI-010, the `showToast` type-word signature collision

*Owner: this document is at **Gate 0 only**. Nothing below is approved, and nothing below
authorizes implementation, test authoring, or any change to
[`static/js/modules/toast.js`](../../static/js/modules/toast.js) or
[`static/js/modules/__tests__/toast.test.js`](../../static/js/modules/__tests__/toast.test.js).*

> ⚠️ **ANNOTATION 2026-08-27 — the *"this document is at Gate 0 only"* clause above is SPENT in
> its first half and INTACT in its second.** **Gate 0 was SIGNED by the owner on 2026-08-27**;
> the five blocking questions are answered as **OD-1 … OD-5** at **§0.14**, and the option tables
> at §0.11 are annotated in place rather than rewritten. **The rest of that paragraph stands
> verbatim: nothing here authorizes implementation, test authoring, or any change to `toast.js`
> or `toast.test.js`.** Gate 1 has not begun, and under **OD-1** the implementation is
> deliberately deferred past `2026-09-05T17:59:26Z`.

**Packet identity.** [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4 defines
**Packet U3** as *two* defects — **KI-010** and **KI-011** — to be executed as *"two independently
reviewable commits or PRs — each needs its own Gate 0 and Gate 1"*. This document is the KI-010
half and is labelled **U3a** so the two halves cannot be conflated by a later reader.
**KI-011 (the action-button wipe) is deliberately not planned here**, is not in scope, and owes its
own separate Gate 0. Sharing the file `toast.js` is not a reason to share a gate.

**Everything in Section 0 was measured against `origin/main` at
`52c44c43a9d4f643437057085de233b1e9b4b689`** (PR #424, `docs(u2): sign Gate 1 plan for backup
save-first continuity`), in the isolated worktree `Hypertrophy-Toolbox-v3-main-u3-ki010-gate0`
on branch `wt/u3-ki010-gate0`. Line numbers below are re-anchored by measurement against that
commit, not carried forward from the source documents.

---

## Section 0 — Requirements Brief

### 0.1 The request, restated

Remove the ambiguity between the legacy and current `showToast` signatures for the four cases
where a caller's **message text is itself one of the four type words** — `error`, `warning`,
`success`, `info` — so that a type-word message renders as a message rather than as a boolean or
as default success copy.

The reason this needs Gate 0 rather than going straight to a plan is stated by the execution plan
itself: the fix must **deliberately invert a characterization test that currently pins the
defective output**, and `showToast` is a **shared, repository-wide dispatcher** reached from every
page. A test whose assertions are reversed is indistinguishable from a regression unless the
replacement contract was signed first.

### 0.2 Measured mechanism — why the collision happens

[`toast.js`](../../static/js/modules/toast.js) declares
`showToast(type, message, options = {})` and detects the legacy call shape
`showToast(message, isError?, duration?)` with **one** test, at
[`toast.js:15`](../../static/js/modules/toast.js#L15):

```js
const validTypes = new Set(['success', 'error', 'warning', 'info']);   // :12

if (!validTypes.has(type)) {                                            // :15
    const legacyMessage  = type;                                        // :16
    const legacyIsError  = typeof message === 'boolean' ? message : false;  // :17
    ...
    type    = legacyIsError ? 'error' : 'success';                      // :21
    message = legacyMessage;                                            // :22
}
```

**The discriminator is the *value* of the first argument, not the call's arity or its argument
types.** A legacy caller whose message happens to equal a type word therefore satisfies
`validTypes.has(type)`, the legacy branch at `:15-27` never executes, and the call is interpreted
as a modern one. What the caller passed as `isError` is then consumed as `message` and coerced by
`String(message)` at [`:50`](../../static/js/modules/toast.js#L50).

The one-argument form fails the other way: `message` is `undefined`, so the guard at
[`:49`](../../static/js/modules/toast.js#L49) falls through to the default copy at
[`:52`](../../static/js/modules/toast.js#L52) — and because the *class* is still driven by the
(accidentally valid) `type`, the toast is coloured for the type word while saying something else.

**Root cause, stated as one sentence for the migration note:** the legacy and current signatures
are distinguished by a value test on argument 1, and the two signatures' argument-1 domains
**overlap on exactly four strings**.

### 0.3 Reproduction — measured, not inferred

Executed under Node 24 + jsdom against the worktree's own `toast.js`, with the Bootstrap `Toast`
class faked exactly as [`toast.test.js`](../../static/js/modules/__tests__/toast.test.js) fakes it
(harness: `artifacts/ki010-repro.mjs`, gitignored, not part of this PR).

| Call | Rendered body text | Class applied | Caller's intent |
|---|---|---|---|
| `showToast('error', true)` | `"true"` | `bg-danger` | red toast saying `error` |
| `showToast('warning', true)` | `"true"` | `bg-warning` | red toast saying `warning` |
| `showToast('success', true)` | `"true"` | `bg-success` | red toast saying `success` |
| `showToast('info', true)` | `"true"` | `bg-info` | red toast saying `info` |
| `showToast('error', false)` | `"false"` | `bg-danger` | **green** toast saying `error` |
| `showToast('error')` | `"An unexpected error occurred."` | `bg-danger` | red toast saying `error` |
| `showToast('warning')` | `"Action completed successfully."` | `bg-warning` | green toast saying `warning` |
| `showToast('success')` | `"Action completed successfully."` | `bg-success` | green toast saying `success` |
| `showToast('info')` | `"Action completed successfully."` | `bg-info` | green toast saying `info` |

**All four type words reproduce in both arities. Nine defective outcomes, not one.**

**Three findings that were measured here and are recorded in no existing document:**

1. **`showToast('error', false)` is a severity inversion, not only a message loss.** A legacy
   caller asking for a *success* toast whose message is the word `error` gets a **red** toast
   reading `"false"`. Every existing description of KI-010 uses the `isError = true` form, in
   which the class happens to agree with the type word by coincidence. With `false` the class and
   the intent disagree. **No test pins this case.**
2. **`showToast('warning')` — the yellow toast that says the action succeeded — is real and is
   the sharpest of the nine.** It is recorded in prose at `STEP12_JS_UNIT_GATE0.md` §10.7-R3 and
   in the KI-010 row, and **no test pins it**. `showToast('info')` and `showToast('success')`
   behave identically; only `showToast('success')` is pinned, by **B43**.
3. **The collision is exact-string and case-sensitive.** Measured controls:
   `showToast('Error', true)` renders `"Error"` on `bg-danger`, and `showToast('errors', true)`
   renders `"errors"` on `bg-danger` — both correct. The defect's domain is exactly the four
   lowercase strings in the `validTypes` set at `:12`, which bounds any fix and any migration.

### 0.4 Caller inventory — measured against `52c44c4`

`showToast` is called **112** times in production JS (all files under `static/js` excluding
`__tests__/` and `toast.js` itself). Every one was classified; the harness is
`artifacts/ki010-caller-scan.py` / `ki010-legacy-total.py` (gitignored, not part of this PR).

| Class | Sites | Collision-capable? |
|---|---:|---|
| Modern, literal type word as argument 1 | 71 | No |
| Modern, multi-line literal type word | 2 | No |
| Modern, ternary over two literal type words | 3 | No |
| Modern, variable type from a closed valid set | 3 | No — traced, see below |
| Legacy, literal or template message as argument 1 | 19 | No — traced, see below |
| **Legacy, two-argument, expression as argument 1** | **8** | **YES** |
| Legacy, two-argument, expression traced to a fixed-prefix template | 1 | No — traced, see below |
| **Legacy, one-argument, expression as argument 1** | **5** | **YES** |
| **Total** | **112** | **13 collision-capable** |

**The 8 collision-capable two-argument sites** — all of shape
`showToast(<expr>.message || '<fallback>', true)`:

| Site | Line as measured on `52c44c4` |
|---|---|
| [`filters.js:251`](../../static/js/modules/filters.js#L251) | `showToast(error.message \|\| "Failed to reload exercises", true);` |
| [`workout-plan-execution-style.js:215`](../../static/js/modules/workout-plan-execution-style.js#L215) | `showToast(error.message \|\| 'Failed to update execution style', true);` |
| [`workout-plan-supersets.js:200`](../../static/js/modules/workout-plan-supersets.js#L200) | `showToast(error.message \|\| 'Failed to create superset', true);` |
| [`workout-plan-supersets.js:227`](../../static/js/modules/workout-plan-supersets.js#L227) | `showToast(error.message \|\| 'Failed to unlink superset', true);` |
| [`workout-plan-table.js:688`](../../static/js/modules/workout-plan-table.js#L688) | `showToast(error.message \|\| 'Failed to update exercise order', true);` |
| [`workout-plan.js:114`](../../static/js/modules/workout-plan.js#L114) | `showToast(error.message \|\| 'Failed to load workout plan', true);` |
| [`workout-plan.js:160`](../../static/js/modules/workout-plan.js#L160) | `showToast(error.message \|\| 'Failed to load exercise details', true);` |
| [`workout-plan.js:193`](../../static/js/modules/workout-plan.js#L193) | `showToast(error.message \|\| 'Failed to load exercise recommendations', true);` |

**The 5 collision-capable one-argument sites** — all of shape
`showToast(<expr>.message || '<fallback>')`:

| Site | Line as measured on `52c44c4` |
|---|---|
| [`exercises.js:31`](../../static/js/modules/exercises.js#L31) | `showToast(result.message \|\| "Exercise removed successfully!");` |
| [`exercises.js:59`](../../static/js/modules/exercises.js#L59) | `showToast(result.message \|\| 'Workout plan cleared successfully!');` |
| [`workout-plan-supersets.js:191`](../../static/js/modules/workout-plan-supersets.js#L191) | `showToast(data.message \|\| 'Superset created successfully');` |
| [`workout-plan-supersets.js:221`](../../static/js/modules/workout-plan-supersets.js#L221) | `showToast(data.message \|\| 'Superset unlinked successfully');` |
| [`workout-plan-table.js:680`](../../static/js/modules/workout-plan-table.js#L680) | `showToast(data.message \|\| 'Exercise order updated successfully');` |

**Both lists reproduce the KI-010 row's `8` and `5` exactly, and every line number in that row
is still accurate on `52c44c4`.** The row was written on 2026-08-22; U1's implementation (#423,
`06a3f41`) moved `volume-splitter.js` but touched none of these thirteen files.

**Four sites that a shape-based grep flags and that tracing clears — recorded so a later reader
does not "find" a fourteenth.**

| Site | Why it is not collision-capable |
|---|---|
| [`workout-plan-add-exercise.js:254`](../../static/js/modules/workout-plan-add-exercise.js#L254) | `showToast(message, true)` looks bare, but `message` is bound two lines earlier at `:253` to `` `Please fill in the following required fields: ${…}` `` — a fixed-prefix template literal that can never equal a type word. **A pattern-only inventory returns 9 here; the correct answer is 8.** |
| [`backup-center.js:858`](../../static/js/modules/backup-center.js#L858) | `showToast(toastLevel, message)` — `toastLevel` is bound at `:835` to `restoredCount === 0 ? 'warning' : 'success'`, a closed set of valid type words, so the modern branch is always the intended one. |
| [`workout-plan-replacement.js:78`](../../static/js/modules/workout-plan-replacement.js#L78), [`:88`](../../static/js/modules/workout-plan-replacement.js#L88) | `showToast(t.severity, t.message)` — `t` comes from `resolveSwapErrorToast()` at [`workout-plan-helpers.js:204-212`](../../static/js/modules/workout-plan-helpers.js#L204-L212), whose every branch returns `severity` of `'warning'` or `'error'`. Closed and valid. |
| [`exercises.js:36`](../../static/js/modules/exercises.js#L36), [`:68`](../../static/js/modules/exercises.js#L68) | Interpolated with a fixed prefix (`` `Unable to …: ${error.message}` ``), so always prefixed. Already recorded at §10.7-R3; re-confirmed here. |

**Reachability today — re-measured, and the conclusion holds.** No production `showToast` call
can currently receive a bare type word as its message, because the server never sends one.
Scanning `routes/`, `utils/` and `app.py` (harness `artifacts/ki010-server-scan.py`): **229**
`success_response(` / `error_response(` call sites, of which **0** pass a bare type word as the
first positional argument and **0** bind `message=` to one.
[`utils/errors.py`](../../utils/errors.py) only forwards whatever its caller supplies (`:36-37`,
`:94-97`), and [`fetch-wrapper.js:61`](../../static/js/modules/fetch-wrapper.js#L61) hands that
envelope message straight through to `error.message`.

> **The `229` differs from the `234` recorded on 2026-08-22 and that difference is not
> evidence of a code change.** The earlier figure's counting method is not stated in the source
> document, and mine is (occurrences of `success_response(` / `error_response(` on non-`def`
> lines across `routes/**`, `utils/**` and `app.py`). **The load-bearing half is identical in
> both readings: zero collision-capable messages.** Do not treat either integer as a tracked
> metric; re-derive it if it ever matters.

**KI-010 is therefore a latent defect, one server-copy change from firing** — and "latent"
is a statement about today's copy, not about the dispatcher. Any new `error_response('error', …)`
or a `message` field of `"info"` in a future route makes it live with no change to `toast.js`.

### 0.5 The characterization test that pins the defect

[`toast.test.js:556-569`](../../static/js/modules/__tests__/toast.test.js#L556-L569), case **B45**:

```js
it('B45: a legacy call whose message IS a type word swallows the message', () => {
    // PINNED SHARP EDGE, NOT DESIRED BEHAVIOR -- and NOT mitigated here.
    ...
    showToast('error', true);
    expect(bodyText()).toBe('true');
    expect(bgClasses()).toEqual(['bg-danger']);
});
```

**B45 asserts the defect.** Any fix that makes `showToast('error', true)` render `"error"` reds
B45 by construction. That red is the intended review signal, and it is exactly why this packet
owes Gate 0.

**B43 is the second test in scope**, at
[`toast.test.js:535-543`](../../static/js/modules/__tests__/toast.test.js#L535-L543): it pins
`showToast('success')` → `"Action completed successfully."`. Whether B43 must also change depends
entirely on the answer to **Q2** below. **If the one-argument form is left alone, B43 is
untouched; if it is fixed, B43 inverts too.**

**Three cases that must stay green under any fix**, because they define the legacy contract that
still has 33 live callers:

| Case | Assertion |
|---|---|
| **B5** ([`:169`](../../static/js/modules/__tests__/toast.test.js#L169)) | `showToast('Bare message')` → body `'Bare message'`, `bg-success` |
| **B6** ([`:175`](../../static/js/modules/__tests__/toast.test.js#L175)) | `showToast('Broke', true)` → body `'Broke'`, `bg-danger` |
| **B7** ([`:181`](../../static/js/modules/__tests__/toast.test.js#L181)) | `showToast('Fine', false)` → body `'Fine'`, `bg-success` |
| **B8** ([`:189`](../../static/js/modules/__tests__/toast.test.js#L189)) | `showToast('Msg', 'not-a-boolean')` → body `'Msg'`, `bg-success` |
| **B9** ([`:196`](../../static/js/modules/__tests__/toast.test.js#L196)) | `showToast('Broke', true, {requestId:'R1'})` → `'Broke (Request ID: R1)'` |
| **B11** ([`:210`](../../static/js/modules/__tests__/toast.test.js#L210)) | `showToast('m', false, 5000)` → delay `5000`, body `'m'`, `bg-success` |

### 0.6 The three pinning layers a fix has to move, and one required check it trips

This was measured because it is the part most likely to be discovered late.

| Layer | Where | What it pins | Trips on |
|---|---|---|---|
| **1. The test itself** | `static/js/modules/__tests__/toast.test.js` | B45's assertions, B43's assertion | inverting either |
| **2. The generated inventory** | [`docs/test_inventory/TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) + `.md` | **every Vitest case's identity string**, plus per-file counts (`toast.test.js`: **47**) and totals (**13** files / **231** cases) | **renaming** a case — which an honest inversion of B45 requires, since its current title is `"…swallows the message"` |
| **3. The pytest contract** | [`tests/test_vitest_inventory_contracts.py`](../../tests/test_vitest_inventory_contracts.py) | the literals `EXPECTED_TOTAL_CASES = 231`, `EXPECTED_TOTAL_FILES = 13`, `EXPECTED_PER_FILE[".../toast.test.js"] = 47` | **adding or removing** a case |

`Test Inventory Drift` is a **required** branch-protection context and the Vitest row is *the only
inventory row that pins identities rather than counts alone*
([`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md), "What trips `Test Inventory Drift`"). So:

- **Inverting B45 in place, keeping its title** → no inventory change, no pytest change. Dishonest;
  the title would then assert the opposite of the case.
- **Inverting B45 and retitling it** → `docs/test_inventory/` must be **regenerated** in the same
  PR. Layer 3 stays green (47 / 231 / 13 unchanged).
- **Adding any new case** (e.g. to pin `showToast('warning')`, or `showToast('error', false)`) →
  regeneration **and** an edit to the pinned literals in `tests/test_vitest_inventory_contracts.py`,
  which is itself covered by `Run Tests`.

> **This packet does not edit any of layers 2 or 3, and does not edit
> `STEP12_JS_UNIT_GATE0.md`, `UI_SCENARIOS_GAP_ANALYSIS.md`, or any shared status document.**
> They are named here as *measured consequences the owner is deciding about*, and they belong to
> the implementation PR that Gate 1 will authorize.

### 0.7 Qualification-window consequences — the decisive constraint

A **live strict 14-day JS-unit qualification window** is running, and KI-010 is the first packet
whose fix **necessarily** changes a JS test case inside it.

| Fact | Measured value | Source |
|---|---|---|
| **T0** | `2026-08-22T17:59:26Z` — `completed_at` of job `97070630453`, `JS Unit (Vitest, non-required)` | `STEP12_JS_UNIT_GATE0.md` §13.0 |
| **Strict mark** | `2026-09-05T17:59:26Z` | §6.5 annotation |
| **Suite being qualified** | **13 files / 231 cases** | `TEST_INVENTORY.json`, re-read on `52c44c4` |
| **Ledger state** | rows 1–12 recorded green; **row 13** (PR #424's post-merge run) is measured and **owed** by the U2 docs lane, not by this packet | §13.0 LIVE LEDGER |
| **Remaining as of 2026-08-27** | ≈ **9 days** | arithmetic on the strict mark |

**The governing rule, and why it is not §6.5's literal sentence.** Owner ruling **Q2** (§6.5)
says the window *"runs from the first successful `JS Unit (Vitest, non-required)` run on `main`
after the final expansion packet lands."* Read alone that is a **start** rule and says nothing
about a later change. **U1's Gate 1 finding R13 settled this**, and its resolution — recorded at
[`volume_failure_feedback/PLANNING.md` §v2.1](../volume_failure_feedback/PLANNING.md) and signed
by the owner on 2026-08-26 — is the governing wording:

> The operative test is **"changed no JS test case."**

That reading was derived from the document's own repeated practice, applied at §13.0 to rows 3, 4,
5, 6, 7, 10, 11 and 12, each of which discharged the restart question with the sentence *"changed
no JS test case, so Q2's restart clause did not engage."* U1's Plan v2 hardened the corollary from
*"arguably restarts"* to **"restarts — not arguably"** for a packet that adds a Vitest case.

**Applying it to KI-010, honestly:** every viable fix changes at least one JS test case, because
B45 asserts the behavior being removed. **On the governing wording, U3a's implementation PR
restarts the qualification window and discards the ~13 days already accumulated**, moving the
strict mark to roughly *U3a's merge + 14 days* and delaying decision **D2** (promoting
`JS Unit (Vitest, non-required)` into branch protection) by about a fortnight.

**One honest distinction the owner may or may not wish to draw**, stated as a question rather
than as a loophole. Every restart precedent so far concerns suite **composition** — a case added,
or a file added. **No precedent yet exists for an in-place semantic edit at constant 13 files /
231 cases.** A reading under which "changed no JS test case" means *"changed no test case's
existence or identity"* would let a title-preserving inversion pass without restarting — but that
reading is (a) not what the signed wording says, (b) achievable only by leaving B45's title
asserting the opposite of its body, and (c) still trips `Test Inventory Drift` the moment the
title is corrected. **This packet does not recommend it. It is surfaced as Q3 because deciding it
silently would be worse than deciding it wrongly.**

**Cost of each test change, measured:**

| Test change | Files / cases after | Inventory regen? | `test_vitest_inventory_contracts.py` edit? | Window under the governing rule |
|---|---|---|---|---|
| Invert B45's assertions, keep title | 13 / 231 | No | No | **Restarts** (a case changed) |
| Invert B45 + retitle | 13 / 231 | **Yes** | No | **Restarts** |
| Invert B45 + retitle + invert B43 | 13 / 231 | **Yes** | No | **Restarts** |
| Any of the above **+ new cases** for `showToast('warning')` and `showToast('error', false)` | 13 / 231+n | **Yes** | **Yes** (three literals) | **Restarts** |
| **Ship nothing until after `2026-09-05T17:59:26Z`** | 13 / 231 | No | No | **Untouched** |

**Consequence worth stating plainly: the window question is a scheduling decision, not a design
decision, and the "cheapest" test change costs exactly the same window as the most complete one.**
If U3a lands inside the window at all, the days are already spent — so there is no reason to ship
a *narrower* fix in order to protect the clock. Either defer the whole packet past the strict
mark, or ship the complete fix. That is **Q1**.

> **DECIDED 2026-08-27 — OD-1: defer.** The owner chose the table's last row,
> **"Ship nothing until after `2026-09-05T17:59:26Z`"**. **The window is untouched:** T0 stays
> `2026-08-22T17:59:26Z`, the strict mark stays `2026-09-05T17:59:26Z`, the suite stays
> **13 files / 231 cases**, and **U3a's implementation PR must not merge before that instant**.
> The other four rows are preserved as the measurement they are; none of them is the chosen
> path. The **`231+n`** row is what U3a will eventually ship under **OD-4**, but *after* the
> mark, where its restart cost is zero. See §0.14.

### 0.8 Compatibility invariants

Any accepted fix must preserve all of these. They are stated as invariants, not as tests, so that
Gate 1 can derive tests from them rather than the reverse.

| # | Invariant | Why it is load-bearing |
|---|---|---|
| **CI-1** | `showToast('<type>', '<message>')` — the modern 2-argument form — is unchanged for all four types, in both class and body text. | **79** of 112 production sites. |
| **CI-2** | `showToast('<type>', '<message>', <number>)` still treats the number as `delay`. | Pinned by **B10**. |
| **CI-3** | `showToast('<type>', '<message>', {duration, requestId, action})` is unchanged, including the `requestId` suffix gate (`error` type only). | Pinned by **B19–B23** (the suffix gate, one case per type plus the empty-ID case) and **B29** (the default delay reaching the constructor). |
| **CI-4** | `showToast('<non-type-word message>')` still renders that message on `bg-success`. | Pinned by **B5**; **19** literal-first legacy sites depend on it. |
| **CI-5** | `showToast('<non-type-word message>', true \| false)` still maps to `bg-danger` / `bg-success` with the message rendered. | Pinned by **B6**/**B7**. |
| **CI-6** | A non-boolean second argument in the legacy form is **not** an error flag. | Pinned by **B8**. |
| **CI-7** | `showToast('<msg>', <bool>, <number>)` still treats the number as `delay`. | Pinned by **B11**. |
| **CI-8** | A deliberate empty-string message is rendered, not replaced by default copy. | Pinned by **B44**; independent of this defect and must survive. |
| **CI-9** | The two default-copy strings are unchanged unless Q2 is answered in a way that requires it, and `toast.test.js` remains their sole exact-string guard (owner ruling 3, Gate 1, 2026-08-22). | A copy change here is a separate signed decision. |
| **CI-10** | **KI-011 is neither fixed nor worsened.** B30–B35 stay green and stay placement-neutral; `toastBody.innerHTML = ''` at `:60` and the button append at `:84` are not touched. | KI-011 owes its own Gate 0; U3a must not pre-empt it or silently half-fix it. |
| **CI-11** | No `bg-*` class mapping changes; `typeToClass[type] \|\| 'bg-success'` at `:98` keeps its fallback. | Pinned by B1–B4 and B42. |
| **CI-12** | The single-`#liveToast` / last-message-wins behavior (KI-004, mitigated) is unchanged. | Locked by `e2e/ui-hardening.spec.ts`. |

### 0.9 Scope

**In scope**

- [`static/js/modules/toast.js`](../../static/js/modules/toast.js) — the signature-disambiguation
  logic at `:12-32` only.
- [`static/js/modules/__tests__/toast.test.js`](../../static/js/modules/__tests__/toast.test.js) —
  **B45**, and **B43** if and only if Q2 is answered "fix the one-argument form"; plus any new
  cases Q4 authorizes. **RESOLVED 2026-08-27 by OD-2 and OD-4: the conditional fires. The
  in-scope characterization set is B45, B43 and — a case this bullet did not anticipate —
  B13, plus the new cases OD-4 authorizes. See §0.14 OD-2.**
- ~~Whichever of the **13** collision-capable call sites Q2/Q5 decide to migrate.~~
  **STRUCK 2026-08-27 by OD-5 — dispatcher-only. NO call site is migrated, and this bullet is
  reproduced in the out-of-scope list below so a later reader cannot find it only here.**
- `docs/test_inventory/**` and `tests/test_vitest_inventory_contracts.py` — **regeneration and
  literal updates only**, in the implementation PR, as a mechanical consequence of the above.
- The KI-010 row in [`docs/UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md) —
  status change and the link to the fixed-behavior test, **in the implementation PR only**.
- A migration note in the implementation PR description (§0.12).

**Out of scope — named so it cannot drift in**

- **KI-011** in every respect: the action-button wipe, `toastBody.innerHTML` at `:60`, the append
  at `:84`, `volume-splitter.js`, and the six B30–B35 cases beyond keeping them green.
- **Packet U2** in every respect — `docs/backup_confirmation_continuity/**`,
  `static/js/modules/backup-center.js`, `e2e/program-backup.spec.ts`. U2's implementation is
  running concurrently and merge order is unresolved.
- **Packet U1's residue** — U1-FOLLOWUP-1, U1's AA/contrast debt, `volume-splitter.js`.
- **Decisions Q4, D2 and D4**, and any branch-protection change. U3a *affects* the D2 timeline
  (§0.7); it does not decide D2.
- **The `STEP12_JS_UNIT_GATE0.md` ledger.** U3a's own PRs will mint ledger rows, and those rows
  are owed — but by the packet that owns that document, not by this one.
- **KI-004** (single-toast reuse), the `requestId` suffix rule, the default-copy strings
  themselves, and the `bg-*` mapping.
- Any change to `utils/errors.py`, `fetch-wrapper.js`, or server-side response copy. §0.4 shows
  the server side is clean; hardening it is a different packet.
- Dependabot PRs **#415** and **#416**.
- **Caller migration of any kind — added 2026-08-27 by OD-5.** None of the **13**
  collision-capable call sites, and none of the **33** legacy-form sites, may be edited by U3a.
  The fix is confined to `toast.js`. Q5 options (b) and (c) are declined, and (c) — deleting the
  legacy branch outright — remains available to a **later** packet, not to this one.
- **Shipping before `2026-09-05T17:59:26Z` — added 2026-08-27 by OD-1.** U3a's implementation PR
  merging inside the qualification window is out of scope, not merely deprioritised.

### 0.10 Acceptance criteria

**AC-1.** For all four type words `T ∈ {error, warning, success, info}`, the legacy two-argument
call `showToast(T, true)` renders body text exactly `T` on `bg-danger`, and `showToast(T, false)`
renders body text exactly `T` on `bg-success` — matching what the same call does today for any
non-type-word message (CI-5).

**AC-2.** The one-argument case `showToast(T)` behaves per the owner's answer to **Q2**, and
whichever behavior is chosen is identical for all four type words. Today it is not: `showToast('error')`
yields the *error* default copy and the other three yield the *success* default copy.
**RESOLVED 2026-08-27 by OD-2:** for all four type words `T`, `showToast(T)` renders body text
exactly `T` on `bg-success` — the same result the same call already produces for any
non-type-word message (CI-4). The "identical for all four" requirement is met by construction.

**AC-3.** Every invariant CI-1 … CI-12 in §0.8 holds, evidenced by the named existing cases
staying green without modification.

**AC-4.** **B45 is inverted, retitled to state the fixed contract, and carries an in-file comment
naming this document and the Gate 1 sign-off date** — so a later reader can tell a deliberate
inversion from a regression. This is the execution plan's own acceptance criterion, restated.

**AC-5.** `docs/test_inventory/` is regenerated in the same PR (never hand-edited), and
`Test Inventory Drift` is green.

**AC-6.** If Q4 authorizes new cases, `EXPECTED_TOTAL_CASES`, `EXPECTED_TOTAL_FILES` and
`EXPECTED_PER_FILE[".../toast.test.js"]` in `tests/test_vitest_inventory_contracts.py` are updated
in the same PR and `Run Tests` is green. **RESOLVED 2026-08-27 by OD-4: it does, so AC-6 is
unconditional.** `EXPECTED_TOTAL_FILES` stays **13** — OD-4 adds cases to an existing file and
creates no new one — while `EXPECTED_TOTAL_CASES` and `EXPECTED_PER_FILE[".../toast.test.js"]`
both move. **Both new values must be measured at implementation time, never predicted here.**

**AC-7.** The **mutation** evidence discriminates: reverting the production fix alone must red the
inverted B45 (and B43, if changed) and **nothing else**; and the negative control — applying the
fix without the test changes — must red exactly the characterization cases and no others. A fix
whose only proof is "the suite is green" is not accepted.

**AC-8.** The KI-010 row in `UI_SCENARIOS_GAP_ANALYSIS.md` moves from **Open** to **Mitigated**
with a link to the fixed-behavior test, and its "8 live call sites / 5 one-argument" sentences are
re-measured rather than copied — **or**, if Q5 chooses caller migration, updated to the post-migration
count. **RESOLVED 2026-08-27 by OD-5: the second branch is spent.** No caller is migrated, so the
counts stay **8** and **5** — but they are still **re-measured** at implementation time rather
than copied, because U3a will land after other packets have moved those files.

**AC-9.** The implementation PR description carries the migration note required by §0.12.

**AC-10.** No production line outside `toast.js` and the call sites Q5 authorizes is changed.
**RESOLVED 2026-08-27 by OD-5: Q5 authorizes zero call sites, so AC-10 tightens to its strongest
form — `toast.js` is the ONLY production file U3a may change.** A diff touching any other
production file fails Gate 2 on this criterion alone.

### 0.11 Blocking owner questions

All five must be answered before Gate 1 planning begins. Each option below is stated with its
measured cost.

> ⚠️ **ANNOTATION 2026-08-27 — all five are now ANSWERED.** The rulings are **OD-1 … OD-5** at
> **§0.14**, which is the authoritative record. The tables below are annotated **CHOSEN** /
> **NOT CHOSEN** in place and are otherwise unedited, so the options the owner declined — and
> the measured costs that made them declinable — remain readable. **A recommendation that was
> granted is still a recommendation in these tables; §0.14 is where it became a decision.**

---

#### **Q1 — Does U3a land inside the qualification window at all?** *(BLOCKING; decides scheduling before design)*

| Option | Consequence, measured |
|---|---|
| **(a) Defer the whole packet until after `2026-09-05T17:59:26Z`** — *recommended* — **CHOSEN → OD-1** | The window is untouched, D2's ~9 remaining days are preserved, and KI-010 stays latent for ~9 more days. **The defect is not reachable today** (§0.4: 0 of 229 response sites), so the exposure added by waiting is bounded by "no one adds a bare type-word message to a server response in nine days" — a risk the owner can also close by ruling that no such message may be added. Cost: this planning PR sits signed-but-unimplemented for ~9 days, and Gate 1 should be timed to land the implementation just after the mark. |
| **(b) Ship inside the window and accept the restart** — **NOT CHOSEN** | KI-010 is fixed ~9 days sooner. The clock resets to U3a's merge, the ~13 accumulated days are discarded, and **D2 slips by roughly a fortnight**. D2 is not U3a's to spend — this is precisely the reasoning that produced U1's OD-1. |
| **(c) Ship inside the window under the narrow reading of Q3** — **NOT CHOSEN** | Only available if Q3 is answered "composition-only", and only for a title-preserving inversion — which AC-4 forbids. **Listed for completeness; not recommended.** |

---

#### **Q2 — What is the correct behavior for the one-argument form `showToast(T)`?** *(BLOCKING; decides whether B43 also inverts)*

Today `showToast('error')` → *"An unexpected error occurred."* on red; `showToast('warning')`,
`showToast('success')` and `showToast('info')` → *"Action completed successfully."* on their own
colours. **The yellow toast that says the action succeeded is the sharpest live case and no test
pins it.**

| Option | What it means | Cost |
|---|---|---|
| **(a) One argument means *modern with no message* — keep today's default-copy behavior** — **NOT CHOSEN** | The 5 one-argument call sites keep the collision. `showToast('warning')` still renders success copy on yellow. | B43 untouched. Smallest change. **Leaves a documented defect open and would require KI-010 to close as *partially* fixed** — a status the gap-analysis table has no idiom for. |
| **(b) One argument means *legacy bare message* — `showToast('warning')` renders `"warning"` on green** — **CHOSEN → OD-2** | Consistent with CI-4: a one-argument call has always meant "here is my message". | **B43 inverts.** Removes the reachable path at the 5 one-argument sites. Makes the rule uniform: *argument 1 is a type word only when a second argument identifies it as the modern form*. |
| **(c) Split by type: keep the modern reading, but make all four types use their own default copy** — **NOT CHOSEN** | `showToast('warning')` → a *warning*-appropriate default string. | Requires **two new copy strings**, which CI-9 makes a separate signed decision. Does not fix the collision; only makes it less misleading. **Not recommended.** |

**Plan-stage recommendation: (b).** It is the only option under which AC-2's "identical for all
four type words" is satisfiable without inventing copy, and it is the option that actually closes
the 5 one-argument sites. **This is a recommendation, not a decision.**

> **DECIDED 2026-08-27 — OD-2: (b).** The recommendation was granted. **OD-2 carries a
> consequence this section did not anticipate and that §0.14 records in full: it puts a THIRD
> characterization case in scope — B13 — and it forces a design choice about how "one argument"
> is detected.** Read §0.14 OD-2 before deriving anything from this table.

---

#### **Q3 — Does an in-place edit to an existing JS test case, at constant 13 files / 231 cases, engage Q2's restart clause?** *(BLOCKING if and only if Q1 = (b) or (c))*

| Option | Basis |
|---|---|
| **(a) YES — any change to a JS test case restarts the window** — *recommended* — **CHOSEN → OD-3** | The governing wording signed on 2026-08-26 is *"changed no JS test case"*, and inverting B45 changes one. Consistent with every §13.0 row. |
| **(b) NO — only a change in suite composition (files, case count, case identity) restarts it** — **NOT CHOSEN** | Defensible from the *literal* §6.5 sentence, which is a start rule. But it (i) contradicts the signed operative wording, (ii) is unavailable to any honest fix because AC-4 requires a retitle, and (iii) would need to be signed as an **amendment** to the Q2 ruling, which falsifies every restatement of it — including the three in `MASTER_HANDOVER.md` and the one in `volume_failure_feedback/PLANNING.md` §v2.1. |

**If (b) is chosen it must be recorded as an amendment to owner ruling Q2, not as an
interpretation of it**, and the restatements must be grepped and corrected in the same packet
that amends it. That work is **not** in U3a's scope and would need its own owner instruction.

> **DECIDED 2026-08-27 — OD-3: (a).** The paragraph immediately above is therefore **SPENT**:
> (b) was not chosen, **no amendment to owner ruling Q2 is required, and no restatement of it
> anywhere in the repository is falsified by this packet.** That is the load-bearing half of
> this ruling. **The owner ruled Q3 deliberately even though OD-1 makes it moot for U3a** —
> this question's own heading scopes it *"BLOCKING if and only if Q1 = (b) or (c)"* — so the
> precedent exists on the record before the next packet needs it. See §0.14.

---

#### **Q4 — Which of the nine defective outcomes get pinned by a test?** *(BLOCKING; decides whether layer 3 moves)*

| Option | Cases | Cost |
|---|---|---|
| **(a) Invert B45 only** — **NOT CHOSEN** | 1 changed, 0 added | 13 / 231 holds; no `test_vitest_inventory_contracts.py` edit. Leaves `showToast('warning', true)`, `showToast('success', true)`, `showToast('info', true)` and the `false` severity-inversion unpinned — a fix that regresses for three of four type words would pass. |
| **(b) Invert B45 and parametrize it over all four type words** — *recommended* — **NOT CHOSEN (subsumed by (d))** | 1 changed, +3 | Directly evidences AC-1. **Moves totals to 234** (`toast.test.js` 47 → 50) and requires the three literal updates in `tests/test_vitest_inventory_contracts.py`. |
| **(c) (b) plus a case for `showToast(T, false)` — the severity inversion** — **NOT CHOSEN (subsumed by (d))** | 1 changed, +4 or +7 | Pins the finding at §0.3 item 1, which no document currently records. Same mechanical cost as (b). |
| **(d) (c) plus the one-argument cases, if Q2 = (b)** — **CHOSEN → OD-4** | B43 + B45 changed, +7 or more | Complete. Largest inventory movement. |

**Plan-stage recommendation: (c) if Q2 = (a); (d) if Q2 = (b).** Under Q1 = (a) the window cost is
zero either way, so there is no reason to under-pin.

> **DECIDED 2026-08-27 — OD-4: (d).** Q2 was answered (b), so the conditional resolves to (d) and
> the recommendation was granted. **The `if Q2 = (b)` clause in row (d) is now unconditional.**
> The row's *"+7 or more"* is a Plan-v1 estimate, **not a signed count** — the exact case count,
> and therefore the exact `test_vitest_inventory_contracts.py` literals, are Gate 1's to derive
> and must be **measured**, not carried forward from this cell. See §0.14.

---

#### **Q5 — Is the fix confined to the dispatcher, or are collision-capable callers migrated too?** *(BLOCKING; decides blast radius)*

The execution plan explicitly leaves this open: *"Migrate collision-capable callers if changing
the central dispatcher alone would create an ambiguous compatibility rule."*

| Option | Blast radius | Cost |
|---|---|---|
| **(a) Dispatcher only** — *recommended* — **CHOSEN → OD-5** | 1 production file | The disambiguation rule proposed at §0.13 (*"treat argument 1 as a type word only when argument 2 is not a boolean"*) is **not** ambiguous — it is a total function of the argument types, and §0.3's controls show the domain is exactly four strings. All 13 sites are fixed without being touched. **Zero risk to 10 unrelated modules.** |
| **(b) Dispatcher + migrate the 13 collision-capable sites to the modern signature** — **NOT CHOSEN** | 1 + 6 production files | Removes the collision at the source as well as the dispatcher. Cost: 13 edits across `filters.js`, `exercises.js`, `workout-plan.js`, `workout-plan-supersets.js`, `workout-plan-table.js`, `workout-plan-execution-style.js` — each routes to its own E2E specs under `QUALITY_GATE.md`, materially widening the gate set for one PR. |
| **(c) Dispatcher + migrate **all 33** legacy-form sites and delete the legacy branch** — **NOT CHOSEN** | 1 + 10 production files | Eliminates the ambiguity permanently and lets `:15-31` be deleted. **B5–B9 and B11 would all have to be deleted**, which is a much larger deliberate test removal than KI-010 requires, moves `toast.test.js` well off 47 cases, and is a refactor wearing a bug-fix's clothes. **Not recommended for U3a**; a reasonable follow-up once the window closes. |

---

### 0.12 Migration-note requirement

The refactor invariant in [`CLAUDE.md`](../../CLAUDE.md) §1 requires migration notes in the PR
description for any change to core workflow behavior. **KI-010's fix changes what a shared
dispatcher emits for input it previously mishandled**, so the implementation PR description must
carry a note containing, at minimum:

1. **The signature rule before and after**, stated as a rule and not as a diff — *"argument 1 was
   read as a type word whenever its value was one of four strings; it is now read as a type word
   only when \<the signed rule\>"*.
2. **The exact behavior change table** — the nine rows of §0.3, with the new rendered body and
   class beside each old one, so the change is reviewable without running anything.
3. **The list of call sites whose observable output changes** and the list of call sites whose
   output is unchanged, with the §0.4 counts re-measured at implementation time rather than copied
   from this document.
4. **An explicit statement that B45 (and B43, if changed) were inverted deliberately**, naming
   this document and the Gate 1 sign-off date, and stating that the red a reviewer would see
   without the inversion is the intended signal.
5. **The qualification-window disposition** — whether the PR restarts the window, under which
   answer to Q1/Q3, and what the new strict mark is if it does.
6. **An explicit statement that KI-011 is untouched**, with CI-10 as the evidence.
7. **The inventory-regeneration statement** — that `docs/test_inventory/` was regenerated by
   `python scripts/generate_test_inventory.py` and not hand-edited.

### 0.13 Proposed Gate 1 entry conditions

Gate 1 planning may begin only when **all** of the following hold. This list is a proposal; the
owner sets it.

1. ~~**Q1 … Q5 are each answered on the record**, in this document, with a date.~~
   **DISCHARGED 2026-08-27** — OD-1 … OD-5 at §0.14.
2. ~~**Q1 is answered first**, because (a) makes Q3 moot and changes Gate 1's timing.~~
   **DISCHARGED 2026-08-27** — Q1 was answered **(a)**, and Q3 was ruled anyway rather than
   left moot, so the precedent is on the record. **Conditions 3 … 8 all still stand.**
3. **This planning PR is merged.** Per the house rule that authorization begins at merge, not at
   signature, Gate 1 planning against an unmerged Gate 0 would be planning against a document
   `main` does not carry.
4. **Packet U2's merge order is resolved.** U2's implementation is running concurrently. U3a
   touches no U2 path (§0.9), so the two do not conflict in content — but both mint ledger rows
   in `STEP12_JS_UNIT_GATE0.md` §13.0, and rows are sequential and unclaimed-first. **Whoever
   merges second owes the later row**; that must be agreed, not discovered.
   **REAFFIRMED 2026-08-27 by the owner as a binding Gate 1 entry condition.** Measured the same
   day: `origin/main` is still `52c44c4` and **U2's implementation has not merged**, so the
   ordering is still open. This condition is **not** discharged by OD-1's deferral — waiting for
   the strict mark is not the same as resolving the ledger-row order.
5. **The proposed disambiguation rule is stated in Plan v1 as a total function of the argument
   types**, not as a patch. The rule this document recommends, for the council to attack:

   > Treat argument 1 as a **type word** only when it is one of the four strings **and**
   > argument 2 is not a boolean. Otherwise treat the call as legacy.
   >
   > Under Q2 = (b), add: **and** argument 2 is not `undefined`.

   ⚠️ **AMENDED 2026-08-27 by OD-2.** The addendum is now **unconditional** — Q2 was answered
   (b). But *"argument 2 is not `undefined`"* is **one of two candidate spellings and Gate 1
   must choose between them on the record**, because they differ on a case an existing test
   pins. §0.14 OD-2 carries the measurement. **Plan v1 may not present the wording above as
   settled.**

   Measured properties of that rule, for the council to verify rather than accept:

   - It changes nothing for **CI-1** — argument 2 is a string at all **79** modern sites, and
     `typeof '<string>' !== 'boolean'`.
   - It changes nothing for **CI-4 … CI-7** — argument 1 is not a type word at any of the **33**
     legacy sites *except* when the collision fires, which is the case being fixed.
   - **The Q2 = (b) addendum breaks nothing either: there are ZERO single-argument literal
     type-word calls in production JS** (measured; harness `artifacts/ki010-onearg-literal.py`),
     so no existing site relies on `showToast('<type>')` meaning "modern, no message". The only
     callers that reach that shape are the **5** one-argument collision sites, and reaching it is
     the defect.
   - It makes `showToast('error', true)` render `"error"` on `bg-danger`, satisfying **AC-1**.

6. **Plan v1 states the mutation and negative-control design required by AC-7** before the council
   runs, not after.
7. **The gate set is derived from `QUALITY_GATE.md` in Plan v1**, and it must include at minimum:
   `npm run test:js`; `python scripts/generate_test_inventory.py` + `--check`; full `pytest`
   (reached through `tests/test_vitest_inventory_contracts.py`); and — because `toast.js` is
   loaded on every page — the E2E specs `ui-hardening.spec.ts`, `error-handling.spec.ts` and
   `validation-boundary.spec.ts`, plus each spec routed to by any module Q5 authorizes migrating.
8. **The council runs all three plan-stage reviewers** — `architecture-reviewer`,
   `test-strategist`, `product-risk-reviewer` — via `/council-plan`, producing a response matrix
   and Plan v2, per the *Large* row of `QUALITY_GATE.md`'s plan-stage routing. `toast.js` is a
   shared dispatcher reached from every page; that is a cross-cutting change.

---

### 0.14 Owner decisions — GATE 0, 2026-08-27

**All five blocking questions are answered. This subsection is the authoritative record**; the
§0.11 tables are annotated in place and keep the declined options and their measured costs. Each
ruling is stated with the consequence it creates, because a decision recorded without its
consequence is the failure mode this document exists to avoid.

---

#### **OD-1 — Q1 = (a). U3a is DEFERRED until after `2026-09-05T17:59:26Z`.**

**Consequences.**

- **The live JS-unit qualification window is untouched by U3a.** T0 stays `2026-08-22T17:59:26Z`,
  the strict mark stays `2026-09-05T17:59:26Z`, and the suite stays **13 files / 231 cases**.
  Decision **D2** loses none of its accumulated days to this packet.
- **U3a's implementation PR must not merge before that instant.** This is a scope boundary
  (§0.9), not a priority — a merge inside the window is out of scope, not merely discouraged.
- **Passing the strict mark is a precondition, not an authorization.** Reaching
  `2026-09-05T17:59:26Z` does not start implementation; **all eight §0.13 entry conditions must
  still hold**, Gate 1 must still run its council, and Gate 1 must still be signed.
- **Because the window cost is now zero, there is no reason to under-pin the fix.** That is the
  premise OD-4 rests on.
- **The latent-defect exposure during the wait is ACCEPTED and NOT mitigated.** §0.11 Q1 offered
  the owner a way to close it — *"a risk the owner can also close by ruling that no such message
  may be added"* — and **that ruling was not made**. So for the remainder of the window, any new
  `error_response('error', …)`, or any route setting a `message` to one of the four type words,
  makes KI-010 live with no change to `toast.js`. **Recorded as an open residual, not as a closed
  one.**

---

#### **OD-2 — Q2 = (b). One argument means a legacy bare message.**

For all four type words `T`, `showToast(T)` renders body text exactly `T` on `bg-success` — the
same result the same call already produces for any non-type-word message (**CI-4**). The yellow
toast reading *"Action completed successfully."* is removed, and the **5** one-argument
collision-capable call sites (§0.4) are fixed without being edited.

**Consequences — including one this document had not anticipated.**

- **B43 inverts**, as §0.11 Q2 predicted.
- **B13 enters scope, making THREE characterization cases, not two.**
  [`toast.test.js:236-239`](../../static/js/modules/__tests__/toast.test.js#L236-L239) is
  `showToast('error', undefined)` asserting the error default copy. In JavaScript an omitted
  second argument and an explicitly-passed `undefined` are indistinguishable *by the parameter's
  value* — which is precisely what **B43's own in-file comment says**: *"`message` has no default
  parameter, so an omitted second argument IS undefined; this is behaviourally identical to
  `showToast('success', undefined)`."*
- **Therefore the rule at §0.13 condition 5 has two candidate spellings, and they disagree on
  B13. Gate 1 must choose one on the record; Gate 0 deliberately does not.**

  | Spelling | B13 (`showToast('error', undefined)`) | Cost |
  |---|---|---|
  | **S1** — legacy when `message === undefined` | **flips** to body `"error"`, `bg-danger` | Simplest rule, and it **keeps B43's comment's premise TRUE** — the two calls stay behaviourally identical. Cost: a **third** case joins the inverted set, and B13's own title and assertion must be rewritten. |
  | **S2** — legacy when `arguments.length < 2` | **stays green** | Distinguishes omitted from explicit `undefined`, so only B43 and B45 invert and B13 is untouched. Cost: **falsifies B43's comment as written** — the two calls stop being behaviourally identical — and leaves the dispatcher with a distinction no caller currently makes. |

  **Measured, so Gate 1 argues from fact rather than folklore** (harness
  `artifacts/ki010-arity-probe.mjs`, gitignored): inside a function whose parameter list is
  non-simple (`options = {}`) in a strict-mode ES module, `arguments.length` **does** still
  distinguish the two — it reports **1** for `probe('error')` and **2** for
  `probe('error', undefined)`, while `message === undefined` is `true` in both. **S2 is
  mechanically available.** Which spelling is *correct* is a contract question, not a feasibility
  one, and it is Gate 1's.
- **Either spelling obliges Gate 1 to revisit B43's in-file comment.** Under S2 it is false as
  written and must be corrected; under S1 it stays true but now explains why a *second* case
  (B13) inverts alongside it, which it does not say. Leaving it untouched is not an option.
- **CI-9 holds under both spellings.** Neither default-copy string changes, and both remain
  reachable and pinned through the explicit-`null` cases **B12**, **B14**, **B15a** and **B15b** —
  `null` is not `undefined`, so those four stay green either way.

---

#### **OD-3 — Q3 = (a). Any change to a JS test case restarts the qualification window.**

**Ruled deliberately, and deliberately on the record even though OD-1 makes it moot for U3a.**
Q3's own heading scopes it *"BLOCKING if and only if Q1 = (b) or (c)"*, and Q1 was answered (a) —
so this ruling changes nothing about U3a's execution. The owner ruled it anyway so the precedent
exists before the next packet needs it.

**Consequences.**

- **The signed operative wording is affirmed, not amended.** Owner ruling **Q2** of
  `STEP12_JS_UNIT_GATE0.md` — as governed by U1's finding **R13** and its *"changed no JS test
  case"* test, signed 2026-08-26 — stands exactly as written.
- **No restatement of it anywhere in the repository is falsified by this packet.** That is the
  load-bearing half: option (b) would have required an amendment plus a grep-and-correct sweep
  across `MASTER_HANDOVER.md` and `volume_failure_feedback/PLANNING.md` §v2.1, and **none of that
  work is now needed or authorized.**
- **An in-place semantic edit at constant 13 files / 231 cases restarts the window**, the open
  question §0.7 raised. Any future packet that edits a JS test case inside a live window spends
  that window, whether or not the suite's composition moves.

---

#### **OD-4 — Q4 = (d). Complete coverage.**

The inverted characterization behavior, all four lowercase type words, the `showToast(T, false)`
severity inversion, and the one-argument cases OD-2 requires.

**Consequences.**

- **Pinning layer 3 moves** (§0.6). `EXPECTED_TOTAL_FILES` stays **13** — OD-4 adds cases to an
  existing file and creates no new one — while `EXPECTED_TOTAL_CASES` and
  `EXPECTED_PER_FILE[".../toast.test.js"]` both move, and `docs/test_inventory/` must be
  regenerated. Under OD-1 all of this happens **after** the strict mark, so its window cost is
  **zero**.
- **No case count is signed here.** Q4 row (d)'s *"+7 or more"* is a Plan-v1 estimate. The exact
  count depends on OD-2's unresolved spelling (S1 puts B13 in the inverted set; S2 does not) and
  on how Gate 1 parametrises. **Gate 1 measures it; nobody carries this cell forward as a
  number.**
- **The changed-case set is at least {B45, B43} and at most {B45, B43, B13}**, plus the new cases.
  Which, is OD-2's spelling question.
- **AC-4's retitle-and-comment obligation applies to every inverted case, not only B45.**

---

#### **OD-5 — Q5 = (a). Dispatcher-only. No caller is migrated.**

**Consequences.**

- **`toast.js` is the only production file U3a may change.** AC-10 tightens to its strongest form;
  a diff touching any other production file fails on that criterion alone.
- **All 13 collision-capable sites are fixed without being edited**, and the **33** legacy-form
  sites keep their contract (CI-4 … CI-7).
- **The gate set narrows.** §0.13 condition 7's clause *"plus each spec routed to by any module Q5
  authorizes migrating"* resolves to **the empty set**. The minimum set — `npm run test:js`, the
  inventory generator plus `--check`, full `pytest`, and the three shared E2E specs — is unchanged
  and still required, because `toast.js` loads on every page.
- **The legacy branch is NOT deleted.** Q5 (c) — migrating all 33 sites and removing `:15-31`
  outright — is declined **for U3a** and stays available to a later packet once the window has
  closed. U3a leaves the legacy signature supported.
- **AC-8's caller-migration branch is spent**; the KI-010 row's counts stay **8** and **5**, and
  are still re-measured at implementation time rather than copied.

---

#### What signing Gate 0 does **not** do

- It does **not** authorize implementation, test authoring, or any edit to `toast.js` or
  `toast.test.js`.
- It does **not** start Gate 1. Per §0.13 condition 3, Gate 1 planning may not begin until **this
  PR is merged** — authorization begins at merge, not at signature.
- It does **not** resolve **U2's merge order or the §13.0 ledger-row sequence** (§0.13 condition
  4), which the owner reaffirmed as binding on the same day. Measured 2026-08-27: `origin/main` is
  `52c44c4` and U2's implementation has not merged.
- It does **not** settle OD-2's spelling (S1 vs S2), OD-4's case count, or any gate U3a owes.
- It does **not** close the latent-defect exposure OD-1 leaves open.


---

### Section 0 sign-off — GATE 0 — **SIGNED 2026-08-27**

- [x] Owner confirms the acceptance criteria AC-1 … AC-10 match intent — **accepted 2026-08-27**,
      with AC-2, AC-6, AC-8 and AC-10 resolved in place by OD-2, OD-4 and OD-5.
- [x] Owner reviews the compatibility invariants CI-1 … CI-12 and corrects or accepts each —
      **all twelve accepted 2026-08-27, unamended.**
- [x] Owner answers blocking questions **Q1 … Q5** — **answered 2026-08-27** as **OD-1 … OD-5**
      at §0.14.
- [x] Owner confirms the scope boundaries in §0.9, in particular that **KI-011 stays out** —
      **confirmed 2026-08-27**, and §0.9 gained two further out-of-scope entries from OD-5 and OD-1.

**Gate 0 is SIGNED.**

**Gate 1 has NOT begun, and signing Gate 0 does not authorize it.** Per
[`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4 and §10, U3 owes **its own
Gate 0 and Gate 1, per defect**. No gate passed by U1 or U2 carries to U3a, and U2's lighter
Gate-1-only requirement is U2's alone. There is no roadmap-level gate spanning U1–U3.

**Gate 1 planning may not begin until this PR is merged** (§0.13 condition 3) **and U2's
merge-order / ledger-row question is resolved** (§0.13 condition 4) — both reaffirmed by the owner
at signing. **And under OD-1, the implementation PR may not merge before
`2026-09-05T17:59:26Z`.** Signing Gate 0 authorizes exactly one thing: that Gate 1 planning may
be *requested* once those conditions hold.

**No production or test code has been modified by this packet.** This PR adds exactly one file
and, at the sign-off commit, modifies exactly that same one file.
The measurement harnesses named in §0.3, §0.4 and §0.14 were written to the gitignored
`artifacts/` directory in the packet's isolated worktree and are deliberately **not** committed —
they are throw-away evidence scripts, and §9's start checklist requires re-measurement at
implementation time anyway.
