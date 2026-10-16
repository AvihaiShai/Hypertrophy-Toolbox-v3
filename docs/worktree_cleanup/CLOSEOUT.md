# Worktree cleanup — closeout record

**Date:** 2026-10-16
**Authority:** owner closeout directive v2 (avihay1989@gmail.com), 2026-10-16.
**Outcome:** steps 1–6 complete and reviewed. **Step 7 (removal) did not run.** All 91 targets retained, nothing deleted.
**Preservation:** `C:\Users\aviha\Backups\Hypertrophy-Toolbox-v3\worktree-closeout-20261016-150200\`

---

## 1. Summary

The directive lifted the teardown hold for everything in `git worktree list`, granted gates
0/1/2 and the B/C/D approvals in one act, and told me to run to deletion autonomously.

Inventory, preservation, restore testing, plan publication and the single pre-deletion
review all completed. **Deletion itself is blocked by the installed guard**, which the same
directive forbids me to modify or bypass (§7 below). Nothing was removed, and no target was
left in a worse state than it started.

## 2. Scope as measured

`git worktree list` returns **92** entries: the main checkout plus **91** linked worktrees.
The directive's estimate of ~96 worktrees / ~139 branches / 8 stashes re-measured as
**91 / 139 / 8**, with **12** worktrees on detached HEADs (not ~16).

- **Protected, never a target:** `D:\development\Hypertrophy-Toolbox-v3-main`. It carries 23
  modified + 10 untracked files; these were left exactly as found and never staged.
  `git add -A` was never run.
- **Targets:** the 91 linked worktrees, all under `D:\development\`.
- **Out of scope:** 28 further entries under `D:\development\` that are not in
  `git worktree list` — including `Hypertrophy-Toolbox-v3-git-backups`,
  `Hypertrophy-Toolbox-cleanup-planning`, the `ht-opa-*` lanes and several loose files. Per
  §1.A the command output *is* the scope.
- **Branch scope:** 139 local branches = 1 (`main`) + **79** checked out in a target + **59**
  unattached. Branch deletion was restricted to the 79; the 59 unattached are outside the
  authorized scope and were not considered, including 4 that are ancestors of `origin/main`
  and would have been deletable. That is the conservative error.

### Merge baseline

`origin/main` = `71fc658`, after a fresh `git fetch --prune` (which also pruned 5 deleted
remote branches). Local `main` = `85e2372` is **diverged**: 3 ahead, 41 behind. Local `main`
was therefore *not* used as the baseline — doing so would have misclassified 41 commits'
worth of already-merged work as unmerged.

## 3. Classification of all 91 targets

| verdict | count |
|---|---|
| removal-eligible, tip preserved, no unique local state | 87 |
| removal-eligible, tip preserved, unique local state captured | 4 |
| ineligible on preservation, fidelity or activity grounds | 0 |
| branch also deletable (merged into `origin/main`, exact tip preserved) | 9 |
| branch kept (unmerged or uncertain) | 70 |
| branch n/a (detached HEAD) | 12 |

### The 9 branches that qualified for deletion

Each independently confirmed: `git merge-base --is-ancestor <tip> origin/main` succeeds,
0 commits ahead of `origin/main`, and the branch tip equals the captured HEAD OID exactly.

`wt/deepgate-0831-monitor`, `docs/worktree-cleanup-replacement-20260904`,
`fix/npm-audit-colord-js-yaml-20260910`, `docs/js-ledger-56-64`,
`diag/linux-visual-gate1-diag-20260901`, `docs/optional-css-status-reconcile-20260901`,
`wt/opt-wp-audit`, `wt/optional-css-audits-publish`, `docs/u2-ledger-rows-20-21`.

Measured caveat: `git branch -d` deletes only what is merged into `HEAD` *or* into the
branch's upstream. 5 of these 9 have an upstream whose remote-tracking ref no longer exists
**and** tips not contained in local `main`, so `-d` will refuse them. Real yield is **~4 of
9**; the rest fail safe (branch kept) and the script logs the refusal. Forcing them would
need `-D`, which is both denied by the guard and less safe.

### The 4 targets with unique local state (all captured)

| worktree | unique paths |
|---|---|
| `HT-p1-measure` | `pyright.json`, `pyright.stderr.txt` |
| `ht-wt-opt-reval-20260902` | `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md`, `docs/worktree_cleanup/PLANNING.md`, `scripts/worktree_cleanup_audit.py`, `tests/test_worktree_cleanup_audit.py` |
| `ht-wt-theme-align-20260830` | `static/css/components.css`, `static/js/darkMode.js`, `static/js/theme-init.js` — all three **staged** |
| `…main-ledger2223` | `artifacts_check.md` |

The local `docs/worktree_cleanup/PLANNING.md` lineage is captured to the backup. It was
**not** reconciled against the committed lineage and **not** committed, per §1.G.

The five files that appear modified in nearly every worktree
(`.claude/commands/status.md`, `.claude/commands/worktree.md`,
`.claude/hooks/guard-destructive-command.ps1`, `docs/WORKTREE_CLEANUP_PLAN.md`,
`docs/ai_workflow/PARALLEL_WORKFLOW.md`) are the *same* edits propagated across trees and
identical to the main checkout's uncommitted set — not unique work. Captured regardless.

## 4. Preservation

Destination is on volume `C:`; every target is on `D:` — outside all deletion targets and on
a different volume. Total **1.9 GB**.

- **`all-refs.bundle`** — 367 MB. `git bundle verify`: *"The bundle records a complete
  history."* Bundle ref count **359** = 267 repo refs + main `HEAD` + all 91
  `worktrees/<name>/HEAD`. Source refs missing from the bundle: **0**.
- **40 reachability pins**, created *before* bundling because a plain `--all` bundle misses
  detached HEADs and all but the top of the stash reflog:
  `refs/closeout/20261016-150200/detached/<name>` for each of the 12 detached worktrees, and
  `.../stash/<0-7>` plus `.../stash/<n>-p<k>` for all 8 stash commits and their 20 parents.
  (`refs/stash` exposes only `stash@{0}`; `stash@{1..7}` live solely in that ref's reflog.)
- **`p/001..091/`** — per-target payload: every modified, staged, untracked **and** ignored
  user-bearing file. **16,300 files.** Slots are numbered rather than named to keep paths
  under MAX_PATH; `p/index.tsv` maps slot → worktree path + HEAD OID.
- **`p/<slot>/staged/`** — staged blobs extracted with `git cat-file`. A staged blob is
  referenced only by the index, never by a ref, so `git bundle --all` does **not** contain
  it; 4 such blobs would otherwise have been lost silently.
- **`git-state/`** — all 91 `.git/worktrees/<name>/` directories (HEAD, index, ORIG_HEAD,
  reflogs), the main `.git/logs/` reflogs, and main's `HEAD`/`ORIG_HEAD`/`packed-refs`/
  `config`/`index`/`refs`.
- **`MANIFEST.txt`** — SHA-256 of every file in the destination: **17,913 files, 0 errors.**
- **`evidence/`** — ref snapshots, bundle ref list and diff, worktree porcelain, stash list,
  `branch -vv`, detached tips, stash pins, restore and fidelity logs, the all-tranche
  recheck output, `inv/` (inventory + classification + tranches) and `scripts/` (every
  script used, including the removal mechanics). The inventory and scripts are stored here
  so the run does not depend on a session scratchpad.

§7 preservation **breadth** was applied. §7 **ceremony** was waived per §1.D: no
owner-captured runtime map, no freeze budget, no manifest-with-OIDs, no operation lock, no
archive ref.

## 5. Restore test

Restored into an isolated scratch directory from a copy of the bundle taken out of the
backup, with no dependency on the live repository.

**Git side — PASS.** Isolated bundle SHA-256 identical to the in-backup copy. `git fsck
--full` clean. 267 source refs checked: **0 objects absent, 0 work refs unrestored** (224
non-codex refs restored by name; 43 `refs/codex/...` restored under remapped names with
OIDs verified present). **91/91** per-worktree HEAD objects present. All 12 detached tips
fully readable via `git archive` (which forces every tree and blob): ~1,800 files / 130 MB
each. All 8 stash commits **and all 20 parents** fully readable, including the
untracked-file parents. Real materialisation to disk: `stash@{0}` → **1,794 files**, a
detached tip → **1,827 files**.

**Payload — PASS.** 91 slots restored out of the backup and verified against their SHA-256
manifests, 0 hash failures.

**Capture fidelity vs live source — PASS.** Every captured working-tree file re-hashed
against the file still live in its worktree. The final verification, run after the gap
capture in §6, re-hashed **all 16,300 captured files across all 91 targets** with **0
mismatches and 0 missing** (`evidence/recheck-all-tranches.txt`: retained=0 for all ten
tranches). This is the check that proves the backup represents the sources rather than
merely being self-consistent, and it can only run while the sources still exist.

### Restore-harness defects found and corrected

1. `git fetch 'refs/*:refs/*'` **aborts atomically on Windows** against this repo: 43
   `refs/codex/turn-diffs/checkpoints/<hash>/<hash>/<ts>/<uuid>` refs are 150 characters, and
   a 155-character loose-ref destination prefix puts them past MAX_PATH. The source repo only
   holds them *packed*, so the problem appears solely on restore. Any future restore must
   fetch namespaces selectively, flatten `refs/codex/*`, or use a very short destination.
   **The bundle itself is unaffected.**
2. `sha256sum` on this host emits binary-mode `<hex> *<path>`, not `<hex>  <path>`. A checker
   that splits on two spaces silently compares **zero** files and still reports success. The
   first fidelity run did exactly that and produced a vacuous pass; only the corrected run is
   cited above.

## 6. Review and the findings it produced

One independent read-only review ran once, before any deletion, per §3 and §6. It returned
**3 blocking findings, all legitimate.** All three are fixed and each fix was verified.

**B1 — ten user-bearing documents were not in the backup.** The original capture filtered
ignored files to `data/`, `artifacts/`, `logs/`, `.env*` and `*.db*`. `.gitignore` ignores
`MASTER_HANDOVER.local.md` and `WORKSTREAM_OWNERSHIP.local.md`, which match none of those
globs; `git status --porcelain` does not list ignored files at all, so they fell through both
lists. 10 such files existed across 10 targets (254 B–4,466 B), carrying session handovers
and released-claims logs with merge evidence. **This was a real gap in my own work and would
have destroyed 10 unique documents.** Fixed generically rather than by whitelisting
`*.local.md`: the capture now takes every untracked-or-ignored file that is not a regenerable
cache. 1,853 files (1.48 MB) were added — the 10 documents, 1,841 Hypothesis
property-test cache files and 2 pytest sentinels; all 1,853 were captured rather than
judged. Verified: gap re-measures at **0**, all 10 documents are in `MANIFEST.txt` with
hashes matching the live files, and the 28 affected slots re-verify at 13,045 files with 0
backup-hash and 0 live mismatches.

**B2 — the junction-unlink step failed open.** `rmdir` failure was logged and ignored, and a
failed *detection* was reclassified as "real directory, leave it for git", both ending in a
forced recursive delete with a live junction still present. Fixed: detection moved into
`evidence/scripts/escaping-reparse.ps1`, which reports every reparse point whose target
resolves outside the worktree and **exits 2 on scan failure**; the caller retains on a
non-zero exit, on a non-empty result, and after a post-unlink re-scan. Verified against
three controls — positive (returns exactly the escaping junctions), negative (silent), and
fail-closed (exit 2 on a missing root). Fixing this exposed two further bugs of my own: the
first detector returned **empty for worktrees that do have escaping junctions** (bash mangled
the inline PowerShell backslash path), and `Write-Error` under `$ErrorActionPreference='Stop'`
threw before `exit 2`, so the fail-closed code never fired.

**B3 — the recheck could not see a newly created ignored file.** `status --porcelain` without
`--ignored` omits ignored paths, and a path absent from the manifest was never iterated, so a
`data/database.db` written after capture would have been deleted unbacked. 47 of 91 targets
carry `data/database.db` and one capture includes four `data/auto_backup/database_202608*.db`
program backups, so the exposure was real. Fixed: the recheck re-enumerates with two
independent passes and blocks on anything not already captured. Verifying this fix found two
more of my own bugs: `git ls-files --others` **under-reports ignored trees** (2,530 paths
against the 10,631 my `find` saw), so it is not a usable superset and both enumerations are
now required; and my first gap measurement **silently skipped git-quoted non-ASCII paths**
(`"...\303\274..."`), because an existence test on the escaped string always fails — now
fixed with `core.quotePath=false`. The hardened gate initially produced a false retain on the
largest target by comparing 1,223 intra-tree symlinks against a capture that only ever copied
regular files; it now compares regular files only. Verified: all ten tranches recheck with
**retained=0**.

## 7. Why step 7 did not run

`.claude/hooks/guard-destructive-command.ps1`, wired to both `Bash` and `PowerShell` in
`.claude/settings.json`, returns an unconditional `deny` for:

| operation | guard behaviour |
|---|---|
| `git worktree remove` | denied outright (~line 962) |
| `git branch -d` / `-D` | denied outright (~line 966) |
| `git worktree prune` | denied unless provably a dry run (~line 942) |

These checks sit **above** every profile check and above the generic dry-run exemption, and
the guard's own comment states the hold is *"neither mode-dependent nor profile-dependent"*.
There is no compliant invocation of either removal primitive.

Directive §1.A authorizes exactly these operations. Directive §1.E forbids modifying or
bypassing the guard, and §6 forbids changing prevention tooling. Those instructions are in
direct conflict, and I did not resolve it by editing or circumventing the guard.

Deleting only the directories was considered and **rejected as strictly worse than doing
nothing**: it would leave 91 broken registrations in `git worktree list` with real
`git worktree prune` also denied — a less clean end state than today, and the opposite of
the directive's definition of done.

`git worktree prune --dry-run` (which the guard does permit) reports **nothing prunable**:
all 91 registrations have live directories, so there were no stale registrations to inspect.

**This is the one decision that needs the owner.** Everything else is finished; removal is a
mechanical run of `evidence/scripts/step7_remove.sh` per tranche once the denial is lifted.

## 8. Junction hazard — the load-bearing removal detail

A full recursive scan of the 91 targets finds **1,097 reparse points**. An early
depth-limited scan reported only 115 and was wrong.

Of those 1,097, exactly **113 point outside their own worktree**, and all 113 are:

| name | count | target |
|---|---|---|
| `node_modules` | 60 | `D:\development\Hypertrophy-Toolbox-v3-main\node_modules` |
| `.venv` | 53 | `D:\development\Hypertrophy-Toolbox-v3-main\.venv` |

**Every junction that escapes its worktree points into the main checkout.** Any recursive
delete that follows one destroys the main checkout's Python or Node toolchain. Three
worktrees have a *real* `node_modules` directory rather than a junction.

The remaining **984 are self-contained** — targets resolve inside their own worktree — so
removing a worktree destroys only its own content. Nearly all are pytest tmpdir symlinks
under `artifacts/`. The 12 with alarming names (`.git` ×4, `dangling-link` ×4, `redirected`
×2, `*.lock` ×2) are all pytest fixtures inside one worktree
(`Hypertrophy-Toolbox-npm-audit-fix\artifacts\t1\pytest-of-aviha\pytest-0\test_*`) from the
guard's own reparse-point test suite — not real git directories and not real locks.

This measurement is what makes the mechanics safe rather than merely careful: the removal
unlinks **every** escaping reparse point (not a hardcoded two names), then asserts none
survives before deleting, failing closed if the scan itself fails. Unlinks use
`cmd /c rmdir` — link only, target untouched — never `rm -rf`, never from inside a junction.

The capture pruned `.venv`, `node_modules` and `.git` from every `find`, so nothing traversed
them.

## 9. Retained targets

**All 91**, for one shared reason: the guard denies the removal primitive. No target was
retained for a preservation, fidelity or activity reason — all 91 pass the hardened recheck
(`retained=0` across all ten tranches).

Four are additionally flagged for ordering: `ht-lane-sol-20260929`, `ht-wt-457-merge-opus`,
`ht-wt-462-opus` and `ht-wt-463-opus` are the `opus`/`sol` parallel lanes driven by an owner
"next batch" trigger, with 0/11/2/4 unpushed commits (all tips pinned and bundled). No live
process, lock, WAL/SHM file or recent write was found for any of them, and they were ordered
last (tranches 9–10). **Removing them retires the directories that the standing "next batch"
trigger drives — that is a workflow decision for the owner, not a data-loss risk.**

## 10. Accepted risks

Recorded, not fixed, per the directive's severity rule.

- **The process-based activity check is near-vacuous on Windows.** No process on this machine
  has an image path under `D:\development\*`, because every interpreter resolves through the
  `.venv` junction into the main checkout or to `C:\Program Files\nodejs\`. A live Flask app
  or pytest run inside a target would be invisible to it. Inactivity rests instead on: no
  `index.lock`, no SQLite `-wal`/`-shm` outside stale pytest fixtures, and no file written in
  the last 60 minutes — all three now enforced in the recheck.
- The recheck is **not atomic** with the removal: a write landing between recheck and
  `git worktree remove` is undetectable. Inherent to a shared checkout.
- Whether `git worktree remove --force` follows a Windows directory junction during recursive
  deletion is **not settled** — determining it requires running the denied primitive. The
  mechanics are written so the answer does not matter: nothing escaping survives the assert.
- The largest target (real `node_modules`, 10,631 ignored files, 982 reparse points) is the
  most likely `remove --force` partial failure on MAX_PATH; outcome would be a half-deleted
  tree with a live registration, not loss, since its payload is captured.
- Two file counts circulate legitimately: 16,300 captured files vs 16,296 compared for
  fidelity — the 4 extracted staged blobs have no working-tree twin by definition.
- 1,841 of the files added by the B1 fix are Hypothesis test cache, captured without
  judgement rather than filtered. Harmless over-capture (1.48 MB).
- `docs/worktree_cleanup/` is listed in `.gitignore`, but `CLOSEOUT.md` is not ignored and
  `origin/main` already tracks two files in that directory, so this record commits normally.

## 11. Waived for this cleanup

Recorded as **waived, not completed and not passed**, per §1.C: the three VS Code capture
sessions, the scheduled-task calendar firing, the loaded-source coverage review, the G07
decision, and every Gate A row. Operation A qualification and monitoring were neither run nor
waited on. §7 preservation ceremony waived per §1.D. The August-backup attribution
investigation stayed closed per §1.F; the 14,255-entry manifest was not re-walked.

## 12. Staying parked

Operation E / main reconciliation, `docs/worktree_cleanup_amendment/`, Operations F and G,
`D:\c` and `D:\d`. The drive-root audit was left exiting non-zero, as intended. The two
`PLANNING.md` lineages were not reconciled and the local one was not committed.

## 13. Contradictions between the documents and this directive

Per §2, `docs/worktree_cleanup/` (≈2,800 lines across `PLANNING.md`, `STATUS.md`,
`AMENDMENT_2026-09-28.md`, `PROVENANCE_RECOVERY_OPTIONS.md`) is treated as history. Its open
"OWED" items, Gate A rows and decisions 1–5 were not re-derived or re-litigated. The one
contradiction that mattered operationally is in §7: the installed guard still enforces the
worktree-retention hold that §1.A lifts.

## 14. Not done, by instruction

No `git gc`, no `git reflog expire`, no object pruning, no branch pushes of target branches,
no remote-ref deletion, no backup deletion. No pytest, E2E or visual suites — this was git
housekeeping, not a code change. No application code, prevention tooling or repository policy
changed. No new planning packet, amendment, status document, options memo or ADR was created;
this file is the single record.
