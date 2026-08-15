# Cross-Model Orchestration — Tier 1 Consult

**Status — stated once, and the sign-off block at the foot of this document matches it:**
Gate 0 signed 2026-08-13 by the owner (Session 8 pack), which also pre-approved Gate 1 for
a consult-only, read-only, council-reviewed Plan v2. The council ran and returned three
`REVISE` verdicts; Plan v2 reflects them. Implementation proceeded under that pre-approval
and merged as **`9906105`** (PR #344, 18/18 checks green).

**Gate 2: ratified by the owner on 2026-08-13, *after* `9906105` merged.** The sequence
matters and is stated plainly rather than smoothed over: the diff landed on the owner's
pre-approval of Gates 0 and 1, and the owner reviewed and ratified it afterwards. This is
**post-merge ratification**, not pre-merge approval, and nothing in this document should be
read as claiming the owner saw the diff before it merged.

- **Primary owner:** Repository owner
- **Implemented scope:** the consult — either CLI asks the other model one bounded,
  read-only question
- **Deferred scope:** the heavier `$orchestrate` mechanism and the PR-bus loop, planned
  and explicitly unimplemented — see
  [Deferred mechanisms](#deferred-mechanisms--planned-not-implemented)
- **Pre-council reviewers (advisory, historical):** Fable 5, Claude Opus 5

This proposal extends the existing AI workflow; it does not create a second set of
quality gates. [`QUALITY_GATE.md`](QUALITY_GATE.md),
[`AUTONOMY.md`](AUTONOMY.md), and
[`PARALLEL_WORKFLOW.md`](PARALLEL_WORKFLOW.md) remain canonical.

> **This plan is closed.** The consult shipped as `9906105` and Gate 2 was ratified
> post-merge. What remains below the implementation is deferred scope with no
> authorisation attached. The [decision packet](#standalone-candidates--decision-packet)'s
> five loose ends have since been resolved — packets **A, B and C shipped** and **D was
> declined** — so the scope still deferred is the `$orchestrate` mechanism, the PR-bus
> loop, and the MCP transport a heavier tier would use. A read-only re-probe on
> **2026-08-14** found the three host blockers that defer `$orchestrate` unchanged; see
> [Host-readiness re-probe — 2026-08-14](#host-readiness-re-probe--2026-08-14-read-only).

> **Reading order.** Section 0 below is the **v2 requirements brief**, redrafted
> 2026-08-13 around the owner's G1–G3 goal clarification. The original 2026-08-01 brief
> is superseded; it survives in git history and every finding that changed it is
> dispositioned in the [Response matrix](#response-matrix). "Plan v1" further down is
> the original state-machine draft, retained unmodified as the audit trail for the three
> pre-council reviews. The plan that was actually built is
> [Plan v2 — the consult mechanism](#plan-v2--the-consult-mechanism).

---

## Section 0 — Requirements Brief (v2, redrafted 2026-08-13)

**Raw requests** (verbatim, in the order received)

> i want the codex to be the orchistrator and OPus will be the worker and span multiple agents

> and how can we make it automated so I won't need some magic prompts in order to loopit for the right flow

> what the other option inssted of each prompt enter flow chart for delegation.
>
> how can I trigger the mechanism in prompt magic word

> add proposed plan to be reviewd by Fable5 under the ai_workflow folder

Goal clarification received 2026-08-02, **after** all four requests above and after the
first two pre-council reviews (verbatim):

> the goal is create orchstrator that you openai models will be able to talk with
> anthropic models without me as a mediator in the middle to copy-paste responses and
> we need a solution that won't waste tokes for simple tasks that can be diriect one
> model without passing it around for serval models and\or span multiple agents, we
> need a better system the span agents as well beside the openai-antorpic comunication
> inside this project.

### The three goals

Finding F5B-9 requires the brief to be organised around this clarification rather than
around the earlier delegation framing. It is:

- **G1 — no-mediator channel.** An OpenAI model and an Anthropic model exchange a
  question and an answer without the owner copy-pasting between two windows.
- **G2 — token-tiered routing.** A simple task goes directly to one model. Nothing is
  relayed between models, and no agent fan-out happens, unless the task earns it.
- **G3 — a better agent-spawning system** inside this project, beyond the cross-vendor
  channel itself. The owner named **all four** pains (Q11): handoff quality, agent
  selection friction, council/manager weight on medium tasks, and the absence of
  cross-model specialists in one flow.

### Problem

Two capable CLIs are installed on this machine and both are authenticated, but nothing
connects them. Every cross-model exchange today is the owner copy-pasting a question
into the other window and pasting the answer back — the "mediator in the middle" G1
names. The 2026-08-01 brief proposed to solve this with a Codex-owned `$orchestrate`
state machine, but three independent reviews and a fresh host re-probe agree that the
heavy tier is both the most expensive thing to build and the thing this host is least
able to run: as measured again on 2026-08-13, the Codex CLI still cannot execute its
configured model non-interactively and still cannot spawn any process under
`workspace-write`. Meanwhile the cheap exchange the owner actually described — one
bounded question, one bounded answer, no work packages and no persisted task state —
has no mechanism at all, and forcing it through a task-level state machine is precisely
the token waste G2 forbids.

### Owner decisions absorbed into this brief

Recorded 2026-08-02 (Q8–Q11) and re-affirmed with additional decisions 2026-08-13. They
are **decisions, not assumptions**, and are not re-opened here:

| # | Decision |
|---|---|
| D1 | The three-tier architecture is approved, and Tier 1 is built first. |
| D2 | Tier 1 consults are **symmetric**: Claude may consult Codex and Codex may consult Claude. |
| D3 | Read-only consults use hybrid natural-language triggers ("ask Claude…", "ask Codex…"). The strict `$orchestrate` keyword stays reserved for the later heavy tier. |
| D4 | The initial correction cap is two rounds per phase. |
| D5 | A medium task does not automatically enter heavy orchestration. A Tier 1 consult may be selected when it has clear expected value; canonical planning gates are unchanged. |
| D6 | Stop performs a graceful timeout and then terminates only the owned child process if it is still live. |
| D7 | G3 covers all four pains. Tier 1 may reduce routing and consult friction, but may not weaken `QUALITY_GATE.md` and may not silently rewrite the `manager` role. |

### Acceptance criteria

Criteria are numbered continuously with the superseded brief so that the pre-council
findings that cite "criterion 4" or "criterion 12" still resolve. Criteria 1–12 are
restated for Tier 1; 13–18 come from the Claude pre-council pass; 19–26 are new and
come from G1–G3 and the 2026-08-13 re-probe.

1. Given an ordinary prompt with no consult trigger and no `$orchestrate` keyword, when
   either CLI handles it, then this mechanism starts **no** child model process.
2. *(Tier 3, deferred.)* Decomposition and delegation-value recording before invoking a
   worker. Not implemented; no Tier 1 surface may imply it exists.
3. Given a consult, when the caller invokes the adapter, then the callee receives a
   structured request — objective, question, artifact paths, constraints — and never the
   caller's raw prompt as its entire assignment.
4. Given a consult, when the callee runs, then its capability boundary is enforced by
   CLI flags rather than by prose: the Claude callee runs with `--permission-mode plan`
   and a write-tool denylist, and the Codex callee runs under `-s read-only`.
5. Given a consult result, when the caller uses it, then the result is **advisory until
   the caller independently verifies it**. The caller never treats a `status: success`
   claim as evidence.
6. *(Tier 3, deferred.)* Session resume with delta-only feedback. Tier 1 consults are
   one-shot and stateless; no session is resumed.
7. Given a consult, when it does not return a schema-valid result within the configured
   bounds, then the adapter returns a typed terminal outcome — `error`, `timeout`, or
   `cancelled` — and never retries on its own.
8. *(Tier 3, deferred.)* `$orchestrate status` / `resume` / `stop`. Tier 1 has no
   persisted task state to query; each consult writes one self-contained record.
9. Given a medium or large task, when the canonical planning rules require Gate 0 or
   Gate 1, then those gates still trigger exactly as before. A consult is evidence
   gathering; it is never an owner decision and never substitutes for a gate.
   **Extended after council (CR-16):** a consult also never satisfies a Required-reviewers
   cell in [`QUALITY_GATE.md`](QUALITY_GATE.md) and is never recorded as a council role.
   G3's "cross-model specialists in one flow" is served by consults being *available*, not
   by them counting as reviewers.
10. Given a consult, when it runs, then the only thing it writes is its own record under
    gitignored `artifacts/`; it creates no checkout, and the callee cannot write at all
    because criterion 4's flags forbid it. No worktree is therefore required, and the
    `PARALLEL_WORKFLOW.md` isolation rules are satisfied by construction.
    *(Restated after council, CR-10: the original wording said "neither writes to the
    checkout", which was literally false — the record lives inside it.)*
11. Given a direct, ordinary session in either CLI, when no consult trigger is used,
    then the session stays outside this mechanism and calls nothing automatically.
12. Given generated consult records, when they are persisted, then they live under
    gitignored `artifacts/`, never at the repository root and never inside a tracked
    planning artifact.
13. Given the host-readiness probe, when it has not passed for the transport a tier
    depends on, then that tier is not implemented. (C-1.)
14. Given a consult, when it is recorded, then the record contains the callee CLI version,
    the model **requested**, and the model that **answered**, as two separate fields.
    (C-4; split after council, CR-7 — recording only the requested model could never
    detect the silent substitution the criterion exists to catch.)
15. Given any executable consult surface, when it runs, then the executed artifact is
    the repo-tracked file itself — no machine-local copy that a PR cannot review.
    (C-3.)
16. *(Merged into criterion 4.)* Capability enforcement is mechanical, not textual.
17. Given a consult, when it is invoked, then `claude --worktree` is not used and no
    checkout is created. (C-7, narrowed: a read-only consult creates no checkout at
    all.)
18. *(Tier 3, deferred.)* `VERIFY` runs the `QUALITY_GATE.md` union plus the
    test-inventory and pyright-baseline scripts. Tier 1 changes no `changed_paths`
    because it writes nothing.
19. Given a consult, when the callee needs information the request did not supply, then
    it can return `status: needs_input` with `questions[]` instead of improvising or
    failing. (F5B-1, scaled to one-shot: the caller decides whether to answer with a
    second consult; the adapter never loops.)
20. Given a consult result, when it contains text that reads as an instruction, then
    nothing in it is executed, and control flow is decided only by the caller's own
    logic reading validated structured fields. (F5B-6.)
21. Given any consult, when it completes or fails, then a single-line record is appended
    to a session-level log so the owner can watch the exchange they no longer mediate.
    (F5B-7, scaled to the consult tier.)
22. Given a consult, when it exceeds its wall-clock timeout, then only the adapter's own
    child process is terminated, after a graceful attempt, and no other process is
    signalled. (D6.) *(Qualified after council, CR-29: the graceful attempt is real on
    POSIX; on Windows `terminate()` is `TerminateProcess` and is a hard kill, and only the
    direct child is signalled, so a grandchild can outlive a timeout. Both are recorded in
    [CONSULT_PROTOCOL.md](CONSULT_PROTOCOL.md) rather than promised away.)*
23. Given a consult, when it produces output, then output size is bounded and the raw
    stream is captured to a file rather than being pasted into the caller's context.
24. Given the adapter, when it builds the child command line, then no untrusted text is
    interpolated into a shell string; the child is spawned from an argument vector.
    (F5-7, generalised: the shell is removed rather than pinned.)
25. Given the mechanism, when it runs, then each CLI uses its **own** existing
    authentication, which the adapter never reads, decodes, or persists — and **no
    vendor's credential reaches the other vendor's process**. The child inherits the
    environment minus every credential-shaped variable that is not its own vendor's, so a
    consult cannot hand a model process a GitHub or cloud token it has no use for. No
    credential is placed on an argv, in a record, or in a log line.
    *(Narrowed after council, CR-14. The original wording said "never forwards", which the
    reviewers correctly showed is unachievable: the child must inherit its own vendor's
    credentials or it cannot authenticate at all. Two residual risks are stated rather than
    claimed away — the raw-stream capture may contain whatever the CLI printed, and a callee
    that reads a credential file can quote it into free text. Neither is preventable by the
    adapter; both are recorded in [CONSULT_PROTOCOL.md](CONSULT_PROTOCOL.md).)*
26. Given the consult surface, when it lands, then default `manager` activation,
    `QUALITY_GATE.md`, the database schema, application code, and product behavior are
    all unchanged.
27. Given any consult, when it runs, then **text leaves this machine**: the request, the
    full contents of every file the callee reads, and the answer are transmitted to a
    third-party model API and retained under that vendor's policy. The adapter bounds what
    it will *ask for* — `data/**`, any `*.db`, `logs/**`, `artifacts/**`, `.env*`, key and
    credential files, `.git/**`, and anything outside the repository are refused before any
    child starts — but it cannot bound what a callee reads on its own initiative.
    *(New after council, CR-12 and CR-13. This is the one place in a local-first repository
    where repository content deliberately leaves the machine, and the brief said nothing
    about it: the containment story had been written entirely on the write axis, and the
    read axis is where the owner's real training log lives.)*
28. Given the adapter, when it is invoked from a Claude Code session, then it runs under
    the **already-granted** `Bash(.venv/Scripts/python.exe:*)` permission and produces no
    prompt. *(New after council, CR-18: recorded as a consequence the owner should see, not
    a control the packet claims. `.claude/settings.json` is a never-claimed shared path
    under [PARALLEL_WORKFLOW.md](PARALLEL_WORKFLOW.md) and is deliberately not modified
    here. An `HT_CONSULT=1` opt-in was considered and rejected — the same agent that runs
    the adapter can set the variable, so it would buy the appearance of a gate without the
    substance. What actually bounds the risk is criterion 27's denylist and
    `--max-budget-usd`.)*

### Calculation surface

- `none`. This work changes no product calculation, no database schema, no API contract,
  and no runtime application behavior. It adds a developer-tooling adapter, its
  contracts, its tests, and workflow documentation.

### In scope

- One symmetric, read-only, one-shot consult adapter, invoked identically from either
  side, with a request contract and a result contract.
- Mechanical capability enforcement of the callee via CLI flags.
- Bounded timeout, bounded output, owned-child termination, and typed terminal outcomes
  for success, error, needs-input, timeout, and cancellation.
- Structured artifact-path handoff: the request names canonical paths for the callee to
  read directly instead of paraphrasing file contents.
- Tracked trigger surfaces on both sides — a Claude command and a Codex-facing protocol
  document reached from `AGENTS.md`.
- Gitignored per-consult records plus a session-level consult log.
- A deterministic dry-run matrix built on fixture CLIs, plus one real live smoke in each
  direction.
- Documentation of what Tier 2 and Tier 3 would add, and what still blocks them.

### Out of scope / non-goals

- The heavy `$orchestrate` state machine, its persisted task state, its round-capped
  correction loop, and its `status`/`resume`/`stop` verbs. Explicitly deferred.
- Any write-capable consult. Tier 1 consults are read-only in both directions.
- Session resume or any claim of conversational continuity between consults.
- Changing default `manager` activation, the council, or any `QUALITY_GATE.md` routing.
- Making a consult mandatory, automatic, or implicit for ordinary prompts.
- An MCP surface. Measured as viable on this host (see HR-6) but deferred with its
  evidence; Tier 1 needs no long-lived server and no new listening surface.
- `claude --worktree`, checkout creation, or any process that writes to the checkout.
- Committing, pushing, merging, deleting worktrees, or touching `data/database.db`.
- Changing reviewer models, or making any third model a runtime dependency.
- Fixing the Codex sandbox, the Codex version skew, or the configured-model 400. Those
  are recorded as host facts that bound what Tier 1 promises, not as work items here.

### Assumptions made

- ⚠️ The consult tier is worth building **before** either heavier tier, on the evidence
  that Tier 1's transport is the only one this host can run today. If the owner wants
  Tier 3 first, this ordering is wrong and the host blockers must be cleared first.
- ⚠️ A consult is worth its cold-start cost. Measured on this host: **$0.3055** and
  50,271 cache-creation tokens for a repo-loaded `claude -p` consult, **$0.0800** and
  39,184 tokens with settings and MCP servers suppressed (HR-9). The adapter therefore
  defaults to the cheap profile and lets the caller opt into the repo-loaded one.
- ⚠️ `gpt-5.5` is an acceptable Codex callee model while `gpt-5.6-sol` cannot run
  non-interactively on codex-cli 0.135.0 (HR-2). The adapter records which model
  answered, so a later upgrade is visible rather than silent.
- ⚠️ The Codex-side trigger is documentation the Codex model reads, not a dispatch
  primitive. C-5 is correct that no `$`-prefixed dispatch exists; the mitigation is that
  a consult is *inert until the adapter actually runs*, which is observable, rather than
  a claim about how reliably a keyword is recognised.
- ⚠️ Python is the right adapter language on this host, rather than the PowerShell of
  the superseded plan. It removes shell quoting entirely (criterion 24), it is testable
  from the existing pytest suite on both Windows and the Linux CI runner, and the repo
  already keeps comparable tooling in `scripts/*.py`.

### Open questions for the owner

`none` — Q1–Q11 were answered and are recorded as D1–D7 above and in
[Owner responses to questions 8–11](#owner-responses-to-questions-811-2026-08-02). This
brief does not re-ask them.

Two items are **reported, not asked**, because they change nothing in Tier 1 and need no
answer before implementation:

- The Codex→Claude direction cannot complete a consult inside `codex exec` under
  `-s workspace-write` or `-s read-only` (HR-3, HR-5, HR-7). Its supported entry points
  are the interactive Codex session, where `approval_policy = "on-request"` lets the
  owner approve the call, and `-s danger-full-access`, which is what the live smoke used
  (HR-12). This is recorded in the containment note rather than described as partial
  containment.
- Upgrading codex-cli from 0.135.0 to 0.146.0 would very likely change HR-2, HR-3 and
  HR-7. Tier 1 does not depend on the upgrade; Tier 3 does. **Re-probed read-only
  2026-08-14: no upgrade has happened and all three still hold.** The upgrade is now
  recorded as the explicit *trigger* for revisiting Tier 3, not merely as a likely fix —
  see [Host-readiness re-probe — 2026-08-14](#host-readiness-re-probe--2026-08-14-read-only).

### Section 0 sign-off — GATE 0

- [x] Owner confirms the acceptance criteria match intent — Gate 0 approval for this
      redrafted Section 0 was given in the Session 8 prompt (2026-08-13), which also
      supplied D1–D7 and instructed that Q1–Q11 not be re-asked.
- [x] **Owner reviewed and accepted or corrected every assumption — ratified 2026-08-13,
      after `9906105` merged.** This box was deliberately left unchecked until then,
      because the `product-risk-reviewer` was right that the five ⚠️ assumptions were
      written *after* the prompt cited as Gate 0 approval, so self-certifying it would have
      been the "never approve your own workflow" failure the `manager` charter names. The
      owner has now accepted the three load-bearing ones explicitly:
      - **Build order** — build the bounded consult first; `$orchestrate` and the PR-bus
        stay deferred.
      - **Callee model** — `gpt-5.5` as the **temporary** Codex callee while `gpt-5.6-sol`
        returns 400 non-interactively. Temporary is the operative word: every record
        carries the model that answered, so the day this stops being true it shows up in
        the evidence.
      - **Per-consult spend** — ~$0.08 lean / ~$0.31 repo-loaded, **with lean remaining the
        default**.

      The other two ⚠️ assumptions (Python as the adapter language; the Codex-side trigger
      being documentation rather than a dispatch primitive) were not separately raised and
      are accepted as part of the ratified diff.
- [x] Blocking questions are answered — none remain open. Two items are *reported* rather
      than asked, below.

---

## Host-readiness re-probe — 2026-08-13

C-1 made Gate 0 contingent on a host-readiness probe, and C-4 warned that every host
finding in this document has a short shelf life. Both were honoured: the probes below
were re-run from scratch in the `cross-model-tier1` worktree before any design work, and
they **changed the design**. Raw transcripts are under the gitignored
`artifacts/orchestration/probes/`; every row is reproducible from the command shown.

**Version stamp:** `codex-cli 0.135.0`, `claude 2.1.220 (Claude Code)`,
`PowerShell 7.6.4`, `node v24.19.0`. All three CLI versions are **unchanged** from the
2026-08-01 pass, so version skew (C-4) is confirmed still open, not resolved.

| # | Probe | Observed result | Effect on the design |
|---|---|---|---|
| HR-1 | `codex --version`, `claude --version`, `pwsh -c $PSVersionTable` | `0.135.0`, `2.1.220`, `7.6.4` | No version moved in 12 days. C-4 stands. |
| HR-2 | `codex exec -s workspace-write "…"` with the configured model | `400 … "The 'gpt-5.6-sol' model requires a newer version of Codex."` | E2 reconfirmed. The Codex callee must be given an explicit `-m`. |
| HR-3 | `codex exec -m gpt-5.5 -s workspace-write` running `git rev-parse` | `ERROR codex_core::exec: exec error: windows sandbox: spawn setup refresh`, `exited -1 in 0ms`, three retries | E4 reconfirmed **exactly**. Under `workspace-write` the Codex model cannot spawn any process at all. |
| HR-4 | `codex exec -m gpt-5.5 -s read-only --output-schema … -o …` reading `AGENTS.md` | pwsh **spawned successfully in 186 ms**; `Get-Content` returned; final message was schema-valid `{"status":"ok","answer":"# AGENTS.md"}` | **New, and it changes everything.** HR-3's failure is scoped to the write-capable sandbox, not to `codex exec` as such. The Codex side can act as a **read-only consult callee today**, with schema-validated output. |
| HR-5 | `codex exec -m gpt-5.5 -s read-only` asked to run `claude -p …` | `declined in 0ms: … rejected: blocked by policy` | Under `read-only`, Codex's *execpolicy* — a separate gate from the sandbox — refuses commands it cannot classify as reads. So Codex cannot call Claude from `read-only` either. |
| HR-6 | An stdio MCP server registered via `-c mcp_servers.…` and exercised under `-s workspace-write` | The server process **started** (`server start pid=… ppid=…`) and completed `initialize` and `tools/list` **while the shell tool was dead** | **F5B-4 confirmed on this host.** Codex spawns MCP servers from the host process, entirely outside the sandboxed exec path. |
| HR-7 | The same MCP server's `tools/call` in non-interactive `codex exec` | `mcp: hostprobe/host_probe (failed)` → `user cancelled MCP tool call`; unchanged by `--disable guardian_approval` | MCP transport is *spawnable* but not *callable* without an approver. In `codex exec` there is nobody to approve, so the call auto-declines. This is why Tier 1 does not ship an MCP surface. |
| HR-8 | `claude -p --output-format json --json-schema …` | Exit 0; `structured_output` present and schema-valid; `session_id` returned | The Claude side is a working consult callee, non-interactively, unattended. |
| HR-9 | Cost of one trivial `claude -p` consult | Repo-loaded default: **$0.3055**, 50,271 cache-creation tokens, 5.1 s. With `--model claude-haiku-4-5-20251001 --setting-sources "" --strict-mcp-config --mcp-config '{"mcpServers":{}}'`: **$0.0800**, 39,184 tokens, 4.7 s | C-11 and F5B-10 answered with numbers. A consult's floor cost is the cold start, and suppressing settings/MCP cuts it **3.8×**. The adapter defaults to the cheap profile. |
| HR-10 | `ls $CODEX_HOME/skills`, `ls $CODEX_HOME/prompts` | `skills/` exists and is **empty**; `prompts/` does not exist | E10/C-3 unchanged: there is still no repo-relative Codex skill root, which is why the Codex-side trigger is a tracked document plus a tracked script, not a machine-local skill. |
| HR-11 | `git ls-files data/`, `git check-ignore -v data/database.db` | `data/database.db` is **untracked** and ignored by `.gitignore:29 *.db` | **C-7's premise is stale.** The `git update-index --skip-worktree` assertion it proposed cannot pass, because the file is no longer tracked. Restated in the response matrix. |
| HR-12 | `codex exec -m gpt-5.5 -s danger-full-access` running `node -e …` | `{"status":"ok","answer":"CODEX_SPAWN_OK"}` | A **third** distinct behaviour, and the one the Codex→Claude live smoke uses. Spawning works; only `workspace-write` is broken. No `--dangerously-bypass-approvals-and-sandbox` was needed. |

### What the probes settle

1. **The two directions are not symmetric in difficulty, only in interface.**
   Claude→Codex runs unattended today (HR-4). Codex→Claude has no transport that
   completes inside `codex exec` under the containment the repo documents (HR-3, HR-5,
   HR-7); its working paths are the interactive session's own approval prompt and
   `-s danger-full-access` (HR-12). The adapter is therefore written once, symmetrically,
   and the asymmetry is recorded as a host limitation rather than hidden behind a
   wrapper that pretends both sides are equal.
2. **Tier 1 is the only tier this host can run.** Every Tier 3 dry-run row in the
   superseded plan needed `workspace-write` spawning, which is still dead (HR-3). The
   owner's Tier-1-first order (D1) is independently confirmed by measurement.
3. **`sandbox_mode` is not binary.** C-2 reasoned that the only choice was
   full containment or `--dangerously-bypass-approvals-and-sandbox`. There are three
   modes with three different behaviours (HR-3, HR-4, HR-12), and the middle one —
   `read-only` — is exactly what a consult callee needs.

---

## Host-readiness re-probe — 2026-08-14 (read-only)

C-4 said every host finding here has a short shelf life, so the three blockers that defer
`$orchestrate` — **HR-2, HR-3 and HR-7** — were re-checked one day after the table above.
This pass was deliberately bounded to **free, local, non-destructive** probes: no upgrade,
no live or model-billed call, no MCP server, no adapter change, no worktree. The
2026-08-13 table is left exactly as it was; this section records what a later, cheaper
pass could and could not establish.

**Version and configuration stamp — nothing moved.**

| Fact | Observed 2026-08-14 |
|---|---|
| `codex --version` | `codex-cli 0.135.0`; `codex.exe` mtime **2026-05-28**, so the binary was never replaced |
| `claude --version` | `2.1.220 (Claude Code)` |
| `~/.codex/config.toml` | mtime **2026-08-12 15:42** — *older than the 2026-08-13 probe pass*, so no setting changed after it was measured |
| `model` / `sandbox_mode` / `approval_policy` | `gpt-5.6-sol` / `workspace-write` / `on-request`, plus `[windows] sandbox = "elevated"` — identical to what `AGENTS.md` records |
| `codex mcp list` | `No MCP servers configured yet` — HR-6/HR-7's server was ad-hoc via `-c mcp_servers.…` and was never persisted |
| `~/.codex/rules/default.rules` | exactly two allows: `["git","status"]` and `["Get-Content"]` |
| Adapter surface | `scripts/consult/consult.py`, `request.schema.json`, `result.schema.json` all present and unmodified |
| CLI flags the adapter depends on | all still present — `--output-schema`, `-o`, `-s {read-only,workspace-write,danger-full-access}` on Codex; `--json-schema`, `--output-format`, `--permission-mode`, `--disallowedTools`, `--setting-sources`, `--strict-mcp-config` on Claude |
| `pytest tests/test_consult_adapter.py` | **59 passed in 6.97 s**, fixture CLIs only, no live call |

### HR-2's mechanism, established locally for the first time

The 2026-08-13 pass recorded HR-2 as an *observed* HTTP 400 — `"The 'gpt-5.6-sol' model
requires a newer version of Codex."` — without a local explanation. `~/.codex/models_cache.json`
supplies a candidate one, and since Codex rewrote that cache the same day it is not a stale
snapshot from the era of the original 400:

| Cached model | `tool_mode` | `multi_agent_version` |
|---|---|---|
| `gpt-5.6-sol` *(the configured model)* | `code_mode_only` | `v2` |
| `gpt-5.6-sol-wm`, `gpt-5.6-terra` | `code_mode_only` | `v2` |
| `gpt-5.6-luna`, `codex-auto-review` | `code_mode_only` | `v1` |
| **`gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`** | **absent** | **absent** |

`codex features list` on 0.135.0 reports `code_mode` and `code_mode_only` as
**`under development`, `false`**, and `multi_agent_v2` likewise. The entire `gpt-5.6`
family requires a tool mode this build does not implement; the three older models require
neither.

**How much this proves.** It is a specific, checkable requirement gap whose wording matches
the 400's, which is considerably better than the bare symptom recorded on 2026-08-13 — but
it is strong circumstantial evidence, not a server-confirmed cause. The server was never
asked. Its practical value is that it gives **P1** something free to falsify: if a later
build reports `code_mode_only` as supported and the 400 still happens, this explanation is
wrong and HR-2 needs a different one.

It also confirms that the adapter's existing `-m gpt-5.5` pin selects **one of the cached
models this build satisfies**, rather than being an arbitrary workaround. It is not the
only such model — `gpt-5.4` and `gpt-5.4-mini` carry neither requirement either, so if
`gpt-5.5` ever became unavailable the pin has somewhere to fall back to without waiting on
an upgrade.

### Status of the three blockers

| Blocker | Status 2026-08-14 | Basis |
|---|---|---|
| **HR-2** — configured model 400s non-interactively | **Still proven** | Both inputs unchanged (0.135.0, `model = "gpt-5.6-sol"`), *and* the candidate mechanism above supplies a requirement gap matching the 400's wording — circumstantial, not server-confirmed |
| **HR-3** — `workspace-write` cannot spawn any process | **Still proven** | Same binary, same config, config file older than the measurement. The recorded correlate is also intact: config requests `[windows] sandbox = "elevated"` while the build reports `elevated_windows_sandbox` **and** `experimental_windows_sandbox` as `removed`, and HR-3's error names the `windows sandbox` subsystem. That match is suggestive, not proof — `AGENTS.md` records the same mismatch "as observed, not endorsed" |
| **HR-7** — MCP `tools/call` auto-declines unattended | **Still proven** | No approver mechanism has appeared: `guardian_approval` still `stable` (and HR-7 already showed `--disable guardian_approval` does not change the outcome), `exec_permission_approvals` still `under development`/`false`. `tool_call_mcp_elicitation` is `stable`/`true`, but elicitation *requests* a human rather than substituting for one, so it cannot close HR-7 inside `codex exec` |

None is obsolete, and none is "likely changed but needs a live probe".

> **Evidence caveat, stated because it changes how much weight these rows carry.** All
> three were sustained through **unchanged preconditions, not re-execution.** No
> `codex exec` ran in this pass, so none of the three was re-measured. They are also not
> equally well supported, and collapsing them into one confidence level would be the
> mistake this note exists to prevent:
>
> - **HR-2** is the strongest — preconditions unchanged *and* a specific requirement gap
>   whose wording matches the 400, though the server was never asked to confirm it.
> - **HR-3** rests on unchanged preconditions plus a suggestive subsystem-name match. The
>   mechanism is plausible and undisturbed, but it was inferred here, not demonstrated.
> - **HR-7** is the weakest — the argument is only that the same build cannot have a
>   different code path. That is sound reasoning, but it is not evidence about behaviour.
>
> Anyone who needs a *measured* HR-7 must run P5 below and pay for it; a measured HR-3
> needs P3. Neither is worth doing before the upgrade that would change the answer.

### Post-upgrade probe matrix — P1 to P5

These are the **exact minimal** probes that would re-decide the three blockers. They are
worth running **only after** an owner-approved codex-cli upgrade; on 0.135.0 they spend
money to re-confirm what the evidence above already establishes.

| # | Probe | Cost | Authority required |
|---|---|---|---|
| **P1** | `codex --version`, then re-dump the `tool_mode` column of `models_cache.json` | **$0** | none |
| **P2** | `codex exec -m gpt-5.6-sol -s read-only "reply ok"` — has HR-2's 400 cleared? | ~$0 (a 400 bills no tokens) | none |
| **P3** | `codex exec -m <working model> -s workspace-write` running **`git status`** — HR-3 | ~$0.01–0.05 | none; layer 2 intact |
| **P4** | The same as P3 but running `git rev-parse` | ~$0.01–0.05 | none; layer 2 intact |
| **P5** | Register an ad-hoc stdio server via `-c mcp_servers.…` and issue one `tools/call` under `codex exec` — HR-7 | ~$0.01–0.05 | **owner** — starts a new local server process, which Tier 1 lists as a non-goal |

**Ordering is load-bearing, and P3 must not reuse HR-3's original command.** What isolates
the **sandbox spawn layer** from the **execpolicy layer** is using a command execpolicy
already allows, and `~/.codex/rules/default.rules` allows exactly two: `git status` and
`Get-Content`. Either would serve; `git status` is the one specified here because it keeps
HR-3's original `git` command shape and changes only the subcommand. HR-3's own
`git rev-parse` is refused by execpolicy independently of the sandbox, so a post-upgrade
run of it cannot distinguish "HR-3 still broken" from "HR-3 fixed, HR-5 still applies".
Run **P1 → P2 → P3 → P4 → P5** in order: P1 is free and may end the exercise on its own,
and P3 passing while P4 fails means HR-3 cleared and only HR-5 remains.

Total cost to re-decide all three is **well under $0.25**. Cost is not the constraint here;
authority is. P1–P4 need no new authority because `read-only` and `workspace-write` are the
containment [AUTONOMY.md](AUTONOMY.md) layer 2 already documents. P5 does. And any
**Codex→Claude live transport** probe still requires `-s danger-full-access`, which removes
layer 2 for that invocation — the genuine authority gate, and the reason
[CONSULT_PROTOCOL.md](CONSULT_PROTOCOL.md) says it should be chosen deliberately or not
at all.

### The trigger for revisiting

**Revisit only after an owner-approved Codex CLI upgrade.** Elapsed time is not a trigger,
and neither is a re-probe: the first step of any reopening is the upgrade itself, which is
an owner decision because it changes the host software and the sandbox and model surface
all three blockers sit on. Until it lands, a probe pass can only reconfirm the current
answer. When it does land, run P1 first — if the `tool_mode` gap closes, P2–P4 become
worth their few cents, and *only then* is there a Gate 0 conversation about `$orchestrate`.

### Gate routing for a future adapter change

This is a consequence of packet A shipping, and it is recorded here because it did not
hold when Plan v2 was written. [`QUALITY_GATE.md`](QUALITY_GATE.md) now carries a
`Tooling / scripts` row. `scripts/consult/consult.py` is **not** in that row's always-run
carve-out, and the stem plus directory-token derivation on `consult` returns a non-empty
union, so the `/verify-suite` fallback will **not** fire. Derived 2026-08-14, that search
names two files — `tests/test_consult_adapter.py` and `tests/fixtures/consult/fake_cli.py`
— of which only the first is a test module; the second is the fixture CLI those tests
drive. A future packet touching the adapter therefore routes to
**`tests/test_consult_adapter.py` plus `code-reviewer`**, where the same change would have
pulled the full suite before `5177176`. Re-derive the union rather than copying this
result; a non-empty union suppressing the fallback is exactly the shallow-coverage hazard
that packet A's own carve-out exists to bound.

---

## Plan v1 *(2026-08-01 — Tier 3 draft, superseded)*

> **Historical.** This is the original Codex-orchestrator state-machine plan. It is
> retained **unmodified** because the three pre-council reviews below cite its line
> numbers and its wording. It was **not** implemented. The implemented plan is
> [Plan v2 — the consult mechanism](#plan-v2--the-consult-mechanism); everything here that
> survived is recorded in the [Response matrix](#response-matrix), and everything that did
> not is deferred in
> [Deferred mechanisms](#deferred-mechanisms--planned-not-implemented).

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

## Response matrix

Every pre-council finding is dispositioned here. Dispositions are stated against
**Tier 1**, the scope that was actually built. A finding whose subject matter belongs to
a tier that was not built is dispositioned **defer**, with the tier that owns it named —
that is a scope statement, not a dismissal, and each deferred row is carried in
[Deferred mechanisms](#deferred-mechanisms--planned-not-implemented) so nothing is lost.

Three rows disposition **reject**. Each rejects a *premise* that the 2026-08-13 re-probe
measured to be false, and each says what replaced it.

### Fable 5 first pass (F5-1 – F5-8)

| Finding | Severity | Disposition | Action |
|---|---|---|---|
| **F5-1** — Codex sandbox contradicts the adapter's core operations; the child `claude` cannot authenticate and the sibling worktree is outside the writable root | HIGH | **reject (premise disproven), partially superseded** | The premise had two halves and both are now measured. (a) *Authentication:* `network_access = false` sits under `[sandbox_workspace_write]` and does not apply in `read-only`; the Codex callee reached the API under `-s read-only` (HR-4) and the Claude callee runs from the caller's own shell, not from inside Codex's sandbox. (b) *Worktree creation:* Tier 1 creates no checkout at all (criterion 10, 17), so the sibling-directory problem does not arise. The genuine residue — that `workspace-write` cannot spawn — is HR-3 and is dispositioned under C-1. |
| **F5-2** — "Opus inner manager" is unimplementable: `manager` is read-only so it cannot run an implement package, and a plain `claude -p` is bound by no allowlist | HIGH | **accept** | The whole "inner manager" construct is removed from Tier 1. There is no implement package. The Claude callee is a plain `claude -p` **whose capability boundary is set mechanically** — `--permission-mode plan` plus a write-tool denylist — which is criterion 4. The finding's own correction (enforce per phase via flags) is what Tier 1 does, minus the phases. |
| **F5-3** — the state machine collapses Gate 0, Gate 1 and Gate 2 into one `WAIT_OWNER_GATE` node | MEDIUM | **defer (Tier 3)** | Tier 1 has no state machine and no gate node. What Tier 1 owes instead is proof that the *canonical* gates still fire — criterion 9, covered by the `gates_still_trigger` dry-run row. The parameterised-gate correction is carried forward to Tier 3. |
| **F5-4** — resume validation omits process liveness and drive-letter case, the two recorded Windows session hazards | MEDIUM | **defer (Tier 3)** | Tier 1 never resumes a session (criterion 6), so neither hazard is reachable. Carried to Tier 3, where resume returns. The related liveness concern that *is* live in Tier 1 — terminating only the owned child — is criterion 22 and is covered by the `cancellation` dry-run row. |
| **F5-5** — no cross-task mutual exclusion; two concurrent tasks can claim the same checkout as writer | MEDIUM | **defer (heavier mechanism)** | A consult is not a writer: it creates no checkout, writes nothing to the tree outside its own record, and touches no database, so a checkout-scoped lock would be dead weight. **Corrected after council (CR-8):** the original reasoning claimed "no shared state", which criterion 21 had since made false — the session log is one shared append. Log lines are now encoded once and written with a single `os.write` to an `O_APPEND` handle, so two concurrent consults cannot interleave a line. The real lock is carried forward to the tier where writers reappear. |
| **F5-6** — `VERIFY` is not bound to the canonical test derivation, so "independent verification" is untestable | MEDIUM | **accept in principle, defer the mechanism (Tier 3)** | Tier 1 has no `VERIFY` state, but the finding's *principle* is criterion 5: a consult result is advisory until the caller verifies it, and the protocol document names verification as the caller's job. The deterministic `QUALITY_GATE.md` union binding is a Tier 3 obligation and is carried forward with C-8. |
| **F5-7** — adapter shell and encoding unpinned; PowerShell 5.1 corrupts UTF-8 to native executables | LOW | **accept, stronger remedy than proposed** | The finding proposed pinning to `pwsh` 7 with explicit UTF-8. Tier 1 goes further and **removes the shell**: the adapter is Python and spawns from an argument vector with `shell=False`, so no quoting or pipeline-encoding layer exists to corrupt anything. Encoding is pinned explicitly at the pipe (`encoding="utf-8"`). This is criterion 24, and it also removes F5-7's whole failure class from the Codex→Claude direction. |
| **F5-8** — `.agents/skills/` discovery is unverified; no `.agents/` directory exists | LOW | **accept** | Confirmed and superseded by C-3 and HR-10: the directory still does not exist, and `$CODEX_HOME/skills` is the real (machine-local, empty) root. Tier 1 therefore places **no** file in either location. The Codex-side trigger is `AGENTS.md` → a tracked protocol document → a tracked script, all three PR-reviewable. |

### Claude Opus 5 pre-council pass (C-1 – C-12)

| Finding | Severity | Disposition | Action |
|---|---|---|---|
| **C-1** — the mechanism cannot be dry-run on this host; Gate 0 needs a host-readiness probe first | BLOCKER | **accept, and executed** | The probe was run before any design work; it is the [Host-readiness re-probe](#host-readiness-re-probe--2026-08-13) section, and it is criterion 13. Its three pass conditions resolve as: configured model **still fails** (HR-2, mitigated by pinning `-m gpt-5.5`); `workspace-write` spawn **still fails** (HR-3, and this is why Tier 3 is not built); `claude -p --json-schema` **passes** (HR-8). The probe also found the condition C-1 did not think to test — `-s read-only` works (HR-4) — which is what makes Tier 1 possible today. |
| **C-2** — in the non-interactive path the sandbox is all-or-nothing, so per-invocation escalation is not available | HIGH | **reject (premise disproven)** | There are three sandbox modes with three measured behaviours, not two: `workspace-write` cannot spawn (HR-3), `read-only` spawns and permits reads (HR-4) while declining unclassifiable commands (HR-5), and `danger-full-access` spawns freely (HR-12). The choice is therefore not "full containment or `--dangerously-bypass-approvals-and-sandbox`". C-2's *demand* is still honoured: [`AUTONOMY.md`](AUTONOMY.md) now states plainly what layer 2 is during a consult in each direction, and does not call it "partial containment". |
| **C-3** — the proposed skill path is the wrong root; a file in `~/.codex/skills/` is machine-local, unreviewable in a PR, and invisible to Gate 2 | HIGH | **accept** | Criterion 15. Tier 1 installs nothing outside the repository: the executed artifact *is* the tracked file. There is no copy, therefore no drift check is needed — the drift class is designed out rather than monitored. |
| **C-4** — the orchestrator is version-skewed, so every finding here has a short shelf life | HIGH | **accept** | Re-probed: all three versions are unchanged (HR-1), so the skew is confirmed open. Criterion 14 requires each consult record to carry the callee CLI version and the model that actually answered, so a future upgrade shows up as a change in the evidence rather than as a silent behavioural shift. Recording versions in a plan document alone was explicitly rejected by this finding, and is not what was done. |
| **C-5** — `$orchestrate` is a prompt convention, not a dispatch primitive, so criterion 1 is unfalsifiable | MEDIUM | **accept, reframed** | Confirmed: no `$`-prefixed dispatch exists, and `$CODEX_HOME/prompts` does not exist either (HR-10). Tier 1 does not claim deterministic dispatch. It makes criterion 1 falsifiable a different way: the consult is **inert until the adapter process actually runs**, and the adapter's own record is the observable. The `no_trigger_no_child` dry-run row asserts exactly that, and it cannot false-pass, because it checks for the absence of a record that the adapter always writes when it runs. |
| **C-6** — the adapter reimplements six controls the Claude CLI already provides natively | MEDIUM | **accept, four of six adopted; two are Tier 3** | Adopted: `--json-schema` for result validation (criterion 7), `--permission-mode`/`--disallowedTools` for the capability boundary (criterion 4), `--max-budget-usd` as a hard cost ceiling (criterion 23), and `--setting-sources`/`--strict-mcp-config`/`--mcp-config` for reproducibility and for the 3.8× cost reduction measured in HR-9. Not adopted: `--session-id` and `--bg`/`claude agents --json`, because Tier 1 is one-shot and stateless — there is no session to name and no background task to poll. Both are carried to Tier 3. |
| **C-7** — `claude --worktree` must be an explicit non-goal or it silently violates DB isolation | MEDIUM | **accept the rule, reject the proposed assertion (premise stale)** | `--worktree` is a named non-goal (criterion 17) and the adapter never passes it. The *proposed evidence* no longer works: `data/database.db` is now untracked and gitignored (HR-11), so `git ls-files -v data/database.db` returns nothing and can never show a `--skip-worktree` flag. The replacement assertion is stronger and matches what Tier 1 actually guarantees — the `no_checkout_no_db` row asserts that a consult creates no directory and opens no database file at all. |
| **C-8** — binding `VERIFY` to `QUALITY_GATE.md` alone still lets a worker produce a locally-green change that fails CI | MEDIUM | **defer (Tier 3)** | Tier 1 produces no `changed_paths`: a consult writes nothing, so neither `Test Inventory Drift` nor the pyright baseline can move because of one. The finding's second half — that the two CI-only gates arguably belong in `QUALITY_GATE.md` for *all* work, not just orchestration — is a real observation about a shared authority file, and is deliberately **not** actioned here: `QUALITY_GATE.md` may not be widened by a Tier 1 packet (D7). Carried to Tier 3 and recorded as a standalone candidate. |
| **C-9** — `AUTONOMY.md` and `AGENTS.md` misstate the live Codex configuration | MEDIUM | **accept, widened to three files** | Re-verified against the live `~/.codex/config.toml` on 2026-08-13: `approval_policy = "on-request"` (both docs said `"never"`), and `[windows] sandbox = "elevated"` is set while `codex features list` reports both `elevated_windows_sandbox` and `experimental_windows_sandbox` as `removed`. **Extended after council (CR-5):** `PARALLEL_WORKFLOW.md` carried identically-shaped drift — it still asserted `data/database.db` is tracked, which HR-11 measured false — so it is corrected here too. All three corrections are factual restatements; no new policy is introduced under cover of a drift fix. |
| **C-10** — the architecture puts the fragile half at the root of the tree; the owner should choose the direction explicitly | STRATEGIC | **accept; resolved by the owner, and the re-probe agrees** | The owner chose symmetric consults (D2), which is neither pure Option A nor pure Option B: **neither** model is the root, because a consult has no root — it has a caller and a callee, and either side may be either. Option C (MCP) was measured rather than assumed: it is real on this host (HR-6) but not callable unattended (HR-7), so it is deferred with its evidence instead of being adopted or dismissed. The priced comparison the finding asked for is preserved in the tier table. |
| **C-11** — no cost or latency budget is quantified anywhere | LOW | **accept** | Answered with measurements rather than defaults: HR-9 gives $0.3055/50,271 tokens repo-loaded versus $0.0800/39,184 tokens suppressed, both around 5 s. The adapter defaults to the cheap profile, passes `--max-budget-usd`, and records duration and cost in every consult record, so the next cap is set from accumulated data rather than intuition. |
| **C-12** — the plan does not say what happens to `docs/MASTER_HANDOVER.md` | LOW | **accept** | Consult records are gitignored under `artifacts/consult/` (criterion 12). Nothing in this mechanism writes `MASTER_HANDOVER.md`, and the protocol document says so explicitly. This packet does not edit it either; its result is recorded in the worktree-local handover for the integration session. |

### Fable 5 second pass (F5B-1 – F5B-10)

| Finding | Severity | Disposition | Action |
|---|---|---|---|
| **F5B-1** — the plan solves delegation; the owner described conversation. There is no channel for the worker to ask a question | HIGH | **accept, scaled to one-shot** | `status: needs_input` with a `questions[]` array is in the result contract and is criterion 19. It is a **terminal** status, not a loop: the adapter returns it to the caller and stops. Whether to answer is the caller's decision, expressed as a second consult, so the round-control guarantee is preserved without a round counter. The `needs_input` dry-run row asserts the status survives validation and that no second child is spawned. |
| **F5B-2** — there is no lightweight consult primitive; the state machine is the only door | HIGH | **accept — this finding is the packet** | Tier 1 *is* the consult primitive: one bounded question, one bounded answer, no work packages, no worktree, no `state.json`, one record. This is the finding that reorganised the whole plan, and it is why the heavy tier is deferred rather than built first. |
| **F5B-3** — neither CLI's native multi-agent surface was surveyed before proposing a hand-rolled one (G3) | HIGH | **accept the survey, defer the G3 build** | Surveyed at current versions. Codex: `multi_agent` is `stable true`, `enable_fanout` and `multi_agent_v2` are `under development`, `hooks` is `stable true`. Claude Code 2.1.220: eleven `.claude/agents/` charters, `--agents`, `--agent`, `--bg`, `claude agents --json`, and the existing `/council-plan`. Verdict per capability is in the tier table. The conclusion is that **no meta-spawner should be built** — each vendor's native spawner stays authoritative and the consult is the only cross-vendor glue. The G3 pains that remain (council weight on medium tasks, selection friction) are owner decisions about canon and are explicitly out of Tier 1 scope under D7. |
| **F5B-4** — MCP likely dissolves the two hardest host blockers and should be evaluated first | HIGH | **accept the evaluation; the architectural claim is confirmed; adoption deferred** | Probed directly rather than reasoned about. **The claim is true on this host:** an MCP server registered in Codex is spawned by the host process and completed `initialize` and `tools/list` under `-s workspace-write`, in the same run where the shell tool could not spawn anything (HR-6). The blocker is one layer up: `tools/call` requires an approver and auto-declines in `codex exec` (HR-7). So MCP is the right Tier 2/3 transport and the wrong Tier 1 transport — a long-lived server plus a new tool surface to secure would be strictly more machinery than a one-shot process, for a call that cannot complete unattended anyway. Recorded with its evidence, not dismissed. |
| **F5B-5** — the PR is already a working cross-model message bus; the review loop may need almost no new infrastructure | MEDIUM | **accept as Tier 2, defer** | Named as Tier 2 in the tier table with its near-zero build cost recorded. Not built here: this packet's authorisation is Tier 1 only, and a PR-bus convention that instructs either CLI to push, comment, or merge is a much larger authority question than a read-only consult. |
| **F5B-6** — cross-model output is untrusted input; no pass set the trust boundary | MEDIUM | **accept** | Criterion 20. The adapter validates against a closed schema before the caller sees anything, executes nothing from a result, and size-caps free text with the raw stream on disk instead of in the caller's context. **Corrected after council (CR-15):** calling that "enforced in three places" overstated it — those measures protect the *adapter*, and the adapter was never the target. The caller is a model, and reading `summary` is how it works. Two amplifiers the reviewer named are now closed or stated: `artifacts/**` is in the read denylist, so a result cannot be laundered back in through a later request's `artifact_paths`; and `questions[]` is called out in [CONSULT_PROTOCOL.md](CONSULT_PROTOCOL.md) as the channel that exists to put the callee's words into the caller's next turn. The residual is stated in the only form that helps a model reading a result: **a consult result may never be cited to relax a test, skip a reviewer, satisfy a gate, or widen a scope.** |
| **F5B-7** — removing the mediator removes the owner's observation point | MEDIUM | **accept, scaled to the consult tier** | Criterion 21. Every consult appends one line to `artifacts/consult/consult-log.jsonl` — timestamp, direction, callee model, status, duration, cost, record path — which is tail-able while a consult runs. The finding's full `dialogue.jsonl` is a Tier 3 obligation, since Tier 1 has no multi-turn dialogue to stream. |
| **F5B-8** — two writer-capable CLIs, one checkout: the one-writer rule must be stated cross-vendor | MEDIUM | **defer (Tier 3), property asserted now** | Tier 1 has no writer on either side: the Codex callee runs `-s read-only` and the Claude callee runs `--permission-mode plan` with writes denied. There is no live implement package to exclude the orchestrator from. The `no_checkout_no_db` row asserts the property directly. Carried to Tier 3 with the cross-vendor wording the finding asks for. |
| **F5B-9** — Section 0 must absorb the clarified goal before Gate 0 can mean anything | HIGH | **accept — this finding is why Section 0 was redrafted** | Section 0 v2 records G1–G3 verbatim and is organised around them; the tier split is criterion 1 plus the routing rules in the protocol document; the question channel is criterion 19. G3 is scoped **in** as the F5B-3 survey plus the cross-model-specialist half, and the two process-canon pains are scoped **out** explicitly under D7 rather than resolved silently — which is exactly the failure mode this finding predicted. |
| **F5B-10** — per-invocation context tax and model tier are unpriced | LOW | **accept** | Priced in HR-9 and acted on: the adapter's default profile suppresses settings and MCP servers and uses a fast callee model, which is the measured 3.8× saving, and the caller opts into the repo-loaded profile when the question genuinely needs repository context. Model tier is a per-consult argument, recorded in the record, not a fixed choice. |

### Where deferred findings are carried

F5-3, F5-4, F5-5, F5-6, C-8, F5B-5 and F5B-8 are deferred to a tier that was not built.
Each is listed in
[Deferred mechanisms — planned, not implemented](#deferred-mechanisms--planned-not-implemented)
with the obligation it imposes on that mechanism, so a future reader inherits the finding
rather than the summary of it. C-8's second half — the proposal to name
`Test Inventory Drift` and the pyright baseline gate inside `QUALITY_GATE.md` for all
work — is recorded there as a standalone candidate that needs its own owner decision,
because widening a shared authority file is out of scope for this packet under D7.

---

## Plan v1 — Tier 1 consult *(2026-08-13, the draft the council reviewed)*

### Goal

Let either CLI ask the other model one bounded, read-only question and get back a
schema-validated answer, without the owner relaying anything, and without any change to
the planning gates, the `manager` role, the schema, the app, or product behavior.

### Scope

**In**

- One adapter, `scripts/consult/consult.py`, used identically in both directions.
- Two JSON Schema contracts — request and result — shared by both directions.
- Mechanical read-only enforcement of the callee.
- Bounded timeout, bounded output, owned-child termination, typed terminal outcomes.
- Gitignored per-consult records and one appended session log line per consult.
- Tracked triggers: `.claude/commands/consult.md` on the Claude side, and
  `AGENTS.md` → `docs/ai_workflow/CONSULT_PROTOCOL.md` on the Codex side.
- Factual corrections to `AUTONOMY.md` and `AGENTS.md` (C-9), and an `INDEX.md` entry.
- A fixture-driven dry-run matrix in `tests/test_consult_adapter.py`, plus one live
  smoke per direction recorded in this document.

**Out**

- Everything in the non-goals list of Section 0 v2, and in particular: the
  `$orchestrate` state machine, any write-capable consult, session resume, an MCP
  surface, checkout creation, and any change to `QUALITY_GATE.md` routing.

### Artifacts

| Path | Change | Notes |
|---|---|---|
| `scripts/consult/consult.py` | new | The adapter. Argument-vector spawn, no shell. Subcommands `ask-codex`, `ask-claude`, `validate`. |
| `scripts/consult/request.schema.json` | new | Request contract: objective, question, artifact paths, constraints. |
| `scripts/consult/result.schema.json` | new | Result contract: `status`, `summary`, `findings[]`, `questions[]`, `artifacts_read[]`. Closed (`additionalProperties: false`). |
| `docs/ai_workflow/CONSULT_PROTOCOL.md` | new | The protocol both models read: triggers, contracts, limits, trust boundary, what a consult may not do. |
| `.claude/commands/consult.md` | new | Claude-side trigger. |
| `AGENTS.md` | modify | Codex-side trigger pointer; C-9 config correction. |
| `docs/ai_workflow/AUTONOMY.md` | modify | C-9 config correction; containment note for consults in both directions. |
| `docs/ai_workflow/INDEX.md` | modify | Index the protocol; retire the "not implemented" wording on this plan's entry. |
| `docs/ai_workflow/CROSS_MODEL_ORCHESTRATION_PLAN.md` | modify | This document. |
| `tests/test_consult_adapter.py` | new | The dry-run matrix, driven by fixture CLIs. |
| `tests/fixtures/consult/` | new | Fake `claude` / `codex` executables that produce each modelled outcome deterministically. |

**Effort**: M · **Owner**: autonomous Opus session 8 · **Depends on**: nothing

### Sequence

1. Write the two schemas, then the protocol document, so the behavioural contract is
   reviewable before the code exists.
2. Write the adapter against the schemas.
3. Write the fixture CLIs and the dry-run matrix; require every row to fail for its
   stated reason before it passes.
4. Run one live smoke per direction; record the evidence here.
5. Land the trigger surfaces and the C-9 corrections.
6. Reviews, then PR.

### Dry-run matrix

| Row | Required observation |
|---|---|
| `claude_to_codex_success` | One argument-vector spawn; schema-valid result; record written with callee version and model. |
| `codex_to_claude_success` | Same, mirrored. |
| `unavailable_cli` | Missing executable produces `status: error`, `kind: cli_unavailable`; no traceback; no retry. |
| `timeout` | Child exceeding the deadline is terminated; `status: timeout`; only the owned PID is signalled. |
| `malformed_result` | Non-JSON and schema-violating output both produce `status: error`, `kind: malformed_result`; the raw output is preserved on disk. |
| `needs_input` | `status: needs_input` with `questions[]` survives validation and spawns no second child. |
| `cancellation` | A cancel request terminates only the owned child, gracefully first. |
| `path_handoff` | The request carries artifact **paths**; the child's argv contains the request-file path and not the file contents. |
| `no_trigger_no_child` | Importing the module and running `validate` starts no child process and writes no record. |
| `embedded_instruction` | A result whose free text contains an imperative produces byte-identical adapter behaviour to the benign case. |
| `no_checkout_no_db` | A consult creates no directory outside `artifacts/`, and opens no `.db` file. |
| `gates_still_trigger` | `QUALITY_GATE.md` plan-stage routing and the council command are unchanged by this packet's diff. |
| `no_secret_leak` | No environment variable resembling a credential appears in any record, log line, or argv. |

### Expected gates

- pytest: `tests/test_consult_adapter.py`, plus `tests/test_agent_workflow_contracts.py`
  because `.claude/**` and `docs/ai_workflow/**` change; full pytest before the PR.
- e2e: none — no template, JS, CSS, route, or schema surface is touched.
- other: `Test Inventory Drift` regeneration for the new test module; Pyright baseline
  diff for the new Python module; `git diff --check`.
- reviewers: `code-reviewer` (AI workflow / agent config row), plus
  `architecture-reviewer` for the process-boundary question and a security pass, because
  the packet spawns child processes and handles cross-model output.

---

## Council review — 2026-08-13

### Agent provenance

| Role | Agent | Run evidence | Notes |
|---|---|---|---|
| `product-manager` — Plan v1 | **not used** | — | Section 0 v2, the response matrix, Plan v1 and Plan v2 were written by the primary autonomous Opus session. See the evidence gap and the decision below it. |
| `product-manager` — response matrix + Plan v2 | **not used** | — | Same. |
| `architecture-reviewer` | real subagent, completed | 47 tool calls, 161,673 tokens, 527 s, verdict `REVISE` | Step 2 reviewer. |
| `test-strategist` | real subagent, completed | 25 tool calls, 156,533 tokens, 483 s, verdict `REVISE` | Step 2 reviewer. |
| `product-risk-reviewer` | real subagent, completed | 18 tool calls, 92,677 tokens, 315 s, verdict `REVISE` | Step 2 reviewer. |

**Same product-manager resumed for the matrix + Plan v2?** `no` — no `product-manager`
agent was used at any step.

**Reviewer-ID note.** The three reviewers ran as real subagents and each returned a real
agent ID. Those IDs are session-internal harness identifiers that the runtime marks as not
to be reproduced outside the session, so this table records each run's measurable
evidence — tool calls, tokens, duration, verdict — instead. **No ID was invented**, no
placeholder was passed off as an ID, and no completed council work was rerun to
manufacture continuity. Each reviewer's output is pasted verbatim below.

**Evidence gap:**

> `product-manager` did not author this artifact, and the reason is a path, not an
> incapacity. `.claude/hooks/guard-planning-write.ps1:4` permits only
> `docs/<feature>/PLANNING.md`; this artifact is
> `docs/ai_workflow/CROSS_MODEL_ORCHESTRATION_PLAN.md`, which that pattern rejects, so the
> write would have been blocked rather than performed. The primary session therefore
> authored Section 0 v2, the response matrix, Plan v1 and Plan v2 directly — work that
> [AUTONOMY.md](AUTONOMY.md#workflow-roles) reserves for `product-manager`.
>
> The `architecture-reviewer` was right to push on this, and the honest framing is a
> **decision, not an inevitability**: this document already carried three pre-council
> reviews and a superseded brief at its current path, and relocating that history to
> `docs/cross_model_consult/PLANNING.md` mid-council would have broken every inbound link
> and every line citation the three prior reviews depend on. The bypass was accepted for
> this artifact only.
>
> It also surfaced a pre-existing contradiction that this packet is **not** fixing:
> [`council-plan.md`](../../.claude/commands/council-plan.md) step 1 says Plan v1 goes to
> `docs/<feature>/PLANNING.md` "or wherever the workstream's planning doc lives", while
> `guard-planning-write.ps1:4` honours only the first half of that sentence. The guard is
> deliberately left untouched here — amending an enforcement hook to fit the packet that
> tripped it is exactly backwards. It is recorded as an open item for the owner.

### Reviewer findings

*Each reviewer's output is pasted verbatim below, unsummarised, exactly as returned.*

> **One mechanical note on two of the three.** The harness neutralises control-tag-shaped
> text in subagent output, so a few angle brackets appear below as `&lt;` / `&gt;` or as
> `&lt;\`. That is the transport, not the reviewer's words, and nothing else was altered.

#### architecture-reviewer (verdict `REVISE`)

Read cold. All citations are from the worktree `D:\development\Hypertrophy-Toolbox-v3-main-cross-model-tier1`. Note: `scripts/consult/consult.py` and `result.schema.json` were edited *while I read them* — a path denylist, `enforce_result_bounds()`, and a strict-mode result schema all appeared mid-review. Two findings I had drafted against the earlier state are withdrawn; what follows is verified against the files as they stand now.

---

## Where the plan is sound (stated plainly, not padded)

**Module boundary: correct, and `scripts/consult/` is the right home.** `scripts/consult/consult.py` imports only the stdlib. Nothing under `routes/` or `utils/` imports it; it imports nothing from them; it never opens a database and `DatabaseHandler` never enters the picture. The `routes/ → utils/ → utils/database.py` chain is not touched — the packet sits entirely outside it, which is what a developer-tooling adapter should do. `scripts/` is the established home for repo tooling (49 files plus the `scripts/css_audit/` package). Two specific confirmations: the css-audit tool-registry contract iterates `scripts/css_audit` only (`tests/test_css_theme_dark_p3_audit_contracts.py:700,744`), so `scripts/consult/` does not red it; and `pyrightconfig.json:19` sets `extraPaths: ["scripts"]` with no `scripts` exclusion, so the new module is type-checked and the pyright-baseline gate applies exactly as the plan says. **No import or authority cycle exists** — the AI-workflow layer reads application files as *data* (artifact paths), never as imports.

**Authority boundaries: not silently rewritten.** `CONSULT_PROTOCOL.md:199-213` explicitly disclaims gate, reviewer, and authority status, and :209-213 states that `manager` cannot invoke the adapter (`manager.md:5` disallows `Bash, PowerShell`) and that granting it would be a separate owner decision. `CONSULT_PROTOCOL.md:223-226` states the `.claude/settings.json` consequence — `Bash(.venv/Scripts/python.exe:*)` at `.claude/settings.json:4` already makes the adapter promptless — and declines to change the file because `PARALLEL_WORKFLOW.md:88` names it never-claimed. That is the correct handling of shared state, and it is better than most packets manage.

**Calculation/product-impact claim: verified true.** No path in the artifact table (plan:1206-1218) reaches `routes/`, `utils/`, `templates/`, `static/`, `app.py`, or any schema helper. `.gitignore:57` (`/artifacts/`) already covers the record root, so no `.gitignore` edit is needed. `docs/MASTER_HANDOVER.md` is correctly left alone (plan:1145).

---

## Findings

**`tests/test_agent_workflow_contracts.py:92,158-162` vs `docs/ai_workflow/CONSULT_PROTOCOL.md:1,54,207,282` — the packet's own vocabulary is banned by a committed contract test, and the test is red on disk right now.**
`RETIRED_NUMBERING = re.compile(r"\bTier \d|\bAppendix A\d")` is parametrized over `[p for p in SURFACE if not p.name.endswith("_PLAN.md")]`. `CONSULT_PROTOCOL.md` is in `docs/ai_workflow/` and does not end in `_PLAN.md`, so `test_surface_does_not_use_the_retired_tier_numbering[docs/ai_workflow/CONSULT_PROTOCOL.md]` fails today on four lines, starting with the H1 `# Cross-Model Consult Protocol (Tier 1)`. The same trap is armed for the still-unwritten `.claude/commands/consult.md` and for whatever "Tier 1" text the packet adds to `INDEX.md:49-51` and `AUTONOMY.md`. The test's own docstring is explicit that the exemption exists for *proposal* documents only — ":23-26": *"A proposal document owns whatever internal numbering it defines in its own text (`CROSS_MODEL_ORCHESTRATION_PLAN.md` builds in Tier 1/2/3). What an authority document may not do is import numbering from a file that does not exist."* `CONSULT_PROTOCOL.md:4` declares itself *"canonical for the consult mechanism"* — an authority document by its own words. The plan lists this exact test in its Expected gates (plan:1253-1254) without noticing.
  Risk: full pytest is red the moment the packet lands, and the tempting repair (adding `CONSULT_PROTOCOL.md` to the `_PLAN.md` exemption, or widening the regex) weakens an existing guarantee that the packet has no authorisation to touch.
  Fix: rename the tier vocabulary in every non-`_PLAN.md` file the packet writes — the regex is case-sensitive, so lowercase "tier 1" or wording like "the consult tier" / "the orchestrate tier" passes without editing the contract.

**`docs/test_inventory/TEST_INVENTORY.md:70` vs `tests/test_agent_workflow_contracts.py:80-86` and plan:1256 — the inventory delta is larger and differently located than the plan says.**
That file is pinned at 77 nodes. `SURFACE` is a filesystem glob, so each new markdown file in `.claude/commands/` or `docs/ai_workflow/` adds one node to *each* of the two parametrized surface tests. `CONSULT_PROTOCOL.md` already moves it 77 → 79; `.claude/commands/consult.md` will move it to 81 (arithmetic reconciled: 32 surface files × 2 tests − 1 `_PLAN.md` exemption + 14 fixed nodes = 77). The plan scopes regeneration to "the new test module". Separately, `test_every_surface_file_is_tracked_by_git:206` reds the suite locally for any surface file present-but-unstaged.
  Risk: `Test Inventory Drift` fails on the PR, or someone regenerates against a partly-staged tree and bakes a wrong per-file count in.
  Fix: state in the plan that `tests/test_agent_workflow_contracts.py` moves 77 → 81 and that both new markdown files must be `git add`ed before the inventory is regenerated.

**plan:1135 and plan:1142 — the response matrix asserts, in the past tense, edits that have not been made.**
C-2's disposition reads *"`AUTONOMY.md` now states plainly what layer 2 is during a consult in each direction"*; `AUTONOMY.md:25` is unmodified and contains no consult note. C-9's reads *"Both files are corrected in this packet"*; `AUTONOMY.md:25` and `AGENTS.md:9` both still say `approval_policy = "never"` against the live `"on-request"`. The F5-1 **reject** at :1121 leans on the AUTONOMY.md statement existing.
  Risk: the response matrix is the Gate 1 evidence artifact. Past-tense claims for undone work are the false-green class this repo has already hardened against; an owner reading :1135 has no way to tell the sentence is a plan, not a fact.
  Fix: put every unmade edit in the future tense, or make the edits before the council closes — do not leave the matrix mixing both.

**plan:1279-1291 vs `.claude/hooks/guard-planning-write.ps1:4` — the evidence gap's *fact* holds; its *inference* does not, and it converts a path choice into a self-granted author exception.**
I verified the guard myself: `'(?i)(^|[\\/])docs[\\/][^\\/]+[\\/]PLANNING\.md$'` with `exit 2` on any non-match, so `docs/ai_workflow/CROSS_MODEL_ORCHESTRATION_PLAN.md` would indeed have been blocked. But the gap is written as though `product-manager` is structurally incapable of authoring a council document; it is incapable of authoring *this path*. `PLAN_REVIEW_TEMPLATE.md:3` directs the council artifact to `docs/&lt;feature&gt;/PLANNING.md`, every active plan in `INDEX.md:22-32` lives there, and `council-plan.md:30` even says "or wherever the workstream's planning doc lives" — wording the guard does not honour, which is a pre-existing contradiction this packet surfaced but did not name. Net effect: the primary session authored Section 0, Plan v1, and the response matrix, which `AUTONOMY.md:48-54`, `manager.md:16-22`, and `product-manager.md:22-26` reserve for `product-manager`.
  Risk: a council whose author role was bypassed by artifact placement, recorded as an inevitability rather than as a decision — and a future packet can cite this precedent to bypass it again.
  Fix: either place the council artifact at `docs/cross_model_consult/PLANNING.md` so `product-manager` can own it, or record the bypass as an explicit owner decision naming `council-plan.md:30` vs `guard-planning-write.ps1:4` as the underlying contradiction; do not amend the guard inside this packet.

**HR-11 (plan:285) vs `docs/ai_workflow/PARALLEL_WORKFLOW.md:71,82` — the packet fixes two of the three drifted authority docs it measured.**
HR-11 measured `data/database.db` untracked and ignored (`.gitignore:29 *.db`, whitelists at :34-35 exclude it), and `scripts/new-worktree.ps1:101-104` already codes for it in a comment: *"once Packet A untracked data/database.db, this line aborted the script"*. Yet `PARALLEL_WORKFLOW.md:71` still asserts *"`data/database.db` is currently tracked in this repo"* and :82 still calls untracking it out of scope. C-9 corrects `AUTONOMY.md`/`AGENTS.md` for identically-shaped drift, so the omission is inconsistent — and `AUTONOMY.md:67` defers to `PARALLEL_WORKFLOW.md` as canonical for exactly this rule.
  Risk: the packet's own probe leaves the authority doc for DB isolation stating the opposite of measured reality, and the C-7 `reject` cites that measurement as its basis.
  Fix: add the two-line `PARALLEL_WORKFLOW.md:71,82` factual correction to the C-9 scope, or record explicitly why the third file is excluded.

**plan:23, :8-9, :313-314, :1112, :1166 — three internal anchors and one whole promised section do not exist.**
`#plan-v2--tier-1-only` is linked twice; the actual heading (plan:1175) is "Plan v1 — Tier 1 consult". `#tier-2-and-tier-3--planned-not-implemented` is linked four times and there is no such section (`## `/`### ` heading census confirms). plan:1164-1171 states that F5-3, F5-4, F5-5, F5-6, C-8, F5B-5 and F5B-8 *"are listed"* there *"so a future reader inherits the finding rather than the summary of it"* — they are listed nowhere.
  Risk: seven of the twenty-nine dispositions are `defer` justified by a carry-forward that does not exist, so the deferral half of the response matrix is unbacked at Gate 1.
  Fix: write the "Tier 2 and Tier 3 — planned, not implemented" section with the seven carried obligations, and rename the anchor or the heading so they match.

**plan:136 (criterion 14) and `CONSULT_PROTOCOL.md:261-262` vs the adapter's `run_consult()` — the record carries the model *requested*, not the model that answered.**
`callee` is seeded with the `--model` argument and only `cli_version` is subsequently measured (`read_cli_version()`); `extract_claude_result()` reads `total_cost_usd` off the envelope and nothing else, and `extract_codex_result()` reads only the last-message payload. Criterion 14 says "the model actually used"; the protocol doc repeats it as "the model that actually answered". Given HR-2 (plan:276) — the configured Codex model 400s and must be pinned with `-m` — catching a silent model substitution is the entire purpose of the criterion, and echoing the request cannot do it.
  Risk: C-4 was dispositioned `accept` on the strength of this criterion; the evidence it produces cannot detect the failure it was written for.
  Fix: read the answering model from the Claude JSON envelope (and record `null` plus a note for the Codex side, as is already done for cost), or restate criterion 14 as "the model requested".

**plan:1125 (F5-5 `defer`) — the "two concurrent consults cannot conflict" premise is no longer accurate.**
The defer reasons there is no shared state, so a lock would be dead weight. Criterion 21 (plan:154-156) was added afterwards and introduces exactly one piece of shared mutable state: the append to `artifacts/consult/consult-log.jsonl` in `write_record()`. A buffered text-mode append is not a guaranteed-atomic write, so two concurrent consults in one checkout can interleave log lines.
  Risk: low impact (evidence log only), but the reasoning that retired the lock is now stale, and the log is the owner's live observation point per F5B-7.
  Fix: restate the defer as "the only shared state is one append-only log line", and either open the log with a single `os.write` of the encoded bytes or accept the interleave explicitly.

**`CONSULT_PROTOCOL.md:268-272` vs `resolve_executable()` / `run_child()` — the fixture-CLI seam is single-token, so the "reproducible on Windows and Linux alike" promise needs a decision before `tests/fixtures/consult/` is written.**
`CONSULT_&lt;VENDOR&gt;_CLI` returns one string, which becomes `argv[0]` of a `shell=False` spawn. A Python fixture cannot be expressed (`python fake_claude.py` is two tokens), so the fixtures must be directly executable — a `.cmd` on Windows and a shebang script with the exec bit on Linux, i.e. two families of the same logic.
  Risk: the dry-run matrix is the packet's entire evidence base; divergent fixtures make a green Linux CI row and a green Windows row prove different things.
  Fix: accept an argv-prefix override (a JSON list, or a companion `CONSULT_&lt;VENDOR&gt;_CLI_ARGS`) so one Python fixture serves both platforms.

**plan:125-127 (criterion 10) vs plan:1247 — the criterion overstates what the adapter does.**
Criterion 10 says a consult *"neither writes to the checkout"*; the adapter writes `artifacts/consult/&lt;id&gt;/{request,prompt,raw.stdout,raw.stderr,record}` inside the checkout. The `no_checkout_no_db` dry-run row has the accurate form ("creates no directory outside `artifacts/`").
  Risk: a criterion that is literally false is either unfalsifiable or fails its own test row.
  Fix: align criterion 10's wording to the dry-run row.

**plan:3-4 vs plan:1272-1274, :1297, :1313 vs `scripts/consult/` on disk — three mutually inconsistent gate states in one artifact.**
The header says "Gate 1 pre-approved". The sign-off checklist leaves "Owner approved Plan v2 (Gate 1)" unchecked, the reviewer IDs are `&lt;pending&gt;`, and the findings block is still `&lt;!-- COUNCIL_FINDINGS_PLACEHOLDER --&gt;`. Meanwhile the adapter, both schemas, and the protocol document are written. `QUALITY_GATE.md:14` routes new-workflow work to Gate 0 + Gate 1 *before* implementation.
  Risk: not mine to relitigate the owner's pre-approval, but the artifact cannot be all three at once, and the response matrix's past tense (finding 3) compounds it.
  Fix: state in one place which is true — e.g. "Gate 1 pre-approved for a Tier-1-only scope; council in progress; implementation started under that pre-approval" — and make the sign-off checkboxes match.

---

### On the `reject`/`defer` premises you asked me to test

The three `reject` rows hold on the evidence given. **F5-1** (plan:1121): `network_access = false` is nested under `[sandbox_workspace_write]` per `AGENTS.md:9`, so it genuinely does not bind `-s read-only`, and HR-4 measured the API reached under that mode — the reject is sound, though it depends on an `AUTONOMY.md` statement that has not been written (finding 3). **C-2** (:1135): three measured sandbox behaviours (HR-3/HR-4/HR-12) do disprove the binary framing; well evidenced. **C-7** (:1140): `.gitignore:29` plus the whitelists at :34-35 plus `scripts/new-worktree.ps1:101-109` all corroborate HR-11, so `git ls-files -v data/database.db` genuinely cannot produce the proposed assertion — but see finding 5 on the doc it leaves behind. Among the `defer` rows, only **F5-5** rests on a premise I can show is now wrong (finding 8); **C-8**'s defer is correctly scoped to the *mechanism* rather than the packet, and the packet's own inventory/pyright exposure is separately acknowledged at plan:1256-1257.

Nothing in the packet changes default `manager` activation, `QUALITY_GATE.md` routing, the DB schema, application code, or product behavior. Criterion 26 holds.

REVISE

#### test-strategist (verdict `REVISE`)

## Headline

Three things are load-bearing and none of them are in the plan:

1. **The packet will red an existing contract test on contact.** `test_agent_workflow_contracts.py:163` scans every `docs/ai_workflow/*.md` and `.claude/commands/*.md` that does not end in `_PLAN.md` for the regex at `:92`, `r"\bTier \d|\bAppendix A\d"`. The plan's four documentation targets — new `CONSULT_PROTOCOL.md`, new `.claude/commands/consult.md`, edited `AUTONOMY.md`, edited `INDEX.md` — are all in that surface and all four are described in the plan using the exact vocabulary the regex forbids (plan lines 1211–1215).
2. **Five of thirteen dry-run rows cannot fail**, and one (`malformed_result`) asserts a `kind` the code does not produce.
3. **Criterion 4 — the mechanical capability boundary, the packet's central safety claim — has no dry-run row at all**, despite being a pure-function assertion over `build_claude_argv` / `build_codex_argv`.

```
## Required gates
- pytest: tests/test_consult_adapter.py (new), tests/test_agent_workflow_contracts.py,
          then FULL pytest (cascade risk is not local to those two files)
- e2e:    none derivable — no template/JS/CSS/route surface; the required Chromium
          contexts still run on the PR regardless
- other:  python scripts/generate_test_inventory.py (REGENERATE, not just check),
          flake8 blocking select, pyright baseline diff, `git add` before pytest
- reviewers: code-reviewer (QUALITY_GATE.md:34) + architecture-reviewer (voluntary,
          justified: child-process spawn + untrusted cross-model input)

## Existing coverage
- scripts/consult/consult.py — NONE. No test file references it (`rg consult tests` → 0 hits).
- scripts/consult/{request,result}.schema.json — NONE.
- .claude/commands/consult.md (new) — tests/test_agent_workflow_contracts.py:139, :163, :206
  (auto-enrolled by the glob at :80-86; adds 2 nodes)
- docs/ai_workflow/CONSULT_PROTOCOL.md (new) — same three, same enrolment (adds 2 nodes)
- docs/ai_workflow/{AUTONOMY,INDEX,CROSS_MODEL_ORCHESTRATION_PLAN}.md — already in SURFACE;
  CROSS_MODEL_ORCHESTRATION_PLAN.md is exempt from :163 by the `_PLAN.md` filter at :160
- AGENTS.md (root) — NONE. Not in SURFACE (:80-86 takes .claude/{commands,agents,rules},
  docs/ai_workflow, and root CLAUDE.md only). The Codex-side trigger has zero mechanical cover.
- docs/test_inventory/TEST_INVENTORY.json:258-259 pins this file at **77**; it becomes **81**.

## Coverage gaps
(see "Uncovered criteria" below — 11 criteria with no row, plus 5 vacuous rows)

## Conftest / fixture work
- tests/conftest.py — none required. No blueprint, no table, no schema.
- REQUIRED instead: a module-scoped autouse fixture that sets BOTH CONSULT_CLAUDE_CLI and
  CONSULT_CODEX_CLI on every test, or pytest on this Windows host resolves the REAL,
  billable CLIs via shutil.which (consult.py:270).
- tests/fixtures/consult/ is safe as a location: tests/fixtures/make_old_schema_db.py is the
  precedent, and pytest.ini sets no python_files override, so a non-`test_*.py` file is not collected.

## Verdict
Targeted gate insufficient as written — see gate analysis; full pytest is required and
the plan's Expected gates are incomplete.
```

---

## A. Dry-run matrix — falsifiability, row by row

**Rows that cannot fail (vacuous):**

| Row | Why it passes even if the behavior is absent |
|---|---|
| `no_trigger_no_child` | `main()` handles `validate` at `consult.py:697-711` and **returns at :711** — before any `subprocess` call and before the `write_record` at `:743`. There is no code path in the validate branch that could spawn or record. The row therefore asserts a structural property of an `if` block, not criterion 1 (which is about a *model* not invoking the adapter — unfalsifiable in pytest by construction). The response matrix's defence at plan line 1138 ("cannot false-pass") is half-true: it proves the record is a reliable tripwire, not that the trigger is disciplined. |
| `embedded_instruction` | Nothing in the adapter ever reads a result's free text. `finish()` at `:626` passes `payload["status"]` and nothing else. There is no branch that could differ, so "byte-identical behaviour" holds on **any** implementation. "Byte-identical" is also literally false — `consult_id`, `started_at`, `duration_ms`, `child_pid` all differ per run, so the test must normalise, and after normalising it compares `status` + `exit_code`, which the schema enum already fixes. |
| `no_checkout_no_db` | The only `mkdir` is `record_dir.mkdir()` at `:522` under `--record-root`, which the test will point at `tmp_path`. There is no sqlite import, no `.db` literal, and no checkout-creating code anywhere in the file. Nothing could fail. Worse: criterion 10's real DB exposure is that `build_codex_argv` passes `-C &lt;cwd&gt;` at `:439-440`, handing the callee a working directory that *contains* `data/database.db`; what stops a write is the callee's `-s read-only` sandbox (`:436-437`), a **host** property no pytest row can prove. |
| `no_secret_leak` | `ConsultRecord` (`:173-203`) has **no environment field**. "No credential appears in any record" cannot fail because there is no field for one. And the record's `argv_shape` elides the prompt at `:639-640` (`len(token) &gt; 120` → `&lt;N chars&gt;`), so an argv assertion made against the record is doubly blind. |
| `gates_still_trigger` | "unchanged by this packet's diff" is not implementable as a pytest assertion. A hard-coded digest of `QUALITY_GATE.md` is self-referential (whoever changes the file updates the digest); a `git diff` against a base ref is unavailable — the `test-inventory` job checks out without `fetch-depth: 0` (ci.yml:1038-1039), unlike the `test` job (ci.yml:637-640). Either form proves nothing about criterion 9, which is a claim about the *planning process*. |

**Row that contradicts the code:**

- `malformed_result` claims non-JSON **and** schema-violating output "both produce `status: error`, `kind: malformed_result`". Schema violations produce `kind: "schema_violation"` — `validate_or_raise(payload, RESULT_SCHEMA_PATH, "schema_violation")` at `consult.py:622`, surfaced verbatim by `finish(...)` at `:624`. A test written to the row's wording fails; a test written to the code passes but leaves the matrix wrong. Split the row.
- Its second clause, "the raw output is preserved on disk", is true for the JSON/schema paths (`:587-590` runs before extraction) but **false for the output-cap path**: `run_child` raises at `:334-338` *before* `stdout_path.write_bytes`, and `fail()` never sets `raw_stdout_path`. An over-cap response loses its raw stream entirely, directly contradicting criterion 23. There is no row for the cap.

**Row that is unreachable:**

- `cancellation`. The only route to `status: cancelled` is `except KeyboardInterrupt` inside `run_child` at `:330-332`. There is no `--cancel` flag, no signal handler, no cancel subcommand. Reaching it requires monkeypatching `Popen.communicate` — i.e. asserting on the mock. And "gracefully first" is **false on the plan's own host**: `_terminate_owned_child` at `:344` calls `proc.terminate()`, which on Windows is `TerminateProcess` — uncatchable, not graceful. D6's graceful-attempt promise is POSIX-only. Either delete the row and drop `cancelled` from the Tier 1 status set, or implement a real cancel path and record the Windows limitation.

**Rows that are sound but under-specified:**

- `claude_to_codex_success` / `codex_to_claude_success` — "One argument-vector spawn" is **false**: every consult spawns **two** children, because `read_cli_version` runs `[executable, "--version"]` at `:281-286` before `run_child`. Assert 2, or the row is wrong. Also, `read_cli_version` returns `"unknown"` on any failure (`:287-288`), so criterion 14 is satisfiable by the literal string `"unknown"` — the row must assert the fixture's actual version string round-trips.
- `timeout` — the status half is solid (`:324-329` → `fail()` maps `timeout` at `:541`, exit 4 via `:70`). "Only the owned PID is signalled" is unfalsifiable without a sentinel: spawn an unrelated child before the consult and assert it survives. Note also that `terminate()` kills the direct child only — a real `claude` spawns node grandchildren that survive and keep billing. The fixture must spawn a grandchild for this row to mean anything, or the plan must record the orphan as a known limitation.
- `path_handoff` — ambiguous and, on the likely reading, false. `build_prompt` at `:377-382` embeds the **entire request JSON** into the prompt, which is `argv[2]` for claude (`:393-395`) and the trailing positional for codex (`:445`). The request *contents* are in argv. What's true is that artifact-file contents are never inlined — but nothing in the adapter opens an artifact path, so that cannot fail either. Make it real: write a temp artifact containing a unique sentinel, list its path in `artifact_paths`, assert the sentinel appears nowhere in the fixture's received argv, `prompt.txt`, or `record.json`.
- `needs_input` — first half sound. "Spawns no second child" is vacuous (no loop exists) unless the fixture logs each invocation and the test asserts an exact count. Separately: `result.schema.json:8` requires only `["status","summary"]`, and the hand-rolled validator (`consult.py:109-155`) implements no `if/then` or `dependentRequired`, so **`needs_input` with an empty `questions[]` validates fine** — criterion 19's "with `questions[]`" is not enforced anywhere.
- `unavailable_cli` — sound *only if* the override is always set. `resolve_executable` returns the override verbatim without an existence check (`:267-268`); if a test instead clears it to exercise the `shutil.which` branch at `:270`, the row passes for **different reasons on the two platforms** — Linux CI has no `claude` on PATH, this Windows host does, and the adapter would spawn the real CLI inside pytest.

---

## B. Acceptance criteria with no dry-run row

Genuinely uncovered (excluding 2, 6, 8, 16, 18, which are explicitly Tier-3-deferred):

| # | What is uncovered | Cheap, falsifiable replacement |
|---|---|---|
| **3** | The request contract's *enforcement*. `load_request` → `validate_or_raise(..., "bad_request")` at `:658`, and `main()`'s bad-request record branch at `:716-728`, are untested. | Feed a request missing `question`; assert `status: error`, `kind: bad_request`, exit 1, and that a record was still written. |
| **4** | **The whole criterion.** Nothing asserts `--permission-mode plan` (`:404-405`), `--disallowedTools Write,Edit,...` (`:406-407`), or `-s read-only` (`:436-437`) are present. This is the packet's primary safety claim and its most trivially testable one. | Pure-function assertions on `build_claude_argv` / `build_codex_argv`. |
| 5 | The `advisory` field (`:197-200`) is never asserted to reach the record. | One assertion on `record["advisory"]`. |
| 7 | The exit-code map `_EXIT_FOR_STATUS` (`:67-73`) — the machine-readable half of "typed terminal outcome". | Parametrize status → exit code. |
| 11 | Same unfalsifiable class as 1. **State it as untestable in the plan** rather than letting `no_trigger_no_child` imply coverage. | — |
| 12 | Records live under gitignored `artifacts/`. `DEFAULT_RECORD_ROOT` at `:50`; `.gitignore:57` is `/artifacts/`. Verified by me, asserted by nothing. | Assert `DEFAULT_RECORD_ROOT` is under `REPO_ROOT/"artifacts"`, plus a `git check-ignore` probe. |
| 15 | The executed artifact is the tracked file. | Copy the pattern at `test_agent_workflow_contracts.py:206-238`. |
| 17 | `--worktree` never appears. | `assert "--worktree" not in build_claude_argv(...)`. |
| **21** | The session log. `write_record` appends to `consult-log.jsonl` at `:233-234`; nothing asserts it. This is the owner's only live observation point (F5B-7). | Two consults → two parseable JSONL lines with the named fields. |
| 23 | The output cap (`:334-338`), and `--max-budget-usd` (`:408-409`). Note the undisclosed asymmetry: **`build_codex_argv` passes no budget flag at all** (`:431-446`) — the cost ceiling is one-directional. | An oversize fixture response; an argv assertion for the budget flag; a plan line disclosing the asymmetry. |
| **24** | No-shell / argument-vector. Asserted nowhere. | Put `"; rm -rf / &amp; echo $HOME"` in `question` and assert it arrives byte-identical in the fixture's `sys.argv`. |

**Also missing, and I rate it the highest-value test not in the plan:** the hand-rolled validator at `consult.py:109-155` implements only `type`, `required`, `additionalProperties`, `maxItems`, `items`, `minLength`, `maxLength`, `enum`. It **silently ignores** `minItems`, `pattern`, `format`, `if/then`, `dependentRequired`, `oneOf`, `anyOf`, `$ref`, and every numeric keyword. Both schemas currently stay inside that subset — but a future schema edit adding one unsupported keyword is silently unenforced with every gate green. Add a contract test that walks both `.json` files and fails on any keyword `_validate` does not implement. The docstring at `:102-106` claims the tests assert "the validator rejects each construct it claims to enforce"; that is the weaker direction. Assert both.

---

## C. Fixtures vs live runs, and the `CONSULT_&lt;VENDOR&gt;_CLI` seam

**Fixtures are unambiguously right for the gate.** CI's `test` job runs on `ubuntu-latest` (ci.yml:631) where neither CLI exists; live dual-CLI rows would be cost-bearing, nondeterministic, and would skip on the only machine that gates the merge. The plan's split — fixtures in pytest, one live smoke per direction recorded in the document (plan line 1229) — is correct. Keep it.

**The seam is sound in principle, holed in practice.** What's right: it exercises the real `Popen`, real argv, real bytes, real timeout, and it is read from `os.environ` at call time (`:267`) so `monkeypatch.setenv` works with no import-order trap. And `record["executable"]` (`:601`) means a fixture run is distinguishable from a live one in evidence — genuinely good design.

Three holes:

1. **It accepts one token, so it cannot name a cross-platform fixture.** `resolve_executable` returns the override as `argv[0]` with no way to prepend an interpreter. Windows does not honour shebangs, so a `.sh` fixture works on Linux and fails on Windows; a `.cmd` fixture works on Windows and fails on Linux; a bare `.py` depends on a host file association. Pick one at plan time: (a) accept a JSON argv prefix (`CONSULT_&lt;VENDOR&gt;_CLI_ARGV`), (b) generate a per-platform launcher into `tmp_path` from one shared Python body, or (c) have `resolve_executable` return `[sys.executable, path]` when the override ends in `.py`. **(c) is the smallest and keeps one fixture body.** Leaving this to implementation is how you get a matrix that only runs on Windows.
2. **It does not disable the live fallback.** Any test that forgets to set it reaches `shutil.which` at `:270`. Same hazard class as "test hits live DB" (`tests/CLAUDE.md:63`) and it needs the same treatment: autouse env fixture plus an assertion that `record["executable"]` is under the fixture directory.
3. **It gives the test no observation channel.** Without the fixture writing its own `sys.argv` and a filtered `os.environ` to a log file, `path_handoff`, `no_secret_leak`, `embedded_instruction`, `needs_input`'s second half and every spawn-count assertion are unfalsifiable.

**What the fixture must do for a green row to mean the same thing on ubuntu-latest and on this host:**

- Answer `--version` (else `read_cli_version` at `:281-286` returns `"unknown"` and criterion 14 goes vacuous).
- Append `sys.argv` + a filtered `os.environ` to `$CONSULT_FIXTURE_LOG` on **every** invocation, including `--version`.
- Switch behaviour on `CONSULT_FIXTURE_MODE`, not on argv parsing, so one file serves all rows.
- Be **asymmetric**, because the adapter's extraction is: claude reads a `{"structured_output":…, "total_cost_usd":…}` envelope from stdout (`:454-481`); codex must honour `-o &lt;path&gt;` and write the bare result there (`:484-499`).
- Write bytes explicitly via `sys.stdout.buffer` or pin `PYTHONIOENCODING=utf-8` — `run_child` uses byte pipes (no `text=True`), and a `print()` on Windows emits cp1252, so any non-ASCII assertion diverges from Linux.
- Never assert on the child's *whole* environment. `_CREDENTIAL_NAME` at `:81-83` includes `SESSION`, which matches `SESSIONNAME` on Windows and `SESSION_MANAGER`/`XDG_SESSION_ID` on Linux — the filtered set differs by platform by construction. Assert membership of named keys only.
- Keep the `timeout` row at `--timeout 1` with a terminable sleeper; `TERMINATE_GRACE_SECONDS = 5` (`:56`) is added to CI wall-clock on every mis-built variant.

One factual correction the plan should absorb: criterion 25 says the mechanism "never reads, copies, forwards, or persists a credential." `child_environment` at `:243-256` **deliberately forwards** the vendor's own credentials — `ANTHROPIC_*`/`CLAUDE_*` to claude, `OPENAI_*`/`CODEX_*` to codex (`:84-87`) — by inheritance. That is the correct design (each CLI uses its own auth), but "forwards" is the wrong word in the criterion. Say "does not read, decode, copy between vendors, or persist"; the honest testable property is the **cross-vendor** filter, and that one has a real mutation.

---

## D. Expected gates — corrections

Plan lines 1251–1260, checked against `QUALITY_GATE.md`:

**Correct:** the `.claude/**` + `docs/ai_workflow/**` → AI-workflow row (QUALITY_GATE.md:34); `code-reviewer`; naming `Test Inventory Drift` and the pyright baseline; "full pytest before the PR"; `architecture-reviewer` as a justified voluntary addition. No `product-risk-reviewer` is required — the calculation surface is genuinely `none`.

**Missing or wrong:**

1. **`scripts/**` has no row in the change-type table and no rule in the derivation list.** QUALITY_GATE.md:24-35 and :53-64 cover routes, app.py, utils, templates, static/js, scss, static/css, e2e, `.claude`/`CLAUDE.md`/`docs/ai_workflow`, and docs. `scripts/consult/consult.py` — the packet's primary source file — matches none. The union is not literally empty (the new test file self-derives), so the :64 `/verify-suite` fallback does not mechanically fire, but the plan presents "e2e: none" as *derived* when it is in fact a judgement filling an authority gap. Under D7 this packet may not widen `QUALITY_GATE.md`. So: state the gap explicitly, state the judgement ("no template/JS/CSS/route surface, so the feature map at :66-80 yields nothing; the required Chromium contexts run on the PR regardless"), and let the owner see it at Gate 1. Do not present it as a derivation.
2. **The inventory delta is understated.** The plan says regeneration is needed "for the new test module". It is also needed for `tests/test_agent_workflow_contracts.py`, whose node count is a **filesystem glob** (`:80-86`) over the two directories this packet adds files to. `TEST_INVENTORY.json:258-259` pins it at **77**; two new markdown files × two parametrized tests = **81**. `Test Inventory Drift` is blocking (ci.yml:1064-1086) and pins per-file counts.
3. **`test_surface_does_not_use_the_retired_tier_numbering` will red.** Confirmed by grep: `Tier \d` currently appears in `docs/ai_workflow/` **only** in `CROSS_MODEL_ORCHESTRATION_PLAN.md`, which the `_PLAN.md` filter at `:160` exempts. The four new/edited doc targets are not exempt. Decide the vocabulary at plan time — "consult tier", "the heavy tier", or cite the plan document by name. **Do not relax the regex**; that contract exists because a retired numbering scheme resolved to nothing (`test_agent_workflow_contracts.py:11-14`), and weakening a guarantee to land a packet is the case QUALITY_GATE.md:32 explicitly forbids.
4. **Ordering hazard.** `test_every_surface_file_is_tracked_by_git` (`:206-238`) fails until the two new markdown files are `git add`ed. Sequence is write → `git add` → pytest → regenerate inventory. A session that runs pytest first gets a red that looks like a real defect.
5. **flake8 is blocking and unnamed.** ci.yml:110 selects `E9,F63,F7,F82,F811,E711,E712,F401` over the whole tree minus `artifacts`. Both new Python files and the fixture CLI are in scope; `F401` in particular bites test scaffolding.
6. **The pyright requirement needs its action stated.** `pyrightconfig.json` has no `include`, so the project root is in scope and both new files are checked. ci.yml:840-844 fails on **net-new** diagnostics. Either land at zero new, or regenerate the baseline — and that is a reviewed change, not a step.
7. **`AGENTS.md` has no mechanical coverage at all** (it is not in SURFACE). Record that as an accepted gap, or extend SURFACE deliberately — which moves node counts again.
8. **If `consult` joins any agent's `-AllowedCsv`**, `test_allowed_commands_do_not_have_forbidden_steps` (`:244`) then constrains what `.claude/commands/consult.md`'s `## Steps` section may invoke. The plan doesn't say whether it will.

**False alarm, stated so nobody chases it:** `scripts/consult/` does **not** touch the P3 tool-registry contract; `test_css_theme_dark_p3_audit_contracts.py:688` is scoped to `scripts/css_audit/`.

**Known-red awareness:** none of the plan's surfaces touch the two documented exceptions, so they only matter if a full E2E run happens. Note a discrepancy in my own charter: it lists `e2e/nav-dropdown.spec.ts:117` as current, but the canonical file retired it — QUALITY_GATE.md:126, "no longer a known red as of 2026-06-11." The canonical file wins; `program-backup.spec.ts:79` (QUALITY_GATE.md:124) is the only live entry.

---

## E. Mutation discipline — the specific mutations to run

Plan sequence step 3 (line 1227-1228) says "require every row to fail for its stated reason before it passes." That is exactly right and is the discipline that has caught false-greens in this repo twice. Name the mutations, or it will be done by feel:

| Test | Mutation | Must red |
|---|---|---|
| capability boundary (new) | delete `"--permission-mode", "plan"` at `:404-405` | argv assertion |
| capability boundary (new) | delete `"--disallowedTools", …` at `:406-407` | argv assertion |
| capability boundary (new) | change `-s read-only` → `workspace-write` at `:436-437` | codex argv assertion |
| no-shell (new) | change `Popen(argv, …)` at `:308` to `" ".join(argv)` + `shell=True` | metacharacter round-trip |
| `path_handoff` | insert `Path(p).read_text()` for each `artifact_paths` entry into `build_prompt` | sentinel-absent assertion |
| `no_secret_leak` | delete `and not name.upper().startswith(keep_prefixes)` at `:253` | cross-vendor keep assertion |
| `no_secret_leak` | delete the whole `if` at `:253-254` | drop assertion for `GITHUB_TOKEN` |
| `malformed_result` (split) | change `"schema_violation"` at `:622` to `"malformed_result"` | the schema-violation row |
| `needs_input` / spawn count | add a second `run_child` call after `:583` | exact spawn-count assertion (baseline **2**) |
| `no_trigger_no_child` | delete the `return EXIT_SUCCESS` at `:711` so validate falls through to `write_record` at `:743` | record-absence assertion |
| `timeout` | change `_terminate_owned_child` at `:344` to `pass` | status/duration assertion + sentinel survival |
| session log (new) | delete the append at `:233-234` | JSONL line-count assertion |
| output cap (new) | raise `DEFAULT_MAX_OUTPUT_BYTES` at `:54` to 10× | oversize-response assertion |
| exit-code map (new) | swap `EXIT_TIMEOUT`/`EXIT_CANCELLED` at `:70-71` | parametrized exit assertion |
| validator-subset (new) | add `"minItems": 1` to `questions` in `result.schema.json` | keyword-coverage assertion |
| tracked-artifact (new) | point the assertion at a path outside the repo | tracked assertion |

For `embedded_instruction` specifically, the only honest mutation is: make `finish()` at `:626` derive `status` from `payload["summary"]` content instead of `payload["status"]`. If the row cannot be made to red under that mutation, delete the row — a green that no mutation can flip is a liability, not evidence.

---

**Bottom line.** The engineering underneath this is careful — the argument-vector spawn, the callee-cannot-claim-failure schema split (`result.schema.json:12` vs `consult.py:11-14`), the adapter-owned status vocabulary, and recording the resolved executable so a fixture run can never masquerade as live are all genuinely good. The gap is between what the code does and what the matrix claims to prove: five rows are unfalsifiable, one contradicts the code, one is unreachable, the packet's central safety criterion has no row, and the plan does not know it will red an existing contract on contact. All of that is fixable inside Tier 1 scope without touching the adapter's design.

REVISE

#### product-risk-reviewer (verdict `REVISE`)

I read the plan document in full (1,315 lines), the three canonical workflow docs, `AGENTS.md`, the manager charter, `.claude/settings.json`, and `.gitignore`, and I checked the worktree for the artifacts the plan describes.

## Findings

**Section 0 "In scope" (line 185-186) + criterion 3 (108) + criterion 10 (126-127) + dry-run row `path_handoff` (1244) / `no_checkout_no_db` (1247) — the artifact-path handoff is an unbounded read-egress channel, and the plan presents it as containment.**
  Invariant at risk: root `CLAUDE.md` §1 local-first non-goals, as bound to technical containment by `AUTONOMY.md:25` (`network_access = false`) and `AUTONOMY.md:116`.
  Risk: criterion 4's mechanism constrains **writes only**. `--permission-mode plan` and `-s read-only` both permit unrestricted **reads** — HR-4 (line 278) is the proof, the Codex callee spawned pwsh and ran `Get-Content` under `-s read-only`. The same capability reads `data/database.db` (the owner's actual training log), `logs/app.log`, `artifacts/**`, and any `.env`. "Ask Codex why my weekly summary looks wrong" is the natural first consult, and it ships user training data to a third-party API. Criterion 10 asserts a consult "touches no `data/database.db`" — nothing enforces that, and the row that "proves" it runs against fixture CLIs (line 1217-1218) that cannot open a `.db` under any mutation, so it cannot fail for its stated reason and violates the plan's own sequence step 3 (line 1227).
  Fix: validate `artifact_paths` in the adapter against a denylist (`data/**`, `*.db`, `logs/**`, `artifacts/**`, `.env*`, `~/.codex/**`, `~/.claude/**`), restate criterion 10 as a write-side property, and add a real criterion bounding read egress.

**Section 0 "Calculation surface" (172-176) and the whole brief — no statement of what leaves the machine.**
  Invariant at risk: `CLAUDE.md` §1 non-goals; `AUTONOMY.md:116` names layer 2 as the enforcement of that invariant.
  Risk: the words "leaves this machine", "vendor", and "retention" appear nowhere in Section 0. The brief's honesty is entirely about writes, gates, and cost. A consult transmits the request text, everything the callee reads, and the full response to Anthropic and OpenAI, where it is retained under vendor policy the owner does not control. Criterion 12's "records live under gitignored `artifacts/`" reads as containment and is only local containment.
  Fix: add an acceptance criterion stating the egress and retention plainly, and require the same sentence at the top of `CONSULT_PROTOCOL.md`.

**Criterion 25 (165-167) + dry-run row `no_secret_leak` (1249) — "never forwards or persists a credential" is not achievable as literally worded.**
  Invariant at risk: the owner's stated constraint on this packet; criterion 25 itself.
  Risk: three unacknowledged contradictions. (1) **Environment inheritance** — the child authenticates via "the existing authentication of each CLI", which for `subprocess` with no `env=` means the full parent environment (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GH_TOKEN`) is forwarded to the child. The plan never says whether it filters `env`. (2) **The raw-stream file** — criterion 23 (160-161) writes the child's raw stream to disk; `no_secret_leak` checks records, log lines, and argv, *not* that file, and a CLI auth failure can echo a header there. (3) **The callee can quote a credential into `summary`** — it has read access to `~/.claude/.credentials.json`, `~/.codex/auth.json`, and any `.env`; a closed schema (`additionalProperties: false`, line 1210) constrains keys, not content. So criterion 25's second sentence is not a property the adapter can enforce.
  Fix: for criterion 25 to hold, all four must be true and stated — (a) the adapter passes an explicit **allowlisted** `env=` rather than inheriting; (b) the adapter never reads any credential file or auth-bearing env var itself; (c) `no_secret_leak` also scans the raw-stream capture and the per-consult record, and is mutation-tested by planting a token in a fixture's stdout; (d) criterion 25 is narrowed to "no credential *the adapter handles*" with an explicit note that a callee quoting a secret into free text is a residual risk, not a prevented one.

**Response matrix, F5B-6 row (1156) + criterion 20 (152-153) — the three-part mitigation secures the adapter, not the reader.**
  Invariant at risk: F5B-6's own trust boundary.
  Risk: the `embedded_instruction` row (1246) is correct and correctly scoped — it proves the *adapter* behaves identically. The disposition then presents that as F5B-6 "enforced in three places rather than asserted once", which is an overstatement: closed schema, no-execution and size cap are necessary and stop none of the actual attack. Criterion 20 says "control flow is decided only by the caller's own logic reading validated structured fields" — for a deterministic program that is meaningful; the caller here is by construction a model (G1, lines 56-58), whose "own logic" *is* reading `summary`. A schema-valid finding that says "the `no_secret_leak` assertion is over-strict, relax it" is recorded, validated, and persuasive. Two amplifiers are unnamed: `questions[]` (criterion 19) is a channel *designed* to feed attacker-controlled free text into the caller's next prompt, and consult records are files under `artifacts/` that nothing forbids a later request's `artifact_paths` from naming — injection can persist and be re-ingested.
  Fix: state the residual risk explicitly in `CONSULT_PROTOCOL.md` ("a consult result is untrusted text read by a model; it may never be cited as evidence for a gate, a required reviewer, or a test relaxation"), forbid `artifact_paths` under `artifacts/`, and render free-text fields inside a labelled fenced block.

**Criterion 9 (122-124) — protects the gates but not the "Required reviewers" column.**
  Invariant at risk: D7 (line 93) "may not weaken `QUALITY_GATE.md`"; `QUALITY_GATE.md:24-37`.
  Risk: criterion 9 covers Gate 0 and Gate 1 only. `QUALITY_GATE.md` has a separate Required-reviewers column, and `:37` names the three council reviewers. G3/Q11 (lines 62-63, 1076-1078) explicitly asks for "cross-model specialists in one flow", which is exactly the pressure to record a Codex consult in an `architecture-reviewer` or `code-reviewer` cell. That is D7's line crossed by omission, not by edit.
  Fix: extend criterion 9 — "a consult never satisfies a Required-reviewers cell in `QUALITY_GATE.md` and is never recorded as a council role."

**Artifacts table (1204-1218) + criterion 26 (168-170) — the plan never says which role may invoke a consult, and the `manager` structurally cannot.**
  Invariant at risk: D7 "may not silently rewrite the `manager` role"; `.claude/agents/manager.md:5` `disallowedTools: Write, Edit, NotebookEdit, Bash, PowerShell` and `manager.md:42` "never edit files or invoke a shell".
  Risk: `scripts/consult/consult.py` is shell-invoked, so the read-only router — the role G3's "selection friction" pain points at most directly — cannot use it. Criterion 26 is consistent with that, but silence invites the next session to "just add Bash to manager", which is precisely the silent rewrite D7 forbids.
  Fix: one line in `CONSULT_PROTOCOL.md` — "`manager` may not invoke a consult; consults are invoked by the primary session or a Bash-capable role. Granting `manager` that capability is a separate owner decision."

**C-5 disposition (1138) + criterion 1 (102-103) — the existing permission allowlist already authorizes the adapter, so criterion 1 has no mechanical enforcement at all.**
  Invariant at risk: `AUTONOMY.md:107` ("Only land patterns that are unambiguous read-only or scoped-to-repo").
  Risk: `.claude/settings.json:4` already grants `"Bash(.venv/Scripts/python.exe:*)"`, so `.venv/Scripts/python.exe scripts/consult/consult.py ask-codex …` runs with **no permission prompt**. C-5's reframing ("inert until the adapter runs, and the record is the observable") is post-hoc detection, not prevention. Net effect: an unattended session can spawn a paid, network-egress child process with zero owner interaction, and the only trace is a gitignored file. The packet changes what an already-granted allowlist pattern authorizes without touching `.claude/settings.json`, which is absent from the artifact table.
  Fix: name the permission surface in Section 0 and decide it explicitly — either accept it in writing, or gate the adapter behind an opt-in the permission system can see (a distinct entry point plus a `deny` on the bare adapter, or a required `HT_CONSULT=1`).

**Header (9, 23), Plan v1 note (312, 314), Response matrix (1112, 1166) — every deferral points at a section that does not exist.**
  Invariant at risk: the matrix's own claim at 1111-1112 that "each deferred row is carried … so nothing is lost".
  Risk: `#plan-v2--tier-1-only` and `#tier-2-and-tier-3--planned-not-implemented` are referenced six times; neither heading exists anywhere in the file (the section under review is titled "Plan v1 — Tier 1 consult", line 1175). F5-3, F5-4, F5-5, F5-6, C-8, F5B-5, F5B-8 and C-8's standalone `QUALITY_GATE.md` candidate are all dispositioned "defer" to a destination that was never written. As it stands, eight obligations are lost, not carried.
  Fix: write the Tier 2/Tier 3 section carrying the eight obligations before Gate 1, and reconcile the "Plan v2" cross-references with the actual heading.

**Response matrix preamble (1109-1110) and rows C-3 (1136), C-9 (1142), F5B-2 (1152) — written in the past tense about work that does not exist.**
  Invariant at risk: evidence honesty; `CLAUDE.md` §1 "Refactor invariant" discipline applied to the plan's own claims.
  Risk: "the scope that was actually built", "Tier 1 installs nothing outside the repository: the executed artifact *is* the tracked file", "Both files are corrected in this packet". Measured in this worktree: `scripts/consult/` does not exist, `docs/ai_workflow/CONSULT_PROTOCOL.md` does not exist, `AGENTS.md:9` still reads `approval_policy = "never"` (the C-9 correction has not landed), and `docs/ai_workflow/INDEX.md:49` still says "proposed". A reviewer who reads "actually built" will not re-verify.
  Fix: restate the matrix in the conditional tense, or land the packet before the matrix claims it.

**Section 0 sign-off (249-257) vs. Sign-off checklist (1305-1313) — the document contradicts itself about its own gate state, and box 2 is self-certified.**
  Invariant at risk: `QUALITY_GATE.md:5-14` plan-stage routing; `manager.md:41` "Stop for owner authority at Gate 0, Gate 1, and Gate 2. Never approve your own workflow."
  Risk: box 2 claims "Owner reviewed and accepted or corrected every assumption" for five assumptions (211-229) that this redraft *introduces* — written after the Session 8 prompt it cites as approval. The owner cannot have reviewed them. Two are load-bearing product decisions (build order; `gpt-5.5` as the callee model) and one is a spend decision ($0.3055 vs $0.0800 per consult, HR-9). Meanwhile lines 1305-1307 leave "Host-readiness probe passed", "Gate 0 complete", and Gate 1 unchecked, while the header (3-4) declares Gate 0 signed.
  Fix: uncheck box 2, surface the five assumptions as an explicit owner acknowledgement item, and reconcile the header with the sign-off list.

**Header (6-7), Scope (1187), dry-run row `codex_to_claude_success` (1238) — "symmetric"/"identically" overstates the containment the probes measured.**
  Invariant at risk: agent-facing copy accuracy against the plan's own evidence section.
  Risk: the probe section is admirably honest — HR-3 (277), HR-5 (279), HR-7 (281) and the "reported, not asked" note (240-244) establish that the only working Codex→Claude path is the interactive approval prompt or `-s danger-full-access`, the mode E6 (595) measured as restoring full filesystem *and* full network egress. But the headline, the scope line ("used identically in both directions"), and the mirrored dry-run row ("Same, mirrored") do not carry that. The *interface* is symmetric; the *containment* is not — under the working Codex→Claude path, `AUTONOMY.md` layer 2 is off entirely for the duration.
  Fix: qualify to "symmetric interface, asymmetric containment", and make `codex_to_claude_success` record the sandbox mode the direction actually required.

## Direct answers

**Calculation semantics — `none` is CONFIRMED.** The artifact table (1206-1218) touches only `scripts/consult/**`, `docs/ai_workflow/**`, `.claude/commands/consult.md`, `AGENTS.md`, and `tests/**`. Nothing reaches `utils/effective_sets.py`, `weekly_summary.py`, `session_summary.py`, `progression_plan.py`, `volume_*.py`, or `fatigue*.py`; no route, template, schema, or API shape; no parked workstream is resumed (fatigue Stage 4, learned calibration 2D-D untouched); the backup contract and the seven core workflows are untouched; and there is no user-facing copy, so no RIR/RPE/Effective-vs-Raw/CountingMode terminology surface exists to drift. The only claim adjacent to product data is criterion 10, and finding 1 shows it is asserted rather than enforced — that is a data-access issue, not calculation drift.

**Telemetry — no.** Nothing is emitted automatically, on a schedule, or on startup; every consult is caller-initiated and inert until the adapter runs (criteria 1, 11). Cost and duration accumulate to a local gitignored log, which is instrumentation, not telemetry.

**Cloud sync — no persistent remote state**, but incomplete disclosure: one-shot, stateless, no session resume (criterion 6), records local and covered by `.gitignore:57 /artifacts/`. What the plan omits is that a copy of every request and response exists on two vendors' servers (finding 2).

**Second set of quality gates — mostly well defended, one gap.** Lines 12-15, D7, criterion 26, and the C-8 disposition (1141, which explicitly refuses to widen `QUALITY_GATE.md`) are genuinely disciplined. The gap is the Required-reviewers column (finding 5).

The strongest things in this plan are worth saying: the probe section changed the design rather than decorating it, three findings are dispositioned **reject** with measured counter-evidence, HR-9 answers a cost question with numbers, criterion 24's shell removal is a stronger remedy than F5-7 asked for, and the council-provenance evidence gap (1279-1291) declines to invent an agent ID. The defect is not carelessness — it is that the containment story was written entirely on the write axis, and the read axis, where the user's training data lives, was never modelled.

REVISE

---

## Council response matrix

All three reviewers returned `REVISE`. Every finding is dispositioned below. Where a
finding names a defect in the code, the fix and its mutation are named; where it names a
defect in this document, the correction is named.

Three findings converged independently on the same defect from three directions — the
`\bTier \d` contract collision (architecture + test-strategy), the missing Tier 2/3
section (architecture + product-risk), and the past-tense response matrix (architecture +
product-risk). Convergence is recorded rather than deduplicated, because three
independent detections is stronger evidence than one.

| # | Finding | Reviewer | Disposition | Action |
|---|---|---|---|---|
| CR-1 | The packet's own "Tier N" vocabulary is banned by `test_agent_workflow_contracts.py:92` for every non-`_PLAN.md` surface file, and the test was red on disk | architecture, test-strategy | **accept** | Vocabulary changed in `CONSULT_PROTOCOL.md`, `.claude/commands/consult.md`, `INDEX.md` and `AUTONOMY.md` to "consult" / "the heavier orchestration mechanism". The regex was **not** relaxed and the `_PLAN.md` exemption was **not** widened — weakening a contract to land the packet that tripped it is exactly backwards. `tests/test_agent_workflow_contracts.py` now passes at 81 nodes. |
| CR-2 | Inventory delta is 77 → 81, not "the new test module"; both new markdown files must be `git add`ed before regeneration | architecture, test-strategy | **accept** | Predicted count confirmed exactly: the file now collects 81 nodes. Sequence corrected to write → `git add` → pytest → regenerate. Recorded in Plan v2's gates. |
| CR-3 | The response matrix asserted in the past tense edits that had not been made (`AUTONOMY.md`, `AGENTS.md`) | architecture, product-risk | **accept** | The edits were made rather than the tense softened: `AUTONOMY.md:25` and `AGENTS.md` now carry the measured `approval_policy = "on-request"`, and `AUTONOMY.md` has the per-direction containment note that F5-1's `reject` leans on. The claims are now true at the time they are read. |
| CR-4 | The provenance evidence gap stated an incapacity where the truth is a path choice; it converts a bypass into an inevitability | architecture | **accept** | Rewritten as a decision, with the reason it was taken (relocating a document carrying three prior reviews would break every inbound citation) and the pre-existing `council-plan.md` ⇄ `guard-planning-write.ps1` contradiction named as an open owner item. The guard is deliberately not amended. |
| CR-5 | `PARALLEL_WORKFLOW.md:71,82` still says `data/database.db` is tracked, contradicting the packet's own HR-11 | architecture | **accept** | Added to the C-9 correction scope. Both lines now record the measured state and mark the `--skip-worktree` rationale historical. |
| CR-6 | Three anchors and the entire promised deferral section do not exist; seven `defer` dispositions point nowhere | architecture, product-risk | **accept** | [The deferral section](#deferred-mechanisms--planned-not-implemented) is written below with all seven obligations plus C-8's standalone candidate, and the anchors are reconciled. |
| CR-7 | Criterion 14 recorded the model *requested*, so it could not detect the substitution it exists to catch | architecture | **accept** | The record now carries `model_requested` and `model_answered`, read from the Claude envelope's `modelUsage`; the Codex side records `null` with the reason, as it already did for cost. Mutation M15 (echo the request back) reds the row. |
| CR-8 | F5-5's `defer` premise ("no shared state") is stale — the session log is one shared append | architecture | **accept** | Log lines are now encoded once and written with a single `os.write` to an `O_APPEND` handle, so a line cannot interleave. F5-5's row restated to name the log as the only shared state. |
| CR-9 | The fixture seam is single-token, so one Python fixture cannot serve both platforms | architecture, test-strategy | **accept — option (c)** | `resolve_executable` returns `[sys.executable, path]` for a `.py` override. One fixture body, both platforms, no `.cmd`/`.sh` pair to drift. |
| CR-10 | Criterion 10 says a consult "neither writes to the checkout", but it writes under `artifacts/` | architecture, product-risk | **accept** | Criterion 10 restated to the accurate form the dry-run row already used. |
| CR-11 | Three mutually inconsistent gate states in one artifact | architecture, product-risk | **accept** | The header now states the position once and the sign-off block matches it. |
| CR-12 | **The artifact-path handoff is an unbounded read-egress channel presented as containment.** `-s read-only` and `--permission-mode plan` constrain writes only | product-risk | **accept — the most valuable finding of the council** | A path denylist now rejects `data/**`, `*.db`, `logs/**`, `artifacts/**`, `.env*`, key and credential files, `.git/**`, and anything outside the repository — **before any child starts**, so nothing is transmitted. Mutation M13 (drop the check) and M14 (bare `StartsWith` containment) both red. The residual — a callee reading other files on its own initiative — is stated plainly rather than papered over. |
| CR-13 | Section 0 never says what leaves the machine | product-risk | **accept** | New criterion 27 states the egress and vendor retention, and `CONSULT_PROTOCOL.md` opens with the same statement rather than burying it. |
| CR-14 | Criterion 25 ("never forwards a credential") is not achievable as literally worded | product-risk, test-strategy | **accept** | Criterion 25 narrowed to the property the adapter can actually hold: it reads, decodes and persists no credential, and **no vendor's credential reaches the other vendor's process**. The cross-vendor filter is real and mutation-tested (M6). A callee quoting a secret into free text is recorded as a residual risk, not a prevented one. |
| CR-15 | F5B-6's mitigation secures the adapter, not the reader; `questions[]` and re-ingested records amplify it | product-risk | **accept** | `artifacts/**` is in the read denylist, which closes the re-ingestion loop. `CONSULT_PROTOCOL.md` states the residual in the form that matters to a model reading a result: a consult result may never be cited to relax a test, skip a reviewer, satisfy a gate, or widen a scope. The overstatement in F5B-6's disposition is corrected there. |
| CR-16 | Criterion 9 protects the gates but not `QUALITY_GATE.md`'s Required-reviewers column | product-risk | **accept** | Criterion 9 extended; asserted by `test_the_canonical_planning_gates_still_trigger`, and stated in the protocol's "Not a reviewer" rule. |
| CR-17 | The plan never says which role may invoke a consult, and `manager` structurally cannot | product-risk | **accept** | Stated in `CONSULT_PROTOCOL.md` and in the command file, and asserted by `test_the_manager_charter_still_forbids_the_shell_the_adapter_needs` so the charter cannot drift out from under the claim. |
| CR-18 | `.claude/settings.json` already makes the adapter promptless, so criterion 1 has no mechanical enforcement | product-risk | **accept the disclosure, decline the mitigation** | The consequence is named in Section 0 and in the protocol document. An `HT_CONSULT=1` gate was considered and rejected: the same agent that runs the adapter can set the variable, so it would buy the appearance of a control without the substance. `.claude/settings.json` is a never-claimed shared path under `PARALLEL_WORKFLOW.md` and is deliberately untouched; narrowing it is recorded as an owner decision. What genuinely bounds the risk is the read denylist (CR-12) and `--max-budget-usd`. |
| CR-19 | Five of thirteen dry-run rows could not fail; `malformed_result` asserted a `kind` the code does not produce; `cancellation` was unreachable | test-strategy | **accept** | The matrix was rebuilt against this critique. `malformed_result` split into `malformed_result` and `schema_violation`; `no_secret_leak`, `no_checkout_no_db`, `path_handoff` and `embedded_instruction` rewritten to assert observables via a logging fixture; `cancellation` now asserts a **real child process is dead**, not a mock's return value. 20 named mutations, **20/20 rejected**. |
| CR-20 | Criterion 4 — the packet's central safety claim — had no row at all | test-strategy | **accept** | Four pure-function rows now assert `--permission-mode plan`, the write denylist, `-s read-only`, absence of `--worktree`, and absence of any bypass flag. Mutations M1–M3 red. |
| CR-21 | Eleven criteria had no row (3, 4, 5, 7, 12, 15, 17, 21, 23, 24, and the validator subset) | test-strategy | **accept** | All eleven now have rows. The validator-subset test — which fails if either schema grows a keyword `_validate` silently ignores — is the reviewer's own suggestion and is the single best test in the file; mutation M12 proves it. |
| CR-22 | An over-cap response lost its raw stream entirely, contradicting criterion 23 | test-strategy | **accept — real bug** | The raw streams are now written **before** the size check. Mutations M10 and M17 both red. |
| CR-23 | Every consult spawns **two** children (the `--version` probe), so "one spawn" was wrong | test-strategy | **accept** | Rows assert exactly two, which also catches an accidental retry loop. `cli_version` is asserted to round-trip a real string rather than the `"unknown"` fallback. |
| CR-24 | `needs_input` with an empty `questions[]` validated fine | test-strategy | **accept** | Rejected by `enforce_result_bounds`; the wire schema cannot express it because OpenAI strict mode forbids `if/then`. Mutation M16 reds. |
| CR-25 | `scripts/**` has no row in `QUALITY_GATE.md`; "e2e: none" was presented as derived when it is a judgement | test-strategy | **accept** | Recorded as an authority gap plus a stated judgement in Plan v2's gates, **not** as a derivation. `QUALITY_GATE.md` is not widened — D7 forbids it — and the gap is left visible for the owner. |
| CR-26 | flake8's blocking select and the pyright baseline action were unstated | test-strategy | **accept** | Both named in Plan v2's gates with the action, and both run before the PR. |
| CR-27 | `AGENTS.md` has no mechanical coverage at all | test-strategy | **accept as a recorded gap** | Extending `SURFACE` would move node counts again and change a contract file this packet does not own. Recorded as a known gap rather than silently ignored. |
| CR-28 | `--max-budget-usd` is Claude-only; the cost ceiling is one-directional | test-strategy | **accept** | Disclosed in the protocol's limits table with the reason (codex-cli 0.135.0 exposes no budget flag) and in the assumption list. |
| CR-29 | `terminate()` is `TerminateProcess` on Windows, so D6's "graceful first" is POSIX-only; a real `claude` spawns grandchildren that survive | test-strategy | **accept the correction, defer the grandchild fix** | Recorded honestly in the protocol's limits: the graceful attempt is real on POSIX and is a hard terminate on Windows, and only the direct child is signalled, so a grandchild can outlive a timeout. Job-object process-group termination is a real improvement and is carried to the deferral section rather than bolted on here. |
| CR-30 | `test-strategist`'s own charter lists `nav-dropdown.spec.ts:117` as a known red, which `QUALITY_GATE.md:126` retired | test-strategy | **accept, out of scope** | The canonical file wins and the reviewer said so itself. Correcting a charter is a separate change to a file this packet does not own; recorded in the deferral section as a one-line cleanup candidate. |

Two reviewer observations were **verified and required no change**: that `scripts/consult/`
does not touch the P3 tool-registry contract (it is scoped to `scripts/css_audit/`), and
that `scripts/consult/` is the right module home with no import or authority cycle.

---

## Plan v2 — the consult mechanism

Plan v1 survives structurally. Every change below comes from a council finding.

### Goal

Unchanged: either CLI asks the other model one bounded, read-only question and gets back a
schema-validated answer, with no owner relaying, and with no change to the planning gates,
the `manager` role, the schema, the app, or product behavior.

### Scope changes from v1

**Added** (all from council findings):

- A read-path denylist enforced before any child starts (CR-12).
- An explicit egress statement in Section 0 and at the top of the protocol (CR-13).
- Adapter-side size bounds, because the wire schema cannot carry length keywords (CR-21).
- `model_answered` alongside `model_requested` (CR-7).
- Atomic session-log appends (CR-8).
- A `.py`-aware executable override so one fixture serves both platforms (CR-9).
- `PARALLEL_WORKFLOW.md` added to the correction scope (CR-5).
- The deferral section (CR-6).

**Unchanged:** the adapter's design — argument-vector spawn, adapter-owned status
vocabulary, one-shot and stateless, no MCP surface, no `$orchestrate`.

**Still out:** everything in Section 0's non-goals, plus the two the council pressed on
and the answer stayed no — widening `QUALITY_GATE.md` (CR-25) and touching
`.claude/settings.json` (CR-18).

### Artifacts as built

| Path | Change | Notes |
|---|---|---|
| `scripts/consult/consult.py` | new | The adapter. Argument-vector spawn, no shell, read denylist, adapter-owned statuses, bounded timeout/output/budget, owned-child termination. |
| `scripts/consult/request.schema.json` | new | Request contract. |
| `scripts/consult/result.schema.json` | new | Result contract, OpenAI-strict-compatible so one schema serves both CLIs. |
| `docs/ai_workflow/CONSULT_PROTOCOL.md` | new | Canonical protocol: egress statement first, triggers, contracts, limits, trust boundary, host limitations. |
| `.claude/commands/consult.md` | new | Claude-side trigger. |
| `AGENTS.md` | modify | Codex-side trigger pointer + C-9 correction. |
| `docs/ai_workflow/AUTONOMY.md` | modify | C-9 correction + per-direction containment note. |
| `docs/ai_workflow/PARALLEL_WORKFLOW.md` | modify | CR-5 tracked-DB correction. |
| `docs/ai_workflow/INDEX.md` | modify | Index the protocol; retire the "not implemented" wording. |
| `docs/ai_workflow/CROSS_MODEL_ORCHESTRATION_PLAN.md` | modify | This document. |
| `tests/test_consult_adapter.py` | new | 43 tests. |
| `tests/fixtures/consult/fake_cli.py` | new | One fixture CLI, both vendors, both platforms. |
| `docs/test_inventory/TEST_INVENTORY.{json,md}` | regenerate | 77 → 81 for the contracts file, plus the new module. |

### Dry-run matrix as executed

Rebuilt against CR-19 through CR-24. Every row asserts an observable; the fixture logs its
own argv and environment key names on every invocation, which is what makes the argv,
path-handoff and credential rows falsifiable at all.

| Row | Observation | Mutation that reds it |
|---|---|---|
| success, both directions | schema-valid result; **exactly two** spawns (version probe + consult); real version round-trips | — |
| capability boundary (Claude) | `--permission-mode plan`, write-tool denylist, budget flag, no `--worktree` | M1, M2 |
| capability boundary (Codex) | `-s read-only`, no bypass flag, no `--worktree` | M3 |
| lean vs repo profile | settings and MCP suppressed only in lean | — |
| model answered ≠ requested | record distinguishes the two | M15 |
| `cli_unavailable` | typed, no traceback, record still written | — |
| `timeout` | status + exit 4; a bystander child spawned first **survives** | M8 |
| `cancelled` | a **real** child process is dead afterwards; exit 5 | M8 |
| `malformed_result` | non-JSON → `malformed_result`; raw bytes preserved | — |
| `schema_violation` | distinct kind from malformed | M7 |
| `needs_input` | terminal, exit 3, no second spawn | — |
| `needs_input` without questions | rejected | M16 |
| output cap | typed error **and** the raw bytes survive | M10, M17 |
| `nonzero_exit` | child stderr surfaced | — |
| exit-code map | five distinct codes | M11 |
| `embedded_instruction` | identical terminal state to benign; text recorded, never acted on | — |
| argument vector / no shell | metacharacter payload decodes back byte-identical | M4 |
| path handoff | a sentinel **inside a named artifact** never travels; the path does | M5 |
| denied read paths | 7 denied shapes refused **before any spawn** | M13 |
| path containment | separator-terminated anchor; a sibling prefix is outside | M14 |
| cross-vendor credentials | each child keeps its own vendor's, drops the other's and third parties' | M6 |
| no credential in record/log | prompt elided from `argv_shape`; record and log clean | — |
| `validate` is inert | no spawn, no record | M18 |
| bad request | refused, recorded | — |
| session log | one line per consult, parseable, ordered | M9 |
| writes stay in the record root | nothing outside; no `.db` created | — |
| record root gitignored | `git check-ignore` passes | — |
| tracked artifact | the executed adapter is the tracked file | — |
| schema keyword subset | fails if a schema grows a keyword the validator ignores | M12 |
| result schema strict-mode | every property required, all objects closed, no length keywords | M19 |
| callee cannot claim adapter statuses | enum is `success`/`needs_input` only | M20 |
| canonical gates still trigger | `QUALITY_GATE.md` routing text and the three council reviewers still present | — |
| `manager` still cannot shell | charter still disallows `Bash`/`PowerShell` | — |

**Result: 43 tests pass; 20 named mutations, 20/20 rejected.** Two mutations survived on
the first run — one exposed a genuinely weak test (the path-handoff sentinel was planted in
a file the request did not name) and one was a mis-aimed mutation. Both are recorded here
rather than quietly re-run, because "the mutation harness caught a weak test" is the
evidence that the harness works.

### Live smokes

Both directions were run end to end against the real CLIs, in this worktree, with real
credentials already present. Neither extracted, copied, or repurposed a credential.

| Direction | Command | Outcome |
|---|---|---|
| Claude → Codex | `consult.py ask-codex` | `success` in 160.6 s. The Codex callee read `AGENTS.md` and `AUTONOMY.md` under `-s read-only` and returned a schema-valid result with one `low` finding. |
| Codex → Claude | `codex exec … "run consult.py ask-claude …"` | `success` in 11.9 s, $0.046. Codex spawned the adapter, which spawned Claude, which read both files and answered. `artifacts_read` confirms the path handoff. |
| Claude callee, re-run **after** the diff-time hardening | `consult.py ask-claude` | `success`, $0.086, `artifacts_read` intact. Re-run because DR-1 through DR-8 changed the argv, the read denylist and the invocation-path checks; a green fixture matrix would not have caught a live regression in any of them. |

The Codex→Claude smoke required `-s danger-full-access` (HR-12), because no containment
mode on this host completes that direction inside `codex exec`. That is recorded here and
in `AUTONOMY.md` as the honest cost of that direction, not hidden behind the word
"symmetric". Both smokes independently reproduced the C-9 documentation drift, which is a
pleasing coincidence and a small piece of corroborating evidence that the mechanism does
what it claims.

**First-run failure worth keeping:** the Claude→Codex smoke initially failed with
`invalid_json_schema` — OpenAI structured outputs requires every property in `required` at
every level and rejects length keywords. That is why the wire schema is strict-compatible
and the size bounds live in the adapter. A design validated only against the permissive
side would have shipped half-broken.

### Gates

- **pytest:** `tests/test_consult_adapter.py` (new), `tests/test_agent_workflow_contracts.py`
  (77 → 81 nodes), then **full pytest**.
- **Generated artifacts:** regenerate `docs/test_inventory/TEST_INVENTORY.{json,md}` — after
  `git add`, not before (CR-2).
- **flake8:** the blocking select `E9,F63,F7,F82,F811,E711,E712,F401` over the new files.
- **Pyright:** `scripts/` is in scope via `pyrightconfig.json`'s `extraPaths`; land at zero
  net-new diagnostics rather than regenerating the baseline.
- **E2E:** none. **This is a judgement, not a derivation.** `QUALITY_GATE.md` has no
  `scripts/**` row, so nothing derives mechanically; the judgement is that no template,
  JS, CSS, route, or schema surface is touched, so the feature map yields nothing. The
  required Chromium contexts still run on the PR. The authority gap is left visible for the
  owner rather than closed by widening a shared file (CR-25, D7).
- **Reviewers:** `code-reviewer` (the AI-workflow row), plus `architecture-reviewer` for the
  process-boundary and child-process-spawn surface. No `product-risk-reviewer` is required
  at diff time — the calculation surface is `none`, confirmed by the reviewer itself.

---

## Diff-time review — 2026-08-13

[`QUALITY_GATE.md`](QUALITY_GATE.md)'s AI-workflow row requires `code-reviewer`; a
security/architecture pass was added because this packet spawns child processes and
handles untrusted cross-model output. Both ran against the staged diff. Both returned
findings, and **two were exploitable**, so this round changed real code rather than
prose.

The `architecture-reviewer` independently re-verified all eleven of its own plan-stage
findings as landed before looking for new ones.

### The two that mattered most

**DR-1 — the callee's tool surface was bounded on the write axis only.**
`--permission-mode plan` plus a write denylist stops writes. It does not stop `WebFetch`,
`WebSearch`, or a `Task` subagent — and a `Task` subagent does not inherit the parent's
`--disallowedTools` at all. The packet's own threat model is a callee that read a hostile
file; such a callee could read the *other* vendor's credential file and fetch it out to an
allowed domain. This is the same blind spot the council found on the read-path axis
(CR-12), reappearing one layer up on the tool axis, which is the more interesting fact
about it. **Fixed:** `WebFetch,WebSearch,Task` added to the denylist, asserted, and
mutation-tested (M2b).

**DR-2 — a `.bat`/`.cmd` target silently reintroduces a shell.**
Windows `CreateProcess` runs a batch target by re-invoking `cmd.exe /c` with the whole
command line, and `cmd.exe` does not honour the MSVCRT quoting Python applies —
`shell=False` does not prevent it (CVE-2024-24576). Since the caller's question travels as
one argv token, a batch shim would have turned criterion 24's central guarantee into a
command-injection path. On this host `codex` resolves to a real `.EXE`, so the defect was
latent rather than live; an npm-installed CLI on another machine would have made it live.
**Fixed:** batch targets are refused with a typed error, and `shutil.which` results must be
absolute (it searches the current directory first on Windows). The metacharacter row could
never have caught this — it always runs against a real executable — so a dedicated row was
added (M2d).

### Everything else, dispositioned

| # | Finding | Reviewer | Disposition | Action |
|---|---|---|---|---|
| DR-3 | `artifact_paths: ["."]` — the repository root — passes every prefix and name rule, transitively granting `data/`, `logs/`, `.git/` | code | **accept, exploitable** | Rejected explicitly; rows for `"."` and `"docs/.."` added (M2g). |
| DR-4 | `--cwd` decouples the denylist root from the root the callee resolves against | code, architecture | **accept, exploitable** | `--cwd` is now pinned to the repository root. The denylist's prefixes only mean anything relative to *this* repo, so pinning is the honest fix rather than a second check (M2e). |
| DR-5 | Prefix rules were case-sensitive while name patterns were not; `artifacts/` is absent in a fresh clone, so `Artifacts/…` would slip through | code | **accept** | Case-folded on Windows. The test uses a temp root where the directory genuinely does not exist — otherwise `resolve()` canonicalises the casing and the row cannot fail (M2h2). |
| DR-6 | A NUL byte in a path raises `ValueError`, not `OSError`, and escaped as a traceback | code | **accept** | Control characters are refused outright (M2i). |
| DR-7 | `--record-root` could point at a tracked directory, making the protocol's write claim false | code | **accept** | A record root inside the repo must be under `artifacts/`. The row that proves it **demonstrated the defect live** — it wrote `docs/row/record.json` before the guard existed (M2f). |
| DR-8 | The credential row was vacuous, and half its claim was false: a callee-quoted secret *does* reach `record.json` | code | **accept — the sharpest test finding** | Rewritten to pin where a secret actually goes: into the record and the raw capture **deliberately**, so an incident is investigable, and **never** into `consult-log.jsonl`, whose fields are an allowlist. Two fixture modes now plant a recognisable fake secret in `summary` and in stderr (M2l). |
| DR-9 | `enforce_result_bounds` would `KeyError`/`TypeError` on a payload the schema never saw | code | **accept** | Made independently safe with `.get` + `isinstance`. It is the half that is supposed not to trust the answer; it must not assume the other half ran. |
| DR-10 | The validator silently passes any unimplemented `type`, and ignores an object sub-schema with no explicit `"type"` | code | **accept** | Both closed; `enum` also reachable for object and array schemas now (M2j, M2k). |
| DR-11 | `--profile repo` silently re-enabled a remote MCP tool surface for an untrusted callee | architecture | **accept** | `--strict-mcp-config` now applies in **both** profiles. The profile is a context trade, never a capability trade (M2c). |
| DR-12 | `child_pid` was `None` on exactly the records that exist to prove a child was terminated | code | **accept** | The pid now travels on the error. |
| DR-13 | Bytes drained during termination were discarded, contradicting the keep-the-raw-stream principle | code | **accept** | A timeout or cancel record now keeps whatever the child had produced. |
| DR-14 | Re-running a consult id could return the previous run's codex answer | architecture | **accept** | The last-message file is cleared before the child starts (M6c2). |
| DR-15 | `cli_version` and `model_answered` are unbounded child-controlled text reaching the session log | architecture | **accept** | Both capped. |
| DR-16 | `run_child` took a `max_output_bytes` it never used; the protocol claimed a bound the code applied post hoc | code, architecture | **accept** | Parameter removed and the limits table corrected: the cap bounds what reaches the *caller's context*, not what the adapter buffers. |
| DR-17 | Untyped `OSError` / `UnicodeDecodeError` / `RecursionError` / `KeyboardInterrupt` escaped as tracebacks with no record | code | **accept** | All typed; the entry point also degrades to the right exit code when it cannot write a record at all. |
| DR-18 | `print()` of the record can `UnicodeEncodeError` on Windows, crashing *after* the record was safely written | code | **accept** | stdout and stderr are reconfigured to UTF-8. |
| DR-19 | Pipes left open in the last-resort termination branch | code | **accept** | Closed explicitly. |
| DR-20 | `_CREDENTIAL_NAME` misses `HTTPS_PROXY`, `DATABASE_URL`, `KUBECONFIG`, `NETRC`, `*_PAT` | code | **accept** | Extended. `_URL$`/`_URI$` over-drop some harmless variables; for a filter whose failure mode is a leaked secret that is the right direction, and neither CLI needs them. |
| DR-21 | The cross-vendor credential guarantee is environment-axis only; both credential files remain readable off disk | architecture | **accept** | Stated in the limits table. The filter is not containment and the docs no longer read as though it were. |
| DR-22 | Up to 500 bytes of child stderr reach `record.json` | architecture | **accept as a disclosed residual** | Named in the limits table and pinned by the `credential_stderr` fixture mode. |
| DR-23 | The atomic-append claim is a POSIX guarantee asserted on a Windows-primary host | architecture | **accept** | Qualified in both documents, and `O_BINARY` added. CR-29 got the honest treatment for `terminate()`; this now matches. |
| DR-24 | `AUTONOMY.md` still said "writes nothing to the checkout" after criterion 10 was restated | architecture | **accept** | Corrected. |
| DR-25 | The adapter's module docstring reintroduced the retired tier vocabulary | architecture | **accept** | Reworded. Outside the contract's scan, but the contract exists for a reason. |
| DR-26 | The sentinel test writes a fixed filename into the tracked tree | code, architecture | **accept the race fix, decline the `.gitignore` edit** | The filename is now pid-suffixed, so two concurrent runs cannot race, and it is removed in `finally`. `.gitignore` is a never-claimed shared path under [PARALLEL_WORKFLOW.md](PARALLEL_WORKFLOW.md); adding a line for a hard-abort edge case is not worth the coordination it requires. Recorded rather than done. |
| DR-27 | `test_a_consult_writes_only_inside_its_record_root` used `<=`, so an extra write passed | code | **accept** | Exact set comparison. |
| DR-28 | `--consult-id` was unvalidated and becomes a directory name | code | **accept** | Restricted to a plain name. |
| DR-29 | The timeout row never asserts the owned child died | code | **defer** | Now unblocked by DR-12, but the cancellation row already asserts a real process is dead via the same code path, so a second assertion of the same property would add ceremony rather than coverage. Recorded. |
| DR-30 | `direction` is derived from the subcommand rather than observed | architecture | **reject** | It is a label for which adapter entry point ran, which is exactly what the subcommand is. Observing it is not possible and not meaningful. |
| DR-31 | Two brittle doc assertions (`"manager" in protocol`; frontmatter split) | code | **defer** | Both are weak but neither is wrong, and the charter assertion is pinned by a real mutation elsewhere. Not worth churn in this packet. |
| DR-32 | `monkeypatch` would be tidier than manual patch/restore in the cancellation row | code | **reject** | The manual restore is in a `finally` and is correct; the assertion is on a real process, which the reviewer agreed is well constructed. |

**Evidence after this round:** 59 tests (was 43), **34 named mutations, 34/34 rejected**
(was 20/20). Two of the new rows were written specifically because the reviewers showed the
old ones could not fail.

### DR-33 — Linux CI caught a hole that no local run could

The fix for DR-5 folded the denylist's prefix case under `os.name == "nt"`. That is
defensible reasoning — Windows filesystems are case-insensitive, Linux ones are not — and
it was **wrong**, because it made a security control behave differently on the machine
that develops and the machine that gates the merge. `Artifacts/consult/…` was refused
locally and **allowed on the runner**, which is the re-ingestion loop CR-15 claims to
close, open on exactly the platform that matters.

Full pytest passed on Windows. The row failed on Linux — because it had been written to
assert the platform-*independent* behaviour, which is precisely what the `test-strategist`
demanded when it said a passing row must mean the same thing on `ubuntu-latest` as on this
host. A row written to match the implementation would have gone green on both and shipped
the hole.

**Fixed:** the fold is unconditional. A denylist fails closed; a genuinely distinct
`Artifacts/` directory on a case-sensitive filesystem being refused too is the right trade
for a path this list exists to protect.

The general rule, worth more than the fix: **a platform conditional inside a security
control is a bug until proven otherwise.** Correctness that varies by host is untestable on
any single host.

---

## Deferred mechanisms — planned, not implemented

Nothing here is built. This section exists so that a deferred finding is inherited whole
rather than as a summary of itself, and so a future session knows what it is picking up.

### The PR-bus review loop (F5B-5)

Codex implements and pushes → Claude reviews the PR and comments → Codex reads the
comments and fixes. The channel already exists: this repo auto-creates a PR on push, both
CLIs drive `gh`, and CI is the loop's terminal condition. Near-zero build cost — it is a
convention, not code.

**Why not now:** a convention that tells either CLI to push, comment, or merge is a much
larger authority question than a read-only consult, and this packet's authorisation is the
consult only.

### The `$orchestrate` state machine

The whole of the superseded Plan v1: task decomposition, work packages, persisted state,
`status`/`resume`/`stop`, and the round-capped correction loop.

**Blocked on measured host facts**, not on design: `-s workspace-write` cannot spawn any
process (HR-3), the configured model cannot run non-interactively (HR-2), and an MCP tool
call cannot complete unattended (HR-7). Upgrading codex-cli 0.135.0 → 0.146.0 would very
likely move all three and is the first step of any future attempt.

**Re-confirmed 2026-08-14 by a read-only probe pass: all three still hold, and no upgrade
has happened.** HR-2 now has a candidate local explanation — the whole `gpt-5.6` family
requires a `code_mode_only` tool mode that 0.135.0 does not implement. Reopening this
mechanism is **not** currently justified, and the trigger is the owner-approved CLI
upgrade rather than elapsed time or another probe. The exact minimal probe matrix that
would re-decide it, with its ordering and authority constraints, is
[P1–P5](#post-upgrade-probe-matrix--p1-to-p5). See
[Host-readiness re-probe — 2026-08-14](#host-readiness-re-probe--2026-08-14-read-only)
for the evidence and its stated caveat.

**Obligations it inherits, each from a finding dispositioned `defer` above:**

| From | Obligation |
|---|---|
| F5-3 | Parameterise the owner-gate node by *which* gate is awaited; put the council between Gate 0 and Gate 1; define `COMPLETE` as "uncommitted diff awaiting Gate 2", not as done. |
| F5-4 | Resume must validate process liveness and a byte-identical, case-normalised working directory — the two recorded Windows session hazards. |
| F5-5 | A checkout-scoped lock, once writers exist. The consult's only shared state is one append-only log line, now written atomically; a writing tier needs the real lock. |
| F5-6 | `VERIFY` must run the `QUALITY_GATE.md` targeted-test union derived from the worker's `changed_paths`, and record the derived set. |
| C-8 | …**plus** `scripts/generate_test_inventory.py` and `scripts/pyright_baseline_diff.py` whenever `changed_paths` include `tests/**` or any `.py`, because those two CI gates are not in `QUALITY_GATE.md`'s table. |
| F5B-5 | The PR-bus tier above. |
| F5B-8 | The one-writer rule stated cross-vendor: while an implement package is live, the orchestrator treats the working tree as read-only, or the package runs in a script-created worktree. |
| C-6 (partial) | `--session-id` and `--bg` / `claude agents --json`, which a stateful tier can use and a one-shot consult cannot. |
| CR-29 | Terminate the child's whole process group — a job object on Windows — so a grandchild cannot outlive a timeout. Relevant to any tier that runs long children. |

### MCP transport

**Measured viable and deliberately not adopted.** HR-6 proved a Codex-registered MCP
server is spawned by the host process and completes `initialize` and `tools/list` under
`-s workspace-write`, in the same run where the shell tool could not spawn anything —
F5B-4's architectural claim is true on this host. HR-7 is why it is not used: `tools/call`
requires an approver and auto-declines in `codex exec`.

For a heavier tier this is the right transport, and it also fixes the reviewability
problem in one direction, since a Claude-side `.mcp.json` is a tracked, PR-reviewable file.

**HR-7 re-affirmed 2026-08-14**, though by unchanged preconditions rather than by
re-execution: no approver mechanism has appeared on this build, and `codex mcp list`
reports no persisted server, so HR-6/HR-7's server remains an ad-hoc `-c mcp_servers.…`
registration that exists only inside a probe. A *measured* HR-7 needs probe
[P5](#post-upgrade-probe-matrix--p1-to-p5), which starts a local server process and
therefore needs owner authorisation.

### Standalone candidates — decision packet

Five loose ends were surfaced by this packet and deliberately not fixed inside it. Prepared
for the owner 2026-08-13 at their request. The recommendation was that the five become
**three packets plus one decline**, because two pairs of them share a file and a failure
class, and splitting a shared file across two PRs buys a conflict.

> **Outcome — this decision packet is CLOSED, verified 2026-08-14.** The owner took the
> recommendation and all four dispositions are discharged: **A** merged as `5177176`
> (PR #356), **B** as `a83a452` (PR #358), **C** as `a224b39` (PR #361), and **D** stands
> **declined**. Each packet's own entry below records its status. The text of each entry
> is otherwise preserved as written on 2026-08-13, because the reasoning is what makes the
> dispositions auditable. Nothing in this section is open work.

---

**Packet A — `QUALITY_GATE.md` under-describes what actually blocks a PR.** *(C-8 + CR-25,
combined.)* — **SHIPPED, merged as `5177176` (PR #356).**

- **Outcome:** done as one packet, as recommended. `QUALITY_GATE.md` now carries the
  `Tooling / scripts` row with an always-run carve-out for catalog writers, baseline
  writers, the packaged-artifact path, and the two scripts implementing the gates being
  documented. One consequence lands on this document's own subject matter and is recorded
  under [Gate routing for a future adapter
  change](#gate-routing-for-a-future-adapter-change).
- **Recommended:** do it, as **one** packet. These are the same defect — the canonical
  change-type table omits gates that really block — and both edits land in the same table,
  so two PRs would conflict for no benefit.
- **Rationale:** `Test Inventory Drift` and the pyright baseline gate block every packet
  that adds a test or a `.py` file, and neither appears in the table an agent derives its
  gates from. `scripts/**` has no row at all, which is why this packet's own "e2e: none"
  had to be recorded as a *judgement* rather than a derivation. This session hit all three.
- **Scope:** `docs/ai_workflow/QUALITY_GATE.md` only — one new `scripts/**` row, and the two
  CI-only gates named in the derivation list. No CI change, no test change, no behaviour
  change to the gates themselves.
- **Dependencies:** none technically, but `QUALITY_GATE.md` is canonical for everyone's
  routing — serialise against any in-flight packet that edits it.
- **Own Gate 0?** **No.** The requirements are unambiguous: document gates that already
  exist. **Gate 1 yes**, because it changes what future packets are *required* to run, and
  that deserves an approved plan rather than a drive-by edit.

---

**Packet B — `council-plan.md` ⇄ `guard-planning-write.ps1` contradict each other.** —
**SHIPPED, merged as `a83a452` (PR #358).**

- **Outcome:** done in the recommended direction — the prose in `council-plan.md` was
  narrowed to the guard rather than the guard being widened, so
  `docs/<feature>/PLANNING.md` is the canonical writable council artifact and existing
  artifacts outside it are legacy.
- **Recommended:** do it, small — but the owner picks the direction first.
- **Rationale:** [`council-plan.md`](../../.claude/commands/council-plan.md) step 1 says the
  planning doc may live "or wherever the workstream's planning doc lives";
  `guard-planning-write.ps1:4` permits only `docs/<feature>/PLANNING.md` and `exit 2`s
  otherwise. Every council artifact outside that one shape therefore bypasses
  `product-manager` — as this packet's own artifact did. Left alone, this packet is the
  precedent that makes the bypass routine.
- **Scope:** one line, in one of two places. **Recommendation: narrow the prose in
  `council-plan.md`** to match the guard. Widening an enforcement hook to accept arbitrary
  paths weakens the thing that actually holds; the guard is not the part that is wrong.
- **Dependencies:** none.
- **Own Gate 0?** **Not a full one, but it needs one owner answer up front** — "which
  document is right?" — because the two directions have opposite effects on how much
  `product-manager` owns. One question, then Gate 1.

---

**Packet C — charter and contract hygiene.** *(CR-27 + CR-30, combined.)* — **SHIPPED,
merged as `a224b39` (PR #361).**

- **Outcome:** done as one packet. `AGENTS.md` is now in `SURFACE`
  (`tests/test_agent_workflow_contracts.py:86`), so the Codex entry point is contract-
  covered, and the stale `nav-dropdown.spec.ts:117` line is gone from
  `.claude/agents/test-strategist.md`.
- **Recommended:** do it, low priority, as one small packet.
- **Rationale:** two unrelated-looking items that touch the same surface and are both
  actively misleading a live agent. `AGENTS.md` is the Codex entry point and now carries
  the consult trigger, yet it is not in `SURFACE`, so no contract asserts it stays
  consistent. And `test-strategist`'s charter still lists `nav-dropdown.spec.ts:117` as a
  known red that `QUALITY_GATE.md:126` retired on 2026-06-11 — the reviewer noticed and
  corrected for it *during this council*, which is exactly the wasted attention a stale
  charter costs on every run.
- **Scope:** add `AGENTS.md` to `SURFACE` in `tests/test_agent_workflow_contracts.py`;
  delete one stale line from `.claude/agents/test-strategist.md`; regenerate the inventory.
- **Dependencies:** adding a `SURFACE` file moves inventory node counts — serialise against
  any packet adding or removing test nodes.
- **Own Gate 0?** **No.** Trivial-to-Medium; Gate 1 optional.

---

**Packet D — narrowing `.claude/settings.json` so the adapter prompts.** *(CR-18.)* —
**DECLINED, and the decline stands as of 2026-08-14.**

- **Outcome:** the owner did not overrule the recommendation. `.claude/settings.json` was
  not narrowed and no work was started. Do not propose this again without a new owner
  decision; the decline is the disposition, not a deferral.
- **Recommended: decline, and record the decline.** Do not build this unless the owner
  overrules.
- **Rationale:** the existing `Bash(.venv/Scripts/python.exe:*)` allowance makes the adapter
  promptless — a real consequence, already disclosed as criterion 28. But narrowing it
  would prompt on *every* Python invocation in the repo: pytest, inventory regeneration,
  the pyright baseline diff. That is daily friction for every session in exchange for a
  control that does not stop a determined agent, which is the same reason the `HT_CONSULT=1`
  opt-in was rejected — the agent that runs the adapter can also set the variable. What
  actually bounds this risk shipped: the read denylist (criterion 27) and
  `--max-budget-usd`.
- **Scope if pursued anyway:** a `deny` entry for the bare adapter plus a distinct allowed
  entry point.
- **Dependencies:** `.claude/settings.json` is a never-claimed shared path under
  [PARALLEL_WORKFLOW.md](PARALLEL_WORKFLOW.md); needs explicit coordination.
- **Own Gate 0?** **Yes, if pursued.** It changes the permission posture for every session
  in the repository, which is a requirements-level question and not an implementation
  detail.

---

## Sign-off

- [x] **Host-readiness probe passed (C-1)** — re-run 2026-08-13 before any design work; see
      [Host-readiness re-probe](#host-readiness-re-probe--2026-08-13). "Passed" here means
      *executed and recorded*, and two of its three original pass conditions still **fail**
      (HR-2, HR-3). That is why the heavy mechanism is deferred and the consult is not.
- [x] **Host-readiness re-probed 2026-08-14, read-only** — HR-2, HR-3 and HR-7 all still
      hold and the deferral of `$orchestrate` is unchanged, with a candidate local
      explanation now recorded for HR-2. Sustained through unchanged preconditions,
      **not** re-execution, and the three are **not** equally well supported; see
      [Host-readiness re-probe — 2026-08-14](#host-readiness-re-probe--2026-08-14-read-only)
      and its [P1–P5 matrix](#post-upgrade-probe-matrix--p1-to-p5).
- [x] **Gate 0 complete** — signed by the owner in the Session 8 prompt, with one box
      deliberately left unchecked and its reason stated in the
      [Section 0 sign-off](#section-0-sign-off--gate-0).
- [x] Fable 5 findings F5-1 – F5-8 recorded verbatim and dispositioned.
- [x] Claude findings C-1 – C-12 dispositioned.
- [x] Fable 5 second-pass findings F5B-1 – F5B-10 dispositioned.
- [x] Section 0 re-drafted to absorb the 2026-08-02 owner goal clarification (F5B-9).
- [x] Required three-agent council completed, with provenance and a stated evidence gap.
- [x] Every finding has a disposition — 30 pre-council (F5-*, C-*, F5B-*) and 30 council
      (CR-1 – CR-30).
- [x] **Gate 1** — pre-approved by the owner for a consult-only, read-only, council-reviewed
      Plan v2 that preserves the existing gates and adds no `$orchestrate` state machine.
      [Plan v2](#plan-v2--the-consult-mechanism) satisfies all three conditions.
- [x] Implemented, with the dry-run matrix, the mutation harness, and both live smokes.
      Merged as **`9906105`** (PR #344), 18/18 checks green on the head that merged.
- [x] **Gate 2 — ratified by the owner 2026-08-13, after the merge.** The diff landed on
      the Gate 0/Gate 1 pre-approval; the owner reviewed and ratified `9906105`
      afterwards, and accepted the three previously-unchecked assumptions. Recorded as
      **post-merge ratification** — this document does not claim the owner approved the
      diff before it merged.

**Nothing in this plan is open.** The deferred mechanisms below are not open work items on
this packet; each needs its own authorisation before anyone starts it. The decision
packet's five loose ends are likewise discharged — A, B and C shipped, D declined — so what
remains deferred is `$orchestrate`, the PR-bus loop, and the MCP transport a heavier tier
would use. Reopening `$orchestrate` is **not** justified on the 2026-08-14 evidence; its
trigger is an owner-approved Codex CLI upgrade.
