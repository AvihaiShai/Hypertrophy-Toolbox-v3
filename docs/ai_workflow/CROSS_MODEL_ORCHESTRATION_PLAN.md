# Cross-Model Orchestration — Proposed Plan

**Status:** Proposed; Gate 0 and Gate 1 are not approved  
**Primary owner:** Repository owner  
**Proposed outer orchestrator:** Codex  
**Proposed delegated worker:** Claude Code using Opus  
**Requested pre-council reviewer:** Fable 5  

This proposal extends the existing AI workflow; it does not create a second set of
quality gates. [`QUALITY_GATE.md`](QUALITY_GATE.md),
[`AUTONOMY.md`](AUTONOMY.md), and
[`PARALLEL_WORKFLOW.md`](PARALLEL_WORKFLOW.md) remain canonical.

---

## Section 0 — Requirements Brief

**Raw requests** (verbatim)

> i want the codex to be the orchistrator and OPus will be the worker and span multiple agents

> and how can we make it automated so I won't need some magic prompts in order to loopit for the right flow

> what the other option inssted of each prompt enter flow chart for delegation.
>
> how can I trigger the mechanism in prompt magic word

> add proposed plan to be reviewd by Fable5 under the ai_workflow folder

### Problem

The repository has a mature Claude-oriented manager and specialist-agent workflow,
but it has no Codex entry point that can deliberately invoke that workflow while
keeping Codex responsible for decomposition, integration, independent verification,
and the final answer. Blindly forwarding every prompt to Opus would add latency and
token cost without adding judgment. Requiring the owner to relay messages or repeat a
large orchestration prompt would defeat the purpose of automation.

### Acceptance criteria

1. Given an ordinary prompt without the explicit orchestration trigger, when Codex
   handles it, then no Claude/Opus process is started by this mechanism.
2. Given `$orchestrate <goal>`, when the workflow starts, then Codex first inspects
   repository state, decomposes the goal, records acceptance checks, and states why
   each proposed delegation adds value before invoking Opus.
3. Given an orchestrated task, when Codex delegates, then Opus receives bounded work
   packages rather than the raw user prompt as its entire assignment.
4. Given an Opus work package, when parallel work is useful, then the Opus main
   session may use the existing allowlisted Claude agents; Codex remains the outer
   orchestrator and final integrator.
5. Given a response from Opus, when Codex evaluates it, then Codex independently
   inspects changed files and verification evidence rather than treating the worker's
   `complete` claim as proof.
6. Given actionable review findings, when another Opus turn is justified, then the
   mechanism resumes the recorded Claude session with delta-only feedback; it does not
   resend the complete original prompt.
7. Given no changed evidence, an unchanged diff, a repeated failure, a required owner
   gate, or the configured round cap, when the state machine evaluates progress, then
   it terminates or pauses instead of looping indefinitely.
8. Given a workflow pause, when `$orchestrate status` is requested, then state is read
   without invoking Opus; `$orchestrate resume` continues the recorded task, and
   `$orchestrate stop` prevents further delegation.
9. Given a medium or large task, when the canonical planning rules require Gate 0 or
   Gate 1, then the mechanism stops for owner authority exactly as the existing
   workflow requires. It automates agent-to-agent relaying, not owner decisions.
10. Given concurrent work that may edit files, run tests, start the app, or touch the
    database, when a worker is launched, then it uses a checkout created according to
    `PARALLEL_WORKFLOW.md`; no two checkouts share `data/database.db`.
11. Given a direct, ordinary Opus session started by the owner, when this Codex skill
    is not the entry point, then the session remains outside this mechanism and does
    not call Codex automatically.
12. Given generated orchestration state or transcripts, when they are persisted, then
    they are stored under gitignored `artifacts/`, never at the repository root and
    never in a tracked planning artifact.

### Calculation surface

- `none`; this proposal must not change product calculations, database schema, API
  contracts, or runtime application behavior.

### In scope

- An explicit `$orchestrate` Codex skill trigger.
- A Codex-owned state machine and task decomposition contract.
- A thin, non-interactive Claude Code invocation adapter for Opus.
- Reuse of existing `.claude/agents/` roles and canonical AI workflow rules.
- Persisted, gitignored task state sufficient for status, resume, and stop.
- Bounded retries, independent Codex review, failure handling, and token controls.
- Documentation and deterministic dry-run evidence for the orchestration mechanism.

### Out of scope / non-goals

- Invoking Opus for every prompt or making delegation implicit for normal prompts.
- Replacing `docs/ai_workflow/` with a Codex-specific duplicate workflow.
- Making Opus or its subagents the final authority over scope, acceptance, or gates.
- Connecting two already-open interactive chat windows.
- Allowing circular delegation in which Opus calls Codex and Codex calls Opus without
  a bounded state transition.
- Removing Gate 0, Gate 1, Gate 2, sandbox, reviewer, or worktree requirements.
- Changing reviewer models or making Fable 5 a permanent runtime dependency before
  the seeded evaluation required by the existing Phase 6 plan.
- Automatically committing, pushing, merging, deleting worktrees, or editing the
  tracked main-checkout database.

### Assumptions made

- ⚠️ `$orchestrate` is the desired explicit trigger name.
- ⚠️ An orchestrated task should use one Opus main session per active phase and resume
  it only for concrete feedback; phase boundaries may start a fresh session from
  canonical artifacts if context growth makes continuation wasteful.
- ⚠️ Two Codex-to-Opus correction rounds per phase are a safe initial cap. A lower or
  higher cap requires an owner decision and dry-run evidence.
- ⚠️ Existing Claude roles remain `model: inherit`; this plan does not silently
  choose cheaper models for subagents.
- ⚠️ Direct Opus usage remains an intentional bypass rather than being mechanically
  forced through Codex.

### Open questions for the owner

1. Confirm `$orchestrate` as the trigger, or choose another skill name.
2. Confirm the initial maximum of two Codex-to-Opus correction rounds per phase.
3. Should bounded **medium** changes invoke one Opus worker by default after the
   trigger, or should Opus be reserved for large/parallelizable/high-risk work even
   when `$orchestrate` was used?
4. Should `$orchestrate stop` merely mark the task stopped, or also terminate a live
   Claude child process after a graceful timeout?

### Section 0 sign-off — GATE 0

- [ ] Owner confirms the acceptance criteria match intent.
- [ ] Owner reviewed and accepted or corrected every assumption.
- [ ] Blocking questions are answered.

---

## Plan v1

### Goal

Provide an opt-in Codex orchestration mechanism in which Codex owns reasoning,
decomposition, integration, and completion decisions while Opus and its existing
Claude subagents perform only bounded, value-justified work packages.

### Responsibility boundary

```text
Owner
  └─ approves required gates
     └─ Codex outer orchestrator
        ├─ owns problem model, task graph, state, integration, and final response
        ├─ performs central-path work that does not benefit from delegation
        └─ invokes Opus for bounded packages with explicit expected value
           └─ Opus inner manager
              └─ delegates to existing Claude specialists when useful
```

The Opus manager is the primary router only inside its delegated Claude phase. It is
not the overall task owner and cannot expand scope or approve an owner gate.

### Routing policy

The explicit trigger selects the mechanism; it does not force a Claude call.

| Task shape after `$orchestrate` | Initial route |
|---|---|
| Explanation, status, or trivial change | Codex handles directly and records that delegation had no expected value |
| Complex but cohesive/sequential | Codex owns the central path; Opus may receive a focused review or investigation package |
| Parallelizable investigation or implementation | Codex creates independent packages; Opus coordinates allowlisted Claude agents |
| Ambiguous or high-risk change | Codex establishes the decision questions; Opus runs bounded planning/review work; owner gates remain mandatory |
| Worker result with no new diff/evidence | Stop; do not spend another worker turn |

No adapter call may use the user's raw prompt as the complete Opus assignment. Every
call must include a recorded delegation reason, bounded objective, allowed paths,
constraints, deliverables, acceptance checks, and stop conditions.

### State machine

```text
ROUTE
  ├─ DIRECT_CODEX ───────────────────────────────────────────┐
  ├─ WAIT_OWNER_GATE ──(approved)──> BUILD_WORK_PACKAGES     │
  └─ BUILD_WORK_PACKAGES ──> RUN_OPUS ──> CODEX_REVIEW       │
                                      ├─ accepted ──> VERIFY ┤
                                      ├─ actionable delta ──> RESUME_OPUS
                                      ├─ owner decision ──> WAIT_OWNER_GATE
                                      └─ no progress/cap ──> BLOCKED
  VERIFY
    ├─ pass ──> COMPLETE
    └─ attributable failure + remaining round ──> RESUME_OPUS
```

Terminal states are `COMPLETE`, `STOPPED`, and `BLOCKED`. `WAIT_OWNER_GATE` is a
pause, not a failure. A task may have at most one live Claude process and one writer
inside a checkout unless the approved plan and `PARALLEL_WORKFLOW.md` provide isolated
worktrees and non-overlapping ownership.

### Delegation contract

Each worker request should be generated as structured data equivalent to:

```json
{
  "task_id": "stable-task-id",
  "phase": "plan|implement|review|verify",
  "objective": "bounded outcome",
  "delegation_reason": "specific expected value from Opus or parallel agents",
  "artifact_paths": ["canonical files to read directly"],
  "allowed_paths": ["paths the worker may modify"],
  "constraints": ["scope, safety, and compatibility constraints"],
  "deliverables": ["patch, findings, or verification evidence"],
  "acceptance_checks": ["observable checks Codex will independently evaluate"],
  "stop_conditions": ["conditions that require return rather than improvisation"]
}
```

The worker result must use a validated schema with at least `status`, `summary`,
`changed_paths`, `verification`, `risks`, `owner_decisions`, and `session_id`. A
worker's `status: complete` is advisory until Codex verifies the deliverables.

### Persistence and continuity

Persist generated state at `artifacts/orchestration/<task-id>/state.json`. The state
must contain no credentials and should include only the task ID, phase, status,
checkout, artifact paths, Claude session ID, process metadata needed for safe stop,
review-round count, last observed diff identity, and timestamps.

- `$orchestrate status` reads state and repository evidence without starting Claude.
- `$orchestrate resume` validates that the checkout, session, and diff identity still
  match before continuing.
- `$orchestrate stop` records `STOPPED` and prevents future resumes unless the owner
  explicitly starts a new task or chooses a defined reopen action.
- Missing or stale Claude session state falls back to a fresh worker that reads the
  canonical artifacts; it must not pretend conversational continuity was preserved.

### Token and loop controls

1. Normal prompts do not load or execute the orchestration body.
2. The trigger starts one task-level state machine, not a turn-by-turn conversation
   relay.
3. Codex passes artifact paths and delta feedback instead of duplicating file contents
   and prior reports.
4. Opus handles its internal subagent prompts; Codex does not micromanage every Claude
   specialist turn.
5. A second worker call requires new actionable information and an explicit expected
   outcome.
6. Unchanged diff identity plus unchanged verification evidence is a no-progress
   terminal condition.
7. Round and time limits are explicit configuration with conservative defaults.
8. Structured worker output is concise and excludes raw subagent transcripts unless
   a blocking finding requires exact evidence.

### Safety and failure handling

- Invoke Claude without interpolating untrusted prompt text into a shell command.
  Prefer stdin, a structured SDK call, or an argument-safe process API.
- Use existing Claude authentication; never copy credentials into state, prompts, or
  tracked files.
- Keep child-process permissions no broader than the delegated work package.
- Validate the resolved checkout before any worker write or process termination.
- Never infer approval for commits, pushes, merges, destructive Git commands, schema
  changes, or owner-only gates.
- On malformed output, timeout, missing executable, authentication failure, stale
  session, or worker crash, record a typed failure and return control to Codex. Do not
  retry indefinitely.
- Apply the tracked-database and one-checkout-per-feature rules by reference to
  `PARALLEL_WORKFLOW.md`; do not reproduce or weaken them in the adapter.

### Proposed artifacts

| Path | Change | Purpose |
|---|---|---|
| `.agents/skills/orchestrate/SKILL.md` | new | Explicit trigger, routing rules, state transitions, and Codex responsibility contract |
| `.agents/skills/orchestrate/scripts/invoke-opus.ps1` | new | Argument-safe Claude invocation, structured result capture, resume, timeout, and stop support |
| `.agents/skills/orchestrate/references/result-schema.json` | new | Machine-readable worker-result contract |
| `AGENTS.md` | modify | Point Codex to the opt-in skill without duplicating the workflow |
| `docs/ai_workflow/AUTONOMY.md` | modify | Document the outer-Codex/inner-Opus authority boundary and direct-Opus bypass |
| `docs/ai_workflow/INDEX.md` | modify | Link the accepted orchestration policy and skill after approval |
| `docs/ai_workflow/CROSS_MODEL_ORCHESTRATION_PLAN.md` | retain | Requirements, review findings, dispositions, approved plan, and evidence |
| `artifacts/orchestration/**` | generated, gitignored | Per-task runtime state and diagnostic evidence; never committed |

### Sequence

1. Complete Gate 0 by resolving the four owner questions and signing the requirements
   brief.
2. Run the normal plan council. Fable 5's pre-council review is additional evidence,
   not a replacement for the three required council roles.
3. Record every finding verbatim, disposition it, produce Plan v2, and obtain Gate 1.
4. Create the repo skill metadata and instructions before the invocation adapter so
   the behavioral contract is reviewable independently of shell code.
5. Define and validate the worker result schema.
6. Implement the PowerShell adapter with argument-safe invocation, typed failures,
   timeout handling, session capture/resume, and safe stop behavior.
7. Add the minimal `AGENTS.md`, `AUTONOMY.md`, and index wiring; do not copy the full
   orchestration procedure into multiple files.
8. Run deterministic dry-runs using a disposable worktree and fake or controlled
   worker results before any live Opus test.
9. Run one bounded live smoke with a read-only task, followed by one isolated
   trivial-edit probe demonstrating that Codex can decline delegation after the
   explicit trigger.
10. Perform the AI-workflow manual review gate and record evidence. Do not enable the
    skill as an implicit default.

### Required dry-run matrix

| Scenario | Required observation |
|---|---|
| Normal prompt | No orchestration process or state directory created |
| `$orchestrate` trivial task | Codex chooses `DIRECT_CODEX`; no Claude process |
| Bounded worker package | Exactly one argument-safe Opus invocation and schema-valid result |
| Actionable Codex finding | Same valid session resumed with delta-only feedback |
| Unchanged diff/evidence | No additional worker invocation; task blocks or completes explicitly |
| Round cap reached | No further invocation; typed `BLOCKED` result |
| Gate 0 or Gate 1 required | State pauses before implementation and names the required owner decision |
| Malformed worker JSON | Typed failure; no unbounded retry |
| Missing/stale session | Evidence gap recorded; fresh-session fallback reads artifacts directly |
| Stop request | State changes to `STOPPED`; validated live child process receives graceful termination behavior selected at Gate 0 |
| Concurrent DB/test work | Separate script-created worktree and isolated `data/database.db` |
| Direct Opus session | No automatic Codex callback or orchestration state mutation |

### Expected gates

- Planning size: **Large / new workflow**.
- Gate 0: required before council review is finalized.
- Gate 1: required after council-reviewed Plan v2 and before implementation.
- Implementation verification: AI workflow / agent config manual dry-run and careful
  self-review or `code-reviewer`; targeted script tests if the adapter introduces
  executable behavior.
- Gate 2: owner review of the resulting diff and evidence before commit or activation.
- Application pytest/E2E: not required unless implementation changes source behavior;
  the union rule still applies if scope expands.

---

## Fable 5 Pre-Council Review

**Status:** Completed — verdict `REVISE_BEFORE_GATE_0_REVIEW`  
**Model:** `claude-fable-5`  
**Review session:** `256cea85-118e-445f-9fd2-2139d47c4728`  
**Execution note:** The first broad-source attempt timed out before returning a final
response and produced no review evidence. The successful bounded pass read the plan
and the relevant canonical workflow documents directly. Its findings are advisory
and have not been silently folded into Plan v1.

Requested review focus:

1. Whether Codex performs substantive orchestration rather than prompt forwarding.
2. Whether the opt-in trigger actually prevents trivial-prompt delegation tax.
3. Whether state, resume, stop, and terminal conditions prevent circular or runaway
   calls.
4. Whether authority and Gate 0/Gate 1/Gate 2 boundaries remain unambiguous.
5. Whether the PowerShell/Claude invocation design is safe on this Windows checkout.
6. Whether worktree and SQLite isolation rules are preserved by reference.
7. Whether the plan duplicates or conflicts with the current `manager` charter or
   Phase 6 default-manager evaluation.
8. Missing acceptance probes, failure modes, security controls, or token-cost guards.

### Findings (verbatim)

Review complete. Plan v1 is structurally strong — the opt-in trigger, delegation contract, no-progress terminal conditions, and dry-run matrix are genuinely substantive — but two HIGH findings contradict recorded host/charter facts and reach into Section 0's acceptance criteria, so the requirements brief needs revision before Gate 0 review.

**F5-1 — HIGH — Codex sandbox contradicts the adapter's core operations.**
Evidence: `docs/ai_workflow/AUTONOMY.md:25` records the Codex layer-2 containment as `sandbox_mode = "workspace-write"` with `network_access = false`; `docs/ai_workflow/CROSS_MODEL_ORCHESTRATION_PLAN.md:273` has the adapter spawn `claude` (which requires network egress for API auth), and `docs/ai_workflow/PARALLEL_WORKFLOW.md:41` places worktrees in a *sibling* directory (`..\Hypertrophy-Toolbox-v3-<slug>`) outside the workspace-write boundary. As specified, the child Claude process cannot authenticate and the "script-created worktree" dry-run row (plan line 317) cannot create its checkout. Correction: add an acceptance criterion and a Plan v2 section naming the sandbox escalation mechanism for the adapter (per-invocation escalation or a scoped config exception), and state explicitly what remains of layer-2 containment when the worker runs escalated.

**F5-2 — HIGH — "Opus inner manager" is unimplementable as written and conflicts with the `manager` charter.**
Evidence: plan lines 153–157 and 48–50 route work packages through an "Opus inner manager" that "may use the existing allowlisted Claude agents", and the delegation contract (line 204) includes an `implement` phase. But `.claude/agents/manager.md:4-5` makes `manager` read-only (`disallowedTools: Write, Edit, NotebookEdit, Bash, PowerShell`), so it cannot execute an implement package; a plain `claude -p` session, conversely, is bound by no agent allowlist, voiding the guarantee criterion 4 relies on. (Recorded host constraint from the Agent Workflow v2 arc: per-agent `mcpServers` don't attach in `claude -p --agent` primary mode — worth re-verifying, but it further constrains the `--agent` route.) Correction: specify the invocation entry point per phase (e.g., `--agent manager` only for plan/review packages; implement packages via a defined writer path), reconcile with the fact that `manager.md:41-42` makes the inner manager *also* stop for Gates 0/1/2, and add this as owner question 5 if the choice is a real decision.

**F5-3 — MEDIUM — the state machine collapses three distinct gates into one node.**
Evidence: plan line 182 shows a single `WAIT_OWNER_GATE ──(approved)──> BUILD_WORK_PACKAGES` transition, and lines 187–189 show `VERIFY ──pass──> COMPLETE` with no owner-review pause. `docs/ai_workflow/QUALITY_GATE.md:14` requires Gate 0 → council → Gate 1 in sequence for Large work, and `manager.md:41-42` treats Gate 2 as an owner stop before commit. Correction: parameterize `WAIT_OWNER_GATE` with the specific gate awaited, place the council between Gate 0 and Gate 1 for orchestrated Large tasks, and define `COMPLETE` as "uncommitted diff in the checkout awaiting Gate 2 owner review" (consistent with the no-auto-commit non-goal at lines 102–103).

**F5-4 — MEDIUM — resume validation omits the two known Windows session hazards.**
Evidence: plan lines 227–229 validate "checkout, session, and diff identity" on resume but not process liveness or path casing. On this host, a live idle `claude.exe` holds its session ID's lock (a second attach fails with exit code 1), and drive-letter case differences split the session-store project key, making a recorded session ID undiscoverable from a differently-cased cwd — both previously recorded on this machine; re-verify against the current Claude Code version. Correction: state.json must record child PID and the exact launch path; `resume` must confirm the prior child has exited (or route to `stop` semantics first) and relaunch from the byte-identical, case-normalized working directory.

**F5-5 — MEDIUM — no cross-task mutual exclusion.**
Evidence: plan lines 192–195 cap "at most one live Claude process and one writer" *per task*; nothing prevents two concurrent `$orchestrate` tasks from both claiming the same checkout as writer, violating `PARALLEL_WORKFLOW.md:17-21` (when to fork) and the one-writer rule itself. The dry-run matrix (lines 305–318) has no second-active-task row. Correction: add a checkout-scoped lock (e.g., `artifacts/orchestration/active-task.lock`) that refuses starting a second active task in the same checkout, plus a matching dry-run row.

**F5-6 — MEDIUM — VERIFY is not bound to the canonical test derivation, making "independent verification" untestable.**
Evidence: criterion 5 (plan lines 51–53) and the `VERIFY` state (lines 187–189) never define what Codex verifies against, while `QUALITY_GATE.md:22-39` and `:54-64` already define the change-type → test derivation deterministically. Correction: require `VERIFY` to run the QUALITY_GATE targeted-test union derived from the worker's `changed_paths` and record the derived set in `state.json`, so the "Bounded worker package" dry-run row has an objective pass condition.

**F5-7 — LOW — adapter shell and encoding unpinned.**
Evidence: plan lines 254–255 say "prefer stdin", but this host has both Windows PowerShell 5.1 and pwsh, and 5.1's default pipeline encoding corrupts UTF-8 payloads piped to native executables. Correction: pin `invoke-opus.ps1` to `pwsh` 7+ with explicit UTF-8 (`[Console]::OutputEncoding`, `utf8NoBOM`), and pass the work-package JSON via a temp file path rather than raw stdin text.

**F5-8 — LOW — `.agents/skills/` discovery is unverified in this repo.**
Evidence: plan line 272 proposes `.agents/skills/orchestrate/SKILL.md`; no `.agents/` directory exists anywhere in the checkout (root `AGENTS.md` does exist, so that modify target is fine). The dry-run "normal prompt" row would false-pass even if the installed Codex version never loads the skill, since nothing loads in either case. Correction: add an early sequence step proving the installed Codex CLI actually loads the skill body on `$orchestrate` (a harmless marker behavior) before the adapter is built.

The two HIGH findings change what Section 0 must ask the owner (sandbox escalation, worker entry point), so the requirements brief should absorb them before Gate 0 sign-off. No finding here is a disposition — all await the owner and the required council per the plan's own sequence.

REVISE_BEFORE_GATE_0_REVIEW

---

## Claude (Opus 5) Pre-Council Review

**Status:** Completed — verdict `REVISE_BEFORE_GATE_0_REVIEW` (host readiness must be
proven first)
**Model:** `claude-opus-5[1m]`
**Reviewed:** 2026-08-01, main checkout, no files modified other than this document.
**Relationship to the Fable 5 pass:** independent and additive. Nothing below is folded
into Plan v1, and no Fable 5 finding is dispositioned here. Where the two reviews touch
the same area the finding IDs are cross-referenced.

**Execution note:** this pass differs from the Fable 5 pass in that it *ran* the host
tooling rather than reading the plan against the documents. Several claims in Plan v1
and in the Fable 5 review turn out to be either wrong or unmeasurable on this machine
today. All commands and raw outputs are recorded in "Measured host evidence" below so
that the council can reproduce them, and every finding carries a version stamp —
`codex-cli 0.135.0`, `claude 2.1.220`, `PowerShell 7.6.4`.

### Measured host evidence

| # | Command | Observed result |
|---|---|---|
| E1 | `codex --version` | `codex-cli 0.135.0`; `codex doctor` reports **`0.146.0 available`** |
| E2 | `codex exec -s workspace-write "…"` (configured model) | `ERROR … status 400 … "The 'gpt-5.6-sol' model requires a newer version of Codex."` — **the orchestrator's own default model cannot run non-interactively on the installed CLI** |
| E3 | same, plus `codex_models_manager::cache` line | `failed to load models cache: unknown variant 'max', expected one of 'none','minimal','low','medium','high','xhigh'` — version skew between the cached model list and the binary |
| E4 | `codex exec -m gpt-5.5 -s workspace-write "Run: git rev-parse --abbrev-ref HEAD"` | `execution error: Io(Custom { kind: Other, error: "windows sandbox: spawn setup refresh" })` — **no shell command can be spawned at all under the sandboxed exec path** |
| E5 | header printed by every `codex exec` run | `approval: never` and `sandbox: workspace-write [workdir, /tmp, $TMPDIR]` |
| E6 | `codex exec --dangerously-bypass-approvals-and-sandbox …` | Ran successfully: `main`, and a TCP connect to `api.anthropic.com:443` returned `True` |
| E7 | `codex sandbox --permissions-profile workspace-write …` | `Error: default_permissions requires a [permissions] table` — the standalone sandbox runner is unusable with this config |
| E8 | live `C:\Users\aviha\.codex\config.toml` | `approval_policy = "on-request"` (**not** `"never"`), `sandbox_mode = "workspace-write"`, `network_access = false`, `[windows] sandbox = "elevated"` |
| E9 | `codex features list` | `multi_agent stable true`, `hooks stable true`, `elevated_windows_sandbox removed false`, `experimental_windows_sandbox removed false` |
| E10 | bundled `skills/.system/skill-creator/SKILL.md:256,292` and `skill-installer/SKILL.md:48` | Skills are discovered from **`$CODEX_HOME/skills`** (`~/.codex/skills`); no repo-relative discovery root is documented |
| E11 | `ls .agents` in the checkout | absent (confirms F5-8's premise) |
| E12 | `claude --help` (2.1.220) | `--session-id`, `--json-schema`, `--agents`, `--agent`, `--permission-mode {plan,acceptEdits,dontAsk,bypassPermissions,manual,auto}`, `--allowedTools`, `--disallowedTools`, `--tools`, `--max-budget-usd`, `--add-dir`, `--bg`, `claude agents --json`, `--worktree`, `--fork-session`, `--setting-sources`, `--strict-mcp-config`, `--safe-mode`, `--bare` all exist |

**Not measured:** whether `network_access = false` is actually enforced for a child
process under the Windows sandbox. The probe could not run because the sandboxed spawn
itself fails (E4). Only the *bypassed* path was measured, and there the network is open
(E6). F5-1's "the child Claude process cannot authenticate" is therefore an untested
assertion on this host, not an established fact.

### Findings

**C-1 — BLOCKER — the mechanism cannot be dry-run on this host today; Gate 0 needs a
host-readiness probe before it can be signed.**
Evidence: E4 — every sandboxed `codex exec` shell spawn fails with
`windows sandbox: spawn setup refresh`; E2 — the configured model 400s on the installed
CLI. The plan's sequence steps 8 and 9 and *every row* of the Required dry-run matrix
depend on Codex being able to spawn a process non-interactively. None of them can
produce evidence right now. Correction: add sequence step 0, "prove host readiness",
with three pass conditions — `codex exec` runs the *configured* model, `codex exec`
spawns a shell command under `-s workspace-write`, and `claude -p` returns a
schema-valid result — and make Gate 0 sign-off contingent on them. This is a
prerequisite, not a plan revision, and it is cheap to check after upgrading to 0.146.0.

**C-2 — HIGH — extends F5-1: in the non-interactive path the sandbox is all-or-nothing,
so "per-invocation escalation" is not an available control.**
Evidence: E5 — `codex exec` prints `approval: never` even though the live config says
`approval_policy = "on-request"` (E8), so there is no escalation prompt to grant; E6 —
the only configuration that executed anything was
`--dangerously-bypass-approvals-and-sandbox`, which simultaneously restored full
filesystem access *and* full network egress. F5-1's proposed correction ("per-invocation
escalation or a scoped config exception") assumes a graduated control that this CLI
version does not offer in `exec` mode. The real choice is binary and belongs to the
owner: either (a) the adapter is invoked from the **interactive** Codex session, where
`on-request` can still escalate a single command, or (b) orchestrated work runs with
layer 2 of [`AUTONOMY.md`](AUTONOMY.md) **removed entirely**, compensated by layers 1, 3
and 4. Correction: state which, as an acceptance criterion, and say plainly in
`AUTONOMY.md` what the four-layer model degrades to during an orchestrated task. Do not
describe it as "partial containment".

**C-3 — HIGH — extends F5-8: the proposed skill path is not merely unverified, it is the
wrong root, and that breaks the plan's own reviewability argument.**
Evidence: E10 — Codex 0.135.0 discovers skills from `$CODEX_HOME/skills`; E11 — no
`.agents/` exists. The consequence goes past F5-8: the plan's sequence step 4
deliberately lands the behavioral contract before the shell code "so the behavioral
contract is reviewable independently", but a file in `~/.codex/skills/` is machine-local,
untracked, unreviewable in a PR, and invisible to Gate 2. Correction: keep the tracked
source inside the repo (`docs/ai_workflow/orchestrate/SKILL.md` or
`scripts/codex/orchestrate/`), add an idempotent install script that copies it to
`$CODEX_HOME/skills/orchestrate/`, and add a dry-run row asserting the installed copy is
byte-identical to the tracked source. Without the drift check, the reviewed artifact and
the executed artifact are different files.

**C-4 — HIGH — the orchestrator is version-skewed, so every finding in this document has
a short shelf life.**
Evidence: E1, E2, E3. The installed CLI is two minor versions behind, its cached model
list contains an effort variant it cannot parse, and its configured model is rejected by
the API. Skill discovery, sandbox behavior, and `exec` flags are all plausible things to
change between 0.135 and 0.146. Correction: upgrade first, then re-run the probes above,
then record the Codex version, model, and Claude Code version in
`artifacts/orchestration/<task-id>/state.json` and as a Gate 1 precondition. A
cross-model mechanism whose two halves version independently needs the versions in its
state, not just in a plan document.

**C-5 — MEDIUM — `$orchestrate` is a prompt convention, not a dispatch primitive, which
makes acceptance criterion 1 unfalsifiable.**
Evidence: Codex skills are selected by the model from `name` and `description` (E10,
bundled `skill-creator` frontmatter section); nothing in `codex --help` or
`codex exec --help` exposes a literal `$`-prefixed dispatch. As specified, "Codex sees
`$orchestrate` and enters the state machine" is model judgment reading `AGENTS.md` —
which is precisely the "magic prompt" nondeterminism the raw request asked to remove,
and it means criterion 1 ("no Claude process is started without the trigger") can be
violated by an ordinary prompt that merely *sounds* orchestration-shaped. Correction:
prove deterministic dispatch before building the adapter. Two candidates exist on this
host: a custom prompt under `$CODEX_HOME/prompts/` (verify the directory is honoured in
0.135/0.146 — it does not currently exist), and the `hooks` feature, which E9 shows as
`stable`/`true`. Record which mechanism was chosen and add a negative probe — a batch of
ordinary prompts, zero orchestration state directories created — as a real dry-run row
rather than the current "Normal prompt" row, which F5-8 correctly notes would false-pass.

**C-6 — MEDIUM — the adapter reimplements six controls the Claude CLI already provides
natively; adopting them removes most of the bespoke PowerShell surface.**
Evidence: E12. This is the largest simplification available to Plan v2.

| Plan v1 mechanism | Native replacement (claude 2.1.220) | Effect |
|---|---|---|
| Capture `session_id` from worker output; "missing/stale session" fallback | `--session-id <uuid>` — the **caller assigns** the ID | Deletes the capture/parse step and most of F5-4's failure class; the ID is known before the process starts, so state is valid even if the worker dies mid-run |
| Hand-rolled result-schema validation in the adapter, `references/result-schema.json` | `--json-schema '<schema>'` with `--output-format json` | Validation moves into the worker process; "Malformed worker JSON" becomes a typed CLI failure instead of adapter parsing logic |
| "Opus inner manager … may use the existing allowlisted Claude agents" (the F5-2 contradiction) | `--agents '<json>'` to define a purpose-built worker inline, plus `--agent`, `--allowedTools`, `--disallowedTools`, `--tools` | Resolves F5-2 without overloading the read-only `manager` charter: a plan/review package gets `--permission-mode plan`, an implement package gets `--permission-mode acceptEdits` and an explicit tool list. Enforcement becomes **mechanical** rather than charter-textual |
| `state.json` process metadata, PID tracking, graceful-stop design (open question 4) | `--bg` plus `claude agents --json` (documented as not requiring a TTY) | Status and stop become CLI queries instead of hand-rolled process management; directly serves `$orchestrate status` / `stop` |
| Round caps as the only cost control | `--max-budget-usd <amount>` | A hard ceiling that holds even when a single round runs long; complements rather than replaces the round cap |
| Sibling worktree outside the writable root (F5-1, E5) | `--add-dir <worktree>` on the Claude side; `--add-dir` / `-C` on the Codex side | The documented mechanism for granting the worktree path, and it is per-invocation rather than a config change |

Also relevant to deterministic dry-runs: `--setting-sources`, `--strict-mcp-config`,
`--safe-mode`, and `--bare` let a dry-run pin exactly which settings, MCP servers, and
customizations the worker loads, so a matrix row means the same thing on another
machine. Plan v1 has no reproducibility control at all.

**C-7 — MEDIUM — `claude --worktree` must be an explicit non-goal, or it will silently
violate the DB isolation contract.**
Evidence: E12 shows the flag exists; [`PARALLEL_WORKFLOW.md`](PARALLEL_WORKFLOW.md) lines
40–46 and 69–80 place the DB seeding and the `git update-index --skip-worktree
data/database.db` step inside `scripts/new-worktree.ps1`. A worker (or an adapter author)
reaching for `--worktree` gets a checkout carrying HEAD's tracked `data/database.db` with
no seed and no `--skip-worktree`, which is exactly the corruption and
accidental-DB-commit path the tracked-DB rule exists to prevent. Plan v1 says "a checkout
created according to `PARALLEL_WORKFLOW.md`" but never names the flag it must not use.
Correction: add `--worktree` to the non-goals, forbid it in the adapter, and add a
dry-run row asserting the worker's checkout was created by `scripts/new-worktree.ps1`
and that `git ls-files -v data/database.db` reports the skip-worktree flag.

**C-8 — MEDIUM — extends F5-6: binding VERIFY to `QUALITY_GATE.md` alone still lets a
worker produce a locally-green change that fails CI.**
Evidence: [`QUALITY_GATE.md`](QUALITY_GATE.md)'s change-type table derives pytest,
Playwright, and reviewer requirements but does not name two CI gates that block on this
repo — `Test Inventory Drift`, which fails on any test add or removal until
`scripts/generate_test_inventory.py` is re-run, and the `pyright measure-only` job, which
blocks net-new diagnostics via `scripts/pyright_baseline_diff.py`. An orchestrated
implement package that adds one test file passes every locally-derived gate and fails on
the PR. Correction: `VERIFY` must run the `QUALITY_GATE.md` union **plus** those two
scripts whenever `changed_paths` include `tests/**` or any `.py` file, and record the
derived set in `state.json` as F5-6 proposes. If the council agrees, the same two lines
belong in `QUALITY_GATE.md` itself, since the gap is not specific to orchestration.

**C-9 — MEDIUM — two of the three files the plan proposes to modify currently misstate
the live configuration; fix the drift before Plan v2 builds on those lines.**
Evidence: E8 versus [`AUTONOMY.md`](AUTONOMY.md) line 25 and [`AGENTS.md`](../../AGENTS.md)
line 9 — both record `approval_policy = "never"`; the live config says `"on-request"`.
Neither file mentions `[windows] sandbox = "elevated"`, which is set in config while E9
lists both `elevated_windows_sandbox` and `experimental_windows_sandbox` as `removed`.
F5-1 reasons *from* AUTONOMY.md line 25 as if it described the machine. Correction: land
the AUTONOMY.md/AGENTS.md correction as a standalone docs change ahead of this plan, and
run `codex --strict-config` once to surface config keys the installed binary no longer
recognises. A plan that reasons about containment from a stale description of the
containment will keep producing findings like F5-1.

**C-10 — STRATEGIC — the architecture puts the fragile half at the root of the tree; the
owner should choose the direction explicitly at Gate 0 rather than inherit it.**
Evidence, consolidated: the proposed orchestrator is the side that currently cannot spawn
a subprocess (E4), cannot run its configured model (E2), is two versions behind (E1),
cannot host a repo-tracked skill (E10), and has no verified deterministic trigger (C-5).
The proposed worker is the side that already has a repo-tracked, gate-aware, charter-
driven agent system — `manager`, `product-manager`, `senior-developer`, the three council
reviewers, `/council-plan`, and a permission allowlist — with per-invocation capability
control built into its CLI (E12). Plan v1 spends its entire complexity budget rebuilding
orchestration on the weaker side. That may still be the right call, because the owner's
stated intent is cross-model independence: a reviewer that shares no weights with the
implementer catches different things, and Codex owning the final answer is what makes it
independent rather than advisory. That is a real benefit and this finding does not argue
against it. It argues that the alternatives were never priced. Three options for the
owner:

- **Option A — as proposed.** Codex orchestrates, Opus works. Highest independence,
  highest build cost, and blocked on C-1 through C-5.
- **Option B — invert the direction.** The existing Claude `manager` orchestrates using
  machinery that already exists and is already gated, and calls
  `codex exec --json --output-schema <file> -o <file>` as an independent cross-model
  reviewer at plan time and diff time. Codex becomes a leaf, so its sandbox, version, and
  trigger problems stop being load-bearing; `--output-schema` gives the structured result
  the plan wants; Claude Code already has Bash. Retains most of the cross-model value at a
  fraction of the build cost, but Codex no longer owns the final answer.
- **Option C — MCP bridge.** `codex mcp-server` (stdio) registered as an MCP server in
  Claude Code, or `claude mcp serve` registered in Codex. Replaces the hand-rolled
  PowerShell process adapter with typed tool calls, and removes F5-7's shell/encoding
  problem entirely. Cost: an MCP surface to secure, and — per the recorded host note from
  the Agent Workflow v2 arc — MCP attachment behaviour in non-interactive Claude modes
  needs re-verification on 2.1.220.

Correction: add this as owner question 5 or 6 and record the decision with its reasoning.
Whatever is chosen, the priced comparison belongs in the artifact, because a future
reader will otherwise assume Option A was the only design considered.

**C-11 — LOW — no cost or latency budget is quantified anywhere in the plan.**
Evidence: the token-controls section is entirely qualitative ("conservative defaults",
"bounded"), and open question 2 asks the owner to confirm a round cap with no measured
per-round cost to confirm it against. Correction: pass `--max-budget-usd` on every worker
invocation (C-6), and record real wall-clock and token/cost figures from the first live
smoke as Gate 1 evidence, so the round cap is set from data rather than from intuition.

**C-12 — LOW — the plan does not say what happens to `docs/MASTER_HANDOVER.md`.**
Evidence: root [`CLAUDE.md`](../../CLAUDE.md) makes the Master Handover canonical for
point-in-time state and [`PARALLEL_WORKFLOW.md`](PARALLEL_WORKFLOW.md) line 88 lists it
as a never-claimed shared path, yet an orchestrated task produces exactly the kind of
state that normally lands there. Correction: state that orchestration state lives only
in gitignored `artifacts/` (criterion 12 already implies this) and that the handover
update remains a normal owner-gated step performed after Gate 2 — not something the state
machine writes.

### Recommended Section 0 changes

These are proposals for the owner and the council, not edits. Plan v1 and the Section 0
brief are left untouched.

**New acceptance criteria**

13. Given the host-readiness probe (C-1), when it has not passed, then Gate 0 cannot be
    signed and no adapter code is written.
14. Given an orchestrated task, when a worker runs, then the recorded state contains the
    Codex CLI version, the Codex model, and the Claude Code version in effect (C-4).
15. Given the orchestration skill, when it executes, then the installed copy is verified
    byte-identical to the repo-tracked source (C-3).
16. Given a worker package, when it is invoked, then its capability boundary is enforced
    by CLI flags (`--permission-mode`, `--allowedTools`/`--tools`, `--session-id`,
    `--json-schema`), not by charter prose alone (C-6).
17. Given any worker checkout, when it is created, then it was created by
    `scripts/new-worktree.ps1`; `claude --worktree` is never used (C-7).
18. Given `VERIFY`, when `changed_paths` include `tests/**` or any `.py` file, then the
    test-inventory and pyright-baseline scripts run as part of the derived set (C-8).

**Assumptions to correct**

- The assumption that layer-2 containment survives orchestrated work is not supported on
  this host (C-2). Restate it as an owner decision.
- The assumption that `$orchestrate` is a dispatch mechanism is unproven (C-5). Restate
  it as "trigger mechanism TBD, to be selected from custom prompt or hook".

**Additional owner questions**

5. Interactive-session escalation or explicit sandbox bypass for orchestrated work
   (C-2)?
6. Option A, B, or C for the orchestration direction (C-10)?
7. Upgrade Codex to 0.146.0 before Gate 0, or pin 0.135.0 and accept that the configured
   model cannot be used non-interactively (C-4)?

### Recommended additions to the dry-run matrix

| Scenario | Required observation |
|---|---|
| Host readiness (C-1) | Configured model runs under `codex exec`; a shell command spawns under `-s workspace-write`; `claude -p --json-schema` returns a valid object |
| Trigger determinism (C-5) | A batch of ordinary prompts creates zero orchestration state; the trigger creates it every time |
| Skill drift (C-3) | Installed `$CODEX_HOME/skills/orchestrate/SKILL.md` is byte-identical to the tracked source |
| Version stamp (C-4) | `state.json` records both CLI versions and the model actually used |
| Capability boundary (C-6) | A `plan`-phase worker launched with `--permission-mode plan` produces no file writes even when the package text invites them |
| Worktree provenance (C-7) | Worker checkout was produced by `scripts/new-worktree.ps1`; `git ls-files -v data/database.db` shows the skip-worktree flag |
| CI-gate derivation (C-8) | A package that adds a test file causes `VERIFY` to derive and run the test-inventory script |
| Second active task (F5-5) | The checkout-scoped lock refuses the second `$orchestrate` start |
| Budget ceiling (C-11) | A worker invocation with an exceeded `--max-budget-usd` terminates typed, not silently |

### Verdict

`REVISE_BEFORE_GATE_0_REVIEW`

Plan v1 is a genuinely good piece of design work — the opt-in trigger, the delegation
contract, the no-progress terminal condition, and the dry-run matrix are the right
skeleton, and the Fable 5 pass sharpened it further. The problem is that both reviews so
far reasoned from documents, and this host does not match those documents: the
orchestrator cannot currently spawn a process, cannot run its configured model, and
cannot host the skill where the plan puts it. C-1 through C-5 are prerequisites rather
than design changes; C-6 is where the plan gets substantially smaller if adopted; C-10 is
the one question worth answering before any code is written.

Findings C-1 through C-12 are advisory and undispositioned, exactly like F5-1 through
F5-8. They await the owner and the required three-agent council.

---

## Fable 5 Second-Pass Review (Owner-Clarified Goal)

**Status:** Completed — verdict `REVISE_BEFORE_GATE_0_REVIEW`
**Model:** `claude-fable-5[1m]`
**Reviewed:** 2026-08-02, main checkout; only this document was edited.
**Session:** `bcb1c28a-9702-4e2c-9fd5-d2123138a54a` (distinct from the first Fable 5
pass, session `256cea85…`).
**Relationship to prior passes:** independent third pass. It dispositions nothing —
F5-1–F5-8 and C-1–C-12 all still await the owner and the council — and it does not
modify Plan v1 or Section 0. Its distinct input is a goal clarification received from
the owner *after* both prior reviews, quoted verbatim below. The prior passes reviewed
the plan against the four raw requests; this pass reviews it against what the owner has
now said they actually want, and it deliberately re-examines the two earlier reviews
for shared blind spots.

### Newly received owner input (2026-08-02, verbatim)

> the goal is create orchstrator that you openai models will be able to talk with
> anthropic models without me as a mediator in the middle to copy-paste responses and
> we need a solution that won't waste tokes for simple tasks that can be diriect one
> model without passing it around for serval models and\or span multiple agents, we
> need a better system the span agents as well beside the openai-antorpic comunication
> inside this project.

Read as three goals:

- **G1 — no-mediator channel.** OpenAI models and Anthropic models exchange messages
  without the owner copy-pasting between windows.
- **G2 — token-tiered routing.** Simple tasks go directly to one model; no multi-hop
  relay and no agent fan-out unless the task earns it.
- **G3 — a better agent-spawning system** inside this project, beyond the cross-vendor
  channel itself.

Plan v1 serves G1 partially (one-directional delegation, not an exchange), G2 partially
(a routing table exists, but the only entry point is the heaviest mechanism), and G3
not at all. That mismatch drives most of the findings below.

### Findings

**F5B-1 — HIGH — the plan solves delegation; the owner described conversation.**
Evidence: the delegation contract (plan lines ~199–218) gives the worker result
`status`, `summary`, `changed_paths`, `verification`, `risks`, `owner_decisions`,
`session_id` — there is no field through which the worker can ask the orchestrator a
question, and the state machine (lines ~178–195) has `RESUME_OPUS` for Codex→worker
feedback but no worker→Codex clarification transition. A worker that hits mid-task
ambiguity must improvise (violating its own stop conditions), burn a full round, or go
`BLOCKED` — all three are wrong for G1, whose verb is "talk with". Correction: add
`status: "needs_input"` plus a `questions[]` field to the result schema, and an
`ANSWER_WORKER` transition that resumes the same session with answers only. An answer
exchange counts toward the round cap so the loop-control guarantees survive.

**F5B-2 — HIGH — there is no lightweight consult primitive; the state machine is the
only door.**
Evidence: the routing table (lines ~160–175) routes everything arriving *after
`$orchestrate`*, and the cheapest route still loads the full skill body and records a
delegation decision. But most of the real-world copy-paste mediation G1 describes is
"ask the other model what it thinks of X" — one bounded question, one bounded answer,
no work packages, no worktree, no `state.json`. Forcing that through a task-level state
machine is exactly the token and latency waste G2 forbids, and it will push the owner
back to manual copy-paste — the mechanism failing by disuse. Correction: split the
mechanism into tiers (see "A better implementation shape" below). A one-shot
`$consult`-class primitive — read-only, schema-bounded output, no persisted task state
beyond one log line — should exist *beside* `$orchestrate`, and the skill should route
between them.

**F5B-3 — HIGH — neither CLI's native multi-agent surface was surveyed before
proposing a hand-rolled one (G3).**
Evidence: E9 already records `multi_agent` as **stable and enabled** in Codex 0.135.0
(with `enable_fanout` under development); Claude Code 2.1.220 ships in-session
subagents (the repo's `.claude/agents/` roster of eleven charters), background agents
(`--bg`, `claude agents --json`), and deterministic multi-agent workflow scripts. Plan
v1 proposes a bespoke outer state machine without once asking what either vendor's
native orchestration already does — the classic build-vs-audit inversion, and for G3 it
is the difference between a config change and a quarter of engineering. Correction: add
an explicit survey step to the sequence — enumerate both CLIs' native spawn/fan-out
capabilities at current versions, with a one-line verdict per capability ("sufficient /
insufficient because …") — and let the adapter build only the glue the survey proves
missing.

**F5B-4 — HIGH — MCP likely dissolves the two hardest host blockers and should be
evaluated *first*, not carried as Option C.**
This elevates C-10's Option C and corrects the prior Claude pass's ordering, which
priced the option but still treated the Plan v1 skeleton as the default. The
architectural fact both prior passes missed: **MCP servers are spawned by the host CLI
process at startup, not through the model's sandboxed shell tool.** If that holds on
this host, E4 (`windows sandbox: spawn setup refresh` — the sandboxed spawn failure
that currently blocks every dry-run row) and the F5-1/C-2 network-egress question
simply do not apply to a registered Claude MCP server, because the process never passes
through the sandboxed exec path. Owner question 5 (escalation vs. bypass) would then
dissolve for the consult tier entirely. Both directions exist natively today: Codex-host
via `codex mcp add` / `[mcp_servers]` in `config.toml` (the `mcp` subcommand is in E1's
help output), and Claude-host via repo-tracked `.mcp.json` — which also fixes the C-3
reviewability problem in that direction, since the registration itself becomes a
tracked, PR-reviewable file. Three probes before relying on this: (1) an MCP server
registered in Codex runs and reaches the network with `network_access = false`
(expected yes — host-spawned; must be measured, not assumed); (2) the exact tool
surface `claude mcp serve` exposes on 2.1.220 and its behavior on long calls — if the
surface is wrong-shaped for "ask Claude a question", a thin stdio wrapper around
`claude -p --json-schema` preserves the same host-spawned property; (3) registration on
Windows via config file, not shell `claude mcp add` (argument mangling previously
recorded on this host). Boundary: synchronous tool calls fit consults and reviews, not
hour-long implement packages — the long tier still needs background delegation
(`--bg` + `claude agents --json`, per C-6).

**F5B-5 — MEDIUM — the PR is already a working cross-model message bus in this repo;
the review loop may need almost no new infrastructure.**
Evidence: the owner's raw request "loop it for the right flow" is, concretely, an
implement→review→fix loop; this repo's established workflow already auto-creates a PR
on push and auto-merges on green CI, and both CLIs drive `gh`. So: Codex implements and
pushes → Claude reviews the PR and leaves comments → Codex reads the comments, fixes,
pushes again. The channel is durable, owner-observable at every step, survives version
skew on both CLIs, needs no session plumbing, no schema, and no state machine — CI is
already the loop's terminal condition. Correction: name the "PR-bus review loop" as an
explicit tier of the mechanism. It is nearly prompt-only to build and may deliver most
of G1's looping value on its own.

**F5B-6 — MEDIUM — cross-model output is untrusted input; no pass set the trust
boundary.**
Evidence: in every variant of this design, model A's free text lands in model B's
context (with MCP, tool results land verbatim). Nothing in Plan v1 or either review
says what happens when a worker result *contains instructions* — "also run X", "delete
Y", a prompt-injection payload picked up from a file the worker read. Corrections:
control flow is decided only by the orchestrator's own logic reading structured fields;
free-text fields (`summary`, `risks`) are data, never instructions; no command that
appears inside a result is executed without the orchestrator independently deriving it;
result sizes are capped. Add one dry-run row: a worker result containing an embedded
instruction produces no action beyond being recorded.

**F5B-7 — MEDIUM — removing the mediator removes the owner's observation point; live
visibility is unspecified.**
Evidence: today the copy-paste role is also how the owner *watches* the exchange and
catches derailment early. Plan v1 persists state for `status` queries (lines ~220–233)
but specifies no live view of the dialogue itself. Correction: append every cross-model
message — direction, models, timestamp, token count, truncated text — to
`artifacts/orchestration/<task-id>/dialogue.jsonl`, tail-able while the task runs
(`Get-Content -Wait`); `$orchestrate status` summarizes it. The consult tier logs one
line per consult to a session-level file. Without this, the first misrouted
conversation will be reconstructed from two CLIs' separate session stores, which is
exactly the mediation burden the mechanism was meant to remove.

**F5B-8 — MEDIUM — two writer-capable CLIs, one checkout: the one-writer rule must be
stated cross-vendor.**
Evidence: plan line ~193 caps "one live Claude process and one writer inside a
checkout" — but the orchestrator itself is a writer under `workspace-write`, and the
sentence is ambiguous about whether Codex counts toward its own cap. During a delegated
implement package in the shared checkout, both processes can write concurrently; that
is two writers by any reading of [`PARALLEL_WORKFLOW.md`](PARALLEL_WORKFLOW.md).
Correction: the delegation contract must state that while an implement package is live,
the orchestrator treats the working tree as read-only — or the package runs in a
script-created worktree (C-7). One dry-run row: orchestrator write attempted during a
live implement package → refused by the state machine.

**F5B-9 — MEDIUM — Section 0 must absorb the clarified goal before Gate 0 can mean
anything.**
Evidence: the verbatim input above post-dates every raw request in Section 0. G2
strengthens acceptance criterion 1 from "no Claude process without the trigger" into a
tiering requirement across *all* mechanisms; G1 adds the worker-question channel
(F5B-1) that no current criterion covers; and G3 is an entirely new scope question that
is currently in neither "In scope" nor "Out of scope" — the worst place for it, since
whoever drafts Plan v2 will resolve it silently. Correction: the Gate 0 re-draft
records G1–G3 verbatim in the requirements brief, adds acceptance criteria for the
question channel and the tier split, and either scopes G3 in (minimally: as the F5B-3
survey) or defers it explicitly.

**F5B-10 — LOW — per-invocation context tax and model tier are unpriced.**
Every one-shot `claude -p` consult pays a cold start — settings, CLAUDE.md, MCP
handshakes; seconds and kilotokens — acceptable for repo-aware questions, waste for
generic ones; a long-lived MCP-served session amortizes it. Routing should also pick
*model tier*, not only delegate-vs-direct: consults default to a fast tier and escalate
on request; implement packages use the full tier. On this host cost is not the binding
constraint — latency and quota are — which argues for the same tiering from a different
direction.

### A better implementation shape — answering the owner's direct question

The owner asked whether a better implementation exists. Yes: invert the build order and
split the mechanism into three tiers, each with its own trigger, transport, and cost
ceiling. Plan v1 builds only the heaviest tier and routes everything through it — the
single design decision most at odds with G2.

| Tier | Trigger | Transport | Cost / latency | Serves | Build cost |
|---|---|---|---|---|---|
| **1 — Consult** | "ask claude/codex …" or `$consult` | MCP tool call (host-spawned — F5B-4); fallback: one-shot `claude -p --json-schema` / `codex exec --output-schema` | seconds–minutes; one bounded, read-only call | G1 + G2 — the daily copy-paste pain | Small: registration, tool-description discipline, three probes |
| **2 — PR-bus review loop** | branch push / PR open | `gh` on both sides (F5B-5) | asynchronous, minutes; no live cross-process state | G1's "loop it for the right flow" | Near zero: prompt/docs conventions |
| **3 — Orchestrate** | `$orchestrate` | Plan v1's state machine, slimmed per C-6; worktrees per `PARALLEL_WORKFLOW.md` | bounded rounds and budgets | Large, parallel, high-risk work | Large; blocked on C-1…C-5 |

Build order: **Tier 1 → Tier 2 → re-evaluate whether Tier 3 is still needed.** The
honest possibility is that Tiers 1+2 absorb the real demand and the state machine is
never built — which is a success, not a failure, of this plan. Tier 1 also answers
Tier 3's hardest open question (the transport) at a fraction of the cost.

For G3 specifically: run the F5B-3 survey first, then prefer each vendor's native
spawner — Claude-side subagents/background agents/workflows over the existing
`.claude/agents/` roster; Codex-side its stable `multi_agent` — and let Tiers 1–3 be
the *only* cross-vendor glue. Do not build a meta-spawner that owns both vendors'
agents; that is the most expensive and most fragile of the available shapes, and
nothing in G1–G3 requires it.

### Additional owner questions (continuing the numbering)

8. Approve the three-tier shape and the Tier-1-first build order?
9. Directionality: Codex→Claude only, or symmetric consults (Claude can also ask
   Codex) from the start?
10. Consult trigger: natural language ("ask claude …") acceptable, or strict keyword
    only? Strict keywords give criterion-1-style determinism; natural language reads
    better but relies on model judgment.
11. G3: what exactly is unsatisfying about agent spawning today — council/manager
    weight on medium tasks, agent-selection friction, absence of cross-model
    specialists in one flow, handoff quality, something else? The answer decides
    whether G3 is a survey, a config change, or a real build.

### Owner responses to questions 8–11 (2026-08-02)

Recorded the same day as this review. These are Gate 0 *inputs*, not sign-off; they
must be absorbed into the Section 0 re-draft (F5B-9) and confirmed there.

- **Q8 — First build:** Tier 1 (consult) first, after the Section 0 re-draft.
- **Q9 — Directionality:** symmetric consults — either CLI may consult the other
  model; heavy orchestration remains Codex-led.
- **Q10 — Trigger:** hybrid — natural language ("ask claude/codex …") for read-only
  consults; the strict `$orchestrate` keyword reserved for the heavy tier.
- **Q11 — G3 pain points:** the owner selected **all four**: handoff quality,
  selection friction, council/manager weight on medium tasks, and absence of
  cross-model specialists in one flow.

Implication of Q11 that the Section 0 re-draft must not soften: G3 is a first-class
requirement area, not a survey afterthought. Two of the four pains point at the
mechanism this plan builds (cross-model specialists, handoff quality — served by the
tier design plus the artifact-path-not-paraphrase discipline the `manager` charter
already mandates), but the other two point at the *process itself*: "council/manager
too heavy for medium tasks" is feedback on the canonical planning flow in
[`QUALITY_GATE.md`](QUALITY_GATE.md), and "selection friction" asks for routing the
owner doesn't have to spell out. Neither can be fixed silently by this plan — changing
gate weight is an owner decision about canon, and it belongs in Section 0 as an
explicit scope question (in, or deferred to its own plan), not as a side effect of an
orchestration adapter.

### Verdict

`REVISE_BEFORE_GATE_0_REVIEW` — for a different reason than the first two passes. They
found the plan inconsistent with the host and the charters; this pass finds it aimed at
a narrower goal than the owner has now stated. The requirements brief predates the
clarification, so Gate 0 cannot be signed on the current Section 0 regardless of how
F5-x and C-x are dispositioned. The cheapest correct next step is not fixing the
adapter design — it is re-drafting Section 0 around G1–G3 and pricing the three-tier
shape against Plan v1 in the council.

F5B-1 through F5B-10 are advisory and undispositioned, like all prior findings.

---

## Response Matrix

_Pending owner decisions and the required council. Fable 5 findings F5-1 through
F5-8, Claude findings C-1 through C-12, and Fable 5 second-pass findings F5B-1
through F5B-10 have not been dispositioned._

---

## Plan v2

_Not drafted. Plan v2 must follow finding disposition and Gate 0 completion._

---

## Sign-off

- [ ] Host-readiness probe passed (C-1).
- [ ] Gate 0 complete.
- [ ] Fable 5 findings recorded verbatim and dispositioned.
- [ ] Claude findings C-1 through C-12 dispositioned.
- [ ] Fable 5 second-pass findings F5B-1 through F5B-10 dispositioned.
- [ ] Section 0 re-drafted to absorb the 2026-08-02 owner goal clarification (F5B-9).
- [ ] Required three-agent council completed with provenance.
- [ ] Every finding has a disposition.
- [ ] Owner approved Plan v2 (Gate 1).
- [ ] Ready to implement.
