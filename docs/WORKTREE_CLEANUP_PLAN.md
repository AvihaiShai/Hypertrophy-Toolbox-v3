# P1.2 — Worktree and generated-artifact cleanup

Execution goal for [`LEFTOVERS_BY_PRIORITY.md`](LEFTOVERS_BY_PRIORITY.md) row **P1.2**
("Remove obsolete worktrees and generated artifacts"), which has stood at 0% across
six audit revisions because it was never converted from a warning into a procedure.

Status: **PARTIAL — WORKTREE REMOVAL COMPLETE; GENERATED-ARTIFACT PACKET NOT EXECUTED.**
Owner gate remains required for artifact and preserved-worktree disposition decisions.

> **Execution update — 2026-08-08, attempt 6.** A fresh 50-worktree / 305-PR /
> `ls-remote` gate found all 40 candidates eligible and 10 KEEP rows. All 40 were removed
> non-forced after an immediate per-path identity/cleanliness check; 0 skipped, 0 failed.
> The final registry contains exactly the 10 KEEP rows recorded in §9, and prune dry-runs
> were empty before and after the no-op prune. No branch was deleted. Twenty deregistered
> paths retain only validated `.venv`/`node_modules` junctions into shared main; they were
> deliberately not recursively or manually deleted. This update supersedes the dated §5
> counts and completes the worktree half only; §6's artifact work remains open.

> **Reconciliation — 2026-08-10, against `origin/main` `8b5231a`.** The removal held:
> **0 of the 41 REMOVED paths in §9 are registered again**, `git worktree prune --dry-run`
> is still empty, and 20 of them still carry the junction-only shells described above.
> The registry has since moved on its own — it now reads **12**, not 10 — so the count is
> not the invariant and §7's check has been reworded accordingly. Three registrations are
> new work by other sessions, and one KEEP row was removed externally. Details in §9.1.

---

## 1. Goal

Return the machine to a defensible working state:

- **Worktrees:** 42 registered → 8 retained. Every removal proven disposable by the
  §4 test; every retention justified by a named reason.
- **Generated artifacts:** 2.5 GB of `artifacts/` + `build/` + `dist/` + `logs/`
  reduced to the protected subset, without deleting anything an open investigation reads.
- **The row closes.** `P1.2` moves to RETIRE with a recorded disposition per path, so
  the next audit recounts against a ledger instead of re-deriving from scratch.

### Definition of done

1. `git worktree list --porcelain` reports only the §5 retained set, and `git worktree prune`
   is a no-op afterwards.
2. Every removed path has a ledger row: path, branch, HEAD OID, PR, proof used.
3. Every retained path has a ledger row naming the reason it was kept.
4. No branch was deleted. Branch deletion is **out of scope** — see §7.
5. `docs/LEFTOVERS_BY_PRIORITY.md` P1.2 updated to RETIRE with a pointer to the ledger.
6. Working tree of the shared checkout is clean and still on `main`.

> **Corrected 2026-08-10 by execution.** Two of these were written wrong.
> **(1)** is not testable as stated: this is a live machine, and legitimate new worktrees
> appear between any two commands — three did during this packet's own reconciliation. The
> real invariant is *set-based, not count-based*: **no §9 REMOVED path is registered, and
> every §9 KEEP path either is registered or has a recorded disposition in §9.1.**
> **(5)** overreached: only the worktree half ran, so P1.2 goes to **PARTIAL**, not RETIRE.
> RETIRE needs §6 as well. (2), (3), (4) and (6) are met.

### Out of scope / non-goals

- Deleting branches (worktree removal and branch deletion are separate risks).
- Touching `data/`, `data/auto_backup/`, or any `.db` file — that is P1.7's lane.
- Any change to application code, tests, or CI. This packet is filesystem-only.
- `git reset --hard` or `git clean -f` anywhere in the recovery path — both are
  **denied** by the guard hook (§3) and no step may depend on them.

---

## 2. Why the WAIT gate is discharged

v23 classified P1.2 as **WAIT** on two conditions. Both are now false:

| v23 gate | State on 2026-08-03 | Effect |
|---|---|---|
| "known dirty/open-PR worktrees must be excluded" | Still true as a *rule*, but the specific set is now enumerable and small — 4 dirty, 2 open-PR-bound (§5). | Rule kept as §4 procedure; no longer a blocker. |
| `D:/development/HT-v23-audit` — "remove it only after P1.0 has published the branch" | P1.0 shipped. `docs/leftovers-v23-audit` merged as **PR #278** (`c0dff15`). | The audit worktree is now removable in Packet A. |

Also note: the v23 open-PR hold list (**#245, #250, #274, #275**) is entirely stale.
All four are closed or merged. The live hold list is **#286** and **#281** only.

---

## 3. Non-negotiable safety rules

These come from the guard hook and from what the v18→v23 audit arc actually observed.
They are constraints on *how* the work runs, not preferences.

1. **`git worktree remove` prompts.** Intercepted at
   [`guard-destructive-command.ps1:438-440`](../.claude/hooks/guard-destructive-command.ps1)
   with decision **`ask`**. An unattended agent run **stalls, it does not proceed** —
   so this packet must be run interactively, or each removal pre-approved. Do not
   attempt to route around the hook.
2. **`git reset --hard` is denied** at `:397`, and `git clean -f` at `:403`. No recovery
   step may assume either exists.
3. **Never recursively delete a registered worktree.** `rm -rf` on a worktree path
   leaves a dangling registration and loses the safety metadata. Always
   `git worktree remove <exact-path>`, then `git worktree prune` once at the end.
4. **Re-derive every count at execution time.** The registered-worktree count has read
   24 → 25 → 29 → 30 → 35 → **42** across revisions. Every number in this document is
   *evidence from 2026-08-03*, never an execution input.
5. **The shared checkout is not yours.** It switched branch mid-audit once already.
   Never `git checkout` in `D:/development/Hypertrophy-Toolbox-v3-main`; never
   `git add -A` there.
6. **Squash merges defeat ancestry and patch-equivalence.** `git cherry main <head>`
   reports false uniques for every squash-merged branch here — measured: 14 of 31
   merged branches show `uniq>0` purely as a squash artifact. Merge proof comes from
   the PR state, not from `git cherry`. See §4.

---

## 4. The disposability test

Run for **every** non-current worktree. A worktree is removable only if all four pass.

```bash
# 1. Dirty check — ANY output means skip and preserve.
git -C "$WT" status --short --untracked-files=all

# 2. Identity — record before touching anything.
git -C "$WT" rev-parse --abbrev-ref HEAD    # branch (or HEAD if detached)
git -C "$WT" rev-parse HEAD                 # OID

# 3. PR association — all states, not just open.
gh pr list --state all --head "$BRANCH" --json number,state,title

# 4. Unique-content proof.
git rev-list --count main..$OID             # 0 => strictly contained in main
git cherry main $OID | grep '^+'            # non-empty => inspect, do not assume unique
```

**Decision table**

| Dirty | PR state | `main..HEAD` | Verdict |
|---|---|---|---|
| any output | — | — | **PRESERVE** — investigate the working tree first |
| clean | OPEN | — | **PRESERVE** — active PR |
| clean | MERGED | any | **REMOVE** — content landed; `git cherry` noise is a squash artifact |
| clean | none | 0 | **REMOVE** — contains nothing `main` lacks |
| clean | none | > 0 | **OWNER** — real unpublished local work; do not guess |

Rule 6 of §3 is why row 3 reads the way it does: with a MERGED PR, `git cherry` is
evidence of *how* it merged, not of whether the work survives.

---

## 5. Disposition — evidence snapshot, 2026-08-03

42 registered worktrees (41 non-current). **34 removable, 7 preserved, 1 current.**

### Packet A — merged-PR worktrees, clean (31 removals)

Each has a merged PR and a clean working tree. Bulk of the reclaim.

| Worktree path (suffix after `Hypertrophy-Toolbox-v3-`) | Branch | PR |
|---|---|---|
| `HT-v23-audit` *(full path `D:/development/HT-v23-audit`)* | `docs/leftovers-v23-audit` | #278 |
| `app-py-p1-handlers` | `wt/app-py-p3-cleanup` | #235 |
| `bs538-rebuild` | `wt/playwright-lockstep` | #283 |
| `ci-inv-text` | `docs/ci-inventory-summary-text` | #271 |
| `invdrift` | `wt/inventory-drift-blocking` | #267 |
| `ki006-modal-keyboard` | `wt/ki006-modal-keyboard` | #284 |
| `main/.claude/worktrees/agent-a079c616d5d9a5cb4` | `docs/wp4-4-p2-quality-gate-css-row` | #222 |
| `main/.claude/worktrees/agent-aa6ae3dc2a05b8161` | `docs/wp4-4-p1-linux-reds-ledger` | #223 |
| `main-bootstrap-538-compat` | `wt/bootstrap-538-compat` | #274 |
| `main-n4-checkpoint` | `wt/wp4-4-k-integration` | #217 |
| `main-node24-ci` | `wt/node24-ci` | #275 |
| `main-p3-a0-audit` | `wt/p3-a0-audit` | #280 |
| `main-visual-helper` | `wt/wp4-4-visual-helper-band` | #211 |
| `main-wp4-4-b-base` | `wt/wp4-4-b-base` | #192 |
| `main-wp4-4-d1-a11y` | `wt/wp4-4-d1-a11y` | #197 |
| `main-wp4-4-d2-a11y` | `docs/wp4-4-d2-evidence-corrections` | #204 |
| `main-wp4-4-e-layout` | `wt/wp4-4-e-layout` | #195 |
| `main-wp4-4-g-components-audit` | `wt/wp4-4-g-components-audit` | #207 |
| `main-wp4-4-g-terminology-correction` | `wt/wp4-4-g-terminology-correction` | #209 |
| `main-wp4-4-h-components-dead` | `wt/wp4-4-h-components-dead` | #208 |
| `main-wp4-4-i-is-repair` | `wt/wp4-4-i-oracle-provenance` | #215 |
| `main-wp4-4-j` | `wt/wp4-4-j-theme-dark` | #216 |
| `p1-7-sidecars` | `chore/p1-7-sidecar-cleanup` | #285 |
| `p4-audit` | `docs/p4-verification-closeout` | #257 |
| `p4stop` | `docs/phase4-stopgap-ledger` | #273 |
| `p5fix` | `wt/app-py-p4-version-buster` | #236 |
| `testing-phase01` | `wt/testing-execution-log` | #255 |
| `tsdrift` | `docs/testing-strategy-status-drift` | #270 |
| `verify` | `fix/post-merge-hardening` | #266 |
| `wpb4` | `wt/wpb4-unassigned-bucket` | #256 |
| `wpb4-plan` | `docs/closeout-stale-instructions` | #265 |

> The two `.claude/worktrees/agent-*` entries are **harness-created**, not owner-created.
> Remove them the same way, but expect the harness to recreate equivalents later; they
> are not a recurring leak to fix here.

### Packet B — no PR, nothing unique, clean (3 removals)

`main..HEAD` is empty, so these contain nothing `main` lacks.

| Worktree path suffix | Branch | Evidence |
|---|---|---|
| `docs-status-row` | `rescue/p1-refinement-probe` | ahead=0 |
| `prep4` | detached `99c5a36` | ahead=0 |
| `vbl` | detached `489a7ce` | ahead=0 |

### Packet C — PRESERVE, dirty (4)

Uncommitted content. **Do not remove.** Each needs a separate disposition decision.

| Worktree path suffix | Branch | Dirty files | Note |
|---|---|---|---|
| `bs538-spike` | `wt/bs538-spike` | 4 | Also 1 unpublished commit, no PR. The #274 source. |
| `main-p1-6-deps-closeout` | `wt/p1-6-deps-closeout` | 2 | ahead=0 — the *only* content is uncommitted. |
| `main-visual-determinism` | `wt/visual-determinism` | 6 | Also PR **#286 OPEN** (draft, Gate 2 FAILED). Double hold. |
| `main-wp4-4-f1-navbar` | `wt/wp4-4-f1-navbar` | 2 | PR #199 merged, but the dirty files are not in it. |

### Packet D — PRESERVE, owner decision (3)

| Worktree path suffix | Branch | Reason |
|---|---|---|
| `visual-recovery-update` | `recovery/linux-visual-baselines` | PR **#281 OPEN** (draft, frozen pending owner review of 84 PNGs). Hard hold. |
| `main-stylelint17` | `probe/stylelint17` | 1 unpublished commit, no PR. Probe — publish or discard? |
| `sep` | `fix/tbl-separator-contrast` | 2 unpublished commits, no PR. Real fix — publish or discard? |

### Retained set after execution (8)

`main` (current) + the 7 in Packets C and D.

---

## 6. Generated artifacts — measured 2026-08-03

| Path | Size | Disposition |
|---|---|---|
| `artifacts/` | **2.3 GB** | Selective — see below |
| `dist/` | 92 MB | Delete — PyInstaller output, regenerable |
| `build/` | 76 MB | Delete — PyInstaller intermediate, regenerable |
| `logs/` | 63 MB | Truncate — keep the current `app.log`, drop rotations |
| `debug/` | 145 KB | Delete |

`artifacts/` breakdown:

| Subpath | Size | Disposition |
|---|---|---|
| `wp4_4` | 643 MB | **HOLD** — protected bundle, pending its own explicit decision |
| `playwright` | 522 MB | Delete — regenerable test output |
| `environment-backups` | 460 MB | **OWNER** — name implies recovery value; confirm before deleting |
| `pr281_owner_audit` | 84 MB | **HOLD** — #281 is open and under owner review |
| `vd_gen1` / `vd_gen2` / `vd_gen3` | 191 MB | **HOLD** — #286 visual-determinism evidence, PR open |
| `visual_review*` (3 dirs) | 155 MB | Delete after confirming #281/#286 do not cite them |
| `_a2zip` / `_a3zip` | 118 MB | Delete — scratch archives |

Roughly **0.9–1.4 GB** reclaimable without touching a held path; ~1.9 GB if
`environment-backups` is cleared too.

**Precondition for every artifact deletion:** confirm no open PR body, evidence doc,
or running process references the path. `#281` and `#286` are both open — anything
they cite is held until they close.

---

## 7. Sequence

| Packet | Content | Gate | Effort |
|---|---|---|---:|
| **A** | 31 merged-PR worktree removals + one `git worktree prune` | none — proof is mechanical | 30–45 min |
| **B** | 3 nothing-unique worktree removals | none | 5 min |
| **C** | Ledger + `LEFTOVERS_BY_PRIORITY.md` P1.2 → RETIRE | none | 20 min |
| **D** | Artifact deletions, held paths excluded | **OWNER** on `environment-backups` | 20 min |
| **E** | Packet C/D worktree dispositions (7 preserved) | **OWNER** — one decision per path | 30 min |

A and B are the value; run them first and independently. D and E are separable and
can stay open without blocking closure of the row's worktree half.

Run A and B **interactively** — §3 rule 1 means an unattended run stalls at the first
`git worktree remove`.

### Verification

Filesystem-only packet, so the suite is not the gate — but run it once at the end to
prove nothing in the shared checkout moved:

```bash
git -C D:/development/Hypertrophy-Toolbox-v3-main status --short   # must be empty
git worktree list --porcelain                                      # compare as a SET, see below
git worktree prune --dry-run                                       # must print nothing
```

**Do not assert a worktree count.** An earlier revision of this block asserted `8`, and the
execution update briefly replaced it with `10`; both were stale within two days, and during
this packet's own reconciliation the registry grew from 10 to 12 between two consecutive
commands. Other sessions create worktrees legitimately and continuously. Compare the
porcelain output against §9 as a set instead: **no REMOVED path may appear, every KEEP path
must appear or carry a §9.1 disposition, and anything else is new work belonging to another
session — not this packet's residue and not evidence of failure.**

Only if `artifacts/` deletions touched a path a test reads: `/run-tests`.

---

## 8. Risks

| Risk | Mitigation |
|---|---|
| Squash-merge false uniques cause a wrongly-preserved worktree | Accepted — the failure mode is *keeping* something, which is recoverable. Never invert this. |
| A worktree becomes dirty between the scan and the removal | Re-run the §4 dirty check immediately before each `git worktree remove`, not once up front. |
| The guard hook stalls an unattended run | Run interactively. Do not disable the hook. |
| A held artifact path is deleted because its PR closed mid-run | Re-check `gh pr view 281 286` before Packet D, not before Packet A. |
| The count changes again before execution | Expected — §3 rule 4. Re-derive; this document is evidence, not input. |

---

## 9. Ledger

Populated during execution. One row per path, removed or retained.

**51 rows = 41 REMOVED + 10 KEEP.** The 41 is not a contradiction of the "40 candidates"
figure in the execution update: `…-pyright-fc` was already gone when attempt 6 derived its
registry — the #307 session removed it — so it is carried here as **REMOVED EXTERNALLY**
for continuity but was never one of the 40 this packet acted on. 50 registered = 40 + 10.

| Path | Branch | HEAD | PR | Proof | Action | Date |
|---|---|---|---|---|---|---|
| `…-v3-main` | `main` | `4025295` | — | Shared current checkout | **KEEP** | 2026-08-08 |
| `D:/development/HT-v23-audit` | `docs/leftovers-v23-audit` | `9dc4eef` | #278 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `D:/development/HT-v3-winregen` | `fix/win32-visual-baseline-regen` | `b990412` | — | Unpublished, only copy | **KEEP** | 2026-08-08 |
| `…-app-py-p1-handlers` | `wt/app-py-p3-cleanup` | `c485521` | #235 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-awi` | `wt/agent-workflow-integrity` | `2bddd98` | #292 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-bs538-rebuild` | `wt/playwright-lockstep` | `44976f4` | #283 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-bs538-spike` | `wt/bs538-spike` | `d72d00e` | — | 4 dirty entries | **KEEP** | 2026-08-08 |
| `…-ci-inv-text` | `docs/ci-inventory-summary-text` | `a6e7843` | #271 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-dnone` | `wt/dnone-visibility` | `f93040e` | #303 open | Open draft; 3 local commits ahead | **KEEP** | 2026-08-08 |
| `…-docs-status-row` | `rescue/p1-refinement-probe` | `57027ab` | — | Mandated preservation | **KEEP** | 2026-08-08 |
| `…-invdrift` | `wt/inventory-drift-blocking` | `5ccb66d` | #267 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-ki006-modal-keyboard` | `wt/ki006-modal-keyboard` | `36f0c8a` | #284 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main/.claude/worktrees/agent-a079c616d5d9a5cb4` | `docs/wp4-4-p2-quality-gate-css-row` | `f20a85c` | #222 merged | Fresh §3 gate; nested harness row | **REMOVED** | 2026-08-08 |
| `…-main/.claude/worktrees/agent-aa6ae3dc2a05b8161` | `docs/wp4-4-p1-linux-reds-ledger` | `5f52d82` | #223 merged | Fresh §3 gate; nested harness row | **REMOVED** | 2026-08-08 |
| `…-main-bootstrap-538-compat` | `wt/bootstrap-538-compat` | `905950a` | #274 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-n4-checkpoint` | `wt/wp4-4-k-integration` | `81872c7` | #217 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-node24-ci` | `wt/node24-ci` | `95f51ca` | #275 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-p1-2-cleanup` | `wt/p1-2-cleanup` | `d53c800` | — | Assigned execution checkout | **KEEP** | 2026-08-08 |
| `…-main-p1-6-deps-closeout` | `wt/p1-6-deps-closeout` | `88f6f96` | #289 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-p3-a0-audit` | `wt/p3-a0-audit` | `df0d0a5` | #280 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-stylelint17` | `probe/stylelint17` | `fb0e059` | — | Unpublished Stylelint 17 probe | **KEEP** | 2026-08-08 |
| `…-main-visual-determinism` | `wt/visual-determinism` | `160b1a8` | #286 merged | HEAD contained in `origin/main` | **REMOVED** | 2026-08-08 |
| `…-main-visual-helper` | `wt/wp4-4-visual-helper-band` | `3b74901` | #211 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-wp4-4-b-base` | `wt/wp4-4-b-base` | `62ac008` | #192 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-wp4-4-d1-a11y` | `wt/wp4-4-d1-a11y` | `b83c3eb` | #197 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-wp4-4-d2-a11y` | `docs/wp4-4-d2-evidence-corrections` | `0564716` | #204 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-wp4-4-e-layout` | `wt/wp4-4-e-layout` | `6b709c5` | #195 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-wp4-4-f1-navbar` | `wt/wp4-4-f1-navbar` | `96eb844` | #199 merged | 2 dirty junction entries | **KEEP** | 2026-08-08 |
| `…-main-wp4-4-g-components-audit` | `wt/wp4-4-g-components-audit` | `0309043` | #207 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-wp4-4-g-terminology-correction` | `wt/wp4-4-g-terminology-correction` | `8ada8f6` | #209 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-wp4-4-h-components-dead` | `wt/wp4-4-h-components-dead` | `5503a23` | #208 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-wp4-4-i-is-repair` | `wt/wp4-4-i-oracle-provenance` | `f01e0b4` | #215 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-main-wp4-4-j` | `wt/wp4-4-j-theme-dark` | `ca6f127` | #216 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-p1-7-sidecars` | `chore/p1-7-sidecar-cleanup` | `edc61a8` | #285 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-p13-p18-closeout` | `wt/p13-p18-closeout` | `108c50d` | — | Unpublished docs closeout | **KEEP** | 2026-08-08 |
| `…-p4-audit` | `docs/p4-verification-closeout` | `97754a4` | #257 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-p4stop` | `docs/phase4-stopgap-ledger` | `5b41464` | #273 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-p5fix` | `wt/app-py-p4-version-buster` | `c64a809` | #236 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-prep4` | detached | `99c5a36` | — | Proven ancestor of `origin/main` | **REMOVED** | 2026-08-08 |
| `…-pyright-fc` | `wt/pyright-fatigue-context` | `93e54fb` | #307 merged | Removed by #307 session before attempt 6 | **REMOVED EXTERNALLY** | 2026-08-08 |
| `…-scale-btn` | `wt/scale-btn-cleanup` | `f61e3f4` | #302 open | Open draft | **KEEP** | 2026-08-08 |
| `…-sep` | `fix/tbl-separator-contrast` | `25d8ce9` | #290 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-tblhelpers` | `wt/css-tbl-helpers` | `fb78365` | #300 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-testing-phase01` | `wt/testing-execution-log` | `3ad0c0a` | #255 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-tsdrift` | `docs/testing-strategy-status-drift` | `bfc8039` | #270 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-vbl` | detached | `489a7ce` | — | Proven ancestor of `origin/main` | **REMOVED** | 2026-08-08 |
| `…-verify` | `fix/post-merge-hardening` | `4a5c4e4` | #266 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-visual-recovery-update` | `recovery/linux-visual-baselines` | `50447d3` | #281 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-winvis` | `docs/windows-visual-staleness` | `ffbc1c9` | #305 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-wpb4` | `wt/wpb4-unassigned-bucket` | `b636a39` | #256 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |
| `…-wpb4-plan` | `docs/closeout-stale-instructions` | `07a5ae4` | #265 merged | Fresh §3 gate | **REMOVED** | 2026-08-08 |

### 9.1 Post-execution reconciliation — 2026-08-10

Re-derived against `origin/main` `8b5231a`. **The removal held.** None of the 41 REMOVED
paths is registered again, `prune --dry-run` is empty, and 20 still carry junction-only
shells. Everything below is drift caused by other sessions after attempt 6, recorded here
rather than by rewriting the table above — none of it is this packet's residue.

| Change | Detail | Disposition |
|---|---|---|
| KEEP row removed externally | `D:/development/HT-v3-winregen` — worktree **and** branch `fix/win32-visual-baseline-regen` are gone. | **No loss.** Its commit `b990412` is contained in `recovery/win32-visual-baseline-corpus`, which shipped as **#309**. Verified with `git for-each-ref --contains b990412`. |
| KEEP row re-pointed | `…-dnone` was `wt/dnone-visibility` @ `f93040e` (#303 open); it is now `recovery/win32-visual-baseline-corpus` @ `4001fbd`. | **Its KEEP basis has expired** — #303 and #309 are both merged and the tree is clean, so §4 now classifies it REMOVE. Deferred to the owner-gated Packet E; do not act on it here. Removing the worktree would not endanger `b990412` — the branch ref survives worktree removal. |
| Shared checkout advanced | `…-v3-main` `4025295` → `8b5231a`. | Expected. Not drift. |
| Three new registrations | `…-main-xdist`, `…-main-single-exercise-catalog-fetch`, `…-main-unlink-button-visibility`. | **Out of scope.** Active work owned by other sessions. Two appeared mid-reconciliation. |

Still-valid KEEP rows: 8 of 10 unchanged (`…-v3-main` advanced, `…-dnone` re-pointed,
`HT-v3-winregen` gone). `…-scale-btn` remains a genuine hold — **#302 is still open.**

The "No branch was deleted" claim in §1 and the execution update is about *this packet's*
actions and remains true. One branch has since been deleted by another session
(`fix/win32-visual-baseline-regen`, above); that was not this packet.
