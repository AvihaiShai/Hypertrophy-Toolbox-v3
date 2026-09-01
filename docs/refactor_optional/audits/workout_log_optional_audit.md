# Workout Log optional CSS cleanup audit after WP4.3j-d

## Audit boundary and recommendation

This is a planning-only, static/source/history audit. It does not authorize an
implementation packet. No server, browser, Playwright run, visual generation,
workflow dispatch, database operation, screenshot or baseline change, tag, pull
request, push, or GitHub setting was used. The only repository change made by this
audit is this report.

- **Audited HEAD:** `7e1b665d240300dfecaba531e12d874067380a50`
- **Audit date:** 2026-09-01
- **Worktree state at the final audit read:** clean
- **Audit start:** `b36ea9e1a3d7e0e37918e9db4198cb4bf7e0ecf8`
- **Parallel movement during the audit:** `97a79167` landed the separate bounded
  shared-CSS report and `7e1b665` landed the theme-dark/P3 feasibility report. Their
  only changed paths were their two new files under
  `docs/refactor_optional/audits/`; every Workout Log, shared-CSS, contract, harness,
  template, workflow, and visual path examined here was byte-identical across
  `b36ea9e..7e1b665`.
- **Mandatory freshness rule:** all implementation recommendations below expire if
  `HEAD` changes. After any active parallel work merges, rebase a clean worktree,
  re-resolve selectors structurally, re-hash all served cascade inputs, re-run the
  source/contract inventory, and repeat the full current-cascade proof. A clean merge
  with no textual conflict is not revalidation.

Current measured source identity at the audited HEAD:

| Surface | LF-normalized SHA-256 | Git blob | Current shape |
|---|---|---|---|
| `static/css/pages-workout-log.css` | `4d84ac6cecad48e2f16ca2671019b89488bdda2131e4c6b47b362a6f2048cc94` | `ced407378a0b8e2c92b3c082c23da50774f9cbee` | 1,700 lines; 226 style rules; 683 declarations; 242 `!important`; 9 at-rules |
| `static/css/components.css` | `1c420eabfa83cb9839f6e4210abcac4f754a6edee2479046f0ff5f781a2612b5` | `0c79f87633aaf0f56302b5e8392e0c8a657f6d35` | current shared table/frame owners |
| `static/css/theme-dark.css` | `c567fc273b700b215558467bea675e9be53a9c15a64e594b2fa20f2dc6361b3c` | `c2fb6f44dfff69df0af74f6e9ae6ee41c08208d4` | current last-loaded dark owner |

**Post-rebase publication validation (2026-09-01):** the report stack was rebased onto
`origin/main` at `c809d02461c5c7f9a63d9d92b883e54809ae9adb`; the audited HEAD above remains the
measurement provenance. The three LF-normalized hashes and Git blobs in this table still match
exactly. The intervening mainline range did not change Workout Log CSS, its template or product
JavaScript, shared CSS, `theme-dark.css`, `tests/test_css_cascade_contracts.py`, or the cited WP4.4
CSS contracts. It did merge the Linux visual Gate-0 diagnosis and the fail-closed deep-gate
selection repair, so the file-overlap table's active-branch wording is a point-in-time record rather
than current branch status. The Linux proof environment remains unresolved and therefore grants no
new deletion authority. The recommendation remains no broad Workout Log cleanup: only the bounded
empty-shell packet and audit-only recertification are candidates, each still owner-gated.

**Revalidation at `origin/main` `5d3bc95a5251f74d74ff9350a1de11a4131d7999`, 2026-09-02.**
Read-only; no production CSS, contract, harness, workflow, baseline, screenshot, or
canonical status document was touched, and no implementation packet was started. This
discharges the *Mandatory freshness rule* above **for the source/contract half only**; it
is not the runtime cascade proof, and WL-O0 through WL-O5 still require everything in
*Required fresh proof*.

`git diff b36ea9e..5d3bc95` over `static/`, `templates/` and `scripts/` reports **no
changed path**. The three source identities in the table above were re-derived, not copied:

| Re-measured item | Report claim | Value at `5d3bc95` | Result |
|---|---|---|---|
| `pages-workout-log.css` LF SHA-256 / blob | `4d84ac6c…cc94` / `ced40737` | **identical** | matches |
| `components.css` LF SHA-256 / blob | `1c420eab…12b5` / `0c79f876` | **identical** | matches |
| `theme-dark.css` LF SHA-256 / blob | `c567fc27…1b3c` / `c2fb6f44` | **identical** | matches |
| `pages-workout-log.css` PostCSS shape | 1,700 lines / 226 rules / 683 declarations / 242 `!important` / 9 at-rules | **1,700 / 226 / 683 / 242 / 9** | matches |
| Media queries and their conditions | nine, five of them empty shells | nine at `:459`, `:468`, `:504`, `:509`, `:514`, `:518`, `:541`, `:546`, `:1696`; the five at **`:504`, `:509`, `:514`, `:541`, `:546`** are empty and still carry their `WP4.3j-b-dead` retention comments | matches |
| `REGION_H_SHA256` | `b973c748…2442` | `tests/test_css_cascade_contracts.py:44`, **unchanged** | matches |
| Donor `:is()` group and reduced-motion cell rule | `components.css:3335-3411` and `:4413` | `components.css` byte-identical, so both hold | matches |

**Disposition unchanged.** WL-O1 (five empty shells) remains the only source-empty
candidate and remains owner-gated on **OD-WL1**; WL-O0 remains the only other PROCEED and
is measurement-only.

**The one prerequisite that moved, and did not clear.** *Required fresh proof* and WL-O0's
*Order* both wait on the deep-gate/Linux state settling. It has not settled. Gate 0 merged
as [#475](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/475) (`1e9cb4b`);
[#477](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/477) (`fabdb2f`) merged a
single-use diagnostic workflow that ran once
([`33565764116`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/33565764116));
and the Gate-1 closeout is **open and unmerged as PR #481**. The diagnostic supports the
unsynchronized-source/baseline hypothesis for **one** capture with runner, browser and
committed-baseline inputs held measurably equal, but it names no causal commit, identifies
no mechanism, and generalizes to none of the other 64 failures (the scheduled deep gate was
**65 failed / 17 did not run / 18 passed**). It authorizes no fix and no baseline
regeneration. **The Linux proof environment therefore still grants no deletion authority,
and a red Linux comparison is still not permission to explain a WL diff after the fact.**

**The file-overlap table below is now a point-in-time record.** At `5d3bc95` the only open
pull request in the repository is **#481**; every other prompt/worktree listed there has
merged or is clean, and the `wt/opt-*` audit worktrees hold no uncommitted work. The
single-writer collision rules in *Exact future single-writer collision points* are
unaffected and still bind.

The counts are PostCSS source counts over LF-normalized text. They are not regex
brace counts, and comments are not counted as declarations.

### Disposition

| Decision | Scope |
|---|---|
| **PROCEED, owner-gated** | One very small structural packet removing the five empty responsive shells, after revalidation. This is the only candidate that is source-empty today and does not require a deadness inference. |
| **PROCEED with measurement only** | A fresh current-HEAD cascade audit of regions A-C, the retained responsive declarations, dark editable/badge rules, and late Region I. The audit must not edit production CSS. |
| **DEFER implementation** | Every declaration-level deletion in A-C, responsive rules, Region C hover, dark editable/badge, and Region I until the required controls and real states pass on a post-parallel-merge HEAD. |
| **DECLINE as cleanup** | Region G's two known-live hover filters; Region H's lane system; controls, legend, progression-state, collapse, modal, spinner/edit, column-layout, and route-palette work that is actually redesign or behavior work; any monolithic “finish Workout Log CSS” packet. |

The expected deletion yield beyond the empty shells is unknown at current HEAD. The
historical numbers are hypotheses for a new audit, not a forecast and not authority.

## Sources read and authority order

The audit read `AGENTS.md`, `CLAUDE.md`, `docs/MASTER_HANDOVER.md`,
`docs/REFACTOR_PLAN.md`, `docs/ai_workflow/PARALLEL_WORKFLOW.md`, the frontend,
testing, verification, and workstream-ownership rules, and the following directly
relevant evidence:

- `docs/CSS_PHASE4_WP4_3J_A_EVIDENCE.md`
- `docs/CSS_PHASE4_WP4_3J_B_EVIDENCE.md`
- `docs/CSS_PHASE4_WP4_3J_B_DEAD_EVIDENCE.md`
- `docs/CSS_PHASE4_WP4_3J_C_AUDIT_EVIDENCE.md`
- `docs/CSS_PHASE4_WP4_3J_C_DEAD_EVIDENCE.md`
- `docs/CSS_PHASE4_WP4_3J_D_HOVER_PAINT_EVIDENCE.md`
- `docs/CSS_PHASE4_WP4_4_N4_INVENTORY_A_IS_FAMILY.md`
- `docs/CSS_PHASE4_WP4_4_N4_INVENTORY_B_REGIONS_ABC.md`
- `docs/CSS_PHASE4_WP4_4_H_COMPONENTS_DEAD_EVIDENCE.md`
- `docs/CSS_PHASE4_WP4_4_I_IS_REPAIR_EVIDENCE.md`
- `docs/CSS_PHASE4_WP4_4_J_THEME_DARK_EVIDENCE.md`
- `docs/css_phase4_wp4_4/PLANNING.md`
- `docs/css_phase4_wp4_4/N4_CONTINUATION_AUTHORITY.md`
- `docs/css_phase4_wp4_4/EXECUTION_HANDOFF_I_K.md`

Current source and executable contracts outrank dated prose. Historical evidence is
usable for method, old source identity, and risk discovery; it is not a substitute for
measurement against the hashes above.

## Exact remaining inventory

The table below partitions every current declaration in
`pages-workout-log.css`. Line numbers identify the audited HEAD only; a future packet
must use normalized selector list plus source offset and enclosing at-rule, not line
number or occurrence index.

| Current lines | Region/family | Rules | Declarations | `!important` | Current disposition |
|---:|---|---:|---:|---:|---|
| 1-251 | page/frame/table foundation, routine cells, route dark palette, 17-column geometry | 45 | 112 | 31 | Unclassified as cleanup; layout/redesign-sized |
| 252-285 | **A** base header | 1 | 20 | 10 | Retained; old classifications need fresh proof |
| 286-306 | **B** dark header | 1 | 7 | 6 | Retained; old classifications need fresh proof |
| 307-349 | **C** base/even/hover cells | 3 | 18 | 10 | Retained; hover rule is interaction-state scope |
| 350-457 | text wrapping, exercise media/video, delete button, badge, early row filters | 11 | 43 | 11 | Unclassified; media/action/interaction behavior |
| 458-548 | responsive retained families and five empty shells | 10 | 22 | 7 | Explicitly withheld by j-b-dead; audit separately |
| 549-675 | editable/date/native-number inputs and dark table text | 18 | 58 | 7 | Unclassified interaction/form scope |
| 676-807 | controls frame/import furniture | 18 | 61 | 8 | Shared-frame overlap; redesign/interaction scope |
| 808-919 | progression legend | 16 | 53 | 6 | Unclassified; visual/semantic scope |
| 920-1042 | scored/progression states, row highlights, pseudo overlays | 21 | 46 | 14 | Real JS/data state required |
| 1043-1095 | collapse rest/hover/focus/collapsed states | 8 | 28 | 11 | Interaction-state scope; changed after WP4.4 |
| 1096-1155 | clear-log modal | 12 | 19 | 10 | Real open/focus/backdrop state required |
| 1156-1177 | retained dark editable-input and badge neighbors | 2 | 4 | 3 | Explicitly protected; never classified by j-c |
| 1178-1211 | **G** light/dark filter-only hover owners | 2 | 2 | 0 | Known live; decline deletion |
| 1212-1493 | **H** metric-lane variables and ID-level table-calm paint | 33 | 101 | 61 | Live product paint; redesign, not dead-CSS cleanup |
| 1494-1608 | custom spinner/edit interactions | 16 | 49 | 42 | Real hover/active/editing state required |
| 1609-1700 | **I** late frame/table/legend generation and late 1200px query | 9 | 40 | 5 | Old classification obsolete; audit or redesign |
| **Total** | | **226** | **683** | **242** | Complete partition |

This partition is deliberately broader than the old A-I audit. Everything outside the
old regions remains **unclassified**, not implicitly live and not implicitly dead. A
selector being duplicated, visually old, or heavy in `!important` is not a removal
verdict.

### Exact responsive residue from WP4.3j-b

Twenty-three declarations remain across nine media queries: 22 in the early
responsive band at lines 458-548, one in the late legend query, and five of the nine
queries are empty shells.

| Condition | Selector/family | Declarations | Status |
|---|---|---:|---|
| `max-width: 992px` | `.workout-log-table` | `display:block`, `overflow-x:auto`, momentum scrolling | Explicitly unclassified and contract-protected |
| `max-width: 1280px` | `.workout-log-page` | zero padding | Explicitly unclassified and protected |
| `max-width: 1280px` | delete buttons/icons | 5 size declarations + icon font size | Explicitly unclassified and protected |
| `max-width: 1280px` | routine cell and three text roles | 2 widths + 2 type-size declarations covering three roles | Explicitly unclassified and protected |
| `1281px-1366px` | empty shell | 0 | Bounded structural candidate |
| `1367px-1536px` | empty shell | 0 | Bounded structural candidate |
| `1537px-1600px` | empty shell | 0 | Bounded structural candidate |
| `1601px-1920px` | page and delete controls | 2 page paddings + 5 button sizes + icon font size | Explicitly unclassified and protected |
| `1921px-2560px` | empty shell | 0 | Bounded structural candidate |
| `min-width: 2561px` | empty shell | 0 | Bounded structural candidate |
| separate `max-width: 1200px`, lines 1696-1699 | `.legend-item` | `min-width:180px` | Explicitly unclassified and protected |

The five shells have no nested rule or declaration. Their deletion still requires an
owner decision because current contracts affirmatively require them and the source
comments record their retention.

## Regions A-C reconstructed

### Current authored shape

The structural identity established by WP4.4 Inventory B still resolves uniquely:

| Region | Complete rule shape | Arms | Authored declarations | Current properties |
|---|---|---:|---:|---|
| A | five-arm base `thead th` rule | 5 | 20 | `position`, `top`, `background`, `background-color`, `z-index`, `padding`, both borders, type, alignment, sizing, color, weight and shadows |
| B | five-arm dark `thead th` rule | 5 | 7 | `background`, `background-color`, `color`, both borders, `box-shadow`, `text-shadow` |
| C1 | five-arm base `td` rule | 5 | 14 | padding/alignment/border/type/overflow/background/color/transition/shadow |
| C2 | three-arm even-row rule | 3 | 1 | `background` |
| C3 | three-arm hover rule | 3 | 3 | `background`, `box-shadow`, `filter` |
| **A+B+C** | five rules | **21** | **45** | 26 `!important` |

All 21 arms remain ID-free, with the historical specificity range
`(0,1,1)`-`(0,4,2)`. There is no current byte lock over A-C as a unit. Region A's
`text-transform:none !important` and Region C's three-declaration hover shape are
individually protected by the j-c/j-d contract.

### Historical status, kept with its denominator

The WP4.3j-c ownership audit used expanded property records rather than Inventory B's
45 authored declarations:

| Region | Old property-record total | Cascade-dead | Live | Mixed | Unverified |
|---|---:|---:|---:|---:|---:|
| A | 28 | 17 | 6 | 4 | 1 |
| B | 12 | 10 | 2 | 0 | 0 |
| C | 28 | 24 | 2 | 2 | 0 |

The one A unverified record was `text-transform`. Complementary header
`border-top-width`/`border-top-style` records won while the shared owner forced the color
transparent; removing the border width would change layout by 1px even if it painted no
color. They are redesign/layout candidates, not bounded dead declarations.

WP4.4 Inventory B then measured the 45 authored declarations across 12
light/dark × 375/768/1440 × rest/hover contexts:

| Region | Always wins | Mixed | Never wins |
|---|---:|---:|---:|
| A (20) | 7 | 3 | 10 |
| B (7) | 0 | 1 | 6 |
| C (18) | 2 | 2 | 14 |
| **Total** | **9** | **6** | **30** |

Of those 45, 16 lost only to the shared `components.css` donor family and 13
more lost partly to it. The direct-risk properties were A `padding`, `font-size`,
`letter-spacing`, `font-weight`, `box-shadow`, `text-shadow`; B `border-top`,
`box-shadow`, `text-shadow`; and C `padding`, `border-bottom`, `font-size`, `color`,
`transition`, and two `box-shadow` declarations. The partial cohort was the A/B/C
background, background-color, color, border-bottom, even-row and hover paint.

These numbers explain the risk but do not certify a deletion at audited HEAD.

### What WP4.4 did to ownership

WP4.4-i split only `.progression-plan-container` out of the shared selector. It retained:

```css
:is(#workout[data-page="workout-plan"], .workout-log-page,
    .summary-frame.frame-calm-glass)
```

on the twelve table rules at current `components.css:3335-3411`, and retained
`:is(#workout[data-page="workout-plan"], .workout-log-page)` on the reduced-motion
cell rule at current line 4413. The ID donor therefore remains in the matching Workout
Log group and its specificity is bit-identical to the pre-i group. The repaired G3 run
reported 0 A-C resurrections and 0 ownership drift over 56,304 records.

That finding is valid for WP4.4-i's two measured revisions only. It does not make the
old A-C result permanently reusable.

WP4.4-h changed other shared frame/collapsible ownership by removing 101 certified
non-winners from `components.css`, including 91 declarations in the nested shared frame
generation. It excluded every declaration in the donor table family, Region H,
interaction states, pseudo-elements, custom properties, and JS-applied `.value-changed`
states. This makes h strong evidence for what h deleted, but it also means old Region I,
controls, collapse, and frame-neighbor conclusions must be resolved against the
post-h shared generation rather than inferred from pre-h line references.

WP4.4-j left the current last-loaded
`:where([data-theme="dark"] .workout-log-frame)` owner in `theme-dark.css:88`; its
25-declaration deletion did not remove that selector. Region I therefore still has a
late dark competitor, but its current per-property result is not known without a fresh
walk.

Finally, commit `e9eff89a1344f87668b733bef272879d9e95c040` (#464) materially
changed the cascade after all WP4.3j and WP4.4 evidence:

- it edited `pages-workout-log.css`, `components.css`, `layout.css`, `tokens.css`, and
  `theme-dark.css`;
- it changed shared dark table values while retaining the donor selector shape;
- it changed the dark Region G filter from `saturate(1.05) brightness(1.03)` to
  `saturate(0.96) brightness(1.02)`;
- it revised Region H's variables and paint and added page-scoped dark frame and
  pseudo-element overrides in Region I;
- it changed the page's `!important` count from 213 to 242; and
- it regenerated the approved Win32 visual baselines, including all six Workout Log
  full-page captures. Linux baseline work remained a separate deep-gate concern.

The selector text of A-C did not change in that commit, but their competitors, inherited
values, dark tokens, route paint, and evidence hashes did. That is enough to require a
new cascade measurement.

## Retained old regions D-I

| Region | State after j-d | Current decision |
|---|---|---|
| D | Entire 16-record dark-cell family deleted by j-c-dead | Closed. Absence contract-protected. Do not recreate. |
| E | Entire 70-record positional metric-lane family deleted by j-c-dead | Closed. Absence contract-protected. Do not recreate or use old line spans. |
| F | Eight dark visibility rules deleted; adjacent editable-input/badge rules retained | Deleted portion closed. The two retained neighboring rules are a new audit scope. |
| G | Six non-hover rules deleted; four hover paint declarations deleted by j-d; two filter declarations retained because they won | Decline further cleanup of the two filters unless a behavior redesign is commissioned. Region C's separate hover rule is not G and remains protected. |
| H | Retained as the ID-level lane implementation | Live/redesign scope. Current block is 33 rules, 101 declarations, 61 important declarations and a contract-locked 282-newline span. |
| I | Historically 21 property records: 5 dead, 2 live, 14 mixed | Classification obsolete after h/j/#464. Current late source band is 9 rules/40 declarations and includes new dark frame overrides plus the late legend query. |

The old Region H `background-clip` finding also cannot authorize a deletion. Those
declarations were complementary to a background owned elsewhere and the block was
subsequently rethemed. The eight old H unverified dark planned/scored header records and
the A `text-transform` record remain structurally represented, but “still present” is not
the same as “freshly verified.”

## Current contract protections

| Contract/premise | What it protects | Consequence for a future packet |
|---|---|---|
| `test_workout_log_drops_inert_responsive_table_and_frame_families` | deleted ladders stay absent; shared padding/font owner survives; 992 rule, page/delete/routine families, late legend query, and five empty shells survive; 242 important count | Shell or responsive work must amend the affirmative survival assertions deliberately and re-pin weight only for an explained removal. |
| `test_workout_log_drops_cascade_dead_header_and_cell_glass` | 37 deleted selector arms remain absent; donor group and dark cell owner remain; table keeps `table table-calm`; Region H digest; nine structurally represented unverified records; retained responsive/editable/badge neighbors; 242 important count | A-C/H/F-neighbor/shared-owner edits cannot weaken or delete these premises. A template/JS class change invalidates prior deletion proof. |
| `test_workout_log_hover_rules_own_only_their_live_filters` | both G rules remain filter-only with exact current values; Region C retains all three hover declarations; exactly three saturate filters | Region C hover and G must be separate packets. Any deletion needs a replacement assertion for the intended final shape, not removal of the regression guard. |
| `REGION_H_SHA256 = b973c748...2442` | LF-normalized bytes from the unique Region H anchor to `NUMBER INPUT SPINNERS`, plus 282-newline span | No incidental H edit. A palette/redesign packet must explicitly re-measure and re-pin; a cleanup packet stops. |
| `tests/test_css_wp4_4_i_is_repair_contracts.py` | Workout Log and Summary stay grouped with the ID donor; Progression remains split; reduced-motion asymmetry remains | No optional Workout Log packet may de-weight or regroup the shared family. Such work is a new five-route shared-owner packet. |
| `tests/test_css_wp4_4_components_contracts.py` | donor-group counts/shape and the surviving nested frame generation after h | Page cleanup may read shared ownership but not edit it. A shared edit serializes against every page audit. |
| table markup/runtime premise | `#workout-log-table` retains both `table` and `table-calm`; JS does not remove/toggle them | Any markup or runtime change is an immediate stop and forces remeasurement of all deleted/retained families. |
| route/bundle ownership and 18-bundle cap | `workout_log.html` loads `pages-workout-log.css` at the route injection point | No new bundle or link; keep route ownership in the existing page bundle. |
| current approved visual set | #464 deliberately changed and regenerated Win32 baselines | Cleanup must compare against current baselines and may not update them to absorb drift. |

Contracts are protections, not proof that a retained declaration is live. Conversely, an
old “never wins” result is not permission to weaken a current contract without a new
owner decision and a red-path-proven replacement assertion.

## Obsolete or non-transferable evidence

| Evidence/claim | Why it cannot be reused as implementation proof |
|---|---|
| WP4.3j-a's early statement that Region F colors were live | j-c's stronger ownership audit corrected it; the eight rules were dead and were deleted. |
| j-b/j-c line numbers in 2,180/2,025-line source | Current source is 1,700 lines. Identity must be selector + source offset + at-rule. |
| j-c A-C totals 28/12/28 | They are expanded property-record totals, not the current 20/7/18 authored-declaration denominator. |
| j-c Region I 5 dead / 2 live / 14 mixed | Shared frame declarations changed in h; last-loaded dark ownership was adjudicated in j; #464 added current Region I dark rules. |
| j-c H 81 declarations and old eight unverified literals | Current H contains 101 authored declarations and a different digest/palette after #464. Only its current contract is authoritative. |
| j-d exact dark filter, H hash, and 213 important count | All three were intentionally changed and re-pinned by #464. The method remains useful; the literals do not. |
| Inventory B page SHA `d07e2c07...c8c6`, 1,621 lines | Current page SHA/shape is different. Its 9/6/30 result is a hypothesis until rerun. |
| WP4.4-i post-split `components.css` digest `0702558b...c6f0e5` | Current LF digest is `1c420eab...12b5` after #464. i proves its own diff, not the current cascade. |
| WP4.4-i initial G3 artifact naming | The evidence itself records that the first design was unfalsifiable because it tracked only unchanged page CSS. Current proof must record distinct roots plus on-disk and served page/shared digests. |
| pre-#464 “zero visual change” and old screenshots | #464 intentionally changed the rendered design and regenerated Win32 baselines. Compare only to current approved images; never rebaseline a cleanup. |
| any zero-winner census alone | WP4.4 g/h established that zero ownership nominates a candidate; only a removal oracle with valid controls certifies deletion. |

## Candidate classification

### Bounded deletion candidates

1. **Five empty media shells.** Exact, source-empty, indivisible low-risk packet. Their
   comments and affirmative contract protection make this owner-gated despite the lack of
   cascade effect.
2. **A-C non-interaction declarations certified by a fresh audit.** No current declaration
   is placed in this bucket yet. The old 30 never-winners define the maximum hypothesis,
   not the authorized set. Delete only a freshly certified, structurally enumerated set;
   keep live, mixed, complementary, unverified, transition, and pseudo-state declarations.
3. **Responsive declarations certified by a fresh audit.** Again, current candidate count
   is zero. Each query must be tested inside its own condition and against zoom/scale.
4. **Non-interaction portions of Region I certified against current shared owners.** The
   old five-dead figure is not a candidate count.

### Interaction-state candidates

- Region C's three-declaration hover rule. Historically its paint lost to the shared/H
  owners and its filter lost to G, but all three must be proven under real pointer hover.
- delete-button hover/focus, date-edit hover, collapse hover/focus/collapsed, modal focus
  and backdrop, row hover/status, spinner hover/active/edit-visible, and pseudo overlays.
- G is the known-live control for this cohort, not a deletion candidate.

Any interaction-state packet stops unless its identical-CSS control reaches zero. A
rest-state differential cannot certify these selectors.

### Redesign or behavior candidates, not cleanup

- Region H lane palette/specificity, its custom-property system, and its 61 important
  declarations;
- the transparent 1px header border/layout artifact;
- 17-column `nth-child` width architecture and narrow-screen table behavior;
- route dark palette, controls-frame/legend/modal styling, progression indicators,
  status rows, edit experience, custom spinners, and frame glass;
- `!important` reduction where removing weight changes ownership rather than deleting a
  proven non-winner; and
- any token extraction or shared-selector regrouping.

These require a named visual/product owner, explicit acceptance criteria, and expected
visual change handling. They must not be smuggled into a dead-CSS packet.

### Uncertain/declined candidates

- A `text-transform` and the eight historical H unverified records: retain until observed
  in real mobile horizontal-scroll positions.
- F-neighbor dark editable/badge declarations: retain pending real editing/badge states.
- Region I mixed/frame properties: retain pending fresh current-owner measurement.
- G filters: decline deletion; they are current known-live controls.
- Whole unclassified sections in the 683-declaration partition: decline blanket cleanup.

## Required fresh proof

### 1. Provenance and cascade census

Before implementation, the audit packet must:

1. start from clean, rebased `main` and record exact HEAD, branch, root, dirty state,
   browser build, OS, network/font state, and frozen fixture digest;
2. hash LF-normalized on-disk and browser-served `tokens`, Bootstrap, `base`, `layout`,
   `components`, `navbar`, `a11y`, `pages-workout-log`, `motion`, and `theme-dark` in
   actual load order; served and checkout bytes must match;
3. resolve each candidate by normalized full selector, source offset and enclosing
   at-rule; fail on zero or multiple resolutions;
4. enumerate every matching declaration owner through CSSOM/CDP, implementing
   `:is()`/`:where()`/`:not()`/`:has()`, nesting, shorthands, `@layer`, and important-layer
   inversion; and
5. sweep injected CSS under `e2e/**` as well as production CSS before any shared
   specificity claim.

Use and extend the committed `scripts/css_audit/` tooling. Do not trust the old artifact
directory name, an expected digest override, naive comma splitting, reserialized CSS, or
line-keyed identity.

### 2. Context matrix and real states

At minimum, cover both themes and ordinary 375/768/1440 widths, plus both sides of every
relevant breakpoint:

`991/992/993`, `1199/1200/1201`, `1279/1280/1281`, `1366/1367`,
`1536/1537`, `1600/1601`, `1920/1921`, and `2560/2561` CSS px.

For responsive and geometry claims, repeat under the supported visual-scale states that
change effective density; do not infer “scaled displays” from nominal viewport width.
Each media declaration must have a capture where its query is true.

The seeded DOM must include:

- all 17 columns and enough rows for odd, even, last, and horizontally scrolled targets;
- nonmetric, planned and scored metric cells in each lane;
- success/warning/danger badges and row-status classes;
- normal text, long routine/exercise text, thumbnail, missing-media fallback, video and
  delete controls;
- view-simple/view-advanced table states;
- editable display, real visible input and custom spinner wrapper;
- controls expanded/collapsed, keyboard focus-visible and pointer hover;
- clear-log modal closed/open with backdrop and focus containment; and
- reduced-motion, print, and forced-contrast where a candidate is condition-sensitive.

Use real mouse hover and real keyboard focus. For spinner `:active`, use a held pointer;
for JS/data classes, drive the product path rather than merely adding a class unless a
separate synthetic control is explicitly being validated.

### 3. Oracle validation

Every run needs all of the following:

- **Known-live controls:** Region G's two filters under real hover; a Region H ID-level
  lane background/border; shared table-cell padding/color; and one visible current
  responsive declaration inside its media condition.
- **Known-dead control:** a committed synthetic lower-specificity important declaration
  that matches a real table cell but deliberately loses to the donor family, with CDP
  proving the match and losing owner. It must not be one of the declarations under test.
- **Same-CSS control:** two distinct roots/runs with identical complete served CSS and
  fixture. Require zero owner/computed records and zero pixels in every packet-scoped
  capture. Any non-zero result invalidates the run; it is not a tolerance budget.
- **Sentinel control:** transitions suppressed before apply, read, removal and revert;
  each sentinel must change the computed value, target a visible in-frame element, and
  restore cleanly. Handle `var()` shorthands through shorthand-aware queries.
- **Known-live mutation:** a reproducible, source-pinned mutation that produces a
  non-zero computed and scoped-pixel delta. A differential that has never failed is not
  an oracle.

### 4. Before/after removal proof

The implementation half must be compared with a pristine before half from a different
root. The intended candidate source identities disappear; all other selectors and
declarations remain byte-identical. Require:

- zero unexplained computed-value and declaration-owner changes;
- no formerly losing page-local declaration becomes a winner;
- no winner falls through to a UA or unrelated shared fallback;
- zero scoped pixels in stable table/header/control captures;
- the current full visual and thumbnail matrices reproduce their existing outcomes as a
  backstop, with no snapshot update;
- no accessibility, responsive geometry, table interaction, or dark first-paint
  regression; and
- Stylelint occurrence counts, maximum specificity, duplicate counts, and
  `!important` move only by the exact deleted source set and never increase.

Full-page Workout Log capture remains secondary because animated chrome can contaminate
it. The load-bearing pixel oracle is packet-scoped and stable. A known-red ledger is not
permission to explain a new diff after the fact.

## Proposed future packets

All packets are serial where they touch `pages-workout-log.css` or
`tests/test_css_cascade_contracts.py`. Audit-only readers may run in parallel only when
their evidence and harness paths are disjoint and no server/database is used concurrently.

### WL-O0 — current-cascade recertification (audit only)

- **Own:** `scripts/css_audit/workout_log_optional_inventory.mjs` (new),
  `docs/refactor_optional/evidence/workout_log_optional_current.md` (new), and, only if
  durable test nodes are added,
  `tests/test_css_workout_log_optional_audit_contracts.py` plus
  `docs/test_inventory/TEST_INVENTORY.{md,json}`.
- **Read only:** all served CSS, `templates/workout_log.html`, Workout Log JS, existing
  CSS contracts, visual helpers and E2E specs.
- **Scope:** A-C, responsive retained declarations, F neighbors, G controls, H controls,
  and current I. Produce per-declaration current verdicts; authorize no deletion.
- **Order:** after all currently active optional-audit, deep-gate, test-inventory and
  reconciliation work merges; then rebase and hash again.
- **Gate:** every proof item above; harness red paths before any result is reported.
- **Stop:** any provenance mismatch, non-zero same-CSS control, missing real state,
  selector ambiguity, unexpected shared-owner change, or candidate set that reaches H/G
  or shared CSS.

### WL-O1 — five empty responsive shells

- **Own:** `static/css/pages-workout-log.css`,
  `tests/test_css_cascade_contracts.py`, and
  `docs/refactor_optional/evidence/workout_log_empty_shells.md` (new).
- **Exact change:** delete only the five empty at-rules and their shell-retention
  comments; amend the contract from “shells survive” to exact absence/no-empty-at-rule.
- **Expected movement:** five at-rules removed; zero rules, declarations,
  `!important`, specificity, computed ownership, or pixels changed.
- **Order:** may follow a lightweight HEAD/source revalidation; land before any other
  Workout Log implementation so line/source offsets are refreshed once.
- **Gates:** PostCSS parse; focused cascade contract with adversarial restoration of one
  shell; CSS lint delta; full pytest; Workout Log functional/accessibility specs and
  existing visual matrices as no-update backstops.
- **Rollback:** any non-zero semantic CSS AST movement beyond those empty at-rules, any
  contract weakening, visual/functional red, or any attempt to touch a nonempty query.
- **Stop:** owner declines low-value churn or another packet edits the page/contract first.

### WL-O2 — A-C rest-state deletion, only after WL-O0

- **Own:** `static/css/pages-workout-log.css`,
  `tests/test_css_cascade_contracts.py`,
  `scripts/css_audit/workout_log_optional_inventory.mjs`, and a new bounded evidence file
  under `docs/refactor_optional/evidence/`.
- **Scope:** only WL-O0 declarations proven never to win and removal-neutral in rest
  states. Exclude C hover, transitions, complementary border geometry, all unverified or
  mixed records, G/H, shared CSS, templates and JS.
- **Order:** after WL-O1 and after owner approval of the exact declaration manifest.
- **Gates:** fresh before/after cascade and scoped pixels; 21-arm structural identity;
  donor-group contracts; no resurrection; exact expected important/Stylelint movement;
  full page tests and current visual backstops without rebaseline.
- **Rollback:** any changed owner/computed value/pixel outside the manifest, any new
  winner, any 1px geometry shift, or any shared-owner edit.
- **Stop:** if no declaration passes both ownership and removal or if the set cannot be
  expressed without splitting a shorthand unsafely. A zero-yield audit is acceptable.

### WL-O3 — retained responsive declarations

- **Own for audit:** a new responsive evidence file and the WL-O0 harness only.
- **Own for a separately approved deletion follow-up:**
  `static/css/pages-workout-log.css` and `tests/test_css_cascade_contracts.py`.
- **Scope:** 992 table overflow; 1280 and 1601-1920 page/delete/icon/routine rules; late
  1200 legend rule. Exclude column redesign, shells already handled by WL-O1, and all
  breakpoints not represented in the exact manifest.
- **Order:** after WL-O2 because both write the page bundle; audit may be parallel only if
  it writes disjoint evidence and uses no shared runtime.
- **Gates:** boundary-bracketing matrix, scale states, horizontal-scroll geometry,
  action target size, long text, real icons/media, and zero same-CSS/differential results.
- **Rollback/stop:** any size, wrapping, scroll reachability, touch target, column/header
  alignment, or legend change; any candidate that is merely aesthetically undesirable is
  redesign and stops.

### WL-O4 — Region C hover (interaction packet)

- **Own:** `static/css/pages-workout-log.css`,
  `tests/test_css_cascade_contracts.py`, WL-O0 harness, and a dedicated hover evidence file.
- **Scope:** the one three-arm Region C hover rule only. G's two filter rules are immutable
  known-live controls. H hover lanes, nonmetric cells, planned/scored cells and both themes
  must be measured independently.
- **Order:** after WL-O2; never combine with rest-state deletion.
- **Gate:** real mouse hover; animation/transition stabilization; identical-CSS zero;
  apply/revert sentinels; owner/computed and scoped-pixel removal proof.
- **Rollback/stop:** any same-CSS drift, any G filter failure, any hover cell whose owner
  or pixels change, or inability to reach horizontally scrolled mobile targets.

### WL-O5 — F neighbors and Region I

- **Own for audit:** WL-O0 harness plus a new frame/edit evidence file.
- **Own for a later page-only deletion:** `static/css/pages-workout-log.css` and
  `tests/test_css_cascade_contracts.py`.
- **Read only:** `components.css`, `theme-dark.css`, `layout.css`, `tokens.css` and their
  WP4.4 contracts.
- **Scope:** two dark editable/badge rules and current late Region I, split into rest and
  interaction cohorts. The late legend query remains in WL-O3.
- **Order:** last cleanup audit, after A-C/responsive/hover stabilize.
- **Gates:** light/dark frame ownership, pseudo-element, real frame hover, editing and
  badge states, current theme tokens, shared nested generation, and #464-approved visuals.
- **Rollback/stop:** if the safe fix requires editing any shared CSS, token, product
  design, baseline, template or JS. Open a separately approved redesign/shared packet
  instead.

### No cleanup packets for G, H, or the remaining unclassified sections

Region G and H have current product ownership. The remaining foundation, controls,
legend, progression, collapse, modal, spinner and layout families are too behavior- or
design-coupled for a dead-CSS packet. A future redesign must be commissioned independently
and name its visible outcome, accessibility obligations, product owner, token/document
updates, and baseline review. This audit declines to invent such authorization.

## File-overlap map

Static worktree registration cannot prove that a human/agent process is still running.
The table therefore records observable prompt/worktree scopes at audit time and treats
them conservatively as active until merged or explicitly abandoned.

| Observed prompt/worktree | Current/likely owned paths | Overlap with this audit or future packets | Decision |
|---|---|---|---|
| bounded shared-CSS audit, `wt/opt-bounded-css-audit` | landed only `docs/refactor_optional/audits/bounded_shared_css_audit.md` as `97a79167` | No file overlap with this report or WL production packets. Its result declines new scale/table-helper deletion work. | Discharged; revalidated relevant paths after merge. |
| theme-dark/P3 feasibility audit | landed only `docs/refactor_optional/audits/theme_dark_and_p3_feasibility.md` as `7e1b665` | No report-path collision. It identifies `theme-dark.css`, `components.css`, tokens, shared audit tooling, visual helpers and Linux evidence as future collision points and likewise requires post-merge revalidation. | Discharged as a report; serialize any WL-O5/shared-oracle follow-up with its proposed work. |
| Workout Plan optional audit, `wt/opt-wp-audit` | expected separate report; may later propose `pages-workout-plan.css`, `components.css`, cascade contracts and visual gates | No report-path collision. Potential future overlap on `components.css`, `tests/test_css_cascade_contracts.py`, CSS audit harnesses, test inventory and visual infrastructure. | Let its report land first; serialize any shared implementation/harness work. |
| this Workout Log prompt, registered `wt/opt-wlog-audit` plus current checkout | this report only | A second writer to the same report path would conflict. | This commit is the single report owner; do not merge a duplicate report blindly. |
| deep-gate robustness/Linux visual Gate 0/1 worktrees | `.github/workflows/deep-gate.yml`, `e2e/visual-helpers.ts`, Linux inherited-red evidence, workflow contracts, visual planning | Future WL visual proof depends on the resulting runner/helper semantics. WL packets must not edit these paths and must not use pre-merge gate behavior as proof. | Defer WL runtime proof until the deep-gate state is reconciled on main. |
| blank/null rep-bound Gate work | export/validation utilities and tests; generated test inventory | No CSS overlap; possible collision only if WL-O0 adds test nodes and regenerates `TEST_INVENTORY`. | Wait before any packet that changes test inventory. |
| JS-unit ledger/cutoff work | `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` and sometimes generated inventory in adjacent reconciliation branches | No CSS/report overlap; possible generated-inventory serialization. | No blocker for this report; serialize inventory writes. |
| Open Work live reconciliation | `docs/OPEN_WORK_EXECUTION_PLAN.md` and status/evidence files | Those paths are prohibited in this audit. Its merge may change which work is considered active and therefore triggers the mandatory HEAD/status revalidation. | Do not overlap; re-read after merge. |

Exact future single-writer collision points are:

| Path | Packets/readers | Rule |
|---|---|---|
| `static/css/pages-workout-log.css` | WL-O1/O2/O3-dead/O4/O5-dead | Strict serial order; rebase and rerun after each. |
| `tests/test_css_cascade_contracts.py` | every implementation packet; possible Workout Plan audit proposal | One writer at a time; preserve unrelated contracts. |
| `scripts/css_audit/workout_log_optional_inventory.mjs` | WL-O0/O2/O4/O5 | One harness owner; measurement runs may not race servers/DBs. |
| `docs/test_inventory/TEST_INVENTORY.{md,json}` | WL-O0 only if tests added; active testing prompts | Serialize after active testing merges. |
| `static/css/components.css`, `layout.css`, `theme-dark.css`, `tokens.css` | read by all WL packets; possible Workout Plan/shared work | Read-only for WL cleanup. Any required edit stops and becomes a new shared packet. |
| `e2e/visual-helpers.ts`, screenshots, workflow files | read/run as gates | Never owned by WL cleanup; no rebaseline or gate relaxation. |

## Owner decisions required

1. **OD-WL1:** Is the five-shell deletion worth a packet despite zero behavioral yield?
   Recommendation: **yes only as a tiny isolated packet**, never bundled with declaration
   cleanup.
2. **OD-WL2:** Fund WL-O0's fresh runtime/cascade measurement after active work settles?
   Recommendation: **yes** if further cleanup is desired; it is the prerequisite to every
   declaration deletion.
3. **OD-WL3:** If WL-O0 finds rest-state non-winners, permit an exact-manifest A-C
   deletion packet? Recommendation: **decide only after seeing the current manifest and
   controls**, not in advance.
4. **OD-WL4:** Fund interaction-state proof for Region C hover? Recommendation:
   **defer** unless WL-O0 suggests meaningful yield; three declarations do not justify an
   unstable oracle.
5. **OD-WL5:** Treat H, frame glass, controls, legend, column geometry, spinners, and
   important reduction as a redesign program? Recommendation: **decline under cleanup**;
   commission separately only with a desired product outcome.
6. **OD-WL6:** If a candidate requires shared selector/token changes, open a new
   cross-route owner packet? Recommendation: **stop and ask**. No decision here transfers
   WP4.4's spent authority.

## Final recommendation

**Do not resume Workout Log cleanup as one arc.** The safe path is:

1. allow active optional-audit, deep-gate, test-inventory and status work to settle;
2. revalidate exact HEAD and hashes;
3. optionally ship only the five empty shells under OD-WL1;
4. if the owner still wants declaration cleanup, run WL-O0 as an audit-only packet;
5. present its exact current candidate manifest for a new owner decision; and
6. execute at most one narrowly scoped, page-only packet at a time, with rollback rather
   than rebaseline on any unexplained difference.

Thus the current recommendation is **PROCEED** only for bounded shell cleanup and fresh
measurement, **DEFER** all declaration deletion pending that proof, and **DECLINE** G/H or
redesign-sized work as “cleanup.”
