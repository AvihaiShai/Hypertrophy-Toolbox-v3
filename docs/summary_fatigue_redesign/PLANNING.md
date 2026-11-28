# Plan review — #736 Step 4, Weekly Summary, Session Summary and Fatigue

Section 0 and Plan v1 for `feat/736-summary-fatigue`. This branch starts at the verified Navigation merge, `5668cfa3c2d7b6ba1a7c180dd2245e56613b1600`, which is the control for the real-route frame checks and ordinary before/after comparisons. The owner signed Step 4 Gate 0 on November 26. The group council and delegated Gate 1 await review of this version. [Navigation PR #755](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/755)

## Section 0 — Requirements brief

### Raw request

> Work the steps in order, one PR per step or per group of related screens (Weekly and Session Summary go together).

> On all 11 routes at 390, 768 and 1440 px, in both themes, there are no blank icons, no page-level sideways scroll and one left-gutter value per width, and the frame check defined in the pilot's Section 0 passes.

> D2: B. Open on the first routine tab. Keep All available and keep the choice stateless between visits.
> D3: C. Collapse the filters and show each active filter by name as a removable chip.
> For all other questions through D24, I accept the published defaults. This is my Gate 0 reply for steps 3–5. Begin step 3 after #748 merges.

The owner's November 26 reply above is transcribed from the local decision record. The project issue carries the adopted plan and owner decisions. [Issue #736](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/736) · [Local run prompt](../../artifacts/design-736/RUN_PROMPT.md) · [Local owner reply](../../artifacts/design-736/DECISIONS_REPLY.md)

### Problem

On a phone, the Summary pages can replace readable category rows with rows whose values are all hidden. On a tablet, visible volume values can sit under the wrong headings. The selector appears above information it does not control. On Fatigue, the outer white card and large decorated readouts obscure the relationship between the page title, period, planned/logged figures and body map. A user must still be able to trace each number to the same muscle, routine, period, channel and classification after the redesign.

### Decisions in force

| Source | Applies to this group |
|---|---|
| Owner, D13 | Keep the four volume colours and Session warnings as small pills with text. Remove Session’s whole-row warning tint. |
| Owner, D14 | Flatten Fatigue and the shared projected-fatigue badge. Preserve the band colours and body map. Set large readouts to 24 px. By-eye review follows the delegation in the run prompt. |
| Owner, D15 | Summary tables become cards below 768 px and tables from 768 px. Repair both known data-display defects. |
| Owner, D18 | Correct false wording and list each correction in the PR. Keep the three page titles. |
| Council, K27–K36, K39–K41, K47, K51, K55 | Migrate the three routes together after Navigation. Keep Fatigue’s descriptive caveat, put the contribution selector in the volume panel, keep the visible legend, put the definitions and formula in one disclosure, use neutral Pattern Coverage chips, and retain numeric alignment. None of the three pages needs a filled primary action. Build needed shared components in the existing bundle, retain the visual hooks, and remove proven-dead route overrides. |

[Council decision record](../../artifacts/design-736/decisions/COUNCIL_SETTLED.md)

### Candidate mockup and existing evidence

Open the [Weekly mockup](mockup.html?route=weekly&theme=light), [Session mockup](mockup.html?route=session&theme=light), or [Fatigue mockup](mockup.html?route=fatigue&theme=light). The same synthetic content is shown at each width. Use `theme=dark` for the other theme. The shared prototype from `artifacts/design-736/step3/resume-unit/summary-fatigue-mockup.html` supplies all three route bodies and sample data. The promoted version resolves bundled Inter, Font Awesome, design tokens and the MuscleMap figures relative to this document. Its inline copy of the application heatmap renderer and its embedded original SVGs allow the Fatigue preview to work when opened directly from disk. Over HTTP it reads the actual SVG files from the repository. The original prototype evidence directory contains 18 PNGs named `{weekly,session,fatigue}-{390,768,1440}-{light,dark}.png` and `measurements.json`.

| Viewport | Heading left | Sampled panel edges | Document width |
|---:|---:|---:|---:|
| 390 px | 16 px | 16–374 px | 390 px |
| 768 px | 24 px | 24–744 px | 768 px |
| 1440 px | 32 px | 32–1408 px | 1440 px |

These measurements come from the original prototype at all three widths in both themes. The heading measured 24 px in all 18 renders. All six Fatigue renders reached `ready` with two SVGs. The recorded error list is empty. Only one panel per render was measured. Fixed-navbar offset, every panel edge, scale 8, separators, accessibility tree, focus states and production actions require checks on the real application. The `b03ea21` directory identifies the earlier mockup evidence. A browser has yet to verify the relocated mockup; the acceptance checks below apply to the group’s real application control and candidate. [Original prototype](../../artifacts/design-736/step3/resume-unit/summary-fatigue-mockup.html) · [Original measurements and sibling PNGs](../../artifacts/design-736/step4-summaries/mockup-b03ea21/measurements.json)

### Acceptance criteria

1. **Frame.** Given each real route at scale 6, at 390, 768 and 1440 px in both themes, the page header and every outer panel have left and right gutters of 16, 24 and 32 px respectively. The header begins 16 px below the actual navbar on phone and 24 px below it on tablet and desktop. The content cap is 1800 px. C2–C4 enforce the existing radius, typography and surface rules. C5 finds zero page-level horizontal overflow, including at scale 8. C8 finds zero theme-specific `.ui-*` selectors outside tokens. Visible route icons render their glyphs.
2. **Titles and readouts.** Given a Summary or Fatigue page, its visible H1 remains `Plan Volume Summary`, `Session Summary`, or `Fatigue meter`. Projected score and planned/logged SFR readouts are 24 px at default scale. The H1 remains at least as large as any readout. Fatigue’s descriptive-only caveat is visible beside the title or directly beneath it.
3. **Responsive values.** Given populated data, after initial load and after a contribution-mode refresh, both Summary pages show every category, subcategory and exercise count below 768 px. At 767 px each card has visible field labels. At 768 px and 1440 px each visible cell aligns with the matching column heading. Check a real value in **each** of the six volume fields, three category fields and six conditional isolated-muscle fields. Include long routine or muscle names. Numeric cells are right-aligned and tabular, with 14 px values and 12 px headings at default scale.
4. **Contribution and terminology.** Given either Summary, `Muscle Contribution Mode` is visibly and programmatically labelled inside the muscle-volume panel. Its values remain `total` and `direct`, with Total initially selected. A change uses the existing updater and JSON request with `contribution_mode`. The rendered effective/raw values match the response, and independent categories, isolated statistics, pattern coverage and projected fatigue retain their values. The existing navbar naming preference still updates dynamic muscle names and server-rendered isolated names. There is no counting-mode control.
5. **Legend, formula and status.** Given a Summary page, the four labelled class swatches remain visible and match `--bs-danger`, `--bs-orange`, `--bs-success` and `--bs-purple`. One keyboard-operable disclosure exposes raw/effective definitions, contributions, effort and rep-range factors, and the per-exercise volume formula. Session retains both the class and the per-session warning. Records at 10.0 and 11.0 effective sets per session visibly read `Borderline` and `Excessive` respectively. A routine with no logged sessions retains `No Sessions`. The row surface remains neutral for each state.
6. **Truthful wording.** Given the volume, isolated-muscle and fatigue sections, the visible copy distinguishes credited raw sets in the muscle table from unweighted raw sets in the isolated table. The latter’s classifier still reads `muscle.total_sets`. The projected-fatigue explanation describes planned routines and omits the nonexistent counting toggle. Session’s explanatory ranges read below 10, 10 to below 11, and 11 or above. Labels and any touched tooltip ranges must also cover fractional sets. List the wording changes in the PR.
7. **Pattern Coverage.** Given Weekly’s live `/api/pattern_coverage` response, the panel shows named patterns, zero-count core patterns, warning messages with their meaning, per-routine totals and target range. Neutral chips and text preserve the distinctions readers previously obtained from colour. Its loading, empty and failed states are distinguishable. An independent failure leaves other successful sections usable.
8. **Projected fatigue.** Given either Summary, the badge retains the rounded projected score or existing empty mark, text band, applicable period, accessible explanation and working `View per-muscle breakdown` link. Weekly reports the planned week. Session identifies the selected routine or heaviest planned routine where applicable. Changing contribution mode leaves these values intact. The phone info control is reachable by touch and keyboard.
9. **Fatigue readings.** Given the Fatigue page, `Most recent session`, `This week (Mon–Sun)` and `Last 4 weeks` use the existing GET form and `period` values. A missing or invalid period falls back to `this_week`. Planned readings retain their existing period independence. Logged values follow the selected window. Preserve SFR precision, missing-ratio explanations, percentages, unranked muscles, ordering, score formatting, track/reference semantics and accessible meter values.
10. **Body map.** Given Fatigue data, the native body-map disclosure is open above the bar list and collapses from the keyboard. Planned-only and logged-only data show the available channel. With both channels the control changes `aria-pressed`, caption and actual SVG fills together. Preserve the five light/dark band colours, named front/back figures, gray unread regions and mapping caveats. Check original fill/stroke values and representative region assignments against the control. Missing SVG assets leave the fallback and usable bar list. The visual harness still reaches `ready` or `empty`.
11. **Empty and error states.** Given a confirmed wholly empty page, one page-level `ui-empty-state` explains it. Partial availability remains visible, including the Fatigue planned-only case. Loading and request failure do not become “no data.” A genuine summary refresh failure still reports that the data could not load. Keep the existing Plan link from empty Fatigue and the existing `data-testid`, visual and live-update hooks used by callers.
12. **Export.** Given either Summary, the visible and accessible secondary action begins `Export workout data`. It still invokes the existing `exportToExcel()` handler. The full workbook can contain Workout Plan, Workout Log, Weekly Summary, Session Summary, Progression Goals, Categories and Isolated Muscles. The current handler requires `#workout_plan_table_body`, which neither Summary renders, so clicking currently gives the empty-plan toast before a request. Keep the reproduced defect in #754. The prototype’s direct link is illustrative and must not be promoted into production. [Summary export follow-up #754](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/754)
13. **Accessibility.** Given the current exact axe register, target zero migrated findings on Weekly light, Session light, Fatigue dark and the populated Weekly table state; each currently records four contrast nodes. Keep Weekly dark, Session dark and Fatigue light clean. Re-measure on the merged control and final head. The populated structural scan must reach a visible table with at least three data rows and more than three columns. At 375/390 px prove a painted card boundary exists; at 768/1440 px prove a painted row separator exists. Require at least 3:1 against its actual backdrop. Exercise focus, open/close, tooltip disposal on refresh, and the first and last usable controls at 320/360/390 px at scale 8.
14. **Evidence and scope.** Given the verified precursor and implementation, independent manual QA compares ordinary before/after screens to the mockup **before** regeneration. Compare each allowed capture on both native platforms. Any difference on an unlisted capture is investigated as a regression. No new runtime stylesheet, page-level `!important`, general navbar or `.container` restyle is introduced. Update `DESIGN_BRIEF.md` with the rules that ship.

**Calculation surface:** `none`. Existing Python and JS classifications and score inputs are reference oracles. The prototype’s synthetic arithmetic, simplified track fill and sample data do not enter application code.

**In scope:** the three route bodies, shared badge, two existing Summary bundles, Fatigue SCSS and compiled artifacts, opt-in shared components needed by these routes, prompt-approved wording, equivalent or stronger test pins, ordinary evidence, the scoped visual baselines and product documentation.

**Out of scope:** #754’s export fix, a new Summary export, an Effective/Raw toggle, changes to routes’ response shapes, database/schema work, score or threshold adjustments, a Fatigue page bundle, navbar changes, other route redesigns, global motion changes and file deletion.

### Product assumptions for council disposition

| Assumption | What the owner sees | Trade-off | Recommendation |
|---|---|---|---|
| ⚠️ Panel order | Summary header with secondary Export, projected fatigue, muscle-group volume, categories, conditional isolated muscles, and Weekly-only Pattern Coverage. Fatigue has header/period, one SFR panel, open Body map and per-muscle list. | Volume follows the short projected-fatigue panel. | Use the mockup order and verify first-screen content at 390 px. |
| ⚠️ Phone H1 | 24 px titles on these three routes permit 24 px D14 readouts while passing the title-largest rule. | These titles are 4 px larger than the pilot’s phone title. | Adopt an opt-in shared title variant. Leave the global title token intact. |
| ⚠️ Explanations | Definitions and formula sit behind Details. The existing fatigue information control still exposes its explanation on tap/focus. | Some reference copy takes one action to read. The prototype uses a second disclosure for badge information. | Keep the working badge control and its 44 px phone target. Preserve the selector’s visible help and tooltip lifecycle. |
| ⚠️ Tablet panel | All columns remain available from 768 px. Long text wraps and a labelled table region can scroll if needed. | Some tablet records may be taller or need local horizontal movement. | Prefer wrapping. Where local scrolling is necessary, prove keyboard access and last-column reachability. |
| ⚠️ Status palette and border | Pill fills retain their original hues, with readable text. Card/table boundaries may be darker than the prototype hairline. | The 3:1 boundary is more visible. | Prioritise measured contrast and preserve existing swatch-token assertions. |
| ⚠️ Empty state and export | One page-level empty state can coexist with meaningful partial sections. The secondary action describes workout data. | The separately reproduced export defect persists until #754. | Derive whole-page emptiness from loaded data, leave the existing transport alone and document the follow-up. |

**Blocking owner questions:** none. The November 26 reply accepts the published defaults for D13, D14, D15 and D18. The specific panel, copy and geometry proposals above go to the formal group council.

### Section 0 sign-off — Gate 0

- [x] Owner signed Gate 0 for Step 4 in the Decisions reply of 2026-11-26. The four applicable answers appear above with their visible outcomes.
- [x] The owner assigned remaining presentation assumptions to council and Astra on November 27. The six product assumptions above await group council disposition. [Recorded delegation](../navigation_redesign/PLANNING.md#section-0-sign-off--gate-0)
- [x] No blocking owner question remains for this scope.

## Plan v1

**Goal.** Give the three Analyze routes the common frame and fix phone/tablet value-to-label mapping while preserving every displayed measure and its controls.

**Effort:** Large. **Author:** product manager. **Dependency:** Navigation PR #755 merged at `5668cfa3c2d7b6ba1a7c180dd2245e56613b1600`. The original author resumed for formal Section 0 and Plan v1 on `feat/736-summary-fatigue`. See Agent provenance below.

### Implementation and verification paths

| Path | Work |
|---|---|
| `templates/weekly_summary.html`, `templates/session_summary.html`, `templates/partials/_volume_controls.html` | Opt into the frame, restructure panels, move the labelled select, preserve updater names, keep visible legend and table IDs, and correct copy. |
| `static/js/modules/weekly-summary.js`, `static/js/modules/session-summary.js`, `static/js/modules/summary-helpers.js` | Fix live row markup for all fields, especially dynamic categories. Keep API headers, row replacement, tooltip disposal/recreation, naming updates and independent Pattern Coverage rendering. |
| `templates/fatigue.html`, `templates/_fatigue_badge.html`, `templates/_fatigue_heatmap.html`, `templates/_fatigue_muscle_bar.html` | Remove Fatigue’s local use of legacy `.container`, apply the frame and panels, and preserve score/period/meter expressions, figure mounts, status and terminal-state hooks. |
| `static/css/components.css`, `static/css/pages-weekly-summary.css`, `static/css/pages-session-summary.css` | Add opt-in table/card, select, notice or segmented-control styles only where existing components do not meet the contract. Keep page bundles for route layout. Preserve the 1360 px Plan/Log table rules and the live shared Calm Glass selector family used by Progression. |
| `scss/_fatigue.scss`, `static/css/bootstrap.custom.min.css`, `static/css/bootstrap.custom.min.css.map` | Restyle existing Fatigue surfaces exactly once. Compare compiled CSS outside Fatigue rules against the control. Unexpected non-Fatigue changes stop acceptance of the rebuild. |
| `e2e/frame-check.ts`, `e2e/scripts/run_frame_check.py`, new route check file(s) | Reuse shared C1–C5/C8. Register the three routes against the verified Navigation merge. Select the page header and **every** relevant outer panel and assert the expected population before checking its geometry. Cover visible SVG regions, readouts, labels and actual 767/768 layouts separately. |
| `e2e/summary-pages.spec.ts`, `e2e/fatigue.spec.ts`, `e2e/fatigue-stage4-smokes.spec.ts`, `e2e/accessibility.spec.ts`, `e2e/visual-field-separator.spec.ts`, `e2e/empty-states.spec.ts` | Preserve selector, fetch, terminal, keyboard, tooltip and colour guarantees. Strengthen empty-seed tests with reachable populated data and nonzero dimensions. Keep independent route/JS/golden characterizations. |
| `tests/test_css_cascade_contracts.py`, `tests/test_css_field_separator_contracts.py`, `tests/test_css_wp4_4_components_contracts.py`, `tests/test_css_wp4_4_i_is_repair_contracts.py`, `tests/test_visual_selector_contracts.py`, `tests/test_css_wp4_4_a_baseline_contracts.py` | Map superseded Summary pins to their new guarantees. Preserve shared-family specificity, Fatigue’s no-page-bundle assertion, swatch identity and capture protections. Update `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` only for justified changes. |
| `docs/product/DESIGN_BRIEF.md`, `docs/testing_phase2/A11Y_EXCEPTIONS.md`, `docs/test_inventory/`, group `PLANNING.md` and `mockup.html` | Record shipped semantics, exact measured axe counts, generated inventory where identities change, decisions, provenance and evidence. |

**Source constraints.** `static/css/layout.css` supplies the existing global `container` paint, old priority-column/card rules and frame. `templates/base.html` supplies the default main wrapper and navbar. Apply the frame using child-template `main_class`. Global `.container-fluid` changes would affect other routes and the navbar. Reweighting `.summary-frame.frame-calm-glass` within the legacy `:is()` families can change Progression’s table and its dark captures. The current capture helper also neutralizes several surface and control properties. Ordinary rendering and computed-style checks must establish the redesigned appearance.

### Sequence and proposed commits

1. **Requirements and control.** The group branch starts at `5668cfa3c2d7b6ba1a7c180dd2245e56613b1600`. Use this full SHA in source manifests and as the registered control for each of the three route checks. The same-content [mockup](mockup.html) sits beside Section 0. Its illustrative Export, sticky prototype navbar, simplified bar fill, selected-channel inset shadow, 3 px swatch radius and header spacing are prototype differences. The merged Navigation and common frame govern the application. The manager commits and pushes these planning artifacts, convenes the formal council, and records finding dispositions and delegated Gate 1 before production work.
2. **Ordinary before evidence and red tests.** On the verified merge, capture the 18 route × viewport × theme ordinary screens on a copied synthetic fixture. Record source/seed, effective date or window, app scale, viewport and theme. Include supplemental before states for Direct Only, Details open, Session boundary warnings, Fatigue Planned/Logged, empty/error, and scale-8 320/360/390 px. Use an isolated fixture with a recorded logged date inside the intended window for the dual-channel check. Test through normal page entry points and actual AJAX rerenders. Save the two demonstrated data defects, representative frame failures and relevant contrast results before changing production. Record existing passes separately.
3. **Summary frame and row repairs.** Implement shared opt-in components plus both Summary markup/render paths. Use one accessible row population for the card and table presentations where practical. Preserve `#weekly-summary-container`, `#session-summary-container`, both volume `tbody` IDs, `#categories-table-body`, `#contribution-mode`, `#volume-formula-text`, Pattern Coverage hooks and `data-visual-surface` consumers. Pair strict dynamic category labels and tablet header correspondence with green tests. Keep `#754`’s handler; preserve category tooltip disposal and re-creation. Include design-brief updates and equivalent contract pins in this commit.
4. **Fatigue and shared badge.** Apply the frame locally, restyle score, SFR, meter surroundings and badge, and preserve band tokens, source SVGs, track range/reference, DOM data and original channel/period handling. Keep the map’s no-JS/asset-failure fallback. Rebuild CSS and sourcemap once and inspect drift. Compare light/dark palette and representative map region paints directly with the control. Run focused Summary and Fatigue tests together because the shared badge affects all three page comparisons.
5. **Evidence and scoped baselines.** Capture ordinary after screens with identical fixture and states. Run each new frame check twice and compare metrics bytes. Re-run prior migrated route checks. A fresh manual reviewer receives the before/after screens, candidate mockup and acceptance criteria. Resolve concrete discrepancies before regenerating. Apply only the approved files from the allowlist below, update the two affected screenshot-manifest records and digests, then compare the complete visual suites.
6. **Release gates.** Run required gates from changed paths and `/verify-and-polish`, including full pytest, functional Chromium, seed-backed main visual matrix, TypeScript, Vitest, inventory checks, seven-surface Stylelint and edited Summary stylesheet lint, SCSS drift, independent code/manual/polish reviews, and native Linux deep compare without retries. Shared-CSS coverage includes `smoke-navigation`, `nav-dropdown`, `accessibility`, `dark-mode`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes` and `ui-hardening`. Record final-head checks, migration notes for presentation, corrected wording, unchanged calculations, #754, reviewers and **Decisions taken without the owner** in the PR. The manager records delegated Gate 2 only when the required evidence exists.

### Snapshot allowlist and controls

For **each** of `win32` and `linux`, only existing PNGs under `e2e/__screenshots__/<platform>/visual.spec.ts-snapshots/` matching one route stem and one suffix below may change.

| Route stem | Exact suffixes |
|---|---|
| `weekly-summary-` | `mobile-light.png`, `mobile-dark.png`, `tablet-light.png`, `tablet-dark.png`, `desktop-light.png`, `desktop-dark.png` |
| `session-summary-` | `mobile-light.png`, `mobile-dark.png`, `tablet-light.png`, `tablet-dark.png`, `desktop-light.png`, `desktop-dark.png` |
| `fatigue-` | `mobile-light.png`, `mobile-dark.png`, `tablet-light.png`, `tablet-dark.png`, `desktop-light.png`, `desktop-dark.png` |

This is **18 permitted files per platform, 36 total**. Baseline viewports are **375×812, 768×1024 and 1440×900**. Ordinary/frame review uses **390×844, 768×1024 and 1440×900**. No thumbnail or other route is on the allowlist. There are zero new byte exemptions. The five registered exemptions remain `workout-plan-desktop-light`, `workout-plan-desktop-dark`, `plan-desktop-light-advanced`, `plan-desktop-dark-advanced` and `plan-desktop-dark-simple`.

Use scoped Windows generation only after manual comparison. For Linux, use the authorized native generate workflow and copy only the changed allowlisted files. Retain the full native compare, existing tolerances, masks and terminal checks. Keep ordinary captures under `artifacts/design-736/step4-summaries/`, and put paths and measured conclusions into the PR and committed planning record.

### Council questions

1. Does the opt-in 24 px phone H1 resolve D14 and C3 with the smallest change to shared components?
2. Do the new tests prove real post-refresh card labels and actual tablet column identity, including a category row and an isolated-muscle row, without allowing a hidden table or zero-width border to satisfy the check?
3. Does the badge retain a usable existing explanation, and do full/partial/error states preserve all available readings without duplicating page-level empty messages?
4. Do the ordinary Fatigue comparisons establish palette, fill/stroke, meter reference, period and channel parity independently of the stabilized snapshots?
5. Is every protected workflow and unrelated image insulated from page-bundle cleanup, the SCSS rebuild, and any opt-in shared CSS changes?

## Agent provenance

| Role | Agent ID | Status |
|---|---|---|
| Product manager, Section 0 and Plan v1 | `/root/summary_routes_pm` | Original scratch-draft author resumed and formally promoted both artifacts. ID supplied by the manager. |
| Product manager, response matrix and Plan v2 | Pending | Resume the original author after reviewer dispositions. |
| Architecture reviewer | Pending | Group council has not run. |
| Test strategist | Pending | Group council has not run. |
| Product risk reviewer | Pending | Group council has not run. |

**Same PM resumed for the matrix and v2?** Pending. **Continuity evidence gap for Section 0 and v1:** none.

**Approval status:** Owner Gate 0 is complete. Formal group council, finding dispositions, Plan v2 and delegated Gate 1 are pending. Capture ordinary screens and red controls on the Navigation merge before implementation. Candidate measurements, independent manual comparison, baseline approval and Gate 2 follow implementation.
