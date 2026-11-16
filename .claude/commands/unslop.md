---
description: Quality gate — diff → targeted tests → code-reviewer → unslop-reviewer → handover update.
---

Run the post-implementation polish gate. Which tests and reviewers a change needs is
canonical in [`docs/ai_workflow/QUALITY_GATE.md`](../../docs/ai_workflow/QUALITY_GATE.md);
the Steps below only sequence it.

## Steps
1. **Capture changed files**. Include staged, unstaged, and untracked files:
   - `git diff --name-only HEAD`
   - `git diff --name-only --cached`
   - `git ls-files --others --exclude-standard`
   - If a feature branch has an upstream/base, also include `git diff --name-only <merge-base>...HEAD`.
   - De-duplicate the list. If it is empty, stop.
2. **Targeted tests** — derive targeted tests from [`docs/ai_workflow/QUALITY_GATE.md`](../../docs/ai_workflow/QUALITY_GATE.md), using its change-type table, targeted-test derivation and frontend feature map. Run the union for all changed paths; use the more specific matching rule and the documented full-suite fallback when meaningful coverage cannot be derived. A local excerpt is guidance only and cannot replace or weaken that canonical routing. Preserve all mandatory reviewers and plan/owner gates.
   - Run via `/run-tests <files>` and `/run-e2e <specs>`; use `/verify-suite` where the canonical routing names it.
3. **`code-reviewer` agent**: invoke on the staged diff. Address every finding or document why deferred.
4. **`unslop-reviewer` agent**: invoke on the staged diff. Address every finding before commit; AI smells are not "preferences".
5. **`/handover`**: prepend a session block to `MASTER_HANDOVER.local.md` capturing what shipped + new test counts.

## When to use
- Before declaring a non-trivial change complete.
- Before opening a PR.
- Not for product-docs-only or comment-only changes — those go straight to `/handover`.
- For `.claude/**`, `CLAUDE.md`, folder `CLAUDE.md`, and `docs/ai_workflow/**`, do the manual dry-run/self-review from `QUALITY_GATE.md`; these files change agent behavior even though they are Markdown.

## When NOT to chain
- If targeted tests fail in step 2, stop and fix; do not let `code-reviewer`/`unslop-reviewer` review broken code.
- If the diff is purely product docs, skip steps 2–4; jump to step 5.
