# Plan Review — Packet U2: Backup "save first" confirmation continuity

**Packet**: U2, from [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4 ([`:152-181`](../OPEN_WORK_EXECUTION_PLAN.md#L152-L181))
**Priority**: P1 · **Status**: **Gate 1 SIGNED — 2026-08-26.** Plan v2 is an approved plan; the owner's four decisions are recorded in §v2.1 and restated in *Sign-off*. **Implementation becomes authorized only after this signed planning PR merges** — signing alone authorizes nothing.
**Base**: `origin/main` at **`06a3f419fd658403b2659ac2e2053d332254b3e2`** (PR #423, Packet U1 implementation), **plus this PR's own two edits** — this document and the [`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md) ledger row 12 recorded in the *Operational rider* below. Every line citation in §0 was read from the **base commit's** content of the file it cites; the ledger file is the one exception and is treated separately.
**Branch**: `docs/u2-gate1-plan`

> **Reading order.** §0 is the measured substrate and is **maintained**: where the council falsified a
> §0 statement, it is corrected **in place** and marked `⚠️ CORRECTED`, because every later section
> reads from it and a stale substrate propagates. **Plan v1 is frozen** exactly as the three reviewers
> saw it — including its errors — because a response matrix that answers a rewritten plan proves
> nothing. **Plan v2 governs.**

> **This document changes no code.** It is a planning artifact. No production file, no test file
> and no configuration file is changed by the PR that carries it — and the Gate 1 signature below
> did not change that. **Gate 1 is now SIGNED**, so this document records an approved plan rather
> than a candidate; but **the signature is not the authorization, the merge is.** Implementation
> begins only once this planning PR is on `main`.

> **Gate 0 is deliberately absent, by owner authorization.** The owner authorized this packet as
> "Gate 1 planning only" and stated that "U2 requires no separate Gate 0". §0 below therefore carries
> the requirements brief inline rather than as a separately-signed gate. **That waiver is specific to
> U2's own requirements.** It does **not** automatically dispose of every other
> gate this packet touches; §0.4 records one such collision — owner ruling **Q3** — which the owner
> may grant or overrule, and which **§v2.1 OD-1** put to them. **Settled at Gate 1: the owner chose
> OD-1 (i), E2E-only.** No Gate 0 was requested and none was granted, so Q3 is neither crossed nor
> spent, and its recorded gap stays recorded.

---

## Section 0 — Requirements brief

### 0.0 The requirement, as given

The owner stated the packet in five clauses, reproduced here as the owner worded them in the
authorization. ⚠️ **CORRECTED (architecture N6, product-risk NIT).** Plan v1 called these "verbatim"
and they are the *owner's* wording, not the *document's*. [`OPEN_WORK_EXECUTION_PLAN.md:162-180`](../OPEN_WORK_EXECUTION_PLAN.md#L162-L180)
words two of them differently, and one difference is load-bearing:

- The document says *"Detail rendering calls `clearPendingAction()`"*; clause 2 below names `renderBackupDetails()`. Same mechanism, and §0.1 measures it.
- The document says *"Changing **selection**"*; clause 4 below says "changing the selected backup". **This matters**: §0.3 measures three clearing paths — sort, filter and search — in which the selection does **not** change and which neither wording covers. U2 preserves them anyway. **U2 preserves more than clause 4 asks for, deliberately**, and §v2.4 says so rather than letting it look like clause 4's scope.
- The document says those flows' *"tests remain green"*; clause 5 below says their *behavior* must be unchanged. That is a deliberate strengthening — a green test suite is not proof of unchanged behavior when the suite is blind to the behavior (§0.5 measures exactly that blindness). U2 holds itself to the stronger reading.

1. During restore confirmation, "Save current plan first" refreshes the backup center.
2. `renderBackupDetails()` reaches `clearPendingAction()`, destroying the pending restore intent.
3. The repaired flow must let the user continue the same restore after the save-first snapshot succeeds.
4. Changing the selected backup or cancelling must still clear the pending action.
5. Existing backup create, restore, delete, and erase-flow behavior — especially
   `showAutoBackupBanner()` — must remain unchanged.

Clauses 1 and 2 are **claims about current code**. §0.1 and §0.2 measure them rather than assume
them. Clauses 3, 4 and 5 are **acceptance criteria**; **§v2.4** turns them into enumerated state
transitions and **§v2.8** into arms.

### 0.1 Measured substrate

Every line number in this document was read from the working tree at
`06a3f419fd658403b2659ac2e2053d332254b3e2`. [`backup-center.js`](../../static/js/modules/backup-center.js)
is **1069** lines with **one** export, `initializeBackupCenter()` at
[`:923`](../../static/js/modules/backup-center.js#L923), and **eight** module-level mutable
variables at [`:12-19`](../../static/js/modules/backup-center.js#L12-L19).

**The pending-action state machine.** One module variable, `pendingAction`
([`:16`](../../static/js/modules/backup-center.js#L16)), holds `null`, `'restore'` or `'delete'`.

| Symbol | Lines | Role |
|---|---|---|
| `showPendingAction(type)` | [`:706-741`](../../static/js/modules/backup-center.js#L706-L741) | The **sole** writer of a non-null `pendingAction` ([`:709`](../../static/js/modules/backup-center.js#L709)). Builds the whole confirm UI: title, text, confirm-button class and label, and the save-first button's visibility, `disabled` and label ([`:720-729`](../../static/js/modules/backup-center.js#L720-L729) for `restore`). Reveals the panel at [`:740`](../../static/js/modules/backup-center.js#L740). Guarded by `if (!selectedBackupDetails) return;` at [`:707`](../../static/js/modules/backup-center.js#L707). |
| `clearPendingAction()` | [`:148-170`](../../static/js/modules/backup-center.js#L148-L170) | The **sole** writer of `pendingAction = null` ([`:149`](../../static/js/modules/backup-center.js#L149)). Hides the panel ([`:157`](../../static/js/modules/backup-center.js#L157)), resets the confirm button's `disabled`, `className` and `innerHTML` ([`:158-162`](../../static/js/modules/backup-center.js#L158-L162)), resets the save-first button's `hidden`, `disabled` and `innerHTML` ([`:163-167`](../../static/js/modules/backup-center.js#L163-L167)), and resets the title and text ([`:168-169`](../../static/js/modules/backup-center.js#L168-L169)). |
| `handleConfirmAction()` | [`:808-882`](../../static/js/modules/backup-center.js#L808-L882) | The **sole** reader that acts on it. Early-returns on `if (!pendingAction \|\| !selectedBackupDetails) return;` at [`:809`](../../static/js/modules/backup-center.js#L809). |

**The six call sites of `clearPendingAction()`, plus one direct binding.** ⚠️ **CORRECTED
(architecture N1).** Plan v1 said "five … all measured, none inferred" and omitted
[`:870`](../../static/js/modules/backup-center.js#L870). Re-derived by grepping the symbol across the
whole file rather than by reading the functions someone thought were relevant:

| # | Call site | Reached from |
|---|---|---|
| 1 | [`:538`](../../static/js/modules/backup-center.js#L538) in `renderEmptyDetail()` | no backup selected, or the list is empty |
| 2 | [`:575`](../../static/js/modules/backup-center.js#L575) in `renderDetailError()` | the detail fetch rejected |
| 3 | **[`:635`](../../static/js/modules/backup-center.js#L635)** in `renderBackupDetails()` | **every successful detail render** — this is the defect's mechanism |
| 4 | [`:860`](../../static/js/modules/backup-center.js#L860) in `handleConfirmAction()`'s **restore** branch | a restore that actually executed |
| 5 | **[`:870`](../../static/js/modules/backup-center.js#L870)** in `handleConfirmAction()`'s **delete** branch | a delete that actually executed — **the site Plan v1 missed** |
| 6 | [`:891`](../../static/js/modules/backup-center.js#L891) in `handleListClick()` | the user clicks a *different* record in the library list |
| — | [`:1059`](../../static/js/modules/backup-center.js#L1059) — `cancelBtn.addEventListener('click', clearPendingAction)` | a **direct binding**, not a call in source; the Cancel button |

**The fourth terminal state of the refresh, which Plan v1 did not model.** ⚠️ **ADDED (architecture
B2, measured in §0.7).** `loadBackupDetails()` carries a stale-response guard:

```js
const requestId = ++detailRequestSequence;             // :649
const details = await fetchBackupDetails(...);         // :652
if (requestId !== detailRequestSequence) { return; }   // :653-655  ← returns WITHOUT assigning
selectedBackupDetails = details;                       // :657
renderBackupDetails(details);                          // :658
```

Every non-save-first caller invokes `loadBackupDetails()` **without awaiting it** — sort
[`:993`](../../static/js/modules/backup-center.js#L993), search
[`:967`](../../static/js/modules/backup-center.js#L967), filter
[`:917`](../../static/js/modules/backup-center.js#L917), list click
[`:892`](../../static/js/modules/backup-center.js#L892). Any of them firing mid-flight starts request
N+1 and strands request N, which then returns at `:654` **without assigning `selectedBackupDetails`
and without calling `renderBackupDetails()`**. `refreshBackupCenter()`'s `await` at
[`:696`](../../static/js/modules/backup-center.js#L696) resolves regardless. **So "the refresh
resolved" does not imply "the detail render ran", and `selectedBackupDetails` may still hold the
pre-refresh object.** Note also that `loadBackupDetails()` assigns `selectedBackupId`
**synchronously** at [`:645`](../../static/js/modules/backup-center.js#L645) while
`selectedBackupDetails` is only assigned at `:657` — the two module variables **diverge** for the
duration of a fetch. §0.7 measures that divergence on the live page.

**The save-first handler**, an anonymous `async` listener registered inside
`initializeBackupCenter()` at [`:1022-1051`](../../static/js/modules/backup-center.js#L1022-L1051) (the enclosing `if (saveFirstBtn) {` block runs `:1021-1052`).
It has no name, which is itself relevant to §v2.3:

| Step | Line | What it does |
|---|---|---|
| guard | [`:1023`](../../static/js/modules/backup-center.js#L1023) | `if (!selectedBackupDetails) return;` — note it does **not** check `pendingAction === 'restore'` |
| lock | [`:1029-1034`](../../static/js/modules/backup-center.js#L1029-L1034) | disables both buttons, swaps both labels to spinners |
| act | [`:1038`](../../static/js/modules/backup-center.js#L1038) | `await createBackup('Pre-restore snapshot (<stamp>)', 'Automatic snapshot taken before restore')` |
| tell | [`:1039`](../../static/js/modules/backup-center.js#L1039) | `showToast('success', 'Current plan saved as "…".')` |
| refresh | [`:1040-1041`](../../static/js/modules/backup-center.js#L1040-L1041) | captures `preferredSelectionId = selectedBackupDetails.id`, then `await refreshBackupCenter({ preserveSelection: true, preferredSelectionId })` |
| fail | [`:1042-1050`](../../static/js/modules/backup-center.js#L1042-L1050) ⚠️ **CORRECTED (A-NIT)** | on error: toast, then **restore both buttons by hand** |

**There is no `finally`.** On the **success** path nothing in the handler re-enables the two buttons
or restores their labels. That work is done, incidentally, by `clearPendingAction()` at
[`:159`](../../static/js/modules/backup-center.js#L159) and
[`:165-166`](../../static/js/modules/backup-center.js#L165-L166) — reached through the very
`renderBackupDetails()` call that constitutes the defect. **The bug and the button reset are the same
line.** Any fix that stops `:635` from running on this path must take over that reset, or it trades a
vanished panel for two permanently-disabled buttons showing "Saving…" and "Working…". **§v2.3** treats
this as the design's primary hazard, and arm `u1` asserts it (T-NB7).

**The refresh chain**, which is what carries `:635` into the save-first path:

```
save-first listener :1041
  └─ refreshBackupCenter({preserveSelection:true, preferredSelectionId}) :669-704
       ├─ renderLibraryState('… Loading backups…')                      :675
       ├─ backupsCache = await fetchBackups()                            :678
       ├─ selection resolution — preferred id wins when still available  :685-691
       ├─ renderBackupList()                                             :693
       └─ await loadBackupDetails(selectedBackupId)                      :696
            ├─ renderDetailLoading()                                     :647
            ├─ details = await fetchBackupDetails(id)                    :652
            ├─ selectedBackupDetails = details                           :657
            └─ renderBackupDetails(details)                              :658
                 ├─ … repaints the detail pane …
                 ├─ clearPendingAction()                                 :635   ← DESTROYS THE INTENT
                 └─ clearRestoreResultPanel()                            :636
```

**Two network round trips** sit between `:1041` and `:635` — `GET /api/backups`
([`program-backup.js:12`](../../static/js/modules/program-backup.js#L12)) and
`GET /api/backups/<id>` ([`program-backup.js:27`](../../static/js/modules/program-backup.js#L27)).
> ⚠️ **CORRECTED (product-risk B-2, measured in §0.7).** Plan v1 continued here: *"That matters for
> §v1.4: the teardown is not instantaneous, so whatever replaces it is not instantaneous either"*,
> and §v1.4 built on it by placing the two round trips **between** the teardown and the re-assert.
> **That ordering is wrong.** Both GETs complete **before** `:635` — the teardown is the *last* thing
> the refresh does. Between `:635` and where a re-assert would run there is **no network at all**,
> only two `await` resumptions on already-settled promises. §0.7 measures this. The consequence is
> that **OD-2's "blink" is not a real cost**, and Plan v2 retires that decision.

**The template**, [`backup.html`](../../templates/backup.html) — the confirm panel is static markup,
not generated:

| Element | Line |
|---|---|
| `#backup-action-confirm` (the panel, `hidden` in source) | [`:187`](../../templates/backup.html#L187) |
| `#backup-action-title` | [`:189`](../../templates/backup.html#L189) |
| `#backup-action-text` | [`:190`](../../templates/backup.html#L190) |
| `#backup-restore-save-first` (`hidden` in source) | [`:193`](../../templates/backup.html#L193) |
| `#backup-action-cancel` | [`:196`](../../templates/backup.html#L196) |
| `#backup-action-confirm-btn` | [`:197`](../../templates/backup.html#L197) |
| `#backup-restore-result` (`role="status"`) | [`:201`](../../templates/backup.html#L201) |

**The confirm panel has no live-region role and no `aria-live`.** `#backup-restore-result` at
[`:201`](../../templates/backup.html#L201) carries `role="status"`; `#backup-action-confirm` at
[`:187`](../../templates/backup.html#L187) carries none, and neither does `#backup-action-title`. A
sighted user sees the panel appear; a screen-reader user is told nothing. That is **true today, before
U2**. ⚠️ **CORRECTED (P-B3).** Plan v1 recorded this as pre-existing and declined to touch it. **That disposition was withdrawn**: U2 turns an un-announced *disarmed* state into an un-announced *armed destructive* one, which is not the same risk, and the repair costs **no template edit** — `showPendingAction()` can set the attribute from JS. **§v2.1 OD-6** put it to the owner. **Settled at Gate 1: OD-6 (a) — announce, and place focus on Cancel.**

### 0.2 Reproduction — measured live, not derived from the source

The defect was reproduced against a server launched from **this worktree** at `06a3f41`, port 5050,
`FLASK_DEBUG=0`, reloader off, on the worktree's own isolated `data/database.db` seeded from the
visual fixture.

**Provenance of the server was proven, not assumed.** `backup-center.js` is byte-identical between
this worktree and the shared `main` checkout, so its digest cannot discriminate between them. The
discriminating asset is `volume-splitter.js`, which PR #423 changed and the shared checkout (at
`5111a7f`) predates: the served copy digests **`b867416934b899b24a0c6acfce03c262`**, matching this
worktree, and **not** `64562fc2587019777269a41e0c8034e9`, the shared checkout's. Port 5050's listener
was confirmed to be a `python.exe` process. The reproduction ran against `06a3f41`.

**Steps.** Open `/backup`; select a backup; click **Restore**; click **Save current plan first**; wait
for the success toast.

**Measured state, before and after the single click.** Every field is a DOM read, not an inference:

| Property | Before the click | After the click | |
|---|---|---|---|
| `#backup-action-confirm` `.hidden` | `false` | **`true`** | ❌ panel destroyed |
| `#backup-action-title` `.textContent` | `"Confirm restore"` | **`"Confirm action"`** | ❌ reset to the idle placeholder |
| `#backup-action-text` `.textContent` | `"Restore \"Delete Test 1776469272389\"? The current workout plan and all logged sessions will be cleared."` | **`""`** | ❌ emptied |
| `#backup-action-confirm-btn` `.innerHTML` | `<i class="fas fa-undo" aria-hidden="true"></i> Confirm Restore` | **`Confirm`** | ❌ relabelled to the idle default |
| `#backup-restore-save-first` `.hidden` | `false` | **`true`** | ❌ hidden |
| `#backup-restore-save-first` `.disabled` | `false` | `false` | reset by `:165` |
| `#backup-action-confirm-btn` `.disabled` | `false` | `false` | reset by `:159` |
| `#backup-detail-name` `.textContent` | `"Delete Test 1776469272389"` | `"Delete Test 1776469272389"` | ✅ **unchanged** |
| selected record `data-backup-id` | `"4"` | `"4"` | ✅ **unchanged** |
| record count in the list | `4` | **`5`** | ✅ the snapshot **was** created |
| toast | — | `Current plan saved as "Pre-restore snapshot (2026-08-26 12:08:08)".` | ✅ the save succeeded |

Console errors across the whole session: **0** of 10 messages were errors or warnings.

**Two readings follow from that table, and both shape the fix.**

1. **The selection survives; only the *intent* dies.** `preferredSelectionId` at
   [`:1040`](../../static/js/modules/backup-center.js#L1040) does its job — the same backup is still
   selected and its details are still on screen. The user has lost the *confirmation*, not the
   *target*. A fix does not need to re-find anything; it needs to re-assert one enum and one panel.
2. **The two buttons come back enabled and correctly labelled**, and the only thing that did that is
   `clearPendingAction()`. This is the hazard §0.1 named, now measured on the live page rather than
   argued from the source.

### 0.3 The five clearing paths that must **survive** — measured, and three of them are load-bearing on `:635`

Clause 4 says "changing the selected backup or cancelling must still clear the pending action". The
naive fix — delete or neuter `:635` — would satisfy clause 3 and break clause 4. **That is measured,
not predicted.** Each of the following was driven on the live page with a restore confirmation
already open:

| Arm | Action taken with a restore pending | `#backup-action-confirm.hidden` after | Selected id after | Cleared by |
|---|---|---|---|---|
| **A** | Click `#backup-action-cancel` | `true` ✅ | `4` (unchanged) | [`:1059`](../../static/js/modules/backup-center.js#L1059) → `clearPendingAction` **directly** |
| **B** | Click a *different* record in the list | `true` ✅ | `4` → `5` | [`:891`](../../static/js/modules/backup-center.js#L891) **directly**, *and* `:635` afterwards |
| **C** | Change `#backup-sort` from `newest` to `name-asc` | `true` ✅ | `5` (**unchanged**) | **`:635` only** |
| **D** | Click the `manual` filter button | `true` ✅ | `5` (**unchanged**) | **`:635` only** |
| **E** | Type in `#backup-search` | `true` ✅ | `5` (**unchanged**) | **`:635` only** |

The sort handler ([`:982-999`](../../static/js/modules/backup-center.js#L982-L999)),
`handleFilterClick()` ([`:895-921`](../../static/js/modules/backup-center.js#L895-L921)) and the
search handler ([`:957-972`](../../static/js/modules/backup-center.js#L957-L972)) **do not call
`clearPendingAction()` themselves**. Arms C, D and E clear only because they route through
`loadBackupDetails()` → `renderBackupDetails()` → `:635`. In all three the selection did not even
change, so no identity check would have saved them.

**Therefore: `:635` is load-bearing for three measured behaviors and must keep firing.** A fix that
removes it, or makes it conditional on a flag that C/D/E do not set, silently regresses three paths
that no current test covers. **§v2.2** chooses the design on this basis, and **§v2.9's M7** is the mutation that proves it.

### 0.4 The collision the Gate 0 waiver does not automatically dispose of — owner ruling Q3

[`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md) §2.4
([`:491-513`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L491-L513)) records an owner ruling dated
2026-08-15 whose subject is **this exact module**:

> **CLOSED UNSTARTED.** `backup-center.js` is **not** covered by step 12. No test file for it may be
> written under this packet, and its 0 % coverage is an **accepted, recorded** gap for the duration
> of step 12 — not an oversight to quietly close later.

and, at [`:512-513`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L512-L513):

> Reviving this needs its **own** Gate 0 and its own plan — it is not a follow-up any step-12 packet
> may absorb, and Packets A–C must not grow a `backup-center` test “while they are in there”.

Two clauses of that ruling reach U2, and they reach it differently:

- **The Vitest prohibition binds U2's *test* tier.** Q3's "no test file for it may be written" is
  scoped to step 12, and U2 is authorized by a different document. But the sentence that follows —
  *"reviving this needs its own Gate 0"* — is not step-12-scoped; it is a statement about what
  authorizing `backup-center.js` unit coverage requires. ⚠️ **CORRECTED (A-N5).** Plan v1 argued here that *because* U2 has no Gate 0, U2 therefore **cannot** be the vehicle that revives `backup-center.js` unit coverage. **That syllogism does not hold.** [`OPEN_WORK_EXECUTION_PLAN.md:158-160`](../OPEN_WORK_EXECUTION_PLAN.md#L158-L160) says U2's *requirements* are settled — a statement about what U2 need not re-derive, not a rule about what U2 may do. **The owner can simply grant the Gate 0 Q3 asks for.** Q3's substantive point still stands on its own (unit-testing this module at its single export means standing up the whole Backup Center DOM), but the **decisive** obstacle is the live qualification window, not Q3. **§v2.1 OD-1** is restructured accordingly. **Settled at Gate 1: OD-1 (i)** — the owner neither requested nor granted the Gate 0 this paragraph shows they *could* have.
- **The seam-extraction prohibition is *not* binding on U2, and must not be mistaken for a licence.**
  Q3 says extracting "`detailRequestSequence` and the `pendingAction` state machine into seams" is a
  production change "outside step 12's test-only scope", and that "the owner ruled that extraction out
  of scope". That ruling disposes of the extraction **as a step-12 activity**. U2 is a production
  packet, so the scope argument does not transfer — but neither does an authorization. Plan v1 does
  **not** propose the extraction, and **§v2.2** chooses a design specifically so the question does not
  arise. If a reviewer or the owner wants the extraction, it is **OD-4**, not an implementation detail.

Q3 also records a consequence that is now doubly relevant:

> The module keeps its existing coverage: one E2E spec (`program-backup.spec.ts`) and nothing at unit
> level. That spec is now the **sole** guard on the stale-response race guard and the confirm/cancel
> state machine.

§0.5 measures how good that sole guard actually is on U2's specific behavior. The answer is: it is
blind to it.

### 0.5 The existing E2E coverage is blind to this defect — measured

[`e2e/program-backup.spec.ts`](../../e2e/program-backup.spec.ts) carries **22** tests. Three assert on the
confirm panel's *visibility*; four more (`:158`, `:193`, `:231`, `:280`) click its confirm button
without asserting the panel's own state. One names save-first directly:

- [`:91-118`](../../e2e/program-backup.spec.ts#L91-L118) — `restore and delete actions use inline confirmation on the detail pane`. Asserts the panel opens for restore, closes on cancel, and opens for delete. **Covers arm A.** Untouched by U2.
- [`:120-137`](../../e2e/program-backup.spec.ts#L120-L137) — `restore confirmation mentions logged sessions and offers a save-first snapshot`. Asserts the copy and that the save-first button is visible. It then **cancels**; it never clicks save-first. Untouched by U2.
- **[`:139-156`](../../e2e/program-backup.spec.ts#L139-L156)** — `save-first snapshot creates a pre-restore backup before restore`. This is the one that matters.

Its last three lines are:

```ts
await page.locator('#backup-search').fill('Pre-restore snapshot');   // :153
await expect(page.locator('#backup-center-list')).toContainText('Pre-restore snapshot');
await expect(page.locator('#backup-action-confirm')).not.toBeVisible();   // :155
```

**Line `:155` looks like it pins the defect. It does not — on today's code it is an oracle that
cannot fail.** That conclusion survived all three reviews. **The mechanism Plan v1 gave for it did
not.**

> ⚠️ **CORRECTED (all three reviewers, independently).** Plan v1 attributed `:155`'s non-failure to
> §0.3 arm **E** — "a search input clears **even when the selection does not change**". In *this*
> test the selection **does** change: `:153` fills `Pre-restore snapshot`, which excludes the
> `Save First E2E …` backup from the visible list, so the search handler's
> [`:960-961`](../../static/js/modules/backup-center.js#L960-L961) branch reassigns
> `selectedBackupId`. `:155` is **over-determined**, not arm-E-determined. The conclusion holds; the
> reasoning was wrong.

> ⚠️ **CORRECTED, and this one reverses a consequence (test-strategist B-2).** Plan v1 concluded
> *"U2's fix does not red `:155`"*. **On repaired code `:155` becomes bistable, not stable-green.**
> The race: `:152`'s `expectToast` returns at
> [`:1039`](../../static/js/modules/backup-center.js#L1039), **before `refreshBackupCenter()` is even
> entered** (§0.1's step table). `:153`'s fill therefore lands while the refresh is still in flight.
> If it lands before the refresh reaches its selection resolution, that resolution's
> **`else if` chain** at [`:685-691`](../../static/js/modules/backup-center.js#L685-L691) takes the
> **first** branch — `preferredSelectionId` is still available — and **discards the search's
> selection change**; `loadBackupDetails(preferred)` then bumps `detailRequestSequence` at `:649`,
> dropping the search's own detail fetch at `:653`; `:635` clears; and the re-assert lands **last**,
> leaving the panel **visible**. `:155` **reds**. If the fill lands after the refresh completes, the
> search's `loadBackupDetails` runs last and `:155` passes. **Two stable outcomes, race-selected**,
> in a spec that already carries a documented flake ([`QUALITY_GATE.md:224`](../ai_workflow/QUALITY_GATE.md)).

**The corrected consequences:**

1. **Deleting `:155` is mandatory, not tidy.** Plan v1 offered it as a preference and offered an
   "alternative if a reviewer prefers no deletion". Plan v2 removes the choice (§v2.8) and §v2.13
   requires the bistability to be **measured** before the deletion, not asserted.
2. **`:155` is a latent trap** for a future reader who takes it for a guard. Its replacement must
   assert the same claim in a state where it can actually fail.
3. **The defect has no regression pressure at all today.** Nothing in the repository fails if it is
   reintroduced — so whatever U2 ships must be a *discriminating* arm, proven so by mutation, not
   merely an arm that is green. No review disputed this, and
   test-strategist B-1 then showed Plan v1's own arms did not meet it.
### 0.6 `showAutoBackupBanner()` — the exclusion boundary is clean, and measured

Clause 5 singles it out. `showAutoBackupBanner()` is defined at
[`program-backup.js:112-140`](../../static/js/modules/program-backup.js#L112-L140), imported at
[`app.js:29`](../../static/js/app.js#L29), exposed as `window.showAutoBackupBanner` at
[`app.js:53`](../../static/js/app.js#L53), called from `welcome.js`, and covered by
[`e2e/erase-flow.spec.ts`](../../e2e/erase-flow.spec.ts).

**`backup-center.js` never references it.** A grep of the whole repository for the symbol returns no
hit inside `backup-center.js`, and the module's import block at
[`:1-10`](../../static/js/modules/backup-center.js#L1-L10) pulls **six** named functions from
`program-backup.js` — `fetchBackups`, `fetchBackupDetails`, `createBackup`, `restoreBackup`,
`deleteBackup`, `updateBackupMetadata` — and not the seventh.

The exclusion is therefore satisfied structurally rather than by care: **U2 does not edit
`program-backup.js` at all** (§*Artifacts*), so the banner cannot move. **§v2.10 step 5** still runs
`erase-flow.spec.ts` as a control, because "the file was not edited" and "the behavior did
not change" are different claims and only the second one is the requirement.

---
### 0.7 The mid-flight window — measured, and it is where Plan v1 was unsafe

All three reviewers independently reported that Plan v1's design is unsound during the save-first
flight. The claims were argued from source; the following was **measured** on the live page at
`06a3f41` with a `MutationObserver` on `#backup-action-confirm[hidden]`, a `PerformanceObserver` on
`/api/backups*`, and a `requestAnimationFrame` frame counter on one monotonic clock.

**(a) Event ordering — the refresh's network completes *before* the teardown.**

| Δt from t0 | Frame | Event |
|---:|---:|---|
| 123.7 ms | 31 | save-first clicked |
| 134.8 ms | 33 | `POST /api/backups` response (`createBackup`) |
| 141.0 ms | 35 | `GET /api/backups` response (`fetchBackups`, [`:678`](../../static/js/modules/backup-center.js#L678)) |
| 148.7 ms | 36 | `GET /api/backups/2` response (`fetchBackupDetails`, [`:652`](../../static/js/modules/backup-center.js#L652)) |
| **149.5 ms** | **36** | **`#backup-action-confirm.hidden = true`** — the [`:635`](../../static/js/modules/backup-center.js#L635) teardown |

The teardown is **last**, 0.8 ms after the final response and **in the same animation frame**. A
re-assert placed after `await refreshBackupCenter(...)` resumes in a microtask off that same frame,
so **no paint is expected between `hidden=true` and `hidden=false`**. This falsifies §v1.4 and
retires **OD-2**.

**(b) What is actually locked during the flight — two controls out of everything.** Read at
Δt = 139.5 ms, with the `POST` still in flight:

| Control | State mid-flight |
|---|---|
| `#backup-restore-save-first` | `disabled: true` ✅ |
| `#backup-action-confirm-btn` | `disabled: true` ✅ |
| **`#backup-action-cancel`** | **`disabled: false`, visible** ❌ |
| **`#backup-detail-delete`** | **`disabled: false`** ❌ |
| **`#backup-detail-restore`** | **`disabled: false`** ❌ |
| **`#backup-sort`**, **`#backup-search`** | **`disabled: false`** ❌ |
| **`#backup-center-list`** | **`style.pointerEvents` unset — fully live** ❌ |
| `#backup-action-confirm` | `hidden: false` — the panel is **on screen** for the whole flight |

**(c) The resurrection precondition — measured true.** Drove: open restore confirmation on backup
`2` → click save-first → **click Cancel 5 ms later, while the `POST` is in flight** → let the refresh
settle.

| | `#backup-action-confirm.hidden` | `#backup-detail-name` | list `.is-selected` |
|---|---|---|---|
| before save-first | `false` | `API Test Backup 1776469272329` | `2` |
| immediately after Cancel | **`true`** — Cancel works mid-flight | `API Test Backup 1776469272329` | `2` |
| after the refresh settles | `true` | **`API Test Backup 1776469272329`** | **`2`** |

**`selectedBackupDetails.id` still equals the captured id after the user cancelled.** Plan v1's
identity check (§v1.2 A, frozen) compares exactly that and nothing else, so **it would pass, and
`showPendingAction('restore')` would re-arm the confirmation the user had just dismissed** — on a
flow that deletes the plan and every logged session (§0.8). This is the measured form of the finding
all three reviewers raised.

**(d) The two selection variables diverge — measured.** Same setup, but mid-flight the user clicks a
**different** record (`4`):

| | `#backup-detail-name` (← `selectedBackupDetails`) | list `.is-selected` (← `selectedBackupId`) |
|---|---|---|
| 3 ms after the click | `API Test Backup …` (record **2**) | **`4`** |
| after everything settles | `Delete Test …` (record **4**) | `4` |

`selectedBackupId` moves **synchronously** at `:645`; `selectedBackupDetails` lags until `:657`. An
identity check reading only `selectedBackupDetails.id` compares `2 === 2` and **passes**, while the
list already shows `4` selected — so the re-asserted panel would read `Restore "API Test Backup…"`
over a list showing a different record, and confirming there restores `2`
([`:826-827`](../../static/js/modules/backup-center.js#L826-L827)). Architecture B2, measured.

### 0.8 The protective affordance is narrower than the loss it precedes — measured

Not raised in clauses 1–5, found by the product-risk review, and verified here:

| Operation | Tables touched | Source |
|---|---|---|
| `create_backup()` — what "Save current plan first" writes | reads **`user_selection` only** | [`utils/program_backup.py:201`](../../utils/program_backup.py#L201) (`FROM user_selection`); `program_backup_items` has no session columns |
| `restore_backup()` — what the restore it guards does | deletes **`workout_log`** *and* **`user_selection`** | [`:478`](../../utils/program_backup.py#L478), [`:479`](../../utils/program_backup.py#L479) |

The warning the user reads two lines above the button says *"The current workout plan **and all
logged sessions** will be cleared"* ([`:722`](../../static/js/modules/backup-center.js#L722)). The
button says *"Save current plan first"* and the toast says *"Current plan saved as …"*. **The
snapshot does not contain logged sessions; the restore deletes them.**

U2 does not create this. **U2 makes it more available**: today the affordance vanishes the instant it
is used, and U2's entire purpose is to keep it on screen afterwards. It is therefore U2's to surface,
and it is **OD-5** in Plan v2 — not the implementer's to word. **Settled at Gate 1: OD-5 (a)**, in the
owner's exact words — `Saves the current workout plan only — logged sessions are not included in this snapshot.`
## Plan v1 — FROZEN as reviewed

> **Plan v1 is left exactly as the three council reviewers saw it, errors included.** It is
> superseded by **Plan v2** and must not be read as current. Where §0 has since been corrected,
> the corrections are marked in §0 and the *Reviewer findings* section below records who found
> what. A response matrix that answers a quietly-rewritten plan proves nothing, which is why
> nothing below this line has been edited.

> **What was superseded, and why, is §v2.0's table — not restated here.** Plan v1's **§Scope** is superseded by **§v2.1a**; its five-call-site list is wrong (A-N1).


### v1.0 Owner decisions — surfaced, not decided

Four questions below are genuinely the owner's. Plan v1 makes a recommendation on each and decides
none of them. **Every artifact and gate line in this plan is written for the recommended option and
changes if the owner picks otherwise.**

---

#### OD-1 — Coverage tier: E2E-only, or a Vitest file for `backup-center.js`?

**Two independent obstacles stand in front of a Vitest file, and either alone is decisive.**

*Obstacle 1 — owner ruling Q3.* §0.4. Reviving `backup-center.js` unit coverage "needs its own Gate
0", and the owner's U2 authorization states U2 has none.

*Obstacle 2 — the live strict qualification window.*
[`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md) §6.5
([`:844-868`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L844-L868)) is running a 14-day window:
**T0 = `2026-08-22T17:59:26Z`**, strict mark **`2026-09-05T17:59:26Z`**, qualifying the suite pinned
at **13 files / 231 cases**. §13.0's live ledger stands at **12 consecutive green** `main` `js-unit`
results with zero red, zero missing, zero skipped and zero cancelled (§13.0's post-#417 block, row 12,
appended by this PR — see §*Operational rider*). The operative restart test, ratified as R13 during
U1's Gate 1, is **"changed no JS test case"**. Adding
`static/js/modules/__tests__/backup-center.test.js` changes a JS test case, engages Q2's restart
clause, discards the ~3 d 18 h already accumulated, and pushes the strict mark to roughly U2's merge
plus fourteen days — delaying **D2**. U1 declined to spend D2 on exactly this trade
([`volume_failure_feedback/PLANNING.md`](../volume_failure_feedback/PLANNING.md) §v2.1); **D2 is not
U2's to spend either.**

| Option | What U2 ships | Cost, stated honestly |
|---|---|---|
| **(i) E2E-only — RECOMMENDED** | Every arm in [`e2e/program-backup.spec.ts`](../../e2e/program-backup.spec.ts). Zero Vitest files, zero Vitest cases. | Window untouched, Q3 untouched. Cost: the `pendingAction` machine keeps 0 % unit coverage — an **already-accepted, already-recorded** gap (Q3), not a new one. Per-spec Playwright counts move, which is an ordinary inventory regeneration and reds nothing. |
| **(ii) Vitest now** | A new `backup-center.test.js`. | Restarts the window (not "arguably" — on the rule §13.0 has applied at rows 2 through 12), delays D2, **and** proceeds without the Gate 0 Q3 requires. Two rulings crossed for coverage the owner has already priced and declined. |
| **(iii) Vitest deferred past the strict mark** | (i) now, plus a follow-up packet after `2026-09-05T17:59:26Z` **with its own Gate 0**. | Window untouched, Q3 honoured, coverage eventually written. Cost: a second packet and a second review cycle. Needs a tracked obligation or it is forgotten — U1's §v2.14 is the precedent. |

**Recommendation: (i).** Not (iii)-as-a-rider: U2 should not book a follow-up obligation against a
module whose unit coverage the owner has already ruled needs its own Gate 0. If the owner wants
(iii), it should be **opened as its own packet**, not attached to U2. That distinction is itself part
of the decision.

**This is a recommendation, not a decision. The owner decides.**

---

#### OD-2 — What does "continue the same restore" mean on screen?

Clause 3 says the user "must be able to continue the same restore". Three readings produce visibly
different pages, and the difference is a product decision, not an implementation detail.

| Reading | On screen after the save-first snapshot succeeds | Argument for |
|---|---|---|
| **(a) Restore the confirmation as it was — RECOMMENDED** | The panel is back, titled "Confirm restore", with the same warning copy and the same **Confirm Restore** button. The user clicks Confirm and the restore proceeds. | Literal reading of clause 3. The user's next click is the one they were already about to make. |
| **(b) Restore it, and mark the snapshot as taken** | As (a), plus the save-first button changes to a non-actionable "Saved" state (see **OD-3**). | Tells the user the protective step is done, which is the whole reason they clicked it. |
| **(c) Do not tear the panel down at all** | The panel never disappears; only the library list and the detail table repaint underneath it. | No flicker. But see §v1.2 — this reading forces the more invasive of the two designs. |

**(a) and (c) differ only in whether the panel visibly blinks.** Under the recommended design (§v1.2)
the panel is torn down and rebuilt across two network round trips, so the blink is **real and
user-visible**, not sub-perceptual. Whether that blink is acceptable, or whether it reads as "the app
lost my place and then found it again", is a judgement about the product's feel that the owner should
make with the trade-off in front of them.

**Recommendation: (a)**, on the grounds that it is the smallest change that satisfies clause 3 and the
only one that leaves all four of §0.3's surviving clear-paths structurally untouched. If the owner
finds the blink unacceptable, the answer is (c) and §v1.2 switches to Design A, which costs three
changed function signatures and takes on the §0.3 regression risk deliberately.

---

#### OD-3 — After a successful save-first, may the user save again?

Today the question cannot arise: the button is hidden by the teardown. Once the panel is restored, it
is answerable and must be answered.

| Option | Behavior | Consequence |
|---|---|---|
| **(a) Leave it enabled — RECOMMENDED for its honesty** | The user can click "Save current plan first" repeatedly. | Each click creates a *separate* `Pre-restore snapshot (<stamp>)` backup. Two clicks, two near-identical snapshots seconds apart, cluttering the library. Nothing is lost or corrupted. |
| **(b) Disable it and relabel** | e.g. `<i class="fas fa-check"></i> Current plan saved`, `disabled`. | No duplicate snapshots; clearly communicates that the protective step succeeded. Adds one new user-facing string, which is new copy the owner should approve. |
| **(c) Hide it** | Panel returns with only Cancel and Confirm Restore. | Cleanest, but silently removes an affordance the user can see one moment and not the next. |

**Recommendation: (b)** on user-experience grounds — it is the only option that answers the question
the user actually has ("did my plan get saved?") without relying on a toast that has already begun to
fade. **But (b) introduces new user-facing copy**, and this repository treats copy as an owner
decision (U1's Gate 0 did the same). **The owner decides, including the exact wording.** If the owner
picks (a), U2 ships strictly less code and this plan's artifact list does not change.

---

#### OD-4 — Is a `pendingAction` seam extraction in scope?

**Recommendation: NO, and Plan v1 does not propose one.** §0.4 explains why the question exists at
all. The recommended design (§v1.2) adds one module-private helper and one call; it does not restructure
the state machine, does not touch `detailRequestSequence`, and leaves the module at one export.

Surfaced because a reviewer may reasonably argue that the *right* fix is the extraction, and because
Q3 disposed of that extraction only in step 12's scope. **If the owner wants it, it is a different
packet with a different size class**, not a widening of U2.

---

### Scope

- **In**: the save-first click listener at [`backup-center.js:1021-1052`](../../static/js/modules/backup-center.js#L1021-L1052); **one** new module-private helper in that same file; **one** new `test.describe` block appended to [`e2e/program-backup.spec.ts`](../../e2e/program-backup.spec.ts); a repair to the non-discriminating assertion at [`:155`](../../e2e/program-backup.spec.ts#L155); a `KI-013` row in [`UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md); the row-10 residual in [`DUPLICATION_REGISTRY.md`](../DUPLICATION_REGISTRY.md); the regenerated [`docs/test_inventory/`](../test_inventory/) artifact; this planning document.
- **Out**: `clearPendingAction()` itself ([`:148-170`](../../static/js/modules/backup-center.js#L148-L170)) — **not one line changes**; its call sites at [`:538`](../../static/js/modules/backup-center.js#L538), [`:575`](../../static/js/modules/backup-center.js#L575), **[`:635`](../../static/js/modules/backup-center.js#L635)**, [`:860`](../../static/js/modules/backup-center.js#L860) and [`:891`](../../static/js/modules/backup-center.js#L891) — **none is removed, moved or made conditional**; `showPendingAction()` [`:706-741`](../../static/js/modules/backup-center.js#L706-L741); `refreshBackupCenter()` [`:669-704`](../../static/js/modules/backup-center.js#L669-L704); `loadBackupDetails()` [`:639-667`](../../static/js/modules/backup-center.js#L639-L667); `renderBackupDetails()` [`:580-637`](../../static/js/modules/backup-center.js#L580-L637); `handleConfirmAction()` [`:808-882`](../../static/js/modules/backup-center.js#L808-L882); `handleSaveSubmit()` [`:743-806`](../../static/js/modules/backup-center.js#L743-L806); the inline metadata editor [`:234-398`](../../static/js/modules/backup-center.js#L234-L398); [`program-backup.js`](../../static/js/modules/program-backup.js) and therefore `showAutoBackupBanner()`; [`templates/backup.html`](../../templates/backup.html); [`toast.js`](../../static/js/modules/toast.js); [`fetch-wrapper.js`](../../static/js/modules/fetch-wrapper.js); [`routes/program_backup.py`](../../routes/program_backup.py); [`utils/program_backup.py`](../../utils/program_backup.py); [`utils/auto_backup.py`](../../utils/auto_backup.py); the `/api/backups*` contracts, status codes and payloads; DB schema; backup `schema_version`; any `scss/**` or `static/css/**` edit; any new `.spec.ts` file and therefore any edit to [`ci.yml`](../../.github/workflows/ci.yml); branch protection.
- **Out — U1's residue, named so it cannot drift in**: U1's AA/contrast debt; U1's coverage gaps; **U1-FOLLOWUP-1** ([`volume_failure_feedback/PLANNING.md`](../volume_failure_feedback/PLANNING.md) §v2.14); **KI-010** and **KI-011** ([`UI_SCENARIOS_GAP_ANALYSIS.md:105-106`](../UI_SCENARIOS_GAP_ANALYSIS.md)); Dependabot PRs **#415** and **#416**; shared toast behavior of any kind; unrelated Backup Center cleanup.
- **Out — recorded debt owned elsewhere**: [`MASTER_HANDOVER.md`](../MASTER_HANDOVER.md); [`ACTIVE_DEVELOPMENT.md`](../ACTIVE_DEVELOPMENT.md); [`LEFTOVERS_BY_PRIORITY.md`](../LEFTOVERS_BY_PRIORITY.md); packets U3, R0–R3, V1, Track P1, Track D1.

### Artifacts

**Six changed paths** under the recommended options. The count is stated here and repeated in §v1.10's
blast-radius check.

| Path | Change | Notes |
|---|---|---|
| [`static/js/modules/backup-center.js`](../../static/js/modules/backup-center.js) | modify | The whole production change: one new module-private helper, and a rewrite of the save-first listener's success tail at [`:1036-1041`](../../static/js/modules/backup-center.js#L1036-L1041). See §v1.2. |
| [`e2e/program-backup.spec.ts`](../../e2e/program-backup.spec.ts) | modify | One `test.describe` appended (`u1`–`u6`), plus the [`:155`](../../e2e/program-backup.spec.ts#L155) repair. **Not** in `ci.yml`'s 25-spec required list at [`:341-365`](../../.github/workflows/ci.yml#L341-L365) — it runs in its own required job (§v1.9), so extending it is structurally free and does **not** approach the `== 25` pin at [`test_playwright_shard_launcher_contracts.py:67`](../../tests/test_playwright_shard_launcher_contracts.py#L67). |
| [`docs/UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md) | modify | Add row **`KI-013`** — the next id after `KI-012` at [`:107`](../UI_SCENARIOS_GAP_ANALYSIS.md#L107) — per the file's own rule at [`:109-112`](../UI_SCENARIOS_GAP_ANALYSIS.md#L109-L112). Editing an existing `docs/*.md` moves no inventory node. |
| [`docs/DUPLICATION_REGISTRY.md`](../DUPLICATION_REGISTRY.md) | modify | Row 10 ([`:49`](../DUPLICATION_REGISTRY.md#L49)) names its live residual as *"the refresh/confirm race, owned by **Packet U2**"*. Discharging the residual falsifies that row's present tense; it must be updated in the implementation PR, not left to a later reconciliation. |
| [`docs/test_inventory/TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) · [`.md`](../test_inventory/TEST_INVENTORY.md) | regenerate | Per-spec Playwright counts move. `waitForTimeout` lines must **not** move — §v1.7 forbids hard waits. Regenerate with the generator; never hand-edit. |
| [`docs/backup_confirmation_continuity/PLANNING.md`](PLANNING.md) | modify | This document. |
| [`static/js/modules/program-backup.js`](../../static/js/modules/program-backup.js) | **not modified** | §0.6. This is what makes clause 5's `showAutoBackupBanner()` guarantee structural. |
| [`templates/backup.html`](../../templates/backup.html) | **not modified** | The panel is static markup and the fix is entirely in JS state. Editing it would pull in the `templates/**` gate row and the visual matrix. |
| [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) | **not modified** | No new spec file, so the required-spec list and the `== 25` pin are untouched. |
| `static/js/modules/__tests__/backup-center.test.js` | **not created** | Listed so the omission is deliberate and visible. See **OD-1** and §0.4. |

**Effort**: **S** · **Owner**: implementation agent, after Gate 1 sign-off and after this planning PR merges · **Depends on**: **OD-1**, **OD-2**, **OD-3** answered; **OD-4** confirmed as out.

### v1.1 Design candidates — and why the obvious one is wrong

| Design | Mechanism | Verdict |
|---|---|---|
| **Design 0 — delete or guard `:635`** | Stop `renderBackupDetails()` from clearing. | **REJECTED, on measurement.** §0.3 arms **C**, **D** and **E** clear *only* through `:635`, with the selection unchanged. Removing it regresses sort, filter and search. Guarding it on a flag that only the save-first path sets is equivalent and equally wrong, because it leaves `:635` firing everywhere else — which is correct — but then also leaves the save-first path relying on nothing to reset the two spinner-locked buttons (§0.1). |
| **Design A — thread a `preservePendingAction` option** | `refreshBackupCenter(opts)` → `loadBackupDetails(id, opts)` → `renderBackupDetails(backup, opts)`; skip `:635` when set **and** the reloaded id matches. | Viable and the only way to satisfy **OD-2 (c)** (no blink). Costs three changed signatures, makes `:635` conditional — the exact thing §0.3 warns about — and forces the handler to take over the button reset that `:635` currently performs. **Not recommended** unless OD-2 selects (c). |
| **Design B — capture and re-assert — RECOMMENDED** | Before the refresh, capture `pendingAction` and the backup id it was raised against. After `refreshBackupCenter()` resolves, if the captured action was `'restore'` and the reloaded `selectedBackupDetails.id` still equals the captured id, call the **existing** `showPendingAction('restore')` again. | `:635` keeps firing on every path, so §0.3's arms C/D/E are structurally untouched. The teardown still performs the button reset, and `showPendingAction()` then rebuilds the panel from the single existing builder — no duplicated copy, no duplicated class names. **The blink is the cost**, and OD-2 prices it. |
| **Design C — skip the refresh entirely** | Do not call `refreshBackupCenter()` on save-first; splice the new backup into `backupsCache` and re-render only the list. | No blink, no teardown, smallest DOM churn. **Rejected**: it invents a second source of truth for `backupsCache` and diverges from the module's uniform "re-fetch after mutation" discipline, which every other mutating path follows ([`:798`](../../static/js/modules/backup-center.js#L798), [`:861`](../../static/js/modules/backup-center.js#L861), [`:871`](../../static/js/modules/backup-center.js#L871)). A correctness risk traded for a cosmetic gain. |

### v1.2 Exact production change — Design B

All in [`backup-center.js`](../../static/js/modules/backup-center.js). No new import: `showToast` and
`createBackup` are already imported at [`:1`](../../static/js/modules/backup-center.js#L1) and
[`:5`](../../static/js/modules/backup-center.js#L5).

**(A) One new module-private helper**, placed immediately after `showPendingAction()` at
[`:741`](../../static/js/modules/backup-center.js#L741) so the two live together:

```
function restorePendingAction(capturedType, capturedBackupId) { … }
```

- Returns immediately unless `capturedType === 'restore'`. **Delete is deliberately excluded** — the save-first button is `hidden` for `delete` ([`:735-737`](../../static/js/modules/backup-center.js#L735-L737)), so a captured `'delete'` cannot reach this path today, and re-asserting one would be inventing behavior the requirement does not ask for.
- Returns immediately unless `selectedBackupDetails` is truthy **and** `Number(selectedBackupDetails.id) === Number(capturedBackupId)`. **This identity check is the safety property**: `refreshBackupCenter()`'s selection resolution at [`:685-691`](../../static/js/modules/backup-center.js#L685-L691) can land on a *different* backup if the preferred one has vanished, and re-asserting a restore confirmation against a backup the user never confirmed would be a data-loss hazard, not a convenience.
- Otherwise calls `showPendingAction('restore')`.

**(B) The save-first listener's success tail**, currently
[`:1036-1041`](../../static/js/modules/backup-center.js#L1036-L1041), becomes:

1. Capture `const capturedAction = pendingAction;` and `const capturedBackupId = selectedBackupDetails.id;` **before** the `await createBackup(...)` at [`:1038`](../../static/js/modules/backup-center.js#L1038) — before any `await`, so no interleaved handler can move them.
2. `createBackup(...)` and `showToast(...)` unchanged.
3. `await refreshBackupCenter({ preserveSelection: true, preferredSelectionId: capturedBackupId })` — the existing call with the captured id substituted for the re-read `selectedBackupDetails.id`, which is now stale by two awaits.
4. `restorePendingAction(capturedAction, capturedBackupId);`

**(C) Nothing else changes.** The guard at [`:1023`](../../static/js/modules/backup-center.js#L1023),
the button locking at [`:1029-1034`](../../static/js/modules/backup-center.js#L1029-L1034) and the
entire `catch` at [`:1042-1049`](../../static/js/modules/backup-center.js#L1042-L1049) are untouched.

**Under OD-3 (b)** a second helper — or a parameter on the first — additionally sets the save-first
button to its `disabled`, relabelled state *after* `showPendingAction()` has rebuilt it. Order
matters: `showPendingAction()` sets `saveFirstBtn.disabled = false` at
[`:727`](../../static/js/modules/backup-center.js#L727) and rewrites its `innerHTML` at
[`:728`](../../static/js/modules/backup-center.js#L728), so any "Saved" state must be applied after,
never before.

### v1.3 State transitions, enumerated

`P` = `pendingAction`. `S` = the id in `selectedBackupDetails`. `C` = the captured pair.

| # | From | Event | To | Panel |
|---|---|---|---|---|
| 1 | `P=null` | click `#backup-detail-restore` | `P='restore'`, `S=x` | visible, "Confirm restore", save-first shown |
| 2 | `P='restore'`, `S=x` | click save-first; `createBackup` **resolves**; refresh resolves with `S=x` | `P='restore'`, `S=x` | **torn down, then rebuilt** — the repair |
| 3 | `P='restore'`, `S=x` | click save-first; `createBackup` **rejects** | `P='restore'`, `S=x` | never torn down; buttons restored by [`:1042-1049`](../../static/js/modules/backup-center.js#L1042-L1049) — **unchanged behavior** |
| 4 | `P='restore'`, `S=x` | click save-first; `createBackup` resolves; **`fetchBackups` rejects** | `P=null` | `renderEmptyDetail()` via [`:702`](../../static/js/modules/backup-center.js#L702) → `:538`. `restorePendingAction` finds `selectedBackupDetails === null` and does nothing. **Correct**: the library could not be read, so no restore may be confirmed against it. |
| 5 | `P='restore'`, `S=x` | click save-first; `createBackup` resolves; **`fetchBackupDetails` rejects** | `P=null` | `renderDetailError()` → `:575`. Identity check fails on `selectedBackupDetails === null` ([`:664`](../../static/js/modules/backup-center.js#L664)). **Correct**, same reason. |
| 6 | `P='restore'`, `S=x` | click save-first; refresh resolves but **`x` is gone**, selection falls to `y` | `P=null` | `x !== y`, so no re-assert. **Correct — this is the data-loss guard.** |
| 7 | `P='restore'` | click `#backup-action-cancel` | `P=null` | cleared via [`:1059`](../../static/js/modules/backup-center.js#L1059). **Unchanged** — §0.3 arm A. |
| 8 | `P='restore'` | click a different record | `P=null` | cleared via [`:891`](../../static/js/modules/backup-center.js#L891) **and** `:635`. **Unchanged** — arm B. |
| 9 | `P='restore'` | change sort / filter / search | `P=null` | cleared via `:635` alone. **Unchanged** — arms C, D, E. |
| 10 | `P='restore'`, panel rebuilt | click Confirm Restore | restore executes | `handleConfirmAction()` [`:809`](../../static/js/modules/backup-center.js#L809) passes because `P` is non-null again. **This is the acceptance criterion.** |
| 11 | `P='delete'` | save-first is `hidden` ([`:736`](../../static/js/modules/backup-center.js#L736)) | — | unreachable; helper returns early regardless |

### v1.4 The blink, stated honestly

Under Design B the panel is hidden by `:635` and re-shown by `restorePendingAction()`. Between those
two moments sit `GET /api/backups` and `GET /api/backups/<id>` (§0.1). **On localhost this is tens of
milliseconds; it is still a real repaint and a real disappearance.** During it the detail table also
shows "Loading backup details…" ([`:554`](../../static/js/modules/backup-center.js#L554)).

Plan v1 does **not** propose to suppress it, because suppressing it is Design A and Design A is what
OD-2 (c) buys. The plan states it here so the owner decides with it visible rather than discovering
it after implementation.

### v1.5 The `:635` non-regression proof obligation

Because Design B's entire safety argument is *"`:635` still fires everywhere"*, that claim must be
**proven, not asserted**. §v1.7 arms `u4`, `u5` and `u6` re-measure §0.3's arms C, D and E after the
change. They are not decoration: they are the only evidence that Design B did what it says.

### v1.6 Migration notes required in the implementation PR body

Per [`CLAUDE.md`](../../CLAUDE.md) §1's refactor invariant, U2 changes user-facing behavior in a core
workflow (backup/restore) and the PR body must carry:

1. **The behavior that changed**, in one sentence, with the before/after of §0.2's table.
2. **The behavior that did not change** — §0.3's five arms, `showAutoBackupBanner()`, and the four `/api/backups*` contracts.
3. **The `:155` repair**, explicitly, with §0.5's argument for why it was not a guard.
4. **Why no `.py` file and no route changed** — this is a client-state fix; the server was never involved.
5. **The `KI-013` and `DUPLICATION_REGISTRY` row-10 edits**, named as scoped and justified.
6. **The OD-1 omission**: no Vitest file, by owner decision, with the Q3 and window citations.

### v1.7 The regression arms

All in [`e2e/program-backup.spec.ts`](../../e2e/program-backup.spec.ts), appended as one
`test.describe`. **No `page.waitForTimeout` in any arm** — the inventory pins `waitForTimeout` lines
per file at 82 across 14 files ([`TEST_INVENTORY.md:21`](../test_inventory/TEST_INVENTORY.md)), and
that surface must read zero delta for this file. Wait on
`page.waitForResponse('**/api/backups')` and on `expectToast`, both already idiomatic in this spec.

| Arm | What it drives | What it asserts | Kills |
|---|---|---|---|
| **`u1`** | Restore → save-first → **assert before touching anything else** | `#backup-action-confirm` **visible**; `#backup-action-title` = `Confirm restore`; `#backup-action-text` contains `logged sessions will be cleared`; `#backup-action-confirm-btn` contains `Confirm Restore`; `#backup-detail-name` unchanged. | The defect itself. **The discriminating arm** §0.5 says does not exist today. |
| **`u2`** | `u1`, then click **Confirm Restore** | The restore executes: success toast, `#backup-restore-result` populated. | A "panel is visible but `pendingAction` is still null" fix — a cosmetic repair that leaves [`:809`](../../static/js/modules/backup-center.js#L809) early-returning. **`u1` alone cannot catch that.** |
| **`u3`** | `u1`, then click **Cancel** | Panel not visible. | A fix that restores the panel but leaves it un-cancellable. Re-proves §0.3 arm A *after* a re-assert. |
| **`u4`** | Restore pending → change `#backup-sort` | Panel not visible; selection unchanged. | Design 0 / a mis-scoped Design A. §0.3 arm C. |
| **`u5`** | Restore pending → click a filter button | Panel not visible. | §0.3 arm D. |
| **`u6`** | Restore pending → type in `#backup-search` | Panel not visible. | §0.3 arm E. **Also the arm that makes [`:155`](../../e2e/program-backup.spec.ts#L155) redundant** — `u6` asserts what `:155` appeared to assert, in a state where it can actually fail. |

**The [`:155`](../../e2e/program-backup.spec.ts#L155) repair.** Its enclosing test keeps its subject —
that save-first creates a snapshot — and `:155` is **deleted**, with `u6` carrying the search-clears
claim honestly. Deleting an assertion is a weakening unless something stronger replaces it; `u6` is
that replacement and the PR body must say so (§v1.6 item 3). **Alternative, if a reviewer prefers no
deletion**: invert `:155` to `toBeVisible()` and move it *above* the `:153` search fill. That is
equivalent to `u1` and would make `u1` redundant. Plan v1 prefers the delete-plus-`u6` form because it
leaves the existing test's subject single.

### v1.8 Mutation matrix

Green arms prove nothing without proof they can red. Each mutation is applied alone, to the
**implemented** branch, and reverted before the next.

| # | Mutation | Predicted red | Predicted green | Proves |
|---|---|---|---|---|
| **M1** | Delete the `restorePendingAction(...)` call at the end of the save-first tail | `u1`, `u2` | `u3`–`u6` | The repair is load-bearing, and `u4`–`u6` are **not** measuring it (they must not move). |
| **M2** | In `restorePendingAction`, drop the identity check — always re-assert | *(no arm)* | all | **A DELIBERATE, RECORDED GAP.** State 6 (the restore target vanishes mid-refresh) needs a second browser or a direct API delete to reach, and this spec has no such fixture. Recording an unkillable mutation is the honesty rule; claiming a kill would be false. See §v1.11. |
| **M3** | Restore `:635` to unconditional… *(no-op under Design B)* | — | — | **Not applicable.** Design B never makes `:635` conditional. Its absence from this matrix is the point: Design 0 and Design A would each need an M3, and neither is being shipped. |
| **M4** | Change the helper's guard from `'restore'` to always-true | *(no arm)* | all | Unreachable — save-first is `hidden` for `delete`. Recorded as an equivalent mutation, not a gap. |
| **M5** | Revert the `:155` deletion **and** delete `u6` | *(no arm)* | all | **Proves §0.5's central claim**: the two are not equivalent oracles, and the old one cannot fail. Run it once, as evidence for the PR body, not as a standing gate. |
| **M6** | In `handleListClick`, delete `clearPendingAction()` at [`:891`](../../static/js/modules/backup-center.js#L891) | *(expected none — `:635` still clears)* | all | **A negative control on the plan's own reasoning.** If `u5`/`u6` red here, §0.3's attribution is wrong and the design's premise must be re-derived. |

### v1.9 Gates

Derived from [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)'s change-type table, taking the
**union** over every changed path.

| Changed path | Row | Gate |
|---|---|---|
| `static/js/modules/backup-center.js` | **Frontend (JS)** ([`:30`](../ai_workflow/QUALITY_GATE.md#L30)) | matching Chromium specs + manual smoke (interactive) + **`docs/test_inventory/` regeneration** |
| `e2e/program-backup.spec.ts` | **E2E spec** | run the spec |
| `docs/*.md` ×3 | **Product docs only** | none |
| `docs/test_inventory/*` | *(the artifact itself)* | `Test Inventory Drift` |

**The union, as commands:**

1. `.venv/Scripts/python.exe scripts/generate_test_inventory.py` — regenerate and commit. Per-spec Playwright counts move; **`waitForTimeout` lines must not** (§v1.7). Verify with `--check` before pushing. **Do not regenerate while an untracked or gitignored `.md` sits in a globbed surface directory** ([`QUALITY_GATE.md:51`](../ai_workflow/QUALITY_GATE.md#L51)).
2. `npx playwright test e2e/program-backup.spec.ts --project=chromium` — the packet's own spec, and the exact command CI's **`E2E Backup (Chromium, isolated)`** job runs ([`ci.yml:465`](../../.github/workflows/ci.yml#L465)). That job is a **required** branch-protection context ([`UI_SCENARIOS_GAP_ANALYSIS.md:98`](../UI_SCENARIOS_GAP_ANALYSIS.md), KI-003).
3. `npx playwright test e2e/erase-flow.spec.ts --project=chromium` — **negative control for clause 5.** `program-backup.js` is not edited, but the requirement is about behavior, not diffs (§0.6).
4. `npx playwright test e2e/accessibility.spec.ts --project=chromium` — **run, not edited.** The Backup Center is in the axe matrix and the fix changes which elements are visible at rest. Node counts are pinned exactly ([`project_a11y_exceptions_register_arc`](../testing_phase2/PLANNING.md)); a move is a signal, not a re-baseline.
5. **Full `pytest`** — **not** required by any row above, and Plan v1 does **not** claim it. No `.py`, no template, no `ci.yml`, no `scripts/**` file is touched. Stated explicitly so a later reader does not read its absence as an oversight. `Test Inventory Drift` is the only Python-side gate in play, and step 1 owns it.
6. `npm run build:css` — **not run, and must not be.** No `scss/**` or `static/css/**` edit. Running it locally is the documented cause of the phantom-modification red.
7. **Manual smoke, interactive** — the `Frontend (JS)` row requires it and §0.2's procedure is the script. Re-run §0.2's table and §0.3's five arms by hand on the implemented branch.

**Reviewers required by the table**: none for `static/js/**`. Plan v1 nonetheless requires
`code-reviewer` and `unslop-reviewer` on the staged implementation diff, per this repository's
standing practice on packets that touch a state machine.

**Not run, and why**: `visual.spec.ts` (no CSS surface changes; the confirm panel's *visibility* moves
only mid-interaction, and the visual matrix captures rest states only); the seven-surface Stylelint
sweep; `/verify-suite` (its pytest half is not derivable from any changed path).

### v1.10 Scope containment, blast radius, rollback

**Blast radius: six paths** (§*Artifacts*), of which exactly **one** is production code and exactly
**one** is a test file. The production diff is a helper of roughly ten lines plus a four-line edit to
one listener's tail. `clearPendingAction()` and all five of its call sites are byte-identical before
and after.

**Rollback conditions — any one of these, revert the whole packet, do not patch forward:**

1. `u4`, `u5` or `u6` reds — §0.3's attribution was wrong and the design's premise is falsified.
2. `M6` reds anything — same.
3. `erase-flow.spec.ts` reds — clause 5 is broken by a mechanism nobody predicted.
4. `accessibility.spec.ts` node counts move — the fix changed the accessible tree at rest.
5. `Test Inventory Drift` reds on a surface **other than** per-spec Playwright counts — something moved that this plan did not model.
6. Any of the 22 pre-existing tests in `program-backup.spec.ts` reds other than the `:155` line this plan deliberately removes.

**Revert mechanics**: `git revert` of the single squash commit restores all six paths. There is no DB
migration, no schema change, no persisted state and no server change, so a revert is complete — the
packet leaves nothing behind that a revert cannot reach.

### v1.11 Residual risks, stated

1. **State 6 has no automated arm.** `M2` is unkillable with this spec's fixtures (§v1.8). The identity check ships correct-by-inspection and manually verified only. Closing it needs a second browser context or a direct `DELETE /api/backups/<id>` mid-flight, which is a fixture this spec does not have and which U2 is too small to justify building.
2. **The `pendingAction` machine keeps 0 % unit coverage.** By owner ruling Q3 (§0.4), pending **OD-1**.
3. **The confirm panel is not announced to assistive technology**, before or after U2 (§0.1). U2 does not make this worse — it makes the panel *reappear*, which is one more un-announced state change. Recorded, not repaired: repairing it means editing `backup.html`, which pulls in the `templates/**` row and the visual matrix, and it is not in clauses 1–5.
4. **The blink** (§v1.4), pending **OD-2**.
5. **`e2e/program-backup.spec.ts` is not in the 25-spec required functional shard.** It is guarded by its own required job, which is stronger for this packet, but a reader checking the shard list will not find it. Recorded so that absence is not mistaken for a gap.

### Sequence

1. Owner answers **OD-1**, **OD-2**, **OD-3**; confirms **OD-4** is out.
2. Plan v2 is rewritten against those answers.
3. Owner signs Gate 1; this planning PR merges.
4. Implementation on a fresh worktree based on `main` at that time.
5. Arms `u1`–`u6` written **before** the production change and observed to red (`u1`, `u2` must red; `u3`–`u6` must be green against unchanged code — they encode existing behavior).
6. Production change.
7. Mutations M1, M2, M4, M5, M6 executed and recorded with measured results, not predictions.
8. Gates §v1.9 steps 1–4 and 7.
9. `code-reviewer` + `unslop-reviewer` on the staged diff.
10. PR with the §v1.6 migration notes. **Do not merge without explicit owner confirmation.**

### Expected gates

| Gate | Expectation |
|---|---|
| `E2E Backup (Chromium, isolated)` | green, **22 → 28** tests |
| `Test Inventory Drift` | green after regeneration; `program-backup.spec.ts` row `22 → 28`, `playwright.total_tests` `662 → 668`; `hard_waits.total_lines` unchanged at **82**; `vitest.total_files`/`total_cases` unchanged at **13 / 231** |
| `E2E Erase Flow` | green, unchanged |
| `E2E Functional (Chromium)` | green, unchanged — this spec is not in that shard |
| `Type Check` | green, unchanged — no `.ts` type surface and no Python |
| `JS Unit (Vitest, non-required)` | green, **unchanged at 13 files / 231 cases** — the OD-1 evidence |

---

## Agent provenance

Three plan-stage reviewers were run **in parallel and independently** against the frozen Plan v1, per
[`/council-plan`](../../.claude/commands/council-plan.md) and
[`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)'s plan-review row. None saw another's output.

| Reviewer | Dimension | Verdict on Plan v1 |
|---|---|---|
| `architecture-reviewer` | module boundaries, state-machine correctness, coupling, signature churn, contract risk | **Needs revision** — 3 blocking, 6 non-blocking, 7 nits |
| `test-strategist` | gate derivation, arm discrimination, mutation matrix, pinned counts | **Not signable as written** — 5 blocking, 7 non-blocking, 5 nits |
| `product-risk-reviewer` | destructive-action safety, user-facing copy, local-first invariants, non-goals | **Blocking** — 4 blocking, 6 non-blocking, 3 nits |

**All three reviewers converged, independently, on the same defect**: Plan v1's Design B has no way to
see that the user revoked their intent during the save-first flight, and would re-arm a destructive
confirmation. That convergence is why it is treated as settled rather than argued.

**Every reviewer claim used below was re-verified before acceptance**, by code trace, by `gh`/`git`
measurement, or by driving the live page. Several findings were errors of fact in Plan v1 — the five-vs-six call sites, the §v1.4 ordering, the §0.5 mechanism; §0 carries the corrections. A separate list below records the claims that were checked and **held**, so they are not re-litigated.

**What the reviewers could not do:** none had a shell. The `§0.2` reproduction, the `§0.3` arms, the
`§0.7` mid-flight measurements, the `§0.8` table and the ledger-row-12 API values were measured in
this session and are cited above as measurements, not as reviewer claims. Conversely, `§0.3`'s
load-bearing claim was **independently confirmed by the architecture reviewer's code trace**, so it
does not rest on the live half alone.

---

## Reviewer findings and response matrix

Reviewer IDs: **A** = `architecture-reviewer`, **T** = `test-strategist`, **P** = `product-risk-reviewer`.
Every finding is listed. **Disposition** is one of ACCEPTED (Plan v2 changes), ACCEPTED-AS-CORRECTION
(§0 changes), PARTIALLY ACCEPTED, REJECTED (with reason), or DEFERRED-TO-OWNER.

### The convergent blocking finding

| ID | Finding | Verification | Disposition |
|---|---|---|---|
| **A-B1 · T-B4 · P-B1** | During the save-first flight only `#backup-restore-save-first` and `#backup-action-confirm-btn` are disabled ([`:1029-1034`](../../static/js/modules/backup-center.js#L1029-L1034)). Cancel, Delete, Restore, the list, sort, filter and search all stay live. Plan v1's identity check compares only `selectedBackupDetails.id`, which a mid-flight Cancel does not change — so the re-assert **resurrects a cancelled destructive confirmation**. A mid-flight *Delete* click is silently converted into a *restore* intent. | **MEASURED, §0.7(b) and §0.7(c).** Cancel is `disabled:false` and visible at Δt=139.5 ms; after a Cancel at +5 ms the detail name and selected id are **unchanged** when the refresh settles, so Plan v1's check would pass. | **ACCEPTED, in full.** Plan v1's sentence *"before any `await`, so no interleaved handler can move them"* named the hazard as the guarantee. §v2.3 replaces the identity check with an **authorization** check: a module-scoped intent-generation counter (**A-B1 option ii / P-B1 part i / T-B4 option a**) **plus** making the flight inert via the module's existing `setDetailActionDisabled()` (**A-B1 option i / P-B1 part ii**). Both, not either — see §v2.3 for why the lock alone is insufficient. New arms `u7`, `u8`; new mutations `M3`, `M4`, `M5`, `M6`. |

### `architecture-reviewer`

| ID | Finding | Verification | Disposition |
|---|---|---|---|
| **A-B2** | `await refreshBackupCenter(...)` resolving does **not** imply `renderBackupDetails()` ran: the `detailRequestSequence` guard at [`:653-655`](../../static/js/modules/backup-center.js#L653-L655) returns without assigning `selectedBackupDetails`. And `selectedBackupId` moves synchronously at `:645` while `selectedBackupDetails` lags to `:657`, so the identity check reads a stale object and passes while the list shows a different record. | **MEASURED, §0.7(d).** 3 ms after a mid-flight click on record `4`: list `.is-selected` = `4`, `#backup-detail-name` still record `2`. Exactly as predicted. | **ACCEPTED.** §0.1 gains the fourth terminal state. §v2.3's guard checks the generation counter **and** both selection variables. §v2.4 gains the state row. §v1.11's "correct-by-inspection" claim is withdrawn. |
| **A-B3** | The Artifacts table omits [`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md), which this PR does change; "six changed paths" is therefore false; `§ Operational rider` is referenced and does not exist; and §0.1's "everything read at `06a3f41`" is falsified for that file, whose row 12 records a run minted 29 s **after** `06a3f41`. | Verified — all four are true. The dangling reference and the ledger omission were mine. | **ACCEPTED, in full.** The **Operational rider** section is now written (below). The header's Base line is qualified. §v2.6's artifact table lists the ledger file and, per the diff-stage review, states **two counts** — this planning PR's two files and the implementation PR's seven — rather than one summed figure. |
| **A-N1** | Six `clearPendingAction()` call sites, not five — [`:870`](../../static/js/modules/backup-center.js#L870) (the delete branch) was omitted, under a heading claiming "all measured, none inferred". | Verified by grepping the symbol: `:538 :575 :635 :860 :870 :891` + the binding at `:1059`. | **ACCEPTED-AS-CORRECTION.** §0.1's table rebuilt from the grep. **§v2.1a (Scope)**, §v2.3 and §v2.11 all say six; Plan v1's frozen §Scope, which says five, is superseded by §v2.1a. |
| **A-N2** | `u5` and `u6` silently degrade into selection-change tests unless the fixture pins the selection: a search string that excludes the selected backup, or a filter the selected backup fails, takes the `:960-961` / `:910-911` branch instead. They would then inherit `:155`'s vacuity while claiming to replace it. | Verified against `getVisibleBackups()` [`:70-98`](../../static/js/modules/backup-center.js#L70-L98) and both handlers. | **ACCEPTED.** §v2.8 specifies for `u5` a filter matching the selected backup's `backup_type`, for `u6` a substring of the selected backup's own name, and requires **both** arms to assert the selection is unchanged — otherwise the arm is not measuring what it claims. |
| **A-N3** | A fifth design is missing: **Design E — do not refresh at all on save-first.** It removes the teardown, the round trips and every interleaving at once. Its costs: the handler must take over the button reset, and the new snapshot is absent from the library until the flow ends, which **reds `program-backup.spec.ts:153-154`**. | Verified: `:153-154` assert the snapshot appears in the list. Design E does red them. | **ACCEPTED as a plan defect; Design E EVALUATED AND REJECTED.** §v2.2 adds it with its costs stated. Rejected because it inverts a *correct* existing assertion (unlike `:155`, which is vacuous), and because the save-first snapshot's absence from the library is a real information loss for a user deciding whether to proceed. Recorded so the owner can overrule. |
| **A-N4** | Under OD-3(b), the "Saved" label becomes a **seventh** writer of `#backup-restore-save-first`'s `innerHTML`/`disabled`; and the state is **not durable** — any later `clearPendingAction()` resets it at `:165-166` and a re-opened Restore relabels it at `:728`. | Verified: writers at `:166`, `:725-728`, `:821`, `:879`, `:1030`, `:1045`. | **ACCEPTED.** Folded into **OD-3**, whose (b) row now carries the non-durability honestly. §v2.3 requires the label to live in one module constant if (b) is chosen. |
| **A-N5** | OD-1's "obstacle 1" is a syllogism the authorizing text does not support: [`OPEN_WORK_EXECUTION_PLAN.md:158-160`](../OPEN_WORK_EXECUTION_PLAN.md#L158-L160) says U2's *requirements* are settled, not that U2 may not do something needing a Gate 0 — the owner can simply grant one. Obstacle 2 (the window) is the decisive, measured one. | Verified — the reviewer is right about what the text says. | **ACCEPTED.** §v2.1 restructures OD-1 so the **qualification window is the obstacle** and Q3 is an **argument**. This matters: it means the owner *can* grant (ii) without contradiction, which is precisely what an owner decision should look like. |
| **A-N6 · P-NIT** | §0.0's clauses are called "verbatim" and are paraphrases; one difference is load-bearing, because arms C/D/E change no selection and are not covered by the source's "changing selection" at all. | Verified against [`:162-180`](../OPEN_WORK_EXECUTION_PLAN.md#L162-L180). | **ACCEPTED-AS-CORRECTION.** §0.0 rewritten; the three differences are enumerated and the deliberate strengthening is stated. |
| **A-NIT ×7** | Header anchor pointed at Packet U1 (`:107-131` is U1; U2 is `:152-181`) · "stale by two awaits" is off by one · §0.5's arm-E attribution · the inventory duty routes from `QUALITY_GATE.md:59`, not `:30` · the `catch` runs `:1042-1050` · the literal is `Loading backup details...` with ASCII periods · 82 hard waits is a repository total, the pin is per-file. | All seven verified. | **ALL ACCEPTED.** Header corrected; §0.5 corrected; the rest applied in Plan v2's prose. |

### `test-strategist`

| ID | Finding | Verification | Disposition |
|---|---|---|---|
| **T-B1** | **Plan v1's arms cannot kill its own primary mutation.** `expectToast` resolves at [`:1039`](../../static/js/modules/backup-center.js#L1039), **before `refreshBackupCenter()` is entered**. So `u1`'s "assert before touching anything else" samples the **pre-teardown** panel; on the M1 mutant the panel has never been torn down and `u1` passes. `u2` inherits it. The proposed `waitForResponse('**/api/backups')` matches the POST and the list GET, both of which settle before `:635`, so it is the same false green. And `showPendingAction()` rebuilds the panel **byte-identically**, so under OD-3(a) **no DOM state discriminates "never torn down" from "torn down and rebuilt"**. | **MEASURED, §0.7(a).** The teardown is the last event, after all three responses. The reviewer is exactly right. | **ACCEPTED, in full — this is the finding that reshapes the test design.** §v2.8 replaces state-sampling with a **transition oracle**: a `MutationObserver` installed before the click, recording every `hidden` flip, asserted to be the sequence `[true, false]`. §v2.9 re-predicts M1 as **red by timeout** (only `[true]` is ever recorded). The "assert before touching anything else" wording is deleted. |
| **T-B2** | §0.5's reasoning about `:155` is wrong, and post-fix `:155` becomes **bistable**, because `:685`'s `else if` chain discards the search's selection change and the re-assert lands last. Deleting it is mandatory; the offered "alternative — invert and move above `:153`" is **the exact false-green construction** T-B1 identifies and must be struck. | Verified by tracing `:685-691`, `:649`, `:653`. The `else if` chain does take the first branch. | **ACCEPTED, in full.** §0.5's consequence 1 reversed in place. §v2.8 makes the deletion mandatory and **strikes the alternative**. §v2.13 requires the bistability to be measured (20 runs of the unmodified test against the patched branch) before deleting, so the claim is evidence and not assertion. |
| **T-B3** | **M2 is not unkillable.** `page.route` is used four times in this very spec (`:169`, `:204`, `:242`, `:291`) and `page.request` nine times. Intercepting `GET /api/backups` to omit the captured id drives `refreshBackupCenter` into the `:687-688` fallback and kills the mutation in five lines. Shipping a data-loss guard "manually verified only" when that is available is not defensible at Gate 1. | Verified — 4 + 9 = 13 `page.route`/`page.request` uses in the file. | **ACCEPTED, in full.** §v2.8 adds arm **`u9`**; §v2.9 re-predicts **M2 as red on `u9`**; §v2.12's residual 1 is **deleted**. |
| **T-B5** | [`QUALITY_GATE.md:224`](../ai_workflow/QUALITY_GATE.md) records `program-backup.spec.ts:79` as a documented DB-pollution flake. Plan v1's rollback condition 6 ("any of the 22 pre-existing tests reds → revert") would mandate reverting a correct fix on one recurrence. | Verified — the known-red is recorded, and `:79` is `can create a backup from the dedicated page`. | **ACCEPTED.** §v2.11 carves it out explicitly and requires an isolation re-run before it counts. §v2.11 also records that the citation **survives** this edit: `:155` is deleted (shifting only lines >155) and the new block is appended, so `:79` stays `:79`. |
| **T-NB1** | A derived pytest target was missed: [`tests/test_css_cascade_contracts.py:259`](../../tests/test_css_cascade_contracts.py#L259) reads `backup-center.js` and asserts a literal substring in it. §v1.9's *"no `.py` is touched, therefore no pytest"* skipped QUALITY_GATE's targeted-test derivation step. | Verified — the file does read `backup-center.js`. | **ACCEPTED.** §v2.10 adds it. The **conclusion** (no full `pytest`) is unchanged and the reviewer independently re-derived it against every escalation trigger — but the derivation is now the documented one. |
| **T-NB2** | `Type Check` is a **derived** gate, not a bystander: [`tsconfig.json`](../../tsconfig.json) has `"include": ["e2e/**/*.ts", …]` under `"strict": true`. Concretely material, because the T-B1 `MutationObserver` oracle needs a `declare global` block or `strict` rejects the implicit `any`. | Verified — the tsconfig is exactly that. | **ACCEPTED.** §v2.10 lists `npx tsc --noEmit` as required-and-derived; §v2.8 requires the declaration. |
| **T-NB3** | §v1.7 called `waitForResponse` "already idiomatic in this spec". It appears **zero** times in `program-backup.spec.ts`. | Verified. | **ACCEPTED-AS-CORRECTION.** Moot under the new oracle, which uses no `waitForResponse` at all; the false claim is removed. |
| **T-NB4 · P** | The `accessibility.spec.ts` rationale is overstated — the fix changes nothing at rest, since `#backup-action-confirm` is `hidden` in source. The axe pins are real ([`accessibility.spec.ts:841-842`](../../e2e/accessibility.spec.ts#L841-L842), `nodes: 2` each) but U2 cannot move them. Same for `erase-flow.spec.ts`: a clause-5 product control, not table-derived. | Verified both. | **ACCEPTED.** §v2.10 relabels both as **discretionary tripwires** with honest rationales, and keeps them — a tripwire that fires only if the implementation drifts into `backup.html` is worth its cost. |
| **T-NB5** | The predicted counts are right for six arms and will be wrong after this review adds arms. State them as **derived from the arm list**, not as a pin. | Verified: `22` tests, `662` total, `82`/`14` hard waits, `231`/`13` vitest. | **ACCEPTED.** §v2.14 states counts as derived and gives the arithmetic. |
| **T-NB6** | §v1.3 rows 3, 4 and 5 have no arm. Row **3** matters: §v1.2 requires the capture **before** `await createBackup(...)`; an implementer who places it after silently breaks the untouched `catch`, and nothing notices. | Verified. | **ACCEPTED.** §v2.8 adds arm **`u10`** (500 on `POST /api/backups`; panel still visible, both buttons re-enabled and re-labelled). It is the only guard on §v1.2(C)'s "nothing else changes". |
| **T-NB7** | The plan's self-declared "primary hazard" (the missing `finally`) has **no assertion**. Low-risk under Design B, but **blocking if OD-2 had selected (c)**. | Verified. | **ACCEPTED.** §v2.8 adds the `disabled`/label assertions to `u1` now. Under Plan v2 this is no longer merely prophylactic: `setDetailActionDisabled(true)` makes the handler own the unlock, so the hazard is live again and must be asserted. |
| **T-N1** | `u3` (cancel after settle) is close to unfalsifiable — cancel is bound once at `:1059` and U2 does not touch it; no plausible U2 defect makes the panel un-cancellable. Drop the "Kills" claim. | Verified. | **PARTIALLY ACCEPTED.** The "Kills" claim is dropped and `u3` is relabelled a characterization guard. It is **kept, and it is no longer vacuous under Plan v2**: `setDetailActionDisabled()` now disables `#backup-action-cancel` mid-flight, and `clearPendingAction()` does **not** reset that button's `disabled` (`:157-169`), so a fix that forgets to unlock leaves Cancel permanently dead. `u3` catches exactly that. |
| **T-N2** | M6 cannot falsify what it claims: `u5` and `u6` never invoke `handleListClick`. Its *prediction* is right but for the wrong reason — `:891` and `:635` produce an identical terminal state, so M6 is a timing mutation with no terminal observable. The mutation that actually tests §0.3's attribution is deleting `:635` and predicting `u4`/`u5`/`u6` all red. | Verified. | **ACCEPTED.** §v2.9 adds that as **M7** and keeps the `:891` mutation as **M8** with its reasoning corrected. §v1.8's "M3 — not applicable" confused *mutating shipped code* with *proving the arms discriminate*; M7 is the latter. |
| **T-N3** | M4 is **unreachable through the UI**, not equivalent — `dispatchEvent('click')` would reach it. "Equivalent" means no test can ever distinguish it; that is a stronger and false claim. | Verified. | **ACCEPTED.** §v2.9 relabels it unreachable-by-affordance. |
| **T-N4** | §v1.9's drift-gate derivation is circular — it maps the gate to the artifact, which is the remedy, not the trigger. | Verified. | **ACCEPTED.** §v2.10 derives it from `QUALITY_GATE.md:59`. |
| **T-N5** | `showPendingAction()` also calls `clearInlineEditState()` at [`:710`](../../static/js/modules/backup-center.js#L710), so re-asserting also tears down any inline editor. Unreachable under Design B, but "nothing else changes" is one call deeper than it reads. | Verified. | **ACCEPTED.** Stated in §v2.3. |

### `product-risk-reviewer`

| ID | Finding | Verification | Disposition |
|---|---|---|---|
| **P-B2** | §v1.4 puts the network on the wrong side of the teardown, so **OD-2 asks the owner to price a cost that probably does not exist** — and §v1.11 books a residual risk that may be imaginary. Measure it rather than assert either way. Separately: the confirm panel stays **visible** during the two round trips, above a table reading "Loading backup details...", today and after U2 alike. | **MEASURED, §0.7(a).** Teardown at 149.5 ms / frame 36, after all three responses; a re-assert resumes in a microtask off the same frame, so **no paint is expected**. The panel is `hidden:false` throughout the flight, as the reviewer said. | **ACCEPTED, and the reviewer's requested measurement was taken.** §v1.4 corrected in §0.1 and §0.7. **OD-2 is RETIRED** — Plan v2 does not put it to the owner, because it has been measured away. Design A's only justification went with it. |
| **P-B3** | §v1.11's "U2 does not make this worse" is false: U2 converts an unannounced **disarmed** state into an unannounced **armed destructive** one. Focus is never mentioned once — under OD-3(b) a `disabled` button is unfocusable, so a keyboard user is dumped on `<body>` in front of a re-armed destructive control. And the stated reason for not repairing ("it means editing `backup.html`") is wrong: `showPendingAction()` can set the attribute from JS with zero template edits. | Verified: `#backup-action-confirm` has no role/`aria-live` ([`backup.html:187`](../../templates/backup.html#L187)); the toast **is** announced (`role="alert"`, `aria-live="assertive"`). | **ACCEPTED, in full.** The "does not make this worse" claim is withdrawn. Promoted from a recorded residual to **OD-6**, with a recommended default (announce the panel; focus **Cancel**, never the destructive control) and a new arm asserting `document.activeElement`. The JS-only route means the repair costs no template edit and no visual gate. |
| **P-B4** | `create_backup()` covers `user_selection` only; `restore_backup()` deletes `user_selection` **and** `workout_log`. The protective affordance is narrower than the loss described one line above it, and OD-3(b)'s proposed copy would state that overclaim on screen. U2 makes the misreading **more** available. | **VERIFIED by source**: [`program_backup.py:201`](../../utils/program_backup.py#L201) vs [`:478-479`](../../utils/program_backup.py#L478-L479). | **ACCEPTED, in full.** New §0.8 records the measurement. New **OD-5** puts the copy question to the owner with concrete candidates. This was entirely outside clauses 1–5 and would have shipped unnoticed. |
| **P-N1** | OD-3(a)'s "nothing is lost or corrupted" understates the cost. The stamp is second-resolution (`.slice(0,19)`), `UNIQUE(name, created_at)` does not stop duplicates because `created_at` carries microseconds, and `formatDate()` renders at **minute** resolution — so two snapshots in the same minute are **identical in every rendered field**. And they are permanent: `prune_auto_backups()` deletes `backup_type='auto'` only. In the emergency this feature exists for, the user picks between identical rows where a wrong pick wipes everything. | Verified: [`:1037`](../../static/js/modules/backup-center.js#L1037), [`program_backup.py:58`](../../utils/program_backup.py#L58), [`:211`](../../utils/program_backup.py#L211), [`:685-687`](../../utils/program_backup.py#L685-L687), `formatDate()` [`:42-57`](../../static/js/modules/backup-center.js#L42-L57). | **ACCEPTED.** OD-3(a)'s consequence cell rewritten with the measured facts; the OD now also asks whether the stamp should carry sub-second resolution. The **UTC-stamp / local-render** mismatch the reviewer flagged is recorded in §v2.12 as pre-existing and **not repaired here**. |
| **P-N2** | OD-3(b)'s "no duplicate snapshots" is overclaimed — the state survives only the current panel instance. And its justification ("without relying on a toast that has already begun to fade") is **inverted for an AT user**: the toast *is* announced; a `disabled` relabel is announced to nobody. | Verified. | **ACCEPTED.** Both corrections carried into OD-3(b), and the AT point is cross-linked to OD-6. |
| **P-N3** | §v1.3 row 6's guard is correct but **fails silently**, and U2 teaches the user to expect otherwise — a learned expectation that fails silently is worse than a consistent failure. States 4 and 5 both surface a message; state 6 does not. | Verified: `renderDetailError()` and `renderLibraryState()` both message; the `id`-mismatch branch does not. | **ACCEPTED.** §v2.3 requires an explicit `showToast('warning', …)` on the no-re-assert branch, wording folded into **OD-5**. This also gives the guard an observable, which is part of why `u9` can kill M2. |
| **P-N4** | Substituting the captured id into `preferredSelectionId` is a **behavior change**, not a staleness fix: today's read reflects a selection the user changed *during* the flow, and the substitution overrides the user. | Verified — Plan v1 justified it as fixing staleness. The reviewer is right that it changes direction. | **ACCEPTED.** §v2.3 **drops the substitution**. Under Plan v2 the mid-flight lock plus the generation counter make it unnecessary, and it was the more invasive of the two options. Recorded in §v2.7's migration notes as considered-and-rejected. |
| **P-N5** | OD-2(b) is the union of OD-2(a) and OD-3(b), so the owner can answer OD-2(b) and OD-3(a) and produce a contradiction. And **OD-4 is not the owner's decision** — it is implementation architecture, already answered, inflating the list and inviting authorization of a larger packet with no product reason. | Verified — both are drafting defects in Plan v1. | **ACCEPTED.** OD-2 is retired outright (P-B2), which dissolves the contradiction. **OD-4 is demoted** to a decided note under its own heading in §v2.1. The freed slots carry **OD-5** and **OD-6**, which are genuine product questions Plan v1 answered by silence. |
| **P-N6** | OD-3(b)'s copy is offered as an "e.g.", which cannot be signed. On register: the confirm panel's own labels are sentence case while the detail-action labels are Title Case, so `Current plan saved` is right — and the plan should **say so as a measurement** rather than leave it to taste. | Verified: `Save current plan first` / `Cancel` vs `Restore To Current Plan` / `Confirm Restore` / `Delete Backup`. | **ACCEPTED.** OD-3(b) and OD-5 now carry **exact, signable candidate strings** with the register measurement stated. |
| **P-NIT ×3** | §0.5's arm-E attribution (same as A-NIT/T-B2) · §v1.9's manual-smoke script cannot reach any in-flight state · the `22 → 28` base is right but the target moves. | All verified. | **ALL ACCEPTED.** §v2.10's manual smoke is extended with the four in-flight interactions rather than inherited from §0.2. |

### Claims the reviewers verified **for** Plan v1 — recorded so they are not re-litigated

- **§0.3's load-bearing claim is confirmed by independent code trace** (A): sort `:982-999`, filter `:895-921` and search `:957-972` contain no `clearPendingAction()`; each reaches it only via `:635`. **Design 0 is correctly rejected.**
- **The 25-spec pin is not approached** (A and T, independently). `program-backup.spec.ts` is in `EXPECTED_EXCLUSIONS` at [`test_playwright_shard_launcher_contracts.py:36`](../../tests/test_playwright_shard_launcher_contracts.py#L36); the `== 25` assertion at [`:67`](../../tests/test_playwright_shard_launcher_contracts.py#L67) reads the shard step only and **cannot see this spec**; `TEST_INVENTORY.json` records `"in_required_functional_set": false`. Extending this spec is structurally free.
- **Module boundaries: no violation** (A). No new import, one export preserved, no second source of truth, **zero signature churn** — and the plan does not understate it.
- **Design C correctly rejected** (A): `:798`, `:861`, `:871` are a uniform re-fetch-after-mutation discipline.
- **Clause 5 holds structurally** (A and P). `backup-center.js` imports six symbols from `program-backup.js` and not the seventh; grep for `showAutoBackupBanner`/`erase` in `backup-center.js` returns **0**; `program-backup.js` holds **no module-level mutable state**, so no shared-state channel exists even in principle.
- **No calculation-semantics or non-goal exposure** (P): nothing touches `effective_sets`, `weekly_summary`, `session_summary`, `progression`, fatigue, `CountingMode`/`ContributionMode`, and no auth/cloud/remote-DB surface is involved.
- **Full `pytest` is genuinely not required** (T, re-derived independently against every escalation trigger) — with the three additions in T-NB1, T-NB2 and T-B5.
- **`/build-css` and `visual.spec.ts` correctly excluded** (T).
- **The identity check is well-founded on the payload** (A): [`program_backup.py:377`](../../utils/program_backup.py#L377) selects `id`, so `selectedBackupDetails.id` is never `undefined`.
- **Creating `docs/backup_confirmation_continuity/PLANNING.md` moves no inventory node** (T). Independently confirmed here by running `scripts/generate_test_inventory.py --check` in the worktree: **"Test inventory is up to date"**, exit 0.

---

## Plan v2

> **Plan v2 governs.** It supersedes Plan v1 entirely. Where Plan v1 and Plan v2 could be read as
> disagreeing, Plan v2 wins; where §0 and either plan disagree, **§0 wins**, because §0 is measurement.

### v2.0 What changed from Plan v1, in one place

Plan v1's *diagnosis* survived review intact and is unchanged: the mechanism (§0.1), the reproduction
(§0.2), the five clearing paths (§0.3), the Q3 collision (§0.4) and the blindness of the existing
coverage (§0.5) were all confirmed, two of them by independent code trace. **Plan v1's *design* and
its *test design* did not survive.**

| # | What Plan v1 said | What Plan v2 says | Driver |
|---|---|---|---|
| 1 | The identity check on `selectedBackupDetails.id` is "the safety property". | It is **not a safety property at all** — it cannot see intent revocation, and it reads a variable that lags. Replaced by a **generation counter** plus a **mid-flight lock**. | A-B1 · T-B4 · P-B1 · A-B2, measured §0.7(c)(d) |
| 2 | The blink is a real cost and **OD-2** asks the owner to price it. | The blink was **measured away**. **OD-2 is retired**, and with it Design A's only justification. | P-B2, measured §0.7(a) |
| 3 | `u1`/`u2` kill M1 by asserting panel state after the toast. | They **cannot** — the toast fires two round trips early. Replaced by a **transition oracle**. | T-B1, measured §0.7(a) |
| 4 | `:155` need not be inverted; deleting it is a preference. | `:155` becomes **bistable** post-fix; deleting it is **mandatory**, and the "alternative" was a false green — **struck**. | T-B2 |
| 5 | M2 is unkillable; the guard ships inspection-only. | M2 **is** killable with fixtures already in the file. New arm `u9`; the residual is deleted. | T-B3 |
| 6 | Four owner decisions: OD-1..OD-4. | **Four owner decisions: OD-1, OD-3, OD-5, OD-6.** OD-2 retired (measured away), OD-4 demoted (not the owner's), **OD-5** and **OD-6** added — both were questions Plan v1 answered by silence. | P-B3 · P-B4 · P-N5 |
| 7 | Six changed paths; gates derived from three rows. | **Seven files in the implementation PR, two in this one — counted separately**; three gate omissions repaired (`test_css_cascade_contracts.py`, `Type Check`, the known-red carve-out). | A-B3 · T-NB1 · T-NB2 · T-B5 |
| 8 | Five `clearPendingAction()` call sites. | **Six**, plus one binding. | A-N1 |

---

### v2.1 Owner decisions

Four. Each is genuinely the owner's: two are product behavior, one is user-facing copy on a
destructive flow, one spends a shared resource that is not U2's.

⚠️ **ALL FOUR ARE DECIDED — 2026-08-26.** Each decision is recorded in its own subsection below under a
**DECIDED** line, and each selects the option Plan v2 recommended. **Plan v2's recommendations and
their arguments are left standing as written**, so the decision can be read against the reasoning that
produced it rather than replacing it.

**Every artifact, gate, count and risk below has been re-derived against the decisions rather than
against the recommendations.** They coincide here, and that coincidence is not a licence to skip the
derivation — two restatements were falsified rather than merely confirmed by it, and both are marked
⚠️ where they live (§v2.8's `u1` assertion row, and §v2.8's oracle rationale).

---

#### OD-1 — Coverage tier: E2E-only, or a Vitest file for `backup-center.js`?

> **DECIDED — 2026-08-26: (i) E2E-only.** The owner further directed: **do not add or schedule a
> Vitest follow-up.** Option **(iii) is declined, not deferred** — U2 books **no** follow-up
> obligation, **no** tracked rider and **no** successor packet against `backup-center.js` unit
> coverage. If that coverage is ever wanted, it must be opened as its own packet with its own Gate 0,
> by a future decision that this one does not pre-commit.
>
> **Derived consequences.** Zero Vitest files and zero Vitest cases ship. The qualifying suite stays
> at **13 files / 231 cases**; **T0 stays `2026-08-22T17:59:26Z`** and the strict mark stays
> **`2026-09-05T17:59:26Z`**; Q2's restart clause does not engage; **D2 is not spent**. The generation
> counter and the re-assert guard get **E2E coverage only**, and `backup-center.js` keeps 0 % unit
> coverage as an accepted, recorded gap — §v2.12 residual 2, now decided rather than pending.

⚠️ **Restructured per A-N5.** The decisive obstacle is the qualification window; owner ruling Q3 is an
argument, not a barrier, because the owner can grant the Gate 0 it asks for.

**The obstacle — measured.** [`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md)
§6.5 ([`:844-868`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L844-L868)) is running a live strict
14-day window: **T0 = `2026-08-22T17:59:26Z`**, strict mark **`2026-09-05T17:59:26Z`**. The suite it qualifies is pinned at **13 files / 231 cases** — a figure that comes from §13.0 and [`TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json), **not** from §6.5, which states only T0 and the mark. The ledger's state, elapsed time and time remaining are measured once, in the **§*Operational rider***, and are **not restated here** — §13.0's own rule is that the count lives in exactly one place. The operative restart test, ratified as **R13** during U1's Gate 1, is **"changed no JS test
case"**. A new `backup-center.test.js` changes one, engages Q2's restart clause, discards the days
accumulated and moves the strict mark to roughly U2's merge plus fourteen days — **delaying D2**.

**The argument — owner ruling Q3.** §0.4. `backup-center.js` is `CLOSED UNSTARTED` for step 12, its
0 % unit coverage is an *accepted, recorded* gap, and reviving it "needs its own Gate 0 and its own
plan". U2 has no Gate 0 ([`OPEN_WORK_EXECUTION_PLAN.md:158-160`](../OPEN_WORK_EXECUTION_PLAN.md#L158-L160)),
but that text settles U2's *requirements*, not its permissions — **the owner can simply grant a Gate
0 if they want option (ii)**. Q3's substantive point stands on its own: unit-testing this module at
its single export means standing up the whole Backup Center DOM, "an integration test wearing a unit
test's clothing".

| Option | What U2 ships | Cost, stated honestly |
|---|---|---|
| **(i) E2E-only — RECOMMENDED** | Every arm in [`e2e/program-backup.spec.ts`](../../e2e/program-backup.spec.ts). Zero Vitest files, zero Vitest cases. | Window untouched — the suite stays at 13 / 231 and the strict mark stays `2026-09-05T17:59:26Z`. Q3's recorded gap stays recorded. Cost: the generation counter and the re-assert guard get no unit-level coverage. Per-spec Playwright counts move — an ordinary inventory regeneration that reds nothing. |
| **(ii) Vitest now** | A new `static/js/modules/__tests__/backup-center.test.js`, **plus** the Gate 0 Q3 requires. | **Restarts the window** on the rule §13.0 has applied at every row since T0. Spends **D2**, which is not U2's to spend, and adds a Gate 0 round to a packet the roadmap sized at 0.5–1 day. |
| **(iii) Vitest deferred past the strict mark** | (i) now, plus a **separate packet** after `2026-09-05T17:59:26Z`, with its own Gate 0. | Window untouched, Q3 honoured, coverage eventually written. Cost: a second packet and a second review cycle. |

**Recommendation: (i).** Deliberately **not** (iii)-as-a-rider — U2 should not book a follow-up
obligation against a module whose unit coverage the owner has already ruled needs its own Gate 0. If
the owner wants (iii), opening it as its own packet is the honest form, and that is itself part of
this decision.

---

#### OD-2 — RETIRED, not deferred

Plan v1 asked the owner to price a visible "blink". **§0.7(a) measured it away**: the teardown is the
*last* event of the refresh, 0.8 ms after the final network response and in the same animation frame,
so a re-assert resumes in a microtask off that frame with **no paint expected between them**. There is
no cost to price. Design A — the only design that needed OD-2(c) to justify its three changed
signatures and its deliberate §0.3 regression risk — is rejected with it. **Recorded rather than
deleted**, so a later reader does not re-raise it.

---

#### OD-3 — After a successful save-first, may the user save again?

> **DECIDED — 2026-08-26: (b) disable and relabel**, with the exact string **`Current plan saved`**.
> **The sub-question is answered NO**: the snapshot stamp does **not** gain sub-second resolution. It
> stays second-resolution at [`:1037`](../../static/js/modules/backup-center.js#L1037) and U2 changes
> not one character of it.
>
> **Derived consequences.** §v2.3 clause **(D)** becomes unconditional, and the label lives in **one
> module constant** (A-N4) — a seventh *writer* of that button, not a seventh scattered literal.
> Option (a)'s indistinguishable-duplicate-rows hazard is **largely averted**, which is exactly why
> the sub-second stamp is unnecessary; it is **not eliminated**, because (b)'s first honest limit
> stands — the `disabled` state is not durable, so a cancel / re-open cycle re-enables the button and
> a second snapshot stays reachable (§v2.12 residual 7).
>
> ⚠️ **This decision falsifies a Plan v2 assertion rather than merely confirming it.** §v2.8's `u1`
> row, following **T-NB7**, asserted *both* spinner-locked buttons `toBeEnabled()` with their correct
> labels. Under (b) the save-first button ends **disabled** and relabelled. That assertion is
> **inverted for that button** in §v2.8, and §v2.8's oracle rationale is narrowed with it.

Today unanswerable (the button is torn down). Once the panel is restored it must be answered.

| Option | Behavior | Consequence — ⚠️ measured, per P-N1 and P-N2 |
|---|---|---|
| **(a) Leave it enabled** | Repeated clicks create repeated snapshots. | **Not merely clutter.** The stamp is second-resolution ([`:1037`](../../static/js/modules/backup-center.js#L1037)), so two clicks in one second produce two rows with an **identical name**; `UNIQUE(name, created_at)` ([`program_backup.py:58`](../../utils/program_backup.py#L58)) does not stop them because `created_at` carries microseconds ([`:211`](../../utils/program_backup.py#L211)); and `formatDate()` renders at **minute** resolution ([`:42-57`](../../static/js/modules/backup-center.js#L42-L57)). **Two snapshots in the same minute are identical in every rendered field** — name, created time, and `item_count` (which cannot differ, since `user_selection` does not change from `/backup`). The only discriminator is the hidden `data-backup-id`. They are permanent: `prune_auto_backups()` deletes `backup_type='auto'` only ([`:685-687`](../../utils/program_backup.py#L685-L687)) and these are `'manual'` ([`routes/program_backup.py:105`](../../routes/program_backup.py#L105)). In the emergency this feature exists for, the user chooses between indistinguishable rows where a wrong choice wipes the plan and every logged session. |
| **(b) Disable and relabel — RECOMMENDED** | Exact candidate strings, signable as written: **`Current plan saved`** *(recommended)* · `Snapshot saved` · `Plan snapshot taken`. Rendered as `<i class="fas fa-check" aria-hidden="true"></i> Current plan saved`, `disabled`. | Answers the question the user actually has, without depending on a toast. **Register measured (P-N6)**: this panel's own labels are sentence case (`Save current plan first`, `Cancel`) while detail-action labels are Title Case (`Restore To Current Plan`, `Confirm Restore`, `Delete Backup`) — so `Current plan saved` matches the button's existing register and echoes the toast prefix at `:1039`. **Two honest limits**: the state is **not durable** — any later `clearPendingAction()` resets it at [`:165-166`](../../static/js/modules/backup-center.js#L165-L166) and a re-opened Restore relabels it at [`:728`](../../static/js/modules/backup-center.js#L728), so a cancel/re-open cycle invites a second snapshot anyway; and it is announced to **nobody** — see **OD-6**, where the AT user's version of this benefit lives. |
| **(c) Hide it** | Panel returns with Cancel and Confirm Restore only. | Cleanest, but removes an affordance the user could see a moment earlier, with no explanation. |

**Recommendation: (b)**, with **`Current plan saved`**. A sub-question the owner may also settle:
**should the stamp carry sub-second resolution** so duplicate rows are at least distinguishable by
name? Recommended **yes if (a) is chosen**, unnecessary under (b).

---

#### OD-4 — DEMOTED, per P-N5

*"Is a `pendingAction` seam extraction in scope?"* is implementation architecture, not a product
decision, and presenting it as the owner's invited authorization of a larger packet for no product
reason. **The answer is no, and Plan v2 makes it.** No candidate design needs it; §0.4 shows Q3
disposed of it only within step 12's scope, so it is neither forbidden nor licensed here. If a
reviewer argues for it, it is a **separate packet with a different size class**.

---

#### OD-5 — NEW. Must the save-first affordance say that logged sessions are not included?

> **DECIDED — 2026-08-26: (a) state the limit**, in the owner's exact words:
>
> ```
> Saves the current workout plan only — logged sessions are not included in this snapshot.
> ```
>
> **The bundled second string is decided with it** — the state-6 warning toast, in the owner's exact
> words:
>
> ```
> The backup you were restoring is no longer available. Please choose it again.
> ```
>
> **Neither string is the implementer's to reword.** Both are signed criteria.
>
> **Derived consequences.** §v2.3 gains a new clause **(F)**: the note is rendered **from JS** by
> `showPendingAction()`, in the **`restore` branch only**, so
> [`templates/backup.html`](../../templates/backup.html) stays **unmodified** and the `templates/**`
> gate row and the visual matrix stay out of the gate set — exactly as OD-3(b) and OD-6(a) already
> do. §v2.3(B) condition 4's toast text is **pinned** to the string above instead of left as `…`.
> §v2.12 residual 6 is **closed**. The note lives inside `#backup-action-confirm`, which is `hidden`
> at rest, so `accessibility.spec.ts`'s at-rest axe pins cannot move — a property of the panel's rest
> state, which §v2.10 step 6 now proves rather than assumes.

**The measured fact (§0.8)**, which no clause of the requirement mentions: `create_backup()` reads
**`user_selection` only** ([`program_backup.py:201`](../../utils/program_backup.py#L201)), while the
restore it guards deletes **`workout_log` *and* `user_selection`**
([`:478-479`](../../utils/program_backup.py#L478-L479)). The warning one line above the button says
*"The current workout plan **and all logged sessions** will be cleared."* **The snapshot does not
contain the sessions.**

U2 does not create this. **U2 makes it materially more available** — today the affordance vanishes the
instant it is used; U2's whole purpose is to keep it on screen afterwards, next to that warning, in a
state that reads as "done".

| Option | What ships |
|---|---|
| **(a) State the limit — RECOMMENDED** | One line inside `#backup-action-confirm`, below the warning. Candidates, signable as written: **`Saves the current workout plan only — logged sessions are not included in this snapshot.`** *(recommended)* · `This snapshot covers your workout plan. Logged sessions are not saved.` |
| **(b) Ship without it** | No copy change. The mismatch is recorded in §v2.12 as an accepted, owner-decided residual. |
| **(c) Rename the button** | e.g. `Save current plan first` → `Save current plan first (plan only)`. Cheapest, but crowds a button that already carries an icon and six words. |

**Recommendation: (a).** **The owner decides, including the exact string.** This is the most
consequential copy decision in the packet and it must not fall to the implementer.

**A second string is bundled here**, per **P-N3**: state 6 (the restore target vanishes mid-refresh)
currently fails **silently**, and U2 teaches the user to expect continuity, so a silent failure is
worse after U2 than before. Plan v2 requires a `showToast('warning', …)` on that branch. Candidate:
**`The backup you were restoring is no longer available. Please choose it again.`**

---

#### OD-6 — NEW. Is the re-asserted confirmation announced, and where does focus go?

> **DECIDED — 2026-08-26: (a) announce, and place focus on Cancel.**
>
> **Derived consequences.** §v2.3 clause **(E)** becomes unconditional. Arm **`u11`** becomes
> **mandatory**, taking the appended block to **eleven** arms (`u1`–`u11`) and collapsing every
> conditional "(or 33)" figure in §v2.14 to a single derived value. §v2.10 step 6
> (`accessibility.spec.ts`) becomes **required** rather than discretionary. §v2.12 residual 5 is
> **closed**. Focus goes to `#backup-action-cancel` — the safe control — and **never** to
> `#backup-action-confirm-btn`. Still **zero template edits**: both the `role` and the focus move are
> applied from JS.

⚠️ **P-B3 withdrew Plan v1's claim that U2 "does not make this worse".** Measured: `#backup-action-confirm`
([`backup.html:187`](../../templates/backup.html#L187)) has **no role and no `aria-live`**, while the
toast **is** announced (`role="alert"`, `aria-live="assertive"`). So today, after save-first, an
assistive-technology user hears the toast and is left on a page with **nothing armed**. Under U2 they
hear the same toast and are left with a live **Confirm Restore** button targeting an operation that
deletes the plan and every logged session — **and nothing announces it.** That is not "one more
un-announced state change"; it is the difference between disarmed and armed.

**Focus makes it sharper, and Plan v1 never mentioned focus once.** At the click, focus is on
`#backup-restore-save-first`, which `clearPendingAction()` then hides
([`:164`](../../static/js/modules/backup-center.js#L164)). **Under OD-3(b) the answer is not in
doubt**: a `disabled` button is not focusable, so focus is definitively lost to `<body>` — a keyboard
user is left in front of a re-armed destructive control with no landmark and no announcement. For a
keyboard or screen-reader user, *"continue the same restore"* (clause 3) **is** focus continuity.

**Plan v1's stated reason for not repairing this was wrong**: it declined because the repair "means
editing `backup.html`, which pulls in the `templates/**` row and the visual matrix". `showPendingAction()`
can set the attribute **from JS**, with zero template edits, zero visual gate and no new artifact.

| Option | What ships |
|---|---|
| **(a) Announce and place focus — RECOMMENDED** | `showPendingAction()` sets `role="alert"` on `#backup-action-confirm` when re-asserting, **and** moves focus to `#backup-action-cancel` — the **safe** control, never `Confirm Restore`. Arm `u11` asserts `document.activeElement`. Zero template edits. |
| **(b) Announce only** | The `role`, no focus move. Cheaper; leaves the keyboard user on `<body>`. |
| **(c) Ship neither** | Recorded in §v2.12 as an owner-accepted residual, in the plain terms above. |

**Recommendation: (a).** **The owner decides.** If (c), the plan must say plainly that a destructive
confirmation is re-armed with no announcement and no focus target — which is what would be signed.

---

### v2.1a Scope

⚠️ **Added per the diff-stage review.** Plan v1's `§Scope` is frozen and lists only **five** `clearPendingAction()` call sites (A-N1). This is the governing statement.

- **In**: the save-first click listener at [`:1022-1051`](../../static/js/modules/backup-center.js#L1022-L1051); one new module-scoped counter and two increments; one new module-private helper; the mid-flight lock/unlock; one `test.describe` appended to [`e2e/program-backup.spec.ts`](../../e2e/program-backup.spec.ts) plus the mandatory [`:155`](../../e2e/program-backup.spec.ts#L155) deletion; a `KI-013` row; the `DUPLICATION_REGISTRY` row-10 residual; the regenerated [`docs/test_inventory/`](../test_inventory/) artifact; this document.
- **Out — `clearPendingAction()` and all SIX of its call sites.** Not one line of [`:148-170`](../../static/js/modules/backup-center.js#L148-L170) changes, and **none** of [`:538`](../../static/js/modules/backup-center.js#L538), [`:575`](../../static/js/modules/backup-center.js#L575), [`:635`](../../static/js/modules/backup-center.js#L635), [`:860`](../../static/js/modules/backup-center.js#L860), **[`:870`](../../static/js/modules/backup-center.js#L870)** or [`:891`](../../static/js/modules/backup-center.js#L891) is removed, moved or made conditional. The Cancel binding at [`:1059`](../../static/js/modules/backup-center.js#L1059) is likewise untouched.
- **Out — code**: `refreshBackupCenter()`, `loadBackupDetails()`, `renderBackupDetails()`, `handleConfirmAction()`, `handleSaveSubmit()`, the inline metadata editor; [`program-backup.js`](../../static/js/modules/program-backup.js) and therefore `showAutoBackupBanner()`; [`templates/backup.html`](../../templates/backup.html); [`toast.js`](../../static/js/modules/toast.js); [`fetch-wrapper.js`](../../static/js/modules/fetch-wrapper.js); [`routes/program_backup.py`](../../routes/program_backup.py); [`utils/program_backup.py`](../../utils/program_backup.py); [`utils/auto_backup.py`](../../utils/auto_backup.py); the `/api/backups*` contracts, status codes and payloads; DB schema and backup `schema_version`; any `scss/**` or `static/css/**` edit; any new `.spec.ts` file and therefore any [`ci.yml`](../../.github/workflows/ci.yml) edit; branch protection.
- **Out — U1's residue, named so it cannot drift in**: U1's AA/contrast debt; U1's coverage gaps; **U1-FOLLOWUP-1**; **KI-010** and **KI-011**; Dependabot PRs **#415** and **#416**; shared toast behavior of any kind; unrelated Backup Center cleanup.
- **Out — debt owned elsewhere**: [`MASTER_HANDOVER.md`](../MASTER_HANDOVER.md), [`ACTIVE_DEVELOPMENT.md`](../ACTIVE_DEVELOPMENT.md), [`LEFTOVERS_BY_PRIORITY.md`](../LEFTOVERS_BY_PRIORITY.md), packets U3, R0–R3, V1, Track P1, Track D1 — and the five stale ledger-count restatements listed under *Flagged, not edited*.

### v2.2 Design — B-hardened, and the four rejected alternatives

| Design | Verdict |
|---|---|
| **0 — delete or guard `:635`** | **REJECTED on measurement.** §0.3 arms C/D/E clear *only* through `:635`, selection unchanged. Independently confirmed by the architecture reviewer's code trace. |
| **A — thread a `preservePendingAction` option** | **REJECTED.** Its sole advantage was avoiding the blink, and **OD-2 measured the blink away**. It costs three changed signatures and makes `:635` conditional — the exact hazard §0.3 warns about. |
| **C — splice `backupsCache`, skip the refresh** | **REJECTED.** Invents a second source of truth against the module's uniform re-fetch-after-mutation discipline ([`:798`](../../static/js/modules/backup-center.js#L798), [`:861`](../../static/js/modules/backup-center.js#L861), [`:871`](../../static/js/modules/backup-center.js#L871)). Confirmed correct by review. |
| **E — do not refresh at all on save-first** ⚠️ *added by A-N3* | **EVALUATED AND REJECTED.** It genuinely removes the teardown, the round trips and **every** interleaving at once, and unlike C it invents no second source of truth — it only defers the fetch. Rejected for two reasons: (1) it **reds `program-backup.spec.ts:153-154`**, which assert the new snapshot appears in the library — and unlike `:155`, those assertions are **correct**, so inverting them would be weakening real coverage; (2) the snapshot's absence from the library is real information loss for a user deciding whether to proceed. The handler would also have to take over the button reset `:635` performs incidentally. **Recorded so the owner can overrule.** |
| **B-hardened — capture, authorize, re-assert — CHOSEN** | `:635` keeps firing on every path, so §0.3's arms are structurally untouched and no signature changes. Plan v1's Design B is kept **only** as its shape; its guard is replaced. |

---

### v2.3 Exact production change

All in [`backup-center.js`](../../static/js/modules/backup-center.js). No new import.

**(A) One new module-scoped counter**, beside the eight existing module variables at
[`:12-19`](../../static/js/modules/backup-center.js#L12-L19):

```
let pendingActionGeneration = 0;
```

Incremented **once** in `clearPendingAction()` (at [`:149`](../../static/js/modules/backup-center.js#L149),
beside `pendingAction = null`) and **once** in `showPendingAction()` (at
[`:709`](../../static/js/modules/backup-center.js#L709), beside `pendingAction = type`). Those are the
state machine's only two writers (§0.1), so **every** transition of intent — from any of the six call
sites, the Cancel binding, or a fresh Restore/Delete click — moves the counter. This is the
authorization token; the id comparison alone is not one.

**(B) One new module-private helper**, placed immediately after `showPendingAction()` at
[`:741`](../../static/js/modules/backup-center.js#L741):

```
function reassertPendingRestore(capturedGeneration, capturedBackupId) { … }
```

It re-asserts **only if all four hold**, and reports the failure rather than swallowing it:

1. `pendingActionGeneration === capturedGeneration` — **the authorization check.** Any user gesture during the flight moves it, so a mid-flight Cancel, Delete, Restore or list-click **blocks the re-assert**. This is the guard that closes A-B1 / T-B4 / P-B1, measured in §0.7(c).
2. `Number(selectedBackupId) === Number(capturedBackupId)` — `selectedBackupId` moves **synchronously** at [`:645`](../../static/js/modules/backup-center.js#L645), so this closes the list-click case that a details-object check cannot (A-B2, measured in §0.7(d)).
3. `selectedBackupDetails && Number(selectedBackupDetails.id) === Number(capturedBackupId)` — closes the case where the refresh landed on a *different* backup because the target vanished ([`:687-688`](../../static/js/modules/backup-center.js#L687-L688)). Conditions 2 and 3 are **both** required precisely because the two variables diverge.
4. On failure of **condition 3 specifically** — the target is gone — `showToast('warning', 'The backup you were restoring is no longer available. Please choose it again.')` per **P-N3** and **OD-5**. ⚠️ **The string is the owner's, pinned at Gate 1, and is not the implementer's to reword.** Failures of 1 and 2 are user-initiated and are **silent by design**: the user did something, and the app honouring it needs no announcement.

**Note (T-N5):** `showPendingAction()` also calls `clearInlineEditState()` at
[`:710`](../../static/js/modules/backup-center.js#L710), so a re-assert also tears down any inline
editor. Unreachable here — `renderBackupDetails()` has already repainted the detail pane — but stated,
because "nothing else changes" is one call deeper than it reads.

**(C) The save-first listener** ([`:1021-1052`](../../static/js/modules/backup-center.js#L1021-L1052))
becomes:

1. **Lock the flight**: call the module's existing `setDetailActionDisabled(true)` ([`:211-232`](../../static/js/modules/backup-center.js#L211-L232)), which disables all seven panel and detail controls **and** sets `pointerEvents:'none'` on `#backup-center-list`. Keep the existing spinner labels at [`:1029-1034`](../../static/js/modules/backup-center.js#L1029-L1034).
2. **Capture, before the first `await`**: `const capturedGeneration = pendingActionGeneration;` and `const capturedBackupId = selectedBackupDetails.id;`.
3. `createBackup(...)` and `showToast(...)` — **unchanged**.
4. `await refreshBackupCenter({ preserveSelection: true, preferredSelectionId: selectedBackupDetails?.id ?? capturedBackupId })` — ⚠️ **the captured-id substitution Plan v1 proposed is DROPPED (P-N4).** Forcing the selection back to the pre-click target would override a selection the user changed during the flow. The lock plus the counter make the substitution unnecessary.
5. `reassertPendingRestore(capturedGeneration, capturedBackupId);`
6. **Unlock**: `setDetailActionDisabled(false)`, in **both** the success tail and the `catch`.

**Why the lock is not sufficient alone, and the counter is not sufficient alone.** The lock does
**not** cover `#backup-sort` or `#backup-search` — `setDetailActionDisabled()`'s array covers seven
controls plus the list, and those two are absent — and §0.7(b) measured both live mid-flight. So the
counter is required. Conversely the counter alone would leave every affordance clickable and every
click silently discarded, which is a worse interaction than refusing the click. **Both.**

**Two consequences the implementer must not miss:**

- `clearPendingAction()` does **not** reset `#backup-action-cancel`'s `disabled` — compare [`:157-169`](../../static/js/modules/backup-center.js#L157-L169), where cancel is absent. **The handler owns that unlock.** Forgetting it leaves Cancel permanently dead; arm `u3` catches exactly that (T-N1).
- `:635` re-enables the confirm and save-first buttons mid-lock at [`:159`](../../static/js/modules/backup-center.js#L159) and [`:165`](../../static/js/modules/backup-center.js#L165). Harmless — `pendingAction` is `null` in that sliver and step 6 re-establishes the correct state — but it means the lock is not monotonic and must not be assumed so.

**(D) Per OD-3(b), decided**: after `showPendingAction()` has rebuilt the button, set it to the
`disabled` relabelled state. **Order matters** — `showPendingAction()` sets `disabled = false` at
[`:727`](../../static/js/modules/backup-center.js#L727) and rewrites `innerHTML` at
[`:728`](../../static/js/modules/backup-center.js#L728), so the "saved" state must be applied
**after**, never before. Per **A-N4** the label lives in **one module constant**, making it a seventh
writer of that button rather than a seventh scattered literal. **The constant's value is the owner's
exact string**, pinned at Gate 1:

```
const SAVE_FIRST_SAVED_LABEL = '<i class="fas fa-check" aria-hidden="true"></i> Current plan saved';
```

**(E) Per OD-6(a), decided**: `showPendingAction()` sets `role="alert"` on `#backup-action-confirm`
and moves focus to `#backup-action-cancel` — the **safe** control, never `#backup-action-confirm-btn`.
**Zero template edits.**

**(F) Per OD-5(a), decided** — ⚠️ **a new clause. Plan v2 as reviewed had none**, because the copy was
still undecided when it was written; the decision, not a reviewer, creates the production work.
`showPendingAction()` renders the snapshot-coverage note **from JS**, inside `#backup-action-confirm`
and **below** the warning paragraph `#backup-action-text`, in the **`restore` branch only** — the
`delete` branch has no save-first affordance and must not show it. The exact string is the owner's:

```
Saves the current workout plan only — logged sessions are not included in this snapshot.
```

Two constraints, stated because neither is obvious:

- **The node must be created idempotently.** `showPendingAction()` runs on every Restore click *and* on every re-assert, so an unguarded `insertAdjacentHTML` stacks a second and a third copy of the note on the same panel. Create-or-reuse by id, and set `textContent`.
- **[`templates/backup.html`](../../templates/backup.html) stays unmodified**, exactly as under (D) and (E). All three decided user-facing changes are applied from JS, which is what keeps the `templates/**` gate row and the visual matrix out of §v2.10.

**Nothing else changes.** `clearPendingAction()` and all **six** of its call sites are byte-identical
before and after. `showPendingAction()` gains one counter increment (plus (E) if chosen).
`refreshBackupCenter()`, `loadBackupDetails()`, `renderBackupDetails()`, `handleConfirmAction()`,
`handleSaveSubmit()` and the inline editor are untouched.

---

### v2.4 State transitions, enumerated

`G` = `pendingActionGeneration`, `C` = the captured `(generation, id)` pair.

| # | Event | Outcome | Why |
|---|---|---|---|
| 1 | click Restore | `pendingAction='restore'`, `G++` | panel visible |
| 2 | save-first → create resolves → refresh resolves, **no user gesture in flight** | **panel torn down, then re-asserted** | all four conditions hold — **the repair** |
| 3 | save-first → `createBackup` **rejects** | panel never torn down; `catch` restores the buttons; **lock released** | [`:1042-1050`](../../static/js/modules/backup-center.js#L1042-L1050) unchanged; arm `u10` |
| 4 | save-first → `fetchBackups` **rejects** | `renderEmptyDetail()` via [`:702`](../../static/js/modules/backup-center.js#L702) → `:538` → `G++`; no re-assert | condition 1 fails. The library could not be read, so no restore may be confirmed against it |
| 5 | save-first → `fetchBackupDetails` **rejects** | `renderDetailError()` → `:575` → `G++`; no re-assert | condition 1 fails; the error is already on screen |
| 6 | save-first → refresh resolves but the **target is gone**, selection falls to `y` | no re-assert **+ a warning toast** | conditions 2 and 3 fail. ⚠️ **The toast is new (P-N3)** — Plan v1 let this fail silently |
| 7 ⚠️ **NEW** | **Cancel during the flight** | Cancel is **locked** (v2.3 C.1). If it lands anyway, `G++` and **condition 1 blocks the re-assert** | A-B1 · T-B4 · P-B1; measured §0.7(c). Arm `u8` |
| 8 ⚠️ **NEW** | **Delete clicked during the flight** | Delete is **locked**. If it lands, `showPendingAction('delete')` moves `G` and **condition 1 blocks** | the delete→restore conversion A-B1 found |
| 9 ⚠️ **NEW** | **A different record clicked during the flight** | list `pointerEvents:'none'`. If it lands, `:891` moves `G` **and** `selectedBackupId` moves synchronously — **conditions 1 and 2 both block** | A-B2; measured §0.7(d). Arm `u7` |
| 10 ⚠️ **NEW** | **Sort / filter / search during the flight** | **not covered by the lock** — measured live in §0.7(b). Each reaches `:635` → `G++` → **condition 1 blocks** | why the counter is required, not optional |
| 11 ⚠️ **NEW** | Refresh resolved but its detail render was **superseded** by a concurrent `loadBackupDetails()` | `selectedBackupDetails` is stale; the concurrent path moved `G` → **condition 1 blocks** | the `:653-655` fourth terminal state (A-B2) |
| 12 | Cancel **after** the re-assert has settled | cleared, as today | [`:1059`](../../static/js/modules/backup-center.js#L1059) unchanged; arm `u3` |
| 13 | different record clicked after settle | cleared | `:891` **and** `:635` — §0.3 arm B |
| 14 | sort / filter / search after settle | cleared | `:635` alone — §0.3 arms C, D, E; arms `u4`, `u5`, `u6` |
| 15 | Confirm Restore after the re-assert | **the restore executes** | `pendingAction` non-null again, so [`:809`](../../static/js/modules/backup-center.js#L809) passes — **the acceptance criterion**; arm `u2` |
| 16 | `pendingAction === 'delete'` at capture time | save-first is `hidden` ([`:736`](../../static/js/modules/backup-center.js#L736)); unreachable | the helper re-asserts `'restore'` only |

**Rows 7–11 are the five states Plan v1 did not model.** Each is now closed twice over — by the lock
and by the counter — except row 10, which the lock does not reach and the counter alone closes.

---

### v2.5 Behavioral invariants

**Must change (the packet's purpose):**

- **I1.** After a save-first that succeeds with **no user gesture in flight**, the restore confirmation is present and armed, and confirming executes the restore the user originally initiated.

**Must not change (proved by arm, not by assertion):**

- **I2.** Cancel clears the pending action. *(arm `u3`; §0.3 arm A)*
- **I3.** Selecting a different record clears it. *(§0.3 arm B)*
- **I4.** Sort, filter and search each clear it, **with the selection unchanged**. *(arms `u4`, `u5`, `u6`; §0.3 arms C, D, E)*
- **I5.** A restore is **never** re-armed across an async gap in which the user did anything. *(arms `u7`, `u8`; the principle behind rows 7–11)*
- **I6.** A restore confirmation is never re-asserted against a backup the user did not confirm against. *(arm `u9`)*
- **I7.** Backup create, restore, delete and the erase flow behave exactly as today. *(the 22 surviving pre-existing tests; `erase-flow.spec.ts`)*
- **I8.** `showAutoBackupBanner()` is unchanged — structurally, since `program-backup.js` is not edited. *(§0.6; `erase-flow.spec.ts` as the behavioral control)*
- **I9.** The failure paths behave as today: create-rejects leaves the panel up and the buttons restored. *(arm `u10`)*
- **I10.** No `/api/backups*` request, payload, status code or response shape changes. *(no server file is touched)*

---

### v2.6 Artifacts

⚠️ **Two PRs, two diffs — never summed** (A-B3, sharpened by the diff-stage review). Rows **1–7** are the **implementation** PR's diff, which does not exist yet. Row **8** is **this planning PR's**, already written. So:

- **This planning PR: 2 files** — row 7 (this document) and row 8 (the ledger rider). No production file, no test file, no configuration file. **The Gate 1 signature did not move this count**: signing edits row 7 again, it does not add a row.
- **The implementation PR: 7 files** — rows 1–7, plus **ledger row 14**, which its own merge mints. ⚠️ **Re-derived against the four decisions, and still 7.** OD-3(b), OD-5(a) and OD-6(a) are each applied from JS inside row 1, and OD-1(i) creates nothing — so no decision adds an eighth path, and in particular none of them adds [`templates/backup.html`](../../templates/backup.html).

Row 7 appears in both, because both PRs edit this document. §v2.11's blast radius is the implementation PR's alone.

| # | Path | Change | Notes |
|---|---|---|---|
| 1 | [`static/js/modules/backup-center.js`](../../static/js/modules/backup-center.js) | modify | The whole production change: one counter, two increments, one helper, a rewritten save-first tail with lock/unlock. §v2.3. |
| 2 | [`e2e/program-backup.spec.ts`](../../e2e/program-backup.spec.ts) | modify | One `test.describe` appended (`u1`–`u11`), plus the mandatory `:155` deletion. **All eleven arms are mandatory** — `u11` stopped being conditional when the owner chose **OD-6(a)**. **Not** in `ci.yml`'s 25-spec list ([`:341-365`](../../.github/workflows/ci.yml#L341-L365)); it runs in its own **required** job, so extending it never approaches the `== 25` pin. |
| 3 | [`docs/UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md) | modify | Add **`KI-013`** — next after `KI-012` at [`:107`](../UI_SCENARIOS_GAP_ANALYSIS.md#L107) — per the file's rule at [`:109-112`](../UI_SCENARIOS_GAP_ANALYSIS.md#L109-L112). |
| 4 | [`docs/DUPLICATION_REGISTRY.md`](../DUPLICATION_REGISTRY.md) | modify | Row 10 ([`:49`](../DUPLICATION_REGISTRY.md#L49)) names its live residual as *"the refresh/confirm race, owned by **Packet U2**"*. Discharging it falsifies that present tense. **All five of its `backup-center.js` anchors — `:148-170`, `:172-183`, `:400-456`, `:580-637` and `:635` — were re-verified at `06a3f41` and are exact** — re-anchor by measuring after the diff, never by applying one drift figure. |
| 5 | [`docs/test_inventory/TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) | regenerate | Per-spec Playwright counts move. |
| 6 | [`docs/test_inventory/TEST_INVENTORY.md`](../test_inventory/TEST_INVENTORY.md) | regenerate | Same artifact, second file. **Counted separately here** — Plan v1 folded them into one row, which is part of how its "six paths" was wrong. |
| 7 | [`docs/backup_confirmation_continuity/PLANNING.md`](PLANNING.md) | modify | This document — the implementation record. |
| 8 | [`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md) | **already modified by THIS PR — not by the implementation PR** | ⚠️ **A-B3.** Ledger row 12, the sole authorized operational-documentation exception. See the *Operational rider*. **This planning PR's merge mints row 13**, which the implementation PR will carry as a rider; the implementation PR's own merge then mints **row 14**. |
| — | [`static/js/modules/program-backup.js`](../../static/js/modules/program-backup.js) | **not modified** | §0.6 — this is what makes clause 5's `showAutoBackupBanner()` guarantee structural. |
| — | [`templates/backup.html`](../../templates/backup.html) | **not modified** | ⚠️ **Re-derived against the decisions, and it holds.** All **three** decided user-facing changes — **OD-3(b)**'s relabel, **OD-5(a)**'s note and **OD-6(a)**'s `role` plus focus move — are applied from JS (§v2.3 D, F, E). Keeps `templates/**` and the visual matrix out of the gate set. |
| — | [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) | **not modified** | No new spec file. |
| — | [`e2e/fixtures.ts`](../../e2e/fixtures.ts) | **not modified** | Raw selectors are deliberate for a single-spec block. |
| — | `static/js/modules/__tests__/backup-center.test.js` | **not created** | Listed so the omission stays deliberate and visible. **Decided at Gate 1 — OD-1 (i)**, with no follow-up packet or rider booked. §0.4. |

**Effort**: **M** — Plan v1 said S; the lock, the counter, five new states and five new arms move it.
**Owner**: implementation agent, after Gate 1 sign-off **and** after this planning PR merges.
**Depends on**: **OD-1**, **OD-3**, **OD-5**, **OD-6** — **all four answered on 2026-08-26**. The only remaining precondition is this planning PR's merge.

---

### v2.7 Migration notes required in the implementation PR body

Per [`CLAUDE.md`](../../CLAUDE.md) §1's refactor invariant — U2 changes user-facing behavior in a core
workflow (backup/restore):

1. **What changed**, with §0.2's before/after table.
2. **What did not** — §v2.5's I2–I10, named individually.
3. **The `:155` deletion**, with the **measured** bistability evidence §v2.13 requires — not the argument.
4. **The mid-flight lock** as a deliberate interaction change: seven controls and the list become inert for the duration of the snapshot. This is new behavior, not a bug fix, and it is what closes the destructive-resurrection defect.
5. **The `preferredSelectionId` substitution considered and rejected** (P-N4), and why.
6. **Why no `.py` and no route changed** — a client-state fix; the server was never involved.
7. **The `KI-013` and `DUPLICATION_REGISTRY` row-10 edits**, scoped and justified.
8. **The OD-1 omission**: no Vitest file, by owner decision — **OD-1 (i), 2026-08-26** — citing Q3 and the window. State also that **no follow-up packet and no rider is booked**, which the owner directed explicitly, so a later reader does not read the omission as an oversight.
9. **Ledger row 13** — minted by the *planning* PR's merge and carried here as a rider. This PR's own merge then mints **row 14**, owed by whoever lands it.
10. ⚠️ **Three new user-facing strings on a destructive flow**, each pinned by the owner at Gate 1 and **none of them the implementer's to reword**: the `Current plan saved` relabel (**OD-3(b)**), the snapshot-coverage note (**OD-5(a)**), and the state-6 warning toast (**OD-5**, bundled). Quote all three verbatim in the PR body, and say that the snapshot-coverage note discloses a pre-existing asymmetry (§0.8) rather than repairing it.
11. ⚠️ **The OD-6(a) announcement and focus move** — `role="alert"` on `#backup-action-confirm`, and focus placed on `#backup-action-cancel`. This is a deliberate focus change on a destructive confirmation, chosen so the keyboard user lands on the **safe** control; it must not be described as incidental.

---

### v2.8 The regression arms

All in [`e2e/program-backup.spec.ts`](../../e2e/program-backup.spec.ts), one appended `test.describe`.
**No `page.waitForTimeout` anywhere** — the inventory pins `waitForTimeout` lines per file (82 across
14 files in total), and this file must read **zero delta**. Both oracle constructions below need zero
timers.

**⚠️ The oracle (T-B1).** Plan v1 sampled panel
state after `expectToast`. **That cannot work**: `expectToast` resolves at
[`:1039`](../../static/js/modules/backup-center.js#L1039), before `refreshBackupCenter()` is entered
(§0.7(a)), so the assertion sees the **pre-teardown** panel and passes on a mutant that never
re-asserts. Worse, `showPendingAction()` rebuilds the panel **byte-identically**, so under OD-3(a)
**no DOM state distinguishes "never torn down" from "torn down and rebuilt"**.

⚠️ **Re-derived against OD-3(b), and the oracle is KEPT — but its second argument is withdrawn.** The
decision *does* create a discriminating end state: after a re-assert the save-first button is
`disabled` and reads `Current plan saved`, which a never-torn-down panel would not. So the
byte-identical sentence above no longer holds under the decided design. **That does not rescue the
state sample**, because the *first* defect is independent of it — `expectToast` resolves two round
trips early, so a sample taken there reads the panel before the M1 mutant has finished doing nothing,
and passes. Only a transition oracle observes the **ordering**. The `Current plan saved` end state is
asserted too, in `u1`, as an **assertion** rather than as the oracle.

**Arms `u1`, `u2`, `u7`, `u8` therefore use a transition oracle, not a state sample:**

```
// installed BEFORE the save-first click
new MutationObserver(...).observe(panel, {attributes:true, attributeFilter:['hidden']})
  -> pushes each panel.hidden value into a window-scoped array
// then
await page.waitForFunction(() => window.__u2?.length >= 2)
expect(recorded).toEqual([true, false])      // torn down, then re-asserted
```

Per **T-NB2**, `tsconfig.json`'s `strict: true` over `e2e/**/*.ts` requires a
`declare global { interface Window { __u2?: boolean[] } }` block — an implicit `any` reds `Type Check`.

| Arm | Drives | Asserts | Kills |
|---|---|---|---|
| **`u1`** | restore → save-first, transition oracle installed first | recorded sequence `[true, false]`; title `Confirm restore`; text contains `logged sessions will be cleared`; confirm button contains `Confirm Restore`; **the OD-5(a) note reads** `Saves the current workout plan only — logged sessions are not included in this snapshot.`; **and (T-NB7)** the two spinner-locked buttons in their **decided** end states — ⚠️ **inverted for save-first by OD-3(b)**: `#backup-action-confirm-btn` `toBeEnabled()` and labelled `Confirm Restore`, `#backup-restore-save-first` **`toBeDisabled()`** and labelled `Current plan saved` (**not** `toBeEnabled()`, as this row read before the decision) | **M1** — by timeout, since only `[true]` is ever recorded |
| **`u2`** | `u1`, then click **Confirm Restore** | the restore executes: success toast, `#backup-restore-result` populated | a cosmetic fix that shows the panel but leaves `pendingAction` null, so [`:809`](../../static/js/modules/backup-center.js#L809) early-returns. **`u1` alone cannot see this** |
| **`u3`** | `u1`, then **Cancel** | panel hidden | **not vacuous under Plan v2** (T-N1): the lock disables `#backup-action-cancel` and `clearPendingAction()` never resets that button's `disabled`, so a forgotten unlock leaves Cancel dead. `u3` catches it |
| **`u4`** | restore pending (settled) → change `#backup-sort` | panel hidden; **selection unchanged** | Design 0; a mis-scoped guard. §0.3 arm C |
| **`u5`** | restore pending → click a filter **whose predicate the selected backup satisfies** | panel hidden; **selection unchanged** | ⚠️ **A-N2**: a non-matching filter takes [`:910-911`](../../static/js/modules/backup-center.js#L910-L911) and degrades the arm into a selection-change test. §0.3 arm D |
| **`u6`** | restore pending → type a substring **of the selected backup's own name** | panel hidden; **selection unchanged** | ⚠️ **A-N2**: a non-matching string takes [`:960-961`](../../static/js/modules/backup-center.js#L960-L961) and inherits `:155`'s vacuity. §0.3 arm E. **This is `:155`'s honest replacement** |
| **`u7`** ⚠️ NEW | `page.route` holds `GET /api/backups`; click save-first; **click another record while held**; release | panel **stays hidden**; no re-assert | state 9 · A-B1(3) · A-B2 |
| **`u8`** ⚠️ NEW | same hold; **press Cancel while held**; release | panel **stays hidden** | **state 7 — the destructive-resurrection defect.** A-B1 · T-B4 · P-B1 |
| **`u9`** ⚠️ NEW | `page.route` fulfils `GET /api/backups` **omitting the captured id** | panel **not** visible; `#backup-detail-name` shows the fallback backup; the **warning toast** appears | **M2** — ⚠️ **T-B3**: Plan v1 called this unkillable; `page.route` is used 4× in this file already |
| **`u10`** ⚠️ NEW | `route.fulfill` a **500** on `POST /api/backups` | panel still visible; both buttons re-enabled and re-labelled from `originalSaveFirstHtml` / `originalConfirmHtml`; **lock released** | ⚠️ **T-NB6**: the only guard on §v2.3's "nothing else changes" — an implementer who moves the capture inside the `try` breaks the untouched `catch` and nothing else notices |
| **`u11`** ⚠️ NEW, **mandatory per OD-6(a)** | `u1`, then read `document.activeElement` | focus is on `#backup-action-cancel`; `#backup-action-confirm` has `role="alert"` | **P-B3** — clause 3 for a keyboard user *is* focus continuity |

**The [`:155`](../../e2e/program-backup.spec.ts#L155) disposition — MANDATORY.** Its enclosing test
keeps its subject (save-first creates a snapshot) and `:155` is **deleted**. ⚠️ **Plan v1's
"alternative if a reviewer prefers no deletion" is STRUCK (T-B2)**: inverting `:155` to
`toBeVisible()` above `:153` places it immediately after `expectToast` — precisely the false-green of
T-B1 — and it would pass on the M1 mutant. `u6` carries the search-clears claim in a state where it
can fail; `u1` carries the visibility claim through a transition oracle.

---

### v2.9 Mutation matrix

Each applied alone to the **implemented** branch, reverted before the next. Results are **measured and
recorded**, never carried forward as predictions.

| # | Mutation | Predicted red | Predicted green | Proves |
|---|---|---|---|---|
| **M1** | Delete the `reassertPendingRestore(...)` call | `u1` (oracle timeout), `u2` | `u3`–`u11` | The repair is load-bearing, and `u4`–`u6` are **not** measuring it. ⚠️ Re-predicted under the new oracle (T-B1) |
| **M2** | Drop condition 3 (the target-identity check) | **`u9`** | others | ⚠️ **T-B3**: killable after all. Plan v1's "deliberate gap" was giving up early |
| **M3** | Drop condition 1 (the **generation** check) | **`u8`**, **`u7`** | `u1`–`u6`, `u9`–`u11` | **The destructive-resurrection guard is load-bearing.** If this row does not red, the packet has not fixed what the council found |
| **M4** | Drop condition 2 (`selectedBackupId`) | **`u7`** | others | The two selection variables genuinely diverge (§0.7(d)); condition 3 alone does not cover it |
| **M5** | Remove `setDetailActionDisabled(true)` (keep the counter) | *(none — the counter still blocks)* | all | **Deliberate and recorded.** Proves the two guards are **independent**, not redundant, and that the counter is the load-bearing one. Removing *both* is M3 |
| **M6** | Forget `setDetailActionDisabled(false)` in the success tail | **`u3`** | others | The unlock is load-bearing; `clearPendingAction()` never resets Cancel's `disabled` (T-N1) |
| **M7** | Delete `clearPendingAction()` at [`:635`](../../static/js/modules/backup-center.js#L635) | **`u4`**, **`u5`**, **`u6`** | `u1`, `u2` | ⚠️ **T-N2**: **the mutation that actually tests §0.3's attribution.** Plan v1's "M3 not applicable" confused mutating shipped code with proving the arms discriminate |
| **M8** | Delete `clearPendingAction()` at [`:891`](../../static/js/modules/backup-center.js#L891) | *(none expected)* | all | ⚠️ Kept with **corrected reasoning** (T-N2): `:891` clears synchronously and `:635` clears after the fetch, so the **terminal state is identical** — this is a timing mutation with no terminal observable, not a control on §0.3's attribution. M7 is that control |
| **M9** | Move the capture **inside** the `try`, after `createBackup` | **`u10`** | others | The `catch` at `:1042-1050` stays correct (T-NB6) |
| **M10** | Change the helper's type guard so `'delete'` also re-asserts | *(none)* | all | ⚠️ **T-N3**: **unreachable through the UI**, not equivalent — save-first is `hidden` for `delete` at [`:736`](../../static/js/modules/backup-center.js#L736) and `locator.click()` requires visibility. `dispatchEvent` would reach it. Recorded honestly |
| **M11** | Revert the `:155` deletion **and** delete `u6` | *(none)* | all | Evidence for §0.5's claim that the two are not equivalent oracles. Run once for the PR body, not as a standing gate |

**Rule (§4.5 honesty rule):** an unkillable mutation is recorded as a gap **with the reason**, never
quietly dropped. M5, M8 and M10 are the three here, and each says which it is.

---

### v2.10 Gates

⚠️ **Three omissions from Plan v1 repaired.** Derived as the **union** over every changed path, using
[`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)'s change-type table **and** its targeted-test
derivation step — which Plan v1 skipped by reasoning "no `.py` is touched".

| Changed path | Row | Gate |
|---|---|---|
| `static/js/modules/backup-center.js` | Frontend (JS), [`:30`](../ai_workflow/QUALITY_GATE.md#L30) | feature-map specs ([`:128`](../ai_workflow/QUALITY_GATE.md#L128) → `program-backup.spec.ts`) + manual smoke |
| `static/js/modules/backup-center.js` | **targeted-test derivation** | ⚠️ **T-NB1** — [`tests/test_css_cascade_contracts.py:259`](../../tests/test_css_cascade_contracts.py#L259) reads this file and asserts a literal substring in it |
| `e2e/program-backup.spec.ts` | E2E spec | run the spec |
| `e2e/program-backup.spec.ts` | **`tsconfig.json` `include` + `strict`** | ⚠️ **T-NB2** — `Type Check` is **derived**, not a bystander |
| `e2e/program-backup.spec.ts` | drift surface, [`:59`](../ai_workflow/QUALITY_GATE.md#L59) | ⚠️ **T-N4** — per-spec Playwright counts. The **trigger** is the spec edit; the artifact is the **remedy** |
| four `docs/*.md` | Product docs only | none — and **verified**, not assumed: `--check` returned *"Test inventory is up to date"*, exit 0, with this new directory present |

**The union, as commands:**

1. `.venv/Scripts/python.exe scripts/generate_test_inventory.py` — regenerate and commit; verify with `--check` before pushing. Per-spec Playwright counts move; **`waitForTimeout` lines must not**. Never regenerate while an untracked or gitignored `.md` sits in a globbed surface directory.
2. `.venv/Scripts/python.exe -m pytest tests/test_css_cascade_contracts.py -q` ⚠️ **NEW.**
3. `npx tsc --noEmit` ⚠️ **NEW** — required and derived.
4. `npx playwright test e2e/program-backup.spec.ts --project=chromium` — the exact command the **required** `E2E Backup (Chromium, isolated)` job runs ([`ci.yml:465`](../../.github/workflows/ci.yml#L465)).
5. `npx playwright test e2e/erase-flow.spec.ts --project=chromium` — ⚠️ **relabelled per T-NB4**: a **discretionary clause-5 control**, not table-derived. Kept because "the file was not edited" and "the behavior did not change" are different claims. Its context, `E2E Erase Flow (Chromium, isolated, non-required)`, **is required in branch protection despite the suffix** — one of the two deliberate false "(non-required)" labels.
6. `npx playwright test e2e/accessibility.spec.ts --project=chromium` — ⚠️ **relabelled per T-NB4**: a **discretionary tripwire**. The fix changes nothing at rest, so the axe pins at [`:841-842`](../../e2e/accessibility.spec.ts#L841-L842) (`backup:light` / `backup:dark`, `color-contrast`, `nodes: 2` each) **cannot** move — which is exactly what makes it a useful tripwire if the implementation drifts into `backup.html`. ⚠️ **Now REQUIRED, not discretionary**: **OD-6(a)** is decided and adds a `role`, and **OD-5(a)** adds a copy node. Both live inside `#backup-action-confirm`, which is `hidden` at rest, so the pins are still predicted **unmoved** — and this arm's job is now to **prove** that rather than to assume it.
7. **Full `pytest` — NOT required**, and this is now derived rather than asserted: no `routes/**`, `app.py`, DB/schema file, `utils/**`, `templates/**`, `scss/**`, `static/css/**`, `scripts/**`, `.github/workflows/**` or `tests/conftest.py`; no new blueprint and no new table. One targeted pytest file, per step 2.
8. `npm run build:css` — **not run, and must not be.** No `scss/**` or `static/css/**` edit; running it locally is the documented cause of the phantom-modification red.
9. **Manual interactive smoke** — ⚠️ **extended per P-NIT**: §0.2's procedure **cannot reach any in-flight state**, so it may not simply be inherited. It must additionally exercise Cancel, Delete, a list click and a sort change **during** the snapshot request (throttled network or a paused route).

**Reviewers**: `code-reviewer` and `unslop-reviewer` on the staged implementation diff. The
change-type table requires none for `static/js/**`; Plan v2 requires both anyway, because this packet
adds a guard on a destructive path.

**Branch-protection context set, measured this session** — 12 required contexts, of which four are
touched by U2's run set: `E2E Backup (Chromium, isolated)`, `E2E Erase Flow (…, non-required)`,
`Test Inventory Drift`, `Type Check (tsc blocking + pyright measure-only)`.
`JS Unit (Vitest, non-required)` is **not** among the 12 — D2 remains unsigned, which is the
background to OD-1.

---

### v2.11 Scope containment, blast radius, rollback

**Blast radius of the implementation PR: seven files** (§v2.6 rows 1–7), of which **one** is production code and **one** is a test file. **This planning PR's own blast radius is two documentation files** and is not counted here. `clearPendingAction()` and all **six** of its call sites are byte-identical before and
after.

**Rollback — any one of these: revert the whole packet, do not patch forward:**

1. `u4`, `u5` or `u6` reds → §0.3's attribution is wrong and the design's premise is falsified.
2. `u7` or `u8` reds → the resurrection guard does not hold. **Non-negotiable**: this is the destructive-safety guard.
3. `M7` fails to red `u4`/`u5`/`u6` → the arms are not discriminating and the suite is a false green.
4. `erase-flow.spec.ts` reds → clause 5 is broken by an unpredicted mechanism.
5. `accessibility.spec.ts` node counts move → the accessible tree changed at rest.
6. `Test Inventory Drift` reds on a surface **other than** per-spec Playwright counts.
7. Any of the **22** surviving pre-existing tests in `program-backup.spec.ts` reds — `:155` is an *assertion*, not a test, so deleting it removes no test — ⚠️ **carve-out (T-B5): [`program-backup.spec.ts:79`](../../e2e/program-backup.spec.ts#L79) is a documented known-red** ([`QUALITY_GATE.md:224`](../ai_workflow/QUALITY_GATE.md)). If it reds, re-run it **in isolation** and record the result; it does not trigger rollback. **The citation survives this edit**: `:155` is deleted (shifting only lines > 155) and the new block is appended, so `:79` stays `:79`.

**Revert mechanics**: `git revert` of the **implementation** PR's squash commit restores all seven of its files. It does **not** reach ledger row 12, which belongs to this planning PR's commit — and must not be reverted with it in any case: a ledger row records a `main` run that happened and stays true regardless of what the code does afterwards. No DB
migration, no schema change, no persisted state, no server change. ⚠️ **The OD-3(a) caveat is
discharged by the decision**: the owner chose **(b)**, so U2 does not make duplicate
`Pre-restore snapshot` rows an expected outcome of the flow. The general point survives in a smaller
form — any snapshot a user did create is **user data** and **persists through a revert**, as every
backup always has.

---

### v2.12 Residual risks

1. ⚠️ **DELETED.** Plan v1's "state 6 has no automated arm" is closed by arm `u9` (T-B3).
2. **The `pendingAction` machine keeps 0 % unit coverage** — owner ruling Q3 (§0.4). ⚠️ **Decided, not pending: OD-1 (i)**, and with **no follow-up packet and no rider booked**, by explicit owner direction. The generation counter and the re-assert guard ship with E2E coverage only, and reviving this module's unit coverage would need a future packet with its own Gate 0.
3. **The mid-flight lock is a real interaction change.** For the duration of the snapshot request, seven controls and the library list are inert. On a slow connection that is a visible freeze. It is the price of not re-arming a destructive confirmation, and §v2.7 requires it in the migration notes rather than shipping it quietly.
4. **`#backup-sort` and `#backup-search` are outside the lock** (§0.7(b)) and are covered by the generation counter alone. Deliberate: adding them to `setDetailActionDisabled()` would change a shared helper used by other paths, widening the blast radius for no additional safety.
5. ⚠️ **CLOSED by OD-6(a).** The confirmation is announced (`role="alert"`, set from JS in `showPendingAction()`) and focus lands on `#backup-action-cancel`, the safe control. **One narrower limit is recorded rather than dropped**: the `role` is applied by JS, not by [`backup.html`](../../templates/backup.html), so it exists only from the moment `showPendingAction()` first runs — the panel's own markup stays un-annotated, and annotating it is a template edit U2 deliberately does not make.
6. ⚠️ **CLOSED by OD-5(a).** The affordance now states its own limit on screen, in the owner's words. **The underlying asymmetry is disclosed, not repaired, and is not U2's to repair**: `create_backup()` still covers `user_selection` only while the restore it guards deletes `workout_log` too (§0.8).
7. **Pre-existing and NOT repaired here (P-N1):** the snapshot stamp is **UTC** ([`:1037`](../../static/js/modules/backup-center.js#L1037)) while `formatDate()` renders **local** time ([`:47`](../../static/js/modules/backup-center.js#L47)), so for any non-UTC user the name and the rendered date disagree. U2 does not introduce this and, per **OD-3**'s sub-question, does **not** add sub-second resolution either. ⚠️ **Re-derived against OD-3(b)**: the duplicate-row case that made this sharp is now the exception rather than the flow's expected outcome — but it is not gone, because (b)'s `disabled` state is not durable and a cancel / re-open cycle re-enables the button. Recorded for that residual case.
8. **`program-backup.spec.ts` is not in the 25-spec required functional shard.** It is guarded by its own required job — stronger for this packet — but a reader checking the shard list will not find it.

---

### v2.13 Evidence obligations — things the implementation must MEASURE, not assert

1. **The `:155` bistability.** Run the **unmodified** `:139-156` test **20 times** against the patched branch **before** deleting `:155`, and record the pass/fail split. T-B2 derived the race from source order; nobody has executed it. If it comes back 20/20 green, T-B2's mechanism is wrong and §0.5's second correction must be re-derived before the deletion is justified.
2. **The zero-frame claim.** §0.7(a) measures that the teardown is the last event and predicts no intervening paint. Re-measure **on the implemented branch** with a frame counter across `hidden: true → false` and record the frame count. A non-zero count reopens **OD-2**.
3. **Every mutation result**, as measured exit codes — ⚠️ Vitest and Playwright can both print "N passed" while exiting non-zero; **judge each row by exit code**, never by the summary line.
4. **The re-anchored `DUPLICATION_REGISTRY` row 10 citations**, measured against the shipped file as the **last** edit. Drift is banded, not one number.

---

### v2.14 Predicted counts — derived, not pinned

⚠️ Per **T-NB5**, stated as arithmetic so a later arm addition does not read as a broken prediction.

⚠️ **RE-DERIVED AT GATE 1.** Every base figure below was **re-read from
[`TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) at `06a3f41` in the signing session**,
not carried forward from Plan v2's pre-decision text. **OD-6(a) makes `u11` mandatory**, so the
conditional "(or 33)" form is gone and each line now carries **one** derived figure.

- `program-backup.spec.ts`: **22** today − **0** deleted tests (`:155` is an *assertion*, not a test) + **11** arms (`u1`–`u11`) = **33**. *(The base was measured two independent ways and they agree: `specs[16].tests = 22` in the inventory, and **22** `test(` declarations in the spec file.)*
- `playwright.total_tests`: **662** → **673**. *(662 re-read from the inventory.)*
- `playwright.total_spec_files`: **33**, unchanged — no new spec file.
- `hard_waits.total_lines`: **82** across **14** files, **unchanged** — no arm uses `waitForTimeout`, and this spec contributes **0** today (measured).
- `vitest.total_files` / `total_cases`: **13 / 231**, **unchanged** — the **OD-1 (i)** evidence.
- `Required functional gate`: **527** across **25** specs, unchanged — the inventory records `in_required_functional_set: false` for this spec.

**The three decided strings and the focus move add no spec file and no arm.** They are asserted inside
arms this count already contains: `u1` carries the two panel strings, `u9` the warning toast, `u11`
the announcement and the focus target.

| Gate | Expectation |
|---|---|
| `E2E Backup (Chromium, isolated)` | green, **22 → 33** |
| `Test Inventory Drift` | green after regeneration |
| `E2E Erase Flow` | green, unchanged |
| `E2E Functional (Chromium)` | green, unchanged |
| `Type Check` | green — **derived, not a bystander** |
| `Run Tests` (pytest) | green, unchanged |
| `JS Unit (Vitest, non-required)` | green, **unchanged at 13 / 231** |

---

### Sequence

1. ✅ **DONE — 2026-08-26.** Owner answered **OD-1 (i)**, **OD-3 (b)**, **OD-5 (a)** and **OD-6 (a)**. (OD-2 retired, OD-4 demoted — neither needed an answer.)
2. ✅ **DONE — 2026-08-26.** Plan v2 amended against those answers, and every restatement re-derived. ⚠️ **Amending a criterion falsifies every restatement of it**, so this document was grepped for restatements before the amendment was called done. **Two were falsified rather than merely confirmed**, and both are marked ⚠️ where they live: `u1`'s "both buttons `toBeEnabled()`" (T-NB7, inverted for save-first by OD-3(b)), and §v2.8's "no DOM state distinguishes" oracle rationale (narrowed by the same decision). A third consequence had no restatement to amend at all — **OD-5(a) needed a production clause Plan v2 did not have**, which is why §v2.3 gains **(F)**.
3. ✅ **Gate 1 SIGNED — 2026-08-26** (*Sign-off*). ⚠️ **This planning PR has NOT merged**, and that merge is the one remaining precondition. Steps 4 onward are unstarted.
4. Fresh worktree on `main` as it stands at that time.
5. Arms `u1`–`u11` written **first** and observed: `u1`, `u2`, `u7`, `u8`, `u9`, `u10` must **red** against unchanged code; `u3`–`u6` must be **green** (they encode existing behavior).
6. §v2.13 obligation 1 — the 20-run `:155` measurement — **before** the deletion.
7. Production change (§v2.3).
8. Mutations **M1–M11** executed; measured results recorded, predictions replaced.
9. Gates §v2.10 steps 1–6 and 9; §v2.13 obligation 2.
10. `code-reviewer` + `unslop-reviewer` on the staged diff.
11. PR with §v2.7's migration notes, and **ledger row 13** as a rider. **Do not merge without explicit owner confirmation naming the PR.**

---

## Sign-off

### GATE 1 — SIGNED 2026-08-26

**The owner approved Plan v2 on 2026-08-26**, deciding all four open questions and directing that the
plan be amended against them with **no further amendments**. **No production file, no test file and no
configuration file has been changed by this PR** — its entire diff is this planning document plus the
ledger row recorded below, and the signature did not change that.

**All four decisions selected the option Plan v2 recommended.** That is recorded because it is
evidence about the *plan*, not a reason to have skipped the derivation: every count, gate, risk and
conditional branch below was re-derived against the **decisions**, and two restatements came back
falsified.

| Decision | Answer | Exact copy pinned by the owner |
|---|---|---|
| **OD-1** — coverage tier | **(i) E2E-only.** ⚠️ **No Vitest follow-up is added and none is scheduled** — (iii) is **declined, not deferred**. | — |
| **OD-3** — save again after save-first | **(b) disable and relabel.** Sub-second stamp resolution: **NO**. | `Current plan saved` |
| **OD-5** — snapshot-coverage copy | **(a) state the limit.** | `Saves the current workout plan only — logged sessions are not included in this snapshot.` |
| **OD-5** — state-6 warning toast (bundled) | **Required**, wording pinned. | `The backup you were restoring is no longer available. Please choose it again.` |
| **OD-6** — announcement and focus | **(a) announce, and place focus on Cancel.** | — |

**OD-2** is retired by measurement and **OD-4** is demoted; neither needed an answer.

**The three strings and the focus target are signed criteria, not implementation choices.** An
implementer who rewords any of them, or who focuses `#backup-action-confirm-btn` instead of
`#backup-action-cancel`, is changing a signed criterion.

**What is authorized is exactly Plan v2 as amended here** — the **seven** changed paths in §v2.6's
Artifacts table, the **eleven** arms in §v2.8, the **eleven-row** mutation matrix in §v2.9, the gate
set in §v2.10 with `accessibility.spec.ts` now required, and the four evidence obligations in §v2.13.
Nothing else.

**Implementation becomes authorized only after this signed planning PR merges successfully.** Signing
is not the authorization; the merge is. Until `docs/u2-gate1-plan` is on `main`, no production code,
no test code, no edit to [`backup-center.js`](../../static/js/modules/backup-center.js) and no edit to
[`program-backup.spec.ts`](../../e2e/program-backup.spec.ts) is authorized.

```
GATE 1 — Packet U2 — Backup "save first" confirmation continuity
Owner: Yaakov Avihai Shai            Date: 2026-08-26

OD-1  [x] (i) E2E-only   [ ] (ii) Vitest now   [ ] (iii) separate deferred packet
      -> and no Vitest follow-up is added or scheduled
OD-3  [ ] (a) leave enabled   [x] (b) disable + relabel: "Current plan saved"
      [ ] (c) hide       sub-second stamp? [ ] yes  [x] no
OD-5  [x] (a) state the limit:
          "Saves the current workout plan only — logged sessions are not included in this snapshot."
      [ ] (b) ship without      [ ] (c) rename the button
      state-6 warning toast (bundled, required):
          "The backup you were restoring is no longer available. Please choose it again."
OD-6  [x] (a) announce + focus Cancel   [ ] (b) announce only   [ ] (c) neither

Plan v2 approved as written / as amended above:  [x] yes   [ ] no
```

**What this signing leaves stale elsewhere — flagged, not edited.** This signing session was
authorized to modify **this file only**, so nothing below is repaired here.
[`OPEN_WORK_EXECUTION_PLAN.md:155`](../OPEN_WORK_EXECUTION_PLAN.md#L155) reads
`**Status:** Execute — ready to enter its **own** Gate 1`. U2 has now entered that gate **and passed
it**, so the line is stale from this moment — not from U2 shipping, which is how the
*Flagged, not edited* section below had it before this signing. §4's per-packet gating blockquote at
[`:218-225`](../OPEN_WORK_EXECUTION_PLAN.md#L218-L225) is **not** stale: it is framed as the gates each
packet *owes*, and a "gates it owes" framing survives a gate being passed. Repairing the `Status:`
line belongs to a status-reconciliation packet, and it is **owner action owed**.

---

## Operational rider — JS-unit ledger row 12

⚠️ **This section exists because A-B3 found it referenced and missing.**

**This PR carries one edit outside U2's planning scope**, by explicit owner authorization: the next
sequential row of the JS-unit qualification ledger in
[`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md) §13.0. The owner authorized it
as **"the sole narrow operational-documentation exception"** and directed that any further file
wanting an update be **flagged rather than edited**. §*Flagged, not edited* below does that.

**Why the row was owed.** PR [#423](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/423)
carried row 11 and merged as squash `06a3f41` at `2026-08-26T10:43:48Z`. **A ledger block can never
record the `main` run its own merge produces**, so #423 left row 12 owed. This PR is the next to open,
so it is the rider — the same mechanism that produced rows 6 through 12.

**Row 12, measured at job level** (read at `2026-08-26T12:05:47Z`, from the GitHub API response `Date`
header, not the host clock):

| Field | Value |
|---|---|
| `main` run | [`32959719238`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32959719238) |
| Event / head | `push` / `06a3f41` (PR #423) |
| `js-unit` job | [`98149159459`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32959719238/job/98149159459) |
| Job `status` / `conclusion` | `completed` / **`success`** |
| Job `completed_at` | **`2026-08-26T10:44:17Z`** |
| Run jobs | 18/18 |

**No run's overall conclusion was used as a proxy.** The job object was fetched from
`/actions/runs/32959719238/jobs` and its `status`, `conclusion` and `completed_at` read off **that
job**. The run's overall conclusion is also `success`; that fact was measured and **not** used.

**All eleven prior rows were re-derived from the API and returned byte-identical.** The superset query
(`created_at >= 2026-08-22T17:00:00Z`, deliberately earlier than T0, across **every** workflow)
returned **16** `main` runs: **12** `CI/CD Pipeline` qualification attempts and **4** others — three
Dependabot `dynamic` runs and one `Deep Gate` `schedule` run — each re-enumerated and each returning
**zero** `JS Unit (Vitest, non-required)` jobs. They are **classified, not tallied**.

**T0 did not move, and the argument is not the one rows 7–11 used.** #423 is an implementation PR and
**does** change the production JS tree: `static/js` moved
`815ca75c109c93c0f914f36d0de24ba46a89bc3d` → **`bd703e800d512c21e32d6f03066cfe8080859f93`**. The
whole-tree identity those rows relied on is therefore **unavailable and is not claimed**. The
operative rule is **"changed no JS test case"**, satisfied by a narrower and stronger measurement:
`static/js/modules/__tests__` is **byte-identical** at
`9db6d8b2e9635755775b8c362f9bebbd750ff3c3` across `1243728 → 06a3f41`, and `vitest.config.js` is
unchanged at `c16ca428f7478708d8dd96a20ebcb86f98a8b935`. `TEST_INVENTORY.json` at `06a3f41` reads
`vitest.total_files = 13`, `vitest.total_cases = 231` — identical to `1243728`, while
`playwright.total_tests` moved **649 → 662** and `hard_waits.total_lines` held at **82**. **Q2's
restart clause did not engage. T0 remains `2026-08-22T17:59:26Z`; the strict mark remains
`2026-09-05T17:59:26Z`.**

**Ledger state after row 12:** **12** qualification attempts, **12** green, **0** red, **0** missing,
**0** skipped, **0** cancelled. **≈ 3 d 18 h 6 m** elapsed of the required **14 d**; **≈ 10 d 5 h
54 m** remaining.

**This PR's own merge will mint row 13**, and whoever merges it owes that row — which the U2 *implementation* PR will carry as its rider, before its own merge mints **row 14**.

### Flagged, not edited

Four documents carry ledger-row counts that are **already stale at `06a3f41`** — they were falsified
by rows 6 through 11, **before** this session. Row 12 does not newly falsify them. Per the owner's
instruction they are **flagged and left untouched**:

| Document | Stale claim | Live value |
|---|---|---|
| [`ACTIVE_DEVELOPMENT.md:62`](../ACTIVE_DEVELOPMENT.md) | *"the qualification ledger now holds **FIVE** rows"* | **12** |
| [`MASTER_HANDOVER.md:77`](../MASTER_HANDOVER.md) | *"now holds **FIVE** rows"* | **12** |
| [`MASTER_HANDOVER.md:187`](../MASTER_HANDOVER.md) | *"now holds **FOUR** rows"* | **12** |
| [`OPEN_WORK_EXECUTION_PLAN.md:9`, `:663`](../OPEN_WORK_EXECUTION_PLAN.md) | *"reconciled to **six** rows"* | **12** |
| [`TESTING_STRATEGY_PLANNING.md:30`](../TESTING_STRATEGY_PLANNING.md) | *"the ledger now holds **five** rows"* | **12** |

**These belong to a status-reconciliation packet, not to U2.** §13.0's own rule — *"the count still
lives in exactly one place"* — means each of these is a restatement that should not exist, and
repairing them is a scoped decision the owner should make deliberately.

Two other documents that name U2 are likewise not touched here, and ⚠️ **the Gate 1 signature moved
one of them from "when U2 ships" to "now"**:

- [`DUPLICATION_REGISTRY.md:49`](../DUPLICATION_REGISTRY.md) — row 10's live residual. Still falsified only **when U2 ships**, and the implementation PR owns it (§v2.6 row 4).
- [`OPEN_WORK_EXECUTION_PLAN.md:155`](../OPEN_WORK_EXECUTION_PLAN.md#L155) — Packet U2's `**Status:** Execute — ready to enter its **own** Gate 1` line. ⚠️ **Stale from 2026-08-26**, because U2 has now entered that gate and passed it. A status packet owns the repair; see the closing paragraph of *Sign-off*.

---

## See also

- [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4 Packet U2 ([`:152-181`](../OPEN_WORK_EXECUTION_PLAN.md#L152-L181)) — the authorization, and the per-packet gating at [`:218-225`](../OPEN_WORK_EXECUTION_PLAN.md#L218-L225)
- [`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md) §2.4 (owner ruling Q3), §6.5 (the window), §13.0 (the live ledger)
- [`volume_failure_feedback/PLANNING.md`](../volume_failure_feedback/PLANNING.md) — Packet U1, the sibling packet and the precedent for OD-1
- [`DUPLICATION_REGISTRY.md`](../DUPLICATION_REGISTRY.md) row 10 — the independent record of this defect
- [`UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md) — where `KI-013` will live
- [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) — the gate derivation and the `:79` known-red
