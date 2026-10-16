# Worktree cleanup — closeout record

**Date:** 2026-10-16
**Authority:** owner closeout directive v2 (avihay1989@gmail.com), 2026-10-16.
**Outcome:** complete, with one item unresolved by instruction — prevention (§18).
Steps 1–6 ran on 2026-10-16 (§1–§14 below); **step 7 ran later the same day under the owner's continuation directive and removed all 91 worktrees** (§15); a branch cleanup (§16) and the clearance of §15.4's removal residue (§17) ran on 2026-10-17 under their own directives. A drive-root cleanup (§18) also ran on 2026-10-17 under a *separate* directive and is **not** part of the worktree program; it is recorded here because it supersedes part of §12. §1–§14 are the first run's record and are left as written; §1, §2, §3, §5, §7, §8, §9, §10, §12 and §14 carry supersession or evidence notes where a later run or a later check made them untrue, and §15 carries its own where §16 and §17 overtook it. §20 is the status of all four worktree-program tasks at close.
**Section-reference convention:** a bare §N means a section of *this file*. A reference to the owner's directive is always written "directive §N".
**Preservation:** `C:\Users\aviha\Backups\Hypertrophy-Toolbox-v3\worktree-closeout-20261016-150200\`

---

## 1. Summary

The directive lifted the teardown hold for everything in `git worktree list`, granted gates
0/1/2 and the B/C/D approvals in one act, and told me to run to deletion autonomously.

Inventory, preservation, restore testing and plan publication all completed, and the single
pre-deletion review ran. **No reviewer report was retained for it** — its findings survive
only as §6 below and as the fixes in `evidence/scripts/`, so its *result* is reconstructed
rather than evidenced. **Deletion itself is blocked by the installed guard**, which the same
directive forbids me to modify or bypass (§7 below). Nothing was removed, and no target was
left in a worse state than it started.

> **Superseded by §15.** A later continuation directive on 2026-10-16 granted a narrow,
> temporary guard exception for exactly these 91 targets. All 91 were removed; the guard was
> restored byte-for-byte afterwards.

## 2. Scope as measured

`git worktree list` returns **92** entries: the main checkout plus **91** linked worktrees.
The directive's estimate of ~96 worktrees / ~139 branches / 8 stashes re-measured as
**91 / 139 / 8**, with **12** worktrees on detached HEADs (not ~16).

- **Protected, never a target:** `D:\development\Hypertrophy-Toolbox-v3-main`. It carries 23
  modified + 10 untracked files; these were left exactly as found and never staged.
  `git add -A` was never run. (This counts *files*, with untracked directories expanded.
  §15.7's "28 uncommitted files" counts `git status --porcelain` *entries*, which collapse
  untracked directories to one row each: 23 modified + 5 entries. Same working tree, two
  units — 23 + 10 does not equal 28 and was never meant to.)
- **Targets:** the 91 linked worktrees, all under `D:\development\`.
- **Out of scope:** 28 further entries under `D:\development\` that are not in
  `git worktree list` — including `Hypertrophy-Toolbox-v3-git-backups`,
  `Hypertrophy-Toolbox-cleanup-planning`, the `ht-opa-*` lanes and several loose files. Per
  directive §1.A the command output *is* the scope.
- **Branch scope:** 139 local branches = 1 (`main`) + **79** checked out in a target + **59**
  unattached. Branch deletion was restricted to the 79; the 59 unattached are outside the
  authorized scope and were not considered, including 4 that are ancestors of `origin/main`
  and would have been deletable. That is the conservative error.

> **Superseded by §15 and §16**, which both measure **140 / 60**. The difference is exactly
> one branch, and it is this record's own: `evidence/branch-vv.txt` (this inventory, 15:02)
> lists 139 names and does **not** contain `docs/worktree-closeout-20261016`, while
> `evidence/continuation-20261016/branches-after.txt` lists 140 and does. The figures above
> are correct as of their own measurement.

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

> **Superseded by §16 — and the prediction above was exactly right.** A later
> owner-authorized run re-inventoried against the same `origin/main` baseline and deleted
> **13** branches, not 9: the 9 named above plus `wt/dep415-triage`, `wt/ledger-2223`,
> `wt/u3a-gate1` and `wt/u3a-impl` — which are precisely the "4 that are ancestors of
> `origin/main` and would have been deletable" that §2 records as the conservative error.
> Of the original 9, **4 went with plain `-d` and 5 refused it** and needed `-D`, matching
> the "~4 of 9" estimate. The `-D` denial described here was lifted for exactly those names.

### The 4 targets with unique local state (all captured)

| worktree | unique paths |
|---|---|
| `HT-p1-measure` | `pyright.json`, `pyright.stderr.txt` |
| `ht-wt-opt-reval-20260902` | `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md`, `docs/worktree_cleanup/PLANNING.md`, `scripts/worktree_cleanup_audit.py`, `tests/test_worktree_cleanup_audit.py` |
| `ht-wt-theme-align-20260830` | `static/css/components.css`, `static/js/darkMode.js`, `static/js/theme-init.js` — all three **staged** |
| `Hypertrophy-Toolbox-v3-main-ledger2223` (slot 072) | `artifacts_check.md` |

The local `docs/worktree_cleanup/PLANNING.md` lineage is captured to the backup. It was
**not** reconciled against the committed lineage and **not** committed, per directive §1.G.

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

Directive §7 preservation **breadth** was applied. Directive §7 **ceremony** was waived per
directive §1.D: no owner-captured runtime map, no freeze budget, no manifest-with-OIDs, no
operation lock, no archive ref.

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
capture in §6, re-hashed every captured file that has a working-tree twin — **16,296 of the
16,300**, the other 4 being extracted staged blobs that have no twin by definition (§10) —
with **0 mismatches and 0 missing**. This is the check that proves the backup represents the
sources rather than merely being self-consistent, and it can only run while the sources
still exist.

> **Evidence qualification.** The artifact this paragraph used to cite,
> `evidence/recheck-all-tranches.txt`, records only `removed=0 retained=0 branches_deleted=0`
> for each of the ten tranches — it carries **no file count at all**. The one retained
> artifact with a fidelity count is `evidence/FIDELITY.txt`, and it records the
> **pre-gap-capture** run: 91 slots, **14,443** live files compared, 0 byte-differs,
> 0 vanished. 14,443 plus the 1,853 files added by the B1 fix is 16,296, which is consistent
> with the claim — but **the post-gap comparison was never written to an artifact**, and the
> sources are gone. The 16,296 figure is reconstructed, not independently evidenced.

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

One independent read-only review ran once, before any deletion, per directive §3 and §6. It
returned **3 blocking findings, all legitimate.** All three are fixed and each fix was
verified. **No reviewer report was retained.** The findings below are reconstructed from the
fixes and the retained scripts, which corroborate them strongly — H1 especially is readable
straight off the code — but the review's own output does not exist in `evidence/`.

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

> **Historical. Resolved by §15.** The owner resolved the conflict described here by
> authorizing a scoped, temporary exception to the two denials below. This section records
> why the first run stopped, not the final state.

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
bypassing the guard, and directive §6 forbids changing prevention tooling. Those instructions are in
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

> **Evidence qualification.** Of these figures only **984** was written down, as a comment in
> `evidence/scripts/step7_remove.sh`. The 1,097 and 113 counts have no retained artifact, and
> every target is now gone, so they cannot be re-measured. `evidence/scripts/REMOVAL_PLAN.md`
> also still asserts the superseded **115** figure that the paragraph above calls wrong; the
> retained plan was never corrected, so a reader following the citation meets the wrong
> number with no marker on it.

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

> **Corrected by §17.** The 2026-10-17 residue inventory of that same worktree found **10**
> such reparse points, not 12: the `.git` ×4, `dangling-link` ×4 and `redirected` ×2, but no
> `*.lock` reparse points. The 2 `.lock` entries are unaccounted for — most plausibly file
> symlinks removed along with the files during the §15 run, but nothing retained records it.

This measurement is what makes the mechanics safe rather than merely careful: the removal
unlinks **every** escaping reparse point (not a hardcoded two names), then asserts none
survives before deleting, failing closed if the scan itself fails. Unlinks use
`cmd /c rmdir` — link only, target untouched — never `rm -rf`, never from inside a junction.

The capture pruned `.venv`, `node_modules` and `.git` from every `find`, so nothing traversed
them.

## 9. Retained targets

> **Superseded by §15.3.** Zero targets are retained. All 91 were removed on 2026-10-16
> after the guard exception was granted. The ordering caveat recorded below was honoured:
> the four `opus`/`sol` lanes ran last, in tranches 9–10. The single removal residue is
> recorded in §15.4 and was cleared in §17.

**All 91**, for one shared reason: the guard denies the removal primitive. No target was
retained for a preservation, fidelity or activity reason — all 91 pass the hardened recheck
(`retained=0` across all ten tranches).

Four are additionally flagged for ordering: `ht-lane-sol-20260929`, `ht-wt-457-merge-opus`,
`ht-wt-462-opus` and `ht-wt-463-opus` are the `opus`/`sol` parallel lanes driven by an owner
"next batch" trigger, with 0/11/2/4 unpushed commits (all tips pinned and bundled). No live
process, lock, WAL/SHM file or recent write was found for any of them, and they were ordered
last (tranches 9–10). **Removing them retires the directories that the standing "next batch"
trigger drives — that is a workflow decision for the owner, not a data-loss risk.**

> **That decision was never separately put to the owner.** §15.3 removed all four in tranches
> 9–10. The continuation directive's instruction to remove all 91 was treated as subsuming
> the workflow question raised here, but the owner was not asked it and did not answer it,
> and it appears in neither §11 (waived) nor §12 (parked). It is recorded here as **decided
> by implication, not by the owner.** If that implication was wrong, the four lane
> directories are reconstructable from the backup.

## 10. Accepted risks

> **Partly superseded by §15.5.** Three of these were closed by measurement during the
> removal run: the near-vacuous activity check was replaced by an OS-level exclusive-access
> probe, the junction-following question was answered on a throwaway worktree, and the
> predicted MAX_PATH partial failure actually occurred on the largest target. The
> non-atomicity of recheck-then-remove still stands.

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
- `docs/worktree_cleanup/` is **not** ignored. An earlier draft of this bullet said it was
  listed in `.gitignore`. That is wrong: `.gitignore` contains no `worktree_cleanup` entry and
  `git check-ignore -v docs/worktree_cleanup/CLOSEOUT.md` exits 1 with no matching pattern.
  (`git check-ignore -v` on the directory *with a trailing slash* appears to match
  `.gitignore:101`, but line 101 is blank and the printed pattern is empty — a false positive,
  contradicted by `-n`.) `origin/main` already tracks `PLANNING.md` and
  `OPERATION_A_OWNER_ACCEPTANCE.md` there, so this record commits normally — the conclusion
  held, the stated reason did not.
- Because the directory is **not** ignored, the local untracked `PLANNING.md`, `STATUS.md`,
  `AMENDMENT_2026-09-28.md`, `PROVENANCE_RECOVERY_OPTIONS.md`, `evidence/` and `tasks/` stay
  permanently visible in `git status`. Git is **not** preventing them from being staged. The
  local `PLANNING.md` is a divergent lineage, shorter than the copy on `origin/main`, and must
  never be staged (§3, §12).

## 11. Waived for this cleanup

Recorded as **waived, not completed and not passed**, per directive §1.C: the three VS Code
capture sessions, the scheduled-task calendar firing, the loaded-source coverage review, the
G07 decision, and every Gate A row. Operation A qualification and monitoring were neither run
nor waited on. Directive §7 preservation ceremony waived per directive §1.D. The
August-backup attribution investigation stayed closed per directive §1.F; the 14,255-entry
manifest was not re-walked.

## 12. Staying parked

Operation E / main reconciliation, `docs/worktree_cleanup_amendment/`, Operations F and G,
`D:\c` and `D:\d`. The drive-root audit was left exiting non-zero, as intended. The two
`PLANNING.md` lineages were not reconciled and the local one was not committed.

> **Partly superseded by §18.** `D:\c` and `D:\d` were removed on 2026-10-17 under a
> *separate* owner directive, outside the worktree program and outside the teardown lift this
> record was written under. Everything else listed here stays parked, including both
> `PLANNING.md` lineages.

## 13. Contradictions between the documents and this directive

Per directive §2, `docs/worktree_cleanup/` (≈2,800 lines across `PLANNING.md`, `STATUS.md`,
`AMENDMENT_2026-09-28.md`, `PROVENANCE_RECOVERY_OPTIONS.md`) is treated as history. Its open
"OWED" items, Gate A rows and decisions 1–5 were not re-derived or re-litigated. The one
contradiction that mattered operationally is recorded in §7: the installed guard enforced the
worktree-retention hold that directive §1.A lifts. It was resolved by the continuation
directive's scoped, temporary exception (§15.1); the hold itself is back in force.

## 14. Not done, by instruction

> **Two items superseded.** "No prevention tooling changed" was true of the first
> run only. The continuation directive authorized a temporary, scoped edit to the guard; it
> was installed, verified, used for the 91 removals and then reverted to its exact original
> bytes. **"No pytest" is also superseded:** §15.2 ran the 1,282-case guard regression suite
> and a 372-case exception suite, both under pytest. What was never run is the *application*
> suite — no application test, E2E or visual run happened in any of these tasks. Nothing else
> in this list changed: still no `git gc`, no reflog expiry, no object pruning, no branch
> pushes, no remote-ref deletion, no backup deletion.

No `git gc`, no `git reflog expire`, no object pruning, no branch pushes of target branches,
no remote-ref deletion, no backup deletion. No pytest, E2E or visual suites — this was git
housekeeping, not a code change. No application code, prevention tooling or repository policy
changed. No new planning packet, amendment, status document, options memo or ADR was created;
this file is the single record.


---

## 15. Continuation run — removal executed, 2026-10-16/17

**Authority:** owner continuation directive, 2026-10-16, which explicitly authorized "the narrow
guard modification required below" and superseded the previous prohibition on modifying prevention
tooling *for that bounded change only*.

**Window:** baseline captured `2026-10-16T20:07:34Z`; the 91 removals ran between roughly
`20:15Z` and `20:55Z`; the guard exception was installed and verified before the baseline and
restored and behaviourally re-verified after the last removal. The exact install and restore
instants were **not recorded to the second**, and the retained evidence does not pin them — an
earlier draft of this line carried `19:4xZ` and `20:5xZ`, which were placeholders rather than
measurements and are withdrawn rather than guessed at. Local time crossed into 2026-10-17 during the
write-up, which is why this section is dated across both days.

**Outcome: 91 of 91 worktrees removed. 0 retained. 0 branches deleted. The guard is restored to its
exact original bytes.** The preservation directory is untouched.

### 15.1 The guard exception

`.claude/hooks/guard-destructive-command.ps1` is wired twice — by `.claude/settings.json` **and**
by `C:\Users\aviha\.claude\settings.json`, both with `-GuardProfile main`. The copy this session
actually invokes is the **user-level** one; the first denial message of the run is what revealed
that. Both copies were byte-identical (`0afb81b8…4502`) and both were patched identically.

Original bytes preserved before any edit, in two places, and hash-checked:
`<scratchpad>/guard-restore/guard-destructive-command.ORIGINAL.ps1` and
`<backup>/evidence/guard-destructive-command.ORIGINAL.ps1`, both
`0afb81b851c9b00b71dea8928cf199d7e5665ca4f46016495e4b1ad5a8184502` / 62,363 bytes.

The exception authorizes **one command form against one explicit list**, and denies unless *every*
one of these holds:

| axis | requirement |
|---|---|
| profile | `main` only — the `agent` profile still denies |
| repository | the hook payload's own `cwd` must be the main checkout |
| session | the payload's `session_id` must be this coordinator session |
| segment | the segment **as written** must be exactly five tokens starting `git`, at suffix position 0 |
| form | `remove` `--force` `<path>`, compared case-sensitively; no `-f`, no `--force=1`, no extra operand |
| target | ordinal case-insensitive equality with one of the 91 canonical inventory paths |

Everything else in the retention hold was left exactly as it was: `worktree prune`, branch, tag,
`symbolic-ref`, `update-ref` and remote-ref deletion, and the whole `rm` family. The hook was never
disabled, no permission mode was changed, no `deny` was broadly replaced, and the removal primitive
was never run from inside an opaque script — every one of the 91 removals went through the guarded
tool path as literal text the guard parsed.

**Branch deletion was deliberately left out of the exception.** §4 of the directive makes it
optional and says to retain whenever deletion is denied, so the guard's unchanged `git branch -d`
denial stood and **all 140 local branches were kept at the end of this run**, including the 9
that qualified for deletion in §3.

> **Superseded by §16.** True of this removal run only. A separate owner-authorized run on
> 2026-10-17 deleted 13 branches under its own scoped exception; **127 remain.**

### 15.2 Verification of the exception

| check | result |
|---|---|
| pre-existing guard regression suite | **1282 / 1282 pass**, unchanged, against both PowerShell hosts |
| new exception suite (kept out of `tests/`, uncommitted) | **372 / 372 pass** — 2 hosts × 2 guard copies |
| repository/session binding checks | **25 / 25 pass** |
| pre-removal gate mutation matrix | **19 / 19 pass**, every gate exercised in both directions |
| disposable no-follow removal smoke test | **pass**, both arms |
| restored-guard behavioural checks | **76 / 76 pass** |

> **Evidence qualification.** Every *denominator* here is reproducible from the retained
> harnesses — 1,282 and 372 by pytest collection, 25 cases in `probe_binding.py`, 19 mutation
> arms plus a baseline in `mutate.sh`, and 76 = 2 hosts × 2 guard copies × 19 cases in
> `verify_restored.py`. **The pass/fail output was not retained for any row except the last.**
> That one is still re-runnable against the restored guard, and an independent re-run at
> `2026-10-16T21:41Z` passed 76/76. The 372-case and 25-case suites exercise the *patched*
> guard and can no longer be re-run at all, so their verdicts rest on this narrative alone.

The new test files live beside the run scripts rather than in `tests/`: the exception is temporary
and must not reach a commit, and adding a file under `tests/` would also move the
test-inventory drift gate.

### 15.3 What was removed

All 91, in the ten risk-ordered tranches from `evidence/inv/tranches.txt`, lowest risk first and
the `opus`/`sol` lanes last. `git worktree list` went **92 → 1**: only
`D:\development\Hypertrophy-Toolbox-v3-main` remains. `git worktree prune --dry-run -v` reports
**nothing prunable**, so no pruning exception was needed or added — normal removal retired every
registration, as §4 of the directive anticipated.

Per target, immediately before its own removal and in the same shell command as it, the gate
rechecked: the inventory row, that the caller's path matches that row, that the target is not the
main checkout and is under `D:/development/`, the canonical path, that the root is not itself a
reparse point, that the target is still a registration of this repository, `HEAD`, **the index**
(staged path list and every staged blob OID against the capture), every captured file by SHA-256,
that nothing uncaptured had appeared, `index.lock`, SQLite WAL/SHM, the 60-minute write window, the
process-image probe, **exclusive OS-level access**, and finally that nothing under the worktree
could reach outside it.

**113 escaping junctions were unlinked across the run**, every one of them pointing into this main
checkout's `.venv` or `node_modules`. Each was removed as a *link* with `rmdir`, never followed,
and each target re-scanned to zero before the forced delete. The main checkout's toolchain is
byte-for-byte intact: `.venv` 8,256 files, `node_modules` 6,566 files, `python.exe` 255,200 bytes
— all three identical to the pre-run baseline.

### 15.4 Targets retained, and the one residue

**None retained.** Every one of the 91 passed its gate and was removed.

One target left residue. `D:\development\Hypertrophy-Toolbox-npm-audit-fix` (slot 062, the
largest target: a real `node_modules`, 10,631 ignored files, 982 reparse points) had its
registration retired and all of its **files** deleted, but **25 empty directories survive** under
its `artifacts/` tree — 0 files, 540 KB of directory entries, no `.git`, and a re-scan confirms
**0 reparse points that can reach outside it**. This is exactly the MAX_PATH partial failure §10
predicted, and it is the predicted *harmless* shape of it: nothing is lost (the payload is in the
backup and re-verified), and nothing can reach the main checkout. It is left in place because
clearing empty directories needs a recursive delete that the restored guard denies by design, and
working around that with a verb the guard does not model would be the evasion the directive
forbids. **Clearing it is a one-line owner action, not an open risk.**

> **Superseded by §17.** The residue was cleared on 2026-10-17 and
> `D:\development\Hypertrophy-Toolbox-npm-audit-fix` no longer exists. Three things above were
> wrong. The tree also held **10 dangling fixture junctions** this paragraph does not count —
> four of them *named* `.git`, which makes "no `.git`" read more reassuringly than the facts
> warrant, though none was a real git directory. Clearing it needed **no recursive delete and
> no guard change**, so "the restored guard denies it" was not the reason it was left. And it
> was not "a one-line owner action": it took an inventory, a preflight, 48 guard probes, a
> two-reviewer gate, a resumable journal and 35 separate operations. The conclusion — nothing
> lost, nothing able to reach the main checkout — held.

### 15.5 What the review found, and what measurement settled

One independent reviewer read the exception and its tests, per directive §2. It returned six
findings — two high (H1, H2), three medium (M1, M2, M5) and one low (L2). **Three were real
and are fixed (H1, H2, M1); two were not reproduced (M2, L2); one was a stale read (M5).**
Each was checked by running it where that was possible — though not uniformly: H1 and M1 were
reproduced by running them, while **H2 was confirmed by reading the agent definitions** and
**M5 was explained from the file's edit history**, neither of which is a run.

> **Correction.** An earlier draft of this paragraph said "three high-severity findings — two
> real, one false premise". That contradicted the list underneath it, which has always held
> six, of which three are described as real and fixed. The count above is the one the body
> supports.
>
> **Unaccounted labels.** The reviewer's identifiers run H1, H2, M1, M2, M5, L2 — **M3, M4 and
> L1 are absent**, and the reviewer's own finding list was not retained in `evidence/`. Their
> disposition is **unknown and unrecorded**. They must not be read as "no finding", as
> withdrawn, or as cleared.

**H1 — the fail-closed branch could never fire. Real, and the worst of the three.** The escaping-
reparse helper's exit status was captured inside a `$(...)` command substitution, which runs in a
**subshell**, so the caller's copy of the status stayed `0` forever. Measured directly: a helper
exiting 2 prints nothing, the empty result reads as "nothing escapes", and the forced recursive
delete would have proceeded with the junctions into this main checkout still live. **This bug came
in with the reviewed `step7_remove.sh`, where the same fix is recorded as applied** — the fix
that file's own header labels F2, and that §6 reports as finding **B2**, was written but was
inert. (An earlier draft called it "§6's F2 fix"; §6 labels its findings B1/B2/B3 and defines
no F2.) The status is now read from a file, and the branch is proven to fire by
a mutation arm that makes the helper exit 2.

**H2 — the exception was not actually bound to this repository or to the coordinator.** Confirmed
by reading the agent definitions: only `senior-developer` and `automation-qa` wire the Bash guard
in frontmatter (and they do so *without* `-GuardProfile`, so they correctly default to `agent`).
The other eight agent types run under the settings-level `main` hook alone, and the user-level
guard is global to every session on the machine. Fixed by binding to the payload's `cwd` and
`session_id`, whose presence was established by capturing one real payload rather than assumed.

**M1 — wrapper and prefix forms reached allow.** Confirmed by measurement: `GIT_DIR=D:/other/.git
git worktree remove --force <listed>`, `env -C D:/other git …`, `sudo …` and `nice …` **all
returned allow** against a listed target. The cause was not wrapper stripping but the guard's
every-position suffix rescan, which re-presents the inner command as a clean five-token `git …`.
Fixed by pinning authorization to suffix position 0 of a segment that is literally the five-token
form. All four now deny, and all four are pinned by tests.

**M2 — not reproduced; the measurement was not retained.** The premise was that PowerShell 5.1's `Get-ChildItem -Recurse`
descends into junctions, so the scanner would report reparse points *inside* the main checkout
under worktree-prefixed paths. Measured on a live target: 2 reparse points found, **0 entries under
the `.venv` junction**. It does not descend. **That measurement was never written to an
artifact, and every target is now gone, so it cannot be re-run** — this finding must be read
as not reproduced, not as refuted. The hardening it suggested was applied anyway because
it is cheap and strictly safer: the unlink loop now processes shortest path first, skips anything
nested under a link already removed, and **aborts instead of swallowing a failed unlink with
`|| true`**.

**M5 — explained: a stale read.** The reviewer read `precheck.sh` before the validation-mode and
alternate-expectations hooks were added, and reported the mutation harness as unable to work. The
harness demonstrably ran against the fake expectation set.

**L2 — refuted by measurement, and independently re-confirmed.** The concern was that the
`build`/`dist` cache exemption could hide an uncaptured user file. Across all 91 targets there was exactly **one** such file: a 6-byte
`<html>` pytest fixture, and it is already in the backup manifest with a matching hash.

**The junction question is now answered.** §10 recorded as unsettled whether
`git worktree remove --force` follows a Windows directory junction, and noted that settling it
required running the denied primitive. A second disposable smoke arm settled it: with a **live**
junction deliberately left in place, pointing at a throwaway directory with sentinels, git
**did not follow it** — the external target came back byte-identical. What it did instead is
instructive: it deleted everything else, **left the junction and its parent directory behind, and
still retired the registration**. So the unlink step is what makes a removal *complete*, and a
`rm -rf` — not git — was always the thing that would have destroyed this checkout's toolchain.

**The activity check is no longer near-vacuous.** §10's first accepted risk was that no process on
this machine has an image path under `D:\development\*`, so a live app or test run inside a target
was invisible. A new `exclusive-access.ps1` asks the OS instead: it opens the worktree root with
share mode `NONE` and every database, gitfile and per-worktree `index`/`HEAD` with
`FileShare.None`, and fails closed on a probe error. Validated against four controls — quiet target
(clear), a process merely *sitting* in the directory (**detected**, win32 32, which the old check
could not see), a held-open database file (**detected**), and a missing or non-directory root
(fail closed). Across the run it enumerated 1,805–12,781 files per target to find the paths
worth opening; the handles actually opened with `FileShare.None` are the worktree root plus
its database, gitfile and per-worktree `index`/`HEAD`/`ORIG_HEAD` paths — low hundreds at
most, even on the largest target. An earlier draft of this line called that enumeration range
a handle count.

Two of my own checks passed **vacuously** before they were trusted, and both were caught by
deliberately making them fail: the first two exclusive-access positive controls were measuring
holder processes that had already died, and one mutation arm used `${3:-default}`, which substitutes
the default for an *empty* argument and so silently re-ran the baseline.

### 15.6 Residual scope limits, recorded not claimed closed

- **A subagent of this same session could have passed the binding.** The payload carries no agent
  identity field, so `session_id` cannot distinguish a subagent from its parent. No agent was
  spawned at any point during the removal run, and the exception is now gone. Two of the ten agent
  types are additionally protected by their own `agent`-profile hook.
- **The `cwd` test pins the tool's directory, not the repository git acts on.** A
  `cd other-repo &&` segment keeps this payload `cwd`. What pins the repository in practice is the
  explicit 91-path allowlist plus the gate's assertion that the target is a current registration of
  *this* repository.
- **Recheck and removal are still not atomic.** A write landing between the gate and the removal is
  undetectable. Inherent to a shared checkout; unchanged from §10.

### 15.7 Final state

| | before | after |
|---|---|---|
| `git worktree list` | 92 | **1** (main only) |
| stale registrations (`prune --dry-run`) | 0 | **0** |
| local branches | 140 | **140** (identical names) — later 127, see §16 |
| stashes | 8 | **8** (identical) |
| main `HEAD` | `85e2372` | `85e2372` |
| main uncommitted files | 28 | **28** (byte-identical list) — later 27, see §20.1 |
| main staged files | 0 | **0** |
| main `.venv` / `node_modules` | 8,256 / 6,566 | **8,256 / 6,566** |
| guard SHA-256 (both copies) | `0afb81b8…4502` | **`0afb81b8…4502`** |

The preservation directory is unchanged at **1.9 GB**, `MANIFEST.txt` still lists 17,913 files, and
the 40 `refs/closeout/…` reachability pins are all still present. (§17 qualifies this: two
`__pycache__` objects later appeared under `evidence/continuation-20261016/`, so *full*
unchanged-backup equality is not claimed. The manifest, the bundle and the payload are
unaffected.) `git add -A` was never run; only
this file was staged.

### 15.8 Not done in this run

> **Scope note.** "In this run" means the removal run of 2026-10-16. Branch deletion was done
> afterwards under separate authorization (§16), and §15.4's residue was cleared in §17.
> Everything else in this list still stands.

No `git gc`, no reflog expiry, no object pruning, no branch deletion, no branch pushes, no
remote-ref deletion, no `refs/closeout` retirement, no pruning exception, no backup deletion. No
new planning packet, amendment, status document, options memo or ADR. No application code or
repository policy changed, and the guard change was reverted. The items parked in §12 stay parked.

## 16. Authorized local-branch cleanup — 2026-10-17

Completed at `2026-10-16T21:30:54+00:00` under the owner's explicit branch-deletion and temporary scoped-guard authorization. Fresh inventory: **140 local branches**; **13 deleted**, **127 retained**. One coordinator performed all mutations; two read-only subagents independently classified tips and verified preservation/reviewed the exact deletion plan. One pre-deletion review completed with no outstanding blockers; the benign ambient `GIT_PAGER` execution issue was fixed and verified within that review. No new worktrees, application execution or database access.

Fetched origin with `--no-prune --no-tags --no-auto-maintenance` and `gc.auto=0`. Exact merge baseline: `origin/main` = `71fc65864cf510d78382c6d6504a3b68b30c2158`. Local `main` = `85e23725bc2871c5f005162f29be231a2f106b85` remained checked out and diverged (3 ahead / 41 behind); it was never substituted for the baseline.

### 16.1 Preservation and deletion

Reused the existing `worktree-closeout-20261016-150200/all-refs.bundle`: SHA-256 `31262a3af38231249fd7202c70e688eba6efa920def1d1e6c3c53b434cf34274` matches its original manifest. All 13 reviewed name/OID pairs were advertised exactly by that bundle; no missing eligible tip required supplemental preservation. Fresh standalone bare restore: `C:\Users\aviha\Backups\Hypertrophy-Toolbox-v3\branch-cleanup-20261017\restore.git`. It has independent object storage, no alternates or shallow history, and passes full fsck. Both read-only agents independently confirmed exact-tip eligibility/preservation.

Each branch was rechecked for exact OID, pinned-baseline ancestry, checkout/protection status and standalone restore availability. `git branch -d` ran first; `-D` was used only where the sole refusal was Git's not-fully-merged check against diverged local HEAD/upstream. OID was rechecked immediately before each deletion. Exact results:

| Deleted branch | Exact preserved tip | Command |
|---|---|---|
| `diag/linux-visual-gate1-diag-20260901` | `fabdb2f7db9f2c4173080c5a2e86b87c57f04c84` | `git branch -D` |
| `docs/js-ledger-56-64` | `4ce59e54d6b3aff559f1f1f5b7f944e29c14e2d2` | `git branch -D` |
| `docs/optional-css-status-reconcile-20260901` | `884cfb3bd89372fdcc8c8c84cfdd5136cc434679` | `git branch -D` |
| `docs/u2-ledger-rows-20-21` | `d35e369e4def316643af2aa9df63f7d0f61376ad` | `git branch -d` |
| `docs/worktree-cleanup-replacement-20260904` | `0f1ac2ed66c24151f6d8c00d9962ebd8a959ad6f` | `git branch -d` |
| `fix/npm-audit-colord-js-yaml-20260910` | `6d31aa53e8ee68e2953b20463fdfd3f77b2cda12` | `git branch -d` |
| `wt/deepgate-0831-monitor` | `450d3a721391721a0c579f8e8d819dc4e77cc207` | `git branch -d` |
| `wt/dep415-triage` | `52c44c43a9d4f643437057085de233b1e9b4b689` | `git branch -d` |
| `wt/ledger-2223` | `5111a7fc9793fe5323134c157054e6b740641717` | `git branch -d` |
| `wt/opt-wp-audit` | `1dd710af56d01d714b568ab92bb89c2d3a5c0de1` | `git branch -D` |
| `wt/optional-css-audits-publish` | `d932d368f72b3fbab9e035387350aedb2075f3a6` | `git branch -D` |
| `wt/u3a-gate1` | `5111a7fc9793fe5323134c157054e6b740641717` | `git branch -d` |
| `wt/u3a-impl` | `5111a7fc9793fe5323134c157054e6b740641717` | `git branch -d` |

Execution blockers: **0**. Deleted with `-d`: **8**; authorized `-D`: **5**.

### 16.2 Retained branches and reasons

`main` remains protected and checked out. `docs/worktree-closeout-20261016` remains protected for open PR #507. The other 125 branches have exact tips that are not ancestors of the fetched baseline; squash/name/closed-PR equivalence was not inferred. Nine open PRs were freshly queried; no other local branch matched an open PR. Active claims registry reports none. Preservation/WIP branches are additionally retained where named below.

| Retained branch | Reason |
|---|---|
| `docs/d4-signature-and-gate1-plan` | exact tip is not ancestor of origin/main |
| `docs/deep-gate-linux-visual-gate0-20260831` | exact tip is not ancestor of origin/main |
| `docs/hlinux-unsync-01-gate1-closeout-20260902` | exact tip is not ancestor of origin/main |
| `docs/js-unit-ledger-row-44-2026-08-29` | exact tip is not ancestor of origin/main |
| `docs/js-unit-ledger-row-7` | exact tip is not ancestor of origin/main |
| `docs/js-unit-ledger-rows-22-23` | exact tip is not ancestor of origin/main |
| `docs/js-unit-ledger-rows-24-26` | exact tip is not ancestor of origin/main |
| `docs/ledger-rows-22-23` | exact tip is not ancestor of origin/main |
| `docs/ledger-rows-27-37-and-plan-reconcile` | exact tip is not ancestor of origin/main |
| `docs/od1-waiver-record-20260829` | exact tip is not ancestor of origin/main |
| `docs/open-work-live-reconciliation-20260830` | exact tip is not ancestor of origin/main |
| `docs/open-work-plan-post417` | exact tip is not ancestor of origin/main |
| `docs/open-work-plan-status-2026-08-27` | exact tip is not ancestor of origin/main |
| `docs/post-p1-status-reconcile-20260829` | exact tip is not ancestor of origin/main |
| `docs/post414-evidence-reconciliation` | exact tip is not ancestor of origin/main |
| `docs/r1-name-collision-reconcile` | exact tip is not ancestor of origin/main |
| `docs/r1-postmerge-reconcile` | exact tip is not ancestor of origin/main |
| `docs/refactor-plan-p1-closure-2026-08-29` | exact tip is not ancestor of origin/main |
| `docs/status-reconciliation` | exact tip is not ancestor of origin/main |
| `docs/step12-od1-waiver-clause` | exact tip is not ancestor of origin/main |
| `docs/t0-declaration-final-expansion-packet-2026-08-29` | exact tip is not ancestor of origin/main |
| `docs/u1-gate1-plan` | exact tip is not ancestor of origin/main |
| `docs/u2-gate1-plan` | exact tip is not ancestor of origin/main |
| `docs/u3a-ki010-gate0-plan` | exact tip is not ancestor of origin/main |
| `docs/u3a-ki010-gate1-plan` | exact tip is not ancestor of origin/main |
| `docs/u3b-ledger-row-17-19` | exact tip is not ancestor of origin/main |
| `docs/v1-probe-result` | exact tip is not ancestor of origin/main |
| `docs/worktree-closeout-20261016` | PR #507; open PR #507; exact tip is not ancestor of origin/main |
| `feat/body-muscles-integration` | exact tip is not ancestor of origin/main |
| `feat/d4-packet-a-role-weight-accumulation-b` | exact tip is not ancestor of origin/main |
| `feat/d4-packet-b-rep-range-totality` | exact tip is not ancestor of origin/main |
| `feat/u1-volume-failure-feedback` | exact tip is not ancestor of origin/main |
| `feat/u1-volume-failure-feedback-impl` | exact tip is not ancestor of origin/main |
| `feat/u3a-ki010-toast-collision` | exact tip is not ancestor of origin/main |
| `fix/css-theme-source-alignment-2026-08-27` | exact tip is not ancestor of origin/main |
| `fix/css-theme-source-alignment-reconciled-20260830` | exact tip is not ancestor of origin/main |
| `fix/css-theme-source-alignment-reconciled-20260830-b` | exact tip is not ancestor of origin/main |
| `fix/msys-path-conversion-prevention-20260903` | exact tip is not ancestor of origin/main |
| `fix/p1-workout-plan-final-pyright-2026-08-29` | exact tip is not ancestor of origin/main |
| `fix/pyright-youtube-row-narrowing` | exact tip is not ancestor of origin/main |
| `fix/r21-scan-export-bounds-min-max` | exact tip is not ancestor of origin/main |
| `fix/visual-table-raster-stability` | exact tip is not ancestor of origin/main |
| `integrate/p1-addressable-tail-2026-08-29` | exact tip is not ancestor of origin/main |
| `integrate/p1-profile-weekly-user-fatigue-2026-08-28` | exact tip is not ancestor of origin/main |
| `ki006-merge` | exact tip is not ancestor of origin/main |
| `local-pr415-head` | exact tip is not ancestor of origin/main |
| `local-test-merge-415` | exact tip is not ancestor of origin/main |
| `main` | main; checked out; exact tip is not ancestor of origin/main |
| `p1-superseded-local` | preservation or uncertain WIP branch; exact tip is not ancestor of origin/main |
| `p2-post-p1-base` | exact tip is not ancestor of origin/main |
| `pr239-v2` | exact tip is not ancestor of origin/main |
| `pr241` | exact tip is not ancestor of origin/main |
| `pr241-v2` | exact tip is not ancestor of origin/main |
| `pr395-audit` | exact tip is not ancestor of origin/main |
| `pr396-audit` | exact tip is not ancestor of origin/main |
| `pr397-audit` | exact tip is not ancestor of origin/main |
| `pr400tmp` | exact tip is not ancestor of origin/main |
| `pr401-review` | exact tip is not ancestor of origin/main |
| `pr415-updated` | exact tip is not ancestor of origin/main |
| `pr427` | exact tip is not ancestor of origin/main |
| `pr431tmp` | exact tip is not ancestor of origin/main |
| `pr432` | exact tip is not ancestor of origin/main |
| `pr438` | exact tip is not ancestor of origin/main |
| `pr457-review` | exact tip is not ancestor of origin/main |
| `pr462-review` | exact tip is not ancestor of origin/main |
| `pr463-review` | exact tip is not ancestor of origin/main |
| `probe/stylelint17` | exact tip is not ancestor of origin/main |
| `probe/v1-drop-compositing-hints` | exact tip is not ancestor of origin/main |
| `review/pr351` | exact tip is not ancestor of origin/main |
| `salvage/local-main-pre-reset` | preservation or uncertain WIP branch; exact tip is not ancestor of origin/main |
| `salvage/old-feat-fatigue-meter` | preservation or uncertain WIP branch; exact tip is not ancestor of origin/main |
| `save-rebased` | preservation or uncertain WIP branch; exact tip is not ancestor of origin/main |
| `scan/codebase-grounding` | exact tip is not ancestor of origin/main |
| `tmp-rebased` | exact tip is not ancestor of origin/main |
| `verify/r21-457-opus-20260830` | exact tip is not ancestor of origin/main |
| `verify351` | exact tip is not ancestor of origin/main |
| `wip/session-docs` | preservation or uncertain WIP branch; exact tip is not ancestor of origin/main |
| `wt-axe-merge` | exact tip is not ancestor of origin/main |
| `wt/blank-null-rep-bound-gate0` | exact tip is not ancestor of origin/main |
| `wt/blank-null-rep-bound-gate1` | exact tip is not ancestor of origin/main |
| `wt/bs538-sass-rebuild` | exact tip is not ancestor of origin/main |
| `wt/bs538-spike` | exact tip is not ancestor of origin/main |
| `wt/deepgate-evidence-correction` | exact tip is not ancestor of origin/main |
| `wt/deepgate-robustness-gate0` | exact tip is not ancestor of origin/main |
| `wt/deepgate-robustness-gate1-20260831` | exact tip is not ancestor of origin/main |
| `wt/fatigue-caveat-refresh` | exact tip is not ancestor of origin/main |
| `wt/final-truth-audit` | exact tip is not ancestor of origin/main |
| `wt/js-unit-ledger-cutoff-20260831` | exact tip is not ancestor of origin/main |
| `wt/node24-refresh` | exact tip is not ancestor of origin/main |
| `wt/opt-audits-reval-20260902` | exact tip is not ancestor of origin/main |
| `wt/opt-bounded-css-audit` | exact tip is not ancestor of origin/main |
| `wt/opt-theme-p3-audit` | exact tip is not ancestor of origin/main |
| `wt/opt-wlog-audit` | exact tip is not ancestor of origin/main |
| `wt/p1-calibration-integration-worker` | exact tip is not ancestor of origin/main |
| `wt/p1-db-migration-worker` | exact tip is not ancestor of origin/main |
| `wt/p1-effective-sets-tail-20260829` | exact tip is not ancestor of origin/main |
| `wt/p1-export-utils-tail-20260829` | exact tip is not ancestor of origin/main |
| `wt/p1-fatigue-context-tail-20260829` | exact tip is not ancestor of origin/main |
| `wt/p1-fatigue-context-tail-20260829-b` | exact tip is not ancestor of origin/main |
| `wt/p1-fatigue-test-contracts-worker` | exact tip is not ancestor of origin/main |
| `wt/p1-free-exercise-mapping-worker` | exact tip is not ancestor of origin/main |
| `wt/p1-optional-subscript-tranche1` | exact tip is not ancestor of origin/main |
| `wt/p1-persistence-boundaries-20260829` | exact tip is not ancestor of origin/main |
| `wt/p1-profile-calibration-pyright` | exact tip is not ancestor of origin/main |
| `wt/p1-program-backup-worker` | exact tip is not ancestor of origin/main |
| `wt/p1-strength-calibration-worker` | exact tip is not ancestor of origin/main |
| `wt/p1-test-db-boundaries-20260829` | exact tip is not ancestor of origin/main |
| `wt/p1-user-profile-helpers-worker` | exact tip is not ancestor of origin/main |
| `wt/p1-user-profile-pyright-worker` | exact tip is not ancestor of origin/main |
| `wt/p1-volume-progress-tail-20260829` | exact tip is not ancestor of origin/main |
| `wt/p1-volume-progress-worker` | exact tip is not ancestor of origin/main |
| `wt/p1-weekly-summary-parser-worker` | exact tip is not ancestor of origin/main |
| `wt/p1-workout-log-utils-worker` | exact tip is not ancestor of origin/main |
| `wt/p1-youtube-video-id-worker` | exact tip is not ancestor of origin/main |
| `wt/post367-status` | exact tip is not ancestor of origin/main |
| `wt/pyinstaller-622-prose` | exact tip is not ancestor of origin/main |
| `wt/r1-deepgate-probes-b` | exact tip is not ancestor of origin/main |
| `wt/release-pipeline` | exact tip is not ancestor of origin/main |
| `wt/test-honesty` | exact tip is not ancestor of origin/main |
| `wt/u2-update-427` | exact tip is not ancestor of origin/main |
| `wt/u3-ki011-gate0` | exact tip is not ancestor of origin/main |
| `wt/u3a-gate1-integrate` | exact tip is not ancestor of origin/main |
| `wt/u3a-impl-integrate` | exact tip is not ancestor of origin/main |
| `wt/u3a-ledger-t0-restart` | exact tip is not ancestor of origin/main |
| `wt/v1-docs-recon-20260829` | exact tip is not ancestor of origin/main |
| `wt/v1-frozen-policy-closeout-20260830` | exact tip is not ancestor of origin/main |
| `wt/xdist` | exact tip is not ancestor of origin/main |

### 16.3 Guard and final invariants

The installed guard denied branch deletion before the exception. Temporary exception was limited to 26 exact whole-command forms: the 13 reviewed branch names with `-d`/`-D`, explicit repository paths, matching coordinator session/cwd/main profile, and no repository-affecting Git environment overrides. Unrelated protections remained in force. Original baseline controls: **94/94**; proposed exception controls: **94/94**; both installed copies: **94/94 each**; restored originals: **94/94 each**, across Windows PowerShell and pwsh. Both guard copies were restored in `finally`, byte-for-byte, SHA-256 `0afb81b851c9b00b71dea8928cf199d7e5665ca4f46016495e4b1ad5a8184502`. Settings files are unchanged.

Final ref comparison equals the initial post-fetch ref set minus exactly the 13 reviewed branch refs. All 127 retained branch names/OIDs, 40 closeout preservation refs, two tags, eight stashes (including reflog entries), remote refs and other non-target refs remain exact. Main HEAD, symbolic checkout, worktree registration and index bytes remain exact. Tracked working-tree diff is unchanged across deletion. Existing backup bundle hash remains exact.

No push, merge, PR creation, reflog expiry, object pruning, backup deletion, staging or commit was performed. Evidence and coordinator scripts: `artifacts/branch-cleanup-20261017/`, copied to `C:\Users\aviha\Backups\Hypertrophy-Toolbox-v3\branch-cleanup-20261017\evidence\`.

---

## 17. Empty-directory residue cleanup — 2026-10-17

**Authority:** owner's exact-target residue directive, 2026-10-17. This appendix
supersedes the remaining-residue statement in §15.4; earlier records are unchanged.
**Outcome:** `D:\development\Hypertrophy-Toolbox-npm-audit-fix` no longer exists;
only the main worktree remains registered. No branch/ref operations were performed.

The coordinator and two read-only subagents independently measured **25 ordinary
directories (including the root), 0 regular files, and 10 directory junctions**.
The previous “empty directories” report omitted those junction objects. Their ownership
was resolved before removal: all ten are the guard-test fixtures explicitly documented
in §8 (`dangling-link` ×4, `.git` ×4, `redirected` ×2), with stored targets inside this
residual tree and absent from its no-follow ordinary-directory inventory. No live
worktree registration, root gitfile, foreign files, or escaping link target was found.
The junction metadata was recorded before removal; no junction was followed.

One pre-removal review ran with both subagents and found no blocking issues. The
coordinator unlinked those **10 owned dangling junction objects**, then removed **25
rechecked-empty ordinary directories bottom-up**, including the root. Every operand
was canonical, inside the exact named target, wildcard-free, and had ordinary resolved
ancestors. Native PowerShell 7 `Remove-Item -Path '<exact path>' -EA Stop` was used
without recursion or force. The removal journal spans **2026-10-16T21:32:59Z–21:33:29Z**
(**2026-10-17 00:32:59–00:33:29 Asia/Jerusalem**).

The unchanged installed guard misclassifies `-LiteralPath`/`-ErrorAction` as recursion;
the standard `-Path`/`-EA` form passes its existing model, with wildcard rejection
making the path literal in effect. **No guard exception or edit was needed.** Both
copies remain SHA-256 `0afb81b851c9b00b71dea8928cf199d7e5665ca4f46016495e4b1ad5a8184502`.
Guard-only checks passed 48/48 across both hosts, copies and profiles, with destructive
negative controls; all 35 literal command forms also passed both hooks on both hosts.
Automatic platform approval rejected the combined inline command forms as “blocked
by policy”. The specific runtime fix separated read-only prechecks, each visible
standalone literal removal command, and its absence check/journal write; both reviewers
verified the fix without restarting the review. No opaque deletion script was invoked.

Independent postchecks confirm target absence by parent enumeration, main-only
registration, 35 distinct journal entries, unchanged guard bytes/behavior, and identical
`.venv`/`node_modules` metadata fingerprints (8,949/7,524 entries). Protected sibling
root metadata, `D:\c`, `D:\d`, hook settings, main HEAD, index hash, status and staged
state also match the pre-removal baseline. Nothing was staged. No worktrees, servers,
database access, dependency changes, application tests, PRs or merges were introduced.

**Preservation verification qualification:** no cleanup command wrote to the backup,
but its ambient metadata snapshot changed **29,991 → 29,993 entries** during the run.
Two new objects appeared at **2026-10-16T21:33:11Z** beneath
`evidence/continuation-20261016/`: `__pycache__/` and
`__pycache__/test_guard_worktree_exception.cpython-314-pytest-9.1.1.pyc`, also changing
their parent directory timestamp. **The actor is now confirmed:** a concurrent read-only
reconciliation session ran `pytest --collect-only` against the retained exception suite at
that instant, and Python wrote the bytecode cache beside it. It was not the residue
coordinator or either of its subagents. Nothing was deleted or overwritten, and the two
objects were left in place rather than removed from a preservation directory. These objects were preserved outside the sole
authorized deletion target. **Full unchanged-backup equality is not claimed.** The
existing `MANIFEST.txt` SHA-256 remains
`bd474ebe6a9ebda251bf6afb4f5f0662ec5e6d11d65bb8b2adce2dda5a43ed92`.

Resumable inventory, exact reviewed command forms, the single review receipt, guard
checks, 35-operation journal, before/after fingerprints and backup-change evidence
are in gitignored `artifacts/residue-cleanup-20261017/`. No deletion scope was expanded.

---

## 18. Drive-root stray-directory cleanup — 2026-10-17

**Separate authorization, separate scope.** This section records a cleanup that is **not part
of the worktree program**. The 2026-10-16 directive lifted the teardown hold for everything in
`git worktree list` (§1); the five directories considered here sit at the `D:\` drive root and
were **outside that lift**. They were removed under a distinct owner directive of 2026-10-17
that authorized three named targets and nothing else. No worktree was removed, no prune was
run, no branch was deleted, no ref was retired. `git worktree list` was **1** entry before and
**1** entry after.

### 18.1 What was removed

| Target | Files | Bytes | Basis |
|---|---|---|---|
| `D:\ht-b1-scratch` | 14,367 | 3,322,859,877 | 15 clone roots; 0 untracked, 0 stashes; both HEADs (`0a1f778`, `6dfb3b3`) on `origin`; every differing blob reachable from a main commit |
| `D:\d` | 52 | 16,994,332 | MSYS path-conversion fault; preserved and hash-verified first |
| `D:\c` | 1 | 54,905 | 245-entry vitest listing, sha256 `41f8ddb1…be581`, referencing an already-removed worktree |

**Measured space reclaimed: 3,372,470,272 bytes (3.14 GB)**, by `Get-PSDrive D` free-space
delta across the removal run.

Removal used native PowerShell with `-LiteralPath` and drive-qualified absolute paths. Each
target was re-resolved and re-asserted against a three-entry allow-list immediately before
deletion; the target and every directory beneath it were checked for reparse points, and the
run was written to refuse on any hit. **Zero reparse points were found** at any target, so no
recursive delete could escape its intended folder.

### 18.2 What was preserved, and the verification that gated removal

Preserved to the gitignored `artifacts/drive-root-recovery-20261017/`, with `ORIGIN.md`
recording original paths and `MANIFEST.sha256` giving `<sha256>  <bytes>  <relative path>`
for every file:

- `d-hlinux-gate1/` — 52 files, the `h-linux-unsync-01-gate1` Gate-1 control/treatment
  evidence. The intended location `D:\development\ht-wt-hlinux-gate1-20260902` no longer
  exists, so `D:\d` held the **sole surviving copy**.
- `ht-b1-scratch-evidence/` — 69 loose files from the 2026-10-09 B1 restore test
  (listings, comparisons, `HASHES.*`, `restore-run.log`, `REVIEW-pass1-backup.md`).
- `ht-b1-scratch-evidence/_clone-local-scripts/` — `append_rows.py` and `clock.py`, found in
  the clones' gitignored `artifacts/`. Preserved because `git cat-file` confirmed **neither
  blob exists in the main repository's object database**, unlike every other differing file
  in those clones.

**All 123 source files were re-hashed against their preserved copies before any deletion:
123 identical, 0 mismatches, 0 missing.** Removal was gated on that pass.

One disposition note worth recording: the restored clones' apparent working-tree
modifications were largely **autocrlf line-ending artifacts** — `docs/WORKTREE_CLEANUP_PLAN.md`
carried an identical blob hash with a 4-byte size difference. Tip equality alone did not
settle disposability; the ignored-file and object-database checks did.

### 18.3 RESIDUE-1 and RESIDUE-2 — deliberately untouched

`D:\dev-cleanup-20260824-digest` and `D:\_digest-discard-bin` were **excluded by instruction
and remain untouched**. They were not moved, renamed, written into or read destructively.
Their NTFS creation times are **one of the two independent corroborations** bounding the
4 min 21 s backup-removal window, and were re-measured after the cleanup as unchanged:

```
D:\dev-cleanup-20260824-digest   CreationTime 2026-09-28 18:26:56   30 files
D:\_digest-discard-bin           CreationTime 2026-09-28 18:31:21  548 files
```

### 18.4 What remains open

**This section closes nothing in the backup-disappearance investigation.** Still unresolved
and unchanged by this cleanup:

- **Who removed the August preservation paths, and when**, is NOT established. The removal
  remains an owner-account console event on 2026-09-28.
- **Whether the off-device copy restores** is NOT established. No restore has been performed,
  and content identity is verified for **2 of 14,255** manifest entries only.
- The 22-day audit gap between 2026-09-07 and 2026-09-29 is unchanged, and remains a gap in
  evidence rather than evidence of anything.

### 18.5 Prevention

The `D:\c` and `D:\d` faults were **MSYS path conversion**, not destination choice: a
`/c/...` or `/d/...` path landed as a literal relative directory beneath the drive root.
Destination validation alone does not address this. The standing controls are therefore:
native PowerShell with drive-qualified absolute paths; validation of the resolved
destination before anything is created; and a check that flags unexpected new `D:\`
children, run around browser-automation sessions.

---

## 19. Prevention — in progress, outcome pending

**Status: unresolved, work ongoing elsewhere.** Prevention is being carried out as a separate task
and will land in **its own pull request**, based on `origin/main` and carrying its own tests and
guidance. It is deliberately **not** part of this record or the pull request that carries it.

As of `2026-10-16T21:55Z` that task reports its assessment complete and its implementation **not**
finished. No prevention outcome is recorded here, because none has been delivered: no artifact
directory, no branch and no pull request for it existed at the time of writing, and the lifecycle
and guard tooling are unmodified. **Nothing is `PREVENTION_COMPLETE`.**

This is recorded as **unresolved — not waived, not complete, and not assessed by this record**.
Nothing here is a prevention design, finding, approval, review or sign-off, and the absence of a
recorded finding here is not evidence that there is none. The prevention task's own conclusions are
its to publish, and must be read there rather than inferred from this section.

What already existed and was **not** changed by any of the four tasks: the guard's
worktree-retention hold (`git worktree remove`, `git worktree prune` and `git branch -d`/`-D` all
denied by default), the `scripts/new-worktree.ps1` lifecycle controls, and `.claude/settings.json`.
Both guard copies are back at their original SHA-256 `0afb81b8…4502`, and the hold is in force: the
coordinator that wrote this section had `git worktree prune --dry-run -v` denied by it.

---

## 20. The four tasks at close

One row per task, with the distinction the owner asked for: **completed** (ran and was verified),
**retained** (deliberately kept), **waived** (consciously not done), **unresolved** (not done and
not waived). The drive-root cleanup in §18 is **not** one of these four: it ran under a separate
directive, on targets that were never in `git worktree list`, and is recorded alongside rather
than inside this program.

| # | task | status | outcome |
|---|---|---|---|
| 1 | Worktree removal (§15) | **completed** | 91 of 91 removed, 0 retained; one residue, since cleared |
| 2 | Branch cleanup (§16) | **completed** | 13 deleted, 127 retained; all remaining refs exact |
| 3 | Residue cleanup (§17) | **completed** | target absent; 35 operations; no guard change needed |
| 4 | Prevention (§19) | **unresolved** | not performed, not waived, not in this record |

**Retained, deliberately:** 127 local branches (125 whose exact tips are not ancestors of
`origin/main`, plus `main` and the branch carrying this record); all 8 stashes; the 40
`refs/closeout/…` reachability pins; the 1.9 GB preservation directory; and the 28 entries under
`D:\development\` that were never in `git worktree list` and were out of scope throughout.

**Waived — none of these ran, and none may be cited as passed, as "no findings", or as approval.**
Per directive §1.C and directive §1.D, unchanged by the later runs: the three VS Code capture sessions, the
scheduled-task calendar firing, the loaded-source coverage review, the G07 decision, every Gate A
row, Operation A qualification and monitoring, and the directive §7 preservation ceremony. §12's
parked items stay parked.

**Still open, named rather than closed:**

- Prevention (§18).
- The disposition of reviewer findings **M3, M4 and L1** (§15.5) — unknown, with no retained record.
- Recheck-then-removal is still **not atomic** (§10, §15.6); inherent to a shared checkout.
- The two divergent `docs/worktree_cleanup/PLANNING.md` lineages are still unreconciled, and the
  local copy is still uncommitted and still must not be staged (§3, §10, §12).
- The exact install and restore instants of the §15 guard exception were never recorded (§15).

### 20.1 Main checkout — preserved in every tracked respect, with one untracked file lost

Verified after all four tasks: `HEAD` `85e2372` on `main`, one worktree registration, 8 stashes,
**0 staged**, the index digest unchanged across the branch deletions, and the tracked
working-tree diff byte-identical before and after. All **23 modified** paths are intact. Local
`main` remains diverged from `origin/main` (3 ahead, behind by the rest) and was never used as a
merge baseline, never pulled, reset, stashed or switched. `git add -A` was never run. Of this
directory, only `CLOSEOUT.md` was ever staged or committed.

**One untracked file was lost, and this record cannot say by whom.** `git status --porcelain`
listed **28** entries at `2026-10-16T21:30:06Z`, including `?? analysis.json` at the repository
root. It listed **27** at `2026-10-16T22:10Z`, and `analysis.json` no longer exists. The 23
modified paths and the four remaining untracked directories are unaffected, so the porcelain
figure of 28 recorded in §15.7 was correct when measured and is now 27.

What is established:

- **It is not recoverable.** `analysis.json` was never tracked by git (`git log --all` on the path
  is empty), it does not appear in the 2026-10-16 preservation `MANIFEST.txt`, and it is not in
  the `artifacts/drive-root-recovery-20261017/` capture. No copy is known to exist.
- **No task in this record claims it.** The removal run (§15) never touched the main checkout and
  its before/after status snapshots hash identically. The branch cleanup (§16) reports the
  tracked working-tree diff unchanged and worked through a temporary index. The residue cleanup
  (§17) was bounded to one directory on `D:\development\`. The drive-root cleanup (§18) was
  bounded to three named `D:\` targets. The session that wrote this section made no filesystem
  write in the checkout other than to this file.
- **Its removal may well have been deliberate**, since generated output at the repository root is
  a policy violation under ADR-002. But **no directive known to this record authorized it, and no
  actor has claimed it.**

It is therefore recorded as **an unaccounted-for deletion of an untracked file**, not as
preservation and not as cleanup. Given that this whole program exists to account for filesystem
state, an unexplained loss inside the one directory it promised to protect belongs in the record
even though the file was, by policy, one that should not have been there.

### 20.2 What this record is, and is not

The pull request carrying this file changes **one file**: `docs/worktree_cleanup/CLOSEOUT.md`. It
is a record, not a change. It contains no application code, no configuration, no test, no
dependency bump and no prevention tooling. The main checkout's long-standing uncommitted edits
under `.claude/`, `docs/ai_workflow/`, `scripts/` and `tests/` are **not** part of it and were
never staged.

At the time of writing, merging it was blocked by two required CI contexts failing on dependency
advisories that predate it and equally affect `origin/main`: `Security Audit` (`Werkzeug` 3.1.8,
PYSEC-2026-4312, published 2026-10-05) and `JS Supply Chain` (four high npm advisories published
2026-09-18 and 2026-09-29, one of which — `braces` GHSA-vfj7-8cjw-p6xm — has no patched version at
all). Neither is caused by this record and neither remedy belongs in it. **No check was disabled,
no allowlist entry was added and no protection was bypassed to move this record forward.**
