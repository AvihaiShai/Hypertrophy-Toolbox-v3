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
>
> ⚠️ **THIRD ANNOTATION — 2026-08-22, after the two above. Both are now falsified on the two clauses
> they had left standing, and are annotated rather than rewritten.** **This document necessarily
> predates its own merge**: every sentence above was written on the branch and could not describe what
> happened to it. **The live truth is §13.0.**
>
> - **Packet C is MERGED.** PR [#410](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/410),
>   squash **`9cb6cdc`**, merged **`2026-08-22T17:59:03Z`**. §11's "NOT MERGED" heading and §11.18's
>   "T0 is NOT established by this packet" are annotated in place at each site.
> - **T0 IS established: `2026-08-22T17:59:26Z`** — job `97070630453`
>   (`JS Unit (Vitest, non-required)`) of post-merge `main` run
>   [`32589375849`](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/actions/runs/32589375849),
>   which was **18/18 green** on `9cb6cdc`. The strict 14-day mark is **`2026-09-05T17:59:26Z`**.
>   Full ledger at §13.0.
> - **Packet F planning HAS BEGUN and Packet F implementation remains UNAUTHORIZED.** The scoped plan
>   and its Gate 1 council record are §13. **No generator, inventory artifact, JS test, workflow or
>   branch-protection change is made or authorized by that section.**
>   > ⚠️ **FOURTH ANNOTATION 2026-08-22 — the bullet above is SUPERSEDED.** The owner signed
>   > **Gate 0 and Gate 1** at **§13.16** and authorized implementation, mutation execution,
>   > commit, push and a ready-for-review PR. **Packet F is IMPLEMENTED and its PR is OPEN and
>   > NOT MERGED** (§13.17). A generator change, both inventory artifacts, one new pytest file
>   > and three documentation surfaces *were* changed — by that ruling, not by §13.
>   > **No JS test, workflow, dependency, Vitest-config, branch-protection or repository-setting
>   > change was made, and merging is still unauthorized.**
> - **Q4, Q6 and D2 are still untouched and still unauthorized**, exactly as all three annotations say.
>
> ⚠️ **FIFTH ANNOTATION — 2026-08-23, post-merge reconciliation. Packet F is MERGED, and every
> "NOT MERGED" clause above is falsified. Annotated, not rewritten.** This document, like all four
> annotations before it, was written on a branch and could not describe what happened to it.
>
> - **Packet F is MERGED.** PR [#411](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/411),
>   squash **`2c95bae`**, merged **`2026-08-22T21:52:14Z`**, head `wt/phase3-packet-f-inventory`
>   @ `d7494e2`. `origin/main` is **`2c95bae`**. The post-merge `main` run
>   [`32600832091`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32600832091)
>   (`push`, `2c95bae`) is **18 jobs, all 18 `success`** — read at job level, never off the overall
>   conclusion. **§13.18's merge STOP is DISCHARGED** and annotated at its own site, as is §11.18's.
> - **NT-4 is MEASURED and CLOSED.** The PR's ubuntu `Test Inventory Drift` job —
>   **`97094899990`** on run
>   [`32599231895`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32599231895)
>   (`pull_request`, head `d7494e2`), runner label **`ubuntu-latest`**, conclusion **`success`**,
>   completed **`2026-08-22T21:19:58Z`** — ran step 7, *"Check committed inventory against a fresh
>   Linux regeneration"*, to `success` against a Windows-generated artifact. Cross-platform
>   agreement on the sorted identity list is now **measured, not reasoned**. That whole PR run was
>   **18/18 green**. Annotated at §13.2's NT-4 row, §13.10 step 12, and §13's own preamble.
> - **T0 and the strict mark are UNCHANGED.** T0 remains **`2026-08-22T17:59:26Z`**; the strict
>   14-day mark remains **`2026-09-05T17:59:26Z`**. **Packet F changed no JS test case**, so Q2's
>   restart clause never engaged — §13.10 step 8 gated exactly that, and §13.0's rule says a
>   required predecessor may land inside the window without restarting it. **The window did not
>   restart, and #411's own `mergedAt` is NOT T0.**
> - **The ledger is EXTENDED, at job level, in §13.0.** Two `main` `JS Unit (Vitest, non-required)`
>   results exist from T0 through **`2026-08-23T10:11:56Z`**; **both green**, with **zero** red,
>   missing, skipped or cancelled. It must keep being extended, never restated.
> - **Q4, Q6 and D2 are STILL untouched and still unauthorized**, and **D4** and the `js-unit`
>   half of **D2** are still unsigned. `js-unit` is still **non-required**: branch protection
>   carries **12** required contexts, re-read live 2026-08-23, and
>   `JS Unit (Vitest, non-required)` is **absent** from them. **§7.2 would still add a 13th.**
> - **Packet D stays DROPPED (Q3) and the letter E stays deliberately vacant** (§2.4, §2.6). The
>   step-12 sequence **A → B → C → F is now complete on `main`**; §0.1's revised-gate conditions 1
>   and 2 are satisfied, condition 3 (the 14-day window) is **running**, and condition 4 (a separate
>   owner signature on D2) is **unmet**.
>
> ⚠️ **FIFTH ANNOTATION — 2026-08-23, the Q6 documentation packet. Exactly two clauses above, and
> their ~40 restatements elsewhere in this document, are falsified; both are annotated here rather
> than at every site, because §10.12's rule is that the LIVE block carries the truth.**
>
> - **"Two `main` `JS Unit` results exist from T0 through `2026-08-23T10:11:56Z`" is superseded.**
>   There are now **three**, all green, read at job level at **`2026-08-23T14:01:12Z`**: row 3 is
>   job [**`97193944527`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32639359162/job/97193944527) of run
>   [`32639359162`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32639359162)
>   (`push` / `ca28ec0`, PR #412, 18/18), completed **`2026-08-23T12:26:02Z`**. **§13.0's LIVE LEDGER
>   is the only place that count lives** — do not read it off this bullet at a later session.
>   **T0 is UNCHANGED at `2026-08-22T17:59:26Z`** and the strict mark is UNCHANGED at
>   **`2026-09-05T17:59:26Z`**: PR #412 was documentation-only and changed no JS test case.
> - **"Q6 is untouched" is spent. Q6 is DISCHARGED** — its register row (§8) is updated in place and
>   the correction itself landed in `TESTING_STRATEGY_PLANNING.md` (new **§2.1a**) and in one
>   `vitest.config.js` **comment**. Every *other* clause those ~40 sites assert **still stands
>   verbatim**: **Q4 and D2 remain untouched and unauthorized**, **D4** and the `js-unit` half of
>   **D2** remain unsigned, and `js-unit` remains **non-required**. The Q6 packet changed no
>   executable configuration, no JS test, no dependency, no workflow and no branch-protection
>   setting.
> - **Nothing is claimed about the 2026-08-24 deep-gate cron.** At this read time it has not
>   executed, and this document asserts nothing about it.
>
> ⚠️ **SIXTH ANNOTATION — 2026-08-23, after the Q6 packet MERGED. Exactly one clause of the
> fifth annotation is now spent; every other clause it asserts still stands verbatim.**
>
> - **The Q6 packet is MERGED.** PR
>   [#413](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/413), squash **`b0aa393`**,
>   merged **`2026-08-23T18:03:43Z`**. Its diff is **exactly three** tracked files:
>   [`TESTING_STRATEGY_PLANNING.md`](../TESTING_STRATEGY_PLANNING.md), **this document**, and
>   [`vitest.config.js`](../../vitest.config.js) — **comment-only in that file, no executable
>   configuration changed**. **Zero** files under `static/js/**`. Post-merge `main` run
>   [`32656837264`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32656837264),
>   **18 jobs, all 18 `success`**, read at job level.
> - **The fifth annotation's *“the `main` run it produces on merge will mint row 4, and whoever
>   lands it owes that row”* is DISCHARGED.** Row 4 is job
>   [`97236769067`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32656837264/job/97236769067),
>   **`success`**, completed **`2026-08-23T18:04:10Z`**, and it is written into §13.0's
>   *LIVE LEDGER* — which remains **the only place any ledger count lives**. **Do not read a
>   count off this bullet at a later session.**
> - **T0 is UNCHANGED at `2026-08-22T17:59:26Z`** and the strict mark is UNCHANGED at
>   **`2026-09-05T17:59:26Z`**: #413 changed **no JS test case**, so Q2's restart clause did
>   not engage.
> - **Everything else still stands verbatim.** **Q4 and D2 remain untouched and unauthorized**,
>   **D4** and the `js-unit` half of **D2** remain **unsigned**, `js-unit` remains
>   **non-required** (branch protection re-read live 2026-08-23: **12** required contexts,
>   `JS Unit (Vitest, non-required)` **absent**), and **KI-010 / KI-011 remain OPEN**.
> - **Still nothing is claimed about the 2026-08-24 deep-gate cron.** At this read time it has
>   not executed either.
>
> ⚠️ **SEVENTH ANNOTATION — 2026-08-24, after PR #414 merged and after the 2026-08-24
> deep-gate cron executed. Exactly two clauses of the sixth annotation are now spent; every
> other clause it asserts still stands verbatim.**
>
> - **Row 4's ledger reading is superseded by a FIVE-row one.** Row 5 is job
>   [`97247194117`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32661056527/job/97247194117),
>   **`success`**, completed **`2026-08-23T19:23:22Z`**, on `main` run
>   [`32661056527`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32661056527)
>   (`push` / `31659a5`, PR [#414](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/414),
>   18/18). It is written into §13.0's *LIVE LEDGER* — its **post-#414** block, which is now the
>   live one and **the only place any ledger count lives**. **Do not read a count off this bullet
>   at a later session.**
> - **The "nothing is claimed about the 2026-08-24 deep-gate cron" clause is DISCHARGED, and it
>   resolved the way both earlier annotations predicted it would have to.** The cron fired: run
>   [`32688747703`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32688747703),
>   event `schedule`, head `31659a5`, **7/7 jobs `success`** read individually, `visual-linux`
>   (job `97318476983`) **executed and not skipped** with *Assert compare mode wrote no baseline*
>   passing at step level. **It changed nothing in this document's window**, because
>   `deep-gate.yml` declares **no** `js-unit` job — the standing clause *"it can only ever add a
>   row here by not adding one"* is now exercised rather than predicted. What it is evidence for
>   — R1-D3's three-consecutive-green-scheduled-runs clock, recorded at **2 of 3** — lives in
>   [`release_pipeline/PLANNING.md`](../release_pipeline/PLANNING.md), not here.
> - **One scope repair travels with row 5, and it is stated here because it changes how a later
>   session must read the tally.** §6.1 fixes the qualification scope at **`ci.yml`
>   (`CI/CD Pipeline`)**. Through row 4 the broad "every `main` run" query and that narrow scope
>   agreed by accident; on 2026-08-24 they diverge, and **a `main` run belonging to another
>   workflow is not a qualification attempt and must never be tallied as a `js-unit` result
>   "missing"**. §13.0's post-#414 block carries the classification.
> - **T0 is UNCHANGED at `2026-08-22T17:59:26Z`** and the strict mark is UNCHANGED at
>   **`2026-09-05T17:59:26Z`**: #414 changed **no JS test case**, so Q2's restart clause did not
>   engage.
> - **Everything else still stands verbatim.** **Q4 and D2 remain untouched and unauthorized**,
>   **D4** and the `js-unit` half of **D2** remain **unsigned**, `js-unit` remains
>   **non-required** (branch protection re-read live 2026-08-24: **12** required contexts,
>   `JS Unit (Vitest, non-required)` **absent**), and **KI-010 / KI-011 remain OPEN**.
>
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
>
> ⚠️ **ANNOTATION 2026-08-23 — Q6 is now DISCHARGED, in its own packet, and the numbers in this
> paragraph have themselves drifted.** All three surfaces are corrected: the two
> `TESTING_STRATEGY_PLANNING.md` prose sites and its §8.6 rows are annotated in place with a new
> **§2.1a** carrying the live reading, and `vitest.config.js`'s comment now quotes **no** module
> counts at all. **The `9 of 57` / `5.6 %` above is the 2026-08-15 reading of run `31856035853`
> and is preserved as that record — do not quote it as current either.** Re-measured
> **2026-08-23** from job [`97193944527`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32639359162/job/97193944527) (run `32639359162`, `push` /
> `ca28ec0`) and reproduced
> locally: **13 files / 231 cases**, statements **7.8 %** (582 / 7,453), **57** files under
> `static/js` excluding `*.test.js`, **13** with any coverage, **44** at exactly 0 %, and **5** test
> files carrying the jsdom pragma. That packet was **documentation- and comment-only**: no
> executable configuration, no JS test, no workflow and no branch-protection change. **Q4 and D2
> remain untouched and unauthorized.**

### 1.2 RECORDED FINDING — the jsdom claim is stale; the migration path is proven in-tree

`TESTING_STRATEGY_PLANNING.md` line 79 states *"`jsdom` is installed but **zero test files opt into
it**"*, and line 172 repeats *"`jsdom` installed but unused"*. **Both are false as of `c404a06`.**

> ⚠️ **ANNOTATION 2026-08-23 — corrected at source by the Q6 packet.** Both sites are now annotated
> in place (they have since moved to lines **125** and **218** of that file, which is why a line
> number is a poor anchor), and the live reading lives in its new **§2.1a**. The count below has
> also grown: **five** test files carry the pragma as of `ca28ec0` — the two listed here plus
> `exercises`, `toast` and `workout-controls-persistence`. The two-row table is left as the
> `c404a06` record.

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

> **CORRECTION 1 of 3, 2026-08-22 (`b52df68`) — the `exercises.js` E2E count was an over-count:
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

> **CORRECTION 2 of 3, 2026-08-22 — the KI-005 criterion-4 claim in this row was an over-read, and it
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

**The cross-module contract worth pinning first.** `exercises.js:12`, `:36` **and `:68`** call
`showToast(message, true)` — the **legacy two-argument** signature — while `:31` and `:59` call
`showToast(message)`, the legacy **one-argument** form. **Three two-argument and two one-argument
calls, five sites in total** (measured, §11.2). `toast.js:15` routes the two-argument form through
the backward-compatibility branch. Nothing currently asserts that this pairing works; a well-meant
cleanup of either side breaks the other silently, and every E2E spec would still pass as long as
*some* toast appears.

> **CORRECTION 3 of 3, 2026-08-22 (owner-authorized after the execution record) — the paragraph
> above named `:12` and `:36` only and OMITTED `:68`.** It has read that way since 2026-08-15, and it
> is the **same undercount** the owner authorized correction 4 to repair at §2.3. `unslop-reviewer`
> raised it at execution; §11.17 **routed it to the owner rather than fixing it**, because repairing
> it would be a **fifth** correction outside §11 and the Gate 1 ruling had covered four. **The owner
> authorized that fifth correction explicitly on 2026-08-22**, after the execution record was written.
> It is applied here and recorded as **row 5** of §11.2's *Corrections applied* table.
>
> The measured split it now states — two-argument `:12`, `:36`, `:68`; one-argument `:31`, `:59` — is
> **§11.2's table unchanged**; this edit brings §1.3's prose into line with a measurement the document
> already held, and invents no new one. **No test, production, workflow or configuration file changes**,
> so every measured result recorded in §11.17 — 29 cases, 202 → 231, the 42-row mutation matrix, the
> coverage and E2E figures — **stands unaffected**.
>
> **This block also moves §1.3's own denominator from 2 to 3.** The two blocks above it were written
> as *"1 of 2"* and *"2 of 2"* when §1.3 carried exactly two corrections; they are renumbered *of 3*
> here because §1.3 now carries three. That is **not** the renumbering §11.17 declined — that one
> proposed re-scoping these ordinals onto §11's counter, which they still do not follow. Their
> **order and content are untouched**.

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

> ⚠️ **ANNOTATION 2026-08-23 — the heading's "PR open and NOT merged" is FALSE and is annotated, not
> rewritten.** **Packet C is MERGED**: PR
> [#410](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/410), squash **`9cb6cdc`**, merged
> **`2026-08-22T17:59:03Z`**, post-merge `main` run `32589375849` **18/18 green** at job level. It
> established **T0 = `2026-08-22T17:59:26Z`** (§13.0). §11.18's merge STOP is discharged at its own
> site.

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

> **CORRECTED 2026-08-22 (Gate 1 owner ruling, correction 4 of 5 outside §11; plan-hygiene correction
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

> ⚠️ **ANNOTATION 2026-08-23 — Packet F is MERGED, so this subsection is now the record of a shipped
> packet rather than a forward plan. Annotated, not rewritten.** PR
> [#411](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/411), squash **`2c95bae`**, merged
> **`2026-08-22T21:52:14Z`**; post-merge `main` run `32600832091` **18/18 green** at job level.
> **§0.1's revised-gate condition 2 is satisfied.** The *"Note it will trip its own gate, once and
> deliberately"* bullet below is now a measured fact (§13.10 step 2, §13.17); the *"Ordering caution"*
> bullet's reversal is **in force on `main` from `2c95bae` onward** — every later JS test add, remove
> or **rename** must ship a regenerated `docs/test_inventory/` artifact in the same PR. **What Packet F
> did NOT do:** it added no required context, changed no branch-protection setting, and promoted
> nothing. `js-unit` is still non-required and **D2 is still unsigned**.

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

> ⚠️ **ANNOTATION 2026-08-22 — §5 EXPIRES WHEN PACKET F MERGES, and is annotated, not rewritten.**
> **Packet F's PR is open and NOT merged** (§13.18), so every statement below is still literally
> true of `main` today. It stops being true the moment the PR lands.
> Everything below was measured and true for Packets A–C, and **the five-row table is now
> five-of-six**: Packet F added a **sixth** pinned surface — per-file Vitest case counts **and the
> full sorted list of case identities** — so the "Adding `static/js/modules/__tests__/*.test.js`
> touches none of them" sentence becomes **false the moment Packet F merges**. Every later JS test
> add, remove or **rename** will then trip `Test Inventory Drift` and must ship a regenerated
> artifact in the same PR.
> §5's own closing note predicted exactly this. The live surface list is
> [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)'s six-row table; the implementation record is
> **§13.17**.
>
> ⚠️ **FOLLOW-ON ANNOTATION 2026-08-23 — §5 HAS NOW EXPIRED. The condition the annotation above states
> in the future tense has occurred.** Packet F merged as **`2c95bae`** (PR
> [#411](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/411),
> `2026-08-22T21:52:14Z`). **Everything below this banner is now HISTORY, not a description of `main`.**
> Specifically: *"`scripts/generate_test_inventory.py` contains **zero** references to `vitest`"* is
> **false on `main`**; the five-row table below is **five of six**; and *"Adding
> `static/js/modules/__tests__/*.test.js` touches none of them"* is **false** — it now trips the
> **required** `Test Inventory Drift` context, whose ubuntu run also closed **NT-4**. The
> **"No inventory regeneration is required"** sentence was true for Packets A–C **only** and must not
> be read forward. The section is left standing as the pre-Packet-F measurement it was.

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

> ✅ **THE WINDOW IS NOW RUNNING — annotation 2026-08-22.** The conditions this subsection describes in
> the future tense have been met. **The final expansion packet (Packet C) landed as `9cb6cdc`**, and
> **T0 = `2026-08-22T17:59:26Z`** (job `97070630453` of run `32589375849`). **The strict 14-day mark is
> `2026-09-05T17:59:26Z`.** The live ledger, and the rule that Packet F may land inside the window
> without restarting it, are at **§13.0**.

---

## 7. The exact branch-protection change, if the owner later signs D2

Recorded so it is unambiguous when the time comes. **Nothing in this section is executed by this
packet.**

### 7.1 Measured current state

> ⚠️ **ANNOTATION 2026-08-22 — the 2026-08-15 reading below is SUPERSEDED and is annotated, not
> rewritten.** Branch protection now carries **12** required contexts, not 11:
> `JS Supply Chain (npm audit, non-required)` was promoted by PR #409 (`a937116`) on 2026-08-22.
> **What has not changed, and is the load-bearing half for Packet F:** `Test Inventory Drift` is
> still required, and **`JS Unit (Vitest, non-required)` is still absent.** Consequently the
> promotion in §7.2 would add a **13th** context, not a 12th, and the whole `checks` array it must
> resend has **12** entries. **Packet F changed no branch-protection setting** — it pinned the Vitest
> surface *inside* the already-required `Test Inventory Drift` context, which is §2.5's whole design.

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

> ⚠️ **ANNOTATION 2026-08-22 — read "12th" as "13th" and "11 existing entries" as "12".** See §7.1's
> annotation: the live count moved to 12 with PR #409, and the count below is preserved as the
> 2026-08-15 measurement it was. **Re-measure before executing this section** — it has now been wrong
> once, and its failure mode is silently un-protecting a context by omitting it from the resent array.

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
| **Q6** | Correct the stale coverage/jsdom claims in `TESTING_STRATEGY_PLANNING.md` (lines 79, 172, 540-541) and `vitest.config.js`'s comment (§1.1, §1.2)? | **DISCHARGED 2026-08-23**, as the recommended **separate docs-only packet** — based on `main` @ `ca28ec0`, in its own isolated worktree. All figures were **re-measured**, not carried over: job [`97193944527`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32639359162/job/97193944527) gives **13 files / 231 cases**, statements **7.8 %** (582 / 7,453), **57** files under `static/js` excluding `*.test.js`, **13** with any coverage, **44** at exactly 0 %, **5** test files carrying the jsdom pragma. The three prose sites (now lines **125**, **137**, **218** — the line numbers in this cell moved, which is why they are a poor anchor) and the §8.6 rows are **annotated in place**, with the live reading in a new **§2.1a**; `vitest.config.js`'s comment now quotes **no** module counts, so it cannot rot again. **Comment-only in that file — no executable configuration changed.** Q4 and D2 were **not** drawn in. |

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

> ⚠️ **ANNOTATION 2026-08-22 — true for Packet A, and Packet F ends it.** There are **six** pinned
> surfaces once Packet F merges, and the sixth is exactly the one described as missing here.

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

> ⚠️ **STALE AS OF 2026-08-27 — annotated, deliberately NOT re-derived (owner ruling OD-10).**
> The **KI-010 fix** (Packet U3a, `docs/toast_type_word_collision/PLANNING.md`, Gate 1 signed
> 2026-08-27) changed `toast.test.js`. **What is now false in §10.3 and §10.5, named so a reader
> does not trust it:**
>
> - **The "47 cases" arithmetic in this section, and the totals line that derives it.** The file is
>   **61** cases and the suite is **13 files / 245 cases**. `TEST_INVENTORY.json` is the live figure.
> - **B45's and B43's rows**, which describe the *pinned defect* in the present tense. Both cases
>   were **deliberately inverted** and parametrised over four type words as **B45a–d** and
>   **B43a–d**; **B46a–d** and **B47a–d** are new. The red a reviewer sees on those rows without the
>   production fix is the **intended review signal**, not a regression.
> - **§10.5's mutation kill sets.** N8 loses B43; N10 and N12 gain the new B45 family. The
>   disclosure elsewhere in §10.5 that *"B43 is not independently killed"* is **inverted** — B43a
>   acquires an independent kill, because `arguments.length` now distinguishes an omitted argument
>   from an explicit `undefined`.
> - **The two signed Gate 1 checkboxes** further down that reference the 47-case matrix and *"the
>   cases with no isolating killer (B23, B43)"*.
> - **EVERY `toast.js:NN` LINE ANCHOR IN THIS DOCUMENT.** The fix inserted a predicate near the top
>   of the file, so every anchor below it moved by roughly **+45** — §10.5's mutation table alone
>   carries sixteen. An anchor followed from here lands on unrelated code **with no other warning
>   than this bullet.** The post-fix mapping is `toast_type_word_collision/PLANNING.md` §i.2.
>   **Re-anchor by measuring, never by adding the offset.**
>
> **Nothing in §10.3 or §10.5 is edited.** Both remain the record of what Packet B measured and
> signed, which was accurate when written. **Re-deriving §10.5's kill sets against the post-fix
> suite is a packet of its own and is not authorized here.** The live mutation evidence for the
> post-fix file is `toast_type_word_collision/PLANNING.md` §v2.8, whose every arm was executed
> against the full 245-case suite.


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

> ⚠️ **STALE AS OF 2026-08-27 — see the annotation under §10.3.** The kill sets below, and every
> `toast.js:NN` anchor in this table, describe the **pre-fix** module. Not re-derived, per owner
> ruling OD-10.

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

> ⚠️ **STALE AS OF 2026-08-27 — see the annotation under §10.3.** **KI-010 is FIXED and its row is
> now `Mitigated`.** Everything above is the record of what Packet B measured, and it was accurate
> when written: *"still Open and still unfixed"*, *"Pinned, not fixed"*, and B43/B45 pinning the
> defect are all **superseded**. B45 and B43 were deliberately **inverted** and parametrised; the
> citation to a comment at `toast.test.js:563` no longer resolves — that comment was replaced.
> Not re-derived, per owner ruling OD-10.

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
>
> ⚠️ **ANNOTATION 2026-08-22 — falsified for Packet F ONLY, and annotated rather than rewritten.**
> **Packet F is no longer "unstarted": planning has begun at §13**, and Packet C has since **merged**
> (`9cb6cdc`). **Packet F implementation remains UNAUTHORIZED**, and **Q4, Q6 and D2 remain untouched
> and unauthorized** — that half of the clause still stands exactly as written.
>
> ⚠️ **FURTHER ANNOTATION 2026-08-22 — "implementation remains UNAUTHORIZED" is now FALSE.**
> Gate 0 and Gate 1 were signed at **§13.16**; Packet F is implemented, with an open, unmerged
> PR (§13.17). **Q4, Q6 and D2 remain untouched and unauthorized** — that half still stands.
>
> ⚠️ **THIRD FURTHER ANNOTATION 2026-08-23 — "an open, unmerged PR" is now FALSE too.**
> **Packet F MERGED** as PR #411, squash **`2c95bae`**, at **`2026-08-22T21:52:14Z`**; post-merge
> `main` run `32600832091` is **18/18 green** at job level. **Three of the five items this section
> listed have now moved** — the KI-010/KI-011 follow-up, Packet C, and Packet F. **Two have not, and
> they are the surviving clause, restated exactly: promotion of `js-unit` (Q4 / D2) and Q6 remain
> untouched and unauthorized.** **KI-010 and KI-011 are still `Open`** — that item moved by being
> *registered*, which is not the same as being fixed or mitigated, and neither is.

---

## 11. Packet C — scoped plan (`exercises.js`) — **PLAN v2; GATE 1 APPROVED AND EXECUTED 2026-08-22, NOT MERGED** *(the heading read "GATE 1 NOT YET APPROVED" until the ruling at §11.16)*

> ⚠️ **ANNOTATION 2026-08-23 — the heading's "NOT MERGED" is FALSE and is annotated, not rewritten.**
> **Packet C MERGED** as PR [#410](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/410),
> squash **`9cb6cdc`**, at **`2026-08-22T17:59:03Z`**; post-merge `main` run `32589375849` was
> **18/18 green** at job level, and its `JS Unit (Vitest, non-required)` job **`97070630453`**
> established **T0**. §11.18's merge STOP is discharged below.

> ⚠️ **ANNOTATION 2026-08-22 — "NOT MERGED" in the heading above is FALSIFIED and is annotated, not
> rewritten.** **Packet C MERGED** as PR #410, squash **`9cb6cdc`**, at **`2026-08-22T17:59:03Z`**.
> The heading records what was true when the section was written on the branch; §13.0 carries the
> live state and the T0 ledger it started.

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

**FIVE** edits are made outside §11 — **one** by Plan v1, **two more** by Plan v2, **one more by
the Gate 1 owner ruling of 2026-08-22**, and **one more by the owner's separate authorization of
2026-08-22, after the execution record was written** — and all five are listed here so nothing in the
diff is a surprise. *(Plan v1 said "exactly one"; council C-1(d) and C-13 each added one, the owner's
§2.3 ruling added the fourth, and the post-execution authorization added the fifth, so that sentence
has now been corrected three times.)*

| # | Where | Change | Why it was narrowly necessary |
|---|---|---|---|
| **1** *(Plan v1)* | **§1.3**, the `exercises.js` row's *"E2E specs touching it"* cell, plus its adjacent note block | **9 → 3**, with the grep stated and **every** file it returns dispositioned (rebuilt by Plan v2 per council C-11) | The cell states a **measured quantity** that is **false as measured**. Packet C's entire justification is *what E2E does not reach*, so leaving a 3× over-count in the document that authorizes it would have a reviewer weighing this plan against a coverage picture that does not exist |
| **2** *(Plan v2, council C-1)* | **§1.3**, the same row's *"untested high-risk behavior"* cell, plus a second note block | *"the ordering contract … must run **after** the refresh (KI-005 criterion 4)"* → **"runs only after the server clear succeeds and never on the error path"** | The old wording is a **false attribution to a named criterion**, present since 2026-08-15, and it is the **source** of the over-read that Plan v1 then built C19 and P33 on. `ki005_controls_persistence/PLANNING.md:448` says the reset is called *after the successful server clear* and that its "LAST" is **internal to the helper** (`workout-plan.js:408-413`), not a position relative to the refresh. Leaving it would leave the document arguing against itself, since §11.3-C19 now labels the call order as characterization |
| **3** *(Plan v2, council C-13)* | The document's opening **Scope** block, lines 13-14 | Annotated in place: *"Packet C now has a Gate 1 plan at §11; still unauthorized"* | The block says **Packet C** is *"untouched and still unauthorized"*. §11 falsifies the first half. This is the standard §10.12 discipline — *"this commit falsified prose that was true before it"* — and Packet B annotated **four** such places. The block is **annotated, not rewritten**, so the original sequence stays legible |
| **4** *(Gate 1 owner ruling, 2026-08-22)* | **§2.3**, the *Coverage targets* bullet, plus a note block under it | *"`showToast` receiving the **legacy** two-argument shape"* → **both** legacy arities, **3 two-argument** and **2 one-argument**, as measured; and *"the KI-005 criterion-4 ordering"* → **"runs only after the server clear succeeds and never on the error path"**, with contract and characterization separated explicitly | Both claims are **false as measured**, and §2.3 is the *source* wording — the same false criterion-4 attribution corrected at §1.3 (row 2) survives here, so a reader who starts at §2.3 re-derives exactly the over-read §11.15-C-1 unwound. The *"Why third"* framing is **not** touched: it is superseded in §11.2 above, where the measurement lives |
| **5** *(owner authorization, 2026-08-22, after the execution record)* | **§1.3**, the *"cross-module contract worth pinning first"* paragraph, plus a third note block under it | *"`exercises.js:12` and `:36` call `showToast(message, true)`"* → **`:12`, `:36` and `:68`** as the two-argument sites, with `:31` and `:59` named as the one-argument form and the total stated as **three plus two** | The sentence named **2 of the 3** two-argument sites — the **same undercount** corrected at §2.3 by row 4, surviving in the earlier section that a reader reaches first. `unslop-reviewer` raised it at execution and §11.17 **routed it to the owner unfixed**, because it would have been a fifth correction against a ruling that covered four. The owner authorized it separately. It is **prose only** — §11.2's measured table, the test file and every measured result in §11.17 are unchanged — and it removes item 4 from §11.18's follow-up list |

Nothing else in §0–§10 is modified, and no file outside
`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` is modified. **§2.3's *Coverage targets* bullet IS now
edited** (row 4 above, added by the Gate 1 owner ruling — this supersedes Plan v2's *"§2.3 is still not
edited"*, and its *"Why third"* framing remains untouched and superseded in place). **§1.3's
cross-module-contract paragraph is now edited too** (row 5, added by the owner's post-execution
authorization); §1.3's own correction blocks are renumbered *of 2* → *of 3* to match, with their order
and content untouched. Neither
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
`static/js/**/*.js`** (council C-19). These are not part of QUALITY_GATE's five pinned surfaces
(**six** once Packet F merges — and its new sixth surface is a *different* mechanism from the one
described here: it trips the inventory gate, not the full-pytest gate), so
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
> *(At the Gate 1 ruling the owner authorized a **fourth**, in §2.3 — question 6 is annotated below.
> A **fifth**, in §1.3, was authorized separately on 2026-08-22 after the execution record; the running
> total outside §11 is now **five**, and §11.2's table is the ledger.)*

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
   "Corrections applied".)* — ***as posed at Gate 1; a FIFTH was authorized separately on 2026-08-22,
   after execution (§11.2 row 5), and the question text is left as it was asked.***
   **(a)** §1.3's E2E count **9 → 3**, with the grep stated and all nine files
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
   > ⚠️ **ANNOTATION 2026-08-22 — "untouched" is falsified for Packet F only.** Packet F **planning**
   > has begun at §13; **implementation remains UNAUTHORIZED**. **Q4 and Q6 remain untouched.** The
   > question itself was answered as written at the time it was put.
   > **FURTHER ANNOTATION, same day:** implementation was subsequently **authorized and executed**
   > (§13.16, §13.17). **Q4 and Q6 are still untouched.**

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
>
> ⚠️ **FURTHER ANNOTATION 2026-08-22 — "Packet F ... still untouched" is now FALSE.** Packet F was
> authorized at §13.16 and executed at §13.17; its PR is open and unmerged. **Q4 / D2 promotion /
> Q6 remain untouched and unauthorized.**

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
| **C-13** | The document's Scope block is falsified by §11 and is not annotated | `architecture` (5) | **ACCEPTED.** Lines 13-14 said *"**Packet C** … untouched and still unauthorized"*; Packet C is no longer untouched. Packet B set the standard: §10.12 annotated **four** places outside §10 *"because this commit falsified prose that was true before it"*. The block is **annotated, not rewritten**, and recorded as **correction 3 of 5** *(3 of 3 when Plan v2 was written; the Gate 1 owner ruling added a fourth, in §2.3; the owner's post-execution authorization of 2026-08-22 added a fifth, in §1.3)* — so §11.2's "exactly one edit outside §11" is itself corrected |
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
*Corrections applied* table, which carried **three** rows at Plan v2, **four** after the Gate 1 owner
ruling added the §2.3 correction, and **five** after the owner's post-execution authorization of
2026-08-22 added the §1.3 one. **Nothing outside
`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` was touched**, no test file was created, no production JS
was changed, no mutation harness was built, and nothing was committed or pushed.

**Counts after Plan v2:** cases **29** (unchanged), suite delta **202 → 231** (unchanged), files
**12 → 13** (unchanged), mutations **40 → 42**, EOL-risk rows **10 → 13**, corrections outside §11
**1 → 3** *(→ **4** at the Gate 1 owner ruling; → **5** at the owner's post-execution authorization of
2026-08-22)*, owner questions **6 → 7**, risk rows
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
| **6** | The corrections outside §11 | **ALL THREE STAND**, and a **fourth is authorized** in **§2.3**: replace the false *"KI-005 criterion-4 ordering"* wording with the actual contract (reset only after a successful server clear, never on the error path); describe the measured toast call shapes accurately (**three two-argument** and **two one-argument** legacy-shaped calls); and distinguish contractual behavior from characterization of the current refresh / reset / notification order. Applied — §11.2's *Corrections applied* table carried **four** rows at this ruling. **ANNOTATED 2026-08-22 (after execution): the owner authorized a FIFTH correction, in §1.3, repairing the same two-argument `showToast` undercount that this ruling repaired at §2.3; the table now carries FIVE rows.** This ruling itself is unchanged — it covered four, and the fifth is a separate authorization, not a re-reading of this one |
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
| **PR CI** — [#410](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/410), head **`5cf2a04`** | **18/18 pass, zero pending**, run **32581336508**. **`JS Unit (Vitest, non-required)` kept its exact name and stayed non-required**, passing in 26 s. The check count grew **17 → 18** mid-run — `E2E Functional (Chromium)` is the aggregating job and appears only once both shards report, which is why a run must be polled to **zero pending** rather than judged on a first listing |

> **This CI row records the run for `5cf2a04`, the commit that carried the work — and the commit that
> ADDS this row is necessarily covered by a later run.** The regress is stopped here deliberately: the
> evidence that matters is the run over the test file and the mutation-verified state, and a docs-only
> follow-up commit on the same branch cannot change what that run measured. **The head SHA at merge
> time is what the merge confirmation should name**, not this one.

**FIVE STATUS ANNOTATIONS were made at execution time — three outside §11 and two inside it — and
they are NOT corrections.** The §11.2 *Corrections applied* table counts **five** edits that repair
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

> ⚠️ **ANNOTATION 2026-08-22 — this is a META-claim about the annotations, and it is now falsified in
> its own terms.** A **fourth** annotation round exists (the header's THIRD ANNOTATION, §6.5, §11
> and §11.18) and it does **not** leave the clause untouched: **Packet F planning has begun at §13**,
> so "untouched" is no longer true of Packet F. **The surviving clause, restated exactly:**
> **Packet F implementation remains UNAUTHORIZED, and Q4 / D2 promotion / Q6 remain untouched and
> unauthorized.** Recorded here rather than rewritten, because a sentence whose subject is the
> annotation record must itself be annotated when the record grows.
>
> ⚠️ **AND THE RECORD GREW AGAIN, 2026-08-22.** By its own rule this sentence is annotated a
> second time: **Packet F implementation is no longer unauthorized** — Gate 0 and Gate 1 were
> signed at **§13.16** and executed at **§13.17**, with **merge** still requiring its own
> confirmation. **Q4 / D2 / Q6 remain untouched and unauthorized.**
>
> ⚠️ **AND AGAIN, 2026-08-23 — by the same self-imposed rule.** The merge confirmation was
> given and **Packet F merged as `2c95bae`** (PR #411). **The clause that survives every round of
> this chain, and is the only one left: Q4 / D2 promotion and Q6 remain untouched and
> unauthorized.**

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
| Renumber §1.3's *"CORRECTION 1 of 2 / 2 of 2"*, a third numbering scheme | **Declined, and the decline still stands on its stated ground:** those ordinals are **scoped to §1.3's own corrections**, and renumbering ratified prose to serve a *different section's* counter is the failure this document already fought once (§2.6). **ANNOTATED 2026-08-22 (after execution): the denominator has since moved to *of 3* — not to follow §11's counter, but because the owner's fifth authorized correction gave §1.3 a THIRD correction of its own.** *"Correct as written"* was true when written and this later edit falsified it; the ordinals' order and content are untouched |

**One finding was ROUTED TO THE OWNER rather than fixed — and has since been AUTHORIZED and FIXED:**
§1.3's prose named `exercises.js:12` and `:36` as the legacy two-argument sites and **omitted `:68`** —
the same undercount the owner authorized correction 4 to repair at §2.3. **It was not repaired at
execution**, because that would have been a **fifth** correction outside §11 and the Gate 1 ruling
covered four; it was recorded instead as item 4 of §11.18's follow-up list.

> **RESOLVED 2026-08-22 — the owner authorized the fifth correction explicitly, after this execution
> record was written.** §1.3's paragraph now names **`:12`, `:36` and `:68`** as the two-argument sites
> and **`:31` and `:59`** as the one-argument form, three plus two, five in total. The correction is
> **prose only**, in **one tracked file** — `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md`. It is recorded
> as **row 5** of §11.2's *Corrections applied* table and **removed from §11.18's follow-up list**, which
> is three items again.
>
> **Every measured result above stands**, because neither production nor test code changed: 29 cases,
> **202 → 231**, the **42-row** mutation matrix (41 killed, P40 the declared survivor), the coverage
> figures, the four local Chromium specs, and the `5cf2a04` CI run. **The 42-row local mutation matrix
> was deliberately NOT re-run for this documentation correction** — the discipline that a test-file
> change invalidates every measured row (see the two deleted assertions above) applies to *test-file*
> changes, and this is not one.

### 11.18 STOP — merge — **DISCHARGED 2026-08-22 (recorded 2026-08-23)**

> ✅ **DISCHARGE 2026-08-23.** The STOP below was honoured: the PR was left ready-for-review, the
> owner gave the separate explicit confirmation the protocol requires, and **PR #410 merged as
> `9cb6cdc` at `2026-08-22T17:59:03Z`**. Everything the STOP lists **other than the Packet C merge**
> still stood at the moment of discharge; **Packet F has since been separately authorized and merged**
> (`2c95bae`, PR #411 — §13.16, §13.18), and **Q4, Q6 and D2 remain unauthorized and untouched**.
> The three numbered follow-ups below are **still open and still unauthorized**; none was taken by
> Packet F or by this reconciliation. The section is annotated, not rewritten.

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

> **A FOURTH item stood here and is now CLOSED, not dropped.** Raised by `unslop-reviewer` at execution:
> *"§1.3's prose names `exercises.js:12` and `:36` as the legacy two-argument `showToast` sites and omits
> `:68`"* — left unrepaired at execution because it would have been a **fifth** correction outside §11
> and the Gate 1 ruling covered four. **The owner authorized that fifth correction on 2026-08-22 and it
> is applied** (§11.2 row 5, §1.3's *CORRECTION 3 of 3*, §11.17's RESOLVED block). It is removed from
> the numbered list above because it is no longer open; the list is **three** again, matching its own
> heading. The three items above are untouched and still open.

**T0 is NOT established by this packet.** It begins only after a separately authorized Packet C merge
**and** the first successful post-merge `main` `JS Unit (Vitest, non-required)` run.

> ⚠️ **ANNOTATION 2026-08-22 — the paragraph immediately above is FALSIFIED and is annotated, not
> rewritten.** It was correct as a statement about *this packet*: Packet C did not establish T0, and
> could not. **Both of its two conditions have since been met.** The owner authorized the merge
> separately; PR #410 merged as **`9cb6cdc`** at **`2026-08-22T17:59:03Z`**; the first successful
> post-merge `main` `JS Unit (Vitest, non-required)` run is job **`97070630453`** of run
> **`32589375849`**, completed **`2026-08-22T17:59:26Z`**. **T0 = `2026-08-22T17:59:26Z`.**
>
> The **STOP above still stands as written for everything it lists except the Packet C merge**, which
> the owner has since authorized and which has happened. **Packet F remains unauthorized for
> implementation** — §13 is planning and a Gate 1 council record only, and it makes no generator,
> inventory, JS-test, workflow or branch-protection change. **Q4 / D2 / Q6 are untouched.**
>
> ⚠️ **FURTHER ANNOTATION 2026-08-22 — the "Packet F remains unauthorized" sentence is now FALSE.**
> Gate 0 and Gate 1 were signed at §13.16 and Packet F is implemented (§13.17): the generator and
> both inventory artifacts DID change. **No JS-test, workflow or branch-protection change was
> made, merge is still unauthorized, and Q4 / D2 / Q6 are still untouched.** *(Found by review:
> §11.18 carries TWO such sentences and the first pass annotated only one — a partially-annotated
> record is its own defect, and the packet had already listed §11.18 as done.)*

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

---

## 13. Packet F — scoped plan (Vitest inventory + drift enforcement) — PLAN v2; **GATE 0 AND GATE 1 APPROVED AND EXECUTED 2026-08-22, NOT MERGED** *(the heading read "GATE 1 NOT YET APPROVED" until the ruling at §13.16)*

> ⚠️ **ANNOTATION 2026-08-23 — the heading's "NOT MERGED" is FALSE and is annotated, not rewritten.**
> **Packet F MERGED** as PR [#411](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/411),
> squash **`2c95bae`**, at **`2026-08-22T21:52:14Z`**; post-merge `main` run `32600832091` was
> **18/18 green** at job level. §13.18's merge STOP is discharged at its own site, and the first of
> its two surviving obligations — **NT-4** — is **closed by measurement** on the PR's ubuntu
> `Test Inventory Drift` job `97094899990`. The second — the qualification-window ledger — is
> **still running**, extended at §13.0.

**This section is appended AFTER §12 Provenance on purpose, and the ordering is not a mistake to be
fixed.** Renumbering §12 a second time is a known hazard here — Packet C already renumbered
§11 → §12 once and had to verify twice that nothing cited a "§11 Provenance" (§12's own note,
§11.15-C-20) — and **nothing outside this file cites a section number in it**, so appending costs
nothing while renumbering risks orphaning a cross-reference for a second time. §12 remains the Gate 0
provenance record; Packet F's provenance is §13.0 and §13.2.

**Council status, stated so the "PLAN v2" label in the heading is not over-read.** The label is the one
this section was created under. **No Gate 1 council record for Packet F exists in this document** —
§11.15 is *Packet C's* council record and belongs to it. If a council runs against §13, its response
matrix belongs in a new subsection and the label is earned there; until then the heading's "PLAN v2"
describes the drafting round, not a reviewed-and-dispositioned round. **The launching session supplied
no agent ID to the writer of this section**, so no agent-provenance stamp is made here rather than an
invented one.

**Evidence rule for this whole section.** Every number below comes from a **live measurement dossier
taken 2026-08-22 in this worktree** (`D:\development\Hypertrophy-Toolbox-v3-main-phase3-packet-f-inventory`,
branch `wt/phase3-packet-f-inventory`, base `9cb6cdc`, with `npm ci` run **inside** the worktree).
That dossier is a **session scratchpad and is not committed to the repository**, which is why §13.2
restates its content rather than linking to it, and why its identifiers (**M0–M8**, **P1–P14**) are
quoted on every claim that rests on them. **Where the dossier lacks a fact, this section says
`MEASUREMENT NOT TAKEN` or `OPEN QUESTION` instead of supplying one** (§13.2's second table, and
§13.12). Nothing in §13.8 has been executed.

> ⚠️ **ANNOTATION 2026-08-22 — the last sentence is now FALSE and is annotated, not rewritten.**
> **The whole of §13.8 has since been executed**, with the revisions §13.15 requires. Measured
> results, deviations and every survivor are at **§13.17**; §13.8 remains the **prediction** it
> was written as, so that prediction and outcome can still be compared. The `MEASUREMENT NOT
> TAKEN` rows are also partly closed there — though **NT-4 is NOT among them**: Linux behaviour of
> `vitest list --json` is measured by the PR's ubuntu `Test Inventory Drift` run and by nothing
> before it.
>
> ⚠️ **FOLLOW-ON ANNOTATION 2026-08-23 — that run has now happened and NT-4 IS CLOSED.** Job
> **`97094899990`**, `Test Inventory Drift`, runner label **`ubuntu-latest`**, on run
> [`32599231895`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32599231895)
> (`pull_request`, head `d7494e2`): conclusion **`success`**, completed **`2026-08-22T21:19:58Z`**,
> with step 7 — *"Check committed inventory against a fresh Linux regeneration"* — **`success`**.
> A Linux regeneration matched the Windows-generated artifact byte for byte, so cross-platform
> agreement on the sorted identity list is **measured, not reasoned**. **NT-7 (`describe.each`)
> remains open and unexercised**; nothing here closes it.

### 13.0 Packet C merge, T0, and the live qualification-window ledger

**Three annotation blocks elsewhere in this document point forward to this subsection** — the header's
THIRD ANNOTATION, §6.5's "THE WINDOW IS NOW RUNNING" block, and §11.18's T0 annotation. This is the
live block they defer to.

**Packet C merged.** *(M0)*

| Item | Measured value |
|---|---|
| PR | [#410](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/410), head `wt/phase3-packet-c-exercises` |
| State | **`MERGED`** |
| Squash commit | **`9cb6cdc`** (`9cb6cdc70fde23e3a2b6428084a5672b6b6700c3`) — this is `origin/main` |
| Merged at | **`2026-08-22T17:59:03Z`** |
| Post-merge `main` run | [`32589375849`](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/actions/runs/32589375849) — workflow `CI/CD Pipeline`, event `push`, headSha `9cb6cdc`, conclusion **success**, **18 jobs, all 18 `success`** |
| Open PRs at planning time | **0** |

**T0 is established, and it is a job-level fact, not a workflow-level one** — §6.1's discipline, which
resolves every window measurement to the exact context string rather than to the run's overall
conclusion.

| Item | Measured value |
|---|---|
| T0 job | **`97070630453`** — `JS Unit (Vitest, non-required)`, conclusion **`success`** |
| **T0** | **`2026-08-22T17:59:26Z`** (job `completedAt`) |
| **Strict 14-day mark** | **`2026-09-05T17:59:26Z`** |

**The ledger — every `main` `JS Unit (Vitest, non-required)` result from T0 onward.** *(M0)*

| # | `main` run | Job | Conclusion | Completed (UTC) |
|---|---|---|---|---|
| **1 — T0** | `32589375849` (`push`, `9cb6cdc`, 18/18 `success`) | `97070630453` | **`success`** | **`2026-08-22T17:59:26Z`** |
| — | **No `main` run has occurred after T0.** T0's run is the newest `main` run at planning time | — | — | — |

| Ledger tally, at planning time | Value |
|---|---:|
| Green `main` `JS Unit` results since and including T0 | **1** |
| **Red** results | **0** |
| **Missing** results (a `main` run with no `js-unit` job) | **0** |
| **Cancelled** results | **0** |
| `main` runs after T0 of any kind | **0** |

**No red, missing or cancelled result exists in the window.** The window opened on the day this section
was written (**2026-08-22**), so the ledger is one row long by arithmetic, not by omission — and it must
be **extended, never restated from memory**, at every later session until `2026-09-05T17:59:26Z`.

---

#### LIVE LEDGER — extended 2026-08-23, read from the API, not from the tables above

> **This block is the live one.** The two tables above are the **planning-time** reading of
> 2026-08-22 and are left as that record; §13.17 Part 7 is the **execution-time** reading of the same
> day. Neither is restated here — this block is a fresh job-level read, and it is what a later
> session extends.
>
> ⚠️ **ANNOTATION 2026-08-23 — this block is SUPERSEDED by the *post-#413* LIVE LEDGER further
> down this subsection**, which is a fresh **four**-row job-level read taken after PR #413
> merged. This block is left exactly as the `2026-08-23T14:01:12Z` **three**-row reading and is
> **not** restated there. Its three rows are unchanged and still correct as of that moment; only
> its *count* and its “newest `main` run” are spent.

**Read at `2026-08-23T14:01:12Z`** (UTC now, taken from the GitHub API response `Date` header, not
from the host clock). *(This block supersedes its own `2026-08-23T10:11:56Z` reading, which recorded
two rows and is not restated — a third `main` run has landed since, and the whole ledger was
re-derived from the API rather than extended from the page.)* Method:
`gh api "repos/:owner/:repo/actions/runs?branch=main&per_page=100"`,
filtered to `created_at >= 2026-08-22T17:00:00Z` — deliberately **earlier** than T0, so the filter is a
superset and cannot hide a run — across **every** workflow, not just `CI/CD Pipeline`. Each returned
run's `/jobs` was then enumerated in full and matched on the exact context string
`JS Unit (Vitest, non-required)`. **No run's overall conclusion was used as a proxy for its `js-unit`
result** — §6.1's discipline.

| # | `main` run | Event / head | Run conclusion | `js-unit` job | Job conclusion | Completed (UTC) |
|---|---|---|---|---|---|---|
| **1 — T0** | [`32589375849`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32589375849) | `push` / `9cb6cdc` (PR #410, Packet C) | `success`, **18/18** | `97070630453` | **`success`** | **`2026-08-22T17:59:26Z`** |
| **2** | [`32600832091`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32600832091) | `push` / `2c95bae` (PR #411, Packet F) | `success`, **18/18** | **`97098730892`** | **`success`** | **`2026-08-22T21:52:42Z`** |
| **3** | [`32639359162`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32639359162) | `push` / `ca28ec0` (PR #412, post-#411 status reconciliation) | `success`, **18/18** | [**`97193944527`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32639359162/job/97193944527) | **`success`** | **`2026-08-23T12:26:02Z`** |

| Ledger tally, at `2026-08-23T14:01:12Z` | Value |
|---|---:|
| Green `main` `JS Unit` results since and including T0 | **3** |
| **Red** results | **0** |
| **Missing** results (a `main` run with no `js-unit` job) | **0** |
| **Skipped** results | **0** |
| **Cancelled** results | **0** |
| `main` runs of **any** workflow at or after T0 | **3** — all three `CI/CD Pipeline`, all three `push`, all three 18/18 |
| Elapsed since T0 | **≈ 20 h 2 m** of the required **14 d** |

**Nothing is inferred.** All three rows were resolved by enumerating the run's jobs and reading each
job's own `conclusion` and `completed_at`; each run's `/jobs` reported `total_count = 18` with every
job `success`. There is **no** `main` run in this window whose `js-unit` result is red, missing,
skipped or cancelled — and there is **no** `main` run in this window that this ledger omits: the
superset query returned exactly **three** `main` runs of any workflow in that span, and all three are
listed. *(Row 1's run was **created** at `2026-08-22T17:59:06Z`, twenty seconds before T0 — the
ledger indexes `js-unit` **results** at or after T0, not runs, and that job's `completed_at` **is** T0.)*
**No `schedule`-event run has occurred in the window** — all three rows are `push`. The next
deep-gate cron is **2026-08-24**; it has **not executed at this read time and nothing about it is
claimed here**, and `deep-gate.yml` carries no `js-unit` job in any case, so it can only ever add a
row here by not adding one.

**Row 3 did not restart the window, and #412's `mergedAt` is not T0.** PR #412 was
**documentation-only** — it changed no file under `static/js/**`, so the suite the window is
qualifying is still **13 files / 231 cases**, byte-identical across `2c95bae → ca28ec0`, and Q2's
restart clause did not engage. **T0 remains `2026-08-22T17:59:26Z`; the strict mark remains
`2026-09-05T17:59:26Z`.** The same holds for the Q6 documentation packet that appended this row:
it touches `docs/**` and one `vitest.config.js` **comment**, no executable configuration and no JS
test, so it cannot restart the window either — but the `main` run it produces on merge **will** mint
row 4, and whoever lands it owes that row.

**Packet F's own PR runs are not `main` runs and do not enter this ledger** — including run
`32599231895`, whose `JS Unit (Vitest, non-required)` job `97094899981` passed. That run is evidence
about **NT-4** (§13.2), not about the window.

**T0 did NOT move when Packet F merged.** T0 is still **`2026-08-22T17:59:26Z`** and the strict mark is
still **`2026-09-05T17:59:26Z`**. Packet F changed **no JS test case** — the suite is **13 files / 231
cases** on both sides of `2c95bae` (§13.10 step 8 gated exactly this) — so Q2's restart clause never
engaged. **#411's `mergedAt` (`2026-08-22T21:52:14Z`) is not T0 and must never be recorded as one.**

**Still to do, and owed by whoever picks this up:** extend this ledger at **every** later session until
`2026-09-05T17:59:26Z`, at **job** level, appending any red, missing, skipped or cancelled result
rather than summarising it. **A red resets the window to zero** (§6.5), with §6.2's attribution
discipline argued on the record and never applied silently.

---

#### LIVE LEDGER — extended 2026-08-23 after PR #413 merged (post-#413 read)

> **This block is now the live one.** It supersedes the `2026-08-23T14:01:12Z` block above,
> which recorded **three** rows and is left standing as that record — it is **not** restated
> here. Everything below is a fresh job-level read of the API, not an extension of the page.
>
> ⚠️ **ANNOTATION 2026-08-24 — this block is SUPERSEDED by the *post-#414* LIVE LEDGER further
> down this subsection**, which is a fresh **five**-row job-level read taken after PR #414 merged
> and after the 2026-08-24 deep-gate cron executed. This block is left exactly as the
> `2026-08-23T18:50:52Z` **four**-row reading and is **not** restated there. Its four rows are
> unchanged and still correct. **Three** of its clauses are spent: its *count*, its
> *"`main` runs of **any** workflow at or after T0 — all four `CI/CD Pipeline`"* row (four
> non-`ci.yml` `main` runs have since landed), and its *"the next deep-gate cron is
> **2026-08-24**; it has not executed at this read time"* clause, which is now discharged.

**Read at `2026-08-23T18:50:52Z`** (UTC now, taken from the GitHub API response `Date` header, not
from the host clock), after PR [#413](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/413)
merged (squash `b0aa393`, `2026-08-23T18:03:43Z`). Method, deliberately identical to the block
above: `gh run list --branch main` plus
`gh api "repos/:owner/:repo/actions/runs?branch=main&per_page=100"`, filtered to
`created_at >= 2026-08-22T17:00:00Z` — deliberately **earlier** than T0, so the filter is a
superset and cannot hide a run — across **every** workflow, not just `CI/CD Pipeline`. Each
returned run's `/jobs` was then enumerated in full and matched on the exact context string
`JS Unit (Vitest, non-required)`. **No run's overall conclusion was used as a proxy for its
`js-unit` result** — §6.1's discipline. The superset returned exactly **four** `main` runs of any
workflow in that span, and all four are listed below.

| # | `main` run | Event / head | Run conclusion | `js-unit` job | Job conclusion | Completed (UTC) |
|---|---|---|---|---|---|---|
| **1 — T0** | [`32589375849`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32589375849) | `push` / `9cb6cdc` (PR #410, Packet C) | `success`, **18/18** | [`97070630453`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32589375849/job/97070630453) | **`success`** | **`2026-08-22T17:59:26Z`** |
| **2** | [`32600832091`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32600832091) | `push` / `2c95bae` (PR #411, Packet F) | `success`, **18/18** | [`97098730892`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32600832091/job/97098730892) | **`success`** | **`2026-08-22T21:52:42Z`** |
| **3** | [`32639359162`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32639359162) | `push` / `ca28ec0` (PR #412, post-#411 status reconciliation) | `success`, **18/18** | [`97193944527`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32639359162/job/97193944527) | **`success`** | **`2026-08-23T12:26:02Z`** |
| **4** | [`32656837264`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32656837264) | `push` / `b0aa393` (PR #413, the Q6 documentation correction) | `success`, **18/18** | [**`97236769067`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32656837264/job/97236769067) | **`success`** | **`2026-08-23T18:04:10Z`** |

| Ledger tally, at `2026-08-23T18:50:52Z` | Value |
|---|---:|
| Green `main` `JS Unit` results since and including T0 | **4** |
| **Red** results | **0** |
| **Missing** results (a `main` run with no `js-unit` job) | **0** |
| **Skipped** results | **0** |
| **Cancelled** results | **0** |
| `main` runs of **any** workflow at or after T0 | **4** — all four `CI/CD Pipeline`, all four `push`, all four 18/18 |
| **`schedule`-event runs in the window** | **0** |
| Elapsed since T0 | **≈ 24 h 51 m** of the required **14 d** |

**Nothing is inferred, and nothing is omitted.** All four rows were resolved by enumerating the
run's jobs and reading each job's own `conclusion` and `completed_at`; each run's `/jobs`
reported `total_count = 18` with every job `success`. There is **no** `main` run in this window
whose `js-unit` result is red, missing, skipped or cancelled, and **no** `main` run this ledger
omits. *(Row 1's run was **created** at `2026-08-22T17:59:06Z`, twenty seconds **before** T0 —
the ledger indexes `js-unit` **results** at or after T0, not runs, and that job's `completed_at`
**is** T0. A run created before T0 can still be row 1.)*

**Row 4 did not restart the window, and #413's `mergedAt` is not T0.** PR #413 touched **exactly
three** files — [`TESTING_STRATEGY_PLANNING.md`](../TESTING_STRATEGY_PLANNING.md), this
document, and [`vitest.config.js`](../../vitest.config.js), whose change is **comment-only** (no
executable configuration) — and **zero** files under `static/js/**`. The suite the window is
qualifying is therefore still **13 files / 231 cases**, byte-identical across
`ca28ec0 → b0aa393`, and Q2's restart clause did not engage. **T0 remains
`2026-08-22T17:59:26Z`; the strict mark remains `2026-09-05T17:59:26Z`.** The same already held
for row 3 (#412, documentation-only).

**No `schedule`-event run has occurred in the window** — all four rows are `push`. The next
deep-gate cron is **2026-08-24**; it has **not executed at this read time and nothing about it
is claimed here**, and `deep-gate.yml` carries no `js-unit` job in any case, so it can only ever
add a row here by not adding one.

**Still to do, and owed by whoever picks this up:** extend **this** block — not the superseded
one above — at **every** later session until `2026-09-05T17:59:26Z`, at **job** level, appending
any red, missing, skipped or cancelled result rather than summarising it, and re-deriving the
whole ledger from the API rather than extending it from the page. **A red resets the window to
zero** (§6.5), with §6.2's attribution discipline argued on the record and never applied
silently.

---

#### LIVE LEDGER — extended 2026-08-24 after PR #414 merged (post-#414 read)

> **This block is now the live one.** It supersedes the `2026-08-23T18:50:52Z` block above,
> which recorded **four** rows and is left standing as that record — it is **not** restated
> here. Everything below is a fresh job-level read of the API, not an extension of the page.
>
> ⚠️ **ANNOTATION 2026-08-24 — this block is SUPERSEDED by the *post-#417* LIVE LEDGER
> further down this subsection**, which is a fresh **six**-row job-level read taken after PR
> #417 — the PR that carried *this* block onto `main` — merged as squash commit `5111a7f`.
> ⚠️ **ANNOTATION 2026-08-25 — the *six-row* description just above is the dated size of
> the post-#417 block on 2026-08-24, and is left standing as that reading, not restated.** That
> block was
> **extended in place** three times on 2026-08-25 and three times more on 2026-08-26, and now carries
> **sixteen** rows: the seventh is
> the `main` run minted by PR #418's own merge, the eighth PR #419's (`5ca4191`), the ninth PR
> #420's (`77f4adf`), the tenth PR #421's (`b4d6b13`), the eleventh PR #422's (`1243728`), the
> twelfth PR #423's (`06a3f41`), the thirteenth PR #424's (`52c44c4`), the fourteenth PR #415's
> (`7a64d2e`), the fifteenth PR #425's (`db6c34b`) and the sixteenth PR #416's (`b733c14`).
> The pointer is otherwise unchanged and
> still resolves —
> the post-#417 block is still the live one, and it was **not** superseded by a new block.
> This block is left exactly as the `2026-08-24T17:03:00Z` **five**-row reading and is **not**
> restated there. Its five rows are unchanged and still correct. **Three** of its clauses are
> spent as live statements while remaining accurate as the dated reading they were: its
> *count* (**5**), its completeness-check figure (*"**9** — the 5 above plus the 4 classified
> below"*), and its closing *"extend **this** block"* instruction, which now points at the
> post-#417 block instead. **A ledger block can never record the `main` run its own merge
> produces** — that run does not exist until after the merge — which is exactly why this
> block ends by owing the next row to whoever lands it. That debt is discharged below.
>
> **A scope correction travels with this block, and it is why the tally below has a new row.**
> Both earlier blocks tallied *"`main` runs of **any** workflow at or after T0"* and, in the
> same breath, defined a **Missing** result as *"a `main` run with no `js-unit` job"*. Through
> row 4 those two readings agreed **by accident**: every `main` run in the window happened to
> be a `CI/CD Pipeline` run, so the broad count and the qualification count were the same
> number. **On 2026-08-24 they diverge.** Four `main` runs of other workflows landed — three
> Dependabot `dynamic` update runs and the weekly `Deep Gate` cron — and **none of them is a
> qualification attempt**: §6.1 fixes the qualification scope at **`ci.yml`
> (`CI/CD Pipeline`)**, and neither `dynamic/dependabot/dependabot-updates` nor
> `.github/workflows/deep-gate.yml` declares a `js-unit` job at all. Tallying them as
> **Missing** would manufacture four phantom gaps out of four workflows that were never in
> scope, and a later session would read four phantom gaps as a defect in the window. **The
> broad superset query is kept exactly as it was** — it is the completeness check that proves
> no qualification attempt is hidden — but its result is now **classified** rather than
> tallied straight into the *Missing* row.
>
> **One clause is retired in BOTH superseded blocks at once, and it is retired here rather
> than at either site.** Each of them ends *"No `schedule`-event run has occurred in the
> window — all N rows are `push`"*, and each pairs it with *"the next deep-gate cron is
> 2026-08-24; it has not executed at this read time"*. **It has now executed** — run
> `32688747703`, event `schedule`, on `main`. Both clauses are therefore spent as live
> statements while remaining accurate as the dated readings they were. The five *ledger* rows
> are still all `push`, because `ci.yml` declares no `schedule` trigger at all; the schedule
> run belongs to a different workflow and is classified below rather than tallied.

**Read at `2026-08-24T17:03:00Z`** (UTC now, taken from the GitHub API response `Date` header, not
from the host clock), after PR [#414](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/414)
merged (squash `31659a5`, `2026-08-23T19:22:55Z`). Method, deliberately identical to the two blocks
above: `gh run list --branch main` plus
`gh api "repos/:owner/:repo/actions/runs?branch=main&per_page=100"`, filtered to
`created_at >= 2026-08-22T17:00:00Z` — deliberately **earlier** than T0, so the filter is a
superset and cannot hide a run — across **every** workflow, not just `CI/CD Pipeline`. Each
returned run's `/jobs` was then enumerated in full and matched on the exact context string
`JS Unit (Vitest, non-required)`. **No run's overall conclusion was used as a proxy for its
`js-unit` result** — §6.1's discipline. The superset returned **nine** `main` runs of any workflow
in that span: **five** `CI/CD Pipeline` runs, which are the qualification attempts and are the five
rows below, and **four** runs of other workflows, classified in the table after the tally.

| # | `main` run | Event / head | Run conclusion | `js-unit` job | Job conclusion | Completed (UTC) |
|---|---|---|---|---|---|---|
| **1 — T0** | [`32589375849`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32589375849) | `push` / `9cb6cdc` (PR #410, Packet C) | `success`, **18/18** | [`97070630453`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32589375849/job/97070630453) | **`success`** | **`2026-08-22T17:59:26Z`** |
| **2** | [`32600832091`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32600832091) | `push` / `2c95bae` (PR #411, Packet F) | `success`, **18/18** | [`97098730892`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32600832091/job/97098730892) | **`success`** | **`2026-08-22T21:52:42Z`** |
| **3** | [`32639359162`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32639359162) | `push` / `ca28ec0` (PR #412, post-#411 status reconciliation) | `success`, **18/18** | [`97193944527`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32639359162/job/97193944527) | **`success`** | **`2026-08-23T12:26:02Z`** |
| **4** | [`32656837264`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32656837264) | `push` / `b0aa393` (PR #413, the Q6 documentation correction) | `success`, **18/18** | [`97236769067`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32656837264/job/97236769067) | **`success`** | **`2026-08-23T18:04:10Z`** |
| **5** | [`32661056527`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32661056527) | `push` / `31659a5` (PR #414, post-#413 status reconciliation) | `success`, **18/18** | [**`97247194117`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32661056527/job/97247194117) | **`success`** | **`2026-08-23T19:23:22Z`** |

| Ledger tally, at `2026-08-24T17:03:00Z` | Value |
|---|---:|
| **Qualification attempts** — `main` `CI/CD Pipeline` (`ci.yml`) runs at or after T0 | **5** — all five `push`, all five 18/18 |
| Green `main` `JS Unit` results since and including T0 | **5** |
| **Red** results | **0** |
| **Missing** results (a `main` **`ci.yml`** run with no `js-unit` job) | **0** |
| **Skipped** results | **0** |
| **Cancelled** results | **0** |
| `main` runs of **any** workflow at or after T0 (completeness check, not a tally) | **9** — the 5 above plus the 4 classified below |
| **`schedule`-event `ci.yml` runs in the window** | **0** — `ci.yml` has no `schedule` trigger |
| Elapsed since T0 | **≈ 1 d 23 h 4 m** of the required **14 d** |

**The four `main` runs in the window that are NOT qualification attempts.** Each was resolved the
same way as the rows above — by enumerating its `/jobs` — and each is recorded so a later session
does not rediscover them and mistake them for gaps.

| `main` run | Workflow / path | Event | Jobs | Why it cannot mint a ledger row |
|---|---|---|---|---|
| [`32676594582`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32676594582) | `pip in /. - Update #1537135558` — `dynamic/dependabot/dependabot-updates` | `dynamic` | **1** — `Dependabot`, `success` | Not `ci.yml`. Dependabot's update runner declares one job and **no** `js-unit`. It opened PR **#415**. |
| [`32676594619`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32676594619) | `npm_and_yarn in /. - Update #1537135574` — same path | `dynamic` | **1** — `Dependabot`, `success` | As above. It opened PR **#416**. |
| [`32676594928`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32676594928) | `github_actions in /. - Update #1537135595` — same path | `dynamic` | **1** — `Dependabot`, `success` | As above. It opened no PR. |
| [`32688747703`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32688747703) | `Deep Gate (manual + weekly)` — `.github/workflows/deep-gate.yml` | **`schedule`** | **7** — all `success` | Not `ci.yml`. `deep-gate.yml` contains **zero** occurrences of `js-unit` / `JS Unit`, measured on `31659a5`. This is the first exercise of the clause both earlier blocks already carried: *it can only ever add a row here by not adding one.* Its own evidential value is R1-D3's, not this window's — see [`release_pipeline/PLANNING.md`](../release_pipeline/PLANNING.md) § *The second `schedule`-event run*. |

**Nothing is inferred, and nothing is omitted.** All five ledger rows were resolved by enumerating
the run's jobs and reading each job's own `conclusion` and `completed_at`; each run's `/jobs`
reported `total_count = 18` with every job `success`. There is **no** `main` `ci.yml` run in this
window whose `js-unit` result is red, missing, skipped or cancelled, and **no** qualification
attempt this ledger omits. *(Row 1's run was **created** at `2026-08-22T17:59:06Z`, twenty seconds
**before** T0 — the ledger indexes `js-unit` **results** at or after T0, not runs, and that job's
`completed_at` **is** T0. A run created before T0 can still be row 1.)*

**Row 5 did not restart the window, and #414's `mergedAt` is not T0.** PR #414 touched **exactly
three** files — [`ACTIVE_DEVELOPMENT.md`](../ACTIVE_DEVELOPMENT.md),
[`MASTER_HANDOVER.md`](../MASTER_HANDOVER.md) and **this document** — and **zero** files under
`static/js/**`, no workflow, no dependency, no generated inventory and no `vitest.config.js`. The
suite the window is qualifying is therefore still **13 files / 231 cases**, byte-identical across
`b0aa393 → 31659a5`, and Q2's restart clause did not engage. **T0 remains
`2026-08-22T17:59:26Z`; the strict mark remains `2026-09-05T17:59:26Z`.** The same already held for
rows 3 and 4.

**Two Dependabot PRs are open and neither enters this ledger.** **#415** (`pyinstaller`
6.22.0 → 6.22.2) and **#416** (`sass` 1.102.0 → 1.103.1), both opened `2026-08-24T00:25Z`, both
unmerged at this read time. Their `ci.yml` runs execute on **PR branches**, not on `main`, so they
are outside §6.5's *"the clock starts on `main`"* rule — the same reason Packet F's own PR run
`32599231895` was excluded. **If either merges, its post-merge `main` run mints the next ledger row,
and whoever lands it owes that row.**

**Still to do, and owed by whoever picks this up:** extend **this** block — not either superseded
one above — at **every** later session until `2026-09-05T17:59:26Z`, at **job** level, appending any
red, missing, skipped or cancelled result rather than summarising it, and re-deriving the whole
ledger from the API rather than extending it from the page. **Classify, do not tally, any `main` run
that is not a `ci.yml` run.** **A red resets the window to zero** (§6.5), with §6.2's attribution
discipline argued on the record and never applied silently.

---

#### LIVE LEDGER — extended 2026-08-24 after PR #417 merged (post-#417 read), extended again 2026-08-25 after PR #418 merged (post-#418 read), extended a third time 2026-08-25 after PR #419 and PR #420 merged (post-#420 read), extended a fourth time 2026-08-25 after PR #421 merged (post-#421 read), extended a fifth time 2026-08-26 after PR #422 merged (post-#422 read), extended a sixth time 2026-08-26 after PR #423 merged (post-#423 read), extended a seventh time 2026-08-26 after PR #424, PR #415, PR #425 and PR #416 merged (post-#416 read)

> **This block is now the live one.** It supersedes the `2026-08-24T17:03:00Z` block above,
> which recorded **five** rows and is left standing as that record — it is **not** restated
> here. Everything below is a fresh job-level read of the API, not an extension of the page.
>
> **The merge that minted this block is the merge of the block above.** PR #417 carried the
> post-#414 reading onto `main` as squash commit `5111a7f`, and that push started a `main`
> `ci.yml` run of its own. **No ledger block can record the run its own merge produces**, so
> every block necessarily ends one row short of the state that exists a minute after it lands.
> That is a property of the mechanism, not an omission, and the post-#414 block named it
> correctly: *"whoever lands it owes that row."* **Row 6 is that row.**
>
> ⚠️ **EXTENDED 2026-08-25 — this block is STILL THE LIVE ONE. It is extended IN PLACE, and it
> is NOT superseded by a new block.** PR #418 — the PR that carried *this* block onto `main` —
> merged as squash commit `26ce7e9`, and that push started a `main` `ci.yml` run of its own.
> **Row 7 is that run**, and recording it discharges the debt this block booked against itself
> in *"#418 is the block's own carrier"* below. Everything from **Read at** onward is a fresh
> job-level read of the API at `2026-08-25T08:37:25Z`, not an extension of the page: all six
> earlier rows were re-derived from the API and came back byte-identical.
>
> **Four of this block's own clauses were spent by that extension, and each is corrected here
> rather than left for a later session to re-derive:** its read timestamp and tally, its
> completeness figure (*"**10** — the 6 above plus the 4 classified below"*), its open-PR
> table, which listed **#418** as open, and its *"#418's merge is already owed"* paragraph.
> **T0 did not move**, and the reason is measured below, not assumed.
>
> ⚠️ **EXTENDED AGAIN 2026-08-25 — this block is STILL THE LIVE ONE, and it is still extended
> IN PLACE.** Two merges landed after the extension above, so **two** rows are appended here, not
> one. PR #419 — the PR that carried the row-7 extension onto `main` — merged as squash commit
> `5ca4191`, and **row 8 is the `main` run that push started**. PR #420 (Packet T0) then merged as
> squash commit `77f4adf`, and **row 9 is its run**. Everything from *Read at* onward is a fresh
> job-level read of the API at `2026-08-25T14:50:55Z`, not an extension of the page.
>
> **Five of the `08:37:25Z` extension's own clauses are spent by this one, and each is corrected
> where it stands rather than left for a later session to re-derive:** its *Read at* timestamp
> and its seven-row tally, its completeness figure (*"**11** — the 7 above plus the 4 classified
> below"*), its open-PR paragraph, its *"whoever merges the row-7 PR owes row 8"* clause, and
> the *"now carries **seven** rows"* annotation it planted in the superseded post-#414 block
> further up this subsection.
>
> **Row 8 was measured before this extension existed, and was deliberately kept out of the
> document.** PR #420's body records run `32842991664`, job `97786392022`, `success`,
> `2026-08-25T11:34:34Z` in full, and states that the observation is *“deliberately not”* added to
> its own STEP12 diff because Packet T0 held that diff to an exact one-line repair. **A
> measurement recorded only in a PR body is not in the ledger**, so #420 discharged nothing and
> left **two** rows owed rather than one. This extension discharges both.
>
> ⚠️ **EXTENDED A THIRD TIME 2026-08-25 — this block is STILL THE LIVE ONE, and it is still
> extended IN PLACE.** This is the third of this block's in-place extensions and the fourth
> reading in the heading's count; the two series number differently because the heading counts
> the block's creation as its first reading. PR
> [#421](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/421) — the PR that carried the
> rows-8-and-9 extension onto `main`, together with Packet U1's Gate 0 requirements brief —
> merged as squash commit `b4d6b13`, and **row 10 is the `main` run that push started**.
> Everything from *Read at* onward is a fresh job-level read of the API at
> `2026-08-25T20:53:02Z`, not an extension of the page.
>
> **Six of the `2026-08-25T14:50:55Z` extension's own clauses are spent by this one, and each is
> corrected where it stands rather than left for a later session to re-derive:** its *Read at*
> timestamp and its nine-row tally, its completeness figure (*“**13** — the 9 above plus the 4
> classified below”*), its open-PR paragraph, its *“whoever merges it owes the next sequential
> ledger row”* clause written against the #421 carrier, the *“now carries **nine** rows”*
> annotation it planted in the superseded post-#414 block further up this subsection, and — caught
> on a later re-read of this block rather than when it was written — its *“as the **two**
> 2026-08-25 extensions did”* instruction in the *Still to do* paragraph at the end of this
> subsection, which was true when there were two and is corrected to **three** in place.
>
> **Row 10 could not have been written by the PR that produced it, and that is a property of the
> mechanism rather than an omission.** A merge mints its row only after the diff that could have
> carried it is already sealed, so #421 left the row owed rather than written; the measurement
> itself is row 10 below. **This extension discharges it.**
>
> ⚠️ **EXTENDED A FOURTH TIME 2026-08-26 — this block is STILL THE LIVE ONE, and it is still
> extended IN PLACE.** This is the fourth of this block's in-place extensions and the fifth
> reading in the heading's count; the two series number differently for the reason the third
> extension gives — the heading counts the block's creation as its first reading. PR
> [#422](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/422) — the PR that carried the
> row-10 extension onto `main`, together with Packet U1's Gate 1 council-reviewed plan and the
> owner's sign-off of it — merged as squash commit `1243728`, and **row 11 is the `main` run that
> push started**. Everything from *Read at* onward is a fresh job-level read of the API at
> `2026-08-26T00:25:41Z`, not an extension of the page.
>
> **Six of the `2026-08-25T20:53:02Z` extension's own clauses are spent by this one, and each is
> corrected where it stands rather than left for a later session to re-derive:** its *Read at*
> timestamp and its ten-row tally, its completeness figure (*“**14** — the 10 above plus the 4
> classified below”*), its open-PR paragraph, its *“whoever merges it owes the next sequential
> ledger row”* clause written against the `docs/u1-gate1-plan` carrier, the *“now carries **ten**
> rows”* annotation it planted in the superseded post-#414 block further up this subsection —
> **which is where that phrase actually lives; the clause list this one replaces mislocated it in
> this block's own read paragraph, and the third extension had located the analogous phrase
> correctly** — and its *“as the **three** 2026-08-25 extensions did”*
> instruction in the *Still to do* paragraph at the end of this subsection, which was true when
> all three extensions were made on 2026-08-25 and is corrected in place now that a fourth has
> been made on 2026-08-26.
>
> **Row 11 could not have been written by the PR that produced it either.** #422 left the row
> owed rather than written, exactly as #421 left row 10; the measurement itself is row 11 below.
> **This extension discharges it**, and it is carried by the Packet U1 **implementation** PR
> rather than by a ledger-only PR — a recursive ledger-only PR would mint a twelfth row and owe
> a thirteenth, without end.
>
> ⚠️ **EXTENDED A FIFTH TIME 2026-08-26 — this block is STILL THE LIVE ONE, and it is still
> extended IN PLACE.** This is the fifth of this block's in-place extensions and the sixth
> reading in the heading's count; the two series number differently for the reason the third
> extension gives — the heading counts the block's creation as its first reading. PR
> [#423](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/423) — the PR that carried the
> row-11 extension onto `main`, together with Packet U1's implementation — merged as squash commit
> `06a3f41`, and **row 12 is the `main` run that push started**. Everything from *Read at* onward
> is a fresh job-level read of the API at `2026-08-26T12:05:47Z`, not an extension of the page.
>
> **Six of the `2026-08-26T00:25:41Z` extension's own clauses are spent by this one, and each is
> corrected where it stands rather than left for a later session to re-derive:** its *Read at*
> timestamp and its eleven-row tally, its completeness figure (*“**15** — the 11 above plus the 4
> classified below”*), its open-PR paragraph, its *“Whoever merges it owes the next sequential
> ledger row”* clause written against the U1 implementation carrier, the *“now carries **eleven**
> rows”* annotation it planted in the superseded post-#414 block further up this subsection, and
> its *“as the **three** 2026-08-25 extensions and the 2026-08-26 one did”* instruction in the
> *Still to do* paragraph at the end of this subsection, which was true when only one extension
> had been made on 2026-08-26 and is corrected in place now that a second has been.
>
> **The fourth extension's prediction about row 12's carrier held, and it is measured below rather
> than assumed.** That extension wrote *“Whoever merges it owes the next sequential ledger row”*
> against the U1 implementation PR and, separately, predicted that the same PR could not restart
> the window even though it moved `static/js`. Both are now settled by measurement: #423 merged,
> row 12 is its run, and the *Row 12 did not restart the window* paragraph below carries the tree
> hashes. **The prediction was about the restart clause only; the run's `success` result was not
> predicted and was read off the job.**
>
> **This extension is carried by a docs-only planning PR, and that is a change of pattern worth
> naming.** Rows 6 through 10 were recorded by documentation PRs and row 11 by an implementation
> PR; row 12 is carried by Packet U2's **Gate 1 planning** PR, which changes no `static/js` file
> at all. The carrier's identity does not affect the row — it affects only the *next* row, which
> that carrier's own merge will mint.
>
> ⚠️ **EXTENDED A SIXTH TIME 2026-08-26 — this block is STILL THE LIVE ONE, and it is still
> extended IN PLACE.** This is the sixth of this block's in-place extensions and the seventh
> reading in the heading's count; the two series number differently for the reason the third
> extension gives — the heading counts the block's creation as its first reading. **Four merges
> landed since the previous extension, so FOUR rows are appended here, not one**, and that is the
> largest single extension this block has taken. PR
> [#424](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/424) — the PR that carried the row-12
> extension onto `main`, together with Packet U2's Gate 1 plan — merged as squash commit
> `52c44c4`, and **row 13 is the `main` run that push started**. PR
> [#415](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/415), the PyInstaller 6.22.0 → 6.22.2 Dependabot
> bump, merged as squash commit `7a64d2e`, and **row 14 is its run**. PR
> [#425](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/425), Packet U3a's Gate 0 requirements, merged as
> squash commit `db6c34b`, and **row 15 is its run**. PR
> [#416](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/416), the Sass 1.102.0 → 1.103.1 Dependabot bump,
> merged as squash commit `b733c14`, and **row 16 is its run**. Everything from *Read at* onward is
> a fresh job-level read of the API at `2026-08-26T23:37:12Z`, not an extension of the page: all
> twelve earlier rows were re-derived from the API and came back byte-identical.
>
> **Six of the `2026-08-26T12:05:47Z` extension's own clauses are spent by this one, and each is
> corrected where it stands rather than left for a later session to re-derive:** its *Read at*
> timestamp and its twelve-row tally, its completeness figure (*"**16** — the 12 above plus the 4
> classified below"*), its **"The four `main` runs in the window that are NOT qualification
> attempts"** heading and its *"No fifth non-attempt run has landed"* sentence — **both now false,
> and this is the first extension to have to correct them**, its *"whoever merges it owes the next
> sequential ledger row"* clause written against the Packet U2 Gate 1 carrier, and its *"as the
> **three** 2026-08-25 extensions and the **two** 2026-08-26 ones did"* instruction in the *Still to
> do* paragraph at the end of this subsection.
>
> **A fifth non-attempt run exists, and it is the first one minted by a merge rather than by
> Dependabot's scheduler.** Run [`33017596325`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33017596325),
> `Configured Graph Update: pip in /. #1542182565`, event `dynamic`, was started by PR #415's own
> push to `main` — a dependency-graph submission that runs *because* a pip lockfile changed. It
> declares **one** job and no `js-unit`, so it is classified, not tallied, exactly as the four
> Dependabot runs are. **The four-run classification table below is now a five-run table.**
>
> **Rows 14 and 16 are the first ledger rows minted by dependency PRs, and row 16 is the first
> minted by a JS dependency PR.** Every earlier row was carried by a documentation PR or by Packet
> U1's implementation. That is a change of carrier class, and because Q2's restart clause is
> written about *test-suite expansion*, it is answered below by measurement — tree hashes and
> inventory totals — rather than by assuming that "a dependency bump is not an expansion."

**Read at `2026-08-26T23:37:12Z`** (UTC now, taken from the GitHub API response `Date` header, not
from the host clock), after PR [#424](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/424) merged (squash
`52c44c4`, `2026-08-26T20:41:30Z`), PR [#415](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/415) merged
(squash `7a64d2e`, `2026-08-26T21:56:38Z`, final PR head `97aa3c4`), PR
[#425](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/425) merged (squash `db6c34b`) and PR
[#416](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/416) merged (squash `b733c14`,
`2026-08-26T23:22:30Z`, final PR head `73208e8`). **This read supersedes this block's own
`2026-08-26T12:05:47Z` twelve-row reading**, which is not restated. Method, deliberately identical to the three blocks
above and to this block's six earlier reads: `gh run list --branch main` plus
`gh api "repos/:owner/:repo/actions/runs?branch=main&per_page=100"`, filtered to
`created_at >= 2026-08-22T17:00:00Z` — deliberately **earlier** than T0, so the filter is a
superset and cannot hide a run — across **every** workflow, not just `CI/CD Pipeline`. Each
returned run's `/jobs` was then enumerated in full and matched on the exact context string
`JS Unit (Vitest, non-required)`. **No run's overall conclusion was used as a proxy for its
`js-unit` result** — §6.1's discipline: each of rows 13–16 had its job object fetched from its own
run's `/jobs`, and its `status`, `conclusion` and `completed_at` were read off **that job**, not off
its run. All four runs' overall conclusions are also `success`, and that fact was **not** used. The
superset returned **twenty-one** `main` runs of any workflow in that span: **sixteen** `CI/CD
Pipeline` runs, which are the qualification attempts and are the sixteen rows below, and **five**
runs of other workflows, classified in the table after the tally. The twelve rows this block
previously carried were **re-derived from the API, not copied from the page**, and all twelve came
back byte-identical.

| # | `main` run | Event / head | Run conclusion | `js-unit` job | Job conclusion | Completed (UTC) |
|---|---|---|---|---|---|---|
| **1 — T0** | [`32589375849`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32589375849) | `push` / `9cb6cdc` (PR #410, Packet C) | `success`, **18/18** | [`97070630453`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32589375849/job/97070630453) | **`success`** | **`2026-08-22T17:59:26Z`** |
| **2** | [`32600832091`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32600832091) | `push` / `2c95bae` (PR #411, Packet F) | `success`, **18/18** | [`97098730892`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32600832091/job/97098730892) | **`success`** | **`2026-08-22T21:52:42Z`** |
| **3** | [`32639359162`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32639359162) | `push` / `ca28ec0` (PR #412, post-#411 status reconciliation) | `success`, **18/18** | [`97193944527`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32639359162/job/97193944527) | **`success`** | **`2026-08-23T12:26:02Z`** |
| **4** | [`32656837264`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32656837264) | `push` / `b0aa393` (PR #413, the Q6 documentation correction) | `success`, **18/18** | [`97236769067`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32656837264/job/97236769067) | **`success`** | **`2026-08-23T18:04:10Z`** |
| **5** | [`32661056527`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32661056527) | `push` / `31659a5` (PR #414, post-#413 status reconciliation) | `success`, **18/18** | [`97247194117`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32661056527/job/97247194117) | **`success`** | **`2026-08-23T19:23:22Z`** |
| **6** | [`32776201165`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32776201165) | `push` / `5111a7f` (PR #417, post-#414 evidence reconciliation) | `success`, **18/18** | [**`97587721956`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32776201165/job/97587721956) | **`success`** | **`2026-08-24T20:51:38Z`** |
| **7** | [`32826755101`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32826755101) | `push` / `26ce7e9` (PR #418, Open Work Execution Plan + this block) | `success`, **18/18** | [**`97736360454`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32826755101/job/97736360454) | **`success`** | **`2026-08-25T08:28:30Z`** |
| **8** | [`32842991664`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32842991664) | `push` / `5ca4191` (PR #419, the row-7 ledger extension) | `success`, **18/18** | [**`97786392022`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32842991664/job/97786392022) | **`success`** | **`2026-08-25T11:34:34Z`** |
| **9** | [`32851276626`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32851276626) | `push` / `77f4adf` (PR #420, Packet T0) | `success`, **18/18** | [**`97812537880`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32851276626/job/97812537880) | **`success`** | **`2026-08-25T13:05:57Z`** |
| **10** | [`32874746454`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32874746454) | `push` / `b4d6b13` (PR #421, Packet U1 Gate 0 plus rows 8–9) | `success`, **18/18** | [**`97889882928`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32874746454/job/97889882928) | **`success`** | **`2026-08-25T16:55:12Z`** |
| **11** | [`32911310086`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32911310086) | `push` / `1243728` (PR #422, Packet U1 Gate 1 sign-off plus row 10) | `success`, **18/18** | [**`98005892825`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32911310086/job/98005892825) | **`success`** | **`2026-08-25T23:34:05Z`** |
| **12** | [`32959719238`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32959719238) | `push` / `06a3f41` (PR #423, Packet U1 implementation plus row 11) | `success`, **18/18** | [**`98149159459`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32959719238/job/98149159459) | **`success`** | **`2026-08-26T10:44:17Z`** |
| **13** | [`33011674872`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33011674872) | `push` / `52c44c4` (PR #424, Packet U2 Gate 1 plan plus row 12) | `success`, **18/18** | [**`98319257214`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33011674872/job/98319257214) | **`success`** | **`2026-08-26T20:42:09Z`** |
| **14** | [`33017593094`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33017593094) | `push` / `7a64d2e` (PR #415, PyInstaller 6.22.0 → 6.22.2) | `success`, **18/18** | [**`98339729053`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33017593094/job/98339729053) | **`success`** | **`2026-08-26T21:56:58Z`** |
| **15** | [`33020896786`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33020896786) | `push` / `db6c34b` (PR #425, Packet U3a Gate 0 requirements) | `success`, **18/18** | [**`98350728218`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33020896786/job/98350728218) | **`success`** | **`2026-08-26T22:49:15Z`** |
| **16** | [`33023109789`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33023109789) | `push` / `b733c14` (PR #416, Sass 1.102.0 → 1.103.1) | `success`, **18/18** | [**`98358033353`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33023109789/job/98358033353) | **`success`** | **`2026-08-26T23:22:55Z`** |
| **17** | [`33026310164`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33026310164) | `push` / `ec1a5cb` (PR #429, JS-unit ledger rows 13–16) | `success`, **18/18** | [**`98368349021`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33026310164/job/98368349021) | **`success`** | **`2026-08-27T00:17:21Z`** |
| **18** | [`33026399702`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33026399702) | `push` / `3098282` (PR #430, pyright Packet P1) | `success`, **18/18** | [**`98368648573`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33026399702/job/98368648573) | **`success`** | **`2026-08-27T00:19:06Z`** |
| **19** | [`33030127322`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33030127322) | `push` / `5b35966` (**PR #426, Packet U3b — KI-011 toast action continuity**) | `success`, **18/18** | [**`98380484320`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33030127322/job/98380484320) | **`success`** | **`2026-08-27T01:27:24Z`** |
| **20** | [`33063751367`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33063751367) | `push` / `1211915` (PR #432, JS-unit ledger rows 17–19) | `success`, **18/18** | [**`98488650519`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33063751367/job/98488650519) | **`success`** | **`2026-08-27T10:37:48Z`** |
| **21** | [`33064557028`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33064557028) | `push` / `efa780c` (PR #427, Packet U2 implementation) | `success`, **18/18** | [**`98491338039`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33064557028/job/98491338039) | **`success`** | **`2026-08-27T10:48:05Z`** |
| **22** | [`33066528401`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33066528401) | `push` / `a37d7e7` (PR #428, Packet U3a Gate 1 plan) | `success`, **18/18** | [**`98497846286`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33066528401/job/98497846286) | **`success`** | **`2026-08-27T11:15:16Z`** |
| **23** | [`33067456258`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33067456258) | `push` / `07781a8` (PR #433, JS-unit ledger rows 20–21) | `success`, **18/18** | [**`98500982021`**](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33067456258/job/98500982021) | **`success`** | **`2026-08-27T11:28:17Z`** |

| Ledger tally, at `2026-08-26T23:37:12Z` | Value |
|---|---:|
| **Qualification attempts** — `main` `CI/CD Pipeline` (`ci.yml`) runs at or after T0 | **16** — all sixteen `push`, all sixteen 18/18 |
| Green `main` `JS Unit` results since and including T0 | **16** |
| **Red** results | **0** |
| **Missing** results (a `main` **`ci.yml`** run with no `js-unit` job) | **0** |
| **Skipped** results | **0** |
| **Cancelled** results | **0** |
| `main` runs of **any** workflow at or after T0 (completeness check, not a tally) | **21** — the 16 above plus the 5 classified below |
| **`schedule`-event `ci.yml` runs in the window** | **0** — `ci.yml` has no `schedule` trigger |
| Elapsed since T0 | **≈ 4 d 5 h 38 m** of the required **14 d** |
| Remaining to the strict mark | **≈ 9 d 18 h 22 m** |

> **LEDGER EXTENSION — `2026-08-27T01:36:07Z`, rows 17–19.** The tally immediately above was true at
> `2026-08-26T23:37:12Z` and is **annotated, not rewritten**; the live reading is the block below.
> Three `main` `ci.yml` runs have landed since it, and **all three are enumerated at job level** —
> the `js-unit` job's own `conclusion` and `completed_at`, never the run's overall conclusion.

| Ledger tally, at `2026-08-27T01:36:07Z` | Value |
|---|---:|
| **Qualification attempts** — `main` `CI/CD Pipeline` (`ci.yml`) runs at or after T0 | **19** — all nineteen `push`, all nineteen 18/18 |
| Green `main` `JS Unit` results since and including T0 | **19** |
| **Red** results | **0** |
| **Missing** results (a `main` **`ci.yml`** run with no `js-unit` job) | **0** |
| **Skipped** results | **0** |
| **Cancelled** results | **0** |
| `main` runs of **any** workflow at or after T0 (completeness check, not a tally) | **24** — the 19 above plus the **5** classified below, which is **unchanged**: 3 `Dependabot Updates`, 1 `Deep Gate (manual + weekly)`, 1 `Dependency Graph`. Re-enumerated at this read, not carried forward |
| **`schedule`-event `ci.yml` runs in the window** | **0** — `ci.yml` has no `schedule` trigger |
| Elapsed since T0 | **≈ 4 d 7 h 37 m** of the required **14 d** |
| Remaining to the strict mark | **≈ 9 d 16 h 23 m** |

> **LEDGER EXTENSION — `2026-08-27T10:37:48Z`, row 20.** The tally immediately above was true at
> `2026-08-27T01:36:07Z` and is **annotated, not rewritten**, exactly as the block before it was; the
> live reading is below. **One** `main` `ci.yml` run has landed since, read at job level.
>
> **Why this row is being written by Packet U2's PR rather than its own.** Row 20 records the merge of
> **#432**, the PR that wrote rows 17–19 — a ledger PR cannot record its own landing, because the run
> it would cite does not exist until after it merges. The row is therefore appended by the **next**
> authorized PR to touch this file, which is #427. That is the same reason row 17 (#429's own merge)
> was written by #432 rather than by #429.

| Ledger tally, at `2026-08-27T10:37:48Z` | Value |
|---|---:|
| **Qualification attempts** — `main` `CI/CD Pipeline` (`ci.yml`) runs at or after T0 | **20** — all twenty `push`, all twenty 18/18 |
| Green `main` `JS Unit` results since and including T0 | **20** |
| **Red** results | **0** |
| **Missing** results (a `main` **`ci.yml`** run with no `js-unit` job) | **0** |
| **Skipped** results | **0** |
| **Cancelled** results | **0** |
| **`schedule`-event `ci.yml` runs in the window** | **0** — `ci.yml` has no `schedule` trigger |
| Elapsed since T0 | **≈ 4 d 16 h 38 m** of the required **14 d** |
| Remaining to the strict mark | **≈ 9 d 7 h 22 m** |

**Row 20 restarts nothing.** #432 was **documentation-only** — its whole diff is this file — so it
changed no JS test case, no `vitest.config.js`, and no generated inventory. **T0 remains
`2026-08-22T17:59:26Z`; the strict mark remains `2026-09-05T17:59:26Z`.**

> **LEDGER EXTENSION — `2026-08-27T10:48:05Z`, row 21.** The tally immediately above was true at
> `2026-08-27T10:37:48Z` and is **annotated, not rewritten**, exactly as the two blocks before it
> were; the live reading is below. **One** `main` `ci.yml` run has landed since, read at job level.
>
> **Why this row is written here.** Row 21 records the merge of **#427**, Packet U2's
> implementation — the PR that carried row 20 as a rider. A PR cannot record its own landing, so
> the row falls to the next authorized PR to touch this file, which is this one. That is the same
> mechanism row 20 records for #432 and row 17 records for #429.

| Ledger tally, at `2026-08-27T10:48:05Z` | Value |
|---|---:|
| **Qualification attempts** — `main` `CI/CD Pipeline` (`ci.yml`) runs at or after T0 | **21** — all twenty-one `push`, all twenty-one 18/18 |
| Green `main` `JS Unit` results since and including T0 | **21** |
| **Red** results | **0** |
| **Missing** results (a `main` **`ci.yml`** run with no `js-unit` job) | **0** |
| **Skipped** results | **0** |
| **Cancelled** results | **0** |
| `main` runs of **any** workflow at or after T0 (completeness check, not a tally) | **26** — the 21 attempts plus the 5 classified non-attempts |
| **`schedule`-event `ci.yml` runs in the window** | **0** — `ci.yml` has no `schedule` trigger |
| Elapsed since T0 | **≈ 4 d 16 h 48 m** of the required **14 d** |
| Remaining to the strict mark | **≈ 9 d 7 h 12 m** |

> **LEDGER EXTENSION — `2026-08-27T11:28:17Z`, rows 22–23.** The tally immediately above was true at
> `2026-08-27T10:48:05Z` and is **annotated, not rewritten**, as every extension before it has been;
> the live reading is below. **Two** `main` `ci.yml` runs have landed since, both read at job level —
> the `js-unit` job's own `conclusion` and `completed_at`, never the run's overall conclusion.
>
> **Row 23 is another self-recording gap closed by the next writer**, the same mechanism rows 20 and
> 17 record: #433 wrote rows 20–21 and could not record its own landing, because the run it would
> cite does not exist until after it merges.

| Ledger tally, at `2026-08-27T11:28:17Z` | Value |
|---|---:|
| **Qualification attempts** — `main` `CI/CD Pipeline` (`ci.yml`) runs at or after T0 | **23** — all twenty-three `push`, all twenty-three 18/18 |
| Green `main` `JS Unit` results since and including T0 | **23** |
| **Red** results | **0** |
| **Missing** results (a `main` **`ci.yml`** run with no `js-unit` job) | **0** |
| **Skipped** results | **0** |
| **Cancelled** results | **0** |
| `main` runs of **any** workflow at or after T0 (completeness check, not a tally) | **28** — the 23 attempts plus **5** classified non-attempts, re-enumerated at this read and **unchanged**: 3 `Dependabot Updates`, 1 `Deep Gate (manual + weekly)`, 1 `Dependency Graph` |
| **`schedule`-event `ci.yml` runs in the window** | **0** — `ci.yml` has no `schedule` trigger |
| Elapsed since T0 | **≈ 4 d 17 h 29 m** of the required **14 d** |
| Remaining to the strict mark | **≈ 9 d 6 h 31 m** |

**Neither row restarts anything, and both carry the STRONGEST available form of the argument rather
than the narrowest.** #428 and #433 are **documentation-only**: `git rev-parse <sha>:static/js`
returns **`fedecefa6acc738319ec95dc75e97009a5e24d03`** at `efa780c`, `a37d7e7` **and** `07781a8`, so
the **entire production JS tree** — not merely the test corpus — is byte-identical across both
merges. The narrower "changed no JS test case" measurement holds a fortiori:
`git rev-parse <sha>:static/js/modules/__tests__` is
**`9db6d8b2e9635755775b8c362f9bebbd750ff3c3`** at all three, and `vitest.config.js` is
`c16ca428f7478708d8dd96a20ebcb86f98a8b935` at all three, so the collection mechanism did not move
either. [`TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) reads
`vitest.total_files = 13`, `vitest.total_cases = 231` at **both** `a37d7e7` and `07781a8`.
**T0 remains `2026-08-22T17:59:26Z`; the strict mark remains `2026-09-05T17:59:26Z`.**

**One packet is deliberately being held out of this window.** PR
[#431](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/431) (Packet U3a, KI-010) is open,
**draft**, retargeted to `main` and **18/18 green** — and it is **not merged by owner ruling OD-1**.
It takes the Vitest corpus **231 → 245**, so merging it *would* engage Q2's restart clause and reset
T0. It **must not land before `2026-09-05T17:59:26Z`**, and reaching that timestamp is **not itself
merge authorization**.

**Row 21 restarts nothing either — but the argument is NOT row 20's, and substituting it would be
wrong.** #427 is Packet U2's implementation and it **does** change the production JS tree:
`git rev-parse 1211915:static/js` returns `2d122654289967c4538b3086dddeb9e558393a53` while
`git rev-parse efa780c:static/js` returns **`fedecefa6acc738319ec95dc75e97009a5e24d03`**. The
whole-tree identity row 20 relied on is therefore **unavailable here, and is not claimed**. The
operative rule is the one this document has applied at every row since T0 — **"changed no JS test
case"**, not "changed no JS" — and it is satisfied by a narrower and stronger measurement:
`git rev-parse 1211915:static/js/modules/__tests__` and
`git rev-parse efa780c:static/js/modules/__tests__` both return
**`9db6d8b2e9635755775b8c362f9bebbd750ff3c3`**, so the entire Vitest corpus is byte-identical
across the merge, and `vitest.config.js` is unchanged at
`c16ca428f7478708d8dd96a20ebcb86f98a8b935`, so the collection mechanism did not move either. The
suite the window is qualifying is still **13 files / 231 cases**, re-read from
[`TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) at `efa780c` — while
`playwright.total_tests` moved **675 → 686** and `hard_waits.total_lines` held at **82**. **Q2's
restart clause did not engage. T0 remains `2026-08-22T17:59:26Z`; the strict mark remains
`2026-09-05T17:59:26Z`.** This is the same shape as row 12, the only other row whose carrier moved
`static/js`.

**The five non-attempt runs are unchanged, and were re-enumerated rather than carried forward.**
Each was resolved by enumerating its `/jobs` and matching the exact context string; all five return
**zero** `JS Unit (Vitest, non-required)` jobs — the three Dependabot `dynamic` runs, the one
`Deep Gate` `schedule` run, and the `Configured Graph Update` `dynamic` run. **No sixth has
landed.**

**Whoever merges THIS PR owes the next unclaimed row**, by the rule stated earlier in this block: a
PR cannot record its own landing.

**Row 19 is the one this extension exists for, and it is the row the window was most exposed to.**
PR [#426](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/426) (Packet U3b, KI-011) is the
**first post-T0 merge to rewrite the module `toast.test.js` imports**. A collection failure or a red
there would have **reset the clock to zero** (§6.5) and voided the premise its own Gate 1 was decided
on. **It did not**: the `JS Unit` job is `success`, and the suite it ran is **byte-identical** to the
one the window is qualifying.

**Q2's restart clause did not engage, and the argument is the narrow one §13.0 has used since row 12
— "changed no JS test case", not "changed no JS".** U3b **does** change the production JS tree, so
whole-tree identity is unavailable and is not claimed. The operative measurement is
`git rev-parse 3098282:static/js/modules/__tests__` and
`git rev-parse 5b35966:static/js/modules/__tests__`, both
**`9db6d8b2e9635755775b8c362f9bebbd750ff3c3`** — the entire Vitest corpus is byte-identical across the
merge, not merely the files someone remembered to check. `git rev-parse <sha>:vitest.config.js` is
`c16ca428f7478708d8dd96a20ebcb86f98a8b935` on both sides, so the collection mechanism did not move
either, and
[`TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) at `5b35966` reads
`vitest.total_files = 13`, `vitest.total_cases = 231` — unchanged — while `playwright.total_tests`
moved **662 → 675** and `hard_waits.total_lines` held at **82**. **T0 remains
`2026-08-22T17:59:26Z`; the strict mark remains `2026-09-05T17:59:26Z`.**

**Rows 17 and 18 restart nothing either, for the ordinary reason:** #429 was documentation-only and
#430 touched `utils/filter_predicates.py` and two documents — **zero** files under
`static/js/modules/__tests__/` in either.

**One obligation this extension does NOT discharge.** U3b's regression is **E2E-only by owner
ruling**, so the Vitest coverage for KI-011's helpers is deferred exactly as **U1-FOLLOWUP-1** is
(§v2.14 of [`volume_failure_feedback/PLANNING.md`](../volume_failure_feedback/PLANNING.md)) — it
**must not land before `2026-09-05T17:59:26Z`**, for the same reason.

**The five `main` runs in the window that are NOT qualification attempts.** **A fifth has landed
since the `2026-08-26T12:05:47Z` read, and the previous "no fifth non-attempt run has landed"
sentence is retired rather than restated.** Each was **re-enumerated rather than carried forward** —
resolved the same way as the rows above, by enumerating its `/jobs` and matching the exact context
string. All five returned **zero** `JS Unit (Vitest, non-required)` jobs, so the twenty-one-run
superset is 16 attempts + 5 classified, with nothing unaccounted for. *(The weekly `Deep Gate` cron
is still the only `schedule`-event run in the window and it has still fired once, on 2026-08-24; no
second cron firing has occurred at this read time.)*

| `main` run | Workflow / path | Event | Jobs | Why it cannot mint a ledger row |
|---|---|---|---|---|
| [`32676594582`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32676594582) | `pip in /. - Update #1537135558` — `dynamic/dependabot/dependabot-updates` | `dynamic` | **1** — `Dependabot`, `success` | Not `ci.yml`. Dependabot's update runner declares one job and **no** `js-unit`. It opened PR **#415**. |
| [`32676594619`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32676594619) | `npm_and_yarn in /. - Update #1537135574` — same path | `dynamic` | **1** — `Dependabot`, `success` | As above. It opened PR **#416**. |
| [`32676594928`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32676594928) | `github_actions in /. - Update #1537135595` — same path | `dynamic` | **1** — `Dependabot`, `success` | As above. It opened no PR. |
| [`32688747703`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32688747703) | `Deep Gate (manual + weekly)` — `.github/workflows/deep-gate.yml` | **`schedule`** | **7** — all `success` | Not `ci.yml`. `deep-gate.yml` contains **zero** occurrences of `js-unit` / `JS Unit`. Its own evidential value is R1-D3's, not this window's — see [`release_pipeline/PLANNING.md`](../release_pipeline/PLANNING.md) § *The second `schedule`-event run*. |
| [`33017596325`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33017596325) | `Configured Graph Update: pip in /. #1542182565` — `dynamic/dependabot/dependabot-updates` | `dynamic` | **1** — `Dependabot`, `success` | Not `ci.yml`. **The first non-attempt run minted by a merge rather than by Dependabot's scheduler** — PR #415's push to `main` changed a pip lockfile, which triggers a dependency-graph submission. One job, **no** `js-unit`. |

There is **no** `main` `ci.yml` run in this
window whose `js-unit` result is red, missing, skipped or cancelled, and **no** qualification
attempt this ledger omits. *(Row 1's run was **created** at `2026-08-22T17:59:06Z`, twenty seconds
**before** T0 — the ledger indexes `js-unit` **results** at or after T0, not runs, and that job's
`completed_at` **is** T0. A run created before T0 can still be row 1.)*

**Rows 13, 14, 15 and 16 did not restart the window, and none of the four `mergedAt` values is
T0.** By the stronger of the two available checks first: `git rev-parse 06a3f41:static/js`,
`git rev-parse 52c44c4:static/js`, `git rev-parse 7a64d2e:static/js`,
`git rev-parse db6c34b:static/js` and `git rev-parse b733c14:static/js` **all** return the same tree
hash, **`bd703e800d512c21e32d6f03066cfe8080859f93`**, so the entire JS tree is byte-identical across
all four merges. The suite the window is qualifying is therefore still **13 files / 231 cases**,
re-read from [`TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) at `b733c14`
(`total_files = 13`, `total_cases = 231`). The file lists agree: PR #424 touched **exactly two**
files (Packet U2's `PLANNING.md` and this document), PR #425 **exactly one**
(`toast_type_word_collision/PLANNING.md`), PR #415 **exactly one** (`requirements-build.txt`) and
PR #416 **exactly two** (`package.json` and `package-lock.json`). **T0 remains
`2026-08-22T17:59:26Z`; the strict mark remains `2026-09-05T17:59:26Z`.**

**Rows 14 and 16 needed an argument the twelve rows before them did not, because both are dependency
bumps and the earlier no-restart paragraphs all recited "no dependency" as part of their case.** That
recital is not available here, so the claim is made by measurement instead:

- **Row 14 (#415, PyInstaller 6.22.0 → 6.22.2)** changes `requirements-build.txt`, a **Python
  build-only** requirements file. It is not a Node dependency, is absent from `package.json`, and
  cannot reach a Vitest run at all.
- **Row 16 (#416, Sass 1.102.0 → 1.103.1)** changes `package.json` and `package-lock.json`, so it
  **is** a JS dependency change — the first to mint a ledger row. It still cannot move the suite:
  `sass` is a **devDependency only** (the manifest's runtime `dependencies` object is empty);
  `vitest.config.js` scopes `include` to `static/js/**/*.test.js`; **no file in the suite imports
  `.scss`, `.sass` or `.css`, and none imports `sass`**; and the `vitest`, `@vitest/coverage-v8` and
  `jsdom` pins are **byte-identical across `db6c34b → b733c14`** at `4.1.11`, `4.1.11` and `30.0.1`.
  The lockfile delta was also measured node-by-node: **277 package nodes before and after, none
  added and none removed**, with exactly two nodes carrying any field change — the root
  `devDependencies` pin and `node_modules/sass` (`version`, `resolved`, `integrity`). **No transitive
  dependency moved.**

**Neither is an "expansion packet" in Q2's sense**, which is what the restart clause is written
about; and the measured JS tree hash above settles it independently of how that phrase is read.

**Row 6 did not restart the window, and #417's `mergedAt` is not T0.** PR #417 touched **exactly
six** files — [`ACTIVE_DEVELOPMENT.md`](../ACTIVE_DEVELOPMENT.md),
[`DECISIONS.md`](../DECISIONS.md), [`MASTER_HANDOVER.md`](../MASTER_HANDOVER.md),
[`TESTING_STRATEGY_PLANNING.md`](../TESTING_STRATEGY_PLANNING.md),
[`release_pipeline/PLANNING.md`](../release_pipeline/PLANNING.md) and **this document** — and
**zero** files under `static/js/**`, no workflow, no dependency, no generated inventory and no
`vitest.config.js`. The suite the window is qualifying is therefore still **13 files / 231 cases**,
byte-identical across `31659a5 → 5111a7f`, and Q2's restart clause did not engage. **T0 remains
`2026-08-22T17:59:26Z`; the strict mark remains `2026-09-05T17:59:26Z`.** The same already held for
rows 3, 4 and 5.

**Row 7 did not restart the window either, and #418's `mergedAt` is not T0.** Measured, not
predicted: PR #418 touched **exactly three** files —
[`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md),
[`README.md`](../README.md) and **this document** — and **zero** files under `static/js/**`, no
workflow, no dependency, no generated inventory and no `vitest.config.js`. The check is stronger
than a file list: `git rev-parse 5111a7f:static/js` and `git rev-parse 26ce7e9:static/js` return
the **same tree hash**, `815ca75c109c93c0f914f36d0de24ba46a89bc3d`, so the entire JS tree — not
merely the files someone remembered to look at — is byte-identical across the merge. The suite the
window is qualifying is therefore still **13 files / 231 cases**, re-read from
[`TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) at `26ce7e9`
(`total_files = 13`, `total_cases = 231`), and Q2's restart clause did not engage. **T0 remains
`2026-08-22T17:59:26Z`; the strict mark remains `2026-09-05T17:59:26Z`.** The post-#417 block
predicted this outcome for the restart clause and explicitly refused to predict the run's
*result*; the result is row 7 above, and it was measured after the run existed.

**Rows 8 and 9 did not restart the window either, and neither `mergedAt` is T0.** By the stronger
of the two available checks first: `git rev-parse 26ce7e9:static/js`,
`git rev-parse 5ca4191:static/js` and
`git rev-parse 77f4adf:static/js` all return the **same** tree hash,
`815ca75c109c93c0f914f36d0de24ba46a89bc3d`, so the entire JS tree — not merely the files someone
remembered to look at — is byte-identical across both merges. The file lists agree: PR #419
touched **exactly one** file, this document, and PR #420 touched **exactly five** —
[`CSS_OWNERSHIP_MAP.md`](../CSS_OWNERSHIP_MAP.md),
[`DUPLICATION_REGISTRY.md`](../DUPLICATION_REGISTRY.md), [`REFACTOR_PLAN.md`](../REFACTOR_PLAN.md),
[`scan/README.md`](../scan/README.md) and this document — with **zero** files under
`static/js/**`, no workflow, no dependency, no generated inventory and no `vitest.config.js` in
either. The suite the window is qualifying is therefore still **13 files / 231 cases**, re-read
from [`TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) at `77f4adf`
(`total_files = 13`, `total_cases = 231`), and Q2's restart clause did not engage. **T0 remains
`2026-08-22T17:59:26Z`; the strict mark remains `2026-09-05T17:59:26Z`.**

**Row 10 did not restart the window either, and #421's `mergedAt` is not T0.** By the stronger of
the two available checks first: `git rev-parse 77f4adf:static/js` and
`git rev-parse b4d6b13:static/js` return the **same** tree hash,
`815ca75c109c93c0f914f36d0de24ba46a89bc3d` — the value rows 7, 8 and 9 also carry, so the entire
JS tree is byte-identical across all four of those merges. `git rev-parse 77f4adf:vitest.config.js`
and `git rev-parse b4d6b13:vitest.config.js` likewise both return
`c16ca428f7478708d8dd96a20ebcb86f98a8b935`. The file list agrees: PR #421 touched **exactly two**
files — **this document** and
[`volume_failure_feedback/PLANNING.md`](../volume_failure_feedback/PLANNING.md) — with **zero**
files under `static/js/**`, no workflow, no dependency and no generated inventory. The suite the
window is qualifying is therefore still **13 files / 231 cases**, re-read from
[`TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) at `b4d6b13`
(`total_files = 13`, `total_cases = 231`), and Q2's restart clause did not engage. **T0 remains
`2026-08-22T17:59:26Z`; the strict mark remains `2026-09-05T17:59:26Z`.**

**Row 11 did not restart the window either, and #422's `mergedAt` is not T0.** By the stronger of
the two available checks first: `git rev-parse b4d6b13:static/js` and
`git rev-parse 1243728:static/js` return the **same** tree hash,
`815ca75c109c93c0f914f36d0de24ba46a89bc3d` — the value rows 7 through 10 also carry, so the entire
JS tree is byte-identical across all five of those merges. `git rev-parse b4d6b13:vitest.config.js`
and `git rev-parse 1243728:vitest.config.js` likewise both return
`c16ca428f7478708d8dd96a20ebcb86f98a8b935`. The file list agrees: PR #422 touched **exactly two**
files — **this document** and
[`volume_failure_feedback/PLANNING.md`](../volume_failure_feedback/PLANNING.md) — with **zero**
files under `static/js/**`, no workflow, no dependency and no generated inventory. The suite the
window is qualifying is therefore still **13 files / 231 cases**, re-read from
[`TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) at `1243728`
(`total_files = 13`, `total_cases = 231`), and Q2's restart clause did not engage. **T0 remains
`2026-08-22T17:59:26Z`; the strict mark remains `2026-09-05T17:59:26Z`.**

**Row 12 did not restart the window either, and #423's `mergedAt` is not T0 — but the argument is
not the one rows 7 through 11 used, and substituting theirs would be wrong.** #423 is Packet U1's
implementation, and it **does** change the production JS tree: `git rev-parse 1243728:static/js`
returns `815ca75c109c93c0f914f36d0de24ba46a89bc3d` while `git rev-parse 06a3f41:static/js` returns
**`bd703e800d512c21e32d6f03066cfe8080859f93`**. The whole-tree identity that carried rows 7 through
11 is therefore **unavailable here, and is not claimed**. The operative rule is the one this
document has applied at every row since T0 — **“changed no JS test case”**, not “changed no JS” —
and it is satisfied by a **narrower and stronger** measurement than a file list:
`git rev-parse 1243728:static/js/modules/__tests__` and
`git rev-parse 06a3f41:static/js/modules/__tests__` both return
**`9db6d8b2e9635755775b8c362f9bebbd750ff3c3`**, so the entire Vitest corpus — not merely the files
someone remembered to look at — is byte-identical across the merge. `git rev-parse
1243728:vitest.config.js` and `git rev-parse 06a3f41:vitest.config.js` likewise both return
`c16ca428f7478708d8dd96a20ebcb86f98a8b935`, so the collection mechanism did not move either. The
file list agrees and is recorded in full because this is the first row-carrying PR since T0 whose
diff is not documentation-only: #423 touched **exactly eight** files —
[`UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md),
[`test_inventory/TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json),
[`test_inventory/TEST_INVENTORY.md`](../test_inventory/TEST_INVENTORY.md), **this document**,
[`volume_failure_feedback/PLANNING.md`](../volume_failure_feedback/PLANNING.md),
[`e2e/volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts),
[`static/js/modules/volume-splitter.js`](../../static/js/modules/volume-splitter.js) and
[`tests/test_volume_history_busy_signal_contracts.py`](../../tests/test_volume_history_busy_signal_contracts.py)
— with **zero** files under `static/js/modules/__tests__/`. The suite the window is qualifying is
therefore still **13 files / 231 cases**, re-read from
[`TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) at `06a3f41`
(`vitest.total_files = 13`, `vitest.total_cases = 231` — unchanged from `1243728`, while
`playwright.total_tests` moved **649 → 662** and `hard_waits.total_lines` held at **82**), and Q2's
restart clause did not engage. **T0 remains `2026-08-22T17:59:26Z`; the strict mark remains
`2026-09-05T17:59:26Z`.** **The absence of any Vitest file from #423 is deliberate and
owner-decided** — the reasoning, and the follow-up obligation it created, are recorded once in the
paragraph below that discharges #422's debt, and are **not restated here**. The fourth extension
predicted exactly this outcome for the restart clause and explicitly
refused to predict the run's *result*; the result is row 12 above, measured after the run existed.

**Two PRs are open at this read time, and neither is in this ledger.** Re-measured live at
`2026-08-26T12:05:47Z`, not carried forward: both are still `OPEN` and unmerged, and they are the
same two Dependabot PRs the previous five reads found. **#423 never
appeared in this table** — it was opened and merged between the `00:25:41Z` read and this one, so
it is row 12 above rather than a table entry here, exactly as #422 was at the previous read.
**The carrier of this extension is absent for
the same reason**: it did not exist at the read time. It is accounted for in
the carrier paragraph below instead:

| PR | Head | State | Why it is not a ledger row |
|---|---|---|---|
| [#415](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/415) | `dependabot/pip/pyinstaller-6.22.2` (`pyinstaller` 6.22.0 → 6.22.2) | **`OPEN`**, `MERGEABLE`/`CLEAN`, unmerged | Its `ci.yml` runs execute on a **PR branch**, not on `main` — outside §6.5's *"the clock starts on `main`"* rule, the same reason Packet F's own PR run `32599231895` was excluded |
| [#416](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/416) | `dependabot/npm_and_yarn/sass-1.103.1` (`sass` 1.102.0 → 1.103.1) | **`OPEN`**, `MERGEABLE`/`CLEAN`, unmerged | As above |

**Merging either of them mints the next sequential ledger row.** Do not write a fixed row number
into a forward-looking sentence: whichever of them lands first takes the next **unclaimed** row,
and the row a given PR receives depends on what merged before it.

**#418's debt is DISCHARGED.** The clause this block carried here before the
`2026-08-25T08:37:25Z` extension — *"#418 is the block's own carrier, and its merge is already
owed … whoever merges #418 owes its post-merge `js-unit` result in the next ledger refresh"* — is
spent as a live statement while remaining accurate as the dated prediction it was. It was
discharged on 2026-08-25: #418 merged as `26ce7e9`, and its post-merge `js-unit` result is **row 7**.

**#419's and #420's debts are both DISCHARGED too.** The clause the `2026-08-25T08:37:25Z`
extension left here — *“whoever merges the row-7 PR owes row 8 in the next ledger refresh”* — is
spent as a live
statement while remaining accurate as the dated prediction it was. It was discharged twice over
on 2026-08-25: #419 merged as `5ca4191` and its post-merge `js-unit` result is **row 8**; #420
merged as `77f4adf` and its result is **row 9**. **Two rows, not one, were owed when this
extension began**; the annotation above records why.

**#421's debt is DISCHARGED too.** The clause the `2026-08-25T14:50:55Z` extension left here —
*“whoever merges it owes the next sequential ledger row”*, written against the PR that carried
rows 8 and 9 — is spent as a live statement while remaining accurate as the dated prediction it
was. It was discharged on 2026-08-25: #421 merged as `b4d6b13`, and its post-merge `js-unit`
result is **row 10**.

**#422's debt is DISCHARGED too.** The clause the `2026-08-25T20:53:02Z` extension left here —
*“whoever merges it owes the next sequential ledger row”*, written against the
`docs/u1-gate1-plan` PR that carried row 10 and Packet U1's Gate 1 sign-off — is spent as a live
statement while remaining accurate as the dated prediction it was. It was discharged on
2026-08-25: #422 merged as `1243728`, and its post-merge `js-unit` result is **row 11**. The same
extension's prediction about the restart clause also held, and was measured rather than assumed:
the file list and both tree hashes are in the *Row 11 did not restart the window* paragraph above.

**#423's debt is DISCHARGED too.** The clause the `2026-08-26T00:25:41Z` extension left here —
*“Whoever merges it owes the next sequential ledger row”*, written against the Packet U1
**implementation** PR that carried row 11 — is spent as a live statement while remaining accurate
as the dated prediction it was. It was discharged on 2026-08-26: #423 merged as `06a3f41`, and its
post-merge `js-unit` result is **row 12**. The same extension's prediction about the restart
clause also held, and was measured rather than assumed — see the *Row 12 did not restart the
window* paragraph above, which records the one tree hash that **moved** as well as the two that
did not.

**The same mechanism now applies to the PR carrying THIS extension.** Row 12 is recorded by
Packet U2's **Gate 1 planning** PR, which changes no file under `static/js/**`, no workflow, no
dependency and no generated inventory — so it cannot engage Q2's restart clause, and the only
prediction made here is about that clause, **not** about its run's result. **Whoever merges it
owes the next sequential ledger row**, by the *Merging either of them mints the next sequential
ledger row* rule stated above.

**One superseded clause is retired rather than left to mislead.** The paragraph immediately below
opens *“That carrier changes the production JS tree, and it still cannot restart the window”* and
was written on 2026-08-26 about the **U1 implementation** carrier, in the future tense. It is now
spent as a live statement while remaining accurate as the dated prediction it was: that carrier
merged, and the measured outcome is the *Row 12 did not restart the window* paragraph above.
**It does not describe the current carrier**, which is documentation-only.

**That carrier changes the production JS tree, and it still cannot restart the window.** This is
the first row-carrying PR since T0 for which `static/js` moves, so the reasoning is spelled out
rather than reused. The operative rule is the one this document has applied at rows 2, 3, 4, 5, 6,
7, 8, 9, 10 and 11 — **“changed no JS test case”** — not “changed no JS”. The U1 implementation PR
edits [`volume-splitter.js`](../../static/js/modules/volume-splitter.js), which moves
`static/js`'s tree hash off `815ca75c109c93c0f914f36d0de24ba46a89bc3d`; it adds **no** file under
`static/js/modules/__tests__/`, changes **no** existing Vitest case, and leaves
`vitest.config.js` at `c16ca428f7478708d8dd96a20ebcb86f98a8b935` and the collection mechanism
untouched, so the qualifying suite stays at **13 files / 231 cases**. That omission is deliberate
and owner-decided: **OD-1** granted option (i) — E2E coverage only while this window is live — and
registered the Vitest file as **U1-FOLLOWUP-1**, which must not land before the strict mark. See
[`volume_failure_feedback/PLANNING.md`](../volume_failure_feedback/PLANNING.md) §v2.1, §v2.13 and
§v2.14. **Q2's restart clause therefore does not engage, T0 stays `2026-08-22T17:59:26Z` and the
strict mark stays `2026-09-05T17:59:26Z`** — but that is a statement about the restart clause,
**not** a prediction about the run's result.

**Row 11 rides an implementation PR on purpose, and the alternative was rejected.** Opening a
ledger-only PR to record row 11 would mint a twelfth row and owe a thirteenth, and so on without
end; every row in this block from 6 onward exists because some later PR carried the extension as a
rider.

> ⚠️ **DATED 2026-08-26 — this paragraph's closing sentence is spent as a live statement while
> remaining accurate as the `00:25:41Z` reading it was.** It said *“The U1 implementation PR is the
> next PR to merge, so it is the rider — which is why this document appears in a diff otherwise
> scoped to Packet U1's six functional artifacts.”* **That PR has since merged** (#423, `06a3f41`),
> so it is no longer *next*; and its diff was **eight** files, not six — measured in the *Row 12 did
> not restart the window* paragraph above. **The current carrier is Packet U2's Gate 1 planning PR**,
> whose diff is two documentation files. The retirement recorded three paragraphs above covers the
> same class of clause and is extended here rather than repeated.

**Still to do, and owed by whoever picks this up:** extend **this** block — not any of the three
superseded ones above, and **in place, as the three 2026-08-25 extensions and the three 2026-08-26 ones did**, rather than by minting a
fourth superseding block — at **every** later session until `2026-09-05T17:59:26Z`, at **job** level,
appending any red, missing, skipped or cancelled result rather than summarising it, and re-deriving
the whole ledger from the API rather than extending it from the page. **Classify, do not tally, any
`main` run that is not a `ci.yml` run.** **A red resets the window to zero** (§6.5), with §6.2's
attribution discipline argued on the record and never applied silently.

---

**The standing rule, from §6.5, and why Packet F satisfies it.**

> **"Final expansion packet" means the last of A, B, C to merge. Packet F is a separate required
> predecessor (§2.5) and may land inside the window; it does not restart it.**

**Packet F qualifies because it changes no JS test case.** Its diff (§13.1) touches the generator, the
generated inventory artifacts, one **pytest** file and this document — **zero files under
`static/js/**`**, and **zero** existing Vitest tests. The suite the window is qualifying —
**13 files / 231 cases** (M4) — is byte-identical before and after Packet F, so the run that the window
counts is measuring exactly the same thing on either side of the merge. Had Packet F added, removed or
renamed a single JS case, Q2's restart clause would engage on its own terms and this paragraph would be
wrong; §13.10 therefore makes **"13 files / 231 cases unchanged"** a gate, not a nicety.

**Status, stated exactly, because three annotations depend on this clause holding:**

> **Packet F planning has begun. Packet F implementation remains UNAUTHORIZED.**
>
> ⚠️ **ANNOTATION 2026-08-22 — SUPERSEDED by §13.16.** Gate 0 and Gate 1 are signed and
> implementation is complete (§13.17). **Q4, Q6 and D2 are still untouched**, and **merge is
> still unauthorized**. The three annotations that depend on this clause are each annotated in
> place rather than left to be re-derived from here.
>
> ⚠️ **FOLLOW-ON ANNOTATION 2026-08-23 — the "merge is still unauthorized" half is now spent.** The
> owner gave the separate merge confirmation and **Packet F merged as `2c95bae`** (PR #411,
> `2026-08-22T21:52:14Z`), post-merge `main` run `32600832091` **18/18 green** at job level.
> **Q4, Q6 and D2 are STILL untouched and still unauthorized** — that clause survives every
> annotation on this section, which is the whole reason it is stated separately.

This section is a plan and nothing else. **No generator change, no regenerated artifact, no pytest file,
no JS test, no workflow edit and no branch-protection change is made or authorized by it.** **Q4, Q6 and
D2 are untouched.** §13.13 restates the stop in full.

#### U3a's ledger extension — **WITHDRAWN 2026-08-27, superseded by PR #429**

> **This block recorded rows 14, 15 and 16 and is withdrawn in full.** While Packet U3a's Gate 1
> planning PR was open, **PR [#429](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/429)
> merged to `main` and wrote rows 13–16** — the same four results, from the same runs and jobs.
>
> **The unclaimed-first rule fired against this packet, exactly as designed.** U3a's block was
> written when #427 held row 13 and rows 14–16 were unclaimed; #429 landed first, so those rows are
> **no longer U3a's to write**. Restating them would put one result in the ledger twice, which is
> the single failure sequential numbering cannot survive — and it is the hazard U3a's own block
> named when it declined to restate row 13.
>
> **The results themselves are unchanged and are now on `main` at rows 13–16:**
> `33011674872`/`98319257214`, `33017593094`/`98339729053`, `33020896786`/`98350728218` and
> `33023109789`/`98358033353` — all `success`. **Nothing measured here was wrong; it was simply
> claimed elsewhere first.** The conditional row numbering U3a attached to its block was the correct
> precaution and it is what made this withdrawal a deletion rather than a correction.
>
> **U3a therefore writes no ledger row.** Whoever merges U3a's PRs still owes the post-merge
> `js-unit` result of each, by the standing *merging mints the next row* rule; **no row number is
> predicted for them here.**

### 13.1 Ownership, containment, and the must-not-touch list

| | |
|---|---|
| **Implementation modifies** | [`scripts/generate_test_inventory.py`](../../scripts/generate_test_inventory.py) — extended with **one** new collector and **one** new inventory block |
| **Implementation regenerates** | [`docs/test_inventory/TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) and [`docs/test_inventory/TEST_INVENTORY.md`](../test_inventory/TEST_INVENTORY.md) — **regenerated by the script, never hand-edited** ([`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md), *"Never hand-edit it"*) |
| **Implementation creates** | **Exactly one** new pytest contract file (name and justification: §13.7) |
| **This packet may modify** | `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` (this plan and its later execution record) |
| **Total files in the diff** | **five**. A **sixth file voids §13.10's gate derivation** and the gate set must be re-derived before anything is committed — the §11.12 rule, restated because Packet F's diff is larger than any previous step-12 packet's. ⚠️ **ANNOTATION 2026-08-22: the ceiling is SEVEN, by owner ruling QF5** (§13.16), which moved [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) and [`.claude/rules/testing.md`](../../.claude/rules/testing.md) in-scope. **The gate set was re-derived and did not change** — the *Tooling / scripts* row forces `/verify-suite` regardless, and `docs/**` plus an in-place edit under `.claude/rules/` add no gate. **Eight files is still a stop condition.** |

**Must not touch — each row has a reason, not just a prohibition:**

| Path / surface | Why it is off-limits |
|---|---|
| `static/js/modules/**` (production **and** `__tests__/**`) | Touching a JS test would move the 231-case suite and re-engage Q2's restart clause (§13.0). **This is the single most load-bearing containment rule in the packet.** |
| Any existing test file, JS or pytest | Same class; and an existing pytest file's node count moving would confound M8's second inventory move with a real change |
| `package.json`, `package-lock.json` | A dependency change is not a test-inventory change; and the shared `main` checkout is already at vitest **4.1.10** against a lockfile pinning **4.1.11** (M4) — a lockfile edit would make that divergence worse, not better |
| [`vitest.config.js`](../../vitest.config.js) | §11.1's ruling stands: the `configLoader: 'native'` warning (P11, §11.2) is **pre-existing** and Packet F must not "fix" it. Editing the config would convert a tooling packet into a config change and move the collector's own inputs |
| [`.github/workflows/**`](../../.github/workflows/ci.yml) | **No workflow edit is needed**: the `test-inventory` job already runs `npm ci` and already runs `--check` as its blocking step (M6). The job's stale *"not in branch protection"* comment is **known-stale and deliberately not fixed** ([`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)); Packet F does not own it |
| `scripts/release_gate.py` | Holds `REQUIRED_CONTEXTS`, the in-repo copy of the protected-context list. **`Test Inventory Drift` is already required (M1)** so no context is added or renamed by this packet, and that file must not move |
| Branch protection / repository settings | **No new required context.** `Test Inventory Drift` is context #11 of the **12** measured live (M1); the new surface inherits enforcement, which is §2.5's whole design |
| Production Python / Flask behavior (`routes/**`, `utils/**`, `app.py`, `templates/**`) | Out of scope entirely. Packet F is a tooling packet |
| `e2e/**` | Packet F **runs** the Chromium suite (§13.10) and adds, removes and renames **no** spec — which is what keeps two of the five pinned surfaces still *(six after this packet; the two E2E ones are unaffected either way)* |
| `.claude/settings.json`, any harness or permission configuration | **A permission failure during execution is a blocker to report, not authority to change configuration** (§11.12's rule, restated verbatim) |
| Shared canonical documents — `docs/MASTER_HANDOVER.md`, `docs/TESTING_STRATEGY_PLANNING.md`, `docs/UI_SCENARIOS_GAP_ANALYSIS.md`, [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) | Read-only here. **Two of them are made incomplete by this packet and the repair is routed to the owner, not taken** — §13.11-RF3 and §13.12-QF5 |
| §5 and §7 **of this document** | §5's expiry note and §7.1's context count both move when Packet F lands, and **both are recorded as observed drift in §13.11 rather than edited**. M1 is explicit: *"Record this as an observed drift; do NOT edit §7 — Packet F does not own it."* |

**Must not do**: promote `js-unit`; act on **Q4**, **Q6** or **D2**; begin any other packet; edit
`QUALITY_GATE.md`'s pinned-surface table even though this packet makes it a five-of-six list; or run
any mutation against the real `static/js` suite.

> ⚠️ **ANNOTATION 2026-08-22 — one clause above is SUPERSEDED; the rest stands.** Owner ruling
> **QF5** (§13.16) moved [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)'s pinned-surface table
> **and** [`.claude/rules/testing.md`](../../.claude/rules/testing.md) **in-scope**, and both were
> edited; §5 and §7.1/§7.2 were **annotated** under the same ruling, superseding the
> *"recorded as observed drift, not fixed"* disposition in the two rows above. **Everything else
> here held**: `js-unit` was not promoted, Q4/Q6/D2 were not acted on, no other packet was begun,
> and **no mutation ran against the real `static/js` suite** — R1 deleted those arms and the
> executed matrix confirms it (§13.17 Part 4).

### 13.2 What was measured before planning

**Every row is measured in this worktree on `9cb6cdc`, 2026-08-22, with `npm ci` run inside the
worktree.** §11.15 Part 1 established the discipline this subsection imitates: **measured and reasoned
are separated explicitly, and reasoning is never presented as measurement.**

**Part 1 — MEASURED.**

| ID | Measurement | Result | What it settles |
|---|---|---|---|
| **M0** | Ground truth | `origin/main` = **`9cb6cdc`**; PR #410 **MERGED** `2026-08-22T17:59:03Z`; post-merge run `32589375849` **18/18 success**; T0 job `97070630453` at **`2026-08-22T17:59:26Z`**; **0** `main` runs after T0; **0** open PRs; **no** pre-existing Packet F branch, worktree or PR (the only `packet.f` branch match is `wt/theme-animating-packet-f`, an unrelated historical CSS branch); worktree clean | §13.0's ledger, and that Packet F starts from nothing |
| **M1** | Branch protection, read live | **12** required contexts. **`Test Inventory Drift` IS required.** `JS Unit (Vitest, non-required)` is **absent** | **Packet F needs no branch-protection edit** — §2.5's central claim, now measured rather than assumed |
| **M2** | The generator at `9cb6cdc` | 461 lines; top-level JSON keys are exactly **`schema_version`, `generator`, `playwright`, `pytest`, `hard_waits`**; `SCHEMA_VERSION = 1`; `render_json` = `json.dumps(indent=2, sort_keys=True) + "\n"`; `_write(newline="\n")`; `_normalize()` collapses CRLF/CR; `_check()` prints **up to 200** unified-diff lines. **Zero Vitest references** in the generator or in either committed artifact. **Baseline `--check` is CLEAN** (`Test inventory is up to date.`, exit 0) | The extension point, the fail-closed idioms to **match not reinvent**, and a clean baseline to mutate from |
| **M3** | Consumer inventory (exhaustive grep over `*.py`, `*.yml`, `*.js`, `*.ts`, excluding `node_modules`, `.venv`, `artifacts/`) | The `ci.yml` *"Report totals"* step **indexes named keys only and never enumerates**, so a new sibling key is invisible to it. **No consumer parses the Markdown. No consumer enumerates top-level keys, validates a schema, or branches on `schema_version`.** The only *asserted* `schema_version` in the repo belongs to the unrelated program-backup feature. **No pytest file tests `scripts/generate_test_inventory.py` at all** | §13.5's `schema_version` ruling, and §13.7's "no overlap, because there is nothing to overlap with" |
| **M4** | Vitest baseline | **vitest 4.1.11** in this worktree (`vitest/4.1.11 win32-x64 node-v24.19.0`), lockfile-matching. **`npx vitest run` → 13 files passed (13), 231 tests passed (231), real exit 0.** Per-file counts: 15 / 29 / 2 / 15 / 3 / 7 / 22 / 47 / 12 / 35 / 13 / 29 / 2 = **231 across 13 files**. **231 unique `(file, name)` identities — zero collisions.** `vitest.config.js` `include` = `['static/js/**/*.test.js']`, environment `node` | The pin Packet F must reproduce, and §13.10's unchanged-suite gate |
| **M4-w** | The shared checkout | **The shared `main` checkout's `node_modules` has vitest 4.1.10** — behind the lockfile | **Any measurement taken in the shared checkout is against the wrong runner.** Implementation must `npm ci` inside its own worktree |
| **P1** | `vitest list`, human form | 231 stdout lines, `<repo-relative posix path> > <suite> > … > <case>`, exit 0 | Paths are already relative here — but see P3 |
| **P2** | `vitest list --json`, stdout form | A JSON **array**; each element has **exactly two keys**, `name` and `file`. `file` is **ABSOLUTE** with forward slashes. **No status, no `title`, no `ancestorTitles`** | §13.4's element-shape validation and the relativization requirement |
| **P3** | Determinism of listing order | **Three consecutive runs on an unchanged tree produced three different md5 sums.** After mapping to `(relative_file, name)` and **sorting**, all three are **byte-identical, 231 rows** | **Sorting is mandatory, not stylistic** — an unsorted pin reds a *required* gate at random |
| **P4** | `.skip` / `.todo` / `describe.skip` | **OMITTED entirely.** A 9-case probe listed **6** | Cuts both ways: drift **is** detectable (the row disappears), and **status is NOT reportable** — §13.3's price |
| **P5** | `test.each` | `test.each([1,2,3])` lists as **three separate rows** | Parameter-array shrinkage is detectable by count **and** identity |
| **P6** | `.only` | Collapses the file to its single `only` case; probe total went **231 → 232** instead of 231 + 9 | **A `.only` anywhere is a massive, unmissable identity change** |
| **P7** | `CI=true` | With `CI=true` **and** an `.only`, `vitest list --json` **exits 1 while still printing complete, parseable JSON**. With `CI=true` and no `.only`, exit **0** and the listing is the normal 231/13 | **The exit code must be checked; parseable output is not proof of success.** And the Linux CI job and a local Windows run agree on the clean tree |
| **P8** | A syntactically broken test file | Exit **1**, **0 bytes** of stdout | Collection failure is loud, not silent |
| **P9** | stdout contamination | A module-level `process.stdout.write('RAW STDOUT WRITE\n')` prefixed the JSON; parsing the captured stdout failed with `Unexpected token 'R'`, **exit code 0** — the exit code did **not** catch it. `console.log` was intercepted and did not leak | **Capturing stdout is an unsafe channel** |
| **P10** | `--json=<path>` | Wrote clean, fully parseable JSON to the file **while the same noise went to stdout and was discarded**. Exit-code semantics unchanged | **This is the robust capture channel** — §13.3's choice |
| **P11** | stderr | **Every** invocation writes ~385 bytes of `configLoader: 'native'` warning to stderr | **stderr can never be a health signal**, and merging it into the capture channel would contaminate **every** run |
| **P12** | Delimiter ambiguity | `name with > angle` + `has > inside name` → `name with > angle > has > inside name`. The join is **not invertible** | Acceptable **only** if the joined string is used whole and never re-split. **Measured today: 231 rows, 231 unique identities, zero collisions** |
| **P13** | The alternative collector, `vitest run --reporter=json` | Strictly richer — `status` (`passed`/`skipped`/`todo`), `ancestorTitles` as an **array**, `duration`. Reported **240** on the probe tree | **Disqualified. §13.3 treats this as a stop-condition, not a trade-off** |
| **P14** | Path relativization on Windows | `Path('D:/…/exercise-helpers.test.js').relative_to(REPO_ROOT).as_posix()` → `static/js/modules/__tests__/exercise-helpers.test.js`, **including with a lower-case drive letter** (`WindowsPath` comparison is case-insensitive). **No custom normalization needed** beyond `relative_to` + `as_posix()` | §13.4's relativization, with no hand-rolled path munging |
| **M6** | The `test-inventory` CI job | `runs-on: ubuntu-latest`, timeout 20 min; **`npm ci` already runs in this job**; the blocking `--check` step captures `$STATUS` and `exit $STATUS`; installs **no browsers** and starts **no Flask server** | **A Vitest collector needs no new step, no new dependency and no workflow edit** — and `vitest list` needs neither a browser nor a server, so that property is preserved |
| **M7** | Gate routing for Packet F's own diff | [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)'s **Tooling / scripts** row requires **`/verify-suite` regardless of what the targeted-test search returns** for a script that *"implements one of the two blocking gates (`generate_test_inventory.py`, `pyright_baseline_diff.py`)"*. `/verify-suite` = **full pytest + full Chromium E2E**. Reviewer: `code-reviewer`. `product-risk-reviewer` is **not** triggered — this script does not write the `exercises` catalog. `docs/**` edits fall under *Product docs only*: no tests required | §13.10's gate set is **forced**, not chosen |
| **M8** | The self-tripping regeneration | Packet F moves the inventory **twice**: (1) the new Vitest surface appears for the first time; (2) **adding a new pytest file under `tests/`** changes per-file pytest node counts and `total_files` / `deterministic_files`. Both must land in the **same commit** | §13.11-RF1, and §13.10's regenerate-last ordering |

**Part 2 — REASONED, not measured.** Every one of these is derived by reading source or documents. It is
recorded separately so no later session promotes an inference to a measurement:

| Claim | Basis |
|---|---|
| **A new top-level `vitest` key breaks no consumer** | Reasoned from M3's *behavior* of the `ci.yml` step (named-key indexing). **No one ran the modified step.** The proof is the CI run in §13.10, not this table |
| **The `&` in `_check(JSON) & _check(MD)` is non-short-circuiting, so a Markdown-only staleness is always reported** | Read from the generator source (`main()`), not executed |
| **Windows and Linux will agree on the sorted identity list** | Reasoned from P14 (relativization) + P3 (sorting) + P7 (CI=true agrees on a clean tree). **No Linux run was performed** — see the `MEASUREMENT NOT TAKEN` table |
| **Every mutation row's kill prediction (§13.8)** | Derived by reading the generator and the dossier. **Nothing in §13.8 has been executed** — ⚠️ **ANNOTATION 2026-08-22: all of it has now been executed; the measured results are §13.17, and three predictions were wrong.** |
| **`schema_version` should increment** | A judgement about what the field is *for*, resting on M3's finding that nothing reads it. **Flagged for the owner** (§13.12-QF2) |

**Part 3 — MEASUREMENT NOT TAKEN.** These facts are needed by the plan and the dossier does not contain
them. **None is guessed.**

| # | Missing fact | Why it matters | When it must be taken |
|---|---|---|---|
| **NT-1** | The **pytest baseline node count / file count** on `9cb6cdc` | M8's second inventory move is a pytest-count move, and §13.10 wants a before/after | At execution, **before** the new contract file is written |
| **NT-2** | Whether the **`Run Tests` (pytest) CI job installs `node_modules`** | Decides whether a pytest contract test may shell out to `vitest` at all. **M6 measured only the `test-inventory` job.** §13.7 designs around this by forbidding the subprocess in the contract test, so the answer changes nothing — but the plan must not *assume* it | Before any contract test is written that would need it |
| **NT-3** | Whether any **`VITEST_*` environment variable** redirects or alters `--json=<path>` output | `collect_playwright()` pops three `PLAYWRIGHT_JSON_OUTPUT_*` vars for exactly this reason; the Vitest analogue is unprobed | At implementation, before the subprocess call is finalized |
| **NT-4** | **Linux behavior of `vitest list --json`** | Every probe P1–P14 ran on **win32-x64 / node v24.19.0**. Cross-platform agreement is *reasoned*, and its only proof is the first ubuntu `--check` | ✅ **TAKEN AND CLOSED 2026-08-22** — job `97094899990` (`Test Inventory Drift`, `ubuntu-latest`) on PR run `32599231895`, conclusion **`success`**, completed `2026-08-22T21:19:58Z`, step *"Check committed inventory against a fresh Linux regeneration"* **`success`**. Agreement is now **measured** |
| **NT-5** | The **size** of the regenerated artifacts (added JSON/Markdown lines) | Bears on NT-6 and on review cost | At regeneration |
| **NT-6** | Whether a whole-surface drift **exceeds `_check()`'s 200-line diff cap** | With a 231-row identity list, a surface-wide drift could be truncated in the CI report — the gate still **reds**, but the operator sees a truncated diff | At the first deliberate red (§13.10 step 4) |
| **NT-7** | Whether **`describe.each`** expands in `vitest list` the way `test.each` does (P5 measured `test.each` only) | Only matters if a future JS test uses it; today none is known to | Before any future packet adds one |
| **NT-8** | The **wall-clock cost** of `vitest list` inside the `test-inventory` job (20-minute timeout, M6) | A collector that materially lengthens a required job is a cost the owner should see | The PR's first CI run |
| **NT-9** | `vitest list --filesOnly` output shape | Documented in `--help` (M5) but **not probed**. Named only so a later reader does not think it was evaluated and rejected on evidence | Only if the file-level-only design is ever revisited |

### 13.3 Collector design — `vitest list --json=<path>` CHOSEN; `vitest run --reporter=json` REJECTED

**The rejection is a stop-condition that was triggered and resolved by design, not a preference
balanced against others.**

| Candidate | Verdict | Basis |
|---|---|---|
| **`vitest list --json=<path>`** | **CHOSEN** | P10 — writes clean, fully parseable JSON to a file **while stdout noise is discarded**. P2 gives a two-key element shape that is trivially validated. P7/P8 keep the exit code meaningful |
| `vitest list --json` to **stdout** | Rejected | **P9** — a single module-level `process.stdout.write` prefixes the payload, `JSON.parse` fails with `Unexpected token 'R'`, **and the exit code is 0**. The failure is silent in exactly the channel the design would depend on |
| `vitest list` **human form** | Rejected | P1's paths are already relative and POSIX, which is tempting — but the output is a `>`-joined line format with **no structure**, and P12's join is non-invertible, so a parser would be guessing where the path ends and the suite begins |
| `vitest list --filesOnly` | Rejected | File-level only: it cannot see a deleted, renamed, `.skip`-ed or `.todo`-ed **case**, which is the entire requirement in §2.5. **Its exact output shape is NT-9, unprobed** — it is rejected on *what it reports*, not on measured behavior |
| **`vitest run --reporter=json --outputFile=<path>`** | **REJECTED — stop-condition** | See below |

**Why `vitest run --reporter=json` is a stop-condition.** P13 measured that it is **strictly richer**:
`status` (`passed`/`skipped`/`todo`), `ancestorTitles` as an **array** (no delimiter ambiguity at all),
`fullName`, `numTotalTests`. On the probe tree it reported **240** total — 231 plus **all 9** probe cases
including the skipped and todo ones. Everything §13.3 gives up, that reporter provides.

**It is still disqualified, on two grounds, and the second one alone ends the discussion:**

1. **It runs the tests.** `duration` is in the payload, so the collector's output becomes a function of
   machine speed. The determinism contract in the generator's own module docstring — *"no timestamps, no
   absolute paths, no host or tool versions"* — is violated at the source, and the inventory would have
   to strip the very fields that make the reporter richer.
2. **It couples a REQUIRED context to JS test OUTCOMES.** `Test Inventory Drift` **is required** (M1).
   If the generator shells out to `vitest run`, then **a single failing or flaky JS test reds a required
   check** — which is **de-facto promotion of `js-unit` to required**, the exact decision **D2 reserves
   for the owner** and which §0.1's revised gate places **after** a 14-day window that is still running
   (§13.0). **A packet whose stated purpose is to *precede* promotion cannot implement promotion as a
   side effect of a collector choice.**

> **This is recorded as a stop-condition already triggered and resolved.** The condition — *"the design
> would make `js-unit` outcomes block merges before D2 is signed"* — was reached during design, and the
> resolution is the collector choice itself. Had `vitest list` not existed, the correct action would have
> been to **stop and ask the owner**, not to adopt `vitest run` and note the coupling in a risk table.

**The price paid, stated plainly rather than minimized.** Per **P4**, `vitest list` **omits `.skip`,
`.todo` and `describe.skip` cases entirely** — a 9-case probe listed 6. Therefore:

- **The collector cannot report a `run` / `skip` / `todo` status. It cannot distinguish a skipped case
  from a deleted one.**
- **The schema must not claim to store status** (§13.5), and §13.7's contract test asserts the
  **absence** of any `status` key in the Vitest block, so the limitation is enforced rather than merely
  documented. A negative that nothing asserts is asserted by nothing.
- **The requirement in §2.5 is still met**: marking a case `.skip` or `.todo` **removes its row**, which
  moves both the count and the identity list, which reds the drift gate. The gate cannot stay green when
  a case is silently disabled — which is what §2.5 asked for. What is lost is *honest reporting of why*,
  not *detection*.

### 13.4 Parser and subprocess design

**Shape, matching `collect_playwright()` and `collect_pytest()` rather than inventing a third idiom
(M2).** The new function is `collect_vitest() -> tuple[dict[str, int], list[tuple[str, str]]]` —
per-file counts **and** the sorted identity list, returned together so the two can never be derived from
different runs.

**Exact argv:**

```python
[_npx(), "vitest", "list", f"--json={output_path}"]
```

- **`_npx()` is reused, not re-implemented.** It already raises `SystemExit` when `npx` is missing, with
  a message that names `npm ci` — the exact failure a fresh worktree hits. Matching M2's idiom.
- **`cwd=REPO_ROOT`**, as both existing collectors do, so `vitest.config.js` resolves and the emitted
  absolute paths are inside the repository (P14's precondition).
- **`capture_output=True, text=True, encoding="utf-8", errors="replace"`** — identical to the existing
  collectors. stdout is captured **only to be quoted in an error message**, never parsed (P9).
- **`env`**: the existing `collect_playwright()` pops three `PLAYWRIGHT_JSON_OUTPUT_*` variables so an
  ambient setting cannot redirect the report. **The Vitest analogue is `NT-3` — unmeasured.** The plan's
  instruction is to **probe it before finalizing**, and if any such variable exists, pop it by the same
  pattern. **Do not add speculative pops for names nobody measured.**
- **`CI` is neither set nor unset.** P7 measured both directions: on a clean tree `CI=true` gives exit 0
  and the normal 231/13, so the ubuntu job and a local Windows run agree; with an `.only` present,
  `CI=true` gives **exit 1 with parseable output** — which the exit-code check (below) turns into a loud
  failure, and which is the **desired** behavior for a stray `.only`.

**The temporary file — created outside the repository, on purpose.**

| Decision | Reason |
|---|---|
| Use `tempfile.mkdtemp()` in the **OS temp directory**, and write `<dir>/vitest-list.json` | P10 requires a file channel. Putting that file **inside** the repository risks two known traps: the *parametrized configuration surface* trips on **adding or deleting any file** under `.claude/commands/`, `.claude/agents/`, `.claude/rules/` or `docs/ai_workflow/` ([`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)), and that same document warns to **"never regenerate while an untracked or gitignored `.md` sits in a globbed surface directory"**. A transient file the generator itself creates during `--check` is precisely the shape of that trap. Keeping it out of the tree removes the class |
| Create the **directory**, let **Vitest** create the file | On Windows, holding an open Python handle on a path a child process is about to write is a locking hazard. Nothing needs the file until the child exits |
| Remove the whole temp directory in a **`finally`** | The generator runs in CI and locally; a leaked temp directory per invocation is a slow leak, and cleanup in `finally` survives the `SystemExit` paths below |
| **Never** write it under `artifacts/` or the repository root | Repository-root policy (ADR-002, [`CLAUDE.md`](../../CLAUDE.md) §3). `artifacts/` would also be *acceptable* by that policy — it is rejected only because the OS temp dir cannot interact with any globbed surface at all |

**Order of operations — the exit-code check comes BEFORE the parse, and that ordering is load-bearing:**

1. **Run** the subprocess.
2. **Check `result.returncode != 0` → `SystemExit`**, quoting truncated stdout **and** stderr, in the
   format `collect_playwright()` already uses. **P7 is the reason this is step 2 and not step 5**: a
   nonzero exit can accompany complete, parseable JSON, and a parser that reads the file first will
   produce a perfectly valid inventory from a run the runner considered failed. **P8 is the reason it
   cannot be skipped**: a broken test file exits 1 with 0 bytes, and the error message must say so rather
   than surfacing as a `FileNotFoundError`.
3. **Check the output file exists and is non-empty** → `SystemExit` naming the path.
4. **`json.loads`** the file's text. A `json.JSONDecodeError` is caught and re-raised as `SystemExit`
   with the first ~2000 bytes quoted — a truncated write must not surface as a traceback.
5. **Validate the top-level is a `list`** and that it is **non-empty** → `SystemExit`
   (*"refusing to write an empty inventory"*, matching `collect_playwright()`'s wording).
6. **Validate every element's shape**: a `dict` whose key set is **exactly `{"name", "file"}`** (P2).
   **Exactly**, not "at least" — a superset means the tool's output format changed, which is precisely
   what `collect_pytest()`'s parser-drift check exists to catch. Message: *"the output format changed;
   fix the parser rather than committing a wrong number."*
7. **Relativize**: `Path(element["file"]).relative_to(REPO_ROOT).as_posix()` (**P14** — no custom
   normalization, and it is measured to work with a lower-case drive letter). A `ValueError` from
   `relative_to` means Vitest listed a file outside the repository → `SystemExit`, never a silently
   dropped row.
8. **Sort** (**P3** — mandatory): identities sorted by `(relative_file, name)`; the per-file dict is
   emitted through `sorted()` at render time, as both existing collectors do.
9. **Cross-check** (below).

**The cross-check, in the spirit of `collect_pytest()`'s parsed-vs-reported assertion — and an honest
statement of what it cannot do.**

`collect_pytest()` can reconcile against a number **the tool itself prints** (`"N tests collected"`).
**`vitest list --json` prints no summary line at all** (P2), so **no parsed-vs-reported check of that
exact kind is available.** Proposing one anyway would be the strongest-sounding and least honest choice
in this plan. What is proposed instead:

| Check | Fails closed on | What it **cannot** catch |
|---|---|---|
| `sum(per_file.values()) == len(identities)` | An internal inconsistency between the two returned structures — the one defect that would let the count and the identity list disagree in the committed artifact | Anything where both are wrong the same way |
| **`len(identities) == len(set(identities))`** — duplicate `(file, name)` pairs are a **hard failure**, not a silent de-duplication | **P12's collision hazard.** Measured today: 231 rows, **231 unique identities, zero collisions** (M4). The moment two cases join on the same `>`-string, a set-based implementation would under-count **and stay green** | Nothing — but it is a *policy* choice: it converts a future naming collision into a red that a human must resolve by renaming a test |
| Every relativized path matches `static/js/**/*.test.js` — the config's own `include` (M4) | A collector that started listing files from outside the configured surface | A file inside the surface that stopped being collected |
| Non-empty overall, and **every listed file has ≥ 1 case** | An empty or half-collected listing that still parses | — |

**What none of them can catch, stated because it is the real hole:** a **well-formed but truncated**
listing — Vitest exits 0 and reports, say, 12 files instead of 13. Nothing in the payload declares an
expected total, so no self-consistency check can see it. **Two things do:** P8's measured fail-closed
behavior (a file that fails to collect exits 1 with empty stdout), and — decisively — **the committed
artifact itself**. The pin *is* the missing "reported total": a truncated listing produces a different
sorted identity list, and `--check` reds. **That is the strongest argument for committing the full
identity list rather than counts alone** (§13.5).

### 13.5 The proposed JSON schema addition

**A single new top-level key, sibling to `playwright` / `pytest` / `hard_waits`.** Literal shape
(`render_json` uses `sort_keys=True`, so key order in the file is alphabetical regardless; **array order
is the generator's responsibility**, which is why §13.4 sorts):

```json
"vitest": {
  "collector": "vitest list --json",
  "config_include": "static/js/**/*.test.js",
  "total_cases": 231,
  "total_files": 13,
  "files": [
    { "file": "static/js/modules/__tests__/exercise-helpers.test.js", "cases": 15 },
    { "file": "static/js/modules/__tests__/exercises.test.js", "cases": 29 }
  ],
  "cases": [
    { "file": "static/js/modules/__tests__/exercise-helpers.test.js", "name": "<suite> > … > <case title>" },
    { "file": "static/js/modules/__tests__/exercises.test.js", "name": "<suite> > … > <case title>" }
  ]
}
```

*(`files` and `cases` are shown truncated to two rows each; the real artifact carries **13** and **231**
respectively — M4.)*

**Every element, decided and justified:**

| Element | Decision | Justification |
|---|---|---|
| **Per-file counts** (`files[]`) | **Include** | Mirrors `pytest.files[]` and `playwright.specs[]` exactly, so the Markdown table and the human review experience match the tiers beside it. It is also the only surface that survives the 200-line diff cap legibly (NT-6) |
| **The sorted node-identity list** (`cases[]`) | **Include — this is the load-bearing element** | **Counts alone cannot detect a RENAME.** Renaming a case leaves 231/13 untouched and would pass a count-only pin silently, which is the same false-green class §2.5 exists to close. It is also the substitute for the reported-total cross-check the tool does not provide (§13.4). Cost: **231 rows** — the size in lines is **NT-5**. **Flagged to the owner as QF3** because it is the packet's largest artifact-size decision |
| **Totals** (`total_cases`, `total_files`) | **Include** | The `ci.yml` *"Report totals"* step indexes **named keys only** (M3), so a headline pair is what a future step-summary line would read. Names chosen as `total_cases` / `total_files`: "cases" is this document's own unit (§11.3) and Vitest's; no consumer enumerates keys, so nothing collides |
| **`collector`, `config_include`** | **Include** | Both are **fixed literals in the generator**, not host- or version-derived, so they cost no determinism. They record *how* the numbers were produced — the same role `playwright.project: "chromium"` plays. A future reader who finds 231 wrong needs to know it came from `list`, not `run` |
| **Any `status` field** | **FORBIDDEN, and asserted absent** | **P4**: `vitest list` cannot report status, and a schema field implying otherwise would be a lie in a generated artifact. §13.7's contract test asserts **no `status` key appears anywhere in the `vitest` block** |
| **Durations, tool version, absolute paths, timestamps** | **FORBIDDEN** | The generator's own determinism contract. This is also the second reason `vitest run` is rejected (§13.3) |
| **An `environment_dependent_*` allowlist for Vitest** | **Not added** | The pytest analogue exists for a **measured** host dependence (`shutil.which` over PowerShell hosts). **No Vitest file is measured to be host-dependent.** Adding an empty allowlist would create a suppression mechanism ahead of any evidence — and M2 records that the generator already fails closed when an allowlist entry goes stale. If ubuntu disagrees with Windows (NT-4), **that is a finding to investigate, never a row to add** |

**`schema_version` — RECOMMENDATION: increment `SCHEMA_VERSION` from `1` to `2`, and pin the new value
in the contract test.**

*Reasoning, based on M3's consumer inventory:*

- **Nothing in the repository reads it.** M3's exhaustive grep found **no consumer that branches on
  `schema_version`**, and the only *asserted* `schema_version` symbol belongs to the unrelated
  program-backup feature. **So incrementing breaks nothing and not incrementing breaks nothing** —
  the compatibility argument is empty in both directions, and cannot decide it.
- **What decides it is what the field is for.** A version field that does not move when a **new
  top-level surface** is added is a field that asserts nothing — the same "asserted by nothing" class
  this repository's false-green work keeps finding. Adding a sixth pinned surface is the largest schema
  change the artifact has had since it was created.
- **The bump only acquires meaning if something pins it.** §13.7's contract test therefore asserts
  `schema_version == 2` **exactly**. Without that assertion the increment is decoration.
- **The honest counter-argument, stated rather than hidden:** the change is **purely additive** — M3
  shows the `ci.yml` step is invisible to a new sibling key — and an integer version has no minor
  channel, so a bump to `2` signals "breaking" to a future consumer when nothing broke. A reader could
  reasonably rule "leave it at 1 and document that additive keys do not bump it."

> **This is genuinely contestable and is routed to the owner as §13.12-QF2**, with the packet's
> recommendation being **`2`**. Whichever value is chosen, **the contract test must pin it**, and the
> rule that produced the choice must be written into the generator as a comment so the next additive
> change is not decided again from scratch.

### 13.6 The Markdown surface

**Rows added to [`TEST_INVENTORY.md`](../test_inventory/TEST_INVENTORY.md):**

| Where | Added content |
|---|---|
| `## Totals` table | One row: `\| JS unit cases (Vitest) \| **231** across 13 files \|` — placed beside the existing Playwright and pytest total rows, in the same bold-number style `render_markdown()` already uses |
| A new `## Vitest test files` section | The `\| File \| Cases \|` table, **13** rows, right-aligned counts, matching the `## pytest files` and `## Playwright specs` sections' shape |
| A disclosure sentence under that heading | That the collector is `vitest list`, that **`.skip` / `.todo` cases do not appear at all** (P4), and that **status is deliberately not recorded** — so a human reading a count of 231 knows what 231 means |
| A pointer sentence | That the **per-case identity list lives in the JSON only** |

**The 231-row identity list is deliberately NOT rendered into the Markdown.** The `.md` is the
human-facing twin — `.claude/rules/testing.md` points prose at it — and 231 rows of `suite > case`
strings would bury the four tables that make it useful. The JSON carries the identities; the Markdown
carries the counts.

**Why the Markdown must be pinned INDEPENDENTLY of the JSON:**

1. **The generator already checks them separately, and the check is non-short-circuiting.** `main()`
   evaluates `_check(JSON_PATH, json_text) & _check(MARKDOWN_PATH, markdown_text)` — a **bitwise `&`**,
   so **both** are always evaluated and a Markdown-only staleness is reported in its own right. The
   design must not undo that by making the Markdown a projection nothing verifies.
2. **No consumer parses the Markdown at all** (M3). That is exactly why it needs its own pin: if
   `render_markdown()` silently omitted the Vitest section, **nothing anywhere would notice** — no test,
   no CI step, no reader who was not looking for it. The **byte diff is the only oracle the Markdown
   has**, and the only way that oracle can fire is if the numbers are actually restated there.
3. **The two failure directions are different defects.** A stale JSON is a collector or regeneration
   failure; a stale Markdown is a **renderer** failure — a `render_markdown()` that was not updated when
   `build_inventory()` was. §13.8 gives each its own mutation row (**F22**, **F23**) for precisely this
   reason.

### 13.7 The pytest contract file — name and justification

**Chosen filename: [`tests/test_vitest_inventory_contracts.py`](../../tests/test_vitest_inventory_contracts.py).**

**Idiom survey, done before choosing.** `tests/` carries **both** naming idioms:

| Idiom | Examples | When it is used |
|---|---|---|
| `test_<subject>_contracts.py` (**plural**) | `test_release_workflow_contracts.py`, `test_npm_audit_gate_contracts.py`, `test_playwright_runner_contracts.py`, `test_playwright_shard_launcher_contracts.py`, `test_agent_workflow_contracts.py`, `test_visual_selector_contracts.py` | A file pinning **several** related invariants about one subsystem |
| `test_<subject>_contract.py` (**singular**) | `test_node_version_contract.py`, `test_python_version_contract.py`, `test_packaging_contract.py`, `test_error_page_contract.py`, `test_bootstrap_version_contract.py` | A file pinning **one** fact |

*(The exact file census is not in the dossier and is not needed for the ruling — the idiom, not its
frequency, is what decides the name. Recorded so no later reader thinks a count was measured.)*

Packet F pins **many** invariants — the surface's presence, the totals, per-file counts, the identity
list's sortedness and uniqueness, the absence of a `status` key, `schema_version`, and the collector's
argv shape — so the **plural** form applies.

**Why `vitest_inventory` and not `inventory` or `test_inventory`:**

| Candidate | Verdict |
|---|---|
| **`test_vitest_inventory_contracts.py`** | **Chosen.** Names exactly what it pins: **the Vitest surface of the inventory** |
| `test_test_inventory_contracts.py` | Rejected — the doubled `test_test` reads as a typo and is hostile to grep |
| `test_inventory_contracts.py` | Rejected — **it over-promises.** It reads as "contracts for the inventory", but the other four pinned surfaces would still have **no test at all**, and a filename that claims coverage the file does not provide is the shallow-coverage failure class this repository has already recorded once (QUALITY_GATE `scripts/**` routing arc) |
| `test_generate_test_inventory_contracts.py` | Rejected — names the *script* rather than the *surface*, and would imply the file tests the whole 461-line generator |

**Overlap check — there is nothing to overlap with.** **M3 is explicit: no existing pytest file tests
`scripts/generate_test_inventory.py` at all.** `grep -rln "generate_test_inventory" tests/` returns only
files that mention it **in comments** — `tests/test_agent_workflow_contracts.py` (`:63`, `:69`, `:103`,
`:212`) and `tests/test_css_wp4_4_a11y_contracts.py:529`. **Packet F creates the first test of this
generator in the repository's history.** That is a notable fact about a script that implements a
**required blocking gate**, and it is recorded here rather than buried.

**Two authoring rules the new file must obey:**

1. **It must NOT shell out to `npx vitest`.** Its collection count and runtime would then depend on
   `node_modules` being present in the `Run Tests` job, which is **NT-2 — unmeasured**. The file asserts
   against the **committed artifact** and against the **generator's own structure**, with any subprocess
   behavior exercised through injected/faked results, never a real run. This keeps a **required** gate
   free of a dependency nobody has measured.
2. **Its collected node count must be identical on Windows and Linux.** No `shutil.which`-style
   parametrization, no environment-derived parametrize list. `ENVIRONMENT_DEPENDENT_PYTEST_FILES` exists
   because one file legitimately violates this (M2), and **Packet F must not add a second**. A
   `skipif`-marked test is still *collected*, so conditional skipping is safe; a conditional
   `parametrize` list is not.

**And it moves the inventory.** Adding this file changes per-file pytest counts, `total_files` and
`deterministic_files` — **M8's second move** — so §13.10 regenerates **after** the file exists, not
before.

### 13.8 Mutation matrix — F1–F27 (**PREDICTION**)

> **EVERY ROW BELOW IS A PREDICTION. NOTHING IN THIS MATRIX HAS BEEN EXECUTED.** No mutation has been
> applied to any file, real or copied, and no runner has judged any row. §10.7-R9's standing rule
> governs: a discrepancy at execution is **investigated**, never edited away to match what happened.
>
> ⚠️ **ANNOTATION 2026-08-22 — EXECUTED. This table is left as the PREDICTION it was**, which is the
> only way prediction and outcome can be compared. The measured matrix — with §13.15's repairs
> applied (F1–F5 on `T` only, F15 replaced, F25 split, F28 and F29 added) — is **§13.17**. **Three
> rows behaved differently from the prediction and are investigated there, not edited away here.**

**ID prefix — a recorded deviation.** `M1`–`M19` belong to Packet A, `N1`–`N32` to Packet B, `P1`–`P42`
to Packet C — **and in this section `M#` and `P#` additionally denote the measurement dossier's rows**,
which are cited throughout §13.2–§13.7. Reusing either letter would be doubly ambiguous. Packet F
therefore uses **`F`**, which is unused. **Throughout §13, `M#`/`P#` always mean the dossier; `F#`
always means a mutation row.**

**The four substrates. Every row names exactly one, and no row runs against the real JS suite:**

| Key | Substrate | Restore |
|---|---|---|
| **T** | A **temp fixture tree in the OS temp directory** — a minimal Vitest project (its own `vitest.config.js` and 2–3 tiny `.test.js` files with known counts), **never** `static/js`. Proves what the **collector** does | Delete the tree. Nothing in the repository was written |
| **G** | A **copy of the generator** plus a **copy of the committed artifacts** in a scratch directory, pointed at **T** | Delete the scratch directory |
| **W** | The **isolated worktree's real tracked files**, mutated in place and restored by **`git checkout -- <path>`**. Proves what the **committed pin** does — which **T can never prove** | `git checkout -- <path>`, then assert `git status --porcelain` is empty **and** `--check` is green again |
| **C** | A **copy of the new contract file** run under its own path, or the real one on **W** with git restore | As W |

**Harness rules, carried from §9.13-D3, §10.5, §10.12 and §11.8. All mandatory:**

- **Judge every row by the process EXIT CODE**, never by a parsed failure count. Packet B measured Vitest
  exiting 1 while printing zero failures; **P7 measures the mirror image for `vitest list`** — exit 1
  with complete, valid JSON.
- **Every pytest row must report the expected collected node count**, or be recorded as a loud
  **`BAD RUN`**, never a survivor (§10.12 defect 2: *a green run of the wrong suite is
  indistinguishable from a survivor if you only look at the exit code*).
- **Apply every mutation exactly once**; report **`NOT APPLIED`** otherwise.
- **Both directions where a row has one** — the false-green hardening arc's standing rule. F26 is F22's
  reverse direction and is not optional.
- **Compare each row's predicted killer against the runner's actual failure IDs**, not merely
  "went red / stayed green".
- **An unexplained survivor is a test weakness and must be fixed.** Only F27's survival is predicted, and
  it is **declared in advance** as a disclosed detection hole, not discovered as a mystery.
- **A `W` row must end with `git status --porcelain` empty.** If any `W` row leaves the tree dirty,
  **stop immediately** — that is a containment failure, and §10.12 defect 3's lesson applies: assert
  through git's own normalization, never a raw byte compare.

**Group A — the JS test surface. These are the rows §2.5 exists for.**

| # | Exact mutation | Substrate | Predicted killer | Anti-vacuity check | Apply / restore | Equivalence handling |
|---|---|---|---|---|---|---|
| **F1** | **Delete a whole `*.test.js` file** (in T: one fixture file; in W: temporarily `git rm --cached`-free rename of one real test file) | **T** then **W** | **PRED —** `--check` reds: `total_files` 13→12, `total_cases` drops by that file's count, and every one of its identity rows disappears. The new contract test also reds on `total_files` | Confirm the **pre-mutation** `--check` is green (M2's clean baseline) and that the diff names the deleted file, not just a number | T: delete the fixture file. W: `git mv` the file aside, then `git checkout .` + restore | Not equivalent under any implementation that pins per-file counts |
| **F2** | **Delete one `it(...)` case** from a Vitest file | **T** then **W** | **PRED —** `--check` reds on `total_cases` 231→230, the file's `cases` count, and one missing identity row | The diff must show **the removed identity string**, not only the count — a count-only red would also fire for F3 and would not distinguish them | T: edit the fixture. W: delete the case, then `git checkout --` | Not equivalent |
| **F3** | **Rename one case** (`it('a')` → `it('a renamed')`), leaving counts untouched | **T** then **W** | **PRED —** **only** the `cases[]` identity list reds. **`total_cases`, `total_files` and every per-file count are unchanged** | **This is the row that justifies committing the identity list at all** (§13.5). If F3 survives, the identity list is not doing its job and the schema decision must be revisited before merge | As F2 | Not equivalent — and if a count-only schema were adopted, F3 would become a **genuine equivalence**, i.e. an undetectable rename. That is the outcome the schema choice avoids |
| **F4** | **`it(...)` → `it.skip(...)`** on one case | **T** then **W** | **PRED —** identical signature to **F2** (P4: the row vanishes) | Must confirm the diff is **indistinguishable from a deletion** — that is P4's measured limitation, and the run must demonstrate it rather than the plan merely asserting it | As F2 | Not equivalent to green; **is** observationally equivalent to F2, which is disclosed, not hidden |
| **F5** | **`it(...)` → `it.todo('name')`** | **T** | **PRED —** same as F4 (P4) | Same as F4 | Edit the fixture | Same as F4 |
| **F6** | **Add `.only`** to one case (`it.only`) | **T** (both with and without `CI=true`) | **PRED —** **two distinct kills.** Without `CI`: exit 0, but the file **collapses to one row** (P6) → massive identity drift → `--check` reds. With `CI=true`: **exit 1** (P7) → the generator's step-2 exit check raises `SystemExit` **before parsing** | **Run both env states.** A harness that runs only one cannot tell which mechanism killed it, and P7's whole lesson is that the two are different | Edit the fixture; unset/set `CI` per arm | Not equivalent |
| **F7** | **Shrink a parameterized array**: `test.each([1,2,3])` → `test.each([1,2])` | **T** | **PRED —** count −1 and **one identity row (`param case 3`) disappears** (P5) | Assert the *specific* missing identity, not just the count — otherwise this row is indistinguishable from F2 and proves nothing about `each` expansion | Edit the fixture | Not equivalent |
| **F8** | **Add a new `*.test.js` file** with 1 case (the inverse direction of F1) | **T** | **PRED —** `total_files` +1, `total_cases` +1, one new identity row | **Both directions, per the harness rule.** A pin that reds on removal but not addition would let a new untracked test file drift in silently | Create then delete the fixture file | Not equivalent |
| **F9** | **Force an identity collision**: two cases in one file whose joined `suite > case` strings are byte-identical (P12's non-invertible join) | **T** | **PRED —** the collector's **uniqueness cross-check** (§13.4) raises `SystemExit` naming the duplicate | **Verify the failure is the uniqueness check, not a count mismatch.** If a set-based implementation slipped in, this row silently under-counts and **stays green** — which is exactly the defect the check exists to prevent | Edit the fixture | Not equivalent. Today's tree has **231 unique identities, zero collisions** (M4), so this row can only be exercised on T |

**Group B — the collector, parser and subprocess. Every row is a mutation of a COPY of the generator.**

| # | Exact mutation | Substrate | Predicted killer | Anti-vacuity check | Apply / restore | Equivalence handling |
|---|---|---|---|---|---|---|
| **F10** | **`collect_vitest()` returns empty structures** (`{}`, `[]`) with the fail-closed guard removed | **G** | **PRED —** with the guard removed, the generator **writes an empty surface and exits 0** — so the killer is the **non-empty guard itself** (§13.4 step 5). With the guard present: `SystemExit`, *"refusing to write an empty inventory"* | **Run both arms.** Guard-removed must be shown to produce a **green run with a hollow artifact** — that is the false green being prevented, and asserting it is the only way to know the guard is load-bearing | Edit the generator copy; delete the copy | Not equivalent |
| **F11** | **Move the exit-code check AFTER the parse** (or delete it), then run against a tree with an `.only` and `CI=true` | **G** + **T** | **PRED —** mutated: the run **succeeds** and commits a listing from a failed invocation. Unmutated: `SystemExit` on exit 1 **before** the file is read | **This row's value is entirely in the mutated arm** — P7 measured that the output is *complete and parseable*, so nothing downstream will notice. If the mutated arm also reds, the check under test is not the one doing the work | Edit the generator copy | Not equivalent |
| **F12** | **Delete the "output file exists / non-empty" check**, then run against a tree with a **syntax-broken** test file (P8: exit 1, 0 bytes) | **G** + **T** | **PRED —** the **exit-code check (F11's) fires first**, so this row is expected to be **co-killed** and may not isolate | **Declared in advance as a probable non-isolating row.** To isolate it, run a second arm with the exit-code check stubbed to always pass — then a missing file must produce a **named `SystemExit`**, never a `FileNotFoundError` traceback | Edit the generator copy | If it does not isolate even with the second arm, record as **co-killed with F11**, not as equivalent |
| **F13** | **Truncate the JSON output file** mid-array before the parse (simulate a partial write) | **G** | **PRED —** `json.JSONDecodeError` → converted to `SystemExit` with the payload's first bytes quoted | Assert the message quotes the payload. A bare traceback is a *failure*, but not the fail-closed behavior the generator's other collectors provide | Write a truncated file into the temp path in a harness fake | Not equivalent |
| **F14** | **Switch the capture channel from `--json=<path>` back to stdout**, then run against a tree whose test module does a top-level `process.stdout.write('RAW STDOUT WRITE\n')` | **G** + **T** | **PRED —** mutated: **`JSON.parse` fails with `Unexpected token 'R'` while the exit code is 0** (P9) — i.e. the failure the file channel removes. Unmutated (`--json=<path>`): **clean parse, noise discarded** (P10) | The unmutated arm is the anti-vacuity half: it must be shown to **succeed on the same contaminated tree**. Without it, the row proves only that a broken parser breaks | Edit the generator copy | Not equivalent |
| **F15** | **Merge stderr into the capture channel** (`stderr=subprocess.STDOUT`, or read stderr as the payload) | **G** | **PRED —** fails on **every** run, on a clean tree, because P11 measured **~385 bytes of `configLoader` warning on every single invocation** | This row must be run on an **unmodified tree** — its point is that the mutation cannot survive even one clean run. If it survives, the warning is not being produced and P11 must be re-measured | Edit the generator copy | Not equivalent |
| **F16** | **Delete the relativization** — commit `element["file"]` as emitted (absolute) | **G** + **W** | **PRED —** the artifact gains **absolute paths containing the checkout directory name**, which differ between this worktree, the shared checkout and the ubuntu runner → `--check` reds on **any** other machine. The contract test reds on the "every path is repo-relative POSIX" assertion | **Must be judged by the contract test, not by `--check` on the same machine** — locally the regenerated and committed files would agree, and `--check` would be **green**. That is the trap: this defect is invisible to the drift gate on the machine that created it | Edit the generator copy | Not equivalent |
| **F17** | **Drop `.as_posix()`** (use `str(Path(...))`) | **G** + **W** | **PRED —** backslash separators on Windows, forward on Linux → contract test reds on the separator assertion; CI `--check` reds against a Windows-generated artifact | Same trap as F16: **the local `--check` may be green**. The contract test must assert `"\\" not in path` explicitly, not merely that the path "looks right" | Edit the generator copy | **Genuinely equivalent on Linux only.** On a Linux-only run this row cannot be killed at all; it is a **platform-conditional** row and must be executed on Windows. Recorded, not skipped |
| **F18** | **Delete the sort** — emit rows in Vitest's own order | **G**, repeated **≥3 times** | **PRED —** three consecutive regenerations produce **three different artifacts** (P3 measured three different md5 sums), so `--check` reds **at random** — and, crucially, may pass once | **A single run of this row proves nothing.** It must be run **at least three times** and judged on *any* disagreement. This is the one row where "it went green" is not evidence of survival | Edit the generator copy | Not equivalent — but **flaky by construction**, which is precisely the defect |
| **F19** | **Delete the element-shape validation**, then feed an element missing `file` (or carrying a third key) | **G** | **PRED —** mutated: a `KeyError` traceback, **or** — worse — a silently skipped row if the implementation used `.get()`. Unmutated: `SystemExit` naming the format change | **Assert the unmutated arm fails on a SUPERSET key too**, not only on a missing key. P2 measured **exactly two keys**; an "at least these keys" check would pass a changed format and is the vacuous version of this validation | Feed a doctored payload through the harness | Not equivalent |
| **F20** | **Delete the `sum(per_file) == len(identities)` and uniqueness cross-checks** | **G** | **PRED —** **survives on a clean tree** — and is killed **only** in combination with **F9** (collision) or a doctored payload where the two structures disagree | **Declared in advance as a conditionally-killed row.** Its honest statement is: the cross-check has **no killer on today's tree**, because today's tree is internally consistent (M4: 231 rows, 231 unique). Its value is entirely prospective | Edit the generator copy | **Not** filed as an equivalence — it is a row whose kill requires a paired mutation, and the pairing is stated |
| **F21** | **Swap the collector to `vitest run --reporter=json --outputFile=<path>`** — the rejected design (P13) | **G** | **PRED —** killed by a **contract-test assertion on the generator's argv**: the constructed command must contain `list` and must **never** contain `run` or `--reporter` | **This is a design mutation, and its killer must be a real assertion, not a comment.** Without it, §13.3's stop-condition is a prose commitment that a later session can undo without any gate noticing. Also assert the artifact contains no `duration` and no `status` key | Edit the generator copy | Not equivalent — the two collectors produce different totals (P13 measured **240** vs 231 on the probe tree) |

**Group C — the artifact, the renderer, and the pipeline.**

| # | Exact mutation | Substrate | Predicted killer | Anti-vacuity check | Apply / restore | Equivalence handling |
|---|---|---|---|---|---|---|
| **F22** | **Stale JSON alone** — hand-edit **one number** in the committed `TEST_INVENTORY.json` Vitest block (e.g. `total_cases` 231 → 230) and leave the `.md` untouched | **W** | **PRED —** `--check` reds with `DRIFT: docs/test_inventory/TEST_INVENTORY.json differs…` **and** the Markdown check passes — the `&` is non-short-circuiting, so both are evaluated and exactly one reports. The new contract test also reds | **Confirm the Markdown check reports NOTHING in this arm.** If both files red, the two surfaces are not independent and §13.6's argument is wrong | `git checkout -- docs/test_inventory/TEST_INVENTORY.json`; assert `git status --porcelain` empty and `--check` green | Not equivalent |
| **F23** | **Stale Markdown alone** — delete the `## Vitest test files` table from the committed `.md`, leaving the JSON untouched | **W** | **PRED —** `--check` reds on the **Markdown only**. **No consumer parses the Markdown (M3), so the byte diff is the ONLY oracle this surface has** | **The row's real purpose is to prove that oracle exists.** If `--check` stays green, `render_markdown()` is not emitting the section it is supposed to, and §13.6 is unimplemented | `git checkout --`; assert clean and green | Not equivalent |
| **F24** | **`build_inventory()` omits the whole `vitest` key** (delete the block from the returned dict) | **G** + **W** | **PRED —** `--check` reds against the committed artifact **with a very large diff — possibly truncated at `_check()`'s 200-line cap** (NT-6). The contract test reds on `"vitest" in inventory` | **The contract test must assert the KEY'S PRESENCE, not merely that the numbers are right when present.** A test written as "if the key exists, its total is 231" is satisfied by deletion — the exact "a citation-shape contract must assert the symbol is **present**, or deletion satisfies it" failure recorded in the CSS citation-repair arc | Edit the generator copy / restore via git | Not equivalent |
| **F25** | **Schema/consumer mismatch** — rename the emitted key `vitest` → `js_unit` (or leave `schema_version` at `1` if the owner rules `2`) without updating the contract test | **G** + **C** | **PRED —** the contract test reds on the key name **and** on the pinned `schema_version`. **The `ci.yml` "Report totals" step does NOT red** — M3 measured that it indexes named keys only and never enumerates, so it is blind to both the addition and the rename of a sibling | **Assert the CI-step blindness explicitly rather than assuming it** — this is a *reasoned* claim (§13.2 Part 2), and the PR's own CI run is where it becomes measured | Edit the generator copy | Not equivalent |
| **F26** | **The reverse direction of F22** — leave the artifact correct and mutate the **contract test's pinned number** (231 → 999) | **C** | **PRED —** the contract test reds. `--check` stays **green** | **This is what proves the contract test's numbers are load-bearing rather than decorative.** If the contract test stays green with a wrong pinned number, it is not reading the artifact at all | Edit the contract-test copy | Not equivalent |
| **F27** | **A deliberately vacuous contract test** — replace a pinned assertion with a tautology, e.g. `assert isinstance(inventory["vitest"], dict)` in place of the exact-count assertion | **C** | **PRED — NO KILLER. THIS ROW IS PREDICTED TO SURVIVE, AND ITS SURVIVAL IS THE FINDING.** Full pytest passes, `--check` passes, CI is 18/18 green, and the surface is no longer pinned by the test at all | **There is no automated anti-vacuity check for this row, and inventing one would be dishonest.** The only detections are: (a) **F26** run in the opposite direction on the *same* assertion — a tautology cannot red when the artifact is wrong; and (b) a human reading the diff. Both are named as the mitigation | Edit the contract-test copy; discard | **Not an equivalence** — it is a **disclosed detection hole**. Filing it as "equivalent" would be the mistake: an equivalent mutant changes no behavior, whereas this one **removes protection while changing no observable outcome**. It is recorded here so a reviewer knows the matrix has a floor, and §13.12-QF7 asks whether the owner wants a stronger structural guard |

**Row count: 27 (F1–F27)** — **9** on the JS test surface (Group A), **12** on the collector/parser
(Group B), **6** on the artifact/pipeline (Group C). **Zero declared equivalences.** **One row (F27) is
predicted to survive as a disclosed detection hole**, **one (F17) is platform-conditional**, and **two
(F12, F20) are predicted to be co-killed or conditionally killed** — all three classes declared **in
advance**, per §11.8's rule that an unexplained survivor is a test weakness while a declared one is a
finding.

### 13.9 Determinism and cross-platform strategy

| Property | Mechanism | Evidence |
|---|---|---|
| **Stable order** | Identities sorted by `(relative_file, name)`; per-file dict rendered through `sorted()` | **P3 — mandatory, not stylistic.** Three consecutive unsorted runs produced three different md5 sums; after mapping and sorting, all three were **byte-identical, 231 rows** |
| **POSIX separators** | `Path(...).relative_to(REPO_ROOT).as_posix()` — no hand-rolled normalization | **P14**, measured on Windows including a **lower-case drive letter** |
| **No absolute paths** | Same, plus a contract assertion that every path starts with `static/js/` | P2 measured the raw form is absolute; **F16** is the mutation row |
| **LF newlines** | `_write(..., newline="\n")` — the existing writer, reused unchanged | M2 |
| **CRLF tolerance on `--check`** | `_normalize()` collapses CRLF/CR before diffing — reused unchanged | M2. This is why a CRLF checkout does not report phantom drift |
| **No timestamps, durations, host or tool versions** | Only `collector` — a **fixed literal in the generator**. ⚠️ **`config_include` was DROPPED** by the owner's design ruling (§13.16, R6): a literal claiming to record a config the generator never reads is a hand-maintained count in disguise | The generator's own determinism contract; and the second disqualifier for `vitest run` (P13's `duration`) |
| **No status field** | Forbidden by §13.5 and **asserted absent** by the contract test | **P4** |

**How Windows and Linux are proven to agree — and it is a proof, not an assertion:**

1. **The inputs are platform-independent.** A case identity is `(repo-relative POSIX path, joined case
   title)`. Both are functions of file contents. The **only** platform-varying element in the raw payload
   is the absolute path prefix (P2), and relativization removes it (P14).
2. **`CI=true` does not change the listing.** P7 measured that with `CI=true` and no `.only`, exit is
   **0** and the listing is the normal **231/13** — *"so the Linux CI job and a local Windows run
   agree"*. The env difference between the two hosts is therefore not a source of divergence on a clean
   tree.
3. **The proof is the CI run itself, and it is free.** The `test-inventory` job runs `--check` on
   **ubuntu-latest** after `npm ci` (M6) against an artifact regenerated on **Windows**. A whole-file
   text diff on a foreign platform is exactly the cross-platform oracle; if Linux disagrees by one byte,
   the **required** context reds. **This is `NT-4`, and the PR's first CI run is when it is taken.**
4. **If they disagree, the repair is investigation, not an allowlist.** No
   `ENVIRONMENT_DEPENDENT_*` entry may be added for a Vitest file (§13.5). The one existing entry exists
   for a *measured, designed* host dependence; a Vitest divergence would be an unexplained finding, and
   suppressing it would convert the new pin into decoration on the exact day it was created.

**One residual, disclosed:** **node/Vitest versions are not pinned into the artifact by design**, so a
lockfile bump that changes `list --json` output would move a **required** gate. That is **RF5** in
§13.11, and §13.12-QF6 asks whether the owner accepts it.

### 13.10 Verification plan

**M7 forces the gate set.** [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)'s **Tooling / scripts**
row requires **`/verify-suite` regardless of what the targeted-test search returns** when the changed
script *"implements one of the two blocking gates (`generate_test_inventory.py`, …)"*. **`/verify-suite`
= full pytest + the full Chromium E2E suite.** No targeted-union argument, and no override, is available
here — unlike Packet B's empty-union reasoning or Packet C's mapped-union resolution. **Required
reviewer: `code-reviewer`.** `product-risk-reviewer` is **not** triggered (M7).

**Ordering matters and is not free-form. The steps run in this order:**

| # | Step | Command | Expected outcome |
|---|---|---|---|
| **0** | **Record the baselines FIRST** | `npx vitest run`; `.venv/Scripts/python.exe -m pytest tests/ -q`; `.venv/Scripts/python.exe scripts/generate_test_inventory.py --check` | **13 files / 231 tests, exit 0** (M4); the pytest node/file totals — **`NT-1`, currently unmeasured, must be recorded here**; **`Test inventory is up to date.`, exit 0** (M2). A baseline that does not match M4 is a **stop condition** |
| **1** | Extend the generator | — | — |
| **2** | **Observe the gate go RED on purpose** | `.venv/Scripts/python.exe scripts/generate_test_inventory.py --check` | **MUST report `DRIFT` and exit 1.** **This step is not a formality — it is the packet's own anti-vacuity check.** §2.5 predicts *"it will trip its own gate, once and deliberately"*; if `--check` stays **green** after the collector is added, **the new surface is not actually pinned** and the packet has shipped nothing. **Capture the output** |
| **3** | Write the pytest contract file (§13.7) | — | The inventory is now **doubly** stale — M8's two moves: the Vitest surface **and** this file's own pytest node count |
| **4** | **Regenerate — LAST, after the contract file exists** | `.venv/Scripts/python.exe scripts/generate_test_inventory.py` | Writes both artifacts; the console summary prints the playwright/pytest/hard-wait totals. **Regenerating before step 3 would produce an artifact that is stale the moment the test file lands** |
| **5** | Focused contract tests | `.venv/Scripts/python.exe -m pytest tests/test_vitest_inventory_contracts.py -q` | All pass. **Judge by exit code**, and confirm the collected count for this file |
| **6** | **`--check` green again** | `.venv/Scripts/python.exe scripts/generate_test_inventory.py --check` | **`Test inventory is up to date.`, exit 0** |
| **7** | **Determinism — regenerate a SECOND time and compare bytes** | Run step 4 again, then `git status --porcelain docs/test_inventory/` | **Empty output.** A byte-identical second regeneration is the local proof that **P3's sorting** is in place. **Repeat a third time** — F18's lesson is that a single agreement is not evidence when the underlying order is genuinely random |
| **8** | **The JS suite is UNCHANGED** | `npx vitest run` | **13 files passed (13), 231 tests passed (231), exit 0** — identical to step 0 and to M4. **This is the gate that keeps §13.0's window intact**; any movement here means Packet F touched a JS test and Q2's restart clause engages |
| **9** | **FULL pytest** | `/run-tests` (or `.venv/Scripts/python.exe -m pytest tests/ -q`) | Green, with **exactly one new file's worth of nodes** above the step-0 baseline (NT-1). A larger delta means an existing file moved |
| **10** | **FULL Chromium E2E** | `/run-e2e` (`npx playwright test --project=chromium --reporter=line`) | Exit 0, zero failures. **Judge by exit code and zero failures, not by the "17 did not run" line** — the visual specs are excluded by default by design ⚠️ **ANNOTATION 2026-08-22: the second half is MEASURED FALSE.** `playwright.config.ts` has no `testIgnore` and no `grepInvert`, and neither spec self-skips — `PW_VISUAL_SEED` selects the **seed script**, not the spec set. A default run executes all 649 and reds 63 of them, so *"zero failures on a default run"* is a criterion that cannot be met. The suite needs **two** invocations; §13.17 Part 1 records both |
| **11** | The mutation matrix | §13.8, F1–F27, on substrates **T / G / W / C** | Every row behaves as predicted; **F27 survives as a declared detection hole**; every other survivor is a defect and is fixed. **F18 is run ≥3 times; F6 in both `CI` states; F17 on Windows** |
| **12** | PR CI | — | **All 18 jobs green** on the head commit — the same 18/18 shape measured on `9cb6cdc` (M0). **`Test Inventory Drift` green is the load-bearing one**, and its ubuntu run is where **NT-4** is finally taken ✅ **MEASURED 2026-08-22:** run `32599231895` on head `d7494e2` — **18 jobs, all 18 `success`**, enumerated at job level. `Test Inventory Drift` = job `97094899990`, `ubuntu-latest`, `success`. **NT-4 taken and closed** |
| **13** | **Window monitoring, continuing** | §13.0's ledger | **Every `main` `JS Unit (Vitest, non-required)` result from T0 through `2026-09-05T17:59:26Z`** is appended to §13.0, at job level (§6.1's discipline), including any red, missing or cancelled result. **A cancelled run neither starts nor advances the clock** (§6.5) |

**`/verify-suite` may be run as the single command covering steps 9–10**; it is written out here so the
two halves and their pass criteria are explicit.

### 13.11 Risks, ambiguities, and the self-tripping regeneration

| # | Risk / ambiguity | Disposition |
|---|---|---|
| **RF1** | **The packet trips its own gate TWICE** (M8): once for the new Vitest surface, once because **adding a file under `tests/`** moves per-file pytest counts and `total_files` / `deterministic_files` — the **first** pinned surface in QUALITY_GATE's trip table | **Both moves land in the same commit**, and §13.10 orders the steps so regeneration happens **after** the contract file exists. §2.5 anticipates move 1 (*"it will trip its own gate, once and deliberately"*); move 2 is the **ordinary `tests/**` rule**. **Neither is a workaround** — the repair path is the documented one. The failure mode to avoid is regenerating at step 2 and shipping an artifact already stale by one pytest file |
| **RF2** | **§5 of this document expires the moment Packet F lands.** Its own note says so: *"Once F pins Vitest nodes, every subsequent JS test add, remove, or rename will trip `Test Inventory Drift`"* | **Recorded, not edited.** §5 already carries its own expiry note pointing readers to §2.5. Packet F's execution record — if authorized — is the right place to annotate it in the §10.12 style, **not** this plan |
| **RF3** | **Two documents Packet F does not own become incomplete**: [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) says the artifact pins **five** change surfaces and lists five rows — there would be **six** — and **§7.1 of this file records 11 required contexts when M1 measured 12** (`JS Supply Chain (npm audit, non-required)` was promoted by PR #409, `a937116`), so **§7.2's "add a 12th context" becomes "add a 13th"** | **Both recorded as observed drift; neither is fixed here.** The dossier is explicit: *"Record this as an observed drift; do NOT edit §7 — Packet F does not own it."* `QUALITY_GATE.md` is a shared canonical document on the do-not-touch row (§13.1). **Routed to the owner as QF5**, exactly as Packet C routed its feature-map gap rather than fixing it |
| **RF4** | **After Packet F, every JS test change requires a regenerated artifact** — friction that did not exist for Packets A–C | This is the **intended** outcome, and it is the same discipline `tests/**` and `e2e/**` already carry. Recorded so a future JS packet's author is not surprised by a red on a test-only change |
| **RF5** | **NEW COUPLING: a dependabot Vitest bump can red a REQUIRED context.** If a future version changes `list --json`'s element shape (P2 measured exactly `{name, file}` on **4.1.11**), the shape validation fails closed and `Test Inventory Drift` reds on a dependency PR | **Deliberate — failing closed is the design.** But it is a **new** way for a required check to red on a change that touches no test, and the owner should see it before it happens (**QF6**). The §6.2 precedent is directly on point: the only three `js-unit` reds ever measured were a **dependabot** engine incompatibility |
| **RF6** | **The shared `main` checkout has vitest 4.1.10 against a lockfile pinning 4.1.11** (M4) | **Any measurement or regeneration performed in the shared checkout is against the wrong runner.** Implementation must run `npm ci` **inside its own worktree**, per the standing worktree rule that a junction inherits main's install state |
| **RF7** | **A whole-surface drift may exceed `_check()`'s 200-line diff cap** (M2), truncating the CI report | **The gate still reds** — only the operator's view is truncated. **NT-6** takes the measurement at §13.10 step 2, which produces exactly that diff. If it truncates badly, the repair is a **follow-up on the generator's reporting**, not a smaller pin |
| **RF8** | **P4's honesty limit**: the artifact cannot distinguish a `.skip`-ed case from a deleted one | **Disclosed in the Markdown surface itself** (§13.6) and enforced by the no-`status` assertion (§13.5). **Detection is unaffected** — both change the pin — and §2.5's requirement is about detection. **QF4** asks the owner to accept it explicitly rather than letting it be discovered later |
| **RF9** | **P12's collision hazard**: two cases could in principle join to the same identity string | **Zero collisions today** (M4: 231 rows, 231 unique). The collector treats a duplicate as a **hard failure** rather than de-duplicating (§13.4), so a future collision becomes a red a human resolves by renaming — not a silent under-count. **F9** is the mutation row |
| **RF10** | **The new contract test could itself be vacuous**, and §13.8-**F27** predicts **no automated killer** for that | **Disclosed, not solved.** Mitigations are F26 (reverse direction on the same assertion) and human review of the diff. **QF7** asks whether the owner wants a stronger structural guard. Claiming this hole is closed would be the single most damaging false claim this plan could make |
| **RF11** | **NT-2 is unmeasured** — whether the `Run Tests` job has `node_modules` | **Designed around**: §13.7 forbids the contract test from shelling out to `npx`. The risk is therefore *not* taken; it is recorded so nobody later "improves" the test by adding a real collector invocation |
| **RF12** | **Cross-platform agreement (NT-4) is reasoned, not measured** | §13.9 states the reasoning and names the CI run as the measurement. **It must not be written up as measured until that run exists** |

### 13.12 Owner questions for Gate 1

**These are decisions the packet cannot take for itself.** They are separate from acceptance of the work
specified above.

1. **QF1 — Is Packet F authorized to proceed past Gate 1 at all?** §0.1's Q5 makes Packet F a **required
   predecessor** to D2, and §11.18's STOP lists **Packet F** among the items *"still not authorized,
   each needing its own confirmation."* **Gate 1 approval is that confirmation.** If granted, please
   state **separately** whether **committing, pushing and opening a PR** are authorized. **Merge is NOT
   requested** and, per the standing protocol, requires its own later confirmation naming the PR —
   **green CI is not that confirmation, and neither is a selection among options.**
2. **QF2 — `schema_version`: increment to `2`, or leave at `1`?** **M3 measured that nothing reads it**,
   so compatibility cannot decide it. The packet **recommends `2`**, because a version that does not move
   when a new top-level surface is added asserts nothing — and because the contract test will pin
   whichever value is chosen, which is what gives the field any force. **The counter-argument is real**:
   the change is purely additive, and an integer version has no minor channel, so `2` signals "breaking"
   when nothing broke. **This is genuinely contestable; the packet will not self-resolve it.**
3. **QF3 — Does the committed JSON carry the full sorted identity list (231 rows), or per-file counts
   only?** The identity list is **the only thing that detects a case RENAME** (F3 — counts are unchanged
   by a rename) and it substitutes for the reported-total cross-check `vitest list` does not provide
   (§13.4). Its cost is artifact size, which is **NT-5, unmeasured**. **The packet recommends including
   it.** Ruling "counts only" is coherent — it accepts that renames are invisible — but it should be
   ruled, not defaulted into.
4. **QF4 — Is P4's limitation accepted on the record?** `vitest list` **cannot distinguish a `.skip`-ed
   case from a deleted one and cannot report status at all**. Detection is unaffected; **honest
   reporting is**. The alternative collector that *does* report status is `vitest run`, which §13.3
   rejects as a **stop-condition** because it would couple a required context to JS test outcomes ahead
   of D2. Confirm the trade as described, or direct otherwise — noting that "otherwise" is a promotion
   decision in disguise.
5. **QF5 — The two documents Packet F makes incomplete: follow-up, or in-scope?** (a)
   [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)'s *"pins five change surfaces"* table would have
   **six**; (b) **§7.1 of this file records 11 required contexts where M1 measured 12**, so §7.2's *"add
   a 12th"* is now *"add a 13th"*. **The packet recommends a separate follow-up for both** — the first is
   a shared canonical document, the second is a section Packet F does not own, and the dossier's
   instruction is explicit that §7 must not be edited here. Confirm, or authorize either edit in this
   packet.
6. **QF6 — Is the new dependabot coupling accepted?** After Packet F, a Vitest version bump that changes
   `list --json`'s output shape reds the **required** `Test Inventory Drift` context on a dependency PR
   that touches no test (**RF5**). Failing closed is the design; the §6.2 precedent — the **only** three
   `js-unit` reds ever measured were a dependabot engine incompatibility — makes this a realistic
   scenario rather than a theoretical one.
7. **QF7 — Does the owner want a structural guard against a vacuous contract test?** §13.8-**F27** is
   predicted to **survive with no automated killer**: a tautological assertion leaves full pytest,
   `--check` and CI all green while the surface is unpinned. The packet's mitigations are **F26's reverse
   direction** and **human review**. A stronger guard (for example, a meta-test asserting that the
   contract file contains the literal pinned counts) is possible but is **additional scope**, and the
   packet will not adopt it unilaterally.
8. **QF8 — Confirmation only: Packet F lands inside the qualification window and does not restart it.**
   §6.5 already rules this — *"Packet F … may land inside the window; it does not restart it"* — and
   §13.0 records why Packet F satisfies the condition: **it changes no JS test case**, so the suite the
   window qualifies is byte-identical either side of the merge. Confirmation is sought that approving
   Packet F draws in **none** of **Q4**, **Q6** or **D2**.

*(Not owner questions, recorded so they are not mistaken for any: the mutation-ID prefix is **`F`**
because `M`/`N`/`P` are taken by Packets A/B/C **and** because `M#`/`P#` denote the measurement dossier
throughout §13; and the choice of `tests/test_vitest_inventory_contracts.py` is a naming decision the
packet takes for itself under the surveyed idiom, §13.7.)*

### 13.13 STOP — **DISCHARGED FOR IMPLEMENTATION 2026-08-22; THE MERGE HALF STANDS**

> ⚠️ **ANNOTATION 2026-08-22 — the STOP below is superseded in part and is annotated, not
> rewritten.** The owner signed **Gate 0 and Gate 1** at **§13.16** and separately authorized local
> implementation, mutation execution, commit, push and a **ready-for-review** PR. The bullets below
> covering the generator, the artifacts, the contract file, the §13.8 mutations, and committing /
> pushing / opening a PR are **discharged**; the execution record is **§13.17**.
>
> **What is NOT discharged, and is unchanged in force:** **merging** — a separate confirmation
> naming the PR, which **green CI is not** and **a multi-choice selection is not**; **Q4**, **Q6**
> and **D2**; every branch-protection or repository-settings change; every edit to
> `.github/workflows/**`, `scripts/release_gate.py`, `package.json`, `package-lock.json`,
> `vitest.config.js`, `static/js/**` and any existing test; and any `.claude/settings.json` or
> permission change. **The two shared canonical documents this STOP forbade —
> [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) and `.claude/rules/testing.md` — were moved
> IN-SCOPE by ruling QF5**, and by nothing else.

> **This section is a plan. It is not authorization to implement it.**

**Nothing has been executed.** No generator change exists, no inventory has been regenerated, no pytest
file has been written, **no mutation in §13.8 has been applied to anything**, no branch has been pushed
and no PR has been opened. The only work performed is **measurement** — the dossier summarized in §13.2,
taken read-only in this worktree — plus the writing of this section.

**Every number in §13.8, §13.9 and §13.10's expectations is a PREDICTION.** §10.7-R9's standing rule
governs all of them: a discrepancy at execution is **investigated**, never edited away.

**Explicitly unauthorized, each needing its own confirmation:**

- **Modifying [`scripts/generate_test_inventory.py`](../../scripts/generate_test_inventory.py)**, in any
  way, including "harmless" ones.
- **Regenerating or hand-editing [`docs/test_inventory/`](../test_inventory/)**.
- **Creating `tests/test_vitest_inventory_contracts.py`** or any other test file.
- **Running any mutation from §13.8**, including on a copy or a temp fixture.
- **Committing, pushing, opening a PR** — and **merging**, which is a **separate confirmation again,
  naming the PR**, per the standing protocol.
- **Promotion of `js-unit` (Q4 / D2)**, **Q6**, and any branch-protection or repository-settings change.
- **Any edit to `.github/workflows/**`, `scripts/release_gate.py`, `package.json`,
  `package-lock.json`, `vitest.config.js`, `static/js/**`, any existing test, or any shared canonical
  document** — including [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md), whose five-surface table
  this packet makes incomplete and **still may not repair** (QF5).
- **Any `.claude/settings.json` or permission change.** A permission failure during execution is a
  **blocker to report, not authority to change configuration.**
- **The promotion packet itself.** Packet F is a **predecessor** to D2, not a step of it.

**Awaiting explicit owner approval of Gate 1 and rulings on the eight questions in §13.12.**

> ⚠️ **ANNOTATION 2026-08-22 — the line above is superseded by the council and is annotated, not
> rewritten.** The **Gate 1 council has since run** (§13.14) and returned **42 findings, 3 of them
> BLOCKER**, with all three reviewers independently reaching **NEEDS REVISION**. Two consequences:
>
> - **The questions are now NINE, not eight.** **QF9 — plan-stage size** was added because two
>   reviewers read Packet F as **Large** under `QUALITY_GATE.md`'s plan-stage routing (Gate 0 **+**
>   council), while §13.12-QF1 requests Gate 1 alone. **The packet does not decide it.**
> - **Approval must be given against the REVISED plan, not this one.** §13.15 records the **29 binding
>   revisions** — four of them blocking — that separate the drafted plan (§13.1–§13.13) from the
>   reviewed one. **Nothing in §13.15 has been implemented either.** ⚠️ **ANNOTATION 2026-08-22:
>   §13.15 has since been implemented in full — see §13.16 for the approval and §13.17 for the
>   record of how each of R1–R29 was discharged.**
>
> **The STOP above stands in full and is discharged by nothing.**

### 13.14 Plan v2 record — Gate 1 council (2026-08-22)

**The council ran.** Three reviewers — `architecture-reviewer`, `test-strategist`, `product-risk-reviewer`
— were launched in parallel against §13 as drafted (lines 3903–4626 at the time), each given the same
live measurement dossier and each told to re-derive rather than trust it. **42 findings** were returned:
**3 BLOCKER**, **14 MAJOR**, **19 MINOR**, **6 NIT**.

**This subsection is what earns the "PLAN v2" label in §13's heading.** §13's preamble was correct when
written that no council record existed; it exists now, and the preamble is annotated at the end of this
subsection rather than rewritten.

**Verdict of the council: NEEDS REVISION — Gate 1 should not pass on §13 as drafted.** All three
reviewers reached that conclusion independently, and all three named the **same** blocking defect.

---

#### Part 1 — what was MEASURED at council time, and what remains reasoned

Six findings were checked against the code by the launching session before disposition, because a
reviewer claim is not evidence either. **Every one held.**

| Check | Result |
|---|---|
| §13.1 forbids *"run any mutation against the real `static/js` suite"* while F1–F4 name substrate **W** | **CONFIRMED** — the contradiction is literal, at `:4025` against `:4411–4414` |
| Packet C already ruled on this exact technique | **CONFIRMED** — §11.1: *"In-place mutation with byte-restore is **not** an alternative — §10.1's reasoning transfers verbatim"* |
| Four sites still assert Packet F is "untouched"/"unstarted" un-annotated | **CONFIRMED** at lines 2200, 3337, 3716 (line 2193 was already covered by its own following annotation) |
| No required gate covers production `static/js/**` today | **CONFIRMED** — `tsconfig.json` `include` is `["e2e/**/*.ts", "playwright.config.ts"]` with no `allowJs`/`checkJs`; `Code Linting` is flake8-only |
| `subprocess.run(capture_output=True, stderr=subprocess.STDOUT)` raises | **CONFIRMED** — `ValueError: stdout and stderr arguments may not be used with capture_output`. **F15 is not merely equivalent; it is unrunnable as written** |
| The parser-seam precedent exists and has the claimed shape | **CONFIRMED** — [`tests/test_pyright_baseline_diff.py`](../../tests/test_pyright_baseline_diff.py) imports pure functions, feeds in-test fixtures, and tests repo-relative POSIX normalization against a **fake absolute root** (`REPO = Path("/repo").resolve()`), with no subprocess and no `node_modules` |

**Two new measurements were taken at council time**, and both change the plan:

- **S1 — the `T` substrate CANNOT live in the OS temp directory.** A fixture Vitest project built under
  the scratchpad failed with **`ERR_MODULE_NOT_FOUND`** on `vitest` itself: `--root` moves module
  resolution outside the worktree's `node_modules`. The same fixture placed under the **gitignored
  `artifacts/`** collected correctly (exit 0, 1 case listed). **§13.8's substrate table is wrong on
  this point and must be corrected** — `T` belongs under `artifacts/`, which is also where Packet C put
  its harness (§11.1) and which keeps it out of every globbed surface. *(This does not affect §13.4's
  temp-file decision: the collector's `--json=<path>` **output** file has no module-resolution needs and
  correctly stays in the OS temp dir.)*
- **S2 — the throwing-import coupling is MEASURED, not inferred.** A fixture whose test file imports a
  production module that throws at module scope made `vitest list --json` **exit 1 and produce no JSON
  file at all**; the same fixture with the throw removed exited **0** and listed its case. `architecture`
  filed this as INFERRED; **it is now measured**, and it upgrades finding AR3 from a reasoned risk to a
  demonstrated one.

**Reasoned, not measured, and still so after the council:** cross-platform agreement (**NT-4** — every
probe was win32; the first ubuntu `test-inventory` run is the measurement), `describe.each` expansion
(**NT-7**), and the behavior of `--allowOnly=false` with an `.only` present.

**A dossier error the council surfaced, corrected here:** the dossier's M2 recorded the generator as
**461 lines**; it is **469**. §13.2-M2 and §13.7 quoted the wrong figure, and §13's own evidence rule
makes it load-bearing because it appears inside a rejection rationale.

---

#### Part 2 — the three BLOCKERs, and the dispositions that change the deliverable

| # | Finding | Raised by | Disposition |
|---|---|---|---|
| **B1** | **F1–F4 mutate the real JS suite**, which §13.1 calls the packet's most load-bearing prohibition and §13.8's own preamble denies doing (*"no row runs against the real JS suite"*). F1's restore recipe is also broken twice over: `git checkout .` does not undo a staged `git mv`, and `git checkout .` is **repo-wide**, so it would discard unrelated uncommitted work | **all three** | **ACCEPTED IN FULL.** The `W` arms are **deleted** from F1–F5; those rows run on **`T` only**. The committed-pin claim they were reaching for is already proven by **F22/F24**, which mutate artifacts Packet F owns. `git checkout .` is **banned outright** from every row; restores are `git checkout -- <named path>`. **This was the right call for a reason beyond tidiness:** a `W` row abandoned mid-flight leaves a modified JS test in a worktree whose next commit is *expected* to move the inventory — the one circumstance in which a stray `static/js` diff is least likely to be caught, and its cost is a two-week T0 restart |
| **B2** | **Step ordering leaves the tree-clean and suite-unchanged gates BEFORE the only steps that dirty the tree.** §13.10 runs the "13 files / 231 cases" gate at step 8 and the mutation matrix at step 11, with nothing after it | `test-strategist` | **ACCEPTED IN FULL.** Steps **11a–11c** are added after the matrix and are blocking: `git status --porcelain` empty; `--check` green; `npx vitest run` = 13 files / 231 tests, exit 0. A non-empty `git status` at 11a is a **stop condition, not a cleanup task.** This is the gate that actually protects §13.0's window, and it was being taken at the wrong moment |
| **B3** | **No parser seam.** `collect_vitest()` was specified as one function doing subprocess + validate + relativize + sort + cross-check, while §13.7 correctly forbids the contract test from running a runner. The consequence: the entire validation layer of a **required-gate script** is proved once by hand and pinned by nothing thereafter | `test-strategist` | **ACCEPTED IN FULL — this is the single most valuable finding of the council.** The collector is split into `_vitest_list_argv(path) -> list[str]`, `_run_vitest_list(path)`, and a **pure** `parse_vitest_listing(payload, repo_root)` carrying validation, relativization, sort and both cross-checks. **The precedent is not hypothetical**: [`tests/test_pyright_baseline_diff.py`](../../tests/test_pyright_baseline_diff.py) — the test for **the other** blocking-gate script named in the same QUALITY_GATE row — already does exactly this, including the fake-absolute-root technique that makes F16/F17 platform-independent. §13.7's overlap survey missed it. With the seam, **F9, F13, F16, F17, F18, F19, F20, F21 and F28 all gain permanent, isolating, runner-free killers**, and F18 stops needing its ≥3-run lottery |

---

#### Part 3 — the disposition table

**ACCEPTED (28).** Folded into the plan as revisions; the plan is not re-drafted here, and §13.15 records
the revision list that must be applied before implementation is requested.

| Finding | Raised by | Disposition |
|---|---|---|
| **Markdown emitted but pinned by nothing that survives regeneration** — `--check` compares committed vs regenerated, so a renderer that never emits the Vitest section against a committed `.md` that never contains it is **green forever**. F23 kills a *stale* artifact, not an *under-emitting* renderer | `architecture` | **ACCEPTED.** This is the registration-analogue defect in its exact repository-native form. §13.7's contract test must assert the **committed `.md`** contains the literal `## Vitest test files` heading and the totals row; a new Group-C row covers *"delete the section from `render_markdown()` **and regenerate**"* |
| **F21 and F25 are vacuous by construction** — both name substrate `G` (a copy) but predict killers that read the **real** module or the **committed** artifact | `test-strategist` | **ACCEPTED.** Both get explicit `W` arms on files Packet F owns. **F25 is split** — a row carrying two mutations (key rename *and* `schema_version`) cannot isolate either |
| **F15 is an undeclared equivalent mutant and is literally unrunnable** | `test-strategist` | **ACCEPTED, and verified in Part 1.** Replaced by the single unambiguous mutation *"parse `result.stderr` as the payload"*, predicting `JSONDecodeError` on P11's warning bytes |
| **F11 has no isolating killer and this was not declared** — every measured nonzero-exit scenario (P6/P7/P8) also changes the payload, so the artifact oracle reds in both arms | `test-strategist` | **ACCEPTED.** Declared non-isolating; with B3's seam it becomes directly assertable at the parser boundary. **This is the finding class the launching session cares most about**: four non-isolating rows had been *asserted* clean rather than *derived* |
| **F28 missing** — §13.4 names "a well-formed but short listing" as the real hole and no row exercises it | `test-strategist` | **ACCEPTED.** Added: inject a payload with one file's rows removed, tree unchanged |
| **`CI` unset makes the documented repair path produce a corrupt artifact** — locally an `.only` gives exit 0 and a collapsed listing; the developer follows the tool's own printed instruction, commits it, local `--check` goes green, and ubuntu hard-fails | `architecture` | **ACCEPTED.** `collect_vitest()` sets **`env["CI"] = "true"`** (or passes `--allowOnly=false`) so behavior is a function of the tree alone. **Independently reached by the launching session's own M9.6 measurement** — `--allowOnly` defaults to `!process.env.CI`, confirmed in `--help` — which makes this a two-source finding, not one reviewer's opinion |
| **`config_include` is a hardcoded literal mirroring `vitest.config.js`**, which the packet forbids itself from touching — and it contradicts the generator's own "derive, never type" idiom (`required_functional_specs()` derives the spec list from `ci.yml` *precisely* so it cannot disagree) | `architecture` | **ACCEPTED.** Either derive `include` from `vitest.config.js` or **drop the field and its cross-check**. Committing a literal that claims to record a config it never read is the same class as a hand-maintained count |
| **The pyright baseline diff is omitted from §13.10** — repo-wide, triggered by any `.py`, blocking inside a required context, and re-baselining is an owner decision, not a repair | `test-strategist` | **ACCEPTED.** Added as a step with "zero net-new diagnostics" as the criterion and a stop condition if red |
| **A new coupling: production `static/js` can red a required context** — a module that throws at import breaks collection. RF4 covers only *test* changes | `architecture` | **ACCEPTED, and UPGRADED to measured (S2).** New RF row, folded into **QF6**. It matters because **nothing required covers production JS today** (verified in Part 1), so this is a genuinely new gate, not an increment |
| **M9 staleness** — NT-1/NT-2/NT-8/NT-9 filed as unmeasured when the dossier had measured them | **all three** | **ACCEPTED.** Moved into Part 1 with values; Part 3 reduces to NT-3/NT-4/NT-5/NT-6/NT-7 — and NT-3, NT-5, NT-6 are **also now closed** (below), leaving **NT-4 and NT-7** |
| **RF11 understates NT-2** — the prohibition is a measured hard constraint, not a precaution. Node 24 *is* on the `Run Tests` PATH, so `shutil.which("npx")` **succeeds** and `_npx()` will not raise its helpful error; `npx` with no local vitest may attempt a registry fetch inside a required job | `architecture` + `test-strategist` | **ACCEPTED, with the sharpening kept.** This is the most consequential half of the M9 finding: it removes the affordance for a later session to "measure NT-2 and relax the rule" |
| **No `skipif` on node/npx availability**, and no contract-test path may reach `_npx()` | `test-strategist` | **ACCEPTED** as a third authoring rule in §13.7, citing the repository's own recorded scar |
| **F18 has a deterministic killer the plan does not use** | `test-strategist` | **ACCEPTED.** The sortedness assertion on a `W`-regenerated artifact is the primary killer; the ≥3 repetitions stay as secondary |
| **F4/F5's "anti-vacuity check" is a characterization**, not a demonstration that the check can fail | `test-strategist` | **ACCEPTED.** Given F1's pre-mutation-green form; the "indistinguishable from deletion" line moves to the equivalence column, where it belongs |
| **F10's arms are mode-ambiguous**; the false green exists only in regenerate mode, and the guard's reachability is unproven | `test-strategist` | **ACCEPTED.** Mode stated per arm; the empty case is reached through the parser seam |
| **"Zero declared equivalences" is false** — F4 (observational) and F17 (Linux-only) qualify it | `product-risk` + `test-strategist` | **ACCEPTED.** Restated as *"no row is filed as a true equivalence; two carry conditional equivalence, both declared in advance."* A summary line that a later grep quotes without its table is a known local failure mode |
| **Group B's header contradicts its own `G + W` rows**; **§13.8's "every row names exactly one substrate"** is false for ~7 rows | `architecture` + `test-strategist` | **ACCEPTED.** Both reworded |
| **Two annotations claim a Gate 1 council record that §13's preamble denies** | `product-risk` | **ACCEPTED — and discharged by construction.** The claim was forward-looking when written; **this subsection makes it true.** The preamble is annotated at the end of this subsection rather than rewritten |
| **Four un-annotated "untouched"/"unstarted" sites**, the worst being §11.17's **meta-claim about the annotations themselves** | `product-risk` | **ACCEPTED AND ALREADY APPLIED.** Annotations added at lines 2200, 3337 and 3716; line 2193 was already covered. The meta-claim got the fullest treatment — a sentence whose subject is the annotation record must itself be annotated when the record grows |
| **RF3 undercounts the documents made incomplete** — `.claude/rules/testing.md:15` enumerates the artifact's contents as a four-item list that becomes five, and §5's own five-row table becomes five-of-six | `architecture` + `test-strategist` | **ACCEPTED.** Both added to RF3 and to **QF5** as items (c) and (d). Noted for the owner: *editing* a file under `.claude/rules/` does **not** trip the parametrized surface (add/delete only), so (c) is a real in-packet option |
| **`.claude/**` missing from must-not-touch** — the obvious place someone would "helpfully" add a Vitest line, and add/delete there trips a pinned surface | `architecture` | **ACCEPTED.** Added as a row with that reason |
| **QF5 offers an option that voids the packet's own gate derivation** — option (a) is a sixth file | `product-risk` | **ACCEPTED, with a correction the reviewer did not make.** QF5 now flags the sixth-file consequence — **but** `test-strategist` is right that the gate *set* would not actually change, since `/verify-suite` is already forced. Both facts are stated so the owner is not over-warned |
| **NT-5/NT-6 were answerable without execution** | `product-risk` + `architecture` + `test-strategist` | **ACCEPTED, and MEASURED rather than derived.** See Part 4 — the numbers are larger than any reviewer estimated, and they change **QF3** |
| **Two truncation caps, not one** — `_check()`'s 200 lines *and* `ci.yml`'s `head -c 8000` | `test-strategist` | **ACCEPTED.** Both named in RF7 |
| **Known-red E2E exception omitted from step 10**, and ad-hoc E2E batches are nondeterministic | `test-strategist` | **ACCEPTED.** `e2e/program-backup.spec.ts:79` cited with the isolation re-run as its disposition, plus the standing stash-and-rerun rule before attributing any failure to this diff |
| **Reviewer set under-specified** — `unslop-reviewer` omitted, and roughly half this packet's diff is prose in a document that has already produced three falsified-neighbour cases | `test-strategist` | **ACCEPTED.** `code-reviewer` **+ `unslop-reviewer`** at code time; the council named separately |
| **Generated-file contention is not re-checked before regenerating** | `architecture` | **ACCEPTED.** §13.10 step 4 re-checks `gh pr list` immediately before regenerating. §13.0 already imposes exactly this "never restate from memory" discipline on the T0 ledger |
| **Dossier ID `M5` cited but absent from §13.2's table; "461 lines" wrong; `collector` literal disagrees with the actual argv** | `product-risk` + `test-strategist` | **ACCEPTED.** M5 row added; **469** corrected; the `collector` value must match the command actually run |

**ACCEPTED WITH AMENDMENT (2).**

| Finding | Disposition |
|---|---|
| **`test-strategist`: F3 (rename) is only PARTIAL — conditional on QF3.** If the owner rules "counts only", the rename shape becomes **NOT COVERED** and F3 becomes a true equivalence | **ACCEPTED, and escalated.** The reviewer is right that a required drift shape is currently hostage to an unruled question. **Amendment:** this is no longer presented as a balanced choice. **QF3 now carries a recommendation the packet will not soften** — rule "include", or accept on the record that the most common JS-test edit there is becomes invisible to the gate |
| **`architecture`: the `ci.yml` failure annotation will mis-diagnose the new failure class** and §13.1 forbids fixing it | **ACCEPTED as the constraint; AMENDED on the remedy.** No workflow edit. **Instead, `collect_vitest()`'s `SystemExit` messages must open with a line that visibly contradicts the annotation** — e.g. `COLLECTION FAILURE — this is not drift; do not regenerate.` This puts the correction in the file Packet F owns |

**NOTED, NOT ACTIONED (3).**

| Finding | Why not actioned |
|---|---|
| **`test-strategist`: `describe.each` (NT-7) has no row** | **Genuine gap, recorded not closed.** No JS test uses `describe.each` today, so a row would exercise a shape the suite does not contain. Recorded in §13.11 so it is added the day one appears |
| **`architecture` + `test-strategist`: plan-stage size is never derived; both read it as Large (Gate 0 + council), while QF1 requests Gate 1 only** | **ROUTED TO THE OWNER as QF9**, not decided. Both reviewers concede "schema" in that table plainly means the DB/API surface, not a generated doc artifact — and this session's authorization is explicitly *"Packet F scoped planning … and Gate 1 council review"*. **Deciding it either way would be the packet grading its own gate**, so it is asked instead |
| **`test-strategist`: §13.7's naming rejection is refuted by its closest precedent** (`tests/test_pyright_baseline_diff.py` names the script) | **The name stands; the RATIONALE is replaced.** `tests/test_vitest_inventory_contracts.py` is kept, rested on scope rather than on a rule the sibling script disproves |

**DISAGREEMENT — one, settled by routing rather than by the packet (1).**

`architecture` **disputes the packet's QF2 recommendation.** The plan recommends bumping
`schema_version` to `2`; `architecture` would **leave it at `1`** and argues the remedy for "asserts
nothing" is to assert the **top-level key set** — `set(inventory) == {…, "vitest"}` — which catches both
the rename F25 mutates and the deletion F24 removes, **in one assertion that never needs editing for an
additive change**, whereas a pinned `schema_version == 2` catches neither.

**The launching session's assessment: `architecture` has the better argument on the mechanism, and its
key-set assertion is adopted regardless of how QF2 is ruled** — it is strictly stronger than what §13.7
listed and costs nothing. It also raises a placement problem the packet had not seen: `schema_version`
is a **whole-artifact** field, and pinning it inside a file deliberately named for the Vitest surface
means a future sixth surface bumping to `3` reds a Vitest-named test, whose tempting repair is to edit
the number.

**QF2 is therefore re-put to the owner with the packet's recommendation WEAKENED from "increment to 2"
to "no recommendation", the two arguments stated side by side, and the key-set assertion adopted either
way.** The packet does not get to settle a question it raised and then lost the argument on.

---

#### Part 4 — measurements taken at council time that change an owner question

**NT-5 and NT-6 are now measured, and they are larger than the reviewers' estimates.**

The proposed `vitest` block was built in memory from the real listing and serialized with the
generator's own `json.dumps(indent=2, sort_keys=True)` shape. **Nothing was written into the repository.**

| Quantity | Measured |
|---|---|
| `vitest` block **with** the full 231-row `cases[]` | **988 lines / 45,741 bytes** |
| Current `TEST_INVENTORY.json` | **758 lines / 18,507 bytes** |
| Projected `TEST_INVENTORY.json` after Packet F | **≈1,740 lines / ≈64 KB** |
| The counts-only alternative | **13 rows, ≈55 lines** |

**This changes QF3 materially.** The `cases[]` array alone is **larger than the entire current
artifact**: the identity list roughly **triples the JSON by bytes** and grows it **2.3× by lines**. The
whole cost of detecting a **rename** is about **930 committed lines**. The owner should rule QF3 with
those numbers in hand, not with "NT-5, unmeasured".

**NT-6 resolves as: yes, it truncates — twice, and harmlessly.** A ~988-line first-landing diff against
`_check()`'s 200-line cap truncates ~5×, and `ci.yml`'s `head -c 8000` truncates again. **The gate still
reds correctly** — truncation affects only what the operator sees. `architecture` adds the reassuring
half: `sort_keys=True` places `vitest` **last** alphabetically, so its hunk cannot crowd out the other
four surfaces' diffs, and `_check()` is called once per file so JSON and Markdown each get their own
200 lines. **§13.10 step 2's pass criterion is therefore "reports `DRIFT` and exits 1", never "shows the
complete diff".**

**NT-3 is closed.** Every `process.env.*` read in `node_modules/vitest/dist/**` was enumerated: there is
**no Vitest analogue of `PLAYWRIGHT_JSON_OUTPUT_NAME`**. The defensive `env.pop()` §13.4 left as an open
instruction **has no counterpart to perform**, and no speculative pop should be added. Two variables do
matter — `CI` (the `--allowOnly` default, the subject of the accepted finding above) and
`GITHUB_ACTIONS` (reporter selection, irrelevant under the file channel).

**Remaining unmeasured after the council: NT-4** (Linux behavior — every probe was win32; the first
ubuntu `test-inventory` run is the measurement) and **NT-7** (`describe.each`).

---

#### Part 5 — what the council did NOT dislodge

Recorded because a later reader should know which parts survived three adversarial passes:

- **§13.3's rejection of `vitest run --reporter=json`.** All three reviewers examined it; `architecture`
  probed hardest and narrowed the claim (S2's indirect path) **without reversing the decision**, calling
  it *"the strongest thing in the section"*. Framing it as a **stop-condition** rather than a trade-off
  is correct and **should not be revisited.**
- **§13.4's order of operations** — exit-code check before parse, before file-existence, before shape
  validation — is the right reading of P7 against P8.
- **The mandatory sort (P3) and `relative_to().as_posix()` (P14)** as load-bearing rather than stylistic.
- **M3's consumer inventory**, re-derived independently by `architecture` over a wider file set plus
  `.claude/**` and `docs/**`: the only code consumers are `ci.yml`'s exit-code check and its named-key
  indexing, which never enumerates. **A new top-level key breaks no consumer.**
- **`Test Inventory Drift` is required (context #11 of 12), so no branch-protection edit is needed** —
  §2.5's whole design holds.
- **§13.0's ledger is honest** — one green result, zero red, zero missing, zero cancelled, zero runs
  after T0, and it claims **no** elapsed window progress.
- **§7 was not quietly fixed.** All three confirmed §7.1 still records 11 contexts and §7.2 still says
  "12th", with the drift routed to the owner rather than edited. Same for `QUALITY_GATE.md`'s
  five-surface table.
- **No calculation-surface, non-goal, or local-first violation**, checked rather than assumed: no
  `routes/`, `utils/`, `app.py`, or template; no Effective/Raw surface; no `CountingMode` /
  `ContributionMode`; the parked fatigue workstream is not resumed.
- **F27's disclosure as a detection hole rather than an equivalence** is the honest call and
  **should not be "fixed" by inventing a killer.**

---

#### Part 6 — annotation of §13's own preamble

> ⚠️ **ANNOTATION — §13's preamble (the "Council status" paragraph) is now superseded and is annotated,
> not rewritten.** It states *"No Gate 1 council record for Packet F exists in this document"* and that
> the "PLAN v2" label *"describes the drafting round, not a reviewed-and-dispositioned round."* **Both
> were true when written and are now false: this subsection is that record.** The label is earned.
> **What has NOT changed: Gate 1 is still NOT APPROVED.** A council record is the input to the owner's
> ruling, not the ruling. §13.15's revisions must be applied and the nine questions in §13.12 answered
> before implementation may be requested.

### 13.15 Revisions required before implementation may be requested

**§13.1–§13.13 are the plan as DRAFTED. §13.14 is the council. This subsection is the binding
difference between them.** It is written as a checklist rather than folded into the prose above, for
the reason §13's preamble already gives: **a drafted section that is silently rewritten to match its
review loses the evidence of what the review changed.** The sections above are left as the drafting
round; **where they and this subsection disagree, this subsection wins.**

**None of these has been applied to any code. All are plan-text revisions plus design commitments that
bind the implementation if and when it is authorized.**

#### Blocking — the plan is not implementable until these are applied

| # | Revision | Source |
|---|---|---|
| **R1** | **Delete the `W` arms from F1–F5.** Those rows run on **`T` only**. F22/F24 carry the committed-pin claim. **`git checkout .` is banned from every row** — restores are `git checkout -- <named path>`, never repo-wide, never after a `git mv`. §13.8's preamble sentence *"no row runs against the real JS suite"* becomes true | B1 |
| **R2** | **Correct the `T` substrate location.** `T` lives under the **gitignored `artifacts/`**, not the OS temp directory — measured (S1): a fixture in the temp dir cannot resolve `vitest` (`ERR_MODULE_NOT_FOUND`). §13.4's temp-file decision for the collector's `--json=<path>` **output** is unaffected and stands | S1 |
| **R3** | **Add steps 11a–11c after the mutation matrix**, blocking: `git status --porcelain` empty; `--check` green; `npx vitest run` = 13 files / 231 tests, exit 0. **A non-empty `git status` at 11a is a stop condition, not a cleanup task** | B2 |
| **R4** | **Split the collector at a parser seam**: `_vitest_list_argv(path)`, `_run_vitest_list(path)`, and a **pure** `parse_vitest_listing(payload, repo_root)` holding validation, relativization, sort and both cross-checks. Model it on [`tests/test_pyright_baseline_diff.py`](../../tests/test_pyright_baseline_diff.py), including its **fake absolute root** technique, which makes F16/F17 platform-independent | B3 |

#### Design commitments — settled by the council, binding on implementation

| # | Revision | Source |
|---|---|---|
| **R5** | **`collect_vitest()` sets `env["CI"] = "true"`** (or passes `--allowOnly=false`) so a stray `.only` fails closed **identically on Windows and ubuntu**. Without it, the repair path the tooling itself prints produces a corrupt artifact | AR4 + M9.6 |
| **R6** | **Resolve `config_include`**: derive `include` from `vitest.config.js`, or **drop the field and its path-prefix cross-check**. Do not commit a literal claiming to record a config it never read | AR5 |
| **R7** | **Pin the Markdown surface in the contract test** — assert the **committed** `.md` contains the literal `## Vitest test files` heading and the totals row. Add a Group-C row for *"delete the section from `render_markdown()` **and regenerate**"*. `--check` alone cannot see an under-emitting renderer | AR2 |
| **R8** | **Adopt the top-level key-set assertion** — `set(inventory) == {"schema_version","generator","playwright","pytest","hard_waits","vitest"}` — **regardless of how QF2 is ruled.** It is strictly stronger than the drafted list and catches both F24's deletion and F25's rename in one assertion | AR disagreement |
| **R9** | **`collect_vitest()`'s `SystemExit` messages open with a line that contradicts the workflow's fixed annotation** — e.g. `COLLECTION FAILURE — this is not drift; do not regenerate.` **No workflow edit** | AR7 |
| **R10** | **Third authoring rule in §13.7**: no `skipif` on node/npx availability, and **no contract-test path may reach `_npx()`**. Node *is* on the `Run Tests` PATH, so `shutil.which("npx")` succeeds and `_npx()` will **not** raise its helpful error — a shelling test would attempt a registry fetch inside a required job rather than failing fast | TS20 + AR6 |

#### Mutation-matrix repairs

| # | Revision | Source |
|---|---|---|
| **R11** | **F21 and F25 get `W` arms** (real generator, real regeneration, real contract test, restore by named-path checkout). **F25 splits in two** — key rename and `schema_version` are separate mutations | TS5 |
| **R12** | **F15 is replaced** by *"parse `result.stderr` as the payload"*, predicting `JSONDecodeError` on P11's warning bytes. The `stderr=STDOUT` form is **unrunnable** (`ValueError`, verified) | TS6 |
| **R13** | **Add F28** — inject a payload with one file's rows removed, tree unchanged. This is the one hole §13.4 names and no row exercised | TS9 |
| **R14** | **Declare F11 non-isolating**, and judge it at the parser seam rather than by the artifact oracle | TS7 |
| **R15** | **F18's primary killer becomes the sortedness assertion** on a `W`-regenerated artifact; the ≥3 repetitions stay secondary | TS11 |
| **R16** | **F4/F5 get F1's pre-mutation-green anti-vacuity form**; "indistinguishable from deletion" moves to the equivalence column | TS12 |
| **R17** | **F10's mode is stated per arm**; the empty case is reached through the parser seam, not the runner | TS10 |
| **R18** | **Correct two false summary lines**: "Zero declared equivalences" → *"no true equivalence; two conditional, both declared"*; and "every row names exactly one substrate" / Group B's "every row mutates a copy", both false for ~7 rows | PR5 + TS6 + TS17 + AR13 |

#### Gate-set and evidence repairs

| # | Revision | Source |
|---|---|---|
| **R19** | **Add the pyright baseline diff** to §13.10 — repo-wide, blocking inside a required context, "zero net-new diagnostics", stop condition if red. Re-baselining is an owner decision, not a repair | TS3 |
| **R20** | **Reviewers: `code-reviewer` + `unslop-reviewer`** at code time, council named separately. Roughly half this diff is prose in a document that has already produced three falsified-neighbour cases | TS13 |
| **R21** | **Cite the known-red** `e2e/program-backup.spec.ts:79` in step 10 with the isolation re-run as its disposition, plus the standing rule that an ad-hoc E2E batch is nondeterministic — stash and re-run the identical batch before blaming the diff | TS14 |
| **R22** | **Re-check `gh pr list` immediately before step 4's regeneration.** §13.0 already imposes this "never restate from memory" discipline on the T0 ledger | AR12 |
| **R23** | **Move NT-1/NT-2/NT-8/NT-9 into §13.2 Part 1 with their values**; close **NT-3, NT-5, NT-6**; Part 3 reduces to **NT-4 and NT-7**. Restate **RF11** as a measured constraint. Put `2809 / 124 / 125` into step 0 with a mismatch as a stop condition | all three |
| **R24** | **Add the S2 coupling as an RF row and fold it into QF6** — a production `static/js` change that breaks module-scope evaluation reds a required context, and **nothing required covers production JS today** | AR3 + S2 |
| **R25** | **Extend RF3/QF5** to four documents: `QUALITY_GATE.md`, §7.1 of this file, **`.claude/rules/testing.md:15`**, and **§5's five-row table**. Note that *editing* under `.claude/rules/` does not trip the parametrized surface | AR9 + TS15 + PR9 |
| **R26** | **Add `.claude/**` to must-not-touch**, citing the parametrized-configuration surface | AR9 |
| **R27** | **Correct 461 → 469 lines**; add the missing **M5** row; make the `collector` literal match the argv actually run; flag QF5(a)'s sixth-file consequence **while noting the gate set would not actually change** | PR8 + TS18 + AR13 + PR6 |
| **R28** | **QF3 carries the measured cost** (988 lines / 45.7 KB; ≈3× the current JSON) and an unsoftened recommendation to include. **QF2's recommendation is withdrawn to neutral** with both arguments side by side | Part 4 + AR disagreement |
| **R29** | **Add QF9 — plan-stage size.** Two reviewers read Packet F as **Large** (Gate 0 + council), while QF1 requests Gate 1 only. Routed, not decided: the packet may not grade its own gate | AR11 + TS13 |

---

**Nothing in §13.15 has been implemented.** No generator change, no artifact, no test file, no mutation
run. The revisions bind the implementation **if and when the owner authorizes it**; they are recorded
here so that authorization is given against the reviewed plan rather than the drafted one.

> ⚠️ **ANNOTATION 2026-08-22 — the paragraph above is SUPERSEDED and is annotated, not rewritten.**
> The owner authorized implementation at **§13.16**, and **all of R1–R29 have been applied**. The
> per-revision discharge table is **§13.17**. The sentence stands as the record of what was true
> when the revisions were written.

### 13.16 Owner ruling at Gate 0 and Gate 1 (2026-08-22) — **APPROVED, WITH NINE RULINGS AND ONE DESIGN RULING**

**Both gates are now signed, and the §13.13 STOP is discharged for implementation only.** The owner
classified Packet F as **Large / new workflow** under
[`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)'s plan-stage routing — which settles **QF9**,
the one question §13.14 Part 3 explicitly refused to decide on the packet's own behalf — and ruled
that **Gate 0 is required and approved by the ruling itself**, with the completed three-reviewer
council (§13.14) satisfying the council half after its **29 revisions** are applied.

**Gate 1 is approved against §13.1–§13.13 as the drafting record, §13.14 as the council, all of
R1–R29 in §13.15, and the rulings below.** Where the drafted plan and §13.15 or these rulings
disagree, **§13.15 and these rulings govern** — the same precedence §13.15 already declared for
itself. **A second council is not required** if the revisions are applied faithfully; the standing
instruction is to **stop and return to Gate 1** if implementation changes the approved schema shape,
collection mechanism, owned files, T0 premise or required-gate behavior. *(It did not: §13.17 records
five deviations, all of them below that line, each stated rather than folded in.)*

#### The twelve Gate 0 requirements, as approved

Restated because they are the acceptance criteria §13.17 is judged against, and because a
requirement list that lives only in a prompt is a requirement list nothing can be checked against
later:

| # | Requirement |
|---|---|
| 1 | Extend the required Test Inventory Drift gate to inventory Vitest **without executing the JS tests** as its collection mechanism |
| 2 | Use `vitest list --json=<path>` and the **file** output channel — not stdout, not `vitest run --reporter=json` |
| 3 | Remain deterministic across Windows and Linux through **explicit sorting** and **POSIX-relative paths** |
| 4 | Fail closed on runner failure, missing output, malformed output, empty output, duplicates, path escape and partial listings |
| 5 | Keep subprocess execution separate from a **pure parser seam** |
| 6 | Required pytest contract tests must never invoke `npx`, depend on `node_modules`, skip themselves when Node is unavailable, or attempt network access |
| 7 | Pin per-file counts and full stable case identities strongly enough to detect **file deletion, case deletion and case rename** |
| 8 | Change **no** JavaScript test, production JavaScript, workflow, dependency, Vitest configuration, branch protection or repository setting |
| 9 | Preserve the **13-file / 231-case** JS suite byte-for-byte, and therefore preserve **T0** |
| 10 | Keep the existing required `Test Inventory Drift` context as the enforcement mechanism; **add no new context** |
| 11 | Provide mutation evidence, deterministic regeneration evidence, full verification and code-time review |
| 12 | Update the live documentation surfaces made inaccurate by Packet F |

**These may not be widened without a new owner ruling.**

#### Rulings QF1–QF9

| # | Question | Ruling |
|---|---|---|
| **QF1** | Proceed past Gate 1? | **YES.** Local implementation, **mutation execution under the approved containment rules**, commit, push, and a **ready-for-review** PR titled `test(inventory): Packet F — pin Vitest nodes` are each authorized. **Merge is NOT authorized** and remains a separate confirmation naming the PR |
| **QF2** | `schema_version` | **Increment `1` → `2`.** Adding the required `vitest` top-level surface is a material artifact-schema revision even though it is backward-compatible for current consumers. **R8's exact top-level key-set assertion is adopted as well — the version assertion does not replace it.** Schema-version coverage stays in the **general artifact-contract** portion of the test, so a future surface change is not misleadingly treated as Vitest-only behavior. *(This resolves §13.14's disagreement by taking both halves: `architecture` won the argument that the key-set assertion is the stronger mechanism, and it is adopted; the bump is ruled in on its own grounds.)* |
| **QF3** | Full identity list, or counts only? | **Include the complete sorted identity list.** The measured cost — **≈988 lines / 45.7 KB for 231 identities** — **is accepted**: detecting a rename is worth that committed size. **Counts-only is rejected** because it leaves case renames invisible. **Do not render the identities into Markdown** — the `.md` carries the summary and per-file counts and points at the JSON |
| **QF4** | P4's skip/todo limitation | **Accepted.** `vitest list` omits `.skip` and `.todo`, so the inventory **honestly cannot** distinguish either from deletion. Detection still occurs because the identity disappears. **Do not add a `status` field and do not claim status visibility. Do not switch to `vitest run`** — that would couple a required context to JS test outcomes before D2 |
| **QF5** | The documents Packet F makes incomplete | **All four are handled in Packet F** rather than knowingly landing stale live guidance: (a) live `QUALITY_GATE.md` five → **six** pinned surfaces, with the Vitest surface described accurately; (b) live `.claude/rules/testing.md` inventory description includes Vitest; (c) §7.1/§7.2 **annotated** with the current 12-context state and the eventual promotion being a **13th**; (d) §5 **annotated** for the sixth surface. **Preserve dated historical statements through annotations; update current live rules directly.** **Do not edit** `MASTER_HANDOVER.md`, `ACTIVE_DEVELOPMENT.md`, `TESTING_STRATEGY_PLANNING.md` or `UI_SCENARIOS_GAP_ANALYSIS.md` in this packet |
| **QF6** | The new coupling | **Accepted, and must be documented plainly:** a future Vitest bump changing `list --json`'s shape can red the required inventory gate, and **production JS throwing during module-scope collection can also red it** (§13.14's S2). Both are **deliberate fail-closed outcomes**. Collection-failure messages must open with wording such as `COLLECTION FAILURE — this is not drift; do not regenerate.` **Do not weaken validation or edit the workflow annotation to conceal the coupling** |
| **QF7** | A structural guard against a vacuous contract test | **No.** Do not add a source-text meta-test or a literal-count meta-test. **F27 is recorded as an accepted detection hole common to contract tests** — a deliberately tautological assertion may survive. The controls are F26's reverse direction, the pure-parser tests, the exact artifact assertions, the mutation evidence, `code-reviewer` and `unslop-reviewer`. **Do not claim this generic residual is eliminated** |
| **QF8** | T0 | **Confirmed.** Packet F may land inside the qualification window and **does not restart T0**, provided no file under `static/js/**` changes, the suite remains exactly 13 files / 231 cases, and no skipped, todo, filtered or `.only` state appears. **T0 remains `2026-08-22T17:59:26Z`; the strict mark remains `2026-09-05T17:59:26Z`.** **Q4, Q6 and D2 remain unauthorized** |
| **QF9** | Plan-stage size | **Large / new workflow.** Gate 0 required and approved; the completed council satisfies the council review after R1–R29 are applied |

#### The additional design ruling — `config_include`

**Drop `config_include` from the artifact** rather than parsing or duplicating `vitest.config.js`.
**The actual successful listing is the source of truth**, and a hand-maintained copy of a
configuration the generator never reads is the class of defect §13.14-AR5 raised. This takes the
**second** of R6's two options; the path-prefix cross-check that belonged to the field goes with it,
and the repo-relative-POSIX assertions that kill F16 and F17 move to the contract test, where
§13.14-B3's fake-root technique makes them platform-independent.

#### Authorized tracked files — **seven, and a stop condition at eight**

1. [`scripts/generate_test_inventory.py`](../../scripts/generate_test_inventory.py)
2. [`tests/test_vitest_inventory_contracts.py`](../../tests/test_vitest_inventory_contracts.py)
3. [`docs/test_inventory/TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json)
4. [`docs/test_inventory/TEST_INVENTORY.md`](../test_inventory/TEST_INVENTORY.md)
5. `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` (this file)
6. [`docs/ai_workflow/QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)
7. [`.claude/rules/testing.md`](../../.claude/rules/testing.md)

**Any need for another tracked path is a stop condition requiring owner approval.** Note that the
drafted §13.1 said **five** files and called a sixth a gate-re-derivation trigger; the ruling raises
the ceiling to **seven** by moving QF5(a) and QF5(b) in-scope. §13.14 Part 3 already recorded the
resolution of that tension: `/verify-suite` is forced by the **Tooling / scripts** row regardless, so
the **gate set does not change** — only the file count does. `.claude/rules/testing.md` is **edited,
never added or deleted**, so the parametrized configuration surface is not tripped.

#### What is still forbidden

Unchanged from §13.13 and restated because approval of implementation is not approval of anything
adjacent to it: **merging this PR**, **Q4**, **Q6**, **D2**, any branch-protection or
repository-settings change, any edit to `.github/workflows/**`, `scripts/release_gate.py`,
`package.json`, `package-lock.json`, `vitest.config.js`, `static/js/**`, any existing test, or
`.claude/settings.json`. **A permission failure during execution remains a blocker to report, not
authority to change configuration.**

### 13.17 Execution record — 2026-08-22

**Packet F is implemented.** Base `origin/main` **`9cb6cdc`**, worktree
`D:\development\Hypertrophy-Toolbox-v3-main-phase3-packet-f-inventory`, branch
`wt/phase3-packet-f-inventory`, with `npm ci` run **inside** the worktree (vitest **4.1.11**,
lockfile-matching — RF6's hazard avoided rather than merely noted).

**Everything below is MEASURED.** Where a §13.8 prediction and an observed result disagree, the
disagreement is recorded and investigated under §10.7-R9, never edited away — **three did**, and each
one is written up in full at the end of this subsection. **Two of the three turned out to be defects
in this packet's own work, not in the plan**, which is the outcome that rule exists to produce.

#### Part 1 — the gates, measured

| # | Gate | Result |
|---|---|---|
| **0a** | JS suite **before** | **13 files / 231 tests, exit 0** — matches M4 |
| **0b** | pytest inventory baseline (**NT-1**, taken here) | `collected_deterministic` **2809** / `deterministic_files` **124** / `total_files` **125** — the values R23 required in step 0, confirmed rather than assumed |
| **0c** | Baseline `--check` | `Test inventory is up to date.`, **exit 0** |
| **2** | **Deliberate red** — generator extended, artifacts stale | **exit 1.** **Both** surfaces reported independently: `DRIFT: docs/test_inventory/TEST_INVENTORY.json` **and** `DRIFT: docs/test_inventory/TEST_INVENTORY.md`. **This is the packet's own anti-vacuity check** — a green here would have meant the new surface was not pinned at all. **NT-6 closes as predicted:** the JSON hunk truncated at `_check()`'s 200-line cap and the gate still red correctly |
| **4** | Regeneration | JSON **757 → 1746** lines (**63,545** bytes LF); Markdown **215 → 239** lines. **NT-5 closes at 985 lines / 45,697 bytes** for the `vitest` block as it sits in the artifact (lines 761–1745), of which **926 lines** are `cases[]` alone; the file itself grew by **989** lines. The council projected 988/45,741 for a standalone dump of the same block — **3 lines out, and the difference is the two wrapping braces a standalone dump adds**, not a measurement error in either |
| **5** | Focused contracts | **46 passed**, exit 0 |
| **6** | `--check` green again | `Test inventory is up to date.`, exit 0 |
| **7** | **Determinism** | **Three** consecutive regenerations, byte-identical: JSON `0b8a8fb4f937e806316f6e78a9a9f8cb`, Markdown `2aee5cca02eca10ffb0e7275c6651c24`. Re-run on the **final** generator, not only the first draft |
| **8** | **JS suite after** | **13 files / 231 tests, exit 0** — byte-identical to step 0. **§13.0's window is intact and T0 is not restarted** |
| **9** | **Full pytest** | **3175 passed, 2 skipped**, exit 0, 221.1s. Delta is **exactly 46** — the new file's own nodes and nothing else (3131 baseline = 2809 deterministic + 322 from the one env-dependent file on a Windows host) |
| **9b** | **Pyright baseline diff (R19)** | **PASS — 0 net-new diagnostics** (baseline 132, current 132). Nothing re-baselined |
| **10** | **Chromium E2E** | **649 / 649 pass, in two invocations.** See the E2E note below — it corrects a standing repository belief |
| **11** | **Mutation matrix** | **58 recorded arms, 0 disagreements** on the final run — 52 mutation arms, 1 pre-mutation baseline, 5 containment gates. Part 4 |
| **11a–c** (R3) | **Post-matrix containment** | `git status --porcelain` **empty**; `--check` **green**; JS suite **13 / 231**; and all **seven** tracked blob hashes **identical** to the checkpoint |

**The E2E result, stated precisely, because the naive reading is wrong.**

`npx playwright test --project=chromium` — the command `CLAUDE.md` and the `/run-e2e` skill both
document — returned **569 passed, 63 failed, 17 did not run**. All 63 failures were in
`visual.spec.ts` (52), `workout-plan-desktop-contract.spec.ts` (10) and
`visual-baseline-thumbnails.spec.ts` (1), and the first failure is **behavioural, not visual**:
`expect(rowCount).toBeGreaterThanOrEqual(4)` received **1**. That is a **seeding** fact — without
`PW_VISUAL_SEED=1` the throwaway DB is built by `prepare_e2e_db.py`, which wipes the user state those
specs need.

| Batch | Result |
|---|---|
| The **549** non-visual tests, functional seed | **549 passed**, exit 0 |
| The **100** visual tests, `PW_VISUAL_SEED=1` | **100 passed**, exit 0 |

**A standing belief is corrected here, on measurement.** The repository's working assumption has been
that the visual specs are *excluded* from a default local run and that a default run should therefore
show zero failures. **They are not excluded**: `playwright.config.ts` has no `testIgnore`, no
`grepInvert`, and neither spec carries a self-skip — `PW_VISUAL_SEED` selects only the **seed script**.
The full local suite needs **two** invocations, and "judge a default local run by zero failures" is
not a criterion that can ever be met. **`e2e/program-backup.spec.ts:79` — the known-red R21 names —
did not fire in either batch.**

**Attribution, since the rule is to stash-and-rerun before blaming a diff:** the seeded re-run passing
100/100 on the *same* working tree settles it, and the diff contains **no** file any browser or Flask
process can observe — no `e2e/`, `static/`, `templates/`, `routes/`, `utils/`, `app.py`.

#### Part 2 — the twelve Gate 0 requirements

| # | Requirement | Discharged by |
|---|---|---|
| 1 | Inventory Vitest without executing the JS tests | `vitest list`; **F21/F21-W** assert the argv can never become `vitest run` |
| 2 | `--json=<path>`, file channel | `_vitest_list_argv()`; **F14** proves the stdout channel fails on a contaminated tree where the file channel succeeds |
| 3 | Deterministic across Windows and Linux | mandatory `identities.sort()` + `relative_to().as_posix()`; three byte-identical regenerations; **F16/F17/F18** |
| 4 | Fail closed on runner failure, missing output, malformed output, empty output, duplicates, path escape, partial listings | Six of the seven are hard `SystemExit`s with **F10, F12, F13, F19, F9** and two path tests as killers. **The seventh is honest:** a well-formed but SHORT listing is internally consistent and **no payload check can see it** — **F28** demonstrates the parser accepting one. The oracle is the committed identity list, which is the strongest argument for QF3's ruling |
| 5 | Subprocess separate from a pure parser seam | `_vitest_list_argv` / `_run_vitest_list` / `parse_vitest_listing`; **17 of the 43 test functions** (46 collected nodes) exercise the pure parser |
| 6 | No `npx`, no `node_modules`, no self-skip, no network in the required pytest tests | `_vitest_list_argv(path, npx="npx")` takes the executable as a defaulted parameter, so **no test path reaches `_npx()`**; the file has **zero** `skipif` and **zero** subprocess calls |
| 7 | Detect file deletion, case deletion, case rename | **F1**, **F2**, **F3**. F3 is the one that matters: **counts are byte-identical under a rename** and only `cases[]` moves |
| 8 | No JS, production, workflow, dependency, config, protection or settings change | `git diff --stat` is **seven files**, listed in Part 6 |
| 9 | 13 files / 231 cases preserved; T0 preserved | measured before, after implementation, and again after the entire mutation matrix |
| 10 | No new required context | branch protection untouched; the surface lands inside the already-required `Test Inventory Drift` |
| 11 | Mutation, determinism, verification and review evidence | Parts 1, 4, 5 |
| 12 | Update the live documentation surfaces | Part 6 |

#### Part 3 — how R1–R29 were discharged

| # | Discharge |
|---|---|
| **R1** | F1–F5 ran on **`T` only**. No `W` arm exists for them, and **`git checkout .` appears nowhere** — every restore is `git checkout -- <named path>`, and `restore()` raises `CONTAINMENT FAILURE` if the tree is not clean afterwards. It fired once, correctly (Finding 3) |
| **R2** | `T` lives at `artifacts/packetf-fixture/` (gitignored), where `vitest` resolves by walking up. Collector output still goes to `tempfile.mkdtemp()` |
| **R3** | Steps 11a–11c run and pass; the hash comparison against the checkpoint was added on top |
| **R4** | The three-function seam exists, modelled on `tests/test_pyright_baseline_diff.py` including its **fake absolute root** (`Path("/repo").resolve()`), which is what makes F16/F17 assertable on either platform |
| **R5** | `_run_vitest_list()` sets `env["CI"] = "true"`. **F6 mutates that pin directly** and shows the corrupt-artifact path it prevents |
| **R6** | **`config_include` dropped** (owner's design ruling), and the include-derived cross-check with it. The path assertions moved to the contract test, where they have a fake root and no config to duplicate |
| **R7** | Four contract tests read the **committed** `.md`. **F29** — the council's addition — proves they are the only oracle: an under-emitting renderer plus a regeneration leaves `--check` **green** |
| **R8** | `test_top_level_key_set_is_exact` adopted. **F24 and F25a** both die on it |
| **R9** | Every `SystemExit` on the collection path opens with `COLLECTION FAILURE - this is not drift; do not regenerate.` No workflow edit |
| **R10** | Third authoring rule written into the module docstring; the `npx` parameter makes it structural rather than a promise |
| **R11** | F21 gained its `W` arm; **F25 split** into F25a (key name) and F25b (`schema_version`). Both were **repaired further at execution** — see Finding 4 |
| **R12** | F15 is *"parse `result.stderr` as the payload"*; it dies on a **clean** tree, on P11's warning bytes |
| **R13** | **F28 added** |
| **R14** | **F11 declared non-isolating** and judged at the seam |
| **R15** | F18's primary killer is the sortedness assertion; the ≥3 live repetitions are secondary and produced **2 distinct orderings in 3 runs** — flaky by construction, as declared |
| **R16** | F4/F5 carry F1's pre-mutation-green form (row **F0**); "indistinguishable from deletion" is stated as the equivalence it is |
| **R17** | F10's arms are mode-explicit and the empty case is reached **through the parser seam**, not the runner |
| **R18** | Corrected in this record: **no row is a true equivalence; two are conditional** — F4/F5 (observational, vs deletion) and F17 (Linux-only) |
| **R19** | Pyright baseline diff run: **0 net-new** |
| **R20** | `code-reviewer` **and** `unslop-reviewer`, Part 5 |
| **R21** | Known-red cited and checked: it did not fire. The E2E note above goes further and corrects the criterion itself |
| **R22** | `gh pr list` re-checked immediately before **each** regeneration: **0 open PRs** both times |
| **R23** | NT-1 taken (**2809 / 124 / 125**) and matched. **NT-3, NT-5, NT-6 closed**; **NT-4** closes on the PR's ubuntu run |
| **R24** | Folded into QF6 and into the live `QUALITY_GATE.md` row, which now names **`static/js/**/*.js`** as a tripping path |
| **R25** | All four surfaces handled — QF5 moved (a) and (b) in-scope and (c)/(d) are annotated |
| **R26** | `.claude/**` add/delete remains off-limits; `.claude/rules/testing.md` was **edited in place**, which does not trip the parametrized surface. `--check` green after the edit confirms it |
| **R27** | The `collector` literal is `VITEST_COLLECTOR`, pinned equal to the argv shape by `test_collector_string_matches_the_argv_actually_run`. The seven-file ceiling and the unchanged gate set are recorded at §13.16 |
| **R28** | QF3 ruled with the measured cost in hand. The block occupies **985** lines of the artifact |
| **R29** | QF9 answered by the owner: **Large / new workflow** |

#### Part 4 — the mutation matrix, measured

**58 recorded arms across 30 rows — 52 of them mutation arms. Final run: 0 disagreements.** Every row proved application (an exact-match
patcher raises **`NOT APPLIED`** rather than counting a silent no-op as a survivor), expected
behaviour, and restoration. **No row touched `static/js/**`, any pre-existing test, or any file
outside the seven authorized paths.**

**Group A — the JS test surface (substrate `T`, a 3-file / 6-case fixture under `artifacts/`).**

| Row | Measured |
|---|---|
| **F0** | Pre-mutation: 3 files / 6 cases, sorted. The anti-vacuity floor for every row below |
| **F1** | Delete a file → 2 files / 5 cases, its identities gone |
| **F2** | Delete one case → 3 files / **5** cases, `alpha > b` gone by name |
| **F3** | **Rename** one case → **counts byte-identical**, identity list moved. **This row is the entire argument for QF3** |
| **F4 / F5** | `.skip` / `.todo` → **identity-for-identity indistinguishable from F2's deletion.** P4's limitation *demonstrated*, not asserted |
| **F6** | **Repaired at execution — Finding 1.** Arm 1 (real generator, ambient `CI` unset): `SystemExit`. Arm 2 (**CI pin removed**, ambient unset): **exit 0 with the file collapsed to 1 case** — the corrupt artifact a developer would commit and only ubuntu would reject. Arm 3 (pin removed, ambient `CI=true`): `SystemExit`. **R5 is what makes arms 2 and 3 differ, so R5 is what the row now measures** |
| **F7** | `test.each([1,2,3]) → [1,2]` → `param case 3` specifically absent |
| **F8** | Add a file → 4 files / 7 cases. Both directions covered |
| **F9** | Two cases joining to the same `>`-string → `SystemExit` **naming the duplicate**, not a silent de-duplication |

**Group B — collector, parser and subprocess (substrate `G`, mutated copies).**

| Row | Measured |
|---|---|
| **F10** | Guard present on `[]` → `SystemExit`. **Guard removed → returns `({}, [])` and exits 0** — the hollow surface the guard exists to prevent |
| **F11** | Check present → `SystemExit` **before the file is read**. Check deleted → **succeeds, committing a listing from a run the runner rejected.** **Declared non-isolating** and judged at the seam |
| **F12** | Three arms. All checks present → `SystemExit` (co-killed by F11's). Exit check stubbed → **named** `SystemExit`. **Both deleted → a raw `FileNotFoundError` traceback**, which is exactly what the named check replaces. **The second arm isolates it, as the plan required** |
| **F13** | Truncated payload → `SystemExit` quoting the payload |
| **F14** | File channel on a `process.stdout.write`-contaminated tree → **clean parse**. Stdout channel on the same tree → parse fails. The unmutated arm is the anti-vacuity half |
| **F15** | stderr as payload, **clean** tree → fails. Cannot survive one clean run |
| **F16** | No relativization → the **absolute** path is emitted. Local `--check` would be **green**; the contract assertion is the killer |
| **F17** | No `.as_posix()` → `'static\\js\\a.test.js'` on win32. **Conditionally equivalent on Linux — declared, not skipped** |
| **F18** | Seam: returns listing order, sortedness assertion reds (**primary**). Live: **2 distinct orderings in 3 runs** (secondary) |
| **F19** | Missing key **and superset key** → `SystemExit`. Validation deleted → `KeyError` on the former and, on the latter, **silent acceptance of a changed output format** |
| **F20** | Cross-checks deleted, clean tree → **SURVIVES, declared in advance.** Paired with F9's payload it accepts a collision; with the checks present the same payload dies. **Its kill requires the pairing, and the pairing is stated** |
| **F21** | Collector swapped to `vitest run --reporter=json` → the argv assertions red |
| **F28** | A well-formed **partial** listing → **the parser accepts it.** Nothing in the payload could catch it; `--check` and the pinned counts do |

**Group C — the committed pin (substrate `W`/`C`, Packet F-owned tracked files only).**

| Row | Measured |
|---|---|
| **F21-W** | Real generator, argv swapped → **3** contract tests red, including `test_argv_lists_and_never_runs`. §13.3's stop-condition is now an assertion, not prose |
| **F22** | One number changed in the committed JSON → `--check` **exit 1**, `json_drift=True`, **`md_drift=False`**. The two surfaces are independent and the non-short-circuiting `&` is confirmed by observation |
| **F23** | Vitest table deleted from the committed `.md` → `--check` **exit 1**, **`md_drift=True`, `json_drift=False`** |
| **F24** | **Repaired at execution — Finding 4.** Artifact arm: the `vitest` key absent → **13** contract tests red including `test_top_level_key_set_is_exact`. Generator arm: **fails closed EARLIER than predicted** — `render_markdown()` raises `KeyError` before any diff is produced, so `--check` exits 1 with **zero** `DRIFT:` lines |
| **F25a** | Key renamed in the artifact → **13** red, on the key set. **And measured, not reasoned:** `ci.yml`'s *Report totals* step, replayed against the doctored artifact, **still succeeds** — it indexes named keys and never enumerates |
| **F25b** | `SCHEMA_VERSION` back to `1` → `test_schema_version_is_pinned` reds, alone |
| **F26** | Pinned `231 → 999` **in the test** → the test reds; `--check` stays **green**. The two oracles are independent, and the pinned numbers are read rather than decorative |
| **F27** | Exact counts replaced by `assert isinstance(block, dict)` → **46 passed. SURVIVES, as declared.** The disclosed detection hole, unchanged by anything in this packet |
| **F29** | Renderer stops emitting the section **and the artifact is regenerated** → `--check` **GREEN**, and **four** contract tests red. **This is the row `--check` is structurally blind to**, and the council's most valuable addition after the parser seam |

**Equivalence accounting, corrected per R18:** **no row is a true equivalence.** **Two are
conditional** — F4/F5 (observationally identical to F2, disclosed) and F17 (unkillable on Linux). **One
row survives by design** (F27) and **one has no killer on today's tree** (F20). All four were declared
before execution.

#### Part 5 — findings, including two defects in this packet's own work

**Finding 1 — F6's two arms could not have distinguished anything as drafted.** The plan's arms were
ambient `CI` unset vs `CI=true`. **R5 makes the ambient value irrelevant** — `_run_vitest_list()` sets
it — so both arms hit the same code path. Repaired by making the **CI pin itself** the mutation. The
mechanisms P6 and P7 measured are both still exercised; what varies is now the thing the plan
committed to.

**Finding 2 — the fail-closed path could destroy its own diagnostic. A REAL DEFECT, found by a
mismatch and fixed.** F12's first arm disagreed with its prediction. The investigation: `vitest`
writes **U+276F** into its stack frames, `_run_vitest_list()` quotes the child's stderr verbatim into
the `SystemExit` message, and on a **cp1252** console Python raises `UnicodeEncodeError` **while
printing that message** — so the operator gets a traceback *about the diagnostic* instead of the
diagnostic. On the one path whose entire job is to say what went wrong. Fixed by `_console_safe()`,
which substitutes unencodable characters against the interpreter's stderr encoding and takes that
encoding as a parameter so **the substitution is pinned identically on Windows and Linux**
(`test_quoted_child_output_survives_a_non_utf8_console`). **This is why `COLLECTION_FAILURE` itself is
ASCII** — the owner's ruling quotes it with an em dash and permits "wording such as", and an em dash
on a fail-closed stderr path is the same hazard in miniature.

**Finding 3 — a same-length revert can leave the MUTATION live in the next row.** In the first `W`
run, F26 reported an extra failing test and F27 appeared **killed**. Neither was real. `SCHEMA_VERSION
= 2` → `1` → restore is a **same-length** edit, and CPython invalidates `.pyc` on `(mtime, size)`; a
restore inside one mtime tick reuses the **mutated** bytecode in the next row's process. Confirmed by
re-running F27 in isolation — it passed clean. Both harnesses now set `PYTHONDONTWRITEBYTECODE=1`, and
the final matrix was re-run in full under it. **Recorded because the failure shape is indistinguishable
from a real kill**, and a mutation harness that produces phantom kills is worse than none.

**Finding 4 — F24 and F25a were vacuous as drafted, in the same way F21/F25 already were.** Both
mutated `build_inventory()`, but the contract test reads the **committed** artifact, which a
generator-only mutation does not touch — so both rows would have "passed" while proving nothing about
key absence. The council caught this shape for F21 and F25 (TS5) and **missed it for F24 and F25a**.
Each row is now split: an **artifact** arm that actually tests the contract, and a **generator** arm —
kept, because it produced a genuine finding: deleting the key fails closed **earlier** than predicted,
in `render_markdown()`, before `--check` can produce a diff.

**Finding 5 — the autocrlf phantom is real on this path.** F29's restore initially left
`TEST_INVENTORY.json` "modified" with an **empty** content diff: `_write()` emits LF, the checkout
holds CRLF. The tree-clean gate caught it, which is what the gate is for. The restore now names the
JSON explicitly.

**Deviations from the approved plan, stated rather than folded in.** None touches the approved schema
shape, collection mechanism, owned files, T0 premise or required-gate behaviour, so none is a
stop-and-return condition:

| # | Deviation | Why |
|---|---|---|
| **D-1** | `COLLECTION_FAILURE` uses an ASCII hyphen, not the em dash the ruling quotes | R9 says "wording such as". Finding 2 is the reason: this string reaches stderr on the fail-closed path, and a non-UTF-8 console would replace the diagnostic with an encoding traceback |
| **D-2** | `_vitest_list_argv(path, npx="npx")` takes a second, defaulted parameter | The approved call shape `_vitest_list_argv(path)` still works. Without it, R4's signature and R10's "no contract-test path may reach `_npx()`" cannot both hold |
| **D-3** | `config_include` and its path-prefix cross-check are **absent** | The owner's design ruling, taking the second of R6's two options |
| **D-4** | The `sum(per_file) == len(identities)` check is an **independent-accumulation** check, not a restatement | Counts and identities accumulate separately in one pass, so the check can actually fail (a `counts[relative] = 1` mutation kills it). Building counts *from* the identity list would have made it a tautology — F27's own class |
| **D-5** | No *"every listed file has ≥ 1 case"* check | It is true by construction of `counts`, and an assertion that cannot fail is decoration. Recorded rather than quietly dropped |
| **D-6** | Rows F6, F24, F25a repaired at execution | Findings 1 and 4 |

**Still open. NT-4** — Linux behaviour of `vitest list --json` — is **not** closed by anything above.
Every probe ran on win32/node 24.19.0. **NT-7** (`describe.each`) remains unexercised because no JS
test uses it.

#### Part 6 — the diff

**Seven tracked files, the ceiling §13.16 set. No eighth.**

| File | Change |
|---|---|
| `scripts/generate_test_inventory.py` | +1 collector (three seams), `SCHEMA_VERSION` 1→2, one JSON block, one Markdown section, one console line |
| `tests/test_vitest_inventory_contracts.py` | **new** — 43 test functions, **46 collected nodes**. The **first test of this generator in the repository's history**, for a script that implements a blocking gate |
| `docs/test_inventory/TEST_INVENTORY.json` | regenerated: 757 → 1746 lines |
| `docs/test_inventory/TEST_INVENTORY.md` | regenerated: 215 → 239 lines |
| `docs/ai_workflow/QUALITY_GATE.md` | five → **six** pinned surfaces, with the `.skip`/collection-failure consequences named (QF5a, R24) |
| `.claude/rules/testing.md` | inventory description includes Vitest and `vitest.cases` (QF5b). **Edited in place** — no add/delete, so the parametrized surface is not tripped |
| `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` | §13.16, §13.17, §13.18, and the annotations enumerated below |

**Zero** files under `static/js/**`, `.github/workflows/**`, `routes/**`, `utils/**`, `templates/**`,
`e2e/**`, `scripts/release_gate.py`, `package.json`, `package-lock.json`, `vitest.config.js` or
`.claude/settings.json`. **No branch-protection or repository-setting change.** No permission or
harness configuration was altered at any point.

**The annotation sites are enumerated rather than counted**, because "annotate, never rewrite" is only
a discipline if the coverage is complete — and a numeral is the part of that claim most likely to rot:

> the header's bullet (FOURTH ANNOTATION); **§5**; **§7.1**; **§7.2**; **§9.10**; **§11.10**;
> **§11.13**; **§11.14**; **§11.17**; **§11.18 — BOTH of its false sentences**; §13's preamble;
> §13.0's status clause; §13.1's file-count row, its `e2e/**` row and its *Must not do* paragraph;
> §13.2 Part 2's prediction row; §13.8's preamble; §13.9's `config_include` cell; §13.10's step 10;
> §13.13's annotation; and §13.15's closing paragraph.

**Six of those were added only after review** (§11.10, §11.14, §11.18's second sentence, §13.1's
*Must not do*, §13.9's cell, §13.10's step 10), and **§9.10 and §5's wording were corrected in the same
pass**. The first attempt claimed eleven sites and listed §11.18 among them while having annotated only
one of that section's two false sentences — **a partially-annotated record that then asserted its own
completeness**, which is the failure this enumeration exists to prevent.

#### Part 7 — the qualification-window ledger, extended

**Read live, not from memory**, per §13.0's standing rule.

| # | `main` run | Job | Conclusion | Completed (UTC) |
|---|---|---|---|---|
| **1 — T0** | `32589375849` (`push`, `9cb6cdc`, 18/18 `success`) | `97070630453` | **`success`** | **`2026-08-22T17:59:26Z`** |

| Tally at execution time | Value |
|---|---:|
| Green `main` `JS Unit` results since and including T0 | **1** |
| **Red** / **missing** / **cancelled** | **0** / **0** / **0** |
| `main` runs after T0 of any kind | **0** |

**No red, missing or cancelled result exists in the window.** T0 remains `2026-08-22T17:59:26Z`; the
strict mark remains `2026-09-05T17:59:26Z`. Packet F's own PR runs are **not** `main` runs and do not
enter this ledger.

#### Part 8 — code-time review (R20), and what it changed

**`code-reviewer` and `unslop-reviewer` ran in parallel against the seven-file diff.** Between them
they returned **8 + 15 findings**. **Nineteen were accepted and applied**, **three were routed to
follow-up as out of scope**, and **one was refuted by measurement**. The two reviewers overlapped on
exactly two findings (the `.claude/rules/testing.md` pair) and were otherwise disjoint — the same
result the standing rule about running both predicts.

**REFUTED — the one finding that did not survive checking.**

`code-reviewer` F1 argued from the vitest source (`cac.uFydS1Z4.js:2372-2378`, `cli-api.CnMVyzaz.js:14664`)
that the dominant collection-failure mode is **exit 0 with no file written**, and that the comment
above the exit-code check was therefore backwards. **Measured on vitest 4.1.11 in this worktree:**

| Shape | Exit | Output file |
|---|---:|---|
| Module-scope `throw` | **1** | none |
| Unresolvable import | **1** | none |
| No file matches `include` | **0** | writes `[]` |

**Two of the three collection failures exit 1**, which is what P8, §13.14's S2 and F12 all measured
independently. The reviewer's exit-0 path is real but reaches a **different** shape — an empty include —
and that one **does** write a file, so `exists()` is not its detector either; the **non-empty guard** is.
**The finding is recorded as refuted, and the comment was still rewritten**, because the *caution*
underneath it was sound: it now names all three measured shapes, states that none subsumes another, and
records that `exists()` is meaningful only because `collect_vitest()` hands in a path inside a fresh
`mkdtemp`. *(This is the third time in this document a reviewer prescription has been checked by
running it rather than accepted — and the second time the check changed the disposition.)*

**ACCEPTED AND APPLIED (19).**

| Finding | Applied |
|---|---|
| **CR-F2** — `parse_vitest_listing` validated key NAMES but not value TYPES: a `null` name survived to `identities.sort()` (TypeError) and a non-string `file` raised out of `Path()`, neither carrying `COLLECTION_FAILURE` | Value types added to the shape check; **4 parametrized cases** pin it |
| **CR-F3** — `_console_safe`'s **production** branch was untested. Every call site omits the encoding, so `codec = encoding or "utf-8"` would restore the original bug **with both existing tests green** | A third case pins the default branch through a monkeypatched `sys.stderr` |
| **CR-F8** — the argv pins bound the **helper**, not the call site: inlining `vitest run` into `_run_vitest_list` left all three argv tests green | A call-site test with `_npx` and `subprocess.run` **replaced** (never invoked — R10 holds), which also pins **R5's `CI=true`** and `cwd=REPO_ROOT`, neither of which had a contract test before |
| **CR-F5 / UR-C3** — `.claude/rules/testing.md` called the gate `Test Inventory Drift (non-required)`. **Measured: the job name carries no suffix and it IS 1 of the 12 required contexts** | Corrected, with the required status stated |
| **CR-F6 / UR-C4** — that rule file's frontmatter globs `tests/**` and `e2e/**`, so **the guidance about JS-case renames never loaded for `static/js/**`** | `static/js/**/*.test.js` added to `paths:` — an in-place edit, so the parametrized surface stays untripped |
| **UR-C1** — the inserted Vitest paragraph broke the referent of an untouched sentence: *"That last row"* no longer pointed at the parametrized-configuration row | Referent named explicitly |
| **UR-C2** — `QUALITY_GATE.md`'s **Frontend (JS)** row still required no inventory regeneration, though `static/js/**` now trips a required check | Regeneration requirement added to the row |
| **UR-A1** — the §13 preamble annotation claimed **NT-4 had been taken**, contradicting three other places in the same diff | Corrected; NT-4 is open until the ubuntu run |
| **UR-A2** — the `vitest` block was recorded as **987 lines**; in the artifact it is **985** | Corrected here and in R28. The 987 was a standalone `json.dumps` of the block, whose wrapping braces the artifact does not have — **a real measurement of the wrong object** |
| **UR-A3** — "18 of the 40 contract tests exercise the pure parser" was a grep count including the docstring | **17 of 43 functions / 46 nodes** |
| **UR-A4** — §5's annotation said Packet F **"LANDED"**; it is not merged | Rewritten to the conditional, matching §13.18 |
| **UR-B1** — **§11.18 carries TWO false sentences and only one was annotated**, while Part 6 listed §11.18 as done | Second annotation added; Part 6 now **enumerates** sites instead of counting them |
| **UR-B2** — §11.14's STOP un-annotated | Annotated |
| **UR-B3** — §13.1's *Must not do* forbade editing `QUALITY_GATE.md`'s table, which QF5 authorized and this packet did | Annotated, with the clauses that still hold restated |
| **UR-B4** — §13.10 step 10 states the E2E belief §13.17 Part 1 demolishes | Annotated as measured-false |
| **UR-B5** — four surviving *"five pinned surfaces"* claims (§9.10, §11.10, §13.1) and §13.9's `config_include` cell | All four annotated |
| **UR-D1 / D2** — two docstrings restating their own signatures | Deleted |
| **UR-D3** — the duplicate scan relied on `set.add()` returning `None` inside a comprehension, on the cold path of a blocking gate | `Counter` |
| **CR-F4 (partial)** — `_console_safe` sat under the `# Vitest` banner while being general | Moved to a **Shared helpers** section, with a comment recording that the siblings are deliberately not retrofitted |

**ROUTED TO FOLLOW-UP — out of Packet F's authorized scope (3).**

| Finding | Why not done here |
|---|---|
| **CR-F4 (main)** — `collect_playwright()` and `collect_pytest()` interpolate raw child output the same way and carry the **identical** UnicodeEncodeError hazard; neither prefixes `COLLECTION_FAILURE`. Playwright's stderr carries `✘` and `›` on failure, so it is the **likeliest** of the three to hit it | Retrofitting changes the failure output of two collectors this packet does not own. Requirement 12 covers documentation surfaces, not sibling behaviour, and the ruling says the requirements may not be widened without a new ruling. **Recorded in the code, at `_console_safe`'s docstring, so the next reader finds it where it matters** |
| **CR-F7** — `ci.yml:1106-1108`'s "no browser, no server" rationale no longer enumerates `vitest list`, and the job's `$GITHUB_STEP_SUMMARY` table does not report the surface it now gates | **`.github/workflows/**` is an explicit stop condition.** Not touched, not negotiated |
| **CR-F8 residual** — a `inspect.getsource` meta-test would close the last of it | **Ruling QF7 forbids a source-text meta-test.** The call-site test above closes the substantive half without one; the residual is disclosed alongside F27 |

**One new residual, disclosed.** `test_vitest_block_records_no_status_and_no_duration` is a substring
scan, so a Vitest case literally named `status` would red it. **False-red only** — it cannot hide a
missing pin, and the exact key-set assertions cover the real risk. Recorded rather than "fixed",
because tightening it would trade a harmless false red for a real blind spot.

### 13.18 STOP — merge — **DISCHARGED 2026-08-22 (recorded 2026-08-23)**

> ✅ **DISCHARGE 2026-08-23.** The STOP below was honoured exactly as written: the PR was left
> ready-for-review, green CI was **not** treated as the go-ahead, and the owner gave a separate
> explicit confirmation naming the PR. **PR #411 merged as `2c95bae` at `2026-08-22T21:52:14Z`**;
> post-merge `main` run `32600832091` is **18/18 green**, read at job level.
>
> **Everything else the STOP lists is UNCHANGED and still unauthorized** — **Q4**, **Q6**, **D2**
> (including the `js-unit` promotion), any branch-protection or repository-settings change, any edit
> to `.github/workflows/**`, `scripts/release_gate.py`, `package.json`, `package-lock.json`,
> `vitest.config.js`, `static/js/**` or any pre-existing test, and any `.claude/settings.json` or
> permission change. **§7's branch-protection change is still recorded, not executed**, and its
> "re-measure before executing" warning has been re-confirmed rather than discharged: branch
> protection was re-read live on **2026-08-23** and carries **12** required contexts with
> `JS Unit (Vitest, non-required)` **absent**, so §7.2 would add a **13th**.
>
> **The two surviving obligations, both re-checked here:**
>
> 1. ✅ **NT-4 is CLOSED — and it was closed by measurement, not by argument.** The PR's ubuntu
>    `Test Inventory Drift` job **`97094899990`** (run `32599231895`, `ubuntu-latest`) concluded
>    **`success`** at `2026-08-22T21:19:58Z`, with its *"Check committed inventory against a fresh
>    Linux regeneration"* step green. The claim that Windows and Linux agree on the sorted identity
>    list **may now be written up as measured**, and is, at §13.2's NT-4 row and §13.10 step 12.
>    **NT-7 is untouched and still open.**
> 2. ⏳ **The qualification-window ledger is STILL RUNNING and still owed.** It is extended at
>    **§13.0's LIVE LEDGER block** through `2026-08-23T10:11:56Z`: **two** `main` `js-unit` results,
>    both green, **zero** red / missing / skipped / cancelled. **T0 is unchanged** at
>    `2026-08-22T17:59:26Z` — Packet F changed no JS case, so Q2's restart clause never engaged.
>    Keep extending it at job level, never restating it from memory, until
>    **`2026-09-05T17:59:26Z`**.

> **The PR is open and ready for review. It is NOT merged, and merging is not authorized by anything
> in this document, by green CI, or by a selection among options.**

**Merge requires its own explicit confirmation naming the PR and saying "merge"** — the standing
protocol, restated because it has been broken once in this repository's history and the correction is
the reason the rule is written this way.

**Also still unauthorized, each needing its own confirmation:**

- **Q4**, **Q6**, and **D2** — including the `js-unit` promotion Packet F is a *predecessor* to, not a
  step of. §7's branch-protection change is **recorded, not executed**, and its counts are now known to
  have been wrong once (§7.1's annotation): **re-measure before executing it.**
- Any **branch-protection or repository-settings** change.
- Any edit to `.github/workflows/**`, `scripts/release_gate.py`, `package.json`,
  `package-lock.json`, `vitest.config.js`, `static/js/**`, or any pre-existing test.
- Any `.claude/settings.json` or permission change.

**Two obligations survive this packet and belong to whoever picks it up next:**

1. **NT-4 is closed only by the PR's ubuntu `Test Inventory Drift` run.** Until that job is green, the
   claim that Windows and Linux agree on the sorted identity list is **reasoned, not measured** — and
   it must not be written up as measured before then.
2. **The qualification-window ledger (§13.0, extended at §13.17 Part 7) must be extended, never
   restated from memory**, at every session until `2026-09-05T17:59:26Z`, at **job** level, including
   any red, missing or cancelled result.
