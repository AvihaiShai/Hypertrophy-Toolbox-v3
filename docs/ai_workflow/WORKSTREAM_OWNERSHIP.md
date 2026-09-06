# Workstream Ownership

*Advisory path-claim rules for parallel Claude instances. Solo dev — claims are coordination hints, not enforced. This file is the canonical authority for path claims; the checkout and DB isolation those claims assume live in [PARALLEL_WORKFLOW.md](PARALLEL_WORKFLOW.md).*

## Where live claims go

**Do not put live claims in this file.** This committed doc is rules + template only; live ownership rows would create merge churn on every claim/release.

Put live claims in one of:
- `MASTER_HANDOVER.local.md` — append a claim block under the current session entry (gitignored).
- `WORKSTREAM_OWNERSHIP.local.md` — gitignored sibling of this file, dedicated to claims (see [`.gitignore`](../../.gitignore)).

## Active claims (template)

Copy this block into your local file, fill in the rows, delete rows when done.

```markdown
## Active claims
| Path glob | Workstream | Owner instance | Worktree | Started |
|---|---|---|---|---|
| `routes/workout_plan.py`, `templates/workout_plan.html` | fatigue badge slot | claude-A | Hypertrophy-Toolbox-v3-fatigue-badge | 2026-05-11 14:00 |
```

## Rules

1. Before editing files matching a claimed glob, check the local claim file in the worktree(s) you know about.
2. If you must edit a claimed path, note it in `MASTER_HANDOVER.local.md` and coordinate — rebase, pair, or wait.
3. Release a claim by deleting the row from the local file (nothing to commit).
4. **Never-claimed shared paths** (coordinate per-edit, not via claims):
   - `app.py`
   - root [`CLAUDE.md`](../../CLAUDE.md) and any folder-level `CLAUDE.md`
   - [`.claude/settings.json`](../../.claude/settings.json), and everything else under [`.claude/`](../../.claude/) — commands, agent charters, hooks, and skills
   - [`docs/MASTER_HANDOVER.md`](../MASTER_HANDOVER.md)
   - [`.gitignore`](../../.gitignore)
5. **Per-worktree, never shared** (do not claim — they are isolated by construction):
   - `data/database.db` and its `-wal` / `-shm` sidecars
   - `data/auto_backup/`
   - `MASTER_HANDOVER.local.md`
   - `.venv/`

## Claim granularity

- Prefer file globs over folder-level claims. `routes/workout_plan.py` is a claim; `routes/**` is a foot-gun.
- A single workstream can hold multiple claims — list them as separate rows.
- Reviewer-only edits (proofreading, comments) don't need a claim; coordinate verbally.

## Lifecycle annotations (Operation A)

The Git main checkout's `docs/ai_workflow/WORKSTREAM_OWNERSHIP.local.md` contains
ordinary claim/history prose and exactly one fenced `json` block. Schema version 1
has `records`; each record has these fields:

| Field | Contract |
|---|---|
| `identity`, `path` | Exact ordinary worktree path plus NTFS volume serial:file ID from `Get-WorktreePathIdentity`; never a wildcard/prefix identity. |
| `owner`, `task`, `branch` | Accountable owner, work description, exact short branch (empty for detached). |
| `createdAt`, `expectedPr` | ISO-8601 creation timestamp and PR number, or null when unassigned. |
| `teardownCondition`, `nextReviewDate` | Retention/next condition and future ISO-8601 review timestamp. |
| `disposition`, `rationale` | ACTIVE, KEEP, DEFERRED, COMPLETED or ABANDONED; an acknowledgment needs a rationale and future review. None grants deletion. |
| `activity`, `activityObservedAt` | Observed activity and its ISO-8601 timestamp; older than 24 hours becomes UNKNOWN. A claim is not proof of no active process. |

`audit-worktrees.ps1` derives registration from NUL-delimited Git output, verifies
Git common/admin relationships and scans only direct development-parent entries
without following reparses. Missing annotations are OWNERLESS/activity UNKNOWN;
stale identities remain ORPHANED_ANNOTATION, physical disagreements UNRESOLVED.
Neither annotations nor PR metadata can waive a physical mismatch.

Optional private PR metadata schema 1 contains `observedAt` and `records` with
`number`, `state` (OPEN/CLOSED/MERGED), `headRefOid`. Only a single exact PR-number
and full HEAD match within 24 hours contributes triage; otherwise state is UNKNOWN.
Merged/closed/overdue rows need explicit owner acknowledgment before new creation.

Drive baseline schema 1 contains `approvedBy`, `approvedAt`, `developmentParent`,
and `roots`: each exact root has `path` and `children` containing exact `path` and
`identity`. The owner reviews dated direct-child identities before approving a
baseline. Missing approval/baseline and identity drift are blocked/unknown; unexpected
children are only reported. Audits emit JSON to stdout and never change annotations,
Git, databases, environments or baseline. Redirection must use explicit scratch output.

Creation validates environment/lifecycle/collisions, creates Git state, publishes the
validated seed (or verified empty mode), verifies target DB/log launch resolution,
then writes the final annotation under a short exclusive `.lock` file handle with
atomic replacement. Concurrent writers re-read under the lock to avoid lost updates.
Failures before final annotation retain the registered worktree as OWNERLESS; review
the retained temporary annotation/seed evidence. Lock-file presence alone is no lock.
There is no cross-resource transaction or automatic rollback/removal.

During the signed sequence, completed/abandoned/KEEP/DEFERRED developments retain
worktrees, branches, detached/archive refs, reflogs and local-only recovery roots.
Normal development may advance branches and append reflogs; retirement requires
separate operation authority. See [owner acceptance](../worktree_cleanup/OPERATION_A_OWNER_ACCEPTANCE.md)
for the proposed installation/monitoring choices and disposable Windows procedure.

## Related guides

- [PARALLEL_WORKFLOW.md](PARALLEL_WORKFLOW.md) — when to fork, DB isolation rule.
- [`.claude/commands/worktree.md`](../../.claude/commands/worktree.md) — how to fork.
- `MASTER_HANDOVER.local.md` — preferred home for live claims.
