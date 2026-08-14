# Leftovers by Priority

> **Audit snapshot:** 2026-08-02, deep-scan revision v23 (final adversarial
> audit). Codex authored v18, Opus re-verified as v19, v20 reconciled
> #264–#267, v21 added the third-model deep scan, v22 made the resulting queue
> safe and executable, and v23 audits v22 for anything factually wrong, unsafe,
> ambiguously gated, mis-sequenced, or non-executable.
>
> **Purpose:** current, evidence-based queue of unfinished work, small closeouts,
> stale plans, and disposable artifacts. This replaces the June punch list and
> its long closed-item history. Historical implementation evidence stays in the
> linked source plans, Git history, and the archive.
>
> **Authority (corrected at v23):** use freshly fetched `origin/main`, generated
> inventories, current code, and read-only runtime data ahead of old prose.
> v22's own authority note was stale in a way that inverted its instruction: it
> reported `origin/main` at `f178790` with the checkout **10 behind**. In fact
> this document's commit sits directly on top of the current `origin/main`
> (`ac16e4c`, PR #271) — **1 ahead, 0 behind**, nothing to reconcile. Every
> number in this file remains snapshot evidence: fetch, recompute divergence,
> and recount PRs/worktrees immediately before acting.

> **What v19/v20 already corrected in the plan** (kept for continuity): the
> two-edit inventory flip, the "(non-required)" naming trap, salvage of unlanded
> `…-verify` work (merged via #266), stale PR/worktree counts, classification
> of `build/`+`dist/` as disposable output, and identification — **not yet
> removal** — of the unignored SQLite sidecars.
>
> **What v21 adds — findings from angles no prior pass took:**
> **(1)** a docs-wide link-integrity sweep: **12 broken at the snapshot**,
> headlined by three *active* workflow docs claiming to implement a
> `.claude/SHARED_PLAN.md` tier system that no longer exists (new P1.8);
> **(2)** single-producer policy violations that predate the policy —
> `E2E_TESTING.md` is a hand-maintained count inventory frozen at 2026-06-10;
> **(3)** `CHANGELOG.md` stops at July 29 and records none of the August ships,
> including user-visible WPB.4; **(4)** a numbering collision between the
> grounding scan's bug list (A1–A12) and `REFACTOR_PLAN.md`'s Track A (A1–A8)
> that makes this file's own "shipped" row misleading — corrected in §2 with the
> explicit mapping; **(5)** Dependabot has re-filed the *known SCSS-breaking*
> Bootstrap 5.1.3→5.3.8 bump as #269, and #268's new ignore policy covers only
> stylelint — bootstrap files as semver-minor, so no existing rule catches it;
> **(6)** a small set of evidence/design docs has no durable inbound index link
> (the v22 candidates are named in P1.1; do not pin a count that this plan's own
> links immediately change); **(7)** the queue and
> worktree counts churn intra-day — v22 requires recount-at-execution for both
> surfaces and treats every number in this document as snapshot evidence only.

> **What v23 adds — new findings only; v18–v22 findings above are not repeated.**
>
> **N1 — HISTORICAL, discharged 2026-08-02.** The arc was published as **#278**
> (`c0dff15`) and `origin/main` now serves this document, so neither the
> unreachability nor the "origin still serves v17" claim below is still true. The
> finding is kept as written for continuity; do not act on it. *Original text:*
>
> **N1 — this plan is not reachable by anyone else, and `origin` still publishes
> the June punch list.** `git ls-remote --heads origin` has no
> `docs/status-reconciliation`; `gh pr list --head docs/status-reconciliation
> --state all` returns `[]`. Commit `2b16474` exists only on two **local**
> branches (`docs/status-reconciliation`, `wip/session-docs`). Meanwhile
> `origin/main:docs/LEFTOVERS_BY_PRIORITY.md` and the one branch that *is*
> pushed (`origin/docs/testing-strategy-reconciliation` @ `bdb1f60`) both still
> carry **v17, dated 2026-06-11**. The entire v18→v23 arc is one `git branch -D`
> from being lost, and every reader of the repository currently sees the June
> list. **Publishing this branch is the highest-value action in the file.**
>
> **N2 — the Bootstrap decision was already taken.** #269 is **CLOSED, not
> merged** (2026-08-02T00:45:22Z) and **#274 opened 20 seconds earlier** as a
> real migration: Bootstrap 5.3.8, `variables-dark`/`maps` added to the SCSS
> import graph, rebuilt bundle + map, CDN pin alignment, and a new
> `tests/test_bootstrap_version_contract.py`. #274 also corrects the diagnosis —
> the hard failure is `_root.scss` needing `$theme-colors-rgb` from the maps
> layer; the `red()`/`green()`/`blue()` messages are only deprecation warnings.
> P1.6 lane (b) is therefore **decided**; "#269 will re-file weekly" is obsolete.
>
> **N3 — the P1.5 ↔ Bootstrap hazard has already materialised.** #274's stated
> validation includes "Chromium navigation/accessibility/UI sweep — 127 passed",
> which contains exactly the tests P1.5 proves cannot fail. The upgrade is being
> validated by a modal-keyboard test structurally incapable of detecting a
> modal-keyboard regression. v22's "land P1.5 before any Bootstrap *decision*"
> is too weak and aimed at the wrong PR.
>
> **N4 — #250 is not an unexplained red; it has a named prerequisite.** #275
> (draft) diagnoses it: jsdom 30 requires Node `^22.22.2 || ^24.15.0 || >=26`
> while CI pins Node 20.20.2, so `EBADENGINE` fires and Vitest workers crash
> through undici. #275 moves all 13 `setup-node` pins to Node 24, adds
> `tests/test_node_version_contract.py`, and deliberately excludes #250.
>
> **N5 — the now-required drift gate creates generated-file contention.**
> `Test Inventory Drift` is a **required** context (11 total, read from the
> protection API). #274 and #275 both modify `docs/test_inventory/TEST_INVENTORY.json`
> and `.md`; P1.4 and P1.5 will each have to regenerate the same two files.
>
> **N6 — P1.4 and P1.5 collide on one spec file.** P1.4 edits the KI-005 header
> in `e2e/ui-hardening.spec.ts`; P1.5 adds modal assertions to the same spec and
> to `accessibility.spec.ts`. Both change test counts.
>
> **N7 — the retention constraint is harder than "QUALITY_GATE links them".**
> Six CSS evidence artifacts are **pytest-pinned** in `tests/test_css_wp4_4_*.py`
> (`_D1_A11Y_`, `_D2_A11Y_`, `_E_LAYOUT_`, `_H_COMPONENTS_DEAD_`,
> `_A_BASELINE.json`, `_1_STYLELINT_BASELINE.json`); moving one reds the required
> `Run Tests`. The seven orphan `WP4_3I_*` files are **not** test- or
> CI-referenced and are the genuinely movable subset.
>
> **N8 — cleanup executability in this repo.** `git worktree remove` is
> intercepted by `.claude/hooks/guard-destructive-command.ps1:438-440` with
> decision **`ask`** (an unattended run stalls rather than proceeds) and
> `git reset --hard` is **denied** outright at `:397`. Worktrees are now **35**
> (24→25→29→30→35 across revisions) with three dirty; and the shared checkout
> **changed branch mid-audit** (`docs/testing-strategy-reconciliation` →
> `docs/p3-gate-signoff`), which is the recount rule proving itself.
>
> **N9 — HISTORICAL, re-checked 2026-08-04.** `CROSS_MODEL_ORCHESTRATION_PLAN.md`
> is tracked on `main`, and `git status --untracked-files=all docs/ai_workflow/`
> in the shared checkout is now clean — the loose duplicate is gone, so there is
> no longer a fork risk. *Original text:* a duplicate of the orchestration plan
> was committed here *and* sat untracked in the shared checkout; committing that
> copy on another branch would have forked the document.
>
> **N10 — this document did not render correctly.** The P1.4 row contained a raw
> `|` inside `{{ exercises|length }}`, splitting it into six cells in a
> five-column table, so GitHub dropped the trailing content of the row that
> describes the debug block. Fixed at v23 by escaping the pipe. Anything quoting
> Jinja, shell pipes, or regex alternation inside these tables must escape `|`.

> **v27 — post-#359 canonical reconciliation, 2026-08-14 (later the same day as
> v26). Docs-only; one item retired, nothing promoted.** Verified against
> `origin/main` at **`fbb76f5`** with **zero open PRs** on the repository.
> **P2.7 is RETIRED** — the checkout-name-dependent consult test that v26's run
> had only just recorded (#354, `52c5a78`) was fixed the same day by **#357**
> (`e84d19c`), which derives the escape path from `REPO.name`. **One v26
> statement is corrected rather than retired:** v26 said *"Testing Phase-2 Packet
> A shipped as #342, while Packets C/D remain queued"* — **Packet C (strict
> console) shipped as #362** (`52331bf`); **only Packet D (axe) is still
> queued**, and with no open PR its completion is not predicted here.
> Separately, **#361** (`a224b39`) discharged the *cross-model* plan's Packet C
> (charter and contract hygiene), which is a different packet series from Testing
> Phase-2's and does not touch the `$orchestrate` bullet below. **Consequence at
> v27: P2.7 was the section's only executable row, so P2 now holds exactly one
> live item — P2.4, which is OWNER / demand-gated.** The live database was not
> read.

> **v26 — integration truth reconciliation, 2026-08-14.** Two more execution
> items are retired: **P2.2** shipped as #339 (`ea82ef1`), and the compiled-CSS
> drift proposal shipped as #335 (`542df07`) with the stronger bundle-plus-map
> pathspec. Two broader bullets are corrected rather than falsely retired:
> Testing Phase-2 Packet A shipped as #342, while Packets C/D remain queued; the
> one-shot cross-model consult shipped as #344/#348, while heavy `$orchestrate`
> remains deliberately unimplemented. Product docs remain retired. No proposal
> is promoted by this reconciliation.

> **v25 — P2.1 owner decision recorded, 2026-08-13. Docs-only; one item retired, nothing promoted.** The owner closed the Fatigue *Phase 2* Stage 4 calibration window as **no real-use evidence / no threshold change**, kept Learned Calibration **2D-D** parked, and authorised retiring only observer *instructions* or generated artifacts **proven regenerable and unpinned**. Evidence re-verified read-only that day — see [`PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md) §5 Stage 4. **No file was deleted:** both named artifact families failed the *proven-regenerable* half of the bar (measurement in §10 there), and the observer scripts plus their 26 tests were explicitly kept for a possible restart. **Consequence at v25: OWNER-gated items dropped from three to two (P2.2, P2.4).** Docs-only; the live database was read-only throughout.
>
> **v24 — truth-maintenance pass, 2026-08-13. Docs-only; no finding is new and no
> item is promoted.** This revision does one thing: it stops the file presenting
> already-shipped work as currently actionable. Verified against `origin/main`
> at **`af14036`** (checkout **0 ahead / 0 behind**). The pass opened against
> `ae37365`; **#330** (`af14036`, the session-summary Pyright typing fix) landed
> mid-pass, so every premise below was **re-verified at `af14036`** rather than
> carried forward. #330 touches `utils/session_summary.py`, two
> `tests/test_session_summary*.py`, the Pyright baseline and the generated test
> inventory — a file set disjoint from everything this revision claims.
> Five reclassifications, each with the evidence that retires it:
>
> | Item | Was | Now | Evidence re-verified at `af14036` |
> |---|---|---|---|
> | **P1.5 / KI-006** | READY | **RETIRE** | **#284**, squash `4e9b7d0` |
> | **P1.7** | READY | **RETIRE** | **#285**, squash `4a24773` |
> | **P1.2** | PARTIAL wording still live in the row + final sequence | **RETIRE** (already so in the classification block) | **#327**, `ae37365`; [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9.5 |
> | **P2.3** | OWNER, open execution item | **RETIRE** as an execution item; residual is owner-deferred and owned elsewhere | #281 `864043f`, #294 `73c5c46`, #298 `f8988f9`, #309 `10ba89f` |
> | **P2.5** | unclassified — the v23 block named only P2.1–P2.4 — but the row read as a live finding with a 2–4 h estimate | **RETIRE** | **#286**, merge `9683f77` (incl. `160b1a8`) |
>
> **One further factual correction, not a reclassification:** the P3 bullet on
> inert `d-flex` / `d-inline-block` consumers still called #303 an unmerged draft.
> **#303 merged 2026-08-08 as `42e8a4d`** (Linux baselines followed in #308,
> `99e172d`). Only the provenance sentence changed — the bullet stays a
> **PROPOSAL**, and #303 shipping the *narrowing* pre-authorizes nothing about
> *widening* it.
>
> **Consequence: P1 is fully discharged — there is no READY item left in this
> file.** Everything that remains is OWNER-gated (P2.4, the §4 taxonomy TODOs,
> and the `npm audit` severity/exception policy — P2.1 and P2.2 are retired) or
> a PROPOSAL (the remaining P3 bullets). v26 promotes nothing: no proposal
> became approved work, no owner gate was inferred as taken, and no production
> TODO disposition changed. The recomputed queue is in §6.
>
> **Method note, carried forward.** Dated blocks below are kept as written and
> annotated in place rather than rewritten — the same rule v23 applied to N1 and
> N9. A `PARTIAL`/`READY`/`OWNER` word inside a dated historical block is
> evidence of what was true on that date, never an instruction; the row header
> and §6 own current status.

## Status key

| Status | Meaning |
|---|---|
| **READY** | Small, bounded work with no unresolved product decision. |
| **WAIT** | A named external condition must become true first. |
| **OWNER** | Requires an explicit owner choice; do not infer one. |
| **PROPOSAL** | Valid future work, but not a forgotten activity or current commitment. |
| **RETIRE** | Shipped, superseded, irrelevant, or disposable after the stated safety check. |

**Current classification (v26, 2026-08-14, superseding v23–v25):** **no item in this
file is READY.** **RETIRED** — all of P1 (P1.0 #278, P1.1 #295, P1.2 #327, P1.3+P1.8
#292, P1.4 #291, P1.5 #284, P1.6 closeout doc, P1.7 #285), plus **P2.3** and **P2.5**
(and P2.6, shipped 2026-08-04), plus **P2.1** (owner decision taken
2026-08-13), plus **P2.2** (#339). **OWNER** — P2.4. Every remaining item in P3
is a **PROPOSAL**. See the v24–v26 blocks above for the per-item evidence and §6
for the queue.

> *Superseded 2026-08-13.* This line previously read: *"READY — P1.5, P1.7
> (P1.0 has since shipped as #278, and P1.4 as #291 — see §2); RETIRED — P1.2 (the
> 2026-08-12 final artifact action completed its recorded scope; see below); OWNER —
> P2.1–P2.4."* Accurate for P1.2 when written; P1.5 and P1.7 had already shipped
> (#284/#285) and P2.3/P2.5 had already been discharged by the visual-determinism and
> baseline-recovery arcs.

**P1.6 is reclassified OWNER → RETIRE (2026-08-03).** Both of its owner decisions
were taken and executed; see
[`P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md`](P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md). The
deferred Playwright 1.62.1 upgrade carried forward from it is tracked there with
an explicit unblock condition, and is **not** P1.6 residue. Artifact targets explicitly labeled safe-to-retire are
**RETIRE** only after their stated safety checks. There is no weaker "OWNER-lite"
status.

**P1.1 is RETIRED (2026-08-04).** It shipped as **#295** (squash `4d5d8cc`) and is
recorded in §2. v22's WAIT gate ("reconcile the dirty doc patch with current
`main` and #271") had already been discharged before execution and never applied.

**P1.3 and P1.8 are RETIRED (2026-08-04).** They shipped together as **#292**
(squash `db1bc5d`) and are recorded in §2. The workflow deliberately preserves
independent review: the manager or primary session runs `/verify-and-polish`
steps 2–3, while `senior-developer` runs steps 1 and 4 without receiving the
`Agent` tool.

**P1.5 is RETIRED (recorded 2026-08-13; shipped 2026-08-02).** It landed as **#284**
(squash `4e9b7d0`) and is recorded in §2. Re-verified at `af14036`: the
`accessibility.spec.ts` Escape test now waits on `hidden.bs.modal` with the comment
*"Escape is the only close path exercised here. No fallback click"* and then asserts
backdrop and `body.modal-open` cleanup — the `if (btnVisible)` guard and the fallback
click the v23 row describes are gone from it. `e2e/ui-hardening.spec.ts` adds
`expectForwardWraparound` / `expectBackwardWraparound` / `expectEscapeCloses` and
applies all three to **both** `#clearPlanModal` and `#clearLogModal`, so wraparound is
asserted at the boundary in both directions. **The closeout was not test-only:** it
needed a product fix, `static/js/modules/modal-focus-trap.js`, loaded globally from
`base.html`, because Bootstrap's `focusin`-driven trap cannot fire when focus falls
through to `document.body`. KI-006 is marked ✅ Resolved 2026-08-02 in
[`UI_SCENARIOS_GAP_ANALYSIS.md`](UI_SCENARIOS_GAP_ANALYSIS.md). **Do not re-open, and do
not "restore" the removed guard or fallback click — their absence is the point.**

**P1.7 is RETIRED (recorded 2026-08-13; shipped 2026-08-02).** It landed as **#285**
(squash `4a24773`) and is recorded in §2. Re-verified at `af14036`: `.gitignore` carries
`*.db-shm` at `:30` and `*.db-wal` at `:31`; `data/auto_backup/*.db-shm` and `*.db-wal`
do not exist; `docs/requirements_dry_run/` does not exist; and
`git status --porcelain --untracked-files=all data/ docs/` is empty, which is the actual
property the row wanted — no unignored sidecar is one `git add -A` from being committed.

**P2.3 is RETIRED as an execution item (recorded 2026-08-13).** Both platforms' baseline
debt was discharged by the #281 → #294 → #298 → #309 sequence and is recorded in §2; the
row below carries the annotation. **The residual is not this file's work:** the two WP4.0
rendering observations stay **open and owner-deferred** in
[`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) § *Known Windows visual reds*, which owns them.
Retiring the baseline item retires **no** safety rule — never blind-rebaseline, never
raise the global tolerance, never gate on an exact pixel count for a banded red, and run
the compare **before** regenerating anything.

**P2.5 is RETIRED (recorded 2026-08-13; shipped 2026-08-02).** FontAwesome is no longer
CDN-only: it ships as a tracked local asset through the visual-determinism arc, **#286**
(merge `9683f77`, including `160b1a8` *"test(package): require vendored Font Awesome
fonts"*). Re-verified at `af14036`: [`base.html:16`](../templates/base.html) loads
`static/vendor/fontawesome/css/all.min.css`, and `static/vendor/fontawesome/` is tracked
with its three `webfonts/*.woff2` files and `LICENSE.txt`. The row's consequence — a
visual gate comparing one broken-icon render against another — no longer holds, and both
platforms' baselines were regenerated after the change (162 tracked PNGs, 81 per
platform).

> **⚠️ The eight dated P1.2 blocks that follow are HISTORICAL and are closed by the
> "Final execution, 2026-08-12 — P1.2 RETIRED" block at the end of the run.** They are
> kept verbatim because they carry the method — the seven-check removal gate, the
> set-based (never count-based) registry invariant, the separator-terminated containment
> anchor, the reversible rename probe that measured "blocked by live processes" **false**,
> and the guard's `ask`/`deny` tiers. **None of their status words is current.** Every
> `READY`, `PARTIAL`, "still open", "artifact half", "attempt 14 failed" and "needs an
> owner call on which directories are meant" below was true on its own date and is
> **not** true now: the owner named all six `visual_review*` paths, all six were deleted,
> and [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9.5 records the terminal
> disposition. **Do not re-derive, re-certify, or re-attempt any of it.** The one thing
> that survives is a boundary, not a task: the authorization was **path-specific** and
> conferred nothing over `wp4_4` or `environment-backups`, which remain held.

**P1.2 is reclassified WAIT → READY (2026-08-03), and now has an execution goal:
[`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md).** Both v23 gate conditions
are discharged. P1.0 shipped as **#278**, which un-holds `D:/development/HT-v23-audit`;
and the v23 open-PR hold list (#245, #250, #274, #275) is entirely stale — all four
are closed or merged, leaving **#286** and **#281** as the only live holds. The
dirty/open-PR rule stays in force as procedure, but it is a per-path test, not a
blocker on the item. The plan carries a 2026-08-03 disposition for all 42 registered
worktrees: 34 removable, 7 preserved, 1 current.

> **P1.2 execution update — 2026-08-08.** The worktree half is complete. Attempt 6
> re-derived a 50-worktree registry against `origin/main` `86c3e1c`, a fresh 305-PR index,
> and fresh remote refs; all 40 candidates passed the seven-check gate and were removed
> non-forced with 0 skips / 0 failures. The final registry contains 10 verified KEEP rows,
> no candidate registration, and an empty prune dry-run. No branch was deleted. Twenty old
> path shells contain only validated `.venv`/`node_modules` junctions into shared main and
> were deliberately left untouched. This supersedes the stale counts and execution wording
> in the P1.2 table row below. **P1.2 remains PARTIAL, not RETIRE:** generated-artifact
> cleanup and its owner-gated holds were not authorized or executed. Full disposition:
> [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9 and the gitignored local
> `artifacts/P1_2_WORKTREE_DISPOSITION_LEDGER.md`.
>
> **Re-verified 2026-08-10 against `origin/main` `8b5231a`** (the run above gated against
> `86c3e1c`, which was current that day). The removal held: none of the removed paths is
> registered again and the prune dry-run is still empty. **Do not read "10 KEEP rows" as a
> count to re-check** — the registry is 12 now, and grew by two *during* this
> verification. Other sessions add worktrees continuously, so the check is set-based, not
> count-based; the plan's §7 has been corrected to say so. One KEEP row was removed by
> another session with no content loss, and one had its hold expire. Both are recorded in
> [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9.1.
>
> **Attempts 12–13, 2026-08-10 — nothing removed, nothing deleted; both blockers now
> measured.** Pre-flight was re-run in full and all three Packet E targets still match their
> audited branch, HEAD and dirty state; the set invariant holds and the prune dry-run is
> empty. **Stop commissioning either packet as "get owner approval and run it" — the owner
> gate is discharged and is not what is blocking.** Packet E has failed 13 times for one
> reason: `git worktree remove` is decided `ask`, and a `bypassPermissions` session cannot
> render a prompt, so the guard fails closed. It needs a prompting-mode session or a manual
> run — not another authorization. Packet D's recorded reason ("needs a quiet machine") was
> **measured and found false**: a per-path reversible rename probe shows **all 20 candidate
> paths FREE** with 13 Playwright processes live, because a live process is not a process
> holding a path. Its real blocker is that the guard **hard-`deny`s** recursive force delete
> and `ask`s on recursive delete, and every §6 candidate is a directory tree — so Packet D
> cannot run unattended in *any* permission mode, and evading that file-by-file would be
> routing around the guard. Full evidence, plus two scope corrections (`visual_review*` is
> six dirs now, not three; `artifacts/e2e` and `artifacts/dev-server` are **not** approved
> candidates) in [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9.3.
>
> **Manual execution, 2026-08-11 — Packet E complete; Packet D complete except
> `visual_review*`.** The three owner-dispositioned worktrees were removed, including the
> accepted four-file discard in `bs538-spike`; all three branch refs survive and `b990412`
> remains reachable. The 15 literal artifact/build/log targets in the runbook are gone,
> reclaiming about **1.07 GB**; every protected and non-§6 path verified present. The six
> `visual_review*` directories remain because §6 names a wildcard, records a stale count of
> three, and names no directory — so **no individual one is identifiably authorized** — and
> the follow-up all-six deletion was hard-denied before execution. **The denial is not the
> boundary; the missing scope decision is.** P1.2 remains **PARTIAL** on it, and closing it
> is an owner call on which directories are meant, not a recount and not a re-read of the
> wildcard. This paragraph supersedes the stale "the artifact half has not" wording in the
> classification block above and the "Packet E remains" / "artifact half has not run" wording
> in the historical table row below; full output and retained-set detail are in
> [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9.3.
>
> **Owner authorization + certification, 2026-08-12 — scope settled, execution still
> blocked.** The owner named **exactly six** literal `visual_review*` paths for permanent
> deletion, so the authority gap recorded above is **closed** and §6's stale count of three
> no longer governs. The authorization is path-specific: it confers nothing over
> `wp4_4`, `environment-backups`, or the three non-§6 diagnostic sets. All six then passed a
> four-part pre-deletion certification — containment beneath `artifacts/` against a
> separator-terminated anchor, ordinary-directory/no-reparse, unreferenced by tracked
> evidence and by both open draft PRs (#325, #326), and **all six probe FREE**. **Attempt 14
> then failed on the guard**, not on the decision: `git`-adjacent recursive delete is `ask`,
> and `bypassPermissions` cannot render a prompt. It was not retried with `--force` (a hard
> `deny`) or file-by-file (routing around the guard). Nothing was deleted; 694 files /
> 217 MB remain. **P1.2 therefore stays PARTIAL** — definition-of-done item 5 needs the
> deletion to have run. Item 6 now *passes*: the shared checkout is back on `main` and clean.
> The certification does not need re-deriving; the exact command is in
> [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9.4.

> **Final execution, 2026-08-12 — P1.2 RETIRED.** The six literal paths authorized in §9.4
> were deleted after each was revalidated as a real non-reparse directory contained beneath
> `artifacts/`. A post-delete check found none of them remaining. `wp4_4`,
> `environment-backups`, `vbl_check`, `codex-pr309-review-7d03c7a`,
> `pr294-visual-diagnostics`, `e2e`, and `dev-server` were all verified present; the database
> remained 839,680 bytes with its existing timestamp. The local disposition ledger is now
> complete at `artifacts/P1_2_WORKTREE_DISPOSITION_LEDGER.md`; the durable closeout evidence
> is [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9.5. No branch was deleted.

## 1. Recommended execution order

### P1 — Small closeouts that remove real debt — **ALL RETIRED (2026-08-13)**

> **Every row in this table is closed.** P1.0 #278, P1.1 #295, P1.2 #327, P1.3 + P1.8
> #292, P1.4 #291, P1.5 #284, P1.6 by owner decision, P1.7 #285. The four rows still
> printed below (P1.2, P1.5, P1.6, P1.7) are retained as the record of what was found and
> how it was discharged — **nothing here is dispatchable.** The "Why it was open" column
> is a past-tense evidence snapshot in every row; read the row header and the Status
> column for current state.

| ID | Activity | Why it **was** open (historical evidence) | Completion action | Status |
|---|---|---|---|---:|
| P1.2 | **RETIRED 2026-08-12 — do not execute this row.** *Remove obsolete worktrees and generated artifacts* — *2026-08-03: WAIT → READY, goal written: [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md); 2026-08-08: → PARTIAL, worktree half executed and re-verified 2026-08-10; **2026-08-12: → RETIRED**, both halves complete, recorded in #327 (`ae37365`) and [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9.5* | **⚠️ SUPERSEDED — the whole cell below is the v23/2026-08-08 evidence snapshot, retained for method only. The artifact half has since run.** All 40 candidate worktrees were removed, the 15 literal artifact/build/log targets were deleted manually on 2026-08-11 (≈1.07 GB), and the six owner-named `visual_review*` directories were deleted on 2026-08-12 after a four-part certification. Nothing here is a live count, a live hold, or a live command. *Original text:* **Only the artifact half of this row is still open** — 40 of 40 candidate worktrees were removed, and the per-path disposition is [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9 with its 2026-08-10 reconciliation in §9.1. What remains is §6 (generated artifacts, owner-gated on `environment-backups` and the held `wp4_4`/#281/#286 paths) and §7's Packet E (the preserved worktrees). *The v23 evidence below is historical and was superseded by the execution; it is kept for continuity — do not re-derive from it.* **The registered-worktree count is unstable — 24 at v19, 25 at v20, 29 at v21, 30 at v22, and 35 at the v23 recheck.** Recount with `git worktree list --porcelain` at execution time. **v23 additions (N8):** three worktrees are dirty right now — the shared checkout, `…-bs538-spike` (4 files; the #274 source), and `…-wp4-4-f1-navbar` (2). New since v22: `…-bs538-rebuild`, `…-node24-ci` (#275), `…-tsdrift`, and the read-only audit worktree `D:/development/HT-v23-audit` created for this revision (detached at this commit — **exclude it, and remove it only after P1.0 has published the branch**). The shared checkout **switched branch during this audit** (`docs/testing-strategy-reconciliation` → `docs/p3-gate-signoff`), so any branch/path fact here is evidence, never an execution input. **Command executability:** `git worktree remove` is intercepted by [`guard-destructive-command.ps1:438-440`](../.claude/hooks/guard-destructive-command.ps1) with decision **`ask`** — an unattended agent run stalls instead of proceeding — and `git reset --hard` is **denied** at `:397`, so no recovery path may rely on it. Known holds otherwise unchanged: any worktree associated with an open PR (now #245, #250, #274, #275) is protected. A local worktree branch name may differ from the GitHub PR head, so branch-name lookup alone is not proof. Generated output remains approximately: `artifacts/` 1.7 GB (`wp4_4` 643 MB held, `playwright` 522 MB, `environment-backups` 460 MB, `vbl_check` 21 MB), `build/` 76 MB, `dist/` 92 MB, `logs/` 63 MB, `debug/` 1 MB. | **None — done.** The completion action below was carried out; [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9–§9.5 is the durable record and this cell is retained only for the procedure it describes. **The `wp4_4` (643 MB) and `environment-backups` (460 MB) holds were never authorized and were never touched — they remain held, and deleting either is a separate owner decision, not P1.2 residue.** *Original text:* **Execute [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md)** — it converts this cell into packets with a per-path disposition table and a 2026-08-03 recount (**42** worktrees, not 35). The procedure below is its §4 and remains authoritative. For **every** non-current worktree, record path/branch/HEAD and run `git status --short --untracked-files=all`; any output means **skip and preserve**. Query `gh pr list --state all --head <branch>`, but treat it only as one signal: also compare the worktree HEAD OID with PR commits and use Git patch-equivalence/diff checks because squash merges and alternate local branch names defeat ancestry/name tests. Remove only a clean worktree with no unique patch and no open-PR association, through `git worktree remove <exact-path>`, then `git worktree prune`; do not recursively delete a registered worktree and do not delete its branch unless separately proven disposable. Delete transient artifacts only after confirming no active investigation/process references them; retain the protected `wp4_4` bundle pending its explicit decision. | **RETIRED** |
| P1.5 | **RETIRED — SHIPPED as #284 (`4e9b7d0`), 2026-08-02.** *Close KI-006 with honest modal keyboard tests* | **⚠️ SUPERSEDED — the cell below describes the pre-#284 tests and no longer describes any file on `main`.** The fallback click, the `if (btnVisible)` guard and the single-Tab focus assertion are gone; strict Escape plus forward **and** backward wraparound are asserted on the Plan and Log modals, and the closeout required a product fix (`static/js/modules/modal-focus-trap.js`). See the P1.5 retirement note above and the §2 row. *Original text:* Confirmed. [`accessibility.spec.ts:103-115`](../e2e/accessibility.spec.ts#L103-L115) presses Escape, waits 500 ms, and then **clicks the close button if the modal is still open** — the test passes whether or not Escape works. The whole block is guarded by `if (btnVisible)`. The focus-trap assertion checks only that the *first* Tab stays inside, which cannot prove wraparound. **v23 escalation (N3): the hazard is no longer hypothetical.** Draft **#274** upgrades Bootstrap to 5.3.8 and lists among its validation "Chromium navigation/accessibility/UI sweep — **127 passed**" — a sweep that includes these very tests. A Bootstrap-5.3 modal regression in Escape handling or focus wraparound would pass that sweep silently. v22's wording ("before any Bootstrap *decision*, P1.6/#269") is both too weak and aimed at a PR that is now closed. | **None — done, and the implementation and its tests must not be altered.** The completion action below was carried out and is now the shipped contract. Two of its instructions were overtaken by events and must not be re-read as tasks: the "#274 merge prerequisite" is moot (#274 merged 2026-08-02, and the strengthened sweep is what `main` runs), and the P1.4 spec collision resolved itself (P1.4 shipped as #291). *Original text:* Add strict Escape and forward/backward wraparound assertions for the Plan and Log modals, without the fallback click and without the visibility guard. **Treat this as a merge prerequisite for #274, not a preference:** land P1.5, then re-run #274's accessibility/UI sweep against the strengthened tests before #274 leaves draft. Sequence against P1.4 (**N6** — both edit `e2e/ui-hardening.spec.ts`) and regenerate the test inventory last (**N5**). Fix production behavior only if the new tests expose a failure; otherwise this is a test-only closeout and KI-006 can be marked resolved in [`UI_SCENARIOS_GAP_ANALYSIS.md`](UI_SCENARIOS_GAP_ANALYSIS.md). *(As executed it was **not** test-only — the new tests exposed a real containment failure on `/workout_log` and the product fix landed with them.)* | **RETIRED** |
| P1.6 | **CLOSED 2026-08-03 — disposition in [`P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md`](P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md).** All four v23 lanes discharged (#283 superseded #245; #274, #275, #250 merged 2026-08-02), and the two dependency PRs that opened afterwards were closed by owner decision: **#288** (`@playwright/test` 1.62.1) deferred — the bump moves Chromium 148 → 151 and would silently stale every visual baseline, since the visual specs run only in `deep-gate.yml`'s manual `visual-linux` job; **#287** (`stylelint` 16.26.1) refused — the pin is the CSS measurement instrument. Both are now `dependabot.yml` ignore rules, with the Playwright unblock condition (#281 merged **and** #286 resolved, then bump both ecosystems and regenerate both platforms' baselines in one arc) recorded on the rule itself. *Historical v23 record follows.* **Triage the dependency queue — v23: the queue drained and the Bootstrap lane was decided** | **Recount with `gh pr list --state open` at execution time.** Since v22, #240/#243/#244/#246 (Actions v7), #249 (`@types/node` 26), #251 (**TypeScript 7**) and #261 (`sass`) all **merged**, and **#269 was CLOSED, not merged** (**N2**). Only two dependency PRs remain: **#245** (`playwright` 1.61, all checks green) and **#250** (`jsdom` 30, red on JS Unit). Two owner drafts now carry the hard work: **#274** — the deliberate Bootstrap 5.3.8 migration that replaces #269 (SCSS import graph, rebuilt bundle, CDN pin, version contract), and **#275** — Node 20 → Node 24 across 13 `setup-node` pins plus a version contract. **N4:** #250's red is fully explained — jsdom 30 requires Node `^22.22.2 \|\| ^24.15.0 \|\| >=26`, so #275 is its prerequisite and #275 deliberately excludes it. **#252/#268 policy note stands:** the stylelint-major ignore remains the precedent, but it is no longer the open question for bootstrap. | Four lanes: **(a)** merge **#245** now — it is green and independent; **(b)** land **#275**, then rebase and re-validate **#250** against Node 24 — do not investigate #250 on its own; **(c)** **#274 is blocked twice over** — by P2.3's stale Linux baselines (its own stated blocker) *and*, per **N3**, by P1.5: it must not leave draft until the modal tests can actually fail; **(d)** the Actions-v7/TypeScript-7 majors are discharged — verify `Type Check (tsc blocking …)` stayed green on `main` after #251 rather than assuming it. Keep the `npm audit` severity/exception-policy decision separate. | **DONE 2026-08-03.** `npm audit` policy remains the one open, separate decision. |
| P1.7 | **RETIRED — SHIPPED as #285 (`4a24773`), 2026-08-02.** *Close two repository-hygiene gaps* | **⚠️ SUPERSEDED — neither gap exists on `main`.** `.gitignore` now carries `*.db-shm` (`:30`) and `*.db-wal` (`:31`); both orphan sidecars and `docs/requirements_dry_run/` are absent; `git status --porcelain --untracked-files=all data/ docs/` is empty. *Original text:* Still present at this audit. (a) `.gitignore:29`'s `*.db` does not match SQLite sidecars, so `data/auto_backup/database_20260712_000549.db-shm` and `.db-wal` sit **untracked and unignored** — one `git add -A` from being committed. Their presence beside a July-12 snapshot also means a backup DB was opened read-write and not clean-closed. (b) `docs/requirements_dry_run/` is an empty leftover directory. | **None — done.** *Original text:* Add `*.db-shm` / `*.db-wal` to `.gitignore`, delete the two orphaned sidecars after confirming no process holds them, and remove the empty directory. No production change. | **RETIRED** |

### P2 — Product/workflow activities that can be explicitly closed or advanced

| ID | Activity | Real state / gate | Completion action | Effort |
|---|---|---|---|---:|
| P2.1 | **RETIRED 2026-08-13 — the owner decision was taken: close the inactive window, no threshold change.** *Fatigue Phase 2 Stage 4 disposition* | **⚠️ SUPERSEDED — the owner decision this row was waiting for has been taken.** On **2026-08-13** the owner chose **option (b)**: close the inactive *Phase 2* Stage 4 window as *no real-use evidence, no threshold change*, keep Learned Calibration **2D-D** parked, and retire only what passes the retention tests. **Every premise the row asserted was re-verified read-only that day and all of it held** — evidence table in [`PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md) §5 Stage 4. One wording correction: *every* user table is not empty — `user_selection` holds **1** row; the rest are 0. The disambiguation the row leads with is correct and still worth keeping: *Phase 1* Stage 4 closed 2026-05-20, *Phase 2* Stage 4 closed 2026-08-13, and they are different closes on different evidence. *Original text:* **Disambiguation first (v21):** two "Stage 4"s exist. *Phase 1* Stage 4 was parked 2026-05-13 and **closed 2026-05-20** — [`STAGE4_PARKED_HANDOFF.md`](fatigue_meter/STAGE4_PARKED_HANDOFF.md) carries a proper SUPERSEDED banner. The open item is ***Phase 2*** Stage 4 ([`PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md), window opened 2026-05-24). That window is inactive: every user table in `data/database.db` is empty (`workout_log=0`), the last observer log is 2026-05-30, no scheduled task is installed. Learned Calibration 2D-D depends on the same missing evidence. | **None — done, and nothing was deleted.** Shipped as a docs-only closeout: [`PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md) §5 Stage 4 now carries the close, the re-verified evidence table, and a three-part reopen bar (fresh written owner decision **plus** a representative multi-week `workout_log` **plus** ≥2 same-direction real-use disagreements); §10 marks the observer automation dormant and retires the standing run instructions; [`LEARNED_CALIBRATION_PLAN.md`](user_profile/LEARNED_CALIBRATION_PLAN.md) §2D-D records the re-verification and keeps 2D-D not-started, reopen-only on fresh owner approval **plus** new evidence. **⚠️ The v23 safety check below is half wrong and must not be reused as written.** Its *pin* half is right — no test or workflow reads either artifact. Its *regenerable* half was **measured and disproven**, so **nothing was deleted**: both artifact families are kept, as are the observer scripts and their 26 tests (measurement and reasoning in [`PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md) §10). The closing prohibition survives the retirement and still binds: **never tune thresholds or make 2D-D prescriptive without the documented evidence bar and fresh approval.** *Original text:* **OWNER:** (a) restart real-use collection and keep Stage 4 open, or (b) close the inactive window as "no evidence / no threshold change," park 2D-D, and retire the no-longer-used observer tooling instructions **plus the generated artifacts committed under `docs/fatigue_meter/`** (`baseline-2026-04-30*.txt`, `generated-calibration-report.md`) per retention policy. **v23 safety check on that cleanup:** `generated-calibration-report.md` is `DEFAULT_OUTPUT` of [`scripts/fatigue_calibration_report.py:32-36`](../scripts/fatigue_calibration_report.py) and is rewritten by `output.write_text(...)` at `:546` — it is regenerable script output, so deleting it loses no evidence. But `tests/test_fatigue_stage4_observer.py` and `tests/test_calibration_integration.py` both reference `docs/` paths, so confirm neither pins the files being retired before removing them (**N7**). Never tune thresholds or make 2D-D prescriptive without the documented evidence bar and fresh approval. | **RETIRED** |
| P2.2 | **RETIRED — Fatigue body heatmap shipped as #339 (`ea82ef1`), 2026-08-13.** | All six owner decisions were resolved and implemented: both delt regions map to Middle-Shoulder; existing planned/logged + period state drives four discrete fatigue bands; the separate panel is collapsible; unranked muscles stay visible and neutral; the head remains flat gray. No fatigue formula, threshold, schema or API changed. | None. **[UPDATED 2026-08-14]** Linux baseline follow-up **#351 has since merged** (`5a03d47`), regenerating all twelve fatigue captures and removing a duplicated body-map caveat from the template. It was a separate visual-corpus packet throughout, never unfinished heatmap behavior. | **RETIRED** |
| P2.3 | **RETIRED as an execution item 2026-08-13 — the baseline debt is discharged on both platforms.** *Visual-baseline debt: the Windows pair plus stale Linux baselines* | **⚠️ SUPERSEDED — the owner action this row asks for has been run, twice over.** **Linux:** #281 (`864043f`) accepted the deterministic set, #294 (`73c5c46`) the six progression captures stale from #291, and #298 (`f8988f9`) took five plan-desktop captures off the byte gate; the Linux ledger in [`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) is annotated **CLOSED 2026-08-04** with three consecutive green `visual-linux` compares. **Windows:** #309 (`10ba89f`) regenerated the win32 corpus after owner by-eye review; a seeded win32 run passes **66 + 18**. 162 baselines are tracked, 81 per platform. **The D3 blocker in the cell below is also discharged** — the weekly deep gate merged as #323 (`3b1160b`) with #325 (`4d01698`) adding job timeouts. **What is NOT retired:** the two WP4.0 rendering observations (animated navbar logo; `plan-desktop-light-advanced`) stay **open and owner-deferred**, but they are `BYTE_GATE_EXEMPT` with no PNG on either platform, so they are **not baseline debt** and are **not owned by this file** — [`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) § *Known Windows visual reds* owns them. *Original text:* Two real Windows-only failures remain: the animated navbar logo in Workout Plan desktop dark, and `plan-desktop-light-advanced` in `visual-baseline-thumbnails.spec.ts` (**6,084 px** measured / 6,098 retry vs **6,262 px** baseline — [`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) Windows ledger). New on `origin/main` via #273: the **Linux** baselines were last written before 57 later CSS/template commits and now produce at least 11 failures (57 pass, 16 do not run); this is separate from the Windows pair and blocks the signed D3 weekly deep-gate stopgap. [`QUALITY_GATE.md`](ai_workflow/QUALITY_GATE.md) does not yet describe the full platform-specific state. | **None — done. But every safety rule below survives the retirement and still binds any future baseline work:** **never blind-rebaseline**, never raise the global tolerance, never gate on an exact pixel count for a banded red, run the **compare before regenerating anything**, and treat an owner by-eye review as mandatory for each regeneration — it attests to the pixels reviewed, not to future diffs. Also still true: no CI path generates win32 baselines, so a win32 corpus can stale silently and must be re-measured rather than assumed. *Original text:* **OWNER action first:** run the Linux generate workflow, download and inspect all 84 PNGs by eye, commit only approved baselines, then confirm Linux compare is green before adding D3's weekly schedule. Separately stabilize the Windows animation/snapshot timing and diagnose the advanced-thumbnail delta; never blind-rebaseline or raise the global tolerance. **v23: the Bootstrap coordination target is now #274, not the closed #269** — and the dependency runs the other way: #274 names this stale-baseline debt as its *own* blocker, so the Linux regeneration is a prerequisite for the Bootstrap migration, not merely something to coordinate with it. *(That ordering was honoured and is spent: #274 merged 2026-08-02 and the baselines were brought current afterwards.)* | **RETIRED** |
| P2.4 | **Broader KI-005 manual-edit provenance staleness** | KI-005 itself is shipped and Gate-2 approved. Only the explicitly accepted limitation remains: arbitrary manual edits can leave estimate provenance/ancillary text stale. | Treat as a new UX packet only if this is visible or confusing in real use. Do not reopen the completed KI-005 implementation plan for cosmetic comment work. | OWNER / demand-gated |
| P2.5 | **RETIRED — SHIPPED through the visual-determinism arc, #286 (merge `9683f77`), 2026-08-02.** *The CI visual gate certifies a broken-icon state — FontAwesome is CDN-only with no fallback* *(finding raised 2026-08-02)* | **⚠️ SUPERSEDED — FontAwesome is no longer CDN-only.** [`base.html:16`](../templates/base.html) now loads `static/vendor/fontawesome/css/all.min.css`, and `static/vendor/fontawesome/` is tracked (three `webfonts/*.woff2` plus `LICENSE.txt`), pinned by `160b1a8` *"test(package): require vendored Font Awesome fonts"*. Icons therefore resolve offline and on a CI runner, so the "gate that cannot fail" consequence no longer holds, and both platforms' baselines were regenerated after the change. *Original text:* [`base.html:16`](../templates/base.html) loads FontAwesome from `cdnjs.cloudflare.com` with **no local fallback** — unlike the Bootstrap stylesheet at `:15`, which falls back to jsdelivr. It does not resolve on the CI runner, so **every icon renders as a magenta placeholder square** in the committed Linux baselines. Confirmed identical in the pre- and post-regeneration sets during the #281 review, so it is **long-standing and did not block that recovery**. The consequence is what matters: the visual gate compares one broken-icon render against another, so **no icon regression can ever fail it**, and any future change that genuinely breaks icons passes silently. This is the same "a gate that cannot fail" class as the `occurrences <= 1` assertion and `measure.verify_blind_spots()`. | **None — done; the first option was taken.** *Original text:* Ship FontAwesome as a **deterministic local asset**, or give it the same `onerror` fallback the Bootstrap link already has, then regenerate both platforms' baselines once so they encode a real icon render. **Do not fix this inside a baseline-recovery packet** — it is a rendering change and needs its own before/after. *(Honoured: it shipped in the determinism arc with its own before/after, not folded into #281's recovery.)* | **RETIRED** |
| P2.6 | **`j_known_live_mutation.mjs` pins a raw-byte digest that cannot match on Linux** — **SHIPPED 2026-08-04** *(new 2026-08-02)* | **Closed by the LF-normalization packet.** The tool now hashes the **LF-normalized text** — UTF-8 with every `CRLF` collapsed to `LF` — and pins `3ab06083c89eae0b5dd46d820dde4d2da1d59de1ffa6d825585aaca0ad17e14a`, which is the committed blob's own digest, so a Windows and a Linux checkout of the same commit both satisfy the gate without `--expect-sha`. Only content is pinned: the mutated file is written back with the line endings it arrived with, byte-for-byte identical to what the previous script produced here. `tests/test_css_audit_digest_normalization_contracts.py` pins the property from both ends (the constant is the canonical digest of the tracked file; both checkout forms are accepted and report identical digests; a genuinely edited stylesheet is still refused), and the pytest CI job now sets up Node so those cannot silently skip. `theme-dark.css` is untouched and **P3 stays terminated**. The durable rule went to [`verification.md`](../.claude/rules/verification.md) § Windows scripting hazards. **Original finding, retained:** [`scripts/css_audit/j_known_live_mutation.mjs`](../scripts/css_audit/j_known_live_mutation.mjs) read `theme-dark.css` with `readFileSync` (an untranslated Buffer) and hashed the raw bytes, so its pinned `EXPECTED_INPUT = e54818bf…` was the **CRLF** digest. The repo is `core.autocrlf=true` with **no `.gitattributes`**, so the committed blob is LF and hashes to `3ab06083…` — exactly **574 bytes** smaller, one `CR` per line. The control therefore **ran on Windows and refused to run on Linux**, where it would have demanded the very `--expect-sha` override its own docstring forbids using to silence it. Surfaced by P3-a0, which corrected its own evidence claim; **a0 hit the identical hazard in its contract file and CI caught it** (PR #280). Recorded as debt rather than fixed: it sat outside a0's owned paths and **P3 is terminated — this must not reopen it**. | **Done.** Of the two options this row offered, the first was taken: normalize before hashing. The `.gitattributes` alternative was rejected — it would have re-pinned this one constant by changing how *every* file in the repository is checked out, to fix a defect that lives in one script. **The standing obligation survives the closure: any future packet that re-pins that digest must still state which line-ending form it pinned**, and the contract test now reds if the constant stops being the canonical digest of the tracked file. | 1–2 h *(actual: ~1 h)* |
| P2.7 | **RETIRED 2026-08-14 — SHIPPED as #357 (`e84d19c`), the same day it was recorded.** *`test_consult_adapter.py` hard-codes a checkout directory name, so it fails in the canonical main checkout and passes everywhere else* *(new 2026-08-14)* | **⚠️ SUPERSEDED — the defect is not present on `main`.** [`tests/test_consult_adapter.py:585-592`](../tests/test_consult_adapter.py) now builds the denied path as `f"../{REPO.name}-not-a-real-sibling/CLAUDE.md"`, which resolves outside the repository root in **every** checkout, worktree and CI runner, so the node no longer depends on what the directory is called. The recommended fix was taken exactly as written — the first of the two options — and `check_artifact_paths()` was **not** relaxed. The finding's durable lesson survives the retirement: *a literal directory name is only "outside the repo" until someone clones into a directory with that name*, and the comment left at the fix site says so. *Original text:* **The production code is correct; the test is wrong.** `tests/test_consult_adapter.py:583` lists `"../Hypertrophy-Toolbox-v3-main/CLAUDE.md"` among the denied artifact paths, intending *"a path that escapes the repo root"*. Whether that holds depends on what the checkout is **named**. In any worktree (`…-main-scssdrift`, …) and on the CI runner (`Hypertrophy-Toolbox-v3`) the path resolves to a different, non-existent sibling → outside the root → correctly refused → **passes**. In the checkout actually named `Hypertrophy-Toolbox-v3-main`, `..` and back in resolves to **the repo root itself**, so `check_artifact_paths()` correctly *accepts* it and the assertion fails. Reproduced on `main` @ `7e4c1e9`: `1 failed, 10 passed` for that node; the full suite at `538919a` read **1 failed / 2810 passed**. **No gate can see this** — CI is green on the same commit and will stay green, and every worktree is green. It is the exact inverse of **DR-33** (*"Linux CI caught a hole that no local run could"*): here a local run caught a hole no CI run can. | Derive the escape path from the checkout instead of hard-coding it — e.g. `f"../{REPO.name}-not-a-real-sibling/CLAUDE.md"`, or build it under `tmp_path`. **Verify in the main checkout, not a worktree** — a worktree run cannot reproduce the failure and will report a false pass. Do not "fix" it by relaxing `check_artifact_paths()`; the production behaviour under test is correct. | **RETIRED** |

### P3 — Valid proposals, not forgotten near-complete work

These items remain legitimate but should not displace the remaining owner
decisions (P2.4 and the §4 TODOs). **Every non-retired bullet below is still a
PROPOSAL — v26 promoted none of them, and P1 being empty is not an argument for
starting one.**

- **Testing Strategy remaining packets and decisions** in
  [`TESTING_STRATEGY_PLANNING.md`](TESTING_STRATEGY_PLANNING.md). Phases 0–1 are
  complete. Phase-2 Packet A shipped as #342 (`1438a14`), repairing nine
  false-green accessibility assertions. **[UPDATED 2026-08-14 — this bullet
  previously read "Packets C (strict console) and D (axe) remain queued".]**
  **Packet C shipped as #362** (`52331bf`): `e2e/console-guard.ts` plus three
  migrated specs. **Only Packet D (axe) remains queued**, with no open PR at
  this reconciliation. D3's weekly compare-only stopgap shipped
  as #323 (`3b1160b`) with #325 (`4d01698`) adding timeouts, but its first
  scheduled run is still due 2026-08-17. D4, D7 and the `js-unit` half of
  D2 remain unsigned (D6 signed 2026-08-14, ADR-007); Phases 3/5 and the release/tag half of Phase 4 remain
  proposals.
- ~~**Product documentation suite** in [`PRODUCT_DOCS_PLAN.md`](PRODUCT_DOCS_PLAN.md)~~
  — **EXECUTED.** Gate 0 answered, council run, Plan v2 recorded in §8; the
  owner-selected subset shipped as [`docs/product/**`](product/README.md).
  PRD and TECH_DESIGN were deliberately not built (§8.5). Not a leftover.
- **Cross-model orchestration beyond the shipped consult** in
  [`ai_workflow/CROSS_MODEL_ORCHESTRATION_PLAN.md`](ai_workflow/CROSS_MODEL_ORCHESTRATION_PLAN.md).
  The bounded, read-only one-shot consult shipped as #344 (`9906105`), and Gate
  2 was ratified post-merge by #348 (`a459520`). **[UPDATED 2026-08-14]** That
  plan's own **Packet C** (charter and contract hygiene) shipped as **#361**
  (`a224b39`) — a different packet series from Testing Phase-2's C/D above, and
  the two must not be conflated. Its **Packet D** (narrowing
  `.claude/settings.json` so the adapter prompts, CR-18) is **declined at plan
  level, not queued**: the recorded disposition is *"accept the disclosure,
  decline the mitigation"*, because narrowing that allowance would prompt on
  every Python invocation in the repository while still not stopping an agent
  that can set the variable itself. What bounds the risk instead is the read
  denylist plus `--max-budget-usd`. Pursuing it anyway would need its own
  Gate 0. The heavy `$orchestrate`
  manager/state-machine remains planned and deliberately unimplemented; the
  plan is tracked and indexed, so v21's untracked-file warning is retired.
- **Theme-dark P3** in [`css_theme_dark_p3/PLANNING.md`](css_theme_dark_p3/PLANNING.md):
  both gates were signed, `P3-a0` shipped as #280 (`cd93480`), and the owner
  terminated the arc at a0. No later P3 packet is authorized; this remains a
  large CSS change, not a cleanup leftover.
- **App-JS TypeScript checking:** `tsconfig.json` still covers E2E/config only.
  Expanding it across ~14.6k lines of untyped app JavaScript is a large
  migration, not the cheap A12 task the old plan implied.
- **User Profile v2:** per-exercise overrides, auto-updated lifts, bodyweight
  add-ons, confidence display, and future related-exercise transfer ratios.
  The current DB has no profile/lift/log evidence; the shipped 2A infrastructure
  (`exercise_transfer_ratios` schema, [`RELATED_EXERCISE_TRANSFER_DESIGN.md`](user_profile/RELATED_EXERCISE_TRANSFER_DESIGN.md))
  is in place but unpopulated. Product ideas, not nearly finished activities.
- **Fatigue Phase 3:** owner-supplied landmarks for six unranked muscles,
  systemic/joint fatigue, decay, `%1RM`, technique modifiers, custom thresholds,
  partial-week display, and API work. Do not invent domain thresholds.
- **Remaining CSS/refactor tail:** the 235 `@layer workout` pins, Workout
  Plan/Log redesign-sized cleanup, superset dark tint, theme-dark unlinking,
  10 animation-dependent declarations, `.tbl-show-*`/`.tbl-hide-*` as a unit,
  dormant `.scale-btn[data-scale]`, and 155 uncertified navbar nominations.
  Explicitly deferred/owner-gated, not forgotten quick wins.
- **Inert `d-flex` / `d-inline-block` consumers.** *(Corrected 2026-08-13: the
  bullet was written inside #303 while it was still a draft and said "**draft PR
  #303**, unmerged". **#303 merged 2026-08-08 as `42e8a4d`**, with its Linux
  baselines following in #308 (`99e172d`). That changes only the provenance
  sentence — **this bullet remains a PROPOSAL and nothing in it is authorized.**)*
  OD-2 (implemented and owner-accepted, shipped in **PR #303**, `42e8a4d`)
  restored Bootstrap's `display`
  utility but deliberately narrowed it to `values: none inline` — enough for
  `d-none` and its indivisible `d-lg-inline` partner, and no further. `d-flex`
  (15 call sites) and `d-inline-block` (1, `templates/fatigue.html:22`) are
  therefore **still inert by design**, recorded in `KNOWN_INERT` and pinned by
  `tests/test_css_display_utilities_contracts.py::test_the_deliberately_withheld_utilities_stay_withheld`,
  so the narrowing cannot widen without updating the contract. Activating them is
  a one-line SCSS change but **a rendering change, not a bug fix** — and #303
  merging does **not** pre-authorize it; #303 shipped the narrowing, not its
  widening. Measured
  against a same-machine baseline it moves **12 further visual captures** —
  session-summary ×6 and weekly-summary ×6 at 120k–564k pixels each, because
  those pages build `d-flex` rows in JS — plus the `/fatigue` period select from
  `block` to `inline-block`. Needs its own packet with **dedicated
  visual-baseline review and regeneration**; do not fold it into an unrelated
  change. Measurement:
  [`dnone_display_utilities/EVIDENCE.md`](dnone_display_utilities/EVIDENCE.md) §3, §7.
- ~~**Nothing ties the committed `bootstrap.custom.min.css` to its SCSS
  source.**~~ **RETIRED by #335 (`542df07`).** The required frontend-build job
  now deletes both generated artifacts, runs the real compiler once, and fails
  on a diff across exactly the bundle **and its `.map`**. The map makes the gate
  stronger than the original proposal: a compiler that silently stops emitting
  it cannot pass. #339 was the first real SCSS/compiled-artifact traffic and
  passed the gate with both regenerated outputs committed.
- **Six E2E specs hard-code `http://127.0.0.1:5000`, so none is port-portable.**
  `api-integration`, `exercise-interactions`, `progression`,
  `replace-exercise-errors`, `summary-pages` and `workout-plan` build absolute
  request URLs against port 5000 instead of a `baseURL`-relative path — 12
  references. Any run on another port fails them with `ECONNREFUSED` no matter
  what the product does, which is exactly what happens to a packet that uses an
  isolated port to avoid certifying against a concurrent worktree's checkout
  (`playwright.config.ts` hard-codes 5000). CI never notices, because it runs the
  default config on 5000 — so this is invisible to every gate and only bites
  local parallel work. Found while verifying PR #303, whose five "local
  failures" were entirely this. Low risk to fix — replace the absolute URLs with
  relative paths so Playwright resolves them against `baseURL` — but it touches
  six spec files, so it wants its own packet rather than a drive-by.
- **Grounding-scan doc set** (`docs/scan/PHASE_02…22`, `SCAN_FINDINGS.md`,
  `SCAN_PROGRESS.md`, `SCAN_RECOMMENDATIONS.md`) and the ~56 `CSS_PHASE4_*`
  evidence files at the `docs/` root: both arcs complete and merged; the scan
  tracker still points at a deleted worktree (`D:/development/HT-scan`). Archive
  candidates under [`DOC_RETENTION.md`](ai_workflow/DOC_RETENTION.md), but the
  6-month criterion is unmet. **v23 (N7): the CSS blocker is harder than a doc
  link.** Six of these artifacts are asserted by pytest in
  `tests/test_css_wp4_4_*.py` — `_D1_A11Y_`, `_D2_A11Y_`, `_E_LAYOUT_`,
  `_H_COMPONENTS_DEAD_`, plus `CSS_PHASE4_WP4_4_A_BASELINE.json` and
  `CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json` — so moving one reds the **required**
  `Run Tests` context, not merely a documentation link. The seven orphan
  `WP4_3I_*` files carry no test or CI reference and are the only genuinely
  movable subset. Revisit, do not act now.

## 2. Findings that are already done, superseded, or no longer relevant

Do not resurrect these from unchecked boxes or old dated prose.

| Prior activity / stale claim | Current disposition |
|---|---|
| **P1.0 publish the v18→v23 audit arc** | **SHIPPED** as **#278** (`c0dff15`, merged 2026-08-02). `origin/main` serves this document; N1's "not reachable by anyone else" and "`origin` still publishes the June punch list" are historical and annotated in place. |
| **P1.1 documentation truth and compaction pass** | **SHIPPED** as **#295** (squash `4d5d8cc`, merged 2026-08-04), docs-only across 13 documents. Corrected: the discharged stale-rows block in `DUPLICATION_REGISTRY.md` with rows 3/11/14 re-derived and WP2.6 recorded shipped; four missing workstreams added to `INDEX.md`; the expired Fatigue Stage-4 window in three files; KI-003 and KI-007; `QUALITY_GATE.md` now **links** the visual-red producers instead of restating a count and records branch protection at **11** contexts; the WPB.4 gate claim in `REFACTOR_PLAN.md` marked historical in place; an August section in `CHANGELOG.md`; hand counts removed from `E2E_TESTING.md` and `TESTING_STRATEGY_PLANNING.md`; orphan dispositions written into `DOC_RETENTION.md`. **Two premises in the v23 row were wrong and are corrected in the goal doc, not here:** the orphan inbound counts conflated the `WP4_3I_*` and `WP4_4_*` families, and the `WP4_4_*` **`.md`** files are *not* pytest-pinned — the **JSON** siblings are (see **N7**, which repeats that imprecision). Goal doc: [`doc_truth/PLANNING.md`](doc_truth/PLANNING.md). |
| **P1.3 + P1.8 agent-workflow integrity** | **SHIPPED** together as **#292** (squash `db1bc5d`, merged 2026-08-04). P1.3 added `/handover` to `senior-developer`'s skill allowlist and contract-tested the real PowerShell guard. P1.8 removed eleven active dependencies on the retired `.claude/SHARED_PLAN.md` tier/appendix system, routed each rule to its real authority, and added anti-recreation contracts. The apparent reviewer-step mismatch is resolved by the documented role split: the manager or primary session runs the independent reviewers; the implementing agent retains `disallowedTools: Agent`. Goal doc: [`agent_workflow_integrity/PLANNING.md`](agent_workflow_integrity/PLANNING.md). |
| **P1.4 small UI/debug scaffolding** | **SHIPPED.** All six items deleted in one packet: the visible `Available exercises` counter (and the now-dead `.debug-info` branch in `progression.spec.ts`), the **17** `console.log` calls in `progression-plan.js`, both inert `*_DEBUG` wrappers with all **18** no-op call sites (the v23 row said 21 — recounted at `828fb07`), the zero-caller `handleApiResponse()`, and the false "expected to be RED" KI-005 header. The six **win32** `progression-*` visual baselines were intentionally regenerated and reviewed in the same PR. The six **linux** ones are **not** regenerated here: #281 merged first (`864043f`) with a set already current against #290, so this packet knowingly stales those six by its own 19px counter-line delta (mobile 2132px → 2113px) and leaves the runner-generated replacement to a future owner-reviewed regeneration. Deep-gate only — `visual.spec.ts` is excluded from required CI and `visual-linux` is manual. Goal doc: [`p1_4_debug_scaffolding/PLANNING.md`](p1_4_debug_scaffolding/PLANNING.md). |
| **P1.5 close KI-006 with honest modal keyboard tests** | **SHIPPED** as **#284** (squash `4e9b7d0`, merged 2026-08-02). Not test-only as scoped: the strict tests exposed a real containment failure and the packet added the product fix `static/js/modules/modal-focus-trap.js`, loaded globally from `base.html`, because Bootstrap's `focusin`-driven trap cannot fire when focus falls through to `document.body`. `e2e/ui-hardening.spec.ts` now asserts forward wraparound (last→first), backward wraparound (first→last via Shift+Tab) and Escape-only close on **both** `#clearPlanModal` and `#clearLogModal`; `e2e/accessibility.spec.ts`'s Escape test waits on `hidden.bs.modal` with no fallback click and no `if (btnVisible)` guard, then asserts backdrop + `body.modal-open` cleanup. KI-006 is ✅ Resolved in [`UI_SCENARIOS_GAP_ANALYSIS.md`](UI_SCENARIOS_GAP_ANALYSIS.md). **Do not restore the removed guard or fallback click.** |
| **P1.7 two repository-hygiene gaps** | **SHIPPED** as **#285** (squash `4a24773`, merged 2026-08-02) — a two-line `.gitignore` change plus the deletions. Re-verified at `af14036`: `*.db-shm` at `.gitignore:30`, `*.db-wal` at `:31`, no `data/auto_backup/*.db-shm`/`*.db-wal`, no `docs/requirements_dry_run/`, and `git status --porcelain --untracked-files=all data/ docs/` empty. |
| **P2.3 visual-baseline debt (Windows pair + stale Linux baselines)** | **DISCHARGED as an execution item** by #281 (`864043f`) → #294 (`73c5c46`) → #298 (`f8988f9`) on Linux and #309 (`10ba89f`) on Windows; #308 (`99e172d`) later accepted the six Linux volume-splitter captures. The Linux ledger is annotated **CLOSED 2026-08-04**; a seeded win32 run passes 66 + 18; 162 baselines tracked, 81 per platform. **Residual, not this file's:** the two WP4.0 rendering observations remain open and owner-deferred in [`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) § *Known Windows visual reds* — both are `BYTE_GATE_EXEMPT` with no PNG on either platform, so no byte gate measures them and they are not baseline debt. **The safety rules outlive the item:** never blind-rebaseline, never raise the global tolerance, never gate on an exact pixel count for a banded red, and compare before regenerating. |
| **P2.5 FontAwesome is CDN-only, so the visual gate certifies a broken-icon render** | **SHIPPED** through the visual-determinism arc, **#286** (merge `9683f77`), including `160b1a8` *"test(package): require vendored Font Awesome fonts"*. [`base.html:16`](../templates/base.html) loads the tracked `static/vendor/fontawesome/css/all.min.css`; the vendor directory carries three `webfonts/*.woff2` and `LICENSE.txt`. Icons resolve on a CI runner, so the "gate that cannot fail" consequence is gone, and both platforms' baselines were regenerated afterwards. The row's own instruction was honoured — it shipped as its own rendering change with a before/after, not folded into #281's recovery. |
| **WPB.4 `Unassigned` weekly-summary bucket is gated/not started** | **SHIPPED** in PR #256 (`9fe5dbd`); Track B closed. The planning doc now carries a SHIPPED / DO-NOT-EXECUTE banner (#265). |
| **Old A12: add JavaScript unit tests** | **DONE.** Vitest, coverage reporting, nine test files, and a non-required CI job exist. Low coverage is a separate future decision. |
| **Old A12: audit known-red E2E** | **DONE.** Generated inventory plus the inherited-red ledgers replaced the manual count. The two explicit Windows visual reds are the only ledgered pair, and since #309 (`10ba89f`) regenerated the win32 corpus a seeded Windows run reds on **none** of the 66 + 18 — neither of the pair is byte-compared any more (both are `BYTE_GATE_EXEMPT` with no PNG, per #298). See `MASTER_HANDOVER.md` §"Known Windows visual reds". |
| **Agent Workflow v2 / Phase 5** | **COMPLETE and owner-signed.** Keep only P1.3's concrete guard contradiction; do not call the whole workflow unfinished. |
| **KI-005 Workout Controls persistence** | **COMPLETE, ported, verified, and Gate-2 reapproved.** Its planning artifact is completion history, not an active checklist. |
| **KI-003 Program Backup suite pollution** | **RESOLVED by CI isolation.** `E2E Backup (Chromium, isolated)` runs on a fresh server and throwaway DB and is a required context. Only the gap-analysis doc still says "Mitigated" (P1.1). |
| **KI-004 last-toast-wins** | Intentional/tested behavior; not an open defect. |
| **KI-007 isolated-muscle table empty** | **OBSOLETE/RESOLVED.** Both live and seed DBs contain **1,598** mappings across **1,897** exercises (re-queried). |
| **KI-008 multi-tab conflict detection** | **NO LONGER RELEVANT** under the single-user/single-tab product model. Keep as a non-goal, not backlog. |
| **User Profile issues 1–24 / phases A–H** | **SHIPPED.** Unchecked boxes inside historical issue bodies are stale narrative, not work. |
| **Learned Calibration 2A–2D-C** | **SHIPPED.** Only 2D-D remains, and it is **not started**. Its real-use evidence gate outlived P2.1: the upstream Stage 4 window closed 2026-08-13 without collecting any, so 2D-D reopens only on fresh owner approval **plus** new evidence. |
| **Fatigue *Phase 1* Stage 4** | **CLOSED 2026-05-20, owner-reviewed, no threshold changes.** [`STAGE4_PARKED_HANDOFF.md`](fatigue_meter/STAGE4_PARKED_HANDOFF.md) is properly superseded-bannered. Do not confuse with *Phase 2* Stage 4, which is a separate close on separate evidence — opened 2026-05-24, **closed 2026-08-13** as no-evidence / no-change (P2.1). |
| **Program Backup "restore an active volume plan and clear `is_active`"** | **IRRELEVANT.** Current Program Backup stores `user_selection`, not `volume_plans`; the archived R6 premise does not match the product. |
| **Program Backup non-atomic creation and export 500 ms delay** | **FIXED.** Backup creation uses one transaction; export cleanup retries only after an unlink failure. |
| **Grounding-scan bug list A1–A12 (SCAN_RECOMMENDATIONS §A)** | **ALL DISPOSITIONED — but the numbering does not match `REFACTOR_PLAN.md` Track A (A1–A8), which caused this file's own earlier rows to under-enumerate.** Mapping: scan-A1…A5, A8, A10, A11 → Track A fixes (toast severity, duplicate submission, badge drift, error page + fatigue error path, backup atomicity, listener cleanup, export delay); **scan-A6 → WPB.1** (#103, weight 0); **scan-A7 → WPB.2** (#107, server-side bounds); **scan-A12 → WPB.3** (#128, export no longer mutates `exercise_order`; the route is POST and delegates to `export_plan_to_workout_log()`); scan-A9 (tokens.css cascade order) → resolved in the Phase 4 CSS work and locked by `tests/test_css_cascade_contracts.py`. When citing "A-numbers," always name the source document. |
| **Refactor Track A, Track B, Phases -1 through 3, WP4.4 a–k** | **COMPLETE** after WPB.4. Remaining CSS work is the deferred P3 registry above. `REFACTOR_PLAN.md:425` still says otherwise inside a dated block — P1.1's marker job, not reopened work. |
| **app.py review P1–P5** | **COMPLETE**, including packaged-smoke permanence and #266's post-merge cache/payload/isolation hardening. |
| **`Test Inventory Drift` is a deferred, one-token flip** | **DONE / superseded.** PR #267 removed `continue-on-error`, returns `exit $STATUS`, renamed the job safely, and the live branch-protection list requires it as the 11th context. The two older required E2E names retain their historical `(non-required)` suffix by documented design. |
| **Post-merge `main` runs may be cancelled by PR activity** | **FIXED** in #264; post-merge runs for #264–#267 completed green. |
| **#252 stylelint 16→17 red** | **CLOSED by policy, not merged.** #268 added a Dependabot ignore for stylelint majors: v17 changes warning semantics on byte-identical CSS, and the baseline deliberately pins 16.11.0. A major upgrade requires an owner-approved re-baselining packet. **The same reasoning is now pending for bootstrap — see P1.6.** |
| **Body Composition, Filter View Mode, workout.cool/YouTube curation, movement-pattern cleanup, response-contract migration, catalogue seed/packaging work** | **COMPLETE.** Reopen only for a concrete regression or new product request. |
| **Archived plan-volume unchecked tasks / archive-wide unchecked boxes** | Historical records, not open work, unless a current plan explicitly reactivates an item. |

## 3. Artifact and documentation retirement plan

### Safe to retire after this plan is committed and the listed checks pass

> **⚠️ EXECUTED — this table is a historical inventory, not a work list (2026-08-13).**
> The authorized set was removed under P1.2: 40 of 40 candidate worktrees, the 15
> literal artifact/build/log targets (≈1.07 GB, 2026-08-11), and the six owner-named
> `visual_review*` directories (2026-08-12). P1.7's two rows shipped as #285. The sizes
> below are 2026-08-02/03 measurements. **Two rows were never authorized and are
> untouched: `artifacts/wp4_4/` and `artifacts/environment-backups/…` remain held**, and
> `vbl_check`, `codex-pr309-review-7d03c7a`, `pr294-visual-diagnostics`, `e2e` and
> `dev-server` were verified present after the final pass. Deleting anything further is a
> **new** owner decision with its own path-specific authorization — this table confers
> none. Terminal disposition: [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9.5.

| Target | Observed size | Disposition |
|---|---:|---|
| Obsolete non-current Git worktrees — **DONE (P1.2)** | ~6+ GB | **Executed 2026-08-08; re-verified 2026-08-10.** 40 of 40 candidates removed non-forced, 0 skips / 0 failures, no branch deleted, prune dry-run empty. *Historical procedure:* **Recount at execution time** (30 at the v22 snapshot and still volatile). Apply P1.2's status/HEAD/patch-equivalence proof; skip every dirty worktree and every open-PR association. Known v22 exclusions include the Bootstrap spike, WP4.4 F1 navbar, current checkout, and any #269/#271 worktree still active at execution time. |
| `artifacts/playwright/` | 522 MB | Generated test output; delete when no failure investigation is active. |
| `artifacts/environment-backups/20260729-python-3.14.4/` | 460 MB | Obsolete after the Python 3.14.6 alignment, provided no current task references it. |
| `dist/` | 92 MB | Gitignored PyInstaller output; regenerated by `build_exe.bat`. |
| `build/` | 76 MB | Gitignored packaging staging output; regenerated on next build. |
| `logs/` | 63 MB | Delete old generated logs. The May fatigue observer log is stale evidence, not a live calibration record. |
| `artifacts/vbl_check/` | 21 MB | Visual-baseline scratch. **Verified present after the 2026-08-12 pass and NOT deleted** — it was outside the authorized set. P2.3 is retired, but that does not itself authorize removal; treat this as a fresh owner decision. |
| `debug/*` | ~1 MB | Delete, do not archive, per [`DOC_RETENTION.md`](ai_workflow/DOC_RETENTION.md). |
| `data/auto_backup/*.db-shm`, `*.db-wal` — **DONE (P1.7, #285)** | <1 MB | **Removed, and `.gitignore` extended** with `*.db-shm` / `*.db-wal`. *Historical:* orphaned SQLite sidecars, untracked **and** unignored. |
| `docs/requirements_dry_run/` — **DONE (P1.7, #285)** | empty | **Removed.** *Historical:* empty leftover directory. |

### Hold or review before deleting

| Target | Observed size | Why it is protected |
|---|---:|---|
| Any worktree backing an open PR | — | Recheck `gh pr list` immediately before the cleanup pass; the set changes daily. |
| `data/auto_backup/*.db` | 5.6 MB / 7 snapshots | Real recovery snapshots; retention/rotation owns them. |
| `artifacts/wp4_4/` | 643 MB | Theme-dark P3 may need prior instrumentation context. Extract reusable inputs or explicitly reject P3 before deleting. |
| current checkout and current document change | — | Never include in a bulk deletion. The main checkout currently holds uncommitted doc work (see Authority note). |
| local branches not proven patch-equivalent | — | Preserve salvage branches and unique commits; inspect PR/squash history first. |

### Documentation handling

- Keep canonical guides, indexes, decision records, current handover, generated
  inventories, and active product/workflow plans.
- Trim completed plans that accumulated append-only execution transcripts;
  preserve final decisions, migration constraints, evidence links, and reopen
  conditions.
- Archive completed plans only after no open references and ≥6 months without
  meaningful edits. The grounding-scan and `CSS_PHASE4_*` sets fail both today.
- **Load-bearing `docs/` paths in code (v21, concrete list):** before moving any
  doc, know that `scripts/generate_test_inventory.py`,
  `scripts/pyright_baseline_diff.py`, `scripts/css_audit/emit_baseline.py`,
  `scripts/fatigue_stage4_observer.py`, `scripts/fatigue_calibration_report.py`,
  ~18 references in `.github/workflows/ci.yml`, and `deep-gate.yml` all hardcode
  `docs/` paths. Grep the whole repo, not just docs.
- **v23 (N7) — `docs/` paths pinned by *tests*, which is the stricter class:**
  `tests/test_css_wp4_4_*.py`, `tests/test_profile_estimator_contract.py`,
  `tests/test_fatigue_stage4_observer.py`, `tests/test_calibration_integration.py`
  and `tests/test_erase_data_guard.py` all reference `docs/` paths. A CI-workflow
  reference reds an advisory job; a pytest reference reds the **required**
  `Run Tests`. Check both before moving anything.
- **v23 (N5) — generated-file contention.** `docs/test_inventory/TEST_INVENTORY.json`
  and `.md` are now guarded by a **required** check and are edited by #274, #275,
  and any packet that adds or removes a test (P1.4, P1.5). Regenerate as the last
  step of a packet, never mid-branch, and expect conflicts if two land together.
- Delete local/debug/generated command output instead of turning it into project
  memory. (`MASTER_HANDOVER.local.md` is gitignored, current, and operational —
  not a leftover.)

## 4. Remaining source TODOs

Three `TODO` markers remain in production Python, covering two decisions
(`constants.py` carries the same question on two adjacent alias lines). None is a
quick implementation task without an owner decision. No `TODO`/`FIXME` markers
remain in `static/js/`.

| Location | TODO | Disposition |
|---|---|---|
| [`utils/constants.py:19`](../utils/constants.py#L19) | Consider collapsing `Front-Shoulder` into anatomical deltoid naming. | **OWNER / taxonomy migration.** Cross-module string matching makes this a product/data migration, not a rename. |
| [`utils/constants.py:100-101`](../utils/constants.py#L100-L101) | Decide whether `Mid/Upper Back` remains a dedicated grouping (duplicated on both casing aliases). | **OWNER / taxonomy decision.** Preserve current aliases until decided; resolve both lines together. |
| ~~[`utils/program_backup.py:18`](../utils/program_backup.py#L18)~~ | ~~`schema_version` is written but not consumed.~~ | **RESOLVED 2026-08-14** — Testing Strategy D6 decided as retain-informational, recorded as [ADR-007](DECISIONS.md). The TODO is replaced by a stated contract at the definition site. |

## 5a. Evidence added at v23

Commands run read-only from an isolated worktree (`D:/development/HT-v23-audit`,
detached at this commit); the shared checkout was never switched or edited.

- **Reachability (N1):** `git ls-remote --heads origin` (no
  `docs/status-reconciliation`), `git branch --contains 2b16474` (two local
  branches only), `git branch -r --contains 2b16474` (empty),
  `gh pr list --head docs/status-reconciliation --state all` → `[]`, and
  `git show origin/main:docs/LEFTOVERS_BY_PRIORITY.md | tail` → *"Last updated:
  2026-06-11 (v17 …)"*.
- **Base currency (N-authority):** `git log --oneline 2b16474 -3` shows parent
  `ac16e4c` = `origin/main`; `git rev-list --left-right --count` confirms 1/0.
- **Dependency lane (N2, N4):** `gh pr view 269` → `state: CLOSED,
  mergedAt: null, closedAt: 2026-08-02T00:45:22Z`; `gh pr view 274/275` file
  lists and bodies; `gh pr checks 245` green, `gh pr checks 250` red on
  `JS Unit (Vitest, non-required)`.
- **Required contexts (N5):** branch-protection API returns 11 contexts
  including `Test Inventory Drift`; #274 and #275 both list
  `docs/test_inventory/TEST_INVENTORY.json` and `.md` in their changed files.
- **Spec collision (N6):** `e2e/ui-hardening.spec.ts:538-546` read at source —
  the KI-005 header still says "PRE-IMPLEMENTATION … expected to be RED".
- **Retention pinning (N7):** `grep -rhn -oE "CSS_PHASE4[A-Za-z0-9_]*\.(md|json)"
  tests/*.py` returns six artifacts; the seven `WP4_3I_*` orphans return nothing
  from `tests/`, `scripts/`, or `.github/`.
- **Cleanup executability (N8):** `guard-destructive-command.ps1:438-440`
  (`worktree` → `ask`) and `:397` (`reset --hard` → `deny`); `git worktree list`
  → 35 entries; per-worktree `git status --porcelain` → 3 dirty.
- **Methodology re-validation:** the link sweep re-run on this tree gives 606
  relative links / 12 broken, and the split matters — **4 are genuine active
  authority defects** (all `SHARED_PLAN.md`, P1.8), **2 sit in active folders but
  are historical** (`workout_cool_integration/*` pointing at a deleted generated
  screenshots directory), and **6 are archive records** in
  `archive/MISSING_TESTS_PART2.md`. Only the first group is work. The orphan
  methodology is basename-frequency and therefore false-positive-prone: v22's
  exclusion of `PROFILE_ESTIMATOR_CLUSTERS.md` is **confirmed correct**
  (`tests/test_profile_estimator_contract.py`, `utils/profile_estimator.py`
  reference it), and no remaining candidate is referenced from code or CI.

## 5. Evidence used for this revision

v21 deliberately took angles the prior passes did not; v22 re-ran the
execution-sensitive checks and corrected the queue where live state had moved:

- **Novel sweeps:** a scripted link-integrity check over every `docs/**/*.md`
  found 12 broken links (itemized; the total link count changes as this document
  adds links); a scripted inbound-reference check over 146 docs, followed by a
  v22 correction for references introduced by this plan and filename references
  from production/test code; a count-restating grep against the single-producer
  policy; a `docs/`-path grep across `tests/`, `scripts/`, and workflows.
- **Cross-numbering audit:** `SCAN_RECOMMENDATIONS.md` §A read in full and each
  A-item traced into `REFACTOR_PLAN.md` Track A / WPB packets, with scan-A12
  verified closed in code (`routes/exports.py` POST route, no `exercise_order`
  mutation) — resolving the collision that made earlier "shipped" rows
  under-enumerate.
- **Dependency policy:** `.github/dependabot.yml` read in full, including its
  own record of the Bootstrap+Sass SCSS break; #268's body and #252's CLOSED
  state confirmed via `gh`; #269's isolated failing checks inspected. The v22
  queue was recounted rather than copied from v21.
- **Git/GitHub:** `origin/main` re-fetched at `f178790`; the checkout remained at
  `5b7a4f1` (10 behind), #270/#272/#273 were merged, #271 remained open, and all
  dirty paths were enumerated. No pinned queue count is an execution input.
- **Docs:** `STAGE4_PARKED_HANDOFF.md`, the three orphan `user_profile/` design
  docs, `E2E_TESTING.md`, `CHANGELOG.md` entry list, `TEST_INVENTORY.md` header,
  `DECISIONS.md` ADR log, `docs/README.md`, and the new 699-line
  `CROSS_MODEL_ORCHESTRATION_PLAN.md` (untracked) all read at source.
- **Carried forward from v19/v20** (re-verified where volatile): worktree
  enumeration (30 at the v22 snapshot), artifact/log sizes, DB row counts,
  P1.3–P1.5 premises, production TODO markers, and branch-protection contexts.
  The v22 status pass found three dirty checkouts: current, Bootstrap spike, and
  WP4.4 F1 navbar; all are explicit P1.2 exclusions.

## 6. Definition of "closed" for this queue

An item leaves this file only when one of these is true:

1. the implementation and proportional verification have landed on `main`;
2. the owner explicitly rejects/parks it and the source plan records the reopen
   condition;
3. current code/data proves the premise obsolete, and active docs no longer
   present it as work; or
4. disposable artifacts are removed after the safety checks above.

**The sequence, recomputed at v26 (2026-08-14): there is no sequence left — P1 is
empty, and P2.1/P2.2 are retired.** Every P1 item has landed:
P1.0 #278, P1.1 #295, P1.2 #327 (execution recorded in
[`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9.5), P1.3 + P1.8 #292,
P1.4 #291, P1.5 #284, P1.6 by owner decision (closeout doc), P1.7 #285. **No item
in this file is READY, and nothing here should be dispatched as a next task.**

What genuinely remains, and it is all gated:

| Remaining | Status | Who decides |
|---|---|---|
| **P2.4** Broader KI-005 manual-edit provenance staleness | **OWNER / demand-gated** — a new UX packet only if it is visible in real use | owner |
| **§4** two production `TODO` decisions | **OWNER** — two taxonomy questions (`utils/constants.py`). The third, `schema_version`, was resolved 2026-08-14 by Testing Strategy D6 / [ADR-007](DECISIONS.md) | owner |
| The `npm audit` severity / exception policy | **OWNER** — held apart from P1.6 throughout and still undecided; [`P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md`](P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md) owns it | owner |
| **Remaining P3 proposals** | Legitimate future work, not forgotten activity; completed or terminated P3 bullets stay closed | owner, at Gate 0 |

**Two residuals are recorded here but owned elsewhere; do not schedule them from
this file.** The two WP4.0 Windows rendering observations belong to
[`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) § *Known Windows visual reds*, and the
deferred Playwright 1.62.1 bump belongs to
[`P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md`](P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md) with its
unblock condition on the `dependabot.yml` ignore rule.

> *Superseded 2026-08-13.* The section opened by recording that v22's own opener
> ("preserve the dirty doc patch → fetch/reconcile → commit the orchestration plan
> + INDEX row + this file together") had been discharged by the v23 commit — that
> remains true and is now simply old. It then read: *"What remains of it is:
> **P1.7** (sidecar-scoped, no production change) → **P1.5** … one
> `ui-hardening.spec.ts` at a time, regenerating the inventory last → **P1.2**
> cleanup of only proven-clean, unprotected, recounted targets."* All three had
> shipped by 2026-08-12 (#285, #284, #327). Retained so the ordering rationale is
> not lost: P1.5 and P1.4 collided on one spec file, and the generated test
> inventory is regenerated **last** in any packet that adds or removes a test —
> both still-good rules for future work, neither a live instruction.

P1.3/P1.8 no longer gate any workflow work. Their closeout preserves the role
boundary established by Agent Workflow v2: independent reviewers remain owned by
the manager or primary session, not by the implementing developer. Re-query any
remaining P2 premise before scheduling it; its row, not this historical
sequence, owns its current gate.

---

*Last updated: 2026-08-02 (v23 — final adversarial audit on top of `2b16474`:
found the arc unpublished and `origin` still serving v17, released P1.1's
already-satisfied WAIT gate, replaced the closed #269 with the #274 migration,
escalated P1.5 to a #274 merge prerequisite, recorded the #275→#250 chain, the
required-check generated-file contention, the P1.4/P1.5 spec collision, the
pytest-pinned retention constraint, and the guard-hook limits on cleanup
commands; verified against `origin/main` @ `ac16e4c`.)*

*Prior revisions retained above: v18 (Codex), v19–v20 (Opus), v21 (Fable 5
deep scan), v22 (execution-safety). v23 adds findings **N1–N9** and changes no
prior finding except where explicitly labelled a v23 correction.*

*Last updated: 2026-08-13 (v24 — truth-maintenance pass, docs-only, verified
against `origin/main` @ `af14036` with the checkout 0 ahead / 0 behind.
Retired five stale current-status claims — P1.5 (#284 `4e9b7d0`), P1.7 (#285
`4a24773`), the residual P1.2 PARTIAL wording (#327 `ae37365`), P2.3's baseline
execution item (#281/#294/#298/#309) and P2.5 (#286 `9683f77`) — and recomputed
§6, which is now empty of READY work. Also corrected one factual statement in P3:
#303 is merged (`42e8a4d`), not an unmerged draft — provenance only, the bullet
stays a PROPOSAL. **No new finding, no new scope, no
proposal promoted, no owner gate inferred as taken, no production TODO
disposition changed.** Every retired row is annotated in place with its original
text preserved. #330 landed mid-pass; every premise was re-verified against it.)*
