# Master Handover

*Committed canonical state. Curated manually after each milestone. New Claude instances read this first.*

## Current State

> **2026-10-20T15:05Z — current state, measured against GitHub `main` `b86e9ad7`
> (#538); the merge receipt and local commit object are verified.** Readings below
> were taken 15:03–15:05Z. B2, E1+D3 and the necessary D3 trigger repair are merged;
> #531 carries this closeout. The superseded unmerged #531 draft and earlier blocks
> are retained in
> [`archive/2026/master-handover/CURRENT_STATE_HISTORY.md`](archive/2026/master-handover/CURRENT_STATE_HISTORY.md).
> The maintenance rule for this block is the subsection headed *Maintenance rule*.

**Work queue and owner decisions:** [`OPEN_WORK_EXECUTION_PLAN.md`](OPEN_WORK_EXECUTION_PLAN.md)
§0 is the single actionable queue (Q12, [`project_direction/AGREED_PLAN.md`](project_direction/AGREED_PLAN.md)
§11). Its §0.2 holds every open owner decision and §0.4 every open obligation; this block does not
repeat them. The queue's §4, §8, §15 and §§11–26 remain earlier readings.

### Trunk, CI and live readings

| Reading | Value |
|---|---|
| GitHub `main` | `b86e9ad7` (#538); main push `39444332091` running at this reading. B2 and E1+D3 main pushes succeeded, each 26/26; CI PLANNING §§15.6, 16.9–16.10 |
| Open PRs | Three at the reading: #531 carries this closeout; #535/#536 are new Dependabot PRs outside the named delegation. Re-read live state before acting |
| Live split checks | Suite 6/6; Linux compare 65 failed / 18 passed, no baseline write. Watch closed suite #534; visual #537 remains open. Completion-to-issue observations: visual 24 s, corrected suite 27 s; CI PLANNING §§16.9–16.10 |
| Dependabot alerts | 0 at 15:05Z |
| Branch protection | Re-read this session: 12 required contexts; `strict: false`; `JS Unit (Vitest, non-required)` absent. A1 kept the required name `Run Tests`, now a fan-in job |
| Weekly gates (Mondays 03:17 UTC) | Pre-split: 8 scheduled failures through 2026-10-19; only the visual job failed in the latest two. After #533, read `deep-gate.yml` and `deep-gate-visual.yml` separately at job and compare-step level. First post-split scheduled slot, 2026-10-26, is pending for both |
| `release.yml` | Two `workflow_dispatch` runs only; `push: tags` has never fired, and no GitHub Release exists |
| Pyright baseline | 0 / 0 / 0 with no headroom. A net-new diagnostic fails `Type Check`; the fix is the code, never the baseline |
| Test counts | [`test_inventory/TEST_INVENTORY.md`](test_inventory/TEST_INVENTORY.md) is the single producer |

### Landed since the 09:13Z reading (`e486e3b5`)

Merges #481–#520 are listed in the archived 09:13Z block. Queue §0.6 lists the closures that
contradict older queue sections.

| PR | What |
|---|---|
| #522, #523, #525 | Dependabot version bumps |
| #524 | Button accessible names aligned for the axe 4.14 upgrade |
| #526, #527, #528 | Handover condensed (WS1b); owner approvals distinguished from reviewer passes (WS2(b)); five closed records archived |
| #529 | CI/CD E3: bounded bisect of H-LINUX-UNSYNC-01 ([`GATE2.md`](deep_gate_linux_visual_failure_20260831/GATE2.md)) |
| #530 | CI/CD A1: guard-hook tests split out behind a fail-closed `Run Tests` fan-in |
| #532 | CI/CD B2: workflow lint; first main-push lint job and both linters succeeded (CI PLANNING §15.6) |
| #533 | CI/CD E1+D3: separate Linux visual workflow and deterministic watchdog; rebased-head CI 26/26 before merge (CI PLANNING §16.9) |
| #538 | D3 literal workflow-name filter repaired after live qualification exposed the unescaped plus; full pytest 5,569 passed / 2 skipped, PR CI 26/26, corrected automatic delivery and recovery verified |

### Holds in force

Constraints to know before acting. Decisions and obligations live in queue §0.2 and §0.4.

- **Operation A:** `PREVENTION_COMPLETE` is not declared, and there is no standing teardown
  authority. The owner-only remainder is
  [`worktree_cleanup/CLOSEOUT.md`](worktree_cleanup/CLOSEOUT.md) §19.6; retained refs are in §20.
- **Sequencing.**
  - The [`WORKTREE_CLEANUP_PLAN.md`](ai_workflow/WORKTREE_CLEANUP_PLAN.md) §1.2 order still binds
    Operations B–E: prevention, then open-development closeout, then separately approved cleanup.
  - Under the owner's 2026-10-19 delegation (Q8(a) in
    [`AGREED_PLAN.md`](project_direction/AGREED_PLAN.md) §11; not a Gate 0 or Gate 1 signature),
    isolated application-factory, service-extraction and dependency-group work does not wait for
    `PREVENTION_COMPLETE`; each still needs its own gates. WS4 implementation follows WS3; WS5
    implementation is eligible only after its manifest and applicable gates are approved; §11's
    Q8(a) boundaries apply (a standalone clone with independent Git storage and private
    environments, and a check of live freezes and blocked-recovery states before work).
- **Visual baselines:** regenerating Linux or Win32 baselines requires separate owner
  authorization; a red comparison is not a regeneration mandate; `--update-snapshots` is never
  the resolution of a red.
- **Owner-only actions:** merges outside the named #531–#533 closeout and necessary D3
  repair #538; repository settings, C4 promotion, credentials, spending and release publication.
  Each dependency PR still needs its own merge authority; Dependabot security updates remain
  off under D-6, so alerts need human-opened PRs.

### Dated items

- `braces` / #513: closed 2026-10-18 by #519. The 2026-11-14 waiver expiry no longer applies, and
  the deliberately skipped watcher bump stays skipped.
- Fatigue Stage-4 handoff: earliest archive review 2026-11-20 (queue §7).

### Standing constraints and parked work

- **Decisions:** ADR-003 through ADR-012 in [`DECISIONS.md`](DECISIONS.md) are settled and remain
  in force.
- **CI:**
  - Required check names are fixed. Three required contexts carry a deliberately false
    "(non-required)" suffix: E2E Fatigue Context, E2E Erase Flow and JS Supply Chain.
  - A test-node change regenerates `docs/test_inventory/`.
  - Coverage is non-blocking.
- **Product:**
  - Effective sets are informational only.
  - Calculation paths add `product-risk-reviewer` ([`QUALITY_GATE.md`](ai_workflow/QUALITY_GATE.md)).
- **Parked and closed work:** queue §5 and §6 list them, and queue §0.5 carries the open items of
  [`LEFTOVERS_BY_PRIORITY.md`](LEFTOVERS_BY_PRIORITY.md). Reopening any of them takes a new owner
  decision. This includes:
  - P3 beyond `P3-a0`;
  - R4, which forbids unlinking `theme-dark.css`;
  - Fatigue (see the *Active Workstreams* fatigue row; calibration guardrails in
    [`ACTIVE_DEVELOPMENT.md`](ACTIVE_DEVELOPMENT.md), cited by `scripts/fatigue_stage4_observer.py`);
  - the app.py review.
- **Accessibility:** owner-deferred exceptions live in
  [`testing_phase2/A11Y_EXCEPTIONS.md`](testing_phase2/A11Y_EXCEPTIONS.md), which tests read.

### Preserved obligations in feature folders

- [`agent_roles/`](agent_roles/PLANNING.md): Phase 6 is conditional.
- [`ki005_controls_persistence/`](ki005_controls_persistence/PLANNING.md): Stage 4 restoration held.
- [`testing_d4_invariants/`](testing_d4_invariants/PLANNING.md): Packet C is deferred.
- [`finding1_residual/`](finding1_residual/PLANNING.md): residual behavior needs a current reference.
- [`backup_confirmation_continuity/`](backup_confirmation_continuity/PLANNING.md): residual-risk reconciliation.
- [`release_pipeline/`](release_pipeline/PLANNING.md): R3, deep-gate entry conditions.
- [`deep_gate_linux_visual_failure_20260831/`](deep_gate_linux_visual_failure_20260831/GATE1.md): option C (Linux baseline sync) taken after [`GATE2.md`](deep_gate_linux_visual_failure_20260831/GATE2.md); a compare run on `main` remains.
- [`visual_determinism/`](visual_determinism/PLANNING.md): the ADR-011 residual.
- [`volume_failure_feedback/`](volume_failure_feedback/PLANNING.md): U1-FOLLOWUP-1.
- [`toast_action_continuity/`](toast_action_continuity/PLANNING.md): U1-FOLLOWUP-1's amended condition.
- [`worktree_cleanup/`](worktree_cleanup/PLANNING.md): Operation A ([`CLOSEOUT.md`](worktree_cleanup/CLOSEOUT.md) §19–§20).
- [`ci_cd_expansion/`](ci_cd_expansion/PLANNING.md): Post-split scheduled qualification; later packets remain unstarted.

The full list is [`README.md`](README.md) *Feature folders → Active*.

### Next safe step

The named merge closeout completes when #531 lands after its fresh CI. The next evidence
is the 2026-10-26 scheduled slot, read independently for the suite and visual workflow;
record it through [`ci_cd_expansion/PLANNING.md`](ci_cd_expansion/PLANNING.md) §§16.9–16.10.
`run_visual` removal is accepted and zizmor stays online while non-required (§16.8).
A green suite or a manual dispatch cannot satisfy the scheduled visual threshold.
Issue #537 closes on the first `main` compare run after the Linux baseline sync merges.
Nothing else starts automatically; B3, C4/settings and later packets keep their own authority
and gates.

### Maintenance rule

- Replace this block in place and move the outgoing block to the archive file; never prepend a
  new block.
- `docs/MASTER_HANDOVER.md` is a never-claimed shared path, so coordinate each edit
  ([`WORKSTREAM_OWNERSHIP.md`](ai_workflow/WORKSTREAM_OWNERSHIP.md) rule 4).
- Status and next steps come from this block. The *Next safe step* above is the current one. The
  *Open Decisions*, *Blockers* and *Next Safe Step* sections after this block are historical.
  *Active Workstreams* rows keep their own dates.
- In those retained sections, a reference to an old Current State block or entry ("at the top
  of this file", "this file's 2026-08-29 Current State block", "the top of `## Current State`"
  and similar) now means the archive file. "The block above" or "the block below" inside one of
  those sections still means the neighbouring block there, and references to the two ledger
  headings at the end of this block still resolve here.

### Known Windows visual reds — historical WP4.0 observations inside the accepted terminal residual

[The full ledger is in the archive.](archive/2026/master-handover/CURRENT_STATE_HISTORY.md)

- The two observations are ADR-011 residuals: `BYTE_GATE_EXEMPT`, with no PNG.
- They are bands; they are never rebaselined or gated on an exact pixel count.
- Visual runs use `PW_VISUAL_SEED=1`.
- In the serial thumbnails spec, "N did not run" is collateral.
- The win32 thumbnail corpus is not in CI, so it is re-measured rather than assumed.
- Any future investigation needs a newly named, testable rendering hypothesis and separate
  authorization.

### Known LINUX visual reds — stale baselines after the WP4.4 CSS arc (2026-08-02)

[The full ledger is in the archive.](archive/2026/master-handover/CURRENT_STATE_HISTORY.md)

- Closed 2026-08-04 (#294, #298). The 2026-08-02 measurement was "11 failed, 57 passed, 16 did not
  run"; with a serial suite, 11 is a floor. The unblock sequence is not to be re-run.
- Pixel counts cannot tell CSS-arc drift apart from a real regression. Any regeneration therefore
  needs a human by-eye review of the PNGs, and `maxDiffPixels` stays where it is.
- The 2026-10-19 Linux failure is a separate condition:
  [H-LINUX-UNSYNC-01](deep_gate_linux_visual_failure_20260831/GATE1.md). Under GATE1 option C the
  owner approved regenerated Linux PNGs by eye on 2026-10-21 (generate run `39465642620`).

## Active Workstreams
| Workstream | Status | Next safe step | Docs |
|---|---|---|---|
| Avi Lewis AI workflow refit | complete through Tier 2 + T3.1 | Use [docs/ai_workflow/INDEX.md](ai_workflow/INDEX.md) + this handover as active truth; treat `.claude/SHARED_PLAN.md` as local audit history only | [docs/ai_workflow/INDEX.md](ai_workflow/INDEX.md) |
| Fatigue meter | Phase 1 and Phase-2 Path 1 shipped. **Phase-2 Stage 4 closed 2026-08-13 via #338 (`700b5da`) as no real-use evidence / no threshold change**; observer code and evidence were retained, and Learned Calibration 2D-D remains parked. **The per-muscle body heatmap shipped via #339 (`ea82ef1`)** with the six owner-locked choices and no formula, threshold, schema or API change. | No threshold tuning without the documented real-use bar plus fresh owner approval. Six unranked labels and later Phase-3 ideas remain deferred. **[UPDATED 2026-08-14]** The Linux fatigue baselines are no longer a separate open draft: **#351 merged as `5a03d47`**, regenerating all twelve fatigue captures (six Linux, six win32) and removing the duplicated body-map caveat from `templates/_fatigue_heatmap.html`. **The W20 anchor rows are absent from the live database** — the 21 rows logged 2026-05-20 behind the one real calibration anchor, the week that *agreed* with the engine's `moderate` band, are no longer present, so [calibration-notes.md](fatigue_meter/calibration-notes.md) is the surviving evidence and they are not re-derivable from the DB. An empty `workout_log` is **not** proof the anchor never existed; do not reconstruct those rows. | [docs/fatigue_meter/PHASE2_PLANNING.md](fatigue_meter/PHASE2_PLANNING.md), [docs/fatigue_meter/HEATMAP_PLANNING.md](fatigue_meter/HEATMAP_PLANNING.md), [docs/fatigue_meter/PLANNING.md](fatigue_meter/PLANNING.md) |
| workout.cool integration | **§3 / §3.6 body maps SUPERSEDED 2026-06-13** — the workout-cool *and* react-body-highlighter body art (plan-modal Simple/Advanced + Profile coverage) were retired and unified on a single **MuscleMap (MIT)** figure with no Simple/Advanced toggle; see [docs/muscle_selector_vendor.md](muscle_selector_vendor.md). The §4/§5 **exercise media** features below remain live. §4 + §4.6 + §5 all shipped. §5 curation closed 2026-05-23 at **56 curated rows** (`cf21191` 36 rows + `ff244aa` +20 rows); long-tail rows use the search fallback by design. §3.6 Profile coverage bodymap shipped locally 2026-05-23 (`18ad223`) — lifts the previously "deferred indefinitely" status. §4.6 pixel baselines locked 2026-05-23 via `toHaveScreenshot()` (`b5b8c7a`). Origin refs: §4 squash-merge `8b348a5` (PR #20), post-§4 follow-up `bfd9087` (PR #23), §4.6 visual baseline `631b5f8` (PR #22). | None. All §5 curation, §4.6 pixel baselines, and §3.6 bodymap work has shipped. Worktree disposition for the §4.6 visual-baseline worktree closed 2026-05-23 (`21859a1`); both worktree paths were already absent from disk and the related branch refs deleted — see [LEFTOVERS_BY_PRIORITY.md §6](LEFTOVERS_BY_PRIORITY.md). Reopen the curation only if the owner supplies new vetted YouTube IDs (see YOUTUBE_REFERENCE_VIDEOS.md "Curation Closed"). | [docs/workout_cool_integration/YOUTUBE_REFERENCE_VIDEOS.md](workout_cool_integration/YOUTUBE_REFERENCE_VIDEOS.md), [docs/workout_cool_integration/PLANNING.md](workout_cool_integration/PLANNING.md), [docs/workout_cool_integration/EXECUTION_LOG.md](workout_cool_integration/EXECUTION_LOG.md) |
| Redesign post-P8 triage | ✅ complete — 10 of 11 shipped, #1 deferred by owner choice (keep nav Backup link) | none | local-only `debug/redesign_post_p8_issues_SESSION_STATE.md` (closed; annotated 2026-05-19) |
| phase5_3i_plan | ✅ closed — accepted-as-shipped (owner decision 2026-05-19) | none | local-only `debug/phase5_3i_plan_SESSION_STATE.md` (closed banner added); planning doc shipped `c0da18e` 2026-04-15 and deleted `635fa3e` 2026-04-24; 5A–5H validation gates never ran but `12c90ac` refactors have held 5+ weeks under 1160-test baseline with no regression |
| Body Composition Issue #21 | ✅ **Fully closed 2026-05-23.** Shipped via PR #31 (squash `20b4b24`, 2026-05-20: backend formula module + idempotent migration + 49 first-slice tests; blueprint with 4 endpoints, calculator page with ACE band + Jackson & Pollock + trend SVG + history, JS formula mirror, route bundle, navbar slot, 18 route tests + 4 Playwright specs). Hardened via PR #32 (`94482d7`, 2026-05-21: `captured_at` ISO validation + JS↔Python numeric parity test). Profile-page display hooks shipped locally via `de3e4d0` (2026-05-23: BFP/ACE line + Lean Mass sub-line on insights card, display-only). Visual baselines for the page added via `40d7dd2` (2026-05-23: 6 PNG baselines). | None blocking. Future read-only consumers (e.g. lean-mass-aware cold-start ratios) remain a separate workstream — do not start without owner direction. | [docs/archive/body_composition/development_issues.md](archive/body_composition/development_issues.md) (source of truth, status now Resolved). OPUS_START_PROMPT.md deleted 2026-06-12 (spent kickoff scaffolding) |
| app.py review | ✅ **COMPLETE 2026-08-01 — all five packets merged.** P1 `24a6f68` (#227), P2 `d453010` (#232), P3 `573bb7e` (#235), P4 `16a4e53` (#236), P5 `e71e3859` (#230); plan approval `b0cdaf3` (#226). Behavior changes: 405/413/403 now return their real status with `Allow` preserved instead of 500; the `"404"`-in-message misfire is gone; `clear_trailing` deleted so query strings and POST methods survive; all 33 first-party CSS/JS links carry a `?v={{ app_version }}` from the new `utils/version.py`. Findings were triple-verified before execution and a third-round `internal_error` candidate was tested and **dismissed** (§3c). **The finding surface is exhausted — do not commission another review round and do not reopen this plan as a "next task".** One regression was introduced and fixed in-session (`bd121c9`, #234 — see §7). **P4's gates were discharged *after* its merge, not at merge time (§7a).** PR #236 reported "475 passed, 0 failed"; its own retained `.last-run.json` records `status=failed` with **49** failures, caused by running the visual specs without `PW_VISUAL_SEED=1` (the functional seed cannot match visual baselines), and its packaged smoke never ran. Both were re-run correctly and pass: nonvisual **457/457**, packaged smoke **PASS via real bootloader** (36/36). Two follow-ups merged after the plan closed: `a075b0c` (#258) repaired `real_app_client`'s database isolation, which had resolved to the checkout's own `data/database.db` on a first import; `1619262` (#262) closed the F4 residual and made the packaged smoke a per-PR CI gate. | **None owned by this plan — the app.py review stays COMPLETE with no follow-up of its own.** **[CORRECTED 2026-08-05]** This cell previously asserted that *"a correctly seeded visual run reproduces **exactly the two WP4.0 known reds and nothing else**"*. That was true when written and is **withdrawn** — it is the same stale claim the §"Known Windows visual reds" block at the top of this file corrects, and it must not be read as current truth. The two WP4.0 entries themselves remain valid as historical rendering observations: `workout-plan desktop dark` (875/882, in band) and `plan-desktop-light-advanced` (6,084/6,098 vs a historical 6,262). **[CLOSED AS POLICY RESIDUALS 2026-08-30]** ADR-011 accepts them inside the terminal 81-byte/5-semantic contract; they are no longer open work, and any future investigation requires a newly named, testable rendering hypothesis. Measured against unmodified `main` at `02e73c7`, `e2e/visual.spec.ts` failed **58 of 66** on Windows, reproducibly: a stale corpus, not two localized defects. **[UPDATED 2026-08-10]** That corpus was regenerated by **#309** (`10ba89f`) and the suite reds on **none** of the 66 today, so the "cannot serve as a merge gate" consequence this cell used to state is **withdrawn** and issue #304 is **closed**. Current state and authority: §"Known Windows visual reds" at the top of this file; do not re-derive it in this row. | [docs/APP_PY_REVIEW_PLAN.md](APP_PY_REVIEW_PLAN.md) |
| Product documentation suite | ✅ **SHIPPED 2026-08-13 — three PRs, all merged, all 18/18 green.** **#340** (`53af816`) built the owner-selected subset as `docs/product/`: `README.md` (D0 scaffold + D6 planning pointer), `APP_FLOW.md`, `BACKEND_SCHEMA.md`, `DESIGN_BRIEF.md` — plus `docs/product/**` in the Always-active retention class, the suite indexed from `docs/README.md`, and a back-pointer from each of `.claude/rules/routes.md` / `database.md` / `frontend.md`. **#343** (`d1efc93`) and **#345** (`18c7916`) then corrected drift from #341 and #339, which merged alongside. Gate 0 and Gate 1 were both satisfied: owner decisions are recorded in §8.1, the three-reviewer council in §8.3, and Plan v2 in §8.7. **D1 (PRD) and D3 (TECH_DESIGN) were deliberately not built** — the council was asked whether any requirement of theirs could not live in the four selected documents and found none (§8.5). The plan doc originated 2026-08-01 via PR #219. | **None — do not reopen.** "Finish the six-document suite" is a reopened decision, not leftover work. The suite is descriptive and carries no status by design; on conflict the code wins. Drift is caught by the three rules-file pointers plus the re-verification commands in `docs/product/README.md` — deliberately **not** by a committed parity test, which would be stricter than a document allowed to lag (§8.8, T6). §8.9–§8.10 record two same-day drift corrections as the suite's real maintenance cost. | [docs/PRODUCT_DOCS_PLAN.md](archive/2026/product-docs/PRODUCT_DOCS_PLAN.md) · [docs/product/README.md](product/README.md) |
| Testing strategy review | **Phases 0–1 complete.** ~~Phase-2 truth refresh is partially executed.~~ **[UPDATED 2026-08-15 — Phase 2 is COMPLETE (#366, #372), as the next column already records; this cell contradicted it.]** Packet A shipped as #342 (`1438a14`), repairing nine accessibility assertions that previously could not fail, with no test-node change. The already-shipped real erase-handler work remains retired rather than duplicated. | **[UPDATED 2026-08-14]** **Packet C (per-spec strict console handling) SHIPPED as #362 (`52331bf`)** — `e2e/console-guard.ts` plus three migrated specs, with anti-catch-all allowlist rules enforced at setup. **[UPDATED 2026-08-15]** **Packet D (axe coverage) SHIPPED as #366 (`f627161`)** on the owner's explicit-exception path, and #372 (`385ce52`) recorded **Testing Strategy Phase 2 complete**; residual accessibility debt is X7–X13 and X15, owner-deferred. **[UPDATED 2026-08-20 — X11, X12 and X13 shipped in #393 (`eff4362`); the owner-deferred set is now X7–X10 and X15, plus the newly recorded, deliberately unregistered X16.]** Phases 3 and 5 remain proposals. The D3 weekly compare-only stopgap shipped as #323 (`3b1160b`), and **the first scheduled run executed 2026-08-17 and was green** (run 31993105305); it ran R2-b's file, so the pre-#388 evidence the override forfeited stays forfeited, and 2026-08-24 is simply the next scheduled run; **the release/tag half of Phase 4 shipped as Packet R1, #374 (`5222db2`)**, with Phase 4 still open on §7.3 entry criteria 2 and 3. **[UPDATED 2026-08-23 — "Phases 3 and 5 remain proposals" is now stale for Phase 3.]** **Phase 3 step 12 is in execution and its expansion sequence is COMPLETE on `main`**: Packets **A → B → C → F** all merged — B #406 (`987588a`), C #410 (`9cb6cdc`), F #411 (`2c95bae`) — with **Packet D dropped** (owner ruling Q3) and **the letter E deliberately vacant**. **`js-unit` is still NOT promoted**: the 14-day qualification window is running from **T0 `2026-08-22T17:59:26Z`** to **`2026-09-05T17:59:26Z`**, ledgered at job level in [`testing_phase3/STEP12_JS_UNIT_GATE0.md`](testing_phase3/STEP12_JS_UNIT_GATE0.md) §13.0, and **Q4 / D2 stay unsigned** — a separate owner signature is required even once the window closes. Phase 3 **step 11** and **Phase 5** are unchanged. **[UPDATED 2026-08-29 — this cell's window reading is SPENT. #431 (`288667d`) took the Vitest corpus 231 → 245 on 2026-08-27 and engaged Q2's restart clause, so **T0 `2026-08-22T17:59:26Z` and the mark `2026-09-05T17:59:26Z` no longer exist**; the new T0 is **conditional and undeclared** pending an owner determination, and §13.0 is the only place to read it. The cell's **A → B → C → F** clause is unchanged and is about the Phase-3 step-12 lettered sequence — read it in that sense only, because **Vitest corpus expansions are a different thing and two are still unlanded** (U3b's KI-011 helper coverage and U1-FOLLOWUP-1), which is precisely what the owed owner determination turns on. The Q4 / D2, step-11 and Phase-5 clauses are unchanged. See this file's 2026-08-29 Current State block.]** **[RE-UPDATED 2026-08-29, later the same day — the bracket above is SPENT on two clauses and is annotated rather than rewritten. The owner ruled **#431 the final Vitest expansion packet**, so the T0 is **no longer conditional or undeclared**: **T0 `2026-08-27T23:18:21Z`**, **strict mark `2026-09-10T23:18:21Z`** ([`testing_phase3/STEP12_JS_UNIT_GATE0.md`](testing_phase3/STEP12_JS_UNIT_GATE0.md) §13.0, *OWNER RULING — #431 IS THE FINAL EXPANSION PACKET*). And *"two are still unlanded"* is now **one**: **U1-FOLLOWUP-1** stays OPEN and required, re-anchored to the new mark, while **U3b's KI-011 helper coverage is RETIRED** — `OQ-10` authorized E2E-only coverage and created no Vitest follow-up. **The Q4 / D2 clause still stands: both remain UNSIGNED and `js-unit` remains non-required at 12 required contexts.**]** | [docs/TESTING_STRATEGY_PLANNING.md](TESTING_STRATEGY_PLANNING.md), [docs/testing_phase2/PLANNING.md](testing_phase2/PLANNING.md), [docs/testing_phase3/STEP12_JS_UNIT_GATE0.md](testing_phase3/STEP12_JS_UNIT_GATE0.md) |

## Open Decisions

- **Two of the three WP4.4 closeout proposals are discharged.** P1 merged as
  `d543a4b` (PR #223) and P2 as `4b0670b` (PR #222), both owner-approved.
  **P3 is also discharged, by termination.** Both gates were **signed 2026-08-02**;
  **`P3-a0` shipped** (PR #280, squash `cd93480`); and the owner then **terminated
  the arc at a0** the same day, after a0's nineteen-tool assessment priced `P3-a1`
  at **nine** new tools against the small deletion yield already accepted at Q6.
  **`P3-a1` … `P3-e` carry no residual authorization** — reopening requires a new
  owner decision. **No WP4.4 closeout proposal is open.**
- **The app.py review is CLOSED** (2026-08-01) — all five packets merged, and
  P4's gates were discharged post-merge in §7a. No decision is open on it; see
  [`APP_PY_REVIEW_PLAN.md`](APP_PY_REVIEW_PLAN.md) §7 and §7a. Separately, the
  **two WP4.0 known Windows visual observations are historical accepted residuals** — ledgered in
  §"Known Windows visual reds" at the top of this file. ADR-011 closed them as policy items on
  2026-08-30 under the terminal 81-byte/5-semantic contract; the rendering defect is not declared
  fixed.
- **Discharged 2026-08-13:** the product-documentation suite is shipped through
  #340/#343/#345. D1 (PRD) and D3 (TECH_DESIGN) were deliberately omitted after
  the council found no requirement that needed them; completing a six-document
  set is not leftover work.
- **Testing strategy is partially advanced, not closed.** Phase-2 Packet A
  shipped as #342 and **Packet C (strict console) shipped as #362** (`52331bf`).
  **[UPDATED 2026-08-14 — this bullet previously read "Packets C … and D … remain
  queued".]** **[UPDATED again 2026-08-14 — Packet D (axe) shipped as #366 (`f627161`),
  and Packets E and F closed register rows X1 and X6; Testing Strategy Phase 2 is
  COMPLETE.]** The bullet previously read "Only **Packet D (axe) remains queued**" under the approved Plan v2;
  it had no open PR at the 2026-08-14 reconciliation. D4, D7 and the
  `js-unit` half of D2 remain unsigned (D6 signed 2026-08-14 as retain-informational,
  recorded as ADR-008); Phases 3 and 5 remain proposals.
  **[UPDATED 2026-08-21 — D7 is now SIGNED and `README.md` now carries the recovery section; see `TESTING_STRATEGY_PLANNING.md` §8.1d. D4 is unchanged.]**
  **[UPDATED 2026-08-23 — "Phases 3 and 5 remain proposals" is stale for Phase 3.
  Phase 3 **step 12 is in execution**, and its expansion sequence A → B → C → F is
  **complete on `main`** (#406 `987588a`, #410 `9cb6cdc`, #411 `2c95bae`; D dropped,
  E vacant). **The `js-unit` half of D2 is still unsigned and `js-unit` is still
  non-required** — that clause is unchanged, and the 14-day window running to
  `2026-09-05T17:59:26Z` does not by itself sign it. **D4** is unchanged. Phase 3
  step 11 and Phase 5 are unchanged.]**
  **[UPDATED 2026-08-29 — the `2026-09-05T17:59:26Z` terminus above is **SPENT**: #431
  (`288667d`) moved the Vitest corpus 231 → 245 on 2026-08-27 and restarted the window, and
  the new T0 is **conditional and undeclared** pending an owner determination.
  **RE-UPDATED 2026-08-29, later the same day — the determination is MADE and the T0 is
  DECLARED: `2026-08-27T23:18:21Z`, strict mark `2026-09-10T23:18:21Z`** (§13.0's
  *OWNER RULING — #431 IS THE FINAL EXPANSION PACKET*). The *"conditional and undeclared"*
  clause is spent; everything else in this bracket stands. Everything
  else in the annotation above is unchanged — **the `js-unit` half of D2 is still unsigned,
  `js-unit` is still non-required at 12 required contexts, and D4 is still unsigned.**]**
  **[UPDATED 2026-08-15 — this bullet's tail previously read "Phases 3 and 5 **and the
  release/tag half of Phase 4** remain proposals". Only the "Phases 3 and 5" half is
  still true: the release/tag half **SHIPPED** as Packet R1, #374 (`5222db2`), with
  #375 (`d3c3436`) recording its passing post-merge dry run. Phase 4 itself stays
  **open** — its `push: tags` trigger has never fired and §7.3 entry criteria 2 and 3
  are unmet. The clause survived #376, #377 and #381 because it is split across two
  source lines, so a grep for "release/tag half of Phase 4" never matched it.]**

> **Superseded 2026-08-01.** The note below read *"None blocking"* and described
> a working tree and `origin/main` parity measured on **2026-05-29**. Retained
> for the Body Composition and worktree-disposition history it records; do not
> read its tree/sync claims as current.

- Working tree clean except for `data/database.db` runtime dirt (owner-approved kept dirty; do not commit). Local `main` is fully up to date with `origin/main` (0 commits ahead) after the 2026-05-29 push of `df9b6f9` + `f2cdc23` + handover sync. Body Composition Issue #21 fully closed (PR #31 + PR #32 + 2026-05-23 Profile hooks). Worktree disposition (former LEFTOVERS row #14) closed 2026-05-23 by inspection + branch cleanup (`21859a1`) — both old worktree paths were already absent from disk and the stale branch refs (`test/visual-baseline-thumbnails` local + remote, `redesign/calm-glass-2026` remote) deleted.

## Blockers

- **No blocker is open for WP4.4.** The arc is closed at `k`; there is no next
  packet in it.
- **P1 and P2 are approved and merged** — `d543a4b` (#223) and `4b0670b` (#222).
  Neither gates anything further.
- **No blocker is open for P3 — the arc is terminated.** Both gates were signed
  2026-08-02, `P3-a0` shipped as `cd93480` (PR #280), and the owner terminated the
  arc at a0. **`P3-a1` … `P3-e` are unauthorized**, so there is nothing left for a
  gate to block. Reopening requires a new owner decision, which would re-enter at
  the plan stage. Full record:
  [`css_theme_dark_p3/PLANNING.md`](css_theme_dark_p3/PLANNING.md).
- The Packet-a layer-span work is **deferred, not blocking**: 235 declarations
  remain untouched for a separately certified future packet.

> **Superseded 2026-08-01.** This section previously read *"No owner-decision
> blocker is open for WP4.4 i–k. N4 is approved…"* and pointed at
> [`EXECUTION_HANDOFF_I_K.md`](css_phase4_wp4_4/EXECUTION_HANDOFF_I_K.md) for
> live execution state. Correct while i–k were running; that handoff is now a
> historical restart ledger, not live state.

## Next Safe Step

> **[UPDATED 2026-08-29 — the block below is NO LONGER THE LATEST next-safe-step reading.
> `git rev-list --count 2c95bae..225b7b0` is **38**, so `origin/main` has moved thirty-eight
> commits past the `2c95bae` this block verified against. **Its four numbered next actions are
> ALL discharged or spent:** (1) Q6 shipped as #413 (`b0aa393`); (2) the 2026-08-24 deep gate
> executed and was inspected — this file's 2026-08-24 block records it 7/7 green at job level;
> (3) the ledger obligation stands but its terminus `2026-09-05T17:59:26Z` is **SPENT**, #431
> having restarted the window on 2026-08-27; and (4) *"until then"* refers to that same spent
> mark, though **Q4 and D2 do remain unsigned**. The block also says **KI-010 and KI-011 are
> still open**; both have since shipped — `288667d` (#431) and `5b35966` (#426). **The live
> current status is the 2026-08-30 block at the top of this file**; read that
> one, not the four actions below. **Most of what the block asserts still stands** — the
> A → B → C → F sequence, 12 required contexts with `js-unit` absent, ~~D4 unsigned~~, the
> ~~`scan_export_bounds()` and `rep_range_integrity.py` items open~~, ~~`needs:` and job-level
> `continue-on-error:` unmeasured~~, Phase 4 open, and `push: tags` never fired; what is falsified
> is listed above. Nothing below is edited except this annotation.
>
> **Amended 2026-08-29, later the same day: the `scan_export_bounds()` and
> `rep_range_integrity.py` items are NO LONGER OPEN.** The owner decided **R2.1** — recorded as
> **ADR-010** in [`DECISIONS.md`](DECISIONS.md) — and the follow-through shipped with it:
> `scan_export_bounds()` now reproduces `export_plan_to_workout_log`'s single combined
> `validate_workout_bounds(..., allow_null=True)` call, so a numeric `min > max` row is named
> instead of silently producing no finding, and the module docstring was rewritten to follow the
> ruling. **D4 is no longer unsigned either** — it was signed 2026-08-29 as **ADR-009**
> (`fcc0e59`, [#453](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/453)), which landed
> before this amendment's own base, so the *"D4 unsigned"* entry in the still-stands list above is
> falsified too. **The mutation clause is also spent:** #455 measured it locally, and ADR-012
> closed the `frozen-windows` reusable-caller residual as invalid/non-reachable on 2026-08-30.
> The rest of that list is unaffected.]**

**Current (2026-08-23, latest): Phase 3 step 12's expansion sequence is COMPLETE
on `main` and there is still no automatic next feature packet.** Verified against
`origin/main` at **`2c95bae`** (#411), 18/18 checks green on that commit at job
level, with **zero open PRs**:

- **Packets A → B → C → F are all merged**: A inside the Gate 0 PR #387 (`9e5997a`),
  B as #406 (`987588a`), C as #410 (`9cb6cdc`), F as #411 (`2c95bae`). **Packet D stays DROPPED** (owner ruling Q3,
  closed unstarted) and **the letter E stays deliberately vacant** in step 12.
  Neither is leftover work; do not queue either.
- **The four next actions, each needing its own authorization:**
  1. **Q6 is a separate correction packet** — the stale coverage / jsdom prose in
     `STEP12_JS_UNIT_GATE0.md` §1. It is deliberately **not** folded into any
     status reconciliation.
  2. **Inspect the 2026-08-24 scheduled deep gate after it executes**, at **job**
     level, with `visual-linux` confirmed *executed* rather than skipped — never
     off the overall green. Allow up to an hour of scheduler delay.
  3. **Continue the qualification-window ledger until `2026-09-05T17:59:26Z`**,
     at job level, in
     [`STEP12_JS_UNIT_GATE0.md`](testing_phase3/STEP12_JS_UNIT_GATE0.md) §13.0 —
     extended, never restated, and recording any red, missing, skipped or
     cancelled result. A red resets the window to zero.
  4. **Q4 and D2 remain unsigned until then**, and D2 needs its own separate owner
     signature even after the window closes.
- **`js-unit` is still non-required.** Branch protection carries **12** required
  contexts, re-read live 2026-08-23; `JS Unit (Vitest, non-required)` is absent
  and promoting it would add a **13th**. Neither packet touched a repository
  setting.
- **Unchanged and still open:** **D4** stays unsigned; the `scan_export_bounds()`
  numeric `min > max` behavior decision and the `utils/rep_range_integrity.py`
  docstring correction are both still open and still unauthorized; `needs:` and
  job-level `continue-on-error:` on the deep gate remain **unmeasured**;
  **KI-010** and **KI-011** are still open; Testing Phase 4 stays open; and
  `release.yml`'s `push: tags` trigger has **still never fired**.

**Current (2026-08-21): #402 merged and there is still no automatic next
feature packet.** Verified against `origin/main` at **`1f9c05a`**, 18/18 checks
green on that commit **[UPDATED 2026-08-23 — superseded by the block above;
`origin/main` is now `2c95bae` (#411), twelve commits later, and D7 has since been
signed. Nothing else below is edited]**:

- **#402** (`1f9c05a`) is tests-only. It closed the first of the three packets the
  block below preserved: the **five** unpinned `deep-gate.yml` jobs — `full-e2e`,
  `first-install`, `empty-schema`, `old-db-migration` and `dependency-health` —
  are now barred from carrying **any** job-level `if:` key, each killed by its own
  parametrized arm after all five were measured as false greens beforehand.
  `visual-linux` stays the deliberate exception with its disjunct set pinned;
  `frozen-windows` keeps its prior unconditional protection. No workflow or
  runtime behavior changed; the inventory moved **2740 → 2746** with that contract
  file at **44 → 50**. #401 (`96b3ef2`) is the docs-only reconciliation that wrote
  the block below.
- **Two of those three packets remain open and unauthorized:** the
  `scan_export_bounds()` numeric `min > max` behavior decision, and the related
  `utils/rep_range_integrity.py` docstring correction. Both still need their own
  authorization.
- **Named by #402, unmeasured, not authorized:** `needs:` and a job-level
  `continue-on-error:` are two further shapes that could stop one of the five jobs
  from gating. Neither is a demonstrated false green — each needs its own mutation
  proof and its own packet.
- **Unchanged:** D4 and D7 stay **unsigned**, `README.md` stays untouched, Testing
  Phase 4 stays open, `release.yml`'s `push: tags` trigger has still never fired,
  and the next scheduled deep-gate run is **2026-08-24**.
  **[UPDATED 2026-08-21 — D7 is now SIGNED and `README.md` now carries the recovery section; see `TESTING_STRATEGY_PLANNING.md` §8.1d. D4 is unchanged.]**

**Current (2026-08-20): four PRs merged and there is still no automatic
next feature packet.** Verified against `origin/main` at **`81771d1`**, 18/18
checks green on that commit **[UPDATED 2026-08-21 — superseded by the block
above; `origin/main` is now `1f9c05a`]**:

- **#393** (`eff4362`) closed register rows **X11, X12 and X13**; the
  owner-deferred accessibility set is now **X7–X10 and X15**, and **X16** was
  recorded as documented-but-deliberately-unregistered.
- **#394** (`c208745`) closed the FINDING-1 residual's two user-visible
  problems. `docs/LEFTOVERS_BY_PRIORITY.md` §4a is corrected in this pass.
- **#399** (`280c211`) and **#400** (`81771d1`) are tests-only deep-gate
  contract hardening. Together they closed nine mutation-proven false-green
  shapes — seven in #399, and the two it named and did not reach in #400.
- **Three future packets are deliberately preserved, none authorized here:**
  (1) job-level `if:` protection for the **five** unpinned `deep-gate.yml` jobs
  (`full-e2e`, `first-install`, `empty-schema`, `old-db-migration`,
  `dependency-health`) **[UPDATED 2026-08-21 — item (1) SHIPPED as #402
  (`1f9c05a`); items (2) and (3) are still open and still unauthorized]**;
  (2) the `scan_export_bounds()` numeric `min > max`
  behavior decision; (3) the related `utils/rep_range_integrity.py` docstring
  correction. #393 additionally raised, and did not take, the X16 fix, the X13
  element deletion plus its 12-capture re-baseline, and the missing
  `/workout_log` export button.
- **Unchanged:** D4 and D7 stay **unsigned**, `README.md` stays untouched,
  Testing Phase 4 stays open, `release.yml`'s `push: tags` trigger has still
  never fired, and the next scheduled deep-gate run is **2026-08-24**.
  **[UPDATED 2026-08-21 — D7 is now SIGNED and `README.md` now carries the recovery section; see `TESTING_STRATEGY_PLANNING.md` §8.1d. D4 is unchanged.]**

**Current (2026-08-15): Testing Strategy Phase 2 is COMPLETE, the
release/tag pipeline has SHIPPED, and there is still no automatic next feature
packet.** Verified against `origin/main` at `aec309d`:

- **Testing Phase-2 is closed.** Packet D (axe) shipped as **#366** (`f627161`)
  on the owner's explicit-exception path; **#372** (`385ce52`) recorded the phase
  complete across five status surfaces. No Phase-2 packet remains queued.
  Residual accessibility debt stays **X7–X13 and X15, owner-deferred**, pinned at
  exact axe node counts rather than suppressed. **[UPDATED 2026-08-20 — X11,
  X12 and X13 shipped in #393 (`eff4362`), so the owner-deferred set is now
  X7–X10 and X15; X16 was recorded alongside them as documented but
  deliberately unregistered. The "pinned at exact node counts" half is
  unchanged.]**
- **The release/tag half of Testing Phase 4 shipped** as **#374** (`5222db2`);
  **#375** (`d3c3436`) recorded the passing post-merge dry-run and discharged R-3.
- **Testing Strategy D6 closed** as a reserved informational `schema_version`
  label — **#373** (`bae49ce`), **ADR-008**.
- **#369** (`5a48e89`) pinned the four residual false-green contracts that #334
  recorded and deliberately left out of scope; that residual set is now empty.
- **#370** (`ebe6390`) re-pinned the fatigue observer guardrail pointer in
  `PHASE2_PLANNING.md` §10 after #359 shifted the line it named. Docs-only.
- **#376** (`94f0d8c`) is the reconciliation that wrote the block you are reading.
- **#377** (`aec309d`) corrected two claims #376 left live — the release/tag
  pipeline and Packet D — across the superseding notes and the Active
  Workstreams row. Recorded so this ledger has no hole.
- **Unchanged and still owner-gated:** the first scheduled deep-gate run is
  inspected at job level **[UPDATED 2026-08-16 — this read "only after
  2026-08-17 03:17 UTC"; post-#388 that run is contaminated] [UPDATED 2026-08-17 —
  the cron fired that day, 7/7 green, run 31993105305; next run 2026-08-24]**, with
  `visual-linux` executed rather than skipped and compare mode writing no
  baselines; the heavier `$orchestrate` design and the remaining CSS/refactor
  tails stay gated where their source plans leave them.

> **Superseded 2026-08-15.** The block below said *"Only **Packet D (axe)** is
> still queued … with no open PR at this reconciliation"*. Packet D shipped as
> **#366** (`f627161`); the phase was recorded closed by **#372** (`385ce52`).
> Its #351 and Packet-C statements remain accurate and are retained as the dated
> record.

**Current (2026-08-14): the ten-session pack has no automatic next
feature packet.** Finish only work that already has its own authority:

- **[UPDATED 2026-08-14]** visual-baseline follow-up **#351 has merged**
  (`5a03d47`); it is no longer an open draft and no longer needs holding clear
  of a docs packet. Its regenerated Linux captures are what the 2026-08-17
  deep-gate compare will run against;
- **[UPDATED 2026-08-14]** Testing Phase-2 **Packet C shipped as #362**
  (`52331bf`). Only **Packet D (axe)** is still queued in
  [`testing_phase2/PLANNING.md`](testing_phase2/PLANNING.md), with no open PR at
  this reconciliation;
- the first scheduled deep-gate run must be inspected after
  **2026-08-17 03:17 UTC**, at job level, with `visual-linux` executed rather
  than skipped and compare mode writing no baselines **[UPDATED 2026-08-17 — the cron fired; run 31993105305, 7/7 green]**;
- the heavier `$orchestrate` design and the remaining CSS/refactor tails stay
  gated exactly where their source plans leave them.

The historical WP4.4 next-step record below is closed evidence, not a queue.

> **Superseded 2026-08-14.** The block below was the latest instruction on
> 2026-08-02. Its P3 prohibition remains true, but it no longer describes the
> repository's overall next step after the August integration pack.

**Current (2026-08-02): all three WP4.4 closeout proposals are settled.
P1 and P2 merged; P3 is TERMINATED at `P3-a0`. There is no next P3 packet — do
not dispatch one.**

**The next safe step is no longer P3 adjudication.** The two candidates listed
here were both *outside* this arc, and **both have now shipped** — the Linux
visual-baseline recovery on 2026-08-04 and Q10 on 2026-08-13. **Neither is a
candidate any more; the table below is kept for the dispatch notes inside it, not
as a queue.** This section names no live next step for the WP4.4 arc.

| Candidate | State |
|---|---|
| ~~**The Linux visual-baseline recovery packet**~~ **— DONE 2026-08-04, no longer a candidate.** | Delivered by #294 (`73c5c46`) and #298 (`f8988f9`); the investigation branch #296 was closed without merging. All 84 visual tests execute — the 16 thumbnail tests that had never run on any recorded run now do — and the job runs **100** tests once the new `workout-plan-desktop-contract.spec.ts` is counted. **Do not start this packet.** The dispatch note stays useful for any *future* regeneration: `gh workflow run deep-gate-visual.yml --ref main -f visual_mode=generate`; **the input is mandatory**, since `visual_mode` defaults to `compare` and a bare dispatch generates nothing (E1 removed `run_visual`). |
| ~~**The Q10 blind-spot-register repair**~~ **— DONE 2026-08-13, no longer a candidate.** | Delivered by **#331** (`5dd0b22`), 18/18 green. The register is now **bidirectionally verified** at **22 entries / 52 declarations**; `e2e/visual-helpers.ts` was read, never written, so no snapshot moved. **Do not start this packet.** Two notes stay useful. The `emit_baseline` warning held and still holds — a whole-file regeneration moves `isFamily` and reds `test_is_family_enumeration_is_complete_and_classified`, so patch **only** the `oracleBlindSpots` array (#331 did exactly that, 6 → 22 entries). And the register covers `prepareForScreenshot()` only: `prepareForElementScreenshot()`'s second stylesheet is pinned separately by `measure.element_capture_rules()`. Full detail in the 2026-08-13 entry at the top of `## Current State`. |

**P3 — terminated, and what that forecloses.** `P3-a1` is **not funded**;
`P3-b`, `P3-c`, `P3-d` and `P3-e` are **not authorized**. **Reopening requires a
new owner decision**, and the Gate 0 / Gate 1 sign-off confers no residual
authority over any later packet. The preconditions those packets carried —
#274's ordering, the replacement ledger, the N8 exclusion bucket — are void as
P3 obligations; only the 84-vs-68 baseline consequence survives, reassigned to
the recovery packet above.

**Still deferred and still not to be reopened without a separate owner
decision:** the **235** declarations `h` withheld behind the frozen
`@layer workout` span (C8), the superset dark-tint gap (G4), and unlinking
`theme-dark.css` (R4) — **R4 still stands; P3's termination does not relax it.**

> **Superseded 2026-08-02.** The block below read *"the next safe step is owner
> adjudication of the three closeout proposals"* and carried P3 as *"Planning
> only — Gate 0 and Gate 1 both UNSIGNED."* Both gates were signed on 2026-08-02,
> `P3-a0` was then executed, and the owner terminated the arc at it the same day.
> The table is retained below as the P1/P2 record.

**Historical (2026-08-01): WP4.4 is COMPLETE and the arc is closed at `k`.**
Every packet is merged and the authorized order is fully discharged:

```
a ✔ → c ✔ → b ✔ → e ✔ → d1 ✔ → f1 ✔ → d2 ✔ → f2 ✔ → g ✔ → h ✔ → N4 ✔ → helper ✔ → i ✔ → j ✔ → k ✔
```

**There is no next packet in this arc. Do not dispatch one.** The next safe step
is owner adjudication of the three closeout proposals recorded in
[`CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md`](CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md)
§5:

| Proposal | State |
|---|---|
| **P1** — the Linux inherited-reds ledger under-described reality: its **schema-v1** shape bound the ledger to a single spec file and recorded **10** reds, while its own rules made an unlisted red a rollback trigger | **Owner-approved and merged** via PR #223 (V2 / R3 condition 6 discharged). Schema **v2** covers **11** reds across two spec files; the 10-red figure is historical schema-v1 text |
| **P2** — no `static/css/**` row in `QUALITY_GATE.md`, so every CSS packet re-infers its gate routing | **Owner-approved and merged** via PR #222 (N10 discharged), with two owner amendments: cascade-contract edits must be *explicitly scoped, justified, and must not weaken an existing guarantee*, and a Targeted-test derivation bullet now routes `static/css/**` to that row instead of the `/verify-suite` fallback — **closing F21 fully** |
| **P3** — `theme-dark.css` is largely inert: `:where()` zeroes its specificity, so a far larger reduction than C11 permitted is likely available | **🛑 TERMINATED at `P3-a0`, owner, 2026-08-02.** Both gates *were* signed that day and `P3-a0` — a read-only audit — executed and is the arc's **only** implemented packet. Its nineteen-tool assessment priced `P3-a1` at **nine** new tools, which the owner ruled does not clear the cost/risk bar against the Q6 yield. **`P3-a1` is not funded; `P3-b` … `P3-e` are not authorized; reopening needs a new owner decision.** **No production CSS was ever touched and R4 still forbids unlinking the file.** Evidence: [`CSS_THEME_DARK_P3_A0_AUDIT_EVIDENCE.md`](CSS_THEME_DARK_P3_A0_AUDIT_EVIDENCE.md) |

~~**The P1-before-P3 precondition is satisfied.**~~ **Moot — no P3 packet will
run.** It was satisfied (`d543a4b` made the ledger schema v2 with 11 reds across
two spec files), and P3-a0 never needed it: a0 dispatched no deep gate and
reconciled the N8 denominator documentarily instead. The one consequence that
outlives this is that **11 is a floor** — see the recovery packet above.

Deferred, and not to be reopened without a separate owner decision: the **235**
declarations `h` withheld behind the frozen `@layer workout` span (C8), the
superset dark-tint gap (G4), and unlinking `theme-dark.css` (R4).

> **Superseded 2026-08-01.** This section previously read *"Packet i is active"*
> and instructed resuming the i worktree from the live handoff. Correct on
> 2026-07-31; stale once #212, #215, #216 and #217 merged. Packet `k` reconciled
> the Current State block at the top of this file but left this section and
> `## Blockers` untouched, so the file asserted both "the arc is closed" and
> "packet i is active" at once — the precise drift class the note at the end of
> this section says `/status` exists to catch.

**`f2` closeout findings later packets must not undo:** layer membership is
frozen (N2), the last `@layer navbar` block survives (G11), and the block still
spans lines 6–883. The pinned `--nav-gap` / `--nav-padding-y` /
`--nav-padding-x`, all 93 `!important` occurrences and all 72 custom-property
declarations remain. The 486-scenario matrix covered collapsed/expanded
navigation, dropdowns, keyboard paths, both themes, required routes, breakpoint
edges, forced interactions, reduced motion, contrast and print. The visual
result 875/882/875 stays inside **875/882 ∪ 1,039/1,046 px**.

**Method additions carried into `g` and `h`:** a CSS-only universal
`transition: none !important` suppressor does not satisfy M6a. `f2` proved this
with a transitioned known-live control and 7 externally settled
`CSSTransition` objects. A broad census verdict is only a nomination; exact
source structure and declaration ownership decide certification. `f2` also
confirmed that matched layered `!important` declarations cannot be dismissed
using normal layer ordering.

> **Superseded 2026-07-30 (latest).** This block previously named `f2` as the
> next action. `f2` merged in PR #205 (`6a5465c`); `g` is now next.

> **Superseded 2026-07-29 (latest).** This block previously read *"`a`, `c`,
> `b`, `e`, `d1` and `f1` are merged — 6 of 11. WP4.4-d2 is the next action"*.
> `d2` merged in PR #201 (`0a912d9`) and `f2` is now next.

> **Superseded 2026-07-29 (latest).** This block previously read *"`a`, `c`,
> `b`, `e` and `d1` are merged — 5 of 11. WP4.4-f1 … is the next action"* and
> gave the band as 1,039 / 1,046 only. `f1` merged in PR #199 (`1127486`) and
> widened the recorded band downward.

**Method now binding on every remaining packet, paid for by `e` and `d1`:**

1. A rest-state differential **cannot falsify an unreachable rule** — deleting
   one changes nothing on any rendered page. Pair it with a runtime
   **full-selector** census taken *before* injecting synthetics, and a synthetic
   control that fails the selector by exactly one compound, reading properties
   **derived from the rule's own declarations**.
2. **Validate the oracle before trusting it** — measure a known-live control on
   the same surface first. `d1`'s compact generation returned census > 0 in
   160/160 contexts; without that, none of its candidate findings would count.
3. **State the post-deletion flip by source identity**, never as "the rule went
   blind" — that is indistinguishable from "the oracle stopped working". Where a
   selector name legitimately survives in a retained rule, attribute the residual
   by declaration owner (CDP `CSS.getMatchedStylesForNode`) to that rule's exact
   source range.
4. **Avoid substring assertions where duplicate selector text can mask a
   deletion** — a defect class hit in **both** `e` and `d1`, so treat it as a
   property of the technique. Use occurrence-count or source-shape assertions.

**Recorded by `d1`, owner-gated, do not act:** `.scale-btn[data-scale]` has
runtime census **0** — `accessibility.js:144` and `:202` query an empty set, a
second dormant JS path beside the accessibility dropdown. The 11 bare
`.scale-btn` rules in `a11y.css` were **never audited as `d1` candidates**,
because the static pass wrongly treated a JS *query* as proof of reachability.
They are retained untouched; deleting them needs its own census and packet.

Workout Log cleanup beyond WP4.3j-d-hover-paint (PR #186) remains closed and
owner-gated. The i–k continuation does not authorize that separate cleanup.

**Deferred by `e`, owner-gated, do not act:** the nine-rule
`.tbl-show-*` / `.tbl-hide-*` breakpoint-helper family in `layout.css`. Census
is 0 and six of nine are oracle-visible, but three declare `display: block` — a
bare div's initial value — so no control element can distinguish them. It is
pinned by exact occurrence count and must be deleted as a **unit** under fresh
evidence, never eroded rule by rule.

> **Supersession note — completed work, do not re-dispatch.** The preceding
> `.scale-btn` and table-helper paragraphs are historical deferral records only.
> PR #300 (`b6550e6`, merged 2026-08-05) later refuted the apparent table-helper
> oracle limitation: the bare `div` probe host caused it, and the packet deleted
> all nine `.tbl-show-*` / `.tbl-hide-*` rules atomically. PR #302 (`9c83777`,
> merged 2026-08-10) independently certified and atomically deleted all eleven
> bare `.scale-btn` rules. Neither family remains deferred, retained, gated, or
> eligible for another deletion packet. This completed work must not be
> re-dispatched.

> **Superseded 2026-07-29 (later).** This section previously read "packets `a`,
> `c` and `b` are merged — 3 of 11 … WP4.4-e is the next action". `e` merged in
> PR #195 (squash `1346a35`).

> **Superseded 2026-07-29.** This section previously read *"WP4.4 packets `a`
> and `c` are merged. `b`, `d1`, `e` and `f1` are eligible and unstarted; they
> need explicit owner direction before dispatch."* `b` merged in PR #192 and the
> owner gave explicit direction for the sequence through `h` on 2026-07-29.
>
> **Superseded 2026-07-28.** This section previously read "no WP4.4 work is
> authorized", which contradicted the Current State block above it and
> contradicted merged history: Gate 1 was approved 2026-07-27 and PR #187 and
> PR #188 both landed. That contradiction is what `/status`
> ([`.claude/commands/status.md`](../.claude/commands/status.md)) exists to
> catch — the same drift previously caused agents to be dispatched at
> already-shipped WP3.5 and WP4.3g work. Reconcile this file, `ACTIVE_DEVELOPMENT.md`
> and `REFACTOR_PLAN.md` together, or not at all.

Use [docs/ACTIVE_DEVELOPMENT.md](ACTIVE_DEVELOPMENT.md) as the execution source
of truth. The older Fatigue Stage-4 and Body Composition material below is
retained as historical verification context, not as the current next action.

**Verification of Body Composition Issue #21 second slice (2026-05-20, later):**

- Original Opus targeted pytest: `.venv/Scripts/python.exe -m pytest tests/test_body_composition_routes.py tests/test_body_fat.py tests/test_db_migration.py -q` → **66 passed in 7.25s** (17 route tests on top of the 49 first-slice tests).
- Startup-touching subset: `.venv/Scripts/python.exe -m pytest tests/test_body_composition_routes.py tests/test_body_fat.py tests/test_db_migration.py tests/test_database_user_profile.py tests/test_harness_isolation.py tests/test_user_profile_routes.py tests/test_program_backup.py -q` → **132 passed in 21.06s**.
- Full pytest: `.venv/Scripts/python.exe -m pytest tests/ -q` → **1371 passed in 173.08s** (17 net new vs. 1354 first-slice baseline; no regressions).
- Opus post-Codex full pytest: `.venv/Scripts/python.exe -m pytest tests/ -q` → **1372 passed in 189.58s** (18 route tests after the profile-demographics contract test; no regressions).
- Playwright targeted: `npx playwright test e2e/body-composition.spec.ts --project=chromium --reporter=line` → **4 passed in 5.4s**.
- Playwright nav sweep: `npx playwright test e2e/body-composition.spec.ts e2e/smoke-navigation.spec.ts e2e/nav-dropdown.spec.ts --project=chromium --reporter=line` → **20 passed in 39.9s**.
- One unrelated flake observed: `e2e/accessibility.spec.ts:283 focus returns after modal closes` (workout-plan `generatePlanModal` close — independent of body composition; passes in isolation).
- Codex review targeted pytest after profile-demographics + navbar fixes: `.venv/Scripts/python.exe -m pytest tests/test_body_composition_routes.py tests/test_body_fat.py tests/test_db_migration.py -q` → **67 passed in 4.76s**.
- Codex review intermediate Playwright checks: `npx playwright test e2e/body-composition.spec.ts e2e/smoke-navigation.spec.ts e2e/nav-dropdown.spec.ts --project=chromium --reporter=line` first exposed a strict-fixture failure after temporarily adding Profile to `nav-dropdown`'s backup-route list (`19 passed, 1 failed in 47.1s`; existing Profile bodymap SVG console error), then passed after narrowing that list back to the primary flow plus `/body_composition` (`20 passed in 42.8s`). `npx playwright test e2e/nav-dropdown.spec.ts --project=chromium --reporter=line` then failed twice while adding the no-clipped-label assertion (`5 passed, 1 failed in 19.7s` for clipped `Body Composition`; `5 passed, 1 failed in 19.0s` after an over-tight primary-pill adjustment), and finally passed after the targeted CSS width fix: **6 passed in 18.7s**.
- Codex review final relevant Playwright sweep: `npx playwright test e2e/body-composition.spec.ts e2e/smoke-navigation.spec.ts e2e/nav-dropdown.spec.ts --project=chromium --reporter=line` → **20 passed in 42.7s**.

The second-slice working-tree change touches: `routes/body_composition.py` (new), `templates/body_composition.html` (new), `static/js/modules/body-composition.js` (new), `static/css/pages-body-composition.css` (new), `tests/test_body_composition_routes.py` (new), `e2e/body-composition.spec.ts` (new), `templates/base.html` (moves Profile into the main left flow and adds the full-label `Body Composition` link between Profile and Distribute), `static/css/navbar.css` (desktop width rule for the longer body-composition nav pill), `static/js/modules/navbar.js` (added pathMap entry), `app.py` (registered blueprint), `tests/conftest.py` (registered blueprint), `e2e/fixtures.ts`, `e2e/smoke-navigation.spec.ts`, `e2e/nav-dropdown.spec.ts` (updated asserted nav order and added no-clipped-label coverage), `.claude/rules/frontend.md` (route-bundle cap/list and nav-flow update), `docs/ACTIVE_DEVELOPMENT.md`, `docs/MASTER_HANDOVER.md` (this update). `data/database.db` is dirty as runtime-only (kept dirty by owner policy). `utils/fatigue.py`, `tests/test_fatigue.py`, and `scripts/fatigue_calibration_report.py` were **not touched**.
