---
description: Update local handover scratch with current session state; optionally edit committed handover; at feature closeout, record the docs retention line.
---

Update the two handover layers: the gitignored `MASTER_HANDOVER.local.md` scratch,
and the curated committed [`docs/MASTER_HANDOVER.md`](../../docs/MASTER_HANDOVER.md).
The Steps below are the whole contract — there is no separate specification.

## Steps
1. Capture current state:
   - Run `git status --short --branch` and `git log -1 --oneline`.
   - Note the current TodoWrite list (if any) and the file/line you are mid-edit on.
2. **Prepend** a new dated block to `MASTER_HANDOVER.local.md` (do not overwrite or delete prior blocks). Block template:

   ```markdown
   ## YYYY-MM-DDTHH:MM
   - git status: <one-line summary>
   - last commit: <sha> — <subject>
   - in-progress edit: <file:line>
   - open todos: <list>
   - next step: <action>
   ```
3. Ask the user: "Update committed `docs/MASTER_HANDOVER.md` too? (y/N)" — default no.
4. If yes, open `docs/MASTER_HANDOVER.md` for manual edit; never auto-write to it. The committed handover is curated, not appended.
5. **Feature closeout only.** If this session completes or abandons the feature tracked by a `docs/<feature>/PLANNING.md`, append one line to that plan:
   `Docs retention at closeout: keep active | split | archive — <named files>; <current replacement source>; <reason>`.
   - Choose `archive` only for named, closed records that meet every [Archive Criterion](../../docs/ai_workflow/DOC_RETENTION.md#archive-criteria). Never move a file that a test, script or workflow reads, or a record deferred behind a named trigger, and never archive a whole shipped folder automatically.
   - `split` keeps the live text at its path and moves history verbatim to `docs/archive/<year>/<topic>/`.
   - The line moves nothing and approves nothing. Each `split` or `archive` is its own bounded change: `git mv`, never delete; open follow-ups and current constraints stay in the active tree; inbound references are repaired under the [Archive Procedure](../../docs/ai_workflow/DOC_RETENTION.md#archive-procedure). It grants no worktree, branch or ref retirement.
6. No Stop hook is wired — `/handover` stays manual until it proves low-noise.
