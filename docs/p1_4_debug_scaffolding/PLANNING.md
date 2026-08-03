# P1.4 — Delete the remaining small UI/debug scaffolding

*Plan-stage size: **Medium** under
[QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) — bounded
hygiene across four files, **no schema, API, or calculation surface**. It is not
Trivial (Trivial requires single-file), so **Gate 1 plan approval is required**
before implementation. Gate 0 is included here because two of the six items carry
a real owner choice (Q1, Q2) and one has a rendering consequence the source row
did not record (Q3 / §5).*

**Status: ✅ IMPLEMENTED — Gate 0 and Gate 1 signed by the owner 2026-08-03; all
six items landed on branch `wt/p1-4-scaffolding`, awaiting merge. See
[§Execution record](#execution-record) for the answered questions, the corrected
counts, and the verification evidence.**

Source row: [`LEFTOVERS_BY_PRIORITY.md`](../LEFTOVERS_BY_PRIORITY.md) §1 P1.4
(v23, classified **READY**). Premise re-verified in this document against
`main` @ `4e9b7d0`, and **re-verified again at execution against `origin/main`
@ `828fb07`** — see the execution record for the three count corrections.

---

## Section 0 — Requirements Brief

### Raw request (verbatim)

> P1.4 scaffolding 0% All 6 items confirmed present; bounded single packet Agent 1–3 h
>
> — create a goal to complete it

Completion action carried over verbatim from the P1.4 row:

> One bounded hygiene packet: remove the visible debug counter and simplify the
> now-dead E2E branch; remove or consistently gate the verbose logs; delete the
> zero-caller helper; consolidate the two inert debug wrappers; correct only the
> named KI-005 comment block. Run affected Vitest/pytest plus
> `e2e/progression.spec.ts` and Workout Plan smoke coverage. Ignore the copies
> under `build/` and `dist/` — regenerated output.

### Problem

Six pieces of development-time scaffolding survived into the shipped app. One is
user-visible on `/progression`; the rest are dead or misleading code and one
factually false test comment that tells a reader the KI-005 suite is *expected to
fail* when it has been green since 2026-07-13. None of it is load-bearing, and
each item is independently removable — but the packet has never been executed
because it was sequenced behind P1.5 (**N6**), which has now shipped.

### Verified premise (re-verified at `4e9b7d0`, 2026-08-03)

All six items are still present. `build/` and `dist/` copies are excluded from
every count below.

| # | Item | Evidence at HEAD |
|---|---|---|
| 1 | User-visible debug counter | [`templates/progression_plan.html:20-22`](../../templates/progression_plan.html#L20-L22) — `<div class="debug-info …">Available exercises: {{ exercises\|length }}</div>` inside `.exercise-selector` |
| 2 | Verbose logs | **17** unguarded `console.log` in [`progression-plan.js`](../../static/js/modules/progression-plan.js) (lines 100, 114, 122, 140, 141, 162, 168, 175, 183, 280, 296, 298, 306, 313, 316, 343, 382) |
| 3 | Inert debug wrapper A | [`app.js:35-40`](../../static/js/app.js#L35-L40) — `const APP_DEBUG = false` + `appDebugLog`, **15** call sites |
| 4 | Zero-caller helper | [`workout-plan.js:94`](../../static/js/modules/workout-plan.js#L94) — `handleApiResponse()`, already `@deprecated`; repo-wide grep returns **only** its definition line |
| 5 | Inert debug wrapper B, duplicated | [`workout-plan-add-exercise.js:33-38`](../../static/js/modules/workout-plan-add-exercise.js#L33-L38) (module scope, **4** call sites) and [`workout-plan.js:137-142`](../../static/js/modules/workout-plan.js#L137-L142) (also module scope despite its indentation, **2** call sites) — byte-identical bodies, both permanently `false` |
| 6 | False test comment | [`ui-hardening.spec.ts:739-748`](../../e2e/ui-hardening.spec.ts#L739-L748) — "PRE-IMPLEMENTATION ACCEPTANCE TESTS … expected to be RED until it lands". KI-005 landed 2026-07-13 (`2426c89`) and is recorded ✅ Resolved in [`UI_SCENARIOS_GAP_ANALYSIS.md:100`](../UI_SCENARIOS_GAP_ANALYSIS.md). **#284 rewrote other parts of this same file and left this header untouched.** |

Two facts that make item 1 safe to delete:

- [`progression.spec.ts:98-101`](../../e2e/progression.spec.ts#L98-L101) wraps the
  assertion in `if (await debugInfo.isVisible())`, so removing the block cannot
  red that test — it silently degrades to a no-op branch, which is exactly why the
  branch must be deleted with the block.
- No `tests/**` file references `debug-info` or `Available exercises`.

And one that makes item 2 safe: the `consoleErrors` fixture
([`fixtures.ts:25-44`](../../e2e/fixtures.ts#L25-L44)) collects only
`msg.type() === 'error'`, so removing `console.log` calls cannot change any
spec's outcome.

### Acceptance criteria

1. **Given** `/progression` renders, **when** the DOM is inspected, **then** no
   element carries class `debug-info` and the string `Available exercises` does
   not appear. *(Subject to Q3.)*
2. **Given** `e2e/progression.spec.ts`, **when** `exercise selector shows
   available exercises` runs, **then** the spec contains no `.debug-info` locator
   and no `isVisible()` guard, and still asserts the option count directly.
3. **Given** `static/js/modules/progression-plan.js`, **when** grepped, **then**
   it contains **0** unguarded `console.log(` calls (from 17), and the module's
   observable behavior on `/progression` is unchanged.
4. **Given** the three debug wrappers, **when** grepped, **then** exactly one
   definition survives per the owner's Q2 choice — no module declares its own
   permanently-`false` `*_DEBUG` const with a duplicated helper body.
5. **Given** `static/js/modules/workout-plan.js`, **then** `handleApiResponse` is
   gone and no reference to it exists outside `build/` and `dist/`.
6. **Given** `e2e/ui-hardening.spec.ts`, **then** the KI-005 block header states
   that KI-005 shipped (2026-07-13, `2426c89`) and that these are green
   regression locks, and **no other comment block or assertion in that file is
   edited** — #284's KI-006 work is untouched.
7. **Given** the packet is finished, **when**
   `python scripts/generate_test_inventory.py --check` runs, **then** it reports
   no drift; if it does report drift, the regenerated
   `docs/test_inventory/TEST_INVENTORY.{json,md}` are committed as the **last**
   step of the branch (**N5**).
8. **Given** the full derived gate below runs, **then** every named suite is green
   with no new console errors and no product behavior change other than the
   removed counter.

### In scope

`templates/progression_plan.html`, `static/js/app.js`,
`static/js/modules/progression-plan.js`, `static/js/modules/workout-plan.js`,
`static/js/modules/workout-plan-add-exercise.js`, the one test in
`e2e/progression.spec.ts`, and the one comment block in
`e2e/ui-hardening.spec.ts`.

### Out of scope

- **Every other `console.log` in `static/js/`.** `exports.js`, `workout-log.js`,
  `ui-handlers.js`, `filters.js`, `exercises.js`, `fetch-wrapper.js`,
  `workout-controls-animation.js` and `filter-view-mode.js` all log too. The P1.4
  row names `progression-plan.js` only; a repo-wide log policy is a separate
  proposal, not this packet.
- Any refactor of `progression-plan.js` beyond deleting log statements.
- Any change to KI-005 or KI-006 assertions, or to any other spec.
- `build/` and `dist/` copies — regenerated output.
- Introducing a build-time debug flag, log level, or logger abstraction.

### Assumptions

- ⚠️ The 17 `console.log` calls are pure development narration with no operator
  value; nothing outside the browser console consumes them.
- ⚠️ Deleting `handleApiResponse` is safe because nothing imports it by design,
  not because a caller was recently removed and will return. It is already marked
  `@deprecated` in favor of the `api` wrapper.
- ⚠️ The `.debug-info` class has no styling of its own worth preserving (it rides
  on `text-muted small mb-3` Bootstrap utilities) — confirm no `scss/**` rule
  targets it before deleting, and remove the rule with the block if one exists.
- ⚠️ Item 6 is a comment-only edit; the KI-005 tests themselves are correct as
  written and stay untouched.

### Calculation surface

**none.** No file in scope imports `utils/effective_sets.py`,
`weekly_summary`, `session_summary`, `progression`, or fatigue logic. No
migration notes are owed.

---

## §5 — The one finding the source row does not carry: visual baselines

**Deleting the `.debug-info` block changes what `/progression` renders, which
stales 12 committed visual baselines** — `progression-{desktop,tablet,mobile}-{light,dark}.png`
under both [`e2e/__screenshots__/win32/`](../../e2e/__screenshots__/win32) and
[`e2e/__screenshots__/linux/`](../../e2e/__screenshots__/linux). `visual.spec.ts`
screenshots the whole page and the block sits high in `.exercise-selector`.

Severity, stated precisely:

- **Not a merge blocker.** `visual.spec.ts` is excluded from required CI and from
  the deep gate's full run; `visual-linux` is manual-only and *never* a required
  check ([`deep-gate.yml:10-22`](../../.github/workflows/deep-gate.yml#L10-L22)).
- **But it collides with frozen state.** PR **#281** (draft, owner review
  required) regenerates exactly these six Linux progression PNGs at `4de6b62`.
  Landing the template deletion first makes #281's progression baselines stale
  *before* the owner finishes reviewing them, and the visual-determinism arc
  (#286, Gate 2 FAILED) is already open on the same surface.
- Windows baselines can be regenerated locally; Linux baselines cannot be
  produced from this machine. Re-baselining here would be an **intentional**
  markup change, not a tolerance raise — but it must be an owner decision, not a
  side effect of a hygiene packet.

This is what Q3 below is asking about.

---

## Blocking questions for the owner (Gate 0) — ANSWERED 2026-08-03

> **Owner rulings, verbatim:** *"Q1 delete all 17 progression logs; Q2 delete the
> inert debug wrappers and their 21 no-op call sites; Q3 delete the visible
> progression counter now."* Plus: intentionally regenerate and review the six
> affected **Windows** progression baselines, leave Linux regeneration to
> **#281**, and do not touch unrelated console logging or broaden the refactor.
>
> So: **Q1 = delete** (the recommendation). **Q2 = option (a)**, delete both
> wrappers and every call site. **Q3 = option (b)**, land all six now and
> re-baseline win32 in this PR — the recommended split (a) was **not** taken.

**Q1 — the 17 logs: delete or gate?** The row says "remove **or** consistently
gate." *Recommendation: **delete**.* Gating them behind another
permanently-`false` const recreates in `progression-plan.js` precisely the dead
wrapper this packet removes from two other modules.

**Q2 — the debug wrappers: delete outright, or consolidate into one shared
helper?** There are 21 call sites total (15 `appDebugLog`, 4 + 2
`workoutPlanDebugLog`), all currently no-ops.
(a) **Delete both wrappers and all 21 call sites** — smallest surface, loses the
    log statements' text permanently. *Recommended.*
(b) **One shared `static/js/modules/debug-log.js`**, imported by all three
    modules, still defaulting to off — keeps the call sites, adds a module.
(c) Delete the duplication only: keep `app.js`'s wrapper, have the two
    workout-plan modules import it.
Note (a) is a larger diff than (b) despite being the smaller end state.

**Q3 — the visible counter: delete now, or split the packet?** Per §5:
(a) **Split — recommended.** Land items 2–6 now (zero visual impact, zero
    baseline churn), and hold item 1 until #281 is reviewed and the visual arc
    unfreezes. P1.4 then closes in two commits instead of one.
(b) Land all six, regenerate the six win32 progression baselines in the same PR,
    and explicitly record the six Linux ones as stale for #281 to absorb.
(c) Keep the count as a deliberate, non-debug UI label (drop the `debug-info`
    class and the "Available exercises:" debug phrasing) — this is a product
    choice, not hygiene, and still changes the baselines.

---

## Derived verification gate

From [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) change-type → gates,
union of the touched paths (`templates/**`, `static/js/**`, `e2e/**`):

| Path touched | Required |
|---|---|
| `templates/progression_plan.html` | Chromium `progression`, `smoke-navigation`, `empty-states` (all three navigate the progression route) |
| `static/js/**` | the specs above + `workout-plan`, `ui-hardening`, `exercise-interactions`; `npx vitest run` (9 suites under `static/js/modules/__tests__/`) |
| `e2e/**` | run the edited specs; re-baseline only if §5 option (b) is chosen, and only intentionally |
| whole packet | `pytest tests/ -q` (unchanged, but it is the cheap regression net); `python scripts/generate_test_inventory.py --check` **last** |
| reviewers | none required by path; `/unslop` (`code-reviewer` + `unslop-reviewer`) is appropriate for a delete-only packet |

Sequencing facts, verified 2026-08-03 — recheck at execution:

- **N6 discharged.** P1.5 shipped as **#284** (`4e9b7d0`), so P1.4 now owns
  `e2e/ui-hardening.spec.ts` alone.
- No open PR touches any file in scope. #287/#288 are dependency bumps, #286 is
  visual determinism, and #281 touches only `e2e/__screenshots__/linux/**` — which
  is exactly the §5 overlap, and only if Q3 answers (b).
- **N5 stands:** regenerate the test inventory as the final step, never mid-branch.

## Execution record

Executed 2026-08-03 on branch `wt/p1-4-scaffolding`, based on `origin/main`
@ `828fb07` (**not** the `4e9b7d0` this plan was drafted against — #290 landed in
between, and that turned out to matter; see §Baselines below).

### Count corrections found at re-grep

The plan told the executor to re-grep before acting. Three counts moved:

| Claim in the premise table | Actual at `828fb07` |
|---|---|
| `appDebugLog` — 15 call sites | **14** |
| `workoutPlanDebugLog` in `workout-plan.js` — 2 call sites | **1** |
| `workoutPlanDebugLog` in `workout-plan-add-exercise.js` — 4 call sites | **3** |
| **Total "21 no-op call sites"** | **18** |

The owner's Q2 ruling names 21, but its intent — delete *every* no-op call site —
is unambiguous, so all 18 were deleted. The other three items matched exactly:
**17** `console.log`, one `.debug-info` block, one zero-caller `handleApiResponse`.

### Structural consequences of deleting the call sites

Deleting a call site whose enclosing shell existed only to hold it leaves visible
residue, so the shell went with it — the same reasoning §0 applies to the
`isVisible()` guard in `progression.spec.ts`:

- Five `return { cleanup: () => { … } }` objects in `app.js` whose only statement
  was an `appDebugLog` call. **Nothing consumes them** — `initializer()` at the
  DOMContentLoaded handler discards the return value (verified by grep).
- `initializeHomePage()`, whose entire body was two `appDebugLog` calls, plus its
  `'/': initializeHomePage` entry in `pageInitializers`. `/` now has no
  page-specific initializer, which is behaviourally identical to running the
  empty one; `commonInit()` still runs on every path.
- The `else` branch of the initializer lookup, which held only a log.

**Deliberately left alone** (pre-existing, out of scope, flagged not fixed):
`initializeModules()` in `app.js` has **zero callers** and is dead independently
of this packet. Its two logs were removed; the function was not. Also untouched:
the `#debug-info` **ID** rules at `static/css/pages-workout-log.css:613,621`,
which match no element anywhere in the repo — a different symbol from the
`.debug-info` **class** this packet removed.

No `scss/**` or `static/css/**` rule targets the `.debug-info` class, so the
§0 assumption held and no CSS rule needed removing.

### Baselines — the finding that changed §5

§5 predicted this packet would stale 12 progression baselines. **Six of them
(win32) were already stale before this branch existed**, and §5 could not have
known: `828fb07` (#290, merged the same day, and this branch's base) added
`VISUAL_PROGRESSION_GOALS` to `e2e/scripts/prepare_visual_db.py` — three seeded
`completed = 0` goal rows that make the Current Goals table render populated —
without regenerating the win32 progression baselines, which were last written in
**#82**. The committed win32 baselines still showed an *empty* goals table.

Proven, not assumed: the six progression visual specs were run against a
**stashed, pristine `origin/main` tree** and all six failed there too. Attribution
is therefore exact:

| Component | Evidence |
|---|---|
| #290's pre-existing drift (populated goals table, tablet 768→770px) | 6/6 fail on pristine `main`; mobile page 812px baseline vs **2132px** actual |
| This packet's own delta (the removed counter line) | mobile actual **2132px → 2113px**, a **19px** reduction, nothing else |

The regenerated win32 baselines therefore absorb both. That is the correct
current render of `main` + this packet, and it is strictly better than leaving
six known-stale PNGs committed — but it is recorded here explicitly so the
re-baseline is never read as this packet alone having changed that much.

**Linux baselines were deliberately not touched** (owner instruction) and remain
for **#281**. Note for whoever reviews #281: its six Linux progression PNGs are
regenerated at `4de6b62`, which predates #290, so they carry the same
empty-goals-table staleness plus this packet's removed line.

### Verification evidence

| Gate | Result |
|---|---|
| `pytest tests/ -q` | **2443 passed, 2 skipped** (8m12s) |
| `npx vitest run` | **105 passed**, 9 suites |
| Chromium `progression`, `smoke-navigation`, `empty-states`, `workout-plan`, `ui-hardening`, `exercise-interactions` | **145 passed**, 0 failed |
| `visual.spec.ts -g "visual baseline: progression"` (win32) | 6 regenerated, reviewed image-by-image, re-run **6 passed** |
| `node --check` on all four edited JS modules | clean |
| Residue grep (`APP_DEBUG`, `appDebugLog`, `WORKOUT_PLAN_DEBUG`, `workoutPlanDebugLog`, `handleApiResponse`, `debug-info`, `Available exercises`) outside `build/`+`dist/` | **0 hits** |
| `scripts/generate_test_inventory.py --check` | run last (**N5**): **"Test inventory is up to date"** — no drift, nothing to regenerate. This packet removes assertions *inside* an existing test but adds/removes no test, so the generated inventory is unchanged and the N5 contention with #274/#275 does not arise. |

### Out-of-scope observations (not fixed here)

1. `initializeModules()` — zero-caller dead function in `app.js`.
2. `#debug-info` ID rules in `pages-workout-log.css` — match no element.
3. At tablet width the Current Goals responsive table renders its header row as
   only `Exercise` / `Actions` with the remaining columns unlabelled, and
   overflows to 770px in a 768px viewport. Visible in the regenerated tablet
   baselines; predates this packet.

---

## Definition of done

Item 1 of the LEFTOVERS §6 closure rule: implementation and proportional
verification landed on `main`, the P1.4 row retired from
[`LEFTOVERS_BY_PRIORITY.md`](../LEFTOVERS_BY_PRIORITY.md), and this document
banner-flipped to SHIPPED with the merge SHA. If Q3 answers (a), the row is
retired only when the held-back item 1 also lands — until then it stays open with
its scope narrowed to that single line, in writing.

---

*Created 2026-08-03 against `main` @ `4e9b7d0`. Premise counts are snapshot
evidence: re-grep before acting.*
