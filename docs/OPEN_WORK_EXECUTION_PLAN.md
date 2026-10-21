# Open Work Execution Plan

**Status:** the single actionable queue (Q12, [`project_direction/AGREED_PLAN.md`](project_direction/AGREED_PLAN.md)
§11). Nothing here authorizes a packet, a merge, a setting change or a release.
**Current-state entry point:** [`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) *Current State*.

**Section map.** This file holds §0, §5, §6, §7 and §9. The revision header and §§1–4, 8 and
10–26 moved on 2026-10-20 to
[`archive/2026/open-work/OPEN_WORK_EXECUTION_HISTORY.md`](archive/2026/open-work/OPEN_WORK_EXECUTION_HISTORY.md);
a bare section number from those ranges, here or in another document, refers to that file.

## 0. Current actionable queue — reconciled 2026-10-20 at `b86e9ad7`

**Read this section first.** Readings at `2026-10-20T15:03–15:05Z` verify GitHub `main`
`b86e9ad783d6ba4e7b5835db5aec64a180e915da`. #532, #533 and necessary D3 repair #538
are merged; #531 carries this closeout. As a queue it supersedes the status words in §4, §8 and §15,
which stop at the §24 reading (2026-08-31); §25 and §26 are later dated logs. Where they disagree,
§0 is newer. The current-state entry point is [`MASTER_HANDOVER.md`](MASTER_HANDOVER.md)
*Current State*. Dedicated plans and ledgers keep their detailed authority. Every obligation below
is carried forward unless its row cites closing evidence, and no status word here is an approval.

**Cell refresh, 2026-10-21 at `d98f45d3`.** The following cells were re-read against `main` at
`d98f45d3`:
- #531 and #537
- R2.3 and H-LINUX-UNSYNC-01
- WS3, CI core and the documentation slices
- the workflow-lint residuals, U1-FOLLOWUP-1 and the JS-unit ledger

They now record the merges that settle them: #531, #539, #540, #541–#548 and #545. Every other
cell keeps its `b86e9ad7` reading. No obligation is closed
without cited evidence, and nothing here authorizes a packet, merge or setting.

**Elsewhere:** parked work §5; closed work §6; owner-deferred accessibility exceptions
[`testing_phase2/A11Y_EXCEPTIONS.md`](testing_phase2/A11Y_EXCEPTIONS.md).

### 0.1 Named PR closeout and qualification

The owner delegated decisions and execution for #531–#533 to the consulting team on
2026-10-20. CI PLANNING §16.8 records the three independent advisers and the adopted
decisions. The necessary correction of D3 in #538 is recorded in §16.10; no later packet
is authorized by that repair or by the closeout.

| Item | Landed scope | Record | Next |
|---|---|---|---|
| CI/CD **B2** | #532 merged as `1a5e0e6f`; workflow lint on every PR and main push | CI PLANNING §15.6 | First main push `39428398134` succeeded, 26/26; lint job and both linters executed successfully. C4 promotion remains separate |
| CI/CD **E1 + D3** | #533 merged as `48d6a450`, after rebase and 26/26 fresh-head CI | CI PLANNING §§16.8–16.9 | Manual suite 6/6; Linux compare executed with known failures and no baseline write. First post-split scheduled slot, 2026-10-26, remains pending for each workflow |
| D3 **repair #538** | Merged as `b86e9ad7`; exact literal suite filter, with strengthened existing contract | CI PLANNING §16.10 | Full pytest 5,569 passed / 2 skipped; PR CI 26/26. Corrected automatic suite delivery and recovery observed in 27 s; independent visual issue #537 stayed open until #548's merge closed it (H-LINUX row, §0.2) |
| Documentation **#531** | Handover refresh, single queue, Q9 publication and final CI receipts | This section; AGREED_PLAN §11; CI PLANNING §§15.6, 16.9–16.10 | **Merged** as `71c4cc6d` (2026-10-20), discharging this named merge closeout; it authorizes no next packet |

### 0.2 Owner decisions and owner-only actions

| Item | State at `b86e9ad7` (cells refreshed at `d98f45d3` are dated) | Record |
|---|---|---|
| **R2.3 — Q4/D2** (`JS Unit` required?) | **Owner approval recorded 2026-10-21.** **D2's recorded condition is met (2026-10-21):** #544 merged as `b4a2653c`, and cycle rows 26–75 match GitHub at 50 / 0 / 0 / 0 / 0 exact JS Unit jobs. Q4 approves `JS Unit (Vitest)` in its own change before protection; that rename has **not landed** and is queued for the sole `ci.yml` slot. CI PLANNING's live Q4/D2 cells (§3 CI-D3, §7 C4, §9, §11.5) still read "unsigned" and are left to the CI lane while #549 edits that file. C4 settings activation requires separate owner approval | [Exact ruling](r23_js_unit_promotion/DECISION.md); [`STEP12_JS_UNIT_GATE0.md`](testing_phase3/STEP12_JS_UNIT_GATE0.md) §13.0 |
| **R2.4** (`visual-linux` in the release gate) | **Unsigned.** ADR-007's threshold is unmet. Eight mixed-workflow scheduled failures through 2026-10-19 predate the split; read suite and visual clocks separately from #533 onward. Next slot 2026-10-26 | §15.4 item 5 |
| **R3** (real tag trigger) | **Unproved.** `release.yml` has two `workflow_dispatch` runs and no `push` run; only a real version tag named by the owner can prove it | §15.4 item 6; §4 R3 |
| **H-LINUX-UNSYNC-01** next step | Option A ran as CI/CD E3 (#529, `c7fec052`): one capture, first-parent boundary #463 → #464, no fix. **2026-10-21:** the owner took GATE1 option C on 2026-10-20 and approved the 77 regenerated Linux PNGs on 2026-10-21. #548 merged them as `c2020735`. GitHub closed #537 at the merge, through the PR body's closing keyword; the watch did not close it. Two later `main` compare dispatches, `39601909853` and `39604203934`, succeeded with compare executed and no baseline written. Each, however, needed Playwright retries for byte-gated captures (2 and 1 flaky), and a green reached through retries is not a pass ([`visual_determinism/PLANNING.md`](visual_determinism/PLANNING.md) §8.1). The first scheduled visual compare is 2026-10-26. Further fixes, wider matrices and baseline changes are unauthorized | [`GATE1.md`](deep_gate_linux_visual_failure_20260831/GATE1.md), [`GATE2.md`](deep_gate_linux_visual_failure_20260831/GATE2.md) |
| CI/CD owner actions | Merges outside the named closeout and necessary D3 repair (§16.10), including each dependency PR (Dependabot security updates are off under D-6); settings C1–C5 including C4 promotions; D1 credential/app authorization; any spending; F1/F3 release publication | CI PLANNING §3, §4, §6; §4 Track D1 |
| Project direction WS3–WS5 | **WS3 merged 2026-10-21** as #545 (`d98f45d3`) on a delegated Gate 1 recorded in [`app_factory/PLANNING.md`](app_factory/PLANNING.md) §V19; that file records Gate 2 as not given. WS4 and WS5 remain DRAFT; each needs its own Gate 0, council and Gate 1. Publishing `AGREED_PLAN.md` approves none of them | AGREED_PLAN §6, §11 |
| Operation A remainder | `PREVENTION_COMPLETE` not declared; owner-only list unchanged | [`worktree_cleanup/CLOSEOUT.md`](worktree_cleanup/CLOSEOUT.md) §19.6 |

### 0.3 Sequenced, not started

- **CI/CD core after B2:** B3 → A2 → A3 → G6 → G7, in that order. *(2026-10-21: B3 merged as #539 and
  A2 as #540; A3 is open as draft PR #549, holding the sole `ci.yml` slot. The Q4 rename also needs that
  slot; its order relative to A3/G6/G7 belongs to the CI lane.)* B4 is a non-blocking measurement
  slot after A1; D1 also waits on its credential and freshness gates. F1/F3 are a separate delivery
  milestone. A4, A5, B5, D2, F2, G1–G5 and G8 are deferred (CI PLANNING §4, §5, §7).
- **Project direction, documentation slices** — selected 2026-10-20 in AGREED_PLAN §12. *(Landed
  2026-10-20: this file's split and the LEFTOVERS reconciliation as #541; the `ACTIVE_DEVELOPMENT.md`
  and cross-model orchestration plan splits as #542 and #543.)* Every deferred slice waits on its
  trigger in AGREED_PLAN §12.
- **Everything else in the project-direction record** stays governed by AGREED_PLAN §4, §9.2,
  §11 and §12, each item with its own approval: WS2 (a) and (c)–(f), and WS6 (deferred).

### 0.4 Open obligations

| Obligation | State | Record |
|---|---|---|
| **CI/CD qualification** | Bounded manual healing and corrected automatic completion delivery are recorded. First 2026-10-26 scheduled runs/freshness remain pending per workflow; broader cron/backup behavior is not yet qualified | CI PLANNING §§16.9–16.10 |
| **Workflow-lint residuals** | **Closed by #546 (`28484dda`, 2026-10-21):** packaged-release pip cache and the three Dependabot cooldowns. Its first `main` push, `39601539825`, succeeded (26 jobs succeeded, PR-only `Dependency Review` skipped). Its lint job ran and succeeded there; recording that reading and the packaged-timing comparison in §18.6 is still owed | CI PLANNING §15.5, §18 |
| **U1-FOLLOWUP-1** | **Closeout record, 2026-10-21.** Implementation [#551](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/551) merged by direct named authority as `a12b680fba9503b8578d777ed51dff571f7c44f2`; the exact merged-main [JS job](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39655584237/job/119414814441) and coverage step succeeded on 14 files / 269 cases. Approved filing (a2)+(i) discharges this obligation when this docs/status record merges; its own publication and named merge remain separate. The qualification owner handles the ledger and Q2 next-window rule; no row or T0 is assigned here | [`u1_followup_1_vitest/PLANNING.md`](u1_followup_1_vitest/PLANNING.md#post-merge-receipt-and-closeout-record--2026-10-21); [`volume_failure_feedback/PLANNING.md`](volume_failure_feedback/PLANNING.md) §v2.14; historical [`toast_action_continuity/PLANNING.md`](toast_action_continuity/PLANNING.md) §4.3 |
| **JS-unit ledger debt** | 2026-10-21 reading: the ledger ends at row 122 (#545, `d98f45d`), cutoff `2026-10-21T14:13:09Z`, at 122 / 0 / 0 / 0 / 0 exact JS jobs. Every later `main` merge, including the one landing those rows, owes a row. Write rows only through the §13.0 process, under the exact-job ruling and §6.1's rename annotation. Row 75's reading is settled by the owner's exact-job ruling. Rows 89–122 ran on Vitest 5 | `STEP12_JS_UNIT_GATE0.md` §13.0 |
| **Worktree cleanup holds** | No standing teardown authority: the 2026-10-16/17 directives were scoped to named targets and are spent. Operation E and main reconciliation, `worktree_cleanup_amendment/` and Operations F/G are parked; branches, stashes and `refs/closeout/…` pins are retained; the two `worktree_cleanup/PLANNING.md` lineages are unreconciled and the local copy is not to be staged; reviewer findings M3, M4 and L1 are undispositioned, and items waived in `CLOSEOUT.md` §11 are not passes | `CLOSEOUT.md` §11, §15–§20 |
| **Feature-folder obligations** | Agent roles Phase 6 conditional; KI-005 Stage 4 restoration held; D4 Packet C deferred; FINDING-1 residual reference; backup-confirmation residual risk; release-pipeline R3 and deep-gate entry conditions; visual-determinism ADR-011 residual | Each folder's `PLANNING.md`; [`README.md`](README.md) *Feature folders → Active* |
| **Fatigue Stage-4 handoff** | Earliest archive review 2026-11-20 | §7 |
| **Visual baselines** | Linux or Win32 regeneration needs separate owner authorization; a red is not a mandate | ADR-011; §26.5 |
| **Playwright 1.61.0 → 1.62.1** | Deferred, not dropped. Both `ignore` entries stay until the unblock condition is re-checked against today's baselines; then bump npm and pip in one branch and regenerate both platforms' baselines in the same arc. The bump moves Chromium 148 → 151, so it also needs the visual-baselines owner authorization above | [`P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md`](P1_6_DEPENDENCY_QUEUE_CLOSEOUT.md) §3.4; `.github/dependabot.yml` ignore comment |

### 0.5 Owner-gated items carried from `LEFTOVERS_BY_PRIORITY.md`

Owner-gated remainder of [`LEFTOVERS_BY_PRIORITY.md`](LEFTOVERS_BY_PRIORITY.md) as of 2026-10-20;
none of these is authorized. Its other open-looking rows are closed (§0.6), parked (§5), or owned
elsewhere: the two WP4.0 Windows rendering observations are ADR-011 residuals under
`MASTER_HANDOVER.md` § *Known Windows visual reds*; the Playwright bump is in §0.4; Testing
Strategy Phases 3 and 5, User Profile v2 and Fatigue Phase 3 are in §5.

| Item | Disposition |
|---|---|
| P2.4 — KI-005 manual-edit provenance staleness (accepted limitation) | Owner- and demand-gated; a new UX packet only if visible in real use |
| LEFTOVERS §4 TODOs — `utils/constants.py:19` (`Front-Shoulder`) and `:100–101` (`Mid/Upper Back`), all three markers present at `f3adacf1` | Owner taxonomy decisions; not a rename |
| LEFTOVERS §4a FINDING-1 residuals — the Excel export still shows a fixed failure toast (`static/js/modules/exports.js`), so the server's diagnostic never reaches the screen; site 7 stays unfixed by design | Proposal; a `static/**` packet needs its own gates |
| P3 proposals — app-JS TypeScript checking; widening the inert `d-flex` / `d-inline-block` utilities (pinned by `KNOWN_INERT`; a rendering change that moves 12 visual captures, so it needs its own baseline review); cross-model `$orchestrate`; the CSS/refactor tail (C8 and G4 are in §5; the rest of its list stays in LEFTOVERS §1 P3 as a dated record) | Park, as §5 |
| LEFTOVERS §3 held local artifacts — `artifacts/wp4_4/`, `artifacts/environment-backups/…`, `artifacts/vbl_check/` | Owner housekeeping under the Operation A teardown restrictions. Deleting anything further is a new owner decision with its own path-specific authorization; `data/auto_backup/*.db` snapshots belong to backup rotation and are never cleanup targets |

### 0.6 Closures that correct older sections

| Stale statement | Evidence |
|---|---|
| §4, §8 and §15 show deep-gate selector robustness Gate 1 (#474) in flight | #474 merged with an 18/18 post-merge pipeline (§25) |
| §4, §8 and §15 show H-LINUX-UNSYNC-01 as draft Gate 0 #475; §26.5 leaves options A–D due | #475 merged (§25); the Gate-1 diagnostic was executed and closed out by #481 (`22ee9ade`), which added §26; option A ran as E3, merged as #529 (`c7fec052`, 2026-10-19T19:06:05Z). B–D remain in §0.2 |
| §4, §8 and §15 show #472 and #473 open with MERGE recommendations | Both merged (§25); later Dependabot PRs through #525 merged; #531 is the named closeout PR at this reading |
| LEFTOVERS P3: six E2E specs hard-code `http://127.0.0.1:5000` | No `127.0.0.1:5000` or `localhost:5000` remains under `e2e/` at `f3adacf1`; the last change to those occurrences was #311 (`8b5231ab`) |
| Outside this file: at `f3adacf1`, the CI PLANNING §7 ledger rows for A1 (#530, `f3adacf1`) and E3 (#529) predate their merges, and the B2 / E1 + D3 authority in §0.1 is not yet recorded there | #532 merged those records as `1a5e0e6f`; see §0.1 |
| Earlier B2/E1+D3 status reads in progress or awaiting `run_visual` acknowledgement | #532/#533 merged; the delegated decision accepts input removal and keeps zizmor online while non-required. #538 repaired the suite filter; bounded live recovery is recorded. CI PLANNING §§15.6, 16.8–16.10; remaining qualification is in §0.4 |


## 5. Parked work — do not place in the active queue

| Area | If reopened | Current disposition |
|---|---:|---|
| CSS C8 — 235 declarations crossing the frozen `@layer workout` span | 5–10 days | Park. High cascade risk and no demonstrated user-facing defect. Requires a newly certified packet. |
| G4 — superset dark-tint gap | 1–3 days | Park unless a visible defect or explicit design requirement is supplied. |
| Fatigue Phase 3 | 8–15 days | Product roadmap, not incomplete v1 cleanup. Requires product scope and schema review. |
| User Profile per-exercise ratios | 3–5 days | v2 roadmap. |
| User Profile auto-refresh from logs | 3–5 days | v2 roadmap; needs conflict/source-of-truth rules. |
| Bodyweight-aware weighted lift estimates | 2–4 days | v2 roadmap; calculation semantics require product-risk review. |
| User Profile confidence indicator | 1–2 days | v2 roadmap; define the confidence contract before UI work. |
| Testing Strategy Phase 3 step 11 / Phase 5 proposals | Unknown | Do not execute until separately selected and planned. |

Parking means “not funded now,” not “safe to delete.” If the owner decides these will not be
built, update their source plans to **Not planned** so they stop appearing as ambiguous open
work.

## 6. Closed work — do not reopen from historical references

- Track A bug fixes, including CTE write-lock detection.
- Track B owner decisions, including weight-zero handling, validation bounds, export read-only
  behavior, null-routine aggregation, and the erase-flow backup banner.
- Refactor Phases -1 through 3 and WP4.4 `a–k`.
- The CSS P3 arc beyond `P3-a0`; it was deliberately terminated and retains no authorization.
- Body Composition implementation.
- Plan-volume integration.
- workout.cool integration; further curation is optional content work, not an incomplete
  integration.
- Bootstrap 5.3.8 and Node 24 AI-workflow ownership claims; both are released and no active
  claim remains.

If current code demonstrates a regression in one of these areas, open a new bug packet with new
evidence. Do not reactivate the old implementation plan.

## 7. Documentation retirement actions

- Preserve scan documents as historical evidence, with an explicit notice that they are not
  active backlog.
- Keep the superseded Fatigue Stage-4 handoff until its retention window permits archival;
  based on the recorded May 20 activity, the earliest archive review is 2026-11-20.
- Archive completed execution artifacts only under
  [`ai_workflow/DOC_RETENTION.md`](ai_workflow/DOC_RETENTION.md). Do not delete evidence merely
  to reduce the file count.
- Do not deprecate shipped Body Composition, plan-volume, workout.cool, or AI workflow behavior.
  Retire only stale planning surfaces around them.

## 9. Start checklist for every packet

- [ ] Confirm the item is still open in the latest `MASTER_HANDOVER.md` block, **read on `main`**
      — the block moved with #417 (`5111a7f`).
- [ ] Reproduce or re-measure it against current code.
- [ ] Check `ai_workflow/WORKSTREAM_OWNERSHIP.local.md` for path claims.
- [ ] Use an isolated worktree when the packet may touch the database, dev server, or tests.
- [ ] Route the change through `ai_workflow/QUALITY_GATE.md`.
- [ ] Keep unrelated dirty-worktree changes untouched.
- [ ] Update the owning plan, current handover, and generated inventories only when required.
- [ ] Pass the gates that packet **itself** owes, as recorded in §4 and §8 — **not every packet
      owes both**; U2 owes Gate 1 only. A gate satisfied by a sibling packet does not carry over.
- [ ] Record a closed, parked, or rejected outcome so the item does not remain ambiguously open.
