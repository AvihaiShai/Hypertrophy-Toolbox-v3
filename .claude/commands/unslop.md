---
description: Quality gate — diff → applicable tests → required reviewers → handover update.
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
2. **Required checks** — run every gate `QUALITY_GATE.md` requires for the diff (tests via `/run-tests <files>` and `/run-e2e <specs>`, plus the non-test gates its rows and blocking-CI section name).
3. **Required reviewers** — combine applicable rows' reviewer requirements (a row's self-review alternative covers only that row's files); invoke required reviewers on the staged diff. Run `unslop-reviewer` only if the user explicitly requested it. Address every finding or document why it is deferred.
4. **`/handover`**: prepend a session block to `MASTER_HANDOVER.local.md` capturing what shipped + new test counts.

## When to use
- Before declaring a non-trivial change complete.
- Before opening a PR.
- Not for product-docs-only or comment-only changes — those go straight to `/handover`.
- For `.claude/**`, `CLAUDE.md`, folder `CLAUDE.md`, and `docs/ai_workflow/**`, do the manual dry-run/self-review from `QUALITY_GATE.md`; these files change agent behavior even though they are Markdown.

## When NOT to chain
- If targeted tests fail in step 2, stop and fix; do not send broken code to reviewers.
- If the diff is purely product docs, skip steps 2–3; jump to step 4.
