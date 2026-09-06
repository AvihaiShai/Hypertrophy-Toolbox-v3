# Plan Review — Prevention-first worktree cleanup sequence

*Requirements-only artifact. Technical-design evidence:
[`WORKTREE_CLEANUP_PLAN.md`](../ai_workflow/WORKTREE_CLEANUP_PLAN.md). This
Section 0 grants no implementation, preservation, quarantine, removal, prune,
ref-change, reconciliation, or other cleanup authority.*

## Section 0 — Requirements Brief

**Raw request** (verbatim)

> /requirements Create Section 0 only in docs/worktree\_cleanup/PLANNING.md for this request:
>
> “Start with prevention, then finish the open developments, then start the cleanup plan.”
>
> Use docs/ai\_workflow/WORKTREE\_CLEANUP\_PLAN.md as technical-design evidence.
>
> Required sequence:
>
> 1. The first implementation tranche is Operation A prevention only.
> 2. Operations B–E remain unauthorized during this tranche.
> 3. After prevention is landed, finish or explicitly disposition every open development through its normal workflow without removing its worktree.
> 4. After a stabilization checkpoint, regenerate all live evidence and begin separately approved cleanup operations.
> 5. Operation E remains independently planned and approved.
>
> Surface every assumption and blocking question. Do not implement prevention or execute cleanup. Stop for explicit Gate 0 owner sign-off.

**Problem**

The technical design defines five independently completable operations, but it does
not yet record the owner's stricter rollout order: prevention must complete first;
existing development must then be completed or explicitly dispositioned while its
worktrees remain intact; only after a stabilization checkpoint may current evidence
be regenerated and separately approved cleanup work begin. Without this requirements
gate, the design's independence rules could be misread as permission to start B, C,
D, or E alongside A, or to remove a development worktree through ordinary teardown
before preservation and cleanup approval.

**Technical-design evidence and precedence**

- [`§1.2`](../ai_workflow/WORKTREE_CLEANUP_PLAN.md#12-five-independently-completable-operations)
  defines Operations A–E and their technical dependencies. This brief adds a stricter
  program sequence; it does not weaken any dependency, safety rule, or approval.
- [`§1.3`](../ai_workflow/WORKTREE_CLEANUP_PLAN.md#13-planning-artifact-landing-gate)
  requires this council artifact, Gate 0, Plan v1/v2, reviewer provenance, and Gate 1
  before A may be implemented.
- [`§5`](../ai_workflow/WORKTREE_CLEANUP_PLAN.md#5-operation-a---prevention-and-lifecycle-compliance)
  is the complete technical boundary of the first implementation tranche.
- [`§11`](../ai_workflow/WORKTREE_CLEANUP_PLAN.md#11-completion-and-retention)
  defines `PREVENTION_COMPLETE` as A being merged, installed, tested, with lifecycle
  monitoring active. That outcome is the proposed meaning of “prevention is landed.”
- [`§3`](../ai_workflow/WORKTREE_CLEANUP_PLAN.md#3-evidence-disposition-and-candidate-model)
  requires fresh, dated evidence and explicit dispositions rather than stale counts
  or age-based conclusions.
- [`§9`](../ai_workflow/WORKTREE_CLEANUP_PLAN.md#9-operation-e---separate-main-reconciliation)
  keeps E outside worktree-cleanup completion and requires its own plan and approval.

If this brief and the technical design appear to conflict, the stricter no-authority
or sequencing condition controls until the owner resolves the conflict through the
applicable gate. Gate 0 approval confirms requirements only; it does not approve a
Plan v1/v2, Operation A implementation, a B–D operation, or Operation E.

**Acceptance criteria**

1. Given this Section 0 is unsigned, when any participant reads it, then the only
   authorized change is the requirements artifact itself; no prevention
   implementation or cleanup action is authorized.
2. Given Gate 0 is signed and a later council-reviewed Plan v2 receives Gate 1 owner
   approval, when the first implementation tranche starts, then every implementation
   artifact and action is bounded to Operation A as defined by technical-design
   [`§5`](../ai_workflow/WORKTREE_CLEANUP_PLAN.md#5-operation-a---prevention-and-lifecycle-compliance).
3. Given the Operation A tranche is active, when work is proposed under Operations
   B, C, D, or E, then it remains unauthorized: no live preservation or quarantine,
   no removal or prune, no branch/ref reconciliation, and no B–E production launcher
   or mutation/copy primitive may run.
4. Given A is merely coded or merged but its user-level installation, verification,
   or lifecycle monitoring is incomplete, when sequencing is evaluated, then the
   open-development phase does not start. It starts only after the technical design's
   `PREVENTION_COMPLETE` outcome is recorded.
5. Given `PREVENTION_COMPLETE`, when the transition to open-development closeout is
   proposed, then a fresh read-only inventory establishes the owner-approved universe
   of open developments and its cutoff, including open PRs, active ownership claims,
   active workstreams, registered worktrees, and any additional owner-declared work.
6. Given an open development is in that universe, when it is handled, then it reaches
   either its normal completed outcome or an explicit owner disposition through its
   existing workflow and gates. Cleanup tooling is not used to finish, normalize, or
   disposition development content.
7. Given an open development is completed, abandoned, kept, or deferred during this
   phase, when its normal workflow closes or records that decision, then its worktree
   remains registered and present. No worktree removal, manual directory deletion,
   mutating prune, or cleanup-by-ordinary-teardown is permitted.
8. Given every in-scope open development has a recorded terminal result or explicit
   owner disposition and no blocking ambiguity remains, when the owner evaluates the
   stabilization checkpoint, then the owner must explicitly record that the agreed
   checkpoint criteria have passed before cleanup planning or operations advance.
9. Given the stabilization checkpoint passes, when cleanup preparation resumes, then
   all volatile live evidence is regenerated from current state under the technical
   design's reproducible predicates. Earlier counts, SHAs, paths, process lists,
   statuses, and remote advertisements are not carried forward as current evidence.
10. Given live evidence has been regenerated, when cleanup begins, then each permitted
    B–D operation still requires every technical-design prerequisite and its own
    applicable owner approval; Gate 0, Gate 1 for A, `PREVENTION_COMPLETE`, development
    dispositions, or the stabilization checkpoint grants none of those approvals.
11. Given Operation E is considered at any time, when authority is checked, then E
    remains a separate source-control-maintenance effort with its own plan, manifest,
    reviews, and owner approval; it is not implied by approval or completion of A–D,
    and the technical design's `PRESERVATION_COMPLETE` prerequisite remains binding.
12. Given a later phase proposes deleting a retained worktree, branch/ref, archive,
    quarantine, or preservation object, when authority is checked, then that deletion
    requires the exact separate operation, manifest, and approval required by the
    technical design; no earlier disposition is deletion authority.

**Calculation surface**

- `none` — this requirements packet changes no application behavior, database schema,
  API contract, or hypertrophy calculation.

**In scope**

- Requirements and acceptance criteria for the sequence: Gate 0 → separately approved
  Operation A tranche → `PREVENTION_COMPLETE` → normal closeout/disposition of the
  agreed open-development universe while retaining worktrees → owner-recorded
  stabilization checkpoint → fresh live evidence → separately approved cleanup.
- Explicit authorization boundaries for A, B–D, and E.
- Assumptions and blocking owner decisions needed before Plan v1 may be drafted.
- The technical design as evidence, without treating it as execution authority.

**Out of scope / non-goals**

- Plan v1, council review, response matrix, Plan v2, Gate 1, or implementation-gate
  evidence.
- Implementing, installing, or testing Operation A prevention controls.
- Starting, preflighting, preserving, quarantining, removing, pruning, reconciling,
  or otherwise executing any part of Operations B–E.
- Finishing or dispositioning an actual open development, changing or removing any
  worktree, or changing any branch, ref, PR, ownership claim, runtime, database,
  environment, archive, or quarantine.
- Generating or relying on point-in-time live cleanup evidence during this Gate 0
  packet.
- Planning or approving Operation E.
- Adding the planning artifact's INDEX/current-state pointer, regenerating test
  inventory, or preparing its landing PR; those belong to the later isolated
  planning/CI lane required by technical-design §1.3.

**Assumptions made**

- ⚠️ **A1 — “landed” means `PREVENTION_COMPLETE`.** A must be merged, installed,
  tested, and monitored as defined by technical-design §11; merge alone is
  insufficient.
- ⚠️ **A2 — this is a stricter sequence than the design's independence diagram.**
  Even though B is technically independent of C–E, none of B–E starts before A,
  open-development closeout, stabilization, fresh evidence, and its separate
  approval.
- ⚠️ **A3 — “open development” is broader than open PRs.** It includes the live
  ownership/worktree state and owner-declared work at an agreed cutoff. Parked or
  unsigned proposals are included only if the owner says they are open development,
  not merely because documentation mentions them.
- ⚠️ **A4 — “explicitly disposition” may be non-completion.** A recorded owner
  decision such as abandon, keep, or defer can satisfy this phase if it uses the
  development's normal governance and states its rationale and next condition/date;
  silence, age, a closed PR, or a missing owner cannot.
- ⚠️ **A5 — worktree retention is literal.** Normal closeout may merge or close work,
  but it may not remove or unregister that development's worktree. Retention does not
  itself classify the worktree as a later cleanup candidate.
- ⚠️ **A6 — recovery roots should not be retired during the interlude.** Until fresh
  preservation evidence and the applicable operation approval exist, branch/ref or
  local-only source retirement is presumed forbidden even if a development's usual
  closeout would perform it.
- ⚠️ **A7 — stabilization is an owner gate, not elapsed time alone.** It requires an
  agreed state/evidence checklist and explicit owner acknowledgement; no unstated
  waiting period is assumed.
- ⚠️ **A8 — “regenerate all live evidence” means fresh read-only discovery evidence
  first.** It does not silently start Operation C, create archive refs, copy live
  trees, open databases, or invoke any B–E mutation/copy primitive.
- ⚠️ **A9 — later “cleanup operations” means B, C, and approved D slices under their
  existing technical dependencies and separate approvals.** It does not fold E into
  the cleanup campaign.
- ⚠️ **A10 — E retains the design's timing rule.** E may be considered only after
  `PRESERVATION_COMPLETE` under its own plan and approval, even if some D slices are
  deferred; no decision to commission E is made here.
- ⚠️ **A11 — this file is a draft requirements artifact in the current workspace.**
  Its eventual landing, INDEX/current-state pointer, and test-inventory check must use
  the owner-created isolated lane required by technical-design §1.3; this edit does
  not claim that landing gate has run.
- ⚠️ **A12 — no current counts or identities are durable requirements.** The open-
  development universe and cleanup evidence will be generated at their named future
  checkpoints rather than copied from today's potentially stale state.

**Open questions for the user**

- **Q1 (blocking) — open-development universe and cutoff:** Should A3 be accepted as
  written? In particular, do parked/owner-decision-gated items count only when the
  owner explicitly declares them active, and are developments opened after the
  cutoff prohibited until stabilization or added to the same closeout universe?
- **Q2 (blocking) — allowed explicit dispositions:** Which normal-workflow outcomes
  satisfy “explicitly disposition”: only completed/merged or intentionally abandoned,
  or also KEEP and time-bounded DEFERRED with rationale, owner, next condition, and
  review date?
- **Q3 (blocking) — retained source-control roots:** During the development-closeout
  interlude, must attached branches, detached/archive refs, reflogs, and local-only
  source roots remain intact as A6 proposes, or may a normal workflow retire any of
  them while retaining the physical worktree?
- **Q4 (blocking) — stabilization checkpoint:** What exact observable checklist and,
  if desired, quiet period define stabilization? At minimum, should it require every
  in-scope development disposition recorded, no unresolved ownership/activity state,
  normal workflow gates settled, lifecycle-ledger/worktree reconciliation clean, and
  no active writer or Git operation?
- **Q5 (blocking) — evidence boundary:** Does “regenerate all live evidence” mean the
  read-only discovery/assessment evidence in technical-design §3 before any B–D
  approval, as A8 proposes, or should some separately approved preservation artifact
  be generated at that point too?
- **Q6 (blocking) — post-checkpoint operation order:** After fresh evidence and
  separate approvals, should the technical design's dependency model remain intact
  (B independently schedulable; C before D; D in approved slices), or does the owner
  require the stricter serial order B → C → D?
- **Q7 (blocking) — Operation E timing:** Should A10 be accepted, preserving the
  design's option to plan and run E after `PRESERVATION_COMPLETE` even when D is
  incomplete, or must E wait until the entire D campaign is complete?
- **Q8 (blocking) — artifact landing:** After Gate 0, should the next separately
  authorized action be creation of Plan v1 plus the required INDEX/current-state
  pointer in the §1.3 owner-created standalone-clone lane, with no Operation A code
  started until council review and Gate 1 sign-off?

### Section 0 sign-off — GATE 0

**Current status:** Gate 0 signed by the owner on 2026-09-05 for requirements
only. The final dated entry below resolves the earlier pending record; the
proposals and decision-record boundary are retained as historical evidence.
Gate 1 and all implementation/operation approvals remain pending. The standalone-
clone landing and isolation obligations have not been performed by this edit.

#### 2026-09-05 — Proposed blocker resolutions for owner review

These are assistant recommendations prepared in response to the request to fill
the Gate 0 blockers. They are not recovered owner decisions or a Gate 0 signature.
The original A1–A12 and Q1–Q8 remain above for traceability.

| Question | Proposed resolution |
|---|---|
| Q1 | Accept A3. Establish the owner-approved inventory and cutoff after `PREVENTION_COMPLETE`. Parked proposals count only when explicitly declared active. Add any development opened after the cutoff to the same closeout universe before stabilization can pass. |
| Q2 | Allow normal completed/merged outcomes, intentional abandonment, KEEP, and time-bounded DEFERRED. Every non-completion disposition records rationale, accountable owner, next condition, and review date. None authorizes worktree or source-root retirement. |
| Q3 | Accept A6. Retain attached branches, detached/archive refs, reflogs, and local-only source roots; prohibit explicit retirement, reflog expiration, and object cleanup during the interlude. Normal development may advance branches and append reflogs through its existing workflow. |
| Q4 | Require a reconciled closeout inventory, a result or explicit disposition for every member, settled applicable workflow gates, no unresolved ownership/activity ambiguity, a reconciled lifecycle ledger and worktree inventory, and no active writer or Git operation at the checkpoint. Record explicit owner acceptance. Require no fixed quiet period; later drift invalidates affected evidence and must be resolved before an operation proceeds. |
| Q5 | Accept A8: regenerate read-only discovery and assessment evidence first. Live preservation, archive-ref creation, database opening, and B–E copy/mutation primitives retain their separate prerequisites and approvals. |
| Q6 | Keep the technical dependency model after stabilization and fresh evidence: B independently schedulable, C before D, and D in individually approved slices. Do not impose B → C → D serial execution. |
| Q7 | Accept A10: E may be separately planned and approved after `PRESERVATION_COMPLETE` even if D is incomplete. This packet does not commission E. |
| Q8 | After explicit Gate 0 sign-off, prepare Plan v1 and the required pointers in the owner-created §1.3 standalone-clone lane, then obtain council review, a response matrix, Plan v2, and explicit Gate 1 approval before Operation A implementation. Preserve the recorded isolation and shared-path coordination obligations. |

**Assumption disposition proposed:** Accept A1–A12 with the Q1–Q8
clarifications above. Q3 preserves recovery roots without preventing the normal
branch advancement needed to finish development.

**Q6/A2 consistency:** A2 governs the sequence before cleanup becomes eligible;
Q6 governs scheduling after that sequence and each operation's approvals. B's
technical independence does not permit it to bypass prevention, development
closeout, stabilization, or fresh evidence.

**Missing riders and R1/AC8 consistency:** Neither rider's text, including R1,
is available in this artifact. Do not invent either rider or assert that R1 agrees
with acceptance criterion 8. The owner must supply the two riders or explicitly
withdraw their inclusion requirement. AC8 remains the explicit owner-recorded
stabilization gate unless an approved decision changes it.

**Remaining Gate 0 blockers:** Owner acceptance/correction of these proposals;
supply or explicit withdrawal of the two riders and reconciliation with AC8;
and explicit requirements-only Gate 0 sign-off. The four boxes below remain
unchecked until those assertions are supported. Later operation-specific choices
in technical-design §12 remain at their respective gates.

#### 2026-09-05 — Owner instructions and decision-record boundary

The owner requests a complete dated decision record, both riders, the R1/AC8 and
Q6/A2 consistency notes, and all four Gate 0 boxes checked. The original assumptions
A1–A12 and questions Q1–Q8 above are preserved as the original record. The decisions
and rider text are not present in the available request or drafts; their exact
content has been requested from the owner. Until supplied, this block records only
the explicit instructions below and does not attest that Q1–Q8 have been answered
or that the complete Gate 0 record has been reconciled.

- **Pre-landing status and lane ownership:** The current files are pre-landing
  drafts. The owner will create the §1.3 standalone clone. This record does not
  claim that migration or the landing gate has been completed.
- **Isolation before collection:** In that lane, redirect `TEMP`, `TMP`,
  `HT_RUNTIME_DIR`, `DB_FILE`, caches, and bytecode to scratch **before any test
  collection or inventory check**. Before either command, verify that the clone
  has no alternates or hardlinks to the live object store and that runtime and
  temporary paths cannot resolve to the live database or logs. Record the isolation
  evidence before proceeding; isolation has not been verified in this step.
- **Current-state pointer:** Prepare the `docs/MASTER_HANDOVER.md` pointer in that
  isolated lane using normal per-edit shared-path coordination under
  `WORKSTREAM_OWNERSHIP.md`. This is a future lane obligation, not a pointer edit
  in the shared checkout during this step.
- **User-level authority:** Technical-design §12 requires the owner's explicit
  approval of the user-level guard/memory changes and the lifecycle mechanism.
  Gate 0 does not substitute for that approval. Technical-design §4.6 assigns
  user-level mutations to the owner; an agent does not perform them.
- **Draft retention and cleanup review:** Leave the shared-checkout drafts and
  existing `docs/ai_workflow/INDEX.md` edit in place. After verified migration,
  present the exact proposed source-checkout cleanup, including affected paths and
  proposed changes, for owner review before any source cleanup is performed.
- **This step's boundary:** Update only this Gate 0 record and show the diff.
  Stop before Plan v1 or implementation. No clone creation, migration, pointer
  edit, runtime change, collection, inventory check, or cleanup is performed here.

**Pending record completion:** Insert the complete owner decisions and both riders,
then record their R1/AC8 and Q6/A2 consistency notes without rewriting the original
assumptions or questions. Check all four boxes once their assertions are supported
by that record. No missing decision or rider is inferred from the request to check
the boxes.

#### 2026-09-05 — Owner approval and reconciled requirements-only Gate 0

**Owner approval (verbatim):**

> I approve the proposed Q1–Q8 resolutions and accept A1–A12 with those clarifications. I withdraw the requirement for the two unspecified riders; AC8 remains unchanged.
>
> I confirm the problem statement and acceptance criteria and explicitly sign Gate 0 for requirements only.
>
> Reconcile the dated decision record, preserve the original questions and historical record, and check the four supported Gate 0 boxes. Stop before Plan v1 or implementation. Give me the next prompt for Operation A council planning in the owner-created standalone clone.

**Final decision record:** All eight resolutions in the dated proposed-resolution
table above are now owner-approved, without changes. A1–A12 are accepted with
those Q1–Q8 clarifications. The original assumptions, questions, proposals, and
earlier pending statements remain intact for traceability; this entry supersedes
their unresolved status and the earlier request to insert both riders.

**Riders and R1/AC8 consistency:** The owner explicitly withdrew the inclusion
requirement for both unspecified riders. Neither rider is supplied, inferred, or
adopted, and no claim of R1/AC8 agreement is made. AC8 remains unchanged: the owner
must explicitly record that the agreed stabilization checkpoint has passed before
cleanup planning or operations advance. The approved Q4 resolution defines the
checkpoint checklist and requires no fixed quiet period.

**Q6/A2 consistency:** Both are accepted. A2 retains the prevention → open-
development closeout → owner-accepted stabilization → fresh evidence sequence
before cleanup becomes eligible. Q6 then retains B's independent scheduling,
C before D, and individually approved D slices; it does not bypass A2 or require
B → C → D serial execution. Q7 preserves E's separate planning and approval after
`PRESERVATION_COMPLETE`, even if D is incomplete; E is not commissioned here.

**Authority and remaining gates:** No Gate 0 blockers remain. This signature
approves requirements only. Q8 identifies the next planning step in the owner-
created §1.3 standalone clone; this edit stops before Plan v1, council review,
Plan v2, Gate 1, or implementation. The prior isolation, shared-path coordination,
draft-retention, and user-level authority obligations remain binding. The later
operation-specific decisions in technical-design §12 remain open at their
respective gates; no landing, collection, inventory check, or cleanup is claimed.

- [x] Owner confirms the problem statement and acceptance criteria match the request.
- [x] Owner accepts or corrects assumptions A1–A12.
- [x] Owner answers blocking questions Q1–Q8.
- [x] Owner explicitly signs Gate 0, acknowledging that this approves requirements
  only and grants no authority to implement A or execute B–E.

---

## 2026-09-05 — Operation A council planning authorization

The original Section 0 above is preserved verbatim as the historical requirements
packet. Its final 2026-09-05 decision is signed; earlier pending questions are not
reopened. This dated continuation records the separately requested council work.
Gate 1 remains unsigned. Nothing in this continuation implements A or executes B–E.

**Council request (verbatim)**

> Continue the worktree-cleanup packet through Operation A council planning only.
>
> Read CLAUDE.md, docs/MASTER\_HANDOVER.md, docs/worktree\_cleanup/PLANNING.md,
> docs/ai\_workflow/WORKTREE\_CLEANUP\_PLAN.md, and the canonical council,
> quality-gate, and ownership instructions.
>
> Treat the final 2026-09-05 Gate 0 decision as signed. Preserve the
> requirements and historical record; do not reopen resolved questions.
>
> First verify this is the owner-created standalone clone required by
> technical-design §1.3, not a linked worktree. Before any collection or
> inventory check, redirect TEMP, TMP, HT\_RUNTIME\_DIR, DB\_FILE, caches, and
> bytecode to scratch. Record proof that the clone has no alternates or
> hardlinks to the live object store and cannot use the live database or logs.
>
> Copy any missing planning drafts and the intended INDEX change from
> D:\development\Hypertrophy-Toolbox-v3-main without overwriting differing
> destination content. Leave the source drafts and INDEX edit intact.
> Prepare the MASTER\_HANDOVER.md pointer using required shared-path coordination.
>
> Run the /council-plan workflow:
>
> - Keep the manager read-only; delegate planning-document writes to product-manager.
> - Draft Plan v1 for Operation A: prevention guards, safe SQLite snapshot
>   seeding, lifecycle reporting, workflow corrections, and applicable tests.
> - Obtain independent architecture-reviewer, test-strategist, and
>   product-risk-reviewer reviews.
> - Record actual agent provenance, verbatim findings, a complete response
>   matrix, and Plan v2 in docs/worktree\_cleanup/PLANNING.md.
> - Preserve B–E safety contracts and dependencies; defer their implementation
>   details to their later operation gates.
>
> Complete the isolated planning-artifact checks required by §1.3, including
> tracked/staged visibility before the inventory check. Regenerate inventory
> only after proved drift.
>
> Present Plan v2, the diff, validation evidence, and any remaining decisions
> for explicit Gate 1 approval for Operation A. Stop there.
>
> Do not implement A, mutate user-level settings, execute B–E, or clean up
> the source checkout. If the required clone or isolation is unavailable,
> report the exact missing prerequisite.

**Clone continuation (verbatim)**

> I created the standalone clone at:
> D:\development\Hypertrophy-Toolbox-worktree-cleanup-plan
>
> Continue here. Verify its isolation before collection or inventory checks.
> The uncommitted planning drafts and INDEX edit remain in the source checkout;
> copy them into this clone as previously instructed, preserving the originals.
> Proceed through Operation A council planning and stop for Gate 1 approval.

## Plan v1

**Goal:** Prevent another path-conversion incident and uncontrolled worktree
accumulation while giving each newly created worktree a consistent, isolated
SQLite seed and keeping all existing development and recovery roots intact.

**Scope**

- **In:** Operation A in technical-design §5: bounded project/owner-level guard
  contract; fresh-session inherited-state preflight; consistent `copy-current`
  snapshots; reconciled lifecycle and drive-root reporting; creation integration;
  active workflow/guidance corrections; focused executable contracts and gates.
- **Out:** A implementation in this planning turn; all B–E launchers, preservation,
  source copying, quarantine, removal, prune, ref retirement/reconciliation, and
  live recovery; source-checkout cleanup; agent-performed external or user-level
  mutations; application schema/API/calculation/UI changes.
- **Calculation surface:** `none`. No hypertrophy functions, weights, terms,
  response shapes, application backups, startup sequence, or product workflows
  change. The `copy-current` developer-tool behavior change gets explicit PR
  migration notes and tests.

**Grounding, not approval evidence:** The destination's measured HEAD is
`85e23725bc2871c5f005162f29be231a2f106b85`. Its `new-worktree.ps1` uses a raw
`Copy-Item -Force` in `copy-current`; active worktree guidance still contains
force/prune/branch-retirement advice. Its guard does not contain the later named
MSYS-variable denial described in the source's historical handover. The clone
and source HEAD are equal; the source has an uncommitted guard implementation
different from the clone's committed guard. Importing that source implementation
is not part of migrating the two planning drafts and INDEX edit. Before future implementation,
re-read the chosen base and account for already landed prevention work without
silently overwriting either checkout or declaring untested code compliant.

**Artifacts proposed for A implementation, after Gate 1**

| Path | Change | Owner / purpose |
|---|---|---|
| `.claude/hooks/guard-destructive-command.ps1` | Modify only measured gaps | senior-developer; bounded MSYS suppression denial, existing BOM/ASCII/fail-closed semantics |
| `.claude/settings.json`; shell-capable `.claude/agents/senior-developer.md`, `.claude/agents/automation-qa.md`, plus any newly discovered shell-capable registrations | Verify/update effective registrations | senior-developer; every installed hook surface and both profiles; each `.claude` edit coordinated |
| `scripts/preflight-worktree-environment.ps1` | New standalone preflight | senior-developer; inspect Process/User/Machine suppression state, resolved runtime and approved roots without application import |
| `scripts/new-worktree.ps1` | Modify | senior-developer; fail-closed lifecycle preflight, safe snapshot integration, atomic annotation after Git success |
| `scripts/seed_worktree_snapshot.py` | New standalone stdlib utility | senior-developer; SQLite-native backup and validation with no application import or live logging |
| `scripts/audit-worktrees.ps1` | New read-only report | senior-developer; Git/filesystem/annotation projection plus approved drive-root baseline comparison |
| `CLAUDE.md`; `.claude/commands/status.md`, `.claude/commands/worktree.md`; `docs/ai_workflow/PARALLEL_WORKFLOW.md`, `AUTONOMY.md`, `WORKSTREAM_OWNERSHIP.md` | Correct active instructions | senior-developer; preserve root size cap and shared-path per-edit coordination |
| Owner-enumerated active memory, local handover, retained-checkout and user-level guidance | Prepare exact proposed deltas; owner applies external/user-level edits | No blanket write permission; keep historical incident quotations explicitly non-prescriptive |
| `tests/test_guard_destructive_command.py`; `tests/test_agent_workflow_contracts.py` | Extend actual guard/config coverage | automation-qa |
| `tests/worktree_cleanup/guard-contract.ps1` | New standalone immediate guard harness | automation-qa; no pytest/conftest/application imports |
| `tests/test_worktree_environment_preflight.py`, `tests/test_worktree_snapshot.py`, `tests/test_worktree_lifecycle.py` | New scratch-only behavioral contracts | automation-qa; invoke infrastructure scripts against explicit disposable roots |
| `docs/test_inventory/` | Generated only after demonstrated drift | generated artifact; never hand-edit |
| `docs/worktree_cleanup/PLANNING.md`; coordinated `docs/MASTER_HANDOVER.md` pointer | Council record and current-state evidence | product-manager owns this planning document; delegated support owns pointer |

**Effort:** L, three implementation units (guard/guidance, snapshot, lifecycle)
followed by integrated acceptance. **Owner:** read-only manager routes
senior-developer implementation and automation-qa tests within one owner-created
isolated manager checkout; owner installs user-level changes and approves gates.
**Depends on:** signed Gate 0, explicit Gate 1 for A, §1.3 isolated planning checks;
future PREVENTION_COMPLETE also depends on owner installation and live monitoring.

### A1. Bounded prevention guard and guidance

1. Enumerate installed PowerShell 5.1/7 hosts, effective project and shell-agent
   registrations, both `main`/`agent` profiles and `bypassPermissions` behavior.
   Name absent hosts as unavailable, never passed. Codex's currently available
   command-tool transport is not evidence of Claude hook interception; report
   actual interception and advisory-only surfaces separately.
2. Deny observable assignment/export of `MSYS_NO_PATHCONV` or
   `MSYS2_ARG_CONV_EXCL`, including direct, `env`, `cmd`, PowerShell, .NET,
   `setx`, chained, multiline, and nested command-text forms. Preserve exit 2
   on deny/internal failure and the UTF-8 BOM plus ASCII contract. A fresh-session
   preflight checks inherited Process/User/Machine values and fails closed while
   either variable is present; agents never clear persistent settings themselves.
3. Keep the guard's limits explicit: raw command text cannot prove expanded native
   argv, script contents, alias/function expansion, executable identity, opaque
   destinations, or all child processes. Known literal-output heuristics must have
   tests and cannot be sold as a complete native-process boundary.
4. Require drive-qualified native output paths, PowerShell end to end and argument
   arrays for cleanup writes. Safe Git blob reads resolve exactly one full blob OID
   via `ls-tree` and pass that OID separately to `cat-file blob`. Verify these safe
   reads and normal development commands remain allowed.
5. Correct active guidance and remove prescriptive suppression/POSIX-native-output,
   `branch -D`, mutating prune and forced teardown advice. Preserve historical
   quotations with clear incident context. The operation's discovered snapshot
   retention overrides rotation only for this packet, not normal future rotation.

### A2. Consistent SQLite snapshot seeding

1. `copy-current` selects the current checkout's explicit source database; resolve
   and report absolute source/target identities before opening, reject aliasing,
   reparse redirection, source=target, or destination collisions. Missing source or
   unavailable snapshot/validation capability is a failure, not a success warning.
   Honor any documented runtime override only after explicitly verifying its
   resolved source identity; never silently fall through to a different database.
2. Proposed scoped exception requiring Gate 1 approval: this standalone
   infrastructure helper uses Python stdlib `sqlite3` directly, with a read-only
   source URI and no `DatabaseHandler`, application config, app, or logger imports.
   `DatabaseHandler` changes connection journal settings and checkpoints on close;
   importing it also binds application logging, contrary to the isolated utility's
   purpose. Application DB access continues to use `DatabaseHandler` unchanged.
   Infrastructure diagnostics use explicit return codes and caller-captured output,
   not the application's log tree. This is not permission to open live databases
   during planning, tests, a live freeze, or a B–E capture operation.
3. Use SQLite online backup into a newly created unique temporary database in the
   target directory. Bound lock wait and total backup duration; SQLite may observe
   concurrent commits, but only a transactionally consistent completed snapshot is
   accepted. Never copy `database.db` bytes alone, use `immutable=1` on an active
   WAL database, force a source checkpoint, or infer safety from absent sidecars.
4. Close the backup, validate the completed disposable copy (`integrity_check=ok`
   plus schema/version/readability checks), then publish to an absent target with
   a verified same-volume no-overwrite primitive. For a tracked or pre-existing
   target, refuse and leave its bytes/index state intact; resolving that collision
   is explicit and cannot become `-Force`. Reject a newly appeared target at commit.
   Failure/interruption leaves no published partial seed and reports the retained
   scratch file; cleanup is confined to newly owned scratch and is never live DB
   cleanup. Do not change the source's journal mode or application startup behavior.
5. Automated fixtures are synthetic DB families in scratch: an active WAL with a
   committed row absent from the base file; concurrent multi-table atomic writes;
   busy/timeout; corruption; missing helper/source; validation failure; publish
   collision; interruption before publication. Verify coherent row invariants,
   correct schema and committed WAL content, unchanged existing target, and no
   fixture escape. Byte equality of an actively written source is not an oracle.

### A3. Lifecycle and drive-root reporting

1. Reconcile every report from `git worktree list --porcelain -z`, Git common/admin
   relationships, a no-follow scan of the explicitly approved development parent,
   and annotations in the main checkout's gitignored
   `docs/ai_workflow/WORKSTREAM_OWNERSHIP.local.md`. Parse NUL-delimited records,
   avoid path prefix/wildcard selection, and report missing paths, unregistered
   directories, reparse anomalies, detached worktrees and unresolved relationships.
2. Extend the canonical annotation schema with stable worktree identity, owner,
   task, branch, creation time, expected PR, teardown condition, next review date,
   disposition/rationale and activity observation time. Git remains authoritative
   for registration. Missing annotation is OWNERLESS/activity UNKNOWN; stale
   annotation is ORPHANED_ANNOTATION; a registry/filesystem mismatch is UNRESOLVED.
   No report silently converts an annotation into physical/registration truth.
3. Creation fails closed on a fresh projection with ownerless/anomalous rows or
   unacknowledged merged/closed/overdue rows until the owner records KEEP/close
   disposition or time-bounded deferral. Remote PR metadata is optional triage
   evidence with exact PR-head matching and a freshness timestamp. Unknown or
   unavailable metadata/activity stays visibly UNKNOWN; never infer closure.
4. After successful `git worktree add`, update the annotation under a short local
   exclusive lock using atomic replacement. Git and the annotation are not one
   transaction. If annotation or seed completion fails or the creator is interrupted,
   preserve the worktree and return incomplete creation; the next audit exposes
   missing annotation as OWNERLESS. Test concurrent creators without lost updates,
   blocked lock/partial write, and interruption after Git success. Never auto-remove.
5. Status/handover emits review rows for merged/closed/overdue/ownerless/orphaned
   state. Scan only owner-approved drive roots and compare direct child identities
   with a dated owner-approved baseline; a missing baseline fails closed, and
   unexpected children are reported, never deleted. Reports go to explicit scratch
   output or stdout and may not update annotations, Git, shared environments or DBs.
6. During the signed closeout interlude, normal completion, abandonment, KEEP or
   DEFERRED retains the worktree and all recovery roots. The ordinary verified
   teardown alternative in technical-design §5.3 is unavailable under AC7 until its
   separately approved later operation. Normal branch advancement/append-only
   reflog development continues; retirement, expiration and object cleanup do not.

### A4. Sequence and expected gates

1. Finish this council, record all review findings/dispositions and Plan v2, complete
   §1.3 checks, and stop for owner Gate 1. No implementation check is claimed by
   passing a planning-artifact inventory check.
2. After approval, revalidate implementation base, declare exact file ownership,
   coordinate each shared-path edit, and establish isolated scratch runtimes before
   any collection. Draft criteria-derived tests through automation-qa, then implement
   the three A units through senior-developer in the same isolated manager checkout.
3. Run the standalone guard harness first without `tests/conftest.py`. Run focused
   guard/config tests and new snapshot/lifecycle/preflight behavioral tests only in
   the standalone isolated lane before C. Capture test commands, host/profile
   matrix, failure probes and before/after protected-root evidence. Never execute
   the historical `npx` or `gh` incident payloads: serialize hook input and prove
   denial without launching the named children.
4. Apply technical-design §4.5 and QUALITY_GATE.md's union: targeted script stem/
   directory-token tests where they actually exercise the changed behavior;
   `/verify-suite` if coverage remains absent; manual workflow dry-run; code-reviewer
   plus normal diff-time `/unslop` or `/verify-and-polish`; repository-wide pyright
   baseline diff for the Python helper. Run inventory `--check`, regenerate only
   on proved drift with tracked/staged config visibility, then recheck. No browser,
   CSS or visual gate is invented for this infrastructure-only scope; any full-suite
   fallback runs its canonical gates in the isolated lane.
5. Obtain owner review of exact user-level guard/memory changes and lifecycle
   mechanism/baseline. The owner installs external/user-level changes, runs a fresh
   session scope check and one representative scratch interactive acceptance, and
   records effective registrations, active reporting and any unavailable host.
   No agent changes user settings or performs live cleanup as an installation test.
6. Merge through normal authorized workflow and record PREVENTION_COMPLETE only
   when every technical-design §5.4 item passes, including owner installation and
   lifecycle monitoring. Then use the already signed Q1–Q8 sequence: owner-approved
   fresh development universe/cutoff, normal completion or explicit disposition
   while retaining worktrees, owner-recorded AC8 stabilization, fresh read-only
   evidence, and separately approved operations.

**B–E contracts retained without new implementation design:** Technical-design
§§2–4 and 6–11 remain binding: no force/prune/ref retirement; exact immutable
digest-bound owner manifests; independent Windows filesystem review before live
copy/mutation; no-follow identity/containment checks; one shared exclusive B–E
coordination hold and persistent blocked-recovery state; durable per-mutation
journals; maintenance suspension and verified single-hold clean closeout;
complete private authenticated-encrypted/off-machine restore-tested preservation
and explicit protected-OID set equality; owner-only launchers and recovery;
immutable D campaign denominator, independently approved slices and exact outcomes;
retention with no automatic expiry. B is independently schedulable after rollout
prerequisites, C precedes D, and E requires PRESERVATION_COMPLETE and separate
planning/approval even if D remains incomplete. None of their launcher, recovery,
storage, key-custody or manifest choices is a prerequisite to this A council.

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `/root/product_manager` | Actual collaboration tool canonical ID supplied by manager; did not author historical Section 0 |
| `product-manager` — response matrix + Plan v2 | `/root/product_manager` | Same Plan v1 author resumed by manager with synthesized dispositions |
| `architecture-reviewer` | `/root/architecture_reviewer` | Independent read-only cold review of Plan v1 |
| `test-strategist` | `/root/test_strategist` | Independent read-only cold review of Plan v1 |
| `product-risk-reviewer` | `/root/product_risk_reviewer` | Independent read-only cold review of Plan v1 |

**Same product-manager resumed for the matrix + Plan v2?** yes — the manager
resumed `/root/product_manager` through `collaboration.followup_task` and supplied
the synthesis/IDs through messages. This is the same agent that wrote Plan v1.

**Evidence gap:** none. These are the actual canonical task IDs returned by the
collaboration tool and supplied by the manager, not invented UUIDs. The three
reviewers independently read the artifact. `/root` remained the read-only manager;
`/root/planning_support` performed delegated migration, pointer, isolated tooling
and generated-inventory support. Neither authored the council plan or substituted
for an independent reviewer. Historical Section 0 authorship is not attributed to
this council PM.

## Planning-lane evidence — initial entry

- Standalone owner-created destination confirmed by manager: repository root
  `D:\development\Hypertrophy-Toolbox-worktree-cleanup-plan`, with Git directory
  and common directory both that clone's `.git`, ordinary parent/`.git` paths.
  No alternates/http-alternates; recursive no-follow object walk found three files,
  each with exactly one clone-local hardlink path from `fsutil hardlink list`.
  Local-source origin is recorded but not used for collection or fetching.
- Delegated support copied both missing drafts exactly, reconciled only the intended
  five-line INDEX insertion, and coordinated the new MASTER_HANDOVER pointer with
  the read-only manager. Original PLANNING SHA-256:
  `9B821E4E8C804BE678818C9F0F8B712B5801B8B10B6E4074B82F19D0CA9815EA`.
  Source draft/INDEX/index preservation evidence is retained by support in the
  clone-local scratch lane; no source files were changed by this council.
- Scratch root is `artifacts/worktree-cleanup-planning/council-20260905` inside
  the clone with verified ordinary ancestors. Runtime/cache redirection,
  independent dependencies, tracked/staged visibility, collection and inventory
  checks remain pending at Plan v1 authoring. Do not run collection before complete
  isolation proof. This is not a claim that §1.3 checks already passed.

## Reviewer findings

The original independent reviews below are reproduced verbatim. Their citations
refer to Plan v1 and the then-current source. Plan v1 remains historical; accepted
findings are implemented in the planning text of Plan v2, not in application code.

### architecture-reviewer (agent `/root/architecture_reviewer`)

Independent architecture-reviewer review of Plan v1, read directly from the standalone clone. Review was read-only: no document writes, collection, tests, application imports, database operations, or remote actions were performed. The signed 2026-09-05 Gate 0 decision is accepted; its historical record and B–E boundaries are not reopened.

**AR1 — `docs/worktree_cleanup/PLANNING.md:504`, A2.1 and A4.2 — Source runtime overrides need an explicit target-session isolation contract.**  
Risk: A2 deliberately permits a verified source selected through `DB_FILE` or `HT_RUNTIME_DIR`, but does not specify what happens to those inherited variables in the newly created worktree’s launch environment. The existing launcher opens a terminal with a working directory alone (`scripts/new-worktree.ps1:162`). Merely changing directories and publishing an isolated seed cannot override `DB_FILE`’s documented precedence (`CLAUDE.md`, §3 “Env vars”; `utils/runtime_paths.py`, module precedence contract). A subsequent application launch can therefore select the source database or log tree despite successful seed creation.  
Fix: Specify target-bound process runtime values for the supported launch path and emitted launch instructions, verify that both the target database and log paths are isolated before declaring the worktree ready, and test inherited source-pointing `DB_FILE`/`HT_RUNTIME_DIR` without changing persistent user settings.

**AR2 — `docs/worktree_cleanup/PLANNING.md:558`, A3.4 — Seed failure can contradict the promised OWNERLESS recovery signal.**  
Risk: The plan says to publish the annotation after Git succeeds, then groups “annotation or seed completion” failure under recovery in which “the next audit exposes missing annotation as OWNERLESS.” If annotation publication succeeds before seed creation fails, that annotation is present. The next Git/filesystem/annotation projection can look complete even though worktree creation returned incomplete. Technical-design §5.3 explicitly relies on the projection exposing interrupted post-Git annotation failure; an additional seed stage must not introduce an invisible incomplete state.  
Fix: Define the creation order and readiness boundary explicitly—for example, complete seed validation/publication before the final atomic annotation, so failed or interrupted seeding leaves the registered worktree visibly OWNERLESS—and test interruption at each boundary, retaining the worktree without automatic removal.

**AR3 — `docs/worktree_cleanup/PLANNING.md:510`, A2.2 and the artifact table — Record the proposed DB/logging exception in the canonical instructions.**  
Risk: The proposed direct `sqlite3` use and infrastructure diagnostics conflict with the unconditional “All DB access via `DatabaseHandler`” and “All logging via `get_logger()`” rules at `CLAUDE.md:66` and `CLAUDE.md:68`; `.claude/rules/database.md`, “DatabaseHandler pattern,” repeats the DB requirement. The exception is technically justified by the measured implementation: importing `utils/database.py` initializes its application logger, `_configure_connection()` changes journal mode, and connection close performs a checkpoint (`utils/database.py:90`, `utils/database.py:93`, `utils/database.py:502`). Leaving the exception solely in this planning packet makes a future reviewer likely to “repair” the helper into the prohibited import and connection behavior.  
Fix: Make Gate 1’s proposed approval explicitly cover this named standalone snapshot helper and its caller-captured diagnostics, and include coordinated, narrowly scoped cross-references in the canonical DB/logging instructions while preserving the application-wide requirements and root file size cap.

No new blueprint, application table, JSON route, normalization boundary, calculation behavior, or `utils/__init__.py` re-export is proposed. Their registration and response-contract rules therefore do not require new implementation work in A. The shared-path artifact list and per-edit coordination requirement are explicit. B–E safety contracts remain binding and their later implementation choices need not be settled for this council.

**Needs revision**.

### test-strategist (agent `/root/test_strategist`)

Independent test-strategist review of Plan v1

Provenance: `/root/test_strategist`. I read Plan v1 directly in `D:\development\Hypertrophy-Toolbox-worktree-cleanup-plan`, the test-strategist charter, canonical quality gate, technical-design §§1.3/4.5/5, and relevant source/tests. This was a read-only cold review. I ran no tests, collection, application imports, database operations, or writes. Gate 0 remains signed; this review concerns Operation A only.

Required gates

Planning-artifact gate now:

- Manual council/document review and the isolated `scripts/generate_test_inventory.py --check` sequence required by technical-design §1.3.
- Before collection, prove independent object storage, scratch runtime/cache/bytecode paths, and tracked/staged visibility of the new configuration document.
- Regenerate only after a successful collection demonstrates actual drift, then recheck. Dependency or collection failure is not drift.
- These checks do not establish that Operation A’s behavior passes.

Future Operation A implementation gate:

- Standalone `tests/worktree_cleanup/guard-contract.ps1`, without pytest/conftest/application imports, on every installed PowerShell host.
- Pytest union: `tests/test_guard_destructive_command.py`, `tests/test_agent_workflow_contracts.py`, proposed `tests/test_worktree_environment_preflight.py`, `tests/test_worktree_snapshot.py`, and `tests/test_worktree_lifecycle.py`, with the integration coverage specified below.
- Manual workflow dry-run, code review, Python baseline-diff gate, inventory check and justified regeneration.
- If script coverage remains absent or merely textual, full `/verify-suite` is required. Its actual definition runs full pytest followed by Chromium E2E; it cannot be reported as a pytest-only fallback (`.claude/skills/verify-suite/SKILL.md:7`).
- No CSS/visual-specific gate follows from the proposed paths. If full-suite fallback runs, record any recurrence of the historical `e2e/program-backup.spec.ts:79` pollution flake and its isolated result (`QUALITY_GATE.md:221`); do not assume a present failure is covered by that history.

Existing coverage

- `.claude/hooks/guard-destructive-command.ps1`: `tests/test_guard_destructive_command.py` exercises outcomes, nested commands, malformed payloads, permission-mode behavior, BOM/ASCII encoding, and parsing under installed hosts (`:58`, `:305`, `:323`, `:350`, `:370`, `:386`). This is real guard coverage.
- `.claude` Markdown and workflow documents: `tests/test_agent_workflow_contracts.py` checks retired references/numbering, command allowlists, local-only exclusion, Git tracking, and the skill guard (`:139`, `:166`, `:184`, `:207`, `:268`). It does not currently prove destructive-hook installation in project settings and shell-agent registrations.
- `scripts/new-worktree.ps1`: no existing behavioral coverage found. The `new-worktree` hit at `tests/test_guard_destructive_command.py:283` is a serialized Bash command naming `new-worktree.sh`, whose contents remain opaque to the guard. It is not coverage of the PowerShell creator.
- Proposed preflight, snapshot, and audit scripts: no existing test hits for their stems, including hyphen/underscore spellings. They need the proposed behavioral test modules.
- `CLAUDE.md`, status/worktree commands, `PARALLEL_WORKFLOW.md`, `AUTONOMY.md`, and `WORKSTREAM_OWNERSHIP.md`: configuration contracts plus manual active-guidance review; current contracts do not detect every unsafe instruction.
- Planning document and MASTER_HANDOVER pointer: document review. The new technical-design document also changes the parametrized configuration surface.
- Generated `docs/test_inventory/`: generator output and `--check`, never manual editing.
- Owner-level guidance/installation: review exact deltas and retain owner-run installation/fresh-session evidence. Repository tests cannot establish installation outside the repository.

Findings

TS1 — Medium: Pin the actual test union and creator integration coverage.

Plan v1 A4.4 (`PLANNING.md:590`) states the correct derivation rule but does not record its present result. The source search finds no genuine coverage for the four infrastructure scripts. The guard’s `new-worktree.sh` string must not suppress the fallback (`QUALITY_GATE.md:111`).

Required disposition: Put the coverage mapping above into Plan v2. Explicitly assign `tests/test_worktree_lifecycle.py` to invoke the real `new-worktree.ps1` against disposable repositories, as well as exercising `audit-worktrees.ps1`; assign `tests/test_worktree_snapshot.py` to the helper and its creator integration; assign `tests/test_worktree_environment_preflight.py` to the preflight entry point.

Failure oracles: a blocked lifecycle/preflight must leave Git registration, refs, and filesystem children unchanged; successful creation must produce exactly one registered worktree and matching annotation; post-Git seed/annotation failure must return nonzero/incomplete, retain the registered worktree, and never print the current unconditional “Worktree ready” success (`scripts/new-worktree.ps1:148`). Re-derive the union from the final implementation diff. If these tests do not actually cover the scripts, run full `/verify-suite`.

TS2 — Medium: Make registration and inherited-state acceptance executable.

A1 specifies both profiles and Process/User/Machine scope (`PLANNING.md:478`), but the existing config suite tests the skill guard, not destructive-hook wiring. Existing outcome cases mostly use `main`; installed-host parametrization alone does not prove the required profile/permission matrix.

Required disposition: Extend `tests/test_agent_workflow_contracts.py` to enumerate actual shell-capable charters and project settings, assert destructive-hook registrations, and invoke their resolved hook commands with serialized deny/allow inputs. Extend the guard suite and standalone harness across installed host × `main`/`agent` × normal/`bypassPermissions` modes. Unknown permission semantics retain fail-closed tests. Missing hosts must be reported unavailable.

In `tests/test_worktree_environment_preflight.py`, use an injected environment-scope reader for User/Machine values; tests must not call persistent setters. Exercise both variable names independently in every scope, including `"0"`, nonempty values, an empty value where the platform distinguishes it from absence, and a scope-read error. Presence and unreadable state must fail closed. Absent variables with valid scratch identities must pass. A disposable child-process environment can test actual Process inheritance without changing user settings.

Failure oracles: every denied hook invocation returns exactly 2 before any child payload executes; ordinary native-path/blob-read controls remain allowed; removing or misrouting one required registration makes its contract fail. Preflight errors must prevent creator mutation. Automated wiring proof and owner fresh-session installation proof remain separate.

TS3 — Medium: Protect index state at the creator boundary, not only inside the snapshot helper.

Plan v1 A2.4 correctly promises unchanged target bytes/index state (`PLANNING.md:524`), but the current creator calls `git update-index --skip-worktree` before entering the seed switch (`scripts/new-worktree.ps1:108`). A safe helper could refuse a tracked target after the wrapper has already violated the promised index invariant.

Required disposition: Add explicit wrapper-level tests in `tests/test_worktree_snapshot.py` using a synthetic repository with tracked `data/database.db`, and require the `copy-current` collision decision before any skip-worktree/index mutation. Record target bytes and `git ls-files -v --stage` before invocation. On refusal, both must remain identical; no source or existing-target replacement occurs.

Also pin the proposed helper’s failure cases to explicit oracles: active-WAL committed rows are present; concurrent multi-table invariants remain coherent; bounded timeout terminates; corrupt/invalid copies never publish; an appearing destination retains its sentinel bytes; interruption leaves no final target and reports only owned retained scratch. The wrapper must propagate helper/validation failure as incomplete creation without automatic removal.

Conftest / fixture work

No blueprint, application table, or `tests/conftest.py` change is required. New tests use synthetic scratch SQLite families and disposable Git repositories. `tests/conftest.py:9` already imports `DatabaseHandler` during collection, so even focused pytest requires the fully isolated canonical lane. The standalone immediate guard harness must remain independent of it.

Verdict

Targeted implementation gates are sufficient only after the proposed genuine script/creator coverage is added and verified; otherwise full `/verify-suite` is required. Plan v1 needs the three planning clarifications above before a clean Gate 1 recommendation. They require no implementation during this planning turn and no reopening of Gate 0 or B–E design.

### product-risk-reviewer (agent `/root/product_risk_reviewer`)

Independent product-risk-reviewer review of Plan v1

Reviewer provenance: `/root/product_risk_reviewer`. Cold read of `docs/worktree_cleanup/PLANNING.md`, the final signed 2026-09-05 Gate 0 decision, technical-design §§2.2, 5, 11–12, `CLAUDE.md`, the database rule, current handover, and the existing worktree-creation script. Read-only review; no tests, collection, application imports, database access, or mutations performed.

**Findings: None requiring revision.**

- **Product behavior and scope:** Plan v1 explicitly declares calculation surface `none` and excludes schema, API, UI, calculation, application-backup, and startup changes. It preserves the seven application workflows and includes migration notes and tests for the changed developer-facing `copy-current` behavior. This respects `CLAUDE.md` §1’s refactor invariant and does not resume a parked product workstream.

- **Snapshot loss and privacy:** A2 replaces the existing raw database-file copy with a completed, validated SQLite-native snapshot; preserves existing targets; refuses unavailable sources or validation; and bounds lock waits and backup duration. Its synthetic test families and exclusion of application configuration/logging imports protect the planning/test lane from user data. A2.2 explicitly makes direct `sqlite3` access an owner-approved infrastructure exception at Gate 1, rather than silently bypassing the required application `DatabaseHandler` pattern. No remote user-data transfer or cloud service is introduced. The proposed seed remains distinct from the application’s program-backup and startup-backup contracts. References: Plan v1 A2.1–A2.5; technical-design §5.2; `CLAUDE.md` §§1–2; `.claude/rules/database.md`.

- **Lifecycle disruption and retention:** A3 makes blocked creation actionable through owner disposition, preserves incomplete creations, and retains ownerless or anomalous entries visibly. Audit output never grants deletion authority. A3.6 explicitly applies signed AC7 over ordinary teardown guidance, retaining worktrees and recovery roots during development closeout while permitting normal branch advancement. A1.5 preserves the packet’s snapshot-retention exception without extending it into a permanent ban on normal backup rotation. References: Plan v1 A1.5, A3.2–A3.6; signed Section 0 AC7 and approved Q2–Q3; technical-design §§5.2–5.3.

- **Approval scope:** Gate 0 remains signed and its historical questions remain historical. A4 preserves owner installation, verification, monitoring, closeout, and stabilization requirements before later cleanup eligibility. Gate 1 for A grants no B–E execution or source-cleanup authority. Later preservation, retention, and E dependencies remain binding without making B–E implementation choices prerequisites to A planning. References: Plan v1 A4.5–A4.6 and “B–E contracts retained”; final Gate 0 record; technical-design §§11–12.

**Plan respects product invariants.**

## Response matrix

The read-only manager proposed the dispositions below and resumed the same PM to
write them and Plan v2. All six requested revisions are accepted. The positive
product-risk assessment is recorded as PR0 so no reviewer output is omitted.
No finding is rejected or deferred; later B–E design remains an existing scope
boundary, not a deferred council finding requiring a local follow-up note.

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| AR1 — inherited source runtime can defeat target isolation | architecture-reviewer | accept | V2.2 and V2.3 bind launch child/instructions to target process `DB_FILE`/`HT_RUNTIME_DIR`, verify DB/log paths and test inherited source values |
| AR2 — annotation before seed can hide incomplete creation | architecture-reviewer | accept | V2.3 orders validated seed publication before final annotation/readiness; every earlier post-Git interruption remains OWNERLESS and retained |
| AR3 — SQLite/diagnostics exception missing from canonical guidance | architecture-reviewer | accept | V2 artifact list adds `.claude/rules/database.md`; V2.2 and Gate 1 name helper/diagnostics exception with coordinated root/canonical-rule cross-references and root size cap |
| TS1 — actual script test union and creator integration need pinning | test-strategist | accept | V2.4 maps five test modules to real script entry points and failure/success oracles; full pytest + Chromium fallback if genuine coverage absent |
| TS2 — registration/host/profile/permission/scope tests incomplete | test-strategist | accept | V2.1 and V2.4 require executable registration checks, host × profile × permission matrix, injected User/Machine readers and real child Process inheritance without persistent setters |
| TS3 — wrapper may change skip-worktree/index before refusing collision | test-strategist | accept | V2.2/V2.3 place collision checks before any index mutation; wrapper tests preserve target bytes and `git ls-files -v --stage` on refusal |
| PR0 — no revision; product invariants respected | product-risk-reviewer | accept | Retain no application change, snapshot/privacy separation, literal retention, and approval scope; no additional product feature or migration introduced |

## Plan v2

**Goal:** Prevent another path-conversion incident and uncontrolled worktree
accumulation; create worktrees with consistent SQLite seeds, explicit runtime
isolation and truthful readiness/lifecycle reporting while retaining existing work
and recovery roots.

**Scope:** Operation A only, technical-design §5. In scope are the bounded guard,
fresh-session environment preflight, SQLite-native `copy-current`, reconciled
read-only lifecycle/drive-root reports, creation integration, active guidance
correction, tests and owner installation evidence. This turn produces planning and
its isolated artifact checks only. No implementation, user-level mutation, source
cleanup, B–E launchers/copy/mutation, database preservation, quarantine, removal,
prune, history retirement or reconciliation is authorized by this document.

**Calculation surface:** `none`. Application DB schema, routes, JSON response
contracts, calculations, normalization, UI, all seven product workflows, program
backup, startup backups, and initialization remain unchanged. No blueprint,
application table, conftest registration or `utils/__init__.py` export is needed.
PR migration notes must explain developer-facing changes to `copy-current`,
blocked/incomplete creation and launch instructions; tests pin that behavior.

**Effort / ownership:** L, three implementation units plus integrated acceptance.
Read-only manager orchestrates; senior-developer owns infrastructure/config/docs
implementation, automation-qa owns tests, product-manager owns this council record.
Owner creates the isolated manager checkout, applies external/user-level changes,
and makes approval/installation decisions. All implementers stay in that one
isolated lane. Plan v1's measured source-versus-clone uncommitted guard difference
remains a reconciliation obligation, not permission to copy source implementation.

### V2 artifacts

All paths below are proposed future implementation artifacts; this planning turn
changes only the packet documents/pointers and generated inventory.

| Path | Planned change / owner |
|---|---|
| `.claude/hooks/guard-destructive-command.ps1` | senior-developer: fill measured denial gaps; preserve BOM/ASCII/exit-code and bounded-parser contract |
| `.claude/settings.json`; shell-capable `.claude/agents/senior-developer.md`, `.claude/agents/automation-qa.md` and any other actually discovered shell registration | senior-developer: enumerate and verify effective destructive-hook wiring under both profiles |
| `scripts/preflight-worktree-environment.ps1` | senior-developer: standalone scope/runtime/root preflight, injected read adapters for tests |
| `scripts/seed_worktree_snapshot.py` | senior-developer: named stdlib-only SQLite snapshot helper with explicit input/output and captured diagnostics |
| `scripts/new-worktree.ps1` | senior-developer: lifecycle preflight, early collision protection, seed-before-annotation sequencing, target-bound launch and truthful readiness |
| `scripts/audit-worktrees.ps1` | senior-developer: read-only reconciled projection and approved drive-root comparison |
| `CLAUDE.md`; `.claude/rules/database.md` | senior-developer: narrowly scoped named snapshot-helper DB/diagnostics exception and canonical cross-references; preserve application rules and root file under 200 lines |
| `.claude/commands/status.md`, `.claude/commands/worktree.md`; `docs/ai_workflow/PARALLEL_WORKFLOW.md`, `AUTONOMY.md`, `WORKSTREAM_OWNERSHIP.md` | senior-developer: safe instructions, target runtime contract, annotation schema, literal retention and role boundaries |
| Exact owner-enumerated active project/user memories, local handovers and retained-checkout guidance | Review exact proposed deltas; owner applies external/user-level changes; no blanket write grant or historical record erasure |
| `tests/worktree_cleanup/guard-contract.ps1` | automation-qa: standalone immediate guard harness, no conftest/application import |
| `tests/test_guard_destructive_command.py`, `tests/test_agent_workflow_contracts.py` | automation-qa: actual outcomes/encoding and resolved-registration host/profile/permission matrix |
| `tests/test_worktree_environment_preflight.py` | automation-qa: real preflight entrypoint, injected persistent-scope reads, child Process inheritance, target runtime contract |
| `tests/test_worktree_snapshot.py` | automation-qa: helper and real creator integration; snapshot, collision, index and interruption oracles |
| `tests/test_worktree_lifecycle.py` | automation-qa: real creator/audit entrypoints against disposable repositories; concurrency, anomalies and readiness |
| `docs/test_inventory/TEST_INVENTORY.json`, `TEST_INVENTORY.md` | Generator only, after proved drift; then `--check` |
| `docs/worktree_cleanup/PLANNING.md`; `docs/MASTER_HANDOVER.md` pointer | product-manager council record; delegated coordinated pointer and dated gate status |

Check known local claims before each edit. Root/folder CLAUDE, all `.claude` paths
and MASTER_HANDOVER are never-claimed shared paths: coordinate each exact edit
through the manager; do not claim them globally. The canonical exception belongs
to future Gate-1-approved A work, not this planning diff.

### V2.1 Bounded guard, environment preflight and active guidance

1. Enumerate actual project and shell-agent hook registrations and installed
   PowerShell 5.1/7 hosts. Test installed host × `main`/`agent` profile ×
   normal/`bypassPermissions` mode. Missing hosts are unavailable, not passing;
   unknown permission semantics must fail closed. Execute each resolved registered
   hook command with serialized deny/allow payloads, and prove deleting/misrouting
   one required registration fails its contract. Report actual tool interception
   separately from advisory-only transports; this Codex transport does not prove
   Claude hooks ran.
2. Deny observable setting/export of either suppression variable in direct/env/cmd/
   PowerShell/.NET/setx, chained, multiline and nested command-text forms. Every
   denied/internal-error hook invocation must exit exactly 2 before any payload
   child executes. Preserve UTF-8 BOM plus ASCII and safe ordinary commands,
   drive-qualified native paths and full-OID Git blob reads as allow controls.
3. Fresh-session preflight reads both variable names independently at Process,
   User and Machine scope. Presence (including `"0"`, nonempty or distinguishable
   empty values), unreadable scope, malformed path or unverified root fails closed.
   Tests inject User/Machine readers without persistent setters and test actual
   Process inheritance in disposable child environments. Absent variables plus
   verified scratch/runtime identities pass. Preflight denial occurs before creator
   mutation. Owner fresh-session installation evidence remains a separate gate.
4. The guard is bounded raw-text prevention, not a sandbox or complete native argv
   interceptor. It cannot inspect opaque scripts, arbitrary alias/function expansion,
   final executable identity/destinations or every child process. Any literal
   heuristic is tested and described with that limit. Historical incident commands
   are serialized test inputs only; never execute their `npx` or `gh` payloads.
5. Active guidance must prescribe PowerShell end to end, direct argument arrays and
   drive-qualified native output paths. Git revision/path reads resolve exactly one
   validated full blob OID with `ls-tree`, then pass it separately to `cat-file blob`.
   Remove active suppression, POSIX-native-output, branch `-D`, forced teardown and
   mutating-prune advice; preserve historical quotations as non-prescriptive evidence.
   Preserve every discovered backup/snapshot for this packet while leaving normal
   post-operation backup rotation policy intact.

### V2.2 SQLite snapshot and runtime isolation contract

1. Resolve and report distinct absolute source, target database, target runtime and
   logs identities, validating no reparse/alias escape or source=target. A documented
   source `DB_FILE`/`HT_RUNTIME_DIR` override requires explicit source verification;
   there is no fallback to a different live database. Missing source or unavailable
   backup/validation refuses `copy-current`. Inspect the prospective checkout tree
   for a tracked `data/database.db` before creation; refuse a predictable collision
   before mutation. Recheck the actual target after Git creation and immediately
   before publication. **Every copy-current collision decision precedes any
   skip-worktree/index mutation.** Existing target bytes/index flags are never
   changed to make the helper succeed.
2. Gate 1 explicitly proposes one named exception: `scripts/seed_worktree_snapshot.py`
   may use stdlib `sqlite3` directly and caller-captured diagnostics, avoiding
   application `DatabaseHandler`/`get_logger()` imports and their journal/log side
   effects. Add coordinated narrow cross-references in root CLAUDE and the canonical
   database rule, retaining application-wide DatabaseHandler/get_logger requirements
   and the root size cap. No other application DB/logging exception is introduced.
   This utility never creates an app, initializes application schema, checkpoints the
   source, or supplies an opening/copy primitive for B–E.
3. Open the verified source with read-only SQLite URI; use online backup into a
   unique newly created temporary database in the target directory, with bounded
   lock wait and total duration. Never copy base DB bytes alone, infer safety from
   missing WAL/SHM, use `immutable=1` on active WAL, or change source journal mode.
   Close the completed backup and validate only the disposable copy with integrity,
   schema/version and readability checks. Concurrent writes may affect which
   committed state is captured; the result must be transactionally coherent.
4. Publish only after validation using a verified same-volume no-overwrite primitive
   to a still-absent target. A new destination collision preserves its bytes. Failure
   or interruption never publishes a partial seed; report only newly owned retained
   scratch and keep its identity for diagnosis. Any scratch cleanup remains confined
   to those owned files. No source family or pre-existing target is cleaned up.
5. **Target-session boundary (AR1):** source-selection variables never become target
   launch configuration. The supported `-OpenTerminal` child and the exact emitted
   manual launch instructions explicitly set process-only `HT_RUNTIME_DIR` to the
   verified new worktree runtime root and process-only `DB_FILE` to its verified
   target database. Bind logs/backups/temp/cache/bytecode to that target's isolated
   runtime/scratch paths; verify effective database and log resolution before final
   annotation/readiness. Merely setting the working directory is insufficient.
   Reject a source-pointing or unresolved target launch configuration; do not change
   persistent User/Machine values or the parent source session. Tests inject inherited
   source-pointing variables and prove the supported child/instructions resolve the
   target DB and logs. Plain unrelated shell launches are outside this supported
   launch contract and must not be advertised as already isolated.
6. Planning/tests/pre-C verification use synthetic SQLite families only. No live
   source opening is an automated acceptance step and no collector runs during a
   live freeze. Tests prove active-WAL committed rows, coherent concurrent multi-table
   transactions, bounded timeout, invalid/corrupt-copy rejection, validation failure,
   helper absence, publish collision and interruption oracles. Actively written source
   byte equality is not a snapshot-validity oracle.

### V2.3 Lifecycle projection, creation ordering and retention

1. `audit-worktrees.ps1` reads Git `worktree list --porcelain -z`, reported common/admin
   relationships, an approved development-parent no-follow scan and the main checkout's
   gitignored WORKSTREAM_OWNERSHIP annotations. Parse NUL records and exact identities;
   never wildcard/prefix-select action targets or follow unapproved reparse entries.
   Report registered/missing/unregistered/detached/anomalous entries even without
   annotations. Git controls registration truth, not physical existence.
2. Schema fields are stable worktree identity, owner/task, branch, creation time,
   expected PR, teardown condition, next review date, disposition/rationale and
   timestamped activity observation. Missing annotations => OWNERLESS/activity UNKNOWN;
   stale annotations => ORPHANED_ANNOTATION; registry/filesystem mismatch => UNRESOLVED.
   Fresh merged/closed PR metadata and exact PR-head matching are triage evidence only;
   unavailable/stale metadata remains UNKNOWN and cannot imply closure or removal.
3. Creation reads a freshly reconciled projection and refuses ownerless/anomalous or
   unacknowledged merged/closed/overdue rows until owner KEEP/close disposition or a
   time-bounded deferral. A blocked preflight must leave registrations, refs and
   filesystem children unchanged. Annotation data cannot waive physical disagreement.
4. **Readiness order (AR2/TS3):** environment/lifecycle/identity and predictable target
   collision preflight → successful Git creation → actual target collision check before
   any index mutation → seed validation/publication (or explicit validated non-copy
   seed mode) → target launch DB/log/runtime verification → final annotation under a
   short exclusive local lock with atomic replacement → success/readiness. There is
   no transaction claiming to atomically commit Git and annotations. Never publish the
   final annotation before seed and runtime verification succeed.
5. Failure/interruption after Git but before final annotation retains the registered
   worktree, returns nonzero/incomplete and leaves it visibly OWNERLESS to the next
   projection; no automatic removal, prune, branch deletion or misleading “Worktree
   ready.” Test immediately before/after each seed/publication/annotation boundary,
   lock/read/write failure and concurrent creators without lost updates. Interruption
   after durable final annotation has a complete projection because prerequisite seed
   and runtime checks already passed; avoid falsely claiming failed seed readiness.
6. Audits are read-only: stdout or explicit scratch output, no annotation/Git/runtime/
   shared-environment mutations. Drive-root reporting compares approved direct-child
   identities against a dated owner-approved baseline; missing baseline or unresolved
   topology is explicit blocked/unknown state and unexpected children are only reported.
   Status/handover presents merged/closed/overdue/ownerless/orphaned review rows.
7. Signed AC7 controls the interlude: completed/abandoned/KEEP/DEFERRED developments
   retain worktrees and recovery roots. Technical-design §5.3's ordinary verified
   teardown alternative is unavailable until the separate approved operation. Normal
   branch advancement and appended reflogs are allowed; retirement, reflog expiration
   and object cleanup are not. No age, PR state or annotation authorizes deletion.

### V2.4 Acceptance tests and implementation gates

The present coverage derivation is explicit: the existing guard suite is real
coverage; workflow contracts currently cover metadata/skill rules, not effective
destructive-hook wiring. No existing behavioral coverage was found for the creator
or the proposed preflight/snapshot/audit scripts. The serialized `new-worktree.sh`
string is not creator coverage. Required new tests therefore close those gaps:

| Gate / path | Required behavior and oracle |
|---|---|
| `tests/worktree_cleanup/guard-contract.ps1` | Standalone, no conftest/app imports; installed host × profile × permission deny/allow matrix; exit 2 before payload child launch; BOM/ASCII preserved |
| `tests/test_guard_destructive_command.py` | Same effective host/profile/permission outcomes, malformed/unknown modes and every observable variable-setting form; safe native/blob controls |
| `tests/test_agent_workflow_contracts.py` | Enumerate actual shell charters/settings, resolve and execute each registered hook with inert payloads; missing/misrouted registration fails; canonical exception remains precisely scoped |
| `tests/test_worktree_environment_preflight.py` | Real preflight entrypoint; both variables in every scope with `"0"`, nonempty, distinguishable empty and read-error cases; injected User/Machine reads only; child Process inheritance; inherited source runtime overridden by supported target launch; no mutation on refusal |
| `tests/test_worktree_snapshot.py` | Real helper plus real creator wrapper; active WAL rows and concurrent relational invariants; deadline termination; invalid copy/validation/publish/interruption failures; no final partial target; source/target distinct; appearing destination sentinel unchanged |
| `tests/test_worktree_snapshot.py` tracked-target integration | Synthetic tracked `data/database.db`; record bytes and `git ls-files -v --stage` before invocation; collision rejection before skip-worktree/index mutation; bytes/flags unchanged; propagate helper error as incomplete without auto-removal |
| `tests/test_worktree_lifecycle.py` | Real `new-worktree.ps1` and `audit-worktrees.ps1` against disposable repos; preflight leaves registry/refs/children unchanged; success exactly one new registration and final annotation; post-Git failures retained OWNERLESS/incomplete with no readiness text; concurrent annotation/interruption/no-follow/unknown-baseline and read-only report oracles |

Run the union of these five pytest modules after the standalone harness, with
all collection in the verified standalone/scratch lane (conftest imports application
DB modules even for focused collection). Re-derive paths from the final diff with
script stem/directory-token searches; a textual mention is not behavioral coverage.
If any changed script remains genuinely uncovered, run full `/verify-suite`:
**full pytest plus Chromium E2E**, not pytest alone. No CSS/visual-specific gate is
required by these paths. If the fallback exposes the historical program-backup
pollution flake, record and investigate its actual isolated result; history is not
a waiver. No conftest, blueprint or application table changes are planned.

Also required: manual workflow/guidance dry-run, code-reviewer and the normal
`/unslop` or `/verify-and-polish` diff-time review, repository-wide pyright baseline
diff for any Python implementation, and inventory `--check` with tracked/staged
config visibility; only proved drift permits regeneration and a second check.
Test commands/results identify host, profile and isolation. No implementation
gate is considered passed by the planning inventory evidence below.

### V2.5 Delivery sequence, Gate A and retained B–E boundaries

1. Present this Plan v2, exact diff and §1.3 evidence. Stop for explicit owner Gate 1
   for A, including the named helper/diagnostics exception and lifecycle architecture.
2. After approval, revalidate the implementation base and reconcile any already landed
   guard changes under normal review. Coordinate exact paths, establish scratch
   isolation, author criteria-derived tests, then implement guard/guidance, snapshot
   and lifecycle units. Do not import uncommitted source code by inference.
3. Complete V2.4's actual script tests, manual/review/type/inventory gates and one
   owner-run interactive disposable Windows acceptance. Keep all live protected roots
   unchanged by automated verification and retain private evidence.
4. Prepare exact user-level guard/memory deltas and configured lifecycle/baseline
   choices for owner review/application. Agents do not install them. The owner
   verifies effective installations and fresh Process/User/Machine scope, installed
   hosts/profiles, active guidance scan and actual lifecycle reporting. Tests of
   repository code cannot attest external installation.
5. Merge through the normal authorized workflow. Declare PREVENTION_COMPLETE only
   after every technical-design §5.4 item is verified: exact installed host/profile
   controls; fail-closed encoding/exit semantics; fresh absence of suppression state;
   safe guidance/allow controls; read-only scratch lifecycle; WAL/concurrent/failure
   snapshots; concurrent/interrupted creator projection; implementation and inventory
   gates; merge; owner installation; active lifecycle monitoring. Merge alone is not
   completion and starts no development-closeout phase.
6. Then follow the signed Q1–Q8 sequence without re-decision: fresh owner-approved
   open-development universe/cutoff (including later entrants), normal completion or
   explicit justified owner disposition while retaining worktrees/recovery roots,
   owner-recorded AC8 stabilization checklist without a fixed quiet period, fresh
   read-only evidence, and separately approved cleanup operations.

Technical-design §§2–4 and 6–11 remain unchanged and binding for B–E: exact identities,
no-follow containment, independent Windows filesystem review, immutable digest-bound
owner manifests, one exclusive shared coordination hold and persistent recovery
blocks, per-mutation durable journals, maintenance control and single-hold verified
clean closeout, complete private authenticated-encrypted off-machine restore-tested
preservation and protected-OID set equality, owner-only live execution/recovery,
immutable D target denominator and exact slice/campaign outcomes, and retention
without automatic expiry. B remains independently schedulable only after rollout
prerequisites; C precedes D; E needs PRESERVATION_COMPLETE plus separate plan and
approval even if D is incomplete. Their storage, key custody, launchers, manifests
and operation-specific recovery choices remain at later gates, not prerequisites
to A and not council findings deferred by this plan. No B–E action runs now.

## Planning-lane evidence — completed §1.3 checks

These are dated observations of this isolated planning lane, not current cleanup
inventory or Operation A implementation-test results. Detailed evidence stays in
the gitignored private directory
`artifacts/worktree-cleanup-planning/council-20260905/`; the relative links below
are local review aids, not promised public/committed artifacts. Source database and
log hashes are deliberately not copied into this planning document.

| Requirement | Observed proof / result |
|---|---|
| Owner-created standalone clone | `D:\development\Hypertrophy-Toolbox-worktree-cleanup-plan`; `.git` equals common directory; HEAD `85e23725bc2871c5f005162f29be231a2f106b85`; ordinary non-reparse clone ancestry. Source-pointing origin remained unused. |
| Independent Git object storage before collection | Initial no-follow proof checked all three object files, each `fsutil hardlink list` containing exactly one clone path; no alternates/http-alternates/reparse object members. After staging, a second proof checked all nine then-present files with the same result: [Git storage proof](../../artifacts/worktree-cleanup-planning/council-20260905/git-storage-proof.json). The different totals are evidence epochs, not omitted initial members. |
| Scratch runtime before collection | [Runtime proof](../../artifacts/worktree-cleanup-planning/council-20260905/runtime-isolation-proof.json) records the clone-local interpreter and `utils/config.py`; effective DB, DATA_DIR, LOGS_DIR and Python tempfile paths all resolve inside the verified scratch root; the scratch planning DB was absent at proof time. No path resolves to the live DB or logs. |
| Complete cache/temp/bytecode isolation | Scratch `isolated-env.ps1` sets TEMP/TMP/TMPDIR, HT_RUNTIME_DIR, DB_FILE, npm/pip/XDG, pytest, Hypothesis and Playwright caches; bytecode is disabled and its prefix is scratch. [Node cache proof](../../artifacts/worktree-cleanup-planning/council-20260905/node-cache-isolation-proof.json) uses actual Node realpaths to prove private `.vite`/`.vite-temp` junctions resolve only to scratch cache targets. These intentional cache junctions are distinct from prohibited object/runtime redirection to live roots. |
| Independent dependencies | Fresh clone-local ordinary `.venv` and `node_modules`; dependency installation exits 0. Actual Python 3.14.6, Node 24.19.0 and npm 11.17.0. No shared source dependency tree was reused or mutated. |
| Migration / shared-path coordination | Support copied missing PLANNING and technical design byte-for-byte; inserted only the intended source INDEX delta after base comparison; preserved source drafts, source INDEX bytes and source Git index. Manager acknowledged support's exact MASTER_HANDOVER insertion per shared-path rules before its edit; historical text remains. |
| Git visibility before first collection | [Staged visibility](../../artifacts/worktree-cleanup-planning/council-20260905/staged-visibility.txt) shows four packet documents staged before the initial inventory run. [Surface proof](../../artifacts/worktree-cleanup-planning/council-20260905/surface-tracked-proof.json) shows all 36 configuration Markdown surface files Git-visible, with no untracked/ignored contamination. |
| Proved drift before regeneration | Initial `scripts/generate_test_inventory.py --check` exited 1 with actual successful-collection drift only: workflow-contract nodes 83 → 84 and deterministic pytest total 2913 → 2914, caused by the new technical-design document. [Initial check](../../artifacts/worktree-cleanup-planning/council-20260905/inventory-check-initial.log). No dependency/collection failure was misclassified as drift. |
| Generator and final check | Regenerator exited 0 and wrote both inventory artifacts: [generation log](../../artifacts/worktree-cleanup-planning/council-20260905/inventory-regenerate.log). Subsequent `--check` exited 0: “Test inventory is up to date.” [Final check](../../artifacts/worktree-cleanup-planning/council-20260905/inventory-check-final.log). Both generated files were staged; six packet files total. |
| Diff and source protection | Default `git diff --cached --check` passed at Plan v1/inventory staging. After verbatim reviews were inserted, default whitespace checking reports exactly six intentional Markdown two-space hard breaks in the architecture review; these are retained to honor the verbatim requirement and reviewed as formatting, not content defects. A separately labelled per-command `core.whitespace=-blank-at-eol` check may check remaining whitespace without changing configuration; it does not erase the six default flags. Private source-after-validation evidence confirms all 15 baseline hashes unchanged, including draft/INDEX bytes, source Git index and 11 source DB/log-family files. Source DB-family/direct-log member sets also match, with no new sidecars/log files. No source SQLite connection was opened to obtain those byte/member checks. |
| History preservation | Manager verified the original source requirements artifact is the exact 24,381-byte prefix of the expanded PLANNING. Plan v1 remains unchanged after reviewer cold reads; the earlier pending evidence block is kept as a dated record, superseded by this completed entry. |

The inventory command performed collection in the isolated clone; no implementation
tests, server, application launch or browser session ran. Subsequent edits are
planning prose/pointer updates and do not alter the collected surface, so final
support restaging and byte/diff verification do not require redundant collection.
Source preservation and final staging are rechecked at handoff. No A behavior,
installation, PREVENTION_COMPLETE outcome or B–E action is claimed by these results.

## Sign-off — GATE 1, Operation A only

- [x] Gate 0 complete: final owner decision dated 2026-09-05, unchanged.
- [x] Every council finding has a recorded disposition: AR1–AR3, TS1–TS3 accepted;
      PR0 accepted with no added product scope. None rejected/deferred.
- [x] Agent provenance complete, including same-PM continuity and evidence-gap `none`.
- [x] Isolated §1.3 planning-artifact checks complete with evidence.
- [x] Owner approves Plan v2 for Operation A, including the scoped infrastructure
      SQLite/logging exception and lifecycle mechanism.
- [x] Ready to implement A through its required implementation gates.

User-level installation requires the owner's exact subsequent approval/application;
PREVENTION_COMPLETE remains blocked until it is verified. All B–E decisions stay
at their later operation gates. This planning turn stops for Gate 1.

## 2026-09-05 — Explicit Gate 1 sign-off and Operation A implementation authorization

**Owner approval (verbatim):**

> I approve Plan v2 in docs/worktree\_cleanup/PLANNING.md for Operation A only,
> including all recorded council dispositions, the named
> scripts/seed\_worktree\_snapshot.py exception permitting direct stdlib sqlite3
> and caller-captured diagnostics, and the lifecycle mechanism.

This explicit approval signs Gate 1 for Operation A and supports the two checked
approval/readiness boxes above. It supersedes only earlier pending Gate 1 and
planning-turn stop statements; the signed requirements, council findings,
dispositions, Plan v1, Plan v2 and historical evidence remain unchanged. Readiness
means implementation may begin through V2.4/V2.5, not that any implementation or
installation gate has passed.

**Authorized lane and routing:** The owner directs implementation in
`D:\development\Hypertrophy-Toolbox-worktree-cleanup-plan`. The manager remains
read-only; senior-developer owns implementation, automation-qa owns tests and
product-manager owns this planning record. On 2026-09-05 the manager released
scoped edits after senior-developer reported fresh implementation-base,
ownership-coordination and scratch-isolation preflight PASS, with private
`operation-a-preflight-proof.json` evidence. No collection or implementation result
is inferred from that release. Existing guard changes must be reconciled without
importing uncommitted source implementation by inference.

**Implementation-record provenance:** Manager `/root` assigned this entry to new
product-manager `/root/product_manager`; implementation and test roles are
`/root/senior_developer` and `/root/automation_qa`. These are this implementation
turn's identities, not replacements for the recorded council agents. Prior council
continuity and evidence remain intact. This host exposes no native filesystem Read
tool; after initial shell-backed reads exposed the role restriction, further
reading used senior-developer's verbatim file-content relay under manager direction.
The signed Gate 0 outcome, current Plan v2 and final Gate 1 checklist were read for
this scoped continuation; no new council review or continuity claim is made.

**Remaining obligations and authority boundary:** Complete all approved A units
and their behavioral, manual, review, type-check and inventory gates, then present
the exact final diff and validation results with the proposed user-level
guard/memory deltas, lifecycle/baseline choices and owner-run disposable Windows
acceptance instructions. The owner has not authorized agent application of
user-level changes, Operations B–E, source-checkout cleanup or a push to the
source-pointing origin. Preserve source drafts, live runtime data, all existing
worktrees and recovery roots. Publication or merge remains after the requested
review handoff.

`PREVENTION_COMPLETE` is **not recorded**: merge, owner installation, owner-run
interactive acceptance and active lifecycle monitoring still require actual
verification in addition to every technical-design §5.4 Gate A requirement. This
signature starts no open-development closeout or cleanup phase.

## Operation A implementation verification and owner review handoff

This continuation records repository work authorized by the explicit Gate 1
signature above. The signed requirements, original council evidence, dispositions
and Plan v2 remain unchanged. Repository verification does not attest owner
installation, publication, merge or active lifecycle monitoring.

### Implemented scope and review provenance

Senior-developer implemented all three approved A units: bounded suppression guards
and workflow guidance; read-only environment preflight and validated SQLite online
snapshot seeding; and reconciled lifecycle/baseline reporting with fail-closed
creation, retained incomplete worktrees, target launch verification and final atomic
annotation. The named stdlib SQLite/caller-captured diagnostics exception remains
limited to `scripts/seed_worktree_snapshot.py`. Application behavior, schema,
calculations, response contracts and backup rotation were not changed.

The manager `/root` remained read-only. `/root/senior_developer` authored
implementation and `/root/automation_qa` authored and ran tests. Initial independent
code/manual review was performed by `/root/manual_qa_reviewer`. The tool's four-thread
limit prevented that review worker's resumption, so the manager separately assigned
fix-verification code review and then the required unslop review to
`/root/product_manager`. This worker authored neither implementation nor tests;
the sequential review roles reused one worker and are not represented as distinct
independent agents. Those review tasks are complete; the worker has now resumed
the product-manager role solely for this planning-record append. Prior council
agent provenance and continuity evidence are unchanged.

All five original code findings were corrected and rechecked: inherited Git
redirection, Python startup/import redirection, observable suppression setters,
reciprocal worktree/admin identity and invalid annotation/date/branch waivers.
Seven grouped residual findings also closed through code review and behavioral
verification: inherited Git trace output; compound/arithmetic suppression setters;
dangling reparse inspection; metadata validation before Git invocation; strict
timezone-bearing creator review dates; annotation-lock reparse rejection; and
mandatory real target configuration verification. The missing-config regression
first failed on both installed hosts, proving the former readiness bypass, before
the bounded fix was applied.

The three manual-document findings closed with an exact fixture audit and expected
`UNEXPECTED`/exit-1 oracle, a fresh-fixture manual alternative when Windows Terminal
is unavailable, and self-contained fresh installed-session checks. Unslop review
identified two unused test-scaffolding fragments (an emitted `$argv` assignment and
unused proxy context-manager methods); automation-qa removed both. Final code,
manual-text and unslop review report no open findings.

### Actual validation sequence

All collection and behavioral verification remained in the verified standalone
checkout with its private dependencies and scratch runtime/temp/cache/bytecode
isolation. SQLite fixtures and disposable Git repositories were synthetic. The
earlier 602-test checkpoint predates review corrections and is superseded by the
results below; the planning-lane inventory results are not implementation evidence.
Exact commands, isolation details and retained test-log references are recorded in
the [final QA receipt](../../artifacts/worktree-cleanup-planning/council-20260905/operation-a-qa-closeout.json).

| Gate | Observed result and limit |
|---|---|
| Standalone guard harness | **168 passed** across Windows PowerShell **5.1.26100.9278** and PowerShell **7.6.5**, both `main`/`agent` profiles and `default`/`bypassPermissions` modes. Payloads were serialized hook inputs; no incident payload children ran. This proves direct hook behavior, not actual Claude interception or owner installation. |
| Required five-module union after review corrections | **686 passed, zero failures/skips, 672.55 seconds**: `test_guard_destructive_command.py`, `test_agent_workflow_contracts.py`, `test_worktree_environment_preflight.py`, `test_worktree_snapshot.py` and `test_worktree_lifecycle.py`. This full union preceded the final missing-config correction and two dead-scaffolding removals. |
| Final affected modules after those last changes | Complete lifecycle (**140**) and snapshot (**33**) modules: **173 passed, zero failures/skips, 360.81 seconds**, including both new missing-config cases and the changed test scaffolding. The current five-module union collects **688 nodes**; **688 was not executed as one final full run**. The 173 result overlaps the earlier union and is not added to 686 as a distinct-test total. |
| Native annotation-lock reparse coverage | Both actual creator hosts passed using the existing Windows native file-symlink capability. An earlier PowerShell 5.1 fixture-cmdlet setup skip was corrected by changing synthetic fixture creation; the final affected run has zero skips. No settings or privileges were changed. |
| Manual synthetic workflow/guidance dry-run | PASS for copy-current, actual target configuration probe, final annotation and read-only audit. The fixture's old baseline intentionally reports the new retained child `UNEXPECTED` with exit **1**; this is the expected baseline-drift oracle, not failed creation or permission to delete/update the baseline. Interactive owner acceptance remains separate. |
| Repository-wide Python type-check baseline diff | Pyright **1.1.410**, **246 files**, **zero diagnostics**; baseline zero, current zero, net-new zero. |
| Inventory gate | Successful collection proved deterministic inventory drift **3076 → 3162** (**86** added regression nodes), with the final inventory covering **129 files**. Regeneration then final `--check` passed, and both generated inventory artifacts were staged. Final receipt: [inventory closeout check](../../artifacts/worktree-cleanup-planning/council-20260905/operation-a-inventory-closeout-final.log). |
| Final preservation after the implementation evidence append | **PASS**, [final preservation receipt](../../artifacts/worktree-cleanup-planning/council-20260905/operation-a-final-preservation.json): all **15** initial protected-source hashes unchanged (including index, drafts and runtime files); exact **11** database-family/direct-log members preserved; the original **93,940-byte** planning prefix preserved apart from the two authorized Gate 1 checkbox substitutions; technical design byte-identical to its source draft; all **90** observed registered source roots ordinary and present. The registry proof establishes the initial observed count and final presence, not a byte-identical initial registry snapshot. No source SQLite connection or source mutation was used for this verification. |
| Final exact diff capture | **Available**: [staged diff](../../artifacts/worktree-cleanup-planning/council-20260905/operation-a-final.diff) and [capture receipt](../../artifacts/worktree-cleanup-planning/council-20260905/operation-a-final-diff-receipt.json), covering **27 files**. Senior-developer will refresh these same artifacts after staging this final record update; no digest is embedded here. Default `git diff --check` reports exactly six preserved original council Markdown hard breaks; all other checked whitespace classes pass. |

The script-path coverage derivation maps the changed guard, creator, preflight,
snapshot and audit entrypoints to these behavioral gates. No changed script was
left with only a textual mention as coverage, so the approved uncovered-script
full-pytest/Chromium fallback was not triggered. No application/conftest/blueprint
change or CSS/visual-specific gate was introduced.

### Concrete owner handoff and remaining gates

The reviewable owner procedure is
[OPERATION_A_OWNER_ACCEPTANCE.md](OPERATION_A_OWNER_ACCEPTANCE.md), including
developer-facing migration behavior, disposable Windows acceptance commands,
fresh-session scope and installed-hook checks, and proposed lifecycle/baseline
choices. Its exact private installation proposals are retained at
`artifacts/worktree-cleanup-planning/council-20260905/operation-a-owner-deltas.private.json`.
The regenerated private scan records **275 proposals**, **90 registered roots** and
**270 guidance entries**, with **zero unresolved scan entries**. These are dated
proposal-scan observations, not a cleanup candidate inventory or permission to
change retained checkouts. All proposals remain unapplied; the owner must review
their exact current-byte prerequisites and declare any additional active guidance
before the installation gate can be verified.

The coordinated MASTER_HANDOVER current-state supersession is staged and preserves
the historical Gate 1-pending planning entry. The owner handoff must include the
final exact diff captured after this record update and the linked final preservation
receipt.

- [x] Explicit Gate 1 approval recorded for Operation A and its named exception.
- [x] Approved A repository implementation, behavioral/type/inventory gates and
      code/manual-text/unslop reviews completed as recorded above.
- [x] Final post-append protected-source and historical-record preservation verified.
- [x] Exact-diff handoff artifact available; final delivered capture refreshed after this record update.
- [ ] Owner reviews the final diff and authorizes the subsequent publication/merge
      workflow; merge is actually verified.
- [ ] Owner applies approved exact guard/settings/memory/guidance deltas and verifies
      fresh Process/User/Machine scope, effective registrations, installed hosts,
      profiles, encoding/exit semantics and actual hook interception.
- [ ] Owner runs and records the disposable interactive Windows acceptance.
- [ ] Owner approves and installs the actual lifecycle annotations/baseline and
      monitoring mechanism, then verifies fresh reports and active monitoring.
- [ ] Every technical-design §5.4 Gate A requirement is actually verified before
      `PREVENTION_COMPLETE` is declared.

`PREVENTION_COMPLETE` remains **not declared**. No user-level changes, Operations
B–E, source-checkout cleanup or push to the source-pointing origin were performed.
Existing worktrees, source drafts, live runtime data and recovery roots remain
protected. Owner review/installation/acceptance and active monitoring cannot be
substituted by repository tests or merge, and no development-closeout or cleanup
phase begins from this implementation handoff alone.

## 2026-09-05 — Terminal acceptance failure and bounded correction

The owner-run fixture `owner-acceptance-6295ddaa87dc48e2a65229836894346b`
completed snapshot/runtime validation, one new target registration with final
`ANNOTATED` status, unchanged source-console settings, and the expected audit
exit **1** for the retained child absent from the old baseline. Its saved
`source-and-audit-result.json` still records the interactive observation as
`PENDING`: Windows Terminal reported **0x80070002** while launching the spaced
PowerShell executable path (`C:\Program "Files...`). Creation/audit success is
therefore not interactive acceptance. All fixture roots remain retained.

Within the existing Gate 1 authorization, `scripts/new-worktree.ps1` now invokes
Windows Terminal directly with separate, unquoted path operands and checks its
dispatch exit code. The encoded target setup is unchanged. The earlier helper
failure on inherited `GIT_ASKPASS` was addressed in the owner acceptance wrapper
with process-only Git environment preservation/restoration; the application
guard was not relaxed. This continuation changes no calculation, schema or API
contract and does not reopen the completed council or approval gates.

The strengthened test checks the entire argument vector and host identity, then
executes the captured target setup. Its PowerShell adapter forwards operands to a
trusted Python receiver; this extra boundary does **not** test Windows Terminal
app-alias activation or its visible tab. A preliminary ordinary native receiver
also accepted the original arguments, so there is no automated reproduction of
the owner's app-alias failure. Application Control subsequently blocked a
generated receiver; the final test uses no compiler or Application Control change.

Final affected verification: lifecycle **140 passed in 344.20 seconds** and
snapshot **33 passed in 30.27 seconds**, with zero failures/skips. The two focused
host cases overlap these **173** cases and are not an additional total. Logs are
`terminal-lifecycle-final-20260906.log` and
`terminal-snapshot-final-20260906.log` under the existing `council-20260905`
artifact directory; their filename suffix does not change this record's date.
Pyright **1.1.410** checked **246 files** with zero diagnostics/net-new findings.
Inventory `--check` passed without regeneration. Code and unslop reviews are clean.

Provenance: the manager reused `/root/terminal_review` sequentially for code
review, unslop review, then this product-manager append; these are not independent
review agents or resumed council-PM continuity. `/root/terminal_dev` owned the
correction and type/inventory gates; `/root/terminal_qa` owned test changes and
behavioral runs. Native read tools were unavailable, so the manager expressly
authorized bounded read-only shell commands; this PM wrote only this append.

The original 27-file final diff/receipt remains historical and is not evidence
for the changed bytes. Original digest-pinned publication commands are **STALE**.
The developer's refreshed
[correction receipt](../../artifacts/worktree-cleanup-planning/council-20260905/terminal-fix-validation-receipt.json)
records the new diff and validation evidence after this append is staged.
Remaining gates are the owner's actual terminal retry, upstream reconciliation
and authorized publication/merge, external installation/interception, and
lifecycle baseline/monitoring verification. No Gate 2 approval or
`PREVENTION_COMPLETE` is recorded; no external installation, B–E execution or
cleanup is authorized by this correction.

## 2026-09-05 — Owner diagnostic and second terminal correction

The direct-invocation repair above did **not** fix the owner's retry: fixture
`owner-acceptance-5d71714e28394b229159dcecbf593cea` encountered the same Windows
Terminal **0x80070002** launch failure. Its successful creation/audit does not
supersede the missing terminal observation.

The subsequent owner-run diagnostic
`terminal-diagnostic-12ee20db36a04673a073f69fbf44c791` produced
`owner-host-bootstrap.json` with **ok=true**: the exact PowerShell **7.6.5** caller
ran with the expected target directory, DB/runtime, TEMP/TMP, npm cache and
bytecode setting. The separate `system-control.json` failed at unavailable
`Get-FileHash` before setup; it is not a successful isolation check. This is
evidence for the bootstrap route, not acceptance of the corrected creator.

The second production correction sends only a verified absolute, whitespace-free
system PowerShell executable and encoded operands through Windows Terminal.
The encoded bootstrap invokes the exact caller host with the encoded target
setup; no raw target `-d` or spaced caller path crosses that boundary. Bootstrap
prerequisites and command length are checked before Git creation. Review caught
an outer `-NoExit` shell retaining inherited source settings after the caller
exited; that flag was removed. Normal caller exit closes the bootstrap; failure
prints an error and pauses for Enter before exit **1**, without a usable fallback
prompt. The bootstrap uses no module cmdlets, module-path changes or production
execution-policy override. Source settings and the existing retention rules are
unchanged.

Final fresh verification: **146 lifecycle tests passed in 361.27 seconds**, zero
failures/skips, in `terminal-bootstrap-lifecycle-final.log` under
`artifacts/worktree-cleanup-planning/council-20260905`. Coverage includes both
caller hosts, spaces/apostrophes, actual nested encoded startup and target values,
unchanged source settings, normal/nonzero caller termination, pre-Git bootstrap
refusal and retained dispatch failure. Focused cases overlap the full run.
The receiver still substitutes for Windows Terminal; actual creator UI
acceptance remains pending. Prior unaffected snapshot **33-pass** and Pyright
**246-file/zero-diagnostic** results were reused, not rerun or reported as fresh.
Successful inventory collection proved **3162 → 3168** nodes; regeneration and
the subsequent `--check` passed, with **129 files** unchanged in count.

Code/manual/unslop review is clean after the outer-shell correction. The manager
resumed the same `/root/terminal_review` sequentially for those reviews and this
PM append; `/root/terminal_dev` and `/root/terminal_qa` retained their correction
and QA roles. No new council or independent-reviewer continuity is claimed.
This append preserves the earlier record and signed approval boxes.

The first terminal-fix receipt/diff is now historical. The new
[bootstrap correction receipt](../../artifacts/worktree-cleanup-planning/council-20260905/bootstrap-fix-validation-receipt.json)
records the final staged capture after this append. Digest-pinned publication
commands remain stale. A fresh owner-run creator and same-run actual host/target
observation are next; upstream reconciliation/publication, installation and
interception, and lifecycle monitoring gates remain open. No approval,
`PREVENTION_COMPLETE`, external installation, B–E operation or cleanup is implied.

## 2026-09-05 — Verified interactive acceptance and local integration continuation

**Current status:** Disposable interactive Windows acceptance **PASSED**. This
entry supersedes earlier pending acceptance statements and the earlier handoff
checklist. The original requirements, council, implementation and correction
record above remains the exact **114,799-byte** reviewed prefix, SHA-256
`804A85184BA0F1DF92305F6AC3E2F4AC9D0CBFB12A45C0432FAFD3A82A4E7930`.
Its test results retain their dated scope; none becomes fresh validation of
upstream-integrated or subsequently changed code.

The owner authorized local preservation commits and a separate integration branch
to reconcile Operation A with freshly verified upstream main from
`AvihaiShai/Hypertrophy-Toolbox-v3`, resolve conflicts, run justified checks and
prepare the final diff and Gate 2 review packet. This is normal development
integration of A, not the separately planned Operation E. Push, merge, external
installation, Operations B–E and cleanup remain prohibited in this continuation.
Local integration commits do not satisfy the publication/merge gate or authorize
worktree retirement, development closeout or `PREVENTION_COMPLETE`.

### Acceptance evidence and limits

The [saved interactive review](../../artifacts/worktree-cleanup-planning/council-20260905/owner-acceptance-570dae1e9a1a4d9c8260936c7a937057/interactive-acceptance-review.json)
records `PASS` at **2026-09-05T20:32:01.7721652Z**, for the fresh production fixture
`owner-acceptance-570dae1e9a1a4d9c8260936c7a937057`. Its SHA-256 is
`444DD7DA7234DBCC4B78C60E82BA6EA2BCD8992CB694CC865A4A098F23A9D2A4`.
This continuation re-read the actual source, terminal, audit and transcript files
and independently matched all four byte counts and hashes in that receipt.

- Actual caller `C:\Program Files\PowerShell\7\pwsh.exe`, version **7.6.5**, matches
  the same-run expected caller. All nine captured fields match: host/version,
  current directory, `DB_FILE`, `HT_RUNTIME_DIR`, `TEMP`, `TMP`, npm cache and bytecode.
- Source-console database/runtime environment values are identical before and after
  creation and distinct from the target. This proves environment preservation;
  it does not assert source-database byte equality during an active snapshot.
- The exact target has one registered, unblocked `ANNOTATED` row, the expected
  owner/branch/identity and no review reasons. Both fixture worktrees are registered
  and unblocked. Audit exit **1** and `ok=false` identify only the expected new child
  missing from the old disposable baseline; they do not indicate failed creation.
- The transcript records successful production creation and the exact subsequent
  terminal capture command. The owner reported capturing the observation in the
  actual new terminal. This reviewer read saved evidence, launched no terminal and
  claims neither direct visual observation nor a new acceptance run.
- The original `source-and-audit-result.json` retains its pre-capture `PENDING`
  field. The later capture/review supersedes it without rewriting raw evidence.
  All original evidence and fixtures remain retained.

At re-verification, `scripts/new-worktree.ps1` SHA-256
`DCBDA8C0E5236C8FC67F487AD5E9759EA4223B242B51F1E4EC328EB7277ED05A`
matched the reviewed bootstrap correction. The original
[bootstrap validation receipt](../../artifacts/worktree-cleanup-planning/council-20260905/bootstrap-fix-validation-receipt.json)
SHA-256 is `BA519A18CBE5A6A65E081970B9CF5DE62FD4D1E8071475B966C7FE9A36E1DA40`;
its [full reviewed diff](../../artifacts/worktree-cleanup-planning/council-20260905/bootstrap-fix-full.diff)
SHA-256 is `AEA529C405510721BCABEFD620EE94B0C77953CAED90ECB245A7CDF4B7D1B9C4`.
Both artifacts were independently hashed and match their recorded bindings.
Reuse after integration must identify unchanged surfaces. This acceptance does not
attest changed launch behavior, external installation, actual installed hook
interception or active lifecycle monitoring.

### Current gate checklist

- [x] Signed Gate 0 and Operation A Plan v2 Gate 1 remain effective, including the
      named standalone SQLite/diagnostics exception and unchanged technical contracts.
- [x] Owner-run disposable interactive Windows acceptance is recorded and verified
      against the exact reviewed bootstrap launcher and same-run raw evidence.
- [x] Authorized local upstream integration and path-derived checks completed;
      fresh results and reused evidence are distinguished below.
- [x] Integrated diff, refreshed publication proposal and Gate 2 review packet
      prepared; final capture is refreshed after this documentation update.
      Old digest-pinned publication commands remain stale and unexecuted.
- [ ] Owner grants Gate 2 approval and separately authorizes publication/merge;
      publication and merge are actually verified.
- [ ] Owner applies approved current external deltas and verifies installation,
      fresh environment scope and actual installed interception.
- [ ] Owner approves lifecycle annotations/baseline and monitoring mechanism,
      installs them and verifies fresh reports and active monitoring.
- [ ] Every technical-design Gate A obligation is verified before any
      `PREVENTION_COMPLETE` declaration. It is **not declared** here.

**Continuation provenance:** Read-only manager `/root` assigned new worker
`/root/planning_review` as product-manager for this append, then sequentially as
coordinated documentation support for MASTER_HANDOVER and the technical plan's
factual approval-status header. The same worker is not multiple independent
reviewers, did not author the original council and claims no original-worker
continuity. `/root/integration_dev` owns production/conflict integration and Git
mutations; `/root/integration_qa` owns tests and validation. Native read tools were
unavailable; the manager authorized bounded read-only shell/hash access and
byte-preserving document writes. Git checkout had changed the planning file's line
endings; restoring LF exactly recovered the verified original prefix before append.
This documentation worker changed no production code, tests, evidence or fixtures.
Independent review of implementation and documentation remains separate from authorship.

### Integrated result and Gate 2 handoff

The original reviewed packet is preserved at local commit
`123c9fbdf6b532f058fb53965bb656a8a14677d1`. A separate
`operation-a-integration-20260905` branch applies only Operation A to freshly
advertised/fetched upstream `0f1ac2ed66c24151f6d8c00d9962ebd8a959ad6f`; the local
integration commit is `093dd04f45c217e20da2bbafda7c62561a102d5e` before this final
documentation update. Its conflict resolutions preserve the reviewed stronger
guard/status behavior, all incoming upstream tests and both handover histories.
The three unrelated local audit commits remain on the preserved original branch;
they are excluded from publication ancestry. All **1,798** unrelated upstream
paths are mode/blob-identical to the verified base.

Fresh [QA evidence](../../artifacts/worktree-cleanup-integration-20260905/operation-a-integration-qa.json):
the standalone guard passed **168 cases** across both installed hosts, profiles
and permission modes; the integrated guard/workflow union passed **516 tests**,
zero failures/skips, **314.53 seconds**. Pyright **1.1.410** checked **247 files**
with zero diagnostics and zero net-new. Unchanged lifecycle **146**, snapshot
**33**, preflight **66** (a subset of the historical 686 union) and interactive
acceptance evidence were reused after source/test/helper/dependency identity
checks, not rerun. These overlapping historical results are not added to fresh
counts or presented as a final full five-module run.

Inventory collection proved drift from upstream **2,919 → 3,174** deterministic
pytest nodes. The generator then ran and final `--check` passed: **130** deterministic
pytest files, **131** files overall; Playwright **686/33 specs** and Vitest
**245/13 files** unchanged. Existing private Click **8.4.2** versus upstream
**8.5.0**, and `@types/node` **26.2.0** versus **26.4.0**, bound local evidence to
that environment; no dependency installation or pinned remote-CI pass is claimed.
No unrelated upstream application work is claimed as freshly retested.

Post-collector [preservation proof](../../artifacts/worktree-cleanup-integration-20260905/preservation-before-final-docs.json)
passed for **41,781** original entries, including **26,772 files / 193,059,738 bytes**,
the original reviewed evidence/fixtures, all **15** protected source hashes against
historical and turn-start baselines, and the source registry's **90 roots** plus
**11** runtime/log members. No original evidence or fixture was rewritten.
Code/manual/unslop integration review found no open issues after correcting the
owner-procedure status link. `/root/planning_review` performed those roles
sequentially, excluding its own authored planning/handover/header prose; the
manager and `/root/integration_qa` independently reviewed that prose. This same
worker now resumes product-manager solely for this results append.

The review packet is private under `artifacts/worktree-cleanup-integration-20260905/`:
[validation receipt](../../artifacts/worktree-cleanup-integration-20260905/integration-validation-receipt.json),
[exact Git/diff capture](../../artifacts/worktree-cleanup-integration-20260905/integration-capture-receipt.json),
[final preservation](../../artifacts/worktree-cleanup-integration-20260905/preservation-final.json),
[upstream-relative publication diff](../../artifacts/worktree-cleanup-integration-20260905/operation-a-upstream.diff),
[reviewed-packet comparison](../../artifacts/worktree-cleanup-integration-20260905/operation-a-reviewed-packet-relative.diff),
[Operation A scope comparison](../../artifacts/worktree-cleanup-integration-20260905/operation-a-reviewed-scope-relative.diff),
[refreshed publication proposal](../../artifacts/worktree-cleanup-integration-20260905/publication-proposal.md)
and [PR body](../../artifacts/worktree-cleanup-integration-20260905/operation-a-pr-body.md).
The pre-documentation diff and preservation capture already exist; final captures
bind the subsequent documentation-only commit without a self-referential digest
in this tracked record. Six original council Markdown hard breaks remain preserved;
the other whitespace classes pass.

**Stop: Gate 2 owner approval is pending.** Push, PR creation, merge, external
installation, installed interception and lifecycle baseline/active monitoring
remain unperformed. The source-pointing `origin` is not a publication destination.
Operations B–E and cleanup remain unauthorized; `PREVENTION_COMPLETE` is not declared.
