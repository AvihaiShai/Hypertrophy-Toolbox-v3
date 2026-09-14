---
description: Full gate — /verify-suite, then the reviewers QUALITY_GATE.md requires, then handover. Use when QUALITY_GATE.md selects the full gate or the user explicitly requests it.
---

This is a **sequence guide**, not a chained skill. Use it when `QUALITY_GATE.md` selects the full gate or the user explicitly requests it.

> **Who runs which step.** Step 2 spawns subagents when reviewer requirements call for them, so a `senior-developer` — which sets `disallowedTools: Agent` precisely so developers do not approve their own work ([AUTONOMY.md](../../docs/ai_workflow/AUTONOMY.md#workflow-roles)) — cannot run those subagents. In a manager-led session the manager or primary session runs step 2; the implementing agent runs steps 1 and 3.

## Steps
1. **`/verify-suite`** — full pytest + Chromium E2E gate. Must pass (modulo the known current red / historical flake in `e2e/CLAUDE.md` Gotchas) before continuing.
2. **Required reviewers** — combine applicable rows' reviewer requirements (a row's self-review alternative covers only that row's files); invoke required reviewers on the staged diff. A full-suite requirement does not add reviewers. Run `unslop-reviewer` only if the user explicitly requested it. Address every finding or document why it is deferred.
3. **`/handover`** — prepend a session block to `MASTER_HANDOVER.local.md`. If a milestone shipped, edit `docs/MASTER_HANDOVER.md` manually with new test counts and workstream status.

## Failure handling
- After a fix, rerun failing and affected checks. A required full gate must have passed against the final relevant code, tests, dependencies, and configuration; run it if that evidence is missing or invalidated. Documented baseline exceptions still govern.
- Do not skip to commit on partial success.

## Difference vs `/unslop`
`/unslop` is the **lighter** post-implementation gate — uses targeted tests instead of the full suite. Use `docs/ai_workflow/QUALITY_GATE.md` to choose the gate. The number of edited files alone does not select this full sequence.
