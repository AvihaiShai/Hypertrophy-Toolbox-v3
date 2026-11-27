# Plan Review — Workout Plan redesign (#736 step 3)

**Status** — Section 0 drafted on 2026-11-27. The owner's "Decisions" reply of 2026-11-26 is
the Gate 0 answer for the decisions it names (see
[Section 0 sign-off](#section-0-sign-off--gate-0)). Thirteen assumptions (P1–P13) are not
covered by that reply and carry no owner sign-off. The plan council reviewed Plan v1 on
2026-11-27: three verdicts of "sound with changes", no blocking finding, and every finding has a
disposition. It settled P1–P13 without the owner, and an owner answer overrides any of them.
Plan v2 is written. Gate 1 is recorded as approved by Claude under the owner's delegation of
2026-11-20 (see [Sign-off](#sign-off)). Implementation has not started.

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

The mockup page is [`mockup.html`](mockup.html), committed beside this file. It is a static
page that links the shipped `tokens.css`, `layout.css` and `components.css` and carries the new
components in its own `<style>`. It shows the same content at every width: the fixture under
*Fixture for the Plan*. States are reached by query string, for example
`mockup.html?theme=dark&state=all&details=squat&zoom=1.2`. Its captures and measurements are
under `artifacts/design-736/step3/mockups/` (not committed), built on 2026-11-27.

| Capture | Shows |
|---|---|
| `populated-{390,768,1440}-{light,dark}.png` | The populated plan on the first routine's tab: one-column cards, two-column cards, the table |
| `populated-1359-light.png`, `populated-1360-light.png` | The switch from cards to the table |
| `all-tab-{390,1440}-light.png` | The All tab |
| `empty-{390,1440}-light.png` | The empty plan |
| `details-open-390-light.png` | A card with Details open |
| `row-selected-{390,1440}-light.png` | The superset selection bar |
| `filters-open-chips-{390,1440}-light.png`, `filters-collapsed-chips-390-light.png` | Filters open and collapsed, with two active chips |
| `more-menu-open-{390,1440}-{light,dark}.png` | The More menu |
| `clear-plan-modal-*.png`, `generate-modal-{390,1440}-light.png` | The shared modal style |
| `volume-drawer-*.png` | The shared drawer style |
| `advanced-1440-light.png` | The table in Advanced |
| `zoom1.2-*-{320,360,390}-light.png` | Narrow phones at app scale 8, with Details open on the Squat and Deadlift cards and with a row selected |
| `measurements.json` | The numbers below, and edges, tap targets and overflow at every captured width |

**The mockup against this brief** (measured from the mockup, not from a built page):

- The three P13 thresholds hold: a closed card with a one-line name is 150 px (limit 200), the
  first card starts 581 px from the top at 390 px (limit 600), and the Exercise column is 222 to
  228 px (minimum 220).
- No page-level sideways scroll at 320, 360, 390, 768, 1359, 1360 or 1440 px, at scale 6 or 8.
  The smallest tap target at 320, 360 and 390 px is 44 × 44 px.
- At 1360 px the Simple table scrolls 74 px inside its region. It fits at 1440 px.

**Where the mockup departs from the text of this brief.** The plan council rules on each. It
accepted all four on 2026-11-27 (response matrix, M1–M4):

- P5 says three fields to a row behind Details. On the narrowest cards (320 to 390 px at scale 8)
  `102.5` does not fit a third of the row, so the mockup shows two to a row there and three
  everywhere wider.
- "One line per tab": a routine name longer than the row wraps inside its tab.
- The More popover is anchored to the actions row, not to the More button. Anchored to the button
  it ran off-screen at 320 px at scale 8, where More wraps to the left.
- The mockup draws the cards and the table as two lists and uses native selects. The built page
  keeps one `tr` per record and the `.wpdd` dropdowns.

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
| **Menu** ⚠️ (P12) | "More" | A secondary `ui-btn` labelled "More" with a chevron, `aria-haspopup="menu"` and `aria-expanded`. The popover is a raised surface: `--surface-2`, 1 px hairline, 12 px radius, `--shadow-elev-2`, at least 200 px wide, aligned to the right edge of the actions row and never outside the viewport (corrected 2026-11-27 under M3; the draft said the button's right edge). Items are 40 px tall (44 px below 768 px) with 14 / 20 px text. The destructive item uses `--ui-danger` text and sits below a hairline |
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
  Weight. ⚠️ Three to a row, and two to a row where the card's content box is narrower than
  240 px (P5; corrected 2026-11-27 under M1).
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
| `scss/pages/_workout_plan_volume_panel.scss` | Not edited in this step (corrected 2026-11-27: the council changed P8). The drawer's old rules stay in the Bootstrap build underneath the shared drawer's rules and are named for a later deletion. The Volume Splitter rules in the same file stay until step 4 |

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
| `e2e/workout-plan-desktop-contract.spec.ts:353-397` | Its existing assertions and its skip of a `0px` edge stay. It gains one new assertion that the `td` bottom border has a width above 0 (criterion 18; corrected 2026-11-27 under Q3, where the draft said "stays as written") |
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
| `tests/test_css_cascade_contracts.py::test_bootstrap_artifact_keeps_scss_owned_selector_families` (`:106-121`) | Requires `.vp-drawer` and `#vpToggle` in the compiled Bootstrap file. Does not move: the council changed P8 on 2026-11-27 and the SCSS is not edited |
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
- ⚠️ **P3. Routine tabs wrap, and each keeps today's label order.** *Not covered by the owner's
  reply.* (Corrected 2026-11-27: the draft read workout first, as the Log's caption does. The
  council changed it, because R23 keeps labels as they are.)
  - You will see: each tab on one line, reading environment, program, workout as today, with
    its count. When the tabs do not fit one row they continue on the next.
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
    fields three to a row (Sets, Min Rep, Max Rep, then RIR, RPE, Weight), and two to a row
    where the card's content box is narrower than 240 px, which is 320 to 390 px at scale 8.
  - You lose: the page does not remember which cards you opened.
  - Recommendation: accept. A layout rule decides the wrap, not a script. (Corrected 2026-11-27
    under M1. The draft said three to a row fits a 320 px phone at scale 8 at about 62 px a
    field. That figure left out the panel's padding: a field is about 50 px there, too narrow
    for `102.5`.)
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
  - Changed by the council on 2026-11-27, two reviewers to one: the alternative is used. The
    SCSS is not edited, nothing is rebuilt and no pin moves. The mechanism is in Plan v2.
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
- **No value in this brief has been checked against a built page.** The mockup was built after
  this list was written. Its measurements are under *Mockups* and come from the mockup alone.

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

**Status of the two open boxes, recorded 2026-11-27.** This is a status note, not an owner
statement.

- The owner's "Decisions" reply of 2026-11-26, quoted above, is the Gate 0 answer for steps 3 to
  5: "This is my Gate 0 reply for steps 3–5". The questions were put to the owner to be answered
  once (`artifacts/design-736/DECISIONS_FOR_ASTRA.md:3`).
- As the orchestrating session reports it, the owner's instruction of 2026-11-25 for this run is
  that decisions come once as a batch. Later questions go to the council and `/consult`, then to
  the orchestrator's judgment, preferring the smaller and more reversible option, and are listed
  in the PR under "Decisions taken without the owner". This agent did not read that instruction
  itself.
- P1–P13, M1–M4 and Q1–Q12 were settled that way by the plan council on 2026-11-27 (see the
  response matrix). The owner has not reviewed them. An owner answer overrides any of them.
- The two boxes stay unticked because the owner has not confirmed this text or these
  assumptions.

Gate 1 and Gate 2 for this step are delegated by the owner (2026-11-20) and are recorded in this
file when given, as "approved by Claude under the owner's delegation of 2026-11-20". Merging
this step's PR needs the owner's authorization in the message that starts or resumes the session.

---

## Plan v1

Drafted 2026-11-27 on `feat/736-workout-plan` at `0573f1f5`. Section 0 is the requirements text
and is not restated here. This pass had no shell, so nothing was run: each statement about a file
comes from opening it at this head, and each count is a text-search line count. *Not verified*
marks what was not opened or cannot be settled by reading; the list is at the end.

**Goal** — A lifter opens Workout Plan on the routine they are about to train, reads and edits
each exercise on a card on a phone or in a contained table on a desktop, and adds an exercise from
one panel, on the frame and components the Workout Log already uses.

**No calculation, schema or response-shape change** (checked against the code; no stop condition
was found)

- No file under `routes/` or `utils/`, and not `app.py`, is in the artifact list. No table or
  column changes.
- No payload builder is edited: `buildExecutionStylePayload`, `buildAddExercisePayload`,
  `buildFieldUpdatePayload`, `buildReplacePayload`, `buildSupersetLinkPayload`,
  `buildSupersetUnlinkPayload` and `buildExerciseOrderPayload`
  (`static/js/modules/workout-plan-helpers.js:148-190`).
- The opening tab is a value of `workoutPlanState.currentRoutineTabFilter`.
  `applyRoutineTabFilter()` (`workout-plan-helpers.js:102-107`) filters rows already fetched and
  sends nothing. The prescription line is composed from fields the row already prints
  (`workout-plan-table.js:413-418`).
- Two consequences, both today's behaviour. A drag on a routine's tab posts the order of that
  tab's rows only, because the payload is built from the rows in the `tbody`
  (`workout-plan-table.js:701-702`). If P8 stands, `static/css/bootstrap.custom.min.css` is
  rebuilt, which is build output.

**Scope**

- **In** — Everything under *In scope* in Section 0: the page on the frame, the new shared
  components (modal, drawer, menu, tabs, chip, neutral badge, filled danger button, ruled table
  and card), the four modals and the drawer, the deletions, the generalised frame check, the
  modal and drawer check, the moved pins, the 26 baselines and the documents.
- **Out** — Everything under *Out of scope* in Section 0. In addition this plan does not edit
  `templates/base.html`, `playwright.config.ts`, `.github/workflows/**`, `scripts/**`,
  `e2e/visual.spec.ts`, `e2e/visual-baseline-thumbnails.spec.ts` or `e2e/visual-helpers.ts`
  (question Q4), and adds no spec file to the required set, which stays at 25
  (`tests/test_playwright_shard_launcher_contracts.py:67`).

**Artifacts — production** (writer: `senior-developer`)

| Path | Change | What changes |
|---|---|---|
| `templates/workout_plan.html` | rewrite | Sets `main_class` to `ui-page-frame` (the block is at `templates/base.html:228`). Keeps `#workout[data-page="workout-plan"]` and every id under *Hooks that stay*. Order: `header.ui-page-header`, the list `section.ui-panel`, the Add exercise `section.ui-panel`. Drops the three `.collapsible-frame` blocks, every `[data-section]`, `[data-visual-header]`, `[data-visual-accent]` and page-content `[data-visual-surface]`, the classes `frame-calm-glass`, `btn`, `btn-*`, `form-control`, `input-calm-inset`, `table`, `table-striped`, `table-calm`, `tbl` and `tbl--responsive`, the inline `width: 1600px` (`:372`), the emoji in options (`:165-166`, `:397-398`, `:412-414`) and `fa-trash-alt` (`:278`, `:569`, `:580`). The table keeps `data-table-responsive="workout_plan"`, `data-testid="exercise-table"`, `.workout-plan-table` and its 22 `th[data-label]`, and gains `ui-data-table ui-data-table--ruled` |
| `templates/workout_log.html` | modify | `#clearLogModal` only (`:142-168`): `ui-modal`, plain header, `ui-btn` buttons. Ids unchanged |
| `templates/partials/exercise_video_modal.html` | modify | `ui-modal`. "Watch on YouTube" becomes a secondary `ui-btn`. Ids unchanged |
| `static/css/tokens.css` | add | `--ui-modal-radius` and `--ui-danger-fill` in the existing `--ui-*` blocks (`:479-504`). No existing token changes |
| `static/css/components.css` | add, edit one rule, delete | **Added** after `:5091`, outside every `@layer`: `.ui-btn--danger-fill`, `.ui-btn[aria-pressed="true"]`, `.ui-badge--neutral`, `.ui-chip`, `.ui-tabs` and `.ui-tab`, `.ui-menu` with `__popover`, `__item` and `__sep`, `.ui-data-table--ruled`, `.ui-record-card--ruled`, `.ui-modal` (surface, header, title, close, body, footer, `--confirm` and `--wide` widths), `.ui-drawer` (shell, header, close, body, open state, backdrop). **Edited:** the unscoped `.modal-content { box-shadow … !important }` at `:2238-2240` is narrowed so it stops applying to `.ui-modal` (Q1). **Deleted:** rules that name only the Plan and no longer match, including the five `#generatePlanModal` rules at `:2335-2353` and the four input rules Section 0 places at `:3454-3569`. The shared `:is()` groups are not edited. `!important` falls from 883; none is added |
| `static/css/layout.css` | delete | The `.tbl-view-mode-toggle` chrome at `:1609-1665` (Q2). `.tbl-controls` (`:1581-1601`), the print rule and the view-mode column rule (`:1673-1686`) stay. Section 0 expected no change to this file |
| `static/css/theme-dark.css` | delete | The Plan-only per-field input rules at `:437-531` (24 selector lines) and the `.tbl-view-mode-toggle` dark rules at `:199-220` (Q2) |
| `static/css/pages-workout-plan.css` | delete, rewrite | The families Section 0 lists under *What is deleted*. New Plan-only layout: the card grid on `tr`, column widths, the heading row, the Add exercise grid, the superset rail, the drawer's rows. `!important` falls from 490 lines to at most 65, Section 0's ceiling. The families that stay hold 26 such lines today by Section 0's table (4 + 3 + 2 + 2 + 15), so the expected end is 26 or fewer. The measured figure is pinned as an upper bound. None is added |
| `static/css/pages-workout-log.css` | delete | The 12 `#clearLogModal` rules (`:4-59`), which hold all 10 of the file's `!important` lines (Q8) |
| `scss/pages/_workout_plan_volume_panel.scss`, `static/css/bootstrap.custom.min.css` and its `.map` | modify, rebuild | Only if P8 stands. The `.vp-*` and `#vpToggle` rules go. `.volume-active-summary`, `.volume-history-section` and `.activate-plan` stay, including where they share a selector list with a `.vp-` selector (`:1-2`, `:11-12`, `:22-23`, `:218-219`, `:225-226`, `:294-296`) |
| `static/js/modules/workout-plan.js`, `workout-plan-table.js`, `workout-plan-helpers.js`, `workout-plan-supersets.js`, `workout-plan-page.js`, `workout-plan-media.js`, `workout-plan-execution-style.js`, `filters.js` | modify | See *JavaScript changes* |
| `static/js/modules/ui-menu.js` | new | The shared menu behaviour |
| `static/js/table-responsiveness.js` | modify | One line: the toggle it creates (`:239`) also carries `ui-btn ui-btn--small` (Q2) |

**Artifacts — tests** (writer: `automation-qa`, `tests/**` and `e2e/**` only)

| Path | Change | What changes |
|---|---|---|
| `e2e/frame-check.ts` | new | Shared helper, not a spec: theme and scale setup, the C1–C5 population read, the C8 source scan, a one-pass box reader, a mutation recorder |
| `e2e/workout-plan-frame.check.ts` | new | The Plan's fixture, matrix and WP6–WP12 |
| `e2e/overlay-style.check.ts`, `e2e/overlay-style.reference.json` | new | The modal and drawer check, and the values the four unmigrated modals compute on `8b023d1a` |
| `e2e/workout-log-frame.check.ts` | modify | Uses the helper. Its checks and its control keep their coverage |
| `e2e/scripts/run_frame_check.py`, `e2e/playwright.frame.config.ts` | new | The launcher and config for any registered route |
| `e2e/scripts/run_workout_log_frame.py`, `e2e/playwright.workout-log-frame.config.ts` | modify | Reduced to shims, so the Log's documented command still works (Q6) |
| `tests/test_workout_log_frame_runner.py` | modify | Imports the new launcher. Keeps its three path guards and gains the route cases |
| `e2e/workout-plan.spec.ts`, `exercise-interactions.spec.ts`, `superset-edge-cases.spec.ts`, `empty-states.spec.ts`, `error-handling.spec.ts`, `accessibility.spec.ts`, `ui-hardening.spec.ts`, `program-backup.spec.ts`, `dark-mode.spec.ts` | modify | The pins Section 0 lists, and the new functional cases below. No spec file is added |
| `e2e/workout-plan-desktop-contract.spec.ts`, `e2e/visual-field-separator.spec.ts` | modify | Criteria 17 and 18 (Q3) |
| `tests/test_css_cascade_contracts.py` | modify | `:239-242`; the ten `test_workout_plan_*` tests, each retargeted in its own slot to assert that its retired family is absent and that what survives is present; `:114-121` only if P8 stands |
| `tests/test_css_wp4_4_i_is_repair_contracts.py` (`:112`, `:215`, `:226`), `tests/test_css_wp4_4_components_contracts.py` (`:385`, `:448-449`), `tests/test_css_wp4_4_a_baseline_contracts.py` (`:157`, `:175-205`), `tests/test_template_landmarks.py` (`:15`) | modify | Measured replacements. `!important` counts may only fall |

**Artifacts — documents and baselines**

| Path | Change | Writer |
|---|---|---|
| `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` | Hand-edit of the affected entries only, with values read from `scripts/css_audit/measure.py`, never typed from memory and never with `emit_baseline.py` (Q7) | `automation-qa` |
| `docs/test_inventory/` | Regenerated with `scripts/generate_test_inventory.py` | orchestrator |
| `docs/product/DESIGN_BRIEF.md`, `docs/product/APP_FLOW.md` (the Plan section starts at `:281`), `docs/CSS_OWNERSHIP_MAP.md`, `docs/testing_phase2/A11Y_EXCEPTIONS.md` | The rules that shipped | `senior-developer` |
| `docs/workout_plan_redesign/PLANNING.md` | Council sections, delegated approvals, evidence rounds | `product-manager` |
| 26 PNG files under `e2e/__screenshots__/` | See *Visual baselines* | orchestrator |

**Effort** — L · **Owner** — Claude (orchestrator), under `RUN_PROMPT.md` approval 1 ·
**Depends on** — #748, merged as `8b023d1a`, the base of this branch. The orchestrator settles
P1–P13 under the run prompt's "Decisions and missing information" order before Gate 1.

### Sequence

One writer at a time. The orchestrator commits and pushes; no agent commits. A pin that a commit
breaks moves in that commit, so `automation-qa` follows `senior-developer` before commits 3 to 5.

| # | Commit | Writer | State after the commit |
|---|---|---|---|
| 1 | Generalise the frame check | `automation-qa` | The Log run passes twice with byte-identical `metrics.json`. Its control at `5dc83cef` still fails C1–C4 and C10. pytest is green |
| 2 | Acceptance tests, red: the Plan frame check, the modal and drawer check, and the new functional cases | `automation-qa` | Red by design, on a page that is still `8b023d1a`'s. Both checks fail on this head, and `--control-ref 8b023d1a` passes in control mode: the Plan fails C1, C2, C3, C4, C5 and WP10, the migrated overlays fail their pinned values, and the four unmigrated modals equal the reference file. Each new functional case fails for the reason it tests, and the list of red cases is recorded in this file's evidence round. No existing test is edited in this commit |
| 3 | Shared components and tokens | `senior-developer`, then `automation-qa` for the line-count and ledger pins | Additive apart from Q1. No page changes. The full visual matrix compares clean with no regeneration. The red list is unchanged |
| 4 | Template and scripts | `senior-developer`, then `automation-qa` for the pins Section 0 lists as following the markup | The functional specs and Vitest are green, including every case that was red since commit 2. The Plan frame check may still fail where a legacy rule reaches the new markup (Q9) |
| 5 | Deletions | `senior-developer`, then `automation-qa` for the cascade tests and the ledger | Both checks pass. Two Plan runs give byte-identical `metrics.json`. WP9 is measured |
| 6 | Pins and documents | `automation-qa` for `AXE_REGISTER`; `senior-developer` for the documents; orchestrator for the inventory | Full pytest, full Chromium, Stylelint, tsc, pyright and Vitest are green. The three visual specs are red only on the 26 listed captures |
| 7 | Baselines | orchestrator, after the `manual-qa-reviewer` comparison | The three visual specs are green on both platforms. Only the 26 files and four digests moved |

Commits 2 and 3 carry red cases in required specs. The pull request is opened after commit 6, so
its CI first runs on a head where those cases are green. The other order, in which the
new cases are written first but committed with commit 4, keeps every commit green and loses the
committed red-before record; the council may prefer it. The test inventory is regenerated in each
commit that adds, removes or renames a test. The `DESIGN_BRIEF.md` entries for the tokens and
components ship in commit 3, and its description of the Plan in commit 6.

### Layout by construction

The pilot was held for a five-field card that left a 320 px phone at scale 8, and its fix was a
script that measured cards after first paint. The Plan uses no script to decide layout.

| Need | Rule |
|---|---|
| One record, two layouts | One `tr` per record. Below 1360 px `tbody` is a grid (one column, two from 768 px) and each `tr` is a grid whose cells are placed by `grid-area`. No node is moved in the DOM, so the pilot's reorder after first paint has no counterpart |
| Closed card | The cells outside the closed set are `display: none` until the row has `details-open` |
| Field labels on cards | `td::before { content: attr(data-label) }`. The cell's text stays the bare value, which the editor reads from `textContent` (`workout-plan-table.js:532`) |
| Six numbers behind Details | The row grid has six equal `minmax(0, 1fr)` tracks. A number cell spans two (three to a row). Inside `@container (max-width: 239px)` on the row it spans three (two to a row), as `mockup.html:115-119` does |
| 44 px targets at scale 8 | `min-height: 44px`, and for widths the pilot's rule at `static/css/pages-workout-log.css:138` |
| Nothing wider than its box | `min-width: 0` on every grid and flex child. `overflow-wrap: anywhere` on names, captions, tab labels, chips and the prescription line. `flex-wrap: wrap` on the header actions, heading row, tabs, chips, selection bar and card actions. No `white-space: nowrap` below 1360 px |
| Menu inside the viewport | The popover is positioned against `.ui-page-actions` with `right: 0` and `max-width: 100%` (`mockup.html:42-44`) |
| Table region | `.tbl-wrap` stays as a wrapper that does not scroll and holds `.tbl-controls`. A child `div[role="region"][aria-label][tabindex="0"]` holds the table and takes the shared rule at `components.css:5077`. `table-responsiveness.js` finds its wrapper with `closest('.tbl-wrap')` (`:190`) and is not edited for this |
| Columns from 1360 px | Fixed widths per `data-label`. Without `tbl` and `tbl--responsive` no container query hides a column; only `tbl--view-simple` does (`layout.css:1673-1686`), and it also hides the six Advanced-only fields on cards |
| Separators | The ruled variant draws a 1 px `--ink-3` `border-bottom` on `tbody td` from 1360 px and a 1 px `--ink-3` outline on `tbody tr` below it. Both are keyed on the table, not on a row class (Q3) |

**Where script is unavoidable, and how the first paint stays correct**

- **Rows arrive by request**, as today (`fetchWorkoutPlan()`, `workout-plan.js:90-117`). The
  list starts as `data-plan-state="loading"`, which shows neither the empty panel nor a record.
  In one synchronous block the script chooses the opening tab, builds the tabs, renders the rows
  with their card markup already in place and sets the state to `populated` or `empty`. The All
  tab is therefore never painted as selected on a populated plan, and the empty panel is never
  painted over a plan that has rows.
- **The Simple/Advanced toggle is created at `DOMContentLoaded`** (`table-responsiveness.js:423-452`).
  The template ships an empty `.tbl-controls` inside `.tbl-wrap` with the toggle's height
  reserved; the script reuses it (`:99`).
- **Chips** are drawn on a `change` event, and once at start for a value the browser restored.
- **Check.** The frame check installs a `MutationObserver` before navigation. From the first row
  insertion to the settled page it must see one child-list batch on `#workout_plan_table_body`,
  no attribute change on any row, and no change of `aria-selected` in `#routine-tabs`. It runs at
  320 px at scale 8 and at 1440 px.
- **No flaky reads.** Every comparison of two positions reads both in one `evaluate`, after the
  page reports its state and `scrollTo(0, 0)`. Nothing is read straight after `reload()`. The
  pilot's race came from two reads in two calls.

### JavaScript changes

Each row keeps the request, payload, toast and result of the *Behaviour that must not change*
entry it names.

| Module | Change | Stays | Listeners |
|---|---|---|---|
| `workout-plan.js` | `fetchWorkoutPlan()` chooses the opening tab on the first successful response, before `updateRoutineTabs()`: the first routine by `compareRoutines()`, or `all` for an empty plan. It sets `data-plan-state` and shows or hides the empty panel. The once-per-load flag is module-private | `GET /get_workout_plan`. The four keys of `workoutPlanState` and its default `'all'`, pinned by `__tests__/workout-plan-state.test.js:7-13`. Plan load and refresh | None added |
| `workout-plan-table.js` | The row template (`:379-430`) emits the card markup: `ui-record-card`; a `button.ui-field` around each of the six values; a prescription line, the "Superset" badge and a Details button in the Exercise cell; a `label` around the superset checkbox; Remove as `ui-btn ui-btn--danger ui-btn--small` with `data-action="delete"` and its `onclick="removeExercise(id)"`. Tabs keep `li.routine-tab > button.routine-tab-btn[data-routine]` and gain `ui-tab`. `makeTableCellEditable()` reads and writes the value button, gives its input `ui-field-input` in place of the classes at `:536`, refreshes the prescription line after a save and returns focus to the value button unless the user moved it | Every row hook under *Hooks that stay*. `supersetRowClasses()` output and `workoutPlanState.supersetColorMap`. The `superset-group-N` classes stay on rows and no rule colours them. `POST /update_exercise`, `POST /update_exercise_order`, `Sortable.create(tbody, { handle: '.drag-handle' })`. Inline edit, drag, Remove | One delegated `click` listener on `#workout_plan_table_body` for Details, bound once at start. The per-cell, swap, checkbox and style listeners are bound per row as today |
| `workout-plan-helpers.js` | `formatRoutineForTab()` (`:82-87`) emits workout, environment, program if P3 stands. `renderExecutionStyleBadge()` (`:143`) drops `btn` and adds `badge ui-badge ui-badge--neutral` | `formatRoutineForDisplay()`, pinned exactly at `__tests__/workout-plan-seams.test.js:45`; the card caption reorders its three spans in CSS. The cases at `:51-54` and `:73-77` use `toContain` and hold unedited. No Vitest case is added, removed or renamed | None |
| `workout-plan-supersets.js` | The selection message's state moves from the inline `var(--wp-bad)`, `var(--wp-warn)` and `var(--wp-good)` colours (`:113`, `:119`, `:125`, `:132`) to a `data-state` attribute styled with `--ui-danger`, `--ui-pending` and `--ui-achieved` | The message texts. `style.display` on `#superset-actions` (`:74`, `:78`). `POST /api/superset/link` and `/unlink`. Superset select, link and unlink | None added |
| `filters.js` | A chip renderer, called from the existing delegated `change` handler on `#workout` (`:102-119`), at the end of `clearFilters()` and once in `initializeFilters()`. Removing a chip sets that select to `''` and dispatches `change`. The filters toggle sets `hidden` on the grid, `aria-expanded` and its count | `clearFilters()` (`:161-256`) is otherwise unedited. `#filters-form` and `select.filter-dropdown[data-filter-key]`. A removed chip reaches the server through the existing debounce, so it sends one request. The renderer sends none, so one `/get_all_exercises` request per load holds | One delegated `click` on the chip list and one on the toggle. None on `#routine` |
| `ui-menu.js`, called from `workout-plan-page.js` | Opens on click, Enter, Space and ArrowDown; arrows move between items; Escape closes and focuses the button; a click outside closes. An item that opens a modal closes the menu first, and a one-shot `hidden.bs.modal` listener returns focus to the More button | The four controls keep their ids, `onclick`, `href` and `data-bs-*` attributes, so each does what it does today. Export, Backup Center, Generate Starter Plan, Clear Plan | Per menu: two on the button and two on the popover. One `click` on `document` |
| `workout-plan-page.js` | The collapsible-frame block (`:199-256`) goes with its markup. "Add first exercise" focuses the first control of the Add exercise panel and scrolls it into view (P11) | The generator form wiring (`:110-197`) and the muscle-filter rebuild (`:30-107`). Generate Starter Plan | One `click` |
| `workout-plan-media.js` | `appendExerciseVideoButton()` (`:23-32`) gives the Plan's button `ui-btn ui-btn--ghost`. The shared builder (`exercise-video-modal.js:134-140`) is not edited | `.btn-video`, `[data-action="play-video"]`, `img.exercise-thumbnail` with `width="32"` and `height="32"`. Reference video and thumbnail preview | None |
| `workout-plan-execution-style.js` | The picker drops `frame-calm-glass` (`:76`) | `.execution-style-picker` and its requests. Execution style | None |
| `table-responsiveness.js` | The class at `:239` (Q2) | Everything else. Simple/Advanced | None |
| `plan_volume_panel.js`, `routine-cascade.js`, `exports.js`, `exercises.js`, the estimate and persistence modules | None | `vpDrawer.open` in `localStorage` (`plan_volume_panel.js:3`) and the move of the drawer to `body` (`:36-45`) | None |

`e2e/exercise-catalog-fetch.spec.ts` (two tests, at `:42` and `:69`) is run unedited as the
control for the one-request and one-listener contracts. It is outside the required set.

### The generalised frame check (R21)

**Files and commands.** `e2e/scripts/run_frame_check.py` holds a registry and everything the
Log's launcher does today: the scratch-path guard (`run_workout_log_frame.py:22-26`), the server
entry that refuses a wrong database, runtime or source (`:80-103`), the free loopback port
(`:127-129`) and the `git archive` export for a control (`:119-125`). Each run gets a new
directory under `artifacts/frame-check/<route>/`.

```powershell
.venv/Scripts/python.exe e2e/scripts/run_frame_check.py --route workout_plan
.venv/Scripts/python.exe e2e/scripts/run_frame_check.py --route workout_plan --control-ref 8b023d1a
.venv/Scripts/python.exe e2e/scripts/run_frame_check.py --route overlays
.venv/Scripts/python.exe e2e/scripts/run_workout_log_frame.py
```

| Route key | Check file | Control | Fixture |
|---|---|---|---|
| `workout_log` | `e2e/workout-log-frame.check.ts` | `5dc83cef` | Today's seven-record edits, unchanged |
| `workout_plan` | `e2e/workout-plan-frame.check.ts` | `8b023d1a` | Section 0's seven edits |
| `overlays` | `e2e/overlay-style.check.ts` | `8b023d1a` | The Plan fixture. `#clearLogModal` is in the Log's template whether or not the log has rows (`templates/workout_log.html:142`). The unmigrated four are on `/`, `/progression` and `/volume_splitter` |

- **Route selection.** `--route` picks the row. `--control-ref` accepts only that row's control,
  as `choices=[CONTROL]` does today (`:108`). The launcher passes the check file to
  `e2e/playwright.frame.config.ts`, which sets `testMatch` from it and otherwise equals the
  current config: one worker, no retries, its own server, `reuseExistingServer: false`. An
  unknown route, or a route without a control, is refused before any seeding.
- **Shared part.** `e2e/frame-check.ts` reads the C1–C4 population in one `evaluate`, as
  `measure()` does (`workout-log-frame.check.ts:825-885`), with the frame selectors passed in by
  the route. It evaluates C1–C5 on the entries and runs the C8 scan with PostCSS (`:1026-1031`).
  The Log's file keeps its own extras: C6, C7, C9, C10 and the pilot's editing journey.
- **The Plan's fixture.** The launcher copies the committed visual seed with
  `prepare_visual_db.py` and writes nothing else. The check applies Section 0's seven edits
  through the page's own endpoints (`/add_exercise`, `/update_exercise`, `/api/superset/link`,
  `/api/execution_style`), asserts each response, and compares `/get_workout_plan` with an
  expected list before measuring. A failed setup is an error, not a failed check. The same steps
  run against the control export, because the endpoints are identical there. The empty passes
  follow `POST /clear_workout_plan`.
- **Exemptions.** The Plan's check starts with an empty named list. Any entry needs a reason in
  the file and a row in the PR.
- **pytest.** `tests/test_workout_log_frame_runner.py` keeps its three refusals (live database,
  external database, runtime outside the run) and its positive control, parametrised over the
  routes, and adds a refusal of an unknown route and of another route's control ref. The
  inventory moves and is regenerated.

### How each criterion is verified

**Frame** is `workout-plan-frame.check.ts`. **Overlay** is `overlay-style.check.ts`. **Plan spec**
means `e2e/workout-plan.spec.ts`, with `exercise-interactions.spec.ts` and
`superset-edge-cases.spec.ts` where the behaviour already lives. The functional lane runs at
1440 × 900 (`playwright.config.ts:90`), so every card case sets its own viewport.

| Criteria and rows | Check | Control that shows it can fail |
|---|---|---|
| 1, 2, 3 — C1, C2, C3, C4, C5 | Frame, over Section 0's matrix: three widths, both themes, empty and populated, the scale 8 passes, 320 and 360 px, 1359 and 1360 px, Simple and Advanced, the opening tab and All | `8b023d1a` fails all five |
| 4 | Frame counts visible `.ui-btn--primary` in `#main-content`, and separately every button whose computed fill is `--ui-primary` or a red fill. Plan spec pins it empty and populated | `8b023d1a` has four filled primaries and a filled red Remove |
| 5 | Frame reads the tops of the header and the two panels in one pass, and the first card's top at 390 px. A pytest contract reads the same order from the template source | Red before commit 4; `8b023d1a` |
| 6, 7 | Plan spec. A plan with two routines is created, then the page is opened: the first routine's tab is selected and only its rows are listed. All is activated by pointer and by keyboard. After a reload the first tab is selected again. `localStorage`, `sessionStorage` and `document.cookie` are compared key by key before and after | Red before commit 4: today the page opens on All |
| 8 | Plan spec and `empty-states.spec.ts`: the panel, no `tr`, All selected, summary and Volume targets visible, the modal from the panel's button, focus after "Add first exercise" | Red before commit 4 |
| 9 | Plan spec: toggle closed and 12 selects hidden on load; two chips by filter name and value; one removed, with the request counted by `page.on('request')`; Clear Filters and its toast | Red before commit 4 |
| 10 — WP12 | `accessibility.spec.ts` for the keyboard path and focus return. Frame for WP12 with the menu open at 390 and 1440 px in both themes | Red before commit 4. Mutation: anchor the popover to the button and WP12 fails at 320 px at scale 8 |
| 11, 12, 14 — WP6 | Frame at 390 and 768 px. Plan spec for Details by touch and keyboard, in Simple and Advanced, closed after a reload | `8b023d1a` has no card and no Details |
| 13 — WP11 | Frame at 320, 360 and 390 px at scale 8 and 320 px at scale 6, with Details closed, open on Squat and Deadlift, and with a row selected. Plan spec carries a required regression case at the three widths at scale 8 | Mutation: remove the container rule and the Squat card fails at 320 px at scale 8 |
| 15 — WP10 | Frame at 1359 and 1360 px | `8b023d1a` fails WP10 |
| 16 — WP7 | Frame at 1360 and 1440 px, Simple and Advanced: one pass reads the region and every row's Remove after `scrollLeft` is set to its end, and `elementFromPoint` at each Remove's centre. Arrow keys on the focused region change `scrollLeft` | Mutation: `overflow: hidden` on the region fails the Remove read |
| 17 | `workout-plan-desktop-contract.spec.ts`, in `visual-linux` and locally with `PW_VISUAL_SEED=1`. The four titles and `width: 1440` stay (`tests/test_visual_capture_contracts.py:250-256`). The column lists (`:47-66`) and row counts (`:265-269`, `:297-317`) are not edited | Red before commit 4: the rewritten composition test fails on three `[data-section]` blocks and on page overflow |
| 18 | `visual-field-separator.spec.ts` and the contract's fourth test. Both gain an assertion that the border they measure has a width above 0 (Q3) | Mutation: set the ruled border to the hairline and it fails at about 1.29:1; set it to 0 and the width assertion fails |
| 19 — C8 | Frame for C8. `accessibility.spec.ts`: the four `AXE_REGISTER` entries (`:887-896`, `:952-960`) are re-measured, may only fall, and move with `A11Y_EXCEPTIONS.md` | A count that rises is a red |
| 20 | Frame: both rows of the pair carry the rail and the badge, and no element computes a `--superset-color-*` value. `superset-edge-cases.spec.ts`: a second pair looks the same | `8b023d1a` colours by group |
| 21 | `exercise-interactions.spec.ts` at 1440 px and at 390 px behind Details: keyboard reach, one `POST /update_exercise` on Enter and on leaving, none on Escape or a blank count, the warning on rejection, the stored value after a reload | The 390 px case and the keyboard case are red before commit 4 |
| 22 | The existing Plan specs, unedited except for the pins Section 0 lists. Each row of the behaviour table gains a 390 px case where it has none. Drag by the handle on a card and in the table. The route pytest files pass unedited | A changed payload fails the existing request assertions |
| 23 | Plan spec reads the heading row and the tabs in one pass. `volume-progress.spec.ts` unedited | Red before commit 4: the summary sits above the filters |
| 24 | Overlay, at 390 and 1440 px in both themes | `8b023d1a` fails the migrated overlays and equals the reference for the unmigrated four |
| 25 — WP9 | Frame source scan and the retargeted cascade tests: no deleted family in `pages-workout-plan.css`, its `!important` at or under the measured bound, no `#clearLogModal` rule and no `!important` in `pages-workout-log.css`, every shared `:is()` group equal to its text on `8b023d1a` | Restoring a deleted rule fails |
| 26 | The four commands above, two Plan runs compared byte for byte, the Log run and its control | The Log control still fails C1–C4 and C10 |
| 27 | The three visual specs on both platforms, `tests/test_css_cascade_contracts.py:65-82` for the 18 bundles, seven-surface Stylelint | An unlisted capture that fails is a regression |
| 28, 29 | PR evidence under `artifacts/design-736/step3/` and the `manual-qa-reviewer` comparison | Review |

**The modal and drawer check.** It opens each modal with `bootstrap.Modal.getOrCreateInstance(el).show()`
and waits for `shown.bs.modal`, so it does not depend on where a trigger sits and runs unchanged
on the control. It opens the drawer with `#vpToggle`. It reads rendered sizes, because
`components.css:2224-2228` counter-zooms `.modal`. `overlay-style.reference.json` is written from
the `8b023d1a` control run, and the control run asserts that the file equals what it measures, so
the reference is not hand-typed.

**Stated limit.** The two checks are opt-in. After merge CI protects only what the required
specs, the contract spec and pytest hold. The pilot recorded the same limit as V-TS-1.

### Visual baselines

**The 26 files**, 13 per platform, for `<platform>` in `win32` and `linux`:

- `e2e/__screenshots__/<platform>/visual.spec.ts-snapshots/workout-plan-{mobile,tablet}-{light,dark}.png` (4)
- `e2e/__screenshots__/<platform>/visual-baseline-thumbnails.spec.ts-snapshots/plan-desktop-light-simple.png` (1)
- `e2e/__screenshots__/<platform>/visual-baseline-thumbnails.spec.ts-snapshots/plan-{mobile,tablet}-{light,dark}-{simple,advanced}.png` (8)

**Order**

1. Before any regeneration, ordinary screenshots (not capture-helper ones) of `8b023d1a` and of
   the branch in the states criterion 28 lists, under `artifacts/design-736/step3/`.
   `manual-qa-reviewer` compares them with the mockup captures and the criteria. This is the
   by-eye sign-off the owner delegated (`RUN_PROMPT.md`, approval 4). A finding is fixed first.
2. win32, locally, with `PW_VISUAL_SEED=1` and a name filter, never a blanket update. The titles
   are `${page} ${viewport} ${theme}` (`e2e/visual.spec.ts:42`) and the capture label
   (`e2e/visual-baseline-thumbnails.spec.ts:55`):
   - `-g "workout-plan (mobile|tablet) (light|dark)$"`; `--list` must return 4.
   - `-g "plan-(mobile|tablet)-(light|dark)-(simple|advanced)$|plan-desktop-light-simple$"`;
     `--list` must return 9.
3. linux: `gh workflow run deep-gate-visual.yml --ref feat/736-workout-plan -f visual_mode=generate`
   on the pushed head. Only the 13 listed files are copied out of the `visual-baselines-linux`
   artifact. The generate step rewrites every capture on the runner
   (`.github/workflows/deep-gate-visual.yml:158`); nothing else is taken from it.
4. The four `snapshotManifest` digests are recomputed with the algorithm at
   `tests/test_css_wp4_4_a_baseline_contracts.py:641-645` (sorted names and byte sizes) and
   hand-edited. `EXPECTED_SNAPSHOT_COUNTS` (`:46-51`) stays at 66 and 15.
5. Every other capture compares clean with no regeneration: the three specs locally on win32,
   then the deep gate in compare mode on the final head with a clean first attempt. `git status`
   must show exactly the 26 PNG files changed. The five exempt captures still have no PNG.

Until the win32 files are pushed, `visual-windows` on the PR is red on the four Plan captures in
`visual.spec.ts`. That is expected and is not a required check.

### Expected gates

From the changed paths, per `QUALITY_GATE.md`. The union is run, never the weaker set.

| Changed paths | Gate |
|---|---|
| `tokens.css`, `components.css`, `layout.css`, `theme-dark.css` (shared surfaces) | Full pytest. Chromium `smoke-navigation`, `nav-dropdown`, `accessibility`, `dark-mode`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening`. The full `visual.spec.ts` matrix with `PW_VISUAL_SEED=1`. `node scripts/css_audit/stylelint_surfaces.mjs`, with no category rising. The Linux visual deep gate, green on its first attempt |
| `pages-workout-plan.css`, `pages-workout-log.css` | Their page specs, their `visual.spec.ts` variants, Stylelint on each edited file |
| `scss/**`, if P8 stands | `/build-css`, then the rebuild check: the old and new compiled files are parsed rule by rule, and every difference must be a removed rule, or a removed branch of a selector list, that names `.vp-` or `#vpToggle`. Anything else stops the run. The compiled-CSS drift contract runs inside full pytest |
| `templates/**`, `static/js/**` | `workout-plan`, `exercise-interactions`, `superset-edge-cases`, `ui-hardening`, `workout-log`, `volume-progress`, `program-backup`, `validation-boundary`, `error-handling`, `empty-states`, `accessibility`, `browser-navigation-state`, `replace-exercise-errors`, `exercise-catalog-fetch`, and a manual smoke on a seeded scratch database |
| `e2e/**` | Each edited spec and check is run. `npx tsc --noEmit`. `--list` on both Playwright configs, to show the checks stay out of the default run |
| Any `.py` | The pyright measurement and `scripts/pyright_baseline_diff.py` |
| Any test added, removed or renamed | `scripts/generate_test_inventory.py`, then `--check` |
| `static/js/**` | `npm run test:js`. No case is added, removed or renamed, so the Vitest inventory pins stay |

Because `table-responsiveness.js` and four shared stylesheets change, the closing gate is
`/verify-and-polish`: `/verify-suite` (full pytest and full Chromium), then `code-reviewer` and
`unslop-reviewer` in fresh contexts with the diff and Section 0's criteria. The three visual specs
are run separately with `PW_VISUAL_SEED=1`. Both frame-check routes and the overlay check are run
twice each. `tests/test_css_theme_dark_p3_audit_contracts.py::test_this_packet_wrote_no_production_css`
is red while a stylesheet edit is uncommitted, as the pilot's Evidence rounds record, and is read
only on a committed tree.

### Risks and open points for the council

**Assumptions P1–P13.** None has a ruling. The plan is drafted as if each stands. Each row gives
the evidence a ruling needs and the smaller option, which the plan can take without other change.

| # | Rule on | Evidence | Smaller, reversible option |
|---|---|---|---|
| P1 | The opening tab is chosen once per load | The default is `'all'` (`workout-plan-state.js:22`). Only a tab click changes it (`workout-plan-table.js:246-263`). The add toast names a routine the tab hides (`workout-plan-add-exercise.js:307-313`). `e2e/workout-plan.spec.ts:329` expects All after adding to a plan that was empty at load | As drafted: one flag, set on the first response |
| P2 | A selected routine that disappears falls back to All | Existing code, `workout-plan-table.js:231-239` | As drafted: no change |
| P3 | Tabs wrap; the label reads workout first | Today's order is environment, program, workout (`workout-plan-helpers.js:82-87`). The Log's caption reads workout first (`templates/workout_log.html:72`). The height of six wrapped tabs on a phone was not measured | Wrap in CSS and keep today's label order: no script change |
| P4 | "Filters · 2 active", chips, Clear Filters always shown | `clearFilters()` also clears the routine and the exercise (`filters.js:174-218`); a chip does not | As drafted: `clearFilters()` is not edited |
| P5 | Details closed on load, three fields to a row | Mockup departure 1. Also: every re-render rebuilds the rows (`workout-plan-table.js:314`), so a reorder or a superset link closes every open card | No memory of open cards. The alternative is a module-private set of open ids for the life of the page |
| P6 | The selection bar is sticky below 1360 px | One declaration (`mockup.html:79`). `.ui-panel` sets no `overflow`, so it sticks inside the panel. WP11 measures it with a row selected | In flow, not sticky |
| P7 | One filled button per modal; `--ui-danger-fill` | `#a84f49` is today's dark `--action-danger` (`tokens.css:460`). The ratios are hand-computed; the overlay check and the `state:modal-open` axe scan measure them | Without the token the confirm button is the outline danger button, which does not meet D17's "filled red on the confirm button" |
| P8 | The drawer's rules leave the Bootstrap build | The `.vp-` selectors exist only in the compiled file, the template and `plan_volume_panel.js`. Six selector lists are shared with Volume Splitter (paths in the artifact table). `[data-theme='dark'] .vp-drawer` (`_workout_plan_volume_panel.scss:231`) outranks a plain `.ui-drawer` rule | Leave the SCSS alone and write the drawer as `.vp-drawer.ui-drawer` in `components.css`: no rebuild and no pin move, but the old rules stay underneath |
| P9 | `--ink-3` reaches the card outline | `visual-field-separator.spec.ts:128-136` reads the first data row's `td` bottom border and `tr` top border. On an empty plan it injects bare rows (`:87-100`), so the rule must be keyed on the table | Only the card outline is ruled: one declaration |
| P10 | The Simple/Advanced toggle shows on cards | `layout.css:1673-1686` hides the six cells at any width, so cards follow the mode with no new code | Hide `.tbl-controls` below 1360 px: one declaration |
| P11 | Empty-plan copy; "Add first exercise" moves focus | `e2e/volume-progress.spec.ts:189-190` opens the drawer on an empty plan. Whether `#routine-env` is replaced by a `.wpdd` button was not verified, so the test asserts the first tabbable control of the panel | As drafted |
| P12 | New copy, `fa-trash`, the neutral badge, the 12 px menu radius, message colours | `fa-trash-alt` is at `templates/workout_plan.html:278`, `:569`, `:580`; `fa-trash` is at `workout-plan-table.js:427`. Each new icon must be in the bundled set (`tests/test_visual_selector_contracts.py:12-20`) | As drafted |
| P13 | The thresholds 200 px, 600 px and 220 px | The mockup measures 150, 581 and 222 to 228. The first card has 19 px to spare against the real navbar, the default summary text and the toggle row, none of which the mockup carries exactly. No built page exists before Gate 1 | Keep the limits. A miss on the built page is a defect to fix, recorded in the evidence round, not a limit to move |

**The four mockup departures** (Section 0, *Mockups*)

| # | Departure | Evidence | Rule on |
|---|---|---|---|
| M1 | Two number fields to a row on the narrowest cards | `mockup.html:115-119`. At scale 8 a card's content box is the layout width less 100 px (two gutters, the panel's and the card's padding and borders): about 167 px at 320 px, 200 px at 360 px and 225 px at 390 px. Three to a row leaves a 50 px field at 320 px, with about 36 px for `102.5` at 16 px text. Two to a row leaves 79 px. By arithmetic, not measured | Accept as the construction above, or hold P5's three to a row and accept a clipped `102.5` at 320 px, which WP11 forbids |
| M2 | A long routine name wraps inside its tab | `mockup.html:39`. The contract's equal-height assertion (`workout-plan-desktop-contract.spec.ts:208-213`) holds at 1440 px with the seed's two tabs; it is not run against the long name | Accept, or truncate with the full name in `title`, which Section 0 does not allow for exercise names |
| M3 | The popover is anchored to the actions row | `mockup.html:42-44`. Section 0's table says "aligned to the button's right edge" | Accept and correct that table cell in Plan v2, or anchor to the button and add a script that flips it |
| M4 | The mockup draws two lists and native selects | The built page keeps one `tr` and `.wpdd`. The card is built by grid placement, not by the mockup's markup, so a mockup measurement is not evidence for the built card | Accept that the `manual-qa-reviewer` comparison and the frame check on the built page are the evidence |

**Questions from this plan**

- **Q1. The modal shadow.** `components.css:2238-2240` sets `box-shadow … !important` on every
  `.modal-content`. A `.ui-modal` rule cannot give `--shadow-elev-2` without `!important`. The
  plan narrows that selector with `:not(.ui-modal)`: the count stays 883 there and the unmigrated
  modals compute the same value, which the overlay check proves. Is editing that shared rule
  acceptable, or should the migrated modals keep the legacy shadow until step 4?
- **Q2. The toggle's chrome is in shared bundles.** `.tbl-view-mode-toggle` is styled at
  `layout.css:1609-1665` and `theme-dark.css:199-220` with a gradient, a shadow, a blur, an 18 px
  radius and 0.8rem text. It fails C2, C3 and C4. Only the Plan's table carries
  `data-table-responsive`, so only the Plan renders it. Section 0 expected no `layout.css` change.
  The plan deletes those rules and adds two classes at `table-responsiveness.js:239`. Accept, or
  keep the rules and restate them with tokens?
- **Q3. Which border the separator checks measure.** Both read the `td` bottom border and the
  `tr` top border and skip a width of `0px` (`workout-plan-desktop-contract.spec.ts:379-380`,
  `visual-field-separator.spec.ts:163`). The shared table draws `border-top`
  (`components.css:5081`), and so does `mockup.html:59`, so a ruled variant that follows either
  would pass on nothing. The plan draws `border-bottom` and adds a width assertion to both specs.
  Section 0 says the contract's fourth test "stays as written" and criterion 18 says the check
  asserts the width. Which governs?
- **Q4. The Plan's capture-helper rules.** `e2e/visual-helpers.ts:197-206` and `:213-215` will
  match nothing. Section 0 lists them as moving. Removing them moves the blind-spot register in
  `scripts/css_audit/measure.py`, its counts at `tests/test_css_wp4_4_a_baseline_contracts.py:282-284`
  and the `oracleBlindSpots` array. The plan leaves the three rules in place and lists them as
  dead. Accept, or remove them and add a `scripts/**` edit to this step?
- **Q5. The stand-in for the five exempt captures** asserts that `[data-visual-surface]` exists
  in the document (`e2e/visual-helpers.ts:84-91`). After the migration the only carriers on the
  Plan are the contents of closed modals, as on the Log. The plan keeps the attribute there. Is
  that enough?
- **Q6. File names for the frame check.** The plan adds a generic launcher and config and leaves
  the two Log-named files as shims, because no file can be deleted. The alternative is to
  generalise the two existing files in place and add `--route`, with no leftover file and a
  misleading name.
- **Q7. The size of the ledger move.** Deleting Plan-only rules shifts every later line of
  `components.css`: the newline count, the `@layer workout` span (3358 to 3923), the `:is(`
  totals (19 falls to 14 if the four input rules hold five) and the `isFamily` records. How many
  `contractAnchors` and `pinnedDeclarations` entries carry a line number was not measured. The
  plan makes all `components.css` deletions in commit 5, so the lines shift once.
- **Q8. The Clear Log rules are not all styling.** `pages-workout-log.css:4-36` sets `z-index`,
  `display` and `pointer-events` with `!important`. Section 0 deletes all 12 rules. Clear Plan
  has no such rules and works on the same Bootstrap modal. The control is the Log's clear flow at
  390 and 1440 px before and after. If it fails, the functional rules stay and the count is
  reported.
- **Q9. Legacy rules outrank the new components.** The Plan's rules in `components.css` carry id
  weight, sit in `@layer workout` (from `:3358`) and use `!important`. A `ui-` rule loses to any
  of them that still matches. The new markup therefore carries none of the legacy classes, and
  the frame check is expected green from commit 5, not commit 4. Is one commit that is not
  frame-green acceptable?
- **Q10. Dropdowns built while hidden.** The filters are `hidden` at load.
  `static/js/modules/workout-dropdowns.js` was not opened. If the `.wpdd` layer measures a select
  when it enhances it, the grid needs a first-open refresh. Whether `selectOption` works on a
  select in the closed panel is also unknown; affected tests open the panel first.
- **Q11. Drag on a card grid.** The checks drag with a mouse on a one-column and a two-column
  grid. Touch dragging is not automated; `manual-qa-reviewer` is asked to try it in device
  emulation.
- **Q12. The overlay fixture has no active volume plan**, so the drawer is measured in its empty
  state and the row chrome is not read. `e2e/volume-progress.spec.ts` covers rows on the
  functional seed. Should the fixture activate a volume plan?

**Not verified in this pass**

- Nothing was run. No measurement of the built page exists.
- Opened only in part: `static/css/pages-workout-plan.css` (headings and `@layer` lines; its
  family ranges are Section 0's), `components.css` (`:2209-2358`, `:3352-3477`, `:5018-5091`),
  `e2e/workout-log-frame.check.ts` (`:1-36`, `:820-1043`), `e2e/workout-plan.spec.ts`,
  `e2e/accessibility.spec.ts`, `e2e/volume-progress.spec.ts` and
  `tests/test_css_cascade_contracts.py` (`:57-121`, `:177-250`, `:1396-1445`).
- Not opened: `workout-dropdowns.js`, `routine-cascade.js`, `exports.js`, `exercises.js`,
  `filter-view-mode.js`, `scripts/css_audit/emit_baseline.py`,
  `tests/test_css_theme_dark_p3_audit_contracts.py`, `tests/test_vitest_inventory_contracts.py`,
  `tests/test_console_guard_contracts.py` beyond `:50`, `docs/product/DESIGN_BRIEF.md` and
  `docs/product/APP_FLOW.md` beyond their headings, and `docs/CSS_OWNERSHIP_MAP.md`.
- Whether a `.check.ts` that imports `./strict-fixtures` is counted by the console-guard pin.
- Which rules in `components.css` name only the Plan and still match the new markup. Commit 5
  starts with that census, made with `scripts/css_audit/measure.py`.
- The server's bound for RPE. The other fixture values are inside the bounds
  `.claude/rules/routes.md` states (weight 0 to 1000 kg, RIR 0 to 10, sets and reps at least 1).
- Whether `layout.css` and `theme-dark.css` carry a line-count or `!important` pin that the Q2
  deletions move.

---

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `a0cf1a8b9a288e254` | Author of Plan v1. Section 0 was written by a different `product-manager`, `a498d607032f21526`. The mockup was built by a general-purpose agent, `afa4d71956251b7be` |
| `product-manager` — response matrix + Plan v2 | `a0cf1a8b9a288e254` | Author of the council section, the response matrix and Plan v2 |
| `architecture-reviewer` | `a25d424cf3e42a127` | Step 2 reviewer |
| `test-strategist` | `a9d8425e1e51c7316` | Step 2 reviewer |
| `product-risk-reviewer` | `a8278cfffbf10c3c0` | Step 2 reviewer |

Every ID above was supplied by the manager. None was invented.

**Same product-manager resumed for the matrix + Plan v2?** `yes` (resumed via `SendMessage` to
the Plan v1 agent ID).

**Evidence gap** — none.

---

## Council review of Plan v1

**Reviewed** — Plan v1 in this file, on `feat/736-workout-plan`, on 2026-11-27. The branch head
was `0573f1f5` when the plan was drafted; the commit the reviewers read was not reported to this
agent. The manager ran the three reviewers and synthesized the proposed
dispositions. Their returns are copied below from `artifacts/design-736/step3/council/`.

**Verdicts**

- `architecture-reviewer` — sound with changes (4 findings, none blocking).
- `test-strategist` — sound with changes (9 findings, none blocking; TS-1 to be fixed before
  implementation).
- `product-risk-reviewer` — sound with changes (5 findings, none blocking).

**Outcome** — No blocking finding is open. Every finding and every ruling is accepted, and Plan
v2 applies them. Nothing is rejected or deferred. Three assumptions were not unanimous: P3 and
P8 change, and P6 stands with a stated fallback. On reading the returns against the code, the
product-manager restated two findings (PR-1, PR-4) and added two (PM-1, PM-2). They are marked
in the matrix and were reported to the manager.

### Response matrix

AR is `architecture-reviewer`, TS is `test-strategist`, PR is `product-risk-reviewer` and PM is
the `product-manager`. "3/3" means all three reviewers gave that ruling.

**Findings**

| ID | Finding | Reviewer | Severity | Disposition | Action in Plan v2 |
|---|---|---|---|---|---|
| AR-1 | A second unscoped `.modal-content` rule (`components.css:2274-2281`) sets a 20 px radius, a glass background, a blur and its own shadow on the element the new modal styles | AR | Non-blocking | Accept | `.ui-modal` declares its radius, border, opaque background, `backdrop-filter: none`, shadow and focus outline explicitly, on the content, the header and the footer. The overlay check asserts a computed `backdrop-filter` of `none` on all three |
| AR-2 | The legacy focus ring (`components.css:2246-2271`, `!important`) applies inside migrated modals | AR | Non-blocking | Accept | The ring is left unchanged. The `state:modal-open` axe scan is the oracle. If it fails, the rule is narrowed the way Q1 narrows the shadow rule |
| AR-3 | `static/js/CLAUDE.md` lists modules by file and the new `ui-menu.js` is not declared | AR | Non-blocking | Accept | `static/js/CLAUDE.md` joins the documents table with one row for `ui-menu.js` |
| AR-4 | Q2 is safe only while `tbl-view-mode-toggle` stays on the toggle; the script looks it up by that class | AR | Non-blocking | Accept | The two classes are appended at `table-responsiveness.js:239`, never substituted. A contract assertion requires the class in the script |
| TS-1 | "Outline" on the card can make both 3:1 checks pass on nothing: an outline computes a border width of 0, and both specs skip a `0px` edge | TS | Non-blocking, to fix before implementation | Accept | The card edge is a real `border` on `tr`. Each layout gets a new `expect` on the edge it draws: the `tr` top border below 1360 px, the `td` bottom border from 1360 px. The existing skip logic is not edited. The four mutation rows are run per layout |
| TS-2 | Tabs set `active` together with `aria-selected`, and `exercise-interactions.spec.ts:634` asserts the class. `:611` selects `#routine-tabs .nav-link`, which may match nothing | TS | Non-blocking | Accept | `active` stays alongside `aria-selected`. **Found:** `.nav-link` matches nothing. The template (`:299-312`) and `workout-plan-table.js:186-197` build `li.routine-tab > button.routine-tab-btn`, and no `nav-link` exists in the template or the Plan's modules. `tabCount` is 0, so the body at `:614-623` never runs. The test "routine tabs filter the table" is not counted as coverage of R3. It is not edited in this step |
| TS-3 | `visual-field-separator.spec.ts:37` selects `table.tbl--responsive`, a class the Plan's table loses | TS | Non-blocking | Accept | The Plan entry becomes `[data-testid="exercise-table"]` in commit 4, the commit that drops the class |
| TS-4 | Criteria 16 and 17 and the contract half of 18 have no PR-time CI path | TS | Non-blocking | Accept | "Expected gates" names a local `PW_VISUAL_SEED=1` run of `workout-plan-desktop-contract.spec.ts` and a deep-gate dispatch on the final head. Listed as a stated limit |
| TS-5 | `:not(.ui-modal)` raises the specificity of an `!important` rule from (0,1,0) to (0,2,0) | TS | Non-blocking | Accept | Q1 uses `.modal-content:where(:not(.ui-modal))`, which keeps (0,1,0) |
| TS-6 | Without `[data-visual-surface]` on page content the capture helper stops flattening the Plan's dark captures, which could flip on Linux | TS | Non-blocking | Accept | After the Linux baselines are copied out, the Linux deep gate runs in compare mode twice on the final head. A flip is a finding, not a retry |
| TS-7 | No test for P2, for P5's re-render, for a drag on a routine's tab, for the menu's keyboard contract or for `.wpdd` dropdowns in the closed panel | TS | Non-blocking | Accept | Five cases are added: the P2 fallback; P5's re-render pinned as a known loss; the two drag cases under PR-1; the menu's keyboard path in `accessibility.spec.ts`; the 12 `.wpdd` triggers' width after the panel opens, at 390 and 1440 px |
| TS-8 | The frame check and the overlay check are opt-in | TS | Non-blocking | Accept | The raw runs are in the PR. The mutation "restoring a deleted rule fails" is run and its output recorded, not claimed |
| TS-9 | `listener-cleanup.spec.ts` is missing from the gates. `test_css_cascade_contracts.py:1396-1413` asserts a Clear Filters rule that goes | TS | Non-blocking | Accept | `e2e/listener-cleanup.spec.ts` joins the gates. The assertion sits in `test_workout_plan_drops_dead_filter_button_family` (from `:1361`). It is retargeted, never deleted |
| TS, commit order | Keep the red-before commit. No `ci.yml` run happens on a branch push without a PR. Dispatch the deep gate only after commit 6 | TS | Note | Accept | The sequence keeps commit 2 red by design. The deep gate is dispatched after commit 6 |
| TS, fixture note | `program-backup.spec.ts:79` is a known flake and the plan edits `:20-37` of that spec | TS | Note | Accept | If it reds, the PR records whether it passes in isolation |
| PR-1 | With D2, a drag in a routine's tab is the default path. It writes that tab's ordinals only, and `exercise_order` is global | PR | Non-blocking | Accept, with the failure restated by PM | Payload and route are unchanged. Two functional cases are added. The PR's migration notes disclose the consequence. The orchestrator opens a follow-up issue. **Restated:** the reviewer wrote that the All tab then interleaves routines. It does not: the page sorts by routine before `exercise_order` (`workout-plan-table.js:322-332`). The payload is 1 to n, not 0 to n-1 (`workout-plan-helpers.js:190`). Details are under *Drag order* in Plan v2 |
| PR-2 | P3 reorders the tab label, against R23 ("labels stay as they are") | PR | Non-blocking | Accept | Tabs wrap in CSS and keep today's order. `formatRoutineForTab()` is not edited. The orchestrator corrects the mockup's tab labels |
| PR-3 | The Goal says "the routine they are about to train". The opening tab is the first by `compareRoutines()`, not the next due | PR | Non-blocking | Accept | The Goal reads "opens on the first routine's tab" |
| PR-4 | P5's list of actions that close open Details is incomplete | PR | Non-blocking | Accept, with one item corrected by PM | The list adds an execution-style save (`workout-plan-execution-style.js:213`). **Corrected:** Swap does not re-render. It updates the row in place (`workout-plan-replacement.js:44-70`) and has no call to `refreshPlan`, so an open card stays open after a swap |
| PR-5 | The overlay check never measures the drawer's rows | PR | Non-blocking | Accept | Recorded as a stated limit. PM-2 adds a source contract for the rows |
| PM-1 | With P3 changed, the tab reads environment, program, workout while Section 0's card caption reads workout first (`Workout A · GYM · Full Body`), on the same page. No reviewer raised it | PM (added) | Non-blocking | Accept as a stated inconsistency | Section 0's caption stands, because it follows the Log's shipped card (`templates/workout_log.html:72`). The PR discloses it. The orchestrator may override before commit 4; the other option is no reorder rule, so the caption reads in tab order |
| PM-2 | With P8 changed, the legacy light and dark rules for the drawer's rows stay live, and the overlay check sees no rows (Q12, PR-5) | PM (added) | Non-blocking | Accept | A pytest contract requires that every property a `.vp-` rule in the SCSS sets on a class the drawer renders is also declared under `.ui-drawer` for that class. One by-eye capture pair shows the drawer with rows in both themes |

**Assumptions P1–P13**

| ID | Rulings | Disposition | Action in Plan v2 |
|---|---|---|---|
| P1 | Accept, 3/3 | Accept | As drafted: one flag, set on the first successful response |
| P2 | Accept, 3/3 | Accept | No code change. A test is added (TS-7) |
| P3 | AR change, PR change, TS accepts wrapping and has no view on the order | Change | Wrap in CSS, keep today's label order, no helper edit (PR-2). Section 0's P3 is corrected |
| P4 | Accept, 3/3 | Accept | As drafted. `clearFilters()` is not edited |
| P5 | Accept, 3/3 | Accept | No memory of open cards. The re-render loss is pinned by a test and listed in the PR (PR-4). Section 0's P5 is corrected for M1 |
| P6 | PR accept, TS accept with a fallback, AR change to in flow | Stands, 2/3. Dissent: AR | Sticky below 1360 px. If WP11 fails with a row selected, the bar goes in flow and the change is recorded |
| P7 | Accept, 3/3 | Accept | As drafted |
| P8 | AR change, TS change, PR accept the rebuild | Change, 2/3. Dissent: PR | `.vp-drawer.ui-drawer` in `components.css`. No SCSS edit and no rebuild. Mechanism and its check are under *Shared components* in Plan v2. Section 0's P8 and two table cells are corrected |
| P9 | Accept, 3/3 | Accept | As drafted, keyed on the table, with TS-1's border |
| P10 | Accept, 3/3 | Accept | As drafted |
| P11 | Accept, 3/3 | Accept | As drafted. The test asserts the first tabbable control of the panel |
| P12 | Accept, 3/3 | Accept | Every icon in the template is checked against the bundled set before commit 4 |
| P13 | Accept, 3/3 | Accept | The limits stay. A miss on the built page is a defect to fix |

**Mockup departures M1–M4**

| ID | Rulings | Disposition | Action in Plan v2 |
|---|---|---|---|
| M1 | Accept, 3/3 | Accept | Two fields to a row inside the container rule. Section 0's P5 and its Details bullet are corrected |
| M2 | Accept, 3/3 | Accept | The fixture's long routine name exercises the wrap. With P3 changed the tab reads `GYM`, `Upper Lower Hypertrophy Split`, `Workout B Heavy` |
| M3 | Accept, 3/3 | Accept | Section 0's popover cell is corrected |
| M4 | Accept, 3/3 | Accept | The built page's frame check and the `manual-qa-reviewer` comparison are the evidence |

**Questions Q1–Q12**

| ID | Rulings | Disposition | Action in Plan v2 |
|---|---|---|---|
| Q1 | AR and PR accept `:not(.ui-modal)`; TS accepts with `:where()` | Accept, in the `:where()` form | See TS-5 and AR-1 |
| Q2 | Accept, 3/3 | Accept | With AR-4. Whether `layout.css` or `theme-dark.css` carry a count pin is still not verified; the contract subset is run after the deletion |
| Q3 | 3/3: the width assertion is added | Accept: criterion 18 governs | With TS-1. Section 0's "stays as written" is corrected |
| Q4 | Accept, 3/3 | Accept | The three capture-helper rules stay and are listed as dead |
| Q5 | Accept, 3/3 | Accept | `[data-visual-surface]` stays on the migrated modals' content. The contract spec is the real guard |
| Q6 | Accept the shims, 3/3 | Accept | As drafted |
| Q7 | Accept, 3/3 | Accept | Every `components.css` deletion is in commit 5 |
| Q8 | Accept, 3/3 | Accept | The Clear Log flow is a Playwright case at 390 and 1440 px, green before and after. If it fails after the deletion, the functional rules stay and the count is reported |
| Q9 | Accept, 3/3 | Accept | One commit may be frame-red. Its reds are confined to legacy-rule collisions, and its functional specs and Vitest are green |
| Q10 | TS accept, PR accept, AR no view | Accept | Tests open the panel before using a filter. The width case from TS-7 is added. PR cites `workout-dropdowns.js:592` as measuring at open, which this agent did not open |
| Q11 | Accept, 3/3 | Accept | Touch drag is tried by `manual-qa-reviewer` in device emulation |
| Q12 | Accept the smaller option, 3/3 | Accept | The overlay fixture has no active volume plan. See PR-5 and PM-2 |

No finding is rejected or deferred.

### architecture-reviewer (agent `a25d424cf3e42a127`)

*Verbatim from `artifacts/design-736/step3/council/architecture-reviewer.md`, without that file's
one-line header.*

**Review: Plan v1, Workout Plan redesign (#736 step 3)**

I read Section 0 and Plan v1 in full. The code claims I checked came from `components.css:2205-2290`, `table-responsiveness.js:169-242`, `templates/base.html:228`, `e2e/scripts/` (file list only) and greps of `theme-dark.css` and `layout.css`. Everything else I cite from the plan is marked "not verified".

**Charter checks: all pass or do not apply**
- **Module boundaries and API:** No file under `routes/`, `utils/` or `app.py` is touched. No blueprint, schema or `run_all_initializers` change is needed.
- **DB access, responses, logging and normalization:** There is no new route, DB access, logging or persisted string, so these do not apply.
- **`utils/__init__.py`:** No re-export is planned.
- **Payload builders:** The plan keeps the seven payload builders unedited, which I did not re-read.
- **Base template:** `templates/base.html:228` does define `{% block main_class %}`, so the `main_class` claim holds. The plan does not edit `base.html`.
- **Shared-state edits:** The plan declares its edits to shared CSS, `DESIGN_BRIEF.md`, `CSS_OWNERSHIP_MAP.md` and `A11Y_EXCEPTIONS.md`.

**Findings**

**AR-1 (non-blocking). Q1 names one shared modal rule, but a second one overrides the same properties.**
- **Evidence:** `components.css:2238-2240` is the `!important` shadow rule the plan names. `components.css:2274-2281` is a second unscoped `.modal-content` rule. It sets a 20 px radius, a glass background, `backdrop-filter: blur(20px)`, a glass border and its own box-shadow.
- **Failure:** The new `.ui-modal` rule must win over this second rule on the same element. It does so only by source order, since both have specificity (0,1,0) and the new rules go after `:5091`. If `.ui-modal` does not declare `backdrop-filter: none` and an opaque background explicitly, the blur leaks through and the "no backdrop-filter" rule in Section 0 fails.
- **Fix:** Add `.ui-modal` to the commit-3 spec as declaring radius, border, background, `backdrop-filter: none` and the focus outline explicitly. Make the overlay check assert computed `backdrop-filter` as `none`.

**AR-2 (non-blocking). The legacy focus ring applies inside migrated modals.**
- **Evidence:** `components.css:2267-2271` sets `.modal *:focus-visible { outline: 2px solid rgba(13,110,253,.5) !important }`, and `:2246-2264` removes focus shadows with `!important`.
- **Failure:** The new modals get a half-opacity legacy blue ring, not an indigo token. Whether it meets the 3:1 contrast check was not verified. If it fails, the `state:modal-open` axe scan reds in commit 5 or 6.
- **Fix:** Say in Plan v2 that the focus ring is left unchanged and that the axe scan is the oracle. If it fails, narrow the rule with `:not(.ui-modal *)`, as Q1 does for the shadow rule.

**AR-3 (non-blocking). A folder `CLAUDE.md` changes without being declared.**
- **Evidence:** `static/js/CLAUDE.md` lists the modules by file. Plan v1 adds `static/js/modules/ui-menu.js` and the artifact table does not list that file.
- **Failure:** Charter point 8 (undeclared shared-state edit). Leaving it out also makes the folder map stale.
- **Fix:** Add `static/js/CLAUDE.md` (one row for `ui-menu.js`) to the documents table, or state that no row is added.

**AR-4 (non-blocking). The plan says the `.tbl-wrap` hooks still hold, and they do.**
- **Evidence:** `table-responsiveness.js:169`, `:190` and `:230` use `closest('.tbl-wrap')`, and `:99-112` finds `.tbl-controls` inside that wrapper. The toggle class is set at `:239`, and `:174` and `:197` look it up by the class `tbl-view-mode-toggle`.
- **Failure:** Q2 is safe only if the class stays on the toggle. Deleting the chrome rules is fine as long as `tbl-view-mode-toggle` remains the hook.
- **Fix:** In the Q2 edit, append `ui-btn ui-btn--small` to the className and never replace it. Add a contract assertion that the class is still present.

**Rulings on P1–P13**
- **P1 accept as drafted.** The default is All (`workout-plan-state.js:22`), and `workout-plan.spec.ts:329` expects All after adding to an empty plan, which one flag set on the first response preserves.
- **P2 accept.** It is existing code and needs no change.
- **P3 change to the smaller option.** Wrap in CSS and keep today's label order (`workout-plan-helpers.js:82-87`). The JS edit to `formatRoutineForTab` buys only a caption order, and nothing is lost by keeping it.
- **P4 accept.** `clearFilters()` also clears routine and exercise, so leaving it unedited is correct.
- **P5 accept the smaller option, no memory of open cards.** The loss is a closed card after a reorder or superset link. That is not a wrong result, and the alternative adds state.
- **P6 change to the smaller option, in flow and not sticky.** It needs no `.ui-panel` overflow assumption, which I did not verify. The cost is one scroll to reach Link on a long list, which does not block the operation.
- **P7 accept.** The token is needed for D17's filled red confirm. The `#a84f49` source at `tokens.css:460` is not verified.
- **P8 accept the smaller option, `.vp-drawer.ui-drawer` and no SCSS rebuild.** The compound selector ties the dark rule at (0,2,0), so order decides. Require the overlay check to read every property the legacy rule sets, so nothing leaks. Bundle load order is not verified.
- **P9 accept as drafted, keyed on the table.** The plan's own evidence is that the separator spec injects bare rows on an empty plan (`visual-field-separator.spec.ts:87-100`), so a card-outline-only rule would pass on nothing.
- **P10 accept as drafted.** The toggle shows at every width. Hiding it on cards would leave only the navbar muscle toggle to reach Advanced fields, and K3 says it stays.
- **P11 accept.**
- **P12 accept.** Confirm that `fa-trash` is in the bundled icon set (`tests/test_visual_selector_contracts.py:12-20`) before commit 4. Not verified.
- **P13 accept.** Keep the limits.

**Rulings on M1–M4**
- **M1 accept.** It is arithmetic only, and WP11 is the measurement.
- **M2 accept.** Wrapping loses nothing.
- **M3 accept.** Correct the Section 0 table cell in Plan v2.
- **M4 accept.**

**Rulings on Q1–Q12**
- **Q1 accept the `:not(.ui-modal)` narrowing.** Without it, `!important` would be needed. See AR-1.
- **Q2 accept.** See AR-4.
- **Q3 the plan governs, adding a width assertion.** A `border-top` ruled variant would pass on nothing. Correct Section 0's "stays as written" wording.
- **Q4 accept.** Leave the dead capture-helper rules and avoid a `scripts/**` edit.
- **Q5 accept.**
- **Q6 accept the shims.** `e2e/scripts/run_workout_log_frame.py` is the only existing launcher (confirmed by the file list), and no file may be deleted.
- **Q7 accept.** Do all `components.css` deletions in one commit.
- **Q8 accept.** Use the Log clear flow as the control.
- **Q9 accept one commit that is not frame-green.** Reds in commit 4 must be confined to the legacy-rule collisions.
- **Q10 no view.** `workout-dropdowns.js` was not opened. Opening the panel first in affected tests is the smaller option.
- **Q11 accept.**
- **Q12 accept the smaller option.** Keep the empty drawer, because `volume-progress.spec.ts` covers rows.

**Verdict: sound with changes.** No finding names a concrete loss, a wrong result or a blocked operation. Apply AR-1 to AR-4 and the P3 and P6 changes in Plan v2.

### test-strategist (agent `a9d8425e1e51c7316`)

*Verbatim from `artifacts/design-736/step3/council/test-strategist.md`, without that file's
one-line header. The reviewer's own headings are demoted to fit this section.*

#### Required gates

Derived from `docs/ai_workflow/QUALITY_GATE.md`. The plan's own "Expected gates" table matches the canonical routing, with the additions in TS-9.

- **pytest: full `pytest`.** The plan edits the shared surfaces `tokens.css`, `components.css`, `layout.css` and `theme-dark.css`, so the full suite is required. It includes:
  - `tests/test_css_cascade_contracts.py`
  - `tests/test_css_wp4_4_{a_baseline,components,i_is_repair,a11y,motion}_contracts.py`
  - `tests/test_css_theme_dark_p3_audit_contracts.py`
  - `tests/test_visual_capture_contracts.py`
  - `tests/test_visual_selector_contracts.py`
  - `tests/test_template_landmarks.py`
  - `tests/test_workout_log_frame_runner.py`
  - `tests/test_playwright_shard_launcher_contracts.py` (the `== 25` pin at `:67` exists)
- **e2e (Chromium):**
  - The shared-surface set: `smoke-navigation`, `nav-dropdown`, `accessibility`, `dark-mode`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening`.
  - The feature-map set for `workout_plan` and `workout-plan`: `workout-plan`, `exercise-interactions`, `superset-edge-cases`. Add `ui-hardening` for Clear Plan, `workout-log` for the Clear Log modal, `volume-progress`, `program-backup`, `empty-states`, `error-handling` and `browser-navigation-state`.
  - The control specs: `exercise-catalog-fetch` and **`listener-cleanup`** (see TS-9).
  - The full `visual.spec.ts` matrix and `visual-baseline-thumbnails.spec.ts`, both with `PW_VISUAL_SEED=1`.
  - `workout-plan-desktop-contract.spec.ts`, run locally with `PW_VISUAL_SEED=1` and in `deep-gate-visual.yml:148`.
  - `visual-field-separator.spec.ts`.
- **other:**
  - Seven-surface Stylelint (`node scripts/css_audit/stylelint_surfaces.mjs`).
  - `/build-css` plus the rebuild check, if P8 stands.
  - `npm run test:js`, `npx tsc --noEmit`, and the pyright baseline diff (any `.py` is touched).
  - `scripts/generate_test_inventory.py --check`.
  - The Linux visual deep gate on the final head, with a clean first attempt.
  - `/verify-and-polish`, with `code-reviewer` and `unslop-reviewer`.
  - **No** change under `.github/workflows/**`.

#### Existing coverage (verified)

- The 26 baselines. The plan's list is correct on disk. Each platform has 4 `workout-plan-{mobile,tablet}-{light,dark}.png` files under `visual.spec.ts-snapshots` and 9 `plan-*.png` files under `visual-baseline-thumbnails.spec.ts-snapshots`, which is 13 per platform.
- `BYTE_GATE_EXEMPT` (`e2e/visual-helpers.ts:58-64`) holds exactly the five names the plan states.
- Contract spec: `e2e/workout-plan-desktop-contract.spec.ts:206` pins `surfaces` at 14, `:215-222` pins page overflow, and `:293` counts `.btn-danger`. `:379-380` and `visual-field-separator.spec.ts:163` skip an edge whose width is `0px`.
- `static/js/modules/__tests__/workout-plan-seams.test.js:45,51-54,73-77` use `toContain` or `toBe` on the functions the plan edits. I did not open `workout-plan-state.test.js` or `workout-plan-helpers.test.js`.
- `e2e/exercise-catalog-fetch.spec.ts` and `e2e/listener-cleanup.spec.ts` exist and are outside the required set.
- `tests/test_ui_flows.py` mentions `workout_plan` 37 times but asserts no template ids. It is unaffected.
- `.check.ts` files do not match the default `*.spec.ts` match. The `playwright.config.ts` grep found no `testMatch` or frame-check entry.

#### Findings

**TS-1 (non-blocking, high value): the "outline" wording can make the 3:1 separator checks pass vacuously.**
- **Evidence.** PLANNING.md "Layout by construction", Separators row: the ruled variant draws `border-bottom` on `td` from 1360 px and "a 1 px `--ink-3` outline on `tbody tr`" below it.
  - `visual-field-separator.spec.ts:134-135` reads `trs.borderTopWidth`, and `:163` returns early on `0px`.
  - `workout-plan-desktop-contract.spec.ts:380` does the same.
  - A CSS `outline` computes `border-top-width` as 0.
- **Failure.** At 375 and 768 px the `td` border is not drawn (the plan draws it only from 1360 px), and the `tr` edge would be an outline. Both edges skip, so a 1.29:1 hairline or no separator at all passes criterion 18.
- **Fix.**
  - Draw the card outline as a real `border` on `tr`.
  - Add the width assertion as a new `expect`, not as an edit to the early return. At each viewport assert the edge that layout draws: `tr` top border below 1360 px, `td` bottom border from 1360 px.
  - Do not assert both edges at every width. At 1440 px the `tr` border is legitimately 0.
  - The plan's own mutation rows ("set it to 0 fails") only prove this if the assertion is per-layout.

**TS-2 (non-blocking): the opening-tab and tab-state hooks are underspecified.**
- **Evidence.** `workout-plan-table.js:201-254` sets the `active` class together with `aria-selected`. `exercise-interactions.spec.ts:622,634` assert `toHaveClass(/active/)` on `#tab-all`. The plan's pin table does not list them.
- **Failure.** If the new `ui-tab` styling keys on `aria-selected` only and the JS drops `active`, `:634` goes red.
- **Fix.** State that `active` stays alongside `aria-selected`.
- **Related.** `exercise-interactions.spec.ts:611` selects `#routine-tabs .nav-link`. `workout-plan-table.js` has no `nav-link`, and I did not check the template. If the selector matches nothing, `if (tabCount > 1)` skips the whole body and the test passes today without testing anything. It is outside this plan's scope, but do not count it as coverage of R3.

**TS-3 (non-blocking): the `visual-field-separator` Plan selector must change in the same commit.**
- **Evidence.** `visual-field-separator.spec.ts:37` is `table.tbl--responsive`. The plan drops `tbl--responsive` from the Plan table.
- **Failure.** `missing: true` fails the test in the required functional gate, and `:185-186` follows.
- **Fix.** Retarget to `[data-testid="exercise-table"]`. This spec is in the required set, so it must move in commit 4, not commit 6. The plan's sequence puts these pins in commit 4, which is consistent.

**TS-4 (non-blocking): two criteria with no CI-required test.**
- **Evidence.** `workout-plan-desktop-contract.spec.ts` runs only in `visual-linux` (weekly or dispatch, `deep-gate-visual.yml:148`) and locally with the visual seed.
- **Failure.** Criteria 16 and 17, and the contract half of criterion 18, have no PR-time CI path.
- **Fix.** The PR must carry a local `PW_VISUAL_SEED=1` run of the contract spec. A dispatch of the deep gate on the final head is also needed. The plan names "visual-linux" but not the local run in "Expected gates".

**TS-5 (non-blocking): Q1's `:not(.ui-modal)` raises the specificity of an `!important` rule.**
- **Evidence.** `components.css:2238` is `.modal-content { box-shadow … !important }`, at specificity (0,1,0). `:4199` is `[data-theme='dark'] .modal-content.frame-calm-glass`.
- **Failure.** `:not(.ui-modal)` makes it (0,2,0), so it can now beat other `!important` box-shadow rules on the four unmigrated modals. The overlay check would catch it, but only after the fact.
- **Fix.** Use `.modal-content:where(:not(.ui-modal))`, which keeps specificity identical.

**TS-6 (non-blocking): the capture helper stops flattening the Plan's dark captures.**
- **Evidence.** `visual-helpers.ts:173-193` flattens dark borders and backgrounds only on `[data-visual-surface]`. The plan removes that attribute from page content.
- **Failure.** `workout-plan-mobile-dark` and `plan-*-dark-*` are captured without the determinism layer, and `workout-plan-mobile-light` has a recorded 13 px flip. These could flip on Linux.
- **Fix.** The plan's "clean first attempt" compare is the right control. Add: after the baselines are copied out, run the Linux deep gate in compare mode twice, and treat any flip as a finding, not a retry.

**TS-7 (non-blocking): plan items with no test.**
- **P2.** Remove the last exercise of the opening tab and assert All becomes selected. No named test.
- **P5.** A reorder or superset link closes open Details. Pin it either as intended behaviour or as a known loss.
- **Drag on the opening tab.** Drag now posts only that tab's rows by default. The plan itself concedes this ("becomes the common case"). Add a case: drag on the opening tab, reload, and assert the other routines' order is unchanged. Whether the route tolerates a partial list is **not verified**.
- **`ui-menu.js` and the chip renderer.** They have no Vitest case, only Playwright. This is acceptable because the plan promises no Vitest add or rename, but the keyboard contract (arrows, Escape, focus return) must be in `accessibility.spec.ts` as the plan says.
- **`.wpdd` dropdowns in a hidden panel (Q10).** Add: open the filters, then assert all 12 `.wpdd` triggers have non-zero width at 390 and 1440 px.

**TS-8 (non-blocking): the frame check and the overlay check are opt-in (V-TS-1).**
- **Fix.** The PR must show raw runs, as planned. The WP9 source scan and the retargeted cascade tests are the only durable guard. Mutation row 25 ("restoring a deleted rule fails") must be run, not claimed.

**TS-9 (non-blocking): gate additions.**
- Add `e2e/listener-cleanup.spec.ts`. It covers detached picker and dropdown listeners, and the plan adds delegated listeners in `filters.js`.
- `test_css_cascade_contracts.py:1396-1413` asserts `#workout[data-page="workout-plan"] #clear-filters-btn.btn {` survives in the CSS. It is probably one of the ten `test_workout_plan_*` tests, but I did not confirm which. If Clear Filters becomes `ui-btn`, retarget it deliberately. Do not delete the assertion.

**Not blocking, verified clean.** `tests/test_ui_flows.py`, `test_template_landmarks.py:15`, and the `== 25` pin are unaffected by the plan's file set.

#### Coverage gaps (new tests to write)

- **`e2e/workout-plan.spec.ts`**
  - P2 fallback to All.
  - Drag on the opening tab, then reload.
  - Hidden-panel `.wpdd` width.
  - The No-flash `data-plan-state` case is frame-check only.
- **`e2e/visual-field-separator.spec.ts` and the contract spec**
  - The per-layout width assertion (TS-1).
- **`e2e/accessibility.spec.ts`**
  - The menu keyboard path and focus return after a modal.

#### Conftest / fixture work

None. No blueprint or table is added. `e2e/frame-check.ts` is a helper and not a spec, so it is not counted in the inventory. The new `.check.ts` files stay out of the default run. Regenerate `docs/test_inventory/` after the changes to `tests/test_workout_log_frame_runner.py` and the specs. Known-red: `e2e/program-backup.spec.ts:79`. The plan edits that spec's lines `:20-37`. If it reds, record whether it passes in isolation.

#### Rulings on the open points

**Assumptions**
- **P1:** accept. It keeps `workout-plan.spec.ts:329` true.
- **P2:** accept. It is today's behaviour. Add the test from TS-7.
- **P3:** accept wrapping. Keep today's label order (the plan's "smaller option") if the `formatRoutineForTab` reorder touches `workout-plan-seams.test.js:51-54`. Those cases use `toContain`, so the reorder is safe either way. No view beyond that.
- **P4:** accept. `clearFilters()` stays unedited, and tests click Clear Filters without opening the panel.
- **P5:** accept (closed on load, no memory of open cards).
- **P6:** accept, but the smaller option is "in flow, not sticky". WP11 measures it with a row selected, so keep sticky only if that check passes.
- **P7:** accept.
- **P8:** change to the smaller, reversible option: `.vp-drawer.ui-drawer` in `components.css`, with no SCSS rebuild. The rebuild moves a generated artifact, a contract pin and an extra stop condition. The old rules stay underneath. That is not a concrete loss, and a later step can delete them. If the owner wants the deletion, keep the plan's rebuild check as drafted.
- **P9:** accept. The pilot spec needs a drawn border (see TS-1).
- **P10:** accept.
- **P11:** accept. Assert the first tabbable control of the panel, as drafted.
- **P12:** accept. Every new icon must be in the bundled set.
- **P13:** accept. A miss on the built page is a defect, not a limit to move.

**Mockup departures**
- **M1:** accept (two fields to a row at narrow widths). It satisfies WP11 by construction.
- **M2:** accept. The equal-height assertion (`:208-213`) is not run against a long name, so add one to the fixture. The plan's fixture already has a long routine name.
- **M3:** accept, and correct the Section 0 table cell.
- **M4:** accept.

**Questions**
- **Q1:** accept with the `:where()` form (TS-5).
- **Q2:** accept. Only `workout_plan.html:330` carries `data-table-responsive`, and no test asserts the toggle's chrome. I did not check `layout.css` or `theme-dark.css` for line-count pins.
- **Q3:** criterion 18 governs. Add the width assertion as a new `expect` and keep the existing skip logic. Draw the card edge as a `border` (TS-1).
- **Q4:** accept (leave the dead capture rules). See TS-6 for the determinism side.
- **Q5:** accept with a note. `visual-helpers.ts:84` counts the whole document, so closed modals keep it above zero even if page content has none. The Plan's contract spec is the real guard.
- **Q6:** accept the shims.
- **Q7:** accept (all `components.css` deletions in commit 5).
- **Q8:** accept (run the Clear Log flow before and after, and keep the functional rules if it fails).
- **Q9:** accept one commit that is not frame-green, provided commit 4's functional specs and Vitest are green.
- **Q10:** accept with the hidden-panel width case from TS-7.
- **Q11:** accept (manual).
- **Q12:** accept (the drawer in its empty state). `volume-progress.spec.ts` covers rows.

**Commit order.** Keep the plan's order, red-before at commit 2. No `ci.yml` run happens on a non-PR branch push. The deep-gate dispatch uses the pushed head, so dispatch only after commit 6.

#### Verdict

**Sound with changes.** No finding names a concrete loss, a wrong result or a blocked operation.

TS-1 is the one to fix before implementation, because it decides whether criterion 18 can fail. TS-2 to TS-9 are non-blocking.

**Not verified:**
- `workout-plan-state.test.js` and `workout-plan-helpers.test.js` contents.
- The `/update_exercise_order` partial-list behaviour.
- Whether `layout.css` or `theme-dark.css` carry line-count pins.
- Which `test_css_*` assertions move beyond those the plan lists.
- Whether `#routine-tabs .nav-link` matches anything.

### product-risk-reviewer (agent `a8278cfffbf10c3c0`)

*Verbatim from `artifacts/design-736/step3/council/product-risk-reviewer.md`, without that file's
one-line header. The reviewer's own headings are demoted to fit this section.*

#### Review of Plan v1, #736 step 3 (Workout Plan)

**Verdict: sound with changes.** I found no blocking finding. Nothing in Plan v1 or Section 0 needs more than presentation, and nothing contradicts an owner answer, so nothing has to go back to the owner.

##### What I verified

- **No calculation, schema or response-shape change.**
  - The artifact list touches no file under `routes/` or `utils/`.
  - `applyRoutineTabFilter` filters rows already fetched (`workout-plan-helpers.js:102-107`).
  - Inline edit does not re-fetch the plan. `refreshPlan` is called only after drag (`workout-plan-table.js:712,717`), superset link and unlink (`workout-plan-supersets.js:197,224`) and an execution-style save (`workout-plan-execution-style.js:213`).
  - No `utils/effective_sets.py` or fatigue surface is touched, and the page adds no Effective/Raw gating.
- **Local-first.** The plan adds no accounts, no cloud sync and no telemetry. Opening on the first tab needs only a module-private flag, with nothing written to storage (R3, `workout-plan-state.js:22`). That honours D2's "nothing remembered between visits". The drawer's existing `vpDrawer.open` persistence stays.
- **Copy.**
  - Today's Excel export label is "Export All Tables" (`templates/workout_plan.html:239`), and the plan keeps it (K13).
  - "Volume targets", "Superset", "RIR" and "RPE" are unchanged.
  - The mockup's prescription line uses RIR and RPE in the canonical form.
- **Backup contract.** No schema change, so existing backups stay restorable.
- **Only the Plan renders the Simple/Advanced toggle.** `data-table-responsive` appears only at `templates/workout_plan.html:330`.
- **Mockups viewed:** `populated-390-light.png` and `clear-plan-modal-390-light.png`. They match the brief, with one filled primary, a neutral Superset rail and badge, and a filled danger confirm.

##### Findings

**PR-1 — non-blocking. Drag reorder in a tab becomes the default path.**
- Evidence: `workout-plan-table.js:701-702` posts 0..n-1 for the visible tab's rows only. `routes/workout_plan.py:444` writes those values to `exercise_order`, which is global across routines. `routes/workout_plan.py:204` orders by `exercise_order, routine, exercise`. New rows are placed at max+1 (`utils/exercise_manager.py:59`).
- Failure: with D2 the first tab is the opening view, so a drag in a later routine writes small ordinals that tie with the first routine's. The All tab then interleaves rows from different routines. It is today's behaviour, but it now happens routinely.
- Fix: keep the payload and route unchanged, because API shapes are frozen. Put it under the PR's migration notes as a known consequence of D2. Add one functional case that drags within a second routine's tab and asserts that tab's order after reload.

**PR-2 — non-blocking. P3 reorders the tab label, which conflicts with K13/R23 ("labels stay as they are").**
- Evidence: `workout-plan-helpers.js:82-87` emits environment, program, workout. Plan v1 changes `formatRoutineForTab` to workout first. R23 says labels stay.
- Failure: the tab text no longer matches the Add-exercise breadcrumb, the cascade or the existing copy, and the change is not listed as a wording change.
- Fix: take P3's smaller option, wrap tabs in CSS and keep today's order. Regenerate the mockup's tab labels to match (see the M-list below).

**PR-3 — non-blocking. The Goal sentence overstates D2.**
- Evidence: the Goal reads "the routine they are about to train". The opening tab is the first routine by `compareRoutines` (`workout-plan-helpers.js:89-100`), which is alphabetical by environment, program, then workout. It is not recency or "next up".
- Failure: the PR text would promise something the page does not do.
- Fix: reword to "opens on the first routine's tab", as D2 says.

**PR-4 — non-blocking. P5's evidence is incomplete.**
- Evidence: the plan names reorder and superset link as the actions that close open Details. An execution-style save (`workout-plan-execution-style.js:213`) and Swap also re-render.
- Failure: a user on a phone who changes an execution style sees the card collapse. This is mild.
- Fix: add both to P5's list and to the PR's behaviour notes. The ruling does not change.

**PR-5 — non-blocking. The overlay check never measures the drawer's rows.**
- Evidence: the frame check reads "every overlay closed", and Q12's fixture has no active volume plan.
- Failure: the rows' 12 px radius and type sizes (the D17 drawer style) are covered by no C2/C3 reading.
- Fix: record this as a stated limit next to the opt-in limit. Activating a volume plan in the fixture is optional.

##### Rulings on P1–P13

| # | Ruling | Evidence |
|---|---|---|
| P1 | Accept | The add toast already covers a routine hidden by the tab (`workout-plan-add-exercise.js:307-313`). An empty plan stays on All. |
| P2 | Accept | Existing behaviour, `workout-plan-table.js:231-233`. |
| P3 | Change: keep today's label order | See PR-2. |
| P4 | Accept | A chip is a single-filter clear, and `clearFilters()` stays unedited, so nothing silently changes meaning. |
| P5 | Accept, with PR-4 | No memory of open cards is the smaller and more reversible option. |
| P6 | Accept | A superset message is invisible deep in a card list unless the bar sticks. WP11 measures the occlusion, and the fallback is in-flow. |
| P7 | Accept | D17 requires a filled red confirm. `#a84f49` is today's dark `--action-danger`. |
| P8 | Accept | `[data-theme='dark'] .vp-drawer` outranks plain `.ui-drawer` rules, so the old dark rules would override the tokens. The plan's rebuild check (only `.vp-` removals) is adequate. I did not open the SCSS: not verified. |
| P9 | Accept | Keying the rule on the table, as the empty-plan injection at `visual-field-separator.spec.ts:87-100` needs, is right. |
| P10 | Accept as drafted | Hiding the toggle below 1360 px would remove the Advanced-only fields from phones and contradict K3/R25. |
| P11 | Accept | Asserting the first tabbable control of the panel is the right hedge. |
| P12 | Accept | The icon names must be checked against the bundled set before commit 4. I did not verify them. |
| P13 | Accept | A miss on the built page is a defect to fix, not a limit to move. |

##### Rulings on M1–M4

| # | Ruling | Evidence |
|---|---|---|
| M1 | Accept | A clipped `102.5` at 320 px at scale 8 is forbidden by WP11. |
| M2 | Accept | Truncating names was ruled out in Section 0. |
| M3 | Accept | Correct Section 0's popover cell ("aligned to the button's right edge") in Plan v2. |
| M4 | Accept | The frame check on the built page and the `manual-qa-reviewer` comparison are the evidence. |
| (new) | Follows PR-2 | Mockup tab labels must revert to environment · program · workout order. |

##### Rulings on Q1–Q12

| # | Ruling | Evidence |
|---|---|---|
| Q1 | Accept `:not(.ui-modal)` | The unmigrated modals compute the same value, and the overlay check proves it. The alternative breaks D17's shadow. |
| Q2 | Accept | Only the Plan renders the toggle (`templates/workout_plan.html:330`). The chrome fails C2, C3 and C4. |
| Q3 | Accept the plan | Adding a width assertion strengthens the check and does not weaken it. Correct Section 0's "stays as written" in v2. |
| Q4 | Accept | Leave the dead helper rules and avoid a `scripts/**` edit. |
| Q5 | Accept | |
| Q6 | Accept shims | R27 says no file is deleted. |
| Q7 | Accept | A single commit of deletions shifts the lines once. |
| Q8 | Accept | Make the Log clear-flow control a Playwright case, not a by-eye one. The rules at `pages-workout-log.css:4-36` set `pointer-events` and `z-index` with `!important`. |
| Q9 | Accept | The branch is not pushed for review until commit 6. |
| Q10 | Accept | `workout-dropdowns.js:592` measures at open, not at enhance. Whether `selectOption` works on a hidden select is not verified. The tests should open the panel first. |
| Q11 | Accept | |
| Q12 | Accept the smaller option | See PR-5. |

##### Owner-answer check

- D1 (list first, then the Add exercise panel), D3 (collapsed, with chips), D4 (Export in the header, the rest in More) and D24 are all met.
- D5 (cards below 1360 px), D6, D7 and D17 are met as the plan describes them.
- D2 is met, with the PR-1 consequence disclosed.

---

## Plan v2

Product-manager `a0cf1a8b9a288e254`, 2026-11-27. This revision adopts Plan v1's scope, artifact
tables, sequence, layout rules, script changes, frame check, criterion table, baseline list and
gates. The text below supersedes the matching v1 text. Every disposition in the response matrix
is applied. As with v1, nothing was run: statements about files come from opening them.

**Goal** — A populated plan opens on the first routine's tab. A lifter reads and edits each
exercise on a card on a phone or in a contained table on a desktop, and adds an exercise from one
panel, on the frame and components the Workout Log already uses.

**No calculation, schema or response-shape change** — as in v1, re-checked for the order route
(see *Drag order*). No file under `routes/` or `utils/` is edited.

### What changed from Plan v1

| Area | Plan v1 | Plan v2 | From |
|---|---|---|---|
| Tab label | Workout first, by editing `formatRoutineForTab()` | Today's order. The helper is not edited | P3, PR-2 |
| Drawer | SCSS edit and Bootstrap rebuild | `.vp-drawer.ui-drawer` rules. No SCSS edit, no rebuild, no pin move | P8 |
| Legacy modal shadow rule | `:not(.ui-modal)` | `.modal-content:where(:not(.ui-modal))` | Q1, TS-5 |
| Modal rules | Surface, header, title, close, body, footer | The same, with every property the two legacy `.modal-content` rules and the header and footer rules set declared explicitly | AR-1 |
| Card edge below 1360 px | "Outline" on `tbody tr` | A `border` on `tbody tr` | TS-1 |
| Separator specs | A width assertion | One new `expect` per layout; the skip logic is untouched | TS-1, Q3 |
| Tab state | Not stated | `active` stays with `aria-selected` | TS-2 |
| Toggle class | "Also carries" | Appended, with a contract assertion | AR-4 |
| Tests | v1's list | Seven cases added; see *Tests added to v1's list* | TS-7, PR-1, Q8 |
| Gates | v1's table | The `scss/**` row goes. Three runs are added | TS-4, TS-6, TS-9 |
| Documents | v1's table | `static/js/CLAUDE.md` is added | AR-3 |

### Artifacts — changes to the v1 tables

**Removed**

- `scss/pages/_workout_plan_volume_panel.scss`, `static/css/bootstrap.custom.min.css` and its
  `.map`: not edited.
- The edit to `tests/test_css_cascade_contracts.py:114-121`: that pin does not move.
- The change to `formatRoutineForTab()` in `workout-plan-helpers.js`. The file's only change is
  `renderExecutionStyleBadge()` (`:143`).

**Changed**

| Path | Plan v2 |
|---|---|
| `static/css/components.css` | Adds `.vp-drawer.ui-drawer` and its descendants in place of a plain `.ui-drawer` family. Edits `:2238` to `.modal-content:where(:not(.ui-modal))`. `.ui-modal` declares the properties listed under *Shared components* |
| `templates/workout_plan.html` | `#vpDrawer` keeps `vp-drawer` and gains `ui-drawer`. `#vpActiveSummary` loses `vp-active-summary` and its wrapper loses `vp-header-summary`, because the old rules for those classes stay live (`_workout_plan_volume_panel.scss:1-26`, `:218-229`). Both ids stay. No test, and none of the Plan's modules, reads either class. Every `fas` icon is checked against the bundled set first (P12) |
| `static/js/modules/workout-plan-table.js` | As v1. The `active` class is still toggled with `aria-selected` (`:199-254`). Tab labels come from the unedited helper |
| `static/js/table-responsiveness.js` | `:239` becomes `'tbl-view-mode-toggle ui-btn ui-btn--small'`. The first class is the lookup key at `:174` and `:197` and is never removed |
| `e2e/visual-field-separator.spec.ts` | The Plan entry at `:37` becomes `[data-testid="exercise-table"]`. One new `expect` per layout for the Plan surface. `:163` is not edited |
| `e2e/workout-plan-desktop-contract.spec.ts` | As v1, plus one new `expect` that `separatorWidth` is above 0, placed before the call at `:396`. `:379-380` is not edited |
| `e2e/overlay-style.check.ts` | Also reads `backdrop-filter` on each migrated modal's content, header and footer, and on the drawer's shell every property the legacy light and dark rules set |
| `tests/test_css_cascade_contracts.py` | As v1 without `:114-121`. `test_workout_plan_drops_dead_filter_button_family` keeps its hook assertions (`:1397-1404`) and has its Clear Filters assertion (`:1406-1413`) retargeted: the template's `#clear-filters-btn` carries `ui-btn`, and the page bundle holds no `#clear-filters-btn` rule. Two assertions are added: `tbl-view-mode-toggle` is in the class string at `table-responsiveness.js:239`, and the drawer contract below |

**Added**

| Path | Change | Writer |
|---|---|---|
| `static/js/CLAUDE.md` | One row for `modules/ui-menu.js` | `senior-developer` |

### Shared components

**Modal (AR-1, AR-2, Q1).**

- The `ui-modal` class goes on the `.modal-content` element, which is what lets the `:where()`
  form below exclude a migrated modal. The two widths are classes on `.modal-dialog`
  (`ui-modal-dialog--confirm`, `ui-modal-dialog--wide`). Plan v1 did not say which element
  carries the class.
- `.ui-modal` declares, on `.modal-content`: `border-radius`, `border`, an opaque `background`,
  `backdrop-filter: none` and `box-shadow`. On `.modal-header` and `.modal-footer`: `background`,
  `backdrop-filter: none`, `border`, `border-radius` and `padding`. On `.modal-body`: `padding`
  and `background`. Those are the properties the legacy rules at `components.css:2274-2306` set.
- The legacy shadow rule becomes `.modal-content:where(:not(.ui-modal)) { box-shadow … !important }`.
  Its specificity stays (0,1,0) and the `!important` count stays 883 at that point.
- The focus ring inside a modal is the legacy one (`components.css:2246-2271`) and is not
  changed. The `state:modal-open` axe scan decides. If it fails, that rule is narrowed with the
  same `:where(:not(…))` form.

**Drawer (P8, changed). Plan v2 uses the compound selector, not the rebuild.** The manager asked
for a check of whether it can win without `!important` or a `[data-theme]` selector. It can:

- **Load order.** `bootstrap.custom.min.css` is linked at `templates/base.html:16`,
  `components.css` at `:22`, the page bundle at `:27` and `theme-dark.css` at `:29`.
- **The legacy rules.** `scss/pages/_workout_plan_volume_panel.scss` was read whole. It has no
  `!important`. Its strongest dark rules are one attribute and one class, (0,2,0), such as
  `[data-theme='dark'] .vp-drawer` (`:231`), and one at (0,2,1),
  `[data-theme='dark'] .vp-drawer__header h2` (`:241`).
- **The new rules.** `.vp-drawer.ui-drawer` is (0,2,0). A part is written `.ui-drawer .vp-row`,
  also (0,2,0), and the title `.ui-drawer .vp-drawer__header h2`, (0,2,1). Each ties its legacy
  competitor and loads later, so it wins on order. No rule uses `!important` or `[data-theme`.
- **C8 holds.** The new rules carry no `[data-theme`. The scan also skips `.min.css` files
  (`e2e/workout-log-frame.check.ts:1027`).
- **Full shadowing.** A tie on order wins only for the properties the new rule declares. The new
  rules therefore restate every property the old ones set, including position, size,
  `transform` and today's 220 ms transition. A later deletion of the SCSS rules then changes
  nothing. The shell goes in `components.css`. The rows (`.vp-list`, `.vp-row*`, `.vp-progress`,
  `.vp-dot`, `.vp-state*`, `.vp-bonus*`) go in `pages-workout-plan.css`, unscoped by `#workout`
  because the script moves the drawer to `body` (`plan_volume_panel.js:36-45`).
- **Checks.** The overlay check reads, on the drawer, its header, title, close button, body and
  state box, every property the legacy light and dark rules set, in both themes. The rows are not
  rendered in that fixture, so a pytest contract covers them at source: for each `.vp-` class the
  drawer renders, every property a rule in the SCSS partial sets for it must be declared under
  `.ui-drawer` for the same class in `components.css` or `pages-workout-plan.css` (PM-2).
- **What stays underneath.** The `.vp-` and `#vpToggle` rules in the SCSS and in the compiled
  file. They are listed for the owner as a later deletion. `#vpToggle { width: 100% }` at 576 px
  and below (`:289-299`) stays live and agrees with the full-width heading row below 768 px.
- **Fallback.** If the contract or the overlay check shows a legacy value that cannot be
  shadowed without `!important`, the run falls back to v1's rebuild with its stop check, and the
  change is recorded here.

**Ruled table and card (TS-1, Q3).**

- Below 1360 px: `.ui-data-table--ruled tbody tr { border: 1px solid var(--ink-3) }`. It is a
  border, not an outline, and it is keyed on the table so the bare rows the separator spec
  injects take it. Cells draw no border.
- From 1360 px: `.ui-data-table--ruled tbody td` has `border-top: 0` and
  `border-bottom: 1px solid var(--ink-3)`. The row declares no border.
- `visual-field-separator.spec.ts` asserts, for the Plan only, a `tr` top border above 0 at 375
  and 768 px and a `td` bottom border above 0 at 1440 px. The contract spec asserts the `td`
  bottom border at 1440 px.
- Mutations, run and recorded after commit 5. For each of the two layouts: the border colour set
  to `--ui-hairline` must fail the ratio, and the border width set to 0 must fail the new
  `expect`.

### Tabs, Details and drag

- **Tabs (P3, TS-2).** Tabs wrap in CSS. The label is today's three spans in today's order. A
  tab is styled from `aria-selected`, and the script keeps toggling `active`, which
  `e2e/exercise-interactions.spec.ts:634` reads.
- **Selection bar (P6).** Sticky below 1360 px. If WP11 fails with a row selected, it goes in
  flow.
- **What closes an open card (P5, PR-4).** Any re-render: a tab click
  (`workout-plan-table.js:262`), a drag (`:712`, `:717`), a superset link or unlink
  (`workout-plan-supersets.js:197`, `:224`), an execution-style save
  (`workout-plan-execution-style.js:213`), and an add or a remove. A swap and an inline edit
  update the row in place and leave the card open. The loss is pinned by a test and listed in
  the PR.

**Drag order (PR-1).** The manager asked what the order route does with a partial list.

- `POST /update_exercise_order` (`routes/workout_plan.py:421-451`) checks that each entry has an
  id and an order, then runs one `UPDATE user_selection SET exercise_order = ? WHERE id = ?` per
  entry in one transaction. It does not require the whole plan. A partial list is tolerated: a
  row the payload does not name keeps its value.
- A drag on a routine's tab writes 1 to n for that tab's rows (`workout-plan-helpers.js:190`).
  Rows of different routines can then hold equal values.
- The page is not affected: it sorts by routine before `exercise_order`
  (`workout-plan-table.js:322-332`), so the All tab keeps each routine together. The Excel export
  also orders by routine first (`utils/export_service.py:291`).
- Two readers order by `exercise_order` first: the raw `/get_workout_plan` response
  (`routes/workout_plan.py:204`), which the page re-sorts, and the backup snapshot
  (`utils/program_backup.py:258`). Whether a restore depends on that order was not verified.
- The payload and the route are not changed. The PR's migration notes say that, with D2, a drag
  usually reorders one routine. The follow-up issue for equal values across routines is the
  orchestrator's to open.

### Tests added to v1's list

All are written by `automation-qa` in commit 2. No spec file is added.

| Case | Spec | On `8b023d1a`'s page |
|---|---|---|
| P2: on a routine's tab, remove its last exercise; All is selected | `workout-plan.spec.ts` | Green (today's behaviour) |
| P5: with a card's Details open, a superset link and an execution-style save close it; a swap and an inline edit do not. Marked as a known loss | `workout-plan.spec.ts`, at 390 px | Red (no Details) |
| PR-1: drag within a second routine's tab, reload, assert that tab's order | `exercise-interactions.spec.ts` | Green |
| TS-7: drag within the first routine's tab, reload, assert the other routines' order is unchanged and All lists each routine together | `exercise-interactions.spec.ts` | Green |
| Menu: Enter, Space and ArrowDown open; arrows move; Escape closes and focuses More; focus returns to More after a modal opened from the menu | `accessibility.spec.ts` | Red |
| Q10: after the filters open, each of the 12 `.wpdd` triggers has a width above 0, at 390 and 1440 px | `workout-plan.spec.ts` | Red (no toggle) |
| Q8: Clear Log opens, cancels, confirms and clears, at 390 and 1440 px | `workout-log.spec.ts` | Green; it must stay green after the 12 rules go |

Whether `workout-log.spec.ts` already holds the Q8 flow at both widths was not checked; the case
is added only where it is missing. The test at `exercise-interactions.spec.ts:607-624` is not
counted as coverage of R3 (TS-2).

### Sequence — changes to the v1 table

Plan v1's seven commits, writers and rules stand. These rows change.

| # | Commit | Change from v1 |
|---|---|---|
| 2 | Acceptance tests | Two lists are recorded in the evidence round: the cases that are red, each for the reason it tests, and the characterization cases that must be green now and stay green (P2, the two drag cases, Q8) |
| 3 | Shared components and tokens | The modal's explicit declarations, the `:where()` form, and the drawer's shell as `.vp-drawer.ui-drawer`. No SCSS and no rebuild |
| 4 | Template and scripts | The icons are checked first. The separator spec's selector and its per-layout `expect` move here. The drawer's rows and the drawer contract land here |
| 5 | Deletions | The 12 Clear Log rules go only if the Q8 case stays green. The mutations for criteria 18 and 25 are run and their output kept |
| 6 | Pins and documents | Adds `static/js/CLAUDE.md`. The contract spec is run locally with `PW_VISUAL_SEED=1`. The branch is pushed and the PR opened after this commit, and the deep gate is first dispatched then |
| 7 | Baselines | After the 13 Linux files are copied out and committed, the deep gate runs in compare mode twice on that head |

### Expected gates — changes to the v1 table

- **Removed:** the `scss/**` row. Nothing is rebuilt, so `/build-css` and the rebuild check do
  not run.
- **Added to `templates/**`, `static/js/**`:** `e2e/listener-cleanup.spec.ts`, outside the
  required set, run as a control for the delegated listeners.
- **Added:** `PW_VISUAL_SEED=1 npx playwright test e2e/workout-plan-desktop-contract.spec.ts --project=chromium`,
  locally, with its output in the PR. It is the only PR-time evidence for criteria 16 and 17 and
  the contract half of 18.
- **Added:** `gh workflow run deep-gate-visual.yml --ref feat/736-workout-plan` in compare mode
  on the final head, twice. Both runs must be green on the first attempt. A capture that passes
  once and fails once is a finding to investigate, not a retry.
- If `e2e/program-backup.spec.ts` reds at its known flake (`:79`), the PR records whether it
  passes in isolation.

### Stated limits

1. The frame check and the overlay check are opt-in. After merge, CI protects only what the
   required specs, the contract spec and pytest hold.
2. Criteria 16 and 17 and the contract half of 18 have no PR-time CI path. Their evidence is the
   local contract run and the deep-gate runs.
3. The overlay check does not render the drawer's rows. The source contract and one by-eye
   capture pair with an active volume plan cover them.
4. The Plan's dark captures are no longer flattened by the capture helper. The double compare
   run is the control.
5. Touch drag on a card grid is tried by hand, not automated.
6. A re-render closes an open card.
7. The tab reads environment, program, workout and the card caption reads workout first (PM-1).
8. The three Plan rules in `e2e/visual-helpers.ts` (`:197-206`, `:213-215`) and the drawer's
   SCSS rules stay as dead or shadowed code and are listed for the owner.

### For the orchestrator

These are outside this document and outside this agent's writes.

- Open the follow-up issue for equal `exercise_order` values across routines, with the facts
  under *Drag order*.
- Correct the mockup's tab labels to environment, program, workout.
- Confirm or override PM-1 before commit 4.
- List P1–P13, M1–M4, Q1–Q12, PM-1 and PM-2 in the PR under "Decisions taken without the owner",
  and put the D2 drag consequence and the P5 loss in its migration notes.
- Consider a follow-up for the test at `e2e/exercise-interactions.spec.ts:607-624`, which runs
  no assertion today.

**Orchestrator's record, 2026-11-27** (Claude, the orchestrating session):

- PM-1 is confirmed as recorded: the card caption stays workout first, as on the Log's card, and
  the tab keeps today's order. It is the smaller change and is listed in the PR.
- The mockup's three tab labels now read environment, program, workout. Its captures under
  `artifacts/design-736/step3/mockups/` were taken before that correction and still show the old
  label order on the tabs.
- Issue #750 was opened for equal `exercise_order` values across routines and closed the same
  day as not a defect. It was opened from PR-1 as first written, before the page's own sort by
  routine (`workout-plan-table.js:320-332`) was checked. Its correction comment carries the
  facts under *Drag order*. The two drag cases stay in the test list.
- No follow-up is opened for `e2e/exercise-interactions.spec.ts:607-624`. This step's new R3
  cases cover the opening tab; the vacuous test is named in the PR.

### Not verified in Plan v2

- Everything under "Not verified in this pass" in Plan v1 still applies, except the order
  route's handling of a partial list and the `.nav-link` selector, both now checked.
- `static/js/modules/workout-dropdowns.js` was not opened. `:592` is the product-risk
  reviewer's citation.
- `components.css:4199`, cited in TS-5, was not opened.
- Whether a restore depends on the row order of a backup snapshot.
- Whether `e2e/workout-log.spec.ts` already covers the Clear Log flow at 390 and 1440 px.
- The add and remove paths' calls to the plan refresh were not opened; they are listed as
  re-renders from the wiring at `workout-plan.js:83` and from Section 0's behaviour table.

---

## Sign-off

- [x] **Gate 0.** The owner's "Decisions" reply of 2026-11-26 is the Gate 0 answer for steps 3 to
  5. The two owner confirmations in Section 0's Gate 0 block stay unticked; the status note
  there explains why.
- [x] **Every finding has a disposition.** See the response matrix. None is rejected or deferred.
- [x] **Agent provenance complete.** Both `product-manager` IDs, same-PM-resumed `yes`, the three
  reviewer IDs, and an evidence gap of `none`.
- [x] **Plan v2 approval (Gate 1) — delegated, not an owner sign-off.** Gate 1 approved by Claude
  under the owner's delegation of 2026-11-20. Recorded on 2026-11-27 at the orchestrating
  session's instruction. Grounds: the council ran (`architecture-reviewer` `a25d424cf3e42a127`,
  `test-strategist` `a9d8425e1e51c7316`, `product-risk-reviewer` `a8278cfffbf10c3c0`), every
  finding has a disposition, and no blocking finding is open. The delegation is the owner's
  sentence in `artifacts/design-736/RUN_PROMPT.md`, "Approvals I am giving", item 2. The owner
  has not reviewed Plan v2, and an owner answer overrides it.
- [x] **Ready to implement.** The orchestrator proceeds under Plan v2. The `product-manager`
  stops here.

## Migration-test isolation prerequisite

A source inspection on 2026-11-27 confirmed two paths from tests to installation data. The no-override fresh interpreter in `test_real_app_db_isolation.py` could migrate the installation database, and its state checks also enumerated the installation's backup directory. In `test_runtime_migration.py`, passing an explicit scratch database and destination still left the parameterless backup copy using the installation and runtime defaults.

The question for the council was whether to run the fresh probes from an allowlisted disposable installation, redirect the path resolver in the probes, or use a different test-only design. Architecture, test strategy and product risk each voted for a disposable application installation for the subprocess probes and private installation and runtime roots for the in-process migration tests. The second-vendor review agreed. The physical installation exercises the production resolver with real source and the public catalog seed, while the default backup-copy path can be tested on synthetic snapshots. The decision affects test fixtures only.

The isolation prerequisite is PR #751. The ordinary frame-runner tests on the Plan branch passed all 26 cases and commit 1 is `d8b2d52f`. On the prerequisite branch, 106 tests passed across the two migration modules, the runtime initialization module and the app factory module. The test inventory matched and Pyright reported zero diagnostics. Independent code and maintainability reviewers ran. The code review led to moving two adjacent import and snapshot probes onto the same private installation. Full local pytest on the Plan branch resumes only when the fixture isolation is present there.


PR #751 merged as `1facfe6c` on November 27 after all 12 required contexts passed on `1ed54a46`. Gate 2 for the isolation prerequisite was approved by Astra under the owner's delegation of 2026-11-27.

### Acceptance tests before the redesign

The functional cases below all failed at their first design assertion on the original page. The three narrow-phone cases reached the card assertion with app scale 8 selected by cookie. Later assertions in these cases still need a passing implementation.

- More supports click and keyboard, ordered items, Escape and modal focus return
- empty Plan offers the starter and focuses the first Add exercise control
- drags the phone card by its handle and writes the same payload as the table
- keyboard edits and rejection › edits a field by keyboard, saves once, discards drafts and warns on rejection at 390 px
- keyboard edits and rejection › edits a field by keyboard, saves once, discards drafts and warns on rejection at 1440 px
- phone links a second pair with the same neutral rail and badge and can unlink it
- opens on the first routine, exposes All by pointer and keyboard, and never remembers the choice
- shows only Add Exercise as filled primary and puts volume above the tabs at 390 px
- collapses filters and renders all 12 dropdown triggers when opened at 390 px
- shows only Add Exercise as filled primary and puts volume above the tabs at 1440 px
- collapses filters and renders all 12 dropdown triggers when opened at 1440 px
- names active filter chips and removing one sends one filter request
- phone Details › reveals the approved Simple and Advanced fields by touch and keyboard and closes after reload
- fits widest realistic values and card actions at 320 px and scale 8
- fits widest realistic values and card actions at 360 px and scale 8
- fits widest realistic values and card actions at 390 px and scale 8
- card Details closes on link and execution-style rerenders but stays open on swap and inline edit
- phone Add exercise preserves cascade, validation, estimate request, hidden-routine toast and control values
- phone exports the current mode to Excel, follows Backup Center and exports to Workout Log
- phone starter generation keeps its payload and Clear Plan resets the six controls
- phone card keeps thumbnail preview and plays and dismisses the curated reference video
- swap errors › phone card reports each established swap rejection and keeps its exercise

Five characterization cases passed on the original page. Removing the last exercise in a selected routine returned to All. Dragging in the first or second routine persisted after reload and preserved the other routine's order. The Clear Log cancel and confirm flows passed at both 390 and 1440 px. Both established catalog controls also passed.

Both new opt-in checks passed their historical control at `8b023d1a`. C1–C5 and WP10 failed as expected on Plan. The four retained modals matched their measured references across both widths and themes, and all 20 comparisons for the overlays slated for migration detected a difference. The reference records geometry at the plan's half-pixel precision. Both opt-in candidates were red before implementation. The targeted Python run had 71 passes and one expected failure for the missing Add exercise heading. TypeScript passed.

Local evidence is under `artifacts/design-736/step3/commit2-qa/`. The functional logs are `12-characterization.txt`, `18-acceptance.txt` and `24-catalog-control.txt`. The Plan controls and candidates are in `16-plan-control.txt` and `17-plan-candidate.txt`, overlay results in `22-overlay-control.txt` and `23-overlay-candidate.txt`, and the Python result in `20-pytest.txt`.

### Dark modal surfaces

How can the migrated dialogs become opaque while the four retained dialogs keep their dark glass appearance? The dark stylesheet applies five important declarations to every `.modal-content`. Architecture and product risk voted to scope that rule to the existing `.frame-calm-glass` class. Test strategy voted for a separate opt-out attribute to preserve the legacy default on any future unmarked Bootstrap modal. The 2–1 decision is to use `:where([data-theme="dark"] .modal-content.frame-calm-glass)` when the templates migrate in commit 4. All eight current modal contents have the glass class. The four migrated surfaces will drop it, and the four retained surfaces will keep it. A future unmarked Bootstrap modal will not inherit the dark glass fallback from this rule.

The second-vendor review suggested negating the glass class on the premise that the four retained surfaces lacked it. Inspection of the Welcome, Progression and Volume Splitter templates contradicts that premise. The measured legacy overlay references remain the acceptance check. Restoring the original broad dark selector should fail a migrated dark-dialog check.

### Shared component verification

The final additive styles passed all 100 Windows visual and desktop-contract cases on the original markup. Each of the 22 functional acceptance cases still failed, the same five characterizations stayed green, and the template-order test still failed at the Add exercise heading. The opt-in Plan and overlay candidates also retained their expected failures.

Across the seven shared stylesheets the same Stylelint configuration reported 2,652 warnings on the historical control and 2,651 on the candidate. No category increased. The drawer backdrop token retains the existing SCSS color. Component-owned class names on modal parts and tab items avoid introducing new descending-specificity findings and will be added alongside their Bootstrap and routine classes in commit 4. The stylesheet contracts passed 96 focused cases. The broader 260-case CSS run found only the audit that intentionally fails whenever production CSS has uncommitted edits. The components bundle still contains 883 important declarations.

Evidence lives under `artifacts/design-736/step3/commit3-final-visual-cd631978/`, `commit3-final-functional-2b574fdc/` and `commit3-pins/`.

### Template and interaction verification

The first successful Plan GET sets the opening routine and reveals the list. The same rows serve the cards and the desktop table. The media fixtures now enter through that GET and still verify exact image paths, attributes and escaping. Removing a filter chip sent one POST containing the remaining Equipment selection. Each of the three subsequent routine changes sent its own POST with that same selection. Clear Filters reset all 17 controls.

The first phone run exposed a 29 px Swap target and an execution-style picker that pushed Apply off screen when AMRAP expanded. The corrected controls passed the real 320, 360 and 390 px scale-8 cases. The three-row drag test now verifies that the pointer hits both intended rows below the navbar and the new order survives a reload. The frame then found that the sticky superset controls covered Details on selected cards. Under the approved P6 fallback, the selection bar stays in normal flow. The frame waits for the navbar to leave compact mode after the preceding keyboard-scroll test before it reads both positions together.

All 22 acceptance tests and five characterization tests passed, alongside four media/helper cases and the cross-page dark-theme check. The 16 desktop contracts passed in four theme/detail combinations, as did 39 cases covering volume progress, supersets and related workflows. All 271 JavaScript unit tests passed. TypeScript and the generated inventory passed.

The final frame run passed C1, C5, WP10 and all 262 Plan-specific observations. C2, C3, C4 and the WP9 source checks still see the legacy styles scheduled for deletion. The temporary selector scopes separate migrated controls from legacy WPDD and table rules during this commit. The ordinary population probe identified the exact controls involved, including the routine selectors, match count, execution badge, mode toggle and Clear Filters. The overlay check still saw legacy padding and phone targets on Generate and the dark legacy surface on Clear Log. All four retained dialogs matched their references.

The dark audit mutation script now checks the measured LF-normalized SHA-256 of the stylesheet with the glass selector narrowed. Its CRLF test uses the measured Windows bytes. The input check and refusal for an unexpected digest are still exercised. The source audit yielded 249 passes and its intentional dirty-production-CSS failure before commit. The four axe states were measured against their previous exact registers. Counts fell, and the register and its companion document move together after the CSS retirement.

Evidence is under `artifacts/design-736/step3/` in `commit4-final-behavior-8316c6a7/`, `commit4-desktop-fixes-d94e174f/`, `commit4-preserved-workflows-f699df0a/`, `population-probe-p2572wtj/` and `commit4-unit/`. The raw final frame data is `artifacts/frame-check/workout_plan/candidate-p9z11yhm/metrics.json`.

### CSS retirement and phone verification

The Plan stylesheet went from 6,390 to 1,999 lines. Its three remaining important declarations are covered by the source check. The shared components stylesheet went from 883 to 539 important declarations, and the Workout Log page stylesheet went from ten to zero. The Clear Log cancel and confirm flows passed at phone and desktop widths. The seven shared stylesheets produced 1,939 Stylelint warnings compared with 2,652 on the control, with no category increasing.

At 320 px and scale 8 the Barbell Squat card had 167.375 CSS pixels available inside its padding. Removing just the narrow container rule made its six numeric fields form two rows of three. The weight field still had a 60.56 px hit target and stayed inside the card, but its value of 102.5 wrapped. With the rule present it measured 95.64 px across and the number fit on one line. The functional case and the opt-in frame now check the rendered field order and line positions in open Details. The unmodified CSS passed the three functional widths. Intercepting the stylesheet and removing the rule failed both tests, including WP11 at 320 px and scale 8.

The manual reviewer compared ordinary captures with the mockup and exercised touch drag. The review found overlapping routine text on phones, broken numeric and heading text on desktop, and unreadable text in the dark Generate and Clear Log dialogs. After corrections the reviewer found the affected states legible and approved the named baseline updates. Q5's three modal markers remain in the markup. The light estimate caption now uses the secondary text token. Fresh axe scans found zero contrast violations in the light and dark Plan, open modal and validation-error states.

Both runs of each opt-in check passed for Plan, overlays and Log. The two Plan measurements are byte-identical (SHA-256 `ca3a8f0dff38760aac4264d23d6ec915ac1b153948cb21eb7d8f840402cf764b`). Mutation output, rendered boxes and functional results are under `artifacts/design-736/step3/wp11-controls/`, the repeated checks under `resume-frames-6c01eb35/`, and the four measured accessibility states under `resume-caption-b68bf4b0/`. The earlier selector, separator, desktop overflow, overlay and More menu controls are in `commit5-gates/`.

### Accessibility register and visual review

The light and dark Plan and the required-field validation state each have one `aria-allowed-attr` target (the exercise picker button) and two `aria-hidden-focus` targets (the exercise select and the volume drawer). The modal-open scan has one `aria-allowed-attr` target. All four have zero contrast violations. The register and the exceptions document record these counts together.

The first full functional run passed 635 of 638 cases, and all 37 backup cases passed separately. The three failures identified two stale test assumptions. The accessibility test needs a populated plan to check its table headings, and the Clear Log tests need to identify Cancel by its accessible name. Those three cases and the four axe states passed in a six-test targeted run.

The full functional rerun passed all 638 Chromium cases in 10.9 minutes on the corrected tests (`resume-final-functional-ed1b82b7/result.txt`).

A by-eye review of the phone Generate dialog identified a partially visible routine preview. After scrolling the modal vertically, the last letter was still at x=421 px in both themes, beyond its preview box (x=356) and the dialog body (x=373). Allowing the routine badge to wrap put its complete text on two lines ending at x=289. Two fresh runs of the overlay check passed. The reviewer inspected the scrolled preview in both themes and approved the 13 named baseline updates per platform. In the ordinary caption captures, “default values” is the text of the estimate provenance element.

Evidence under `artifacts/design-736/step3/` includes the empty and populated control in `ordinary-before-6rxztlpt/`, additional populated states in `ordinary-before-d22816il/`, and 88 final ordinary captures in `ordinary-after-0ae5e3cx/`. All 87 Windows visual cases outside the named update list passed on the existing baselines (`resume-other-visuals-033c6a9c/`). The retained desktop exemptions ran at their actual viewport. TypeScript, the zero-diagnostic Pyright gate, the test inventory, all 271 Vitest cases and the selection of four full-page and nine thumbnail cases passed.

### Config test isolation prerequisite

The scratch-only full Python run exposed an order-dependent configuration test. The no-directory probe reloaded the shared `utils.config` module inside the temporary environment, including in its cleanup. The next test inherited that temporary data directory alongside the outer run's database path. Three other override probes also reloaded the shared module. The ordered config module reproduced the failure with a precreated scratch data directory and both path overrides present.

Architecture and test strategy voted for a separate test-only prerequisite PR. Product risk voted for a separate commit in the Plan PR. The second-vendor adviser preferred an inline change and recommended executing the config source in a private namespace. Its assumption about the cleanup order disagreed with the source. The decision was to isolate all four probes in a separate PR, preserve the assertions, then rerun the complete Plan suite with both scratch overrides. Git Bash and PowerShell were also selected by their installed executable directories for the Windows launcher tests.

PR #753 implements the prerequisite. Its independent reviewers passed the final test module. All 20 tests passed in order. A separate run verified that all five cached configuration values and the four outer environment overrides survived the four probes. Test inventory and the zero-diagnostic Pyright check passed.

Gate 2 for the config prerequisite was approved by Astra under the owner's delegation of 2026-11-27. All 12 required checks passed on `03203924` and the branch contained the freshly fetched main. The owner-authorized squash merge produced `a28a9394`. The Workout Plan branch integrated it at `a1811035`. [Prerequisite PR](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/753) · [Issue checkpoint](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/736#issuecomment-7227954923)

### Named visual baselines

The full browser rerun also passed all 37 isolated backup tests (`resume-final-backup-6e5c03c4/`). The two name-filtered Windows updates selected four full pages and nine thumbnails. A fresh Windows comparison then passed all 100 visual and desktop-contract cases without retries (`final-windows-compare-c76787a9/`). The Linux generator ran on `eb552666` and produced the normal artifact. Only the same 13 named Linux files were copied. The diff matched the 26 approved PNG paths exactly, and the four manifest entries retained their original file lists and counts. [Linux generation run](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/46065138183)

### Integrated validation

The full local Python suite on `a1811035` passed 7,008 tests with three skips in 19 minutes and 17 seconds. Eight workers ran with file-level distribution and private runtime, database, cache and temporary paths. The run used the installed Git Bash and PowerShell executables. Output is in `artifacts/p736-check-704b537/full-pytest.log`.

Both the snapshot commit and the integration commit passed all 100 Linux visual and desktop-contract cases on the first attempt. Windows CI also passed the visual comparison on the integration commit. All 12 required checks passed on that head. [Snapshot comparison](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/46065780475) · [Integration comparison](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/46066805786) · [Windows visual check](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/46066788986/job/140734537491)

### Independent review corrections

The code reviewer found that saving Sets by clicking All could leave the newly mounted row one save behind, and an older catalog response could overwrite a newer filter choice. A browser history restoration kept the previous tab. Rejected Weight and RIR values displayed a generic error. In dark mode Swap still inherited the old blue paint, and hovering an editable number painted a pencil over it.

All eight targeted controls failed on the previous code (`review-red-84fa88d7/`). The revised implementation passed those cases and the related catalog controls, 11 in total (`review-green-803ce1fb/`). Tests delivered real successful responses in reverse order for filtered, routine and unfiltered catalogs. A genuine Back navigation from Backup Center restored the document from Chromium's back-forward cache in both probes. On the control All remained selected. After the fix the first routine was selected. The browser recorded transparent Swap fill and border in both idle and hover, and no pencil over the hovered value. The native browser evidence is in `artifacts/p736-check-10f4edd/` and `artifacts/p736-check-dae505a/`.

All 271 Vitest cases passed. The generated inventory contains 780 Chromium cases and 77 hard waits. The Stylelint report matched the previous report byte for byte. The two exact CSS contract files passed all 17 cases. The only new rule separates legacy Swap colors from the layout of the control. The shared stylesheet has 4,599 lines, 132,438 normalized bytes and 539 important declarations. A fresh round of 88 ordinary captures is in `artifacts/design-736/step3/ordinary-after-d5jvy3p3/`.

The independent manual reviewer compared the updated ordinary captures with the original page, earlier candidate and mockup, including both themes, phone and desktop, the 320 px Details, caption and scrolled preview. The reviewer approved the changed subset of the same 13 files per platform. Exactly six per platform changed after this correction, all dark phone or tablet images. All 100 local Windows comparisons passed on those files without retries (`review-windows-compare-9be6d36c/`). [Linux generation after review](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/46070288222)

The post-review functional run passed 641 of 643 cases, and all 37 isolated backup cases passed. Two superset cases tried to add an exercise while its profile estimate was arriving. The failure screenshot showed 68–12 reps where the fixture intended 8–12. The server correctly rejected the reversed bounds. The setup now waits for the existing estimate-readiness marker after selecting an exercise and asserts both filled values before submitting. All 17 cases in the superset spec passed on a fresh database (`superset-ready-c14c92c0/`). The revised snapshots passed all 100 Linux cases without a retry. [Linux comparison](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/46070825866)
