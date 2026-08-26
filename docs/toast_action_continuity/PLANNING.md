# Packet U3b — KI-011, toast action continuity — **Gate 0 candidate**

> **STATUS: GATE 0 CANDIDATE. NOT SIGNED. NOT AUTHORIZED.**
> This document is **requirements discovery only**. No production file, test file, inventory
> artifact, ledger or status document is edited by the PR that carries it, and none may be.
> **Gate 1 does not begin, and implementation does not begin, until the owner signs §0.9 below.**
>
> **Base:** `origin/main` @ **`52c44c4`** (`docs(u2): sign Gate 1 plan for backup save-first
> continuity (#424)`), fetched and measured **2026-08-27**.
> **Worktree:** `Hypertrophy-Toolbox-v3-main-u3-ki011-gate0`, branch `wt/u3-ki011-gate0`,
> created from `origin/main` and fast-forwarded to `52c44c4` before any measurement was taken.
> **Defect:** **KI-011**, [`UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md) row
> `KI-011` — *Open, not mitigated, not fixed*.
> **Roadmap slot:** [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §"Packet U3 —
> Toast contract defects KI-010 and KI-011", which requires **its own Gate 0 and Gate 1, *per
> defect***.
>
> **KI-010 is a different packet.** Packet **U3a** owns KI-010 (the type-word signature collision)
> in `docs/toast_type_word_collision/`. **KI-010 and KI-011 are separate artifacts and separate
> gates.** This document neither describes, plans, nor pre-approves any part of KI-010. Where the
> two defects touch the same file, that is recorded here as a **sequencing risk** (§0.10), not as
> shared scope.

---

## 0.1 Ownership, containment, and what this packet may touch

| | |
|---|---|
| **This document creates** | `docs/toast_action_continuity/PLANNING.md` — **one new file, and nothing else** |
| **Live ownership claim** | `docs/toast_action_continuity/**`, recorded in `docs/ai_workflow/WORKSTREAM_OWNERSHIP.local.md` (gitignored) per [`WORKSTREAM_OWNERSHIP.md`](../ai_workflow/WORKSTREAM_OWNERSHIP.md) "Where live claims go". The claim covers that directory and **nothing else** |
| **Must not touch — and does not** | [`static/js/modules/toast.js`](../../static/js/modules/toast.js); [`static/js/modules/__tests__/toast.test.js`](../../static/js/modules/__tests__/toast.test.js) or **any** test file; [`static/js/modules/volume-splitter.js`](../../static/js/modules/volume-splitter.js); `e2e/**`; **either** test-inventory artifact (`docs/test_inventory/TEST_INVENTORY.json`, `docs/test_inventory/TEST_INVENTORY.md`); [`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md); [`docs/UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md); [`docs/OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md); `docs/backup_confirmation_continuity/**` (Packet **U2**); `docs/toast_type_word_collision/**` (Packet **U3a**); `docs/volume_failure_feedback/**` (Packet **U1**, shipped) |
| **Where the reproduction harness lives** | The gitignored **`artifacts/probe/`**, never `scripts/`. This is the containment rule Packet B established ([`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md) §10.1) and it has teeth: a file under `scripts/**` pulls in QUALITY_GATE's *Tooling* routing and changes the packet's gate set. **The harness is scratch, is not committed, and is not part of the deliverable** |
| **Must not do** | Begin Gate 1; write any production or test line; touch KI-010; edit any ledger row; regenerate any inventory; promote `js-unit`; merge or rebase this branch around **U2** |

**Concurrency.** Two other workstreams are live at authoring time: **U2 implementation** (backup
save-first continuity) and **U3a / KI-010 Gate 0 planning**. Neither of their path sets is claimed
or edited here, and neither claims `docs/toast_action_continuity/**`. Merge order among U2, U3a and
U3b is **unresolved** and is not decided by this document.

---

## 0.2 Measured current behavior, and the reproduction

### 0.2.1 The dispatcher, as it stands on `52c44c4`

[`toast.js`](../../static/js/modules/toast.js) is **unchanged since Packet B merged**: `git
hash-object static/js/modules/toast.js` returns
**`42863b4664b7f87a2519556b7f9db8af2cb36e64`** on `52c44c4`, the same blob
[`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md) records at `987588a`. **U1
did not touch it** and neither did U2's planning.

Every toast in this application is rendered into **one** shared element pair declared once in
[`base.html:243-263`](../../templates/base.html#L243-L263) — `#liveToast` and, nested inside it,
`#toast-body`. `showToast()` renders like this:

| Line | Statement | Consequence |
|---|---|---|
| [`:60`](../../static/js/modules/toast.js#L60) | `toastBody.innerHTML = '';` | **Destroys every child of `#toast-body`**, unconditionally, on every call |
| [`:61-63`](../../static/js/modules/toast.js#L61-L63) | create `<span>`, set `textContent`, append | The message |
| [`:65-85`](../../static/js/modules/toast.js#L65-L85) | if `action` is well-formed, create `<button>`, wire `click`, `toastBody.appendChild(button)` | **The action button is a child of the node `:60` clears** |
| [`:103-106`](../../static/js/modules/toast.js#L103-L106) | `getInstance(...)?.dispose()` | The previous Bootstrap instance is disposed |
| [`:108-109`](../../static/js/modules/toast.js#L108-L109) | `new bootstrap.Toast(el, {delay: duration}); toast.show()` | A **new** instance with the **new** call's duration |

**The defect is the composition of `:60` and `:84`.** The action button lives inside the node the
*next* call erases. There is no ownership check, no "is this action still live" test, no opt-out,
and no way for a caller to raise a non-destructive message. `showToast()` has no concept of an
action outliving a message.

### 0.2.2 Reproduction — measured, not asserted

The defect was reproduced against a **byte-identical copy** of the production module
(`artifacts/probe/toast.js`, `git hash-object` → `42863b4664b7f87a2519556b7f9db8af2cb36e64`,
identical to `static/js/modules/toast.js`). **The production file was never written to.** The probe
reuses the fixture and `bootstrap` fake from
[`toast.test.js`](../../static/js/modules/__tests__/toast.test.js) and runs under a probe-only
Vitest config scoped to `artifacts/probe/**`, so it cannot collect the real suite and cannot be
mistaken for a suite-count reading.

**Result: 1 file, 6 tests, all passing, exit 0** (`vitest v4.1.10`, jsdom).

| Row | What it drives | Measured outcome |
|---|---|---|
| **R1** | The exact production shape of the save toast ([`volume-splitter.js:424-431`](../../static/js/modules/volume-splitter.js#L424-L431)) followed by the exact history-refresh error toast ([`:564`](../../static/js/modules/volume-splitter.js#L564)) | Before: **1** action button in `#liveToast`, `aria-label="Activate volume plan 7"`. After: **0** action buttons anywhere in `#liveToast`; body text is the history-refresh message; still exactly **one** `#liveToast`; the `onClick` handler was **never invoked** |
| **R2** | Instance lifecycle across the same two calls | Ordered log `['construct:6000','show','dispose','construct:3000','show']`. **The second toast also truncates the first's declared 6000 ms life to 3000 ms** — the destruction is not merely visual, the whole 6 s affordance window collapses |
| **R3** | Reachability of the destroyed node | The button object survives only as a **detached** node: `isConnected === false`, `document.contains(...) === false`. **No user can reach it**, and its closure is dropped with it |
| **R4** | "from anywhere" | A plain `showToast('success', 'Exercise updated successfully')` — the [`workout-plan-table.js:576`](../../static/js/modules/workout-plan-table.js#L576) shape, **no action, no options** — wipes it just the same. Nothing about the second call needs to be related to the first |
| **R5** | **U1's Retry**, and the cross-packet consequence | U1's Retry button is destroyed identically, **and** U1's shared probe `document.querySelector('#liveToast button[aria-label="Retry volume calculation"]')` flips **`true` → `false`** as a direct result. See §0.10 — this is the sharpest cross-packet risk in the packet |
| **R6** | Whether the existing suite forbids the fix | With a button relocated **outside `#toast-body` but inside `#liveToast`**, **B26**'s two assertions verbatim (`#toast-body` holds exactly one `<span>`; its text is the second message) **still pass**, and the relocated button **survives the body clear**. The suite's locators do not block a relocation fix |

**Baseline, taken in the same worktree at the same commit:** `npx vitest run` → **13 files / 231
tests, all passing**; `docs/test_inventory/TEST_INVENTORY.json` reads `vitest.total_files = 13`,
`vitest.total_cases = 231`; working tree clean of tracked changes.

### 0.2.3 What is measured and what is traced — stated so it is not over-read

- **Measured (jsdom, deterministic, exit-code judged):** the dispatcher mechanism, in all six rows
  above, against production-shaped calls and a byte-identical module copy.
- **Traced by citation, not browser-measured:** that the *production sequence* on the Volume
  Splitter page reaches those two calls in that order (§0.3). The path is three unconditional
  statements and is read directly from the shipped file, but **no browser reproduction was run**.
  A browser-level arm is listed as a **Gate 1 entry condition** (§0.11), not claimed here.

---

## 0.3 Which live flow reaches it, and how it differs from U1's behavior

### 0.3.1 The reachable route — Volume Splitter "save without activating"

All citations are to [`volume-splitter.js`](../../static/js/modules/volume-splitter.js) on
`52c44c4`. The [`UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md) KI-011 row was
re-anchored for U1's `+125`-line shift on 2026-08-26 and its four anchors are **confirmed exact**
here.

1. The user saves a volume plan **without activating it** (`#export-volume`). `savePlan()` posts
   `/api/save_volume_plan`.
2. On success with a `plan_id` and `activate` falsy, [`:424-431`](../../static/js/modules/volume-splitter.js#L424-L431)
   raises `showToast('success', 'Plan #N saved.', { duration: 6000, action: { label: 'Activate for
   Plan tab', ariaLabel: 'Activate volume plan N', onClick: () => toggleActivePlan(N, false) } })`.
   **This is the only toast in the application whose action is the sole affordance for its offer.**
3. [`:433`](../../static/js/modules/volume-splitter.js#L433) — **the very next statement, on every
   save, unconditionally** — calls `loadVolumeHistory()`.
4. `loadVolumeHistory()` ([`:493`](../../static/js/modules/volume-splitter.js#L493)) issues
   `GET /api/volume_history` with **`retries: 0`** ([`:499`](../../static/js/modules/volume-splitter.js#L499)),
   so a single transport or non-2xx failure goes straight to the handler.
5. Its `.catch` ([`:554`](../../static/js/modules/volume-splitter.js#L554)) ends at
   [`:564`](../../static/js/modules/volume-splitter.js#L564) with
   `showToast('error', 'Failed to load saved volume plans. Please try again.')`.
6. **`:60` fires. The button is gone**, the 6 s window collapses to 3 s (R2), and the user is left
   reading a message about *loading history* when what they were offered was *activation*.

**Why this route matters more than its severity rating suggests.** The button is destroyed
**without the user doing anything at all**. Steps 3–6 run on their own, milliseconds after step 2,
on every single save. The user has not clicked, typed, or navigated. The offer is withdrawn by the
application, silently, and the replacement message does not mention the withdrawn offer.

**Secondary routes on the same page** (user-action dependent, same mechanism, not separately
measured): a slider change inside the 6 s window schedules `calculateVolume()`, whose failure
raises U1's toast at [`:184`](../../static/js/modules/volume-splitter.js#L184); a failed export
raises [`:599`](../../static/js/modules/volume-splitter.js#L599); a delete raises
[`:382`](../../static/js/modules/volume-splitter.js#L382) or
[`:388`](../../static/js/modules/volume-splitter.js#L388); and **any** api call on the page that
does not pass `showErrorToast: false` reaches the shared wrapper's own toast at
[`fetch-wrapper.js:213`](../../static/js/modules/fetch-wrapper.js#L213) /
[`:246`](../../static/js/modules/fetch-wrapper.js#L246).

### 0.3.2 How this differs from U1's calculation-failure behavior — the distinction that must not blur

They are **different defects with different remedies**, and U1 fixed the other one.

| | **KI-012 (U1's defect, MITIGATED)** | **KI-011 (this packet, OPEN)** |
|---|---|---|
| What failed | A failed **calculation** produced **no user-visible signal at all** — two independent suppressions on one call | A **successful** save's action button is **destroyed by an unrelated later message** |
| Surface at fault | `volume-splitter.js`'s own error handling | **`toast.js`**, the shared dispatcher every page uses |
| Blast radius | One page's calculate path | **112 call sites in 20 modules** (§0.4) |
| U1's remedy | An accessible toast **carrying a Retry action** *plus* a **durable inline** `#volume-calculate-error` region prepended to `.volume-insights-panel`, plus `clearResults()` | **None. U1 explicitly does not fix KI-011** |
| Why U1 was safe without a fix | **The inline region is the durable retry path.** U1's plan states it directly: *"U1 accepts that loss and does not fix KI-011 — the durable Retry is the inline region"* ([`volume_failure_feedback/PLANNING.md`](../volume_failure_feedback/PLANNING.md) §v2.2) | **The save toast has no inline fallback.** "Activate for Plan tab" exists **only** in the toast |

**The asymmetry is the whole reason KI-011 is still worth fixing after U1 shipped.** U1 made its
own action button *expendable* by giving the same capability a durable home on the page. The save
toast's action has no such home: the plan row in the history table has its own `.activate-plan`
button ([`:524`](../../static/js/modules/volume-splitter.js#L524)) — but on the route in §0.3.1
**the history table has just failed to load**, so on that exact route the table shows
*"Failed to load volume history."* and the fallback affordance is absent too. **The one route that
destroys the button is also the route that removes its alternative.** That is measured from
[`:554-564`](../../static/js/modules/volume-splitter.js#L554-L564), which replaces `#history-body`
with the failure row.

---

## 0.4 Complete caller and action inventory

Measured on `52c44c4` by `grep -rn "showToast(" static/js --include=*.js`, excluding
`__tests__/**` and excluding `toast.js`'s own three hits (one declaration at
[`:11`](../../static/js/modules/toast.js#L11) and two comments at
[`:14`](../../static/js/modules/toast.js#L14) and [`:29`](../../static/js/modules/toast.js#L29),
none of them calls).

### 0.4.1 Every module that calls `showToast()` — 112 call sites across 20 modules

| Module | Sites | Module | Sites |
|---|---:|---|---:|
| [`workout-log.js`](../../static/js/modules/workout-log.js) | 17 | [`workout-plan.js`](../../static/js/modules/workout-plan.js) | 4 |
| [`volume-splitter.js`](../../static/js/modules/volume-splitter.js) | 12 | [`workout-plan-table.js`](../../static/js/modules/workout-plan-table.js) | 4 |
| [`backup-center.js`](../../static/js/modules/backup-center.js) | 11 | [`workout-plan-add-exercise.js`](../../static/js/modules/workout-plan-add-exercise.js) | 4 |
| [`exports.js`](../../static/js/modules/exports.js) | 8 | [`user-profile-settings.js`](../../static/js/modules/user-profile-settings.js) | 4 |
| [`workout-plan-supersets.js`](../../static/js/modules/workout-plan-supersets.js) | 6 | [`filters.js`](../../static/js/modules/filters.js) | 4 |
| [`progression-plan.js`](../../static/js/modules/progression-plan.js) | 6 | [`workout-plan-replacement.js`](../../static/js/modules/workout-plan-replacement.js) | 3 |
| [`workout-plan-estimates.js`](../../static/js/modules/workout-plan-estimates.js) | 5 | [`workout-plan-execution-style.js`](../../static/js/modules/workout-plan-execution-style.js) | 3 |
| [`exercises.js`](../../static/js/modules/exercises.js) | 5 | [`user-profile-calibration-review.js`](../../static/js/modules/user-profile-calibration-review.js) | 3 |
| [`body-composition.js`](../../static/js/modules/body-composition.js) | 5 | [`fetch-wrapper.js`](../../static/js/modules/fetch-wrapper.js) | 2 |
| [`app.js`](../../static/js/app.js) | 5 | [`user-profile-forms.js`](../../static/js/modules/user-profile-forms.js) | 1 |

**All twenty are loaded on every page.** [`app.js`](../../static/js/app.js) is the single
`type="module"` entry point in [`base.html:282`](../../templates/base.html#L282) and it statically
imports the whole set. Whether a given site *fires* depends on its DOM and its handlers, but
nothing is page-scoped by loading, and **`fetch-wrapper.js`'s two sites can fire from any api call
on any page**. A KI-011 change to `toast.js` is a change every one of these 112 sites experiences.

### 0.4.2 Every live **action-button** caller — exactly 2, both in `volume-splitter.js`

Measured by `grep -rn "action *:" static/js --include=*.js` excluding tests: **two** matches,
both in `volume-splitter.js`. There are no others anywhere in the application.

| # | Site | Message | `action.label` | `action.ariaLabel` | `action.onClick` | `duration` | Durable fallback? |
|---|---|---|---|---|---|---|---|
| **A1** | [`:424-431`](../../static/js/modules/volume-splitter.js#L424-L431) | `Plan #N saved.` | `Activate for Plan tab` | `Activate volume plan N` | `toggleActivePlan(N, false)` | **6000** | **None on the failing route** — the history-table `.activate-plan` button ([`:524`](../../static/js/modules/volume-splitter.js#L524)) is absent precisely when the wipe happens (§0.3.2) |
| **A2** | [`:184-190`](../../static/js/modules/volume-splitter.js#L184-L190) | `Volume calculation failed, so no results are shown. Please try again.` | `Retry` | `Retry volume calculation` | `calculateVolume()` | default **3000** | **Yes** — the durable inline `#volume-calculate-error` region with its own `Retry` at [`:216-229`](../../static/js/modules/volume-splitter.js#L216-L229) |

**A2 is U1's, shipped 2026-08-26 in [#423](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/423).**
The KI-011 row's original *"sole caller"* wording was amended for exactly this reason; the amendment
is already on `main` and is not restated or re-amended here.

### 0.4.3 Two consumers of the action button that are **not** callers, and are load-bearing

Both are in `volume-splitter.js` and both read the **DOM presence** of A2's button. A KI-011 fix
changes what they observe. Neither may be edited by this packet.

| Consumer | Site | What it does today | What a "preserve the action" fix does to it |
|---|---|---|---|
| `ourToastContentStands()` | [`:258-260`](../../static/js/modules/volume-splitter.js#L258-L260) | `Boolean(document.querySelector('#liveToast button[aria-label="Retry volume calculation"]'))`. Deliberately scoped to **`#liveToast`, never `#toast-body`** — U1's plan makes that **binding**, so the probe survives the relocation a KI-011 fix requires | **Its answer inverts.** Today an unrelated toast makes it `false` (measured, R5). If the action is preserved, it stays `true` |
| `dismissCalculateFailureToast()` | [`:241-252`](../../static/js/modules/volume-splitter.js#L241-L252) | On the next success, if the probe says our content stands, `hide()` the live toast — so a success does not sit under a stale error toast | **It could hide a stranger's toast.** With the Retry button preserved across a replacement, the probe says `true` while `#liveToast` is showing an unrelated message; `hide()` would then dismiss that unrelated message |

**And the third consumer, which is a signed owner decision.** U1's announce condition at
[`:183`](../../static/js/modules/volume-splitter.js#L183) is
`forceAnnounce || !standing || !ourToastContentStands()`. Owner decision **OD-2** (ratified,
[`volume_failure_feedback/PLANNING.md`](../volume_failure_feedback/PLANNING.md) §v2.13) reads:
*"Repeat slider-originated announcements are suppressed while the same failure region **and**
U1-owned toast content stand; explicit user commands always announce, **and so does any failure at
a moment when U1's toast no longer stands.**"* Preserving the action across replacement means
U1's toast content **does** still stand where today it does not — so a repeat slider-originated
failure that **announces today would fall silent**. **That is a change to a ratified owner
decision and it is `OQ-8`.**

---

## 0.5 Requirements and acceptance criteria — **DRAFT, pending Gate 0**

Every criterion below is **conditional on the owner's answers in §0.9** and several are written in
two forms because the answer decides which applies. Nothing here is signed.

### 0.5.1 Functional requirements

| ID | Requirement | Depends on |
|---|---|---|
| **F1** | A well-formed action passed to `showToast()` remains **operable** — present in the accessibility tree and clickable, with its original `onClick` closure intact — after a later `showToast()` replaces the message, for as long as the action is **still valid** as defined by the owner's answer to `OQ-1` | OQ-1 |
| **F2** | The **message** contract is unchanged: the body still shows the **latest** message, exactly one message node, with stale `bg-*` classes cleared and the new type's class applied | OQ-5 |
| **F3** | A later call that **supplies its own action** resolves against a standing action by the rule the owner picks in `OQ-3` — replace, reject, or coexist — and never leaves two actions with the same accessible name | OQ-3 |
| **F4** | A later call that supplies **no** action resolves by the rule the owner picks in `OQ-2` | OQ-2 |
| **F5** | A standing action is **invalidated and removed** on each of the conditions the owner signs in `OQ-7` (at minimum: the user activates it; the user dismisses the toast) | OQ-7 |
| **F6** | The toast's **lifetime** across a replacement follows `OQ-4`. Today the later call's `duration` wins outright and can shorten a standing 6000 ms affordance to 3000 ms (**measured, R2**) | OQ-4 |
| **F7** | **All 112 existing call sites keep working unchanged**, with no signature change, no new required option, and no caller edit. A caller that passes no `action` behaves exactly as it does today | OQ-9 |
| **F8** | The **destroyed-node** failure mode is gone: no code path leaves an action button detached-but-believed-live, and no path leaves a live button whose `onClick` targets state that no longer exists | OQ-7 |

### 0.5.2 Acceptance criteria (candidate — the roadmap's three, expanded and made measurable)

[`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) states three KI-011 criteria. They
are the starting point, not the finished set; each is expanded into something a test can fail.

| # | Roadmap criterion | Candidate measurable form |
|---|---|---|
| **C1** | *"A still-valid action remains operable after a later message update."* | Drive A1's exact call, then A2's exact call, then assert: the A1 button is still in `#liveToast`, still carries `aria-label="Activate volume plan N"`, and **clicking it still invokes the original `onClick` with the original `planId`** — the last clause is the one that catches a fix that re-renders the button but drops the closure |
| **C2** | *"Existing toast accessibility, styling, duration, and action coercion tests remain green."* | **B30–B45 all green, unmodified** (§0.10 explains why B26 and B30–B35 permit the relocation and R6 measures it); `e2e/ui-hardening.spec.ts`'s three toast tests green; **`e2e/volume-splitter.spec.ts:340`**'s `/Plan #\d+ saved\.\s*Activate for Plan tab/i` green |
| **C3** | *"Preserve the existing single-toast/last-message-wins behavior unless an explicit product decision changes it."* | Exactly one `#liveToast` in the DOM; exactly one message node; body text equals the **latest** message. **`OQ-5` is that explicit product decision** and must be answered before C3 can be signed |
| **C4** | *(new — the reachable-route regression the roadmap asks for)* | A **browser-level** arm on the §0.3.1 route: save without activating, force `GET /api/volume_history` to fail, assert the Activate action is still operable and still activates plan *N* |
| **C5** | *(new — cross-packet)* | U1's `a1`, `a2`, `b1`, `a6`, `s3` and `c1` arms in `e2e/volume-splitter.spec.ts` **stay green**, and the OD-2 announce behavior is either unchanged or **re-signed** under `OQ-8` |

---

## 0.6 Behavioral and accessibility invariants

These hold **before and after** any fix. A fix that breaks one is wrong even if it satisfies §0.5.

### 0.6.1 Behavioral

| ID | Invariant | Evidence it is real today |
|---|---|---|
| **I1** | Exactly **one** `#liveToast` element exists in the DOM at all times | `e2e/ui-hardening.spec.ts:324-327`; measured R1 |
| **I2** | The body shows the **latest** message; a second toast does not stack or append | `toast.test.js` **B26**; `e2e/ui-hardening.spec.ts:329-340` |
| **I3** | Stale `bg-*` classes are removed before the new one is added — all four, not just the previous one | `toast.test.js` **B24**, **B25**, **B25b**; `e2e/ui-hardening.spec.ts:342-356` |
| **I4** | A message is rendered as **text**, never as HTML — `textContent`, never `innerHTML`, for user-supplied strings | `toast.test.js` **B18**. **A fix must not reintroduce an `innerHTML` write for the action** |
| **I5** | The action click **hides the toast before running `onClick`**, in that order | `toast.test.js` **B36**; the ordering is the assertion B36 exists for |
| **I6** | A throwing `onClick` is **caught and logged**, never propagated | `toast.test.js` **B38** |
| **I7** | A malformed action (non-function `onClick`, falsy label) renders **no button at all**, and the message still renders | `toast.test.js` **B33**, **B34** |
| **I8** | `showToast()` never throws on a missing `#toast-body` or `#liveToast`; it logs and returns, body first | `toast.test.js` **B39**, **B40**, **B41** |

### 0.6.2 Accessibility

| ID | Invariant | Source |
|---|---|---|
| **A-I1** | The action button's accessible name is `action.ariaLabel` when given, and **the attribute is absent — not the string `"undefined"` —** when not | `toast.test.js` **B31**, **B32**. B32 exists because mutation **N21** produces a screen reader announcing *"undefined"* |
| **A-I2** | The container is `aria-live="polite"` and `#liveToast` is `role="alert" aria-live="assertive" aria-atomic="true"`. **`toast.js` never touches these** and must not start | [`base.html:237-248`](../../templates/base.html#L237-L248); owned by `e2e/ui-hardening.spec.ts:358-364`, `e2e/accessibility.spec.ts` and the axe register |
| **A-I3** | The action button is **keyboard reachable and operable** — a real `<button type="button">`, in the tab order, activated by Enter and Space | `toast.js:66-67`; **not currently asserted at any tier**, see `OQ-6` |
| **A-I4** | The preserved action must not be **announced twice**. `aria-atomic="true"` on an `assertive` region means each body rewrite re-announces the **whole** region. If a preserved button stays inside the atomic region, its label is re-read on every subsequent message | Derived from [`base.html:246-247`](../../templates/base.html#L246-L247). **This is the strongest technical argument for relocating the action outside `#toast-body`, and it is `OQ-6`** |
| **A-I5** | Focus is **never stolen** by a toast, and a preserved action must not trap or move focus when the message around it changes. If the user has focused the action button and a later message replaces the body, focus must not be lost to `document.body` | Not currently asserted; **a preserved-then-destroyed button today drops focus to `body` silently.** `OQ-6` |
| **A-I6** | No colour-only signal. The action inherits `text-white text-decoration-underline` on a `bg-*` surface. **U1 measured 1.58:1 for a Bootstrap button variant inside `.alert-danger`** and chose a plain control instead ([`volume-splitter.js:218-225`](../../static/js/modules/volume-splitter.js#L218-L225)) — a KI-011 relocation that changes the action's painted surface **must re-measure contrast**, not assume it | U1's measured precedent |

---

## 0.7 Explicit scope exclusions

**Out of scope for KI-011, named so they cannot drift in:**

1. **KI-010 in its entirety** — the type-word signature collision. Separate defect, separate
   packet (**U3a**, `docs/toast_type_word_collision/`), separate Gate 0, separate Gate 1. This
   document does not describe, plan, or pre-approve any part of it. It appears here **only** as a
   sequencing risk (§0.10-K).
2. **The legacy `showToast(message, isError?, duration?)` signature.** KI-011 does not remove,
   deprecate, or migrate it. Of the 112 call sites, a large minority still use it.
3. **Toast stacking / a multi-toast queue.** `I1` and `I2` stand. Anything else is a product change
   the owner has not asked for, and `C3` forbids it absent an explicit decision (`OQ-5`).
4. **`fetch-wrapper.js`.** Its two sites at [`:213`](../../static/js/modules/fetch-wrapper.js#L213)
   and [`:246`](../../static/js/modules/fetch-wrapper.js#L246) pass only `{ requestId }` and gain
   no action. U1's **OD-4** already ruled on the wrapper's toast and that ruling stands.
5. **U1's residue** — U1's AA/contrast debt, U1's coverage gaps, and **U1-FOLLOWUP-1**
   ([`volume_failure_feedback/PLANNING.md`](../volume_failure_feedback/PLANNING.md) §v2.14, the
   deferred `volume-splitter.test.js`). KI-011 does not discharge it and must not be used to smuggle
   it in early (§0.9, `OQ-10`).
6. **Anything belonging to Packet U2** — `docs/backup_confirmation_continuity/**`,
   `backup-center.js`, `e2e/program-backup.spec.ts`. U2 adds a new plain
   `showToast('warning', …)` and **no action button**; it is a new *later-toast source*, not a new
   action caller.
7. **Promoting `js-unit` to required**, decision **D2**, decision **Q4**, or any branch-protection
   edit. Untouched and unauthorized.
8. **Editing the KI-011 row itself.** [`UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md)
   is a **must-not-touch** for this planning PR. Flipping the row to *Mitigated* belongs to the
   implementation PR, per that file's own usage rule at `:109-112`.
9. **Toast visual styling and the seven-class Bootstrap string** at
   [`toast.js:68`](../../static/js/modules/toast.js#L68), deliberately pinned by no case at any tier
   (`STEP12` §10.5). A relocation must not turn it into a pinned contract by accident.
10. **Any inventory regeneration, any ledger row, and any status document.** §0.8 explains why the
    inventory question is *deferred to the implementation PR*, not answered here.

---

## 0.8 Qualification-window implications — the constraint that may decide the schedule

### 0.8.1 The window, as measured

| | |
|---|---|
| **T0** | **`2026-08-22T17:59:26Z`** — the `completed_at` of the `JS Unit (Vitest, non-required)` job `97070630453`, run `32589375849`, on `9cb6cdc`. **Not a `mergedAt`** |
| **Strict 14-day mark** | **`2026-09-05T17:59:26Z`** |
| **Suite being qualified** | **13 files / 231 cases** — re-measured in this worktree at `52c44c4`: `npx vitest run` → 13 files / 231 tests; `TEST_INVENTORY.json` → `vitest.total_files = 13`, `vitest.total_cases = 231` |
| **Governing wording** | `STEP12_JS_UNIT_GATE0.md` §6.5: the window *"runs from the first successful `JS Unit (Vitest, non-required)` run on `main` after the final expansion packet lands"*, and *"Any `js-unit` failure during the window resets it to zero"* |
| **Operative rule the ledger has applied at every row since T0** | **"changed no JS test case"** — *not* "changed no JS". Row 12 (#423, U1's implementation) states this explicitly and proves it by tree hash: `git rev-parse <sha>:static/js/modules/__tests__` identical across the merge, plus `vitest.config.js` identical, plus the inventory totals unchanged |

### 0.8.2 What a KI-011 implementation does to it

The roadmap requires KI-011 to *"add a fixed-behavior regression for the reachable volume-splitter
history-refresh failure"*, and the KI-011 row states *"No fixed-behavior regression test exists yet
— one must be added with the fix."*

**If that regression lands as a Vitest case, it is the first post-T0 change to the JS test corpus,
and on the ledger's own operative rule the window's premise breaks.** There is a **directly
governing precedent already signed**: **U1-FOLLOWUP-1** (`volume_failure_feedback/PLANNING.md`
§v2.14, owner decision **OD-1**, 2026-08-26) defers a `volume-splitter.test.js` on exactly this
ground —

> *"**It must not land before `2026-09-05T17:59:26Z`**, the strict mark in
> `STEP12_JS_UNIT_GATE0.md` §6.5, because doing so restarts the qualification window under the
> operative 'changed no JS test case' rule."*

**Three further mechanical consequences, all measured:**

1. **`tests/test_vitest_inventory_contracts.py` reds full pytest**, not merely the inventory-drift
   job. It pins `EXPECTED_TOTAL_CASES = 231`, `EXPECTED_TOTAL_FILES = 13` and, per file,
   `"static/js/modules/__tests__/toast.test.js": 47`. Adding **one** case to `toast.test.js` fails
   two of those three literals. That file is a **required** gate.
2. **Both inventory artifacts must be regenerated** — `TEST_INVENTORY.json` and
   `TEST_INVENTORY.md` — which is Packet F's surface.
3. **An E2E-only regression avoids all of it.** A Playwright arm in `e2e/volume-splitter.spec.ts`
   changes no Vitest case, so the window does not restart; it moves
   `playwright.total_tests` in the inventory (which #423 already did, 649 → 662, without engaging
   Q2) and, if the spec is on `ci.yml`'s required list, may move a pinned count.
   **This is the same trade U1 took and the owner granted as OD-1 option (i).**

**Recommendation, and it is `OQ-10`:** land KI-011's regression at the **E2E tier only** if the fix
is wanted before `2026-09-05T17:59:26Z`; add the Vitest cases as a follow-up **after** the strict
mark, alongside U1-FOLLOWUP-1. **A `js-unit` red during the window resets the clock to zero
regardless of tier**, so any KI-011 implementation carries schedule risk even when it adds no
Vitest case.

---

## 0.9 Owner decisions required — **the Gate 0 boundary**

Ten questions. Each carries the evidence, the options, and a recommendation. **The recommendation
is not the decision.** Nothing proceeds until these are answered.

---

**`OQ-1` — What makes an existing action "still valid"?**
*This is the load-bearing definition; F1, F5 and F8 all resolve to it.*

`showToast()` has no concept of validity today; the action lives exactly as long as the next call
is far enough away. Options:

- **(a) Time-scoped.** Valid until the toast that raised it would have auto-dismissed on its own
  `duration` (A1: 6000 ms). Simple, needs no caller change, and it is the only reading under which
  R2's 6000 → 3000 truncation is itself part of the defect.
- **(b) Caller-scoped.** Valid until the raising module says otherwise — a returned handle or an
  explicit `dismissAction()`. Precise, but it is an **API addition** and touches F7.
- **(c) Interaction-scoped.** Valid until the user acts on it or dismisses the toast; a later
  message alone never invalidates it.
- **(d) Semantic.** Valid while the underlying operation is still meaningful — plan *N* still
  exists and is still inactive. Most correct, and **not implementable inside `toast.js`**, which
  knows nothing about plans.

**Recommendation: (a), with (c) as its termination clause** — an action lives for its own toast's
declared duration or until the user acts or dismisses, whichever is first. It needs no signature
change (F7 holds), it is fully testable in jsdom with fake timers, and it makes R2's truncation a
named part of the fix rather than an unexamined side effect. **(d) is the right answer in principle
and the wrong layer**; if the owner wants it, it belongs in the caller via (b), and F7 must then be
renegotiated.

---

**`OQ-2` — A later toast supplies NO action. Preserve or remove the standing one?**

- **(a) Preserve** (default-preserve). Fixes the §0.3.1 route directly, since the destroyer is a
  no-action error toast. **Risk:** an action whose label no longer matches the message beside it —
  *"Failed to load saved volume plans. Please try again."* next to *"Activate for Plan tab"* is a
  genuinely confusing pairing, and today's behavior at least does not produce it.
- **(b) Remove** (default-remove). Keeps message and action always coherent. **But it does not fix
  the defect** — it *is* the current behavior.
- **(c) Preserve, and re-render the action with its own context** — e.g. the action carries a short
  standing label so the pairing reads as two separate statements rather than one sentence.

**Recommendation: (a), with the §0.6 `A-I4` mitigation from `OQ-6`.** (b) is a no-op. (c) is (a)
plus a copy change and can be added later without re-gating. **The confusing-pairing risk is real
and must be accepted explicitly, not hand-waved** — the alternative is that the user loses the
offer entirely, which is measurably worse: on the §0.3.1 route the fallback affordance is gone too
(§0.3.2).

---

**`OQ-3` — A later toast supplies its OWN action. What happens to the standing one?**

- **(a) Replace.** Newest action wins; at most one action ever. Consistent with last-message-wins.
- **(b) Reject the new one** while an action stands. Protects the older offer; surprising to the
  new caller and silently drops a well-formed request.
- **(c) Coexist** — two buttons. Breaks `I2`'s spirit, doubles the `aria-atomic` announcement, and
  risks two identically-labelled controls.

**Recommendation: (a) Replace.** Only two action callers exist (A1, A2) and they are on the same
page, so the collision is real but narrow: a save toast standing when a calculation fails. Replace
is the only option consistent with `C3`, and it is the only one that cannot produce two controls
with the same accessible name. **The cost is explicit:** on that one sequence, the Activate offer
is lost — which is exactly today's behavior for that sequence, so (a) is never worse than the
status quo and is better everywhere else.

---

**`OQ-4` — Does a later toast's `duration` shorten a standing action's window?**

**Measured (R2):** today it does. A 6000 ms save toast becomes a 3000 ms error toast; the affordance
window collapses by half even in a hypothetical world where the button survived.

- **(a) Later duration wins** (today's behavior). Simple; partially defeats `OQ-1(a)`.
- **(b) The standing action extends the toast** to the later of the two deadlines.
- **(c) Decouple** — the message auto-dismisses on its own duration; the **action** persists on its
  own clock until `OQ-1`'s validity ends.

**Recommendation: (b).** It preserves last-message-wins for the message, keeps one timer, and makes
`OQ-1(a)` mean what it says. **(c) is the most correct and the most expensive** — it implies the
action is no longer inside the toast's lifecycle at all, which is a larger change to a shared
dispatcher than this defect justifies.

---

**`OQ-5` — Does last-message-wins remain the governing copy contract?**

The roadmap says *"Preserve the existing single-toast/last-message-wins behavior **unless an
explicit product decision changes it**."* This is that decision point. KI-004 mitigated message
loss on exactly this contract, and `I1`/`I2` are asserted at both the unit and E2E tiers.

**Recommendation: YES, unchanged, and say so explicitly.** KI-011 is an **action-continuity**
defect, not a message-continuity defect. Every option above is compatible with last-message-wins.
**Signing this "yes" is what lets `C3` be asserted rather than assumed**, and it is what keeps a
future reader from mistaking a preserved action for a step toward toast stacking.

---

**`OQ-6` — Where does a preserved action live, and what are the a11y expectations?**

`#liveToast` is `role="alert" aria-live="assertive" aria-atomic="true"`
([`base.html:245-247`](../../templates/base.html#L245-L247)). **`aria-atomic="true"` means every
body rewrite re-announces the entire region** — so a preserved button *inside* the announced region
has its label re-read on every subsequent message (`A-I4`). Three sub-decisions:

- **(i) Placement.** Inside `#toast-body` (needs `:60` to become selective) **or** in a sibling
  action slot inside `#liveToast`. **The suite permits either — measured, R6:** B26 counts spans in
  `#toast-body` only, and B30–B35 locate through `#liveToast` by owner ruling
  (`STEP12` §10.11 ruling 4, §10.7-R10). **A relocation outside `#liveToast` would red B30–B35 and
  is therefore excluded.**
- **(ii) Announcement.** Should the preserved action be excluded from re-announcement — a separate
  non-atomic subtree, or a scoped `aria-atomic="false"`?
- **(iii) Focus.** If the user has focused the action and the message is replaced, focus must not
  fall to `document.body`. Today the button is destroyed under the user's focus and focus is lost
  **silently** — a real, currently-unasserted a11y defect that this packet uncovers.

**Recommendation: relocate to a sibling action slot inside `#liveToast` (i), exclude it from the
atomic re-announcement (ii), and require focus preservation across a message replacement (iii).**
The relocation is the smaller change to `:60` — the clear stays unconditional and total, which
keeps `I2`, `I4` and B26 trivially true — and it is the shape the existing suite was deliberately
written to permit. **(iii) should become a named acceptance criterion**, because it is the part of
the defect no existing test at any tier would notice.

---

**`OQ-7` — How is a stale or dangerous action invalidated?**

An action is a **captured closure over state that can go away.** A1's `onClick` is
`toggleActivePlan(N, false)`; between the toast appearing and the click, plan *N* can be deleted
([`:382`](../../static/js/modules/volume-splitter.js#L382)), activated from the history table
([`:960`](../../static/js/modules/volume-splitter.js#L960)), or the whole page can have moved on.
**Today the wipe accidentally limits this exposure — a fix that preserves actions lengthens it.**

Minimum invalidation set to sign:

1. The user **activates** the action (already true — `I5` hides then invokes).
2. The user **dismisses** the toast via the close button.
3. The action's own validity window ends (`OQ-1`).
4. **Open question:** does a **navigation or full re-render** of the raising page invalidate it?
   This is a single-page-per-route app, so navigation tears down the module anyway; a `pagehide`
   or `beforeunload` teardown is likely unnecessary but should be **stated**, not assumed.

**Recommendation: sign 1–3 as the invalidation set, and state explicitly that a stale `onClick` is
the CALLER's responsibility, not the dispatcher's.** `toast.js` cannot know a plan was deleted, and
giving it a validity callback would be `OQ-1(b)` by another name. **This must be written down**:
the fix makes actions live longer, and the packet should not pretend it also made them safer.

---

**`OQ-8` — Does the change to U1's `ourToastContentStands()` require re-signing OD-2?**

**Measured (R5):** preserving the action inverts U1's probe. Two consequences, both real:

- **Announcement.** OD-2 (ratified) says a failure announces *"at a moment when U1's toast no
  longer stands."* With the Retry preserved, U1's content **does** still stand — so a repeat
  slider-originated failure that **announces today would fall silent**.
- **Dismissal.** `dismissCalculateFailureToast()` would `hide()` the live toast while it is showing
  an **unrelated** message, because the probe only asks whether the Retry button exists.

- **(a) Re-sign OD-2** with an amended announce condition, and narrow
  `dismissCalculateFailureToast()` so it fires only when the toast's **message** is also U1's.
- **(b) Declare it acceptable** — the region still stands, so the user is not left uninformed.
- **(c) Sequence around it** — land KI-011 only together with the U1 amendment.

**Recommendation: (a), and treat it as BLOCKING for Gate 1.** U1's plan is explicit that the
`#liveToast` scoping *"must NOT be narrowed to `#toast-body`"* — that instruction stands and must
not be reversed. But the probe was written to answer *"has an unrelated `showToast` replaced our
content?"*, and **a KI-011 fix silently changes what that question means.** A signed criterion whose
meaning drifts under a later packet is exactly the failure mode this repository's gate discipline
exists to catch. **Under no reading may KI-011 land without an explicit decision on this row.**

---

**`OQ-9` — Backward compatibility for the 112 existing callers.**

- **(a) No signature change.** All existing shapes behave identically; continuity is a property of
  the dispatcher, driven by `OQ-1`–`OQ-4`. **Zero caller edits.**
- **(b) Opt-in** — a new option such as `{ action: { …, persist: true } }`. Explicit, but leaves
  the two existing action callers unfixed until edited, and `volume-splitter.js` is **not this
  packet's to edit** without extending scope.
- **(c) Opt-out** — persistence by default, `{ replaceAction: true }` to force removal.

**Recommendation: (a).** Only two action callers exist and both want continuity. (b) would mean
KI-011 ships a mechanism and fixes nothing, since fixing A1 would then require editing
`volume-splitter.js` — which lands this packet in U1's and U2's neighbourhood. **The blast radius
argument cuts the other way here:** with 112 sites, the safest change is the one that requires none
of them to change.

---

**`OQ-10` — Test tier and timing, given the qualification window.**

Restating §0.8 as a decision:

- **(a) E2E-only regression, land any time.** No Vitest case, so no window restart on the
  ledger's operative rule; matches the precedent OD-1 set for U1. **Vitest cases follow after
  `2026-09-05T17:59:26Z`**, with U1-FOLLOWUP-1.
- **(b) Vitest + E2E, land after `2026-09-05T17:59:26Z`.** Strongest coverage; delays the fix by
  roughly nine days from this document's date.
- **(c) Vitest + E2E, land now and accept the restart.** T0 moves; D2 slips by a further fortnight.

**Recommendation: (a) if the fix is wanted before the strict mark; (b) if it is not.** **(c) should
be declined** unless the owner has independently decided D2 is not near-term — it spends the entire
qualification window to buy coverage that (a)-then-follow-up obtains for free. **Note either way:**
a `js-unit` red during the window resets it to zero regardless of tier, so any KI-011 implementation
carries schedule risk.

---

## 0.10 Risks arising from the shared dispatcher

| ID | Risk | Why it is real | Mitigation to carry into Gate 1 |
|---|---|---|---|
| **K1** | **Blast radius.** `toast.js` is imported by 20 modules and reached by **112 call sites** on every page | Measured §0.4.1. Every behavior change is felt by all of them | Prefer `OQ-9(a)`: no signature change, no caller edits. Require the full E2E suite, not a narrowed batch |
| **K2** | **U1 coupling (the sharpest).** Preserving the action inverts `ourToastContentStands()` — measured, **R5** — which changes a **ratified** owner decision (OD-2) and can make `dismissCalculateFailureToast()` hide an unrelated message | Measured, and U1's plan makes the probe's scoping *binding* | `OQ-8`. **Blocking for Gate 1** |
| **K3** | **B26 / B30–B45 are the contract.** 47 cases pin the dispatcher. R6 measures that B26 and B30–B35 permit a relocation **inside `#liveToast`** — but a relocation **outside** it reds B30–B35, and any `innerHTML` write reds B18 | Measured, R6 | Require all 47 green **unmodified**. A red in B30–B35 is *"a real regression in the button's contract, not a bookkeeping update"* (§10.7-R10) |
| **K4** | **The inventory gate reds required pytest.** `tests/test_vitest_inventory_contracts.py` pins 231 / 13 / `toast.test.js: 47` | Read directly, §0.8.2 | `OQ-10`. If Vitest cases are added, the same PR must update that file **and** regenerate both inventory artifacts |
| **K5** | **Qualification-window restart.** A Vitest case is the first post-T0 change to the JS test corpus | §0.8, with U1-FOLLOWUP-1 as governing precedent | `OQ-10` |
| **K6** | **`aria-atomic` re-announcement.** A preserved button inside the atomic assertive region is re-read on every later message | Derived from `base.html:246-247`; **not asserted at any tier** | `OQ-6(ii)`. Add an axe/E2E arm or record the exception in the a11y register |
| **K7** | **Silent focus loss.** The button is destroyed under the user's focus today; focus falls to `document.body` unannounced | Follows from R3 (`isConnected === false`); no test at any tier notices | `OQ-6(iii)`. Make it a named acceptance criterion |
| **K8** | **Longer-lived closures are staler closures.** A preserved action holds `planId` across an unrelated failure; the plan can be deleted or activated meanwhile | `:382`, `:960` are both reachable inside a 6 s window | `OQ-7`. **Write down that staleness is the caller's problem** rather than implying the fix solved it |
| **K9** | **E2E copy pin.** `e2e/volume-splitter.spec.ts:340` asserts `/Plan #\d+ saved\.\s*Activate for Plan tab/i` — the button's text must remain part of the toast's accumulated text | Read directly | A relocation must keep the button inside `#liveToast`'s text content. R6's shape does |
| **K10** | **Stale citations in a doc this packet may not edit.** `STEP12_JS_UNIT_GATE0.md` §10.7-R10 still cites the **pre-U1** anchors `volume-splitter.js:299-306`, `308` and `439`; the live values are **`424-431`**, **`433`** and **`564`**. The `UI_SCENARIOS_GAP_ANALYSIS.md` KI-011 row **was** re-anchored (2026-08-26); §10.7-R10 was not | Measured on `52c44c4` | **Not repaired here** — `STEP12` is a must-not-touch. Recorded so a Gate 1 reader does not re-derive the fix from stale line numbers. Repair belongs to the implementation PR or to a docs packet |
| **K11** | **Sequencing with KI-010 (U3a).** Both defects target `toast.js`, and **both must change `toast.test.js`** — KI-010 must *invert or update* **B45** and re-check **B43**; KI-011 must *add* a fixed-behavior case. Two packets editing the same 47-case file, each moving the pinned count, is a guaranteed conflict and a doubled window exposure | Measured: the KI-010 row and the KI-011 row both name `toast.test.js` obligations | **Serialize.** KI-011 implementation **must not run concurrently with KI-010 implementation** — already a constraint on this packet. Gate 1 must state which lands first and rebase the other |
| **K12** | **U2 in flight.** U2 adds a new `showToast('warning', …)` in `backup-center.js` — a new *later-toast source*, though **no** new action caller | Read from U2's Gate-1 plan | No overlap in scope. Merge order remains unresolved; **do not rebase this branch around U2** |

---

## 0.11 Anticipated Gate 1 entry conditions

Gate 1 does not open until **all** of the following hold. Listed now so the boundary is visible from
Gate 0 rather than discovered later.

1. **All ten `OQ` rows in §0.9 are answered in writing**, with `OQ-1`, `OQ-2`, `OQ-5`, `OQ-8` and
   `OQ-10` explicitly signed — those five decide the shape, the copy contract, the cross-packet
   obligation and the schedule.
2. **`OQ-8` is resolved before any code is written.** Whether OD-2 is re-signed, accepted as-is, or
   sequenced around, the decision is recorded in *this* document and cross-referenced from Gate 1.
   **This packet may not edit U1's planning artifact**; if OD-2 needs amending, that is a separate,
   separately-authorized edit.
3. **KI-010's landing order is decided** (K11), and the loser rebases. Both packets' Gate 1 plans
   must name the same order.
4. **A browser-level reproduction of the §0.3.1 route exists** — §0.2.3 is explicit that today's
   evidence is jsdom plus citation. Gate 1's plan must specify the arm (route interception on
   `GET /api/volume_history` after a successful save) and predict its pre-fix failure.
5. **A mutation matrix is specified**, run against a **copy** under `artifacts/probe/` with a
   byte-identity assertion on the production file, following `STEP12` §10.1's containment rule.
   At minimum: restore the unconditional `innerHTML` clear; drop the preservation branch; break the
   invalidation condition from `OQ-7`; and **run every mutation in both directions**.
6. **The gate set is derived from the changed paths**, per `docs/ai_workflow/QUALITY_GATE.md` —
   `static/js/**` routes to full pytest **and** the E2E suite. **`/verify-suite` is required**;
   Packet B's "no `/verify-suite`" override was a docs-and-tests-only argument and **does not
   transfer to a production JS change**.
7. **The E2E measurement plan accounts for the known baseline.** The default E2E invocation is
   **not** clean (569 passed / 63 failed / 17 not run, measured 2026-08-23) and needs **two**
   invocations. Gate 1 must state the comparison, not assert "zero failures".
8. **The inventory and window consequences of `OQ-10` are written out** — which files move, which
   pinned literals change, and whether T0 restarts — before implementation, not after CI reds.
9. **A plan-review council runs** (`architecture-reviewer`, `test-strategist`,
   `product-risk-reviewer`), with a response matrix and a Plan v2. The roadmap's own reasoning
   applies: *"U3 changes a shared dispatcher every page uses"*, which is why U2's lighter gate is
   **not** available here.
10. **Verification is performed on a base rebased onto `main`**, since U2 and U3a may land first
    and both touch neighbouring surfaces.

---

## 0.12 STOP — Gate 0 owner-decision boundary

**Nothing below this line has been done, and nothing below it is authorized.**

- No production line changed. `static/js/modules/toast.js` is blob
  `42863b4664b7f87a2519556b7f9db8af2cb36e64` on `52c44c4`, unchanged.
- No test file created or modified. The suite is **13 files / 231 cases**, re-measured green in this
  worktree.
- No inventory artifact, ledger row, or status document touched.
- The reproduction harness lives in the gitignored `artifacts/probe/` and is **not** part of this
  PR.
- **Gate 1 has not begun. KI-011 implementation is not authorized**, and it must not run
  concurrently with KI-010 implementation.

**This document's PR carries exactly one new file and merges nothing else.**
