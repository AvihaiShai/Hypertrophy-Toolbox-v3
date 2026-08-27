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
| `showToast('error')` | `"An unexpected error occurred."` | `bg-danger` | **green** toast saying `error` ⚠️ |
| `showToast('warning')` | `"Action completed successfully."` | `bg-warning` | green toast saying `warning` |
| `showToast('success')` | `"Action completed successfully."` | `bg-success` | green toast saying `success` |
| `showToast('info')` | `"Action completed successfully."` | `bg-info` | green toast saying `info` |

**All four type words reproduce in both arities. Nine defective outcomes, not one.**

> ⚠️ **CORRECTED 2026-08-27 by owner ruling OD-8.** Row 6's *Caller's intent* cell read *"red toast
> saying `error`"* when this table was signed. **That cell was wrong.** The legacy one-argument
> contract is fixed by **B5** ([`toast.test.js:188`](../../static/js/modules/__tests__/toast.test.js#L188)):
> `showToast('Bare message')` renders that message on **`bg-success`**. A legacy caller writing
> `showToast('error')` therefore intends a **green** toast whose body is the word `error` — which is
> exactly what **AC-2** and **OD-2** deliver. **The cell is corrected in place, not rewritten
> silently**, and the correction is the owner's, not this packet's. **Rows 1–5 and 7–9 were and
> remain correct**; only row 6 moved. The product-risk reviewer surfaced the contradiction and read
> it as AC-2 being wrong; measurement showed the table was.

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
   lowercase strings in the `validTypes` set at `:31` (`:12` before this packet), which bounds any
fix and any migration.

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

> ⚠️ **ANCHOR NOTE 2026-08-27 — `:556-569` no longer resolves, and re-numbering it would be wrong.**
> The case quoted above **no longer exists**: this packet **inverted** B45 and parametrised it over
> the four type words. The successor, `B45a–d`, sits at **`:625-633`** with its explanatory comment
> from **`:610`**, and it asserts the **opposite**. The block above is preserved as the record of
> what pinned the defect at Gate 0; it is history, not a pointer.

**B43 is the second test in scope**, at
[`toast.test.js:535-543`](../../static/js/modules/__tests__/toast.test.js#L535-L543): it pins
`showToast('success')` → `"Action completed successfully."`. Whether B43 must also change depends
entirely on the answer to **Q2** below. **If the one-argument form is left alone, B43 is
untouched; if it is fixed, B43 inverts too.**

> ⚠️ **ANCHOR NOTE 2026-08-27 — `:535-543` no longer resolves either.** OD-2 answered Q2 with (b),
> so **B43 inverted**. The successor, `B43a–d`, sits at **`:589-597`** with its explanatory comment
> from **`:574`**. Same reasoning as the B45 note above: history, not a pointer.

**Three cases that must stay green under any fix**, because they define the legacy contract that
still has 33 live callers:

| Case | Assertion |
|---|---|
| **B5** ([`:188`](../../static/js/modules/__tests__/toast.test.js#L188)) | `showToast('Bare message')` → body `'Bare message'`, `bg-success` |
| **B6** ([`:194`](../../static/js/modules/__tests__/toast.test.js#L194)) | `showToast('Broke', true)` → body `'Broke'`, `bg-danger` |
| **B7** ([`:200`](../../static/js/modules/__tests__/toast.test.js#L200)) | `showToast('Fine', false)` → body `'Fine'`, `bg-success` |
| **B8** ([`:208`](../../static/js/modules/__tests__/toast.test.js#L208)) | `showToast('Msg', 'not-a-boolean')` → body `'Msg'`, `bg-success` |
| **B9** ([`:215`](../../static/js/modules/__tests__/toast.test.js#L215)) | `showToast('Broke', true, {requestId:'R1'})` → `'Broke (Request ID: R1)'` |
| **B11** ([`:229`](../../static/js/modules/__tests__/toast.test.js#L229)) | `showToast('m', false, 5000)` → delay `5000`, body `'m'`, `bg-success` |

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
| **CI-10** | **KI-011 is neither fixed nor worsened.** B30–B35 stay green and stay placement-neutral; `toastBody.innerHTML = ''` at `:60` and the button append at `:84` are not touched. ⚠️ **RECONCILED 2026-08-27 — the second clause is now FALSE AS A DESCRIPTION OF THE FILE and the criterion is restated, not deleted.** **KI-011 shipped first** (PR #426, squash `5b35966`): `toastBody.innerHTML = ''` **no longer exists**, and the action button is appended into a `div.toast-action-slot.d-inline` inside `#toast-body` rather than directly. **The criterion's intent is unchanged and still binds** — U3a must not fix, half-fix or regress KI-011 — but it is now met by **leaving the shipped continuity behaviour intact**, not by leaving two specific lines untouched. **B30–B35 staying green is the live half of this row**, and the anchors `:60` / `:84` must be re-measured against merged `main` before they are cited again. | KI-011 owes its own Gate 0; U3a must not pre-empt it or silently half-fix it. |
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
  ⚠️ **RECONCILED 2026-08-27.** KI-011 **shipped** as PR #426 (`5b35966`), so the exclusion now
  reads forward, not backward: U3a excludes the **merged** KI-011 behaviour — the action slot,
  the message-node replacement, the expiry timer, the dispose-before-content ordering and the
  `volume-splitter.js` message probe — and the line anchors above describe a file that no longer
  exists in that form.
- **Packet U2** in every respect — `docs/backup_confirmation_continuity/**`,
  `static/js/modules/backup-center.js`, `e2e/program-backup.spec.ts`. U2's implementation is
  running concurrently and merge order is unresolved. ⚠️ **RECONCILED 2026-08-27: U2 has
  MERGED** (PR #427, squash `efa780c`), so the concurrency and the unresolved order are both
  retired as facts.
- **Packet U1's residue** — U1-FOLLOWUP-1, U1's AA/contrast debt, `volume-splitter.js`.
- **Decisions Q4, D2 and D4**, and any branch-protection change. U3a *affects* the D2 timeline
  (§0.7); it does not decide D2.
- ~~**The `STEP12_JS_UNIT_GATE0.md` ledger.** U3a's own PRs will mint ledger rows, and those rows
  are owed — but by the packet that owns that document, not by this one.~~
  ⚠️ **AMENDED 2026-08-27, RATIFIED by owner ruling OD-9.** The owner authorised U3a to *"edit
  planning/ledger documentation"* and to *"record each still-unclaimed result once, in actual
  merge order"*. **U3a therefore appends rows to §13.0 and the bullet above no longer binds.**
  The crossing is recorded openly rather than left implicit — see §v2.0. **What still binds:**
  U3a records only results **no open PR claims**, never restates an existing row, and never
  renumbers one.
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

   ✅ **AMENDED AGAIN 2026-08-27 by owner ruling OD-6 — AND THE CONDITION'S OWN WORDING IS
   AMENDED WITH IT.** The spelling is **S2**: `arguments.length < 2`. The addendum above is
   therefore **superseded** — read *"and argument 2 was actually supplied"*, **not** *"and
   argument 2 is not `undefined`"*. An **explicitly supplied `undefined` remains a modern call**.

   **This condition previously required the rule *"as a total function of the argument types"*.**
   `arguments.length` is not a type, so S2 could not satisfy that wording — the architecture
   reviewer's finding A2. **The owner amended the condition on the record rather than
   reinterpreting it silently:**

   > **Condition 5, as amended 2026-08-27:** the disambiguation rule must be stated as a **total
   > function of the argument types AND the call shape/arity**, not as a patch.

   §v2.3 states it in that form. **No other clause of §0.13 is amended.**

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
  [`toast.test.js:255-274`](../../static/js/modules/__tests__/toast.test.js#L255-L274) is
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

---

## Plan v1 — Gate 1

*Written 2026-08-27 against `origin/main` at **`db6c34be35ba09168926c2d9f786925c51944251`** (PR #425,
this packet's own Gate 0 sign-off), in the isolated worktree
`Hypertrophy-Toolbox-v3-main-u3a-gate1` on branch `docs/u3a-ki010-gate1-plan`.*

**Gate 1 is NOT signed and this plan does not authorize implementation.** **OD-1 remains binding: no
U3a implementation PR may merge before `2026-09-05T17:59:26Z`, and passing that timestamp is neither
implementation authorization nor merge authorization.**

### v1.0 What changed since Gate 0, and what did not

| | |
|---|---|
| Gate 0 | **SIGNED 2026-08-27**, §0.14, rulings OD-1 … OD-5. Merged as squash `db6c34b` (PR #425). |
| §0.13 condition 3 — *this planning PR is merged* | **DISCHARGED** — `db6c34b` is on `main`. |
| §0.13 condition 4 — *U2 merge order resolved* | **DISCHARGED for Gate 1 planning** by the owner's ordering ruling of 2026-08-27 (§v1.1). |
| §0.13 conditions 5–8 | **This plan is the discharge attempt.** They are addressed at §v1.3, §v1.8, §v1.9 and by the council record below. |
| The nine defective outcomes, the caller inventory, the pinning layers | **Re-measured on `db6c34b`, not carried forward** (§v1.2). Every figure reproduced. |

### v1.1 Condition 4 — the owner's ordering ruling, and exactly what it does

> ⚠️ **SUPERSEDED IN PART, 2026-08-27 — U3a WRITES NO LEDGER ROW.** Everything in §v1.1 about the
> *ordering ruling* stands. What is spent is the **ledger-writing** half: while this PR was open,
> **PR [#429](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/429) merged to `main` and
> wrote rows 13–16** — the same four results U3a had measured. **The unclaimed-first rule fired
> against this packet**, U3a's block is **withdrawn** (see the withdrawal record in
> [`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md) §13.0), and the table below
> is left as the **disposition it was at planning time**, not as a live claim.
>
> **The conditional numbering was the right precaution and it is what made this a clean deletion
> rather than a correction to a shipped ledger.** The measurements themselves were never wrong —
> they are on `main` now, at rows 13–16, with the run and job ids U3a recorded.
>
> **OD-9's amendment to §0.9 stands but is now moot in effect:** U3a was authorised to write ledger
> rows and, as it turns out, has none to write.


> **Owner ruling, 2026-08-27:** *"U2 PR #427 has merge priority over U3a. U2 goes first; U3a goes
> second. Ledger entries remain strictly ordered by actual `main` merges and claimed unclaimed-first.
> Treat this ordering decision as discharging condition 4 for Gate 1 planning. This does not
> authorize merging PR #427."*

**What it discharges:** §0.13 condition 4, **for Gate 1 planning only**.

**What it does not do**, stated because each was a live risk:

- It is **not** merge authorization for #427, for this planning PR, or for any U3a implementation PR.
- It does **not** relax **OD-1**. Even after #427 merges, no U3a implementation may merge before
  `2026-09-05T17:59:26Z`.
- It does **not** let a row number be assumed. The ledger rows this packet writes are **14** and
  **15** *because* #427 claims **13** — measured from #427's head, not inferred — and that premise is
  re-checkable by one command. The precondition and the command are recorded in
  [`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md) §13.0, in the block this
  packet appends.

**The ledger disposition, measured.** Of the three settled `js-unit` results outstanding when this
plan began, **one was already claimed and two were not**:

| `main` run | `js-unit` job | Head / PR | Claim state, measured 2026-08-26T23:11:32Z | Written by U3a? |
|---|---|---|---|---|
| `33011674872` | `98319257214` | `52c44c4` / #424 | **Claimed as row 13 by PR #427** ⚠️ **RECONCILED 2026-08-27: #427 is now MERGED** (`efa780c`), and the row was in fact written by **#429**, not #427 | **No** — restating it would write one result twice |
| `33017593094` | `98339729053` | `7a64d2e` / #415 | **Unclaimed.** #427 explicitly declines it — *"Row 14 is owed, and it is measurable"* | **Yes — row 14** |
| `33020896786` | `98350728218` | `db6c34b` / #425 | **Unclaimed.** No open PR mentions it | **Yes — row 15** |

### v1.2 Re-measured substrate — every volatile count and line reference, on `db6c34b`

`static/js` tree hash is `bd703e800d512c21e32d6f03066cfe8080859f93` at both `52c44c4` and `db6c34b`,
so no JS moved between Gate 0 and Gate 1 — but every figure below was re-derived rather than carried
forward.

**`toast.js` anchors** (re-measured; all unchanged from Gate 0):

| Line | Content |
|---:|---|
| `11` | `export function showToast(type, message, options = {})` |
| `12` | `const validTypes = new Set(['success', 'error', 'warning', 'info']);` |
| **`15`** | **`if (!validTypes.has(type)) {`** — the single line this packet changes |
| `16`–`26` | the legacy normalisation body |
| `28` | `} else if (typeof options === 'number') {` |
| `49` | `if (message !== undefined && message !== null) {` |
| `52` | the two default-copy strings |
| `60` | `toastBody.innerHTML = '';` — **KI-011's surface, not touched** |
| `84` | `toastBody.appendChild(button);` — **KI-011's surface, not touched** |
| `98` | `const bgClass = typeToClass[type] \|\| 'bg-success';` |

**Caller inventory** (harnesses `artifacts/ki010-caller-scan.py`, `ki010-legacy-total.py`,
`ki010-onearg-literal.py`, all gitignored):

| Class | Sites |
|---|---:|
| Total `showToast` calls in production JS | **112** |
| Modern (argument 1 resolves to a type word) | **79** |
| Legacy (argument 1 is a message) | **33** |
| **Collision-capable, two-argument** | **8** |
| **Collision-capable, one-argument** | **5** |
| Single-argument **literal** type-word calls | **0** |
| **Explicit `undefined` as argument 2** | **0** — see §v1.4, this is the number that decides S1 vs S2 |

The 8 + 5 are the same thirteen sites listed at §0.4, at the same line numbers. The shape-based
over-count of 9 reproduces, and `workout-plan-add-exercise.js:254` traces clear again.

**Blast radius, measured for the first time at Gate 1** — this is why the gate set at §v1.9 is wide:

- **22 production modules import `toast.js`.**
- **15 of the E2E specs reference a toast**, led by `volume-splitter.spec.ts` (33 mentions),
  `workout-plan.spec.ts` (28), `ui-hardening.spec.ts` (27) and `program-backup.spec.ts` (14).

**Pinning layers** (re-read on `db6c34b`): `TEST_INVENTORY.json` reports **13 files / 231 cases** with
**47** for `toast.test.js` and **47** case-identity strings for that file;
`tests/test_vitest_inventory_contracts.py` pins `EXPECTED_TOTAL_CASES = 231` (`:57`),
`EXPECTED_TOTAL_FILES = 13` (`:58`) and `"…/toast.test.js": 47` (`:67`).

**Server-side reachability**: **229** `success_response(` / `error_response(` sites across `routes/`,
`utils/` and `app.py`; **0** pass a bare type word. KI-010 remains latent.

### v1.3 The disambiguation contract, stated as a total function

Condition 5 requires the rule as a total function of the argument types, not as a patch. Let
`VALID = {'success', 'error', 'warning', 'info'}` and let `argc` be the number of arguments actually
passed.

```
isTypeWord := VALID.has(type)
isFlag     := typeof message === 'boolean'
isAbsent   := <SPELLING>          // S1: message === undefined
                                  // S2: argc < 2

isModern   := isTypeWord AND (NOT isFlag) AND (NOT isAbsent)
```

- **`isModern`** → `(type, message, options)` are taken as given. A numeric `options` still becomes
  `{duration}` (`toast.js:28`).
- **NOT `isModern`** → the call is legacy: the message is `type`, the severity is
  `isFlag AND message` → `'error'` else `'success'`, and a numeric third argument still becomes
  `duration`.

**This is total.** Every `(argc, type, message, options)` tuple lands in exactly one branch, and the
predicate reads only argument *types* and one closed four-element string set — never a heuristic on
message content. **The `isTypeWord` half is unchanged from today; the whole of KI-010 is the two new
conjuncts.**

**Why the two new conjuncts are safe, measured rather than argued:**

- `isFlag` cannot fire on a modern call: argument 2 is a **string at all 79 modern sites**, and
  `typeof '<string>' !== 'boolean'`.
- `isAbsent` cannot fire on a modern call: there are **0** single-argument literal type-word calls and
  **0** explicit-`undefined` second arguments in production.

**The production diff is one predicate**, and nothing else in `toast.js` moves:

```js
// toast.js:15 — before
if (!validTypes.has(type)) {

// after
const isLegacyCall = !validTypes.has(type)
    || typeof message === 'boolean'
    || <SPELLING>;
if (isLegacyCall) {
```

### v1.4 S1 versus S2 — measured against the real test file, not reasoned

**Both spellings were built and run.** A mirrored probe (`artifacts/probe/`, gitignored) carries a
copy of `toast.js` and the **unmodified** `toast.test.js`, collected by a scoped Vitest config whose
`include` points only at the probe — so the real suite, the real inventory and `Test Inventory Drift`
are all untouched. The pristine arm is the anti-vacuity control.

| Arm | Vitest exit | Result | Cases that red |
|---|---:|---|---|
| **S0** — pristine `toast.js` | **0** | **47 passed (47)** | *(none — the probe is faithful)* |
| **S1** — `message === undefined` | **1** | **3 failed \| 44 passed (47)** | **B13**, **B43**, **B45** |
| **S2** — `arguments.length < 2` | **1** | **2 failed \| 45 passed (47)** | **B43**, **B45** |

**Neither spelling reds anything else.** B5–B11 (the legacy contract, CI-4 … CI-7), B12/B14/B15a/B15b
(default copy via explicit `null`, CI-9), B16/B17 (coercion), B19–B23 (the `requestId` gate, CI-3),
B24–B29 (class clearing and instance lifecycle, CI-11/CI-12), **B30–B35 (KI-011's action button,
CI-10)** and B42/B44 all stay green under both. **That is the measured evidence for AC-3.**

**The rendered behaviour is IDENTICAL under S1 and S2** — all nine defective outcomes and all three
controls, measured through the same jsdom harness as §0.3:

| Call | Before | **After — S1 and S2 agree** |
|---|---|---|
| `showToast(T, true)`, all four `T` | `"true"` on the type's own class | **`T` on `bg-danger`** |
| `showToast('error', false)` | `"false"` on `bg-danger` | **`"error"` on `bg-success`** |
| `showToast(T)`, all four `T` | default copy on the type's own class | **`T` on `bg-success`** |
| `showToast('Real msg', true)` | `"Real msg"` on `bg-danger` | unchanged |
| `showToast('errors', true)` / `showToast('Error', true)` | correct already | unchanged |

**So the choice is not about user-visible behaviour at all.** S1 and S2 differ on **exactly one
input** — `showToast(T, undefined)`, an *explicitly passed* `undefined` — and the measured population
of that input is:

- **0** production call sites (harness `artifacts/ki010-undef-arg2.py`);
- **1** site in the entire repository: **`toast.test.js:271`, which is B13 itself** (`:237` at the
  time of this measurement; re-anchored 2026-08-27, the case and its assertions unchanged).

| | **S1** — legacy when `message === undefined` | **S2** — legacy when `argc < 2` |
|---|---|---|
| **B13** `showToast('error', undefined)` | **REDS.** Must invert: body `"error"`, `bg-success`, and its title must change | **Stays green, untouched** |
| **B43** `showToast('success')` | Inverts | Inverts |
| **B45** `showToast('error', true)` | Inverts | Inverts |
| **Parametrisation** | B43 and B45 parametrise over four `T`; B13 also needs a decision — leave as one inverted case, or parametrise to four | B43 and B45 parametrise over four `T`; B13 is out of scope entirely |
| **Predicted `toast.test.js` cases** | **57** (B13 left single) or **60** (B13 parametrised) | **57** |
| **Predicted suite totals** | **13 / 241** or **13 / 244** | **13 / 241** |
| **Rule reads** | one expression, no `arguments` | uses `arguments.length` inside a function with a default parameter — legal and measured working, but a less common idiom |
| **B43's in-file comment** | Its premise (*"an omitted second argument IS undefined … behaviourally identical"*) **stays true**; the comment must still be rewritten because it now explains why a second case inverts alongside it | Its premise becomes **false** — the two calls stop being behaviourally identical — so the comment must be corrected |
| **What the contract says about an explicit `undefined`** | *"Passing `undefined` is the same as passing nothing."* Simpler to state; loses the ability to say "no message" on a modern call | *"An argument you passed is an argument you passed."* Preserves an explicit-`undefined` escape hatch that **no caller uses** |

**Measured fact underpinning S2's feasibility:** inside a function whose parameter list is non-simple
(`options = {}`) in a strict-mode ES module, `arguments.length` still distinguishes the two —
**1** for `probe('error')`, **2** for `probe('error', undefined)`, while `message === undefined` is
`true` in both (harness `artifacts/ki010-arity-probe.mjs`). **Both spellings are mechanically
available; neither is blocked.**

**Plan v1 recommends S1**, for three reasons, none of which is decisive on its own:

1. **It is the rule the signed Gate 0 text already names.** §0.13 condition 5's addendum reads *"and
   argument 2 is not `undefined`"*. S2 would be a substitution, not a spelling of the signed rule.
2. **It keeps the contract statable in one sentence a caller can hold in their head** — *"a type word
   in argument 1 is a type only when you actually passed a non-boolean message"* — with no dependence
   on `arguments`, which behaves differently in arrow functions and is the kind of construct a future
   refactor silently breaks.
3. **It costs one extra inverted case, and that case has zero production population.** B13 pins an
   input no caller makes; inverting it costs a title and an assertion, not coverage.

**The honest case for S2**, stated so the owner is not choosing blind: it is the *smaller* change to
the existing test file (two inverted cases instead of three), and it preserves a distinction —
explicit `undefined` means "modern, no message" — that a future caller *could* want, even though none
wants it today. If the owner values keeping B13 exactly as it stands, S2 is the correct choice and
Plan v1's recommendation should be overridden.

**This is a recommendation. Plan v1 does not choose, and the artifacts below are written so that
either ruling is a small, localised edit — not a rewrite.**

### v1.5 Exact production change

| File | Symbol | Change |
|---|---|---|
| [`static/js/modules/toast.js`](../../static/js/modules/toast.js) | `showToast` | **Line 15 only.** Replace `if (!validTypes.has(type)) {` with the `isLegacyCall` predicate of §v1.3, in the spelling the owner rules. **No other line moves.** The comment at `:14` is updated to describe the new rule. |

**Nothing else in production changes** — OD-5 confines the fix to the dispatcher, and AC-10 in its
tightened form makes `toast.js` the only production file this packet may touch.

### v1.6 Test design under OD-4

OD-4 = complete coverage: the inverted characterization behavior, all four type words, the
`showToast(T, false)` severity inversion, and the one-argument cases OD-2 requires.

| Case | Shape | Asserts | Status |
|---|---|---|---|
| **B45a–B45d** | `showToast(T, true)` for `T ∈ {error, warning, success, info}` | body is exactly `T`; class is `bg-danger` | **replaces B45** (1 → 4) |
| **B46a–B46d** | `showToast(T, false)` for all four `T` | body is exactly `T`; class is `bg-success` | **new** (0 → 4) — pins the severity inversion at §0.3 finding 1, which no test has ever covered |
| **B43a–B43d** | `showToast(T)` for all four `T` | body is exactly `T`; class is `bg-success` | **replaces B43** (1 → 4) |
| **B13** | `showToast('error', undefined)` | **S1:** body `"error"`, `bg-success` — inverted and retitled. **S2:** unchanged, stays green | **spelling-dependent** |

Every replaced or inverted case carries the AC-4 comment: that the inversion is deliberate, naming
this document and the Gate 1 sign-off date, and stating that the red a reviewer would see without it
is the intended signal — not a regression.

**B43's existing in-file comment is rewritten under either spelling** (§v1.4), and the two default-copy
strings stay pinned by B12/B14/B15a/B15b, which is why CI-9 survives.

### v1.7 Inventory arithmetic — a prediction, to be measured

`47 − 2 (B43, B45 removed) + 12 (B43a–d, B45a–d, B46a–d) = **57**` for `toast.test.js`, and
`231 + 10 = **241**` for the suite. `EXPECTED_TOTAL_FILES` stays **13** — no new file. Under S1 with
B13 parametrised the figures would instead be **60 / 244**.

> **None of these numbers is signed, and the implementation must not assume them.** They are
> arithmetic on a design, and OD-4 explicitly refuses to sign a case count. The implementation
> measures `npx vitest list` output and sets the three literals in
> `tests/test_vitest_inventory_contracts.py` (`:57`, `:58`, `:67`) from that measurement.

### v1.8 Mutation and negative-control procedure (AC-7)

Run on a **mirrored probe** — `artifacts/probe/static/js/modules/` carrying copies of `toast.js` and
`toast.test.js`, with a scoped Vitest config whose `include` points only into the probe. `toast.js`
imports nothing, so no collaborator mocks are needed. **This probe design is not hypothetical: Plan
v1's §v1.4 table was produced by it.**

| Step | Arm | Substrate | Required outcome |
|---:|---|---|---|
| **0** | **Pre-flight** | pristine `toast.js` + pristine `toast.test.js` | Exit **0**, **`47 passed (47)`**. Any other collected count is **BAD RUN**, not a result |
| **1** | **Negative control — fix without tests** | fixed `toast.js` + **pristine** `toast.test.js` | Exit **1**, and the failing set is **exactly** `{B43, B45}` under S2 or `{B13, B43, B45}` under S1. **Any additional red is a defect in the fix, not in the tests** |
| **2** | **Negative control — tests without fix** | **pristine** `toast.js` + new `toast.test.js` | Exit **1**, and the failing set is **exactly** the new and inverted cases. A green here means the new cases do not discriminate |
| **3** | **The pair** | fixed + new | Exit **0**, collected count equal to the §v1.7 measured figure |
| **4** | **Rival-spelling arm** | **the other spelling's** `toast.js` + the shipped `toast.test.js` | Reds **exactly B13** and nothing else. This is the arm that proves S1 and S2 differ *only* there — and it is the third, rival arm the repository's own false-green practice requires |
| **5** | **Per-conjunct mutation, both directions** | fixed `toast.js`, one conjunct at a time | Deleting `typeof message === 'boolean'` must red the B45a–d and B46a–d families and **nothing else**. Deleting the `isAbsent` conjunct must red B43a–d (and B13 under S1) and **nothing else**. Negating each conjunct must also red — a mutation tested in one direction only is half-tested |
| **6** | **`isTypeWord` control** | fixed `toast.js` with `validTypes` emptied | Must red broadly, including B1–B4. Proves the untouched half of the predicate is still load-bearing |

**Two judging rules, both learned the hard way and both mandatory:**

1. **Judge by exit code AND collected count together.** A run that exits 1 having collected **zero**
   cases is a **BAD RUN**, not a kill. This was hit for real while producing §v1.4: passing an
   unsupported `--reporter=basic` made Vitest exit **1** with no test results at all — indistinguishable
   from "everything failed" if only the exit code is read.
2. **A wrong probe path fabricates a survivor.** The first probe attempt resolved the source path one
   directory too high and failed loudly; had it failed *silently* it would have produced a green arm
   from a stale copy. Step 0's collected-count assertion is the guard, and it runs before every arm.

### v1.9 The complete gate set, derived from `QUALITY_GATE.md`

**Paths the implementation PR will change**, and the rows they route to:

| Path | `QUALITY_GATE.md` row |
|---|---|
| `static/js/modules/toast.js` | **Frontend (JS)** |
| `static/js/modules/__tests__/toast.test.js` | **Frontend (JS)** — and the row's explicit *"regenerate `docs/test_inventory/` whenever a `*.test.js` case is added, removed or renamed"* clause |
| `docs/test_inventory/TEST_INVENTORY.{json,md}` | regenerated output, never hand-edited |
| `tests/test_vitest_inventory_contracts.py` | `tests/**` → Targeted-test derivation |
| `docs/UI_SCENARIOS_GAP_ANALYSIS.md`, `docs/toast_type_word_collision/PLANNING.md` | **Product docs only** |

**Plan-stage size: Large** — a shared dispatcher reached from every page. Gate 0 + Gate 1, both with
the three-reviewer council. Already satisfied by §0.14 and by the council record below.

**The gate set, in required order:**

| # | Gate | Command | Pass condition |
|---:|---|---|---|
| **1** | Vitest, the changed suite | `npm run test:js` | Exit 0; collected count equals the §v1.7 **measured** figure |
| **2** | Inventory regeneration | `.venv/Scripts/python.exe scripts/generate_test_inventory.py` | Writes both artifacts. **Never hand-edited** |
| **3** | Inventory drift — the required context | `… generate_test_inventory.py --check` | `Test inventory is up to date.`, exit 0 |
| **4** | Determinism | regenerate a second and third time, then `git status --porcelain docs/test_inventory/` | Empty output each time |
| **5** | Full pytest | `/run-tests` | Green. The delta against baseline must be **zero new nodes** — this packet changes literals inside an existing test file and adds no pytest node. **A non-zero delta means something else moved** |
| **6** | Pyright baseline | `.venv/Scripts/python.exe scripts/pyright_baseline_diff.py` | No net-new diagnostics. Repo-wide, and `tests/**` is a `.py` change |
| **7** | **Full Chromium E2E, two invocations** | `/run-e2e`, then the seeded visual invocation | Exit 0 both times. **Derived from measurement, not from the feature map**: 22 production modules import `toast.js` and 15 specs reference a toast, so no narrow spec list is defensible. **The default single invocation cannot pass** — `PW_VISUAL_SEED` selects the seed script, not the spec set |
| **8** | Manual smoke | `/run-hypertrophy-toolbox` | Exercise **one** legacy two-argument caller and **one** one-argument caller and see the message — the Frontend (JS) row's *"manual smoke if interactive"*. The unit tests run in jsdom against a faked Bootstrap `Toast`; nothing else proves the real toast still renders |
| **9** | PR CI | — | **All 18 jobs green**, enumerated at job level. `Test Inventory Drift` and `Run Tests` are the load-bearing required contexts |
| **10** | Code-time review | `/unslop` | `code-reviewer` + `unslop-reviewer` over the final diff |
| **11** | Ledger | §13.0 | The implementation PR's own post-merge `main` `js-unit` result is owed as the next sequential row |

**Not in the gate set, and why:** `/build-css` (no `scss/**` or `static/css/**` change);
`e2e/visual.spec.ts` baselines (no paint change — toast copy is not captured at rest, and no baseline
may be regenerated without owner sign-off); branch-protection changes (D2 is not this packet's).

### v1.10 Scope containment and rollback

- **One production file.** A diff touching any other production file fails AC-10 outright.
- **KI-011 untouched** — `toast.js:60` and `:84` are not in the diff, and B30–B35 must stay green in
  every arm of §v1.8. **PR #426 is a separate lane and U3a neither reviews nor depends on it.**
- **Rollback is one predicate.** Reverting `toast.js:15` to `if (!validTypes.has(type)) {` restores
  today's behaviour exactly; the test and inventory changes then red, which is the intended signal.
- **The ledger block is append-only** and restates nothing, so it cannot conflict with #427's row 13
  beyond ordinary adjacency.

### v1.11 Sequencing and merge preconditions

1. **#427 merges first** (owner ruling, §v1.1). Not authorized by this plan.
2. **This Gate 1 planning PR** may merge once Gate 1 is signed **and** `gh pr view 427 --json state`
   reports `MERGED` — the row-14/15 precondition.
3. **Gate 1 signature** — owner, including the S1/S2 ruling.
4. **Implementation** may begin only after 2 and 3.
5. **The implementation PR may not merge before `2026-09-05T17:59:26Z`** (OD-1), and passing that
   instant authorizes nothing on its own.

### v1.12 Open decisions carried into the council

- **OD-6 (proposed): S1 versus S2.** Plan v1 recommends **S1**; §v1.4 carries the measured
  consequences of both. **Left to the owner.**
- **OD-7 (proposed): under S1, is B13 parametrised over all four type words** (60 / 244) **or left as
  one inverted case** (57 / 241)? Moot under S2.

> ⚠️ **SPENT 2026-08-27.** Both proposals above are now **ruled**: OD-6 = **S2**, OD-7 = **N/A**.
> The wording is left as the Plan-v1 record it was; the rulings are at the Gate 1 sign-off block.

---

## Council record — Gate 1, 2026-08-27

Three reviewers ran in parallel against Plan v1, per `QUALITY_GATE.md`'s **Large** plan-stage row.
**All three returned "needs revision".** Nine findings were BLOCKING. Every finding below was
**independently re-verified by measurement before disposition** — three were partly wrong on detail
and are corrected here rather than accepted as written.

**The killer class this council caught:** Plan v1 recommended **S1** on the strength of a
**syntactic** measurement (`0` occurrences of the literal token `undefined` in argument-2 position)
used to support a **runtime** safety property. All three reviewers hit that independently, from
three different directions. **The recommendation is reversed in Plan v2.**

### Response matrix

| # | Reviewer | Finding | Disposition |
|---|---|---|---|
| **A1** | architecture | **BLOCKING.** §v1.1/§v1.10/§v1.9 have U3a editing `STEP12_JS_UNIT_GATE0.md`, which signed §0.9 puts **out of scope**; and §v1.9's path table omits that file entirely | **ACCEPTED.** The owner authorised the ledger edit explicitly on 2026-08-27 (*"You are authorized to edit planning/ledger documentation … Record each still-unclaimed result once"*). That authorisation **amends signed §0.9** and is recorded as such at **§v2.0**, not left as an undocumented contradiction. The file is added to §v2.9's path table. **Ratification is owner decision OD-9.** |
| **A2** | architecture | **BLOCKING.** §v1.3's single totality proof — *"reads only argument **types**"* — is true of S1 and **false of S2** (`argc` is not a type). Signed §0.13 condition 5 requires the rule *"as a total function of the argument types"*, so **S2 cannot satisfy condition 5 as worded** | **ACCEPTED, and it is the sharpest procedural finding of the council.** §v2.3 now states **two** contracts: S1 over argument *values*, S2 over *call shape*. **Choosing S2 therefore requires amending §0.13 condition 5 on the record** — surfaced in the sign-off block so the S1/S2 ruling carries that consequence visibly. |
| **A3 / P2 / T-B2** | all three | **BLOCKING.** The evidence that `isAbsent` "cannot fire on a modern call" is a **lexical scan for the token `undefined`**; S1's predicate is a **runtime value** test | **ACCEPTED — this is the finding that reverses the recommendation.** Re-measured with a value-shape oracle: of the 74 single-line modern sites, **43 pass a literal**, **18 are `\|\|`/ternary-guarded**, and **13 pass a bare expression**. Architecture and test-strategist independently traced all of them and agree with me that **today every one is guarded at its assignment**, so the reachable population is genuinely **0**. But the invariant is **not structural**, and both named the same exposure: [`workout-plan-helpers.js:210`](../../static/js/modules/workout-plan-helpers.js#L210) `default: return { severity: 'error', message };` forwards its caller's `message` **unguarded**. §v2.4 now carries the value-shape measurement **and** the residual. |
| **P2 / T-B3** | product-risk, test-strategist | **BLOCKING.** Under S1, a modern call whose message evaluates to `undefined` at runtime renders the **type word on a GREEN toast** — a severity inversion, the class §0.3 calls "the sharpest of the nine". And the inverted B13 would **assert that outcome as correct** | **ACCEPTED. Measured and confirmed** (§v2.4): under S1 `showToast('error', <undefined>)` → `"error"` / `bg-success`; under S2 → `"An unexpected error occurred."` / `bg-danger`, i.e. **S2 preserves today's behaviour and S1 degrades it**. Test-strategist's false-pass scenario is real: delete the `\|\| 'Failed to replace exercise'` guard — which **OD-5 forbids U3a from touching and no test pins** — and S1 renders a green "error" with the whole suite green. **Plan v2 recommends S2.** |
| **P1** | product-risk | **BLOCKING.** §0.3's signed *intent* column says `showToast('error')` means *"red toast saying error"*, but AC-2/OD-2 deliver **green**. The signed table and the signed criterion disagree | **ACCEPTED, and the reviewer is right that the cell is wrong** — but the correction is the opposite of what it implies. Measured: **B5** ([`toast.test.js:188`](../../static/js/modules/__tests__/toast.test.js#L188)) fixes the legacy one-argument contract as **success/green**. So `showToast('error')` from a legacy caller means **green**, and it is **§0.3 row 6's intent cell that is in error**, not AC-2. Rows 1–5 and 7–9 are all correct. **This packet does not silently edit a signed table**: the correction is raised as owner decision **OD-8**. |
| **P3** | product-risk | **SHOULD-FIX.** The "8 live call sites" figure is shape-only; at most 6 are ever visible — `workout-plan.js:114` sits behind `if (!error.code)` which `normalizeError` makes always-false, and `filters.js:251` is clobbered in the same tick by `:255` under KI-004 | **ACCEPTED.** §v2.2 gains a visibility column, and **AC-8 is amended** to require the KI-010 row to carry the **visible** count beside the shape count. |
| **P4 / P5 / P11 / P13** | product-risk | **SHOULD-FIX.** The fix restores **fidelity, not quality**: `showToast('success', true)` becomes a **red** toast whose only word is `"success"`. Severity comes from the boolean and never from the message | **ACCEPTED, in full and without softening.** §v2.10 states it plainly and the migration note must carry it. This is the finding most likely to be lost in a summary, so it is stated as a named limitation rather than a caveat. |
| **P6** | product-risk | **SHOULD-FIX.** No a11y statement anywhere, and `#liveToast` is an **assertive live region** | **ACCEPTED.** Measured: [`base.html:243-248`](../../templates/base.html#L243-L248) carries `role="alert"`, `aria-live="assertive"`, `aria-atomic="true"`, and severity is conveyed **only** by the `bg-*` class — no icon, no visually-hidden prefix. So the announced string changes for all nine outcomes and a screen-reader user cannot distinguish a red "success" from a real success. §v2.10 records it; `e2e/accessibility.spec.ts` is named in §v2.9. |
| **P7 / T-S10** | product-risk, test-strategist | **SHOULD-FIX.** Gate 8's manual smoke **cannot observe the fix**, because no server response reaches the collision | **ACCEPTED.** §v2.9 gate 8 now requires **console-invoked** `showToast('error', true)` and `showToast('warning')` on a loaded page, recording body, `bg-*` class and announcement. Without this the fixed behaviour is proven **only in jsdom against a fake Bootstrap `Toast`**. |
| **P8 / A6 / T-B2** | three | **SHOULD-FIX.** "Nine defective outcomes" is not the changed input domain — the **three-argument** legacy form also crosses the branch | **ACCEPTED.** Measured, and it is worse than "the delay happens to agree": `showToast('error', false, {requestId:'R1'})` renders `"false (Request ID: R1)"` on `bg-danger` today and **`"error"` on `bg-success` with the suffix SILENTLY DROPPED** after the fix, under **both** spellings — because legacy sets `type='success'` and the suffix gate at `:56` is error-only. **New, and no test pins it.** §v2.6 adds cases; disposition is owner decision **OD-11**. |
| **P9 / T-S8** | product-risk, test-strategist | **SHOULD-FIX.** Flipping KI-010 to *Mitigated* falsifies neighbouring prose: `UI_SCENARIOS_GAP_ANALYSIS.md:208` is a **second** pointer saying "open as KI-010", and `STEP12_JS_UNIT_GATE0.md` §10.3/§10.5 restate B43/B45 and the 47-case arithmetic in the present tense | **ACCEPTED.** `:208` joins §v2.9's in-scope list. The §10.3/§10.5 staleness is **larger than either reviewer stated** — test-strategist traced kill-set shifts in N8/N10/N12 and two **signed Gate 1 checkboxes** at `:2054`/`:2067`. Disposition is owner decision **OD-10**. |
| **P10 / T-N6** | product-risk, test-strategist | **NOTE.** Both default-copy strings are **already production-dead**, and S1 removes the last modern route to them | **ACCEPTED as a disclosure.** CI-9 survives — the strings are unchanged and still pinned by B12/B14/B15a/B15b — but §v2.10 records that they are contract-only, so a later reader does not delete them as dead code. |
| **A4** | architecture | **SHOULD-FIX.** Q5(a) answered "not ambiguous" with a **totality** argument; ambiguity is a property of the **reader**. Post-fix, the meaning of argument 1 is decided by the runtime type of argument 2, four ways — and the JSDoc at `toast.js:1-10` is already false today | **ACCEPTED.** §v2.5 now requires the **JSDoc block** to carry the four-row dispatch table. This does not reopen OD-5 — no caller is migrated — but it fixes the only artefact 22 importing modules can actually read. |
| **A5** | architecture | **SHOULD-FIX.** §v1.10's rollback claim is false twice: reverting "line 15" alone leaves a **parse error** in a module `app.js` imports at the top; and a production-only revert reds **only** `JS Unit (Vitest, non-required)`, which is **not a required context** — a silent red branch protection cannot see | **ACCEPTED, both halves.** §v2.11 restates rollback as a **full PR revert**, and records the silent-red hazard explicitly. |
| **A6** | architecture | **SHOULD-FIX.** "Line 15 only. No other line moves" is false — a multi-line predicate shifts every anchor below, including **CI-10's own evidence anchors** `:60`/`:84`, and `e2e/workout-plan.spec.ts:682` cites `modules/toast.js:14-27` | **ACCEPTED.** Verified: that E2E comment exists at `:682`. §v2.5 restates the change as "one predicate, N inserted lines" and adds a **re-anchoring obligation as the LAST edit before commit**. `e2e/**` joins the path table. |
| **A7 / T-S9** | architecture, test-strategist | **SHOULD-FIX.** PR **#426** (KI-011 Gate 0) is a concurrent lane on the same file and is unsequenced; and the probe is safe only because `vitest.config.js:23`'s `include` is **root-anchored** | **ACCEPTED, both.** #426 is added to §v2.12's sequencing — if it moves any `toast.test.js` case, U3a's three literals and regenerated inventory go stale and **two green sibling PRs red `main`**, this repository's own recorded failure. §v2.8 now states the probe-location constraint **and its reason**. |
| **A8 / T-S1** | architecture, test-strategist | **SHOULD-FIX / BLOCKING.** `isFlag := typeof message === 'boolean'` misses `new Boolean(true)`, `1`, `0` — so KI-010 still fires for them; and the **narrowing** mutation `message === true` is the most plausible mis-implementation and is absent from the matrix | **ACCEPTED, and MEASURED — this is the council's best test finding.** `showToast('error', new Boolean(true))` renders `"true"` on `bg-danger` under S0, S1 **and** S2: the residual is real. And the narrowing mutation is **indistinguishable from the correct predicate against all 47 current cases** — identical red sets `{B43, B45}` under S2 and `{B13, B43, B45}` under S1. **That vindicates the B46 family: killing `message === true` is its only justification, and §v1.8's matrix could not have found it.** Both go into §v2.8. |
| **A9** | architecture | **SHOULD-FIX.** OD-4 says "complete coverage" but no proposed case carries `options` | **ACCEPTED** — same as P8. §v2.6 adds the `(T, <bool>, {requestId})` family. |
| **A10 / T-N/A** | architecture | **SHOULD-FIX.** The `null` asymmetry is unstated: `typeof null === 'object'`, so `showToast(T, null)` stays **modern** | **ACCEPTED.** §v2.3's branch statement now names `null` explicitly. CI-9's survival depends entirely on it. |
| **A12** | architecture | **NOTE, and it cuts AGAINST the new recommendation — recorded for exactly that reason.** S1 is a **value** test so it propagates through indirection; S2 is a **call-shape** test so it does **not**. A forwarding wrapper `f(t,m,o){showToast(t,m,o);}` called as `f('error')` passes `argc = 3`, so S2 sees a modern call. That wrapper shape exists in-repo at `e2e/ui-hardening.spec.ts:31-44` | **ACCEPTED and promoted into §v2.4's comparison table.** This is the strongest argument **for S1** and it must sit beside the strongest argument for S2. OD-2's guarantee that the five one-argument sites are fixed without being edited holds under S2 **only because those five call `showToast` directly** — verified. |
| **A11 / T-N4** | architecture, test-strategist | **NOTE.** `arguments.length` is mechanically safe — **no JS build step**, modules served raw, esbuild at esnext. Caveat: a future refactor to `(...args) =>` silently reverts S2's one-argument fix | **ACCEPTED.** Independently measured here too: `package.json` has only `build:css`; `templates/base.html:282` serves `type="module"`. Recorded in §v2.4 with the durability caveat. |
| **A13** | architecture | **NOTE.** All exotic tuples land correctly — zero-arg, `Object.create(null)`, `new String('error')`, throwing getter. No tuple lands in no branch or both | **ACCEPTED and independently reproduced** (`artifacts/probe/edge_probe.mjs`). Recorded so it is not re-litigated. One measured refinement: a throwing options getter now throws from the spread at `:19` rather than the destructure at `:33` for newly-legacy inputs — different line, same observable outcome. |
| **T-B1** | test-strategist | **BLOCKING.** §v1.9 gate 7 is **unachievable as written** and self-contradictory: `/run-e2e` is the full suite **including** visual specs, whose measured baseline for that invocation is **569 passed / 63 FAILED**; the row demands "exit 0 both times" while its own justification says the default cannot pass. It invites `--update-snapshots`, which `QUALITY_GATE.md` forbids | **ACCEPTED — the single most likely cause of a wasted implementation cycle.** §v2.9 gate 7 is rewritten as two **asymmetric** invocations and the contradiction with the "not in the gate set" line is removed. |
| **T-B4** | test-strategist | **BLOCKING.** AC-7's *"nothing else"* is a claim about the **231-case** suite; §v1.8 measures it over the **47-case** probe | **ACCEPTED.** Verified the probe generalises — measured: `exercises.test.js:66`, `exports.test.js:5` and `fetch-wrapper.test.js:5` all `vi.mock('../toast.js', …)`, and **`toast.test.js` is the only file importing the real module**. §v2.8 adds a **full `npm run test:js`** arm and records those three mock lines as the reason the probe generalises. |
| **T-S2** | test-strategist | **SHOULD-FIX.** Nine of the twelve proposed cases (B45b/c/d, B46b/c/d, B43b/c/d) have **no independent kill**, and this repository's precedent (§10.5's B43 disclosure, D-h) makes disclosure mandatory | **ACCEPTED.** §v2.6 carries the disclosure verbatim in the file, in the B15a/B15b idiom. The sharper half is also recorded: after the fix, B45a–d and B46a–d are insensitive to `validTypes` membership entirely. |
| **T-S3** | test-strategist | **SHOULD-FIX.** Step 6's *"must red broadly"* is the only arm with no exact expected set — and it is the arm most exposed to the BAD-RUN mode the section itself names | **ACCEPTED.** Every arm in §v2.8 now carries an **exact expected failing set and an exact collected count**. Step 6 is replaced by the **measured** `drop-isTypeWord` arm, which reds `{B8, B43, B45}` (+`B13` under S1) — a precise oracle rather than "broadly". |
| **T-S4** | test-strategist | **SHOULD-FIX.** Gate 1's pass condition is **circular** — "collected count equals the measured figure" is satisfied by any number — and `vitest list` cannot see a `.skip` | **ACCEPTED. This is a genuine false-green and it is now closed.** §v2.9 gate 1 is a **three-way reconciliation**: diff-derived expected count == `vitest run` collected == the pinned literal, **plus** a `.only`/`.skip`/`.todo` grep, **plus** the regenerated `vitest.cases` must literally contain each new title. Local `vitest run` does not fail on `.only` — `allowOnly` is unset, so that protection exists only under `CI=true`. |
| **T-S5** | test-strategist | **SHOULD-FIX.** §v1.9's path table omits files, and the *"`tests/**` → Targeted-test derivation"* citation is **wrong** — `QUALITY_GATE.md` has no `tests/**` row and no `tests/X.py` bullet | **ACCEPTED. The conclusion was right and the derivation was not**, which is exactly the kind of error that survives review by being correct. §v2.9 now derives full pytest and full E2E from the **empty-union fallback** (`QUALITY_GATE.md`, *"If the union is empty, run `/verify-suite`"*), with the 22-importer / 15-spec blast-radius measurement offered as **corroboration, not authority**. |
| **T-S6** | test-strategist | **SHOULD-FIX.** §v1.9 drops the **`tsc --noEmit`** half of a required context | **ACCEPTED.** Added to §v2.9. |
| **T-S7 / A18** | test-strategist, architecture | **SHOULD-FIX.** *"All 18 jobs green"* is pinned as a literal against a known **17 → 18 mid-run growth** hazard | **ACCEPTED.** §v2.9 gate 9 now reads *"poll to zero-pending, then re-read `total_count`"*. |
| **T-S1b** | test-strategist | **SHOULD-FIX.** Two omitted off-by-one mutations: S1's `== undefined`, and S2's `argc !== 2` — the latter *"killed by B19 only"*, with **B10 blind to it** | **ACCEPTED, with one correction from measurement.** `== undefined` reds `{B12, B14, B15a, B15b, B43, B45, B13}` — existing cases already kill it, as predicted. But `argc !== 2` reds **nine** cases (`B19–B23`, `B33`, `B34`, `B43`, `B45`), not "B19 only". The **conclusion holds and is stronger than stated**; the detail is corrected. **B10 is indeed blind to it** — confirmed, and B10 is CI-2's sole pin. |
| **T-N1 / T-N2 / T-N3** | test-strategist | **NOTE.** §v1.7 arithmetic correct; only **two** lines change (`:57`, `:67`), `:58` is re-confirmed; the three literals are the complete set; the zero-node-delta claim is correct | **ACCEPTED.** Independently reproduced here: the file's only `@pytest.mark.parametrize` (`:387`) uses four fixed entries, so the node count stays **46** whatever the Vitest case count. §v2.7 corrects "three literals" to "two edited, one re-confirmed", and §v2.9 gate 5 now requires **recording a baseline first** (`CLAUDE.md` §4.B). |
| **T-N4** | test-strategist | **NOTE.** E2E blast radius is smaller than §v1.2 implies — only **three** specs call `showToast`, all modern three-argument with string messages; **no E2E spec can red on this change** | **ACCEPTED, and it changes how the E2E tier must be read.** §v2.9 records that E2E is a **regression net, not an oracle for AC-1** — a green E2E run is not evidence the fix works. |
| **A14–A17, T-N5, T-N7, T-N8** | both | **NOTE.** No module-boundary or import-graph risk; §v1.8 steps hand-checked sound; no `conftest.py` work; the OD-1 "restart cost is zero" reasoning holds and the ledger arithmetic backs it | **ACCEPTED, no change required.** Recorded so a later reader knows they were examined. |

### What the council did NOT dislodge

- **The mechanism** (§0.2), the **nine outcomes** (§0.3), the **8 + 5 caller inventory** (§0.4) and the
  **three pinning layers** (§0.6) — all re-measured on `db6c34b` and all reproduced.
- **OD-1, OD-3, OD-4 and OD-5** were not challenged by any reviewer.
- **The fix itself.** No reviewer proposed a different production change. All three attacked the
  *spelling*, the *evidence*, and the *gates* — not the predicate.
- **Ledger rows 14 and 15**, and the merge-order precondition attached to them.

---

## Plan v2 — Gate 1

*Plan v2 is Plan v1 revised by the council. **Plan v1 is left above exactly as it was written**, per
the house rule that a plan is superseded in place and never rewritten — every figure it carries was
true when measured, and the two it got wrong are corrected here, not erased.*

### v2.0 Scope amendment — the ledger edit (finding A1)

Signed §0.9 puts the `STEP12_JS_UNIT_GATE0.md` ledger out of scope: *"those rows are owed — but by
the packet that owns that document, not by this one."* **The owner amended that on 2026-08-27**, in
the same instruction that ordered U2 first:

> *"You are authorized to edit planning/ledger documentation … Record each still-unclaimed result
> once, in actual merge order."*

U3a therefore appends **rows 14 and 15** to §13.0 and adds that file to the path table at §v2.9.
**The amendment is recorded here rather than left implicit**, because a signed boundary that is
crossed silently is worse than one that is crossed openly. **Ratification is OD-9.**

### v2.1 Ordering ruling and ledger disposition — unchanged from §v1.1

§v1.1 stands as written. The owner's ordering ruling discharges §0.13 condition 4 for Gate 1
planning only; rows **14** and **15** and their merge-order precondition are unchanged.

### v2.2 Re-measured substrate — §v1.2, plus a visibility column

Every figure in §v1.2 reproduced on `db6c34b`. **§v1.2's caller table gains a visibility column**
(finding P3):

| Site | Shape-collision-capable | Actually visible to a user |
|---|---|---|
| `workout-plan.js:114` | yes | **No** — guarded by `if (!error.code)`, and `normalizeError` sets `code` on all four branches, so the guard is always false for an API error |
| `filters.js:251` | yes | **No** — `:255` raises an unconditional toast in the same tick; under KI-004 the user never sees `:251` |
| the other **6** two-argument sites | yes | yes |
| the **5** one-argument sites | yes | yes |

**So the shape count is 13 and the visible count is 11.** **AC-8 is amended** to require the KI-010
row to carry both.

### v2.3 The disambiguation contract — stated separately per spelling (finding A2, A10)

`VALID = {'success','error','warning','info'}`; `argc` = arguments actually passed.

```
isTypeWord := VALID.has(type)
isFlag     := typeof message === 'boolean'      // NOTE: typeof null === 'object', so null is NOT a flag
                                                //       and `new Boolean(true)` is NOT a flag either
isAbsent   := S1: message === undefined         // a function of argument VALUES
              S2: argc < 2                      // a function of CALL SHAPE

isModern   := isTypeWord AND (NOT isFlag) AND (NOT isAbsent)
```

- **S1 is a total function of the argument values.** Every `(type, message, options)` triple lands in
  exactly one branch.
- **S2 — RULED, and this is the shipping contract.** A total function of the **call shape and the
  argument values**. `argc` is not a type, so §0.13 condition 5's original wording did not cover
  it; **the owner amended that condition on 2026-08-27** (see §0.13) so the contract may depend on
  argument types **and** call shape/arity. The amendment is recorded there, not assumed here.
- **`null` is explicitly modern.** `showToast(T, null)` renders the default copy, under both
  spellings, before and after. **CI-9's survival depends entirely on this** and it was unstated in
  Plan v1.

### v2.4 S1 versus S2 — the comparison the owner rules on

**Measured against the real `toast.test.js` in the mirrored probe** (`artifacts/probe/`, gitignored;
pristine control = **47 passed (47)**, exit 0):

| Arm | Exit | Result | Cases that red |
|---|---:|---|---|
| **S0** pristine | 0 | 47 passed (47) | *(none)* |
| **S1** | 1 | 3 failed \| 44 passed | **B13, B43, B45** |
| **S2** | 1 | 2 failed \| 45 passed | **B43, B45** |

**Nothing else reds under either.** B5–B11, B12/B14/B15a/B15b, B16–B29, **B30–B35 (KI-011, CI-10)**,
B42/B44 all stay green. **That is AC-3's evidence.**

**Rendered behaviour is identical under S1 and S2 for all nine outcomes and all controls.** They
diverge on one *class* of input — **not one input**, as Plan v1 claimed (finding T-B2):

> `{ showToast(T, u, …rest) : T ∈ VALID, u evaluates to undefined at runtime, argc ≥ 2 }`

| | **S1** — `message === undefined` | **S2** — `argc < 2` |
|---|---|---|
| `showToast(T, <undefined>)` | **`T` on `bg-success`** — a **severity inversion**: a red error toast becomes a green one | **default copy on the type's own class** — today's behaviour, preserved |
| Three-argument form `showToast(T, <undefined>, {duration})` | legacy; duration honoured | modern; today's behaviour |
| **B13** | **reds; must invert — and the inverted case then ASSERTS the severity inversion as correct** | stays green, untouched |
| Reachable today? | **No** — all 13 bare-expression sites are guarded at assignment. But **not structurally**: [`workout-plan-helpers.js:210`](../../static/js/modules/workout-plan-helpers.js#L210) forwards `message` unguarded, its two callers supply the `\|\|`, and **no test pins that guard** | same population, but the outcome if it ever fires is **benign** |
| **Propagation through indirection** (finding A12) | **Propagates** — a value test survives forwarding wrappers, `apply`, spread | **Does not propagate** — `f(t,m,o){showToast(t,m,o)}` called as `f('error')` passes `argc = 3`, so S2 reads it as modern. That wrapper shape exists at `e2e/ui-hardening.spec.ts:31-44` |
| Mechanical availability | trivially | **Measured available**: `arguments.length` is 1 vs 2 despite the non-simple parameter list, and survives `apply`/spread. **No JS build step exists** — only `build:css`; modules are served raw as `type="module"` — so nothing rewrites `arguments` |
| Durability caveat | none | a future refactor to `(...args) =>` **silently reverts** the one-argument fix, with B13 saying nothing about arity |
| §0.13 condition 5 | satisfied as worded | **requires an amendment** (finding A2) |
| Predicted `toast.test.js` / suite | **57 / 241** (B13 single) or **60 / 244** (B13 parametrised — OD-7) | **57 / 241** |
| Mutation consequence | B13 and B43 detect the **same** conjunct — an equivalence class needing disclosure | B13's **only** kill is the rival-spelling arm; B43 gains its **first independent kill** |

> ## ✅ **OD-6 RULED 2026-08-27 — S2.**
>
> **`isAbsent := arguments.length < 2`.** An **explicitly supplied `undefined` remains modern-call
> behaviour** and must not trigger the legacy green-toast path. **S1 is not adopted.**
>
> Consequences, all binding on implementation:
>
> - **B13 is untouched.** `showToast('error', undefined)` keeps rendering
>   `"An unexpected error occurred."` on `bg-danger`, and B13 stays green in every arm.
> - **The characterization set is exactly {B43, B45}** — two inverted cases, not three.
> - **§0.13 condition 5 is amended** (see the amendment block at §0.13). The contract may depend on
>   argument types **and call shape/arity**.
> - **The durability caveat is now a live obligation, not a footnote:** a future refactor of
>   `showToast` to `(...args) =>` silently reverts the one-argument fix. §v2.6 pins arity
>   explicitly so that refactor reds.
> - **The S1-only risk is closed by construction** — no runtime-`undefined` message can reach the
>   legacy branch, so the severity inversion the council found cannot occur.

**PLAN v2 REVERSED PLAN v1 AND RECOMMENDED S2; the owner ruled S2 on 2026-08-27.**

The reason is single and measured: **S1 converts a red error toast into a green one for any modern
call whose message expression evaluates to `undefined` at runtime, and the inverted B13 would assert
that as the contract.** That is the same defect class — severity inversion — that this packet exists
to remove, reintroduced by the fix, and pinned as correct. S2 leaves that input exactly as it
behaves today. The population is **0** today under both, but it is 0 by a `||` at each of 13 call
sites, none of which is pinned by any test, and one of which (`workout-plan-helpers.js:210`)
forwards unguarded.

**Plan v1's three reasons for S1 are answered:** (1) §0.13 condition 5 names the S1 wording — but
that condition is amendable and A2 shows it must be touched either way; (2) "no dependence on
`arguments`" is a real durability point and is why the caveat above is stated rather than buried;
(3) "B13 pins an input no caller makes" was the syntactic-oracle error itself.

**The honest case for S1 remains A12: it propagates through indirection and S2 does not.** If the
owner weighs future forwarding wrappers above the severity-inversion risk, S1 is the correct ruling
and this recommendation should be overridden. **Plan v2 does not choose.**

> ✅ **RESOLVED 2026-08-27 — the owner ruled S2**, i.e. granted Plan v2's recommendation and declined
> the A12 counter-argument above. The paragraph is left standing as the honest case it was: **A12 is
> a real property of S2 and it did not go away by being outvoted.** Its live consequence is the
> durability obligation now carried by B13's comment (§v2.6) and by mutation arm **5f** (§v2.8).

### v2.5 Exact production change (findings A4, A6)

| File | Change |
|---|---|
| [`toast.js`](../../static/js/modules/toast.js) | **One predicate, N inserted lines** at `:15` — *not* "line 15 only". The `const isLegacyCall = …` statement replaces the bare `if`. |
| same | **The JSDoc at `:1-10` must carry the four-row argument-2 dispatch table.** It currently says `@param {string} message`, which is already false today. This is the only contract artefact the 22 importing modules can read. |
| same | The comment at `:14` describes the new rule. |

**Re-anchoring obligation — the LAST edit before commit.** Inserting lines shifts every anchor below
`:15`. At minimum: §v1.2's anchor table; **CI-10's evidence anchors `:60` and `:84`**, which are what
prove KI-011 is untouched; and `e2e/workout-plan.spec.ts:682`, which cites `modules/toast.js:14-27`
in a pinned comment. **Re-anchor by measuring, never by adding a constant offset.**

**Disclosed, not hidden:** the legacy body at `:16-27` now executes for an input class it never ran
for. For those inputs `options` becomes a shallow copy (`{...options}` at `:19`), so
prototype-inherited keys are dropped and an options getter fires at `:19` rather than at `:33`.

### v2.6 Test design (findings A9, P8, T-S2)

B45a–d, B46a–d, B43a–d as in §v1.6, **plus**:

| Case family | Shape | Why |
|---|---|---|
| **B47a–d** | `showToast(T, <bool>, { requestId: 'R1' })` | **Measured new behaviour, pinned by nothing today:** `showToast('error', false, {requestId:'R1'})` renders `"false (Request ID: R1)"` / `bg-danger` before and **`"error"` / `bg-success` with the suffix SILENTLY DROPPED** after — under both spellings. Disposition is **OD-11** |
| **B13** | `showToast('error', undefined)` | ✅ **ASSERTIONS UNTOUCHED — OD-6 ruled S2.** It keeps asserting `"An unexpected error occurred."` on `bg-danger` and **must stay green in every arm**. Under OD-7 the S1-only parametrisation is **not** added. B13 is now the case that pins *"an explicitly supplied `undefined` is still a modern call"*, and its **only** mutation kill is the rival-spelling arm (§v2.8 step 4) — which is therefore mandatory. **Its COMMENT must be rewritten** to state the arity dependence explicitly — that the distinction rests on `arguments.length`, and that a refactor of `showToast` to `(...args) =>` must carry `args.length` with it. That is the discharge of OD-6's durability obligation (see the withdrawn B48 row below for why it is a comment and not a case) |
| ~~**B48**~~ | ~~an arity-pinning case~~ | ❌ **PROPOSED, THEN MEASURED, THEN WITHDRAWN — 2026-08-27.** Plan v2 proposed a new case to guard OD-6's named durability risk, claiming a rest-parameter rewrite would red *"exactly B48"*. **The claim was measured and is false** (harness `artifacts/probe/b48_probe.mjs`). Two results: a **faithful** rewrite keeping `args.length < 2` **preserves the behaviour entirely** — the refactor is not inherently breaking; and a **careless** rewrite that drops the conjunct (because `arguments` is unavailable in an arrow function) makes `showToast('error')` modern again, which **B43a–d already kill**. So B48 would have had **no independent mutation kill**, and adding it would have been test bloat dressed as a guard. **The obligation is discharged by documentation instead** — see the B13 row above. *Recorded rather than quietly dropped, because a proposal that fails its own measurement is evidence, not an embarrassment.* |

**Mandatory disclosure, in the file, in the B15a/B15b idiom** (finding T-S2): **nine of the twelve
new cases — B45b/c/d, B46b/c/d, B43b/c/d — have no independent mutation kill**, because the
predicate contains no per-type branch. They defend against a *future* per-type implementation. The
sharper half must also be stated: after the fix, B45a–d and B46a–d are insensitive to `validTypes`
membership entirely — removing `'warning'` from `:12` leaves B45b green.

### v2.7 Inventory arithmetic

**Under the rulings (S2; OD-11 pins B47; OD-7 adds nothing; B48 withdrawn on measurement):**
`47 − 2 (B43, B45 removed) + 12 (B43a–d, B45a–d, B46a–d) + 4 (B47a–d) = **61**` for
`toast.test.js`, and `231 + 14 = **245**` for the suite. `EXPECTED_TOTAL_FILES` stays **13**.
**Two literals are edited (`:57`, `:67`); `:58` is re-confirmed, not edited** (finding T-N1).

> **This is arithmetic on a design, not a signed count.** OD-4 refuses to sign a case count and
> that refusal stands. **The implementation measures `vitest list` and sets the literals from the
> measurement**; if the measured figure differs from 62 / 246, the *measurement* wins and the
> discrepancy is investigated before the literals are touched.

### v2.8 Mutation and negative-control procedure — every arm with an exact oracle

Probe as §v1.8. **The probe must live outside `static/js/`**, because `vitest.config.js:23`'s
`include` is root-anchored at `static/js/**/*.test.js` and `generate_test_inventory.py` collects
through the same glob — a probe inside it would double-collect and red gates 1 and 3 (finding T-S9).

**The probe generalises to the full suite, and here is why** (finding T-B4): `exercises.test.js:66`,
`exports.test.js:5` and `fetch-wrapper.test.js:5` all `vi.mock('../toast.js', …)`, and
**`toast.test.js` is the only file that imports the real module**.

| Step | Arm | Exact required outcome |
|---:|---|---|
| **0** | Pre-flight, pristine | exit **0**, **`47 passed (47)`**. Any other collected count is **BAD RUN** |
| **1** | Fix + pristine tests | exit **1**, collected **47**, reds **exactly** `{B43, B45}` — **measured under the ruled S2 spelling** |
| **1b** | **Full `npm run test:js`** with fix + pristine tests | exit **1**, collected **231**, same red set. **This is the arm that makes AC-7's "nothing else" a claim about the real suite** |
| **2** | Pristine + new tests | exit **1**, reds **exactly** the new and inverted cases |
| **3** | The pair | exit **0**, collected = the measured §v2.7 figure |
| **4** | **Rival spelling** (S1 as the rival), both directions | reds **exactly `{B13}`** — **measured**. This is B13's only kill, so the arm is mandatory, not optional |
| **5a** | drop `isFlag` | reds **exactly** `{B43}` against pristine tests — **measured** |
| **5b** | drop `isAbsent` (`arguments.length < 2`) | reds **exactly** `{B45}` — **measured** |
| **5c** | **NARROW `isFlag` → `message === true`** | **MEASURED: indistinguishable from correct against all 47 current cases** — identical red sets. **B46a–d exist to kill this and nothing else.** Must also be run as `message === false` |
| **5d** | ~~S1 only: `== undefined`~~ | **DROPPED — OD-6 ruled S2**, so this arm mutates a conjunct the shipped code does not contain. Its measurement (`{B12, B14, B15a, B15b, B13, B43, B45}`) is retained above as the evidence it was |
| **5e** | **`argc !== 2`** — the off-by-one on the ruled conjunct | reds **nine**: `{B19–B23, B33, B34, B43, B45}` — **measured**. **B10 is blind to it**, and B10 is CI-2's sole pin. **Now a required arm, not an optional one** |
| **5f** | **drop the `arguments.length` conjunct entirely** — the careless `(...args) =>` rewrite | reds **exactly** `{B43a–d}` — **measured**, and this is the corrected oracle: Plan v2 first predicted a dedicated case would be needed and the measurement showed **B43a–d already cover it**. A *faithful* rewrite carrying `args.length < 2` changes nothing and must stay **green** — run both directions |
| **6** | drop `isTypeWord` | reds **exactly** `{B8, B43, B45}` — **measured**. Replaces §v1.8's *"must red broadly"*, which had no oracle |

**Judging rules.** Judge by exit code **and** collected count together — a run that exits 1 with
**zero** collected is a **BAD RUN**, hit for real while producing this table by passing an
unsupported `--reporter=basic`. And a wrong probe path fabricates a survivor; step 0 is the guard.

### v2.9 Gate set — corrected derivation (findings T-S5, T-B1, T-S4, T-S6, T-S7)

**Paths the implementation PR will change:** `static/js/modules/toast.js`;
`static/js/modules/__tests__/toast.test.js`; `docs/test_inventory/*`;
`tests/test_vitest_inventory_contracts.py`; `docs/UI_SCENARIOS_GAP_ANALYSIS.md` (**rows `:105` and
`:208`**); `docs/toast_type_word_collision/PLANNING.md`;
**`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md`**; and **`e2e/workout-plan.spec.ts`** (the `:682`
citation only).

**Correct derivation:** `toast` hits **no row** in `QUALITY_GATE.md`'s feature map, and there is **no
`tests/**` row**. Both therefore reach the **empty-union fallback** — *"If the union is empty, run
`/verify-suite`"* — which is the authority for full pytest **and** full Chromium E2E. The
22-importer / 15-spec blast-radius measurement is **corroboration, not authority**.

| # | Gate | Pass condition |
|---:|---|---|
| **1** | `npm run test:js` | **Three-way reconciliation**: diff-derived expected count **==** `vitest run` collected **==** the pinned literal; **plus** a `.only`/`.skip`/`.todo` grep over `toast.test.js`; **plus** the regenerated `vitest.cases` must literally contain each new title. *(Local `vitest run` does not fail on `.only` — `allowOnly` is unset, so that guard exists only under `CI=true`)* |
| **2–4** | inventory regenerate, `--check`, determinism ×3 | as §v1.9 |
| **5** | Full pytest | **Record a baseline first** (`CLAUDE.md` §4.B). Delta must be **zero** new nodes — verified: the file's only `parametrize` uses four fixed entries, so its node count stays **46** |
| **6** | **`tsc --noEmit`** *and* `pyright_baseline_diff.py` | both — the required context is two blocking steps |
| **7** | **E2E, two ASYMMETRIC invocations** | **(a)** full Chromium **excluding** `visual*.spec.ts` (~549), exit 0. **(b)** `PW_VISUAL_SEED=1` **scoped to the visual specs** (~100), reconciled against `MASTER_HANDOVER.md`'s Windows ledger. **Never `--update-snapshots`.** The single default invocation reds ~63 on unmodified surfaces and **cannot pass** |
| **8** | Manual smoke | **Console-invoke** `showToast('error', true)` and `showToast('warning')` on a loaded page; record body, `bg-*` class and the live-region announcement. Exercising a real caller **cannot reach the fix** |
| **9** | PR CI | **Poll to zero-pending, then re-read `total_count`** — never pin the integer 18 |
| **10** | `/unslop` | `code-reviewer` + `unslop-reviewer` |
| **11** | Ledger | the implementation PR's own post-merge row is owed |

**E2E is a regression net, not an oracle for AC-1** (finding T-N4): only three specs call
`showToast`, all modern three-argument with string messages, so **no E2E spec can red on this
change**. A green E2E run is not evidence the fix works.

### v2.10 User-facing limitations — stated, not softened (findings P4, P5, P6, P11, P13, P10)

- **The fix restores fidelity, not quality.** `showToast('success', true)` becomes a **red** toast
  whose entire body is the word `"success"`. The severity channel is now right and the text channel
  contradicts it. That is less wrong than `"true"`, and it is not good copy.
- **Under the legacy form, severity comes from the boolean and never from the message** — so
  `showToast('warning', true)` is **red** by design. Permanent property, not a second bug.
- **Accessibility.** `#liveToast` is `role="alert"`, `aria-live="assertive"`, `aria-atomic="true"`,
  and severity is conveyed **only** by the `bg-*` class — no icon, no visually-hidden prefix. The
  announced string changes for all nine outcomes, from a sentence to a single context-free word, and
  a screen-reader user cannot distinguish a red `"success"` from a real success.
- **Both default-copy strings are already production-unreachable** and survive as the dispatcher's
  contract for an explicit `null`, pinned by B12/B14/B15a/B15b. Not dead code.
- **Residual, disclosed:** `isFlag` uses `typeof`, so `new Boolean(true)`, `1` and `0` are **not**
  flags — `showToast('error', new Boolean(true))` still renders `"true"`, measured under S0, S1 and
  S2. **CI-6/B8 makes a non-boolean second argument contract-legal**, so a legacy caller writing
  `showToast(msg, isError ? 1 : 0)` still trips KI-010 after the fix.
- **Preventing a bare type word from reaching the dispatcher is a server-side concern, deliberately
  left open** — it is OD-1's declined residual.

### v2.11 Rollback (finding A5)

**Rollback is a full PR revert.** Reverting `toast.js:15` alone leaves an orphaned `const` or a
dangling `||` — a **parse error** in a module `app.js` imports at the top, which takes down every
page.

**And a production-only revert is a SILENT red.** The inverted cases would fail, but
`EXPECTED_TOTAL_CASES` / `EXPECTED_PER_FILE` count cases, not outcomes — so `Test Inventory Drift`
and `Run Tests` both stay **green**, and the only red is `JS Unit (Vitest, non-required)`, which is
**not a required context**. Branch protection cannot see it. **Never revert production alone.**

### v2.12 Sequencing (finding A7)

⚠️ **RECONCILED 2026-08-27 (integration pass) — steps 1 to 4 are DISCHARGED; step 5 alone still
binds.** The list below is Plan v2's prose as signed and is not rewritten. Measured against merged
`main` at `f9726a3`: **#427 merged (`efa780c`)**, **#426 merged (`5b35966`)**, **#428 — the Gate 1
planning PR — merged (`a37d7e7`)**, and implementation is complete and green. The step-3
precondition it names, `gh pr view 427 --json state` reporting `MERGED`, was **re-read at this pass
and reports `MERGED`**. **Nothing in steps 1–4 is an open blocker.** Step 5 — OD-1's embargo — is,
and **reaching `2026-09-05T17:59:26Z` is not itself merge authorization.**

1. **#427 merges first** (owner ruling). Not authorized here.
2. **#426 is RESOLVED BY MEASUREMENT, not by waiting.** Measured `2026-08-26T23:50:36Z`:
   `gh pr diff 426 --name-only` returns **exactly one file**,
   `docs/toast_action_continuity/PLANNING.md` — a docs-only Gate 0 candidate that touches **no**
   `static/js` path and therefore **cannot move a Vitest case**. The finding A7 hazard is real in
   general and **does not apply to #426 as it currently stands**. **This must be re-measured, not
   assumed, if #426 gains a commit**; gates 2–5 re-run after any rebase regardless.
3. This Gate 1 planning PR merges once Gate 1 is signed **and** `gh pr view 427 --json state` reports
   `MERGED` — the row-14/15 precondition.
4. Implementation begins.
5. **The implementation PR may not merge before `2026-09-05T17:59:26Z`** (OD-1).

### v2.13 Open owner decisions carried to Gate 1 sign-off

| | Decision | Plan v2 position |
|---|---|---|
| **OD-6** | **S1 or S2** | ✅ **RULED 2026-08-27 — S2.** `arguments.length < 2`; an explicit `undefined` stays modern. §0.13 condition 5 amended. |
| **OD-7** | Under S1 only: parametrise B13 over four type words (60/244) or leave it single (57/241)? | ✅ **RULED N/A 2026-08-27.** S2 was chosen, so B13 is never inverted. **The S1-only parametrisation must NOT be added.** |
| **OD-8** | **§0.3 row 6's intent cell is wrong** — it says `showToast('error')` means a *red* toast; B5 fixes the legacy one-argument contract as **green**. Correct the signed cell? | ✅ **RULED 2026-08-27 — CORRECT IT.** Applied at §0.3, annotated in place. |
| **OD-9** | Ratify the §0.9 ledger-scope amendment (§v2.0) | ✅ **RATIFIED 2026-08-27.** Applied at §0.9. |
| **OD-10** | `STEP12_JS_UNIT_GATE0.md` §10.3/§10.5 go stale — the 47-case arithmetic, B43/B45's present-tense rows, N8/N10/N12's kill sets, and **two signed Gate 1 checkboxes**. Re-derive in the implementation PR, or land a dated stale-pointer annotation? | ✅ **RULED 2026-08-27 — Plan v2's proposal ACCEPTED.** A **dated stale-pointer annotation** lands in the implementation PR; §10.5 is **not** re-derived here. **Measured at implementation time:** the annotation itself shifted those checkboxes, which then sat at `:2095` and `:2108` — the `:2054`/`:2067` figures in the council row above were the pre-annotation reading and are left as that record. ⚠️ **RE-MEASURED 2026-08-27 (integration pass): they now sit at `:2102` and `:2115`**, because this pass extended the same annotation by seven lines. Measured, not offset. |
| **OD-11** | The **requestId suffix drop** on `showToast(T, false, {requestId})` — pin it with B47a–d, or accept it unpinned? | ✅ **RULED 2026-08-27 — PIN IT.** B47a–d ship. |


---

### Gate 1 sign-off — **SIGNED 2026-08-27**

**Gate 1 is SIGNED.** All six open decisions were ruled by the owner on 2026-08-27 and the plan of
record is **Plan v2 as amended by those rulings**.

| | Decision | Ruling |
|---|---|---|
| **OD-6** | S1 or S2 | ✅ **S2** — `arguments.length < 2`. An **explicitly supplied `undefined` remains modern-call behaviour** and must not trigger the legacy green-toast path. **§0.13 condition 5 amended on the record** so the contract may depend on argument types **and call shape/arity** |
| **OD-7** | B13 parametrisation | ✅ **N/A under S2.** The S1-only inverted parametrisation is **not** added |
| **OD-8** | §0.3 row 6's intent cell | ✅ **Corrected** — B5 fixes the legacy one-argument contract as **green**. Applied at §0.3, annotated in place |
| **OD-9** | §0.9 ledger-scope amendment | ✅ **Ratified.** Applied at §0.9 |
| **OD-10** | §10.3 / §10.5 staleness | ✅ **Plan v2's proposal accepted** — a dated stale-pointer annotation in the implementation PR; §10.5 is not re-derived |
| **OD-11** | requestId-suffix drop | ✅ **Pinned** — B47a–d ship |

**One Plan v2 proposal did not survive its own measurement and was withdrawn before signing.** Plan
v2 proposed a new case **B48** to guard OD-6's named durability risk. The claim that a
rest-parameter rewrite would red *"exactly B48"* was **measured and is false**: a faithful rewrite
preserves the behaviour, and a careless one is already killed by **B43a–d**. B48 is withdrawn, the
obligation is discharged by rewriting **B13's comment** instead, and the case count falls from the
proposed 62 to **61**. The withdrawal is recorded at §v2.6 rather than quietly dropped.

#### What the signature authorises

**Implementation may begin**, against Plan v2 as amended, in the **S2** spelling.

#### What the signature does NOT authorise — unchanged and still binding

- **It is not merge authorisation for anything.** **OD-1 remains binding: no U3a implementation PR
  may merge before `2026-09-05T17:59:26Z`, and passing that instant is neither implementation
  authorization nor merge authorization.**
- **It does not authorise merging this planning PR**, PR **#427**, or PR **#426**. ⚠️ **RECONCILED
  2026-08-27:** all three have since merged under the owner's own authorization, not this
  signature's — **#426 `5b35966`**, **#427 `efa780c`**, **#428 `a37d7e7`**. The bullet stands as the
  record of what the Gate 1 signature did and did not confer; it is **not** a live blocker, and it
  never covered the implementation PR, which OD-1 governs separately.
- **The ledger row numbers stay conditional.** Measured `2026-08-26T23:50:36Z`: **#427 is `OPEN` and
  unmerged**. Rows **14 / 15 / 16** hold only if #427 lands row 13 first. `gh pr view 427 --json
  state` must report `MERGED`, and the numbers must be re-confirmed against §13.0's then-current
  last row, immediately before this PR merges.

  ⚠️ **RECONCILED 2026-08-27 — this precaution fired, and it fired the right way.** The rows it
  guarded were **claimed by PR #429 first**, and U3a's block was **withdrawn in full** rather than
  restated (§13's withdrawal note). The re-confirmation this bullet demands is therefore **done and
  its answer is: U3a writes no ledger row at all**. Measured against merged `main`: rows **13–16**
  belong to #429 (`ec1a5cb`), rows **17–19** to #432 (`1211915`). **Rows 20 and 21 — the post-merge
  `js-unit` results of #432 itself (`1211915`, job `98488650519`, `success`, `2026-08-27T10:37:48Z`)
  and of #427 (`efa780c`, job `98491338039`, `success`, `2026-08-27T10:48:05Z`) — are MEASURED AND
  UNCLAIMED.** They are recorded here as evidence only; **this PR does not write them**, because its
  own withdrawal note states that U3a writes no ledger row, and falsifying that note to claim them
  would be the double-entry hazard the note exists to prevent.
- **It does not close KI-011**, a separate packet with its own Gate 0 (PR #426). ⚠️ **RECONCILED 2026-08-27: KI-011 is
  CLOSED and SHIPPED** — PR #426 merged as `5b35966`, post-merge `main` 18/18. It is no longer a
  pending sibling; it is the baseline U3a's implementation must be rebased onto.
- **It does not close OD-1's open residual**: for the remainder of the window, any new
  `error_response('error', …)` makes KI-010 live, and the owner declined to rule that out.

#### The contract being implemented, in one place

```
VALID      = {'success','error','warning','info'}
isTypeWord = VALID.has(type)
isFlag     = typeof message === 'boolean'      // null and new Boolean() are NOT flags
isAbsent   = arguments.length < 2              // an explicit `undefined` is NOT absent
isModern   = isTypeWord && !isFlag && !isAbsent
```

**Production diff: one predicate in `toast.js`, plus the JSDoc dispatch table. No other production
file may change** (AC-10, tightened by OD-5).

#### Standing limitations the signature accepts

§v2.10 in full, and specifically: the fix restores **fidelity, not quality** — a legacy
`showToast('success', true)` becomes a **red** toast reading `"success"`; the assertive live region
now announces a single context-free word; and `new Boolean(true)` / `1` / `0` remain **uncovered**
while CI-6/B8 keeps them contract-legal.

---

## Implementation record — 2026-08-27

*Executed against `origin/main` at **`b733c14f8e76c7f85b1d9dcc75acd8bca8321524`**, in the isolated
worktree `Hypertrophy-Toolbox-v3-main-u3a-impl` on branch `feat/u3a-ki010-toast-collision`, under
**Gate 1 as signed** and in the **S2** spelling ruled by **OD-6**.*

*⚠️ **INTEGRATED 2026-08-27.** `b733c14` is **pre-KI-011**: its `toast.js` is **111 lines** and
carries no action slot. The branch has since merged `main` — most recently `f9726a3` — so the file
this record describes now sits on top of KI-011 (PR #426, `5b35966`) and is **353 lines**. Every
line anchor below was **re-measured against the integrated file**; the pre-integration readings are
preserved as superseded rather than deleted.*

> **OD-1 STILL BINDS. This implementation may NOT merge before `2026-09-05T17:59:26Z`**, and passing
> that instant is neither implementation authorization nor merge authorization.
>
> ⚠️ **RECONCILED 2026-08-27 (integration pass).** The ordering condition this blockquote used to
> carry — *"#427 must also merge first"* — is **discharged by measurement**: #427 merged as
> `efa780c`. So did the two other PRs the Gate 1 signature withheld authorization for — **#426 as
> `5b35966`** and the **Gate 1 planning PR #428 as `a37d7e7`**. This PR is consequently **based on
> `main`**, not stacked on #428. **OD-1 is now the sole remaining merge blocker**, and reaching
> `2026-09-05T17:59:26Z` is not itself merge authorization. The §13.0 ledger row numbers must still
> be re-confirmed against the then-current last row immediately before merge: §13.0 stands at **row
> 23** on `main` at `f9726a3`, and **U3a writes no row of its own** (§v2.1's withdrawal note). The
> next row is owed by whoever merges this PR, against its **post-merge `main`** `js-unit` result.

### i.0 Baselines, recorded FIRST (`CLAUDE.md` §4.B)

| Baseline | Value |
|---|---|
| `npx vitest run` | **13 files / 231 tests**, exit 0 |
| `pytest tests/ -q` | **3175 passed, 2 skipped**, exit 0 |
| `generate_test_inventory.py --check` | `Test inventory is up to date.`, exit 0 |

### i.1 The production change — one predicate, as planned

`static/js/modules/toast.js`. The single `if (!validTypes.has(type)) {` — at `:15` on the
implementation base `b733c14`, and at **`:187`** on merged `main` (`f9726a3`) once KI-011 had landed
— became:

```js
const isLegacyCall = !validTypes.has(type)
    || typeof message === 'boolean'
    || arguments.length < 2;

if (isLegacyCall) {
```

plus the comment block explaining the contract and the arity dependence, and the **JSDoc dispatch
table** finding A4 required. **No other production file changed** — AC-10 in its tightened form.

**Behaviour, measured through the same jsdom harness as §0.3.** §0.3's signed table enumerates
**nine** defective outcomes and all nine are fixed — but **nine is a known undercount of the real
family, and the fix changes twelve.** §0.3 lists the `false` arity for `'error'` only; the defect is
present for all four type words in that arity, which is why **B46 ships parametrised over four**.
The qualified count is carried here and in the note under §i.2; the signed figure is left as signed.

| Call | Before | After |
|---|---|---|
| `showToast(T, true)`, all four `T` | `"true"` on the type's own class | **`T` on `bg-danger`** |
| `showToast('error', false)` | `"false"` on `bg-danger` | **`"error"` on `bg-success`** |
| `showToast(T, false)`, the other three `T` — **not among §0.3's nine** | `"false"` on the type's own class | **`T` on `bg-success`** |
| `showToast(T)`, all four `T` | default copy on the type's own class | **`T` on `bg-success`** |
| `showToast('Real msg', true)` / `showToast('errors', true)` / `showToast('Error', true)` | correct | **unchanged** |

**Separately, and not one of the twelve:** `showToast(T, false, {requestId})` now **drops** the
request-ID suffix. The drop is observable only for `T = 'error'`, because the suffix gate is
error-only; **B47a–d** pin the whole arity-3 family per OD-11.

### i.2 Line-anchor re-measurement — the LAST content edit, done by measuring

Inserting the predicate shifted every anchor below it. Re-measured, not offset-arithmetic.

⚠️ **SUPERSEDED 2026-08-27 (integration pass) — this table now reads against merged `main`.** The
reading it replaces was taken on the **pre-KI-011** base `b733c14`, whose `toast.js` is 111 lines;
KI-011 (PR #426, `5b35966`) then rewrote the rendering half of the same function and moved every
anchor again. **The superseded pairs, preserved rather than deleted:** `:12→:31`, `:15→:50`,
`:15-27→:54-66`, `:28→:67`, `:49→:88`, `:52→:91`, `:56→:95`, `:60→:99`, `:84→:123`,
`:88-109→:127-148`, `:98→:137`. **None of those numbers resolves on the shipped file.** The "Was"
column below is merged `main` at **`f9726a3`** (304 lines); the "Now" column is this branch (**353
lines**). Both were measured, neither derived. **The shift is not a single offset** — it ranges from
`+29` above the predicate to `+49` below it, on top of KI-011's own displacement of roughly `+170`.

| Anchor | Was (`main` `f9726a3`) | Now (this branch) |
|---|---:|---:|
| the click handler's `bootstrap.Toast.getInstance` | `:107` | **`:136`** |
| the `onClick` `try`/`catch` | `:112-116` | **`:141-145`** |
| `validTypes` set | `:184` | **`:213`** |
| the discriminator | `:187` | **`:232`** (predicate `:232-234`; `if (isLegacyCall)` at `:236`) |
| the legacy normalisation block | `:187-199` | **`:236-248`** |
| `} else if (typeof options === 'number')` | `:200` | **`:249`** |
| `#toast-body` id read | `:206` | **`:255`** |
| `#liveToast` id read | `:212` | **`:261`** |
| the `message !== undefined` guard | `:224` | **`:273`** |
| the two default-copy strings | `:227` | **`:276`** |
| the `requestId` suffix gate | `:230` (append at `:231`) | **`:279`** (append at `:280`) |
| the KI-004 span (`classList.remove` → `toast.show()`) | `:265-284` | **`:314-333`** |
| `typeToClass[type] \|\| 'bg-success'` | `:272` | **`:321`** |

**Two anchors this record used to name no longer exist, and re-numbering them would have been the
wrong repair.** `toastBody.innerHTML = ''` — CI-10's evidence, and §10.7-R10's wipe mechanism — was
**deleted by KI-011**; the nearest surviving line is `toastBody.replaceChildren()` at **`:289`**,
which runs **only on the first render into an empty body** and is not a per-call clear.
`toastBody.appendChild(button)` was **replaced** by
`resolveSlot(toastBody).appendChild(buildActionButton(…))` at **`:303-304`**, which appends into
`div.toast-action-slot`, a **child** of `#toast-body` rather than `#toast-body` itself. Anyone
re-reading CI-10 or §10.7-R10 against the shipped file must read those two rows as **identity
changes, not line moves**.

**The two fixes occupy different halves of `showToast()` and both are live** — KI-010 decides how the
ARGUMENTS are read (`:232-248`), KI-011 decides how the toast RENDERS (`:283-337`). This packet's
diff touches only the first.

**Every other `toast.js:NN` citation in this document — §0.2's `:15`, §0.5's `:15`, §v1.x's `:15`,
`:28`, `:60`, `:84`, `:1-10` and `:14-27`, and §v2.x's restatements of them — describes the PRE-FIX
file and is left as written.** They sit next to quoted pre-fix source and next to prose that reasons
about the defect; **re-numbering them would point a reader at the repaired code while the sentence
still describes the break**, which is strictly worse than a number that does not resolve. Two of
them are additionally identity changes, not line moves: §v1.10's *"KI-011 untouched — `toast.js:60`
and `:84` are not in the diff"* names two lines KI-011 has since **deleted and replaced**; §i.10
carries the measured restatement of that claim against the shipped file. **The table above is the
only mapping to trust.**

**Citations INTO the files this packet moved were re-anchored too**, not just citations out of
them: **B5** `:169 → :183` and the `validTypes` set `:12 → :31` in §0.3/§0.5 (this packet's own test
header and predicate comment pushed them down), and OD-10's two signed Gate 1 checkboxes
`:2054`/`:2067 → :2095`/`:2108` (the stale-pointer annotation pushed them down). **A signed section's
line citations are still re-anchored when this packet is what moved them** — the prose is frozen, the
line numbers are measurements.

⚠️ **AMENDED 2026-08-27 (integration pass) — every figure in the paragraph above is superseded, and
"unaffected" was the wrong answer for all of them.** §0.3 and §0.5's `validTypes` citation is
**`:213`** on the shipped file, not `:31`; `:31` was the pre-KI-011 reading. `B5`'s `:183` and
OD-10's `:2095`/`:2108` are **anchors into files KI-011 did not touch — but THIS PASS touched both**,
by adding comment blocks to `toast.test.js` and seven lines to the `STEP12` annotation. **A citation
is falsified by whoever moves the target, including the author re-anchoring it.** Every one below was
measured after the last content edit:

| Citation | Was | Now |
|---|---:|---:|
| **B5** (§0.3, §0.5's table, and council row P1) | `:183` | **`:188`** |
| **B6** (§0.5) | `:175` | **`:194`** |
| **B7** (§0.5) | `:181` | **`:200`** |
| **B8** (§0.5) | `:189` | **`:208`** |
| **B9** (§0.5) | `:196` | **`:215`** |
| **B11** (§0.5) | `:210` | **`:229`** |
| **B13**'s span (§v1.1) | `:236-239` | **`:255-274`** |
| **B13**'s `showToast('error', undefined)` call (§v1.4) | `:237` | **`:271`** |
| OD-10's two signed Gate 1 checkboxes (`STEP12`) | `:2095` / `:2108` | **`:2102` / `:2115`** |

**Two §0.5 anchors were deliberately NOT re-numbered**, because the cases they name no longer exist:
`:556-569` (pre-fix **B45**) and `:535-543` (pre-fix **B43**) were both **inverted** by this packet.
Each carries a dated anchor note naming its successor family — **B45a–d at `:625-633`**, **B43a–d at
`:589-597`** — and saying that the quoted block is history rather than a pointer. **Re-numbering a
citation whose target changed its assertion would be worse than leaving it stale**, because the new
number resolves and the reader has no signal that the meaning moved.

**The `toast.js:NN` citations inside `toast.test.js` were re-anchored a second time, for a reason
worth recording.** Their first re-anchoring in this packet applied pre-KI-011 offset arithmetic to
numbers that were **already** pre-KI-011 stale on `main` — KI-011 shipped without updating them — so
both readings were wrong and the second was wrong in a way that looked deliberate. Measured against
the shipped file: `#liveToast`'s id **`:80 → :261`**, the at-rest class value
**`(:127, :138) → (:314, :321)`**, `#toast-body`'s id **`(:74) → (:255)`**, the message span's
creation and append **`:100-102 → :290-292`**, the action button's append **`:123 → :303-304`**, the
click handler's `getInstance` **`:113 → :136`**, and the `onClick` `try`/`catch`
**`:117-120 → :141-145`**. The placement-neutrality comment's claim that the button is appended
**to `#toast-body`** and that a subsequent toast **destroys** it is **prose KI-011 falsified, not a
number**; it is corrected in place with a dated note rather than silently re-numbered.

**On "nine defective outcomes" (§0.3, signed) — nine is a KNOWN UNDERCOUNT and must not be restated
as an unqualified current fact.** The count is nine because §0.3's table lists the `false` arity only
for `'error'`. The defect is in fact present for **all four** type words in that arity —
`showToast('warning', false)` rendered `"false"` on `bg-warning`, `showToast('success', false)`
rendered `"false"` on `bg-success` — which is exactly why **B46 is parametrised over four rather than
shipping as one case**. **The measured family is three arities × four type words = TWELVE changed
outcomes**, of which §0.3 enumerates nine. The signed figure is left as signed; **every restatement
outside §0.3 — this PR's body included — carries the qualification**, so a reader who counts the B46
family does not conclude the arithmetic is broken. **Not counted in the twelve:** the arity-3
request-ID drop pinned by **B47a–d**, which is a new consequence rather than a repaired defect.

> **These figures supersede an earlier reading in this same section** (`:56`/`:94`/`:97`/`:105`/`:129`/`:143`),
> taken before the review pass trimmed the predicate's comment block and shifted every line again.
> **That is precisely why re-anchoring is specified as the LAST edit** — it was done twice here,
> and only the second reading is true.

`e2e/workout-plan.spec.ts:682`'s pinned comment was re-anchored from `modules/toast.js:14-27` to
`:50-66` (finding A6). ⚠️ **SUPERSEDED 2026-08-27 (integration pass):** `:50-66` was the pre-KI-011
span. The legacy-signature fallback's true span on the shipped file is **`:236-248`**, measured, and
the comment now carries that.

### i.3 Test changes — exactly what OD-4, OD-7 and OD-11 authorised

| Family | Cases | Status |
|---|---:|---|
| **B45a–d** `showToast(T, true)` → `T` on `bg-danger` | 4 | **replaces B45** — deliberately inverted |
| **B46a–d** `showToast(T, false)` → `T` on `bg-success` | 4 | **new** — the severity inversion |
| **B43a–d** `showToast(T)` → `T` on `bg-success` | 4 | **replaces B43** — deliberately inverted |
| **B47a–d** `showToast(T, false, {requestId})` → `T`, **no suffix** | 4 | **new**, per **OD-11** |
| **B13** | 1 | **assertions unchanged**; comment rewritten to state the arity dependence. Per **OD-7**, the S1-only parametrisation was **not** added |

Every inverted family carries the AC-4 comment naming this document and the Gate 1 sign-off date,
and the file header states that a red there without the production fix is the intended signal. The
**nine-cases-have-no-independent-kill disclosure** (finding T-S2) is in the file, in the B15a/B15b
idiom.

### i.4 The AC-7 matrix — every arm run against the FULL suite

**All ten arms collected 245. No survivors, no BAD RUNs.**

| Arm | Exit | Result | Cases red |
|---|---:|---|---|
| **3** the pair (shipped) | **0** | 245 passed (245) | *(none)* |
| **2** pristine prod + new tests | 1 | 16 failed \| 229 passed | **B43, B45, B46, B47 families — exactly the new and inverted cases** |
| **4** rival spelling **S1** | 1 | 1 failed \| 244 passed | **B13, and only B13** |
| **5a** drop `isFlag` | 1 | 12 failed | B45, B46, B47 |
| **5b** drop `isAbsent` | 1 | 4 failed | **B43 only** |
| **5c** narrow → `message === true` | 1 | 8 failed | **B46, B47** |
| **5c′** narrow → `message === false` | 1 | 4 failed | **B45** |
| **5e** `argc !== 2` | 1 | 7 failed | B19–B23, B33, B34 |
| **5f** careless rest rewrite (drop arity) | 1 | 4 failed | **B43** |
| **6** drop `isTypeWord` | 1 | 1 failed | **B8, and only B8** |

**Three results worth stating on their own:**

1. **Arm 2 satisfies AC-7's *"nothing else"* over the real 231/245-case suite**, not over a scoped
   probe — the gap finding T-B4 identified. Before the test changes, the fix alone red exactly
   `{B43, B45}` out of 231.
2. **Arm 5c is the whole justification for B46a–d**, and it held: the narrowing mutation
   `message === true` — measured *indistinguishable* from the correct predicate against every
   pre-fix case — is now **killed, and only by B46/B47**. Without this packet's new families the most
   plausible mis-implementation of this fix would have shipped green.
3. **Arm 4 vindicates keeping B13.** The rival spelling reds **exactly one case**, so B13 is the sole
   discriminator between the two contracts — which is precisely why OD-6 needed ruling and why B13
   could not simply be deleted.

### i.5 Gate results

| Gate | Result |
|---|---|
| **1** `npm run test:js` | **245 passed (245)**, 13 files, exit 0. **Three-way reconciliation holds:** diff-derived **61 / 245** == `vitest run` collected **245** == the pinned literals. `.only`/`.skip`/`.todo` grep over `toast.test.js`: **clean**. All 16 new case identities present in the regenerated `vitest.cases` |
| **2** inventory regeneration | `vitest: 245 cases / 13 files`; `toast.test.js` **47 → 61** |
| **3** `--check` | `Test inventory is up to date.`, exit 0 |
| **4** determinism | regenerated **three** times, `git status --porcelain docs/test_inventory/` byte-stable |
| **5** full pytest | **3175 passed, 2 skipped** — **a delta of exactly ZERO nodes** against the recorded baseline, as predicted |
| **6** `tsc --noEmit` **and** pyright baseline | tsc exit 0; **`PASS — 0 net-new diagnostics`**. ⚠️ **RE-MEASURED 2026-08-27 (integration pass): `baseline 130, current 130`.** The `132 / 132` reading this row carried was taken before **PR #430** (Packet P1, `3098282`) lowered the committed baseline **132 → 130**; the *delta* — zero net-new — is what the gate blocks on and is unchanged |
| **7** E2E, two invocations | see below |
| **8** manual smoke | see below |
| **9** PR CI | ✅ **SATISFIED at the integration pass — 18/18 green.** Run [`33067601349`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33067601349), `pull_request` event, head `bbe2115`, every one of the eighteen jobs `success`, read individually. This **supersedes** the ❌ **BLOCKED** reading the row carried while the PR was stacked; §i.11 keeps both readings and the mechanism |

**Post-integration re-run, 2026-08-27** — after merging `main` (`f9726a3`) and applying this pass's
documentation and comment corrections, gates **1–6** were re-executed in full from this worktree:
Vitest **245 passed (245) / 13 files**, `--check` **`Test inventory is up to date.`**, full pytest
**3175 passed, 2 skipped** (the same zero-node delta), `tsc --noEmit` exit 0, pyright baseline
**PASS**. **Gates 7 and 8 were not re-run locally**, and deliberately so: this pass changed only
Markdown, JSDoc-adjacent comments and test comments — no production line, no test case, no
generated artifact — and the sharded `E2E Functional` matrix is covered by PR CI run
`33067601349`'s successor rather than by a second local batch whose reds this packet already
measured as environmental (§i.8).

**Contract literals** — two edited, one re-confirmed, exactly as finding T-N1 predicted:
`EXPECTED_TOTAL_CASES` **231 → 245**, `EXPECTED_PER_FILE[".../toast.test.js"]` **47 → 61**,
`EXPECTED_TOTAL_FILES` **unchanged at 13**. `tests/test_vitest_inventory_contracts.py`: **46 passed**.

### i.7 Documentation updated, and one thing deliberately not

- **`UI_SCENARIOS_GAP_ANALYSIS.md`** — the **KI-010** row moves **Open → Mitigated**, with counts
  **re-measured at fix time** (AC-8) and carrying the **visible** count (11) beside the shape count
  (13). The **second pointer at §3.1** — which finding P9 caught, and which would otherwise have left
  the file contradicting itself — is updated in the same pass.
- **`STEP12_JS_UNIT_GATE0.md`** — a **dated stale-pointer annotation** only, per **OD-10**, placed
  at **§10.3** and pointed to from **§10.5** and **§10.7-R3**, the two other sites that assert the
  pre-fix state. The 47-case arithmetic, B43/B45's present-tense rows, §10.5's kill sets, the two
  signed Gate 1 checkboxes and **every `toast.js:NN` anchor in that document** are named as false;
  **nothing there is edited**. Re-deriving §10.5 against the post-fix suite is a packet of its own
  and is **not** authorized here.
- **Not touched:** `MASTER_HANDOVER.md`, `OPEN_WORK_EXECUTION_PLAN.md`, KI-011, `volume-splitter.js`,
  and every U2 path.

### i.8 E2E — the two invocations, and how attribution was actually closed

**Gate 7(a) — 30 non-visual specs, 536 tests:** **520 passed / 16 failed.**
**Gate 7(b) — 3 visual specs, seeded, 126 tests:** **122 passed / 4 failed.**

**Neither red set is attributable to this diff, and that was established by measurement, not by
inspection.** The repository rule — re-run the identical batch before blaming your diff — was
applied to both tiers, and it mattered:

| Tier | Modified tree | Pristine tree | Verdict |
|---|---|---|---|
| non-visual, 536 tests | **16 failed** | **29 failed** | Failure sets differ in **both** directions — 5 only-modified, 18 only-pristine, 11 common. **Not a regression signal** |
| the 5 only-modified candidates, run alone | **54 passed / 0 failed** | — | Order- and DB-state-dependent, not caused by the fix |
| visual, seeded, 126 tests | 4 failed — `user-profile` ×1, `backup` ×3 | 4 failed — `progression` ×2, `body-composition` ×2 | **Same count, ZERO overlap.** Environmental |

**No baseline was regenerated and `--update-snapshots` was never run.** Every red above sits on a
page this packet does not touch; the fix changes no CSS, no layout and no markup.

**Two BAD RUNS were caught, both by reading output rather than exit status** — the failure mode
§v2.8's judging rules exist for:

1. `playwright test --testIgnore=…` — **not a Playwright CLI option**. The command died instantly
   and the shell reported **exit 0**. Nothing ran.
2. The first pristine-baseline batch **never executed**: port **5000** was still held by an orphaned
   `app.py` from the previous run's `webServer`, so Playwright aborted in 150 bytes. Read naively,
   that produced a comparison saying *"16 failures caused by the diff"* — **entirely false**.

**Consequence worth carrying forward:** the two E2E invocations in §v2.9 gate 7 need a **port-5000
clear between them**, and every invocation must be judged by its `Running N tests` header and its
summary line, never by exit status alone.

### i.9 Gate 8 — manual smoke against REAL Bootstrap

Run against the app on `127.0.0.1:5000` from this worktree, invoking the module directly on a loaded
`/workout_plan` page — because §0.4 measures **0 of 229** server sites emitting a bare type word, so
no real caller can reach the fixed path.

| Call | body | class |
|---|---|---|
| `showToast('error', true)` | `"error"` | `bg-danger` |
| `showToast('warning')` | `"warning"` | `bg-success` |
| `showToast('success', true)` | `"success"` | **`bg-danger`** |
| `showToast('error', false, {requestId:'R1'})` | `"error"` | `bg-success` |

In every row the element carried `role="alert"` and `aria-live="assertive"`.

**All four match the contract**, including the OD-11 request-ID drop. Row 3 is §v2.10's stated
limitation observed in a real browser: a **red** toast whose entire body is the word `"success"`.
**This is the only tier that exercises the fix outside jsdom.**

### i.10 What is NOT done, and what merging still requires

- **The merge embargo is stated in this section's header and is not restated here.** Its one clause
  the header lacks: the §13.0 ledger row numbers must be re-confirmed **against the then-current last
  row** immediately before this PR merges.
- ⚠️ **RECONCILED 2026-08-27 (integration pass).** This list used to say *"The Gate 1 planning PR is
  not merged either."* **It is merged** — #428, `a37d7e7` — and so are #426 (`5b35966`) and #427
  (`efa780c`). **No ordering condition remains unmet.** The one thing still outstanding is **OD-1's
  embargo**, and reaching `2026-09-05T17:59:26Z` is not merge authorization.
- **KI-011 is untouched, re-verified after integration.** The KI-011 lines are now physically present
  in the same file, so "untouched" is a claim about the **diff**, not about the file:
  `git diff origin/main...HEAD -- static/js/modules/toast.js` carries no line from the rendering half
  (`:283-337`), and **B30–B35 stayed green in all ten mutation arms** and in the post-integration
  re-run.
- **§10.5's kill sets are annotated, not re-derived** (OD-10). That remains a packet of its own.

### i.11 Gate 9 — BLOCKED while stacked, SATISFIED after retargeting

⚠️ **SUPERSEDED 2026-08-27 (integration pass).** This section was written while #431 was stacked on
the Gate 1 planning branch and read *"Gate 9 is BLOCKED, not satisfied — and it cannot be unblocked
from this branch."* **That reading is no longer true**, and the sequence it named as the only way out
is exactly what happened. The diagnosis is preserved below because it is correct about the
mechanism, and because the mechanism will recur on the next stacked PR.

#### The state that produced the BLOCKED reading — preserved, dated, no longer live

**PR #431 had received ZERO check-suites, and that was structural rather than a glitch.**

Measured: `.github/workflows/ci.yml` declares

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
```

The `pull_request` trigger filters on the **base** branch. #431's base was
`docs/u3a-ki010-gate1-plan` — the Gate 1 planning branch it was stacked on — which is neither `main`
nor `develop`, so **no workflow run was ever created for it**. `gh pr checks 431` reported *"no checks
reported"*, and `gh api .../actions/runs?branch=feat/u3a-ki010-toast-collision` returned an **empty**
list.

**Close/reopen did not fix this.** It was tried, and it did not: the repository's close/reopen
remedy applies to a *different* mechanism (a PR that is CI-dark despite a valid base). There the base
branch itself was outside the trigger's filter, so there was nothing to re-fire.

**Unblocking was a sequence, not an action available at the time**: #427 merges, then #428 merges,
then #431 is **retargeted to `main`**, at which point `ci.yml`'s filter admits it and Gate 9 runs for
the first time. Retargeting *before* #428 merged would have folded the entire Gate 1 plan into this
PR's diff and put a signed planning document through an implementation review — which is why it was
deliberately not done then.

#### What actually happened, measured

**All three predecessors merged and the PR was retargeted to `main`.** #426 → `5b35966`, #427 →
`efa780c`, #428 → `a37d7e7`. `gh pr view 431 --json baseRefName` reports **`main`**, and `ci.yml`'s
filter admits it.

**Gate 9 is SATISFIED. Read at the integration pass:**

| | Value |
|---|---|
| Run | [`33067601349`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33067601349) |
| Event / head | `pull_request` / `bbe2115` |
| Result | **18 of 18 jobs `success`**, read individually rather than from the run's overall conclusion |
| Both load-bearing required contexts | `Test Inventory Drift` [`98501473180`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33067601349/job/98501473180) **`success`**; `Run Tests` [`98501473126`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33067601349/job/98501473126) **`success`** |
| The three legs local runs cannot cover | `Frontend Build (npm ci + SCSS)` [`98501473167`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33067601349/job/98501473167), `E2E Functional Shard 1/2` [`98501541080`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33067601349/job/98501541080) and `Shard 2/2` [`98501541067`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33067601349/job/98501541067) — all **`success`** |
| Mergeability at that read | `MERGEABLE` / `CLEAN`, **draft** |

**The local-run caveat is discharged, and it is worth saying which part.** Gates 1–8 and 10 ran on a
Windows host in a worktree whose `node_modules` is a **junction to the main checkout's**, so they
could not detect a dependency problem, could not run the ubuntu leg of `Test Inventory Drift`, and
could not compose the sharded `E2E Functional` matrix as CI does. **Run `33067601349` covered all
three**, and the packaged-artifact smoke besides.

**Gate 11 (the ledger row) is still not satisfied and is still not owed by this packet** — §v2.1's
annotation records that PR #429 claimed rows 13–16 first and U3a's block was withdrawn. §13.0 stands
at **row 23** on `main` at `f9726a3`. Whoever merges #431 owes its **post-merge `main`** `js-unit`
result as the next **unclaimed** row; **no row number is predicted here**, and this PR's own
`pull_request` run is **not** a ledger row — the ledger indexes `main` `push` results only.
