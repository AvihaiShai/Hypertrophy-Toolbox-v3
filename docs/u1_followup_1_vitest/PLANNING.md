# Plan Review — U1-FOLLOWUP-1: Vitest coverage for the Volume Splitter calculate-failure helpers

> **DIRECT OWNER UPDATE — 2026-10-21: Gate 1 APPROVED.** The owner directly
> approved the refreshed decision packet, the joint criterion 3(b) reading and all
> disclosed §v2.G toast assertions; selected filing (a2)+(i); and made this packet
> eligible before Q4/C4 after checks and independent review. Publication and named-PR
> merge remain separate. The historical unsigned status and council findings below
> are preserved as their original record. Gate 0 remains a signed **relayed record**.
> Verbatim direct answers and current implementation state are appended at the end.


> ~~**Status: Section 0 written. STOPPED AT GATE 0 (unsigned).**~~ ⚠️ **UPDATED 2026-10-21 —
> Gate 0 recorded as SIGNED by the owner, on a relayed record** (see *Section 0 sign-off* for the
> relay chain). ~~Plan v1, the council, the response matrix and Plan v2 are **not drafted**. Plan v1
> waits for the measured seam evidence.~~ ~~⚠️ **UPDATED 2026-10-21 (later) — Plan v1 is DRAFTED**
> (see *Plan v1*), citing the measured seam evidence. **The council is PENDING**: the reviewer
> findings, response matrix and Plan v2 are not written, and Gate 1 is unsigned.~~ ⚠️ **UPDATED
> 2026-10-21 (council complete) — Plan v2 is WRITTEN. STOPPED AT GATE 1 (unsigned).** All three
> reviewers' findings are pasted verbatim. Every finding has a **proposed** disposition in the
> response matrix, and the owner confirms each one at Gate 1. Plan v2 ends with the Gate 1 decision
> list (*Plan v2*, §v2.O). **Nothing is authorized:** no implementation, no production change, no
> commit, no merge, no ledger edit and no qualification-window or C4 decision.

**Planning size (manager classification, recorded verbatim in substance):** **Large / ambiguous**
under [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) plan-stage routing —
**Gate 0 + council (`/council-plan`) + Gate 1 are required.** Reason: the requirements are unclear
(the recorded condition is stale and has to be re-derived); the test seam is an open owner decision
that may require a `static/js/**` production export; and the landing interacts with the JS-unit
qualification-window governance (the Q2 restart clause, Q4/D2) and with the required
`Test Inventory Drift` check.

**Source of truth for every citation below:** `origin/main` =
`1f5ae0f059f6cb4a994f92b6e03c57d689fd060c` (2026-10-20T23:07:19+03:00, *"ci: add PR-only
Dependency Review (B3) (#539)"*), read from byte-exact blob copies, **not** from the shared main
checkout's working tree. `path:N` means line N of that file at that commit. Anything read from
somewhere else is marked ⚠️ and listed under *Evidence gaps*.

---

## Section 0 — Requirements Brief

**Raw request** (verbatim, as relayed by the top-level session)
> keep working on U1-FOLLOWUP-1 with the ai consulting team until it get done

**Problem**

U1 (Volume Splitter calculation-failure feedback, PR #423) added the calculate-failure helpers to
`static/js/modules/volume-splitter.js` with **browser-level coverage only**. The owner's OD-1
decision (2026-08-26) made Vitest unit coverage of those helpers a **required, open follow-up**,
U1-FOLLOWUP-1, recorded at
[`volume_failure_feedback/PLANNING.md`](../volume_failure_feedback/PLANNING.md) §v2.14
(`:1276-1318`; OD-1 at `:1271`). The coverage still does not exist. The obligation's own text
specifies its coverage in terms of a condition that **no longer matches the shipped code**
(U3b's K13), so the obligation cannot be planned until the requirement is re-derived from what
actually shipped. That re-derivation is §0.3 below.

The outcome that is missing: a pure-logic regression in the failure state machine (region
idempotence, the announce condition, the request-sequence guard, the toast probes) is today
caught only through a Playwright browser run, and is not caught by the Vitest tier at all.

### 0.1 Facts — measured on `origin/main` `1f5ae0f0`

**The obligation and its standing record**

- F1. U1-FOLLOWUP-1 is **OPEN and REQUIRED**. OD-1: *"option (i) now, with option (iii) as the
  REQUIRED follow-up"*; the owner accepted §v2.14 as the authoritative record; the implementation
  PR body *"must link §v2.14 explicitly"* — `volume_failure_feedback/PLANNING.md:1271`,
  `:1316-1318`.
- F2. The original text requires *"`static/js/modules/__tests__/volume-splitter.test.js` covering
  the region's idempotence, the `forceAnnounce || !standing || !ourToastContentStands()` condition,
  the sequence guard, and the shared probe"* — `volume_failure_feedback/PLANNING.md:1316`.
- F3. The 2026-08-29 owner amendment, annotated in place above that text, says the quoted
  condition is **STALE (K13)** and that *"whoever discharges U1-FOLLOWUP-1 re-reads §4.3 first and
  derives the coverage from the shipped condition, not from the sentence below"* —
  `volume_failure_feedback/PLANNING.md:1294-1301`. It also re-anchors the no-landing-before bar to
  **`2026-09-10T23:18:21Z`** (`:1283-1293`) and states that *"once the strict mark passes, landing
  this packet restarts the *next* window; it does **not** retroactively void a qualification cycle
  that completed successfully before it"* (`:1303-1306`).
- F4. The amendment does not authorize the packet and does not file it in
  `OPEN_WORK_EXECUTION_PLAN.md` §4 or §7, *"which OD-1 left as an open owner option, not a
  precondition"*; OD-1 itself is unamended — `volume_failure_feedback/PLANNING.md:1308-1312`.
- F5. U3b recorded the staleness as **K13** and did not repair U1's document:
  [`toast_action_continuity/PLANNING.md`](../toast_action_continuity/PLANNING.md) `:1207`
  (response-matrix row A2/P5) and §4.6 item 9 `:1538-1541`.
- F6. The single actionable queue lists U1-FOLLOWUP-1 as *"Open and required, unplanned. The
  strict-mark bar has passed; re-derive its stale K13 condition before planning it through its own
  gates"* — [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §0.4 `:189`. §0 is the
  single queue under Q12 (`:119-123`, `:126-134`; [`project_direction/AGREED_PLAN.md`](../project_direction/AGREED_PLAN.md) §11 `:348`).
- F7. The 2026-08-29 owner ruling in STEP12 §13.0 re-states U1-FOLLOWUP-1 as OPEN and required,
  says its coverage *"must be re-read against U3b's amended announce condition, recorded as K13"*,
  and retires U3b's KI-011 Vitest helper coverage: *"Reviving that coverage requires a new packet
  and its own Gate 0"* —
  [`testing_phase3/STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md)
  `:5178-5186`. The same ruling *"does **not** authorize U1-FOLLOWUP-1's implementation"* (`:5192`).

**The shipped code — `static/js/modules/volume-splitter.js` (blob `6fc3da55…`)**

- F8. The module's **only export** is `initializeVolumeSplitter()` (`:59`). It imports
  `showToast` and `toastMessageText` from `./toast.js` and `api` from `./fetch-wrapper.js`
  (`:1-2`). Its only caller is the page router in `static/js/app.js` (blob `c6754a85…`): the
  import at `:25` and the `'/volume_splitter'` route entry at `:211`.
- F9. Module-level mutable state: `volumeConfig`, `currentMode`, `calculateDebounceId`,
  `modeVolumeState`, `modeRangeState` (`:4-14`), `calculateRequestSeq` (`:32`),
  `pendingDeletePlanId`, `deleteModal` (`:368-369`) — **eight bindings, none with an exported
  reset.**
- F10. Constants: `CALCULATE_ERROR_ID = 'volume-calculate-error'` (`:23`);
  `CALCULATE_ERROR_MESSAGE = 'Volume calculation failed, so no results are shown. Please try again.'`
  (`:27`).
- F11. **There are now six helpers, not five.** U1's §v2.2 (C)–(F),(J) defined five
  (`volume_failure_feedback/PLANNING.md:1038-1076`); U3b added a sixth, `ourMessageStands()`
  (`toast_action_continuity/PLANNING.md` §4.3 `:1426-1435`; §8.2 `:2206-2210`). Shipped:
  `enterCalculateFailureState` `:177-192`, `renderCalculateFailureRegion` `:194-232`,
  `exitCalculateFailureState` `:234-239`, `dismissCalculateFailureToast` `:241-259`,
  `ourToastContentStands` `:265-267`, `ourMessageStands` `:280-282`. None is exported.

**`static/js/modules/toast.js` (blob `2cfc123a…`)**

- F12. `toastMessageText()` is exported at `:351-353` and returns
  `document.querySelector('#toast-body span.toast-message')?.textContent ?? null` — it
  deliberately excludes the action slot (`:340-350`).
- F13. Since KI-011, a later toast **without** an action preserves a standing action
  (`:296-306`); the action is removed on `hidden.bs.toast` (`:165-171`), on its own expiry timer
  (`:147-155`, `:97-103`) and on activation (`:135-146`). The message span persists after a hide.
  Consequence measured by U3b (§4.1 A5; §7.2 `:2056-2060`): the two probes **diverge in both
  directions** — a replacement keeps the button but changes the message; an auto-hide keeps the
  message but removes the button.

**Vitest harness and precedent**

- F14. [`vitest.config.js`](../../vitest.config.js) (blob `c16ca428…`, unchanged since the
  STEP12 ledger's readings): `environment: 'node'` by default, per-file
  `// @vitest-environment jsdom` opt-in, `include: ['static/js/**/*.test.js']`, report-only
  coverage with no thresholds (`:5-23`, `:25-48`). `npm run test:js` = `vitest run`
  ([`package.json`](../../package.json) `:9`); `jsdom` 30.1.3 and `vitest` 5.0.5 pinned (`:20-27`).
- F15. Corpus today: **13 files / 245 cases** —
  [`TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) `:1831-1832`. There is no
  `static/js/modules/__tests__/volume-splitter.test.js` on `origin/main` (manifest tree listing).
- F16. **Mock-and-re-import precedent (no production change):**
  `static/js/modules/__tests__/exercises.test.js` (Packet C) mocks four collaborators with
  `vi.hoisted()` + `vi.mock()` (`:50-74`), fakes the `bootstrap` global (`:149-157`) and re-imports
  the module under `vi.resetModules()` because its module-level state has no exported reset
  (`:170-174`). `toast.test.js` (Packet B) fakes `bootstrap.Toast` against a reduced
  `#liveToast` fixture (`:48-110`). Both state the repository's two authoring rules — every
  negative is paired with a positive (`toast.test.js:35-42`, `exercises.test.js:17-22`).
- F17. **Pure-export precedent:** `workout-plan-seams.test.js` and
  `workout-controls-persistence.test.js` test modules that already export the functions under
  test (`workout-plan-seams.test.js:3-32`; `workout-controls-persistence.test.js:13-23`).
- F18. **A grep of `static/js/modules/**` on `origin/main` finds no test-only export
  convention** (no `__testing`, `_forTest`, `TEST_ONLY`, or `export { … }` re-export block).
- F19. **The closest governance precedent declined a production seam.** STEP12 Q3 /
  Packet D: `backup-center.js` was *"1069 lines behind a **single** export,
  `initializeBackupCenter()`, with eight module-level mutable variables"*; the options were skip,
  test through the full-DOM init surface, or a production seam extraction; the owner **dropped** it
  and ruled the extraction out of scope — `STEP12_JS_UNIT_GATE0.md:974`, `:491-513`.
  `volume-splitter.js` has the same shape (1057 lines, one export, eight mutable bindings — F8, F9).
  That ruling governed step 12 only; it is precedent here, not a binding rule.
- F20. No `vi.useFakeTimers` use exists in the corpus snapshot (grep), so testing the 300 ms
  debounce path (`volume-splitter.js:1012-1018`) would be new technique for this repository.

**Qualification-window and ledger state**

- F21. Q2 (signed 2026-08-15): the strict 14-day window runs *"from the first successful
  `JS Unit (Vitest, non-required)` run on `main` after the final expansion packet lands"* —
  `STEP12_JS_UNIT_GATE0.md:210`, `:973`. Q4 (drop the `(non-required)` suffix) is **OPEN** and is
  to be decided *"**with** D2 and never after"* (`:975`).
- F22. Declared **T0 `2026-08-27T23:18:21Z`**, strict mark **`2026-09-10T23:18:21Z`**, suite
  **13 files / 245 cases**, with the ruling's definition of *"final expansion packet"* as *"the last
  change merged before this qualification window that added, removed, renamed or materially changed
  a case under `static/js/**/*.test.js`"* — `STEP12_JS_UNIT_GATE0.md:5159-5208`.
- F23. **R2.3 — Q4/D2 is unsigned and no longer time-gated:** *"the strict mark … has passed, which
  is a precondition, not a signature"* — `OPEN_WORK_EXECUTION_PLAN.md:157`. Branch protection: 12
  required contexts, `strict: false`, `JS Unit (Vitest, non-required)` absent —
  [`MASTER_HANDOVER.md`](../MASTER_HANDOVER.md) `:28`.
- F24. **The canonical §13.0 ledger stops at row 64** (fixed cutoff `2026-08-31T23:05:48Z`,
  `STEP12_JS_UNIT_GATE0.md:5521-5550`), which is **before** the strict mark. Five later greens
  (2026-09-01) are enumerated as owed in `OPEN_WORK_EXECUTION_PLAN.md` §26.4 `:3978-4002`; §0.4
  records *"33 unrecorded `main` runs"* per #526's description and *"Write rows only through the
  §13.0 process"* (`:190`). **Whether the 2026-08-27 → 2026-09-10 cycle completed with zero red,
  missing, skipped or cancelled results is therefore not recorded on `main`.**
- F25. Standing ledger rule: a PR cannot record its own landing; *"merging mints the next
  unclaimed row"* (`STEP12_JS_UNIT_GATE0.md:5713-5714`, `:5933-5935`). U3b's precedent made its
  implementation PR owe a §13.0 row read **at job level** and proven **by blob SHA**, and warned that
  *"a `js-unit` red on that `main` run resets T0 to zero"* (`toast_action_continuity/PLANNING.md`
  §4.6 item 11 `:1543-1547`).

**Gates and pins this packet will owe**

- F26. A `static/js/**/*.test.js` file falls under the **Frontend (JS)** row: matching Chromium
  specs from the feature map (`volume-splitter.spec.ts`, `volume-progress.spec.ts`), manual smoke
  if interactive, and **regenerate `docs/test_inventory/`** whenever a `*.test.js` case is added —
  [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) `:50`, `:146`.
- F27. `Test Inventory Drift` pins Vitest per-file counts **and every case's identity**; it is a
  whole-file diff, and the artifact is regenerated, never hand-edited — `QUALITY_GATE.md:71`,
  `:80`, `:85-90`. `Type Check` blocks on `tsc --noEmit` and on net-new pyright diagnostics for any
  `.py` in the diff (`:72`, `:97-98`).
- F28. `tests/test_vitest_inventory_contracts.py` (blob `877bb838…`) pins the Vitest surface as
  literals that *"are the point of the file"* (`:55-58`): `EXPECTED_TOTAL_CASES = 245` (`:59`),
  `EXPECTED_TOTAL_FILES = 13` (`:60`), and `EXPECTED_PER_FILE`, an exact 13-entry file → count map
  (`:61-75`). Three tests compare against them by **equality**: the totals
  (`test_vitest_totals_are_pinned`, `:136-139`), the per-file map (`rows == EXPECTED_PER_FILE`,
  `:142-144`) and the Markdown totals row and per-file listing (`:541-545`, `:548-551`). **A new
  Vitest file therefore reds full pytest** unless, in the same PR, both totals move and the map
  gains an exact entry for `static/js/modules/__tests__/volume-splitter.test.js`. The file runs no
  subprocess and must keep an identical node count on Windows and Linux (`:19-28`). *(The shared
  working-tree copy of this file differs from `origin/main` and lacks part of this; only the
  `origin/main` copy is cited here.)*
- F29. Existing E2E coverage of the same behavior: `e2e/volume-splitter.spec.ts` blocks
  *"Volume Splitter calculation failure feedback"* (`:798`; arms `a1`–`a6`, `b1`, `c1`–`c2`,
  `s1`–`s3`, `s6`) and *"KI-011 toast action continuity"* (`:1244`; `t1`–`t12`, `t5b`), including
  `t9` replacement → re-announce (`:1411-1433`), `t10` dismiss guard (`:1435-1506`) and `t11`
  auto-hide → suppressed (`:1508-1550`).

**Process, sequencing and checkout rules**

- F30. Q8(a) (2026-10-19 delegated decision) classified **only WS3, WS4 and WS5**; its boundaries
  require a standalone clone with independent Git storage and private DB/runtime/backup/log/temp/
  cache/bytecode paths (*"A linked worktree does not provide that isolation"*), and a check of live
  freezes and blocked-recovery states before work — `AGREED_PLAN.md` §11 `:340-359`. The
  consultation that preceded it warns *"Do not infer either a blanket ban on all unrelated
  development or a global hold release"* (`:257`).
- F31. [`WORKTREE_CLEANUP_PLAN.md`](../ai_workflow/WORKTREE_CLEANUP_PLAN.md) §1.2 orders
  *prevention → `PREVENTION_COMPLETE` → finish or explicitly disposition open development → …* and
  binds Operations B–E (`:50-69`); `PREVENTION_COMPLETE` is not declared
  (`MASTER_HANDOVER.md:54-59`).
- F32. One manager-led feature owns one checkout; concurrent work must start in a separate checkout
  created before its manager session (`AUTONOMY.md:87-89`;
  [`PARALLEL_WORKFLOW.md`](../ai_workflow/PARALLEL_WORKFLOW.md) `:26-32`). Worktree creation goes
  through `scripts/new-worktree.ps1` with owner-approved lifecycle metadata and baseline
  (`PARALLEL_WORKFLOW.md:34-58`; `AUTONOMY.md:43-47`). The **tracked-DB commit rule** is
  `PARALLEL_WORKFLOW.md:96-108` and is referenced, not restated, here.
- F33. Owner approvals (Gates 0–2, merge of a named PR) are given directly; *"an agent's relay,
  summary or inference of the owner's intent is not an owner approval"* —
  `QUALITY_GATE.md:22-40`. The owner **has** delegated decisions to the consulting team before,
  by explicit words, for named items: #531–#533 (`OPEN_WORK_EXECUTION_PLAN.md:141-144`) and
  AGREED_PLAN §11's four items (`AGREED_PLAN.md:333-338`, which states it is *"not … an owner
  Gate 0/Gate 1 signature"*).
- F34. `OPEN_WORK_EXECUTION_PLAN.md` carries an existing docs-cleanup claim (AGREED_PLAN §9.1 Q8(b)
  `:258`) and `MASTER_HANDOVER.md` is a never-claimed shared path requiring per-edit coordination
  ([`WORKSTREAM_OWNERSHIP.md`](../ai_workflow/WORKSTREAM_OWNERSHIP.md) `:29-34`).

### 0.2 The stale condition, stated explicitly

**§v2.14's quoted condition `forceAnnounce || !standing || !ourToastContentStands()` is STALE
(K13) and is NOT the requirement of this packet.** It describes U1's code at #423
(`volume_failure_feedback/PLANNING.md:1043`), which U3b (#426) changed. The requirement is the
shipped behavior in §0.3, derived from `volume-splitter.js` at `1f5ae0f0` and cross-checked against
U3b's normative §4.3 and implementation record §8.2. Likewise *"the shared probe"* in §v2.14 no
longer names one function: U3b's shipped comment *"no longer calls itself 'the single shared
probe', which the second probe falsified"* (`toast_action_continuity/PLANNING.md:2209-2210`).

One internal inconsistency in U3b's record is noted so it is not inherited: §4.4's table row for
`t11` says the auto-hide path *"re-announces"* (`toast_action_continuity/PLANNING.md:1472`), but
§7.2 re-specified `t11` with **suppression** as the pristine outcome (`:2056-2060`), and the shipped
arm asserts suppression (`e2e/volume-splitter.spec.ts:1508`, `:1546-1549`). **This brief follows
the shipped code, the shipped arm and §7.2.**

### 0.3 The four coverage targets, re-derived from the shipped code

All line numbers are `static/js/modules/volume-splitter.js` at `1f5ae0f0` unless stated.

**T-1 — Region idempotence** (`renderCalculateFailureRegion()` `:194-232`, with its exit at
`:234-239`)

- Returns without building, and without rewriting text, if `#volume-calculate-error` already
  exists (`:195-199`).
- Returns without building if `.volume-insights-panel` is absent (`:201-204`); the panel is
  [`templates/volume_splitter.html`](../../templates/volume_splitter.html) `:83`.
- Otherwise builds one `div` with `id` and `data-testid` both derived from `CALCULATE_ERROR_ID`
  (`:206-209`), a message `span` set by `textContent` (`:213-215`), and a Retry `button` with
  `type="button"`, `data-testid="volume-calculate-retry"`, `aria-label="Retry volume calculation"`,
  whose click calls `calculateVolume()` with the default `forceAnnounce: true` (`:217-229`); then
  `panel.prepend(region)` (`:231`). The region is deliberately **not** a live region (`:211-212`).
- On success and on reset the region is **removed** from the DOM (`.remove()`, never hidden)
  (`:234-237`, `:164`, `:331`).

**T-2 — Announce condition** (`enterCalculateFailureState()` `:177-192`)

- Order: `clearResults()` (`:178`), then `standing` = whether the region existed **before**
  rendering (`:180`), then render (`:181`), then announce.
- **Shipped condition: `forceAnnounce || !standing || !ourMessageStands()`** (`:183`) — keyed on
  the **message** probe, matching U3b §4.3 item 3 (`toast_action_continuity/PLANNING.md:1431-1432`).
- The announcement is `showToast('error', CALCULATE_ERROR_MESSAGE, { action: { label: 'Retry',
  ariaLabel: 'Retry volume calculation', onClick: () => calculateVolume() } })` (`:184-190`).
- `forceAnnounce` defaults to `true` (`:126`) on the explicit paths: Calculate button (`:75`),
  `loadPlan()` (`:360`), `setMode()` (`:680`), and both Retry handlers (`:188`, `:228`). It is
  `false` on the two slider-originated paths: the debounced `input` path via `scheduleCalculate()`
  (`:774`, `:1017`) and the slider `change` listener (`:777-783`).
- Re-signed OD-2 text that this condition implements: *"Repeat slider-originated announcements are
  suppressed while the same failure region **and U1's own toast MESSAGE** stand; explicit user
  commands always announce, and so does any failure at a moment when **U1's MESSAGE** no longer
  stands"* (`toast_action_continuity/PLANNING.md:1442-1445`).

**T-3 — Request-sequence guard** (`calculateVolume()` `:126-175`, `resetValues()` `:321-332`)

- `const seq = ++calculateRequestSeq;` is the first statement (`:127`).
- The success `.then` returns early if `seq !== calculateRequestSeq` (`:151-154`); inside it, a
  post-2xx handling throw goes to the inner `catch`, which calls `enterCalculateFailureState`
  (`:155-163`); success calls `exitCalculateFailureState()` (`:164`).
- The outer `.catch` (request-failure class) returns early on the same check, then calls
  `enterCalculateFailureState` (`:166-174`).
- `resetValues()` clears results, bumps `calculateRequestSeq` and then calls
  `exitCalculateFailureState()` (`:327-331`), so an in-flight failure resolving after a reset
  cannot repaint.
- The request payload and options (`:136-149`, including `showErrorToast: false` at `:147`, which
  OD-4 keeps) are not a coverage target and must not change.

**T-4 — The probes ("the shared probe" is now two probes plus a conjunction)**

- **Action probe** `ourToastContentStands()` (`:265-267`):
  `Boolean(document.querySelector('#liveToast button[aria-label="Retry volume calculation"]'))`.
  Scoped to `#liveToast`, **never** `#toast-body` — a binding instruction carried from U1 §v2.2 (J)
  and U3b §4.3 item 1 (`:261-264`). Deliberately blind to visibility.
- **Message probe** `ourMessageStands()` (`:280-282`):
  `toastMessageText() === CALCULATE_ERROR_MESSAGE`, using `toast.js`'s exported reader, not a
  `#toast-body` query (`:269-279`; `toast.js:351-353`).
- **Announce** uses the message probe only (T-2).
- **Dismiss guard** (`dismissCalculateFailureToast()` `:241-259`) requires **both**: it returns if
  the action probe is false (`:244-246`) and returns if the message probe is false (`:251-253`),
  then calls `bootstrap.Toast.getInstance(#liveToast)?.hide()` (`:255-258`). Two sequential early
  returns, equivalent to U3b §4.3 item 4's
  `if (!ourToastContentStands() || !ourMessageStands()) return;` (`:1433-1435`).
- **Therefore T-4 means both probes, and the divergence between them in both directions** (F13):
  replacement (button stands, message is a stranger's) and auto-hide/expiry (message stands,
  button gone).

### 0.4 Calculation surface

**`none`.**

Evidence: every function in §0.3 manipulates DOM nodes, toast calls and a request counter; none
computes a volume, range, status, effective set or any other calculated value. The request payload
built at `volume-splitter.js:136-149` and the `/api/calculate_volume` server contract
(`routes/volume_splitter.py`, `utils/volume_splitter_service.py`, both out of U1's scope at
`volume_failure_feedback/PLANNING.md:986`) are untouched by a test-only packet. No schema, API
response shape or calculation changes under any option in §0.8 Q-seam; option (a)/(b)/(e) there
would change only the JavaScript module **export surface**, which is not an API response shape.
No migration note is owed under the calculation rule; the PR description should still state "no
user-visible behavior change", per [`CLAUDE.md`](../../CLAUDE.md) §1's refactor invariant, because
`volume_splitter` is the *Distribute* workflow.

### 0.5 Acceptance criteria

The criteria describe observable outcomes and deliberately do not choose the seam (Q-seam).
"Reach" below means: through whichever seam the owner approves.

1. **Given** `origin/main` plus this packet, **when** `npm run test:js` runs, **then** a new file
   `static/js/modules/__tests__/volume-splitter.test.js` is collected and passes, and the corpus
   reads **14 files / 245 + N cases**, where N is stated in Plan v2 and matches the regenerated
   [`TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json); every pre-existing Vitest file
   is byte-identical.
2. **T-1.** **Given** a calculation failure has rendered the region, **when** a second failure
   occurs, **then** exactly one `#volume-calculate-error` exists, it is the **same node** (identity,
   not equality), and its message text was not rewritten. **Given** no `.volume-insights-panel`,
   **when** a failure occurs, **then** no region is created and nothing throws. **Given** a standing
   region, **when** the next calculation succeeds or the user resets, **then** the node is absent
   from the DOM (not merely hidden).
3. **T-2, one case per disjunct, each with a paired positive proving the failure reached the state
   machine.** (a) An explicit command (`forceAnnounce` true) announces even while the region **and**
   our message stand. (b) A slider-originated first failure (`!standing`) announces. (c) A
   slider-originated repeat failure while the region and our message stand does **not** announce.
   (d) A slider-originated repeat failure after a stranger's message replaced ours **does**
   announce, even though our Retry button still stands. (e) A slider-originated repeat failure
   after our button is gone but our message stands (auto-hide/expiry) does **not** announce. Every
   announcement carries `CALCULATE_ERROR_MESSAGE`, type `error`, and an action labelled `Retry`
   with `ariaLabel` `Retry volume calculation`.
4. **T-3.** **Given** two calculations in flight, **when** the older one resolves after the newer
   one — as a success, as a request failure and as a post-2xx handling failure — **then** the older
   one neither paints results, nor renders a region, nor announces, nor dismisses. **Given** a
   calculation in flight, **when** the user resets and that calculation then fails, **then** no
   region and no toast appear.
5. **T-4.** The action probe answers true exactly when `#liveToast` contains a
   `button[aria-label="Retry volume calculation"]`, **including** when that button sits outside
   `#toast-body` (the binding `#liveToast` scoping). The message probe answers true exactly when
   `toastMessageText()` equals `CALCULATE_ERROR_MESSAGE`. On a success after a failure, the toast is
   hidden **only** when both stand; it is **not** hidden when only the button stands (stranger's
   message) or only the message stands (button gone).
6. **Authoring rules.** No negative assertion stands alone (the repository rule at
   `toast.test.js:35-42` and `exercises.test.js:17-22`); every module-level-state dependency is
   reset between cases by a stated mechanism.
7. **Discrimination.** For each of T-1 … T-4 at least one mutation of the production logic makes
   the new file fail, and reverting it makes the file pass; mutations run against copies (never the
   repository file) and are judged by process exit code. Scope per Q-mutation.
8. **No behavior change.** `e2e/volume-splitter.spec.ts` and `e2e/volume-progress.spec.ts` pass
   with the spec files byte-identical; `static/js/modules/volume-splitter.js` and `toast.js` are
   byte-identical to `origin/main` **unless** Q-seam authorizes a production change, in which case
   the diff to them is limited to exactly the authorized lines.
9. **Gates.** `scripts/generate_test_inventory.py --check` exits 0 after regeneration in the same
   commit; full pytest is green (including any pin literal that must move per Q-pins);
   `tsc --noEmit` reports zero errors; pyright reports no net-new diagnostic if any `.py` is in the
   diff.
10. **Record-keeping.** The implementation PR body links
    `volume_failure_feedback/PLANNING.md` §v2.14; §v2.14 is **annotated in place, never rewritten**;
    the queue and ledger are handled as decided under Q-filing and Q-window.

### 0.6 In scope

- The new Vitest file and its fixtures/fakes.
- Regeneration of `docs/test_inventory/TEST_INVENTORY.{json,md}`.
- The minimal pin update in `tests/test_vitest_inventory_contracts.py` that F28 makes necessary:
  the two totals and one new `EXPECTED_PER_FILE` entry (Q-pins).
- Only if Q-seam selects it: the exact authorized export or extraction lines in
  `static/js/modules/volume-splitter.js`.
- This planning document; the §v2.14 in-place annotation and queue/ledger edits as decided under
  Q-filing and Q-window.

### 0.7 Out of scope / non-goals

- Any change to failure-feedback behavior, copy, announce semantics, the 300 ms debounce, the
  request payload, `showErrorToast: false`, or the `#liveToast` scoping.
- `static/js/modules/toast.js`, `toast.test.js` and every other existing Vitest file.
- **U3b's retired KI-011 helper coverage of `toast.js` itself** (slot, expiry timer, dismissal
  wiring, dispose ordering) — retired by owner ruling, revivable only by its own Gate 0 (F7). See
  Q-scope for the boundary with `ourMessageStands()`.
- New or edited E2E specs, `e2e/fixtures.ts`, `ci.yml`, branch protection, promotion of `js-unit`,
  and Q4/D2 themselves.
- Coverage thresholds, `vitest.config.js` changes, new devDependencies.
- The other `volume-splitter.js` paths (save, load, delete, activate, history, Excel export).
- Any database change; the tracked-DB commit rule (`PARALLEL_WORKFLOW.md:96-108`) applies
  unchanged.

### 0.8 Owner decisions and blocking questions

Each is phrased for a multiple-choice answer. The recommendation is the product-manager's and is
**not** a decision. "Blocks" says what each answer is needed for.

> **STATUS OF THESE QUESTIONS — recorded 2026-10-21.** The analysis and options below are left
> as written at Gate 0. Each question carries a dated status line; the provenance of every ruling
> is in *Section 0 sign-off*.
>
> | Question | Status |
> |---|---|
> | Q-scope, Q-seam, Q-delegation, Q-done | **OWNER-RULED** 2026-10-21 (relayed record) |
> | Q-mutation, Q-E2E, Q-pins | **Delegated to the team under Q-delegation (b)**; to be settled in Plan v1/v2 as **TEAM decisions, not owner rulings** |
> | Q-window, Q-filing, Q-sequencing | **OPEN — owner decisions, carried to Gate 1** |

**Q-scope — what "the shared probe" covers, and its boundary with U3b's retired coverage.**
*Blocks: Gate 0.*
- (a) T-4 covers **both** probes, the message-keyed announce condition and the two-probe dismiss
  guard, as §0.3 derives; it excludes `toast.js` internals; and the owner confirms this is
  U1-FOLLOWUP-1's re-derived scope, **not** a revival of U3b's retired coverage.
- (b) As (a), and the owner additionally records that it partially revives U3b's coverage and
  authorizes that here.
- (c) Cover only the original five helpers and the action probe; leave `ourMessageStands()`
  uncovered.
- **Recommended: (a).** F3 instructs that coverage be derived from the shipped condition, and T-2
  cannot be tested without the message probe; (c) would test a condition that no longer ships.
- ✅ **OWNER-RULED 2026-10-21 — (a)** *"Both probes, as U1 scope"* — *cover all six helpers as the
  re-derived scope of U1-FOLLOWUP-1, not a revival of U3b's retired coverage.* (The quoted choice
  label is the owner's as relayed; the italic gloss after the dash is the top-level session's
  relayed wording.)

**Q-seam — how the tests reach module-private code.** *Blocks: Plan v1 (the plan must name a
seam). Any option that edits production JS needs explicit owner authorization.*
- (a) Plain named exports of the six helpers plus whatever T-3 needs (`calculateVolume` and the
  constants, or a counter accessor) — a production `static/js/**` change that widens the module's
  public API beyond `initializeVolumeSplitter()`.
- (b) One named test-only export (e.g. a single frozen object) — a production change with **no
  repository precedent** (F18).
- (c) **No production change:** drive everything through `initializeVolumeSplitter()` and its real
  listeners (Calculate click, slider `change`/`input`, Reset click) against a jsdom fixture reduced
  from `templates/volume_splitter.html` and the `#liveToast` markup, with `fetch-wrapper.js` mocked
  and controllable promises, a faked `bootstrap` global, and a fresh module per case via
  `vi.resetModules()` — the Packet C precedent (F16). Sub-choice for the council: mock `toast.js`
  (`showToast`, `toastMessageText`) or use the real `toast.js` behind the Bootstrap fake.
- (d) Hybrid: (c) wherever reachable, plus a minimal export only for a target the council proves
  unreachable, brought back to the owner before Gate 1.
- (e) Extract the failure-state helpers into a new module imported by `volume-splitter.js` — the
  production seam extraction Q3 declined for the analogous `backup-center.js` (F19).
- (f) Re-open OD-1 and close U1-FOLLOWUP-1 without Vitest coverage — listed for completeness; it
  reverses a signed REQUIRED decision.
- **Recommended: (c), falling back to (d) only on measured unreachability.** All four targets are
  reachable through public listeners: Calculate vs slider `change` selects `forceAnnounce`, Reset
  bumps the counter, and controllable `api.post` promises order responses. It keeps production JS
  byte-identical, has direct precedent, and avoids the API widening Q3 refused. ⚠️ Reachability is
  reasoned, not measured.
- ✅ **OWNER-RULED 2026-10-21 — (d)** *"No prod change, fallback export"* — *drive through
  initializeVolumeSplitter() with a test DOM, mocked api, fake bootstrap, fresh module per test; a
  minimal export only for a target shown (measured) unreachable, and any such export needs a
  separate owner approval naming the symbols.* (Label as relayed; gloss in the top-level session's
  relayed wording.)
  - **Where the ruling differs from option (d) as drafted, the ruling governs.** The fallback
    export is **not** a team decision and is not settled by bringing it back before Gate 1. It
    needs its **own separate owner approval naming the symbols**, and it is available only for a
    target **measured** to be unreachable.
  - **Reachability is being measured** by a throwaway probe; the results are to be cited in
    Plan v1. Until then the ⚠️ above stands.
  - Within the ruling, the seam details — including the toast mock-versus-real sub-choice — are
    delegated to the team under Q-delegation (b).

**Q-window — accepting the qualification-window consequence of landing.** *Blocks: Gate 1 (the
plan's sequence depends on it); not Gate 0.*
- (a) Land when the gates pass; accept that it restarts the **next** window (F3), with Q4/D2 still
  unsigned.
- (b) Hold the landing until the owner decides R2.3 (Q4/D2) on the completed 245-case cycle, then
  land.
- (c) Land, and rule now that D2 may be signed on the completed 245-case cycle without a fresh
  14-day window on the 14-file suite.
- (d) Before landing, record the §13.0 ledger through the strict mark `2026-09-10T23:18:21Z` via
  its own process, so "a cycle that completed successfully" (F3) is evidenced rather than assumed
  (F24); then (a), (b) or (c).
- Also to confirm: who owes the post-merge `JS Unit` row this landing mints (F25), and whether a
  red on that run is a stop condition for declaring the packet done.
- **Recommended: (d) followed by (a).** F3's protection presupposes a completed cycle that §13.0
  does not yet record. Once it is recorded, landing restarts only the next window, and D2 stays a
  separate owner act. Choose (b) instead if promoting `js-unit` soon matters more than this
  coverage.
- ⏳ **OPEN 2026-10-21 — owner decision, carried to Gate 1.** Q-delegation (b) leaves the JS-unit
  window with the owner.

**Q-filing — the queue entry and how §v2.14 records discharge.** *Blocks: Gate 1.*
- Filing: (a) do not file in `OPEN_WORK_EXECUTION_PLAN.md` §4/§7; update the existing §0.4 row on
  discharge. (b) Also file a packet entry in §4 or §7, as OD-1 allowed. (c) Neither; record
  discharge only here and in §v2.14.
- §v2.14: (i) a dated in-place annotation in the implementation PR, pointing to this document,
  with the merge SHA added by the next status PR; (ii) annotate only in a post-merge docs PR that
  can cite the merge SHA; (iii) do not touch §v2.14.
- **Recommended: (a) + (i).** §0 is the single queue (Q12) and §4 is an earlier reading by §0's own
  header (`OPEN_WORK_EXECUTION_PLAN.md:128-134`). An in-place annotation keeps U1's record honest at
  merge time. OPEN_WORK edits need coordination with its existing claim (F34); the PR body links
  §v2.14 under either option (F1).
- ⏳ **OPEN 2026-10-21 — owner decision, carried to Gate 1.**

**Q-sequencing — whether implementation may start after Gate 1, and in which checkout.** *Blocks:
implementation only; planning may proceed.*
- (a) Permitted after Gate 1, in a **standalone clone** under AGREED_PLAN §11's Q8(a) boundaries
  (F30), with the owner extending that classification to this packet by name.
- (b) Permitted after Gate 1, in a linked worktree created by `scripts/new-worktree.ps1` with
  owner-approved lifecycle metadata and baseline (F32).
- (c) Permitted after Gate 1, in the main checkout, only once it is clean and no other session is
  active (sequential work, F32).
- (d) Held until `WORKTREE_CLEANUP_PLAN.md` §1.2's open-development disposition or
  `PREVENTION_COMPLETE` (F31).
- **Recommended: (a).** The main checkout is shared and dirty with other sessions' edits; the
  owed gates include full pytest and Chromium E2E, which use a DB and a server; and (a) is the
  isolation standard the owner already accepted for WS3–WS5. A live freeze check is required before
  work under any option.
- ⏳ **OPEN 2026-10-21 — owner decision, carried to Gate 1.** Q-delegation (b) leaves checkout
  handling with the owner.

**Q-mutation — mutation evidence scope.** *Blocks: Gate 1.*
- (a) A Vitest-tier matrix covering every target, run in both directions against copies under
  `artifacts/`, judged by exit code — at minimum U1's M5/M6 (region), M8 and U3b's N11 (announce),
  M9 (sequence) and a dismiss-guard narrowing mutation (probes).
- (b) One mutation per target.
- (c) None beyond the gates.
- **Recommended: (a).** Every prior JS-unit packet used a both-directions matrix, and U1's own
  record holds that *"an arm that cannot be made to fail is not evidence"*
  (`volume_failure_feedback/PLANNING.md:1209`).
- 🔁 **DELEGATED 2026-10-21 to the team under Q-delegation (b).** To be settled in Plan v1/v2 as a
  **team decision, not an owner ruling.**

**Q-pins — test-file edits outside the new file.** *Blocks: Gate 1.*
- (a) Authorize updating `tests/test_vitest_inventory_contracts.py` in the same PR:
  `EXPECTED_TOTAL_CASES` (`:59`) and `EXPECTED_TOTAL_FILES` (`:60`) move to the new exact values,
  and `EXPECTED_PER_FILE` (`:61-75`) gains exactly one entry, for the new file. All three stay
  exact-equality assertions, and the 13 existing entries are unchanged. The same applies to any
  similar pin found on fresh `origin/main`.
- (b) Require a separate PR for pin changes.
- **Recommended: (a).** A split would leave `main` red between merges; precedent: U1 and U3b each
  bumped a literal in the same PR (`toast_action_continuity/PLANNING.md:2244-2249`).
- 🔁 **DELEGATED 2026-10-21 to the team under Q-delegation (b).** To be settled in Plan v1/v2 as a
  **team decision, not an owner ruling.** The basis is the **coordinator's statement** that Q-pins
  is included in what the team may settle. The relayed Q-delegation gloss names *"seam details
  within Q-seam, mutation scope and E2E handling"* and does **not** name the pins, so this inclusion
  is the coordinator's reading rather than the owner's words. If the owner says otherwise, Q-pins
  reverts to an owner decision at Gate 1.

**Q-E2E — existing browser coverage.** *Blocks: Gate 1.*
- (a) Leave all E2E arms unchanged; the Vitest file is additive.
- (b) Retire or trim overlapping arms.
- **Recommended: (a).** The E2E arms measure live-region, focus and Bootstrap lifecycle behavior
  that jsdom approximates (`volume_failure_feedback/PLANNING.md:981`); trimming them is a separate
  decision with its own risk.
- 🔁 **DELEGATED 2026-10-21 to the team under Q-delegation (b).** To be settled in Plan v1/v2 as a
  **team decision, not an owner ruling.**

**Q-done — what "until it get done" means.** *Blocks: Gate 0 (it fixes the end state).*
- (a) Done = PR merged on separate explicit owner confirmation naming the PR, its post-merge
  `JS Unit` job green, §v2.14 annotated and the queue row updated.
- (b) Done = PR ready for review with all gates green; merge is a separate owner act.
- **Recommended: (a), with the merge confirmation kept as its own owner act.**
  `QUALITY_GATE.md:24-30` makes merging a named PR an owner approval.
- ✅ **OWNER-RULED 2026-10-21 — (a)**, relayed together with the Gate 0 signature: *"Gate 0:
  SIGNED; done = PR merged (merge needs the owner's separate confirmation naming the PR), post-merge
  JS Unit green, records annotated."* (Relayed wording.)

**Q-delegation — what the request delegates to the consulting team.** *Blocks: Gate 0.*
- (a) Nothing: the owner answers each question above and signs Gates 0 and 1 and the merge.
- (b) Technical choices only — Q-seam within (c)/(d), Q-mutation and Q-E2E may follow the
  council's recommendation — while Gate 0, Gate 1, Q-window, Q-sequencing and the merge stay with
  the owner.
- (c) Broader delegation, as for #531–#533 (F33), naming which items.
- **Recommended: (b), only if the owner states it in their own words.** The request does not say
  this on its face. Under F33 an agent may not infer a delegation, and Gate signatures and merges
  are owner approvals in every case.
- ✅ **OWNER-RULED 2026-10-21 — (b)** *"Technical choices only"* — *team decides seam details
  within Q-seam, mutation scope and E2E handling; Gates 0/1, the JS-unit window, checkout handling
  and merge stay with the owner.* (Label as relayed; gloss in the top-level session's relayed
  wording.) Q-filing is not named on either side of that split; this document keeps it with the
  owner (see the status table above).

### 0.9 Preconditions

**Blocking the START of planning (Plan v1): none outstanding beyond Gate 0 itself.** Checked:

- The no-landing-before bar `2026-09-10T23:18:21Z` has passed (F3, F23); it governed landing, not
  planning.
- The queue's *"re-derive its stale K13 condition before planning"* (F6) is discharged by §0.2–§0.3,
  **subject to owner acceptance at Gate 0**.
- No queue, hold, freeze or sequencing rule found on `origin/main` bars documentation-only planning
  in a new `docs/` folder. PARALLEL_WORKFLOW exempts docs-only edits from forking (`:22-24`), and the
  new folder is not a parametrized inventory surface (`QUALITY_GATE.md:83`).
- Gate 0 needs answers to **Q-scope, Q-done and Q-delegation**; the rest can be carried into the
  council and Gate 1. ✅ *2026-10-21: all three owner-ruled (relayed record), and Gate 0 is
  recorded as signed. Plan v1 additionally waits for the measured seam-reachability evidence
  (Q-seam).*

**Blocking IMPLEMENTATION:**

1. Gate 0 signed, then Gate 1 signed on a council-reviewed Plan v2.
2. Q-seam answered; if it is (a), (b), (d) or (e), explicit owner authorization of the production
   `static/js/**` change, naming the symbols. *2026-10-21: answered (d). No production change is
   authorized. Any fallback export needs a separate owner approval naming the symbols, and only for
   a target measured to be unreachable.*
3. Q-sequencing answered; the selected checkout created under its own rules; a live freeze /
   blocked-recovery check done before any test runs (F30); a path claim recorded in the gitignored
   local claim file (`WORKSTREAM_OWNERSHIP.md:5-11`).
4. Q-window answered, including option (d)'s ledger evidence if chosen.
5. Fresh `origin/main` re-reconciliation before the first edit: blobs `volume-splitter.js`
   `6fc3da55…`, `toast.js` `2cfc123a…`, `vitest.config.js` `c16ca428…`,
   `tests/test_vitest_inventory_contracts.py` `877bb838…`, and the inventory at 13 / 245. Any drift
   is a stop-and-report condition. The shared main checkout's working-tree copies are **not** a
   valid base; at least `tests/test_vitest_inventory_contracts.py` differs from `origin/main`.
6. No other open PR or session touching `static/js/modules/volume-splitter.js`, `toast.js`,
   `static/js/modules/__tests__/` or `docs/test_inventory/` — re-checked live.

### 0.10 Assumptions made

- ⚠️ The file path `static/js/modules/__tests__/volume-splitter.test.js` named in §v2.14 is treated
  as binding.
- ⚠️ The request delegates no Gate approval, merge or window decision (Q-delegation).
  *Resolved 2026-10-21 by the Q-delegation (b) ruling.*
- ⚠️ "Done" includes a merged PR (Q-done). *Resolved 2026-10-21 by the Q-done (a) ruling.*
- ⚠️ All four targets are reachable through `initializeVolumeSplitter()` in jsdom without a
  production change (Q-seam (c)) — reasoned from the code, not measured. *2026-10-21: being
  measured by a throwaway probe; results to be cited in Plan v1.*
- ⚠️ `bootstrap` must be faked: `dismissCalculateFailureToast()` dereferences `bootstrap.Toast`
  unguarded (`:257`), while `initDeleteModal()` is guarded (`:373`); `tippy` absent is a safe early
  return (`:112`, `:814`). `initializeVolumeSplitter()` also issues `api.get('/api/volume_history')`
  on init (`:108`, `:515-522`), which any mock must satisfy.
- ⚠️ No live preservation/destructive freeze is in force at implementation time — not verifiable
  from the snapshot.
- ⚠️ The shipped `t11` / §7.2 reading (auto-hide → suppressed) governs over U3b §4.4's stale row
  (§0.2).
- ⚠️ Mutation copies under `artifacts/` follow the U3b and Packet B precedent; the exact loading
  mechanism for a mutated module under Vitest is a plan-stage question.

### 0.11 Evidence gaps (could not be verified from the `origin/main` snapshot)

- *Closed:* `docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md` (`bf9f33b5…`),
  `tests/test_vitest_inventory_contracts.py` (`877bb838…`) and `static/js/app.js` (`c6754a85…`)
  are now read from the `origin/main` snapshot. The first two **differ** from the shared working
  tree. For the template, the only difference this document depends on is its Sign-off wording,
  *"Owner approved Plan v2 (Gate 1)"* (`:152`), which is adopted below; the Section 0 shell
  (`:9-46`) is what this brief follows. For the pin file, F28 now cites `origin/main`.
- Whether the 2026-08-27 → 2026-09-10 qualification cycle completed without a red, missing, skipped
  or cancelled `JS Unit` result: §13.0 ends at row 64 (2026-08-31). The results of the later runs
  are not on `main`, apart from §26.4's five greens (F24).
- Live state: open PRs, other sessions' path claims (gitignored), live freezes, and whether
  `scripts/new-worktree.ps1` creation is currently unblocked.
- No branch-protection or GitHub API reading was taken; F23 relies on the committed handover's
  2026-10-20 reading.

### Section 0 sign-off — GATE 0 — ~~**UNSIGNED**~~ **SIGNED 2026-10-21 by the owner (relayed record)**

- [x] User confirms the acceptance criteria (§0.5) match intent.
- [x] User reviewed the assumptions (§0.10) and corrected or accepted each one.
- [x] User accepts §0.2–§0.3 as the re-derived requirement that replaces §v2.14's stale K13
      condition.
- [x] Blocking questions are answered: **Q-scope**, **Q-done**, **Q-delegation**. Q-seam,
      Q-window, Q-filing, Q-sequencing, Q-mutation, Q-pins and Q-E2E are answered now or carried
      into the council and Gate 1.

*Signed by:* the owner — *Date:* 2026-10-21 — *(an agent's relay or summary is not a signature;
`QUALITY_GATE.md:22-40`. That rule still stands. The signature is the owner's own answer, given
directly to the top-level session; what this document holds is a relayed record of it, as stated
next.)*

**Provenance of this signature, stated plainly.**
- The owner gave these answers **directly to the top-level session**, through a multiple-choice
  prompt, on 2026-10-21.
- The top-level session relayed them to the manager, and the manager relayed
  them to this `product-manager` (`a72fdf8fc4f04cb64`), which recorded them here.
- **Neither the manager nor this `product-manager` received them from the owner directly.** This
  document holds a relayed record and has not seen the owner's own words. The primary evidence is
  whatever the top-level session retains of that prompt and its answer.
- The relayed answer for Gate 0 is *"Gate 0: SIGNED"*, with the Q-done text in §0.8. No separate
  per-checkbox answers were given. The ticks above record that **the signature covers this block as
  written** — the criteria, assumptions, re-derived requirement and blocking questions as they
  stood when signed. They are not four independent confirmations.
- Rulings recorded with this signature: **Q-scope (a)**, **Q-seam (d)**, **Q-delegation (b)** and
  **Q-done (a)** — verbatim text at each question in §0.8.
- Not ruled: Q-window, Q-filing and Q-sequencing stay **OPEN** for Gate 1. Q-mutation, Q-E2E and
  Q-pins are delegated to the team.
- This signature authorizes requirements only. It authorizes no implementation, no production
  change, no merge and no window decision.

---

## Plan v1

*~~Not drafted. Drafted only after Gate 0 is signed, when the manager delegates it.~~ Drafted
2026-10-21 by `product-manager` on the manager's delegation during `/council-plan` Step 1, after
Gate 0 was recorded as signed (relayed record). The author's agent ID is stamped in *Agent
provenance* when the manager supplies it.*

> **What Plan v1 is.** It is a proposal for the council to review. It does not authorize
> implementation, a production change, a commit, a merge, a ledger edit or a
> qualification-window decision. Items marked **TEAM proposal** are delegated technical choices
> under Q-delegation (b). The council reviews them and Plan v2 settles them; none of them is an
> owner ruling. Items marked **OWNER decision** stay with the owner and are carried to Gate 1. **Signed
> Section 0 is not amended anywhere below.** Where the measured evidence refines a §0.5
> criterion, that refinement is a plan-level reading, and it is flagged for the owner at Gate 1.

### v1.0 Evidence base and base refresh

**Measured evidence cited throughout:**
[`artifacts/u1_followup_1/seam_probe/EVIDENCE.md`](../../artifacts/u1_followup_1/seam_probe/EVIDENCE.md)
(gitignored, local only) and the files beside it: `probe_tests/vs-harness.js`,
`probe_tests/vs-cases.js`, `probe_tests/vs-real.test.js`, `probe_tests/vs-mocked.test.js`,
`mutation/run_mutations.py`, `mutation/matrix_round1.tsv`, `mutation/matrix.tsv` and
`vitest_list.json`. **It was produced by the top-level session
`a1cc95d8-4001-4af7-83f4-01d37ee356cc`, not by an agent.** It resumed a probe scaffold that session
`e09a8b9f-…` had left unrun (EVIDENCE.md header). This document cites it as **measured evidence**:
this `product-manager` read the files but did not re-run anything.

**Base refresh record (K13 re-derivation).** Per EVIDENCE.md *Base*:

- The re-derivation in §0.2–§0.3 was refreshed against `origin/main` =
  **`43f5df3357e0c8d9a1e7e3c050eb57ad1af5b538` (#540)**.
- **Delta from Section 0's base `1f5ae0f0`:** three paths only. They are
  `.github/workflows/ci.yml` (the Operation A Windows step only, `-n 4 --dist load`),
  `docs/ci_cd_expansion/PLANNING.md` and `tests/test_worktree_ci_contracts.py`. EVIDENCE.md states
  that none of them touches this packet's surface.
- **Blobs the probe ran against**, verified by `git hash-object` on the copies and stated identical
  at both `43f5df33` and `1f5ae0f0`:
  - `static/js/modules/volume-splitter.js` `6fc3da556e437a05f5687864cc7d92fa6fb537a7`
  - `static/js/modules/toast.js` `2cfc123aba0a3d4e9c4ced4f3316415471ca703c`
  - `static/js/modules/fetch-wrapper.js` `6268765ade4b246b679b53a78f143b5a2ca77da1`
  - `vitest.config.js` `c16ca428f7478708d8dd96a20ebcb86f98a8b935`
  - `package.json` `b61713d3…` and `package-lock.json` `a5f6ed6c…` (vitest 5.0.5, jsdom 30.1.3)
- Also stated unchanged: `tests/test_vitest_inventory_contracts.py` `877bb838…` and
  `static/js/app.js` `c6754a85…`.
- **Consequence: every §0.3 line citation still holds at `43f5df33`.** No Section 0 text needed
  repair.
- **Implied rather than listed:** `templates/volume_splitter.html` (`29bc9e5a…`),
  `docs/test_inventory/TEST_INVENTORY.json` (`2a0834b1…`) and `TEST_INVENTORY.md` (`6dc7331d…`) are
  not named in EVIDENCE.md's unchanged list. They follow from the stated three-path delta. Sequence
  step 2 re-verifies them directly.

**Line citations in this plan.** `path:N` keeps Section 0's meaning: line N of that file at
`1f5ae0f0`, which the delta above makes identical at `43f5df33`. The source is the byte-exact
`origin/main` snapshot whose blob OIDs are listed in that session's `om\_MANIFEST.txt`. ⚠️ The shared
main checkout's working tree is dirty and is **not** a valid base. Its copies of `QUALITY_GATE.md`,
`PARALLEL_WORKFLOW.md`, `PLAN_REVIEW_TEMPLATE.md` and `tests/test_vitest_inventory_contracts.py` are
known to differ from `origin/main`. For example, the working-tree `PARALLEL_WORKFLOW.md` puts the
tracked-DB rule at `:82-89`, while `origin/main` has it at `:96-108`. Where this plan relied on a
working-tree read, it says so.

### v1.1 Goal

**Goal:** add `static/js/modules/__tests__/volume-splitter.test.js`, so that a pure-logic regression
in the Volume Splitter calculate-failure state machine (T-1 to T-4 in §0.3) reds the Vitest tier,
with **no production JavaScript change and no user-visible behavior change**. This discharges
U1-FOLLOWUP-1 under Q-done (a).

### v1.2 Scope

- **In**
  - The new Vitest file, one file, 23 cases (v1.4), with its fixture, fakes and harness inline.
  - The pin update in `tests/test_vitest_inventory_contracts.py` (TD-4, a TEAM proposal).
  - Regeneration of `docs/test_inventory/TEST_INVENTORY.{json,md}` on the final rebased base.
  - This planning document, tracked in the implementation PR, with an implementation record
    appended.
  - The §v2.14 in-place annotation and the queue-row update, as the owner decides under Q-filing.
  - Local, gitignored mutation evidence under `artifacts/u1_followup_1/` (TD-2).
- **Out** (unchanged from §0.7, restated for the plan)
  - Any change to `static/js/modules/volume-splitter.js`, `toast.js`, `fetch-wrapper.js`,
    `vitest.config.js`, `package.json`, `package-lock.json`, `ci.yml`, branch protection, any E2E
    spec or `e2e/fixtures.ts`, or any of the 13 existing Vitest files.
  - The fallback export (v1.3).
  - U3b's retired KI-011 helper coverage of `toast.js`.
  - Q4, D2 and C4 themselves.
  - The §13.0 ledger row (owed through §13.0's own process; see Q-window).
  - Any database change. The **tracked-DB commit rule** in
    [`PARALLEL_WORKFLOW.md`](../ai_workflow/PARALLEL_WORKFLOW.md) §*Tracked-DB commit rule*
    (`:96-108`, cited by F32) applies unchanged. It is referenced here, not restated.
  - Coverage thresholds and new devDependencies.

### v1.3 Seam — Q-seam (d) as ruled, now measured

- **Measured result:** all four targets are reachable through `initializeVolumeSplitter()`, with
  production JS byte-identical (EVIDENCE.md *Results* item 1). Both probe variants passed 23/23
  (46 total) with `vitest run` exit 0 in about 1.4 s.
- **Order independence:** 46/46 on each of 5 shuffled seeds (1, 7, 42, 1234, 99999) plus 3 plain
  repeats (item 2).
- **Collection:** `vitest list --staticParse=false --json`, the generator's collector, exits 0 and
  lists the cases as `describe > it` strings (item 3; `vitest_list.json`).
- **Therefore the ruling's fallback export is NOT triggered.** No production export is proposed,
  and no symbol-naming owner approval is needed or sought.
- **If unreachability is discovered later**, for any target, at any stage (implementation, rebase
  or review), the ruling's separate path applies unchanged. The work stops, the measured
  unreachability is reported, and a **separate owner approval naming the symbols** is required
  before any `static/js/**` production line changes. That approval is not a team decision, and the
  council cannot grant it.
- **Seam mechanics, as measured** (`vs-harness.js`):
  - The DOM is a jsdom fixture reduced from `templates/volume_splitter.html` plus the `#liveToast`
    markup. `#history-body` is deliberately placed outside `.volume-insights-panel`, so that the
    no-panel case (2b) does not also break the history load at init.
  - `fetch-wrapper.js` is mocked with `vi.hoisted()` + `vi.mock()`. Each `api.post` call queues one
    controllable deferred. `api.get` resolves `{data:{}}`, which satisfies the init-time
    `/api/volume_history` call (§0.10).
  - A global `bootstrap` fake provides a `Toast` class with an element-to-instance registry and a
    `getInstance` spy, plus a no-op `Modal`.
  - Each case gets `vi.resetModules()` and a fresh `import()`, following the Packet C precedent
    (F16).
  - Fake timers are installed per case, for the 300 ms debounce and the action-expiry timer. This
    is new technique for this repository (F20).
  - `console.error` is spied and silenced per case.
  - The drivers are the real listeners: Calculate click, Reset click, region Retry, toast action,
    mode `change`, slider `change`, and debounced slider `input`.

### v1.4 The test file — structure, case list, and N

**One file**, `static/js/modules/__tests__/volume-splitter.test.js`:

- A `// @vitest-environment jsdom` docblock (the per-file opt-in, F14).
- The harness is inlined. The probe's four-file split existed only for the A/B comparison
  (EVIDENCE.md *Observations*, last bullet).
- **One** toast variant, chosen under TD-1.
- Four `describe` blocks, one per target.

**Proposed identity format.** The `describe` titles are `T-1 region idempotence`, `T-2 announce
condition`, `T-3 request-sequence guard` and `T-4 probes and dismiss guard`. The probe's
`(criterion N)` suffix is dropped from the titles. Case titles keep their `2a…5e` labels, which
trace to §0.5. The final strings are fixed in Plan v2. `Test Inventory Drift` pins each
`describe > it` identity, so the strings must not change after regeneration.

**State reset (criterion 6), stated mechanism:**

- `document.body.innerHTML` is replaced with the fixture before every case.
- `vi.resetModules()` runs, then fresh imports of `volume-splitter.js` and, under TD-1, `toast.js`
  in the same module-registry generation. This resets all eight module-level bindings (F9) and
  `toast.js`'s own module state.
- The `fetch-wrapper.js` mocks are reset.
- The `bootstrap` fake is re-installed, and `globalThis.bootstrap` is deleted in `afterEach`.
- Fake timers are installed per case and cleared and restored in `afterEach`.
- The `console.error` spy is restored.

**Authoring rule (criterion 6, negatives).** Every negative assertion is paired with a positive one
showing that the failure reached the state machine. Examples:

- a sentinel row removed by `clearResults()`;
- the `request failed` log count;
- a getter spy proving the stale chain reached the guard;
- the region present or absent;
- the announcement count before the negative.

The probe's `// positive:` comments mark each pairing, and the deliverable keeps them.

**Announcement-shape check (criterion 3, last sentence).** It runs in `afterEach` over every
announcement whose message equals `CALCULATE_ERROR_MESSAGE`. The rule learned in round 1 is
carried as an authoring rule: **a shape check must never filter on the property it asserts.** The
probe's mocked variant filtered on `type === 'error'`, which hid mutation `M8j`.

**N = 23 cases.** Case-to-criterion map, with the mutations each case kills in round 2
(`mutation/matrix.tsv`; identical in both variants):

| Case | §0.5 criterion | Discriminating content | Kills (round 2) |
|---|---|---|---|
| 2a repeat failure keeps the same single node and does not rewrite text | 2 | Node identity (`toBe`), an empty `MutationObserver` record, no `aria-live`, `id`/`data-testid`/`type`/`aria-label`; positive: 2 announcements | M5, M5b, M5d, M8 |
| 2b no `.volume-insights-panel`: no region, nothing throws | 2 | Positive: announced once and logged once | M5c |
| 2c-success next success removes the node from the DOM | 2 | `isConnected === false`, not merely hidden; positive: success painted | M6 |
| 2c-reset reset removes the node from the DOM | 2 | As above; positive: the slider reset to 0 | M6, M6b |
| 3a explicit commands announce while region AND our message stand | 3(a) | Calculate, region Retry, toast Retry action and `setMode()` each announce (5 total) | M8, M8h, M8i |
| 3b slider-originated first failure announces (change) | 3(b) | The observable outcome of 3(b) | — (shape check only) |
| 3b slider-originated first failure announces (debounced input) | 3(b) | Reaches calculation only after 300 ms of fake time | — (shape check only) |
| **3b-after-recovery** slider failure after a success announces although our message text persists | **3(b), refinement** | Region gone and message still standing, so **only `!standing` is true** | **M8b, M8e** (sole killer), M6 |
| 3c slider repeat while region and our message stand does NOT announce | 3(c) | Positive: sentinel cleared and failure logged, for both `change` and debounced `input` | M8d, M8f, M8g |
| 3d slider repeat after a stranger replaced our message DOES announce, button still standing | 3(d) | Replacement keeps the button but changes the message (F13) | M8c, N11 |
| 3d-near-miss message probe is exact equality | 3(d), 5 | A message with a suffix appended does not count as ours | M8c, N11, P5 (sole killer) |
| 3e slider repeat after our button is gone but our message stands does NOT announce | 3(e) | Auto-hide/expiry divergence (F13) | N11, M8d, M8f |
| 4a stale SUCCESS after a newer failure: no paint, no region removal, no dismiss | 4 | Getter spy proves the stale chain ran | M9, M9d |
| 4b stale REQUEST FAILURE after a newer success: no region, no announce | 4 | Positive: still painted | M9b, M9d |
| 4c stale POST-2xx HANDLING FAILURE after a newer success: no region, no announce | 4 | Getter spy | M9, M9d |
| 4c-control a CURRENT post-2xx handling failure does enter the failure state | 4 (positive) | Pairs 4c | M9e |
| 4d reset while in flight, then the request fails: no region, no toast | 4 | Positive: reset ran | M9b, M9c |
| 4d-handling reset while in flight, then a post-2xx handling failure: no region, no toast | 4 | Getter spy | M9, M9c |
| 5a both stand: success hides the toast | 5 | `getInstance(#liveToast)` then `hide()` | M6, P6 |
| 5b action probe is scoped to `#liveToast`: button OUTSIDE `#toast-body` still counts | 5 | The binding `#liveToast` scoping | M6, P1, P6 |
| 5c only the button stands (stranger message): NOT hidden | 5 | Dismiss-guard message half | M6, P3 |
| 5d only the message stands (button gone): NOT hidden | 5 | Dismiss-guard action half | M6, P4, P7 |
| 5e a same-label button OUTSIDE `#liveToast` does not count as ours | 5 (scoping) | Decoy outside the toast | M6, P2, P4, P7 |

`M8j` (toast type `error` → `warning`) is killed in every announcing case through the `afterEach`
shape check.

**Observation for the council.** The two first-failure `3b` cases discriminate no matrix mutation
except through the shape check. They are kept because §0.5 3(b) names their observable outcome, and
because the debounced case is the only one that proves the 300 ms `input` path reaches a
calculation. The council may want a debounce mutation, for example a delay of 300 → 400. Such a
mutation is **not measured**, and adding one is a TD-2 question.

**Criterion 3(b) — plan-level refinement, flagged for owner attention at Gate 1.** §0.5 3(b)
reads: *"A slider-originated first failure (`!standing`) announces."* The measurement shows that
**on a first failure the `!standing` disjunct is masked.** No toast has been shown yet, so
`!ourMessageStands()` is also true. Mutations `M8b` (drop `!standing`) and `M8e` (read `standing`
after render) therefore **survived round 1 in both variants** (`matrix_round1.tsv`). Only a
**failure → success → slider-failure** sequence isolates the disjunct. In that sequence the success
removes the region, and the message span persists after the hide (F13), so `!standing` is the only
true disjunct. That is probe case `3b-after-recovery`, which kills both mutations in round 2.

The plan therefore reads 3(b) as satisfied **jointly**: the two first-failure cases cover the
criterion's stated outcome, and `3b-after-recovery` covers its stated disjunct, which criterion 3's
own "one case per disjunct" and criterion 7 require. **Section 0 is not edited.** At Gate 1 the
owner is asked to confirm this reading of 3(b), or to say how 3(b) should be read instead.

### v1.5 TEAM proposals under Q-delegation (b) — for the council to review, not owner rulings

**TD-1 — the toast sub-choice within Q-seam: real `toast.js` (probe variant A).** Proposed: import
the real `toast.js` behind the `bootstrap` fake, and do not mock it.

| | Variant A — real `toast.js` | Variant B — mocked `toast.js` |
|---|---|---|
| Measured | 23/23; 29/29 killed in round 2, all reverted runs green | 23/23; 29/29 killed in round 2, all reverted runs green |
| Round 1 | Survivors `M8b` and `M8e` only (shared with B) | Also `M8j`, a defect in the test's own model |
| How the divergences of F13 are produced | **By `toast.js` itself.** A stranger's message is `showToast('info', …)`, which KI-011 lets keep our button. Button-gone is advancing 3001 ms so `toast.js`'s own expiry timer removes it. | By the test author's model. `setMessage` sets a variable, and `buttonGone` removes a node. |
| Blind spot (EVIDENCE.md *Observations*) | Depends on `toast.js`'s 3000 ms action-expiry timer to model auto-hide. The announced type is observed indirectly, as `bg-danger` on `#liveToast`. | *"Encodes its own model of the toast DOM (it would not notice a `toast.js` contract change)"* |

Rationale for A:

- T-4 is the divergence between two probes that query `toast.js`'s **real output**
  (`#toast-body span.toast-message`, and a Retry button inside `#liveToast`).
- Variant B certifies `volume-splitter.js` against a hand-built model of that output. Its round-1
  survivor shows the model can be wrong without anything failing.
- If `toast.js` drifts in a way that breaks the probes in production, A goes red and B stays
  green. That is the false-green class this packet exists to close.
- A's blind spots fail **loudly**. Each case asserts its arrangement first, for example
  `expect(liveToastBtn()).toBeNull()` after the 3001 ms advance. A timer change therefore reds an
  arrangement assertion. It does not silently pass a negative.

Points for the council to test:

1. **Q-scope boundary.** Q-scope (a) excludes `toast.js` internals. Variant A *uses* `toast.js`
   behavior to arrange cases, but its only `toast.js`-internal **assertion** is `danger: true`
   (`bg-danger`), which stands in for criterion 3's "type `error`". Is that within Q-scope (a)?
2. **Unmeasured refinement.** A pass-through partial mock
   (`vi.mock('../toast.js', async (importOriginal) => …)`, wrapping the real `showToast` in a spy)
   would let the announced type be asserted on the call itself while the real DOM behavior is kept.
   This is **not measured**. If the council adopts it, it must be measured, including the full
   matrix, before Plan v2 relies on it.
3. **Cross-packet coupling.** A future `toast.js` change that alters the action-preservation
   behavior, the expiry timer or the `error` → `bg-danger` mapping would red this file. That PR
   would then have to touch a Vitest case, which is itself a Vitest corpus change.

**TD-2 — Q-mutation: option (a), the measured 29-mutation matrix, re-run on the final file.**

- **Scope.** The 29 mutations in `mutation/run_mutations.py`:
  - T-1 (6): M5, M5b, M5c, M5d, M6, M6b;
  - T-2 (11): M8, M8b, M8c, N11, M8d, M8e, M8f, M8g, M8h, M8i, M8j;
  - T-3 (5): M9, M9b, M9c, M9d, M9e;
  - T-4 (7): P1–P7.

  This includes §0.8's minimum: U1's M5 and M6 (region), M8 and U3b's N11 (announce), M9
  (sequence), and dismiss-guard narrowing mutations (P3, P4, P7).
- **Both directions.** Each mutated run must exit non-zero, and each reverted run must exit 0. A
  clean baseline run comes first.
- **Exact anchors.** Each mutation is an exact single-occurrence replacement. An anchor that occurs
  other than once is recorded as a **harness failure**, never as a kill.
- **Judged by process exit code.** The JSON reporter's failing-case names are diagnostic only.
- **Copies only.** Mutations run against copies of `volume-splitter.js` in a throwaway tree under
  `artifacts/u1_followup_1/mutation/` in the implementation checkout, never against the repository
  file (§0.5 criterion 7). The raw outputs stay local and gitignored. The summary table goes into
  the PR body and this document's implementation record.
- **Re-run on the final file.** Consolidating four probe files into one is a code change, so the
  probe's round-2 result is evidence about the *probe*, not the deliverable. The matrix is re-run
  against the final single file, which runs 29 mutated and 29 reverted runs plus the baseline.
- **Round-1 history carried forward.**
  - `M8b` and `M8e` survived in both variants. They are fixed by `3b-after-recovery`.
  - `M8j` survived in the mocked variant only, because the shape filter hid it. That is fixed by
    filtering on the message; under TD-1 the fix is moot, but the authoring rule in v1.4 carries
    the lesson forward.
  - Round 2 killed 29/29 in both variants: 58/58 mutated runs exited 1, and 58/58 reverted runs
    exited 0.
- **Mechanism gap to close at implementation.** EVIDENCE.md does not record how the probe tree's
  `node_modules` was provisioned. The runner reads `PROBE/node_modules/vitest/vitest.mjs`. The
  implementation must state its mechanism, and must not run `npm ci` in the shared main checkout.

**TD-3 — Q-E2E: option (a), leave every E2E arm unchanged.** The Vitest file is additive.
`e2e/volume-splitter.spec.ts` (`a1`–`a6`, `b1`, `c1`–`c2`, `s1`–`s3`, `s6`, `t1`–`t12`, `t5b`;
F29) and `e2e/volume-progress.spec.ts` must pass, and both spec files must be byte-identical
(criterion 8). Rationale, as in §0.8: jsdom approximates the live-region, focus and Bootstrap
lifecycle behavior that the E2E arms measure. The reduced fixture also cannot see template drift,
and only the E2E arms run the real `templates/volume_splitter.html`.

**TD-4 — Q-pins: option (a), pins moved in the same PR.** ⚠️ **Caveat carried from §0.8:** Q-pins
is treated as delegated on the **coordinator's reading**. The relayed Q-delegation gloss names
*"seam details within Q-seam, mutation scope and E2E handling"* and does not name the pins. **If
the owner disagrees, Q-pins reverts to an owner decision at Gate 1.**

**Corpus totals:** **13 → 14 files; 245 → 268 cases (245 + N, N = 23).**

**Exact edits to `tests/test_vitest_inventory_contracts.py`.** Line numbers refer to blob
`877bb838…`, read from the `origin/main` snapshot:

1. `:59` `EXPECTED_TOTAL_CASES = 245` → `EXPECTED_TOTAL_CASES = 268`
2. `:60` `EXPECTED_TOTAL_FILES = 13` → `EXPECTED_TOTAL_FILES = 14`
3. Insert one entry into `EXPECTED_PER_FILE` (`:61-75`) in sorted position, between `:70`
   (`"static/js/modules/__tests__/user-profile-data.test.js": 12,`) and `:71`
   (`"static/js/modules/__tests__/workout-controls-persistence.test.js": 35,`):
   `    "static/js/modules/__tests__/volume-splitter.test.js": 23,`

The three assertions stay exact equalities (`:136-139`, `:142-144`, `:541-551`), and the 13
existing entries are unchanged. The edit adds no pytest node, so the per-file pytest count of this
file is unchanged.

**Flagged separately, beyond option (a)'s literal three edits:** the module docstring at `:4` reads
*"13 files, 245 cases"*. The file's own precedent is the parenthetical *"(231 until the KI-010
toast fix …)"* at `:5-7`, which updated that prose rather than leave it false. Proposed: the same
treatment, giving `14 files, 268 cases` with a parenthetical `(245 until U1-FOLLOWUP-1 …)`. This
is prose, not an assertion, and the council or owner may strike it. The illustrative `245` in the
comment at `:104` stays as it is.

**Other pins.** A grep of `tests/` for `245` and `total_cases` found no other Vitest pin. ⚠️ That
grep was a **working-tree read** and must be re-run on the implementation base, under §0.8 Q-pins
(a)'s *"any similar pin found on fresh `origin/main`"*.

### v1.6 Live coordination facts — RELAYED by the top-level session (2026-10-21), UNVERIFIED by this council

Neither the manager, this `product-manager` nor the reviewers can reach GitHub. **Every item below
is relayed and unverified.** Each must be **verified live before Gate 1, and again before
implementation starts** (Sequence steps 0 and 1).

- **L1. PR #544** (open, reported CLEAN) writes JS-unit ledger rows **65–113** into STEP12 §13.0
  and edits the OPEN_WORK §0.4 row. It reports that the
  `2026-08-27T23:18:21Z` → `2026-09-10T23:18:21Z` cycle crossed **with no red**. That is the
  evidence §0.8 Q-window option (d) asked for, and another session is recording it through §13.0's
  own process.
- **L2. PR #547** (open, reported CLEAN) records an owner decision of 2026-10-21:
  - **D2 approved conditionally.** It becomes effective once §13.0 records that cycle with zero
    adverse `JS Unit` job conclusions, which means once #544 lands.
  - The **Q4 rename to `JS Unit (Vitest)`** is approved, and it lands in its own change before
    protection.
  - **C4** (settings activation, i.e. branch protection) needs separate approval.

  The owner's text is in #547's `docs/r23_js_unit_promotion/DECISION.md`. That file is not on
  `main` and was not readable here.
- **L3.** A peer session (`hypertrophy-toolbox-v3-main-ee`) announced the landing order
  **#541 → #542 → #543 → #544 → #547**, with the Q4 rename queued behind #546 and A3. **#541, #544
  and #547 edit `docs/OPEN_WORK_EXECUTION_PLAN.md`**, which is Q-filing's target.
- **L4.** **PRs #545** (WS3 app-factory) and **#546** (CI B2 residuals) both modify
  `docs/test_inventory/TEST_INVENTORY.{json,md}`. That is a whole-file artifact this packet must
  regenerate.
- **L5.** The same peer session logged a dated addendum in the gitignored
  `WORKSTREAM_OWNERSHIP.local.md`. It is **coordination, not an owner ruling**, and it says:
  - U1-FOLLOWUP-1 lands only after the owner's timing decision.
  - Of U1-FOLLOWUP-1, #545, #546 and the Q4 rename, **whichever merges second regenerates
    `docs/test_inventory/*`**.
  - When U1-FOLLOWUP-1 lands, the ledger owner must re-check Q2's window-restart rule, because it
    is the first Vitest corpus change since T0.

**One working-tree observation that bears on regeneration** (session git snapshot, not verified on
`origin/main`): the shared main checkout holds untracked files under `docs/ai_workflow/`
(`WORKSTREAM_OWNERSHIP.local.md.lock`, `WORKTREE_CLEANUP_PLAN.md`). That directory is a globbed
parametrized surface. QUALITY_GATE's `Test Inventory Drift` row (`:71`) forbids regenerating while
an untracked or gitignored `.md` sits in such a directory. This is a further reason the main
checkout is not a valid place to regenerate.

### v1.7 OWNER decisions for Gate 1 — restated against L1–L5

§0.8's options stay readable at §0.8 and are not rewritten there. Below, each question is restated
against the relayed facts. Every option keeps the same caveat: **the facts are unverified until
checked live.** Each question stays an **owner decision**, and each recommendation is the team's,
not a ruling.

#### Q-window — restated

**What the texts say:**

- F3 / §v2.14 (`volume_failure_feedback/PLANNING.md:1303-1306`): *"once the strict mark passes,
  landing this packet restarts the *next* window; it does **not** retroactively void a
  qualification cycle that completed successfully before it."*
- The 2026-08-29 ruling (`STEP12_JS_UNIT_GATE0.md:5181-5182`): its *"eventual post-mark landing
  does not retroactively invalidate a successfully completed qualification cycle."*
- Q2 (`:210`): the window runs *"from the first successful `JS Unit (Vitest, non-required)` run on
  `main` after the final expansion packet lands."*
- The ruling defines *"final expansion packet"* relative to **"this qualification window"**
  (`:5170-5172`).

**Team reading, for the owner to confirm or correct.** Landing after #544 and #547 cannot void the
completed 245-case cycle that conditional D2 rests on. Three reasons:

- That cycle is past, and its job conclusions are fixed.
- #431 remains the final expansion packet *for that window*.
- U1-FOLLOWUP-1 engages Q2 only for the **next** window.

What the texts do **not** settle is whether anything is gated on that next window. The open
question is **C4**: does activating protection for the context require a fresh 14-day window on the
**14-file / 268-case** suite? The owner should answer that before the ledger owner has to infer it
(L5).

**The Q4 rename.** Q2 and the T0 record (`:5200`) match the job on its **exact** context string. A
rename therefore changes the name any next window is read under. It does not affect the completed
cycle, because that cycle is already recorded under the old name.

**Restated options:**

- **(a) Land when the gates pass, without waiting for #544 or #547** (§0.8 (a)). If it lands before
  #544, that ledger PR must be re-extended to cover this merge's run. The ledger owner would then
  apply Q2 to a corpus change in the middle of recording the cycle that D2's condition names.
- **(b) Hold until both #544 and #547 have merged, then land.** This replaces §0.8 (b) and (d):
  #544 is the ledger evidence that (d) asked for, and #547 is the R2.3 decision that (b) waited
  for. D2 is then effective on the recorded 245-case cycle before the corpus moves.
- **(c) As (b), landing before C4 activation, with an owner ruling now that C4 does NOT require a
  fresh window on the 14-file suite.** This restates §0.8 (c) as a ruling about C4, since #547
  appears to have settled D2 itself.
- **(d) As (b), landing before C4 activation, with C4 waiting for a fresh 14-day window.** The
  window would run from U1-FOLLOWUP-1's first successful post-merge `JS Unit` job. This delays C4
  by at least 14 days.
- **(e) Add-on to (b), (c) or (d): also wait for the Q4 rename to land first**, so that this
  merge's row and any next window are read under one name. The cost is a dependency on #546 and A3
  (L3).
- **(f) Hold until after C4 activation.** U1-FOLLOWUP-1 then lands under a required `JS Unit`
  check, and the window question is moot. The cost is that the new file's first Linux runs on
  `main` are already merge-blocking for every PR. EVIDENCE.md measured Windows only (*Base*, last
  bullet).

**Also to confirm (§0.8 carried forward):**

- **Who owes the post-merge §13.0 row.** Team proposal: the ledger owner, through §13.0's own
  process. A PR cannot record its own landing (F25), and §0.4 says *"Write rows only through the
  §13.0 process"* (F24). This packet records the post-merge job reading as its own Q-done evidence
  in this document's implementation record. That reading is taken at job level (`conclusion`,
  `completed_at`), under the exact job name in the merge commit's `ci.yml` blob, with the landed
  blobs proven by SHA (U3b precedent, F25). The packet does not write the §13.0 row.
- **Whether a red is a stop condition.** Team proposal: **yes.** Under Q-done (a), a red post-merge
  `JS Unit` job means the packet is not done. The work stops and is reported to the owner, with no
  re-run-to-green without the owner. The ledger owner records the red as it stands. Under (c) or
  (d), whether C4 proceeds after a red is the owner's call.
- **That D2 is not reopened.** The owner is asked to state that U1-FOLLOWUP-1's landing does not
  reopen D2's conditional approval. That gives the ledger owner a ruling to apply rather than one
  to make (L5).

**Team recommendation: (c), without (e)** unless the Q4 rename has already landed by the time the
PR is ready.

- (b)'s ordering keeps the corpus change out of the cycle that #544 records and #547's condition
  names.
- Landing before C4 gives the 14-file suite non-blocking Linux runs on `main` before it becomes
  required.
- An advance ruling on C4 follows F3's text and spares the ledger owner an inference.
- Ordering relative to the rename is neutral for correctness, because the post-merge job is read
  under the name in the merge commit's own `ci.yml`. A dependency on A3 would hold the packet for
  an unrelated reason.
- Choose **(d)** if a window on the exact suite being protected matters more than C4's timing.
  Choose **(f)** if C4's timing matters most.

#### Q-filing — restated

**Live facts (unverified):** #541, #544 and #547 edit `OPEN_WORK_EXECUTION_PLAN.md`, and #544
edits the very §0.4 row this packet would update (L1, L3). `OPEN_WORK_EXECUTION_PLAN.md` also
carries a docs-cleanup claim (F34).

**One further live check.** AGREED_PLAN's folder review lists `volume_failure_feedback` among the
folders whose live conditions are to be retained and reconciled. It must be checked live whether
any WS1 slice (#541–#543) moves or splits `docs/volume_failure_feedback/PLANNING.md`. If one does,
the §v2.14 annotation targets the post-slice path.

**Queue row:**

- (a) Do not file in §4 or §7, and update the §0.4 row **in the implementation PR**. That PR then
  has to be rebased after #541, #544 and #547, and coordinated with the docs-cleanup claim.
- **(a2) New: do not file, and update the §0.4 row in a post-merge status PR** once #541, #544 and
  #547 have landed. That PR cites the merge SHA and the post-merge `JS Unit` reading.
- (b) Also file a §4 or §7 packet entry.
- (c) Neither.

**§v2.14:** (i), (ii) or (iii), unchanged from §0.8.

**Team recommendation: (a2) + (i).**

- (a2) keeps the implementation PR's diff off a file with three concurrent editors and a claim.
- It lets the row state facts the implementation PR cannot know at merge time: its own merge SHA
  and post-merge result. This is the same reason a PR cannot record its own ledger row.
- (i) keeps U1's record honest at merge time, and the status PR adds the merge SHA.
- Under Q-done (a), "records annotated" is then complete only when that status PR merges.
- The PR body links §v2.14 under every option (F1).

#### Q-sequencing — restated

**Options (a)–(d) are as in §0.8.** The live facts add four points:

- the peer addendum's *"lands only after the owner's timing decision"* (L5), which is consistent
  with Q-window staying with the owner;
- the whole-file inventory contention with #545, #546 and the Q4 rename (L4, L5);
- the untracked files in `docs/ai_workflow/` that make the main checkout unsafe for regeneration
  (v1.6), which weighs further against option (c);
- the unverified state of `scripts/new-worktree.ps1` creation (§0.11), which affects option (b).

**New sub-choice, applicable to (a)–(c):**

- **(i)** Implementation may start after Gate 1. The PR is opened as a **draft** and held from
  merge until the Q-window landing conditions hold.
- **(ii)** Implementation starts only once those conditions hold.

Under either, the rebase and regeneration step (Sequence step 11) runs against the then-current
`origin/main`.

**Team recommendation: (a) with (i).** The isolation standard and the dirty, shared main checkout
are unchanged from §0.8. Rebasing a small additive file is cheap, and a draft PR blocks no one.
Under every option, a live freeze and blocked-recovery check, plus a path claim in the gitignored
local claim file, come before any test runs (§0.9 item 3).

### v1.8 Artifacts

| Path | Change | Notes |
|---|---|---|
| `static/js/modules/__tests__/volume-splitter.test.js` | new | 23 cases; jsdom; real `toast.js` (TD-1); mocked `fetch-wrapper.js`; global `bootstrap` fake; fresh module per case |
| `tests/test_vitest_inventory_contracts.py` | modify | TD-4: three pin edits, plus the separately flagged docstring prose |
| `docs/test_inventory/TEST_INVENTORY.json` | regenerate | Never hand-edited. Vitest block goes to 14 files and 268 cases, with 23 new identities. Other sections change only if a sibling PR landed first (L4) |
| `docs/test_inventory/TEST_INVENTORY.md` | regenerate | Totals row `\| JS unit cases (Vitest) \| **268** across 14 files \|` and one new per-file row |
| `docs/u1_followup_1_vitest/PLANNING.md` | new (tracked in the PR) | This document, plus an appended implementation record (blob proof, gate results, mutation summary) |
| `docs/volume_failure_feedback/PLANNING.md` | modify, annotated in place | Only per Q-filing §v2.14; never rewritten; the path is subject to the WS1-slice check |
| `docs/OPEN_WORK_EXECUTION_PLAN.md` | modify | Only per Q-filing; under the recommendation, in a **post-merge status PR**, not the implementation PR |
| `artifacts/u1_followup_1/**` | local, gitignored | Mutation tree and raw outputs; never committed |

**Byte-identical to the verified base (proved by blob SHA in the PR):** `volume-splitter.js`,
`toast.js`, `fetch-wrapper.js`, `vitest.config.js`, `package.json`, `package-lock.json`,
`templates/volume_splitter.html`, `static/js/app.js`, all 13 existing Vitest files,
`e2e/volume-splitter.spec.ts`, `e2e/volume-progress.spec.ts` and `.github/workflows/ci.yml`.

**Not touched by this packet:** STEP12 §13.0 (owned by the ledger owner) and the committed
`docs/MASTER_HANDOVER.md` (a never-claimed shared path; any edit needs per-edit coordination, F34).

**PR description obligations:**

- Link §v2.14 explicitly (F1).
- State "no user-visible behavior change" (§0.4; `CLAUDE.md` §1).
- Migration notes: none owed, because the calculation surface is `none`.
- Include the mutation summary and the byte-identity proof.

**Effort:** **M.** The code is small (one test file, three pin lines and a regenerated artifact).
The coordination is not: inventory contention, the ledger, and owner-timed landing. ·
**Owner (implementer):** proposed `senior-developer`, writing all three code artifacts in one
checkout. `automation-qa`'s write boundary is `tests/**` and `e2e/**` (AUTONOMY.md *Workflow
roles*), which excludes `static/js/**/__tests__/`. The council is asked to confirm the role
assignment. · **Depends on:** Gate 1; the Q-window landing conditions; the live verification of
L1–L5; the Q-sequencing checkout.

### v1.9 Sequence

0. **Gate 1.** The owner signs Plan v2 with Q-window, Q-filing and Q-sequencing answered. The owner
   also confirms or overrides TD-4's delegation and the criterion 3(b) reading. **L1–L5 are
   verified live before the signature.**
1. **Pre-implementation live check.**
   - Re-verify L1–L5 and the state of the Q4 rename and C4.
   - Confirm that no open PR or session touches `volume-splitter.js`, `toast.js`,
     `static/js/modules/__tests__/` or `docs/test_inventory/` beyond L4 (§0.9 item 6).
   - Run the freeze and blocked-recovery check, and record the path claim (§0.9 item 3).
2. **Checkout and base verification.** Create the checkout chosen under Q-sequencing. Record the
   base `origin/main` SHA, and re-verify against it:
   - every blob listed in v1.0 and in the byte-identical list in v1.8;
   - the inventory at 13 / 245.

   **Any drift in `volume-splitter.js` or `toast.js` is a stop condition.** The case list and the
   mutation anchors would need re-deriving, which goes back to the council. Drift elsewhere is
   reported and assessed before continuing.
3. **Author** the single file by consolidating the probe's harness, cases and variant A. Make no
   production edit.
4. **Run it.** Run the file alone, then the full corpus (`npm run test:js`, which must read 14
   files / 268 cases with exit 0). Also run the shuffled seeds and repeats from v1.3. Then confirm
   byte-identity.
5. **Mutation matrix (TD-2)** on copies under `artifacts/`: a baseline run, then 29 mutated and 29
   reverted runs. The result must be 29/29 killed and 29/29 reverted green, with no anchor
   failures. Record the summary.
6. **Pins and inventory.**
   - Apply the TD-4 edits.
   - Confirm that no untracked or gitignored `.md` sits in a globbed surface directory.
   - Regenerate with `python scripts/generate_test_inventory.py`.
   - `--check` must exit 0.
   - Run `tests/test_vitest_inventory_contracts.py`, then full pytest.
   - Run the pyright baseline diff, which must show no net-new diagnostics, because a `.py` file is
     in the diff.
   - `tsc --noEmit` must report zero errors.
7. **E2E.** Run Chromium `volume-splitter.spec.ts` and `volume-progress.spec.ts` against the
   checkout's own isolated DB and server, with both spec files byte-identical.
8. **Records.** Make the §v2.14 annotation per Q-filing, and append the implementation record here.
9. **Diff-time gate: `/unslop`.** The change-type table requires no reviewer for `static/js/**` or
   `docs/**`, and has no row for `tests/**`. Any additional reviewer is an **owner option**,
   proposed here and not assumed (`CLAUDE.md` §3, *Reasoning effort is not agent authorization*).
10. **Commit and PR.** Open the PR as a draft under Q-sequencing (i), with the description
    obligations from v1.8. On CI:
    - all required contexts must be green;
    - `JS Unit (Vitest, non-required)` must be green, which is the **first Linux measurement** of
      the new file;
    - `Test Inventory Drift` must be green.

    The PR is never auto-merged.
11. **Rebase and regeneration before the merge request.** This runs after any of #545, #546 or the
    Q4 rename has landed first (L4, L5), and again if `origin/main` moves before merge.
    - Rebase onto the then-current `origin/main`.
    - Re-verify the step 2 blob set. **Stop on drift** in `volume-splitter.js` or `toast.js`.
    - Regenerate the inventory on the rebased tree, and never merge an older artifact.
    - Re-run steps 4 and 6.
    - Re-run the Linux CI.
12. **Merge request.** Once the Q-window landing conditions hold, ask the owner for merge
    confirmation **naming the PR** (Q-done (a); QUALITY_GATE `:24-30`).
13. **Post-merge.**
    - Read the merge commit's push run at job level: `conclusion` and `completed_at`, under the
      exact job name in that commit's `ci.yml`.
    - Prove the landed blobs by SHA, and record both here.
    - Notify the ledger owner that the §13.0 row is owed, and that Q2's restart rule is to be
      applied per the owner's Q-window ruling.
    - **A red stops the work** (Q-window).
14. **Q-filing follow-through.** Under (a2), open the post-merge status PR: the §0.4 row, plus the
    merge SHA into the §v2.14 annotation.
15. **Done** per Q-done (a).

### v1.10 Expected gates

*Draft by `product-manager`, built as the union of the planning gates and the implementation gates
(QUALITY_GATE `:16`); for `test-strategist` to confirm or correct.*

- **Vitest:** the new file alone; `npm run test:js` (14 / 268, exit 0); 5 shuffled seeds plus 3
  repeats; the mutation matrix (TD-2).
- **pytest:** `tests/test_vitest_inventory_contracts.py`, then **full pytest** (§0.5 criterion 9).
  The only `.py` change is the pin file, which has no change-type row, so the criterion governs.
- **Inventory:** regenerate, then `scripts/generate_test_inventory.py --check` exits 0
  (`Test Inventory Drift`, QUALITY_GATE `:71`, `:80`).
- **Type Check:** `tsc --noEmit` reports zero errors. EVIDENCE.md item 4 shows that `tsconfig.json`
  covers only `e2e/**/*.ts` and `playwright.config.ts`, so the new file sits outside `tsc`, but the
  required context still runs. The pyright baseline diff must show no net-new diagnostic
  (QUALITY_GATE `:72`, `:97-98`).
- **E2E (Chromium):** `volume-splitter.spec.ts` and `volume-progress.spec.ts`, from the feature map
  (QUALITY_GATE `:50`, `:146`).
- **Manual smoke / `/verify`:** not applicable. There is no production or user-visible runtime
  change, and the Frontend (JS) row's smoke applies only *"if interactive"*. The council may
  dispute this.
- **CI:** all required contexts, plus the non-required `JS Unit` job on the PR (the Linux
  evidence).
- **Byte-identity:** blob-SHA comparison of the v1.8 list against the verified base.

### v1.11 Risks and stop conditions

| # | Risk | Handling |
|---|---|---|
| R1 | **Linux is unmeasured** (EVIDENCE.md *Base*). jsdom, fake timers and the 20-step microtask `flush()` have only been run on Windows with Node v24.20.0 | The PR's `JS Unit` run is the first Linux evidence. Any Linux-only failure or flake **stops** the work before a merge request |
| R2 | **`flush()` depth.** A future production `await` could leave a chain unresolved | Negatives are always paired with positives (v1.4), so an under-flushed case fails loudly rather than passing vacuously. The council may test this claim |
| R3 | Coupling to `toast.js` behavior under TD-1 | Accepted as the deliberate trade-off in TD-1. Such failures are loud, and the PR that changes `toast.js` owns the follow-on |
| R4 | Fidelity of the reduced fixture | The E2E arms remain the oracle for the real template (TD-3) |
| R5 | Whole-file inventory contention with #545, #546 and the Q4 rename | Sequence step 11 |
| R6 | Q2 interpretation at landing | An owner ruling in advance under Q-window. The ledger owner applies it and does not infer one |
| R7 | Coupling to log strings (`'Volume calculation: request failed'`, `'… response handling failed'`) used as positive evidence | A change to those strings reds the file, loudly. Noted for the council |
| R8 | New technique: fake timers (F20) | Installed and restored per case, and order independence was measured (v1.3) |
| R9 | **Unreachability discovered later** | Stop. Revert to the Q-seam ruling's separate owner approval naming the symbols (v1.3) |

### v1.12 Evidence gaps (Plan v1)

- **The seam evidence is a session's measurement, not an agent's.** This council read
  EVIDENCE.md and its files but re-ran nothing. Every number in v1.3–v1.5 is quoted from it.
- **Linux not measured** (EVIDENCE.md *Base*).
- **Probe-tree provisioning unrecorded.** How `node_modules` reached the probe tree is not
  recorded (TD-2).
- **Implied rather than listed.** The blobs of `templates/volume_splitter.html` and the two
  inventory files at `43f5df33` follow from the stated delta and are not listed (v1.0).
- **All of L1–L5 are relayed and unverified.** #547's `DECISION.md` was not readable. The exact
  conditions of D2 and C4 are therefore known only through the relay.
- **Working-tree reads.**
  - The grep for other Vitest pins (TD-4) was taken on the working tree.
  - The untracked-file observation in v1.6 comes from the session's git snapshot.
  - Every other line citation above is to the `origin/main` snapshot (`1f5ae0f0`, unchanged at
    `43f5df33` per the delta).
- **Role coverage.** No role charter was found that names `static/js/**/__tests__/` as a write
  path (v1.8).
- **WS1-slice impact.** Whether #541–#543 touch `docs/volume_failure_feedback/PLANNING.md` is
  unknown (Q-filing).

---

## Agent provenance

*Placeholder. The manager supplies every ID; none is invented here.*

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Section 0 | `a72fdf8fc4f04cb64` | Author of Section 0. ID supplied by the manager, as recorded when the `Agent` call returned. |
| `senior-developer` — `origin/main` snapshot extraction | `a12fcd9e8fa11c72c` | Extracted the byte-exact `origin/main` `1f5ae0f0` copies under the session scratchpad `om\` folder that Section 0 cites. Read-only git; each blob OID and size verified per `_MANIFEST.txt`. Not a council role. ID supplied by the manager. |
| `product-manager` — Plan v1 | `a1dca7baa596ca062` | Fresh product-manager spawned by the manager for Plan v1; ID supplied by the manager as recorded when the Agent call returned. |
| `product-manager` — response matrix + Plan v2 | `a1dca7baa596ca062` | The same agent that wrote Plan v1, resumed by the manager via `SendMessage` to the recorded Plan v1 ID. The ID was supplied by the manager. |
| `architecture-reviewer` | `a14fb858eb881b5c5` | Step 2 reviewer. Verdict: sound, with concerns (4 findings). The ID was supplied by the manager as recorded when the `Agent` call returned. |
| `test-strategist` | `aa900ede7f79be449` | Step 2 reviewer. Verdict: concerns, not blocking (12 findings). The ID was supplied by the manager as recorded. |
| `product-risk-reviewer` | `aa61d8d4ffe59e712` | Step 2 reviewer. Verdict: concerns, not blocking (8 findings). The ID was supplied by the manager as recorded. |

**Same product-manager resumed for the matrix + Plan v2?** **yes.** The manager resumed it via
`SendMessage` to the Plan v1 agent ID `a1dca7baa596ca062`.

**Evidence gap.** The continuity of the council itself has no gap. The gap is scoped to these five
points:
> - The council was orchestrated by a manager subagent spawned from the top-level session
>   `a1cc95d8-4001-4af7-83f4-01d37ee356cc`. The manager does not know its own agent ID, so that
>   ID is not recorded.
> - The seam probe and the mutation matrices (`artifacts/u1_followup_1/seam_probe/`) were run by
>   that top-level session, not by an agent, so they have no agent ID.
> - Section 0's `product-manager` (`a72fdf8fc4f04cb64`) belongs to a prior session and was not
>   resumed. Plan v1 is new work by a fresh `product-manager`.
> - The reviewers' background output files were empty. Their reports reached this document as the
>   manager's verbatim paste in its resume message, so this `product-manager` has not seen the
>   reviewers' original outputs. No reviewer was re-run, and no completed council work was rerun.
> - No reviewer could read `origin/main` or GitHub. All three read the shared dirty working tree
>   and said so.
>
> No ID was invented.

---

## Reviewer findings

*Pasted verbatim from the manager's resume message (2026-10-21). Only heading levels were changed so
that the text nests under this section. The reviewers' background output files were empty, and the
texts below are the manager's verbatim paste (see* Agent provenance → Evidence gap*). Each reviewer
read the shared working tree, not `origin/main`.*

### architecture-reviewer (agent `a14fb858eb881b5c5`)

**Verdict: sound, with concerns.** There are no blocking findings. The plan has no module-boundary, blueprint-registration, schema, API-contract, logger, DB-access or normalization hazards. It adds no Python route or util and no table, and it changes no production JS. The architecture-level concerns are the harness's cleanup ordering, the pin-file line citations that I could not check against origin, and one scoping rule for the single-file layout.

**Limits of this review**
- I could not read `origin/main`. All reads were of the shared working tree.
- I re-ran nothing. Every measured number comes from `EVIDENCE.md`.
- Linux and Node-version behaviour is unmeasured. The plan already says so (R1).
- `tests/test_vitest_inventory_contracts.py` in the working tree matches the plan on three points:
  - the `:59` and `:60` literals;
  - the 13-entry map at `:61-75`;
  - the equality assertions at `:136-144`.
- It does not match on the Markdown assertions. The plan cites them at `:541-551`. In the working tree they sit at `:496-519`.

**Findings**

1. **Medium. The probe's `afterEach` runs its assertion before its cleanup.**
   - Plan location: v1.4 "State reset" and "Announcement-shape check".
   - Evidence: `probe_tests/vs-cases.js:29-35` calls `A.assertAnnouncementShapes()` first. Only afterwards do `vi.clearAllTimers()`, `vi.useRealTimers()`, `errorSpy.mockRestore()` and `delete globalThis.bootstrap` run.
   - Risk: when a shape check fails, the throw skips the cleanup. Fake timers, the console spy and the `bootstrap` global then leak into the next case. One real regression would show up as a cascade of unrelated reds, and the later reds would depend on case order. That works against the file's own order-independence claim. This is the only place the "stated reset mechanism" can fail; the cleanup is otherwise sound.
   - Fix: say in v1.4 that cleanup is unconditional. Run the shape check inside `try`/`finally`, or put it in a separate `afterEach` that is registered so it runs before the cleanup hook. Then add a measured check that a deliberately failing shape check does not contaminate the following case.

2. **Low. The fake `bootstrap.Toast.hide()` never fires `hidden.bs.toast`, so case 3e's "auto-hide" is only the expiry-timer path.**
   - Plan location: v1.4 cases 3e and 5d. TD-1 says the button-gone arrangement is "advancing 3001 ms".
   - Evidence:
     - `vs-harness.js:74` has `hide() { h.log.push(...) }` and does not dispatch the event.
     - `toast.js:165-171` removes the action on `hidden.bs.toast`, and `toast.js:153` removes it on a per-action timer.
     - `volume-splitter.js:275-279` describes the auto-hide case as "an auto-hide leaves the message but takes the button".
   - Risk: the case is tied to the 3000 ms default duration and the timer path. The hidden-event path, which is what real Bootstrap auto-hide produces, is not exercised. A change to the duration default would red the file loudly. A change that breaks only the `hidden.bs.toast` wiring in `toast.js` would pass silently. That wiring is outside scope, but the plan calls the case "auto-hide".
   - Fix: either have the fake's `hide()` dispatch `hidden.bs.toast` on the element, and use that as the button-gone arrangement for 3e and 5d, or keep the timer arrangement and rename the plan wording to "action expiry". If the dispatch is adopted, measure it. It is unmeasured today, and it needs a full matrix re-run.

3. **Low. Make "keep the harness inline" a binding rule, and give the reason.**
   - Plan location: v1.4, "The harness is inlined".
   - Evidence:
     - `vitest.config.js:44-45` sets coverage `all: true`, includes `static/js/**/*.js` and excludes only `*.test.js`.
     - `QUALITY_GATE.md:62` treats `static/js/**/*.js` as an inventory-drift trigger, because a module that throws on import breaks collection.
   - Risk: the probe's `vs-harness.js` and `vs-cases.js` are non-test files. If an implementer copies that split into `__tests__/`, those files become unmeasured "production modules" in the coverage denominator and in the inventory-drift trigger. The plan states the inlining but gives only the A/B-comparison reason.
   - Fix: add a sentence that no non-`*.test.js` helper may be added under `static/js/**`, citing the config and the gate row.

4. **Low. The TD-4 line references for the Markdown assertions can't be confirmed from here.**
   - Plan location: F28 and TD-4.
   - Evidence: the working tree has `test_markdown_totals_row_is_pinned` at `:500` and `test_markdown_lists_every_vitest_file_with_its_count` at `:507`. The plan cites `:541-551`. The working copy is known to differ from `origin/main`, so this is expected.
   - Risk: none to the design. The edit set is correct either way, because the Markdown assertions are driven by the same three constants.
   - Fix: sequence step 2 should re-read the pin file's blob and re-derive the line numbers. The three edits should be described by symbol (`EXPECTED_TOTAL_CASES`, `EXPECTED_TOTAL_FILES`, one new `EXPECTED_PER_FILE` entry), with line numbers as hints.

**Answers to the plan's questions**

- **Toast sub-choice: use the real `toast.js` (variant A).**
  - The mocked variant hand-builds the toast DOM. Its `M8j` survival in round 1 shows the model can be wrong without anything failing.
  - The `exercises.test.js` precedent explicitly forbids `importActual` partial mocks (`exercises.test.js:12-16`). That counts against the unmeasured pass-through partial mock in TD-1 point 2. Reject it unless it is fully measured; I don't see a need for it.
- **Q-scope boundary for the `bg-danger` assertion: acceptable.** It is the only `toast.js`-internal assertion, it stands in for criterion 3's "type error", and it sits in one place (the shape check). Record it as a deliberate exception, and say that a change to the `error` → `bg-danger` mapping is expected to red this file (TD-1 point 3).
- **Seam: the evidence supports "no production export".**
  - There is no `document` or `window` listener, observer or storage use in `volume-splitter.js` (grep returned nothing). Listeners are bound to fixture nodes, which `document.body.innerHTML` replaces each case, so per-case module reset is sound.
  - `vi.resetModules()` followed by a fresh import resets all eight bindings, and `toast.js` keeps its state in the DOM, so it needs no separate reset.
  - The `afterBoot` import of `toast.js` is safe only because `volume-splitter.js`'s own `./toast.js` import was resolved in the same registry generation. The implementer should keep that ordering.
  - The fallback-export path is not triggered, and the plan handles the owner-approval requirement correctly.
- **Export surface:** the module keeps its single `initializeVolumeSplitter()` export, and `static/js/app.js` is untouched. This matches the Packet D / backup-center precedent.
- **Implementer role for `static/js/**/__tests__/`: `senior-developer`.** `AUTONOMY.md:55-59` makes `automation-qa` writes behaviourally limited to `tests/**` and `e2e/**`, and `senior-developer` the code writer. The change also spans the pin file under `tests/` and the generated artifacts, so one writer is cleaner. Independence is supplied by the reviewers and by the mutation evidence, not by role splitting.
- **Layout and inventory:** the layout fits the repo. The file path matches the other 13 files (`static/js/modules/__tests__/*.test.js`). The jsdom docblock, `vi.hoisted` plus `vi.mock` for `fetch-wrapper.js`, the `bootstrap` global fake and re-import after `vi.resetModules()` follow the `exercises.test.js` precedent. `tsconfig.json` excludes `static/js`, so `tsc` is unaffected. The three pin edits and the regeneration are necessary and sufficient. I found no other Vitest pin in `tests/*.py`: grep for `245`, `13 files` and the existing test-file names found only the pin file. That was a working-tree read, which the plan already flags. `.github/workflows/ci.yml` has no per-file `static/js` list.
- **Diff-time review:** I agree with the plan: `/unslop` only, and any further reviewer is an owner option.

**Verified clean**
- The probe's mutation anchors are exact single-occurrence replacements in a copy.
- Round 2's 58/58 killed and 58/58 reverted figures are judged by exit code.
- The plan's reading of criterion 3(b) is correct. `!standing` is masked on a first failure because `ourMessageStands()` is also false then, and only `3b-after-recovery` isolates it.

**Verdict: sound, with concerns.** Resolve finding 1 in Plan v2. Findings 2 to 4 can be settled there as stated dispositions.

### test-strategist (agent `aa900ede7f79be449`)

#### Verdict: concerns (not blocking)

Plan v1 is sound on seam, case list, N, and gate set. It needs these changes before Plan v2:

- **Mutation matrix:** wider, with a stricter kill criterion.
- **`loadPlan` path:** decide whether to cover it or record the exclusion.
- **v1.10 gates:** add the coverage-mode run and the collector-parity caveat.
- **Rebase protocol:** state the rule for pin literals and inventory files.

I did not re-run anything. I counted N, cross-checked the case table against `matrix.tsv`, and read the probe sources and the gate docs.

**Working tree versus `origin/main`.** I can only read the shared working tree, and it is stale or different from `origin/main`. Evidence:
- `package.json:22,27` pins jsdom 30.0.1 and vitest 4.1.11. The plan and EVIDENCE.md say 30.1.3 and 5.0.5.
- The working-tree `docs/test_inventory/TEST_INVENTORY.json` has its Vitest totals at `:1803`. The plan cites `:1831`.
- The working-tree pin file has its Markdown tests at about `:500-510`. The plan cites `:541-551`.

I therefore could not verify any `origin/main` blob OID, any vitest 5.0.5 behavior, or the plan's `origin/main` line numbers. Line numbers in the working-tree `volume-splitter.js` (`:126-232`) do match the plan's citations.

#### Gate map

| Gate | Required? | Notes |
|---|---|---|
| New file alone, `npm run test:js` (14 files / 268 cases), shuffled seeds | Yes | N = 23 confirmed (see finding 11). |
| Mutation matrix | Yes | See findings 2 and 3. |
| `tests/test_vitest_inventory_contracts.py`, then full pytest | Yes | Table has no `tests/**` row. Full pytest is the safe union. |
| `scripts/generate_test_inventory.py --check` | Yes | Regenerate in a clean standalone clone. |
| Type Check (`tsc` plus the pyright baseline diff) | Yes | `tsconfig.json:13` includes only `e2e/**/*.ts` and `playwright.config.ts`, so the new file is outside `tsc`. Pyright is repo-wide whenever a `.py` is in the diff. |
| Chromium `volume-splitter.spec.ts` and `volume-progress.spec.ts` | Yes | The literal glob `static/js/**` includes the test file. The run measures no delta, but the "union, never the weaker set" rule applies. |
| `/verify-suite`, `/build-css`, visual | No | `tests/conftest.py`, `app.py` and the generator script are untouched. |
| Conftest / fixtures | None | No blueprint or table. |
| Known-red | `e2e/program-backup.spec.ts:79` is not in this spec set. | |

#### Findings

1. **Medium. `loadPlan()` is not driven.**
   - Plan location: v1.4, case 3a.
   - §0.3 T-2 names `loadPlan() :360` as a `forceAnnounce=true` path. 3a drives four explicit paths (Calculate, region Retry, toast action, `setMode`), but not that one.
   - `volume-splitter.js:359-360` calls `calculateVolume()` with the default. A mutant passing `{forceAnnounce:false}` there would survive. No such mutation is in `run_mutations.py`.
   - Change: add a case `3a-loadPlan`, reached through an `api.get` history row. That makes N = 24, so 14 files / 269 cases and a per-file pin of 24. Feasibility is unmeasured. Otherwise record the exclusion in Plan v2 so the owner signs it knowingly.

2. **Medium. Several claimed assertions have no killing mutation.**
   - Plan location: v1.4 table and TD-2.
   - The `3b` change and input cases kill nothing (`matrix.tsv`). Likewise, 2a's `type`, `data-testid`, `aria-label` and `firstElementChild` assertions have no mutation. Neither do the afterEach label and `ariaLabel` checks. This is the "arm that cannot be made to fail" standard that criterion 7 cites.
   - Change: measure these additions on the final file, both directions:
     - `prepend` → `appendChild`
     - drop the Retry button's `aria-label`
     - drop `retry.type`
     - action label `'Retry'` → `'Retry now'`
     - alter the message constant
     - delete `exitCalculateFailureState()` at `:164`
     - debounce 300 → 400 (the only mutation that discriminates the `3b` input case)
     - slider `change` listener never calls calculate
   - Any survivor needs a case or a recorded exclusion.
   - The debounce mutation touches a §0.7 non-goal. Use it only as proof that the input case discriminates, not as a coverage target.

3. **Medium. The kill criterion is exit code alone.**
   - Plan location: TD-2.
   - A syntax error or runner crash exits non-zero without any assertion failing. `run_mutations.py:116-129` records failing names as diagnostic only. The measured matrix happens to have non-empty `killing_cases` on every row.
   - Change: make a kill mean exit ≠ 0, plus at least one assertion-level failure in the JSON report, plus no file-level error. Also require anchor count == 1 and mutated bytes ≠ original.
   - This answers the provisioning gap. A tree under `<checkout>/artifacts/u1_followup_1/mutation/` resolves `vitest` and `jsdom` by ancestor `node_modules` lookup. That needs no junction and no `npm ci` in the shared checkout. I have not measured this.
   - The runner hard-codes `PROBE/node_modules/vitest/vitest.mjs` (`:19`) and should be parameterized.

4. **Medium. The R2 claim is overstated for 4b and 4d.**
   - Plan location: v1.11, R2.
   - 4b's "still painted" positive was already true before the stale rejection. 4d's "reset ran" positive precedes the settle. Neither proves the stale chain reached the guard (`vs-cases.js:246,280`). Only the 4a and 4c getter spies do.
   - Reachability for 4b and 4d rests on mutations M9b and M9c, not on in-test positives.
   - Change: reword R2 to say so. Make re-running M9b and M9c on the final file mandatory. Measure the minimum `flush()` depth at which the file passes, and record the margin over 20.

5. **Low-Medium. `hides(h)` counts couple to `toast.js` internals.**
   - Plan location: TD-1 and R3.
   - 5a asserts `toBe(1)` and 5c/5d assert `toBe(0)` on absolute counts (`vs-cases.js:314,333,342,353`). This cuts against Q-scope (a), which excludes `toast.js` internals.
   - Change: assert the delta from a snapshot taken after the arrangement step.

6. **Low. The shape-check rule contradicts the deliverable.**
   - Plan location: v1.4, "Announcement-shape check".
   - Variant A filters on `e.message === MSG` (`vs-real.test.js:24`) and asserts `message: MSG` (`:26`).
   - Change: narrow the rule to "never filter on `danger`, `actionLabel` or `actionAria`". Or filter by announcement identity instead, for example by excluding the test's own stranger shows.

7. **Low. afterEach cleanup is skipped when the shape check throws.**
   - Plan location: v1.4, state reset.
   - `vs-cases.js:29-35` runs the shape assertion first. If it throws, the timers, spy and `globalThis.bootstrap` are not restored. Order independence was measured on green runs only, and leaked state can inflate kill lists.
   - Change: use `try/finally`, or a separate cleanup hook. Do not depend on hook ordering.

8. **Medium. Add a coverage-mode run to v1.10.**
   - CI runs `npm run test:js -- --coverage` (`.github/workflows/ci.yml:985`, with `all: true`). The probe only ran `vitest run`.
   - Change: add one local `npm run test:js -- --coverage`, with fake timers and per-case `resetModules` under v8.
   - Also note that `tests/test_css_cascade_contracts.py:1255,1383,1699` string-scan every `static/js/**/*.js`, including the new file. That is another reason full pytest is the right gate. The fixture has no forbidden strings, but I did not scan it exhaustively.

9. **Low-Medium. Collector parity is overstated.**
   - Plan location: v1.3 and EVIDENCE.md item 3.
   - The probe used `vitest list --staticParse=false --json`, called "the generator's collector". The generator's argv is `npx vitest list --json=<path>` with `CI=true` (`generate_test_inventory.py:249,258-277`). This is a working-tree read, and the file is modified there.
   - Change: treat the probe listing as indicative. The authoritative identities come from the generator at Sequence step 6. Require literal-string titles and no `it.each` or template titles in the final file, so the output is the same under either parser.

10. **Medium. Q-pins and rebase protocol.**
    - **Q-pins (a) is technically right.** The three equalities must move in the same PR. Insertion position is correct, because `user-profile-data` < `volume-splitter` < `workout-controls-persistence`. My working-tree grep found no other Vitest pin. The `origin/main` copy has about 41 more lines, so re-grep there.
    - **Add a rebase rule** to step 11: never textually merge the pin literals or the two inventory files. Regenerate them, and recompute N from `vitest list` independently. If a sibling PR changed the Vitest total, recompute the literals relative to it.
    - **Prose is out of scope.** `docs/MASTER_HANDOVER.md`, `docs/ACTIVE_DEVELOPMENT.md` and `docs/OPEN_WORK_EXECUTION_PLAN.md` carry "245 cases" prose. No test pins it. It belongs to the status PR or ledger owner.

11. **Low. Case list and N.**
    - N = 23 is confirmed: 4 + 8 + 6 + 5 in `vs-cases.js`. 245 + 23 = 268. `vitest_list.json` lists 23 + 23.
    - Every matrix-kill entry in the plan's table matches `matrix.tsv`.
    - Titles are pinned identities. Plan v2 should list all 23 final strings, because the `(criterion N)` suffix is dropped. A rename after regeneration reds `Test Inventory Drift`.

12. **Low. Windows versus Linux.**
    - Nothing in the planned file is platform-conditional. Titles are literals. Sorting is Python-side. Path normalization is already pinned by the contract file.
    - Linux is unmeasured. The first Linux evidence is the non-required `JS Unit` job, and `Test Inventory Drift` on Linux covers collection only. Keep reading the `JS Unit` job conclusion at job level before any merge request (step 10 already does).
    - Implementation needs `npm ci` from the `origin/main` lock in the standalone clone before measuring (see the stale-checkout note above).

#### Answers to the plan's questions

- **Q-mutation:** Option (a) is right, with findings 2 and 3 applied.
- **Q-E2E:** Agree with option (a). The reduced fixture cannot see template drift, and the E2E arms remain the oracle.
- **Q-pins:** Agree with option (a), subject to the `origin/main` re-grep and the rebase rule in finding 10.
- **TD-1 (real versus mocked `toast.js`):** Keep variant A as measured. It is sound.
  - **Q-scope boundary:** the `bg-danger` observation arguably stays inside Q-scope (a), since it is an observation used to arrange and check cases. Finding 5 trims the count coupling.
  - **Partial pass-through mock:** unmeasured, and optional. If adopted, measure the whole matrix first.
- **Manual smoke:** not applicable. Agree with the plan.

### product-risk-reviewer (agent `aa61d8d4ffe59e712`)

**Verdict: concerns.** Nothing blocks Gate 1. The calculation, local-first, terminology and non-goal checks are clean. I found no silent amendment of signed Section 0. The concerns are about how the plan frames owner decisions, mostly in Q-window and the toast boundary.

Two limits on what I could verify:
- I read the working tree, not `origin/main`. The `volume-splitter.js` and `toast.js` citations match exactly (`volume-splitter.js:126-282`, `toast.js:314-317`), and so does §v2.14 (`volume_failure_feedback/PLANNING.md:1276-1318`).
- Other citations are shifted or absent in the working tree, so I could not verify them. `OPEN_WORK_EXECUTION_PLAN.md` has different section positions here. The STEP12 ruling sits about 16 lines earlier than the plan cites. A grep of `QUALITY_GATE.md` for "relay", "owner approval" and "multiple-choice" found nothing, so the owner-approval text the plan cites at `:22-40` is not in this copy.

I did not verify L1–L5 or PRs #541–#547. The plan handles them as unverified.

**Clean checks**
- **Calculation surface `none`:** correct. Nothing under `utils/` is touched, and there is no schema, API or copy change.
- **Informational-only, local-first and non-goals:** nothing at risk.
- **Terminology:** the plan adds no new user-facing copy. `CALCULATE_ERROR_MESSAGE` and "Retry volume calculation" are unchanged.
- **Q-delegation (b) split:** the plan keeps Gates 0 and 1, Q-window, Q-sequencing, Q-filing, the fallback export and the merge with the owner. It labels TD-1 through TD-3 as team proposals. Q-pins is correctly caveated as the coordinator's reading, not the owner's words (plan §0.8 and TD-4).
- **Q-done (a):** respected. The plan makes a separate merge confirmation naming the PR a step (v1.9 step 12).

**Findings**

1. **Medium. TD-1 misstates its own toast.js coupling (`PLANNING.md` v1.5 TD-1, "Points for the council" 1).**
   - **Evidence:** the plan says the only `toast.js`-internal assertion is `danger: true`. But `vs-cases.js:206-208` (case 3e) asserts `liveToastBtn()` is null after `buttonGone()` (a 3001 ms advance, `vs-real.test.js:35`). It also asserts `messageText()` equals the failure message. The plan's own case table and TD-1 rationale say the same (the "asserts its arrangement first" line). Those are assertions on `toast.js`'s action-expiry timer and message persistence. U3b's retired coverage, which Q-scope (a) says this is not a revival of, includes the "expiry timer" (`toast_action_continuity/PLANNING.md:724-729`).
   - **Answer to your question:** the `bg-danger` assertion stays within Q-scope (a). It observes the public output of `showToast('error', …)` (`toast.js:317`) and stands in for criterion 3's "type `error`". It is not coverage of `toast.js`. The arrangement assertions are a closer call. They are guard preconditions for the negatives, not coverage of `toast.js`, and I read them as in scope. They need to be disclosed, though, because the owner ruled "not a revival".
   - **Fix:** in Plan v2, correct the sentence and list every `toast.js`-derived assertion (`bg-danger`, button-gone after 3001 ms, message persistence after hide). Label them arrangement guards and the `bg-danger` check as the criterion-3 shape check. Ask the owner to confirm that reading at Gate 1. Optionally measure the pass-through spy so `type` is asserted on the call itself. The plan already says it is unmeasured.

2. **Medium. The Q-window recommendation (c) is justified on a false premise (v1.7, "Team recommendation: (c)").**
   - **Evidence:** the plan says "An advance ruling on C4 follows F3's text". F3 (`volume_failure_feedback/PLANNING.md:1303-1306`) says landing restarts the next window. Option (c) rules that the next window does not gate C4. That is a waiver of Q2's consequence for the new corpus (Q2, `STEP12_JS_UNIT_GATE0.md:210`, "Defines the D2 precondition").
   - **Second weakness:** the rationale "Landing before C4 gives the 14-file suite non-blocking Linux runs" collapses if C4 activates soon after. The plan prices that cost only under (f).
   - **Scope:** C4 and D2 are out of scope in §0.7. Gate 1 would record a C4 ruling in this packet's PLANNING.md, where the ledger owner may not look.
   - **Fix:**
     - Restate the recommendation as a waiver the owner chooses, not as following F3.
     - Add a minimum-green-runs-on-main alternative before C4, as an owner option.
     - Require that any C4 ruling be recorded in, or cross-linked from, the #547 decision lineage.

3. **Medium. Load-bearing sentences state relayed facts as facts (v1.7 Q-window "Team reading", v1.6 L1–L2).**
   - **Evidence:** "Landing after #544 and #547 cannot void the completed 245-case cycle that conditional D2 rests on" and "#544 is the ledger evidence that (d) asked for" are unhedged. Section 0 F23 ("Q4/D2 is unsigned") and F24 ("not recorded on main") would be stale if L1 and L2 verify. The plan never says so. The v1.6 header and Sequence step 0 do require live verification before Gate 1, which is correct.
   - **Fix:** in Plan v2, give each relayed fact a "verified live / unverified" status. Make the (c) recommendation explicitly conditional on L1 reporting zero red, missing, skipped or cancelled results. State that if L1 does not verify, the fallback is the original (d). Annotate F23 and F24 as potentially superseded without editing them.

4. **Low-Medium. The ledger-row and done-record vehicle is undefined (v1.7 "Also to confirm", Sequence steps 13–14).**
   - **Evidence:** step 13 says to record the post-merge job reading and blob proof "here", but an implementation PR cannot contain post-merge facts. Only the (a2) status PR is a vehicle. Under Q-filing (a) or (c) none exists. Q-done (a) requires "records annotated". The "ledger owner writes the row" split is reasonable (F25: a PR cannot record its own landing). It does depart from U3b T10, where the implementation PR itself owed the row. The plan should say so.
   - **Fix:** name the post-merge docs PR as a Q-done deliverable under every Q-filing option. State the departure from U3b T10 explicitly. Say whether a red post-merge job resets only the next window or also touches the conditional D2.

5. **Low. The 3(b) refinement is handled openly and is not an amendment (v1.4).**
   - **Evidence:** the measurement is sound: `!standing` is masked on a first failure (EVIDENCE.md item 5, round 1 survivors `M8b` and `M8e`). The extra `3b-after-recovery` case is strictly additive. It tightens, not weakens, criteria 3 and 7, and the plan states Section 0 is not edited.
   - **Fix:** at Gate 1, put it to the owner as a standalone question. Plan v2 must not record it as confirmed without the owner's answer.

6. **Low. The Gate 0 provenance chain is the weakest link (Section 0 sign-off).**
   - **Evidence:** the plan discloses that the owner's answers reached the PM through three relays, and that the ticks cover the block as written, not four independent confirmations. That is honest. Gate 1 depends on Gate 0 being valid.
   - **Fix:** have the top-level session retain and quote the owner's verbatim Gate 0 answers. Re-confirm Gate 0 in the same direct prompt as Gate 1.

7. **Low. `/unslop` is called a "diff-time gate" (v1.9 step 9).**
   - **Evidence:** the plan itself says the table requires no reviewer for these paths. `unslop-reviewer` runs only on explicit user request, and CLAUDE.md §3 says optional agents need authorization. The "owner option" caveat in the same bullet contradicts the "gate" label.
   - **Fix:** reword it as an optional owner-authorized step.

8. **Low. Citation basis (v1.0 "Line citations").**
   - **Evidence:** all citations are to `origin/main` blobs read in another session, with the working tree flagged as unreliable. That is correctly disclosed, and it matches the divergences I saw. I could not independently confirm the `QUALITY_GATE.md`, `OPEN_WORK_EXECUTION_PLAN.md` and `STEP12` line numbers.
   - **Fix:** none. Make sure Sequence step 2's blob re-verification also covers the policy docs it cites for gating.

**Plan respects product invariants, but needs revision before Gate 1 on findings 1–4.**

---

## Response matrix

*The dispositions are the manager's synthesis (`/council-plan` Step 3), written here by the
`product-manager`. **Every disposition is proposed, and the owner confirms it at Gate 1.** No finding is
deferred. Two proposals are **rejected** inline, with their rationale: adopting the
`hidden.bs.toast` dispatch (A2), and the pass-through spy (P1, from TD-1). Where this
`product-manager` found that a disposition or finding rests on a misreading of the plan or of a
cited file, the disposition is kept unchanged and a **PM note** is added.*

| ID | Finding (one line) | Reviewer | Disposition | Action in v2 |
|---|---|---|---|---|
| **A1 / T7** (merged) | The `afterEach` shape check runs before cleanup, so a throw leaks timers, the console spy and `bootstrap` into the next case | architecture-reviewer; test-strategist | **accept** — proposed; owner confirms at Gate 1 | Cleanup is unconditional (`try`/`finally`, or a separate cleanup hook that does not rely on hook ordering). A measured negative control is added at implementation (§v2.E rule 1; §v2.L step 4) |
| **A2** | The fake `hide()` never fires `hidden.bs.toast`, so 3e/5d exercise only the action-expiry path, yet the plan calls it "auto-hide" | architecture-reviewer | **accept the wording option; REJECT adopting the dispatch now** — proposed; owner confirms at Gate 1 | The 3e/5d arrangement is renamed "action expiry (`toast.js` per-action timer)". The `hidden.bs.toast` path stays with E2E `t11` (Q-E2E (a)) and lies outside Q-scope (a) (§v2.E rule 6). **Reason for the reject:** the dispatch is unmeasured, would need a full matrix re-run, and adds coupling to `toast.js` internals. *PM note:* `t11` (`e2e/volume-splitter.spec.ts:1508-1550`) runs a real Bootstrap auto-hide end to end and asserts that the button is gone (`:1518-1522`). It does not isolate whether `toast.js` removed the button through `hidden.bs.toast` or through its action timer, so "covered by `t11`" means *exercised*, not *isolated* |
| **A3** | Make "keep the harness inline" a binding rule, and give the reason | architecture-reviewer | **accept** — proposed; owner confirms at Gate 1 | Binding rule: no non-`*.test.js` helper under `static/js/**`, citing `vitest.config.js` coverage `all: true` and the QUALITY_GATE drift-trigger row (§v2.E rule 2) |
| **A4** | The pin-file Markdown-assertion lines could not be confirmed | architecture-reviewer | **accept** — proposed; owner confirms at Gate 1 | Edits are described by symbol, with line numbers as hints re-derived at step 2 (§v2.I). *PM note:* the `origin/main` blob `877bb838…` read for Plan v1 does carry the Markdown assertions at `:541-551`. The reviewer's `:496-519` reading is of the differing working-tree copy. The disposition is unchanged |
| **T1** | `loadPlan()` (`:360`, default `forceAnnounce: true`) is not driven | test-strategist | **accept** — proposed; owner confirms at Gate 1 | Add case `3a-loadPlan` and mutation `M8l` (§v2.F, §v2.H). The target is N = 24. Feasibility is **unmeasured** and is measured at steps 3–4 before the pins are edited. If the path is unreachable without a production change, **nothing is exported**, the exclusion is recorded, N reverts to 23, and the deviation is reported at the merge request |
| **T2** | Several claimed assertions have no killing mutation (the 3b cases, 2a's attributes and position, the label and `ariaLabel` shape checks) | test-strategist | **accept** — proposed; owner confirms at Gate 1 | The eight listed mutations and the T1 mutation are added, measured in both directions on the final file, for a matrix of **38**. A survivor gets a case or a recorded exclusion. The debounce mutation is discrimination-only, and the §0.7 non-goal is untouched (§v2.H) |
| **T3** | Exit code alone is the kill criterion; a crash also exits non-zero | test-strategist | **accept** — proposed; owner confirms at Gate 1 | Kill = exit ≠ 0, plus at least one assertion-level failure in the JSON report, plus no file-level or collection error. Each mutation also needs anchor count == 1 and mutated bytes ≠ original. The runner's vitest path is parameterized. Provisioning via ancestor `node_modules` is recorded as **unmeasured**, with no junction and no `npm ci` in the shared checkout (§v2.H) |
| **T4** | R2 is overstated for 4b and 4d; their positives do not prove that the stale chain reached the guard | test-strategist | **accept** — proposed; owner confirms at Gate 1 | R2 is reworded. Re-running M9b and M9c on the final file is mandatory. The minimum `flush()` depth and its margin over 20 are measured and recorded (§v2.N R2; §v2.L step 4) |
| **T5** | Absolute `hides(h)` counts couple to `toast.js` internals | test-strategist | **accept** — proposed; owner confirms at Gate 1 | Assert deltas from a post-arrangement snapshot (§v2.E rule 4) |
| **T6** | The "never filter on what you assert" rule contradicts variant A's `message === MSG` filter | test-strategist | **accept** — proposed; owner confirms at Gate 1 | Never filter on `danger`, `actionLabel` or `actionAria`. Announcements are identified by **identity**: every `show` not caused by the test's own stranger arrangement. Both the count and the shape check use that identity (§v2.E rule 3) |
| **T8** | CI runs Vitest in coverage mode, but the probe did not | test-strategist | **accept** — proposed; owner confirms at Gate 1 | Add `npm run test:js -- --coverage` to the gates. `tests/test_css_cascade_contracts.py` string-scans `static/js/**/*.js`, which is a further reason for full pytest (§v2.M) |
| **T9** | Collector parity between the probe listing and the generator is overstated | test-strategist | **accept** — proposed; owner confirms at Gate 1 | The probe listing is indicative only; the generator at step 6 is authoritative. Titles must be literal strings, with no `it.each` and no template titles (§v2.E rule 5). *PM note (partial misreading, disposition kept):* the finding reads the generator's argv from the **modified working-tree** `generate_test_inventory.py`. On `origin/main`, the pin file `877bb838…` asserts that the generator's argv contains `--staticParse=false` (`:209`, `:254`) and sets `CI=true` (`:309`). The flag therefore matches. The remaining parity gaps are `npx` resolution and `CI=true`, which is enough to keep the disposition |
| **T10** | Q-pins, the rebase protocol, and "245 cases" prose elsewhere | test-strategist | **accept** — proposed; owner confirms at Gate 1 | Re-grep for Vitest pins on `origin/main` at step 2. Rebase rule: never textually merge the pin literals or the inventory files; regenerate, and recompute N and the totals from `vitest list` relative to whatever a sibling PR landed. This also implements L5. The "245 cases" prose in MASTER_HANDOVER, ACTIVE_DEVELOPMENT and OPEN_WORK is out of scope and goes to the status PR or the ledger owner (§v2.I, §v2.C) |
| **T11** | The titles are pinned identities; list them | test-strategist | **accept** — proposed; owner confirms at Gate 1 | All final titles are listed verbatim (§v2.F) |
| **T12** | Windows versus Linux; `npm ci` | test-strategist | **accept** — proposed; owner confirms at Gate 1 | Run `npm ci` from the `origin/main` lock in the implementation checkout before measuring, never in the shared main checkout. The first Linux evidence is the PR's `JS Unit` job, read at job level (§v2.L steps 2 and 10) |
| **P1** | TD-1 misstates its `toast.js` coupling; `danger: true` is not the only `toast.js`-derived assertion | product-risk-reviewer | **accept; the pass-through spy is REJECTED** — proposed; owner confirms at Gate 1 | The sentence is corrected and every `toast.js`-derived assertion is listed, including the extra ones this PM found (§v2.G). A Gate 1 owner confirmation is added (§v2.O G1-5). **Reason for rejecting the spy:** the `exercises.test.js` precedent forbids `importActual` partial mocks (`:12-16`, per architecture-reviewer); the spy is unmeasured; and it is not needed |
| **P2** | Q-window (c) is justified on a false premise; it is a waiver of Q2's consequence and not "following F3"; C4 is out of scope | product-risk-reviewer | **accept** — proposed; owner confirms at Gate 1 | The claim is withdrawn. Q-window is re-scoped to this packet's own landing, and the new team recommendation is **(b)**. The question of C4 against the next window is **noted, not decided**: the owner is asked to answer it in, or cross-linked from, the #547 / R2.3 lineage before C4 activation. Options (c) waiver, (d) fresh window and (g) minimum green runs stay visible with no team preference, and landing options (e) and (f) keep their costs (§v2.O G1-1) |
| **P3** | Relayed facts are stated as facts | product-risk-reviewer | **accept** — proposed; owner confirms at Gate 1 | A status column is added for L1–L5 (all currently unverified). The (b) recommendation is conditional on L1 and L2 verifying, and the fallback is §0.8's original (d) followed by (a). F23 and F24 are noted as potentially superseded, with no Section 0 edit (§v2.J, §v2.O G1-1) |
| **P4** | The vehicle for the done record is undefined | product-risk-reviewer | **accept** — proposed; owner confirms at Gate 1 | A post-merge docs/status PR is a Q-done deliverable under **every** Q-filing option. The departure from U3b T10 is stated. A new owner question asks whether a red post-merge job resets only the next window or also bears on the conditional D2 (§v2.L steps 13–15; §v2.O G1-1, G1-2) |
| **P5** | The 3(b) refinement | product-risk-reviewer | **accept** — proposed; owner confirms at Gate 1 | Put to the owner as a standalone Gate 1 question, and **not** recorded as confirmed (§v2.O G1-4) |
| **P6** | The Gate 0 relay chain is the weakest link | product-risk-reviewer | **accept as a Gate 1 process recommendation** — proposed; owner confirms at Gate 1 | The top-level session puts the Gate 0 re-confirmation to the owner in the same direct prompt as Gate 1 and keeps the verbatim answers. No Section 0 edit (§v2.O G1-7) |
| **P7** | `/unslop` is called a "gate" while no reviewer is required | product-risk-reviewer | **accept in part** — proposed; owner confirms at Gate 1 | `/unslop` is kept as the diff-time gate (council-plan.md Step 6). It is reworded: for these paths QUALITY_GATE requires no reviewer, so `/unslop` runs the required checks only. `unslop-reviewer` and any further reviewer run only on explicit owner request (§v2.L step 9). *PM note:* the cited `.claude/commands/unslop.md:1-17` and `:17` are a **working-tree read**, since that file is modified in the shared checkout. Its text supports the reading: step 2 runs required checks, and step 3 runs `unslop-reviewer` only on explicit request. "Any further reviewer only on explicit request" comes from `CLAUDE.md` §3, not from `unslop.md:17` |
| **P8** | Citation basis | product-risk-reviewer | **accept** — proposed; owner confirms at Gate 1 | Step 2's re-verification also covers the policy docs cited for gating (QUALITY_GATE, STEP12, OPEN_WORK, AGREED_PLAN, PARALLEL_WORKFLOW, AUTONOMY), with line numbers re-derived from `origin/main` (§v2.L step 2). *PM note:* the owner-approval text the reviewer could not find is present at `origin/main` `QUALITY_GATE.md:22-40` (snapshot blob `e9cb6efa…`), and is absent only from the working-tree copy |
| Plan question — implementer role | `static/js/**/__tests__/` lies outside `automation-qa`'s write boundary | architecture-reviewer (answer) | **accept `senior-developer`** as the single writer — proposed; owner confirms at Gate 1 | §v2.K |
| Plan question — TD-1 toast sub-choice | Real versus mocked `toast.js` | all three (concur) | **variant A, real `toast.js`** — TEAM decision, proposed; owner confirms at Gate 1 | §v2.D |
| Plan questions — Q-mutation / Q-E2E / Q-pins | Delegated technical choices | test-strategist; architecture-reviewer | **(a) / (a) / (a)**, as TEAM decisions under Q-delegation (b), amended per T2/T3/T10 — proposed; owner confirms at Gate 1 | §v2.H, §v2.C, §v2.I. Q-pins keeps its caveat (§v2.O G1-6) |
| Plan questions — Q-filing / Q-sequencing | Owner decisions | product-risk-reviewer (P4) | Team recommendations **kept**: Q-filing **(a2) + (i)**, reinforced by P4, with the WS1-slice path check kept; Q-sequencing **(a) with (i)**, with L5 recorded as coordination, not a ruling — owner decides at Gate 1 | §v2.O G1-2, G1-3 |

No reviewer returned a blocking finding, so no reviewer was re-run.

---

## Plan v2

*Written 2026-10-21 by `product-manager` `a1dca7baa596ca062`, the Plan v1 author, resumed for this
step. It restates Plan v1 with the accepted findings applied. Plan v1 above is left as written, for
the audit trail. **Plan v2 authorizes nothing.** Every "TEAM decision" here is a delegated technical
choice under Q-delegation (b). It is proposed, and the owner confirms it at Gate 1; it is not an
owner ruling. **Signed Section 0 is not amended.***

### v2.A What changed from Plan v1

- **Seam:** unchanged. The toast sub-choice is settled on variant A, and the pass-through spy is
  rejected (P1).
- **N** goes from 23 to a **target of 24**, by adding `3a-loadPlan` (T1). ~~That target is conditional on
  the case being measured as feasible.~~ *2026-10-21: feasibility is measured on the probe
  (EVIDENCE.md §Round 3), and it is re-confirmed on the final file at §v2.L step 4.*
- **Mutation matrix** grows from 29 to **38**, with a stricter kill criterion (T2, T3).
- **Harness rules:**
  - unconditional cleanup (A1/T7);
  - inline-only helpers (A3);
  - announcements identified by identity (T6);
  - delta counts for hides (T5);
  - literal titles (T9);
  - "action expiry" wording (A2).
- **Coupling to `toast.js`:** every assertion derived from it is listed, and the list goes to the
  owner (P1).
- **Gates:** a coverage-mode run is added (T8).
- **Pins** are described by symbol (A4), with an explicit rebase and regeneration rule (T10).
- **Relayed facts** get a verification-status table (P3).
- **Q-window** is re-scoped and its recommendation changes from (c) to (b). C4 is noted, not decided
  (P2).
- **Done record:** a post-merge docs PR is a Q-done deliverable under every Q-filing option (P4).
- **`/unslop`** is reworded (P7). Step 2 also re-verifies the policy docs (P8).

### v2.B Goal

Unchanged from v1.1. Add `static/js/modules/__tests__/volume-splitter.test.js` so that a pure-logic
regression in T-1 to T-4 reds the Vitest tier. There is no production JavaScript change and no
user-visible behavior change. This discharges U1-FOLLOWUP-1 under Q-done (a).

### v2.C Scope

**In**
- The new Vitest file: one file, a target of 24 cases (§v2.F), with its harness inline.
- The pin update in `tests/test_vitest_inventory_contracts.py`, by symbol (§v2.I).
- Regeneration of `docs/test_inventory/TEST_INVENTORY.{json,md}` on the final rebased base.
- This planning document, tracked in the implementation PR, with its pre-merge implementation record.
- The §v2.14 annotation and the queue row, as Q-filing decides.
- The **post-merge docs/status PR**, under every Q-filing option (P4).
- Local mutation evidence under `artifacts/u1_followup_1/` (gitignored).

**Out**
- Everything in v1.2's Out list, unchanged:
  - any production `static/js/**` line, and the fallback export;
  - `toast.js` and the 13 existing Vitest files;
  - E2E specs and fixtures;
  - `ci.yml` and branch protection;
  - Q4, D2 and **C4**;
  - the §13.0 row;
  - DB changes. The tracked-DB commit rule (`PARALLEL_WORKFLOW.md` §*Tracked-DB commit rule*,
    `:96-108`) applies unchanged.
- Also out:
  - the "245 cases" prose in `MASTER_HANDOVER.md`, `ACTIVE_DEVELOPMENT.md` and
    `OPEN_WORK_EXECUTION_PLAN.md`, which is left to the status PR or the ledger owner (T10);
  - the `hidden.bs.toast` dispatch in the fake (A2);
  - the pass-through `toast.js` spy (P1).

### v2.D Seam — TEAM decision within the Q-seam (d) ruling

- The measured result from v1.3 stands: all four targets are reachable through
  `initializeVolumeSplitter()` with production JS byte-identical, so the fallback export is **not
  triggered**. If any target, including `3a-loadPlan`, is later found unreachable, the work
  **stops**, and the ruling's separate owner approval **naming the symbols** applies. Nothing is
  exported on the team's authority.
- **Toast sub-choice: real `toast.js` (variant A).** All three reviewers concur.
- **The import order is load-bearing** (architecture-reviewer). `toast.js` is imported after
  `volume-splitter.js` in the same module-registry generation, so that the test and the module
  share one `toast.js` instance.
- `toast.js` keeps its state in the DOM, so the fixture reset also resets it.
- `volume-splitter.js` installs no `document` or `window` listener, observer or storage use
  (architecture-reviewer grep). Per-case `innerHTML` replacement plus `vi.resetModules()` is
  therefore a sound reset.

### v2.E Test-file design rules (binding for the implementer)

1. **Cleanup is unconditional (A1/T7).**
   - The shape check and the cleanup are separated, so a failing assertion cannot skip the cleanup.
     Use `try`/`finally` inside one `afterEach`, or an equivalent that **does not depend on hook
     execution order**.
   - The cleanup covers:
     - clearing timers and restoring real timers;
     - restoring the `console.error` spy;
     - deleting `globalThis.bootstrap`;
     - resetting the `fetch-wrapper.js` mocks.
   - **Measured negative control, at implementation only, never shipped.** In the throwaway
     mutation tree, force one case's shape check to fail. Then show that the following case runs
     with real timers, a restored `console.error` and a freshly installed `bootstrap` fake, and
     that it passes.
2. **Inline only (A3).** No non-`*.test.js` helper may be added anywhere under `static/js/**`.
   Reasons:
   - `vitest.config.js` coverage uses `all: true`, with `include: ['static/js/**/*.js']` and only
     `*.test.js` excluded (`:41-48`). A helper would therefore enter the coverage denominator as a
     "production module".
   - QUALITY_GATE's drift-trigger row (`:80`) makes every `static/js/**/*.js` an inventory-drift
     trigger.
3. **Announcements are identified by identity, not by an asserted property (T6).**
   - An "announcement" is every `bootstrap.Toast.show()` the fake records that was **not** caused
     by the test's own stranger arrangement. Stranger shows (`showToast('info', …)` in 3d,
     3d-near-miss and 5c) are tagged by the test when it makes them.
   - Both the announcement **count** and the `afterEach` **shape check** use that identity.
   - The shape check asserts all of `message`, `danger`, `actionLabel` and `actionAria`, and
     filters on none of them.
4. **Hides are counted as deltas (T5).** Each T-4 case, and 4a, snapshots the hide count after its
   arrangement step and asserts the change (+1 for 5a and 5b; 0 for 4a, 5c, 5d and 5e). Absolute
   counts are not asserted.
5. **Titles are literal strings (T9, T11).** No `it.each`, no template literals and no computed
   titles. The probe's `vitest list` output is indicative only. The generator's output at §v2.L
   step 6 is authoritative for the pinned identities.
6. **Wording (A2).** The button-gone arrangement in 3e, 5d and 5e is **"action expiry
   (`toast.js` per-action timer)"**: an advance of 3001 ms of fake time. It is not called
   "auto-hide". The fake's `hide()` stays a no-op that only logs.
   - Real Bootstrap auto-hide, including `hidden.bs.toast`, is exercised by E2E `t11`, which TD-3
     leaves unchanged. That path lies outside Q-scope (a).
   - `t11` exercises the path but does not isolate which `toast.js` mechanism removes the button
     (matrix note on A2).
7. **The state reset and the authoring rules from v1.4 carry forward unchanged**, except as amended
   above. Every negative is paired with a positive, and every module-level dependency is reset by
   the mechanism stated in v1.4.

### v2.F Case list, N and totals

**Target N = 24.** That gives **14 files / 269 cases** and a per-file pin of **24**. These values
are still recomputed against the base's own Vitest totals at every rebase (§v2.I). ~~Feasibility of
`3a-loadPlan` is **unmeasured**, so this target is conditional:~~

> ⚠️ **UPDATED 2026-10-21 (post-council measurement; not a reviewer finding; the plan content is
> unchanged) — `3a-loadPlan` is MEASURED FEASIBLE with production JS byte-identical.**
> - Source: [`artifacts/u1_followup_1/seam_probe/EVIDENCE.md`](../../artifacts/u1_followup_1/seam_probe/EVIDENCE.md)
>   §*Round 3*. The top-level session `a1cc95d8-…` ran it, not an agent, and this
>   `product-manager` re-ran nothing.
> - Mechanism, as recorded:
>   - append `button.load-plan[data-plan-id="4"]` to `#history-body`;
>   - a per-URL `api.get` resolves `/api/volume_plan/4` to
>     `{ training_days: 3, mode: 'basic', volumes: { Chest: { weekly_sets: 6 } } }`;
>   - the click produces **exactly one** new `api.post`, so `skipCalculate` is honored;
>   - failing that request produces one new announcement.
> - Result: **24 cases per variant, 48/48 pass, exit 0** (`vs-cases.js` blob `ffd743c8…`, as
>   recorded; this `product-manager` could not hash it).
> - **The N = 23 fallback below is NOT TRIGGERED.** It is kept as written, because the final single
>   file (§v2.E) is still unwritten and must re-confirm the case at §v2.L step 4.
>
> The conditional text below is preserved as it was written:

- **If `3a-loadPlan` is measured feasible** at §v2.L steps 3–4, with production JS byte-identical:
  N = **24**, **14 files / 269 cases**, pin entry **24**, mutation matrix **38**.
- **If it is not reachable without a production change** *(NOT TRIGGERED, per the 2026-10-21
  Round 3 measurement above)*: nothing is exported (Q-seam (d)), the
  exclusion is recorded in the implementation record, and the deviation is reported at the merge
  request. N = **23**, **14 files / 268 cases**, pin entry **23**, mutation matrix **37** (`M8l`
  dropped).

**Feasibility notes for `3a-loadPlan`** (read from the working-tree `volume-splitter.js`, whose
§0.3 line citations the reviewers confirmed match; ~~**⚠️ not a measurement**~~ *2026-10-21: the
mechanism these notes describe is the one Round 3 measured; see the update above*):

- `loadPlan(planId)` (`:334-366`) is reached through the **delegated** click listener on
  `#history-body` (`:100`, `:954-959`), which looks for `.load-plan[data-plan-id]`.
- The case can therefore insert that button into the fixture's `#history-body`. It must replace the
  harness's `api.get` with a **per-URL** mock that resolves `/api/volume_plan/<id>` to a plan.
- `loadPlan()` then calls `setMode(..., { skipCalculate: true })` and then `calculateVolume()`
  (`:359-360`).
- To discriminate `M8l`, the case should:
  - arrange a standing region and a standing message;
  - load a plan;
  - assert **exactly one** new `api.post`, which proves that `skipCalculate` was honored and that
    `setMode()`'s own forced calculation is not masking the result;
  - fail that request;
  - assert one new announcement.

**Final identities (`describe > it`), verbatim.** These are the strings the regenerated inventory
will pin. They must not change after regeneration (T11).

| # | Identity |
|---|---|
| 1 | `T-1 region idempotence > 2a repeat failure keeps the same single node and does not rewrite text` |
| 2 | `T-1 region idempotence > 2b no .volume-insights-panel: no region, nothing throws` |
| 3 | `T-1 region idempotence > 2c-success next success removes the node from the DOM` |
| 4 | `T-1 region idempotence > 2c-reset reset removes the node from the DOM` |
| 5 | `T-2 announce condition > 3a explicit commands announce while region AND our message stand` |
| 6 | `T-2 announce condition > 3a-loadPlan loading a saved plan announces while region AND our message stand` *(~~conditional on feasibility~~ measured feasible 2026-10-21, Round 3; the probe uses the same `it` title)* |
| 7 | `T-2 announce condition > 3b slider-originated first failure announces (change)` |
| 8 | `T-2 announce condition > 3b slider-originated first failure announces (debounced input)` |
| 9 | `T-2 announce condition > 3b-after-recovery slider failure after a success announces although our message text persists` |
| 10 | `T-2 announce condition > 3c slider repeat while region and our message stand does NOT announce` |
| 11 | `T-2 announce condition > 3d slider repeat after a stranger replaced our message DOES announce, button still standing` |
| 12 | `T-2 announce condition > 3d-near-miss message probe is exact equality` |
| 13 | `T-2 announce condition > 3e slider repeat after our button is gone but our message stands does NOT announce` |
| 14 | `T-3 request-sequence guard > 4a stale SUCCESS after a newer failure: no paint, no region removal, no dismiss` |
| 15 | `T-3 request-sequence guard > 4b stale REQUEST FAILURE after a newer success: no region, no announce` |
| 16 | `T-3 request-sequence guard > 4c stale POST-2xx HANDLING FAILURE after a newer success: no region, no announce` |
| 17 | `T-3 request-sequence guard > 4c-control a CURRENT post-2xx handling failure does enter the failure state` |
| 18 | `T-3 request-sequence guard > 4d reset while in flight, then the request fails: no region, no toast` |
| 19 | `T-3 request-sequence guard > 4d-handling reset while in flight, then a post-2xx handling failure: no region, no toast` |
| 20 | `T-4 probes and dismiss guard > 5a both stand: success hides the toast` |
| 21 | `T-4 probes and dismiss guard > 5b action probe is scoped to #liveToast: button OUTSIDE #toast-body still counts` |
| 22 | `T-4 probes and dismiss guard > 5c only the button stands (stranger message): NOT hidden` |
| 23 | `T-4 probes and dismiss guard > 5d only the message stands (button gone): NOT hidden` |
| 24 | `T-4 probes and dismiss guard > 5e a same-label button OUTSIDE #liveToast does not count as ours` |

The criterion mapping from v1.4 carries forward. `3a-loadPlan` maps to §0.5 criterion 3(a) and to
the `loadPlan()` path in §0.3 T-2 (`:360`). The reading of criterion 3(b) is **not** confirmed. It
is a standalone owner question (§v2.O G1-4).

### v2.G Every `toast.js`-derived assertion (P1) — for owner confirmation at Gate 1

This section corrects v1.5 TD-1. The statement there that `danger: true` is *"the only
`toast.js`-internal assertion"* is **wrong**. Every assertion whose truth depends on `toast.js`'s
behavior rather than on `volume-splitter.js` is listed below. The list includes items the
product-risk-reviewer named and further ones this `product-manager` found in
`probe_tests/vs-cases.js` and `vs-real.test.js`.

| Kind | Assertion | Where | Depends on |
|---|---|---|---|
| **Criterion-3 shape check** | `danger: true`, meaning `#liveToast` carries `bg-danger` at `show()` time | `afterEach`, all announcing cases | `showToast('error', …)` mapping the type to `bg-danger` (`toast.js:317`, per product-risk-reviewer) |
| Criterion-3 shape check | `actionLabel: 'Retry'` and `actionAria: 'Retry volume calculation'`, read from `.toast-action-slot > button` | `afterEach` | The action-slot DOM that `toast.js` renders |
| Criterion-3 shape check | `message: MSG`, read from `#toast-body span.toast-message` | `afterEach` | The message span that `toast.js` renders |
| Announcement detection | An announcement is a fake `show()` that the test did not cause (§v2.E rule 3) | every announce count | `toast.js` calling `bootstrap.Toast#show()` |
| Dismiss observation | The hide delta (§v2.E rule 4) | 4a, 5a–5e | `toast.js` having constructed and registered a `bootstrap.Toast` instance for `#liveToast`, so that `getInstance()` finds one |
| **Arrangement guard** | Button **still standing** after a stranger `showToast('info', …)` | 3d, 3d-near-miss, 5c | KI-011 action preservation (`toast.js:296-306`, F13) |
| Arrangement guard | Message text **replaced** by the stranger's | 3d, 3d-near-miss | `showToast()` overwriting the message span |
| Arrangement guard | Button **gone** after 3001 ms | 3e, 5d (5e relies on it without asserting it) | The `toast.js` per-action expiry timer (F13; `:147-155`, `:97-103`) |
| Arrangement guard | Message **still standing** after action expiry | 3e, 5d, 5e | The message span persisting when the action is removed |
| Arrangement guard | Message **still standing** after the success-path dismiss | 3b-after-recovery | The message span persisting across `hide()`. Under the fake, `hide()` is a no-op, so this observes that `toast.js` does not clear the span on the dismiss *call*. It does not observe a real Bootstrap hide |
| Driver | The toast Retry action is clicked through `.toast-action-slot > button` | 3a | The action-slot DOM that `toast.js` renders |

**Team reading, for the owner to confirm at Gate 1 (G1-5).**

- These assertions sit **within Q-scope (a)**, and they are **not** a revival of U3b's retired
  KI-011 helper coverage, which explicitly includes the "expiry timer"
  (`toast_action_continuity/PLANNING.md:724-729`, per product-risk-reviewer).
- The shape checks observe the **public output** of `volume-splitter.js`'s announcement. The
  arrangement guards are **preconditions** that make the paired negatives meaningful. Neither kind
  is a coverage target for `toast.js`, and none appears in the mutation matrix, which mutates only
  `volume-splitter.js`.
- **Accepted consequence:** a change to the `error` → `bg-danger` mapping, to the action-slot
  markup, to KI-011 preservation, to the 3000 ms expiry, or to message-span persistence is
  **expected to red this file loudly**. The PR making that change then owns the follow-on, and that
  follow-on is itself a Vitest corpus change.

### v2.H Mutation matrix — TEAM decision (Q-mutation (a), amended per T2/T3)

**Size: 38 mutations,** or 37 if `3a-loadPlan` proves infeasible *(the 37 fallback is NOT
TRIGGERED, per the 2026-10-21 Round 3 measurement)*. Each runs mutated **and**
reverted, against the final single file, after one clean baseline run.

- **The 29 measured mutations** (`run_mutations.py`):
  - T-1: M5, M5b, M5c, M5d, M6, M6b;
  - T-2: M8, M8b, M8c, N11, M8d, M8e, M8f, M8g, M8h, M8i, M8j;
  - T-3: M9, M9b, M9c, M9d, M9e;
  - T-4: P1–P7.
> ⚠️ **UPDATED 2026-10-21 (post-council measurement) — all 38 mutations are MEASURED on the
> probe.**
> - Source: [`EVIDENCE.md`](../../artifacts/u1_followup_1/seam_probe/EVIDENCE.md) §*Round 3* and
>   `mutation/matrix_round3_38.tsv`; runner blob `e6d741ca…`, as recorded and not hashed by this
>   `product-manager`.
> - **Every anchor occurs exactly once.**
> - **76/76 mutated runs** (38 mutations × 2 variants) exit 1 with at least one assertion-level
>   case failure and no collection error. **76/76 reverted runs exit 0.**
> - `M8l` is killed **only** by `3a-loadPlan`, and `M8n` by `3b`/`3c`. The TSV is consistent with
>   both statements; this `product-manager` read it.
>
> **Scope of that evidence:**
> - It is about the **four-file probe in both variants**, not about the final single file under
>   §v2.E. The full matrix is still re-run on the final file (§v2.L step 5).
> - In the TSV, the "killing cases" column truncates titles to their first token. The two
>   first-failure `3b` cases therefore both read `3b`, and the TSV cannot show which of them kills
>   `M8n`. The final run should record full titles.
> - The runner copy in `artifacts/` derives assertion-level failures from the JSON report's
>   per-case statuses. As read here, it encodes **no** explicit file-level-error check and **no**
>   explicit mutated ≠ original check. Those two parts of the T3 criterion therefore rest on
>   EVIDENCE.md's statement, and on the fact that every replacement string differs from its anchor.
>   The final runner must encode both checks explicitly.
>
> The labels below that call these mutations "unmeasured" are superseded for the probe, and kept
> as written.

- **The 8 added by T2** (~~unmeasured; anchors to be fixed at implementation~~ *measured on the
  probe, 2026-10-21, Round 3; anchors as in the probe runner, re-confirmed on the final file*):
  - `M5e`: region `panel.prepend(region)` → `panel.appendChild(region)`.
  - `M5f`: drop the **region** Retry button's `aria-label` attribute.
  - `M5g`: drop the region Retry button's `type="button"`.
  - `M8k`: the toast action label `'Retry'` → `'Retry now'`.
  - `M8m`: alter `CALCULATE_ERROR_MESSAGE`.
  - `M6c`: delete the success-path `exitCalculateFailureState()` call at `:164`.
  - `M8n`: debounce 300 → 400. This one is **discrimination-only**. It proves that the debounced
    `3b` case discriminates, and it is not a coverage target. The §0.7 non-goal on the debounce is
    untouched.
  - `M8o`: the slider `change` listener never calls `calculateVolume`.
- **The 1 added by T1:** `M8l`: the `loadPlan()` call at `:360` passes `{ forceAnnounce: false }`.

The new identifiers (M5e–M5g, M6c, M8k–M8o) are assigned by this plan and may be renamed at
implementation. Several anchors (`exitCalculateFailureState();`, `'Retry'`,
`'Retry volume calculation'`, `calculateVolume();`) occur more than once in the module. Each one
must carry enough context to occur **exactly once**.

**Kill criterion (T3).** All of the following must hold for a mutation to count as killed:

1. The anchor occurs exactly once in the original.
2. The mutated bytes differ from the original.
3. The mutated run exits ≠ 0.
4. The JSON report shows **at least one assertion-level failure**.
5. The JSON report shows **no file-level or collection error**.
6. The reverted run exits 0, with all cases passing.

A mutated run that exits non-zero only through a crash or a collection error is a **harness
failure**, not a kill. It is fixed and re-run.

**Survivors.** Any survivor gets either a new case, which changes N and is reported before the pins
are edited, or a **recorded exclusion** with its reason. **M9b and M9c must be re-run on the final
file** (T4). They are the only reachability evidence for 4b and 4d.

**Runner and location.** The runner's vitest path is parameterized (T3), replacing the hard-coded
`PROBE/node_modules/vitest/vitest.mjs` at `run_mutations.py:19`. Mutations run on copies in a
throwaway tree under `<implementation checkout>/artifacts/u1_followup_1/mutation/`, never against
the repository file.

**Provisioning (unmeasured).** The tree resolves `vitest` and `jsdom` by ancestor `node_modules`
lookup. That needs no junction and no `npm ci` in the shared main checkout. It is **unmeasured**
and must be confirmed before the matrix runs. *(2026-10-21: Round 3 does not record how the probe
tree was provisioned. This item stays unmeasured.)*

**Recording.** The raw outputs stay local and gitignored. The summary table, with one row per
mutation giving the mutated exit, the reverted exit, the killing cases and any exclusion, goes into
the PR body and this document's implementation record.

**Round-1 history** is carried as recorded in v1.5 TD-2.

### v2.I Pins and the rebase rule — TEAM decision (Q-pins (a), amended per A4/T10)

⚠️ **Q-pins caveat, carried from §0.8:** Q-pins is treated as delegated on the **coordinator's
reading**, not on the owner's words. **If the owner disagrees, Q-pins reverts to an owner decision
at Gate 1** (G1-6).

**Edits to `tests/test_vitest_inventory_contracts.py`, by symbol.** The line numbers are hints from
`origin/main` blob `877bb838…` and are re-derived at step 2.

1. `EXPECTED_TOTAL_CASES` → **245 + N** relative to the base, so **269**, or 268 under the
   fallback (hint `:59`).
2. `EXPECTED_TOTAL_FILES` → **14** (hint `:60`).
3. `EXPECTED_PER_FILE` gains exactly one entry,
   `"static/js/modules/__tests__/volume-splitter.test.js": N` (24, or 23). It goes in sorted
   position after `user-profile-data.test.js` and before `workout-controls-persistence.test.js`
   (hints `:70`/`:71`).

All assertions stay exact equalities, and the 13 existing entries are unchanged.

The docstring prose at `:4` gets the parenthetical treatment flagged in v1.5 TD-4. It stays flagged
as beyond option (a)'s three edits, and the owner may strike it (G1-6).

**Re-grep.** At step 2, re-grep `origin/main` for any other Vitest pin. The `origin/main` copy of
the pin file is longer than the working tree's (test-strategist). Any pin found is reported before
it is edited.

**Totals.** If the Vitest corpus on the base is still 13 / 245: **14 files / 269 cases**, or 268
under the fallback.

**Rebase and regeneration rule (T10; implements L5).**

- **Never textually merge** the pin literals or `docs/test_inventory/TEST_INVENTORY.{json,md}`.
  After every rebase onto a then-current `origin/main`:
  1. Regenerate the inventory from the rebased tree.
  2. Recompute N **independently** from `vitest list` on the new file.
  3. Recompute the literals **relative to the base's own Vitest totals**. If a sibling PR (#545,
     #546, the Q4 rename or another) changed the Vitest corpus, the new totals are that sibling's
     totals plus N, not 245 plus N.
- Whichever of U1-FOLLOWUP-1, #545, #546 and the Q4 rename merges **second** regenerates (L5,
  coordination). This packet regenerates on every rebase regardless.
- **Never regenerate** while an untracked or gitignored `.md` sits in a globbed surface directory
  (QUALITY_GATE `:71`).

### v2.J Relayed coordination facts — verification status (P3)

| Fact | Content (relayed by the top-level session, 2026-10-21) | Status | Bears on |
|---|---|---|---|
| L1 | #544 writes §13.0 rows 65–113 and edits the §0.4 row; it reports that the `2026-08-27T23:18:21Z` → `2026-09-10T23:18:21Z` cycle had no red | ~~**UNVERIFIED**~~ **VERIFIED AS OPEN-PR CONTENT, 2026-10-21, by the top-level session via `gh`** (not a reviewer finding). #544 is **OPEN, not merged**, head `72de3e223aa781603a5a5a6182999e2695de84c8`. Its diff adds 49 §13.0 rows (65–113). In the cycle rows 65–75, every `JS Unit` **job** conclusion is `success`. Row 75's **workflow** conclusion is `cancelled` (`Run Tests` timeout), while its JS job is `success`. **§13.0 on `main` does NOT yet record the cycle** | Q-window (b); F24 |
| L2 | #547 records an owner decision: D2 approved conditionally (effective once §13.0 records the cycle with zero adverse `JS Unit` conclusions); the Q4 rename to `JS Unit (Vitest)` approved, in its own change before protection; C4 needs separate approval. The owner text is in #547's `docs/r23_js_unit_promotion/DECISION.md`, which was not readable here | ~~**UNVERIFIED**~~ **VERIFIED AS OPEN-PR CONTENT, 2026-10-21, by the top-level session via `gh`** (not a reviewer finding). #547 is **OPEN**, head `fea91820179f80bd97edc2d5c7907863ce70c2e1`. Its added `docs/r23_js_unit_promotion/DECISION.md` quotes the owner, 2026-10-21: *"Approve promotion and rename, conditional: D2 takes effect only once the §13.0 ledger records the 2026-08-27 → 2026-09-10T23:18:21Z cycle through its own process with zero red/missing/skipped/cancelled runs. The Q4 rename lands in its own change before any protection change. C4 settings activation stays a separate step needing my separate approval."* On reading the cancellation, it quotes: *"Assess exact JS Unit job conclusions under §13.0"*. **This is a record in an unmerged PR, not on `main`** | Q-window (b); F23 |
| L3 | Landing order #541 → #542 → #543 → #544 → #547, with the Q4 rename behind #546 and A3; #541, #544 and #547 edit OPEN_WORK | ~~**UNVERIFIED**~~ **PARTLY VERIFIED, 2026-10-21, by the top-level session via `gh`.** The `gh` file lists confirm that #541, #544 and #547 each edit `docs/OPEN_WORK_EXECUTION_PLAN.md`. **The landing order itself is peer coordination only** | Q-window, Q-filing |
| L4 | #545 and #546 both modify `docs/test_inventory/TEST_INVENTORY.{json,md}` | ~~**UNVERIFIED**~~ **VERIFIED, 2026-10-21, by the top-level session via `gh`.** The file lists show that #545 and #546 both modify `docs/test_inventory/TEST_INVENTORY.json` and `.md` | §v2.I rebase rule |
| L5 | Peer addendum in the gitignored `WORKSTREAM_OWNERSHIP.local.md`: coordination, **not an owner ruling** | ~~**UNVERIFIED** (contents relayed; this council did not read the file)~~ **VERIFIED, 2026-10-21, by the top-level session.** The addendum is at `WORKSTREAM_OWNERSHIP.local.md:1660`, and it matches the relayed content. It is **coordination, not an owner ruling** | Q-window, Q-sequencing, §v2.I |

**Verification points.** Each fact is verified live **before Gate 1**, and again **before
implementation** (§v2.L steps 0 and 1). The status column is updated in this document when that
happens.

**Possible supersession of Section 0 facts.** If L1 and L2 verify, two Section 0 facts may be
superseded:

- **F23** (*"Q4/D2 is unsigned"*), by #547's conditional D2;
- **F24** (*"not recorded on `main`"*), by #544's rows.

That supersession is a reading of the live state at that time. **Section 0 is not edited.**

### v2.K Artifacts, effort, owner, dependencies

| Path | Change | Notes |
|---|---|---|
| `static/js/modules/__tests__/volume-splitter.test.js` | new | 24 cases (23 under the fallback); jsdom; real `toast.js`; mocked `fetch-wrapper.js` (per-URL `api.get` for `3a-loadPlan`); global `bootstrap` fake; fresh module per case; harness inline (§v2.E) |
| `tests/test_vitest_inventory_contracts.py` | modify | Three pin edits by symbol, plus the flagged docstring prose (§v2.I) |
| `docs/test_inventory/TEST_INVENTORY.json` | regenerate | Never hand-edited; regenerated on every rebase (§v2.I) |
| `docs/test_inventory/TEST_INVENTORY.md` | regenerate | The totals row and one new per-file row follow from the regeneration |
| `docs/u1_followup_1_vitest/PLANNING.md` | new (tracked in the implementation PR) | This document, plus the **pre-merge** implementation record: base SHA, blob proof, gate results, mutation summary, flush-depth measurement, `3a-loadPlan` feasibility |
| `docs/volume_failure_feedback/PLANNING.md` | modify, annotated in place | Per Q-filing §v2.14 option; never rewritten; the path is subject to the WS1-slice check |
| `docs/OPEN_WORK_EXECUTION_PLAN.md` | modify | Per Q-filing; under the recommendation (a2), in the post-merge PR only |
| **Post-merge docs/status PR** | new PR (docs only) | **Q-done deliverable under every Q-filing option (P4).** It carries the merge SHA, the job-level post-merge `JS Unit` reading, the blob proof of what landed, the §v2.14 merge-SHA addition (under (i)), the completion of this document's implementation record, and, under (a2), the §0.4 row |
| `artifacts/u1_followup_1/**` | local, gitignored | Mutation tree, raw outputs and the negative control; never committed |

**Byte-identical to the verified base** (unchanged from v1.8): `volume-splitter.js`, `toast.js`,
`fetch-wrapper.js`, `vitest.config.js`, `package.json`, `package-lock.json`,
`templates/volume_splitter.html`, `static/js/app.js`, the 13 existing Vitest files,
`e2e/volume-splitter.spec.ts`, `e2e/volume-progress.spec.ts` and `.github/workflows/ci.yml`.

**Not touched:** STEP12 §13.0 (owned by the ledger owner) and the committed `MASTER_HANDOVER.md`.

**PR description obligations** (unchanged): link §v2.14; state "no user-visible behavior change";
state that no migration notes are owed; include the mutation summary and the byte-identity proof.

**Effort:** **M.** · **Implementer:** **`senior-developer`** as the single writer (TEAM proposal;
architecture-reviewer concurs). `automation-qa`'s write boundary excludes `static/js/**/__tests__/`
(`AUTONOMY.md` *Workflow roles*). · **Depends on:**

- Gate 1;
- live verification of L1–L5;
- the Q-window landing conditions;
- the Q-sequencing checkout.

### v2.L Sequence

0. **Gate 1.** The owner answers the §v2.O decision list directly and signs Plan v2. L1–L5 are
   verified live before the signature, and §v2.J's status column is updated.
1. **Pre-implementation live check.**
   - Re-verify L1–L5, and the states of the Q4 rename and C4.
   - Check that no other open PR or session touches `volume-splitter.js`, `toast.js`,
     `static/js/modules/__tests__/` or `docs/test_inventory/` beyond L4.
   - Run the freeze and blocked-recovery check.
   - Record the path claim in the gitignored local claim file.
2. **Checkout and base verification (A4, P8, T10, T12).**
   - Create the checkout chosen under Q-sequencing, and record the base `origin/main` SHA.
   - Run `npm ci` from that base's lock, in that checkout only.
   - Re-verify against the base:
     - the code blobs (v1.0 and the §v2.K byte-identical list);
     - the inventory's Vitest totals;
     - the pin-file blob, re-deriving the line numbers and re-grepping for other Vitest pins;
     - the **policy docs cited for gating** (QUALITY_GATE, STEP12, OPEN_WORK, AGREED_PLAN,
       PARALLEL_WORKFLOW, AUTONOMY), re-deriving the cited lines.
   - **Drift in `volume-splitter.js` or `toast.js` is a stop condition** (back to the council).
     Other drift is reported and assessed before continuing.
3. **Author** the single file under §v2.E, including `3a-loadPlan`. Make no production edit.
4. **Run and measure.**
   - Run the file alone.
   - ~~Settle `3a-loadPlan` feasibility first.~~ *2026-10-21: feasibility is measured on the
     probe (EVIDENCE.md §Round 3).* Re-confirm `3a-loadPlan` on the final file first. If it fails
     there without a production change, apply the §v2.F fallback and record it.
   - Run the full `npm run test:js`.
   - Run 5 shuffled seeds and 3 repeats.
   - Run the A1 negative control (§v2.E rule 1).
   - **Measure the minimum `flush()` depth** at which the whole file passes, and record its margin
     below 20 (T4).
   - Confirm byte-identity.
5. **Mutation matrix** (§v2.H): 38 (or 37) mutations, both directions, under the T3 kill criterion.
   Resolve survivors **before** the pins are edited, because a new case changes N.
6. **Pins and inventory.**
   - Apply the edits by symbol, with values recomputed relative to the base (§v2.I).
   - Run the untracked-`.md` check.
   - Run `python scripts/generate_test_inventory.py`. Its output is **authoritative** for the
     identities, which are compared against §v2.F (T9).
   - `--check` must exit 0.
   - Run the pin file, then full pytest, then the pyright baseline diff.
   - `tsc --noEmit` must report zero errors.
   - Run `npm run test:js -- --coverage` (T8).
7. **E2E.** Run Chromium `volume-splitter.spec.ts` and `volume-progress.spec.ts` on the checkout's
   own isolated DB and server, with both spec files byte-identical.
8. **Pre-merge records.** Make the §v2.14 annotation per Q-filing (under (i), with no merge SHA
   yet). Write the pre-merge implementation record in this document.
9. **Diff-time gate: `/unslop` (P7).** For these paths QUALITY_GATE requires **no reviewer**, so
   `/unslop` runs the **required checks only**. `unslop-reviewer` and any further reviewer run only
   on explicit owner request (§v2.O G1-8). None is proposed.
10. **Commit and PR.** Open a draft PR under Q-sequencing (i), with the PR description obligations
    (§v2.K). CI must show all required contexts green, `Test Inventory Drift` green, and the
    non-required `JS Unit` job **read at job level** green. That job is the first Linux evidence
    (T12). Never auto-merge.
11. **Rebase and regeneration** under §v2.I's rule. This runs after any sibling (#545, #546, the Q4
    rename or another) lands first, and again whenever `origin/main` moves before the merge
    request.
    - Re-verify the step 2 set. **Stop on drift** in `volume-splitter.js` or `toast.js`.
    - Regenerate the inventory and recompute the pins.
    - Re-run steps 4 (excluding the matrix, unless an anchored blob changed, which is a stop
      anyway) and 6.
    - Re-run the Linux CI.
12. **Merge request.** Only once the Q-window landing conditions hold, ask the owner for merge
    confirmation **naming the PR** (Q-done (a)).
13. **Post-merge reading.**
    - Read the merge commit's push run at **job level**: `conclusion` and `completed_at`, under
      the exact job name in that commit's `ci.yml` blob.
    - Prove the landed blobs by SHA.
    - **A red stops the work** (§v2.O G1-1).
    - Notify the ledger owner that the §13.0 row is owed, and that Q2's restart rule is to be
      applied as the owner has ruled.
14. **Post-merge docs/status PR (P4)**, under every Q-filing option. It carries the step 13
    readings, the §v2.14 merge SHA (under (i)), the completion of this document's implementation
    record, and the §0.4 row (under (a2)). **The departure from U3b T10, stated (P4):**
    - U3b's implementation PR itself owed its §13.0 row.
    - Here the **ledger owner** writes the §13.0 row, because #544's lineage owns §13.0 (L1,
      unverified) and a PR cannot record its own landing (F25).
    - This status PR's own merge also mints a §13.0 row, owed through the same process.
15. **Done** per Q-done (a):
    - the implementation PR is merged on the owner's named confirmation;
    - the post-merge `JS Unit` job is green;
    - the records are annotated, which includes the step 14 PR being merged.

### v2.M Expected gates

*Union of the planning gates and the implementation gates. The test-strategist's gate map is
adopted, with T8 added.*

- **Vitest:**
  - the new file alone;
  - `npm run test:js` (14 files / 269, or 268), exit 0;
  - 5 shuffled seeds plus 3 repeats;
  - **`npm run test:js -- --coverage`** (T8; CI runs coverage mode with `all: true`);
  - the A1 negative control;
  - the minimum `flush()` depth measurement;
  - the 38- (or 37-) mutation matrix under the T3 kill criterion.
- **pytest:** `tests/test_vitest_inventory_contracts.py`, then **full pytest**. There is no
  `tests/**` row in the table, so the criterion 9 union governs. `tests/test_css_cascade_contracts.py`
  string-scans every `static/js/**/*.js`, which includes the new file (T8).
- **Inventory:** regenerate, then `--check` exits 0, on every rebase (§v2.I).
- **Type Check:** `tsc --noEmit` reports zero errors (the new file is outside `tsconfig.json`'s
  scope). The pyright baseline diff must show no net-new diagnostics (a `.py` is in the diff).
- **E2E (Chromium):** `volume-splitter.spec.ts` and `volume-progress.spec.ts`. The known-red
  `program-backup.spec.ts:79` is not in this set.
- **Not required:** `/verify-suite`, `/build-css`, the visual matrix, conftest or fixture changes,
  and manual smoke or `/verify`, because there is no runtime change.
- **CI:** all required contexts, plus the non-required `JS Unit` job read at job level (the Linux
  evidence).
- **Byte-identity:** blob-SHA comparison against the verified base (§v2.K).

### v2.N Risks, stop conditions and evidence gaps

| # | Risk | Handling |
|---|---|---|
| R1 | Linux is unmeasured | The PR's `JS Unit` job, read at job level, is the first Linux evidence. A Linux-only failure or flake **stops** the work before the merge request |
| R2 | **Reworded (T4).** The pairing of negatives with positives does **not** prove reachability everywhere. For 4b, the "still painted" positive held before the stale rejection. For 4d, "reset ran" precedes the settle. Only the getter spies in 4a, 4c and 4d-handling prove that a stale chain reached the guard | Reachability for 4b and 4d rests on **M9b and M9c**, which are mandatory re-runs on the final file. The minimum `flush()` depth and its margin are measured and recorded. A future production `await` that deepens a chain beyond that margin can still produce a vacuous negative in 4b or 4d. The margin record makes that visible |
| R3 | Coupling to `toast.js` (§v2.G) | Accepted and disclosed. Such failures are loud, and the PR that changes `toast.js` owns the follow-on. The owner confirms the boundary at Gate 1 (G1-5) |
| R4 | Fidelity of the reduced fixture | The E2E arms remain the oracle for the real template (TD-3) |
| R5 | Whole-file inventory contention | The §v2.I rebase rule |
| R6 | Q2 interpretation at landing | Owner rulings in advance (§v2.O G1-1). The ledger owner applies them and does not infer them |
| R7 | Coupling to log strings | Loud failure; noted |
| R8 | Fake-timer technique (F20) | Installed per case; unconditional cleanup (§v2.E rule 1); order independence re-measured |
| R9 | Unreachability discovered later, including `3a-loadPlan` | **Stop.** No export. The separate owner approval naming the symbols applies. For `3a-loadPlan` specifically, the §v2.F fallback applies first. *(2026-10-21: `3a-loadPlan` is measured feasible on the probe (EVIDENCE.md §Round 3), so the fallback is not triggered. The risk remains only for the final single file.)* |
| R10 | Mutation provisioning by ancestor `node_modules` is unmeasured | Confirmed before the matrix runs. No junction; no `npm ci` in the shared checkout |

**Evidence gaps (Plan v2).**

- Everything listed in v1.12 carries forward.
- All three reviewers read the shared working tree, not `origin/main`.
- ~~The added mutations (T2, T1) and `3a-loadPlan` are **unmeasured**.~~ ⚠️ **UPDATED 2026-10-21:
  `3a-loadPlan` and all nine added mutations are MEASURED on the four-file probe in both variants**
  ([`EVIDENCE.md`](../../artifacts/u1_followup_1/seam_probe/EVIDENCE.md) §*Round 3*;
  `mutation/matrix_round3_38.tsv`): 24 cases per variant, 48/48 pass, 76/76 mutated runs killed at
  assertion level, and 76/76 reverted runs green. That evidence comes from the top-level session.
  This `product-manager` re-ran nothing and could not hash the recorded blobs (`ffd743c8…`,
  `e6d741ca…`).
- **What still remains unmeasured** (EVIDENCE.md §*Round 3*, last bullet):
  - **The final single file under §v2.E**: variant A only, with unconditional cleanup,
    identity-based announcement matching, hide-count deltas, literal titles and the A1 negative
    control. It is not written, so neither its suite run nor its 38-mutation re-run (§v2.L
    steps 4–5) exists.
  - **Coverage mode** (`npm run test:js -- --coverage`).
  - **The minimum `flush()` depth** and its margin.
  - **Linux.**
  - **Mutation-tree provisioning** (§v2.H).
  - **The T3 checks for file-level errors and for mutated bytes differing from the original**, as
    explicit runner checks (§v2.H note).
- The §v2.F feasibility notes and the line citations for `loadPlan` are a ⚠️ working-tree read of
  `volume-splitter.js`. The file is not modified in the shared checkout, and the reviewers confirmed
  that its §0.3 lines match. It still has to be re-verified at step 2.
- The cited `unslop.md` lines are a ⚠️ working-tree read of a modified file.

### v2.O Gate 1 decision list — owner decisions, with team recommendations

*Each item is the owner's to answer directly. The recommendations are the team's and are not
rulings. Relayed facts are unverified until §v2.J's status column says otherwise.*

**G1-1 — Q-window, re-scoped to this packet's own landing (P2, P3, P4).** The question is when the
U1-FOLLOWUP-1 PR may merge.

- **Landing options:**
  - **(a)** Land when the gates pass, without waiting for #544 or #547. Cost: #544 must be
    re-extended, and the ledger owner applies Q2 to a corpus change in the middle of recording the
    cycle that D2's condition names.
  - **(b)** Land only after **#544 and #547 have both merged**.
  - **(e)** As (b), and also after the Q4 rename has landed, so that this merge's row is read under
    one job name. Cost: a dependency on #546 and A3 (L3).
  - **(f)** Land only after C4 activation. Cost: the new file's first Linux runs on `main` are
    already merge-blocking for every PR.
- **Team recommendation: (b), conditional on L1 and L2 verifying live.** That means:
  - §13.0 records the cycle through the strict mark `2026-09-10T23:18:21Z` with **zero red,
    missing, skipped or cancelled** `JS Unit` results;
  - #547's owner text has been read directly.
- **If L1 or L2 does not verify,** the fallback is §0.8's original recommendation: **(d)**, record
  §13.0 through the strict mark via its own process, followed by **(a)**.
- The ordering in (b) keeps this corpus change out of the cycle that #544 records and that #547's
  condition names. It takes no position on C4.
- **Also to confirm (owner):**
  1. **Who owes the post-merge §13.0 row.** Team proposal: the ledger owner, through §13.0's own
     process (a departure from U3b T10, stated at §v2.L step 14). This packet records the
     job-level reading in the post-merge docs PR.
  2. **Whether a red post-merge `JS Unit` job is a stop condition for "done".** Team proposal:
     **yes**, with no re-run to green without the owner.
  3. **Whether such a red only resets the next window, or also bears on the conditional D2** (P4).
     Owner question; no team preference.
  4. **That this landing does not reopen D2's conditional approval.** Owner statement requested, so
     that the ledger owner applies a ruling rather than inferring one (L5).
- **Noted, NOT decided in this packet: C4 against the next window.** C4 and D2 are out of scope
  under §0.7. Landing restarts the **next** window (F3), and something must decide whether C4
  activation waits on it. **The owner is asked only to note that the question exists, and to answer
  it in, or cross-linked from, the #547 / R2.3 decision lineage before C4 activation**, where the
  ledger owner will look. The options are listed for information, with **no team preference**:
  - **(c) Waiver.** C4 may activate without a fresh window on the new corpus. This is explicitly a
    **waiver of Q2's consequence** for the new corpus (Q2, `STEP12_JS_UNIT_GATE0.md:210`). It does
    not "follow F3".
  - **(d) Fresh window.** A 14-day window on the 14-file suite, from U1-FOLLOWUP-1's first
    successful post-merge `JS Unit` job.
  - **(g) Minimum green runs (new).** A minimum number of green post-merge `JS Unit` runs on
    `main`, recorded in §13.0, before C4.

**G1-2 — Q-filing (P4).**

- **Queue row options:**
  - (a) Update the §0.4 row in the implementation PR, rebased after #541, #544 and #547 and
    coordinated with the docs-cleanup claim.
  - **(a2)** Update the §0.4 row in the post-merge docs PR.
  - (b) Also file a §4 or §7 packet entry.
  - (c) Neither.
- **§v2.14 options:**
  - **(i)** An in-place annotation in the implementation PR, with the merge SHA added by the
    post-merge PR.
  - (ii) Annotate only in the post-merge PR.
  - (iii) Do not touch §v2.14.
- **Under every option, the post-merge docs/status PR is a Q-done deliverable** (§v2.K).
- **Live check kept:** whether a WS1 slice (#541–#543) moves or splits
  `docs/volume_failure_feedback/PLANNING.md`. If one does, the annotation targets the post-slice
  path.
- **Team recommendation: (a2) + (i).**

**G1-3 — Q-sequencing.**

- **Checkout options:**
  - (a) A standalone clone under AGREED_PLAN §11's Q8(a) boundaries, with the owner extending that
    classification to this packet by name.
  - (b) A linked worktree created by `scripts/new-worktree.ps1`, with owner-approved lifecycle
    metadata.
  - (c) The main checkout, only once it is clean and no other session is active.
  - (d) Hold until the WORKTREE_CLEANUP_PLAN §1.2 disposition or `PREVENTION_COMPLETE`.
- **Timing sub-choice:**
  - (i) Start after Gate 1, with the PR held as a draft until G1-1's landing conditions hold.
  - (ii) Start only once those conditions hold.
- **L5** (*"lands only after the owner's timing decision"*, and the regeneration rule) is recorded
  as **coordination, not a ruling**.
- **Team recommendation: (a) with (i).**

**G1-4 — The criterion 3(b) reading (P5), a standalone question.** §0.5 3(b) reads *"A
slider-originated first failure (`!standing`) announces."* The measurement shows that `!standing`
is masked on a first failure (v1.4; round-1 survivors `M8b` and `M8e`).

- **(a)** Read 3(b) as satisfied **jointly**: the two first-failure cases cover the stated outcome,
  and `3b-after-recovery` covers the stated disjunct.
- **(b)** Read 3(b) as the first-failure outcome only, keeping `3b-after-recovery` as extra
  discrimination without criterion status.
- **(c)** Another reading the owner states.
- **Team recommendation: (a).** **Not recorded as confirmed.** Section 0 is not edited under any
  answer.

**G1-5 — The `toast.js`-assertion boundary (P1).**

- **(a)** Confirm that every assertion listed in §v2.G sits within Q-scope (a) and is **not** a
  revival of U3b's retired KI-011 coverage. The consequence accepted with (a) is that a `toast.js`
  change to those behaviors reds this file.
- **(b)** Not within Q-scope (a). The owner names which assertions to drop. This sends the design
  back to the council, because variant B or another mechanism would need to be measured.
- **Team recommendation: (a).**

**G1-6 — Confirmation of the Q-pins delegation.**

- **(a)** Confirm that Q-pins was within the team's delegation, which makes §v2.I a team decision.
- **(b)** Decide Q-pins as the owner: the pins in the same PR as §v2.I, or a separate PR.
- **Also:** keep or strike the flagged docstring-prose edit (§v2.I).
- **Team recommendation: (a)** with the docstring edit kept.

**G1-7 — Gate 0 re-confirmation (P6).** A process recommendation: the top-level session puts the
Gate 0 re-confirmation (Q-scope (a), Q-seam (d), Q-delegation (b), Q-done (a), and the §0.5
criteria as signed) to the owner **in the same direct prompt as Gate 1**, and keeps the owner's
verbatim answers. No Section 0 edit.

**G1-8 — Plan v2 approval (Gate 1).** Approve Plan v2 as written, or with stated changes.

- **(a)** Approve. Also confirm the TEAM decisions recorded here: TD-1 variant A; Q-mutation (a)
  amended (38 mutations); Q-E2E (a); `senior-developer` as implementer.
- **(b)** Approve with changes.
- **(c)** Do not approve.

**No additional diff-time reviewer is proposed.** The owner may authorize one explicitly
(`CLAUDE.md` §3). Approval authorizes implementation only within the approved scope, and only once
G1-1's landing conditions and G1-3's checkout are in place. **The merge needs its own confirmation
naming the PR.**

## Sign-off

- [x] Gate 0 complete (Section 0 above) — signed 2026-10-21, relayed record. Re-confirmation at
      Gate 1 is recommended (P6; §v2.O item G1-7).
- [x] Every finding has a disposition. All 24 findings have a matrix row (A1 and T7 are merged into
      one row). Every disposition is **proposed**, and the owner confirms it at Gate 1.
- [x] Agent provenance complete: both `product-manager` IDs, same-PM-resumed = yes, the three
      reviewer IDs, and a scoped evidence-gap line.
- [ ] Owner approved Plan v2 (Gate 1).
- [ ] Ready to implement.


## Direct Gate 1 owner decision and current-main implementation record — 2026-10-21

This addendum supersedes historical Gate 1 status and the stale open-PR readings;
it preserves Section 0, Gate 0's relayed provenance, all council findings and
proposed dispositions as their historical record. No new council was run.

### Direct questions and verbatim owner answers

1. **Question:** Approve U1-FOLLOWUP-1 Plan v2 as detailed in
   artifacts/parallel-next-five/u1/GATE1_DECISION_PACKET.md, including the joint
   criterion 3(b) reading and all §v2.G real-toast output/arrangement assertions
   (including action expiry and message persistence), while preserving retired
   KI-011 scope and making no production JS changes?
   **Owner:** “Approve Gate 1 with these readings”
2. **Question:** For U1-FOLLOWUP-1 records, approve the recommended filing:
   annotate §v2.14 in the implementation PR; put queue discharge, merge SHA and
   post-merge evidence in a later docs/status PR; send qualification receipts to
   prompt 2?
   **Owner:** “Approve recommended filing (a2)+(i)”
3. **Question:** After checks and independent review pass, may U1-FOLLOWUP-1 become
   eligible to land before the approved Q4 rename, now that #544/#547 have merged?
   Publication and named-PR merge authority remain separate.
   **Owner:** “Eligible before Q4/C4; coordinate with prompt 1”

Source: the owner's direct reply to this Codex conversation's
`request_user_input_async` call `call_a9d43a22057a4ac29aa8bd9862d2e39f`.
The exact structured receipt is retained locally at
`artifacts/parallel-next-five/u1/OWNER_GATE1_APPROVAL.json`.

Gate 1 is **approved directly**. This is distinct from Gate 0's original relayed
record. The independent-clone, three-role, inventory-contract and generated-inventory
scope came directly from the current owner commission. The narrow §v2.F loadPlan
fallback remains available as originally written; it is not triggered by the
historical measured probe or the current source read.

### Base refresh and isolation

Implementation starts from remote `main`
`d98f45d34de8356f7ac2becb7a7c4b3bef48f8e3`, rechecked after approval. The clone is
`D:\development\Hypertrophy-Toolbox-v3-u1-20261021`, branch
`test/u1-followup-1-vitest`. It was cloned from the remote with independent Git
storage and no alternates/hardlinks to the shared recovery checkout. Private
dependencies, runtime, database, backup/log, temp, cache and bytecode paths are
required; the process-local setup lives at
`artifacts/parallel-next-five/u1/launch-private.ps1`.

The original local plan in the shared checkout remains unchanged (SHA-256
`3de635643d3464c605e022bc8e1ac941c69509643373705b166e3bcb4e73826a`).
The committed copy here is the approved implementation record.

Three explicitly requested roles independently inspected current source and
historical evidence: JavaScript implementer, behavioral verifier and scope/review
agent. Their reports and the independent preapproval evidence review are under
`artifacts/parallel-next-five/u1/`. No material redesign was found and no council
was repeated. Before execution, current coordination records showed no applicable
active preservation/destructive freeze; retention and recovery holds remain.

Current-source production blobs match the measured probe: shipped K13 is
`forceAnnounce || !standing || !ourMessageStands()`; all six helpers remain
reachable through the public initialization seam. No production export or
JavaScript change is authorized or needed.

### Integration and done boundary

- #544 merged as `b4a2653c0b64965a6bd906ebb981fef0cd412bf7`; #547 merged as
  `aafba153cd0508d4f92934c3bf622ef0e9a9ff40`. Their old open/pending readings above
  are superseded by these measured receipts. Their approvals are not requested again.
- The owner already chose exact JS Unit job conclusions and separately approved
  Q4/D2. The Q4 rename has not landed at this base; current display name remains
  `JS Unit (Vitest, non-required)`. C4 remains separate and unapproved here.
- #545 and #546 have also landed; inventories are generated against their integrated
  main, and must be regenerated after any subsequent integration/rebase.
- Under filing (a2)+(i), the implementation annotates §v2.14 in place. Queue §0.4
  discharge, merge SHA and post-merge job evidence belong in the post-merge
  docs/status PR. The ledger owner in prompt 2 records §13.0; this packet does not
  edit the qualification ledger.
- Qualification receipts go to prompt 2; landing coordination goes to prompt 1.
  File-based receipts are retained under the evidence root. The base-main green job
  is explicitly pre-U1 evidence and cannot discharge U1 post-merge qualification.
- The existing owner amendment governs Q2: a corpus change restarts the next window
  without retroactively voiding a completed cycle. No new C4/window ruling is inferred.
- Publication and named-PR merge remain separate owner actions. The post-merge
  docs/status PR and green exact merged-main JS job remain part of Q-done(a).

### Implementation and validation

Implementation and local execution are complete. Final case identities, pins,
mutation outcomes, cleanup control, flush-depth margin, coverage, Chromium and
Python/type/inventory gates, runtime byte identity, and independent diff/evidence
review are recorded below before publication authority is requested. Historical
probe outcomes above remain historical and are not final-file results.
### Measured local implementation evidence — 2026-10-21

The final file is `static/js/modules/__tests__/volume-splitter.test.js`, Git blob
`9df343ad2858f5258dc58e5cabbce922b2fac335`. Its 24 literal identities match §v2.F
exactly. `3a-loadPlan` is feasible on the final file, so the 23/37 fallback was
not triggered. No production JavaScript or export was changed.

| Check | Actual outcome | Local evidence under `artifacts/parallel-next-five/u1/` |
|---|---|---|
| Focused Vitest | 24 passed | `implementation/focused-vitest.json` |
| Full JS suite | 269 passed across 14 files | `implementation/full-vitest.json` |
| Coverage execution | 269 passed; v8 reports generated, no threshold added | `coverage-vitest.json`, `coverage/` |
| Mutation matrix | 38 assertion kills; all 38 reverted controls pass 24/24; no survivor/exclusion | `validation/matrix-final.tsv`, `validation/runs/20261021T174346-abb5c81ff4/summary-adjudicated.json` |
| Order/repeat | Five shuffled seeds (1, 7, 42, 1234, 99999), three repeats; each 24/24 | Same behavioral run's structured reports |
| Cleanup negative control | Only forced first shape assertion fails; following case verifies prior state restored and fresh Bootstrap, then passes; reverted file 24/24 | `validation/BEHAVIORAL_VALIDATION.md`, retained cleanup-control copy and reports |
| Flush measurement | Depths 0/1 fail; every depth 2–20 passes; minimum 2, shipped 20, margin 18 | Same behavioral run's `checks.flush` |
| Chromium | 75 passed; zero skipped, unexpected or flaky; isolated port 5167 and DB/runtime | `chromium.log`, `chromium-exit.json`, `chromium-environment.json` |
| Inventory | Generated 14 files / 269 cases; check exits 0; existing 13 entries / 245 identities preserved | `inventory-generate.log`, `inventory-check.log`, `final-file-list.json` |
| Inventory contracts | 48 passed | `pytest-target.xml`, `pytest-target.log` |
| Python full-corpus evidence | Exact 5,660 original identities reconciled across completed runs: 5,658 passed, same 2 existing skips; no clean single full/core process pass claimed | `validation/PYTHON_EVIDENCE_ASSESSMENT.md`, raw full/core/correction XML and exit receipts |
| TypeScript | `tsc --noEmit` exits 0 | `tsc.log`, `type-gates.json` |
| Pyright | 1.1.410; zero diagnostics, zero net-new baseline entries | `pyright-final.json`, `pyright-baseline-final.log`, `final-python-types.json` |
| Blocking flake8 selection | E9/F63/F7/F82 exits 0 | `flake8.log`, `final-python-types.json` |
| Environment preflight | Read-only repository preflight passes; both suppression names absent at all three scopes | `environment-preflight.json`, `suppression-readback.json` |
| Runtime/config preservation | All 26 protected blobs match the verified base, including the 13 existing JS tests, matching specs, workflow, ledger and handover | `unchanged-blob-proof.json` |
| Independent source/diff review | PASS on final test design, exact generated contract and six-path scope | `final-review/source-review.md`, `final-review/implementation-diff-review.md` |

**M5c's explicit classification.** Removing the no-panel guard causes the expected
null.prepend rejection in the mutated continuation and independently fails 2b's
one-announcement assertion. All 24 identities execute; there is no file, suite or
collection error. The strict runner initially withheld the kill. The independent
scope reviewer read the raw JSON/audit/stdout/stderr and clean revert and accepted
the exact runtime-error fingerprint under approved T3. It is retained unsuppressed
in the evidence, not counted through a crash alone. Original/reverted controls
have no unhandled error. No mutation was excluded or weakened.

**Reachability and limitations.** M9b kills 4b/4d; M9c kills 4d/4d-handling, so the
required negative guards remain discriminating. M8l is killed only by loadPlan;
M8n is killed by the debounced-input 3b and 3c, and remains discrimination-only.
The 18-turn margin describes these current promise chains and is not proof against
future deeper awaits. The disclosed real-toast support coupling is accepted by the
direct Gate 1 decision; standalone retired KI-011 coverage is not revived.

**Independent roles and qualification.** The JavaScript implementer wrote the
new file; the behavioral verifier wrote/executed only artifact-copy controls; the
scope reviewer changed no implementation. Prompt 2 acknowledged the qualification
receipt and owns §13.0; no row number or new T0 is preassigned. Prompt 1 received the
landing handoff alongside its CI-core coordination record. Its A3 #549 owns the
workflow slot; this packet changes no workflow or `vitest.config.js`.

**Publication readiness:** independent source, behavioral and Python evidence
reviews accept the local candidate with the exact composite limitation below.
Remote main remains `d98f45d34de8356f7ac2becb7a7c4b3bef48f8e3` at the final
readback; the generated inventory is checked against that integrated base.
Publication authority for the concrete reviewed candidate remains required.
The Linux JS job and required PR contexts need the published candidate. Named-PR
merge authority, the green merged-main job and the post-merge docs/status PR remain
separate completion requirements. No clean single full/core Python process pass,
native PR gate result or completed U1 obligation is claimed.

### Final-file mutation summary

Each mutated run below exits 1 with actual assertion failures; each reverted run
exits 0 with all 24 cases passing. Full identities, source hashes, strict error
checks and full raw reports are retained in `validation/matrix-final.tsv` and the
adjudicated structured run. The M5c runtime classification is explained above.
| Mutation | Mutated exit | Reverted exit | Killing cases | Exclusion |
|---|---:|---:|---|---|
| M5-no-idempotence-guard | 1 | 0 | 2a repeat failure keeps the same single node and does not rewrite text | none |
| M5b-rewrite-text-on-repeat | 1 | 0 | 2a repeat failure keeps the same single node and does not rewrite text | none |
| M5c-no-panel-guard | 1 | 0 | 2b no .volume-insights-panel: no region, nothing throws | none |
| M5d-live-region | 1 | 0 | 2a repeat failure keeps the same single node and does not rewrite text | none |
| M6-hide-not-remove | 1 | 0 | 2c-success next success removes the node from the DOM; 2c-reset reset removes the node from the DOM; 3b-after-recovery slider failure after a success announces although our message text persists; 5a both stand: success hides the toast; 5b action probe is scoped to #liveToast: button OUTSIDE #toast-body still counts; 5c only the button stands (stranger message): NOT hidden; 5d only the message stands (button gone): NOT hidden; 5e a same-label button OUTSIDE #liveToast does not count as ours | none |
| M6b-reset-does-not-exit | 1 | 0 | 2c-reset reset removes the node from the DOM | none |
| M8-drop-forceAnnounce | 1 | 0 | 2a repeat failure keeps the same single node and does not rewrite text; 3a explicit commands announce while region AND our message stand; 3a-loadPlan loading a saved plan announces while region AND our message stand | none |
| M8b-drop-not-standing | 1 | 0 | 3b-after-recovery slider failure after a success announces although our message text persists | none |
| M8c-drop-message-disjunct | 1 | 0 | 3d slider repeat after a stranger replaced our message DOES announce, button still standing; 3d-near-miss message probe is exact equality | none |
| N11-announce-keyed-on-action-probe | 1 | 0 | 3d slider repeat after a stranger replaced our message DOES announce, button still standing; 3d-near-miss message probe is exact equality; 3e slider repeat after our button is gone but our message stands does NOT announce | none |
| M8d-always-announce | 1 | 0 | 3c slider repeat while region and our message stand does NOT announce; 3e slider repeat after our button is gone but our message stands does NOT announce | none |
| M8e-standing-read-after-render | 1 | 0 | 3b-after-recovery slider failure after a success announces although our message text persists | none |
| M8f-change-listener-forces | 1 | 0 | 3c slider repeat while region and our message stand does NOT announce; 3e slider repeat after our button is gone but our message stands does NOT announce | none |
| M8g-debounce-forces | 1 | 0 | 3c slider repeat while region and our message stand does NOT announce | none |
| M8h-toast-retry-not-forced | 1 | 0 | 3a explicit commands announce while region AND our message stand | none |
| M8i-region-retry-not-forced | 1 | 0 | 3a explicit commands announce while region AND our message stand | none |
| M8j-wrong-toast-type | 1 | 0 | 2a repeat failure keeps the same single node and does not rewrite text; 2b no .volume-insights-panel: no region, nothing throws; 2c-success next success removes the node from the DOM; 2c-reset reset removes the node from the DOM; 3a explicit commands announce while region AND our message stand; 3a-loadPlan loading a saved plan announces while region AND our message stand; 3b slider-originated first failure announces (change); 3b slider-originated first failure announces (debounced input); 3b-after-recovery slider failure after a success announces although our message text persists; 3c slider repeat while region and our message stand does NOT announce; 3d slider repeat after a stranger replaced our message DOES announce, button still standing; 3d-near-miss message probe is exact equality; 3e slider repeat after our button is gone but our message stands does NOT announce; 4a stale SUCCESS after a newer failure: no paint, no region removal, no dismiss; 4c-control a CURRENT post-2xx handling failure does enter the failure state; 5a both stand: success hides the toast; 5b action probe is scoped to #liveToast: button OUTSIDE #toast-body still counts; 5c only the button stands (stranger message): NOT hidden; 5d only the message stands (button gone): NOT hidden; 5e a same-label button OUTSIDE #liveToast does not count as ours | none |
| M9-no-then-guard | 1 | 0 | 4a stale SUCCESS after a newer failure: no paint, no region removal, no dismiss; 4c stale POST-2xx HANDLING FAILURE after a newer success: no region, no announce; 4d-handling reset while in flight, then a post-2xx handling failure: no region, no toast | none |
| M9b-no-catch-guard | 1 | 0 | 4b stale REQUEST FAILURE after a newer success: no region, no announce; 4d reset while in flight, then the request fails: no region, no toast | none |
| M9c-reset-no-bump | 1 | 0 | 4d reset while in flight, then the request fails: no region, no toast; 4d-handling reset while in flight, then a post-2xx handling failure: no region, no toast | none |
| M9d-no-increment | 1 | 0 | 4a stale SUCCESS after a newer failure: no paint, no region removal, no dismiss; 4b stale REQUEST FAILURE after a newer success: no region, no announce; 4c stale POST-2xx HANDLING FAILURE after a newer success: no region, no announce | none |
| M9e-handling-throw-swallowed | 1 | 0 | 4c-control a CURRENT post-2xx handling failure does enter the failure state | none |
| P1-action-probe-toast-body-scope | 1 | 0 | 5b action probe is scoped to #liveToast: button OUTSIDE #toast-body still counts | none |
| P2-action-probe-unscoped | 1 | 0 | 5e a same-label button OUTSIDE #liveToast does not count as ours | none |
| P3-dismiss-drops-message-check | 1 | 0 | 5c only the button stands (stranger message): NOT hidden | none |
| P4-dismiss-drops-action-check | 1 | 0 | 5d only the message stands (button gone): NOT hidden; 5e a same-label button OUTSIDE #liveToast does not count as ours | none |
| P5-message-probe-includes | 1 | 0 | 3d-near-miss message probe is exact equality | none |
| P6-no-dismiss | 1 | 0 | 5a both stand: success hides the toast; 5b action probe is scoped to #liveToast: button OUTSIDE #toast-body still counts | none |
| P7-dismiss-guard-or | 1 | 0 | 5d only the message stands (button gone): NOT hidden; 5e a same-label button OUTSIDE #liveToast does not count as ours | none |
| M5e-append-not-prepend | 1 | 0 | 2a repeat failure keeps the same single node and does not rewrite text | none |
| M5f-region-retry-no-aria | 1 | 0 | 2a repeat failure keeps the same single node and does not rewrite text | none |
| M5g-region-retry-no-type | 1 | 0 | 2a repeat failure keeps the same single node and does not rewrite text | none |
| M8k-toast-action-label | 1 | 0 | 2a repeat failure keeps the same single node and does not rewrite text; 2b no .volume-insights-panel: no region, nothing throws; 2c-success next success removes the node from the DOM; 2c-reset reset removes the node from the DOM; 3a explicit commands announce while region AND our message stand; 3a-loadPlan loading a saved plan announces while region AND our message stand; 3b slider-originated first failure announces (change); 3b slider-originated first failure announces (debounced input); 3b-after-recovery slider failure after a success announces although our message text persists; 3c slider repeat while region and our message stand does NOT announce; 3d slider repeat after a stranger replaced our message DOES announce, button still standing; 3d-near-miss message probe is exact equality; 3e slider repeat after our button is gone but our message stands does NOT announce; 4a stale SUCCESS after a newer failure: no paint, no region removal, no dismiss; 4c-control a CURRENT post-2xx handling failure does enter the failure state; 5a both stand: success hides the toast; 5b action probe is scoped to #liveToast: button OUTSIDE #toast-body still counts; 5c only the button stands (stranger message): NOT hidden; 5d only the message stands (button gone): NOT hidden; 5e a same-label button OUTSIDE #liveToast does not count as ours | none |
| M8m-message-constant | 1 | 0 | 2a repeat failure keeps the same single node and does not rewrite text; 2b no .volume-insights-panel: no region, nothing throws; 2c-success next success removes the node from the DOM; 2c-reset reset removes the node from the DOM; 3a explicit commands announce while region AND our message stand; 3a-loadPlan loading a saved plan announces while region AND our message stand; 3b slider-originated first failure announces (change); 3b slider-originated first failure announces (debounced input); 3b-after-recovery slider failure after a success announces although our message text persists; 3c slider repeat while region and our message stand does NOT announce; 3d slider repeat after a stranger replaced our message DOES announce, button still standing; 3d-near-miss message probe is exact equality; 3e slider repeat after our button is gone but our message stands does NOT announce; 4a stale SUCCESS after a newer failure: no paint, no region removal, no dismiss; 4c-control a CURRENT post-2xx handling failure does enter the failure state; 5a both stand: success hides the toast; 5b action probe is scoped to #liveToast: button OUTSIDE #toast-body still counts; 5c only the button stands (stranger message): NOT hidden; 5d only the message stands (button gone): NOT hidden; 5e a same-label button OUTSIDE #liveToast does not count as ours | none |
| M6c-success-no-exit | 1 | 0 | 2c-success next success removes the node from the DOM; 3b-after-recovery slider failure after a success announces although our message text persists; 5a both stand: success hides the toast; 5b action probe is scoped to #liveToast: button OUTSIDE #toast-body still counts; 5c only the button stands (stranger message): NOT hidden; 5d only the message stands (button gone): NOT hidden; 5e a same-label button OUTSIDE #liveToast does not count as ours | none |
| M8n-debounce-400 | 1 | 0 | 3b slider-originated first failure announces (debounced input); 3c slider repeat while region and our message stand does NOT announce | none |
| M8o-change-no-calculate | 1 | 0 | 3b-after-recovery slider failure after a success announces although our message text persists; 3c slider repeat while region and our message stand does NOT announce; 3d slider repeat after a stranger replaced our message DOES announce, button still standing; 3d-near-miss message probe is exact equality; 3e slider repeat after our button is gone but our message stands does NOT announce | none |
| M8l-loadPlan-not-forced | 1 | 0 | 3a-loadPlan loading a saved plan announces while region AND our message stand | none |

### Python execution and setup corrections — exact receipts retained

The initial full Windows invocation completed with **5,651 passed, 7 failed,
2 skipped** (exit 1). Six failures selected the System32 WSL Bash launcher with
no configured distribution; one configuration test temporarily changed
`HT_RUNTIME_DIR` while the explicit inherited `DB_FILE` still won. The artifact-only
Python launcher selects installed Git Bash and resolves the database from the
still-pinned private runtime without a competing process `DB_FILE` override.
All three complete affected modules, the exact original **126 identities**, passed.

The subsequent complete non-guard core run retained **3,624 passed, 2 failed,
2 skipped** (exit 1). Both failures were initial Git fixture creation under an
overly long scratch name. A direct diagnostic retained exit 128 and `Filename too
long`; the production code and assertions were not involved or changed.

A shorter scratch name permitted those lifecycle tests to pass. That complete
core invocation retained **3,625 passed, 1 failed, 2 skipped** (exit 1): the sole
remaining database-isolation assertion requires a `pytest-` path component, while
the temporary name was `pc2`. Its earlier assertions already proved the active DB
was the existing private scratch database. The complete **10-case** database-
isolation module then passed (exit 0) under the short private name `pytest-u1`.
The verifier also measured both terminal-payload host cases passing independently.

**Corpus reconciliation is by whole module, not by a selected passing case.** The
original full run supplies all **2,032** guard-hook identities, all passing. The
latest complete core supplies its exact **3,628** complementary identities, with
the entire 10-case database-isolation module replaced by that complete corrected
module run. The disjoint Counter union equals the original **5,660** identities
exactly: **5,658 passing, the same 2 existing skips, no missing/extra/duplicate
identity**. All source/assertion blobs remain unchanged by the setup corrections.
Every original red process receipt remains red and retained; **this is not a claim
of a clean single full-suite or complete-core process rerun**.

The independent behavioral verifier and independent scope reviewer checked this
modular execution evidence and its limits for local publication readiness.
Native required PR CI remains a separate proof before merge. Captured nonfatal
rotating-log `WinError 32` diagnostics during parallel Python execution are
retained and disclosed in the assessment; they are distinct from JUnit failures
or errors and do not establish a production change.

Raw evidence: `pytest-full.*`, `pytest-correction.*`, `pytest-core-corrected.*`,
`git-path-diagnostic.json`, `pytest-core-final.*`,
`pytest-db-isolation-correction.*`, `pytest-lifecycle-probe.*`, private launch and
preflight receipts, and `validation/python-evidence-assessment.json` under
`artifacts/parallel-next-five/u1/`. No test, fixture, workflow, baseline, ledger,
assertion or application source was changed to obtain these corrections.

### Integration after A3 #549 — 2026-10-21

This entry supersedes the earlier current-base and pending-publication statements
for the integrated candidate. The direct owner approved publishing reviewed commit
`2b85faab5d72c8188c3666585b0fb5b3970dbb31` and opening draft PR
[#551](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/551). The exact
question and answer are retained in `OWNER_PUBLICATION_APPROVAL.json`. Named-PR
merge authority remains separate and has not been granted.

A3 #549 then landed as `dee3c379b8435e1ba0941884b9f264675f8012b7`. The private branch was rebased under approved
§v2.L step 11; the original published commit is retained on
`retain/u1-followup-1-before-dee3`. The rebased execution head is `8d651690852b7fb0ca87f46ed2f9b8fb08133584`.
Only A3's workflow, CI plan, two generated inventories and two Python contract
files changed upstream. No Volume Splitter, toast, fetch-wrapper, dependency,
existing JS-test, E2E or governing-policy blob drifted, so no council was repeated.
The final U1 diff remains the same six approved paths against this new base.

Inventories were regenerated from live collection after rebase and checked again:
the deterministic Python subset is 3,651 cases, while Vitest is 14 files / 269
cases. All 245 prior Vitest identities and all 13 old per-file counts remain.
Fresh generation matches the rebased artifact exactly; no generated counts were
merged by hand. The inherited A3 workflow is byte-identical to new main, with no
U1 workflow or qualification-ledger edit.

| Fresh integration check | Result |
|---|---|
| Focused / full JS / coverage execution | 24 / 269 / 269 passed |
| Five shuffled seeds and three repeats | All eight runs pass 24/24 |
| Cleanup negative control | Only deliberate first failure; restored following case and clean revert |
| Flush depth | 0/1 fail by assertions, 2–20 pass; minimum 2, shipped margin 18 |
| Inventory generation/check and contract suite | Exit 0; 48 contracts pass |
| TypeScript / pyright / baseline / blocking flake8 | All exit 0; zero pyright diagnostics/net-new |
| Matching Chromium | 75 passed; no skips, flakes, unexpected results or global errors |
| Full Windows Python invocation | 5,681 passed, 2 existing skips, zero failures/errors, exit 0; 5,683 unique identities |

These fresh receipts are under `artifacts/parallel-next-five/u1/integration-dee3/`.
Python uses its own runtime and real Git Bash, without an explicit DB_FILE
override, and a fresh short private `pytest-i` scratch prefix. Chromium uses a
separate private runtime/database and port 5169. Earlier red full/core invocations
and their composite reconciliation remain retained as historical evidence; this
new row describes an actual clean full invocation on the integrated source.

The 38-mutation matrix is retained under step 11's explicit exception: all
anchored production and final-test Git blobs remain identical. Rebase changed
the test checkout from LF to CRLF; raw test bytes are therefore not described as
identical across rebase. Its Git blob remains `9df343ad2858f5258dc58e5cabbce922b2fac335`,
and normalized source is identical. Fresh order/cleanup/flush controls ran again.
`source-proof.json` and `independent-source-review.md` record the applicability
proof and all 26 protected blobs against the integrated base.

The original published head's native run `39645223680`, attempt 1, passed all
27 workflow jobs, including Linux JS coverage and the required Python/guard
route. Those receipts are historical for `2b85faa`; they are not substituted
for the integrated head's fresh native CI. Final independent evidence review,
the routine integration update to the existing draft PR and fresh native CI
follow this local execution record. Publication remains within the directly
approved branch/PR scope and mandated step 11 integration sequence; the owner
did not separately approve this new commit by SHA.

Prompt 1 received the A3 integration/landing-order handoff, and prompt 2 received
the pre-merge job/step receipt explicitly outside the mainline ledger. No row or
new T0 is preassigned. U1 still requires named-PR merge authority, a green exact
merged-main JS Unit job and the later docs/status PR before completion.
