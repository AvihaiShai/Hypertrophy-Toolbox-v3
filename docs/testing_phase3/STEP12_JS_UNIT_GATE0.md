# Testing Strategy Phase 3 — Step 12 (JS unit expansion with jsdom) — Gate 0 decision packet

> **Scope**: the step-12 decision packet, **plus Packet A as implemented** (§9) **and Packet B as
> implemented** (§10, Gate 1 approved with one owner amendment and executed 2026-08-22 — §10.11,
> §10.12). Each adds **one new test file** and nothing else. **No production JS, `package.json`,
> Vitest config, CI, or branch-protection change is made or authorized by this document**, and
> `js-unit` stays **non-required**. **Packet B is MERGED** — PR
> [#406](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/406), squash **`987588a`**, merged
> **2026-08-22** local (`2026-08-21T23:10:23Z`), **18/18** green on that commit (post-merge run
> `32535888704`). §10.13's merge STOP is **DISCHARGED** and annotated in place; of the items it
> listed, only the **KI-010 / KI-011** follow-up has moved — it is implemented in this commit,
> as a docs-only packet separate from Packet B, in
> [`UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md). **Packet C**,
> **Packet F**, **Q4**/**D2** promotion and **Q6** are untouched and still unauthorized.
>
> ⚠️ **ANNOTATION 2026-08-22 — the line above is falsified for Packet C and is annotated, not
> rewritten.** **Packet C is no longer untouched: it has a Gate 1 plan at §11 (PLAN v2).** It remains
> **unauthorized** — no test file exists, no mutation has been run, nothing is committed, and Gate 1
> is not approved. **Packet F, Q4/D2 promotion and Q6 are still untouched and still unauthorized**,
> exactly as written.
>
> ⚠️ **SECOND ANNOTATION, later the same day — the annotation immediately above is now falsified in
> turn, and is likewise annotated rather than rewritten.** **Gate 1 for Packet C was APPROVED**
> (§11.16): the test file exists, all **42** mutations have been run, and the work is committed and
> pushed as a **ready-for-review PR** (§11.17). **Packet C is NOT merged** — merge is a separate
> confirmation (§11.18). **Packet F, Q4/D2 promotion and Q6 remain untouched and unauthorized**, which
> is the one clause both annotations leave standing. This annotation follows the standard §10.12 set: when a commit falsifies prose
> that was true before it, the prose is annotated in place and the live block carries the truth.
> **Base**: `origin/main` @ `c404a06`, branch `wt/phase3-jsunit-gate0`, isolated docs-only worktree
> — this is the **Gate 0 origin** of the document, not a base for any packet. Packet A built on
> `9e5997a`’s base, Packet B rebased onto `0984d2e` (§10.12), and Packet B merged as `987588a`.
> **Covers**: [`TESTING_STRATEGY_PLANNING.md`](../TESTING_STRATEGY_PLANNING.md) §5 Phase 3 **step 12**,
> and the **unsigned `js-unit` half of D2** (§6, §8.1 row 2, reaffirmed unsigned in §8.1a and §8.1c).
> **Gate 0**: **PARTIALLY CLOSED 2026-08-15** — **Q1 and Q2 are signed** and Q3 is ruled (§0.1).
> Packets A → B → C are authorized as **test-only** expansion. **Promotion of `js-unit` to required
> is NOT authorized**, and is gated behind a restarted qualification window **and** Packet F.
> Q4–Q6 remain open (§8). Implementation of any packet still **STOPS** at its own Gate 1 plan.
> **Sibling packet**: [`PLANNING.md`](PLANNING.md) in this directory owns Phase 3 **step 11**
> (restore-path fuzz). This file owns step 12 only; the two share no file.
>
> ✅ **Label collision RESOLVED 2026-08-15 — administrative relabel, owner-directed.** The Vitest
> inventory/drift packet defined in **§2.5 of this file** was introduced as "Packet E" and is now
> **Packet F**. `PLANNING.md` in this same directory keeps **"Packet E (restore-path fuzz
> characterization)"** for **step 11**, unchanged and untouched. The letter **E is not reused
> anywhere in step 12** — step 12's sequence runs **A → B → C → F**, with **D dropped** (§2.4) and
> **E deliberately vacant** so the two packets can never be confused again.
>
> **This relabel changed nothing but the label.** Packet F's scope, contents, rationale, and its
> position *after* Packet C and *before* D2 are unchanged from when it was Packet E.
> No ordering, authorization, or gate condition moved. Full record in §2.6.

---

## 0. Summary and revised gate

### 0.1 Owner sign-off (2026-08-15)

The §8 questions were put to the owner and answered. **This section is the authority**; §8 is left
as the record of what was asked, annotated with each ruling.

| # | Ruling | Scope authorized |
|---|---|---|
| **Q1** | **AUTHORIZED — Phase 3 test expansion only.** `js-unit` is **not** promoted to required yet. | Packets A, B, C (§2.1–§2.3) as **test-only** work. No production JS, no `package.json`, no `vitest.config.js`, no CI, no branch protection. |
| **Q2** | **YES — the window restarts.** The strict **14-day** qualification window runs **from the first successful `JS Unit (Vitest, non-required)` run on `main` after the final expansion packet lands.** | Defines the D2 precondition. The 331-run streak measured in §6 **does not** count toward it. |
| **Q3** | **DROP `backup-center.js` from step 12.** Its required production seam extraction is out of scope. | Packet D is **closed unstarted** (§2.4). |
| **Q5** | **Promoted to a required predecessor**, as **Packet F** (§2.5). | Extend `generate_test_inventory.py` with Vitest inventory + drift enforcement **before** promotion. |

**Revised gate — every condition must hold before D2 may be signed:**

1. Packets **A → B → C** merged, in that order.
2. **Packet F** merged — Vitest node counts pinned and drift-enforced.
3. **14 consecutive days** with no `js-unit` failure, counted from the **first successful run on
   `main` after the final expansion packet lands** (Q2).
4. A **separate** owner signature on D2 itself. Q1 explicitly does not grant it.

### 0.2 Why the clock could not simply be inherited

The `js-unit` job is genuinely stable: **331 consecutive successful runs**, zero failures, over
**13 d 5 h 57 m** (§6). That stability is real — and it is **evidence about the wrong suite**.

> **The 331-run streak validates the existing 120-case suite only. It cannot qualify the expanded
> suite, and no part of it carries over.** Every one of those runs executed a suite at 5.6 %
> statement coverage that touches **none** of the modules Packets A–C will add. The jsdom
> environment, DOM fixtures, and the `bootstrap` global fake (§3.3) are precisely the machinery most
> likely to introduce a flake that a pre-expansion record cannot predict. Promotion readiness does
> not survive the expansion that changes what the job runs — which is why Q2 restarts the clock
> rather than extending it.

Two independent things were both true, and neither alone settled D2:

| Question | Measured answer |
|---|---|
| Is the *job* stable enough to be required? | **Yes.** 331/331 green; the only 3 reds in 16.8 days are one attributable, resolved dependabot incompatibility (§6.2). |
| Is the *suite behind it* worth requiring? | **Not yet.** 5.6 % statement coverage; the four named high-risk modules are at **0 % executed** coverage (§1). |

A required check over a suite that asserts almost nothing buys process cost without buying
protection. The value of promotion is created by the expansion, not by the clock.

**Authorized order**: **A → B → C**, then **F**, then a fresh 14-day window per Q2, then D2.

---

## 1. Current JS-unit coverage and untested high-risk behaviors

### 1.1 Measured baseline

Read from the `JS Unit (Vitest, non-required)` job of run
[`31856035853`](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/actions/runs/31856035853)
(push to `main`, 2026-08-15T01:16Z):

| Metric | Value |
|---|---|
| Test files | **10 passed (10)** |
| Test cases | **120 passed (120)** |
| Wall time | **1.86 s** |
| Statements / branches / functions / lines | **5.6 % / 8.3 % / 6.1 % / 5.4 %** |
| JS files under `static/js` excluding `*.test.js` | **57** (51 of them in `static/js/modules/`) |
| Modules directly imported by a test | **9** |

> **Three stale numbers in the source documents, corrected here.** `TESTING_STRATEGY_PLANNING.md`
> lines 79/172 say **"8 of 49 modules"**; §8.6 line 540-541 records **"5.14 %"** and **"47 of 55"**;
> `vitest.config.js` says **"8 covered modules and the 41 that have no test"**. Today's measured
> figures are **9 of 57** and **5.6 %**. These are drift from ordinary growth, not errors that were
> ever wrong when written — recorded so the next session does not re-derive them. They are **not**
> corrected in those files by this packet; that is question **Q6**.

### 1.2 RECORDED FINDING — the jsdom claim is stale; the migration path is proven in-tree

`TESTING_STRATEGY_PLANNING.md` line 79 states *"`jsdom` is installed but **zero test files opt into
it**"*, and line 172 repeats *"`jsdom` installed but unused"*. **Both are false as of `c404a06`.**

Two files already carry the exact `// @vitest-environment jsdom` pragma that F5-6 prescribes:

| File | Line 1 | What it establishes |
|---|---|---|
| [`__tests__/exports.test.js`](../../static/js/modules/__tests__/exports.test.js) | `// @vitest-environment jsdom` | DOM fixture via `document.body.innerHTML`, hoisted `vi.mock` of two collaborators, `localStorage.clear()`, prototype spies |
| [`__tests__/fetch-wrapper.test.js`](../../static/js/modules/__tests__/fetch-wrapper.test.js) | `// @vitest-environment jsdom` | `vi.mock('../toast.js')`, `vi.spyOn(globalThis, 'fetch')` |

This materially de-risks §3: the per-file-pragma approach is not a proposal to validate, it is an
**existing, green, two-file precedent**. What remains genuinely new is the **`bootstrap` global
fake** (§3.3), for which there is no precedent anywhere in the suite.

### 1.3 The four target modules — untested high-risk behaviors

> **RECORDED FINDING — `toast.js` is at 0 % *executed* coverage despite two tests naming it.**
> `exports.test.js` and `fetch-wrapper.test.js` both declare
> `vi.mock('../toast.js', () => ({ showToast: vi.fn() }))`. The module is **stubbed, never run**, so
> a filename grep reports coverage that the coverage collector does not. Any future claim that
> `toast.js` "has tests" must be checked against the collector, not against a grep. This is the
> concrete reason Packet B is worth doing at all, and the reason `all: true` in the coverage config
> is load-bearing.

**None of the four is executed by any current unit test**, for the reason recorded above.

| Module | LOC | Exports | E2E specs touching it | Untested high-risk behavior |
|---|---:|---:|---:|---|
| [`workout-controls-persistence.js`](../../static/js/modules/workout-controls-persistence.js) | 207 | 9 | **1** (`ui-hardening`) | The whole KI-005 contract: hydration guard (OWNER-1) suppressing *every* save path; single versioned `sessionStorage` key (OWNER-3); per-field fallback to pinned defaults on missing/malformed/non-numeric/out-of-range (TS-7, criterion 9); `declaredRange()` reading `min`/`max` **off the input attributes** so `rir`/`rpe` cap at 10 while weight/sets/reps have **no** upper bound (OWNER-5); `clearWorkoutControls()` leaving the key **absent**, not empty (OWNER-1.4); silent degradation when storage throws |
| [`toast.js`](../../static/js/modules/toast.js) | 111 | 1 | 5 (incidental) | The **legacy-signature branch** (`showToast(msg, true)`) — a pure-logic re-dispatch that E2E cannot distinguish from the modern call; `options`-as-number in **both** signatures; null/undefined message → type-dependent default copy; request-ID suffix **only** when `type === 'error'`; the dispose-then-recreate Bootstrap sequence; both missing-DOM early returns |
| [`exercises.js`](../../static/js/modules/exercises.js) | 70 | 2 | **3** — *corrected from **9** 2026-08-22; see the note under this table* | The module-level `deletingExercises` **double-delete guard** and its `finally` cleanup — the one behavior here that is genuinely hard to reach from E2E; and, in `clearWorkoutPlan()`, that `resetWorkoutControlsToDefaults()` runs **only after the server clear succeeds** and **never on the error path** (KI-005 criterion 4) — *corrected 2026-08-22; see the second note under this table* |
| [`backup-center.js`](../../static/js/modules/backup-center.js) | 1069 | **1** | 1 (`program-backup`) | `detailRequestSequence` **stale-response race guard** (checked twice per fetch); `pendingAction` confirm/cancel state machine; `SORT_PREF_KEY` `localStorage` round-trip; ~15 listener bindings — **all of it behind one exported `initializeBackupCenter()`** |

> **CORRECTION 1 of 2, 2026-08-22 (`b52df68`) — the `exercises.js` E2E count was an over-count:
> 9 → 3.** The **9** was a filename count. The corrected figure is derived from a **stated grep**, and
> every file that grep returns is dispositioned below, so the arithmetic reconciles to 9 rather than
> asking a reader to trust a phrase.
>
> **Pattern:** `rg -n "remove_exercise|removeExercise|clear_workout_plan|clearWorkoutPlan" e2e/` →
> **9 spec files** (plus `e2e/fixtures.ts`, not a spec). Opening every hit:
>
> | File | What the hits are | Drives the module? |
> |---|---|---|
> | `e2e/exercise-interactions.spec.ts:218` | Clicks the real delete button; waits for `POST /remove_exercise`; asserts status 200 only. **Wrapped in `if (count > 0)`** — vacuous on an empty table | **Yes**, weakly |
> | `e2e/superset-edge-cases.spec.ts:256-277` | Clicks the real delete button; asserts 200 + row count + partner unlinked | **Yes** |
> | `e2e/ui-hardening.spec.ts:996-1034` | Drives `#clear-plan-btn` → `#confirmClearPlanBtn`, i.e. the real `clearWorkoutPlan()`. Asserts the **modal closes** (`:1018`) and KI-005's **end state** | **Yes** — the sole spec |
> | `e2e/empty-states.spec.ts:33` | Declares a **local helper also named `clearWorkoutPlan`** that calls `resetWorkoutPlan(page)` and reloads. **Never invokes the module** — a pure name collision | No |
> | `e2e/api-integration.spec.ts:50,146` | `request.post('/clear_workout_plan')` and `request.post('/remove_exercise')` — **route level, no browser JS** | No |
> | `e2e/error-handling.spec.ts:282` | Raw `fetch('/remove_exercise')` inside `page.evaluate` — bypasses the module | No |
> | `e2e/progression.spec.ts:671,677` | `page.request.post` — route level | No |
> | `e2e/program-backup.spec.ts:45,368` | `page.request.post` — route level | No |
> | `e2e/workout-log.spec.ts` | `page.request.post` — route level | No |
> | `e2e/volume-progress.spec.ts` | `page.request.post` — route level | No |
> | *(`e2e/fixtures.ts:315-316`)* | `page.request.post` inside a shared helper — route level, and **not a spec file**, so it is outside the 9 | No |
>
> **9 = 3 that drive the module + 6 that do not.** Note `e2e/accessibility.spec.ts` is **not** in the
> 9: it is a **content** hit only under the broader `exercise` stem — `#clearPlanModal` in a comment
> at `:589`, `ADD_EXERCISE_BTN` at `:598`/`:1037`, `#exerciseSelect` at `:826` — and **no hit invokes
> either export**. Calling it "a filename hit only" would be wrong; it is named here so a reader who
> greps a looser pattern is not surprised by it.
>
> Only this one cell is corrected. The full disposition, and the list of behaviors with **zero** E2E
> coverage at any tier, is **§11.2** — and that list, not the count, is Packet C's case for existing.

> **CORRECTION 2 of 2, 2026-08-22 — the KI-005 criterion-4 claim in this row was an over-read, and it
> has been in this document since 2026-08-15.** The row previously said the module carries *"the
> ordering contract in `clearWorkoutPlan()` where `resetWorkoutControlsToDefaults()` must run **after**
> the refresh (KI-005 criterion 4)"*. **Criterion 4 does not say that.**
> [`docs/ki005_controls_persistence/PLANNING.md:448`](../ki005_controls_persistence/PLANNING.md) says
> only that the reset is called from `clearWorkoutPlan()` **after the successful server clear**, and
> that it *"calls `clearWorkoutControls()` **LAST**"* — a **LAST that is internal to the helper**
> (`static/js/modules/workout-plan.js:408-413`: `withHydrationSuppressed(applyWorkoutControlDefaults)`
> and then `clearWorkoutControls()`), **not** a position relative to `fetchWorkoutPlan()`. The same
> wording appears at `:396` and `:633`. Measured against the code, `fetchWorkoutPlan()`
> (`workout-plan.js:90-117`) touches **no** workout control and does its DOM work after
> `await api.get(...)`, so swapping the reset against the refresh is **not observable in production**.
> The row now states the property criterion 4 **does** assert and Packet C **can** honestly pin: the
> reset runs **only after `api.post` resolves**, and **never on the error path**. The call-order
> assertion Packet C still makes is **characterization**, and is labelled as such at §11.3-C19,
> §11.8-P33 and §11.11-R8.

**The cross-module contract worth pinning first.** `exercises.js:12` and `:36` call
`showToast(message, true)` — the **legacy** signature. `toast.js:15` routes it through the
backward-compatibility branch. Nothing currently asserts that this pairing works; a well-meant
cleanup of either side breaks the other silently, and every E2E spec would still pass as long as
*some* toast appears.

---

## 2. Proposed test packets, ordered by risk and file ownership

Ordering principle: **highest contract density per line, lowest collaborator count, and one owned
file per packet.** Each packet is independently shippable and owns its test file exclusively; none
owns a production file.

**Owner-ratified sequence (Q1):** **A → B → C**, strictly in that order, each merged before the next
begins. **D is dropped** (Q3). **F** (§2.5) follows C and is a **required predecessor to promotion**,
not to the expansion itself. **The letter E is deliberately vacant in step 12** — see §2.6.

### 2.1 Packet A — `workout-controls-persistence.js` *(AUTHORIZED — first)*

- **Owns**: `static/js/modules/__tests__/workout-controls-persistence.test.js` (new). No production file.
- **Why first**: the best risk-to-cost ratio in the set. **Zero module imports** — no `vi.mock` at
  all — so it needs jsdom plus `sessionStorage` and nothing else. It is the densest written contract
  in the four (nine numbered criteria and five owner rulings, all in the module header), and it has
  the **thinnest** E2E coverage (one spec).
- **Coverage targets**: hydration suppression on both save paths; `withHydrationSuppressed()`
  restoring the *previous* flag rather than clearing it; single-key storage shape; the four TS-7
  fallback classes; attribute-derived bounds including the deliberate **absence** of an upper bound
  on weight/sets/reps; `restored[]` reporting only valid fields; key **absent** after clear;
  silent degradation when `getStore()`/`setItem` throws.
- **Caution**: module-level `hydrating` persists across tests in a file — see §4.1.

### 2.2 Packet B — `toast.js` *(**SHIPPED** — Gate 1 approved and executed 2026-08-22, **MERGED as PR #406** / squash `987588a`; §10.11, §10.12, §10.13)*

- **Owns**: `static/js/modules/__tests__/toast.test.js` (new). No production file.
- **Why second**: most-imported module in the app at **0 % executed** coverage, and its legacy-
  signature branch is the highest-value pure logic that E2E structurally cannot reach.
- **Coverage targets**: both signatures and the number-as-`options` form in each; default copy for
  null/undefined message split by type; request-ID suffix present for `error` and **absent** for
  every other type; background-class add/remove; action button wiring (`type`, `aria-label`,
  hide-then-invoke order, `onClick` throwing being caught); both missing-DOM early returns.
- **New work**: this is the first test in the repo to need a **`bootstrap` global fake** (§3.3).

### 2.3 Packet C — `exercises.js` *(AUTHORIZED — third; **Gate 1 approved and executed 2026-08-22**, PR open and **NOT merged** — §11.16, §11.17, §11.18)*

- **Owns**: `static/js/modules/__tests__/exercises.test.js` (new). No production file.
- **Why third**: heavily E2E-covered already, so unit value is narrower — but the double-delete
  guard and the legacy-signature pairing are real and currently unpinned.
- **Coverage targets**: guard rejects a concurrent second call for the same id and **releases** it
  in `finally` on both success and failure; missing-id early return; `showToast` receiving **both**
  legacy call shapes — **three two-argument** calls (`:12`, `:36`, `:68`) and **two one-argument**
  calls (`:31`, `:59`), measured §11.2; `notifyVolumeAffectingPlanChange` reason strings; and, in
  `clearWorkoutPlan()`, that `resetWorkoutControlsToDefaults()` runs **only after the server clear
  succeeds** and **never on the error path**.
- **Collaborators to mock**: `toast.js`, `workout-plan.js`, `workout-plan-events.js`,
  `fetch-wrapper.js` — four, versus zero for Packet A. Plus a `bootstrap.Modal` fake.

> **CORRECTED 2026-08-22 (Gate 1 owner ruling, correction 4 of 4 outside §11; plan-hygiene correction
> 3 of 4).** Two claims in the coverage-targets bullet were false as measured, and both were the
> *source* wording that §11 had to argue against rather than inherit:
>
> 1. ***"`showToast` receiving the legacy two-argument shape"*** covered **3 of the 5** call sites.
>    `exercises.js:31` and `:59` are the legacy **one-argument** form (§11.2's measured table), and
>    §11.3 pins **both** arities. The corrected bullet names the split.
> 2. ***"the KI-005 criterion-4 ordering in `clearWorkoutPlan()`"*** attributed an **ordering** to
>    criterion 4 that it does not state. `ki005_controls_persistence/PLANNING.md:448` says the reset is
>    called *after the successful server clear*, and its "LAST" is **internal to the helper**
>    (`workout-plan.js:408-413`). This is the same false attribution corrected at §1.3 (correction 2)
>    and it is corrected here for the same reason — leaving it would let a reader re-derive the
>    over-read §11.15-C-1 had to unwind.
>
> **What is contract and what is characterization, stated so the distinction is not lost again:** the
> **contract** is `api.post` → `resetControls` — the reset runs only after the server clear resolves and
> **never** on the error path (pinned by §11.3-C19's relation and decisively by **C25**). **Everything
> else in the call order is characterization of current behavior**, because no ordering among
> `fetchWorkoutPlan`, `notifyVolume` and `resetControls` is observable in production —
> `fetchWorkoutPlan()` touches no workout control and the sole
> `workout-plan:volume-affecting-change` listener is **150 ms-debounced** (§11.2). A red on one of
> those relations means *"confirm intent"*, not *"a user-visible defect"* (§11.11-R8).
>
> **The *"Why third"* bullet is deliberately NOT edited.** Its *"heavily E2E-covered already"* framing
> is superseded by §11.2's measurement (**3** specs, one vacuous on an empty table), which is recorded
> in the section that owns it; its **sequencing** judgement — Packet C runs third — is unaffected and
> stands. §11.2's *"§2.3 is still not edited"* sentence is itself corrected by this block.

### 2.4 Packet D — `backup-center.js` — **DROPPED from step 12 (owner ruling Q3, 2026-08-15)**

> **CLOSED UNSTARTED.** `backup-center.js` is **not** covered by step 12. No test file for it may be
> written under this packet, and its 0 % coverage is an **accepted, recorded** gap for the duration
> of step 12 — not an oversight to quietly close later.

The reasoning behind the ruling, retained: `backup-center.js` is 1069 lines behind a **single**
export, `initializeBackupCenter()`, with eight module-level mutable variables. Unit-testing its named
risks at the exported surface means standing up the entire Backup Center DOM and driving listeners —
an integration test wearing a unit test's clothing, and the most expensive and most brittle of the
four by a wide margin.

The only route that would make it genuinely unit-testable — extracting `detailRequestSequence` and
the `pendingAction` state machine into seams — is a **production change**, outside step 12's
test-only scope and outside anything D2 authorizes. **The owner ruled that extraction out of scope.**

**Consequences to carry forward:**

- The module keeps its existing coverage: one E2E spec (`program-backup.spec.ts`) and nothing at unit
  level. That spec is now the **sole** guard on the stale-response race guard and the confirm/cancel
  state machine.
- Reviving this needs its **own** Gate 0 and its own plan — it is not a follow-up any step-12 packet
  may absorb, and Packets A–C must not grow a `backup-center` test "while they are in there".

### 2.5 Packet F — Vitest inventory + drift enforcement *(AUTHORIZED — required before promotion)*

Promoted from question **Q5** to a **blocking predecessor of D2** by the owner on 2026-08-15.

- **Owns**: [`scripts/generate_test_inventory.py`](../../scripts/generate_test_inventory.py) and the
  regenerated [`docs/test_inventory/`](../test_inventory/) artifact.
- **Runs**: after Packet C, so it pins the **post-expansion** node set rather than a count that is
  about to change three times.
- **Why it blocks promotion.** §5 measures that the generator has **zero** vitest references, so JS
  unit is the **only** test tier with no drift pin. Today that is a tolerable gap. The moment
  `js-unit` becomes required it stops being tolerable: a required check would guard a node count that
  **nothing pins**, so deleting or `.skip`-ing every new case added by Packets A–C would leave the
  check green and CI silent. Requiring a check whose contents can be emptied without detection is a
  false green by construction — the exact failure class the false-green hardening arc exists to
  prevent. **Packet F closes that hole before, not after, the check starts blocking merges.**
- **Scope**: extend the generator to collect Vitest nodes (`vitest list` or equivalent, pinned to the
  same deterministic-output discipline as the pytest and Playwright collectors), emit per-file case
  counts into the committed artifact, and let the existing `--check` drift gate cover them. **No new
  required context is added by this packet** — `Test Inventory Drift` is already required, so the new
  surface inherits enforcement without a branch-protection change.
- **Note it will trip its own gate, once and deliberately.** Adding a pinned surface changes the
  artifact, so this packet regenerates and commits it in the same change. That is the documented
  repair path, not a workaround.
- **Ordering caution.** Packets A–C add Vitest cases that the artifact does **not** yet track (§5),
  so they require no regeneration. Once F lands, **every later JS test change does** — a reversal of
  the rule stated in §5, and the reason F must come last rather than first.

---

### 2.6 Relabel record — step-12 "Packet E" → "Packet F" (2026-08-15)

**Administrative only. Owner-directed. No scope or ordering change.**

| | Before | After |
|---|---|---|
| Step-12 Vitest inventory/drift packet | Packet E | **Packet F** |
| Step-11 restore-path fuzz packet (`PLANNING.md`) | Packet E | **Packet E — unchanged, untouched** |
| Step-12 sequence | A → B → C, D dropped, then E | **A → B → C → F**, D dropped |
| Step-12 letter E | in use | **deliberately vacant** |

**What did not change**: Packet F's scope, its contents, its rationale, its position after Packet C
and before D2, and its status as a required predecessor to promotion. The revised gate in §0.1 has
the same four conditions it had before the relabel; only condition 2's letter differs.

**Why the letter is left vacant rather than reused.** Reusing E for some later step-12 packet would
recreate exactly the ambiguity this relabel removes — two "Packet E"s in one directory, one of them
newer than the collision note that warns about it. A vacant letter costs nothing and cannot be
misread.

**Done while it was still cheap.** Nothing outside this document referenced step-12 Packet E — the
packet had not been started, and PR #387 was still draft. The relabel therefore touches one file and
zero commits of implementation work. Renaming after Packet F had merged, or after other documents
cited it, would have meant chasing references across the repository.

---

## 3. jsdom adoption plan

**The global environment does not change, and no existing test is touched.** This is F5-6's cheaper
path, and §1.2 shows it is already in production use here.

### 3.1 What stays exactly as it is

- `vitest.config.js` keeps `environment: 'node'`. **No edit to this file is proposed.**
- `include: ['static/js/**/*.test.js']` already matches new co-located files — **no config change is
  needed to pick up any packet above.**
- The coverage block stays report-only (`all: true`, no `thresholds`). Expansion moves the reported
  number; it must not introduce a gate. D1 was signed as non-blocking measurement.
- All **10** existing test files are untouched, including the 8 that run under Node.

> The config's own header comment already prescribes this approach by name and cites `toast.js` as
> the example. Packets A–C implement that comment; they do not amend it.

### 3.2 What each new file adds

Exactly one line, first line, before any import:

```js
// @vitest-environment jsdom
```

Vitest resolves this per file, so a jsdom packet and a Node packet coexist in one run with no
project split, no `environmentMatchGlobs`, and no second config.

### 3.3 The one genuinely new mechanic — the `bootstrap` global

`toast.js` and `exercises.js` reach for a **global** `bootstrap` (`bootstrap.Toast`,
`bootstrap.Modal`) that the app supplies via a CDN-less vendor script tag, not via an ES import.
jsdom does not provide it and no existing test fakes it.

Proposed rule, to be applied identically in Packets B and C:

- Install an explicit fake on `globalThis.bootstrap` in `beforeEach`; delete it in `afterEach`.
- Fake **only** the surface the module under test actually calls — for `toast.js` that is
  `Toast.getInstance`, `Toast` as a constructor, `.show()`, `.hide()`, `.dispose()`.
- Assert the **sequence** where the module depends on it (`dispose()` before `new Toast(...)`;
  `hide()` before `action.onClick()`), because that ordering is the actual contract.
- **Never** import real Bootstrap into a unit test — that would make these tests a Bootstrap
  upgrade's problem, which is what the visual and E2E tiers already own.

### 3.4 Explicitly out of scope

No jsdom migration of the 8 Node-environment files; no global environment flip; no
`jsdom` version change (30.0.1 is pinned and current); no new devDependency.

---

## 4. Determinism, fixture, and mocking rules

These are proposed rules for the packets, not changes to existing tests.

### 4.1 Module-level state must be reset explicitly — `restoreAllMocks` is not enough

The existing jsdom precedent uses `vi.restoreAllMocks()` in `beforeEach`. That restores **spies**.
It does **not** reset a module's own top-level variables, and three of the four targets carry them:
`hydrating` (persistence), `deletingExercises` (exercises), and eight variables in backup-center.

**Rule**: any file testing a module with top-level mutable state either calls `vi.resetModules()`
and re-imports per test, or drives the state back to a known value through the module's own exported
API (`endHydration()` for Packet A). State that can only be reset by re-import is a finding to
record, not to work around silently.

### 4.2 Fixtures

- DOM built in `beforeEach` via `document.body.innerHTML`, matching the existing precedent.
- Fixture markup must carry the **real attributes the module reads** — Packet A's inputs need their
  actual `min`/`max`, because `declaredRange()` derives behavior from them. A fixture without those
  attributes would make every bounds test vacuously pass. This is the single most likely
  false-green in the set. Measured from
  [`templates/workout_plan.html`](../../templates/workout_plan.html) lines 88-100, the four
  attribute-bearing controls are:

  | Input | `min` | `max` | `step` | `value` |
  |---|---|---|---|---|
  | `weight` | `0` | *(none — deliberate, OWNER-5)* | `any` | `25` |
  | `sets` | `1` | *(none — deliberate)* | — | `3` |
  | `rir` | `0` | `10` | — | `3` |
  | `rpe` | `1` | `10` | `0.5` | `7` |
  | `min_rep` | `1` | *(none — deliberate)* | — | `6` |
  | `max_rep_range` | `1` | *(none — deliberate)* | — | `8` |

  **Four of the six have no upper bound** — `weight`, `sets`, `min_rep`, `max_rep_range`. Only `rir`
  and `rpe` cap, both at `10`. A test asserting an upper-bound rejection on any of the four would be
  asserting a rule the product does not have, and must not be written.

  The template's `value` attributes are **identical** to `WORKOUT_CONTROL_DEFAULTS`
  (`25/3/3/7/6/8`), which is what makes "fall back to the pinned template default" coherent.
- Fixture markup is **copied from the live template**, not invented, and the template path is cited
  in a comment so drift is greppable.
- `sessionStorage.clear()` / `localStorage.clear()` in `beforeEach`; jsdom shares them across tests
  in a file.

### 4.3 Mocking

- `vi.mock` at module top level (hoisted), matching `exports.test.js`.
- Mock **collaborators**, never the module under test.
- `fetch` via `vi.spyOn(globalThis, 'fetch')`, never a global reassignment.
- Assert **call shape**, not just call count, where a cross-module contract exists — Packet C must
  assert `showToast` received the two-argument legacy shape, since that is the contract §1.3 names.

### 4.4 Determinism

- No real timers. `toast.js` passes `delay` into Bootstrap, which the fake receives as data, so no
  fake-timer machinery is required; if a packet ever needs one, `vi.useFakeTimers()` with a matching
  `vi.useRealTimers()` in `afterEach`.
- No dependence on test file or case ordering; each case sets up its own state.
- No network, no filesystem, no dev server, no SQLite.
- No `Date.now()`/`Math.random()` dependence without injection or a spy.

### 4.5 The honesty rule

Every packet must include at least one **mutation check**: break the production behavior the test
claims to pin, confirm the test reds, revert. Record it in the packet's evidence section. A test
that passes against both the real and the broken implementation pins nothing — the standing lesson
from the false-green hardening arc, and the reason `all: true` is set in the coverage config.

---

## 5. Test-node inventory consequences

**Measured: none. Packets A–C cannot trip `Test Inventory Drift`.**

`scripts/generate_test_inventory.py` contains **zero** references to `vitest`, `test:js`,
`static/js`, or `*.test.js` (grep over the whole file returns nothing). The artifact
(`docs/test_inventory/TEST_INVENTORY.json` / `.md`) pins five surfaces, per
[`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md):

| Pinned surface | Tripped by | Packets A–C? |
|---|---|---|
| Per-file pytest node counts | `tests/**` | No |
| Per-spec Playwright counts | `e2e/**/*.spec.ts` | No |
| `waitForTimeout` lines per file | `e2e/**/*.ts` | No |
| Required functional spec set | `ci.yml` `e2e-functional-shard` list | No |
| Parametrized configuration surface | add/delete under `.claude/commands|agents|rules/`, `docs/ai_workflow/` | No |

Adding `static/js/modules/__tests__/*.test.js` touches none of them. **No inventory regeneration is
required by any packet in §2**, and none may be committed as if it were.

**This document itself** lands under `docs/testing_phase3/` — also not a pinned surface, and under
QUALITY_GATE's *Product docs only* row, which requires no tests.

> **The gap this reveals — now owned by Packet F.** JS unit nodes are the **only** test tier with no
> drift pin. A silently deleted or `.skip`-ed Vitest case is invisible to CI in a way the equivalent
> pytest or Playwright deletion is not — and that gap widens with every packet added. It becomes
> materially more serious **if** `js-unit` is promoted, because a required check would then be
> guarding a node count nothing pins.
>
> **Owner ruling Q5 (2026-08-15): closing this is now a required predecessor to promotion**, carried
> as **Packet F** (§2.5). It runs **after** Packet C and **before** D2 may be signed.

> **The statement above expires when Packet F lands.** "No inventory regeneration is required" is
> true for Packets A–C **only**. Once F pins Vitest nodes, every subsequent JS test add, remove, or
> rename **will** trip `Test Inventory Drift` and **will** require a regenerated artifact — the same
> discipline `tests/**` and `e2e/**` already carry. Anyone reading this section after F has merged
> should read §2.5 first.

---

## 6. Measured stability evidence

### 6.1 Method

The overall workflow conclusion was **not** used — it reflects ~18 other jobs and would answer a
different question. Every run was resolved to the **job level** via
`GET /repos/:owner/:repo/actions/runs/{id}/jobs`, filtering on the exact context string
`JS Unit (Vitest, non-required)`.

| Parameter | Value |
|---|---|
| Workflow | `ci.yml` (`CI/CD Pipeline`) |
| Window | **2026-07-29T06:29:19Z → 2026-08-15T01:55:52Z** = **16 d 19 h 26 m** |
| Runs enumerated | **515** (all events: `push`, `pull_request`) |
| Runs probed at job level | **515** (probe errors: 0) |
| Job introduced | `6446b7c` (PR #142) — **predates the window**, so no run is missing the job for that reason |

### 6.2 Results

| Outcome | Count |
|---|---:|
| `success` | **510** |
| `failure` | **3** |
| Job absent (whole run had **zero** jobs) | **2** |

**All 3 failures are the same branch, the same day, and the same attributable cause.**

| Run | Time | Branch | Duration |
|---|---|---|---:|
| [`30707924490`](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/actions/runs/30707924490) | 2026-08-01T16:31Z | `dependabot/npm_and_yarn/jsdom-30.0.1` | 20 s |
| [`30709687357`](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/actions/runs/30709687357) | 2026-08-01T17:11Z | `dependabot/npm_and_yarn/jsdom-30.0.1` | 22 s |
| [`30715929723`](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/actions/runs/30715929723) | 2026-08-01T19:58Z | `dependabot/npm_and_yarn/jsdom-30.0.1` | 19 s |

Root cause, read from the job log of `30715929723`: at commit `afdea86` the `js-unit` job pinned
`node-version: '20'`, while the PR under test raises `jsdom` to 30.0.1, which declares
`engines.node: ^22.13.0 || >=24.0.0`. The log shows `npm warn EBADENGINE … current: { node:
'v20.20.2' }` followed by `Process completed with exit code 1`. **This is a deterministic
environment incompatibility introduced by the change under test — the job correctly reporting a real
defect, not flake.** It is fully resolved: `jsdom` 30.0.1 merged as **#250** (`cc91c57`) and `ci.yml`
now pins `node-version: '24'`.

**The 2 job-absent runs are not a `js-unit` gap.** Both are pushes to `main` on 2026-08-01
(`30708534843`, `30711234413`) with `conclusion: cancelled` and `total_count: 0` — **no jobs ran at
all**. That is the concurrency-group behavior `ci.yml` documents in its own header comment (a queued
run cancelled when a newer run joins the group), and it affects every job in the workflow equally.
Verified by re-querying the runs directly rather than inferred from the probe's empty result.

### 6.3 The clean streak

| Measurement | Value |
|---|---|
| Last `js-unit` failure of any kind | **2026-08-01T19:58:50Z** |
| Runs since, at job level | **331** |
| Failures among them | **0** |
| Elapsed | **13 d 5 h 57 m** |
| Strict 14-day mark falls at | **2026-08-15T19:58:50Z** |

### 6.4 Is promotion ready? — **No, on two independent grounds**

**(a) The strict window is not yet closed.** Measured from the last red, the streak is **13 d 5 h
57 m** — short of fourteen days by **≈18 h**. It closes later today, 2026-08-15T19:58:50Z. If the
owner's intent is *fourteen days since the last red on any cause*, the answer becomes yes tonight,
and this ground alone is thin — the three reds were attributable and resolved, so a reasonable owner
could discount them and call the window already satisfied.

**(b) The window was earned by the wrong suite — this is the load-bearing objection.** Step 12 reads:
*"JS unit expansion with jsdom … **then** promote the Vitest job to required **once green for 2
weeks**."* The order is expansion first. Every one of the 331 green runs executed a **120-case suite
that touches none of the four target modules**, at 5.6 % statement coverage. Promoting on that
evidence would make required a check whose stability record says nothing about the code the
expansion is about to add — and jsdom, DOM fixtures, and a `bootstrap` global fake are precisely the
machinery most likely to introduce a flake the current record cannot predict.

**A required check is only worth its process cost if it would have caught something.** Today's suite
would not have. That is an argument for doing Packets A–C, not an argument against D2.

### 6.5 The qualification window, as ratified (owner ruling Q2, 2026-08-15)

> **The strict 14-day window RESTARTS. It runs from the first successful
> `JS Unit (Vitest, non-required)` run on `main` after the final expansion packet lands.**

Consequences, stated so no later session re-reads §6.3 as a promotion credit:

- **The 331-run streak in §6.3 validates the existing 120-case suite only.** It is preserved below as
  the measurement it is, and it **cannot qualify the expanded suite**. **Zero** of it carries over.
- The 2026-08-15T19:58:50Z 14-day mark in §6.3 is now **irrelevant to D2**. It marks only when the
  *pre-expansion* suite would have completed a clean fortnight — a fact about a suite that will no
  longer exist.
- The clock starts on **`main`**, not on a PR branch, and on a **successful** run — a cancelled run
  (§6.2 records two) neither starts nor advances it.
- "Final expansion packet" means the last of **A, B, C** to merge. **Packet F** is a separate
  required predecessor (§2.5) and may land inside the window; it does not restart it.
- Any `js-unit` failure during the window **resets it to zero**, with the same attribution discipline
  §6.2 applies — an attributable, resolved, externally-caused red should be argued on the record, not
  silently discounted.

---

## 7. The exact branch-protection change, if the owner later signs D2

Recorded so it is unambiguous when the time comes. **Nothing in this section is executed by this
packet.**

### 7.1 Measured current state

`GET /repos/avihay1989/Hypertrophy-Toolbox-v3/branches/main/protection`, read 2026-08-15:

- `required_status_checks.strict`: **`false`**
- `required_status_checks.checks`: **11** entries, each `app_id: 15368` (GitHub Actions)
- `enforce_admins`: `false`; `required_approving_review_count`: **0**
- **`JS Unit (Vitest, non-required)` is absent** — the job is genuinely non-required, matching §8.6.

The 11 are: `Run Tests`, `E2E Functional (Chromium)`, `E2E Backup (Chromium, isolated)`,
`E2E Smoke (Chromium)`, `Type Check (tsc blocking + pyright measure-only)`, `Code Linting`,
`Frontend Build (npm ci + SCSS)`, `Security Audit`, `E2E Fatigue Context (Chromium, non-required)`,
`E2E Erase Flow (Chromium, isolated, non-required)`, `Test Inventory Drift`.

### 7.2 The change

Add a **12th** context. The name must match the workflow's `name:` **byte for byte**:

```
JS Unit (Vitest, non-required)
```

The update replaces the whole `checks` array, so all 11 existing entries must be resent — omitting
one silently un-protects it. This is a **GitHub API/UI change; no repository file grants it.**
Editing `ci.yml` alone does not promote a context, exactly as Phase 0 step 4 records for
`e2e-erase-flow`.

### 7.3 The naming trap — resolve it *before* promotion, or not at all

The job's name ends in `(non-required)`, which becomes false the moment it is promoted. Per
QUALITY_GATE's *CI job naming* section the repository already carries **two** jobs in exactly that
inaccurate state (`E2E Fatigue Context`, `E2E Erase Flow`), deliberately frozen because renaming a
**protected** job orphans its context.

There is a window here that does not reopen:

| Sequence | Outcome |
|---|---|
| Rename **while still unprotected**, then promote the new name | Clean. This is QUALITY_GATE's row 2 ("rename freely — and drop a stale `(non-required)` suffix when its meaning changes"). |
| Promote first, then rename | **Orphans the required context.** Every PR blocks on a check that will never report again. |
| Promote and never rename | Safe, but adds a **third** permanently misleading job name. |

The rename must therefore happen in the change **before** promotion, or be consciously forgone.
This is **question Q4**.

Note also `tests/test_release_workflow_contracts.py` asserts that no job whose `name:` appears in
the required-context list uses `uses:`. `js-unit` is a plain job, so promotion does not violate it —
but converting it to `uses:` afterwards would, and would rename its context by side effect.

### 7.4 Verification after any promotion

Confirm on a throwaway PR that the new context appears as **required** and that its name renders
identically to the protection entry. A missing check-run reads as *pending*, not *passing*, so a
mismatched name blocks every PR silently.

---

## 8. Gate 0 — questions and rulings

**§0.1 is the authority on what was decided.** This table is the record of what was asked, annotated
with each answer.

| # | Question | Ruling (2026-08-15) |
|---|---|---|
| **Q1** | Is step 12's expansion authorized at all? Phase 3 is still a **proposal** — §8.1a and §8.1c both state Phases 2, 3 and 5 are not authorized, and D6's signing covered step 11 *"precondition only"*. | **SIGNED — authorized, Phase 3 test expansion only.** Packets A, B, C. `js-unit` is **not** promoted to required yet. |
| **Q2** | Does the two-week window restart on the **post-expansion** suite (§6.4b), or does the existing 331-run streak count toward D2? | **SIGNED — restarts.** From the first successful `JS Unit (Vitest, non-required)` run on `main` after the final expansion packet lands. See §6.5. |
| **Q3** | `backup-center.js` (Packet D): **skip**, test through the full-DOM `initializeBackupCenter()` surface, or authorize a **production** seam extraction? | **RULED — dropped from step 12.** The required production seam extraction is out of scope. §2.4. |
| **Q4** | Drop the `(non-required)` suffix from the job name **in the change before** promotion? | **OPEN.** Not yet needed — promotion is not authorized. But the window closes permanently once the context is protected (§7.3), so decide it **with** D2 and never after. |
| **Q5** | Extend `generate_test_inventory.py` to pin Vitest node counts? | **RULED — required before promotion.** Carried as **Packet F** (§2.5), sequenced after Packet C. |
| **Q6** | Correct the stale coverage/jsdom claims in `TESTING_STRATEGY_PLANNING.md` (lines 79, 172, 540-541) and `vitest.config.js`'s comment (§1.1, §1.2)? | **OPEN.** Recommendation unchanged: a **separate docs-only packet**. `vitest.config.js` is a config file, so it cannot ride along inside a test packet. |

### STOP — the Gate 0 STOP, **partly superseded**

> **ANNOTATION 2026-08-22 — read this before the paragraphs below.** The first clause is still live and
> governs every unbuilt packet. The second paragraph's *"as of this commit nothing has been
> implemented"* is a **point-in-time statement that two later commits falsified**, and it is annotated
> rather than rewritten so the sequence stays legible. **Two test files now exist**, each built from
> its own scoped plan after its own gate: **Packet A** (§9, `workout-controls-persistence.test.js`,
> merged as `9e5997a` / PR #387) and **Packet B** (§10, `toast.test.js`, built 2026-08-22 under the
> Gate 1 ruling in §10.11, and **merged 2026-08-22 as `987588a` / PR #406**).
> **Everything in the "explicitly still unauthorized" list below remains
> unauthorized and untouched** — no production JS, no `package.json`, no `vitest.config.js`, no CI
> workflow, no branch-protection change, no `backup-center.js` test, and no `.skip` anywhere.

**No implementation begins in this packet.** Q1 authorizes Packets A–C to be *planned and then
built*; it does not make this document their plan, and it does not authorize code written from it
directly. Each packet needs its own scoped plan first.

As of this commit **nothing has been implemented**: no test file, no production JS, no
`package.json`, no `vitest.config.js`, no CI workflow, and no branch-protection setting has been
created or modified. *(Superseded for the two test files only — see the annotation above.)*

**Explicitly still unauthorized:**

- **Promoting `js-unit` to required**, or any branch-protection edit (§7). D2 needs its own signature;
  Q1 does not grant it.
- Any **production JS** change, including the `backup-center.js` seam extraction (§2.4).
- Any `vitest.config.js` or `package.json` edit — §3.1 is a plan to **not** change them.
- Any test for `backup-center.js` under step 12, including one added incidentally to another packet.
- Any `.skip`, tolerance, or threshold that would let an expansion packet land amber (§4.5).

---

## 9. Packet A — scoped plan (`workout-controls-persistence.js`)

> **AUTHORIZED AND IMPLEMENTED 2026-08-15.** This section is now both the specification and the
> execution record. §9.8's matrix has been **run**, and its measured results replace the earlier
> predictions. §9.12 records what shipped; **§9.13 records four evidence-driven deviations**,
> including a defect this section itself contained (D1) and a proven equivalent mutant (D2).
> **`js-unit` remains non-required** — nothing here promotes it.

### 9.1 Ownership and boundaries

| | |
|---|---|
| **Creates** | `static/js/modules/__tests__/workout-controls-persistence.test.js` — one new file |
| **Modifies** | **nothing** |
| **Must not touch** | `vitest.config.js`, `package.json`, any file under `static/js/modules/` other than the new test, `.github/workflows/**`, `docs/test_inventory/**`, branch protection |
| **Environment** | `// @vitest-environment jsdom` — line 1, per §3.2 |
| **Collaborator mocks** | **none.** The module imports nothing (§2.1); a `vi.mock` in this file would be a sign the plan drifted |

### 9.2 The nine exports and the rulings each carries

Every export gets coverage. The middle column is the contract source, quoted from the module header
and [`ki005_controls_persistence/PLANNING.md`](../ki005_controls_persistence/PLANNING.md).

| # | Export | Ruling / criterion | Test IDs |
|---|---|---|---|
| 1 | `WORKOUT_CONTROL_IDS` | criterion 2 — *exactly* these six, no others | A1 |
| 2 | `WORKOUT_CONTROL_DEFAULTS` | TS-7 — the pinned template defaults, one source of truth | A2 |
| 3 | `beginHydration()` | OWNER-1 — arms the guard | A3 |
| 4 | `endHydration()` | OWNER-1 — disarms the guard | A4 |
| 5 | `withHydrationSuppressed(fn)` | OWNER-1 — restores the *previous* flag, not `false` | A5, A6, A7 |
| 6 | `saveWorkoutControls()` | OWNER-1 (no-op while hydrating), OWNER-3 (one versioned key, `sessionStorage` only) | A8–A13 |
| 7 | `applyWorkoutControlDefaults()` | PR-1 — plain value writes, no estimate, no recompute | A14, A15 |
| 8 | `restoreWorkoutControls()` | criterion 8 (saved-wins), criterion 9 + TS-7 (per-field fallback), OWNER-5 (declared bounds only), OWNER-1.1/.2 (never writes) | A16–A28 |
| 9 | `clearWorkoutControls()` | OWNER-1.4 — key left **absent** | A29, A30 |

**Case list.**

| ID | Case | Asserts |
|---|---|---|
| A1 | `WORKOUT_CONTROL_IDS` equals `['weight','sets','rir','rpe','min_rep','max_rep_range']` | Exact array, exact order. Deep equality — not `toContain`, which would pass if a seventh control were added |
| A2 | `WORKOUT_CONTROL_DEFAULTS` equals `{weight:'25',sets:'3',rir:'3',rpe:'7',min_rep:'6',max_rep_range:'8'}` | Exact object, and every value a **string** |
| A3 | `beginHydration()` then `saveWorkoutControls()` | Storage untouched — key absent |
| A4 | `beginHydration()` → `endHydration()` → `saveWorkoutControls()` | Record now written |
| A5 | `withHydrationSuppressed(fn)` returns `fn`'s return value | Return is passed through |
| A6 | `withHydrationSuppressed` while **already** hydrating leaves hydration **on** afterward | The `previous` restore — the nesting bug this guards |
| A7 | `withHydrationSuppressed` whose `fn` **throws** still restores the flag, and rethrows | `finally` correctness; use `expect(...).toThrow()` |
| A8 | `saveWorkoutControls()` writes **one** key, named `hypertrophy_workout_controls_v1` | `sessionStorage.length === 1`; key name exact (OWNER-3) |
| A9 | The stored value parses to an object with exactly the six ids | No extra fields; JSON round-trip |
| A10 | Values are read from the **live DOM**, not from defaults | Set inputs to non-default values first, assert those persist |
| A11 | Nothing is written to `localStorage` | `localStorage.length === 0` (criterion 6) |
| A12 | With **no** control inputs in the DOM, nothing is written | The `found` guard — key stays absent |
| A13 | With **some** inputs present, only those are recorded | Partial DOM does not fabricate fields |
| A14 | `applyWorkoutControlDefaults()` sets all six inputs to `WORKOUT_CONTROL_DEFAULTS` | Per-field value equality |
| A15 | `applyWorkoutControlDefaults()` does **not** write to storage | Key absent afterward |
| A16 | Valid stored record restores all six; `restored` lists all six ids | Saved-wins (criterion 8) |
| A17 | **Absent** key → fields left **untouched**; `restored` is `[]` | TS-7 — **corrected during implementation, see §9.13-D1** |
| A18 | **Malformed JSON** → all six get defaults; `restored` is `[]` | The `catch` returning `{}` |
| A19 | Stored **array** (not object) → treated as empty; `restored` is `[]` | The `!Array.isArray` guard |
| A20 | Stored **`null`** JSON → defaults; `restored` is `[]` | The `parsed && typeof` guard |
| A21 | Field with **non-numeric** string (`'abc'`) → that field defaults, others restore | Per-field, not all-or-nothing |
| A22 | Field with **empty / whitespace** string → that field defaults | The `text === ''` guard |
| A23 | Field with a **boolean / object** value → that field defaults | The `typeof` guard |
| A24 | `rir` stored as `11` → defaults to `'3'` | Upper bound from `max="10"` (OWNER-5) |
| A25 | `rpe` stored as `10.5` → defaults to `'7'` | Upper bound from `max="10"` |
| A26 | `weight` stored as `-1` → defaults to `'25'`; `sets` as `0` → defaults to `'3'` | Lower bounds from `min` |
| A27 | Numeric (non-string) stored values are accepted and applied as strings | `typeof stored === 'number'` branch |
| A28 | `restoreWorkoutControls()` writes **nothing** to storage | OWNER-1.1/.2 — the pre-existing record survives init |
| A29 | `clearWorkoutControls()` leaves the key **absent**, not empty-string | `getItem(...) === null` **and** `sessionStorage.length === 0` (OWNER-1.4) |
| A30 | `clearWorkoutControls()` on already-empty storage is a no-op and does not throw | Idempotence |

**Mixed-validity case, called out because it is the one most likely to be written weakly**: A21
seeds a record where `weight` is valid and `rir` is `'abc'`, then asserts **both** that `weight`
took the stored value **and** that `rir` shows `'3'` **and** that `restored` is exactly
`['weight']`. Asserting only the fallback would pass against an implementation that discards the
whole record.

### 9.3 Fixture structure

Built in `beforeEach` via `document.body.innerHTML`, copied from
[`templates/workout_plan.html`](../../templates/workout_plan.html) **lines 88-108** with that path
and line range in a comment above it so drift is greppable (§4.2).

**The `min`/`max` attributes are load-bearing** — `declaredRange()` reads them off the elements, so a
fixture without them makes every bounds case (A24–A26) pass vacuously. Exact values as measured:

| `id` | `type` | `min` | `max` | `step` | `value` |
|---|---|---|---|---|---|
| `weight` | `number` | `0` | *(absent)* | `any` | `25` |
| `sets` | `number` | `1` | *(absent)* | — | `3` |
| `rir` | `number` | `0` | `10` | — | `3` |
| `rpe` | `number` | `1` | `10` | `0.5` | `7` |
| `min_rep` | `number` | `1` | *(absent)* | — | `6` |
| `max_rep_range` | `number` | `1` | *(absent)* | — | `8` |

`class`, `name`, `placeholder`, and `aria-label` are **omitted** — the module never reads them, and
copying them in invites a reader to think they matter.

**A31 — a fixture self-check**, so the fixture cannot silently rot into a vacuous one: assert that
`#rir` and `#rpe` each report `max === '10'`, and that `#weight`, `#sets`, `#min_rep`,
`#max_rep_range` each report `getAttribute('max') === null`. If a future edit strips the attributes,
A31 reds immediately instead of A24–A26 quietly passing for the wrong reason.

Cases that need a **partial** or **empty** DOM (A12, A13) set their own `innerHTML` inside the test,
after the shared `beforeEach`.

### 9.4 Isolation and reset — module-level `hydrating`

`hydrating` is a module-level `let` (line 39). It is **not** reset by `vi.restoreAllMocks()`, and a
test that leaves it `true` would make every later `saveWorkoutControls()` case in the file pass for
the wrong reason — a false green that looks like a pass (§4.1).

**Strategy — belt and braces, both cheap:**

1. **`endHydration()` in `beforeEach`**, unconditionally, as the primary reset. It is an exported
   part of the contract, so this uses the module's own API rather than reaching into its internals.
2. **`endHydration()` in `afterEach`** as well, so a test that throws mid-way cannot poison the next.

`vi.resetModules()` is **deliberately not used**: it would force a dynamic re-import in every case
and buys nothing here, since `endHydration()` fully restores the only mutable state the module has.
**If a case is ever added that `endHydration()` cannot reset, that is a finding to record, not to
paper over** (§4.1).

**A32 — a leak detector**: the last case in the file asserts that a fresh `saveWorkoutControls()`
writes, proving hydration was left disarmed by everything before it.

### 9.5 `sessionStorage` — setup, teardown, and throwing-storage

jsdom provides a real `sessionStorage` shared across cases in a file (§4.2).

- **Setup**: `sessionStorage.clear()` **and** `localStorage.clear()` in `beforeEach`. `localStorage`
  is cleared so A11's "nothing leaked to localStorage" cannot pass on a stale-empty accident.
- **Seeding**: cases seed via `sessionStorage.setItem('hypertrophy_workout_controls_v1', <json>)`
  directly — testing `restoreWorkoutControls()` through `saveWorkoutControls()` would couple the two
  and hide a bug present in both.
- **Teardown**: `sessionStorage.clear()` in `afterEach`, plus `vi.restoreAllMocks()` to undo the
  throwing-storage spies below.

**Throwing-storage simulations** — the module has three independent `try`/`catch` sites, and each
gets its own case:

| ID | Simulation | Expected |
|---|---|---|
| A33 | `vi.spyOn(Storage.prototype,'setItem').mockImplementation(() => { throw new DOMException('QuotaExceededError') })`, then `saveWorkoutControls()` | Does **not** throw; degrades silently |
| A34 | `vi.spyOn(Storage.prototype,'getItem').mockImplementation(() => { throw new Error('denied') })`, then `restoreWorkoutControls()` | Does **not** throw; returns `{restored: []}`; fields left **untouched** (**corrected — §9.13-D1**) |
| A35 | `vi.spyOn(Storage.prototype,'removeItem').mockImplementation(() => { throw new Error('denied') })`, then `clearWorkoutControls()` | Does **not** throw |

**`getStore()`'s own `try`/`catch`** (a `window.sessionStorage` *access* that throws — the private-mode
case) is **not** simulated: making a property access throw in jsdom requires redefining `window`,
which is more fragile than the branch is worth. **Recorded as a deliberate, named coverage gap**
rather than left as an unexplained blank — the honest disclosure §4.5 and the no-silent-caps rule
both require.

### 9.6 Fallback and `restored[]` assertions

- **Fallback**: asserted as the **literal expected string**, never `WORKOUT_CONTROL_DEFAULTS[field]`.
  Reading the expectation from the same constant the implementation reads makes the assertion
  tautological — it would pass even if the constant were wrong. A2 pins the constant once; every
  other case hard-codes (`expect(el('rir').value).toBe('3')`).
- **`restored[]`**: asserted with **exact deep equality on the whole array**, including order —
  `expect(result.restored).toEqual(['weight','sets','rir','rpe','min_rep','max_rep_range'])`. Never
  `toContain`, never `.length`. `toContain` would pass on a superset, and length alone would pass on
  the wrong fields. Iteration order follows `WORKOUT_CONTROL_IDS`, so order is part of the contract.
- **Empty case**: `expect(result.restored).toEqual([])` — distinct from `toBeFalsy()`, which an
  accidental `undefined` return would also satisfy.

### 9.7 Explicit confirmation — no upper-bound rejection tests

> **Confirmed. No case in Packet A asserts that `weight` or `sets` rejects a large value, and none
> may be added.**

Extended to what the template actually says: **four** of the six controls have **no `max`
attribute** — `weight`, `sets`, `min_rep`, and `max_rep_range` (§9.3). Under OWNER-5, "out of range"
means *the input's own declared bounds and only those*. Asserting an upper-bound rejection on any of
the four would invent a product rule, and inventing one here would make a reload non-transparent —
the exact failure OWNER-5 exists to prevent. Server-side, `utils/workout_validation.py:65-71` still
rejects an absurd value at add time, exactly as it would if the user had typed it without reloading.

Bounds cases are therefore **only**: A24/A25 (`rir`, `rpe` upper, from `max="10"`) and A26 (lower
bounds, from `min`). **A31** pins the *absence* of the four `max` attributes so this stays true.

### 9.8 Mutation matrix (§4.5) — **EXECUTED 2026-08-15, measured results**

All 19 rows were run. Each applies a deliberate break, runs the **full** Vitest suite, records which
case IDs red, then restores the file. The harness asserts each mutation matches **exactly once**
before running — a mutation that silently fails to apply is otherwise indistinguishable from one the
tests failed to catch. The module and test file are asserted byte-identical to their pristine state
afterward.

**Result: 18 of 19 killed. 1 survivor, analysed below and confirmed an equivalent mutant.**

| # | Deliberate break | Predicted | **Measured** | Verdict |
|---|---|---|---|---|
| M1 | `saveWorkoutControls`: delete `if (hydrating) return;` | A3 | A3, A6 | ✅ killed |
| M2 | `withHydrationSuppressed`: `hydrating = false` in `finally` instead of `= previous` | A6 | A6 | ✅ killed |
| M3 | `withHydrationSuppressed`: drop the `try`/`finally`, call `fn()` bare | A7 | A7 | ✅ killed |
| M4 | `STORAGE_KEY` → drop `_v1` | A8 | A8 + 17 others | ✅ killed |
| M5 | `getStore()` returns `window.localStorage` | A11 | A11 + 19 others | ✅ killed |
| M6 | `saveWorkoutControls`: delete `if (!found) return;` | A12 | A12 | ✅ killed |
| M7 | `validateStoredValue`: `return text` before the range checks | A24, A25, A26 | A24, A25, A26 | ✅ killed |
| M8 | `declaredRange`: return `{min: undefined, max: undefined}` | A24, A25, A26 | A24, A25, A26 | ✅ killed |
| M9 | `declaredRange`: read `max` where `min` is read | A26 | A16, A26 | ✅ killed |
| M10 | `restoreWorkoutControls`: `continue` instead of applying the default | A18, A21 | A18–A26 (9 cases) | ✅ killed |
| M11 | `restoreWorkoutControls`: push every field, valid or not | A18, A21 | A18–A27 (10 cases) | ✅ killed |
| M12 | `readRecord`: `catch` returns `null` instead of `{}` | A18 | A18 | ✅ killed |
| M13 | `readRecord`: drop the `!Array.isArray(parsed)` guard | A19 | **(none red)** | ⚠️ **SURVIVED — equivalent mutant, §9.13-D2** |
| M14 | `clearWorkoutControls`: `setItem(STORAGE_KEY, '')` instead of `removeItem` | A29 | A29, A30 | ✅ killed |
| M15 | `validateStoredValue`: drop `if (text === '') return null;` | A22 | A22 | ✅ killed |
| M16 | `restoreWorkoutControls`: save before returning | A28 | A28 | ✅ killed |
| M17 | `saveWorkoutControls`: remove the `try`/`catch` around `setItem` | A33 | A33 | ✅ killed |
| M18 | `WORKOUT_CONTROL_IDS`: append a seventh id | A1 | A1 | ✅ killed |
| M19 | **Fixture**: strip `max="10"` from `#rir` | A31 | A24, A31 | ✅ killed |

**Every prediction was a subset of what actually red** — no row killed *fewer* cases than predicted.
M4, M5, M10 and M11 red far more than predicted because they break a shared path; over-detection is
not a defect.

**M19 is the anti-vacuity check** and it worked: it breaks the *fixture* rather than the module, and
A31 caught it. A24 also red, confirming the mechanism — without `max="10"` on `#rir`, the stored `11`
is accepted, which is exactly the vacuous pass A31 exists to prevent.

### 9.9 Gate

| Gate | Command | Expected | **Measured 2026-08-15** |
|---|---|---|---|
| JS unit — baseline | `npm run test:js` | 10 files / 120 cases | **10 files / 120 passed** ✅ (matches CI run `31856035853` exactly) |
| JS unit — with Packet A | `npm run test:js` | 11 files, 120 + ~35 | **11 files / 155 passed**, 793 ms ✅ — exactly **+35**, so no existing test was touched |
| Mutation | §9.8, full suite per row, reverted | Every row reds its named cases | **18/19 killed**; 1 equivalent mutant (§9.13-D2) ✅ |
| Inventory | **none — see §9.10** | no drift | **`--check` → "Test inventory is up to date", exit 0** ✅ |

The **+35 delta is itself the assertion** that Packet A touched no existing test: 155 − 120 = 35, the
exact case count in §9.2.

Full `/verify-suite` is **not** required: a new file under `static/js/modules/__tests__/` matches
QUALITY_GATE's *Frontend (JS)* row only in path, and adds no production behavior for an E2E spec to
cover. The existing E2E specs are unaffected and are not re-run for this packet.

The 120-case count is itself an assertion: if it moves, Packet A touched an existing test, which it
must not.

### 9.10 Inventory regeneration — deferred, confirmed

> **Confirmed: Packet A requires NO test-inventory regeneration, and none may be committed with it.**

Measured in §5 — `scripts/generate_test_inventory.py` has **zero** references to `vitest`, `test:js`,
`static/js`, or `*.test.js`, and none of the five pinned surfaces covers JS unit tests. Adding
`workout-controls-persistence.test.js` therefore cannot trip `Test Inventory Drift`.

> **Confirmed empirically, not only by reading the generator.** With the new test file present,
> `python scripts/generate_test_inventory.py --check` prints **"Test inventory is up to date"** and
> exits **0**. The claim is now measured from both directions.

**This holds for Packets A, B, and C, and expires when Packet F lands** (§2.5). Once F pins Vitest
nodes, every later JS test change will require a regenerated artifact. A regenerated
`docs/test_inventory/` appearing in Packet A's diff is a **defect in the packet** — most likely the
symptom of an untracked `.md` in a globbed surface directory, not a real drift.

### 9.11 Residual risks

| Risk | Handling | Status after execution |
|---|---|---|
| `getStore()`'s access-level `try`/`catch` is unreachable in jsdom | Named gap, §9.5 — disclosed, not hidden | **Open, accepted** (§9.13-D5) |
| `!Array.isArray` guard is behaviorally unobservable | Equivalent mutant, proven not assumed | **Open, accepted** (§9.13-D2) — a finding about the module |
| Fixture drifts from the template | A31 + the cited line range | **Closed** — M19 proved A31 catches it |
| Later cases inherit poisoned `hydrating` | Double reset (§9.4) + A32 leak detector | **Closed** — M1/M2 killed, A32 green |
| `restored[]` order treated as incidental | Exact deep equality (§9.6) | **Closed** — M11 killed by 10 cases |
| Assertions written against the constant rather than literals | Explicit rule in §9.6 | **Closed** — M18 killed by A1; every fallback assertion is a literal |
| A mutation silently failing to apply | Match-exactly-once assertion in the harness | **Closed** — it fired on 8 rows (§9.13-D3) |

### 9.12 Execution record

**Authorized and IMPLEMENTED 2026-08-15.** Scope held exactly: one new file,
`static/js/modules/__tests__/workout-controls-persistence.test.js`, 35 cases. **No production,
config, CI, or branch-protection file was modified** — `git status` shows the test file as the only
addition, and the module under test is byte-identical to `origin/main` after the mutation run.

`js-unit` remains **non-required**. Q4 and Q6 were **not** acted on, per instruction.

### 9.13 Evidence-driven deviations and findings

**D1 — the plan conflated two distinct fallback classes. Corrected; the module is right.**

§9.2 predicted that an **absent** stored record makes "all six get defaults", and §9.5 predicted the
same for a **throwing `getItem`**. Reading the implementation while writing the cases showed both are
wrong, because `readRecord()` has **two** failure returns, not one:

| Condition | `readRecord()` | `restoreWorkoutControls()` behavior |
|---|---|---|
| Key absent, empty, or `getItem` throws | `null` | **Early-returns; touches no field.** The rendered values stand. |
| Malformed JSON, JSON `null`, or a JSON array | `{}` | Iterates; **every field falls back** to its pinned default. |

Both are correct product behavior — an absent record must be a no-op, while a *present but unusable*
one must reset. The plan's prose flattened them. **A17 and A34 now assert the untouched behavior**
(by pre-setting the controls to non-defaults first), and A18/A19/A20 assert the defaults behavior the
same way. The distinction is load-bearing: it is exactly what **M12** kills, and M12 would have
passed against the plan's original wording.

This is a defect in the plan, found by implementation. No production code changed.

**D2 — M13 is an equivalent mutant, not a test weakness.**

Dropping `!Array.isArray(parsed)` from `readRecord()` red **nothing**. Verified rather than assumed:
a JSON array is `typeof 'object'` and truthy, so the mutant returns the array as the record — but
**every one of the six control ids is `undefined` on a JSON array**, so each field falls back exactly
as it would from `{}`. The two paths are observationally identical through the module's public API.

Measured directly:

```
typeof: object | truthy: true
every control id on a JSON array is undefined => true
```

**A19 was not weakened or strengthened in response.** No test can distinguish these without asserting
something unobservable, and contorting one to chase a 19/19 score would be exactly the false-rigour
§4.5 exists to prevent. The `!Array.isArray` guard is **defensive but behaviorally unreachable**
through this API — recorded as a finding about the production module, not about the tests.

**D3 — the mutation harness had to be CRLF-aware.**

The first full run reported **8 of 19 "NOT APPLIED"**. Cause: the module is CRLF on disk (`autocrlf`)
while the patterns were authored with `\n`, so every multi-line pattern matched zero times. **The
match-exactly-once assertion is what surfaced this** — without it, those 8 rows would have been
silently recorded as "no tests red", producing a fabricated 8-survivor result and a false conclusion
that the suite was weak. Re-run with newline normalisation: 18 killed, 1 equivalent.

Recorded because it generalises: **any mutation harness in this repository must normalise line
endings**, and any harness reporting a surprising number of survivors should be suspected of not
applying its mutations before the tests are blamed.

**D4 — case count landed exactly as planned.** 35 cases, suite 120 → 155. The `+35` delta doubles as
proof that no existing test was modified.

**D5 — the `getStore()` access-level gap stands as disclosed.** §9.5 declared it out of scope
(forcing `window.sessionStorage` *access* to throw needs `window` redefinition). It remains
uncovered, deliberately and on the record. A33/A34/A35 cover the three method-level `try`/`catch`
sites; the access-level one is the fourth and is not covered.

---

## 10. Packet B — scoped plan (`toast.js`) — **GATE 1 APPROVED, EXECUTED AND MERGED 2026-08-22**

> **STATUS: SHIPPED. Gate 1 approved with one owner amendment, built, and MERGED.** The owner's rulings
> are recorded verbatim in **§10.11**, the amendment is folded into §10.3, §10.7-R10 and §10.8 below,
> and the measured execution record is **§10.12**. §10.10's STOP is discharged and annotated in place.
> **Terminal result:** PR
> [#406](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/406) merged as squash
> `987588a612ff29b8f52fc5ad1ea96707316eb66f`; the post-merge CI run `32535888704` on that
> commit passed **18/18**. `static/js/modules/toast.js` is **unchanged** by the packet — blob
> `42863b4664b7f87a2519556b7f9db8af2cb36e64` on both sides. §10.13's merge STOP is
> **DISCHARGED**; every other item it listed stays unauthorized except the **KI-010 / KI-011**
> follow-up, now implemented in its own docs-only packet.
> **Base**: `origin/main` @ **`0984d2e`** — re-verified 2026-08-22. Packet A is merged as `9e5997a`
> (PR #387). Isolated worktree `wt/phase3-packet-b-toast`, rebased onto `0984d2e` at execution time.
> **PLAN v2 — 2026-08-22** (record in §10.9). Written on 2026-08-15 against `origin/main` @
> `81df507`; refreshed against `0984d2e` (13 commits later), then reviewed by the Gate 1 council
> (`architecture-reviewer`, `test-strategist`, `product-risk-reviewer`) and **corrected against
> measurement**. Six substantive defects (D-c…D-h) from the 2026-08-15 text and eleven council
> amendments (C-1…C-11) are folded in; one reviewer prescription was **measured and refuted**
> (§10.9-C-9).
> **Predicted count: 47 cases, delta 155 → 202, mutations N1–N32.**

### 10.1 Ownership and containment

| | |
|---|---|
| **Implementation creates** | `static/js/modules/__tests__/toast.test.js` — one new file, nothing else |
| **This packet may modify** | `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` (this plan + its later execution record) |
| **Must not touch** | `static/js/modules/toast.js` or any production JS; any existing test file; `package.json`; `vitest.config.js`; `.github/workflows/**`; `docs/test_inventory/**`; branch protection |
| **The one qualification to that row** (council C-7) | §10.5 applies **31 mutations to `toast.js` and one to `toast.test.js`** (N30, the fixture row), which reads as a flat contradiction of the row above. It is not, because **the mutations are applied to a COPY**: the harness copies `toast.js` into `artifacts/probe/`, mutates the copy, and points the run at it. **The production file is never written to at all**, and the run ends by asserting `static/js/modules/toast.js` is **byte-identical to `0984d2e`** — that assertion is the check, not the mechanism. This is exactly how the Plan v2 measurements in §10.9 were taken. **In-place mutation with byte-restore is NOT an alternative**: a second, unexercised containment mechanism is a hazard, not an option |
| **Where the mutation harness lives** (council C-7) | The gitignored **`artifacts/`**, never `scripts/`. This is a containment rule with teeth: a file under `scripts/**` pulls in QUALITY_GATE's *Tooling* routing, which would **void §10.6's whole "no `/verify-suite`" argument** and change the packet's gate set. The harness is scratch, is not committed, and is not part of the deliverable |
| **Must not do** | Promote `js-unit`; act on **Q4** or **Q6**; begin **Packet C** or **Packet F** |
| **Environment** | `// @vitest-environment jsdom` on **line 1** (§3.2) — third jsdom file in the suite |
| **Collaborator mocks** | none. `toast.js` imports nothing; its only external dependency is the **global** `bootstrap` (§10.4) |

### 10.2 What was measured before planning

Rows marked **re-verified 2026-08-22** were read out of the file in this worktree during the refresh.
A citation carried forward on trust is exactly the drift class that produced **C-10** below, so the
line numbers here are the ones a reader can open today, not the ones that were true on 2026-08-15.

| Finding | Evidence |
|---|---|
| **KI-004 is a real, documented contract** | [`UI_SCENARIOS_GAP_ANALYSIS.md:99`](../UI_SCENARIOS_GAP_ANALYSIS.md) — single shared `#liveToast`, last-message-wins, mitigated by disposing the prior instance |
| **KI-004 already has deliberate E2E coverage** — **citation CORRECTED, re-verified 2026-08-22** | `e2e/ui-hardening.spec.ts` **324-356**: `only one #liveToast element exists` at **324**, `rapid successive toasts: last message wins` at **329**, `switching toast type clears stale bg-* classes` at **342** (its assertion at **355**). The 2026-08-15 citation `324-338` was **wrong** — it stopped short of 342 and therefore did **not** contain the stale-`bg-*` assertion the row claimed. A fourth test, `toast container uses polite live region`, runs at **358-364**; cite **324-364** if the live-region test is meant to be included |
| **The legacy signature is live production code** — **re-counted 2026-08-22, with the pattern stated beside each number** | `rg "showToast\(.*,\s*true\s*[,)]" static/js` (excluding `__tests__`) returns **22** lines across **8** files: `exercises.js`, `filters.js`, `progression-plan.js`, `workout-plan.js`, `workout-plan-add-exercise.js`, `workout-plan-execution-style.js`, `workout-plan-supersets.js`, `workout-plan-table.js`. Of those, **8** have the collision-capable `showToast(error.message \|\| '<fallback>', true)` shape — `workout-plan.js:114,160,193`, `workout-plan-supersets.js:200,227`, `workout-plan-table.js:688`, `filters.js:251`, `workout-plan-execution-style.js:215` — and that **8** is the only number §10.7-R3 relies on. `exercises.js:36` and `:68` are interpolated (`` `Unable to …: ${error.message}` ``): always prefixed, so they **cannot** collide with a type word. (A previously stated total of "15" was not reproducible by any grep and is withdrawn.) |
| **The action-button CLICK path has ZERO coverage at any tier** — **measured 2026-08-22** | `e2e/volume-splitter.spec.ts:340` asserts the action toast's **text** (`/Plan #\d+ saved\.\s*Activate for Plan tab/i`) and then moves on — it **never clicks the button**. So `toast.js:73-83` — the listener, `getInstance` → `hide` → `onClick`, and the `try`/`catch` — is executed by **no unit test, no E2E spec, and no visual test today**. **B36/B37/B38 would be its only coverage anywhere** |
| **The `action` option is live, not dead** — **re-verified 2026-08-22** | Still exactly **one** caller repo-wide: a grep for `action:\s*\{` under `static/js` returns a single hit. The block has **moved** — it is now [`volume-splitter.js:301-306`](../../static/js/modules/volume-splitter.js) (`action: {` at 301, `label` 302, `ariaLabel` 303, `onClick` 304, `}` 305, `});` 306), **not** the `302-305` this row cited on 2026-08-15. `volume-splitter.js` is the one JS file that changed between `81df507` and `0984d2e` (+19/−5). **Testing the option therefore does not entrench dead code** — a live caller exists, so B30–B38 pin behavior the product actually uses |
| **Toast markup** — **re-verified 2026-08-22** | [`templates/base.html`](../../templates/base.html) **lines 236-263**, unchanged: container `<div>` opens at 236, `#liveToast` at 243, `#toast-body` at 251, close button 256-260 |
| **`#liveToast` carries no `bg-*` class at rest** — **re-verified 2026-08-22** | `base.html:244` — the class list is exactly `toast align-items-center text-white border-0`. Load-bearing for B42 |
| **`#toast-body` is NESTED INSIDE `#liveToast`** — **re-verified 2026-08-22** | `base.html`: `#liveToast` opens at 243 and closes at 262; `#toast-body` sits at 251, inside it. This is why B40 cannot be produced by deleting the `#liveToast` element (§10.3, D-d) |
| **`toast.js` is untouched since the plan was written** | 111 lines, byte-identical between `81df507` and `0984d2e`. Every line number cited in §10.3–§10.5 was read from this worktree on 2026-08-22 |

**Consequence for scope.** Because `ui-hardening.spec.ts` already owns last-message-wins at the
integration level, Packet B deliberately targets what E2E **cannot** reach: legacy dispatch, the
request-ID gate, default copy, string coercion, action-button wiring, and **call ordering**. It does
not re-litigate KI-004's end-to-end behavior.

### 10.3 Case matrix — B1–B45 (**47 cases**)

> **Count history, stated once: 42 (2026-08-15) → 44 (refresh) → 47 (Plan v2).**
> The refresh split **B15 → B15a / B15b** and added **B43**. Plan v2 adds three more, each because a
> **measurement** showed an existing case could not distinguish a real defect: **B25b** (partial
> `classList.remove`), **B44** (falsy-but-defined message), and **B45** (the type-word collision).
> Every other ID keeps its original number so §10.5 stays readable.
> **Rows = predicted cases = 47.** See §10.9 C-2, C-3, C-4.

**Two authoring rules that apply to every row below.**

1. **No negative assertion stands alone** (council C-5). A bare `not.toContain` / `not.toHaveBeen…`
   passes just as happily when `showToast` threw on line one and rendered nothing at all. **Every
   negative assertion must be paired with a positive one proving the call ran to completion.**
   Concretely, and non-negotiably: **B20–B23** assert the **exact full body text** with `toBe`, never
   `not.toContain('Request ID')`; **B32** asserts the button is non-null *before* asserting the
   attribute is absent; **B33/B34** additionally assert the message `<span>` rendered **and** that
   `errorSpy` was not called; **B10/B11/B29** assert `FakeToast.constructed` has length **1**, so a
   `{delay:…}` assertion cannot pass against zero constructions. This rule exists because the repo has
   already shipped one such vacuous assertion — `ui-hardening.spec.ts:355` asserts
   `not.toContain('bg-info')` on a toast that was never `bg-info` (§10.9 C-2).
2. **Every legacy-signature case asserts the rendered BODY TEXT, not just the class** (council C-1,
   measured). See the callout under the legacy block — this is the amendment all three reviewers
   found, and the plan's stated N1 kill set was wrong without it.

| ID | Case | Asserts |
|---|---|---|
| **Modern signatures** | | |
| B1 | `showToast('success','Saved')` | `bg-success` added; body text `Saved` |
| B2 | `showToast('error','Nope')` | `bg-danger` |
| B3 | `showToast('warning','Careful')` | `bg-warning` |
| B4 | `showToast('info','FYI')` | `bg-info` |
| **Legacy signature** — **every row asserts BODY TEXT, not only the class** | | |
| B5 | `showToast('Bare message')` | Legacy → `bg-success`, **and body text `'Bare message'`** — not the word "success" |
| B6 | `showToast('Broke', true)` | → `error`, `bg-danger`, **and body text `'Broke'`** |
| B7 | `showToast('Fine', false)` | → `success`, **and body text `'Fine'`** (survives N1 on class alone — §10.5) |
| B8 | `showToast('Msg', 'not-a-boolean')` | Non-boolean 2nd arg → `legacyIsError` false → `success`, **and body text `'Msg'`** (survives N1 on class alone — §10.5) |
| B9 | `showToast('Broke', true, {requestId:'R1'})` | Object 3rd arg survives; `bg-danger`, **and body text exactly `'Broke (Request ID: R1)'`** |
| **Numeric options, both signatures** | | |
| B10 | `showToast('success','m',5000)` | Constructor receives `{delay: 5000}` **and `FakeToast.constructed.length === 1`** |
| B11 | `showToast('m', false, 5000)` | Legacy numeric duration → `{delay: 5000}`, `constructed.length === 1`, **and body text `'m'`** (survives N1 on class *and* delay alone — §10.5) |
| **Default copy, split by type** | | |
| B12 | `showToast('error', null)` | `An unexpected error occurred.` |
| B13 | `showToast('error', undefined)` | Same |
| B14 | `showToast('success', null)` | `Action completed successfully.` |
| B15a | `showToast('warning', null)` | Non-error copy — `Action completed successfully.` |
| B15b | `showToast('info', null)` | Non-error copy — one **case per type**, so a regression in one type cannot hide behind its sibling's assertion inside a shared row |
| **Coercion** — these pin a **coercion contract, not desired output** (§10.9 C-10) | | |
| B16 | `showToast('success', 42)` | Body text `'42'` |
| B17 | `showToast('success', {a:1})` | Body text `'[object Object]'`. **Commented in the file as: this pins what `String()` does today, not what the product should show.** A future improvement that renders objects sensibly is *expected* to red B17, and that red means "update the case", not "revert the improvement" |
| B18 | `showToast('success','<b>x</b>')` | Rendered via `textContent`: text is the literal string and `toastBody.querySelector('b')` is **null** |
| **Request-ID gate** — every row asserts the **exact full body text** with `toBe` (rule 1) | | |
| B19 | `error` + `requestId:'R1'` | Body is exactly `'Nope (Request ID: R1)'` — suffix present |
| B20 | `success` + `requestId:'R1'` | Body is exactly the message, with **no** suffix — asserted positively, never as `not.toContain` |
| B21 | `warning` + `requestId:'R1'` | Body is exactly the message |
| B22 | `info` + `requestId:'R1'` | Body is exactly the message |
| B23 | `error` + `requestId:''` | Falsy id → body is exactly the message. It is **N10's predicted kill**, but N10 reds four other cases too, so nothing isolates B23 (§10.5) |
| **Class handling** | | |
| B24 | Element pre-set to `bg-danger`, then `showToast('success',…)` | `bg-danger` removed, `bg-success` present |
| B25 | Element pre-set to **all four** `bg-*`, then `showToast('info',…)` | Only `bg-info` remains |
| **B25b** | Element pre-set to **all four** `bg-*`, then **`showToast('success',…)`** | **Only `bg-success` remains.** Added because measurement showed **both B24 and B25 are blind to a partial `classList.remove`**: with `"bg-info"` deleted from the remove list at `:88`, B25 reads `["bg-info"]` on both pristine and mutant, and B24 is unaffected. This arrangement reads `["bg-success"]` pristine and `["bg-info","bg-success"]` mutant — **it is the only case in the matrix that distinguishes N31** (§10.9 C-2) |
| B26 | Two successive calls | `toastBody.innerHTML=''` clears: exactly **one** `<span>`, showing the second message |
| **Dispose / construct / show** | | |
| B27 | An existing instance is present | Ordered log is `getInstance → dispose → construct → show` |
| B28 | No existing instance | **No** `dispose`; still `construct → show` |
| B29 | Default options | Constructor called with `(toastElement, {delay: 3000})`, **`FakeToast.constructed.length === 1`**, then `show()` once |
| **Action button construction** — **PLACEMENT-NEUTRAL by owner amendment** (§10.11 ruling 4). The button is appended into `#toast-body` at `:84` today, but that parent is the implementation detail implicated in the measured wipe defect, so B30–B35 locate and assert **through `#liveToast`** and pin the button's **type, label, aria-label, guard and coercion** behavior while staying silent about its direct parent (§10.7-R10) | | |
| B30 | Valid action | Exactly one action `<button>` exists **within `#liveToast`**; `type === 'button'`; `textContent === label` |
| B31 | `action.ariaLabel` provided | `aria-label` attribute set to it. **This is an a11y assertion and is deliberately in scope** (§10.7-R7) |
| B32 | No `ariaLabel` | Button is **non-null first**, then `hasAttribute('aria-label')` is **false**. Guards a real bug: **N21 (set `aria-label` unconditionally) produces the literal accessible name `"undefined"`** — a screen reader announcing "undefined" is exactly what B32 prevents |
| B33 | `action.onClick` not a function | **No** action button anywhere in `#liveToast` — **and** the message `<span>` did render **and** `errorSpy` was not called, so the row cannot pass on a `showToast` that died early |
| B34 | `action.label` falsy (`''`) | **No** action button anywhere in `#liveToast` — same positive pairing as B33 |
| B35 | `action.label` is `5` | `textContent === '5'`. Like B16/B17, this pins **String coercion**, not desired output |
| **Action click behavior** (log reset after `showToast()` — see §10.4) | | |
| B36 | Click with an existing instance | After `calls` is reset and `currentInstance` is set, the click's ordered log is **`['getInstance','hide','onClick']`** — the handler at `toast.js:74` does its **own** `getInstance`, so that entry is part of the contract, not noise. `hide` **before** `onClick` is the assertion this row exists for |
| B37 | Click with **no** existing instance — `currentInstance` left `null` for the whole case | Click log is **`['getInstance','onClick']`** — `onClick` still runs and **no** `hide` is recorded. Its sibling B36 sets `currentInstance` *between* `showToast()` and the click, which the fake honours because `getInstance` reads the variable at call time; the two rows together prove the click branch is driven by what `getInstance` returns **at click time**, not by what `showToast()` saw (§10.4) |
| B38 | `onClick` throws | **The kill is `expect(errorSpy).toHaveBeenCalledWith('Toast action handler failed:', expect.any(Error))`** (`toast.js:81`). **Measured against the N23 shape: the spy's call count is 0**, so this assertion genuinely fails on the mutant. A `not.toThrow()` around the click is **vacuous in jsdom** and must not be presented as the assertion — see §10.7-R8, and note that the reviewer-proposed `window` error guard was measured and **refuted** (§10.9 C-9) |
| **Missing-DOM early returns** (produced by removing an **`id` attribute**, never a node — §10.9 D-d) | | |
| B39 | `#toast-body` unresolvable: `document.getElementById('toast-body').removeAttribute('id')` | **A LEADING `expect(() => showToast(…)).not.toThrow()`** — load-bearing here, unlike in B38 — then `console.error('Error: toast-body not found in the DOM!')`; **Bootstrap never touched**. The leading guard matters because **N25 kills this row by TypeError**, not by the console assertion (§10.5): with the `return` at `:38` deleted, `:60` dereferences a null `toastBody` and throws, which would make the later assertions unreachable rather than failing informatively |
| B40 | `#liveToast` unresolvable, body still resolvable: `document.getElementById('liveToast').removeAttribute('id')` | Same **leading `not.toThrow()`** (N26 throws at `:88` on a null `toastElement`), then `console.error('Error: liveToast not found in the DOM!')`; **Bootstrap never touched**. **The node must stay in the DOM** — `#toast-body` is nested inside `#liveToast` (`base.html` 243/251/262), so deleting the element would delete the body too and drive the test down B39's path instead |
| B41 | **Both** unresolvable: `removeAttribute('id')` on **both** elements | Only the **toast-body** error fires — proves lookup order (`toast.js:35` before `:41`). Asserted as `errorSpy.mock.calls` deep-equalling a single-entry array, not as "the toast-body message appears somewhere" |
| **Anti-vacuity** | | |
| B42 | Fixture self-check | `#liveToast` and `#toast-body` exist, and `#liveToast` carries **no** `bg-*` class at rest — so B1–B4 cannot pass on a pre-existing class |
| **API sharp edge** (§10.7-R3) | | |
| B43 | `showToast('success')` — **one** argument | Body text is `Action completed successfully.`, **not** `success`. `message` has no default parameter, so an omitted second argument *is* `undefined`; this is behaviourally identical to `showToast('success', undefined)` and is pinned **because R3 names it as the edge a reader gets wrong**, not because it reaches a distinct branch. B14 does **not** cover it: B14 passes an explicit `null` |
| **B44** | **`showToast('success', '')`** — a falsy-but-**defined** message | **Body is exactly `''`.** Added because measurement showed the `message !== undefined && message !== null` guard at `:49` is **perturbed by no mutation and reached by no existing case**: mutating `:49` to `if (message)` leaves B1, B12, B14, B16 and B17 all indistinguishable, and **only** an empty (or `0`) message tells the two apart. Without B44 the module could silently regress to replacing a deliberate empty message with boilerplate copy. Kills **N32** |
| **B45** | **`showToast('error', true)`** — a legacy two-argument call whose message **is a type word** | Body is exactly `'true'` and the class is `bg-danger`. **Commented in the file as a PINNED SHARP EDGE, NOT DESIRED BEHAVIOR.** `'error'` passes `validTypes.has()` at `:15`, so the legacy branch never runs, `message` becomes the boolean `true`, and the caller's actual message is **swallowed**. See §10.7-R3 for the full measured table and why it is not reachable today |

**Predicted count: 47 cases** — B1–B14 (14) + B15a, B15b (2) + B16–B25 (10) + B25b (1) +
B26–B43 (18) + B44, B45 (2) = **47**, and the table above has exactly 47 non-heading rows. The row
count and the predicted case count are deliberately the same number so `+47` in §10.6 is an
arithmetic check, not an estimate.

**One case was considered and declined.** A `showToast('success', 0)` companion to B44 also
distinguishes N32 (pristine `'0'`, mutant the default copy). It is **not** added: B44 already kills
N32, and a second case of the same class would grow the count without growing the kill set.

### 10.4 The first-in-suite global `bootstrap` fake

No test in this repository fakes the `bootstrap` global today (§1.2). This is the one genuinely new
mechanic in step 12, and Packet C will reuse it for `bootstrap.Modal`.

**Installation and teardown**

```js
let calls;               // the single ordered log, shared by every fake object
let currentInstance;     // what Toast.getInstance() returns; null by default.
                         // Read at CALL time, so a test may change it between
                         // showToast() returning and the action button click.
let errorSpy;            // vi.spyOn(console, 'error'); the handle B38/B39/B40/B41 assert on

beforeEach(() => {
    calls = [];
    currentInstance = null;
    FakeToast.constructed = [];      // static, so it MUST be reset per case or it
                                     // accumulates across the whole file
    errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    document.body.innerHTML = TOAST_FIXTURE;
    globalThis.bootstrap = { Toast: FakeToast };
});

afterEach(() => {
    delete globalThis.bootstrap;     // never leak the global into another file
    vi.restoreAllMocks();            // undoes the console.error spy
    document.body.innerHTML = '';
});
```

**How cross-object ordering is recorded without importing real Bootstrap.** Every fake method pushes
a label onto **one shared `calls` array** rather than onto per-object counters. Because the *old*
instance's `dispose()` and the *new* instance's `constructor`/`show()` append to the same array, the
relative order of events **across two different objects** is directly readable:

```js
class FakeToast {
    constructor(element, options) {
        calls.push('construct');
        this.element = element;
        this.options = options;
        FakeToast.constructed.push(this);
    }
    show()    { calls.push('show'); }
    hide()    { calls.push('hide'); }
    dispose() { calls.push('dispose'); }
}
FakeToast.getInstance = (el) => { calls.push('getInstance'); return currentInstance; };

// An "already present" instance is a PLAIN OBJECT, never `new FakeToast(...)`:
// constructing one would push 'construct' onto the log during arrange, before
// the module has done anything, and corrupt B27's and B36's expected arrays.
const makeInstance = () => ({
    show()    { calls.push('show'); },
    hide()    { calls.push('hide'); },
    dispose() { calls.push('dispose'); },
});
```

**Ordered-log expectations, stated exactly.** `calls` is a *cumulative* log for the whole test, not a
per-phase one. The 2026-08-15 draft under-specified this and stated B36's expected value wrongly
(§10.9 D-c). The rule and the four expected arrays:

| Phase | Arrangement | Expected `calls` |
|---|---|---|
| **B27** — `showToast()` with an existing instance | `currentInstance = makeInstance()` **before** the call | `['getInstance','dispose','construct','show']` |
| **B28/B29** — `showToast()` with no existing instance | `currentInstance` left `null` | `['getInstance','construct','show']` — no `dispose` |
| **B36** — the click, existing instance | `showToast(…, {action})` → `currentInstance = makeInstance()` → **`calls.length = 0`** → `button.click()` | `['getInstance','hide','onClick']` |
| **B37** — the click, no instance | `showToast(…, {action})` → leave `currentInstance = null` → **`calls.length = 0`** → `button.click()` | `['getInstance','onClick']` |

Three consequences that the earlier draft missed and that the implementer must not re-derive by
guesswork:

1. **The log must be reset between `showToast()` and the click.** By the time `showToast()` returns,
   `calls` already holds its own `getInstance` / `construct` / `show` entries (`toast.js:103`, `:108`,
   `:109`). Clearing it (`calls.length = 0`) isolates the click.
2. **`getInstance` is the click's own first entry.** The handler installed at `toast.js:73` calls
   `bootstrap.Toast.getInstance(toastElement)` itself at `:74`, so `['hide','onClick']` — the value
   the 2026-08-15 draft named — is **not** achievable. `['getInstance','hide','onClick']` is.
3. **`currentInstance` is read at call time, so the test controls what the *click* sees**, independent
   of what `showToast()` saw. **B36 sets the instance *after* `showToast()` returns, and the reason is
   fidelity, not bookkeeping.** (The earlier "so `dispose` stays out of the log" rationale was
   vestigial — `calls.length = 0` already excludes it.) Setting it *before* the call means the module
   **disposes** that instance at `:105`; a disposed instance is not what production's `getInstance`
   returns when the user clicks the button moments later. Arranging it afterward models the real
   sequence: `showToast()` constructs a live instance, and the click then finds *that* one.

B27's single deep-equality check pins *both* "dispose happened" and "it happened before construction".
B36/B37 have their `onClick` push its own `'onClick'` label onto the same array. **This is the only
technique in the plan that could not be expressed as independent per-method spies**, and it is why a
hand-written class is used rather than `vi.fn()` objects alone.

Only the surface `toast.js` actually calls is faked: `Toast.getInstance`, the `Toast` constructor,
`show`, `hide`, `dispose`. Nothing else. **Real Bootstrap is never imported** — that would make these
tests a Bootstrap-upgrade problem, which the visual and E2E tiers already own (§3.3).

**§4.1 is discharged for this module, explicitly** (council C-8). The determinism rules require every
packet to say how a module's top-level mutable state is reset, and Packet A needed a double
`endHydration()` for exactly that reason. **`toast.js` has none.** Every binding in the file is
function-local, including `validTypes` at `:12`, which is re-created on each call; there is no
module-level `let`, no cache, and no counter. **So no `vi.resetModules()` and no per-test re-import is
needed, and adding one would be cargo cult.** The only cross-test state this file creates is state the
*test* installs — `globalThis.bootstrap`, `calls`, `currentInstance`, `FakeToast.constructed`, the
`console.error` spy and `document.body` — and all six are reset in `beforeEach`/`afterEach` above.
Stating this closes §4.1 for Packet B rather than leaving a reader to wonder whether it was forgotten.

**Packet C reuses the PATTERN, not the code** (council C-8). §2.2 said this fake would be "reused" for
`bootstrap.Modal`; verified against the code, that overstates it. `exercises.js:47,49` touches only
`Modal.getInstance(modal)` and `bsModal.hide()` — **no constructor, no `show`, no `dispose`**. §3.3
forbids faking more surface than the module under test calls, so Packet C must build its **own**,
smaller `Modal` fake. **No shared helper file is authorised by Packet B or Packet C**, and creating
one would be a second new file that neither packet's ownership row permits.

**Console spies.** `console.error` is spied with
`errorSpy = vi.spyOn(console,'error').mockImplementation(()=>{})` so B38/B39/B40/B41 can assert on it
without polluting output; `vi.restoreAllMocks()` in `afterEach` restores it. The spy handle is kept in
a variable because **B38's only non-vacuous assertion runs through it** (§10.7-R8).

**Fixture**, copied from [`templates/base.html`](../../templates/base.html) **lines 236-263**
(re-verified 2026-08-22), with that citation in a comment. Only the parts `toast.js` reads are kept —
the outer container, `#liveToast` with its **exact** at-rest class list, `#toast-body`, and the close
button:

```html
<div class="position-fixed toast-container">
  <div id="liveToast" class="toast align-items-center text-white border-0"
       role="alert" aria-live="assertive" aria-atomic="true">
    <div class="d-flex">
      <div class="toast-body" id="toast-body"></div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto"
              data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  </div>
</div>
```

The **absence** of any `bg-*` class here is load-bearing and is pinned by **B42**: if a future edit
added one, B1–B4 would pass without the module ever adding a class.

**What the fixture deliberately omits, and why the omission is safe.** The fixture is a *reduction* of
`base.html:236-263`, not a copy, and the reduction must be stated so a later reader does not treat it
as drift. Omitted on purpose:

| Omitted from the fixture | Where it lives in `base.html` | Why omitting it is safe |
|---|---|---|
| `data-testid="toast-container"` | 239 | Read only by Playwright locators, never by `toast.js` |
| `aria-live="polite"`, `aria-atomic="true"` on the **container** | 237-238 | `toast.js` never reads or writes them; a11y is owned by `e2e/accessibility.spec.ts` and the axe register (§10.7-R7) |
| `style="bottom: 20px; right: 20px; z-index: 9999; pointer-events: none;"` on the container | 241 | Presentational; jsdom does no layout, so it could not be asserted meaningfully anyway |
| `style="pointer-events: auto;"` on `#liveToast` | 248 | Same — and it is not part of the class list B42 pins |

**Kept because the module reads them**: `#liveToast`'s `id` (`toast.js:41`) and its exact at-rest
`class` value (`:88`, `:99`), and `#toast-body`'s `id` (`:35`) and its position **inside** `#liveToast`
(the nesting B40 depends on). `role`/`aria-live`/`aria-atomic` on `#liveToast` are kept for fidelity to
the source markup, not because the module reads them.

**The missing-DOM cases mutate the fixture by attribute, not by node.** B39/B40/B41 call
`removeAttribute('id')` on the relevant element inside the test body, after the shared `beforeEach`.
Deleting the `#liveToast` **element** would take `#toast-body` with it — they are nested — so B40
would silently exercise B39's path and pass for the wrong reason (§10.9 D-d).

**The action-button locator is placement-neutral** (owner amendment, §10.11 ruling 4). B30–B35 find the
button by searching **`#liveToast`**, not `#toast-body`:

```js
const actionButtons = () =>
    Array.from(liveToast().querySelectorAll('button:not([data-bs-dismiss="toast"])'));
```

Two details are load-bearing. **The search root is `#liveToast`**, so a future fix that appends the
button to `#liveToast` — the obvious way to make it survive `:60`'s `innerHTML` clear — leaves every
one of B30–B35 **green**, which is the entire point of the amendment. And **the fixture's own close
button is excluded by its `data-bs-dismiss` attribute, not by the action button's `className`**:
`:68`'s seven-class Bootstrap string is deliberately pinned by no case at any tier (§10.5), and
matching on it in the locator would smuggle that coupling back in through the back door.

**No mutation depends on the parent, re-derived rather than assumed.** N18–N24 are the seven rows that
touch the action path, and each was re-checked against the neutral locator: N18/N19 flip the guard so
the button's **existence** changes, N20 removes `type`, N21 makes `aria-label` unconditional, and
N22/N23/N24 alter the click handler — none reads or moves `toastBody.appendChild` at `:84`. The
expectations are unchanged, and execution confirmed all seven (§10.12).

### 10.5 Mutation matrix — prediction (**N1–N32**)

> Plan v2 adds **N31** (partial `classList.remove`) and **N32** (the `:49` message guard) to the
> refresh's N1–N30, so the matrix is **N1–N32 everywhere**.

Harness requirements, carried forward from §9.13-D3 and extended:

- **Judge every row by the runner's PROCESS EXIT CODE, never by parsing the failed-test count.**
  **Measured 2026-08-22**: under the N23 shape, Vitest reports the uncaught listener error as an
  **unhandled error** and **exits 1 while printing `Tests N passed` and zero failures**. A harness
  that greps for `failed` would record that row as a **survivor** and hand back a fabricated test
  weakness. This is the §9.13-D3 failure class — a harness bug masquerading as a test result — on a
  new axis, and it is the single most likely way this matrix produces a wrong conclusion.
- **`toast.js` is CRLF on disk — measured, not assumed.** §9.13-D3's normalisation rule is **live for
  this file**, not theoretical. **Eleven rows span more than one line** and are the ones EOL
  normalisation can silently void — **N4, N5, N14, N15, N21, N22, N23, N24, N25, N26, N27** (see the
  `Line` column below). Verify those **first**; a `NOT APPLIED` among them is the expected symptom of
  skipped normalisation. **N1 is not one of them** — its canonical form is a single-token replacement
  on one line, so a `NOT APPLIED` there means something else entirely.
- **Normalise line endings** — convert `\n` in every pattern to the target file's dominant EOL. This
  is not optional; it silently voided 8 of 19 rows on the first Packet A run.
- **Mutate a COPY under `artifacts/probe/`** (§10.1) — the production file is never written to.
- **Require every mutation to match exactly once**, and report `NOT APPLIED` otherwise. A mutation
  that fails to apply must never be recorded as "no tests red".
- **Run the full Vitest suite per mutation**, not just `toast.test.js`.
- **Discard the probe directory afterward** and assert `static/js/modules/toast.js` is byte-identical
  to `0984d2e`.
- **Distinguish equivalent mutants from genuine survivors** — a survivor is only equivalent once a
  *reason* is demonstrated (as M13 was). An unexplained survivor is a test weakness and must be fixed.
- **Several patterns are NOT unique without surrounding context**, and under the match-exactly-once
  rule an under-anchored pattern reports `NOT APPLIED` rather than mutating. Anchors verified by
  reading `toast.js` on 2026-08-22:

  | Pattern | Occurrences | Required anchor |
  |---|---:|---|
  | `return;` | **2** (`:38`, `:44`) | Match with the preceding `console.error(...)` line. **N25 and N26 differ only by that line** — this is the pair most likely to mis-apply |
  | `console.error(` | **3** (`:37`, `:43`, `:81`) | Anchor on the message literal; all three differ |
  | `bootstrap.Toast.getInstance(toastElement)` | **2** (`:74`, `:103`) | Anchor on the assignment: `const instance =` (click handler) vs `const existingToast =` (dispose path). N14/N15/N24 all depend on this |
  | `typeof options === 'number'` | **2** (`:18`, `:28`) | N4 must include the `} else if (` prefix; `:18` is the legacy ternary |
  | `type === 'error'` | **2** (`:52`, `:56`) | N8 anchors on the ternary at `:52`; N9 anchors on the whole `if (requestId && type === 'error') {` at `:56` |
  | `.textContent` | **2** (`:62`, `:69`) | N29 anchors on `messageSpan.textContent`; `:69` is `button.textContent` |
  | **N1's condition** `!validTypes.has(type)` | **1** (`:15`) | **Unambiguous as a single token** — one more reason to prefer the condition-replacement form below over a block delete |

> **N1 was defective in both form and prediction. All three council reviewers found the form defect
> independently, and measurement settled the prediction.** Both fixes are folded in below; the
> original wording is kept here because the failure generalises.
>
> **(a) The delete form does not parse.** MEASURED: removing `:15-27` leaves a dangling `} else if (`
> and the file stops being JavaScript — Vite reports *"Failed to parse source for import analysis …
> invalid JS syntax"*. **A mutation that cannot be loaded is not a survivor; it is not a mutation.**
> **Canonical form: replace the condition `!validTypes.has(type)` → `false` at `:15`**, which keeps
> the `else if` attached and is a clean, uniquely-matching single-token edit.
>
> **(b) Under that form, the plan's kill set was WRONG.** MEASURED, pristine vs mutant:
>
> | Case | pristine | N1 mutant | did the plan's stated assertion distinguish them? |
> |---|---|---|---|
> | B5 body | `"Bare message"` | `"Action completed successfully."` | **yes** |
> | B6 class | `bg-danger` | `bg-success` | **yes** |
> | B7 class / body | `bg-success` / `"Fine"` | `bg-success` / `"false"` | class **NO**, body yes |
> | B8 class / body | `bg-success` / `"Msg"` | `bg-success` / `"not-a-boolean"` | class **NO**, body yes |
> | B9 body | `"Broke (Request ID: R1)"` | `"true"` | **yes** |
> | B11 delay / class / body | `{delay:5000}` / `bg-success` / `"m"` | `{delay:5000}` / `bg-success` / `"false"` | delay **NO**, class **NO**, body yes |
>
> **As originally specified, B7, B8 and B11 all SURVIVE N1** — the true kill set was `{B5, B6, B9}`.
>
> **(c) Two reviewers disagreed and the measurement resolved it.**
> The `architecture-reviewer` predicted `{B5,B6,B9,B11}`; the `test-strategist` predicted
> `{B5,B6,B9}`. **The test-strategist is right.** Under N1 the `else if (typeof options === 'number')`
> at `:28` becomes **live**, so the *mutant* produces `{delay: 5000}` for B11 too. Inferring a "before"
> from reading the diff is what produced the wrong answer; measuring every arm's before is what
> produced the right one.
>
> **(d) The fix, and why it belongs here anyway.** **Every legacy case (B5–B9, B11) now asserts the
> rendered body text** (§10.3), and with that the original prediction becomes true. The reason is
> structural, not incidental: the `|| 'bg-success'` fallback at `:98` means **a broken legacy branch
> emits the same class a correct one does**, so a class-only assertion cannot tell "legacy dispatch
> ran" from "the fallback happened to agree". Legacy dispatch is this packet's headline claim (§10.2),
> so the body-text assertion would be required even if N1 did not exist.

Every row was re-checked against `toast.js` on 2026-08-22 and names text actually in the file. The
`Line` column is the harness author's map; multi-line entries are the EOL-normalisation risk set.

| # | Line | Deliberate break | Predicted to red |
|---|---|---|---|
| **N1** | `:15` | **Condition replacement: `!validTypes.has(type)` → `false`** (**not** a block delete — that does not parse) | B5, B6, B7, B8, B9, B11 — **true only because every one of them now asserts body text**; with the 2026-08-15 assertions it was `{B5, B6, B9}` |
| N2 | `:17` | `legacyIsError` → always `false` | B6, B9 |
| N3 | `:21` | Legacy `type = legacyIsError ? 'success' : 'error'` (swap) | B6, B7, B8, B9 — **also B5 and B11; see the over-broad note below, corrected from execution** |
| N4 | `:28-31` | Delete the modern `else if (typeof options === 'number')` branch | B10 |
| N5 | `:25-27` | Delete `if (legacyDuration !== undefined) options.duration = …` | B11 |
| N6 | `:33` | Default `duration = 3000` → `5000` | B29 |
| N7 | `:52` | Error default copy → the success copy | B12, B13 |
| N8 | `:52` | Default-copy gate `type === 'error'` → `type !== 'error'` | B12, B13, B14, B15a, B15b, B43 |
| N9 | `:56` | Request-ID gate: drop `&& type === 'error'` | B20, B21, B22 |
| N10 | `:56` | Request-ID gate: drop the `requestId &&` truthiness check | **Predicted kill B23**; additionally reds **B6, B12, B13, B45** — every `error` case that asserts body text picks up a ` (Request ID: null)` suffix. **B9 canNOT red** (its `requestId` is truthy, so mutant and pristine are byte-identical) and **B2 cannot** (it asserts class only) |
| N11 | `:88` | Delete the **whole** `classList.remove(...)` call | B24, B25, B25b |
| **N31** | `:88` | **Partial removal: delete only `"bg-info"` from the remove list** | **B25b only.** MEASURED: B24 and B25 as specified are **both blind** — under B25 (all four pre-set → `showToast('info')`) pristine and mutant both read `["bg-info"]`. The E2E tier cannot catch it either: `ui-hardening.spec.ts:342` goes success→error and its `not.toContain('bg-info')` at `:355` is **vacuous, because `bg-info` was never set** |
| N12 | `:93` | `typeToClass.error` → `'bg-warning'` | B2 — additionally reds **B6, B9, B45**, every case asserting `bg-danger` |
| N13 | `:98` | `typeToClass[type] \|\| 'bg-success'` → `typeToClass[type]` | **(none) — predicted EQUIVALENT, see §10.7-R1** |
| N14 | `:104-106` | Delete `if (existingToast) existingToast.dispose();` | B27 |
| N15 | `:104-108` | Move the dispose **after** `new bootstrap.Toast(...)` | B27 |
| N16 | `:109` | Delete `toast.show()` | B27, B28, B29 |
| N17 | `:108` | Constructor options `{delay: duration}` → `{}` | B10, B11, B29 |
| N18 | `:65` | Action guard: drop `&& action.label` | B34 |
| N19 | `:65` | Action guard: drop `typeof action.onClick === 'function'` | B33 |
| N20 | `:67` | Delete `button.type = 'button'` | B30 |
| N21 | `:70-72` | Set `aria-label` unconditionally | B32 |
| N22 | `:74-82` | Click handler: call `action.onClick()` **before** `instance.hide()` | B36 |
| N23 | `:78-82` | Click handler: remove the `try`/`catch` | B38 |
| N24 | `:75-77` | Click handler: delete the `if (instance) instance.hide();` | B36 |
| N25 | `:37-38` | Delete the `return` after the toast-body `console.error` | **B39 — by TypeError, not by its console assertion.** Execution continues to `:60` and dereferences a **null `toastBody`**. B39's **leading** `not.toThrow()` is what turns that into a clean, informative red. **Also reds B41; see the over-broad note below, corrected from execution** |
| N26 | `:43-44` | Delete the `return` after the liveToast `console.error` | **B40 — also by TypeError**: `:88` dereferences a null `toastElement`. Same leading `not.toThrow()` |
| N27 | `:35-45` | Look up `#liveToast` before `#toast-body` | B41 |
| N28 | `:60` | Delete `toastBody.innerHTML = '';` | B26 |
| N29 | `:62` | `messageSpan.textContent` → `.innerHTML` | B18 |
| **N30** | *fixture* | **Add `bg-success` to `#liveToast`'s at-rest class list** | **B42** — the anti-vacuity check, mirroring M19. The only row that touches **`toast.test.js`** rather than the module |
| **N32** | `:49` | **`message !== undefined && message !== null` → `if (message)`** | **B44 only.** MEASURED: B1 (`'Saved'`), B16 (`42`), B17 (`{a:1}`), B12 and B14 (`null`) are **all** indistinguishable; only a falsy-but-defined message separates them. In production this would silently replace a deliberate empty or zero message with boilerplate copy |

**Over-broad predictions.** Per §9.8, over-detection is not a defect — but an **unpredicted** red sends
the next session investigating a phantom, so the known ones are in the rows above (N10, N12) plus:
**N3** also reds **B5**, because the swap makes a bare-message legacy call render as an error.

**Two of those lists were still incomplete, and EXECUTION found it — not review** (2026-08-22, §10.12).
The harness compares each row's predicted red-ID set against the runner's JSON report, which is why
these surfaced at all; a harness that recorded only "went red / stayed green" would have absorbed both
silently.

- **N3 also reds B11**, not just B5. `showToast('m', false, 5000)` has `legacyIsError === false`, so the
  swapped ternary sends it to `'error'`, and B11's `bg-success` assertion goes red. The 2026-08-15 list
  was derived before B11 carried a class assertion at all, and the Plan v2 sweep re-derived every row
  against the five **new** cases (B15a/B15b/B25b/B44/B45) — but **not** against the assertions that
  Plan v2 had just *added to existing* cases. That is the gap: **a sweep scoped to new rows misses the
  rows whose assertions changed underneath it.**
- **N25 also reds B41.** With the `return` at `:38` gone, B41 — which removes **both** ids — falls
  through the toast-body guard into the `#liveToast` guard and logs a **second** `console.error`, so
  B41's single-entry `errorSpy.mock.calls` deep-equality fails. This is the lookup-order case doing
  exactly what it was written to do; it was simply not listed.

Neither is a test weakness and neither changes a verdict: all 32 rows were killed or survived exactly
as their **status** predicted. Both lists are corrected in the rows above.

**The kill sets were re-derived against the Plan v2 cases, not just patched where a reviewer pointed.**
B15a, B15b, B25b, B44 and B45 were added after the matrix was first written, so every one of the 32
rows was re-checked against all five. Two rows moved — **N10** and **N12**, both gaining **B45** —
and the sweep confirmed no other row does: N1–N5 touch the legacy path only and all five new cases
use a **valid** type; N6/N17 move the delay, which none of them asserts; N18–N26 need an `action`,
which none of them passes.

**N13 is a deliberate equivalence probe**, and the argument is derived
from the code rather than asserted. On every path out of the signature-normalising block, `type` is
one of exactly four values: either `validTypes.has(type)` was already true at `:15`, or the legacy
branch reassigned it at `:21` to `'error'` or `'success'`. `validTypes` (`:12`) and the `typeToClass`
keys (`:91-96`) are the **same four strings**, so `typeToClass[type]` at `:98` can never be
`undefined` and the `|| 'bg-success'` fallback is unreachable through the module's public API. If N13
survives *and* that reasoning holds under measurement, it is recorded as an equivalent mutant exactly
as M13 was (§9.13-D2) — **not** chased with a contorted test.

**A second declared equivalence, beside N13** (council C-11). `:19`'s defensive **copy**
`legacyOptions = { ...options }` versus a plain alias is **unobservable through the public API**. The
only write to `legacyOptions` is `:26`, and it executes only when `legacyDuration !== undefined`, which
requires `typeof options === 'number'` at `:18` — in which case `:19`'s own `typeof options ===
'object'` test is false and `legacyOptions` is **already a fresh `{}`**. So the caller's object can
never be the thing written to. Declared as an equivalence **in advance**, in the same idiom as N13,
rather than discovered as a mystery survivor.

**Two named gaps, recorded and deliberately not closed:**

- **`showToast('success','msg', null)` throws a `TypeError`** at the `:33` destructure — parameter
  defaults fire only on `undefined`, never on `null`. **No caller does this today.** It is recorded as
  a named gap: **not** a case (it would pin a crash as a contract) and **not** a production fix (out of
  scope). If a caller ever starts passing `null` options, this note is the pointer.
- **`:68`'s `button.className`** — the seven-class Bootstrap string — is pinned by **no case at any
  tier**, and deliberately so. Asserting it would couple the unit suite to presentational styling that
  the visual tier owns, and it would red on any theme change. Recorded as a decision, not a blank.

**B43 is not independently killed.** Under N8 it reds together with B14, and no mutation in N1–N32
distinguishes `showToast('success')` from `showToast('success', null)` — because JavaScript does not
distinguish them either (§10.3). B43 pins the *documented* answer to §10.7-R3; its value is
documentation of intent, not additional mutation coverage.

### 10.6 Gates and predicted deltas

**Baseline — re-measured 2026-08-22 on current `origin/main` `0984d2e`**, in this worktree:

```
Test Files  11 passed (11)
     Tests  155 passed (155)
```

This is the **same figure** the 2026-08-15 draft recorded against `81df507`, but it is now a *current*
measurement rather than one inherited across 13 commits. **The evidence that it should be unchanged is
not the coincidence of the two numbers** — it is that no JS test file moved between the two bases.
`git diff --stat 81df507 origin/main` over `static/js`, `package.json`, `vitest.config.js`,
`.github/workflows/ci.yml` and `docs/test_inventory` shows exactly three things: a **comment-only**
`ci.yml` edit, a **regenerated** `docs/test_inventory/`, and `static/js/modules/volume-splitter.js`
(+19/−5). **No test file, no config, and no change to `toast.js`.**

**Authoring constraint — the file must resolve to exactly 47 *reported* cases, and the count rule
itself needed fixing.** Two separate measurements bear on this.

*First*, reported cases are **not** `it(` call sites in this suite. Measured 2026-08-22: a
line-anchored grep for `it(` / `test(` / `it.each(` across the 11 existing files finds **145 call
sites**, while the runner reports **155 cases**; the gap is the two `it.each` blocks at
`static/js/modules/__tests__/workout-plan-seams.test.js:132` and
`static/js/modules/__tests__/user-profile-data.test.js:14`, which expand.

*Second — and this voids the rule as previously written* — **the parenthesised total includes skipped
and todo cases.** MEASURED 2026-08-22: a file containing one `.todo` and one `.skip` reports
`Tests 9 passed | 1 skipped | 1 todo (11)`. So **"202 or an existing test moved" is not a proof**: a
file with 45 real cases plus two `.todo` stubs satisfies it while asserting nothing. That is precisely
the "a required check whose contents can be emptied without detection" failure §2.5 exists to prevent,
reappearing at the case-count level.

**The count gate is therefore four pinned checks, not one number** (council C-6):

| # | Check | Why it is not redundant |
|---|---|---|
| i | A **focused** run of `toast.test.js` reports **47 passed / 47 total in 1 file** | Isolates the new file from the rest of the suite |
| ii | `npm run test:js` reports **12 files / 202** | Proves no existing file moved |
| iii | **Zero** skipped, **zero** todo and **zero** filtered in **both** runs | The measurement above: the total alone cannot see a `.skip` or `.todo` |
| iv | A grep asserting the new file contains **no** `.only`, `.skip`, `.todo` — and no `it.each` unless its expansion is counted | Catches the defect at source rather than in a number |

(§10.9 D-f and C-6.)

| Gate | Command | Expectation |
|---|---|---|
| Baseline | `npm run test:js` | **11 files / 155 cases** — measured 2026-08-22 on `0984d2e` |
| With Packet B | `npm run test:js` | **12 files / 202 cases** — exactly **+47** (§10.3), **and** all four checks (i)–(iv) above. Any other delta means either an existing test moved (a defect) or the new file did not resolve to 47 reported cases (also a defect) |
| Coverage | `npm run test:js -- --coverage` | Record measured movement. The figures **statements 6.7 %, branches 9.2 %, functions 7.1 %, lines 6.4 %** are the **PR-#387 head-run measurement from 2026-08-15** (`js-unit` job of run `31889768992`) and are carried here as history, **not** as a current number — they were taken before `0984d2e` and are **re-measured at execution time**, not assumed. `toast.js` is 111 lines at **0 % executed** today, so a rise is expected; the number is **recorded, never gated** (D1 is signed as non-blocking measurement) |
| Mutation | §10.5, full suite per row, against a copy | Every row reds its predicted cases; survivors explained or fixed |
| Inventory | `.venv/Scripts/python.exe scripts/generate_test_inventory.py --check` | **"Test inventory is up to date"**, exit 0 — derived below, not assumed. **Do not regenerate** — Packet F has not landed, so Vitest nodes are still unpinned (§9.10) |
| CI | all required contexts green | `js-unit` stays **non-required** |

**Why `Test Inventory Drift` stays green — the derivation, not the assertion.**
[`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) pins **five** surfaces. Taken one at a time
against the single file this packet adds, `static/js/modules/__tests__/toast.test.js`:

| Pinned surface | Trip condition (QUALITY_GATE) | Packet B |
|---|---|---|
| Per-file pytest node counts | add/remove/rename/move under `tests/**` | **No** — nothing under `tests/**` |
| Per-spec Playwright counts | add/remove/rename in `e2e/**/*.spec.ts` | **No** |
| `waitForTimeout` lines per file | add/delete a hard wait in `e2e/**/*.ts` | **No** |
| Required functional spec set | the `e2e-functional-shard` spec list in `ci.yml`, or a rename of that job | **No** — `.github/workflows/**` is out of scope (§10.1) |
| Parametrized configuration surface | **adding or deleting** a file under `.claude/commands/`, `.claude/agents/`, `.claude/rules/`, or **`docs/ai_workflow/`** | **No** — the new file is under `static/js/`, and this plan lives under **`docs/testing_phase3/`**, which is *not* `docs/ai_workflow/`. Editing an existing file in place does not trip it either |

Confirmed from the other direction as well: a grep of `docs/test_inventory/` for `vitest`, `test:js`
or `static/js` returns **zero** matches on `0984d2e` — the artifact contains no Vitest nodes at all,
because Packet F has not started. Adding a Vitest file therefore cannot move a pinned count.

**Two more required checks, confirmed non-applicable by reading the config.** Not a council item —
folded in from measurement taken 2026-08-22:

| Required check | Why Packet B cannot trip it |
|---|---|
| `Type Check (tsc blocking + pyright measure-only)` | **`tsconfig.json` includes only `["e2e/**/*.ts", "playwright.config.ts"]`**, with **no `allowJs` and no `checkJs`**. A new `.js` file under `static/js` is **outside the TypeScript program entirely**. The pyright half is repo-wide but triggers on `.py`; Packet B adds none |
| `Code Linting` | The job installs `flake8` **and** `pylint` (`ci.yml:101`) but **only ever invokes `flake8`** — three commands at `:110`, `:112`, `:123`; `pylint` is never run. Either way both are **Python** linters and **`package.json` defines no JS lint script**, so no JS file can fail this job |

**Why no Playwright or `/verify-suite` gate is required — a CONSCIOUS OVERRIDE, not a derivation**
(council **C-3**). The 2026-08-15 text called this a derivation, and that was **too strong**. Read
literally, `QUALITY_GATE.md` **line 107** says *"Run the union. If the union is empty, run
`/verify-suite`"*, and the plan-stage carve-out at **lines 16-20** exempts only *"a docs-only change
whose row explicitly requires no tests"* — which Packet B is not, because the file it adds lives under
`static/js/**` and matches the *Frontend (JS)* row. That row's feature map yields **no** spec for
`toast`, so the union is **empty**, so a literal reading **escalates to `/verify-suite`**. The override
is taken on the two grounds below, exactly as Packet A did in §9.9, and it is **void the moment the
diff grows beyond the one test file**.

1. **The change adds no production behavior.** The *Frontend (JS)* row asks for "matching Chromium
   specs + manual smoke if interactive", and the feature map has no `toast` row — because a toast is
   routed by the production change that *provokes* it, never by a unit test of the emitter. There is
   nothing for a spec to exercise that it was not exercising yesterday, and nothing interactive to
   smoke. The targeted gate is the runner that executes the file: `npm run test:js`.
2. **It is enforced regardless.** `ci.yml` has **no `paths:` or `paths-ignore:` filter at all** —
   **re-verified by grep on `0984d2e`, 2026-08-22: zero matches**, and the only `ci.yml` change since
   `81df507` is a comment. So every PR runs every job, including the full Chromium matrix. Packet A is
   the precedent: it merged with **18/18 green**, the complete E2E suite included, without a local
   Playwright run. The override therefore costs no coverage, only local minutes.

### 10.7 Risks and behavioral ambiguities

| # | Risk / ambiguity | Disposition |
|---|---|---|
| **R1** | `\|\| 'bg-success'` is unreachable once `type` is normalised | Predicted **equivalent mutant** (N13). Will be recorded as a finding about the module, not chased. Mirrors §9.13-D2 |
| **R2** | The global `bootstrap` could leak between test files and silently satisfy another file's expectations | `delete globalThis.bootstrap` in `afterEach`; no other test file references it today, and the full suite is run per mutation so a leak would surface |
| **R4** | B26 asserts `innerHTML=''` clears prior content; if a future action button is appended the span count changes | B26 asserts exactly one `<span>` after two **action-free** calls, isolating the clearing behavior |
| **R5** | Ordered-log assertions are stricter than behavior strictly requires — a refactor preserving semantics but reordering `getInstance` could red B27 | Accepted deliberately: the dispose-before-construct order **is** the KI-004 mitigation, so pinning it is the point. Documented so a future red is read as "confirm intent", not "flaky test" |
| **R6** | Packet A's harness bug (CRLF) could recur | §10.5 makes normalisation and match-exactly-once explicit harness requirements |
| **R9** | The ordered log is cumulative, so a click-phase assertion written without resetting `calls` would compare against `showToast()`'s own entries and be quietly rewritten to whatever the implementation produced | §10.4 fixes the four expected arrays in a table and mandates `calls.length = 0` between `showToast()` and the click. The expected values there are **predictions**, not measurements; if execution produces different arrays, the discrepancy is investigated before any expectation is edited |

The remaining four need more than a table cell.

#### R3 — the type-word collision (MEASURED on the pristine module)

The 2026-08-15 text framed this as "`showToast('success')` renders default copy". The real edge is
worse: **a legacy two-argument call whose message happens to equal a type word swallows the message
entirely**, because `validTypes.has()` at `:15` sees a valid type and the legacy branch never runs.

| Call | Body rendered | Class |
|---|---|---|
| `showToast('Broke', true)` | `"Broke"` | `bg-danger` *(correct)* |
| `showToast('error', true)` | **`"true"`** | `bg-danger` |
| `showToast('warning', true)` | **`"true"`** | `bg-warning` |
| `showToast('success', true)` | **`"true"`** | `bg-success` |
| `showToast('warning')` | **`"Action completed successfully."`** | `bg-warning` — a yellow warning toast whose copy says the action **succeeded** |

**Pinned, not fixed.** **B43** covers the one-argument form; **B45** pins `showToast('error', true)` →
body `'true'` + `bg-danger`. Both are commented in the test file as **pinned sharp edges, not desired
behavior**. **Reachability, measured**: **8** live call sites have the collision-capable
`showToast(error.message || '<fallback>', true)` shape (§10.2), so this is **one server-copy change
away** from firing — but it is **not reachable today**, because `utils/errors.py` never sets a message
to one of the four type words. Fixing it is production code and out of scope for a test-only packet;

§10.9 routes it to the owner as a candidate KI row, and it was **accepted there as KI-010**
(§10.11 ruling 2) — registered in [`UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md)
by the separate follow-up packet, still **Open** and still unfixed.

> **ANNOTATION 2026-08-22 (KI follow-up) — the conclusion holds, the attribution was imprecise.**
> `utils/errors.py` does not *set* the message at all: `error_response(code, message, …)` and
> `success_response(message=…)` forward whatever their caller supplies (`:36-37`, `:94-97`), and
> `fetch-wrapper.js:61` passes that envelope message through to `error.message`. The guarantee
> therefore belongs to the **call sites**, not to `errors.py`. Re-measured 2026-08-22: **0** of
> **234** `error_response()` / `success_response()` call sites across `routes/`, `utils/` and
> `app.py` pass a bare type word, so "not reachable today" is still correct — but a future auditor
> must re-check the call sites, not this one module. The same phrasing survives in the comment at
> `toast.test.js:563`, which this docs-only packet may not edit. KI-010 in
> [`UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md) carries the corrected wording.

#### R7 — what a11y scope actually is (this row was inaccurate as written)

"a11y assertions are out of scope here" was **false**: `toast.js:70-72` sets `aria-label` on the
action button, and **B31/B32 are a11y assertions**. What is out of scope is **live-region and role
semantics** — `role="alert"`, `aria-live`, `aria-atomic` — which `toast.js` never touches and which
are owned by `ui-hardening.spec.ts:358-364` (container `aria-live` is `polite`),
`accessibility.spec.ts:695-704` (live regions exist), and the axe register. **The action button's
`aria-label` IS in scope**, pinned by B31/B32, and concretely load-bearing: **N21 yields the literal
accessible name `"undefined"`**, which a screen reader would announce. B32 is what stops that
shipping.

#### R8 — `not.toThrow()` is vacuous in jsdom and cannot carry N23

An exception thrown inside a DOM event listener does **not** propagate out of `dispatchEvent` /
`.click()` — jsdom routes it to the window error handler. So `expect(() => button.click())
.not.toThrow()` passes **with or without** the `try`/`catch` at `toast.js:78-82`; writing it as B38's
headline assertion would be a false green of exactly the class §4.5 exists to prevent.

**B38's load-bearing assertion — and the only thing that kills N23 — is**
`expect(errorSpy).toHaveBeenCalledWith('Toast action handler failed:', expect.any(Error))`
(`toast.js:81`). Measured against the N23 shape the spy's call count is **0**, so it correctly fails
on the mutant. A `not.toThrow()` line may be kept as documentation of intent **only if** a comment
says it is non-load-bearing. This risk also produced §10.5's exit-code harness rule; the reviewer
prescription that was measured and refuted is recorded once, at §10.9-C-9.

#### R10 — the action button is destroyed by any subsequent toast

`:60` clears `toastBody.innerHTML` and `:84` appends the button **into `toastBody`**, so the *next*
`showToast()` from anywhere silently removes it. **Reachable inside its own only caller**:
`volume-splitter.js:299-306` raises the action toast with `duration: 6000`, line **308** immediately
calls `loadVolumeHistory()`, and that function's `.catch` at **439** emits `showToast('error', …)`.
On a slow or failing history fetch the user's "Activate for Plan tab" button vanishes mid-toast.

**Pinned, not fixed** — production behavior, out of scope. Packet B **characterizes** this defect and
does **not** mitigate it: no production line changes, and nothing in the test file makes the button
survive a body clear.

**The 2026-08-15 disposition was reversed by the owner at Gate 1** (§10.11 ruling 4). It read: *"B30–B35
deliberately assert the button's placement inside `#toast-body`, so a future relocation is expected to
red them."* The owner declined that: **the exact parent is the implementation detail implicated in this
very defect, so pinning it would pre-commit the suite to the shape the fix must change.** B30–B35 now
locate the button through **`#liveToast`** and enforce type, label, `aria-label`, guard and coercion
while remaining neutral about the direct parent (§10.4). A relocation fix must leave all six **green**;
if it reds one, that is a real regression in the button's contract, not a bookkeeping update.

Routed to the owner in §10.9 as the second candidate KI row, and **accepted there as KI-011** —
a separate follow-up, not this packet (§10.11 ruling 2).

### 10.8 Gate 1 checklist — **CLOSED 2026-08-22**

Ticked against the owner's approval (§10.11) and the measured execution record (§10.12). The one row
the owner **changed** is marked; every other row is accepted as written.

- [x] Scope: **one** new file, `static/js/modules/__tests__/toast.test.js`
- [x] Case matrix **B1–B45 (47 cases)** accepted — §10.3. Count approved unchanged (§10.11 ruling 1)
- [x] The two authoring rules — negative-assertion pairing, legacy body text — §10.3 rules 1–2
- [x] The global `bootstrap` fake, the `makeInstance()` helper, and the four expected arrays — §10.4.
      All four arrays were **predictions**; all four were confirmed by execution unchanged (§10.12)
- [x] No `vi.resetModules()` (no module-level state); Packet C reuses the **pattern**, not the fake — §10.4
- [x] Containment: mutations run against a **copy** under `artifacts/probe/`, harness never under
      `scripts/**` — §10.1
- [x] Fixture from `base.html:236-263` with its stated omissions; B39/B40/B41 remove an **`id`**, not a
      node — §10.4
- [x] **AMENDED BY THE OWNER** — B30–B35 do **not** pin the action button's exact parent. They locate
      and assert through **`#liveToast`** and enforce type, label, `aria-label`, guard and coercion
      while staying neutral about the direct parent — §10.4, §10.7-R10, §10.11 ruling 4. Count stays 47
- [x] Mutation matrix **N1–N32**, including **N1's canonical condition-replacement form**, N31, N32,
      the two declared equivalences, and the cases with no isolating killer (B23, B43) — §10.5
- [x] Harness rules — §10.5 (exit-code judging, CRLF normalisation and its eleven multi-line rows,
      match-exactly-once, the **six ambiguous patterns plus one deliberately unambiguous** anchor,
      full suite per row). Two further rules were **added from execution**: a collected-case-count
      check per row, and an oid-based identity check (§10.12)
- [x] Gate set — §10.6 (the four count checks, coverage recorded not gated, inventory `--check`
      without regeneration, CI green, `js-unit` still non-required)
- [x] The no-`/verify-suite` position accepted as a **conscious override**, void if the diff grows — §10.6
- [x] Predicted delta: **155 → 202**, 11 → 12 files — §10.6. **Measured: exactly that**
- [x] Still out of scope: production JS (**including both sharp edges, §10.7-R3 and R10**), Q4, Q6,
      Packet C, Packet F, promotion
- [x] **The six owner rulings at the end of §10.9 are answered** — recorded verbatim in §10.11

### 10.9 Plan v2 record — refresh + Gate 1 council (2026-08-22)

**Part 1 — the 2026-08-22 refresh against `0984d2e`.**

**What was re-measured on current `origin/main` `0984d2e`, in the `wt/phase3-packet-b-toast` worktree:**

| Re-measured | Result |
|---|---|
| `npm run test:js` baseline | **11 files / 155 cases** — unchanged figure, but now a *current* measurement (§10.6) |
| `git diff --stat 81df507 origin/main` over `static/js`, `package.json`, `vitest.config.js`, `ci.yml`, `docs/test_inventory` | Only: `ci.yml` **comment-only**; `docs/test_inventory/` **regenerated**; `volume-splitter.js` **+19/−5** |
| `static/js/modules/toast.js` | **Byte-identical** to the version planned against; **111 lines** |
| `templates/base.html:236-263` | Toast markup unchanged; `#liveToast` at 243 with class list `toast align-items-center text-white border-0` at 244; `#toast-body` at **251, nested inside** `#liveToast` (closes 262) |
| grep `action:\s*\{` under `static/js` | **One** hit — `volume-splitter.js:301` |
| grep `paths:` / `paths-ignore:` in `ci.yml` | **Zero** matches |
| grep `vitest` / `test:js` / `static/js` in `docs/test_inventory/` | **Zero** matches — no Vitest nodes; Packet F has not started |
| `it(` / `test(` / `it.each(` call sites across the 11 existing test files | **145** sites vs **155** reported cases; two `it.each` blocks account for the gap |

**What drifted since 2026-08-15:**

1. The `action:` caller block in `volume-splitter.js` moved **302-305 → 301-306**. This is the only
   substantive JS drift, and it is the reason a citation must be re-read rather than carried forward.
2. `origin/main` advanced 13 commits (`81df507` → `0984d2e`); Packet A is merged as `9e5997a` (#387).
3. Nothing else in this packet's evidence base moved. Packets C and F have not started.

**Disposition of the substantive defects found in the 2026-08-15 text.** Three of the original nine
were cosmetic — a heading typo, a re-anchored base, and a relabelled measurement — and are not
tabulated; the six that recorded a **false claim** are:

| # | Defect | Disposition |
|---|---|---|
| **D-c** | §10.4's ordered-log design was under-specified and **B36's stated expectation was wrong** — `['hide','onClick']` is unreachable because the click handler calls `getInstance` itself at `toast.js:74` | **Fixed** — §10.4 now fixes four expected arrays in a table, mandates `calls.length = 0` between `showToast()` and the click, adds a plain-object `makeInstance()` so arranging an instance cannot push `'construct'`, and states that `currentInstance` is read at call time so the test controls what the click sees. **B36 is predicted `['getInstance','hide','onClick']`, B37 `['getInstance','onClick']` — predictions, not measurements** |
| **D-d** | B40 was described as "`#liveToast` absent", unachievable by deletion because `#toast-body` is nested inside it | **Fixed** — B39/B40/B41 now remove an **`id` attribute**, never a node, with the nesting cited from `base.html` 243/251/262 |
| **D-e** | B38's "click does not throw" is vacuous in jsdom and cannot kill N23 | **Fixed** — the kill is now the `errorSpy` assertion; the reasoning lives at §10.7-R8 |
| **D-f** | "+42 or it is a defect" assumed the file resolves to 42 *reported* cases | **Fixed, then strengthened.** The refresh added a reported-case constraint backed by the measured 145-sites-vs-155-cases gap. Plan v2 found the rule **still unsound** — the total includes skipped and todo (**C-6**) — and replaced it with the four pinned checks (i)–(iv) in §10.6 |
| **D-g** | B15 packed two calls into one row, so rows ≠ predicted cases | **Fixed** — **B15 splits into B15a and B15b** (chosen over merging, because one case per type stops a per-type regression hiding behind a sibling assertion). Every other ID keeps its number |
| **D-h** | §10.7-R3 claimed the one-argument sharp edge was "covered implicitly by B14's shape" — false, B14 is the two-argument `showToast('success', null)` | **Fixed** — added as explicit case **B43**, and §10.5 states honestly that B43 has **no independent mutation kill** because JavaScript does not distinguish an omitted argument from `undefined` |

**Part 2 — the Gate 1 council, and how its claims were settled.**

Three reviewers ran in parallel: `architecture-reviewer`, `test-strategist`, `product-risk-reviewer`.
Every disputed or high-value claim was then **MEASURED** by executing mutant **copies** of `toast.js`
under Vitest + jsdom in the gitignored `artifacts/probe/`, leaving the production file untouched. The
evidence for each accepted amendment lives in the body section named beside it; **C-9 is written out
in full here because it is the one prescription that was refuted, and this is its only home.**

| # | Claim | Disposition |
|---|---|---|
| **C-1** | N1's delete-form does not parse; and as specified, B7/B8/B11 survive it | **ACCEPTED** → §10.5 (canonical form + measured table), §10.3 rule 2 |
| **C-2** | Partial `classList.remove` is uncovered at every tier | **ACCEPTED** → B25b, N31 |
| **C-3** | The `:49` message guard is perturbed by no mutation | **ACCEPTED** → B44, N32 |
| **C-4** | The type-word collision is worse than R3 recorded | **ACCEPTED** as pinning, **refused** as fixing → B45, §10.7-R3 |
| **C-5** | Negative assertions are vacuous unless paired with a positive | **ACCEPTED** → §10.3 rule 1 |
| **C-6** | The count rule is unsound: the total includes skipped and todo | **ACCEPTED** → §10.6 checks (i)–(iv) |
| **C-7** | §10.1 contradicted §10.5; the harness must not live under `scripts/**` | **ACCEPTED** → §10.1, two rows |
| **C-8** | §4.1 was never discharged; the Packet C reuse claim was overstated | **ACCEPTED** → §10.4 |
| **C-9** | `test-strategist`: under N23, jsdom's exception report reaches the same `console.error` the plan spies on, so `toHaveBeenCalled()` would **pass** on the mutant; prescribed a `window.addEventListener('error', e => e.preventDefault())` guard | **REFUTED — MEASURED FALSE, and the fix is NOT adopted.** Under the N23 shape the spy's call count is **0**, so the assertion correctly **fails** on the mutant. The prescribed guard **changed nothing** (count 0 either way) and did **not** remove the unhandled-error channel. Adding it would be cargo cult. **What IS true**, and is folded in instead: a throwing listener is invisible to the `.click()` caller (**R8's vacuity claim is confirmed**), **and Vitest exits 1 while printing `Tests N passed` with zero failures** — which produced the new §10.5 rule to judge every row **by exit code, never by a parsed failure count**. That is the §9.13-D3 harness-bug class on a new axis |
| **C-10** | Citation and framing fixes: `ui-hardening.spec.ts:324-338` misses the stale-`bg-*` test; R7 is inaccurate; B16/B17/B35 pin coercion | **ACCEPTED** → §10.2 (re-cited 324-356), §10.7-R7, §10.3 coercion rows |
| **C-11** | Record the second equivalence and the two named gaps | **ACCEPTED** → §10.5 |

**Corrections applied after the council, from measurement rather than review.** Recorded because two
of them fix numbers the council itself did not question:

- **N10's over-broad list was wrong in both directions.** It named B2 and B9, neither of which can red
  — B9's `requestId` is truthy so mutant and pristine are identical, and B2 asserts class only — and
  it omitted **B45**. Corrected in the N10 row.
- **N12 omitted B45.** Root cause for both: **B45 was added in Plan v2 and the over-broad lists were
  never re-derived against it.** All 32 rows have now been swept against all five Plan v2 cases
  (§10.5); only N10 and N12 moved.
- **The CRLF triage list named N1**, which is now a single-line replacement and cannot be affected by
  EOL normalisation. Replaced with the eleven genuinely multi-line rows.
- **"32 mutations of `toast.js`"** is **31 of the module plus one of the test file** (N30).
- **A "15 legacy call sites" figure was not reproducible.** The measured grep returns **22** lines
  across **8** files; the only number any argument depends on is the **8** collision-capable sites,
  which is verified. §10.2 now states the pattern beside each number.
- **`Code Linting` installs `pylint` but never invokes it** — three `flake8` commands only.

**Predictions introduced or changed by Plan v2** (stated as predictions, and not to be quietly edited
to match whatever execution produces): the case count **47** and suite delta **155 → 202**; N1's kill
set **under the new body-text assertions**; N31 killed by B25b alone; N32 killed by B44 alone; the
four ordered-log arrays in §10.4; N8's kill set including B15a/B15b/B43; the over-broad reds predicted
for N3/N10/N12; and the two declared equivalences (N13, `:19`).

**Scope, and the one edit outside §10.** Plan v2 changed `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md`
§10 and **four lines elsewhere in this same file**, so a reviewer is not surprised by them in the diff:
**§2.6 records that step-12's Vitest inventory/drift packet was relabelled E → F and that the letter
E is "deliberately vacant"**, but §2.5 and §5 still called it **E**. Corrected `E` → `F` at lines
**241, 242, 428, 430**. This is a pre-existing contradiction inside a file this packet already owns,
not something the refresh introduced. **Four lines, not the three initially identified** — line 241's
"Once E lands" sits two lines from 242's "the reason E must come last", and fixing one while leaving
the other would have left the same defect in the same paragraph. Every other `E` in the file belongs
to the relabel record itself and is correct as written. Nothing outside this file was touched.

---

#### Owner must rule at Gate 1 — **ALL SIX ANSWERED 2026-08-22; the rulings are in §10.11**

These are decisions the packet **cannot** take for itself. They are separate from §10.8's checklist,
which records acceptance of work already specified. The six questions are preserved below **as they
were asked**; the answers live in §10.11 so a reader can see both halves.

1. **The final case count and delta** — **47 cases, 155 → 202**. Confirm, or name which of
   B25b / B44 / B45 to drop and accept the coverage loss that follows.
2. **The two sharp edges — do they get a follow-up item?** The type-word collision (§10.7-R3) and the
   action-button wipe (§10.7-R10) are **real, measured, and unfixed**. Both look like candidate **KI
   rows in `docs/UI_SCENARIOS_GAP_ANALYSIS.md`**. **This packet may not edit that file**, so it cannot
   self-resolve — it can only pin the behavior and report it. Related: **`UI_SCENARIOS_GAP_ANALYSIS.md:99`
   cites `templates/base.html:228` for the toast markup, which is now stale** — the toast section
   begins at **236** (line 228 is the fallback-content comment). That correction also needs a home.
3. **Does `toast.test.js` become the sole owner of the two default-copy strings** —
   `'An unexpected error occurred.'` and `'Action completed successfully.'`? If yes, the protocol must
   be explicit: a deliberate copy change **updates the cases in the same PR**, and the red is the
   **intended signal**, not an obstacle. Note that **B15a/B15b pin a default no production call site
   can currently reach** — no caller passes a null message with type `warning` or `info` — which is
   the same "defensive but unreachable" idiom as N13, and is disclosed rather than dressed up.
4. **Is the action button's placement *inside* `#toast-body` accepted as pinned?** B30–B35 assert it.
   If the owner expects the button to be relocated so it survives a body clear, those rows are
   pre-committing to a shape that is about to change.
5. **The rebase and the PR** — *(the git state below was true when the question was asked and is now
   superseded: the branch was rebased to `543311c` on `0984d2e`, a PR was opened, and it has
   since **merged** as `987588a` / #406 — §10.12, §10.13.)*
   `55161b8` is still based on `81df507`, and the branch has **no PR**.
   Rebasing onto `0984d2e` and opening a PR are **both still unauthorized**.
6. **Q4 and Q6** — unchanged and still open (§8). Nothing in Plan v2 touches either.

### 10.10 STOP — **DISCHARGED 2026-08-22**

> **This section is kept as written and annotated, not rewritten.** It was true until the owner signed
> Gate 1; the sentence below records what changed.

**This plan is not authorization to write it.** No test file exists, and **no mutation has been run
against the repository** — the Plan v2 measurements ran against copies under the gitignored
`artifacts/`, leaving `toast.js` byte-identical. The refresh and the council corrected the plan; they
did **not** advance it past Gate 1.
Awaiting explicit owner approval of Gate 1 (§10.8) and rulings on the six questions above.

**DISCHARGED.** The owner approved Gate 1 with one amendment on **2026-08-22** and authorised the
rebase, the implementation and the PR (§10.11). `static/js/modules/__tests__/toast.test.js` now
exists, all 32 mutations have run, and `toast.js` is still identical to `origin/main` — the
containment claim above held through execution and is re-asserted with evidence in §10.12.
**A NEW STOP replaced this one: merge was NOT authorized.** See §10.13 — *and that STOP is
itself **DISCHARGED** as of the 2026-08-22 merge of PR #406 (`987588a`).*

### 10.11 Owner ruling at Gate 1 (2026-08-22) — **APPROVED WITH ONE AMENDMENT**

| # | Question (§10.9) | Ruling |
|---|---|---|
| **1** | The final case count and delta | **APPROVED unchanged** — all 47 cases, B1–B45, preserving the measured **+47** delta. None of B25b / B44 / B45 dropped |
| **2** | Do the two sharp edges get a follow-up item? | **YES — both are real open defects and each gets its OWN KI row**, the type-word collision (§10.7-R3) and the action-button wipe (§10.7-R10). **Packet B may not edit `UI_SCENARIOS_GAP_ANALYSIS.md`**: **KI-010 / KI-011** and the stale **`base.html:228` → `:236`** citation correction are left to a **separate follow-up**. Packet B **only characterizes and pins current behavior** — neither defect may be described anywhere as mitigated or fixed |
| **3** | Does `toast.test.js` become sole owner of the two default-copy strings? | **YES.** `'An unexpected error occurred.'` and `'Action completed successfully.'` are guarded by exact string nowhere else. **Protocol, explicit: a deliberate copy change updates these tests in the SAME PR, and the red is the intended review signal** |
| **4** | Is the action button's placement inside `#toast-body` accepted as pinned? | **NO — AMENDED.** Do **not** pin the exact parent: it is the implementation detail implicated in the measured wipe defect. B30–B35 must require the button to exist **within `#liveToast`** and enforce its **type, label, `aria-label`, guard and coercion** behavior while **remaining neutral about its direct parent** — locating and asserting through `#liveToast`. **Case count stays 47**; affected mutation expectations re-derived, though none was expected to depend on the parent |
| **5** | The rebase and the PR | **AUTHORIZED** — preserve the uncommitted Plan v2 work; fetch and rebase onto latest `origin/main`; `--force-with-lease` if a history-rewriting push is required; **stop and report** if relevant toast/config/test drift has occurred; implement, verify, commit, push, open the PR. **Merge is NOT authorized** |
| **6** | Q4 and Q6 | **UNTOUCHED** — still open (§8) |

> **ANNOTATION 2026-08-22 (later).** Ruling 5's closing *"Merge is NOT authorized"* is the ruling as
> given at Gate 1 and is preserved verbatim. It was **discharged by a separate owner confirmation**
> naming PR #406; the PR merged as `987588a` with 18/18 green (§10.13). Rulings 1–4 and 6 are
> unchanged.

**Where ruling 4 landed in this document**, so a reader is not left to hunt: the §10.3 *Action button
construction* header and rows **B30, B33, B34**; the new placement-neutral-locator block in **§10.4**;
the rewritten disposition in **§10.7-R10**; and the amended checklist row in **§10.8**. The 2026-08-15
position is quoted in R10 rather than deleted, because the reversal — *"do not pin the shape the fix
must change"* — is the transferable lesson, and a silently rewritten row would carry none of it.

**Execution constraints carried into §10.12**, recorded so the gate list is auditable against the
instruction rather than against memory: no production changes including `toast.js`; deliverable scope
is `toast.test.js` plus this planning/execution record; run the focused 47-case gate, the full JS
suite, coverage, all N1–N32 against copies under `artifacts/probe` **judged by process exit code**, and
inventory `--check`; confirm `toast.js` unchanged; the local `/verify-suite` override holds **only**
while the diff stays within the approved scope; do not begin Packet C or F and do not promote
`js-unit`.

### 10.12 Execution record — 2026-08-22

**Rebase (ruling 5).** The uncommitted Plan v2 edit to this file was stashed by path, the branch was
rebased `81df507` → **`0984d2e`**, and the edit was restored. The plan commit `55161b8` became
**`543311c`**; the rebase was clean and no conflict was resolved.

**Drift check before implementing — the "stop and report" condition was NOT met.** Every claim
§10.2/§10.6 rests on was re-verified against the new base:

| Surface | Result |
|---|---|
| `static/js/modules/toast.js` | **Unchanged** between `81df507` and `0984d2e` (empty diff), still 111 lines |
| `.github/workflows/ci.yml` | Changed, and **read in full: comment-only** — two prose blocks, one about the win32 byte gate, one about `_packaged-windows.yml`. No `run:`, `if:`, `uses:` or job change |
| `package.json`, `vitest.config.js` | **Untouched** |
| Every existing test file | **Untouched** |
| `docs/test_inventory/` | Regenerated (no Vitest nodes, as §10.6 derived) |
| `static/js/modules/volume-splitter.js` | +19/−5, the drift §10.9 already recorded |

**Line endings.** `toast.js` is **CRLF** on disk (111 CRLF, 0 bare LF) as §10.5 assumed. `core.autocrlf`
is `true` and there is **no `.gitattributes`**, and all three existing jsdom test files are CRLF on
disk, so **`toast.test.js` was normalised to CRLF before committing** — an LF file here would check out
as CRLF and show as phantom-modified on the next status.

**Gate results.**

| Gate | Expected | Measured |
|---|---|---|
| (i) Focused `toast.test.js` | 47 passed / 47 total, 1 file | **47 passed (47), 1 file** ✔ |
| (ii) `npm run test:js` | 12 files / 202 | **12 files / 202 passed** ✔ |
| (iii) Zero skipped / todo / filtered in **both** runs | — | **Zero** in both; the runner printed a bare `passed` total with no `skipped` or `todo` segment ✔ |
| (iv) No `.only` / `.skip` / `.todo` / `it.each` in the new file | — | **Zero matches**; **47 `it(` call sites = 47 reported cases**, so the file needs no expansion accounting ✔ |
| Inventory | `Test inventory is up to date`, exit 0, **no regeneration** | **Exactly that, exit 0** ✔ |
| `toast.js` unchanged | identical to `origin/main` | **oid `42863b46` on both sides** ✔ |

**Coverage — recorded, never gated** (D1 is signed as non-blocking measurement). Both arms were
measured **in this worktree on this base**, so the movement is a real difference and not a figure
carried from PR #387:

| | Baseline (`0984d2e`, no Packet B) | With Packet B | Movement |
|---|---|---|---|
| Statements | 6.66 % (497/7453) | **7.4 % (552/7453)** | +0.74 pp, +55 |
| Branches | 9.23 % (429/4644) | **10.22 % (475/4644)** | +0.99 pp, +46 |
| Functions | 7.11 % (79/1110) | **7.29 % (81/1110)** | +0.18 pp, +2 |
| Lines | 6.37 % (443/6946) | **7.16 % (498/6946)** | +0.79 pp, +55 |

The baseline arm reproduces the **6.7 / 9.2 / 7.1 / 6.4** figures §10.6 carried as history from run
`31889768992`, which is a corroboration rather than an assumption.

**`toast.js` goes 0 % → 100 % statements, lines and functions, and 97.87 % branches (46 of 47).** The
**one** uncovered branch is independent corroboration of the **N13 equivalence**: §10.5 argued from the
code that `|| 'bg-success'` at `:98` is unreachable through the public API, and the coverage tool
independently reports exactly one branch that no test can reach. Two different instruments, same
answer, neither told about the other.

**Mutation matrix — 32 rows, all against copies under the gitignored `artifacts/probe/`.**

**32 / 32 behaved as predicted**: 31 killed, **N13 survived as declared equivalent**, **0 unexplained
survivors, 0 unexpected kills, 0 `NOT APPLIED`**. Every row was judged by the runner's **process exit
code**. The `predicted vs measured` red-ID comparison matched on **30 of 32** rows; the two that
differed are the over-broad-list corrections folded into §10.5 (**N3 also reds B11**, **N25 also reds
B41**) — both over-detection, neither a weakness, neither changing a verdict.

**Three harness defects were found and fixed, and all three are the §9.13-D3 class — a harness bug
wearing a test result's clothes.** They are recorded because each would have produced a *confident
wrong answer*, and only the first was anticipated by the plan:

1. **`npx.cmd` cannot be `spawnSync`-ed without a shell on Windows** — `EINVAL`, `status === null`. The
   control arm caught it instantly because it checks for exit **0**, not merely "not 1": a harness that
   treated non-zero-or-null as "red" would have declared every row killed and reported a perfect
   matrix from **32 runs that never started**. Fixed by spawning `node node_modules/vitest/vitest.mjs`
   directly — no shell between the harness and the exit code it judges by.
2. **N30 silently ran the wrong suite.** The mutated test file is included by absolute path, and an
   absolute Windows path is **not a valid glob**, so Vitest matched nothing: the row collected **155**
   cases (the 11 original files, with the real `toast.test.js` excluded and the mutant never added) and
   reported a clean **SURVIVOR** — a fabricated weakness in B42, the anti-vacuity case. **A green run of
   the wrong suite is indistinguishable from a survivor if you only look at the exit code.** Fixed
   twice over: the include path is now POSIX-separated and relative to `root`, **and** every row must
   now report **202 collected cases** or it is recorded as a distinct, loud `BAD RUN` — never as a
   survivor. This is the one rule §10.5 did not have and now needs.
3. **The byte-identity assertion failed on a file nobody touched.** `git show
   origin/main:static/js/modules/toast.js` returns the **normalised (LF)** blob while the working file
   is **CRLF**, so a raw byte compare reported `identical: NO` — the containment check crying wolf,
   which is corrosive in exactly the way a silent one is. Fixed by comparing git's own object ids
   (`rev-parse` vs `hash-object`), which applies to the working file the same normalisation a commit
   would. **On any `core.autocrlf` checkout, "byte-identical" must be asserted through git's
   normalisation, not around it.**

**The four §10.4 ordered-log arrays were predictions and are now measurements**, unchanged: B27
`['getInstance','dispose','construct','show']`, B28/B29 `['getInstance','construct','show']`, B36
`['getInstance','hide','onClick']`, B37 `['getInstance','onClick']`. §10.7-R9 required that a
discrepancy be investigated before any expectation was edited; **none arose, and no expectation was
edited.**

**Deviations from Plan v2.** One, and it is the owner's amendment, not a drift: **B30–B35 no longer pin
`#toast-body` as the action button's parent** (ruling 4). Case count, delta, mutation matrix and every
other expectation are as Plan v2 specified. The three harness fixes above changed the *measuring
instrument*, not the plan's claims.

**Edits outside §10, listed so nothing in the diff is a surprise.** Plan v2 held itself to this
discipline (§10.9, last paragraph) and the execution commit keeps it. Four places outside §10 changed,
every one of them because **this commit falsified prose that was true before it** — the failure class
the working rules call out by name:

| Where | Why it had to move |
|---|---|
| The document's opening **Scope** block | Said the file covers "Packet A as implemented"; Packet B is now implemented too, and the merge STOP belongs where a reader starts |
| **§2.2** heading | Read *"(AUTHORIZED — second)"*, which a reader would take as *not yet built* |
| **§8's Gate 0 STOP** | Said *"as of this commit nothing has been implemented: no test file …"*. That was **already falsified by Packet A** in 2026-08-15 and this commit falsifies it twice over. **Annotated, not rewritten** — the live annotation carries the truth, the original paragraph keeps the sequence legible, and the "explicitly still unauthorized" list underneath it is confirmed still accurate item by item |
| **§10.9's owner-question 5** | Made a bare git-state claim (*"still based on `81df507` … no PR"*) that the rebase falsified. Marked superseded in place; the question text is preserved, because §10.11 answers it and an edited question makes the answer unreadable |

Nothing outside this file was touched.

**Not done, deliberately:** no production JS changed; `UI_SCENARIOS_GAP_ANALYSIS.md` untouched (KI-010,
KI-011 and the `base.html:228` → `:236` correction are a separate follow-up — *which has since been
implemented; see the §10.13 annotation*); no inventory
regeneration; **Q4 and Q6 untouched**; Packets C and F not begun; `js-unit` still **non-required**; no
`/verify-suite` run locally, on the §10.6 conscious override, which holds because the diff is exactly
the two files its scope permits.

### 10.13 STOP — merge — **DISCHARGED 2026-08-22**

> **This section is kept as written and annotated, not rewritten.** The paragraph below was true from
> the moment the PR opened until the owner's merge confirmation; the annotation after it records what
> changed and what did not.

The PR is open and CI-verified. **Merging it is not authorized.** Per the standing PR protocol, a merge
requires a separate, explicit owner confirmation that names the PR and says "merge"; green CI is not
that confirmation, and neither is a selection among options.

Also still not authorized, and not blocked on the same confirmation — each needs its own: **Packet C**,
**Packet F**, promotion of `js-unit` (**Q4**/**D2**), **Q6**, and the **KI-010 / KI-011** follow-up in
`UI_SCENARIOS_GAP_ANALYSIS.md`.

**DISCHARGED 2026-08-22.** The merge went ahead under owner direction, which is what the
paragraph above reserved it for. PR [#406](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/406) is
**MERGED**, squash `987588a612ff29b8f52fc5ad1ea96707316eb66f` (`2026-08-21T23:10:23Z`), and
the **post-merge** CI run `32535888704` on that commit passed **18/18**. Packet B's terminal
shape is what §10.12 measured: **47 new cases**, full Vitest suite **12 files / 202 cases**,
and `static/js/modules/toast.js` **unchanged** at blob `42863b46`.

**Of the five items the paragraph above listed, exactly one moved.** The **KI-010 / KI-011**
follow-up in [`UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md) was authorized
and **implemented as its own docs-only packet**: **KI-010** (the type-word collision,
§10.7-R3) and **KI-011** (the action-button wipe, §10.7-R10) are now registered rows, **both
`Open`, neither mitigated nor fixed**, and KI-004's stale `templates/base.html:228` citation
is corrected to `:236`. That packet changed **documentation only** — no production, test,
config, workflow or inventory file — so it neither fixes nor mitigates either defect, and
B45 and B30–B35 are untouched.

**Still not authorized and still unstarted, each needing its own confirmation:** **Packet C**,
**Packet F**, promotion of `js-unit` (**Q4** / **D2**), and **Q6**.

> ⚠️ **ANNOTATION 2026-08-22 — the line above and the "exactly one moved" count are falsified for
> Packet C, and are annotated rather than rewritten.** **A second of the five items has now moved:
> Packet C's Gate 1 was APPROVED** (§11.16) and the packet is **written, measured, committed, pushed and
> open as a ready-for-review PR** (§11.17). It is **NOT merged** — that is a separate confirmation
> (§11.18). **Packet F, Q4/D2 promotion and Q6 are still unauthorized and still unstarted**, exactly as
> written.

---

## 11. Packet C — scoped plan (`exercises.js`) — **PLAN v2; GATE 1 APPROVED AND EXECUTED 2026-08-22, NOT MERGED** *(the heading read "GATE 1 NOT YET APPROVED" until the ruling at §11.16)*

> ⚠️ **SUPERSEDED 2026-08-22 — the STATUS line below described this section before Gate 1, and is
> annotated rather than rewritten so the planning-time state stays legible.** **Gate 1 is APPROVED**
> (§11.16). The test file exists, the **42**-row matrix ran, the branch is pushed and a
> **ready-for-review PR** is open (§11.17). **Merge remains separately gated** (§11.18). Read §11.16 and
> §11.17 for the live state; everything below this line is the plan **as approved**, and its
> predictions are left exactly as predicted so §11.17 can be read against them.
>
> **STATUS: PLANNING ONLY.** No test file exists, no mutation has been run against the repository, no
> branch has been pushed and no PR has been opened. **Gate 1 for Packet C is not approved** — §10.13
> lists Packet C among the items each needing its own confirmation, and §0.1's Q1 authorizes it only
> as *test-only* work, not as permission to start. §11.14 restates the stop.
> **PLAN v2 — 2026-08-22** (record in **§11.15**). Plan v1 was written the same day against `b52df68`,
> then reviewed by the Gate 1 council (`architecture-reviewer`, `test-strategist`,
> `product-risk-reviewer`, all read-only) and **corrected against measurement**. **All three returned
> "Needs revision."** Twenty-two claims (C-1…C-22) are dispositioned in §11.15 and applied in place;
> **four were blocking**, and **two of those four were found independently by two reviewers each**.
> **One prescription was inverted by measurement** — the `vi.resetModules()` mock-identity trap that
> Plan v1's §11.5 was built around **does not exist in Vitest 4.1.11** (§11.15-C-5). The four probe
> measurements that settled it ran against throwaway files under the gitignored `artifacts/probe/`
> with their own `--config`; **`static/js` was never touched and the repository suite was never run.**
> **Base**: `origin/main` = local `main` = **`b52df68`**, measured 2026-08-22. **Open PRs: 0.**
> Isolated worktree `d:/development/HT-v3-packetc-exercises`, branch `wt/phase3-packet-c-exercises`.
> **Predecessor state**: Packet A merged as `9e5997a` (#387); **Packet B merged as `987588a`** (#406),
> its KI-010/KI-011 documentation follow-up as **`f3b9313`** (#407). Post-merge CI on `b52df68` is run
> **32574292061**, **18/18 green**, `JS Unit (Vitest, non-required)` included.
> **Predicted count: 29 cases, delta 202 → 231, mutations P1–P42.** The **case** count is unchanged by
> Plan v2 — no council item added or removed a case — so the delta and all four pinned count checks
> stand. The **mutation** count moved **40 → 42** (§11.15-C-6). Every figure in this section is
> either a **measurement** with its commit and date, or is labelled a **prediction**. Predictions are
> not to be quietly edited to match whatever execution produces (§10.7-R9's standing rule).

### 11.1 Ownership and containment

| | |
|---|---|
| **Implementation creates** | `static/js/modules/__tests__/exercises.test.js` — **one** new file, nothing else |
| **This packet may modify** | `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` (this plan and its later execution record) |
| **Must not touch** | `static/js/modules/exercises.js` **or any production JS**; any existing test file; `package.json`; `package-lock.json`; `vitest.config.js`; `.github/workflows/**`; branch protection; `docs/test_inventory/**`; `backup-center.js` (dropped by Q3, §2.4); `.claude/settings.json` or any harness configuration; and the shared canonical status documents (`docs/MASTER_HANDOVER.md`, `docs/TESTING_STRATEGY_PLANNING.md`, `docs/UI_SCENARIOS_GAP_ANALYSIS.md`, `docs/ai_workflow/QUALITY_GATE.md`) |
| **No new helper module** | §10.4's closing paragraph already ruled this: *"No shared helper file is authorised by Packet B or Packet C, and creating one would be a second new file that neither packet's ownership row permits."* Packet C reuses Packet B's **patterns** — the ordered log, the hand-written fake, the anti-vacuity fixture check — and **none of its code**. The `bootstrap.Modal` fake is written fresh inside `exercises.test.js` and is **smaller** than Packet B's `Toast` fake, because `exercises.js` calls less surface (§11.6) |
| **The one qualification to the "must not touch" row** | §11.8 applies **40 mutations to `exercises.js` and 2 to `exercises.test.js`** *(Plan v1's **38** was not swept when P41 and P42 were appended — §11.8's own row-count line has said 40 since Plan v2)*, which reads as a contradiction and is not one: **every mutation is applied to a COPY** under the gitignored `artifacts/probe/`, the production file is never written to, and the run ends by asserting `static/js/modules/exercises.js` is unchanged **through git's own normalisation** (`rev-parse` vs `hash-object`, §10.12 defect 3), not by a raw byte compare. In-place mutation with byte-restore is **not** an alternative — §10.1's reasoning transfers verbatim |
| **Where the harness lives** | The gitignored **`artifacts/`**, never `scripts/`. A file under `scripts/**` pulls in QUALITY_GATE's *Tooling* routing and would change this packet's gate set (§10.1, council C-7). The harness is scratch, is not committed, and is **not part of the deliverable** |
| **Must not do** | Promote `js-unit`; act on **Q4** or **Q6**; begin **Packet F**; regenerate the test inventory; touch either KI row; edit `QUALITY_GATE.md`'s frontend feature map (§11.10 raises a real gap in it and routes it to the owner rather than fixing it) |
| **Environment** | `// @vitest-environment jsdom` on **line 1** (§3.2) — the fourth jsdom file in the suite, after `exports.test.js`, `fetch-wrapper.test.js` and `toast.test.js` |
| **Collaborator mocks** | **Four** modules plus one global fake — the highest collaborator count of any packet in step 12 (§2.3 predicted exactly this). Detailed in §11.6 |

**Workstream ownership — measured, and it is clean.** No live claim exists on `static/js/**` or on
`exercises.js`. `docs/ai_workflow/WORKSTREAM_OWNERSHIP.md` holds **no** live claims by design — live
claims live in gitignored `*.local.md` files — and neither `WORKSTREAM_OWNERSHIP.local.md` nor
`docs/MASTER_HANDOVER.local.md` claims this path. **No `exercises.test.js` exists in any of the ~55
worktrees on this machine** (scanned 2026-08-22).

> **CORRECTED 2026-08-22 (Gate 1 owner ruling, plan-hygiene correction 2 of 4).** Plan v1 and Plan v2
> both closed the paragraph above with *"and there is no Packet C branch, worktree or PR"*. **That was
> true before planning began and the planning itself falsified it** — the same class of stale prose
> §10.12 made a discipline of annotating. The **sole** Packet C branch and worktree are the ones this
> section's own header block already names:
>
> | | |
> |---|---|
> | Branch | **`wt/phase3-packet-c-exercises`** |
> | Worktree | **`D:/development/HT-v3-packetc-exercises`** |
> | PR | **none at ruling time** — the PR opened by §11.17's execution is recorded there |
>
> No other checkout on this machine holds a Packet C branch, and the ~55-worktree scan for an
> `exercises.test.js` still returns nothing.

> **RECORDED LABEL COLLISION — two unrelated things are called "Packet C".** Greps of the local status
> documents for *"Packet C"* return hits that belong to **Testing Phase-2 Packet C (strict console,
> merged as #362)** — a different arc, long closed, with no relationship to this section. This is the
> same failure class the document already fought once and resolved administratively (the Packet E → F
> relabel, §2.6). **It is recorded, not renamed**: Phase-2 Packet C is merged and its label is
> historical, so a rename would rewrite a closed record to serve a live one. Any future reader
> grepping *"Packet C"* must disambiguate by **phase**, and this file's Packet C is always the
> `exercises.js` one.

### 11.2 What was measured before planning

Every row was measured **2026-08-22 in the `wt/phase3-packet-c-exercises` worktree on `b52df68`**.
Nothing here is inherited from §1, §2.3 or §10; where an inherited figure was re-measured and found
wrong, the row says so.

**Toolchain and suite baseline — re-measured, not inherited.**

| Surface | Measured value |
|---|---|
| Vitest | **4.1.11** (raised by the merged dependabot PR #408) |
| node / jsdom | **v24.19.0** / **30.0.1** |
| `npm run test:js` | **12 test files / 202 cases passed**, ~**770 ms** |
| `npm run test:js -- --coverage` | statements **7.4 % (552/7453)**, branches **10.22 % (475/4644)**, functions **7.29 % (81/1110)**, lines **7.16 % (498/6946)** |
| Per-file coverage today | `exercises.js` **0 % / 0 % / 0 % / 0 %**; `toast.js` **100 / 97.87 / 100 / 100** (Packet B); `fetch-wrapper.js` 55.12 % st; `workout-plan.js` **0 %**; `workout-plan-events.js` **0 %** st and fn |
| `exercises.js` coverage denominators | **30 statements, 30 lines, 2 functions, 12 branches** |

Packet B's predicted **155 → 202** is therefore **confirmed as the live baseline**, measured on this
base rather than carried from §10.6.

> **NEW, and recorded so it is never mistaken for a Packet C regression.** Vitest **4.1.11** emits a
> config warning on **every** run: *"Your Vite config uses features that are unsupported by
> `configLoader: 'native'` … ESM syntax in a file loaded as CommonJS (vitest.config.js:1:1)"*. It is a
> **warning only** — **exit code 0, 202/202 pass**. It is present on `b52df68` **before Packet C exists**.
> **Packet C must not fix it**: `vitest.config.js` is on the do-not-touch row (§11.1), and touching it
> would convert a test-only packet into a config change. A future reader seeing this warning beside a
> Packet C run must attribute it to the dependabot Vitest bump, not to the test file.

**The module under test — `static/js/modules/exercises.js`, 70 lines, byte-verified on `b52df68`.**

| Fact | Evidence |
|---|---|
| Exports: **exactly 2** | `removeExercise` (`:9`), `clearWorkoutPlan` (`:42`) — both `export async function` |
| Module-level mutable state: **exactly 1** | `const deletingExercises = new Set()` at **`:7`**. The **binding** is `const`; its **contents** are mutable, which is what makes it state. **There is no exported reset** — §11.5 discharges §4.1 against this fact |
| Imports: **4 modules**, no globals besides `bootstrap` | `showToast` (`:1`), `fetchWorkoutPlan` + `resetWorkoutControlsToDefaults` (`:2`), `notifyVolumeAffectingPlanChange` (`:3`), `api` (`:4`) |
| DOM read by `removeExercise` | **None at all.** The function contains no `document` reference |
| DOM read by `clearWorkoutPlan` | **Exactly one node** — `document.getElementById('clearPlanModal')` at `:45` |
| `bootstrap` surface touched | **Only** `bootstrap.Modal.getInstance(modal)` (`:47`) and `bsModal.hide()` (`:49`). **No constructor, no `show`, no `dispose`** |

**Collaborator contracts — measured, and two of them contradict what an implementer would assume.**

*(1) `showToast` — §2.3 named only the two-argument legacy shape; there are **two** legacy arities.*
All five call sites in `exercises.js` use a legacy call **shape** — a message in the first position,
never a type word by intent. `toast.js`'s modern signature is `showToast(type, message, options = {})`,
and the legacy branch at `toast.js:15` fires only when the first argument is **not** one of
`success|error|warning|info`.

> **The shape is legacy; the branch taken is not always the legacy one** (council C-14). `:31` and
> `:59` pass `result.message` straight through, so **whenever the server's message happens to equal a
> type word, `toast.js:15` takes the MODERN branch** and the caller's message is swallowed. That is
> exactly the KI-010 collision **C26** documents. Plan v1 said "all five use the legacy **signature**",
> which contradicted C26 two subsections later. The correction is harmless for the tests — `toast.js`
> is mocked, so the arities below are unaffected — but two claims in one document must not disagree.

| Site | Call | Arity |
|---|---|---|
| `exercises.js:12` | `showToast("Exercise ID is missing. Unable to remove exercise.", true)` | **2 args, legacy** |
| `exercises.js:31` | `showToast(result.message \|\| "Exercise removed successfully!")` | **1 arg, legacy** |
| `exercises.js:36` | `` showToast(`Unable to remove exercise: ${error.message}`, true) `` | **2 args, legacy** |
| `exercises.js:59` | `showToast(result.message \|\| 'Workout plan cleared successfully!')` | **1 arg, legacy** |
| `exercises.js:68` | `` showToast(`Unable to clear workout plan: ${error.message}`, true) `` | **2 args, legacy** |

So the shape §2.3 and §4.3 name — *"the two-argument legacy shape"* — covers **3 of 5** sites; the
other **2** are the legacy **one-argument** form, which §2.3 does not mention. §11.3 pins **both**.
Note that Vitest's `toHaveBeenCalledWith` is **arity-exact**, so every row asserting a full argument
list already pins the argument count; no separate arity case is added, and none is needed.

*(2) `api.post` rejects with a PLAIN OBJECT, not an `Error` — this is the single most likely way a
Packet C fixture goes wrong.* `fetch-wrapper.js`'s `normalizeError()` (`:51-91`) returns
`{ code, message, requestId }`, and that object is what is **thrown** at `:216` and `:249`. On success
`api.post` resolves with the parsed JSON with `requestId` stamped on (`:196`). **A rejection fixture
built as `new Error('Boom')` would test a shape production never produces** — the error paths at
`exercises.js:35-36` and `:67-68` only ever see a plain object. Every rejection in §11.3 is therefore
`{ code: 'SOME_CODE', message: 'Boom', requestId: 'R1' }`.

*(3) `workout-plan.js`* exports `export async function fetchWorkoutPlan()` and
`export function resetWorkoutControlsToDefaults()`. Both are mocked. **`fetchWorkoutPlan()` is not
awaited** by `exercises.js` (`:32`, `:60`) — pinned by **C27**.

*(4) `workout-plan-events.js` is a 5-line, single-export module.*
`notifyVolumeAffectingPlanChange(reason)` dispatches
`CustomEvent('workout-plan:volume-affecting-change', { detail: { reason } })` on `document`. Its
**only** listener repo-wide is `static/js/modules/plan_volume_panel.js:245`. The reason vocabulary
across the app is `'add-exercise'`, `'remove-exercise'`, `'clear-workout-plan'`, `'replace-exercise'`,
`'sets-edit'`, `'starter-plan-generated'`, `'program-backup-restore'`; **`exercises.js` owns exactly
two of them** — `'remove-exercise'` (`:33`) and `'clear-workout-plan'` (`:61`). A reason string is a
plain string argument with no compile-time protection, so a typo is invisible to every other tier.

> **And the listener is DEBOUNCED — measured, and it constrains what the ordered log may claim**
> (council C-1, C-17). `plan_volume_panel.js:244-247` routes the event into a **150 ms-debounced**
> `fetchAndRender`. So the *relative* order of `notifyVolumeAffectingPlanChange()` against
> `fetchWorkoutPlan()` or `resetWorkoutControlsToDefaults()` is **not observable in production**: any
> of those orderings collapses into the same 150 ms window. This is why every ordered-log expectation
> in §11.3 except the `api.post` → `resetControls` relation is labelled **characterization of current
> call order**, not a contract (§11.11-R8).

**Entry points and the argument type production actually passes.**

| Entry | Where | What it passes |
|---|---|---|
| `removeExercise` | Generated in JS, **not** in a template — `static/js/modules/workout-plan-table.js:419`: `` <button … onclick="removeExercise(${exercise.id})"> `` | **Always a NUMBER** — the template literal interpolates a bare id, so the emitted attribute is `removeExercise(7)` |
| `clearWorkoutPlan` | `templates/workout_plan.html:579` — `#confirmClearPlanBtn` with `onclick="clearWorkoutPlan()"` | No arguments |
| Both | Wired as `window.*` globals at `static/js/app.js:36-37` | — |

Modal markup, for the fixture: `templates/workout_plan.html` has `#clear-plan-btn` at **:277**
(`data-bs-toggle="modal" data-bs-target="#clearPlanModal"`), the modal
`<div class="modal fade" id="clearPlanModal" …>` opening at **:564**, `#clearPlanModalLabel` at
**:568**, and `#confirmClearPlanBtn` at **:579**.

**FINDING-C-E2E — the E2E coverage figure in §1.3 was an over-count, and the honest picture is a
STRONGER case for Packet C than §2.3's.**

> **Plan v2 rebuilt this table's evidence** (council C-11, raised independently by **all three**
> reviewers). Plan v1 claimed *"measured by reading every hit"* but listed only **3 + 4 = 7** files
> against a **9** it was correcting, stated **no grep**, and mis-cited four line references. All three
> reviewers nevertheless re-derived **3** independently, so the **conclusion stands and the figure in
> §1.3 stands** — it was the evidence that was thin, not the answer. The table below is the repaired
> version: the pattern is stated, every file it returns is dispositioned, and the arithmetic
> reconciles.

**Pattern:** `rg -n "remove_exercise|removeExercise|clear_workout_plan|clearWorkoutPlan" e2e/` →
**9 spec files**, plus `e2e/fixtures.ts` which is not a spec.

| Spec | What it actually does | Drives the module? |
|---|---|---|
| `e2e/exercise-interactions.spec.ts:218` *"clicking delete sends the remove request"* | Clicks the real delete button, waits for `POST /remove_exercise`, asserts **status 200 only**. **Wrapped in `if (count > 0)`** — it passes **vacuously** on an empty table | **Yes**, weakly |
| `e2e/superset-edge-cases.spec.ts:256-277` | Clicks the real delete button; asserts 200 + row count + partner unlinked | **Yes** |
| `e2e/ui-hardening.spec.ts:996-1034` | Drives `#clear-plan-btn` → `#confirmClearPlanBtn`, i.e. the real `clearWorkoutPlan()`. Asserts **the modal actually closes** — `:1018`, `await expect(page.locator('#clearPlanModal')).not.toHaveClass(/show/, …)` — **and** KI-005's end state (six controls at pinned defaults, storage key absent, survives reload) | **Yes** — the sole spec |
| `e2e/empty-states.spec.ts:33` | Declares a **local helper also named `clearWorkoutPlan`** that calls `resetWorkoutPlan(page)` and reloads. **Never invokes the module.** A pure name collision | **No** |
| `e2e/api-integration.spec.ts:50,146` | `request.post('/clear_workout_plan')` and `request.post('/remove_exercise')` — **route level, no browser JS**. *(Plan v1 cited `:49,145`, which are the helper declaration and the test title, not the calls.)* | **No** |
| `e2e/error-handling.spec.ts:282` | Raw `fetch('/remove_exercise')` inside `page.evaluate` — bypasses the module | **No** |
| `e2e/progression.spec.ts:671,677` | `page.request.post` — route level | **No** |
| `e2e/program-backup.spec.ts:45,368` | `page.request.post` — route level | **No** |
| `e2e/workout-log.spec.ts` | `page.request.post` — route level | **No** |
| `e2e/volume-progress.spec.ts` | `page.request.post` — route level | **No** |
| *(`e2e/fixtures.ts:315-316`)* | `page.request.post` in a shared helper. **Not a spec file**, so outside the 9 | **No** |

**The arithmetic reconciles: 9 = 3 + 6.** `e2e/accessibility.spec.ts` is **not** among the 9 — it
matches only a looser `exercise` stem (`#clearPlanModal` in a comment at `:589`, `ADD_EXERCISE_BTN` at
`:598`/`:1037`, `#exerciseSelect` at `:826`) and **no hit invokes either export**. Plan v1 called it
"a filename hit only", which was wrong on its face; it is named here so a reader greping a looser
pattern is not surprised.

**2 specs reach `removeExercise()`; 1 reaches `clearWorkoutPlan()`. §1.3's "9" is corrected in place
to 3** (see correction note 1 under §1.3's table).

**What has ZERO coverage at any tier today** — this list, not the count, is why Packet C exists:

- the **concurrent-delete guard** (`:17-20`) and its **`finally` release** (`:37-39`);
- the **missing-ID early return** (`:10-14`) on either falsy value;
- **any** `showToast` call shape — neither arity, neither copy string, neither fallback;
- **either** `notifyVolumeAffectingPlanChange` reason string;
- **both** error paths (`:34-36`, `:66-68`);
- the exact `api.post` argument triples, including `showErrorToast: false` and `body: null`;
- **that `resetWorkoutControlsToDefaults()` never runs on the error path** — `ui-hardening.spec.ts`
  drives only the success journey, so the failure branch at `:66-68` is unexercised anywhere;
- the **call order** inside `clearWorkoutPlan()` — `ui-hardening.spec.ts` asserts the **end state**, and
  an end-state assertion is **order-blind** by construction. *(Kept as a cross-tier fact. **It is not a
  contract claim**: §11.2's debounce measurement shows no ordering here is observable in production, so
  §11.3-C19 and §11.8-P33 pin it as **characterization** — council C-1.)*;
- **two of the three modal branches** (`:45-46` absent, `:47-48` no-instance). The third — `hide()`
  being called when an instance exists (`:49`) — **is** partly covered: `ui-hardening.spec.ts:1018`
  asserts `#clearPlanModal` loses its `show` class (council C-12). What is uncovered there is the
  *branching*, not the effect.

> **§2.3's framing is superseded by this subsection, and §2.3 is deliberately NOT edited.** §2.3 reads
> *"heavily E2E-covered already, so unit value is narrower"*. Measured, that is backwards: the module
> has **3** specs, one of which is vacuous on an empty table, and the behaviors listed above are
> unreached by **any** tier. §2.3's *sequencing* judgement (Packet C runs third) is unaffected and
> stands. The claim being corrected is a **rationale**, not a false number, and §11 is the scoped plan
> that supersedes it — so it is corrected **here**, in the section that owns it, rather than by editing
> a ratified earlier section.

#### Corrections applied to earlier sections

**FOUR** edits are made outside §11 — **one** by Plan v1, **two more** by Plan v2, and **one more by
the Gate 1 owner ruling of 2026-08-22** — and all four are listed here so nothing in the diff is a
surprise. *(Plan v1 said "exactly one"; council C-1(d) and C-13 each added one, and the owner's §2.3
ruling added the fourth, so that sentence has now been corrected twice.)*

| # | Where | Change | Why it was narrowly necessary |
|---|---|---|---|
| **1** *(Plan v1)* | **§1.3**, the `exercises.js` row's *"E2E specs touching it"* cell, plus its adjacent note block | **9 → 3**, with the grep stated and **every** file it returns dispositioned (rebuilt by Plan v2 per council C-11) | The cell states a **measured quantity** that is **false as measured**. Packet C's entire justification is *what E2E does not reach*, so leaving a 3× over-count in the document that authorizes it would have a reviewer weighing this plan against a coverage picture that does not exist |
| **2** *(Plan v2, council C-1)* | **§1.3**, the same row's *"untested high-risk behavior"* cell, plus a second note block | *"the ordering contract … must run **after** the refresh (KI-005 criterion 4)"* → **"runs only after the server clear succeeds and never on the error path"** | The old wording is a **false attribution to a named criterion**, present since 2026-08-15, and it is the **source** of the over-read that Plan v1 then built C19 and P33 on. `ki005_controls_persistence/PLANNING.md:448` says the reset is called *after the successful server clear* and that its "LAST" is **internal to the helper** (`workout-plan.js:408-413`), not a position relative to the refresh. Leaving it would leave the document arguing against itself, since §11.3-C19 now labels the call order as characterization |
| **3** *(Plan v2, council C-13)* | The document's opening **Scope** block, lines 13-14 | Annotated in place: *"Packet C now has a Gate 1 plan at §11; still unauthorized"* | The block says **Packet C** is *"untouched and still unauthorized"*. §11 falsifies the first half. This is the standard §10.12 discipline — *"this commit falsified prose that was true before it"* — and Packet B annotated **four** such places. The block is **annotated, not rewritten**, so the original sequence stays legible |
| **4** *(Gate 1 owner ruling, 2026-08-22)* | **§2.3**, the *Coverage targets* bullet, plus a note block under it | *"`showToast` receiving the **legacy** two-argument shape"* → **both** legacy arities, **3 two-argument** and **2 one-argument**, as measured; and *"the KI-005 criterion-4 ordering"* → **"runs only after the server clear succeeds and never on the error path"**, with contract and characterization separated explicitly | Both claims are **false as measured**, and §2.3 is the *source* wording — the same false criterion-4 attribution corrected at §1.3 (row 2) survives here, so a reader who starts at §2.3 re-derives exactly the over-read §11.15-C-1 unwound. The *"Why third"* framing is **not** touched: it is superseded in §11.2 above, where the measurement lives |

Nothing else in §0–§10 is modified, and no file outside
`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` is modified. **§2.3's *Coverage targets* bullet IS now
edited** (row 4 above, added by the Gate 1 owner ruling — this supersedes Plan v2's *"§2.3 is still not
edited"*, and its *"Why third"* framing remains untouched and superseded in place). Neither
`UI_SCENARIOS_GAP_ANALYSIS.md`, `QUALITY_GATE.md`, nor `ki005_controls_persistence/PLANNING.md` is
touched — the last two are **read** for the corrections above and nothing more.

### 11.3 Case matrix — C1–C29 (**29 cases**, prediction)

> **Rows = predicted reported cases = 29.** The row count and the predicted case count are deliberately
> the same number, so `+29` in §11.10 is an arithmetic check rather than an estimate — the discipline
> §10.3 established.

**Three authoring rules, inherited and non-negotiable.**

1. **No negative assertion stands alone** (§10.9 C-5). Every `not.toHaveBeenCalled` must be paired with
   a positive proving the call ran to completion. Concretely: **C1/C2** assert the `console.error` text
   **and** the toast **before** asserting `api.post` was not called; **C9/C25** express their negatives
   as a **deep-equality on the ordered log**, which is positive and negative in one assertion; **C11**
   asserts two `api.post` calls **before** asserting the duplicate-guard `console.log` never fired;
   **C17** asserts the flow completed **before** asserting `Modal.getInstance` was never called.
2. **Rejections are plain objects, never `Error`s** (§11.2, contract 2). Any row using `new Error(...)`
   is wrong by construction.
3. **Ordered-log expectations are PREDICTIONS.** The four arrays below are derived from reading the
   module, not from running it. §10.7-R9's rule applies: if execution produces a different array, the
   discrepancy is **investigated before any expectation is edited**.

**The single shared ordered log.** One `calls` array, appended to by **all five** mocks — `api.post`,
`showToast`, `fetchWorkoutPlan`, `notifyVolumeAffectingPlanChange`, `resetWorkoutControlsToDefaults` —
plus the `Modal` fake. Labels: `'Modal.getInstance'`, `'Modal.hide'`, `'api.post'`, `'showToast'`,
`'fetchWorkoutPlan'`, `'notifyVolume'`, `'resetControls'`. **This is the technique that cannot be
expressed as independent per-mock spies** (§10.4). Unlike Packet B's B36/B37, **no mid-case
`calls.length = 0` is needed**: each ordering row covers exactly one call of one exported function from
a clean `beforeEach`.

> **What the ordered log is, and is not, evidence of** (council C-1 and C-17, both accepted). Plan v1
> said this log *"is the only thing in the repository that can catch a KI-005 criterion-4 ordering
> regression"*. **The cross-tier half of that is true and is kept; the contract half is false and is
> dropped.**
>
> - **Kept:** no other tier can red a reordering here. `ui-hardening.spec.ts:996-1034` asserts the
>   **end state**, which is identical under every ordering.
> - **Dropped:** that a reordering would be a *regression*. Measured — `fetchWorkoutPlan()`
>   (`workout-plan.js:90-117`) touches **no** workout control, and the sole
>   `workout-plan:volume-affecting-change` listener is **150 ms-debounced**
>   (`plan_volume_panel.js:244-247`). So **no ordering among `fetchWorkoutPlan`, `notifyVolume` and
>   `resetControls` is observable in production.** Those relations are pinned as **characterization of
>   current call order**, and a future red means *"confirm intent"*, not *"a user-visible defect"*.
> - **The one relation that IS a contract**, and the one criterion 4 actually states, is
>   **`api.post` → `resetControls`**: the reset runs *only after the successful server clear*
>   (`ki005_controls_persistence/PLANNING.md:448`) and **never on the error path**. That is pinned by
>   the `api.post`-before-`resetControls` position inside **C19** and, decisively, by **C25**.

| Phase | Arrangement | Expected `calls` (**prediction**) |
|---|---|---|
| **C7** — `removeExercise` success | resolved `api.post` | `['api.post','showToast','fetchWorkoutPlan','notifyVolume']` |
| **C9** — `removeExercise` failure | rejected `api.post` | `['api.post','showToast']` |
| **C19** — `clearWorkoutPlan` success, modal **and** instance present | `getInstance` returns a fake instance | `['Modal.getInstance','Modal.hide','api.post','showToast','fetchWorkoutPlan','notifyVolume','resetControls']` |
| **C25** — `clearWorkoutPlan` failure, modal **and** instance present | rejected `api.post` | `['Modal.getInstance','Modal.hide','api.post','showToast']` |

---

| ID | Behavior | Arrange | Oracle | Production lines |
|---|---|---|---|---|
| **`removeExercise` — missing-ID early return** | | | | |
| **C1** | Falsy id (`undefined`) is refused before any work | call `removeExercise(undefined)` | `console.error` called with exactly `"Error: exercise ID is required to remove an exercise."`; `showToast` called with **exactly two** args `("Exercise ID is missing. Unable to remove exercise.", true)`; **then** `api.post` **not** called and `calls` is `['showToast']` | `exercises.js:10-14` |
| **C2** | `0` — the **plausible-but-invalid** falsy value, because **no in-app call site passes a string** and ids arrive as numbers (`workout-plan-table.js:419`) | `removeExercise(0)` | Same oracle as C1. **Isolated by P42** (`!exerciseId` → `exerciseId == null`), the exact "fix" a developer would write, under which `0` passes the guard while `undefined` still does not — council C-6 | `exercises.js:10`, `workout-plan-table.js:419` |
| **`removeExercise` — success path** | | | | |
| **C3** | The exact `api.post` argument triple | `api.post` resolves `{ message: 'Removed' }`; `removeExercise(7)` | `api.post` called **once** with `("/remove_exercise", { id: 7 }, { headers: { "Content-Type": "application/json" }, showLoading: false, showErrorToast: false, useDefaultHeaders: false })` — deep equality on all three arguments. **`showErrorToast: false` is why the module toasts for itself at `:31`/`:36`; flipping it would double-toast in production** | `exercises.js:25-30` |
| **C4** | `result.message` is passed through **verbatim**, one argument | resolves `{ message: 'Removed' }` | `showToast` called **once** with **exactly one** argument `'Removed'` | `exercises.js:31` |
| **C5** | The `\|\|` fallback branch | resolves `{}` (no `message`) | `showToast` called once with exactly one argument `"Exercise removed successfully!"`. **DISCLOSED (council C-10): this fallback is UNREACHABLE through the real route.** `routes/workout_plan.py:299` always returns `message="Exercise removed successfully"` and `utils/errors.py:36-37` sets `response["message"]` whenever truthy, so `result.message` is always present — and the fallback string differs from the server's **by a trailing `!`**. Same "defensive but unreachable" class Packet B disclosed for B15a/B15b (§10.9 owner-question 3); pinned because the branch exists, **not** because a user can see it | `exercises.js:31`; `routes/workout_plan.py:299` |
| **C6** | The reason string is exactly `'remove-exercise'` | resolved post | `notifyVolumeAffectingPlanChange` called **once** with **exactly** `'remove-exercise'` | `exercises.js:33` |
| **C7** | Success ordering | resolved post | `calls` deep-equals `['api.post','showToast','fetchWorkoutPlan','notifyVolume']` | `exercises.js:25,31,32,33` |
| **`removeExercise` — error path** | | | | |
| **C8** | The interpolated error toast and the console record | `api.post` rejects with the **plain object** `{ code:'REMOVE_FAILED', message:'Boom', requestId:'R1' }` | `console.error` called with `("Error removing exercise:", <that same object, by identity>)`; `showToast` called with **exactly two** args `('Unable to remove exercise: Boom', true)` | `exercises.js:34-36` |
| **C9** | Nothing downstream runs on failure | same rejection | `calls` deep-equals `['api.post','showToast']` — a single assertion that is **positive** (the toast ran) and **negative** (no refresh, no notify) at once, satisfying rule 1 without a bare `not.` | `exercises.js:32-33` vs `:34` |
| **`removeExercise` — the concurrent-delete guard (the headline, zero coverage anywhere)** | | | | |
| **C10** | A concurrent second call for the **same** id is rejected | `const p1 = removeExercise(1);` **unawaited**, then `await removeExercise(1);` then `await p1;`. **Fully deterministic — no timers**: the synchronous prologue `:10-22` runs to the first `await` at `:25`, so the second call's guard check at `:17` happens before any microtask can resume `p1` | `api.post` called **exactly once**; `console.log` called with `('Delete already in progress for exercise:', 1)`; `calls` deep-equals `['api.post','showToast','fetchWorkoutPlan','notifyVolume']` — i.e. **one** toast, not two | `exercises.js:17-20` |
| **C11** | A concurrent call for a **different** id is **not** blocked | `const p1 = removeExercise(1);` then `await removeExercise(2);` then `await p1;` | `api.post` called **twice**, with bodies `{id:1}` and `{id:2}`; **then** `console.log` never called. **Co-killed by P41** (`.has(exerciseId)` → `.size > 0`, the realistic broken-guard shape, under which a concurrent delete of a *different* id is wrongly blocked) **and by P11** (the body shape). *(Plan v2 said "**Isolated** by P41"; **measured false** — P41 also reds C14, §11.17. **No mutation reds C11 alone**, and it is back in §11.8's disclosure table.)* | `exercises.js:17,22` |
| **C12** | The guard is **released** on success | `await removeExercise(1); await removeExercise(1);` — sequential | `api.post` called **twice**. **The honest oracle is a second successful call, not inspection of the unexported `Set`.** No mutation isolates C12 from C13 — disclosed under the matrix, not discovered later | `exercises.js:37-39` |
| **C13** | The guard is **released** on failure | **`api.post.mockRejectedValueOnce({ code:'REMOVE_FAILED', message:'Boom', requestId:'R1' }).mockResolvedValue({ message:'Removed' })`**, then **two sequential awaited calls**: `await removeExercise(1); await removeExercise(1);`. *(Plan v1's "re-point the mock" wording left both calls resolving, which does not produce the oracle below — council C-16.)* | `api.post` called **twice**; the **first** call's `showToast` carries the error shape (two args) and the **second** carries the success shape (one arg), proving the second reached `:31` and not `:36` | `exercises.js:37-39` |
| **C14** | **CHARACTERIZATION — `Set` keys are type-sensitive.** `1` and `'1'` are different keys, so both proceed. **No in-app call site passes a string** — `workout-plan-table.js:419` interpolates a bare `${exercise.id}` — but `removeExercise` is also a `window` global (`static/js/app.js:36`), so "unreachable" would overstate it (council C-18). A recorded property of the guard, **not a bug report** | `const p1 = removeExercise(1);` then `await removeExercise('1');` then `await p1;` | `api.post` called **twice**. Commented in the file as *characterization of `Set` identity, not desired behavior*; see §11.11-R4. **No *isolating* killer** — disclosed under the matrix. *(Plan v2 said "killed by **no** mutation of `exercises.js`"; **MEASURED FALSE** — **P41 reds C11 and C14 together**, §11.17. Corrected in place here and in §11.8's disclosure table.)* | `exercises.js:7,17,22`; `workout-plan-table.js:419`; `app.js:36` |
| **`removeExercise` — isolation and DOM independence** | | | | |
| **C15** | **ANTI-VACUITY: the module-reset strategy actually works.** Self-contained; **no cross-case ordering dependency** (§4.4) | `api.post` returns a **manually-controlled deferred**; `const p1 = removeExercise(1)` leaves `1` **trapped** in the guard; assert a second `removeExercise(1)` on **this** instance is blocked; then `vi.resetModules()` and dynamically re-import `exercises.js`; call `removeExercise(1)` on the **fresh** instance with `api.post` now resolving; finally resolve the deferred and `await p1` so no promise dangles | Blocked call → `api.post` still at **1**; fresh instance → `api.post` at **2**. This proves both that `deletingExercises` is genuinely per-instance state **and** that the hoisted mock handles survive `resetModules()` (§11.5) | `exercises.js:7,17,22` |
| **C16** | `removeExercise` reads **no DOM** | `document.body.innerHTML = ''` — no `#clearPlanModal`, no fixture at all | The full success path still completes: `calls` deep-equals C7's array, and `document.getElementById` (spied) is **never called** | `exercises.js:9-40` — the function contains no `document` reference |
| **`clearWorkoutPlan` — the three modal branches** | | | | |
| **C17** | Modal element **absent** | remove `#clearPlanModal` from the fixture; `api.post` resolves | Flow completes first — `calls` deep-equals `['api.post','showToast','fetchWorkoutPlan','notifyVolume','resetControls']` — **and** `Modal.getInstance` was never called | `exercises.js:45-46` |
| **C18** | Modal present, `getInstance` returns **`null`** | fixture present; fake `getInstance` returns `null` | `Modal.getInstance` called **once with the `#clearPlanModal` element** (identity); `hide` never called; `calls` deep-equals `['Modal.getInstance','api.post','showToast','fetchWorkoutPlan','notifyVolume','resetControls']` — the trailing entries are the positive pairing, and they are what makes P23 red (§11.8) | `exercises.js:47-48` |
| **C19** | **Two claims of DIFFERENT strength, and Plan v1 conflated them** (council C-1). **(a) CONTRACT** — `resetControls` runs **after `api.post` resolves**, which is what KI-005 criterion 4 actually states (`ki005_controls_persistence/PLANNING.md:448`). **(b) CHARACTERIZATION** — the rest of the sequence, including `hide()` before `api.post` and `fetchWorkoutPlan` before `notifyVolume` before `resetControls`. **No ordering in (b) is observable in production** (§11.2's debounce measurement) | fixture present; `getInstance` returns a fake instance; `api.post` resolves | `calls` deep-equals `['Modal.getInstance','Modal.hide','api.post','showToast','fetchWorkoutPlan','notifyVolume','resetControls']`. **No other tier can red a reordering** — `ui-hardening.spec.ts:996-1034` asserts the end state, which is order-blind — but that is a statement about *coverage*, **not** about product risk. Commented in the file as **characterization of current call order**, except the `api.post`→`resetControls` relation, which is labelled as the criterion-4 contract | `exercises.js:47,49,53,59,60,61,65`; `ki005_controls_persistence/PLANNING.md:448` |
| **`clearWorkoutPlan` — success path** | | | | |
| **C20** | The exact `api.post` argument triple, **body `null`** | resolves `{ message: 'Cleared' }` | `api.post` called **once** with `('/clear_workout_plan', null, { headers: { 'Content-Type': 'application/json' }, showLoading: false, showErrorToast: false, useDefaultHeaders: false })`. **The second argument is `null` — not `undefined`, not `{}`**, and P27 exists to prove this row can tell the difference | `exercises.js:53-58` |
| **C21** | `result.message` passed through verbatim, one argument | resolves `{ message: 'Cleared' }` | `showToast` called once with **exactly one** argument `'Cleared'` | `exercises.js:59` |
| **C22** | The `\|\|` fallback branch | resolves `{}` | `showToast` called once with exactly one argument `'Workout plan cleared successfully!'`. **DISCLOSED (council C-10): unreachable through the real route** — `routes/workout_plan.py:320` always returns `message="Workout plan cleared successfully"`, and the fallback differs from it **by a trailing `!`**. Same disclosure as C5 | `exercises.js:59`; `routes/workout_plan.py:320` |
| **C23** | The reason string is exactly `'clear-workout-plan'` | resolved post | `notifyVolumeAffectingPlanChange` called **once** with **exactly** `'clear-workout-plan'` | `exercises.js:61` |
| **`clearWorkoutPlan` — error path** | | | | |
| **C24** | The interpolated error toast and the console record | `api.post` rejects with `{ code:'CLEAR_FAILED', message:'Boom', requestId:'R1' }` | `console.error` called with `('Error clearing workout plan:', <that object, by identity>)`; `showToast` called with **exactly two** args `('Unable to clear workout plan: Boom', true)` | `exercises.js:66-68` |
| **C25** | **`resetWorkoutControlsToDefaults` is NOT called on the error path**, and neither is the refresh or the notify — expressed positively | same rejection, modal **and** instance present | `calls` deep-equals `['Modal.getInstance','Modal.hide','api.post','showToast']`. One deep equality carries the positive (the modal closed, the error toast fired) and all three negatives; **no bare `not.` assertion is used** (rule 1) | `exercises.js:60-65` vs `:66` |
| **Characterization tie-ins** | | | | |
| **C26** | **KI-010 PASS-THROUGH ONLY.** `exercises.js:31` and `:59` are 2 of the 5 one-argument collision sites named at `docs/UI_SCENARIOS_GAP_ANALYSIS.md:105` | `api.post` resolves `{ message: 'error' }`; `clearWorkoutPlan()` | `showToast` called with **exactly one** argument, the string `'error'` — **verbatim, unmodified**. **Commented in the file as: this pins pass-through and NOTHING ELSE. Packet C mocks `toast.js`, so it cannot observe the collision's rendering; this case neither pins nor mitigates KI-010**, which stays `Open` in a file this packet **may not edit** (§11.1) | `exercises.js:59`; `UI_SCENARIOS_GAP_ANALYSIS.md:105` |
| **C27** | **`fetchWorkoutPlan()` is NOT awaited** — a real regression guard, since adding an `await` at `:60` would strand `notify` and `reset` behind a slow refresh. **DISCLOSED 2026-08-22: this row covers `:60` ONLY.** Its "Production lines" cell also cited `:32`, which C27 does not drive — C27 calls `clearWorkoutPlan()`. **The `:32` counterpart is pinned by nothing and no mutation row exists for it**: adding an `await` at `:32` strands nothing, because `notifyVolumeAffectingPlanChange` at `:33` is the last statement of the `try` and the ordered log is unchanged, so C7/C10/C16 stay green. Recorded as an **accepted, disclosed gap**, not closed — closing it would add a 30th case, and the count is owner-pinned at 29 | `fetchWorkoutPlan` mocked to return a promise that **never settles**; `api.post` resolves; **an explicit per-case timeout of `1000` ms** — a pinned value, not an aspiration (council C-8; reasoning at §11.11-R11) | `await clearWorkoutPlan()` **resolves**, and both `notifyVolume` and `resetControls` are present in `calls`. Kills P37 | `exercises.js:60` *(`:32` was cited here by Plan v2 and is **removed** — C27 never drives it; see the disclosure in this row's Behavior cell)* |
| **Anti-vacuity** | | | | |
| **C28** | **The handles the test asserts on are the handles the module receives.** *(Plan v1 framed this as "the case that fails if the `resetModules` identity trap bites". **That trap does not exist in Vitest 4.1.11 — measured, §11.15-M-a.** The case is kept because the property it asserts is real and independent of any `resetModules` behavior: a test whose spies are not the module's spies asserts nothing, however that came about.)* | after the standard `beforeEach` re-import | The test file's `h.showToast` / `h.fetchWorkoutPlan` / `h.notifyVolumeAffectingPlanChange` / `h.resetWorkoutControlsToDefaults` / `h.post` handles are **`vi.fn()`s at call count 0**, and are the **same object identities** (`toBe`) as the exports of a freshly imported `../toast.js`, `../workout-plan.js`, `../workout-plan-events.js`, `../fetch-wrapper.js`. Kills P39 | §11.5, §11.6 |
| **C29** | **Fixture and `bootstrap` self-check** | default `beforeEach` state, nothing else arranged | `document.getElementById('clearPlanModal')` is **non-null**, and `globalThis.bootstrap.Modal.getInstance` is a function. Without this, **C17's "modal absent" arrangement would be indistinguishable from a fixture that never had the node**, and C18/C19 would pass against a `bootstrap` global that was never installed. Kills P38 — the Packet C analogue of M19 and N30 | §11.4, §11.6 |

**Predicted count: 29 cases** — C1–C29 with no sub-lettered IDs, and the table above has exactly 29
non-heading rows.

**Two cases were considered and declined**, so a later reader does not read the gaps as oversights:

- **`removeExercise(null)` and `removeExercise('')`** — same class as C1/C2 (the `:10` falsy guard),
  killed by the same mutations, and adding them would grow the count without growing the kill set. The
  two chosen values are the two most plausible: `undefined` (a missing `exercise.id`) and `0`
  (a numeric id that is falsy), given that `workout-plan-table.js:419` emits a bare number.
  **Consistency note (council C-6): this criterion — "declined because it adds no kill" — was applied
  to the declined pair while C2 itself had no isolating mutation.** Plan v2 closes that asymmetry by
  adding **P42**, so C2 now earns its place by the same standard the declined pair is judged against.
  Had P42 not been added, the honest move would have been to decline C2 too.
- **A `removeExercise` twin of C26** at `exercises.js:31`. The pass-through claim is identical and the
  same mutation class covers both; one labelled characterization row is enough, and two would imply the
  packet is doing more about KI-010 than it is.

### 11.4 Fixtures and DOM requirements

**`removeExercise` needs no fixture at all.** It contains no `document` reference (§11.2), which is
measured, not assumed — and **C16 pins it** by running the whole success path against
`document.body.innerHTML = ''` with a `getElementById` spy that must never fire. This is the single
biggest structural difference from Packet B, whose every case needed the toast markup: **Packet C's
fixture is one element.**

**`clearWorkoutPlan` reads exactly one node.** The fixture is therefore `#clearPlanModal` and its
minimum enclosing markup, **transcribed verbatim from
[`templates/workout_plan.html`](../../templates/workout_plan.html) starting at line 564** at authoring
time — copied from the live template, never invented, with **the citation in a comment** exactly as
§4.2 requires:

```js
// Reduced from templates/workout_plan.html:564 (#clearPlanModal opens here;
// #clearPlanModalLabel :568, #confirmClearPlanBtn :579). Re-read on b52df68, 2026-08-22.
// Only the id is load-bearing: exercises.js:45 does getElementById('clearPlanModal')
// and nothing else. Transcribe the element's real attributes from the template at
// authoring time; do NOT hand-write approximations of them.
```

**What the fixture deliberately omits, and why each omission is safe** — stated so a later reader does
not mistake the reduction for drift (§10.4's discipline):

| Omitted | Where it lives | Why omitting it is safe |
|---|---|---|
| `#clear-plan-btn` | `workout_plan.html:277` | The **trigger**, wired by `data-bs-toggle`/`data-bs-target`. `exercises.js` never reads it; the button → modal → confirm journey is owned by `ui-hardening.spec.ts:996-1034` |
| `#confirmClearPlanBtn` | `workout_plan.html:579` | The **entry point** (`onclick="clearWorkoutPlan()"`). Packet C calls the exported function directly, so the wiring is E2E's to own |
| `#clearPlanModalLabel` and the modal body/footer chrome | `workout_plan.html:568` onward | Presentational; `exercises.js` reads none of it, and jsdom does no layout |
| The delete button that calls `removeExercise` | Generated by `workout-plan-table.js:419`, **not in any template** | `removeExercise` reads no DOM at all — C16 pins that |

**Fixture rules carried from §4.2**: DOM built in `beforeEach` via `document.body.innerHTML`; torn
down in `afterEach`; `sessionStorage.clear()` / `localStorage.clear()` in `beforeEach` even though this
module uses neither, because jsdom shares them across cases in a file and `workout-plan.js` — mocked
here — is a storage user in production.

**C17's arrangement removes the element inside the case body**, after the shared `beforeEach`. There is
no nesting hazard here of the kind that produced §10.9's D-d — `#clearPlanModal` is the only node in
the fixture, so removing the element and removing its `id` are equivalent. **Removing the element is
preferred** because it models the real absence condition (a page without the modal) rather than a
malformed one.

### 11.5 Module-reset / isolation strategy — and §4.1 discharged **explicitly**

**§4.1 is NOT discharged by absence for this module, and that is the difference from Packet B.**
§10.4 could close §4.1 by observing that `toast.js` has no module-level mutable state. `exercises.js`
does: `const deletingExercises = new Set()` at **`:7`**, with **no exported reset**. §4.1 names this
exact situation — *"State that can only be reset by re-import is a finding to record, not to work
around silently"* — so it is **recorded here as a finding about the module**:

> **FINDING — `exercises.js`'s only module-level state is unreachable from its public API.** The
> `deletingExercises` `Set` (`:7`) is populated at `:22` and drained at `:38`. Neither export reads it
> back, and there is no `resetDeletingExercises()`. In production this is fine — the guard is
> self-clearing in a `finally` — but it means a unit suite **must** re-import the module to get a clean
> instance, and it means an id can only be *observed* as trapped through its **effect** (a second call
> being refused), never by inspection. **Packet C does not work around this and does not propose fixing
> it**: adding an exported reset is a production change and out of scope for a test-only packet.

**The chosen strategy: `vi.hoisted()` stable handles + `vi.resetModules()` + per-case re-import.**

> **PLAN v2 REWROTE THIS SUBSECTION'S JUSTIFICATION, BECAUSE MEASUREMENT INVERTED IT.** Plan v1 built
> the strategy around a `vi.resetModules()` mock-identity trap. **That trap does not exist in Vitest
> 4.1.11** (§11.15-M-a, measured). `vi.hoisted()` is still **mandatory** — for a different and also
> measured reason (§11.15-M-b) — and the `resetModules()` isolation half is sound (§11.15-M-c). The
> mechanics below are unchanged; only the reason for them is corrected, and a false reason left
> standing would have a future reader "simplify" the file on a premise that never held.

```js
// The five mock handles are created ONCE, above every vi.mock factory, and the
// factories RETURN them. vi.hoisted() is REQUIRED — measured, §11.15-M-b — because
// vi.mock factories are hoisted above every plain top-level binding: a factory that
// references a plain `const` throws
//   ReferenceError: Cannot access '<name>' before initialization
// at COLLECTION, and the file reports "(0 test)". It is NOT required to preserve
// identity across vi.resetModules(); measurement shows identity survives regardless.
const h = vi.hoisted(() => ({
    showToast:                       vi.fn(),
    fetchWorkoutPlan:                vi.fn(),
    resetWorkoutControlsToDefaults:  vi.fn(),
    notifyVolumeAffectingPlanChange: vi.fn(),
    post:                            vi.fn(),
}));

vi.mock('../toast.js',                () => ({ showToast: h.showToast }));
vi.mock('../workout-plan.js',         () => ({ fetchWorkoutPlan: h.fetchWorkoutPlan,
                                               resetWorkoutControlsToDefaults: h.resetWorkoutControlsToDefaults }));
vi.mock('../workout-plan-events.js',  () => ({ notifyVolumeAffectingPlanChange: h.notifyVolumeAffectingPlanChange }));
vi.mock('../fetch-wrapper.js',        () => ({ api: { post: h.post } }));

let removeExercise, clearWorkoutPlan;

beforeEach(async () => {
    vi.resetModules();                       // fresh `deletingExercises` per case
    ({ removeExercise, clearWorkoutPlan } = await import('../exercises.js'));
    // ... reset h.* mocks, calls[], the bootstrap fake and the fixture here
});
```

> **THE CLAIM PLAN v1 MADE HERE WAS FALSE, AND MEASUREMENT — NOT REVIEW — SETTLED IT.** Plan v1 stated
> that an inline `vi.mock('../toast.js', () => ({ showToast: vi.fn() }))` factory **re-runs** on the
> fresh registry after `vi.resetModules()`, handing the re-imported module a **new** `vi.fn()` while the
> test file's own binding went stale — and it built an "asymmetric failure / negatives pass vacuously
> forever" argument on top. **Every part of that is wrong for Vitest 4.1.11.**
>
> **MEASURED 2026-08-22** (probe under the gitignored `artifacts/probe/`, its own `--config`, nothing
> under `static/js` touched, repository suite not run):
>
> ```
> PROBE A1 factoryRuns = 1 | topLevel===current = true
> PROBE A2 factoryRuns before/after = 1 1
> PROBE A2 factory fn identity stable = true
> PROBE A2 topLevel === current factory fn = true
> PROBE A2 topLevel call count = 2      <- the FRESH module instance called the ORIGINAL handle
> PROBE A3 fresh instance has(99) = false
> ```
>
> **`vi.resetModules()` does not re-run the factory. The mock registry survives it, and the test file's
> top-level binding stays live and wired to the freshly imported module.** So there is no stale
> binding, no asymmetric failure, and no "negatives pass vacuously forever". §11.11-R1 is rewritten to
> match, and the reader should treat any surviving memory of that argument as void.
>
> **`vi.hoisted()` is still mandatory — for a measured reason, not this one.** A `vi.mock` factory that
> references a plain top-level `const` fails at **collection**:
> `Error: [vitest] There was an error when mocking a module … Caused by: ReferenceError: Cannot access
> '<name>' before initialization`, with the file reporting **`(0 test)`** and the suite failing. Factories
> are hoisted above every ordinary binding; `vi.hoisted()` is the only way to give them something to
> reference. **The strategy is unchanged; its justification is replaced.**
>
> **The `resetModules()` half is sound and was confirmed, not merely assumed** — `PROBE A3` shows a
> freshly imported instance whose `Set` does **not** contain an id the previous instance held. That is
> exactly C15's mechanism.
>
> **The alternative resolution Plan v1 listed** — re-importing every collaborator alongside the module
> in `beforeEach` — is now understood to solve a problem that does not exist. It is **not** adopted, and
> the reason is no longer "five chances to forget one" but simply that it is unnecessary.

**C15 and C28 survive the correction, on their own merits.** C15 demonstrates that a fresh module
instance accepts an id still trapped in the previous instance's guard — self-contained, with **no
cross-case ordering dependency** (§4.4) — and `PROBE A3` independently corroborates the mechanism.
C28 asserts that the handles the test asserts on are the handles the module receives; that is a real
anti-vacuity property **whatever** Vitest's `resetModules()` semantics happen to be, and **P39** proves
it can fail. An isolation strategy that no case can falsify is indistinguishable from no isolation
strategy — that reasoning was right in Plan v1 and is unaffected.

**Everything else reset per case**: the five `vi.fn()`s (cleared, and their implementations re-pointed —
`h.post` is re-configured by each case, so `mockReset()` rather than `mockClear()`), the shared `calls`
array, `currentModalInstance`, `globalThis.bootstrap`, the `console.error` / `console.log` spies, and
`document.body`. `vi.restoreAllMocks()` in `afterEach` restores the console spies and the
`getElementById` spy C16 installs.

### 11.6 Mocks — four modules and one global fake

**Rule (§4.3): mock collaborators, never the module under test; fake only the surface the module
actually calls.**

| Mocked | Shape | Why this shape, measured |
|---|---|---|
| `../toast.js` | `{ showToast: vi.fn() }` | One export. `exercises.js` calls it at `:12`, `:31`, `:36`, `:59`, `:68` — **3 two-argument and 2 one-argument legacy calls** (§11.2). Because `toast.js` is mocked, Packet C sees **call shapes only** and no rendering; that boundary is what makes C26 a pass-through row and nothing more |
| `../workout-plan.js` | `{ fetchWorkoutPlan: vi.fn(), resetWorkoutControlsToDefaults: vi.fn() }` | Both are real exports (`export async function` / `export function`). `fetchWorkoutPlan` is **not awaited** by the module — C27 pins that, and the mock's default return must therefore be a value the module ignores |
| `../workout-plan-events.js` | `{ notifyVolumeAffectingPlanChange: vi.fn() }` | A **5-line, single-export** module. Mocking it — rather than letting the real `CustomEvent` dispatch — is deliberate: the real module's only listener is `plan_volume_panel.js:245`, and importing that would drag a page module into a unit test. The **reason string** is the contract; the dispatch is `workout-plan-events.js`'s own to prove |
| `../fetch-wrapper.js` | `{ api: { post: vi.fn() } }` | **Only `api.post` is faked** — the module imports `api` (`:4`) and calls `post` and nothing else. `apiFetch`, `api.get` and the rest are not faked, because faking unused surface is the §3.3 violation Packet B was corrected for. **Every rejection is a plain object** (§11.2, contract 2) |
| `globalThis.bootstrap` | `{ Modal: { getInstance } }` — **that is the whole fake** | `exercises.js` touches `Modal.getInstance(modal)` (`:47`) and `bsModal.hide()` (`:49`). **No constructor, no `show`, no `dispose`.** §10.4 already ruled that Packet C builds its own, smaller fake and that **no shared helper file is authorised** — this honours that, and the fake is **not** a copy of `FakeToast` |

**None of the four factories may use `importActual`.** A partial mock would let real collaborator code
execute, which would (a) break the coverage arithmetic in §11.9 and (b) make `toast.js`'s already-100 %
numbers move for reasons unrelated to Packet C. Recorded as **§11.11-R10**.

**The `Modal` fake, in full** — smaller than Packet B's by design:

```js
let currentModalInstance;   // what Modal.getInstance() returns; null by default.
                            // Read at CALL time, so a case controls what :47 sees.

const modalInstance = () => ({ hide() { calls.push('Modal.hide'); } });

beforeEach(() => {
    calls = [];
    currentModalInstance = null;
    globalThis.bootstrap = {
        Modal: {
            getInstance: (el) => { calls.push('Modal.getInstance'); getInstanceArgs.push(el); return currentModalInstance; },
        },
    };
});

afterEach(() => { delete globalThis.bootstrap; });   // never leak the global into another file
```

Two details are load-bearing and are stated so they are not re-derived:

1. **The "already present" instance is a plain object, never a constructed fake.** There is no
   constructor in this fake at all — `exercises.js` never constructs a `Modal` — so the §10.4 hazard
   that made `makeInstance()` necessary (an arrange-time `'construct'` entry corrupting the log) cannot
   arise. It is recorded anyway, because the *reason* it cannot arise is a measurement about the module,
   not a general truth.
2. **`getInstance` records the element it was handed** (`getInstanceArgs`), which is how C18 asserts
   `Modal.getInstance` received the `#clearPlanModal` element **by identity** rather than merely being
   called. **CORRECTED 2026-08-22:** Plan v2 justified this by *"a call-count-only assertion would
   survive P21 (`if (modal)` → `if (true)`), which calls `getInstance(null)`"*. **That is C17's
   argument, not C18's** — C18's fixture *has* the modal, so `if (modal)` and `if (true)` are
   indistinguishable there, §11.8's own P21 row says *"C18/C19 stay green"*, and **P21 measured as
   killing C17 alone** (§11.17). The `getInstanceArgs` record is what makes **C17's** negative
   non-vacuous; in C18 it pins that `:47` is handed the `#clearPlanModal` node itself. **Both uses are
   real — only the attribution was wrong.**

**Console spies.** `console.error` and `console.log` are both spied with `mockImplementation(() => {})`
and their handles kept in variables — `console.log` because **C10's duplicate-guard oracle runs through
it** (`exercises.js:18`), and `console.error` because C1/C2/C8/C24 assert on it. `vi.restoreAllMocks()`
in `afterEach` restores both.

### 11.7 Anti-vacuity assertions — the cases that prove the file can fail

§4.5 requires each packet to break the behavior it claims to pin and confirm a red. Four distinct
mechanisms in this file could each pass while asserting nothing, and each has a case and a mutation
that proves otherwise:

| What could be vacuous | The case that proves it is not | The mutation that proves the case can fail |
|---|---|---|
| **The mocks** — if the handles the test asserts on are not the handles the module receives, the file asserts nothing *(the specific `resetModules` mechanism Plan v1 named for this **does not exist** — §11.15-M-a — but the property is real however it might arise)* | **C28** — identity equality against a freshly imported collaborator | **P39** — change only the four `vi.mock` **factory bodies** to return their own inline `vi.fn()`s, keeping the `h` object and every test-body reference. **The literal "delete the handles" form is NOT usable**: it fails at collection with a `ReferenceError` (§11.15-M-b), and §10.5's N1 lesson applies — *a mutation that cannot be loaded is not a mutation* |
| **The fixture and the `bootstrap` global** — C17's "modal absent" is meaningless if the modal was never present, and C18/C19 are meaningless against an uninstalled global | **C29** — `#clearPlanModal` is non-null at rest and `bootstrap.Modal.getInstance` is a function | **P38** — remove `#clearPlanModal` from the default fixture. This is the Packet C analogue of **M19** and **N30**, and one of only **two** rows that touch the test file |
| **The isolation strategy** — a `resetModules()` that does not actually produce a fresh `Set` would make C10–C14 pass by accident | **C15** — a trapped id is refused on one instance and accepted on a freshly imported one, in one self-contained case. *(Independently corroborated by `PROBE A3`, §11.15-M-c.)* | **P6** — delete `deletingExercises.add(...)` at `:22`; the trapped-id arrangement then cannot be established |
| **The concurrency oracle** — asserting "the guard works" via a call count is only meaningful if the count can move | **C10** (exactly one `api.post`) paired with **C11** (exactly two for different ids) and **C12/C13** (exactly two after release) | **P4**, **P5**, **P6** each make C10 read **two**. **P7** makes *both* C12 and C13 read **one**; **P8** makes **only C13** read one — C12 stays green, which is P8's whole stated purpose. *(Plan v1 said "P7, P8 each make C12/C13 read one", contradicting its own P8 row — council C-9; §11.8 was right, this table was wrong.)* **P41** makes C11 read **one** |

**Every negative assertion in §11.3 is paired**, per rule 1, and four of them are expressed as an
ordered-log **deep equality** (C9, C17, C18, C25) rather than as a `not.` — a deep equality on an array
is simultaneously the positive and the negative, and it cannot pass against a function that died on
line one.

### 11.8 Mutation matrix — prediction (**P1–P42**)

> **Plan v2 changed three things here, all from the council.** **P41** and **P42** are **appended**
> (council C-6) so no existing ID moves; **ten rows' kill sets were under-predicted and are corrected**
> (council C-3); and the **probe layout** — absent from Plan v1 and load-bearing — is now specified
> (council C-2). **P40 remains the sole declared equivalence**, and **P39 remains a live mutation**
> with a corrected form.

> **ID PREFIX — a deliberate deviation, recorded rather than silent.** The drafting instruction for this
> section specified `M1…Mn`. **`M1`–`M19` are already taken by Packet A** (§9.13; `M13` is the declared
> equivalent mutant and `M19` the anti-vacuity fixture row, both referenced from §10.5 and §10.7), and
> `N1`–`N32` by Packet B. Reusing `M` would make every existing cross-reference to `M13`/`M19`
> ambiguous — the same collision class this document already had to resolve administratively once
> (§2.6). Packet C therefore uses **`P`**, which is unused in this file. This is a labelling decision the
> packet can take for itself; it is **not** an owner question, and it is recorded here so the departure
> from the instruction is visible rather than inferred.

**Harness requirements — carried from §9.13-D3, §10.5 and the three defects execution found in §10.12.
All of them are mandatory; none is a suggestion.**

- **Judge every row by the runner's PROCESS EXIT CODE, never by a parsed failure count.** Measured in
  Packet B: **Vitest exits 1 while printing `Tests N passed` and zero failures** when an unhandled error
  occurs. A harness that greps for `failed` records that row as a **survivor** and hands back a
  fabricated test weakness.
- **Every row must report exactly 231 collected cases** (the predicted post-Packet-C total) or be
  recorded as a loud, distinct **`BAD RUN`** — never as a survivor. This is the rule §10.5 did not have
  and §10.12 defect 2 proved it needed: *a green run of the wrong suite is indistinguishable from a
  survivor if you only look at the exit code.* It applies to **all 42 rows**, including P38 and P39,
  neither of which changes the case count.
- **Include paths must be POSIX-separated and relative to `root`.** An absolute Windows path is not a
  valid glob and silently matches nothing (§10.12 defect 2).
- **Apply every mutation exactly once**; report **`NOT APPLIED`** otherwise. A mutation that fails to
  apply must never be recorded as "no tests red".
- **Normalise line endings before matching. EOL is MEASURED, not assumed** (§11.15-M-d, 2026-08-22):
  `git config core.autocrlf` → **`true`**, **no `.gitattributes` exists**, and `file` reports both
  `static/js/modules/exercises.js` and `static/js/modules/__tests__/toast.test.js` as **CRLF**. So this
  rule is about **authoring the patterns correctly**, not about discovering the EOL at run time.
  **The criterion is any pattern OR ANCHOR containing a line break — not "any mutation spanning
  lines"** (council C-7); Plan v1 used the narrower phrasing and under-counted. **Thirteen rows
  qualify: P3, P5, P8, P10, P14, P16, P19, P22, P25, P28, P33, P34, P40.** The three Plan v1 missed are
  **P10** and **P28** (single-line edits whose *anchors* span `:26-28` and `:54-56`, per the anchor
  table below) and **P14** (`fetchWorkoutPlan();` occurs at `:32` **and** `:60`, and the only stated
  discriminator is `:60`'s trailing comment — so the `:32` pattern must carry a line break to match
  exactly once). Verify these **first**; a `NOT APPLIED` among them is the expected symptom of skipped
  normalisation.
- **Mutate a COPY under the gitignored `artifacts/probe/`** (§11.1). The production file is never
  written to.
- **Run the FULL Vitest suite per row**, not just `exercises.test.js`.
- **Re-derive EVERY row's kill set against the eleven whole-log / cross-instance cases, not only
  against the case it was written for** (council C-3). **C1, C2, C7, C9, C10, C16, C17, C18, C19, C25**
  assert a **deep equality on the entire ordered log**, and **C15** asserts a **cross-instance
  `api.post` call count**; *(**C1 and C2 were missing from Plan v2's list of "nine"** — both assert
  `calls` deep-equals `['showToast']`, per §11.3's own oracle. Found at execution, corrected here, and
  it changed **no** measured result: no row red C1 or C2 unexpectedly, §11.17. §11.15-C-3's council
  record keeps its original wording, because a disposition record is history, not a live claim.)* any mutation that adds, removes or reorders a logged call, or that changes how many times
  `api.post` runs, reds **all** of them that reach it — regardless of which behavior the row was aimed
  at. Plan v1 derived kill sets per behavior and never swept them, which is precisely the §10.5 failure
  class that produced Packet B's N3/N10/N12/N25 corrections. The sweep is now a **stated harness
  requirement**, not a review artefact.
- **Assert byte-identity through git's own normalisation** — `rev-parse` vs `hash-object`, never a raw
  byte compare, which cries wolf on a CRLF checkout (§10.12 defect 3).
- **Compare each row's predicted red-ID set against the runner's JSON report**, not merely "went red /
  stayed green". Packet B's two over-broad-list corrections surfaced **only** because the harness did
  this; a harness recording pass/fail alone would have absorbed both silently.
- **An unexplained survivor is a test weakness and must be fixed.** A survivor is *equivalent* only once
  a reason is demonstrated — and the one predicted equivalence here is **declared in advance** (P40),
  not discovered as a mystery.

**Ambiguous patterns — anchors verified by reading `exercises.js` on `b52df68`.** Under the
match-exactly-once rule an under-anchored pattern reports `NOT APPLIED` rather than mutating:

| Pattern | Occurrences | Required anchor |
|---|---:|---|
| `return;` | **2** (`:13`, `:19`) | Match with the **preceding** line. **P3 and P5 differ only by that line** — this is the pair most likely to mis-apply, exactly as N25/N26 were in Packet B |
| `showErrorToast: false` | **2** (`:28`, `:56`) | P10 anchors on the preceding `showLoading: false,` **plus** the `"Content-Type"` double-quote form (`:26`); P28 on the single-quote form (`:54`) |
| `showLoading: false,` / `useDefaultHeaders: false` | **2 each** | Same quote-style discriminator |
| `fetchWorkoutPlan();` | **2** (`:32`, `:60`) | `:60` carries the trailing comment `// Refresh the table to show empty state`; `:32` does not |
| `console.error(` | **2** (`:11`, `:35`) *(plus `:67`)* — **3** total | Anchor on the message literal; all three differ |
| `result.message \|\|` | **2** (`:31`, `:59`) | Anchor on the fallback string, which differs |
| `catch (error) {` | **2** (`:34`, `:66`) | Anchor on the following `console.error` literal |
| `deletingExercises` | **4** (`:7`, `:17`, `:22`, `:38`) | Anchor on the method: `new Set()`, `.has(`, `.add(`, `.delete(` — all four differ |

#### How a mutated copy is LOADED — specified, because Packet B's mechanism does not transfer

**Plan v1 omitted this entirely** (council C-2, raised independently by `architecture-reviewer` and
`test-strategist`). §10.1 describes a harness that copies `toast.js` into `artifacts/probe/` and
*"points the run at"* it — and §10.1's own last row records **why that was enough**:
*"Collaborator mocks: **none**. `toast.js` imports nothing."* Packet C's file carries **five relative
specifiers that must all resolve at once**: `../exercises.js` plus the four `vi.mock` paths
(`../toast.js`, `../workout-plan.js`, `../workout-plan-events.js`, `../fetch-wrapper.js`). **Copying
the test file alone breaks the four mock paths; copying the module alone breaks `../exercises.js`.**
This is §10.12 defect 2 one level up — a wrong include path there silently ran the wrong suite and
**fabricated a survivor**.

**Required layout.** Mirror the real directory shape under the probe root, so every relative specifier
resolves by construction rather than by luck:

```
artifacts/probe/static/js/modules/
    exercises.js                  <- copy; mutated by P1–P37, P40, P41, P42
    toast.js                      <- pristine copy (mock path target)
    workout-plan.js               <- pristine copy
    workout-plan-events.js        <- pristine copy
    fetch-wrapper.js              <- pristine copy
    __tests__/
        exercises.test.js         <- copy; mutated by P38, P39 only
```

- **Module rows (P1–P37, P40–P42)** mutate the copied `exercises.js` beside a **pristine** copied test
  file. **Test-file rows (P38, P39)** mutate the copied `exercises.test.js` beside a **pristine** copied
  module. No row mutates both.
- The Vitest `include` is **POSIX-separated and relative to `root`**, pointing at
  `artifacts/probe/static/js/modules/__tests__/exercises.test.js` — never an absolute Windows path
  (§10.12 defect 2).
- **PRE-FLIGHT ROW, run before P1:** load the **pristine** probe copy and assert **all five specifiers
  resolve** and the run is green at **231 collected cases**. A harness that starts at P1 cannot tell a
  broken probe layout from a suite that legitimately reds — and would report the first several rows as
  killed for the wrong reason.
- The **231-collected-cases** assertion (above) remains the per-row check that the *right pair* loaded.
- The probe tree is discarded afterward, and `static/js/modules/exercises.js` is asserted unchanged
  **through git's own normalisation**.

---

| # | Line(s) | Deliberate break | Predicted to red |
|---|---|---|---|
| **`removeExercise` — missing-ID guard** | | | |
| P1 | `:10` | Condition replacement `!exerciseId` → `false` | **C1, C2** |
| P2 | `:12` | Drop the second argument: `showToast("Exercise ID is missing. Unable to remove exercise.")` | **C1, C2** — `toHaveBeenCalledWith` is arity-exact |
| P3 | `:13` | Delete the `return;` (**anchored on the preceding `showToast` line**) | **C1, C2** — execution falls through, `api.post` fires, and `calls` is no longer `['showToast']` |
| **`removeExercise` — the concurrent-delete guard** | | | |
| P4 | `:17` | Condition replacement `deletingExercises.has(exerciseId)` → `false` | **C10, C15** — `api.post` reads **2** in both; C15's blocked-call arm is no longer blocked *(C15 added by the C-3 sweep)* |
| P5 | `:19` | Delete the `return;` (**anchored on the preceding `console.log` line**) | **C10, C15** — the `console.log` still fires, so **only the call-count and ordered-log assertions kill this row**; a `console.log`-only oracle would let it survive *(C15 added by the C-3 sweep)* |
| P6 | `:22` | Delete `deletingExercises.add(exerciseId);` | **C10, C15** |
| P7 | `:38` | Delete `deletingExercises.delete(exerciseId);`, emptying the `finally` | **C12, C13** |
| P8 | `:37-39` | Move the `delete` **out of `finally`** into the `try`, after `:33` — so the guard is released on success but **not** on failure | **C13 only.** C12 stays green, which is the point: this is the row that proves C12 and C13 are not redundant |
| **`removeExercise` — the `api.post` contract** | | | |
| P9 | `:25` | `"/remove_exercise"` → `"/remove-exercise"` | **C3** |
| P10 | `:28` | `showErrorToast: false` → `true` | **C3.** In production this would **double-toast** — the wrapper would raise its own toast alongside `:31`/`:36`. The unit tier can only observe the *option value*, because `fetch-wrapper.js` is mocked; that limitation is stated rather than dressed up |
| P11 | `:25` | Body `{ id: exerciseId }` → `{ exerciseId }` | **C3** |
| **`removeExercise` — success effects** | | | |
| P12 | `:31` | Drop the `\|\| "Exercise removed successfully!"` fallback | **C5** |
| P13 | `:31` | `result.message \|\| <fallback>` → `<fallback>` (always the fallback) | **C4** |
| P14 | `:32` | Delete `fetchWorkoutPlan();` — **the pattern must carry a line break** to disambiguate `:32` from `:60` (EOL row) | **C7, C10, C16** — C10's oracle includes the whole-log deep equality *(C10 added by the C-3 sweep)* |
| P15 | `:33` | Reason `'remove-exercise'` → `'clear-workout-plan'` | **C6.** Not C7/C9/C16 — the ordered log records **labels, not arguments**, which is why C6 exists as a separate row |
| P16 | `:32-33` | Swap the order of `fetchWorkoutPlan()` and `notifyVolumeAffectingPlanChange(...)` | **C7, C10, C16** *(C10 added by the C-3 sweep)*. **CHARACTERIZATION-ONLY ordering** (council C-17): nothing requires `fetchWorkoutPlan` before `notifyVolume` — the sole listener is 150 ms-debounced (§11.2) — so a red here means *"confirm intent"*, not *"a user-visible defect"* |
| **`removeExercise` — error path** | | | |
| P17 | `:36` | `${error.message}` → `${error.code}` | **C8** |
| P18 | `:36` | Drop the `true` second argument | **C8** |
| P19 | `:35-36` | Delete the `showToast` line at `:36` | **C8, C9** |
| P20 | `:35` | Delete the `console.error` line | **C8** |
| **`clearWorkoutPlan` — the three modal branches** | | | |
| P21 | `:46` | `if (modal)` → `if (true)` | **C17** — `Modal.getInstance` is called with `null`. **C18/C19 stay green**, so C17 is this row's only killer, and its `getInstanceArgs` identity assertion (§11.6) is what makes it non-vacuous |
| P22 | `:45-51` | Delete the whole modal block | **C18, C19, C25** *(C25 added by the C-3 sweep — its log loses `'Modal.getInstance'` and `'Modal.hide'`)* |
| P23 | `:48` | `if (bsModal)` → `if (true)` | **C18 — and it reds by TypeError routed through the module's own `catch`.** `null.hide()` throws at `:49`; the `try` opened at `:43` catches it at `:66`, so `api.post` never runs and C18's trailing ordered-log entries are absent. **This is precisely why C18 carries positive pairing** — a `hide`-not-called assertion alone would pass on the mutant |
| P24 | `:49` | Delete `bsModal.hide();` | **C19, C25.** **NOT unit-only** (council C-12): `ui-hardening.spec.ts:1018` asserts `#clearPlanModal` loses its `show` class, so E2E would red too. Plan v1 implied the unit tier was this line's sole guard; it is not |
| P25 | `:45-51` | Move the whole modal block to **after** `api.post` (`:58`) | **C18, C19, C25** *(C18 added by the C-3 sweep — its log's `'Modal.getInstance'` moves after `'api.post'`)*. On C25's error arrangement the modal is never closed at all, so its log becomes `['api.post','showToast']`. **CHARACTERIZATION-ONLY ordering** (council C-17): closing the modal before or after the request is not observably different in production |
| **`clearWorkoutPlan` — the `api.post` contract** | | | |
| P26 | `:53` | `'/clear_workout_plan'` → `'/clear-workout-plan'` | **C20** |
| P27 | `:53` | Body `null` → `{}` | **C20** — the row that proves C20 distinguishes `null` from an empty object |
| P28 | `:56` | `showErrorToast: false` → `true` | **C20** |
| **`clearWorkoutPlan` — success effects and CALL ORDER** *(relabelled from "the ORDERING contract" — council C-1)* | | | |
| P29 | `:59` | Drop the `\|\| 'Workout plan cleared successfully!'` fallback | **C22** |
| P30 | `:59` | `result.message \|\| <fallback>` → `<fallback>` (always) | **C21, C26** |
| P31 | `:61` | Reason `'clear-workout-plan'` → `'remove-exercise'` | **C23** |
| P32 | `:65` | Delete `resetWorkoutControlsToDefaults();` | **C17, C18, C19** *(C17 and C18 added by the C-3 sweep — both logs end in `'resetControls'`)* |
| **P33** | `:60`, `:65` | **Move `resetWorkoutControlsToDefaults()` from `:65` to BEFORE `fetchWorkoutPlan()` at `:60`** | **C17, C18, C19** *(C17 and C18 added by the C-3 sweep; Plan v1 said "C19 only", which was wrong — all three assert the whole log)*. **RELABELLED BY PLAN v2 — this is CHARACTERIZATION, not a criterion-4 contract** (council C-1). The cross-tier fact **stands**: no other tier can red it, because `ui-hardening.spec.ts:996-1034` asserts the **end state**. The product claim **does not**: `fetchWorkoutPlan()` touches no workout control (`workout-plan.js:90-117`), so this reordering is **not observable in production**. The criterion-4 property that *is* real — reset only after a successful `api.post`, never on error — is pinned by C19's `api.post`→`resetControls` relation and by **C25** |
| P34 | `:60-65` | Move `resetWorkoutControlsToDefaults()` into a `finally`, so it also runs on the error path | **C25** — its log gains `'resetControls'`. **This is the criterion-4 mutation that matters**: unlike P33 it breaks a property KI-005 actually states |
| **`clearWorkoutPlan` — error path** | | | |
| P35 | `:68` | `${error.message}` → `${error.code}` | **C24** |
| P36 | `:68` | Drop the `true` second argument | **C24** |
| **The un-awaited refresh** | | | |
| P37 | `:60` | Add `await` before `fetchWorkoutPlan()` | **C27.** It reds **by timeout**, not by assertion — C27's mock never settles, so `clearWorkoutPlan()` never resolves. C27 carries a **pinned 1000 ms per-case timeout** (§11.11-R11), so this row costs the matrix **one second**, not the default five |
| **Test-file rows — anti-vacuity (2 of 42)** | | | |
| **P38** | *fixture* | **Remove `#clearPlanModal` from the default fixture in `exercises.test.js`** | **C29**, plus **C18, C19** (which need the node) and **C25** *(added by the C-3 sweep — with no modal, its log loses `'Modal.getInstance'` and `'Modal.hide'`)*. The Packet C analogue of M19 and N30 |
| **P39** | *mock wiring* | **Change ONLY the four `vi.mock` factory bodies to return their own inline `vi.fn()`s**, keeping the `h` object and every test-body reference intact. **FORM CORRECTED BY PLAN v2** (council C-5): the literal "delete the handles" form **cannot be loaded** — it throws `ReferenceError: Cannot access '<name>' before initialization` at collection and the file reports `(0 test)` (§11.15-M-b), and §10.5's N1 lesson applies: *a mutation that cannot be loaded is not a mutation*. Apply as four anchored single-line edits, or as a whole-file mutant **with its oid recorded** | **C28**, plus **every row asserting positively on a mocked collaborator** — predicted **C1–C27** *(C15 added by the C-3 sweep; only C29, which asserts on the fixture and the `bootstrap` global, is expected to stay green)*. **Deliberately over-broad**: its purpose is to prove the mock wiring is load-bearing, and a narrow kill set would understate it. **Still a LIVE mutation, not an equivalence** — C28 compares the `h.*` handles against the freshly imported collaborator exports, so under this form that identity assertion genuinely reds |
| **Declared equivalent, in advance — ONE row, unchanged by Plan v2** | | | |
| **P40** | `:22`, `:24` | **Move `deletingExercises.add(exerciseId);` from `:22` (before the `try`) to the first statement INSIDE the `try`** | **(none) — predicted EQUIVALENT.** Derived from the code, not asserted: there are **no** statements between `:22` and the `try` at `:24`, `Set.prototype.add` cannot throw, and the `finally` at `:37` drains the key on **every** exit path from the `try`. So the two placements are indistinguishable through the public API. If P40 survives **and** that reasoning holds under measurement, it is recorded as an equivalent mutant exactly as M13 (§9.13-D2) and N13 (§10.5) were — **not** chased with a contorted test |
| **Appended by Plan v2 — intended as isolating killers for two orphaned cases** *(council C-6; IDs appended so nothing renumbers. **Measured: only P42 isolates** — §11.17)* | | | |
| **P41** | `:17` | **`deletingExercises.has(exerciseId)` → `deletingExercises.size > 0`** — the realistic broken-guard shape a developer writes when reaching for "is a delete in flight?" | **Predicted C11 only; MEASURED C11 *and* C14** (§11.17). A concurrent delete of a **different** id is now wrongly blocked, so C11's `api.post` reads **1**, not 2 — and C14's second call, which passes `'1'` while `1` is in flight, is blocked for the same reason. C10 is unaffected (same id, still one post) and C12/C13 are sequential, so the `Set` is empty by the second call. **Two claims in this cell were wrong and are corrected rather than deleted**: it does not kill C11 *only*, and it is not *"C11's first and only killer"* — **P11 already red C11**, because C11 asserts the request **bodies**. P41's real value is that it is the only row expressing the **broken-guard shape**; it **isolates nothing** |
| **P42** | `:10` | **`!exerciseId` → `exerciseId == null`** — the exact "fix" a developer writes when told the falsy guard is too broad | **C2 only.** `0` now passes the guard and reaches `api.post`; `undefined` still does not, so C1 stays green. **This is what distinguishes C2 from C1**, and it closes the consistency gap §11.3's declined-cases note names: Plan v1 declined `null`/`''` for adding no kill while keeping a C2 that added none either |

**Rows: 42 — 40 mutating `exercises.js`, 2 mutating `exercises.test.js` (P38, P39), of which exactly 1
is a declared equivalence (P40).** *(Plan v1: 40 rows / 38 module. **P41** and **P42** are appended, so
no existing ID moved.)* Stated in this form because §10.9 recorded that *"32 mutations of `toast.js`"*
was really 31 of the module plus one of the test file, and the ambiguity cost a correction.

**Cases with no *isolating* killer — DISCLOSED, and the list grew twice.** (Council C-6 grew it first.)
Plan v1 named **two**; Plan v2 said **four**; **measurement says FIVE** — C16, C26, C12, C14 **and C11**
(§11.17). Only **C2** was genuinely closed, by P42:

| Case | Status | Why |
|---|---|---|
| **C16** | **No isolating killer — accepted** | Always co-killed with C7 (P14, P16 red both). It pins *DOM independence*, which **no** mutation of `exercises.js` can express, because the property is the **absence** of a `document` reference. The B23/B43 idiom from §10.5 |
| **C26** | **No isolating killer — accepted** | Always co-killed with C21 (P30). It documents the KI-010 boundary; that boundary is its value, not additional mutation coverage |
| **C12** | **No isolating killer — accepted** | Never separated from C13: **P7** reds both, and **P8** reds only C13. A mutation that released the guard on *failure* but not on *success* would isolate C12 — it is not written, because that shape has no plausible authorship (nobody moves a `delete` into a `catch` only) |
| **C14** | **No isolating killer — accepted.** *(Plan v2 said "killed by no mutation of `exercises.js` at all"; **MEASURED FALSE at execution** — **P41 reds C14** as well as C11, §11.17. The row is corrected to the claim that survives measurement.)* | Never separated from C11: **P41** reds **both**, and no row reds C14 alone. A mutation that made the `Set` key type-insensitive (e.g. `String(exerciseId)`) would isolate it — **not written**, because it would pin the coercion *fix* as a defect, and C14 is explicitly characterization (§11.11-R4) |
| **C11** | **No isolating killer — accepted.** *(Plan v2 struck this row as "CLOSED by P41"; **MEASURED FALSE**, §11.17 — **P41 reds C11 AND C14**, and **P11 reds C3 AND C11**. Restored to the table.)* | No row reds C11 alone. **Plan v2's premise was also wrong in the other direction**: it said C11 was "killed by **no** mutation of `exercises.js`", but **P11** (`{ id: exerciseId }` → `{ exerciseId }`) already red it — C11 asserts the **request bodies**, not only the call count, and the C-3 sweep never looked at argument-shape oracles. P41 is still worth its place — it is the only row that expresses the *broken-guard* shape — but it **isolates nothing** |
| ~~C2~~ | **CLOSED by P42 — confirmed by measurement** (P42 reds **C2 only**, §11.17) | Was never distinguished from C1 |

**One named gap, recorded and deliberately not closed.** `:48`'s `if (bsModal)` is equivalent to
`if (bsModal != null)` **under this fake**, because `getInstance` is arranged to return only an object
or `null` — which is what real Bootstrap returns. A mutation between the two forms would therefore be
equivalent *for the wrong reason*: not because the code is insensitive, but because the fake is. It is
**not** written as a mutation row, and the reason is recorded here so a later reader does not add it and
mistake a fake-shaped equivalence for a code-shaped one.

### 11.9 Expected coverage movement — **PREDICTION, recorded and never gated**

D1 is signed as **non-blocking measurement**, so nothing below is a gate. Both arms must be measured
**in this worktree on this base** at execution time, so the movement is a real difference rather than a
figure carried from another run — the discipline §10.12 established.

**Per-file, `exercises.js`** (denominators measured 2026-08-22; the target is a **prediction**):

| | Denominator (measured) | Predicted after Packet C | Reasoning |
|---|---:|---|---|
| Statements | **30** | **30/30 = 100 %** | Both exports are driven end to end, including both `catch` blocks (C8, C24) and the `finally` (C12, C13) |
| Lines | **30** | **30/30 = 100 %** | Same |
| Functions | **2** | **2/2 = 100 %** | The module has exactly two functions, both exported |
| Branches | **12** | **12/12 = 100 %** | Six binary branches, both arms of each: `!exerciseId` (C1/C2 vs C3), `.has()` (C10 vs C3), `result.message \|\|` at `:31` (C4 vs C5), `if (modal)` (C19 vs C17), `if (bsModal)` (C19 vs C18), `result.message \|\|` at `:59` (C21 vs C22). **Independently confirmed achievable by two council reviewers**, who also both confirmed that `try`/`catch`/`finally` contribute **no** branch under this provider — so the `catch` blocks add statements, not branch denominators |

**Suite totals — arithmetic on the measured baseline, all four figures PREDICTIONS:**

| | Measured baseline (`b52df68`) | Predicted with Packet C | Predicted movement |
|---|---|---|---|
| Statements | 7.4 % (**552**/7453) | (552+30)=**582**/7453 = **7.81 %** | **+0.40 pp, +30** |
| Branches | 10.22 % (**475**/4644) | (475+12)=**487**/4644 = **10.49 %** | **+0.26 pp, +12** |
| Functions | 7.29 % (**81**/1110) | (81+2)=**83**/1110 = **7.48 %** | **+0.18 pp, +2** |
| Lines | 7.16 % (**498**/6946) | (498+30)=**528**/6946 = **7.60 %** | **+0.43 pp, +30** |

> **Two of the four movements were rounded the wrong way in Plan v1, and two reviewers caught the same
> pair with the same figures** (council C-15). Branches is **10.2282 → 10.4867 = +0.2585 pp**, which
> rounds to **+0.26**, not +0.27; lines is **7.1697 → 7.6015 = +0.4318 pp**, which rounds to **+0.43**,
> not +0.44. Both were computed from the *displayed* two-decimal percentages instead of from the
> counts. **Statements (+0.40) and functions (+0.18) were correct, and all four predicted values
> (7.81 / 10.49 / 7.48 / 7.60 %) were and remain correct** — only the deltas moved. Recorded because a
> derived figure computed from a rounded input is a distinct error class from a wrong measurement, and
> it is the one nobody re-checks.

**Two stated assumptions this arithmetic rests on**, either of which failing makes the prediction wrong
rather than the packet wrong:

1. **The denominators do not move.** `all: true` in the coverage config means every file under
   `static/js` is counted whether or not a test touches it, so adding a **test** file changes no
   denominator. Verified in principle by Packet B, whose denominators (7453 / 4644 / 1110 / 6946) are
   identical before and after in §10.12's table.
2. **No other file's covered count moves.** This holds **only** while all four collaborator mocks are
   total (§11.11-R10). An `importActual` anywhere would execute real collaborator code and move
   `toast.js`, `workout-plan.js`, `workout-plan-events.js` or `fetch-wrapper.js` — at which point the
   totals above are wrong and the **cause is the mock, not the module**.

**If the measured movement differs, it is investigated before any figure here is edited** (§10.7-R9).

### 11.10 Gates

| Gate | Command | Expectation |
|---|---|---|
| Baseline | `npm run test:js` | **12 files / 202 cases** — **measured** 2026-08-22 on `b52df68` |
| With Packet C | `npm run test:js` | **13 files / 231 cases** — exactly **+29** (§11.3), **and** all four checks (i)–(iv) below. Any other delta means either an existing test moved (a defect) or the new file did not resolve to 29 reported cases (also a defect) |
| Coverage | `npm run test:js -- --coverage` | Both arms measured in this worktree; movement **recorded, never gated** (§11.9) |
| Mutation | §11.8, **full suite per row**, against copies under `artifacts/probe/` **in the mirrored layout §11.8 specifies**, after the **pre-flight row** passes | All **42** rows behave as predicted; **P40 survives as declared equivalent**; every other survivor is a test weakness and is fixed |
| Inventory | `.venv/Scripts/python.exe scripts/generate_test_inventory.py --check` | **"Test inventory is up to date"**, exit 0 — **derived below, not assumed**. **Do not regenerate** |
| Targeted E2E | See the non-empty-union resolution below — **this is where Packet C differs from Packet B** | |
| CI | all required contexts green | **18/18**, and `js-unit` stays **non-required** |

**The four pinned count checks** (§10.6 i–iv, restated for Packet C's numbers, because §10.6's
measurement stands: **the parenthesised total includes skipped and todo**, so a bare `231` proves
nothing — a file with 27 real cases and two `.todo` stubs satisfies it while asserting nothing):

| # | Check | Why it is not redundant |
|---|---|---|
| **i** | A **focused** run of `exercises.test.js` reports **29 passed / 29 total in 1 file** | Isolates the new file from the rest of the suite |
| **ii** | `npm run test:js` reports **13 files / 231** | Proves no existing file moved |
| **iii** | **Zero** skipped, **zero** todo and **zero** filtered in **both** runs | The total alone cannot see a `.skip` or a `.todo` |
| **iv** | A grep asserting the new file contains **no** `.only`, `.skip`, `.todo` — and **no `it.each`** unless its expansion is counted | Catches the defect at source rather than in a number. **Reported cases ≠ `it(` call sites**: measured in Packet B, 145 call sites produced 155 reported cases because two `it.each` blocks expand. **Packet C plans no `it.each`**, so `29 it(` call sites should equal 29 reported cases; if the implementer introduces one, the expansion must be counted and this check updated in the same change |

**Why `Test Inventory Drift` stays green — the derivation, walked one surface at a time, not asserted.**
[`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) pins **five** surfaces. Against the single file this
packet adds, `static/js/modules/__tests__/exercises.test.js`:

| Pinned surface | Trip condition (QUALITY_GATE) | Packet C |
|---|---|---|
| Per-file pytest node counts | add/remove/rename/move under `tests/**` | **No** — nothing under `tests/**` |
| Per-spec Playwright counts | add/remove/rename in `e2e/**/*.spec.ts` | **No** — Packet C **runs** specs but adds, removes and renames none |
| `waitForTimeout` lines per file | add/delete a hard wait in `e2e/**/*.ts` | **No** |
| Required functional spec set | the `e2e-functional-shard` spec list in `ci.yml`, or a rename of that job | **No** — `.github/workflows/**` is on the do-not-touch row (§11.1) |
| Parametrized configuration surface | **adding or deleting** a file under `.claude/commands/`, `.claude/agents/`, `.claude/rules/`, or **`docs/ai_workflow/`** | **No** — the new file is under `static/js/`, and this plan lives under **`docs/testing_phase3/`**, which is *not* `docs/ai_workflow/`. Editing an existing file in place does not trip it either. **Note this is exactly why §11.13's feature-map question is routed to the owner rather than self-resolved**: `QUALITY_GATE.md` is under `docs/ai_workflow/`, and while *editing* it would not trip the gate, it is a shared canonical document on the do-not-touch row |

Confirmed from the other direction as well, and **re-measured on `b52df68`, not carried from §10.6**:
`docs/test_inventory/TEST_INVENTORY.json` and `.md` contain **zero** matches for `vitest`, `test:js` or
`static/js`. **Packet F has not landed, so Vitest nodes are unpinned and adding a Vitest file cannot
move a pinned count.** This statement expires the moment Packet F merges (§5's own expiry note).

**Two required checks, confirmed non-applicable by reading the config on `b52df68`:**

| Required check | Why Packet C cannot trip it |
|---|---|
| `Type Check (tsc blocking + pyright measure-only)` | `tsconfig.json`'s `include` is **`["e2e/**/*.ts", "playwright.config.ts"]`**, with **no `allowJs` and no `checkJs`**. A new `.js` file under `static/js` is **outside the TypeScript program entirely**. The pyright half triggers on `.py`; Packet C adds none |
| `Code Linting` | The job runs **`flake8` only** — a **Python** linter — and **`package.json` defines no JS lint script**, so no JS file can fail it |

**And, measured: `.github/workflows/ci.yml` has ZERO `paths:` / `paths-ignore:` filters**, so every PR
runs every job. Whatever is decided locally, **the full Chromium matrix runs in CI regardless.**

**A SIXTH surface, unwalked by Plan v1 and by Packet B's precedent: pytest contract tests that glob
`static/js/**/*.js`** (council C-19). These are not part of QUALITY_GATE's five pinned surfaces, so
inheriting Packet B's derivation silently would have skipped them — and they run inside the **required**
full-pytest gate, where a hit is a red, not a warning.

| Contract test | Globs `static/js/**/*.js` | Excludes `__tests__`? | Forbidden token it scans for |
|---|---|---|---|
| `tests/test_visual_selector_contracts.py:76-80` | Yes | **No** | `data-visual-preserve-border` |
| `tests/test_css_wp4_4_base_contracts.py:44` | Yes | **No** | `loading-spinner` |
| `tests/test_css_display_utilities_contracts.py:82` | Yes | **Yes** | — (excluded, cannot see the file) |
| `tests/test_css_wp4_4_layout_contracts.py:524` | Yes | **Yes** | — (excluded, cannot see the file) |

**Two of the four will read `exercises.test.js`.** Both are **forbidden-token scans**, and the tokens
are `data-visual-preserve-border`, `loading-spinner` and `fade-enter` — none of which a test of
`exercises.js` has any reason to contain. **So Packet C is safe**, but it is safe *because of an
authoring constraint*, not by structural exclusion, and that constraint is now stated rather than left
implicit: **`exercises.test.js` must not contain the strings `data-visual-preserve-border`,
`loading-spinner` or `fade-enter`** — including inside comments, which a token scan does not skip. A
future JS test that legitimately needed one of those strings would red the **required** pytest job with
a failure message about CSS contracts, which is exactly the kind of surprise this table exists to
prevent.

---

#### The targeted-test union is **NON-EMPTY**, and Packet B's override does **not** transfer

**This is the one gate where copying §10.6 verbatim would be wrong, and the difference is measurable.**
Packet B could argue an *empty* union because `QUALITY_GATE.md`'s frontend feature map has **no `toast`
row**. It **has** an `exercises` row — `QUALITY_GATE.md:114`:

```
| `workout_plan`, `workout-plan`, `filters`, `exercises`, `routine-cascade` | `workout-plan.spec.ts`, `exercise-interactions.spec.ts`, `superset-edge-cases.spec.ts` |
```

Under the *Frontend (JS)* row, a file matching the hint `exercises` maps to **three** Chromium specs.
The union is therefore **non-empty**, and `QUALITY_GATE.md:107`'s *"Run the union. If the union is
empty, run `/verify-suite`"* resolves to **run the union** — not to an escalation, and **not** to
Packet B's override, which was reasoned entirely from emptiness. **Asserting an empty union here would
be false.**

**RECOMMENDATION — run the mapped union in full: all three specs, locally, Chromium.** No override is
taken, and none is needed. This is *strictly stronger* than Packet B's position and it costs local
minutes and nothing else. Two supporting notes, neither of which is used to shrink the union:

- Of the three, only **two are topical**: `exercise-interactions.spec.ts` and
  `superset-edge-cases.spec.ts` are precisely the two specs FINDING-C-E2E measured as reaching
  `removeExercise()`. **`workout-plan.spec.ts` contains ZERO references to `removeExercise` or
  `clearWorkoutPlan`.** It is **still run**: the map routes by *feature hint*, not by symbol, and
  dropping a mapped spec on a symbol grep is exactly the reasoning that produced the §1.3 over-count
  this plan had to correct. A cheap run is not worth a clever exemption.
- Running these specs adds, removes and renames **no** spec file, so the inventory derivation above is
  unaffected (`e2e/**` surfaces trip on *file* changes, not on executions).

**A REAL GAP IN THE FEATURE MAP, found by this derivation and routed to the owner, not fixed.** The
mapped three include **no spec that exercises `clearWorkoutPlan()`**. The sole spec that does is
**`ui-hardening.spec.ts:996-1034`** (FINDING-C-E2E), and **nothing in the map routes to it** — there is
no `clear-plan` or `ui-hardening` hint anywhere in the table. So a literal, fully-compliant reading of
`QUALITY_GATE.md` selects three specs for a module whose **second export is covered by none of them**.
That is a defect in the map, not in this packet, and **Packet C may not edit `QUALITY_GATE.md`**
(§11.1). It is **§11.13 question 3**, with the packet's recommendation being: run the mapped three
**plus `ui-hardening.spec.ts`**, and record the map gap as a separate follow-up item.

> **Plan v2 strengthens the case for adding `ui-hardening.spec.ts` to the local run** (council C-12).
> Plan v1 described that spec as asserting only KI-005's end state. It also asserts, at **`:1018`**,
> that the modal actually closes — `await expect(page.locator('#clearPlanModal')).not.toHaveClass(/show/, …)`.
> So it is the only spec covering **any** part of `clearWorkoutPlan()`'s modal handling, and **P24**
> (`delete bsModal.hide();`) would red it. Question 3 was being argued about a spec the plan described
> incompletely; with the full description, "run it too" is the cheaper and better-supported answer.

### 11.11 Risks and behavioral ambiguities

| # | Risk / ambiguity | Disposition |
|---|---|---|
| **R1** | ~~The `resetModules()` mock-identity trap.~~ **WITHDRAWN — the risk does not exist.** Plan v1 claimed an inline `vi.mock` factory re-runs on the fresh registry, stranding the test file's bindings, with an "asymmetric failure / negatives pass vacuously forever" consequence | **MEASURED FALSE, §11.15-M-a.** In Vitest 4.1.11 `vi.resetModules()` does **not** re-run the factory; the registry survives it and the test file's binding stays wired to the freshly imported module (`topLevel call count = 2`). **The row is withdrawn rather than deleted**, because a plan that quietly drops a risk it argued from teaches nothing. **What replaces it: `vi.hoisted()` is still mandatory** because a factory referencing a plain top-level `const` throws `ReferenceError` at **collection** and the file reports `(0 test)` (§11.15-M-b). **C28 and P39 both survive** on the narrower, real property — the handles the test asserts on must be the handles the module receives |
| **R2** | **`deletingExercises` (`:7`) has no exported reset**, so §4.1 is **not** discharged by absence as it was for Packet B | Discharged **explicitly** in §11.5 and recorded there as a finding **about the module**. Packet C does **not** propose adding a reset — that is a production change |
| **R3** | **`api.post` rejects with a PLAIN OBJECT, not an `Error`** (`fetch-wrapper.js:51-91`, thrown `:216`, `:249`) | Every rejection fixture in §11.3 is `{ code, message, requestId }`. **A `new Error(...)` fixture would test a shape production never produces** — recorded as a hard authoring rule (§11.3 rule 2), not a preference |
| **R4** | **`Set` keys are type-sensitive** — `1` and `'1'` are different guard keys, so both would proceed | **CHARACTERIZATION, not a bug report** (C14). **No in-app call site passes a string** — `workout-plan-table.js:419` interpolates a bare `${exercise.id}` — but `removeExercise` is **also a `window` global** (`static/js/app.js:36`), so Plan v1's *"production always passes a number … not reachable today"* **overstated it** (council C-18). The corrected claim is bounded to in-app call sites. **Whether it earns a KI row is §11.13 question 4** — Packet C **may not edit `UI_SCENARIOS_GAP_ANALYSIS.md`** and cannot self-resolve it |
| **R5** | **Vitest 4.1.11's `configLoader: 'native'` warning** appears on every run and could be misread as a Packet C regression | **Pre-existing on `b52df68`, warning only, exit 0, 202/202 pass** (§11.2). **Packet C must NOT fix it** — `vitest.config.js` is on the do-not-touch row. Recorded so a future reader attributes it to the dependabot bump (#408) |
| **R6** | **Line endings — now MEASURED, upgraded from Plan v1's "assumed"** (§11.15-M-d) | **Three facts, 2026-08-22:** `git config core.autocrlf` → **`true`**; **no `.gitattributes` exists**; `file` reports both `static/js/modules/exercises.js` and `static/js/modules/__tests__/toast.test.js` as **CRLF**. So the risk is no longer *discovering* the EOL — it is **authoring the patterns correctly**. §11.8 names **thirteen** rows whose pattern **or anchor** contains a line break (P3, P5, P8, **P10**, **P14**, P16, P19, P22, P25, **P28**, P33, P34, P40) — Plan v1 listed ten and used the narrower "spans lines" criterion (council C-7). A `NOT APPLIED` among them is the expected symptom of skipped normalisation. **Forward-looking instruction, unchanged: author `exercises.test.js` as CRLF** to match its three jsdom siblings, or it checks out phantom-modified (§10.12) |
| **R7** | **The targeted-test union is non-empty**, unlike Packet B's | §11.10 resolves it by **running the mapped three**, taking **no override**. Packet B's emptiness argument is explicitly **not** reused. **RULED AT GATE 1 (§11.16 ruling 3): the local gate is the mapped three PLUS `ui-hardening.spec.ts`** — §11.10's own recommendation, and what §11.17 ran (**four specs, 111 passed**). This row said "three" and is annotated rather than rewritten |
| **R8** | Ordered-log assertions are stricter than behavior requires — a refactor that preserves semantics but reorders calls will red C7/C9/C16/C17/C18/C19/C25 | **REFRAMED BY PLAN v2** (council C-1 and C-17). Plan v1 justified the strictness by claiming the `reset`-last ordering *"**is** KI-005 criterion 4"*. **It is not** — criterion 4 says the reset runs after the *successful server clear* and that its own "LAST" is internal to the helper (`ki005_controls_persistence/PLANNING.md:448`; `workout-plan.js:408-413`). Measured, **no** ordering among `fetchWorkoutPlan`, `notifyVolume` and `resetControls` is observable in production: `fetchWorkoutPlan()` touches no control, and the sole listener is 150 ms-debounced. **So every ordered-log relation except `api.post` → `resetControls` is CHARACTERIZATION**, named as such at C19, **P16**, **P25** and **P33**, and a red means *"confirm intent"*, never *"a user-visible defect"*. **The one contract relation** — reset only after a successful post, never on error — is pinned by C19's `api.post`→`resetControls` position and by **C25**. **All four expected arrays remain PREDICTIONS** and must not be edited to match execution without investigation (§10.7-R9) |
| **R9** | The `bootstrap.Modal` fake could leak between test files, or drift toward a copy of Packet B's `Toast` fake | `delete globalThis.bootstrap` in `afterEach`. Only `toast.test.js` also uses the global, and the full suite runs per mutation, so a leak would surface. **No shared helper file is created** (§10.4's ruling); the fake is deliberately smaller — `getInstance` and `hide`, nothing else |
| **R10** | **A partial mock (`importActual`) would silently execute real collaborator code**, breaking §11.9's arithmetic and moving `toast.js`'s post-Packet-B numbers for unrelated reasons | Forbidden outright in §11.6. If the coverage totals differ from §11.9's prediction, **check the mocks before blaming the module** |
| **R11** | **C27's never-settling mock plus P37 (`await` added at `:60`) reds by TIMEOUT, not by assertion** — and it is the **only** case in the file with a wall-clock oracle | **The timeout is PINNED AT 1000 ms, not left as "short"** (council C-8). Plan v1's *"an explicit short per-case timeout"* is an aspiration, not a value, and the tempting 50–100 ms **can red against correct code on a loaded CI box** — a flake in the one suite whose entire purpose is qualifying for promotion. **1000 ms is chosen because the pristine path resolves in ~1 ms**, so it cannot flake, while still bounding P37's cost to **one second** instead of Vitest's default five. A future reader seeing this row time out must read it as the mutation working, not as flake |
| **R12** | **§1.3 carried TWO false claims about this module**, and a reviewer weighing the packet against either would misjudge it | Both corrected in place and dated (§11.2, *Corrections applied*, rows 1 and 2): the **E2E count** was 3× too high, and the **KI-005 criterion-4 attribution** was an over-read that Plan v1 then built C19 and P33 on. The measured picture — the behaviors with zero coverage at any tier, listed in §11.2 — is the packet's actual case |
| **R13** | **C26 could be misread as addressing KI-010** | It does not. Packet C **mocks `toast.js`**, so it cannot observe the collision's rendering at all; C26 pins only that `exercises.js:59` passes `result.message` through **verbatim**. **Commented as such in the test file**, and KI-010 stays `Open` and unmitigated in a document this packet may not edit |
| **R14** | The test declared at `exercise-interactions.spec.ts:218` is **wrapped in `if (count > 0)`** — **the guard is at `:225`, not `:218`** — and passes vacuously on an empty table, so one of the three "existing" `removeExercise` specs may assert nothing on a given run. **And there is a SECOND instance**, at `:212`, inside the test declared at `:204` — unmentioned by Plan v2, so the follow-up under-counted its own surface (re-measured 2026-08-22) | Recorded, **not fixed**: `e2e/**` is out of scope and changing that spec would be a second file. It is a further argument for the unit tier, and a candidate follow-up the owner may or may not want to open |
| **R15** *(new, council C-4)* | **`exercises.test.js` becomes the SOLE guard on five user-visible copy strings**, and Plan v1 never said so | Measured: `exercises.js:11, 12, 31, 36, 59, 68` carry literals that occur **nowhere else as exact literals** — and, decisively, **no E2E spec asserts any of them** *(re-verified 2026-08-22 by grepping `e2e/**`)*. **Narrowed 2026-08-22:** *"nowhere else"* unqualified overstated it — the server's copy at `routes/workout_plan.py:299`, `:305`, `:320` and `:323` is the **same user-visible phrasing**, differing by a trailing `!` or by the interpolation, which is exactly what §11.11-R17 discloses for C5 and C22. The claim that carries the protocol is the E2E half, and that half is exact. So a deliberate copy change reds **C1/C2** (`"Error: exercise ID is required…"`, `"Exercise ID is missing. Unable to remove exercise."`), **C5** (`"Exercise removed successfully!"`), **C8** (`'Unable to remove exercise: …'`), **C22** (`'Workout plan cleared successfully!'`) and **C24** (`'Unable to clear workout plan: …'`). **This is the exact condition that made Packet B's Gate 1 question 3 necessary** (asked §10.9, ruled §10.11: *"a deliberate copy change updates these tests in the SAME PR, and the red is the intended review signal"*). **Routed to the owner as §11.13 question 5**; the packet may not adopt the protocol unilaterally |
| **R16** *(new, council C-2)* | **The mutation probe must load a mutated copy alongside four mocked collaborator paths**, and Packet B's single-file mechanism does not transfer | §11.8 now specifies the **mirrored `artifacts/probe/static/js/modules/` layout**, which copy each row mutates, a **pre-flight row** asserting all five specifiers resolve before P1, and the standing **231-collected-cases** check. Without this, a broken layout is indistinguishable from a survivor — §10.12 defect 2, one level up |
| **R17** *(new, council C-10)* | **C5 and C22 pin fallback copy the real routes never render** | Disclosed on both rows: `routes/workout_plan.py:299` and `:320` always supply a `message`, and `utils/errors.py:36-37` forwards it whenever truthy, so `result.message` is always present and the `\|\|` fallbacks are unreachable through the real routes — differing from the server's copy **by a trailing `!`**. Same "defensive but unreachable" class Packet B disclosed for B15a/B15b. Pinned because the branch exists; **not** presented as user-visible behavior |
| **R18** *(new, council C-19)* | **Two pytest contract tests glob `static/js/**/*.js` without excluding `__tests__`**, so the new file is read inside the **required** full-pytest gate | Named in §11.10 with the token list. Packet C is safe **because of an authoring constraint, not structural exclusion**: `exercises.test.js` must not contain `data-visual-preserve-border`, `loading-spinner` or `fade-enter`, **including in comments**. Stated rather than inherited silently from Packet B's precedent |

### 11.12 File ownership, rollback boundary, and stop conditions

**Ownership.** Exactly **two** files may appear in the diff:
`static/js/modules/__tests__/exercises.test.js` (new) and
`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` (this plan and its later execution record). **A third
file in the diff voids §11.10's gate reasoning** and requires the gate set to be re-derived before
anything is committed.

**Rollback boundary.** The harness under `artifacts/probe/` is scratch, gitignored, and discarded after
the run. The production module is never written to; containment is asserted through git's own
normalisation, not around it. **If any mutation row reports the production file as changed, stop
immediately** — that is a harness containment failure, and §10.12's defect 3 is the reason the
assertion must be oid-based before it is believed.

**Stop conditions — report and do not proceed if any of these is true at execution time:**

1. **`static/js/modules/exercises.js` is not byte-identical to `b52df68`.** Every line number in
   §11.3 and §11.8 would need re-deriving.
2. **The baseline is not 12 files / 202 cases.** A moved baseline means an existing test changed and the
   `+29` arithmetic is no longer a proof.
3. **`toast.js`, `workout-plan.js`, `workout-plan-events.js` or `fetch-wrapper.js` changed** — in
   particular any change to `normalizeError()`'s rejection shape (§11.2, contract 2), which would
   invalidate every error-path fixture.
4. **`package.json`, `package-lock.json` or `vitest.config.js` moved.** A Vitest minor bump already
   changed observable output once (§11.2's warning); another could change the report format the harness
   parses.
5. **Packet F has landed.** The inventory derivation in §11.10 **expires** the moment Vitest nodes are
   pinned, and Packet C would then owe a regenerated artifact.
6. **`QUALITY_GATE.md`'s frontend feature map changed**, which would move the targeted union §11.10
   resolves.
7. **Any owner ruling in §11.13 is unanswered.** They are gate conditions, not preferences.

**Deliberately not done, under any circumstance:** no production JS change (including the two sharp
edges this packet only characterizes, §11.11-R4 and R13); no edit to `UI_SCENARIOS_GAP_ANALYSIS.md`,
`QUALITY_GATE.md`, `MASTER_HANDOVER.md` or `TESTING_STRATEGY_PLANNING.md`; no inventory regeneration;
no `js-unit` promotion; **Q4 and Q6 untouched**; Packet F not begun; no `.claude/settings.json` or
permission change — **a permission failure during execution is a blocker to report, not authority to
change configuration.**

### 11.13 Owner questions for Gate 1

These are decisions the packet **cannot** take for itself. They are separate from the acceptance of work
already specified above. **ALL SEVEN WERE ANSWERED 2026-08-22 — the rulings are in §11.16**, and the
questions below are left as asked so each ruling can be read against the question it answers.

> **DUPLICATE REMOVED, 2026-08-22 (Gate 1 owner ruling, plan-hygiene correction 1 of 4).** Plan v2 left
> **two** copies of question 1 in this subsection — one above the note below and one at the head of the
> numbered list — which made the list read as eight questions when the count everywhere else says
> **seven**. The stray copy is deleted; the list below is the single authoritative one and has exactly
> **seven** entries.

> **Plan v2 grew this list from six questions to seven** and rewrote two of them. **Question 5 is new**
> (council C-4 — the copy-ownership protocol Packet B was forced to answer and Plan v1 omitted), and
> what was question 5 is now **question 6**, covering **three** corrections outside §11 rather than one.
> *(At the Gate 1 ruling the owner authorized a **fourth**, in §2.3 — question 6 is annotated below.)*

1. **Is Packet C authorized to proceed past Gate 1 at all?** §0.1's Q1 authorizes Packets A → B → C as
   test-only expansion, and §10.13 lists **Packet C** among the items *"still not authorized and still
   unstarted, each needing its own confirmation"*. **Gate 1 approval is that confirmation.** If granted,
   please state separately whether **committing, pushing and opening a PR** are authorized. **Merge is
   NOT requested and, per the standing protocol, requires its own later confirmation naming the PR.**
2. **The final case count and delta — 29 cases, 202 → 231, and the mutation count 42.** The case count
   is **unchanged by Plan v2**; the mutation count moved **40 → 42** (P41, P42 appended). Confirm, or
   name which rows to drop and accept the coverage and mutation-kill loss that follows. The rows most
   likely to be judged optional are **C14** (`Set` type-identity characterization — *as asked, "killed
   by **no** mutation of `exercises.js`"; **measured false at execution — P41 reds it**, §11.17. The
   ruling at §11.16 retained C14 regardless*), **C26** (the KI-010 pass-through) and **C16** (DOM independence) — each
   is disclosed in §11.8's no-isolating-killer table as pinning an absence rather than a behavior.
3. **The targeted-test gate, and a real gap in `QUALITY_GATE.md`'s feature map.** The mapped union for
   `exercises` is **non-empty** — `workout-plan.spec.ts`, `exercise-interactions.spec.ts`,
   `superset-edge-cases.spec.ts` (`QUALITY_GATE.md:114`) — so Packet B's empty-union override does not
   transfer and is not reused. **The packet recommends running all three locally, taking no override.**
   Two rulings are needed: **(a)** is the local gate the mapped **three**, or the mapped three **plus
   `ui-hardening.spec.ts`** — which FINDING-C-E2E measured as the **sole** spec covering
   `clearWorkoutPlan()`, which **nothing in the map routes to**, and which Plan v2 further measured as
   asserting the **modal close** at `:1018` (so **P24 would red it**)? **(b)** Does that map gap get its
   own follow-up item? **Packet C may not edit `QUALITY_GATE.md`** (§11.1), so it cannot self-resolve
   either half. *The packet's recommendation on (a) strengthened in Plan v2 to: **run all four.***
4. **Do either of the two characterized sharp edges get a KI row, and does a stale KI citation get
   fixed?** Three items, all read-only to this packet: **(i)** the **`Set` key type-sensitivity**
   (§11.11-R4 / C14) — real, unfixed, and reachable from no in-app call site though `removeExercise` is
   a `window` global; **(ii)** the **vacuous `if (count > 0)` wrapper** at
   `exercise-interactions.spec.ts:218` (§11.11-R14); and **(iii)** *(new, council C-21)*
   **`docs/UI_SCENARIOS_GAP_ANALYSIS.md:100` cites `exercises.js:47`** — the
   `bootstrap.Modal.getInstance` line — for KI-005 behavior that lives at **`:65`**. **Packet C may not
   edit `UI_SCENARIOS_GAP_ANALYSIS.md`** or `e2e/**`, so each is a separate follow-up if wanted —
   exactly as KI-010, KI-011 and the stale `base.html:228` citation were routed for Packet B.
5. **NEW (council C-4) — does `exercises.test.js` become the SOLE owner of five copy strings, and is
   the same-PR protocol adopted?** Measured: the literals at `exercises.js:11, 12, 31, 36, 59, 68`
   occur **nowhere else**, and **no E2E spec asserts any of them**, so **C1, C2, C5, C8, C22 and C24**
   become their only guard at any tier. This is the identical condition that produced Packet B's Gate 1
   question 3, ruled at §10.11 as: *"a deliberate copy change updates these tests in the **SAME PR**,
   and the red is the **intended review signal**."* Confirm the same protocol here, or direct that the
   copy assertions be loosened — noting that loosening them removes the only thing that would notice a
   user-visible message changing. Note also **§11.11-R17**: C5's and C22's strings are the *fallback*
   copy, which the real routes never render.
6. **Do the corrections outside §11 stand as applied? There are now FOUR, not one.** *(§11.2,
   "Corrections applied".)* **(a)** §1.3's E2E count **9 → 3**, with the grep stated and all nine files
   dispositioned. **(b)** §1.3's **KI-005 criterion-4 attribution**, corrected from *"must run after the
   refresh"* to *"only after the server clear succeeds, never on the error path"* — a false attribution
   present since 2026-08-15 and the source of the over-read Plan v1 built C19 and P33 on. **(c)** The
   document's opening **Scope** block, **annotated** (not rewritten) to record that Packet C now has a
   Gate 1 plan and remains unauthorized. **(d)** *(added at the Gate 1 ruling, 2026-08-22)* §2.3's
   **Coverage targets** bullet: the *"legacy two-argument shape"* corrected to **both** measured
   arities, and the *"KI-005 criterion-4 ordering"* corrected to the contract criterion 4 actually
   states — with contract and characterization separated. Confirm all four, or direct any of them be
   reverted and recorded only inside §11 — in which case §1.3 and §2.3 keep claims measured to be false.
7. **Q4, Q6 and Packet F** — untouched and still open (§8, §2.5). Nothing in this plan touches any of
   them, and confirmation is sought only that none is drawn in by approving Packet C.

*(Not owner questions, recorded here so they are not mistaken for any: the mutation-ID prefix is
**`P`**, not `M`, because `M1`–`M19` belong to Packet A and `N1`–`N32` to Packet B — reasoning in §11.8;
and the mutation count moving 40 → 42 is a council-driven completeness fix, not a scope increase.)*

### 11.14 STOP — **DISCHARGED 2026-08-22**

> ⚠️ **DISCHARGED 2026-08-22 by the Gate 1 owner ruling recorded in §11.16.** Everything this STOP
> withheld — writing the test file, running the mutation matrix, committing, pushing and opening a PR
> — is now authorized and **executed** (§11.17). **Merge is NOT discharged**: it remains a separate
> confirmation naming the PR (§11.18). **Packet F, Q4/D2 promotion and Q6 are still untouched and
> still unauthorized**, exactly as this block says. The block below is **annotated, not rewritten**, so
> the pre-authorization state stays legible — the §10.12 discipline.

> **This plan is not authorization to write it.**

**No test file exists. No mutation has been run against `exercises.js` or against any copy of it.**
Every number in §11.3, §11.8 and §11.9 is a **prediction** derived by reading `exercises.js`,
`toast.js`, `workout-plan.js`, `workout-plan-events.js`, `fetch-wrapper.js`, `workout-plan-table.js`,
`plan_volume_panel.js`, `app.js`, `routes/workout_plan.py`, `utils/errors.py`,
`templates/workout_plan.html`, `ki005_controls_persistence/PLANNING.md`, the ten E2E files,
`tsconfig.json`, `package.json`, `ci.yml`, `QUALITY_GATE.md`, four pytest contract tests and
`docs/test_inventory/` — **not** by executing anything against the module.

**The four Plan v2 probe measurements (§11.15-M-a…M-d) are the ONLY things that were executed**, and
their containment is stated so it is auditable: throwaway files under the gitignored `artifacts/probe/`
with their own `--config` (`include: ['artifacts/probe/**/*.test.js']`), plus three read-only git and
`file` queries. **Nothing under `static/js` was read into a run, no repository test file was executed,
and no mutation harness was built.** They measured **Vitest's own semantics**, not this module's.

**Three things nobody could verify without executing, and they stay labelled as predictions:** the
**four ordered-log arrays** (§11.3), the **coverage movement** (§11.9), and **Vitest's exit-code and
report behavior under each mutant** (§11.8). §10.7-R9 governs all three — a discrepancy is investigated
before any expectation is edited.

**Explicitly unauthorized, each needing its own confirmation:**

- **Writing `static/js/modules/__tests__/exercises.test.js`** — Gate 1 (§11.13) is not approved.
- **Running any mutation**, even against a copy.
- **Committing, pushing, opening a PR, and merging** — merge is a separate confirmation again, naming
  the PR, per the standing protocol; **green CI is not that confirmation and neither is a selection
  among options.**
- **Packet F**, promotion of `js-unit` (**Q4** / **D2**), and **Q6**.
- Any production JS change, any edit to `UI_SCENARIOS_GAP_ANALYSIS.md`, `QUALITY_GATE.md`,
  `ki005_controls_persistence/PLANNING.md` or `e2e/**`, and any inventory regeneration.

Awaiting explicit owner approval of Gate 1 and rulings on the **seven** questions in §11.13.

### 11.15 Plan v2 record — Gate 1 council (2026-08-22)

**Three reviewers ran in parallel, all read-only against §11**: `architecture-reviewer`,
`test-strategist`, `product-risk-reviewer`. **All three returned "Needs revision."** Four items were
**blocking**, and the strongest signal in the set is that **two of the four were found independently by
two reviewers each**.

#### Part 1 — what was MEASURED, and what was only reasoned

The distinction matters because Plan v1's single largest defect was an unmeasured mechanism asserted as
fact. **Four measurements were taken 2026-08-22.** All four ran against throwaway files under the
gitignored `artifacts/probe/` with their own `--config` (`include: ['artifacts/probe/**/*.test.js']`),
or as read-only git/`file` queries: **nothing under `static/js` was touched and the repository suite was
never run.**

| # | Measurement | Result | What it settled |
|---|---|---|---|
| **M-a** | Does a `vi.mock` factory that creates its own `vi.fn()` re-run across `vi.resetModules()` + dynamic re-import? | **NO.** `factoryRuns before/after = 1 1`; `factory fn identity stable = true`; `topLevel === current factory fn = true`; **`topLevel call count = 2`** — the **fresh module instance called the ORIGINAL handle** | **The trap Plan v1's §11.5 was built around DOES NOT EXIST in Vitest 4.1.11.** The registry survives `resetModules()` and the test file's binding stays live |
| **M-b** | Is `vi.hoisted()` still required? | **YES, for a different reason.** A factory referencing a plain top-level `const` fails at **collection**: `Error: [vitest] There was an error when mocking a module … Caused by: ReferenceError: Cannot access '<name>' before initialization`, file reports **`(0 test)`**, suite fails | The strategy is unchanged; **its justification is replaced**. Also fixes **P39's form** |
| **M-c** | Does `vi.resetModules()` actually give a fresh module-level `Set`? | **YES** — `PROBE A3 fresh instance has(99) = false` | **C15's mechanism and the isolation half of §11.5 are sound** |
| **M-d** | On-disk EOL | `git config core.autocrlf` → **`true`**; **no `.gitattributes`**; `file` reports `exercises.js` and `toast.test.js` both **CRLF** | **§11.11-R6 upgraded from "assumed" to measured** |

**Everything else in the dispositions below was reasoned from source**, not executed — including every
kill-set correction in C-3, which is derived by re-reading each mutation against the nine
deep-equality/count cases. **Reasoning is not measurement, and the two are not blurred here.**

**Three things remain unverifiable without execution and stay labelled predictions**: the four
ordered-log arrays (§11.3), the coverage movement (§11.9), and Vitest's exit-code and report behavior
under each mutant (§11.8).

**Convergence is evidence, and it is recorded as such.** Where two reviewers reached the same
conclusion by different routes, the claim is materially stronger than a single reviewer's:

| Item | Reviewers | Independent? |
|---|---|---|
| **C-1** (the KI-005 criterion-4 over-read) | `product-risk-reviewer` **and** `test-strategist` | **Yes — by different routes.** One from the product-risk side (is a reordering user-visible?), one from the test-strategy side (does the cited criterion say this?). Both arrived at *"this is characterization, not a contract"* |
| **C-2** (the probe layout is unspecified) | `architecture-reviewer` **and** `test-strategist` | **Yes** |
| **C-3** (ten under-predicted kill sets) | `architecture-reviewer` (8 rows) **and** `test-strategist` (10 rows) | **Yes**, and the `test-strategist`'s list is a **strict superset** — so the superset is what was applied |
| **C-11** (FINDING-C-E2E's evidence) | **all three** | **Yes** — and all three independently re-derived **3**, which is why the *conclusion* survived while the *evidence* was rebuilt |
| **C-15** (two coverage deltas round wrong) | `architecture-reviewer` **and** `test-strategist` | **Yes — same two rows, same corrected figures** |
| **C-16** (C13's arrange is inconsistent) | `product-risk-reviewer` **and** `test-strategist` | **Yes** |

#### Part 2 — the disposition table

| # | Claim | Source | Disposition |
|---|---|---|---|
| **C-1** | **BLOCKING.** The "KI-005 criterion 4 ordering contract" framing is wrong — the reset running *after* `fetchWorkoutPlan()` is not what criterion 4 says | `product-risk` **+** `test-strategist`, independently | **ACCEPTED**, and re-verified against the source. `ki005_controls_persistence/PLANNING.md:448` says only *"call it from `clearWorkoutPlan()` **after the successful server clear** … then calls `clearWorkoutControls()` **LAST**"* — and that "LAST" is **internal to the helper** (`workout-plan.js:408-413`), not a position relative to the refresh; same wording at `:396`, `:633`. `fetchWorkoutPlan()` (`workout-plan.js:90-117`) touches **no** workout control, and the sole event listener is **150 ms-debounced** (`plan_volume_panel.js:244-247`), so **neither the refresh order nor the notify order is observable in production**. Applied in four places: **(a)** C19 and P33 relabelled **characterization of current call order**; **(b)** the cross-tier fact kept, the product-risk framing dropped (§11.3's ordered-log callout, §11.11-R8); **(c)** the criterion-4 claim re-attached to what it does state and Packet C can honestly pin — **reset only after `api.post` resolves, never on the error path** (C19's `api.post`→`resetControls` relation, plus **C25**); **(d)** **§1.3 line 145 corrected in the same edit**, since it is the **source** of the over-read and has carried it since 2026-08-15 |
| **C-2** | **BLOCKING.** §11.8 never states how a mutated copy is loaded, and Packet B's mechanism does not transfer | `architecture` **+** `test-strategist`, independently | **ACCEPTED.** §10.1's harness *"points the run at"* a copied `toast.js` — and §10.1's own last row says why that sufficed: *"Collaborator mocks: **none**. `toast.js` imports nothing."* Packet C's file carries **five** relative specifiers that must resolve at once. §11.8 now specifies the **mirrored `artifacts/probe/static/js/modules/` layout** with all four collaborators copied, POSIX `include` relative to that root, module rows mutating the copied module beside a pristine copied test file and **P38/P39 the reverse**, a **pre-flight row asserting all five specifiers resolve before P1**, and the standing 231-collected-cases check. §10.12 defect 2 is this hazard one level up — a wrong include path **fabricated a survivor** |
| **C-3** | **BLOCKING.** Ten mutation rows under-predict their kill sets | `architecture` (8 rows) **+** `test-strategist` (10 rows) | **ACCEPTED — the `test-strategist`'s list is a strict superset and is what was applied.** This is §10.5's failure class reproduced: kill sets were derived per behavior and never swept against the **nine** cases whose oracle is a whole-log deep equality (**C7, C9, C10, C16, C17, C18, C19, C25**) or a cross-instance call count (**C15**). Corrected cells: **P4** +C15; **P5** +C15; **P14** +C10; **P16** +C10; **P22** +C25; **P25** +C18; **P32** +C17,C18; **P33** +C17,C18 (and its "C19 only" claim removed); **P38** +C25; **P39** +C15. The sweep is added to §11.8 as a **stated harness requirement**. **Both reviewers confirmed no predicted kill is false** — unlike Packet B's N10/N12, this is pure omission, which is the cheaper of the two errors but still one that sends a future session chasing phantoms |
| **C-4** | **BLOCKING.** The copy-change protocol Packet B was forced to answer is absent | `product-risk` | **ACCEPTED.** §11 pins five literals by exact text (`exercises.js:11,12,31,36,59,68`) and they occur **nowhere else** — **no E2E asserts any of them** — so `exercises.test.js` becomes their **sole** guard at any tier. That is the exact condition behind Packet B's Gate 1 question 3 (§10.9, ruled §10.11: *"a deliberate copy change updates these tests in the SAME PR, and the red is the intended review signal"*). Added as **§11.11-R15** and **§11.13 question 5**, naming **C1/C2/C5/C8/C22/C24** |
| **C-5** | §11.5's `resetModules` trap is unmeasured; P39's mutant form is a `ReferenceError`, not the trap | `architecture` (3, 4) **+** `test-strategist` (6) | **PARTLY REFUTED BY MEASUREMENT, PARTLY ACCEPTED — see Part 3, which is this row's real home** |
| **C-6** | Three more cases lack an isolating killer: C11, C12, C14, C2 | `test-strategist` (4) | **ACCEPTED, with the stronger of the two remedies.** C11 and C14 are killed by **no** mutation of `exercises.js` (they appear only inside P39's over-broad set); C12 is never isolated from C13; and C2 is never distinguished from C1 — **while the declined-cases note rejects `removeExercise(null)`/`('')` precisely because they add no kill**, so Plan v1 applied a criterion to the declined pair it did not apply to C2. Two rows **appended** (IDs stable): **P41** `.has(exerciseId)` → `.size > 0` (**kills C11 only** — blocks a concurrent delete of a *different* id, the realistic broken-guard shape), and **P42** `!exerciseId` → `exerciseId == null` (**kills C2 only** — `0` then passes; the exact "fix" a developer would write). §11.8's disclosure table now names **C12** and **C14**, which the two new rows do not cover, and §11.3's declined-cases note records the consistency repair |
| **C-7** | The EOL-risk list of ten is incomplete | `test-strategist` (5) | **ACCEPTED. Ten → thirteen.** Added **P10** and **P28** (anchors span `:26-28` and `:54-56`, per §11.8's own anchor table) and **P14** (`fetchWorkoutPlan();` occurs at `:32` and `:60`, and the only stated discriminator is `:60`'s trailing comment, so the `:32` pattern must carry a line break). The criterion is restated as **"any pattern *or anchor* containing a line break"**, not "any mutation spanning lines". **M-d** is folded in: EOL is now measured CRLF, so this is about authoring patterns correctly, not discovering the EOL |
| **C-8** | C27's "explicit short per-case timeout" is an aspiration, not a value | `test-strategist` (8) | **ACCEPTED.** C27 is the only case with a wall-clock oracle, and a 50–100 ms value **can red against correct code on a loaded CI box** — a flake in the one suite whose purpose is qualifying for promotion. **Pinned at 1000 ms**, with the reasoning recorded: pristine resolves in ~1 ms so it cannot flake, and it costs the matrix one second on P37 |
| **C-9** | §11.7 contradicts §11.8's P8 row | `test-strategist` (2) | **ACCEPTED — §11.8 was right, §11.7 was wrong.** P8 releases the guard on success, so **C12 stays green**; that is the row's whole stated purpose. §11.7 now reads *"P7 makes both C12 and C13 read one; P8 makes only C13 read one"* |
| **C-10** | C5/C22 pin fallback copy production never renders, undisclosed | `product-risk` (3) | **ACCEPTED.** `routes/workout_plan.py:299` returns `message="Exercise removed successfully"` and `:320` `message="Workout plan cleared successfully"`; `utils/errors.py:36-37` sets `response["message"]` whenever truthy — so `result.message` is always present, the `\|\|` fallbacks at `:31`/`:59` are **unreachable through the real routes**, and the fallback strings differ from the server's **by a trailing `!`**. Same class Packet B disclosed for B15a/B15b. Disclosed on both rows and as **§11.11-R17** |
| **C-11** | FINDING-C-E2E's enumeration does not support "read every hit"; two reason strings and several citations are wrong | **all three** | **ACCEPTED — the conclusion survives, the evidence does not.** All three independently re-derived **3**, so the corrected §1.3 figure stands; but 3 + 4 named false positives = **7**, not the **9** being corrected, and no grep was stated. Repaired in **both** places (§1.3's note and §11.2's table): the **exact pattern** is stated; **every** file it returns is dispositioned, including the four unmentioned extras (`progression.spec.ts:671,677`, `program-backup.spec.ts:45,368`, `workout-log.spec.ts`, `volume-progress.spec.ts`) and `fixtures.ts:315-316`, all route-level `page.request.post`; the arithmetic **reconciles to 9 = 3 + 6**; `accessibility.spec.ts`'s reason changed from *"a filename hit only"* to **"no hit invokes either export"** (it has content hits at `:589`, `:598`, `:826`, `:1037`); `api-integration.spec.ts` re-cited to the calls at **`:50`/`:146`**; and two ranges fixed — superset **256-277** and ui-hardening **996-1034** |
| **C-12** | The `ui-hardening.spec.ts` disposition understates what that spec asserts | `product-risk` (5) | **ACCEPTED.** It also asserts the modal actually closes — `:1018`, `not.toHaveClass(/show/)`. The **order-blindness claim is unaffected**, but **P24 is therefore not unit-only**, and §11.13 q3 was being argued about a spec described incompletely. Added to the row, to P24, and to q3 — where it **strengthens** the recommendation to run that spec too |
| **C-13** | The document's Scope block is falsified by §11 and is not annotated | `architecture` (5) | **ACCEPTED.** Lines 13-14 said *"**Packet C** … untouched and still unauthorized"*; Packet C is no longer untouched. Packet B set the standard: §10.12 annotated **four** places outside §10 *"because this commit falsified prose that was true before it"*. The block is **annotated, not rewritten**, and recorded as **correction 3 of 4** *(3 of 3 when Plan v2 was written; the Gate 1 owner ruling added a fourth, in §2.3)* — so §11.2's "exactly one edit outside §11" is itself corrected |
| **C-14** | §11.2's "all five call sites use the **legacy signature**" contradicts C26 | `architecture` (6) | **ACCEPTED.** `toast.js:15` takes the **modern** branch whenever `result.message` is a type word — precisely the KI-010 collision C26 documents. Changed to *"all five use a legacy call **shape**; `:31`/`:59` route to the modern branch when the message is a type word — see C26"*. Harmless for the tests (toast is mocked, arities unaffected), but two claims in one document must not disagree |
| **C-15** | Two of the four coverage movements round the wrong way | `architecture` (8) **+** `test-strategist` (9), same figures | **ACCEPTED.** Branches is **+0.26 pp** (10.2282 → 10.4867), not +0.27; lines is **+0.43 pp** (7.1697 → 7.6015), not +0.44. Both were computed from the *displayed* two-decimal percentages instead of the counts — a derived-figure error class distinct from a wrong measurement, and the one nobody re-checks. Statements **+0.40** and functions **+0.18** were correct, and **all four predicted values (7.81 / 10.49 / 7.48 / 7.60 %) were and remain correct**. Both reviewers also independently confirmed **12/12 branch coverage is achievable** and that `try`/`catch`/`finally` contribute **no** branch under this provider |
| **C-16** | C13's arrange is internally inconsistent | `product-risk` (12) **+** `test-strategist` (12) | **ACCEPTED.** As written both post-repoint calls resolve, which does not produce the stated oracle. C13 now specifies **`mockRejectedValueOnce(...)` then `mockResolvedValue(...)`, two sequential awaited calls** |
| **C-17** | Ordered-log rows other than C19 also pin non-contract orderings | `product-risk` (6) | **ACCEPTED.** C7/C16 pin `fetchWorkoutPlan` before `notifyVolume`, and nothing requires it — the listener is debounced 150 ms, so either order is behaviorally identical. R8 disclosed the strictness generically; **P16 and P25 are now named as characterization-only orderings** whose red means *"confirm intent"* |
| **C-18** | "Production only ever passes a **number**" overstates unreachability | `product-risk` (9) | **ACCEPTED.** True of the sole in-app call site (`workout-plan-table.js:419`, bare `${exercise.id}`), but `removeExercise` is **also a `window` global** (`app.js:36`). Corrected to **"no in-app call site passes a string"** in **C14** and **R4** |
| **C-19** | One gate surface is unwalked: pytest contract tests that `rglob` `static/js/**/*.js` | `test-strategist` (10) | **ACCEPTED.** `tests/test_visual_selector_contracts.py:76-80` and `tests/test_css_wp4_4_base_contracts.py:44` glob `static/js/**/*.js` **without excluding `__tests__`**; `tests/test_css_display_utilities_contracts.py:82` and `tests/test_css_wp4_4_layout_contracts.py:524` do exclude it. All are **forbidden-token scans** (`data-visual-preserve-border`, `loading-spinner`, `fade-enter`), so a Packet C file is safe — **but safe because of an authoring constraint, not structural exclusion.** §11.10 now names the surface, the four tests, the token list and the constraint (**including in comments**), and it is **§11.11-R18**. Inheriting Packet B's precedent silently would have skipped a surface inside the **required** pytest gate |
| **C-20** | §12 Provenance still describes the Gate 0 session only | `architecture` (9) | **ACCEPTED, minimally.** Renumbering is clean — reviewers confirmed **nothing anywhere cites a `§11 Provenance`**, and the only pre-§11 reference to `§11` correctly points forward to §11.2. **One sentence** added to §12; **no restructuring** |
| **C-21** | KI-005's own citation points at the wrong line | `test-strategist` (12) | **ACCEPTED as a follow-up only.** `docs/UI_SCENARIOS_GAP_ANALYSIS.md:100` cites `exercises.js:47` — the `bootstrap.Modal.getInstance` line — where criterion-4 behavior is at **`:65`**. **Packet C may not edit that file**, so it joins **§11.13 question 4**, exactly as Packet B routed the stale `base.html:228` citation |
| **C-22** | §11.11-R6 states EOL as assumed | **mine (M-d)** | **ACCEPTED.** Upgraded to measured, with the method and the three facts, keeping only the forward-looking instruction that the new file be authored **CRLF** to match its three jsdom siblings |

#### Part 3 — C-5, the one prescription measurement INVERTED

*(Written out in full here because it is this row's only home, mirroring how §10.9 gave C-9 its own
paragraph as Packet B's refuted prescription. The pattern repeating across two consecutive packets is
itself worth noticing: in both cases a reviewer's **mechanism** was wrong and their **prescription** was
right, and only execution could tell the two apart.)*

**Plan v1's §11.5 was built around a trap that does not exist.** It claimed that an inline
`vi.mock('../toast.js', () => ({ showToast: vi.fn() }))` factory **re-runs** on the fresh registry after
`vi.resetModules()`, handing the re-imported module a **new** `vi.fn()` while the test file's own
top-level binding went stale — and it built an elaborate consequence on top: *"the failure is
asymmetric … every negative assertion would pass vacuously and forever … the dangerous outcome is an
implementer who relaxes positives into negatives."* It was a persuasive argument. **It was also false.**

**MEASURED (M-a):** `factoryRuns before/after = 1 1`, `factory fn identity stable = true`,
`topLevel === current factory fn = true`, and decisively **`topLevel call count = 2`** — the freshly
imported module instance called **the original handle**, the one the test file still holds.
`vi.resetModules()` does not re-run the factory; the mock registry survives it.

**The reviewers did not measure this either — they flagged it as unmeasured, which was the right call
for the right reason.** Two of them (`architecture` 3/4, `test-strategist` 6) objected that the trap was
asserted rather than demonstrated, and separately that **P39's stated mutant form — "replace the
`vi.hoisted()` handles with inline factories" — would not produce the trap but a `ReferenceError`.**

**Both halves of their prescription are adopted, and the second is independently confirmed by M-b.**
A `vi.mock` factory referencing a plain top-level `const` fails at **collection**
(`ReferenceError: Cannot access '<name>' before initialization`, file reports `(0 test)`), so the
literal form Plan v1 wrote is **not a mutation at all** — §10.5's N1 lesson applies verbatim: *"a
mutation that cannot be loaded is not a mutation."* **P39's form is corrected** to: keep the `h` object
and every test-body reference, and change **only the four `vi.mock` factory bodies** to return their own
inline `vi.fn()`s — four anchored single-line edits, or a whole-file mutant with its oid recorded.

**What changed, and what did not:**

| | Verdict |
|---|---|
| The `resetModules` mock-identity trap | **DOES NOT EXIST** (M-a). §11.5's central justification, **§11.11-R1** and C28's *"the case that fails if the trap bites"* framing are all **rewritten, not relabelled** |
| `vi.hoisted()` | **STAYS — mandatory**, for the measured reason M-b, not the imagined one |
| `vi.resetModules()` + per-case re-import | **STAYS — sound** (M-c: `fresh instance has(99) = false`) |
| **C15** | **STAYS**, mechanism independently corroborated by `PROBE A3` |
| **C28** | **STAYS**, on a narrower and real property: the handles the test asserts on must be the handles the module receives. **Independent of any `resetModules` behavior** |
| **P39** | **STAYS a LIVE mutation, not an equivalence.** Under the corrected form C28's identity assertion genuinely reds |

**The transferable lesson, stated because it is the reason this section exists:** Plan v1 asserted a
runtime semantic it had not run, and then reasoned three layers of consequence on top of it. The
consequences were internally coherent, which is exactly what made them convincing. **A mechanism you
have not executed is a hypothesis, however well it explains things** — and the correct response to a
reviewer saying *"this is unmeasured"* is to measure it, not to argue it.

#### Part 4 — scope of the Plan v2 edit

Plan v2 changed **§11** and **two places elsewhere in this same file**, so a reviewer is not surprised
by them in the diff: **§1.3's `exercises.js` row** (its KI-005 cell, per C-1(d), plus a rebuilt E2E note
per C-11) and **the opening Scope block** (annotated, per C-13). Both are recorded in §11.2's
*Corrections applied* table, which carried **three** rows at Plan v2 and carries **four** after the
Gate 1 owner ruling added the §2.3 correction. **Nothing outside
`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` was touched**, no test file was created, no production JS
was changed, no mutation harness was built, and nothing was committed or pushed.

**Counts after Plan v2:** cases **29** (unchanged), suite delta **202 → 231** (unchanged), files
**12 → 13** (unchanged), mutations **40 → 42**, EOL-risk rows **10 → 13**, corrections outside §11
**1 → 3** *(→ **4** at the Gate 1 owner ruling)*, owner questions **6 → 7**, risk rows
**R1–R14 → R1–R18** (R1 withdrawn in place).

### 11.16 Owner ruling at Gate 1 (2026-08-22) — **APPROVED, WITH FOUR PLAN-HYGIENE CORRECTIONS**

**Gate 1 is APPROVED.** Implementation in the existing isolated worktree, creation of
`static/js/modules/__tests__/exercises.test.js`, the test / coverage / mutation / E2E gates, this
execution record, **commit, push and a ready-for-review PR** are authorized. **Merge is NOT** — it
remains a separate confirmation naming the PR (§11.18).

**The seven questions of §11.13, answered.**

| # | Question | Ruling |
|---|---|---|
| **1** | Authorized past Gate 1 at all? | **YES.** Implementation, commit, push and PR creation authorized; **merge separately gated** |
| **2** | 29 cases / 202 → 231 / 42 mutations, and the optional-looking rows | **RETAIN ALL.** All 29 cases, the 202 → 231 delta and all 42 mutation rows stand. **C14, C16 and C26 are retained with their characterization / boundary labels.** **P40 remains the declared equivalent mutation and must survive only for the stated reason** |
| **3** | The targeted-test gate, and the feature-map gap | **RUN ALL FOUR** Chromium specs locally: `workout-plan.spec.ts`, `exercise-interactions.spec.ts`, `superset-edge-cases.spec.ts`, **`ui-hardening.spec.ts`**. The missing `ui-hardening.spec.ts` routing is recorded as a **separate follow-up**; **`QUALITY_GATE.md` is NOT edited in Packet C** |
| **4** | KI rows and the stale citation | **NO KI ROW** for the `Set` key type-sensitivity now — **C14 is retained as clearly labelled characterization**, because no in-app caller passes a string ID. The **vacuous `if (count > 0)`** at `exercise-interactions.spec.ts:218` is a separate **test-honesty follow-up**; the stale **`UI_SCENARIOS_GAP_ANALYSIS.md:100`** citation is a separate **documentation follow-up**. **Neither affected file is edited in Packet C** |
| **5** | The copy-ownership protocol | **ADOPTED, identical to Packet B's.** `exercises.test.js` becomes the guard for the five user-visible copy strings. **A deliberate copy change updates the corresponding tests in the SAME PR; the resulting red is an intended review signal, not justification to loosen the assertions.** Recorded in the test file's header comment |
| **6** | The corrections outside §11 | **ALL THREE STAND**, and a **fourth is authorized** in **§2.3**: replace the false *"KI-005 criterion-4 ordering"* wording with the actual contract (reset only after a successful server clear, never on the error path); describe the measured toast call shapes accurately (**three two-argument** and **two one-argument** legacy-shaped calls); and distinguish contractual behavior from characterization of the current refresh / reset / notification order. Applied — §11.2's *Corrections applied* table now carries **four** rows |
| **7** | Q4, Q6, D2, Packet F | **CONFIRMED out of scope and unauthorized.** None is drawn in by approving Packet C |

**Four plan-hygiene corrections, ordered before implementation and applied — plus a post-correction
check, which is a verification step and is deliberately not numbered among them** (the three in-place
annotations in the document say *"correction N **of 4**"*, and that denominator is the correct one).
The owner ruled these factual and ratified, and that **a second Gate 1 council is not required** unless
making them changed the 29-case scope, the 42-mutation scope, ownership, or production behavior.
**None did.**

| # | Correction | Where |
|---|---|---|
| **1** | **The duplicated question 1 removed** — §11.13 carried **two** copies, which read as eight questions against a **seven** stated everywhere else. One numbered list of exactly seven remains | §11.13 |
| **2** | **"there is no Packet C branch, worktree or PR" corrected** — true before planning began, falsified by the planning itself. The sole branch is **`wt/phase3-packet-c-exercises`** and the sole worktree **`D:/development/HT-v3-packetc-exercises`**; **no PR existed at ruling time** | §11.1 |
| **3** | **The §2.3 correction applied** (question 6's fourth item) | §2.3 |
| **4** | **Every affected count and provenance statement moved three → four** — the corrections table and its intro, question 6 and its preamble note, council disposition **C-13** (*"correction 3 of 3"* → *"3 of 4"*), and §11.15 Part 4's row count and count summary | §11.2, §11.13, §11.15 |
| *(check)* | **`git diff --check` run after the corrections** — not a correction | — **clean** |

**Explicitly NOT authorized by this ruling**, and untouched: everything **§11.18** enumerates, plus
any edit outside the two approved tracked files. The list is kept in one place — §11.18, the live STOP
— rather than restated here, so the two cannot drift apart.

### 11.17 Execution record — 2026-08-22

**Base**: `b52df68`, branch `wt/phase3-packet-c-exercises`, worktree
`D:/development/HT-v3-packetc-exercises`. **Tracked diff: exactly two files** —
`static/js/modules/__tests__/exercises.test.js` (new) and this plan.

**All seven stop conditions of §11.12 were checked BEFORE writing a line**, by oid rather than by
inspection: `exercises.js`, `toast.js`, `workout-plan.js`, `workout-plan-events.js`,
`fetch-wrapper.js`, `package.json`, `package-lock.json`, `vitest.config.js` and `QUALITY_GATE.md` all
**oid-identical to `b52df68`**; the baseline measured **12 files / 202 cases**; and
`docs/test_inventory/` still holds **zero** matches for `vitest`, `test:js` or `static/js`, so **Packet
F has not landed**. None of the seven fired.

**Counts — all four pinned checks (i)–(iv) pass.**

| Check | Expected | Measured |
|---|---|---|
| **i** Focused run | **1 file / 29 passed** | **1 file / 29 passed** |
| **ii** Full suite | **13 files / 231 passed** | **13 files / 231 passed** |
| **iii** Skipped / todo / filtered, both runs | **zero** | **zero** — read from the JSON reporter, not from the summary line: `numPendingTests` **0**, `numTodoTests` **0**, and the only assertion status present across all 231 is `passed` |
| **iv** Source grep | no `.only` / `.skip` / `.todo`, no `it.each`, and none of the three forbidden CSS-contract tokens | **none present.** `29` `it(` call sites = **29** reported cases, so no expansion is unaccounted for |

**Coverage — measured on both arms, in this worktree, on this base. Recorded, never gated.**

| | Predicted (§11.9) | Measured | Verdict |
|---|---|---|---|
| `exercises.js` per file | 30/30 st, 30/30 ln, 2/2 fn, **12/12 br** | **30/30, 30/30, 2/2, 12/12 — 100 % on all four** | **Exact** |
| Suite statements | **582**/7453 | **582**/7453 | **Exact** |
| Suite branches | **487**/4644 | **487**/4644 | **Exact** |
| Suite functions | **83**/1110 | **83**/1110 | **Exact** |
| Suite lines | **528**/6946 | **528**/6946 | **Exact** |
| Focused-arm totals | — | **30 st / 12 br / 2 fn / 30 ln covered, and nothing else** | Independently confirms §11.9's **assumption 2** — no other file's covered count moved, so no mock leaked into real collaborator code |

> **ONE DISCREPANCY, INVESTIGATED BEFORE ANYTHING WAS EDITED (§10.7-R9), AND IT IS IN THE REPORTER,
> NOT THE PACKET.** §11.9 predicted the displayed percentages **7.81 / 10.49 / 7.48 / 7.60 %**; v8's
> summary prints **7.8 / 10.48 / 7.47 / 7.6 %**. **Every covered/total COUNT matched exactly**, which is
> the measurement; the difference is that **the reporter truncates where §11.9 rounded** — 10.4867 →
> `10.48` printed against `10.49` predicted, 7.4775 → `7.47` against `7.48`. **No figure in §11.9 is
> edited**: its counts are right and its *deltas* (+0.40 / +0.26 / +0.18 / +0.43 pp) are right. What is
> recorded here is that a **predicted percentage string is not a safe oracle against this reporter** —
> the same lesson §11.15-C-15 drew one step earlier, when two deltas were computed from displayed
> percentages instead of from counts.

**Mutation matrix — all 42 rows executed, harness under the gitignored `artifacts/probe/`, discarded
afterward.** The mirrored layout §11.8 specifies was built exactly as written; the **pre-flight row
passed before P1** (all five relative specifiers resolved, **231** collected, green). Every row ran the
**full suite**, was judged by the runner's **process exit code**, and was required to report **exactly
231 collected cases**. **No row reported `BAD RUN` and no row reported `NOT APPLIED`** — including the
thirteen line-break-anchored rows §11.8 flagged as the expected symptom of skipped normalisation.

**Containment held on every row**, asserted through git's own normalisation (`rev-parse` vs
`hash-object`, never a raw byte compare): `static/js/modules/exercises.js` stayed oid-identical to
`b52df68` and `exercises.test.js` stayed oid-identical to its authored form, **after each of the 42
runs**.

| # | Verdict | Collected | Predicted red | Measured red | |
|---|---|---:|---|---|---|
| **P1** | KILLED | 231 | C1,C2 | C1,C2 | as predicted |
| **P2** | KILLED | 231 | C1,C2 | C1,C2 | as predicted |
| **P3** | KILLED | 231 | C1,C2 | C1,C2 | as predicted |
| **P4** | KILLED | 231 | C10,C15 | C10,C15 | as predicted |
| **P5** | KILLED | 231 | C10,C15 | C10,C15 | as predicted |
| **P6** | KILLED | 231 | C10,C15 | C10,C15 | as predicted |
| **P7** | KILLED | 231 | C12,C13 | C12,C13 | as predicted |
| **P8** | KILLED | 231 | C13 | C13 | as predicted |
| **P9** | KILLED | 231 | C3 | C3 | as predicted |
| **P10** | KILLED | 231 | C3 | C3 | as predicted |
| **P11** | KILLED | 231 | C3 | C3,C11 | **superset** of the prediction |
| **P12** | KILLED | 231 | C5 | C5 | as predicted |
| **P13** | KILLED | 231 | C4 | C4,C13 | **superset** of the prediction |
| **P14** | KILLED | 231 | C7,C10,C16 | C7,C10,C16 | as predicted |
| **P15** | KILLED | 231 | C6 | C6 | as predicted |
| **P16** | KILLED | 231 | C7,C10,C16 | C7,C10,C16 | as predicted |
| **P17** | KILLED | 231 | C8 | C8,C13 | **superset** of the prediction |
| **P18** | KILLED | 231 | C8 | C8,C13 | **superset** of the prediction |
| **P19** | KILLED | 231 | C8,C9 | C8,C9,C13 | **superset** of the prediction |
| **P20** | KILLED | 231 | C8 | C8 | as predicted |
| **P21** | KILLED | 231 | C17 | C17 | as predicted |
| **P22** | KILLED | 231 | C18,C19,C25 | C18,C19,C25 | as predicted |
| **P23** | KILLED | 231 | C18 | C18,C20,C21,C22,C23,C24,C26,C27 | **superset** of the prediction |
| **P24** | KILLED | 231 | C19,C25 | C19,C25 | as predicted |
| **P25** | KILLED | 231 | C18,C19,C25 | C18,C19,C25 | as predicted |
| **P26** | KILLED | 231 | C20 | C20 | as predicted |
| **P27** | KILLED | 231 | C20 | C20 | as predicted |
| **P28** | KILLED | 231 | C20 | C20 | as predicted |
| **P29** | KILLED | 231 | C22 | C22 | as predicted |
| **P30** | KILLED | 231 | C21,C26 | C21,C26 | as predicted |
| **P31** | KILLED | 231 | C23 | C23 | as predicted |
| **P32** | KILLED | 231 | C17,C18,C19 | C17,C18,C19,C27 | **superset** of the prediction |
| **P33** | KILLED | 231 | C17,C18,C19 | C17,C18,C19 | as predicted |
| **P34** | KILLED | 231 | C25 | C25 | as predicted |
| **P35** | KILLED | 231 | C24 | C24 | as predicted |
| **P36** | KILLED | 231 | C24 | C24 | as predicted |
| **P37** | KILLED | 231 | C27 | C27 | as predicted |
| **P38** | KILLED | 231 | C18,C19,C25,C29 | C17,C18,C19,C25,C29 | **superset** of the prediction |
| **P39** | KILLED | 231 | C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,C14,C15,C16,C17,C18,C19,C20,C21,C22,C23,C24,C25,C26,C27,C28 | C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,C14,C15,C16,C17,C18,C19,C20,C21,C22,C23,C24,C25,C26,C27,C28 | as predicted |
| **P40** | SURVIVED | 231 | (none — declared equivalent) | — | **SURVIVED — the declared equivalence** |
| **P41** | KILLED | 231 | C11 | C11,C14 | **superset** of the prediction |
| **P42** | KILLED | 231 | C2 | C2 | as predicted |

**41 killed, 1 survived — and the survivor is P40, exactly as declared in advance.** P40's stated
reasoning holds under measurement: there are no statements between `:22` and the `try` at `:24`,
`Set.prototype.add` cannot throw, and the `finally` at `:37` drains the key on every exit path from the
`try`, so the two placements are indistinguishable through the public API. It is recorded as an
equivalent mutant exactly as **M13** (§9.13-D2) and **N13** (§10.5) were — **not** chased with a
contorted test.

> **NINE ROWS RED MORE THAN PREDICTED, AND NOT ONE RED LESS.** Checked mechanically: for **all 42
> rows, the predicted set is a SUBSET of the measured set** — **no predicted kill failed to
> materialise**. That direction matters. An over-prediction would mean a case does not pin what the
> plan claims; an under-prediction means the plan's *sweep* was incomplete, which is the cheaper error
> and the same class §11.15-C-3 corrected one level up. **No expectation was edited to match
> execution**; each extra kill was traced to the assertion that produced it:
>
> | Row | Extra | Why |
> |---|---|---|
> | **P11** | +C11 | C11 asserts the **request bodies** (`{id:1}`, `{id:2}`), not only the call count. C-3's sweep covered whole-log and call-count oracles and missed **argument-shape** ones |
> | **P13** | +C13 | C13 asserts the **second** call's `showToast` argument list is `['Removed']`; under P13 it is the fallback copy |
> | **P17**, **P18**, **P19** | +C13 | C13 asserts the **first** call's `showToast` argument list is the two-argument error shape; all three rows change or delete it |
> | **P23** | +C20, C21, C22, C23, C24, C26, C27 | §11.8's own P23 row **states the mechanism** — `null.hide()` throws and the module's `catch` at `:66` swallows it, so `api.post` never runs — but predicted only C18. Every `clearWorkoutPlan` case that runs at the **default** `getInstance → null` arrangement therefore reds. The mechanism was right; the sweep stopped at one case |
> | **P32** | +C27 | C27 asserts `resetControls` is present in the log, so deleting the call reds it |
> | **P38** | +C17 | C17's arrangement is `document.getElementById('clearPlanModal').remove()`; with the fixture emptied that throws. **The right signal**: C17 cannot arrange "modal absent" against a fixture that never had the node, which is precisely what C29 exists to guarantee |
> | **P41** | +C14 | C14's second call uses `'1'` while `1` is still in flight; under `.size > 0` it is blocked, so `api.post` reads 1 rather than 2. **This falsifies §11.8's disclosure that C14 is "killed by no mutation of `exercises.js` at all"** — corrected in place there. **And it falsifies the row above it**: Plan v2 struck C11 off the disclosure table as *"CLOSED by P41"*, but P41 reds C11 and C14 **together**, and **P11 already red C11** through its request-body oracle — so **neither case has an isolating killer**, the honest figure is **five**, not four, and only **C2 / P42** was genuinely closed. Both corrections are applied in §11.8, §11.3 and the test file's comments |
>
> **The four ordered-log arrays (§11.3) were predictions and all four matched on the first run**, as
> did every per-file coverage figure — so §10.7-R9 was never invoked to protect a wrong number.

**Every other gate.**

| Gate | Result |
|---|---|
| `scripts/generate_test_inventory.py --check` | **"Test inventory is up to date."**, exit **0**. **Nothing regenerated** |
| The four pytest contract tests globbing `static/js/**/*.js` (§11.10's sixth surface) | **40 passed.** The two that do **not** exclude `__tests__` read the new file and found none of `data-visual-preserve-border`, `loading-spinner`, `fade-enter` |
| Targeted Chromium E2E — the mapped three **plus `ui-hardening.spec.ts`** (owner ruling 3) | **111 passed**, exit **0**, ~3.0 min. Port-5000 mutex respected: the port was verified free first, Playwright started its own server, **`PW_REUSE_SERVER` was never set** and no other session's server was touched |

**FIVE STATUS ANNOTATIONS were made at execution time — three outside §11 and two inside it — and
they are NOT corrections.** The §11.2 *Corrections applied* table counts **four** edits that repair
claims measured to be **false**; these five are a different thing — prose that was **true when written**
and that this commit falsified, annotated in place under the §10.12 discipline rather than rewritten.

| # | Where | In §11? | What it said before |
|---|---|---|---|
| **1** | the opening **Scope** block | outside | its Plan v2 annotation said *"no test file exists … Gate 1 is not approved"*. It now carries a **second** annotation; **both are left standing** so the sequence is legible |
| **2** | **§2.3's heading** | outside | *"(AUTHORIZED — third)"*; now marked *Gate 1 approved and executed, PR open and NOT merged*, exactly as §2.2 was marked for Packet B |
| **3** | **§10.13's closing list** and its *"exactly one moved"* count | outside | listed **Packet C** as *"still not authorized and still unstarted"*. A **second** of its five items has now moved |
| **4** | **§11's heading and STATUS block** | inside | *"GATE 1 NOT YET APPROVED"* / *"PLANNING ONLY"* |
| **5** | **§11.14's STOP** | inside | *"This plan is not authorization to write it"*; marked **DISCHARGED** |

The one clause every annotation leaves untouched, because it is still true: **Packet F, Q4/D2 promotion
and Q6 remain untouched and unauthorized.**

**Authoring decisions worth recording, because a later reader would otherwise re-derive them:**

- **The rejection fixtures are `Object.freeze`d.** §11.3 rule 2 fixes the *shape*; freezing additionally
  guarantees the object C8 and C24 compare **by identity** (`toBe`) cannot be mutated by an earlier
  case. Neither the rule nor any case required it; it is cheap insurance on the one oracle that is an
  identity comparison rather than a deep equality.
- **`api.post` is the only mock re-pointed per case**, through three small helpers (`resolvePost`,
  `rejectPost`, `rejectPostOnce`) that push `'api.post'` onto the ordered log **at call time, before
  resolving or throwing**. That is what makes C9's and C25's arrays start with `'api.post'` on a
  rejection: the log records the **request**, not its outcome.
- **C13 is expressed as `mockImplementationOnce` then a resolving default**, which is the log-pushing
  equivalent of §11.3's `mockRejectedValueOnce(...).mockResolvedValue(...)`. Plain
  `mockRejectedValue*` helpers cannot append to the ordered log.
- **C19 carries a second, weaker assertion after its deep equality** —
  `calls.indexOf('api.post') < calls.indexOf('resetControls')` — stating the **contract** relation
  separately from the characterization array that contains it. If a future session relaxes the array
  because a reordering was intentional, the contract survives the edit rather than being deleted with it.
- **Only the two rejection fixtures are `Object.freeze`d, and `POST_OPTIONS` deliberately is not.**
  The asymmetry is the point: freezing guards the objects C8 and C24 compare **by identity** (`toBe`).
  `POST_OPTIONS` is only ever an argument to a deep equality, where mutation would surface as a failing
  comparison rather than as a silently-passing one.

#### Review record — `code-reviewer` and `unslop-reviewer`, both run over the final two-file diff

Both ran read-only against the staged diff, and **they found disjoint defect classes**, which is the
standing reason for running both. **`code-reviewer` walked all 29 cases against the module and found no
flake vector and no vacuous oracle** — every finding on both sides landed in **comments and in this
document**, not in the assertions. **Three findings were claims this packet's own measurement
falsifies**, which is the class that matters most: prose that was true when Plan v2 wrote it and that
execution disproved.

**Accepted and applied — the three measurement-falsified claims first:**

| Finding | Applied |
|---|---|
| **C11 was struck off §11.8's disclosure table as "CLOSED by P41"** — but P41 reds **C11 and C14 together**, and **P11 already red C11**. *(`code-reviewer`)* | §11.8's row **restored and rewritten**, the count moved **four → five**, §11.3's C11 cell corrected from *"Isolated by P41"*, and the test file's C11 comment corrected |
| **C14's "killed by no mutation of `exercises.js`"** survived in §11.3, §11.13 q2 **and in the shipped test file**, citing as authority the very table §11.17 corrected *(both reviewers, independently)* | Corrected in all three, plus §11.8 |
| **C18's comment credited its identity assertion to P21** — but C18's fixture *has* the modal, so `if (modal)` and `if (true)` are indistinguishable there, and **P21 measured as killing C17 alone**. The argument is C17's *(`code-reviewer`)* | Corrected in the test file **and** at §11.6 item 2, its origin |

**Also accepted and applied:**

- **§11.1 still said "38 mutations to `exercises.js`"** — stale since P41/P42 were appended. Now **40**.
  *(both reviewers, independently.)*
- **C27's "Production lines" cell cited `exercises.js:32`**, which C27 never drives. The `:32`
  un-awaited call is pinned by **nothing** and has **no mutation row** — adding an `await` there strands
  nothing, because `:33` is the last statement of the `try`. **Disclosed as an accepted gap**, not
  closed: closing it would add a 30th case against an owner-pinned 29. *(`code-reviewer`.)*
- **The whole-log enumeration in §11.8's harness requirements omitted C1 and C2**, which also deep-equal
  `calls`. Corrected **nine → eleven**; it changed **no** measured result. *(`unslop-reviewer`.)*
- **§11.16 said "five plan-hygiene corrections" while every in-place annotation said "of 4"** — the fifth
  entry was `git diff --check`, a verification step. Retitled to **four, plus a check**.
  *(both reviewers, by different routes: one proposed raising the annotations to five, the other
  proposed demoting the check — **the second is right**, because the check corrects nothing.)*
- **"the literals occur NOWHERE ELSE in the repository"** overstated it: the server's copy at
  `routes/workout_plan.py:299/305/320/323` is the same user-visible phrasing, differing by a trailing
  `!` — which §11.11-R17 already disclosed for C5 and C22, so the header and the case comments were in
  tension. Narrowed to **"nowhere else as exact literals"**, keeping the load-bearing half, which
  `code-reviewer` independently re-verified: **no E2E spec asserts any of them.** *(`code-reviewer`.)*
- **§11.11-R7 still said the local gate was "the mapped three"**, superseded by ruling 3's **four**.
  Annotated. *(`code-reviewer`.)*
- **The `exercise-interactions.spec.ts` follow-up cited `:218`, a `test(` declaration** — the guard is at
  **`:225`** — **and missed a second vacuous wrapper at `:212`**. Both corrected at §11.11-R14 and
  §11.18, so the follow-up no longer under-counts its own surface. *(`code-reviewer`.)*
- **§10.13's closing list and its "exactly one moved" count**, the **§11 heading**, the **§12 provenance
  pointer** (§11.14–§11.15 → §11.15–§11.17), the **PR cell** added by plan-hygiene correction 2, a
  **broken markdown table** whose blank line orphaned correction row 4, and **three near-identical
  "not authorized" lists**, now kept once in §11.18. *(`unslop-reviewer`.)*

**Two assertions were deleted as subsumed — and the deletion was MEASURED, not reasoned:**
`expect(h.post.mock.calls[0][2].showErrorToast).toBe(false)` in **C3** and
`expect(h.post.mock.calls[0][1]).toBeNull()` in **C20** are both fully covered by their rows'
`toHaveBeenCalledWith(..., POST_OPTIONS)` deep equality. **The full 42-row matrix was re-run after
removing them** — a test-file change invalidates every previously measured row — and the results are
**byte-for-byte the same**: 41 killed, P40 the sole survivor, the same nine supersets, **P10 still red
by C3 and P27 still red by C20**. Had either removal weakened a row, its mutation would have survived.

**Declined, with reasons, because §11.3's matrix is owner-ratified and "follow it exactly" was an
explicit instruction:**

| Declined | Why |
|---|---|
| Drop C1/C2's `expect(h.post).not.toHaveBeenCalled()` as subsumed by the following deep equality | §11.3's C1 oracle prescribes **both** — *"**then** `api.post` **not** called **and** `calls` is `['showToast']`"*. The negative does not stand alone, so authoring rule 1 is satisfied; deleting a prescribed assertion is a deviation from a ratified matrix, not a cleanup |
| Drop C28's `expect(vi.isMockFunction(handle)).toBe(true)` as a tautology | §11.3's C28 oracle prescribes it explicitly — *"are **`vi.fn()`s at call count 0**"*. Same reason |
| Inline the single-caller `rejectPostOnce` helper | It is one of **three parallel helpers for one mock**, and the trio is what keeps every `api.post` arrangement logging identically. Collapsing one of three is a smaller file and a less symmetric one |
| Renumber §1.3's *"CORRECTION 1 of 2 / 2 of 2"*, a third numbering scheme | Those ordinals are **scoped to §1.3's own two corrections** and are correct as written. Renumbering ratified prose to serve a different section's counter is the failure this document already fought once (§2.6) |

**One finding is ROUTED TO THE OWNER, not fixed:** §1.3's prose names `exercises.js:12` and `:36` as the
legacy two-argument sites and **omits `:68`** — the same undercount the owner authorized correction 4 to
repair at §2.3. **It is not repaired here**, because that would be a **fifth** correction outside §11
and the owner ruled on four. It joins §11.18's follow-up list.

### 11.18 STOP — merge

> **This record is not authorization to merge.**

The PR is opened **ready for review** and **stops there**. Per the standing protocol, merge requires a
**separate explicit confirmation naming the PR and saying "merge"** — **green CI is not that
confirmation, and neither is a selection among options.**

**Still not authorized, each needing its own confirmation:**

- **Merging the Packet C PR.**
- **Packet F**, promotion of `js-unit` (**Q4** / **D2**), and **Q6**.
- Any production JS change; any edit to `UI_SCENARIOS_GAP_ANALYSIS.md`, `QUALITY_GATE.md`,
  `ki005_controls_persistence/PLANNING.md` or `e2e/**`; any inventory regeneration; any
  branch-protection or repository-setting change; any `.claude/settings.json` change.

**Three follow-ups were opened by the Gate 1 ruling and are recorded here, not acted on** (each needs
its own authorization, and each touches a file Packet C may not edit):

1. **`QUALITY_GATE.md`'s frontend feature map routes nothing to `ui-hardening.spec.ts`**, the sole spec
   covering `clearWorkoutPlan()` (§11.10).
2. **Two vacuous `if (count > 0)` wrappers in `exercise-interactions.spec.ts`** — the guard at
   **`:225`** (in the test declared at `:218`, the one §11.11-R14 named, citing the declaration rather
   than the guard) **and a second at `:212`** (in the test declared at `:204`, which no earlier surface
   mentioned). Both pass vacuously on an empty table — a test-honesty follow-up covering **two** tests,
   not one.
3. **`docs/UI_SCENARIOS_GAP_ANALYSIS.md:100` cites `exercises.js:47`** for KI-005 behavior that lives at
   **`:65`** (§11.15-C-21) — a documentation follow-up.
4. *(new, raised by `unslop-reviewer` at execution)* **§1.3's prose names `exercises.js:12` and `:36` as
   the legacy two-argument `showToast` sites and omits `:68`** — the same undercount the owner
   authorized correction 4 to repair at §2.3. **Not repaired here**: it would be a **fifth** correction
   outside §11, and the ruling covered four.

**T0 is NOT established by this packet.** It begins only after a separately authorized Packet C merge
**and** the first successful post-merge `main` `JS Unit (Vitest, non-required)` run.

---

## 12. Provenance

> **This table records the Gate 0 session only** (2026-08-15, base `c404a06`) and is deliberately left
> as that record. Each packet carries its own provenance in its own section: **Packet A's is §9**,
> **Packet B's is §10.2 / §10.12**, and **Packet C's is §11.2 (what was measured), §11.15
> (the Gate 1 council) and §11.16–§11.17 (the ruling, and what was executed, by whom)**. *(Renumbered §11 → §12 by Packet C's Plan v1;
> verified then and re-confirmed at Plan v2 that nothing inside or outside this file cites a
> "§11 Provenance", and that the only pre-§11 reference to `§11` points forward to §11.2.)*

| Item | Value |
|---|---|
| Base commit | `c404a06` (`origin/main` at session start) |
| Branch / worktree | `wt/phase3-jsunit-gate0`, isolated docs-only worktree |
| Files owned by this packet | This file only |
| Files read, not modified | `AGENTS.md`, `CLAUDE.md`, `docs/MASTER_HANDOVER.md`, `docs/TESTING_STRATEGY_PLANNING.md`, `docs/ai_workflow/QUALITY_GATE.md`, `package.json`, `vitest.config.js`, the 10 files under `static/js/modules/__tests__/`, the four target modules, `.github/workflows/ci.yml`, `scripts/generate_test_inventory.py` |
| Live measurements | 515 `ci.yml` runs resolved at job level (§6); branch protection read via API (§7.1); coverage and test counts read from run `31856035853` (§1.1) |
| Measured on | 2026-08-15 |
| Owner sign-off | Q1, Q2 signed and Q3, Q5 ruled 2026-08-15 — recorded verbatim in §0.1; §8 annotated |

> **Every number in §1.1, §6 and §7.1 is a live measurement taken this session, not a figure copied
> from another document.** Where a measurement contradicted a source document, the contradiction is
> recorded in place (§1.1, §1.2) rather than silently reconciled.
