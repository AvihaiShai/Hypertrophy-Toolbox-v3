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

## Status key

| Status | Meaning |
|---|---|
| **READY** | Small, bounded work with no unresolved product decision. |
| **WAIT** | A named external condition must become true first. |
| **OWNER** | Requires an explicit owner choice; do not infer one. |
| **PROPOSAL** | Valid future work, but not a forgotten activity or current commitment. |
| **RETIRE** | Shipped, superseded, irrelevant, or disposable after the stated safety check. |

**Current classification (v23, superseding v22's):** **READY** — P1.5, P1.7
(**P1.0 has since shipped as #278, and P1.4 as #291 — see §2**);
**WAIT** — P1.2 (known dirty/open-PR
worktrees must be excluded — **P1.2 has since gone WAIT → READY → PARTIAL: the worktree
half executed 2026-08-08, the artifact half has not; see below**); **OWNER** — P2.1–P2.4;
every item in P3 is a **PROPOSAL**.

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

## 1. Recommended execution order

### P1 — Small closeouts that remove real debt

| ID | Activity | Why it is still open | Completion action | Effort |
|---|---|---|---|---:|
| P1.2 | **Remove obsolete worktrees and generated artifacts** — *2026-08-03: WAIT → **READY**, goal written: [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md); 2026-08-08: → **PARTIAL**, worktree half executed and re-verified 2026-08-10* | **Only the artifact half of this row is still open** — 40 of 40 candidate worktrees were removed, and the per-path disposition is [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md) §9 with its 2026-08-10 reconciliation in §9.1. What remains is §6 (generated artifacts, owner-gated on `environment-backups` and the held `wp4_4`/#281/#286 paths) and §7's Packet E (the preserved worktrees). *The v23 evidence below is historical and was superseded by the execution; it is kept for continuity — do not re-derive from it.* **The registered-worktree count is unstable — 24 at v19, 25 at v20, 29 at v21, 30 at v22, and 35 at the v23 recheck.** Recount with `git worktree list --porcelain` at execution time. **v23 additions (N8):** three worktrees are dirty right now — the shared checkout, `…-bs538-spike` (4 files; the #274 source), and `…-wp4-4-f1-navbar` (2). New since v22: `…-bs538-rebuild`, `…-node24-ci` (#275), `…-tsdrift`, and the read-only audit worktree `D:/development/HT-v23-audit` created for this revision (detached at this commit — **exclude it, and remove it only after P1.0 has published the branch**). The shared checkout **switched branch during this audit** (`docs/testing-strategy-reconciliation` → `docs/p3-gate-signoff`), so any branch/path fact here is evidence, never an execution input. **Command executability:** `git worktree remove` is intercepted by [`guard-destructive-command.ps1:438-440`](../.claude/hooks/guard-destructive-command.ps1) with decision **`ask`** — an unattended agent run stalls instead of proceeding — and `git reset --hard` is **denied** at `:397`, so no recovery path may rely on it. Known holds otherwise unchanged: any worktree associated with an open PR (now #245, #250, #274, #275) is protected. A local worktree branch name may differ from the GitHub PR head, so branch-name lookup alone is not proof. Generated output remains approximately: `artifacts/` 1.7 GB (`wp4_4` 643 MB held, `playwright` 522 MB, `environment-backups` 460 MB, `vbl_check` 21 MB), `build/` 76 MB, `dist/` 92 MB, `logs/` 63 MB, `debug/` 1 MB. | **Execute [`WORKTREE_CLEANUP_PLAN.md`](WORKTREE_CLEANUP_PLAN.md)** — it converts this cell into packets with a per-path disposition table and a 2026-08-03 recount (**42** worktrees, not 35). The procedure below is its §4 and remains authoritative. For **every** non-current worktree, record path/branch/HEAD and run `git status --short --untracked-files=all`; any output means **skip and preserve**. Query `gh pr list --state all --head <branch>`, but treat it only as one signal: also compare the worktree HEAD OID with PR commits and use Git patch-equivalence/diff checks because squash merges and alternate local branch names defeat ancestry/name tests. Remove only a clean worktree with no unique patch and no open-PR association, through `git worktree remove <exact-path>`, then `git worktree prune`; do not recursively delete a registered worktree and do not delete its branch unless separately proven disposable. Delete transient artifacts only after confirming no active investigation/process references them; retain the protected `wp4_4` bundle pending its explicit decision. | 1–3 h |
| P1.5 | **Close KI-006 with honest modal keyboard tests** | Confirmed. [`accessibility.spec.ts:103-115`](../e2e/accessibility.spec.ts#L103-L115) presses Escape, waits 500 ms, and then **clicks the close button if the modal is still open** — the test passes whether or not Escape works. The whole block is guarded by `if (btnVisible)`. The focus-trap assertion checks only that the *first* Tab stays inside, which cannot prove wraparound. **v23 escalation (N3): the hazard is no longer hypothetical.** Draft **#274** upgrades Bootstrap to 5.3.8 and lists among its validation "Chromium navigation/accessibility/UI sweep — **127 passed**" — a sweep that includes these very tests. A Bootstrap-5.3 modal regression in Escape handling or focus wraparound would pass that sweep silently. v22's wording ("before any Bootstrap *decision*, P1.6/#269") is both too weak and aimed at a PR that is now closed. | Add strict Escape and forward/backward wraparound assertions for the Plan and Log modals, without the fallback click and without the visibility guard. **Treat this as a merge prerequisite for #274, not a preference:** land P1.5, then re-run #274's accessibility/UI sweep against the strengthened tests before #274 leaves draft. Sequence against P1.4 (**N6** — both edit `e2e/ui-hardening.spec.ts`) and regenerate the test inventory last (**N5**). Fix production behavior only if the new tests expose a failure; otherwise this is a test-only closeout and KI-006 can be marked resolved in [`UI_SCENARIOS_GAP_ANALYSIS.md`](UI_SCENARIOS_GAP_ANALYSIS.md). | 2–4 h |
| P1.6 | **CLOSED 2026-08-03 — disposition in [`P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md`](P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md).** All four v23 lanes discharged (#283 superseded #245; #274, #275, #250 merged 2026-08-02), and the two dependency PRs that opened afterwards were closed by owner decision: **#288** (`@playwright/test` 1.62.1) deferred — the bump moves Chromium 148 → 151 and would silently stale every visual baseline, since the visual specs run only in `deep-gate.yml`'s manual `visual-linux` job; **#287** (`stylelint` 16.26.1) refused — the pin is the CSS measurement instrument. Both are now `dependabot.yml` ignore rules, with the Playwright unblock condition (#281 merged **and** #286 resolved, then bump both ecosystems and regenerate both platforms' baselines in one arc) recorded on the rule itself. *Historical v23 record follows.* **Triage the dependency queue — v23: the queue drained and the Bootstrap lane was decided** | **Recount with `gh pr list --state open` at execution time.** Since v22, #240/#243/#244/#246 (Actions v7), #249 (`@types/node` 26), #251 (**TypeScript 7**) and #261 (`sass`) all **merged**, and **#269 was CLOSED, not merged** (**N2**). Only two dependency PRs remain: **#245** (`playwright` 1.61, all checks green) and **#250** (`jsdom` 30, red on JS Unit). Two owner drafts now carry the hard work: **#274** — the deliberate Bootstrap 5.3.8 migration that replaces #269 (SCSS import graph, rebuilt bundle, CDN pin, version contract), and **#275** — Node 20 → Node 24 across 13 `setup-node` pins plus a version contract. **N4:** #250's red is fully explained — jsdom 30 requires Node `^22.22.2 \|\| ^24.15.0 \|\| >=26`, so #275 is its prerequisite and #275 deliberately excludes it. **#252/#268 policy note stands:** the stylelint-major ignore remains the precedent, but it is no longer the open question for bootstrap. | Four lanes: **(a)** merge **#245** now — it is green and independent; **(b)** land **#275**, then rebase and re-validate **#250** against Node 24 — do not investigate #250 on its own; **(c)** **#274 is blocked twice over** — by P2.3's stale Linux baselines (its own stated blocker) *and*, per **N3**, by P1.5: it must not leave draft until the modal tests can actually fail; **(d)** the Actions-v7/TypeScript-7 majors are discharged — verify `Type Check (tsc blocking …)` stayed green on `main` after #251 rather than assuming it. Keep the `npm audit` severity/exception-policy decision separate. | **DONE 2026-08-03.** `npm audit` policy remains the one open, separate decision. |
| P1.7 | **Close two repository-hygiene gaps** | Still present at this audit. (a) `.gitignore:29`'s `*.db` does not match SQLite sidecars, so `data/auto_backup/database_20260712_000549.db-shm` and `.db-wal` sit **untracked and unignored** — one `git add -A` from being committed. Their presence beside a July-12 snapshot also means a backup DB was opened read-write and not clean-closed. (b) `docs/requirements_dry_run/` is an empty leftover directory. | Add `*.db-shm` / `*.db-wal` to `.gitignore`, delete the two orphaned sidecars after confirming no process holds them, and remove the empty directory. No production change. | 15–30 min |

### P2 — Product/workflow activities that can be explicitly closed or advanced

| ID | Activity | Real state / gate | Completion action | Effort |
|---|---|---|---|---:|
| P2.1 | **Fatigue *Phase 2* Stage 4 disposition** | **Disambiguation first (v21):** two "Stage 4"s exist. *Phase 1* Stage 4 was parked 2026-05-13 and **closed 2026-05-20** — [`STAGE4_PARKED_HANDOFF.md`](fatigue_meter/STAGE4_PARKED_HANDOFF.md) carries a proper SUPERSEDED banner. The open item is ***Phase 2*** Stage 4 ([`PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md), window opened 2026-05-24). That window is inactive: every user table in `data/database.db` is empty (`workout_log=0`), the last observer log is 2026-05-30, no scheduled task is installed. Learned Calibration 2D-D depends on the same missing evidence. | **OWNER:** (a) restart real-use collection and keep Stage 4 open, or (b) close the inactive window as "no evidence / no threshold change," park 2D-D, and retire the no-longer-used observer tooling instructions **plus the generated artifacts committed under `docs/fatigue_meter/`** (`baseline-2026-04-30*.txt`, `generated-calibration-report.md`) per retention policy. **v23 safety check on that cleanup:** `generated-calibration-report.md` is `DEFAULT_OUTPUT` of [`scripts/fatigue_calibration_report.py:32-36`](../scripts/fatigue_calibration_report.py) and is rewritten by `output.write_text(...)` at `:546` — it is regenerable script output, so deleting it loses no evidence. But `tests/test_fatigue_stage4_observer.py` and `tests/test_calibration_integration.py` both reference `docs/` paths, so confirm neither pins the files being retired before removing them (**N7**). Never tune thresholds or make 2D-D prescriptive without the documented evidence bar and fresh approval. | 15 min decision; weeks if restarted |
| P2.2 | **Fatigue body heatmap** | Owner-requested and technically close to assembly, but [`HEATMAP_PLANNING.md`](fatigue_meter/HEATMAP_PLANNING.md) remains a draft with six owner decisions. Existing MuscleMap SVG, body-map coloring code, fatigue `muscle_rows`, band colors, and period reload behavior cover most of the implementation surface. | Resolve §8 decisions, sign the plan, implement a visualization-only slice with no formula/threshold/schema/API change, and close it. | 1–2 d after decisions |
| P2.3 | **Visual-baseline debt: the Windows pair plus stale Linux baselines** | Two real Windows-only failures remain: the animated navbar logo in Workout Plan desktop dark, and `plan-desktop-light-advanced` in `visual-baseline-thumbnails.spec.ts` (**6,084 px** measured / 6,098 retry vs **6,262 px** baseline — [`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) Windows ledger). New on `origin/main` via #273: the **Linux** baselines were last written before 57 later CSS/template commits and now produce at least 11 failures (57 pass, 16 do not run); this is separate from the Windows pair and blocks the signed D3 weekly deep-gate stopgap. [`QUALITY_GATE.md`](ai_workflow/QUALITY_GATE.md) does not yet describe the full platform-specific state. | **OWNER action first:** run the Linux generate workflow, download and inspect all 84 PNGs by eye, commit only approved baselines, then confirm Linux compare is green before adding D3's weekly schedule. Separately stabilize the Windows animation/snapshot timing and diagnose the advanced-thumbnail delta; never blind-rebaseline or raise the global tolerance. **v23: the Bootstrap coordination target is now #274, not the closed #269** — and the dependency runs the other way: #274 names this stale-baseline debt as its *own* blocker, so the Linux regeneration is a prerequisite for the Bootstrap migration, not merely something to coordinate with it. | 0.5–2 d + owner visual review |
| P2.4 | **Broader KI-005 manual-edit provenance staleness** | KI-005 itself is shipped and Gate-2 approved. Only the explicitly accepted limitation remains: arbitrary manual edits can leave estimate provenance/ancillary text stale. | Treat as a new UX packet only if this is visible or confusing in real use. Do not reopen the completed KI-005 implementation plan for cosmetic comment work. | OWNER / demand-gated |
| P2.5 | **The CI visual gate certifies a broken-icon state — FontAwesome is CDN-only with no fallback** *(new 2026-08-02)* | [`base.html:16`](../templates/base.html) loads FontAwesome from `cdnjs.cloudflare.com` with **no local fallback** — unlike the Bootstrap stylesheet at `:15`, which falls back to jsdelivr. It does not resolve on the CI runner, so **every icon renders as a magenta placeholder square** in the committed Linux baselines. Confirmed identical in the pre- and post-regeneration sets during the #281 review, so it is **long-standing and did not block that recovery**. The consequence is what matters: the visual gate compares one broken-icon render against another, so **no icon regression can ever fail it**, and any future change that genuinely breaks icons passes silently. This is the same "a gate that cannot fail" class as the `occurrences <= 1` assertion and `measure.verify_blind_spots()`. | Ship FontAwesome as a **deterministic local asset**, or give it the same `onerror` fallback the Bootstrap link already has, then regenerate both platforms' baselines once so they encode a real icon render. **Do not fix this inside a baseline-recovery packet** — it is a rendering change and needs its own before/after. | 2–4 h + one baseline regeneration |
| P2.6 | **`j_known_live_mutation.mjs` pins a raw-byte digest that cannot match on Linux** — **SHIPPED 2026-08-04** *(new 2026-08-02)* | **Closed by the LF-normalization packet.** The tool now hashes the **LF-normalized text** — UTF-8 with every `CRLF` collapsed to `LF` — and pins `3ab06083c89eae0b5dd46d820dde4d2da1d59de1ffa6d825585aaca0ad17e14a`, which is the committed blob's own digest, so a Windows and a Linux checkout of the same commit both satisfy the gate without `--expect-sha`. Only content is pinned: the mutated file is written back with the line endings it arrived with, byte-for-byte identical to what the previous script produced here. `tests/test_css_audit_digest_normalization_contracts.py` pins the property from both ends (the constant is the canonical digest of the tracked file; both checkout forms are accepted and report identical digests; a genuinely edited stylesheet is still refused), and the pytest CI job now sets up Node so those cannot silently skip. `theme-dark.css` is untouched and **P3 stays terminated**. The durable rule went to [`verification.md`](../.claude/rules/verification.md) § Windows scripting hazards. **Original finding, retained:** [`scripts/css_audit/j_known_live_mutation.mjs`](../scripts/css_audit/j_known_live_mutation.mjs) read `theme-dark.css` with `readFileSync` (an untranslated Buffer) and hashed the raw bytes, so its pinned `EXPECTED_INPUT = e54818bf…` was the **CRLF** digest. The repo is `core.autocrlf=true` with **no `.gitattributes`**, so the committed blob is LF and hashes to `3ab06083…` — exactly **574 bytes** smaller, one `CR` per line. The control therefore **ran on Windows and refused to run on Linux**, where it would have demanded the very `--expect-sha` override its own docstring forbids using to silence it. Surfaced by P3-a0, which corrected its own evidence claim; **a0 hit the identical hazard in its contract file and CI caught it** (PR #280). Recorded as debt rather than fixed: it sat outside a0's owned paths and **P3 is terminated — this must not reopen it**. | **Done.** Of the two options this row offered, the first was taken: normalize before hashing. The `.gitattributes` alternative was rejected — it would have re-pinned this one constant by changing how *every* file in the repository is checked out, to fix a defect that lives in one script. **The standing obligation survives the closure: any future packet that re-pins that digest must still state which line-ending form it pinned**, and the contract test now reds if the constant stops being the canonical digest of the tracked file. | 1–2 h *(actual: ~1 h)* |

### P3 — Valid proposals, not forgotten near-complete work

These items remain legitimate but should not displace the P1–P2 closeouts:

- **Testing Strategy Phases 2–5 and remaining decisions** in
  [`TESTING_STRATEGY_PLANNING.md`](TESTING_STRATEGY_PLANNING.md). Phases 0–1 are
  complete; #270 corrected the handover and is merged. D1 and the
  `e2e-erase-flow` half of D2 are signed; #272/#273 additionally signed **D5**
  (Chromium-only, shipped as ADR-004) and the **D3 weekly deep-gate stopgap**.
  D3 is authorized but blocked on P2.3's stale Linux baselines. **D4, D6, D7
  and the `js-unit` half of D2 remain unsigned.** Python and JS coverage remain
  measurement-only; Phases 2, 3 and 5 remain proposals, and Phase 4 is not
  complete.
- **Product documentation suite** in [`PRODUCT_DOCS_PLAN.md`](PRODUCT_DOCS_PLAN.md):
  a fresh proposal, not stale work. App Flow and Design Brief are the clearest
  gaps; Gate 0/1 and revision are still required.
- **Cross-model orchestration** in
  [`ai_workflow/CROSS_MODEL_ORCHESTRATION_PLAN.md`](ai_workflow/CROSS_MODEL_ORCHESTRATION_PLAN.md):
  a newly authored proposal (699 lines, Gate 0/Gate 1 pending) for an opt-in
  `$orchestrate` Codex→Opus delegation flow. **v21 caution: the file is
  currently untracked and its `INDEX.md` row uncommitted** — it exists only in
  this checkout until committed; see P1.1's sequencing note. It is a proposal,
  not a leftover.
- **Theme-dark P3** in [`css_theme_dark_p3/PLANNING.md`](css_theme_dark_p3/PLANNING.md):
  fresh, council-reviewed planning with Gate 0 and Gate 1 unsigned. A large CSS
  change, not a cleanup leftover.
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
- **Inert `d-flex` / `d-inline-block` consumers.** OD-2 (implemented and
  owner-accepted in **draft PR #303**, unmerged) restored Bootstrap's `display`
  utility but deliberately narrowed it to `values: none inline` — enough for
  `d-none` and its indivisible `d-lg-inline` partner, and no further. `d-flex`
  (15 call sites) and `d-inline-block` (1, `templates/fatigue.html:22`) are
  therefore **still inert by design**, recorded in `KNOWN_INERT` and pinned by
  `tests/test_css_display_utilities_contracts.py::test_the_deliberately_withheld_utilities_stay_withheld`,
  so the narrowing cannot widen without updating the contract. Activating them is
  a one-line SCSS change but **a rendering change, not a bug fix**: measured
  against a same-machine baseline it moves **12 further visual captures** —
  session-summary ×6 and weekly-summary ×6 at 120k–564k pixels each, because
  those pages build `d-flex` rows in JS — plus the `/fatigue` period select from
  `block` to `inline-block`. Needs its own packet with **dedicated
  visual-baseline review and regeneration**; do not fold it into an unrelated
  change. Measurement:
  [`dnone_display_utilities/EVIDENCE.md`](dnone_display_utilities/EVIDENCE.md) §3, §7.
- **Nothing ties the committed `bootstrap.custom.min.css` to its SCSS source.**
  The bundle is tracked, but the pytest CI job deliberately does not run
  `npm ci` / `npm run build:css`, so pytest asserts against the *committed*
  artifact. Every E2E job does rebuild it, overwriting it at runtime. So editing
  `scss/custom-bootstrap.scss` and forgetting `npm run build:css` leaves the
  display-utility contracts green against a stale artifact while E2E silently
  exercises different CSS. Pre-existing, but PR #303 is the first change to lean
  on the artifact as a contract surface, which is what makes it worth closing.
  Cheap fix: a CI step that runs `build:css` then fails on
  `git diff --exit-code static/css/bootstrap.custom.min.css`. (Verified by hand
  during #303 — the committed bundle *is* currently reproducible: a fresh
  `npm run build:css` produced a byte-identical blob, `71c4046b`.)
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
| **Learned Calibration 2A–2D-C** | **SHIPPED.** Only 2D-D remains, blocked with P2.1's real-use evidence gate. |
| **Fatigue *Phase 1* Stage 4** | **CLOSED 2026-05-20, owner-reviewed, no threshold changes.** [`STAGE4_PARKED_HANDOFF.md`](fatigue_meter/STAGE4_PARKED_HANDOFF.md) is properly superseded-bannered. Do not confuse with the open *Phase 2* Stage 4 (P2.1). |
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

| Target | Observed size | Disposition |
|---|---:|---|
| Obsolete non-current Git worktrees | ~6+ GB | **Recount at execution time** (30 at the v22 snapshot and still volatile). Apply P1.2's status/HEAD/patch-equivalence proof; skip every dirty worktree and every open-PR association. Known v22 exclusions include the Bootstrap spike, WP4.4 F1 navbar, current checkout, and any #269/#271 worktree still active at execution time. |
| `artifacts/playwright/` | 522 MB | Generated test output; delete when no failure investigation is active. |
| `artifacts/environment-backups/20260729-python-3.14.4/` | 460 MB | Obsolete after the Python 3.14.6 alignment, provided no current task references it. |
| `dist/` | 92 MB | Gitignored PyInstaller output; regenerated by `build_exe.bat`. |
| `build/` | 76 MB | Gitignored packaging staging output; regenerated on next build. |
| `logs/` | 63 MB | Delete old generated logs. The May fatigue observer log is stale evidence, not a live calibration record. |
| `artifacts/vbl_check/` | 21 MB | Visual-baseline scratch; delete unless P2.3 is actively using it. |
| `debug/*` | ~1 MB | Delete, do not archive, per [`DOC_RETENTION.md`](ai_workflow/DOC_RETENTION.md). |
| `data/auto_backup/*.db-shm`, `*.db-wal` | <1 MB | Orphaned SQLite sidecars, untracked **and** unignored. Delete and extend `.gitignore` (P1.7). |
| `docs/requirements_dry_run/` | empty | Empty leftover directory; remove (P1.7). |

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

Four `TODO` markers remain in production Python, covering three decisions
(`constants.py` carries the same question on two adjacent alias lines). None is a
quick implementation task without an owner decision. No `TODO`/`FIXME` markers
remain in `static/js/`.

| Location | TODO | Disposition |
|---|---|---|
| [`utils/constants.py:19`](../utils/constants.py#L19) | Consider collapsing `Front-Shoulder` into anatomical deltoid naming. | **OWNER / taxonomy migration.** Cross-module string matching makes this a product/data migration, not a rename. |
| [`utils/constants.py:100-101`](../utils/constants.py#L100-L101) | Decide whether `Mid/Upper Back` remains a dedicated grouping (duplicated on both casing aliases). | **OWNER / taxonomy decision.** Preserve current aliases until decided; resolve both lines together. |
| [`utils/program_backup.py:18`](../utils/program_backup.py#L18) | `schema_version` is written but not consumed. | Testing Strategy decision D6: define/enforce compatibility or explicitly remove the unused contract. Do not silently implement a migration policy. |

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

**The sequence, corrected at v23.** v22's opener ("preserve the dirty doc patch
→ fetch/reconcile → commit the orchestration plan + INDEX row + this file
together") is **already done** — that is this commit. The live sequence is:

**P1.0 has shipped** (#278), **P1.1 has shipped** (#295), and **P1.3 + P1.8
shipped together** (#292) — all are in §2 and are no longer steps in this
sequence. What remains of it is: **P1.7**
(sidecar-scoped, no production change) → **P1.5** (P1.4 followed it and has now
shipped — §2), one `ui-hardening.spec.ts` at a time, regenerating the inventory
last → **P1.2** cleanup of only proven-clean, unprotected, recounted targets.

P1.3/P1.8 no longer gate any workflow work. Their closeout preserves the role
boundary established by Agent Workflow v2: independent reviewers remain owned by
the manager or primary session, not by the implementing developer. Re-query the
remaining P1/P2 premises before scheduling them; their rows, not this historical
v23 sequence, own their current gates.

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
