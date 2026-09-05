---
description: Reconcile every status-claiming document against git/PR ground truth and print a drift table. Read-only; never starts work.
---

Establish where the work actually stands **before** any packet is dispatched.

Agents have twice been sent at work that was already done — WP3.5 (shipped, but
the plan doc carried no completion note) and WP4.3g (duplicated while an open PR
existed). This repo keeps **three** documents that each claim to describe
current state, and they drift apart from each other and from git. Treat all
three as claims to be checked, never as the answer.

## Rules
- **Disk beats memory.** Session memory, handover docs, `ACTIVE_DEVELOPMENT.md`
  and every `*_EVIDENCE.md` are claims. `git` and `gh` are the evidence.
- **The plan doc is the plan.** Determine the next step from the canonical plan
  and the active feature's `PLANNING.md`. Never infer it from an evidence doc —
  those record what happened, not what is next.
- **Read-only.** This command edits nothing, pushes nothing, starts nothing.
- **Read historical blobs safely on Windows.** Do not disable MSYS path conversion.
  Use PowerShell and separate arguments; require exactly one full blob OID:
  ```powershell
  $blob = @(git ls-tree -r --full-tree --format='%(objecttype) %(objectname)' HEAD -- scripts/new-worktree.ps1)
  if ($LASTEXITCODE -ne 0 -or $blob.Count -ne 1 -or $blob[0] -notmatch '^blob ([0-9a-f]{40}|[0-9a-f]{64})$') { throw 'Expected exactly one full blob OID' }
  $blobOid = $Matches[1]
  git cat-file blob $blobOid
  ```
  Native output paths must be drive-qualified; independently verify any absence.
- **Scope the table.** Do not attempt to re-verify every historical packet;
  `git log -20` cannot substantiate a claim about a packet from three months
  ago. Cover packets that are active, ongoing, owner-gated, or proposed-next,
  then look up SHAs and PRs for exactly those.

## Steps
1. Ground truth:
   ```
   git status --short --branch
   git fetch --quiet origin
   git log --oneline -20
   git log --oneline origin/main..HEAD      # local-only commits
   git log --oneline HEAD..origin/main      # unpulled commits
   git worktree list
   git branch -a --format='%(refname:short) %(upstream:track)'
   gh pr list --state open --limit 20 --json number,title,headRefName,isDraft,mergeStateStatus,reviewDecision
   ```
2. For **each** worktree from `git worktree list`, check whether it holds
   uncommitted or unintegrated work — `git worktree list` alone will not show
   this:
   ```
   git -C <worktree> status --short --branch
   git -C <worktree> log --oneline origin/main..HEAD
   ```
3. For any open PR that a packet depends on, establish whether it is actually
   mergeable — draft state and check results, not just existence:
   ```
   gh pr checks <number>
   ```
4. Read the status-claiming documents and record **what each one asserts**,
   without adopting any of them:
   - `docs/REFACTOR_PLAN.md` — shipped-packet table near the top, and the
     **Owner review status table** near the bottom.
   - `docs/MASTER_HANDOVER.md` — CLAUDE.md calls this canonical; it has
     nonetheless carried self-contradictory sections.
   - `docs/ACTIVE_DEVELOPMENT.md` — declares itself the execution source of
     truth for autonomous sessions.
   - The active feature's `PLANNING.md`. Find it rather than assuming a path.
     Identify it from what the live state already points at — the plan doc's
     Ongoing row, the open PR's branch and body, and the handover's current
     block usually name it outright. Only fall back to recent history
     (`git log --diff-filter=AM --name-only -15 -- 'docs/**/PLANNING.md'`) if
     none of those resolve it; a long-running plan may not have been touched in
     the last commits, so recency alone can point at the wrong document.
5. Print one table, most-actionable first:

   | Packet | Claimed by (doc → status) | Git evidence (SHA / PR / worktree) | DRIFT | Next action |

   Raise **DRIFT** for any of: a doc claim with no git evidence; shipped work no
   doc records; two documents that disagree with each other; or a packet with a
   worktree or open PR that the docs describe as not started.
6. Close with: the single next step, every owner gate standing in front of it,
   any document that needs correcting, and the lifecycle rows requiring owner
   review. Run `scripts/audit-worktrees.ps1` with the owner's explicit repository,
   development parent, annotation and dated drive-root baseline paths. Include
   MERGED/CLOSED/OVERDUE/OWNERLESS/ORPHANED_ANNOTATION/UNRESOLVED rows; unavailable
   activity or stale PR metadata remains UNKNOWN. Audit stdout is read-only.
   Retain worktrees and recovery roots under the signed cleanup-sequence hold;
   no status, age or disposition authorizes teardown.
7. **Stop.** Do not begin a packet until the owner confirms the table.

## Permissions
This command needs `gh pr list`, `gh pr checks`, `git fetch` and `git -C …
status`. If any prompt for approval, that is expected on first run — approve
them once rather than narrowing the reconciliation.
