# Packet U3b — KI-011, toast action continuity — **Gate 0 candidate**

> ⚠️ **ANNOTATION 2026-08-27 — the status line below is SUPERSEDED and is annotated, not rewritten.**
> **GATE 0 IS SIGNED** (§1). The owner ruled on all ten `OQ` rows, ruled on sequencing, and authorized
> **Gate 1 planning only**. **Gate 1 is NOT signed and implementation is NOT authorized.** Gate 1 planning is COMPLETE:
> Plan v1 (§2), the three-reviewer council and response matrix (§3), and **Plan v2 (§4)** are
> written; **four owner decisions (OD-11..OD-14) and one unrun mutation (N9) block the signature**
> (§5).
> §0.9's recommendations are superseded by §1's rulings wherever the two differ; §0.9 stays in place as
> the evidence that produced them. This document necessarily predates its own sign-off, so the
> pre-signature text is preserved rather than edited.
>
> > **STATUS: GATE 0 CANDIDATE. NOT SIGNED. NOT AUTHORIZED.**
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

> ⚠️ **ANNOTATION 2026-08-27 — partially SUPERSEDED, annotated in place.** Gate 0 is now **SIGNED** (§1)
> and **Gate 1 planning is COMPLETE** (§2–§4). The live boundary is §5. Every other clause below still stands: no production line
> changed, no test file created or modified, the suite is still **13 files / 231 cases**, no inventory
> artifact / ledger row / status document touched, and **KI-011 implementation is still unauthorized**
> and must not run concurrently with KI-010 implementation.

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

---

## 1. GATE 0 — SIGNED. Owner rulings, 2026-08-27

**The owner signed Gate 0 on 2026-08-27 and authorized Gate 1 planning only.** Implementation
remains unauthorized. The rulings below are the governing text; §0.9's recommendations are
superseded by them wherever the two differ, and §0.9 is left in place as the evidence that produced
them rather than rewritten.

| ID | Question (§0.9) | **RULING** |
|---|---|---|
| **OQ-1** | What makes an action "still valid"? | **Validity is scoped to the raising toast's ORIGINAL duration, ending early on activation or dismissal.** |
| **OQ-2** | Later toast with no action | **Preserves** the standing action. |
| **OQ-3** | Later toast with its own action | **Replaces** the standing action. **Never two actions.** |
| **OQ-4** | Duration precedence | A standing action **extends** the toast through the **later applicable deadline**. |
| **OQ-5** | Last-message-wins | **Preserved.** The action **is not part of the message contract**. |
| **OQ-6** | Placement, announcement, focus | **Relocate the action to a sibling slot inside `#liveToast`**, **exclude it from atomic message re-announcement**, and **explicitly preserve focus across message replacement**. |
| **OQ-7** | Invalidation | **Activation, dismissal, or validity-window expiry.** Stale **caller-owned** state remains the **caller's** responsibility; **document that boundary**. |
| **OQ-8** | U1 / OD-2 | **Re-sign OD-2 with the amended announcement condition**, and **narrow `dismissCalculateFailureToast()`** so it may dismiss **only U1's own matching failure message** — not an unrelated replacement toast. |
| **OQ-9** | Backward compatibility | **No `showToast()` signature change and no caller migration.** |
| **OQ-10** | Test tier and timing | **E2E-only fixed-behavior regression**, so U3b can land **before** the strict qualification mark **without changing the Vitest corpus or restarting T0**. |

**Sequencing ruling.** **KI-011 / U3b lands BEFORE KI-010 / U3a.** U3a remains **deferred until
after the strict mark** and **rebases after U3b**. **Their implementations must not run
concurrently.** Packet **U2** must not be disturbed and its merge order must not be assumed;
reconcile against live `main` and the ownership registry before any eventual implementation.

**What Gate 0's signature does and does not authorize.** It authorizes **Gate 1 planning only** —
this section, §2, §3 and §4 — and the contained measurement in §2.1. It authorizes **no**
production line, **no** test line, **no** inventory regeneration, **no** ledger row, **no**
repository setting, and **no** merge.

---

## 2. PLAN v1 — Gate 1 entry work

> ⚠️ **ANNOTATION — SUPERSEDED IN PART by §4 (Plan v2), and annotated rather than rewritten.**
> The Gate 1 council reviewed **this text**, so it is preserved as reviewed. **§4 governs wherever the
> two differ**, and §3 records every finding and its disposition. Four claims in §2 were measured
> **false** and are corrected in §4: §2.4's console-posture collision (the fixture is **blind** to
> F-NEW-1, not blocked by it), §2.2(F)'s lazy expiry (it does **not** implement the signed **OQ-1**),
> §2.4's pinned-surface bullet (wrong pin cited, and a moving surface declared static), and §2.1g's
> closing sentence (the amendment fixes step 3, **not** the step-2 pairing). §2.1's measurement rows
> otherwise stand and all three reviewers asked that they be preserved verbatim.


> Everything in §2.1 was **measured on `52c44c4`**, in this worktree, against a Flask instance
> serving **this checkout** on port **5311** (`curl` md5 of the served
> `static/js/modules/toast.js` equals the worktree file's md5 — the "relative launch serves the
> other checkout's static" trap was checked, not assumed). **`static/js/modules/toast.js` is blob
> `42863b4664b7f87a2519556b7f9db8af2cb36e64` before, between and after every row**, asserted by the
> harness itself and re-verified after the last run.

### 2.1 Measured evidence

#### 2.1a — Browser-level reproduction of the §0.3.1 route (Gate 1 entry item 1)

`artifacts/probe/browser-repro.mjs`. Real Chromium, real Flask, the real
`volume-splitter.js`, `GET /api/volume_history` intercepted and aborted **only after the save**, so
the page's initial hydration is genuine. **The oracle is a `MutationObserver` TRANSITION log on
`#liveToast`, not a state sample** — the two toasts are milliseconds apart and any post-hoc sample
can miss the button entirely and read as a false green.

**Predicted before the run, and recorded here as the pre-fix prediction: the action is
DESTROYED.** Measured, 3 consecutive runs, identical:

| Arm | Prediction | Measured |
|---|---|---|
| **D1** the Activate action was raised at all | true | **true** — snapshot 1 carries `Activate for Plan tab`, `aria-label="Activate volume plan N"`, `parentIsToastBody: true` |
| **D2** the history-failure toast replaced the body | true | **true** — final body `"Failed to load saved volume plans. Please try again."`, `bg-danger` |
| **D3** the Activate action survives | **false (destroyed)** | **false — DESTROYED.** Final `actions: []` |
| **D4** the failure toast landed after the action toast | true | **true** — first-Activate index 1, first-failure index 2 |

**Control arm** (same script, history refresh allowed to succeed): `actions:` still carries
`Activate for Plan tab` at the end, `bg-success`, **zero console errors**. The destruction is
caused by the replacement, not by the save.

#### 2.1b — F-NEW-1: an uncaught Bootstrap `TypeError` on the replacement path

The failure arm emits, deterministically (3/3), an error the control arm never produces:

```
Global error caught: {message: Cannot read properties of null (reading 'classList'),
 filename: .../static/vendor/bootstrap/js/bootstrap.bundle.min.js, line 6, column 78585,
 error: TypeError: Cannot read properties of null (reading 'classList')}
```

`artifacts/probe/dispose-race.mjs` characterises it by varying **only** the gap between the two
`showToast()` calls, driven through the same module seam `e2e/ui-hardening.spec.ts` uses:

| gap between calls | Bootstrap `TypeError`s | all console errors |
|---:|---:|---:|
| **0 ms** | **2** | 2 |
| 100 ms | 0 | 0 |
| 200 ms | 0 | 0 |
| 400 ms | 0 | 0 |
| 600 ms | 0 | 0 |
| 1000 ms | 0 | 0 |

**It is a dispose-mid-transition race.** `toast.js:103-106` disposes the live instance while its
show transition is still running; Bootstrap's transition-end callback then dereferences a nulled
`_element`. The §0.3.1 route lands at gap ≈ 0 — the next statement plus one aborted fetch — which
is why the reproduction shows it every time.

**Three consequences, and they are not cosmetic.**

1. **It is a defect KI-011 did not know it had.** Nothing in the KI-011 row, `STEP12` §10.7-R10, or
   any test at any tier records it.
2. **It blocks the naive E2E plan.** `e2e/volume-splitter.spec.ts` runs `consoleErrors.assertNoErrors()`
   in `afterEach`. A regression arm that drives the §0.3.1 route **fails on the console posture**
   before it ever asserts anything about the button.
3. **The candidate does NOT fix it** — measured. Preserving the action changes nothing about the
   dispose/construct churn. **See `OD-12` in §2.9.**

#### 2.1c — Mutation matrix (Gate 1 entry item 2)

`artifacts/probe/mutation-matrix.mjs`, against `artifacts/probe/toast.candidate.js` — a
**reference implementation that exists only in the sandbox** and reaches the browser by **Playwright
route interception**. No repository file is written at any point, and
`assertProductionUntouched()` re-reads `git hash-object static/js/modules/toast.js` **before the
first row, between every row, and after the last**.

**Both directions on every row.** A row is `KILLED` only when the arm **fails on the mutant** *and*
**passes on pristine**. A mutation that reds an already-red arm proves nothing and is reported as
`BAD ROW`.

**Nine arms**, each shaped like the E2E regression it stands in for:

| Arm | What it holds |
|---|---|
| **k1** | The KI-011 core, on the **real** save-without-activating route with the history GET aborted |
| **k2** | OQ-3 — a later action replaces; exactly one, and it is the newer |
| **k3** | OQ-4 — a 6000 ms action survives a 500 ms message; the toast is still shown at 2000 ms |
| **k4** | OQ-1/OQ-7 — a 400 ms action is gone 1200 ms later. **Non-isolating; see N4** |
| **k5** | OQ-7 — the close button invalidates the standing action |
| **k6** | **K9** — `#toast-body`'s text still matches `/Plan #\d+ saved\.\s*Activate for Plan tab/i` |
| **k7** | **B26** — exactly one `span` in `#toast-body`, carrying the latest message |
| **k8** | OQ-6 focus — `document.activeElement` is still the action button after a replacement |
| **k9** | OQ-1 expiry **isolated from** dismissal: a 400 ms action inside a toast extended to 6000 ms |

**Result: pristine holds all nine; six of six rows KILLED, both directions.**

| Row | Mutation | Killed by | Survived on |
|---|---|---|---|
| **N1** | restore `toast.js:60`'s wholesale `toastBody.innerHTML = ''` | **k1, k8** | k6 |
| **N2** | OQ-3 violated: a standing action outranks a newly supplied one | **k2** | — |
| **N3** | OQ-4 dropped: the later call's duration wins outright | **k3** | — |
| **N4** | OQ-1/OQ-7 dropped: a standing action never expires | **k9** | **k4** |
| **N5** | OQ-7 dropped: dismissal does not invalidate | **k5** | — |
| **N6** | slot placed **outside** `#toast-body` | **k6** | — |

**Two rows carry a finding, and both are recorded rather than smoothed over.**

- **N4 survived `k4` and is killed only by `k9`.** `k4` cannot tell expiry from dismissal:
  Bootstrap's autohide fires `hidden.bs.toast` at the toast's own delay, so the dismissal path
  removes the action before the expiry path ever runs. **`k9` is the isolating killer** — it
  extends the toast to 6000 ms (OQ-4) so the action's 400 ms deadline passes **while the toast is
  still shown** and `hidden.bs.toast` has not fired. Without `k9`, OQ-1's expiry clause would be
  **unexercised code that no arm can distinguish from its absence**.
- **N1 survived `k6`, correctly.** `k6` raises a single toast, so a wholesale clear has nothing to
  destroy. It is a **placement** arm, not a **preservation** arm; N1 is killed by `k1` and `k8`.

#### 2.1d — The 47-case contract, run against the candidate

Packet C's **mirrored-layout** technique: `artifacts/probe/mirror/static/js/modules/` holds the
candidate beside a **verbatim copy of the real `toast.test.js`**, collected by a probe-scoped Vitest
config that cannot reach the real suite.

| Run | Result |
|---|---|
| **Pre-flight** — mirror loaded with the **pristine production** `toast.js` | **1 file / 47 passed** — proves the mirrored layout resolves and the run is interpretable |
| **Candidate** — same 47 cases, **file unmodified** | **1 file / 47 passed** |

**Criterion C2's Vitest half is therefore measured, not predicted:** the design leaves all 47 cases
green **without touching the file**, which is what makes OQ-10's E2E-only route possible.

#### 2.1e — F-NEW-2: a false green the candidate created, measured and then designed out

**Revision 1 of the candidate held the standing action in a module-level `let`.** That falsifies the
premise recorded in `toast.test.js`'s own header:

> *"toast.js has NO module-level mutable state (every binding in it is function-local, including
> `validTypes`), so there is deliberately no `vi.resetModules()` and no per-test re-import. §4.1 is
> discharged for this module by that fact, not by omission."*

All 47 cases still passed under revision 1 — **and that pass was luck.** A two-case probe measured
the bleed directly:

```
S1: a case raising a 6000 ms action toast          -> passes
S2: THE NEXT CASE, a plain default toast
    expect(constructed[0].delay).toBe(3000)        -> AssertionError: expected 5998 to be 3000
```

`5998` is the previous case's deadline leaking across the `beforeEach`. **That is B29's assertion
shape**, and the real suite escapes it only because B29 (line 365) happens to run **before** the
action cases (line 392). Any reordering, or any new case placed after B30–B38, would red on stale
state — including **the case KI-010 must add or invert in the same file**.

**Revision 2 holds no module state at all.** The standing action lives entirely in the DOM: the slot
node, the button, and a deadline stamped on the button as a data attribute; the dismissal listener
records "already wired" as an **attribute on `#liveToast`**, not a module flag. A fresh
`document.body.innerHTML` resets everything for free. Re-measured: **49/49 green** — the real 47
**plus** S1 and S2, which now both pass. **`toast.test.js`'s stated premise survives the fix
intact, and no `vi.resetModules()` is required.**

#### 2.1f — F-NEW-3: OQ-6's "sibling slot" is ambiguous, and one reading is measurably wrong

`e2e/fixtures.ts`'s `expectToast()` asserts against **`SELECTORS.TOAST_BODY` = `#toast-body`**, and
`e2e/volume-splitter.spec.ts:340` uses it for `/Plan #\d+ saved\.\s*Activate for Plan tab/i`.
**A slot that is a sibling of `#toast-body` therefore reds an existing E2E test** — that is exactly
mutation **N6**, and it is `KILLED` by `k6`.

Both readings of "a sibling slot inside `#liveToast`" are literally satisfiable:

| Reading | Sibling of | B26 | B30–B35 | `volume-splitter.spec.ts:340` |
|---|---|---|---|---|
| **(γ)** slot is a `<div>` child of `#toast-body`, **sibling of the message `<span>`** | the message | **green** (1 span) | **green** (inside `#liveToast`) | **green** — measured, `k6` |
| **(α)** slot is a child of `.d-flex`, **sibling of `#toast-body`** | `#toast-body` | green | green | **RED** — measured, `N6`/`k6` |

**Plan v1 selects (γ)** and flags the ambiguity as **`OD-11`** in §2.9 rather than choosing
silently. (α) remains available if the owner prefers it, at the price of editing
`e2e/volume-splitter.spec.ts:340` and `expectToast`'s scope — an E2E-only edit that does not move
Vitest, but a change to an assertion neither packet set out to touch.

#### 2.1g — F-NEW-4: the OQ-8 regression, measured against the real `volume-splitter.js`

`artifacts/probe/u1-interaction.mjs`. **Only `toast.js` is swapped**, by route interception;
`volume-splitter.js` is the shipped file. Scenario: a slider-originated calculation fails, an
unrelated toast replaces the message, a second slider-originated calculation fails.

| Step | **Production `toast.js`** | **Candidate `toast.js`** |
|---|---|---|
| 1. after the first slider failure | Retry in toast **true**, region **true**, body = U1's message | Retry **true**, region **true**, body = U1's message |
| 2. after an unrelated toast | Retry **false**, body = `"Backup created successfully."` | Retry **true**, body = `"Backup created successfully.Retry"` |
| 3. after the second slider failure | Retry **true**, body = **U1's message** | Retry **true**, body = **`"Backup created successfully.Retry"`** |
| **OD-2 outcome** | **RE-ANNOUNCED** | **DID NOT re-announce** |

**Under the fix, and with no amendment, the user whose calculation just failed is left looking at
`"Backup created successfully."` with a `Retry` button beside it.** That is not a subtle
degradation — it is a success message standing over a failure, which is **strictly worse than the
defect KI-011 describes**. U1's durable inline region is present throughout in both columns, so the
user is not uninformed; but the toast — the assertive live region — is actively misleading.

**This is the measurement that makes OQ-8's amendment mandatory rather than tidy**, and it shows the
exact shape of the fix: the announce probe must key on U1's **message**, not on the button's
presence. Step 2's own snapshot proves the two probes diverge — `retryInToast = true` while the body
contains no part of `CALCULATE_ERROR_MESSAGE`.

### 2.2 Implementation design (Gate 1 entry item 3)

Normative. `artifacts/probe/toast.candidate.js` (revision 2) is the **reference**, not the
deliverable; the implementer writes `static/js/modules/toast.js` from this section.

**(A) No module state — binding, not stylistic.** Every binding in `toast.js` stays
**function-local**. The standing action is read from the DOM on each call. **§2.1e is the reason**,
and the rule is load-bearing for KI-010, which must add or invert a case in the same file.

**(B) The slot.** A `<div class="toast-action-slot" aria-live="off">`, created lazily as the **last
child of `#toast-body`**, sibling of the message `<span class="toast-message">`. **A `div`, never a
`span`** (B26 counts `#toast-body span` and must stay at 1). **Inside `#toast-body`** (§2.1f).

**(C) Message rendering replaces `:60`.** `toastBody.innerHTML = ''` is **deleted**. On first
render into a body that has no managed message node, call `replaceChildren()` **once** to drop the
template's comment and indentation, then install the message `<span>`. Every later call sets
`messageSpan.textContent` — a targeted replacement. `textContent`, **never** `innerHTML` (invariant
**I4**, B18).

**(D) Action resolution.**
- Well-formed action supplied → `clearStanding()` then append a fresh button (**OQ-3**).
- No action supplied → leave the standing action untouched (**OQ-2**).
- Malformed action (non-function `onClick`, falsy label) → **no button, and the standing action is
  left alone** — B33/B34 require the message to render and nothing to error.

**(E) Deadlines (OQ-1, OQ-4).** The button carries `data-action-deadline = Date.now() + duration`
**of the call that raised it**. The Bootstrap delay for any call is
`max(thisCall.duration, standingDeadline - Date.now())`. Bootstrap exposes no "extend the timer"
API, so the existing dispose/construct pair stays — see **`OD-12`**.

**(F) Invalidation (OQ-7).** Three paths, no more: **activation** (`button.remove()` inside the
click handler, after `hide()` and before `onClick()` — B36's order is preserved); **dismissal** (one
`hidden.bs.toast` listener, guarded by a `data-action-dismiss-wired` **attribute on `#liveToast`**,
never a module flag); **expiry** (checked at the top of every `showToast()`).
**Documented boundary, per OQ-7:** `toast.js` cannot know that plan *N* was deleted or already
activated. **A stale `onClick` is the CALLER's responsibility.** The fix makes actions live
**longer**, and therefore makes them **more** exposed to caller-owned staleness, not less. That
sentence belongs in the module docstring.

**(G) Announcement (OQ-6).** The slot carries `aria-live="off"`. **No `toast.js` write to
`#liveToast`'s `role`, `aria-live` or `aria-atomic`** — invariant **A-I2** stands. If `base.html`'s
`aria-atomic` boundary must move for a screen reader to honour the exclusion, that is a **template
change** and is called out as **`OD-13`**; nothing at any tier currently pins `#liveToast`'s
`aria-atomic` (`e2e/ui-hardening.spec.ts:358-364` asserts the **container**'s).

**(H) Focus (OQ-6).** In the pristine path the button is never detached, so focus survives with no
code. The capture/restore pair is retained anyway: it costs two lines, it is what **k8** kills **N1**
with, and it is the seam any future re-rendering variant needs.

### 2.3 The U1 amendments (OQ-8)

Both in `volume-splitter.js`. **They are part of the KI-011 implementation PR** — U1's planning
document is **not** edited by U3b, and OD-2's re-signature is recorded **here**.

1. **Split the probe in two.** `ourActionStands()` keeps today's exact selector
   `#liveToast button[aria-label="Retry volume calculation"]`, still scoped to **`#liveToast`, never
   `#toast-body`** — U1 makes that scoping binding and it is not reversed. **Add**
   `ourMessageStands()`, which asserts `#toast-body`'s **message node** text equals
   `CALCULATE_ERROR_MESSAGE`.
2. **Amended announce condition (OD-2, re-signed).**
   `forceAnnounce || !standing || !ourMessageStands()`. §2.1g measures why: after the fix,
   `ourActionStands()` is `true` while the visible message belongs to someone else.
3. **Narrowed `dismissCalculateFailureToast()`.** `if (!ourMessageStands()) return;` before the
   `hide()`. Today's button-only probe would dismiss an **unrelated** toast once the button
   survives replacement.
4. **OD-2's re-signed wording**, for the record: *"Repeat slider-originated announcements are
   suppressed while the same failure region **and U1's own toast MESSAGE** stand; explicit user
   commands always announce, and so does any failure at a moment when U1's **message** no longer
   stands."* The only change is **content → message**; the rest is OD-2 verbatim.

### 2.4 The E2E-only regression plan (Gate 1 entry item 4)

**All arms land in `e2e/volume-splitter.spec.ts`. No Vitest file is created or edited. No case is
added, removed or renamed under `static/js/**/*.test.js`.**

| Arm | Drives | Asserts | Killed mutation |
|---|---|---|---|
| **t1** | Save without activating; `GET /api/volume_history` fails | The Activate action is **still in `#liveToast`** and **still carries `aria-label="Activate volume plan N"`**, while `#toast-body` shows the history-failure message | **N1** |
| **t2** | `t1`, then **click** the surviving action | `POST /api/volume_plan/N/activate` is issued **with the original N**, and the history row for N shows active. **The closure, not merely the node** | **N1** |
| **t3** | An action toast, then a toast **with its own action** | Exactly **one** action button; its label is the newer one | **N2** |
| **t4** | A 6000 ms action toast, then a 500 ms message | The toast is **still shown** ~2000 ms later | **N3** |
| **t5** | A 400 ms action toast inside a toast extended to 6000 ms | The toast is **still shown** and **no** action button remains — expiry, isolated from dismissal | **N4** |
| **t6** | An action toast, then the close button, then an unrelated toast | **No** action button | **N5** |
| **t7** | The save toast alone | `#toast-body` still matches `/Plan #\d+ saved\.\s*Activate for Plan tab/i` — the existing `:340` contract, restated as a guard | **N6** |
| **t8** | Focus the action, then replace the message | `document.activeElement` is still the action button | **N1** |
| **t9** | U1: slider failure → unrelated toast → slider failure | The second failure **re-announces** — `#toast-body` carries `CALCULATE_ERROR_MESSAGE` again | the OD-2 amendment (§2.3) |

**Counts and artifacts.**

- `static/js/modules/__tests__/toast.test.js` stays at **47 cases**, byte-identical.
- The Vitest corpus stays at **13 files / 231 cases**, so
  `git rev-parse <sha>:static/js/modules/__tests__` is **unchanged across the merge** and Q2's
  restart clause **does not engage**. **T0 remains `2026-08-22T17:59:26Z`; the strict mark remains
  `2026-09-05T17:59:26Z`.**
- `tests/test_vitest_inventory_contracts.py` is **not edited** — its `231` / `13` /
  `toast.test.js: 47` literals all still hold.
- **Both inventory artifacts ARE regenerated**, because `playwright.total_tests` moves by the
  number of arms added and per-spec Playwright counts are a pinned surface
  (`QUALITY_GATE.md` line 59). **This is the same move #423 made** (649 → 662) without engaging Q2.
- `e2e/volume-splitter.spec.ts` is **already** in `ci.yml`'s required functional set
  (`ci.yml:363`), so **no spec is added to that list** and the `required_functional_set` pin at
  `ci.yml:1173` is untouched. *(Adding a spec to that list reds pytest through a pinned count — a
  trap this plan does not go near.)*
- Any `page.waitForTimeout` added moves the **`hard_waits`** surface. `t4` and `t5` are
  duration-shaped and are the likely sites; prefer `expect(...).toBeVisible({timeout})` /
  `toBeHidden({timeout})` **time-bounded positives** over hard waits, exactly as U1's `s3` was
  reworked to.

**The console posture is a blocking dependency, not a detail.** Arms `t1`, `t2` and `t8` drive the
gap-0 sequence that produces **F-NEW-1**. `e2e/volume-splitter.spec.ts`'s `afterEach` runs
`consoleErrors.assertNoErrors()`. Either **`OD-12` resolves to fixing F-NEW-1**, or those arms need
U1's allow-one posture with the Bootstrap `TypeError` named explicitly. **A silent allow-list here
would hide a real defect**, so if the allow-list is chosen it must name the exact message.

### 2.5 Verification gates (Gate 1 entry item 5)

Path-derived from `QUALITY_GATE.md`. The diff touches `static/js/**` (production JS) and `e2e/**`.

| Gate | Why it is in the set | Pass condition |
|---|---|---|
| **Full pytest** | `static/js/**` routes to it; `tests/test_vitest_inventory_contracts.py` and the CSS/inventory contracts live there | green, and the three Vitest literals **unchanged** |
| **Full Chromium E2E** | `static/js/**` + `e2e/**`; `toast.js` is reached by **112 call sites in 20 modules**, so a narrowed batch cannot cover the blast radius | see the two-invocation comparison below |
| **`scripts/generate_test_inventory.py --check`** | per-spec Playwright counts moved | regenerated **in the same commit**, `--check` exits 0 |
| **`npm run test:js`** | the corpus must be provably unmoved | **13 files / 231 cases**, and `toast.test.js` byte-identical |
| **Visual specs** | `toast.js` renders into a shared surface | no new baseline. A visual red is **REAL** and is not fixed with `emit_baseline` |
| **Manual smoke** | `QUALITY_GATE.md` requires it for interactive `static/js/**` | the §0.3.1 route driven by hand, plus one toast on a second page |
| **`/verify-suite`** | **required** | green |

**`/verify-suite` is required and Packet B's override does not transfer.** That override was argued
for a **docs-and-tests-only** diff. U3b changes production JS on the most-imported module in the
application; the override is void by its own terms.

**The two-invocation comparison, stated because "zero failures" is unmeetable.** The default E2E
invocation is **not** clean — measured **569 passed / 63 failed / 17 did not run** on 2026-08-23,
because visual specs are **not** excluded by default (`PW_VISUAL_SEED` selects the seed script, not
the spec set). The gate is therefore **two invocations and a comparison**, never an absolute:

1. **Non-visual functional run** (549 tests) on the branch **and** on its merge-base, same machine,
   same session. **Pass condition: the failure set is identical apart from the new arms passing.**
2. **Seeded visual run** (100 tests) on both. **Pass condition: identical, and no new baseline.**

Ad-hoc batches are **nondeterministic**: before attributing any red to the diff, **stash and re-run
the identical batch**. Verification runs on a base **rebased onto live `main`**, since U2 may land
first.

### 2.6 Migration notes (Gate 1 entry item 7)

Required by the refactor invariant — this changes shared user-facing behavior.

1. **`showToast()`'s signature is unchanged.** All **112** call sites keep working with no edit.
   **No caller migration.** (OQ-9)
2. **New observable DOM.** `#toast-body` gains two managed children: `span.toast-message` and
   `div.toast-action-slot`. Anything selecting `#toast-body > span` by position, or reading
   `#toast-body.innerHTML`, sees a new shape. **Audited: `expectToast` and
   `volume-splitter.spec.ts:340` read `textContent` and are unaffected — measured as `k6`.**
3. **`toast.js:60`'s wholesale clear is deleted.** That is the behavioral change. **Last-message-wins
   is unchanged** (OQ-5), verified by **k7** against B26's exact assertions.
4. **An action can now outlive the message that raised it.** Bounded by OQ-1/OQ-7. **A stale
   `onClick` is the caller's problem** and the module says so (§2.2 F).
5. **A toast can now stay visible longer than its own `duration`** when a standing action's deadline
   is later (OQ-4). Anything asserting a toast is **gone** must be re-read. **Audited across `e2e/**`:
   exactly one such assertion exists** — [`e2e/volume-splitter.spec.ts:1123`](../../e2e/volume-splitter.spec.ts#L1123),
   `await expect(page.locator(SELECTORS.TOAST)).toBeHidden()`, inside U1's stale-response arm. **It is
   unaffected, and the reason is specific rather than reassuring:** in that scenario the stale `500`
   is discarded by U1's `calculateRequestSeq` guard, so `enterCalculateFailureState()` never runs and
   **no action toast is ever raised** — there is no standing deadline to extend. **This is the only
   place the OQ-4 extension could have surfaced as a red, and it must be re-checked by MEASUREMENT at
   implementation time, not by re-reading this note.** No `#toast-body` assertion is at risk: every
   one of them (`empty-states.spec.ts:70`, `:85`, `:144`; `workout-plan.spec.ts:713`, `:772`; and
   `expectToast` itself) uses `toContainText`, which is substring-based on `textContent` and is blind
   to the slot's added whitespace — measured as `k6`.
6. **`volume-splitter.js` gains `ourMessageStands()`; `ourToastContentStands()` is renamed
   `ourActionStands()`.** OD-2 is **re-signed** with content → message (§2.3). **U1's planning
   document is not edited by U3b** — the re-signature lives in §1 and §2.3 of this document.
7. **`toast.test.js` is not edited and stays at 47 cases** — measured green against the design
   (§2.1d). **The "no module-level mutable state" premise in its header remains TRUE** after the
   fix (§2.1e), and that is a deliberate design constraint, not an accident.
8. **`UI_SCENARIOS_GAP_ANALYSIS.md`'s KI-011 row flips to Mitigated** and links `t1`, `t2` and `t8`,
   per that file's own rule at `:109-112`. **That edit belongs to the implementation PR, not to
   #426.**

### 2.7 Sequencing and rebase requirements (Gate 1 entry item 7)

- **U3b lands before U3a.** Owner ruling, §1. **Their implementations must not run concurrently.**
- **U3a rebases onto U3b**, after the strict mark. KI-010 must **invert or update B45** and
  re-check **B43**, which **does** change a Vitest case and **does** restart the window — the
  reason it is deferred past `2026-09-05T17:59:26Z`.
- **U3a inherits §2.1e as a hard constraint**: `toast.js` must still hold no module-level mutable
  state when KI-010 adds its case, or the B45 inversion lands on a file whose premise has silently
  become false.
- **U2 is not disturbed and its merge order is not assumed.** Before implementation: re-fetch, re-read
  `gh pr view --json state`, re-read `WORKSTREAM_OWNERSHIP.local.md`, and rebase onto whatever
  `main` actually is. If U2 has landed and touched `backup-center.js`, **nothing in this plan
  conflicts** — U2 adds a plain `showToast('warning', …)` with **no** action button.
- **A squash merge means the SHA CI verified is never the SHA on the trunk.** Re-verify after
  landing by **blob SHA**, not by "the PR was green".

### 2.8 Open items carried into Gate 1 review

| ID | Item | Why it is the owner's, not the plan's |
|---|---|---|
| **OD-11** | "**Sibling slot inside `#liveToast`**" — sibling of the **message** (γ) or of **`#toast-body`** (α)? | Plan v1 selects **(γ)**. (α) is **measurably** incompatible with `e2e/volume-splitter.spec.ts:340` unless that test's scope is changed (§2.1f, N6/k6). **A plan may not narrow a criterion the owner signed**, so the reading is confirmed, not assumed |
| **OD-12** | **F-NEW-1** — fix the dispose-mid-transition `TypeError` in this packet, or file it as **KI-013** and allow-list it in the new arms? | It is a **new defect**, outside KI-011's signed scope, **and** it blocks `t1`/`t2`/`t8`'s console posture (§2.1b, §2.4). Both options are real; the choice is a scope decision |
| **OD-13** | Does the atomic-announcement exclusion require moving `aria-atomic` in **`base.html`**? | `aria-live="off"` on the slot handles the slot's **own** changes. Whether a screen reader honours the exclusion when the **message** changes depends on nested-`aria-atomic` support. **Nothing at any tier pins `#liveToast`'s `aria-atomic`**, so the change is available — but it is a template edit OQ-6 did not name |

---

## 3. Gate 1 council and response matrix

Three reviewers ran in parallel against **Plan v1 as written in §2**, each told that §1's rulings
were not open for relitigation but that a **silent narrowing** of one must be flagged. All three
returned **"needs revision"**. **Every finding is accepted**, in whole or with a stated
modification; **none is rejected**. Where a finding is accepted with a different remedy than the
reviewer proposed, the reason is measured, not argued.

**Reviewer keys:** `A` = architecture-reviewer · `T` = test-strategist · `P` = product-risk-reviewer.
`S` = found by this session's own measurement, not by a reviewer.

### 3.1 The four findings that falsified a claim Plan v1 made about itself

These are recorded first because each is a case of the plan being **wrong**, not merely incomplete.

| # | Finding | Disposition |
|---|---|---|
| **T3** | **§2.4's console-posture collision does not exist.** Plan v1 said arms `t1`/`t2`/`t8` *"fail on the console posture before it ever asserts anything about the button"*. **Measured false on both channels:** `e2e/fixtures.ts:42` drops any console text containing `'Global error caught'` — the exact prefix `static/js/global-error-handler.js:22` emits — and `:61-62` drops any `pageerror` containing `'classList'` **or** `'Cannot read properties of null'`. F-NEW-1's message is `Cannot read properties of null (reading 'classList')`. **Filtered twice over.** | **ACCEPTED, and it inverts the conclusion.** The fixture is **blind** to F-NEW-1, not blocked by it — so **OD-12 option (b), "allow-list it", is already the silent status quo on `main`**, which is worse than the collision Plan v1 imagined. Worse still: under option **(a)** the fixture could not tell you whether the fix worked. §4 adopts the reviewer's third option — a **dedicated, unfiltered `pageerror` collector** used as F-NEW-1's own oracle — and rewrites OD-12's option set around it |
| **T2 / A7 / P6** | **OQ-1 is not implemented as signed.** §2.2(F) makes expiry lazy — checked only at the top of `showToast()`. **Measured on the reference implementation:** an action **2273 ms past its deadline** was still rendered, `tabIndex >= 0`, and **its `onClick` fired on click**, while the toast was still shown. The owner signed *"validity is scoped to the raising toast's ORIGINAL duration"* | **ACCEPTED, with the remedy that satisfies the ruling instead of amending it.** T2 offered (a) eager expiry or (b) accept lazy expiry and take it back to the owner. **§4 takes (a)**: a `setTimeout` armed at the deadline, its handle stamped on the button as `data-action-timer` and cancelled on removal — so §2.2(A)'s no-module-state rule holds. **Re-measured: the action is gone at +2500 ms with the toast still shown, and `onClick` does not fire.** The owner is not asked to weaken a ruling that can simply be met. New mutation **N7** and new arms `t5b` / `k10` |
| **T6** | **Wrong pin cited, and a moving surface declared static.** `ci.yml:1173` is `req = pw["required_functional_set"]` inside a job-summary print — it asserts nothing. **The real pin is `tests/test_playwright_shard_launcher_contracts.py:67`, `assert len(set(ci_required_specs())) == 25`**, which counts **specs**. And `required_functional_set.tests` **does** move | **ACCEPTED.** Verified: the `== 25` assertion is at that line and counts specs, so it is genuinely untouched. Verified from `TEST_INVENTORY.json`: `playwright.total_tests` **662**, `required_functional_set` `{spec_files: 25, tests: 527}`, `volume-splitter.spec.ts` **46** tests, `hard_waits.total_lines` **82**. §4.6 replaces the bullet with the measured values and the correct pin. **Both sibling packets cited this correctly; Plan v1 regressed a citation they got right** |
| **P1** | **§2.1g's closing sentence is misleading.** *"Under the fix, **and with no amendment**, the user … is left looking at `"Backup created successfully."` with a `Retry` button beside it"* — the qualifier is false. The amendment acts at **step 3** (announcement); **step 2's pairing is unchanged by it** | **ACCEPTED.** §4.1 restates it: the amendment restores the second failure's announcement and **leaves the message/action pairing in place**. The pairing becomes its own owner item, **OD-14** (P2) |

### 3.2 Findings that changed the design

| # | Finding | Disposition |
|---|---|---|
| **A1 / S** | The slot is block-level; `.toast .toast-body` is `text-align: center`, so the action drops to its own line. **The packet's own harness had measured this and §2 reported no result.** Also: `resolveSlot()` ran **unconditionally**, so all 112 sites injected a node | **ACCEPTED in full.** Measured and published as **§4.1's F-NEW-5 table**: block slot = 350×**142** with the action on a second line; **`d-inline` = 350×118, identical to production in every rect**. `.d-inline` already ships in `bootstrap.custom.min.css`, so **no SCSS edit, no bundle drift, and the CSS gate stays out of the gate set**. Slot creation moved **inside** the well-formed branch — re-measured, a no-action toast now creates **no slot at all** and is pixel-identical to production |
| **A2 / P5** | The rename orphans `ourActionStands()` (both call sites move to the message probe), **and** it falsifies text in two files — `volume_failure_feedback/PLANNING.md:1280` (**U1-FOLLOWUP-1**, an OPEN obligation naming `ourToastContentStands()` and the exact condition) and the **KI-012** row at `UI_SCENARIOS_GAP_ANALYSIS.md:107`, which the implementation PR edits anyway. `OQ-8` authorized re-signing OD-2 and narrowing the dismiss guard — **not** a rename | **ACCEPTED; the rename is DROPPED.** §4.3 keeps `ourToastContentStands()` with its binding comment untouched, adds `ourMessageStands()`, and gives the original probe a **live caller** by making the dismiss guard a **conjunction**: `if (!ourToastContentStands() \|\| !ourMessageStands()) return;`. Strictly narrower than today, no orphan, no rename. New **K13** row records that U1-FOLLOWUP-1's quoted condition still goes stale, and §4.6 adds the KI-012 restatement to the same commit |
| **A3** | §2.3 described `ourMessageStands()` in prose. The literal reading (`#toast-body`'s `textContent`) is **measurably never true** once the slot lives inside `#toast-body` — §2.1g measured `"Backup created successfully.Retry"`. `a6` and `s3` would both red | **ACCEPTED.** §4.3 writes the selector normatively rather than describing it |
| **A4** | `span.toast-message` would become an **unpinned cross-module DOM contract**, invented by `toast.js` and depended on by `volume-splitter.js`, with `toast.js` handed to U3a next. A rename there breaks it silently, surfacing only as two U1 arms a KI-010 implementer would misattribute | **ACCEPTED.** `toast.js` **exports `toastMessageText()`**; `volume-splitter.js` imports it instead of querying. An addition, not a signature change, so **OQ-9 holds**. Implemented in the reference and re-measured green |
| **A5** | Bootstrap fires `hidden.bs.toast` on **auto-hide**, not only on the close button, so a button-presence probe stops being *"blind to visibility"* — the property `volume-splitter.js:257` documents | **ACCEPTED, and measured.** After a 700 ms auto-hide: the **button** probe reads `false`, the **message** probe reads `true`. This is a **second, independent reason the OD-2 amendment is mandatory**, unrelated to §2.1g's replacement scenario. Published as **§4.1's A5 row** and covered by arm `t11` |
| **A6** | The single `hidden.bs.toast` listener has **no identity check**. If OD-12 fixes the dispose race, a hide transition completing after the next toast is shown would clear the **new** action | **ACCEPTED as a design requirement, and reported honestly as currently unkillable.** A generation counter is stamped on `#liveToast` and captured on the button; the listener clears only on a match. **Mutation N8 removes that check — and N8 SURVIVED (`k11` holds both ways).** Measured reason: **F-NEW-1 masks it.** The dispose throws inside Bootstrap's queued transition, so the stale `hidden` never fires. **N8 is an equivalent mutation whose equivalence is caused by another open defect.** §4.7 makes it binding: **if OD-12 resolves to (a), N8 must be re-run and must then be KILLED** |
| **P3** | `aria-live="off"` on the slot does **not** exclude it from an **atomic ancestor's** re-announcement. The nearest ancestor with `aria-atomic` is `#liveToast` (`base.html:247`), so every later message is announced as *"&lt;new message&gt; Activate for Plan tab"* — **A-I4 unmitigated**. And OD-13's escape hatch is illusory: removing `aria-atomic` from `#liveToast` promotes the **container** at `:238`, which **is** pinned by `e2e/ui-hardening.spec.ts:361-363` | **ACCEPTED — verified line by line.** This is the most consequential a11y finding in the round. §4.2(G) no longer claims the exclusion; OD-13 is rewritten as the real binary: **accept per-message re-announcement of the action label, or change the container's `aria-atomic` and the spec that pins it.** `OQ-6(ii)` cannot be delivered as the plan assumed |
| **P4** | *"The only change is content → message"* is inaccurate: OD-2's clause 2 substitutes **`toast → message`**, and that is the load-bearing clause | **ACCEPTED.** §4.3 quotes OD-2 verbatim and marks **both** substitutions. The "the rest is verbatim" claim is withdrawn |

### 3.3 Findings that changed the regression plan or the gates

| # | Finding | Disposition |
|---|---|---|
| **T1** | `t5` describes **two** calls; `k9` needs **three** — the third triggers the lazy sweep. As written `t5` fails on the *correct* implementation | **MOOT for the stated reason, ACCEPTED for a better one.** §4's eager expiry removes the dependence on a third call entirely: the action is now gone on a **timer**. `t5` is rewritten around the timer, and the sequence is stated in full so a later tidy-up cannot delete a load-bearing step |
| **T4** | §2.3's **narrowed dismiss guard has no arm and no mutation row**. `s3` exercises only the positive direction and stays green with or without it | **ACCEPTED.** New arm **`t10`** and mutation **`N9`** in §4.4/§4.7, both specified. §4.7 makes running `N9` both directions a **Gate 1 exit condition** |
| **T5** | The tree-hash claim is **inferred from counts**, which runs backwards — a body edit or a name swap preserves 13/231 and moves the tree. And **`vitest.config.js` is never mentioned**, though the rule measures it | **ACCEPTED.** §4.5 adds a gate row that measures the operative rule **directly and after the squash lands**: `git rev-parse <merge-base>:static/js/modules/__tests__` == the post-merge value, `git hash-object vitest.config.js` equal on both, and the three literals at `tests/test_vitest_inventory_contracts.py:57,58,67` unchanged |
| **T7** | **`tsc --noEmit` is missing from §2.5.** `tsconfig.json:13` includes `e2e/**/*.ts`; the `tsc` half of `Type Check` is required and blocking. Nine new arms in a `.spec.ts` route straight to it | **ACCEPTED — verified.** Added to §4.5. pyright correctly stays out: the diff touches no `.py` |
| **T8** | The two-invocation comparison is **not executable**: counts are stale (569/63/17 sums to 649; live `total_tests` is **662**), the 549/100 split is not derivable, there are no commands or artifacts, and the pass condition contradicts the plan's own nondeterminism note | **ACCEPTED in full.** §4.5 restates it as **set containment on emitted JSON**: split by **spec glob** not by count, `--reporter=json` to `artifacts/e2e-base.json` and `artifacts/e2e-branch.json`, reduce to `(file, title)` non-passing sets, require `branch_failures \ base_failures == {}`, and **stash-and-re-run the identical batch** before attributing any element of that difference. Visual half's oracle is `git status --porcelain` clean under `e2e/**-snapshots/` |
| **T9** | `t2`'s second clause is **unreachable on `t1`'s route** — the history GET is still aborted, so the row cannot appear. §0.3.2 makes this exact point | **ACCEPTED.** The history-row clause is dropped. The load-bearing assertion is the `waitForRequest` on `/api/volume_plan/${N}/activate` with the original `N` — **already measured end to end**: production issues **zero** activate requests, the reference issues exactly `/api/volume_plan/21/activate` for saved plan **21** |
| **T10** | The implementation PR **owes a §13.0 ledger row**, and U3b is the highest-risk merge in the window — a `js-unit` red on that `main` run **resets T0 to zero** and voids OQ-10's premise | **ACCEPTED.** §4.6 and §4.8 record the obligation, including that the row is read at **job level** (`js-unit` `conclusion` + `completed_at`, never the run's overall conclusion) and that landing is proved **by blob SHA** |
| **T11** | Unpaired negatives in `t5`/`t6`, and in the harness arms `k4`/`k5` — `k5` clicks a close button that exists in `base.html` regardless | **ACCEPTED and already applied to the harness.** `k4` and `k5` now assert the action **was raised** before driving the invalidating event; `k10` and `k11` were written with the pairing from the start. Re-run: all rows still resolve, `N7` KILLED |
| **T12** | §2.4's own hard-wait advice would make `t4` **vacuous** — `toBeVisible({timeout:2000})` resolves at t≈0 and passes on N3 | **ACCEPTED.** §4.4 specifies a page-side `hidden.bs.toast` **event log** with a `__t0` stamp for `t4`/`t5`, read in a single `page.evaluate`, plus `test.slow()`. The general hard-wait preference is retained but explicitly **does not apply to the two duration arms** |
| **T13** | Three citation slips: the spec's constant is **`CALCULATE_FAILURE_MESSAGE`** (`e2e/volume-splitter.spec.ts:724`), not the module's `CALCULATE_ERROR_MESSAGE`; §2.4 never says which `describe` block the arms join; `showToastViaModule` is **file-local to `ui-hardening.spec.ts:31-43`**, not exported | **ACCEPTED — all three verified.** §4.4 fixes the identifier, names the block, and rules on the seam: **duplicate the helper into `volume-splitter.spec.ts`** rather than promote it, because promoting it also edits `ui-hardening.spec.ts` and widens the diff for no gain |
| **T14** | The matrix scores an arm that **threw** as a kill, so a mutant-side timeout is indistinguishable from a real kill | **ACCEPTED and already applied.** The verdict logic now requires `mutant[a] === false`; any `ERROR` on either leg makes the row **BAD ROW**. Re-run under the stricter logic: unchanged verdicts |
| **A8** | The implementation PR's **shared-path claims are undeclared** — §0.1 claims only the planning directory | **ACCEPTED.** §4.8 requires a live claim on the exact implementation path set before any code is written |
| **P2** | `OQ-2`'s ruling word *"Preserves"* is common to option **(a)** and option **(c)**; Plan v1 implements (a) normatively and never records the acceptance `OQ-2`'s own text demanded. On the fixed route the toast reads **`Failed to load saved volume plans. Please try again.Activate for Plan tab`** | **ACCEPTED.** New owner item **OD-14**, with the reachable `/volume_splitter` pairings enumerated in §4.9. The malformed-action sub-case (a caller that *tried* to offer action X inherits unrelated action Y) is folded into the same row |
| **P7** | OD-11 under-describes what the owner is re-reading: `OQ-6(i)` offered *"inside `#toast-body`"* **versus** *"a sibling action slot inside `#liveToast`"*, and the ruling used the second phrase. **(γ) is the branch the wording was chosen against** — and the recommendation the owner signed argued the relocation was better because *"the clear stays unconditional and total"*, which §2.2(C) **discards** | **ACCEPTED.** §4.9's OD-11 quotes `OQ-6(i)` verbatim, states that (γ) is the `#toast-body` branch, states that §4.2(C) reverses the stated rationale, and marks §4.2(B)/(C) **provisional** until OD-11 is answered |
| **P8** | §2.6 item 8 flips KI-011 to **Mitigated** with no obligation to file **KI-013**, so under OD-12(b) the registry would read "Mitigated" against a route that still throws deterministically | **ACCEPTED.** §4.6 requires that, under OD-12(b), the same PR files **KI-013** and the KI-011 row's Mitigated note names it and the allow-listed message string |
| **S** | Plan v1's migration note 5 claimed *"no assertion that a toast is gone exists today"*. **False** — `e2e/volume-splitter.spec.ts:1123` is exactly that | **Self-corrected before the council reported.** The note now names it, states the specific reason it is unaffected (the stale `500` is discarded by `calculateRequestSeq`, so no action toast is ever raised), and requires re-checking **by measurement** at implementation time |

### 3.4 What all three reviewers agreed was sound

Recorded so the revisions above are read in proportion.

- **§2.1's measurement layer** — all three called it strong and told me to preserve it verbatim.
  The test-strategist independently re-derived **§2.1c's N4/k4/k9 analysis** from the harness and
  confirmed the non-isolation is real; **§2.1d's pre-flight-plus-candidate pair** was called a
  genuine anti-vacuity control; **§2.1e's state-bleed measurement** was accepted as a real finding
  that produced a better design rather than a waiver; **§2.1g** was called *"the strongest row in
  the packet"* for swapping only `toast.js` while running the shipped `volume-splitter.js`.
- **Containment** — `assertProductionUntouched()` before, between and after every row was called
  exemplary.
- **The call-site audit is clean.** The architecture reviewer checked all 112 independently:
  `fetch-wrapper.js:213`/`:246` pass only `{ requestId }` and become *preservers*, which is `OQ-2`
  as signed; `backup-center.js:778→:798` and `:1039→:1041` are the same success-then-refresh-failure
  shape but raise **no action**; `workout-plan-replacement.js:78,88` pass a severity from
  `resolveSwapErrorToast()` that is only ever `'warning'` or `'error'`, so it never reaches the
  legacy branch. **No missed call site.**
- **Early returns, the legacy branch, and B39/B40/B41** hold — the new work sits after both
  `getElementById` guards.
- **No cross-page coupling.** Multi-page Flask, fresh `#liveToast` per navigation, all state
  DOM-resident. **No local-first or non-goal violation:** no storage, no server round-trip, no
  timer outliving a page.
- **U1's shipped contract is respected** where it matters — the durable region,
  `renderCalculateFailureRegion()`'s idempotence, `clearResults()`, the if-and-only-if property,
  and **OD-4's accepted tradeoff**. The `MutationObserver` on `#toast-body` that OD-4 explicitly
  **rejected** is not reintroduced by any arm; it appears only in the gitignored probe.
- **`OQ-10` / OD-1 window discipline is exact**, and `ci.yml`'s required-list claim is correct.
- **Scope is disciplined** — nothing absorbs KI-010, U2 or U1's residue.

---

## 4. PLAN v2 — the normative plan

> **Plan v2 supersedes §2 wherever the two differ.** §2 is preserved as the text the council
> reviewed; it is not rewritten, so a reader can see what changed and why. §2.1's measurement rows
> stand unchanged except where §4.1 adds to them. **Gate 1 is NOT signed.**

### 4.1 Evidence added after Plan v1

All measured on `52c44c4`, same worktree, same Flask instance on port 5311.
**`static/js/modules/toast.js` re-verified as blob `42863b4664b7f87a2519556b7f9db8af2cb36e64`
after every run.**

#### F-NEW-5 — the slot changes the toast's rendered layout, and a utility class fixes it (A1, S)

`components.css:2787` paints `.toast .toast-body { text-align: center }`, and today's button is an
**inline** sibling of the message text. `artifacts/probe/layout-check.mjs`, three variants, one page,
one viewport:

| Variant | `#liveToast` | `#toast-body` | message | button | slot `display` | same line? |
|---|---|---|---|---|---|---|
| **production** | 350 × **118** | 316 × 50 | x 1096, y 773 | x 1224, y 771 | *(none)* | **yes** |
| block slot | 350 × **142** | 316 × **75** | x 1168, y 745 | x 1163, y 771 | `block` | **no** |
| **slot + `d-inline`** | 350 × **118** | 316 × 50 | x 1096, y 773 | x 1224, y 771 | `inline` | **yes** |

**With `d-inline` the geometry is identical to production in every measured rect** — the same
numbers, not merely close. `.d-inline{display:inline !important}` is **already in
`static/css/bootstrap.custom.min.css`**, so there is **no SCSS edit, no `npm run build:css`, no
compiled-bundle byte change**, and the CSS gate, the compiled-SCSS drift gate and the bundle-size
pin stay **out of this packet's gate set**.

**And the slot is now created only when a button is about to go in it.** Re-measured for a
**no-action** toast — the shape **110 of the 112 call sites** use: production and the reference are
**350 × 108, body 316 × 41, message at x 1168 y 779, `(no slot)`** in both. Nothing is injected.

#### The lazy-expiry window, and its repair (T2 / A7 / P6)

`artifacts/probe/expiry-window.mjs`. A 400 ms action, then a 6000 ms message (OQ-4 extends the
toast), sampled at +2500 ms with no third call:

| | **lazy expiry (Plan v1)** | **eager expiry (Plan v2)** |
|---|---|---|
| toast still shown | true | true |
| expired action still in DOM | **true** | **false** |
| past its deadline by | **2273 ms** | — |
| focusable (`tabIndex >= 0`) | **true** | — |
| **`onClick` fired on click** | **TRUE — the stale action ran** | **false** |

**Plan v1 did not implement the ruling the owner signed.** Plan v2 does, without asking for an
amendment.

#### A5 — auto-hide alone flips the button probe (A)

`artifacts/probe/hidden-race.mjs`. A 700 ms action toast, sampled either side of its own auto-hide:

| Sample | button probe | message probe | `.show` |
|---|---|---|---|
| +300 ms | `true` | `true` | `true` |
| **+1700 ms (auto-hidden)** | **`false`** | **`true`** | `false` |

`volume-splitter.js:257` documents the probe as *"deliberately blind to visibility: it returns true
for a toast that has already dismissed itself."* Once OQ-7 wires invalidation to
`hidden.bs.toast` — which Bootstrap fires on **auto-hide**, not only on the close button — **that
property is gone for the button probe and survives only for the message probe.** This is a
**second, independent reason the OD-2 amendment is mandatory**, unrelated to §2.1g's scenario.

#### t2's closure evidence, measured end to end (T9)

`artifacts/probe/closure-survives.mjs`, on the real save-without-activating route with the history
GET aborted:

| | production | reference |
|---|---|---|
| surviving action buttons | **0** | **1** (`aria-label="Activate volume plan 21"`) |
| activate requests issued | **`[]`** | **`["/api/volume_plan/21/activate"]"`** for saved plan **21** |

**The closure survives, not merely the node.** A fix that re-rendered the button from stale data
would keep every node-shaped assertion green and fail this one.

#### The expanded mutation matrix — 8 rows, 11 arms, both directions

Verdict logic hardened per **T14**: a row is `KILLED` only when `mutant === false` **and**
`pristine === true`; **any `ERROR` on either leg is `BAD ROW`, never a kill.** `k4` and `k5` gained
the paired positives **T11** required. Production blob asserted before, between and after every row.

| Row | Mutation | Verdict | Killed by | Survived on |
|---|---|---|---|---|
| **N1** | restore `toast.js:60`'s wholesale clear | **KILLED** | k1, k8 | k6 *(a placement arm; correct)* |
| **N2** | a standing action outranks a new one (OQ-3) | **KILLED** | k2 | — |
| **N3** | the later call's duration wins outright (OQ-4) | **KILLED** | k3 | — |
| **N4** | a standing action never expires | **KILLED** | **k9** | k4 *(non-isolating; see §2.1c)* |
| **N5** | dismissal does not invalidate (OQ-7) | **KILLED** | k5 | — |
| **N6** | slot placed outside `#toast-body` | **KILLED** | k6 | — |
| **N7** | **no eager expiry timer** — OQ-1 honoured only at call boundaries | **KILLED** | **k10** | — |
| **N8** | **no generation check** on the `hidden.bs.toast` listener | **SURVIVED** | — | k11 |

**N8 survived, and the reason is a finding rather than a gap.** The generation check is
**unkillable while F-NEW-1 stands**: the dispose throws inside Bootstrap's queued transition, so the
stale instance's `hidden.bs.toast` never fires and there is nothing for the check to guard against.
Measured directly — with the check removed, a new action raised 40 ms after a close click **survived
anyway**. **N8 is an equivalent mutation whose equivalence is caused by another open defect.** It is
retained, not deleted, and §4.7 makes the consequence binding.

### 4.2 Implementation design — normative

Supersedes §2.2. `artifacts/probe/toast.candidate.js` (revision 3) is the **reference**, not the
deliverable.

**(A) No module state.** Unchanged and still binding — §2.1e is the reason, and it now also covers
the expiry timer handle and the generation counter, both of which live on DOM nodes.

**(B) The slot.** `<div class="toast-action-slot d-inline" aria-live="off">`, created **only when a
well-formed action is about to be appended**, as the last child of `#toast-body`, sibling of
`span.toast-message`. **A `div`, never a `span`** (B26). **`d-inline`, never a bespoke CSS rule**
(§4.1). **Provisional until OD-11 is answered.**

**(C) Message rendering.** `toastBody.innerHTML = ''` is deleted; on first render into an unmanaged
body, `replaceChildren()` once, then install `span.toast-message`; thereafter set `.textContent`.
`textContent`, never `innerHTML`. **Provisional until OD-11 is answered** — this reverses the
rationale the owner's `OQ-6` recommendation was argued on.

**(D) Action resolution.** Unchanged from §2.2(D): well-formed replaces; absent preserves; malformed
renders nothing and leaves the standing action alone — **the last clause is subject to OD-14**.

**(E) Deadlines.** `data-action-deadline = Date.now() + duration` of the raising call; Bootstrap
delay = `max(thisCall.duration, standingDeadline - Date.now())`.

**(F) Invalidation — three paths, and expiry is EAGER.**
- **Activation** — `button.remove()` after `hide()`, before `onClick()` (B36's order preserved).
- **Dismissal** — one `hidden.bs.toast` listener, guarded by `data-action-dismiss-wired` on
  `#liveToast`, and **generation-aware**: `#liveToast` carries `data-toast-generation`, incremented
  on every render; the button captures the value it was built under; the listener clears **only on a
  match**. See **N8** and §4.7.
- **Expiry** — a `setTimeout` armed at the deadline, its handle stamped as `data-action-timer` and
  `clearTimeout`-ed whenever the button is removed. The lazy sweep at the top of `showToast()` is
  **retained as a belt-and-braces check**, not as the mechanism.
- **Documented boundary (OQ-7):** `toast.js` cannot know plan *N* was deleted or already activated.
  **A stale `onClick` is the caller's responsibility**, and the fix makes actions live **longer**,
  so it increases that exposure rather than reducing it. This belongs in the module docstring.

**(G) Announcement — the claim is withdrawn.** `aria-live="off"` on the slot governs changes
**within** the slot. It does **not** remove the slot from what an **atomic ancestor** presents: the
nearest ancestor with `aria-atomic` is `#liveToast` (`base.html:247`), so **every later message is
announced as "&lt;new message&gt; &lt;action label&gt;"** while an action stands. **`OQ-6(ii)` cannot be
delivered by the slot attribute alone.** `toast.js` still writes none of `#liveToast`'s live-region
attributes (**A-I2** holds). The real choice is **OD-13**.

**(H) Focus.** Unchanged; the button is never detached, and the capture/restore pair stays as `k8`'s
kill for **N1**.

**(I) Exported predicate (A4).** `toast.js` exports `toastMessageText()`, returning
`document.querySelector('#toast-body span.toast-message')?.textContent ?? null`. Callers ask the
module rather than querying its DOM shape, so a KI-010 rename cannot break `volume-splitter.js`
silently. **An addition, not a signature change — OQ-9 holds.**

### 4.3 The U1 amendments — no rename

Supersedes §2.3.

1. **`ourToastContentStands()` is KEPT, unrenamed**, with its binding `#liveToast`-scoping comment
   untouched.
2. **Add `ourMessageStands()`** — `toastMessageText() === CALCULATE_ERROR_MESSAGE`, using the
   module's exported predicate, **not** a query on `#toast-body` and **not** `#toast-body`'s own
   `textContent`, which can never equal the message once a button lives inside it (A3).
3. **Announce condition (OD-2, re-signed):**
   `forceAnnounce || !standing || !ourMessageStands()`.
4. **Dismiss guard, narrowed to a conjunction:**
   `if (!ourToastContentStands() || !ourMessageStands()) return;` before the `hide()`. Strictly
   narrower than today, and it keeps the original probe live so nothing is orphaned (A2).
5. **OD-2's re-signature, with both substitutions marked.** Ratified text
   (`volume_failure_feedback/PLANNING.md:1272`):
   > *"Repeat slider-originated announcements are suppressed while the same failure region **and
   > U1-owned toast content** stand; explicit user commands always announce, and so does any failure
   > at a moment when **U1's toast** no longer stands."*

   Re-signed:
   > *"Repeat slider-originated announcements are suppressed while the same failure region **and
   > U1's own toast MESSAGE** stand; explicit user commands always announce, and so does any failure
   > at a moment when **U1's MESSAGE** no longer stands."*

   **Two substitutions, not one:** clause 1 `toast content → toast message`; clause 2
   **`toast → message`** — and clause 2 is the load-bearing one. Pre-fix the two probes were
   provably co-extensive (`:60` destroyed message and button together); post-fix they diverge, for
   **two** independent reasons — replacement (§2.1g) and **auto-hide** (§4.1, A5).

### 4.4 The E2E-only regression plan

Supersedes §2.4. **All arms in `e2e/volume-splitter.spec.ts`, in a new `test.describe` block using
the file's standard `assertNoErrors()` posture** — not U1's allow-one block. **`showToastViaModule`
is duplicated into this file** rather than promoted from `ui-hardening.spec.ts:31-43`, so the diff
does not widen (T13). The spec's constant is **`CALCULATE_FAILURE_MESSAGE`** (`:724`).

| Arm | Drives | Asserts | Kills |
|---|---|---|---|
| **t1** | Save without activating; history GET fails | Action still in `#liveToast` with its `aria-label`, while `#toast-body` shows the history-failure message | N1 |
| **t2** | `t1`, then **click** the action | `waitForRequest` on `/api/volume_plan/${N}/activate` with the **original** N. **No history-row clause** — unreachable while the GET is aborted (T9) | N1 |
| **t3** | Action toast, then a toast with its own action | Exactly one action; label is the newer | N2 |
| **t4** | 6000 ms action toast, then a 500 ms message | **Page-side `hidden.bs.toast` event log** with a `__t0` stamp: `__hideAt` undefined or `> 1500`. **Not `toBeVisible({timeout})`, which resolves at t≈0 and is vacuous** (T12). `test.slow()` | N3 |
| **t5** | 400 ms action toast, then a 6000 ms message | Paired positive first (**the action was raised**), then in **one** `page.evaluate`: toast still shown **and** zero actions. Eager expiry is the mechanism; no third call needed | N4 |
| **t5b** | `t5`, then **click where the button was** | The original `onClick` **did not fire** | **N7** |
| **t6** | Action toast → close button → unrelated toast | Paired positive first, then no action | N5 |
| **t7** | The save toast alone | `#toast-body` still matches `/Plan #\d+ saved\.\s*Activate for Plan tab/i` | N6 |
| **t8** | Focus the action, then replace the message | `document.activeElement` is still the action button | N1 |
| **t9** | Slider failure → unrelated toast → slider failure | The second failure **re-announces** | OD-2 amendment |
| **t10** | Calculate failure (Retry stands) → unrelated 6000 ms toast → **successful** calculation | `#liveToast` is **still visible** and still shows the unrelated message — the narrowed dismiss guard did **not** hide a stranger's toast | **N9** |
| **t11** | Action toast, let it **auto-hide**, then a slider failure | The failure **re-announces** — the auto-hide path, independent of t9's replacement path | OD-2 amendment (A5) |
| **t12** | The §0.3.1 route with a **dedicated, unfiltered `pageerror` collector** | Under **OD-12(a)**: no `Cannot read properties of null (reading 'classList')`. Under **OD-12(b)**: exactly that error, **named**, as a characterization arm | F-NEW-1 |

**Every negative is paired with a positive proving the call ran** (T11) — the rule
`toast.test.js` states in its own header, applied here.

**Counts and artifacts, measured from `TEST_INVENTORY.json` at `52c44c4`** (T6):

- `toast.test.js` stays at **47**, byte-identical. Vitest corpus stays **13 files / 231 cases**.
  `tests/test_vitest_inventory_contracts.py` **not edited** — its `231` / `13` / `47` literals hold.
- **These artifact values DO move** and must be regenerated in the same commit:
  `playwright.total_tests` **662 → 674**, `specs[volume-splitter.spec.ts].tests` **46 → 58**,
  `required_functional_set.tests` **527 → 539**, and `hard_waits.total_lines` (**82** today) if any
  wait is added. **`required_functional_set.spec_files` stays 25.**
- **The pin is `tests/test_playwright_shard_launcher_contracts.py:67`** —
  `assert len(set(ci_required_specs())) == 25`, which counts **specs** and is untouched because no
  spec is added. **`ci.yml:1173` is not a pin**; it is a job-summary print.
- **F-NEW-1 is invisible to the shared fixture, not blocked by it** (T3): `e2e/fixtures.ts:42` drops
  `'Global error caught'`; `:61-62` drops `'classList'` and `'Cannot read properties of null'`.
  Arm **t12** exists because of that — the shared collector **cannot** serve as F-NEW-1's oracle in
  either OD-12 direction.

### 4.5 Verification gates

Supersedes §2.5.

| Gate | Pass condition |
|---|---|
| **Full pytest** | green; the three Vitest literals unchanged |
| **`npx tsc --noEmit`** | **zero errors.** `tsconfig.json:13` includes `e2e/**/*.ts`; the `tsc` half of `Type Check` is required and blocking (T7). pyright is out — no `.py` in the diff |
| **Full Chromium E2E** | the two-invocation comparison below |
| **`scripts/generate_test_inventory.py --check`** | regenerated in the same commit; exits 0 |
| **`npm run test:js`** | 13 files / 231 cases; `toast.test.js` byte-identical |
| **Window rule, measured directly and AFTER the squash** (T5) | `git rev-parse <merge-base>:static/js/modules/__tests__` == the post-merge `main` value; `git hash-object vitest.config.js` equal on both; the three literals at `tests/test_vitest_inventory_contracts.py:57,58,67` unchanged. **Counts are downstream of the tree and are not evidence for it** |
| **Visual specs** | no new baseline; **oracle: `git status --porcelain` clean under `e2e/**-snapshots/`**. A visual red is REAL and is never repaired with `emit_baseline` |
| **Manual smoke** | the §0.3.1 route by hand, plus one toast on a second page |
| **`/verify-suite`** | green. **Packet B's no-`/verify-suite` override does not transfer** — it was argued for a docs-and-tests-only diff |

**The two-invocation comparison, made executable** (T8). The default E2E invocation is **not**
clean, and the 569/63/17 figures quoted in §2.5 are **stale** — they sum to 649, while
`playwright.total_tests` is **662** today. **Re-derive every count from `TEST_INVENTORY.json` at
implementation time, and split by spec glob, never by count.**

1. Run branch and merge-base on the same machine, same session, `--reporter=json` to
   `artifacts/e2e-branch.json` and `artifacts/e2e-base.json`.
2. Reduce each to the set of `(file, title)` with a non-passing outcome.
3. **Pass condition: `branch_failures \ base_failures` is empty**, and the new arms appear in
   neither set.
4. **Any element of that difference is stash-and-re-run on the identical batch before it is
   attributed to the diff** — ad-hoc batches are nondeterministic.
5. Visual half: same procedure; plus the `git status --porcelain` oracle above.

Verification runs on a base **rebased onto live `main`**.

### 4.6 Migration notes

Supersedes §2.6. Items 1–5 and 7 stand as written there, with note 5's correction already applied.
Replacing items 6 and 8, and adding 9–11:

6. **`volume-splitter.js` gains `ourMessageStands()` and imports `toastMessageText()` from
   `toast.js`. `ourToastContentStands()` is NOT renamed** and keeps a live caller in the narrowed
   dismiss guard. OD-2 is **re-signed** with the two substitutions marked in §4.3.
8. **`UI_SCENARIOS_GAP_ANALYSIS.md`'s KI-011 row flips to Mitigated**, linking `t1`, `t2`, `t8`.
   **In the same commit:** correct the **KI-012** row's OD-2 restatement at `:107`, which this diff
   falsifies (P5); and **under OD-12(b), file KI-013** for the dispose-race `TypeError`, with the
   KI-011 Mitigated note naming it and the allow-listed message string (P8).
9. **`volume_failure_feedback/PLANNING.md` §v2.14 (U1-FOLLOWUP-1) goes STALE** — it names
   `ourToastContentStands()` and the exact condition `forceAnnounce || !standing ||
   !ourToastContentStands()`, and the condition changes. **Recorded as K13, not repaired by U3b**:
   U1's planning document is not U3b's to edit. Whoever discharges U1-FOLLOWUP-1 re-reads it first.
10. **`STEP12_JS_UNIT_GATE0.md` §10.7-R10 remains stale** (K10) and is still not repaired here.
11. **The implementation PR owes ledger row N in `STEP12_JS_UNIT_GATE0.md` §13.0** (T10), read at
    **job level** — the `js-unit` job's `conclusion` and `completed_at`, **never** the run's overall
    conclusion — and must prove what landed **by blob SHA**. **A `js-unit` red on that `main` run
    resets T0 to zero and voids OQ-10's premise**, which is the single largest schedule risk in the
    packet.

### 4.7 Mutation obligations carried into implementation

- Run **N1–N9** both directions, against a copy under `artifacts/probe/`, with the production blob
  asserted before, between and after every row.
- **N9** (drop the `ourMessageStands()` conjunct from the dismiss guard) is **new and not yet run** —
  it needs `volume-splitter.js` intercepted the same way `toast.js` is. **Running it both directions
  is a Gate 1 exit condition** (T4).
- **N8 currently SURVIVES and must be re-run if OD-12 resolves to (a).** With the dispose race
  fixed, the stale `hidden.bs.toast` fires and the generation check becomes load-bearing; **N8 must
  then be KILLED by `k11`**. If it still survives, the generation check is genuinely dead and should
  be removed rather than shipped as unexercised code.
- Re-run the **timing-shaped rows** (`N3`, `N4`, `N7`) at **n ≥ 3** and record the count (T14).
- `ERROR` on either leg is **BAD ROW**, never a kill.

### 4.8 Sequencing, ownership and rebase

§2.7 stands, plus:

- **Claim the implementation path set before writing any code** (A8), in
  `WORKSTREAM_OWNERSHIP.local.md`: `static/js/modules/toast.js`,
  `static/js/modules/volume-splitter.js`, `e2e/volume-splitter.spec.ts`,
  `docs/test_inventory/**`, `docs/UI_SCENARIOS_GAP_ANALYSIS.md`,
  `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` (for the §13.0 row), and
  `docs/toast_action_continuity/**`. Three of those are other packets' surfaces.
- **U3a inherits two hard constraints**, not one: `toast.js` must still hold **no module-level
  mutable state** (§2.1e), and `span.toast-message` must keep its name or `toastMessageText()` must
  be updated with it (A4).

### 4.9 Owner decisions outstanding — the Gate 1 boundary

| ID | Decision | Status |
|---|---|---|
| **OD-11** | `OQ-6(i)` offered *"**Inside `#toast-body`** (needs `:60` to become selective) **or** in a sibling action slot inside `#liveToast`"*, and the ruling used **the second phrase**. Plan v2's slot is a child of **`#toast-body`** — the **first** branch. And the recommendation the owner signed argued for relocation because *"the clear stays unconditional and total, which keeps `I2`, `I4` and B26 trivially true"* — **§4.2(C) discards exactly that**, replacing the clear with a targeted `textContent` write. | **OPEN.** §4.2(B)/(C) are **provisional**. Measured basis: the alternative reading reds `e2e/volume-splitter.spec.ts:340` (mutation **N6**, killed by `k6`), because `expectToast` scopes to `#toast-body`. A plan may not narrow a signed criterion, so this is confirmed, not assumed |
| **OD-12** | **F-NEW-1**, the dispose-mid-transition `TypeError`. **(a)** fix it here, with arm `t12` as an unfiltered oracle and a new mutation row; or **(b)** file **KI-013** and ship a **named** characterization arm. | **OPEN, and it is now a correctness dependency, not only scope.** The shared fixture is **blind** to F-NEW-1 (T3), so (b) is already the silent status quo and (a) would otherwise ship unverified. **N8's verdict depends on this row** (§4.7) |
| **OD-13** | The atomic-announcement exclusion. `aria-live="off"` **does not** deliver it (P3). The real binary: **accept that every later message is announced as "&lt;new message&gt; &lt;action label&gt;"** while an action stands, **or** change the **container's** `aria-atomic` at `base.html:238` **and** `e2e/ui-hardening.spec.ts:361-363`, which pins it to `'true'`. | **OPEN.** `OQ-6(ii)` as signed cannot be delivered by the slot attribute alone |
| **OD-14** | `OQ-2`'s ruling word *"Preserves"* is common to option **(a)** bare-preserve and option **(c)** preserve-with-standing-context. §4.2(D) implements (a). `OQ-2`'s own text says the pairing risk *"must be accepted explicitly, not hand-waved."* | **OPEN.** Reachable pairings on `/volume_splitter`, all inside A1's 6000 ms window: `Failed to load saved volume plans. Please try again.` + `Activate for Plan tab` (the very route this packet fixes), plus the delete (`:382`, `:388`), export (`:599`), calculate (`:184`) and either `fetch-wrapper.js` site (`:213`, `:246`). Sub-case in the same row: **a caller whose own action is malformed inherits an unrelated one** — no live caller does this, but §4.2(D) writes the rule for all 112 |

---

## 5. Gate 1 checklist and STOP

**Ready, and evidenced:** the browser reproduction with its pre-fix prediction recorded; the
contained byte-identity-guarded matrix at **8 rows / 11 arms**, both directions, **7 KILLED and one
honestly-reported conditional survivor**; the 47-case contract green against the design without
touching the file; the design; the E2E-only regression plan with its measured artifact deltas; the
full gate set including the two gates Plan v1 omitted; the council, this response matrix, and Plan
v2; migration notes and sequencing.

**Not ready, and blocking Gate 1 signature:**

1. **OD-11, OD-12, OD-13 and OD-14 are unanswered.** OD-12 gates **N8**; OD-11 makes §4.2(B)/(C)
   provisional; OD-13 is an accessibility contract `OQ-6(ii)` cannot deliver as signed; OD-14 is an
   acceptance `OQ-2`'s own text requires be explicit.
2. **N9 has not been run.** The narrowed dismiss guard is the one §4.3 edit with no evidence.

**STOP — Gate 1 owner-signature boundary.**

- No production line changed. `static/js/modules/toast.js` is blob
  `42863b4664b7f87a2519556b7f9db8af2cb36e64`; `toast.test.js` and `volume-splitter.js` are
  untouched.
- No test file created or modified. The suite is **13 files / 231 cases**, re-measured green.
- No inventory artifact, ledger row, status document, repository setting, or U1 / U2 / U3a artifact
  touched. `generate_test_inventory.py --check` exits 0.
- The entire harness lives in the gitignored `artifacts/probe/` and is **not** in the PR.
- **KI-011 implementation is not authorized, must not begin, and must not run concurrently with
  KI-010 implementation. PR #426 stays draft.**
