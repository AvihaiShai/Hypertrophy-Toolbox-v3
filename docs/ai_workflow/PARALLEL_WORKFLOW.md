# Parallel Workflow

*How to run more than one Claude (or any concurrent dev) on this repo without corrupting state. This file is the canonical authority for checkout and DB isolation — [AUTONOMY.md](AUTONOMY.md#workflow-roles) defers to it for the tracked-DB commit rule. Path claims live in [WORKSTREAM_OWNERSHIP.md](WORKSTREAM_OWNERSHIP.md).*

## Why this exists

The app uses SQLite. `app.py` enables WAL mode in non-debug runs ([utils/database.py:90](../../utils/database.py#L90)) and the auto-backup task snapshots `data/database.db` at startup ([utils/auto_backup.py](../../utils/auto_backup.py)). Two parallel checkouts pointing at the same DB file will:

- Race on WAL/SHM sidecars and risk corruption.
- Stomp each other's `data/auto_backup/` snapshots.
- Produce non-deterministic test runs when one agent's seed pollutes another's.

The fix is **one DB per checkout**, achieved via `git worktree`.

## When to fork

Fork when any of these is true:
- Two agents will edit the working tree at the same time.
- One agent will run the dev server or pytest while another agent edits unrelated code.
- An experiment will leave `data/database.db` in a state you don't want to keep.

Don't fork for:
- Single-agent sequential work — the main checkout is fine.
- Docs-only edits that don't touch `data/`.

## Manager-session ownership

One manager-led feature owns one checkout. For sequential work, launch the manager in
the main checkout. Before starting a second feature concurrently, create its isolated
checkout first and launch a separate manager session there. Subagents operate inside
their parent manager's checkout; the manager does not create, merge, or move
worktrees.

## Forking — the short version

```powershell
.\scripts\new-worktree.ps1 -Task <slug> [-Seed visual|empty|copy-current] [-OpenTerminal]
```

The script:
1. `git worktree add -b wt/<slug> ..\Hypertrophy-Toolbox-v3-<slug> HEAD`.
2. Creates `data/` and `data/auto_backup/` in the new worktree.
3. Seeds `data/database.db` per `-Seed`. Defensive — warns and skips if the source is missing rather than aborting.
4. Optionally opens a Windows Terminal tab in the worktree (`-OpenTerminal`).

See [`.claude/commands/worktree.md`](../../.claude/commands/worktree.md) for the seed-mode table and the per-worktree-never-shared list.

## Python environment

`.venv/` is gitignored, so a new worktree starts without one. Two options:

- Fresh venv (slowest, fully isolated):
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\pip.exe install -r requirements.txt
  ```
- Symlink to the main checkout's venv (fast; works because the venv is read-only at runtime):
  ```powershell
  New-Item -ItemType SymbolicLink -Path .venv -Target ..\Hypertrophy-Toolbox-v3-main\.venv
  ```
  Requires admin or Developer Mode on Windows.

## DB isolation rule

**Each worktree owns its own `data/database.db`.** Do not symlink it; do not point a second worktree at the same file via `DB_FILE`. Even read-only access from a second process can disrupt WAL recovery.

Auto-backups land in the worktree's own `data/auto_backup/`. They never need to be merged across worktrees — they are throw-away local snapshots.

### Why the script applied `--skip-worktree`

**Historical, and no longer in force.** `data/database.db` used to be tracked, so
`git worktree add` checked HEAD's copy out into the new worktree before the seed step ran,
and the script then called `git update-index --skip-worktree data/database.db` *inside the
new worktree only* to hide subsequent seed writes from `git status`.

Measured 2026-08-13: the file is **untracked and ignored** — `git ls-files data/` returns
only `catalog.seed.db` and the two CSVs, and `git check-ignore -v data/database.db`
resolves to `.gitignore:29 *.db`. `scripts/new-worktree.ps1` already accounts for this.
A `git ls-files -v data/database.db` check therefore returns nothing and cannot be used as
evidence of anything.

### Tracked-DB commit rule

Only one workstream at a time may prepare a deliberate `data/database.db` change, and
only the repository owner may commit it from the main checkout. Feature worktrees may
copy and mutate their isolated DB for development or verification, but must never
stage or commit that binary. Do not undo `--skip-worktree` in a feature worktree to
bypass this rule. Coordinate the exceptional owner-led DB commit before making it so
no other workstream is preparing one concurrently.

The root cause — that `data/database.db` should not have been tracked at all — has since
been addressed; it is untracked and ignored today. The commit rule above still stands for
the exceptional case where the owner deliberately prepares a DB change from the main
checkout.

## Conflict avoidance

- Read [WORKSTREAM_OWNERSHIP.md](WORKSTREAM_OWNERSHIP.md) before claiming files.
- Put your live claim in `MASTER_HANDOVER.local.md` (gitignored) or in a local `WORKSTREAM_OWNERSHIP.local.md` (also gitignored). The committed `WORKSTREAM_OWNERSHIP.md` is rules + template only — keeping live rows out of git avoids merge churn on every claim/release.
- Coordinate explicitly on the **never-claimed shared paths**: `app.py`, root [`CLAUDE.md`](../../CLAUDE.md) and folder-level `CLAUDE.md` files, [`.claude/settings.json`](../../.claude/settings.json), [`docs/MASTER_HANDOVER.md`](../MASTER_HANDOVER.md), [`.gitignore`](../../.gitignore).
- If two worktrees both need to edit a claimed glob, finish one branch and rebase the other.

## Merging back

Standard PR flow. Push the `wt/<slug>` branch, open a PR, let CI run, merge into `main`. Then:

```powershell
git worktree remove ..\Hypertrophy-Toolbox-v3-<slug>
git branch -d wt/<slug>
```

`git worktree remove` refuses if the worktree has uncommitted changes — that's intentional. Investigate before forcing.

## Failure modes to expect

- **Stale `wt/` branches** — `git worktree list` shows all active checkouts. `git worktree prune` clears orphaned admin entries after a manual directory delete.
- **DB schema drift** — if you fork from an older HEAD and the main DB has new tables, `app.py` startup runs the table-creation helpers idempotently; the worktree's DB will catch up on first launch.
- **Auto-backup spam** — every worktree creates its own startup snapshot. Periodically clear `data/auto_backup/` per worktree.
- **Visual fixture missing** — `.gitignore` whitelists `e2e/fixtures/database.visual.seed.db`, so it should be in tree. If it isn't, the seed step warns and skips; either regenerate the fixture or pass `-Seed empty`.

## See also

- [`.claude/commands/worktree.md`](../../.claude/commands/worktree.md) — slash command.
- [WORKSTREAM_OWNERSHIP.md](WORKSTREAM_OWNERSHIP.md) — path-claim rules.
- [`CLAUDE.md`](../../CLAUDE.md) §3 — `FLASK_USE_RELOADER=0` rationale (same WAL hazard).
