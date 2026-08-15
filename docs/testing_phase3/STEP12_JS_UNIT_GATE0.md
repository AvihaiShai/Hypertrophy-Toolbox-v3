# Testing Strategy Phase 3 — Step 12 (JS unit expansion with jsdom) — Gate 0 decision packet

> **Scope**: a decision packet only. **No test, production JS, `package.json`, Vitest config, CI, or
> branch-protection change is made or authorized by this document.**
> **Base**: `origin/main` @ `c404a06`, branch `wt/phase3-jsunit-gate0`, isolated docs-only worktree.
> **Covers**: [`TESTING_STRATEGY_PLANNING.md`](../TESTING_STRATEGY_PLANNING.md) §5 Phase 3 **step 12**,
> and the **unsigned `js-unit` half of D2** (§6, §8.1 row 2, reaffirmed unsigned in §8.1a and §8.1c).
> **Gate 0**: **OPEN**. §8 lists the questions. Implementation **STOPS** until they are answered.
> **Sibling packet**: [`PLANNING.md`](PLANNING.md) in this directory owns Phase 3 **step 11**
> (restore-path fuzz). This file owns step 12 only; the two share no file.

---

## 0. Summary and recommendation

**Recommendation: expand first, promote later — and do not treat the current green streak as the
promotion window.**

The `js-unit` job is genuinely stable: **331 consecutive successful runs** with zero failures over
**13 d 5 h 57 m** (§6). But that stability was earned by a suite that contains **none** of the four
modules step 12 exists to cover. Step 12's own sequence is *expand, **then** two weeks green* —
so the streak measured today is evidence about a **different suite** than the one promotion would
gate. Promotion readiness cannot be inherited across the expansion that changes what the job runs.

Two independent things are therefore both true, and neither alone settles D2:

| Question | Measured answer |
|---|---|
| Is the *job* stable enough to be required? | **Yes.** 331/331 green; the only 3 reds in 16.8 days are one attributable, resolved dependabot incompatibility (§6.2). |
| Is the *suite behind it* worth requiring? | **Not yet.** 5.6 % statement coverage; the four named high-risk modules are at **0 % executed** coverage (§1). |

A required check over a suite that asserts almost nothing buys process cost without buying
protection. The value of promotion is created by the expansion, not by the clock.

**Proposed order**: Packets A → B → C (§2), then a fresh two-week window measured on the
post-expansion suite, then D2. **Packet D (`backup-center.js`) is not recommended for step 12 at
all** — see §2.4 and question Q3.

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

### 1.2 The jsdom claim is already stale — the migration path is proven in-tree

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

**None of the four is executed by any current unit test.** `toast.js` is referenced twice, but only
as `vi.mock('../toast.js', () => ({ showToast: vi.fn() }))` — it is **stubbed, never run**, so its
0 % is invisible to a reader who greps for the filename.

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

### 2.1 Packet A — `workout-controls-persistence.js` *(recommended first)*

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

### 2.2 Packet B — `toast.js`

- **Owns**: `static/js/modules/__tests__/toast.test.js` (new). No production file.
- **Why second**: most-imported module in the app at **0 % executed** coverage, and its legacy-
  signature branch is the highest-value pure logic that E2E structurally cannot reach.
- **Coverage targets**: both signatures and the number-as-`options` form in each; default copy for
  null/undefined message split by type; request-ID suffix present for `error` and **absent** for
  every other type; background-class add/remove; action button wiring (`type`, `aria-label`,
  hide-then-invoke order, `onClick` throwing being caught); both missing-DOM early returns.
- **New work**: this is the first test in the repo to need a **`bootstrap` global fake** (§3.3).

### 2.3 Packet C — `exercises.js`

- **Owns**: `static/js/modules/__tests__/exercises.test.js` (new). No production file.
- **Why third**: heavily E2E-covered already, so unit value is narrower — but the double-delete
  guard and the legacy-signature pairing are real and currently unpinned.
- **Coverage targets**: guard rejects a concurrent second call for the same id and **releases** it
  in `finally` on both success and failure; missing-id early return; `showToast` receiving the
  **legacy** two-argument shape; `notifyVolumeAffectingPlanChange` reason strings; the KI-005
  criterion-4 ordering in `clearWorkoutPlan()`.
- **Collaborators to mock**: `toast.js`, `workout-plan.js`, `workout-plan-events.js`,
  `fetch-wrapper.js` — four, versus zero for Packet A. Plus a `bootstrap.Modal` fake.

### 2.4 Packet D — `backup-center.js` *(NOT recommended for step 12)*

`backup-center.js` is 1069 lines behind a **single** export, `initializeBackupCenter()`, with eight
module-level mutable variables. Unit-testing its named risks at the exported surface means standing
up the entire Backup Center DOM and driving listeners — an integration test wearing a unit test's
clothing, and the most expensive and most brittle of the four by a wide margin.

The alternative — extracting `detailRequestSequence` and the `pendingAction` state machine into
testable seams — is a **production change**, which is outside step 12's test-only scope and outside
anything D2 authorizes. That makes it an owner decision, not an implementer's: **question Q3**.

Recorded so the next session does not silently pick the expensive path by default.

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

  | Input | `min` | `max` |
  |---|---|---|
  | `weight` | `0` | *(none — deliberate, OWNER-5)* |
  | `sets` | `1` | *(none — deliberate)* |
  | `rir` | `0` | `10` |
  | `rpe` | `1` | `10` |

  A test asserting an upper-bound rejection on `weight` or `sets` would be asserting a rule the
  product does not have, and must not be written.
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

> **The gap this reveals, recorded not fixed.** JS unit nodes are the **only** test tier with no
> drift pin. A silently deleted or `.skip`-ed Vitest case is invisible to CI in a way the equivalent
> pytest or Playwright deletion is not — and that gap widens with every packet added. It becomes
> materially more serious **if** `js-unit` is promoted, because a required check would then be
> guarding a node count nothing pins. Extending the inventory to Vitest is **not** proposed here and
> is not in step 12's scope; it is raised as **question Q5**.

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

**Proposed reading of the two-week window**: it starts when the **last** step-12 packet merges, and
is measured on the suite that includes it.

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

## 8. Gate 0 — questions for the owner

**No implementation may begin until these are answered.** Q1 and Q2 are blocking; Q3–Q6 shape scope.

| # | Question | Why it needs the owner | Recommendation |
|---|---|---|---|
| **Q1** | Is step 12's expansion authorized at all? Phase 3 is still a **proposal** — §8.1a and §8.1c both state Phases 2, 3 and 5 are not authorized, and D6's signing covered step 11 *"precondition only"*. | Authorization for Packets A–C does not exist today under any recorded sign-off. | Authorize **A and B**; hold C. |
| **Q2** | Does the two-week window restart on the **post-expansion** suite (§6.4b), or does the existing 331-run streak count toward D2? | Decides whether D2 could be signed tonight or only ~2 weeks after the last packet merges. This is the packet's central judgment. | **Restart.** The current streak is evidence about a suite that does not contain the code in question. |
| **Q3** | `backup-center.js` (Packet D): **skip**, test through the full-DOM `initializeBackupCenter()` surface, or authorize a **production** seam extraction? | Seam extraction is a production change — outside step 12's test-only scope and outside D2. §2.4. | **Skip for step 12.** Revisit as its own packet with its own Gate 0. |
| **Q4** | Drop the `(non-required)` suffix from the job name **in the change before** promotion? | The window closes permanently once the context is protected (§7.3). | **Yes, rename first** — the only sequence that avoids a third misleading name. |
| **Q5** | Extend `generate_test_inventory.py` to pin Vitest node counts? | JS unit is the only tier with no drift pin (§5); the gap matters much more once the job is required. | Not in step 12. Worth its own packet **before** D2 is signed. |
| **Q6** | Correct the stale coverage/jsdom claims in `TESTING_STRATEGY_PLANNING.md` (lines 79, 172, 540-541) and `vitest.config.js`'s comment (§1.1, §1.2)? | `vitest.config.js` is a **config file** this session is barred from touching; the doc lines are a different owner's text. | Yes, as a **separate docs-only packet** — do not fold it into a test packet. |

### STOP

**This packet ends here.** No test file, no production JS, no `package.json`, no `vitest.config.js`,
no CI workflow, and no branch-protection setting has been created or modified, and none may be until
Q1 and Q2 are answered. The recommendation in §0 is a recommendation, not a decision.

---

## 9. Provenance

| Item | Value |
|---|---|
| Base commit | `c404a06` (`origin/main` at session start) |
| Branch / worktree | `wt/phase3-jsunit-gate0`, isolated docs-only worktree |
| Files owned by this packet | This file only |
| Files read, not modified | `AGENTS.md`, `CLAUDE.md`, `docs/MASTER_HANDOVER.md`, `docs/TESTING_STRATEGY_PLANNING.md`, `docs/ai_workflow/QUALITY_GATE.md`, `package.json`, `vitest.config.js`, the 10 files under `static/js/modules/__tests__/`, the four target modules, `.github/workflows/ci.yml`, `scripts/generate_test_inventory.py` |
| Live measurements | 515 `ci.yml` runs resolved at job level (§6); branch protection read via API (§7.1); coverage and test counts read from run `31856035853` (§1.1) |
| Measured on | 2026-08-15 |

> **Every number in §1.1, §6 and §7.1 is a live measurement taken this session, not a figure copied
> from another document.** Where a measurement contradicted a source document, the contradiction is
> recorded in place (§1.1, §1.2) rather than silently reconciled.
