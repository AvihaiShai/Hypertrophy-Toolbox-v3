# Plan Review — QUALITY_GATE.md routing: `scripts/**` row + the two unnamed blocking CI gates

*Planning size: **Medium** → Gate 1 only. Section 0 is deliberately absent and **Gate 0 is not claimed**; the owner scoped and approved this packet for planning, and what is unapproved is the plan below.*

*Scope is owner-locked to canonical routing documentation in `docs/ai_workflow/QUALITY_GATE.md`. No workflow, test, branch-protection, or job-name change is in scope.*

---

## Plan v1

**Goal**: Make the gates for a `scripts/**` change mechanically derivable instead of a judgement call, and name the two required CI checks that block merges today but appear nowhere in `QUALITY_GATE.md`'s change-type table.

**Scope**

- **In**
  - One new row in the change-type → gates table covering `scripts/**`.
  - One new bullet in the **Targeted-test derivation** list matching that row.
  - One new subsection naming `Test Inventory Drift` and the blocking pyright baseline-diff step inside `Type Check (tsc blocking + pyright measure-only)`, including prose that resolves the misleading job name **without** renaming anything.
  - All three land in `docs/ai_workflow/QUALITY_GATE.md`, and nowhere else.

- **Out**
  - `.github/workflows/ci.yml` — not edited. This packet documents gates that already exist and already block.
  - Any rename of any CI job, any branch-protection edit, any change to what a gate does or to its pass/fail threshold.
  - Any test file, any script under `scripts/`, and `docs/test_inventory/`.
  - Adding test coverage for the ~half of `scripts/` that has none (measured below). That is a real finding, but it is a code packet, not this documentation packet.
  - Re-baselining pyright or regenerating the test inventory.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `docs/ai_workflow/QUALITY_GATE.md` | modify | The only file this packet writes. Three additions, no deletions, no rewording of existing rows. |
| `docs/quality_gate_routing/PLANNING.md` | new (this file) | Plan artifact; not part of the shipped diff's behavior surface. |

**Effort**: S · **Owner**: implementing agent after Gate 1 · **Depends on**: nothing. No packet is blocked by it either — it records existing behavior.

---

### Proposed text 1 — the change-type table row

Insert **after** the `E2E spec` row and **before** the `AI workflow / agent config` row, verbatim:

```markdown
| Tooling / scripts | `scripts/**` | Every test that names the changed path or its parent directory (see Targeted-test derivation). If none exists, `/verify-suite`. Editing `scripts/generate_test_inventory.py` additionally requires re-running it and committing `docs/test_inventory/`; adding or removing any file under `scripts/css_audit/` additionally requires `tests/test_css_theme_dark_p3_audit_contracts.py` | `code-reviewer` |
```

### Proposed text 2 — the Targeted-test derivation bullet

Insert into the **Targeted-test derivation** list, after the `static/css/**` bullet and before the `app.py, tests/conftest.py, root configs` bullet, verbatim:

```markdown
- `scripts/**` (any depth) → search `tests` for the changed path **and for each parent directory prefix**: `rg -F "scripts/X.py" tests`, then `rg -F "scripts/<subdir>/" tests`. Take the union of every test module that names any of them. Do **not** derive from the filename alone — most scripts have no `tests/test_<script>.py` twin, and a newly added file inside an audited directory is caught only by the directory prefix, never by its own name
```

The parent-prefix clause is the load-bearing half. `tests/test_css_theme_dark_p3_audit_contracts.py` asserts against the *directory* `scripts/css_audit/`, so a filename-only grep for a brand-new tool returns nothing precisely when that tool is the thing that reds the contract.

### Proposed text 3 — the blocking CI gates subsection

Insert as a new subsection immediately **after** the change-type table (and after the two existing block quotes that follow it), before `## Diff collection`, verbatim:

```markdown
## Blocking CI gates the change-type table does not derive

Two required checks fail on changes no row above routes to. Neither is derivable
from a changed path, so both are named here rather than in a row.

| Check name (branch protection, verbatim) | What actually blocks | Fix when it reds |
|---|---|---|
| `Test Inventory Drift` | `scripts/generate_test_inventory.py --check` against the committed `docs/test_inventory/`. Blocking since 2026-08-01. The inventory pins **per-file** node counts, so adding, removing, renaming, or moving a single test between files reds it. | Run `python scripts/generate_test_inventory.py` and commit the regenerated artifact. Never hand-edit the artifact, and never edit the workflow. |
| `Type Check (tsc blocking + pyright measure-only)` | **Two** blocking steps, despite the name. `tsc --noEmit` must report zero errors. Separately, `scripts/pyright_baseline_diff.py` fails on net-new pyright diagnostics against `docs/ci_cd_phase3/pyright-baseline.json`. Only the pyright *count* step is measure-only; the baseline diff beside it is not. | Fix the net-new diagnostic. Re-baselining to make it pass is an owner decision, not a repair. |

**The pyright job's name understates what it enforces, and the name stays anyway.**
"measure-only" is accurate for the count step and wrong for the job. The label is
frozen under the CI job naming rule below: this job sits in branch protection, so
renaming it orphans the required context and every PR then blocks on a check that
will never report again. Correct the understanding here; do not correct the label.
```

---

**Sequence**

1. Re-read `QUALITY_GATE.md` and confirm the three insertion points still match the text quoted above (this plan pins them by neighbouring row, not by line number, because line numbers drift).
2. Apply proposed text 1, 2, and 3. No other edit to the file — in particular, leave every existing row's wording byte-for-byte alone.
3. Confirm the three substrings pinned by `tests/test_consult_adapter.py::test_the_canonical_planning_gates_still_trigger` are still present: `## Plan-stage routing`, `Gate 0 (requirements approval) + Gate 1 (council-reviewed plan approval)`, `Run the union, never the weaker set.`
4. Run the two derived pytest modules (below). Do not regenerate `docs/test_inventory/` — this packet adds no test node.
5. Manual dry-run/self-review, then `code-reviewer`.

**Expected gates** *(proposer's derivation — no `test-strategist` ran; a council was not delegated for this Medium packet)*

- pytest: `tests/test_agent_workflow_contracts.py` — parametrizes over `docs/ai_workflow/*.md`, so it asserts directly against the edited file. `tests/test_consult_adapter.py` — pins three QUALITY_GATE.md substrings at lines 1067-1070.
- e2e: none.
- other: manual dry-run/self-review + `code-reviewer`, per the `AI workflow / agent config` row.
- **Not** required: full `pytest`, test-inventory regeneration, `/build-css`, any visual matrix.

Note that the `AI workflow / agent config` row's "run tests only if source behavior changed" reads as *no tests* for a documentation edit. That is wrong for this file: `docs/ai_workflow/QUALITY_GATE.md` is under assertion by two test modules. The two pytest targets above are genuinely required, and step 3 exists because a careless edit to this file can red pytest.

---

## What the new row actually changes — tightening, loosening, and current practice

This is the part most worth the owner's attention, because the honest answer is **all three at once**, in different directions for different files.

**Today, `scripts/**` matches no row.** Verified: `scripts` appears in `QUALITY_GATE.md` only twice, both times as a command to invoke (`node scripts/css_audit/stylelint_surfaces.mjs`) and never as a changed-path glob. `scripts/**` is not `docs/**` and there are no `.md` files anywhere under `scripts/`, so the `Product docs only` row does not catch it either. That row's "none unless examples/scripts changed" gestures at scripts without routing them.

**So the currently *documented* gate for a scripts-only change is the full `/verify-suite`** — via "Run the union. If the union is empty, run `/verify-suite`." A changed file matching no bullet contributes nothing to the union; if it is the only changed file, the union is empty.

Against that documented baseline:

| Direction | Which files | Effect |
|---|---|---|
| **Loosens** | The 12 top-level scripts that a test already names (e.g. `run-playwright.ps1`, `apply_youtube_curated.py`, `stage_package_assets.py`) | Documented gate drops from full `/verify-suite` (full pytest + full Chromium E2E) to one or two targeted modules. |
| **No change** | The 14 top-level scripts no test names at all (including `pyright_baseline_diff.py`, `new-worktree.ps1`, `stylelint-report.mjs`, `playwright_timing_report.py`) | Grep finds nothing, union stays empty, `/verify-suite` still applies. The preserved fallback is what keeps this honest. |
| **Tightens** | Any packet adding or removing a file under `scripts/css_audit/`; any packet editing `scripts/generate_test_inventory.py` | Newly *required* to run something it is not required to run today. |

**Packet shapes newly required to run something they do not run today:**

- **A packet that adds a tool to `scripts/css_audit/`.** `tests/test_css_theme_dark_p3_audit_contracts.py::test_every_committed_css_audit_tool_is_assessed` fails on any unassessed file in that directory. A targeted-diff packet today can plausibly skip it — the existing record is that only a full pytest run surfaces this. The new row makes it derivable and therefore mandatory.
- **A packet editing `scripts/generate_test_inventory.py`.** Newly must re-run the generator, commit `docs/test_inventory/`, and run `tests/test_agent_workflow_contracts.py` (which reads that script's `ENVIRONMENT_DEPENDENT_PYTEST_FILES` behavior as part of its own node-count determinism reasoning).

**And a candid caveat on "records current practice".** For the 12 covered scripts the row is closer to recording what is actually done than to changing it — nobody plausibly runs a full `/verify-suite` for a one-line edit to a reporting script. The *documented* rule and the *practised* rule have diverged, and this row resolves the divergence in favour of practice. That is a real loosening of the written standard even though it is unlikely to change anyone's behavior. **Choosing that direction is the owner's call at Gate 1**, and the alternative — keeping `/verify-suite` mandatory for all of `scripts/**` and writing the row to say so — is a one-line change to proposed text 1 if the owner prefers it.

---

## Measured evidence (verified in this worktree, not carried from the brief)

Two figures in the task brief did not survive verification. Both corrections are minor and neither changes the plan's shape:

- **`scripts/` holds 26 top-level files** (brief said 25), plus `scripts/css_audit/` (22 files) and `scripts/consult/` (3 files).
- **13 test modules reference `scripts/`** (brief said 12). A 14th match, `tests/fixtures/consult/fake_cli.py`, is a fixture rather than a test module.

**The "contracts test named after the script" convention is weaker than the brief describes, and the difference matters.** Exact-name twins exist for only **2 of 26** top-level scripts (`apply_free_exercise_db_mapping.py`, `fatigue_stage4_observer.py`). The dominant real pattern is a test named after the *contract*, not the script — `apply_youtube_curated.py` → `test_youtube_video_id.py`; `build_musclemap_svgs.py` → `test_muscle_selector_mapping.py`; `smoke_packaged_app.py` → `test_static_cache_policy.py`; `stage_package_assets.py` → `test_packaging_contract.py`; `generate_test_inventory.py` → `test_agent_workflow_contracts.py`. **A name-first derivation rule would resolve for 2 of 26 files, which is why proposed text 2 is grep-first.**

Verified pairs from the brief: `scripts/consult/consult.py` → `tests/test_consult_adapter.py` (confirmed), `scripts/css_audit/**` → `tests/test_css_theme_dark_p3_audit_contracts.py` (confirmed), `scripts/run-playwright.ps1` → `tests/test_playwright_runner_contracts.py` (confirmed). One the brief did not name: `scripts/run-playwright-shards.ps1` → `tests/test_playwright_shard_launcher_contracts.py`.

**One brief example does not hold.** `.claude/hooks/guard-destructive-command.ps1` → `tests/test_guard_destructive_command.py` is a real pair, but it is not a `scripts/**` mapping: that test's subject is the hook, and the `scripts/...` strings inside it are sample command inputs. Three of them — `scripts/run.sh`, `scripts/x.ps1`, `scripts/new-worktree.sh` — do not exist on disk. Grepping for a script path will still surface this module for `run-pytest.ps1` and `run-playwright.ps1`, which is harmless but is coincidence rather than convention.

**Both CI gates verified as genuinely blocking** in `.github/workflows/ci.yml`: the `pyright baseline diff (blocking)` step (line 915) carries **no** `continue-on-error`, unlike the `pyright (measure-only count)` step above it (line 899) which does; and `Test Inventory Drift` (job `test-inventory`, name at line 1108) captures `$STATUS` and exits non-zero on drift.

**Not independently re-derived:** the "branch protection requires 11 contexts" figure. `QUALITY_GATE.md` already records it as re-derived 2026-08-04 from `gh api repos/:owner/:repo/branches/main/protection`, and proposed text 3 does not restate the number, so nothing new depends on it. If the owner wants that figure refreshed, it is a separate `gh` call and not a documentation change.

**Deliberately kept out of the proposed text: hard counts.** An earlier draft of proposed text 2 said "only 2 of the 26 top-level scripts". That number is correct today and goes stale the moment anyone adds a script, with no test guarding it. The evidence lives here in the plan; the canonical file gets the durable phrasing instead.

---

## Two hazards the implementer must respect

1. **`docs/ai_workflow/**` is an asserted test surface.** `tests/test_agent_workflow_contracts.py` parametrizes over `docs/ai_workflow/*.md` and fails on the retired `Tier <digit>` / `Appendix A<digit>` numbering and on any `SHARED_PLAN` reference. The proposed text above contains none of these — confirm that again after any Gate 1 rewording.
2. **`tests/test_consult_adapter.py` pins QUALITY_GATE.md substrings.** Three exact strings (listed in Sequence step 3). All three sit in sections this packet does not touch, but a reflow or a "while I'm here" tidy would red pytest.

---

## Self-routing note

This packet's own change type is **`docs/ai_workflow/**`**, so by the table it is routed to *manual dry-run/self-review plus `code-reviewer`*, and no E2E. The mild awkwardness is worth stating plainly: **this packet is routed by the very table it edits.** It is not circular in a way that invalidates anything — the row governing it (`AI workflow / agent config`) is not one of the rows being changed, and the packet adds no row that would re-route itself. But it does mean the packet cannot use its own new `scripts/**` row as evidence that the new row works; the first real exercise of that row will be the next packet that touches `scripts/`.

The one place the existing routing is actually inadequate for this packet is the "run tests only if source behavior changed" clause, which understates the two pytest modules that assert against this file. This plan runs them anyway rather than proposing a fix to that clause, which is out of the owner-locked scope.

---

## Agent provenance

*A three-reviewer council ran against Plan v1. All three returned `REVISE`.*

The reviewers ran as real subagents and returned real agent IDs. Those IDs are session-internal harness identifiers that must not be reproduced outside the session, so each reviewer row records **run evidence** — tool calls, tokens, wall-clock duration, verdict — in place of the ID. This is a deliberate substitution of one accurate record for another, **not** an unrecorded ID: nothing here is invented, and no row reads `unknown — not recorded`, because nothing was in fact unrecorded.

| Role | Run evidence | Notes |
|---|---|---|
| `product-manager` — Plan v1 | this agent | Author of Plan v1. Section 0 deliberately not written (Medium → Gate 1 only). |
| `product-manager` — response matrix + Plan v2 | this agent, resumed | Same agent, same session, resumed via `SendMessage`. |
| `architecture-reviewer` | 24 tool calls · 84,190 tokens · 354 s · `REVISE` | Step 2 reviewer. Output pasted verbatim below. |
| `test-strategist` | 28 tool calls · 114,312 tokens · 447 s · `REVISE` | Step 2 reviewer. Output pasted verbatim below. |
| `product-risk-reviewer` | 22 tool calls · 61,033 tokens · 245 s · `REVISE` | Step 2 reviewer. Output pasted verbatim below. |

**Same product-manager resumed for the matrix + Plan v2?** **`yes`** — resumed via `SendMessage` to the Plan v1 agent. This is genuine continuity, not a reconstruction: the same agent that drafted Plan v1 wrote the response matrix and Plan v2 in the same session, with the Plan v1 reasoning still in context. No fresh `product-manager` read the artifact cold, and no completed council work was rerun to manufacture continuity.

**Artifact ownership.** Unlike the cross-model packet, this artifact sits at the canonical `docs/<feature>/PLANNING.md` path, which is inside the `product-manager` write boundary — so the guard permitted the author to own the file directly and **no author bypass was needed**. That is the shape the next packet should make canonical.

**Evidence gap**: `none` for continuity. One deliberate substitution is recorded above: reviewer agent IDs were returned by the harness and are known, but are session-internal and are therefore represented by run evidence rather than reproduced. No ID was invented, and no ID that was recorded has been discarded or downgraded to `unknown — not recorded`.

---

## Reviewer findings

*Council step 2 — three agents in parallel. Each output is pasted verbatim and unsummarised.*

### architecture-reviewer (run evidence: 24 tool calls · 84,190 tokens · 354 s · `REVISE`)

````markdown
## Findings, ranked

**1. `docs/quality_gate_routing/PLANNING.md:113` — the "no test names it at all" bucket is factually wrong about `scripts/pyright_baseline_diff.py`, and it is wrong via the exact failure mode the plan exists to fix.**

`tests/test_pyright_baseline_diff.py:13` reads `from scripts.pyright_baseline_diff import (baseline_to_counts, counts_from_diagnostics, counts_to_baseline, find_regressions, main)` — a dedicated, exact-name twin module whose docstring says it "Covers the contract the CI gate relies on". The plan lists that script as one of "The 14 top-level scripts no test names at all". It is missed because `rg -F "scripts/pyright_baseline_diff.py" tests` returns nothing: the test imports the dotted module path, never the slash path.
- Risk: the loosening/tightening partition is the owner's Gate 1 decision input (`PLANNING.md:183`), and one of its four named "uncovered" examples is the script implementing one of the two gates this packet documents. The plan's evidence was produced by the rule it proposes, and the rule produced a false negative on its own subject matter.
- Fix: re-derive the partition with a separator-agnostic pattern and correct `PLANNING.md:112-113` and `:132`.

**2. `PLANNING.md:52` — proposed text 2's `rg -F` slash-form search has systematic false negatives; several real script↔test bindings are invisible to it.**

Measured in this worktree:
- `tests/test_packaging_contract.py:67` `"from scripts.stage_package_assets import staged_datas"` and `:82` `"scripts\\stage_package_assets.py"` (backslash). No forward-slash form exists anywhere in `tests/` — yet `PLANNING.md:112` lists `stage_package_assets.py` among the 12 "a test already names".
- `tests/test_package_asset_staging.py:12` — dotted form.
- `tests/test_css_theme_dark_p3_audit_contracts.py:37` `from scripts.css_audit import measure, p3_ceiling`; `:700` uses `ROOT / "scripts" / "css_audit"`. The directory grep hits **only** because of a docstring at `:688` (` ``scripts/css_audit/`` `). Reword that docstring and the parent-prefix clause goes silent while `test_every_committed_css_audit_tool_is_assessed` (`:685`) still asserts — precisely the failure the clause was written to prevent.
- Risk: the row's `/verify-suite` fallback is only protective if the search deciding "none exists" is reliable. As drafted it is not, and the plan's own covered/uncovered table is not reproducible from it.
- Fix: drop `-F` and make the separator a character class, e.g. `rg -n "scripts[/.\\\\]<name>" tests`.

**3. `PLANNING.md:52` — "for each parent directory prefix" is unbounded and contradicts the plan's own impact table.**

For `scripts/new-worktree.ps1` the only parent-directory prefix *is* `scripts/`. Applied literally, `rg -F "scripts/" tests` returns ~13 modules and the union is never empty — but `PLANNING.md:113` asserts that for those files "Grep finds nothing, union stays empty, `/verify-suite` still applies."
- Risk: an agent following the canonical text gets a different, broader targeted set; an agent following the plan's table gets the full suite. Two readers derive opposite gates from the same packet.
- Fix: bound the clause to directories strictly below `scripts/` — "for a file at `scripts/<subdir>/…` also search `scripts/<subdir>`; never search the bare `scripts/` prefix."

**4. `PLANNING.md:64-65` — proposed text 3 opens with a claim its own table refutes.**

"Neither is derivable from a changed path" sits four lines above `:69` "adding, removing, renaming, or moving a single test between files reds it" — which is a changed-path derivation (`tests/**`). Same for pyright: net-new diagnostics arrive with changed `.py` files.
- Risk: the table still has no `tests/**` row, so the most common way to red `Test Inventory Drift` (a packet that adds a test node) stays unrouted, and this sentence tells the reader to stop looking for a trigger.
- Fix: say "neither is *narrowly* path-scoped, so both are named here rather than duplicated into every row", and state the two real triggers.

**5. `PLANNING.md:67` vs `.github/workflows/ci.yml:1099-1102` — text 3's column header asserts branch-protection membership that ci.yml's own comment denies.**

`ci.yml:1099-1102`: "The name carries no `(non-required)` suffix. This job is not in branch protection, so it was renamed freely". `QUALITY_GATE.md:114-119` already supersedes that ("re-derived 2026-08-04 … branch protection requires **11** contexts and `Test Inventory Drift` is one of them"), but the stale comment survives, and text 3's header column reads "(branch protection, verbatim)".
- Risk: a reader reconciling the two "fixes" the wrong side — worst case by renaming a required context, the exact hazard `QUALITY_GATE.md:89-93` exists to prevent.
- Fix: one sentence in text 3 recording the `ci.yml` comment as known-stale and out of scope, or a line in **Out** naming it as a follow-up.

**6. `PLANNING.md:19` — "and nowhere else" understates the effect on two documented consumers.**

`.claude/commands/unslop.md:16-20` and `.claude/agents/test-strategist.md:20-27,56` carry abbreviated copies of the derivation list. Both defer to QUALITY_GATE.md as canonical, so this is not a contract break — but `test-strategist.md:56` ("no map hit — propose `<spec>` or run `/verify-suite`") will keep routing scripts-only changes to the full suite after the canonical file says targeted.
- Risk: low functional, but the plan does not mention either file, so the divergence lands undeclared.
- Fix: one line recording both as knowingly not updated (outside the owner-locked scope) and why the divergence is safe.

**7. `PLANNING.md:132` — the "2 of 26 exact-name twins" membership is wrong (the count survives by coincidence).**

`apply_free_exercise_db_mapping.py`'s test is `tests/test_free_exercise_db_mapping.py` (no `apply_`); `tests/test_apply_free_exercise_db_mapping.py` does not exist, so it is not an exact twin. The real second twin is `pyright_baseline_diff.py` (finding 1). Also, at least **14** top-level scripts are named by a test in some form, not 12.
- Risk: the plan flags these as "verified in this worktree, not carried from the brief" (`:125`), which raises the cost of the error.
- Fix: swap the membership and re-state the split.

**8. `PLANNING.md:119` — `tests/test_agent_workflow_contracts.py` does not assert on `generate_test_inventory.py`.**

Both hits (`tests/test_agent_workflow_contracts.py:69` and `:102`) are **comments**; nothing in that module fails if `ENVIRONMENT_DEPENDENT_PYTEST_FILES` changes. The grep rule will pull it into the union anyway — over-inclusion, which is the safe direction, but the plan describes it as coverage.
- Risk: the same conflation makes `run-pytest.ps1` and `generate_test_inventory.py` look "covered" when the only hits are sample inputs and prose.
- Fix: say the grep hits a comment and the module joins by over-inclusion; state plainly that the rule cannot distinguish coverage from a mention.

**9. `PLANNING.md:104` — minor internal contradiction in the "matches no row" evidence.**

"`scripts` appears in `QUALITY_GATE.md` only twice, both times as a command to invoke". Verified count is 2 (`QUALITY_GATE.md:32`, `:35`), but `:35` is `none unless examples/scripts changed` — prose, not a command, as the plan's own next sentence concedes. The load-bearing conclusion (never a changed-path glob) is correct.

## The central claim

**The plan is right.** `QUALITY_GATE.md:26-35` contains no `scripts` glob; `:57-62` contains no `scripts` derivation bullet; and the Plan-stage carve-out at `:18-20` exempts only "a docs-only change whose row explicitly requires no tests", which `scripts/**` is not. So `:64` "Run the union. If the union is empty, run `/verify-suite`" is the operative rule today, and a targeted row does loosen the written standard. The plan states this against itself rather than hiding it (`:106`, `:121`), which is the right call.

**Is the loosening safe?** Conditionally — and the condition is findings 2 and 3. The fallback only protects if the search that decides "none exists" is trustworthy; as drafted it demonstrably returns nothing for two scripts that do have tests, and its parent-prefix half survives on a docstring. Fix the separator handling and bound the prefix clause and the loosening is safe, because the fallback then genuinely covers the uncovered set. The other thing that would make it safe is already present and should stay: the `/verify-suite` fallback inside the row itself, not just in the derivation list.

## Self-reference

Handled honestly. `PLANNING.md:153-157` correctly identifies that the packet is routed by `AI workflow / agent config` (`QUALITY_GATE.md:34`), that this row is not one it edits, and that the packet cannot cite its own new row as evidence. Its declared gates are correct and verified:
- `tests/test_agent_workflow_contracts.py:84` globs `docs/ai_workflow/*.md` into `SURFACE`, parametrized by `:139` and `:163` — QUALITY_GATE.md is under assertion. The proposed text contains no `Tier <digit>`, `Appendix A<digit>`, or `SHARED_PLAN`, so it complies.
- `tests/test_consult_adapter.py:1067-1070` pins exactly the three substrings the plan quotes, at exactly the cited lines.
- "adds no test node, do not regenerate the inventory" (`:86`) is correct — the packet adds no file under `docs/ai_workflow/`, so `SURFACE`'s node count is unchanged.

One touchpoint the plan misses, harmlessly: `tests/test_consult_adapter.py:617` passes `docs/ai_workflow/QUALITY_GATE.md` as an allowed artifact path. Path-only, content-independent — no gate, but worth knowing so a third grep hit does not surprise the implementer.

## Staleness / hard-coded numbers

Clean, and deliberately so. `PLANNING.md:142` keeps "2 of 26" out of the canonical file because nothing guards it; `:140` declines to restate the "11 contexts" figure. Both are correct calls and I would not change them. The only hard-codes left in text 3 are two file paths (`scripts/pyright_baseline_diff.py`, `docs/ci_cd_phase3/pyright-baseline.json`) and one durable date. No action needed.

## Charter items not applicable

No module boundaries, blueprint triple, schema creator, `DatabaseHandler`, response contract, logger, or normalization surface — this packet writes one Markdown file. The shared-state edit to a canonical authority document is declared explicitly at `PLANNING.md:5`, `:19`, and `:32`, which satisfies the ownership rule.

Plan shape, scope discipline, insertion anchors, and self-routing are sound. What needs revision is the evidence table (findings 1, 7, 8) and the followability of the derivation rule that is the packet's main deliverable (findings 2, 3).

REVISE
````

### test-strategist (run evidence: 28 tool calls · 114,312 tokens · 447 s · `REVISE`)

````markdown
# Plan review — `docs/quality_gate_routing/PLANNING.md` (`wt/quality-gate-routing`)

Reviewed cold against the worktree at `D:\development\Hypertrophy-Toolbox-v3-main-cross-model-tier1`. Everything below is measured in that checkout.

---

## Required gates

```
## Required gates
- pytest: tests/test_agent_workflow_contracts.py, tests/test_consult_adapter.py::test_the_canonical_planning_gates_still_trigger
- e2e:    none
- other:  none. No inventory regeneration, no /build-css, no visual matrix.
```

The plan's Expected-gates block is **correct and complete** for the diff it describes. Both claims verified:

- `tests/test_agent_workflow_contracts.py:80-86` builds `SURFACE` from `(REPO / "docs" / "ai_workflow").glob("*.md")`, parametrized at `:138` and `:158-161`. `QUALITY_GATE.md` is therefore under two nodes.
- `tests/test_consult_adapter.py:1068-1070` holds the three substrings (the plan cites "1067-1070"; 1067 is the `read_text`, the asserts are 1068/1069/1070).
- `rg QUALITY_GATE tests` returns exactly one file (`test_consult_adapter.py`); `rg ai_workflow tests` returns exactly two. Nothing else in `tests/` reads either path.

**No other test reds on this diff.** No `.py`/`.ts` change, so the pyright baseline diff and `tsc` cannot move. The new planning artifact lives at `docs/quality_gate_routing/PLANNING.md`, which is **not** inside any glob in `SURFACE` — so no node is added and the plan's Sequence step 4 ("do not regenerate `docs/test_inventory/`") is right. The plan does not state *why* it is right, and the reason is load-bearing (see gap G5 below).

Two additions I would require in the Sequence:

- `/handover`. Steps stop at `code-reviewer`. `CLAUDE.md` and `.claude/commands/unslop.md:23` both make handover the terminal step.
- A grep of the proposed text against `RETIRED_NUMBERING` (`test_agent_workflow_contracts.py:92`, `\bTier \d|\bAppendix A\d`) and `SHARED_PLAN`. I checked all three blocks: clean. Hazard §1 already says this; it should be a Sequence step, not a note.

---

## Walking three real paths through proposed text 2

Proposed rule (`PLANNING.md:52`): `rg -F "scripts/X.py" tests`, then `rg -F "scripts/<subdir>/" tests`, take the union; if empty → `/verify-suite`.

**Path 1 — `scripts/consult/consult.py`. Resolves, but by luck.**
`rg -F "scripts/consult/consult.py" tests` hits `tests/test_consult_adapter.py:982`. Correct module, and the only one. But that hit is a *string inside an assertion's file list*, not the dependency: the actual coupling is `CONSULT_DIR = REPO / "scripts" / "consult"` (`:35`) and `sys.path.insert(0, str(REPO / "scripts"))` (`:42`), neither of which contains the literal `scripts/consult`. Delete the file-list assertion and the rule goes blind on the one script that has a dedicated 1000-line test module.

**Path 2 — a brand-new `scripts/css_audit/new_tool.mjs`. Fails, and this is the worst case.**
`rg -F "scripts/css_audit/" tests` returns exactly one module — `tests/test_css_theme_dark_p3_audit_contracts.py`, matched at `:688` and `:1012`, both **docstring prose**. The assertions that actually enumerate the directory are at `:700` and `:744` (`(ROOT / "scripts" / "css_audit").iterdir()`) and would not match. Meanwhile the rule misses every other dependent of that directory:

- `tests/test_css_audit_digest_normalization_contracts.py:30` — `ROOT / "scripts" / "css_audit" / "j_known_live_mutation.mjs"`
- `tests/test_playwright_url_contracts.py:35` — `REPO / "scripts" / "css_audit" / "runtime_probe.mjs"`
- `tests/test_css_wp4_4_a_baseline_contracts.py:32` — `from scripts.css_audit import measure, specificity`
- `tests/test_css_wp4_4_i_is_repair_contracts.py:238` — `sys.path.insert(0, str(ROOT / "scripts"))`

This is **true under-gating**, not over-gating: the union is non-empty, so the `/verify-suite` fallback never fires. An agent editing `scripts/css_audit/measure.py` under this rule runs one contract file and ships a break in `test_css_wp4_4_a_baseline_contracts.py`. `scripts/css_audit/` is the most-tested subtree in `scripts/` and the rule finds one of five dependents.

**Path 3 — `scripts/new-worktree.ps1`. The rule contradicts the plan's own evidence.**
The filename grep is empty. The prose says "for **each** parent directory prefix" — for a top-level script the only parent prefix is `scripts/`, and `rg -F "scripts/" tests` hits ~13 files including `test_catalog_invariants.py`, `test_youtube_video_id.py`, `test_muscle_selector_mapping.py`. Under that reading the agent runs a large, irrelevant union and — crucially — never reaches the fallback. Under the narrower "`scripts/<subdir>/` only" reading (the example given), the union is empty and `/verify-suite` applies, which is what `PLANNING.md:113` asserts. **The proposed text and the plan's own Loosens/No-change table disagree about what the rule does for every top-level script.** A future agent will pick whichever reading is convenient.

**The root cause, and the fix.** The rule greps a *slash path*. The dominant idiom in this repo is `ROOT / "scripts" / "x" / "y.py"` and `from scripts.x import y` — neither contains a forward slash. Grepping the **stem** and the **directory token** resolves every failure above:

| Changed path | `rg -F "scripts/..."` (proposed) | `rg -F "<stem>" tests` (works) |
|---|---|---|
| `scripts/pyright_baseline_diff.py` | nothing | `tests/test_pyright_baseline_diff.py:13` |
| `scripts/stage_package_assets.py` | nothing | `tests/test_package_asset_staging.py:12`, `tests/test_packaging_contract.py:67,82` |
| `scripts/wait_for_clean_start.ps1` | nothing | `tests/test_playwright_shard_launcher_contracts.py:150` |
| `scripts/shard_telemetry.ps1` | nothing | `tests/test_playwright_shard_launcher_contracts.py:162` |
| `scripts/playwright_timing_report.py` | nothing | `tests/test_playwright_runner_contracts.py:164` |
| `scripts/css_audit/*` | 1 of 5 modules | `rg -F "css_audit" tests` → all 5 |

The plan's conclusion — "grep-first, not name-first" — is right in spirit and wrong in mechanism. It conflates *the `tests/test_<script>.py` naming convention* (correctly rejected, 2 of 26) with *grepping the basename* (which is what actually works). Rewrite the bullet as: grep the file stem and the parent directory name, path-separator-free; only then fall back.

**Glob ambiguity.** "`scripts/**` (any depth)" does not say whether it is anchored at the repository root. `e2e/scripts/` exists (`build_visual_seed.py`, `prepare_e2e_db.py`, `prepare_visual_db.py`, `seed_summary_regression_db.py`) and is already claimed by the `E2E spec` row (`QUALITY_GATE.md:33`), whose gate ("run the spec") would miss `tests/test_visual_capture_contracts.py:42-43` and `tests/test_packaging_contract.py:102`. The table states no precedence rule for two matching rows. Anchor the glob.

---

## The loosening claim

**Verified, with one correction.** `scripts` appears in `QUALITY_GATE.md` exactly twice — `:32` (`node scripts/css_audit/stylelint_surfaces.mjs`) and `:35` ("none unless examples/scripts changed"). Neither is a changed-path glob, and there are no `.md` files under `scripts/`, so the `Product docs only` row does not catch it. `:64` ("If the union is empty, run `/verify-suite`") therefore governs. The plan's core claim holds. Minor internal contradiction: `PLANNING.md:104` says both occurrences are "a command to invoke", then quotes the second one as a row clause two sentences later.

**Is the drop to targeted safe? Mostly yes — with three named exceptions the plan does not isolate.**

Nothing under `scripts/` is imported by `app.py`, `routes/**`, or `utils/**` at runtime. `rg "from scripts|import scripts"` outside `tests/` returns three production/build hits, and one of them is decisive:

- `Hypertrophy-Toolbox.spec:10` — `from scripts.stage_package_assets import staged_datas`. **`scripts/stage_package_assets.py` is on the shipped-artifact path.** A break there produces a broken installer, not a broken dev tool.
- `scripts/smoke_packaged_app.py:41` imports the same module.

And the sharper structural point: **the two gates this packet documents are themselves implemented in `scripts/`.** `scripts/generate_test_inventory.py` and `scripts/pyright_baseline_diff.py` *are* `Test Inventory Drift` and the pyright baseline diff. The same diff that names them as blocking also loosens the routing for the code that implements them, and never connects the two. A `pyright_baseline_diff.py` that fails open reds nothing in CI; its only proof is `tests/test_pyright_baseline_diff.py`, which the proposed rule does not find.

**Specific scripts that become under-gated** (non-empty-but-incomplete union — the fallback is suppressed):

- `scripts/css_audit/measure.py`, `specificity.py`, `runtime_probe.mjs`, `j_known_live_mutation.mjs`, and any new tool there — 1 of 5 dependent modules derived.
- Any top-level script, *if* the reader takes the broad `scripts/` prefix reading: a 13-module union that excludes `tests/test_pyright_baseline_diff.py`, `tests/test_package_asset_staging.py`, and `tests/test_playwright_shard_launcher_contracts.py` — i.e. the rule actively steers away from the correct targets.

**Two factual errors in the Measured-evidence section**, both load-bearing for the Loosens/No-change split:

- `PLANNING.md:113` lists `pyright_baseline_diff.py` and `playwright_timing_report.py` among "the 14 top-level scripts **no test names at all**". `tests/test_pyright_baseline_diff.py:13` is a dedicated module for the first; `tests/test_playwright_runner_contracts.py:164` covers the second. The claim is true of the *grep*, false as written.
- `PLANNING.md:112` lists `stage_package_assets.py` in the **Loosens** column as a script "a test already names". Under the plan's own rule it resolves to nothing (`tests/test_packaging_contract.py:82` spells it `scripts\\stage_package_assets.py`, backslashed; `test_package_asset_staging.py:12` uses the dotted import). So the plan's direction table was derived semantically, by hand — not by the rule it proposes. That is the clearest evidence the rule is not the thing the author actually used.

**Recommendation:** keep the loosening, add one clause naming the three scripts that always run their own module regardless of grep outcome — `generate_test_inventory.py`, `pyright_baseline_diff.py`, `stage_package_assets.py`. That is one line and it removes the entire unsafe portion.

---

## The two CI gates

**Both genuinely block. Verified.**

- `Test Inventory Drift`: job `test-inventory` at `.github/workflows/ci.yml:1107-1110` — no `continue-on-error` at job level. The check step at `:1139-1161` ends `exit $STATUS`. Blocking.
- pyright baseline diff: job `typecheck` at `ci.yml:859-867` — no job-level `continue-on-error`. `pyright (measure-only count)` at `:898` carries `continue-on-error: true`; `pyright baseline diff (blocking)` at `:915-919` does not. `scripts/pyright_baseline_diff.py:224-227` returns 1 on regressions, raised via `SystemExit(main())` at `:238`. Blocking. The plan's line citations (899, 915, 1108) are all exact.
- `tsc --noEmit (blocking)` at `ci.yml:924-937` captures `$STATUS` and `exit $STATUS`. Blocking. Proposed text 3 correctly calls this out as the *second* blocking step in a job named "measure-only".

**Trigger conditions — the plan describes them incompletely.**

"The inventory pins **per-file** node counts, so adding, removing, renaming, or moving a single test between files reds it" is accurate for pytest (`scripts/generate_test_inventory.py:282-290`) and the per-file framing is the right one — a totals-only artifact would not catch a move. But the artifact pins three more surfaces the row omits, and `_check` (`:405-423`) is a whole-file text diff, so *any* difference reds:

| Also pinned | Where | Changed path that trips it |
|---|---|---|
| Per-spec Playwright counts | `generate_test_inventory.py:260-267` | `e2e/**/*.spec.ts` — add/remove/rename any test |
| `waitForTimeout` lines per file | `:292-297` | `e2e/**/*.ts` — add or delete a single hard wait |
| Required functional set, derived from ci.yml | `:125-156`, `:255-259` | `.github/workflows/ci.yml` — the `e2e-functional-shard` spec list. `:139-144` hard-fails if that job is renamed |
| Parametrized config surface | `tests/test_agent_workflow_contracts.py:80-86` | **adding or deleting any file in `.claude/commands/`, `.claude/agents/`, `.claude/rules/`, or `docs/ai_workflow/`** |

That last row is the one that matters most here, and the plan misses it entirely. Adding `docs/ai_workflow/FOO.md` adds two parametrized nodes, drifts `test_agent_workflow_contracts.py`'s committed count, and reds a required check. Yet `QUALITY_GATE.md:34` and `:62` route exactly that change type to "manual dry-run/self-review; run tests only if source behavior changed" — so today's canonical routing tells the agent to run nothing, and CI reds. **A packet whose stated purpose is "name the blocking gates the table does not derive" should close that gap, and it is the one gap that bites this packet's own change type.** The test file documents the mechanism itself at `:57-71`.

So: run `python scripts/generate_test_inventory.py --check` locally before pushing when the diff touches `tests/**`, `e2e/**`, `.github/workflows/ci.yml`, `scripts/generate_test_inventory.py`, **or adds/removes a file under `.claude/commands|agents|rules` or `docs/ai_workflow/`**. Run `scripts/pyright_baseline_diff.py` when the diff touches any `.py` (it is repo-wide, not per-path — no glob narrows it).

**The "Fix when it reds" advice is wrong in a documented case.** Proposed text 3 (`PLANNING.md:69`) says: "Run `python scripts/generate_test_inventory.py` and commit the regenerated artifact. Never hand-edit the artifact, and never edit the workflow." The third prohibition is missing and it is the one that has actually bitten: an untracked or gitignored `.md` sitting in a globbed surface directory makes `--check` red locally while CI is green, and regenerating **bakes the local file into the committed artifact**. `tests/test_agent_workflow_contracts.py:206-238` states this explicitly — "the fix is to commit it or to give it the `.local.md` suffix, **never to regenerate the inventory around it**". Shipping the proposed wording as canonical would give the wrong instruction in exactly the situation the repo has already hit. Add the clause.

**One more accuracy issue in proposed text 1.** "adding or removing **any file** under `scripts/css_audit/`" over-claims. `scripts/css_audit/p3_ceiling.py:1560-1571` enumerates only `.py`/`.mjs` and explicitly excludes `__init__.py` and anything prefixed `p3_`. A new `p3_*.py` tool, or a `.json`, does **not** red `test_every_committed_css_audit_tool_is_assessed` (`tests/test_css_theme_dark_p3_audit_contracts.py:685`). Direction is safe (over-running), but the row asserts a guarantee the contract does not provide. Say "any `.py` or `.mjs` file other than `__init__.py` and `p3_*`".

---

## Wording that will misread or go stale

1. **`ci.yml:1099-1102` directly contradicts proposed text 3.** That comment says `Test Inventory Drift` "is not in branch protection, so it was renamed freely." `QUALITY_GATE.md:114-119` says the second step has since been taken and it is one of the 11 required contexts. Proposed text 3 puts it in a column headed "Check name (branch protection, verbatim)". An agent who greps `ci.yml` finds the opposite claim. Not this packet's file to fix, but the new subsection should say the workflow comment is stale — otherwise it looks like the new table is the wrong one. (I could not re-derive branch protection from here; I am reporting the two committed claims, not adjudicating them.)
2. **"Blocking since 2026-08-01" inside a branch-protection column** conflates two things `QUALITY_GATE.md:112` is at pains to separate — the job failing, and the merge blocking. The job flipped 2026-08-01; the context was added later (doc says re-derived 2026-08-04). Split them.
3. **"see Targeted-test derivation"** in proposed text 1 creates a forward reference from the table (line ~34) to a section at `:53`. Every other row states its gate inline. Fine, but note that the derivation the reader lands on is the one this review says does not work.
4. **Two consumers duplicate the derivation list and will not gain the new bullet.** `.claude/commands/unslop.md:16-20` and `.claude/agents/test-strategist.md:20-23` each carry a three-bullet excerpt (routes / utils / templates) and then fall to `/verify-suite`. Both defer to `QUALITY_GATE.md` as canonical, so leaving them is defensible — but the practical effect is that the agents that actually route changes will keep sending `scripts/**` to `/verify-suite`, and the new row will sit unused. Either add the bullet to both, or add a one-line "this excerpt is partial; the canonical list is longer" pointer. Worth an explicit owner decision at Gate 1, since the plan's Scope says "and nowhere else."
5. Pre-existing, out of scope, flagged for truth: `.claude/agents/test-strategist.md:31` still lists `e2e/nav-dropdown.spec.ts:117` as a current known-red, which `QUALITY_GATE.md:126` retired on 2026-06-11.

---

## Coverage gaps

- `docs/ai_workflow/QUALITY_GATE.md` — needs no new test. Its two existing assertion points (`tests/test_agent_workflow_contracts.py:138,158`; `tests/test_consult_adapter.py:1068-1070`) are content checks, not structure checks. Nothing asserts that the change-type table's globs are non-overlapping or that every glob is anchored — which is precisely the defect in proposed text 2. Out of scope for a docs packet; worth naming as a finding.
- No new pytest or Playwright file is warranted by this diff.

## Conftest / fixture work

None. No blueprint, no table, no route.

---

## Verdict

Gate selection is right, the two CI-gate verifications are accurate and precisely cited, and the loosening analysis is honest about direction. But the packet's central deliverable — proposed text 2 — does not work on the paths it will be used for: it misses 4 of 5 dependents of `scripts/css_audit/`, misses `tests/test_pyright_baseline_diff.py`, misses `tests/test_package_asset_staging.py`, and its top-level-prefix clause contradicts the plan's own evidence table. Two entries in that table are factually wrong, the loosening silently covers the one script on the packaged-artifact path and the two scripts that implement the gates being documented, and the inventory "fix when it reds" instruction contradicts a hazard already recorded in `tests/test_agent_workflow_contracts.py:206-238`. All are fixable inside the owner-locked scope; none require a code change.

REVISE
````

### product-risk-reviewer (run evidence: 22 tool calls · 61,033 tokens · 245 s · `REVISE`)

````markdown
## Scope note: two of my five charter areas genuinely do not apply

**Local-first / non-goals (charter §3): clean.** Nothing in the plan introduces auth, cloud sync, a remote DB, or telemetry. No finding, and I am not going to manufacture one.

**Terminology drift (charter §4): clean.** The proposed text contains no user-facing copy at all — it is agent-facing routing documentation. RIR/RPE/Effective sets/CountingMode/ContributionMode do not appear and are not at risk. No finding.

The remaining three areas — calculation surface, the weakened-gate risk, and self-overstatement — are where the real content is, and they turn out to be the same finding seen from three angles.

---

## Findings

### 1. The empty-union fallback does not protect the case that actually matters — shallow coverage, not zero coverage

`PLANNING.md:113` rests the plan's entire safety argument on one sentence: *"Grep finds nothing, union stays empty, `/verify-suite` still applies. The preserved fallback is what keeps this honest."*

That is true only for scripts with **zero** test references. The dangerous category is scripts with **one shallow** reference: the union is non-empty, so the fallback never fires, and the documented gate collapses from full pytest to a test that does not assert the thing the script changes. The plan never analyzes this category. Its three-direction table (`PLANNING.md:110-114`) has buckets for "a test already names it" and "no test names it at all" — and no bucket for "a test names it but does not cover it."

Two catalog-mutating scripts land squarely in that unanalyzed bucket:

```
<Proposed text 1 / "What the new row actually changes"> — targeted row routes catalog-mutating scripts to a NULL-check only
  Invariant at risk: CLAUDE.md §1 "Refactor invariant" — do not silently alter calculation logic
  Risk: primary_muscle_group / movement_pattern reassignments reach main with the muscle-attribution goldens unrun
  Fix: exempt scripts that write to the exercises catalog from the targeted rule and keep /verify-suite mandatory for them
```

The mechanism, verified:

- `scripts/fatigue_stage1_cleanup.py:38-43` writes `primary_muscle_group` via `infer_primary_muscle()`, falling back to `'Unassigned'`. That column is the direct input to `ContributionMode.DIRECT_ONLY` (`utils/effective_sets.py:270`) and to per-muscle accumulation in weekly/session summary.
- `scripts/fatigue_movement_pattern_cleanup.py:34-39` writes `movement_pattern` via `classify_exercise()`, falling back to `'unassigned'`. That feeds fatigue pattern-weight resolution and plan-generator blueprint slots.
- Under the proposed rule (`PLANNING.md:52`), `rg -F "scripts/fatigue_stage1_cleanup.py" tests` resolves to exactly one module: `tests/test_catalog_invariants.py:31` (the path appears there only inside an assertion *message*). Same for the pattern script at `tests/test_catalog_invariants.py:52`.
- That module copies the shipped seed (`tests/conftest.py:190-198`) and asserts only `COUNT(*) WHERE col IS NULL OR TRIM(col) = '' == 0`. **Reassigning every exercise from `Chest` to `Unassigned` passes it.**
- The tests that would actually catch it — `tests/test_weekly_summary_unassigned.py`, `tests/test_weekly_summary_golden.py`, `tests/test_fatigue_golden.py` — name no `scripts/` path, so the grep-first rule can never route them. Today they run, because the union is empty and `/verify-suite` fires. Under the new row they do not.

This is a change to Analyze-workflow output reachable without touching `utils/`. It is the "silent calculation change" CLAUDE.md §1 prohibits, arriving through the data rather than the code.

A third instance, same shape: `scripts/css_audit/emit_baseline.py` is named by no test, but the directory prefix `scripts/css_audit/` matches `tests/test_css_theme_dark_p3_audit_contracts.py:688`, so its union is non-empty too. The manifest-digest guard that memory records as full-pytest-only lives in `tests/test_css_wp4_4_a_baseline_contracts.py`, which names no script path and would be skipped.

### 2. Calculation surface — "none" is correct for the diff, and the plan lets that stand for more than it should

```
<Plan-stage sizing: "Medium">, <Artifacts table> — calculation surface is nil for the diff but not for what the row governs
  Invariant at risk: CLAUDE.md §1 "Refactor invariant"; QUALITY_GATE.md:14 (calculation-surface change ⇒ Large)
  Risk: the packet reads as risk-free, so the catalog-writing scripts in §1 above never get discussed at Gate 1
  Fix: add one paragraph naming the catalog-writing scripts the new row routes, and carry it into the Sign-off list
```

Confirmed: the shipped diff is one markdown file (`PLANNING.md:32`) and touches no calculation code. I refute nothing about the diff itself. What I refute is the implied conclusion. `PLANNING.md:121` frames the loosening as affecting only "a one-line edit to a reporting script" — but the loosened set demonstrably includes two scripts that rewrite calculation *inputs* in the shipped catalog, and the plan names neither anywhere in the document. The Sign-off item at `PLANNING.md:183` asks the owner to rule on the loosening direction while presenting only reporting-script examples, so the owner is being asked to decide without the fact that would most likely change the decision.

Related, smaller: the proposed row assigns `code-reviewer` only (`PLANNING.md:44`). `QUALITY_GATE.md:28` requires `product-risk-reviewer` when `effective_sets` / `weekly_summary` / `session_summary` / `progression` / `fatigue` are touched. The new row creates an asymmetry where editing `utils/fatigue.py` summons me and editing the script that populates the catalog fatigue reads from does not. Given memory's standing constraint that Stage 4 calibration is open and threshold changes need ≥2 disagreements, that gap is worth closing in the row's reviewer column.

### 3. The plan's own evidence contains a pair its own rule cannot resolve — and that pair is the packaged catalog seed

```
<Measured evidence, line 132> — stage_package_assets.py → test_packaging_contract.py is cited as verified but is unreachable by proposed text 2
  Invariant at risk: plan-internal accuracy; the derivation rule ships verbatim
  Risk: the evidence justifying grep-first includes a case where grep-first returns nothing
  Fix: re-derive the covered/uncovered split with the exact rg command the row mandates, and correct the three-direction table
```

`PLANNING.md:132` presents `stage_package_assets.py → test_packaging_contract.py` as one of the verified pairs demonstrating the "test named after the contract" pattern, and `PLANNING.md:112` lists `stage_package_assets.py` among the 12 scripts whose gate loosens. Neither holds under the proposed command `rg -F "scripts/stage_package_assets.py" tests`:

- `tests/test_package_asset_staging.py:12` — `from scripts.stage_package_assets import (` — dotted module path, no `/`.
- `tests/test_packaging_contract.py:82` — `assert "scripts\\stage_package_assets.py" in lowered` — backslash separator.

Both miss a forward-slash fixed-string grep. The union is empty, so the outcome is *safe* (`/verify-suite` still applies) — but the plan's classification of this file is wrong, and this is the script that stages `data/catalog.seed.db` into the packaged build (`tests/test_packaging_contract.py:11`). The plan's measured evidence is therefore not reliable enough to support the sign-off question at `PLANNING.md:183`; the split was evidently derived with a looser grep than the one the row mandates.

Secondary fragility, same family: the `scripts/css_audit/` prefix match at `tests/test_css_theme_dark_p3_audit_contracts.py:688` lands in a **docstring**. The test's actual assertions build the path with `ROOT / "scripts" / "css_audit"` (`:700`, `:744`), which no path grep matches. The plan's "load-bearing half" (`PLANNING.md:55`) works today only because of prose that no test pins — a reflow silently disarms it.

### 4. Non-goal check: no second gate system, and no CI weakening — this part of the plan is sound

No finding. The packet writes one file (`PLANNING.md:32`), explicitly excludes `ci.yml`, job renames, and branch-protection edits (`PLANNING.md:22-23`), and adds no parallel authority that could compete with `QUALITY_GATE.md`. Enforced gate behaviour is untouched; what changes is the written standard. The plan says so itself at `PLANNING.md:121` and escalates the direction to the owner rather than deciding it — that candour is the strongest thing in the document and I want it credited plainly.

I also want to credit the genuine tightening at `PLANNING.md:118`: making the `scripts/css_audit/` directory contract derivable converts a hazard that memory records as full-pytest-only into a mandatory targeted gate. That is a real improvement, not a wash.

### 5. Copy and honesty on the two CI gates: accurate, and clear enough

No finding. I verified both claims at `PLANNING.md:138` against the workflow:

- `.github/workflows/ci.yml:899` — `pyright (measure-only count)` carries `continue-on-error: true`.
- `.github/workflows/ci.yml:915` — `pyright baseline diff (blocking)` carries none and shells out to `scripts/pyright_baseline_diff.py`.
- `.github/workflows/ci.yml:1108` — `name: Test Inventory Drift`, with `exit $STATUS` at `:1161`.

Proposed text 3's wording — *"**Two** blocking steps, despite the name... Only the pyright *count* step is measure-only; the baseline diff beside it is not"* — is accurate and correctly scoped to the step, not the job. The bolded paragraph *"The pyright job's name understates what it enforces, and the name stays anyway"* plus *"Correct the understanding here; do not correct the label"* is unambiguous, and it is reinforced by the in-repo comment at `ci.yml:860-864` saying the same thing. An agent reading only that table draws the right conclusion. This satisfies the rename prohibition already recorded at `QUALITY_GATE.md:104`.

One precision nit, non-blocking: the row says `Test Inventory Drift` has been "Blocking since 2026-08-01", under a column headed "Check name (branch protection, verbatim)". Per `QUALITY_GATE.md:114-119` the *job* went red-on-drift on 2026-08-01 while still unprotected; *merge* blocking began only when it entered branch protection, re-derived 2026-08-04. Consider "job blocking since 2026-08-01; in branch protection since 2026-08-04."

---

## What the plan overstates

One sentence, and it is the load-bearing one: `PLANNING.md:113` — *"The preserved fallback is what keeps this honest."* The fallback keeps the **zero-coverage** scripts honest. It does nothing for the shallow-coverage scripts, and that is where the catalog writers, the fatigue data cleanups, and the visual-baseline emitter all sit. The plan's three-direction table has no column for them, so the honest-looking analysis at `PLANNING.md:100-121` is structurally incapable of surfacing the risk it most needed to surface.

Minor, for completeness: `PLANNING.md:104` says `scripts` appears in `QUALITY_GATE.md` "only twice, both times as a command to invoke." One of the two is prose, not a command — `QUALITY_GATE.md:35`, *"none unless examples/scripts changed."* The plan addresses that clause in its very next sentence, so this is loose phrasing rather than a wrong conclusion.

## Suggested minimum revision

Add a fourth direction to the table at `PLANNING.md:110` — "Loosens dangerously: scripts whose only test reference is shallow" — naming `fatigue_stage1_cleanup.py`, `fatigue_movement_pattern_cleanup.py`, and `css_audit/emit_baseline.py`; and amend proposed text 1 so that any script writing to the `exercises` catalog or to a committed baseline keeps `/verify-suite` regardless of what the grep returns. Then re-derive the covered/uncovered split using the exact `rg -F` command the row mandates.

REVISE
````

---

## Response matrix

Every finding gets its own row. Reviewer-numbered findings keep their numbers; unnumbered items are labelled by section and listed individually.

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| **A1** `pyright_baseline_diff.py` wrongly filed as "no test names it"; `tests/test_pyright_baseline_diff.py:13` is a dedicated twin | architecture-reviewer | **accept** | Verified: the module exists and imports the dotted path. Split re-derived from scratch (v2 §"Re-derived split"); the file moves to *covered*, and is additionally pinned by the always-run carve-out in proposed text 1. |
| **A2** `rg -F` slash-form search has systematic false negatives | architecture-reviewer | **accept** | Root defect. Proposed text 2 rewritten to a separator-free stem + directory-token search. |
| **A3** "each parent directory prefix" is unbounded; bare `scripts/` matches ~13 modules | architecture-reviewer | **accept** | Proposed text 2 now says explicitly: never search the bare `scripts/` prefix; the directory token applies only to directories strictly below `scripts/`. |
| **A4** Text 3 opens with "neither is derivable from a changed path", which its own table refutes | architecture-reviewer | **accept** | Reworded to "neither is *narrowly* path-scoped", and both real triggers are now stated in the subsection. |
| **A5** `ci.yml:1099-1102` contradicts text 3's branch-protection column | architecture-reviewer | **accept** | Verified the stale comment verbatim. Text 3 gains a sentence recording it as known-stale; the **Out** list names the `ci.yml` comment fix as an explicit non-goal. |
| **A6** "and nowhere else" understates the effect on two derivation-list consumers | architecture-reviewer | **accept** | Both consumers verified. Recorded in v2 Scope **Out** with the reason the divergence is safe, and raised as a Gate 1 owner question rather than silently resolved. |
| **A7** "2 of 26 exact-name twins" membership wrong — `apply_free_exercise_db_mapping.py` is not a twin | architecture-reviewer | **accept** | Verified: `tests/test_apply_free_exercise_db_mapping.py` does not exist. Membership corrected in v2; the real twins are `fatigue_stage4_observer.py` and `pyright_baseline_diff.py`. |
| **A8** `test_agent_workflow_contracts.py` does not assert on `generate_test_inventory.py` — both hits are comments | architecture-reviewer | **accept** | Verified (lines 69 and 102 are comments). v2 states that a grep hit proves a *mention*, not coverage, and proposed text 2 now carries that caveat as an instruction. |
| **A9** "`scripts` appears twice, both as a command to invoke" — one is prose | architecture-reviewer | **accept** | Loose phrasing corrected in v2's evidence note. Conclusion (never a changed-path glob) unchanged and still verified. |
| **T1** Sequence must end with `/handover` | test-strategist | **accept** | Added as Sequence step 7. |
| **T2** The `RETIRED_NUMBERING` / `SHARED_PLAN` grep should be a Sequence step, not a note | test-strategist | **accept** | Promoted from Hazard §1 to Sequence step 5. |
| **T3** Path 1 — `consult.py` resolves only via a file-list assertion string, not the real dependency | test-strategist | **accept** | Illustrates the same root defect as A2. The stem search (`consult`) reaches the module through its real coupling; recorded in v2's rule rationale. |
| **T4** Path 2 — a new `css_audit` tool derives 1 of 5 dependents; true under-gating, fallback suppressed | test-strategist | **accept** | Verified: `css_audit` stem grep returns all 5 modules, the slash grep returns 1. This is the strongest single argument for the rewrite and is quoted in v2. |
| **T5** Path 3 — proposed text and the impact table disagree for every top-level script | test-strategist | **accept** | Resolved by A3's bound; the v2 impact table is re-derived so both now agree by construction. |
| **T6** Root cause + fix: grep the stem and directory token, separator-free (6 worked examples) | test-strategist | **accept** | All six examples independently re-verified in this worktree before adopting. Proposed text 2 rewritten accordingly. |
| **T7** Glob ambiguity — `e2e/scripts/` exists and is claimed by the `E2E spec` row; no precedence rule | test-strategist | **accept** | Verified `e2e/scripts/` holds 4 files. Proposed text 1's glob is now anchored to the repository root and states precedence explicitly. |
| **T8** `stage_package_assets.py` is on the packaged-artifact path (`Hypertrophy-Toolbox.spec:10`) | test-strategist | **accept** | Verified the import. Added to the always-run carve-out in proposed text 1. |
| **T9** The two documented gates are themselves implemented in `scripts/` | test-strategist | **accept** | The sharpest structural point. Both gate implementations added to the always-run carve-out, and the connection is stated in v2 rather than left implicit. |
| **T10** Two factual errors in Measured evidence (uncovered bucket; `stage_package_assets` in Loosens) | test-strategist | **accept** | Both confirmed wrong. Whole split re-derived mechanically; correction notice added so Plan v1's rows are not read as current. |
| **T11** Recommendation: always-run clause for the three named scripts | test-strategist | **accept, widened** | Adopted and extended beyond the three to include catalog and baseline writers, per PR1/PR2. |
| **T12** The inventory pins three further surfaces beyond per-file pytest counts | test-strategist | **accept** | All four pinned surfaces now listed in proposed text 3's trigger table. |
| **T13** Adding/removing a file under `.claude/{commands,agents,rules}` or `docs/ai_workflow/` reds a required check while canonical routing says run nothing | test-strategist | **accept** | The gap that bites this packet's own change type. Now an explicit trigger row in proposed text 3. |
| **T14** "Fix when it reds" omits the never-regenerate-around-an-untracked-file prohibition | test-strategist | **accept** | Verified the prohibition verbatim at `tests/test_agent_workflow_contracts.py:212-214`. Added to proposed text 3 as the third prohibition. |
| **T15** `scripts/css_audit/` "any file" over-claims | test-strategist | **accept** | Verified `p3_ceiling.py:1564-1571`: `.py`/`.mjs` only, excluding `__init__.py` and `p3_*`. Proposed text 1 corrected to match the contract exactly. |
| **T16** `ci.yml:1099-1102` stale comment (duplicate of A5) | test-strategist | **accept** | Same action as A5; recorded once. |
| **T17** "Blocking since 2026-08-01" conflates job-blocking with merge-blocking | test-strategist | **accept** | Split into "job blocking 2026-08-01; in branch protection 2026-08-04" in proposed text 3. |
| **T18** Forward reference from the table row to the derivation section | test-strategist | **reject** | Kept deliberately. The `static/css/**` row already forward-references "the feature map below", so this matches house style, and inlining the full stem-search rule would make the cell unreadable. The underlying objection — that the referenced rule did not work — is fixed by T6. |
| **T19** Two consumers duplicate the derivation list and will not gain the new bullet | test-strategist | **defer** | Deferred: editing `.claude/**` is outside the owner-locked scope. Reason recorded, and raised as Gate 1 owner question 3 so the owner can widen scope if they prefer. To be noted in `MASTER_HANDOVER.local.md` at implementation time. |
| **T20** `.claude/agents/test-strategist.md:31` still lists a retired known-red | test-strategist | **defer** | Pre-existing and out of scope; verified true. Recorded in v2 **Out** as a follow-up so it is not lost. |
| **T21** Nothing asserts the change-type table's globs are non-overlapping or anchored | test-strategist | **defer** | Legitimate, and it is exactly the defect class T7 found. A structural contract test is a code packet, not a documentation packet. Named as a follow-up candidate in **Out**. |
| **PR1** The empty-union fallback protects zero-coverage scripts, not shallow-coverage ones — catalog writers pass a NULL-check | product-risk-reviewer | **accept** | The most serious finding. Independently verified end to end: `infer_primary_muscle()` falls back to `UNASSIGNED`, and `test_catalog_invariants.py` asserts only NULL/blank, so a wholesale `Chest`→`Unassigned` rewrite passes. A fourth direction is added to the impact table and an always-run carve-out to proposed text 1. |
| **PR2** Calculation surface is nil for the diff but not for what the row governs; `product-risk-reviewer` missing from the row | product-risk-reviewer | **accept** | Both parts adopted: v2 names the catalog-writing scripts explicitly, carries them into the Gate 1 sign-off question, and adds `product-risk-reviewer` to the row's reviewer column for catalog writers. |
| **PR3** The plan's own evidence contains a pair its own rule cannot resolve (`stage_package_assets`) | product-risk-reviewer | **accept** | Same defect as T10; split re-derived with the corrected command. |
| **PR4** No second gate system, no CI weakening — sound (credit) | product-risk-reviewer | **accept (no change)** | No action needed. Scope discipline retained unchanged in v2. |
| **PR5** CI-gate copy accurate (credit) + nit on the 2026-08-01 / 2026-08-04 split | product-risk-reviewer | **accept** | Copy retained verbatim; the date nit is actioned identically to T17. |
| **PR-o** "The preserved fallback is what keeps this honest" is overstated | product-risk-reviewer | **accept** | Sentence retired. v2 states the fallback protects only the zero-reference set and names what covers the rest. |
| **PR-m** "both times as a command to invoke" is loose (duplicate of A9) | product-risk-reviewer | **accept** | Same action as A9. |

---

## Plan v2

> **Supersedes Plan v1's evidence.** Plan v1's three-direction table and its "12 covered / 14 uncovered" split were hand-derived and are wrong in at least three memberships (`pyright_baseline_diff.py`, `playwright_timing_report.py`, `stage_package_assets.py`). Plan v1 is left unedited to preserve the audit trail; **the split below replaces it** and was produced mechanically with the command v2 actually mandates.

**Goal**: Unchanged — make the gates for a `scripts/**` change mechanically derivable, and name the two required CI checks that block merges today but appear nowhere in `QUALITY_GATE.md`'s change-type table. What changes is the derivation mechanism, which Plan v1 got wrong.

**Scope**

- **In**: unchanged in shape — one table row, one derivation bullet, one new subsection, all in `docs/ai_workflow/QUALITY_GATE.md`.
- **Out**: unchanged, plus four items the council surfaced and this packet knowingly does not fix:
  - `.github/workflows/ci.yml:1099-1102`, whose comment still claims `Test Inventory Drift` "is not in branch protection". Verified stale; superseded by `QUALITY_GATE.md:114-119`. Proposed text 3 records it as stale; correcting the comment is a `ci.yml` edit and out of scope.
  - `.claude/commands/unslop.md:16-20` and `.claude/agents/test-strategist.md:20-23`, which carry partial derivation lists and will keep routing `scripts/**` to `/verify-suite`. Safe divergence (both defer to `QUALITY_GATE.md` as canonical, and the stale behaviour is the *stricter* one), but it means the new row will sit unused by those two agents until someone updates them. **Owner question 3.**
  - `.claude/agents/test-strategist.md:31`, still listing `e2e/nav-dropdown.spec.ts:117` as a known-red that `QUALITY_GATE.md:126` retired on 2026-06-11.
  - A structural contract test asserting the change-type table's globs are anchored and non-overlapping. This packet's `e2e/scripts/` collision is exactly the defect such a test would catch; it is a code packet.

**Artifacts** — unchanged from Plan v1.

| Path | Change | Notes |
|---|---|---|
| `docs/ai_workflow/QUALITY_GATE.md` | modify | The only file this packet writes. Three additions, no deletions, no rewording of existing rows. |
| `docs/quality_gate_routing/PLANNING.md` | new (this file) | Plan artifact; not part of the shipped diff's behavior surface. |

**Effort**: S · **Owner**: implementing agent after Gate 1 · **Depends on**: nothing.

---

### Proposed text 1 (revised) — the change-type table row

Insert **after** the `E2E spec` row and **before** the `AI workflow / agent config` row, verbatim:

```markdown
| Tooling / scripts | `scripts/**` at the repository root only — `e2e/scripts/**` stays with the **E2E spec** row above; when two rows match a path, the more specific glob wins | The union from the stem + directory-token search under Targeted-test derivation. If it is empty, `/verify-suite`. **`/verify-suite` regardless of what the search returns** when the changed script writes the `exercises` catalog (`fatigue_stage1_cleanup.py`, `fatigue_movement_pattern_cleanup.py`, `apply_free_exercise_db_mapping.py`, `apply_youtube_curated.py`), writes a committed baseline (`css_audit/emit_baseline.py`), sits on the packaged-artifact path (`stage_package_assets.py`, imported by `Hypertrophy-Toolbox.spec`), or implements one of the two blocking gates below (`generate_test_inventory.py`, `pyright_baseline_diff.py`). Adding or removing a `.py` or `.mjs` file other than `__init__.py` or `p3_*` under `scripts/css_audit/` also requires `tests/test_css_theme_dark_p3_audit_contracts.py` | `code-reviewer`; + `product-risk-reviewer` if the script writes the `exercises` catalog |
```

### Proposed text 2 (revised) — the Targeted-test derivation bullet

Insert after the `static/css/**` bullet and before the `app.py, tests/conftest.py, root configs` bullet, verbatim:

```markdown
- `scripts/**` (repository root; `e2e/scripts/**` is an E2E spec change) → search `tests` for the file **stem** and, for a file below `scripts/`, its **parent directory name** — separator-free, never as a path. The dominant idioms here are `from scripts.x import y` and `ROOT / "scripts" / "x"`, and a slash-path search matches neither: `rg -n "pyright_baseline_diff" tests`, `rg -n "css_audit" tests`. **Never search the bare `scripts/` prefix** — it matches most of the suite and suppresses the fallback. Take the union of every module found; if it is empty, `/verify-suite`. A hit proves a *mention*, not coverage — some are assertion messages, sample inputs, or comments — so confirm the test asserts the behavior you changed, and escalate to `/verify-suite` when it does not
```

### Proposed text 3 (revised) — the blocking CI gates subsection

Insert after the change-type table and its two block quotes, before `## Diff collection`, verbatim:

```markdown
## Blocking CI gates the change-type table does not derive

Two required checks fail on changes the table above does not route to. Neither is
*narrowly* path-scoped — both are triggered by broad, cross-cutting conditions — so
they are named here once rather than duplicated into every row.

| Check name (branch protection, verbatim) | What actually blocks | Fix when it reds |
|---|---|---|
| `Test Inventory Drift` | `scripts/generate_test_inventory.py --check` against the committed `docs/test_inventory/`. The job has been red-on-drift since 2026-08-01; it entered branch protection later, re-derived 2026-08-04. The check is a whole-file text diff, so *any* difference reds. | Run `python scripts/generate_test_inventory.py` and commit the regenerated artifact. Never hand-edit it. Never edit the workflow. **And never regenerate while an untracked or gitignored `.md` sits in a globbed surface directory** — that reds `--check` locally while CI is green, and regenerating bakes the local file into the committed artifact. Commit that file or give it a `.local.md` suffix first. |
| `Type Check (tsc blocking + pyright measure-only)` | **Two** blocking steps, despite the name. `tsc --noEmit` must report zero errors. Separately, `scripts/pyright_baseline_diff.py` fails on net-new pyright diagnostics against `docs/ci_cd_phase3/pyright-baseline.json`. Only the pyright *count* step is measure-only; the baseline diff beside it is not. | Fix the net-new diagnostic. Re-baselining to make it pass is an owner decision, not a repair. |

**What trips `Test Inventory Drift`.** The artifact pins five change surfaces, not one:

| Pinned surface | Changed path that trips it |
|---|---|
| Per-file pytest node counts | `tests/**` — add, remove, rename, or move a test between files |
| Per-spec Playwright counts | `e2e/**/*.spec.ts` — add, remove, or rename any test |
| `waitForTimeout` lines per file | `e2e/**/*.ts` — add or delete a single hard wait |
| Required functional spec set, derived from the workflow | `.github/workflows/ci.yml` — the `e2e-functional-shard` spec list, or a rename of that job |
| Parametrized configuration surface | **adding or deleting any file under `.claude/commands/`, `.claude/agents/`, `.claude/rules/`, or `docs/ai_workflow/`** |

That last row is a genuine gap in the routing above: the `AI workflow / agent config`
row says "run tests only if source behavior changed", but *adding or deleting* a file
in those directories changes a parametrized node count and reds a required check even
though no source behavior moved. Editing an existing file in place does not.

The pyright baseline diff is repo-wide, not per-path: run it when the diff touches any
`.py`. No glob narrows it.

**The pyright job's name understates what it enforces, and the name stays anyway.**
"measure-only" is accurate for the count step and wrong for the job. The label is
frozen under the CI job naming rule below: this job sits in branch protection, so
renaming it orphans the required context and every PR then blocks on a check that
will never report again. Correct the understanding here; do not correct the label.

**Known-stale, deliberately not fixed here:** the comment at `.github/workflows/ci.yml`
above the `test-inventory` job still says that job "is not in branch protection".
That was true when written and is superseded by the CI job naming section below.
Trust this table and that section, not the workflow comment.
```

---

### Re-derived split (mechanical, using the v2 rule)

Produced by searching `tests` for each of the 26 top-level stems, separator-free — the exact command proposed text 2 mandates. This replaces Plan v1's hand-derived table.

**18 of 26 top-level scripts are named by at least one test** (Plan v1 said 12). **8 have no reference at all** (Plan v1 said 14): `baseline_contact_sheet.mjs`, `check_ci_concurrency.py`, `check_fatigue_stage4_automation.ps1`, `fatigue_calibration_report.py`, `install_fatigue_stage4_observer_task.ps1`, `run_fatigue_stage4_observer.bat`, `stylelint-report.mjs`, `playwright_shard_summary.py`.

Exact-name twins are **2 of 26**, but the membership Plan v1 gave was wrong: they are `fatigue_stage4_observer.py` → `tests/test_fatigue_stage4_observer.py` and `pyright_baseline_diff.py` → `tests/test_pyright_baseline_diff.py`. `apply_free_exercise_db_mapping.py` maps to `tests/test_free_exercise_db_mapping.py` (no `apply_` prefix), so it is not a twin.

**The four directions** — Plan v1 had three and was missing the one that matters:

| Direction | Which files | Effect |
|---|---|---|
| **Loosens safely** | Scripts with genuine, behavior-asserting coverage — `apply_youtube_curated.py`, `build_musclemap_svgs.py`, `run-playwright.ps1`, `run-playwright-shards.ps1`, `wait_for_clean_start.ps1`, `shard_telemetry.ps1`, `playwright_timing_report.py`, `fatigue_stage4_observer.py`, `fatigue_stage4_status.py`, `smoke_packaged_app.py` | Documented gate drops from full `/verify-suite` to targeted modules that actually assert the changed behavior. |
| **Loosens dangerously — shallow coverage** | `fatigue_stage1_cleanup.py`, `fatigue_movement_pattern_cleanup.py` (only reference: an assertion *message* in `tests/test_catalog_invariants.py`, which asserts NULL/blank only), `css_audit/emit_baseline.py` (reaches a docstring, not the manifest-digest guard), `generate_test_inventory.py` (both hits are comments), `run-pytest.ps1` and `new-worktree.ps1` (guard *sample inputs*; `scripts/new-worktree.sh` is not even a real file) | **The union is non-empty, so the fallback never fires**, and the gate collapses to a test that cannot see the change. Closed by the always-run carve-out in proposed text 1. |
| **No change** | The 8 scripts with zero references | Union stays empty, `/verify-suite` still applies. |
| **Tightens** | Adding/removing a `.py`/`.mjs` under `scripts/css_audit/`; any script in the carve-out | Newly *required* to run something not required today. |

**The dangerous bucket, stated plainly.** `scripts/fatigue_stage1_cleanup.py` writes `primary_muscle_group` — the direct input to `ContributionMode.DIRECT_ONLY` — with an `Unassigned` fallback. Its only test reference asserts `COUNT(*) WHERE col IS NULL OR TRIM(col) = ''` is zero. **Reassigning every exercise from `Chest` to `Unassigned` writes a non-null, non-blank string and passes.** The tests that would catch it (`test_weekly_summary_unassigned.py`, `test_weekly_summary_golden.py`, `test_fatigue_golden.py`) name no script path and are unreachable by any grep-based rule. Today they run because the union is empty and `/verify-suite` fires; without the carve-out, the new row would stop running them. That is a silent calculation-input change reaching main — precisely what `CLAUDE.md` §1's refactor invariant prohibits — and it is why the carve-out is not optional.

**Sequence**

1. Re-read `QUALITY_GATE.md` and confirm the three insertion points still match by neighbouring row (line numbers drift).
2. Apply proposed texts 1, 2, and 3. No other edit; leave every existing row byte-for-byte alone.
3. Confirm the three substrings pinned by `tests/test_consult_adapter.py:1068-1070` are still present: `## Plan-stage routing`, `Gate 0 (requirements approval) + Gate 1 (council-reviewed plan approval)`, `Run the union, never the weaker set.`
4. Re-verify the carve-out script list against disk — every filename in proposed text 1 must exist, or the row names a ghost.
5. Grep the applied text for `\bTier \d`, `\bAppendix A\d`, and `SHARED_PLAN`. Any hit reds `tests/test_agent_workflow_contracts.py`. (All three proposed blocks are currently clean.)
6. Run the two derived pytest modules. Do **not** regenerate `docs/test_inventory/` — this packet edits an existing file in place and adds no node.
7. Manual dry-run/self-review → `code-reviewer` → `/handover`.

**Expected gates** *(proposer's derivation, confirmed by `test-strategist` as correct and complete for this diff)*

- pytest: `tests/test_agent_workflow_contracts.py`, `tests/test_consult_adapter.py::test_the_canonical_planning_gates_still_trigger`
- e2e: none
- other: manual dry-run/self-review + `code-reviewer` + `/handover`. No inventory regeneration, no `/build-css`, no visual matrix.

Sequence step 6's "no regeneration" holds for a specific, load-bearing reason: `SURFACE` is built by globbing `docs/ai_workflow/*.md`, so the node count depends on the *number* of files, not their contents. This packet adds no file there. The new planning artifact lives at `docs/quality_gate_routing/PLANNING.md`, outside every `SURFACE` glob.

---

## Sign-off

- [x] Gate 0 — **not applicable**: planning size is Medium; Section 0 was not written and Gate 0 is not claimed.
- [x] Every finding has a disposition — 37 rows above (9 architecture, 21 test-strategist, 7 product-risk): 33 accept, 1 reject (T18, with reason), 3 defer (T19, T20, T21, each with a reason and a follow-up home).
- [x] Agent provenance complete — both `product-manager` rows, same-PM-resumed `yes`, three reviewers recorded by run evidence, evidence-gap line present.
- [x] **Owner question 1 — approved 2026-08-14.** Use the targeted row with the always-run carve-out. This retains the useful targeted lane while keeping catalog writers, baseline writers, the packaged-artifact path, and the two gate implementations on `/verify-suite` regardless of shallow references.
- [x] **Owner question 2 — approved 2026-08-14.** The three Plan v2 blocks ship verbatim.
- [x] **Owner question 3 — keep Packet A's scope locked.** Do not edit `.claude/commands/unslop.md` or `.claude/agents/test-strategist.md` in this packet. Their stricter fallback remains safe; the duplication is preserved as a follow-up rather than silently widening a one-file packet.
- [x] **Owner question 4 — approved 2026-08-14.** Place the new CI-gates subsection after the change-type table and its two block quotes, before `## Diff collection`.
- [x] **GATE 1 — APPROVED 2026-08-14.** The owner instructed Codex to proceed from the stopped Gate 1 state and carry the approved serialized work through completion.

---

## See also
- [QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md) — the file this packet edits.
- [PLAN_REVIEW_TEMPLATE.md](../ai_workflow/PLAN_REVIEW_TEMPLATE.md) — artifact shell this follows.
