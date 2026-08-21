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

### 2.2 Packet B — `toast.js` *(**SHIPPED** — Gate 1 approved and executed 2026-08-22, **MERGED as PR #406** / squash `987588a`; §10.11, §10.12, §10.13)*

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

---

## 11. Provenance

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
