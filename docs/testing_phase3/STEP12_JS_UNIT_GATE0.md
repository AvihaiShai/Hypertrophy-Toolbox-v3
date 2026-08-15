# Testing Strategy Phase 3 — Step 12 (JS unit expansion with jsdom) — Gate 0 decision packet

> **Scope**: the step-12 decision packet, **plus Packet A as implemented** (§9). Packet A adds
> **one new test file** and nothing else. **No production JS, `package.json`, Vitest config, CI, or
> branch-protection change is made or authorized by this document**, and `js-unit` stays
> **non-required**.
> **Base**: `origin/main` @ `c404a06`, branch `wt/phase3-jsunit-gate0`, isolated docs-only worktree.
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
| [`exercises.js`](../../static/js/modules/exercises.js) | 70 | 2 | 9 | The module-level `deletingExercises` **double-delete guard** and its `finally` cleanup — the one behavior here that is genuinely hard to reach from E2E; the ordering contract in `clearWorkoutPlan()` where `resetWorkoutControlsToDefaults()` must run **after** the refresh (KI-005 criterion 4) |
| [`backup-center.js`](../../static/js/modules/backup-center.js) | 1069 | **1** | 1 (`program-backup`) | `detailRequestSequence` **stale-response race guard** (checked twice per fetch); `pendingAction` confirm/cancel state machine; `SORT_PREF_KEY` `localStorage` round-trip; ~15 listener bindings — **all of it behind one exported `initializeBackupCenter()`** |

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

### 2.2 Packet B — `toast.js` *(AUTHORIZED — second)*

- **Owns**: `static/js/modules/__tests__/toast.test.js` (new). No production file.
- **Why second**: most-imported module in the app at **0 % executed** coverage, and its legacy-
  signature branch is the highest-value pure logic that E2E structurally cannot reach.
- **Coverage targets**: both signatures and the number-as-`options` form in each; default copy for
  null/undefined message split by type; request-ID suffix present for `error` and **absent** for
  every other type; background-class add/remove; action button wiring (`type`, `aria-label`,
  hide-then-invoke order, `onClick` throwing being caught); both missing-DOM early returns.
- **New work**: this is the first test in the repo to need a **`bootstrap` global fake** (§3.3).

### 2.3 Packet C — `exercises.js` *(AUTHORIZED — third)*

- **Owns**: `static/js/modules/__tests__/exercises.test.js` (new). No production file.
- **Why third**: heavily E2E-covered already, so unit value is narrower — but the double-delete
  guard and the legacy-signature pairing are real and currently unpinned.
- **Coverage targets**: guard rejects a concurrent second call for the same id and **releases** it
  in `finally` on both success and failure; missing-id early return; `showToast` receiving the
  **legacy** two-argument shape; `notifyVolumeAffectingPlanChange` reason strings; the KI-005
  criterion-4 ordering in `clearWorkoutPlan()`.
- **Collaborators to mock**: `toast.js`, `workout-plan.js`, `workout-plan-events.js`,
  `fetch-wrapper.js` — four, versus zero for Packet A. Plus a `bootstrap.Modal` fake.

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
  so they require no regeneration. Once E lands, **every later JS test change does** — a reversal of
  the rule stated in §5, and the reason E must come last rather than first.

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
> true for Packets A–C **only**. Once E pins Vitest nodes, every subsequent JS test add, remove, or
> rename **will** trip `Test Inventory Drift` and **will** require a regenerated artifact — the same
> discipline `tests/**` and `e2e/**` already carry. Anyone reading this section after E has merged
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

### STOP — still in force

**No implementation begins in this packet.** Q1 authorizes Packets A–C to be *planned and then
built*; it does not make this document their plan, and it does not authorize code written from it
directly. Each packet needs its own scoped plan first.

As of this commit **nothing has been implemented**: no test file, no production JS, no
`package.json`, no `vitest.config.js`, no CI workflow, and no branch-protection setting has been
created or modified.

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

## 10. Provenance

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
