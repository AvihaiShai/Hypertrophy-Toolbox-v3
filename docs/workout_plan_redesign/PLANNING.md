# Plan Review — Workout Plan redesign (#736 step 3)

**Status** — Section 0 drafted on 2026-11-27. The owner's "Decisions" reply of 2026-11-26 is
the Gate 0 answer for the decisions it names (see
[Section 0 sign-off](#section-0-sign-off--gate-0)). Thirteen assumptions (P1–P13) are not
covered by that reply and carry no sign-off. No plan has been drafted.

**Planning size:** Large under
[`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md#plan-stage-routing), because the work edits
shared CSS surfaces (`tokens.css`, `layout.css`, `components.css`). Gate 0, then a
council-reviewed Gate 1, precede implementation. The owner delegated Gate 1 and Gate 2 for
steps 3–5 on 2026-11-20 (`artifacts/design-736/RUN_PROMPT.md`, "Approvals I am giving", item 2).

**Sources.** [Issue #736](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/736): the
"Plan: Astra" comment (the adopted plan) and the "Owner decisions" comment, read from
`artifacts/design-736/decisions/issue-736-full.txt`. The owner's standing instruction,
`artifacts/design-736/RUN_PROMPT.md`. The 24 questions, `artifacts/design-736/DECISIONS_FOR_ASTRA.md`,
and the owner's answers, `artifacts/design-736/DECISIONS_REPLY.md`. The council-settled choices,
`artifacts/design-736/decisions/COUNCIL_SETTLED.md`. The pilot's Section 0 and Evidence rounds,
[`docs/workout_log_pilot/PLANNING.md`](../workout_log_pilot/PLANNING.md).

**What was read.** The branch `feat/736-workout-plan`, created from `origin/main` at `8b023d1a`
(the merged pilot, PR #748). The template, stylesheets, scripts and tests cited below were opened
at that commit. Nothing was run: this pass had no shell, so every count is a `grep` line count
and every contrast ratio is computed by hand. The list of what could not be verified is at the
end of Section 0.

---

## Section 0 — Requirements Brief

**Raw request** (verbatim)

The owner's standing instruction for steps 3 to 5 (`artifacts/design-736/RUN_PROMPT.md`):

> Take GitHub issue #736 (AvihaiShai/Hypertrophy-Toolbox-v3, the UI redesign) from where it stands to ready for me to close, working autonomously between my gates.

> 2. Write Section 0 with `/requirements`, with a phone and a desktop mockup of the same content. Commit and push it, and stop for my Gate 0. Present each assumption the way I took the pilot's: one line on what I will see, one line on what I lose, and your recommendation.

The adopted plan's step 3 ("Plan: Astra" on #736), without its trailing link:

> 3. **Move Plan’s routine and exercises up front.** A populated plan opens on the selected routine. An empty plan offers a starter or a first exercise. Put Add Exercise beside its picker and keep active filters discoverable when collapsed. Contain horizontal scrolling inside a labeled, keyboard-accessible table region. Replace the existing 14-surface and page-overflow assertions in the same change. Verify that the last column, row actions and both Simple and Advanced views remain reachable.

The orchestrating session's request for this document. It is an agent's message, not the
owner's. Its first paragraph and its list of contents are quoted in full. Its output path, its
reading list, its style rules and its return instructions are left out:

> Write Section 0 (the requirements brief) for step 3 of GitHub issue #736: migrating the Workout Plan page (`/workout_plan`) of the Hypertrophy Toolbox onto the shared page frame and `ui-` components that the Workout Log pilot (step 2, merged as `8b023d1a`) introduced. Use the `requirements` skill. You are the only writer in this checkout right now; the branch is `feat/736-workout-plan`, already created from fresh `origin/main`. Do not commit — the orchestrator commits.
>
> **What Section 0 must contain:**
> 1. The raw request and scope: what step 3 covers and what it leaves to steps 4 and 5. D17 (one shared modal and drawer style, built in step 3, with a style check for the modal added before the restyle) and D24 belong to this step.
> 2. Every D answer and K item that applies to step 3, stated as a requirement, each with its source (`D2, owner`, `D5, default`, `K7, council 2/3`, …). Where a K item touches D2 or D3 it follows the owner's answer.
> 3. Assumptions: anything Section 0 needs that neither a D answer nor a K item nor the pilot's shipped rules settles. For each, give one line on what the owner will see, one line on what the owner loses, and your recommendation. Mark each one clearly as **not covered by the owner's reply** so the orchestrator can settle it under the run prompt's "Decisions and missing information" order. Do not invent an owner answer.
> 4. Pinned design values for this page, reusing the pilot's tokens and components by name. Say which shared component each Workout Plan element uses, and which new shared components step 3 must build (modal, drawer, anything else the page needs), with measurable values.
> 5. The page at each band: phone and tablet cards below 1360 px, table from 1360 px (D5), card content (D6), supersets (D7), routine tabs (D2, K5), filters (D3), header actions and the "More" menu (D4), Add exercise panel (D1, K1), volume summary and Volume targets button (D24), empty plan (K6), Simple/Advanced (K3), editable numbers (K4), table scroll region (K2). Describe behaviour that must not change (drag reorder, superset link/unlink, swap, inline edit, generator modal, export, replace) by pointing at the route or module that owns it.
> 6. Acceptance criteria, numbered and each checkable by a named kind of test (frame check, Playwright functional, pytest contract, visual capture, manual by-eye). Include the generalised frame check of K11 and the K9 replacement assertions with the four pinned test titles that stay. Include narrow-phone criteria at 320, 360 and 390 px at app scale 8 with the widest realistic values, 44 px tap targets and no page-level sideways scroll — the owner held the pilot for exactly this.
> 7. Page-level overrides that are deleted and what stays (K14).
> 8. Test pins and visual baselines that move: name every committed capture that changes on win32 and linux (the Workout Plan captures in `visual.spec.ts` and the plan thumbnails in `visual-baseline-thumbnails.spec.ts`), state which stay byte-gate-exempt (K10), and list the contract tests, inventory pins and manifest digests that move. Verify each name against the files on disk; do not guess.
> 9. Calculation-surface obligations as the skill requires. The limit is: no change to calculation logic, the database schema or API response shapes. If any requirement above cannot be met as presentation only, say so explicitly under a heading "Needs more than presentation" — that is a stop condition for the run.
> 10. A "Section 0 sign-off — GATE 0" block that quotes the owner's reply from `DECISIONS_REPLY.md` verbatim, dated 2026-11-26, and lists which requirements it covers. Do not write a sign-off for anything listed under item 3.
> 11. A "Mockups" subsection with a placeholder line saying the mockup page will be `docs/workout_plan_redesign/mockup.html` with captures under `artifacts/design-736/step3/mockups/`; the orchestrator fills in the file list.

**Problem**

The Workout Plan page still uses the pre-pilot styling, and it is the page where that styling
costs the most.

- **The whole page scrolls sideways on a desktop.** At 1440 px the page is 1,606 px wide. The
  Simple view shows 16 of the table's 22 columns and the wrapper deliberately lets them overflow
  the page (`.tbl-wrap--full`, `static/css/layout.css:1263-1268`). A test asserts the overflow
  (`e2e/workout-plan-desktop-contract.spec.ts:215-222`).
- **The plan is far down the page.** The page opens with 12 open filter dropdowns, then six
  prescription inputs, then the routine and exercise pickers, then a seven-button toolbar. At
  390 px the Add Exercise button starts about 3,238 px down, the table at 3,812 px, and six
  exercises make the page 9,328 px tall (discovery notes, measured by Astra; not re-measured).
- **The page has five left edges and four filled primary buttons.** At 1440 px the title starts
  at x = 81, the frame titles at 114, the filters at 94, the inputs at 74 and the table at 82.
  `export-to-log-btn`, `add_exercise_btn`, `generate-plan-btn` and `link-superset-btn` are all
  filled, and the row's Remove button is filled red (`templates/workout_plan.html:231-320`,
  `static/js/modules/workout-plan-table.js:426`).
- **The page restyles shared components itself.** `static/css/pages-workout-plan.css` is 5,810
  lines and 490 of them carry `!important`. `static/css/components.css` names the page on 182
  lines, `theme-dark.css` on 24 and `layout.css` on 2 (lines matching
  `data-page="workout-plan"`, `.workout-plan` or `workout-plan-table`).
- **Its dialogs keep the old look.** Generate Starter Plan is a glass panel with an inline width
  of 1600 px, Clear Plan has a filled red header (`templates/workout_plan.html:372-373`,
  `:566-567`), and the Volume targets drawer is styled from the Bootstrap build with its own
  hard-coded colours and dark-theme rules (`scss/pages/_workout_plan_volume_panel.scss`).

Step 3 must put the Workout Plan on the frame and components the Workout Log pilot shipped, build
the shared pieces the Log did not need, and delete the page rules those pieces replace.

### What step 3 covers, and what it leaves

| Step 3 covers | Left to a later step |
|---|---|
| The Workout Plan page at every width, in both themes, empty and populated | The navbar and navigation icons (step 4, D8–D11) |
| The shared modal and drawer style (D17), applied to Generate Starter Plan, Clear Plan, the reference-video modal and the Volume targets drawer, with the Clear Log modal brought in | The modals of pages not yet migrated: Erase All Data, the two Progression goal modals, Delete Volume Plan. They migrate with their pages (step 4) |
| The position of the volume summary and the Volume targets button (D24) | The volume summary on the Volume Splitter page (`.volume-active-summary`, step 4) |
| New shared components the page needs: menu, tabs, chip, modal, drawer | Segmented control, select, text field, checkbox, notice and stat tile as shared components (K51, built by the first step 4 PR that needs each) |
| The frame check generalised so that it runs on the Log and the Plan (K11) | Running the frame check on the other nine routes (step 4), and any decision to make it a CI check (K61, the owner's) |
| | Motion: timings, easing, hover gating and the removal of decorative animation (step 5, D19–D23). Step 3 keeps today's timings for the drawer and the modals and adds no motion |
| | Wording corrections on other pages (D18) and page titles (K28) |

### Mockups

The mockup page will be `docs/workout_plan_redesign/mockup.html`, with captures under
`artifacts/design-736/step3/mockups/`. The orchestrator fills in the file list.

| File | Shows |
|---|---|
| *(to be filled in by the orchestrator)* | |

The thresholds marked ⚠️ in this brief (P13) were derived by arithmetic from the pilot's shipped
values. They are confirmed or corrected against the mockup before Gate 1.

### Requirements from the owner's answers and the council

Each row is a requirement. "D" rows come from the 24 questions: `owner` means the owner chose the
option, `default` means the owner accepted the published default. "K" rows were settled by the
plan council on 2026-11-25 and are not owner answers. Where a K row touches D2 or D3 it follows
the owner's answer, and the row says so.

| # | Requirement | Source |
|---|---|---|
| R1 | The page uses the pilot's frame: one left edge per width (16, 24, 32 px), a plain page header with the title on the left and the actions on the right, opaque panels with a hairline border and no shadow, radii of 8, 12 and 999 px, six type sizes, content capped at 1800 px | Pilot Section 0 as shipped in `8b023d1a`; `DECISIONS_FOR_ASTRA.md`, "What is already fixed and is not being asked" |
| R2 | **Page order.** The exercise list is the first panel. One "Add exercise" panel sits below it and holds the routine, the exercise picker, the six prescription fields, the estimate row and the Add button. The filters are collapsed inside that panel | D1, default |
| R3 | **Routine on open.** A populated plan opens on the first routine's tab. The All tab stays available. Nothing is remembered between visits | D2, owner |
| R4 | **Filters.** Collapsed at every width. Each active filter is shown by name as a removable chip | D3, owner |
| R5 | **Header actions.** Export to Workout Log is in the page header. Export to Excel, Backup Center, Generate Starter Plan and Clear Plan are in a "More" menu | D4, default |
| R6 | **Layout switch.** Cards below 1360 px, the table from 1360 px, the same rule as the Log | D5, default |
| R7 | **Card content.** A closed card shows the name, the routine, one prescription line, Swap and the video button. Muscles, execution style, superset selection and Remove are behind Details | D6, default |
| R8 | **Supersets.** A neutral rail down the left of both rows and a "Superset" text badge. The four colours go | D7, default |
| R9 | **Modals and the drawer.** One shared modal and drawer style: 16 px radius, raised shadow, plain header, filled red only on the confirm button. It is built in this step and applied to this page's dialogs. The Clear Log modal is brought in with it. A style check for the modal is added before the restyle | D17, default |
| R10 | **Volume.** The volume summary and the Volume targets button sit at the top of the exercise list panel, next to the routine tabs | D24, default |
| R11 | Add Exercise is the page's one filled primary button, on an empty plan and on a populated one | K1, council 2/3 |
| R12 | The table keeps all its columns. It scrolls inside a labelled, focusable region. No column is sticky | K2, council 3/3 |
| R13 | The Simple/Advanced toggle stays on the table | K3, council 3/3 |
| R14 | Editable numbers become field-shaped boxes like the Log's logged values | K4, council 2/3 |
| R15 | Routine tabs become one line each and keep their counts. Following D2 (owner), All stays as a tab and the first routine's tab is the one selected on open | K5, council 2/3; D2, owner |
| R16 | An empty plan shows an empty-state panel outside `tbody`, with Generate Starter Plan (today's modal) and "Add first exercise". Following D2 (owner), an empty plan has no routine tab to open on, so All is selected | K6, council 3/3; D2, owner |
| R17 | Row borders on the tables the 3:1 checks measure use `--ink-3`. The checks are not re-pointed. The Plan's row lines are therefore slightly heavier than the Log's | K7, council 2/3 |
| R18 | The custom dropdowns (`.wpdd`) are restyled with tokens and not replaced. This covers the 12 filter dropdowns that D3 collapses and the exercise picker. Accessibility exceptions X9 and X10 stay as the owner deferred them | K8, council 3/3 |
| R19 | The 14-surface, page-overflow and three-section assertions are replaced in the same PR by frame assertions: gutter, no page overflow, the table region scrolls, the last column and the row actions are reachable. The four pinned test titles stay | K9, council 3/3 |
| R20 | The five byte-gate-exempt captures stay exempt | K10, council 3/3 |
| R21 | The frame check is generalised: C1–C5 and C8 on any route, with per-route extras. Any exemption list is explicit and short | K11, council 3/3 |
| R22 | The dark pastel per-field inputs and the routine-tab colours are dropped | K12, council 3/3 |
| R23 | Labels stay as they are. The page uses one delete icon. No select option carries an emoji | K13, council 3/3 |
| R24 | Plan-only rules are deleted. The shared `:is()` groups and the `#workout[data-page]` weight stay | K14, council 3/3 |
| R25 | Link Superset and Unlink become secondary buttons in the selection bar. Drag-to-reorder stays on cards by its handle. Advanced-only fields sit behind Details on cards | `COUNCIL_SETTLED.md`, "Also fixed for step 3" |
| R26 | None of these is built, whichever option is chosen: server-side routine memory; per-routine volume totals beyond `/api/volume_progress`; exporting only visible columns; supersets of more than two; new confirmation behaviour | `COUNCIL_SETTLED.md`, "Not allowed, whichever option is chosen" |
| R27 | No change to calculation logic, the database schema or API response shapes. The indigo accent and bundled Inter stay. No runtime CSS bundle is added. `DESIGN_BRIEF.md` is updated in the same change as any token or component change. The page adds no `!important` and does not restyle shared components from its page bundle. No file is deleted | `RUN_PROMPT.md`, "Limits that stay in force" and "Done means" |

R9 also covers the reference-video modal (`templates/partials/exercise_video_modal.html`). D17
names it, and the two pages that open it, Plan and Log, are both migrated once this step merges.
It is included from `templates/base.html:268`, so the markup is present on every route.

D18 (default B: correct only false statements, each listed in the PR) applies if a false
statement is found on this page. None was identified in this pass. The page was not searched
exhaustively for one.

### Pinned design values

Every value the pilot shipped is reused under its existing name. Where a value is new it is
marked ⚠️ and repeated under *Assumptions made*.

#### Reused from the pilot (no change)

| Kind | Name | Value |
|---|---|---|
| Radius | `--ui-control-radius`, `--ui-panel-radius`, `--ui-pill-radius` | 8 px, 12 px, 999 px |
| Gutter | `--ui-gutter` | 16 px below 768 px, 24 px from 768 px, 32 px from 1360 px |
| Title | `--ui-title-size` / `--ui-title-line` | 20 / 28 px below 768 px, 24 / 32 px from 768 px, weight 600 |
| Type | Inter, weights 400, 500 and 600, six sizes | 12, 14, 16, 18, 20 and 24 px, fixed (pilot A2) |
| Hairline | `--ui-hairline` | `#dfe3ec` light, `#3a4654` dark |
| Field surface | `--ui-field-surface` | `--surface-2` light, `--surface-0` dark, with a 1 px `--ink-3` border |
| Primary fill | `--ui-primary` | `#4263eb` light, `#5264ad` dark |
| Danger text | `--ui-danger` | `#c0362c` light, `#f08a80` dark |
| Status | `--ui-achieved`, `--ui-achieved-bg`, `--ui-pending`, `--ui-pending-bg` | As shipped (`static/css/tokens.css:487-503`) |
| Raised surface | `--shadow-elev-2` | Dropdowns, drawers, modals and toasts only |

- The page header starts 16 px below the navbar under 768 px and 24 px from 768 px.
- Inside the page content there is no `box-shadow`, `backdrop-filter`, gradient or inset shadow.
- Below 768 px every button, field and disclosure is at least 44 px tall. From 768 px buttons
  are 40 or 32 px tall. A field on a card (below 1360 px) is 44 px tall with 16 / 24 px text.
- Dark theme is a token swap. No new component carries a `[data-theme='dark']` rule of its own.
- Numeric cells and fields use tabular numerals and are right-aligned.

#### Which shared component each element uses

| Workout Plan element | Shared component | Notes |
|---|---|---|
| Page container, header, title, actions | `ui-page-frame`, `ui-page-header`, `ui-page-title`, `ui-page-actions` (`static/css/layout.css:1839-1862`) | The template sets `main_class` to `ui-page-frame` as `templates/workout_log.html:9` does. `#workout[data-page="workout-plan"]` stays as the page wrapper |
| Exercise list panel, Add exercise panel | `ui-panel` | 16 px padding, 12 px radius, hairline, no shadow. Panels are 16 px apart |
| Export to Workout Log, the More button, Generate Starter Plan and "Add first exercise" in the empty state, Link as Superset, Unlink Superset, Swap, Clear Filters, the filters toggle | `ui-btn`, secondary (ghost for Swap, the video button, Details and the filters toggle) | |
| Add Exercise | `ui-btn ui-btn--primary` | The only filled primary in the page content (R11) |
| Remove, Clear Plan | `ui-btn ui-btn--danger` | Outline shape with danger text. Remove is `ui-btn--small` in the table |
| Six prescription inputs in the Add exercise panel, the routine and exercise selects | `ui-field-input` chrome | The `.wpdd` custom dropdowns take the same tokens (R18) |
| Editable numbers in the table and behind Details | `ui-field` | 32 px tall in the table, 44 px on a card (R14) |
| "Superset" badge, execution-style badge | `ui-badge`, neutral | ⚠️ A neutral badge variant is new: `--ink-2` text on `--surface-1` (P12) |
| Records below 1360 px | `ui-record-card` | The card and the table row are the same `tr`, as on the Log |
| Records from 1360 px | `ui-data-table` | With the ruled variant below |
| Empty plan | `ui-panel ui-empty-state` | |

#### New shared components that step 3 builds

All of these go in `static/css/components.css`, with tokens in `static/css/tokens.css`. None is
styled from the page bundle.

| Component | Used for | Measurable values |
|---|---|---|
| **Modal** ⚠️ (P7) | Generate Starter Plan, Clear Plan, Clear Log, the reference-video modal | Opt-in by class, so a modal that has not migrated keeps today's look. Surface `--surface-2`, opaque, 1 px hairline, radius 16 px (new token `--ui-modal-radius`), shadow `--shadow-elev-2`, no `backdrop-filter`. Header: plain, on the modal surface, title 18 / 24 px at weight 600, close control 40 px square (44 px below 768 px). Body and footer padding 16 px, footer buttons 8 px apart. Width: at most 480 px for a confirmation, at most 1120 px for Generate Starter Plan, 800 px for the video as today, and never wider than the viewport minus two gutters. The inline `width: 1600px` goes. At most one filled button, the confirm action |
| **Filled danger button** ⚠️ (P7) | A destructive modal's confirm action only | New token `--ui-danger-fill`: `#c0362c` light, `#a84f49` dark, white text. Computed by hand: 5.52:1 and 5.41:1 |
| **Drawer** ⚠️ (P8) | Volume targets | Right-hand sheet, `min(360px, 100vw)` wide and the full height of the viewport, as today. Surface `--surface-2`, radius 16 px on its two left corners, shadow `--shadow-elev-2`, plain header with an 18 / 24 px title at weight 600 and a 40 px close control (44 px below 768 px), body padding 16 px with its own vertical scroll. Rows are hairline boxes with a 12 px radius. Dark theme by token swap |
| **Menu** ⚠️ (P12) | "More" | A secondary `ui-btn` labelled "More" with a chevron, `aria-haspopup="menu"` and `aria-expanded`. The popover is a raised surface: `--surface-2`, 1 px hairline, 12 px radius, `--shadow-elev-2`, at least 200 px wide, aligned to the button's right edge and never outside the viewport. Items are 40 px tall (44 px below 768 px) with 14 / 20 px text. The destructive item uses `--ui-danger` text and sits below a hairline |
| **Tabs** ⚠️ (P3) | Routine tabs | One line per tab: label then count. 40 px tall (44 px below 768 px), 14 / 20 px at weight 500, 8 px radius. The selected tab has `--ink-1` text, a `--surface-1` fill and a 1 px `--ink-3` border. The others have `--ink-2` text and no border. No per-routine colour (R22). Tabs wrap onto further lines |
| **Chip** ⚠️ (P4) | Active filters | A pill (999 px) that is itself a button: filter name, value and a remove mark. 32 px tall (44 px below 768 px), 12 / 16 px at weight 500, `--ink-1` text on `--surface-1`, 1 px `--ink-3` border. Chips wrap |
| **Ruled table and card** (R17) | The Plan's table and cards | A variant of `ui-data-table` and `ui-record-card` whose row separator and card outline are 1 px `--ink-3`: 3.16:1 on the light panel and 5.10:1 on the dark panel (the pilot's computed figures). It is a shared variant because step 4's tables are measured by the same check |

### The page at each band

**Order, at every width (R2):** page header, exercise list panel, Add exercise panel.

#### Page header (R5, R11)

- Title "Workout Plan" (`h1`, unchanged text) on the left. Actions on the right: **Export to
  Workout Log** (secondary) and **More**. Below 768 px the actions drop under the title, and wrap
  onto a second row when they do not fit one.
- **More** holds, in this order: Export All Tables (today's label for the Excel export, R23),
  Backup Center, Generate Starter Plan, then Clear Plan below a hairline in danger text.
- The menu opens with a click, Enter, Space or the down arrow. The arrow keys move between items.
  Escape closes it and returns focus to More. A click outside closes it.
- Each item does what its button does today. Generate Starter Plan and Clear Plan open today's
  modals. When a modal opened from the menu closes, focus returns to the More button.

#### Exercise list panel (R3, R10, R13, R15, R16)

Top to bottom:

1. **Heading row.** The section title "Workout Plan Table" (`h2#workout-plan-table-heading`,
   unchanged text, 18 / 24 px), the volume summary (`#vpActiveSummary`) and the **Volume targets**
   button (`#vpToggle`, secondary). Below 768 px these stack and each is full width.
2. **Routine tabs.** All, then one tab per routine in today's order: Environment, then Program,
   then Workout (`compareRoutines()` in `static/js/modules/workout-plan-helpers.js:89-100`).
   - On a populated plan the first routine's tab is selected when the page opens, and only that
     routine's exercises are listed.
   - All lists every routine's exercises, as today.
   - Nothing about the chosen tab is written to `localStorage`, `sessionStorage`, a cookie or the
     server. A reload, or leaving and returning, opens on the first routine's tab again.
   - ⚠️ The opening tab is chosen once per page load (P1). ⚠️ A selected routine that no longer
     exists falls back to All (P2).
3. **Superset selection bar** (`#superset-actions`), shown only while a row is selected. It
   holds Link as Superset and Unlink Superset as secondary buttons (R25) and the selection
   message. ⚠️ Below 1360 px it stays in view under the navbar while it is shown (P6).
4. **Simple/Advanced toggle** (`.tbl-view-mode-toggle[data-table-key="workout_plan"]`). ⚠️ It is
   shown at every width (P10).
5. **Records**: cards below 1360 px, the table from 1360 px.
6. **Empty plan (R16).** The empty-state panel takes the place of the records. The table stays
   in the document with no rows, so its hooks resolve. The heading row and the tabs stay: the
   All tab shows a count of 0 and is selected, and the volume summary and Volume targets stay
   usable (`e2e/volume-progress.spec.ts:183-190` opens the drawer on an empty plan). ⚠️ Copy and
   the behaviour of "Add first exercise" are in P11.

#### Cards, below 1360 px (R6, R7, R8, R25)

One column below 768 px, two columns from 768 px.

**Always visible on a card**

| Element | Content |
|---|---|
| Drag handle | `.drag-handle`, a 44 × 44 px target |
| Thumbnail | 40 px, or nothing when the exercise has none (today's behaviour) |
| Exercise name | In full. It wraps and is never truncated |
| Routine | One caption line, for example `Workout A · GYM · Full Body` |
| Superset | The neutral rail on the card's left edge and the "Superset" badge, on both cards of a pair |
| Prescription line | For example `3 sets × 8–12 · 60 kg · RIR 2`. RPE is appended when the plan holds one (`· RPE 8`). The line wraps and is never truncated |
| Swap | Today's replace control |
| Video | Today's reference-video control: play when curated, search otherwise |
| Details | A disclosure button that reports its expanded state |

**Behind Details**

- The six editable numbers as fields, each with its label: Sets, Min Rep, Max Rep, RIR, RPE,
  Weight. ⚠️ Three to a row (P5).
- Muscles and the other Simple columns: Primary Muscle, Secondary Muscle, Isolated Muscles,
  Grips. In Advanced mode also Tertiary Muscle, Utility, Movement Pattern, Movement Subpattern,
  Stabilizers and Synergists (R25).
- Execution style: today's badge, which opens today's picker.
- The superset checkbox, with a visible label.
- Remove.

⚠️ Details is closed on load and its state is not remembered, as on the Log (pilot A12, P5).

#### Table, from 1360 px (R6, R12, R13, R14, R17)

- The table sits in a region with `role="region"`, an accessible name and `tabindex="0"`. The
  region scrolls sideways. The page does not.
- All 22 columns stay, in today's order and with today's headings. Simple shows the 16 columns
  listed at `e2e/workout-plan-desktop-contract.spec.ts:47-52` and Advanced adds the six at
  `:55-58`. From 1360 px, which columns show depends only on Simple or Advanced, never on the
  width of the container.
- No column is sticky. The last column (Actions) and every row's controls are reached by
  scrolling the region with the pointer or the keyboard.
- The six number columns show field-shaped boxes, 32 px tall, that open today's editor.
- Rows are separated by a 1 px `--ink-3` line (R17).
- A superset pair carries the neutral rail on the left of both rows and the "Superset" badge
  beside each name (R8).
- Each row keeps its checkbox, drag handle, thumbnail, name, Swap, video, execution-style badge
  and Remove.

#### Add exercise panel (R2, R4, R11, R18, R22)

Top to bottom:

1. Section title "Add exercise" (18 / 24 px).
2. **Routine**: today's three dependent selects (Environment, Program, Workout) and the
   breadcrumb (`#routine-breadcrumb`). The options lose their emoji (R23). Option values do not
   change.
3. **Exercise**: today's picker (`#exercise`) with its match count.
4. **Filters**: a toggle that is closed on load at every width, with Clear Filters beside it and
   the chips under it. Opening it shows today's 12 dropdowns (`#filters-form`).
   - One chip per filter that has a value. Removing a chip clears that one filter and re-runs
     today's filtering.
   - Clear Filters does exactly what it does today (`clearFilters()` in
     `static/js/modules/filters.js:161-256`): it clears every filter, the routine selection and
     the exercise selection.
   - ⚠️ Wording and placement are in P4.
5. **Prescription**: the six inputs in today's order (Weight, Sets, RIR, RPE, Min Rep, Max Rep),
   with no per-field colour (R22). Six to a row from 768 px, three to a row below.
6. **Estimate row**: the provenance text, the Learned badge, the Fatigue context chip and the
   "Show the math" expander, as today.
7. **Add Exercise** (`#add_exercise_btn`), the filled primary.

#### Dialogs and the drawer (R9)

- Generate Starter Plan, Clear Plan, Clear Log and the reference-video modal take the shared
  modal style. Their content, controls and ids do not change.
- ⚠️ Generate Plan is the one filled button in its modal (indigo). Clear Plan and "Yes, Clear
  All" are filled danger. "Watch on YouTube" becomes secondary (P7).
- The Volume targets drawer takes the shared drawer style. Its open state is still remembered
  across reloads (`vpDrawer.open`, `e2e/volume-progress.spec.ts:345-362`). The owner's deferral
  of exception X15 stands: the drawer's ARIA behaviour is not changed in this step.

#### Behaviour that must not change

Each of these keeps its request, its payload, its toast and its result. Only its appearance and
position change.

| Behaviour | Owner |
|---|---|
| Plan load and refresh | `GET /get_workout_plan`; `fetchWorkoutPlan()` in `static/js/modules/workout-plan.js:90-117` |
| Add Exercise, its validation and its toasts, including the toast that names a routine hidden by the active tab | `POST /add_exercise`; `static/js/modules/workout-plan-add-exercise.js` |
| Inline edit: Enter or leaving saves, Escape cancels, a blank count reverts, a rejected value keeps the saved one | `POST /update_exercise`; `makeTableCellEditable()` in `static/js/modules/workout-plan-table.js:525-644` |
| Drag to reorder by the handle, with a superset partner following | `POST /update_exercise_order`; `initializeDragAndDrop()` in `workout-plan-table.js:654-721` |
| Superset select, link, unlink and the selection messages | `POST /api/superset/link`, `POST /api/superset/unlink`; `static/js/modules/workout-plan-supersets.js` |
| Swap (replace) and its three outcomes | `POST /replace_exercise`; `static/js/modules/workout-plan-replacement.js` |
| Remove | `POST /remove_exercise` |
| Execution style | `GET /api/execution_style_options`, `POST /api/execution_style`; `static/js/modules/workout-plan-execution-style.js` |
| Reference video and thumbnail preview | `static/js/modules/exercise-video-modal.js`, `static/js/modules/workout-plan-media.js` |
| Filtering and Clear Filters | `POST /filter_exercises`, `GET /get_all_exercises`; `static/js/modules/filters.js` |
| Routine cascade, including its blank state after a load, a refresh and Back | `GET /get_routine_exercises/<routine>`; `static/js/modules/routine-cascade.js` |
| Estimates and the six controls' persistence in `sessionStorage` | `GET /api/user_profile/estimate`; `workout-plan-estimates.js`, `workout-controls-persistence.js` |
| Simple/Advanced, shared with the navbar's muscle-naming toggle | `static/js/modules/filter-view-mode.js`, `static/js/table-responsiveness.js:182-341` |
| Generate Starter Plan | `POST /generate_starter_plan`; the modal's form and `static/js/modules/workout-plan-page.js:110-197` |
| Export to Workout Log | `POST /export_to_workout_log` |
| Export to Excel, for all columns in the chosen view mode | `GET /export_to_excel?view_mode=…`; `static/js/modules/exports.js` |
| Backup Center link | `/backup?intent=browse` |
| Clear Plan, including the reset of the six controls | `POST /clear_workout_plan` |
| Volume summary and drawer | `GET /api/volume_progress`; `static/js/modules/plan_volume_panel.js` |
| One `/get_all_exercises` request per load and one `change` listener on `#routine` | `e2e/exercise-catalog-fetch.spec.ts` |

### Acceptance check ("frame check")

The pilot's check measures one route (`e2e/workout-log-frame.check.ts`, started by
`e2e/scripts/run_workout_log_frame.py`). R21 makes it run on any route. Anyone must be able to
rerun it for a named route with one documented command, on a throwaway database that never
shares a server run with `visual.spec.ts`.

**Shared checks, any route**

| # | What is counted | Pass |
|---|---|---|
| C1 | Left and right edges of the page header block and of each panel | One left edge, equal to the gutter for that width. The right edge is the viewport width minus the gutter. The header starts 16 px below the navbar under 768 px and 24 px from 768 px |
| C2 | `border-top-left-radius` of every element with a non-zero radius | Distinct values are within 8, 12 and 999 px |
| C3 | `font-size` and `font-weight` of every element that has its own text, excluding Font Awesome glyphs | Sizes within 12, 14, 16, 18, 20 and 24 px. Weights within 400, 500 and 600. The title is the largest text on the page |
| C4 | `box-shadow`, `backdrop-filter`, `background-image` of every element | All `none` |
| C5 | `document.documentElement.scrollWidth` | Not above the viewport width, at every width and in every scale 8 pass |
| C8 | Source: `[data-theme` selectors that name a `ui-` class, outside `tokens.css` | 0 |

The population is every element inside `#main-content` that has a client rect, with every
overlay closed. Values are read with `getComputedStyle` and `getBoundingClientRect`, with fonts
loaded and transitions and animations disabled. "Distinct" means the set of serialized values
after rounding lengths to 0.5 px. A route's exemptions are written in the check as a named list
with a reason each.

**Fixture for the Plan.** The database built by `e2e/scripts/prepare_visual_db.py`, which holds
six plan rows in `GYM - Full Body - Workout A` (`e2e/scripts/build_visual_seed.py:52-59`). Every
seed row has one routine, no superset, no RPE and the standard execution style, so the check
applies scripted edits before it measures. Which row carries which edit was chosen here, not by
the owner.

| Edit | Case it provides |
|---|---|
| Barbell Bench Press and Barbell Bent Over Row linked through `POST /api/superset/link` | A superset pair (R8) |
| Barbell Squat set to 10 sets, 30–30 reps, 102.5 kg, RIR 10, RPE 9.5 | The widest realistic values as the page prints them |
| Barbell Deadlift set to 999.5 kg | The widest value the inline editor's limit allows (0–1000 kg) |
| Barbell Curl given the AMRAP execution style with a 60 s cap | A non-standard style badge |
| `Cable Standing Single Arm Internally Rotated Incline Chest Fly` added to Workout A | A long name (62 characters) |
| Two exercises added to `GYM - Full Body - Workout B` | A second routine, so the opening tab can be told from All (R3) |
| One exercise added to `GYM - Upper Lower Hypertrophy Split - Workout B Heavy` | A long routine name for the tabs and the caption |

The Plan prints stored numbers as JavaScript numbers, so 100.0 shows as `100`
(`workout-plan-table.js:413-418`). The widest realistic weight on this page is therefore a
half-kilogram value such as `102.5`, which is as wide as the `100.0` the owner named on the Log.

**Conditions for the Plan**

- Chromium at 390 × 844, 768 × 1024 and 1440 × 900, light and dark, empty and populated, at app
  scale level 6.
- One extra pass at scale level 8 (factor 1.2) at 390 and 1440 px.
- Narrow passes at 320 and 360 px at scale 8 in both themes, and at 320 px at scale 6.
- Two passes at 1359 × 900 and 1360 × 900, light, populated.
- At 1360 and 1440 px, both Simple and Advanced. At every width, both the opening tab and All.

**Checks for the Plan only**

| # | What is counted | Pass |
|---|---|---|
| WP6 | At 390 px at scale 6: name lines, card height, targets | The six seed names take at most two lines. The long name shows in full with no ellipsis. Every visible button, field and disclosure is at least 44 × 44 px. ⚠️ A closed card with a one-line name is at most 200 px tall, and the top of the first card is less than 600 px from the top of the page (P13) |
| WP7 | At 1440 and 1360 px, Simple and Advanced: the table region | No heading has `scrollWidth` above `clientWidth`. ⚠️ The Exercise column is at least 220 px (P13). In Advanced the region's `scrollWidth` exceeds its `clientWidth`. After the region is scrolled to its end, each row's Remove button is inside the region's visible box and is the element at its own centre point. The visible headings are the Simple or the Advanced list |
| WP9 | Source: rules in `pages-workout-plan.css` that target a shared component (families under *Overrides*) | 0 for each deleted family. No `!important` is added, and the file's count falls from 490 lines to at most 65 |
| WP10 | At 1359 px and at 1360 px: which layout renders | At 1359 px the records are two-column cards and no column heading is displayed. At 1360 px the table is displayed. C5 passes at both |
| WP11 | At 320, 360 and 390 px at scale 8, and at 320 px at scale 6, with Details closed, with Details open on the Barbell Squat and Barbell Deadlift cards, and with a row selected | Every card is inside the viewport. Every control and value is inside its card or panel, to 0.5 px. No value or label is clipped and none overlaps another. Every button, field, tab, chip and disclosure is at least 44 × 44 px as rendered. The header actions, the tabs, the chips, the selection bar and the Add exercise panel's fields are inside their containers. C5 passes |
| WP12 | With the More menu open, at 390 and 1440 px in both themes | The popover is inside the viewport, its items are at least 44 px tall below 768 px, and its radius, surface and shadow are the pinned values |

**Controls.** The check is evidence only if it also fails where it should.

- On `main` at `8b023d1a` the Plan run must fail C1, C2, C3, C4, C5 and WP10.
- Two consecutive Plan runs on the branch must give byte-identical `metrics.json`.
- The Log run must still pass on the branch, and its control at `5dc83cef` must still fail C1 to
  C4 and C10, as recorded in the pilot's Evidence rounds.
- The raw output of every run goes under `artifacts/design-736/step3/` and is summarized in the
  pull request.

**The modal and drawer style check (R9).** It is a committed check that opens each of
`#generatePlanModal`, `#clearPlanModal`, `#clearLogModal` and `#exerciseVideoModal`, and the
drawer `#vpDrawer`, in both themes at 390 and 1440 px, and reads computed styles. It is
committed before the restyle and shown to fail on `8b023d1a`. It passes when:

- the modal surface is opaque `--surface-2` with a 16 px radius, the `--shadow-elev-2` shadow and
  no `backdrop-filter`;
- the header has no fill of its own and its title is 18 / 24 px at weight 600;
- the footer has at most one filled button: `--ui-primary` in Generate Starter Plan,
  `--ui-danger-fill` in Clear Plan and Clear Log, none in the video modal;
- the dialog is inside the viewport with at least the gutter on each side, and every button is
  at least 44 px tall below 768 px;
- the drawer has the pinned surface, radius and shadow and is inside the viewport;
- the modals that have not migrated (`#eraseDataModal`, `#deleteGoalModal`, `#goalSettingModal`,
  `#deleteVolumePlanModal`) read the same values on the branch as on `8b023d1a`.

### Page-level overrides that are deleted, and what stays

**Where things live.** No new bundle and no new `<link>`; the cap stays at 18.

| File | Receives |
|---|---|
| `static/css/tokens.css` | `--ui-modal-radius`, `--ui-danger-fill`. Additive: no existing token changes value |
| `static/css/components.css` | Modal, drawer, menu, tabs, chip, the neutral badge, the ruled table and card variant |
| `static/css/layout.css` | Nothing expected. The frame is already there |
| `static/css/pages-workout-plan.css` | Plan-only layout: column widths, the card's internal arrangement, the Add exercise panel's grid, the superset rail, the routine cascade, the execution-style picker, the body map inside Generate Starter Plan, the drawer's rows |
| `static/css/theme-dark.css` | Nothing for the Plan. Its Plan-only rules are deleted |
| `scss/pages/_workout_plan_volume_panel.scss` | ⚠️ Loses the drawer's rules (P8). The Volume Splitter rules in the same file stay until step 4 |

**What is deleted from `pages-workout-plan.css`.** The sections are the file's own comment
headings at `8b023d1a`. The `!important` figures are `grep` line counts bucketed by those line
ranges, not a parse. Rule and declaration counts per family were not measured in this pass; the
plan measures them with `scripts/css_audit/measure.py`.

| Family (file section, lines) | `!important` lines | After step 3 |
|---|---:|---|
| Filter dropdown and filter-form chrome, including the per-filter colour families (1–461) | 39 | Deleted. The filters toggle, the chips and the tokens replace it |
| Page header, collapsible frames, collapse toggles, Filters section, Workout Controls, inline controls row, input fields group, colour-coded control backgrounds, buttons, the table's glass chrome, the seven viewport-band blocks, the Advanced-mode table optimizations (713–3414 and 3948–4166, apart from the first routine-tabs block) | 425 | Deleted. The frame, `ui-panel`, `ui-btn`, `ui-field-input`, `ui-data-table` and `ui-record-card` replace them. Only field-keyed column widths and card layout remain |
| Routine tabs, both blocks (2631–2781, 4167–4260) | 0 | Deleted. The shared tabs replace them |
| Superset styles (3415–3673) | 15 | The four hues, the "SS" badge chrome and the selection-bar chrome are deleted. The rail's layout stays |
| Custom dropdown layer and its popover (462–712) | 4 | Kept and restyled with tokens (R18) |
| Execution style (3674–3947) | 3 | Kept. The badge takes the neutral badge; the picker's layout stays |
| Routine cascade (4261–4745) | 2 | Layout kept. Chrome and connector colours deleted |
| Dark mode block and transition animations (4746–4896) | 2 | The dark block is deleted (token swap). Feedback animations stay until step 5 |
| Muscle selector, the body map inside Generate Starter Plan (4897–5810) | 0 | Kept |

The `@layer workout-dropdowns` block stays, so the layer order pinned by
`tests/test_css_cascade_contracts.py::test_one_explicit_order_covers_every_existing_layer` does
not change. Whether the page's `@layer workout` block keeps any rule is for the plan; if it
empties, that pin moves and the plan says so.

**Shared bundles that name the Plan (R24).**

- Rules whose selector names only the Plan (`#workout[data-page="workout-plan"] …` with no other
  branch) are deleted where they style something the page no longer renders or would restyle a
  new component.
- That includes the four input rules at `components.css:3454-3569`. They use `:is(#weight, #sets,
  …)` to list the six inputs, but they are Plan-only and are not one of the shared groups.
- The shared `:is()` groups are not edited. `:is(#workout[data-page="workout-plan"],
  .workout-log-page, .summary-frame.frame-calm-glass)` gives the Summary pages their weight, and
  removing the Plan branch changes 8,856 computed values there
  (`tests/test_css_wp4_4_i_is_repair_contracts.py:18-33`).
- The template keeps `<div id="workout" data-page="workout-plan">`. The migrated elements stop
  carrying the classes those groups style (`table-calm`, `frame-calm-glass`, `collapsible-frame`,
  `btn-calm-*`, `input-calm-inset`), so the legacy rules stop applying to them without being
  touched.
- The legacy modal rules (`.modal-content.frame-calm-glass` and the like) stay for the modals
  that have not migrated.

**The Log.** The 12 `#clearLogModal` rules in `static/css/pages-workout-log.css:4-59` are
deleted when that modal takes the shared style. They were the pilot's one exception (pilot A10).
The file then has no `!important`.

**No file is deleted.** A file the redesign empties is left in place and listed for the owner.

### Test pins and visual baselines that move

**Hooks that stay**, so that functional specs keep working:

- Page and header: `#workout[data-page="workout-plan"]`, the `h1` text "Workout Plan",
  `h2#workout-plan-table-heading`.
- Add exercise panel: `#filters-form` with its `select.filter-dropdown[data-filter-key]`,
  `#clear-filters-btn`, `#routine`, `#routine-env`, `#routine-program`, `#routine-day`,
  `#routine-breadcrumb`, `#exercise`, `#exercise-match-count`, `#weight`, `#sets`, `#rir`, `#rpe`,
  `#min_rep`, `#max_rep_range`, `#weight-hand-hint`, the five `#workout-estimate-*` elements,
  `#add_exercise_btn`, and every `data-testid` these carry today.
- Actions: `#export-to-log-btn`, `[data-testid="export-excel-btn"]`, `#load-program-btn` with its
  `href`, `#generate-plan-btn`, `#clear-plan-btn`. The last four are inside the More menu.
- List: `#routine-tabs`, `#tab-all`, `#tab-count-all`, `.routine-tab-btn[data-routine]`,
  `.tab-count`, `#superset-actions`, `#link-superset-btn`, `#unlink-superset-btn`,
  `#superset-selection-info`, `[data-testid="exercise-table"]`, `.workout-plan-table`,
  `#workout_plan_table_body`, `tr[data-exercise-id][data-routine]`, `data-superset-group`,
  `.superset-checkbox`, `.drag-handle`, `.exercise-name`, `img.exercise-thumbnail` with
  `width="32"` and `height="32"`, `.btn-swap[data-action="replace"]`,
  `[data-action="play-video"]`, `td[data-field]`, every `data-label`, `.execution-style-cell`,
  `.execution-style-picker`, `.tbl-view-mode-toggle[data-table-key="workout_plan"]`,
  `tbl--view-simple` and `tbl--view-advanced`, and the row classes `supersetRowClasses()`
  returns (`static/js/modules/__tests__/workout-plan-seams.test.js:160-164`).
- Dialogs: `#generatePlanModal` and its form ids, `#generatePlanSubmit`, `#clearPlanModal`,
  `#confirmClearPlanBtn`, `#clearLogModal`, `#confirm-clear-log-btn`, `#exerciseVideoModal`,
  `.btn-close`, `#vpActiveSummary`, `#vpToggle`, `#vpDrawer`, `.vp-close`, `#vpBackdrop`,
  `#vpDrawerBody`, and the `.vp-*` classes the drawer's rows use.

**Pins that move.** Each moves in the same PR as the design change it follows.

| Pin | Why it moves |
|---|---|
| `e2e/workout-plan-desktop-contract.spec.ts:69`, `:193-201` | Three `[data-section]` blocks in order. Replaced by the page header, list panel and Add exercise panel in order (R2, R19) |
| `e2e/workout-plan-desktop-contract.spec.ts:206` | 14 `[data-visual-surface]` elements. Replaced by the gutter assertion (R19) |
| `e2e/workout-plan-desktop-contract.spec.ts:215-222` | The page must overflow 1440 px. Replaced by no page overflow, the region scrolls, the last column and the row actions are reachable (R19) |
| `e2e/workout-plan-desktop-contract.spec.ts:170`, `:293` | Select `.tbl-wrap` and `.btn-danger`. They follow the markup |
| `e2e/workout-plan-desktop-contract.spec.ts:353-397` | Stays as written. It must measure a drawn border (criterion 18) |
| `e2e/visual-field-separator.spec.ts:37`, `:185-186` | Selects `table.tbl--responsive` on the Plan. The 3:1 requirement and what it measures stay (R17). The selector string follows the class only if the class goes |
| `e2e/workout-plan.spec.ts:57`, `:361`, `:384` | `#filters-form` and its selects are visible on load. The filters are collapsed (R4) |
| `e2e/workout-plan.spec.ts:69`, `:506` | The Excel export button is visible on load. It is in the More menu (R5) |
| `e2e/workout-plan.spec.ts:637`, `:661`, `:681`, `:704`, `:789`, `:854`, `:882` | Click `#generate-plan-btn` directly. It is in the More menu |
| `e2e/exercise-interactions.spec.ts:549-591` | `selectOption` on the filter selects with the panel closed. Whether it fails was not verified; the tests open the panel if it does |
| `e2e/exercise-interactions.spec.ts:212`, `:223`, `:244` | Find Remove by `.btn-danger` among other selectors. Unchanged if Remove carries `data-action="delete"` or `.delete-btn` |
| `e2e/empty-states.spec.ts:60-61`, `e2e/error-handling.spec.ts:170` | The Excel export button is visible on load |
| `e2e/accessibility.spec.ts:257-259`, `:464-466`, `:495-497`, `:1107-1109` | `#generate-plan-btn` is visible on load |
| `e2e/accessibility.spec.ts:513` | Focus returns to `#generate-plan-btn` after the modal closes. It returns to the More button |
| `e2e/accessibility.spec.ts:887-896`, `:952-960` | `AXE_REGISTER` for `workout_plan:light`, `workout_plan:dark`, `state:modal-open` and `state:validation-error`. Counts may only fall (criterion 19). `docs/testing_phase2/A11Y_EXCEPTIONS.md` rows X7, X9, X10 and X15 change with them |
| `e2e/ui-hardening.spec.ts:637`, `:660`, `:1019` | Click or focus `#clear-plan-btn` directly. It is in the More menu |
| `e2e/program-backup.spec.ts:20-37` | The "Program actions" group holds `load-program-btn` and `clear-plan-btn`, and Backup Center is visible on load. Both are in the More menu |
| `e2e/dark-mode.spec.ts:137` | `#clear-plan-btn` has the filled red background `rgb(168, 79, 73)`. It becomes a danger-text menu item. Line 136 (`#add_exercise_btn` is `rgb(82, 100, 173)`) stays: that is `--ui-primary` in dark |
| `e2e/superset-edge-cases.spec.ts`, `e2e/exercise-interactions.spec.ts` and any spec that reads `#workout_plan_table_body tr` after loading a plan with more than one routine | The page opens on the first routine's tab, not All (R3). Specs that start from an empty plan are unaffected (P1). The full list was not established in this pass |
| `e2e/visual-helpers.ts:197-206`, `:213-215` | Capture-time CSS aimed at `[data-visual-header]`, `[data-visual-accent]` and `[data-section="filters"]` on the Plan, which the page no longer renders |
| `tests/test_css_cascade_contracts.py::test_relocated_frame_selectors_remain_reachable_from_runtime_hooks` (`:239-242`) | Asserts `class="collapsible-frame`, `frame-header-2025` and `.collapsible-frame` in the Plan template and `workout-plan-page.js` |
| `tests/test_css_cascade_contracts.py`, the ten `test_workout_plan_*` tests (`:807`, `:865`, `:951`, `:1056`, `:1106`, `:1144`, `:1186`, `:1230`, `:1285`, `:1361`) | Assert the text of rules in `pages-workout-plan.css` that are deleted, and at `:1045-1053` three collapsible frames, the header markup and the collapse script |
| `tests/test_css_cascade_contracts.py::test_bootstrap_artifact_keeps_scss_owned_selector_families` (`:106-121`) | Requires `.vp-drawer` and `#vpToggle` in the compiled Bootstrap file. Moves only if P8 is accepted |
| `tests/test_css_theme_dark_p3_audit_contracts.py:68` | Names `test_workout_plan_page_header_and_collapsible_frame_ownership_cleanup` |
| `tests/test_css_wp4_4_i_is_repair_contracts.py:112`, `:226` | `components.css` has 5,091 newlines and 883 `!important`. Lines are added and removed. `!important` may only fall |
| `tests/test_css_wp4_4_i_is_repair_contracts.py:215`, `tests/test_css_wp4_4_components_contracts.py:383-385` | `components.css` holds 19 `:is(` tokens, five of them in the four Plan-only input rules at `components.css:3454-3569`. Those rules are the per-field inputs R22 drops |
| `tests/test_css_wp4_4_a_baseline_contracts.py:156-158` | The `@layer workout` block of `components.css` spans lines 3358 to 3923, as a literal and against the working tree. Deleting a Plan-only rule inside or above that block moves the span, as the pilot's deletions did |
| `tests/test_css_wp4_4_components_contracts.py` (other assertions), `tests/test_css_wp4_4_a11y_contracts.py:314`, `tests/test_css_wp4_4_motion_contracts.py:33` | Pin the shape of `components.css` or name a line of `pages-workout-plan.css`. Which further assertions move was not established in this pass |
| `tests/test_template_landmarks.py:15` | Lists the routes whose `main` carries `ui-page-frame`. `/workout_plan` joins it |
| `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` with `tests/test_css_wp4_4_a_baseline_contracts.py` | `layers.spans` for `components.css` and `pages-workout-plan.css` (`:185-217` of the JSON), the `isFamily` totals and its records for the four Plan-only input rules (`:220-222`, `:610-766`), the two `oracleBlindSpots` entries that name the page bundle (`:2376`, `:2714`), the `workoutLogPilot.surfaces` ledger (`:2845-2884`), and the four `snapshotManifest` digests. Hand-edited for the affected entries only, never with `scripts/css_audit/emit_baseline.py` |
| `e2e/workout-log-frame.check.ts`, `e2e/scripts/run_workout_log_frame.py`, `e2e/playwright.workout-log-frame.config.ts`, `tests/test_workout_log_frame_runner.py` | The frame check is generalised (R21). The Log's checks and its scratch-path guards keep their coverage |
| `docs/test_inventory/` | Regenerated when any test is added, removed or renamed |
| `tests/test_vitest_inventory_contracts.py:75-77` | Only if a Vitest case is added, removed or renamed |

**Pins that must not move**

- The four test titles in `e2e/workout-plan-desktop-contract.spec.ts`, pinned by
  `tests/test_visual_capture_contracts.py:250-256`: "page composition and section order",
  "progressive column disclosure", "row media and controls" and "theme surfaces and separator
  contrast", with the literal `width: 1440`.
- The column lists at `e2e/workout-plan-desktop-contract.spec.ts:47-66` and the row checks at
  `:265-269` and `:297-317` (R12, R23).
- `BYTE_GATE_EXEMPT` in `e2e/visual-helpers.ts:58-64` and its strict equality at
  `tests/test_visual_capture_contracts.py:178-208` (R20).
- `e2e/browser-navigation-state.spec.ts:49-81`: the routine selects are blank after a load, a
  refresh and Back. R3 concerns the tabs, not these selects.
- `e2e/workout-plan.spec.ts:329` and `:463-468`: on a plan that was empty when the page loaded,
  All is selected (R16, P1).
- `e2e/volume-progress.spec.ts`, all of it: the drawer's behaviour, its geometry at three
  widths in both themes, and its remembered open state.
- `EXPECTED_SNAPSHOT_COUNTS` in `tests/test_css_wp4_4_a_baseline_contracts.py:46-51`: 66 and 15
  per platform. No capture is added or removed.
- `tests/test_playwright_shard_launcher_contracts.py`: the required functional set stays at 25.
  The frame check and the modal check stay out of CI.

**Visual baselines that move: 26 files**, each verified present under `e2e/__screenshots__/`.

| Spec | Captures | Per platform | Platforms |
|---|---|---:|---|
| `visual.spec.ts` | `workout-plan-mobile-light.png`, `workout-plan-mobile-dark.png`, `workout-plan-tablet-light.png`, `workout-plan-tablet-dark.png` | 4 | win32, linux |
| `visual-baseline-thumbnails.spec.ts` | `plan-desktop-light-simple.png`, and `plan-{mobile,tablet}-{light,dark}-{simple,advanced}.png` | 9 | win32, linux |

- **Still exempt, with no PNG on either platform (R20):** `workout-plan-desktop-light`,
  `workout-plan-desktop-dark`, `plan-desktop-light-advanced`, `plan-desktop-dark-advanced` and
  `plan-desktop-dark-simple`. They still run, render at 1440 × 900 and fail on a console error.
  Their coverage stays in `workout-plan-desktop-contract.spec.ts`.
- The suite's viewports are 375, 768 and 1440 px, so the captures show one-column cards,
  two-column cards and the table.
- win32 baselines are regenerated locally. The win32 thumbnail captures have no CI path. linux
  baselines come from the `Deep Gate Visual (Linux)` generate mode, and only the 13 listed files
  are copied out of its artifact.
- No baseline is regenerated before the by-eye sign-off, which the owner delegated for the PRs
  of steps 3 to 5 (`RUN_PROMPT.md`, "Approvals I am giving", item 4), and never with a blanket
  `--update-snapshots`.
- Every other committed baseline must compare clean without regeneration. The Log's 12 captures
  per platform do not move: its modal is closed in every capture.

**Documents updated in the same change:** `docs/product/DESIGN_BRIEF.md` (the rules that ship;
its "Components, as measured" table at `:310-332` describes today's Plan page),
`docs/product/APP_FLOW.md` (the Plan section, `:281-344`), `docs/CSS_OWNERSHIP_MAP.md` if it
lists a moved selector, and `docs/testing_phase2/A11Y_EXCEPTIONS.md` if an axe count moves.

**Acceptance criteria**

"The fixture" is the Plan fixture above. Widths are 390, 768 and 1440 px at app scale 6 unless
stated. Each criterion names the kind of test that checks it.

1. **Gutter and header.** Given the Plan at each width, in both themes, empty and populated,
   when the frame check reads the edges, then C1 passes. *(frame check)*
2. **Radius, type and surfaces.** Given the same pages, then C2, C3 and C4 pass. *(frame check)*
3. **No page-level sideways scroll.** Given the fixture at 320, 360, 390, 768, 1359, 1360 and
   1440 px, at scale 6 and at scale 8, in Simple and in Advanced, on the opening tab and on All,
   then C5 passes. *(frame check)*
4. **One primary action.** Given an empty plan or a populated one with every overlay closed,
   then the page content has exactly one filled primary button, `#add_exercise_btn`, and no
   filled red button. *(frame check; Playwright functional)*
5. **Page order.** Given the fixture at each width, then the page header, the exercise list
   panel and the Add exercise panel appear in that order from the top, and at 390 px the first
   card starts less than 600 px from the top of the page. *(frame check; pytest contract on the
   template)*
6. **Opening tab.** Given the fixture, when the page loads, then the first routine's tab
   (`GYM - Full Body - Workout A`) is selected and only its rows are listed. When All is chosen
   and the page is reloaded, then the first routine's tab is selected again. After any of these,
   `localStorage`, `sessionStorage` and the cookies hold no entry for the routine tab.
   *(Playwright functional)*
7. **All stays available.** Given the fixture, when All is activated by pointer or keyboard,
   then every routine's rows are listed and All reports `aria-selected="true"`. *(Playwright
   functional)*
8. **Empty plan.** Given an empty plan, then the empty-state panel is shown, `#workout_plan_table_body`
   has no `tr`, All is selected, and the volume summary and Volume targets are visible. When
   Generate Starter Plan is activated in the panel, then `#generatePlanModal` opens. When "Add
   first exercise" is activated, then focus is on the first control of the Add exercise panel.
   *(Playwright functional)*
9. **Filters collapsed, chips named.** Given the page at any width, when it loads, then the
   filters toggle reports `aria-expanded="false"` and the 12 dropdowns are not displayed. Given
   two filters with values, then two chips are shown, each naming its filter and its value, with
   the panel closed. When one chip is removed, then that filter's select is empty, the other is
   unchanged, one filtering request is sent and one chip remains. When Clear Filters is
   activated, then every filter, the routine selection and the exercise selection are cleared
   and the toast reads "Filters cleared successfully". *(Playwright functional)*
10. **Header actions.** Given the page, then Export to Workout Log is visible in the header and
    Export All Tables, Backup Center, Generate Starter Plan and Clear Plan are not visible. When
    More is opened by click, Enter, Space or the down arrow, then the four items are visible in
    that order. When Escape is pressed, then the menu closes and More has focus. When Clear Plan
    is chosen and its modal is closed, then More has focus. *(Playwright functional)*
11. **Card content.** Given the fixture at 390 px with Details closed, then each card shows the
    drag handle, the exercise name in full, the routine, the prescription line, Swap, the video
    button and Details, and the two linked cards show the rail and the "Superset" badge. The
    muscles, the execution style, the superset checkbox and Remove are not displayed.
    *(frame check; Playwright functional)*
12. **Details.** Given a card, when Details is activated by touch or keyboard, then the six
    number fields, the muscles, the execution style, the superset checkbox and Remove appear,
    and the button reports its expanded state. In Advanced mode the six Advanced-only fields
    appear as well. After a reload Details is closed. *(Playwright functional)*
13. **Narrow phones.** Given the fixture at 320, 360 and 390 px at scale 8, and at 320 px at
    scale 6, with the Barbell Squat values (10 sets, 30–30 reps, 102.5 kg, RIR 10, RPE 9.5),
    then WP11 passes with Details closed, with Details open and with a row selected. The same
    holds for the Barbell Deadlift card at 999.5 kg, except that at 320 px at scale 8 its value
    may run into its field's padding provided nothing is clipped and C5 passes. *(frame check;
    Playwright functional regression test at 320, 360 and 390 px at scale 8)*
14. **Card size and two columns.** Given the fixture at 390 px, then WP6 passes. Given the
    fixture at 768 px, then the records are cards in two columns. *(frame check)*
15. **The switch.** Given the fixture at 1359 px, then the records are two-column cards. Given
    the fixture at 1360 px, then the table is shown. WP10 passes. *(frame check)*
16. **Table region.** Given the fixture at 1360 and 1440 px, in Simple and in Advanced, then the
    table is inside a region with `role="region"`, an accessible name and `tabindex="0"`, WP7
    passes, and with the region focused the arrow keys scroll it. *(frame check;
    `workout-plan-desktop-contract.spec.ts`)*
17. **Replacement assertions.** Given `workout-plan-desktop-contract.spec.ts`, then its four
    test titles are unchanged, "page composition and section order" asserts the order of
    criterion 5, the 32 px gutter, no page overflow, that the region scrolls in Advanced and
    that the last column and each row's Remove are reachable, and it no longer asserts 14
    surfaces, three `[data-section]` blocks or page overflow. "progressive column disclosure"
    and "row media and controls" assert the same column lists and counts as today.
    *(Playwright, in `visual-linux`; pytest contract `tests/test_visual_capture_contracts.py`)*
18. **Separators at 3:1.** Given the Plan at 375, 768 and 1440 px in both themes, when
    `visual-field-separator.spec.ts` and "theme surfaces and separator contrast" run, then the
    border they measure is drawn (its width is above 0) and its contrast is at least 3:1. A pass
    on a zero-width border does not count, and the check asserts the width. *(Playwright
    functional)*
19. **Dark theme and accessibility.** Given dark theme, then C8 passes. The axe counts for
    `workout_plan:light`, `workout_plan:dark`, `state:modal-open` and `state:validation-error`
    do not rise for any rule, the `color-contrast` target is 0 in both themes, and every count
    that falls is recorded in `AXE_REGISTER` and in `A11Y_EXCEPTIONS.md`. *(frame check;
    `accessibility.spec.ts`)*
20. **Supersets.** Given the fixture, then both rows of the pair show the rail and the
    "Superset" badge at every width, and no element on the page uses a per-superset colour.
    When a second pair is linked, then it looks the same as the first. *(frame check;
    Playwright functional)*
21. **Editable numbers.** Given a number field in the table or behind Details, then it is a
    field-shaped target reachable by keyboard, and: Enter or leaving saves a changed value once;
    Escape restores the saved value; a blank count reverts with no request; a rejected value
    shows the warning and keeps the saved value; a reload shows the stored value.
    *(Playwright functional)*
22. **Behaviour is unchanged.** Given each row of *Behaviour that must not change*, when the
    action is performed at 390 px and at 1440 px, then the same request with the same payload is
    sent as on `8b023d1a` and the same toast and result follow. Drag to reorder is exercised by
    its handle on a card and in the table. *(Playwright functional; the existing route pytest
    files pass unedited)*
23. **Volume.** Given the fixture, then the volume summary and Volume targets are in the
    exercise list panel's heading row, above the routine tabs' rows, at every width, and
    `volume-progress.spec.ts` passes unedited apart from any selector that follows the markup.
    *(Playwright functional)*
24. **Modal and drawer style.** Given the modal and drawer style check, then it fails on
    `8b023d1a` and passes on the branch, in both themes at 390 and 1440 px. *(Playwright
    computed-style check, committed before the restyle)*
25. **Overrides are gone.** Given the merged change, then WP9 passes, `pages-workout-log.css`
    has no `#clearLogModal` rule and no `!important`, no file adds a `[data-theme` rule for a
    `ui-` class, and the shared `:is()` groups are byte-identical to `8b023d1a`. *(frame check;
    pytest contracts)*
26. **The frame check is general.** Given the frame check, then one documented command runs it
    for the Log and one for the Plan, the Plan's controls fail as listed, two Plan runs give
    identical `metrics.json`, and the Log's run passes with its control still failing.
    *(frame check)*
27. **Other pages do not move.** Given the full visual matrix on both platforms, then every
    capture other than the 26 listed compares clean without regeneration, the runtime bundle
    count is still 18, and the seven-surface Stylelint counts do not rise in any category.
    *(visual capture; pytest contract; Stylelint)*
28. **Evidence.** Given the pull request, then it contains the frame check's command and runs,
    the modal check's control and candidate runs, ordinary (not capture-helper) screenshots of
    the Plan before and after at 390 and 1440 px in both themes, empty and populated, with
    Details open, the More menu open, each modal open and the drawer open, plus 320 and 360 px
    at scale 8, and a `manual-qa-reviewer` comparison of them with the mockup. The paths are
    under `artifacts/design-736/step3/`. *(manual by-eye)*
29. **Documents.** Given the merged change, then `DESIGN_BRIEF.md` and `APP_FLOW.md` describe
    the Plan as shipped, and the PR lists R11–R25 and every accepted assumption under
    "Decisions taken without the owner". *(manual review)*

**Calculation surface**

- `none`.
- The change is presentation only. It does not touch `utils/effective_sets.py`, the volume
  progress calculation behind `/api/volume_progress`, the plan generator, the estimate
  endpoints, any route, the schema, or an API response shape. No worked before/after example
  applies, because no function's output changes.
- The prescription line on a card is composed in the browser from fields `/get_workout_plan`
  already returns. Which tab is selected filters rows already in the page and sends nothing.
- If the plan finds that a requirement needs a calculation, schema or response-shape change, the
  run stops (`RUN_PROMPT.md`, "When to stop") and the change is not made here. Any change to
  core workflow behaviour would need migration notes in the PR description and updated test
  coverage (`CLAUDE.md`, "Refactor invariant").

### Needs more than presentation

**Nothing found.** Each requirement was checked against the routes and modules that own it.

| Requirement | Why it is presentation only |
|---|---|
| R3, opening tab | `workoutPlanState.currentRoutineTabFilter` is in-memory state. Choosing its first value in the browser needs no storage and no request |
| R4, chips | A chip writes an empty value to an existing select and dispatches the `change` event the page already handles |
| R5, More menu | The four controls keep their ids, handlers and targets |
| R6, R7, cards | The same `tr` laid out as a card, as on the Log. The rows are built by `updateWorkoutPlanTable()` from the existing response |
| R8, supersets | Markup and CSS. `supersetRowClasses()` keeps its output |
| R9, modal and drawer | CSS and classes. The drawer's ARIA behaviour is left alone |
| R10, volume position | Two existing elements move in the template |
| R12–R14 | CSS, an accessible name and `tabindex` on a wrapper, and a button around a value that opens the existing editor |
| R16, empty state | Shown and hidden in the browser from the row count. Generate uses today's modal and request |

Two points the plan should confirm, neither of which is a change today:

- Dragging on a routine's tab sends an order for that routine's rows only. That is today's
  behaviour whenever a tab is selected; with R3 it becomes the common case. No request or
  response changes.
- If P8 is accepted, the compiled Bootstrap file is rebuilt. That is a build artifact, not a
  response shape. If the rebuilt file differs outside the drawer's rules, the run stops.

**In scope**

- The Workout Plan page rebuilt on the frame: header and More menu, exercise list panel with the
  volume row, tabs, selection bar, cards and table, the Add exercise panel with collapsed
  filters and chips, and the empty state.
- New shared components in `components.css` and tokens in `tokens.css`: modal, drawer, menu,
  tabs, chip, neutral badge, filled danger button, ruled table and card.
- The shared modal style applied to Generate Starter Plan, Clear Plan, Clear Log and the
  reference-video modal, and the shared drawer style applied to Volume targets.
- Deleting the Plan's page overrides, the Plan-only rules in the shared bundles and the Log's
  modal rules.
- The generalised frame check, the modal and drawer style check, the moved test pins, the 26
  baselines and the documents.

**Out of scope / non-goals**

- Any other route, the navbar and the navigation icons (step 4).
- Motion (step 5). Today's timings and feedback animations stay.
- Replacing the custom dropdowns with native selects, or fixing exceptions X9, X10 and X15.
- The modals of pages that have not migrated.
- New features: remembered routine, per-routine volume totals, exporting visible columns only,
  supersets of more than two, a sort control, a sticky column, a one-click starter plan.
- Changing a label, other than removing emoji from select options and replacing the "SS" badge
  text with "Superset" (R8, R23).
- Changing the value of any existing token, or the shared rules other routes still use.
- Adding the frame check or the modal check to the required CI set.
- Calculation logic, the database schema and API response shapes.

**Assumptions made**

Each is a choice this brief needed and that no D answer, K item or shipped pilot rule settles.
**None of P1–P13 is covered by the owner's reply of 2026-11-26.** No owner answer is recorded
for any of them. The orchestrator settles each under the run prompt's "Decisions and missing
information" order and lists the result in the PR under "Decisions taken without the owner".

- ⚠️ **P1. The opening tab is chosen once, when the page loads.** *Not covered by the owner's
  reply.*
  - You will see: a populated plan opens on the first routine's tab. After that the tab changes
    only when you tap one. Adding, removing, swapping or reordering does not move it.
  - You lose: a plan that was empty when the page loaded stays on All after you add its first
    exercise, until the next visit.
  - Recommendation: accept. It keeps the toast that names a hidden routine meaningful and keeps
    `e2e/workout-plan.spec.ts:329` true.
- ⚠️ **P2. When the selected routine disappears, the page shows All.** *Not covered by the
  owner's reply.*
  - You will see: after you remove a routine's last exercise, or regenerate the plan, the All
    tab is selected. That is what happens today (`workout-plan-table.js:231-239`).
  - You lose: the page does not jump to the next routine's tab.
  - Recommendation: accept. It is today's behaviour and the smaller change.
- ⚠️ **P3. Routine tabs wrap, and each reads workout first.** *Not covered by the owner's
  reply.*
  - You will see: each tab on one line, such as `Workout A · GYM · Full Body 6`, in the order
    the Log's caption uses. When the tabs do not fit one row they continue on the next.
  - You lose: height. Five routines and All take up to six rows on a phone, about 310 px. The
    alternative is one row that scrolls sideways inside itself, which hides the tabs past the
    screen edge.
  - Recommendation: accept wrapping. Every routine stays visible and nothing leaves its
    container.
- ⚠️ **P4. Filter toggle, chips and Clear Filters.** *Not covered by the owner's reply.*
  - You will see: a "Filters" toggle that reads "Filters · 2 active" when two are set, with
    Clear Filters beside it at all times, and under it one chip per active filter reading
    `Equipment: Barbell`. Tapping a chip removes that filter only.
  - You lose: Clear Filters is on screen even when no filter is set, and it still clears the
    routine and exercise selection as it does today, which a chip does not.
  - Recommendation: accept. Clear Filters stays one tap away, and five existing tests click it
    without opening anything.
- ⚠️ **P5. Details on a card.** *Not covered by the owner's reply.*
  - You will see: Details closed on every load, as on the Log. Opened, the six numbers are
    fields three to a row (Sets, Min Rep, Max Rep, then RIR, RPE, Weight) at every card width.
  - You lose: the page does not remember which cards you opened.
  - Recommendation: accept. Three to a row fits a 320 px phone at scale 8 with a five-character
    value by arithmetic (about 62 px a field), with no script deciding the wrap.
- ⚠️ **P6. The superset selection bar stays in view on cards.** *Not covered by the owner's
  reply.*
  - You will see: below 1360 px, while a row is selected, the bar with Link and Unlink stays
    under the navbar as you scroll the list.
  - You lose: about 60 px at the top of the list while a selection exists. Without it you would
    scroll back to the top of the list to press Link after selecting two cards.
  - Recommendation: accept. It is a CSS position, with no new control.
- ⚠️ **P7. Filled buttons in modals, and the filled danger colour.** *Not covered by the
  owner's reply.*
  - You will see: one filled button per modal, the confirm action. Generate Plan is indigo.
    Clear Plan and "Yes, Clear All" are red: `#c0362c` in light and `#a84f49` in dark with white
    text. "Watch on YouTube" becomes an outline button.
  - You lose: the green Generate button and the filled YouTube button. The one-primary rule is
    counted with every overlay closed, so an open modal may show a second filled button.
  - Recommendation: accept. `#a84f49` is today's dark Clear Plan fill, and both values clear
    4.5:1 with white text by hand computation.
- ⚠️ **P8. The drawer's rules move out of the Bootstrap build.** *Not covered by the owner's
  reply.*
  - You will see: nothing different from the shared drawer style D17 already sets. The muscle
    rows keep their status dot with its text label, as D13's default keeps status colours.
  - You lose: nothing on screen. The PR carries a rebuilt `bootstrap.custom.min.css`, and one
    contract pin moves (`tests/test_css_cascade_contracts.py:118-119`).
  - Recommendation: accept, and stop if the rebuilt file differs anywhere outside the drawer's
    rules (the rule K34 sets for Fatigue). The alternative, overriding the old rules from
    `components.css`, adds a layer on top instead of deleting one.
- ⚠️ **P9. K7 reaches the card outline.** *Not covered by the owner's reply.*
  - You will see: below 1360 px each Plan card has a `--ink-3` outline, slightly heavier than
    the Log card's hairline. From 1360 px the table's row lines are `--ink-3`, as K7 says.
  - You lose: Plan and Log cards do not have the same outline.
  - Recommendation: accept. `visual-field-separator.spec.ts` measures the row's own border at
    375 and 768 px, where the row is the card. A hairline there is about 1.29:1 and fails the
    check; a border of zero width would pass on nothing, which weakens the test.
- ⚠️ **P10. The Simple/Advanced toggle is shown above cards too.** *Not covered by the owner's
  reply.*
  - You will see: the same toggle at every width. On cards it decides whether the six
    Advanced-only fields are listed behind Details.
  - You lose: one more control above the cards on a phone. The navbar's muscle-naming toggle
    does the same thing.
  - Recommendation: accept. It is the control K3 keeps, shown in one more layout.
- ⚠️ **P11. Empty-plan copy and "Add first exercise".** *Not covered by the owner's reply.*
  - You will see: "No exercises in your plan yet", a line saying you can generate a starter plan
    or add your first exercise below, and two outline buttons. "Add first exercise" moves focus
    to the Environment select in the Add exercise panel and scrolls it into view. The heading
    row and an All tab with a count of 0 stay above the message.
  - You lose: neither button is filled, because Add Exercise below is the page's one primary.
  - Recommendation: accept. The Volume targets button must stay usable on an empty plan, which
    `e2e/volume-progress.spec.ts` relies on.
- ⚠️ **P12. New copy, the delete icon and small component values.** *Not covered by the owner's
  reply.*
  - You will see: "More", "Add exercise" as the panel's title, "Filters", "Details", "Superset"
    in place of "SS", "Select for superset" beside the checkbox, and "Remove filter: …" as a
    chip's accessible name. One delete icon, `fa-trash`, as the Log uses. A neutral badge
    (`--ink-2` on `--surface-1`), a 12 px radius on the menu's popover, and the selection
    message in the danger, pending or achieved colour by state.
  - You lose: the panel titles "Filter Exercises", "Workout Controls" and "Exercise Selection",
    and the `fa-trash-alt` icon on Clear Plan.
  - Recommendation: accept. The three old titles named panels that no longer exist.
- ⚠️ **P13. Frame-check thresholds come from arithmetic, not a rendered page.** *Not covered by
  the owner's reply.*
  - You will see: checks that hold a closed card to 200 px, the first card to within 600 px of
    the top at 390 px, and the Exercise column to at least 220 px.
  - You lose: nothing. A threshold that the mockup or the built page shows to be wrong is
    corrected before Gate 1 and the correction is recorded.
  - Recommendation: accept, following the pilot's A15. The 220 px figure is the pilot's own.

**Open questions for the user**

None blocks Gate 0. Every open choice is one of P1–P13, is presentation only and can be reversed
inside the step's own PR.

**Could not be verified in this pass**

- **Nothing was run.** No test, script, build or browser was available to this agent. Counts are
  `grep` line counts. The discovery notes' totals for `pages-workout-plan.css` (738 rules, 2,475
  declarations, 489 `!important` declarations) were not re-measured; the 490 here counts lines.
- **Measurements of today's page** (1,606 px at 1440 px, the five left edges, 3,238 px, 3,812 px
  and 9,328 px) come from the discovery notes and the issue. They were not re-measured.
- **The owner's reply** was read from `artifacts/design-736/DECISIONS_REPLY.md`, which records
  it "as given". The comment on #736 was not opened.
- **`8b023d1a` as `origin/main`** comes from the request and the session's git status. No fetch
  was made.
- **Contrast ratios** for `--ui-danger-fill` were computed by hand with the WCAG formula. The
  `--ink-3` figures are the pilot's.
- **Whether `selectOption` fails on a select inside a closed filter panel.** The discovery agent
  did not check it either.
- **The full list of specs that rely on All being selected on load** with more than one routine
  in the plan. Running the Plan specs on the branch establishes it.
- **Which further assertions move** in `tests/test_css_wp4_4_components_contracts.py`,
  `tests/test_css_wp4_4_a11y_contracts.py` and `tests/test_css_wp4_4_motion_contracts.py`, and
  which entries of `pinnedDeclarations` and `contractAnchors` name a deleted rule. Whether the
  baseline's `isFamily` records are compared with the working tree was not read.
- **`tests/test_css_cascade_contracts.py:1396-1410`** and
  **`e2e/superset-edge-cases.spec.ts:501-732`** were read in part.
- **`docs/CSS_OWNERSHIP_MAP.md`** was confirmed to exist and was not read.
- **Which nodes** make up the six light and one dark `color-contrast` findings on the Plan.
- **Drag by the handle on a card grid, with touch,** was read from the code
  (`Sortable.create(tbody, { handle: '.drag-handle' })`) and not exercised.
- **Rendering between 1281 and 1366 px** on today's page, which the discovery agent also left
  unchecked. WP10 covers 1359 and 1360 px on the new page.
- **The mockup does not exist yet**, so no value in this brief has been checked against one.

### Section 0 sign-off — GATE 0

#### Owner's reply, 2026-11-26

Quoted from `artifacts/design-736/DECISIONS_REPLY.md`, which records the reply the owner gave to
the comment "Decisions for the rest of #736 (steps 3, 4 and 5)":

> D2: B. Open on the first routine tab. Keep All available and keep the choice stateless between visits.
> D3: C. Collapse the filters and show each active filter by name as a removable chip.
> For all other questions through D24, I accept the published defaults. This is my Gate 0 reply for steps 3–5. Begin step 3 after #748 merges.

#748 merged as `8b023d1a`, the base of this branch.

#### What the reply covers

| Requirement | Decision | How the reply covers it |
|---|---|---|
| R3 | D2 = B | The owner's own choice and wording |
| R4 | D3 = C | The owner's own choice and wording |
| R2 | D1 = A | Published default, accepted |
| R5 | D4 = B | Published default, accepted |
| R6 | D5 = A | Published default, accepted |
| R7 | D6 = A | Published default, accepted |
| R8 | D7 = B | Published default, accepted |
| R9 | D17 = B, with a style check for the modal added before the restyle | Published default, accepted |
| R10 | D24 = B | Published default, accepted |
| R1, R27 | The frame and the limits | Stated to the owner as "already fixed and not being asked", and set by the owner in `RUN_PROMPT.md` |

#### What the reply does not cover

- **R11–R26** are council-settled choices (K1–K14 and the paragraph after them). The owner was
  told that these choices exist and where they are recorded. The owner did not answer them
  item by item. They are listed in the PR under "Decisions taken without the owner", and an
  owner answer overrides any of them.
- **P1–P13.** No sign-off is recorded for any assumption.
- **The acceptance criteria as written here.** The reply was given before this text existed. It
  fixes the decisions the criteria implement; it does not confirm the criteria.

#### Gate 0 confirmations

- [x] The owner answered the questions that apply to step 3 (D1–D7, D17, D24): two by choice and
  seven by accepting the default, in the reply quoted above.
- [ ] User confirms the acceptance criteria match intent. *(Not given for this text.)*
- [ ] User reviewed the assumptions and corrected or accepted each one. *(Not given. P1–P13 are
  open.)*
- [x] Blocking questions are answered. *(None is open.)*

Gate 1 and Gate 2 for this step are delegated by the owner (2026-11-20) and are recorded in this
file when given, as "approved by Claude under the owner's delegation of 2026-11-20". Merging
this step's PR needs the owner's authorization in the message that starts or resumes the session.
