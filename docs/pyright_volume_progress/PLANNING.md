# Pyright burn-down packet — `utils/volume_progress.py` `reportAssignmentType`

*Continuous track — pyright baseline burn-down (`docs/REFACTOR_PLAN.md` §"Continuous
track"). One file, one tightly coupled diagnostic family, type-only.*

Branch `wt/pyright-vp`. Forked from `origin/main` @ `ac2923b`; rebased onto
`origin/main` @ `f8988f9` before the final baseline regeneration, per the §6 rebase
rule. The intervening commit (#298, visual capture coverage) touches no file this
packet owns and added no pyright diagnostic — the rebased tree still measures 174.
Planning size: **Medium** (`docs/ai_workflow/QUALITY_GATE.md` §Plan-stage routing) —
bounded, known contracts, but it edits a module on the volume calculation surface.
Gate 0 is waived: requirements and non-goals were fully specified by the owner.

---

## 0. Objective

Eliminate exactly the one existing `reportAssignmentType` diagnostic in
`utils/volume_progress.py` without changing runtime values, ordering, calculations,
API behavior, database behavior, or any other Pyright diagnostic family.

### Non-goals

- No calculation, ordering, or serialization change.
- No change to taxonomy constants, basic/advanced mode selection, target
  calculation, set distribution, diagnostics payloads, API output, or persistence.
- No change to any test expectation.
- No opportunistic fixes to other diagnostics or other files.
- No suppression: no `Any`, no `cast(Any, ...)`, no `# type: ignore`, no rule
  disablement, no broad union, no baseline-only edit.

---

## 1. Exact diagnostic identity

Reproduced on an unmodified branch at `ac2923b` under the committed
`pyrightconfig.json` (pythonVersion 3.14, pythonPlatform Windows).

**Pyright version — pinned to CI. [corrected in v2 — F1]** `.github/workflows/ci.yml:700`
runs `npx pyright@1.1.410`, and `ci.yml:652` records that the committed baseline was
generated under 1.1.410. Every run in this packet therefore uses `npx pyright@1.1.410`,
not bare `npx pyright` (which currently resolves to 1.1.411).

```
npx pyright@1.1.410 --outputjson
→ version 1.1.410, filesAnalyzed 213, errorCount 175, warningCount 0
npx pyright         --outputjson
→ version 1.1.411, filesAnalyzed 213, errorCount 175, warningCount 0
```

Both versions were run and their diagnostic **multisets compared key-by-key** through
`scripts/pyright_baseline_diff.py`'s own `counts_from_diagnostics`:

```
410 == 411      : True
410 == baseline : True
totals 175 / 175 / 175      keys 51 / 51 / 51
```

So the two releases agree exactly on this tree today. The packet still pins 1.1.410,
because that equality is a measured fact about this tree at this commit, not a
guarantee about the version `npx` resolves after a rebase.

The single tracked instance:

| Field | Value |
|---|---|
| file | `utils/volume_progress.py` |
| severity | `error` |
| rule | `reportAssignmentType` |
| message | `Type "tuple[str, ...]" is not assignable to declared type "list[str]"\n  "tuple[str, ...]" is not assignable to "list[str]"` |
| range | 0-based line 236 char 27 → line 239 char 9 (**1-based lines 237–240**) |
| baseline count | 1 |

Gate reproduction against the committed snapshot:

```
python scripts/pyright_baseline_diff.py --current artifacts/pyright_before.json \
    --baseline docs/ci_cd_phase3/pyright-baseline.json
→ pyright baseline gate: PASS — 0 net-new diagnostics (baseline 175, current 175).
```

Current committed baseline `_meta`: **175 total_diagnostics / 51 distinct_keys**
(re-derived, not assumed). `reportAssignmentType` has **exactly one instance
repo-wide**, and it is this one — so closing it removes the entire rule family from
the baseline, taking it to **174 / 50**.

### 1.1 Premise correction — the owner's stated cause is not the actual cause

The packet brief attributes the diagnostic to `_mode_muscles()` "being declared as
`list[str]` while returning the taxonomy group tuples". **That is not what Pyright
reports, and it is not true of the code.**

- `utils/volume_taxonomy.py:18` declares `BASIC_MUSCLE_GROUPS: list[str] = [...]` and
  `:39` declares `ADVANCED_MUSCLE_GROUPS: list[str] = [...]`. Both are genuine
  `list` literals, not tuples.
- `_mode_muscles()` (`utils/volume_progress.py:66`) therefore returns `list[str]`
  from both branches and its `-> list[str]` annotation is already truthful. It emits
  **zero** diagnostics.

The real defect is a **reused local name** in `_aggregate_blank_pst_row`. The name
`advanced_targets` is declared `list[str]` in the advanced branch
(`volume_progress.py:220`) and then rebound in the mutually exclusive basic branch
(`:237`) with the `tuple[str, ...]` returned by `_record_token_resolution()`. Pyright
scopes a declared type to the whole function, so the basic-branch rebind violates the
advanced-branch declaration.

The *target* is unambiguous regardless — the file contains exactly one
`reportAssignmentType` — so the objective is deliverable as written. Only the
attributed cause changes, and with it the shape of the fix: the owner's stated
preference ("correct the private function's type contract") was written for
`_mode_muscles()` and does not apply, because no function's return contract is
untruthful here. The *spirit* of that preference — make the declaration describe the
real value rather than convert values to satisfy a declaration — is what §4 follows.

`_mode_muscles()` is therefore **left untouched**. Editing it would be a gratuitous
change to a function that produces no diagnostic.

### 1.2 Encoding hazard found while verifying §1

Pyright indents continuation lines of a diagnostic message with **U+00A0 non-breaking
spaces**, so the baseline's `message` values contain non-ASCII bytes. Reading
`pyright-baseline.json` without an explicit encoding on Windows (cp1252 default)
silently mangles every multi-line message and makes the multiset comparison report 26
phantom key differences. `scripts/pyright_baseline_diff.py` already handles this
correctly — `read_text(encoding="utf-8")` (`:222`), `write_text(..., encoding="utf-8")`
with `ensure_ascii=False` (`:210–213`) — so the tool is sound and needs no change. This
is recorded because it will bite anyone who inspects the artifact with an ad-hoc script,
as it bit the first verification pass of this plan.

---

## 2. Caller inventory

### 2.1 `_mode_muscles()` — 2 call sites, both in-file, both iteration-only

`rg _mode_muscles` over the whole repository:

| Site | Use | Mutates? | Relies on list identity? |
|---|---|---|---|
| `utils/volume_progress.py:304` | `totals = {muscle: 0.0 for muscle in _mode_muscles(normalized_mode)}` | no — dict comprehension over the iterable | no |
| `utils/volume_progress.py:455` | `muscle_order = _mode_muscles(mode)`, consumed only by the `for muscle in muscle_order` comprehension at `:456–460` | no — builds a **new** list `all_muscles` | no |
| `docs/scan/PHASE_03.md:410` | prose reference only | — | — |

No caller outside the module; no route, template, or test references it. Nothing
mutates the returned object, appends to it, compares it by identity, or serializes it
directly. Recorded for completeness only — **this packet does not modify
`_mode_muscles()`**.

### 2.2 Consumer chain of the function actually being edited [added in v2 — F6/PR-1]

§2.1 inventories the function the packet does *not* change. The chain that reaches the
edited lines:

```
_aggregate_blank_pst_row            utils/volume_progress.py:191   ← edited (:237, :241)
  ← aggregate_planned_sets          utils/volume_progress.py:315
    ← get_volume_progress           utils/volume_progress.py:436
      ← GET /api/volume_progress    routes/workout_plan.py:69–73 (imports at :17)
        ← plan_volume_panel.js      static/js/modules/plan_volume_panel.js:218
```

The endpoint belongs to the **Plan** blueprint, not Distribute. `rg` for
`utils.volume_progress` across `tests/` returns **only** `tests/test_volume_progress.py`,
which already contains the endpoint coverage (`:283`, `:305`, `:520`).
`tests/test_volume_splitter_api.py` imports `routes.volume_splitter`, `utils.database`
and `utils.volume_export` — never `utils.volume_progress` — and
`routes/volume_splitter.py:6` imports only `activate_volume_plan` /
`deactivate_volume_plan`, neither of which this packet touches. The §6 route/API gate
row is corrected accordingly.

### 2.3 The actual defect site — `_aggregate_blank_pst_row` basic branch

> **Describes the pre-fix source.** Line numbers and the `advanced_targets` binding
> below are the state this packet started from. For the post-fix source, see §4.

`advanced_targets` inside `_aggregate_blank_pst_row` has exactly **two** binding
regions, in mutually exclusive branches:

| Lines | Branch | Binding | Type | Downstream use |
|---|---|---|---|---|
| 220, 222–224, **225**, 228 | `if mode == "advanced":` (returns at `:229`) | `advanced_targets: list[str] = []`, then `.extend(...)` | genuine `list[str]`; `.extend` requires a real list | read at `:225` (`if not advanced_targets:`) then `_add_distributed(totals, advanced_targets, contribution)` at `:228` |
| 237–240 | basic path (only reachable when the advanced branch did not run) | `advanced_targets = _record_token_resolution(...)` | `tuple[str, ...]` | `for advanced in advanced_targets:` at `:241` — **iteration only** |

*(`:225` added in v2 — F4. The advanced branch `return`s at `:229`, so this read can
never observe the basic-branch binding; the conclusion is unchanged, but an
enumeration offered as proof has to be exhaustive.)*

The basic-branch value is consumed by a single `for` loop and is never mutated,
stored, compared, or returned. `_record_token_resolution()` already declares
`-> tuple[str, ...]` truthfully (`:176`); its returns are `()`, or the tuple from
`_advanced_targets_for_token()` which is `tuple[str, ...] | None` (`:74`). No caller
needs list identity or mutability at `:237`.

---

## 3. Proof that the calculation surface is unchanged

The change is a **local-variable rename inside one function body**. It cannot alter
behavior, and the following are the specific reasons. *(As in §2.3, line numbers and
the `advanced_targets` name describe the pre-fix source.)*

1. **No value changes.** The right-hand side of `:237` is untouched;
   `_record_token_resolution()` is called with identical keyword arguments.
2. **No type coercion.** The tuple is *not* converted to a list. `for advanced in
   <tuple>` and `for advanced in <list>` iterate identically and in the same order.
3. **No ordering change.** `basic_targets.append(...)` order at `:244` is driven by
   the `tokens` loop and the tuple's own order, both unchanged.
4. **No scope leak, and the `diagnostics` appends are identical.
   [reworded in v2 — PR-3]** The renamed name is function-local and dies at the
   `return`; `_aggregate_blank_pst_row` returns `None` and mutates only `totals` and
   `diagnostics`. The renamed line *is* the call that appends to
   `diagnostics["ignored_tokens"]` / `["unmapped_muscles"]` (`:180`, `:187`) — so
   rather than claiming `diagnostics` is untouched, the correct claim is that the
   call site, its keyword arguments and its call order are unchanged, making those
   appends identical in content and order.
5. **No signature change.** No function's parameters, return type, or name changes.
6. **Nothing else in the module reads the name.** `advanced_targets` appears at
   `:220`, `:222`, **`:225`**, `:228`, `:237`, `:241` and nowhere else in the
   repository; the advanced-branch occurrences are in a branch that `return`s at
   `:229`, before `:231` is reachable. *(`:225` added in v2 — F4.)*
7. **Existing coverage already pins the exact path.**
   `tests/test_volume_progress.py:217` —
   `test_selected_exercise_with_blank_pst_uses_isolated_only_strategy` — drives a
   blank-P/S/T row with tokens `["upper-pectoralis", "long-head-triceps"]` and
   asserts `basic_totals["Chest"] == 2.0` and `basic_totals["Triceps"] == 2.0`.
   Those two assertions are produced *by the lines being renamed*
   (`:237` → `:241` → `ADVANCED_TO_BASIC` → `basic_targets` → `_add_distributed`).
   The sibling `exclude`-strategy test at `:239` additionally pins the early return
   at `volume_progress.py:201–202`.

   **[corrected in v2 — F5]** Plan v1 also cited an "ignored-token test at `:400`" as
   pinning a surrounding branch. That citation was wrong twice over: the test is
   `test_ignored_token_is_not_attributed_but_is_recorded` at
   `tests/test_volume_progress.py:396` (`:400` is an argument line), and it builds the
   exercise with `primary="Chest"` (`:402`), so `role_values` is not all-`None` and
   `aggregate_planned_sets` never enters `_aggregate_blank_pst_row` at all
   (`volume_progress.py:314–315`) — it exercises `_aggregate_advanced_primary`. It is
   withdrawn as evidence. §3.7 rests on `:217` (the edited path) and `:239` (the early
   return), which are both verified.

**Conclusion:** the calculation surface is provably unchanged, and the proof is
enforced by tests that already exist and are not being modified.

---

## 4. Chosen type contract, and rejected alternatives

### Chosen — rename the basic-branch local so each name carries one truthful type

```python
# utils/volume_progress.py, _aggregate_blank_pst_row, basic branch
-        advanced_targets = _record_token_resolution(
+        token_targets = _record_token_resolution(
             raw_token=token,
             diagnostics=diagnostics,
         )
-        for advanced in advanced_targets:
+        for advanced in token_targets:
```

Two lines. The advanced-branch accumulator keeps its `list[str]` declaration, which is
correct there (it is built with `.extend`). The basic-branch name is new and
undeclared, so Pyright infers `tuple[str, ...]` — the value's real type. Both
declarations now describe what they actually hold, which is the truthful correction
the owner asked for, applied at the site that is actually lying.

Rationale for `token_targets`: the function already distinguishes `basic_targets`
(the accumulator) from per-token resolution results, and the sibling function
`_aggregate_advanced_primary:263` uses the same per-token-result idiom
(`targets = _advanced_targets_for_token(token)`). `token_targets` reads correctly at
the use site: `for advanced in token_targets`.

### Rejected alternatives

| Alternative | Why rejected |
|---|---|
| Change `_mode_muscles() -> list[str]` to `Sequence[str]` / `tuple[str, ...]` | It is not the diagnostic's cause (§1.1). It emits no error; changing it fixes nothing and edits a function outside the defect. |
| `list(_record_token_resolution(...))` at `:237` | Mechanically converts a tuple into a new list to satisfy a declaration. Explicitly forbidden by the owner, allocates per token, and is behavior-adjacent for no benefit. |
| Re-declare `advanced_targets: tuple[str, ...]` at `:237` | Pyright rejects a second declaration of the same name in one scope (`reportRedeclaration`) — trades one diagnostic for another. |
| Widen `:220` to `list[str] \| tuple[str, ...]` | A broad union, explicitly forbidden. It also breaks `.extend` at `:222` since tuples have no `.extend`, producing a new diagnostic. |
| Rename the **advanced**-branch accumulator instead | Equivalent correctness, but touches three lines (`:220`, `:222`, `:228`) instead of two, and would rename the name whose declaration is already accurate. |
| `# type: ignore` / `cast` / rule disable / baseline-only edit | Explicitly forbidden; all four hide the defect rather than remove it. |
| Extract the basic loop body into a helper | A structural refactor disguised as a typing fix — barred by the burn-down track rule "type-only changes; no behavior refactors disguised as typing fixes". |

### Observation recorded, deliberately not acted on

`_mode_muscles()` returns the module-level mutable lists `taxonomy.BASIC_MUSCLE_GROUPS`
/ `ADVANCED_MUSCLE_GROUPS` **by reference**, so a future caller that mutates the result
would corrupt the taxonomy for the whole process. No current caller does (§2.1), so
this is latent, not live. Hardening it would change a return contract on the volume
calculation surface and is out of this packet's scope.

**[scoped in v2 — PR-4]** The same by-reference aliasing exists in two places *outside*
`_mode_muscles()`, so a future hardening packet must treat it as one surface rather
than fixing one function and declaring it done:

| Site | Shape | Current use |
|---|---|---|
| `utils/volume_splitter_service.py:36–37` | `get_muscle_list_for_mode()` returns `BASIC_MUSCLE_GROUPS` / `ADVANCED_MUSCLE_GROUPS` directly | read-only at `routes/volume_splitter.py:67–70` |
| `routes/volume_splitter.py:38–39` | binds both module lists and passes them into `render_template` | read-only |
| `utils/volume_progress.py:66` | `_mode_muscles()` | read-only (§2.1) |

All three are read-only today, so the hazard is latent everywhere and live nowhere.
Recorded so the next burn-down packet can decide on the whole surface with evidence.

---

## 5. Test plan

No new test. Per §3.7 the exact renamed path is already pinned by
`tests/test_volume_progress.py:217`, and the owner's brief directs a focused
characterization test *only if caller behavior is not already pinned*. A test
asserting an annotation string is explicitly excluded by the brief.

**[withdrawn in v2 — F3/F8]** Plan v1 additionally argued that adding a test "would
move the generated test inventory and red the `Test Inventory Drift` CI gate". That is
false and has been removed. `ci.yml:894–896` and `.claude/rules/testing.md:22` both
state the opposite policy: a drifted inventory is fixed by running
`scripts/generate_test_inventory.py` and committing the artifact in the same PR. It is
a one-command chore, never a reason to skip needed coverage. §5 rests on §3.7 alone.
(The separate claim that *this* change does not move the inventory is correct — the
generator derives everything from `pytest --collect-only`, `playwright test --list` and
a `waitForTimeout` scan of `e2e/**`, none of which a local-variable rename affects.)

**Conditional obligation [added in v2 — F9].** The "no new test" conclusion is valid
only for a strictly 2-line diff. If the implementation diff is anything other than
exactly 2 insertions / 2 deletions confined to lines 237–241, the conclusion is void
and a characterization test over the unpinned `_BASIC_ONLY_TOKEN_TO_BASIC` blank-P/S/T
path becomes required. §6 makes this a mechanical gate rather than a promise.

**Pre-existing coverage gaps, recorded and out of scope.** `_aggregate_blank_pst_row`'s
`backfill` branch (`:203–205`), all three `blank_pst_orphan` increments (`:209`,
`:226`, `:247`) and the `_BASIC_ONLY_TOKEN_TO_BASIC` early-`continue` (`:234–236`) have
no test anywhere (`rg blank_pst_orphan tests` returns nothing;
`docs/scan/PHASE_03.md:272` already records the backfill gap). This packet does not
close them — it must not, being type-only — but they are listed so the §3.7 pin is not
mistaken for full coverage of the function.

---

## 6. Gates

Derived from `docs/ai_workflow/QUALITY_GATE.md` (Business logic row: `utils/**.py`
non-DB → `pytest tests/test_<module>.py` + `code-reviewer`) unioned with the
burn-down track gate in `docs/REFACTOR_PLAN.md` ("zero net-new diagnostics, lower
count, focused tests, then full pytest").

### Focused

| Gate | Command | Expected |
|---|---|---|
| **Diff shape** [F9] | `git diff --stat utils/volume_progress.py`; `git diff -U0 utils/volume_progress.py` | exactly **2 insertions / 2 deletions**, no hunk outside lines 237–241. If exceeded, §5's conditional obligation fires and a characterization test is required before proceeding. |
| Diagnostic reproduction (before) | `npx pyright@1.1.410 utils/volume_progress.py --outputjson` | 1 `reportAssignmentType` at 1-based 237–240 |
| Diagnostic removal (after) | same | 0 diagnostics in the file |
| Module tests | `.venv/Scripts/python.exe -m pytest tests/test_volume_progress.py -q` | all pass, unchanged count |
| Taxonomy tests | `... -m pytest tests/test_volume_taxonomy.py -q` | all pass (constants untouched) |
| Baseline-diff script tests | `... -m pytest tests/test_pyright_baseline_diff.py -q` | 13 pass. **Label [F5]:** this is a regression guard on the *script*, not validation of the regenerated artifact — every case writes its own `tmp_path` fixtures and none reads `docs/ci_cd_phase3/pyright-baseline.json`. The only real check on the artifact is CI's `Type Check` job. |
| Route/API tests [**corrected** — F6/TS-F1/PR-1] | `... -m pytest tests/test_volume_progress.py tests/test_workout_plan_routes.py -q` | all pass. `/api/volume_progress` is served by `routes/workout_plan.py:69`; its real coverage lives in `tests/test_volume_progress.py:283/305/520`. `tests/test_workout_plan_routes.py` is run as a cheap blueprint-level check despite having no volume assertions. **`tests/test_volume_splitter*.py` is withdrawn** — it cannot reach the edited code. |

### Full

| Gate | Command | Expected |
|---|---|---|
| Pyright net-new gate | `python scripts/pyright_baseline_diff.py --current artifacts/pyright_after.json --baseline docs/ci_cd_phase3/pyright-baseline.json` (pre-regeneration, against the **committed** baseline) | PASS, 0 net-new, current 174 < baseline 175 |
| Baseline regeneration | `npx pyright@1.1.410 --outputjson > artifacts/pyright_after.json` then `--write-baseline` | `_meta` 174 / 50; `git diff` removes exactly the one record |
| Full pytest | `.venv/Scripts/python.exe -m pytest tests/ -q` | green (required by `docs/REFACTOR_PLAN.md:1546`, not by QUALITY_GATE) |
| `/verify-and-polish` | full `/verify-suite` → `code-reviewer` → `unslop-reviewer` → handover | green |

### E2E [reworded in v2 — F3/TS-F3]

**No E2E is *derived* from the changed path** — `docs/ai_workflow/QUALITY_GATE.md:28`
routes `utils/**.py` to pytest only, and the change has no runtime, response-shape, or
template effect. Skipping is also correct on the merits: `e2e/volume-progress.spec.ts`
asserts drawer visibility, geometry and `Active plan: #\d+` (`:76–158`, `:187`), never a
blank-P/S/T numeric total, so it could not catch a regression here even if it ran.

**But the full Chromium suite runs anyway**, because `/verify-and-polish` invokes
`/verify-suite`, whose step 2 is `npx playwright test --project=chromium`. That is a
superset, not a gap — the v1 phrasing "E2E: not required" was correct about derivation
and misleading as an instruction.

**Known reds to apply to that run [added in v2 — F4/TS-F4]**, per
`docs/ai_workflow/QUALITY_GATE.md:121–126`:
- `e2e/program-backup.spec.ts:79` — known DB-state-pollution flake; if it reds, record
  whether it passes in isolation.
- `nav-dropdown.spec.ts` is **no longer** a known red (de-listed 2026-06-11). A red
  there blocks and must not be waived.

### Shared-path and claim declarations [added in v2 — F2]

- `docs/ci_cd_phase3/pyright-baseline.json` is contended between concurrent pyright
  packets. It is claimed for this packet's duration in `MASTER_HANDOVER.local.md`
  (gitignored), per `docs/ai_workflow/WORKSTREAM_OWNERSHIP.md:26–28`.
- `docs/MASTER_HANDOVER.md` is a **never-claimed shared path**
  (`WORKSTREAM_OWNERSHIP.md:33`). This packet **does not edit it**. Handover is recorded
  in the local file only. If the owner wants the committed handover updated, that is a
  separate coordinated edit.
- Also explicitly not edited: `docs/REFACTOR_PLAN.md`, `docs/LEFTOVERS_BY_PRIORITY.md`,
  `docs/test_inventory/**`, any CSS or visual artifact, `utils/volume_taxonomy.py`.

### PR description obligation [added in v2 — PR-5]

`CLAUDE.md` §1 "Refactor invariant" requires migration notes in the PR description for
any change to plan/analyze/distribute behavior. Since §3 proves there is no delta, the
PR description must say so explicitly rather than leave it implicit: *"Local-variable
rename only. No runtime, ordering, rounding, status-classification, diagnostics, API or
schema delta — see `docs/pyright_volume_progress/PLANNING.md` §3."*

### Rebase rule

Rebase onto current `origin/main` **before** the final baseline regeneration, so the
committed baseline reflects the final branch state. If a concurrent pyright packet
lands a reduction, regenerate from the rebased state rather than overwriting its work,
and confirm the diff contains this packet's removal plus only already-merged
reductions.

---

## 7. Council review

The owner stated that the repository explicitly calls for council review when
refactoring `utils/volume_*.py`. **Verified — the rule exists**, in
[`.claude/commands/council-plan.md:15`](../../.claude/commands/council-plan.md):
"When to use … Refactor that touches a calculation engine (`utils/effective_sets.py`,
`utils/weekly_summary.py`, `utils/session_summary.py`, `utils/progression_plan.py`,
`utils/volume_*.py`, `utils/fatigue.py`)." It is **not** in `docs/REFACTOR_PLAN.md`
(whose only `volume_` hits are lines 246 and 642, both unrelated) nor in
`docs/ai_workflow/QUALITY_GATE.md`, so the trigger is the command file. The council is
therefore required by repository rule *and* directly instructed by the owner.

### Agent provenance

**Deviation:** the owner designated one primary session as both manager and
implementation owner, so the `/council-plan` manager/`product-manager` write split was
not used — the primary session authored Plan v1, the response matrix and Plan v2 itself,
and spawned only the three reviewers. Owner confirmed at Gate 1 (2026-08-04).

| Role | Agent ID | Note |
|---|---|---|
| Plan v1 author | *n/a* | Primary session; no `product-manager` spawned, so no ID exists to record |
| Response matrix + Plan v2 author | *n/a* | Same primary session; continuity inherent, not delegated |
| `architecture-reviewer` | `aa1484f8d973ef019` | 7 findings |
| `test-strategist` | `ac77407c27e389e46` | 9 findings |
| `product-risk-reviewer` | `aede2a178e34bb69f` | 5 findings |

No agent ID is unknown or unrecorded; the two authoring IDs do not exist because those
agents were never spawned.

Findings and dispositions: §8. Plan v2: §9.

---

## 8. Council findings and dispositions

21 findings from three reviewers; overlapping findings are merged with all reporters
credited. **Every finding is accepted** — none was rejected or deferred. Each was
independently verified against source before disposition; the verification command and
result are noted where it mattered.

| # | Finding | Reviewer(s) | Sev | Disposition | Action taken in v2 |
|---|---|---|---|---|---|
| F1 | Baseline regenerated under unpinned `npx pyright` (1.1.411) while CI pins `pyright@1.1.410` | architecture, test-strategist | important | **accept** | §1 pins `npx pyright@1.1.410` in every command. **Verified:** ran both; multisets compared through the tool's own key function — `410 == 411 == committed baseline`, 175/51 each. Equality recorded as a measured fact, not assumed forward. |
| F2 | `pyright-baseline.json` is contended shared state but no claim declared; `MASTER_HANDOVER.md` intent unstated | architecture | important | **accept** | §6 gains "Shared-path and claim declarations". Claim recorded in `MASTER_HANDOVER.local.md`; `docs/MASTER_HANDOVER.md` explicitly **not** edited. |
| F3/F8 | §5's "adding a test would red Test Inventory Drift" is factually wrong | architecture, test-strategist | minor | **accept** | Clause deleted. **Verified** against `ci.yml:894–896` + `.claude/rules/testing.md:22`: the fix is regenerate-and-commit, not a blocked gate. §5 now rests on §3.7 alone. |
| F4 | §2.3/§3.6 occurrence enumeration omits `volume_progress.py:225` | architecture, test-strategist | minor | **accept** | `:225` added to both. **Verified** by `grep -n advanced_targets`. Conclusion unchanged (`:225` is inside the branch returning at `:229`), but a proof-by-exhaustion must be exhaustive. |
| F5 | §3.7's ignored-token citation is wrong on line *and* relevance | architecture, test-strategist, product-risk | minor | **accept** | Citation withdrawn. **Verified:** test is at `:396`, builds `primary="Chest"` at `:402`, so it never enters `_aggregate_blank_pst_row`. |
| F6 | §6 route/API row names `tests/test_volume_splitter*.py`, which cannot reach the edited code | architecture, test-strategist, product-risk | important | **accept** | New §2.2 records the real consumer chain; §6 row corrected to `test_volume_progress.py` + `test_workout_plan_routes.py`. **Verified:** splitter test imports no `volume_progress`; `rg` finds only `test_volume_progress.py`. |
| F7 | §7 leans on `council-plan.md` authority while departing from its manager/PM write split | architecture | minor | **accept** | Recorded in the Agent provenance block as a disclosed deviation with an explicit evidence-gap line; surfaced for owner confirmation at Gate 1 rather than settled unilaterally. |
| TS-F3 | "E2E not required" contradicts `/verify-and-polish`, which runs the full Chromium suite | test-strategist | minor | **accept** | §6 E2E section reworded: no E2E *derived*, full suite runs anyway as a superset. Merits of skipping confirmed — the spec asserts geometry, never a numeric total. |
| TS-F4 | §6 omits the known-red list required before any full-suite run | test-strategist | minor | **accept** | Both facts added: `program-backup.spec.ts:79` is a known flake; `nav-dropdown` is de-listed and must block. |
| TS-F5 | `test_pyright_baseline_diff.py` validates the script, not the regenerated artifact | test-strategist | minor | **accept** | Gate row relabelled. **Verified:** all 13 cases use `tmp_path` fixtures; `rg ci_cd_phase3 tests` returns nothing. |
| TS-F9 | The "no new test" conclusion is only valid for a strictly 2-line diff; edit spill into unpinned neighbours would be silent | test-strategist | important | **accept** | New **diff-shape gate** as the first focused gate (exactly 2 ins / 2 del, no hunk outside 237–241), plus a conditional obligation in §5 that fires a characterization test if it is exceeded. |
| PR-1 | §2 inventories the unchanged function and omits the edited one's consumer chain; gate aimed at Distribute not Plan | product-risk | important | **accept** | Merged into F6. §2.2 records the full chain down to `plan_volume_panel.js:218`. |
| PR-3 | §3.4's "diagnostics not touched" contradicts the code — the renamed line *is* the diagnostics-appending call | product-risk | minor | **accept** | §3.4 reworded to the correct claim: call site, kwargs and call order unchanged ⇒ appends identical in content and order. |
| PR-4 | §4's deferred aliasing observation is under-scoped; two more sites alias the same taxonomy lists | product-risk | minor | **accept** | §4 gains a three-row table incl. `volume_splitter_service.py:36–37` and `routes/volume_splitter.py:38–39`. **Verified** — both read-only today, so still latent everywhere. |
| PR-5 | No explicit "no behavior delta" line for the PR body, which `CLAUDE.md` §1 requires | product-risk | minor | **accept** | §6 gains a PR-description obligation with the exact sentence. |
| — | **Self-found while verifying F1:** pyright messages contain U+00A0; reading the baseline without explicit UTF-8 on Windows fabricates 26 phantom key diffs | primary session | minor | **record** | New §1.2. The tool already handles this correctly (`read_text(encoding="utf-8")`, `ensure_ascii=False`) — **no code change**; recorded as a hazard for hand-inspection, since it produced a false alarm in this very plan's first verification pass. |

Reviewer statements accepted as confirmation rather than as findings: all three
independently verified §1's diagnostic identity, §1.1's premise correction, §2.1's
caller inventory, §3.7's primary pin, and §4's rejected-alternatives reasoning
(including that the union alternative would break `.extend` at `:222` and the
re-declaration alternative would trigger `reportRedeclaration`). The
`product-risk-reviewer` additionally scanned and cleared the invariant surface: no
effective-sets, RIR/RPE, weekly/session/progression/fatigue involvement; no schema,
backup, terminology, or non-goal impact; and neither golden-test suite imports this
module, so the shared `GENERATE_GOLDEN` surface is out of blast radius.

---

## 9. Plan v2

No reviewer challenged the diagnosis, the chosen fix, or the decision not to add a
test. **The fix in §4 is unchanged** — the same two-line rename. Every accepted finding
corrected the *evidence and gates* around it; §8's "Action taken in v2" column is the
per-finding record, and the inline `[… in v2 — F#]` markers show where each landed.

### 9.1 Expected result

| Measure | Before | After |
|---|---|---|
| `reportAssignmentType` in `utils/volume_progress.py` | 1 | 0 |
| `reportAssignmentType` repo-wide | 1 | 0 (family eliminated) |
| Baseline `_meta.total_diagnostics` | 175 | 174 |
| Baseline `_meta.distinct_keys` | 51 | 50 |
| Any other diagnostic key or count | — | unchanged |
| Runtime values, ordering, calculations, API, DB | — | unchanged |

### 9.2 Measured results

| Gate | Result |
|---|---|
| Focused pyright on `utils/volume_progress.py`, before → after | 1 → **0** diagnostics |
| Diff-shape gate (TS-F9) | **2 insertions / 2 deletions**, hunks only at 237 and 241 — conditional test obligation did not fire |
| Net-new gate vs the **committed** baseline, before regenerating | PASS, 0 net-new, 175 → 174 |
| Regenerated baseline | `_meta` 174 / 50; `git diff` = one record removed + two `_meta` counts, nothing else |
| CI gate re-simulated on the committed tree | PASS, 174 == 174 |
| Focused pytest (4 files) | 119 passed |
| Full pytest | **2527 passed, 2 skipped** |
| Test Inventory Drift | up to date (no regeneration needed) |
| flake8 blocking set on the changed file | clean |
| `code-reviewer` | clean on all five charter rules |
| `unslop-reviewer` | production code clean |
| CI on PR #299 | **17/17 checks pass**, including the blocking `Type Check` baseline gate |

#### Full Chromium E2E — 81 failures, all attributed to inherited state

The full local suite returned **507 passed / 81 failed**. Every failure was traced; none
is caused by this packet.

| Group | Count | Attribution |
|---|---|---|
| `visual.spec.ts` + `visual-baseline-thumbnails.spec.ts` | 65 | **Operator error**: the run omitted `PW_VISUAL_SEED=1`. `docs/ai_workflow/QUALITY_GATE.md:39` states that without it the matrix fails en masse on a page-height data difference "on unmodified CSS too". This packet changes no CSS, template, or JS. |
| `workout-plan-desktop-contract.spec.ts` | 10 | **Inherited from `f8988f9`** (PR #298), the commit this branch rebased onto, which introduced the spec. Proven by control — see below. |
| `volume-progress.spec.ts` (`:208`, `:479`) | 2 | **Serial-run DB pollution.** Re-run in isolation from a fresh seed: **16/16 passed.** |
| `exercise-interactions`, `validation-boundary` ×2, `workout-log` | 4 | **Serial-run DB pollution.** Re-run in isolation from a fresh seed: all passed (73 passed across the group). |

**The `workout-plan-desktop-contract` control.** Isolated runs of that spec alone, from
an identically fresh-seeded DB, with only `utils/volume_progress.py` differing:

| Tree state | Result |
|---|---|
| This packet's change present | **16 failed** |
| This packet's change reverted to `f8988f9` (`git checkout f8988f9 -- utils/volume_progress.py`) | **16 failed** |

Identical. The spec is red at main on this Windows machine independently of this packet.
It is **not** this packet's to fix — the branch owns no `e2e/**`, template, CSS, or JS
path — and it is recorded here rather than silently absorbed. CI's own E2E jobs
(Functional shards 1/2 and 2/2, Smoke, Backup, Erase, Fatigue Context) are all green on
PR #299, which is the gate that governs merge.

### 9.3 Sign-off

Gate 0 not applicable (requirements and non-goals fully specified by the owner).

- [x] **Gate 1 — owner approved Plan v2, 2026-08-04**, with the instruction to keep the
  change confined to the two-line rename, not to modify `_mode_muscles()`, and to
  continue autonomously through verification, PR and CI.
