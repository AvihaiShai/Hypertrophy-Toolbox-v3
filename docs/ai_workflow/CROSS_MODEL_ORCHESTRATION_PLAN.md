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
  [Deferred mechanisms](../archive/2026/cross-model-orchestration/CROSS_MODEL_ORCHESTRATION_HISTORY.md#deferred-mechanisms--planned-not-implemented)
- **Pre-council reviewers (advisory, historical):** Fable 5, Claude Opus 5

This proposal extends the existing AI workflow; it does not create a second set of
quality gates. [`QUALITY_GATE.md`](QUALITY_GATE.md),
[`AUTONOMY.md`](AUTONOMY.md), and
[`PARALLEL_WORKFLOW.md`](PARALLEL_WORKFLOW.md) remain canonical.

> **This plan is closed.** The consult shipped as `9906105` and Gate 2 was ratified
> post-merge. What remains below the implementation is deferred scope with no
> authorisation attached. The [decision packet](../archive/2026/cross-model-orchestration/CROSS_MODEL_ORCHESTRATION_HISTORY.md#standalone-candidates--decision-packet)'s
> five loose ends have since been resolved — packets **A, B and C shipped** and **D was
> declined** — so the scope still deferred is the `$orchestrate` mechanism, the PR-bus
> loop, and the MCP transport a heavier tier would use. A read-only re-probe on
> **2026-08-14** found the preconditions behind the three host blockers that defer
> `$orchestrate` unchanged, so all three are **inferred to still hold — from unchanged
> preconditions, not re-measured**; see
> [Host-readiness re-probe — 2026-08-14](../archive/2026/cross-model-orchestration/CROSS_MODEL_ORCHESTRATION_HISTORY.md#host-readiness-re-probe--2026-08-14-read-only).

> **Reading order.** Section 0 below is the **v2 requirements brief**, redrafted
> 2026-08-13 around the owner's G1–G3 goal clarification. The original 2026-08-01 brief
> is superseded; it survives in git history and every finding that changed it is
> dispositioned in the [Response matrix](../archive/2026/cross-model-orchestration/CROSS_MODEL_ORCHESTRATION_HISTORY.md#response-matrix). "Plan v1" further down is
> the original state-machine draft, retained unmodified as the audit trail for the three
> pre-council reviews. The plan that was actually built is
> [Plan v2 — the consult mechanism](#plan-v2--the-consult-mechanism).

**Section map.** This file keeps the status header, Plan v2 and the sign-off. Section 0, both
host-readiness re-probes, the Plan v1 drafts, every review and the council, the response matrix,
the diff-time review and *Deferred mechanisms* moved on 2026-10-20, word for word, to
[`CROSS_MODEL_ORCHESTRATION_HISTORY.md`](../archive/2026/cross-model-orchestration/CROSS_MODEL_ORCHESTRATION_HISTORY.md).
Where the text here says "below" or "further down" about one of those sections, read that file.
Before changing the consult adapter, read its [*Gate routing for a future adapter change*](../archive/2026/cross-model-orchestration/CROSS_MODEL_ORCHESTRATION_HISTORY.md#gate-routing-for-a-future-adapter-change).

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

## Sign-off

- [x] **Host-readiness probe passed (C-1)** — re-run 2026-08-13 before any design work; see
      [Host-readiness re-probe](../archive/2026/cross-model-orchestration/CROSS_MODEL_ORCHESTRATION_HISTORY.md#host-readiness-re-probe--2026-08-13). "Passed" here means
      *executed and recorded*, and two of its three original pass conditions still **fail**
      (HR-2, HR-3). That is why the heavy mechanism is deferred and the consult is not.
- [x] **Host-readiness re-probed 2026-08-14, read-only** — HR-2, HR-3 and HR-7 are all
      **inferred to still hold** and the deferral of `$orchestrate` is unchanged, with a
      candidate local explanation now recorded for HR-2. Sustained through unchanged
      preconditions, **not** re-measurement, and the three are **not** equally well
      supported; see
      [Host-readiness re-probe — 2026-08-14](../archive/2026/cross-model-orchestration/CROSS_MODEL_ORCHESTRATION_HISTORY.md#host-readiness-re-probe--2026-08-14-read-only)
      and its [P1–P5 matrix](../archive/2026/cross-model-orchestration/CROSS_MODEL_ORCHESTRATION_HISTORY.md#post-upgrade-probe-matrix--p1-to-p5).
- [x] **Gate 0 complete** — signed by the owner in the Session 8 prompt, with one box
      deliberately left unchecked and its reason stated in the
      [Section 0 sign-off](../archive/2026/cross-model-orchestration/CROSS_MODEL_ORCHESTRATION_HISTORY.md#section-0-sign-off--gate-0).
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

**Nothing in this plan is open.** The [deferred mechanisms](../archive/2026/cross-model-orchestration/CROSS_MODEL_ORCHESTRATION_HISTORY.md#deferred-mechanisms--planned-not-implemented) are not open work items on
this packet; each needs its own authorisation before anyone starts it. The decision
packet's five loose ends are likewise discharged — A, B and C shipped, D declined — so what
remains deferred is `$orchestrate`, the PR-bus loop, and the MCP transport a heavier tier
would use. Reopening `$orchestrate` is **not** justified on the 2026-08-14 evidence; its
trigger is an owner-approved Codex CLI upgrade, and elapsed time or a re-probe is not one
([*The trigger for revisiting*](../archive/2026/cross-model-orchestration/CROSS_MODEL_ORCHESTRATION_HISTORY.md#the-trigger-for-revisiting)).
