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
- **Read historical blobs safely on Windows.** Do not disable MSYS path
  conversion. Avoid passing `<revision>:<path>` across a Git Bash/MSYS boundary;
  resolve the path to an object ID first, then read that ID:
  ```powershell
  $blob = @(git ls-tree -r --full-tree --format='%(objectname)' <revision> -- <path>)
  if ($blob.Count -ne 1) { throw "Expected exactly one blob, found $($blob.Count)" }
  git cat-file blob $blob[0]
  ```
  Independently verify any unexpected absence.
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
   any document that needs correcting, and any stale worktree or branch worth
   retiring.
7. **Stop.** Do not begin a packet until the owner confirms the table.

## Permissions
This command needs `gh pr list`, `gh pr checks`, `git fetch` and `git -C …
status`. If any prompt for approval, that is expected on first run — approve
them once rather than narrowing the reconciliation.
