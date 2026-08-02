# Leftovers by Priority

> **Audit snapshot:** 2026-08-02, deep-scan revision v22 (post-Fable execution-
> safety review). Codex authored v18, Opus re-verified as v19, v20 reconciled
> #264–#267, v21 added the third-model deep scan, and v22 makes the resulting
> queue safe and executable.
>
> **Purpose:** current, evidence-based queue of unfinished work, small closeouts,
> stale plans, and disposable artifacts. This replaces the June punch list and
> its long closed-item history. Historical implementation evidence stays in the
> linked source plans, Git history, and the archive.
>
> **Authority:** use freshly fetched `origin/main`, generated inventories,
> current code, and read-only runtime data ahead of old prose. At the v22
> recheck `origin/main` had advanced to `f178790`; the shared checkout remained
> at `5b7a4f1` (**10 behind**) with overlapping uncommitted doc work. These are
> snapshot facts, not execution inputs: fetch, recompute divergence, and recount
> PRs/worktrees immediately before acting. Preserve and reconcile the dirty doc
> patch before updating `main`; never pull through it blindly.

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

## Status key

| Status | Meaning |
|---|---|
| **READY** | Small, bounded work with no unresolved product decision. |
| **WAIT** | A named external condition must become true first. |
| **OWNER** | Requires an explicit owner choice; do not infer one. |
| **PROPOSAL** | Valid future work, but not a forgotten activity or current commitment. |
| **RETIRE** | Shipped, superseded, irrelevant, or disposable after the stated safety check. |

**Current classification (v22):** **READY** — P1.4, P1.5, P1.7;
**WAIT** — P1.1 (reconcile the dirty doc patch with current `main` and #271),
P1.2 (known dirty/open-PR worktrees must be excluded); **OWNER** — P1.3,
P1.6, P1.8, P2.1–P2.4; every item in P3 is a **PROPOSAL**. Artifact
targets explicitly labeled safe-to-retire are **RETIRE** only after their stated
safety checks. There is no weaker "OWNER-lite" status.

## 1. Recommended execution order

### P1 — Small closeouts that remove real debt

| ID | Activity | Why it is still open | Completion action | Effort |
|---|---|---|---|---:|
| P1.1 | **Documentation truth and compaction pass** — *WAIT on reconciliation with current `main` and #271* | PR #265 merged (WPB.4 plan banner, handover flip gate, registry row 8), and **#270 is merged** (testing-strategy workstream status). PR **#271 remains open** at the v22 snapshot and corrects the Test Inventory job-summary prose. **Residue after reconciling those changes:** `DUPLICATION_REGISTRY.md` rows **3, 11, 14** + its summary-table/row-4 contradiction; [`ai_workflow/INDEX.md`](ai_workflow/INDEX.md) omissions (testing-strategy, theme-dark P3, app.py review, product-docs; still calls the Fatigue *Phase 2* Stage 4 window open) — note an **uncommitted local edit** already adds the cross-model row; [`UI_SCENARIOS_GAP_ANALYSIS.md`](UI_SCENARIOS_GAP_ANALYSIS.md) KI-003/KI-007 stale statuses; [`QUALITY_GATE.md`](ai_workflow/QUALITY_GATE.md) omits part of the current visual-red state; [`fatigue_meter/PLANNING.md:3`](fatigue_meter/PLANNING.md) "awaiting sign-off on Stage 0"; [`REFACTOR_PLAN.md:425`](REFACTOR_PLAN.md) WPB.4-is-gated inside a dated block; and [`MASTER_HANDOVER.md:107`](MASTER_HANDOVER.md) restates stale generated test totals. **New in v21/v22:** [`CHANGELOG.md`](CHANGELOG.md) ends at July 29 — WPB.4 (user-visible weekly-summary change), asset cache-versioning (#262/#266), and the CI gate promotions (#248/#267) are unrecorded; [`E2E_TESTING.md`](E2E_TESTING.md) (last updated 2026-06-10) is a hand-maintained per-spec inventory violating the single-producer rule — gut its counts and point at [`test_inventory/TEST_INVENTORY.md`](test_inventory/TEST_INVENTORY.md); [`docs/README.md:13`](README.md) still describes this file as the June "punch list" and sells `E2E_TESTING.md` as "current inventory"; [`TESTING_STRATEGY_PLANNING.md`](TESTING_STRATEGY_PLANNING.md) also carries dated copied totals; the remaining inbound-reference candidates need an index link or archive-disposition entry when retention permits: `CSS_PHASE4_WP4_3I_B_EVIDENCE.md`, `_C_`, `_D_`, `_E_`, `_F_`, `_G_`, `_H_`, `WP3_5_FETCH_INVENTORY.md`, `archive/CLEANUP_V2_DEAD_CODE_AUDIT.md`, and `user_profile/DUMBBELL_LOAD_BASIS_FIX.md`. The v21 pre-revision scan also counted `PROFILE_ESTIMATOR_CLUSTERS.md` and `RELATED_EXERCISE_TRANSFER_DESIGN.md`; v22 excludes them because production/test code references the former and this queue now links the latter. | First preserve this dirty patch, fetch, and reconcile it with the merged #270/#272/#273 changes plus #271 if that PR has landed by execution time. Then sweep only the named residue. **Never copy a replacement test count into prose**; link to the generated inventory. Mark dated blocks as historical rather than rewriting them. **Sequencing:** this file's P3 links to `CROSS_MODEL_ORCHESTRATION_PLAN.md`, which is still **untracked** — commit that file (with its INDEX row) before or with this one, or the link breaks on `main`. Do not archive recent completed plans until [`DOC_RETENTION.md`](ai_workflow/DOC_RETENTION.md)'s 6-month/no-open-reference rule is met. | 2–4 h |
| P1.2 | **Remove obsolete worktrees and generated artifacts** | **The registered-worktree count is unstable — 24 at v19, 25 at v20, 29 at v21, 30 at the v22 recheck.** Recount with `git worktree list --porcelain` at execution time. Known holds at v22: `…-bs538-spike` has uncommitted changes in `scss/custom-bootstrap.scss`, the generated Bootstrap bundle/map, and `templates/base.html`; `…-wp4-4-f1-navbar` carries untracked `.venv`/`node_modules`; the current checkout carries the doc patch; and any worktree associated with an open PR (including #269/#271 work at this snapshot) is protected. A local worktree branch name may differ from the GitHub PR head, so branch-name lookup alone is not proof. Generated output remains approximately: `artifacts/` 1.7 GB (`wp4_4` 643 MB held, `playwright` 522 MB, `environment-backups` 460 MB, `vbl_check` 21 MB), `build/` 76 MB, `dist/` 92 MB, `logs/` 63 MB, `debug/` 1 MB. | For **every** non-current worktree, record path/branch/HEAD and run `git status --short --untracked-files=all`; any output means **skip and preserve**. Query `gh pr list --state all --head <branch>`, but treat it only as one signal: also compare the worktree HEAD OID with PR commits and use Git patch-equivalence/diff checks because squash merges and alternate local branch names defeat ancestry/name tests. Remove only a clean worktree with no unique patch and no open-PR association, through `git worktree remove <exact-path>`, then `git worktree prune`; do not recursively delete a registered worktree and do not delete its branch unless separately proven disposable. Delete transient artifacts only after confirming no active investigation/process references them; retain the protected `wp4_4` bundle pending its explicit decision. | 1–3 h |
| P1.3 | **Fix the `/verify-and-polish` → `/handover` skill-guard contradiction** | **Confirmed verbatim.** [`senior-developer.md:30`](../.claude/agents/senior-developer.md) passes `-AllowedCsv run-tests,run-e2e,verify-suite,verify-and-polish,verify,run,build-css,run-hypertrophy-toolbox` — no `handover` — while [`verify-and-polish.md:11`](../.claude/commands/verify-and-polish.md) makes `/handover` step 4. The agent can start the command it is allowed to run and then be blocked partway through it. | Decide the intended contract, then either permit `handover` for `senior-developer` or remove/delegate that step. Add a guard test for the chosen path. The older `git merge-base` false-positive is already fixed and must not be reopened. | 30–90 min |
| P1.4 | **Delete the remaining small UI/debug scaffolding** | **All six confirmed in the live tree.** A user-visible `Available exercises: {{ exercises|length }}` block at [`progression_plan.html:21`](../templates/progression_plan.html#L21); **17** unguarded `console.log` calls in [`progression-plan.js`](../static/js/modules/progression-plan.js); an inert `const APP_DEBUG = false` wrapper at [`app.js:35`](../static/js/app.js#L35); zero-caller `handleApiResponse()` at [`workout-plan.js:94`](../static/js/modules/workout-plan.js#L94); `WORKOUT_PLAN_DEBUG` declared twice (module scope in `workout-plan-add-exercise.js:33`, function scope in `workout-plan.js:137`); and [`ui-hardening.spec.ts:541-546`](../e2e/ui-hardening.spec.ts#L541) still labels the now-green KI-005 tests "PRE-IMPLEMENTATION" and "expected to be RED." The E2E assertion at [`progression.spec.ts:98`](../e2e/progression.spec.ts#L98) is wrapped in `if (await debugInfo.isVisible())`, so deleting the template block does **not** red that test. | One bounded hygiene packet: remove the visible debug counter and simplify the now-dead E2E branch; remove or consistently gate the verbose logs; delete the zero-caller helper; consolidate the two inert debug wrappers; correct only the named KI-005 comment block. Run affected Vitest/pytest plus `e2e/progression.spec.ts` and Workout Plan smoke coverage. Ignore the copies under `build/` and `dist/` — regenerated output. | 1–3 h |
| P1.5 | **Close KI-006 with honest modal keyboard tests** | Confirmed. [`accessibility.spec.ts:103-115`](../e2e/accessibility.spec.ts#L103-L115) presses Escape, waits 500 ms, and then **clicks the close button if the modal is still open** — the test passes whether or not Escape works. The whole block is guarded by `if (btnVisible)`. The focus-trap assertion checks only that the *first* Tab stays inside, which cannot prove wraparound. **v21 note:** these tests exercise Bootstrap 5.1.3 modal defaults — land this closeout *before* any Bootstrap upgrade decision (P1.6/#269), or the upgrade ships against tests that can't fail. | Add strict Escape and forward/backward wraparound assertions for the Plan and Log modals, without the fallback click and without the visibility guard. Fix production behavior only if those tests expose a failure; otherwise this is a test-only closeout and KI-006 can be marked resolved in [`UI_SCENARIOS_GAP_ANALYSIS.md`](UI_SCENARIOS_GAP_ANALYSIS.md). | 2–4 h |
| P1.6 | **Triage the dependency queue — including the Bootstrap policy gap** | **Recount with `gh pr list --state open` at execution time.** At the v22 recheck the open queue was six Dependabot PRs (#245, #249–#251, #261, #269) plus owner #271; #240/#243/#244/#246 had merged, as had #270. **#252 was CLOSED by policy** — #268 added a Dependabot ignore for stylelint *majors* after v17 changed warning semantics on identical CSS. **The remaining policy gap:** that ignore names only stylelint, and **#269 re-files bootstrap 5.1.3→5.3.8**; its isolated CI run confirms the SCSS build failure (`_functions.scss` undefined-variable), not merely the earlier grouped Bootstrap+Sass ambiguity. Bootstrap 5.1→5.3 is technically semver-minor, so the "majors are isolated" convention never catches it, and it will re-file weekly. Bootstrap 5.1.3 is load-bearing across `templates/base.html`, the SCSS build, KI-006 modal semantics, and both platform visual-baseline sets. Older heads may also predate current required contexts and remain `BLOCKED` until refreshed. | Three lanes: **(a)** refresh/rebase green low-risk updates and merge in small batches; **(b)** decide #269 the way #252 was decided — either extend the `dependabot.yml` ignore to bootstrap or authorize a deliberate Bootstrap-5.3 migration packet that fixes SCSS and then runs the modal + Windows/Linux visual gates; do not let it linger as a weekly re-filer; **(c)** review each remaining major (#249 node types and #251 TypeScript 7 at this snapshot) individually. The Actions-v7 queue is discharged at v22 but must be recounted rather than copied forward. Keep the `npm audit` severity/exception-policy decision separate. | 2–6 h |
| P1.7 | **Close two repository-hygiene gaps** | Still present at this audit. (a) `.gitignore:29`'s `*.db` does not match SQLite sidecars, so `data/auto_backup/database_20260712_000549.db-shm` and `.db-wal` sit **untracked and unignored** — one `git add -A` from being committed. Their presence beside a July-12 snapshot also means a backup DB was opened read-write and not clean-closed. (b) `docs/requirements_dry_run/` is an empty leftover directory. | Add `*.db-shm` / `*.db-wal` to `.gitignore`, delete the two orphaned sidecars after confirming no process holds them, and remove the empty directory. No production change. | 15–30 min |
| P1.8 | **Resolve the `.claude/SHARED_PLAN.md` ghost authority** — *new in v21* | Three **active** workflow docs claim to *implement* a tiered plan system whose source file does not exist: [`PARALLEL_WORKFLOW.md:3`](ai_workflow/PARALLEL_WORKFLOW.md) ("Implements `.claude/SHARED_PLAN.md` Tier 2.1"), [`PLAN_REVIEW_TEMPLATE.md:3`](ai_workflow/PLAN_REVIEW_TEMPLATE.md) ("Tier 2.2 Appendix A2.2"), and [`WORKSTREAM_OWNERSHIP.md:3,32`](ai_workflow/WORKSTREAM_OWNERSHIP.md) ("Appendix A2.1"). Only `INDEX.md` hedges ("optional… if present"). An agent told to consult the tier definitions has nowhere to go; the tier/appendix numbering is now meaningless. This survived every prior audit because no pass checked links in *workflow* docs. | **OWNER decision, then 30 min:** either restore/recreate a minimal `SHARED_PLAN.md` defining the tiers, or (simpler, recommended) strip the "Implements Tier …" claims and let each doc stand on its own authority. Update `INDEX.md:9` to match. Also fix or annotate the two historical broken links in `workout_cool_integration/` (deleted screenshots dir) and the six in `archive/MISSING_TESTS_PART2.md` only if touched for other reasons — archive docs are point-in-time records. | 30–60 min |

### P2 — Product/workflow activities that can be explicitly closed or advanced

| ID | Activity | Real state / gate | Completion action | Effort |
|---|---|---|---|---:|
| P2.1 | **Fatigue *Phase 2* Stage 4 disposition** | **Disambiguation first (v21):** two "Stage 4"s exist. *Phase 1* Stage 4 was parked 2026-05-13 and **closed 2026-05-20** — [`STAGE4_PARKED_HANDOFF.md`](fatigue_meter/STAGE4_PARKED_HANDOFF.md) carries a proper SUPERSEDED banner. The open item is ***Phase 2*** Stage 4 ([`PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md), window opened 2026-05-24). That window is inactive: every user table in `data/database.db` is empty (`workout_log=0`), the last observer log is 2026-05-30, no scheduled task is installed. Learned Calibration 2D-D depends on the same missing evidence. | **OWNER:** (a) restart real-use collection and keep Stage 4 open, or (b) close the inactive window as "no evidence / no threshold change," park 2D-D, and retire the no-longer-used observer tooling instructions **plus the generated artifacts committed under `docs/fatigue_meter/`** (`baseline-2026-04-30*.txt`, `generated-calibration-report.md`) per retention policy. Never tune thresholds or make 2D-D prescriptive without the documented evidence bar and fresh approval. | 15 min decision; weeks if restarted |
| P2.2 | **Fatigue body heatmap** | Owner-requested and technically close to assembly, but [`HEATMAP_PLANNING.md`](fatigue_meter/HEATMAP_PLANNING.md) remains a draft with six owner decisions. Existing MuscleMap SVG, body-map coloring code, fatigue `muscle_rows`, band colors, and period reload behavior cover most of the implementation surface. | Resolve §8 decisions, sign the plan, implement a visualization-only slice with no formula/threshold/schema/API change, and close it. | 1–2 d after decisions |
| P2.3 | **Visual-baseline debt: the Windows pair plus stale Linux baselines** | Two real Windows-only failures remain: the animated navbar logo in Workout Plan desktop dark, and `plan-desktop-light-advanced` in `visual-baseline-thumbnails.spec.ts` (**6,084 px** measured / 6,098 retry vs **6,262 px** baseline — [`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) Windows ledger). New on `origin/main` via #273: the **Linux** baselines were last written before 57 later CSS/template commits and now produce at least 11 failures (57 pass, 16 do not run); this is separate from the Windows pair and blocks the signed D3 weekly deep-gate stopgap. [`QUALITY_GATE.md`](ai_workflow/QUALITY_GATE.md) does not yet describe the full platform-specific state. | **OWNER action first:** run the Linux generate workflow, download and inspect all 84 PNGs by eye, commit only approved baselines, then confirm Linux compare is green before adding D3's weekly schedule. Separately stabilize the Windows animation/snapshot timing and diagnose the advanced-thumbnail delta; never blind-rebaseline or raise the global tolerance. Coordinate all of this with any Bootstrap #269 decision because that upgrade changes the same render surface. | 0.5–2 d + owner visual review |
| P2.4 | **Broader KI-005 manual-edit provenance staleness** | KI-005 itself is shipped and Gate-2 approved. Only the explicitly accepted limitation remains: arbitrary manual edits can leave estimate provenance/ancillary text stale. | Treat as a new UX packet only if this is visible or confusing in real use. Do not reopen the completed KI-005 implementation plan for cosmetic comment work. | OWNER / demand-gated |

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
- **Grounding-scan doc set** (`docs/scan/PHASE_02…22`, `SCAN_FINDINGS.md`,
  `SCAN_PROGRESS.md`, `SCAN_RECOMMENDATIONS.md`) and the ~56 `CSS_PHASE4_*`
  evidence files at the `docs/` root: both arcs complete and merged; the scan
  tracker still points at a deleted worktree (`D:/development/HT-scan`). Archive
  candidates under [`DOC_RETENTION.md`](ai_workflow/DOC_RETENTION.md), but the
  6-month criterion is unmet and `QUALITY_GATE.md` links several `CSS_PHASE4_*`
  files directly. Revisit, do not act now.

## 2. Findings that are already done, superseded, or no longer relevant

Do not resurrect these from unchecked boxes or old dated prose.

| Prior activity / stale claim | Current disposition |
|---|---|
| **WPB.4 `Unassigned` weekly-summary bucket is gated/not started** | **SHIPPED** in PR #256 (`9fe5dbd`); Track B closed. The planning doc now carries a SHIPPED / DO-NOT-EXECUTE banner (#265). |
| **Old A12: add JavaScript unit tests** | **DONE.** Vitest, coverage reporting, nine test files, and a non-required CI job exist. Low coverage is a separate future decision. |
| **Old A12: audit known-red E2E** | **DONE.** Generated inventory plus the inherited-red ledgers replaced the manual count. Only the two explicit Windows visual reds remain. |
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

The best short sequence is **preserve the dirty doc patch → fetch/reconcile it
with current `main` (including #270/#272/#273 and #271 if landed) → commit the
orchestration plan + INDEX row + this file together → P1.7 → P1.2 cleanup of
only proven-clean/unprotected targets → P1.1 residue → READY packets P1.4/P1.5**.
Then obtain the OWNER decisions for P1.3/P1.8, P1.6/#269, P2.3's visual-baseline
work, and Fatigue Phase 2 Stage 4. Do not schedule D3 until the Linux compare is
green. This clears the highest-value stale state before any new large proposal.

---

*Last updated: 2026-08-02 (v22 — post-Fable execution-safety revision: live-state
reconciliation, destructive-worktree safeguards, generated-count discipline,
explicit status classification, KI-005 target precision, dependency recount,
and D3/D5 + Linux-baseline updates; checked against `origin/main` @ `f178790`.)*
