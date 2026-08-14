# AI Workflow Index

*Navigation map for AI agents and humans working on this repo. The Master Handover is the entry point; everything else here is reference.*

## Spine (read first)
- [Master Handover](../MASTER_HANDOVER.md) — canonical current state
- root [CLAUDE.md](../../CLAUDE.md) — operational guidance
- [`.claude/rules/`](../../.claude/rules/) — subsystem rules (auto-loaded by Claude Code on matching paths)

> **There is no shared plan file, and no tier or appendix numbering.** Workflow
> authority is split by topic, and each of these is canonical for its own:
> [QUALITY_GATE.md](QUALITY_GATE.md) (which tests and reviewers a change needs,
> and which planning gates apply), [AUTONOMY.md](AUTONOMY.md) (roles, approval,
> review boundaries), [PARALLEL_WORKFLOW.md](PARALLEL_WORKFLOW.md) (checkout and
> DB isolation), [WORKSTREAM_OWNERSHIP.md](WORKSTREAM_OWNERSHIP.md) (path
> claims). A retired `.claude/SHARED_PLAN.md` once claimed to define all four;
> it is gitignored so that a local scratch copy can never become tracked truth
> again. If a document tells you to consult a "Tier" or "Appendix", that
> reference is stale — use this list instead.

## Active feature plans
- [Agent workflow v2.2](../agent_roles/PLANNING.md) — manager, requirements,
  implementation, and independent-QA role rollout; Gate 0/Gate 1 approved 2026-07-11
- [Fatigue meter](../fatigue_meter/PLANNING.md) — Phase 1 shipped; Phase 2 Path 1 shipped 2026-05-23 via PR #35 (`d5b80bf`); Phase 2 Stage 3 verify-suite gate closed 2026-05-24 (`1a93f66`). [Phase 2 Stage 4](../fatigue_meter/PHASE2_PLANNING.md) **closed 2026-08-13** via #338 (`700b5da`) — no real-use evidence, no threshold change. The [Fatigue heatmap](../fatigue_meter/HEATMAP_PLANNING.md) shipped via #339 (`ea82ef1`) as visualization only. Phase 1 Stage 4 closed separately, 2026-05-20.
- [workout.cool integration](../workout_cool_integration/PLANNING.md) — §3 + §3.6 + §4 + §4.6 + §5 all shipped (§3.6 Profile bodymap landed 2026-05-23, `18ad223`; §5 first curated batch landed 2026-05-22, `cf21191`)
- [YouTube reference videos](../workout_cool_integration/YOUTUBE_REFERENCE_VIDEOS.md) — closed 2026-05-23 (`cf21191` 36 rows + `ff244aa` +20 rows = **56 curated rows**); long tail uses the search fallback by design
- [User profile](../user_profile/PLANNING.md) — questionnaire + bodymap + insights card + Body Composition display hooks (#17/#18) all shipped
- [Body Composition Issue #21](../archive/body_composition/development_issues.md) — Resolved 2026-05-23; PR #31 (`20b4b24`) + PR #32 (`94482d7`) + Profile hooks (`de3e4d0`)
- [Testing strategy](../TESTING_STRATEGY_PLANNING.md) — Phases 0–1 shipped; Phase-2 Packet A shipped as #342 (`1438a14`), while strict-console Packet C and axe Packet D remain queued in [`testing_phase2/PLANNING.md`](../testing_phase2/PLANNING.md). D4, D6, D7 and the `js-unit` half of D2 remain unsigned; Phases 3/5 and the release/tag half of Phase 4 remain proposals
- [Theme-dark P3](../css_theme_dark_p3/PLANNING.md) — both gates were signed, `P3-a0` shipped as #280 (`cd93480`), and the owner terminated the arc at a0. No later P3 packet is authorized
- [app.py review](../APP_PY_REVIEW_PLAN.md) — P1–P5 all merged 2026-08-01, including packaged-smoke permanence and #266's post-merge hardening. Completion history; do not reopen
- [Product documentation suite](../PRODUCT_DOCS_PLAN.md) — **executed**; the owner-selected subset shipped as [`docs/product/**`](../product/README.md) (App Flow, Backend Schema, Design Brief, plus the suite README). PRD and TECH_DESIGN were deliberately not built — see §8.5. Completion history; do not reopen

## History & decisions
- [CHANGELOG](../CHANGELOG.md)
- [DECISIONS](../DECISIONS.md) — durable project choices and lightweight ADRs
- [Documentation Retention](DOC_RETENTION.md) — when to keep, archive, or delete docs
- [CLAUDE.md audit](../CLAUDE_MD_AUDIT.md)
- [E2E testing notes](../E2E_TESTING.md)
- [CSS ownership map](../CSS_OWNERSHIP_MAP.md)
- [Volume taxonomy audit](../archive/VOLUME_TAXONOMY_AUDIT.md)

## Workflow artifacts
- [P1.6 dependency-queue closeout](../P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md) — CLOSED
  2026-08-03. #287 (stylelint) and #288 (Playwright) closed, both frozen by
  `dependabot.yml` ignore rules. Carries the **unblock condition** for the deferred
  Playwright 1.62.1 upgrade: #281 merged **and** #286 resolved, then bump both
  ecosystems and regenerate both platforms' baselines in one arc
- [Cross-model consult protocol](CONSULT_PROTOCOL.md) — canonical for the opt-in,
  read-only, one-shot consult in which either CLI asks the other model one bounded
  question. Shipped 2026-08-13. Read its first section before the first consult of a
  session: a consult sends text off this machine, and it answers no gate
- [Cross-model orchestration plan](CROSS_MODEL_ORCHESTRATION_PLAN.md) — the design
  record behind the protocol above: measured host evidence, the disposition of all
  thirty pre-council findings, the council review, and the heavier `$orchestrate`
  mechanism that remains **planned and deliberately unimplemented**
- [Quality Gate](QUALITY_GATE.md) — change-type → required tests/reviewers map
- [Autonomy Model](AUTONOMY.md) — Codex/Claude approval, sandbox, worktree, and review boundaries
- [Parallel Workflow](PARALLEL_WORKFLOW.md) — one manager-led feature per checkout,
  DB isolation, and the tracked-DB commit rule
- Folder orientation maps (Claude Code auto-loads on path entry):
  - [routes/CLAUDE.md](../../routes/CLAUDE.md)
  - [utils/CLAUDE.md](../../utils/CLAUDE.md)
  - [tests/CLAUDE.md](../../tests/CLAUDE.md)
  - [e2e/CLAUDE.md](../../e2e/CLAUDE.md)
  - [templates/CLAUDE.md](../../templates/CLAUDE.md)
  - [static/js/CLAUDE.md](../../static/js/CLAUDE.md)
- [Plan Review Template](PLAN_REVIEW_TEMPLATE.md) — size-conditional Section 0 / Gate 0 → Plan v1 → council findings → response matrix → Plan v2
- Skills live in `.claude/skills/<name>/SKILL.md`; the requirements workflow lives
  at `.claude/skills/requirements/SKILL.md`, is owned by `product-manager`, and stays
  strictly Section-0-only (stops at Gate 0). `product-manager`'s broader write
  ownership — the entire active `docs/<feature>/PLANNING.md`, including Plan v1, the
  response matrix, and Plan v2 when the read-only `manager` delegates them during
  `/council-plan` — is documented in [AUTONOMY.md](AUTONOMY.md#workflow-roles).
- Slash commands: `/handover`, `/unslop`, `/verify-and-polish`, `/council-plan`, `/consult` (in `.claude/commands/`)
- Agents (diff-time): `code-reviewer`, `unslop-reviewer` (in `.claude/agents/`)
- Agents (plan-time, council): `architecture-reviewer`, `test-strategist`, `product-risk-reviewer` (in `.claude/agents/`)
- Active workflow roles: `manager`, `product-manager`, `senior-developer`,
  `automation-qa`, `manual-qa-reviewer` (implemented and dry-run in Phase 3 of
  the agent workflow plan; default-manager activation remains Phase 6-gated).

## Baselines (gitignored, generated locally)
- `artifacts/baseline_pytest.txt`, `artifacts/baseline_e2e.txt` — last full-suite outputs; not in git
- Generated output belongs under `artifacts/`, never the repository root. `/artifacts/`
  is gitignored, and Playwright (`playwright.config.ts`), pytest's cache (`pytest.ini`),
  and both CI workflows already write there.
