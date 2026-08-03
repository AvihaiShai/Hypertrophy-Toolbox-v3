# P1.2 — Worktree and generated-artifact cleanup

Execution goal for [`LEFTOVERS_BY_PRIORITY.md`](LEFTOVERS_BY_PRIORITY.md) row **P1.2**
("Remove obsolete worktrees and generated artifacts"), which has stood at 0% across
six audit revisions because it was never converted from a warning into a procedure.

Status: **READY** (v23 classified it WAIT; see §2 — the named condition is now satisfied).
Owner gate required before Packet C and Packet D only.

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
git worktree list --porcelain | grep -c '^worktree '               # must equal 8
git worktree prune --dry-run                                       # must print nothing
```

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

| Path | Branch | HEAD | PR | Proof | Action | Date |
|---|---|---|---|---|---|---|
| _(pending execution)_ | | | | | | |
