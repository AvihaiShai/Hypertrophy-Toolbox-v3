# Agent-workflow integrity — LEFTOVERS P1.8 + P1.3

*One packet. Both source rows are the same defect class: the committed agent
configuration disagrees with itself, and nothing in CI can see it because every
file involved is Markdown.*

**Source items:** [`LEFTOVERS_BY_PRIORITY.md`](../LEFTOVERS_BY_PRIORITY.md) rows
**P1.8** (ghost `.claude/SHARED_PLAN.md` authority) and **P1.3**
(`/verify-and-polish` → `/handover` skill-guard contradiction), deep-scan
revision v23.

**Evidence snapshot:** 2026-08-04, `origin/main` @ `ed14bb3`. Every premise below
was re-derived at that commit, not copied from the v23 rows.

**Planning size:** **Medium** under
[QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) — a bounded
workflow change with known scope and no schema, API, or calculation surface. The
two owner decisions that made these rows **OWNER** were supplied verbatim in the
raw request, so Gate 0 does not apply and Gate 1 is satisfied by that request.

**Change-type row:** *AI workflow / agent config* (`.claude/**`,
`docs/ai_workflow/**`) — manual dry-run / self-review, plus tests because this
packet adds them.

---

## Section 0 — Requirements Brief

### Raw request (verbatim)

> Create a goal to resolve P1.8 and P1.3 as one agent-workflow integrity packet.
> Do not recreate .claude/SHARED_PLAN.md. Remove every active dependency on its
> missing tier/appendix definitions, including /handover, /unslop, /council-plan,
> PARALLEL_WORKFLOW.md, PLAN_REVIEW_TEMPLATE.md, and WORKSTREAM_OWNERSHIP.md;
> point each to the real canonical authority. Then permit handover in the
> senior-developer allowlist so /verify-and-polish can complete its documented
> final step. Add guard tests and perform the required agent-config dry run.
> Avoid historical archive churn. Publish a focused PR and stop merge-ready.

### Problem

Two independent ways for a correctly-behaving agent to be stopped by the repo's
own configuration:

1. **P1.8 — an authority that does not exist.** Six active command, charter, and
   workflow documents tell a reader to act "per `.claude/SHARED_PLAN.md`
   Tier 2.1 / Tier 2.2 / Appendix A1.1 / A1.2 / A2.1 / A2.2". The file is
   gitignored and absent. An agent instructed to consult a tier definition has
   nowhere to go, and the numbering it is asked to honor no longer maps to
   anything. The reverse failure is worse than the forward one: the numbering
   looks authoritative enough that a future session could *recreate* a
   SHARED_PLAN.md and re-import a tier system the project abandoned.

2. **P1.3 — a permitted command whose steps are not permitted.**
   `senior-developer` may invoke `/verify-and-polish`, whose documented step 4 is
   `/handover`, which its own skill guard denies. The agent starts a command it
   is allowed to run and is blocked partway through, after the expensive step 1
   has already burned a full pytest + Chromium run.

Neither is reachable by any existing gate. `Run Tests`, the E2E gates, Stylelint
and the visual matrix all operate on code; these files are configuration
expressed as prose.

### Verified premise (re-derived at `ed14bb3`, 2026-08-04)

**P1.8 — the v23 row names three documents. There are eleven reference sites
across eight files.** The row's own scoping ("three active workflow docs") is an
undercount, because no prior pass looked outside `docs/ai_workflow/`:

| # | Site | Current text | Class |
|---|---|---|---|
| 1 | [`.claude/commands/handover.md:5`](../../.claude/commands/handover.md) | "per `.claude/SHARED_PLAN.md` Appendix A1.1" | directive |
| 2 | [`.claude/commands/unslop.md:5`](../../.claude/commands/unslop.md) | "per `.claude/SHARED_PLAN.md` Appendix A1.2" | directive |
| 3 | [`.claude/commands/council-plan.md:5`](../../.claude/commands/council-plan.md) | "from `.claude/SHARED_PLAN.md` Tier 2.2" + broken relative link | directive + broken link |
| 4 | [`.claude/agents/architecture-reviewer.md:10`](../../.claude/agents/architecture-reviewer.md) | "an issue body, or a SHARED_PLAN tier" | input contract |
| 5 | [`.claude/agents/product-risk-reviewer.md:10`](../../.claude/agents/product-risk-reviewer.md) | identical | input contract |
| 6 | [`ai_workflow/PARALLEL_WORKFLOW.md:3`](../ai_workflow/PARALLEL_WORKFLOW.md) | "Implements … Tier 2.1" + broken link | implements-claim |
| 7 | [`ai_workflow/PLAN_REVIEW_TEMPLATE.md:3`](../ai_workflow/PLAN_REVIEW_TEMPLATE.md) | "Implements … Tier 2.2 Appendix A2.2" + broken link | implements-claim |
| 8 | [`ai_workflow/WORKSTREAM_OWNERSHIP.md:3`](../ai_workflow/WORKSTREAM_OWNERSHIP.md) | "Implements … Appendix A2.1" + broken link | implements-claim |
| 9 | [`ai_workflow/WORKSTREAM_OWNERSHIP.md:32`](../ai_workflow/WORKSTREAM_OWNERSHIP.md) | ghost file listed as a never-claimed shared path + broken link | broken link |
| 10 | [`ai_workflow/INDEX.md:9`](../ai_workflow/INDEX.md) | "optional local planning/audit trail if present; Tier 1 artifacts here should stand on their own" | hedged pointer |
| 11 | [`.gitignore:91`](../../.gitignore) | "# AI workflow scratch (see .claude/SHARED_PLAN.md Appendix A1.1, A2.1)" | directive in a comment |

Four of these carry a **relative Markdown link** to the absent file
(`../../.claude/SHARED_PLAN.md`) — sites 3, 6, 7, 8, 9 — which is the "4 genuine
active authority defects" the v23 link sweep counted. The other six are prose
directives the link sweep could not see, which is why the row undercounts.

**Orphaned numbering outside the SHARED_PLAN name.** The retired tier vocabulary
also survives in [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) at three
places — `:3` ("the canonical implemented version of the Tier 1 quality gate"),
`:37` ("All three Tier 2 reviewers"), `:51` ("untracked Tier 1-style artifacts").
These are self-contained labels rather than pointers, but they are the same
retired numbering, and leaving them preserves exactly the vocabulary this packet
exists to remove. Included.

**P1.3 — confirmed verbatim.**
[`senior-developer.md:30`](../../.claude/agents/senior-developer.md) passes
`-AllowedCsv run-tests,run-e2e,verify-suite,verify-and-polish,verify,run,build-css,run-hypertrophy-toolbox`.
[`verify-and-polish.md:11`](../../.claude/commands/verify-and-polish.md) makes
`/handover` step 4. [`guard-skill.ps1:10-13`](../../.claude/hooks/guard-skill.ps1)
exits **2** — the blocking code — on anything not in that CSV.

### Acceptance criteria

Each criterion is one file's observable end state.

1. Given each of the eleven sites above, when the packet lands, then none of them
   instructs a reader to consult `.claude/SHARED_PLAN.md`, and each carries a
   pointer to the authority that actually holds the rule.
2. Given [`ai_workflow/INDEX.md`](../ai_workflow/INDEX.md), when the packet
   lands, then its Spine section states positively that no shared-plan tier file
   exists and routes the four topics — gates, roles, checkout isolation, path
   claims — to their real owners. This is the anti-recreation control.
3. Given [`.gitignore`](../../.gitignore), when the packet lands, then the
   `.claude/SHARED_PLAN.md` **ignore rule survives** with a comment explaining
   why: it is the backstop that keeps a future local scratch file from being
   committed and re-establishing the ghost authority as tracked truth.
4. Given [`senior-developer.md`](../../.claude/agents/senior-developer.md), when
   the packet lands, then `handover` is in its `-AllowedCsv` and
   `guard-skill.ps1` exits 0 for it under every PowerShell host on the machine.
5. Given an unlisted skill name, when the same guard runs with the same
   allowlist, then it still exits 2 — the fix widens the allowlist by exactly one
   entry and does not weaken the guard.
6. Given `tests/`, when the packet lands, then a guard test fails if either
   defect is reintroduced: a new `SHARED_PLAN`/tier reference anywhere in the
   active agent-config surface, or a command step naming a skill its caller is
   not allowed to invoke.
7. Given [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)'s AI workflow /
   agent config row, when the packet lands, then its required manual dry-run has
   been performed and recorded in this document with commands and exit codes.

### In scope

- The eleven reference sites, plus the three `QUALITY_GATE.md` tier labels.
- One entry added to the `senior-developer` skill allowlist.
- One new pytest file of configuration-contract guards.
- Goal-doc pointers in the P1.3 and P1.8 rows of
  [`LEFTOVERS_BY_PRIORITY.md`](../LEFTOVERS_BY_PRIORITY.md), matching the
  precedent P1.4 set.
- Regenerated `docs/test_inventory/` artifacts, because this packet adds tests
  and `Test Inventory Drift` is a required context.

### Out of scope

- **Recreating `.claude/SHARED_PLAN.md` in any form.** Directed by the owner.
- **Historical records that mention the file.** Left byte-identical:
  [`CHANGELOG.md:174`](../CHANGELOG.md) (the entry that *retired* it),
  [`agent_roles/PLANNING.md:484`](../agent_roles/PLANNING.md) (self-review
  evidence from the refit that shipped), and
  [`MASTER_HANDOVER.md:1585`](../MASTER_HANDOVER.md) (a completed-workstream
  status row that already names the correct authorities). `docs/archive/**` and
  `docs/scan/**` are point-in-time records and are not touched.
- The two historical `workout_cool_integration/` broken links and the six in
  `archive/MISSING_TESTS_PART2.md`. The P1.8 row itself says to fix these "only
  if touched for other reasons" — they are not touched here.
- **Granting `senior-developer` the `Agent` tool.** See §2.
- Any change to `guard-skill.ps1` itself. The hook is correct; the data it was
  given was wrong.

### Assumptions

1. The owner's two decisions — *strip, do not restore* and *permit `handover`* —
   are the Gate 1 approval for this packet. Recorded verbatim above.
2. `/handover` writing `MASTER_HANDOVER.local.md` is inside `senior-developer`'s
   charter: the file is gitignored and lives in the assigned checkout, so rule 4
   ("never write outside the assigned checkout") is not engaged.

### Calculation surface

**None.** No file in scope touches Effective Sets, RIR/RPE, weekly/session
summaries, progression, fatigue, or any DB, route, or response contract. The
`CLAUDE.md` §1 refactor invariant is not engaged.

---

## §2 — The finding neither source row carries

**Permitting `handover` fixes step 4 of `/verify-and-polish`. Steps 2 and 3 stay
unexecutable by `senior-developer`, for a different reason.**

`senior-developer.md:5` sets `disallowedTools: Agent`. Steps 2 and 3 of
`/verify-and-polish` are "invoke the `code-reviewer` agent" and "invoke the
`unslop-reviewer` agent". So the same command has a second, unrelated blocked
step, and P1.3's framing — a *skill-guard* contradiction — does not cover it.

**This is not a defect to fix by widening the toolset.**
[`AUTONOMY.md`](../ai_workflow/AUTONOMY.md#workflow-roles) states that reviewers
"remain independent; developers do not approve their own work." Giving
`senior-developer` the `Agent` tool so it can spawn its own reviewers would
invert that invariant to close a documentation gap. The correct reading is that
`/verify-and-polish` steps 2–3 belong to the manager or the primary session, not
to the implementing agent.

**Disposition:** the command file gets one sentence stating who runs which steps.
That is a factual correction to a document this packet already opens, and it is
required for the packet's own claim to be true — without it, "so
`/verify-and-polish` can complete its documented final step" would ship alongside
two other steps that still cannot run, with nothing recording why. No toolset,
charter permission, or role boundary changes. Flagged here and in the PR body as
an addition beyond the literal instruction.

---

## §3 — Authority mapping

The replacement for each stripped claim. "Point to the real canonical authority"
resolves differently per site, because the retired tiers bundled four unrelated
topics:

| Retired reference | Real authority | Why |
|---|---|---|
| Tier 2.1 (parallel work) | [`PARALLEL_WORKFLOW.md`](../ai_workflow/PARALLEL_WORKFLOW.md) **is** the authority | `AUTONOMY.md` already defers to it for the tracked-DB commit rule; it implements nothing above itself |
| Tier 2.2 / Appendix A2.2 (plan review) | [`QUALITY_GATE.md#plan-stage-routing`](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) for routing; [`PLAN_REVIEW_TEMPLATE.md`](../ai_workflow/PLAN_REVIEW_TEMPLATE.md) for the artifact shell | `council-plan.md:7-11` *already* names QUALITY_GATE as canonical for routing — the ghost clause contradicted the line below it |
| Appendix A2.1 (path claims) | [`WORKSTREAM_OWNERSHIP.md`](../ai_workflow/WORKSTREAM_OWNERSHIP.md) **is** the authority | same shape as Tier 2.1 |
| Appendix A1.1 (handover layers) | [`MASTER_HANDOVER.md`](../MASTER_HANDOVER.md) is the committed layer; the command's own Steps are the whole contract | there is no second specification, and pretending otherwise is what created the ghost |
| Appendix A1.2 (polish gate) | [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) | `unslop.md:14` already derives targeted tests from it |
| "SHARED_PLAN tier" as reviewer input | `docs/<feature>/PLANNING.md` or an issue body | the two remaining input forms, both real |

---

## §4 — Derived verification gate

From the *AI workflow / agent config* row, plus what this packet actually adds:

| Gate | Why | Required |
|---|---|---|
| Manual dry-run / self-review | The row's stated requirement for `.claude/**` and `docs/ai_workflow/**` | yes — recorded in §5 |
| `guard-skill.ps1` execution under every installed PowerShell host | The fix changes hook input data; `test_guard_destructive_command.py` established that a guard green under one host can be a parser failure under another | yes |
| Full `pytest` | The packet adds a test file; the suite total moves | yes |
| `scripts/generate_test_inventory.py --check` | `Test Inventory Drift` is a required context and fails on any test add | yes |
| Chromium E2E | No template, JS, CSS, route, or util changes | **no** — the change-type row requires tests "only if source behavior changed", and no source behavior changed |
| `code-reviewer` / `unslop-reviewer` | The row names "`code-reviewer` or careful self-review" | self-review; recorded in §5 |

---

## §5 — Execution record

Branch `wt/agent-workflow-integrity`, worktree
`D:/development/Hypertrophy-Toolbox-v3-awi`, forked from `origin/main` @
`ed14bb3` (local `main` was **11 behind** at the time and would have been the
wrong base).

### What changed

| File | Change |
|---|---|
| `.claude/commands/handover.md` | directive → the two real layers + "the Steps below are the whole contract" |
| `.claude/commands/unslop.md` | directive → `QUALITY_GATE.md` is canonical for which tests/reviewers apply |
| `.claude/commands/council-plan.md` | ghost clause + broken link deleted; the line below it already named `QUALITY_GATE.md#plan-stage-routing` as canonical, so the ghost was contradicting its own next paragraph |
| `.claude/commands/verify-and-polish.md` | added the who-runs-which-step note (§2) |
| `.claude/agents/architecture-reviewer.md`, `product-risk-reviewer.md` | "or a SHARED_PLAN tier" dropped from the input contract |
| `.claude/agents/senior-developer.md` | `handover` appended to `-AllowedCsv` |
| `docs/ai_workflow/PARALLEL_WORKFLOW.md` | implements-claim → "this file is the canonical authority for checkout and DB isolation" |
| `docs/ai_workflow/WORKSTREAM_OWNERSHIP.md` | implements-claim → canonical-for-path-claims; the ghost file in the never-claimed list replaced by the rest of `.claude/` |
| `docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md` | implements-claim → owns the artifact shell only; gates are `QUALITY_GATE.md`'s |
| `docs/ai_workflow/INDEX.md` | hedged bullet → the positive anti-recreation note (criterion 2) |
| `docs/ai_workflow/QUALITY_GATE.md` | three retired tier labels at `:3`, `:37`, `:51` |
| `.gitignore` | comment rewritten; **ignore rule kept**, with the reason written down |
| `tests/test_agent_workflow_contracts.py` | new — six guard contracts |
| `docs/test_inventory/` | regenerated (required context) |
| `docs/LEFTOVERS_BY_PRIORITY.md` | goal-doc pointers on the P1.3 and P1.8 rows |

### Guard tests, and proof they can fail

`tests/test_agent_workflow_contracts.py` — **75 collected, 75 passed** in 1.9 s.

A guard that cannot fail is the defect class this repo already names (the
`occurrences <= 1` assertion, `measure.verify_blind_spots()`, and P2.5's
broken-icon visual gate). So both defects were reintroduced and the suite re-run:

| Reintroduced defect | Tests that red |
|---|---|
| `handover` removed from the allowlist | `test_allowed_commands_do_not_have_forbidden_steps[senior-developer]`; `test_skill_guard_decides…[handover-0-powershell]`; `[handover-0-pwsh]` |
| `Implements … SHARED_PLAN.md Tier 2.1` restored in `PARALLEL_WORKFLOW.md` | `test_surface_does_not_direct_readers_to_the_retired_plan_file[…]`; `test_surface_does_not_use_the_retired_tier_numbering[…]` |

**5 failed, 70 passed** with both defects present; both files then restored from
backup and the suite returned to 75/75.

**One design choice worth recording.** The hook test is parametrized over both
PowerShell hosts *unconditionally* and skips at run time.
`test_guard_destructive_command.py` decides its hosts at collection time, which
makes its node count machine-dependent and forced an entry in
`ENVIRONMENT_DEPENDENT_PYTEST_FILES`. Doing it at run time keeps this file's
count identical on Windows and the ubuntu runner, so no exception entry is
needed — one fewer place for a real diff to hide.

### Dry run — required by the AI workflow / agent config row

**(a) Skill-guard decision table.** The real
[`guard-skill.ps1`](../../.claude/hooks/guard-skill.ps1), the real post-change
allowlist, 15 skill names × 2 hosts = 30 invocations:

- **allow (exit 0)** — `handover`, `verify-and-polish`, `verify-suite`,
  `run-tests`, `run-e2e`, `build-css`, `run`, `verify`,
  `run-hypertrophy-toolbox`
- **deny (exit 2)** — `council-plan`, `unslop`, `requirements`, `worktree`,
  `status`, and the empty skill name

Identical under `powershell` (5.1) and `pwsh` (7). The allowlist widened by
exactly one entry and the guard still denies everything else — criteria 4 and 5.

**(b) Link resolution.** Every relative Markdown link in the 15 changed
documents: **180 resolve, 0 broken**, including the two anchors this packet
introduces (`AUTONOMY.md#workflow-roles`, `QUALITY_GATE.md#plan-stage-routing`).
Before the change, five of these files carried a link to a file that does not
exist.

**(c) Routing self-check.** `git status --short --untracked-files=all` against
the production globs returns **nothing** — no `routes/`, `utils/`, `static/`,
`templates/`, `scss/`, `e2e/`, or `app.py`. No source behavior changed, so the
change-type row's "run tests only if source behavior changed" is satisfied and
the Chromium suite is correctly not required.

### Test and static-analysis evidence

| Command | Result |
|---|---|
| `pytest tests/ -q` | **2518 passed, 2 skipped** in 530.83 s |
| `pytest tests/test_agent_workflow_contracts.py -q` | 75 passed |
| `generate_test_inventory.py` then `--check` | "Test inventory is up to date." |
| `npx pyright tests/test_agent_workflow_contracts.py` | 0 errors, 0 warnings, 0 informations |

The 2 skips are pre-existing platform skips, not introduced here — one is
`test_package_asset_staging.py:242` ("Windows filesystems carry no executable
bit"). The new file skips nothing on this host: both PowerShell hosts are
installed, so all 8 hook nodes ran.

### Two additions beyond the literal instruction, both flagged

1. **The `/verify-and-polish` who-runs-which-step note** — reasoned in §2. Without
   it this packet would claim to let the command "complete its documented final
   step" while two other steps stay unexecutable, with nothing recording why.
2. **`WORKSTREAM_OWNERSHIP.md:32`** — the dead entry sat in a *never-claimed
   shared paths* list beside `.claude/settings.json`. Deleting it alone would
   have implied agent charters, commands, and hooks are claimable. Three
   concurrent worktrees hold copies of exactly those files today, so the entry
   was replaced with the rest of `.claude/` rather than removed.

### Deliberately not touched

`CHANGELOG.md:174`, `agent_roles/PLANNING.md:484`, `MASTER_HANDOVER.md:1585`,
`docs/archive/**`, `docs/scan/**`. All are point-in-time records; the handover
row additionally already routes readers to the correct authorities. Rewriting
completed history to remove a word is the archive churn this packet was told to
avoid.

### Known overlap with the in-flight P1.1 packet

`docs/doc_truth/PLANNING.md` (P1.1, Gate 0 pending) also edits
`ai_workflow/INDEX.md` and `ai_workflow/QUALITY_GATE.md`. The line ranges are
disjoint — P1.1 targets INDEX's *Active feature plans* section and
QUALITY_GATE's `:114-116` branch-protection claim plus its visual-red state;
this packet touches INDEX's Spine and QUALITY_GATE `:3`, `:37`, `:51`. Textual
conflict is unlikely but whichever lands second should rebase rather than
force-resolve.

---

## §6 — Definition of done

Item 1 of the [LEFTOVERS §6](../LEFTOVERS_BY_PRIORITY.md) closure rule:
implementation and proportional verification landed on `main`, the **P1.3** and
**P1.8** rows retired from `LEFTOVERS_BY_PRIORITY.md`, and this document
banner-flipped to SHIPPED with the merge SHA.

Per the raw request the PR **stops merge-ready** — opened, green, and not merged.
Row retirement therefore happens after the owner merges, not in this packet.

---

*Created 2026-08-04 against `origin/main` @ `ed14bb3`. Site counts are snapshot
evidence: re-grep before acting.*
